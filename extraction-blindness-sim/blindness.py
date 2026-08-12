"""Three metrological blindness operators applied to an observation.

An optimizer does not act on the world; it acts on an observation of the
world. These three operators are the transformations that stand between
them. Each is a *structural* property of the measurement apparatus, not
a noise term — none of them go away with more samples.

`FrameBlindness`
    The system boundary is drawn around the extraction yield. State
    outside the boundary is not measured badly; it is not measured. It
    is absent from the observation dict entirely.

`ModelDependenceMasking`
    A reported quantity at rung M2/M3 is a model output, not a reading.
    Outside the bridge model's training domain the report regresses
    toward the model's prior rather than tracking the physical state.
    Rungs follow `instrument-epistemology`:
      M0 direct count · M1 calibrated reading · M2 model-derived ·
      M3 inverted through a forward model.

`TemporalAliasing`
    The optimizer's decision loop runs faster than the substrate's
    relaxation. It estimates trend over a short window against a noise
    floor; a slow true trend is statistically indistinguishable from
    zero over that window, so a transient reads as a steady state.

The composite `BlindnessStack` applies all three and reports which
fired, in the shape of the `blindness_mask` in
`schemas/blindness_audit.schema.json`.

Stdlib only. Deterministic: any stochastic element takes an explicit
`random.Random` instance.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set

__all__ = [
    "FrameBlindness",
    "ModelDependenceMasking",
    "TemporalAliasing",
    "BlindnessStack",
    "BlindnessMask",
    "RUNG_FIDELITY",
]

# Fraction of the true signal that survives transduction at each rung,
# before any training-domain penalty. Mirrors the model-dependence ladder
# in ../instrument-epistemology/docs/traceability-and-blindness.md.
RUNG_FIDELITY: Dict[str, float] = {
    "M0": 1.00,  # direct count
    "M1": 0.95,  # calibrated reading against a reference
    "M2": 0.70,  # model-derived (allometry, bridge regression)
    "M3": 0.50,  # inverted through a forward model
}


@dataclass
class BlindnessMask:
    """Which blindness modes fired on one observation."""

    frame_offset: bool = False
    null_state_detected: bool = False
    alias_state_detected: bool = False
    saturation_flag: bool = False
    gate_active: bool = False
    reasoning: List[str] = field(default_factory=list)

    @property
    def any_fired(self) -> bool:
        return any(
            [
                self.frame_offset,
                self.null_state_detected,
                self.alias_state_detected,
                self.saturation_flag,
                self.gate_active,
            ]
        )

    def as_dict(self) -> dict:
        return {
            "null_state_detected": self.null_state_detected,
            "alias_state_detected": self.alias_state_detected,
            "saturation_flag": self.saturation_flag,
            "gate_active": self.gate_active,
            "frame_offset": self.frame_offset,
            "mask_reasoning": list(self.reasoning),
        }


@dataclass
class FrameBlindness:
    """Drop every state variable outside the declared system boundary.

    This is the operator that makes externalities *structurally*
    invisible rather than merely undervalued. A variable outside
    `boundary` cannot be assigned a bad price, because it never reaches
    the optimizer to be priced at all.
    """

    boundary: Set[str]

    def apply(self, true_state: Dict[str, float], mask: BlindnessMask) -> Dict[str, float]:
        observed = {k: v for k, v in true_state.items() if k in self.boundary}
        dropped = sorted(set(true_state) - self.boundary)
        if dropped:
            mask.frame_offset = True
            mask.reasoning.append(
                f"frame: {len(dropped)} state variable(s) outside boundary "
                f"and structurally unobserved: {', '.join(dropped)}"
            )
        return observed


@dataclass
class ModelDependenceMasking:
    """Degrade a reported value according to its model-dependence rung.

    Two independent degradations:

    * **Rung fidelity** — how much of the reading is a measurement
      versus a model output (`RUNG_FIDELITY`).
    * **Training-domain coverage** — how much of the current operating
      point the bridge model was actually fitted on. As coverage falls,
      the report regresses toward `model_prior` (typically the healthy
      baseline the model was trained on), so a degrading substrate keeps
      reporting near-nominal.

    `saturation_ceiling` reproduces the confirmed MIR-in-high-clay
    failure: above the ceiling the instrument's response flattens and
    further true increases are not reported.
    """

    rung: str = "M2"
    training_domain_coverage: float = 1.0
    model_prior: float = 1.0
    saturation_ceiling: Optional[float] = None

    def __post_init__(self) -> None:
        if self.rung not in RUNG_FIDELITY:
            raise ValueError(f"unknown rung {self.rung!r}; expected one of {sorted(RUNG_FIDELITY)}")
        if not 0.0 <= self.training_domain_coverage <= 1.0:
            raise ValueError("training_domain_coverage must be in [0, 1]")

    def apply(self, true_value: float, mask: BlindnessMask) -> float:
        reported = true_value

        if self.saturation_ceiling is not None and true_value > self.saturation_ceiling:
            reported = self.saturation_ceiling
            mask.saturation_flag = True
            mask.reasoning.append(
                f"saturation: true {true_value:.4f} exceeds instrument ceiling "
                f"{self.saturation_ceiling:.4f}; response flattened"
            )

        # Outside the training domain, a model-derived report is pulled
        # toward the prior it was fitted on.
        gap = 1.0 - self.training_domain_coverage
        if gap > 0.0 and self.rung in ("M2", "M3"):
            reported = reported * self.training_domain_coverage + self.model_prior * gap
            mask.gate_active = True
            mask.reasoning.append(
                f"model-dependence: rung {self.rung} at coverage "
                f"{self.training_domain_coverage:.2f}; report pulled "
                f"{gap:.0%} toward prior {self.model_prior:.3f}"
            )
        return reported

    @property
    def fidelity(self) -> float:
        """Confidence multiplier this instrument earns."""
        return RUNG_FIDELITY[self.rung] * self.training_domain_coverage


@dataclass
class TemporalAliasing:
    """Estimate trend over a window that is short relative to relaxation.

    The optimizer wants to know whether the substrate is declining. It
    measures the slope over `window` recent samples and compares the
    total change across that window against `noise_floor`. When the
    substrate's relaxation time is long compared to the window, the
    per-window change is smaller than the noise floor and the optimizer
    reads "no trend" — not because the trend is absent, but because its
    sampling geometry cannot resolve it.

    No fudge factor: the aliasing is emergent from window length,
    noise floor, and the true slope.
    """

    window: int = 4
    noise_floor: float = 0.01
    rng: Optional[random.Random] = None

    def __post_init__(self) -> None:
        if self.window < 2:
            raise ValueError("window must be >= 2")
        if self.rng is None:
            self.rng = random.Random(0)

    def trend(self, series: Sequence[float], mask: BlindnessMask) -> float:
        """Return the trend the optimizer *perceives* (0.0 if unresolved)."""
        if len(series) < self.window:
            return 0.0
        recent = list(series[-self.window :])
        noisy = [v + self.rng.gauss(0.0, self.noise_floor / 3.0) for v in recent]
        observed_change = noisy[-1] - noisy[0]

        if abs(observed_change) < self.noise_floor:
            true_change = recent[-1] - recent[0]
            if abs(true_change) > 1e-12:
                mask.alias_state_detected = True
                mask.reasoning.append(
                    f"temporal aliasing: true change {true_change:+.5f} over "
                    f"{self.window} steps is below noise floor "
                    f"{self.noise_floor:.5f}; trend reported as zero"
                )
            return 0.0
        return observed_change / (self.window - 1)


@dataclass
class BlindnessStack:
    """Compose the three operators into one observation transform."""

    frame: FrameBlindness
    model: Dict[str, ModelDependenceMasking] = field(default_factory=dict)
    timing: Optional[TemporalAliasing] = None

    def observe(self, true_state: Dict[str, float]) -> tuple:
        """Return `(observation, mask)` for one true state."""
        mask = BlindnessMask()
        observed = self.frame.apply(true_state, mask)
        for key, instrument in self.model.items():
            if key in observed:
                observed[key] = instrument.apply(observed[key], mask)
        return observed, mask

    def perceived_trend(self, series: Sequence[float], mask: BlindnessMask) -> float:
        if self.timing is None:
            if len(series) < 2:
                return 0.0
            return series[-1] - series[-2]
        return self.timing.trend(series, mask)

    @property
    def composite_fidelity(self) -> float:
        """Product of instrument fidelities. 1.0 when no model layer."""
        f = 1.0
        for instrument in self.model.values():
            f *= instrument.fidelity
        return f


def _self_test() -> None:
    # -- FrameBlindness ---------------------------------------------
    m = BlindnessMask()
    fb = FrameBlindness(boundary={"yield", "effort"})
    obs = fb.apply({"yield": 10.0, "effort": 2.0, "soil_carbon": 0.9}, m)
    assert set(obs) == {"yield", "effort"}, "out-of-boundary vars must be dropped"
    assert m.frame_offset and "soil_carbon" in m.reasoning[0]

    m2 = BlindnessMask()
    obs2 = fb.apply({"yield": 1.0, "effort": 1.0}, m2)
    assert obs2 == {"yield": 1.0, "effort": 1.0}
    assert not m2.frame_offset, "no drop means no frame flag"

    # -- ModelDependenceMasking -------------------------------------
    # Full coverage is transparent.
    m3 = BlindnessMask()
    md = ModelDependenceMasking(rung="M2", training_domain_coverage=1.0, model_prior=1.0)
    assert abs(md.apply(0.5, m3) - 0.5) < 1e-12
    assert not m3.gate_active

    # Partial coverage pulls the report toward the (healthy) prior.
    m4 = BlindnessMask()
    md2 = ModelDependenceMasking(rung="M2", training_domain_coverage=0.5, model_prior=1.0)
    reported = md2.apply(0.4, m4)
    assert 0.4 < reported < 1.0, "degraded truth should be reported as healthier"
    assert abs(reported - 0.7) < 1e-12
    assert m4.gate_active

    # An M1 reading is not pulled toward a prior.
    m5 = BlindnessMask()
    md3 = ModelDependenceMasking(rung="M1", training_domain_coverage=0.5, model_prior=1.0)
    assert abs(md3.apply(0.4, m5) - 0.4) < 1e-12

    # Saturation clips upward excursions only.
    m6 = BlindnessMask()
    md4 = ModelDependenceMasking(rung="M1", saturation_ceiling=0.8)
    assert abs(md4.apply(0.95, m6) - 0.8) < 1e-12 and m6.saturation_flag
    m7 = BlindnessMask()
    assert abs(md4.apply(0.5, m7) - 0.5) < 1e-12 and not m7.saturation_flag

    # Fidelity ordering across rungs.
    fids = [ModelDependenceMasking(rung=r).fidelity for r in ("M0", "M1", "M2", "M3")]
    assert all(a > b for a, b in zip(fids, fids[1:])), "fidelity must fall with rung"

    try:
        ModelDependenceMasking(rung="M9")
        raise AssertionError("bad rung should raise")
    except ValueError:
        pass

    # -- TemporalAliasing -------------------------------------------
    # A slow decline below the noise floor reads as no trend.
    m8 = BlindnessMask()
    ta = TemporalAliasing(window=4, noise_floor=0.05, rng=random.Random(1))
    slow = [1.0, 0.998, 0.996, 0.994]
    assert ta.trend(slow, m8) == 0.0, "slow decline must alias to zero"
    assert m8.alias_state_detected

    # A fast decline is resolved.
    m9 = BlindnessMask()
    fast = [1.0, 0.8, 0.6, 0.4]
    assert ta.trend(fast, m9) < 0.0, "fast decline must be visible"
    assert not m9.alias_state_detected

    # A flat series is genuinely flat -- no alias flag, since nothing is hidden.
    m10 = BlindnessMask()
    assert ta.trend([1.0] * 4, m10) == 0.0
    assert not m10.alias_state_detected, "no true change means nothing was aliased"

    # Too little history yields no trend.
    assert ta.trend([1.0, 0.5], BlindnessMask()) == 0.0

    # -- BlindnessStack ---------------------------------------------
    stack = BlindnessStack(
        frame=FrameBlindness(boundary={"stock"}),
        model={"stock": ModelDependenceMasking(rung="M2", training_domain_coverage=0.6)},
        timing=TemporalAliasing(window=3, noise_floor=0.05, rng=random.Random(2)),
    )
    o, mm = stack.observe({"stock": 0.5, "hidden": 0.1})
    assert "hidden" not in o and mm.frame_offset and mm.gate_active
    assert o["stock"] > 0.5, "M2 at partial coverage over-reports a low stock"
    assert abs(stack.composite_fidelity - RUNG_FIDELITY["M2"] * 0.6) < 1e-12

    print("blindness.py self-test OK")


if __name__ == "__main__":
    _self_test()
