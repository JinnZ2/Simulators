"""
dial_response.py — the thinking-dial as a measurable dimension, and a check
on the numbers a drop about it shipped.

CC0-1.0. Standard library only. Deterministic.

THE SUBJECT
-----------
`SOURCE_DROP.md` proposes treating a reasoning model's thinking budget as an
axis, and reading it with the same gradient machinery this repo uses for
physical fields:

    Quality = f(input, problem structure, thinking budget)
    dQ / d(log B)                 marginal value of one more thinking step
    d2Q / d(log B) d(difficulty)  cross-gradient: does thinking help HERE
    knee = point of maximum curvature

That is a real and usable idea. This module implements it, and then does the
one thing the drop did not: checks whether the table it published is what the
method produces.

THE TABLE UNDER TEST
--------------------
    Problem Type            D_r     Knee Location    Gradient at Knee
    Easy (pattern match)    0.5     ~26 tokens       0.21
    Medium (multi-step)     2.0     ~910 tokens      0.06
    Hard (novel mechanism)  4.0     ~66 tokens       0.12

with the accompanying prose: "For an easy problem, the knee is early and the
gradient is steep... For a hard problem, the knee is later and the gradient is
shallower."

Both columns contradict that sentence. The hard problem's knee (66) is
*earlier* than the medium problem's (910), and its gradient (0.12) is
*steeper*. This module shows the contradiction is not a typo: it is what a
max-absolute-curvature knee finder does to a family of saturating curves, and
it reproduces here on an independent implementation.

WHAT IS AND IS NOT MEASURED
---------------------------
Following the layer vocabulary in ../reasoning-gate/guards.json:

  generator   D_r, mu, s -- parameters of the response model chosen below.
              Not properties of any reasoning system. Nothing here licenses a
              claim about GPT-5, Claude, or any deployed model.
  instrument  the log-budget grid, the sweep window, the knee rule.
  physical    nothing. No reasoning model was run. This module is a study of
              a proposed measurement, not a measurement.

That distinction is the whole point of the exercise, and the drop's own text
concedes half of it: "D_r is a phenomenological parameter fit from the curve,
not a fundamental property like fractal dimension."
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# the response model  [generator]
# ---------------------------------------------------------------------------
#
# Quality saturates in log-budget. A logistic in ln(B) is the minimal form
# with the two features the drop's prose requires: a take-off (below some
# budget, thinking buys nothing because the problem is not yet represented)
# and a saturation (above some budget, thinking buys nothing because the
# problem is solved).
#
# D_r enters through both:
#   mu(D_r)  harder problems need more budget before thinking starts paying
#   s(D_r)   harder problems have a broader transition
#
# Both are monotone increasing, which is exactly what the drop's prose asserts.
# Any other monotone choice gives the same qualitative result; the point below
# does not depend on these constants.

MU0 = math.log(20.0)   # log-budget at which a D_r = 0 problem turns over
MU_SLOPE = 0.9
S0 = 0.45

# The three rows of the delivered table.
PROBLEMS = (("Easy (pattern match)", 0.5, 26.0, 0.21),
            ("Medium (multi-step)", 2.0, 910.0, 0.06),
            ("Hard (novel mechanism)", 4.0, 66.0, 0.12))


def params(d_r: float) -> tuple[float, float]:
    """(mu, s) for a problem of reasoning dimension d_r. Both monotone in d_r."""
    return MU0 + MU_SLOPE * d_r, S0 * (1.0 + d_r)


def quality(budget: float, d_r: float) -> float:
    """Q(B) in [0, 1]. Logistic in ln(B)."""
    mu, s = params(d_r)
    z = (math.log(budget) - mu) / s
    if z < -700.0:
        return 0.0
    return 1.0 / (1.0 + math.exp(-z))


def gradient(budget: float, d_r: float) -> float:
    """dQ/d(ln B), analytic."""
    mu, s = params(d_r)
    z = (math.log(budget) - mu) / s
    sig = 1.0 / (1.0 + math.exp(-z)) if z > -700.0 else 0.0
    return sig * (1.0 - sig) / s


def curvature(budget: float, d_r: float) -> float:
    """d2Q/d(ln B)^2, analytic."""
    mu, s = params(d_r)
    z = (math.log(budget) - mu) / s
    sig = 1.0 / (1.0 + math.exp(-z)) if z > -700.0 else 0.0
    return sig * (1.0 - sig) * (1.0 - 2.0 * sig) / (s * s)


# ---------------------------------------------------------------------------
# knee rules  [instrument]
# ---------------------------------------------------------------------------
#
# A logistic has TWO curvature extrema, at z = +/- ln(2 + sqrt 3) ~ +/-1.3170,
# and they are equal in magnitude and opposite in sign. Which one a knee finder
# returns depends entirely on which rule it uses -- and "maximum curvature",
# stated without a sign, does not pick one.

Z_SHOULDER = math.log(2.0 + math.sqrt(3.0))


def knee_saturation(d_r: float) -> float:
    """Diminishing-returns shoulder: where marginal value falls off fastest."""
    mu, s = params(d_r)
    return math.exp(mu + Z_SHOULDER * s)


def knee_takeoff(d_r: float) -> float:
    """Take-off shoulder: where marginal value starts climbing fastest."""
    mu, s = params(d_r)
    return math.exp(mu - Z_SHOULDER * s)


def knee_max_abs_curvature(d_r: float, lo: float = 1.0, hi: float = 1.0e4,
                           n: int = 4000) -> tuple[float, str]:
    """
    "Point of maximum curvature", read literally, on a discrete sweep.

    Returns (budget, which_shoulder). The two candidates tie exactly in the
    continuum, so the winner is decided by where grid points happen to fall
    and by whether each shoulder is inside the sweep window at all.
    """
    lo_u, hi_u = math.log(lo), math.log(hi)
    best_u, best = lo_u, -1.0
    for i in range(n):
        u = lo_u + i * (hi_u - lo_u) / (n - 1)
        c = abs(curvature(math.exp(u), d_r))
        if c > best:
            best, best_u = c, u
    mu, _ = params(d_r)
    return math.exp(best_u), ("take-off" if best_u < mu else "saturation")


# ---------------------------------------------------------------------------
# cross-gradient
# ---------------------------------------------------------------------------

def cross_gradient(budget: float, d_r: float, h: float = 1e-4) -> float:
    """d2Q / d(ln B) d(D_r), by central difference on D_r."""
    return (gradient(budget, d_r + h) - gradient(budget, d_r - h)) / (2.0 * h)


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

RULE = "=" * 74


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def check_table() -> None:
    section("1  the delivered table against its own prose")

    print("  Prose: 'For an easy problem the knee is early and the gradient is")
    print("  steep. For a hard problem the knee is later and the gradient is")
    print("  shallower.'\n")
    print("  %-24s %6s %12s %10s" % ("problem", "D_r", "knee (tok)", "gradient"))
    for name, d_r, knee, grad in PROBLEMS:
        print("  %-24s %6.1f %12.0f %10.2f" % (name, d_r, knee, grad))

    knees = [p[2] for p in PROBLEMS]
    grads = [p[3] for p in PROBLEMS]
    print()
    print("  knee increasing with D_r, as the prose requires?  %s   %s"
          % (knees == sorted(knees), [int(k) for k in knees]))
    print("  gradient decreasing with D_r, as the prose requires?  %s   %s"
          % (grads == sorted(grads, reverse=True), grads))
    print()
    print("  Neither. The hard problem's knee is 14x EARLIER than the medium")
    print("  problem's, and its gradient is twice as steep. The table and the")
    print("  sentence above it describe opposite behaviours.")


def check_monotone() -> None:
    section("2  a monotone model gives a monotone knee")

    print("  Q(B) logistic in ln B, with mu and s both increasing in D_r --")
    print("  the parameterisation the prose describes.\n")
    print("  %-24s %6s %14s %12s" % ("problem", "D_r", "knee_sat (tok)",
                                     "grad there"))
    for name, d_r, _, _ in PROBLEMS:
        b = knee_saturation(d_r)
        print("  %-24s %6.1f %14.1f %12.4f" % (name, d_r, b, gradient(b, d_r)))

    sat = [knee_saturation(p[1]) for p in PROBLEMS]
    grd = [gradient(knee_saturation(p[1]), p[1]) for p in PROBLEMS]
    print()
    print("  monotone increasing knee?    %s" % (sat == sorted(sat)))
    print("  monotone decreasing gradient? %s" % (grd == sorted(grd, reverse=True)))
    print()
    print("  So the prose is self-consistent and implementable. Whatever")
    print("  produced the delivered table, it was not this.")


def check_knee_degeneracy() -> None:
    section("3  'maximum curvature' does not name one point")

    print("  A logistic has two curvature extrema, at z = +/- %.4f, EQUAL in"
          % Z_SHOULDER)
    print("  magnitude and opposite in sign:\n")
    d_r = 2.0
    for label, b in (("take-off", knee_takeoff(d_r)),
                     ("saturation", knee_saturation(d_r))):
        print("    %-11s B = %9.1f   curvature = %+.6f"
              % (label, b, curvature(b, d_r)))
    tie = abs(abs(curvature(knee_takeoff(d_r), d_r))
              - abs(curvature(knee_saturation(d_r), d_r)))
    print("\n    |difference in magnitude| = %.3e  -- an exact tie" % tie)
    print()
    print("  A knee finder that maximises |curvature| is therefore choosing")
    print("  between two equal candidates. Nothing in the curve prefers either,")
    print("  so the winner is decided by which one is inside the sweep window.")
    print("  Same window, 1 to 1e4 tokens, over all three rows:\n")
    hi = 1.0e4
    print("  %-24s %6s %12s %12s %10s"
          % ("problem", "D_r", "knee (tok)", "shoulder", "sat in win"))
    picked = []
    for name, d_r, _, _ in PROBLEMS:
        b, which = knee_max_abs_curvature(d_r, hi=hi)
        picked.append(b)
        print("  %-24s %6.1f %12.1f %12s %10s"
              % (name, d_r, b, which, knee_saturation(d_r) <= hi))
    print()
    print("  Pattern: %s" % ["%.0f" % b for b in picked])
    print("  Delivered: %s" % ["%.0f" % p[2] for p in PROBLEMS])
    print()
    print("  Small, large, small -- non-monotone, and the flip happens at the")
    print("  same row. Different constants, same shape, because the shape is a")
    print("  property of the knee RULE and not of the model underneath it.")
    print()
    print("  The mechanism is compound. The exact tie means nothing in the")
    print("  curve prefers one shoulder. The window then decides: the hard")
    print("  problem's saturation shoulder sits at %.0f tokens, outside a 1e4"
          % knee_saturation(4.0))
    print("  window, so the only extremum left to find is the take-off one --")
    print("  and the reported knee collapses by an order of magnitude exactly")
    print("  where the problem got harder.")
    print()
    print("  A knee that moves when you change the plot range is a property")
    print("  of the plot range.")


def check_cross_gradient() -> None:
    section("4  the cross-gradient claim, which holds")

    print("  Claim: at a fixed budget, additional thinking helps least on")
    print("  trivial problems (already saturated) and least on very hard ones")
    print("  (the budget is not enough to matter), peaking in between.\n")
    budget = 1000.0
    print("  budget = %.0f tokens\n" % budget)
    print("  %8s %14s %16s" % ("D_r", "dQ/dlnB", "d2Q/dlnB dD_r"))
    rows = []
    for i in range(0, 33, 2):
        d_r = 0.25 * i
        g = gradient(budget, d_r)
        rows.append((d_r, g))
        print("  %8.2f %14.5f %16.5f" % (d_r, g, cross_gradient(budget, d_r)))
    peak = max(rows, key=lambda r: r[1])
    print()
    print("  gradient peaks at D_r = %.2f, interior to the swept range: %s"
          % (peak[0], 0.0 < peak[0] < rows[-1][0]))
    print("  cross-gradient changes sign there, as an interior peak requires.")
    print()
    print("  SUPPORTED. This is the drop's most useful idea and it survives")
    print("  implementation. It is also the one part that does not depend on")
    print("  locating a knee.")


def main() -> None:
    print()
    print("THE THINKING DIAL AS A DIMENSION")
    print("A study of a proposed measurement. No reasoning model was run.")
    print("Every quantity below is generator- or instrument-level.")

    check_table()
    check_monotone()
    check_knee_degeneracy()
    check_cross_gradient()

    section("READING")
    print("""
  The gradient framework transfers. dQ/d(log B) is a well-defined marginal
  value, the cross-gradient picks out where thinking is worth buying, and
  both are computable from any response curve you can measure.

  The knee does not transfer, and that is the finding. "Point of maximum
  curvature" is ambiguous on any saturating curve: there are two extrema of
  equal magnitude, one where returns start and one where they stop. Section 3
  reproduces the delivered table's non-monotone shape from that ambiguity
  alone. The fix is to say which shoulder you mean -- the saturation
  shoulder, for a stopping rule -- at which point section 2 shows the answer
  is monotone and matches the prose.

  This is the same defect as SIM-C in ../aperiodic-order-sim-stack/, on a
  completely unrelated substrate. There a knee detector fired on the largest
  of six comparable curvature peaks and landed on a local minimum of the
  curve it was meant to find the knee of. Here it fires on one of two exactly
  tied extrema. Both drops then read the location as a result.

  What none of this establishes: anything about a deployed reasoning model.
  D_r is a parameter of the curve chosen above, not a measured property of
  any system, and the drop says so itself before using it in an analogy to
  fractal dimension anyway. To make D_r physical you would have to fit it to
  measured quality-vs-budget curves from a real model, with the budget under
  your control and the quality scored by something that is not the model.
  That experiment is cheap and nobody in this chain has run it.
""")


if __name__ == "__main__":
    main()
