#!/usr/bin/env python3
"""selftest for null_calibration.py. CC0. Needs numpy (via null-harness). Prints checks: N failed: M."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import null_calibration as nc  # noqa: E402
ok = total = 0
def check(c, lab):
    global ok, total
    total += 1; ok += bool(c)
    if not c: print("FAIL:", lab)
rows, forced, denom = nc.confusion(n=40)
check(set(nc.SOURCES) <= set(rows) and "UNRESOLVED" in rows, "one control per candidate plus UNRESOLVED")
check(all(rows[s]["counts"].get(s, 0) == 40 for s in nc.SOURCES), "planted, checked sources are recovered")
check(forced == 0 and denom == 40 * 8, "no forced attribution on NONE-correct controls")
check(rows["sensor_collision"]["counts"].get("NONE", 0) == 40, "two OBSERVED on one hop do not separate")
check(rows["NETWORK_LAG/measurement_only"]["counts"].get("NONE", 0) == 40, "measurement-only source is missed (cost of gating, kept)")
check(nc.missed(rows) == 40, "missed count is exactly the measurement_only row")
# Note 2026-11-09 (FINDER ROUND 3): the miss now keeps NETWORK_LAG in the candidate set.
check(rows["NETWORK_LAG/measurement_only"]["retained_in_set"] == 40, "missed source retained in candidate set")
g = nc.gates(n=40)
check(all(v["verdict"] == "OK" for v in g.values()), "every per-candidate gate reads OK in null_harness terms")
# the calibration can fail: a constant verdict reads CONSTANT in null_harness terms
import null_harness as nh
r = nh.bake_off(lambda d: True, nc.gen("UNRESOLVED"), nc.gen("NETWORK_LAG"), n_draws=20)
check(r["verdict"].startswith("CONSTANT_FIRES"), "a constant-yes gate is caught by the same harness")
saved = nc.verdict
nc.verdict = lambda d: "NETWORK_LAG"
rows2, forced2, _ = nc.confusion(n=10)
nc.verdict = saved
check(forced2 == 10 * 8, "a classifier that always assigns a source shows forced attribution 1.0")
r = subprocess.run([sys.executable, os.path.join(HERE, "null_calibration.py"), "--selftest"], capture_output=True, text=True)
check(r.returncode == 2, "module refuses --selftest")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
