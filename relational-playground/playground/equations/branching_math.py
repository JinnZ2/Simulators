"""Branching-process arithmetic. Imports math only, so the repo registry can load it by path."""
import math


def extinction_probability(R, tol=1e-14):
    """P(the line started by ONE individual dies out), Poisson(R) offspring."""
    if R < 0:
        raise ValueError("R must be >= 0")
    if R <= 1.0:
        return 1.0
    q = 0.0
    for _ in range(100000):
        q2 = math.exp(R * (q - 1.0))
        if abs(q2 - q) < tol:
            return q2
        q = q2
    return q


def _poisson(rng, lam):
    if lam <= 0:
        return 0
    if lam > 30:                       # normal approximation, floored at 0; stated, not hidden
        return max(0, int(round(rng.gauss(lam, math.sqrt(lam)))))
    limit, k, prod = math.exp(-lam), 0, rng.random()
    while prod > limit:
        k += 1
        prod *= rng.random()
    return k
