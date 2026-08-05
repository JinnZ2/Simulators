#!/usr/bin/env python3
"""
null_ensemble.py -- the only rigorous coincidence test.  stdlib only, CC0.

Protocol:

  1. State the match rule + tolerance, sealed  (use coincidence.C3Test).
  2. State the search space, N_trials.
  3. Build a null: shuffle, resample, or generate synthetic sets with
     the same STRUCTURE but no shared cause.
  4. Run the SAME search on the null, many times.
  5. p_empirical = P(null produces a hit as good as yours).
     Trials factor is included by construction because you ran the
     search on the null.

Nulls provided:

    shuffle_null       permute the values of one variable while keeping
                       the other fixed.  destroys any monotone
                       correlation.  cheapest.
    resample_null      IID sample with replacement from the marginal
                       of each variable.  destroys correlation and
                       joint structure both.
    permutation_test   swap labels between two groups; classic
                       nonparametric.  wraps random.shuffle.

For statistics that are simple enough (mean difference, correlation,
match count), the null_hits() runner returns the empirical p under any
match_rule callable.  Nothing here needs numpy.
"""

import random
from typing import Callable, List, Sequence, Tuple


# --- generic null-hits runner --------------------------------------------

def null_hits(observed_stat: float,
              null_generator: Callable[[random.Random], float],
              n_iter: int = 10000,
              two_sided: bool = False,
              seed: int = 42) -> dict:
    """
    Empirical p that the null generator produces a statistic >= observed_stat
    (or |stat| >= |observed_stat| if two_sided=True).
    """
    rng = random.Random(seed)
    hits = 0
    for _ in range(n_iter):
        s = null_generator(rng)
        if two_sided:
            if abs(s) >= abs(observed_stat):
                hits += 1
        else:
            if s >= observed_stat:
                hits += 1
    p = (hits + 1) / (n_iter + 1)          # add-one smoothing (never 0)
    return {"observed": observed_stat, "n_iter": n_iter,
            "hits_in_null": hits, "p_empirical": p,
            "two_sided": two_sided}


# --- null generators ------------------------------------------------------

def shuffle_null(xs: Sequence[float], ys: Sequence[float],
                 stat_fn: Callable[[Sequence[float], Sequence[float]], float]) \
        -> Callable[[random.Random], float]:
    """
    Return a generator that permutes ys against xs and returns stat_fn(xs, ys').
    Destroys any (xs, ys) correlation, preserves marginals.
    """
    xs = list(xs); ys = list(ys)
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have same length")

    def gen(rng: random.Random) -> float:
        ys_shuf = list(ys)
        rng.shuffle(ys_shuf)
        return stat_fn(xs, ys_shuf)
    return gen


def resample_null(xs: Sequence[float], ys: Sequence[float],
                  stat_fn: Callable[[Sequence[float], Sequence[float]], float]) \
        -> Callable[[random.Random], float]:
    """IID resample-with-replacement from each marginal.  Destroys joint."""
    xs = list(xs); ys = list(ys)
    n = len(xs)

    def gen(rng: random.Random) -> float:
        x_rs = [rng.choice(xs) for _ in range(n)]
        y_rs = [rng.choice(ys) for _ in range(n)]
        return stat_fn(x_rs, y_rs)
    return gen


def permutation_test(group_a: Sequence[float], group_b: Sequence[float],
                     stat_fn: Callable[[Sequence[float], Sequence[float]], float]) \
        -> Callable[[random.Random], float]:
    """Two-group label swap.  Classic nonparametric permutation."""
    pool = list(group_a) + list(group_b)
    n_a = len(group_a)

    def gen(rng: random.Random) -> float:
        p = list(pool); rng.shuffle(p)
        return stat_fn(p[:n_a], p[n_a:])
    return gen


# --- helpers: common stats -----------------------------------------------

def _mean(xs):
    return sum(xs) / len(xs)


def mean_diff(a, b):
    return _mean(a) - _mean(b)


def pearson(xs, ys):
    n = len(xs)
    mx, my = _mean(xs), _mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx2 = sum((x - mx) ** 2 for x in xs)
    dy2 = sum((y - my) ** 2 for y in ys)
    denom = (dx2 * dy2) ** 0.5
    return 0.0 if denom == 0 else num / denom


def match_count(xs, ys, target_diff: float = 0.0,
                tolerance: float = 0.05):
    """Number of (x, y) pairs whose difference is within tolerance of target."""
    return sum(1 for x, y in zip(xs, ys)
               if abs((x - y) - target_diff) <= tolerance)


# --- self-test ------------------------------------------------------------

def _t_perfect_correlation_beats_null():
    xs = list(range(50))
    ys = [2.0 * x + 1.0 for x in xs]           # r = 1
    stat = pearson(xs, ys)
    gen = shuffle_null(xs, ys, pearson)
    r = null_hits(stat, gen, n_iter=1000, two_sided=True, seed=0)
    assert r["p_empirical"] < 0.01
    assert stat > 0.99


def _t_noise_matches_null():
    rng = random.Random(7)
    xs = [rng.gauss(0, 1) for _ in range(200)]
    ys = [rng.gauss(0, 1) for _ in range(200)]
    stat = pearson(xs, ys)
    gen = shuffle_null(xs, ys, pearson)
    r = null_hits(stat, gen, n_iter=1000, two_sided=True, seed=1)
    assert r["p_empirical"] > 0.01, r        # not surprising vs null


def _t_match_count_null():
    # "how often do X and Y match within tol=0.5"; null shuffles ys
    rng = random.Random(3)
    xs = [rng.gauss(0, 1) for _ in range(100)]
    # ys correlated to xs so many pairs match
    ys = [x + rng.gauss(0, 0.2) for x in xs]
    observed = match_count(xs, ys, target_diff=0.0, tolerance=0.5)
    gen = shuffle_null(xs, ys,
                      lambda a, b: match_count(a, b, 0.0, 0.5))
    r = null_hits(observed, gen, n_iter=500, seed=1)
    assert r["p_empirical"] < 0.05, r


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass")


if __name__ == "__main__":
    _run()
