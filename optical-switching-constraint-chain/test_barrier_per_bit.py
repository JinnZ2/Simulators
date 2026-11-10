#!/usr/bin/env python3
"""Checks for barrier_per_bit.py (OSC-WO1). Stdlib only."""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import barrier_per_bit as b  # noqa: E402

checks = []


def ok(name, cond):
    checks.append((name, bool(cond)))


def raises(fn, **kw):
    try:
        fn(**kw)
    except b.UndeclaredTerm:
        return True
    return False


R = b.REPORT
# reproduces the report where the report is reproducible
for n, st in ((5, 224), (7, 12.5), (9, 2.7), (10, 1.6), (12, 0.75)):
    ok(f"stripe N={n} within 5% of the report's {st} um", abs(b.stripe_period(n, **R) * 1e6 / st - 1) < 0.05)
ok("first N below 1.5 um is 11", b.crossover_n(1.5e-6, **R) == 11)
ok("no crossover over the range returns None, not a number",
   b.crossover_n(1e-12, **R) is None)
for shape, k, t, want in (("cylinder", 5e6, 10e-9, 2.5), ("square", 0.5e6, 12e-9, 6.4),
                          ("square", 0.5e6, 5.4e-9, 9.6), ("square", 0.3e6, 5.4e-9, 12.4)):
    got = b.lateral_at_delta(60, shape=shape, k=k, thickness=t, temperature=300) * 1e9
    ok(f"Delta=60 size {shape} K={k:g} t={t * 1e9:g} nm ~ {want}", abs(got / want - 1) < 0.02)
ok("delta inverts lateral_at_delta",
   abs(b.delta_coherent(shape="square", k=0.5e6, thickness=12e-9, temperature=300,
                        lateral=b.lateral_at_delta(60, shape="square", k=0.5e6, thickness=12e-9,
                                                   temperature=300)) - 60) < 1e-9)

# retention line: two criteria, never merged
sb = b.retention_line(criterion="single_bit", years=10, tau0=1e-9)
ok("single-bit 10-year line is ln(t/tau0) ~ 40.3", abs(sb - math.log(10 * b.YEAR / 1e-9)) < 1e-12 and 40 < sb < 41)
ok("population value without basis is refused",
   raises(b.retention_line, criterion="population", years=10, tau0=1e-9, population_value=60))
ok("population value with basis is returned as declared",
   b.retention_line(criterion="population", years=10, tau0=1e-9, population_value=60, basis="x") == 60.0)
ok("missing tau0 refused", raises(b.retention_line, criterion="single_bit", years=10, tau0=None))

# energy ledger: absorbed needs a declared fraction
kw = dict(fluence=4e-3, spot_diameter=0.76, spot_shape="disc", pulses=100)
inc = b.energy_per_bit(ledger="incident", **kw)
ok("incident AO-HDS row = 1814.6 pJ (disc)", abs(inc * 1e12 - 1814.58) < 0.1)
ok("absorbed without fraction is refused", raises(b.energy_per_bit, ledger="absorbed", **kw))
ok("absorbed with fraction 0.3527 reproduces the stated 640 pJ",
   abs(b.energy_per_bit(ledger="absorbed", absorbed_fraction=640 / 1814.58, **kw) * 1e12 - 640) < 0.1)
ok("spot shape undeclared is refused",
   raises(b.energy_per_bit, fluence=4e-3, spot_diameter=0.76, spot_shape=None, pulses=100, ledger="incident"))
ok("square spot is 4/pi of disc",
   abs(b.energy_per_bit(ledger="incident", **{**kw, "spot_shape": "square"}) / inc - 4 / math.pi) < 1e-12)
ok("measured zero fraction returns 0.0, not refused",
   b.energy_per_bit(ledger="absorbed", absorbed_fraction=0.0, **kw) == 0.0)
try:
    b.energy_per_bit(ledger="absorbed", absorbed_fraction=1.5, **kw)
    rejected = False
except ValueError:
    rejected = True
ok("fraction above 1 rejected", rejected)

# render refuses the absorbed column and flags the borrowed fluence
r = b.render()
ok("render shows REFUSED absorbed column", r.count("REFUSED") >= 4)
ok("render names the borrowed UCSD fluence", "Vomir 2017" in r)
src = (HERE / "barrier_per_bit.py").read_text(encoding="utf-8")
ok("module refuses --selftest", "sys.exit(2)" in src)

failed = [n for n, v in checks if not v]
for n, v in checks:
    print(("PASS " if v else "FAIL ") + n)
print(f"checks: {len(checks)}   failed: {len(failed)}")
sys.exit(1 if failed else 0)
