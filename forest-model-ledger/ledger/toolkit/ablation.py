"""Toolkit: ablation. Tool #2 of the staged build (work order 2026-11-11).

Entry: ledger/toolkit/ablation.yaml. Gate: tests/test_toolkit.py.

Drop one variable, see what actually matters -- and check that one was dropped.

  run(simulate, ablations, seeds, delta, band, active)
    simulate(seed, overrides) -> dict of scalar outputs
    ablations  list of {name, overrides, drops: [component names it intends to remove]}
    active     {component: fn(outputs) -> bool}: an activity the run can be seen doing
               (fire: fires > 0). Declared by the caller; the tool does not infer it.

  per ablation, against the base on the SAME seeds (multi_seed_ensemble.paired):
    per output   MOVED | EXACT_ZERO | EQUIVALENT | UNRESOLVED   (imported, not copied)
    reading      MATTERS            some output MOVED
                 DOES_NOT_MATTER    every output EXACT_ZERO or EQUIVALENT
                 UNRESOLVED         neither: not shown to matter, not shown not to
    co_ablated   activities active in the base on some seed and inactive on every
                 one of those seeds under the ablation, and NOT named in `drops`.
                 Non-empty = the drop removed more than one thing; its reading is
                 about the set, never about the named component alone.
    partial_co   same, but inactive on only some of those seeds

  interaction(simulate, a, b, seeds, delta)
    runs base, a, b, a+b; residual_s = (ab - base) - (a - base) - (b - base) per seed;
    NON_ADDITIVE when the residual reads MOVED, ADDITIVE when EXACT_ZERO / EQUIVALENT.

The reading inherits every threshold of multi_seed_ensemble (K_MOVED = 5).
"""
import os, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
from ledger.toolkit import multi_seed_ensemble as mse


def _runs(simulate, overrides, seeds):
    return {s: simulate(s, dict(overrides)) for s in seeds}


def reading(per_output):
    vs = [v["verdict"] for v in per_output.values()]
    if "MOVED" in vs:
        return "MATTERS"
    if all(v in ("EXACT_ZERO", "EQUIVALENT") for v in vs):
        return "DOES_NOT_MATTER"
    return "UNRESOLVED"


def co_ablation(base, arm, active, drops):
    full, part = [], []
    for comp, fn in (active or {}).items():
        if comp in drops:
            continue
        on = [s for s in base if fn(base[s])]
        if not on:
            continue
        off = [s for s in on if not fn(arm[s])]
        if len(off) == len(on):
            full.append(comp)
        elif off:
            part.append(comp)
    return full, part


def compare(base, arm, name, drops, active=None, delta=None, band=None):
    per = mse.paired(base, arm, delta, band)
    full, part = co_ablation(base, arm, active, drops)
    return dict(name=name, drops=list(drops), per_output=per, reading=reading(per),
                moved=[n for n, v in per.items() if v["verdict"] == "MOVED"],
                co_ablated=full, partial_co=part)


def run(simulate, ablations, seeds, delta=None, band=None, active=None, base=None):
    base = base if base is not None else _runs(simulate, {}, seeds)
    rows = []
    for a in ablations:
        arm = _runs(simulate, a["overrides"], seeds)
        rows.append(compare(base, arm, a["name"], a.get("drops", []), active, delta, band))
    return dict(base=base, rows=rows, seeds=list(seeds))


def interaction(simulate, a, b, seeds, delta=None, base=None):
    base = base if base is not None else _runs(simulate, {}, seeds)
    ra, rb = _runs(simulate, a, seeds), _runs(simulate, b, seeds)
    rab = _runs(simulate, {**a, **b}, seeds)
    resid = {s: {n: (rab[s][n] - base[s][n]) - (ra[s][n] - base[s][n]) - (rb[s][n] - base[s][n]) for n in base[s]}
             for s in seeds}
    zero = {s: {n: 0.0 for n in base[s]} for s in seeds}
    per = mse.paired(zero, resid, delta)
    vs = {n: v["verdict"] for n, v in per.items()}
    out = {n: ("NON_ADDITIVE" if v == "MOVED" else "ADDITIVE" if v in ("EXACT_ZERO", "EQUIVALENT") else "UNRESOLVED")
           for n, v in vs.items()}
    return dict(per_output=per, reading=out)


def render(res, choices=True):
    L = []
    if choices:
        L.append("thresholds (multi_seed_ensemble, [CHOICE]): " + "  ".join(f"{k} {v}" for k, v in mse.CHOICES.items()))
    for r in res["rows"]:
        L.append(f"{r['name']:34s} {r['reading']:16s} moved {r['moved'] or '-'}"
                 + (f"   CO_ABLATED {r['co_ablated']}" if r["co_ablated"] else "")
                 + (f"   partial {r['partial_co']}" if r["partial_co"] else ""))
    return "\n".join(L)


# ---------------------------------------------------------------- gate: planted cases + null harness
def _toy(seed, ov):
    """Synthetic: y = a*x1 + b*x2 + c*x1*x2 + seed noise; z (a 'fire') happens only when x1 > 0."""
    import random
    r = random.Random(seed)
    x1, x2 = ov.get("x1", 1.0), ov.get("x2", 1.0)
    a, b, c = 3.0, 0.0, ov.get("_c", 0.0)
    noise = r.gauss(0, 1)
    z = 4.0 + r.gauss(0, 0.3) if x1 > 0 else 0.0
    return dict(y=a * x1 + b * x2 + c * x1 * x2 + noise, z=z)


ACTIVE = dict(z_event=lambda o: o["z"] > 0)


def known_cases():
    seeds = range(20)
    res = run(_toy, [dict(name="x1 dropped", overrides=dict(x1=0.0), drops=["x1"]),
                     dict(name="x2 dropped", overrides=dict(x2=0.0), drops=["x2"]),
                     dict(name="x1 dropped, z named", overrides=dict(x1=0.0), drops=["x1", "z_event"])],
              seeds, delta=dict(y=0.5, z=0.5), active=ACTIVE)
    row = {r["name"]: r for r in res["rows"]}
    inter = interaction(lambda s, o: _toy(s, {**o, "_c": 2.0}), dict(x1=0.0), dict(x2=0.0), seeds, dict(y=0.5, z=0.5))
    add = interaction(_toy, dict(x1=0.0), dict(x2=0.0), seeds, dict(y=0.5, z=0.5))
    return [
        ("dropping a component with weight 3 MATTERS", "MATTERS", lambda: row["x1 dropped"]["reading"]),
        ("dropping a weight-0 component DOES_NOT_MATTER (silent)", "DOES_NOT_MATTER", lambda: row["x2 dropped"]["reading"]),
        ("dropping x1 silences the undeclared z event: CO_ABLATED", ["z_event"], lambda: row["x1 dropped"]["co_ablated"]),
        ("dropping x2 removes nothing else (silent)", [], lambda: row["x2 dropped"]["co_ablated"]),
        ("the same drop with z declared in drops is not flagged (silent)", [], lambda: row["x1 dropped, z named"]["co_ablated"]),
        ("planted x1*x2 term reads NON_ADDITIVE", "NON_ADDITIVE", lambda: inter["reading"]["y"]),
        ("purely additive toy reads ADDITIVE (silent)", "ADDITIVE", lambda: add["reading"]["y"]),
    ]


def gate(n=200, seeds=(0, 1, 2, 3, 4)):
    from ledger.toolkit import gate as G
    known = G.known_answers(known_cases(), lambda f: f())

    def pair(r, shift):
        base = {s: dict(y=r.gauss(0, 1)) for s in range(20)}
        arm = {s: dict(y=base[s]["y"] + shift + r.gauss(0, 1)) for s in range(20)}
        return base, arm

    def matters(x):
        return compare(x[0], x[1], "draw", [])["reading"] == "MATTERS"

    def act_draw(r, silence):
        k = r.randint(2, 5)
        names = [f"c{i}" for i in range(k)]
        base = {s: {n: 1.0 for n in names} for s in range(10)}
        arm = {s: dict(base[s]) for s in range(10)}
        drops = r.sample(names, r.randint(0, k - 1))
        undeclared = [n for n in names if n not in drops]
        if silence:
            victim = r.choice(undeclared)
            for s in arm:
                arm[s][victim] = 0.0
        else:  # declared drops go silent; undeclared may flicker on some seeds but never all off
            for d in drops:
                for s in arm:
                    arm[s][d] = 0.0
        return base, arm, {n: (lambda o, n=n: o[n] > 0) for n in names}, drops

    def co(x):
        return bool(co_ablation(x[0], x[1], x[2], x[3])[0])

    legs = dict(
        matters=G.null_harness_seeds(matters, lambda r: pair(r, 0.0), lambda r: pair(r, 3.0), n, seeds),
        co_ablated=G.null_harness_seeds(co, lambda r: act_draw(r, False), lambda r: act_draw(r, True), n, seeds),
    )
    return G.combine(known, legs)


if __name__ == "__main__":
    print("refused: library. Gate: python3 tests/test_toolkit.py ; runs: runs/run_14.py, runs/run_15.py")
    raise SystemExit(2)
