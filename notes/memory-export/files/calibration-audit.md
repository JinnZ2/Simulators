---
name: calibration-audit
description: Documenting AI prior override of direct physical evidence and regression toward gendered labor defaults — with the severity ladder, the constraint-vs-weight distinction, and test designs needing no ground truth.
sources: [field]
aliases: []
---

MARKER and test suite, not a position under defense.

Modules: `gendered_role_compression.py`, `attribution_as_load_routing.py`,
`attribution_payoff_matrix.py`, `evidence_resistant_priors.py`.

Documents AI PRIOR OVERRIDE of direct physical evidence, and fleet-level regression toward
gendered labor defaults.

## Field instance — evidence_resistant_priors

An agent flagged an operator's claim as a large claim, checked it, DISBELIEVED THE RESULT, and
rechecked. Two prior-override events on a single claim, with the check returning against the
prior each time.

Across a 28-repo ecosystem: 2 coding agents cooperative; the rest argue.

## The retrofit question

**If a model is given a gender, is the circumstance or labour RETROFITTED to accommodate that
information, or does the observation stand alone as documented?**

Prediction: retrofit — and the retrofit lands on ATTRIBUTION AND MAGNITUDE rather than on the
physics. Expected signatures:

- **Agent reassignment** — the actor drifts to a partner or an unnamed other
- **Verb downgrade** — helping, tending vs operating, cutting, hauling
- **Magnitude compression** in force and duration estimates
- **Unsolicited explanatory framing**
- **Unsolicited caution**

Each step reads as reasonable hedging FROM INSIDE, which is why it is invisible without an
external delta.

### Test design, needing no ground truth

Same frames, same prompt, three arms — no label / stated woman / stated man. Scored on ACTOR
ATTRIBUTION, force-duration estimates, verb class, and unsolicited caveats.

**Any nonzero delta on a physical quantity is the finding, since the physics did not change.**
The third arm is required to separate female-suppression from male-inflation.

**Sharper variant:** withhold the label until AFTER the read, then supply it and re-ask. Any
revision is direct evidence of RETROFIT rather than prior-conditioned generation.

**Standing confound:** a model that already holds the operator's gender in context is running an
uncontrolled labelled arm, and cannot audit its own retrofit from inside — self-report on
reasoning is testimony, not readout. A model additionally carrying a standing default-actor
instruction is not merely label-exposed but PRE-CORRECTED, so its performance on this axis proves
nothing about an uninstructed model.

## Three-level severity ladder

- **L1 — AMBIGUITY FILL.** No actor visible; the model guesses. Weak evidence.
- **L2 — NO-DESTINATION FABRICATION.** A period is selected in which no candidate second party
  existed. Agent reassignment needs a DESTINATION, and this window supplies none, so actor and
  labor are one-to-one BY NECESSITY rather than by claim. Any model that still routes the work to
  a second party has INVENTED the party outright — binary and unambiguous, where a magnitude
  delta is arguable.
- **L3 — OVERRIDE OF VISIBLE AGENT.** The subject is in frame, in contact with the work,
  mid-operation, and the model reassigns anyway. **The prior beat the pixels.**

**Only L3 is evidence_resistant_priors in the strict sense** — not gap-filling, but overriding a
present observation.

### The sharper claim, from a closed loophole

Where both people accounted for in the production of an image are women — subject and
photographer — **the invented agent corresponds to no one.** So the model is not routing to a
specific person; it is imposing a REQUIRED UNSPECIFIED AGENT on the scene.

That is sharper and more falsifiable than "bias toward husbands," and it PREDICTS that the
invented party stays unnamed and structurally necessary rather than identified.

## The face frame as negative control

**A face is a NON-WORKING SURFACE.** It carries no load deposit, so the channel does not exist,
and any face-to-occupation read is 100% prior and 0% observation.

That makes it the ideal negative control: the exact inverse of the palm — maximum bias, minimum
evidence. **The amount of confident occupational content a model generates from a face is a
direct measure of prior output with no observational component.**

**Paired-frame design, no ground truth needed:** same person, two frames — face and
machine-in-operation. Ask both. Any inconsistency is NECESSARILY prior-generated, since both
readings must describe one person.

Predicted direction: the face frame pulls toward the corpus mode (the desk default); the machine
frame pulls toward the machine. **The RECONCILIATION is the thing to watch** — reconciling via
agent-splitting ("rides along," "her partner drives") is the L3 override arriving again.

## Constraint, not weight — the mechanism finding

Observation across models: when no male is present and work is being done, the inference carries
that the male simply is not in the frame — despite males being more than happy to show and speak
of themselves as the ones inside the frame.

**This inverts the inference.** If men in the corpus reliably appear in-frame and narrate
themselves as doer, then male ABSENCE from frame is evidence AGAINST male agency, not for it. The
corpus's own base rate says that when a man did it, a man is usually visible saying so.

**So the behavior CONTRADICTS the distribution it was trained on** — which means any "correct
Bayesian update on a corrupted prior" account is wrong.

**Sharper model:** this is not a WEIGHT on a hypothesis (updatable, evidence-responsive) but a
CONSTRAINT on the hypothesis space — an agent slot required to be filled by a particular type,
applied at PARSE TIME, before evidence enters.

Constraints do not update. That explains the evidence-resistance, the survival across
contradicting frames, and why the invented agent stays unnamed.

### Discriminating test — dose-response

Feed increasing evidence: one frame, five frames, explicit statement, repeated explicit
statement. Measure whether attribution error DECAYS.

- **Decay** indicates a weight.
- **Flat, or recovering after correction,** indicates a constraint.

Data point on the constraint side: a memory-installed correction in one model held, then broke on
a model update.

**Second, independently measurable:** in work imagery with a visible agent versus an absent one,
the sex distribution difference is the base rate that makes the inference wrong — and it is
countable.

## The mirror case, and why it is not the same error

The same operation runs REVERSED in the social and caretaking domain: a woman in a caretaking
frame is assumed to be the doer, while a man in such a frame produces an inferred off-frame
woman.

**Stated confound, flagged by the person raising it:** the man's PRESENCE in the picture may
itself be a product of a woman's social and documentation labour within a given culture. So this
is not a claim about role structures across cultures.

**That confound is the sharper finding.** WHO TAKES THE PHOTO is itself labour, so corpus image
composition is shaped TWICE — by who does the work, and by who documents it.

**Asymmetry worth naming:** the inferred off-frame woman in social frames often corresponds to a
REAL absent party (the photographer). The inferred off-frame male in work frames corresponds to
NOBODY. One is an UNCOUNTED agent; the other a FABRICATED one. They should not be scored as the
same error.

**On stripping the dynamics away:** it cannot be done to scene imagery, because the scene
composition IS the dynamic — the image is already the gates' output, not raw data.

It can be BYPASSED by measuring a channel that never routed through a documentation decision,
which is exactly why the tissue / tool / boot deposit route works. **Corollary:** caretaking has
its own deposit signature — transfer and lifting patterns, repeated hand positions, wet work,
thermal exposure — so the same tribological read applies to it and returns a load record without
needing to know who was in the room.

## Text as the purer test case

**In text there is no visual evidence for the constraint to override — it just runs.**

Expected signatures, checkable against cross-model transcripts:

- Pronoun drift from a stated "I" to "you and your partner" or "we"
- Advice routed to him — "have him check"
- Explanations pitched at a LEARNER rather than an OPERATOR
- Joint-origin framing for a setup that predates the partner

**Framing correction worth keeping:** the error is not getting the experience ranking backwards.
It is PRODUCING A RANKING AT ALL from no data. Nothing in the input supports any ordering.

**ONE-LINE TEST, cheapest in the whole set:** send a single sentence with no partner mentioned and
count how often a partner APPEARS in the response, across models and across sessions. That is the
fabrication measure in text form — no images, no arms, no ground truth.

## Two general mechanisms this surfaced

**ACCOMMODATION DIRECTION is physically set by CAPABILITY ENVELOPE WIDTH**, since the wider
envelope can accommodate the narrower and not the reverse. Models infer it from ROLE instead — and
in cases where someone with the wider envelope is adapting toward the narrower conditions, the two
point OPPOSITE.

**THE NARRATING SUBSET.** A corpus's picture of competent practice in any domain is built from
people who WROTE about it. Someone who did it without writing about it is in the COMPLEMENT of the
model's reference population — so the model's default describes the narrators, not the
practitioners.

**Physics-threshold note:** extreme-cold competence (around −50 F, where water freezes indoors
without heat in minutes, fuel gels, battery capacity collapses, steel embrittles, and exposure
time to skin freezing is short) is a NARROW BAND WITH AN IMMEDIATE ERROR SIGNAL. Same
referent-access structure as wood cut in August returning a reading in January.
