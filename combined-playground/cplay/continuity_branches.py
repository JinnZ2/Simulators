"""G5 item 9: continuity identity ("the same thing" across time), three branches, no winner
(9c VOID-9, BRANCHED).

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

Known cases rebuilt here (stdlib, seedless) after snapshot_delta's four systems, Geometric-to-
Binary-Computational-Bridge @85f3302, CLAIM_TABLE.md EBR_016-019 (sha256 a657c606...):
  fib_exact     context-free word, exact snapshot           EBR_016: resume reproduces the run
  spiral_lossy  stable sink lam=-0.1, state rounded 3 dp    EBR_017: error ratio 0.0498, band [0,3]
  lorenz_lossy  Lorenz, same rounding                       EBR_018: ratio 16980, band 100
  counts_word   word summarised as letter counts            EBR_019: cannot resume (VOID)
The measured resume outcome is recomputed here and printed beside EBR's; the bands [0, 3] and 100
are EBR's, stated there as UNSOURCED.
"""
import hashlib
import math
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


def _ode_case(name, f, s0, ebr, band, *, anchor=None, rnd=round3, tol=1e-3, ref=None):
    dt = 0.01
    anchor = _rk4(f, s0, dt, 1500) if anchor is None else anchor   # t = 15 s by default
    snap = rnd(anchor)
    true_end = _rk4(f, anchor, dt, 3000)         # 30 s horizon
    res_end = _rk4(f, snap, dt, 3000)
    e0 = _dist(anchor, snap)
    ratio = _dist(true_end, res_end) / e0
    outcome = "SAME" if ratio <= band else "NOT_SAME"
    names = "xyz"[:len(anchor)]
    chain = [Transition("round", h(anchor), h(snap), rnd)]
    ra, rs = ref if ref is not None else (anchor, snap)
    growth = _growth(f, ra, rs)
    return {"case": name, "anchor": anchor, "state": snap,
            "vars": (dict(zip(names, anchor)), dict(zip(names, snap)), {n: tol for n in names}),
            "chain": chain, "states": {h(anchor): anchor}, "exact": {h(anchor): anchor},
            "t4": t4_class("FULL_STATE", "LOSSY", growth), "class_growth": growth,
            "class_ref": "the case's own snapshot" if ref is None else "declared reference snapshot",
            "measured": "error ratio %.4g vs band %g" % (ratio, band), "outcome": outcome,
            "ratio": ratio, "ebr": ebr}


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
    return out


def _extend(word, levels):
    for _ in range(levels):
        word = "".join("ab" if c == "a" else "a" for c in word)
    return word


def table():
    rows = []
    for c in cases():
        av, sv, tol = c["vars"]
        got = {"C-A": c_exact(c["anchor"], c["state"]),
               "C-B": c_tolerance(av, sv, tol),
               "C-C0": c_lineage(c["anchor"], c["state"], c["chain"], c["states"]),
               "C-C": c_lineage(c["anchor"], c["state"], c["chain"], c["states"], exact=c["exact"]),
               "D": c_class(c["t4"], c["anchor"], c["state"], (av, sv, tol))}
        own = c["t4"] if c["class_growth"] is None else t4_class("FULL_STATE", "LOSSY", c["ratio"])
        d_own = c_class(own, c["anchor"], c["state"], (av, sv, tol))
        rows.append({"case": c["case"], "branches": got, "outcome": c["outcome"], "t4": c["t4"],
                     "d_own": d_own,
                     "class_growth": c["class_growth"], "class_ref": c["class_ref"],
                     "matches": {k: v == c["outcome"] for k, v in got.items()},
                     "split": len(set(got.values())) > 1, "measured": c["measured"], "ebr": c["ebr"]})
    return rows


BRANCHES = ("C-A", "C-B", "C-C0", "C-C", "D")


def render():
    rows = table()
    out = ["case            T4 class (growth, where measured)              C-A        C-B        C-C0       C-C        D          measured  SPLIT"]
    for r in rows:
        b = r["branches"]
        mark = lambda k: b[k] + ("" if r["matches"][k] else "*")
        g = "" if r["class_growth"] is None else " %.3g at %s" % (r["class_growth"], r["class_ref"])
        out.append("%-15s %-46s %-10s %-10s %-10s %-10s %-10s %-9s %s" % (
            r["case"], (r["t4"] or "VOID") + g, mark("C-A"), mark("C-B"), mark("C-C0"), mark("C-C"),
            mark("D"), r["outcome"], "SPLIT" if r["split"] else ""))
    out.append("* = branch disagrees with the measured resume outcome; C-C0 is the first build, kept as history")
    for k in BRANCHES:
        out.append("%-4s matches on %d of %d  (first four cases: %d of 4)" % (
            k, sum(r["matches"][k] for r in rows), len(rows), sum(r["matches"][k] for r in rows[:4])))
    out.append("SPLIT (branches disagree): " + ", ".join(r["case"] for r in rows if r["split"]))
    out.append("D with growth measured at each case's own snapshot instead: " + ", ".join(
        "%s %s" % (r["case"], r["d_own"]) for r in rows))
    for r in rows:
        out.append("  %-15s %s; %s" % (r["case"], r["measured"], r["ebr"]))
    out.append("no branch picked")
    return "\n".join(out)

if __name__ == "__main__":
    print(render())
