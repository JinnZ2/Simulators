# AUDIT_NOTES — closure-cost

Added, not delivered. [`closure.py`](closure.py) is the drop as received
and is not modified.

    python3 closure.py --selftest
    python3 closure_audit.py

## What the drop is

One file. Reads recorded cases where a variable was closed before the
event arrived.

The shape: **response failure tracks whether a variable was carried as
live**, not whether the event was severe and not whether information about
it was available. A variable closed as impossible has no handling class
attached, because none was ever needed. When the event fires the delay is
not reaction time — it is categorisation, the reading refused because it
contradicts something held as permanent.

Two branches, kept apart because they close different things.
**instrument** — a reliable intermediary becomes the reading and the
underlying quantity stops being sampled; failure clusters where the
intermediary has been correct longest. **event** — the event is closed as
not-happening-here, so procedure for it is never acquired or never
retained.

Selftest 15/15.

## File status

| file | status |
|------|--------|
| `closure.py` | delivered, verbatim |
| `README.md` | delivered drop 2, verbatim |
| `CLAIM_TABLE.md` | delivered drop 2 (C1–C5 + DISCLOSED WEAKNESSES), verbatim |
| `cases/hawaii-missile-alert.json` | delivered drop 2, verbatim |
| `cases/breakdown-cones.json` | delivered drop 2, verbatim — design only, no data |
| `cases/dash-warning-light.json` | delivered drop 2, verbatim — the instrument branch's only case |
| `closure_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Drop 2 delivered three cases. The README's STATE claims check out exactly:
three cases, zero quantified, every `spend` cell `--` and every
`knowledge_state` `not_separable`.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| CC_001 | The schema carries a **named rival hypothesis** (`procedure_gap`) and states that the rival is not independent of the shape; `knowledge_state` is four-valued with `not_separable` explicit — the sixth instance of the absent-vs-known-negative repair in this drop family and the third designed in | the rival being dropped, or `not_separable` collapsing into the three failures | SUPPORTED (holds) |
| CC_002 | `availability_rules_out_procedure_gap` uses `bool(...)`, so "checked, information absent" and "never recorded" both return `False` — in the one field that adjudicates the rival, while `budget_consumed` two lines away returns `None` correctly and is selftest-pinned | a three-valued return, or `None` being illegal in `AVAILABILITY` | SUPPORTED |
| CC_003 | `knowledge_separable` is `!= NOT_SEPARABLE`, so a case omitting `knowledge_state` reads as separable — the default runs toward the informative state | comparing against the vocabulary instead of one member of it | SUPPORTED |
| CC_004 | `--case` and `--branch` have no bounds check where both sibling tools do, so `--case` with no argument raises `IndexError`; and an unknown branch prints an empty table with rc 0 while an unknown case errors with rc 1 | the guard `--new` already uses being applied to both | SUPPORTED |
| CC_005 | The `instrument` branch is `uninstrumented`'s PROXY SUBSTITUTION with a rate term added — `signal.years_correct` — which the register's entry does not carry | the register's entry already carrying a time term | SUPPORTED |
| CC_007 | The README refuses to fill `diagnostic_spend` from Hawaii's 38 minutes and names the mechanism — *"substituting it would be proxy substitution"* — while filling the denominator, which is knowable | the field being filled from the error duration | SUPPORTED (holds) |
| CC_008 | The docstring says a case that mixes branches is recorded as `mixed`; the corpus has one such case, it is coded `event`, and both the case and C4 hold the question open | the case being recoded, or the rule being restated | SUPPORTED |
| CC_009 | `availability_rules_out_procedure_gap` needs a third value: the instrument case's rival is NOT APPLICABLE and the boolean returns `False`, the same value a checked-and-absent event case returns | a three-valued return | SUPPORTED — `CC_002` instanced |
| CC_010 | Two circularities are disclosed before use — `variable_state` inferred from the same evidence C3 rests on, and C5's nearest series carrying a denominator modelled per the category under test — and `signal.years_correct` is 0 of 3 filled, including on the branch it defines | either circularity being softened, or a filled rate term | SUPPORTED (holds) |
| CC_006 | With no `cases/` directory the tool prints a well-formed report with zero rows and exits 0 — third tool in the family to do so, and the three that refuse are the older ones | the empty state refusing, or saying it is empty | SUPPORTED |

## 1 — CC_001, a rival held as a field

**A named rival, in the schema.**

> Missing procedure is the obvious competing account of non-response. It
> is not independent: nobody acquires a protocol for an event they have
> closed. So procedure absence can be a downstream readout of the closed
> prior rather than an alternative to it. That collapse is not automatic.
> It is asserted per case, with the ground stated, and the field records
> which.

`procedure_gap.collapsed_into_closure` and `procedure_gap.ground` carry
it. First folder in this drop family to hold its competing explanation as
a schema field rather than as prose — and first to state that the rival is
**not independent** of the shape, which is the harder admission, because a
non-independent rival cannot be ruled out by finding the shape.

**Four-valued knowledge state.** Three failures with different signatures
and different remedies, plus an explicit state for the record being unable
to separate them, with the reason given: *"Most disaster self-report
cannot separate them, and the field says so rather than guessing."*

Sixth instance of one repair in this family, third designed in:

    PB_004   frame_sim option_gain          0 options found == never ran
    PB_012   binary_audit handoff()         above ceiling == never checked
    GC_004   MECHANISM_10 R3                not cited == no corpus searched
    MD_002   moral-decomposer reduces_to    irreducible == routed elsewhere
    GC_010   SUBCASE_10A S1                 absent vs zero -- specified
    DL_008   anchor.py routing states       unrouted vs absent -- implemented
    CC_001   closure.py knowledge_state     three failures vs not_separable

§2 and §3 are the two places in the same file where the discipline is not
applied.

## 2 — CC_002, the discriminator merges its own null

    rules_out = bool(avail in (PRESENT, PRESENT_LOCAL) and var == CLOSED)

`availability_rules_out_procedure_gap` is the field that decides between
the shape and its rival, and the docstring says so. `AVAILABILITY`
includes `None` as a legal value.

    state                                  availability             rules_out
    checked, information was absent        absent                  False
    never recorded (None is legal)         None                    False
    checked, information present           present                 True
    checked, local memorialised instance   present_local_instance  True

Rows 1 and 2 are different states with one value. *"We looked and the
information was not there, so the procedure gap stands on its own"* and
*"nobody recorded whether it was there"* are the measurement and its
absence.

What makes this sharp rather than routine is that **the same function
keeps the distinction two lines away, and the selftest pins it**:

    budget_consumed on an unfilled case : None    <- selftest: "budget flag none not false"
    rules_out       on an unfilled case : False   <- no check

Same repair, same file, one applied and one not — in the field that
adjudicates the rival the whole design is built around. A three-valued
return needs no new vocabulary: `None` when availability was not recorded,
`False` when it was recorded absent.

## 3 — CC_003, a default that runs toward the claim

    "knowledge_separable": c.get("knowledge_state") != NOT_SEPARABLE

    states not_separable   not_separable   separable=False
    states not_taught      not_taught      separable=True
    omits the field        None            separable=True

A case omitting `knowledge_state` reads as **separable** — the informative
state. That is the opposite of `presented-binary`'s `binary_audit`, where
every default runs toward `absent` (`PB_008`).

`SKELETON` defaults the field to `not_separable`, so anything from `--new`
is safe; a hand-written case is not, and the selftest covers the stated
values and not the omitted one. The fix is §2's: compare against the
vocabulary rather than against one member of it.

## 4 — CC_004, argument handling

    domain-ledger/ledger.py        bounds-checked lookup: True
    domain-ledger/anchor.py        bounds-checked lookup: True
    closure-cost/closure.py        bounds-checked lookup: False

    closure.py --case            IndexError, rc 1
    closure.py --case unknown    "no case named unknown", rc 1
    closure.py --branch unknown  empty table, rc 0

Both sibling tools guard the lookup after a flag. `--new` in this same
file is guarded, so the pattern is known and applied once of three times.

The second asymmetry is between the two lookups: an unknown case errors,
an unknown branch prints an empty table and exits clean. A typo in a
branch name is indistinguishable from a branch with no cases — §2's shape
one layer out, at the CLI.

## 5 — CC_005, mechanism 6 with a rate

> **instrument** — a reliable intermediary exists and becomes the reading.
> The underlying quantity stops being sampled directly. Failure clusters
> where the intermediary has been correct for a long time, which is the
> inverse of how reliability is usually scored.

The first sentence is `uninstrumented/`'s sixth mechanism, PROXY
SUBSTITUTION — *"an enforceable measure displaces the target it stood in
for"*, worked there as hours-since-last-drive standing in for fitness to
drive.

The second sentence is not in the register. PROXY SUBSTITUTION as filed
has no time term: it says the displacement happened, not that exposure
accumulates with the proxy's track record. `signal.years_correct` is that
term, and the claim on it is directional — a longer correct record is a
larger exposure, because reliance grew with it and direct sampling
stopped.

An addition to an existing mechanism rather than a new one, and checkable
in principle with no new vocabulary: across recorded instrument failures,
is time-since-last-direct-sample correlated with response delay. The field
exists; no case does.

## 6 — CC_006, the empty report, third time

    rows printed  : 0
    lines printed : 12
    exit code     : 0

    category-weld/weld.py               refuses on empty: True
    presented-binary/binary_audit.py    refuses on empty: True
    generation-capacity/capacity.py     refuses on empty: True
    domain-ledger/ledger.py             refuses on empty: False
    domain-ledger/anchor.py             refuses on empty: False
    closure-cost/closure.py             refuses on empty: False

Three refuse, three print, and the split is by drop age rather than by
design intent.

`closure.py` does better than the other two on one point: its footer
states the corpus condition, not only the column meanings.

> No case here quantifies the mechanism. These are properties of the
> records, and the records were not built to ask this.

True of an empty run and of a full one, and the right framing for a folder
whose readouts are all properties of records written for another purpose.
`DL_005` stands for all three: the line prints over zero cases and reads
the same.

## 7 — CC_007, a refusal with the mechanism named

> It does not estimate diagnostic spend where the source lacks the
> numbers. Hawaii's 38 minutes is the duration of the **error**, not of
> anyone's decision, and substituting it would be **proxy substitution**.

`diagnostic_spend` is the readout the folder exists for. A 38-minute
number sits in every account of the incident and would fill the cell. The
author names why it must not: it measures a different quantity, and
putting it there would be `uninstrumented/`'s sixth mechanism — an
enforceable measure displacing the target it stood in for.

The refusal is specific rather than blanket:

    hawaii latency.budget_seconds     900
    hawaii latency.diagnostic_seconds None
    resulting diagnostic_spend        --

Budget is flight time under a real threat — a property of the physics, and
knowable. The numerator is a per-respondent time-to-first-protective-action
distribution, which nobody published. One half filled, one half refused,
with the note saying which and why.

Elsewhere in this repo the register's mechanisms diagnose an instrument
after the fact. Here one is used ahead of time as a reason not to produce
a number.

## 8 — CC_008, the mixed branch

    instrument   1
    event        2
    mixed        0

> A case that mixes them is recorded as mixed rather than forced into one.

The corpus contains exactly one case that mixes them, and it is coded
`event`. From `hawaii-missile-alert`'s own signal note:

> some discounted the alert because air-raid sirens were not sounding,
> treating silence on a different instrument as evidence of no threat.
> **That fragment is an instrument-branch reading sitting inside an
> event-branch case.**

Its open list and C4's status say the same thing in the same words:
whether it should be split out is unsettled.

So the rule and the open question point different ways. The docstring says
record it `mixed`; the case holds open between splitting it into a
separate instrument case and leaving it. Both are reasonable; neither is
what the stated rule prescribes.

Related to `DL_011` and distinct from it. There `absent_established` was
unused because no link had been investigated far enough to earn it — the
state was unearned. Here the state is earned, acknowledged twice in the
delivery, and a different value is recorded.

## 9 — CC_009, the third value the boolean needs

    dash-warning-light
      variable_state           not_assessed
      information_availability present
      rules_out                False
      procedure_gap collapsed  None
      ground                   Not applicable on this branch. Procedure is
                               not the missing quantity; direct sampling is.

`CC_002` recorded that the field merges "checked, information absent" with
"never recorded". The instrument case adds a third state it cannot hold:
**not applicable**. The procedure-gap rival is an event-branch object; on
the instrument branch the missing quantity is direct sampling.

`collapsed_into_closure` reads `None` here, correctly. `rules_out` reads
`False` — the same value an event case returns when the information was
checked and found absent, which on that branch is a substantive finding.

Three distinctions now, not two. The information is in the record and
prints in `detail()`; the derived boolean is the only place it collapses —
`DL_003` and `DL_012`'s shape, where the per-item text survives and the
scalar merges.

## 10 — CC_010, two circularities, disclosed

> `variable_state` is inferred, never measured. ... In Hawaii it is
> inferred from the procedure-knowledge finding, which is the same
> evidence C3 uses — so C3 and the coding of that case are not
> independent.

It holds: hawaii's `variable_state: closed` and its `procedure_gap.ground`
both rest on the survey finding, and C3's status cites that same case.

C5 discloses a second one about a series not yet used:

> The rail-crossing data is the nearest available series and the exposure
> denominator there is modelled per warning-device category, which is
> circular for this purpose.

A denominator modelled per device category cannot test a claim about which
device categories fail. That is `GC_003`'s shape — a denominator that does
not survive the question asked of it — caught in advance rather than in
audit.

Both cost the drop something and neither is softened: C3's support is one
case whose coding is not independent of it, and C5's nearest data is
unusable as constituted.

    breakdown-cones        branch=event       years_correct=--
    dash-warning-light     branch=instrument  years_correct=--
    hawaii-missile-alert   branch=event       years_correct=--

`signal.years_correct` is the rate term that makes C5 invert standard
scoring, and it is 0 of 3 — including on the one case on the branch it
defines. The case names where the number would come from ("the
rail-crossing signal ... is a separate case file and is not yet written"),
which is a statement of intent rather than a verification claim about a
file that should exist. Different shape from `CW_001` / `PB_001` /
`GC_009`, and worth keeping apart from them.

## 11 — CC_003, not tripped, which is the point

    breakdown-cones        knowledge_state=not_separable   separable=False
    dash-warning-light     knowledge_state=not_separable   separable=False
    hawaii-missile-alert   knowledge_state=not_separable   separable=False

All three cases state `not_separable` explicitly, so the fail-open default
`CC_003` records is never exercised by the delivered data — and the README
says this is *"the honest state of the published record rather than a gap
in the transcription"*, which the table confirms.

That is why the defect survives. A default running toward the informative
state is invisible on data written by someone who knows the schema, and
fires on the first case written by someone who does not — which, for a
folder whose README invites others to add cases, is the population it will
meet.

## Relation to the rest of the repo

- `uninstrumented/` — §5. The `instrument` branch is PROXY SUBSTITUTION
  with a rate term the register's entry does not carry.
- `domain-ledger/` — §4 and §6. Closest sibling by shape: a scorer with a
  selftest, no corpus, and readouts that are properties of records.
- `presented-binary/` — §3. `PB_008` records every default running toward
  `absent`; this one runs the other way.
- `null-harness/` — §2 and §3 are both fail-open defaults in a tool whose
  vocabulary is built to keep unknown apart from known-negative.
- `generation-capacity/` — §10. `GC_003`'s denominator shape, disclosed in
  advance here; and the README names the shared recall-method defect with
  R1 explicitly.
- `thermal-sensor-degradation-audit/` — the `instrument` branch is the
  same object from the other side: there the package degrades during the
  event it records, here the intermediary is trusted because it has not.
