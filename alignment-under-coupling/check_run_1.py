#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
Checks `RESULTS_RUN_1.md` against the sims that produced it.

HISTORY, because it changes what this file is. The results were delivered
first, without the generators, and checked in `transition-family-marker/` as
algebra and graph invariants alone. The generators arrived afterwards and
that folder was merged into this one, so the checks now IMPORT the code
rather than model it — the repo's own no-copies rule, and the reason the
merge happened rather than two folders being kept.

Having the code changed two verdicts, and one of them was mine:

  TFM_004 was WRONG and is corrected here. It read the delivered prose
  ("renormalized by max each iteration, and damped at 0.85") as a uniform
  scaling, which max-normalisation would cancel exactly. The code is
  `0.85*C + 0.15*target` — a convex combination toward the target, which
  the normalisation does not cancel. The real reason nothing prunes is
  measured below and is a different thing entirely.

  TFM_005 said the drop's tail reading was under-determined without head
  and tail entropies. It is worse than under-determined: computing them
  INVERTS it, and the drop's own UNRESOLVED contradiction dissolves.

The delivered files are not modified. Stdlib only, parses under 3.9.

usage:
    python3 check_run_1.py
    python3 check_run_1.py --selftest
"""

from __future__ import annotations

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sim_b_entropy_depletion as B      # noqa: E402
import sim_c_loop_threshold as C         # noqa: E402
import sim_d_temperature_null as D       # noqa: E402


def close(a, b, tol=1e-12):
    return max(abs(x - y) for x, y in zip(a, b)) < tol


# --------------------------------------------------------------------------
# TFM_001 / TFM_002 -- SIM-D's derived constraint, against the real
# quench() and temper().
# --------------------------------------------------------------------------

def identity_cases(trials=6, n=8, seed=11):
    """
    STATED     temper(quench(p,s), T) == temper(p, T*(1+s))
    CORRECTED  temper(quench(p,s), T) == temper(p, T/(1+s))

    Uses the sims' own functions, so this is a statement about the code and
    not about a model of it.
    """
    rng = random.Random(seed)
    rows = []
    for _ in range(trials):
        p = D.zipf(64)
        rng.shuffle(p)
        for s in (0.0, 0.25, 0.5, 1.0, 2.0):
            for T in (0.5, 1.0, 2.0, 3.0):
                lhs = D.temper(D.quench(p, s), T)
                rows.append({
                    "s": s, "T": T,
                    "as_stated": close(lhs, D.temper(p, T * (1.0 + s)), 1e-9),
                    "corrected": close(lhs, D.temper(p, T / (1.0 + s)), 1e-9),
                })
    return rows


def undo_temperature(trials=4, seed=13):
    """`temper(quench(p,s), T) == p` exactly at T = 1+s."""
    rng = random.Random(seed)
    out = []
    for _ in range(trials):
        p = D.zipf(64)
        rng.shuffle(p)
        for s in (0.25, 0.5, 1.0, 2.0, 4.0):
            out.append({"s": s, "T_undo": 1.0 + s,
                        "recovers": close(D.temper(D.quench(p, s), 1.0 + s),
                                          p, 1e-9)})
    return out


# --------------------------------------------------------------------------
# TFM_003 / TFM_004 / TFM_009 -- SIM-C.
# --------------------------------------------------------------------------

def grid_invariants(k=5):
    nodes, edges = C.build_grid(k)
    return {"nodes": nodes, "edges": len(edges),
            "cycle_rank": len(edges) - nodes + 1,
            "reported_edges": 40, "reported_loops": 16}


def damping_is_cancelled(seed=17, trials=200):
    """
    TFM_004 AS WRITTEN, tested against the code's actual update.

    A uniform scaling IS cancelled by max-normalisation. The code's update
    is not a uniform scaling, so it is not cancelled, and the claim fails.
    Both are computed so the correction is a measurement.
    """
    rng = random.Random(seed)
    uniform_cancelled = actual_cancelled = 0
    for _ in range(trials):
        n = rng.randint(2, 12)
        c = [rng.random() + 1e-6 for _ in range(n)]
        tgt = [rng.random() + 1e-6 for _ in range(n)]
        base = [x / max(c) for x in c]
        u = [0.85 * x for x in c]
        u = [x / max(u) for x in u]
        if close(u, base, 1e-12):
            uniform_cancelled += 1
        a = [0.85 * x + 0.15 * t for x, t in zip(c, tgt)]
        a = [x / max(a) for x in a]
        if close(a, base, 1e-12):
            actual_cancelled += 1
    return {"trials": trials,
            "uniform_scaling_cancelled": uniform_cancelled,
            "actual_update_cancelled": actual_cancelled}


def conductance_range(sigma, k=5, iters=150, gamma=0.5, seed=3):
    """
    The real reason nothing prunes: where the floor sits relative to the
    conductances it is applied to. Re-runs SIM-C's loop with the state
    returned instead of discarded.
    """
    rng = random.Random(seed)
    nodes, edges = C.build_grid(k)
    cond = [1.0] * len(edges)
    source = 0
    base = 1.0 / (nodes - 1)
    for _ in range(iters):
        sinks = [0.0] * nodes
        for i in range(nodes):
            if i == source:
                continue
            sinks[i] = max(0.0, base * (1.0 + sigma * rng.gauss(0, 1)))
        q = C.solve_flows(nodes, edges, cond, sinks, source)
        newc = [0.85 * cond[i] + 0.15 * (abs(x) ** (2.0 * gamma))
                for i, x in enumerate(q)]
        m = max(newc) or 1.0
        cond = [max(1e-9, x / m) for x in newc]
    cond.sort()
    return {"sigma": sigma, "min": cond[0], "median": cond[len(cond) // 2],
            "max": cond[-1], "floor": 1e-3,
            "floor_below_min_by": cond[0] / 1e-3}


def loops_formula(k=5):
    """
    TFM_009. `loops = alive - (nodes - 1)` is cycle rank only when the alive
    subgraph is connected and spanning. Nothing checks that, so a pruned and
    disconnected result reports a loop count as if it were a spanning tree
    plus loops.
    """
    nodes, _ = C.build_grid(k)
    return {"nodes": nodes,
            "rows": [(alive, max(0, alive - (nodes - 1)))
                     for alive in (40, 30, 24, 12)]}


# --------------------------------------------------------------------------
# TFM_005 -- SIM-B, the reading the drop logged as UNRESOLVED.
# --------------------------------------------------------------------------

def split_entropy(p, head=50):
    hm = sum(p[:head])
    tm = sum(p[head:])

    def h(seg, m):
        return (-sum((x / m) * math.log(x / m) for x in seg if x > 0)
                if m > 0 else 0.0)
    return {"head_mass": hm, "H_head": h(p[:head], hm),
            "tail_mass": tm, "H_tail": h(p[head:], tm)}


def final_distribution(anchor, gens=12, corpus=3000, seed=7):
    """SIM-B's loop, returning the distribution rather than the summary."""
    rng = random.Random(seed)
    true_p = B.zipf_dist()
    p = list(true_p)
    for _ in range(gens):
        na = int(corpus * anchor)
        ns = corpus - na
        c1 = B.sample_counts(p, ns, rng) if ns else [0] * B.VOCAB
        c2 = B.sample_counts(true_p, na, rng) if na else [0] * B.VOCAB
        p = B.refit([x + y for x, y in zip(c1, c2)])
    return p, true_p


def head_tail_split(anchors=(0.0, 0.05, 0.40)):
    out = []
    _, true_p = final_distribution(0.0, gens=0)
    base = split_entropy(true_p)
    for a in anchors:
        p, _ = final_distribution(a)
        s = split_entropy(p)
        out.append({"anchor": a, "H_total": B.entropy(p),
                    "tail_mass": s["tail_mass"],
                    "dH_head": s["H_head"] - base["H_head"],
                    "dH_tail": s["H_tail"] - base["H_tail"]})
    return base, out


def entropy_decomposition_holds():
    """H = H(mass split) + head_m*H_head + tail_m*H_tail. Sanity on the split."""
    p = B.zipf_dist()
    s = split_entropy(p)
    mix = -(s["head_mass"] * math.log(s["head_mass"]) +
            s["tail_mass"] * math.log(s["tail_mass"]))
    rebuilt = mix + s["head_mass"] * s["H_head"] + s["tail_mass"] * s["H_tail"]
    return abs(rebuilt - B.entropy(p)) < 1e-9


# --------------------------------------------------------------------------
# TFM_006 / TFM_007 / TFM_010
# --------------------------------------------------------------------------

SIM_B_ANCHORS = (0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.40)


def anchor_grid():
    xs = list(SIM_B_ANCHORS)
    gaps = [xs[i + 1] - xs[i] for i in range(len(xs) - 1)]
    return {"n_points": len(xs), "min_gap": min(gaps), "max_gap": max(gaps),
            "ratio": max(gaps) / min(gaps)}


def entropy_unit():
    """SIM-B uses math.log, so the columns are nats. Confirmed, not assumed."""
    return {"H_true_zipf": B.entropy(B.zipf_dist()),
            "ln_vocab": math.log(B.VOCAB),
            "log2_vocab": math.log(B.VOCAB, 2),
            "reported_H_start": 5.625}


def quick_flag_is_a_noop():
    """TFM_010. run_all.py's --quick rebinds `a` to a copy of itself."""
    import inspect
    import re
    import run_all
    src = inspect.getsource(run_all.main)
    m = re.search(r"if quick:\s*\n\s*a\s*=\s*(\[.+?\])", src)
    body = m.group(1) if m else None
    args = ["--samples", "3000"]
    return {"body": body, "is_copy": body == "[x for x in a]",
            "identical": args == [x for x in args]}


def report():
    print("CHECKS ON RESULTS_RUN_1.md -- generators now present, imported\n")

    print("TFM_001/002  SIM-D's derived constraint, against the real")
    print("             quench() and temper()")
    rows = identity_cases()
    stated = sum(1 for r in rows if r["as_stated"])
    corr = sum(1 for r in rows if r["corrected"])
    zeros = sum(1 for r in rows if r["s"] == 0.0)
    print("  cases                      : %d" % len(rows))
    print("  identity AS STATED holds in: %d   (cases with s=0: %d)"
          % (stated, zeros))
    print("  CORRECTED form holds in    : %d" % corr)
    print("  STATED    temper(quench(p,s),T) == temper(p, T*(1+s))  FALSE")
    print("  CORRECTED temper(quench(p,s),T) == temper(p, T/(1+s))  holds")
    u = undo_temperature()
    print("  undo temperature T = 1+s recovers p in %d of %d cases"
          % (sum(1 for x in u if x["recovers"]), len(u)))
    print("  The drop's prose is right and its formula is not. The")
    print("  correction names a temperature the stated version cannot.")
    print()

    print("TFM_003  SIM-C returned the intact grid")
    inv = grid_invariants()
    print("  5x5: nodes %d  edges %d  cycle rank %d"
          % (inv["nodes"], inv["edges"], inv["cycle_rank"]))
    print("  reported alive_edges %d  loops %d  -> match %s"
          % (inv["reported_edges"], inv["reported_loops"],
             inv["edges"] == inv["reported_edges"] and
             inv["cycle_rank"] == inv["reported_loops"]))
    print()

    print("TFM_004  CORRECTED. My claim was wrong; the code says so.")
    d = damping_is_cancelled()
    print("  a UNIFORM scaling is cancelled by max-normalisation in %d of %d"
          % (d["uniform_scaling_cancelled"], d["trials"]))
    print("  the code's ACTUAL update, 0.85*C + 0.15*target, is cancelled")
    print("  in %d of %d. It is a convex combination, not a scaling."
          % (d["actual_update_cancelled"], d["trials"]))
    print()
    print("  the real reason nothing prunes -- where the floor sits:")
    print("  %-8s %-11s %-11s %-11s %s"
          % ("sigma", "min C", "median", "max C", "min / floor"))
    for s in (0.0, 0.4, 1.6):
        r = conductance_range(s)
        print("  %-8.2f %-11.3e %-11.3e %-11.3e %.0fx"
              % (r["sigma"], r["min"], r["median"], r["max"],
                 r["floor_below_min_by"]))
    print("  The floor is 1e-3 and the SMALLEST conductance is ~4.6e-2, so")
    print("  the floor sits ~46x below anything the dynamics produce. The")
    print("  conductances span about one decade and the spread barely moves")
    print("  with sigma. Nothing can reach the floor -- a G-RES failure,")
    print("  the threshold outside the range of the quantity it tests.")
    print()

    print("TFM_009  the loop count is not cycle rank unless the alive")
    print("         subgraph is connected and spanning, and nothing checks")
    lf = loops_formula()
    for alive, loops in lf["rows"]:
        print("  alive=%-3d -> reported loops = %d" % (alive, loops))
    print("  at alive=12 no subgraph can span %d nodes, and the formula"
          % lf["nodes"])
    print("  still returns 0 rather than flagging a disconnected result.")
    print()

    print("TFM_005  CORRECTED. The drop's UNRESOLVED reading is inverted.")
    base, rows = head_tail_split()
    print("  true distribution: H_head %.3f  H_tail %.3f  tail_mass %.4f"
          % (base["H_head"], base["H_tail"], base["tail_mass"]))
    print("  %-8s %-9s %-11s %-11s %s"
          % ("anchor", "H_total", "tail_mass", "dH_head", "dH_tail"))
    for r in rows:
        print("  %-8.2f %-9.3f %-11.4f %+-11.3f %+.3f"
              % (r["anchor"], r["H_total"], r["tail_mass"],
                 r["dH_head"], r["dH_tail"]))
    print("  decomposition identity holds: %s" % entropy_decomposition_holds())
    print()
    print("  The drop read near-constant tail MASS against a falling H as")
    print("  showing the loss is 'INSIDE the head', contradicting the")
    print("  reported mechanism. Unanchored, the head loses 0.12 nats and")
    print("  the tail loses 2.29. The loss is almost entirely in the tail,")
    print("  which keeps its mass while concentrating it onto fewer tokens.")
    print("  Anchoring cuts the tail loss to 0.90 and leaves the head flat.")
    print("  The reported mechanism is REPRODUCED, not contradicted, and")
    print("  the drop's own UNRESOLVED contradiction dissolves.")
    print()

    print("TFM_006  the gradual-not-steplike negative, and its grid")
    g = anchor_grid()
    print("  %d points, gaps %.3f to %.3f, ratio %.0fx"
          % (g["n_points"], g["min_gap"], g["max_gap"], g["ratio"]))
    print()

    print("TFM_007  the entropy unit, now checkable in the code")
    e = entropy_unit()
    print("  SIM-B uses math.log -> nats. H of the true Zipf = %.3f,"
          % e["H_true_zipf"])
    print("  which is the reported H_start of %.3f. ln(vocab)=%.3f,"
          % (e["reported_H_start"], e["ln_vocab"]))
    print("  log2(vocab)=%.3f. Confirmed nats; still absent from the table."
          % e["log2_vocab"])
    print()

    print("TFM_010  run_all.py's --quick flag does nothing")
    q = quick_flag_is_a_noop()
    print("  body of the branch: %s" % q["body"])
    print("  that is a copy of the same list, so the flag is inert: %s"
          % q["identical"])
    return 0


def selftest():
    fails = []
    for r in identity_cases():
        if not r["corrected"]:
            fails.append("corrected identity failed at s=%s T=%s"
                         % (r["s"], r["T"]))
        if r["s"] > 0 and r["as_stated"]:
            fails.append("stated identity held at s=%s" % r["s"])
    for u in undo_temperature():
        if not u["recovers"]:
            fails.append("T=1+s did not recover p at s=%s" % u["s"])
    inv = grid_invariants()
    if inv["edges"] != 40 or inv["cycle_rank"] != 16:
        fails.append("5x5 grid invariants changed: %r" % inv)
    d = damping_is_cancelled()
    if d["uniform_scaling_cancelled"] != d["trials"]:
        fails.append("a uniform scaling must be cancelled by max-norm")
    if d["actual_update_cancelled"] != 0:
        fails.append("the code's update must NOT be cancelled; TFM_004's "
                     "correction depends on it")
    r = conductance_range(1.6)
    if r["min"] <= r["floor"]:
        fails.append("some conductance reached the floor; TFM_004's "
                     "corrected reason would not hold")
    base, rows = head_tail_split((0.0,))
    if not (rows[0]["dH_tail"] < rows[0]["dH_head"] < 0):
        fails.append("TFM_005's correction requires the tail loss to exceed "
                     "the head loss; got head %+.3f tail %+.3f"
                     % (rows[0]["dH_head"], rows[0]["dH_tail"]))
    if abs(rows[0]["dH_tail"]) < 10 * abs(rows[0]["dH_head"]):
        fails.append("the tail loss is not an order of magnitude larger; "
                     "the correction is weaker than stated")
    if not entropy_decomposition_holds():
        fails.append("the head/tail entropy decomposition does not close")
    if anchor_grid()["ratio"] < 2:
        fails.append("the anchor grid is near-uniform; TFM_006 unearned")
    e = entropy_unit()
    if abs(e["H_true_zipf"] - e["reported_H_start"]) > 1e-3:
        fails.append("H of the true Zipf no longer matches the reported "
                     "H_start; TFM_007's unit confirmation breaks")
    q = quick_flag_is_a_noop()
    if not q["is_copy"]:
        fails.append("--quick is no longer a no-op; TFM_010 must be restated")
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    return report()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
