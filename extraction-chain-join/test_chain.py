# SPDX-License-Identifier: CC0-1.0
"""Checks for chain_join.py. Run: python3 extraction-chain-join/test_chain.py

Prints every check and the count. Exit 0 only if all pass. Every record
scored here is CONSTRUCTED.
"""

import ast
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import chain_join as cj  # noqa: E402

SRC = open(os.path.join(HERE, "chain_join.py"), encoding="utf-8").read()
N = {"pass": 0, "fail": 0}


def check(label, cond):
    N["pass" if cond else "fail"] += 1
    print("%s  %s" % ("PASS" if cond else "FAIL", label))


def raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc:
        return True
    return False


def near(a, b, tol=1e-9):
    return a is not None and b is not None and abs(a - b) <= tol


# -- 1. the work order: pinned, labelled reconstructed
wo = open(cj.WORK_ORDER, "rb").read()
check("WORK_ORDER.md sha256 matches the pin",
      hashlib.sha256(wo).hexdigest() == cj.WORK_ORDER_SHA256)
wot = wo.decode("utf-8")
check("WORK_ORDER.md says it is reconstructed, not verbatim",
      "RECONSTRUCTED, NOT VERBATIM" in wot)
for g in range(1, 8):
    check("G%d is in the work order and has a reader" % g,
          ("**G%d." % g) in wot and hasattr(cj, "g%d_read" % g))
check("the order's coverage rule is carried",
      "report the coverage percentage with every result" in wot)

# -- 2. coverage travels with every result
check("result() refuses a reading with no covered count",
      raises(cj.CoverageMissing, cj.result, "X", "GAP", None, None, 5, "u", "r", "DERIVED"))
check("result() refuses a reading with no unit",
      raises(cj.CoverageMissing, cj.result, "X", "GAP", None, 1, 5, "", "r", "DERIVED"))
check("result() refuses a branch outside the six",
      raises(ValueError, cj.result, "X", "VERDICT", None, 1, 5, "u", "r", "DERIVED"))
check("coverage(0, 0) is None, not zero", cj.coverage(0, 0) is None)
check("coverage(0, 5) is a measured zero", cj.coverage(0, 5) == 0.0)
check("coverage(3, 4) = 0.75", cj.coverage(3, 4) == 0.75)
check("coverage over the total raises", raises(ValueError, cj.coverage, 5, 4))
RES = cj._all_results()
check("every result carries a coverage share key",
      all("share" in r["coverage"] for r in RES.values()))
TEXT = cj.render()
sec1 = TEXT.split("1. every reading")[1].split("\n2.")[0].strip().splitlines()[1:]
check("render prints a coverage figure on every result row (%d rows)" % len(sec1),
      len(sec1) == len(RES) and all("coverage " in ln for ln in sec1))
check("the order's four branches come first; two are added",
      cj.DELIVERED_BRANCHES == ("PATTERN_HOLDS", "SCOPE_LIMITED", "GAP", "MISSED_VARIABLE")
      and set(cj.BRANCHES) - set(cj.DELIVERED_BRANCHES) == {"NO_PATTERN", "NOT_EVALUABLE"})
tiny = cj.g1_read(cj.g1_world("pressure", n_countries=3, n_years=5))
reached = set(r["branch"] for r in RES.values()) | {tiny["branch"]}
check("all six branches are reached on constructed worlds", reached == set(cj.BRANCHES))
check("a full-coverage panel too small to run reads NOT_EVALUABLE, not GAP",
      tiny["branch"] == "NOT_EVALUABLE" and tiny["coverage"]["share"] == 1.0)

# -- 3. G1 debt -> extraction
diffs = cj.g1_differences(cj.g1_world("price"))
xs = [d["dd"] for d in diffs]
ys = [d["dx"] for d in diffs]
zs = [d["dp"] for d in diffs]
beta, _r2 = cj.ols(ys, [xs])
check("slope() agrees with the imported ols on one regressor",
      near(cj.slope(xs, ys), beta[1], 1e-9))
beta2, _r2 = cj.ols(ys, [xs, zs])
check("the partial-regression slope equals the ols coefficient with d price",
      near(cj.slope(cj.residualize(xs, zs), cj.residualize(ys, zs)), beta2[1], 1e-9))
expect = {"G1 pressure": "PATTERN_HOLDS", "G1 scoped": "SCOPE_LIMITED",
          "G1 price": "MISSED_VARIABLE", "G1 price, column dropped": "PATTERN_HOLDS",
          "G1 null": "NO_PATTERN", "G1 sparse": "GAP"}
for k, b in expect.items():
    check("%s reads %s" % (k, b), RES[k]["branch"] == b)
check("without the price column the missed variable reads as the pattern",
      RES["G1 price, column dropped"]["branch"] == "PATTERN_HOLDS"
      and RES["G1 price"]["branch"] == "MISSED_VARIABLE")
check("a GAP carries its reading: scope-limited and unmeasured stay apart",
      RES["G1 sparse"]["core"] is not None and RES["G1 sparse"]["coverage"]["share"] < 0.5)
dv = cj.g1_divergence(cj.g1_world("scoped"))
check("divergence: one world, three samples, three readings",
      dv["dependent only"]["branch"] == "PATTERN_HOLDS"
      and dv["not dependent only"]["branch"] == "NO_PATTERN"
      and dv["pooled"]["branch"] == "SCOPE_LIMITED")
tally = {}
misses = {}
for kind, want in (("pressure", "PATTERN_HOLDS"), ("null", "NO_PATTERN"),
                   ("scoped", "SCOPE_LIMITED"), ("price", "MISSED_VARIABLE")):
    got = [cj.g1_read(cj.g1_world(kind, seed=s))["branch"] for s in range(1, 11)]
    tally[kind] = sum(1 for g in got if g == want)
    misses[kind] = [s for s, g in zip(range(1, 11), got) if g != want]
check("seeds 1..10: pressure 10, null 9, scoped 9, price 9 read as built (%r)" % tally,
      tally == {"pressure": 10, "null": 9, "scoped": 9, "price": 9})
check("the three misses are one seed (2), not three draws",
      misses["null"] == misses["scoped"] == misses["price"] == [2] and not misses["pressure"])

# -- 4. G2 extracting firm -> beneficial owner
W = cj.g2_world()
cons = True
for thr in (0.05, 0.10, 0.25):
    for cut in (40, 60, 80):
        rec, ents = cj.g2_record(W, thr)
        for f in W["hosts"]:
            t = cj.trace(f, rec, ents, W["juris"], cut)
            if not near(t["traced_fraction"] + sum(b["share"] for b in t["breaks"]), 1.0, 1e-12):
                cons = False
check("traced + break shares = 1 for every firm, 3 thresholds x 3 cuts", cons)
g2 = RES["G2"]
check("7 breaks on 11 firms at threshold 0.25", g2["value"] == 7 and len(g2["firms"]) == 11)
check("break count by type", g2["by_type"] == {"BELOW_THRESHOLD": 1, "UNDISCLOSED": 3,
                                               "NOMINEE": 1, "REGISTRY_ABSENT": 1, "CYCLE": 1})
check("break count by tag", g2["by_tag"] == {"SHELL": 1, "SECRECY": 1,
                                             "SHELL+SECRECY": 4, "untagged": 1})
check("coverage 37 of 81 Mt traced", near(g2["coverage"]["covered"], 37.0)
      and near(g2["coverage"]["total"], 81.0))
e02 = {r["firm"]: r for r in cj.g2_read(W, threshold=0.10)["firms"]}["E02"]
check("five 20% holders: untraced at 0.25, fully traced at 0.10",
      cj.compliant_coverage([0.2] * 5, 0.25) == 0.0 and near(e02["traced_fraction"], 1.0))
rec_n, ents_n = cj.g2_record(W, unflag_nominees=True)
check("a nominee recorded as a person reads as traced",
      near(cj.traced_fraction("E05", rec_n, ents_n, W["juris"]), 1.0)
      and any(b["type"] == "NOMINEE" for b in
              {r["firm"]: r for r in g2["firms"]}["E05"]["breaks"]))
e07 = {r["firm"]: r for r in g2["firms"]}["E07"]
check("the cycle break holds the share a cross-holding series would assign (0.5)",
      near(e07["traced_fraction"], 0.5) and e07["breaks"][0]["type"] == "CYCLE"
      and near(e07["breaks"][0]["share"], 0.5))
check("every break node has an owner in the true graph or is a nominee",
      all(b["at"] in W["truth"] or b["at"] in W["nominee_for"] for b in g2["breaks"]))

# -- 5. G3 ownership-based accounting
g3 = RES["G3"]
check("production totals sum to 81", near(sum(g3["production"].values()), 81.0))
for t in cj.TARGETS:
    check("%s: table + UNATTRIBUTED = production total" % t,
          near(sum(g3["ownership"][t].values()) + g3["unattributed"], 81.0, 1e-9))
check("parent-level targets put 6.00 Mt in a SECRECY jurisdiction, BO residence 0",
      near(g3["secrecy_home"]["IMMEDIATE_PARENT"], 6.0)
      and near(g3["secrecy_home"]["ULTIMATE_PARENT"], 6.0)
      and near(g3["secrecy_home"]["BO_RESIDENCE"], 0.0))
tabs = g3["ownership"]
check("the three targets give three different tables",
      tabs["IMMEDIATE_PARENT"] != tabs["ULTIMATE_PARENT"] != tabs["BO_RESIDENCE"]
      and tabs["IMMEDIATE_PARENT"] != tabs["BO_RESIDENCE"])
check("no host jurisdiction keeps its production total under any target",
      all(tabs[t].get(j, 0.0) < g3["production"][j] for t in cj.TARGETS
          for j in g3["production"]))

# -- 6. G4 the gap
g4 = RES["G4"]
check("a secrecy index used as a chain weight is refused",
      raises(cj.CrossLevelRefused, cj.fsi_weight, 70))
check("the gap = 1 - G2 coverage", near(g4["value"], 1.0 - g2["coverage"]["share"], 1e-12))
check("the gap = G3's UNATTRIBUTED row / total", near(g4["lost"], g3["unattributed"], 1e-9))
check("break-type parts sum to the gap", near(sum(g4["by_type"].values()), g4["lost"], 1e-9))
curve = cj.g4_curve(W)
check("secrecy share never rises with the cut (%s)" % curve,
      all(a[1] >= b[1] - 1e-12 for a, b in zip(curve, curve[1:])))
check("secrecy share 0.420 at cut 60, 0.074 at cut 80",
      near(dict(curve)[60], 34.0 / 81.0) and near(dict(curve)[80], 6.0 / 81.0))
check("an unflagged nominee shrinks the measured gap by exactly E05 (5/81): a lower bound",
      near(RES["G4"]["value"] - RES["G4 nominee unflagged"]["value"], 5.0 / 81.0, 1e-12))

# -- 7. G5 the vote
check("auc: separated 1.0", cj.auc([1, 2, 3, 4], [0, 0, 1, 1]) == 1.0)
check("auc: reversed 0.0", cj.auc([4, 3, 2, 1], [0, 0, 1, 1]) == 0.0)
check("auc: all tied 0.5", cj.auc([1, 1, 1, 1], [0, 1, 0, 1]) == 0.5)
check("auc: one class empty is None", cj.auc([1, 2], [1, 1]) is None)
check("influence world: funding moves votes, yet does not out-predict preference",
      RES["G5 influence"]["branch"] == "NO_PATTERN"
      and RES["G5 influence"]["mechanism"]["reading"] == "INFLUENCE_CONSISTENT")
check("selection world: funding out-predicts preference and moves no vote",
      RES["G5 selection"]["branch"] == "PATTERN_HOLDS"
      and RES["G5 selection"]["mechanism"]["reading"] == "SELECTION_CONSISTENT")
check("preference world: NO_PATTERN, NEITHER",
      RES["G5 preference"]["branch"] == "NO_PATTERN"
      and RES["G5 preference"]["mechanism"]["reading"] == "NEITHER")
cands, winners = cj.g5_filter_world()
yes_c = sum(c["vote_post"] for c in cands) / float(len(cands))
yes_w = sum(c["vote_post"] for c in winners) / float(len(winners))
ac = RES["G5 filter, candidates"]["compare"]["auc_tie"]
aw = RES["G5 filter, winners"]["compare"]["auc_tie"]
check("filter world: the seated chamber votes yes more (%.3f vs %.3f)" % (yes_w, yes_c),
      yes_w > yes_c + 0.2)
check("filter world: funding AUC among winners below its AUC among candidates "
      "(%.3f vs %.3f) and both read NO_PATTERN" % (aw, ac),
      aw < ac and RES["G5 filter, winners"]["branch"] == "NO_PATTERN"
      and RES["G5 filter, candidates"]["branch"] == "NO_PATTERN")
check("no vote before the money: mechanism NOT_SEPARABLE",
      RES["G5 filter, winners"]["mechanism"]["reading"] == "NOT_SEPARABLE")
infl = cj.g5_world("influence")
check("G5 coverage counts only legislators with polling",
      RES["G5 influence"]["coverage"]["covered"] ==
      sum(1 for r in infl if r["pref"] is not None))

# -- 8. G6 the money token
check("band: rev 10, other 5, reserves +3 -> (0, 0.2, 0.3)",
      cj.reserve_share_band(10.0, 5.0, 3.0) == (0.0, 0.2, 0.3))
check("band: reserves +12 -> (0.7, 0.8, 1.0)",
      all(near(a, b) for a, b in zip(cj.reserve_share_band(10.0, 5.0, 12.0), (0.7, 0.8, 1.0))))
check("band: reserves fall -> zeros", cj.reserve_share_band(10.0, 5.0, -1.0) == (0.0, 0.0, 0.0))
check("band: no revenue -> None", cj.reserve_share_band(0.0, 5.0, 3.0) is None)
check("a driven-by share is refused", raises(cj.CausalShareRefused, cj.driven_share))
gd, gn = RES["G6 defense"], RES["G6 null"]
check("defense world: PATTERN_HOLDS, step near the built 4.0 (%.2f)" % gd["b"],
      gd["branch"] == "PATTERN_HOLDS" and 3.0 < gd["b"] < 5.0)
check("null world: NO_PATTERN", gn["branch"] == "NO_PATTERN")
check("the accounting band reads lower where volume answers the shortfall",
      gd["mean_band"][1] < gn["mean_band"][1] and gd["mean_band"][2] < gn["mean_band"][2])
a = cj.adequacy(30.0, 120.0, 20.0)
check("adequacy: 30 of reserves on 120 of imports = 3 months, GG 1.5, not short",
      near(a["months"], 3.0) and near(a["gg"], 1.5) and a["short"] is False)
check("adequacy: no imports -> months None", cj.adequacy(30.0, 0.0, 20.0)["months"] is None)

# -- 9. G7 consumption-based over time
check("consumption_based(100, 20, 5) = 85", cj.consumption_based(100.0, 20.0, 5.0) == 85.0)
check("consumption_based with an absent term is None",
      cj.consumption_based(100.0, None, 5.0) is None)
g7 = RES["G7"]
check("dPB = dDomestic + dExportEmbodied every measured year",
      all(near(o["dpb"], o["d_dom"] + o["d_eex"], 1e-9) for o in g7["years"]
          if o["d_dom"] is not None))
check("G7 is GAP: 2025 and 2026 plateau years are past the last consumption year",
      g7["branch"] == "GAP" and g7["unread_plateau"] == [2025, 2026])
check("2024: production flat, consumption-based not flat",
      [o["year"] for o in g7["measured_plateau"]] == [2024]
      and g7["measured_plateau"][0]["cb_flat"] is False)
check("coverage 7 of 9 years", g7["coverage"]["covered"] == 7 and g7["coverage"]["total"] == 9)
check("with no lag every plateau year is read", cj.g7_read(cj.g7_world(cb_lag=0))["branch"]
      == "PATTERN_HOLDS")

# -- 10. the chain
check("six arrows, seven nodes, as the order's chain", len(cj.LINKS) == 6)
check("two correlational arrows: an inference of an inference",
      cj.inference_depth() == 2 and RES["CHAIN coupled"]["inference_of_inference"] is True)
check("the record's unit changes at every arrow (5)", cj.level_changes() == 5)
check("an end-to-end effect is refused", raises(cj.CompositeRefused, cj.chain_effect))
cc, ci = RES["CHAIN coupled"], RES["CHAIN independent"]
check("coupled missingness: joined coverage above the independence product (%.3f vs %.3f)"
      % (cc["coverage"]["share"], cc["independence_product"]),
      cc["coverage"]["share"] > cc["independence_product"] + 0.03)
check("independent missingness: joined within 0.05 of the product (%.3f vs %.3f)"
      % (ci["coverage"]["share"], ci["independence_product"]),
      abs(ci["coverage"]["share"] - ci["independence_product"]) < 0.05)

# -- 11. constructed only
ids = set(W["entities"]) | set(W["juris"])
check("every entity and jurisdiction id is synthetic",
      all(re.match(r"^(J\d|[EAHPN]\d\d)$", i) for i in ids))
countries = set(r["country"] for r in cj.g1_world("null")) | \
    set(r["country"] for r in cj.g6_world("null"))
check("every country id is synthetic", all(re.match(r"^C\d\d$", c) for c in countries))
check("every legislator id is synthetic",
      all(re.match(r"^[LK]\d{3}$", r["id"]) for r in infl + cands))

# -- 12. plumbing
p = subprocess.run([sys.executable, os.path.join(HERE, "chain_join.py"), "--selftest"],
                   capture_output=True, text=True)
check("--selftest refuses with exit 2", p.returncode == 2)
named = re.search(r"([\w./-]+\.py)", p.stderr.split(":", 1)[1]).group(1)
check("and names a test file that exists from the repo root",
      os.path.isfile(os.path.join(ROOT, named)))
p = subprocess.run([sys.executable, os.path.join(HERE, "chain_join.py"), "--choices"],
                   capture_output=True, text=True)
check("--choices prints all %d choices" % len(cj.CHOICES),
      p.returncode == 0 and p.stdout.count("[CHOICE ") == len(cj.CHOICES))
tree = ast.parse(SRC)
dict_src = ast.get_source_segment(SRC, [n for n in tree.body if isinstance(n, ast.Assign)
                                        and getattr(n.targets[0], "id", "") == "CHOICES"][0])
rest = SRC.replace(dict_src, "")
uncited = [k for k in cj.CHOICES if not re.search(r"CHOICE %d\b" % k, rest)]
check("every CHOICE is cited at a site outside its declaration %s" % uncited, not uncited)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import no_severity  # noqa: E402
check("render screens clean, no exemption", no_severity.check(TEXT)[0])
sample = open(os.path.join(HERE, "samples", "render.sample.txt"), encoding="utf-8").read()
check("samples/render.sample.txt is the current render", sample == TEXT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import known_answer as ka  # noqa: E402
ka.seed()
reg = ka.registry_ids()
for m in ("coverage", "traced_fraction", "consumption_based", "reserve_share_band"):
    check("known-answer registers %s" % m,
          "extraction-chain-join/chain_join.py::" + m in reg)
for f in ("chain_join.py", "test_chain.py", "WORK_ORDER.md", "SOURCES.md",
          "README.md", "CLAIM_TABLE.md"):
    path = os.path.join(HERE, f)
    ok = os.path.isfile(path)
    if ok:
        try:
            open(path, encoding="ascii").read()
        except UnicodeDecodeError:
            ok = False
    check("%s exists and is ASCII" % f, ok)
for rel, marker in (("sim-span/three_column.py", "def ols"),
                    ("sheet-structure-scan/no_severity.py", "def check")):
    path = os.path.join(ROOT, rel)
    check("import %s resolves with marker %r" % (rel, marker),
          os.path.isfile(path) and marker in open(path, encoding="utf-8").read())

print("checks: %d   failed: %d" % (N["pass"] + N["fail"], N["fail"]))
sys.exit(1 if N["fail"] else 0)
