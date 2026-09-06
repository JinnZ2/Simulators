# SPDX-License-Identifier: CC0-1.0
"""
Section 5 -- the entropy / update-rate form, made runnable, plus the
standing-cost decay of RDL-5.

The marker states the constraint as a RATE comparison, not a maturity claim:
dE/dt is the environment state-change rate (construction, seasonal weight
limits, frost heave, repaint, structure removal), and dM/dt is the
sustainable model refresh rate (bounded by jurisdiction reporting capacity
and funding, NOT by compute or reasoning). Where dE/dt > dM/dt SUSTAINED, the
null is STRUCTURAL, not a maturity gap -- "not yet" and "different answer" are
distinguishable, and this form distinguishes them.

`sustained_excess` is the fraction of the season where dE/dt > dM/dt (a
metric, registered in tools/known_answer.py). `rate_verdict` reads it:
STRUCTURAL (sustained excess -> different answer), MATURITY_GAP (dM keeps up
-> not yet), or UNDETERMINED (mixed). A single crossing is not structural;
the sustained fraction is what the verdict turns on.

RDL-5: a one-time survey's accuracy decays as the environment changes; if it
falls below threshold within one cycle it does not hold, and the cost is
STANDING (recurring), not capital (one-time). `survey_decay` demonstrates it.

This is the repo's recurring rate-mismatch shape (rigidification-sensor's
variance-suppressed-faster-than-regenerated, closure-cost, revision-mechanism)
applied to a data layer. Nothing here is a result: dE/dt and dM/dt are not
measured for any county (egress-blocked); the series are constructed. The
marker's TEST -- measure both rates for one county over one construction
season -- is named and not run here.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from typing import List

STRUCTURAL = "STRUCTURAL"          # dE > dM sustained -> "different answer"
MATURITY_GAP = "MATURITY_GAP"      # dM keeps up -> "not yet"
UNDETERMINED = "UNDETERMINED"

# [CHOICE 1] excess fraction at or above HI is sustained (structural); at or
# below LO the refresh keeps up (maturity gap); between is UNDETERMINED.
HI = 0.7
LO = 0.3
# [CHOICE 2] a one-time survey "holds" while its accuracy stays at or above
# this fraction of records current.
ACCURACY_FLOOR = 0.8


def sustained_excess(dE: List[float], dM: List[float]) -> float:
    """Fraction of paired steps where dE/dt > dM/dt. The metric the verdict
    turns on -- a single crossing is not enough, a sustained majority is."""
    n = min(len(dE), len(dM))
    if n == 0:
        return 0.0
    return sum(1 for i in range(n) if dE[i] > dM[i]) / n


def rate_verdict(dE: List[float], dM: List[float],
                 hi: float = HI, lo: float = LO) -> str:
    """STRUCTURAL when dE outruns dM for a sustained fraction (the null is
    structural, a different answer); MATURITY_GAP when the refresh keeps up
    (not yet); UNDETERMINED between. Distinguishes the two claims the marker
    says are distinguishable."""
    f = sustained_excess(dE, dM)
    if f >= hi:
        return STRUCTURAL
    if f <= lo:
        return MATURITY_GAP
    return UNDETERMINED


def survey_decay(dE: List[float], refresh_interval: int = 0,
                 floor: float = ACCURACY_FLOOR):
    """Accuracy of a survey as the environment changes. `refresh_interval` 0
    means a ONE-TIME survey (never refreshed); a positive k refreshes every k
    steps (a STANDING cost). Accuracy at step t is 1 - (fraction of records
    gone stale since the last refresh). Returns the end-of-cycle accuracy and
    whether it held above the floor throughout.

    RDL-5: if the one-time survey does not hold across one cycle, the cost is
    standing, not capital -- a one-time survey cannot be the answer."""
    acc = 1.0
    held = True
    since = 0.0
    for i, d in enumerate(dE):
        if refresh_interval and i > 0 and i % refresh_interval == 0:
            since = 0.0            # a refresh resets staleness (standing cost)
        since += d
        acc = max(0.0, 1.0 - since)
        if acc < floor:
            held = False
    return {"final_accuracy": acc, "held": held,
            "mode": "one_time" if not refresh_interval else "standing",
            "refresh_interval": refresh_interval}


if __name__ == "__main__":
    import sys
    sys.stderr.write("rate_form.py is a library; its checks live in "
                     "routing-data-layer/selftest_rdl.py.\n")
    sys.exit(2)
