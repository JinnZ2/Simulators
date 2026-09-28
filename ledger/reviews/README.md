# reviews/

Three append-only records feeding `ledger/review.py`, which computes
`ADDENDUM.md`'s criterion. Nothing here is ever edited or pruned.

## T0.txt

`T`, one ISO date, written by the first run over a non-empty record set
whose records are not all `CONSTRUCTED`. Written once, **never
overwritten** -- `T` is a fact about when the clock started, and a second
write would move a date `ADDENDUM.md` fixes in advance. `T+3` and `T+9` are
computed from it and from nothing else.

When `T0.txt` and the run log's first real-record date disagree,
`review.py` prints **which is earlier**, because the two directions have
different causes and only one is benign:

| direction | reading |
|---|---|
| **log earlier than T0** | records were reclassified out of `CONSTRUCTED` after T0 was written -- a run that did not start the clock then reads as one that could have. Expected and **benign**: T is when the clock started, not when it could first have started. Same signature from a second cause: a row logged before `all_constructed` existed reads as not-all-constructed, because an absent field is not a `False` one. |
| **T0 earlier than log** | T0 was written on a run whose records are `CONSTRUCTED` (which `[CHOICE 12]` is supposed to prevent), or T0 was written wrongly -- by hand, or by a run whose log line was lost. **Not benign.** T is the authority for the review dates, so a T no run supports puts T+3 and T+9 on a date nothing happened. Settle it before either review. |

Averaging is refused in both directions. `T0.txt` stays the authority.

Absent, the verdict is `CLOCK_NOT_STARTED` and there are no review dates.
`review.py` emits none rather than falling back on the pair computed from
the order date, which is wrong and is named as superseded on every run.

## RUNS.jsonl

One line per `ledger.py` run, written by the ledger itself unless
`--no-log`. Carries the date, the machine, the Python version, the record
count, the cross-ledger status, and `cobc --version` when there is a
compiler. Machine and compiler are recorded because the addendum counts
exposure in *distinct machines or compiler versions* and neither is
recoverable after the fact from a run that did not write it down.

It also records the HEAD `commit` and the `flagged_paths` a red flagged,
which is what makes the inferred override channel computable: without a
commit anchor per run a red can be correlated with a later commit only by
date, and a date is not an ordering. A row without one is reported
`UNCORRELATABLE`, never correlated approximately. `all_constructed` marks
a run over records that all declare themselves `CONSTRUCTED`; such a run
does not start the clock.

**A run whose `cross_ledger` is `UNAVAILABLE` is not a completed
cross-ledger run.** It contributes no exposure. Counting it would let the
DROP branch fire on runs that could not have produced a disagreement.

## EXPLAINED.jsonl

One line per cross-ledger disagreement, classifying it. The KEEP criterion
excludes a disagreement *explained by a rounding-mode difference in the
ledger sources themselves*, and whether a row is one is a judgement about
two ledger sources. Nothing infers it.

```json
{"ref": "sim:CLAIM_001", "run_date": "2026-10-01",
 "explained_by": "ROUNDING_MODE",
 "basis": "py uses ROUND_HALF_EVEN; LEDGER.cob line 141 uses ..."}
```

`explained_by` is one of `ROUNDING_MODE`, `SCALE`, `OTHER`, `UNEXPLAINED`.
`basis` is required. Only `UNEXPLAINED` rows satisfy KEEP. While any
disagreement is unclassified the verdict is `UNDECIDED` and names the
rows -- an unclassified row is neither a KEEP nor a not-KEEP.

## REVIEWS.jsonl

One line per review taken, written by `review.py --record`. Carries the
verdict, the exposure and disagreement state at the time, the bulk
measurements, and the two counts nothing can compute:

- `unique_findings` -- findings the ledger produced that no other check found
- `overrides` -- times a ledger red was overridden or ignored

Both require a stated basis and both accept `UNRECORDED`, which is kept
apart from `0`. See `ledger/OVERRIDES.md`.
