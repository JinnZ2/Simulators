# stop-authority

**Marker under exploration.** Delivered spec:
[`SPEC_STOP_AUTHORITY.md`](SPEC_STOP_AUTHORITY.md), landed verbatim.

> "Stop work authority exists" is currently evidenced by policy text and by
> stop COUNT. Both are unsigned. A count of zero is consistent with two
> opposite states:
>
> **A.** no condition warranted a stop
> **B.** the authority is not honored, so none were attempted
>
> Under B, non-use is produced **BY** the hollowness, and reads as safety.

```
python3 stop_authority.py    # the count, the three numbers, the suppression loop
python3 binding.py           # what it can bind; who holds it; what it cost
python3 relocation.py        # the measurement point moved, not the reading
python3 pressure_record.py   # why the crossing is the only period that shows it
```

All take `--selftest`. 26 / 23 / 21 / 26 checks, 96 in all, green. Samples
pinned in `samples/`, byte-reproducible.

The last two come from [`SPEC_ADDENDUM.md`](SPEC_ADDENDUM.md) — a witnessed
transition-period case, and the open work it leaves.

**This module does not flip the error.** Treating zero as evidence of B would
be the published mistake pointing the other way. Every readout returns
`INDISTINGUISHABLE` where the record cannot separate the two, and the work is
identifying which extra number would.

## The count is not weak evidence — it is ordered against the thing it measures

| facility | stops published |
| --- | --- |
| A: genuinely low hazard | 0 |
| B: hollow, fully suppressed | 0 |
| C: hollow, partly suppressed | **1** |

A and B publish an identical record. And C — where stops *are* attempted and
refused four times in five — publishes the **highest** count of the three. Read
as "the authority is being used," the facility demonstrably not binding looks
like the healthiest one.

## Which number is live at zero attempts

| | executed | attempted | warranted-in-review |
| --- | --- | --- | --- |
| A: genuinely low hazard | 0 | 0 | **0** |
| B: hollow, fully suppressed | 0 | 0 | **12** |

The honor ratio is `UNDEFINED_NO_ATTEMPTS` in **both** — 0/0 is not 1.0 and not
0.0 — and the attempt count is zero in both. Exactly **one** field separates
them: `warranted_in_review`.

That makes the spec's "denominator the other two are missing" exact. **The two
numbers that look like the authority measurement are the two that go blind
first, and they go blind precisely in the state that most needs measuring.**
The measurement that still works is the one determined outside the mechanism —
by post-incident review, not by anything the authority itself produces.

## The measurement eats its own denominator

Attempts respond to the honor rate workers have observed. Hazard held constant
at 3 warranted states per step, honor rate 0.15:

| t | warranted | attempts | honored | ratio |
| --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 0 | MEASURED |
| 3 | 3 | 1 | 0 | MEASURED |
| 5 | 3 | 1 | 0 | MEASURED |
| 6 | 3 | **0** | 0 | **UNDEFINED** |
| 10 | 3 | 0 | 0 | UNDEFINED |

**30 warranted-and-available prior states produced 0 published stops, with the
hazard rate never moving.** Attempts fall because the honor rate is low; at
zero attempts the ratio has no denominator; and the published stop count stops
rising — which under the count-alone reading is the record improving.

Stipulated model of a stated mechanism. The learning rule was chosen, not
measured, and 0.15 was picked to make the collapse legible in ten steps. It
shows the loop is arithmetically available, not that any facility behaved
this way.

## What it can bind

Authority is defined by what it can bind, not by who holds it.

| facility | binding | tested |
| --- | --- | --- |
| prior art: SWA as core program element | NO_STOPS_AT_ALL | False |
| named holder, stops only at peer level | UNTESTED_ABOVE | False |
| named holder, one stop bound at executive | BOUND_ABOVE_HOLDER | **True** |

**`FUNCTIONING` is not a value this module returns** — there is no such field
on the summary, by construction. An untested authority is untested; a tested
one has a binding record to read directly. Collapsing both into a single
functioning flag is the move the whole instrument exists to refuse.

**No reversal recorded is not no reversal.** With zero stops there is nothing
that could have been reversed, so the record reads `NOT_LOOKED`. An empty
reversal record beside real stops reads `NONE_FOUND` — a different fact,
distinguished by the stop count beside it and never by the emptiness of the
list.

**On distribution, the module records and does not grade.** Authority located
in everyone has no named position holding it and nobody to be reversed against
— both recorded. Whether that is expansion or contraction is not returned: the
spec says *may*, and which it is depends on a facility this module does not
measure. That refusal has a cost, and the cost is stated: a reader wanting a
verdict gets two structural facts and no number.

## The documented case

Ten years, no stop recalled, evidence offered of function being that workers
reported having **conversations** about safety.

| axis | reading |
| --- | --- |
| stops executed | 0 |
| honor ratio | NOT_COLLECTED |
| warranted-in-review | absent — no denominator |
| highest level bound | NO_STOPS_AT_ALL |
| reversal record | NOT_LOOKED |
| named holder | False — authority in everyone |
| someone to reverse against | False |
| conflict axis | UNASSESSED |
| **count diagnosis** | **INDISTINGUISHABLE** |

**Axes returning a measurement: 0.** Published as working, with every axis
empty.

A conversation is not a stop attempted, not a stop honored, and not a reviewed
warranted state. It is not one of the three numbers, and offering it as
evidence of function substitutes an activity for a measurement.

**The instrument does not say the authority was hollow.** It says the published
claim rested on nothing it could read. Recording that conversations fail to be
a measurement is also different from establishing that the conversations did
nothing, and nothing here does the second.

## The addendum: moving the measurement point instead of arguing with it

CEO pressure to run subpar material; QC read it out of spec; the stated
rationale was **ship it, and returns will identify the problems**. The floor
refused and the refusal held.

**Nobody argued the inspectors were wrong.** The measurement point was
relocated from pre-shipment inspection to post-shipment return, and the
upstream reading — still correct — was made non-binding. `upstream_status()`
returns `NOT_DISPROVEN_MADE_NONBINDING`, never `REFUTED` and never
`SUPERSEDED`. A reading that still holds and no longer binds is the whole
shape of the case.

Same material, same threshold:

| point | reads | decision |
| --- | --- | --- |
| pre-shipment | 0.072 | **REFUSE** |
| post-shipment return | 0.016 | **SHIP** |

The proxy understates by **4.55×** — a product of three unobserved terms
(defect manifests × customer notices × customer returns = 0.198). Not noisier
than the inspection: biased low by a factor nobody reading it can measure.

**The missing denominator is not an error bar.** Over six periods, 480
defective units, 48 returned, **385 silent** — 80% producing no record
anywhere. Not a noisy record; no record. And 240 defective units ship before
the lag elapses and any signal exists at all.

What the module does *not* claim: that returns detect nothing. They do — some
problems, later, after harm, at an unknown fraction. The budget office's stated
rationale is not false. `can_the_proxy_carry_the_decision()` keeps "does it
detect anything" (yes) apart from "can it carry this decision" (no), and
answers only the second.

## Why the pressure event is the only observation available

| period | documented pressure | boundary |
| --- | --- | --- |
| BEFORE | 0 | INTACT_UNAPPROACHED |
| TRANSITION | **1** | CONTESTED |
| AFTER | 0 | UNKNOWN_POSSIBLY_GONE |

**Zero on both sides of the peak, meaning opposite things.** Before, the
decision sat with the function and nothing needed pressing. After, if refusal
no longer holds, nothing requires pressure — so the negotiation never happens
and is never recorded. Identical observable, opposite states, and the count
separates neither. A survey sampling later periods finds zero and reads it as
an improvement on the transition.

That is the same shape as the stop count, and it is **one finding, not two** —
the observable running non-monotonic in the thing it is read as measuring, in
one repo by one builder. Counting them as two independent results would be the
inherited-agreement error `operator-structure-echo/` exists to catch.

A documented pressure event establishes one thing cleanly: **a boundary existed
to press against.** Someone had to be pushed, so something was in the way. It
does not establish the boundary held afterwards — `held_afterwards` is `None`,
not `False`, because no later test is recorded and no later pressure is either.

## Open work, carried and not closed

| item | state |
| --- | --- |
| collect additional transition-period accounts | OPEN (n=1) |
| recover pressure events after the boundary is gone | NO_METHOD_PROPOSED |
| is hollowing the same move as scope contraction | CANNOT_DISCRIMINATE |
| collection mechanism for WARRANTED-IN-REVIEW | NO_METHOD_PROPOSED |
| do published SWA programs report attempts separately | **NOT_RUN** |

**Item 5 has a harness and no survey.** The spec says that if no published
program reports attempts separately from executions, *that absence is itself
the finding*. It would be. Establishing it requires reading published programs;
this side has no access to a corpus of them, and inventing rows would be worse
than an empty table. The harness ships with the one row available — the prior
art case, which reports executions and not attempts — and state `NOT_RUN`.
`ABSENT` is a different state and is not available. `ProgramRecord` refuses a
row where the reporting was never examined: `None` is not `False`.

**Item 3 cannot be discriminated.** The test is one facility with both axes
recorded. Three cases are available, from three facilities, with one axis each
— consistent with one move and with two. Cases cannot be pooled: the facility
is the unit.

**Item 4 may not be solvable in the form stated.** Every mechanism proposed for
collecting `warranted-in-review` requires the reviewing party to admit the count
matters — which is the same authority question one level up, since the party
who would collect the denominator is the party a stop binds against. Recording
that recursion is not progress on it.

## What is not established

- **Nothing here measures a facility.** Two of three binding rows are
  stipulated to make the axes move; the third is the operator's documented case
  carried without independent check. This is a set of refusals with a worked
  example, not a survey.
- **n=1, and three modules now rest on that one account.** `relocation.py`,
  `pressure_record.py` and the open-work register all take their structure from
  a single witnessed transition. Three readouts on one observation is not three
  observations, and the spec's own open work leads with collecting more.
- **The relocation numbers are invented.** The relocation is witnessed; the
  three-period return lag and the manifest/notice/return fractions are this
  module's construction, chosen to land the proxy under the line. They show the
  mechanism is arithmetically available and measure nothing that happened.
- **`warranted-in-review` is itself a judgement made after the fact**, possibly
  by the parties a stop would have cost. The spec places it outside the
  worker's suppressed judgement, which replaces it with a reviewer's. Nothing
  here checks who reviews — and a review conducted by the party a stop binds
  against is the same structure one level up.
- **`UNTESTED_ABOVE` compares two declared levels**, both supplied by whoever
  fills the record. The ordering is real; the placement in it is a declaration.
- **Related, and not independent of it.** `extraction-blindness-sim/` already
  builds "absence of an error signal read as confirmation of safety" on a
  physical substrate. This is the same reading error with an extra loop that
  case does not have — there the sensor fails to see the damage, here the
  hollowness *causes* the silence. Same builder, same repo: by
  `operator-structure-echo/corroboration.py` the agreement between these two
  folders is `INHERITED`, not found.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
