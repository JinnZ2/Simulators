"""Run 10: toolbox trigger -- N misclosure -5.0e-11, near-identical across seeds 0-9.

    python3 runs/run_10.py

Three explanations to separate before calling it roundoff:
  (a) the seed is not wired to the fire draw   -> seed test hollow
  (b) fires are identical across seeds
  (c) roundoff from the deterministic part
model/base.py is not edited by this run.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from model import base, l0_audit

IX = base.IX


def mis(res, budget="N"):
    return l0_audit.audit(res)[budget]["misclosure"]


def main():
    print("== 1. per-seed fire count and fire times (base, 300 yr, dt 1/52)")
    times = {}
    for seed in range(10):
        r = base.simulate(seed=seed)
        ev = [round(e[0], 3) for e in r["events"]]
        times[seed] = ev
        print(f"seed {seed}: fires {len(ev):3d}  first 5 {ev[:5]}  N mis {mis(r):+.6e}")
    distinct = len({tuple(v) for v in times.values()})
    print(f"distinct fire-time sequences across 10 seeds: {distinct}")

    print("\n== 2. seed -> ignition draw alone (drought_sd=0: precipitation identical in every seed)")
    t2 = {}
    for seed in range(10):
        r = base.simulate(seed=seed, params=dict(drought_sd=0.0))
        ev = [round(e[0], 3) for e in r["events"]]
        t2[seed] = ev
        w = r["traj"][:520, IX["W"]]            # first 10 yr, before any fire can differ much
        print(f"seed {seed}: fires {len(ev):3d}  first 3 {ev[:3]}  precip total {r['y'][IX['precipitation']]:.10f}  N mis {mis(r):+.6e}")
    print(f"distinct fire-time sequences with precipitation held identical: {len({tuple(v) for v in t2.values()})}")
    print(f"distinct precipitation totals: {len({round(base.simulate(seed=s, years=5, params=dict(drought_sd=0.0))['y'][IX['precipitation']], 12) for s in range(4)})}")

    print("\n== 3. misclosure at dt, dt/2, dt/4 and at a power-of-two dt (seed 0)")
    for label, dt in (("1/52", 1 / 52), ("1/104", 1 / 104), ("1/208", 1 / 208), ("1/64", 1 / 64), ("1/128", 1 / 128)):
        r = base.simulate(dt=dt)
        print(f"dt {label:6s} steps {int(round(300/dt)):6d}  N mis {mis(r):+.6e}  water mis {mis(r, 'water'):+.6e}  fires {len(r['events'])}")

    print("\n== 4. misclosure with fire disabled, and with the constant deposition term removed (seed 0..2)")
    for seed in range(3):
        a = mis(base.simulate(seed=seed, fires=False))
        rb = base.simulate(seed=seed, params=dict(dep=0.0))
        c = mis(base.simulate(seed=seed, fires=False, params=dict(dep=0.0)))
        print(f"seed {seed}: no fire {a:+.6e}   dep=0 {mis(rb):+.6e} (fires {len(rb['events'])})   no fire and dep=0 {c:+.6e}")

    print("\n== 5. growth with run length (seed 0, dt 1/52): roundoff bias accumulates per step")
    for years in (30, 75, 150, 300):
        r = base.simulate(years=years)
        m = mis(r)
        print(f"years {years:4d}  steps {years*52:6d}  N mis {m:+.6e}  per step {m/(years*52):+.3e}")

    print("\n== 6. the deposition accumulator alone, no model: add dt*dep N times in float64")
    for label, dt in (("1/52", 1 / 52), ("1/104", 1 / 104), ("1/208", 1 / 208), ("1/64", 1 / 64)):
        n = int(round(300 / dt)); acc = 0.0
        for _ in range(n):
            acc = acc + dt / 6 * (1.0 + 2 * 1.0 + 2 * 1.0 + 1.0)   # the RK4 combination for a constant rate 1.0
        print(f"dt {label:5s}: accumulated {acc!r}   minus exact 300 = {acc - 300.0:+.6e}   (model N misclosure has the opposite sign: it subtracts this counter)")


if __name__ == "__main__":
    main()
