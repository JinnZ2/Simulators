"""G5 item 9: continuity identity ("the same thing" across time), three branches, no winner
(9c VOID-9, BRANCHED; DECIDED on evidence 2026-11-18: D2 with a declared sliver bound).

C-A  EXACT STATE  sha256 of the declared state matches the anchor's.
C-B  TOLERANCE    every declared variable within its declared tolerance of the anchor
                  (M8 continuity.return_to_anchor, reused).
C-C  LINEAGE      an unbroken chain of recorded transitions from the anchor to the state.
       C-C0       (first build, kept as history) each transition verified by replaying its own
                  recorded function: a rounding or summary step replays exactly, so it verifies.
       C-C        (fixed, evidence round) each transition verified by replay against the EXACT
                  trajectory: its output must equal the exact trajectory's state at that point.
                  A rounding or summary step leaves the trajectory, so it does not verify.
D    CLASS-CONDITIONED (evidence round) T4 class of the snapshot (snapshot_class.py,
                  Geometric-to-Binary-Computational-Bridge @85f3302) picks the criterion:
                    CONTEXT_FREE_EXACT -> C-A        STABLE_LOSSY  -> C-B
                    CHAOTIC_REFRESH    -> exact-only (C-A)   SUMMARY_ONLY -> NOT_SAME
                  growth = error at the horizon / error injected, MEASURED once per system at a
                  declared reference snapshot (T4: "one horizon on one system decides the class").
                  Broken by case 5 (global class).
D2   BASIN MARGIN WITH A DECLARED SLIVER BOUND (order 2026-11-18). A sampled check cannot prove
                  "no sliver"; it can only bound one, and the verdict says so. Purpose inputs f_min
                  (smallest sliver that matters) and alpha (acceptable miss rate); missing ->
                  UNTESTED. N = ceil(ln alpha / ln(1 - f_min)) points are sampled uniformly in the
                  ball of radius tol around the anchor (seeded) and run to the horizon:
                    any sample with growth > 1  -> NOT_SAME (one sample is proof)
                    zero hits in N              -> SAME_WITH_BOUND: any sliver is < f_min at
                                                   confidence 1 - alpha (rule of three: < 3/N at 95%)
                  Exact and summary snapshots are decided by class, as D.
D2m  EXACT MARGIN, only where a case declares its separatrix (double well: the saddle's stable
                  manifold, traced): margin > tol -> SAME; margin <= tol -> NOT_SAME; no sampling.
                  Sampling is for systems whose boundary is unknown.
Source pattern for the basin-margin rule: oral-tradition glyph #4 (repose: rest is conditional,
still loaded), relayed in chat; not in a repository.
"""
import hashlib
import math
import random
from collections import namedtuple

from . import continuity as M8

Transition = namedtuple("Transition", "name input_hash output_hash replay")


def h(state):
    return hashlib.sha256(repr(state).encode("utf-8")).hexdigest()


def c_exact(anchor, state):
    return "SAME" if h(anchor) == h(state) else "NOT_SAME"


def c_tolerance(anchor_vars, state_vars, tolerance):
    r = M8.return_to_anchor(M8.Anchor("a", anchor_vars), state_vars, tolerance=tolerance)
    return "SAME" if r.state == "OK" else "NOT_SAME"


def c_lineage(anchor, state, chain, states, exact=None):
    """states: {hash: state} recorded along the chain. With `exact` ({hash_in: exact_next_state}) a
    transition verifies only when its output equals the exact trajectory's state (fixed C-C);
    without it, by replaying its own recorded function (C-C0, history)."""
    if not chain or chain[0].input_hash != h(anchor) or chain[-1].output_hash != h(state):
        return "NOT_SAME"
    for prev, nxt in zip(chain, chain[1:]):
        if prev.output_hash != nxt.input_hash:
            return "NOT_SAME"
    for t in chain:
        if t.input_hash not in states or h(t.replay(states[t.input_hash])) != t.output_hash:
            return "NOT_SAME"
        if exact is not None and (t.input_hash not in exact or h(exact[t.input_hash]) != t.output_hash):
            return "NOT_SAME"
    return "SAME"


T4_CLASSES = ("CONTEXT_FREE_EXACT", "STABLE_LOSSY", "CHAOTIC_REFRESH", "SUMMARY_ONLY")
GROWTH_LIMIT = 1.0          # T4's definition, snapshot_class.py


def t4_class(content, fidelity, growth=None):
    if content == "SUMMARY":
        return "SUMMARY_ONLY"
    if fidelity == "EXACT":
        return "CONTEXT_FREE_EXACT"
    if growth is None:
        return None             # T4: growth not given -> VOID, never assumed
    return "STABLE_LOSSY" if growth <= GROWTH_LIMIT else "CHAOTIC_REFRESH"


def c_class(t4, anchor, state, vars_):
    if t4 is None:
        return "VOID"
    if t4 in ("CONTEXT_FREE_EXACT", "CHAOTIC_REFRESH"):
        return c_exact(anchor, state)
    if t4 == "STABLE_LOSSY":
        return c_tolerance(*vars_)
    return "NOT_SAME"


# --- systems --------------------------------------------------------------------------------
def fib_word(level):
    w = "a"
    for _ in range(level):
        w = "".join("ab" if c == "a" else "a" for c in w)
    return w


def counts(w):
    return (w.count("a"), w.count("b"))


def _rk4(f, s, dt, n):
    for _ in range(n):
        k1 = f(s)
        k2 = f(tuple(a + dt / 2 * b for a, b in zip(s, k1)))
        k3 = f(tuple(a + dt / 2 * b for a, b in zip(s, k2)))
        k4 = f(tuple(a + dt * b for a, b in zip(s, k3)))
        s = tuple(a + dt / 6 * (p + 2 * q + 2 * r + t) for a, p, q, r, t in zip(s, k1, k2, k3, k4))
    return s


def spiral(s):
    x, y = s
    return (-0.1 * x - y, x - 0.1 * y)


def lorenz(s):
    x, y, z = s
    return (10.0 * (y - x), x * (28.0 - z) - y, x * y - 8.0 / 3.0 * z)


def round3(s):
    return tuple(round(v, 3) for v in s)


def double_well(s):
    """Damped double well x'' = x - x^3 - 0.5 x': two stable sinks at x = +-1, separatrix through 0."""
    x, v = s
    return (v, x - x ** 3 - 0.5 * v)


def round1(s):
    return tuple(round(v, 1) for v in s)


def _dist(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))


def _growth(f, anchor, snap, dt=0.01, n=3000):
    return _dist(_rk4(f, anchor, dt, n), _rk4(f, snap, dt, n)) / _dist(anchor, snap)


def _ode_case(name, f, s0, ebr, band, *, anchor=None, rnd=round3, tol=1e-3, ref=None,
              dt=0.01, n=3000, lossy="round"):
    anchor = _rk4(f, s0, dt, 1500) if anchor is None else anchor   # t = 15 s by default
    snap = rnd(anchor)
    true_end = _rk4(f, anchor, dt, n)            # 30 s horizon
    res_end = _rk4(f, snap, dt, n)
    e0 = _dist(anchor, snap)
    ratio = _dist(true_end, res_end) / e0
    outcome = "SAME" if ratio <= band else "NOT_SAME"
    names = "xyz"[:len(anchor)]
    chain = [Transition(lossy, h(anchor), h(snap), rnd)]
    ra, rs = ref if ref is not None else (anchor, snap)
    growth = _growth(f, ra, rs, dt, n)
    return {"case": name, "anchor": anchor, "state": snap,
            "vars": (dict(zip(names, anchor)), dict(zip(names, snap)), {n: tol for n in names}),
            "chain": chain, "states": {h(anchor): anchor}, "exact": {h(anchor): anchor},
            "t4": t4_class("FULL_STATE", "LOSSY", growth), "class_growth": growth,
            "class_ref": "the case's own snapshot" if ref is None else "declared reference snapshot",
            "measured": "error ratio %.4g vs band %g" % (ratio, band), "outcome": outcome,
            "ratio": ratio, "ebr": ebr, "f": f, "dt": dt, "n": n, "radius": tol}


def cases():
    a10 = fib_word(10)
    snap = str(a10)
    fib_resumed = fib_word(15) == _extend(snap, 5)
    out = [{"case": "fib_exact", "anchor": a10, "state": snap,
            "vars": (dict(zip("ab", counts(a10))), dict(zip("ab", counts(snap))), {"a": 0, "b": 0}),
            "chain": [Transition("store word verbatim", h(a10), h(snap), lambda w: str(w))],
            "states": {h(a10): a10}, "exact": {h(a10): a10},
            "t4": t4_class("FULL_STATE", "EXACT"), "class_growth": None, "class_ref": "--",
            "measured": "level-15 resume equals uninterrupted: %s" % fib_resumed,
            "outcome": "SAME" if fib_resumed else "NOT_SAME",
            "ebr": "EBR_016: 0 mismatched levels of 26; RK4 exact resume bitwise"}]
    out.append(_ode_case("spiral_lossy", spiral, (1.0, 0.0),
                         "EBR_017: ratio 0.0498 inside band [0, 3] (band UNSOURCED)", 3.0))
    out.append(_ode_case("lorenz_lossy", lorenz, (1.0, 1.0, 1.0),
                         "EBR_018: ratio 16980 vs band 100, needs refresh (band UNSOURCED)", 100.0))
    w8 = fib_word(8)
    c8 = counts(w8)
    out.append({"case": "counts_word", "anchor": w8, "state": c8,
                "vars": (dict(zip("ab", counts(w8))), dict(zip("ab", c8)), {"a": 0, "b": 0}),
                "chain": [Transition("summarise as letter counts", h(w8), h(c8), counts)],
                "states": {h(w8): w8}, "exact": {h(w8): w8},
                "t4": t4_class("SUMMARY", None), "class_growth": None, "class_ref": "--",
                "measured": "counts %s fit C(55,21) = %d words; no decoder" % (c8, math.comb(55, 21)),
                "outcome": "NOT_SAME",
                "ebr": "EBR_019: counts (34, 21) fit 841,728,816,603,675 words; verdict void"})
    # fifth case, built to try to break D: a stable (dissipative) system whose class is measured at a
    # reference snapshot deep in one basin (STABLE_LOSSY), snapshotted near the separatrix and kept
    # at a tolerance (0.1) loose enough to admit 1-dp rounding.
    near = (0.044, -0.056)          # rounds to (0.0, -0.1): within tol 0.1, but the other basin
    deep = (0.9, 0.05)
    out.append(_ode_case("bistable_loose", double_well, None,
                         "constructed here, no EBR claim; band [0, 3] as EBR_017", 3.0,
                         anchor=near, rnd=round1, tol=0.1, ref=(deep, round1(deep))))
    out[-1]["separatrix"] = _stable_manifold
    # sixth case, built to try to break D2: a tolerance ball almost entirely in one basin with a thin
    # sliver (about 2.5 %) across the separatrix; the lossy snapshot is a declared point in the sliver.
    sl = sliver_snapshot()
    out.append(_ode_case("bistable_sliver", double_well, None,
                         "constructed here, no EBR claim; band [0, 3] as EBR_017", 3.0,
                         anchor=SLIVER_ANCHOR, rnd=lambda _a: sl, tol=SLIVER_R,
                         ref=(deep, round1(deep)), dt=0.05, n=600, lossy="lossy encode (declared point)"))
    out[-1]["separatrix"] = _stable_manifold
    return out


SLIVER_ANCHOR = (0.06, -0.01)
SLIVER_R = 0.05
SLIVER_F_EXACT = 0.04362    # sliver_fraction_exact(M=200); recorded, recomputed in the tests at M 40
DIRECT_RUN = {"trials": 10000, "miss": 62, "seed": 2026, "N": 113}   # direct_miss(10000, 113): 386 s
F_MIN = 0.04               # purpose inputs declared for the table run (order 2026-11-18)
ALPHA = 0.01


def _basin(p, dt=0.05, n=600):
    return 1 if _rk4(double_well, p, dt, n)[0] > 0 else -1


def _ball(c, r, rng):
    while True:
        d = [rng.uniform(-r, r) for _ in c]
        if sum(x * x for x in d) <= r * r:
            return tuple(a + b for a, b in zip(c, d))


def sliver_snapshot(seed=7):
    """First seeded ball point (radius SLIVER_R) whose basin differs from the anchor's."""
    rng, home = random.Random(seed), _basin(SLIVER_ANCHOR)
    while True:
        p = _ball(SLIVER_ANCHOR, SLIVER_R, rng)
        if _basin(p) != home:
            return p


def n_required(f_min, alpha):
    """Samples needed so that a sliver of fraction >= f_min is missed with probability <= alpha."""
    return int(math.ceil(math.log(alpha) / math.log(1.0 - f_min)))


D2Verdict = namedtuple("D2Verdict", "state f_min alpha N hits reason")


def _purpose(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and 0.0 < x < 1.0


def d2_bound(c, f_min=None, alpha=None, seed=0):
    """D2 with a declared sliver bound. f_min (smallest sliver that matters) and alpha (acceptable
    miss rate) are purpose inputs; missing -> UNTESTED. N = ceil(ln alpha / ln(1 - f_min)).
    Zero hits -> SAME_WITH_BOUND (any sliver is < f_min at confidence 1 - alpha); any hit ->
    NOT_SAME (one crossing sample is proof)."""
    if f_min is None or alpha is None:
        return D2Verdict("UNTESTED", f_min, alpha, None, None, "f_min and alpha are declared purpose inputs")
    if not (_purpose(f_min) and _purpose(alpha)):
        raise ValueError("f_min and alpha are numbers in (0, 1)")
    av, sv, tol = c["vars"]
    if c["t4"] in ("CONTEXT_FREE_EXACT", "SUMMARY_ONLY") or c.get("f") is None:
        st = c_class(c["t4"], c["anchor"], c["state"], (av, sv, tol))
        return D2Verdict(st, f_min, alpha, None, None, "%s: decided by class, no sampling" % c["t4"])
    N = n_required(f_min, alpha)
    rng = random.Random(seed)
    a, f, dt, n = c["anchor"], c["f"], c["dt"], c["n"]
    end_a = _rk4(f, a, dt, n)
    for k in range(N):
        p = _ball(a, c["radius"], rng)
        if _dist(_rk4(f, p, dt, n), end_a) / _dist(p, a) > GROWTH_LIMIT:
            return D2Verdict("NOT_SAME", f_min, alpha, N, 1,
                             "sample %d of %d grows (growth > 1): proof, not an estimate" % (k + 1, N))
    if c_tolerance(av, sv, tol) != "SAME":
        return D2Verdict("NOT_SAME", f_min, alpha, N, 0, "no crossing, but the snapshot is outside tol")
    return D2Verdict("SAME_WITH_BOUND", f_min, alpha, N, 0,
                     "0 hits in %d: any sliver is < %g of the ball at confidence %g "
                     "(rule of three: < %.3g at 95%%)" % (N, f_min, 1 - alpha, 3.0 / N))


def _stable_manifold(eps=1e-6, dt=0.001, rmax=1.5, steps=40000):
    """Double well: trace the saddle's stable manifold by integrating the reversed flow from the
    saddle along its stable eigenvector. Returns the two branches as separate point lists (joining
    them would add a false segment from one branch's far end back to the other's start)."""
    lam = (-0.5 - math.sqrt(0.25 + 4.0)) / 2.0            # stable eigenvalue of [[0,1],[1,-0.5]]
    back = lambda s: tuple(-v for v in double_well(s))
    branches = []
    for sign in (1, -1):
        p, pts = (sign * eps, sign * eps * lam), []
        for _ in range(steps):
            pts.append(p)
            p = _rk4(back, p, dt, 1)
            if math.hypot(*p) > rmax:
                break
        branches.append(pts)
    return branches


def margin_to(branches, a):
    best = float("inf")
    for points in branches:
        best = min(best, _poly_dist(points, a))
    return best


def _poly_dist(points, a):
    best = float("inf")
    for p, q in zip(points, points[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((a[0] - p[0]) * dx + (a[1] - p[1]) * dy) / L2))
        best = min(best, math.hypot(a[0] - p[0] - t * dx, a[1] - p[1] - t * dy))
    return best


def d2_margin(c):
    """Exact-margin path, only where the case declares its separatrix: margin > tol -> SAME,
    margin <= tol -> NOT_SAME; no sampling. Undeclared -> NOT_DECLARED (use the sampled bound)."""
    if not c.get("separatrix"):
        return "NOT_DECLARED", None
    m = margin_to(c["separatrix"](), c["anchor"])
    return ("SAME" if m > c["radius"] else "NOT_SAME"), m


def miss_table(Ns=(1, 2, 4, 8, 16, 32, 64, 128, 256), trials=400, pool=2000, seed=11):
    """Case 6: how often N ball samples miss the sliver. A pool of labelled ball points is drawn once
    (seeded); each trial draws N points from it. Measured miss rate beside (1 - f_hat)^N."""
    rng = random.Random(seed)
    home = _basin(SLIVER_ANCHOR)
    labels = [_basin(_ball(SLIVER_ANCHOR, SLIVER_R, rng)) != home for _ in range(pool)]
    f_hat = sum(labels) / float(pool)
    rows = []
    for N in Ns:
        miss = sum(not any(labels[rng.randrange(pool)] for _ in range(N)) for _ in range(trials))
        rows.append({"N": N, "miss_rate": miss / float(trials), "predicted": (1 - f_hat) ** N})
    return {"f_hat": f_hat, "pool": pool, "trials": trials, "rows": rows}


def f_threshold(N, alpha):
    """Smallest sliver fraction a run of N independent samples misses with probability <= alpha."""
    return 1.0 - alpha ** (1.0 / N)


def sliver_fraction_exact(M=200, bisect=40, dt=0.05, axis=0):
    """Case 6: the sliver's share of the ball, by chord integration (no sampling). M chords across
    the ball; on each, the basin boundary is located by bisection on the classifier. axis 0 = vertical
    chords, 1 = horizontal; the two orientations are an internal check. Raises on a chord crossing the
    boundary more than once (the single-crossing assumption is checked, not taken)."""
    ax, ay = SLIVER_ANCHOR
    r = SLIVER_R
    e1, e2 = ((1, 0), (0, 1)) if axis == 0 else ((0, 1), (-1, 0))

    def basin(q):
        return 1 if _rk4(double_well, q, dt, int(round(30 / dt)))[0] > 0 else -1
    home, tot = basin(SLIVER_ANCHOR), 0.0
    for i in range(M):
        u = -r + (i + 0.5) * 2 * r / M
        half = math.sqrt(r * r - u * u)
        at = lambda t: (ax + u * e1[0] + t * e2[0], ay + u * e1[1] + t * e2[1])
        ts = [-half + 2 * half * k / 8.0 for k in range(9)]
        bs = [basin(at(t)) for t in ts]
        cross = [k for k in range(8) if bs[k] != bs[k + 1]]
        if len(cross) > 1:
            raise ValueError("chord u=%g crosses the boundary %d times" % (u, len(cross)))
        if not cross:
            tot += 2 * half if bs[0] != home else 0.0
            continue
        lo, hi, blo = ts[cross[0]], ts[cross[0] + 1], bs[cross[0]]
        for _ in range(bisect):
            m = (lo + hi) / 2
            lo, hi = (m, hi) if basin(at(m)) == blo else (lo, m)
        c = (lo + hi) / 2
        tot += (c + half) if blo != home else (half - c)
    return tot * (2 * r / M) / (math.pi * r * r)


def direct_miss(trials, N, seed=2026):
    """Case 6: trials each draw N FRESH ball points (no pool) and stop at the first hit. A miss is a
    trial with no hit. Unlike miss_table, this samples the ball, not a fixed labelled pool."""
    rng, home, miss = random.Random(seed), _basin(SLIVER_ANCHOR), 0
    for _ in range(trials):
        if not any(_basin(_ball(SLIVER_ANCHOR, SLIVER_R, rng)) != home for _ in range(N)):
            miss += 1
    return miss


def _extend(word, levels):
    for _ in range(levels):
        word = "".join("ab" if c == "a" else "a" for c in word)
    return word


_TABLE = []


def table():
    """Deterministic; computed once per process (the D2 sampling is the slow part)."""
    if _TABLE:
        return _TABLE[0]
    rows = _table()
    _TABLE.append(rows)
    return rows


def _table():
    rows = []
    for c in cases():
        av, sv, tol = c["vars"]
        got = {"C-A": c_exact(c["anchor"], c["state"]),
               "C-B": c_tolerance(av, sv, tol),
               "C-C0": c_lineage(c["anchor"], c["state"], c["chain"], c["states"]),
               "C-C": c_lineage(c["anchor"], c["state"], c["chain"], c["states"], exact=c["exact"]),
               "D": c_class(c["t4"], c["anchor"], c["state"], (av, sv, tol)),
               "D2": d2_bound(c, F_MIN, ALPHA).state,
               "D2m": d2_margin(c)[0]}
        own = c["t4"] if c["class_growth"] is None else t4_class("FULL_STATE", "LOSSY", c["ratio"])
        d_own = c_class(own, c["anchor"], c["state"], (av, sv, tol))
        rows.append({"case": c["case"], "_case": c, "branches": got, "outcome": c["outcome"], "t4": c["t4"],
                     "d_own": d_own,
                     "class_growth": c["class_growth"], "class_ref": c["class_ref"],
                     "matches": {k: (None if v == "NOT_DECLARED" else
                                     ("SAME" if v == "SAME_WITH_BOUND" else v) == c["outcome"])
                                 for k, v in got.items()},
                     "split": len({("SAME" if v == "SAME_WITH_BOUND" else v) for v in got.values()
                                   if v != "NOT_DECLARED"}) > 1, "measured": c["measured"], "ebr": c["ebr"]})
    return rows


BRANCHES = ("C-A", "C-B", "C-C0", "C-C", "D", "D2", "D2m")


def render():
    rows = table()
    short = {"SAME_WITH_BOUND": "SAME_WB", "NOT_DECLARED": "--"}
    out = ["purpose inputs: f_min = %g, alpha = %g -> N = %d per lossy snapshot" % (F_MIN, ALPHA, n_required(F_MIN, ALPHA)),
           "case             T4 class         C-A        C-B        C-C0       C-C        D          D2 bound   D2 margin  measured"]
    for r in rows:
        b = r["branches"]
        def mark(k):
            v = short.get(b[k], b[k])
            return v + ("" if r["matches"][k] in (True, None) else "*")
        out.append("%-16s %-16s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %s" % (
            r["case"], r["t4"] or "VOID", mark("C-A"), mark("C-B"), mark("C-C0"), mark("C-C"), mark("D"),
            mark("D2"), mark("D2m"), r["outcome"]))
    out.append("* = disagrees with the measured resume outcome; SAME_WB = SAME_WITH_BOUND; -- = no separatrix declared")
    for k in BRANCHES:
        ms = [r["matches"][k] for r in rows if r["matches"][k] is not None]
        out.append("%-4s matches on %d of %d" % (k, sum(ms), len(ms)))
    out.append("")
    for r in rows:
        c = r["_case"]
        v = d2_bound(c, F_MIN, ALPHA)
        m = d2_margin(c)
        out.append("  %-16s D2: %s -- %s%s" % (r["case"], v.state, v.reason,
                                              "" if m[1] is None else "; margin to separatrix %.4f vs tol %g" % (m[1], c["radius"])))
    N = n_required(F_MIN, ALPHA)
    mt = miss_table(Ns=(N,), trials=400, pool=2000, seed=11)
    row = mt["rows"][0]
    misses = int(round(row["miss_rate"] * mt["trials"]))
    lo, hi = _wilson(misses, mt["trials"])
    out.append("")
    out.append("case 6 at f_min %g, alpha %g, N %d: measured miss rate %.4f (%d of %d trials, Wilson 95%% "
               "[%.4f, %.4f]); predicted (1 - f_hat)^N = %.4f with f_hat %.4f; alpha %g"
               % (F_MIN, ALPHA, N, row["miss_rate"], misses, mt["trials"], lo, hi, row["predicted"],
                  mt["f_hat"], ALPHA))
    out.append("  (that run draws from a fixed labelled pool of 2000, so it measures the pool's f_hat, not the ball)")
    f = SLIVER_F_EXACT
    out.append("resolution run (2026-11-18):")
    out.append("  exact sliver fraction, chord integration (M 200, both orientations, dt 0.05/0.02/0.01): %.5f" % f)
    out.append("  threshold f* = 1 - alpha^(1/N) = %.5f; exact miss (1 - f)^N = %.4f" % (f_threshold(N, ALPHA), (1 - f) ** N))
    k, n = DIRECT_RUN["miss"], DIRECT_RUN["trials"]
    lo, hi = _wilson(k, n)
    out.append("  direct fresh-sample trials (seed %d): %d of %d missed = %.4f, Wilson 95%% [%.4f, %.4f]"
               % (DIRECT_RUN["seed"], k, n, k / float(n), lo, hi))
    out.append("decision rule (order): DECIDED if measured miss <= alpha -> 400-trial pooled run NOT met; "
               "resolved run %s (upper bound %.4f vs alpha %g)" % ("met" if hi <= ALPHA else "NOT met", hi, ALPHA))
    out.append("VOID-9 -> DECIDED: identity across lossy snapshot = D2 with a declared sliver bound; "
               "verdict carries the bound")
    return "\n".join(out)


def _wilson(k, n, z=1.96):
    p = k / float(n)
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    w = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, c - w), min(1.0, c + w)


if __name__ == "__main__":
    print(render())
