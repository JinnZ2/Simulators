---

## CLAIM_TABLE.md

Claims about the delivered conversation‑type/ folder, about what a Python stdlib environment can establish concerning it, and about the self‑audit protocol it inherits from the blame‑attribution and anchor‑interval folders.

This is a marker, not a measurement. No driving data is collected. No incident database is queried. The arithmetic is checkable without any driving data. The marker's design moves — residue window, binary typing, self‑instance — are quantified against the marker's own stated mechanism.

---

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

| id | claim | status |
|---|---|---|
| `CT_001` | The residue window is the marker's strongest move and it is quantifiable. If arousal decays with time constant τ after a call ends, the share of total excess exposure falling outside a call‑window measurement is computable. A 5‑minute call with a 15‑minute decay puts 75% of the exposure outside the window. The shorter the call, the worse it gets — and short calls are the common case. | SUPPORTED (as arithmetic on the marker's own mechanism) |
| `CT_002` | The binary costs about 15%, and the marker's own case list is why that is affordable. Suspendability is graded — dropping a call at a natural pause vs. mid‑sentence are not the same debt, and a dispatch call carries employment debt a spouse call does not. Binarising attenuates to ~86% of the graded signal on a uniform spread, ~97% on a bimodal one. The marker's three‑state list is bimodal in shape: an obligated call and a podcast are not near a boundary. | SUPPORTED |
| `CT_003` | The binary is the right instrument choice for P4 for a reason the arithmetic misses. A graded scale that cannot be typed at 70 mph is worse than a binary that can. The statement is conditional, and the conditional is the finding — the binary is cheap if the distribution is bimodal, and whether it is, is an empirical question P4 answers on the way to the main one. | SUPPORTED |
| `CT_004` | "Three states, one regulatory bin" is one bin short. States 1 (emotional/obligated) and 2 (intellectual/unobligated) are in the distraction rules; state 3 (silence, vigilance decrement) is not. Vigilance decrement is governed by hours‑of‑service, a separate instrument with its own logic. So there are two bins and they do not talk to each other, which is worse than stated and in the direction the marker cares about. | SUPPORTED (correction in the marker's favour) |
| `CT_005` | The adjacent finding — the desk‑worker default prior — is checkable against the session transcript. The marker states: "Instance: this session. Applied twice, corrected twice." A scan of the session transcript with 26 search patterns returns 3 hits — Office and isolate — and every hit so far has been a different sense of the term. The bounded null holds on adjudication and does not hold on the raw count. | SUPPORTED (with limits stated harder than the result) |
| `CT_006` | The scan does not establish that the marker is about this Claude Code session. Content has been relayed from other Claude sessions in this one, twice, marked 'from claude:'. A keyword scan is stepped around by any paraphrase. So the null is bounded, not closed. | SUPPORTED (limits stated) |
| `CT_007` | The marker's arousal channel is distinct from cognitive load, and the two are currently collapsed into one category. Cognitive load competes for road‑relevant resources; emotional arousal occupies the system rather than competing for a slice of it. Arousal degrades spatial reasoning specifically — which for an 80,000 lb vehicle on grade is the safety‑critical channel. | SUPPORTED (by mechanism definition) |
| `CT_008` | The vigilance‑decrement literature has never been connected to conversation type. Steady‑pace verbal reasoning with no stake and no obligation does not spike arousal and can counter vigilance decrement. That is established in the literature, but never connected to conversation type. | SUPPORTED (as a stated gap) |
| `CT_009` | The delivered code is stdlib‑only. design_check.py imports only json, math, os, random, re, sys. | SUPPORTED |
| `CT_010` | The delivered code is runnable. python3 design_check.py --selftest passes all checks. | SUPPORTED |
| `CT_011` | No submission path exists to say so. The reporting‑gap shape with a different payload. The arousal findings exist, the vigilance findings exist, but neither literature reaches motor carrier rulemaking. | SUPPORTED (as a stated gap) |
| `CT_012` | Interest is declared, and it runs the other way this time. The two previous markers in this family made claims favourable to this author's class; the adjacent finding here is unfavourable. Accepting it is the humble move; rejecting it is the interested one. | SUPPORTED |

---

## OPEN_QUESTIONS.md

Open questions in the conversation‑type framework, organized by discipline

Every gap in this folder is a research question with:

- A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
- A falsifier (what would settle it)
- A data source (where to look)
- A method (how to answer it)
- An expected deliverable (what the undergraduate produces)

---

### 1. EMPIRICAL — Arousal Decay Time Constant (P1)

**Gap:** The residue window arithmetic uses τ values (5, 15, 30 min) as placeholders. τ is unmeasured — P1 and P3 are what would estimate it.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What is the actual decay time constant of emotional arousal after an obligated conversation? Does it vary by conversation type, and does it persist beyond the call window?

**Disciplines:** Psychophysiology, cognitive psychology, human factors

**Data sources:**

- Heart rate variability (HRV) by conversation class, in‑cab (P1)
- Published studies on emotional arousal decay
- Simulator studies with post‑arousal hazard detection latency (P3)

**Method:**

1. Design an in‑cab study with HRV monitoring during and after calls
2. Classify calls by suspendability (obligated vs. unobligated)
3. Measure HRV recovery time after call termination
4. Fit an exponential decay model to estimate τ
5. Test whether τ varies by call class

**Expected deliverable:** An empirical estimate of τ for obligated and unobligated calls, with confidence intervals.

**Falsifier:** τ ≈ 0 (arousal decays instantly) — which would put the exposure back inside the call window and make the existing measurement design correct.

---

### 2. EMPIRICAL — Incident Data Cross‑Reference (P2)

**Gap:** The marker proposes P2: incident data cross‑referenced against call type in the preceding 30 min (residue window, not call window). No such study exists.

**Knowledge state:** NOT_STUDIED

**Research question:** Does the presence of an obligated call in the 30 minutes preceding an incident correlate with incident risk? Does the correlation disappear when using a call‑window measurement?

**Disciplines:** Transportation safety, epidemiology, crash analysis

**Data sources:**

- Motor carrier incident databases (FMCSA, state DOTs)
- Call detail records (CDRs) from fleet telematics
- Driver logs and dispatch records

**Method:**

1. Identify incidents with known timestamp and driver
2. Extract call records for the 30 minutes preceding the incident
3. Classify calls by suspendability (obligated vs. unobligated)
4. Compare to a control window (e.g., same time previous day)
5. Test whether obligated‑call exposure predicts incident risk

**Expected deliverable:** An odds ratio for incident risk associated with obligated‑call exposure in the residue window.

**Falsifier:** No correlation between obligated‑call exposure and incident risk (then the residue window is not load‑bearing).

---

### 3. EMPIRICAL — Hazard Detection Latency Post‑Arousal (P3)

**Gap:** The marker proposes P3: hazard detection latency, post‑arousal, on a simulator. No such study has been conducted with conversation type as the independent variable.

**Knowledge state:** NOT_STUDIED

**Research question:** Does hazard detection latency increase after an obligated conversation, and does it persist beyond the call window? How does it compare to unobligated conversation and silence?

**Disciplines:** Cognitive psychology, human factors, driving simulation

**Data sources:**

- Driving simulator studies with conversation manipulation
- Published hazard detection latency literature
- The arousal literature (attentional narrowing, spatial reasoning degradation)

**Method:**

1. Design a simulator study with three conditions: obligated conversation, unobligated conversation, silence
2. Measure hazard detection latency before, during, and after each condition
3. Test whether latency is elevated post‑arousal
4. Test whether the elevation decays with time
5. Compare to the residue window predictions

**Expected deliverable:** A post‑arousal hazard detection latency curve, with decay time constant.

**Falsifier:** No post‑arousal elevation (then the arousal mechanism is not load‑bearing).

---

### 4. EMPIRICAL — Suspendability Distribution (P4)

**Gap:** The marker proposes P4: self‑report of call class, driver‑tallied — no cooperation needed to run. The distribution of suspendability in real fleets is unknown.

**Knowledge state:** UNKNOWN_ATM

**Research question:** What is the empirical distribution of call suspendability in commercial motor carrier operations? Is it bimodal (as the marker assumes) or uniform?

**Disciplines:** Transportation safety, survey methodology, fleet operations

**Data sources:**

- Driver self‑reports of call class (P4)
- Fleet call logs and dispatch records
- Driver interviews and focus groups

**Method:**

1. Design a simple driver‑tallied log: binary classification of each call (obligated vs. unobligated)
2. Deploy in a fleet for a defined period
3. Collect and aggregate the data
4. Test whether the distribution is bimodal or uniform
5. Compute the recovered correlation for the binary instrument (CT_002)

**Expected deliverable:** An empirical distribution of suspendability in a real fleet, with bimodality test.

**Falsifier:** The distribution is uniform (then the binary instrument loses ~15% of the signal, and the marker's defence is weakened)

---

### 5. EMPIRICAL — Regulatory Bin Mapping

**Gap:** CT_004 states that "three states, one regulatory bin" is one bin short. States 1 and 2 are in the distraction rules; state 3 is in hours‑of‑service.

**Knowledge state:** NOT_STUDIED

**Research question:** How do the current regulatory instruments (distraction rules, hours‑of‑service) actually map to the three conversation states? Is there a gap where a driver who eliminates conversation to comply with distraction rules moves toward state 3, which those rules do not measure?

**Disciplines:** Regulatory policy, transportation safety, public administration

**Data sources:**

- FMCSA distraction rules (handheld vs. hands‑free, texting)
- Hours‑of‑service regulations (drive time limits, rest breaks)
- Regulatory guidance and interpretations
- Industry compliance data

**Method:**

1. Map each conversation state to the relevant regulatory instrument
2. Identify gaps where no instrument applies
3. Test whether the gap creates perverse incentives (e.g., eliminating conversation → vigilance decrement)
4. Propose regulatory updates to close the gap

**Expected deliverable:** A regulatory gap analysis for conversation‑type regulation, with proposed updates.

**Falsifier:** The current regulatory instruments already cover all three states (then the gap does not exist).

---

### 6. EMPIRICAL — Desk‑Worker Default Prior Prevalence

**Gap:** The adjacent finding states: "General‑advice corpora appear to assume a default subject: seated, low physical risk, socially isolated, for whom more social contact is the correction. Advice is emitted against that default regardless of stated operating conditions."

**Knowledge state:** NOT_STUDIED

**Research question:** How prevalent is the desk‑worker default prior in general‑advice corpora? Does it persist across domains and contexts?

**Disciplines:** Computational linguistics, corpus linguistics, social epistemology

**Data sources:**

- General‑advice corpora (e.g., Reddit advice, self‑help literature, LLM outputs)
- The session transcript (for the self‑instance check)
- Published studies on default assumptions in advice‑giving

**Method:**

1. Define the desk‑worker default prior operationally
2. Scan a corpus of general‑advice texts for evidence of the prior
3. Test whether the prior persists across domains
4. Test whether the prior is applied regardless of stated operating conditions
5. Document the prevalence and conditions

**Expected deliverable:** A prevalence estimate for the desk‑worker default prior in general‑advice corpora.

**Falsifier:** The prior is rare (< 5% of advice instances) (then the adjacent finding is not load‑bearing).

---

### 7. EMPIRICAL — Conversation Type and Spatial Reasoning

**Gap:** The marker states that arousal degrades spatial reasoning specifically, and that for an 80,000 lb vehicle on grade, spatial reasoning is the safety‑critical channel.

**Knowledge state:** UNDER_STUDY

**Research question:** Does emotional arousal specifically degrade spatial reasoning, and does the degradation persist after the arousal source is removed? How does this compare to cognitive load?

**Disciplines:** Cognitive psychology, neuroscience, human factors

**Data sources:**

- Published studies on arousal and spatial reasoning
- Neuroimaging studies of emotional vs. cognitive load
- Driving simulator studies with spatial reasoning tasks

**Method:**

1. Design a study with three conditions: emotional arousal, cognitive load, control
2. Measure spatial reasoning performance before, during, and after each condition
3. Test whether arousal specifically degrades spatial reasoning
4. Test whether the degradation persists after the arousal source is removed
5. Compare to cognitive load effects

**Expected deliverable:** A dissociation between arousal and cognitive load effects on spatial reasoning, with persistence measures.

**Falsifier:** Arousal does not specifically degrade spatial reasoning (then the marker's mechanism is not supported).

---

### 8. EMPIRICAL — Vigilance Decrement and Conversation

**Gap:** The marker states that steady‑pace verbal reasoning with no stake and no obligation can counter vigilance decrement. This is established in the vigilance‑decrement literature but never connected to conversation type.

**Knowledge state:** NOT_STUDIED

**Research question:** Does unobligated conversation reduce vigilance decrement during long drives? What is the optimal conversation type and timing?

**Disciplines:** Human factors, cognitive psychology, transportation safety

**Data sources:**

- Vigilance‑decrement literature (Mackworth, etc.)
- Driving simulator studies with conversation manipulation
- Hours‑of‑service and fatigue research

**Method:**

1. Design a long‑duration driving simulator study with three conditions: unobligated conversation, silence, obligated conversation
2. Measure vigilance (hazard detection, lane keeping) over time
3. Test whether unobligated conversation slows the vigilance decrement
4. Test whether obligated conversation accelerates it
5. Identify optimal conversation characteristics

**Expected deliverable:** A vigilance‑decrement curve for each conversation condition, with optimal conversation parameters.

**Falsifier:** Unobligated conversation does not slow vigilance decrement (then the marker's claim is not supported).

---

### 9. EMPIRICAL — Population Exposure Scaling

**Gap:** The marker states: "Consequence scales with mass. The exposed population is the one where the outcome of degraded spatial reasoning is an 80,000 lb vehicle in a curve on a grade."

**Knowledge state:** NOT_STUDIED

**Research question:** What is the population exposure to obligated conversation in commercial motor carrier operations? How does it scale with fleet size, route type, and hours?

**Disciplines:** Transportation safety, epidemiology, fleet operations

**Data sources:**

- Fleet call logs and dispatch records
- Driver hours‑of‑service records
- Route and grade data (GIS)
- Incident and near‑miss databases

**Method:**

1. Identify the population of commercial motor carrier drivers
2. Estimate the fraction of drive time spent in obligated conversation
3. Estimate the fraction of drive time spent on grades
4. Compute the exposure product: obligated conversation × grade time
5. Scale to fleet size and incident rates

**Expected deliverable:** A population exposure estimate for obligated conversation on grade, with scaling to incident risk.

**Falsifier:** The exposure product is negligible (< 1% of drive time) (then the mechanism is not load‑bearing for the population).

---

### 10. METHODOLOGICAL — The Two Bins, Not Talking

**Gap:** CT_004 states that there are two regulatory bins (distraction rules and hours‑of‑service) and they do not talk to each other.

**Knowledge state:** UNDEFINED

**Research question:** How should the two regulatory instruments be integrated to address the full conversation‑type space? What would a unified instrument look like?

**Disciplines:** Regulatory policy, systems engineering, public administration

**Data sources:**

- FMCSA distraction rules
- Hours‑of‑service regulations
- Regulatory integration case studies
- Published regulatory design frameworks

**Method:**

1. Define the full conversation‑type space (3 states × 2 instruments)
2. Identify the gaps and overlaps in the current regulatory structure
3. Design a unified instrument that covers all three states
4. Test the design against regulatory feasibility criteria
5. Propose a regulatory update

**Expected deliverable:** A proposed unified regulatory instrument for conversation‑type management in commercial motor carriers.

**Falsifier:** The current instruments already cover all three states when interpreted together (then integration is not needed).

---

### 11. USER GUIDE — Non‑Specialist Translation

**Gap:** The framework is documented for researchers but not for non‑specialists (drivers, fleet managers, policymakers).

**Knowledge state:** NOT_STUDIED

**Research question:** How can the conversation‑type framework's insights be communicated to non‑specialists in a way that changes how they think about conversation and driving safety?

**Disciplines:** Science communication, policy, education

**Data sources:**

- The framework itself
- Published science communication research
- Driver safety training materials

**Method:**

1. Translate each concept into plain language with concrete examples
2. Develop case studies for each conversation state
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences (drivers, fleet managers)
5. Iterate based on feedback

**Expected deliverable:** A non‑technical user guide to the conversation‑type framework.

**Falsifier:** Non‑specialists find the guide unhelpful or incomprehensible.

---

## SCOPE_BOUNDARY.md

Why this framework is broader than standard conversation‑and‑driving practice

---

### The Problem

In conversation‑and‑driving research, things like conversation type, suspendability, arousal residue, and the distinction between cognitive load and emotional occupancy are not separate from the measured effect. They are direct, material, contributing factors to whether a conversation is hazardous. When a study says "hands‑free is safe," that is treated as a finding about the channel.

But the channel is not the variable. Same phone, same channel, two conversations produce entirely different attention states. The regulatory category (handheld vs. hands‑free) is not the actual variable. The actual variable is suspendability without debt — whether the exchange can be dropped mid‑sentence with nothing owed on return.

---

### Six Ways the Connection Gets Lost

#### 1. The "Channel as Variable" Fallacy

Many conversation‑and‑driving studies treat the channel (handheld vs. hands‑free) as the independent variable. If the study says "hands‑free is safe," that is treated as a finding.

But the channel is not the variable. Same phone, same channel, two conversations produce entirely different attention states. A call with a spouse about a sick child is not the same as a call with a colleague about a schedule. The regulatory category collapses both. If the study says "hands‑free is safe," it is not false for the channel, but it may be false for the conversation type. The conversation type was causal—just not represented.

So "channel as variable" often means "We measured the device, not the conversation." That is a measurement error, not evidence that hands‑free is safe.

#### 2. The "Call Window as Measurement Window" Fallacy

Many studies measure distraction during the call. If the study says "no effect during the call," that is treated as evidence of safety.

But the effect may land after the call. Arousal persists. Emotional occupancy continues. The shorter the call, the worse it gets — and short calls are the common case. A five‑minute call with a fifteen‑minute decay puts three quarters of the exposure outside the window. If the study measures only during the call, it is looking at the minority of the effect. The residue window was causal—just not represented.

So "call window as measurement window" often means "We assumed the effect ends with the call." That is a temporal error, not evidence that the effect is contained.

#### 3. The "Cognitive Load as Complete" Fallacy

Many studies treat cognitive load as the complete mechanism. If the study says "cognitive load explains distraction," that is treated as the mechanism.

But arousal is distinct from cognitive load. Cognitive load competes for road‑relevant resources; emotional arousal occupies the system rather than competing for a slice of it. Arousal degrades spatial reasoning specifically. For an 80,000 lb vehicle on grade, spatial reasoning is the safety‑critical channel. If the study measures only cognitive load, it misses the arousal mechanism. The arousal channel was causal—just not represented.

So "cognitive load as complete" often means "We assumed arousal is a subset of load." That is a mechanistic error, not evidence that arousal doesn't matter.

#### 4. The "Three States, One Bin" Fallacy

Many regulatory frameworks treat conversation as a single category. If the regulation says "no handheld devices," that is treated as sufficient.

But there are three states, not one. State 1: emotional/obligated — arousal high, residue after. State 2: intellectual/unobligated — arousal flat, suspendable. State 3: silence, hour nine — vigilance decrement. States 1 and 2 are in the distraction rules; state 3 is in hours‑of‑service. Two bins, not talking to each other. A driver who eliminates conversation to comply with distraction rules moves toward state 3, which those rules do not measure. If the regulation says "no handheld devices," it is not false for the device, but it may be false for the system. The three‑state structure was causal—just not represented.

So "three states, one bin" often means "We collapsed the states." That is a categorical error, not evidence that the states are equivalent.

#### 5. The "Binary as Mistake" Fallacy

Many researchers treat binarising a graded quantity as a mistake. If the study says "the binary attenuates the signal," that is treated as a criticism.

But the binary is not a mistake: a graded scale that cannot be typed at 70 mph is worse than a binary that can. The binary is cheap if the distribution is bimodal, and whether it is, is an empirical question. If the study criticises the binary, it is not false for the attenuation, but it may be false for the operational constraint. The operational constraint was causal—just not represented.

So "binary as mistake" often means "We assumed the graded quantity is measurable." That is an operational error, not evidence that the binary is invalid.

#### 6. The "Desk‑Worker Default Prior" Fallacy

Many general‑advice corpora assume a default subject: seated, low physical risk, socially isolated, for whom more social contact is the correction. Advice is emitted against that default regardless of stated operating conditions.

Where the operating condition is an 80,000 lb vehicle in motion, the default inverts: social contact during the shift is the hazard, and unobligated reasoning is the mitigation. If the advice says "more social contact," it is not false for the desk worker, but it may be false for the driver. The default prior was causal—just not represented.

So "desk‑worker default prior" often means "We assumed the default subject applies." That is a contextual error, not evidence that the advice generalises.

---

### What This Framework Does Differently

This framework treats conversation type — suspendability without debt — as the load‑bearing variable, and treats the channel, the call window, cognitive load, and the regulatory bins as secondary or mis‑specified. The following components document mechanisms that standard conversation‑and‑driving practice typically drops:

- The residue window: Measure in the 30 minutes AFTER the call, not during. The arithmetic shows that a call‑window measurement is looking at the minority of the effect.
- The binary instrument: Suspendability is graded, but the binary is the right choice for P4 because a graded scale cannot be typed at 70 mph.
- The arousal channel: Distinct from cognitive load. Occupies the system rather than competing for a slice. Degrades spatial reasoning specifically.
- Three states, two bins: States 1 and 2 are in distraction rules; state 3 is in hours‑of‑service. They do not talk to each other.
- The desk‑worker default prior: General‑advice corpora assume a default subject for whom more social contact is the correction. The prior does not carry a context check.

---

### The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. The arousal decay time constant τ.
UNDER_STUDY Data collection is in progress; value is provisional. The suspendability distribution.
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Incident data cross‑referenced against residue window.
UNDEFINED The variable has no agreed definition or measurement protocol. The unified regulatory instrument.

---

### What Is NOT a Valid Epistemic State

CHANNEL_AS_VARIABLE is not a valid knowledge state. If the channel is not the variable, treating it as such is a measurement error, not an epistemic one. The conversation does not care about our device classifications.

The framework refuses to record a channel as the variable. Instead, it records the conversation type as the variable — suspendability without debt — and names what would be needed to move it to a measured state.

---

### The Standard

The question should not be:

"Was the driver using a handheld device?"

But rather:

"Was the conversation suspendable without debt, and did it produce arousal that persists after the call?"

If the answer is that the conversation was obligated and arousing, the hazard is real — and it is not measured by current instruments. End of story.

The conversation is already typed by its suspendability and arousal. Our channels, call windows, cognitive‑load measures, and regulatory bins are the only things pretending otherwise. And that pretense has produced a literature of null effects that may be measuring the wrong thing.

This framework does not pretend otherwise.
