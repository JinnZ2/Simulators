# SPDX-License-Identifier: CC0-1.0
"""
The null per column, made runnable.

Each column's NULL is the condition under which it measures nothing. That is
exactly the repo's `null-harness` invariant one level up: a column whose
statistic reads the same regardless of input is a non-instrument, and the
work order requires the null stated so the non-reading is declarable rather
than mistaken for a measurement of zero. Every function here is checked in
both directions on CONSTRUCTED data (null-world -> the null verdict;
signal-world -> a reading), so no column is a constant classifier.

Nothing here is a result. No vendor calendar, poll, eval, or dataset is read
(all egress-blocked); the constructed series exist only to exercise the
statistics and their nulls.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# verdict constants
COLLAPSE = "COLLAPSE"
TWO_COLUMNS = "TWO_COLUMNS"
TIGHTENING = "TIGHTENING"
NO_TIGHTENING = "NO_TIGHTENING"
TRACKING = "TRACKING"
NOT_TRACKING = "NOT_TRACKING"
COLLAPSE_INTO_C4 = "COLLAPSE_INTO_C4"
DISTINCT = "DISTINCT"
RECOVERABLE = "RECOVERABLE"
UNRECOVERABLE = "UNRECOVERABLE"
DRIVING = "DRIVING"
NOT_DRIVING = "NOT_DRIVING"
DRIVING_OTHER_LAG = "DRIVING_OTHER_LAG"

# [CHOICE 1] a cross-correlation below this is "no peak" -- the fad axis is
# not driving at that lag. Printed by callers.
MIN_CORR = 0.5
# [CHOICE 2] the training/release lag band the work order names, in months.
LAG_BAND = (18, 24)
# [CHOICE 3] agreement at or above this collapses two columns into one.
COLLAPSE_TOL = 0.95
# [CHOICE 4] a slope of this magnitude (per unit distance, normalized) counts
# as varying-with-distance; below it, flat.
SLOPE_FLAT = 0.05


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def _corr(xs, ys):
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0
    xs, ys = xs[:n], ys[:n]
    mx, my = _mean(xs), _mean(ys)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / (sxx ** 0.5 * syy ** 0.5)


def _slope(xs, ys):
    n = min(len(xs), len(ys))
    if n < 2:
        return 0.0
    xs, ys = xs[:n], ys[:n]
    mx, my = _mean(xs), _mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx


# ---- C6: the fad-axis lag analysis (the strong, quantitative one) ----------

def lag_of_peak(discourse: List[float], discards: List[float],
                lags: List[int], min_corr: float = MIN_CORR
                ) -> Optional[int]:
    """The lag L at which discards best track discourse: argmax over L of
    corr(discourse[t], discards[t+L]). Returns None when no lag clears
    `min_corr` -- the null, 'the fad axis is not driving', declared rather
    than reported as a weak lag."""
    best_lag, best = None, min_corr
    for L in lags:
        if L >= 0:
            x = discourse[:len(discourse) - L]
            y = discards[L:]
        else:
            x = discourse[-L:]
            y = discards[:len(discards) + L]
        c = _corr(x, y)
        if c > best:
            best, best_lag = c, L
    return best_lag


def c6_fad_driving(discourse, discards, lags, months_per_step=1):
    """Verdict for C6: DRIVING (peak in the 18-24 month band), NOT_DRIVING
    (no peak clears min_corr -- the null), or DRIVING_OTHER_LAG (a peak, but
    outside the band -- the funding layer, not the surface fad)."""
    lag = lag_of_peak(discourse, discards, lags)
    if lag is None:
        return NOT_DRIVING
    months = lag * months_per_step
    lo, hi = LAG_BAND
    return DRIVING if lo <= months <= hi else DRIVING_OTHER_LAG


# ---- C1/C2 collapse --------------------------------------------------------

def c1c2_collapse(stated: List[float], measured: List[float],
                  tol: float = COLLAPSE_TOL) -> str:
    """If stated reasons match measured delta across the series, C1 and C2
    collapse to one column. Agreement is the correlation across the series."""
    if _corr(stated, measured) >= tol:
        return COLLAPSE
    return TWO_COLUMNS


# ---- C4 register tightening ------------------------------------------------

def c4_tightening(register_by_version: List[float]) -> str:
    """Hold one off-distribution input constant across versions, measure the
    returned register. NO_TIGHTENING (the null: C4 measures nothing) when the
    register is invariant across versions; TIGHTENING when it moves."""
    if len(register_by_version) < 2:
        return NO_TIGHTENING
    spread = max(register_by_version) - min(register_by_version)
    return TIGHTENING if spread > 1e-9 else NO_TIGHTENING


# ---- C5 usage depth / coupling ---------------------------------------------

def c5_tracks_coupling(distance_from_modal: List[float],
                       routed_elsewhere_ratio: List[float]) -> str:
    """The routed-elsewhere/routed-to-model ratio against distance from the
    modal user. NOT_TRACKING (the null: depth is not tracking coupling) when
    the ratio does not vary with distance."""
    if abs(_slope(distance_from_modal, routed_elsewhere_ratio)) < SLOPE_FLAT:
        return NOT_TRACKING
    return TRACKING


# ---- C7 -> C4 collapse ------------------------------------------------------

def c7_vs_c4(ontological_distance: List[float],
             per_turn_cost: List[float]) -> str:
    """Per-turn cost against ontological distance from the corpus.
    COLLAPSE_INTO_C4 (the null) when per-turn cost does not vary with
    distance; DISTINCT when it does (C7 is a real axis upstream of C4)."""
    if abs(_slope(ontological_distance, per_turn_cost)) < SLOPE_FLAT:
        return COLLAPSE_INTO_C4
    return DISTINCT


# ---- C2 unrecoverable (a state, not an estimate) ---------------------------

def c2_recoverable(eval_coverage_fraction: float,
                   min_coverage: float = 0.5) -> str:
    """If third-party eval coverage is too sparse to date deltas to version
    boundaries, C2 is UNRECOVERABLE and is declared so rather than
    estimated. Returns a STATE; the caller must not substitute a number."""
    return RECOVERABLE if eval_coverage_fraction >= min_coverage \
        else UNRECOVERABLE


# ---- C3 accepted-side censoring --------------------------------------------

EXIT_FORMS = ("complainer", "jumper", "paid_then_lapsed")


def c3_censoring(exits: List[Tuple[str, bool]]) -> Dict[str, object]:
    """`exits` is a list of (exit_form, was_paying). Only the 'complainer'
    form leaves a record; 'jumper' and 'paid_then_lapsed' are censored. The
    recorded complaint signal is therefore a biased (accepted-side) estimator
    of the discard-affected population, and among the recorded it carries a
    paying-tier filter. Returns the counts so the bias is a number, not an
    assertion."""
    total = len(exits)
    recorded = [e for e in exits if e[0] == "complainer"]
    censored = total - len(recorded)
    paying_recorded = sum(1 for e in recorded if e[1])
    return {
        "total_affected": total,
        "recorded": len(recorded),
        "censored": censored,
        "recorded_fraction": (len(recorded) / total) if total else None,
        "paying_tier_fraction_of_recorded":
            (paying_recorded / len(recorded)) if recorded else None,
        "note": "recorded is complainer-trace only; jumper and "
                "paid-then-lapsed leave no record (accepted-side data)",
    }


if __name__ == "__main__":
    import sys
    sys.stderr.write("null_check.py is a library; its checks live in "
                     "model-deprecation-backcast/selftest_mdb.py.\n")
    sys.exit(2)
