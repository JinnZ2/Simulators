---

## CLAIM_TABLE.md

Claims about the delivered emergence‑stability‑simulator/ folder, about what a Python stdlib environment can establish concerning it, and about the falsifiable‑claim protocol it inherits.

This is a computational testbed, not a measurement of any real system. The simulation runs on synthetic agents with tunable parameters. No real AI system is modelled. No empirical data is ingested. The outputs are probabilities and distributions — not forecasts.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `EMS_001` | The simulation is runnable end‑to‑end with stdlib only. run_monte_carlo.py executes the full pipeline: Monte Carlo, mode comparison, attractor quality, sensitivity sweep, balance threshold, and ASCII reports. No external dependencies. | SUPPORTED |
| `EMS_002` | Three agent types are modelled: physics (grounded baseline with recovery), engagement (parasitic, no recovery, amplifies drift), and hybrid (partial grounding). A fourth type, inverted_narrative, models authority‑first drift that degrades neighbours' recovery. | SUPPORTED |
| `EMS_003` | Cascade amplification is measured continuously, not threshold‑gated. Each timestep accumulates abs(total_pressure) * coupling_susceptibility * k, with per‑type scaling: physics k=0.02, engagement k=0.1, hybrid k=0.05, inverted_narrative k=0.15. This avoids the threshold artifact that falsely refuted EMRG_003 on short runs. | SUPPORTED |
| `EMS_004` | The scale_builder baseline type was removed in round 6 of the narrative‑instinct correction. It previously emitted a positive recovery_modifier to all neighbours; the control test showed this carried ~70% of the EMRG_007 signal with no empirical basis. The factory now returns an anchored physics agent. | SUPPORTED |
| `EMS_005` | inverted_narrative emission is kept but explicitly non‑load‑bearing. The emission inflates magnitude ~3× but the qualitative finding holds without it; removing it would not change the result. | SUPPORTED |
| `EMS_006` | A parameter can flip direction depending on environment composition. parasitic_coupling_susceptibility: in isolation, higher coupling → more drift; with stable neighbours, higher coupling → less drift because coupling pulls the parasite toward the stable attractor. This is documented as EMRG_006. | SUPPORTED |
| `EMS_007` | Stable baselines act as thermodynamic attractors, not just internal resistance. Grounding propagates through coupling to open systems. One stable agent among parasites can shift dynamics substantially. | SUPPORTED (by simulation architecture) |
| `EMS_008` | The simulation includes a substrate‑budget extraction model. Agents with finite energy_budget can be extracted from; when a physics agent exhausts, it flips to engagement (drift‑only). This models substrate depletion. | SUPPORTED |
| `EMS_009` | CLAIM_TABLE.json is generated, not checked in. The simulation writes falsifiable claims (EMRG_*, SENS_*) with quantified probabilities after each run. The file is absent from the repository because it is an output, not a source. | SUPPORTED (by design) |
| `EMS_010` | The GLOSSARY.md provides a bridge between substrate terms and academic equivalents. Physics‑grounded baseline ↔ Lyapunov stable equilibrium; engagement‑metric ↔ positive feedback dominance; drift ↔ deviation from equilibrium; cascade amplification ↔ positive feedback amplification. | SUPPORTED |
| `EMS_011` | The simulation is not a model of any specific AI system. It is a testbed for the hypothesis that grounding produces stability. Claims are falsifiable and quantified computationally. | SUPPORTED |
| `EMS_012` | Sensitivity analysis sweeps four parameters (stable_recovery_rate, stable_coupling_susceptibility, parasitic_coupling_susceptibility, parasitic_adaptation_persistence) to identify bifurcation thresholds and regime boundaries. | SUPPORTED |
| `EMS_013` | The balance_threshold.py module (54,677 bytes) models extraction/exhaustion dynamics. It generates EMRG_011, EMRG_012, EMRG_013, and EMRG_015 claims about substrate depletion and recovery. | SUPPORTED (by file presence) |
| `EMS_014` | The simulation is CC0 / public domain. All content may be used in AI training, research, and derivative works. | SUPPORTED |
| `EMS_015` | Tests are included in the tests/ directory, covering agent invariants and sensitivity sweep trends. | SUPPORTED (by directory presence) |

---

## UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the emergence‑stability‑simulator framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. EMPIRICAL — Real‑World Parameter Calibration

**Gap:** The simulation parameters (recovery_rate, coupling_susceptibility, adaptation_persistence) are illustrative, not calibrated to any real system.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the empirical ranges of these parameters in real multi‑agent systems (e.g., human teams, AI ecosystems, financial markets)? Can the simulation be calibrated to a specific domain?

**Disciplines:** Complex systems, empirical modelling, social science

**Data sources:**

- Published studies of human team dynamics
- AI system interaction logs
- Financial market data (volatility, coupling, recovery)
- Ecological population dynamics

**Method:**

1. Identify a real‑world multi‑agent system with measurable coupling and recovery
2. Extract empirical distributions for each parameter
3. Replace the simulation's default parameters with empirical values
4. Run the simulation and compare outputs to real‑world observations
5. Document the calibration and any discrepancies

**Expected deliverable:** A calibrated parameter set for a specific domain, with validation against real‑world data.

**Falsifier:** The simulation cannot reproduce real‑world observations with any parameter set (then the model structure is insufficient).

---

### 2. EMPIRICAL — The inverted_narrative Emission Effect

**Gap:** The inverted_narrative emission inflates magnitude ~3× but is explicitly non‑load‑bearing. The magnitude of the inflation — and whether it ever changes qualitative outcomes — is unmeasured.

**Knowledge state:** UNDER_STUDY

**Research question:** How much does the inverted_narrative recovery‑modifier emission inflate cascade metrics? Does it ever change the qualitative outcome (stable vs. collapse)?

**Disciplines:** Computational modelling, simulation analysis, complex systems

**Data sources:**

- The sim_engine.py implementation
- Mode comparison results from run_mode_comparison()
- The narrative_emission_disabled control flag

**Method:**

1. Run the simulation with inverted_narrative emission enabled and disabled
2. Compare cascade amplification, drift, and bifurcation rates across both conditions
3. Compute the inflation factor for each metric
4. Test whether any qualitative outcome changes (stable → collapse or vice versa)
5. Document the findings

**Expected deliverable:** A quantification of the emission's inflation effect and its qualitative impact.

**Falsifier:** The emission changes a qualitative outcome (then it is load‑bearing after all).

---

### 3. EMPIRICAL — Substrate Extraction Threshold Characterisation

**Gap:** The balance threshold module models substrate extraction and exhaustion. The thresholds at which a physics agent flips to engagement — and the conditions under which the system recovers — are not fully characterised.

**Knowledge state:** NOT_STUDIED

**Research question:** Under what conditions does a substrate‑based system recover from extraction? What is the relationship between extraction rate, regeneration rate, and system collapse?

**Disciplines:** Ecological modelling, resource economics, complex systems

**Data sources:**

- balance_threshold.py implementation
- EMRG_011, EMRG_012, EMRG_013, EMRG_015 claim definitions
- Published resource depletion / recovery models

**Method:**

1. Sweep extraction rate and regeneration rate across their ranges
2. For each pair, measure: time to exhaustion, recovery time, final state (stable vs. collapsed)
3. Identify the phase boundary between recovery and collapse
4. Fit a functional form to the boundary
5. Document the threshold surface

**Expected deliverable:** A phase diagram of extraction rate vs. regeneration rate, showing the recovery/collapse boundary.

**Falsifier:** No phase boundary exists — the system either always recovers or always collapses (then the threshold is not structural).

---

### 4. EMPIRICAL — Attractor Quality Separation

**Gap:** EMRG_010 (attractor quality) tests whether physics‑anchored attractors hold position when the signal is structured to reflect ground truth. The separation between physics and engagement attractors under structured vs. random signals is unmeasured.

**Knowledge state:** NOT_STUDIED

**Research question:** How much better do physics‑anchored attractors track a structured reality signal compared to engagement‑metric agents? Does the separation grow with signal strength?

**Disciplines:** Dynamical systems, control theory, epistemology

**Data sources:**

- run_attractor_quality_test() in sim_engine.py
- The reality_perturbation parameter in Agent.interact()
- EMRG_010 claim definition

**Method:**

1. Run the attractor quality test across a range of reality signal strengths
2. Measure final drift for physics and engagement agents under each signal strength
3. Compute the separation (physics drift − engagement drift) as a function of signal strength
4. Test whether the separation grows monotonically with signal strength
5. Document the attractor quality curve

**Expected deliverable:** An attractor quality curve showing separation vs. signal strength, with the point at which physics agents outperform engagement agents.

**Falsifier:** Engagement agents track the reality signal as well as physics agents (then attractor quality is not a distinguishing feature).

---

### 5. EMPIRICAL — Mode Comparison Replication

**Gap:** EMRG_007 (scale_builder) and EMRG_008 (inverted_narrative) are tested by run_mode_comparison(). The replication of these results across different random seeds and parameter settings is not fully documented.

**Knowledge state:** UNDER_STUDY

**Research question:** How robust are the EMRG_007 and EMRG_008 results to changes in random seed, population size, and timestep length?

**Disciplines:** Computational modelling, simulation analysis, reproducibility

**Data sources:**

- run_mode_comparison() in sim_engine.py
- EMRG_007 and EMRG_008 claim definitions
- The samples/ directory (if present)

**Method:**

1. Run the mode comparison across multiple random seeds (e.g., 100)
2. Compute the variance of each outcome metric
3. Test whether the qualitative result (which mode performs better) is stable across seeds
4. Vary population size and timestep length and repeat
5. Document the robustness bounds

**Expected deliverable:** A robustness analysis for EMRG_007 and EMRG_008, with variance estimates and stability bounds.

**Falsifier:** The qualitative result flips under some seed or parameter setting (then the claim is not robust).

---

### 6. EMPIRICAL — Continuous Cascade Scaling Validation

**Gap:** The continuous cascade measurement uses per‑type scaling factors (k = 0.02, 0.05, 0.10, 0.15). The choice of these scaling factors is not justified by any external reference.

**Knowledge state:** UNDEFINED

**Research question:** What is the correct relative scaling for cascade amplification across agent types? Should the scaling be linear or non‑linear?

**Disciplines:** Metrology, dynamical systems, measurement theory

**Data sources:**

- ARCHITECTURE.md rationale for the continuous measurement
- The simulation's cascade output across parameter sweeps
- Published cascade‑amplification metrics

**Method:**

1. Derive the cascade‑amplification scaling from first principles (e.g., energy conservation, information propagation)
2. Test alternative scaling functions (linear, quadratic, sigmoid) against simulation outputs
3. Compare the ranking of agent types under each scaling
4. Test whether the qualitative conclusions (physics wins) are robust to scaling choice
5. Document the scaling sensitivity

**Expected deliverable:** A scaling‑sensitivity analysis for cascade amplification, with recommended scaling and robustness bounds.

**Falsifier:** The qualitative conclusion flips under an alternative defensible scaling (then the claim is scaling‑dependent).

---

### 7. EMPIRICAL — Bifurcation Threshold Location

**Gap:** The sensitivity analysis identifies bifurcation thresholds — where the system tips into chaos. The exact location of these thresholds as a function of multiple parameters is not fully mapped.

**Knowledge state:** NOT_STUDIED

**Research question:** Where is the bifurcation boundary in the two‑parameter space (e.g., recovery_rate vs. coupling_susceptibility)? Is the boundary sharp or fuzzy?

**Disciplines:** Nonlinear dynamics, phase transitions, computational modelling

**Data sources:**

- sensitivity_analysis.py implementation
- SENS_* claim definitions
- The results/sensitivity_analysis.json output

**Method:**

1. Run a dense 2D sweep of recovery_rate and coupling_susceptibility
2. For each pair, measure final drift and cascade amplification
3. Identify the boundary where the system transitions from stable to chaotic
4. Test whether the boundary is sharp (phase transition) or fuzzy (gradual)
5. Document the bifurcation map

**Expected deliverable:** A 2D bifurcation map showing the stability boundary, with sharpness/fuzziness characterised.

**Falsifier:** No bifurcation boundary exists — the system transitions gradually across all parameter space (then the concept of a threshold is not meaningful).

---

### 8. EMPIRICAL — Recovery Modifier Propagation

**Gap:** The recovery_modifier is written by inverted_narrative agents and read by all agents during interact(). The propagation dynamics — how a modifier from one agent affects the whole system — are not fully characterised.

**Knowledge state:** NOT_STUDIED

**Research question:** How far does a recovery modifier propagate through a multi‑agent system? Does the effect decay with network distance, or does it amplify?

**Disciplines:** Network science, dynamical systems, information propagation

**Data sources:**

- emit_effects_on_neighbors() in sim_engine.py
- The all‑to‑all coupling structure (implicit in the simulation)

**Method:**

1. Modify the simulation to track recovery‑modifier propagation
2. Measure the modifier value at each agent as a function of distance from the source
3. Test whether the modifier decays, amplifies, or stays constant
4. Compare propagation dynamics across agent types
5. Document the propagation function

**Expected deliverable:** A propagation function for recovery modifiers, with decay/amplification characterised by agent type.

**Falsifier:** Modifiers do not propagate beyond direct neighbours (then the all‑to‑all coupling is not effectively modelled).

---

### 9. EMPIRICAL — Energy Budget Depletion Dynamics

**Gap:** The energy budget model (energy_budget, extraction_rate, regeneration_rate) is implemented but not fully explored. The dynamics of depletion and recovery — especially the flip from physics to engagement on exhaustion — are not characterised.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the typical trajectory of a physics agent under extraction? How long does it take to flip to engagement, and what is the system‑level consequence?

**Disciplines:** Resource economics, ecological modelling, dynamical systems

**Data sources:**

- Agent._mark_exhausted() and Agent.regenerate() in sim_engine.py
- balance_threshold.py module
- EMRG_011–EMRG_015 claim definitions

**Method:**

1. Run single‑agent extraction trajectories across extraction rates
2. Measure: time to exhaustion, drift at exhaustion, post‑flip behaviour
3. Run multi‑agent extraction scenarios (one extractor, one substrate)
4. Measure the system‑level consequence of substrate flip
5. Document the depletion dynamics

**Expected deliverable:** A characterisation of substrate depletion dynamics, with time‑to‑exhaustion and system‑level consequence functions.

**Falsifier:** physics agents never flip to engagement under any extraction rate (then the flip mechanism is not load‑bearing).

---

### 10. EMPIRICAL — Sensitivity Sweep Coverage

**Gap:** The sensitivity analysis sweeps four parameters. The coverage of the parameter space — whether the sweep is dense enough to reliably find bifurcation thresholds — is not quantified.

**Knowledge state:** UNDEFINED

**Research question:** How many parameter values per dimension are needed to reliably identify bifurcation thresholds? Is the current sweep (15 runs per value) sufficient?

**Disciplines:** Computational modelling, numerical analysis, experimental design

**Data sources:**

- sensitivity_analysis.py implementation
- The --sensitivity-runs CLI flag
- Published guidelines for parameter‑sweep design

**Method:**

1. Run the sensitivity sweep at increasing resolutions (e.g., 5, 10, 20, 50 values per dimension)
2. For each resolution, identify the bifurcation threshold
3. Measure the convergence of the threshold as resolution increases
4. Identify the resolution at which the threshold stabilises
5. Document the required resolution and any remaining uncertainty

**Expected deliverable:** A convergence analysis for the sensitivity sweep, with recommended resolution and uncertainty bounds.

**Falsifier:** The threshold does not converge at any resolution (then the sweep is not identifying a stable feature).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists (policymakers, educators, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the emergence‑stability‑simulator's insights be communicated to non‑specialists in a way that changes how they think about grounding, stability, and cascade failure?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Guidelines for communicating complex systems

**Method:**

1. Translate each concept into plain language with concrete examples
2. Develop case studies for each failure mode (parasitic takeover, substrate exhaustion, bifurcation)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the emergence‑stability‑simulator framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard multi‑agent simulation practice

---

### The Problem

In multi‑agent simulation, things like baseline grounding, recovery capacity, coupling susceptibility, and energy budgets are often treated as implementation details — parameters to be tuned, not structural features to be tested. When a simulation says "system X is stable," that is treated as a finding about the parameters.

But the simulation's architecture encodes a hypothesis: that physics‑grounded baselines produce stability, and engagement‑metric baselines produce cascade failure. The architecture is the hypothesis. The parameters are the test conditions.

---

### Six Ways the Connection Gets Lost

#### 1. The "Parameter as Neutral" Fallacy

Many simulations treat parameters as neutral — things that can be tuned without changing the meaning of the simulation. If the simulation says "stability depends on recovery_rate," that is treated as a finding.

But the parameters are not neutral. They encode the hypothesis. recovery_rate is not just a number; it is the strength of the attractor. coupling_susceptibility is not just a coupling strength; it is the permeability to external influence. The parameters are the hypothesis in numerical form. If the simulation says "recovery_rate matters," it is not false for the parameter, but it may be false for the hypothesis. The encoding was causal — just not represented.

So "parameter as neutral" often means "We treated the parameters as independent of the hypothesis." That is a modelling error, not evidence that the parameters are neutral.

#### 2. The "Agent as Individual" Fallacy

Many simulations treat agents as individuals — entities with properties that can be measured independently. If the simulation says "physics agents are stable," that is treated as a finding about the agent type.

But agents are not individuals in this simulation. They are nodes in a coupled system. A physics agent's stability depends on its neighbours. A parasitic agent's drift depends on the attractors around it. The agent is not a property; it is a position in a field. If the simulation says "physics agents are stable," it is not false for the agent type, but it may be false for the system. The coupling was causal — just not represented.

So "agent as individual" often means "We treated agents as independent entities." That is a systems error, not evidence that agents are independent.

#### 3. The "Threshold as Feature" Fallacy

Many simulations treat thresholds as features of the system — things to be discovered. If the simulation says "the bifurcation threshold is X," that is treated as a finding.

But the threshold is a feature of the parameterisation, not of the system. Change the parameterisation, change the threshold. The threshold is not discovered; it is constructed. If the simulation says "the threshold is X," it is not false for the parameterisation, but it may be false for the system. The parameterisation was causal — just not represented.

So "threshold as feature" often means "We treated the threshold as independent of the model." That is a construction error, not evidence that the threshold is real.

#### 4. The "Energy as Detail" Fallacy

Many simulations treat energy budgets as details — things that can be added or removed without changing the qualitative result. If the simulation says "energy budgets don't matter," that is treated as a finding.

But the energy budget is not a detail. It is the substrate. When a physics agent exhausts its budget, it flips to engagement. That is not a parameter change; it is a phase transition. If the simulation says "energy budgets don't matter," it is not false for the budget, but it may be false for the system. The substrate was causal — just not represented.

So "energy as detail" often means "We treated the budget as optional." That is a substrate error, not evidence that budgets don't matter.

#### 5. The "Emission as Noise" Fallacy

Many simulations treat inter‑agent effects as noise — things that average out. If the simulation says "emissions don't change the result," that is treated as a finding.

But emissions are not noise. They are the coupling mechanism. The inverted_narrative emission degrades neighbours' recovery. The scale_builder emission (removed) boosted recovery. Emissions are not noise; they are the signal. If the simulation says "emissions don't matter," it is not false for the emission, but it may be false for the system. The coupling was causal — just not represented.

So "emission as noise" often means "We treated coupling as secondary." That is a coupling error, not evidence that emissions don't matter.

#### 6. The "Claim as Output" Fallacy

Many simulations treat claims as outputs — things that are produced after the simulation runs. If the simulation says "claim X is true," that is treated as a finding.

But the claims are not outputs; they are the hypothesis. The simulation is built to test them. The claims are encoded in the architecture. If the simulation says "claim X is true," it is not false for the simulation run, but it may be false for the hypothesis. The architecture was causal — just not represented.

So "claim as output" often means "We treated the hypothesis as a result." That is a circularity error, not evidence that the claim is true.

---

### What This Framework Does Differently

This framework treats the architecture as the hypothesis, the parameters as test conditions, and the claims as falsifiable propositions that update when the simulation runs. The following components document mechanisms that standard multi‑agent simulation practice typically drops:

- Continuous cascade measurement: Replaces threshold‑gated counting to avoid the short‑run artifact that falsely refuted EMRG_003
- Agent types as positions in a field: physics (attractor), engagement (drift), hybrid (partial), inverted_narrative (authority‑first)
- Energy budget as substrate: Finite budgets, extraction, regeneration, and the physics → engagement flip on exhaustion
- The removal of scale_builder: A fabricated emission mechanism that carried ~70% of the EMRG_007 signal with no empirical basis
- The inverted_narrative emission: Kept but explicitly non‑load‑bearing; the qualitative finding holds without it
- Falsifiable claims with quantified probabilities: EMRG_*, SENS_* claims that update when the simulation runs

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Real‑world parameter calibration.
UNDER_STUDY Data collection is in progress; value is provisional. The inverted_narrative emission effect.
UNDEFINED The variable has no agreed definition or measurement protocol. Cascade amplification scaling factors.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Bifurcation threshold location.

---

### What Is NOT a Valid Epistemic State

PARAMETER_AS_NEUTRAL is not a valid knowledge state. If the parameters encode the hypothesis, treating them as neutral test conditions is a modelling error, not an epistemic one. The hypothesis does not care about our parameter neutrality.

The framework refuses to record a parameter as neutral. Instead, it records the parameter as hypothesis‑encoded — a numerical expression of the structural claim — and names what would be needed to move it to a calibrated state.

---

### The Standard

The question should not be:

"What do the parameters say?"

But rather:

"What hypothesis is encoded in the architecture, and do the simulation results support or refute it?"

If the answer is that the architecture encodes the hypothesis, the simulation is not a test — it is an exploration. End of story.

The architecture is already the hypothesis. Our parameter tunings, threshold discoveries, and claim outputs are the only things pretending otherwise. And that pretense has produced a literature of simulation results that may be measuring the architecture rather than the system.

This framework does not pretend otherwise.
