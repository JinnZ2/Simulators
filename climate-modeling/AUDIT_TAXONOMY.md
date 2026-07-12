# Audit Taxonomy

Sixteen failure modes each mapped to a philosophical fallacy, a mathematical
condition, and a real-world consequence. Six are **built** (a runnable audit
lives in `audits/`). Ten are **frontier stubs** — the failure-mode, the
true-system class, the audit-model class, the forcing generator, and the
failure metric are all spelled out in the stub's docstring; the class raises
`NotImplementedError` until built.

## Built audits

| Audit | Fallacy | Mathematical condition | Consequence |
|---|---|---|---|
| `PhaseChangeAudit` | Smoothness assumption — believing all change is gradual. | Missing threshold/switching term in the mortality function. | Underestimating extinction risk from sudden extremes (coral bleaching, crop failure). |
| `StationarityAudit` | Temporal uniformity — assuming past patterns persist. | Constant parameters despite non-stationary forcing. | Impact projections diverge from reality as warming accelerates. |
| `MissingFeedbackAudit` | Unidirectional causation — ignoring reciprocal loops. | Omitted coupling between state variables. | Overestimation of forest carbon-sink capacity; wrong management decisions. |
| `OmittedVariableAudit` | Over-simplification — assuming all relevant factors are known. | Missing covariate; residuals correlate with hidden driver. | Poor crop yield forecasts from ignoring soil-moisture variability. |
| `DataAggregationAudit` | Resolution neglect — averaging destroys information. | Jensen's inequality when nonlinear functions receive averaged inputs. | Biased parameters from daily/seasonal data used in high-resolution predictions. |
| `CascadeSpeedAudit` | Speed blindness — imagining collapse as gradual when it is punctuated. | Combined omission of threshold + feedback + memory + fat-tailed forcing. | Systematic underestimation of how much time we have. |

## Frontier stubs (cascade family)

| Audit | Fallacy | Mathematical condition | Consequence |
|---|---|---|---|
| `MissingPositiveFeedbackAudit` | One-directional causation with temperature-dependent strength. | Feedback coefficient not scaled with T. | Warming-driven decline arrives faster than the model predicts. |
| `ThresholdSmoothingAudit` | Aesthetic preference for differentiable forms. | Sigmoid replacement of a true step function. | Rapid die-off during extreme events missed. |
| `TemporalAggregationExtremesAudit` | Resolution neglect at the tails. | Daily-mean forcing hides hourly heatwaves. | Extinction risk underestimated; cascade timeline extended. |
| `SpatialHomogenizationAudit` | Grid-cell homogeneity. | Averaging over patches with different vulnerability. | Ignition/propagation events never simulated. |
| `MemoryAmnesiaAudit` | Markov assumption. | No accumulated-stress state variable. | Repeated mild heatwaves eventually crash real system; audit fine. |
| `CrossSystemCouplingAudit` | Domain isolation. | Missing coupling to a mutualist / dependent system. | Cascades jump domains (pollinators → plants); audit never sees them. |
| `BufferExhaustionAudit` | Steady-state calibration. | Hidden buffer state (soil moisture) treated as constant. | Sudden wilting after buffer depletion not captured. |
| `ClusteredExtremesAudit` | Independence assumption for extremes. | No serial correlation in forcing noise. | Compound events (heatwave + windstorm) never simulated. |
| `GaussianBlindnessAudit` | "Everything is Gaussian" habit. | Normal noise where reality has fat tails. | 6σ events happen every few years; model never sees them coming. |
| `IncentiveBiasAudit` | Parsimony as terminal virtue. | AIC/BIC-style selection with in-sample validation. | Simple model wins the contest, misses the cascade in deployment. |

## Building a frontier stub into a live audit

Each stub's docstring lists the true system, audit model, forcing generator,
and failure metric. To promote a stub to a live audit:

1. Add the model classes it needs to `models/` (if not already there).
2. Add any forcing generator it needs to `forcing.py`.
3. Copy the stub, rename to a real audit module (e.g. `audits/memory_amnesia.py`).
4. Fill in `generate_true_system`, `generate_audited_model`, and
   `compute_audit_metrics` per the docstring recipe.
5. Move the class from `frontier_stubs.py` to the new module and update the
   registry so it lives in `BUILT_AUDITS` instead of `FRONTIER_AUDITS`.

## Refutation protocol

Every audit's failure metric is a **falsifiable prediction**: "the audit
model will fall short of the true model by more than X on this metric."
When an audit's failure metric is missed (the audit unexpectedly passes),
the CLAIM about the failure mode updates — not the metric threshold. Do
not lower the tolerance to save a favored audit.
