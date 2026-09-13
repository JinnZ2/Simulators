# test_loop.py
# CC0 1.0 Universal / public domain dedication.
#
# Stdlib only, no pytest, no network. Run: python3 test_loop.py
#
# Expected verdicts live HERE and not in cases.py, so no case can agree with
# the module by construction.

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cases
import loop_weight as lw
from loop_weight import Carries, LoopRead
from tools.authority_scan import PLANT, scan, split_identifier

CHECKS = []


def check(name, condition, detail=""):
    CHECKS.append((name, bool(condition), detail))


def read_by_id(source_id):
    for case in cases.CASES:
        if case["source_id"] == source_id:
            return lw.read(case)
    raise KeyError(source_id)


READS = [lw.read(c) for c in cases.CASES]


# ---------------------------------------------------------------------------
# 1. every enum member is reachable by at least one case
# ---------------------------------------------------------------------------

produced = set(r["verdict"] for r in READS)
for member in LoopRead:
    hits = [r["source_id"] for r in READS if r["verdict"] is member]
    check("reachable: %s" % member.name, hits,
          "cases: %s" % ", ".join(hits) if hits else "NO CASE PRODUCES THIS MEMBER")
check("no member is declared and unpopulated",
      produced == set(LoopRead),
      "%d of %d members produced" % (len(produced), len(list(LoopRead))))

# every Carries member must also be reachable, for the same reason
carries_seen = set()


# ---------------------------------------------------------------------------
# 2. the four named cases resolve as the work order marks them
# ---------------------------------------------------------------------------

EXPECTED = {
    "A_one_hop_unchecked": LoopRead.SHORT_UNCALIBRATED,
    "B_one_hop_scored": LoopRead.SHORT_CALIBRATED,
    "C_four_hop_relay": LoopRead.LONG_CALIBRATED,
    "D_two_hop_lossy": LoopRead.LOSSY,
    "E_one_hop_wrong": LoopRead.SHORT_MISCALIBRATED,
    "F_six_hop_unchecked": LoopRead.LONG_UNCALIBRATED,
    "G_five_hop_diverging": LoopRead.LONG_MISCALIBRATED,
    "H_path_not_described": LoopRead.INSUFFICIENT,
    "I_correlated_others": LoopRead.SHORT_MISCALIBRATED,
    "J_derivations_disagree": LoopRead.SHORT_MISCALIBRATED,
}
for source_id, expected in EXPECTED.items():
    got = read_by_id(source_id)["verdict"]
    check("case %s resolves %s" % (source_id, expected.name), got is expected,
          "got %s" % got.name)


# ---------------------------------------------------------------------------
# 3. THE FALSIFIER. case C must carry more than case A, and by the
#    calibration rule -- not by accident of some other axis.
# ---------------------------------------------------------------------------

a = read_by_id("A_one_hop_unchecked")
c = read_by_id("C_four_hop_relay")
verdict = lw.carries_more(c, a)
carries_seen.add(verdict["verdict"])
check("FALSIFIER: case C carries more than case A",
      verdict["verdict"] is Carries.FIRST_CARRIES_MORE,
      "got %s" % verdict["verdict"].name)
check("FALSIFIER: decided by the calibration rule, not another axis",
      verdict["rule"] == lw.RULE_CALIBRATION_ESTABLISHED,
      "rule was %s" % verdict["rule"])
check("FALSIFIER: and case A's loop really is the shorter one",
      a["loop_length"] < c["loop_length"],
      "A L=%s, C L=%s -- a short loop did not rescue an unchecked instrument"
      % (a["loop_length"], c["loop_length"]))
reverse = lw.carries_more(a, c)
carries_seen.add(reverse["verdict"])
check("FALSIFIER: the comparison is antisymmetric",
      reverse["verdict"] is Carries.SECOND_CARRIES_MORE,
      "got %s" % reverse["verdict"].name)


# ---------------------------------------------------------------------------
# 4. no authority-named field exists in the module or the case set
# ---------------------------------------------------------------------------

FORBIDDEN = {
    "credential", "credentials", "title", "titles", "rank", "ranking", "ranked",
    "seniority", "senior", "tenure", "institution", "institutional",
    "citation", "citations", "cited", "follower", "followers",
    "publication", "venue", "journal", "volume", "reach", "audience",
    "prestige", "authority", "eminence", "standing", "reputation",
}


for path in ("loop_weight.py", "cases.py"):
    hits = scan(open(path).read(), FORBIDDEN)
    check("no authority-named field in %s" % path, not hits,
          "found %s" % hits if hits else "0 identifiers or keys match the forbidden set")

# null test on the checker: it must fire on a plant, or its silence above
# means nothing.
plant_hits = scan(PLANT, FORBIDDEN)
check("the authority checker fires on a planted identifier",
      len(plant_hits) >= 2, "plant hits: %s" % plant_hits)
check("the authority checker does not fire on a near-miss token",
      not scan("reachable = 1\nsubtitle_note = 2\n", FORBIDDEN),
      "token-split matching, not substring")


# ---------------------------------------------------------------------------
# 5. C is never self-reported, and never imputed
# ---------------------------------------------------------------------------

for case in cases.REFUSED:
    try:
        lw.read(case)
        refused = False
    except lw.SelfSuppliedRefused:
        refused = True
    check("refused at load: %s" % case["source_id"], refused,
          "a calibration input supplied by the source, or with no stated supplier, "
          "must raise rather than be silently dropped")

check("C is None when neither derivation is available, not a default",
      a["calibration"]["value"] is None
      and a["calibration"]["state"] == lw.CAL_UNKNOWN,
      "value=%r state=%r" % (a["calibration"]["value"], a["calibration"]["state"]))
check("UNCALIBRATED and MISCALIBRATED are separate returns",
      read_by_id("E_one_hop_wrong")["verdict"] is LoopRead.SHORT_MISCALIBRATED
      and a["verdict"] is LoopRead.SHORT_UNCALIBRATED,
      "unmeasured is not low")
unknown_vs_low = lw.carries_more(a, read_by_id("E_one_hop_wrong"))
carries_seen.add(unknown_vs_low["verdict"])
check("unmeasured against measured-low is INCOMPARABLE, not ranked",
      unknown_vs_low["verdict"] is Carries.INCOMPARABLE
      and unknown_vs_low["rule"] == lw.RULE_KNOWN_LOW_VS_UNKNOWN,
      "%s by %s" % (unknown_vs_low["verdict"].name, unknown_vs_low["rule"]))


# ---------------------------------------------------------------------------
# 6. no scalar collapse
# ---------------------------------------------------------------------------

check("carries_more returns an ordinal verdict, not a number",
      isinstance(verdict["verdict"], Carries),
      "type %s" % type(verdict["verdict"]).__name__)
COLLAPSE_NAMES = {"score", "weight", "rating", "total", "combined", "overall",
                  "composite", "index"}
collapse_keys = [k for k in read_by_id("C_four_hop_relay")
                 if set(split_identifier(k)) & COLLAPSE_NAMES]
check("the read record carries no combined field", not collapse_keys,
      "keys: %s" % collapse_keys if collapse_keys else
      "L, R and C are three separate fields")
check("all three axes survive into every record",
      all(set(("loop_length", "per_hop_retention", "calibration")) <= set(r)
          for r in READS),
      "including on LOSSY and INSUFFICIENT, where the label reports only one")
check("DECLARATION states no scalar collapse and no self-report",
      lw.DECLARATION["scalar_collapse"] is False
      and lw.DECLARATION["self_report_admitted"] is False)
check("DECLARATION lists every return",
      lw.DECLARATION["returns"] == [m.name for m in LoopRead])

# R is the per-hop minimum and is NOT carried through L as a product: a
# cumulative figure would fuse the channel with the topology, which is the
# collapse this instrument exists to refuse.
c_hops = [h["retention"] for h in cases.CASE_C["path"]]
product = 1.0
for value in c_hops:
    product *= value
check("R is per-hop, not cumulative",
      abs(c["per_hop_retention"] - min(c_hops)) < 1e-9
      and abs(c["per_hop_retention"] - product) > 1e-6,
      "R=%.4f, min=%.4f, product would be %.4f" % (c["per_hop_retention"],
                                                   min(c_hops), product))


# ---------------------------------------------------------------------------
# 7. R dominates L, and L does not override R
# ---------------------------------------------------------------------------

d = read_by_id("D_two_hop_lossy")
check("LOSSY fires though D's loop is shorter than C's",
      d["verdict"] is LoopRead.LOSSY and d["loop_length"] < c["loop_length"],
      "D L=%s, C L=%s" % (d["loop_length"], c["loop_length"]))

# a short loop through a lossy channel against a longer clean one, both
# calibrated: the work order states the long clean read may carry more.
short_lossy = lw.read({
    "source_id": "T_short_lossy", "referent": "t",
    "path": [{"id": "t_h1", "retention": 0.3}],
    "comparisons": [{"id": "t_c1", "other_hop_ids": ["z1"],
                     "independence_asserted": True, "agreement": 0.9,
                     "supplied_by": "auditor"}],
    "predictions": [],
})
channel = lw.carries_more(c, short_lossy)
carries_seen.add(channel["verdict"])
check("a longer clean read carries more than a short lossy one",
      channel["verdict"] is Carries.FIRST_CARRIES_MORE
      and channel["rule"] == lw.RULE_CHANNEL_CARRIES,
      "%s by %s" % (channel["verdict"].name, channel["rule"]))

check("unknown retention on a hop does not make a read LOSSY",
      read_by_id("F_six_hop_unchecked")["retention_unknown_hops"] > 0
      and read_by_id("F_six_hop_unchecked")["verdict"] is not LoopRead.LOSSY,
      "unknown is not low")


# ---------------------------------------------------------------------------
# 8. independence: shared hops, contradicted assertions, correlated others
# ---------------------------------------------------------------------------

f = read_by_id("F_six_hop_unchecked")
f_c1 = f["calibration"]["c1"]
check("a pair sharing a hop with the source is excluded",
      any(x["reason"] == "shares_hop_with_source" for x in f_c1["pairs_excluded"]),
      "%s" % f_c1["pairs_excluded"])
check("an independence assertion contradicted by a shared hop is reported",
      len(f_c1["independence_assertions_contradicted"]) == 1,
      "%s" % f_c1["independence_assertions_contradicted"])
check("C-1 with no admissible pair is None, not zero",
      f_c1["value"] is None
      and f_c1["unavailable_because"] == "no_admissible_independent_pair")

i = read_by_id("I_correlated_others")
i_c1 = i["calibration"]["c1"]
agreements = [x["agreement"] for x in cases.CASE_I["comparisons"]]
naive = sum(agreements) / float(len(agreements))
check("correlated others sharing a hop count as one instrument",
      i_c1["pairs_admitted"] == 3 and i_c1["independent_classes"] == 2,
      "%d pairs, %d independent classes" % (i_c1["pairs_admitted"],
                                            i_c1["independent_classes"]))
check("and the rule is load-bearing: counting them as three flips the verdict",
      naive >= lw.DEFAULTS.calibrated_at_or_above
      > i_c1["value"]
      and i["verdict"] is LoopRead.SHORT_MISCALIBRATED,
      "three pairs mean %.3f (clears %.2f), two classes mean %.3f (does not)"
      % (naive, lw.DEFAULTS.calibrated_at_or_above, i_c1["value"]))

b = read_by_id("B_one_hop_scored")
b_c2 = b["calibration"]["c2"]
check("a prediction scored on terms the source set is excluded from C-2",
      any(x["reason"].endswith("_is_the_source") for x in b_c2["predictions_excluded"]),
      "%s" % b_c2["predictions_excluded"])

j = read_by_id("J_derivations_disagree")
check("both derivations are reported when both land",
      j["calibration"]["derivations_used"] == ["C-1", "C-2"])
check("disagreeing derivations are flagged and C takes the lower",
      j["calibration"]["derivations_disagree"]
      and j["calibration"]["value"] == min(j["calibration"]["c1"]["value"],
                                           j["calibration"]["c2"]["value"]),
      "C-1=%.2f C-2=%.2f C=%.2f" % (j["calibration"]["c1"]["value"],
                                    j["calibration"]["c2"]["value"],
                                    j["calibration"]["value"]))


# ---------------------------------------------------------------------------
# 9. L is counted from the path or not at all
# ---------------------------------------------------------------------------

h = read_by_id("H_path_not_described")
check("an undescribed path is INSUFFICIENT, not an inferred hop count",
      h["verdict"] is LoopRead.INSUFFICIENT and h["loop_length"] is None
      and h["loop_length_note"] == "path_not_described")
insufficient_cmp = lw.carries_more(h, c)
carries_seen.add(insufficient_cmp["verdict"])
check("INSUFFICIENT is not ranked against a read",
      insufficient_cmp["verdict"] is Carries.INCOMPARABLE
      and insufficient_cmp["rule"] == lw.RULE_UNMEASURED_PATH)

no_dominance = lw.carries_more(b, b)
carries_seen.add(no_dominance["verdict"])
check("a read does not dominate itself",
      no_dominance["verdict"] is Carries.INCOMPARABLE
      and no_dominance["rule"] == lw.RULE_NO_DOMINANCE)
check("every Carries member is reachable",
      carries_seen == set(Carries),
      "%d of %d" % (len(carries_seen), len(list(Carries))))


# a malformed path is INSUFFICIENT, not a crash and not a counted hop list.
for bad, label in ((  "four hops or so", "a sentence"),
                   ([1, 2], "a list of non-records"),
                   (None, "absent")):
    bad_read = lw.read({"source_id": "malformed", "referent": "m", "path": bad,
                        "comparisons": [], "predictions": []})
    check("a path given as %s is INSUFFICIENT" % label,
          bad_read["verdict"] is LoopRead.INSUFFICIENT
          and bad_read["loop_length"] is None
          and bad_read["per_hop_retention"] is None,
          "got %s L=%r R=%r" % (bad_read["verdict"].name, bad_read["loop_length"],
                                bad_read["per_hop_retention"]))


# ---------------------------------------------------------------------------
# 10. the case set carries raw inputs only, and the parameters are printed
# ---------------------------------------------------------------------------

precomputed = []
for case in cases.CASES + cases.REFUSED:
    for key in case:
        if set(split_identifier(key)) & {"verdict", "expected", "loop", "length",
                                         "retention", "calibration", "score"}:
            precomputed.append((case["source_id"], key))
check("no case carries a precomputed axis or verdict", not precomputed,
      "%s" % precomputed if precomputed else
      "expected verdicts live in this test file, not in the case set")
check("at least 8 hand-built cases", len(cases.CASES) >= 8,
      "%d cases" % len(cases.CASES))
check("every read prints the parameters it was taken under",
      all(r["params"] == lw.DEFAULTS._asdict() for r in READS))


# ---------------------------------------------------------------------------

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-6s %s%s" % ("ok" if ok else "FAIL", name,
                         ("\n         %s" % detail) if detail and not ok else ""))
print()
print("%d checks, %d failed" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
