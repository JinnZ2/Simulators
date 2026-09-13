#!/usr/bin/env python3
"""
Checks for the internal-reference boundary instrument.

No expected verdict lives in cases.py or gap_cases.py; every expectation
is here, so no case can agree with the instrument by construction.

Run: python3 test_boundary.py
CC0. Stdlib only, no pytest. Parses under 3.9.
"""

import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import radials                                            # noqa: E402
import gap_transfer                                       # noqa: E402
import cases                                              # noqa: E402
import gap_cases                                          # noqa: E402
import authority_scan                                     # noqa: E402
import no_severity                                        # noqa: E402

PASS = []
FAIL = []


def ok(cond, label, detail=""):
    (PASS if cond else FAIL).append((label, detail))


def section(name):
    print("\n-- %s" % name)


def _src(fn):
    return open(os.path.join(HERE, fn)).read()


def _is_str_const(n):
    return isinstance(n, ast.Constant) and isinstance(n.value, str)


def _binop_const_sets(source):
    """Every set of literal strings appearing inside one ARITHMETIC or
    comparison expression. Used to assert two quantities are never
    combined: a check on the AST, not on the prose.

    String formatting and string concatenation are excluded, and they had
    to be. `%` is ast.BinOp, so the first version of this check fired on
    the render's own template line -- `"breadth=%s benefit_correlation=%s"
    % (...)` -- and reported that the module combined the two quantities
    it prints side by side. A checker firing on its own report template,
    which is the shape this repository keeps recording.
    """
    tree = ast.parse(source)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Mod) and _is_str_const(node.left):
                continue
            if isinstance(node.op, ast.Add) and (_is_str_const(node.left)
                                                 or _is_str_const(node.right)):
                continue
        elif not isinstance(node, ast.Compare):
            continue
        s = {sub.value for sub in ast.walk(node) if _is_str_const(sub)}
        out.append(s)
    return out


def _field_names(source):
    """Every dict KEY and every bound name in a module. An expected
    verdict, if one were here, would be a field -- so the check runs on
    fields and not on the file's text, which is why the first version
    fired on cases.py's own disclaimer that no expected verdict lives
    there."""
    tree = ast.parse(source)
    ks = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k in node.keys:
                if _is_str_const(k):
                    ks.add(k.value)
        elif isinstance(node, ast.Name):
            ks.add(node.id)
    return ks


def _minus_choices(source):
    """The source with the CHOICES literal removed, so a [CHOICE n] marker
    is counted only where it is CITED, not where it is declared."""
    i = source.find("CHOICES = {")
    if i < 0:
        return source
    j = source.find("\ndef ", i)
    return source[:i] + source[j:]


R_SRC = _src("radials.py")
G_SRC = _src("gap_transfer.py")
C_SRC = _src("cases.py")
GC_SRC = _src("gap_cases.py")


# ------------------------------------------------------- 1. the handoff

section("1  handoff landed verbatim")
hp = os.path.join(HERE, "HANDOFF.md")
ok(os.path.exists(hp), "HANDOFF.md is in the folder")
HAND = open(hp).read()
ok("A boundary drawn by the party inside it" in HAND,
   "the anchor invariant is in the landed handoff")
ok(HAND.count("STATUS:") == 7, "seven radials carry a STATUS line",
   "count=%d" % HAND.count("STATUS:"))
ok("/areas/internal-reference-boundary-anchor.md" in HAND,
   "the two source files are named in the handoff")
ok(not os.path.exists("/areas"),
   "the named source directory is not in this environment; nothing in "
   "this folder is reconstructed from it")
for r in ("R1", "R2", "R3", "R4", "R5", "R6", "R7"):
    ok(("%s " % r) in HAND, "%s is named in the handoff" % r)
ok(radials.INVARIANT.rstrip(".") in
   " ".join(HAND.split()).replace("\n", " "),
   "radials.INVARIANT is the handoff's sentence")


# ---------------------------------------------------- 2. vocabulary

section("2  vocabulary and status carried, not invented")
ok(len(radials.INSTANCES) == 6, "six instances, as the handoff lists")
for i in radials.INSTANCES:
    flat = " ".join(HAND.lower().replace("-", " ").split())
    ok(i.replace("_", " ") in flat,
       "instance %s appears in the handoff" % i)
ok(radials.STATUS["R6"].startswith("METHOD_COMPLETE"),
   "R6 carries the handoff's needs-a-corpus status")
ok(radials.STATUS["R7"].startswith("METHOD_COMPLETE"),
   "R7 carries the handoff's needs-a-corpus status")
ok(all(radials.STATUS[k] == "READY" for k in
       ("R1", "R2", "R3", "R4", "R5")),
   "R1-R5 carry READY")
ok(set(radials.NON_VALUE_STATES) ==
   {radials.UNDECLARED, radials.NEEDS_CORPUS, radials.NOT_EVALUABLE},
   "three non-value states, kept apart")
ok(len(set(radials.NON_VALUE_STATES)) == 3,
   "the three non-value states are distinct strings")


# ------------------------------------------------------------- 3. R1

section("3  R1 encounter rate  [CHOICE 1]")
a = cases.ANCHORS
ok(a["R1_low"]["as_rate_per_occasion"] == 0.0,
   "the low anchor sits at 0.0 on the per-occasion scale")
ok(a["R1_high"]["as_rate_per_occasion"] == 1.0,
   "the high anchor sits at 1.0 on the per-occasion scale")
ok("saturation" in a["R1_high"]["note"],
   "the high anchor is recorded as a saturation statement, not a "
   "measurement -- on a per-time scale it has no value")
r = radials.r1_encounter_rate({"encounters": 8, "occasions_of_need": 10})
ok(abs(r["value"] - 0.8) < 1e-12 and r["state"] == "VALUE",
   "R1 computes the ratio")
ok(radials.r1_encounter_rate({})["state"] == radials.UNDECLARED,
   "R1 with nothing declared is UNDECLARED")
ok(radials.r1_encounter_rate(
    {"encounters": 3, "occasions_of_need": 0})["state"]
   == radials.NOT_EVALUABLE,
   "R1 with an empty denominator is NOT_EVALUABLE, not zero")
ok(radials.r1_encounter_rate(
    {"encounters": 0, "occasions_of_need": 10})["value"] == 0.0,
   "a measured zero is a value, and is a different return from both")
ok(radials.CHOICES[1].startswith("R1 denominator"),
   "[CHOICE 1] is declared")
ok("choice" in r and r["choice"] == 1,
   "[CHOICE 1] is cited inline on the R1 return")


# ------------------------------------------------------------- 4. R2

section("4  R2 measurand ownership  [CHOICE 2]")
ok(len(radials.DISTANCE_LADDER) == 5, "five declared rungs")
ok(radials.LADDER["INSIDE_SAME_BODY"] == 0.0
   and radials.LADDER["CONSTRAINED_PARTY"] == 1.0,
   "the ladder runs 0.0 inside to 1.0 at the constrained party")
ok(radials.r2_measurand_ownership({})["state"] == radials.UNDECLARED,
   "a missing rung is UNDECLARED")
ok(radials.r2_measurand_ownership(
    {"definer_rung": radials.UNDECLARED})["state"] == radials.UNDECLARED,
   "an EXPLICIT UNDECLARED rung is the same state as a missing one -- "
   "found by running gap_transfer.py, which refused a legitimate record")
bad = False
try:
    radials.r2_measurand_ownership({"definer_rung": "SOMEWHERE_ELSE"})
except radials.RecordRefused:
    bad = True
ok(bad, "a rung outside the ladder is still refused")
r2 = radials.r2_measurand_ownership(
    {"definer_rung": "INSIDE_SAME_BODY", "feedback_distance": 30.0})
ok(r2["value"] == 0.0 and r2["feedback_distance"] == 30.0,
   "FEEDBACK DISTANCE is carried beside R2")
ok(not any({"feedback_distance", "definer_rung"} <= s
           for s in _binop_const_sets(R_SRC)),
   "no arithmetic combines feedback distance with the R2 rung: the "
   "handoff logs it as a result, not as an eighth radial")


# ------------------------------------------------------------- 5. R3

section("5  R3 sanction base rate -- two legs, two time bases")
ok(radials.sanction_ratio_point(1e-4, 0.25) == 1e-4 / 0.25,
   "the point ratio divides")
ok(radials.sanction_ratio_point(1e-4, 0) is None,
   "an empty occurrence rate returns None, never a ratio of zero")
anchor = {"consequence_rate": 1e-4, "incidence_lo": 0.25,
          "incidence_hi": 0.50, "incidence_window": radials.UNDECLARED}
r3 = radials.r3_sanction_base_rate(anchor, career_years=30.0)
ok(r3["state"] == "BAND" and r3["value"] is None,
   "with the window undeclared R3 returns a BAND and no point")
ok(abs(r3["readings"]["per_year"][0] - 2.0e-4) < 1e-12,
   "the per-year reading is 2.0e-4 at the high incidence")
ok(abs(r3["readings"]["career"][1] - 1.2e-2) < 1e-9,
   "the career reading at 30 years is 1.2e-2 at the low incidence")
ok(58 < r3["span"] < 62,
   "the band the handoff's own anchor spans is about 60x",
   "span=%.1f" % r3["span"])
r3b = radials.r3_sanction_base_rate(
    dict(anchor, incidence_window="per_year"))
ok(r3b["state"] == "VALUE_BAND" and r3b["band"] == r3["readings"]["per_year"],
   "declaring the window collapses the band to one reading")
r3c = radials.r3_sanction_base_rate(anchor, career_years=10.0)
ok(r3c["span"] < r3["span"],
   "the span moves with [CHOICE 3]; the career length is not a fact")
ok(radials.r3_sanction_base_rate({})["state"] == radials.UNDECLARED,
   "R3 with nothing declared is UNDECLARED")
ok(radials.r3_sanction_base_rate(
    {"consequence_rate": 1e-4, "incidence_lo": 0.0, "incidence_hi": 0.0,
     "incidence_window": "per_year"})["state"] == radials.NOT_EVALUABLE,
   "a zero occurrence rate is NOT_EVALUABLE, not infinite and not zero")
refused = False
try:
    radials.r3_sanction_base_rate(dict(anchor, incidence_window="lifetime"))
except radials.RecordRefused:
    refused = True
ok(refused, "an undeclared window vocabulary is refused")


# ------------------------------------------------------------- 6. R4

section("6  R4 routability -- the predicted sign is refutable")
inverse = [{"routability": x, "damage_capacity": 1.0 - x}
           for x in (0.1, 0.4, 0.7, 0.9)]
direct = [{"routability": x, "damage_capacity": x}
          for x in (0.1, 0.4, 0.7, 0.9)]
ok(radials.r4_sign_test(inverse)["observed_sign"] == "INVERSE",
   "a constructed inverse world returns INVERSE")
ok(radials.r4_sign_test(direct)["observed_sign"] == "DIRECT",
   "a constructed direct world returns DIRECT -- the test is neither "
   "CONSTANT_FIRES nor CONSTANT_SILENT")
ok(radials.r4_sign_test(inverse)["matches_prediction"] is True
   and radials.r4_sign_test(direct)["matches_prediction"] is False,
   "the prediction can be met and can be refuted")
ok(radials.r4_sign_test(inverse[:2])["state"] == radials.NOT_EVALUABLE,
   "fewer than three cases is NOT_EVALUABLE, not a sign")
flat = [{"routability": 0.5, "damage_capacity": d}
        for d in (0.1, 0.4, 0.9)]
ok(radials.r4_sign_test(flat)["state"] == radials.NOT_EVALUABLE,
   "a constant side is NOT_EVALUABLE, not a correlation of zero")
live = radials.r4_sign_test(cases.CASES)
ok(live["observed_sign"] == "DIRECT",
   "on this corpus the observed sign runs AGAINST the handoff's "
   "prediction", "rho=%.4f" % live["rho"])
ok(live.get("corpus_note"),
   "the render carries the note that the sign on a constructed corpus is "
   "a property of the authoring")


# ------------------------------------------------------------- 7. R5

section("7  R5 exemption provenance -- two numbers, never combined")
ok(not any({"breadth", "benefit_correlation"} <= s
           for s in _binop_const_sets(R_SRC)),
   "no arithmetic combines breadth with the benefit correlation")
e = radials.r5_exemption_provenance(
    [c for c in cases.CASES if c["id"] == "eff-01"][0])
ok(e["verdict"] == "ACTUAL_PRINCIPLE",
   "high breadth with a near-zero measured correlation reaches the one "
   "verdict the handoff names")
s5 = radials.r5_exemption_provenance(
    [c for c in cases.CASES if c["id"] == "shell-01"][0])
ok(s5["verdict"] == "BENEFIT_SORTED", "extensions sorted by benefit read "
   "as sorted by benefit")
u5 = radials.r5_exemption_provenance(
    [c for c in cases.CASES if c["id"] == "selfinv-01"][0])
ok(u5["benefit_correlation"] is None
   and u5["correlation_state"] == radials.NOT_EVALUABLE,
   "a constant benefit column is NOT_EVALUABLE, never 0.0")
ok(u5["breadth"] == 4 and u5["verdict"] == "UNDETERMINED",
   "breadth alone does not reach ACTUAL_PRINCIPLE: the rule turns on a "
   "MEASURED zero, and an absent correlation scored as zero would award "
   "the verdict to a claimant nobody measured")
ok(all(x["base_rate"] == "UNKNOWN" for x in (e, s5, u5)),
   "the base rate is printed as UNKNOWN on every return, as the handoff "
   "states it")
ok(e["choices"] == [4, 5],
   "[CHOICE 4] and [CHOICE 5] are cited inline on the R5 return")
ok(radials.r5_exemption_provenance({})["state"] == radials.UNDECLARED,
   "R5 with nothing declared is UNDECLARED")


# ------------------------------------------------------------- 8. R6

section("8  R6 transfer survival -- effective origins by trace identity")
I4 = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
J4 = [[1.0] * 4 for _ in range(4)]
E2 = [[1.0, 0.5], [0.5, 1.0]]
E3 = [[1.0, 0.5, 0.5], [0.5, 1.0, 0.5], [0.5, 0.5, 1.0]]
ok(abs(radials.effective_origins(I4) - 4.0) < 1e-12,
   "four uncoupled origins are four")
ok(abs(radials.effective_origins(J4) - 1.0) < 1e-12,
   "four fully coupled origins are one observation measured four times")
ok(abs(radials.effective_origins(E2) - 1.6) < 1e-12,
   "two origins at coupling 0.5 give 1.6")
ok(abs(radials.effective_origins(E3) - 2.0) < 1e-12,
   "three origins at coupling 0.5 give 2.0")
prev = None
mono = True
for rho in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    m = [[1.0 if i == j else rho for j in range(4)] for i in range(4)]
    v = radials.effective_origins(m)
    if prev is not None and v > prev + 1e-12:
        mono = False
    prev = v
ok(mono, "the count collapses toward 1 as coupling rises, monotonically")
sq = False
try:
    radials.effective_origins([[1.0, 0.5]])
except radials.RecordRefused:
    sq = True
ok(sq, "a non-square coupling matrix is refused")
asym = False
try:
    radials.effective_origins([[1.0, 0.2], [0.9, 1.0]])
except radials.RecordRefused:
    asym = True
ok(asym, "an asymmetric coupling matrix is refused")
silo = [c for c in cases.CASES if c["id"] == "silo-01"][0]
r6 = radials.r6_transfer_survival(silo)
ok(r6["origin_breadth"]["n_nominal"] == 4,
   "four nominal origins on the worked corpus case")
ok(1.9 < r6["origin_breadth"]["n_effective"] < 2.0,
   "they are under two effective origins once shared funders are "
   "declared", "n_eff=%.3f" % r6["origin_breadth"]["n_effective"])
mean6 = radials.r6_transfer_survival(silo, combine="mean")
ok(mean6["origin_breadth"]["n_effective"]
   > r6["origin_breadth"]["n_effective"],
   "[CHOICE 7] MEAN dilutes the coupling and raises the count")
ok(all(v["state"] == radials.NEEDS_CORPUS
       for v in r6["routes"].values()),
   "all four routes return NEEDS_CORPUS, naming the input they want")
ok(r6["routes"][radials.R6_STRONGEST]["strongest"] is True,
   "independent adoption count is marked the strongest route")
ok(not any({"dependency_depth", "necessity"} <= s
           for s in _binop_const_sets(R_SRC)),
   "the SPLIT TO PRESERVE is structural: no arithmetic combines "
   "dependency depth with necessity")
ok(r6["dependency_depth"] == 0.90 and r6["necessity"] == 0.05,
   "both are reported side by side")
ok(radials.r6_transfer_survival({})["origin_breadth"]["state"]
   == radials.NEEDS_CORPUS,
   "with no origins declared the breadth is NEEDS_CORPUS, not zero")


# ------------------------------------------------------------- 9. R7

section("9  R7 permeability -- two metrics on two denominators")
er = radials.r7_entry_ratio({"confirming_entries": 12,
                             "contradicting_entries": 3})
ok(abs(er["value"] - 4.0) < 1e-12 and er["reading"] == "SELECTIVE",
   "an entry ratio of 4 reads as selective at [CHOICE 6]")
ok(radials.r7_entry_ratio({"confirming_entries": 5,
                           "contradicting_entries": 5})["reading"]
   == "PERMEABLE", "equal rates read as permeable")
ok(radials.r7_entry_ratio({"confirming_entries": 5,
                           "contradicting_entries": 0})["state"]
   == "CONFIRMING_ONLY",
   "confirming-only is its own state: selection, not evaluation")
ok(radials.r7_entry_ratio({"confirming_entries": 0,
                           "contradicting_entries": 0})["state"]
   == radials.NOT_EVALUABLE,
   "no entries of either kind is NOT_EVALUABLE, not permeable")
ok(radials.r7_entry_ratio({})["state"] == radials.UNDECLARED,
   "an undeclared entry count is UNDECLARED")
rr = radials.r7_rejection_reason_ratio(silo)
ok(rr["counts"] == {"METHOD": 2, "CONCLUSION": 4}
   and abs(rr["value"] - 0.5) < 1e-12,
   "the rejection-reason ratio counts the two declared kinds")
ok(radials.r7_rejection_reason_ratio({})["state"] == radials.NEEDS_CORPUS,
   "with no pariah set the second metric is NEEDS_CORPUS, not zero")
ok(radials.r7_rejection_reason_ratio({"pariah_set": []})["state"]
   == radials.NOT_EVALUABLE,
   "an empty pariah set is NOT_EVALUABLE -- a corpus of none is a "
   "different return from no corpus")
ok(radials.r7_rejection_reason_ratio(
    {"pariah_set": [{"rejection_reason": "METHOD",
                     "outcome": "stayed_rejected"}]})["state"]
   == "METHOD_ONLY",
   "rejections citing method only get their own state: the field read it")
p = radials.r7_permeability(silo)
ok(p["entry_ratio"]["denominator"] != p["rejection_reason_ratio"][
    "denominator"],
   "the two metrics sit on different denominators -- entries admitted "
   "against rejections issued")
ok(not any({"entry_ratio", "rejection_reason_ratio"} <= s
           for s in _binop_const_sets(R_SRC)),
   "nothing merges them; the handoff calls each of them the measure and "
   "there is no combined permeability number")
ss = radials.r7_second_score(silo)
ok(ss["census"] == {"stayed_rejected": 3, "came_in_with_credit": 1,
                    "came_in_without_credit": 2},
   "the three-state historical census")
ok(ss["informative_state"] == "came_in_without_credit",
   "the third state is marked as the informative one")
ok(abs(ss["latency_years"] - 16.0) < 1e-9 and ss["latency_n"] == 3,
   "latency runs from labelling to absorption over absorbed cases only")
none_abs = radials.r7_second_score(
    {"pariah_set": [{"rejection_reason": "METHOD",
                     "outcome": "stayed_rejected"}]})
ok(none_abs["latency_years"] is None
   and none_abs["latency_state"] == radials.NOT_EVALUABLE,
   "with nothing absorbed the latency is None, never 0 -- [CHOICE 8]")
badout = False
try:
    radials.r7_second_score({"pariah_set": [{"rejection_reason": "METHOD",
                                             "outcome": "maybe"}]})
except radials.RecordRefused:
    badout = True
ok(badout, "an outcome outside the three declared states is refused")


# ------------------------------------- 10. no correctness verdict

section("10  the pariah's correctness is scored nowhere")
vocab = radials.refused_score_tokens()
ok(len(vocab) >= 8, "the refused vocabulary is declared in the module")
ok(authority_scan.scan(R_SRC, vocab) == [],
   "no identifier in radials.py scores whether rejected work is right")
ok(authority_scan.scan(G_SRC, vocab) == [],
   "nor in gap_transfer.py")
ok(authority_scan.scan(authority_scan.PLANT.replace("f", "validity")
                       if False else
                       "def g():\n    validity = 1\n    return validity\n",
                       vocab) != [],
   "the scan fires on a planted violation, so its silence means "
   "something")
ok(all(len(t.split("_")) == 1 for t in vocab),
   "every refused token is a single word: a two-token entry is "
   "unmatchable by construction, since the scanner splits identifiers")
ok("rejection_reason" in R_SRC and "REJECTION_REASONS" in R_SRC,
   "what is scored is the field's stated REASON, which is what removes "
   "the need to adjudicate the rejected work")


# --------------------------------------------- 11. gap transfer

section("11  gap transfer -- track the gap, not the intervention")
EFFICACY = ("efficacy", "effectiveness", "helped", "cured", "success",
            "improvement", "worked")
ok(authority_scan.scan(G_SRC, EFFICACY) == [],
   "no identifier in gap_transfer.py records how an intervention went")
ok(authority_scan.scan(GC_SRC, EFFICACY) == [],
   "nor in the records")
ok(authority_scan.scan("def g():\n    efficacy = 1\n    return efficacy\n",
                       EFFICACY) != [],
   "the efficacy scan fires on a plant")
refused = False
try:
    gap_transfer._check_host({"name": "h", "efficacy": 0.9})
except gap_transfer.RecordRefused:
    refused = True
ok(refused, "a host carrying an efficacy field is refused at intake, so "
   "the rule is enforced and not only documented")
g2 = gap_transfer.read(
    [g for g in gap_cases.GAPS if g["gap_id"] == "gap-02"][0])
ok([t["verdict"] for t in g2["transfers"]] == ["CARRIER", "CARRIER"],
   "a successor inheriting both the population and the horizon is the "
   "carrier")
ok(g2["both_directions"] is True,
   "one horizon, two directions is a reachable reading")
g3 = gap_transfer.read(
    [g for g in gap_cases.GAPS if g["gap_id"] == "gap-03"][0])
ok([t["verdict"] for t in g3["transfers"]]
   == ["PARTIAL_CARRIER", "GAP_CLOSED_NOT_TRANSFERRED"],
   "a successor that measures the gap closed it rather than inheriting "
   "it -- the reachable negative")
ok(g3["transfers"][0]["partial_on"] == "population",
   "a partial carrier names which of the two it inherited")
ok(gap_transfer.gap_state({})["measured"] is None,
   "a successor nobody checked is not scored as having closed the gap")
g1 = gap_transfer.read(
    [g for g in gap_cases.GAPS if g["gap_id"] == "gap-01"][0])
ok(all(t["verdict"] == gap_transfer.NOT_EVALUABLE
       for t in g1["transfers"]),
   "the handoff's WORKED CASE is NOT_EVALUABLE at the resolution it is "
   "delivered at: it states no population and no horizon value")
ok(g1["both_directions"] is False,
   "and its sharpest reading -- same gap, other direction -- is one "
   "field short: the horizon has to be declared in the same unit for "
   "both hosts before SAME_GAP_BOTH_DIRECTIONS can fire")
ok(g1["transfers"][1]["direction"]["reading"] == "DIRECTION_CHANGED",
   "what the delivered case does support is that the direction reversed")
ok(gap_transfer._absent(None) and gap_transfer._absent("UNDECLARED")
   and not gap_transfer._absent(0),
   "one absent test: a missing field and an explicit UNDECLARED are the "
   "same state, and a literal zero is not either of them")
hz = gap_transfer.horizon_inherited(
    {"accounting_horizon": "UNDECLARED", "horizon_unit": "UNDECLARED"},
    {"accounting_horizon": "UNDECLARED", "horizon_unit": "UNDECLARED"})
ok(hz["state"] == gap_transfer.UNDECLARED,
   "two undeclared horizons are not an inherited horizon -- the defect "
   "that made a record of two blanks reach the handoff's own conclusion")
hu = gap_transfer.horizon_inherited(
    {"accounting_horizon": 60, "horizon_unit": "days"},
    {"accounting_horizon": 2, "horizon_unit": "months"})
ok(hu["state"] == gap_transfer.NOT_EVALUABLE,
   "two horizons in different units are NOT_EVALUABLE, not unequal")
lc = gap_transfer.locate_carrier(gap_cases.CANDIDATE_SET["from"],
                                 gap_cases.CANDIDATE_SET["candidates"])
ok(set(lc["carriers"]) == {"cand_same_pop_same_horizon",
                           "cand_overlap_declared"},
   "the handoff's prediction made operative: the candidates inheriting "
   "both, including the one whose population arrives as a declared "
   "overlap rather than an identity", str(lc["carriers"]))
lc9 = gap_transfer.locate_carrier(gap_cases.CANDIDATE_SET["from"],
                                  gap_cases.CANDIDATE_SET["candidates"],
                                  floor=0.90)
ok(lc9["carriers"] == ["cand_same_pop_same_horizon"],
   "raising the [CHOICE 9] floor drops the overlap candidate: the "
   "threshold does work and is not decoration")
ok([o["candidate"] for o in lc["candidates"] if o["horizon"]
    == gap_transfer.NOT_EVALUABLE] == ["cand_horizon_in_another_unit"],
   "a candidate whose horizon is declared in another unit is "
   "NOT_EVALUABLE, not a non-carrier")
ok([o["candidate"] for o in lc["candidates"]]
   == [c["name"] for c in gap_cases.CANDIDATE_SET["candidates"]],
   "locate_carrier ranks nothing: the candidates come back in the order "
   "given")
ok("ranks_nothing" in lc and lc["ranks_nothing"] is True,
   "and says so in its return")


# -------------------------------------------- 12. assembly order

section("12  assembly order is structural")
rc = radials.read_case(cases.CASES[0])
ok("R5" not in rc,
   "read_case returns no R5 key: the handoff puts exemptions in a "
   "SEPARATE LAYER")
ok(not any(isinstance(n, ast.Call)
           and isinstance(n.func, ast.Name)
           and n.func.id == "r5_exemption_provenance"
           for fn in ast.walk(ast.parse(R_SRC))
           if isinstance(fn, ast.FunctionDef) and fn.name == "read_case"
           for n in ast.walk(fn)),
   "and read_case does not call the exemption radial at all")
asm = radials.assemble(cases.CASES)
ok(list(asm.keys())[:4] == ["invariant", "instances", "cases",
                            "exemptions"],
   "the key order IS the assembly order: invariant, instances, cases, "
   "exemptions")
ok(len(asm["exemptions"]) == 3,
   "three cases declare an exemption and the layer carries three")
ok(all("verdict" in x for x in asm["exemptions"]),
   "each exemption entry carries its own verdict")


# ------------------------------------------- 13. open / unrun

section("13  the handoff's OPEN items")
f = radials.fold_test_r2_r5(cases.CASES)
ok(f["verdict"] == "UNRESOLVED",
   "on this corpus the fold test is UNRESOLVED: no coded case populates "
   "the discriminating cell")
ok(cases.FOLD_CELL_ABSENT_ON_PURPOSE,
   "the cell is left out of the corpus deliberately -- authoring it "
   "would close the handoff's OPEN item by writing the answer down")
cell = dict(cases.CASES[0], id="constructed-cell",
            definer_rung="OUTSIDE_FIELD",
            exemption_provenance="self_designated")
f2 = radials.fold_test_r2_r5(cases.CASES + [cell])
ok(f2["verdict"] == "DISTINCT" and f2["cell_populated_by"]
   == ["constructed-cell"],
   "a constructed case in the cell flips it to DISTINCT, so the test "
   "discriminates and is not CONSTANT_SILENT")
ok(f2["corpus_note"],
   "and the return says what that shows: a property of the test, not of "
   "any boundary")
x = radials.r7_x_r6_cell()
ok(x["state"] == "NAMED_UNINSTRUMENTED" and x["instrumented"] is False,
   "the R7 x R6 cell returns a declared state, not a number and not a "
   "null")
u = radials.unrun()
ok(len(u) == 4, "four OPEN / UNRUN items carried from the handoff")
ok(all(item["state"] != "VALUE" for item in u),
   "none of them is run here")
ok(any("psychosurgery" in item["item"] for item in u)
   and any("memoir" in item["item"] for item in u),
   "including the two the handoff names as never having been run on "
   "their populations")


# ---------------------------------------- 14. no composite score

section("14  no composite, no ranking")
RADIAL_KEYS = {"R1", "R2", "R3", "R4", "R5", "R6", "R7"}
ok(not any(len(RADIAL_KEYS & s) >= 2 for s in _binop_const_sets(R_SRC)),
   "no arithmetic expression combines two radials")
tree = ast.parse(R_SRC)
fns = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
ok(not any(("composite" in n) or n == "score" or n.endswith("_score")
           and n != "r7_second_score" for n in fns),
   "no function in radials.py is a composite scorer",
   str([n for n in fns if "composite" in n or n == "score"]))
ok(not any(("rank" in n) for n in fns),
   "and nothing ranks boundaries")


# ------------------------------------------------ 15. free text

section("15  free text is carried, never parsed")
rd = radials.read_case(cases.CASES[0])
ok(rd["what_the_boundary_is"] == cases.CASES[0]["what_the_boundary_is"],
   "what the boundary is comes back byte-for-byte")
ok(rd["who_draws_it"] == cases.CASES[0]["who_draws_it"],
   "who draws it comes back byte-for-byte")
alt = dict(cases.CASES[0],
           what_the_boundary_is="", who_draws_it="x" * 400)
before = radials.read_case(cases.CASES[0])
after = radials.read_case(alt)
ok(all(before[k] == after[k] for k in ("R1", "R2", "R3", "R4")),
   "replacing both free-text fields moves no radial: neither is parsed")


# --------------------------------------------- 16. choices, CLIs

section("16  choices and CLIs")
ok(sorted(radials.CHOICES) == [1, 2, 3, 4, 5, 6, 7, 8],
   "eight choices declared in radials.py")
ok(sorted(gap_transfer.CHOICES) == [9, 10],
   "two more in gap_transfer.py, numbered on")
rep = radials.choices_report() + gap_transfer.choices_report()
for k in list(radials.CHOICES) + list(gap_transfer.CHOICES):
    ok("[CHOICE %d]" % k in rep, "[CHOICE %d] prints" % k)
cited = _minus_choices(R_SRC) + _minus_choices(G_SRC)
for k in list(radials.CHOICES) + list(gap_transfer.CHOICES):
    ok(cited.count("CHOICE %d" % k) >= 1,
       "[CHOICE %d] is cited at the site where it takes effect, not "
       "only in the CHOICES block" % k)
import subprocess                                         # noqa: E402
for mod in ("radials.py", "gap_transfer.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, mod),
                        "--selftest"], capture_output=True)
    ok(p.returncode == 2,
       "%s refuses --selftest rather than exiting 0 on an invocation "
       "that runs nothing" % mod, "rc=%d" % p.returncode)
    p2 = subprocess.run([sys.executable, os.path.join(HERE, mod),
                         "--choices"], capture_output=True)
    ok(p2.returncode == 0 and b"[CHOICE" in p2.stdout,
       "%s --choices prints" % mod)


# ------------------------------------------------- 17. the screen

section("17  the report screens clean")
for label, txt in (("radials render", radials.render(cases.CASES)),
                   ("radials choices", radials.choices_report()),
                   ("gap render", gap_transfer.render(gap_cases.GAPS)),
                   ("gap choices", gap_transfer.choices_report())):
    h = no_severity.hits(txt)
    ok(h == [], "%s screens clean with no exemption" % label, str(h[:3]))
ok(no_severity.hits("this is a critical error") != [],
   "the screen fires on a plant, so the clean results mean something")


# ------------------------------------------- 18. the corpus itself

section("18  the corpus")
ok(all(c.get("provenance") == "CONSTRUCTED" for c in cases.CASES),
   "every boundary case declares itself CONSTRUCTED")
ok({c["instance"] for c in cases.CASES} == set(radials.INSTANCES),
   "one case per instance the invariant names")
C_FIELDS = _field_names(C_SRC)
GC_FIELDS = _field_names(GC_SRC)
for token in ("expected", "verdict", "should", "want", "correct"):
    ok(not any(token in f.lower() for f in C_FIELDS),
       "no field in cases.py names an expected verdict (%s)" % token,
       str([f for f in C_FIELDS if token in f.lower()]))
    ok(not any(token in f.lower() for f in GC_FIELDS),
       "no field in gap_cases.py names an expected verdict (%s)" % token,
       str([f for f in GC_FIELDS if token in f.lower()]))
ok("CARRIED" in gap_cases.GAPS[0]["provenance"],
   "the worked case declares itself carried from the handoff")
ok(all(a in str(cases.ANCHORS) for a in ("10,000", "25-50%", "1-2yr")),
   "the handoff's empirical anchors are carried verbatim in ANCHORS")


# ---------------------------------------- 19. radial independence

section("19  radial independence on this corpus")
ind = radials.independence(cases.CASES)
ok(ind["collinear_pairs"] == [],
   "no two radials are collinear on this corpus",
   str(ind["collinear_pairs"]))
ok(all(v["n"] == 6 for v in ind["pairs"].values()),
   "every pair is computed over all six cases")
ok(len(ind["pairs"]) == 6, "four columns give six pairs")


# ----------------------------------------------------- 20. reach

section("20  every declared state is reached by something")
states_seen = set()
for c in cases.CASES:
    rd = radials.read_case(c)
    states_seen.add(rd["R1"]["state"])
    states_seen.add(rd["R2"]["state"])
    states_seen.add(rd["R3"]["state"])
    states_seen.add(rd["R4"]["state"])
    states_seen.add(rd["R6"]["origin_breadth"]["state"])
    states_seen.add(rd["R7"]["entry_ratio"]["state"])
    states_seen.add(rd["R7"]["rejection_reason_ratio"]["state"])
ok(radials.UNDECLARED in states_seen, "UNDECLARED is reached")
ok(radials.NEEDS_CORPUS in states_seen, "NEEDS_CORPUS is reached")
ok("CONFIRMING_ONLY" in states_seen, "CONFIRMING_ONLY is reached")
ok("VALUE" in states_seen, "VALUE is reached")
verdicts = {gap_transfer.read(g)["transfers"][i]["verdict"]
            for g in gap_cases.GAPS
            for i in range(len(gap_transfer.read(g)["transfers"]))}
ok({"CARRIER", "PARTIAL_CARRIER", "GAP_CLOSED_NOT_TRANSFERRED",
    gap_transfer.NOT_EVALUABLE} <= verdicts,
   "four gap-transfer verdicts reached by the records", str(verdicts))
ok("NOT_THE_CARRIER" not in verdicts,
   "NOT_THE_CARRIER is not reached by the records and is shown "
   "reachable on a constructed pair instead")
nt = gap_transfer.transfer(
    {"name": "a", "population": "P", "accounting_horizon": 30,
     "horizon_unit": "days", "gap_measured": False},
    {"name": "b", "population": "Q", "accounting_horizon": 3650,
     "horizon_unit": "days", "gap_measured": False})
ok(nt["verdict"] == "NOT_THE_CARRIER",
   "a successor inheriting neither is NOT_THE_CARRIER")


# ---------------------------------------------------------- report

print("\n" + "=" * 62)
for label, detail in FAIL:
    print("FAILED  %s" % label)
    if detail:
        print("        %s" % detail)
print("checks: %d   failed: %d" % (len(PASS) + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
