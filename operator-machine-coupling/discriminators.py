# SPDX-License-Identifier: CC0-1.0
"""
The two shape discriminators the marker specifies. Both are built and
null-tested on CONSTRUCTED data; neither is a statement about any real
incident, operator, or organism.

1. error_vs_coupling -- operator error vs coupling failure.
   The marker: coupling failure correlates with time-on-THAT-unit, not with
   time-in-role, and drops sharply after familiarization while total
   experience stays flat. So the discriminator asks which of two predictors
   carries the drop, controlling for the other. When the two predictors are
   collinear (a new hire always on a new unit) it returns UNDETERMINED
   rather than a false attribution -- the exact confound the FAA study flags
   ("undetermined whether accidents reflect lack of flight hours or
   inexperience with the particular aircraft").

2. fixed_vs_convergence -- genotype matching vs coupling.
   The marker: genotype compatibility predicts a FIXED advantage, present
   from first contact and flat over the pairing's life; coupling predicts a
   CONVERGENCE CURVE, advantage accruing with time-in-pairing. The microbe
   case is the ideal control because it is fixed by construction.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

# ---- verdicts --------------------------------------------------------------
COUPLING_FAILURE = "COUPLING_FAILURE"
OPERATOR_ERROR = "OPERATOR_ERROR"
NO_SIGNAL = "NO_SIGNAL"
UNDETERMINED = "UNDETERMINED"

FIXED = "FIXED"
CONVERGENCE = "CONVERGENCE"

# [CHOICE 1] a partial slope below this magnitude counts as "flat". Scaled to
# outcomes normalized to unit spread; printed by the caller.
SLOPE_FLAT = 0.05
# [CHOICE 2] predictors more correlated than this cannot be separated -- the
# partial slopes are not identified, so the verdict is UNDETERMINED.
COLLINEAR = 0.9
# [CHOICE 3] a convergence curve must rise by at least this fraction of its
# asymptote from first contact; below it, the advantage is flat (FIXED).
RISE_FRAC = 0.25


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _corr(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = _mean(xs), _mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / (sxx ** 0.5 * syy ** 0.5)


def _solve3(A, y):
    """Solve a 3x3 linear system by Gaussian elimination. Returns None if
    singular."""
    M = [row[:] + [y[i]] for i, row in enumerate(A)]
    for c in range(3):
        piv = max(range(c, 3), key=lambda r: abs(M[r][c]))
        if abs(M[piv][c]) < 1e-12:
            return None
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(3):
            if r != c and abs(M[r][c]) > 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[0][3], M[1][3], M[2][3]]


def _partial_slopes(x1, x2, y):
    """OLS of y on [1, x1, x2]; return (b1, b2) the partial slopes, or None
    if not identified."""
    n = len(y)
    cols = ([1.0] * n, x1, x2)
    XtX = [[sum(cols[i][k] * cols[j][k] for k in range(n))
            for j in range(3)] for i in range(3)]
    Xty = [sum(cols[i][k] * y[k] for k in range(n)) for i in range(3)]
    beta = _solve3(XtX, Xty)
    if beta is None:
        return None
    return beta[1], beta[2]


def _normalize(y):
    """Scale outcomes to unit spread so SLOPE_FLAT is comparable across
    inputs (a G-RES-style guard: a slope is only 'flat' relative to the
    outcome's own spread)."""
    m = _mean(y)
    sd = (sum((v - m) ** 2 for v in y) / len(y)) ** 0.5 if y else 0.0
    if sd == 0:
        return [0.0 for _ in y], 0.0
    return [(v - m) / sd for v in y], sd


def error_vs_coupling(time_on_unit: List[float], time_in_role: List[float],
                      outcome: List[float]) -> str:
    """`outcome` is a failure score (higher = more failure). Returns which
    predictor carries the drop, or UNDETERMINED when the two are collinear,
    or NO_SIGNAL when neither moves it."""
    n = len(outcome)
    if n < 4 or not (len(time_on_unit) == len(time_in_role) == n):
        return NO_SIGNAL
    if abs(_corr(time_on_unit, time_in_role)) >= COLLINEAR:
        return UNDETERMINED
    y, sd = _normalize(outcome)
    if sd == 0:
        return NO_SIGNAL
    slopes = _partial_slopes(list(map(float, time_on_unit)),
                             list(map(float, time_in_role)), y)
    if slopes is None:
        return UNDETERMINED
    b_unit, b_role = slopes
    unit_drop = b_unit <= -SLOPE_FLAT
    role_drop = b_role <= -SLOPE_FLAT
    unit_flat = abs(b_unit) < SLOPE_FLAT
    role_flat = abs(b_role) < SLOPE_FLAT
    if unit_drop and role_flat:
        return COUPLING_FAILURE       # drops with time-on-unit, flat in role
    if role_drop and unit_flat:
        return OPERATOR_ERROR         # drops with role experience, not unit
    if unit_flat and role_flat:
        return NO_SIGNAL
    return UNDETERMINED               # both move it: not separable here


def fixed_vs_convergence(time_in_pairing: List[float],
                         advantage: List[float]) -> str:
    """Classify a pairing's advantage-over-time as FIXED (present from first
    contact, flat) or CONVERGENCE (accrues with time-in-pairing). The two
    lists are paired samples; they need not be sorted."""
    n = len(advantage)
    if n < 3 or len(time_in_pairing) != n:
        return UNDETERMINED
    pts = sorted(zip(time_in_pairing, advantage))
    ts = [p[0] for p in pts]
    ad = [p[1] for p in pts]
    if max(ad) <= 0:
        return UNDETERMINED           # no advantage to classify
    first = _mean(ad[:max(1, n // 4)])       # advantage near first contact
    plateau = _mean(ad[-max(1, n // 4):])    # advantage at the asymptote
    if plateau <= 0:
        return UNDETERMINED
    rise = (plateau - first) / plateau
    # a rising, correlated-with-time advantage that gains a real fraction of
    # its asymptote is a convergence curve; otherwise it is fixed.
    slope_sign = _corr(ts, ad)
    if rise >= RISE_FRAC and slope_sign > 0:
        return CONVERGENCE
    if rise < RISE_FRAC:
        return FIXED
    return UNDETERMINED


if __name__ == "__main__":
    import sys
    sys.stderr.write("discriminators.py is a library; its checks live in "
                     "operator-machine-coupling/selftest_omc.py.\n")
    sys.exit(2)
