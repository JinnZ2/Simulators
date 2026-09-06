# SPDX-License-Identifier: CC0-1.0
"""
Checks for the routing data-layer marker, on CONSTRUCTED data. No DOT feed,
dock-geometry dataset, or routing output is read (all egress-blocked); every
series is built by hand with a known answer, and every failure-class instance
is carried from the marker, not verified. Nothing is a result.

    python3 routing-data-layer/selftest_rdl.py

Prints `selftest: N checks, M failed` and exits non-zero on any failure.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import envelope as ev             # noqa: E402
import rate_form as rf            # noqa: E402
import upstream as up             # noqa: E402
import known_answer as ka         # noqa: E402

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
print("known-answer gate (sustained_excess):")
ka.seed()
rows = {r["case"]: r["status"] for r in ka.run(
    "routing-data-layer/rate_form.py::sustained_excess")}
ok(rows.get("all excess") == ka.PASS, "known-answer: all excess -> 1")
ok(rows.get("never excess") == ka.PASS, "known-answer: never excess -> 0")
ok(rows.get("alternating") == ka.PASS, "known-answer: alternating -> 0.5")

# --------------------------------------------------------------------------
print("envelope -- required contents and the two structural absences:")
ok(len(ev.REQUIRED) == 10, "ten required contents (R1-R10)")
for r in ev.REQUIRED:
    ev.validate_required(r)
ok(ev.never_created() == ("R8", "R9"),
   "R8 (dock geometry) and R9 (update latency) are NEVER_CREATED")
ok(all(r.record_state == ev.INCOMPLETE for r in ev.REQUIRED
       if r.rid not in ("R8", "R9")),
   "R1-R7 and R10 are INCOMPLETE (a reporting chain exists)")
raises(ev.BadRecordState,
       lambda: ev.validate_required(ev.Required("RX", "x", "MADE_UP")),
       "an unknown record_state is refused")

print("envelope -- the claim table, each claim carrying a refutation:")
ok(len(ev.CLAIMS) == 7, "seven claims RDL-1..RDL-7")
for c in ev.CLAIMS:
    ev.validate_claim(c)
    ok(c.falsifiable(), "%s carries a refutation condition" % c.cid)
raises(ev.IncompleteClaim,
       lambda: ev.validate_claim(ev.Claim("RDL-X", "a claim", "")),
       "a claim with no refutation condition is refused (a position, not a "
       "claim)")
ok(len(ev.FAILURE_CLASSES) == 7 and ev.FAILURE_CLASSES[5].fid == "F6",
   "seven failure classes, F6 the load-bearing one, instances carried")

# --------------------------------------------------------------------------
print("rate form -- dE/dt vs dM/dt, STRUCTURAL vs MATURITY_GAP:")
struct_E = [2.0] * 10
struct_M = [1.0] * 10
ok(rf.rate_verdict(struct_E, struct_M) == rf.STRUCTURAL,
   "dE outruns dM sustained -> STRUCTURAL (the null is a different answer)")
ok(rf.rate_verdict([1.0] * 10, [2.0] * 10) == rf.MATURITY_GAP,
   "dM keeps up -> MATURITY_GAP (not yet)")
mixed_E = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
mixed_M = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2]
ok(rf.rate_verdict(mixed_E, mixed_M) == rf.UNDETERMINED,
   "excess near half -> UNDETERMINED, not forced to a verdict")
ok(abs(rf.sustained_excess(struct_E, struct_M) - 1.0) < 1e-9,
   "sustained_excess is 1.0 when dE always exceeds dM")

print("rate form -- RDL-5, a one-time survey does not hold, standing does:")
dE = [0.05] * 12       # 5% of records go stale per month over a season
one_time = rf.survey_decay(dE, refresh_interval=0)
standing = rf.survey_decay(dE, refresh_interval=3)
ok(not one_time["held"] and one_time["final_accuracy"] < rf.ACCURACY_FLOOR,
   "a one-time survey falls below the floor within one cycle (does not hold)")
ok(standing["held"],
   "a standing (refreshed) survey holds accuracy across the cycle -- the "
   "cost is standing, not capital")

# --------------------------------------------------------------------------
print("upstream -- F6, both wrong => upstream, not a single-vendor fix:")
ok(up.upstream_verdict(10.0, 12.0, 8.0) == up.UPSTREAM_INCOMPLETE,
   "both wrong in different directions -> UPSTREAM_INCOMPLETE (F6 signature)")
ok(up.upstream_verdict(10.0, 12.0, 13.0) == up.SHARED_BIAS,
   "both wrong same direction -> SHARED_BIAS (also upstream)")
ok(up.upstream_verdict(10.0, 12.0, 10.0) == up.VENDOR_DEFECT,
   "one right, one wrong -> VENDOR_DEFECT")
ok(up.upstream_verdict(10.0, 10.0, 10.0) == up.BOTH_CORRECT,
   "both correct -> BOTH_CORRECT")
ok(not up.single_vendor_fix_closes(up.UPSTREAM_INCOMPLETE),
   "a single-vendor fix does NOT close the F6 upstream pattern (RDL-2)")
ok(not up.single_vendor_fix_closes(up.SHARED_BIAS),
   "a single-vendor fix does not close a shared upstream bias either")
ok(up.single_vendor_fix_closes(up.VENDOR_DEFECT),
   "a lone vendor defect IS closable by that vendor")

# --------------------------------------------------------------------------
print("selftest: %d checks, %d failed" % (_checks, _failed))
sys.exit(1 if _failed else 0)
