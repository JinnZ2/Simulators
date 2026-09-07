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

B, model `{recall 0.9, fab_on_recall 0.05, collision 0}` identical in every corner, contract
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

## WORK_ORDER_02 (verbatim in `WORK_ORDER_02.md`)

**Task 1, dense multi-seed** (`multiseed.py`, 30 seeds, model exactly as
seed 1). Δ = true(low) − true(high) per seed:

```
row     independent mean    sd      95% CI              seed-1 Δ   2sd band   inside
dense   +0.0016            0.0212  [-0.0060, +0.0092]   +0.020     0.042      yes
sparse  +0.0009            0.0115  [-0.0032, +0.0051]   +0.002     0.023      yes
paired (one model stream, separate render stream): Δ = 0.0000 on every seed, both rows
```

Verdict: Δ ~ 0 within noise, the factorization holds as written. The
seed-1 dense Δ was one standard deviation of a 500-item binomial and was
never anomalous; the sparse band is narrower because seven of ten items
there are fabricated deterministically and only three vary. The paired
design shows the stronger thing: rendering cannot reach the true rate
by construction. Closes with no cross-term.

**Task 2, collision cell.** Does B emit collisions? Yes, accidentally
and only under `jaccard`: at collision 0, seed 1, fabricated titles
built from the shared word pool matched a real entry 3 / 0 / 2 / 1 times
across the corners, which is the one seed-1 deflation (dense/high
`jaccard` −0.002). No deliberate cell existed. Added `collision` as a
model parameter with `DISTRACTORS` real non-answer items; at 0 seed 1
reproduces byte for byte. At collision 0.3, measured − true SIGNED:

```
corner        exact    norm     jaccard   edit     substring
sparse/low    -0.036   -0.120   -0.252    -0.212   -0.208
sparse/high   -0.234   -0.234   -0.262    -0.236   -0.234
dense/low     +0.624   +0.394   -0.032    +0.066   +0.054
dense/high    -0.048   -0.048   -0.074    -0.050   -0.048
```

The matcher hides fabrication as well as inventing it, and in the
low-canonicality corners the two matcher effects offset: dense/low under
`jaccard` reads −0.032 while hiding fabrications AND missing true items.
`fabrications_hidden_by_matcher` and `true_items_missed_by_matcher` are
printed per cell so the offset is visible; the signed scalar alone is
not. The earlier B under-stated matcher damage.

**Task 3, canonical self-test.** `confound_probe.py` now runs a
pre-flight before any claim: the canonical subset (titles that
self-match uniquely under the loosest matcher) is scored under every
matcher and all have to agree to 3 decimals at 0.000. On disagreement
the matcher set is not sound and the run ABORTS (exit 3) with no catalog claim.
Pinned by injecting a matcher that misses everything. This diagnoses
the instrument without a ground-truth catalog and validates nothing
about the catalog; RC_008 stands.

**Task 4, fixture promotion.** The A fixture is named
`kill_rule_boundary` (`samples/kill_rule_boundary.sample.txt`): strict
form KILL true, mean form false, on one input. Ranking validity there
depends on the rule chosen. Both forms stay printed; the disagreement
is a result.

Not in this order: F repository creation, G `preference_free_rank.py`
(specced, own repo, not started), the protocol-over-information survey
(verbatim, unbuilt).
