# enclosure-first-residual

Enter enclosure terms FIRST, measure residual, and only then treat the
residual as a trait candidate. Trait is not excluded; it is demoted from
assumption to survivor of a control.

Order in [`WORK_ORDER.md`](WORK_ORDER.md), verbatim. Findings in
[`CLAIM_TABLE.md`](CLAIM_TABLE.md). Consumes
[`method-layer`](https://github.com/JinnZ2/method-layer) (F `branch_set`,
G `preference_free_rank`) as a declared external dependency.

```
python3 enclosure_first_residual.py demo                     the seven fixtures
python3 enclosure_first_residual.py demo --table-literal     the order's step-4 table as written
python3 enclosure_first_residual.py run PANEL.json --json --emit-branch-set F.json
python3 enclosure_first_residual.py --selftest
python3 -m unittest discover -s tests -p 'test_*.py'
```

## The shape

```
panel of person-windows
        |
        v
  schema gate ---- term without operationalization ----> BLOCKED(unoperationalized_term)
        |          term from the human label set   ----> BLOCKED (closed node)
        v
  envelope ------- within change CHOSEN by person  ----> OUT_OF_ENVELOPE
        |          (chosen / unknown pairs excluded; exogenous pairs enter)
        v
  NULL FIRST ----- enclosure shuffled within population, band PRINTED
        |          observed between residual inside band -> UNKNOWN_measurable
        v
  between arm      behavior ~ effective_exits + reversible_count    -> residual_between
        |
        v
  within arm       delta behavior ~ delta enclosure, same person,
        |          exogenous, |delta effective_exits| >= 1            -> residual_within
        |          fewer than 3 such pairs                             -> BLOCKED(no_within_person_windows)
        v
  compare          ratio + CI + the order's table cell, printed every run
        |
        v
  return           ENCLOSURE_DOMINANT | TRAIT_RESIDUAL | VARIABLE_UNIDENT (confound)
                   | UNKNOWN_measurable | BLOCKED | OUT_OF_ENVELOPE      -- peer classes
```

`residual = SSE / SST` in both arms: the fraction of that arm's own
behavior variance left after its enclosure regressors. 1.0 is "enclosure
explains nothing here".

## The counterexample the claim table is built on

Fixture F1 is enclosure-only: `behavior = 10 - effective_exits + noise`,
no trait, no selection, forty persons, two exogenous windows each. Under
the order's step-4 table as written it lands in the **confound** cell.

```
between arm  n=80  residual 0.2015  CI [0.1415, 0.2839]
within arm   n=40  residual 0.4291  CI [0.2460, 0.5855]   null band [0.8184, 0.9982]
ratio within/between 2.1297  CI [1.1888, 3.4953]           table cell: >
```

Two things push the within fraction up with nothing wrong in the data.
Differencing doubles the noise variance. Enclosure within a person is
autocorrelated, so the differenced enclosure variance is less than
double. And a stable trait, when present, inflates only the between
residual, so adding one always *lowers* the ratio. The table's cells are
therefore ordered backwards on the ratio axis: no normalisation puts
enclosure-only in `<<` and trait-plus-enclosure in `~` at the same time.
`CLAIM_TABLE.md` `EFR_003` and `EFR_004` carry the algebra and the
fixture numbers.

So the default return is a **corrected reading of the same two arms**,
and the literal table stays one flag away (`--table-literal`) with its
cell printed on every run either way:

1. Does behavior *move* with enclosure within a person? The within
   residual against its own permutation null. Inside the null band means
   the between association was not reproduced within person: confound.
2. If it moves, is anything *person-stable* left over? The share of the
   between residual that sits between persons, against a null from
   shuffling person labels. Above null: `TRAIT_RESIDUAL`. Not above:
   `ENCLOSURE_DOMINANT`.

## Where the fixtures land

| fixture | generative model | default return | literal table |
|---|---|---|---|
| F1 enclosure only | slope -1, no trait | `ENCLOSURE_DOMINANT(0.571, [0.414, 0.754])` | `>` confound |
| F2 trait only | trait sd 2, slope 0 | `UNKNOWN_measurable` (null gate) | same |
| F3 trait + enclosure | trait sd 2, slope -1 | `TRAIT_RESIDUAL(0.477, [0.276, 0.669])` | `~` `TRAIT_RESIDUAL(0.558)` |
| F4 selection into windows | trait sd 2, slope 0, exits sorted by trait | `VARIABLE_UNIDENT` (confound) | `>` confound |
| F5 chosen change | as F1, `change_origin: chosen` | `OUT_OF_ENVELOPE` | same |
| F6 no operationalization | as F1, empty `operationalizations` | `BLOCKED(unoperationalized_term)` | same |
| F7 single windows | as F1, one window per person | `BLOCKED(no_within_person_windows)` | same |

The fixtures are generated in code from explicit models with fixed seeds;
`samples/` holds the demo output, the literal-table output, two panels
written out as JSON, the selftest line, and the branch set F1 emits
(`trait_plain` eliminated by that run).

## Panel schema

```json
{
  "population": "benefit-cliff-2024",
  "operationalizations": {
    "latency_to_approach_novel": "seconds from onset of a novel stimulus to first approach within one body length"
  },
  "windows": [
    {"person_id": "p01", "t0": "2024-01", "t1": "2024-03",
     "change_origin": "baseline",
     "enclosure": {"option_set_size": 3,
                   "exit_cost": [0.2, 0.9, 1.4],
                   "reachability": [1, 1, 0],
                   "reversibility": [1, 0, 0]},
     "behavior": {"latency_to_approach_novel": 12.5}},
    {"person_id": "p01", "t0": "2024-04", "t1": "2024-06",
     "change_origin": "exogenous", "enclosure": {"...": "..."}, "behavior": {"...": "..."}}
  ]
}
```

- `exit_cost` is a fraction of resources **available**, not of total.
- `reachability` is 1 when the exit is reachable without first exiting
  something else.
- `effective_exits = count(reachability == 1 AND exit_cost <= 1.0)`
  carries the hypothesis. `option_set_size` is the nominal count and
  overstates; its residual is printed beside the decision model's on
  every run (`EFR_002`).
- `change_origin` on a window names how the enclosure change *into* that
  window happened: `baseline` (first window), `exogenous`, `chosen`,
  `unknown`. Only `exogenous` pairs enter the within arm.
- Behavior terms are the four graded forms from the order. A term
  outside them, or from the human label set, or without a non-empty
  operationalization string, is `BLOCKED`, never estimated.

## method-layer

Located via `METHOD_LAYER_PATH`, else a sibling `method-layer/` or
`jinnz2/method-layer/` checkout up to three directories up. Set
`METHOD_LAYER_PATH=none` to run as if it were absent.

- Present: returns are built as G `CriterionResult` objects, so a scored
  kind without a fraction or a `BLOCKED` without a named blocker fails at
  construction. The branch set is built through F's `BranchSet` and
  round-tripped through its loader before it is written.
- Absent: the same enum values are mirrored locally, the record says
  `method-layer=absent`, and nothing is estimated differently. The
  selftest passes identically in both modes (`EFR_009`).

## Declared choices

Printed with every run.

| choice | value | what it fixes |
|---|---|---|
| `DELTA_THRESHOLD` | 1 | a within pair needs `|delta effective_exits|` at least this |
| `NULL_DRAWS`, `BOOT_DRAWS` | 300, 300 | permutation and bootstrap draws |
| `DOMINANT_RATIO`, `CONFOUND_RATIO` | 0.5, 1.25 | the order's `<<`, `~`, `>` cells on the ratio |
| `NULL_BAND` | [0.025, 0.975] | central 95% of null draws; observed is inside when at or above the lower edge |
| `MIN_WITHIN_PAIRS` | 3 | fewest exogenous pairs the discriminator will fit |
| `CORRECTED_READING` | on | off with `--table-literal` |

CC0. stdlib only. Parses under Python 3.9. ASCII only in the source.
