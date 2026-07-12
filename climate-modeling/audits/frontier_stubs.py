"""Frontier-stub audits from the cascade family. Each is a build recipe, not
yet implemented — the failure-mode + true-system + audit-model + failure-metric
outline is spelled out in each class docstring. Same pattern as
`sustained-activation-gate/`'s `explore_theta_vs_restore` before it was built.

Drop-in build order: each stub becomes a real audit by supplying two model
classes (true / audited) and one forcing generator, then wiring up
`compute_audit_metrics`. The failure predictions in each docstring are the
falsifiable claims — build the audit, run it, see whether reality matches.
"""

from .base_audit import BaseAudit


class _FrontierStub(BaseAudit):
    """Shared marker for stubs. Every real audit method raises."""

    def generate_true_system(self):
        raise NotImplementedError(f"{self.name}: build recipe in the class docstring.")

    def generate_audited_model(self):
        raise NotImplementedError(f"{self.name}: build recipe in the class docstring.")

    def compute_audit_metrics(self, true_output, audited_output):
        raise NotImplementedError(f"{self.name}: build recipe in the class docstring.")

    def run(self):
        return {
            "audit_name": self.name,
            "failure_detected": None,
            "metrics": {"status": "FRONTIER_STUB"},
            "true_final": None,
            "audited_final": None,
        }


class MissingPositiveFeedbackAudit(_FrontierStub):
    """Temperature-dependent amplifying loop the audit misses.

    TRUE: grass + soil model where the feedback strength itself rises with T
    (e.g. warmer soil accelerates decomposition, releasing CO2 that warms more).
    AUDITED: constant-strength feedback or no feedback.
    FORCING: `DiurnalTemperature(T_mean=23, amplitude=8)` — moderate warming.
    METRIC: RMSE of biomass trajectory; failure if RMSE > 10.
    PREDICTION: audit underestimates decline speed once the feedback engages."""

    def __init__(self):
        super().__init__(
            "Missing Positive Feedback",
            "Temperature-scaled soil-plant feedback the audited model omits.")


class ThresholdSmoothingAudit(_FrontierStub):
    """Step -> sigmoid replacement dilutes the tipping-point signature.

    TRUE: `_StepMortalityGrass` (respiration cliff at 35°C).
    AUDITED: same grass with `_respiration(T)` replaced by
        `base + 10.0 / (1 + exp(-(T - 35) / 2))` — matched-integral sigmoid.
    FORCING: `RampForcing(T_start=20, T_end=40, duration=100, amplitude=3)`.
    METRIC: collapse-time difference; failure if audited late by > 10 h.
    PREDICTION: smooth surrogate delays the die-off across every seed."""

    def __init__(self):
        super().__init__(
            "Threshold Smoothing",
            "Sigmoid replacement of a true step response dilutes the tipping point.")


class TemporalAggregationExtremesAudit(_FrontierStub):
    """Hourly extremes destroyed by daily-mean forcing.

    TRUE: `FatTailedForcing(T_mean=22, amplitude=6, df=3, scale=5)` driving
        a normal grass model. Hourly resolution preserves extreme spikes.
    AUDITED: same model driven by a step-constant forcing whose value each
        24-hour block is the mean of that block's hourly temperatures.
    METRIC: RMSE + collapse-time delay. Failure if audited late by > 15 h.
    PREDICTION: daily means average away the extremes that trigger cascades."""

    def __init__(self):
        super().__init__(
            "Temporal Aggregation Extremes",
            "Averaging hourly forcing to daily means erases the extremes that trigger collapse.")


class SpatialHomogenizationAudit(_FrontierStub):
    """Two-patch fire-spread system vs single-patch averaged temperature.

    TRUE: two-patch model (`temperature_1`, `temperature_2` in forcing).
        Hot patch collapses first; when its biomass drops below a floor,
        an extra mortality term fires in the cool patch (fire propagation).
    AUDITED: single-patch model with `T = mean(T_1, T_2)`.
    FORCING: `TwoPatchForcing(T_mean1=28, T_mean2=20, amplitude=4)`.
    METRIC: total biomass RMSE + presence-of-collapse in audited model.
    PREDICTION: single-patch model never sees the local hotspot ignite."""

    def __init__(self):
        super().__init__(
            "Spatial Homogenization",
            "Two-patch fire propagation invisible to single-patch averaged model.")


class MemoryAmnesiaAudit(_FrontierStub):
    """Accumulated heat damage the memoryless audit forgets.

    TRUE: grass model with a vulnerability state V accumulating above 30°C
        and decaying slowly, gating future photosynthesis by (1 - V).
    AUDITED: memoryless grass; photosynthesis depends only on current T.
    FORCING: diurnal + a scheduled heatwave pulse (`50 < t < 70`, +10°C).
    METRIC: post-heatwave biomass gap. Failure if audited post-heat > 1.5×
        true post-heat.
    PREDICTION: memoryless model overestimates recovery after each pulse."""

    def __init__(self):
        super().__init__(
            "Memory Amnesia",
            "Accumulated heat damage tracked in a memory state, invisible to memoryless audit.")


class CrossSystemCouplingAudit(_FrontierStub):
    """Pollinator collapse propagates to plants — audit sees only plants.

    TRUE: two-state pollinator-plant system. Pollinator mortality accelerates
        above 30°C. Plant reproduction depends on pollinator population.
    AUDITED: plant-only logistic model with elevated intrinsic growth (to
        mimic constant pollination).
    FORCING: slow warming ramp (`T = 25 + 0.05 * t`).
    METRIC: final plant biomass gap. Failure if audited > 1.3× true and true < 30.
    PREDICTION: audit never predicts plant collapse because it has no
        pollinator variable to track."""

    def __init__(self):
        super().__init__(
            "Cross-System Coupling",
            "Pollinator collapse drives plants — audit tracks plants only.")


class BufferExhaustionAudit(_FrontierStub):
    """Soil-moisture buffer depletion invisible to constant-moisture audit.

    TRUE: grass + soil-moisture state W. W recharges slowly, depletes fast
        above 25°C, and gates photosynthesis when W < 20.
    AUDITED: no W state; assumes constant adequate moisture.
    FORCING: diurnal + prolonged heatwave (`80 < t < 150`, +12°C).
    METRIC: post-heatwave biomass. Failure if audited post-heat > 1.5× true.
    PREDICTION: audit misses the sudden wilting once the buffer runs out."""

    def __init__(self):
        super().__init__(
            "Buffer Exhaustion",
            "Soil-moisture buffer that depletes under heat then triggers sudden wilting.")


class ClusteredExtremesAudit(_FrontierStub):
    """Serial correlation of extremes vs independence assumption.

    TRUE: `AutoregressiveExtremesForcing(ar_coef=0.7, df=3, scale=3)` — heavy-
        tailed AR(1) noise causing consecutive heatwave days.
    AUDITED: same grass model driven by iid Gaussian noise with matched variance.
    METRIC: minimum-biomass gap. Failure if audited min > 2× true min.
    PREDICTION: independent-Gaussian assumption never lets adjacent extreme
        days compound; audit's minimum stays much higher than truth's."""

    def __init__(self):
        super().__init__(
            "Clustered Extremes",
            "AR(1) heavy-tailed extremes cluster into cascade-triggering runs.")


class GaussianBlindnessAudit(_FrontierStub):
    """Fat-tailed truth vs Gaussian audit at matched variance.

    TRUE: `FatTailedForcing(df=3, scale=4)` — Student's t with variance
        matched to a Gaussian.
    AUDITED: same grass model driven by Gaussian noise with the matched variance.
    METRIC: minimum-biomass ratio. Failure if audited min > 1.5× true min.
    PREDICTION: at equal variance, the fat-tailed forcing still produces
        deeper minima; the Gaussian audit is systematically optimistic."""

    def __init__(self):
        super().__init__(
            "Gaussian Blindness",
            "Matching variance between fat-tailed and Gaussian noise does not match the tails.")


class IncentiveBiasAudit(_FrontierStub):
    """Parsimony reward selects a simple model that misses the cascade.

    TRUE: `CascadeGrass` under `FatTailedForcing`.
    AUDITED: a `LinearRegression` fit of biomass vs temperature on the first
        half of the true trajectory (this is what a modeler wins when they
        reward simplicity and validate in-sample).
    METRIC: RMSE + collapse-time gap. Failure if RMSE > 20 or audit late > 30 h.
    PREDICTION: the simple model fits the pre-cascade window well and fails
        catastrophically in the second half — the classic incentive trap."""

    def __init__(self):
        super().__init__(
            "Incentive Bias",
            "Parsimony reward selects a simple model that fits pre-cascade data and misses the cascade.")
