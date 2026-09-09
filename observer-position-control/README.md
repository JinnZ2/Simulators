# observer-position-control

CC0. Stdlib only. Phone-buildable. Built to `WORK_ORDER.md` (item J,
verbatim). Method layer: is the maladaptive / adaptive label set by the
behavior, or by whether the describer is inside the population
described? Label extraction over a published corpus, no new observation.
The corpus is the data; blind coding is the only labor, and it happens
outside this script.

```
python3 observer_position_control.py SOURCES.jsonl BEHAVIOR.jsonl [--min-cell 5] [--v 0.3] [--json]
python3 observer_position_control.py --selftest
```

## What is enforced, not instructed

- **Null (a), the main null, is blind by file boundary.** The behavior
  coding arrives in its own file carrying only `source_id`, the three
  pattern components and `intensity`. Any other field in it is refused,
  because a coder who could see position or label was not blind.
- **The held-fixed pattern is a filter, not a label.** Only sources
  whose blind coding shows all three components enter the contingency.
  If the components' distribution differs across positions above the
  threshold, the verdict is `BEHAVIOR_DIFFERS` and J returns nothing
  further, as the order requires.
- **The prediction is in the code before any row is read** and is
  scored against the modal label per position.
- **Nulls (b), (c), (d)** stratify by decade, literature type and
  intensity band; each reports per-stratum Cramér's V, the n-weighted
  pooled V, and how many strata were evaluable at `--min-cell`.
- **Verdict is an enum**: `OBSERVER_INDEXED` / `BEHAVIOR_DIFFERS` /
  `EXPLAINED_BY_ERA` / `EXPLAINED_BY_LITERATURE` /
  `EXPLAINED_BY_SEVERITY` / `NO_ASSOCIATION` / `UNKNOWN_measurable`.
  Thresholds are arguments and are printed.

## Two readings the fixtures forced

- A corpus where the label does not vary reads as `NO_ASSOCIATION`
  (V = 0), not as "not computable": a constant label cannot track
  position. A corpus with one position only stays not computable.
- When position is perfectly confounded with decade, no stratum spans
  two positions and the verdict is `UNKNOWN_measurable`, with the reason
  naming era. A perfect confound cannot be separated from the effect;
  `EXPLAINED_BY_ERA` fires only when strata that span positions show
  the association collapsing within them.

## Samples

`samples/` holds three constructed corpora (`indexed`, `differs`, `era`)
with their outputs. They are constructed and say so; nothing here is a
statement about any literature until a blind-coded corpus is run.
