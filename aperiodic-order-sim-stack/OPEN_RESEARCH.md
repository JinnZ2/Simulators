---

## CLAIM_TABLE_v2.md

Claims made by the drop (SIM_STACK_REPORT.txt) and by the audit (README.md, CLAIM_TABLE.md), each with the measurement that would refute it. Follows the claim-audits/ convention: D = the drop's own claim, A = an audit claim added here.

## REFUTATION_PROTOCOL

The generators were not shipped, so no claim below can be settled by rerunning the original sims. Each falsifier is therefore written as a new run someone with the generators can perform. Two rules, matching the repo's standing practice:

- A failed check updates the claim, not the estimator. If a falsifier fires, the entry is rewritten to what the new measurement says. Nothing here is retuned to preserve a prior.
- Absence of a detected feature is never entered as evidence of a difference unless a positive control has shown the method detects that feature when it is present. AOS_005 exists because the drop broke this rule.

---

| id | claim | status |
|---|---|---|
| `AOS_001` | The two shipped dimension estimators disagree in sign. Box counting gives D_f(AB) − D_f(Cascade) = +0.334 (plateau fit) and +0.240 (global fit). The sandbox estimator, on the same five point sets in the same drop, gives −0.247 (global) and −0.023 (plateau). The report publishes only the box‑counting family and does not mention the disagreement. | SUPPORTED |
| `AOS_002` | The sandbox estimator fails its own 1D control. The Line point set has an exactly known D_f = 1.000. The sandbox estimator returns 1.913 (global) and 1.844 (plateau) — an error larger than the effect under study. Box counting returns 1.000. This is the reason to keep the box‑counting result and discard the sandbox one. It is stated here because the report does not state it. | SUPPORTED |
| `AOS_003` | The decisive gap is largely inside the artifact budget. Sample size (12,000 → 1,024) moves box‑counting D_f by up to 0.137 on probes whose true dimension is fixed. Box‑ladder commensurability moves it by a further 0.115 on a known fractal at fixed N. Combined worst case 0.252, against a reported separation of 0.334. The budget is an upper bound (worst case per source, signs assumed to align); the residual 0.082 is a lower bound on the geometry signal. | SUPPORTED |
| `AOS_004` | The Cascade sample is both sparser and differently shaped than everything it is compared against. Ammann‑Beenker: 12,000 points, spans ±2. Cascade: 1,024 points, spans x ∈ [−8,18], y ∈ [−26,5]. Poisson, Lattice, Line: ~12,000 points, span ±20. The comparison is not matched for N or bounding box. The finite‑size ceiling is visible: Cascade flattens at log N = 3.0 (= 1,024 points); every other curve flattens at log N = 4.08 (= 12,000). | SUPPORTED |
| `AOS_005` | The drop's finite‑size baseline is matched‑N; the decisive difference is not. The report validates ` D_f(AB) − D_f(Cascade) |  |
| `AOS_006` | The three simulations do not "converge" in the sense the report claims. SIM‑B's dimension separation is artifact‑sized (AOS_003). SIM‑A compares peak counts (68 vs 14) and scaling exponents (−1.529 vs −0.069) — these are different quantities, not convergent evidence. SIM‑C's band‑edge splitting (0.0812 vs 0.0015, ratio 54.1) is a different energy scale, not a shared geometric signature. The report's "three independent simulations converge" is a rhetorical claim, not a measurement. | SUPPORTED |
| `AOS_007` | The control finite_n_control.py is stdlib‑only and runnable. It imports only math, random, and typing. It runs three probes (Poisson, Line, Cantor dust) at both sample sizes (12,000 and 1,024) and under two box ladders. It sizes the artifact budget that has to come off the top before a residual is called geometry. | SUPPORTED |
| `AOS_008` | The control does not reproduce the Ammann‑Beenker tiling or the branching cascade. The drop shipped results, not generators. It cannot recover the true Cascade dimension. It can only size the artifact budget that has to come off the top before a residual is called geometry. | SUPPORTED (by design) |
| `AOS_009` | The sandbox Line panel is the diagnostic one. Its local slope oscillates around 1.8–2.0 across the entire radius range, never approaching 1.0. The sandbox failure is systematic, not a bad window choice. | SUPPORTED |
| `AOS_010` | The eight shipped PNGs are checked in exactly as delivered. Not regenerated, not cropped, not recolored. The generator code was not shipped, so these figures are the only primary evidence for the drop's numbers. | SUPPORTED |
| `AOS_011` | The fit window is a free parameter with an effect comparable to the effect being measured. Global fit moves AB by 0.120 and the AB−Cascade gap from 0.240 to 0.334. The fit window is a free parameter with an effect comparable to the effect being measured. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the aperiodic‑order‑sim‑stack framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. GENERATOR RECONSTRUCTION — Ammann‑Beenker Tiling

**Gap:** The Ammann‑Beenker tiling generator was not shipped. The drop contains only results (12,000 points) and figures. The tiling cannot be regenerated from what arrived.

**Knowledge state:** UNKNOWN_ATM (generator missing)

**Research question:** What is the correct algorithm for generating the Ammann‑Beenker tiling point set used in the drop? Can it be reconstructed from the figures and the reported sample size?

**Disciplines:** Computational geometry, aperiodic order, software archaeology

**Data sources:**

- The shipped figures: sim_b_point_sets.png (AB panel: 12,000 points, spans ±2)
- Published literature on Ammann‑Beenker tilings (projection method, substitution rules)
- Open‑source implementations (e.g., hyperspy, quasiperiodic)

**Method:**

1. Identify the generation method from the point set's visual appearance (projection method vs. substitution)
2. Reimplement the generator to produce 12,000 points spanning ±2
3. Compare the reconstructed point set to the shipped figure (visual and statistical)
4. Document the reconstruction and any assumptions

**Expected deliverable:** A working Ammann‑Beenker generator that reproduces the shipped point set, with documentation.

**Falsifier:** The shipped point set cannot be reproduced from published algorithms (then the generator is custom and unrecoverable).

---

### 2. GENERATOR RECONSTRUCTION — Branching Cascade

**Gap:** The branching cascade generator was not shipped. The drop contains only results (1,024 points) and figures. The cascade cannot be regenerated from what arrived.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What is the correct algorithm for generating the branching cascade point set used in the drop? Can it be reconstructed from the figures and the reported sample size?

**Disciplines:** Computational geometry, branching processes, fractal geometry

**Data sources:**

- The shipped figures: sim_b_point_sets.png (Cascade panel: 1,024 points, spans x ∈ [−8,18], y ∈ [−26,5])
- Published literature on branching cascades and multiplicative cascades
- Open‑source implementations

**Method:**

1. Identify the generation method from the point set's visual appearance
2. Reimplement the generator to produce 1,024 points spanning the observed bounding box
3. Compare the reconstructed point set to the shipped figure
4. Document the reconstruction and any assumptions

**Expected deliverable:** A working branching cascade generator that reproduces the shipped point set, with documentation.

**Falsifier:** The shipped point set cannot be reproduced from published algorithms.

---

### 3. EMPIRICAL — Sandbox Estimator Fix

**Gap:** The sandbox estimator fails on the 1D Line control, returning 1.913 instead of 1.000. The failure is systematic, not a bad window choice.

**Knowledge state:** UNDER_STUDY

**Research question:** What is the cause of the sandbox estimator's failure on the 1D Line control? Can it be fixed by changing the estimator's implementation (e.g., boundary correction, radius range, fitting method)?

**Disciplines:** Computational geometry, fractal analysis, numerical methods

**Data sources:**

- The sandbox estimator implementation (if available) or its specification
- Published literature on sandbox / mass‑radius estimators
- The shipped figures: sim_b_sandbox.png, sim_b_sandbox_local.png

**Method:**

1. Implement the sandbox estimator from first principles
2. Run it on the Line control (points on the unit diagonal)
3. Identify the cause of the bias (boundary effects, radius range, fitting method)
4. Propose and test fixes
5. Document the fixed estimator and its performance on all controls

**Expected deliverable:** A corrected sandbox estimator that returns 1.000 on the Line control, with documentation of the fix.

**Falsifier:** The sandbox estimator cannot be fixed to return 1.000 on the Line control (then the estimator is fundamentally broken).

---

### 4. EMPIRICAL — Box‑Counting Artifact Budget

**Gap:** The artifact budget from finite‑N and box‑ladder commensurability is estimated at 0.252 worst‑case, against a reported separation of 0.334. The residual 0.082 is a lower bound on the geometry signal.

**Knowledge state:** UNDER_STUDY

**Research question:** What is the actual artifact budget for the box‑counting estimator on the Ammann‑Beenker and Cascade point sets? Does the residual geometry signal survive when sample sizes are matched?

**Disciplines:** Computational geometry, fractal analysis, numerical methods

**Data sources:**

- The control finite_n_control.py (runs Poisson, Line, Cantor dust at both sample sizes)
- The shipped figures: sim_b_boxcount.png, sim_b_boxcount_local.png
- The Ammann‑Beenker and Cascade point sets (if reconstructable)

**Method:**

1. Run finite_n_control.py to size the artifact budget on known fractals
2. Reconstruct the Ammann‑Beenker and Cascade point sets (Gaps 1 and 2)
3. Run box‑counting on both point sets at matched sample sizes (e.g., both at 1,024 or both at 12,000)
4. Compute the residual D_f(AB) − D_f(Cascade) after artifact correction
5. Determine whether the residual is statistically significant

**Expected deliverable:** A corrected box‑counting dimension separation with artifact budget subtracted, and a significance test.

**Falsifier:** The residual after artifact correction is ≤ 0 (then the separation is entirely artifact).

---

### 5. EMPIRICAL — Structure Factor Comparison

**Gap:** SIM‑A compares peak counts (68 vs 14) and scaling exponents (−1.529 vs −0.069). These are different quantities, not convergent evidence.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the correct way to compare the structure factors of quasiperiodic tilings and branching cascades? Are there any shared spectral signatures?

**Disciplines:** Solid state physics, aperiodic order, Fourier analysis

**Data sources:**

- The shipped figures (if any) for SIM‑A
- Published literature on structure factors of Ammann‑Beenker tilings
- Published literature on structure factors of branching cascades

**Method:**

1. Reconstruct the structure factor for both systems (if generators are available)
2. Define a common metric for comparison (e.g., integrated peak intensity, correlation dimension in Fourier space)
3. Compute the metric for both systems
4. Test whether the metric separates the two classes
5. Document the comparison

**Expected deliverable:** A common metric for structure factor comparison, with results for both systems.

**Falsifier:** The common metric does not separate the two classes (then SIM‑A's conclusion is not supported).

---

### 6. EMPIRICAL — Band‑Edge Splitting

**Gap:** SIM‑C compares band‑edge splitting at different energy scales (0.0812 vs 0.0015, ratio 54.1).

**Knowledge state:** NOT_STUDIED

**Research question:** Is there a shared threshold behavior between quasiperiodic tilings and branching cascades when normalized to a common energy scale?

**Disciplines:** Condensed matter physics, aperiodic order, spectral theory

**Data sources:**

- The shipped figures (if any) for SIM‑C
- Published literature on tight‑binding models on Ammann‑Beenker tilings
- Published literature on spectral properties of branching cascades

**Method:**

1. Reconstruct the tight‑binding model for both systems (if generators are available)
2. Define a common energy scale for both systems
3. Compute the band‑edge splitting as a function of disorder
4. Test whether the knee locations align when normalized
5. Document the comparison

**Expected deliverable:** A common‑scale comparison of band‑edge splitting for both systems.

**Falsifier:** The knee locations do not align when normalized (then SIM‑C's conclusion is supported).

---

### 7. EMPIRICAL — Cascade Sample Size Effect

**Gap:** The Cascade sample size is 1,024, while all other samples are ~12,000. The finite‑size ceiling is visible: Cascade flattens at log N = 3.0 (= 1,024 points); every other curve flattens at log N = 4.08 (= 12,000).

**Knowledge state:** UNDER_STUDY

**Research question:** How does the box‑counting dimension of the Cascade point set change when the sample size is increased to 12,000 (matched to the AB sample)?

**Disciplines:** Computational geometry, fractal analysis, numerical methods

**Data sources:**

- The Cascade point set (if reconstructable, Gap 2)
- The box‑counting estimator from the drop (or a reimplementation)

**Method:**

1. Reconstruct the Cascade point set (Gap 2)
2. Generate additional Cascade points to reach 12,000 (if the generator is known)
3. Run box‑counting on the 1,024‑point and 12,000‑point versions
4. Compute the change in D_f with sample size
5. Compare the 12,000‑point Cascade dimension to the AB dimension

**Expected deliverable:** A matched‑N box‑counting comparison of AB and Cascade, with the sample‑size effect quantified.

**Falsifier:** The Cascade dimension at 12,000 points is still significantly different from AB (then the separation is not purely an artifact of sample size).

---

### 8. EMPIRICAL — Bounding Box Effect

**Gap:** The Cascade bounding box (x ∈ [−8,18], y ∈ [−26,5]) is different from the AB bounding box (±2) and the others (±20).

**Knowledge state:** NOT_STUDIED

**Research question:** How does the bounding box shape and size affect box‑counting dimension estimates? Does the Cascade's elongated bounding box bias its dimension downward?

**Disciplines:** Computational geometry, fractal analysis, numerical methods

**Data sources:**

- The shipped point sets (if reconstructable)
- The box‑counting estimator

**Method:**

1. Reconstruct the Cascade point set (Gap 2)
2. Apply a similarity transform to match the Cascade bounding box to the AB bounding box (span ±2)
3. Run box‑counting on the transformed set
4. Compare the dimension before and after transformation
5. Determine whether the bounding box shape biases the estimate

**Expected deliverable:** A bounding‑box correction for the Cascade dimension estimate.

**Falsifier:** The bounding box shape has no effect on the dimension estimate (then the different shape is not a confound).

---

### 9. LITERATURE — Quasiperiodic vs. Cascade Geometry

**Gap:** The drop asks: "do quasiperiodic tilings and branching cascades share a geometry, or do they only share the property of not being periodic?" The literature on this question is not surveyed.

**Knowledge state:** NOT_STUDIED

**Research question:** What does the existing literature say about the relationship between quasiperiodic tilings and branching cascades? Are they known to share geometric properties?

**Disciplines:** Aperiodic order, fractal geometry, dynamical systems

**Data sources:**

- Published literature on quasiperiodic tilings (Ammann‑Beenker, Penrose)
- Published literature on branching cascades and multiplicative cascades
- Literature on the intersection of aperiodic order and fractal geometry

**Method:**

1. Conduct a literature review on the geometry of quasiperiodic tilings and branching cascades
2. Identify any known shared properties (e.g., scaling exponents, Fourier spectra, multifractal spectra)
3. Compare the literature findings to the drop's results
4. Document the literature consensus (or lack thereof)

**Expected deliverable:** A literature review on the geometric relationship between quasiperiodic tilings and branching cascades.

**Falsifier:** The literature shows a known shared geometry (then the drop's question is already answered).

---

### 10. METHODOLOGICAL — Estimator Selection Criteria

**Gap:** The report selects box‑counting over sandbox without stating the selection criteria. The sandbox estimator fails the 1D control, but the report does not mention this.

**Knowledge state:** UNDEFINED

**Research question:** What are the correct criteria for selecting a dimension estimator in a comparative study? How should estimator failures on known controls be reported?

**Disciplines:** Metrology, fractal analysis, scientific methodology

**Data sources:**

- The drop's estimator selection (implicit)
- Published guidelines for fractal dimension estimation
- The shipped figures and control results

**Method:**

1. Define explicit criteria for estimator selection (e.g., accuracy on known controls, precision, robustness to N)
2. Apply the criteria to both estimators (box‑counting and sandbox)
3. Document which estimator passes the criteria and why
4. Propose a reporting standard for estimator failures on controls

**Expected deliverable:** A methodological note on estimator selection criteria for fractal dimension studies.

**Falsifier:** Both estimators pass the criteria (then the selection is ambiguous).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists.

**Knowledge state:** NOT_STUDIED

**Research question:** How can the aperiodic‑order‑sim‑stack audit's insights be communicated to non‑specialists in a way that changes how they think about simulation results and artifact budgets?

**Disciplines:** Science communication, research methodology, education

**Data sources:**

- The audit itself
- Published science communication research
- Guidelines for communicating uncertainty

**Method:**

1. Translate each claim into plain language with concrete examples
2. Develop case studies for each failure mode (estimator disagreement, sample size mismatch, bounding box difference)
3. Create a user guide explaining: "What this audit means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the aperiodic‑order‑sim‑stack audit.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this audit is broader than standard simulation reporting practice

---

### The Problem

In simulation reporting, things like estimator selection, sample size matching, bounding box shape, and artifact budgeting are not separate from the conclusion. They are direct, material, contributing factors to whether the conclusion is supported. When a report says "the dimensions separate," that is treated as a finding about geometry.

But the report's own figures show the comparison was not matched for sample size or bounding box. The estimator that supports the conclusion passes its controls; the estimator that contradicts it fails its controls — but the failure is not reported. The artifact budget from known confounds is comparable to the reported separation. The report's conclusion is not a measurement of geometry; it is a measurement plus artifacts, with the artifacts unsubtracted.

---

### Six Ways the Connection Gets Lost

#### 1. The "One Estimator" Fallacy

Many studies use a single estimator. If the estimator says "dimensions separate," that is treated as a finding.

But two estimators were run on the same point sets. They disagree in sign. One supports the conclusion; the other contradicts it. The report publishes only the supporting one. The estimator selection is not justified; the contradictory estimator is not mentioned. If the report says "dimensions separate," it is not false for the box‑counting estimator, but it may be false for the geometry. The estimator choice was causal — just not represented.

So "one estimator" often means "We selected the estimator that supports our conclusion." That is a reporting bias, not evidence that the geometry separates.

#### 2. The "Control as Hygiene" Fallacy

Many studies run controls and treat them as hygiene — something that passes and is then forgotten. If the control passes, that is treated as validation of the method.

But the sandbox estimator fails its 1D control. The Line point set has an exactly known D_f = 1.000. The sandbox estimator returns 1.913. The error is larger than the effect under study. The report does not mention this failure. The control is not hygiene; it is a diagnostic. If the report treats the control as hygiene, it misses the diagnostic.

So "control as hygiene" often means "We ran the control and ignored the failure." That is a methodological error, not evidence that the estimator is valid.

#### 3. The "Matched‑N Baseline" Fallacy

Many studies use a matched‑N baseline to validate their method. If the baseline is small, that is treated as evidence that finite‑N effects are small.

But the baseline is matched‑N; the decisive difference is not. The report validates |D_f(AB) − D_f(Cascade)| = 0.334 against a baseline |D_f(AB) − D_f(Poisson)| = 0.021. AB and Poisson are both ~12,000 points. Cascade is 1,024. The baseline is matched‑N; the decisive difference is not. The finite‑size ceiling is the point count itself. If the report says "finite‑N effects are small," it is not false for the matched‑N comparison, but it may be false for the unmatched one.

So "matched‑N baseline" often means "We compared matched‑N sets and then compared unmatched sets." That is a logical error, not evidence that finite‑N effects are small.

#### 4. The "Bounding Box as Detail" Fallacy

Many studies treat bounding box shape as a detail. If the point sets have different bounding boxes, that is treated as irrelevant.

But the Cascade bounding box is different from everything it is compared against. AB spans ±2; Cascade spans x ∈ [−8,18], y ∈ [−26,5]; the rest span ±20. The shape and size of the bounding box affect box‑counting estimates. If the report says "the dimensions separate," it is not false for the bounding boxes as shipped, but it may be false for the geometry. The bounding box was causal — just not represented.

So "bounding box as detail" often means "We assumed shape doesn't matter." That is a geometric error, not evidence that shape is irrelevant.

#### 5. The "Artifact as Noise" Fallacy

Many studies treat artifacts as noise — something that can be ignored if the signal is large enough. If the separation is larger than the artifact budget, that is treated as evidence.

But the artifact budget is comparable to the reported separation. Sample size moves box‑counting D_f by up to 0.137. Box‑ladder commensurability moves it by a further 0.115. Combined worst case 0.252, against a reported separation of 0.334. The residual 0.082 is a lower bound on the geometry signal, not a confirmed signal. If the report says "the dimensions separate," it is not false for the raw numbers, but it may be false for the geometry after artifact subtraction.

So "artifact as noise" often means "We assumed artifacts are small." That is a numerical error, not evidence that artifacts are negligible.

#### 6. The "Convergence as Rhetoric" Fallacy

Many studies treat multiple simulations as convergent evidence. If three simulations point in the same direction, that is treated as strong evidence.

But the three simulations do not "converge" in the sense the report claims. SIM‑B's dimension separation is artifact‑sized. SIM‑A compares peak counts (68 vs 14) and scaling exponents (−1.529 vs −0.069) — these are different quantities, not convergent evidence. SIM‑C's band‑edge splitting (0.0812 vs 0.0015, ratio 54.1) is a different energy scale, not a shared geometric signature. The report's "three independent simulations converge" is a rhetorical claim, not a measurement.

So "convergence as rhetoric" often means "We called different quantities 'convergent' because they all support our conclusion." That is a logical error, not evidence that the conclusion is supported.

---

What This Audit Does Differently

This audit treats simulation results as potentially artifact‑contaminated — sample size mismatches, bounding box differences, estimator disagreement, and artifact budgets that must be subtracted before a geometry signal can be claimed. The following components document mechanisms that standard simulation reporting typically drops:

- finite_n_control.py — The estimator control the drop did not run. Sizes the artifact budget from finite‑N and box‑ladder commensurability on probes whose true dimension is known and independent of N.
- The eight shipped PNGs — Checked in exactly as delivered. The generator code was not shipped, so these figures are the only primary evidence.
- The two estimator families — Box‑counting (reported) and sandbox (unreported). They disagree in sign. The sandbox estimator fails its 1D control.
- The artifact budget — Sample size (12,000 → 1,024) moves box‑counting D_f by up to 0.137; box‑ladder commensurability moves it by a further 0.115. Combined worst case 0.252, against a reported separation of 0.334.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the audit records its epistemic state rather than excluding it:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The true dimension of the Cascade point set.
UNDER_STUDY Data collection is in progress; value is provisional. The artifact budget from finite‑N and box‑ladder commensurability.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. The effect of bounding box shape on dimension estimates.
UNDEFINED The variable has no agreed definition or measurement protocol. Estimator selection criteria.

---

### What Is NOT a Valid Epistemic State

REPORTING_AS_MEASUREMENT is not a valid knowledge state. If a reported number is contaminated by artifacts, treating it as a measurement of geometry is a reporting error, not an epistemic one. The geometry does not respect our estimator choices.

The audit refuses to record a reported number as a measurement without artifact subtraction. Instead, it records the number as a raw estimate — contaminated by sample size, bounding box, and estimator choice — and names what would be needed to move it to a corrected state.

---

### The Standard

The question should not be:

"What does the estimator say?"

But rather:

"What is the geometry signal after artifact subtraction?"

If the answer is that the residual is inside the artifact budget, the geometry is not established. End of story.

The geometry is already independent of our estimator choices. Our sample sizes, bounding boxes, and reporting biases are the only things pretending otherwise. And that pretense has produced a literature of separated dimensions that may be artifacts.

This audit does not pretend otherwise.
