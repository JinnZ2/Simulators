# SPDX-License-Identifier: CC0-1.0
"""
Checks `RESULTS_RUN_1.md` where it can be checked without the generators.

The generators were not delivered. Three of the drop's claims do not need
them, because they are algebra or graph invariants:

  1  SIM-D's derived constraint is an identity between two operations on a
     probability vector. Either it holds or it does not.
  2  SIM-C's reported outputs are graph invariants of a 5x5 grid. Either
     they equal the intact grid's or they do not.
  3  SIM-C's stated cause includes a damping term. Either the damping
     survives the normalisation that follows it or it is cancelled.

Everything else in the drop is a property of code that is not here, and is
recorded as UNVERIFIED rather than assessed. Same posture as
`aperiodic-order-sim-stack/`, which is the nearest precedent in this tree:
a delivered results drop with no generator, checked where checkable.

The delivered file is not modified. CC0. Stdlib only, parses under 3.9.
"""

from __future__ import annotations

import random
import sys


def norm(v):
    s = float(sum(v))
    return [x / s for x in v]


def quench(p, s):
    """The drop's operation: p -> p^(1+s)/Z."""
    return norm([x ** (1.0 + s) for x in p])


def temper(p, T):
    """Softmax temperature on a distribution: p -> p^(1/T)/Z."""
    return norm([x ** (1.0 / T) for x in p])


def close(a, b, tol=1e-12):
    return max(abs(x - y) for x, y in zip(a, b)) < tol


def sim_d_identity(trials=6, n=8, seed=11):
    """
    STATED     temper(quench(p,s), T) == temper(p, T*(1+s))
    CORRECTED  temper(quench(p,s), T) == temper(p, T/(1+s))

    Composing two temperings multiplies the temperatures, because
    (p^(1/T1))^(1/T2) = p^(1/(T1*T2)). A quench by s IS a tempering at
    1/(1+s), so the composite is T/(1+s) and not T*(1+s). The two agree
    only at s=0.
    """
    rng = random.Random(seed)
    rows = []
    for _ in range(trials):
        p = norm([rng.random() + 1e-3 for _ in range(n)])
        for s in (0.0, 0.25, 0.5, 1.0, 2.0):
            for T in (0.5, 1.0, 2.0, 3.0):
                lhs = temper(quench(p, s), T)
                rows.append({
                    "s": s, "T": T,
                    "as_stated": close(lhs, temper(p, T * (1.0 + s))),
                    "corrected": close(lhs, temper(p, T / (1.0 + s))),
                })
    return rows


def undo_temperature(trials=6, n=8, seed=13):
    """
    The corrected identity makes the undo temperature explicit, which the
    stated one does not: temper(quench(p,s), T) == p exactly when
    T/(1+s) == 1, i.e. T = 1+s.
    """
    rng = random.Random(seed)
    out = []
    for _ in range(trials):
        p = norm([rng.random() + 1e-3 for _ in range(n)])
        for s in (0.25, 0.5, 1.0, 2.0, 4.0):
            out.append({"s": s, "T_undo": 1.0 + s,
                        "recovers": close(temper(quench(p, s), 1.0 + s), p)})
    return out


def sim_c_invariants(rows=5, cols=5):
    """
    Reported: loops=16, alive_edges=40, at every sigma. A 5x5 grid graph
    has V = 25, E = 2*rows*(cols-1) = 40, and cycle rank E - V + 1 = 16.
    """
    v = rows * cols
    e = rows * (cols - 1) + cols * (rows - 1)
    return {"nodes": v, "edges": e, "cycle_rank": e - v + 1,
            "reported_edges": 40, "reported_loops": 16}


def damping_survives_normalisation(damp=0.85, seed=17, trials=200):
    """
    The stated cause says conductance is 'renormalized by max each
    iteration, and damped at 0.85'. Applied uniformly, the damping is
    removed exactly by the normalisation that follows it:

        (d*C) / max(d*C)  ==  C / max(C)

    so `damp` has no effect at all on the normalised state. Sharper than
    'nothing ever decays below the floor': there is no decay to speak of.
    """
    rng = random.Random(seed)
    same = 0
    for _ in range(trials):
        c = [rng.random() + 1e-6 for _ in range(rng.randint(2, 12))]
        a = [x * damp for x in c]
        a = [x / max(a) for x in a]
        b = [x / max(c) for x in c]
        if close(a, b, 1e-15):
            same += 1
    return {"trials": trials, "identical": same}


# --------------------------------------------------------------------------
# SIM-B: two readings that need no generator, only the printed table.
# --------------------------------------------------------------------------

SIM_B_TABLE = [
    (0.000, 5.625, 4.429, -1.195, 0.4000, "COLLAPSE"),
    (0.010, 5.625, 4.474, -1.151, 0.4110, "COLLAPSE"),
    (0.020, 5.625, 4.562, -1.063, 0.4133, "COLLAPSE"),
    (0.050, 5.625, 4.737, -0.888, 0.4247, "eroding"),
    (0.100, 5.625, 4.930, -0.695, 0.4393, "eroding"),
    (0.200, 5.625, 5.113, -0.512, 0.4503, "eroding"),
    (0.400, 5.625, 5.255, -0.369, 0.4593, "held"),
]


def sim_b_grid():
    """
    The 'GRADUAL, not steplike' negative is bounded by the anchor grid it
    was read on. Returns the spacings so the bound is a number.
    """
    xs = [r[0] for r in SIM_B_TABLE]
    gaps = [(xs[i + 1] - xs[i]) for i in range(len(xs) - 1)]
    return {"n_points": len(xs), "min_gap": min(gaps),
            "max_gap": max(gaps), "gaps": gaps,
            "ratio": max(gaps) / min(gaps)}


# Every column is printed to three decimals, so H_start, H_end and dH each
# carry +/- 5e-4 of rounding and their difference can disagree by up to
# 1.5e-3 without anything being wrong. Two rows sit at exactly 1.0e-3. The
# check is therefore a consistency check to the table's PRINTED precision
# and establishes nothing finer -- a tighter tolerance flagged rounding as
# an error on the first run.
_ROUNDING = 1.5e-3


def sim_b_arithmetic():
    """dH agrees with H_end - H_start to the table's printed precision."""
    bad = []
    for anchor, h0, h1, dh, tail, reading in SIM_B_TABLE:
        if abs((h1 - h0) - dh) > _ROUNDING:
            bad.append((anchor, round(h1 - h0, 4), dh))
    return bad


def sim_b_rounding_residuals():
    """How far each row sits from exact, for the record."""
    return [(a, round(abs((h1 - h0) - dh), 5))
            for a, h0, h1, dh, _t, _r in SIM_B_TABLE]


def report():
    print("CHECKS ON RESULTS_RUN_1.md -- generators not delivered\n")

    print("SIM-D  the derived constraint, as an identity")
    rows = sim_d_identity()
    stated_ok = sum(1 for r in rows if r["as_stated"])
    corr_ok = sum(1 for r in rows if r["corrected"])
    at_zero = [r for r in rows if r["s"] == 0.0]
    print("  cases tested                : %d" % len(rows))
    print("  identity AS STATED holds in : %d" % stated_ok)
    print("  CORRECTED form holds in     : %d" % corr_ok)
    print("  cases with s = 0            : %d  (the two forms agree only "
          "here)" % len(at_zero))
    print("  STATED     temper(quench(p,s),T) == temper(p, T*(1+s))  -- "
          "FALSE for s > 0")
    print("  CORRECTED  temper(quench(p,s),T) == temper(p, T/(1+s))  -- "
          "holds")
    print()
    print("  the undo temperature the corrected form makes explicit")
    for u in undo_temperature()[:5]:
        print("    s=%.2f  T_undo=%.2f  recovers p exactly: %s"
              % (u["s"], u["T_undo"], u["recovers"]))
    print("  the drop's prose says 'EXACTLY UNDONE by raising temperature'")
    print("  and is right. The formula beside it is not, and the corrected")
    print("  one names the temperature: T = 1+s.")
    print()

    print("SIM-C  the reported outputs against the intact grid")
    inv = sim_c_invariants()
    print("  5x5 grid: nodes %d  edges %d  cycle rank %d"
          % (inv["nodes"], inv["edges"], inv["cycle_rank"]))
    print("  reported: alive_edges %d  loops %d"
          % (inv["reported_edges"], inv["reported_loops"]))
    print("  match: %s -- the sim returned the INTACT grid at every sigma,"
          % (inv["edges"] == inv["reported_edges"] and
             inv["cycle_rank"] == inv["reported_loops"]))
    print("  so the pruning step had no effect at all, not a small one.")
    print()
    d = damping_survives_normalisation()
    print("  uniform damping followed by max-normalisation:")
    print("    identical to no damping in %d of %d random vectors"
          % (d["identical"], d["trials"]))
    print("    (d*C)/max(d*C) == C/max(C). `damp=0.85` is a free parameter")
    print("    with zero effect -- sharper than the stated cause.")
    print()

    print("SIM-B  what the printed table alone supports")
    bad = sim_b_arithmetic()
    res = sim_b_rounding_residuals()
    print("  dH == H_end - H_start to printed precision: %s" % (not bad))
    print("    residuals: %s"
          % ", ".join("%.0e" % r for _a, r in res))
    print("    largest is %.0e, which is rounding of three-decimal columns"
          % max(r for _a, r in res))
    g = sim_b_grid()
    print("  anchor grid: %d points, gaps %.3f to %.3f, ratio %.0fx"
          % (g["n_points"], g["min_gap"], g["max_gap"], g["ratio"]))
    print("  'GRADUAL, not steplike' is read on this grid. A transition")
    print("  narrower than the LOCAL spacing is invisible to it, and the")
    print("  spacing varies by %.0fx across the range. The negative is as"
          % g["ratio"])
    print("  strong as the grid and no stronger.")
    print()
    print("  the tail_mass inference does not follow from tail_mass alone:")
    print("  constant tail MASS does not locate the entropy loss, because")
    print("  the tail's INTERNAL entropy can collapse at fixed mass. The")
    print("  drop's 'inside the head' reading needs the head's and tail's")
    print("  entropies reported separately, and neither is in the table.")
    return 0


def selftest():
    fails = []
    rows = sim_d_identity()
    for r in rows:
        if not r["corrected"]:
            fails.append("corrected identity failed at s=%s T=%s"
                         % (r["s"], r["T"]))
        if r["s"] > 0 and r["as_stated"]:
            fails.append("stated identity held at s=%s; the finding says it "
                         "does not" % r["s"])
        if r["s"] == 0 and not r["as_stated"]:
            fails.append("the two forms must agree at s=0")
    for u in undo_temperature():
        if not u["recovers"]:
            fails.append("T=1+s did not recover p at s=%s" % u["s"])
    inv = sim_c_invariants()
    if inv["edges"] != 40 or inv["cycle_rank"] != 16:
        fails.append("5x5 grid invariants changed: %r" % inv)
    d = damping_survives_normalisation()
    if d["identical"] != d["trials"]:
        fails.append("damping was not cancelled in %d of %d"
                     % (d["trials"] - d["identical"], d["trials"]))
    bad = sim_b_arithmetic()
    if bad:
        fails.append("SIM-B dH column disagrees with H_end - H_start: %r"
                     % bad)
    g = sim_b_grid()
    if g["ratio"] < 2:
        fails.append("the anchor grid is near-uniform; the resolution "
                     "finding would be unearned")
    if quench([0.5, 0.5], 1.0) != [0.5, 0.5]:
        fails.append("quench must fix a uniform distribution")
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
