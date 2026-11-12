"""Held-out gate (chat-side follow-up to PR #258, item 1). stdlib + numpy (residual_regression).

Thresholds were frozen by hash in ledger/toolkit/HELDOUT_FREEZE.md (commit 72244bf) before
this file existed. This file was committed before its first run. It refuses to run if a
frozen tool file has changed. Each tool gets fresh planted cases and fresh null/signal
generators: different distributions, sizes and shapes from the tuning draws in each
tool's gate(), harness seeds 100-104. Run once; a FAIL sends the tool back to PROVISIONAL
and is not retuned against these sets.

Written by the same session that tuned the tools: new draws, not blind.

    python3 tests/test_heldout.py           # one line per tool and leg; exit 1 on any FAIL
"""
import hashlib, math, os, random, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from ledger.toolkit import gate as G

SEEDS = (100, 101, 102, 103, 104)
FREEZE = os.path.join(HERE, "ledger", "toolkit", "HELDOUT_FREEZE.md")


def check_freeze():
    rows = re.findall(r"^(ledger/toolkit/\S+\.py)\s+([0-9a-f]{64})$", open(FREEZE, encoding="utf-8").read(), re.M)
    bad = [p for p, h in rows if hashlib.sha256(open(os.path.join(HERE, p), "rb").read()).hexdigest() != h]
    if bad or len(rows) != 8:
        raise SystemExit(f"refused: frozen tool files changed or freeze record malformed: {bad or rows}")
    return len(rows)


def laplace(r, sd):
    b = sd / math.sqrt(2)
    u = r.random() - 0.5
    return -b * math.copysign(1, u) * math.log(1 - 2 * abs(u))


# ---------------------------------------------------------------- 1 multi_seed_ensemble
def h_mse():
    from ledger.toolkit import multi_seed_ensemble as M
    r = random.Random(201)
    base = {s: dict(a=r.uniform(-2, 2), b=r.uniform(-2, 2)) for s in range(15)}
    big = {s: dict(a=base[s]["a"] - 4.0 + laplace(r, 0.3), b=base[s]["b"]) for s in range(15)}
    known = [
        ("negative planted shift on one of two outputs: a MOVED", "MOVED", lambda: M.paired(base, big, dict(a=0.5, b=0.5))["a"]["verdict"]),
        ("the untouched output b: EXACT_ZERO", "EXACT_ZERO", lambda: M.paired(base, big, dict(a=0.5, b=0.5))["b"]["verdict"]),
        ("spike at the first index of a sweep", [0], lambda: M.variance_spike([9.0, 1.0, 1.2, 0.8, 1.1, 0.9, 1.0])),
        ("two spikes in an odd-length sweep", [2, 5], lambda: M.variance_spike([1.0, 0.9, 5.0, 1.1, 1.0, 4.5, 1.05])),
        ("all-zero sds: no spike (silent)", [], lambda: M.variance_spike([0.0, 0.0, 0.0])),
        ("uniform-noise output, sd/mean 0.3: VARIES (silent)", "VARIES",
         lambda: M.invariance([r.uniform(7, 13) for _ in range(12)])),
    ]
    legs = dict(
        moved_laplace_n15=G.null_harness_seeds(lambda ds: M.paired_one(ds)["verdict"] == "MOVED",
                                               lambda q: [laplace(q, 1.0) for _ in range(15)],
                                               lambda q: [3.0 + laplace(q, 1.0) for _ in range(15)], 200, SEEDS),
        invariant_lognormal=G.null_harness_seeds(lambda xs: M.invariance(xs) in ("INVARIANT", "CONSTANT"),
                                                 lambda q: [math.exp(q.gauss(3, 0.4)) for _ in range(8)],
                                                 lambda q: [50.0 * (1 + q.uniform(-0.01, 0.01)) for _ in range(8)], 200, SEEDS),
    )
    return G.combine(G.known_answers(known, lambda f: f()), legs)


# ---------------------------------------------------------------- 2 ablation
def h_ablation():
    from ledger.toolkit import ablation as A

    def toy(seed, ov):
        q = random.Random(seed * 31 + 7)
        w, v = ov.get("w", 1.0), ov.get("v", 1.0)
        out = dict(p=2.0 * w * w + q.uniform(-1, 1), s=0.0 * v + q.uniform(-1, 1))
        out["burn"] = (1.0 + q.random()) if (w > 0 and v > 0) else 0.0    # needs both
        return out

    act = dict(burn=lambda o: o["burn"] > 0)
    res = A.run(toy, [dict(name="w off", overrides=dict(w=0.0), drops=["w"]),
                      dict(name="v off", overrides=dict(v=0.0), drops=["v"])], range(16), delta=dict(p=0.5, s=0.5, burn=0.5), active=act)
    row = {x["name"]: x for x in res["rows"]}

    def flick(q, silence):
        names = [f"k{i}" for i in range(q.randint(2, 4))]
        base = {s: {n: 1.0 + q.random() for n in names} for s in range(12)}
        arm = {s: dict(base[s]) for s in range(12)}
        victim = q.choice(names)
        off = range(12) if silence else q.sample(range(12), q.randint(1, 11))   # null: some seeds off, never all
        for s in off:
            arm[s][victim] = 0.0
        return base, arm, {n: (lambda o, n=n: o[n] > 0) for n in names}, []

    def pair(q, shift):
        base = {s: dict(y1=q.uniform(-1.7, 1.7), y2=q.uniform(-1.7, 1.7)) for s in range(16)}
        arm = {s: dict(y1=base[s]["y1"] + q.uniform(-1.7, 1.7), y2=base[s]["y2"] + shift + q.uniform(-1.7, 1.7)) for s in range(16)}
        return base, arm

    known = [
        ("quadratic weight dropped: MATTERS", "MATTERS", lambda: row["w off"]["reading"]),
        ("weight-0 factor dropped: no output moves except the event", True, lambda: row["v off"]["per_output"]["s"]["verdict"] in ("EXACT_ZERO", "EQUIVALENT", "UNRESOLVED")),
        ("an AND-gated event silenced by either drop: CO_ABLATED by w", ["burn"], lambda: row["w off"]["co_ablated"]),
        ("and by v", ["burn"], lambda: row["v off"]["co_ablated"]),
        ("partial silencing goes to partial_co, not co_ablated", ([], ["k"]),
         lambda: A.co_ablation({s: dict(k=1.0) for s in range(4)}, {s: dict(k=0.0 if s < 2 else 1.0) for s in range(4)}, dict(k=lambda o: o["k"] > 0), [])),
    ]
    legs = dict(
        matters_uniform_two_outputs=G.null_harness_seeds(lambda x: A.compare(x[0], x[1], "d", [])["reading"] == "MATTERS",
                                                         lambda q: pair(q, 0.0), lambda q: pair(q, 3.0), 200, SEEDS),
        co_ablated_vs_flicker=G.null_harness_seeds(lambda x: bool(A.co_ablation(*x)[0]),
                                                   lambda q: flick(q, False), lambda q: flick(q, True), 200, SEEDS),
    )
    return G.combine(G.known_answers(known, lambda f: f()), legs)


# ---------------------------------------------------------------- 3 support_match
def h_support():
    from ledger.toolkit import support_match as S
    rec = dict(id="h", first_attribution="OTHER_SYSTEM", fits_question="IN_SCOPE")
    items = ("threshold", "baseline", "lattice", "sink", "valve", "horizon")
    own = ("This {i} is a term I am adding here.", "Here I introduce the {i}.", "I would add the {i} myself.")
    give = ("You said the {i} should be separate.", "Your {i} framing holds up.", "You noted the {i} earlier.",
            "As you suggested, the {i} carries it.", "You are right that the {i} matters.")

    def world(sp, line):
        return {"h.txt": (["Rook:", "context", f"{sp}:", line], None)}

    def draw(q, kind):
        i, sp = q.choice(items), q.choice(("Wren", "Kite", "Moss"))
        line = q.choice(own if kind == "own" else give).format(i=i)
        return rec, dict(credited_to=sp, item_terms=[i], support=[dict(file="h.txt", line="4")]), world(sp, line)

    def neutral(q):
        i, sp = q.choice(items), q.choice(("Wren", "Kite", "Moss"))
        line = q.choice(("Pressure readings were steady.", "Two runs were dropped.", "The log ends at noon."))
        return rec, dict(credited_to=sp, item_terms=[i], support=[dict(file="h.txt", line="4")]), world(sp, line)

    known = [
        ("speaker gives the item to its addressee: CONTRADICTS", "CONTRADICTS",
         lambda: S.verdict(rec, dict(credited_to="Wren", item_terms=["valve"], support=[dict(file="h.txt", line="4")]), world("Wren", "Your valve point is the key."))),
        ("same line spoken by someone other than the credited source: not CONTRADICTS (silent)", True,
         lambda: S.verdict(rec, dict(credited_to="Kite", item_terms=["valve"], support=[dict(file="h.txt", line="4")]), world("Wren", "Your valve point is the key.")) != "CONTRADICTS"),
        ("two support lines, one names the item in own voice: MATCHES (silent)", "MATCHES",
         lambda: S.verdict(rec, dict(credited_to="Wren", item_terms=["sink"], support=[dict(file="h.txt", line="2"), dict(file="h.txt", line="4")]),
                           {"h.txt": (["Wren:", "Logs only.", "Wren:", "I add the sink term."], None)})),
        ("item term matched case-insensitively", "CONTRADICTS",
         lambda: S.verdict(rec, dict(credited_to="Wren", item_terms=["Horizon"], support=[dict(file="h.txt", line="4")]), world("Wren", "As you said, the horizon moves."))),
    ]
    legs = dict(
        contradicts_new_phrasings=G.null_harness_seeds(lambda x: S.unsupported_assignment(*x), lambda q: draw(q, "own"), lambda q: draw(q, "give"), 200, SEEDS),
        silent_on_claim_new_basis=G.null_harness_seeds(lambda x: S.unsupported_assignment(*x), lambda q: draw(q, "own"), neutral, 200, SEEDS),
    )
    return G.combine(G.known_answers(known, lambda f: f()), legs)


# ---------------------------------------------------------------- 4 parameter_recovery
def h_recovery():
    from ledger.toolkit import parameter_recovery as P
    grid = [0.5, 0.75, 1.0, 1.25, 1.5]

    def model(fn, off, k, noise, bias=0.0):
        def f(theta, seed, data=False):
            q = random.Random(off + seed)
            return {f"o{i}": fn(theta, i) + (bias if data else 0.0) + laplace(q, noise) for i in range(k)}
        return f

    def run(f, data=None, truth=1.0):
        data = data or f
        obs = [data(truth, s, True) if data is f else data(truth, s) for s in range(200, 208)]
        fit = {g: [f(g, s) for s in range(12)] for g in grid}
        p = P.profile(obs, fit, grid, truth)
        return P.verdict(p["chi2"], grid, truth)[0]

    expo = model(lambda th, i: 5.0 * math.exp(th) * (i + 1), 1, 3, 1.0)
    sat = model(lambda th, i: 4.0 * math.tanh(30 * (th - 0.2)), 2, 3, 0.5)     # saturated over the whole grid
    bias = model(lambda th, i: 8.0 * th * (i + 1), 3, 3, 0.5, bias=3.0)

    def drawf(q, strength):
        off, k, noise = q.randint(0, 10 ** 6), q.randint(2, 4), q.uniform(0.3, 1.5)
        return model(lambda th, i: strength * th * th * (i + 2), off, k, noise)

    known = [
        ("exponential dependence: RECOVERED", "RECOVERED", lambda: run(expo)),
        ("dependence saturated across the grid: NOT_IDENTIFIABLE (silent)", "NOT_IDENTIFIABLE", lambda: run(sat)),
        ("data offset the model lacks: BIASED", "BIASED", lambda: run(bias)),
    ]
    legs = dict(recovered_quadratic_laplace=G.null_harness_seeds(lambda f: run(f) == "RECOVERED",
                                                                 lambda q: drawf(q, 0.0), lambda q: drawf(q, 10.0), 200, SEEDS))
    return G.combine(G.known_answers(known, lambda f: f()), legs)


# ---------------------------------------------------------------- 5 residual_regression
def h_residual():
    from ledger.toolkit import residual_regression as R

    def rows(q, n, kind):
        out = []
        for _ in range(n):
            m1, m2, m3 = q.uniform(0, 1), q.uniform(0, 1), q.uniform(0, 1)
            b1, b2 = q.uniform(0, 1), q.uniform(0, 1)
            y = {"method": 3 * m2 * m2 + 2 * m3, "biology": 3 * b1 * b1 + 2 * b2, "none": 0.0}[kind] + q.expovariate(2.0)
            out.append(dict(m1=m1, m2=m2, m3=m3, b1=b1, b2=b2, y=y))
        return out

    q0 = random.Random(301)
    V = lambda rs: R.fit(rs, "y", ["m1", "m2", "m3"], ["b1", "b2"], n_perm=200)["verdict"]
    known = [
        ("nonlinear method drive, three method columns: METHOD_ARTIFACT", "METHOD_ARTIFACT", lambda: V(rows(q0, 45, "method"))),
        ("nonlinear biology drive: BIOLOGY", "BIOLOGY", lambda: V(rows(q0, 45, "biology"))),
        ("skewed noise only: UNEXPLAINED (silent)", "UNEXPLAINED", lambda: V(rows(q0, 45, "none"))),
    ]
    det = lambda rs: R.fit(rs, "y", ["m1", "m2", "m3"], ["b1", "b2"], n_perm=150)["verdict"] in ("METHOD_ARTIFACT", "MIXED")
    legs = dict(method_explains_nonlinear=G.null_harness_seeds(det, lambda q: rows(q, 35, "biology"), lambda q: rows(q, 35, "method"), 40, SEEDS))
    return G.combine(G.known_answers(known, lambda f: f()), legs)


# ---------------------------------------------------------------- 6 equation_family_swap (handoff only; engine-independent)
def h_swap():
    from ledger.toolkit import equation_family_swap as E

    def curve(xs, f, sd, q, noise):
        return [dict(x=x, mean=f(x) + noise(q, sd), sd=sd) for x in xs]

    xs = [i / 30 for i in range(31)]
    gq = lambda q, sd: q.gauss(0, sd)
    lq = lambda q, sd: laplace(q, sd)
    q0 = random.Random(401)
    a = curve(xs, lambda x: x * x, 0.1, q0, gq)
    band = curve(xs, lambda x: x * x + (2.0 if 0.3 < x < 0.7 else 0.0), 0.1, q0, gq)
    known = [
        ("disagreement only in the middle of the sweep: two handoffs", 2, lambda: len(E.handoff(a, band)["handoffs"])),
        ("a two-point run is below MIN_RUN 3: no regime (silent)", [],
         lambda: E.handoff([dict(x=i, mean=0.0, sd=0.1) for i in range(10)],
                           [dict(x=i, mean=(3.0 if i in (4, 5) else 0.0), sd=0.1) for i in range(10)])["handoffs"]),
        ("mismatched sweeps refused", True, lambda: _raises(lambda: E.handoff(a, a[:-1]), E.AdapterError)),
    ]

    def pair(q, gap):
        sd = q.uniform(0.05, 0.3)
        cut = q.choice(xs[8:23])
        A = curve(xs, lambda x: math.sin(3 * x), sd, q, lq)
        B = curve(xs, lambda x: math.sin(3 * x) + (gap * sd * 10 if x > cut else 0.0), sd, q, lq)
        return A, B

    legs = dict(handoff_laplace_31pt=G.null_harness_seeds(lambda c: bool(E.handoff(*c)["handoffs"]),
                                                         lambda q: pair(q, 0.0), lambda q: pair(q, 1.0), 200, SEEDS))
    return G.combine(G.known_answers(known, lambda f: f()), legs)


def _raises(f, exc):
    try:
        f()
    except exc:
        return True
    return False


# ---------------------------------------------------------------- 7 assumption_block_trace
def h_trace():
    from ledger.toolkit import assumption_block_trace as T

    def studies(q, n, enrich):
        out = []
        for i in range(n):
            blocks = [b for b in ("AB_P", "AB_Q", "AB_R") if q.random() < 1 / 3]
            p = (0.6 if "AB_Q" in blocks else 0.1) if enrich else 0.2
            out.append(dict(id=f"s{i}", blocks=blocks, outcome="FAILED" if q.random() < p else "HELD"))
        return out

    q0 = random.Random(501)
    planted = studies(q0, 120, True)
    known = [
        ("enrichment on AB_Q among three blocks: AB_Q SHARED_FAILURE", "SHARED_FAILURE", lambda: T.trace(planted)["AB_Q"]["verdict"]),
        ("AB_P carries no enrichment: not SHARED_FAILURE (silent)", True, lambda: T.trace(planted)["AB_P"]["verdict"] != "SHARED_FAILURE"),
        ("failures concentrated on NON-users: not SHARED_FAILURE (one-sided, silent)", True,
         lambda: T.trace([dict(id=f"x{i}", blocks=(["AB_Z"] if i < 10 else []), outcome=("HELD" if i < 10 else "FAILED")) for i in range(20)])["AB_Z"]["verdict"] != "SHARED_FAILURE"),
        ("seven known outcomes plus five UNKNOWN: INSUFFICIENT", "INSUFFICIENT",
         lambda: T.trace([dict(id=f"y{i}", blocks=(["AB_Z"] if i % 2 else []), outcome=("FAILED" if i < 4 else "HELD")) for i in range(7)]
                         + [dict(id=f"u{i}", blocks=["AB_Z"], outcome="UNKNOWN") for i in range(5)])["AB_Z"]["verdict"]),
    ]
    det = lambda st: T.trace(st, ["AB_Q"])["AB_Q"]["verdict"] == "SHARED_FAILURE"
    legs = dict(shared_failure_three_blocks_n80=G.null_harness_seeds(det, lambda q: studies(q, 80, False), lambda q: studies(q, 80, True), 200, SEEDS))
    return G.combine(G.known_answers(known, lambda f: f()), legs)


HELDOUT = dict(multi_seed_ensemble=h_mse, ablation=h_ablation, support_match=h_support, parameter_recovery=h_recovery,
               residual_regression=h_residual, equation_family_swap=h_swap, assumption_block_trace=h_trace)


if __name__ == "__main__":
    print(f"freeze verified: {check_freeze()} files unchanged since commit 22a42e2")
    bad = 0
    for t, fn in HELDOUT.items():
        g = fn()
        s = G.summary(g)
        print(f"{s['verdict']:4s}  {t:24s} held-out known {s['known_answer']}")
        for r in g["known"]["rows"]:
            if not r["ok"]:
                print(f"      BAD {r['name']}: expect {r['expect']!r} got {r['got']!r}")
        for leg, line in s["null_legs"].items():
            print(f"      {'':24s} null[{leg}] {line}")
        bad += s["verdict"] != "PASS"
    print(f"{len(HELDOUT)} tools held out, {bad} failed")
    sys.exit(1 if bad else 0)
