# SPDX-License-Identifier: CC0-1.0
"""
The guardrail clock -- a separate layer, not a column.

The work order: safety/guardrail language shifts on news-time (months,
following public incidents), while C1-C7 move on training-cycle time. "Model
it as its own clock or it will contaminate the lag analysis in C6." This
module demonstrates that contamination on CONSTRUCTED data: a guardrail
series that moves on a news-time lag, pooled into the discard series, flips
the C6 lag reading away from the true training-time lag; separating the two
clocks recovers it.

Nothing here is a result. The series are constructed to exercise the
contamination; no real deprecation, incident, or discourse data is read.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import os
import sys
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import null_check as nc            # noqa: E402


def _discourse_series(n: int) -> List[float]:
    """A deterministic, APERIODIC discourse-volume series -- aperiodic so its
    autocorrelation peaks uniquely at zero shift, which is what makes the lag
    identifiable (a periodic series makes lags ambiguous mod its period). A
    small LCG stands in for the varied volume; no randomness at run time."""
    out, s = [], 1
    for _ in range(n):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        out.append(float((s >> 8) % 97))
    return out


def _lagged(x: List[float], L: int) -> List[float]:
    """y[t] = x[t-L] (discards follow discourse by L), zero before start."""
    return [x[t - L] if t - L >= 0 else 0.0 for t in range(len(x))]


def contamination_demo(true_lag: int = 20, guardrail_lag: int = 8,
                       guardrail_amp: float = 3.0, n: int = 72
                       ) -> Dict[str, object]:
    """Build discourse, discards (true training-time lag), and a guardrail
    series (news-time lag). Read the C6 lag two ways: on discards alone
    (separated) and on discards + guardrail pooled (contaminated)."""
    lags = list(range(0, 31))
    discourse = _discourse_series(n)
    discards = _lagged(discourse, true_lag)                 # training-time
    guardrail = [guardrail_amp * v for v in _lagged(discourse, guardrail_lag)]
    pooled = [d + g for d, g in zip(discards, guardrail)]   # news contaminates
    separated = nc.lag_of_peak(discourse, discards, lags)
    contaminated = nc.lag_of_peak(discourse, pooled, lags)
    return {
        "true_lag": true_lag,
        "separated_lag": separated,
        "contaminated_lag": contaminated,
        "contaminated": contaminated != separated,
        "separated_verdict": nc.c6_fad_driving(discourse, discards, lags),
        "contaminated_verdict": nc.c6_fad_driving(discourse, pooled, lags),
    }


if __name__ == "__main__":
    sys.stderr.write("guardrail_clock.py is a library; its checks live in "
                     "model-deprecation-backcast/selftest_mdb.py.\n")
    sys.exit(2)
