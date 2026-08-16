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
