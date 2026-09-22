# assessor-coupling

WO-6, delivered verbatim in `WORK_ORDER.md` and built to. The measurand:
whether an assessor is structurally independent of the party it assesses,
**distinguished from** whether a direct payment runs between them.

**Ordinal collision, recorded rather than resolved.** A different WO-6 —
*THE FOURTH INDEPENDENCE AXIS: CRITERION EXTERNALITY* — landed earlier in
`criterion-externality/`. The two documents share a number and nothing
else. Both stay inspectable: neither file was overwritten, and the test
file asserts the other one is still present and still different.

**CONSTRUCTED.** Every arrangement scored in this folder is built here to
exercise a branch. **No organization is named anywhere**, and the schema has
no field for one — `Arrangement` carries an id, a declared condition vector,
a carried hop-1 value and a basis. Every named party appearing in a render
comes out of the delivered order and none is authored here. Nothing in the
folder is a claim that any specific assessor has been captured, has produced
a biased finding, or acts in bad faith.

## What is built

`conditions.py` parses the eight INDEPENDENCE CONDITIONS out of the order at
call time, scores a declared arrangement against them, and implements the
order's step 1 metric (`pool_fraction`).

`precedent.py` parses the precedent record, the four-item common prior
defense and the non-financial coupling list, and computes what that corpus
can and cannot bound.

## Results

**The hop-1 answer never enters the independence vector (`ASC_002`).** The
order's measurand separates a *routing* question — does the assessed pay the
assessor — from the *independence* question, and combining them is a ratio
across unlike objects. `score()` reads no hop-1 field, asserted from the
AST, and two arrangements differing only in hop-1 score identically. The
computed consequence on the order's own reading of the current position:
hop-1 independence is the one property the sector is recorded as stating,
and **it is not a member of the eight**, so stating it moves the vector by
zero.

**`UNVERIFIABLE_AS_STATED` is a state of its own (`ASC_003`).** Condition 2
sits in it because the order records that no standard defines what
pool-level funding independence would require. A condition with no standard
saying what it asks has not been failed; it has not been asked. Parsed from
the order's own bullets, the current position reads **0 passes, 6 fails, 1
unverifiable, 1 undeclared of 8** — condition 1 undeclared because the
section does not mention it, not because it passes.

**The record's summary sentence is not supported by the record (`ASC_004`).**
The order states *"hop-1 cleanliness has never once been sufficient, in any
domain, at any point in the record"* and, four sections on, that the table is
*"illustrative, selected for documentation quality. Not a systematic sample,
and no base rate is claimed."* Both are in the document. The corpus has ten
cases, every one of which failed, and **a negative arm of zero counted by
parse** — so the four-item prior defense cannot be scored for discriminating
power at all: `NOT_EVALUABLE`, reason `selected_on_outcome`, discrimination
`None` rather than zero. What survives is the narrow reading — in the
selected cases hop-1 cleanliness was not sufficient — and the rate at which
it *is* sufficient is unbounded in either direction. A constructed corpus
carrying a negative arm returns a figure, so the refusal is a property of the
delivered corpus and not of the check. The order names the repair itself:
step 2, the systematic precedent survey.

**Condition 6 is the oldest remedy and the least used one (`ASC_006`).** The
earliest entry in the record is a personal-liability clause, and the order
records condition 6 as the one least discussed in contemporary arrangements.
Both readings are verbatim containment, not a classification.

## What is not run

- **Step 1**, the pool metric, is **built and run on nothing**. No funding
  record is held here and none is composed from memory.
  `field_distribution` refuses a set the caller has not declared complete
  (`[CHOICE 5]`) — the order's *"apply to ALL assessors in a field, not
  selectively"* as a refusal rather than a note.
- **Step 2**, the systematic precedent survey, is the largest and is not
  attempted.
- **Step 3**, the remedy decay study, is archival.
- **Step 4**, the disclosure-field audit, is built (`disclosure_coverage`)
  and scored on no instrument: none is reachable from this environment and
  none is composed from memory. The order's expected result is money only,
  and its own line is that *a null result on the other seven is the
  finding*.
- **Step 5**, scoring a field other than AI blind, takes an arrangement this
  session does not hold; one composed here would be scored by the hand that
  composed it.

Every precedent fact, every date and the whole current-position reading are
**carried from the order and checked against nothing** — the sources are not
reachable from this environment. The order says its own condition-by-
condition scoring should be re-verified before publication, and nothing here
re-verifies it.

## Running

    python3 assessor-coupling/conditions.py     # the eight, four controls
    python3 assessor-coupling/precedent.py      # the record, what it bounds
    python3 assessor-coupling/conditions.py --choices
    python3 assessor-coupling/test_assessor.py  # the checks; prints the count

Both modules refuse `--selftest`. `pool_fraction` is registered in
`tools/known_answer.py`. Stdlib only, parses under 3.9, phone-buildable,
CC0.
