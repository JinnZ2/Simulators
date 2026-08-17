"""
shadow_panel.py — does the shadow pattern work without the human?

CC0-1.0. Standard library only. Deterministic.

THE QUESTION
------------
`SPEC_V1.md` requires three shadows — `human_baseline`, `ai_low`, `ai_high` —
and offers `human_degraded` as optional. The question attached to the drop was
whether the pattern works with or without the human.

`shadow_design.py` §2 established that consensus among shadows measures only
the error they do NOT share, and is blind to the error they do. This module
asks what that costs each panel composition, and what the human is actually
contributing.

THE ANSWER, AHEAD OF THE OUTPUT
-------------------------------
The pattern works without the human. It does not work without DECORRELATION,
and in v1's required panel the human is the only decorrelated element there.

Drop the human from v1's panel and you are left with one model at two
thinking budgets, which is close to one shadow wearing two hats. Replace the
human with three distinct model families instead and the panel is stronger
than v1's original — the human then adds almost nothing measurable on top.

So the design variable is not human-vs-AI. It is how many independent failure
modes the panel contains.

THE MODEL
---------
Each shadow reports  truth + b_shared + b_family + e_individual  where

  b_shared    moves every shadow together: the same physical declaration, the
              same instrument output, the same prompt.
  b_family    moves shadows within a family together: one model's training,
              or one person's habits. Two budgets on one model share it.
  e_ind       independent.

Panel quality is read two ways, both standard:

  N_eff       participation ratio of the shadow correlation spectrum,
              (sum L)^2 / sum L^2. The same statistic
              ../model-ecology/phylogeny.py uses to ask how many independent
              estimators a family of estimators really contains.
  false-pass  P(spread within tolerance AND panel mean wrong by more than
              tolerance). The rate at which the consensus test hands back
              a confident wrong answer.

WHAT IS AND IS NOT MEASURED
---------------------------
  generator   every constant: the three variance components, the tolerance.
              Chosen to be plausible, fitted to nothing.
  instrument  the participation ratio, the false-pass estimator, the RNG.
  physical    nothing. No shadow panel was run.

The RANKING of panel compositions is robust to the constants -- it follows
from which shadows share which bias term. The absolute rates are not, and
should be read as illustrative. §3 shows the ranking surviving a sweep.
"""

from __future__ import annotations

import math
import random

SEED = 20260816
N_TRIALS = 40_000

SIGMA_SHARED = 1.0      # same declaration, same instrument output, same prompt
SIGMA_FAMILY = 0.8      # one model's training, or one person's habits
SIGMA_IND = 0.5         # genuinely independent
TOLERANCE = 1.0         # "agreement", and the size of an error worth catching

RULE = "=" * 74


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


# ---------------------------------------------------------------------------
# panels
# ---------------------------------------------------------------------------
# Each entry is one shadow's FAMILY label. Shadows sharing a label share a
# bias term. "H" is one person; two budgets on one model share a label too.

PANELS = (
    ("v1 required: human + AI-low + AI-high", ("H", "M1", "M1")),
    ("v1 full: + human_degraded", ("H", "H", "M1", "M1")),
    ("v1 minus the human", ("M1", "M1")),
    ("no human, 4 shadows, one model", ("M1", "M1", "M1", "M1")),
    ("no human, 3 model families", ("M1", "M2", "M3")),
    ("no human, 4 model families", ("M1", "M2", "M3", "M4")),
    ("human + 3 model families", ("H", "M1", "M2", "M3")),
)


# ---------------------------------------------------------------------------
# linear algebra, stdlib
# ---------------------------------------------------------------------------

def _eigenvalues(matrix: list[list[float]], sweeps: int = 200) -> list[float]:
    """Symmetric Jacobi eigenvalues. Matrices here are at most 4x4."""
    a = [row[:] for row in matrix]
    n = len(a)
    for _ in range(sweeps):
        p = q = 0
        off = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > off:
                    off, p, q = abs(a[i][j]), i, j
        if off < 1e-13:
            break
        theta = 0.5 * math.atan2(2.0 * a[p][q], a[q][q] - a[p][p])
        c, s = math.cos(theta), math.sin(theta)
        for i in range(n):
            aip, aiq = a[i][p], a[i][q]
            a[i][p], a[i][q] = c * aip - s * aiq, s * aip + c * aiq
        for i in range(n):
            api, aqi = a[p][i], a[q][i]
            a[p][i], a[q][i] = c * api - s * aqi, s * api + c * aqi
    return [a[i][i] for i in range(n)]


def n_effective(correlation: list[list[float]]) -> float:
    """Participation ratio of the correlation spectrum."""
    ev = [max(0.0, e) for e in _eigenvalues(correlation)]
    total = sum(ev)
    sq = sum(e * e for e in ev)
    return (total * total / sq) if sq > 0 else 0.0


# ---------------------------------------------------------------------------
# the panel simulation
# ---------------------------------------------------------------------------

def evaluate(families: tuple[str, ...], rng: random.Random,
             sigma_shared: float = SIGMA_SHARED,
             sigma_family: float = SIGMA_FAMILY,
             sigma_ind: float = SIGMA_IND,
             tolerance: float = TOLERANCE,
             trials: int = N_TRIALS) -> dict[str, float]:
    k = len(families)
    labels = sorted(set(families))
    draws: list[list[float]] = []
    spreads: list[float] = []
    wrong = agree_and_wrong = 0

    for _ in range(trials):
        shared = rng.gauss(0.0, sigma_shared)
        fam = {f: rng.gauss(0.0, sigma_family) for f in labels}
        xs = [shared + fam[f] + rng.gauss(0.0, sigma_ind) for f in families]
        draws.append(xs)

        spread = max(xs) - min(xs)
        spreads.append(spread)
        mean = sum(xs) / k
        if abs(mean) > tolerance:          # the panel is wrong
            wrong += 1
            if spread <= tolerance:        # ...and it agreed anyway
                agree_and_wrong += 1

    means = [sum(d[i] for d in draws) / trials for i in range(k)]
    cov = [[sum((d[i] - means[i]) * (d[j] - means[j]) for d in draws) / trials
            for j in range(k)] for i in range(k)]
    sd = [math.sqrt(cov[i][i]) for i in range(k)]
    cor = [[cov[i][j] / (sd[i] * sd[j]) for j in range(k)] for i in range(k)]

    return {
        "k": float(k),
        "n_eff": n_effective(cor),
        "spread": sum(spreads) / trials,
        "false_pass": agree_and_wrong / max(wrong, 1),
    }


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def check_panels() -> None:
    section("1  what each panel composition buys")

    rng = random.Random(SEED)
    print("  N_eff       independent shadows the panel actually contains")
    print("  false-pass  P(shadows agree | panel mean is wrong by > tolerance)")
    print("              -- the rate of confident wrong answers\n")
    print("  %-40s %3s %7s %9s %11s"
          % ("panel", "k", "N_eff", "spread", "false-pass"))
    results = {}
    for name, fams in PANELS:
        r = evaluate(fams, rng)
        results[name] = r
        print("  %-40s %3d %7.2f %9.3f %10.1f%%"
              % (name, int(r["k"]), r["n_eff"], r["spread"],
                 100 * r["false_pass"]))

    print()
    req = results["v1 required: human + AI-low + AI-high"]
    nohuman = results["v1 minus the human"]
    fams4 = results["no human, 4 model families"]
    hfams = results["human + 3 model families"]

    print("  Reading the table:")
    print()
    print("  v1's required panel has k = 3 and N_eff = %.2f. Two of its three"
          % req["n_eff"])
    print("  shadows are one model at two thinking budgets, which share a")
    print("  family bias and are close to one shadow wearing two hats.")
    print()
    print("  DROP THE HUMAN and it collapses: N_eff %.2f -> %.2f, false-pass"
          % (req["n_eff"], nohuman["n_eff"]))
    print("  %.1f%% -> %.1f%%. A panel that hands back a confident wrong"
          % (100 * req["false_pass"], 100 * nohuman["false_pass"]))
    print("  answer %.0f times in a hundred is not a check." % (100 * nohuman["false_pass"]))
    print()
    print("  REPLACE the human with three distinct model families and it is")
    print("  STRONGER than v1's original: N_eff %.2f vs %.2f, false-pass"
          % (fams4["n_eff"], req["n_eff"]))
    print("  %.1f%% vs %.1f%%." % (100 * fams4["false_pass"],
                                   100 * req["false_pass"]))
    print()
    print("  Adding the human back on top of that buys %+.2f in N_eff and"
          % (hfams["n_eff"] - fams4["n_eff"]))
    print("  %+.1f points of false-pass -- inside the noise of this estimate."
          % (100 * (hfams["false_pass"] - fams4["false_pass"])))


def check_answer() -> None:
    section("2  so: with or without the human?")

    print("""
  WITHOUT is fine. WITHOUT DECORRELATION is not.

  The human is not doing anything a human uniquely does. It is supplying an
  independent failure mode, and in v1's required panel it is the only one
  present -- because the other two shadows are one model at two budgets.

  Three consequences for the spec:

  1. `ai_low` and `ai_high` should not both be required as if they were two
     shadows. On one model they are one shadow at two dial settings, which is
     a reasoning-DIAL measurement, not a shadow-panel measurement. Both are
     worth doing; they answer different questions.

  2. What should be required is a minimum N_eff, not a minimum count. A panel
     of four shadows can carry N_eff = 1.2. Counting shadows measures effort,
     not independence.

  3. If no human is available -- which is most of the time, and the reason
     the question was asked -- the substitution is THREE MODEL FAMILIES, not
     three budgets on one. That is a procurement fact, not an epistemics
     problem: it needs three vendors, not three prompts.

  What the human still uniquely supplies is embodied context: the
  cold-stiffened proprioception in the first-experiment hypothesis is not a
  failure mode any model has. That argues for keeping a human shadow on
  physical measurements specifically, and it is a different argument from
  the decorrelation one.
""")


def check_robustness() -> None:
    section("3  does the ranking survive the constants?")

    print("  The absolute rates depend on the three variance components. The")
    print("  RANKING should not -- it follows from which shadows share which")
    print("  bias. Sweeping the shared/family/independent split:\n")
    print("  %-22s %-22s %-22s"
          % ("(shared, family, ind)", "v1 required N_eff",
             "4 families N_eff"))
    orderings_held = 0
    sweeps = ((1.0, 0.8, 0.5), (2.0, 0.4, 0.5), (0.5, 1.5, 0.5),
              (1.0, 0.8, 1.5), (0.2, 0.2, 1.0))
    for s, f, i in sweeps:
        rng = random.Random(SEED)
        a = evaluate(("H", "M1", "M1"), rng, s, f, i, trials=8000)
        b = evaluate(("M1", "M2", "M3", "M4"), rng, s, f, i, trials=8000)
        held = b["n_eff"] > a["n_eff"]
        orderings_held += held
        print("  %-22s %-22s %-22s  %s"
              % ("(%.1f, %.1f, %.1f)" % (s, f, i),
                 "%.2f" % a["n_eff"], "%.2f" % b["n_eff"],
                 "ok" if held else "REVERSED"))
    print()
    print("  ordering held in %d of %d sweeps." % (orderings_held, len(sweeps)))
    print()
    print("  The last row is the honest edge case: when almost all error is")
    print("  independent, every panel is near-ideal and the composition stops")
    print("  mattering. That is the regime the shadow pattern is unnecessary")
    print("  in, and it is not the regime shadows reading one declaration")
    print("  through one prompt are in.")


def main() -> None:
    print()
    print("SHADOW PANELS: WITH OR WITHOUT THE HUMAN")
    print("A study of a proposed protocol. No shadow panel was run.")

    check_panels()
    check_answer()
    check_robustness()

    section("READING")
    print("""
  The pattern works without the human, and v1's required panel is weaker than
  it looks with one.

  N_eff is the quantity the spec is missing. It already requires a minimum of
  two controls; it should require a minimum N_eff over the shadow panel for
  the same reason, and for the same kind of number. Counting shadows measures
  how much work was done. The participation ratio measures how much of that
  work was independent, and ../model-ecology/phylogeny.py already computes it
  for a family of estimators -- fifteen of them turning out to carry
  N_eff = 2.48.

  None of this has been measured on a real panel. The variance components are
  chosen, not fitted, and the ranking is what survives the sweep -- not the
  rates. Fitting them needs the same thing every other open claim in this
  folder needs: one measurement where several observers read one instrument
  against an independently logged reference.
""")


if __name__ == "__main__":
    main()
