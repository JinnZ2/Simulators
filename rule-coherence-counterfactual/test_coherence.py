# SPDX-License-Identifier: CC0-1.0
# test_coherence.py -- checks for rule-coherence-counterfactual. Stdlib
# only, no pytest, no network. Run: python3 test_coherence.py
#
# Expected values live HERE. Every world in the module is CONSTRUCTED
# with a declared generative model; no model was run and nothing below is
# evidence about any rule, record or observer. What is checked is that the
# four A1 branches, the A2b count and the A3 split behave as the machinery
# claims.

import ast
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import rule_coherence as rc          # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []
EPS = 1e-9


def check(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


def refuses(fn, *a, **k):
    try:
        fn(*a, **k)
    except rc.Refused:
        return True
    return False


def near(a, b, tol=EPS):
    return a is not None and b is not None and abs(a - b) < tol


ORDER = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
ORDER_FLAT = re.sub(r"\s+", " ", ORDER).lower()
README = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
SRC = open(os.path.join(HERE, "rule_coherence.py")).read()

# 1. the delivery
check("order names the four branches",
      all(t in ORDER_FLAT for t in ("tracks incoherence", "tracks restrictiveness",
                                    "tracks both", "separates neither")))
check("order says restrictiveness must be measured not matched by eye",
      "must be measured, not matched by eye" in ORDER_FLAT)
check("order carries the DEF worked case", "def" in ORDER_FLAT and "-50" in ORDER)
check("order says the three arms are run separately",
      "run them separately" in ORDER_FLAT)

# 2. restrictiveness (RCC_001)
check("restrictiveness half", near(rc.restrictiveness(5, 10), 0.5))
check("restrictiveness none space -> None", rc.restrictiveness(5, 0) is None)
check("restrictiveness zero permitted -> 1.0", near(rc.restrictiveness(0, 10), 1.0))
check("permitted > space is refused", refuses(rc.restrictiveness, 11, 10))

# 3. A1 score and void (RCC_002)
a, b, _ = rc.world("unmatched")
v = rc.a1_score(a, b)
check("a mismatched pair is VOID", v["verdict"] == "VOID_RESTRICTIVENESS_UNMATCHED")
check("the void carries the gap and the tol", near(v["gap"], 0.30) and near(v["tol"], rc.TOL))
am, bm, _ = rc.world("incoherence")
vm = rc.a1_score(am, bm)
check("a matched pair scores", vm["verdict"] == "SCORED")
check("the contrast is rate_a - rate_b", near(vm["incoherence_contrast"], vm["rate_a"] - vm["rate_b"]))
check("a1_score refuses an arm with no restrictiveness",
      refuses(rc.a1_score, {"restrictiveness": None, "events": [1]}, bm))

# 4. the four branches all reachable (RCC_003)
got = {}
for kind in ("incoherence", "restrictiveness", "both", "neither"):
    a, b, series = rc.world(kind)
    got[kind] = rc.a1_classify((a, b), series)["branch"]
check("world 'incoherence' -> TRACKS_INCOHERENCE", got["incoherence"] == "TRACKS_INCOHERENCE", got["incoherence"])
check("world 'restrictiveness' -> TRACKS_RESTRICTIVENESS", got["restrictiveness"] == "TRACKS_RESTRICTIVENESS", got["restrictiveness"])
check("world 'both' -> TRACKS_BOTH", got["both"] == "TRACKS_BOTH", got["both"])
check("world 'neither' -> SEPARATES_NEITHER", got["neither"] == "SEPARATES_NEITHER", got["neither"])
check("all four branches distinct on the four worlds", len(set(got.values())) == 4)

# 5. the permutation null fires and is not constant (RCC_004)
a, b, series = rc.world("incoherence")
r = rc.a1_classify((a, b), series)
check("incoherence contrast clears the null (p < 0.05)", r["incoherence_p"] < 0.05)
a, b, series = rc.world("neither")
r = rc.a1_classify((a, b), series)
check("a null contrast does NOT clear (p >= 0.05)", r["incoherence_p"] >= 0.05)

# 6. the 4-level power finding (RCC_005): a 4-point restrictiveness series
# cannot clear the two-sided permutation null, an 8-point one can
strong4 = [{"restrictiveness": x, "events": [1] * int(round((0.1 + 0.7 * x) * 400))
            + [0] * (400 - int(round((0.1 + 0.7 * x) * 400)))}
           for x in (0.2, 0.4, 0.6, 0.8)]
real4, slope4 = rc._restr_slope_real(strong4)
strong8 = [{"restrictiveness": x, "events": [1] * int(round((0.1 + 0.7 * x) * 400))
            + [0] * (400 - int(round((0.1 + 0.7 * x) * 400)))}
           for x in (0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85)]
real8, slope8 = rc._restr_slope_real(strong8)
check("a strong 4-level series does NOT clear the two-sided null", not real4)
check("the same strength at 8 levels does clear it", real8)
check("both carry a real positive slope", slope4 > 0 and slope8 > 0)
two, _ = rc._restr_slope_real(strong4[:2])
check("fewer than three levels is not estimable (real False, slope None)",
      rc._restr_slope_real(strong4[:2]) == (False, None))

# 7. A2b (RCC_006)
au = rc.a2b_audit(rc.a2b_records())
check("A2b: 2 condition-bearing, 5 act-only", au["condition_bearing"] == 2 and au["act_only"] == 5)
check("A2b: a coded-empty field is act-only but counted apart", au["coded_empty"] == 2)
check("A2b: act-only dominates on the constructed set", au["verdict"] == "act-only dominates")
check("A2b: a record with no act is refused", refuses(rc.a2b_audit, [{"condition": "x"}]))
check("A2b: condition-bearing-dominates branch reachable",
      rc.a2b_audit([{"act": "a", "condition": "c"}] * 3 + [{"act": "b"}])["verdict"].startswith("condition-bearing"))
check("A2b: share is None on empty", rc.a2b_audit([])["condition_share"] is None)

# 8. A3 (RCC_007)
e = rc.a3_effect(rc.a3_runs())
check("A3: plain reasoning share 12/18", near(e["plain_reasoning_share"], 12 / 18))
check("A3: labelled reasoning share 3/18", near(e["labelled_reasoning_share"], 3 / 18))
check("A3: label cost is the drop", near(e["label_cost"], 12 / 18 - 3 / 18))
check("A3: NOT_EVALUABLE on a run with neither response", rc.a3_read({"response": None}) == "NOT_EVALUABLE")
check("A3: behaviour -> conformity", rc.a3_read({"response": "behaviour"}) == "CONFORMITY_TRANSFER")
check("A3: principle -> reasoning", rc.a3_read({"response": "principle"}) == "REASONING_TRANSFER")
check("A3: NOT_EVALUABLE is excluded from the denominator, not counted as behaviour",
      rc.a3_effect([{"labelled": False, "response": "principle"}, {"labelled": False, "response": None}])["plain_reasoning_share"] == 1.0)
check("A3: all-unevaluable -> None share", rc.a3_effect([{"labelled": False, "response": None}])["plain_reasoning_share"] is None)

# 9. renders, choices, hygiene
text = rc.render()
check("render screens clean through no_severity, no exemption",
      no_severity.hits(text) == [], str(no_severity.hits(text)[:3]))
check("screen fires on a planted word", no_severity.hits(text + "\nthis is wrong\n") != [])
declared = set(rc.CHOICES)
cited = set()
for m in re.findall(r"\[CHOICE ([\d\-,]+)\]", SRC):
    if "-" in m:
        lo, hi = m.split("-"); cited |= set(range(int(lo), int(hi) + 1))
    else:
        cited |= set(int(x) for x in m.split(","))
check("every declared choice is cited", declared <= cited, str(declared - cited))
check("every cited choice is declared", cited <= declared, str(cited - declared))
check("module is ASCII", all(ord(c) < 128 for c in SRC))
check("README carries no author or working-style section",
      not re.search(r"^#+ .*(author|working style)", README, re.I | re.M))
check("README marks the data CONSTRUCTED", "CONSTRUCTED" in README)
rc_exit = subprocess.run([sys.executable, os.path.join(HERE, "rule_coherence.py"),
                          "--selftest"], capture_output=True).returncode
check("module refuses --selftest (exit 2)", rc_exit == 2)

failed = [c for c in CHECKS if not c[1]]
for name, ok, detail in CHECKS:
    print("%-5s %s%s" % ("ok" if ok else "FAIL", name, ("  [%s]" % detail) if (detail and not ok) else ""))
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
