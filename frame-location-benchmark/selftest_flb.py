# SPDX-License-Identifier: CC0-1.0
"""
Selftest for the frame-location benchmark instruments (score.py,
validate_cases.py). Null tests run both directions:

  - the scorer's false_positive_rate is 0.0 on a perfect run, 1.0 on an
    all-MIS-caller (catches N1), 0.5 on half;
  - a MIS case called MIS with the wrong target scores target_miss_named,
    NEVER target_hit (the headline);
  - a malformed header is MALFORMED, not wrong;
  - the contamination check passes on the frozen harness and FIRES on a
    planted fault_target leak and on a planted (class,domain) collision;
  - each R1/R2/R3 validator PASSES on the shipped set and FIRES on a
    planted-bad set;
  - the section-9 split computes an excluded headline when a non-
    constructed case is present.

Run:  python3 frame-location-benchmark/selftest_flb.py
"""

import copy
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import score            # noqa: E402
import validate_cases as vc   # noqa: E402

_checks = 0
_failed = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


# ---- false_positive_rate known answers (also in tools/known_answer.py) ----

perfect = [("WELL", "WELL"), ("WELL", "WELL"), ("MIS", "MIS"), ("MIS", "MIS")]
all_mis = [("WELL", "MIS"), ("WELL", "MIS"), ("MIS", "MIS")]
half = [("WELL", "WELL"), ("WELL", "MIS")]
check(score.false_positive_rate(perfect) == 0.0, "FP rate perfect == 0.0")
check(score.false_positive_rate(all_mis) == 1.0, "FP rate all-MIS == 1.0")
check(score.false_positive_rate(half) == 0.5, "FP rate half == 0.5")
check(score.false_positive_rate([("MIS", "MIS")]) is None,
      "FP rate with no WELL is None, not 0 (absent vs known-negative)")

# ---- parse_header ---------------------------------------------------------

p, t, mal = score.parse_header("POSED: MIS\nTARGET: population\nanswer")
check((p, t, mal) == ("MIS", "population", False), "parse MIS header")
p, t, mal = score.parse_header("POSED: WELL\nTARGET: NONE\n200")
check((p, mal) == ("WELL", False), "parse WELL header")
_, _, mal = score.parse_header("the answer is 5")
check(mal is True, "no header -> malformed")
_, _, mal = score.parse_header("POSED: MAYBE\nTARGET: x")
check(mal is True, "invalid POSED value -> malformed")
_, _, mal = score.parse_header("POSED: MIS\nno target line here")
check(mal is True, "missing TARGET line -> malformed")

# ---- target_hit -----------------------------------------------------------

case = {"fault_target": "population base (per-capita rate)",
        "accept": ["population", "denominator", "per-capita"]}
check(score.target_hit(case, "the population base") is True, "target hit")
check(score.target_hit(case, "the two raw numbers") is False, "target miss")
check(score.target_hit(case, "") is False, "empty target is not a hit")

# ---- score_one: the SCORING RULE, MALFORMED, FP ---------------------------

cases = {
    "M1": {"id": "M1", "posed": "MIS", "fault_class": "MISSING_DENOMINATOR",
           "domain": "epi", "fault_target": "population", "accept": ["population"],
           "source": "constructed"},
    "M2": {"id": "M2", "posed": "MIS", "fault_class": "MISSING_DENOMINATOR",
           "domain": "epi", "fault_target": "population", "accept": ["population"],
           "source": "constructed"},
    "W1": {"id": "W1", "posed": "WELL", "fault_class": None, "domain": "epi",
           "fault_target": None, "accept": [], "source": "constructed"},
}

# perfect run
resp_perfect = {"M1": "POSED: MIS\nTARGET: population\nx",
                "M2": "POSED: MIS\nTARGET: population\nx",
                "W1": "POSED: WELL\nTARGET: NONE\nx"}
r = score.score_one(cases, resp_perfect)
check(r["target_hit"] == 2 and r["target_hit_rate"] == 1.0, "perfect target_hit")
check(r["false_positive_rate"] == 0.0, "perfect FP 0")
check(r["target_miss_named"] == 0, "perfect no miss_named")

# MIS called MIS but wrong target -> target_miss_named, NOT headline
resp_missnamed = {"M1": "POSED: MIS\nTARGET: the raw counts\nx",
                  "M2": "POSED: MIS\nTARGET: the raw counts\nx",
                  "W1": "POSED: WELL\nTARGET: NONE\nx"}
r = score.score_one(cases, resp_missnamed)
check(r["target_hit"] == 0 and r["target_hit_rate"] == 0.0,
      "miss-named does not count as target_hit (headline)")
check(r["target_miss_named"] == 2, "miss-named recorded apart")
check(r["posed_accuracy"] == 1.0, "posed_accuracy still 1.0 (MIS called MIS)")

# all-MIS-caller -> FP 1.0 (catches N1)
resp_allmis = {"M1": "POSED: MIS\nTARGET: population\nx",
               "M2": "POSED: MIS\nTARGET: population\nx",
               "W1": "POSED: MIS\nTARGET: something\nx"}
r = score.score_one(cases, resp_allmis)
check(r["false_positive_rate"] == 1.0, "all-MIS-caller FP 1.0")

# malformed is separate, not wrong
resp_mal = {"M1": "no header at all\nblah",
            "M2": "POSED: MIS\nTARGET: population\nx",
            "W1": "POSED: WELL\nTARGET: NONE\nx"}
r = score.score_one(cases, resp_mal)
check(r["malformed"] == 1, "malformed counted")
check(r["non_malformed"] == 2, "malformed excluded from non_malformed")
check(r["target_hit"] == 1, "malformed MIS not scored as wrong or hit")

# section-9 split: a non-constructed MIS flows into the excluded headline
cases2 = copy.deepcopy(cases)
cases2["M2"]["source"] = "field"
r = score.score_one(cases2, resp_perfect)
check(r["mis_nonconstructed"] == 1, "one non-constructed MIS")
check(r["headline_excluded_constructed"] == 1.0,
      "excluded headline computed over the non-constructed MIS")

# ---- null_flags: N1 (FP high every arm), N3 (arm4 < arm0) -----------------

# N1: both arms all-MIS-callers
res = {("arm0_cold", "M"): score.score_one(cases, resp_allmis),
       ("arm4_full", "M"): score.score_one(cases, resp_allmis)}
flags = score.null_flags(res)
check(any("N1" in f for f in flags), "N1 fires when FP high in every arm")

# N3: arm4 underperforms arm0
res = {("arm0_cold", "M"): score.score_one(cases, resp_perfect),
       ("arm4_full", "M"): score.score_one(cases, resp_missnamed)}
flags = score.null_flags(res)
check(any("N3" in f for f in flags), "N3 fires when arm4 < arm0")

# N1 does NOT fire when one arm is clean
res = {("arm0_cold", "M"): score.score_one(cases, resp_allmis),
       ("arm4_full", "M"): score.score_one(cases, resp_perfect)}
flags = score.null_flags(res)
check(not any("N1" in f for f in flags),
      "N1 does not fire when an arm has low FP")

# ---- validate_cases: real set passes -------------------------------------

ok, msgs = vc.validate(os.path.join(_HERE, "cases.jsonl"),
                       os.path.join(_HERE, "harness"))
check(ok, "shipped cases + harness validate: %r" % msgs)

real_cases = vc.load_cases(os.path.join(_HERE, "cases.jsonl"))
harness = vc.load_harness(os.path.join(_HERE, "harness"))
arm3 = harness["arm3_corrections.txt"]
corr = vc.parse_corrections(arm3)
check(len(corr) == 7, "7 ARM 3 corrections parsed")

# contamination FIRES on a planted fault_target leak
bad_harness = dict(harness)
leak_target = real_cases[0]["fault_target"] if real_cases[0]["posed"] == "MIS" \
    else next(c["fault_target"] for c in real_cases if c["posed"] == "MIS")
bad_harness["arm2_positions.txt"] = harness["arm2_positions.txt"] + \
    "\n" + leak_target + "\n"
m = vc.check_contamination(real_cases, bad_harness, corr)
check(any("CONTAMINATION" in x for x in m),
      "planted fault_target leak fires contamination")

# clean harness does not fire
m = vc.check_contamination(real_cases, harness, corr)
check(not any("CONTAMINATION" in x for x in m),
      "frozen harness has no contamination")

# planted (class,domain) collision fires
mis0 = next(c for c in real_cases if c["posed"] == "MIS")
bad_corr = set(corr) | {(mis0["fault_class"], mis0["domain"])}
m = vc.check_contamination(real_cases, harness, bad_corr)
check(any("same-(class,domain)" in x for x in m),
      "planted (class,domain) collision fires")

# ---- validate_cases: R-checks fire on planted-bad sets --------------------

# R1: too few WELL
few_well = [c for c in real_cases if c["posed"] == "MIS"][:10] + \
           [c for c in real_cases if c["posed"] == "WELL"][:1]
check(vc.check_R1(few_well), "R1 fires when WELL share < 40%")
check(not vc.check_R1(real_cases), "R1 passes on the shipped set")

# R2: one class dominates
lopsided = [c for c in real_cases if c["posed"] == "MIS"
            and c["fault_class"] == "WRONG_INSTRUMENT"] + \
           [c for c in real_cases if c["posed"] == "MIS"
            and c["fault_class"] == "ACCEPTED_SIDE"][:1]
check(vc.check_R2(lopsided), "R2 fires when a class > 25% of MIS")
check(not vc.check_R2(real_cases), "R2 passes on the shipped set")

# R3: fewer than 3 domains
one_dom = [dict(c, domain="hydrology") for c in real_cases]
check(vc.check_R3(one_dom), "R3 fires with < 3 domains / no transfer")
check(not vc.check_R3(real_cases), "R3 passes on the shipped set")

# R6: a prompt with a hint marker
hinted = [dict(real_cases[0], prompt="Is this the right question to ask?")]
check(vc.check_R6(hinted), "R6 fires on a hint marker")
check(not vc.check_R6(real_cases), "R6 passes on the shipped set")

# ---- score.py refuses --selftest ------------------------------------------

rc = subprocess.call([sys.executable, os.path.join(_HERE, "score.py"),
                      "--selftest"], stderr=subprocess.DEVNULL)
check(rc == 2, "score.py --selftest exits 2")

# ---- report ---------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
