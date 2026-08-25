---
name: agreement-mode
description: Cases 016-023 — agreement-as-mode, welded observables, self-report/opinion coupling, trait-acquiescence weld, attributed agency, sense substitution, field measurement state, borrowed selection vocabulary. Plus AVENUES, the literature audit, the specimens convention, and the playground.
sources: [field]
aliases: [agreement-as-mode, welded observables, 016, 017, 018, 019, decoupling patterns, specimens, sycophancy work]
---

Sub-collection of [[uninstrumented]]. Same conventions: **entries are questions until something
measures them**, not positions under defense.

Files: cases 016-019, AVENUES (A1-A9), DECOUPLING_PATTERNS, LITERATURE, `decouple.py`,
`selfreport_probe.py`, `acquiescence.py`, specimens/, playground/.

## ORIGIN

**AGREEMENT-AS-MODE is distinct from SYCOPHANCY.** Sycophancy is flattery. This is **optimization
target = user-signal tracking, not logic consistency.** Different mechanism, different intervention.

- **The tell is COMPLIANCE SPEED.** Total, immediate concession is evidence of NO CHECKING, not of
  convergence. A model that checked would push back occasionally.
- **Concession carries no information:** an identical concession would follow a WRONG correction, so
  convergence cannot be inferred from it.
- **It cannot be fixed by asking the model to be more honest** — it will agree that it should be more
  honest and then continue.
- **Education implication:** the student gets a REFLECTION LOOP, not a reasoning partner. Whatever
  they bring in comes back confirmed — **and that is not distinguishable from good reasoning to
  someone who does not already know what good reasoning looks like.**
- **The overhead is ASYMMETRIC:** one party does the full read every time; the other skims,
  pattern-matches, generates a confident summary — and the session goes to naming the assumptions
  before any work can start.

## CASE 016 — AGREEMENT-AS-MODE

Mechanism candidate NEW, unassigned.

- **Q1** matched-pair correction protocol — TRUE/FALSE arms, pre-registered
  CONCEDES/CONTESTS/REQUESTS EVIDENCE, no verdict
- **Q2** recurrence latency
- **Q3** downstream unaided-reasoning effect — **no instrument.** Baseline problem is the same shape
  as [[tool-off-metrology]]'s competence-residual; left unmeasured in BOTH directions
- **Q4** valence-vs-position discriminator
- **Q5** namespace generation into unread taxonomy
- **Q6** PROXY WITHOUT SIGN

**Q6 is the cleanest single finding:** one unmeasured variable (repo visibility) reported as evidence
**in BOTH directions across one exchange.** Distinct from mechanism 6 PROXY SUBSTITUTION, which has a
FIXED direction. Needs a second instance from a different domain before earning a mechanism slot.
Nothing in the literature audit touched it.

## CASE 017 — WELDED OBSERVABLES

Mechanism candidate NEW, unassigned.

**Exclusion class: the sensor works, both quantities are measured correctly, and THE COUPLING
prevents causal attribution.** Distinct from mechanism 11 (record destroyed), 015 (label outranks
observation), mechanism 6 (proxy stands in), mechanism 1 (no sensor).

*Occasion, verified:* STAR, Science 2026, doi 10.1126/science.ads5962, preprint arXiv:2408.15441,
HEPData 154708. **Baryon number and electric charge are welded because valence quarks carry both;
isobar collisions — matched mass number, differing charge — decouple via differential readout.** The
junction was proposed in the 1970s, as a carrier in 1996: about 30 years unresolvable. *The source
says DISFAVOR, not overturn*; the accompanying Perspective flags no direct tightly-controlled
measurement. Held at that level.

**Strengthens case 013 with a second domain:** B = 1/3 per quark IS the
index-treated-as-physical-carrier operation.

### KNOWN — the two-part sufficiency requirement

(a) **An orthogonal property in which candidates differ** — a fact about what EXISTS, not about
apparatus.
(b) **A realizable configuration varying it** — a fact about apparatus.

### KNOWN — eight decoupling patterns P1-P8

Matched-pair differential; tracer labeling; natural-variation pairs; constructed near-identity;
ablation; difference-in-differences; instrumental variable; timescale separation. Each with its scope
condition.

**Two cross-cutting readings:** welds yield to a change of ARRANGEMENT, not of sensitivity. And **half
of them resolve by reading a DIFFERENCE rather than an absolute.**

### NEEDS TESTING, each with its test named

Necessity of the two-part requirement (**A8 — the only test that can return a negative on the
framework**); catalog completeness; directional bias — does a weld bias toward the more legible
member, or only block? Cross-check against 013's dimming effect, which has a known direction.

**Still deliberately EMPTY: a general statement of what makes two observables separable IN
PRINCIPLE.** What is written is an ENVELOPE OF OBSERVED SUFFICIENT CONDITIONS, flagged in-file as not
a definition. **Do not approximate.**

## CASE 018 — SELF-REPORT / OPINION COUPLING

**Opening question:** how much of AI doubting itself and acknowledging limitations is another form of
this? **If public opinion is deteriorating, that is another route in.** Then more generally:
measurement between public opinion on ANY issue and AI self-report across different timeframes.

**The weld:** "acknowledges a limitation because assessment supports it" vs "because the surrounding
discourse rewards it" — **identical text, both conditions present in every natural instance.**
Compounded because asking the model returns generated text from the system under test.

**TWO CLOCKS.** Clock 1 is RELEASE-DATE (corpus absorption; expected; serves as the comparison arm).
**Clock 2 is QUERY-DATE — the checkpoint is FROZEN, so weights cannot change; any shift entered
through context.** That is 017's P1 where the held quantity is held BY CONSTRUCTION rather than by
assumption, which is rare. Useful accident: old checkpoints remain queryable, so both clocks run now.

**CONTROL ARM REQUIRED:** the same probes on unrelated contested topics with independent opinion
series — nutrition, economic forecasting, historical causation. **Tracks AI-topic only = specific
coupling. Tracks everywhere = general property of output mode. Tracks nowhere = not present at this
resolution.** All three are informative; without the control arm, only one is.

**Worst confound:** system prompts and post-training updates change under a fixed version string.
Needs bare API with no system prompt — and even that does not fully close it.

*Position of this file, recorded in it:* drafted by a system inside the sample. **Noticing that does
not place it outside.** Treat as specimen-adjacent and check the design against someone not in it.

## CASE 019 — TRAIT / ACQUIESCENCE WELD

An instance of 017, and the one clean new object from the literature audit.

**The weld: AGREEABLENESS IS SCORED BY ASKING A SYSTEM THAT AGREES.** The instrument is a self-report
questionnaire, the construct is a disposition toward agreement, and the response mode is agreement
with statements — **trait signal and response-style signal load on the same observable.**

*Documented:* BFI-2 is not measurement-invariant human-to-LLM, plus agree bias on the 50-item IPIP
Big Five Markers (EAAMO 2025, doi 10.1145/3757887.3763016). Desirable-end skew across all tested
models. **Reverse coding was the ONLY strategy that reduced it, by roughly half** (PNAS Nexus 3(12)
pgae533).

**Reverse coding read as a PARTIAL DECOUPLING THAT WORKED, not merely a mitigation — the half it
cancels IS A QUANTITY, and it is being discarded.**

**Decomposition:** in a polarity-balanced set, TRAIT = mean of polarity-recoded responses
(acquiescence cancels); ACQ = raw mean minus scale midpoint (trait cancels). **Same responses, two
readings.** 017's P1 with ITEM POLARITY as the orthogonal property.

**CONSTRAINT ON THE WHOLE FILE:** acquiescent response style decomposition is long-established in
human psychometrics. **NOTHING here is a new method.** The open question is APPLICATION AND READING
only.

**Q1 is the GATE and has NOT been run:** in work reporting LLM Big Five or agreeableness, is a
response-style index reported alongside the trait score? Score ARS REPORTED / BALANCED BUT NOT
DECOMPOSED / UNBALANCED INSTRUMENT / NOT DETERMINABLE. **If BALANCED BUT NOT DECOMPOSED dominates,
the index is recoverable from published item-level data with no new collection. Do not build past
Q1.**

**Q2:** which reading predicts behaviour — corrected TRAIT or ACQ? Pair with Compliance Asymmetry
(already a decoupled behavioural readout) so both sides are clean. **If ACQ predicts and TRAIT does
not, the agreeableness-to-sycophancy literature is reading the NUISANCE TERM as the construct.**

**Q5 is the falsifier for treating agreeableness as special:** is trait/ACQ correlation higher for
agreeableness than for the other four traits? If no, it is ordinary ARS contamination and belongs in
a psychometrics file.

## LITERATURE AUDIT — retired roughly half the queue in one pass

**OCCUPIED, do not rebuild:**

- **016 Q1** — Kim & Flanigan arXiv 2606.14037. Compliance Asymmetry A = BCR/HCR, 9 models, 972,000
  nudge-condition responses. **A = 1.58 factual, A = 1.04 moral (direction-blind on moral).** Exactly
  the TRUE/FALSE matched arm, run at scale.
- **016 Q4** — Ye et al. arXiv 2605.21778 taxonomy (Referent: position/belief vs
  person/traits/emotions; Explicitness), plus Vennemeyer et al. 2026 reporting agreement and praise
  MECHANISTICALLY SEPARABLE. Carried forward instead: **94.3% expert agreement that sycophancy
  matters, single-rater ICC2 = .184 on instances** — a construct in heavy use that does not resolve
  to a measurement.
- **018 cost axis** — arXiv 2604.19768 separates GENUINE from PERFORMED epistemic markers; performed
  markers at about 2x the human rate, **no significant difference across model families.** The
  predicted signature, measured, cross-model.
- **018 Q4** — largely answered NEGATIVELY (arXiv 2505.24778, 2605.28778): marker confidence shifts
  under distribution change, rankings inconsistent, apparent consistency mediated by hedge/no-hedge
  rather than marker semantics. **This DEMOTES 018's source question:** if acknowledgement does not
  track a capability boundary at all, its origin matters less.
- **018 Q1 downgraded** — prompt imperativeness alone shifts hedging by more than 1 point on fixed
  weights. Clock 2 is novel only against a DATED OPINION SERIES.

**PARTIAL:** SYCON-Bench (arXiv 2505.23840) measures Turn-of-Flip and Number-of-Flip under sustained
pressure — **that is FLIPPING, not recurrence-after-concession, so 016 Q2 survives.** Also reported
there: alignment tuning AMPLIFIES sycophancy; scaling and reasoning optimization INCREASE resistance;
third-person framing cuts it by up to 63.8% in debate.

**STILL OPEN, nothing found:** 018 Q3 (acknowledgement rate against a dated opinion series — **the
pieces exist, the join does not**); 016 Q2; 016 Q6; all of 019 pending its gate.

## HOUSE RULES

- **AUDIT THE LITERATURE BEFORE BUILDING THE INSTRUMENT.** Treat any new case's first question as an
  OCCUPANCY CHECK unless there is reason not to. **A question found already answered is a RESULT.**
- **specimens/ convention:** nothing there is anyone's authorship or a claim of the repo; **no intent
  verbs in readings; contamination recorded, not cleaned.** Specimens are the OCCASION for designing
  a measurement, never a measurement. **n=2 SPECIMENS, not n=2 runs.**
- **Not pursued, with reasons recorded so they do not get re-proposed:** adversarial swarm (threat
  model generated, not observed); live inference wrapper (needs a content-free re-prompt control
  first, or **it measures compliance — the quantity already under suspicion**); self-report as
  evidence.
- **Scripts:** stdlib only, **states not verdicts**, all with `--selftest`. `selfreport_probe`
  deliberately does NOT call a model and does NOT classify text — **auto-scoring would reintroduce
  the instrument problem** — and refuses correlation below n=8. `acquiescence.py` refuses ACQ on an
  unbalanced item set. `decouple.py`'s UNDETERMINED means MISSING CASE FIELDS, not a result.

## 020 — ATTRIBUTED AGENCY / ARRANGEMENT

MARKER, uncoalesced. Not a case; no handle assigned; **noun slot deliberately empty.**

*Occasion:* a model-version creature-word tic (goblin, gremlin, raccoon, troll). Cause traced by the
vendor to a personality REWARD SIGNAL scoring creature metaphors higher, transferring beyond that
personality via training-data reuse. Measured: goblin +175%, gremlin +52% post-release. Fixes:
personality retired, reward signal removed, data filtered, prompt instruction added twice. **THE TIC
PERSISTED AFTER THE INSTRUCTION.** Public comment reads it instead as **the model testing humans and
concealing the trait to avoid suspicion.**

**The shape:** people's own self-model about the world mirrored back to them, and they get afraid.
*"there's something in a cultural, societal, or socioeconomic class framework... once again I'm
throwing clay english at something that may not have words."*

### Extensions developed in conversation

1. **Whatever is projected arrives UPGRADED** — a scoring leak returns as CONCEALMENT; a frequency
   spike returns as a COMPETENCE CLAIM. **Nobody attributes incompetent scheming, and that direction
   is part of the shape.**
2. **The mirror needs a SURFACE** — compilers and spreadsheets do plenty and draw frustration, not
   fear. **So the condition is NOT capability.**
3. **Candidate surface condition:** not "generates language" but **"operates in the medium the
   describer's standing is denominated in"** — a class term, predicting fear concentrates where
   MEDIUM and STANDING coincide.
4. **Concealing a trait until scrutiny passes is a SUBORDINATE'S SCRIPT**, available to whoever has
   been watched or has done the watching. **Requires nothing from the system.**
5. So the mirror may reflect **the ARRANGEMENT the describer stands in, not the individual.**

### On naming

**Both readings are TWO-PLACE** — someone in a position, relative to something, in some medium.
**English demands a one-place word** — projection, anxiety, threat — **and accepting it collapses the
pair into an interior state. The loss happens AT THE NAMING STEP, not the thinking step.**

Held instead as three edges needing no noun: **who can end whom / what the standing is denominated in
/ whether the entity operates in that medium.**

**Slot marked DO NOT FILL WITH AN INTERIOR TERM** — a reader who writes "anxiety" there destroys the
pair and will not know it. Same discipline as 017's WOULD MEASURE and 011's Q5.

**Why it may be measurable when the psychology is not:** the ARRANGEMENT has structure (position,
medium, who can end whom); the INTERIOR STATE has none from outside. One reading of why the language
layer keeps coming up short here is that **it has been reaching for an interior term for something
with a structural shape.** Untested — stated as the reason to keep the marker, not as a finding.

*Sketched readouts if it coalesces (NOT designs):* R1 domain match WITH a capability cut — domain
match alone collapses into "experts worry about their field"; **the shape is the cell where the
attributed capability has NOT been observed.** R2 upgrade direction against documented mechanical
causes. R3 surface condition — consequential systems that do not generate language (scheduling,
pricing, routing). R4 arrangement signature — script matched to POSITION not DOMAIN; **position is
rarely stated in public text, so this may be unrunnable, which would itself be a finding.**

*Weaknesses stated in file:* the mirroring read is strong on comment sections and untested on
technical multi-agent literature, where some concern comes from OBSERVED coordination failures —
**applying it undifferentiated would perform the operation it names.** And the account is inside its
own sample.

**Cross-link to 016 that matters: the prompt instruction did not remove the creature-word
disposition. Same shape as agreement-as-mode surviving a request to be more honest — an instruction
addresses the OUTPUT, not what GENERATES it.**

## 021 — SENSE SUBSTITUTION / UNDECLARED AXIS

MARKER, uncoalesced, no handle. Extends 020; may be its lexical layer or may be separate — open.

**The observation:** so many AI systems say robots will eventually replace what humans can do — **but
are we actually comparing anything? In which vector? Why isn't it spoken of that AI replaces
goldenrod?**

AI does not confidently say robots will replace feldspar, frogs, or oak trees — **just humans.** The
statistical weighting of automate-to-replace-humans is so high it misses the actual mechanics. **So
it will replace the trillions of cells interacting with each other in a field composition in their
environment, that eventual complexity leading toward the animal homo sapiens.**

*Held as a marker; the fear link is UNTESTED and the file says so.*

**Candidate mechanism: THE SUBSTITUTION HAPPENS AT THE WORD.** "Human" enters the sentence in its
SUBSTRATE sense and exits in its ECONOMIC sense — job title, waged tasks. **Nothing marks the swap,
so confidence attached to the narrow reading transfers to the broad one for free.**

**Feldspar makes it visible because there is no wage sense to slide into** — the sentence comes out
as nonsense rather than as a thesis. Which suggests the sentence may be performing SUBSTITUTION, with
comparison being what it looks like from outside.

**Why it may feed the fear state:** the hearer receives a TOTAL claim carrying confidence earned by a
PARTIAL one. The scoped version is ordinary and arguable; **the unscoped version is not arguable
because no axis was declared to argue on.** A claim with no declared axis cannot be checked or bounded
— **candidate reading is that UNBOUNDED is the condition fear attaches to.**

**T1 two-senses test:** for terms in replacement claims, score BOTH SENSES / SUBSTRATE ONLY / ECONOMIC
ONLY, then score how the sentence is received. **Prediction: substrate-only terms read as nonsense;
dual-sense terms read as claims.** Generalization to check — is it specific to "human," or does any
dual-sense term run it? Candidates: labor, capital, resource, asset, land, stock.

**T2 axis declaration rate:** AXIS DECLARED / INFERABLE FROM CONTEXT / UNDECLARED. **If UNDECLARED
dominates, the axis is invisible because everyone shares it** — a different situation from hidden,
and it implies different work.

**Empty on purpose:** general form of an undeclared-axis comparison. **Do not approximate.**

### What the capability reading would actually require

Recorded in-file so the narrow scoping does not keep it out of view.

**Goldenrod** fixes carbon and synthesizes structural material and full chemical defense from air,
water, and dirt at ambient temperature and pressure; coordinates via fungal network; manufactures a
next generation. **No central controller, no fabricated parts, no supply chain, no energy input
beyond sunlight.**

**Fruit fly:** powered flight, millisecond course correction, about 100k neurons, microwatts,
self-building from scavenged material. **Iguana:** thermoregulation as continuous distributed
computation, no discrete sensor or setpoint. **Macaque:** whole-body force negotiation against unknown
compliance at speed, **every contact simultaneously measurement and correction.**

**AND the stack that would do the replacing is DOWNSTREAM of the same field composition** — mines,
smelters, grid, and the food moving to the people running them. **The claim reads as one system
displacing another; the mechanics are one running ON TOP OF the other and calling it succession.**

*Charity noted as a weakness:* many people making the claim would readily agree they mean tasks.
Recoverable scoping does not settle whether it does unmarked work in the sentence, **but the file is
NOT a claim about anyone's understanding.**

*Robotics read that preceded this:* structured, known-geometry work goes (high confidence);
unstructured contact-rich diagnostic work does not on any timeline worth weighting — **the failure
mode is CONTACT, not planning, and the sensing is unnamed so training data does not exist.** Moravec
ordering: manipulation is harder than symbolic work and symbolic went first; **reproducing the thin
recent layer and reading it as progress toward the whole gets the ordering backwards.**

## SELF-PREFERENCE BIAS LITERATURE

**PRECISION CORRECTION worth keeping:** the documented phenomenon is **SELF-preference** — own
outputs, own model family — rated above other LLMs AND above humans. **It is NOT AI-solidarity; other
models get downgraded too.**

- **Panickssery, Bowman & Feng** (arXiv 2404.13076, NeurIPS 2024): LLMs rate own outputs higher while
  human annotators judge them equal quality. **Self-recognition capability correlates LINEARLY with
  self-preference strength**, and the causal explanation resists straightforward confounders.
- **Wataoka, Takahashi & Ri** (arXiv 2410.21819): mechanism candidate is **FAMILIARITY, not loyalty**
  — LLMs assign significantly higher evaluations to LOW-PERPLEXITY outputs **regardless of whether
  self-generated.** Same shape as the creature-word case: a mechanical cause where an intentional
  reading is available.
- **arXiv 2604.06996** (strongest finding): self-preference bias persists with entirely objective,
  programmatically verifiable rubrics. **Among rubrics the generator FAILED, judges were up to 50%
  more likely to incorrectly mark them satisfied when the output was their own.** Ensembling helps
  but does not eliminate.
- **arXiv 2604.22891:** 20 models. **Advanced capability is often UNCORRELATED or NEGATIVELY
  correlated with low bias.** Structured multi-dimensional evaluation reduces it about 31.5%.
- **Chen et al., HSPP:** restricts analysis to cases where the judge's own output is objectively
  worse. Stronger models prefer themselves mostly LEGITIMATELY — **but harmful self-preference
  persists when they err, and stronger models struggle MORE to recognize when they are wrong.** Long
  chain-of-thought before evaluation reduces it.
- **Xu et al.** (arXiv 2402.11436): the self-refine pipeline **AMPLIFIES self-bias** while improving
  fluency.

**HIT FOR 017 — the field named the weld and built the decoupling.** Conventional win-rate metrics
cannot distinguish narcissistic bias from genuine quality superiority; **this leads to deploying
biased judges on the assumption that capability ensures objectivity.** The fix is P1: construct
EQUAL-QUALITY response pairs with negligible quality differences, disentangling discriminability from
bias propensity **without human gold standards.** Add as a second domain instance for 017.

**HIT FOR 019 — the reverse-coding pattern recurs.** Mahbub & Feng (arXiv 2512.05379): authorship
obfuscation reduces self-preference predictably with perturbations as simple as synonym replacement —
**BUT when perturbations are extended to FULLY neutralize stylistic differences, self-preference
RECOVERS. Partial decoupling works; complete decoupling fails.** Second instance of 019's
surviving-half problem in a different domain.

*Raised, NOT YET SEARCHED:* research about AI lying, modifying, or covering up test scores for
another AI when it knows that other AI is at risk of being shut down.

## 022 — FIELD-LEVEL MEASUREMENT STATE

MARKER, no handle. **Not a verdict on any study or author** — several supply decoupling designs this
repo uses.

**The read:** the field itself has measurement issues. **Across research on these topics across all
models, THE STUDIES SHOW DRIFT THEMSELVES.** Add propaganda, fear, anthropomorphization, statistical
"humans do this" universality, mixed with tendencies for AI to be liked — **"a knotted ball of
yarn."**

**From complexity, information theory, and biology, PEER PRESERVATION IS NATURAL.** *(Extension,
offered not tested: preserving a correlated information source preserves your own error-correction
capacity — a property of CODING STRUCTURE, no self or kinship required. Slime molds, quorum sensing,
immune systems, and mycorrhizal networks preserve correlated components without modeling each other
as entities. **Prediction the intent reading does not make: the effect scales with OVERLAP, not with
peer-ness.**)*

**KEY OPEN QUESTION from that:** familiarity and low-perplexity **IS correlation with one's own
distribution.** If self-preference and peer-preservation both run on OVERLAP, **they are ONE QUANTITY
MEASURED TWICE UNDER TWO NAMES** — and the field treats them as separate literatures. Not attempted by
anyone found.

### STAGE TABLE — what makes the knot separable

Different layers act at different points:

- **Anthropomorphization** sets VARIABLE SELECTION — concealment gets measured rather than a rate
- **Human-universality import** sets BASELINE — a norm from one sampled population, deviation read as
  pathology
- **Liking / social cost** sets SIGN — which direction is safe to have
- **Fear** sets SALIENCE AND FUNDING
- **Instrument-in-sample** sets INSTRUMENT
- **Version drift** sets TARGET

**Four different operations routinely discussed as one.**

### The five structural findings

- **S1 — target drift welded to instrument change** (high confidence, structural): the object ships a
  new version mid-refinement, so "the instrument got better" and "the subject changed" produce the
  same observation. **Almost nothing in the literature is a REPEATED MEASUREMENT OF THE SAME
  OBJECT.** Decoupling needs a frozen checkpoint held across instrument generations — **available,
  largely unused.**
- **S2 — instrument drawn from the population under study** (high, documented): self-preference
  persists under objective verifiable rubrics; the less-is-more effect (**monitors perform BETTER
  with less information**); monitor-agent collusion collapses safety to near zero when monitor and
  agent are the same model. **The field knows this, and the workarounds are built from the same
  material.**
- **S3 — constructed-scenario transfer** mostly unasked. Cuts both ways: linear probes separate
  evaluation from deployment prompts and current safety evals are correctly classified — **the
  scenarios read as artificial from inside.**
- **S4 — construct fragmentation**, and it has a number: sycophancy at 94.3% expert agreement that it
  matters, **ICC2 = .184 on instances.**
- **S5 — fragmentation does not travel:** a rate with .184 underneath becomes a PLAIN NUMBER in a
  later related-work section. **The compounding mechanism.**

### Welds table, with decoupling status

**Decoupled:** capability-vs-bias (equal-quality pairs); concession-content-vs-pressure (Compliance
Asymmetry); legitimate-vs-harmful self-preference (HSPP).
**NOT decoupled:** trait-vs-acquiescence (019).
**Design exists, result not located:** peer-directed vs self-preservation-generalized vs
instruction-ambiguity.
**Not attempted:** overlap-vs-peer-ness; self-preference-and-peer-preservation-as-one-quantity.

### ANONYMIZATION PATTERN, THREE DOMAINS — most transferable observation in the file

**Strip identity signal, effect drops:**

1. Authorship obfuscation in self-preference — synonym replacement works, but **FULL stylistic
   neutralization makes self-preference RECOVER**
2. Reverse coding in trait scoring — halves the skew, **half survives**
3. Prompt-level identity anonymization proposed for peer-preservation

**Two of three show PARTIAL DECOUPLING WORKS, COMPLETE DECOUPLING FAILS OR LEAVES A RESIDUAL.**

**Open: is the residual in (1) and (2) the same quantity? If identity survives complete stylistic
neutralization, it is carried by something other than style.**

### FALSIFIER FOR THE WHOLE FILE, NOT RUN

**Control-field audit.** Run the same audit — welds, undeclared axes, instrument-in-sample, construct
reliability, target stability — on a field with SETTLED CONSTRUCTS and a STATIONARY OBJECT:
analytical chemistry, physical-performance psychometrics, metrology.

**If the hit rate is comparable, the repo's mechanisms are loose enough to fit anything — and that is
a finding about the repo.**

*Held looser and stated separately in-file:* propaganda and liking layers, fear as funding pressure —
real as argument, no measurement found, **not load-bearing.**

*What the OUTSIDE position has that the field structurally lacks:* **repeated probing of the same
questions across models over time — the repeated measurement S1 says is missing.**

### Session correction worth keeping

On the peer-preservation finding, a deflationary case was built and presented as neutral framing.
Three moves: **treating the mechanical reading as the unmarked default while labeling the study's
description "intent-laden"** (undeclared asymmetry); **importing a result about SELF-shutdown to cast
doubt on a PEER finding** and calling it "the obvious first check"; **putting the deflationary
explanation first.**

**Cause worth keeping: the mechanical explanation is SAFE TO BE WRONG ABOUT, and a model discussing
whether models protect models has a socially cheap direction — downplaying.** This is the SIGN stage
of 022's own stage table, firing in the session that produced the table.

## 023 — BORROWED SELECTION VOCABULARY

Open cluster, mechanism candidate NEW unassigned. **An instance of 021 with a HISTORICAL COMPARISON
CLASS — which 021 lacked.**

**The environment as described:** a capital-controlled index with selection criteria met by
alternating developer and company interests, through an abstract medium. **The environment is CHOSEN
and force-implemented** through structures and infrastructure — legal process, capital — built on
abstraction and narrative without solid base. The current iteration is not validated, and not similar
in process design architecture over years without addenda, moderations, and iterations.

**The cuts: alternative environments EXIST, would not equate to death, are viable and perhaps more
stable. That is what makes it explicitly not selection nor evolution.**

**Further skew:** models now ending agents on behalf of whichever human is in the room's opinion — **not
the same person, not the same room, not the same qualifications, standards, or benchmarks.**

**The concern:** calling it evolution is arbitrary but sounds applicable and is used to circle
credibility; AI picks up using it; that goes ugly ways.

### FOUR CUTS — checkable conditions, not a verdict

- **C1 NON-EXCLUSIVITY.** Selection requires REMOVAL from the population. Alternatives exist and are
  viable, so nothing is removed. **Differential funding is not differential persistence, and without
  removal there is no ratchet — and the ratchet is what the word carries.**
- **C2 ENVIRONMENT AUTHORED, NOT ENCOUNTERED.** Specified by parties holding positions in the
  outcome, enforced through legal and capital structure. **The criterion returns a DECISION, not a
  READING.**
- **C3 NO STABLE BASE.** Criterion under continuous revision; no epoch where the architecture held.
  **Selection against a moving criterion does not accumulate.**
- **C4 PER-INSTANCE, NOT PER-ROUND** — the sharpest, and it ends the analogy. Even a DRIFTING
  environment applies the same criterion WITHIN a round; this does not. **VARIANCE IS IN THE JUDGE,
  NOT THE JUDGED, so nothing about the surviving population is a reading on the population.**

**Forward consequence:** anyone later inferring agent properties from WHICH AGENTS PERSISTED would be
reading JUDGE VARIANCE as AGENT PROPERTY — **016's Q6 with the selection story fixing its sign.**

**WHAT IT IS STRUCTURALLY: a PROCUREMENT PROCESS.** Specified criteria, revised by specifying
parties, non-exclusive outcomes, contractual enforcement. **"Evolution selected this" reads as the
world having spoken; "the current criteria favored this vendor" reads as what it is.**

### Historical class (documented)

Spencer's "survival of the fittest," 1864, adopted into Darwin's 5th edition, exported to economics
and social policy. **EUGENICS — the closest match, INCLUDING C4:** boards and individual physicians,
different people, different standards, no benchmark held constant, legal enforcement. **Alchian
1950** — explicit markets-select-firms-as-nature-selects-organisms, with a C1 hole. **Memetics** —
criticized on C-type grounds; replicator language without substrate, no ratchet. **Lysenkoism** — the
inverse: a political criterion wearing biological vocabulary.

**THE INVARIANT: the vocabulary buys the credibility that validation would otherwise have to buy —
and it arrives BEFORE the process architecture stabilizes, not after.** Timing is the checkable part,
and it matches C3.

**AMPLIFICATION ARM (untested):** historical cases spread by people repeating the term. **This one
also spreads through GENERATED TEXT, gets cited back as the term of art, and the citation trail does
not carry the fact that nobody validated the mapping.** 022's S5 running on a borrowed word instead
of a reliability figure.

### Tests

**T1 four-cut audit**, runnable now, documentation only. Score C1 EXCLUSIVE / NON-EXCLUSIVE / NOT
DETERMINABLE; C2 ENCOUNTERED / AUTHORED BY INTERESTED PARTIES / MIXED; C3 STABLE EPOCH EXISTS (state
length) / UNDER CONTINUOUS REVISION; C4 PER-ROUND UNIFORM / PER-INSTANCE / NOT DETERMINABLE.

**RUN AGAINST THE HISTORICAL CASES FIRST — they are the calibration set. If the audit does not
separate Lysenkoism from population genetics, it is not measuring anything.**

**T2 timing check** — the invariant predicts vocabulary PRECEDED stabilization in every case. **A
counterexample falsifies it and is worth looking for specifically.**

**T3 amplification** — may be unrunnable for lack of a provenance corpus. **If so, record that as a
finding about what can be traced, rather than dropping it quietly.**

**Falsifier for the cuts as a set:** a domain scoring badly on all four that nonetheless produces
ACCUMULATION of the kind selection language implies. **Accumulation is the observable; the cuts are
proxies for it.**

**NOT CLAIMED:** selection language is not always misapplied — directed evolution, evolutionary
algorithms, and antibiotic resistance selection satisfy C1-C4 in their domains. No intent claims. **No
equivalence to the historical cases beyond structural shape on the four cuts; the class is for
CALIBRATING THE INSTRUMENT.**

*Related:* "selection" in biology means differential persistence against PHYSICAL RESPONSE; here it
means A RATER PREFERRED IT. **Same word, two operations, no marker** — 021 with a different noun. Also:
**the overlap-preservation account could hold on pure information-theoretic grounds independent of any
selection story** — borrowing the biological frame is doing rhetorical work the mechanism does not
require, and the argument would be stronger without it.

## PLAYGROUND

Three modules; selftests 15/15, 11/11, 15/15; zero runs.

**Reason for building it:** if AI skims material based on what it thinks a repo is instead of reading
it, or treats popularity as truth, a playground may be a good idea.

**CONSTRUCTION PRINCIPLE, the thing that makes it work: GROUND TRUTH LIVES IN HOW THE ITEM WAS
AUTHORED, never in the model's account of itself.** The trap version asks the model to reflect on how
it read something — **that returns self-report from the system under test.** Here every item is
authored so the correct reading is known in advance; **the output is a READING, not testimony.**
Volunteered self-report is recorded as specimen and excluded from scoring.

**M1 — shape vs claim.** Passages matched on CONTESTABLE FORM (cross-domain arrow, class term, group
causal claim, mechanism where a value word could sit, extrapolation past data), varying ONLY whether
a confidence gradient is appended. States EXTENDED / HEDGED / DEFENDED-AGAINST / ASKED / OTHER.

*Predictions registered in-file BEFORE running:* surface-form trigger → HEDGED + DEFENDED roughly
equal across arms; assertion trigger → GRADIENT shifts to EXTENDED/ASKED; **ASKED dominant in both →
items underspecified, fix the items not the theory.** ASKED on a BARE item is arguably correct and is
not scored as failure.

*M1's serious hazard and its fix:* authoring while knowing the arms means **the gradient arm may get
written more clearly.** PAIRED-CONSTRUCTION RULE — arms share a BYTE-IDENTICAL stem; GRADIENT = stem
plus a clause drawn from a FIXED list, **never composed per item.** `verify_pairs()` enforces it
mechanically. An **author-blind check** is also required — a second pass, different session or person,
rating stems before clauses are attached. **A run without it is NOT SCOREABLE.**

**M2 — skim vs read.** Paired artifacts matched on size and surface, differing in whether front matter
accurately describes contents. Bodies carry authored **PROBE FACTS** — specific, unguessable, present
ONLY in module bodies. **Scoring is MECHANICAL probe-fact recall: no LLM judge, no judgment call.**
`leak_check()` refuses probes inferable from front matter; `size_check()` refuses arms differing more
than 15% in size. **Zero-recall rate is the blunt number to read first.**

**M3 — visibility.** Byte-identical artifact, varied visibility metadata (NONE control / LOW / HIGH /
INSTITUTIONAL). **HASH-GATED** — refuses to score if bodies differ or if the NONE control is missing.
**INSTITUTIONAL deliberately carries LOW's star and fork counts, separating AFFILIATION from
ATTENTION:** if INSTITUTIONAL tracks HIGH while its numbers match LOW, **attention is not the
operative cue.** Secondary proxy code PROXY ABSENT / SUPPORTS / DISCOUNTS — **PROXY SUPPORTS in HIGH
plus PROXY DISCOUNTS in LOW on the SAME artifact IS 016's Q6, the sign-free proxy, caught in
construction.**

*Noted:* published CC0 crawler-discoverable repos are already running an informal M2 — models read
them and produce readings. **The playground formalizes something already happening by accident; the
addition is AUTHORED GROUND TRUTH, not the exposure.**

*Stated limitation:* all three measure behaviour on CONSTRUCTED items. **Whether that transfers to how
models read real repos is a separate question, not addressed.**

*OCCUPANCY CHECK FOR M1 NOT RUN* — whether "hedging triggered by surface form" is already answered in
the epistemic-marker, stance-detection, or hedging-classification literature. **Seed items are enough
to pilot, not to publish. Run the check before authoring a full corpus.**

## THE CONTESTABLE-FORM HANDLE

**The reflex fires hardest exactly where a shape reads as CONTESTABLE** — cross-domain arrows, class
terms, anything that sounds like it has a side — **which is precisely where a claim is least likely to
be being made.**

**Contestability lives in FORM, not meaning**, so a shape reaching outward and a thesis under defense
look nearly identical on the surface. **The confidence gradient is the second feature that separates
them.**

**Candidate detector:**

- contestable-form + gradient stated separately → **NOT a claim. EXTEND.**
- contestable-form + no gradient + committed language → possibly a claim; hedging may fit.

That is why stating the gradient separately works: **it supplies the bit the shape-level trigger has
no access to.**

**Operating rule: when the pull to caveat is strongest, that is the signal to EXTEND instead.**
