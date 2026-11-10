#!/usr/bin/env python3
"""Checks for sharrock.py (OSC-WO3 helper). Stdlib only."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import sharrock as s  # noqa: E402
from barrier_per_bit import UndeclaredTerm  # noqa: E402

checks = []


def ok(n, c):
    checks.append((n, bool(c)))


for planted in (30.0, 50.0, 80.0):
    t, h = s.synthetic(planted, 1e9, hc0=2.5)
    ok(f"planted Delta {planted:g} recovered at the true f0", abs(s.fit_delta(t, h, f0=1e9) - planted) < 1e-9)
t, h = s.synthetic(50.0, 1e9)
ok("wrong f0 moves Delta (f0 enters the result)", abs(s.fit_delta(t, h, f0=1e10) - 50) > 1)
ok("higher assumed f0 gives higher Delta", s.fit_delta(t, h, f0=1e10) > s.fit_delta(t, h, f0=1e8))
lo, hi = s.delta_band(t, h, f0_range=(1e10, 1e9))
ok("band is ordered and brackets the truth from the low end", lo <= 50 + 1e-9 <= hi + 1e-9 and lo < hi)
try:
    s.fit_delta(t, h, f0=None)
    r = False
except UndeclaredTerm:
    r = True
ok("undeclared f0 refused", r)
try:
    s.fit_delta([1, 10, 100], [1.0, 1.1, 1.2], f0=1e9)
    r = False
except ValueError:
    r = True
ok("rising H_c (no decay) refused", r)
src = (HERE / "sharrock.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)
failed = [n for n, v in checks if not v]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
