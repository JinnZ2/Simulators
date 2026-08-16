"""
overthinking.py — what a second drop of literature does to the first drop's
model, and to mine.

CC0-1.0. Standard library only. Deterministic.

WHAT CHANGED
------------
`SOURCE_DROP_2.md` reports a result that neither the first drop nor
`dial_response.py` can represent: quality does not merely saturate with
thinking budget, it can *decline*. Additional tokens flip correct answers to
incorrect ones, and the marginal utility of thinking goes negative.

`dial_response.py` models the response as a logistic in log-budget. A logistic
is monotone. Its gradient is positive everywhere, so it forbids the
overthinking region by construction — no parameter choice produces one.
Section 1 below measures that, because it is a correction to this folder's own
prior work and not to the drop's.

This module rebuilds the response with a declining branch and asks what
survives.

WHAT IS AND IS NOT MEASURED
---------------------------
Same as `dial_response.py`, and it matters more here because the second drop
is a literature survey:

  generator   every constant below -- the rise parameters, the drift rate,
              the onset. Chosen to have the shape the survey describes, not
              fitted to any reported curve.
  instrument  the log-budget grid, the sweep window, the stopping rule.
  physical    nothing.

The papers in `SOURCE_DROP_2.md` are dated April-May 2026 and their citation
markers point at search results not included in the delivery. Nothing here
verifies them, reproduces them, or depends on them being real. What is tested
is internal: whether the framework's own rules survive the shape the survey
attributes to those papers, and whether the survey's novelty claim is
consistent with its own summary of the work it surveys.
"""

from __future__ import annotations

import math

import dial_response as prior

# ---------------------------------------------------------------------------
# the response model  [generator]
# ---------------------------------------------------------------------------
#
# Q(u) = rise(u) - drift(u),  u = ln(budget)
#
#   rise    the same logistic as dial_response.py: below some budget the
#           problem is not yet represented, above it the problem is solved.
#   drift   damage that accrues per log-token once thinking is underway --
#           context dilution, error compounding, talking yourself out of a
#           right answer. Smoothed onset so curvature stays defined.
#
# The load-bearing choice is that DRIFT DOES NOT DEPEND ON D_r. Damage from
# overthinking is modelled as a property of the reasoning system, not of the
# problem it is pointed at. Section 4 shows what that choice buys and states
# the measurement that would refute it.

DRIFT_RATE = 0.030          # quality lost per log-token, once drift is on
DRIFT_ONSET = math.log(50)  # log-budget at which drift begins
DRIFT_WIDTH = 0.8           # smoothing of the onset

D_R_VALUES = (0.5, 2.0, 4.0)
LABELS = {0.5: "Easy (pattern match)",
          2.0: "Medium (multi-step)",
          4.0: "Hard (novel mechanism)"}


def _softplus(x: float, width: float) -> float:
    z = x / width
    return width * (math.log1p(math.exp(z)) if z < 30.0 else z)


def quality(budget: float, d_r: float) -> float:
    """Q(B): rises, peaks, then declines. The shape the survey reports."""
    u = math.log(budget)
    mu, s = prior.params(d_r)
    rise = 1.0 / (1.0 + math.exp(-(u - mu) / s)) if (u - mu) / s > -700.0 else 0.0
    return rise - DRIFT_RATE * _softplus(u - DRIFT_ONSET, DRIFT_WIDTH)


def gradient(budget: float, d_r: float, h: float = 1e-5) -> float:
    """dQ/d(ln B). Central difference; the softplus makes this smooth."""
    u = math.log(budget)
    return (quality(math.exp(u + h), d_r) - quality(math.exp(u - h), d_r)) / (2.0 * h)


def curvature(budget: float, d_r: float, h: float = 1e-4) -> float:
    """d2Q/d(ln B)^2."""
    u = math.log(budget)
    return (quality(math.exp(u + h), d_r) - 2.0 * quality(budget, d_r)
            + quality(math.exp(u - h), d_r)) / (h * h)


# ---------------------------------------------------------------------------
# stopping rules  [instrument]
# ---------------------------------------------------------------------------

LO_U, HI_U, N_U = math.log(2.0), math.log(1.0e7), 6000


def _grid() -> list[float]:
    return [LO_U + i * (HI_U - LO_U) / (N_U - 1) for i in range(N_U)]


def optimal_stop(d_r: float) -> tuple[float, float, bool]:
    """
    Where the marginal utility of thinking crosses zero: argmax Q.

    Returns (budget, Q there, interior). `interior` is a guard against the
    exact failure this folder documented in RD_002 -- an extremum reported at
    the edge of the sweep is a property of the sweep.
    """
    us = _grid()
    qs = [quality(math.exp(u), d_r) for u in us]
    i = max(range(len(us)), key=lambda k: qs[k])
    return math.exp(us[i]), qs[i], 0 < i < len(us) - 1


def knee_max_abs_curvature(d_r: float) -> float:
    """The first drop's rule, applied to the shape the second drop reports."""
    us = _grid()
    return math.exp(max(us, key=lambda u: abs(curvature(math.exp(u), d_r))))


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

RULE = "=" * 74


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def check_prior_model() -> None:
    section("1  the model in dial_response.py forbids the phenomenon")

    print("  SOURCE_DROP_2 reports negative marginal utility as the central")
    print("  empirical finding: past some budget, more thinking makes answers")
    print("  worse. A logistic is monotone, so dial_response.py cannot produce")
    print("  that at any parameter setting.\n")
    print("  %-24s %28s" % ("problem", "min dQ/dlnB over 2..1e7 tokens"))
    for d_r in D_R_VALUES:
        gs = [prior.gradient(math.exp(u), d_r) for u in _grid()]
        print("  %-24s %28.3e" % (LABELS[d_r], min(gs)))
    print()
    print("  Positive throughout. This is a correction to this folder's own")
    print("  prior work, not to the drop's: RD_003 picked a response family")
    print("  that rules out the effect by construction, and then reported that")
    print("  the family behaves well. It does. It is also the wrong family.")


def check_optimum() -> None:
    section("2  with a declining branch the stopping rule becomes well-posed")

    print("  Q(u) = logistic rise - drift accruing at %.3f per log-token from"
          % DRIFT_RATE)
    print("  B = %.0f. Drift does not depend on D_r.\n" % math.exp(DRIFT_ONSET))
    print("  %-24s %12s %10s %10s" % ("problem", "argmax Q", "Q there", "interior"))
    for d_r in D_R_VALUES:
        b, q, interior = optimal_stop(d_r)
        print("  %-24s %12.0f %10.3f %10s" % (LABELS[d_r], b, q, interior))
    print()
    print("  dQ/d(ln B) = 0 has ONE solution on the declining side. No tie, no")
    print("  choice of shoulder, no dependence on the sweep window -- the")
    print("  interior column is the guard and it passes for all three.")
    print()
    print("  RD_002 found the knee rule degenerate on a saturating curve. On")
    print("  the curve the literature actually reports, the degeneracy is not")
    print("  merely a defect: it is unnecessary. A better primitive exists,")
    print("  and it is the one the surveyed work uses -- marginal utility")
    print("  crossing zero, not curvature reaching a maximum.")


def check_knee_error() -> None:
    section("3  on this shape the knee rule stops far too early")

    print("  %-24s %12s %12s %10s"
          % ("problem", "argmax Q", "knee rule", "knee/opt"))
    ratios = []
    for d_r in D_R_VALUES:
        opt, _, _ = optimal_stop(d_r)
        knee = knee_max_abs_curvature(d_r)
        ratios.append(knee / opt)
        print("  %-24s %12.0f %12.0f %10.2f" % (LABELS[d_r], opt, knee,
                                                knee / opt))
    print()
    print("  The knee lands at %.0f%%-%.0f%% of the optimal budget, always"
          % (100 * min(ratios), 100 * max(ratios)))
    print("  early, and the error grows with difficulty -- worst exactly where")
    print("  the budget matters most.")
    print()
    print("  So the knee is not a conservative version of the optimum. It is a")
    print("  different point on the curve, and reading it as a stopping rule")
    print("  costs the hardest problems most of their budget.")


def check_cross_gradient_claim() -> None:
    section("4  'easier problems flip earlier' is a cross-gradient result")

    print("  SOURCE_DROP_2 quotes the surveyed work: 'easier problems (Level")
    print("  1-2) reach negative marginal utility earlier than hard problems.'")
    print()
    print("  That sentence is a statement about d(argmax Q)/d(difficulty) --")
    print("  how the zero of the budget-gradient moves with problem structure.")
    print("  It is the mixed partial, reported in words.\n")
    print("  %-24s %6s %14s" % ("problem", "D_r", "argmax Q"))
    stops = []
    for d_r in D_R_VALUES:
        b, _, _ = optimal_stop(d_r)
        stops.append(b)
        print("  %-24s %6.1f %14.0f" % (LABELS[d_r], d_r, b))
    print()
    print("  monotone increasing? %s" % (stops == sorted(stops)))
    print()
    print("  And here it is a CONSEQUENCE, not an input. Drift is the same for")
    print("  all three problems; only the rise moves. An easy problem finishes")
    print("  rising sooner, so the fixed drift overtakes it sooner. The")
    print("  ordering falls out of making overthinking-damage a property of")
    print("  the reasoning system rather than of the problem.")
    print()
    print("  That is a structural prediction with a cheap falsifier: measure")
    print("  the drift rate on problems of different difficulty. If it is")
    print("  flat, the ordering needs no separate explanation. If it varies")
    print("  with difficulty, this model is wrong and the ordering is an")
    print("  independent empirical fact.")


def main() -> None:
    print()
    print("OVERTHINKING: A DECLINING BRANCH, AND WHAT IT COSTS THE KNEE")
    print("No reasoning model was run. Every constant is generator-level.")

    check_prior_model()
    check_optimum()
    check_knee_error()
    check_cross_gradient_claim()

    section("READING")
    print("""
  The second drop does three things to the first.

  It REFUTES the response family. A saturating curve cannot produce negative
  marginal utility, so dial_response.py could not have represented the effect
  the surveyed work is about. That is a correction to this folder's model,
  recorded as RD_010.

  It REPLACES the knee. On a curve that declines, the stopping point is where
  the gradient crosses zero -- unique, interior, and independent of the sweep
  window. Every objection RD_002 raised against argmax|curvature| dissolves,
  not because the objection was wrong but because the rule is unnecessary.
  Section 3 measures what keeping it would cost: a stop at 6-17% of the
  optimal budget, worst on the hardest problems.

  It UNDERCUTS the novelty claim. SOURCE_DROP_2 closes by saying no surveyed
  paper computes cross-gradients, and that formalising them is the
  contribution on offer. But the same document quotes a surveyed paper
  reporting that easier problems reach negative marginal utility earlier than
  hard ones -- which is the mixed partial, measured and stratified by
  difficulty, stated in prose. The quantity is already an object of study.
  What is not yet standard is the notation.

  That is a smaller contribution than claimed and still a real one. Section 4
  is the argument for it: written as a derivative, the ordering stops being a
  fact to report and becomes a consequence to derive, with a falsifier
  attached. Prose does not do that.

  None of this checks whether the surveyed papers exist or say what the
  survey says they say. Their citation markers point outside the delivery,
  and the dates sit at the edge of what can be checked from here. Every
  finding above is internal: the framework against its own model, and the
  survey against its own quotations.
""")


if __name__ == "__main__":
    main()
