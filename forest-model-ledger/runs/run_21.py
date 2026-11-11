"""run_21: equation_family_swap against the relational-playground engine (follow-up item 3).

    RELATIONAL_PLAYGROUND_PATH=/path/to/relational-playground python3 runs/run_21.py   # about 6 min, 4 workers

The adapter (ledger/toolkit/equation_family_swap.py, frozen) is bound to the real engine through
ledger/toolkit/rp_engine.py and run on the one component the engine runs under two brief
families: forest_fire_regime, percolation (grid_run) against ODE (ode_run, mean-field).
Sweep = the engine's own PREREG levels; spots 0.0, 0.05, 0.2; 40 grid replicates per point,
seeds 0-39, as the engine's experiment. The engine's known-answer gate certifies its models
first (its own rule: no COMPLETE run on an uncertified model).

Two checks before the adapter reads anything:
  the adapter's grid and ODE means reproduce the engine's own out/part2.json (same seeds)
  every engine run is COMPLETE and nothing is still burning at the last step
handoff() is read twice: sd = standard error of the grid mean (default) and sd = per-run sd.
This is the ENGINE's fire grid, not the ledger's L4_FIRE_MEANFIELD_ODE: no ledger component
is swapped here, and CC_003's local_normal_form slot is not filled by it.
"""
import json, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from ledger.toolkit import equation_family_swap as E, rp_engine as R

SPOTS = (0.0, 0.05, 0.2)
SEEDS = range(40)


def _init(path):
    R._load(path, "forest_fire_regime")


def main():
    found = R.find()
    print(f"engine {found['state']}  path {found['path']}  commit {found['commit']}")
    if found["state"] != "ENGINE_FOUND":
        for p in found["looked"]:
            print("  looked:", p)
        print("NOT RUN: engine absent on every path; set RELATIONAL_PLAYGROUND_PATH")
        return None
    print("brief family -> engine families:", {b: e or "NOT IN ENGINE" for b, e in R.coverage(found).items()})
    print("adapter thresholds:", E.CHOICES, " frozen file equation_family_swap.py (HELDOUT_FREEZE.md)")
    _, mod = R._load(found["path"], "forest_fire_regime")
    sweep = list(mod.LEVELS)
    ref = json.load(open(os.path.join(found["path"], R.COMPONENTS["forest_fire_regime"]["dir"], "out", "part2.json")))["table"]
    from concurrent.futures import ProcessPoolExecutor
    out = {}
    with ProcessPoolExecutor(4, initializer=_init, initargs=(found["path"],)) as ex:
        mapper = lambda f, xs: ex.map(f, xs, chunksize=8)
        for spot in SPOTS:
            rec = R.engine_record(found, spot=spot, seeds=SEEDS, mapper=mapper)
            sw = E.swap("forest_fire_regime", ["percolation", "ODE"], sweep, engine=rec)
            g, o = sw["results"]["percolation"], sw["results"]["ODE"]
            rows = ref["spot_%.2f" % spot]
            repro = max(max(abs(a["mean"] - r["grid_mean"]), abs(b["mean"] - r["ode"])) for a, b, r in zip(g, o, rows))
            statuses = sorted({s for p in g + o for s in p["statuses"]})
            burning = max(p["still_burning"] for p in g + o)
            h_se = E.handoff(g, o)
            g_run = [dict(p, sd=p["sd_run"]) for p in g]
            h_run = E.handoff(g_run, o)
            out[spot] = dict(grid=g, ode=o, repro=repro, statuses=statuses, burning=burning, h_se=h_se, h_run=h_run)
            print(f"\n== spot {spot:.2f}   reproduces engine out/part2.json: max |diff| {repro:.2e}   statuses {statuses}   still burning max {burning:.1e}")
            print("  drought  grid_mean  se       sd_run   ode      |gap|/se  |gap|/sd_run")
            for a, b in zip(g, o):
                gap = abs(a["mean"] - b["mean"])
                print(f"  {a['x']:5.2f}    {a['mean']:.4f}     {a['sd']:.5f}  {a['sd_run']:.5f}  {b['mean']:.4f}  {gap / a['sd'] if a['sd'] else float('inf'):8.1f}  {gap / a['sd_run'] if a['sd_run'] else float('inf'):8.1f}")
            print(f"  handoff, sd = se of the grid mean : disagree at {h_se['disagree_at']}")
            print(f"                                     regime {h_se['regime_at']}  handoffs {h_se['handoffs']}")
            print(f"  handoff, sd = per-run sd           : disagree at {h_run['disagree_at']}")
            print(f"                                     regime {h_run['regime_at']}  handoffs {h_run['handoffs']}")
    return out


if __name__ == "__main__":
    main()
