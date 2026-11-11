"""Run 9: rebuild of the run-6 mass-conserving model as the ledger base.

    python3 runs/run_9.py            # prints the record; runs/run_9.md pins it

Seed, params and every number in run_9.md come from this script.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from model import base, l0_audit

SEED, YEARS = 0, 300


def summary(res):
    ix, tr = base.IX, res["traj"]
    G = tr[:, ix["G"]]
    gone = np.nonzero(G < 1e-6)[0]
    ev = [e[0] for e in res["events"]]
    iv = np.diff(ev)
    return dict(
        fires=len(ev),
        fire_interval_mean=float(iv.mean()) if len(iv) else None,
        fire_interval_sd=float(iv.std()) if len(iv) else None,
        grass_below_1e6_at_yr=float(res["t"][gone[0]]) if len(gone) else None,
        final={k: float(res["y"][ix[k]]) for k in base.N_POOLS + base.W_POOLS},
    )


def main():
    cases = [
        ("base", dict(), True),
        ("no_fire", dict(), False),
        ("planted_leak_0.3", dict(leak=0.3), True),
        ("base_dt_half", dict(), True),
    ]
    for name, params, fires in cases:
        dt = 1 / 104 if name == "base_dt_half" else 1 / 52
        res = base.simulate(years=YEARS, dt=dt, seed=SEED, params=params, fires=fires)
        a = l0_audit.audit(res)
        s = summary(res)
        print(f"== {name}  seed={SEED} years={YEARS} dt=1/{round(1/dt)}")
        print(l0_audit.report(a))
        print(f"fires {s['fires']}  interval mean {s['fire_interval_mean']}  sd {s['fire_interval_sd']}")
        print(f"grass < 1e-6 at year {s['grass_below_1e6_at_yr']}")
        print("final " + "  ".join(f"{k}={v:.4f}" for k, v in s["final"].items()))
        print()
    print("== seeds 0..9, base: fires / grass-gone year / N misclosure")
    for seed in range(10):
        res = base.simulate(years=YEARS, seed=seed)
        a, s = l0_audit.audit(res), summary(res)
        print(f"seed {seed}: fires {s['fires']:3d}  grass gone {s['grass_below_1e6_at_yr']}  N mis {a['N']['misclosure']:+.2e}  {a['_overall']}")


if __name__ == "__main__":
    main()
