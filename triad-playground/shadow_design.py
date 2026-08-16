"""
shadow_design.py — does the shadow-sim pattern measure what it is for?

CC0-1.0. Standard library only. Deterministic.

THE QUESTION ASKED
------------------
`SOURCE_DROP.md` proposes a triad playground: every experiment is a tuple of
(physical system, measurement instrument, reasoning agent), each with its own
dial, and the point of the exercise is the cross-gradient — how an error in
one agent propagates through the others. The shadow-sim pattern runs the same
physical measurement past several reasoning agents and asks whether they
agree.

The question attached was whether that pattern works. Three checks below say:
the triad framing is right, and the protocol as written cannot deliver it.

  1  Step 5 forbids the design step 6 requires.
  2  Consensus among shadows is blind to the error shadows actually share.
  3  The proposed first experiment cannot fail its own skip condition.

A fourth section reads the worked aluminium example, which turns out to
demonstrate something other than what it is used to demonstrate.

WHAT IS AND IS NOT MEASURED
---------------------------
  generator   every constant below — the response coefficients, the bias and
              noise scales, the dial codings. Chosen to have the shape the
              protocol describes.
  instrument  the experimental design (OFAT vs factorial), the consensus rule.
  physical    the aluminium numbers in §3 only: CTE and a dial-indicator
              division are handbook values, not model outputs.

No triad experiment was run. This is a study of a proposed protocol.
"""

from __future__ import annotations

import itertools
import math
import random

RULE = "=" * 74
SEED = 20260816


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# ---------------------------------------------------------------------------
# 1  OFAT vs factorial
# ---------------------------------------------------------------------------
#
# A response over the three dials, with a deliberate interaction between the
# physical and reasoning dials. That interaction IS the cross-gradient the
# playground exists to measure: how much the reasoning dial matters depends on
# how good the physical model is.

MAIN_P, MAIN_I, MAIN_R, INTERACT_PR = 1.0, 0.5, 2.0, 3.0


def response(p: float, i: float, r: float) -> float:
    return MAIN_P * p + MAIN_I * i + MAIN_R * r + INTERACT_PR * (p * r)


def check_design() -> None:
    section("1  step 5 forbids the design step 6 requires")

    print("  The protocol says:")
    print("    step 5  'Never upgrade all three simultaneously (can't")
    print("             attribute variance).'")
    print("    step 6  'Cross-gradient: did conclusion change with dial")
    print("             setting?'")
    print()
    print("  Step 5 is one-factor-at-a-time. Step 6 asks for an interaction.")
    print("  OFAT cannot estimate an interaction, because no run in an OFAT")
    print("  design varies two factors together.\n")
    print("  Truth planted in the response: main effects P=%.1f I=%.1f R=%.1f,"
          % (MAIN_P, MAIN_I, MAIN_R))
    print("  interaction P*R = %.1f\n" % INTERACT_PR)

    base = response(0, 0, 0)
    ofat = {"P": response(1, 0, 0) - base,
            "I": response(0, 1, 0) - base,
            "R": response(0, 0, 1) - base}
    print("  OFAT, 4 runs, baseline plus one dial each:")
    for k, v in ofat.items():
        print("    %-4s %6.2f" % (k, v))
    predicted = base + ofat["P"] + ofat["R"]
    actual = response(1, 0, 1)
    print("    P*R  %6s   <- no run has both dials up" % "n/a")
    print()
    print("    OFAT predicts y(P=1, R=1) = %.1f. Truth = %.1f. Error = %.1f,"
          % (predicted, actual, actual - predicted))
    print("    which is the entire interaction, invisible and unattributed.")

    levels = (-1, 1)
    runs = {k: response(*k) for k in itertools.product(levels, repeat=3)}

    def contrast(term) -> float:
        return sum(term(*k) * v for k, v in runs.items()) / (len(runs) / 2)

    print("\n  2^3 factorial, 8 runs, orthogonal +/-1 contrasts:")
    for label, term, truth in (
            ("P", lambda p, i, r: p, 2 * MAIN_P),
            ("I", lambda p, i, r: i, 2 * MAIN_I),
            ("R", lambda p, i, r: r, 2 * MAIN_R),
            ("P*R", lambda p, i, r: p * r, 2 * INTERACT_PR),
            ("P*I", lambda p, i, r: p * i, 0.0)):
        print("    %-4s %6.2f   truth %6.2f" % (label, contrast(term), truth))
    print()
    print("  Every effect recovered exactly, interaction included, for four")
    print("  extra runs. The protocol's stated reason for OFAT -- 'can't")
    print("  attribute variance' -- is exactly backwards: a factorial design")
    print("  attributes variance to each factor AND to their interaction,")
    print("  which OFAT cannot do at any number of runs.")
    print()
    print("  Fix: replace step 5 with a 2^3 factorial over the three dials at")
    print("  low/high, then upgrade the axis with the largest effect. Eight")
    print("  runs is still cheap, and it is the only design that answers")
    print("  step 6.")


# ---------------------------------------------------------------------------
# 2  consensus is blind to shared error
# ---------------------------------------------------------------------------

def check_consensus() -> None:
    section("2  consensus among shadows is blind to what shadows share")

    print("  The protocol: 'Do the three agree? If not, the axis is")
    print("  underdetermined.' Read as a test, agreement is the pass.\n")
    print("  But the four shadows -- you rested, you fatigued, AI-low,")
    print("  AI-high -- are not independent. They read the same physical")
    print("  declaration, the same instrument output, and for the AI shadows")
    print("  the same prompt, written by one of the human shadows.\n")
    print("  Model each shadow as   truth + shared_bias + individual_noise.")
    print("  Spread across shadows measures individual_noise. It cannot see")
    print("  shared_bias at all, because shared_bias moves every shadow the")
    print("  same way.\n")

    rng = random.Random(SEED)
    truth, noise = 100.0, 1.0
    print("  %14s %14s %14s %12s" % ("shared bias", "mean shadow",
                                     "spread", "error vs truth"))
    for bias in (0.0, 2.0, 5.0, 20.0):
        trials = []
        for _ in range(4000):
            shared = rng.gauss(bias, 0.0)
            vals = [truth + shared + rng.gauss(0.0, noise) for _ in range(4)]
            trials.append((sum(vals) / 4, max(vals) - min(vals)))
        mean_est = sum(t[0] for t in trials) / len(trials)
        mean_spread = sum(t[1] for t in trials) / len(trials)
        print("  %14.1f %14.2f %14.2f %12.2f"
              % (bias, mean_est, mean_spread, mean_est - truth))
    print()
    print("  The spread column does not move. The error column tracks the")
    print("  bias one-for-one. Four shadows agreeing tightly at 120 when the")
    print("  truth is 100 is exactly what this looks like from inside.")
    print()
    print("  So 'do the shadows agree?' has no null. Before agreement means")
    print("  anything you need the disagreement between two runs of the SAME")
    print("  observer at the SAME dial -- the noise floor -- and a way to")
    print("  detect the shared term, which consensus cannot supply.")
    print()
    print("  Both already exist in this repo. ../divergence-playground/ is")
    print("  this protocol built with the null: readings are hash-sealed")
    print("  before reveal so later readers cannot anchor on earlier ones,")
    print("  spread is computed on three declared axes rather than eyeballed,")
    print("  and null_ensemble.py supplies shuffle and permutation nulls.")
    print("  Its agree_by_accident flag is the cell this protocol needs most:")
    print("  shadows that reach the same verdict by different mechanisms.")


# ---------------------------------------------------------------------------
# 3  the proposed first experiment
# ---------------------------------------------------------------------------

CTE_ALUMINIUM = 23.1e-6   # 1/K, handbook  [physical]
BAR_LENGTH_MM = 1000.0
DELTA_T = 60.0            # -40 C to +20 C
DIAL_DIVISION_MM = 0.01   # typical mechanical dial indicator  [physical]


def check_first_experiment() -> None:
    section("3  the first experiment cannot fail its own skip condition")

    expansion = CTE_ALUMINIUM * BAR_LENGTH_MM * DELTA_T
    print("  Aluminium bar, 1 m, %.1f ppm/K, %.0f K swing:" %
          (CTE_ALUMINIUM * 1e6, DELTA_T))
    print("    expansion            %8.3f mm" % expansion)
    print("    dial division        %8.3f mm" % DIAL_DIVISION_MM)
    print("    signal / division    %8.0f     -- the expansion is easy" %
          (expansion / DIAL_DIVISION_MM))
    print()
    print("  But the experiment is not about the expansion. It is about")
    print("  observer variance, and the skip condition reads:")
    print()
    print("    'If all four observers agree within instrument resolution,")
    print("     observer variance is negligible.'")
    print()
    reading = 0.5 * DIAL_DIVISION_MM
    print("    observer reading spread   ~%.4f mm  (half a division)" % reading)
    print("    instrument resolution      %.4f mm" % DIAL_DIVISION_MM)
    print("    ratio                      %.2f" % (reading / DIAL_DIVISION_MM))
    print()
    print("  Four people reading one mechanical dial agree to within a")
    print("  division because a division is the quantum of what the dial can")
    print("  say. The skip condition fires whether or not observer variance")
    print("  exists, so 'negligible' is a statement about the dial.")
    print()
    print("  This is null-harness's CONSTANT_SILENT: a gate that cannot fire")
    print("  has not been shown to work. It is also G-RES -- a null from an")
    print("  instrument that could not have seen the feature.")
    print()
    print("  The fix is cheap and does not need a better bar. The instrument")
    print("  must record independently of the observer reading it:")
    print("    - digital indicator with a data log, or a photograph of the")
    print("      dial timestamped at each reading")
    print("    - observer writes down a value without seeing the log")
    print("    - observer error = |observer value - logged value|, directly")
    print("  Observer variance stops being inferred from consensus and")
    print("  becomes a measured residual against a recorded reference.")
    print()
    print("  With that change the skip condition can fail, which is what")
    print("  makes running it worth anything.")


# ---------------------------------------------------------------------------
# 4  the worked example
# ---------------------------------------------------------------------------

def check_aluminium_example() -> None:
    section("4  the worked example shows a different failure than claimed")

    print("  From the drop, one physical dial setting, three reasoning dials:")
    print()
    print("    low     'crack at 200 cycles'        pattern-matched from a")
    print("                                          previous casting")
    print("    medium  'crack at 1,800 +/- 400'     propagated uncertainty")
    print("    high    'no crack; the heuristic was wrong because this is")
    print("             wrought, not cast'")
    print()
    print("  The drop reads this as a reasoning-dial cross-gradient, and as a")
    print("  G-LAYER violation: the reasoning claim outruns what the physical")
    print("  evidence carries.")
    print()
    print("  Run 3 says something else. It reports that runs 1 and 2 were")
    print("  answering a question about cast aluminium while the specimen is")
    print("  wrought. That is not the observer's gain varying against a fixed")
    print("  system -- it is the physical declaration being wrong, and the")
    print("  high-dial observer catching it.")
    print()
    print("  The distinction is load-bearing for the whole protocol. If a")
    print("  mis-specified physical system is scored as reasoning-dial")
    print("  variance, then every physical error the reasoning agent catches")
    print("  inflates the measured observer variance -- and the playground")
    print("  concludes the observer is unreliable when what happened is that")
    print("  the observer was right.")
    print()
    print("  Both are worth measuring; they are different quantities. The")
    print("  separator is whether the physical declaration survives the run.")
    print("  In triad.json that is `physical.state_declared` versus")
    print("  `physical.state_revised_during_run`, and a run that revises it")
    print("  reports a physical finding, not a reasoning gradient.")


def main() -> None:
    print()
    print("THE SHADOW-SIM PATTERN, TESTED")
    print("A study of a proposed protocol. No triad experiment was run.")

    check_design()
    check_consensus()
    check_first_experiment()
    check_aluminium_example()

    section("READING")
    print("""
  The triad framing holds and is the useful part. Naming the reasoning agent
  as an instrument with its own calibration is the move the rest of this repo
  has been circling: reasoning-gate tags quantities by layer,
  instrument-epistemology grades instruments, and neither has a slot for the
  observer. This does.

  The shadow-sim pattern, as specified, does not yet measure it.

  Step 5's one-factor-at-a-time rule forbids the only design that estimates
  the cross-gradient step 6 asks for. Consensus among shadows measures the
  error they do not share and is blind to the error they do -- which, for
  shadows reading one declaration through one prompt, is the larger term. And
  the proposed first experiment's skip condition fires regardless of the
  truth, because four people reading one mechanical dial agree to within a
  division by construction.

  All three have cheap fixes, and none of them requires abandoning the idea:
  a 2^3 factorial instead of OFAT; hash-sealed readings with a null ensemble,
  which ../divergence-playground/ already implements; and an instrument that
  logs independently of the observer reading it, which turns observer variance
  from something inferred by consensus into a measured residual.

  What this does not establish: that observer variance matters at any
  particular scale. Section 3's fix makes it measurable; nobody has measured
  it. The playground's first real result is still unrun, and it is one bar,
  one dial indicator, one afternoon.
""")


if __name__ == "__main__":
    main()
