**Format example.** [`RESEARCH_RENDER.md`](../RESEARCH_RENDER.md) names this
folder as one of its two worked instances. Read it for what the three
documents look like filled in — `CLAIM_TABLE.md`, `RESEARCH_GAPS.md`,
`SCOPE_BOUNDARY.md`, in that order below. What it says about reader spread
is the folder's own business and is argued there; what it shows a reader
looking for the schema is the shape.

---

## CLAIM_TABLE.md

Claims about the delivered divergence-playground/ folder, about what a Python stdlib environment can establish concerning it, and about the anti-anchoring protocol it inherits.

This is a structured-elicitation instrument, not a measurement of any real fork. The code runs end‑to‑end on a worked example. No LLM calls are made. No cryptographic seal is enforced. The XOR obfuscation in seal.py defends against accidental peeking, not determined attackers. The instrument's subject is the spread across readers — not the truth of any reading.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `DP_001` | The seal is load‑bearing. Without it you get anchoring, and the ensemble collapses into the first reading posted. The seal's purpose is to prevent any reader from seeing another reader's commitment before committing their own. | SUPPORTED |
| `DP_002` | The XOR obfuscation is not a cryptographic seal. It defends against accidental peeking, not against a determined attacker. The API stays the same if swapped for real crypto. | SUPPORTED |
| `DP_003` | Readings are structured, not scalar. Three axes: Verdict (categorical, cheapest), Mechanism (Jaccard on DAG edges), Collapse (operational, strongest). | SUPPORTED |
| `DP_004` | The interesting cell is same verdict, different collapse. Two readers agree by accident — reach the same conclusion via different routes. Variance would never catch this; spread.agreement_accident() flags it. | SUPPORTED |
| `DP_005` | C1–C4 are structured elicitation — the tool cannot infer the maps, trial counts, or tolerances. It refuses to certify a coincidence claim without them. | SUPPORTED |
| `DP_006` | C1 catches quantities related by a deterministic map. Example: rs_ratio = 0.9886 and E_ede_frac = 0.0114 are one number (A = 1 - B), not two. | SUPPORTED |
| `DP_007` | C2 catches the look‑elsewhere effect. p_eff = 1 - (1-p)^N — state N before claiming surprise. | SUPPORTED |
| `DP_008` | C3 catches post‑hoc tolerance windows. Fix the match window before looking; log the timestamp. | SUPPORTED |
| `DP_009` | C4 requires pre‑registration and a falsifiable prediction. The only kind of common cause worth having. | SUPPORTED |
| `DP_010` | The null ensemble is the only rigorous version. null_ensemble.null_hits() runs your search rule on synthetic nulls (shuffle labels, IID resample, or group permutation) and reports the empirical p — trials factor included by construction because you ran the search on the null. | SUPPORTED |
| `DP_011` | The worked example runs the full loop on FK-2. Three readers commit blind; verdict spread 0.33, mechanism spread 1.00, collapse spread 0.33 (strong axis). The verdict‑cluster does not match the collapse‑cluster — the axes measure different things. | SUPPORTED |
| `DP_012` | The run queue auto‑ranks the collapse condition two of three readers converged on. | SUPPORTED |
| `DP_013` | The energy/ audit harvested seven forks. FK-1 θ* engine split RESOLVED (DP-13). FK-2 generative CPL recovery RESOLVED (F2). FK-3 H0 orthogonality PARTIAL (DP-14 option, OB-8 rerun). FK-4 fs8 ≈ 8× ΛCDM OPEN. FK-5 α wall classification OPEN. FK-6 certificate validity r̂ RESOLVED (DP-17). FK-7 D as distance STAKED (DP-15 caveat). | SUPPORTED |
| `DP_014` | No LLM calls. Readers commit through Python API or CLI; the playground is what shows up when the humans and AIs have already written their answers. | SUPPORTED |
| `DP_015` | No storage of raw model output. Only structured Readings. Prose goes in the notes field. | SUPPORTED |
| `DP_016` | The delivered code is stdlib‑only. fork.py, reading.py, seal.py, spread.py, coincidence.py, null_ensemble.py import only from the Python standard library. | SUPPORTED |
| `DP_017` | The delivered code is runnable. The worked example in samples/worked_example.sample.txt runs the full loop. | SUPPORTED |
| `DP_018` | The repository produces no measurement of any real fork. It is an instrument, not a measurement. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the divergence‑playground framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. EMPIRICAL — Cryptographic Seal Replacement

**Gap:** The XOR obfuscation in seal.py defends against accidental peeking, not against a determined attacker. The README states that for adversarial multi‑agent settings, swap the XOR layer for real crypto; the commit/reveal API stays the same.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the correct cryptographic replacement for the XOR obfuscation? What are the trade‑offs between different schemes (e.g., public‑key encryption, commitment schemes, threshold signatures) in terms of security, performance, and ease of use?

**Disciplines:** Cryptography, security engineering, distributed systems

**Data sources:**

- Published cryptographic commitment schemes
- seal.py implementation and API
- NIST cryptographic standards

**Method:**

1. Review cryptographic commitment schemes suitable for anti‑anchoring
2. Implement a replacement for seal.py using a real cryptographic primitive (e.g., SHA‑256 commitment with nonce reveal, public‑key encryption)
3. Test the replacement against the existing API
4. Document the security properties and trade‑offs
5. Produce a migration guide

**Expected deliverable:** A seal_crypto.py replacement module with real cryptographic security, passing the same API tests as the XOR version.

**Falsifier:** The XOR obfuscation is sufficient for all use cases (then no replacement is needed).

---

### 2. EMPIRICAL — Fork Harvesting from Other Domains

**Gap:** The energy/ audit harvested seven forks. The playground can carry any project's own FORKS.jsonl. No forks have been harvested from other domains.

**Knowledge state:** NOT_STUDIED

**Research question:** What forks exist in other domains (e.g., climate, pharmacology, AI governance, bridge engineering)? Can they be harvested and run through the divergence‑playground?

**Disciplines:** Domain‑specific science (climate, pharmacology, etc.), research methodology, metascience

**Data sources:**

- Published papers with known interpretative forks
- The divergence‑playground FORKS schema
- The repositories already analyzed in this collection (Columbia, AMOC, antifungal, etc.)

**Method:**

1. Identify candidate forks from other domains
2. For each candidate, define the fork point (the raw data that admits more than one honest reading)
3. Write a FORKS.jsonl entry for each
4. Run the playground on the harvested forks
5. Document the spread patterns across domains

**Expected deliverable:** A FORKS.jsonl file with 5+ forks from other domains, and a cross‑domain spread analysis.

**Falsifier:** No forks exist in other domains (then the playground is domain‑specific).

---

### 3. EMPIRICAL — Null Ensemble Calibration

**Gap:** null_ensemble.null_hits() runs your search rule on synthetic nulls and reports the empirical p. The calibration of the null ensemble — how many shuffles, resamples, or permutations are needed for stable p‑values — is unspecified.

**Knowledge state:** UNDEFINED

**Research question:** What is the minimum number of null draws needed for stable empirical p‑values in the divergence‑playground? How does the required number vary with the complexity of the search rule?

**Disciplines:** Statistics, computational methods, resampling theory

**Data sources:**

- null_ensemble.py implementation
- Published literature on permutation tests and empirical p‑values
- The worked example and energy/ forks

**Method:**

1. Run the null ensemble with increasing numbers of draws (e.g., 100, 1,000, 10,000, 100,000)
2. Compute the variance of the empirical p‑value at each draw count
3. Identify the draw count at which variance stabilizes
4. Test sensitivity to search rule complexity
5. Document a calibration guideline

**Expected deliverable:** A calibration study for the null ensemble, with recommended draw counts and variance bounds.

**Falsifier:** The empirical p‑value is unstable even at very high draw counts (then the null ensemble is not reliable).

---

### 4. EMPIRICAL — Agreement‑by‑Accident Prevalence

**Gap:** spread.agreement_accident() flags same verdict, different collapse. The prevalence of agreement‑by‑accident in real forks is unknown.

**Knowledge state:** NOT_STUDIED

**Research question:** How often do readers agree on a verdict via different mechanisms or collapse conditions? What fraction of apparent consensus is actually agreement‑by‑accident?

**Disciplines:** Metascience, epistemology, research methodology

**Data sources:**

- The energy/ forks (FK‑1 through FK‑7)
- Forks harvested from other domains (Gap 2)
- The spread.py agreement‑accident detector

**Method:**

1. Run the divergence‑playground on all available forks
2. For each fork, compute the agreement‑by‑accident rate: fraction of reader pairs with same verdict but different collapse
3. Aggregate across forks and domains
4. Test whether agreement‑by‑accident correlates with fork complexity or domain
5. Document the prevalence and correlates

**Expected deliverable:** A prevalence estimate for agreement‑by‑accident across forks, with domain‑specific breakdowns.

**Falsifier:** Agreement‑by‑accident is rare (< 5%) in all forks (then the detector is not load‑bearing).

---

### 5. EMPIRICAL — C1‑C4 Elicitation Burden

**Gap:** C1–C4 require pre‑declared maps, trial counts, and tolerances. The burden of this structured elicitation — how much time and expertise it requires — is unmeasured.

**Knowledge state:** NOT_STUDIED

**Research question:** How much time and expertise does it take to complete C1–C4 for a typical fork? Is the structured elicitation feasible for non‑expert readers?

**Disciplines:** Human factors, research methodology, science communication

**Data sources:**

- The C1–C4 elicitation protocol
- Reader time logs from the energy/ forks
- Published usability testing methods

**Method:**

1. Design a C1–C4 elicitation session for a sample fork
2. Recruit readers with varying expertise levels
3. Measure completion time and error rates
4. Survey readers on perceived difficulty and clarity
5. Document the elicitation burden and feasibility

**Expected deliverable:** A usability study of C1–C4 elicitation, with time and error metrics by expertise level.

**Falsifier:** C1–C4 elicitation is infeasible for non‑expert readers (then the instrument is expert‑only).

---

### 6. EMPIRICAL — C4 Pre‑registration Compliance

**Gap:** C4 requires pre‑registration and a falsifiable prediction. The compliance rate with C4 in practice — how often readers actually pre‑register — is unknown.

**Knowledge state:** NOT_STUDIED

**Research question:** What fraction of readers comply with C4 pre‑registration? What barriers prevent compliance, and what interventions increase it?

**Disciplines:** Metascience, research methodology, behavioral economics

**Data sources:**

- The divergence‑playground deployment logs
- Published pre‑registration compliance studies
- Survey and interview data from readers

**Method:**

1. Deploy the divergence‑playground with C4 tracking
2. Measure the fraction of forks where C4 pre‑registration is completed
3. Survey readers on barriers to pre‑registration
4. Test interventions (e.g., reminders, simplified forms, incentives)
5. Document compliance rates and intervention effects

**Expected deliverable:** A C4 compliance study, with baseline rates and intervention effectiveness.

**Falsifier:** C4 compliance is > 90% (then pre‑registration is not a barrier).

---

### 7. EMPIRICAL — Fork Point Identification

**Gap:** The playground requires a fork point: "a place in a piece of work where the raw data admits more than one honest reading." The process of identifying fork points — and distinguishing them from mere uncertainty or disagreement — is underspecified.

**Knowledge state:** UNDEFINED

**Research question:** What are the operational criteria for identifying a fork point? How do you distinguish a genuine fork (data admits multiple honest readings) from a knowledge gap (data insufficient) or a disagreement (readers differ on interpretation)?

**Disciplines:** Epistemology, philosophy of science, research methodology

**Data sources:**

- The fork point definition in README.md
- Published literature on underdetermination and interpretive forks
- The energy/ forks as case studies

**Method:**

1. Develop operational criteria for fork point identification
2. Test the criteria against the energy/ forks
3. Apply the criteria to candidate forks from other domains
4. Validate against expert judgment
5. Document the criteria and validation

**Expected deliverable:** An operational guide for fork point identification, with case studies and validation.

**Falsifier:** Fork points cannot be identified reliably (then the playground's foundation is unsound).

---

### 8. EMPIRICAL — Mechanism DAG Equivalence

**Gap:** Mechanism comparison uses Jaccard on the DAG‑edge set. "Two readings using different notation for the same chain compare equal." The equivalence of different notations — when two DAGs express the same causal chain — is underspecified.

**Knowledge state:** UNDEFINED

**Research question:** When do two DAGs express the same causal chain despite different notation? What are the equivalence rules, and how should they be implemented?

**Disciplines:** Causal inference, graph theory, knowledge representation

**Data sources:**

- The mechanism DAG specification in reading.py
- Published literature on causal DAG equivalence (d‑separation, Markov equivalence)
- The energy/ forks as case studies

**Method:**

1. Define equivalence rules for causal DAGs (e.g., same d‑separation relations, same conditional independences)
2. Implement equivalence checking in the playground
3. Test against the energy/ forks
4. Validate against expert judgment
5. Document the equivalence rules and implementation

**Expected deliverable:** A mechanism DAG equivalence module for the divergence‑playground, with validation.

**Falsifier:** No two different notations express the same causal chain (then equivalence is not needed).

---

### 9. EMPIRICAL — Collapse Condition Operationalisation

**Gap:** The collapse condition is "the experiment that would resolve the fork." The operationalisation of collapse conditions — what counts as a resolvable experiment — is underspecified.

**Knowledge state:** UNDEFINED

**Research question:** What are the operational criteria for a collapse condition? What makes an experiment "resolvable" in practice?

**Disciplines:** Experimental design, philosophy of science, research methodology

**Data sources:**

- The collapse condition definition in reading.py
- Published literature on crucial experiments and resolvability
- The energy/ forks as case studies

**Method:**

1. Develop operational criteria for collapse conditions
2. Test the criteria against the energy/ forks
3. Apply the criteria to candidate forks from other domains
4. Validate against expert judgment
5. Document the criteria and validation

**Expected deliverable:** An operational guide for collapse condition specification, with case studies and validation.

**Falsifier:** Collapse conditions cannot be specified reliably (then the strong axis is not operational).

---

### 10. EMPIRICAL — Spread Metric Sensitivity

**Gap:** The three‑axis spread metric (verdict, mechanism, collapse) is defined, but its sensitivity — how it responds to different patterns of disagreement — is uncharacterised.

**Knowledge state:** NOT_STUDIED

**Research question:** How sensitive is the spread metric to different patterns of reader disagreement? Does it produce distinguishable signatures for different disagreement types?

**Disciplines:** Metrology, statistics, research methodology

**Data sources:**

- spread.py implementation
- Synthetic ensembles with known disagreement patterns
- The energy/ forks as case studies

**Method:**

1. Generate synthetic ensembles with known disagreement patterns (e.g., verdict only, mechanism only, collapse only, all three)
2. Compute the spread metric for each pattern
3. Test whether the metric produces distinguishable signatures
4. Test sensitivity to ensemble size and reader count
5. Document the sensitivity analysis

**Expected deliverable:** A sensitivity analysis for the spread metric, with signature patterns for different disagreement types.

**Falsifier:** The spread metric produces the same signature for all disagreement patterns (then it is not informative).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists (policymakers, journalists, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the divergence‑playground framework's insights be communicated to non‑specialists in a way that changes how they think about scientific disagreement and consensus?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Guidelines for communicating uncertainty and disagreement

**Method:**

1. Translate each concept into plain language with concrete examples
2. Develop case studies for each failure mode (anchoring, agreement‑by‑accident, look‑elsewhere)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the divergence‑playground framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard consensus and disagreement measurement practice

---

### The Problem

In scientific disagreement and consensus measurement, things like anchoring, agreement‑by‑accident, look‑elsewhere effects, and post‑hoc tolerance windows are not separate from the measurement of consensus. They are direct, material, contributing factors to whether the measured consensus is real. When a study says "the field agrees on X," that is treated as a finding about the science.

But the measurement may be contaminated by anchoring — the first reading posted sets the frame. The consensus may be agreement‑by‑accident — readers reach the same verdict via different mechanisms. The p‑value may be a look‑elsewhere effect — trials not counted. The tolerance may be post‑hoc — the match window fixed after seeing the data. All of these are invisible to standard consensus measures.

---

### Six Ways the Connection Gets Lost

#### 1. The "Consensus as Convergence" Fallacy

Many studies treat consensus as convergence — if readers agree, that is treated as evidence that the science is settled.

But readers may agree by accident — same verdict, different collapse. Variance would never catch this; spread.agreement_accident() flags it. If the study says "the field agrees," it is not false for the verdict, but it may be false for the mechanism. The agreement‑by‑accident was causal — just not represented.

So "consensus as convergence" often means "We measured verdict agreement and called it consensus." That is a measurement error, not evidence that the consensus is real.

#### 2. The "Anchoring as Neutral" Fallacy

Many studies treat the order of elicitation as neutral. If the first reading is posted, that is treated as just another data point.

But without a seal, you get anchoring, and the ensemble collapses into the first reading posted. The seal is load‑bearing. If the study says "the field consensus is X," it is not false for the elicited readings, but it may be false for the underlying disagreement. The anchoring was causal — just not represented.

So "anchoring as neutral" often means "We assumed the order doesn't matter." That is an elicitation error, not evidence that anchoring is absent.

#### 3. The "p‑value as Published" Fallacy

Many studies treat p‑values as published — if p < 0.05, that is treated as evidence.

But the look‑elsewhere effect: p_eff = 1 − (1−p)^N — state N before claiming surprise. If the study says "p < 0.05," it is not false for the single test, but it may be false for the family of tests. The trials factor was causal — just not represented.

So "p‑value as published" often means "We assumed N = 1." That is a statistical error, not evidence that the p‑value is valid.

#### 4. The "Tolerance as Fixed" Fallacy

Many studies treat tolerance windows as fixed. If the match is within the window, that is treated as evidence.

But C3 catches post‑hoc tolerance windows — fix the match window before looking; log the timestamp. If the study says "the match is within tolerance," it is not false for the window, but it may be false for the pre‑registration. The post‑hoc window was causal — just not represented.

So "tolerance as fixed" often means "We assumed the window was set beforehand." That is a methodological error, not evidence that the window was fixed.

#### 5. The "Common Cause as Correlational" Fallacy

Many studies treat correlation as evidence of common cause. If two results correlate, that is treated as evidence of a shared mechanism.

But C4 requires pre‑registration and a falsifiable prediction — the only kind of common cause worth having. If the study says "common cause," it is not false for the correlation, but it may be false for the mechanism. The post‑hoc inference was causal — just not represented.

So "common cause as correlational" often means "We assumed correlation implies shared mechanism." That is a causal error, not evidence that the common cause is real.

#### 6. The "Null as Optional" Fallacy

Many studies treat null ensembles as optional — nice to have but not required. If the study says "the result is significant," that is treated as sufficient.

But the null ensemble is the only rigorous version. null_ensemble.null_hits() runs your search rule on synthetic nulls and reports the empirical p — trials factor included by construction because you ran the search on the null. If the study says "significant," it is not false for the test, but it may be false for the null. The absent null was causal — just not represented.

So "null as optional" often means "We assumed the null is obvious." That is a statistical error, not evidence that the null is correctly specified.

---

### What This Framework Does Differently

This framework treats scientific disagreement and consensus as potentially contaminated by anchoring, agreement‑by‑accident, look‑elsewhere effects, post‑hoc tolerance, and absent nulls. The following components document mechanisms that standard consensus measurement practice typically drops:

- The load‑bearing seal: Without it you get anchoring, and the ensemble collapses into the first reading posted.
- Structured readings: Three axes — verdict, mechanism, collapse — each measuring a different dimension of disagreement.
- Agreement‑by‑accident detection: Same verdict, different collapse — variance would never catch this.
- C1–C4 structured elicitation: The tool cannot infer maps, trial counts, or tolerances. It refuses to certify a coincidence claim without them.
- The null ensemble: The only rigorous version. Empirical p, trials factor included by construction.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Cryptographic seal replacement, fork harvesting.
UNDEFINED The variable has no agreed definition or measurement protocol. Fork point identification, mechanism DAG equivalence.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Agreement‑by‑accident prevalence.
UNDER_STUDY Data collection is in progress; value is provisional. Null ensemble calibration.

---

### What Is NOT a Valid Epistemic State

CONSENSUS_AS_CONVERGENCE is not a valid knowledge state. If readers may agree by accident, treating verdict agreement as consensus is a measurement error, not an epistemic one. The disagreement does not care about our consensus measures.

The framework refuses to record verdict agreement as consensus. Instead, it records the structured spread — verdict, mechanism, collapse separately — and names what would be needed to move it to a settled state: a collapse condition the readers agree on.

---

### The Standard

The question should not be:

"Do the readers agree?"

But rather:

"Do they agree on the verdict, the mechanism, and the collapse condition — and if not, where does the disagreement lie?"

If the answer is that readers agree on the verdict but not the collapse, the consensus is agreement‑by‑accident. End of story.

The disagreement is already structured. Our consensus measures, p‑values, and tolerance windows are the only things pretending otherwise. And that pretense has produced a literature of apparent consensus that may be measuring anchoring, accident, or absence of nulls.

This framework does not pretend otherwise.
