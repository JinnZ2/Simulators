---

## CLAIM_TABLE_v2.md

Claims about the delivered climate-modeling/ folder, about what a Python + NumPy/SciPy environment can establish concerning it, and about the audit taxonomy's epistemological architecture.

This is an audit suite, not a forecast. No climate projection is produced here. No policy recommendation is issued. Every audit is a controlled experiment where the true system is known (we built it), a simplified model is run in parallel, and the discrepancy names a specific failure mode. The folder requires numpy + scipy (see requirements.txt); the dashboard adds streamlit.

The delivered code is runnable — six built audits execute end-to-end from the same BaseAudit interface. Ten frontier stubs raise NotImplementedError with full build recipes in their docstrings.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `CMA_001` | The delivered folder implements two layers: Level-1 is the actual simulation model (grass, cascade grass); Level-2 is experiments about experiments — an audit taxonomy that probes what a modeler's own simplifications systematically miss. | SUPPORTED |
| `CMA_002` | The suite is runnable in this environment with numpy + scipy installed. Six built audits execute; ten frontier stubs raise NotImplementedError with build recipes. | SUPPORTED (contingent on dependencies) |
| `CMA_003` | The whole point of Level-2 is to catch cascade-speed blindness — the pattern where a smooth, memoryless, Gaussian-driven model predicts collapse in fifty years and reality does it in five. | SUPPORTED |
| `CMA_004` | Every audit is a controlled experiment where the true system is known (we built it), a simplified model is run in parallel, and the discrepancy names a specific failure mode. | SUPPORTED |
| `CMA_005` | Six built audits run end-to-end: PhaseChangeAudit, StationarityAudit, MissingFeedbackAudit, OmittedVariableAudit, DataAggregationAudit, CascadeSpeedAudit (the flagship). | SUPPORTED |
| `CMA_006` | Ten frontier stubs each raise NotImplementedError with a full build recipe in the class docstring (true system class, audit model, forcing generator, failure metric). | SUPPORTED |
| `CMA_007` | Each audit maps to a philosophical fallacy, a mathematical condition, and a real-world consequence. | SUPPORTED |
| `CMA_008` | The audit taxonomy contains sixteen failure modes — six built, ten frontier. | SUPPORTED |
| `CMA_009` | The cascade-speed audit combines omission of threshold + feedback + memory + fat-tailed forcing. | SUPPORTED |
| `CMA_010` | AI-patching loop has two patcher families: RuleBasedPatcher (deterministic, no network) and LLMPatcher (falls back to rule-based if OpenAI key missing). | SUPPORTED (if openai package optional) |
| `CMA_011` | The folder produces no climate forecast — no projection, no policy recommendation, no real-world prediction. It produces audit reports: which simplifications cause which failures, and by how much. | SUPPORTED |
| `CMA_012` | The config.py centralises parameters — GRASS_DEFAULTS (P_max, T_opt, sigma, R_base, Q10, M, G, initial_C), SIM_DEFAULTS (duration_hours, max_step), FORCING_DEFAULTS (T_mean, amplitude, day_fraction). | SUPPORTED |
| `CMA_013` | The forcing.py provides six forcing generators — diurnal, ramp, trend, stochastic, fat-tailed, aggregated wrapper. | SUPPORTED (by file listing) |
| `CMA_014` | The models/ directory contains BaseModel with solve_ivp integrator, grass.py (plain carbon-balance grass), and cascade_grass.py (threshold + feedback + memory — the true system). | SUPPORTED (by file listing) |
| `CMA_015` | The entry point run_audits.py prints a report card and writes JSON to samples/audit_report.json. | SUPPORTED |
| `CMA_016` | Promoting a stub to a live audit is a documented five-step procedure in AUDIT_TAXONOMY.md. | SUPPORTED |
| `CMA_017` | The folder contains no real-world data — no observational record, no satellite imagery, no field measurements. All systems are synthetic, constructed to make failure modes visible. | SUPPORTED |
| `CMA_018` | The true system is always known — we built it. This is the key epistemological advantage: we can measure discrepancy exactly because we know the ground truth. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the climate-modeling audit suite, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

These are not vague "future work" paragraphs. Each gap is precisely bounded, checkable, and scoped to a semester or summer of work.

---

### 1. FRONTIER STUB PROMOTION — MissingPositiveFeedbackAudit

**Gap:** The MissingPositiveFeedbackAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED (stub exists, implementation pending)

**Research question:** How does omitting temperature-dependent feedback strength bias warming-driven decline projections?

**Disciplines:** Climate science, dynamical systems, computational modeling

**Data sources:**

- The stub's docstring (true system class, audit model, forcing generator, failure metric)
- The five-step promotion procedure in AUDIT_TAXONOMY.md
- Built audit examples (phase_change.py, cascade_speed.py) as templates

**Method:**

1. Read the stub's docstring to identify the true system, audit model, forcing generator, and failure metric
2. Implement the true system (temperature-dependent feedback)
3. Implement the audit model (feedback coefficient not scaled with T)
4. Implement the forcing generator
5. Define and compute the failure metric
6. Register the audit in audit_registry.py

**Expected deliverable:** A live MissingPositiveFeedbackAudit that runs end-to-end and produces a failure_detected boolean + metrics.

**Falsifier:** The audit shows no discrepancy between true and simplified models (then positive feedback is not load-bearing for this system).

---

### 2. FRONTIER STUB PROMOTION — ThresholdSmoothingAudit

**Gap:** The ThresholdSmoothingAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does replacing a true step function with a sigmoid smooth it, and what rapid die-off events are missed as a result?

**Disciplines:** Ecology, nonlinear dynamics, computational modeling

**Data sources:**

- Stub docstring in frontier_stubs.py
- Built audit examples
- Ecological literature on tipping points and extinction thresholds

**Method:**

1. Implement true system with a step-function mortality threshold
2. Implement audit model with a sigmoid approximation
3. Run both under identical forcing
4. Measure discrepancy: events where the sigmoid model predicts survival but the step model predicts die-off

**Expected deliverable:** A live ThresholdSmoothingAudit with failure metric quantifying missed rapid die-off events.

**Falsifier:** The sigmoid and step function produce identical outcomes for all tested forcings (then smoothing is not a meaningful simplification).

---

### 3. FRONTIER STUB PROMOTION — TemporalAggregationExtremesAudit

**Gap:** The TemporalAggregationExtremesAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does daily-mean forcing hide hourly heatwaves, and how does that bias extinction risk estimates?

**Disciplines:** Climatology, statistics, ecology

**Data sources:**

- Stub docstring
- Hourly vs. daily temperature records (synthetic or from NOAA)
- Ecological literature on heatwave impacts

**Method:**

1. Implement true system with hourly temperature forcing
2. Implement audit model with daily-averaged forcing
3. Run both and compare extinction timing
4. Compute the "cascade timeline extension" — how much later does the aggregated model predict collapse?

**Expected deliverable:** A live TemporalAggregationExtremesAudit with failure metric quantifying the timeline bias.

**Falsifier:** Daily aggregation produces no timeline bias (then hourly resolution is not needed for this system).

---

### 4. FRONTIER STUB PROMOTION — SpatialHomogenizationAudit

**Gap:** The SpatialHomogenizationAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does averaging over patches with different vulnerability hide ignition and propagation events?

**Disciplines:** Landscape ecology, fire science, spatial statistics

**Data sources:**

- Stub docstring
- Landscape patch models (synthetic or from published literature)
- Fire spread models

**Method:**

1. Implement true system with heterogeneous patches (different fuel loads, moisture, vulnerability)
2. Implement audit model with spatially averaged properties
3. Run both and compare fire ignition and propagation
4. Measure discrepancy: events where the homogeneous model predicts no spread but the heterogeneous model does

**Expected deliverable:** A live SpatialHomogenizationAudit with failure metric quantifying missed ignition/propagation events.

**Falsifier:** Homogeneous and heterogeneous models produce identical spread patterns (then spatial heterogeneity is not load-bearing).

---

### 5. FRONTIER STUB PROMOTION — MemoryAmnesiaAudit

**Gap:** The MemoryAmnesiaAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does omitting accumulated-stress state variables cause models to miss collapse from repeated mild heatwaves?

**Disciplines:** Plant physiology, stress ecology, dynamical systems

**Data sources:**

- Stub docstring
- Plant stress-accumulation models (synthetic or from literature)
- Heatwave frequency and intensity data

**Method:**

1. Implement true system with an accumulated-stress state variable
2. Implement audit model with Markov assumption (no memory)
3. Run both under repeated mild heatwaves
4. Measure discrepancy: where the memoryless model predicts recovery but the memory model predicts collapse

**Expected deliverable:** A live MemoryAmnesiaAudit with failure metric quantifying collapse missed by memoryless models.

**Falsifier:** Repeated mild heatwaves cause no accumulated damage (then memory is not load-bearing).

---

### 6. FRONTIER STUB PROMOTION — CrossSystemCouplingAudit

**Gap:** The CrossSystemCouplingAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does domain isolation (e.g., modeling plants without pollinators) cause cascades to jump domains that the audit never sees?

**Disciplines:** Ecology, systems biology, network theory

**Data sources:**

- Stub docstring
- Mutualist/dependent system models (plant-pollinator, predator-prey)
- Published cascade literature

**Method:**

1. Implement true system with coupling to a mutualist/dependent system
2. Implement audit model with the coupled system omitted
3. Run both and compare cascade dynamics
4. Measure discrepancy: cascades that jump domains in the true system but are invisible in the isolated model

**Expected deliverable:** A live CrossSystemCouplingAudit with failure metric quantifying cross-domain cascades missed.

**Falsifier:** No cascades jump domains in the true system (then cross-system coupling is not load-bearing).

---

### 7. FRONTIER STUB PROMOTION — BufferExhaustionAudit

**Gap:** The BufferExhaustionAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does treating a hidden buffer state (soil moisture) as constant cause sudden wilting to be missed?

**Disciplines:** Soil science, hydrology, plant ecology

**Data sources:**

- Stub docstring
- Soil moisture balance models
- Drought and wilting literature

**Method:**

1. Implement true system with a soil moisture buffer state
2. Implement audit model with buffer treated as constant
3. Run both under drying conditions
4. Measure discrepancy: where the constant-buffer model predicts survival but the exhaustible-buffer model predicts wilting

**Expected deliverable:** A live BufferExhaustionAudit with failure metric quantifying sudden wilting events missed.

**Falsifier:** The buffer never exhausts under tested conditions (then buffer dynamics are not load-bearing).

---

### 8. FRONTIER STUB PROMOTION — ClusteredExtremesAudit

**Gap:** The ClusteredExtremesAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does assuming independence of extremes cause compound events (heatwave + windstorm) to never be simulated?

**Disciplines:** Climatology, extreme event statistics, risk analysis

**Data sources:**

- Stub docstring
- Serial correlation models for extremes
- Compound event literature

**Method:**

1. Implement true system with serial correlation in forcing noise (clustered extremes)
2. Implement audit model with independent extremes
3. Run both and compare compound event frequency
4. Measure discrepancy: compound events that occur in the true system but not in the independent model

**Expected deliverable:** A live ClusteredExtremesAudit with failure metric quantifying missed compound events.

**Falsifier:** Clustered and independent extremes produce identical compound event frequencies (then clustering is not load-bearing).

---

### 9. FRONTIER STUB PROMOTION — GaussianBlindnessAudit

**Gap:** The GaussianBlindnessAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does assuming Gaussian noise when reality has fat tails cause 6σ events to be missed?

**Disciplines:** Statistics, extreme value theory, climate risk

**Data sources:**

- Stub docstring
- Fat-tailed distribution models (Cauchy, Lévy, Student-t)
- Extreme event literature

**Method:**

1. Implement true system with fat-tailed forcing noise
2. Implement audit model with Gaussian noise
3. Run both and compare extreme event frequency
4. Measure discrepancy: 6σ events that occur in the true system but never in the Gaussian model

**Expected deliverable:** A live GaussianBlindnessAudit with failure metric quantifying extreme events missed.

**Falsifier:** Fat-tailed and Gaussian noise produce identical extreme event frequencies (then tail shape is not load-bearing).

---

### 10. FRONTIER STUB PROMOTION — IncentiveBiasAudit

**Gap:** The IncentiveBiasAudit stub is documented but not yet built.

**Knowledge state:** NOT_STUDIED

**Research question:** How does AIC/BIC-style selection with in-sample validation cause simple models to win the contest and miss the cascade in deployment?

**Disciplines:** Model selection, philosophy of science, risk analysis

**Data sources:**

- Stub docstring
- Model selection theory (AIC, BIC, cross-validation)
- Published cases of model selection failures

**Method:**

1. Implement a suite of models (simple to complex)
2. Implement true system (complex, with cascades)
3. Apply AIC/BIC selection to choose the "best" model
4. Compare selected model's out-of-sample cascade prediction vs. true system
5. Measure discrepancy: cascades that the selected model misses

**Expected deliverable:** A live IncentiveBiasAudit with failure metric quantifying cascades missed by parsimony-selected models.

**Falsifier:** The simplest model selected by AIC/BIC also captures all cascades (then parsimony bias is not a failure mode).

---

### 11. AI-PATCHING VALIDATION — Rule-Based Patcher Efficacy

**Gap:** The RuleBasedPatcher emits derivative bodies based on audit metrics, but its efficacy is not measured.

**Knowledge state:** NOT_STUDIED

**Research question:** Does the rule-based patcher actually reduce audit failure metrics over multiple rounds? Or does it just change the model without improving it?

**Disciplines:** Machine learning, dynamical systems, software testing

**Data sources:**

- ai_interface.py — RuleBasedPatcher implementation
- meta_experiments.py — AI-patching loop
- Audit results from run_audits.py

**Method:**

1. Run the patching loop for multiple rounds
2. Record audit metrics (rmse, final_biomass_error, audited_late_by_h) at each round
3. Compute improvement trajectories
4. Identify cases where patching helps vs. hurts
5. Document the conditions under which the rule-based patcher succeeds or fails

**Expected deliverable:** A validation report on the rule-based patcher's efficacy, with success/failure conditions and improvement trajectories.

**Falsifier:** The patcher never reduces any audit metric (then the patching loop is not doing useful work).

---

### 12. AI-PATCHING VALIDATION — LLM Patcher vs. Rule-Based Patcher

**Gap:** The LLMPatcher falls back to the rule-based patcher if OpenAI is missing, but its relative performance is unknown.

**Knowledge state:** NOT_STUDIED

**Research question:** Does the LLM patcher outperform the rule-based patcher? If so, by how much and in which failure modes?

**Disciplines:** AI/ML, natural language processing, dynamical systems

**Data sources:**

- ai_interface.py — both patcher implementations
- OpenAI API (if available)
- Audit results from both patcher families

**Method:**

1. Run the patching loop with rule-based patcher
2. Run the patching loop with LLM patcher (with OpenAI key)
3. Compare audit metrics across both runs
4. Identify failure modes where LLM helps more, and where it doesn't
5. Document cost-benefit trade-off (API cost vs. improvement)

**Expected deliverable:** A comparative validation report on LLM vs. rule-based patching, with per-audit improvement metrics and cost analysis.

**Falsifier:** LLM and rule-based patchers produce identical improvements (then the LLM adds no value).

---

### 13. FORCING GENERATOR EXTENSION — Real-World Forcing

**Gap:** All forcing is synthetic (diurnal, ramp, trend, stochastic, fat-tailed, aggregated).

**Knowledge state:** NOT_STUDIED

**Research question:** How do the audit results change when driven by real-world climate forcing (e.g., CMIP6 output, historical temperature records)?

**Disciplines:** Climatology, computational modeling, data science

**Data sources:**

- CMIP6 climate model output
- NOAA/NCEP reanalysis data
- Historical temperature and precipitation records

**Method:**

1. Implement a real-world forcing generator that reads CMIP6 or reanalysis data
2. Register it in forcing.py
3. Run all six built audits with real-world forcing
4. Compare audit results (failure_detected, metrics) against synthetic-forcing baselines
5. Document which failure modes are more or less severe under real-world forcing

**Expected deliverable:** A RealWorldForcing generator and a validation report comparing synthetic vs. real-world audit results.

**Falsifier:** Real-world and synthetic forcing produce identical audit results (then synthetic forcing is sufficient).

---

### 14. MODEL VALIDATION — Cascade Grass Parameter Sensitivity

**Gap:** The cascade grass model (threshold + feedback + memory) has parameters but no sensitivity analysis.

**Knowledge state:** NOT_STUDIED

**Research question:** Which parameters in the cascade grass model most affect audit failure detection? Which parameters are the audit results robust to?

**Disciplines:** Sensitivity analysis, dynamical systems, computational modeling

**Data sources:**

- config.py — GRASS_DEFAULTS
- models/cascade_grass.py — true system implementation
- Audit results from run_audits.py

**Method:**

1. Define parameter ranges (e.g., ±50% around defaults)
2. Run all six built audits across parameter sweeps
3. Compute sensitivity indices (e.g., Sobol indices) for each parameter-audit pair
4. Identify which parameters are most influential for each failure mode
5. Document robust vs. sensitive parameter regimes

**Expected deliverable:** A sensitivity analysis report with per-parameter, per-audit sensitivity indices and robust parameter ranges.

**Falsifier:** All parameters are equally influential (then sensitivity analysis is not informative).

---

### 15. CASCADE SPEED AUDIT — Real-World Calibration

**Gap:** The CascadeSpeedAudit combines threshold + feedback + memory + fat tails, but it is not calibrated to any real-world system.

**Knowledge state:** NOT_STUDIED

**Research question:** Can the CascadeSpeedAudit be calibrated to a real-world system (e.g., a specific ecosystem, crop, or fishery) to produce actionable predictions about cascade speed?

**Disciplines:** Ecology, fisheries science, climate risk

**Data sources:**

- Published ecosystem models (e.g., forest carbon, fisheries, coral reefs)
- Observational time series
- IPCC reports and regional climate assessments

**Method:**

1. Identify a real-world system with threshold + feedback + memory + fat-tailed forcing
2. Calibrate the cascade grass model to that system using observational data
3. Run the CascadeSpeedAudit on the calibrated system
4. Interpret the failure_detected and metrics in real-world terms
5. Produce a case study: "What the CascadeSpeedAudit would have told us about X"

**Expected deliverable:** A calibrated CascadeSpeedAudit for a real-world system, with a case study report and policy-relevant interpretation.

**Falsifier:** The cascade grass model cannot be calibrated to any real-world system (then the audit is purely theoretical).

---

### 16. DOCUMENTATION — User Guide for Non-Modelers

**Gap:** The folder is documented for developers but not for non-modeler users (policymakers, farmers, students in other fields).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the audit suite's insights be communicated to non-modelers in a way that changes how they think about climate projections?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The audit taxonomy itself
- Published science communication research
- Policy documents on climate risk

**Method:**

1. Translate each audit's philosophical fallacy and real-world consequence into plain language
2. Develop case studies or scenarios for each failure mode
3. Create a user guide that explains: "What this audit means for you"
4. Test the guide with non-modeler audiences (policy students, farmers, etc.)
5. Iterate based on feedback

**Expected deliverable:** A non-technical user guide to the audit taxonomy, with case studies and plain-language explanations of each failure mode.

**Falsifier:** Non-modeler audiences find the guide unhelpful or incomprehensible (then the guide needs revision).

---

## SCOPE_BOUNDARY.md

Why this folder is broader than standard climate modeling practice

Delivered verbatim. CC0.

---

### The Problem

In climate impact modeling, things like model selection criteria, spatial aggregation, temporal resolution, and feedback omission are not separate from the science. They are direct, material, contributing factors to the model's output. When a model says those things have "no material effect" or are "within standard practice," that is usually not a scientific finding. It is a boundary choice, a modeling limitation, or a narrow definition of "acceptable error."

The climate system does not care about our computational budgets. Physics does not isolate a grassland from the soil moisture below it, the pollinators that visit it, the heatwaves that stress it, or the modeler's preference for parsimony over complexity. All of those are part of one continuous causal system.

When we model only a piece of that system, or when we choose one functional form over another because it is mathematically convenient, we are not simplifying reality — we are modeling a different system than the one that actually exists. And then we are surprised when the real system behaves in ways the model did not predict.

---

### Six Ways the Connection Gets Lost

#### 1. The "Smoothness" Fallacy

Many climate models assume all change is gradual. They use smooth functions for mortality, growth, and respiration. If the model predicts "gradual decline over 50 years," that is treated as the answer.

But real systems have thresholds. Coral bleaching happens when temperature exceeds a threshold for a critical duration. Crop failure happens when a heatwave crosses a critical intensity. If the report says "gradual decline," it is not false, but it is incomplete. The threshold was causal too — just not represented.

So "smoothness assumption" often means "We chose a differentiable function because it was easier to integrate." That is very different from "The system is actually smooth."

#### 2. The "Stationarity" Fallacy

Many models are calibrated on a stationary window — a historical period assumed to be representative of the future. Parameters are held constant. If the model says "impacts will be X," that is treated as the answer.

But the forcing is non-stationary. Warming accelerates. Precipitation patterns shift. If the parameters were estimated from a cooler, wetter past, they may not apply to a warmer, drier future. The model is not wrong about the past. It is just not a guide to the future.

So "stationarity assumption" often means "We didn't have enough data to estimate time-varying parameters." That is a data limitation, not a physical fact.

#### 3. The "Unidirectional Causation" Fallacy

Many models treat causation as one-way: forcing → response. They omit feedback loops. If the model says "carbon sink capacity is X," that is treated as the answer.

But real systems have feedbacks. Warmer soils respire more CO2, which warms the climate further, which respires more CO2. If the feedback is omitted, the model underestimates the response. The model is not wrong about the direct effect. It is just missing the amplification.

So "unidirectional causation" often means "We didn't include the feedback because it was too complex." That is a modeling choice, not evidence that the feedback is absent.

#### 4. The "Omitted Variable" Fallacy

Many models include only the variables the modeler thought to include. If a variable is not in the model, the model shows no sensitivity to it. If the model says "soil moisture is not a significant driver," that is treated as the answer.

But if soil moisture was never included, the model cannot show sensitivity to it. The statement "not significant" is an artifact of the model's architecture, not a finding about the real world.

So "omitted variable" often means "We didn't think of it" or "We didn't have data for it." That is a human limitation, not a physical fact.

#### 5. The "Resolution Neglect" Fallacy

Many models use aggregated data — daily means, seasonal averages, grid-cell averages. If the model says "no extreme events," that is treated as the answer.

But aggregation destroys information. Jensen's inequality means that the average of a nonlinear function is not the function of the average. Daily-mean temperature may be below a threshold, but hourly peaks may exceed it. The model misses the extremes because it was built on averages.

So "resolution neglect" often means "We couldn't afford the computational cost of higher resolution." That is a budget constraint, not evidence that extremes don't matter.

#### 6. The "Parsimony as Terminal Virtue" Fallacy

Many modelers believe that simpler models are better — that parsimony is a scientific virtue. If a simple model wins an AIC/BIC contest, it is treated as the "best" model.

But parsimony is a preference, not a physical law. A simple model may fit the calibration data well and still miss the cascade in deployment. The model that "wins" the contest may be the one that is most wrong about the future, because it omits the very mechanisms that matter most.

So "parsimony as terminal virtue" often means "We valued simplicity over accuracy." That is a value judgment, not a scientific finding.

---

What This Folder Does Differently

This build spec treats the modeling enterprise as one integrated epistemological system. The following audits document mechanisms that standard climate modeling typically drops:

- PhaseChangeAudit — Smoothness assumption: the model is blind to a true respiration cliff.
- StationarityAudit — Temporal uniformity: parameters constant despite non-stationary forcing.
- MissingFeedbackAudit — Unidirectional causation: grass-only ignores soil-plant coupling.
- OmittedVariableAudit — Over-simplification: hidden moisture cycle drives residuals.
- DataAggregationAudit — Resolution neglect: daily-mean-fitted parameters bias hourly predictions.
- CascadeSpeedAudit — Speed blindness: threshold + feedback + memory + fat tails.
- Ten frontier stubs — Each documents a failure mode not yet built, with the failure-mode, true-system class, audit-model class, forcing generator, and failure metric all spelled out.

---

### The Knowledge-State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the spec records its epistemic state rather than excluding it. The valid states are:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The magnitude of temperature-dependent feedback in a specific ecosystem.
UNDER_STUDY Data collection is in progress; value is provisional. The serial correlation of heatwaves under climate change.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted for this system. The accumulated-stress threshold for a specific plant species.
UNDEFINED The variable has no agreed definition or measurement protocol. "Operational trust" in a model selection procedure.

---

### What Is NOT a Valid Epistemic State

COMPUTATIONAL_CONVENIENCE is not a valid knowledge state. If a mechanism physically influences the system, excluding it because it is computationally expensive, mathematically inconvenient, or violates a model selection criterion is a modeling error, not an epistemic one. The physics does not respect our computational budgets.

The folder refuses to record a mechanism as absent because of convenience. Instead, it records the mechanism as a frontier stub — a documented failure mode waiting to be built — and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"Is this within our model's scope?"

But rather:

"Does this mechanism physically influence the system's behavior?"

If the answer is yes, it belongs in the audit. End of story.

The climate system is already interconnected. Our models and computational budgets are the only things pretending otherwise. And that pretense has cost lives, money, energy, and ecosystems on a scale that we are only beginning to understand.

This folder does not pretend otherwise.
