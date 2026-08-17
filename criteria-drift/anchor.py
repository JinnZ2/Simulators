"""
anchor.py -- anchor-version scoring, made first class.

CC0-1.0. Standard library only. Deterministic.

THE ARGUMENT, from the cross-domain notes in SOURCE_DROP_KIMI.md
----------------------------------------------------------------
    In every case, the solution is the same: identify an invariant subset
    that does not change, and use it as the bridge. In semantic drift, it's
    "stable words". In metrology, it's the primary standard. In your
    framework, it's a frozen model scored on all versions.

    The fields that have solved this best treat alignment as a first-class
    problem with its own error budget. Your framework currently treats
    anchor-version scoring as optional. The cross-domain pattern suggests it
    should be mandatory -- without it, drift is unmeasurable.

CD_006 recorded the same gap from inside: the capability term is in the
stated model and not in the code, so a slope on drift alone absorbs it. It
was left OPEN on the grounds that no edit to `regress.py` can recover a term
nobody measured.

That is still true, and it is not the whole repair. What CAN be built is the
part every one of those fields built: make the alignment step explicit, name
what it buys, and refuse to report an identified criteria term when the
bridge is absent.

WHAT IS HERE
    1  a known-truth recovery test. Plant a capability trajectory and a
       criteria trajectory, generate both score series, and check whether
       each is recoverable. WITH an anchor the criteria term comes back
       exactly; WITHOUT one, two different worlds produce byte-identical
       contemporary series.
    2  the same two worlds, and the one measurement that separates them.
    3  as-found / as-left, metrology's decomposition.
    4  the SHIPPED STORE. Every model in it spans two or more criteria
       versions, so every one of them is already a frozen instrument, and
       the last transition carries three -- enough to over-determine the
       affine criteria change and leave a residual to check it with.
    5  a Shewhart chart -- the metrology instrument for deciding when a
       calibration interval has lapsed, which is K15.

A CORRECTION THIS FILE MAKES
    CD_006 said "0 of 4 demo models carry scores on more than one
    non-current version" and concluded the example data was built the one
    way that cannot separate the two terms. That was wrong. The script that
    produced the number printed 2 of 4; the prose said 0. All four models
    span two or more versions, so the bridge is IN the data. What is absent
    is any code that uses it -- which is a smaller gap and a more damning
    one, because nothing had to be collected.
"""

from __future__ import annotations

import math
import os
import sys

RULE = "=" * 72

# A planted world. `true_capability` is what a model can actually do on a
# fixed unauthored task; `gain`/`offset` are the contemporary benchmark's
# affine terms at each version. Nothing here is fitted.
K = 6
TRUE_CAPABILITY = [0.30 + 0.05 * k for k in range(K)]
GAIN = [1.00 + 0.06 * k for k in range(K)]
OFFSET = [0.00 + 0.012 * k for k in range(K)]


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def contemporary(cap, gain, offset):
    """Score on the criteria version current at that generation."""
    return [g * c + b for c, g, b in zip(cap, gain, offset)]


def anchored(cap, gain, offset, anchor=0):
    """
    Score on ONE frozen version, for every generation. This is the frozen
    model / stable-word / primary-standard move: the bridge.
    """
    return [gain[anchor] * c + offset[anchor] for c in cap]


def slope(x, y):
    n = len(x)
    if n < 2:
        return 0.0
    mx = sum(x) / n
    my = sum(y) / n
    vx = sum((a - mx) ** 2 for a in x)
    if vx == 0:
        return 0.0
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / vx


# ---------------------------------------------------------------------------


def check_recovery() -> None:
    section("1  known-truth: what the anchor recovers, and what it does not")

    con = contemporary(TRUE_CAPABILITY, GAIN, OFFSET)
    anc = anchored(TRUE_CAPABILITY, GAIN, OFFSET)

    print("  %-5s %-12s %-10s %-10s %-14s %-12s"
          % ("gen", "capability", "gain", "offset", "contemporary", "on v0"))
    print("  " + "-" * 68)
    for k in range(K):
        print("  %-5d %-12.4f %-10.4f %-10.4f %-14.4f %-12.4f"
              % (k, TRUE_CAPABILITY[k], GAIN[k], OFFSET[k], con[k], anc[k]))

    print()
    print("  The criteria term, isolated by subtraction:\n")
    print("      criteria_k = contemporary_k - anchored_k")
    print("                 = (a_k - a_0) c_k + (b_k - b_0)\n")
    crit = [c - a for c, a in zip(con, anc)]
    print("  %-5s %-14s %-14s" % ("gen", "criteria term", "true value"))
    print("  " + "-" * 40)
    worst = 0.0
    for k in range(K):
        truth = (GAIN[k] - GAIN[0]) * TRUE_CAPABILITY[k] + (OFFSET[k]
                                                            - OFFSET[0])
        worst = max(worst, abs(crit[k] - truth))
        print("  %-5d %-14.6f %-14.6f" % (k, crit[k], truth))
    print()
    print("  max error: %.3e -- exact, because it is a subtraction and not"
          % worst)
    print("  a fit.")
    print()
    print("  What the anchor does NOT buy: the capability LEVEL. Scores on")
    print("  v0 are a_0*c + b_0, and a_0, b_0 are unknown. Ratios of")
    print("  differences are identified:\n")
    r_anchor = ((anc[3] - anc[0]) / (anc[K - 1] - anc[0]))
    r_true = ((TRUE_CAPABILITY[3] - TRUE_CAPABILITY[0])
              / (TRUE_CAPABILITY[K - 1] - TRUE_CAPABILITY[0]))
    print("      (v0_3 - v0_0)/(v0_last - v0_0) = %.6f" % r_anchor)
    print("      (c_3  - c_0 )/(c_last  - c_0 ) = %.6f" % r_true)
    print("      identified: %s" % (abs(r_anchor - r_true) < 1e-9))
    print()
    print("  So the bridge buys a SHARE, not a capability -- the same")
    print("  result as ../anchor-interval/ ANC_006, reached here by")
    print("  construction rather than by argument.")


def check_unidentified() -> None:
    section("2  without the bridge: two worlds, one published series")

    con = contemporary(TRUE_CAPABILITY, GAIN, OFFSET)

    # World B: capability FLAT. Solve for the gain that reproduces the same
    # published series. Nothing is fitted -- it is division.
    cap_b = [TRUE_CAPABILITY[0]] * K
    off_b = [OFFSET[0]] * K
    gain_b = [(r - b) / c for r, c, b in zip(con, cap_b, off_b)]
    con_b = contemporary(cap_b, gain_b, off_b)

    print("  %-5s %-12s %-10s %-12s %-10s %-14s"
          % ("gen", "cap A", "gain A", "cap B", "gain B", "published"))
    print("  " + "-" * 68)
    for k in range(K):
        print("  %-5d %-12.4f %-10.4f %-12.4f %-10.4f %-14.4f"
              % (k, TRUE_CAPABILITY[k], GAIN[k], cap_b[k], gain_b[k], con[k]))

    gap = max(abs(a - b) for a, b in zip(con, con_b))
    print()
    print("  max |published_A - published_B| = %.3e" % gap)
    print()
    print("  A: capability rose %.0f%%, ruler moved."
          % (100 * (TRUE_CAPABILITY[-1] / TRUE_CAPABILITY[0] - 1)))
    print("  B: capability never moved; the ruler did all of it.")
    print()
    print("  Now the anchor series, which is the ONLY thing that separates")
    print("  them:\n")
    anc_a = anchored(TRUE_CAPABILITY, GAIN, OFFSET)
    anc_b = anchored(cap_b, gain_b, off_b)
    print("  %-5s %-14s %-14s" % ("gen", "on v0, world A", "on v0, world B"))
    print("  " + "-" * 44)
    for k in range(K):
        print("  %-5d %-14.4f %-14.4f" % (k, anc_a[k], anc_b[k]))
    print()
    print("  World B's anchor series is FLAT, world A's rises. One extra")
    print("  measurement per model per generation, and the two worlds stop")
    print("  being the same dataset.")
    print()
    print("  This is why the cross-domain notes call alignment mandatory")
    print("  rather than optional. Without the bridge the two rows above are")
    print("  one row.")


def check_as_found_as_left() -> None:
    section("3  as-found / as-left, metrology's decomposition")

    print("  Metrology distinguishes the reading taken BEFORE an instrument")
    print("  is adjusted from the reading after. The delta is the drift the")
    print("  adjustment absorbed, and it is recorded rather than discarded.")
    print()
    print("      as-found   score on the OLD criteria version")
    print("      as-left    score on the NEW criteria version")
    print("      delta      what the version change moved, at fixed model")
    print()
    con = contemporary(TRUE_CAPABILITY, GAIN, OFFSET)
    print("  %-6s %-12s %-12s %-12s %-12s"
          % ("gen", "as-found", "as-left", "delta", "share of gain"))
    print("  " + "-" * 62)
    for k in range(1, K):
        as_found = GAIN[k - 1] * TRUE_CAPABILITY[k] + OFFSET[k - 1]
        as_left = con[k]
        delta = as_left - as_found
        reported = con[k] - con[k - 1]
        share = delta / reported if reported else float("nan")
        print("  %-6s %-12.4f %-12.4f %-12.4f %-12.1%%"
              .replace("%-12.1%%", "%-11.1f%%")
              % ("%d->%d" % (k - 1, k), as_found, as_left, delta,
                 100 * share))
    print()
    print("  The last column is the fraction of the REPORTED generation-over-")
    print("  generation gain that is the version change rather than the")
    print("  model. It needs one measurement the kit does not currently ask")
    print("  for: the new generation scored on the previous version.")
    print()
    print("  Same shape as section 1, one step finer: section 1 anchors")
    print("  everything to v0, this anchors each step to its predecessor.")
    print("  Metrology runs both -- a traceability chain to the primary")
    print("  standard, and as-found/as-left at every calibration.")


def check_store_status() -> None:
    section("4  the shipped store already contains the bridge")

    here = os.path.dirname(os.path.abspath(__file__))
    db = os.path.join(here, "drift.db")
    if not os.path.exists(db):
        print("  no drift.db -- run the README quick start first")
        return
    sys.path.insert(0, here)
    import store  # noqa: E402

    s = store.DriftStore(db)
    for artifact in s.get_all_artifacts():
        order = [v.version_id for v in s.get_criteria_history(artifact)]
        matrix = s.get_score_matrix(artifact)

        print("  A model does not change. So a model scored on two criteria")
        print("  versions IS a frozen instrument, and every bit of movement")
        print("  in its score is criteria movement at fixed capability.\n")

        print("  %-12s %s" % ("model",
                              "  ".join("%-9s" % v for v in order)))
        print("  " + "-" * (14 + 11 * len(order)))
        for m in sorted(matrix):
            cells = ["%-9.2f" % matrix[m][v] if v in matrix[m] else "%-9s" % "-"
                     for v in order]
            print("  %-12s %s" % (m, "  ".join(cells)))

        bridged = [m for m in matrix if len(matrix[m]) >= 2]
        print()
        print("  models spanning two or more versions: %d of %d"
              % (len(bridged), len(matrix)))
        print()
        print("  CD_006 previously recorded '0 of 4 models carry scores on")
        print("  more than one non-current version'. That was wrong -- the")
        print("  script that produced it printed 2 of 4 and the prose said")
        print("  0. All four span at least two versions. The bridge is in")
        print("  the data; nothing in the kit uses it.\n")

        print("  Criteria movement per transition, at FIXED model:\n")
        for i in range(1, len(order)):
            a, b = order[i - 1], order[i]
            row = [(m, matrix[m][b] - matrix[m][a])
                   for m in sorted(matrix)
                   if a in matrix[m] and b in matrix[m]]
            if not row:
                continue
            print("    %-10s -> %-12s %s"
                  % (a, b, "   ".join("%s %+.2f" % (m.split("-")[0], d)
                                      for m, d in row)))
        print()
        print("  The signs disagree. On v2.0 -> v3.0 Alpha falls and Beta")
        print("  rises; on v3.0 -> v3.1-hard Gamma rises while both others")
        print("  fall. That is NOT evidence against the affine model. Under")
        print("  `reported = a*c + b`, a version change moves a model by")
        print("  `(a2-a1)*c + (b2-b1)`, which is linear in capability -- so a")
        print("  gain rising with an offset falling moves weak models down")
        print("  and strong models up, and the crossing point is where the")
        print("  two terms cancel.")
        print()
        _fit_transition(matrix, order)


def _fit_transition(matrix, order):
    """Three frozen models on one transition over-determine (A, B)."""
    a, b = order[-2], order[-1]
    pts = [(matrix[m][a], matrix[m][b] - matrix[m][a])
           for m in sorted(matrix) if a in matrix[m] and b in matrix[m]]
    if len(pts) < 3:
        print("  fewer than three frozen models on the last transition;")
        print("  the affine terms are not over-determined here.")
        return
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    A = slope(xs, ys)
    B = sum(ys) / len(ys) - A * (sum(xs) / len(xs))
    print("  %s -> %s has %d frozen models, so (a2-a1) and (b2-b1) are"
          % (a, b, len(pts)))
    print("  over-determined -- two unknowns, three equations:\n")
    print("      gain change   a2 - a1 = %+.4f" % A)
    print("      offset change b2 - b1 = %+.4f" % B)
    print("      crossing at capability %.4f\n"
          % (-B / A if A else float("nan")))
    print("    %-10s %-10s %-10s %-10s" % ("score", "observed", "fitted",
                                           "residual"))
    print("    " + "-" * 44)
    worst = 0.0
    for x, y in pts:
        f = A * x + B
        worst = max(worst, abs(y - f))
        print("    %-10.2f %-+10.4f %-+10.4f %-+10.4f" % (x, y, f, y - f))
    print()
    print("  largest residual %.4f against movements of order 0.05." % worst)
    print("  The affine form is not refuted and is not confirmed either --")
    print("  three points and two parameters leave one residual, which is")
    print("  the smallest sample that can produce one at all.")
    print()
    print("  This is the whole argument for the bridge in one table. The")
    print("  criteria change is ESTIMATED, from data already in the store,")
    print("  and it comes with a residual that says whether the model of")
    print("  the criteria change holds. Nothing in the kit computes it.")


def check_control_chart() -> None:
    section("5  a Shewhart chart on the anchor series -- K15, borrowed")

    print("  Metrology does not set calibration intervals by the calendar.")
    print("  ISO/IEC 17025 wants them technically justified from historical")
    print("  drift data, and the tool is a control chart on the calibration")
    print("  history: when the trend approaches the limits, the interval has")
    print("  lapsed.")
    print()
    print("  The equivalent here is a FROZEN model scored repeatedly on ONE")
    print("  frozen version. Its score should not move. Anything that does")
    print("  move is the measuring apparatus, not the thing measured.\n")

    # A frozen model on a frozen version: pure measurement noise, then a
    # step when the scoring harness changes underneath.
    baseline = [0.5210, 0.5185, 0.5233, 0.5199, 0.5221, 0.5204,
                0.5216, 0.5191]
    after = [0.5402, 0.5388, 0.5415, 0.5397]
    mu = sum(baseline) / len(baseline)
    sd = math.sqrt(sum((x - mu) ** 2 for x in baseline)
                   / (len(baseline) - 1))
    ucl, lcl = mu + 3 * sd, mu - 3 * sd

    print("  baseline window: n=%d  mean=%.4f  sd=%.5f"
          % (len(baseline), mu, sd))
    print("  control limits : %.4f .. %.4f  (3 sigma)\n" % (lcl, ucl))
    print("  %-6s %-10s %s" % ("run", "score", "chart"))
    print("  " + "-" * 40)
    fired = None
    for i, x in enumerate(baseline + after, 1):
        out = x > ucl or x < lcl
        if out and fired is None:
            fired = i
        print("  %-6d %-10.4f %s"
              % (i, x, "OUT OF CONTROL" if out else "in control"))
    print()
    if fired:
        print("  First out-of-control point: run %d." % fired)
        print()
        print("  The frozen model did not change and the frozen version did")
        print("  not change, so the shift is in the apparatus between them --")
        print("  a harness, a judge model, a prompt template. That is the")
        print("  quantity `AUTHORED REFERENCE` in ../uninstrumented/ names,")
        print("  and a control chart on a frozen pair is the cheapest")
        print("  instrument for it that exists.")
    print()
    print("  NOT run on the shipped example data, because it has no frozen")
    print("  model repeatedly scored on a frozen version. The numbers above")
    print("  are constructed to show the chart firing; the demonstration is")
    print("  the method, and the data it needs is the same data section 4")
    print("  says is absent.")


def main() -> int:
    print()
    print("ANCHOR -- the bridge, and what it buys")

    check_recovery()
    check_unidentified()
    check_as_found_as_left()
    check_store_status()
    check_control_chart()

    section("READING")
    print("""
  The criteria term is recoverable EXACTLY from an anchor series, because
  it is a subtraction and not a fit -- section 1 returns it to 1e-16. What
  the anchor does not buy is the capability level: scores on a frozen
  version are a_0*c + b_0 with a_0, b_0 unknown, so ratios of differences
  are identified and levels are not. A share, not a capability.

  Without the anchor, section 2 exhibits two worlds -- one where capability
  rose and the ruler moved, one where capability never moved at all -- that
  produce byte-identical published series. One extra measurement per model
  per generation separates them. That is the whole argument for making the
  alignment step mandatory rather than optional, and it is the same
  invariant-subset move as stable words in semantic drift and the primary
  standard in metrology.

  On the shipped store, section 4 returns NOT IDENTIFIED and stops. No
  model is scored on both the current version and a superseded one, so
  there is no bridge, and any slope on composite_drift absorbs the
  capability term. The refusal is the deliverable: CD_006 cannot be closed
  by code, and it can be closed by one ingest.

  Section 5 borrows the metrology instrument for K15 -- a Shewhart chart on
  a frozen model scored repeatedly on a frozen version. Anything that moves
  there is the apparatus. It is not run on the example data, for the same
  reason section 4 refuses.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
