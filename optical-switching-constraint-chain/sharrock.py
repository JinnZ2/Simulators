#!/usr/bin/env python3
"""OSC-WO3 helper: the Sharrock fit, so a future measurement drops straight
into decision.py. Written before any data exists; it is exercised here only
on constructed data with a planted barrier.

Sharrock form (exponent 1/2, as the report quotes it):
    H_c(t) = H_c0 * (1 - sqrt( (k_B T / E_b) * ln(f0 t / ln 2) ))

With x = sqrt(ln(f0 t / ln 2)) this is a straight line, H_c = a + b x, with
a = H_c0 and b = -H_c0 sqrt(k_B T / E_b). Hence

    Delta = E_b / (k_B T) = (a / b)^2

Two consequences the protocol card relies on:
  1. Delta comes out without T or units of H: only the line's shape matters.
  2. The attempt frequency f0 is NOT fitted; it enters through x. So f0 is a
     declared input, and the reported Delta is a band over the declared f0
     range, never a point taken at one assumed f0.

    python3 sharrock.py     fit on constructed data, Delta over an f0 range, decision readout
The module refuses --selftest; checks live in test_sharrock.py.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from barrier_per_bit import UndeclaredTerm  # noqa: E402


def x_of(t, f0):
    arg = f0 * t / math.log(2)
    if arg <= 1:
        raise ValueError("f0 t / ln2 must exceed 1 for the Sharrock form")
    return math.sqrt(math.log(arg))


def _ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    return my - b * mx, b


def fit_delta(times, hc, *, f0):
    """Delta from (waiting time s, remanent coercivity) pairs at one declared f0."""
    if f0 is None:
        raise UndeclaredTerm("undeclared: f0 (attempt frequency is not fitted)")
    if len(times) != len(hc) or len(times) < 3:
        raise ValueError("need at least three (t, H_c) pairs")
    a, b = _ols([x_of(t, f0) for t in times], hc)
    if b >= 0:
        raise ValueError("H_c does not fall with waiting time: no Sharrock decay to fit")
    return (a / b) ** 2


def delta_band(times, hc, *, f0_range):
    """Delta over a declared f0 range (lo, hi): the honest output."""
    if f0_range is None:
        raise UndeclaredTerm("undeclared: f0_range")
    lo, hi = sorted(f0_range)
    d = [fit_delta(times, hc, f0=f) for f in (lo, hi)]
    return min(d), max(d)


def synthetic(delta, f0, hc0=1.0, times=(1, 10, 100, 1e3, 1e4, 1e5)):
    """Constructed data with a planted Delta; for checks only."""
    return list(times), [hc0 * (1 - math.sqrt(math.log(f0 * t / math.log(2)) / delta)) for t in times]


def render():
    import decision as d
    out = ["optical-switching-constraint-chain / sharrock.py", "=" * 64,
           "CONSTRUCTED data, planted Delta = 50 at f0 = 1e9 Hz (no measurement exists)", ""]
    t, h = synthetic(50, 1e9)
    out.append(f"fit at the true f0 1e9:   Delta = {fit_delta(t, h, f0=1e9):.2f}")
    for f in (1e8, 1e10, 1e11):
        out.append(f"fit at a wrong f0 {f:.0e}: Delta = {fit_delta(t, h, f0=f):.2f}")
    lo, hi = delta_band(t, h, f0_range=(1e9, 1e10))
    out.append(f"declared f0 range 1e9..1e10 -> Delta band {lo:.2f}..{hi:.2f}")
    single, pop = d.lines(years=10, tau0=1e-9, population_value=60, basis="carried, see decision.py")
    mid, half = (lo + hi) / 2, (hi - lo) / 2
    r = d.readout(single=single, pop=pop, measured=mid, uncertainty=half)
    out += [f"decision.py on that band: {r['state']}" + (f" {r['spans']}" if r["spans"] else ""),
            "", "f0 is part of the measurement's uncertainty, not a constant to assume."]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("sharrock.py is a library; run: python3 test_sharrock.py")
        sys.exit(2)
    print(render())
