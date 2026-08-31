---

## CLAIM_TABLE.md

Claims about the delivered constraint-assembly/ folder, about what a Python stdlib environment can establish concerning it, and about the composition protocol it inherits.

This is a case reader, not a simulation. It reads JSON case files, checks for composition, and returns structural verdicts—composition present, selection not assembly, soft reliance flagged. It emits no verdict about the operator, no score, no comparison. Every readout is a property of the recorded case.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `CA_001` | Constraints are not what limits the option set. They are what makes composition computable. A term that will not move can be leaned on; a soft term cannot, because there is no way to know when the pieces add up. The parts inventory is domains with hard laws in them. More hard constraints, more composition available. | SUPPORTED (by mechanism definition) |
| `CA_002` | The reversal runs opposite to the two nearest sibling folders on the same object. generation-capacity: option space reduced upstream, cannot generate what is missing. presented-binary: option set closed at presentation, reduction is performed rather than found. constraint-assembly: option is constructed out of parts that individually do not do the job. The three are not in tension—they are three positions on one quantity. | SUPPORTED |
| `CA_003` | The mechanism is decidability. Composition needs a stopping rule, and a term that holds regardless of use supplies one. A term that moves under load does not, so a plan resting on it has no assembly guarantee—which is why soft is a recorded class rather than an excluded one. | SUPPORTED |
| `CA_004` | Two constraint classes exist, and merging them loses the failure mode. invariant: holds regardless of use, cannot be spent, available for the whole event. consumable: finite, availability destroyed by spending. Partial use can be worse than none—applying brakes without enough air to stop leaves zero air, zero brakes, and the grade still acting. | SUPPORTED |
| `CA_005` | The distinction that matters operationally: an invariant is encountered; a consumable is spent. Failure on a consumable is usually spending it, not running into it. | SUPPORTED |
| `CA_006` | Rejected candidates are the data. A composed solution is only visible as composition if the options that were rejected are recorded with the reason. Each rejection names which constraint ruled it out. | SUPPORTED |
| `CA_007` | A case with no rejections is a case of selection, not assembly. The tool records it as such. | SUPPORTED |
| `CA_008` | composition_present fails closed. Used components composition unknown, single sufficient, or unrecorded sufficiency all block composition. The reason is visible—which is the opposite direction from closure-cost CC_003, where an omitted field reads as the informative state. | SUPPORTED |
| `CA_009` | Diagnostic quarantine is recorded separately from the assembly. Where a cause is unknown at the time of action, whether the diagnostic was deferred is recorded. Establishing what class of event this is spends the same budget the assembly needs. | SUPPORTED |
| `CA_010` | The delivered code is stdlib‑only. assemble.py and assembly_audit.py import only from the Python standard library. | SUPPORTED |
| `CA_011` | The delivered code is runnable. assemble.py --selftest passes 18/18 checks, rc=0. | SUPPORTED |
| `CA_012` | Two cases are delivered. grade-stop.json is a single operating record with four components and four grounded rejections. flood-ground.json is a structural placeholder with no rejections. | SUPPORTED |
| `CA_013` | grade-stop records an assembly, not a selection. Four rejected options are each grounded in a specific constraint that ruled them out. | SUPPORTED |
| `CA_014` | flood-ground is correctly read as selection rather than assembly. It has no rejections recorded. | SUPPORTED |
| `CA_015` | The central weakness is named and unfilled. Recognition‑primed selection and genuine construction look identical in a single‑instance retrospective record. Whether a composition was built during the event or recalled from prior route knowledge is not separable from any case currently in here. | OPEN |
| `CA_016` | No quantities are recorded anywhere. grade-stop has grade percentage and gravel friction as nameable laws but no numbers were taken. The assembly is recorded as a structure, never as an energy balance. | SUPPORTED (as a stated gap) |
| `CA_017` | The rejected options are recorded from recall, which is the same self‑report defect flagged throughout closure-cost . | SUPPORTED (as a stated gap) |
| `CA_018` | CLAIM_TABLE.md was not delivered. The audit notes: "delivered: assemble.py, README.md, 2 cases / not delivered: CLAIM_TABLE.md". | SUPPORTED |

---

## UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the constraint‑assembly framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. EMPIRICAL — Recognition vs. Construction Separator

**Gap:** Recognition‑primed selection and genuine construction look identical in a single‑instance retrospective record. No case in the file establishes the distinction.

**Knowledge state:** UNDEFINED

**Research question:** What experimental design separates recognition‑primed selection from genuine construction? Can a during‑event record or a novel constraint set provide the separator?

**Disciplines:** Cognitive psychology, decision science, experimental design

**Data sources:**

- Naturalistic decision‑making literature (Klein, recognition‑primed decision model)
- Published studies of expert decision‑making under time pressure
- The constraint-assembly case schema

**Method:**

1. Design an experiment with two conditions:
- Recognition condition: participants have prior exposure to the constraint set
- Novel condition: participants face a constraint set they have never encountered
2. Measure solution time, rejection patterns, and self‑reported construction vs. recall
3. Test whether the two conditions produce distinguishable signatures
4. Propose a separator criterion for the case schema

**Expected deliverable:** An experimental protocol and separator criterion for distinguishing recognition from construction in retrospective records.

**Falsifier:** No measurable difference between recognition and construction conditions (then the distinction is not empirically separable).

---

### 2. EMPIRICAL — Quantity Recording in Real Cases

**Gap:** grade-stop has grade percentage and gravel friction as nameable laws but no numbers were taken. The assembly is recorded as a structure, never as an energy balance.

**Knowledge state:** NOT_STUDIED

**Research question:** What quantities would make a constraint‑assembly case quantitatively testable? Can an energy‑balance version of grade-stop be constructed with real numbers?

**Disciplines:** Engineering mechanics, vehicle dynamics, numerical methods

**Data sources:**

- Published vehicle dynamics data (grade resistance, friction coefficients, air brake performance)
- Trucking industry standards for grade stopping
- The grade-stop case structure

**Method:**

1. Identify the physical quantities implied by each component:
- Gravel shoulder friction: coefficient of friction, vehicle weight, contact area
- Uphill grade: grade percentage, vehicle mass, gravitational acceleration
- Remaining service air: reservoir volume, pressure, brake application rate
- Steering input: steering ratio, force required, duration
2. Source real values from engineering handbooks or published data
3. Compute whether the assembly would stop the vehicle (energy balance)
4. Test sensitivity to each quantity
5. Produce a quantitatively grounded version of the case

**Expected deliverable:** A grade-stop.quantified.json with real numbers and an energy‑balance computation.

**Falsifier:** The quantities cannot be sourced or the energy balance does not close (then the case remains structural).

---

### 3. EMPIRICAL — Invariant vs. Consumable Failure Distribution

**Gap:** The framework claims that "failure on a consumable is usually spending it, not running into it". This is a prediction about the distribution of failure modes.

**Knowledge state:** NOT_STUDIED

**Research question:** In real constraint‑assembly cases, what fraction of failures are due to spending a consumable versus encountering an invariant? Does the prediction hold?

**Disciplines:** Safety engineering, human factors, incident analysis

**Data sources:**

- Incident databases (aviation, maritime, industrial, transportation)
- Published case studies of constraint‑assembly failures
- NTSB, MAIB, and other accident investigation reports

**Method:**

1. Identify incident reports where a solution was assembled from insufficient components
2. Classify each failure as:
- Consumable spent (resource exhausted before completion)
- Invariant encountered (unexpected law or boundary)
- Both
- Neither
3. Compute the distribution
4. Test whether consumable‑spending dominates
5. Document the findings

**Expected deliverable:** A failure‑mode distribution for constraint‑assembly incidents, with test of the spending‑vs‑encountering prediction.

**Falsifier:** Invariant‑encountering failures are as common as consumable‑spending failures (then the prediction is falsified).

---

### 4. EMPIRICAL — Soft Term Reliance in Practice

**Gap:** The framework states: "A plan built on a soft term has no assembly guarantee". Soft terms are recorded so that reliance on one is visible.

**Knowledge state:** NOT_STUDIED

**Research question:** How often do real constraint‑assembly cases rely on soft terms? Does soft‑term reliance correlate with failure?

**Disciplines:** Safety engineering, organizational theory, risk analysis

**Data sources:**

- Incident databases with constraint descriptions
- Published case studies of assembly‑based decisions
- The constraint-assembly case schema (with soft class)

**Method:**

1. Survey real constraint‑assembly cases for soft‑term reliance
2. Classify each case as:
- No soft terms
- Soft term(s) present but not load‑bearing
- Soft term(s) load‑bearing
3. Correlate soft‑term load‑bearing with outcome (success/failure)
4. Test whether soft‑term reliance predicts failure
5. Document the findings

**Expected deliverable:** A soft‑term reliance study with correlation to outcome.

**Falsifier:** Soft‑term reliance does not correlate with failure (then the "no assembly guarantee" claim is not empirically supported).

---

### 5. EMPIRICAL — Partial Use Destruction in Real Cases

**Gap:** The framework states that for consumables, "partial use can be worse than none". This is a load‑bearing claim about the structure of consumable failure.

**Knowledge state:** NOT_STUDIED

**Research question:** Are there documented cases where partial use of a consumable was worse than no use? Does the pattern match the air‑brake example?

**Disciplines:** Safety engineering, human factors, resource management

**Data sources:**

- Incident databases with resource‑consumption descriptions
- Published cases of consumable exhaustion
- The grade-stop case itself

**Method:**

1. Identify cases where a consumable was partially used and then exhausted
2. Compare outcome to cases where the consumable was not used
3. Test whether partial‑use cases have worse outcomes
4. Identify the conditions under which partial use is worse than none
5. Document the findings

**Expected deliverable:** A case study collection on partial‑use destruction, with conditions and outcomes.

**Falsifier:** No cases of partial‑use destruction can be found (then the claim is theoretical).

---

### 6. EMPIRICAL — Flood‑Ground Case Collection

**Gap:** flood-ground.json is a structural placeholder with no rejections and no actual recorded instance. It tests whether the composition operation belongs to driving or to anything with hard constraints in it.

**Knowledge state:** NOT_STUDIED

**Research question:** Are there real flood‑ground cases where a person on foot assembled a crossing from components that individually do not do the job? If so, do they record identically to the vehicle case?

**Disciplines:** Hydrology, wilderness medicine, emergency response

**Data sources:**

- Search and rescue incident reports
- Published accounts of flood crossings
- Wilderness medicine and survival literature
- The flood-ground case schema

**Method:**

1. Search for documented flood‑crossing decisions where:
- No single option was sufficient
- Multiple components were combined
- Components were physical laws (water momentum, terrain gradient, time)
2. For each case, extract: components, rejections, budget terms, diagnostic state
3. Populate a flood-ground.real.json from real data
4. Test whether the operation records identically to grade-stop

**Expected deliverable:** A real flood-ground case file with grounded rejections and components.

**Falsifier:** No real flood‑ground cases can be found (then the placeholder remains a placeholder).

---

### 7. EMPIRICAL — Budget Terms as the Operational Quantity

**Gap:** The framework records budget_terms separately from components. Budget terms are the quantities that are actually spent or tracked during assembly.

**Knowledge state:** NOT_STUDIED

**Research question:** What is the relationship between budget terms and components in real constraint‑assembly cases? Do budget terms predict the assembly structure?

**Disciplines:** Operations research, resource management, decision science

**Data sources:**

- The grade-stop case (budget terms: stored air pressure, distance remaining, physical force)
- Published cases of resource‑constrained decision‑making
- Incident databases

**Method:**

1. Identify real constraint‑assembly cases with documented budget terms
2. For each case, map budget terms to components
3. Test whether budget terms predict which components are used
4. Test whether budget terms predict the rejection pattern
5. Document the mapping

**Expected deliverable:** A budget‑term to component mapping study, with predictive analysis.

**Falsifier:** Budget terms do not predict component use or rejection patterns (then budget terms are not the operational quantity).

---

### 8. EMPIRICAL — Diagnostic Deferral and Outcome

**Gap:** The framework records diagnostic deferral separately from assembly. Establishing what class of event this is spends the same budget the assembly needs.

**Knowledge state:** NOT_STUDIED

**Research question:** Does diagnostic deferral correlate with successful assembly? Is deferral a strategy or a failure mode?

**Disciplines:** Cognitive psychology, emergency management, decision science

**Data sources:**

- The grade-stop case (diagnostic deferred, cause unknown throughout)
- Incident databases with diagnostic timelines
- Published studies of diagnosis under time pressure

**Method:**

1. Identify cases where diagnostic deferral was recorded
2. For each case, determine:
- Was deferral intentional or forced?
- Did deferral enable assembly?
- Did deferral lead to later failure?
3. Test whether deferral correlates with outcome
4. Document the conditions under which deferral is adaptive vs. maladaptive

**Expected deliverable:** A diagnostic deferral study with outcome correlation and condition analysis.

**Falsifier:** Diagnostic deferral does not correlate with outcome (then deferral is not a load‑bearing variable).

---

### 9. METHODOLOGICAL — Rejected Options Recall Validity

**Gap:** The rejected options in grade-stop are recorded from recall, which is the same self‑report defect flagged throughout closure-cost.

**Knowledge state:** UNDEFINED

**Research question:** How valid are recalled rejections as evidence of assembly? Do people reconstruct rejections after the fact, or do they accurately remember what they ruled out?

**Disciplines:** Cognitive psychology, memory research, survey methodology

**Data sources:**

- Published memory research on decision recall
- Studies of post‑decision reconstruction
- The closure-cost framework (CC_003, omitted field as informative state)

**Method:**

1. Design a study where participants make a constrained decision
2. Immediately after, record their rejected options
3. Later (days/weeks), record their recalled rejections
4. Compare immediate vs. delayed recall
5. Test whether recall is accurate or reconstructed

**Expected deliverable:** A recall‑validity study for rejected options, with accuracy rates and reconstruction patterns.

**Falsifier:** Recall is accurate (> 90% match) (then the self‑report defect is not load‑bearing).

---

### 10. EMPIRICAL — The Three Positions on One Quantity

**Gap:** The framework states that generation-capacity, presented-binary, and constraint-assembly are three positions on one quantity. This is a claim about the structure of the sibling folders.

**Knowledge state:** UNDER_STUDY

**Research question:** Are the three sibling folders actually measuring different positions on the same underlying quantity? Can they be unified into a single instrument?

**Disciplines:** Metrology, systems theory, research design

**Data sources:**

- The three sibling folders: generation-capacity, presented-binary, constraint-assembly
- The constraint-assembly README and audit
- Published literature on option space measurement

**Method:**

1. Define the underlying quantity: "option space under constraint"
2. For each sibling folder, identify what it measures:
- generation-capacity: option space reduced upstream
- presented-binary: option set closed at presentation
- constraint-assembly: option constructed from components
3. Test whether the three measurements are orthogonal or collinear
4. Propose a unified instrument
5. Document the unification

**Expected deliverable:** A unified instrument for measuring option space under constraint, with calibration across the three sibling folders.

**Falsifier:** The three measurements are orthogonal (then they are not positions on one quantity).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists.

**Knowledge state:** NOT_STUDIED

**Research question:** How can the constraint‑assembly framework's insights be communicated to non‑specialists in a way that changes how they think about constraint, composition, and decision‑making?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Decision‑making guides for practitioners

**Method:**

1. Translate each concept into plain language with concrete examples
2. Develop case studies for each failure mode (soft term reliance, partial‑use destruction, diagnostic deferral)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the constraint‑assembly framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard decision‑making practice

---

### The Problem

In decision‑making research, things like option generation, constraint classification, and the distinction between selection and construction are not separate from the decision. They are direct, material, contributing factors to whether the decision is possible. When a study says "the decision was made," that is treated as a finding about the decision.

But the decision literature measures choice among alternatives. The naturalistic literature measures recognition of a candidate. Neither measures construction—the operation of building an option that did not exist in the environment, out of components each insufficient alone, under a fixed and irreversible budget. The same absence shows up from three directions, which suggests one missing instrument rather than three.

---

### Six Ways the Connection Gets Lost

#### 1. The "Selection as Default" Fallacy

Many decision frameworks treat selection as the default operation. If the study says "the decision was X," that is treated as a choice among presented alternatives.

But construction is not selection. It is the assembly of an option that did not exist in the environment. A case with no rejections reads as selection—and the tool says so. If the study says "decision made," it is not false for selection, but it may be false for construction. The operation type was causal—just not represented.

So "selection as default" often means "We assumed the decision was a choice." That is a framing error, not evidence that construction didn't happen.

#### 2. The "Constraint as Limit" Fallacy

Many frameworks treat constraints as limits on the option set. If the study says "constraints reduced options," that is treated as the finding.

But constraints are what makes composition computable. A term that will not move can be leaned on; a soft term cannot, because there is no way to know when the pieces add up. More hard constraints, more composition available. If the study says "constraints limit options," it is not false for the standard framing, but it may be false for the system. The enabling function was causal—just not represented.

So "constraint as limit" often means "We treated constraints as obstacles." That is a framing error, not evidence that constraints don't enable composition.

#### 3. The "Invariant and Consumable as One" Fallacy

Many frameworks treat resources as a single category. If the study says "resources were consumed," that is treated as a finding.

But invariant and consumable behave differently enough that merging them loses the failure mode. An invariant holds regardless of use; a consumable is destroyed by spending. Partial use of a consumable can be worse than none. If the study says "resources were consumed," it is not false for the consumable, but it may be false for the invariant. The class distinction was causal—just not represented.

So "invariant and consumable as one" often means "We treated all resources as consumable." That is a classification error, not evidence that invariants don't matter.

#### 4. The "Rejection as Optional" Fallacy

Many decision records omit rejected options. If the study says "the decision was X," that is treated as sufficient.

But a composed solution is only visible as composition if what was ruled out, and by which constraint, is recorded. Without rejections, the case reads as selection. If the study omits rejections, it is not false for the decision, but it may be false for the mechanism. The rejections were causal—just not represented.

So "rejection as optional" often means "We only recorded what was chosen." That is a recording error, not evidence that rejections don't matter.

#### 5. The "Cause as Prerequisite" Fallacy

Many frameworks treat knowing the cause as a prerequisite for action. If the study says "cause was unknown," that is treated as a failure.

But diagnostic deferral is recorded separately from assembly. Establishing what class of event this is spends the same budget the assembly needs. In grade-stop, the cause of the engine shutdown was unknown throughout and was explicitly quarantined until the vehicle stopped. If the study says "cause unknown = failure," it is not false for the diagnosis, but it may be false for the assembly. The deferral was causal—just not represented.

So "cause as prerequisite" often means "We assumed diagnosis must precede action." That is a timing error, not evidence that deferral is failure.

#### 6. The "Recognition as Construction" Fallacy

Many retrospective records treat recognition and construction as the same. If the study says "the solution was generated," that is treated as a finding.

But recognition‑primed selection and genuine construction look identical in a single‑instance retrospective record. Whether a composition was built during the event or recalled from prior route knowledge is not separable from any case currently in here. If the study says "solution generated," it is not false for the record, but it may be false for the mechanism. The recognition‑construction distinction was causal—just not represented.

So "recognition as construction" often means "We treated recall as assembly." That is a measurement error, not evidence that construction happened.

---

### What This Framework Does Differently

This framework treats decision‑making as potentially construction—the assembly of an option that did not exist in the environment, out of components each insufficient alone, under a fixed and irreversible budget. The following components document mechanisms that standard decision‑making practice typically drops:

- The reversal: Constraints enable composition, they do not limit it. More hard constraints, more composition available.
- Two constraint classes: invariant (holds regardless of use) and consumable (finite, destroyed by spending). Merging them loses the failure mode.
- Rejected candidates as the data: A composed solution is only visible as composition if rejections are recorded.
- Fail‑closed composition detection: composition_present fails when sufficiency is unknown, single sufficient, or unrecorded.
- Diagnostic quarantine: Cause deferral recorded separately from assembly.
- No verdict: No scoring of the operator. Every readout is a property of the recorded case.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
OPEN The question is named and remains open. Recognition vs. construction separability.
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Soft‑term reliance prevalence.
UNDEFINED The variable has no agreed definition or measurement protocol. Separator for recognition vs. construction.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Quantity values for grade-stop.

---

### What Is NOT a Valid Epistemic State

SELECTION_AS_DEFAULT is not a valid knowledge state. If a decision may be construction rather than selection, treating it as selection is a framing error, not an epistemic one. The operation does not care about our default assumptions.

The framework refuses to record a decision as selection without checking for rejections. Instead, it records the decision as unclassifiable—rejections absent, so selection not assembly—and names what would be needed to move it to a classified state.

---

### The Standard

The question should not be:

"What was the decision?"

But rather:

"Was this selection or construction? And if construction, what constraints enabled it?"

If the answer is that rejections are absent, the case is selection, not assembly. End of story.

The decision is already potentially construction. Our selection‑as‑default, constraint‑as‑limit, and recognition‑as‑construction assumptions are the only things pretending otherwise. And that pretense has produced a literature that measures choice and recognition while missing the operation that matters most under fixed budgets.

This framework does not pretend otherwise.
