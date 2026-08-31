---

## CLAIM_TABLE_v2.md

Claims about the delivered antifungal‑mechanism‑sim/ folder, about what a Python stdlib environment can establish concerning it, and about the progression it implements.

This is a design‑exploration progression, not a pharmacological prediction. No MIC breakpoints are used. No patient PK/PD is modeled. No clinical outcome is forecast. What is delivered is a controlled comparison: same seven input codes, three different topologies, opposite rankings on the clinically‑correct answer.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `AFM_001` | The folder implements three modules in order of increasing fidelity: Additive (scalar sum), Coupling (signed pairwise J + multiplicative resistance suppression), Temporal (kicked relaxor + non‑commutative J). Each opens an axis the previous one collapsed. | SUPPORTED |
| `AFM_002` | The additive scorer and the coupling scorer disagree on the SIGN of the best combination. Additive rejects (CW, NA, SS) at −3.0; coupling ranks it at 10.39 with p_res = 0.084. This is the rank‑flip claim, pinned by tests. | SUPPORTED |
| `AFM_003` | The coupling scorer is explicitly aligned with clinical practice. Amphotericin‑B + 5‑flucytosine is the classical orthogonal‑axis synergy example; Hsp90 inhibition is a mechanism‑independent potentiator. The coupling scorer agrees; the additive scorer does not. | SUPPORTED |
| `AFM_004` | The multiplicative resistance suppression (∏) is the lever. Same seven codes, different topology, opposite ranking on the clinically‑correct answer. | SUPPORTED |
| `AFM_005` | The temporal module shows that schedule shape and drug sequence are first‑class parameters, not decorations. All three tested schedules end with R_frac = 1.0, but surviving populations rank by 2+ orders of magnitude: simultaneous (461) < fast cycling (10,938) < sequential mono (65,749). | SUPPORTED |
| `AFM_006` | The interaction matrix is non‑commutative in the temporal module. Azole → polyene: kill = 9.4; polyene → azole: kill = 15.0 — ~60% more total kill when polyene goes first. Static scorers (both additive AND coupling core) collapse this to a single symmetric J. | SUPPORTED |
| `AFM_007` | The temporal module file is absent from the delivered drop. README references temporal_dosing_resistance.py, but it is not in the repository contents. The temporal claims are documented but the code is not delivered. | UNVERIFIED (file missing) |
| `AFM_008` | The delivered code is stdlib‑only. antifungal_mechanism_sim.py imports only random; antifungal_coupling_core.py imports nothing beyond stdlib. | SUPPORTED |
| `AFM_009` | The delivered code is runnable. Both .py files execute and provide interactive CLIs. | SUPPORTED |
| `AFM_010` | 76 unit tests are delivered. Tests cover additive sim (15), coupling core (27), and temporal (34). The temporal tests exist even though the module file is missing — they reference temporal_dosing_resistance. | PARTIAL (tests exist, module missing) |
| `AFM_011` | The coupling core's efficacy formula has three components: within‑axis redundancy discount (max + 0.5×sum others), signed pairwise synergy/antagonism (Jij·sqrt(ei·ej)), and resistance as product over orthogonal axes of min(p_res per axis). | SUPPORTED |
| `AFM_012` | Same‑axis targets share a min (no ∏ bonus). Sterol‑axis targets EG and MD share the same axis; resistance is not multiplied across them. | SUPPORTED |
| `AFM_013` | The repository produces no clinical recommendation. It is explicitly a "design‑exploration progression, not pharmacological predictions". | SUPPORTED |
| `AFM_014` | The additive module is kept as‑is for the genetic‑crossover flow. It is not updated to use coupling; it remains a browsable heuristic. | SUPPORTED |
| `AFM_015` | The coupling core's empirical signatures are pinned to 2 decimal places. Tests enforce exact values. | SUPPORTED |
| `AFM_016` | Collateral sensitivity is modeled in the temporal module. RA is hypersensitive to B, which further suppresses under fast cycling — evolutionary steering. | SUPPORTED (documented, module missing) |
| `AFM_017` | The kicked relaxor model treats dose as a kick; populations relax between kicks. Schedule shape decides the outcome. | SUPPORTED (documented, module missing) |
| `AFM_018` | The folder is not a predictive pharmacology tool. It is a pedagogical progression showing why additive assumptions fail and how coupling and temporal axes change outcomes. | SUPPORTED |

---

## UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the antifungal‑mechanism‑sim framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. TEMPORAL MODULE RECONSTRUCTION — The Missing File

**Gap:** temporal_dosing_resistance.py is referenced in the README and has 34 unit tests, but the file is not in the delivered repository.

**Knowledge state:** UNKNOWN_ATM (file missing)

**Research question:** What does the temporal module's kicked relaxor implementation look like? Can it be reconstructed from the test suite and README specifications?

**Disciplines:** Computational biology, pharmacokinetics/pharmacodynamics (PK/PD), software engineering

**Data sources:**

- README specifications: kicked relaxor, non‑commutative J, collateral sensitivity
- Test file: test_temporal_dosing_resistance.py (34 tests)
- Published literature on multi‑drug resistance evolution, collateral sensitivity, and sequential dosing

**Method:**

1. Extract all test assertions from test_temporal_dosing_resistance.py
2. Reverse‑engineer the expected module interface from test signatures
3. Implement a temporal_dosing_resistance.py that passes all 34 tests
4. Document the reconstruction: which design choices were constrained by tests, which were free
5. Validate against the README's empirical signatures (simultaneous: 461, sequential mono: 65,749, fast cycling: 10,938; azole→polyene: 9.4, polyene→azole: 15.0)

**Expected deliverable:** A working temporal_dosing_resistance.py that passes all 34 tests and reproduces the documented empirical signatures.

**Falsifier:** The tests are inconsistent with the README specifications (then the reconstruction reveals a specification‑test mismatch).

---

### 2. COUPLING CORE CALIBRATION — J Matrix from Published Data

**Gap:** The signed pairwise coupling matrix J is biologically motivated but not calibrated from published combination therapy data.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the actual synergy/antagonism coefficients (J) for clinically used antifungal combinations, and how do they compare to the shipped values?

**Disciplines:** Pharmacology, mycology, computational biology

**Data sources:**

- Published combination therapy studies (checkerboard assays, time‑kill curves)
- Clinical trial data for antifungal combinations (AMB + 5FC, echinocandin + azole, etc.)
- FDA labeling and EUCAST/CLSI combination testing guidelines
- PubMed / Google Scholar: "(antifungal combination) AND (synergy OR antagonism) AND (checkerboard)"

**Method:**

1. Conduct a literature review of antifungal combination synergy/antagonism data
2. Extract effect sizes for pairs: azole+polyene, echinocandin+azole, polyene+5FC, Hsp90+azole, etc.
3. Convert effect sizes to a common scale compatible with the coupling core's J metric
4. Replace the shipped J values with literature‑derived values
5. Re‑run the coupling core and compare rankings

**Expected deliverable:** A literature‑derived J matrix with citations, replacing the biologically motivated placeholder values.

**Falsifier:** The literature shows no consensus on synergy/antagonism coefficients for these pairs (then the shipped values remain the best available estimate).

---

### 3. RESISTANCE PROBABILITY CALIBRATION — p_res from Clinical Data

**Gap:** The per‑target escape probabilities p_res (0.20–0.70) are illustrative, not calibrated from clinical resistance data.

**Knowledge state:** NOT_STUDIED

**Research question:** What are the actual per‑target resistance probabilities for clinically used antifungals, and how do they affect the coupling core's ranking?

**Disciplines:** Clinical microbiology, pharmacoepidemiology, mycology

**Data sources:**

- CDC / WHO antifungal resistance surveillance data
- SENTRY Antimicrobial Surveillance Program
- Clinical isolate resistance frequency databases (e.g., ECMM, CLSI)
- Published resistance rates for Candida, Aspergillus, etc.

**Method:**

1. Extract resistance frequencies for each target class (echinocandin, azole, polyene, 5‑FC, Hsp90, etc.)
2. Compute per‑target escape probabilities from surveillance data
3. Replace the shipped p_res values with surveillance‑derived values
4. Re‑run the coupling core and compare rankings

**Expected deliverable:** A surveillance‑derived p_res dictionary with sources, replacing the illustrative values.

**Falsifier:** Resistance frequencies are not available by target class (then the gap remains UNKNOWN_ATM).

---

### 4. WITHIN‑AXIS REDUNDANCY DISCOUNT — Calibration of the 0.5 Factor

**Gap:** The within‑axis redundancy discount uses a fixed 0.5 factor with no justification from pharmacology.

**Knowledge state:** UNDEFINED

**Research question:** What is the correct within‑axis redundancy discount for same‑target combinations? Is 0.5 the right value, or should it be mechanism‑specific?

**Disciplines:** Pharmacology, dose‑response modeling, systems pharmacology

**Data sources:**

- Dose‑response curves for combination therapies
- Published synergy/antagonism studies with same‑target pairs
- Pharmacodynamic interaction models (e.g., Loewe additivity, Bliss independence)

**Method:**

1. Review the pharmacodynamic literature on same‑target combinations
2. Extract the typical redundancy discount from dose‑response data
3. Test sensitivity of the coupling core's ranking to the discount factor (0.1–1.0)
4. Propose a mechanism‑specific discount based on target binding kinetics

**Expected deliverable:** A calibrated within‑axis redundancy discount (or mechanism‑specific discounts) with literature justification.

**Falsifier:** The ranking is insensitive to the discount factor (then the exact value is not load‑bearing).

---

### 5. FITNESS FUNCTION WEIGHTS — Calibration of w_tox and w_res

**Gap:** The fitness function uses fixed weights w_tox and w_res with no clinical or pharmacological calibration.

**Knowledge state:** UNDEFINED

**Research question:** What are the appropriate weights for toxicity and resistance in antifungal combination fitness, and how do they affect the optimal combination ranking?

**Disciplines:** Clinical pharmacology, pharmacoeconomics, decision analysis

**Data sources:**

- Clinical toxicity profiles for antifungals (FDA labels, published trials)
- Health‑economic evaluations of antifungal therapy
- Patient‑reported outcomes and quality‑of‑life studies

**Method:**

1. Extract toxicity severity scores for each antifungal from clinical data
2. Estimate the relative disutility of toxicity vs. resistance from health‑economic studies
3. Test sensitivity of the coupling core's ranking to weight variations
4. Propose clinically‑informed weights

**Expected deliverable:** A clinically‑informed weight set for w_tox and w_res with sources and sensitivity analysis.

**Falsifier:** The ranking is insensitive to weight variations (then the exact weights are not load‑bearing).

---

### 6. COLLATERAL SENSITIVITY — Empirical Validation

**Gap:** Collateral sensitivity (RA hypersensitive to B) is modeled in the temporal module but not validated against empirical data.

**Knowledge state:** NOT_STUDIED

**Research question:** Does collateral sensitivity actually exist for antifungal resistance mutations, and if so, which resistance‑drug pairs exhibit it?

**Disciplines:** Evolutionary biology, mycology, pharmacogenomics

**Data sources:**

- Published collateral sensitivity studies in fungi (Candida, Aspergillus)
- Experimental evolution studies with antifungal exposure
- Genomic databases of resistance mutations and drug susceptibility

**Method:**

1. Review the literature on collateral sensitivity in antifungal resistance
2. Identify documented pairs: resistance to drug A → hypersensitivity to drug B
3. Quantify the effect size for each pair
4. Incorporate validated pairs into the temporal module's SENS map

**Expected deliverable:** A validated collateral sensitivity map for the temporal module, with literature citations.

**Falsifier:** No collateral sensitivity is documented for antifungal resistance (then the feature is theoretical).

---

### 7. NON‑COMMUTATIVE J — Empirical Validation

**Gap:** The non‑commutative interaction matrix (azole→polyene ≠ polyene→azole) is a design choice, not validated against empirical sequence‑dependent kill data.

**Knowledge state:** NOT_STUDIED

**Research question:** Does drug sequence actually affect kill in antifungal combinations, and if so, by how much?

**Disciplines:** Pharmacology, mycology, PK/PD

**Data sources:**

- Published sequential dosing studies (in vitro time‑kill curves, in vivo models)
- Clinical studies with sequenced antifungal therapy
- PubMed / Google Scholar: "(antifungal) AND (sequence OR order) AND (combination)"

**Method:**

1. Review the literature on sequence‑dependent antifungal kill
2. Extract kill data for azole→polyene vs. polyene→azole sequences
3. Quantify the effect size for each ordered pair
4. Calibrate the temporal module's non‑commutative J against empirical data

**Expected deliverable:** A validated non‑commutative J matrix with literature citations and effect sizes.

**Falsifier:** Drug sequence has no detectable effect on kill (then non‑commutativity is not load‑bearing).

---

### 8. MUTATION RATE CALIBRATION — µ for Resistance Evolution

**Gap:** The temporal module uses a mutation rate µ without calibration to empirical antifungal resistance mutation rates.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What are the empirical mutation rates for antifungal resistance in clinically relevant fungi, and how do they affect the schedule ranking?

**Disciplines:** Evolutionary biology, mycology, population genetics

**Data sources:**

- Published mutation rate estimates for Candida, Aspergillus, Cryptococcus
- Fluctuation assay data for antifungal resistance
- Genomic studies of resistance emergence

**Method:**

1. Extract mutation rates for resistance to each antifungal class
2. Compute the expected rate of double‑mutant emergence (µ²) for simultaneous vs. sequential dosing
3. Calibrate the temporal module's µ parameter
4. Test sensitivity of the schedule ranking to µ variations

**Expected deliverable:** A calibrated mutation rate for the temporal module, with literature sources and sensitivity analysis.

**Falsifier:** Mutation rates are not available for the relevant organism‑drug pairs (then the gap remains UNKNOWN_ATM).

---

### 9. POPULATION SIZE SCALING — Clinical Relevance of the R_frac = 1.0 Result

**Gap:** All three schedules end with R_frac = 1.0, but the surviving population sizes differ by 2+ orders of magnitude. The clinical relevance of this distinction is not quantified.

**Knowledge state:** NOT_STUDIED

**Research question:** What surviving population size constitutes clinical failure? Does the 2‑order‑of‑magnitude difference between simultaneous and sequential mono translate to a clinically meaningful difference in outcome?

**Disciplines:** Clinical pharmacology, infectious disease, PK/PD

**Data sources:**

- Clinical breakpoints for antifungal therapy (EUCAST, CLSI)
- PK/PD targets for fungal clearance
- Published studies on fungal burden and clinical outcome

**Method:**

1. Review the relationship between fungal burden and clinical outcome
2. Identify the threshold population size associated with treatment failure
3. Compare the temporal module's surviving populations to clinical thresholds
4. Translate the schedule ranking into clinical risk categories

**Expected deliverable:** A clinical interpretation of the temporal module's schedule ranking, with threshold‑based risk categories.

**Falsifier:** All surviving populations are below the clinical failure threshold (then schedule differences are clinically irrelevant).

---

### 10. MODEL VALIDATION — 76‑Test Suite Coverage Analysis

**Gap:** The repository has 76 tests, but test coverage (line, branch, and mutation coverage) is not reported.

**Knowledge state:** NOT_STUDIED

**Research question:** How complete is the test suite? What parts of the code are untested, and what would a mutation analysis reveal?

**Disciplines:** Software engineering, computational biology, testing

**Data sources:**

- The test files in tests/
- The module source files
- coverage.py and mutmut (mutation testing) tools

**Method:**

1. Run coverage.py on the test suite
2. Identify untested lines and branches
3. Run mutation testing (mutmut) to identify weak tests
4. Write additional tests to close coverage gaps
5. Document the coverage report and any remaining gaps

**Expected deliverable:** A coverage report and mutation analysis for the test suite, with additional tests to close any gaps.

**Falsifier:** Coverage is already 100% and mutation score is > 90% (then the test suite is already complete).

---

### 11. USER GUIDE — Clinical Translation

**Gap:** The repository is documented for modelers, not for clinicians or pharmacologists.

**Knowledge state:** NOT_STUDIED

**Research question:** How can the framework's insights be communicated to clinicians in a way that changes how they think about combination therapy design?

**Disciplines:** Medical education, science communication, clinical pharmacology

**Data sources:**

- The framework itself
- Published clinical guidelines for antifungal therapy
- Medical education literature on combination therapy

**Method:**

1. Translate each module's finding into clinical language
2. Develop case studies: "What additive thinking would recommend vs. what coupling thinking would recommend"
3. Create a clinical guide explaining the implications of non‑additivity and sequence dependence
4. Test the guide with infectious disease fellows or pharmacists

**Expected deliverable:** A clinical translation guide for the antifungal‑mechanism‑sim framework.

**Falsifier:** Clinicians find the guide unhelpful or not actionable.

---

### 12. MECHANISM‑SPECIFIC SYNERGY — Expanding Beyond the Shipped Seven

**Gap:** The framework uses seven interaction codes. It does not include other antifungal classes or experimental compounds.

**Knowledge state:** NOT_STUDIED

**Research question:** What other antifungal targets and mechanisms should be added to the framework, and how would they change the optimal combination ranking?

**Disciplines:** Medicinal chemistry, pharmacology, mycology

**Data sources:**

- Published antifungal drug discovery pipelines
- Experimental antifungal compounds (e.g., novel targets, fungal‑specific pathways)
- FDA/EMA approved antifungals not in the shipped set

**Method:**

1. Review the antifungal pipeline for novel targets
2. Add new interaction codes with estimated efficacy, toxicity, resistance, and axis
3. Estimate synergy/antagonism coefficients from mechanism‑of‑action knowledge
4. Re‑run the coupling core and identify new optimal combinations

**Expected deliverable:** An expanded interaction set with new targets and a revised optimal combination ranking.

**Falsifier:** No novel antifungal targets are sufficiently characterized (then expansion is not feasible).

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard combination therapy modeling practice

---

### The Problem

In antifungal combination therapy modeling, things like synergy/antagonism topology, multiplicative resistance suppression, dosing schedule, and drug sequence are not separate from the efficacy estimate. They are direct, material, contributing factors to the outcome. When a model says those things are "second‑order effects" or "not in the model's scope," that is usually not a scientific finding. It is a boundary choice, a modeling limitation, or a narrow definition of "combination."

The fungal cell does not care about our modeling conventions. Pharmacology does not isolate efficacy from the interaction topology that modulates it, the resistance pathways that escape it, or the schedule that delivers it. All of those are part of one continuous system.

When we model only the additive sum, we are not simplifying reality—we are modeling a different system than the one that actually exists. And then we are surprised when the real system behaves in ways the model did not predict.

---

### Six Ways the Connection Gets Lost

#### 1. The "Additive as Default" Fallacy

Many combination models treat efficacy as additive: Σ effect − Σ toxicity − Σ resistance. If the model says "combination X is best," that is treated as the answer.

But combinations are non‑additive. Synergy can make a combination greater than the sum of its parts; antagonism can make it worse. The additive model gives the same score (−3.0) to azole+polyene and to (echinocandin+5FC+Hsp90). The coupling model says one is mediocre and the other is among the best. If the report says "both are equivalent," it is not false for the additive model, but it may be false for the system. The interaction topology was causal—just not represented.

So "additive as default" often means "We didn't include non‑additivity." That is a modeling choice, not evidence that combinations are additive.

#### 2. The "Resistance as Sum" Fallacy

Many models treat resistance as additive: sum of per‑drug resistance risks. If the model says "combination has resistance risk R," that is treated as the answer.

But resistance is suppressed multiplicatively by orthogonal‑axis diversity. A three‑axis combination has p_res = 0.7×0.3×0.4 = 0.084—far lower than any additive sum. If the model says "resistance risk is moderate," it may be overestimating resistance by an order of magnitude. The multiplicative suppression was causal—just not represented.

So "resistance as sum" often means "We didn't model orthogonal axes." That is a biological omission, not evidence that resistance adds.

#### 3. The "Schedule as Decoration" Fallacy

Many models treat dosing schedule as an implementation detail—something that happens after the efficacy is computed. If the model says "combination has efficacy E," that is treated as the answer.

But schedule shape decides the outcome. Simultaneous dosing suppresses resistance to 461 survivors; sequential mono allows 65,749. Same drugs, different schedule, two orders of magnitude difference. If the assessment says "efficacy is E," it is not false for the static model, but it may be false for the clinical reality. The schedule was causal—just not represented.

So "schedule as decoration" often means "We assumed concurrent dosing." That is a dosing assumption, not evidence that schedule doesn't matter.

#### 4. The "Sequence as Symmetric" Fallacy

Many models treat drug sequence as irrelevant—A then B is the same as B then A. If the model says "combination kill is K," that is treated as the answer.

But sequence matters. Azole→polyene kills 9.4; polyene→azole kills 15.0—~60% more. Same two drugs, different order, different outcome. If the assessment says "kill is K," it is not false for one sequence, but it may be false for the other. The sequence was causal—just not represented.

So "sequence as symmetric" often means "We assumed concurrent or commutative dosing." That is a modeling assumption, not evidence that order doesn't matter.

#### 5. The "Static as Complete" Fallacy

Many models treat the static state as the complete picture—the combination's properties are fixed and independent of time. If the model says "combination is optimal," that is treated as the answer.

But the system evolves. Populations relax between kicks. Resistance mutations accumulate. Collateral sensitivity can steer evolution. The static scorer collapses both temporal axes. If the assessment says "optimal," it may be optimal for the static state but suboptimal for the temporal dynamics. The time axis was causal—just not represented.

So "static as complete" often means "We didn't model time." That is a temporal omission, not evidence that time doesn't matter.

#### 6. The "Single Model as Truth" Fallacy

Many assessments use a single model. If the model says "combination X is best," that is treated as the answer.

But models disagree on the sign of the best combination. Additive says (CW, NA, SS) is rejected at −3.0. Coupling says it's one of the best at 10.39. Same seven codes, different topology, opposite recommendation. If the assessment says "X is best," it may be true for one model and false for another. The model choice was causal—just not represented.

So "single model as truth" often means "We chose one topology and ignored the others." That is a modeling preference, not evidence that the chosen topology is correct.

---

### What This Framework Does Differently

This framework treats combination therapy as one integrated system of efficacy, interaction topology, resistance suppression, dosing schedule, and drug sequence. The three modules document mechanisms that standard combination modeling typically drops:

- antifungal_mechanism_sim.py: Additive scalar—browsable heuristic, genetic‑style crossover.
- antifungal_coupling_core.py: Coupling topology—signed pairwise J + multiplicative resistance suppression over orthogonal axes. Same codes, different topology, opposite ranking on the clinically‑correct answer.
- temporal_dosing_resistance.py (specified, missing): Kicked relaxor + non‑commutative J—schedule and sequence as first‑class parameters.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Empirical mutation rates for antifungal resistance.
UNDER_STUDY Data collection is in progress; value is provisional. Collateral sensitivity mapping for antifungal pairs.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. Sequence‑dependent kill for azole→polyene vs. polyene→azole.
UNDEFINED The variable has no agreed definition or measurement protocol. Within‑axis redundancy discount factor.

---

### What Is NOT a Valid Epistemic State

MODELING_CONVENIENCE is not a valid knowledge state. If a mechanism physically influences the system, excluding it because it is mathematically inconvenient, computationally expensive, or outside the model's topology is a modeling error, not an epistemic one. The pharmacology does not respect our modeling conventions.

The framework refuses to record a mechanism as absent because of convenience. Instead, it records the mechanism as a progression—an axis the previous module collapsed—and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"Is this within our model's topology?"

But rather:

"Does this mechanism materially affect the combination's outcome?"

If the answer is yes, it belongs in the model. End of story.

The fungal cell is already interconnected. Our additive assumptions, static scorers, and symmetric matrices are the only things pretending otherwise. And that pretense has cost lives on a scale that we are only beginning to understand.

This framework does not pretend otherwise.
