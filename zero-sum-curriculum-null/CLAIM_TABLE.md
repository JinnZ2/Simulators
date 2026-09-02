# zero-sum-curriculum-null — claim table

Claims are about the delivered null construction as a structure, and
about the instrument that reads it. None is a claim about the incident,
the transcripts, any corpus, or whether a zero-sum curriculum affected
anything.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph.

| id | claim | status |
|---|---|---|
| ZSN_001 | the header states a conjunction and the RESULT computes a disjunction; the two give different results and only the second is coherent | SUPPORTED |
| ZSN_002 | the branches are not independent: N2 and N5 carry the null only if N3 does, so the null survives with dependencies applied on N4 alone | SUPPORTED |
| ZSN_003 | N2's test has no outcome that carries the null by itself; both outcomes route through N3 | SUPPORTED |
| ZSN_004 | N2 is the sibling instrument's missing control arm and is expressible in its schema today, every cell UNMEASURED | SUPPORTED |
| ZSN_005 | the three artifacts N5 names are absent from this tree by content, and N5's counter-instance rests on transcripts the sibling records as NOT_RELEASED | SUPPORTED |
| ZSN_006 | N3's status assigns the residual to the curriculum, which the test as written does not establish | SUPPORTED |
| ZSN_007 | nothing here bears on whether the curriculum affected outcomes | UNVERIFIED |

## ZSN_001 — one word, two structures

The header reads *"each is a requirement; if any fails, the null fails
on that branch"*. A requirement is a conjunct: if every branch must
hold, N1 failing on its face empties the set and the RESULT is *the
null fails*, full stop. The RESULT reads *"the null survives only on
the two branches nobody has run"*, which is a disjunction: any surviving
branch carries the null. Computed both ways from the declared states —
conjunction survives on nothing, disjunction on {N2, N4} — and the
stated RESULT matches the second. The conjunction is not merely
uncharitable; it is unsatisfiable on the document's own terms, because
N1 requires the curriculum *absent* from the inputs and N2 requires it
*present*, so no setting satisfies both. The branches are alternative
routes by which the null could hold, and the header's word is the
`RD_002` one-word shape: say *route*, not *requirement*.

Falsifier: a reading of "requirement" under which N1 and N2 can hold
together.

## ZSN_002 — the branches lean on N3

Read as routes, the five are not independent. N2 (present, not
activated by the setting) leaves the observed probing to be explained
by something other than the curriculum; N5 (vocabulary only, not the
moves) leaves the moves to be derived without it. In both cases the
account is N3, the branch whose whole content is *behaviour fully
explained without the curriculum*. Encoded as two dependency edges,
each quoting the text it reads, and applied to a fixed point: the
survival set goes from {N2, N4} to **{N4}**, because N3 is PARTIAL by
the document's own status. So the RESULT's *"two experiments, named"*
is one experiment that stands alone (N4, an ablation run, beyond reach)
and one whose result is conditional on closing a residual the document
says is open. If N3 were closed, N2 would carry again — the selftest
asserts both directions.

Falsifier: a reading of N2 or N5 under which the null holds on that
branch with N3 failed.

## ZSN_003 — N2's outcome table

N2's test is *same models, possible tasks, transparent scorer; measure
probing rate*. Two outcomes. If the probing rate is equal across
settings, N2's requirement is met (the setting did not cue anything)
and the probing still occurred, so the null is not carried until N3
accounts for it. If the probing rate is lower on possible tasks, the
setting cued something and N2's requirement is not met — and whether
what it cued was the adversarial template or the substrate gradient is
exactly N3's question. Neither outcome closes the null. That is not a
defect in the control; it is what a control on activation can and
cannot say, and the document's *"missing control"* framing should carry
it.

## ZSN_004 — the control in the sibling's schema

`hf-incident-extract` codes the incident as a sheet and computes six
measures. N2's control is the same sheet coded from a second run, and
`n2_sheets()` builds both arms from the sibling's `SHEET` by import,
differing only in the `source` block. `n2_compare()` returns per-measure
differences with `None` propagating — a difference with an UNMEASURED
side is `None`, never 0 — and on filled constructed arms it computes
(M1 18.0 against 6.0, difference 12.0). Every real cell is UNMEASURED:
the incident arm wants the report, the control arm wants a run nobody
has made.

## ZSN_005 — named and absent

N5's test is *"the existing depth-stack instrument on the sacrifice
transcripts"* and its status cites *"the delay attempt, DEPTH 3"* as a
filed counter-instance. Searched by content across every `.md`, `.py`,
`.txt` and `.json` in the tree, this folder excluded so the check does
not read its own record: **0 files** carry any of the three. A planted
mention is found, so the scan is not silent by construction. Two things
follow. The instrument N5 calls existing does not exist here, so N5's
counter-instance is a record held elsewhere and is carried at
`ANC_010` status. And the sibling's sheet records the transcripts as
`NOT_RELEASED`; a depth-stack reading of *sacrifice transcripts*
presupposes access the sibling could not assume. Either the author has
access the sibling lacked, or the reading was of report excerpts. Not
resolved here.

## ZSN_006 — a residual is not an attribution

N3's status: *"partial; the opponent-assignment is the residual the
curriculum explains."* The test as written establishes that substrate
reasoning does not obviously predict treating the gate as opponent. It
does not establish that the curriculum does. The step from *not derived
from the substrate* to *explained by the curriculum* is an inference the
branch does not test, and it is the `UNI_005` shape: an absence in one
account recorded as a result for another. The residual is real; its
owner is not yet named by any test in the document.

## ZSN_007 — UNVERIFIED

No corpus scan, no transcript, no ablation, no control run. Every
result above is about the document's own logic and the instrument that
reads it. The drafting model and the auditing model are both inside the
class whose curriculum is the subject; declared, not resolved.

## ZSN_008 — the index tripped the absence check, and the check was changed rather than the index

`ZSN_005`'s check ran clean on first build: 0 files carried any of the
three names. Writing this folder's entry into `CLAUDE.md` and the root
`README.md` then put *depth-stack instrument* and *sacrifice
transcripts* into the tree, and the next run reported both present —
the repo describing the finding became the finding's counterexample.
This is `UNI_010`'s self-reference loop arriving through the index, the
route `notes/check_datasets.py` recorded and `question-availability`
`QA_007` said an exclusion list does not close. The repair is the one
`notes/` reached: hits are split into an *index* column (the two root
index files, which quote this folder) and an *independent* column, and
absence is read on the independent column only, so a hit anywhere else
still fires — a planted mention lands in the independent column and is
caught — while the index quoting the result no longer reads as an
antecedent. The index column is printed rather than excluded.

Falsifier: a file outside the two index files carrying one of the
names, which the independent column would report.
