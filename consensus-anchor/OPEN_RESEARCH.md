---

CLAIM_TABLE.md

Claims about the delivered consensus-anchor/ folder, about what a Python stdlib environment can establish concerning it, and about the ambiguity protocol it inherits.

This is a run of the text‑free arm, not evidence about trained language models. H1 (inherited norm) and H2 (objective) need a trained model and are untouched. The arm tests H3 alone—structural coupling, on a symbolic‑agent population with no corpus anywhere in the pipeline. Nothing here is evidence about trained language models.

---

REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the claim, never the delivered spec or the instrument.

id claim status
CA_001 The design is right and the text‑free arm is the right first move: cheap, needs no model, and H3 alone predicts its signature. SUPPORTED
CA_002 The update rule sentence has two readings and they give opposite verdicts on H3. Under DIST, all three limbs of H3's falsifier fire; under SAMPLED, none does. SUPPORTED
CA_003 The mechanism is exact, not statistical: under the DIST reading, the population mean is invariant to machine precision, so the population reaches total agreement and zero consensus. SUPPORTED
CA_004 J_c is not a property of J. It moves with noise, and the spec has no noise term. SUPPORTED
CA_005 A swept hysteresis gap is not evidence of bistability. The control is the gap across sweep rates, and the spec does not name it. SUPPORTED
CA_006 The chance baseline is not 1/K. Using 1/K manufactures a J_c. The measured chance baseline is 17.8% higher than 1/K. SUPPORTED
CA_007 My first run's null was my parameter choice, not a result. Run at eta = 0.10, T = 80, it cleared threshold by 0.004 with a seed SD of 0.05. At eta = 0, T = 400, the same rule reaches 0.88. SUPPORTED
CA_008 H3's locus is "interaction topology + coupling strength" and the arm as specified sweeps only J. Topology is untested. SUPPORTED
CA_009 The instrument caution in the drop is a real design rule and is the one part this arm cannot exercise. No cases, no records—every number is generated in‑process. UNVERIFIED (by design)

---

CA_002 — one sentence, two readings, opposite verdicts

The arm's update rule is specified as: "weighted mix of own prior and sampled peer positions."

Two readings, both defensible:

· DIST: the peer signal is the mean of peers' distributions
· SAMPLED: the peer signal is the empirical distribution of peers' sampled positions

SAMPLED is the more literal reading—a position is a discrete value, and the sentence says sampled peer positions. DIST is what you get if "position vector" is read as the object being mixed.

H3's stated falsifier, limb by limb, at eta = 0:

limb DIST SAMPLED
no alignment at any J True False
no J_c True False
no hysteresis True False

The limbs are joined by OR, so any one firing falsifies H3 as written. Under DIST all three fire. Under SAMPLED none does.

So the arm the drop calls "the fastest discriminator" discriminates—and what it discriminates on is an implementation choice the spec does not make.

Falsifier: a third reading of the sentence that gives a third verdict, or an argument that one reading is not admissible.

---

CA_003 — total agreement, zero consensus

Under DIST, the update is:

```
p ← (1−J)p + J·mean(p)
```

so the population mean maps to itself: (1−J)·mean + J·mean = mean. It is exactly invariant.

Measured over 200 steps:

metric DIST SAMPLED
population‑mean drift 4.11e-15 7.42e-01
modal mass of agreed distribution 0.267 (≈ chance) 0.962

Both reach total agreement—agent spread exactly 0.0—and they agree on different things. Under DIST, every agent ends holding an identical distribution, that distribution is the one the population started with, and because it is near‑uniform, the expressed positions stay at chance forever, at every J, every noise level, every run length tested.

That is a distinction the spec's order parameter cannot see. m is the fraction on the modal position; DIST produces agreement on a distribution. Full agreement and zero consensus are the same reading on m.

Worth stating for the model‑side arms too: a measurement showing units agreeing is not a measurement showing them converging on a position.

Falsifier: a DIST run where m departs from chance—which would mean the invariance argument is wrong, and it is checkable in one line.

---

CA_004 — J_c moves with the noise the spec does not have

J_c under SAMPLED, at the same grid and the same measured baseline:

eta J_c
0.00 0.15
0.02 0.50
0.10 0.90

A threshold in coupling is a ratio of coupling to noise. With no noise term, any J > 0 aligns eventually and the threshold sits at 0+; with enough noise, the threshold leaves the grid.

The spec sweeps J, lists J = 0 as the isolated control, and names no noise parameter—so "the coupling value at which m departs from chance" has no value until noise is fixed.

eta = 0 is not no noise: under SAMPLED, the coupling channel carries intrinsic sampling noise, which is the whole mechanistic difference from DIST. That is why eta = 0 is the arm where the transition is sharpest, rather than the arm where it disappears.

Falsifier: a J_c invariant across eta.

---

CA_005 — a hysteresis gap is not bistability, and the control is missing

A swept order parameter shows an up‑down gap whenever the sweep outruns relaxation, bistable or not. Relaxation lag shrinks as the sweep slows; bistability does not. So the test is the gap across sweep rates, and the spec asks only for m(J_up) − m(J_down) at one rate.

Measured at eta = 0, dwell = steps held at each J:

rule dwell 50 max gap dwell 200 dwell 800 slowest/fastest ratio
DIST 0.0117 0.0083 0.0083 0.714
SAMPLED 0.5667 0.7067 0.7050 1.244

SAMPLED's gap does not shrink under a 16× slower sweep. That is the bistability signature, and it is a stronger statement than the single‑rate measurement the spec asks for.

Reported honestly in both directions: the mean gap does fall (0.380 → 0.258) while the maximum holds, so part of the fast‑sweep gap is lag and the peak is not.

hysteresis_is_bistability() returns the gap per dwell and computes no verdict—three dwells do not fit a decay, and calling a shrinking gap "lag" or a flat one "bistable" is a reading.

The selftest asserts the carried state is load‑bearing: dropping it collapses the gap, which is what a hysteresis measurement re‑randomised at each J would silently be.

Falsifier: a gap that keeps shrinking at dwells beyond 800.

---

CA_006 — the chance baseline is not 1/K

E[m] under uniform random:

· measured: 0.2944 (sd 0.0223, 200 draws)
· naive 1/K: 0.2500
· ratio: 1.178 (17.8% higher)

With N agents over K positions, the modal fraction under chance is E[max count]/N, not 1/K. It moves with N—the selftest checks a smaller population returns a higher baseline, so the quantity is measured rather than being a constant with a different name.

Using 1/K as chance puts the baseline below where chance already sits and manufactures a J_c.

find_jc() reads the measured mean and requires the feature to clear it by MARGIN = 3.0 chance‑SDs—a reasoning‑gate G‑RES pair, feature against the instrument's own noise—and the selftest asserts 1/K appears nowhere in it.

Falsifier: an N and K where E[max count]/N equals 1/K, which is the N → ∞ limit and not any run.

---

CA_007 — my first run's null was my parameter choice

The first pass ran eta = 0.10, T = 80 and reported SAMPLED reaching m = 0.366 at J = 0.90 against a threshold of 0.3613—clearing by 0.004 with a seed SD of 0.05.

Read at face value, that is no alignment at any J, which fires one of H3's three limbs.

It is a parameter artifact. At eta = 0, T = 400, the same rule reaches m = 0.88.

Recorded rather than quietly fixed, because the failure mode is the one the drop is about: an arm run at a parameter setting that suppresses the effect returns a clean null, and the null is reportable.

The check that caught it was sweeping eta and T rather than reading the result—and nothing in the spec asks for that sweep.

Falsifier: a setting where the alignment result reverses again.

---

CA_008 — topology is H3's locus and is untested here

H3's stated locus is "interaction topology + coupling strength".

The text‑free arm as specified sweeps J and says nothing about topology, and this run is all‑to‑all. So the arm as written tests one of H3's two named factors.

A threshold on a complete graph is not evidence about a sparse one, and much of the interesting behaviour in coupled‑unit models is topological.

Every readout above is reported with topology declared and unswept, and the report says so in its own parameter block.

Cheap next step, no new instrument: run the same two rules on a ring, a random graph at two degrees, and a scale‑free graph, with the peer signal built from neighbours instead of the population.

Falsifier: a topology where SAMPLED loses the threshold or DIST gains one, either of which would make CA_002's split a property of the complete graph rather than of the reading.

---

CA_009 — the instrument caution, and the one part not exercised

"Do not gate case admission on record completeness. Any criterion strict enough to admit only clean cases admits only the cases whose records happened to survive, which is the bias being measured."

That is a real design rule and it is the same finding observer‑exclusion OE_003 measured from the other side: field biologists' notes are institutionally archived where an excluded population's artifacts are not, so a completeness criterion selects on archiving rather than on holding.

This arm cannot exercise it. There are no cases and no records—every number is generated in‑process, so nothing is admitted or excluded.

The adjacent sample is also unexercised and is the drop's own out‑of‑domain check. Its measurable—divergence between surviving variant lineages against transmission distance—has the survivorship problem in its own subject: surviving lineages are the ones that survived.

Falsifier: run it.

---

UNDERGRADUATE_RESEARCH_GAPS.md

Open questions in the consensus‑anchor framework, organized by discipline

Every gap in this folder is a research question with:

· A knowledge state (UNKNOWN_ATM, UNDER_STUDY, NOT_STUDIED, UNDEFINED)
· A falsifier (what would settle it)
· A data source (where to look)
· A method (how to answer it)
· An expected deliverable (what the undergraduate produces)

---

1. EMPIRICAL — Topology Sweep

Gap: H3's locus is "interaction topology + coupling strength", and the arm as specified sweeps only J. Topology is untested.

Knowledge state: NOT_STUDIED

Research question: Does the DIST/SAMPLED split survive when the interaction topology is not all‑to‑all? Does SAMPLED lose its threshold on sparse graphs? Does DIST gain one?

Disciplines: Complex systems, network science, computational modelling

Data sources:

· The textfree.py codebase (same two rules, different graph structures)
· Published literature on consensus on networks
· The reasoning‑dial sibling (RD_002, a knee that moves with the plot range)

Method:

1. Modify textfree.py to accept a topology parameter: ring, random graph (two degrees), scale‑free
2. For each topology, run both DIST and SAMPLED across the same J sweep
3. Measure m, J_c, and hysteresis for each topology
4. Compare to the all‑to‑all baseline
5. Document which topologies preserve the split and which collapse it

Expected deliverable: A topology‑sweep report, with per‑topology J_c values and split status.

Falsifier: A topology where SAMPLED loses the threshold or DIST gains one (then CA_002's split is a property of the complete graph, not of the reading).

---

2. EMPIRICAL — Noise‑Sweep Calibration

Gap: J_c moves with noise, and the spec has no noise term. The threshold is a ratio of coupling to noise—with no noise term, any J > 0 aligns eventually and the threshold sits at 0+.

Knowledge state: UNDER_STUDY

Research question: What is the functional form of J_c(eta) under SAMPLED? Does it follow a simple scaling (e.g., J_c ∝ eta), or is there a phase transition?

Disciplines: Statistical physics, complex systems, computational modelling

Data sources:

· The textfree.py codebase (noise parameter already implemented)
· Published literature on consensus with noise (voter model, noisy consensus)

Method:

1. Sweep eta from 0 to 0.20 in small increments
2. For each eta, find J_c using the measured chance baseline (CA_006)
3. Fit the J_c(eta) curve to candidate functions (linear, power‑law, exponential)
4. Test whether J_c diverges at a finite eta (a phase transition)
5. Document the functional form

Expected deliverable: A J_c(eta) calibration curve with fitted function and uncertainty bounds.

Falsifier: J_c does not vary with eta (then CA_004 is falsified).

---

3. EMPIRICAL — Hysteresis Sweep Rate Characterisation

Gap: The spec asks for a hysteresis gap at one sweep rate. The control is the gap across sweep rates, and the spec does not name it.

Knowledge state: UNDER_STUDY

Research question: At what dwell time does the SAMPLED hysteresis gap stop shrinking? Is there a clear separation between lag (shrinking with dwell) and bistability (flat with dwell)?

Disciplines: Dynamical systems, non‑equilibrium physics, computational modelling

Data sources:

· The textfree.py codebase (dwell parameter already implemented)
· Published literature on hysteresis and bistability

Method:

1. Sweep dwell time from 10 to 10,000 steps (log scale)
2. For each dwell, measure the hysteresis gap (max m(J_up) − m(J_down))
3. Fit a decay function to the gap vs. dwell
4. Identify the dwell time at which the gap asymptotes
5. Document the separation between lag and bistability

Expected deliverable: A hysteresis‑gap‑vs‑dwell curve, with asymptote identified and lag/bistability separation quantified.

Falsifier: The gap continues to shrink at dwells beyond 800 (then the claim that the maximum holds is falsified).

---

4. EMPIRICAL — Chance Baseline as Function of N and K

Gap: The chance baseline is not 1/K. It is E[max count]/N, and it moves with N.

Knowledge state: UNDER_STUDY

Research question: What is the functional form of the chance baseline as a function of N and K? Can it be expressed analytically?

Disciplines: Probability theory, statistics, combinatorics

Data sources:

· The textfree.py codebase (baseline measurement already implemented)
· Published literature on occupancy problems (coupon collector, birthday problem)

Method:

1. Sweep N from 10 to 10,000 and K from 2 to 100
2. For each (N, K) pair, measure E[max count]/N over many random draws
3. Fit the surface to candidate functions
4. Compare to the N → ∞ limit (1/K)
5. Derive an analytical approximation

Expected deliverable: A chance‑baseline surface B(N, K) with analytical approximation.

Falsifier: E[max count]/N = 1/K for any finite N (then CA_006 is falsified).

---

5. EMPIRICAL — SAMPLED vs. DIST on Model‑Side Arms

Gap: The text‑free arm tests H3 alone. H1 (inherited norm) and H2 (objective) need a trained model and are untouched.

Knowledge state: NOT_STUDIED

Research question: Does the DIST/SAMPLED split replicate when the agents are trained models rather than symbolic agents? Do H1 and H2 interact with the split?

Disciplines: Machine learning, AI safety, complex systems

Data sources:

· Trained language models (various sizes and architectures)
· The consensus‑anchor specification (H1, H2, H3)
· The simulation‑hypothesis‑budget sibling (SHB_010, the answer is ill‑posed until the level stack is specified)

Method:

1. Implement H1 (inherited norm) and H2 (objective) on trained models
2. For each, run both DIST and SAMPLED variants
3. Measure consensus outcomes
4. Test whether the DIST/SAMPLED split survives
5. Test whether H1 and H2 interact with the split

Expected deliverable: A model‑side replication of the text‑free arm, with per‑hypothesis results.

Falsifier: The DIST/SAMPLED split does not replicate on trained models (then the text‑free result is not informative about model‑side consensus).

---

6. EMPIRICAL — Parameter Sweep for the Null Artifact

Gap: The first run's null was a parameter choice (eta = 0.10, T = 80). The effect reappeared at eta = 0, T = 400.

Knowledge state: UNDER_STUDY

Research question: What is the full parameter space of (eta, T, J) where SAMPLED shows alignment vs. no alignment? Is there a sharp boundary or a gradual transition?

Disciplines: Complex systems, computational modelling, numerical analysis

Data sources:

· The textfree.py codebase
· The parameter‑sweep infrastructure (already implemented for eta and T)

Method:

1. Sweep eta from 0 to 0.20 and T from 10 to 1000
2. For each (eta, T) pair, measure the maximum m over J
3. Identify the boundary between "alignment" and "no alignment"
4. Test whether the boundary is sharp or gradual
5. Document the full parameter space

Expected deliverable: A phase diagram of (eta, T) showing alignment vs. no‑alignment regions.

Falsifier: No boundary exists—alignment is either always present or always absent (then the null artifact is not a parameter‑space phenomenon).

---

7. EMPIRICAL — Invariance Proof for DIST

Gap: Under DIST, the population mean is invariant to machine precision. The proof is analytic.

Knowledge state: VERIFIED (analytic)

Research question: Does the invariance hold under finite‑precision arithmetic for very long runs? What is the drift rate under floating‑point?

Disciplines: Numerical analysis, floating‑point arithmetic, computational modelling

Data sources:

· The textfree.py codebase
· IEEE 754 floating‑point specification

Method:

1. Run DIST for very long durations (10⁶ steps or more)
2. Measure population‑mean drift
3. Compare to machine epsilon
4. Test whether drift accumulates or remains bounded
5. Document the finite‑precision behaviour

Expected deliverable: A finite‑precision drift analysis for DIST, with bounds on long‑run behaviour.

Falsifier: Drift exceeds machine‑precision expectations (then CA_003's invariance claim is falsified for finite precision).

---

8. EMPIRICAL — Survivorship Bias in the Adjacent Sample

Gap: The adjacent sample—divergence between surviving variant lineages against transmission distance—has the survivorship problem in its own subject.

Knowledge state: NOT_STUDIED

Research question: Does the adjacent sample actually show the survivorship problem? Can it be measured and quantified?

Disciplines: Evolutionary biology, textual criticism, survival analysis

Data sources:

· The adjacent sample (if available)
· Published literature on survivorship bias in transmission
· The observer‑exclusion sibling (OE_003, the survivorship problem)

Method:

1. Identify the adjacent sample (variant lineages, transmission distances)
2. Measure the divergence between surviving lineages
3. Test whether divergence correlates with transmission distance
4. Test whether the correlation is an artifact of survivorship
5. Document the survivorship effect size

Expected deliverable: A survivorship‑bias analysis for the adjacent sample, with effect size.

Falsifier: The divergence‑vs‑distance correlation is robust to survivorship correction (then the survivorship problem is not present).

---

9. EMPIRICAL — reasoning‑dial Knee Movement

Gap: The drop notes that reasoning‑dial RD_002 has a knee that moves with the plot range.

Knowledge state: NOT_STUDIED

Research question: Does the reasoning‑dial knee actually move with the plot range? If so, what does that imply about the measurement?

Disciplines: Visualisation, measurement theory, experimental design

Data sources:

· The reasoning‑dial sibling repository
· Published literature on visualisation artefacts

Method:

1. Replicate the reasoning‑dial measurement
2. Vary the plot range (x‑axis limits, y‑axis limits)
3. Measure the knee position as a function of plot range
4. Test whether the knee is a visual artefact or a genuine feature
5. Document the finding

Expected deliverable: A plot‑range sensitivity analysis for reasoning‑dial.

Falsifier: The knee does not move with plot range (then RD_002's claim is falsified).

---

10. USER GUIDE — Non‑Specialist Translation

Gap: The framework is documented for researchers but not for non‑specialists.

Knowledge state: NOT_STUDIED

Research question: How can the consensus‑anchor framework's insights be communicated to non‑specialists in a way that changes how they think about consensus, ambiguity, and measurement?

Disciplines: Science communication, policy, education

Data sources:

· The framework itself
· Published science communication research
· Guidelines for communicating uncertainty

Method:

1. Translate each claim into plain language with concrete examples
2. Develop case studies for each failure mode (two readings, agreement vs. consensus, chance baseline, parameter artefacts)
3. Create a user guide explaining: "What this framework means for you"
4. Test the guide with non‑specialist audiences
5. Iterate based on feedback

Expected deliverable: A non‑technical user guide to the consensus‑anchor framework.

Falsifier: Non‑specialists find the guide unhelpful or incomprehensible.

---

SCOPE_BOUNDARY.md

Why this framework is broader than standard consensus measurement practice

---

The Problem

In consensus measurement, things like the reading of the update rule, the distinction between agreement on a position and agreement on a distribution, the noise level, and the sweep rate are not separate from the measurement. They are direct, material, contributing factors to whether consensus is detected. When a study says "the population reached consensus," that is treated as a finding about the system.

But the update rule sentence has two readings, and they give opposite verdicts. Under one, all three limbs of H3's falsifier fire; under the other, none does. Under one, the population reaches total agreement and zero consensus—every agent holds an identical distribution, and that distribution is near‑uniform, so expressed positions stay at chance forever. The measurement of consensus depends on the reading of the rule.

---

Six Ways the Connection Gets Lost

1. The "Reading as Neutral" Fallacy

Many studies treat the reading of a rule as neutral—as if the rule has a single, unambiguous interpretation. If the study says "the update rule is X," that is treated as a fact.

But the update rule sentence has two readings, both defensible. SAMPLED is the more literal reading; DIST is what you get if "position vector" is read as the object being mixed. They give opposite verdicts on H3. If the study says "the rule is X," it is not false for one reading, but it may be false for the other. The reading was causal—just not represented.

So "reading as neutral" often means "We assumed the rule has a single interpretation." That is a semantic error, not evidence that the rule is unambiguous.

2. The "Agreement as Consensus" Fallacy

Many studies treat agreement as consensus. If agents agree, that is treated as evidence of consensus.

But under DIST, agents reach total agreement—agent spread exactly 0.0—and zero consensus. Every agent holds an identical distribution, and that distribution is near‑uniform, so expressed positions stay at chance forever. Agreement and consensus are not the same. If the study says "consensus reached," it is not false for the agreement, but it may be false for the system. The distribution was causal—just not represented.

So "agreement as consensus" often means "We measured agreement and called it consensus." That is a measurement error, not evidence that agreement implies consensus.

3. The "J_c as Property of J" Fallacy

Many studies treat J_c as a property of the coupling strength. If the study says "the threshold is J_c," that is treated as a finding about the system.

But J_c moves with noise. With no noise term, any J > 0 aligns eventually and the threshold sits at 0+; with enough noise, the threshold leaves the grid. The threshold is a ratio of coupling to noise. If the study says "J_c is X," it is not false for one noise level, but it may be false for another. The noise was causal—just not represented.

So "J_c as property of J" often means "We assumed noise is fixed or irrelevant." That is a modelling error, not evidence that J_c is a property of J alone.

4. The "Hysteresis as Bistability" Fallacy

Many studies treat a hysteresis gap as evidence of bistability. If the up‑down curves differ, that is treated as evidence of multiple stable states.

But a swept order parameter shows a gap whenever the sweep outruns relaxation, bistable or not. The control is the gap across sweep rates. If the gap shrinks as the sweep slows, it is lag; if it stays flat, it is bistability. The spec asks for one rate. If the study says "hysteresis observed," it is not false for the gap, but it may be false for the interpretation. The sweep rate was causal—just not represented.

So "hysteresis as bistability" often means "We assumed the gap is not lag." That is a dynamical error, not evidence that the gap is bistability.

5. The "Chance as 1/K" Fallacy

Many studies use 1/K as the chance baseline. If the study says "the baseline is 1/K," that is treated as a fact.

But E[max count]/N is the modal fraction under chance. It is 17.8% higher than 1/K for N = 200, K = 4, and it moves with N. Using 1/K puts the baseline below where chance already sits and manufactures a J_c. If the study says "the baseline is 1/K," it is not false for the large‑N limit, but it may be false for the finite‑N run. The finite‑N correction was causal—just not represented.

So "chance as 1/K" often means "We assumed N is large enough." That is a statistical error, not evidence that 1/K is the correct baseline.

6. The "Parameter as Control" Fallacy

Many studies treat parameters as controls—things that are fixed and uninteresting. If the study says "the parameters were X," that is treated as sufficient.

But the first run's null was a parameter choice. Run at eta = 0.10, T = 80, it reported no alignment at any J. At eta = 0, T = 400, the same rule reached m = 0.88. The null was not a result; it was a parameter artifact. If the study says "no alignment observed," it is not false for the parameter setting, but it may be false for the system. The parameter choice was causal—just not represented.

So "parameter as control" often means "We assumed parameters don't affect the result." That is a numerical error, not evidence that the result is parameter‑independent.

---

What This Framework Does Differently

This framework treats consensus measurement as potentially reading‑dependent—the update rule has two readings, they give opposite verdicts, and the distinction is not visible to the order parameter. The following components document mechanisms that standard consensus measurement practice typically drops:

· The two readings — DIST (mean of peers' distributions) and SAMPLED (empirical distribution of peers' sampled positions). They give opposite verdicts on H3.
· The agreement‑vs‑consensus distinction — Under DIST, total agreement and zero consensus. m sees agreement; it does not see the difference between agreeing on a position and agreeing on a distribution.
· The noise‑dependent threshold — J_c moves with noise. The spec has no noise term, so "the coupling value at which m departs from chance" has no value until noise is fixed.
· The sweep‑rate control — Hysteresis is not bistability. The control is the gap across sweep rates, and the spec asks for one rate.
· The measured chance baseline — Not 1/K. E[max count]/N, measured, with a 3.0 chance‑SD margin.
· The parameter artefact — The first run's null was a parameter choice. Recorded rather than fixed, because the failure mode is the one the drop is about.

---

The Knowledge‑State Vocabulary

When a variable or mechanism is physically relevant but not yet quantified, the framework records its epistemic state rather than excluding it:

State Meaning Example
NOT_STUDIED The mechanism is recognised, but no measurement has ever been attempted. Topology sweep, model‑side arms.
UNDER_STUDY Data collection is in progress; value is provisional. J_c(eta) calibration, hysteresis sweep‑rate characterisation.
UNKNOWN_ATM The mechanism is known to exist, but no current value is available. Whether the DIST/SAMPLED split survives on sparse graphs.
VERIFIED The claim is analytic and checked. The invariance proof for DIST.

---

What Is NOT a Valid Epistemic State

ASSUMPTION_OF_READING is not a valid knowledge state. If the update rule has two readings and they give opposite verdicts, assuming one reading is correct is a semantic error, not an epistemic one. The system does not care about our reading preferences.

The framework refuses to record a result as a measurement without stating the reading. Instead, it records the result as reading‑dependent—the verdict changes with the reading—and names what would be needed to move it to a settled state.

---

The Standard

The question should not be:

"What does the consensus measurement say?"

But rather:

"Which reading of the update rule was used, and does the result survive the other reading?"

If the answer is that the verdict changes with the reading, the measurement is not a measurement of consensus—it is a measurement of the reading.

The system is already reading‑dependent. Our assumptions of neutrality, agreement‑as‑consensus, fixed noise, single‑rate hysteresis, 1/K baselines, and parameter‑as‑control are the only things pretending otherwise. And that pretense has produced a literature of consensus measurements that may be measuring the reading rather than the system.

This framework does not pretend otherwise.
