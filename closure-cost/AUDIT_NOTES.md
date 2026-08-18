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
| `cases/` | not delivered — no case has been recorded |
| `README.md`, `CLAIM_TABLE.md` | not delivered |
| `closure_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Nothing here invents a case. A case is a record of an incident, and
writing one would put an account in the author's mouth.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| CC_001 | The schema carries a **named rival hypothesis** (`procedure_gap`) and states that the rival is not independent of the shape; `knowledge_state` is four-valued with `not_separable` explicit — the sixth instance of the absent-vs-known-negative repair in this drop family and the third designed in | the rival being dropped, or `not_separable` collapsing into the three failures | SUPPORTED (holds) |
| CC_002 | `availability_rules_out_procedure_gap` uses `bool(...)`, so "checked, information absent" and "never recorded" both return `False` — in the one field that adjudicates the rival, while `budget_consumed` two lines away returns `None` correctly and is selftest-pinned | a three-valued return, or `None` being illegal in `AVAILABILITY` | SUPPORTED |
| CC_003 | `knowledge_separable` is `!= NOT_SEPARABLE`, so a case omitting `knowledge_state` reads as separable — the default runs toward the informative state | comparing against the vocabulary instead of one member of it | SUPPORTED |
| CC_004 | `--case` and `--branch` have no bounds check where both sibling tools do, so `--case` with no argument raises `IndexError`; and an unknown branch prints an empty table with rc 0 while an unknown case errors with rc 1 | the guard `--new` already uses being applied to both | SUPPORTED |
| CC_005 | The `instrument` branch is `uninstrumented`'s PROXY SUBSTITUTION with a rate term added — `signal.years_correct` — which the register's entry does not carry | the register's entry already carrying a time term | SUPPORTED |
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

## Relation to the rest of the repo

- `uninstrumented/` — §5. The `instrument` branch is PROXY SUBSTITUTION
  with a rate term the register's entry does not carry.
- `domain-ledger/` — §4 and §6. Closest sibling by shape: a scorer with a
  selftest, no corpus, and readouts that are properties of records.
- `presented-binary/` — §3. `PB_008` records every default running toward
  `absent`; this one runs the other way.
- `null-harness/` — §2 and §3 are both fail-open defaults in a tool whose
  vocabulary is built to keep unknown apart from known-negative.
- `thermal-sensor-degradation-audit/` — the `instrument` branch is the
  same object from the other side: there the package degrades during the
  event it records, here the intermediary is trusted because it has not.
