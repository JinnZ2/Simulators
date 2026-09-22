# CLAIM_TABLE — assessor-coupling

Ids are permanent and are never renumbered. `ASC_*` are claims about THIS
build and its reading of the delivered order; they are distinct from the
order's own numbered conditions and steps. Every claim below is checked by
`test_assessor.py` unless its status says otherwise.

No organization is scored, named or assessed anywhere in this folder.

---

**ASC_001 — SUPPORTED.** The eight conditions, the precedent record, the
four-item prior defense and the five-item non-financial coupling list are
all parsed out of the delivered order at call time and never retyped.
*Support:* `conditions()` returns eight numbered entries each contained in
`WORK_ORDER.md` whitespace-flattened, with condition 8 correctly the only
one carrying no gloss; `cases()` returns ten across three eras with the
prior-defense section excluded from the era walk; an AST walk over both
modules' string literals finds no condition title and no case lead retyped;
a document lacking either block raises rather than returning an empty set.
*Falsifier:* a condition or case present as a literal in a module, or a
parse returning an empty set on a document with no section.

**ASC_002 — SUPPORTED, and it is the build's one structural rule.** The
order's measurand separates two questions being treated as one: hop-1 (*does
the assessed pay the assessor*) is a ROUTING question, the pool test is the
INDEPENDENCE question. A hop-1 answer therefore never enters the
independence vector — it is carried on the report and read by nothing
(`[CHOICE 1]`). The computed consequence on the order's own current-position
reading: **hop-1 is the one property the sector is recorded as stating, and
it is not a member of the eight**, so stating it moves the vector by zero.
*Support:* an AST walk over `score()` finds no hop-1 name or attribute; two
arrangements differing only in `hop1_payment` produce identical vectors and
identical counts; `hop1_scored` is `False` on the report; no condition title
names payment.
*Falsifier:* a hop-1 value that changes any condition's state.

**ASC_003 — SUPPORTED.** `UNVERIFIABLE_AS_STATED` is a state of its own and
is kept apart from `FAILS` (`[CHOICE 2]`), and `UNDECLARED` is kept apart
from both (`[CHOICE 3]`). Condition 2 is in the first because the order
records that no standard defines what pool-level funding independence would
require: a condition with no standard saying what it asks has not been
failed, it has not been asked. Condition 1 is in the second because the
section does not mention it.
*Support:* the parsed current position is 0 passes, 6 fails (3,4,5,6,7,8),
1 unverifiable (2), 1 undeclared (1), of 8; an arrangement declaring nothing
scores eight `UNDECLARED` rather than eight fails; all four states are
reached by controls and an all-pass arrangement exists, so the scorer is not
`CONSTANT_FIRES`.
*Falsifier:* a silence scored as either a pass or a fail.

**ASC_004 — REFUTED (the record's summary sentence, as written).** The order
states *"hop-1 cleanliness has never once been sufficient, in any domain, at
any point in the record"* and, in its scope limits, that the table is
*"illustrative, selected for documentation quality. Not a systematic sample,
and no base rate is claimed."* Both lines are in the document and they point
different ways. The corpus carries ten cases, every one of which failed, and
**a negative arm of zero counted by parse** (`[CHOICE 7]`), so the four-item
prior defense cannot be scored for discriminating power: the return is
`NOT_EVALUABLE` with reason `selected_on_outcome` and discrimination `None`
rather than zero. The reading that survives is the narrow one — in the
selected cases hop-1 cleanliness was not sufficient — and how often it *is*
sufficient the corpus cannot bound in either direction. The order names the
repair itself: step 2, the systematic precedent survey. This is the
frame-selected-on-the-variable shape (`UNI_126`, `SHB_023`, `DD_003`)
arriving in a precedent table.
*Support:* both lines located verbatim; `defense_discrimination()` returns
`NOT_EVALUABLE` on the delivered record and `EVALUABLE` with a figure on a
constructed corpus carrying a negative arm, so the refusal is a property of
the corpus and not of the check.
*Falsifier:* a case in the record in which the prior defense held and the
structure did not fail — which is step 2's output, not an objection.

**ASC_005 — SUPPORTED.** Nothing in the folder is an index and nothing ranks
two arrangements (`[CHOICE 4]`). The report is eight per-condition states
and a count carrying its denominator. The order's *"the output is a
distribution, not an accusation"* is a refusal rather than a note:
`field_distribution` raises `SelectiveApplication` unless the caller
declares the set complete (`[CHOICE 5]`), because a selected subset with the
same arithmetic is a different object.
*Falsifier:* a single independence number emitted anywhere, or a
distribution returned over an undeclared subset.

**ASC_006 — SUPPORTED.** The earliest entry in the precedent record is a
personal-liability remedy, and the order records condition 6 as the one
least discussed in contemporary arrangements. The oldest remedy in the
record is the one it reports as least used now. Both readings are verbatim
containment, not a classification of any case.
*Falsifier:* either line absent from the document, or the earliest parsed
case not carrying the liability text.

**ASC_007 — SUPPORTED as a state, `NOT_RUN` as a measurement.** The order's
step 4 is built: `disclosure_coverage()` scores a declared instrument
against the eight and leaves any condition the instrument does not mention
`UNDECLARED` rather than absent — the audit must not commit the move the
order is about, where an absent field reads as ABSENT rather than
unmeasured. No instrument is scored: none is reachable from this environment
and none is composed from memory. The order's expected result is money only
and its own line is that a null result on the other seven is the finding.
*Falsifier:* an instrument scored here without a source.

**ASC_008 — SUPPORTED as a metric, `NOT_RUN` on any field.** `pool_fraction`
is the order's step 1 and keeps a measurement apart from a silence: every
source declared and none coupled is `0.0`, while an empty record, a record
carrying an `UNDECLARED` source and a record summing to zero are all `None`.
Reading an undeclared source as uncoupled would compute independence from a
silence, which is the condition the order says has no standard.
*Support:* registered in `tools/known_answer.py` with six cases; the `0.0`
against the three `None`s is the pin.
*Falsifier:* a share returned on a record carrying an undeclared source.

**ASC_009 — SUPPORTED.** The order's NOT ABOUT ANY NAMED ORGANIZATION
constraint is structural here rather than described: the arrangement schema
has no field for a party's name, no case lead or condition title is retyped
as a literal, and every named party in any render is parsed out of the
delivered document.
*Falsifier:* a party authored in a module, or a name field in the schema.

**ASC_010 — SUPPORTED, recorded rather than resolved.** A different WO-6 —
*THE FOURTH INDEPENDENCE AXIS: CRITERION EXTERNALITY* — landed earlier in
`criterion-externality/`. Two delivered documents share an ordinal and share
nothing else. Neither file is overwritten and both stay inspectable, which
is the repo's supersession convention applied to a collision rather than a
revision. The three companion orders this one names (WO-1, WO-4, WO-5)
resolve by folder path plus a content marker (`[CHOICE 8]`).
*Support:* the other file is asserted present, different, and still on its
own subject.
*Falsifier:* either file edited to remove the collision.

**ASC_011 — UNVERIFIED, and it covers the folder.** Every precedent case,
date, fatality figure and remedy in the record is carried from the order and
checked against nothing; the sources are not reachable from this
environment. The condition-by-condition current-position reading is the
order's own, from public statements, and the order says it should be
re-verified before publication — nothing here re-verifies it. Steps 2, 3, 4
and 5 are all unrun. Nothing in this folder establishes that any assessor,
in any field, is or is not independent.
