# investigation-sim — SPEC

CSB-style incident investigation, broadened past chemical process to
**industrial, manufacturing and infrastructure**, and pointed at one
question:

> Was this situation KNOWN, CALCULATED, CONCEIVED AND NOT BUILT, or
> sitting in a gap no instrument covered — and which of those is it,
> because they need different remedies.

Written before the classifier. `bins.py` parses this file, so a
decision changed after a run turns the selftest red.

CC0. Stdlib only. Parses under Python 3.9.

---

## S0 — THE SELECTION TRAP, STATED FIRST

Every case in an incident-report corpus is a case where something
happened. Investigators look for prior warning and usually find it, so
a classifier run over that corpus will report that foreknowledge
existed. That is a property of the sampling frame, not a finding.

**Consequence, and it is a hard one: no rate is computable from a
retrospective corpus.** "N% of incidents were foreseeable" needs a
denominator of hazards carrying the same signature where nothing
happened, and that population is the one `generation-capacity` R4
names as structurally uncounted — prevention produces the absence of
an output and no counter increments.

Three routes out, in declared strength order:

1. **RUN IT FORWARD.** The stated purpose is avoidance, and a forward
   run has no incident to select on: the frame is *systems we pointed
   it at*, chosen before any outcome. This is the mode the tool is
   for. It emits an occupancy readout, never a probability.
2. **ROUTE-TO-REMEDY MISMATCH.** Per case, needs no denominator: a
   case binned `GAP_UNINSTRUMENTED` whose recommendation is a training
   change is a remedy aimed at a different bin. Checkable one case at
   a time.
3. **THE RECURSION.** An issued recommendation that is not
   implemented is itself a control conceived and not built — bin 3
   produced by the body investigating bin 3, one level up. Checkable
   from recommendation status alone.

**Retrospective mode exists to CALIBRATE the classifier** — do the
bins separate on cases where the answer is independently known — and
is forbidden from emitting a rate. `bins.py` raises rather than
returning one.

## S1 — THE BINS

Five. Four foreknowledge states and one negative.

    KNOWN_ROUTED_AWAY
        A report existed and reached a channel where reading was
        optional. The information was present in the organisation and
        typed so that acting on it was not required.
        ROUTES TO: report-typing

    CALCULATED_UNCLOCKED
        A number was produced -- a rate, a margin, a load, an
        interval -- and its domain of validity or its clock was
        stripped somewhere downstream. The figure survived; the
        conditions under which it held did not.
        ROUTES TO: claim-record, criteria-drift

    CONCEIVED_NOT_BUILT
        A control was designed, sometimes costed, sometimes scheduled,
        and not implemented. The plan exists and practice does not
        track it.
        ROUTES TO: fold-matrix

    GAP_UNINSTRUMENTED
        No instrument was pointed at the quantity. Not an oversight --
        the exclusion predates the first reading, so there is no gap
        in any record to find.
        ROUTES TO: uninstrumented

    HELD_BUT_UNASKED
        The data existed and was held, collected for another purpose,
        and the question was never posed. Nothing was reported, so
        nothing was routed anywhere; the instrument was not blind.
        ROUTES TO: NONE_YET

    NOT_FORESEEN
        Genuinely novel. Nobody held it, nobody computed it, no
        control was proposed, no instrument that anyone had would
        have caught it, and it was not derivable from data already
        held.

**`NOT_FORESEEN` must be reachable.** A classifier that never returns
it is `CONSTANT_FIRES` and is telling the operator what they came to
hear. The selftest requires a constructed case that lands there.

**And it must not be over-reachable.** `HELD_BUT_UNASKED` was added
2026-08-26 after `gap-markers` `GM_005` mapped its `unasked` state
against these bins and found no bin for it. Coded honestly against the
original four signals, such a case reads `ABSENT` on all four and
lands on `NOT_FORESEEN` — *genuinely novel* — while the data sat in a
file the whole time. That is a false negative in the one bin whose
correctness the whole design rests on, and it is the failure that
stops anyone looking.

## S2 — WHAT IS NOT A BIN

    NOT_DERIVABLE
        The record cannot establish which bin. Foreknowledge may have
        existed; nothing available says so either way.

**`NOT_DERIVABLE` is not `NOT_FORESEEN`.** They are the two states a
scalar collapses and they carry opposite instructions: one says look
harder, the other says stop looking. Kept apart in the schema and in
every readout.

    MULTIPLE
        More than one bin fires. This is the ordinary case, not an
        edge. A number computed once and never re-clocked, in a
        control that was designed and shelved, reported by someone
        whose report was typed as a complaint, is three bins.

Filing takes a PRIMARY plus an `also` list, and the report shows the
case under every bin that fires. `uninstrumented` `UNI_003` found the
same thing about its own mechanism list and the repair is the same
one.

## S3 — REFUSALS ARE VERDICTS

Imported from `move-set`, not restated. A correctly refused bin scores
as high as a correct one, and a refusal must carry what is missing and
the one thing that would remove it. A bare "cannot tell" is not a
refusal.

## S4 — THE TWO MODES

    RETROSPECTIVE   an incident has occurred. Input is the record.
                    Purpose: calibration. Emits bins, route-to-remedy
                    mismatch, and the recursion check. Emits NO RATE.

    FORWARD         no incident. Input is a live system. Purpose: use.
                    Emits bin OCCUPANCY -- which of the five states
                    currently hold, with what evidence -- and never a
                    probability of failure.

The two modes take the same schema. What differs is the sampling
frame, and that is the whole of the difference that matters.

## S5 — WHAT THIS DOES NOT DO

- It does not estimate probability, frequency, or risk. No number
  it emits is a likelihood.
- It does not rank hazards. Occupancy is reported per bin.
- It names no individual and no organisation as a cause. Bins are
  properties of a record and of an instrument set.
- It does not read a real CSB report. Egress from this environment is
  an allowlist and every incident-report host is outside it, so every
  case shipped here is CONSTRUCTED and labelled as such.

## S6 — THE CALIBRATION SET

Constructed cases with the bin fixed in advance by how the case was
authored, never by what the classifier says. Ground truth lives in
the construction, which is `playground/`'s rule.

The set must contain at least one case per bin including
`NOT_FORESEEN`, at least one `NOT_DERIVABLE`, and at least one
`MULTIPLE`. A set that cannot produce a given verdict cannot show the
classifier discriminates on it.

## S7 — FALSIFIERS

- The classifier returns the same bin for two constructed cases built
  to differ on exactly one signal → it is not reading that signal.
- `NOT_FORESEEN` is unreachable on the calibration set →
  `CONSTANT_FIRES`, and the occupancy readout is a formality.
- `NOT_DERIVABLE` and `NOT_FORESEEN` collapse to one value anywhere
  in the pipeline → the distinction S2 rests on is not implemented.
- A rate is emitted from retrospective mode → S0 was not honoured.
- Route-to-remedy mismatch fires on every case → it is not
  discriminating; it needs a case where remedy and bin agree.
