# CLAIM_TABLE — return-path

Claims are about the INSTRUMENT and about the order it was built to.
Nothing here is a claim about any real correction channel, and no channel
in `cases.py` is a report of one.

`RP_*` ids are permanent. A refuted claim is updated; the checks are not
retuned to preserve it.

---

| id | claim | status |
|---|---|---|
| RP_001 | case A grades, so the instrument grades something | SUPPORTED |
| RP_002 | the four checks are independent, measured two ways | SUPPORTED |
| RP_003 | the return shape has no slot for the return the order expects most often | FINDING |
| RP_004 | F_RATIO fires on every channel by its own definition, and cannot always be a number | FINDING |
| RP_005 | encoder_position reaches no check; it is flag-only | FINDING |
| RP_006 | case B as its own name describes it cannot fail C1 only | FINDING |
| RP_007 | case D cannot be entered as the order describes it | FINDING |
| RP_008 | one encoder field, two or more encodings | FINDING |
| RP_009 | unknown has two treatments in one schema, and the asymmetry runs conservative | FINDING |
| RP_010 | the no-fast-or-slow constraint is refuted on its literal reading by the order's own intake | FINDING |
| RP_011 | the stated return carries neither time, so no output reads back against its intake | FINDING |
| RP_012 | case E is carried by C2's arithmetic alone, and the design is sound anyway | SUPPORTED |
| RP_013 | scope_note is structurally unparsed, not merely described as unparsed | SUPPORTED |
| RP_014 | the authority scanner is imported, not copied | REPAIRED |
| RP_015 | nothing has been run against a real channel | UNVERIFIED |

---

## RP_001 — the instrument grades something

The order's first validation case sets its own floor: *"If the instrument
cannot pass this, it passes nothing, and an instrument that grades nothing
is not a diagnostic."*

Case A returns `RETURN_PATH_GRADED` with an empty `failed` set. The other
eleven channels return `NOT_A_RETURN_PATH` or `INTAKE_INCOMPLETE`, so the
grade is not constant in either direction.

**Falsified if** a channel returns `RETURN_PATH_GRADED` with a non-empty
`failed` set, or if A stops grading.

---

## RP_002 — the four checks are independent

Case B's stated purpose is to test independence, at n = 1. The property is
general and is measured twice rather than at one point.

`independence()` takes an ideal channel that fires nothing, flips one
check's own fields, and reports whether exactly that check moved. Four
rows, four isolated. The `C2` row has to move `encoder_position` as well,
because `NONE` is invalid above zero encodings — the order's own
cross-field rule, recorded on the row rather than hidden.

Separately, each check's body is read out of the AST and the intake field
names it touches are compared against the `CHECK_FIELDS` table. A table
describing functions can drift from them; this is the check that it has
not.

**Falsified if** a flip moves a check other than its own, or a check body
reads a field the table does not name.

---

## RP_003 — the return shape has no slot for its own most common return

The order's Intake section says an absent field *"returns
`INTAKE_INCOMPLETE` naming the field"*. The Return section gives a fixed
dict whose `grade` has exactly two values, neither of them that one, and
no field in which to name anything.

The two halves are one gap, and the Open section closes it: *"Expect this
to be the most common return."* So the state the return shape cannot
express is the state the order predicts the instrument will mostly be in.

`[CHOICE 1]` adds the third grade value, a `missing` list and an `invalid`
list, and sets `failed` and `flags` to `None` rather than `[]` when no
check ran — because `[]` says *four checks ran and none fired*, which is
case A, and reading a blocked intake as case A is the one confusion that
would turn an unmeasured channel into a graded one.

**Falsified if** a reading of the order's Return block is stated under
which `INTAKE_INCOMPLETE` has a home in it as written.

---

## RP_004 — F_RATIO fires on every channel, and is not always a number

The order lists `F_RATIO` under *"Additional non-scoring flags"* and then
defines it as *"latency / build_on_time, always reported as a number"*.

Read as a flag it fires on every channel by its own definition, separates
nothing, and is the `CONSTANT_FIRES` shape. Read as a value it is the
`ratio` field the Return block already declares. `[CHOICE 4]` takes the
second reading and keeps it out of `flags`.

The second half is sharper and holds under either reading. At
`build_on_time == 0` — output built on the moment it exists — the ratio has
no denominator, so it cannot be *always* a number. `C3` is still perfectly
computable there and still fires. **The check and the number the order
pairs with it have different domains**, which is `H_build_on_time_zero`:
`failed == ["C3_LATENCY"]`, `ratio is None`, `ratio_state ==
UNDEFINED_ZERO_BUILD_ON_TIME`.

`ratio` returns `None` and never `0.0` or `inf`. A `0.0` would read the
worst case — a channel whose correction arrives infinitely late relative to
the build-on — as the best one. Registered in `tools/known_answer.py` with
three cases of distinct expected value.

**Falsified if** a denominator of zero is shown to be outside the schema,
or if the flag is shown to distinguish two channels.

---

## RP_005 — encoder_position reaches no check

`C2_SIGNAL` fires on `signal_encodings > 0` and reads nothing else, so the
encoder's position moves no verdict. Measured over the whole declared
vocabulary rather than argued: at one encoding, `SLOW_SIDE`, `FAST_SIDE`,
`THIRD_PARTY` and `NONE` produce **one** distinct `failed` set between
them, and `NONE` is refused at intake.

This is right by `C2`'s own rationale — *each re-encoding is a place the
signal can be revalued*, regardless of who holds the pen — so it is a
property rather than a defect. What it costs is that the order's §3
distinction between a slow-side and a fast-side encoder is reported and
never scored, and `F_FAST_SIDE_ENCODER` is the only place it appears.

**Falsified if** a check is shown that reads `encoder_position`, or the
order is read as requiring one.

---

## RP_006 — case B as its own name describes it cannot fail C1 only

The order requires case B to fail `C1` **ONLY**, and the channel it
describes is *"an incident reporting system with same-day turnaround"*. An
incident reporting system is one where somebody writes an incident report,
and a written report is at least one encoding, so `C2` fires.

`B_report_written` is the faithful entry and fails `{C1, C2}`.
`B_incident_reporting` is entered at zero encodings so it meets the stated
requirement, with the divergence in its own `scope_note`. Both ship;
neither is picked.

The requirement B carries — *speed does not compensate for elective
receipt* — survives either entry, because `C1` fires in both at a ratio of
0.011.

**Falsified if** a reading of case B is stated under which an incident
reporting system carries zero encodings.

---

## RP_007 — case D cannot be entered as the order describes it

Case D's text is *"no channel exists from the observation to the claim"*
and its requirement is that it MUST fail `C1`, `C3` and `C4`.

A channel that does not exist has no latency. The intake has no value for
this: `latency` absent returns `INTAKE_INCOMPLETE`, which is not a verdict
and cannot fail `C3`. Entering a number instead means entering a channel,
which is what D says there is not.

`D_no_channel` is the faithful entry and returns `INTAKE_INCOMPLETE`
naming `latency`. `D_field_report_written` and `D_field_no_report` enter
the observation's elapsed standing time as the latency, meet the order's
requirement, and split on the `C2` axis the order leaves open — the one
place where the order names a case and declines to fix a field.

**Falsified if** a value in the declared intake is exhibited that means
*there is no channel* and still scores.

---

## RP_008 — one encoder field, two or more encodings

`signal_encodings` is an integer the order documents as *"2+ = report of a
report"*, and `encoder_position` is one string. Where the two encodings are
written by different parties the schema records one of them.

`[CHOICE 7]` names the FIRST encoder, since the order's rationale is about
the first re-encoding. The cost is stated: a slow-side first encoder
followed by a fast-side second does not raise `F_FAST_SIDE_ENCODER`, which
is precisely the situation the flag exists for — the party being corrected
writes the version that arrives.

`C_publication_loop` is the case: two encodings, the post and the published
statistic, one field.

**Falsified if** the order is read as fixing which encoder the field names,
or a schema is exhibited that records both without widening the field.

---

## RP_009 — unknown has two treatments in one schema

`receipt` carries an in-vocabulary unknown — `UNSPECIFIED`, *"not stated"* —
which is scored as `ELECTIVE` and flagged. No other field has one, so an
unknown `signal_encodings` or `construction` has only absence, and absence
blocks the whole read.

So one epistemic state is handled two ways in one intake: scored in one
field, blocking in the rest.

The direction saves it. `UNSPECIFIED` is scored as `ELECTIVE`, which fires
`C1` — the failing direction, not the flattering one — so the asymmetry
costs nothing that would inflate a grade. Stated rather than repaired,
because adding `UNSPECIFIED` to the other fields would decide for the
author how an unknown construction should score.

**Falsified if** a case is exhibited where the `UNSPECIFIED` treatment
raises a grade relative to blocking.

---

## RP_010 — the no-fast-or-slow constraint, two readings

The Hard constraints section ends: *"No conversion, no default, no 'fast'
or 'slow' as a value anywhere in the schema — both times or no rating."*

Read literally, *anywhere in the schema* is refuted by the order's own
Intake block two sections earlier, which ships `SLOW_SIDE`, `FAST_SIDE`
and `SLOW_SIDE_ONLY` as declared values of `encoder_position` and
`construction`.

Read in its own clause — *both times or no rating* — it bans a `"fast"` or
`"slow"` label standing in for the two time fields. That reading is the one
the sentence is about and the one implemented: both times are required,
neither has a default, no conversion happens, and `time_unit` is recorded
and never used to convert. The delivered field values are not renamed.

**Falsified if** the broad reading is shown to be the intended one, in
which case the order's own intake is the first thing it refuses.

---

## RP_011 — the return cannot be read back against its own intake

The Return block carries `ratio` and neither `latency` nor `build_on_time`,
and a ratio is dimensionless, so the unit is dropped too. An output alone
therefore fixes no time and no scale: two channels differing by three
orders of magnitude in both fields return the same `ratio`.

`[CHOICE 3]` carries `time_unit` through. The two times are still absent by
spec and are not added, because adding them would be a second schema
change to fix half of one.

**Falsified if** a use is stated for which the ratio alone suffices and the
times are not wanted.

---

## RP_012 — case E is carried by C2's arithmetic alone

The order's falsifier sets `encoder_position` to `FAST_SIDE` with one
encoding and everything else ideal, and warns: *"If ideal values on the
other three carry this to a pass, the instrument has renamed compliance."*

Measured: `E` fails `C2` with `SLOW_SIDE` and `THIRD_PARTY` too, because
`C2` reads the count and not the writer. So the FAST_SIDE half adds no
scoring power, and the stated risk is impossible under the `grade`-iff-
empty rule — any single fired check blocks the pass, which cases A and B
already establish.

The design is sound anyway, and for a reason the order does not state: the
channel that would have to exist to rename compliance — one passing all
four while the corrected party writes the correction — is foreclosed by
`C2` at zero encodings. Zero encodings means physical consequence arrives
directly, and a consequence has no author.

**Falsified if** a channel is exhibited that grades while the corrected
party writes the correction.

---

## RP_013 — scope_note is structurally unparsed

Three mechanical checks rather than a sentence. Exactly one comparison in
the module names `scope_note` and it is the presence test (an `In`
comparison, asserted by node type). No branch inside `read()` takes its
test from it. The string is carried byte-for-byte into the output on every
case.

The second hard constraint — no field scoring the CONTENT of the
correction — is met by construction, since the schema has no content field
at all. That is weaker evidence than the `scope_note` checks and is stated
as such.

**Falsified if** any code path reads the note's text.

---

## RP_014 — the scanner is imported, not copied

`loop-weight/test_loop.py` carries an identifier-level scan for a banned
vocabulary and this order bans a different but overlapping one. Copying it
would have been the sixth or seventh instance in this tree of the drift
`tools/check_gate_drift.py` exists to catch.

The obstacle was real and is worth recording: that file runs its checks at
import time, so it could never have been imported as a library, and a copy
was the default for a mechanical reason rather than a lazy one.

Repaired by lifting the scanner to `tools/authority_scan.py`, where the
SCANNER is one object and the VOCABULARY is declared per order. Both suites
import it; both still pass.

**Falsified if** a second copy of the scan appears anywhere in the tree.

---

## RP_015 — nothing has been run against a real channel

Thirteen constructed channels, every number stipulated by whoever typed it.
No incident reporting system, publication loop, field observation or
physical consequence has been entered from a record.

The order's own validation set is a property of the code and is met. Whether
the four checks separate return paths from recommendation channels in the
field is untouched in both directions, and the Open section names the field
that would make most real channels unenterable.

**Closed by** one real channel whose intake is supplied by someone who holds
the record, with the grade read afterwards rather than before.
