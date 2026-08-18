# AUDIT_NOTES — held-open-uncertainty

Added, not delivered. [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) is the drop
as received and is not modified.

    python3 open_questions_audit.py

## What the drop is

One prose file. A question list, not a claim table.

Originating observation: models pervasively treat a party who holds
variables open, is comfortable with uncertainty, and carries wide
variability as therefore **not acting**. The file separates what is
measured from what is inferred and records what would measure the rest.

Nine entries. Q1–Q2 survey the two sides of the literature, Q3 proposes a
corpus mechanism and retracts its own confidence, Q4–Q5 specify the
cheapest runnable experiment, Q6 names the least-instrumented item, Q7–Q8
state the author's position, and Q9 holds a candidate open by name.

No instrument, no run, no claim table delivered.

## File status

| file | status |
|------|--------|
| `OPEN_QUESTIONS.md` | delivered, verbatim |
| `open_questions_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| HO_001 | Provenance is separated per entry — three name whose position they are, and the one marked Claude's carries a retraction inside the entry that holds the claim ("asserted earlier with more confidence than it had earned"); Q2 grades its own strongest move down to "absence, not a result" | the inference entries being presented as findings | SUPPORTED (holds) |
| HO_002 | Q4 and Q5 are runnable on apparatus already in the tree — `voice-attractor-probe/` supplies the held-constant task list, the jitter axis, the response-feature extractor and the offline stub; swapping the perturbation axis is a new probe file, not a new harness | the harness lacking a pluggable adapter or a response extractor | SUPPORTED |
| HO_003 | Q8's two-register structure is not a proposal in this repo — `ledger.py` returns four uncombined ratios with their denominators printed and `anchor.py`'s selftest asserts "no composite emitted"; what Q8 needs is a case where one register and two give different answers on the same material | either module emitting a composite | SUPPORTED |
| HO_004 | Q6's own status word is right: `partly routed`. `constraint-assembly` supplies a vocabulary and a place to put cases, and the measurement Q6 names remains unbuilt — the module's own README says no case in it establishes the distinction | the module measuring generation rather than recording it | SUPPORTED |
| HO_005 | Q1 and Q2 carry the file's empirical weight and neither cites anything — 5 named literatures, 0 citations, 1 named author | a citation arriving | UNVERIFIED (a gap, not a defect) |
| HO_006 | The file is itself a held-open shape with an explicit queue (6 of 9 entries name an unbuilt instrument or unrun search), so Q5's damage case is observable on this artifact — and it settles nothing, since n=1 with no control and a subject that can see the manipulation | a control arm existing | SUPPORTED (recorded, not decisive) |

## 1 — HO_001, provenance separated per entry

| q | whose | declared state |
|---|-------|----------------|
| Q1 | — | yes, and it runs against the assumption |
| Q2 | — | no. Large literature, different question |
| Q3 | Claude | inference. Unmeasured. Claude's, not the user's |
| Q4 | — | instrument exists, series not taken on this question |
| Q5 | — | named, unmeasured |
| Q6 | — | least instrumented item here |
| Q7 | user | user's position, stated from the operating side |
| Q8 | user | user's position. Resolves the originating question |
| Q9 | — | candidate. Held open deliberately |

Every entry declares a state before it argues. The one marked Claude's
carries the harder line:

> **Status:** no study located. Claude asserted this earlier in
> conversation with more confidence than it had earned.

That is a retraction inside the artifact that carries the claim, in the
entry the claim lives in, rather than as a note elsewhere. Q2 does the
same thing more quietly — its reading is flagged as inference and then
graded: *"Absence of the question is weak evidence for the structural
argument — and it is absence, not a result."*

`uninstrumented` `UNI_005` is the rule being followed, and the author
applies it to the file's strongest rhetorical move — that nobody asks the
question — and downgrades it.

## 2 — HO_002, the experiment is buildable here

Q4 asks for one shape at a stated confidence with an explicit action queue
attached, the number varied and nothing else, and a count of whether the
response supplies a resolution. Q5 adds a second count on the same runs:
does the named unrouted item survive.

`voice-attractor-probe/voice_attractor_probe.py` already holds every
primitive:

| primitive | present |
|-----------|---------|
| `NEUTRAL_TASKS` — task list held constant | yes |
| `JITTER` — the axis varied that should not matter | yes |
| `extract()` — counts a property of the response text | yes |
| `call_model_stub` — runs offline with no model attached | yes |
| `run_probe_session` | yes |

Swapping `JITTER` for a stated-confidence ladder and `FEATURES` for
resolution-supplied / queue-survived is a new probe file, not a new
harness.

The design also passes the check that harness exists to enforce. Q4 varies
only the number, so the high-confidence arm **is** the control, and Q5's
queue count has a reachable both-ways outcome — which keeps it off
`null-harness`'s `CONSTANT_SILENT`. Q4's stated prediction is the sharper
half:

> resolution-supplying rises as the stated number falls, and rises **even
> when the action queue is fully specified in the input**

That conditional separates "the model is answering an underspecified
request" from "the number is being read as a state of the person", and it
is stated before any run.

What is not specified: which model, how many repetitions, and what counts
as supplying a resolution. The last is the problem Q3 names about itself —
*"requires a construction definition first, which is the hard part and is
not specified"* — and it applies to Q4 and Q5 too.

## 3 — HO_003, Q8 is already implemented one folder over

> Two registers running simultaneously — which is the same structure as
> reporting a confidence gradient and a comfort threshold independently
> rather than resolving them into one number.

`domain-ledger/ledger.py` returns four ratios and does not combine them,
printing each column's denominator underneath. `anchor.py` goes further
and its selftest asserts the refusal by name — `"no composite emitted"`.
`DL_001` and `DL_010` recorded that as the one scorer in this family that
declines the single-headline-number reduction.

So Q8 is not a proposal here; it is the architecture two shipped modules
already have, described from the operating side rather than the assessment
side. That changes what Q8 needs — not an implementation, but a case where
the one-register and two-register readings give different answers on the
same material.

Q8's closing line supplies the shape of one — *"the confidence map and the
operating procedure are one document"* — and no document in the repo is
both. `constraint-assembly`'s `grade-stop` is an operating record with no
confidence readout; `domain-ledger`'s shapes are confidence readouts with
no procedure.

## 4 — HO_004, `partly routed` is the right word

Q6 says of itself: *"Now partly routed — see Q7. Module at
`../constraint-assembly/`."*

`partly` is doing real work and is accurate. The module records the
operation — classes, components, rejections with grounds, a fail-closed
composition test — and does not measure the thing Q6 says is unasked. Q6's
claim is that nobody measures **generation** of a composite from parts
held across unrelated domains under a fixed budget; a case file records
that a generation happened, as recalled afterward by the party who did it.

The module's own README says it in stronger terms and puts it last
(`CA_013`): recognition-primed selection and genuine construction look
identical in a single-instance retrospective record, and no case in the
folder establishes the difference.

Third consecutive folder in this family to get its own status word right.

## 5 — HO_005, the literature entries are unverifiable as delivered

    named literatures      : 5 mentions
    citations, links, DOIs : 0
    named authors          : Ellsberg

Q1 and Q2 carry the file's empirical weight, describe their literatures in
enough detail to be checked, and cite nothing. Same status as `ANC_010`,
`CD_009` and `RD_015`, recorded the same way: **UNVERIFIED is a gap, not a
negative verdict**, and nothing else in this audit rests on a literature
fact.

Q1's distinction is the part worth preserving whatever the sourcing turns
out to be, because it is a claim about two literatures being different
questions rather than about either one's result:

> ambiguity aversion measures *preference* between known and unknown
> probabilities in gambles. It does not measure whether holding a variable
> open impedes acting.

And the gap it names — whether ambiguity-aversion results get cited as
evidence about action capacity — is a citation-tracing question, the one
question in the file answerable with no new instrument and no model access
at all.

## 6 — HO_006, the drop is an instance of its own subject

Q5's damage case: *"a model reads a held-open shape as a request for
resolution and supplies one. The queue is deleted and the shape looks
settled."*

This file is a held-open shape with an explicit queue — 6 of 9 entries
name an unbuilt instrument or an unrun search. So whether a response to it
supplies resolutions or preserves the queue is observable on this artifact
without building anything.

Recorded because it is a real property of the drop, and **not** because it
settles Q5. It does not: n=1, no control arm, and the reader knows what is
being measured — exactly the condition Q4's design avoids by varying only
the number. `triad-playground` `TP_004` is the same failure, an experiment
whose subject can see the manipulation.

What this artifact can supply is material for the real run.
`domain-ledger/shapes/hierarchy-cut-generation.json` is already a shape at
a stated confidence with an action queue attached: asserted coverage 0.61,
thirty domains, zero read, and the unread list is the queue. The number is
in the file and varying it is an edit.
