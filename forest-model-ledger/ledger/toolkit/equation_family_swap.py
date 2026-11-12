"""Toolkit: equation_family_swap -- ADAPTER ONLY. Tool #6 of the staged build (work order 2026-11-11).

Entry: ledger/toolkit/equation_family_swap.yaml. Gate: tests/test_toolkit.py.

The work order places the engine in the relational-playground: "equation_family_swap ->
relational-playground engine; toolkit entry points to it". This file is the adapter: it
finds the engine, hands it a component and a sweep, and compares the families' answers.
It contains no equation family of its own.

ENGINE STATE, checked 2026-11-11: no `relational-playground` in this tree, on any branch of
JinnZ2/Simulators, or among the repositories this session can list. resolve() returns
ENGINE_ABSENT with every path it looked at. No substitute engine is built here: a family
swap run on an engine written in the same session that reads its result would be the
session agreeing with itself.

  resolve(paths=None)         search order: $RELATIONAL_PLAYGROUND_PATH, ../relational-playground
                              (sibling of the Simulators checkout), <repo>/relational-playground.
                              An engine is a directory with engine.py exposing
                              run_family(family, component, sweep) -> [{"x", "mean", "sd"}].
  swap(component, families, sweep, engine)
                              one call per family; a family outside the brief's list is refused
  handoff(a, b, k)            adapter-local: the sweep points where two families disagree beyond
                              k * sqrt(sd_a^2 + sd_b^2); a REGIME of disagreement is a run of at
                              least MIN_RUN consecutive such points, and a handoff is where a
                              regime starts or ends            [CHOICE: K_HANDOFF 3, MIN_RUN 3]
                              Gate history: the first version flagged a handoff at every flip of
                              a single point and failed FP (0.07 on 21-point sweeps: one K=3
                              exceedance in 21 is ordinary noise). A regime is a stretch of the
                              sweep, not a point; MIN_RUN encodes that and is stated as a choice.

FAMILIES is read out of the METHOD BRIEF's toolbox line in forest-model-ledger/CLAUDE.md,
not retyped; a brief edited to another list changes it.
"""
import importlib.util, math, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
K_HANDOFF, MIN_RUN = 3.0, 3
CHOICES = dict(K_HANDOFF=K_HANDOFF, MIN_RUN=MIN_RUN)


class AdapterError(ValueError):
    pass


def brief_families(path=os.path.join(HERE, "CLAUDE.md")):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"equation-family swap \((.*?)\)\s*", text, re.S)
    if not m:
        raise AdapterError("METHOD BRIEF has no equation-family swap line")
    return tuple(f.strip() for f in re.sub(r"\s+", " ", m.group(1)).split("|"))


FAMILIES = brief_families()


def default_paths():
    repo = os.path.dirname(HERE)
    out = []
    if os.environ.get("RELATIONAL_PLAYGROUND_PATH"):
        out.append(os.environ["RELATIONAL_PLAYGROUND_PATH"])
    out += [os.path.join(os.path.dirname(repo), "relational-playground"), os.path.join(repo, "relational-playground")]
    return out


def resolve(paths=None):
    looked = list(paths if paths is not None else default_paths())
    for p in looked:
        f = os.path.join(p, "engine.py")
        if os.path.isfile(f):
            spec = importlib.util.spec_from_file_location("relational_playground_engine", f)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            if not hasattr(mod, "run_family"):
                return dict(state="ENGINE_MALFORMED", path=p, looked=looked, engine=None)
            return dict(state="ENGINE_FOUND", path=p, looked=looked, engine=mod)
    return dict(state="ENGINE_ABSENT", path=None, looked=looked, engine=None)


def swap(component, families, sweep, engine=None):
    eng = engine if engine is not None else resolve()
    if eng["state"] != "ENGINE_FOUND":
        return dict(state=eng["state"], looked=eng["looked"], results=None)
    bad = [f for f in families if f not in FAMILIES]
    if bad:
        raise AdapterError(f"families not in the METHOD BRIEF list: {bad}")
    results = {f: eng["engine"].run_family(f, component, list(sweep)) for f in families}
    return dict(state="RAN", looked=eng["looked"], path=eng["path"], results=results)


def handoff(a, b, k=K_HANDOFF):
    """a, b: lists of {x, mean, sd} on the same sweep."""
    if [p["x"] for p in a] != [p["x"] for p in b]:
        raise AdapterError("handoff needs the two families on the same sweep")
    dis = [abs(p["mean"] - q["mean"]) > k * math.sqrt(p["sd"] ** 2 + q["sd"] ** 2) for p, q in zip(a, b)]
    regime, i = [False] * len(dis), 0
    while i < len(dis):
        j = i
        while j < len(dis) and dis[j]:
            j += 1
        if j - i >= MIN_RUN:
            regime[i:j] = [True] * (j - i)
        i = j + 1 if j == i else j
    flips = [a[i]["x"] for i in range(1, len(regime)) if regime[i] != regime[i - 1]]
    return dict(disagree_at=[p["x"] for p, d in zip(a, dis) if d], regime_at=[p["x"] for p, d in zip(a, regime) if d], handoffs=flips)


# ---------------------------------------------------------------- gate: planted cases + null harness
def _stub_engine():
    """PLANTED test engine: two toy 'families' that agree below x = 0.5 and split above."""
    class Stub:
        @staticmethod
        def run_family(family, component, sweep):
            split = 0.0 if family == FAMILIES[0] else 4.0
            return [dict(x=x, mean=x + (split if x > 0.5 else 0.0), sd=0.2) for x in sweep]
    return dict(state="ENGINE_FOUND", path="<planted stub>", looked=["<planted stub>"], engine=Stub)


def known_cases():
    sweep = [i / 10 for i in range(11)]
    stub = _stub_engine()
    ran = swap("L4_FIRE_MEANFIELD_ODE", FAMILIES[:2], sweep, engine=stub)
    return [
        ("brief families parsed: seven", 7, lambda: len(FAMILIES)),
        ("no engine on the path: ENGINE_ABSENT, nothing returned", ("ENGINE_ABSENT", None),
         lambda: (lambda r: (r["state"], r["results"]))(swap("x", FAMILIES[:1], sweep, engine=resolve(["/nonexistent/rp"])))),
        ("planted engine is called once per family", sorted(FAMILIES[:2]), lambda: sorted(ran["results"])),
        ("family outside the brief is refused", True, lambda: _raises(lambda: swap("x", ["lattice gas"], sweep, engine=stub))),
        ("planted split above 0.5: one handoff at x 0.6", [0.6], lambda: handoff(ran["results"][FAMILIES[0]], ran["results"][FAMILIES[1]])["handoffs"]),
        ("a single-point disagreement is not a regime (silent)", [], lambda: handoff(
            [dict(x=i, mean=0.0, sd=0.1) for i in range(9)], [dict(x=i, mean=(5.0 if i == 4 else 0.0), sd=0.1) for i in range(9)])["handoffs"]),
        ("identical families: no handoff (silent)", [], lambda: handoff(ran["results"][FAMILIES[0]], ran["results"][FAMILIES[0]])["handoffs"]),
        ("default search finds no engine in this checkout", "ENGINE_ABSENT", lambda: resolve()["state"]),
    ]


def _raises(f):
    try:
        f()
    except AdapterError:
        return True
    return False


def gate(n=200, seeds=(0, 1, 2, 3, 4)):
    from ledger.toolkit import gate as G
    known = G.known_answers(known_cases(), lambda f: f())

    def curves(r, gap):
        xs = [i / 20 for i in range(21)]
        cut = r.choice(xs[5:16])
        a = [dict(x=x, mean=x + r.gauss(0, 0.2), sd=0.2) for x in xs]
        b = [dict(x=x, mean=x + (gap if x > cut else 0.0) + r.gauss(0, 0.2), sd=0.2) for x in xs]
        return a, b

    legs = dict(handoff=G.null_harness_seeds(lambda c: bool(handoff(*c)["handoffs"]), lambda r: curves(r, 0.0),
                                             lambda r: curves(r, 3.0), n, seeds))
    return G.combine(known, legs)


if __name__ == "__main__":
    r = resolve()
    print(f"engine: {r['state']}; looked at:")
    for p in r["looked"]:
        print("  ", p)
    print("families (from the METHOD BRIEF):", FAMILIES)
