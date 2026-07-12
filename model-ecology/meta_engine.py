"""
meta_engine.py
--------------
The observer is a measured component of the system, not a privileged vantage.

STABILITY LANDSCAPE
-------------------
Instead of "Model A is correct," the output is:

    "This conclusion is stable across 92% of mathematical frameworks
     and 95% of observer parameterizations."

That is a strictly stronger statement, and unlike a leaderboard it can be wrong
in a way you can see.

REPRESENTATION INVARIANCE
-------------------------
Transform the same problem into several representations and ask WHAT SURVIVES.
Structures that persist across every representation are candidates for real
invariants. Structures that appear in exactly one are candidates for artifacts
of that representation.

NOTE ON THE MANIFOLD
--------------------
`manifold` is registered here as ONE representation among several, scored by the
same pipeline as the rest. It gets no free pass. A framework whose stated purpose
is "what is the domain of validity of this mathematical framework?" cannot exempt
the currently fashionable representation from that question. If manifold structure
is real, it survives the audit. If it is a fad, the audit says so.

Falsifiable claims:
  M1. Observer-invariance is measurable: perturb ONLY observer parameters, hold
      data and models fixed, and measure rank churn in the model ranking.
      A conclusion is observer-invariant iff churn < tolerance.
  M2. A conclusion surviving k representations is more trustworthy than one
      surviving 1. REFUTED IF a single-representation conclusion outperforms
      multi-representation ones out of sample.

CC0. stdlib only.
"""

import math
import random
from core import Observer, REGISTRY, _mean, _std, pearson


# =============================================== representation transforms

@REGISTRY.representation("time")
def rep_time(x):
    return x[:]


@REGISTRY.representation("frequency")
def rep_frequency(x):
    n = len(x)
    m = sum(x) / n
    xd = [v - m for v in x]
    out = []
    for k in range(1, n // 2):
        re = sum(xd[t] * math.cos(2 * math.pi * k * t / n) for t in range(n))
        im = sum(xd[t] * math.sin(2 * math.pi * k * t / n) for t in range(n))
        out.append((re * re + im * im) ** 0.5)
    return out


@REGISTRY.representation("rank")
def rep_rank(x):
    order = sorted(range(len(x)), key=lambda i: x[i])
    r = [0] * len(x)
    for pos, i in enumerate(order):
        r[i] = pos
    return [float(v) for v in r]


@REGISTRY.representation("difference")
def rep_difference(x):
    return [x[i] - x[i - 1] for i in range(1, len(x))]


@REGISTRY.representation("manifold")
def rep_manifold(x, tau=3):
    """
    Delay-coordinate embedding projected to its first principal direction.
    Registered as ONE representation, audited like every other. No free pass.
    """
    pts = [(x[i], x[i + tau]) for i in range(len(x) - tau)]
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    c = [(p[0] - cx, p[1] - cy) for p in pts]
    sxx = sum(a * a for a, _ in c)
    syy = sum(b * b for _, b in c)
    sxy = sum(a * b for a, b in c)
    theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
    return [a * math.cos(theta) + b * math.sin(theta) for a, b in c]


# ============================================================ observer sweep

BASE_OBSERVERS = [
    Observer("parsimony_hawk",   simplicity_bias=0.9, uncertainty_bias=0.7,
             outlier_weight=0.1, determinism_bias=0.8, explain_vs_predict=0.8),
    Observer("outlier_hunter",   simplicity_bias=0.2, uncertainty_bias=0.2,
             outlier_weight=0.9, determinism_bias=0.2, explain_vs_predict=0.3),
    Observer("forecaster",       simplicity_bias=0.4, uncertainty_bias=0.8,
             outlier_weight=0.3, determinism_bias=0.6, explain_vs_predict=0.0),
    Observer("bayesian_dove",    simplicity_bias=0.3, uncertainty_bias=0.1,
             outlier_weight=0.5, determinism_bias=0.0, explain_vs_predict=0.6),
]


def sweep_observers(n: int = 32, seed: int = 7) -> list:
    """Random observer parameterizations, plus the four named archetypes."""
    rng = random.Random(seed)
    obs = list(BASE_OBSERVERS)
    for i in range(n - len(BASE_OBSERVERS)):
        obs.append(Observer(
            f"rand_{i}",
            simplicity_bias=rng.random(), uncertainty_bias=rng.random(),
            outlier_weight=rng.random(), determinism_bias=rng.random(),
            explain_vs_predict=rng.random()))
    return obs


def _spearman(a: list, b: list) -> float:
    return pearson(rep_rank(a), rep_rank(b))


def observer_sensitivity(models: list, results: dict, observers: list) -> dict:
    """
    M1. Hold data and models fixed. Vary ONLY the observer. Measure rank churn.

    churn = 1 - mean pairwise Spearman between rankings induced by observers.
    churn ~ 0 -> the conclusion does not depend on who is looking.
    churn ~ 1 -> the conclusion is an artifact of the observer.
    """
    rankings = []
    names = [m.name for m in models]
    for ob in observers:
        scores = [ob.score(m, results[m.name]) for m in models]
        rankings.append(scores)

    sims = []
    for i in range(len(rankings)):
        for j in range(i + 1, len(rankings)):
            sims.append(_spearman(rankings[i], rankings[j]))
    mean_sim = sum(sims) / len(sims) if sims else 1.0
    churn = 1.0 - mean_sim

    # who wins, under whom
    winners: dict = {}
    for ob, sc in zip(observers, rankings):
        w = names[max(range(len(sc)), key=lambda k: sc[k])]
        winners[w] = winners.get(w, 0) + 1

    return {"observer_churn": churn,
            "mean_rank_agreement": mean_sim,
            "invariant": churn < 0.25,
            "winners": dict(sorted(winners.items(), key=lambda kv: -kv[1])),
            "n_observers": len(observers)}


# ======================================================= representation audit

def representation_invariance(signal: list, conclusion_fn) -> dict:
    """
    M2. Apply `conclusion_fn` to the signal under every registered
    representation. Report which representations support the conclusion.

    conclusion_fn: list -> bool
    """
    support = {}
    for name, fn in REGISTRY.representations.items():
        try:
            support[name] = bool(conclusion_fn(fn(signal)))
        except Exception:
            support[name] = None      # representation could not be applied
    valid = [v for v in support.values() if v is not None]
    frac = sum(valid) / len(valid) if valid else 0.0
    return {"support": support,
            "fraction_supporting": frac,
            "n_representations": len(valid),
            "survives_all": frac == 1.0}


def stability_statement(framework_frac: float, observer_frac: float,
                        rep_frac: float, n_indep_families: int) -> str:
    return (
        f"stable across {framework_frac:6.1%} of mathematical frameworks, "
        f"{observer_frac:6.1%} of observer parameterizations, "
        f"{rep_frac:6.1%} of representations; "
        f"independent mathematical families: {n_indep_families}"
    )
