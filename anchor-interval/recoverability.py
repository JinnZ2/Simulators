"""
recoverability.py -- provenance, not timing, decides whether a clean
reference can be re-acquired.

CC0-1.0. Standard library only. Deterministic (closed forms + seeded draws).

TWO POSITIONS THAT CANNOT BOTH HOLD IN THE SAME CONDITIONS

    drift-literature remedy      detect drift -> retrain on recent data
                                 presupposes a clean reference is obtainable
                                 on demand

    irrecoverability claim       a baseline is only acquirable during a
                                 stable interval; once the system is
                                 deviating, no clean reference exists to
                                 acquire

They are not two opinions about the same regime. They are two regimes, and
which one you are in is set by ONE measurable quantity: the fraction of the
re-acquisition pool that is downstream of the system being corrected.

    REGIME I   provenance independent of the system
               -> timing decides. Axis: shift interval / acquisition time.
               -> the sample, once taken, is clean.
               -> there is an optimal sample length, and it is finite.

    REGIME II  provenance downstream of the system
               -> timing is irrelevant. Error floors at f * b.
               -> sampling longer does not help. More data from the same
                  source.
               -> recoverable only by re-grounding on a reference the
                  system did not generate.

Sections 1 and 2 run the two regimes. Section 3 states the discriminating
measurement and what each side has to concede if it comes back the other way.
"""

from __future__ import annotations

import math
import random

RULE = "=" * 72
SEED = 20260816

SIGMA = 1.0          # per-sample measurement noise


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# ---------------------------------------------------------------------------
# 1  independent provenance -- timing decides


def regime_i(t_acq: int, t_shift: float) -> dict:
    """
    Acquisition needs t_acq consecutive steps inside one stable interval.
    Shifts arrive as a Poisson process with mean spacing t_shift, so the
    probability the window survives is exp(-t_acq / t_shift).

    On success the estimate has standard error SIGMA / sqrt(t_acq).
    On failure the reference is the pre-shift one, carrying the full
    displacement of the shift -- taken as 1.0 in these units.
    """
    p = math.exp(-t_acq / t_shift)
    clean = SIGMA / math.sqrt(t_acq)
    return {
        "t_acq": t_acq,
        "p_success": p,
        "err_on_success": clean,
        "expected_err": p * clean + (1 - p) * 1.0,
    }


def check_regime_i() -> None:
    section("1  REGIME I -- independent provenance: timing decides")

    print("  Acquisition needs t_acq consecutive stable steps. Shifts arrive")
    print("  with mean spacing t_shift. Sampling longer buys precision and")
    print("  costs survival probability, so there is an interior optimum.\n")

    for t_shift in (20.0, 60.0, 200.0):
        print("  t_shift = %.0f" % t_shift)
        print("    %-10s %-14s %-16s %-16s"
              % ("t_acq", "P(window)", "err | success", "expected err"))
        print("    " + "-" * 58)
        best = None
        for t_acq in (2, 5, 10, 20, 40, 80, 160):
            r = regime_i(t_acq, t_shift)
            print("    %-10d %-14.4f %-16.4f %-16.4f"
                  % (t_acq, r["p_success"], r["err_on_success"],
                     r["expected_err"]))
            if best is None or r["expected_err"] < best["expected_err"]:
                best = r
        # finer search for the actual optimum
        fine = min((regime_i(n, t_shift) for n in range(2, 400)),
                   key=lambda r: r["expected_err"])
        print("    optimum at t_acq = %d, expected err %.4f\n"
              % (fine["t_acq"], fine["expected_err"]))

    print("  The optimum is interior and finite, it MOVES with t_shift, and")
    print("  the expected error goes to zero as t_shift grows. Everything")
    print("  here is an argument about scheduling.")


# ---------------------------------------------------------------------------
# 2  downstream provenance -- timing is irrelevant


def regime_ii(checkpoints, f: float, bias: float, seed=SEED) -> dict:
    """
    The re-acquisition pool is a mix: fraction f of the samples passed
    through the system being corrected and carry its bias; the rest are
    independent. Averaging kills the variance and does not touch the bias.

    Returns the running mean at each checkpoint, so a column is one growing
    sample rather than independent draws per row.
    """
    rng = random.Random(seed)
    out, tot, n = {}, 0.0, 0
    for target in checkpoints:
        while n < target:
            b = bias if rng.random() < f else 0.0
            tot += b + rng.gauss(0.0, SIGMA)
            n += 1
        out[target] = abs(tot / n)
    return out


def check_regime_ii() -> None:
    section("2  REGIME II -- downstream provenance: sampling longer is inert")

    bias = 0.35
    fs = (0.0, 0.1, 0.3, 0.6, 1.0)
    checkpoints = (10, 100, 1000, 10000, 100000)

    print("  Pool is a mix. Fraction f of samples came through the system")
    print("  being corrected and carry its bias (%.2f here); the rest are"
          % bias)
    print("  independent. Averaging removes the variance, not the bias.\n")

    cols = {f: regime_ii(checkpoints, f, bias) for f in fs}
    print("  %-8s" % "n" + "".join("%-12s" % ("f=%.2f" % f) for f in fs))
    print("  " + "-" * 68)
    for n in checkpoints:
        print("  %-8d" % n + "".join("%-12.4f" % cols[f][n] for f in fs))
    print("  %-8s" % "floor" + "".join("%-12.4f" % (f * bias) for f in fs))
    print()
    print("  Every column with f > 0 converges to f x bias and stops. The")
    print("  10,000x increase in sample count between the first and last row")
    print("  buys nothing once the floor is reached.")
    print()
    print("  Sample count needed to reach an error of 0.05:")
    print("    %-10s %-16s" % ("f", "n required"))
    print("    " + "-" * 30)
    for f in (0.0, 0.1, 0.14, 0.3, 0.6, 1.0):
        floor = f * bias
        if floor >= 0.05:
            print("    %-10.2f %-16s" % (f, "unreachable at any n"))
        else:
            need = int(math.ceil((SIGMA / math.sqrt(0.05 ** 2 - floor ** 2))
                                 ** 2))
            print("    %-10.2f %-16d" % (f, need))
    print()
    print("  Above f = %.3f the target is not slow to reach. It is outside"
          % (0.05 / bias))
    print("  the reachable set, and no schedule changes that.")


# ---------------------------------------------------------------------------
# 3  the discriminating measurement


def check_discriminator() -> None:
    section("3  the measurement that decides which regime you are in")

    bias = 0.35
    print("  ONE number separates them:\n")
    print("      f = fraction of the re-acquisition pool that is downstream")
    print("          of the system being corrected\n")
    print("  and it is a provenance audit, not a statistical estimate. It is")
    print("  answered by labelling the pool, not by analysing it.\n")

    print("  Verdict column is against a STATED tolerance of 0.05, which is")
    print("  a choice and not a fact. Change the tolerance and the boundary")
    print("  moves; the floor does not.\n")
    print("  %-10s %-22s %-30s" % ("f", "error floor", "at tolerance 0.05"))
    print("  " + "-" * 64)
    for f in (0.00, 0.02, 0.10, 0.35, 0.70):
        floor = f * bias
        who = ("retrain remedy is sound" if floor < 0.05
               else "irrecoverability holds")
        print("  %-10.2f %-22.4f %-30s" % (f, floor, who))

    print()
    print("  So the contradiction resolves into a precondition nobody states.")
    print()
    print("    If f is near zero, K15 (baseline_freshness, in")
    print("    ../measurement-fork/) collapses into an ops step and the")
    print("    mediation prediction that rests on it fails.")
    print()
    print("    If f is not near zero, the retraining remedy has a hidden")
    print("    precondition. f is not among the quantities the remedy asks")
    print("    you to report, so a pipeline can satisfy every published step")
    print("    of it and still sit above the floor. Whether any given paper")
    print("    reports f is a literature question and is NOT checked here --")
    print("    the source drop's citation markers are unresolvable as")
    print("    delivered, so no literature claim in this folder is verified.")
    print()
    print("  Both sides lose something on a measurement neither has run.")
    print()
    print("  Second axis, separate from f and NOT settled by it: the")
    print("  irrecoverability position also asserts no stable plateau is")
    print("  guaranteed -- change is continuous, or the next shift arrives")
    print("  before the sample completes. That is section 1's t_shift, and")
    print("  it is a timing argument. f decides whether timing is even the")
    print("  right axis. Only if f is near zero does t_shift get to matter.")


# ---------------------------------------------------------------------------


def main() -> None:
    print()
    print("RECOVERABILITY: PROVENANCE FIRST, TIMING SECOND")

    check_regime_i()
    check_regime_ii()
    check_discriminator()

    section("READING")
    print("""
  The drift literature's remedy and the irrecoverability claim contradict
  each other only if they are read as claims about one regime. They are
  claims about two, and the regimes are separated by a single measurable
  quantity -- the downstream fraction f of the re-acquisition pool.

  In REGIME I the argument is entirely about scheduling: the optimal
  acquisition length is interior, finite, and moves with the shift
  interval.

  In REGIME II scheduling is inert. Error floors at f x bias, the floor is
  independent of sample count, and above f = 0.14 a 0.05 target is outside
  the reachable set at any n. Recovery is by re-grounding on a reference
  the system did not generate -- which is the anchor interval in
  corpus_loop.py, arrived at from the other end.

  f is a provenance audit, answered by labelling the pool. Nobody reports
  it, and both positions have something to lose depending on how it comes
  back.
""")


if __name__ == "__main__":
    main()
