---

## CLAIM_TABLE_v2.md

Claims about the delivered anchor‑interval/ folder, about what a Python stdlib environment can establish concerning it, and about the self‑reference protocol it inherits.

This is a model, not a measurement of any deployed system. The three scripts are runnable mechanisms with stated arithmetic. They do not measure any real system. They show what follows from the arithmetic — and name the run or measurement that would break each claim.

---

## REFUTATION_PROTOCOL

Two standing rules, carried from the rest of the repo:

- A failed check updates the claim, not the parameters. If a falsifier fires, the entry changes.
- Nothing in SOURCE_DROP.md is source‑checkable as delivered. The drop says so itself — the citation markers are mangled and unresolvable, and one venue attribution is explicitly flagged as unconfirmed.

| id | claim | status |
|---|---|---|
| `ANC_001` | In a corpus loop (corpus → model → outputs → corpus), coupling to an unauthored substrate degrades while every statistic computable from inside improves or goes quiet. The effect is carried entirely by lam — the shrinkage any regularized or capacity‑limited fit applies. | SUPPORTED |
| `ANC_002` | The model‑vs‑corpus consistency check (D1) is CONSTANT_SILENT. Its statistic falls as the drift proceeds — it measures how much of the corpus the model has yet to write, not how much it has drifted from the substrate. | SUPPORTED, structural |
| `ANC_003` | A corpus‑shift detector (D2) has a reachable fire branch and does not discriminate. On the null‑harness/ sweep — degrading arm as known signal, improving arm as known null, identical in every line but the provenance of the injected observations — FP ≥ TP at every threshold. The only threshold with TP − FP = 0 fires on nothing. | SUPPORTED |
| `ANC_004` | The anchor interval must be scheduled, not triggered. Confidence‑triggered anchoring never runs (0 of 24 generations) and its final coupling error is the no‑anchoring number (0.4141). Scheduled anchoring recovers monotonically in frequency (every‑12: 0.3867, every‑4: 0.2747, every‑2: 0.1629). | SUPPORTED |
| `ANC_005` | From a contemporary benchmark score alone, capability and criteria are not separable. A flat‑capability trajectory reproduces a rising one to 5.6e‑17. One equation, two unknowns per release — a rank problem, not a precision problem. | SUPPORTED |
| `ANC_006` | Holding one benchmark fixed across generations isolates the criteria‑drift term and identifies capability only up to that benchmark's own unknown gain and offset. Differences and their ratios are identified (0.428571 both ways); levels are not. | SUPPORTED |
| `ANC_007` | Seven co‑moving terms and one published number. At co‑movement loading 0.95, the attribution design carries N_eff = 1.22 independent directions against 7 claimed terms. The apparatus floor at loading 0 is 6.41, not 7. | SUPPORTED |
| `ANC_008` | The co‑movement is not a nuisance a better ablation removes. The architectural term was selected against the corpus — attention shapes fitted to language statistics, tokenizers to the writing system, context lengths to document lengths, objectives to what the corpus can score. The covariance was built in before any experiment started. SUPPORTED as stated, | UNMEASURED |
| `ANC_009` | The drift‑literature retraining remedy and the irrecoverability claim are not two opinions about one regime. They are two regimes, separated by one measurable quantity: f, the fraction of the re‑acquisition pool that is downstream of the system being corrected. Above f = 0.143 (at bias 0.35, tolerance 0.05) the target is outside the reachable set at any n. | SUPPORTED |
| `ANC_010` | The drop's own coverage reading — every literature hit lands on a non‑coupling branch — is a second independent instrument returning the same shape as ../measurement‑fork/'s empty SAME‑QUANTITY cell. Not a defect verdict; a gap. The citation markers in SOURCE_DROP.md are unresolvable as delivered. | UNVERIFIED |
| `ANC_011` | "Literature contains what survives removal of the body." The creek‑crossing case — read pillow‑at‑2‑o'clock, predict force, take the step, compare, update the reading rule — is a closed calibration loop. The named instrument is ../inverseminar/'s CANNOT DERIVE channel. No round has been run. | OPEN |

---

## UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the anchor‑interval framework, organized by discipline

---

### 1. EMPIRICAL — The lam = 0 Fixed‑Point Test

**Gap:** ANC_001's falsifier states: at lam = 0, the loop becomes a fixed point on the corpus mean and coupling drift falls from +0.0537 to +0.0063. This is demonstrated arithmetically. The empirical question is: does any real system have lam = 0?

**Knowledge state:** UNKNOWN_ATM

**Research question:** What is the distribution of lam (shrinkage toward a prior) in real deployed systems? Are there any with lam = 0?

**Disciplines:** Machine learning, statistics, software engineering

**Data sources:**

- Published model documentation (training objectives, regularization terms)
- Open‑source model implementations
- Industry surveys of ML deployment practices

**Method:**

1. Survey the regularization practices of deployed ML systems
2. Extract the effective lam from each system's loss function
3. Compute the distribution
4. Test whether any system has lam = 0 (identity on its own output)
5. Document the range and central tendency

**Expected deliverable:** An empirical distribution of lam values in real systems.

**Falsifier:** A significant fraction of systems have lam = 0 (then the self‑consuming loop is not universal).

---

### 2. EMPIRICAL — D2 Discrimination Test

**Gap:** ANC_003 states that a corpus‑shift detector (D2) does not discriminate between degrading and improving arms — FP ≥ TP at every threshold. This is demonstrated on a synthetic sweep. The empirical question is: does any real corpus‑shift detector discriminate?

**Knowledge state:** UNDER_STUDY

**Research question:** Do real‑world drift detectors (e.g., in MLOps pipelines) separate degrading from improving shifts when the only difference is provenance?

**Disciplines:** MLOps, monitoring, software engineering

**Data sources:**

- Open‑source drift detection libraries (e.g., alibi‑detect, scikit‑multiflow)
- Published drift detection benchmarks
- Industry drift detection deployments

**Method:**

1. Identify corpus‑shift detectors used in practice
2. Run them on the null‑harness/ sweep (degrading arm vs. improving arm)
3. Compute TP, FP, and the best threshold
4. Test whether any detector achieves TP − FP > 0.5
5. Document which detectors (if any) discriminate

**Expected deliverable:** An empirical test of drift detector discrimination on the null‑harness design.

**Falsifier:** A detector achieves TP − FP > 0.5 (then the claim is falsified for that detector).

---

### 3. EMPIRICAL — Confidence‑Triggered Anchoring

**Gap:** ANC_004 states that confidence‑triggered anchoring never runs — 0 of 24 generations — because the statistic that would trigger it is computed inside the layer it would be detecting. The empirical question is: does confidence‑triggered anchoring ever fire in real systems?

**Knowledge state:** NOT_STUDIED

**Research question:** Do real‑world confidence‑triggered monitors ever fire? Or do they systematically fail to fire because the confidence metric drifts with the system?

**Disciplines:** MLOps, monitoring, AI safety

**Data sources:**

- Published ML monitoring deployments
- Industry case studies of confidence‑based triggers
- Open‑source monitoring implementations

**Method:**

1. Survey confidence‑based monitoring deployments
2. Extract firing rates and conditions
3. Test whether firing correlates with actual degradation
4. Document false negative rates
5. Compare to scheduled monitoring alternatives

**Expected deliverable:** An empirical study of confidence‑triggered monitoring efficacy.

**Falsifier:** Confidence‑triggered monitors fire on degradation with high recall (then scheduled anchoring is not necessary).

---

### 4. EMPIRICAL — Benchmark Capability vs. Criteria Separability

**Gap:** ANC_005 and ANC_006 state that from a contemporary benchmark score alone, capability and criteria are not separable — one equation, two unknowns per release. The empirical question is: does any published benchmark design recover capability levels?

**Knowledge state:** UNKNOWN_ATM

**Research question:** Can a fixed‑benchmark design recover capability levels independently of criteria drift? What is the traceability claim about the benchmark?

**Disciplines:** Metrology, ML benchmarking, philosophy of measurement

**Data sources:**

- Published ML benchmarks (GLUE, SuperGLUE, MMLU, etc.)
- Benchmark versioning and update histories
- Metrology literature on reference standards

**Method:**

1. Identify benchmarks with fixed item sets across releases
2. Check whether the benchmark has an independent reference standard
3. Test whether capability levels can be recovered from the fixed benchmark
4. Document which benchmarks have traceability claims
5. Propose a traceability framework for ML benchmarks

**Expected deliverable:** A traceability analysis of major ML benchmarks.

**Falsifier:** A benchmark with a known independent reference standard recovers capability levels (then the claim is falsified for that benchmark).

---

### 5. EMPIRICAL — Co‑movement of Seven Terms

**Gap:** ANC_007 states that at co‑movement loading 0.95, the attribution design carries N_eff = 1.22 independent directions against 7 claimed terms. The empirical question is: what is the actual co‑movement of the seven terms across real release pairs?

**Knowledge state:** NOT_STUDIED

**Research question:** Across real AI model releases, how many independent directions do the seven co‑moving terms actually span?

**Disciplines:** AI/ML, statistics, metrology

**Data sources:**

- Model release documentation (dates, capabilities, architectures)
- Published performance measurements across releases
- Model cards and release notes

**Method:**

1. Identify the seven terms named in SOURCE_DROP.md
2. Collect measurements across real release pairs
3. Compute the correlation matrix
4. Compute N_eff (the participation ratio)
5. Compare to the claimed 7 independent directions

**Expected deliverable:** An empirical N_eff for real release series.

**Falsifier:** Measured N_eff > 4 (then the attribution is well‑posed for that release series).

---

### 6. EMPIRICAL — Architectural Term Selection Against Corpus

**Gap:** ANC_008 states that the co‑movement is not removable because the architectural term was selected against the corpus. The falsifier is: an architectural term chosen without reference to the corpus should decorrelate the pair. The empirical question is: does a corpus‑independent architectural term decorrelate?

**Knowledge state:** NOT_STUDIED

**Research question:** If we transfer an architectural term from another modality (e.g., vision) or fix it before the corpus exists, does it decorrelate from the corpus‑fitted terms?

**Disciplines:** AI/ML, transfer learning, experimental design

**Data sources:**

- Vision‑to‑language transfer architectures
- Architecture search spaces
- Published transfer learning studies

**Method:**

1. Identify an architectural term chosen without reference to the corpus
2. Measure its co‑movement with corpus‑fitted terms
3. Compare to corpus‑fitted terms' co‑movement
4. Test whether the loading is lower
5. Document the result

**Expected deliverable:** An empirical test of the corpus‑selection hypothesis.

**Falsifier:** The corpus‑independent term has co‑movement as high as corpus‑fitted terms (then the selection mechanism is not what produces the co‑movement).

---

### 7. EMPIRICAL — f Measurement on Real Retraining Pools

**Gap:** ANC_009 states that f — the fraction of the re‑acquisition pool downstream of the system being corrected — separates two regimes. Above f = 0.143 (at bias 0.35, tolerance 0.05) the target is outside the reachable set at any n. The empirical question is: what is f in real retraining pools?

**Knowledge state:** NOT_STUDIED

**Research question:** In real ML retraining pipelines, what fraction of the re‑acquisition pool is downstream of the system being corrected?

**Disciplines:** MLOps, data engineering, software engineering

**Data sources:**

- ML retraining pipeline documentation
- Data lineage and provenance tracking
- Industry ML deployment case studies

**Method:**

1. Identify ML retraining pipelines with documented data provenance
2. For each pipeline, compute f — the fraction of the re‑acquisition pool that is downstream of the system
3. Compare f to the threshold (0.143 at bias 0.35)
4. Document the distribution of f across pipelines
5. Test whether f correlates with retraining efficacy

**Expected deliverable:** An empirical distribution of f in real retraining pipelines.

**Falsifier:** f ≈ 0 for a significant fraction of pipelines (then retraining works as advertised).

---

### 8. LITERATURE — Resolving SOURCE_DROP.md Citations

**Gap:** ANC_010 states that the citation markers in SOURCE_DROP.md are mangled and unresolvable as delivered. The empirical question is: do the named works measure coupling‑level quantities?

**Knowledge state:** UNKNOWN_ATM

**Research question:** Do Besbes/Gur/Zeevi (variation budget), Ulrich 1983 (boundary critique), and Jasanoff (co‑production) measure coupling‑level quantities carried by the system rather than by an external monitor?

**Disciplines:** Literature review, metascience, research methods

**Data sources:**

- Besbes, Gur, Zeevi (variation budget, V^{1/3}T^{2/3})
- Ulrich 1983 (boundary critique, critical systems thinking)
- Jasanoff (co‑production, STS)
- The resolved citations themselves

**Method:**

1. Resolve the mangled citations
2. Read each named work
3. Extract whether the quantity measured is coupling‑level (carried by the system) or instrument‑level (carried by an external monitor)
4. Classify each work
5. Document the findings

**Expected deliverable:** A resolved citation analysis with classification.

**Falsifier:** Any named work measures a coupling‑level quantity carried by the system rather than by an external monitor.

---

### 9. EMPIRICAL — Creek‑Crossing Calibration Loop

**Gap:** ANC_011 names the creek‑crossing case — read pillow‑at‑2‑o'clock, predict force, take the step, compare, update the reading rule — as a closed calibration loop. The empirical question is: can this loop be instantiated in a real system?

**Knowledge state:** OPEN

**Research question:** What does a real creek‑crossing calibration loop look like? Can it be built and tested?

**Disciplines:** Experimental design, calibration, epistemology

**Data sources:**

- The creek‑crossing description in SOURCE_DROP.md
- ../inverseminar/'s CANNOT DERIVE channel
- Published calibration studies

**Method:**

1. Define the creek‑crossing loop operationally
2. Build a working implementation
3. Test the loop with synthetic and real data
4. Document the loop's behavior
5. Compare to the anchor‑interval predictions

**Expected deliverable:** A working creek‑crossing calibration loop implementation.

**Falsifier:** The loop cannot be instantiated (then the case is not informative).

---

### 10. EMPIRICAL — Irrecoverability Claim Test

**Gap:** The irrecoverability claim states: baseline is only acquirable during a stable interval. Once the system is deviating, no clean reference exists to acquire. The empirical question is: are baselines ever recoverable during deviation?

**Knowledge state:** NOT_STUDIED

**Research question:** In real systems, can a clean reference be acquired during deviation? Or is the irrecoverability claim empirically true?

**Disciplines:** MLOps, monitoring, metrology

**Data sources:**

- ML retraining pipeline logs
- Reference acquisition records
- System state during deviation events

**Method:**

1. Identify systems with documented deviation events
2. Check whether a clean reference was acquired during the deviation
3. Compare to references acquired during stable intervals
4. Test whether the irrecoverability claim holds
5. Document the conditions under which references are acquirable

**Expected deliverable:** An empirical test of the irrecoverability claim.

**Falsifier:** A clean reference is acquired during deviation (then the claim is falsified).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists.

**Knowledge state:** NOT_STUDIED

**Research question:** How can the anchor‑interval framework's insights be communicated to non‑specialists in a way that changes how they think about self‑monitoring systems?

**Disciplines:** Science communication, policy, AI governance

**Data sources:**

- The framework itself
- Published science communication research
- Policy documents on AI monitoring

**Method:**

1. Translate each claim into plain language
2. Develop case studies for each failure mode
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the anchor‑interval framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard drift‑detection practice

---

### The Problem

In drift detection and MLOps, things like the provenance of the retraining corpus, the shrinkage of the fit, and the self‑reference of the monitor are not separate from the drift measurement. They are direct, material, contributing factors to whether the monitor can see the drift. When a monitoring system says "drift detected" or "no drift detected," that is treated as a fact about the system.

But the monitor is computed inside the layer it would be detecting. Its statistics are computed on the same substrate as the drift. If the system writes its own corpus, the monitor's statistics improve while coupling to reality degrades. The monitor is not measuring drift; it is measuring how much of the corpus the system has yet to write.

---

### Six Ways the Connection Gets Lost

#### 1. The "Monitor as External" Fallacy

Many drift detection systems assume the monitor is external to the system it monitors. If the monitor says "no drift," that is treated as a fact about the system.

But the monitor is computed on the same substrate as the drift. Its statistics are functions of the corpus. If the corpus is written by the system, the monitor drifts with the system. The monitor is not external — it is an internal instrument, and it drifts with everything else. If the monitor says "no drift," it is not false for the monitor's statistics, but it may be false for the system. The self‑reference was causal — just not represented.

So "monitor as external" often means "We assumed the monitor is independent of the system." That is a design error, not evidence that the monitor is independent.

#### 2. The "Fit as Identity" Fallacy

Many monitoring systems assume that a fit is an identity map — that the model perfectly represents the corpus. If the model says "the corpus is X," that is treated as a fact about the corpus.

But a fit is not an identity map. Any shrinkage toward a prior, lam in the code, means the model does not perfectly represent the corpus. When outputs enter the corpus and the model refits, the model moves toward its own outputs. The fit is not a measurement of the corpus; it is a measurement of how much of the corpus the model has yet to write. If the model says "the corpus is X," it is not false for the fit, but it may be false for the corpus. The shrinkage was causal — just not represented.

So "fit as identity" often means "We assumed the model perfectly represents the corpus." That is a mathematical error, not evidence that the fit is identity.

#### 3. The "Confidence as Signal" Fallacy

Many monitoring systems use confidence as a signal of reliability. If confidence is high, that is treated as evidence that the system is working.

But confidence is computed inside the layer it would be detecting. In the anchor‑interval simulation, confidence‑triggered anchoring never runs — 0 of 24 generations — because the statistic that would trigger it is computed inside the drifted layer. Confidence does not signal reliability; it signals how much of the corpus the system has written. If confidence is high, it may mean the system is tightly coupled to its own outputs, not to reality.

So "confidence as signal" often means "We treated confidence as independent of drift." That is a measurement error, not evidence that confidence signals reliability.

#### 4. The "Benchmark as Fixed" Fallacy

Many capability measurements use a fixed benchmark. If the benchmark score rises, that is treated as evidence that capability rose.

But a benchmark is not fixed in the relevant sense. The capability and the criteria are not separable. One equation, two unknowns per release. A flat‑capability trajectory reproduces a rising one to 5.6e‑17. The benchmark does not measure capability; it measures capability plus criteria drift. If the score rises, it may be capability rising, criteria drifting, or both.

So "benchmark as fixed" often means "We assumed the criteria are stable." That is a metrological error, not evidence that the criteria are stable.

#### 5. The "Retraining as Remedy" Fallacy

Many drift detection systems treat retraining as the remedy. If drift is detected, retrain on recent data.

But retraining presupposes a clean reference is obtainable on demand. The irrecoverability claim states: baseline is only acquirable during a stable interval. Once the system is deviating, no clean reference exists to acquire. If the retraining corpus is downstream of the system, retraining does not fix the drift — it entrenches it. The retraining remedy has a precondition nobody states.

So "retraining as remedy" often means "We assumed a clean reference is available." That is a precondition error, not evidence that retraining fixes drift.

#### 6. The "Provenance as Detail" Fallacy

Many monitoring systems treat data provenance as an implementation detail. If the data comes from the right source, that is treated as sufficient.

But f — the fraction of the re‑acquisition pool downstream of the system — is the one measurable quantity that separates the two regimes. Below the floor f·b, no schedule helps. Above f = 0.143 (at bias 0.35, tolerance 0.05), the target is outside the reachable set at any n. Provenance is not a detail; it is the primary axis. If f is high, retraining cannot work, regardless of the schedule.

So "provenance as detail" often means "We assumed provenance doesn't matter." That is a design error, not evidence that provenance is irrelevant.

---

### What This Framework Does Differently

This framework treats the monitoring system as potentially self‑referential — a system that writes its own corpus, measures itself with statistics computed on that corpus, and improves its internal consistency while its coupling to reality degrades. The following components document mechanisms that standard drift‑detection practice typically drops:

- corpus_loop.py — The loop: corpus → model → outputs → corpus. No adversary, no bad actor. The only ingredient is that a fit is not an identity map. D1 (CONSTANT_SILENT) falls as drift proceeds; D2 (corpus shift) does not discriminate; coupling error rises.
- moving_reference.py — Capability and criteria are not separable from a contemporary benchmark score. A fixed benchmark identifies capability only up to that benchmark's own unknown gain and offset. Differences are identified; levels are not.
- recoverability.py — Two regimes, separated by f, the fraction of the re‑acquisition pool downstream of the system. Above the floor, no schedule helps.
- The anchor interval — Must be scheduled, not triggered. Confidence‑triggered anchoring never runs because the statistic is computed inside the drifted layer.

---

### The Knowledge‑State Vocabulary

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The distribution of lam in real systems.
UNDER_STUDY Data collection is in progress; value is provisional. Whether drift detectors discriminate.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. f in real retraining pools.
OPEN The question is named and an instrument exists to answer it. The creek‑crossing calibration loop.

---

### What Is NOT a Valid Epistemic State

ASSUMPTION_OF_EXTERNALITY is not a valid knowledge state. If the monitor is computed on the same substrate as the drift, assuming it is external is a design error, not an epistemic one. The physics does not respect our monitoring boundaries.

The framework refuses to record a monitor as external because of assumption. Instead, it records the monitor as self‑referential — a system whose internal statistics improve while coupling to reality degrades — and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"What does the monitor say?"

But rather:

"Is the monitor computed inside the layer it would be detecting?"

If the answer is yes, the monitor's statistics are not measurements of drift — they are measurements of how much of the corpus the system has yet to write.

The system is already self‑referential. Our assumptions of externality, fixed benchmarks, and retraining remedies are the only things pretending otherwise. And that pretense has produced monitors that improve while coupling to reality degrades.

This framework does not pretend otherwise.
