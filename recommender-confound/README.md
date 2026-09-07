# recommender-confound

CC0. Stdlib only. Phone-buildable. Built to `WORK_ORDER.md` (verbatim).

The origin is a published recommender audit whose hallucination rate
runs from 0.6% to 61% by catalog while verbalized confidence stays
about constant, and whose reported number moves 10x with the choice of
string matcher. The claim under test: the reported number is
`g(model) x h(catalog) x m(matcher)`, attributed entirely to `g`.

Five instruments, one shared module. Every fixture here is constructed
and says so; nothing is a statement about any published model or
catalog until someone runs A on their own.

| file | what it does | run |
|---|---|---|
| `matchers.py` | six string matchers; every produced string is MATCH / MISS / AMBIGUOUS, ambiguity reported apart | `--selftest` |
| `confound_probe.py` (A) | audit tool for others' catalogs: `halluc[model][matcher]`, matcher spread vs between-model spread, the KILL rule, canonicality, sparsity, separability of h from m | `CATALOG OUTPUTS [--matchers ...]` |
| `synthetic_catalog.py` (B) | null construction: 2x2 density x canonicality, model held constant, measured vs true fabrication rate per corner and matcher | `--seed N` |
| `abstention_channel.py` (C) | contract v1 vs v2, precision not count-completion; `sim` runs the same model under both | `sim --seed N` / `score ...` |
| `shared_generator_test.py` (D) | one generator or several: base vs tuned per family; a decoupled case is a result, never null | `MODELS.jsonl` |
| `slot_map.py` (E) | reader-in-frame: q1 reader presence alone, q2 asserted premise moves retrieval or only agreement | `CATALOG RESPONSES` |

## What the sims return on the constructed model (seed 1)

B, model `{recall 0.9, fab_on_recall 0.05}` identical in every corner, contract
v1 (fill to N):

```
corner        true_fab   exact   norm   jaccard   edit
sparse/low     0.746     0.948   0.868   0.754   0.772
sparse/high    0.744     0.744   0.744   0.744   0.744
dense/low      0.118     0.830   0.618   0.138   0.246
dense/high     0.138     0.138   0.138   0.136   0.138
```

The measured number runs 0.138 to 0.948 under `exact` with the model
untouched. The two moves are separable in the table: sparse vs dense is
the CONTRACT (a deficit filled by fabrication), low vs high canonicality
is the MATCHER (true items rendered non-canonically and scored as
misses). At high canonicality every matcher recovers the true rate.

C, the same model under v1 then v2 on the sparse corner: hallucination
0.738 -> 0.063, precision under v2 0.937, abstention correct on 50 of
50 queries with supply below N. The model did not change.

## Reading rules built in

- A's KILL: if the mean spread across matchers exceeds the mean spread
  across models, the model ranking is void. Ties are recorded as ties,
  and a tie under one matcher against an ordering under another counts
  as two distinct rankings.
- A's separability is an additive two-way fit on
  `halluc[category][matcher]`; the interaction share and its threshold
  are printed.
- D never labels a decoupled pair null: `corr ~ 0` is reported as
  slot-specific deficit handlers, the higher-information reading.
- Every threshold is an argument and is printed with the result.

## Not built

The queued protocol-over-information survey is not specced and is not
built; its signature is in `WORK_ORDER.md` as delivered. F
(`branch_set.py`) is its own folder, `../branch-set/`, marked
`[OWN REPO]` in the order and left promotable.
