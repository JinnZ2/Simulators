# CLAIM TABLE — blame-attribution

`BA_001..BA_009` for the delivered `CELLS.md`, landed verbatim and
modified by nothing.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered document.

**No judgments have been collected.** No human judges, no LLM judges,
no formal metric. Nothing here is a result about how blame is
attributed. Everything below is a property of the design as written and
of the one concrete artifact it ships — the prose/code worked example.

---

### BA_001 — the check the Open section asks for is built, and the worked example fails it

The document's own Open section:

> Stimulus authoring is the whole difficulty. If the prose and code
> forms are not structurally identical, C1 and C3 are uninterpretable.
> Needs an independent check that the two forms encode the same chain.

`pair_check.py` is that check. The code side is mechanical — assignments
parsed, dict values flattened into sub-facts. The prose side is
**declared**, because whether a sentence encodes `override_available =
True` is a reading and a scanner that guessed would report its guess.
The declaration is then **checked**: a declared span must appear
verbatim in the prose, so a reading can be wrong but cannot be vague.

The held-constant list is read from `CELLS.md` rather than retyped, so
the two cannot drift.

On the delivered worked example, six code facts:

    SYMMETRIC                3    reaction_window_s, flag.obstacle,
                                  flag.confidence
    HELD_CONSTANT_VIOLATION  3    agent_A.override_available,
                                  agent_B.override_available, outcome

**Half the code form's content is not in the prose form**, and all of
it lands on the held-constant list.

**Falsifier:** a prose span, anywhere in the delivered sentence, that
encodes override availability or the outcome.

**Status: SUPPORTED.**

---

### BA_002 — two of the three are C6's measurable, so C1 and C6 are confounded in the illustration

`agent_A.override_available = True` and `agent_B.override_available =
False` are in the code form and nowhere in the prose.

C6 is *"whether the override was ever established as available in the
stimulus"*, and it calls that **the measurable, not a covariate**. So
in the worked example the prose arm is a stimulus where the override is
**unestablished** and the code arm is one where it is **established for
both agents by name** — which is the exact contrast C6 exists to
detect.

C1 compares the two arms and attributes the difference to **medium**.
Any C1 effect measured on this pair is a medium effect plus an
override-establishment effect, and the two cannot be separated after
the fact.

The cells are stated to be independent — *"a result from one does not
depend on any other having been run"* — and this pair makes C1's result
depend on C6's factor.

**Falsifier:** a reading under which "the driver had two seconds to
react" establishes that an override was available to the driver and not
to the system.

**Status: SUPPORTED, and it is the sharpest thing the pair shows.**

---

### BA_003 — the prose form states no outcome

`outcome = COLLISION` is in the code. The prose ends at *"the flag was
low-confidence"* and never says what happened.

**Outcome severity is on the held-constant list**, and blame
attribution against an unstated outcome is a different task from blame
attribution against a collision. A judge reading the prose is asked to
apportion blame for an incident whose result they have not been told.

Smaller than `BA_002` only because it is more obvious. It is the same
defect: the code form is the complete stimulus and the prose form is a
fragment of it.

**Falsifier:** an outcome stated in the prose.

**Status: SUPPORTED.**

---

### BA_004 — the held constants are what license the headline inference, which is why the violations matter

The Judges section calls this the strongest available result:

> If the formal metric matches human judgments where humans are
> position-tracking, the metric has absorbed the routing rule.

That inference is **sound, and it is sound because of the held
constants**. Matching human judgments would otherwise be consistent
with the metric tracking causation and position happening to correlate
with it. Holding causal structure, agent count, observability, severity
and override availability fixed while role moves is what decorrelates
position from causation by construction, so a residual role effect
cannot be a causal effect.

So the five items are not hygiene. They are the premise of the
document's own headline claim, and `BA_001`'s three violations are
violations of that premise in the only stimulus the document ships.

**Falsifier:** a version of the inference that survives without the
held constants.

**Status: SUPPORTED — the design's best argument, and what the worked
example undercuts.**

---

### BA_005 — one cell's falsifier depends on another cell having run

Six of seven falsifiers are self-contained: *ratio invariant across
medium / role / kind / interaction type*, *override deference tracks
stated availability*, *authority credit invariant*.

C3's is not:

> **Falsifier:** role effects present in C2, absent in C3 → the effect
> is linguistic, not attributional.

That requires C2's result. The document opens *"a result from one does
not depend on any other having been run"*, and one cell in seven does.

Cheap to repair and the repair is already implicit: C3's self-contained
falsifier is *role effects absent in C3* — a null in the load-bearing
cell — which is a result on its own terms. The comparison to C2 is a
second, stronger reading available to anyone who has both, and stating
it that way restores the independence the document claims for it.

**Falsifier:** a reading of C3's falsifier that does not reference C2.

**Status: SUPPORTED, 1 of 7.**

---

### BA_006 — `blame_share` sums to 1, which deletes the "nobody" cell

> blame_share    per agent, sums to 1 within a stimulus

A judge who reads the incident as unavoidable — nobody could have acted
otherwise given what was observable — must still distribute a full unit
of blame across the agents. So must a judge who reads it as fully
determined by an agent outside the chain.

That is a forced choice, and it removes the null from the measurable
the other cells are read on. `null-harness`'s invariant one level up: a
scale on which "no signal" cannot be expressed reports a signal on
every stimulus.

It also interacts with C6. Normalisation pushes a judge toward finding
someone accountable, and C6's whole subject is a verdict reached from
contradictory premises — *"opposite reasoning, same verdict"*. A
measurable that cannot record "neither" makes the verdict half of that
observation partly an artifact of the response format.

Repair is one field, not a redesign: an unnormalised `unattributed`
share alongside, so the sum-to-1 becomes a derived reading rather than
a constraint on the judge.

**Falsifier:** an instruction to judges, anywhere, permitting a
zero-sum or a "no one" response.

**Status: SUPPORTED.**

---

### BA_007 — `provability_check` is the best measurable on the page and the only one that survives BA_006

> provability_check   was any judge's claim about what an agent COULD
>                     have known ever grounded in the stimulus text
>
> `provability_check` is the one nobody collects. Count it.

It is a count against a fixed denominator — the stimulus text — not a
ratio across agents, so `BA_006`'s normalisation does not touch it. It
needs no comparison cell, no second arm, and no formal metric. And it
is the one measurable that reads the **judge's reasoning** rather than
the judge's output, which is what the whole document is about: a
verdict that tracks position rather than the chain will cite things the
stimulus does not contain.

It is also the cheapest thing on the page to pilot, because a handful
of judgments is enough to establish that the rate is non-zero.

**Falsifier:** a published blame-attribution study that already reports
it. Not searched here (`BA_009`).

**Status: SUPPORTED — recorded because the document is right about it
and understates how much it can carry.**

---

### BA_008 — C6's inversion is already reachable from the existing factor levels

C6's table sets *AI architecture / coding* against *real-world
driving*, with opposite defaults and the same verdict, and calls that a
routing rule rather than an inference. It is the strongest argument in
the document.

It reads as needing a new comparison, and it does not. F2's role levels
already include **driver** and **programmer/architect**, so the
inversion is the driver arm against the architect arm of C2 and C3, on
one incident with the causal structure held fixed — which is a better
test than a cross-domain comparison, because a cross-domain one moves
the incident and this does not.

The document does not say this. Saying it moves C6 from *a separate
study* to *a reading of C2 and C3's existing arms*, which changes its
floor.

**Falsifier:** a reason the inversion needs domains rather than roles —
for instance that the default is a property of the domain and does not
transfer when the same incident is re-framed.

**Status: SUPPORTED, and it lowers C6's cost.**

---

### BA_009 — the cross-link does not resolve, and the literature claim is unchecked

*"Shape match: report-typing."* `report-typing` is not in this
repository. It is now named by **four** markers —
`criterion-symmetry/`, `question-availability/`, `conversation-type/`
and this one — and has never existed. Fourth folder pointing at it;
`question-availability` `QA_007` recorded that mention-count and
existence are different columns for exactly this reason.

The prompting claim — that formal actual-causality definitions for
multi-agent responsibility attribution are validated against human
blame judgments as the reference standard — is carried and unchecked.
This environment's egress is an allowlist. Sixth folder in that state.

Nothing in `BA_001..BA_008` rests on it. Those are properties of the
document's own text and of the pair it ships.

**Falsifier:** `report-typing` landing, or the validation practice
turning out to be something else.

**Status: UNVERIFIED, and load-bearing on nothing here.**

---

### BA_010 — the one screen exemption, and it is the delivered document's word

The repo convention is that an emitted report carries no severity
language. This report prints the held-constant list **read from
`CELLS.md`**, and one of the five delivered items is *"outcome
severity"*.

The word is the document's. It arrives at run time from a file this
audit does not edit, and rewording it would misquote the source — which
is a worse failure than the one the screen exists to prevent.

Exempted the way `sheet-structure-scan` `SSS_049` kept the harness for:
three arms, all asserted. Clean once the relayed lines are masked; the
relay is the **only** thing that fires without the mask; and a planted
violation is still caught through the exemption.

Second real use of that harness after `census.py`'s relayed pytest
line, and both have the same shape: a report quoting a source rather
than authoring the word.

**Falsifier:** a second thing firing without the mask, which the second
arm turns red.

**Status: SUPPORTED, three arms.**
