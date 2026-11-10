#!/usr/bin/env python3
"""Checks for decision.py (OSC-WO2). Stdlib only."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import decision as d  # noqa: E402
from barrier_per_bit import UndeclaredTerm  # noqa: E402

checks = []


def ok(name, cond):
    checks.append((name, bool(cond)))


def raises(exc, fn, **kw):
    try:
        fn(**kw)
    except exc:
        return True
    return False


S, P = d.lines(years=10, tau0=1e-9, population_value=60, basis="test")
ok("single-bit line ~40.3", 40 < S < 41)
ok("population line 60 as declared", P == 60)
ok("population without basis refused",
   raises(UndeclaredTerm, d.lines, years=10, tau0=1e-9, population_value=60, basis=None))
ok("population below single-bit line rejected",
   raises(ValueError, d.lines, years=10, tau0=1e-9, population_value=20, basis="x"))

R = lambda **kw: d.readout(single=S, pop=P, **kw)  # noqa: E731
ok("no inputs -> UNMEASURED", R()["state"] == "UNMEASURED")
ok("measured 75+/-5 -> ABOVE_POPULATION_LINE", R(measured=75, uncertainty=5)["state"] == "ABOVE_POPULATION_LINE")
ok("measured 50+/-3 -> BETWEEN_LINES", R(measured=50, uncertainty=3)["state"] == "BETWEEN_LINES")
ok("measured 30+/-4 -> BELOW_SINGLE_BIT_LINE", R(measured=30, uncertainty=4)["state"] == "BELOW_SINGLE_BIT_LINE")
r = R(measured=58, uncertainty=5)
ok("measured 58+/-5 -> STRADDLES, no route", r["state"] == "STRADDLES" and r["route"] is None
   and r["spans"] == ["ABOVE_POPULATION_LINE", "BETWEEN_LINES"])
ok("measured without uncertainty refused", raises(UndeclaredTerm, R, measured=70))
ok("coherent without discount refused", raises(UndeclaredTerm, R, coherent=1300))
ok("coherent with discount but no basis refused",
   raises(UndeclaredTerm, R, coherent=1300, discount_range=(30, 100)))
e = R(coherent=1300, discount_range=(10, 20), discount_basis="x")
ok("estimate is labelled ESTIMATED", e["source"] == "ESTIMATED" and e["state"] == "ABOVE_POPULATION_LINE")
e = R(coherent=1300, discount_range=(30, 100), discount_basis="x")
ok("report-like discount on 1300 straddles", e["state"] == "STRADDLES")
ok("discount below 1 rejected", raises(ValueError, R, coherent=100, discount_range=(0.5, 2), discount_basis="x"))
ok("exact line value 60 lands ABOVE (>=)", R(measured=60, uncertainty=0)["state"] == "ABOVE_POPULATION_LINE")
reached = {R(measured=m, uncertainty=u)["state"] for m, u in ((75, 5), (50, 3), (30, 4), (58, 5))} | {R()["state"]}
ok("every state reachable", reached == set(d.BANDS) | {"STRADDLES", "UNMEASURED"})
src = (HERE / "decision.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)

failed = [n for n, v in checks if not v]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
