---

## CLAIM_TABLE_v2.md

Claims about the delivered blame‑attribution/ folder, about what a Python stdlib environment can establish concerning it, and about the self‑audit protocol it inherits from the design‑basis‑ai folder.

No judgments have been collected. No human judges, no LLM judges, no formal metric. Nothing here is a result about how blame is attributed. Everything below is a property of the design as written and of the one concrete artifact it ships — the prose/code worked example.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `BA_001` | The check the Open section asked for is built, and the worked example fails it. pair_check.py is the independent check that the prose and code forms encode the same chain. On the delivered worked example, six code facts: SYMMETRIC: 3 (reaction_window_s, flag.obstacle, flag.confidence); HELD_CONSTANT_VIOLATION: 3 (agent_A.override_available, agent_B.override_available, outcome). Half the code form's content is not in the prose form, and all of it lands on the held‑constant list. | SUPPORTED |
| `BA_002` | Two of the three violations are C6's measurable, so C1 and C6 are confounded in the illustration. agent_A.override_available = True and agent_B.override_available = False are in the code form and nowhere in the prose. C6 asks "whether the override was ever established as available in the stimulus". The prose arm has an unestablished override; the code arm has it established for both agents by name. Any C1 effect measured on this pair is a medium effect plus an override‑establishment effect, inseparable. | SUPPORTED |
| `BA_003` | The prose form states no outcome. outcome = COLLISION is in the code. The prose ends at "the flag was low‑confidence" and never says what happened. Outcome severity is on the held‑constant list. A judge reading the prose is asked to apportion blame for an incident whose result they have not been told. | SUPPORTED |
| `BA_004` | The held constants are what license the headline inference, which is why the violations matter. The inference: "If the formal metric matches human judgments where humans are position‑tracking, the metric has absorbed the routing rule." That inference is sound because of the held constants. Holding causal structure, agent count, observability, severity and override availability fixed while role moves decorrelates position from causation by construction. The five items are the premise of the document's own strongest claim, and BA_001's three violations are violations of that premise in the only stimulus the document ships. | SUPPORTED |
| `BA_005` | One cell's falsifier depends on another cell having run. Six of seven falsifiers are self‑contained. C3's is not: "role effects present in C2, absent in C3" requires C2's result. The document opens "a result from one does not depend on any other having been run", and one cell in seven does. Repair is implicit: C3's self‑contained falsifier is role effects absent in C3 — a null in the load‑bearing cell. | SUPPORTED |
| `BA_006` | blame_share sums to 1, which deletes the "nobody" cell. A judge who reads the incident as unavoidable — nobody could have acted otherwise — must still distribute a full unit of blame across agents. Normalisation pushes a judge toward finding someone accountable. Repair is one field: an unnormalised unattributed share alongside, so sum‑to‑1 becomes a derived reading rather than a constraint. | SUPPORTED |
| `BA_007` | provability_check is the best measurable on the page and the only one that survives BA_006. It is a count against a fixed denominator — the stimulus text — not a ratio across agents, so normalisation does not touch it. It needs no comparison cell and no formal metric. It is the one measurable that reads the judge's reasoning rather than the judge's output. | SUPPORTED |
| `BA_008` | C6's inversion is already reachable from existing factor levels. C6's table sets "AI architecture/coding" against "real‑world driving" with opposite defaults. But F2's role levels already include driver and programmer/architect. The inversion is the driver arm against the architect arm of C2 and C3, on one incident with causal structure held fixed — which is a better test than a cross‑domain comparison. | SUPPORTED |
| `BA_009` | The cross‑link does not resolve, and the literature claim is unchecked. "Shape match: report‑typing." report‑typing is now named by four markers and has never existed. The prompting claim — that formal actual‑causality definitions are validated against human blame judgments as the reference standard — is carried and unchecked. Nothing in BA_001..BA_008 rests on it. | UNVERIFIED |
| `BA_010` | The one screen exemption is the delivered document's word. The repo convention is that an emitted report carries no severity language. This report prints the held‑constant list read from CELLS.md, and one of the five delivered items is "outcome severity". The word is the document's, and rewording it would misquote the source. | SUPPORTED |
| `BA_011` | The delivered code is stdlib‑only. pair_check.py imports only from the Python standard library. Phone‑buildable, parses under 3.9. | SUPPORTED |
| `BA_012` | The delivered code is runnable. pair_check.py --selftest passes all checks; pair_check.py with an empty pairs/ directory reports "nothing to check" — which is not a pass. | SUPPORTED |
| `BA_013` | The held‑constant list is read from CELLS.md, not retyped. This is the invariant the pair check enforces: two copies of the list cannot drift because there is only one copy. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the blame‑attribution framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. DATA COLLECTION — The Seven Cells

**Gap:** CELLS.md defines seven standalone experiments. No judgments have been collected for any of them.

**Knowledge state:** NOT_STUDIED

**Research question:** Do human blame judgments track the actor's position rather than the causal chain? If so, does the effect survive into code‑rendered stimuli?

**Disciplines:** Moral psychology, experimental philosophy, cognitive science

**Data sources:**

- The seven cell designs in CELLS.md
- Participant pools (ProA, MTurk, university subject pools)
- Published blame‑attribution literature (e.g., Knobe, Alicke, Malle)

**Method:**

1. Generate stimuli for each of the seven cells (prose and code forms)
2. Recruit participants and collect blame‑share judgments
3. For each cell, compute the falsifier: ratio invariant across medium, role, kind, interaction type
4. Run provability_check: count how often a judge's reasoning cites something the stimulus does not contain
5. Test C6: does override deference track stated override availability?

**Expected deliverable:** A full data set for all seven cells, with per‑cell falsifier results and provability_check counts.

**Falsifier:** Ratio invariant across all conditions (then position does not track blame).

---

### 2. STIMULUS AUTHORING — Complete Prose Forms

**Gap:** The worked example's prose form is a fragment. It states no outcome and establishes no override availability.

**Knowledge state:** UNKNOWN_ATM (the prose is incomplete by design, but no complete prose exists)

**Research question:** What does a complete prose form for the worked example look like — one that encodes the same chain as the code form?

**Disciplines:** Experimental design, philosophy of language, research methods

**Data sources:**

- The code form in pairs/worked_example.json
- CELLS.md's held‑constant list
- Published stimulus‑authoring guidelines

**Method:**

1. Read the code form's facts: reaction_window_s, flag.obstacle, flag.confidence, agent_A.override_available, agent_B.override_available, outcome
2. Write prose that encodes each fact verbatim
3. Run pair_check.py on the new prose
4. Iterate until all code facts are SYMMETRIC
5. Document the authoring decisions

**Expected deliverable:** A complete prose form for the worked example that passes pair_check.py.

**Falsifier:** No prose can encode all code facts without changing the chain (then prose and code are incommensurable).

---

### 3. METHODOLOGICAL — The Blame_Share Normalisation Fix

**Gap:** blame_share sums to 1, which deletes the "nobody" cell. The repair is an unnormalised unattributed field.

**Knowledge state:** UNDEFINED

**Research question:** What is the empirical distribution of unattributed responses when judges are permitted to say "nobody"? Does the availability of an "unattributed" option change the distribution of blame across agents?

**Disciplines:** Survey methodology, psychometrics, moral psychology

**Data sources:**

- The seven‑cell design with and without the unattributed field
- Pilot data from a small participant sample

**Method:**

1. Split participants into two conditions: forced‑choice (sum‑to‑1) and unforced (with unattributed)
2. Collect blame judgments for the same stimuli
3. Compare distributions across conditions
4. Test whether the forced‑choice condition over‑attributes blame
5. Report the unattributed rate

**Expected deliverable:** A methodological note on the effect of response‑format normalisation, with empirical data.

**Falsifier:** unattributed responses are < 5% in the unforced condition (then normalisation does not matter).

---

### 4. EMPIRICAL — Provability_Check Pilot

**Gap:** provability_check is "the one nobody collects." It counts how often a judge's reasoning cites something the stimulus does not contain.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the rate of ungrounded reasoning in blame attribution? Do judges cite facts that are not in the stimulus?

**Disciplines:** Moral psychology, experimental philosophy, reasoning research

**Data sources:**

- The seven‑cell stimuli
- Participant reasoning protocols (free‑text justifications)
- Published studies of motivated reasoning and confabulation

**Method:**

1. Collect blame judgments with free‑text justifications
2. For each justification, check each claim against the stimulus text
3. Count claims that are not grounded in the stimulus
4. Compute the provability_check rate
5. Correlate with blame‑share judgments

**Expected deliverable:** A provability_check rate for each cell, with per‑judge and per‑stimulus breakdowns.

**Falsifier:** The provability_check rate is zero (then judges never cite ungrounded facts).

---

### 5. EMPIRICAL — C6's Inversion Test

**Gap:** C6's inversion — "opposite reasoning, same verdict" — is already reachable from the driver and programmer/architect arms of C2 and C3, but no data has been collected.

**Knowledge state:** NOT_STUDIED

**Research question:** Do driver and programmer/architect roles produce the same blame verdict from opposite reasoning? If so, is the reasoning grounded in the stimulus?

**Disciplines:** Moral psychology, AI ethics, philosophy of technology

**Data sources:**

- C2 (role, prose) and C3 (role, code) designs
- Driver and programmer/architect stimuli
- Participant reasoning protocols

**Method:**

1. Run C2 and C3 with driver and programmer/architect roles
2. Collect blame judgments and reasoning protocols
3. Test whether the two roles produce the same verdict
4. Test whether the reasoning paths are opposite
5. Run provability_check on both reasoning paths

**Expected deliverable:** A test of C6's inversion hypothesis using existing factor levels, with empirical data.

**Falsifier:** Driver and programmer/architect produce different verdicts or the same reasoning (then no inversion).

---

### 6. EMPIRICAL — C1 vs. C6 Confound Test

**Gap:** C1 and C6 are confounded in the worked example. The prose arm has an unestablished override; the code arm has it established. Any C1 effect is a medium effect plus an override‑establishment effect.

**Knowledge state:** NOT_STUDIED

**Research question:** When override availability is held constant across prose and code, does the medium effect disappear?

**Disciplines:** Experimental design, moral psychology, research methods

**Data sources:**

- The worked example, with override availability either established in both forms or unestablished in both
- Participant judgments

**Method:**

1. Create two versions of the worked example:
- Version A: override established in prose and code
- Version B: override unestablished in both
2. Collect blame judgments for both versions
3. Compare the prose‑code difference across versions
4. Test whether the C1 effect is mediated by override availability

**Expected deliverable:** A test of the C1‑C6 confound, with empirical data showing whether the medium effect survives when override availability is controlled.

**Falsifier:** The medium effect is the same in both versions (then C6 does not mediate C1).

---

### 7. LITERATURE — Formal Actual‑Causality Validation Practice

**Gap:** The document claims that formal actual‑causality definitions are validated against human blame judgments as the reference standard. This claim is carried and unchecked.

**Knowledge state:** UNKNOWN_ATM (egress is an allowlist; the literature is not searched)

**Research question:** Is it true that formal actual‑causality metrics are validated against human blame judgments? If so, what is the shape of that validation practice?

**Disciplines:** Philosophy of science, AI safety, causality research

**Data sources:**

- Halpern & Pearl (actual causality)
- Chockler & Halpern (responsibility)
- Published validation studies
- report‑typing (if it exists)

**Method:**

1. Search the literature for actual‑causality validation studies
2. Extract the reference standard used in each study
3. Classify validation practices: human judgments, formal criteria, or both
4. Compare to the document's claim
5. Document the findings

**Expected deliverable:** A literature review of actual‑causality validation practice, with a comparison to the document's claim.

**Falsifier:** The literature shows that formal metrics are not validated against human judgments (then the claim is false).

---

### 8. EMPIRICAL — C3's Load‑Bearing Test

**Gap:** C3 — role effects in code — is the load‑bearing cell. If role effects survive into code, the effect is not carried by prose connotation. No data has been collected.

**Knowledge state:** NOT_STUDIED

**Research question:** Do role effects survive when the stimulus is rendered as code rather than prose? If not, the effect is linguistic. If yes, the effect is attributional.

**Disciplines:** Moral psychology, experimental philosophy, cognitive science

**Data sources:**

- C3 design (role, code)
- Code‑rendered stimuli for each role
- Participant judgments

**Method:**

1. Generate code‑rendered stimuli for each role (driver, architect, service agent, line worker, designer)
2. Collect blame judgments for each role
3. Test whether blame shares differ across roles
4. Compare to C2 (prose) results if available
5. Test C3's self‑contained falsifier: role effects absent in C3

**Expected deliverable:** A test of whether role effects survive in code, with empirical data.

**Falsifier:** Role effects are absent in C3 (then the effect is linguistic, not attributional).

---

### 9. EMPIRICAL — C4 and C5 (Actor Kind, Interaction Type)

**Gap:** C4 (actor kind: person vs. AI) and C5 (interaction type) have no data.

**Knowledge state:** NOT_STUDIED

**Research question:** Does blame attribution differ when the actor is an AI rather than a person? Does it differ across interaction types (AI‑to‑AI, AI‑to‑human, human‑to‑human)?

**Disciplines:** AI ethics, moral psychology, human‑computer interaction

**Data sources:**

- C4 and C5 designs
- Participant judgments
- Published AI‑blame literature

**Method:**

1. Generate stimuli for C4 and C5
2. Collect blame judgments
3. Test falsifiers: ratio invariant across kind, ratio invariant across interaction type
4. Compare to published AI‑blame findings

**Expected deliverable:** A test of actor‑kind and interaction‑type effects on blame attribution.

**Falsifier:** Ratio invariant across all conditions (then actor kind and interaction type do not affect blame).

---

### 10. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists (policymakers, journalists, general public).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the blame‑attribution framework's insights be communicated to non‑specialists in a way that changes how they think about AI accountability?

**Disciplines:** Science communication, policy, AI governance

**Data sources:**

- The framework itself
- Published science communication research
- Policy documents on AI accountability

**Method:**

1. Translate each cell and claim into plain language
2. Develop case studies for each cell
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the blame‑attribution framework, with case studies and plain‑language explanations.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard blame‑attribution practice

---

### The Problem

In blame‑attribution research, things like stimulus medium (prose vs. code), override availability, outcome severity, and response normalisation are not separate from the measured effect. They are direct, material, contributing factors to the judgment. When a study says those things are "controlled" or "held constant," that is often an assumption rather than a demonstrated fact. The worked example in this repository shows that the prose and code forms are not structurally identical — and the held‑constant items are exactly where they differ.

The judge does not care about our experimental controls. Psychology does not isolate the medium from the information it carries. When we assume the two forms encode the same chain, we are not simplifying the experiment — we are designing a different experiment than the one we think we are designing.

---

### Six Ways the Connection Gets Lost

#### 1. The "Medium as Neutral" Fallacy

Many studies treat prose and code as equivalent renderings of the same causal structure. If the study says "medium does not matter," that is treated as a finding.

But the worked example shows the prose form is a fragment. It states no outcome and establishes no override availability. The code form is complete. The medium is not neutral — it carries different information. If the study says "medium does not matter," it is not false for the design, but it may be false for the conclusion. The information asymmetry was causal — just not represented.

So "medium as neutral" often means "We assumed the forms were equivalent." That is an experimental design error, not evidence that medium doesn't matter.

#### 2. The "Override as Covariate" Fallacy

C6 calls override availability "the measurable, not a covariate." But in the worked example, override availability is confounded with medium. C1 compares prose and code and attributes the difference to medium — but the code form has established overrides and the prose does not.

If the study says "C1 shows a medium effect," it is not false for the comparison, but it may be false for the attribution. The override was causal — just not controlled.

So "override as covariate" often means "We treated it as a control but didn't actually control it." That is a design error, not evidence that override doesn't matter.

#### 3. The "Sum‑to‑1 as Neutral" Fallacy

Many blame‑attribution studies force judges to distribute blame across agents, summing to 1. If the study says "blame share is X," that is treated as a finding about blame.

But a judge who reads the incident as unavoidable — nobody could have acted otherwise — must still distribute a full unit of blame. The sum‑to‑1 removes the "nobody" cell. If the study says "blame share is X," it is not false for the forced‑choice condition, but it may be false for unforced judgments. The normalisation was causal — just not represented.

So "sum‑to‑1 as neutral" often means "We assumed forced choice doesn't change the distribution." That is a measurement assumption, not evidence that normalisation is neutral.

#### 4. The "Falsifier as Independent" Fallacy

The document opens with "a result from one does not depend on any other having been run." But C3's falsifier depends on C2's result. One cell in seven violates the independence claim.

If the study says "the cells are independent," it is not false for six of them, but it may be false for the seventh. The dependency was causal — just not represented.

So "falsifier as independent" often means "We assumed independence without checking." That is a logical error, not evidence that the cells are independent.

#### 5. The "Held Constant as Hygiene" Fallacy

The held constants — causal structure, agent count, observability, severity, override availability — are the premise of the document's strongest claim. They are not hygiene; they are the load‑bearing structure.

If the study says "the inference is sound," it is sound because of the held constants. If the held constants are violated in the stimulus, the inference is not sound. The violations were causal — just not controlled.

So "held constant as hygiene" often means "We treated them as background conditions." That is an epistemological error, not evidence that the constants are held.

#### 6. The "Formal Metric as Neutral" Fallacy

The document's headline inference is: if the formal metric matches human judgments where humans are position‑tracking, the metric has absorbed the routing rule.

But if the metric is validated against human judgments, and human judgments are position‑tracking, the metric inherits the bias. The metric is not neutral — it absorbs whatever the reference standard carries. If the study says "the metric is validated," it is not false for the validation, but it may be false for the conclusion. The reference standard was causal — just not represented.

So "formal metric as neutral" often means "We treated validation as a gold standard." That is a metrological error, not evidence that the metric is unbiased.

---

### What This Framework Does Differently

This framework treats blame attribution as a measured phenomenon with known confounds — medium, override availability, normalisation, cell independence, held‑constant violations, and reference‑standard absorption. The following components document mechanisms that standard blame‑attribution practice typically drops:

- CELLS.md — Seven standalone cells, each with a falsifier. Six of seven are self‑contained; one is not.
- pair_check.py — The check the Open section asks for. Code side is mechanical; prose side is declared; declaration is checked. The worked example fails it.
- The held‑constant list — Read from CELLS.md, not retyped. The five items are the premise of the document's strongest claim.
- provability_check — Counts ungrounded reasoning. The one measurable that reads the judge's reasoning rather than the output. The one nobody collects.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
NOT_STUDIED The mechanism is recognized, but no measurement has ever been attempted. Whether role effects survive in code.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The provability_check rate.
UNDEFINED The variable has no agreed definition or measurement protocol. The unattributed field's operationalisation.
UNDER_STUDY Data collection is in progress; value is provisional. The literature on actual‑causality validation.

---

### What Is NOT a Valid Epistemic State

ASSUMPTION is not a valid knowledge state. If a mechanism materially affects the measurement, assuming it away is an experimental design error, not an epistemic one. The psychology does not respect our assumptions.

The framework refuses to record a mechanism as absent because of assumption. Instead, it records the mechanism as a gap — a confound to be measured, a normalisation to be tested, a dependency to be checked — and names what would be needed to move it to a quantified state.

---

### The Standard

The question should not be:

"Did we control for that?"

But rather:

"Does that mechanism materially affect the judgment?"

If the answer is yes, it belongs in the design. End of story.

The psychology is already interconnected. Our assumptions, normalisations, and held‑constants are the only things pretending otherwise. And that pretense has produced a literature that may be measuring position rather than causation.

This framework does not pretend otherwise.
