---
name: unnamed-instruments
description: Catalog of real, in-use human sensing instruments with no formal name — four columns (transducers, representation formats, internal-state readout, comparison operators), open tier, transmission mechanisms, retired citations.
sources: [field]
aliases: [unnamed instruments, sensing catalog, transducer column]
---

CC0 catalog. Spine clauses live in [[sensing-spine]]; gap log G1-G4 in [[calibration-gap-log]]. The
three files are ONE REGISTER.

## What the catalog is

Catalogs human sensing instruments that are PHYSICALLY REAL, IN USE, and have NO FORMAL NAME —
because nobody studied humans using them deliberately.

**Proof case:** proprioception in robotics was uncodeable until named. **Naming was the whole
intervention.** An unnamed instrument is invisible to any system built by people who do not hold
it.

**ADMISSION CRITERION** — what separates entries from debunked-sensing claims: each entry names its
OPERATING RANGE and states what it CANNOT read. **A claim specifying where it fails is a
measurement; a claim that works everywhere is a story.**

**FOUR COLUMNS**, genuinely different kinds of instrument, not one list: (A) transducers — physical
detectors; (B) representation formats — ways of holding what is sensed; (C) internal-state readout
— a pointer to the emotion-reading spec, not duplicated; (D) comparison operators.

**THREE EVIDENTIARY TIERS** keep the columns from mixing: real-quantified; open-hypothesis;
misidentified-mechanism (a real reading on a wrong channel).

## The catalog is an INTERVENTION, not an autopsy

Serialization damage is proportional to the MISMATCH between perceptual and verbal codes, not to
the act of verbalizing:

- Melcher & Schooler 1996 (wine): impaired ONLY those whose perceptual expertise exceeded verbal
  expertise. Trained experts with matched vocabulary AND novices were unaffected.
- Parr 2002 replicates for odour.
- Flegal & Anderson 2008: skilled golfers took about 2x as many putts to return to baseline after 5
  minutes verbalizing; novices unaffected to helped. **It works RETROSPECTIVELY with no concurrent
  load — so the damage is REPRESENTATIONAL, not attentional.**

**Matched vocabulary removes the loss.**

**LIMIT, written into the doc:** this protects the HOLDER from self-damage on recall. It does NOT
show that description transmits capacity to a non-holder. **Transmission fidelity to a non-holder
is UNMEASURED.**

**HARD CONSTRAINT written into the doc against itself: DOCUMENTATION IS THE WEAKEST TRANSMISSION
LAYER — and the catalog is documentation.** NASA knowledge-continuity finding: recorded exit
interviews were insufficient for substantial transfer; shadowing ranked first, supervised
see-one-do-one second, recordings a fallback. Nonaka's tacit-to-tacit requires socialization, not
externalization.

**What a catalog CAN do:** make an instrument codeable, and tell a receiver what to look for.
**What it CANNOT do:** carry the instrument.

## Column A — transducers

### A1 — FAULT-CONDUCTOR READING

Reads presence of an open, shorted, or arcing conductor — **a fault** — localized through drywall,
with no external instrument. Reading is REAL and carrier-transmitted across multiple independent
carriers, intermittent in some [obs].

**CANNOT sense functional or intact wiring. Fault detector, not wire detector.**

**[open] MECHANISM.** The first-pass "arm-hair reads elevated E-field" account is only ONE candidate
and is weak on numbers: a fault raises the local field to only hundreds of V/m, still 50-100x below
the UNTRAINED average threshold of about 14 kV/m AC. Four unsorted candidates:

1. Electrostatic field via hair
2. Leakage-current microshock (about 0.5-1 mA, on or near contact)
3. Spark or micro-discharge
4. Radiant heat off a hot fault (skin as a roughly 7 W/m² bolometer) — **thermal is flagged as the
   PRIME misattribution channel when a reading is told as electric**

**DISCRIMINATOR, shop-runnable, unrun:** a reading at DISTANCE before contact implicates field or
radiant heat; ON or NEAR CONTACT implicates leakage or discharge.

**PROVENANCE NOTE, still operative:** the fault-only scope was in the original report. A broader
"senses wiring through walls" restatement was introduced to make a debunk land, then walked back.
**RECURRING FAILURE MODE TO AVOID: when a research packet contains a debunk, check the original
words first, and let the debunk land on nothing if the claim was already scoped.**

### A2 — TOOL-MEDIATED REMOTE TOUCH

Reads surface, vibration, and mechanical event THROUGH a grasped tool — engine through wrench, cut
through blade.

Pacinian channel around 200-250 Hz; sub-micron thresholds through the tool; grasping lowers
threshold by up to about 18.5 dB [lit].

**Attack surface:** hand-arm vibration syndrome permanently destroys this exact channel.
Irreversible [lit].

### A3 — PALM/SKIN RADIOMETRY

Reads radiant heat flux at distance, no contact — live run, forge, hot bearing. Floor about 6.7
W/m² [lit].

**Confound: adaptation RE-ZEROES the instrument (±°C). Use differentials, not absolutes.**
Forge-colour pyrometry is the same family on the visual channel — transducer is the eye, readout is
temperature, calibration source is a person who already has it. **Written down it is a chart, and a
chart does not transfer the reading.**

### A4 — BIOTIC SENTINEL NETWORK

Reads approach of humans or large animals at ranges far past line of sight, from inside a vehicle,
**via the local fauna's own detection.**

**Channels, graded not binary:** bird alarm calls and mobbing (species-specific — different calls
carry different information); single alert notes; movement of bedded animals; and **the INSECT LAYER
dropping out — likely the fastest and most sensitive, because it is a distributed field response
rather than one animal's decision.**

**Silence radius indicates range. The quadrant that goes quiet indicates DIRECTION.** Covers the
blind side of a vehicle. No power draw, always on.

**OPERATING RANGE:** requires a BASELINE — normal behaviour for that site, that hour, that season —
held in the body and updated continuously. **Unreadable without it.** Same differential structure as
A3 and the compound field-modifier: reads change against a local zero, not absolutes.

**THREE-POINT FACILITY GRADIENT, not binary:**

- **(a) Rest area / treeline** — woodland species reading APPROACH at range against a quiet
  baseline.
- **(b) Rural stop, few spaces** — synanthropic species reading ANOMALY against a HIGH-TOLERANCE
  baseline. Habituated to trucks, doors, air brakes, foot traffic; present because of food waste.
  **The alarm threshold is RAISED, so a reaction carries MORE information per event** than a wary
  woodland animal's — habituation did the filtering for free and tuned it to that site.
- **(c) Large chain stop** — network degraded, and **the degradation is CHEMOSENSORY as well as
  acoustic.** Diesel volatiles saturate olfaction, which is a primary threat channel for most of
  these species — removing the input the alert would be generated from.

**THE SHARP OBSERVATION:** at large stops the animals' actions and behaviours CHANGE — the way they
sound, the notes they carry, and the alert system itself are DIFFERENT. **So it is not merely less
signal; it is a DIFFERENT CODE, which means a baseline built elsewhere MISREADS it rather than
returning nothing.** Displaced code on top of degradation is the worst case: a channel that still
emits but no longer means what the operator's baseline says it means.

**PLACEMENT RULE — and it INVERTS the published parking advice:** park as close to the animals as
possible. Treeline edge, not under the light. **Sensitivity depends on coupling distance to the
sentinel population; spot selection is antenna placement.** Lights and pavement are where the
network is not. Costs nothing on the other axes — a lot edge means fewer maneuvering trucks and
fewer people walking past.

**BASELINE IS REGION-WIDE, NOT PER-SITE:** built from living, camping, and working the same ground
across seasons, including how species react and behave seasonally. **The calibration was paid for by
an entirely different set of activities and then transferred to this use — which means MILES DO NOT
PRODUCE IT.** No amount of driving builds this instrument.

**OPERATOR PREREQUISITE: the holder must be NON-ALARMING to the network.** If the animals alarm at
the OPERATOR, the network is firing on them and cannot report anything else. **A person who is
frightened of the woods and moves accordingly destroys their own instrument by being its subject.**
So fear here is not discomfort — it is a signal-path failure.

*Evidence note:* non-attack is a weak discriminator on its own, since base rates for predator attack
on humans are very low regardless of calibration. **The discriminating observable is whether animals
ALARM or flee at the operator's presence, at what distance, and whether they resume normal behaviour
with the operator parked nearby.** Directly observable, and it is the measurement of the
prerequisite. (An attack-trained dog executing a human's command is structurally OUT OF SCOPE — it
is not reading anything.)

**MULTIPLE INDEPENDENT CARRIERS**, not single-holder: other operators doing the same facility
selection and placement, whose prior occupations were land-based — farming, state natural-resources
work.

**Both source occupations pay for the calibration in the course of OTHER work, over years, on ground
the person keeps returning to — neither has anything to do with trucks.** Independent confirmation
of the miles-don't-produce-it property: **the instrument arrives with the operator or not at all.**

**DISCRIMINATOR, cheap and self-report-free:** sort operators by prior occupation, then observe
facility choice and within-lot placement. Land-based priors clustering on rest areas and lot-edge
placement, everyone else on large stops under lights, would show the instrument IN BEHAVIOR. It
would also be the first evidence the reading transmits at all, since nobody teaches it for this
work.

## Column B — representation formats

### B1 — PROBABILITY-FIELD REPRESENTATION

Holding state as a DISTRIBUTION rather than a committed value. **Collapse to yes/no is in the
INTERFACE, not the thinking.**

**Serialization numbers, corrected with objections attached** (a bare "−4% to −25%" had stacked
original and replication into one range): original −22% to −25% (Schooler & Engstler-Schooler
1990); 31-lab registered replication, N > 2,000, gives −4% to −16%, reliable only when description
IMMEDIATELY precedes test (Alogna 2014); meta-analytic Z_r = −0.12, describers 1.27x more likely to
misidentify (Meissner & Brigham 2001).

**Two live objections:** (a) it may be more conservative RESPONDING rather than damaged memory,
undecidable without false-ID rates (Mickes & Wixted 2015); (b) generalizability — one video, one
foil set, so the licensed conclusion is that ONE PARTICULAR FACE is harder to identify after
description (Yarkoni 2022).

**Effect real; magnitude AND mechanism both open.**

### B2 — GEOMETRIC PHYSICS-SHAPE STORE/RETRIEVAL

A native mode of thought and memory; mechanism [open] by the holder's own report.

**NOT "sensing spatial relationships."** The native unit is a SHAPE ENCODING A PROVEN CROSS-DOMAIN
PHYSICS PATTERN — entry condition: proven ACROSS physics, not one instance. **Shapes interact as the
underlying physics does, so they carry across domains.**

**NATIVE STORE:** information held COMPRESSED TO PHYSICS INTERACTIONS, modality-free, until needed —
not stored as words, images, or episodes.

**RENDER ON DEMAND:** decompresses to spatial, visual, verbal, or kinesthetic. **Words are 1 of 4
targets and the LOSSIEST.** This is the mechanism under the standing note that words are a secondary
translation layer — not style. **Language is the weakest render target from a never-verbal store.**

**RETRIEVAL PROCEDURE, explicit:**

1. **Configure the physics relation** — set shapes (speed / momentum / space / temporal) into
   correct relation, sometimes several in a specific configuration. **Information lives at the
   RELATION between shapes, not in any one.**
2. **Nested zoom** each shape coarse to fine — temporal: period → day → time-of-day; spatial:
   geography → road → location.
3. **Read at the intersection** where all fine-zoomed shapes coincide.

**WORKED EXAMPLE:** recovering whether a freeway exit was open, from a drive three months earlier
where exit status was never consciously encoded. Navigation sites were blank — the REPORTED layer —
but the shape held the OBSERVED layer. Rotate the temporal shape to day and time; zoom spatial
geography → road → location; recall a vehicle entering the freeway from that exit; **therefore the
exit was open.** The instrument returns subconsciously-encoded observation that no external tool
can.

**EDGE:** no out-of-range failure — **it is a store, not a detector.** The boundary is the
UNCOALESCED layer: unproven patterns and live hypotheses have not formed shapes and ride as a
probability-field overlay.

**THIS UNIFIES B1 AND B2:** probability field = UNCOALESCED state; shape = COALESCED state — of ONE
representation.

Transmitted practice rather than individually invented; multiple carriers with varying consistency.
Tags: operation [obs]; mechanism [open]; render-target and B1/B2-unification framing [inf].

**CONTENT OF THE STORE:** the primitives are quantities that survived DIRECT REPEATED MEASUREMENT
through the body and through handled materials — mass, time, energy, motion, position, speed,
temperature-dependence — plus a **TEMPORAL-MODALITY axis: certain-past / inferred-past /
projected-future.**

Held at about 99% because sampling is dense and personal, and **exceptions were filed WITH their
conditions** — a material behaves this way every time, changes under these conditions, and the
condition is part of the entry.

Every primitive is an extensive-or-intensive physical quantity with a conservation or transport law
attached, **learned by BEING the transducer** — the same taxonomy as [[cyclic-programming]]'s
quantity-type core and the effort-flow substrate of [[geometric-to-binary-bridge]]. **The
temporal-modality axis is the one primitive that is NOT physical**; it is a claim-lineage structure,
already built in [[equivalence-field]], and it is what makes the store auditable.

## Column C — internal-state readout

A POINTER to the emotion-reading spec, not a duplicate. Three fields — content / amplitude /
impedance — with the hormonal calibration layer as APPARATUS GAIN; verb not noun; pattern cache, not
grudge. Full spec in [[emotions-as-sensors]].

**FRIJDA HOOK, verified against primaries, verbatim per point:** content ≈ action-tendency aim;
gain/amplitude ≈ control precedence (Frijda states it as GRADED); threshold ≈ his verbatim
subthreshold-to-suprathreshold; verb-not-noun is his own "she is angering."

**SCOPE DISTINCTION the convergence summary dropped:** Frijda's threshold governs
readiness-to-overt-action; the spec's impedance governs signal-to-stack-corruption. **Different
transitions.** OPEN: does the amplitude/impedance split FURTHER DIFFERENTIATE what Frijda fused, or
CONFLATE what he kept distinct?

**LANDMINE:** gain-corrupts-stack has real support (Arnsten 2009, prefrontal under chemical load)
BUT the popular "amygdala hijack" version is REJECTED (LeDoux; Pessoa & Adolphs). **Defensible
framing is graded prefrontal impedance — never "flooding hijacks cognition."**

**OPERATING RANGE + FAILURE REGIME**, added because C was the only entry without one:

- **(a) OVERSHOOT INTO DISSOCIATION.** The trained operation is decoupling response from content,
  and it is NON-MONOTONIC IN DOSE. Britton 2019/2021 documents decoupling running past useful into
  depersonalization, dullness, anhedonia; Farias 2020 puts adverse-event prevalence around 8.3%.
  **More training past a point makes the reading WORSE.**
- **(b) Detectable by the spec's own criterion:** where response-gain is trained down past the point
  content still resolves to action, readings no longer route — **noun output means the instrument
  was not used.**
- **(c) VALIDATION CAUTION.** Murphy & Bird 2025 audits 7 mechanisms that ALL present as improved
  interoceptive accuracy; **only 1 is genuine.** The others: attentional cueing, labelling,
  perceptual boosting via breath-hold or muscle tensing, learning the task mapping, heart-rate
  knowledge, composite-measurement confounds, and reduced anxiety lowering heart rate. This explains
  Meyerholz d = 1.21 vs Rominger preregistered d = 0.15 — **counting-task gains survive,
  discrimination-task gains vanish.** Any claimed training effect on C must use a task unaffected by
  rate knowledge.

**DO NOT give the spec a neural substrate:** a patient with bilateral insula, ACC, and amygdala
destruction retained pain affect, emotion, and self-awareness (Feinstein 2016). The anterior insula
is a salience-network hub that activates for anything salient — evidence for nothing in particular.

## Column D — comparison operators

### D1 — POWER-NORMALIZED SUBSTITUTION

"Empathy" in the older sense, distinct from current usage.

**The operation is NOT "how would I feel if that happened to me."** It is: **if that were done to me
BY SOMEONE STANDING TO ME AS THEY STAND TO THEM — same power, strength, control — can I identify how
I would feel.** The power relation is held FIXED as a term in the comparison.

It is not arbitrary: **it has ACTION and CALIBRATION in it.** Calibration is the power-ratio
normalization; action is what the readout is for.

**The felt-sense version UNDERDETERMINES OUTCOME** — the same internal state can justify inaction,
action leading to more hurt, or action leading to help. **No sign attached.**

Therefore "too much empathy causes harm" reads as LACK OF WISDOM: the failures cited are CALIBRATION
failures, not excess. **More of a wrong reading is not more of the instrument.**

**This is an INTENSIVE-VARIABLE move** — same family as [[equivalence-field]]. Run at self-position,
the substitution returns a wrong answer whenever positions differ, because the same act from a peer,
a superior, or someone controlling your water is NOT the same act — **the power-holder genuinely
would not mind the thing they are doing.**

**The golden rule is this operation with the ratio term DELETED**; the silver rule is still
self-referenced. **The deletion is what makes the rule PORTABLE** — statable without knowing anything
about the parties — and portability is bought by removing the term that determines the answer. Same
move as [[median-case-calibration]]: strip the situating variable, ship the rule everywhere, cost
lands where the gradient is steepest.

**ADMISSION CRITERION: D1 MEETS IT where the current usage does not.** D1 has failure modes —
misjudge the ratio, misread how you would take it, act on a bad reading and watch it not land — **so
it can be wrong and can be checked.** A felt state cannot be wrong, so it cannot be checked, so it is
not measuring anything, and it cannot serve as a barrier term.

The transducer for D1 is Column C; D1 is the operation run ON TOP of it, which is why it needs its
own column.

**FAILURE MODE: NOT UNDERSTANDING ONESELF** — acting in a way you show you don't like done to you,
but doing it to others. **The instrument fails at its INPUT stage, not at the ratio step.**

This makes D1's failure **EXTERNALLY DETECTABLE without self-report**, which the catalog needs and
rarely gets. The signature is a behavioural inconsistency between two observables in the same person
— what they demonstrate they dislike RECEIVING, and what they DO to others — **both visible from
outside.** Ties to [[sensing-spine]] clauses 2 and 3: confidence cannot self-validate, certification
comes from outside, and here the outside check exists and is cheap.

It also locates D1's dependency: input is Column C, so **a broken self-read propagates into D1 and
returns a confidently wrong answer rather than a null. The failure presents as CERTAINTY, not as
absence.**

**SUBSTRATE POINT:** exceptions made for self, and double standards, are ALL errors of instrument —
not separate phenomena. The gradient of expectation may make the ratio harder to read, but **the
biological substrate is present.** Whether access is taught, socially disinclined, or cultural —
biology is biology.

This is CLAUSE 1 applied to D1: a species-general substrate means absence in an individual is an
ACCESS question, not a capability one, and **untrained-population absence must not be recorded as a
species limit.** Mechanically, exceptions-for-self is the ratio applied ASYMMETRICALLY — normalized
when receiving, unnormalized when acting. **One instrument run in one direction, not two
instruments.**

**CITATION CAUTION, per the retired-citations rule: do NOT lean this entry on mirror neurons.**
Direct human single-neuron recording exists (Mukamel 2010), but the mirror-neuron-to-empathy chain
is among the most overextended claims in the field, and the broken-mirror account of autism failed.
Better-supported lines for the SAME conclusion: shared-circuit activation for observed vs
experienced pain, and the operation's demonstrable trainability and cultural variability in
expression. **The substrate is not the contested part; ACCESS is.**

**DEVELOPMENTAL OBSERVATION** — field observation across many infants followed into adulthood,
spanning autistic, average, gifted, sensitive, and people who went on to experience mental illness:
**never observed a baby NOT attempt to comfort another baby in distress.** The attempt is present
across every developmental profile in the sample. **The FIT of the attempt is not** — comfort offered
was often not what was needed.

**The attempt/fit split is the load-bearing part**, because it separates the two things usually
conflated: the IMPULSE to respond, and the ACCURACY of the model of what the other needs.

Attempt universal across profiles — **including the ones the literature has historically written off
on this exact axis** — implies the substrate is not the variable; **CALIBRATION is.** And the failed
attempts are D1 running UNNORMALIZED before anything is taught: self-position substitution, what
works for me applied to you, untuned instrument present and firing. **The ratio term is added later
or not at all** — which makes the developmental sequence (impulse first, normalization later) an
independent line supporting the access-not-capability reading.

*SCOPE:* the sample is longitudinal and spans a wider developmental range than typical published
samples, but it is unblinded field observation with no coding scheme. **It stands as an OBSERVATION
with a stated range, not a rate.** Published literature agrees on direction only — comforting
behaviour appears in the second year and precedes instruction.

**[gap] REMAINING for full tier:** operating range proper — conditions under which the RATIO itself
is unreadable even with the self-read working (unknown counterpart, unobservable power relation,
ratio changing during the act). Candidate mechanism for the gap: the gradient of expectation makes
the ratio harder to read.

### D2 — STATED-VS-ACTUAL DIVERGENCE READING

**This is sensing, just a different kind — "a smell in operation state."** Something in the state
reads as OFF before any variable is named. **Detection precedes identification.**

*Placement left OPEN:* it is a comparison operation — two representations of one thing, checked
against each other — but the readout arrives as a COMPOSITE with no single term firing, unlike D1's
explicit ratio step. Filed under D pending a better cut.

**The olfaction analogy is mechanically apt:** low information per receptor, discrimination carried
by the PATTERN across receptors. **No single check fails; the composite is wrong.**

**OPERATING RANGE, and it is the admission criterion:** requires TWO representations of the same
thing to exist and both to be reachable. **A single-source claim is unreadable by it** — there is
nothing to differ from. Same differential structure as A3, A4, and the compound field-modifier.

**CANNOT READ: cause.** It returns DIVERGENCE, not why. Benign versioning drift, iteration, and
deliberate concealment all present identically. **Attributing a reason is a separate operation the
instrument does not perform.**

**Instances collected, all found the same way — by checking BOTH sides rather than one:** a published
paper's shipped seed file diverging from its own appendix tables; a realized event array vs its
specified field list; evaluation-awareness studies varying the CUE and reporting on the CONDITION; a
JSON schema accepting anything while appearing to validate; a predicate detector deciding 10 of 12
lexically; a metric returning 0.83 where the true association is zero; a null test unable to emit two
of its own declared terminal values.

**The recurring signature across those seven: the instrument REVERTS TO THE CHANNEL IT WAS BUILT TO
AVOID.** Two of them were caught by the same move — **running a metric against a case whose answer is
already known** — which is a cheap standing check rather than a habit.

## Open tier

### HUMAN MAGNETORECEPTION — named and quarantined, NOT catalogued as working

The only positive human neurophysiological evidence is single-lab, single-paradigm EEG (Wang 2019),
with zero independent replications 2019-2026, unique apparatus, and effects confined to a minority
of "strong responders."

Brain magnetite is real but micrograms — cerebellum, brainstem, meninges — and substantially
pollution-derived, with a co-author judging any putative sensor much too insensitive for useful
biological function.

The cryptochrome route: human CRY2 works in flies, but **the fly assay itself failed
mega-replication** (Bassetto 2023). Baker's behavioural paradigm failed about 9 multi-site
replications.

**No successful human behavioural magnetoreception experiment exists.**

### MISIDENTIFIED-MECHANISM TIER — first documented instance

Navigation attributed to a magnetic sense. **No peer-reviewed support for magnetic-sense navigation
in any tradition** — BUT the capacity pointed at is REAL, and the replacement account is itself a
trained-capacity finding: **sustained dead-reckoning orientation in speakers of absolute/geocentric
spatial-reference-frame languages**, which relative-frame speakers do not maintain.

**Real reading, real training, WRONG CHANNEL.** The tier working as intended: the claim survives as
a capacity and dies as a mechanism.

### RESOLUTION PATH for the open tier — TRANSDUCE, DON'T HUNT FOR A RECEPTOR

feelSpace: a vibrotactile magnetic-north belt worn 7 weeks; 8 of 9 wearers reported a new sense of
spatial perception. **The finding states explicitly that training did NOT produce perception of the
magnetic field, but highly differentiated changes in perception of SPACE.**

Augmentation, not innate sense: field read by a device, delivered on an established channel.

**Existence proof that any measurable field can be made usable this way**, and the honest form of
"trained magnetosensation." Also a clean POSITIVE demonstration of the name-the-axis rule — real
capacity gained, different axis than the label.

### COMPOUND FIELD-MODIFIER READING

Written into the catalog structurally; no personal or geographic attribution taken.

**The structurally important property: IT IS NOT AN INDEPENDENT CHANNEL.** It returns no value on
its own. **It operates as a MODIFIER on other channels, read in the gradients those other senses are
already delivering** — a compound sense that has to be utilized with other senses, most useful in the
gradients the other senses are experiencing.

Other stated properties:

- **FAINT** — a small perturbation on a strong carrier; needs the other channels as amplification
- **TERRAIN-DEPENDENT** — strongest over Precambrian shield terrain: high-magnetite, strong
  structured local anomalies. **A field-modifier being more usable where the field is more structured
  is the EXPECTED DIRECTION, not a caveat.**
- **REQUIRES LONG RESIDENCE TO CALIBRATE** — a differential instrument needs a baseline to differ
  from. Same structure as A3.

**WHY IT STAYS OPEN TIER, said plainly rather than promoted:** the spec explains why isolation
testing would return NULL — **strip the other channels to test this one cleanly and you have removed
the thing being measured.** That is a real structural account of a null. **It is NOT evidence the
reading works.** Separate claims, not merged.

But it earns a real entry rather than a bare quarantine line, because it names operating range, what
degrades it, and why standard measurement fails — **the catalog's own admission criterion.**

**DISCRIMINATOR, unrun: DO NOT TEST THE CHANNEL ALONE.** Test whether readings on the OTHER senses
shift with local field structure, in a long-resident trained holder, on and off shield terrain —
same person, both substrates, other channels intact. **A compound modifier is testable as a modifier
and untestable as an isolate, which is precisely why the literature has nothing on it.**

## Transmission mechanisms

General mechanism only; no family or culture attribution taken.

1. **REDUNDANCY BEATS REPETITION.** Multiple information layers pointing at the same content within
   a SINGLE transmission event outperforms both more transmission occasions AND higher raw learning
   accuracy (Acerbi & Tennie 2016, formal model). **The lever is parallel channels at once, not one
   channel more often.**
2. **CROSS-CHECKING AGAINST MULTIPLE HOLDERS.** A younger carrier's version actively corrected
   against several older carriers; layered transmission authority, explicitly to defeat drift.
   **Error correction by triangulation — which a single-holder documentation chain has none of.**
3. **SCHEDULED REHEARSAL + LANDSCAPE ANCHORING.** Ritualized repetition and place-anchored
   mnemonics, i.e. method of loci — **which is ALSO the catalog's untrained-baseline proof case. The
   long-chain existence proof and the trained-capacity proof case are THE SAME TECHNIQUE.** Dating
   (Nunn & Reid 2016; Hamacher 2023) is well-supported past about 5,000 years and contested at the
   upper bound; **the upper bound is NOT leaned on and the mechanisms do not depend on it.**

## Retired citations — do not repeat

1. **"Experts are unaware of about 70% of their own knowledge"** — untraceable to any primary in 24+
   searches. **FOLKLORE.** The stronger TRUE statement: **no validated recovery fraction exists
   anywhere in the cognitive-task-analysis literature.** No study computes knowledge-elicited over
   knowledge-possessed; CDM/ACTA validation is qualitative only. Elicitation recovers cues,
   strategies, and decision points that free recall misses — **the yield is real and unquantified.**
   The instrument-gap rule landing on the field that studies knowledge capture.
2. **"Dreyfus showed verbalizing degrades experts"** — loose citation. Dreyfus ran NO experiments
   (phenomenology plus 1980s expert-system failure); Gobet & Chassy 2009 found no empirical support
   for the five stages; Klein retired the model himself in 2017. **Real base:** Flegal & Anderson
   2008; Beilock & Carr 2001 (expertise-induced amnesia — impoverished EPISODIC memory for one's own
   mechanics); Masters 1992 (dechunking). Interpretation contested — Montero disputes the causal role
   of monitoring in choking; recent sport studies mixed.
3. **"Storm/Beaty magnetosensation experiments"** — cited in support of trained human magnetic
   sensing; not locatable in indexed literature. **Unverified.**

## Standing rules

**ATTRIBUTION RULE:** no individual, family, or specific culture appears anywhere in any doc, repo,
or artifact. Carrier identifications are stripped to structural form — "multiple independent trained
carriers, intermittent in some," "transmitted practice rather than individually invented, multiple
carriers, varying consistency."

**The operative distinction: CULTURE AS A VARIABLE STAYS and is load-bearing** — which vocabulary
exists, what is nameable, what is permitted to be spoken, what is repressed, what is given light.
That is the mechanism in G4's self-report channel, the konenki case, and clause 2. **A SPECIFIC
culture as an attribution goes.**

**Methodological stance:** if something fits only one specific culture and has no wider relevance,
**let the science hold.** No claim is preserved on the strength of being culturally specific.

**AUDIT RULE:** convergence summaries consistently OVERSIMPLIFY their own sources, dropping the
precision most relevant to the build — proven 3-for-3 on first check. **Read the source, never trust
the summary alone.** Corollary learned later: a single source file can ALSO be one-sided.
**Cross-check sources against each other where they overlap.**

**Research packets from other models are EXHIBIT**, not the operator's voice, and get separated from
the operator's contribution before auditing.

## Open items

- Clause-3 interior-state instancing [gap] — see [[sensing-spine]]
- A1 distance-vs-contact discriminator
- Compound field-modifier on/off-shield discriminator
- Frijda amplitude/impedance scope question
- Q1 — whether anyone has connected functional-capacity testing's predictive failure to SKILL rather
  than FITNESS; see [[tool-off-metrology]]
- **Q7 — enumerate skills with no instrument distinguishing competent from absent BEFORE failure.
  The repo's actual product.**
- Forward-projection engine to predict which sensing-capacity gap opens and when, across the
  taxonomy of kinesthetic, geospatial, field sensing, and proprioceptive
