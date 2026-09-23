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
WO-6, delivered verbatim as `WORK_ORDER.md` (sha256
`33436ac4f7203b8f8f7b82dd7a41c0a8f761a4f3af1bd449b60ed98b4307b099`), and
built as an instrument to its five runnable next steps. The measurand, in
the order's own words:

```
Whether an assessor is structurally independent of the party it assesses
— distinguished from whether a direct payment runs between them.

  hop-1 test:  does the assessed pay the assessor?
  pool test:   is the funding source, credentialing body, career path
               and governance of the assessor independent of the OUTCOME
               being assessed?
```

The order is NOT ABOUT ANY NAMED ORGANIZATION and neither is this folder:
no authored file carries an organization's name, asserted by the suite
against the names the order's own table carries, which the renders print
only because they parse the order at call time. Stdlib only, parses under
3.9, phone-buildable, CC0. No network module anywhere; nothing imported
from outside this folder.

## Contamination, declared before any number

`run_all.py` prints this first; repeated here so a reader meets it before
any table.

| axis | declaration |
|---|---|
| authorship | every file is model-authored in one session by the hand that wrote the checks AND the fixtures they are pinned to |
| position | the author is a member of the assessed class the order's current-position section is about; nothing here scores any assessor, and the one scoring shipped is the order's own, carried |
| parties | no organization is named in any authored file |
| records | no 990, grant database, COI instrument or archive was read: the record hosts answered 403 to CONNECT, measured and timestamped in `pool_metric.EGRESS`, `github.com` the connecting control; every graph, instrument and schema is CONSTRUCTED and says so |
| precedent | every table entry is `CARRIED_NOT_VERIFIED`; numbers are extracted as the order wrote them, with a span, and asserted by nobody here |
| companions | WO-4 and WO-5, cited by the order, are not in this tree (named-and-absent, checked by artifact: no folder's `WORK_ORDER.md` is headed by either) |
| interest | the thesis lowers what an evaluation of the author's class can establish and raises the demand for stricter evaluation of it; the two run opposite ways, so the thesis is left unresolved here rather than resolved either way |

## The four parts and the two steps not run

| step | file | input | what it returns |
|---|---|---|---|
| remedy set | `conditions.py` | a scoring as JSON (`--record`), default the order's carried one | per condition `MET` / `FAILS` / `UNVERIFIABLE` / `UNDECLARED`, counts per state, no composite; `REFUSED_NAMED_PARTY` on a name-shaped subject |
| 1 pool metric | `pool_metric.py` | a funding graph as JSON (`--field`), default three constructed | per assessor a fraction, `NO_RECORDED_FUNDING` (None) or `UNDECLARED`; the field's sorted distribution |
| 4 disclosure audit | `disclosure_audit.py` | COI instruments as JSON (`--instruments`), default four constructed | per instrument `MONEY_ONLY` / `BEYOND_MONEY` / `NO_CONDITION_FIELD` / `NOT_EVALUABLE` / `MALFORMED`; the five couplings each `COVERED` or `UNMEASURED` |
| record + 2, 3 | `precedent.py` | `WORK_ORDER.md` | the ten entries parsed and carried; the survey and decay schemas with every cell `UNMEASURED` |
| 5 | — | — | NOT RUN: scoring a non-AI field blind requires a party outside the sample, and the author is inside it |

```
python3 assessor-coupling/run_all.py     # declaration, then all four parts
python3 assessor-coupling/selftest.py    # the null-tested suite; prints its own count
python3 assessor-coupling/conditions.py --record scoring.json
python3 assessor-coupling/pool_metric.py --field graph.json
python3 assessor-coupling/disclosure_audit.py --instruments coi.json
```

Every library module refuses `--selftest` (exit 2) and names the suite.

## The remedy set as a scorer

```
WORK_ORDER.md ---parse at call time---> conditions 1..8 (retyped copy holding 7 raises)

scoring = { hop1_stated: bool,  states: {1..8 -> MET|FAILS|UNVERIFIABLE|UNDECLARED} }
                 |                          |
        a routing question,          counted per state, printed per condition,
        reaches none of the 8        NO composite

carried scoring (the order's current-position section, no party named):
   1 UNDECLARED   2 UNVERIFIABLE   3..8 FAILS      MET 0
common prior defense, all four items stated vs none:  INVARIANT, moved []
```

The order scores seven of eight conditions and says nothing about the
first (authority not revocable by the assessed); the scorer reads that as
`UNDECLARED` and not as either `MET` or `FAILS`. The defense the order
says every precedent ran is carried as four booleans and read by no
condition check, so stating it in full moves nothing — the order's "true
at the transfer level and the structure failed anyway" as an invariance.

## Step 1 — the pool metric on constructed graphs

```
source --funds--> assessor         coupled iff source: funds the sector
source --label--> (grant | contract | salary | ...)       | holds equity in it
                   |                                     | is governed by an equity holder
                   +-- read by NOTHING (AST-asserted)          (depth 2, [CHOICE 1])

fraction(assessor) = coupled funding / total funding
   no recorded funding  -> None, never 0        undeclared amount -> UNDECLARED
field output = sorted fractions + the unmeasurable counted apart; no name ranked

single_pool  [1.0, 1.0, 1.0]     disjoint  [0.0, 0.0]     mixed  [0.2, 1.0, 1.0] + 1 UNDECLARED
relabel every edge 'salary':  moved = False on all three
```

The order's structural claim — a pool cannot audit itself by relabeling
its outflows — is shown rather than stated: the label on the pipe enters
no arithmetic, so no relabeling moves any fraction. Nothing here is a
fraction for any real assessor; the records that would supply one are not
reachable from this environment.

## Step 4 — which conditions a disclosure instrument has a field for

Coverage is DECLARED per field and never read from the field's name
(renaming every field leaves the verdict unchanged, asserted). The
expected null is `MONEY_ONLY` and the constructed money-only instrument
returns it with the other seven conditions in `no_field`. The five
non-financial couplings the order lists are parsed from it and read
against an instrument as `COVERED` or `UNMEASURED` — never `ABSENT`,
because the field that would carry the negative does not exist, which is
the order's own sentence about why they read as absent.

## The precedent record, and steps 2, 3, 5

The ten entries are parsed from the order and carried whole, each
`CARRIED_NOT_VERIFIED`. Two things the parse shows that the prose does
not say: the three entries with no stated remedy are the three closest to
the present, and a fatality figure written as a word (*Thousands*) is not
extracted by a digit reader, so the count of numbered entries is a floor.
Step 2's schema states its sampling frame — a survey of failure
investigations is selected on failure, so it reports coupling among
failures and no rate over arrangements, which the order's own scope limit
already says. Step 3's schema names the four remedies and leaves every
cell `UNMEASURED`. Step 5 is not run.

## Choices

| id | where | what |
|---|---|---|
| CHOICE 1 | `pool_metric.GOVERNANCE_DEPTH` | second-order coupling followed two hops through boards |

## Found by running, not by reading

- The defense parser matched seventeen bullets on a multi-line regex and
  the eight-conditions parser was what caught it, since a check on the
  item count refused; repaired to read one section.
- The suite's check that no authored file names an organization wrote
  the names as a literal in the file that scans for them, and fired on
  itself; the names are now taken from the parsed entries at run time
  (`UNI_010`).

## Relation to the rest of the tree

`chain-position/` is WO-1, the load-bearing criterion the order connects
to; `effective-redundancy-audit/` and `design-basis-ai/` hold the
shared-node arithmetic one level up; `internal-reference-boundary/` is
the same invariant (a boundary drawn by the party inside it) on a
different axis. Nothing is imported from any of them. WO-4 and WO-5 are
not in this tree.

## Scope limits honored

The precedent table is illustrative and no base rate is computed. No
claim is made about any contemporary assessor; the only scoring is the
order's own, marked carried and re-verified against nothing. Whether the
pool metric is measurable in practice is untested here — it runs on
constructed graphs and the public records it wants are egress-refused.
