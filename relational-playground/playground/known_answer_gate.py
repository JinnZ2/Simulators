"""ADDITION 3. Known-answer gate: nothing is trusted until it has been run against
answers fixed in advance, with defects planted, and against nulls.

For every equation module:
  clean draws    random parameters (seeded), answer known in closed form.
                 The detector must stay silent on all of them      -> FP = 0
  planted draws  the same draws with one defect planted:
                   leak  a term in the state equation that is not in the transfer table
                   coef  the first transfer's rate scaled by 1.1 (table and state agree)
                 The detector must fire on all of them             -> TP = 1
  detector       L0 LEAK on a LIVE budget, OR answer outside tolerance.

Pass rule is FP == 0 and TP == 1 exactly. The harness classes follow
null-harness/null_harness.py (CONSTANT_FIRES, CONSTANT_SILENT, ...); that module
imports numpy, so the harness is restated here in stdlib, and its `_verdict`
is not reused because it reads TP = 0.5 as OK (tools/known_answer.py pins that).

A model that has not passed is UNTRUSTED and its runs are INCOMPLETE.
"""
import math, random
from .equations import base as eq
from .equations.base import ModelOutput, from_transfers
from .harness import harness_class

N_DRAWS = 12
_STATE = {}          # model name -> dict(trusted, evidence)
_BUILDERS = {}       # model name -> builder(rng) -> dict(config kwargs, output, expected, tol)
_TOOLS = {}          # tool name -> (nulls, signals, detector)


def plant(model, kind):
    """A defective copy of a model. Never registered; used by the gate only."""
    def fn(state, env, rel, ctl, p):
        out = model.fn(state, env, rel, ctl, p)
        names = list(out.state_changes)
        if kind == "leak":
            d = dict(out.state_changes)
            d[names[0]] -= 0.02 * abs(state[names[0]]) + 0.01
            return ModelOutput(d, transfers=out.transfers, new_config=out.new_config)
        if kind == "coef":
            tr = list(out.transfers)
            n, s, t, r = tr[0]
            tr[0] = (n, s, t, 1.1 * r)
            return ModelOutput(from_transfers(tr, names), transfers=tr, new_config=out.new_config)
        raise ValueError(kind)
    return eq.Model(model.name + "+" + kind, model.family, model.version, fn, model.kind, model.requires)


def add_builder(model_name, builder):
    _BUILDERS[model_name] = builder


def add_tool(name, nulls, signals, detector):
    _TOOLS[name] = (nulls, signals, detector)


def _fires(model, case, make_config):
    from .experiments import runner
    cfg = make_config(case)
    params, state = cfg["parameters"].resolve(), cfg["initial"].resolve()
    times, states, _ = runner.integrate(model, cfg, params, state)
    from . import l0
    rows, _ = l0.audit(cfg["budgets"], states[0], states[-1])
    leak = any(r["verdict"] == "LEAK" for r in rows)
    exp = case["expected"] if isinstance(case["expected"], dict) else {case["output"]: case["expected"]}
    got = {k: states[-1][k] for k in exp}
    off = any(abs(got[k] - v) > case["tol"] * max(1.0, abs(v)) for k, v in exp.items())
    return leak or off, dict(leak=leak, got=got, expected=exp)


def certify(model_name, make_config, seed=20261110):
    """Run the gate for one model. Returns the evidence and stores the trust state."""
    if model_name not in _BUILDERS:
        _STATE[model_name] = dict(trusted=False, evidence="no known-answer cases written for this model")
        return _STATE[model_name]
    model = eq.get(model_name)
    rng = random.Random(seed)
    cases = [_BUILDERS[model_name](rng) for _ in range(N_DRAWS)]
    fp = sum(_fires(model, c, make_config)[0] for c in cases) / len(cases)
    tp_hits, misses = 0, []
    for i, c in enumerate(cases):
        kind = ("leak", "coef")[i % 2]
        hit, detail = _fires(plant(model, kind), c, make_config)
        tp_hits += hit
        if not hit:
            misses.append((kind, detail))
    tp = tp_hits / len(cases)
    cls = harness_class(fp, tp)
    _STATE[model_name] = dict(trusted=cls == "PASS", harness=cls, FP=fp, TP=tp, draws=len(cases),
                              evidence="%d clean draws, %d planted (leak / coef alternating); FP %.2f TP %.2f" % (len(cases), len(cases), fp, tp),
                              misses=misses)
    return _STATE[model_name]


def certify_tool(name):
    nulls, signals, detector = _TOOLS[name]
    fp = sum(bool(detector(x)) for x in nulls) / len(nulls)
    tp = sum(bool(detector(x)) for x in signals) / len(signals)
    cls = harness_class(fp, tp)
    _STATE["tool:" + name] = dict(trusted=cls == "PASS", harness=cls, FP=fp, TP=tp,
                                  evidence="%d nulls, %d planted signals" % (len(nulls), len(signals)))
    return _STATE["tool:" + name]


def trust(name):
    return _STATE.get(name, dict(trusted=False, evidence="gate not run for %s" % name))


def require_tool(name):
    t = trust("tool:" + name)
    if not t["trusted"]:
        raise RuntimeError("analysis tool %s is not through the known-answer gate: %s" % (name, t["evidence"]))


# ---------------------------------------------------------------- closed-form cases

def _u(rng, lo, hi):
    return lo + (hi - lo) * rng.random()


def _linear(rng):
    k, x0, T = _u(rng, 0.2, 2.0), _u(rng, 1.0, 5.0), 1.0
    return dict(model="linear", params=dict(A={"x": {"x": -k}}, B={}, u={}, compartmental=True), initial=dict(x=x0),
                t_end=T, dt=0.01, live=dict(mass=["x"]), output="x", expected=x0 * math.exp(-k * T), tol=1e-6)


def _allee(rng):
    r, a, K = _u(rng, 0.5, 2.0), _u(rng, 0.5, 1.5), _u(rng, 8.0, 12.0)
    h = _u(rng, 0.01, 0.2) * r
    # upper root of (x/a - 1)(1 - x/K) = h/r
    A_, B_, C_ = -1.0 / (a * K), 1.0 / a + 1.0 / K, -(1.0 + h / r)
    x = (-B_ - math.sqrt(B_ * B_ - 4 * A_ * C_)) / (2 * A_)
    return dict(model="allee", params=dict(r=r, a=a, K=K, h=h), initial=dict(x=3 * a), t_end=80.0, dt=0.01,
                live=dict(mass=["x"]), output="x", expected=x, tol=1e-6)


def _network(rng):
    w, x1, x2, T = _u(rng, 0.2, 2.0), _u(rng, 1.0, 5.0), _u(rng, 0.0, 2.0), 1.0
    return dict(model="network", params=dict(edge_class="matter transfer", g="identity", outside_level={}),
                initial=dict(a=x1, b=x2), t_end=T, dt=0.01, live=dict(mass=["a", "b"]), output="b",
                expected=x2 + x1 * (1 - math.exp(-w * T)), tol=1e-6, edges=[("a", "b", w)])


def _energy(rng):
    pin, dem, k, e0, T = _u(rng, 1.0, 3.0), _u(rng, 0.1, 0.9), _u(rng, 0.2, 1.5), _u(rng, 1.0, 4.0), 1.0
    es = (pin - dem) / k
    return dict(model="energy_store", params=dict(P_in=pin, demand=dem, k_diss=k), initial=dict(E=e0), t_end=T, dt=0.01,
                live=dict(energy=["E"]), output="E", expected=es + (e0 - es) * math.exp(-k * T), tol=1e-6)


def _permeable(rng):
    perm, loss, e, x0, T = _u(rng, 0.2, 2.0), _u(rng, 0.05, 0.5), _u(rng, 1.0, 5.0), _u(rng, 0.0, 1.0), 1.0
    xs, lam = perm * e / (perm + loss), perm + loss
    return dict(model="permeable", params=dict(perm0=perm, perm_drift=0.0, outside=e, loss=loss), initial=dict(x=x0),
                t_end=T, dt=0.01, live=dict(mass=["x"]), output="x", expected=xs + (x0 - xs) * math.exp(-lam * T), tol=1e-6)


def _mean_reverting(rng):
    th, mu, x0, dt, n = _u(rng, 0.2, 2.0), _u(rng, -2.0, 2.0), _u(rng, 3.0, 5.0), 0.01, 100
    return dict(model="mean_reverting", params=dict(theta=th, mu=mu, sigma=0.0), initial=dict(x=x0), t_end=n * dt, dt=dt,
                live=dict(mass=["x"]), output="x", expected=mu + (x0 - mu) * (1 - th * dt) ** n, tol=1e-9)


def _percolation(rng):
    L = rng.randrange(4, 9)
    init = dict(unassigned=L * L, unburned=0, burning=0, burned=0, bare=0)
    if rng.random() < 0.5:        # every cell flammable: the whole grid burns from the lit edge
        return dict(model="percolation", params=dict(L=L, p_flammable=1.0, spot=0.0, ignition="left_edge", grid="RANDOM"),
                    initial=init, t_end=4 * L, dt=1.0, live=dict(mass=list(init)), output="burned",
                    expected=dict(burned=L * L, unburned=0, bare=0, burning=0), tol=1e-9)
    w = rng.randrange(1, L - 1)   # a bare wall in column w: only the columns left of it burn
    grid = [[0 if j == w else 1 for j in range(L)] for _ in range(L)]
    return dict(model="percolation", params=dict(L=L, p_flammable=0.0, spot=0.0, ignition="left_edge", grid=grid),
                initial=init, t_end=4 * L, dt=1.0, live=dict(mass=list(init)), output="burned",
                expected=dict(burned=L * w, unburned=L * (L - w - 1), bare=L, burning=0), tol=1e-9)


def _branching(rng):
    n0, k, n = rng.randrange(1, 6), rng.randrange(0, 4), rng.randrange(2, 6)
    retired = n0 * n if k == 1 else n0 * (k ** n - 1) // (k - 1) if k > 1 else n0
    return dict(model="branching", params=dict(R=k, offspring="fixed", cap=10 ** 9), initial=dict(active=n0, retired=0),
                t_end=float(n), dt=1.0, live=dict(mass=["active", "retired"]), output="active",
                expected=dict(active=n0 * k ** n, retired=retired), tol=1e-9)


for _n, _b in (("percolation", _percolation), ("branching", _branching), ("linear", _linear), ("allee", _allee), ("network", _network), ("energy_store", _energy),
               ("permeable", _permeable), ("mean_reverting", _mean_reverting)):
    add_builder(_n, _b)


def default_make_config(case):
    """Build a runnable Config from a case. Lives here so the gate needs nothing from tests/."""
    from .uncertainty import Value, UncertaintyMatrix
    from .system import SystemDefinition, FIELDS as SF, UNDECLARED
    from .controls import ControlMatrix, FIELDS as CF
    from .environment import Environment
    from .relationships import RelationalMatrix, Relationship
    from .experiments.runner import Config
    from . import l0
    K = lambda v: Value(v, "ASSUMED", "known-answer case")
    rel = None
    if case.get("edges"):
        rel = RelationalMatrix([Relationship(s, d, "matter transfer", w) for s, d, w in case["edges"]])
    live = case["live"]
    return Config(run_id="gate:" + case["model"], system=SystemDefinition("gate", **{f: UNDECLARED for f in SF}),
                  boundary=None, model=case["model"], relationships=rel, controls=ControlMatrix(**{f: UNDECLARED for f in CF}),
                  environment=Environment(case.get("seed", 1)),
                  parameters=UncertaintyMatrix({k: K(v) for k, v in case["params"].items()}),
                  initial=UncertaintyMatrix({k: K(v) for k, v in case["initial"].items()}),
                  t_end=case["t_end"], dt=case["dt"], observations=None,
                  budgets=l0.declare(**{b: (l0.Budget(b, pools=live[b]) if b in live else l0.Budget(b, void_reason="not in this case")) for b in l0.BUDGETS}))


def _tool_cases():
    from .analysis import transitions, model_limits
    rng = random.Random(7)
    xs = [i / 10.0 for i in range(11)]
    nulls, signals = [], []
    for _ in range(N_DRAWS):
        s, c = _u(rng, -1.0, 1.0), _u(rng, -1.0, 1.0)
        ramp = [c + s * x for x in xs]
        nulls.append((xs, ramp, None))
        j = rng.randrange(1, 9)
        signals.append((xs, [v + (5.0 if i > j else 0.0) for i, v in enumerate(ramp)], (xs[j], xs[j + 1])))
    add_tool("transitions.read", nulls, signals,
             lambda c: transitions.read(c[0], c[1])["steepest_between"] != "NONE"
             and (c[2] is None or tuple(transitions.read(c[0], c[1])["steepest_between"]) == c[2]))
    nulls = [[dict(point=i, predicted=1.0, observed=1.0 + _u(rng, -0.05, 0.05), uncertainty=0.1) for i in range(5)] for _ in range(N_DRAWS)]
    signals = [[dict(point=i, predicted=1.0, observed=1.0 + (0.5 if i == 2 else 0.0), uncertainty=0.1) for i in range(5)] for _ in range(N_DRAWS)]
    add_tool("model_limits.failure_region", nulls, signals, lambda pts: model_limits.failure_region(pts)["counts"]["OUTSIDE"] > 0)


def certify_all():
    eq.load_all()
    _tool_cases()
    out = {}
    for name in sorted(eq.REGISTRY):
        out[name] = certify(name, default_make_config)
    for name in sorted(_TOOLS):
        out["tool:" + name] = certify_tool(name)
    return out
