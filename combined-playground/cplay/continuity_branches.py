"""G5 item 9: continuity identity ("the same thing" across time), three branches, no winner
(9c VOID-9, BRANCHED).

C-A  EXACT STATE  sha256 of the declared state matches the anchor's.
C-B  TOLERANCE    every declared variable within its declared tolerance of the anchor
                  (M8 continuity.return_to_anchor, reused).
C-C  LINEAGE      an unbroken chain of recorded transitions from the anchor to the state, each
                  verified by replay (replaying the recorded input reproduces the recorded
                  output). Reading taken here: verification is forward replay; a many-to-one or
                  rounding transition replays exactly, so it verifies.

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


def c_lineage(anchor, state, chain, states):
    """states: {hash: state} recorded along the chain, so each transition can be replayed."""
    if not chain or chain[0].input_hash != h(anchor) or chain[-1].output_hash != h(state):
        return "NOT_SAME"
    for prev, nxt in zip(chain, chain[1:]):
        if prev.output_hash != nxt.input_hash:
            return "NOT_SAME"
    for t in chain:
        if t.input_hash not in states or h(t.replay(states[t.input_hash])) != t.output_hash:
            return "NOT_SAME"
    return "SAME"


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


def _dist(a, b):
    return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))


def _ode_case(name, f, s0, ebr, band):
    dt = 0.01
    anchor = _rk4(f, s0, dt, 1500)               # t = 15 s
    snap = round3(anchor)
    true_end = _rk4(f, anchor, dt, 3000)         # 30 s horizon
    res_end = _rk4(f, snap, dt, 3000)
    e0 = _dist(anchor, snap)
    ratio = _dist(true_end, res_end) / e0
    outcome = "SAME" if ratio <= band else "NOT_SAME"
    names = "xyz"[:len(anchor)]
    chain = [Transition("round to 3 dp", h(anchor), h(snap), round3)]
    return {"case": name, "anchor": anchor, "state": snap,
            "vars": (dict(zip(names, anchor)), dict(zip(names, snap)), {n: 1e-3 for n in names}),
            "chain": chain, "states": {h(anchor): anchor},
            "measured": "error ratio %.4g vs band %g" % (ratio, band), "outcome": outcome,
            "ratio": ratio, "ebr": ebr}


def cases():
    a10 = fib_word(10)
    snap = str(a10)
    fib_resumed = fib_word(15) == _extend(snap, 5)
    out = [{"case": "fib_exact", "anchor": a10, "state": snap,
            "vars": (dict(zip("ab", counts(a10))), dict(zip("ab", counts(snap))), {"a": 0, "b": 0}),
            "chain": [Transition("store word verbatim", h(a10), h(snap), lambda w: str(w))],
            "states": {h(a10): a10},
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
                "states": {h(w8): w8},
                "measured": "counts %s fit C(55,21) = %d words; no decoder" % (c8, math.comb(55, 21)),
                "outcome": "NOT_SAME",
                "ebr": "EBR_019: counts (34, 21) fit 841,728,816,603,675 words; verdict void"})
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
               "C-C": c_lineage(c["anchor"], c["state"], c["chain"], c["states"])}
        rows.append({"case": c["case"], "branches": got, "outcome": c["outcome"],
                     "matches": {k: v == c["outcome"] for k, v in got.items()},
                     "split": len(set(got.values())) > 1, "measured": c["measured"], "ebr": c["ebr"]})
    return rows


def render():
    rows = table()
    out = ["case          C-A exact  C-B tol    C-C lineage  measured resume  SPLIT  detail"]
    for r in rows:
        b = r["branches"]
        mark = lambda k: b[k] + ("" if r["matches"][k] else "*")
        out.append("%-13s %-10s %-10s %-12s %-16s %-6s %s" % (
            r["case"], mark("C-A"), mark("C-B"), mark("C-C"), r["outcome"],
            "SPLIT" if r["split"] else "", r["measured"]))
    out.append("* = branch disagrees with the measured resume outcome")
    for k in ("C-A", "C-B", "C-C"):
        out.append("%s matches the measured outcome on %d of %d" % (k, sum(r["matches"][k] for r in rows), len(rows)))
    out.append("SPLIT (branches disagree): " + ", ".join(r["case"] for r in rows if r["split"]))
    out.append("reference: Geometric-to-Binary-Computational-Bridge@85f3302 CLAIM_TABLE.md EBR_016-019")
    for r in rows:
        out.append("  %-13s %s" % (r["case"], r["ebr"]))
    out.append("no branch picked")
    return "\n".join(out)


if __name__ == "__main__":
    print(render())
