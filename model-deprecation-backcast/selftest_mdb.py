# SPDX-License-Identifier: CC0-1.0
"""
Checks for the Model Deprecation Backcast Instrument, on CONSTRUCTED data.
No vendor calendar, poll, eval, or dataset is read (all egress-blocked);
every series is built by hand with a known answer. Nothing is a result.

    python3 model-deprecation-backcast/selftest_mdb.py

Prints `selftest: N checks, M failed` and exits non-zero on any failure.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import instrument as ins           # noqa: E402
import null_check as nc            # noqa: E402
import guardrail_clock as gc       # noqa: E402
import known_answer as ka          # noqa: E402

_checks = 0
_failed = 0


def ok(cond, label):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        print("  FAIL: %s" % label)


def raises(exc, fn, label):
    global _checks, _failed
    _checks += 1
    try:
        fn()
    except exc:
        return
    except Exception as ex:          # noqa: BLE001
        _failed += 1
        print("  FAIL: %s (raised %s)" % (label, type(ex).__name__))
        return
    _failed += 1
    print("  FAIL: %s (did not raise)" % label)


# --------------------------------------------------------------------------
print("known-answer gate (lag_of_peak):")
ka.seed()
rows = {r["case"]: r["status"] for r in ka.run(
    "model-deprecation-backcast/null_check.py::lag_of_peak")}
ok(rows.get("planted lag 20") == ka.PASS, "known-answer: planted lag 20")
ok(rows.get("planted lag 5") == ka.PASS, "known-answer: planted lag 5")
ok(rows.get("flat -- no peak") == ka.PASS, "known-answer: flat -> None")

# --------------------------------------------------------------------------
print("instrument -- seven columns, each carrying a NULL (required):")
ok(len(ins.COLUMNS) == 7, "seven columns")
for c in ins.COLUMNS:
    ins.validate_column(c)
    ok(c.complete(), "%s carries measures + test + null" % c.cid)
raises(ins.IncompleteColumn,
       lambda: ins.validate_column(ins.Column("CX", "n", "m", "re", "ra",
                                              "t", "")),
       "a column with no null is refused (must not be cited)")
raises(ins.IncompleteColumn,
       lambda: ins.validate_column(ins.Column("CX", "n", "", "re", "ra",
                                              "t", "null")),
       "a column with no 'measures' is refused")
coll = ins.collapses()
ok(coll.get("C1") == "C2" and coll.get("C7") == "C4",
   "the nulls' stated collapses are recorded (C1->C2, C7->C4)")
ok(ins.GUARDRAIL_CLOCK.clock.startswith("news-time") and
   "contaminate" in ins.GUARDRAIL_CLOCK.warning,
   "the guardrail clock is a separate layer with the contamination warning")
ok(not ins.OPEN_NODE.named and not ins.OPEN_NODE.graded and ins.OPEN_NODE.held,
   "the OPEN node is held, un-named, un-graded")
ok(ins.SAMPLING_ABSENCE.verification.startswith("CARRIED"),
   "the sampling absence is carried, not verified")

# --------------------------------------------------------------------------
print("C6 -- the fad-axis lag, null-tested both directions:")
x = gc._discourse_series(72)
lags = list(range(0, 31))
inband = [x[t - 20] if t - 20 >= 0 else 0.0 for t in range(72)]
outband = [x[t - 8] if t - 8 >= 0 else 0.0 for t in range(72)]
ok(nc.c6_fad_driving(x, inband, lags) == nc.DRIVING,
   "a discard series lagged 20 mo behind discourse -> DRIVING (in band)")
ok(nc.c6_fad_driving(x, outband, lags) == nc.DRIVING_OTHER_LAG,
   "a lag outside 18-24 mo -> DRIVING_OTHER_LAG (funding layer, not the fad)")
ok(nc.c6_fad_driving(x, [1.0] * 72, lags) == nc.NOT_DRIVING,
   "uniform discards -> NOT_DRIVING (the C6 null)")

# --------------------------------------------------------------------------
print("guardrail clock -- contamination of the C6 lag:")
demo = gc.contamination_demo()
ok(demo["separated_lag"] == 20, "separated (discards only) recovers the true lag 20")
ok(demo["contaminated_lag"] != 20 and demo["contaminated"],
   "pooling the guardrail series flips the lag away from the true one")
ok(demo["separated_verdict"] == nc.DRIVING and
   demo["contaminated_verdict"] == nc.DRIVING_OTHER_LAG,
   "separated reads DRIVING (real, in band); contaminated misreads to the "
   "guardrail's news-time lag")

# --------------------------------------------------------------------------
print("C1/C2 collapse, C4, C5, C7->C4 -- null vs signal:")
ok(nc.c1c2_collapse([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == nc.COLLAPSE,
   "stated == measured across the series -> C1 and C2 COLLAPSE")
ok(nc.c1c2_collapse([1, 2, 3, 4, 5], [5, 1, 4, 2, 3]) == nc.TWO_COLUMNS,
   "stated diverges from measured -> TWO_COLUMNS")
ok(nc.c4_tightening([0.5, 0.5, 0.5, 0.5]) == nc.NO_TIGHTENING,
   "register invariant across versions -> NO_TIGHTENING (C4 measures nothing)")
ok(nc.c4_tightening([0.5, 0.6, 0.75, 0.9]) == nc.TIGHTENING,
   "register moves toward modal -> TIGHTENING")
dist = [0, 1, 2, 3, 4]
ok(nc.c5_tracks_coupling(dist, [1.0, 1.0, 1.0, 1.0, 1.0]) == nc.NOT_TRACKING,
   "routed-elsewhere ratio flat with distance -> NOT_TRACKING (C5 null)")
ok(nc.c5_tracks_coupling(dist, [0.1, 0.4, 0.7, 1.1, 1.5]) == nc.TRACKING,
   "ratio rises with distance from modal -> TRACKING")
ok(nc.c7_vs_c4(dist, [1.0, 1.0, 1.0, 1.0, 1.0]) == nc.COLLAPSE_INTO_C4,
   "per-turn cost flat with ontological distance -> C7 COLLAPSE_INTO_C4")
ok(nc.c7_vs_c4(dist, [0.2, 0.6, 1.0, 1.5, 2.0]) == nc.DISTINCT,
   "per-turn cost rises with ontological distance -> DISTINCT axis")

# --------------------------------------------------------------------------
print("C2 unrecoverable is a state, not an estimate:")
ok(nc.c2_recoverable(0.8) == nc.RECOVERABLE, "dense eval coverage -> RECOVERABLE")
ok(nc.c2_recoverable(0.1) == nc.UNRECOVERABLE,
   "sparse coverage -> UNRECOVERABLE (declared, not estimated)")

# --------------------------------------------------------------------------
print("C3 accepted-side censoring -- the bias is a number:")
exits = ([("complainer", True)] * 2 + [("complainer", False)] * 1 +
         [("jumper", False)] * 4 + [("paid_then_lapsed", True)] * 3)
c3 = nc.c3_censoring(exits)
ok(c3["total_affected"] == 10 and c3["recorded"] == 3,
   "3 of 10 discard-affected leave a record (complainer trace only)")
ok(abs(c3["recorded_fraction"] - 0.3) < 1e-9,
   "recorded fraction 0.3 -- the rest is censored, not absent")
ok(abs(c3["paying_tier_fraction_of_recorded"] - 2.0 / 3.0) < 1e-9,
   "the recorded signal carries a paying-tier filter (2/3 here)")

# --------------------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
