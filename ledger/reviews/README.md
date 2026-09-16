# reviews/

Three append-only records feeding `ledger/review.py`, which computes
`ADDENDUM.md`'s criterion. Nothing here is ever edited or pruned.

## RUNS.jsonl

One line per `ledger.py` run, written by the ledger itself unless
`--no-log`. Carries the date, the machine, the Python version, the record
count, the cross-ledger status, and `cobc --version` when there is a
compiler. Machine and compiler are recorded because the addendum counts
exposure in *distinct machines or compiler versions* and neither is
recoverable after the fact from a run that did not write it down.

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
