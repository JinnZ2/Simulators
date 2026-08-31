---

## CLAIM_TABLE.md

Claims about the delivered instrument-bias-sims/ folder, about what a Python stdlib environment can establish concerning it, and about the self-audit protocol it inherits.

This is a marker collection, not a thesis. Nine sims plus one module set, from delivered work orders, each testing one way an instrument's own construction shapes what it reports. Nothing here is a position under defense, and the correct response to any of it is to test the fit, extend it, or report where it breaks.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `IBS_001` | S1: event-sampled observation reconstructs a false baseline—the distortion is a product of event triggering and cost weighting; neither alone. At low contested_fraction f, B reports a competitive system that is >95% null time. | SUPPORTED |
| `IBS_002` | S2: welfare-interview anchoring has no null case—the extra arms are not a robustness check, they are the second equation; one arm is underdetermined, not merely biased. A single downward-anchored arm has one observable and two unknowns. | SUPPORTED |
| `IBS_003` | S3: instrument error rate without settling what the property is—the rate is not computable; the false-null column varies 0.12–1.00, tracking permissiveness. Cases where an instrument correctly returned null and the property was never conceded are not in the list. | SUPPORTED |
| `IBS_004` | S4: competition vs motor learning—patched. Pre‑patch, rank_prospect was hardcoded {1: 0.25, 2: 0.60, 3: 0.85}—derived from the antler‑rank model, so model A was fitted to its own conclusion. | REPAIRED |
| `IBS_005` | S4's B3 is not identified by the stated test—arm_size carries a free selectivity exponent and reaches the observed young‑buck paternity share at k ≈ 2. The second observable that would identify it: paternity against antler size within an age class. | SUPPORTED |
| `IBS_006` | S5: collective computation requiring competing agents—the criterion is not empty; it is a prediction, and the case it excluded is the case that tests it. Both hand‑built models fit the same data; what is not cheap is enumerating what would separate them. | SUPPORTED |
| `IBS_007` | S6: trained responses are terminal, not wrong—spread = max − min is a range; adding difficulty levels makes it worse, not better. The diagnostic's null test: known‑filter arm must return FILTER; known‑tracker arm must return TRACKING. | SUPPORTED |
| `IBS_008` | S7: unanchored thresholds slide to the labeller's baseline—observer‑dependence is near‑analytic; the cost readout is a consequence of a stipulation. Identical conditions take different labels from different observers without the condition changing. | SUPPORTED |
| `IBS_009` | S8: time as an excuse vs time as a variable—normalisers agree on the sign and disagree 4286× about what would count as parity. The choice of normaliser decides the answer. | SUPPORTED |
| `IBS_010` | S9: corpus position filter—the spec's reason is the two marginals; coupling drives the conjunction's excess above 1.0, so the multiplicative reading overstates suppression by up to 1.85×. | SUPPORTED |
| `IBS_011` | S9, second‑order: content was expected to take over as surface mix rose. It never does—a relevance score defined as closeness to the corpus mean is a typicality measure, so the content correlation stays under 0.2 at every mix. | SUPPORTED |
| `IBS_012` | **S10/M4: the readout compared r |  |
| `IBS_013` | The excluded_subject pattern—a sim built to measure how a position is excluded turns out to have no representation for the position it is about; not a wrong value, no slot. S4 (doe), S9 (filtering agent), S10 (untenured continuous observer), S10/M4 (position high on both generation and writing). | SUPPORTED |
| `IBS_014` | A declared blank is a disclosure; an unreachable agent is the failure. S9's blank is correct and is its point; S10's is a limit on what the module set can say. | SUPPORTED |
| `IBS_015` | The structural rule—AGENTS section comes first, before any equations, and a missing agent must be a visible [BLANK]—was adopted from the S4 patch and is now enforced. agent_table() now renders blanks; PRE_PATCH_OMISSION records the state before rather than quietly fixing it. | SUPPORTED |
| `IBS_016` | Cross‑cutting rules are enforced—five rules over fifteen modules: no moral labels, no intent attribution, confidence separate, README states "marker", signed correlation comparisons. Rule 5 (no abs() on correlations) was earned from S10/M4 and immediately found a second instance in S9. | SUPPORTED |
| `IBS_017` | The cross‑cutting scan is a floor, not a certificate—a keyword scan can be stepped around by any paraphrase, so a PASS on rules 1 and 2 means "no listed token was found", not "the rule holds". | SUPPORTED |
| `IBS_018` | No module reads real data—S3's grid is hand‑coded judgement, S6 has no corpus, S7's cost table is stipulated, S8's present‑day interval is a placeholder. | SUPPORTED |
| `IBS_019` | The delivered code is stdlib‑only—all modules import only from the Python standard library. | SUPPORTED |
| `IBS_020` | The delivered code is runnable—every module exposes report(), confidence(), breaks() and --selftest. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the instrument‑bias‑sims framework, organized by discipline

---

### 1. EMPIRICAL — S4: Doe‑Choice Arm Identification

**Gap:** S4's B3 is not identified by the stated test. arm_size carries a free selectivity exponent and reaches the observed young‑buck paternity share at k ≈ 2.

**Knowledge state:** UNDEFINED

**Research question:** What is the correct test for identifying whether a doe's choice follows a motor‑learning model or a competition model? The second observable that would identify it: paternity against antler size within an age class.

**Disciplines:** Behavioural ecology, evolutionary biology, statistical modelling

**Data sources:**

- Cervid behavioural ecology literature
- Paternity data from wild populations
- Antler growth and age‑class data

**Method:**

1. Identify a dataset with paternity, antler size, and age class
2. Fit both models (motor‑learning vs. competition) to the data
3. Compare the models' predictions for paternity against antler size within age class
4. Test which model better fits the data
5. Document the separator

**Expected deliverable:** A statistical test for separating motor‑learning from competition models using within‑age‑class paternity data.

**Falsifier:** Both models produce identical predictions for the within‑age‑class relationship (then the separator is not informative).

---

### 2. EMPIRICAL — S6: Foreclosure Diagnostic with Real Data

**Gap:** S6 has no corpus and does not implement the classification step that is its whole instrument. The diagnostic has never been run on anything.

**Knowledge state:** NOT_STUDIED

**Research question:** Does the foreclosure diagnostic (filter vs. tracker) actually separate real responses? What is the smallest number of question‑difficulty levels and samples at which the two are separable?

**Disciplines:** Computational linguistics, psychometrics, AI safety

**Data sources:**

- LLM response datasets with known hedging patterns
- Human‑rated response datasets
- The S6 harness and synthetic generators

**Method:**

1. Collect or identify a dataset of responses with known hedging behaviour
2. Run the S6 diagnostic on the dataset
3. Test whether the diagnostic separates known filters from known trackers
4. Measure the minimum sample size for reliable separation
5. Document the diagnostic's real‑world performance

**Expected deliverable:** A validation of the foreclosure diagnostic on real data, with sample‑size recommendations.

**Falsifier:** The diagnostic does not separate real filters from trackers (then the diagnostic is not load‑bearing).

---

### 3. EMPIRICAL — S7: Cost Asymmetry Calibration

**Gap:** S7's cost table is stipulated. The cost asymmetry—whether a label carries an implied obligation—is recorded as a number attached to the condition‑observer pair, but the numbers are stipulated.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What are the actual cost asymmetries in real labelling contexts? How much does an "attaches" label cost the labeller, and how does this vary by condition and observer baseline?

**Disciplines:** Sociology, economics, public policy

**Data sources:**

- Labelling and classification studies
- Administrative burden research
- Implementation science literature

**Method:**

1. Identify real labelling contexts where a label carries an implied obligation
2. Measure the cost (time, resources, institutional friction) of attaching the label
3. Compare costs across conditions and observer baselines
4. Calibrate the S7 cost table with empirical data
5. Document the calibration and any surprises

**Expected deliverable:** An empirically calibrated cost table for S7, replacing the stipulated values.

**Falsifier:** The cost asymmetry is negligible in all contexts (then S7's mechanism is not load‑bearing).

---

### 4. EMPIRICAL — S8: Normaliser Calibration

**Gap:** S8's present‑day interval is a declared placeholder. The normalisers are plausible but not verified.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What are the actual present‑day intervals from problem documentation to delivered relief? Are the three normalisers (comms only, comms + disbursement, raw) defensible, and what is the true normaliser?

**Disciplines:** Public administration, emergency management, historical analysis

**Data sources:**

- Government relief program timelines
- Disaster response records
- Historical administration data

**Method:**

1. Collect actual present‑day interval data for relief delivery
2. Measure the three normaliser components (communication speed, disbursement speed, raw interval)
3. Test which normaliser best predicts observed delivery times
4. Compare to the historical intervals (New Deal, rural electrification)
5. Document the findings and any implications for the 4286× disagreement

**Expected deliverable:** An empirically calibrated set of intervals and normalisers for S8.

**Falsifier:** The present‑day interval is shorter than the historical interval under all normalisers (then the S8 finding is reversed).

---

### 5. EMPIRICAL — S10: Per‑Link Attribution Sensitivity

**Gap:** The residual is 79% of the total effect, and a per‑link table cannot hold the cross‑term. Leave‑one‑in, leave‑one‑out, and Shapley give different per‑link numbers.

**Knowledge state:** UNDEFINED

**Research question:** Which decomposition method (leave‑one‑in, leave‑one‑out, Shapley) is most appropriate for this model? Does the qualitative finding (residual > any single link) hold across all methods?

**Disciplines:** Causal inference, computational social science, model interpretation

**Data sources:**

- The allocation_coupling module set
- Published literature on model decomposition methods

**Method:**

1. Implement all three decomposition methods on the same model
2. Compare the per‑link attributions from each method
3. Test whether the residual > any single link finding holds across methods
4. Document the sensitivity of the finding to method choice
5. Recommend a method and justify it

**Expected deliverable:** A sensitivity analysis of per‑link attribution methods for S10, with a recommendation.

**Falsifier:** The residual < any single link under some decomposition method (then the finding is method‑dependent).

---

### 6. EMPIRICAL — The Excluded Subject Pattern Across Domains

**Gap:** The excluded subject pattern is documented in four instances within this folder. The pattern's prevalence across other domains (and other folders in this collection) is unknown.

**Knowledge state:** NOT_STUDIED

**Research question:** How often does the excluded subject pattern occur in other domains? Is it a general feature of instrument design, or specific to these sims?

**Disciplines:** Metrology, philosophy of science, research methodology

**Data sources:**

- The other folders in this collection
- Published critiques of instrument design
- The excluded_subject.py module itself

**Method:**

1. Survey the other folders in the collection for excluded subject instances
2. For each instance, record: missing agent, subject of the sim, whether it's a declared blank or an absence
3. Compute the prevalence of the pattern
4. Test whether the pattern correlates with domain or instrument type
5. Document the findings

**Expected deliverable:** A cross‑domain prevalence study of the excluded subject pattern.

**Falsifier:** The pattern is unique to this folder (then it is not a general feature).

---

### 7. METHODOLOGICAL — The [BLANK] Rule Effectiveness

**Gap:** The structural rule—AGENTS section first, missing agent as [BLANK]—was adopted from the S4 patch. Its effectiveness at preventing omissions has not been measured.

**Knowledge state:** NOT_STUDIED

**Research question:** Does the [BLANK] rule actually prevent omissions? How many omissions would have been invisible without the rule, and how many are caught by it?

**Disciplines:** Software engineering, research methodology, epistemology

**Data sources:**

- The pre‑patch and post‑patch versions of S4
- Other modules that declare AGENTS
- The excluded_subject.py audit

**Method:**

1. Compare the pre‑patch and post‑patch versions of S4
2. Audit other modules for omissions that would have been invisible without the rule
3. Measure the rule's effectiveness at catching omissions
4. Test whether the rule changes how modules are designed
5. Document the findings

**Expected deliverable:** An effectiveness study of the [BLANK] rule, with quantitative measures.

**Falsifier:** No omissions would have been invisible without the rule (then the rule is not needed).

---

### 8. EMPIRICAL — Cross‑Cutting Rule Compliance

**Gap:** The cross‑cutting rules are enforced by scan, but a keyword scan can be stepped around by any paraphrase. The actual compliance rate with the spirit of the rules (not just the tokens) is unknown.

**Knowledge state:** UNDER_STUDY

**Research question:** What is the actual compliance rate with the cross‑cutting rules (no moral labels, no intent attribution) when measured by human judgment rather than keyword scan?

**Disciplines:** Software engineering, ethics, research methodology

**Data sources:**

- The 15 modules scanned by crosscutting.py
- Human annotators
- The cross‑cutting rules themselves

**Method:**

1. Have human annotators review each module for moral labels and intent attribution
2. Compare human judgments to the keyword scan results
3. Measure the false negative rate (paraphrases that evade the scan)
4. Measure the false positive rate (tokens that are not actually moral/intent labels)
5. Document the findings and recommend improvements

**Expected deliverable:** A compliance study of the cross‑cutting rules, with human‑judgment baselines.

**Falsifier:** The keyword scan has zero false negatives (then paraphrases are not a problem).

---

### 9. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists (instrument designers, policymakers, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the instrument‑bias‑sims framework's insights be communicated to non‑specialists in a way that changes how they think about instrument design and measurement?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Guidelines for communicating measurement uncertainty

**Method:**

1. Translate each module's finding into plain language with concrete examples
2. Develop case studies for each failure mode (event sampling, anchoring, excluded subject, etc.)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the instrument‑bias‑sims framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard instrument‑bias practice

---

### The Problem

In instrument design and measurement, things like the denominator, the anchor, the rubric, the excluded subject, and the normaliser are not separate from the measurement. They are direct, material, contributing factors to what the instrument reports. When a study says "the instrument measures X," that is treated as a finding about the system.

But the instrument's own construction determines what it can report—and the difference between two defensible instrument designs can be 4286×. The instrument is not neutral. It is a filter that selects what it can see and excludes what it cannot.

---

### Six Ways the Connection Gets Lost

#### 1. The "Denominator as Given" Fallacy

Many instruments treat the denominator as given—the population, the sample frame, the set of cases. If the instrument says "the rate is X," that is treated as a finding.

But S1 shows that event‑sampled observation reconstructs a false baseline. A pure event trigger excludes NULL by definition. If the instrument says "the rate is X," it is not false for the sampled events, but it may be false for the system. The denominator was causal—just not represented.

#### 2. The "Anchor as Neutral" Fallacy

Many instruments treat the anchor as neutral—a harmless starting point. If the instrument says "the estimate is X," that is treated as a finding.

But S2 shows that one arm cannot separate the two models. A single downward‑anchored arm has one observable and two unknowns. If the instrument says "the estimate is X," it is not false for the observation, but it may be false for the latent value. The anchor was causal—just not represented.

#### 3. The "Rubric as Fixed" Fallacy

Many instruments treat the rubric as fixed—a stable standard for judgment. If the instrument says "the property is X," that is treated as a finding.

But S3 shows that the false‑null column varies 0.12–1.00, tracking how readily an instrument grants. If the instrument says "the property is X," it is not false for the rubric, but it may be false for the property. The rubric was causal—just not represented.

#### 4. The "Agent as Complete" Fallacy

Many instruments treat the agent set as complete—all relevant parties are represented. If the instrument says "the system is X," that is treated as a finding.

But the excluded subject pattern shows that a sim built to measure how a position is excluded turns out to have no representation for the position it is about. If the instrument says "the system is X," it is not false for the represented agents, but it may be false for the system. The excluded subject was causal—just not represented.

#### 5. The "Normaliser as Neutral" Fallacy

Many instruments treat the normaliser as neutral—a harmless scaling factor. If the instrument says "the interval is X," that is treated as a finding.

But S8 shows that normalisers agree on the sign and disagree 4286× about what would count as parity. If the instrument says "the interval is X," it is not false for the raw data, but it may be false for the comparison. The normaliser was causal—just not represented.

#### 6. The "Correlation as Causal" Fallacy

Many instruments treat correlation as causal—if two things correlate, one causes the other. If the instrument says "X tracks Y," that is treated as a finding.

But S10/M4 shows that a readout compared |r| only and reported "tracks generated observations" for a correlation of −0.85. The sign was the finding and the magnitude comparison lost it. If the instrument says "X tracks Y," it is not false for the magnitude, but it may be false for the direction. The sign was causal—just not represented.

---

### What This Framework Does Differently

This framework treats instruments as potentially biased by their own construction—event sampling, anchoring, rubric, excluded subjects, normalisers, and sign conventions. The following components document mechanisms that standard instrument‑bias practice typically drops:

- Nine modules—each testing one way an instrument's own construction shapes what it reports.
- The structural rule—AGENTS section first, missing agent as [BLANK].
- The excluded subject audit—four instances of the same shape, documented separately.
- Cross‑cutting rules—five rules enforced over fifteen modules.
- The 4286× finding—normalisers agree on the sign and disagree about where the sign flips.
- The 79% residual—per‑link attribution cannot hold the cross‑term.

---

### The Knowledge‑State Vocabulary

State Meaning Example
REPAIRED A defect was found and fixed S4's hardcoded rank_prospect
SUPPORTED The claim holds as stated S1–S3, S5–S9, S10 main result
NOT_STUDIED The mechanism is recognised, but no measurement has been attempted S6 with real data
UNKNOWN_ATM The mechanism is known to exist, but no current value is available S7 cost asymmetry, S8 present‑day interval
UNDEFINED The variable has no agreed definition or measurement protocol S4 doe‑choice identification, S10 decomposition method

---

### What Is NOT a Valid Epistemic State

INSTRUMENT_AS_NEUTRAL is not a valid epistemic state. If an instrument's construction determines what it can report, treating it as neutral is a measurement error, not an epistemic one. The system does not care about our instrument designs.

The framework refuses to record an instrument as neutral. Instead, it records the instrument as biased—by its denominator, its anchor, its rubric, its excluded subjects, its normalisers, or its sign convention—and names what would be needed to move it to a calibrated state.

---

### The Standard

The question should not be:

"What does the instrument report?"

But rather:

"How does the instrument's own construction shape what it reports—and what has it excluded?"

If the answer is that the instrument's construction shapes the report, the report is not a measurement of the system; it is a measurement of the instrument. End of story.

This framework does not pretend otherwise.
