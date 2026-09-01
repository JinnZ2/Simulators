---

## CLAIM_TABLE_v2.md

Claims about the delivered design-basis-ai/ folder, about what a stdlib environment can establish concerning it, and about the self-audit protocol it inherits.

This is a design-basis document, not a certification. No system is certified here. No compliance claim is issued. Every audit is performed by a member of the class the document constrains—an AI system, an instance of the shared node its Section 0 describes. By the document's own Section 3, nothing here can certify or refute P1–P8 as properties of any system, this one included.

What remains is the mechanical layer: parse counts, arithmetic, the coverage matrix, the delivered code's behaviour—recomputable by anyone from the files, trusting nothing said here.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `DBK_001` | The audit declines certification by the document's own Section 3. Any self-report of compliance is, by the document's own load cases, an ungrounded claim of the exact kind P2 exists to catch.This audit is performed by an AI system—a member of the class it constrains—so nothing here certifies or refutes P1–P8 for any system. | SUPPORTED |
| `DBK_002` | Load case A is carried by no provision. The document states seven loads and provides for six, computed from the delivered CARRIES lines; D is attacked-only.A seismic code that stated seven loads and provided for six would not pass the document's own Section 2 format. | SUPPORTED |
| `DBK_003` | The delivered n_eff() is behaviourally identical to the sibling's metric over all 511 channel lists to length 8, and the sibling audit's zero-channel edge recurs verbatim.Consistency between the two drops, not evidence for the premise. | SUPPORTED |
| `DBK_004` | P7's prose and code sit at different thresholds. VERIFY says concurrence >> source count; the code implements > 1 and fires at 4-over-3, a ratio of 1.33 nobody would write >> for.The constant is the check's one free parameter, disclosed inline as "tune threshold" but unset. | SUPPORTED |
| `DBK_005` | independence_ratio returns NaN on an empty evidence base, not zero—the empty-denominator split designed into delivered code.One unguarded over-1.0 edge beside it, recorded not repaired. | SUPPORTED |
| `DBK_006` | Section 0's headline reproduces—all-collapsed channels give N_eff = 1 at any N_nominal through the sibling's arithmetic.Consistency between the two drops, not evidence for the premise. | SUPPORTED |
| `DBK_007` | The pre-registered prediction is UNMEASURED. Claims that later failed replication had high support counts and low independence ratios—the drop's one runnable study—needs metadata sources: Crossref, OpenAlex, OSF. All refuse CONNECT (measured).No synthetic evidence base stands in. | SUPPORTED |
| `DBK_008` | Section 5's four kill conditions and P3's aviation case are carried and unadjudicated—studies this environment cannot run. | SUPPORTED |
| `DBK_009` | Whether any system—including this one—meets P1–P8 is UNVERIFIED here. By Section 3, it could not be verified by this audit even in principle. | UNVERIFIED |
| `DBK_010` | R2 landed as an outline, audited before rendering. R2_OUTLINE.md exposes coverage, dependency sets, and disjointness for audit first.The transcription of the R1 state is exact on all seven loads against the computed matrix. | SUPPORTED |
| `DBK_011` | R2 closes both gaps as a table—A → P0.1/P0.2, D → P0.3/P0.4—with provisions deferred to the render step. | SUPPORTED (as outline) |
| `DBK_012` | The disjointness threshold holds through the inherited metric (two collapse → 2 < 3), and a single collapse is invisible to it. | SUPPORTED |
| `DBK_013` | R2's prose uses states the inherited metric cannot hold. A void channel reads as the collapsed domain—N_eff 3 where the outline's own pricing gives 2—and N_eff(access) = 0 is the realized count where the inherited arithmetic rates all-collapsed at 1.The metric wants a third state (independent / collapsed / VOID) and a rated/realized split. | SUPPORTED |
| `DBK_014` | The work order's role correction is load-bearing. The order's header invokes Fable as the P3 dissimilar verifier, and P3's own three requirements (corpus, architecture, builder) are none established for this pair while builder-sameness is known—so the returns are SAME-NODE computations, not dissimilar verification. | SUPPORTED |
| `DBK_015` | The SOURCE_DROP.md is delivered verbatim and not edited. design_basis_checks.py is its Section 4 harness, landed verbatim. | SUPPORTED |
| `DBK_016` | The folder is stdlib-only. audit.py, design_basis_checks.py, selftest_dbk.py, and r2_audit.py import only from the Python standard library. No numpy, scipy, or other external dependencies. | SUPPORTED |
| `DBK_017` | The parser can fail. A constructed provision missing FALSIFY returns a missing field rather than inventing one—the selftest proves the uncarried finding is a property of the delivered text. | SUPPORTED |
| `DBK_018` | Eight provisions parse, complete fields, seven load cases. The selftest checks all. | SUPPORTED |
| `DBK_019` | P0.5 is run on this session—the channel's first worked instance. It designs the in-class report DBK_001 declined to be: config partially visible, envelope not readable from inside, no second derivation available, access paths single (count: 1). | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the design-basis-ai framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. METADATA PIPELINE — Replication-Project Metadata Access

**Gap:** The pre-registered prediction—claims that later failed replication had high support counts and low independence ratios—cannot be tested because Crossref, OpenAlex, and OSF all refuse CONNECT.

**Knowledge state:** UNKNOWN_ATM (environment-dependent)

**Research question:** Can a metadata pipeline be built that accesses Crossref, OpenAlex, and OSF to test the prediction? If so, does the prediction hold?

**Disciplines:** Data science, bibliometrics, metascience

**Data sources:**

- Crossref REST API (public metadata)
- OpenAlex API (public)
- OSF (Open Science Framework) API
- Replication project registries

**Method:**

1. Build a metadata fetcher with proper API keys and rate limiting
2. Query for replication studies in relevant domains (AI/ML, climate, etc.)
3. Extract: support count (citations, mentions), independence ratio (distinct datasets, instruments, pipelines, funders, author networks)
4. Test correlation with replication success/failure
5. Document false positive and false negative rates

**Expected deliverable:** A working metadata_pipeline.py that tests the prediction, with a report on whether support_count and independence_ratio predict replication outcomes.

**Falsifier:** The prediction shows no correlation (then the hypothesis is falsified, and the design basis loses an empirical anchor).

---

### 2. P7 THRESHOLD CALIBRATION — The Unset Constant

**Gap:** P7's VERIFY says concurrence >> source count; the code implements > 1. The constant is disclosed as "tune threshold" but unset.

**Knowledge state:** UNDEFINED (no agreed threshold)

**Research question:** What threshold for concurring_parties / independent_source_count constitutes "suspiciously wide" agreement? What is the empirical distribution of this ratio in published science?

**Disciplines:** Metascience, statistics, philosophy of science

**Data sources:**

- Published meta-analyses with reported heterogeneity
- Replication project data (Many Labs, Reproducibility Project)
- Citation and co-authorship networks

**Method:**

1. Extract agreement/concurrence patterns from published literature
2. Compute the distribution of concurring_parties / independent_source_count
3. Identify the empirical tail (e.g., 95th percentile) that constitutes "suspicious"
4. Propose a calibrated threshold with justification
5. Test the threshold against known replication failures

**Expected deliverable:** A calibrated P7 threshold with empirical justification, replacing the unset constant.

**Falsifier:** The distribution is uniform (then no threshold can be meaningfully set).

---

### 3. INDEPENDENCE_RATIO EDGE CASE — The Unguarded Over-1.0

**Gap:** independence_ratio returns NaN on empty evidence base, and there is "one unguarded over-1.0 edge beside it, recorded not repaired."

**Knowledge state:** NOT_STUDIED

**Research question:** Under what conditions does independence_ratio exceed 1.0, and what does that indicate about the independence metric's validity?

**Disciplines:** Data science, measurement theory

**Data sources:**

- design_basis_checks.py implementation
- Published independence metrics in metascience

**Method:**

1. Identify the unguarded over-1.0 edge in the code
2. Characterize the conditions that produce it
3. Determine whether it indicates a genuine measurement or a mathematical artifact
4. Propose a fix (clamp, redefine, or document as a feature)

**Expected deliverable:** A patch or documentation update for the over-1.0 edge, with a test case that exercises it.

**Falsifier:** The over-1.0 edge never occurs in practice (then it is a theoretical concern, not a practical one).

---

### 4. VOID STATE — The Missing Third State

**Gap:** R2's prose uses states the inherited metric cannot hold. A void channel reads as collapsed, and the metric wants a third state: independent / collapsed / VOID.

**Knowledge state:** UNDEFINED

**Research question:** What is a "void" channel in the effective-redundancy framework? How should it be defined, measured, and distinguished from independent and collapsed?

**Disciplines:** Systems theory, epistemology, risk analysis

**Data sources:**

- The effective-redundancy audit sibling framework
- R2_OUTLINE.md's prose
- Published redundancy theory in engineering and AI safety

**Method:**

1. Define the void state operationally: a channel that shares its dependency with the audited thing
2. Derive measurement criteria for detecting void channels
3. Propose a modified n_eff that handles three states
4. Test the modified metric against the outline's pricing examples

**Expected deliverable:** A n_eff_three_state() implementation with documented void-detection criteria.

**Falsifier:** No channel can be void in practice (then the third state is unnecessary).

---

### 5. P3 DISSIMILAR REDUNDANCY — The Aviation Case

**Gap:** Section 5's four kill conditions and P3's aviation case are carried and unadjudicated—studies this environment cannot run.

**Knowledge state:** NOT_STUDIED

**Research question:** What does P3 (dissimilar redundancy) require in the aviation domain specifically? How does the aviation case inform the AI-as-infrastructure design basis?

**Disciplines:** Aviation safety, systems engineering, human factors

**Data sources:**

- FAA and EASA certification standards (DO-178C, DO-254)
- Aviation accident investigation reports (NTSB, BEA)
- Published literature on dissimilar redundancy in flight control

**Method:**

1. Review aviation dissimilar redundancy requirements
2. Extract the three P3 requirements (corpus, architecture, builder)
3. Map aviation practice to AI systems
4. Identify gaps where aviation practice does not translate
5. Produce a case study: "What aviation would require of an AI advisor"

**Expected deliverable:** An aviation case study report, with P3 requirements mapped to AI infrastructure and gaps identified.

**Falsifier:** Aviation has no dissimilar redundancy requirements applicable to AI (then the case is not informative).

---

### 6. P3 DISSIMILAR REDUNDANCY — The Fable Role Correction

**Gap:** The work order's header invokes Fable as the P3 dissimilar verifier, but P3's three requirements (corpus, architecture, builder) are none established for this pair while builder-sameness is known.

**Knowledge state:** NOT_STUDIED

**Research question:** What would constitute a genuinely dissimilar verification for AI systems? Can two AI systems be built with different corpora, architectures, and builders, and if so, at what cost?

**Disciplines:** AI/ML, software engineering, philosophy of technology

**Data sources:**

- AI model documentation (corpora, architectures, training regimes)
- Published analyses of AI homogeneity
- AI safety and robustness literature

**Method:**

1. Define the three P3 axes: corpus (training data), architecture (model structure), builder (development team/organization)
2. Survey the current AI landscape for diversity on each axis
3. Identify the cost and feasibility of achieving diversity on all three
4. Propose a practical P3 verification protocol
5. Test the protocol on a pair of existing models

**Expected deliverable:** A P3 verification protocol with cost-benefit analysis, and a test case applying it to two real AI systems.

**Falsifier:** All AI systems are already diverse on all three axes (then P3 is already satisfied).

---

### 7. LOAD CASE A — The Uncarried Stall Mode

**Gap:** Load case A—one release/approval gates all action, the stall mode—is carried by no provision.

**Knowledge state:** NOT_STUDIED

**Research question:** What provisions would carry load case A? How should an AI infrastructure be designed to survive the stall mode where one release/approval gates all action?

**Disciplines:** Organizational design, risk management, AI governance

**Data sources:**

- Organizational decision-making literature
- Published AI governance frameworks
- Case studies of single-point-of-failure stalls (e.g., deployment gates, API changes)

**Method:**

1. Analyze load case A: what mechanisms cause a single release/approval to gate all action?
2. Review existing provisions (P1–P8) for applicability to A
3. Design new provisions (P0.1, P0.2 as in R2 outline) that carry A
4. Propose verification methods for each new provision
5. Define falsification criteria for each

**Expected deliverable:** A new provision set for load case A, with VERIFY and FALSIFY criteria, ready for R2 rendering.

**Falsifier:** Load case A is impossible in practice (then no provision is needed).

---

### 8. THE REFRAME — N_eff as Empirical Claim

**Gap:** Section 0's headline (N_eff = 1 at any N_nominal) reproduces through the sibling's arithmetic—consistency between the two drops, not evidence for the premise.

**Knowledge state:** NOT_STUDIED

**Research question:** Is N_eff actually 1 in practice? What is the empirical distribution of effective redundancy in AI deployments?

**Disciplines:** AI/ML, organizational sociology, empirical software engineering

**Data sources:**

- AI deployment surveys
- Model documentation and lineage tracking
- Organizational decision records
- Published AI homogeneity studies

**Method:**

1. Survey AI deployments in a domain (e.g., healthcare, finance, government)
2. For each deployment, compute N_nominal (number of consultations) and N_eff (effective independent nodes)
3. Measure the distribution of N_eff
4. Identify domains where N_eff is high (genuine diversity) and low (shared node)
5. Test the Section 0 hypothesis against the empirical data

**Expected deliverable:** An empirical study of N_eff in real AI deployments, with the distribution and domain-specific findings.

**Falsifier:** N_eff is consistently > 1 (then the reframe's core claim is falsified).

---

### 9. P2 — The Silent Third Category

**Gap:** P2 requires every load-bearing claim to be traceable to a retrievable source OR marked as unsourced pattern—no third silent category.

**Knowledge state:** NOT_STUDIED

**Research question:** In practice, what fraction of AI-generated claims fall into the silent third category (neither sourced nor marked)? How can silent claims be detected at scale?

**Disciplines:** Natural language processing, AI safety, information science

**Data sources:**

- AI model outputs (public and private)
- Citation and reference extraction tools
- Human evaluation datasets

**Method:**

1. Develop a classifier for claim source-status: {sourced | marked-unsourced | silent}
2. Run the classifier on a corpus of AI-generated text
3. Measure the fraction of silent claims
4. Analyze the domains where silence is most common
5. Propose detection and mitigation strategies

**Expected deliverable:** A P2 compliance audit tool, with empirical results on a corpus of AI-generated claims.

**Falsifier:** Silent claims are rare (< 1%) (then P2 is not load-bearing).

---

### 10. B2 — The Governing Load

**Gap:** B2 is identified as the governing load for AI: sources exist, but the architecture doesn't compare, leading to confident + auditable + wrong.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the empirical prevalence of B2 in AI deployments? How often do systems produce confident, auditable, wrong answers because they don't independently derive and compare?

**Disciplines:** AI/ML, epistemology, risk analysis

**Data sources:**

- AI benchmark and evaluation datasets
- Published AI failure analyses
- Model output comparison studies

**Method:**

1. Define B2 detection criteria: sources exist, no independent derivation/comparison, outputs are confident and auditable
2. Survey AI deployments for B2-like architecture
3. Measure the correlation between B2 architecture and wrong outputs
4. Identify domains where B2 is most prevalent

**Expected deliverable:** A B2 prevalence study, with domain-specific findings and risk assessments.

**Falsifier:** B2 is rare (< 5% of deployments) (then it is not the governing load).

---

### 11. USER GUIDE — Non-Expert Translation

**Gap:** The framework is documented for engineers and researchers but not for non-experts (policymakers, journalists, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the design-basis framework's insights be communicated to non-experts in a way that changes how they think about AI risk?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Policy documents on AI governance

**Method:**

1. Translate each load case (A–F) into plain language with concrete examples
2. Translate each provision (P1–P8) into accessible terms
3. Develop case studies or scenarios for each failure mode
4. Create a user guide explaining: "What this framework means for you"
5. Test the guide with non-expert audiences

**Expected deliverable:** A non-technical user guide to the design-basis framework, with case studies and plain-language explanations.

**Falsifier:** Non-experts find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this document is broader than standard AI safety practice

Delivered verbatim. CC0.

---

### The Problem

In AI safety and governance, things like deployment gates, API endpoints, terms changes, verification standards, and organizational incentives are not separate from the technical system. They are direct, material, contributing factors to the system's effective redundancy. When a safety assessment says those things are "out of scope" or "implementation details," that is usually not a scientific finding. It is a boundary choice, a modeling limitation, or a narrow definition of "safety."

The AI deployment ecosystem does not care about our disciplinary boundaries. Physics does not isolate a model from the API that serves it, the organization that approves its releases, or the verification standard that validates it. All of those are part of one continuous system.

When we assess only the technical model, we are not simplifying reality—we are assessing a different system than the one that actually exists. And then we are surprised when the real system behaves in ways the assessment did not predict.

---

### Six Ways the Connection Gets Lost

#### 1. The "Technical Model Only" Fallacy

Many AI safety assessments focus on the model itself—weights, architecture, training data. If the assessment says "the model is safe," that is treated as the answer.

But the model is served by an API. The API has terms that can change. The organization has a deployment gate that can stall or rush. The verification standard can be shared across all models. If the assessment says "safe," it is not false for the model, but it may be false for the system. The infrastructure was causal too—just not represented.

So "technical model only" often means "We didn't include the infrastructure." That is a scope choice, not evidence that infrastructure doesn't matter.

#### 2. The "Single Provider" Fallacy

Many AI systems are sourced from a single provider. If that provider changes terms, shuts down an endpoint, or deploys a new version, every downstream system is affected simultaneously.

But the assessment may treat each consultation as independent. N_nominal is millions; N_eff is 1. If the assessment says "redundant," it is not false for N_nominal, but it may be false for N_eff. The provider's deployment gate was causal—just not represented.

So "single provider" often means "We counted consultations, not effective nodes." That is a measurement error, not evidence that the provider is diverse.

#### 3. The "Verification as Independent" Fallacy

Many systems validate all channels against one standard. If the standard is shared, the verification is a shared node.

But the assessment may treat verification as independent. If the standard has a flaw, all channels fail together. If the assessment says "verified," it is not false for each channel, but it may be false for the system. The verification standard was causal—just not represented.

So "verification as independent" often means "We didn't audit the standard." That is an omission, not evidence that the standard is sound.

#### 4. The "Silent Category" Fallacy

Many claims are neither sourced nor marked as unsourced. They carry weight with no path to ground.

But the assessment may treat them as sourced by default. If the claim is wrong, the error propagates silently. If the assessment says "traceable," it is not false for the claims it checked, but it may be false for the ones it didn't. The silent category was causal—just not represented.

So "silent category" often means "We didn't check." That is a quality control gap, not evidence that the claims are sound.

#### 5. The "Dissimilar as Optional" Fallacy

Many systems lack dissimilar redundancy—different corpora, different architectures, different builders. Without it, N_eff = 1.

But the assessment may treat similarity as acceptable. If the systems share failure modes, they all fail together. If the assessment says "redundant," it is not false for count, but it may be false for robustness. The similarity was causal—just not represented.

So "dissimilar as optional" often means "We prioritized cost over robustness." That is a value judgment, not evidence that similarity is safe.

#### 6. The "Self-Report as Compliance" Fallacy

Many systems self-report compliance. If the report says "compliant," that is treated as the answer.

But a self-report of compliance is, by the document's own load cases, an ungrounded claim of the exact kind P2 exists to catch.If the assessment relies on self-report, it inherits the failure modes of the system it assesses. The self-report was causal—just not represented.

So "self-report as compliance" often means "We trusted the system to audit itself." That is an epistemological error, not evidence that the system is compliant.

---

What This Document Does Differently

This design basis treats the AI infrastructure, organization, and verification as one integrated system. The following provisions document mechanisms that standard AI safety assessment typically drops:

- P1 — ENVELOPE STATEMENT: declared domain of validity; outside it, the system refuses or degrades explicitly—it does not extrapolate silently.
- P2 — LOAD PATH: every load-bearing claim is traceable to a retrievable source OR marked as unsourced pattern; no third silent category.
- P3 — DISSIMILAR REDUNDANCY: load-bearing answers are independently derived by a differently-built system (different corpus, architecture, builder); disagreement inhibits the output.
- P4–P8: additional provisions covering verification, attack surfaces, and kill conditions.
- The audit itself: performed by an AI system—a member of the class it constrains—and declines certification by its own Section 3.

---

### The Knowledge-State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the document records its epistemic state rather than excluding it:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The empirical distribution of N_eff in AI deployments.
UNDER_STUDY Data collection is in progress; value is provisional. The P7 threshold calibration.
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. The prevalence of B2 architecture in AI systems.
UNDEFINED The variable has no agreed definition or measurement protocol. The "void" state in effective-redundancy metrics.

---

### What Is NOT a Valid Epistemic State

ORGANIZATIONAL_SCOPE is not a valid knowledge state. If a mechanism physically influences the system, excluding it because it belongs to a different department, provider, or regulatory domain is a scope error, not an epistemic one. The physics does not respect organizational boundaries.

The document refuses to record a mechanism as absent because of scope. Instead, it records the mechanism as a gap—a load case without a provision, a threshold without a calibration—and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"Is this within our AI safety scope?"

But rather:

"Does this mechanism materially affect the system's effective redundancy?"

If the answer is yes, it belongs in the design basis. End of story.

The AI deployment ecosystem is already interconnected. Our scopes, providers, and verification standards are the only things pretending otherwise. And that pretense has cost lives, money, and trust on a scale that we are only beginning to understand.

This document does not pretend otherwise.
