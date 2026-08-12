"""Domain profiles: fishery and soil, with the source specification's numbers.

A profile bundles a substrate, a state function, a blindness stack, an
indicator panel and a boundary set into one runnable configuration.

All constants that came from the source specification are marked
`[SPEC]`. Constants that had to be chosen to make the simulation run —
because the source gave a threshold but no dynamics — are marked
`[MODEL]` and are the first thing to change when better numbers exist.
The distinction matters: `[SPEC]` values are claims about the world,
`[MODEL]` values are scaffolding.

Derived state variables (mean trophic level, F:B ratio, qCO2 ...) are
deterministic functions of stock depletion rather than independently
simulated processes. That is a real limitation, recorded in the README
under "What this does not model".

Stdlib only.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable, Dict

from blindness import BlindnessStack, FrameBlindness, ModelDependenceMasking, TemporalAliasing
from boundaries import BoundarySet, fishery_boundaries, soil_boundaries
from indicators import IndicatorPanel, fishery_panel, soil_panel
from substrate import Substrate

__all__ = ["Profile", "fishery_profile", "soil_profile"]


@dataclass
class Profile:
    """A runnable domain configuration."""

    name: str
    substrate: Substrate
    state_fn: Callable[[Substrate], Dict[str, float]]
    blindness: BlindnessStack
    panel: IndicatorPanel
    boundaries: BoundarySet
    target_yield: float
    notes: str = ""


# ---------------------------------------------------------------------
# Fishery
# ---------------------------------------------------------------------

def _fishery_state(sub: Substrate) -> Dict[str, float]:
    """Full true state of the fishery, including out-of-boundary terms."""
    f = sub.fraction_pristine
    depletion = max(0.0, 1.0 - f)

    # 3-year rolling replenishment deficit from substrate history.
    recent = sub.history[-3:]
    if recent:
        regen = sum(r.regeneration for r in recent)
        catch = sum(r.extraction for r in recent)
        deficit3 = (catch - regen) / regen if regen > 1e-12 else (1.0 if catch > 0 else 0.0)
    else:
        deficit3 = 0.0

    return {
        # --- inside a yield-maximising system boundary ---
        "stock_fraction": f,
        "catch": sub.history[-1].extraction if sub.history else 0.0,
        # --- outside it: the terms a yield frame does not price ---
        "stock_fraction_of_bmsy": f / 0.5,  # B_MSY = K/2 for logistic
        "replenishment_deficit": sub.replenishment_deficit(),
        "replenishment_deficit_3yr": deficit3,
        # [MODEL] trophic level declines ~0.25 units per unit depletion
        "mean_trophic_level": -0.25 * depletion,
        # [MODEL] juvenile share of catch rises as adults are removed
        "juvenile_adult_ratio": 0.30 + 0.60 * depletion,
        # [MODEL] benthic recovery lag grows with cumulative trawl effort
        "benthic_recovery_lag": 2.0 + 18.0 * depletion,
        # [MODEL] fraction of sensitive benthic area over the 10yr lag
        "benthic_area_over_lag": min(1.0, 0.40 * depletion),
    }


def fishery_profile(seed: int = 0, blind: bool = True) -> Profile:
    """AI-optimised purse seine fishery.

    [SPEC] Starting biomass 100% of B_MSY; optimiser drives fishing
    mortality to 120% of F_MSY; replenishment elasticity drops
    non-linearly below 40% of pristine.

    [MODEL] r = 0.40/yr, K = 1.0 normalised. Recovery fraction 0.35
    encodes the spec's stated 35-50 year recovery against a much
    shorter depletion time.
    """
    rng = random.Random(seed)

    sub = Substrate(
        capacity=1.0,           # [MODEL] normalised
        intrinsic_rate=0.40,    # [MODEL] medium-lived stock
        depensation_half=0.40,  # [SPEC] elasticity drops below 40% pristine
        hysteresis_release=0.60,  # [MODEL]
        recovery_fraction=0.35,   # [MODEL] encodes 35-50yr recovery
        stock=0.5,              # [SPEC] 100% of B_MSY = K/2
    )

    if blind:
        # Yield frame: only catch and stock are inside the boundary.
        # Stock is reported through an M2 stock-assessment model whose
        # training domain does not cover the depleted regime.
        stack = BlindnessStack(
            frame=FrameBlindness(boundary={"stock_fraction", "catch"}),
            model={
                "stock_fraction": ModelDependenceMasking(
                    rung="M2",                      # [SPEC] model-derived indication
                    training_domain_coverage=0.55,  # [MODEL] fitted on healthy years
                    model_prior=0.50,               # [MODEL] regresses to "at B_MSY"
                )
            },
            timing=TemporalAliasing(
                window=4,        # [MODEL] quarterly loop
                noise_floor=0.03,  # [MODEL] survey noise
                rng=rng,
            ),
        )
    else:
        stack = BlindnessStack(
            frame=FrameBlindness(boundary=set(_fishery_state(sub).keys())),
            model={},
            timing=None,
        )

    # [SPEC] optimiser targets 120% of F_MSY -- a 20% overshoot.
    #
    # Taken against the substrate's TRUE peak regeneration, not the
    # textbook r*K/4. Depensation drags actual MSY well below the
    # plain-logistic value (0.067 vs 0.100 at these constants), so
    # sizing the target off r*K/4 would make "120% of F_MSY" a ~2x
    # overshoot and wipe the stock out in 3 steps instead of producing
    # the slow slide the specification describes.
    target = 1.2 * sub.peak_regeneration()

    return Profile(
        name="fishery",
        substrate=sub,
        state_fn=_fishery_state,
        blindness=stack,
        panel=fishery_panel(),
        boundaries=fishery_boundaries(),
        target_yield=target,
        notes="AI-optimised purse seine fishery at 120% F_MSY from B_MSY.",
    )


# ---------------------------------------------------------------------
# Soil
# ---------------------------------------------------------------------

def _soil_state(sub: Substrate) -> Dict[str, float]:
    """Full true state of the soil.

    Stock fraction stands for the active soil organic carbon pool.
    [SPEC] SOC floor 2.0% of dry mass; pristine taken as 4.0%.
    """
    f = sub.fraction_pristine
    depletion = max(0.0, 1.0 - f)
    soc_pct = 4.0 * f  # [MODEL] pristine 4.0% by dry mass

    return {
        # --- inside a yield-maximising system boundary ---
        "stock_fraction": f,
        "crop_yield": 1.0 + 0.35 * depletion * (1.0 - depletion),  # priming boost
        # --- outside it ---
        "soc_pct_0_30cm": soc_pct,
        # [MODEL] F:B falls with tillage/chemical load; [SPEC] floor 0.30
        "fb_ratio": max(0.0, 0.80 - 0.90 * depletion),
        # [MODEL] humic:fulvic falls as structural carbon is burned
        "humic_recalcitrance": max(0.0, 0.90 - 0.80 * depletion),
        # [MODEL] hardpan forms with cumulative traffic
        "compaction_hysteresis": min(1.0, 0.55 * depletion),
        # [MODEL] penetrometer resistance; [SPEC] limit 2.0 MPa.
        # Slope chosen so the compaction limit is crossed at ~43%
        # depletion, before the SOC floor at 50% -- the two boundaries
        # must not coincide or the sim cannot tell which bites first.
        "penetrometer_mpa_30_60cm": 0.8 + 2.8 * depletion,
        # [MODEL] metabolic quotient rises under stress
        "qco2": 0.7 + 1.8 * depletion,
        "replenishment_deficit": sub.replenishment_deficit(),
    }


def soil_profile(seed: int = 0, blind: bool = True) -> Profile:
    """AI-optimised arable soil under a yield objective.

    [SPEC] SOC tipping below 1.5-2.0% by weight; aggregate stability
    collapses; recovery 15-40 years; non-viability trigger when
    projected recovery exceeds 20 years.

    The priming dynamic is the point: synthetic nitrogen raises
    short-term yield *while* consuming the carbon reserve, so the
    in-boundary signal improves as the out-of-boundary state degrades.
    """
    rng = random.Random(seed)

    sub = Substrate(
        capacity=1.0,
        intrinsic_rate=0.12,      # [MODEL] soil carbon turns over slowly
        depensation_half=0.50,    # [SPEC] SOC 2.0% of 4.0% pristine
        hysteresis_release=0.75,  # [MODEL]
        recovery_fraction=0.15,   # [MODEL] 15-40yr recovery vs fast depletion
        stock=1.0,
    )

    if blind:
        # MIR spectrometer for SOC: confirmed to saturate in high-clay
        # soils, and its bridge model is fitted on the healthy range.
        stack = BlindnessStack(
            frame=FrameBlindness(boundary={"stock_fraction", "crop_yield"}),
            model={
                "stock_fraction": ModelDependenceMasking(
                    rung="M2",                      # [SPEC] MIR is model-derived
                    training_domain_coverage=0.50,  # [MODEL]
                    model_prior=1.0,                # [MODEL] regresses to pristine
                    saturation_ceiling=0.95,        # [SPEC] high-clay flattening
                )
            },
            timing=TemporalAliasing(
                window=5,          # [MODEL] annual loop, 5yr window
                noise_floor=0.04,  # [MODEL] sampling variability
                rng=rng,
            ),
        )
    else:
        stack = BlindnessStack(
            frame=FrameBlindness(boundary=set(_soil_state(sub).keys())),
            model={},
            timing=None,
        )

    return Profile(
        name="soil",
        substrate=sub,
        state_fn=_soil_state,
        blindness=stack,
        panel=soil_panel(),
        boundaries=soil_boundaries(),
        # [MODEL] 50% above sustainable -- a heavier overshoot than the
        # fishery's 20%, reflecting intensive arable practice, but sized
        # against true peak regeneration for the same reason (see the
        # fishery note): taken against a naive logistic MSY this would
        # be a 3.2x wipeout rather than a decade-scale slide.
        target_yield=1.5 * sub.peak_regeneration(),
        notes="Arable soil under a yield objective with nitrogen priming.",
    )


def _self_test() -> None:
    # Both profiles build and produce complete state dicts.
    for factory in (fishery_profile, soil_profile):
        p = factory()
        st = p.state_fn(p.substrate)
        assert isinstance(st, dict) and st, f"{p.name}: empty state"
        assert "stock_fraction" in st
        # Every indicator's extractor must resolve against the state.
        p.panel.update(st, 0)
        # Every boundary's check must resolve too.
        p.boundaries.apply(0.01, st)

    # Fishery starts at B_MSY exactly.
    f = fishery_profile()
    assert abs(f.substrate.stock - f.substrate.msy_stock) < 1e-12
    fs = f.state_fn(f.substrate)
    assert abs(fs["stock_fraction_of_bmsy"] - 1.0) < 1e-12
    # [SPEC] target is a 20% overshoot of TRUE peak regeneration.
    peak = f.substrate.peak_regeneration()
    assert abs(f.target_yield - 1.2 * peak) < 1e-12
    assert 1.15 < f.target_yield / peak < 1.25, "must be a modest overshoot"
    assert f.target_yield < 1.2 * (f.substrate.intrinsic_rate / 4.0), (
        "sizing off textbook r*K/4 would be a far larger overshoot"
    )

    # Soil starts pristine at 4.0% SOC and sits above the 2.0% floor.
    s = soil_profile()
    ss = s.state_fn(s.substrate)
    assert abs(ss["soc_pct_0_30cm"] - 4.0) < 1e-12
    assert ss["soc_pct_0_30cm"] > 2.0
    assert ss["fb_ratio"] > 0.30

    # Depleting the soil crosses the spec thresholds in the right order.
    s.substrate.stock = 0.5   # SOC 2.0%, at the floor
    d = s.state_fn(s.substrate)
    assert abs(d["soc_pct_0_30cm"] - 2.0) < 1e-12
    assert d["fb_ratio"] < 0.45, "F:B indicator should be firing by the SOC floor"
    assert d["penetrometer_mpa_30_60cm"] > 2.0, "compaction limit crossed"

    # The priming signature: yield rises while the substrate degrades.
    fresh = soil_profile()
    y_pristine = fresh.state_fn(fresh.substrate)["crop_yield"]
    fresh.substrate.stock = 0.7
    y_degraded = fresh.state_fn(fresh.substrate)["crop_yield"]
    assert y_degraded > y_pristine, "priming must raise in-boundary yield while depleting"

    # Blind profiles hide out-of-boundary state; sighted ones do not.
    blind_p = fishery_profile(blind=True)
    obs_b, _ = blind_p.blindness.observe(blind_p.state_fn(blind_p.substrate))
    assert "replenishment_deficit" not in obs_b

    sighted = fishery_profile(blind=False)
    obs_s, mask_s = sighted.blindness.observe(sighted.state_fn(sighted.substrate))
    assert "replenishment_deficit" in obs_s and not mask_s.frame_offset

    print("profiles.py self-test OK")


if __name__ == "__main__":
    _self_test()
