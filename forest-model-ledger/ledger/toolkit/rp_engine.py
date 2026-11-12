"""Binding of equation_family_swap to the relational-playground engine (follow-up item 3). stdlib.

equation_family_swap.py is frozen by hash for the held-out gate (HELDOUT_FREEZE.md), so it is
not edited. Its swap(component, families, sweep, engine=...) takes an engine record; this module
builds one from the real engine and hands it in. The adapter's handoff() is used unchanged.

What the engine is, read at JinnZ2/Simulators branch claude/relational-playground (PR #257):
  relational-playground/playground/equations/base.py   REGISTRY of models, each with a family
  relational-playground/playground/known_answer_gate.py  a run is INCOMPLETE unless the gate
                                                       certified its model first (certify_all)
  experiments/model_comparison/forest_fire_regime/run.py  the one experiment that runs the SAME
                                                       component under two families: grid_run
                                                       (family percolation) and ode_run (the
                                                       mean-field ODE, model ode_meanfield)
It has no engine.py and no run_family(family, component, sweep): that was the adapter's guess
at an interface before the engine existed. This module is the translation, nothing more.

  find(paths=None)    ENGINE_FOUND | ENGINE_ABSENT, with path, commit, registered families
  coverage(found)     brief family -> engine families (BRIEF_TO_ENGINE, a declared reading [CHOICE])
  engine_record(...)  the record swap() takes; run_family supports COMPONENTS only
  point(...)          one engine call, module level so a process pool can run it

COMPONENTS: the engine's own components, not the ledger's. forest_fire_regime is a fuel grid
(L x L cells, four-neighbour contact, embers), not the ledger's L4_FIRE_MEANFIELD_ODE: a swap
run on it reads the engine's fire, and says nothing about the ledger's fire component.
"""
import importlib.util, os, subprocess, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# brief family -> engine REGISTRY families that carry it. Ising, spin glass, MaxEnt and
# random-matrix stability have no model in the engine at the pinned commit.
BRIEF_TO_ENGINE = {"ODE": ("linear", "nonlinear"), "percolation": ("percolation",), "Ising": (), "spin glass": (),
                   "MaxEnt": (), "branching process": ("branching",), "random-matrix stability": ()}
COMPONENTS = {"forest_fire_regime": dict(dir=os.path.join("experiments", "model_comparison", "forest_fire_regime"),
                                         families={"percolation": "grid_run", "ODE": "ode_run"})}


def default_paths():
    repo = os.path.dirname(HERE)
    out = [os.environ["RELATIONAL_PLAYGROUND_PATH"]] if os.environ.get("RELATIONAL_PLAYGROUND_PATH") else []
    return out + [os.path.join(os.path.dirname(repo), "relational-playground"), os.path.join(repo, "relational-playground")]


def _commit(path):
    try:
        return subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10).stdout.strip() or None
    except Exception:
        return None


_LOADED = {}


def _load(path, component=None):
    """Import the engine (and a component's experiment module) from `path`. Cached per process."""
    key = (path, component)
    if key in _LOADED:
        return _LOADED[key]
    if path not in sys.path:
        sys.path.insert(0, path)
    from playground.equations import base
    base.load_all()
    mod = None
    if component:
        d = os.path.join(path, COMPONENTS[component]["dir"])
        if d not in sys.path:
            sys.path.insert(0, d)
        spec = importlib.util.spec_from_file_location("rp_component_" + component, os.path.join(d, "run.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        from playground import known_answer_gate as gate
        gate.certify_all()                      # the engine's own rule: no COMPLETE run on an uncertified model
    _LOADED[key] = (base, mod)
    return _LOADED[key]


def find(paths=None):
    looked = list(paths if paths is not None else default_paths())
    for p in looked:
        if os.path.isfile(os.path.join(p, "playground", "equations", "base.py")):
            base, _ = _load(p)
            fam = {}
            for n, m in sorted(base.REGISTRY.items()):
                fam.setdefault(m.family, []).append(n)
            return dict(state="ENGINE_FOUND", path=p, looked=looked, commit=_commit(p), families=fam)
    return dict(state="ENGINE_ABSENT", path=None, looked=looked, commit=None, families={})


def coverage(found):
    return {b: [f for f in e if f in found["families"]] for b, e in BRIEF_TO_ENGINE.items()}


def point(args):
    """One engine call: (path, component, family, x, spot, seed) -> engine result dict."""
    path, component, family, x, spot, seed = args
    _, mod = _load(path, component)
    fn = getattr(mod, COMPONENTS[component]["families"][family])
    return fn(x, spot, seed) if family == "percolation" else fn(x, spot)


def curve(path, component, family, sweep, spot, seeds, mapper=map, spread="se"):
    """[{x, mean, sd, n, sd_run, statuses}] ; sd is the standard error of the mean (spread='se')
    or the per-run sd (spread='run') [CHOICE]. The ODE is deterministic: one call, sd 0."""
    import statistics
    ss = list(seeds) if family == "percolation" else [0]
    jobs = [(path, component, family, x, spot, s) for x in sweep for s in ss]
    res = list(mapper(point, jobs))
    out, k = [], 0
    for x in sweep:
        rs = res[k:k + len(ss)]
        k += len(ss)
        v = [r["burned_fraction"] for r in rs]
        sd_run = statistics.stdev(v) if len(v) > 1 else 0.0
        out.append(dict(x=x, mean=statistics.mean(v), n=len(v), sd_run=sd_run,
                        sd=(sd_run / len(v) ** 0.5) if spread == "se" else sd_run,
                        statuses=sorted({r["status"] for r in rs}), still_burning=max(r["still_burning"] for r in rs)))
    return out


def engine_record(found, spot=0.0, seeds=range(40), mapper=map, spread="se"):
    """The record equation_family_swap.swap(..., engine=) takes."""
    class Binding:
        @staticmethod
        def run_family(family, component, sweep):
            if component not in COMPONENTS:
                raise KeyError(f"component {component!r} is not one the engine runs under two families; engine components: {sorted(COMPONENTS)}")
            if family not in COMPONENTS[component]["families"]:
                raise KeyError(f"family {family!r} has no runner for {component} in the engine")
            return curve(found["path"], component, family, sweep, spot, seeds, mapper, spread)
    return dict(state=found["state"], path=found["path"], looked=found["looked"], engine=Binding)


if __name__ == "__main__":
    f = find()
    print(f"engine: {f['state']}  path {f['path']}  commit {f['commit']}")
    for p in f["looked"]:
        print("  looked:", p)
    if f["state"] == "ENGINE_FOUND":
        print("registered families:", {k: v for k, v in f["families"].items()})
        for b, e in coverage(f).items():
            print(f"  brief {b:24s} -> {e or 'NOT IN ENGINE'}")
