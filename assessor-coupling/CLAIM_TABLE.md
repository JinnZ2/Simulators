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
Ids are `ASC_`, permanent, never renumbered. Every number is printed by
`run_all.py` or `selftest.py` and pinned by `selftest.py`; the renders are
in `samples/`. Nothing here is a statement about any assessor, any
organization, any public record or any historical case: the instruments
were built to WO-6 and run on the order's own text and on constructed
inputs.

| id | claim | status | evidence | falsifier |
|---|---|---|---|---|
| ASC_001 | The folder constraints hold, read from the files: every import is stdlib or this folder, every file parses under 3.9, every library module is under 300 lines and refuses `--selftest` with exit 2, no file names a network module, nothing imports across the folder boundary, `run_all.py` prints the contamination declaration before the first part, and no authored file carries an entry name from the order's table. | SUPPORTED | `selftest.py` folder section | a non-stdlib import, a 3.9 parse failure, a `--selftest` exiting 0, a cross-folder import, a render with a number above the declaration, an organization named in an authored file |
| ASC_002 | The eight INDEPENDENCE CONDITIONS are parsed out of `WORK_ORDER.md` at call time and never retyped; a copy holding seven raises. | SUPPORTED | `selftest.py` "eight conditions parsed", "retyped copy holding seven raises" | a condition literal in any module |
| ASC_003 | The order's current-position section scores seven of eight: it names conditions 3 through 8 as failing and 2 as unverifiable, and says nothing about condition 1 (authority not revocable by the assessed), which the scorer reads as `UNDECLARED` — neither `MET` nor `FAILS`. Counts on the carried scoring: MET 0, FAILS 6, UNVERIFIABLE 1, UNDECLARED 1, and no composite is emitted. | SUPPORTED | run_all conditions block; `selftest.py` "condition 1 is UNDECLARED" | the order's section carrying a statement on condition 1; a composite key in the scoring |
| ASC_004 | The hop-1 test is carried beside the eight and reaches none of them — a routing question kept apart from the independence question, as the order asks — and the common prior defense stated in full moves no condition (`INVARIANT`, moved `[]`): the order's "true at the transfer level and the structure failed anyway" as an invariance of the scorer. | SUPPORTED | `selftest.py` "hop-1 reaches none", "defense INVARIANT" | a defense item or the hop-1 field changing any condition's state |
| ASC_005 | A name-shaped subject is refused (`REFUSED_NAMED_PARTY`), so the scorer cannot be pointed at a named organization; the screen is a word list over registered-entity markers, stated as one, and a paraphrased name steps around it. | SUPPORTED | `selftest.py` "name-shaped subject is REFUSED" | a subject carrying a registered-entity marker that scores |
| ASC_006 | The pool metric is arithmetic on constructed graphs and the label on a funding edge enters none of it (AST-asserted over the three arithmetic functions): relabeling every edge moves no fraction on any of the three fields — the order's "a pool cannot audit itself by relabeling its outflows" shown as an invariance. Single pool reads `[1.0, 1.0, 1.0]`, disjoint sources `[0.0, 0.0]` (the reachable negative), mixed `[0.2, 1.0, 1.0]`. | SUPPORTED | run_all pool_metric block; `selftest.py` relabel checks | a relabel that moves a fraction; a `label` constant inside `coupled`, `assessor_fraction` or `field_distribution` |
| ASC_007 | The metric keeps three non-value states apart and never reads any of them as zero: no recorded funding is `None`, an undeclared amount on any funding edge makes the assessor `UNDECLARED` and drops it from the distribution with its own count, and second-order coupling through governance terminates on a cycle and is switchable by depth (`[CHOICE 1]`). | SUPPORTED | `selftest.py` "NO_RECORDED_FUNDING, fraction None", "A4 UNDECLARED", "governance cycle terminates" | an unfunded or undeclared assessor entering the distribution at 0 |
| ASC_008 | UNVERIFIED: the public records the metric wants (990s, grant databases) are egress-refused — three hosts answered 403 to CONNECT, measured and timestamped, `github.com` the control — so nothing here is a fraction for any real assessor, and whether the metric is measurable in practice is exactly as untested as the order's scope limit says. | UNVERIFIED | `pool_metric.EGRESS`; every field `CONSTRUCTED` | a real field's graph supplied to `--field` |
| ASC_009 | The disclosure audit reads DECLARED coverage and never a field's name (renaming every field leaves verdict and coverage unchanged), reaches all five verdicts on the constructed set, and returns the order's expected null on the money-only instrument: `MONEY_ONLY` with conditions 1 and 3 through 8 in `no_field`. An instrument whose only field is uncoded is `NOT_EVALUABLE`, kept apart from `NO_CONDITION_FIELD`. | SUPPORTED | run_all disclosure block; `selftest.py` disclosure section | a verdict that moves on a rename; an uncoded-only instrument reading as having no field |
| ASC_010 | The five non-financial couplings are parsed from the order and each reads `COVERED` or `UNMEASURED` against an instrument, never `ABSENT`: the order's "because there is no field, these read as ABSENT rather than unmeasured" is implemented as a return vocabulary with no `ABSENT` member. | SUPPORTED | `selftest.py` "coupling readout never returns ABSENT", "COVERED reachable" | an `ABSENT` reading on any coupling |
| ASC_011 | The precedent table parses to ten entries in three eras, every one `CARRIED_NOT_VERIFIED`, and every number extracted is extracted as written with a span that slices out of its own body; three entries carry a digit-adjacent number and a fatality figure written as a word is not extracted, which is the stated limit of a digit reader rather than a count. | SUPPORTED | run_all precedent block; `selftest.py` precedent section | a number asserted that does not slice out of the order's text |
| ASC_012 | The three entries with no stated remedy are the three closest to the present in the order's own table, read from the parse and not from the prose — consistent with the order's "solved, re-opened" and not evidence for it, since the table is illustrative by the order's own scope limit. | SUPPORTED | `selftest.py` "three most recent" | a remedy line on any of the last three entries |
| ASC_013 | Steps 2 and 3 are shipped as schemas with every cell `UNMEASURED`, and step 2's frame is stated: a survey of failure investigations is selected on failure and reports coupling among failures and no rate over arrangements (`IS_001`'s sampling-frame shape, which the order's scope limit already names); no cell is filled from memory. | SUPPORTED | `precedent.survey_schema`, `decay_schema`; `selftest.py` "no numeral in either schema" | a schema cell carrying a value |
| ASC_014 | Step 5 is NOT RUN and cannot be run from here: scoring a non-AI field blind as a calibration requires a party outside the sample, and the author is a member of the assessed class the current-position section is about. | SUPPORTED | run_all precedent block last lines; the declaration's position line | a blind scoring by a party outside the sample |
| ASC_015 | WO-4 and WO-5 are cited by the order for the shape, face 7 and the maintenance-app case, and neither is in this tree — checked by artifact (no folder's `WORK_ORDER.md` is headed by either), not by grep, so the check cannot fire on this folder's own mention of them. Named-and-absent, not reconstructed. | SUPPORTED | `selftest.py` "named-and-absent, by artifact" | a `WORK_ORDER.md` headed `# WO-4` or `# WO-5` landing |
| ASC_016 | Found by running: the defense parser matched seventeen bullets across the rest of the order on a multi-line regex, and the count guard refused it before any number was printed; repaired to read one section. | SUPPORTED | `selftest.py` "common prior defense parses to four items" | — (a record of the build's own slip) |
| ASC_017 | Found by running: the check that no authored file names an organization carried the names as a literal in the file that scans for them and fired on itself; the names are now taken from the parsed entries at run time and the scan is shown to fire on a plant (`UNI_010`). | SUPPORTED | `selftest.py` entry-name checks | the literal names reappearing in any authored file |
| ASC_018 | UNVERIFIED and it covers the folder: no assessor was scored, no record read, no instrument audited, no case verified; the order's own scoring is carried and the order itself asks for it to be re-verified before publication. Every finding is a property of the order's text, of constructed inputs, or of this build's arithmetic. | UNVERIFIED | every render's declaration | a second party with the records in hand running steps 1 and 4 on a real field |
