# Criteria Drift Auditor

Measure the ruler, not just the model.

A stdlib-only Python toolkit for tracking how benchmark and evaluation criteria change over time, and for regressing reported model improvement against that criteria drift.

## Why

When a benchmark saturates, authors expand the criteria. When a rubric drifts, the sign of "better" shifts. When the judge model upgrades, the outcome column moves. Most of this is invisible in headline numbers.

This tool makes it visible by:

1. **Versioning criteria artifacts** with a declared frame (boundary, horizon, who_counts, sign_source, logic, observer_access)
2. **Computing drift** between consecutive versions on their own axis
3. **Regressing** reported model improvement against criteria drift

If the slope is positive and significant, some fraction of "progress" is the ruler stretching.

## The unlogged case

`unlogged_move.py` is the counterpart to everything above. The rest of this
folder assumes versions are declared and measures how fast a declared ruler
moves. That module asks what happens when the ruler moves and **no version is
cut** — the distinction PREAMBLE.md's TERM COLLISION note draws between
REVISION (provenance-bearing, the move is logged) and ASSERTION (no cause
named, nothing records that the criterion moved).

One identical series of twelve readings, read three ways:

| reading | step | → system | error | flagged |
| --- | --- | --- | --- | --- |
| `ASSERTION` | +0.150 | +0.150 | **+0.150** | no |
| `REVISION` | +0.150 | `None` | `None` | yes |
| `REVISION_WITH_BRIDGE` | +0.150 | +0.000 | +0.000 | yes |

The system did not move at all in that scenario. `ASSERTION` reports a 15-point
improvement and carries no flag. Run it again with a real +0.10 system change
and `ASSERTION` reports +0.25 — **wrong by exactly the unlogged move in both
cases**, an error that does not depend on whether the system changed and is not
visible from inside the reading.

Two results worth having:

- **Logging alone does not decompose.** `REVISION` returns `None` for the
  system attribution, not zero. Separating system from criterion needs a
  *bridge* — one measurement taken under both criteria — and without it
  `UNKNOWN` is the correct output. In any summary table `None` will look like
  the reading that failed to produce a result; it is the one that produced the
  right one.
- **"Uninterpretable" understates it.** The prior readings stay present,
  numeric, in range and continuous; nothing in the data marks the move. The
  failure is not a gap where an answer should be — it is a confident wrong
  answer in the same shape as a right one. A blank announces itself; this does
  not.

A third result, about this repo rather than about criteria: **the bridge is
`anchor.py`'s argument, not this module's.** That file already establishes the
same requirement from cross-domain cases — an invariant scored across versions
— and `audit.py regress` already refuses an identified criteria term without
one. Two modules in one folder, by one builder, agreeing is
`operator-structure-echo/corroboration.py`'s `INHERITED` state on a real pair:
one position expressed twice, not two lines of evidence. The sim demonstrates
a requirement established next door; it does not corroborate it.

```
python3 unlogged_move.py [--selftest]     # 24 checks
```

## Design constraints

- **Stdlib only** — no pip install, no cloud APIs, no fragile dependencies
- **SQLite backend** — durable, inspectable, works offline
- **JSON in/out** — human-readable, version-controllable
- **Modular** — any piece can be replaced or repaired

## Quick start

```bash
# 1. Initialize database
python audit.py init

# 2. Ingest criteria versions (example data included)
python audit.py ingest-criteria example_data/codebench_v1.json
python audit.py ingest-criteria example_data/codebench_v2.json
python audit.py ingest-criteria example_data/codebench_v3.json
python audit.py ingest-criteria example_data/codebench_v4.json

# 3. Ingest model scores
for f in example_data/score_*.json; do
    python audit.py ingest-score "$f"
done

# 4. Compute drift history
python audit.py drift CodeBench

# 5. Regress improvement vs drift
python audit.py regress CodeBench --score-type delta

# 6. Full report
python audit.py report -o report.json
```

## The Declared Frame

Every criteria version carries a frame:

```json
{
  "boundary": "what is inside the accounting",
  "horizon": "over what time the outcome is scored",
  "who_counts": "whose outcomes enter the total",
  "sign_source": "where 'better' was set, and by whom",
  "logic": "which formal system",
  "observer_access": "unknown | partial | verified"
}
```

`unknown` is a legal value. Omitted fields are flagged.

## Drift metrics

For each version transition, the engine computes:

| Metric | What it measures |
|---|---|
| `boundary` | Semantic drift in what is counted |
| `horizon` | Drift in time window or task depth |
| `who_counts` | Drift in whose outcomes matter |
| `sign_source` | Drift in who set "better" |
| `logic` | Change in formal system |
| `observer_access` | Change in observer verification |
| `rubric_dimensions` | Jaccard distance on dimension sets |
| `rubric_weights` | Weight vector changes |
| `exemplar_count` | Test set size changes |
| `composite` | Weighted aggregate |

## Regression

The core test:

```
Δscore = β₀ + β₁ · composite_drift + ε
```

- **β₁ > 0, significant**: Criteria inflation explains some reported improvement.
- **β₁ ≈ 0**: Improvement is orthogonal to criteria drift.
- **β₁ < 0**: Stricter criteria are masking real gains.

Run with lag to test predictive power: does drift at t predict improvement at t+k?

**The regression refuses to run unidentified.** A slope on drift alone
absorbs the capability term, so `audit.py regress` first checks for a
**bridge**: a model scored on two or more criteria versions. A model does not
change, so such a model is a frozen instrument and every bit of movement in
its score is criteria movement at fixed capability. Without one, the command
reports `identified: false` and stops. See `anchor.py`.

## File structure

```
criteria_drift_kit/
  schema.py          # Data structures and frame validation
  store.py           # SQLite persistence
  drift.py           # Drift computation engine
  regress.py         # Pure-Python OLS regression
  audit.py           # CLI entry point
  example_data/      # Sample CodeBench history
  README.md          # This file
```

Added after audit (see `AUDIT_NOTES.md`, `CLAIM_TABLE.md`):

```
  anchor.py          # anchor-version scoring, made first class
  drift_sign.py      # can the metric carry the hypothesis?
  regression_audit.py# the series, and the term that was missing
  tests/             # 34 tests, one per repaired defect
```

## Extending

- **Custom drift functions**: Subclass `DriftEngine` and override `_str_drift`, `_list_drift`, etc.
- **New frame fields**: Add to `Frame` in `schema.py` and update `DriftEngine.DEFAULT_WEIGHTS`.
- **Batch ingestion**: Write a small script that walks a directory of JSON files and calls `DriftStore.insert_criteria()`.
- **Visualization**: Export `report.json` and plot `composite_drift` vs `improvement` in any tool.

## License

CC0-1.0. Use it, break it, fix it, extend it.
