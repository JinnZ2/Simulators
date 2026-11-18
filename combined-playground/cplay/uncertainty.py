"""M9: distribution-to-mean information loss flag (COMBINED_SPEC section 8 rows 37, 39).

Built: row 39's flag, raised when a reported interval contains both mean^2 and E[X^2] of the
underlying distribution, so the interval cannot say which was propagated. When the two coincide
(no spread) the flag is raised and `coincide` is set, so the case is reported rather than hidden.

Interval propagation (row 37) is delegated, not copied: formula-audit numcheck, pin P10-numcheck.
"""
from collections import namedtuple

from . import tokens as T

PROPAGATION = T.Token("REFUSED", "not reimplemented here: interval propagation is delegated to formula-audit "
                      "numcheck (outward-rounded Fraction intervals), pin P10-numcheck (9c item 10)")


class UncertaintyError(ValueError):
    pass


MeanLoss = namedtuple("MeanLoss", "flag mean_sq e_x_sq coincide lo hi")


def mean_loss_flag(*, lo, hi, samples):
    if not samples:
        raise UncertaintyError("samples of the distribution required")
    if hi < lo:
        raise UncertaintyError("interval lo > hi")
    n = float(len(samples))
    m = sum(samples) / n
    msq, ex2 = m * m, sum(x * x for x in samples) / n
    flag = lo <= msq <= hi and lo <= ex2 <= hi
    return MeanLoss(flag, msq, ex2, msq == ex2, lo, hi)
