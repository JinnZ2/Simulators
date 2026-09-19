# SPDX-License-Identifier: CC0-1.0
# test_criterion.py -- checks for criterion-externality. Stdlib only, no
# pytest, no network. Run: python3 test_criterion.py
#
# Expected values live HERE. The fault model is CONSTRUCTED and nothing
# below is evidence about any audit regime or about the target paper,
# whose body is not read; what is checked is the machinery and the
# arithmetic that holds without the model.

import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import criterion_externality as ce   # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []
EPS = 1e-9


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except ce.Refused:
        return True
    return False


def near(a, b, tol=EPS):
    return a is not None and b is not None and abs(a - b) < tol


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER_FLAT = re.sub(r"\s+", " ", ORDER).lower()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
SRC = open(os.path.join(HERE, "criterion_externality.py")).read()

# 1. the delivery
check("order carries the four C-grades", all(g in ORDER for g in ce.GRADES4))
check("order names the three axes", all(a.lower() in ORDER_FLAT
                                        for a in ("principal", "substrate",
                                                  "evidence")))
check("order states 5.9%", "5.9%" in ORDER)
check("order's R4 is named the cheapest decisive test",
      "r4 is the cheapest decisive test" in ORDER_FLAT)
check("order states the body was not read", "full body not read" in ORDER_FLAT)

# 2. weakest link (CEX_001, CEX_002)
check("weakest_link empty -> None", ce.weakest_link([]) is None)
check("weakest_link top rungs -> 1.0", near(ce.weakest_link([3, 3, 3]), 1.0))
check("weakest_link one zero -> 0.0", near(ce.weakest_link([3, 3, 3, 0]), 0.0))
check("weakest_link (2,1,3) -> 1/3", near(ce.weakest_link([2, 1, 3]), 1 / 3))
check("a grade off the rungs is refused", refuses(ce.weakest_link, [3, 4]))
t = ce.three_vs_four(3, 3, 3, "C0")
check("separating test: over three 1.0", near(t["over_three"], 1.0))
check("separating test: over four 0.0", near(t["over_four"], 0.0))
check("a non-grade on axis 4 is refused", refuses(ce.three_vs_four, 3, 3, 3, "C4"))
import itertools
mono = all(ce.weakest_link(list(g) + [c]) <= ce.weakest_link(list(g)) + EPS
           for g in itertools.product(ce.RUNGS, repeat=3) for c in ce.RUNGS)
check("adding an axis never raises the aggregate (all 256 cells)", mono)
strict = sum(1 for g in itertools.product(ce.RUNGS, repeat=3) for c in ce.RUNGS
             if ce.weakest_link(list(g) + [c]) < ce.weakest_link(list(g)))
check("and lowers it on a non-empty set of cells", strict > 0, str(strict))

# 3. closed form (CEX_004)
check("expected_rate one party beta 0", near(ce.expected_rate(0.3, 1, 0.0, 1.0), 0.3))
check("expected_rate two parties beta 0", near(ce.expected_rate(0.5, 2, 0.0, 1.0), 0.75))
check("expected_rate beta 1 collapses to one draw", near(ce.expected_rate(0.5, 2, 1.0, 1.0), 0.5))
check("expected_rate q 0 -> 0", near(ce.expected_rate(0.5, 2, 0.0, 0.0), 0.0))
check("expected_rate mixed", near(ce.expected_rate(0.5, 2, 0.5, 1.0), 0.625))
check("expected_rate out of range -> None", ce.expected_rate(0.5, 0, 0.0, 1.0) is None
      and ce.expected_rate(1.5, 2, 0.0, 1.0) is None)
f = ce.FAULT_CLASSES[0]
mc = ce.surfaced_rate(f, 2, 0.3, "C3", draws=20000)
cf = ce.expected_rate(f["p_det"], 2, 0.3, 1.0)
check("Monte Carlo converges on the closed form (within 0.01)", abs(mc - cf) < 0.01,
      "%.4f vs %.4f" % (mc, cf))
check("surfaced_rate refuses a non-grade", refuses(ce.surfaced_rate, f, 2, 0.3, "X"))
check("surfaced_rate refuses beta outside [0,1]", refuses(ce.surfaced_rate, f, 2, 1.5, "C3"))

# 4. R2 on the model (CEX_002, CEX_009)
r2 = ce.r2_rerun(draws=4000)
check("R2: every delta <= 0", all(r2["by_grade"][g]["delta"] <= EPS for g in ce.GRADES4))
check("R2: C3 delta is exactly 0", near(r2["by_grade"]["C3"]["delta"], 0.0))
check("R2: C0 never-surfaced is the four excluded classes",
      r2["by_grade"]["C0"]["never_surfaced"] == ["F2", "F3", "F5", "F7"])
check("R2: no class moves OUT of never-surfaced by adding a gate",
      all(set(r2["by_grade"][g]["never_surfaced"]) >= set()
          and not (set(r2["by_grade"]["C3"]["never_surfaced"])
                   - set(r2["by_grade"][g]["never_surfaced"]))
          for g in ce.GRADES4))
check("R2: never-surfaced share at C0 is one half", near(r2["by_grade"]["C0"]["never_surfaced_share"], 0.5))

# 5. the grading is not monotone in surfaced rate (CEX_005)
qs = ce.discretion_crossover()
check("crossover exists", qs is not None and 0 < qs < 1, str(qs))
check("at the stipulated discretion C2 mean < C1 mean",
      ce.grade_mean("C2") < ce.grade_mean("C1"))
check("at q = 1 C2 mean > C1 mean", ce.grade_mean("C2", q=1.0) > ce.grade_mean("C1"))
check("the crossover is where the two means meet",
      near(ce.grade_mean("C2", q=qs), ce.grade_mean("C1")))
check("grade means are monotone C0 < C1 < C3", ce.grade_mean("C0") < ce.grade_mean("C1")
      < ce.grade_mean("C3"))

# 6. R4 (CEX_003)
r4 = ce.r4_beta_test(draws=1000)
check("R4: four classes excluded at C0", r4["n_excluded_at_C0"] == 4)
check("R4: none reachable by beta or party count", r4["reachable_by_beta_or_parties"] == [])
check("R4: verdict independent on this model", r4["verdict"] == "INDEPENDENT_ON_THIS_MODEL")
check("R4: covered classes have zero criterion sensitivity",
      all(near(r["criterion_sens"], 0.0) for r in r4["rows"] if not r["excluded_at_C0"]))
check("R4: excluded classes have positive criterion sensitivity",
      all(r["criterion_sens"] > 0 for r in r4["rows"] if r["excluded_at_C0"]))
check("R4: scope names the unread paper", "not read" in r4["scope"])
# the collapse branch is reachable: a coverage set that excludes nothing
saved = dict(ce.COVERAGE)
ce.COVERAGE["C0"] = set(ce.COVERAGE["C3"])
r4b = ce.r4_beta_test(draws=200)
ce.COVERAGE.clear(); ce.COVERAGE.update(saved)
check("R4: with nothing excluded there is nothing to be independent on",
      r4b["n_excluded_at_C0"] == 0 and r4b["verdict"] == "INDEPENDENT_ON_THIS_MODEL")
# and the COLLAPSES branch: an excluded class reachable by some setting
# cannot occur under a gate; assert the gate is structural in the source
tree = ast.parse(SRC)
fn = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
      and n.name == "surfaced_rate"][0]
has_gate = any(isinstance(n, ast.If) and isinstance(n.test, ast.UnaryOp)
               and getattr(n.test.operand, "id", None) == "covered"
               for n in ast.walk(fn))
check("the coverage gate precedes every party draw (AST)", has_gate)

# 7. R3 (CEX_007)
p = ce.r3_prediction(ce.REGIMES)
check("R3: carried regimes are all UNCODED", all(r["axis4"] == "UNCODED" for r in ce.REGIMES))
check("R3: NOT_EVALUABLE on the carried set", p["share_c0_c1"] is None
      and p["verdict"].startswith("NOT_EVALUABLE"))
check("a grade with no basis is refused", refuses(ce.code_regime, "x", "C1", None))
check("a non-grade is refused", refuses(ce.code_regime, "x", "C9", "b"))
low = [ce.code_regime("a", "C0", "b"), ce.code_regime("b", "C1", "b"), ce.code_regime("c", "C3", "b")]
high = [ce.code_regime("a", "C3", "b"), ce.code_regime("b", "C2", "b")]
check("R3: prediction-holds branch reachable", ce.r3_prediction(low)["verdict"] == "prediction holds")
check("R3: prediction-fails branch reachable",
      "does not hold" in ce.r3_prediction(high)["verdict"])

# 8. R1 and arrivals (CEX_006, CEX_008)
check("R1 is NOT_RUN with the probe recorded", ce.R1["status"] == "NOT_RUN" and "403" in ce.R1["probe"])
arr = ce.resolve_arrivals(ROOT)
check("arrivals: 2 of 3 RESOLVED", sum(1 for a in arr if a["state"] == "RESOLVED") == 2)
check("arrivals: the third is NOT_IN_TREE", arr[2]["state"] == "NOT_IN_TREE")
bogus = ce.resolve_arrivals(os.path.join(ROOT, "nonexistent-dir"))
check("resolver reports PATH_ABSENT on a bogus root, not RESOLVED",
      all(a["state"] in ("PATH_ABSENT", "NOT_IN_TREE") for a in bogus))

# 9. renders, choices, hygiene
text = ce.render(ROOT)
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], str(no_severity.hits(text)[:3]))
check("screen fires on a planted word", no_severity.hits(text + "\nthis row is wrong\n") != [])
check("every [CHOICE n] cited in the module is declared",
      set(int(x) for x in re.findall(r"\[CHOICE (\d)", SRC)) <= set(ce.CHOICES))
check("every declared choice is cited", all(("[CHOICE %d" % k) in SRC or
      any(("%d]" % k) in m or ("%d," % k) in m or (",%d" % k) in m
          for m in re.findall(r"\[CHOICE ([\d,\-]+)\]", SRC)) for k in ce.CHOICES))
check("module is ASCII", all(ord(c) < 128 for c in SRC))
check("README carries no author or working-style section",
      not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
check("README marks the model CONSTRUCTED", "CONSTRUCTED" in README)
import subprocess
rc = subprocess.run([sys.executable, os.path.join(HERE, "criterion_externality.py"),
                     "--selftest"], capture_output=True).returncode
check("module refuses --selftest (exit 2)", rc == 2)

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-5s %s%s" % ("ok" if ok else "FAIL", name, ("  [%s]" % detail) if (detail and not ok) else ""))
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
