"""run_18: residual_regression on run_10's trigger (card CC_001; run_14 inherits it).

    python3 runs/run_18.py     # about a minute on 4 workers; reproduces samples/run_18.sample.txt

Residual: N misclosure. Design: dt {1/52, 1/64, 1/104} x dep {0.8, 1.0, 1.2} x years {150, 300}
x seeds {0, 1} = 36 runs, every other parameter at DEFAULTS.
Fields, declared:
  method   dt, steps ; and, in fit 2, counter_err: the deposition counter's own roundoff
           computed with NO model (add the RK4 increment for a constant rate `steps` times,
           run_10 section 6)
  biology  dep, fires (count), T_mean (tree N, years 100 on)
Fit 1 asks whether the generic method fields explain the residual; fit 2 adds the counter.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import base, l0_audit
from ledger.toolkit import residual_regression as rr

IX = base.IX


def bare_counter_err(dep, dt, years):
    n = int(round(years / dt)); acc = 0.0
    for _ in range(n):
        acc = acc + dt / 6 * (dep + 2 * dep + 2 * dep + dep)
    return acc - dep * years


def one(args):
    dt, dep, years, seed = args
    r = base.simulate(seed=seed, dt=dt, years=years, params=dict(dep=dep))
    late = r["traj"][int(round(min(100, years / 2) / dt)):]
    return dict(N_mis=l0_audit.audit(r)["N"]["misclosure"], dt=dt, steps=int(round(years / dt)),
                counter_err=bare_counter_err(dep, dt, years), dep=dep, fires=len(r["events"]),
                T_mean=float(late[:, IX["T"]].mean()), years=years, seed=seed)


def main():
    from concurrent.futures import ProcessPoolExecutor
    jobs = [(dt, dep, y, s) for dt in (1 / 52, 1 / 64, 1 / 104) for dep in (0.8, 1.0, 1.2) for y in (150, 300) for s in (0, 1)]
    with ProcessPoolExecutor(4) as ex:
        rows = list(ex.map(one, jobs))
    print("thresholds [CHOICE]:", rr.CHOICES)
    print(f"runs {len(rows)}; N_mis range {min(r['N_mis'] for r in rows):+.3e} .. {max(r['N_mis'] for r in rows):+.3e}")
    print("\n== fit 1: generic method fields only")
    print(rr.render(rr.fit(rows, "N_mis", ["dt", "steps"], ["dep", "fires", "T_mean"])))
    print("\n== fit 2: method fields with the counter's own (model-free) roundoff")
    print(rr.render(rr.fit(rows, "N_mis", ["dt", "steps", "counter_err"], ["dep", "fires", "T_mean"])))
    print("\n== fit 3: counter roundoff alone as method, nothing else")
    print(rr.render(rr.fit(rows, "N_mis", ["counter_err"], ["dep", "fires", "T_mean"])))
    print("\nper run: dt  dep  years  seed   N_mis        -counter_err   fires")
    for r in rows:
        print(f"  1/{round(1 / r['dt']):3d} {r['dep']:.1f} {r['years']:4d} {r['seed']}  {r['N_mis']:+.4e}  {-r['counter_err']:+.4e}  {r['fires']:3d}")


if __name__ == "__main__":
    main()
