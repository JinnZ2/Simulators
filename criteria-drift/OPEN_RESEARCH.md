---

## CLAIM_TABLE.md

Claims about the delivered criteria‑drift/ folder, about what a Python stdlib environment can establish concerning it, and about the repair protocol it inherits.

This is a measurement instrument, not a measurement. No real criteria‑drift finding is produced. The tool runs end‑to‑end on its own example data and reports the shape of the defect in the shipped code.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `CD_001` | The kit runs end‑to‑end on its own quick start, stdlib‑only, SQLite‑backed. Frame is a first‑class dataclass, unknown is legal, omission is flagged, and drift is computed per frame field. | SUPPORTED |
| `CD_002` | The drift metric is unsigned and the decision rule reads the sign. Every primitive returns a non‑negative distance, so widening and narrowing both push composite_drift up. | REPAIRED |
| `CD_003` | build_series() plants a y = 0.0 at the head of every model's series and pairs it with a real drift value. For Alpha‑1B it replaces a measured −0.04. | REPAIRED |
| `CD_004` | version_order is built from to_version, so the first criteria version and every score attached to it is dropped. Delta‑350M holds the longest baseline in the dataset and contributes nothing. | REPAIRED |
| `CD_005` | CD_003 and CD_004 together flip the sign of the only model with three real transitions — between the two opposite readings the README's decision rule offers. | REPAIRED |
| `CD_006` | The capability term is in the stated model and not in the code. Δscore = β₀ + β₁·drift + ε drops it, so the drift slope absorbs it. | REPAIRED (with a correction: the bridge was already in the shipped data; nothing used it) |
| `CD_007` | "Significant" appears twice in README.md and zero times in regress.py. No t‑statistic, no p‑value. The fits that exist have one degree of freedom, and r_squared: 1.0 at n=2 is emitted as a field next to an interpretation string saying the data is insufficient. | REPAIRED |
| `CD_008` | The bridge is anchor.py's argument, not unlogged_move.py's. anchor.py establishes the requirement from cross‑domain cases — an invariant scored across versions — and audit.py regress already refuses an identified criteria term without one. | SUPPORTED |
| `CD_009` | The unlogged move simulation shows that a confident wrong answer in the same shape as a right one is the failure mode. The prior readings stay present, numeric, in range, and continuous; nothing in the data marks the move. | SUPPORTED |

---

CD_002 — the drift metric is unsigned

The README separates three readings — ASSERTION, REVISION, REVISION_WITH_BRIDGE — and the decision rule reads the sign of the drift to decide which one applies. But every primitive returns a non‑negative distance. Widening and narrowing both push composite_drift up, so the same composite_drift value can describe a criterion that expanded or one that contracted. The direction is not encoded.

Repair: drift_sign.py now carries the hypothesis. The metric can carry direction. The selftest asserts that a widening and a narrowing criterion produce different signed drift values.

---

CD_003 — the fabricated point

build_series() plants a y = 0.0 at the head of every model's series and pairs it with a real drift value. For Alpha‑1B, it replaces a measured −0.04. The effect is that every model starts at zero, which biases the regression slope.

Repair: The planted point is removed. regression_audit.py reproduces the old builder in shipped_series() so the cost stays measurable.

---

CD_004 — the dropped baseline

version_order is built from to_version, so the first criteria version and every score attached to it is dropped. Delta‑350M holds the longest baseline in the dataset and contributes nothing. The first version is the one against which all drift is measured — dropping it drops the reference.

Repair: The version order now includes the first version. The selftest pins the fix.

---

CD_005 — the sign flip

CD_003 and CD_004 together flip the sign of the only model with three real transitions. Between the two opposite readings the README's decision rule offers, the shipped code produced one; the repaired code produces the other.

Repair: The flip is now measured against the repaired builder in regression_audit.py.

---

CD_006 — the missing capability term

The model is stated as Δscore = β₀ + β₁·drift + ε. The capability term is in the stated model and not in the code, so the drift slope absorbs it.

Correction: The original claim said "0 of 4 demo models carry scores on more than one non‑current version". That was wrong. The script that produced the number printed 2 of 4; the prose said 0. All four models span two or more versions, so the bridge is in the data. What is absent is any code that uses it — which is a smaller gap and a more damning one, because nothing had to be collected.

Repair: anchor.py now uses the bridge. The regress command refuses to run without one.

---

CD_007 — "significant" with no significance

"Significant" appears twice in README.md and zero times in regress.py. No t‑statistic, no p‑value. The fits that exist have one degree of freedom, and r_squared: 1.0 at n=2 is emitted as a field next to an interpretation string saying the data is insufficient.

Repair: regress.py now computes and reports t‑statistics and p‑values. The interpretation string is conditional on the data being sufficient.

---

CD_008 — the bridge is not new

anchor.py establishes the requirement from cross‑domain cases — an invariant scored across versions — and audit.py regress already refuses an identified criteria term without one. unlogged_move.py reaches the same requirement from a two‑reading toy and adds nothing to the case for it.

Recording that plainly, because operator‑structure‑echo/corroboration.py was written one commit ago and this is its INHERITED state on a real pair: same folder, same builder, same week. Two modules agreeing here is one position expressed twice.

---

CD_009 — the unlogged failure mode

The unlogged move simulation shows that prior readings stay present, numeric, in range, and continuous. Nothing in the data marks the move. The failure is not a gap where an answer should be — it is a confident wrong answer in the same shape as a right one. A blank announces itself; this does not.

---

## OPEN_QUESTIONS.md

Open questions in the criteria‑drift framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. EMPIRICAL — Criteria Drift in Real Benchmarks

**Gap:** The tool runs on example data. No real benchmark history (CodeBench, GLUE, SuperGLUE, MMLU) has been ingested and analysed.

**Knowledge state:** NOT_STUDIED

**Research question:** How much does criteria drift actually occur in published benchmarks? What is the distribution of composite_drift across real benchmark version histories?

**Disciplines:** Metrology, machine learning, bibliometrics

**Data sources:**

- Published benchmark version histories (GLUE, SuperGLUE, MMLU, HELM)
- Benchmark papers and documentation
- The criteria-drift ingestion pipeline

**Method:**

1. Identify benchmarks with documented version histories
2. Extract criteria frames for each version
3. Ingest into the criteria-drift database
4. Compute composite_drift for each transition
5. Document the distribution and identify the largest drift sources

**Expected deliverable:** A criteria‑drift analysis of real benchmarks, with per‑benchmark drift distributions and dominant drift sources.

**Falsifier:** composite_drift is near‑zero for all benchmarks (then criteria drift is not load‑bearing).

---

### 2. EMPIRICAL — Drift vs. Improvement Regression

**Gap:** The regression component runs on example data. No real regression of model improvement against criteria drift has been performed.

**Knowledge state:** NOT_STUDIED

**Research question:** What fraction of reported model improvement in published benchmarks is explained by criteria drift? Does the fraction vary by benchmark and model family?

**Disciplines:** Metrology, machine learning, econometrics

**Data sources:**

- Published model scores across benchmark versions
- The criteria-drift regression pipeline
- The anchor.py bridge construction

**Method:**

1. Collect model scores across benchmark versions
2. Identify models scored on multiple versions (the bridge)
3. Run the regression: Δscore = β₀ + β₁·composite_drift + ε
4. Compute the explained fraction (R² attributable to drift)
5. Test whether the slope is significant

**Expected deliverable:** A regression analysis of model improvement vs. criteria drift for real benchmarks, with per‑benchmark and per‑model results.

**Falsifier:** β₁ ≈ 0 and not significant for all benchmarks (then criteria drift does not explain improvement).

---

### 3. EMPIRICAL — The Anchor Construction

**Gap:** anchor.py demonstrates the anchor principle on planted data. No real anchor has been constructed for any benchmark.

**Knowledge state:** NOT_STUDIED

**Research question:** What constitutes a valid anchor for a benchmark? Can a frozen model, stable words, or a primary standard be constructed for real benchmarks?

**Disciplines:** Metrology, machine learning, philosophy of measurement

**Data sources:**

- Published benchmark version histories
- Model scores across versions
- The anchor.py construction logic

**Method:**

1. Identify candidate anchors for a benchmark:
- A frozen model scored on all versions
- A stable‑word subset of the test set
- An external primary standard
2. Construct the anchor
3. Compute the anchored score series
4. Test whether the anchor separates capability from criteria
5. Document the construction and validation

**Expected deliverable:** A constructed anchor for a real benchmark, with validation showing that it separates capability from criteria.

**Falsifier:** No valid anchor can be constructed (then the separation is not achievable).

---

### 4. EMPIRICAL — Unlogged Moves in Practice

**Gap:** unlogged_move.py demonstrates the unlogged failure mode on a synthetic series. No real unlogged criterion move has been identified.

**Knowledge state:** NOT_STUDIED

**Research question:** Do unlogged criterion moves occur in real benchmark histories? If so, how often and with what magnitude?

**Disciplines:** Metrology, machine learning, bibliometrics

**Data sources:**

- Published benchmark version histories
- Benchmark papers and documentation
- Model score histories

**Method:**

1. Identify benchmark version histories where a criterion change was not logged
2. Detect unlogged moves by comparing model scores to anchors
3. Estimate the magnitude of each unlogged move
4. Compute the frequency and magnitude distribution
5. Document the findings

**Expected deliverable:** A survey of unlogged criterion moves in real benchmarks, with frequency and magnitude estimates.

**Falsifier:** No unlogged moves can be detected (then the unlogged failure mode is theoretical).

---

### 5. METHODOLOGICAL — The Frame's Unknown State

**Gap:** unknown is a legal value in the Frame. The tool flags omitted fields but does not specify how to handle unknown in drift computation.

**Knowledge state:** UNDEFINED

**Research question:** How should unknown frame fields be handled in drift computation? Should they be treated as zero drift, as missing data, or as a separate state?

**Disciplines:** Metrology, survey methodology, measurement theory

**Data sources:**

- The schema.py Frame definition
- Published guidance on handling unknown values in measurement
- The criteria-drift drift computation engine

**Method:**

1. Define candidate treatments for unknown:
- Zero drift (assume no change)
- Missing data (exclude from composite)
- Separate state (treat as a distinct drift category)
2. Test each treatment on synthetic and real data
3. Compare the resulting drift distributions
4. Propose a standard treatment
5. Document the recommendation

**Expected deliverable:** A recommended treatment for unknown frame fields in drift computation, with empirical comparison.

**Falsifier:** The treatment does not affect results (then the choice is not load‑bearing).

---

### 6. EMPIRICAL — Drift Direction Distribution

**Gap:** The signed drift metric (drift_sign.py) computes direction, but the distribution of drift directions in real benchmarks is unknown.

**Knowledge state:** NOT_STUDIED

**Research question:** Does criteria drift tend to widen or narrow? Is there a systematic direction (e.g., criteria always expand, never contract)?

**Disciplines:** Metrology, machine learning, sociology of science

**Data sources:**

- Real benchmark version histories
- The drift_sign.py signed metric

**Method:**

1. Ingest real benchmark version histories
2. Compute signed drift for each transition
3. Test whether the mean signed drift is significantly different from zero
4. Test whether drift direction is correlated with benchmark age or field
5. Document the distribution

**Expected deliverable:** A signed drift distribution for real benchmarks, with tests for systematic direction.

**Falsifier:** The mean signed drift is zero (then drift is equally likely to widen or narrow).

---

### 7. EMPIRICAL — The Bridge and the Shipped Store

**Gap:** anchor.py notes that all four demo models span two or more versions, so the bridge is already in the data. But no code uses it.

**Knowledge state:** UNDER_STUDY

**Research question:** What does the regression produce when the bridge is actually used? Does the shipped data contain enough information to separate capability from criteria?

**Disciplines:** Metrology, machine learning, econometrics

**Data sources:**

- The example_data/ shipped with the kit
- The anchor.py bridge construction
- The regress.py regression pipeline

**Method:**

1. Use the shipped data with the bridge (models scored on multiple versions)
2. Run the regression with and without the bridge
3. Compare the results
4. Test whether the bridge changes the drift slope
5. Document the findings

**Expected deliverable:** A regression analysis of the shipped data using the bridge, with comparison to the bridge‑absent case.

**Falsifier:** The bridge does not change the regression results (then the shipped data does not separate capability from criteria).

---

### 8. EMPIRICAL — Shewhart Chart for Calibration Interval

**Gap:** anchor.py mentions a Shewhart chart as "the metrology instrument for deciding when a calibration interval has lapsed, which is K15." No implementation is provided.

**Knowledge state:** NOT_STUDIED

**Research question:** Can a Shewhart chart be constructed for benchmark criteria drift? What would be the control limits and what would a signal indicate?

**Disciplines:** Metrology, statistical process control, machine learning

**Data sources:**

- The anchor.py anchor construction
- Published Shewhart chart methodology
- Real benchmark version histories

**Method:**

1. Define the measurement process: anchor scores across versions
2. Compute the moving range or standard deviation
3. Set control limits (e.g., ±3 sigma)
4. Plot the anchor scores with control limits
5. Identify signals (points outside limits)
6. Interpret signals as calibration lapses

**Expected deliverable:** A Shewhart chart implementation for benchmark criteria drift, with control limits and signal interpretation.

**Falsifier:** No signals occur in real benchmark histories (then calibration intervals do not lapse).

---

### 9. EMPIRICAL — The Declared Frame in Other Domains

**Gap:** The declared‑frame block is used here for benchmarks. The cross‑domain notes in SOURCE_DROP_KIMI.md suggest it applies elsewhere.

**Knowledge state:** NOT_STUDIED

**Research question:** What other domains have declared frames that could be versioned and measured for drift? (e.g., regulatory criteria, clinical guidelines, educational standards)

**Disciplines:** Metrology, public policy, education, regulation

**Data sources:**

- Regulatory criteria version histories
- Clinical guideline updates
- Educational standard revisions
- The schema.py Frame definition

**Method:**

1. Identify domains with versioned criteria
2. Extract frames for each version
3. Ingest into the criteria-drift database
4. Compute drift for each domain
5. Compare drift patterns across domains

**Expected deliverable:** A cross‑domain drift analysis, with per‑domain drift distributions and comparisons.

**Falsifier:** No other domain has versioned criteria (then the frame is specific to benchmarks).

---

### 10. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists (policymakers, benchmark users, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the criteria‑drift framework's insights be communicated to non‑specialists in a way that changes how they think about benchmark scores and "progress"?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Benchmark reporting guidelines

**Method:**

1. Translate each concept into plain language with concrete examples
2. Develop case studies for each failure mode (unsigned drift, unlogged moves, missing bridge)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the criteria‑drift framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard benchmark reporting practice

---

### The Problem

In benchmark reporting, things like criteria versions, frame fields, drift metrics, and anchors are not separate from the reported improvement. They are direct, material, contributing factors to whether the improvement is real. When a paper says "model X improved by Y%," that is treated as a finding about the model.

But the ruler may have moved. The criteria may have expanded. The sign of "better" may have shifted. The judge model may have upgraded. Most of this is invisible in headline numbers.

---

### Six Ways the Connection Gets Lost

#### 1. The "Improvement as Capability" Fallacy

Many benchmark papers treat reported improvement as capability improvement. If the score goes up, that is treated as evidence that the model got better.

But the score is a product of capability and criteria: score = gain·capability + offset. If the criteria change (gain or offset), the score changes even if capability is flat. The reported improvement is not capability; it is capability plus criteria drift. If the paper says "improved by Y%," it is not false for the score, but it may be false for the capability. The criteria drift was causal—just not represented.

So "improvement as capability" often means "We assumed the criteria are fixed." That is a measurement error, not evidence that the improvement is real.

#### 2. The "Version as Decoration" Fallacy

Many benchmarks have version histories, but the versions are treated as decorations — minor updates that don't affect comparability. If the paper says "we used version X," that is treated as sufficient.

But the frame may have changed. boundary, horizon, who_counts, sign_source, logic, observer_access — any of these can drift between versions. The version number is not the frame. If the paper says "version X," it is not false for the number, but it may be false for the frame. The frame drift was causal—just not represented.

So "version as decoration" often means "We assumed versions are comparable." That is a metrological error, not evidence that the frame is stable.

#### 3. The "Signed Drift as Obvious" Fallacy

Many analyses treat drift direction as obvious — criteria either expand or contract, and you can tell which. If the analysis says "drift is X," that is treated as a finding.

But the drift metric is unsigned. Widening and narrowing both push composite_drift up. The same composite_drift value can describe a criterion that expanded or one that contracted. The direction is not encoded. If the analysis says "drift is X," it is not false for the magnitude, but it may be false for the direction. The sign was causal—just not represented.

So "signed drift as obvious" often means "We assumed the direction is self‑evident." That is a measurement error, not evidence that the direction is known.

#### 4. The "Anchor as Optional" Fallacy

Many analyses treat anchors as optional — nice to have but not required. If the analysis says "we controlled for drift," that is treated as sufficient.

But without an anchor, drift and capability are not separable. Δscore = β₀ + β₁·drift + ε drops the capability term, so the drift slope absorbs it. The regression is unidentified. If the analysis says "we controlled for drift," it is not false for the attempt, but it may be false for the identification. The anchor was causal—just not present.

So "anchor as optional" often means "We assumed separation is possible without one." That is an identification error, not evidence that the separation is valid.

#### 5. The "Logged Move as Decomposed" Fallacy

Many analyses treat logging a criterion move as sufficient for decomposition. If the move is logged, that is treated as evidence that the system and criterion are separated.

But logging alone does not decompose. REVISION returns None for the system attribution, not zero. Separating system from criterion needs a bridge — one measurement taken under both criteria — and without it UNKNOWN is the correct output. If the analysis says "the move is logged, so we know the split," it is not false for the log, but it may be false for the decomposition. The bridge was causal—just not present.

So "logged move as decomposed" often means "We assumed logging is sufficient." That is a decomposition error, not evidence that the split is known.

#### 6. The "Unlogged as Uninterpretable" Fallacy

Many analyses treat unlogged moves as making prior measurements uninterpretable. If the move is unlogged, that is treated as a gap.

But unlogged prior measurements do not become unreadable. They stay perfectly legible and mean something else: the series reads as a clean step in the system, with a number attached, and nothing in it is marked. The failure is not a gap where an answer should be; it is a confident wrong answer in the same shape as a right one. A blank announces itself; this does not.

So "unlogged as uninterpretable" often means "We assumed the only failure mode is missing data." That is a failure‑mode error, not evidence that unlogged moves are gaps.

---

### What This Framework Does Differently

This framework treats benchmark criteria as versioned artifacts with a declared frame, measures drift per frame field, and regresses reported improvement against drift. The following components document mechanisms that standard benchmark reporting practice typically drops:

- The declared frame: boundary, horizon, who_counts, sign_source, logic, observer_access. unknown is legal; omission is flagged.
- The signed drift metric: drift_sign.py carries the hypothesis that direction matters.
- The bridge: anchor.py — an invariant scored across versions — without which drift is unmeasurable and the regression refuses to run.
- The unlogged move: unlogged_move.py — the failure mode where the ruler moves and no version is cut.
- The repair audit: regression_audit.py reproduces the shipped builder so the cost of each defect stays measurable.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Criteria drift in real benchmarks.
UNDER_STUDY Data collection is in progress; value is provisional. The bridge in the shipped store.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The distribution of drift directions.
UNDEFINED The variable has no agreed definition or measurement protocol. Handling of unknown frame fields.

---

### What Is NOT a Valid Epistemic State

IMPROVEMENT_AS_CAPABILITY is not a valid knowledge state. If the reported improvement is a product of capability and criteria, treating it as capability is a measurement error, not an epistemic one. The capability does not care about our reporting conventions.

The framework refuses to record improvement as capability. Instead, it records improvement as capability plus drift — and names what would be needed to separate them: a bridge, measured across versions.

---

### The Standard

The question should not be:

"Did the model improve?"

But rather:

"Did the criteria move, and if so, by how much, in what direction, and was a bridge used to separate the two?"

If the answer is that the criteria moved and no bridge was used, the improvement is not identified. End of story.

The benchmark is already a product of capability and criteria. Our assumptions of fixed criteria, logged moves, and optional anchors are the only things pretending otherwise. And that pretense has produced a literature of reported improvements that may be measuring the ruler stretching.

This framework does not pretend otherwise.
