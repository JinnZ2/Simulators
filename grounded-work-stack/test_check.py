#!/usr/bin/env python3
"""Checks on check.py. CC0, stdlib only. Run: python3 test_check.py"""
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import check  # noqa: E402
import no_severity  # noqa: E402

REPORT_SHA = "20aa9079590f3870e6644eee758e7a87e69b5d783b8437adb824a1a615be6bcc"
FIG_SHA = {
    "fig1_framework.png": "711d21459d8f1fcf11a7f9f5ca55a7750f0ab9ce253f0dbe26ea70227a4b303f",
    "fig2_presignal_funnel.png": "aae7fe3c07f5e0ad02446d21a4d831387c77f79d9e42a6715e5ebeb60babb004",
    "fig3_handoff_evidence.png": "a1c2830ff850b60ec47e220b98eddd2ecec523d15b9ad39c7ce4b3f24396bf5e",
    "fig4_work_about_work.png": "cb3e343d6e4f7c77d7491cecc47185ba66c2c6a737501882c89e443ca32e921d",
}

passed = failed = 0


def ok(cond, name):
    global passed, failed
    if cond:
        passed += 1
    else:
        failed += 1
        print("FAIL", name)


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


# 1. the landed files are byte-identical to the delivery
ok(sha(check.REPORT) == REPORT_SHA, "REPORT.md is the delivered bytes")
for name, h in FIG_SHA.items():
    ok(sha(os.path.join(HERE, "figs", name)) == h, "fig delivered bytes: " + name)

# 2. the readings on the delivered report
text = check.report_text()
rows = {r["id"]: r for r in check.run(text)}
want = {"GWS_001": "HOLDS", "GWS_002": "HOLDS", "GWS_003": "HOLDS",
        "GWS_004": "CONDITIONAL", "GWS_005": "TENSION", "GWS_006": "TENSION",
        "GWS_007": "READING", "GWS_008": "TENSION", "GWS_009": "HOLDS",
        "GWS_010": "UNVERIFIED", "GWS_011": "RESOLVES"}
for k, v in want.items():
    ok(rows[k]["status"] == v, "%s is %s" % (k, v))
ok("200 working days" in rows["GWS_004"]["evidence"], "workweeks need 200 days")
ok("11.25 weeks" in rows["GWS_004"]["evidence"], "250-day year gives 11.25 weeks")
ok("3 sites" in rows["GWS_005"]["evidence"], "90-96% stated at 3 sites")
ok("2 are working rows" in rows["GWS_008"]["evidence"], "2 of the 4 named are working rows")
ok("79 distinct URLs over 64 hosts" in rows["GWS_010"]["evidence"], "citation count")

# 3. the checks can return their other verdict (not constant)
try:
    check.g001_lbf(text.replace("factor of **4.45**", "factor of **4.4**"))
    ok(False, "missing quote raises")
except LookupError:
    ok(True, "missing quote raises")
t2 = text.replace("roughly 27% on skilled work", "roughly 30% on skilled work")
ok(check.g002_asana(t2)["status"] == "DIVERGES", "asana shares can diverge")
t3 = text.replace("the 96% overridden alert", "the overridden alert")
try:
    check.g006_override_reading(t3)
    ok(False, "g006 needs its quote")
except LookupError:
    ok(True, "g006 needs its quote")
saved = check.CROSS_MAP
check.CROSS_MAP = saved + [("x", "no/such/path.py", "planted")]
ok(check.g011_cross_map(text)["status"] == "MISSING", "absent cross-map path reads MISSING")
check.CROSS_MAP = saved
ok(check.g009_ipass(text.replace("10,740", "10,000"))["status"] == "DIVERGES",
   "I-PASS count can diverge")

# 4. the hand transcription stays a declared hand transcription
ok("hand transcription" in check.render(check.run(text)), "render declares transcription")
ok(check.FIG3_META_RANGE == (49.0, 96.0), "meta-range transcribed")

# 5. the render screens clean through no_severity, and the screen can fire
# one declared exemption: "alert(s)" is the report's own subject (medication
# alerts), quoted in GWS_006. Three arms: masked clean, unmasked only the
# exempt token fires, a plant is still caught through the exemption.
EXEMPT = {"alert", "alerts"}
out = check.render(check.run(text))
raw = no_severity.hits(out)
ok([h for h in raw if h[1] not in EXEMPT] == [], "render screens clean with exemption")
ok({h[1] for h in raw} <= EXEMPT, "only the exempt token fires unmasked")
ok([h for h in no_severity.hits(out + "\nthis is wrong") if h[1] not in EXEMPT] != [],
   "plant caught through the exemption")
ok(len(EXEMPT) == 2, "exemption stays two spellings of one token")

# 6. --selftest refuses rather than exiting clean
p = subprocess.run([sys.executable, os.path.join(HERE, "check.py"), "--selftest"],
                   capture_output=True, text=True)
ok(p.returncode == 2 and "test_check.py" in p.stderr, "--selftest refuses, names the test file")

print("checks: %d   failed: %d" % (passed + failed, failed))
sys.exit(1 if failed else 0)
