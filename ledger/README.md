# ledger

Every shipped claim value, as a **committed expected value**.

Two arms over one set of claim records:

| | authoritative for | dependencies |
|---|---|---|
| `py_ledger/` | REACHABILITY -- which claims can be recomputed at all | none, stdlib `decimal`, runs on a phone |
| `cobol_ledger/` | PRECISION -- what the arithmetic comes to | GnuCOBOL |

## Three diffs, and it exits nonzero if any of them fires

**1. INTERNAL** -- the asserted value against the value recomputed from its
own operands. **This is the strongest finding the ledger can produce**, and
it is reported first, at the top, not in a list. A claim that disagrees with
its own arithmetic is wrong from inside; nothing external has to be true for
that to be a finding.

**2. DRIFT** -- the current value against the committed `EXPECTED/` value.
Appended to `DRIFT.md` with the date, the machine and the Python version.
**Never pruned.** A pruned drift log cannot tell a value that never moved
from one whose movement was deleted.

**3. CROSS-LEDGER** -- `py_ledger` against `cobol_ledger`. A disagreement
goes to `DISAGREEMENTS.md` and is **never resolved by picking a winner**:
the two arms are authoritative for different things, and a row there is a
place where those two authorities return different numbers. An arm that is
unavailable marks every claim in the run `PRECISION_UNVERIFIED`. It is never
reported as agreement.

It also reports, without exiting on them: provenance resolved
**transitively** (a `DERIVED` claim whose support reaches a `CARRIED` value
becomes `DERIVED_WEAK` and names the weak operand); claims that could not be
recomputed and why; and `FALSIFIER_UNTESTED`, because a falsifier with no
test is a sentence, not a check.

## A SEEDED value is NOT a verified value. It is a pin.

The first run writes an `EXPECTED/<sim>/<claim_id>.txt` for every claim it
has no pin for, marked `SEEDED` with that day's date. Seeding is not
verification. It records what the value was on the day the ledger first saw
it, so that the next run can tell you whether it is still that.

A pin's state is `SEEDED` or `CONFIRMED`. **The ledger only ever writes
`SEEDED`** -- a ledger that could promote its own pin has verified nothing,
so promotion is a human edit and shows up in a diff.

A claim with no pin is seeded and is **not** drift. A new claim has nothing
to have drifted from.

## What this does not do

- It **does not run sims**.
- It **does not time anything**.
- It does not say any claim is true.
- It does not say any sim is correct.
- It does not say a `CARRIED` value is grounded.

It checks that what the repo says it computes is what it computes, and that
it keeps computing it.

## State

`records/` is **empty**. Nothing in this repository emits claim records yet;
see `records/README.md`. `ledger.py` refuses an empty record set with exit 2
rather than printing a clean ledger over zero rows.

`cobol_ledger/LEDGER.cob` **has never been compiled and has never been
run.** GnuCOBOL is absent from the environment it was written in -- `cobc`
and `cobcrun` both resolve to nothing. Every run in that environment reports
the cobol arm `UNAVAILABLE` and every claim `PRECISION_UNVERIFIED`. The
selftest exercises the cross-ledger diff's firing direction against a
**stub**, which shows that `ledger.py` routes and records a disagreement
correctly and is not evidence that `LEDGER.cob` works.

## ADDENDUM.md -- the criterion, committed before the ledger runs

The cobol arm rests on an **untested hypothesis**: that float arithmetic
corrupts claim values in this tree. Nothing here has demonstrated it.
`ADDENDUM.md` was committed before the ledger ran, and it fixes KEEP, DROP
and UNDECIDED in advance so a reassessment written after the results is not
subject to the same pull that produced them.

It is landed **byte-exact, em dashes included** -- the repo's ASCII
convention is waived here for the same reason `AGENTS.md` waives it, and
more sharply: a document whose own first rule is *do not edit after
results* is not one to transliterate. `review.py` asserts its hash is
unchanged across every run and **parses the thresholds out of it** rather
than carrying a second copy that could drift.

```
python3 ledger/review.py
```

Today it returns **UNDECIDED**, for the reason the addendum names: zero
completed cross-ledger runs, which is fewer than three. A run in which the
cobol arm was UNAVAILABLE is **not** a completed cross-ledger run and
contributes no exposure -- counting it would let the DROP branch fire on
runs that could not have produced a disagreement.

The clock has not started either: `T` is the first run over a **non-empty**
record set (`[CHOICE 7]`), and there has not been one. `review.py` prints
the other reading beside it.

### Dates are computed from T, not from the order date

`T` is written to `reviews/T0.txt` by the first run over a non-empty record
set whose records are not all `CONSTRUCTED` (`[CHOICE 12]` -- the fixtures
are a non-empty record set, and a run over them would otherwise start the
clock on data that is not a measurement of anything). It is written once
and never overwritten, and that run prints `T`, `T+3` and `T+9` once.

`T+3 = 2026-10-07` and `T+9 = 2026-11-18` were computed from the date the
order was written rather than from `T`. **They are wrong and they are
superseded.** `review.py` names them on every run, because a wrong number
in circulation with nothing contradicting it stays in circulation.

`T0.txt` is the authority; the run log's first real-record date is computed
beside it as a cross-check, and the two coming apart is reported rather
than averaged.

### The real signal, and two channels that are never merged

The addendum names the override count as the real signal -- *a gate that
gets routinely overridden has become bulk regardless of what it catches* --
and an override happens outside the ledger and leaves no trace in it. From
inside the gate, a gate that is routinely overridden and a gate that never
is look identical.

**DECLARED.** A field, `UNRECORDED` kept apart from `0`, `--record`
refusing either without a stated basis, and `OVERRIDES.md` so the count can
ever be a number at all. It is **self-reported: an unlogged override is
indistinguishable from no override, and once nonzero the count is a FLOOR,
not a measurement.** The same holds for *findings no other check found*.

**INFERRED.** A second channel requiring nobody's cooperation: a red exit,
then a commit touching a path the red flagged, with **no `OVERRIDES.md`
entry in between**. Read straight out of git history. For it to be
computable at all the run log records the HEAD commit and the flagged paths
per run (`[CHOICE 9]`, `[CHOICE 10]`) -- a date is not an ordering, and a
run logged without a commit anchor is reported `UNCORRELATABLE` rather than
correlated approximately.

**The two are never added, averaged or reconciled** -- asserted
structurally, not promised. One is what people said; the other is what the
history shows. The inferred channel does not close the gap: it observes a
*different* quantity that overlaps the one the addendum asks for, with its
own floor (a red acted on outside git leaves nothing) and its own ceiling
(a commit touching a flagged path for an unrelated reason is counted).

If git history is not reachable, the channel reports `GIT_UNREACHABLE` and
stops. **It does not approximate one.** An empty run log reports `NO_RUNS`,
not a clean `0` -- nothing to correlate against is not the same as nothing
to find.

`reviews/EXPLAINED.jsonl` classifies each disagreement. KEEP excludes a
disagreement *explained by a rounding-mode difference in the ledger sources
themselves*, and whether a row is one is a judgement about two sources.
While any disagreement is unclassified the verdict is UNDECIDED and names
the rows: an unclassified row is neither a KEEP nor a not-KEEP.

## Running it

```
python3 ledger/ledger.py --records ledger/fixtures/records \
                         --expected /tmp/exp --no-log
python3 ledger/ledger.py --choices
python3 ledger/review.py --time
python3 ledger/selftest_ledger.py
```

The fixtures are CONSTRUCTED and say so in their own `status` fields. They
exist to exercise every path the ledger has -- agreement, internal
disagreement, a measured zero divided into, an operand nobody can find, a
two-claim cycle, a `CARRIED` value one and two hops upstream, a bare
reference resolving locally beside a qualified one crossing sims. No value
in them is a measurement of anything.

## Schema decisions that were not in the order

Both are declared rather than slipped in, and `--choices` prints the rest.

1. **`expression`, required for `DERIVED`.** The order asks the ledger to
   recompute a `DERIVED` claim from its operands. A list of operands does
   not say what was done with them -- `[a, b]` recomputes to `a+b`, `a*b`,
   `a/b` or `a-b` with equal warrant -- and picking one would be the ledger
   inventing the arithmetic it exists to check.

2. **Qualified operand references.** The order writes operands as a list of
   `claim_id`s, and in this repository a `claim_id` is not unique. Measured,
   not assumed: five prefixes across twelve folders.

Stdlib only. Parses under Python 3.9. CC0.
