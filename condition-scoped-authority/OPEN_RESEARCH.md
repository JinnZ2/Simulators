---

CLAIM_TABLE.md

Claims about the delivered condition-scoped-authority/ folder, about what a Python stdlib environment can establish concerning it, and about the enumeration protocol it inherits.

This is a checkable claim, not an arguable one. A total order over positions either does or does not reproduce a condition‑scoped authority table. rank_search() enumerates every total order—a complete search at these sizes, not a sample. The code does not simulate, does not measure, does not collect. It enumerates.

---

REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered design.

id claim status
CSA_001 A total order cannot represent a condition‑scoped authority table. rank_search() enumerates every total order over the protective‑detail positions (principal, bodyguard). 2 orders, 0 exact matches. Adding a third scoped position (extension) gives 6 orders, still 0 exact. SUPPORTED (by exhaustive enumeration)
CSA_002 The best ranking fails exactly where the stakes are highest. Principal‑on‑top gets 4 of 5 classes right (80%). The one class it misses is threat_live—the class in which the spec says the specialist holds total authority, including physical force against the principal's stated preference. SUPPORTED
CSA_003 Averaging over classes is the same error as scoring a facility on variables still being read. The classes are not interchangeable. An 80% score on a collapsed structure does not mean the structure is 80% correct—it means it is wrong on the load‑bearing class. SUPPORTED (by mechanism definition)
CSA_004 Adding scoped domains makes a rank fit worse, not better. With a third scoped position, all 6 orders are checked, still 0 exact, and the best is wrong on 2 classes instead of 1. Every domain with its own reading capacity is another class the single ranking must get wrong. SUPPORTED (by exhaustive enumeration)
CSA_005 Rank does not invert. holds() returns DECIDES or NOT_IN_DOMAIN—never a smaller quantity of the same thing. The spec is explicit that the domain is partitioned and that inside the partition the principal was never the decider. Modelling the threat case as "the guard outranks the principal" is already the error. SUPPORTED
CSA_006 The partition must be symmetric. Partition refuses a table where one position holds every class (a ranking written as a table) and refuses a position with no class at all (not a party to the arrangement, constrained by nothing, gaining for free). Neither party reads the other's domain. SUPPORTED
CSA_007 The collapsed structure states silently what nobody would defend if written down. Written out: "principal holds the reading capacity for all 5 condition classes simultaneously." Classes actually held: 4 of 5. Overclaimed: threat_live. Rank has no condition column, so a rank‑only structure says the same thing in every class. SUPPORTED
CSA_008 The coordinating organ is not senior to the others. It is a different organ, which cannot do what they do and cannot sense what they sense. Organ refuses to build a coordinator that senses everything, because such a thing is a hierarchy written in anatomy vocabulary. SUPPORTED
CSA_009 Reassignment by decree produces a non‑functioning system, not a degraded one. An organ reassigned to a task whose sense channel it does not have cannot read the input at all. Output is exactly zero, not a fraction. The failure lands downstream, where the decree cannot observe it. SUPPORTED
CSA_010 Scoring only the coordinating organ and reporting it as the whole system's capacity is the third instance of one recurring shape. Measure a subset, report it as the whole. The safety metric rising while the facility degrades is the same move. Recorded as one shape recurring, not as three findings. SUPPORTED
CSA_011 The claim about rubrics (consciousness, intelligence) is carried and not tested. organ.py has no rubric corpus and does not pretend to one. UNVERIFIED
CSA_012 The delivered code is stdlib‑only. condition_scope.py and organ.py import only from the Python standard library. Phone‑buildable, parses under 3.9. SUPPORTED
CSA_013 The delivered code is runnable. Both files execute and take --selftest. 30 / 25 checks, 55 in all, green. Samples pinned in samples/, byte‑reproducible. SUPPORTED
CSA_014 The vocabulary gap is real and named. Current EHS literature describes direct‑to‑CEO reporting as "strong" using soft verbs (visibility, seat at meetings, influence). There is no term distinguishing BOUND from ADVISORY. Both are called "authority." Any measurement using the word without stating which one is unsigned. SUPPORTED (by definition)
CSA_015 Three open questions are carried, not closed. No proposed method for restoring scope‑partition to a structure already collapsed to rank. Unknown whether BOUND authority survives outside regulated domains. If it survives only where a regulator forced it, that is itself the finding. OPEN
CSA_016 The justification is competence, not rights. The specialist holds authority because the reading capacity sits there. The principal's attention is committed elsewhere by design. Routing the decision upward adds latency and substitutes a worse instrument. It does not add judgment. SUPPORTED (by mechanism definition)

---

UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the condition‑scoped authority framework, organized by discipline

Every gap in this folder is a research question with:

· A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
· A falsifier (what would settle it)
· A data source (where to look)
· A method (how to answer it)
· An expected deliverable (what the undergraduate produces)

---

1. EMPIRICAL — BOUND Authority Prevalence

Gap: The spec asks: "unknown whether BOUND authority survives anywhere outside regulated domains (nuclear, aviation, protective detail). If it survives only where a regulator forced it, that is itself the finding."

Knowledge state: NOT_STUDIED

Research question: Does condition‑scoped (BOUND) authority exist outside regulated domains? If so, in what sectors and under what conditions? If not, is regulatory pressure the only thing that preserves it?

Disciplines: Organizational theory, public administration, regulatory studies

Data sources:

· Organizational charters and governance documents
· Regulatory frameworks (nuclear, aviation, healthcare, finance)
· Published case studies of authority allocation
· Industry surveys of decision‑making structures

Method:

1. Identify domains where BOUND authority is documented (nuclear, aviation, protective detail)
2. Survey other high‑stakes domains (healthcare, finance, emergency management)
3. For each domain, determine whether authority is condition‑scoped or collapsed to rank
4. Test whether regulatory pressure correlates with BOUND authority
5. Document the distribution

Expected deliverable: A prevalence map of BOUND authority across sectors, with regulatory correlation analysis.

Falsifier: BOUND authority is prevalent outside regulated domains (then regulatory pressure is not the preserving mechanism).

---

2. EMPIRICAL — Vocabulary Gap in EHS Literature

Gap: The spec states: "Current EHS literature describes direct‑to‑CEO reporting as the strong configuration, evidenced by: visibility, seat at executive meetings, influence on strategy. All soft verbs. There is no term distinguishing BOUND from ADVISORY."

Knowledge state: NOT_STUDIED

Research question: Does the EHS (Environment, Health, Safety) literature actually lack a term for BOUND vs. ADVISORY authority? If so, what is the distribution of these configurations in practice?

Disciplines: Occupational health and safety, organizational theory, regulatory studies

Data sources:

· EHS academic and practitioner literature
· Corporate EHS organizational charts
· EHS reporting structure surveys
· Regulatory guidance documents

Method:

1. Conduct a literature review of EHS authority and reporting structures
2. Extract descriptions of EHS authority configurations
3. Classify each as BOUND, ADVISORY, or collapsed
4. Test whether the literature distinguishes between them
5. Document the prevalence of each configuration

Expected deliverable: A literature review of EHS authority configurations, with classification and prevalence estimates.

Falsifier: The literature does distinguish BOUND from ADVISORY (then the vocabulary gap is narrower than claimed).

---

3. EMPIRICAL — Restoration Feasibility

Gap: The spec asks: "no proposed method for restoring scope‑partition to a structure already collapsed to rank."

Knowledge state: UNDEFINED

Research question: Can a structure that has been collapsed to rank be restored to a condition‑scoped partition? If so, under what conditions and at what cost?

Disciplines: Organizational design, change management, systems engineering

Data sources:

· Organizational restructuring case studies
· Change management literature
· Published organizational design frameworks
· Regulatory intervention case studies

Method:

1. Identify cases where organizations restored condition‑scoped authority
2. Document the restoration process and conditions
3. Identify success factors and barriers
4. Propose a restoration method
5. Test the method on a case study

Expected deliverable: A proposed method for restoring scope‑partition to a collapsed structure, with case study evidence.

Falsifier: No case of successful restoration can be found (then restoration is infeasible).

---

4. EMPIRICAL — The Protective Detail Partition

Gap: The protective‑detail partition (5 classes: clientele, finances, politics, schedule, threat_live) is a worked example. It is not validated against actual protective detail practice.

Knowledge state: NOT_STUDIED

Research question: Does the protective‑detail partition match actual Secret Service or protective detail practice? Are the condition classes correctly assigned?

Disciplines: Security studies, organizational theory, public administration

Data sources:

· Secret Service organizational documents (public)
· Protective detail manuals and protocols
· Published accounts of protective detail operations
· Interviews with protective detail professionals

Method:

1. Review public Secret Service and protective detail documentation
2. Identify the actual condition classes and authority assignments
3. Compare to the partition in the spec
4. Document discrepancies and their implications
5. Update the partition if warranted

Expected deliverable: A validated protective‑detail partition, with sources and discrepancy analysis.

Falsifier: The actual partition differs from the spec's partition (then the worked example needs updating).

---

5. EMPIRICAL — The Organ Error in Real Systems

Gap: organ.py defines the organ error: scoring only the coordinating organ and reporting the result as the whole system's capacity. The spec adds that this is "the same error as the centralized‑executive prior in consciousness and intelligence rubrics."

Knowledge state: NOT_STUDIED

Research question: Does the organ error actually occur in real systems? Are there documented cases where a coordinating organ was scored and the result reported as the whole system's capacity?

Disciplines: Organizational theory, systems engineering, AI safety

Data sources:

· Published case studies of organizational measurement
· AI safety and intelligence evaluation rubrics
· Corporate and government organizational assessments
· The operator-structure-echo/corroboration.py module

Method:

1. Identify documented cases of subset‑as‑whole measurement
2. Classify each case by domain and measurement type
3. Test whether the organ error pattern recurs
4. Document the prevalence and consequences
5. Compare to the operator-structure-echo prediction

Expected deliverable: A case study collection of organ errors, with prevalence and consequence analysis.

Falsifier: No documented cases of the organ error can be found (then the pattern is theoretical).

---

6. EMPIRICAL — Reassignment by Decree

Gap: organ.py states: "Instructing the hand to be a foot does not produce a degraded system, it produces a non‑functioning one. Output is exactly zero, not a fraction. The failure lands downstream, where the decree cannot observe it."

Knowledge state: NOT_STUDIED

Research question: Are there documented cases of reassignment by decree in real systems? Do they produce non‑functioning systems, and does the failure land downstream where the decree cannot observe it?

Disciplines: Organizational theory, systems engineering, public administration

Data sources:

· Organizational restructuring case studies
· Published accounts of failed reorganizations
· Government and corporate reorganization documents
· The organ.py simulation framework

Method:

1. Identify documented cases of reassignment by decree
2. For each case, determine whether the system became non‑functioning
3. Determine whether the failure was observable at the decree level
4. Document the conditions under which reassignment fails
5. Test the organ.py prediction against the cases

Expected deliverable: A case study analysis of reassignment by decree, with empirical test of the zero‑output prediction.

Falsifier: A case where reassignment produced a degraded system rather than a non‑functioning one (then the zero‑output prediction is falsified).

---

7. EMPIRICAL — Rank Collapse in Organizations

Gap: The core claim is that organizations collapse condition‑scoped authority to rank. The empirical prevalence of this collapse is not measured.

Knowledge state: NOT_STUDIED

Research question: What is the prevalence of rank collapse in organizations? What fraction of organizations that should have condition‑scoped authority have instead collapsed it to rank?

Disciplines: Organizational theory, public administration, sociology

Data sources:

· Organizational charters and governance documents
· Organizational survey data
· Published case studies of authority allocation
· Regulatory compliance documentation

Method:

1. Define criteria for rank collapse (authority held by position rather than condition class)
2. Sample organizations across sectors
3. Classify each organization as condition‑scoped, rank‑collapsed, or mixed
4. Compute prevalence estimates
5. Identify sector and size correlates

Expected deliverable: A prevalence estimate for rank collapse across sectors, with correlates.

Falsifier: Rank collapse is rare (< 10% of organizations) (then the core claim is not empirically supported).

---

8. EMPIRICAL — Competence‑Based Authority

Gap: The spec states: "The specialist holds the authority because the reading capacity sits there. The principal's attention is committed elsewhere by design." This is a claim about the justification for condition‑scoped authority.

Knowledge state: NOT_STUDIED

Research question: Is authority actually held where reading capacity sits? Or is authority held by position regardless of reading capacity?

Disciplines: Organizational theory, cognitive science, decision‑making

Data sources:

· Organizational decision‑making studies
· Published cases of authority allocation
· Expert interviews with decision‑makers
· The condition_scope.py partition framework

Method:

1. Identify decision domains with clear reading‑capacity differences
2. Measure where authority is actually held
3. Compare to where reading capacity sits
4. Test whether authority tracks reading capacity or position
5. Document the alignment or misalignment

Expected deliverable: An empirical test of the competence‑based authority claim, with alignment metrics.

Falsifier: Authority does not track reading capacity (then the justification is not empirically supported).

---

9. EMPIRICAL — The Third Scoped Position

Gap: The extension with a third scoped position is marked "not delivered." The code checks all 6 orders and finds 0 exact matches.

Knowledge state: NOT_STUDIED

Research question: What is the third scoped position? What condition class does it read? How does adding it change the partition?

Disciplines: Organizational theory, security studies, systems design

Data sources:

· The protective‑detail domain
· Published protective detail structures
· The condition_scope.py extension code

Method:

1. Identify the third scoped position from the code or spec
2. Define its condition class and reading capacity
3. Add it to the partition
4. Run the exhaustive search
5. Document the new failure pattern

Expected deliverable: A completed third‑position extension, with exhaustive search results.

Falsifier: The third position produces an exact match (then the core claim is falsified for that partition).

---

10. USER GUIDE — Non‑Specialist Translation

Gap: The framework is documented for researchers but not for non‑specialists (policymakers, organizational designers, general public).

Knowledge state: NOT_STUDIED

Research question: How can the condition‑scoped authority framework's insights be communicated to non‑specialists in a way that changes how they think about authority and organizational design?

Disciplines: Science communication, organizational design, policy

Data sources:

· The framework itself
· Published science communication research
· Organizational design guides

Method:

1. Translate each concept into plain language with concrete examples
2. Develop case studies for each failure mode (rank collapse, organ error, reassignment)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

Expected deliverable: A non‑technical user guide to the condition‑scoped authority framework.

Falsifier: Non‑specialists find the guide unhelpful or incomprehensible.

---

SCOPE_BOUNDARY.md

Why this framework is broader than standard authority and organizational design practice

---

The Problem

In organizational design and authority theory, things like condition classes, reading capacity, and the distinction between BOUND and ADVISORY authority are not separate from the structure. They are direct, material, contributing factors to whether the structure can represent the system. When an org chart says "X reports to Y," that is treated as a description of authority.

But a total order over positions cannot represent a condition‑scoped authority table. Rank has no condition column. The structure then asserts that the top of the hierarchy holds every domain's reading capacity simultaneously. Nobody would defend that claim if it were written down. The structure states it silently.

---

Six Ways the Connection Gets Lost

1. The "Org Chart as Description" Fallacy

Many organizational analyses treat the org chart as a description of authority. If the chart says "X reports to Y," that is treated as a fact about who decides.

But a reporting line is a total order. It has no condition column. If authority is condition‑scoped, the org chart cannot represent it. The chart is not a description; it is a collapse. If the analysis says "X reports to Y," it is not false for the reporting line, but it may be false for the authority. The condition scope was causal—just not represented.

So "org chart as description" often means "We treated the reporting line as the authority." That is a representational error, not evidence that authority follows the reporting line.

2. The "Rank as Inversion" Fallacy

Many analyses treat authority as a rank that can invert. If the specialist decides in an emergency, that is treated as "the specialist outranks the principal."

But rank does not invert. The domain is partitioned, and inside that partition the principal was never the decider. Modelling the threat case as "the guard outranks the principal" is already the error. If the analysis says "rank inverted," it is not false for the inversion model, but it may be false for the system. The partition was causal—just not represented.

So "rank as inversion" often means "We modelled a partition as a ranking." That is a structural error, not evidence that rank inverts.

3. The "Authority as Quantity" Fallacy

Many analyses treat authority as a quantity that can be measured on a single scale. If one position has more authority, that is treated as a description.

But holds() returns DECIDES or NOT_IN_DOMAIN—never a smaller quantity of the same thing. A position either decides in a domain or it does not. There is no "partial authority." If the analysis says "X has 80% authority," it is not false for the quantity model, but it may be false for the system. The partition was causal—just not represented.

So "authority as quantity" often means "We treated a partition as a distribution." That is a measurement error, not evidence that authority is quantifiable.

4. The "Coordinator as Senior" Fallacy

Many analyses treat the coordinating organ as senior to the others. If the coordinator coordinates, that is treated as evidence of higher rank.

But the coordinating organ is not senior to the others. It is a different organ, which cannot do what they do and cannot sense what they sense. Coordination is a specialization, not a rank. If the analysis says "the coordinator is senior," it is not false for the coordination role, but it may be false for the system. The specialization was causal—just not represented.

So "coordinator as senior" often means "We treated a specialization as a rank." That is a categorical error, not evidence that coordination implies seniority.

5. The "Reassignment as Degradation" Fallacy

Many analyses treat reassignment as producing a degraded system. If the hand is told to be a foot, that is treated as a performance reduction.

But reassignment by decree produces a non‑functioning system, not a degraded one. An organ reassigned to a task whose sense channel it does not have cannot read the input at all. Output is exactly zero, not a fraction. If the analysis says "degraded performance," it is not false for the degradation model, but it may be false for the system. The zero output was causal—just not represented.

So "reassignment as degradation" often means "We assumed partial performance is possible." That is a modelling error, not evidence that degradation is the outcome.

6. The "Subset as Whole" Fallacy

Many analyses measure a subset and report it as the whole. If the coordinating organ scores well, that is treated as evidence that the system is functioning.

But scoring only the coordinating organ and reporting it as the whole system's capacity is the same error as the safety metric rising while the facility degrades. The subset is not the whole. If the analysis says "the system is functioning," it is not false for the subset, but it may be false for the system. The subset‑as‑whole was causal—just not represented.

So "subset as whole" often means "We measured what was easy and called it the system." That is a measurement error, not evidence that the subset represents the whole.

---

What This Framework Does Differently

This framework treats authority as condition‑scoped—held by a position for a class of condition—and treats rank and scope as different objects that cannot be collapsed. The following components document mechanisms that standard authority and organizational design practice typically drops:

· condition_scope.py — Exhaustive enumeration of every total order. A total order over positions either does or does not reproduce a condition‑scoped authority table. rank_search() checks every order. NO_RANK_REPRESENTS_IT.
· organ.py — The coordinating organ is a specialization, not a rank. Reassignment by decree produces zero output, not degradation. Scoring the coordinator and reporting it as the whole is the subset‑as‑whole error.
· The partition constraint — Partition refuses a table where one position holds every class (a ranking written as a table) and refuses a position with no class at all. Neither party reads the other's domain.
· The vocabulary gap — BOUND and ADVISORY are both called "authority." Any measurement using the word without stating which one is unsigned.

---

The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Prevalence of BOUND authority outside regulated domains.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Whether BOUND authority survives only where a regulator forced it.
UNDEFINED The variable has no agreed definition or measurement protocol. Method for restoring scope‑partition to a collapsed structure.
OPEN The question is named and remains open. The three open questions in SPEC_CONDITION_SCOPE.md.

---

What Is NOT a Valid Epistemic State

ORG_CHART_AS_AUTHORITY is not a valid knowledge state. If a total order cannot represent a condition‑scoped partition, treating the org chart as a description of authority is a representational error, not an epistemic one. The condition scope does not care about our org charts.

The framework refuses to record a reporting line as authority. Instead, it records the structure as collapsed—a total order standing in for a partition—and names what would be needed to move it to a represented state.

---

The Standard

The question should not be:

"What does the org chart say?"

But rather:

"Does this structure represent the condition classes, or has it collapsed them to rank?"

If the answer is that the structure has no condition column, it does not represent the authority. End of story.

The authority is already condition‑scoped. Our org charts, rankings, and subset measurements are the only things pretending otherwise. And that pretense has produced structures that state silently what nobody would defend if written down.

This framework does not pretend otherwise.
