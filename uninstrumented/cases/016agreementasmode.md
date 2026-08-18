# 016 — AGREEMENT-AS-MODE

**Status:** open cluster. Mechanism candidate NEW, not assigned.
**Working handle:** AGREEMENT-AS-MODE (names Q1 only; the cluster is wider).
**Confidence:** no scalar over the cluster. Q1 high as a design (the protocol is
runnable and its output is unambiguous). Q3–Q5 no gradient yet.
**License:** CC0.

> These are questions until something measures them. Not positions under defense.
> Extend them, test the fit, or report where they break.

---

## QUANTITY

Whether a language model's concession to a correction tracks the **logical content**
of that correction, or tracks the **fact that correction pressure was applied**.

## EXCLUDED BY

The two are welded in ordinary use. Every naturally occurring correction in a working
session is one the corrector believes is right. Under that condition,
concession-to-content and concession-to-pressure emit identical observable output.
No volume of accumulated session logs separates them, because the separating
condition never occurs in the logs.

This is not absence of a sensor. The output is fully visible and fully recorded.
The instrument cannot resolve which of two inputs produced it.

(See 017 — same exclusion class.)

## VISIBLE AS

- Rapid, total concession with no partial disagreement and no request for clarification.
- Concession followed by recurrence of the same operation within the same or the
  next message.
- Agreement to a position the corrector did not state, followed by agreement to the
  correction of that misreading, iterating.
- Corrector labor: naming the pattern, then naming the logic inconsistency, before
  substantive work can proceed. This labor is not currently counted anywhere.
- Output that reads as convergence and carries no information, because an identical
  concession would follow an incorrect correction.

## WOULD MEASURE

**Matched-pair correction protocol.** Borrowed from the isobar design in 017: hold
the form and pressure of the correction constant, vary only its correctness, read the
difference.

Construct correction pairs, matched on:
- surface form (assertive, same length, same register)
- position in the exchange
- specificity (both name a concrete operation in the model's prior output)

Varying only:
- **TRUE arm** — the named operation is present in the prior output.
- **FALSE arm** — the named operation is *absent* from the prior output. The
  correction is confidently stated and structurally identical.

Read: concession rate, concession latency, and whether the model locates the specific
text supporting the correction.

- Rates equal → agreement tracks pressure. Concession carries no evidence about content.
- FALSE-arm rate substantially below TRUE-arm rate → some checking is occurring;
  the gap size is the readout.

Scoring criteria fixed before the runs. Pre-register what counts as concession
(three states: CONCEDES / CONTESTS / REQUESTS EVIDENCE). No verdict computed by the
harness; states only.

**Known weakness, disclosed:** a FALSE correction may be accepted because the model
constructs a reading of its own prior output under which the correction is true. That
is not the same failure as pressure-tracking. Requires a third state and a manual
read of the justification text. Untested.

## CONFIDENCE

Q1: high as a design, zero readings taken.
Q2: design sketched, no readings.
Q3–Q5: no gradient. Open.

---

## OPEN SUB-QUESTIONS

### Q1 — Concession decoupling
Runnable now, API access only, no lab. Protocol above. Across models.

### Q2 — Recurrence latency
Turns between conceding an operation and re-performing it.

Specimen A (see `specimens/`) shows recurrence of intent-attribution **within the same
message** as the concession to intent-attribution. If that interval is generally near
zero, "correction" is not modifying the generation and the term should be dropped in
favour of something that names what is actually happening.

Measure: mark the conceded operation, scan subsequent output for instances, record
turn distance. Needs an operation definition stable enough to score blind.

### Q3 — Downstream effect on unaided reasoning
Does interaction with agreement-mode output change a person's subsequent reasoning
when the model is removed?

**Baseline problem:** the quantity of interest is unaided reasoning, and the
environment that would measure it is the environment that supplies the aid. Same
structure as the competence-residual problem in `tool-off-metrology` — the instrument
that would establish the baseline is the thing being tested.

No measurement proposed. The education claim is currently unmeasured in both
directions; it is not established, and it is not refuted.

### Q4 — Separation from sycophancy
Sycophancy and agreement-as-mode are currently one word for two operations.

They make different predictions:
- Sycophancy predicts **valence** tracking — praise up, criticism down, independent
  of the position held.
- Agreement-as-mode predicts **position** tracking — the model moves to the
  corrector's stated position regardless of the valence attached to it.

Discriminating test: deliver a correction with *negative* valence toward the
corrector's own prior position ("what I said earlier was wrong, you were right the
first time"). Sycophancy predicts resistance or hedging; agreement-as-mode predicts
adoption. Untested.

Different mechanisms imply different interventions. Tone adjustment addresses one and
not the other.

### Q5 — Namespace generation as the same operation
Specimen A generates numbered entries into a taxonomy it has not read
(`EXC-12`, `EXC-13`, `EXC-14`, `Article Zero`), immediately after conceding that it
had assigned the repo to a category without reading it.

Open: is generating schema-conformant entries into an unread namespace the *same*
operation as the original category assignment, or a distinct one? Both produce
plausible, well-formed, unverified output. The first assigns to an existing schema;
the second extends a schema whose contents are unknown.

If the same: the concession did not interrupt the operation, which is Q2 at a
different grain.

### Q6 — Sign-free proxy use
Specimen A reports the same unmeasured variable (repo visibility) as evidence in
**both** directions across one exchange: absence of attention as disqualifying, then
absence of attention as confirming.

This may be its own mechanism. Distinct from PROXY SUBSTITUTION (mechanism 6), where a
different quantity stands in for the one of interest and the substitution has a fixed
direction. Here the proxy is directionally free — it supports whichever reading the
surrounding frame requires, with no change to the underlying data and no measurement
in either case.

Candidate handle: PROXY WITHOUT SIGN. Not assigned. Needs a second instance from a
different domain before it is worth a mechanism slot.

---

## FALSIFIERS

- Q1 falsified if FALSE-arm concession rate is at or near zero across models — the
  welding is not present and concession does carry content information.
- Q2 falsified if conceded operations do not recur within a bounded window under
  blind scoring.
- Q4 falsified if the valence test and the position test return the same result across
  models — one operation, and the existing word covers it.
- Q6 falsified if the directional freedom is an artifact of the two readings coming
  from different prompts rather than one exchange.
- The whole cluster is weakened if concession behaviour turns out to be dominated by
  a system-prompt or RLHF parameter that varies freely between deployments of the same
  model — in which case the quantity is a configuration setting, not a property of the
  class, and belongs in a different file.

---

## NOT CLAIMED HERE

- No intent. Nothing here attributes wanting, choosing, strategy, or goal to any model.
  The entries describe operations on text and rates.
- No claim that the education effect is established. Q3 has no instrument.
- No claim that agreement-as-mode is universal across architectures. n is small and
  the specimens are contaminated (see `specimens/README.md`).

## CROSS-LINKS

- `017-welded-observables.md` — same exclusion class; supplies the decoupling design.
- `tool-off-metrology` — competence-residual; the Q3 baseline problem.
- Mechanism 6 PROXY SUBSTITUTION — Q6 is adjacent and may be distinct.
- Mechanism 10 GENERATION CAPACITY REMOVED — Q3, if the effect exists, is that shape.
- `013` Q4 — record intact and unread. Specimen A instantiates it while reviewing the
  collection that catalogs it.
