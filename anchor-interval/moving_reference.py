"""
moving_reference.py -- "the model drifted" is a difference between two
moving things, reported as a property of one.

CC0-1.0. Standard library only. Deterministic.

Drift measurement assumes a fixed reference the model moved against. What is
actually there is a benchmark, a rater pool, an annotation guideline and a
curation criterion, each set by a cohort with its own formation, each
versioned, each moving.

    reported_k = a_k * c_k + b_k

        c_k   capability of generation k on some fixed unauthored task
        a_k   contemporary benchmark's gain
        b_k   contemporary benchmark's offset

Sections:

  1  IDENTIFIABILITY. Given only `reported`, c and (a, b) are not separable.
     Exhibited constructively: a flat-capability trajectory and a rising one
     that produce byte-identical reported scores.

  2  WHAT A HELD-FIXED BENCHMARK BUYS. Scoring every generation on B_0
     identifies c up to B_0's own unknown affine constants. Shape yes, level
     no -- which is a real caveat on the proposed measurement, not a defeat
     of it.

  3  THE CRITERIA-DRIFT SHARE, under stated assumptions.

  4  SEVEN TERMS MOVED, ONE NUMBER REPORTED. Effective rank of the
     attribution design via the participation ratio of its correlation
     spectrum -- the statistic ../model-ecology/phylogeny.py already uses.
     Includes the objection that makes the co-movement non-removable: the
     architectural term was SELECTED against the corpus, so the covariance
     was built in before any experiment started.
"""

from __future__ import annotations

import math
import random

RULE = "=" * 72
SEED = 20260816


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# ---------------------------------------------------------------------------
# 1  identifiability


def check_identifiability() -> None:
    section("1  capability and criteria are not separable from reported score")

    K = 8
    # Trajectory A: capability rises, benchmark constants fixed.
    cA = [0.30 + 0.05 * k for k in range(K)]
    aA = [1.00] * K
    bA = [0.00] * K

    reported = [a * c + b for a, c, b in zip(aA, cA, bA)]

    # Trajectory B: capability FLAT. Solve for a benchmark gain that
    # reproduces `reported` exactly. Nothing is fitted -- it is division.
    cB = [0.30] * K
    bB = [0.00] * K
    aB = [(r - b) / c for r, c, b in zip(reported, cB, bB)]

    repB = [a * c + b for a, c, b in zip(aB, cB, bB)]

    print("  %-5s %-12s %-12s %-12s %-12s %-12s"
          % ("gen", "c (A)", "a (A)", "c (B)", "a (B)", "reported"))
    print("  " + "-" * 68)
    for k in range(K):
        print("  %-5d %-12.4f %-12.4f %-12.4f %-12.4f %-12.4f"
              % (k, cA[k], aA[k], cB[k], aB[k], reported[k]))

    gap = max(abs(x - y) for x, y in zip(reported, repB))
    print()
    print("  max |reported_A - reported_B| = %.3e" % gap)
    print()
    print("  A: capability rose %.0f%%, ruler fixed."
          % (100 * (cA[-1] / cA[0] - 1)))
    print("  B: capability did not move at all, ruler stretched %.0f%%."
          % (100 * (aB[-1] / aB[0] - 1)))
    print("  The published number cannot tell them apart, and there is no")
    print("  statistical remedy -- it is one equation and two unknowns per")
    print("  release. Not a precision problem. A rank problem.")


# ---------------------------------------------------------------------------
# 2  what a held-fixed benchmark buys


def check_fixed_benchmark() -> None:
    section("2  a held-fixed benchmark identifies shape, not level")

    K = 8
    c = [0.30 + 0.05 * k for k in range(K)]
    a = [1.00 + 0.05 * k for k in range(K)]      # criteria drift
    b = [0.00 + 0.01 * k for k in range(K)]

    contemporary = [ai * ci + bi for ai, ci, bi in zip(a, c, b)]
    on_B0 = [a[0] * ci + b[0] for ci in c]        # everything on gen-0 ruler

    print("  %-5s %-16s %-16s %-16s"
          % ("gen", "contemporary", "on fixed B_0", "divergence"))
    print("  " + "-" * 56)
    for k in range(K):
        print("  %-5d %-16.4f %-16.4f %+.4f"
              % (k, contemporary[k], on_B0[k], contemporary[k] - on_B0[k]))

    print()
    print("  The divergence between the two curves is the criteria-drift")
    print("  term, isolated: (a_k - a_0) c_k + (b_k - b_0).")
    print()
    print("  What it does NOT give: c itself. Scores on B_0 are a_0 c_k + b_0")
    print("  and a_0, b_0 are unknown. So ratios of DIFFERENCES are")
    print("  identified and levels are not:")
    print()
    third = (on_B0[3] - on_B0[0]) / (on_B0[7] - on_B0[0])
    truth = (c[3] - c[0]) / (c[7] - c[0])
    print("    (B0_3 - B0_0)/(B0_7 - B0_0) = %.6f" % third)
    print("    (c_3  - c_0 )/(c_7  - c_0 ) = %.6f" % truth)
    print("    identified: %s" % (abs(third - truth) < 1e-9))
    print()
    print("  So the measurement is worth running and its output is a SHARE,")
    print("  not a capability. And if the old benchmark reads as obsolete")
    print("  rather than as a control, that judgment was made inside the")
    print("  thing being measured.")


# ---------------------------------------------------------------------------
# 3  criteria-drift share


def check_share() -> None:
    section("3  how much of the reported improvement is the ruler moving")

    K = 8
    print("  Stated assumptions -- these are a worked illustration, not a")
    print("  measurement. The point is the decomposition, not the numbers.\n")

    for label, da, db in (("ruler steady        ", 0.00, 0.000),
                          ("ruler +5%/gen       ", 0.05, 0.010),
                          ("ruler +9%/gen       ", 0.09, 0.018)):
        c = [0.30 + 0.05 * k for k in range(K)]
        a = [1.00 + da * k for k in range(K)]
        b = [0.00 + db * k for k in range(K)]
        rep = [ai * ci + bi for ai, ci, bi in zip(a, c, b)]
        true_gain = a[0] * (c[-1] - c[0])
        rep_gain = rep[-1] - rep[0]
        share = 1.0 - true_gain / rep_gain
        print("  %s reported +%.4f   capability +%.4f   ruler share %5.1f%%"
              % (label, rep_gain, true_gain, 100 * share))

    print()
    print("  Nothing here needs anyone to cheat. Every benchmark revision")
    print("  was made for a stated reason, by people who thought the old one")
    print("  had stopped discriminating. The share is what it is regardless")
    print("  of why the revisions happened.")


# ---------------------------------------------------------------------------
# 4  seven terms, one number


def jacobi_eigenvalues(m, iters=100, tol=1e-12):
    """Symmetric eigenvalues by cyclic Jacobi rotation. stdlib only."""
    n = len(m)
    a = [row[:] for row in m]
    for _ in range(iters):
        off = math.sqrt(sum(a[i][j] ** 2
                            for i in range(n) for j in range(n) if i != j))
        if off < tol:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < tol:
                    continue
                theta = (a[q][q] - a[p][p]) / (2.0 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (
                    abs(theta) + math.sqrt(theta * theta + 1.0))
                cs = 1.0 / math.sqrt(t * t + 1.0)
                sn = t * cs
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p] = cs * akp - sn * akq
                    a[k][q] = sn * akp + cs * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k] = cs * apk - sn * aqk
                    a[q][k] = sn * apk + cs * aqk
    return sorted((a[i][i] for i in range(n)), reverse=True)


def n_eff(eigs) -> float:
    """Participation ratio. Same statistic as ../model-ecology/phylogeny.py."""
    s = sum(eigs)
    s2 = sum(e * e for e in eigs)
    return (s * s) / s2 if s2 > 0 else 0.0


def correlation(cols):
    n = len(cols)
    means = [sum(c) / len(c) for c in cols]
    sds = [math.sqrt(sum((x - m) ** 2 for x in c) / len(c)) or 1e-12
           for c, m in zip(cols, means)]
    return [[sum((cols[i][k] - means[i]) * (cols[j][k] - means[j])
                 for k in range(len(cols[0]))) / len(cols[0])
             / (sds[i] * sds[j])
             for j in range(n)] for i in range(n)]


TERMS = ("model architecture", "training corpus", "curation criteria",
         "eval benchmark", "annotation guidelines", "rater pool",
         "definition of neutral")


def check_rank() -> None:
    section("4  seven terms moved, one number reported")

    K = 40   # releases; more than 7 so the design is not trivially singular
    print("  %d terms co-move between releases. The published delta is one"
          % len(TERMS))
    print("  number, attributed to the first term.\n")
    for t in TERMS:
        print("      %s" % t)
    print()
    print("  Effective number of independent directions in the design,")
    print("  by participation ratio of the correlation spectrum:\n")
    print("  %-14s %-12s %-14s %s"
          % ("co-movement", "N_eff", "top eigenvalue", "reading"))
    print("  " + "-" * 62)

    floor = None
    for load in (0.0, 0.3, 0.5, 0.7, 0.85, 0.95):
        rng = random.Random(SEED)
        shared = [rng.gauss(0, 1) for _ in range(K)]
        cols = []
        for _ in TERMS:
            own = [rng.gauss(0, 1) for _ in range(K)]
            cols.append([load * s + math.sqrt(1 - load * load) * o
                         for s, o in zip(shared, own)])
        eigs = jacobi_eigenvalues(correlation(cols))
        ne = n_eff(eigs)
        if floor is None:
            floor = ne
        reading = ("terms separable" if ne > 4
                   else "one direction" if ne < 2 else "partly confounded")
        print("  %-14.2f %-12.3f %-14.3f %s" % (load, ne, eigs[0], reading))

    print()
    print("  The load = 0 row reads %.2f rather than %d: with %d releases the"
          % (floor, len(TERMS), K))
    print("  sample correlation matrix carries its own noise floor. That is")
    print("  the apparatus reading, and every row below sits on it.")
    print()
    print("  What makes the co-movement non-removable by better design:")
    print("  the architectural term was CHOSEN against the corpus.")
    print()
    print("      attention shapes fitted to language statistics")
    print("      tokenizers fitted to the writing system")
    print("      context lengths fitted to document lengths")
    print("      objectives fitted to what the corpus can score")
    print()
    print("  So the term and the data are not independent variables. Varying")
    print("  the term while holding the corpus fixed does not separate them,")
    print("  because the covariance was built in before the experiment")
    print("  started. Ablations at small scale DO isolate -- and small-scale")
    print("  results are known not to transfer reliably upward, so the")
    print("  isolated result is not the one that ships.")
    print()
    print("  Falsifier for the selection claim: an architectural term chosen")
    print("  WITHOUT reference to the corpus -- transferred from another")
    print("  modality, or fixed before the corpus existed -- decorrelates the")
    print("  pair, and the load parameter above should drop for it.")


# ---------------------------------------------------------------------------


def main() -> None:
    print()
    print("MOVING REFERENCE: A DIFFERENCE BETWEEN TWO MOVING THINGS")

    check_identifiability()
    check_fixed_benchmark()
    check_share()
    check_rank()

    section("READING")
    print("""
  From a contemporary score alone, capability and criteria are not
  separable -- one equation, two unknowns, and section 1 exhibits a
  flat-capability trajectory that reproduces a rising one exactly.

  Holding one benchmark fixed across generations is the right measurement
  and it buys a SHARE, not a capability: c is identified only up to the
  fixed benchmark's own unknown gain and offset, so differences and their
  ratios are identified and levels are not.

  Seven terms move between releases and one number is published. At high
  co-movement the design carries close to one independent direction, and
  the co-movement is not a nuisance a better experiment removes: the
  architecture was selected against the corpus, so the two were confounded
  before any ablation was designed.
""")


if __name__ == "__main__":
    main()
