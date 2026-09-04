# schema

Record shapes emitted by the four checks. Every field is present on
every record; a quantity that cannot be produced is `null`, never `0`.

## P1 — `deps.jsonl`, one line per (dependency span, class)

| field | type | note |
|---|---|---|
| `result_id` | str | input filename without extension |
| `dependency` | str | group 1 of the pattern that fired, whitespace-normalised |
| `class` | enum | `instrument` / `calibration_chain` / `method_inherited` / `material_supplied` / `prior_result` / `infrastructure` |
| `verified_in_argument` | bool | `false` unless the same sentence carries a verification verb in a verifying construction [CHOICE 2] |
| `source_span` | [int, int] | character offsets of the dependency text in the input file |
| `source_ref` | str | input filename |

`--report` adds counts by class, `dependencies_required` (records),
`dependencies_argued` (records with `verified_in_argument` true), and
`ratio_required_over_argued`, which is `null` when nothing is argued.
Every count is a floor set by the pattern set [CHOICE 1].

## P2 — `contracts.jsonl`, one line per (call site, layer) plus one per code object

| field | type | note |
|---|---|---|
| `caller` | str | enclosing function's qualified name, or `<module>` |
| `callee` | str | dotted callee expression; `<bytecode>` on compile-layer records |
| `layer` | enum | `function_call` / `allocation` / `numeric` / `transport` / `compile` |
| `contract_assumed` | str | the order's contract text for the layer |
| `verified_at_callsite` | bool | syntactic proxy [CHOICE 2]; always `false` on the compile layer |
| `line` | int | source line |
| `instructions`, `bytecode_calls` | int | compile-layer records only |

Every call site carries a `function_call` record; a callee in the
allocation, numeric or transport sets [CHOICE 1] carries a second
record. `total_callsites` counts sites, `unverified_contracts` counts
records, so the order's ratio can exceed 1.

## P3 — `consistency.json`, one object

`term`, `window`, `min_count`, `sources_total`, `sources_profiled`,
`sources_excluded` (term count below `min_count`), `term_counts` per
source, `pairs`, `consistency_observed` (mean pairwise cosine, `null`
below two profiles), and `null` — `kind` (`shuffle` / `permute`),
`seed`, `reps`, `mean`, `sd`, `max`, `frac_at_or_above_observed`,
`gap_in_sd` — or `null` when not run. `unconstructable_row` carries the
order's third-row statement.

## P4 — `coherence.jsonl`, one line per `p_contest`

`steps`, `p_contest`, `trials`, `budget`, simulated `termination_rate`,
`mean_steps_to_answer` (`null` when no answer was produced), `answers`,
`no_answer`; beside them `exact_termination_rate` and `exact_mean_steps`
from the exact position distribution over the budget, and
`expected_steps_unbounded` (`null` at `p_contest = 1`).
