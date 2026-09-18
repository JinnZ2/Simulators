# SPDX-License-Identifier: CC0-1.0
# test_partition.py -- checks for measurand-partition. Stdlib only, no
# pytest, no network. Run: python3 test_partition.py
#
# Expected values live HERE. Every constructed record in the modules is
# marked PROPOSED and nothing below is evidence about any person, program,
# structure or piece of wood; what is checked is the machinery.

import ast
import copy
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import common                       # noqa: E402
import wo1_partition as w1          # noqa: E402
import wo2_band_sweep as w2         # noqa: E402
import wo3_control_manifest as w3   # noqa: E402
import wo4_lumber as w4a            # noqa: E402
import wo4_survival as w4b          # noqa: E402
import wo5_deselection as w5        # noqa: E402
import no_severity                  # noqa: E402
import known_answer                 # noqa: E402

CHECKS = []
EPS = 1e-9


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except common.Refused:
        return True
    return False


def near(a, b):
    return a is not None and b is not None and abs(a - b) < EPS


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER_FLAT = re.sub(r"\s+", " ", ORDER).lower()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
MODULES = ("common.py", "wo1_partition.py", "wo2_band_sweep.py",
           "wo3_control_manifest.py", "wo4_lumber.py", "wo4_survival.py",
           "wo5_deselection.py")

# ---------------------------------------------------------------------------
# 1. the delivery, read out of WORK_ORDER.md
# ---------------------------------------------------------------------------

check("five work orders are in the delivery",
      all("## WO-%d" % i in ORDER for i in range(1, 6)))
check("status tags are the delivery's",
      "OBSERVED / DERIVED / PROPOSED" in ORDER and common.STATUS ==
      ("OBSERVED", "DERIVED", "PROPOSED"))
check("the four axes are the order's",
      all(t in ORDER for t in ("A1 FRAME", "A2 CHANNEL", "A3 FREQUENCY",
                                "A4 DOMAIN LOAD")) and len(w1.AXES) == 4)
check("WO-3's seven variables are the order's",
      all(v in ORDER_FLAT for v in w3.VARIABLES) and len(w3.VARIABLES) == 7)
check("WO-3's three statuses are the order's",
      "HELD / ADVISED ON / NOT TOUCHED" in ORDER and
      w3.STATUSES == ("HELD", "ADVISED_ON", "NOT_TOUCHED", "UNDECLARED"))
check("WO-5's five capacities are the order's",
      all(c.replace("_", " ") in ORDER_FLAT for c in
          ("balance", "spatial awareness", "load tolerance",
           "controlled falling", "transferable motor structure"))
      and len(w5.CAPACITIES) == 5)
check("the common structure names four populations",
      all(p in ORDER for p in ("WO-1  the child", "WO-3  the observer",
                                "WO-4  the building method",
                                "WO-5  the released athlete"))
      and len(common.POPULATIONS) == 4)
check("the 4x4 pair and the ~40% are the order's",
      "3.5x3.5" in ORDER and "~40%" in ORDER and "FOURTH POWER" in ORDER)

# ---------------------------------------------------------------------------
# 2. common: the record shape
# ---------------------------------------------------------------------------

check("all four delivered populations read UNPARTITIONED",
      all(p["verdict"] == "UNPARTITIONED" for p in common.POPULATIONS))
check("an empty unmeasured set reads PARTITIONED",
      common.attribution("x", "s", [], "x")["verdict"] == "PARTITIONED")
check("an unenumerated set reads NOT_EVALUABLE, not PARTITIONED",
      common.attribution("x", "s", None, "x")["verdict"] == "NOT_EVALUABLE")
check("residual assigned off the observed thing reads ASSIGNED_ELSEWHERE",
      common.attribution("x", "s", ["v"], "the interval")["verdict"]
      == "ASSIGNED_ELSEWHERE")
check("attribution refuses an absent field",
      refuses(common.attribution, "", "s", [], "x") and
      refuses(common.attribution, "x", "s", [], "UNDECLARED"))
check("every ATTRIBUTION member is reachable",
      {common.attribution("x", "s", u, a)["verdict"] for u, a in
       ((["v"], "x"), ([], "x"), (["v"], "y"), (None, "x"))} == set(common.ATTRIBUTION))

# ---------------------------------------------------------------------------
# 3. WO-1
# ---------------------------------------------------------------------------

o = w1.DEMO[0]
check("an axis MEASURED with no instrument is refused [CHOICE 1]",
      refuses(w1.read_observation, dict(o, axes=dict(o["axes"], A1_FRAME={
          "state": "MEASURED", "instrument": None}))))
check("an axis not entered at all is refused (absent is not UNMEASURED)",
      refuses(w1.read_observation, dict(o, axes={k: v for k, v in
                                                  o["axes"].items() if k != "A2_CHANNEL"})))
check("a non-bool interaction flag is refused",
      refuses(w1.read_observation, dict(o, interaction_entered="yes")))
check("residual is NOT_SEPARABLE naming every unmeasured axis and the interaction",
      w1.residual(o)["state"] == "NOT_SEPARABLE" and
      w1.residual(o)["missing"] == list(w1.AXES) + ["INTERACTION"] and
      w1.residual(o)["residual"] is None)
check("residual is a candidate only with all four axes and the interaction entered",
      w1.residual(w1.DEMO[5])["state"] == "RESIDUAL_CANDIDATE" and
      w1.residual(w1.DEMO[6])["missing"] == ["A4_DOMAIN_LOAD"])
check("the residual candidate carries the raw score and says its size is not shown non-zero",
      near(w1.residual(w1.DEMO[5])["residual"], 0.38) and
      "NOT shown" in w1.residual(w1.DEMO[5])["reads"])
b = w1.two_setting_bound(w1.DEMO)
check("two-setting arm: one moved label of two establishes a floor of 0.50",
      b["state"] == "FLOOR_ESTABLISHED" and near(b["floor"], 0.5) and
      b["moved"] == ["p-01"] and b["n_two_settings"] == 2)
check("single-setting individuals are UNBOUNDED, out of the denominator [CHOICE 2]",
      b["unbounded"] == ["p-03", "p-04", "p-05"])
check("with no individual labelled twice the arm is NOT_RUN, floor None not 0",
      w1.two_setting_bound([w1.DEMO[2], w1.DEMO[4]])["state"] == "NOT_RUN" and
      w1.two_setting_bound([w1.DEMO[2], w1.DEMO[4]])["floor"] is None)
check("two settings, no movement: NO_CASE_FOUND at floor 0, stated as not established above it",
      w1.two_setting_bound([w1.DEMO[2], w1.DEMO[3]])["state"] == "NO_CASE_FOUND")
check("WO-1 has no axis-to-performance model: residual() never subtracts",
      not re.search(r"residual\s*=.*-", open(os.path.join(HERE, "wo1_partition.py")).read()))

# ---------------------------------------------------------------------------
# 4. WO-2
# ---------------------------------------------------------------------------

reads = {c["subject"]: w2.single_point(c, w2.STANDARD) for c in w2.DEMO}
check("THE MEASUREMENT FAULT: band-low, band-high and flat-low return one point read",
      near(reads["band-low"], 0.1) and near(reads["band-high"], 0.1)
      and near(reads["flat-low"], 0.1))
states = {c["subject"]: w2.band(c)["state"] for c in w2.DEMO}
check("the sweep separates them: BAND_LOCATED x2 (opposite sides), NOT_REGISTERED",
      states["band-low"] == "BAND_LOCATED" and states["band-high"] == "BAND_LOCATED"
      and states["flat-low"] == "NOT_REGISTERED")
pos = {c["subject"]: w2.report(c, w2.STANDARD)["position"] for c in w2.DEMO}
check("standard point sits ABOVE_CEILING for band-low and BELOW_FLOOR for band-high",
      pos["band-low"] == "ABOVE_CEILING" and pos["band-high"] == "BELOW_FLOOR"
      and pos["flat-low"] == "NOT_LOCATABLE" and pos["band-open"] == "IN_BAND")
check("floor, ceiling, width are read off the curve",
      w2.band(w2.DEMO[0])["floor"] == 1 and w2.band(w2.DEMO[0])["ceiling"] == 5
      and w2.band(w2.DEMO[0])["width"] == 4)
check("a curve still registering at the top is CEILING_NOT_REACHED, ceiling None",
      states["band-open"] == "CEILING_NOT_REACHED" and w2.band(w2.DEMO[3])["ceiling"] is None)
short = w2.read_curve("short", [(1, 0.9), (2, 0.9)])
check("fewer than three levels is NOT_ESTIMABLE [CHOICE 2]",
      w2.band(short)["state"] == "NOT_ESTIMABLE")
check("a level not swept reads NOT_SWEPT, not interpolated",
      w2.single_point(w2.DEMO[0], 4.5) == "NOT_SWEPT")
check("read_curve refuses a level swept twice and a performance outside [0,1]",
      refuses(w2.read_curve, "d", [(1, 0.5), (1, 0.6)]) and
      refuses(w2.read_curve, "d", [(1, 1.5)]))
check("every band state and every position is reached by the demo or a fixture",
      {w2.band(c)["state"] for c in w2.DEMO} | {w2.band(short)["state"]} ==
      {"BAND_LOCATED", "NOT_REGISTERED", "CEILING_NOT_REACHED", "NOT_ESTIMABLE"}
      and set(pos.values()) | {"NOT_SWEPT"} == set(w2.POSITIONS))

# ---------------------------------------------------------------------------
# 5. WO-3
# ---------------------------------------------------------------------------

acad, day = w3.DEMO_PROGRAMS
g = w3.control_gradient(acad)
check("academy-as-described grades 0.40: two HELD of five controllable, ADVISED_ON counted apart",
      near(g["gradient"], 0.4) and g["advised_on"] == ["nutrition", "hydration"]
      and len(g["held"]) == 2)
check("ADVISED_ON never enters the gradient as a fraction [CHOICE 1]",
      near(w3.control_gradient(w3.read_program(dict(acad, statuses={
          v: "ADVISED_ON" for v in w3.VARIABLES})))["gradient"], 0.0))
gd = w3.control_gradient(day)
check("an undeclared variable makes the gradient NOT_COMPUTABLE, naming it",
      gd["state"] == "NOT_COMPUTABLE" and gd["gradient"] is None and
      "nutrition" in gd["undeclared"])
check("a variable absent from the record is UNDECLARED, never NOT_TOUCHED",
      day["statuses"]["hydration"] == "UNDECLARED")
check("a variable outside the manifest is refused",
      refuses(w3.read_program, dict(acad, statuses=dict(acad["statuses"], luck="HELD"))))
t = w3.accuracy_vs_gradient(w3.DEMO_PROGRAMS)
check("WO-3b is NOT_EVALUABLE with no program carrying a measured accuracy [CHOICE 2]",
      t["state"] == "NOT_EVALUABLE" and t["n"] == 0)


def _prog(pid, held, acc):
    st = {v: ("HELD" if i < held else "NOT_TOUCHED")
          for i, v in enumerate(w3.VARIABLES)}
    return w3.read_program({"id": pid, "statuses": st, "accuracy": acc,
                            "status": "PROPOSED"})


rise = [_prog("a", 1, 0.3), _prog("b", 3, 0.5), _prog("c", 5, 0.7)]
fall = [_prog("a", 1, 0.7), _prog("b", 3, 0.5), _prog("c", 5, 0.3)]
check("WO-3b trend RISES and FALLS on constructed programs; not constant",
      w3.accuracy_vs_gradient(rise)["trend"] == "RISES" and
      w3.accuracy_vs_gradient(fall)["trend"] == "FALLS")
check("WO-3b at one gradient is NOT_EVALUABLE (no trend)",
      w3.accuracy_vs_gradient([_prog("a", 2, 0.3), _prog("b", 2, 0.5),
                               _prog("c", 2, 0.7)])["state"] == "NOT_EVALUABLE")
fu = w3.accuracy_floor(w3.DEMO_SHARES_UNDECLARED)
check("WO-3c ceiling is UNDECLARED while any not-controllable share is",
      fu["state"] == "UNDECLARED" and fu["ceiling"] is None and len(fu["missing"]) == 2)
fs = w3.accuracy_floor(w3.DEMO_SHARES_STATED)
check("WO-3c ceiling = 1 - 0.25 - 0.15 = 0.60 on declared shares [CHOICE 3]",
      near(fs["ceiling"], 0.60))
check("a reported 0.60 reads as 1.00 of achievable against that ceiling, None against UNDECLARED",
      near(w3.read_against_ceiling(0.60, fs), 1.0) and
      w3.read_against_ceiling(0.60, fu) is None)
check("shares summing past 1 are refused",
      refuses(w3.accuracy_floor, {"endocrine developmental timing": 0.7,
                                  "experienced social environment": 0.5}))
check("the 6.3 h figure appears in the render and in no computation",
      "6.3 h" in w3.render() and "6.3" not in
      open(os.path.join(HERE, "wo3_control_manifest.py")).read().split("def render")[0]
      .split('"""', 2)[2])

# ---------------------------------------------------------------------------
# 6. WO-4a
# ---------------------------------------------------------------------------

check("4x4: (3.5/4)^4 = 0.5862, the order's ~40% (41.4%) holds",
      near(w4a.stiffness_ratio(4, 4, 3.5, 3.5), (3.5 / 4) ** 4) and
      abs(1 - w4a.stiffness_ratio(4, 4, 3.5, 3.5) - 0.414) < 0.001)
check("depth only: (3.5/4)^3 = 0.670; the fourth power needs the width",
      near(w4a.depth_only_ratio(4, 3.5), (3.5 / 4) ** 3) and
      near(w4a.stiffness_ratio(4, 4, 3.5, 3.5),
           w4a.depth_only_ratio(4, 3.5) * 3.5 / 4))
check("strength ratio on the 4x4 is the cube, 0.670, not the stiffness 0.586",
      near(w4a.strength_ratio(4, 4, 3.5, 3.5), (3.5 / 4) ** 3))
q = w4a.quantity_mismatch()
check("the arithmetic names stiffness and the test measures strength; flagged",
      q["same_quantity"] is False and near(q["strength_kept_4x4"], 0.669921875))
check("2x4 keeps 0.502 of a full 2x4: the square case understates the general one",
      near(w4a.stiffness_ratio(2, 4, 1.5, 3.5), 0.75 * (3.5 / 4) ** 3))
check("a non-positive dimension is None, never 0 or 1",
      w4a.stiffness_ratio(0, 4, 3.5, 3.5) is None and
      w4a.strength_ratio(4, 4, 3.5, 0) is None and w4a.depth_only_ratio(4, 0) is None)
check("stiffness_ratio is registered in tools/known_answer.py",
      "measurand-partition/wo4_lumber.py::stiffness_ratio" in known_answer.EXPECTED_METRICS)
check("the table's linear reduction on the 4x4 is 12.5%",
      near([r for r in w4a.table() if r["nominal"] == "4x4"][0]["linear_reduction"], 0.125))

# ---------------------------------------------------------------------------
# 7. WO-4b
# ---------------------------------------------------------------------------

sp = w4b.split_curves(w4b.DEMO)
check("one matched stratum, one unmatched; the valley records enter no comparison",
      sp["matched_strata"] == [(1870, "ridge")] and sp["unmatched_strata"] == [(1900, "valley")])
check("four arms, two per population, computed apart",
      set(sp["curves"]) == {(p, a) for p in w4b.POPULATIONS
                            for a in ("MAINTAINED_IN_USE", "SURVIVING_NEGLECTED")})
check("maintenance UNKNOWN is excluded and counted", sp["unknown_maintenance"] == ["c-04"])
check("pooled() refuses, naming the split",
      refuses(w4b.pooled, w4b.DEMO))
check("REMOVED is censoring: t-04 removed at 82 leaves the maintained curve at 1.0 [CHOICE 2]",
      near(w4b.survival_at(sp["curves"][("TRANSMITTED", "MAINTAINED_IN_USE")], 150), 1.0))
check("FAILED is the event: the transmitted neglected arm falls to 0.5 by 150",
      near(w4b.survival_at(sp["curves"][("TRANSMITTED", "SURVIVING_NEGLECTED")], 150), 0.5))
check("kaplan_meier over nothing is None, never a flat 1.0",
      w4b.kaplan_meier([]) is None and w4b.survival_at(None, 100) is None)
check("a structure with no construction year is refused",
      refuses(w4b.read_structure, dict(w4b.DEMO[0], built=None)))
check("FAILED without an event year, and observed before built, are refused",
      refuses(w4b.read_structure, dict(w4b.DEMO[0], status="FAILED", event=None)) and
      refuses(w4b.read_structure, dict(w4b.DEMO[0], observed=1800)))
cs = w4b.claim_scope(150, True)
check("a maintenance-conditional claim reads against the maintained arm only, declared not parsed",
      cs["readable_against"] == ("MAINTAINED_IN_USE",) and
      refuses(w4b.claim_scope, 150, "with proper maintenance"))
check("an unconditional claim reads against both arms",
      len(w4b.claim_scope(150, False)["readable_against"]) == 2)

# ---------------------------------------------------------------------------
# 8. WO-5
# ---------------------------------------------------------------------------

pod = w5.score_podium(w5.DEMO)
lea = w5.score_learned(w5.DEMO)
man = w5.manufactured(w5.DEMO)
check("PODIUM: 2 succeed, 3 fail, 3 untrained peers not on the scale",
      len(pod["success"]) == 2 and len(pod["failure"]) == 3 and len(pod["not_on_scale"]) == 3)
check("LEARNED: deselected AHEAD on 4 of 5, TIE on the released-for capacity",
      sum(1 for p in lea["per_capacity"].values() if p["verdict"] == "AHEAD") == 4
      and lea["per_capacity"]["load_tolerance"]["verdict"] == "TIE")
check("MANUFACTURED: the three PODIUM failures are the manufactured category",
      man["count"] == 3 and man["released_for_behind"] == ["load_tolerance"])
check("LEARNED is NOT_COMPUTABLE without untrained peers, manufactured None not 0",
      w5.score_learned([a for a in w5.DEMO if a["group"] != "UNTRAINED_PEER"])["state"]
      == "NOT_COMPUTABLE" and
      w5.manufactured([a for a in w5.DEMO if a["group"] != "UNTRAINED_PEER"])["count"] is None)
check("BEHIND is reachable: a cohort where the deselected trail its peers",
      w5.score_learned([w5.DEMO[5], w5.DEMO[6],
                        w5.read_athlete(dict(w5.DEMO[2], measures={
                            c: 0.2 for c in w5.CAPACITIES}))])
      ["per_capacity"]["balance"]["verdict"] == "BEHIND")
check("a DESELECTED athlete must name the released-for capacity or UNDECLARED",
      refuses(w5.read_athlete, dict(w5.DEMO[2], released_for=None)) and
      w5.read_athlete(dict(w5.DEMO[2], released_for="UNDECLARED"))["released_for"] == "UNDECLARED")
check("released_for on a non-deselected athlete is refused",
      refuses(w5.read_athlete, dict(w5.DEMO[0], released_for="balance")))
check("import line: an undeclared measurand is refused, PODIUM is never a default",
      refuses(w5.import_line, ["x"], None) and refuses(w5.import_line, ["x"], "") and
      w5.import_line(["x"], "PODIUM")["podium_imported"] is True and
      w5.import_line(["x"], "LEARNED")["podium_imported"] is False)
check("the WO-5 render says the demo is a known-answer run on the scorer",
      "known-answer run on the scorer" in w5.render())

# ---------------------------------------------------------------------------
# 9. renders, screens, CLI, hygiene
# ---------------------------------------------------------------------------

for mod, name in ((common, "common"), (w1, "wo1"), (w2, "wo2"), (w3, "wo3"),
                  (w4a, "wo4a"), (w4b, "wo4b"), (w5, "wo5")):
    text = mod.render()
    check("%s render screens clean through no_severity, no exemption" % name,
          no_severity.hits(text) == [], "%s" % no_severity.hits(text)[:3])
    if hasattr(mod, "CHOICES"):
        check("%s render prints every [CHOICE n]" % name,
              all("[CHOICE %d]" % k in text for k in mod.CHOICES))
    if name != "common":
        check("%s render marks its data CONSTRUCTED or nothing measured" % name,
              "CONSTRUCTED" in text or "nothing measured" in text)
check("the screen fires on a planted word",
      no_severity.hits(w1.render() + "\nthis row is wrong\n") != [])
for fn in MODULES:
    p = subprocess.run([sys.executable, os.path.join(HERE, fn), "--selftest"],
                       capture_output=True)
    check("%s refuses --selftest with exit 2" % fn, p.returncode == 2)
    p = subprocess.run([sys.executable, os.path.join(HERE, fn)], capture_output=True)
    check("%s bare invocation renders and exits 0" % fn,
          p.returncode == 0 and len(p.stdout) > 100)
for fn in MODULES + ("test_partition.py",):
    src = open(os.path.join(HERE, fn), "rb").read()
    check("%s is ASCII" % fn, all(b < 128 for b in src))
    ast.parse(src.decode("ascii"), feature_version=(3, 9))
    check("%s parses under 3.9" % fn, True)
check("README carries no author or working-style section",
      not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
check("README states that everything constructed is PROPOSED",
      "PROPOSED" in README and "CONSTRUCTED" in README)
check("no module names any real person, program, county or product",
      not any(re.search(r"\b(Inc|LLC|County|Academy of)\b",
                        open(os.path.join(HERE, fn)).read()) for fn in MODULES))

# ---------------------------------------------------------------------------

failed = [(n, d) for n, ok, d in CHECKS if not ok]
for n, ok, d in CHECKS:
    print("%s  %s%s" % ("ok  " if ok else "FAIL", n, ("  -- " + d) if (d and not ok) else ""))
print()
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
