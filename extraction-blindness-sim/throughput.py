"""Regenerative Throughput (RT) — competing formulations, kept apart.

The source specification supplies more than one mutually exclusive
definition of RT and does not reconcile them. This module implements
each one *as stated* rather than picking a winner, so the disagreement
is measurable instead of hidden behind a house style.

Five formulations and two trigger policies are provided. Which one is
correct is an open question recorded in `../README.md` and
`../CLAIM_TABLE.md`; `demonstrate_orientation_contradiction()` and
`demonstrate_caloric_sign_error()` show the two places they diverge in
sign, which is the part that actually matters for governance.

Stdlib only.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev
from typing import Sequence

__all__ = [
    "rt_as_written",
    "rt_inverted",
    "rt_soil_version_a",
    "rt_soil_version_b",
    "rt_soil_mass_balance",
    "absolute_trigger",
    "relative_trigger",
    "TriggerVerdict",
    "demonstrate_orientation_contradiction",
    "demonstrate_caloric_sign_error",
]

_EPS = 1e-12


# ---------------------------------------------------------------------
# General (fishery) formulations
# ---------------------------------------------------------------------

def rt_as_written(output: float, regenerative_capacity: float, reinvestment: float) -> float:
    """RT = Output / (Regenerative Capacity + Reinvestment). Source form.

    Reproduced exactly as specified. See
    :func:`demonstrate_orientation_contradiction` — under this
    orientation both remedies the source's own governance rule
    prescribes move RT *away* from its threshold.
    """
    denom = regenerative_capacity + reinvestment
    if abs(denom) < _EPS:
        return float("inf") if output > 0 else 0.0
    return output / denom


def rt_inverted(output: float, regenerative_capacity: float, reinvestment: float) -> float:
    """RT = (Regenerative Capacity + Reinvestment) / Output.

    The orientation the source's governance rule actually requires:
    reducing extraction or increasing reinvestment both raise RT, and
    ``RT > 1`` carries the natural meaning "regeneration exceeds
    extraction". Not what the source wrote; what its control logic
    needs.
    """
    if abs(output) < _EPS:
        return float("inf")
    return (regenerative_capacity + reinvestment) / output


# ---------------------------------------------------------------------
# Soil formulations (the two irreconcilable variants, plus a repair)
# ---------------------------------------------------------------------

def rt_soil_version_a(c_humified: float, bio_restored: float,
                      reinvestment_organic: float) -> float:
    """Version A — pure ratio.

    ``RT = C_humified / (Bio_restored + Reinvestment_organic)``
    """
    denom = bio_restored + reinvestment_organic
    if abs(denom) < _EPS:
        return float("inf") if c_humified > 0 else 0.0
    return c_humified / denom


def rt_soil_version_b(c_humified: float, bio_restored: float, c_caloric: float) -> float:
    """Version B — fraction plus an additive caloric term.

    ``RT = C_humified / (C_humified + Bio_restored) + C_caloric``

    The additive term is unbounded, so a large harvest can dominate the
    sum and push RT up while ``C_humified`` is falling. See
    :func:`demonstrate_caloric_sign_error`.
    """
    denom = c_humified + bio_restored
    frac = 0.0 if abs(denom) < _EPS else c_humified / denom
    return frac + c_caloric


def rt_soil_mass_balance(c_humified: float, bio_restored: float,
                         reinvestment_organic: float, c_caloric: float) -> float:
    """Mass-balance repair: remove harvested carbon before the ratio.

    ``RT = (C_humified - C_caloric) / (Bio_restored + Reinvestment_organic)``

    Carbon leaving in the harvest is a debit against the humified pool,
    not a credit added afterwards. This is the form the source's audit
    asks for ("must be deducted from C_humified before calculating the
    ratio, not added afterward") but never writes down.
    """
    denom = bio_restored + reinvestment_organic
    net = c_humified - c_caloric
    if abs(denom) < _EPS:
        return float("inf") if net > 0 else 0.0
    return net / denom


# ---------------------------------------------------------------------
# Trigger policies
# ---------------------------------------------------------------------

@dataclass
class TriggerVerdict:
    fired: bool
    value: float
    threshold: float
    policy: str
    reasoning: str = ""


def absolute_trigger(rt: float, threshold: float = 0.95) -> TriggerVerdict:
    """Fixed-threshold trigger. Source policy: RT < 0.95.

    Uncalibrated by construction: the same threshold is applied to
    substrates whose healthy baselines differ, so it both false-alarms
    on a naturally low-RT substrate and stays silent while a naturally
    high-RT substrate loses a large fraction of its base.
    """
    fired = rt < threshold
    return TriggerVerdict(
        fired=fired,
        value=rt,
        threshold=threshold,
        policy="absolute",
        reasoning=f"RT {rt:.4f} {'<' if fired else '>='} fixed threshold {threshold:.4f}",
    )


def relative_trigger(rt: float, baseline: Sequence[float], k: float = 2.0) -> TriggerVerdict:
    """Deviation-from-own-baseline trigger.

    Fires when `rt` falls more than `k` population standard deviations
    below the mean of this substrate's own historical baseline. Scale-
    free: a sandy soil with a naturally low RT is judged against its own
    history rather than a global constant.
    """
    if len(baseline) < 2:
        raise ValueError("relative_trigger needs at least 2 baseline samples")
    mu = mean(baseline)
    sigma = pstdev(baseline)
    threshold = mu - k * sigma
    fired = rt < threshold
    return TriggerVerdict(
        fired=fired,
        value=rt,
        threshold=threshold,
        policy="relative",
        reasoning=(
            f"RT {rt:.4f} vs baseline mean {mu:.4f} sd {sigma:.4f}; "
            f"{k:g}-sigma floor {threshold:.4f} "
            f"({'breached' if fired else 'intact'})"
        ),
    )


# ---------------------------------------------------------------------
# Contradiction demonstrations
# ---------------------------------------------------------------------

def demonstrate_orientation_contradiction(
    regen: float = 100.0, reinvest: float = 15.0, output: float = 105.0
) -> dict:
    """Show that RT-as-written moves the wrong way under its own remedies.

    The source's governance rule says that when RT falls below its floor
    the operator must "reduce extraction or invest more heavily in
    restoration". Under ``rt_as_written`` both of those *lower* RT.
    Under ``rt_inverted`` both raise it.
    """
    reduced_output = output * 0.857  # ~15% cut
    increased_reinvest = reinvest * 2.0

    written = {
        "baseline": rt_as_written(output, regen, reinvest),
        "reduce_extraction": rt_as_written(reduced_output, regen, reinvest),
        "increase_reinvestment": rt_as_written(output, regen, increased_reinvest),
    }
    inverted = {
        "baseline": rt_inverted(output, regen, reinvest),
        "reduce_extraction": rt_inverted(reduced_output, regen, reinvest),
        "increase_reinvestment": rt_inverted(output, regen, increased_reinvest),
    }
    return {
        "as_written": written,
        "inverted": inverted,
        "as_written_remedies_help": (
            written["reduce_extraction"] > written["baseline"]
            and written["increase_reinvestment"] > written["baseline"]
        ),
        "inverted_remedies_help": (
            inverted["reduce_extraction"] > inverted["baseline"]
            and inverted["increase_reinvestment"] > inverted["baseline"]
        ),
    }


def demonstrate_caloric_sign_error(
    c_humified_start: float = 1.0, c_humified_end: float = 0.7,
    bio_restored: float = 0.5, reinvestment: float = 0.3, c_caloric: float = 0.6
) -> dict:
    """Show Version B rising while the humified carbon pool falls.

    A 30% loss of humified carbon, with a harvest booked as a credit.
    Version B reports improvement; the mass-balance form reports the
    loss.
    """
    b_start = rt_soil_version_b(c_humified_start, bio_restored, 0.0)
    b_end = rt_soil_version_b(c_humified_end, bio_restored, c_caloric)
    mb_start = rt_soil_mass_balance(c_humified_start, bio_restored, reinvestment, 0.0)
    mb_end = rt_soil_mass_balance(c_humified_end, bio_restored, reinvestment, c_caloric)
    return {
        "c_humified_change": c_humified_end - c_humified_start,
        "version_b": {"start": b_start, "end": b_end, "delta": b_end - b_start},
        "mass_balance": {"start": mb_start, "end": mb_end, "delta": mb_end - mb_start},
        "version_b_masks_depletion": (b_end > b_start) and (c_humified_end < c_humified_start),
        "mass_balance_reports_depletion": mb_end < mb_start,
    }


def _self_test() -> None:
    # -- basic arithmetic -------------------------------------------
    assert abs(rt_as_written(105.0, 100.0, 15.0) - 105.0 / 115.0) < 1e-12
    assert abs(rt_inverted(105.0, 100.0, 15.0) - 115.0 / 105.0) < 1e-12
    assert abs(rt_soil_version_a(1.0, 0.5, 0.3) - 1.0 / 0.8) < 1e-12
    assert abs(rt_soil_version_b(1.0, 1.0, 0.25) - (0.5 + 0.25)) < 1e-12
    assert abs(rt_soil_mass_balance(1.0, 0.5, 0.3, 0.4) - 0.6 / 0.8) < 1e-12

    # Degenerate denominators do not raise.
    assert rt_as_written(1.0, 0.0, 0.0) == float("inf")
    assert rt_as_written(0.0, 0.0, 0.0) == 0.0
    assert rt_inverted(0.0, 1.0, 0.0) == float("inf")
    assert rt_soil_version_b(0.0, 0.0, 0.4) == 0.4

    # -- the two formulations genuinely disagree --------------------
    a = rt_soil_version_a(1.0, 0.5, 0.3)
    b = rt_soil_version_b(1.0, 0.5, 0.3)
    assert abs(a - b) > 0.1, "A and B must not be quietly equivalent"

    # -- orientation contradiction ----------------------------------
    d = demonstrate_orientation_contradiction()
    assert not d["as_written_remedies_help"], (
        "as-written orientation should fail its own governance remedies"
    )
    assert d["inverted_remedies_help"], "inverted orientation should satisfy them"
    assert d["as_written"]["reduce_extraction"] < d["as_written"]["baseline"]
    assert d["as_written"]["increase_reinvestment"] < d["as_written"]["baseline"]

    # -- caloric sign error -----------------------------------------
    c = demonstrate_caloric_sign_error()
    assert c["c_humified_change"] < 0, "scenario must actually lose carbon"
    assert c["version_b_masks_depletion"], "Version B should rise despite the loss"
    assert c["mass_balance_reports_depletion"], "mass-balance form should fall"

    # -- triggers ----------------------------------------------------
    assert absolute_trigger(0.90).fired
    assert not absolute_trigger(0.99).fired

    # A substrate whose healthy baseline sits below the fixed threshold
    # false-alarms on the absolute policy but is fine on the relative one.
    low_baseline = [0.92, 0.91, 0.93, 0.92, 0.92]
    assert absolute_trigger(0.92).fired, "absolute policy false-alarms on low-RT substrate"
    assert not relative_trigger(0.92, low_baseline).fired, "relative policy does not"

    # A substrate whose healthy baseline is high can lose a lot and stay
    # silent on the absolute policy while the relative one fires.
    high_baseline = [1.30, 1.28, 1.32, 1.29, 1.31]
    assert not absolute_trigger(1.05).fired, "absolute policy misses a large relative loss"
    assert relative_trigger(1.05, high_baseline).fired, "relative policy catches it"

    try:
        relative_trigger(1.0, [1.0])
        raise AssertionError("too-short baseline should raise")
    except ValueError:
        pass

    print("throughput.py self-test OK")


if __name__ == "__main__":
    _self_test()
