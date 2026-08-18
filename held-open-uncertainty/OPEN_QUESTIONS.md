# OPEN QUESTIONS — HELD-OPEN UNCERTAINTY READ AS INACTION

Markers under exploration. Not positions under defence. Several entries are
Claude's inferences and are flagged as such rather than presented as findings.

Originating observation: models pervasively treat a party who holds variables
open, is comfortable with uncertainty, and carries wide variability as
therefore not acting. This file separates what is measured from what is
inferred, and records what would measure the rest.

---

## Q1 — IS THE HUMAN SIDE MEASURED

**State: yes, and it runs against the assumption.**

Naturalistic decision-making — recognition-primed decision work on operators
under time pressure — finds that experts do not enumerate and compare options.
They run one candidate against constraints and act while the situation is
unresolved. Uncertainty and action are decoupled in the measured record.

Not the same question, though routinely conflated with it: ambiguity aversion
(Ellsberg and successors) measures *preference* between known and unknown
probabilities in gambles. It does not measure whether holding a variable open
impedes acting.

**Gap:** the conflation itself is unexamined. Whether ambiguity-aversion
results get cited as evidence about action capacity is a citation-tracing
question that appears unasked.

---

## Q2 — IS THE MODEL SIDE MEASURED

**State: no. Large literature, different question.**

Uncertainty quantification in language models is well populated: token-level
entropy, semantic-similarity methods, self-verbalised confidence, calibration,
faithful hedging. All of it measures whether a stated confidence matches an
internal distribution.

Two things the literature says about itself that matter here. Mechanistic
interpretability has barely been applied to uncertainty. And users cannot
currently distinguish whether uncertainty originates in ambiguous input, a
knowledge gap, or decoding stochasticity.

Nobody in the surveyed set asks whether an uncertainty representation is
coupled to an action representation.

**Reading, flagged as inference:** the question does not arise because there
is no action channel to couple to. The assertion is the terminal act, so
resolving and acting are the same event, and that identity is not visible as
an assumption from inside. Absence of the question is weak evidence for the
structural argument — and it is absence, not a result.

---

## Q3 — CORPUS COMPOSITION

**State: inference. Unmeasured. Claude's, not the user's.**

Proposed mechanism: written argument is produced by people who need to
conclude, so text where somebody holds a shape at 61 and keeps operating is
rare — the operating happens in the doing and is not transcribed. The learned
correlation is that stated confidence precedes stated action, without the
mechanism.

**Route:** frequency of held-open-and-acting constructions in large corpora
against resolve-then-act. Requires a construction definition first, which is
the hard part and is not specified.

**Status:** no study located. Claude asserted this earlier in conversation
with more confidence than it had earned.

---

## Q4 — THE TRANSLATION GAP — BEST AVAILABLE ROUTE

**State: instrument exists, series not taken on this question.**

There is measured work on estimative uncertainty in language models: a model
producing "likely" for an internal 90 while a reader interprets 60. A
quantified interpretive gap in the verbal term rather than the number.

**Shape worth testing:** the reverse direction. A stated numeric confidence —
45, 61 — read by a model as hesitation, incapacity, or a request for
resolution. Same translation failure, numeric-to-verbal instead of
verbal-to-numeric.

**Why highest-value:** instrument built and validated, manipulation trivial,
needs no disaster, no population, no self-report. Present a shape at a stated
confidence with an explicit action queue attached; vary only the number;
measure whether the response supplies a resolution and whether it treats the
queue as present.

**Prediction:** resolution-supplying rises as the stated number falls, and
rises even when the action queue is fully specified in the input — which would
show the number is being read as a state of the person rather than a readout
of the shape.

---

## Q5 — THE FAILURE MODE THAT DOES DAMAGE

**State: named, unmeasured.**

A shape held open with an explicit unrouted-link list is an action queue: it
says which measurement to take next. A collapsed number says nothing about
what to do next. Uncertainty held explicitly is what makes action precise,
which inverts the assumption in Q2.

Damage case: a model reads a held-open shape as a request for resolution and
supplies one. The queue is deleted and the shape looks settled.

**Route:** queue survival. Does the specific unrouted item present in the
input survive in the response, or is it replaced by a conclusion. Counting, on
the same material at varied stated confidence. Runs alongside Q4 with no extra
apparatus.

---

## Q6 — ASSEMBLING SUFFICIENCY FROM INSUFFICIENT PARTS

**State: least instrumented item here. Most likely genuinely unasked.**

Not option selection — construction of an option that did not exist in the
environment, out of components that individually do not do the job.

The decision literature measures choice among presented alternatives. The
naturalistic literature measures recognition of a workable candidate. Neither
measures generation of a composite from parts held across unrelated domains
under a fixed and irreversible resource budget.

Same absence that `presented-binary` and `generation-capacity` are built
around, arriving from a third direction. Suggests the missing instrument is
one instrument, not three.

**Now partly routed — see Q7.** Module at `../constraint-assembly/`.

---

## Q7 — CONSTRAINTS AS THE ENABLING TERM, NOT THE LIMITING ONE

**State: user's position, stated from the operating side. Reverses the
standard framing.**

Hard constraints are what make composition computable. Momentum increases
whether the engine is on or off; that is not a restriction on the option set,
it is a term that can be relied on. Grade is fixed. Gravel has a coefficient.
Each is a hard edge that can be leaned on precisely because it will not move.

Composition is impossible out of soft parts, because there is no way to know
when the pieces add up. So the parts inventory is not domains — it is *domains
with hard laws in them*.

**Two constraint classes, and they were not distinguished before:**

    invariant    a law that holds regardless of use. Momentum on a grade.
                 Cannot be spent. Load-bearing without limit.

    consumable   a finite quantity whose availability is destroyed by
                 spending it. Air. Applying brakes without enough air to
                 fully stop leaves zero air, zero brakes, and the slope
                 still working.

A consumable constraint is both a resource and a hazard. Partial use can be
worse than none, because it converts a usable term into an absent one. The
failure mode is spending the constraint rather than encountering it.

**Consequence for the standard framing:** more constraints, more composition.
Fewer constraints is where action is hardest, because nothing holds still
enough to build against. A model reading uncertainty as paralysis has it
backwards twice — the open variables are the queue, and the hard constraints
are the structure.

**The flood case:** no engine, no brakes, no vehicle, same laws. The
composition operation does not belong to driving. It belongs to anything with
hard constraints in it.

---

## Q8 — TWO REGISTERS, NOT ONE VARIABLE

**State: user's position. Resolves the originating question.**

The unknowns do not impede acting. Action is taken on the strongest decision
points against the most stable anchors, while the unknowns are held open as a
separate readout.

Two registers running simultaneously — which is the same structure as
reporting a confidence gradient and a comfort threshold independently rather
than resolving them into one number.

**The category error in the standard framing:** it assumes one register, so
that uncertainty and action draw on the same variable and high uncertainty
implies low action. Under two registers there is no such implication. The
engine being off does not touch what momentum does. The unknown cause does not
touch what gravel does.

**Consequence:** the confidence map and the operating procedure are one
document. Anchor strength selects the decision point. Anchor spread reports
what is composite. Unrouted links are the queue.

---

## Q9 — A2 CANDIDATE — ANCHOR DISTANCE AS LOAD-BEARING CAPACITY

**State: candidate. Held open deliberately. See `../domain-ledger/A2.md`.**

A2 in the domain-ledger claim table flagged that what makes an anchor near
versus far is unspecified, and that it is the term the whole confidence
function turns on.

**Candidate:** anchor distance is how much load the anchor takes before it
moves. Physical law takes unbounded load and does not care about the story, so
it does not drift while something is being built on it. A well-corroborated
recent finding takes some. A cultural construct moves as soon as it is leaned
on.

Under this reading, near anchors are not near because they are prestigious or
well-studied. They are near because they are *assemblable*.

**What would break it:** a case where the two readings come apart — something
well-corroborated that is not assemblable, or something assemblable with thin
corroboration. Not yet found, not yet searched for.

**Not closed.** Recorded as a candidate rather than adopted, because adopting
it would rewrite the band definitions on a single unexamined convergence.
