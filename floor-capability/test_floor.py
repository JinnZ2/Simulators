# SPDX-License-Identifier: CC0-1.0
"""Checks for floor_capability.py. Run: python3 floor-capability/test_floor.py

Prints every check and the count. Exit 0 only if all pass. Every record
scored here is CONSTRUCTED.
"""

import ast
import hashlib
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import floor_capability as fc  # noqa: E402

SRC = open(os.path.join(HERE, "floor_capability.py"), encoding="utf-8").read()
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


# -- 1. the draft is read, not retyped
print("-- the draft")
raw = open(fc.DRAFT, "rb").read()
check("DRAFT_V0.txt matches its pin", hashlib.sha256(raw).hexdigest() == fc.DRAFT_SHA256)
tmp = tempfile.mkdtemp()
try:
    bad = os.path.join(tmp, "DRAFT_V0.txt")
    open(bad, "wb").write(raw.replace(b"hidden_cost", b"hidden_kost"))
    check("a draft whose bytes moved is refused", raises(fc.DraftPinError, fc.read_draft, bad))
    planted = os.path.join(tmp, "planted.txt")
    open(planted, "wb").write(raw + b"\nscrap_weight = 0.3\n")
    dp = fc.read_draft(planted, pin=None)
    check("a planted numeric weight reads PRESENT (control)",
          fc.audit(dp)["weights_state"] == "PRESENT")
finally:
    shutil.rmtree(tmp)
d = fc.read_draft()
a = fc.audit(d)
check("six indicators", a["indicator_count"] == 6)
check("five hidden_cost terms, read from the AST",
      a["hidden_cost_terms"] == ["scrap", "machine_damage", "retraining", "hr_churn", "outsourced_repair"])
check("three gaps", len(a["gaps"]) == 3)
check("zero numeric constants in the draft", a["numeric_constants"] == 0)
check("the status line names weights", a["weights_named_in_status"] is True)
check("and the draft carries none: UNSTATED, not unrun", a["weights_state"] == "UNSTATED")
check("1 of 5 terms is named as an indicator", a["terms_named_as_indicator"] == ["scrap"])
check("retraining has no indicator", a["terms_with_no_indicator"] == ["retraining"])
check("0 of 5 terms bound to a cost unit", a["terms_bound_to_a_cost_unit"] == [])
check("three declared overlaps", len(a["overlaps"]) == 3)
check("every binding names a real indicator or None",
      all(b["indicator"] in (None,) + tuple(a["indicator_keys"])
          for b in fc.HIDDEN_TERM_BINDING.values()))
check("every overlap names two hidden_cost terms",
      all(x in a["hidden_cost_terms"] and y in a["hidden_cost_terms"] for x, y, _ in fc.OVERLAPS))
check("reclassify is code level, three codes", a["reclassify_level"] == "CODE"
      and len(a["reclassify_codes"]) == 3)
check("the draft's own gap names the event separation", a["gap_names_event_separation"])

# -- 2. scrap at event level
print("-- scrap")
codes = set(a["reclassify_codes"])
ev = {"code": "material_jam", "precursor": "PRESENT", "lead_time_s": 120, "check_interval_s": 60}
check("lead = margin x check is CATCHABLE", fc.classify_event(ev, codes) == "CATCHABLE")
check("one second short is FASTER_THAN_CHECK",
      fc.classify_event(dict(ev, lead_time_s=119), codes) == "FASTER_THAN_CHECK")
check("no precursor is EQUIPMENT_ONLY",
      fc.classify_event(dict(ev, precursor="ABSENT"), codes) == "EQUIPMENT_ONLY")
check("unknown precursor is UNDETERMINED",
      fc.classify_event(dict(ev, precursor="UNKNOWN"), codes) == "UNDETERMINED")
check("missing precursor field is UNDETERMINED, never ABSENT",
      fc.classify_event({"code": "material_jam"}, codes) == "UNDETERMINED")
check("missing interval is UNDETERMINED",
      fc.classify_event(dict(ev, check_interval_s=None), codes) == "UNDETERMINED")
check("unmapped code kept apart",
      fc.classify_event(dict(ev, code="operator_misload"), codes) == "UNMAPPED")
check("an invalid precursor value raises",
      raises(ValueError, fc.classify_event, dict(ev, precursor="yes"), codes))
rng = random.Random(11)
ok = True
for _ in range(200):
    evs = [{"code": rng.choice(["calibration_drift", "belt/drive_failure", "material_jam", "x"]),
            "precursor": rng.choice(fc.PRECURSOR),
            "lead_time_s": rng.choice([None, 10, 100, 1000]),
            "check_interval_s": rng.choice([None, 30, 300])} for _ in range(rng.randint(1, 30))]
    r = fc.scrap_readout(evs, codes)
    lo, hi = r["catchable_share_of_all"]
    ok = ok and lo <= hi <= r["code_level_share"] + 1e-12
check("event-level share never exceeds the code-level share (200 sets)", ok)
r0 = fc.scrap_readout([], codes)
check("no events: every share is None, not 0",
      r0["code_level_share"] is None and r0["catchable_share_of_all"] == (None, None))
check("catchable_share_low: empty mapped set is None",
      fc.catchable_share_low(["UNMAPPED", "UNMAPPED"]) is None)
check("catchable_share_low: 1 of 4",
      fc.catchable_share_low(["CATCHABLE", "EQUIPMENT_ONLY", "UNDETERMINED", "FASTER_THAN_CHECK", "UNMAPPED"]) == 0.25)
dr, er = fc.scrap_attribution(False), fc.scrap_attribution(True)
check("draft reading UNPARTITIONED", dr["verdict"] == "UNPARTITIONED")
check("event reading UNPARTITIONED, with a strictly smaller unmeasured set",
      er["verdict"] == "UNPARTITIONED" and set(er["unmeasured"]) < set(dr["unmeasured"]))

# -- 3. tenure x scrap
print("-- tenure test")
want = {"operator": "OPERATOR_CHANNEL", "assignment": "NOT_SEPARABLE", "null": "NO_EFFECT"}
hits = {}
for kind, v in want.items():
    hits[kind] = sum(fc.tenure_test(fc.tenure_world(kind, seed=s), seed=s)["verdict"] == v
                     for s in range(1, 11))
    print("      world %-10s %s in %d of 10 seeds" % (kind, v, hits[kind]))
check("operator world reads OPERATOR_CHANNEL in 10 of 10 seeds", hits["operator"] == 10)
check("assignment world reads NOT_SEPARABLE in >= 9 of 10 seeds", hits["assignment"] >= 9)
check("null world reads NO_EFFECT in >= 8 of 10 seeds", hits["null"] >= 8)
rev = [{"tenure_years": t, "catchable_rate": 1.0 + 0.3 * t + (0.01 * (t % 3)),
        "equipment_rate": 2.0 + 0.01 * (t % 2)} for t in range(1, 21)]
opp = [{"tenure_years": t, "catchable_rate": 6.0 - 0.2 * t + 0.01 * (t % 3),
        "equipment_rate": 1.0 + 0.1 * t + 0.01 * (t % 2)} for t in range(1, 21)]
ro = fc.tenure_test(opp)
check("control rising with tenure reads OPERATOR_CHANNEL, flagged as running against (FLC_017)",
      ro["verdict"] == "OPERATOR_CHANNEL" and ro["control_runs_against"] is True)
check("REVERSED is reachable", fc.tenure_test(rev)["verdict"] == "REVERSED")
check("three rows: NOT_EVALUABLE",
      fc.tenure_test(fc.tenure_world("null", n=3))["verdict"] == "NOT_EVALUABLE")
check("ols imported from sim-span, not copied",
      "from three_column import ols" in SRC and "def ols" not in SRC)

# -- 4. maintenance
print("-- maintenance")
check("TRANSFERRED", fc.task_class({"in_house": 8, "outsourced": 1}, {"in_house": 2, "outsourced": 7}) == "TRANSFERRED")
check("NEW_TASK", fc.task_class({"in_house": 0, "outsourced": 1}, {"in_house": 0, "outsourced": 5}) == "NEW_TASK")
check("CAPACITY", fc.task_class({"in_house": 8, "outsourced": 1}, {"in_house": 9, "outsourced": 5}) == "CAPACITY")
check("missing count UNDETERMINED", fc.task_class({"in_house": None, "outsourced": 1}, {"in_house": 2, "outsourced": 7}) == "UNDETERMINED")
check("outsourced flat UNDETERMINED", fc.task_class({"in_house": 8, "outsourced": 3}, {"in_house": 2, "outsourced": 3}) == "UNDETERMINED")
m = fc.maintenance_readout({"a": ({"in_house": 0, "outsourced": 2}, {"in_house": 0, "outsourced": 6}),
                            "b": ({"in_house": 10, "outsourced": 1}, {"in_house": 12, "outsourced": 4})})
b0, b1 = m["aggregate_outsourced_share"]
check("aggregate outsourced share rises with zero TRANSFERRED classes",
      b1 > b0 and m["per_class"]["TRANSFERRED"] == [])

# -- 5. life, handoff, screening, rule origin
print("-- life, handoff, screening, origin")
check("life_ratio 0.8", fc.life_ratio(8000, 10000, "OEM_RATED") == 0.8)
check("life_ratio undeclared basis None", fc.life_ratio(8000, 10000, None) is None)
check("life_ratio unknown basis None", fc.life_ratio(8000, 10000, "VENDOR_SAID") is None)
check("life_ratio zero expected None", fc.life_ratio(8000, 0, "PLANT_HISTORY") is None)
check("handoff 10 days overlap", fc.handoff_overlap(100, 91) == 10)
check("handoff back-to-back is 0", fc.handoff_overlap(100, 101) == 0)
check("handoff 5-day gap is -5", fc.handoff_overlap(100, 106) == -5)
check("handoff missing date None", fc.handoff_overlap(None, 5) is None)
hr = fc.handoff_readout([{"leaver_last_day": 1, "successor_first_day": 1},
                         {"leaver_last_day": 1, "successor_first_day": 2},
                         {"leaver_last_day": 1, "successor_first_day": 9},
                         {"leaver_last_day": 1, "successor_first_day": None, "no_successor": True},
                         {"leaver_last_day": 1, "successor_first_day": None}])
check("handoff: all five states reachable", all(v == 1 for v in hr.values()))
sc = fc.screening_share([{"screen": "NOT_RECORDED"}] * 3)
check("all NOT_RECORDED: tacit share None", sc["tacit_share"] is None and sc["counts"]["NOT_RECORDED"] == 3)
check("a missing screen field counts NOT_RECORDED", fc.screening_share([{}])["counts"]["NOT_RECORDED"] == 1)
check("an invalid screen raises", raises(ValueError, fc.screening_share, [{"screen": "GOOD"}]))
origins = {fc.rule_origin(r) for r in (
    {"post_incident": True, "floor_report": False}, {"post_incident": False, "floor_report": True},
    {"post_incident": True, "floor_report": True}, {"post_incident": False, "floor_report": False},
    {"post_incident": None, "floor_report": True})}
check("rule origin: five states reachable",
      origins == {"REACTIVE", "GENERATED", "BOTH", "NEITHER", "UNKNOWN"})

# -- 6. hidden cost
print("-- hidden cost")
rows = fc.cost_vector({})
check("cost_vector carries every draft term", [r["term"] for r in rows] == a["hidden_cost_terms"])
check("no sum key in the vector", all("sum" not in r for r in rows))
check("combine refuses unmeasured terms", raises(fc.ScalarRefused, fc.combine, rows))
full = {t: (1.0, "USD/yr") for t in a["hidden_cost_terms"]}
mixed = dict(full, scrap=(0.04, "fraction"))
check("combine refuses mixed units", raises(fc.ScalarRefused, fc.combine, fc.cost_vector(mixed)))
check("combine refuses open overlaps", raises(fc.ScalarRefused, fc.combine, fc.cost_vector(full)))
parts = {(x, y): "book to %s" % x for x, y, _ in fc.OVERLAPS}
check("with one unit and every overlap partitioned, a sum is reachable",
      fc.combine(fc.cost_vector(full), parts) == (5.0, "USD/yr"))

# -- 7. structure
print("-- structure")
tree = ast.parse(SRC)
argnames = [x.arg for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) for x in n.args.args]
keys = [k.value for n in ast.walk(tree) if isinstance(n, ast.Dict) for k in n.keys
        if isinstance(k, ast.Constant) and isinstance(k.value, str)]
pat = re.compile(r"countr|nation", re.I)
check("no function takes a country; no dict key names one",
      not any(pat.search(x) for x in argnames + keys))
plant = ast.parse("def f(country):\n    return {'nation': 1}\n")
pa = [x.arg for n in ast.walk(plant) if isinstance(n, ast.FunctionDef) for x in n.args.args]
check("the scan fires on a planted country argument", any(pat.search(x) for x in pa))
check("attribution imported from measurand-partition, not copied",
      "def attribution" not in SRC and "measurand-partition/common.py" in SRC)
for k in fc.CHOICES:
    tag = "[CHOICE %d" % k
    body = SRC.split("CHOICES = {", 1)[1].split("\n}\n", 1)[1]
    check("CHOICE %d is cited outside its declaration" % k, tag in body)
before = hashlib.sha256(open(fc.DRAFT, "rb").read()).hexdigest()
text = fc.render()
check("render leaves the draft unchanged",
      hashlib.sha256(open(fc.DRAFT, "rb").read()).hexdigest() == before)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import no_severity  # noqa: E402
check("render screens clean, no exemption", no_severity.check(text)[0])
p = subprocess.run([sys.executable, os.path.join(HERE, "floor_capability.py"), "--selftest"],
                   capture_output=True, text=True)
check("--selftest refuses with exit 2", p.returncode == 2)
named = re.search(r"([\w./-]+\.py)", p.stderr.split(":", 1)[1]).group(1)
check("and names a test file that exists from the repo root",
      os.path.isfile(os.path.join(ROOT, named)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import known_answer as ka  # noqa: E402
ka.seed()
ids = ka.registry_ids()
for m in ("life_ratio", "catchable_share_low", "handoff_overlap"):
    check("known-answer registers %s" % m, "floor-capability/floor_capability.py::" + m in ids)

for rel, marker in (("credential-channel/credential_channel.py", "def i1_route_correlation"),
                    ("readout-count/readout_count.py", "positions_returning")):
    path = os.path.join(ROOT, rel)
    check("cross-link %s resolves with marker %r" % (rel, marker),
          os.path.isfile(path) and marker in open(path, encoding="utf-8").read())

print("checks: %d   failed: %d" % (N["pass"] + N["fail"], N["fail"]))
sys.exit(1 if N["fail"] else 0)
