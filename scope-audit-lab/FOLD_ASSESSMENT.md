# SAL-WO5: should the lab fold into the repo's own tools?

An assessment for the operator to decide. Nothing is merged, and the
delivered lab is not edited.

## Piece-by-piece map

| lab piece | nearest repo tool | overlap | what the lab adds | what the repo tool adds |
|---|---|---|---|---|
| append-only JSONL records, `interpretation: unassigned` | `claim-record/` (7 fields, clock, derivation parents, collapse record) | same no-verdict rule | separate model / experiment / observation types | required domain of validity, derived clock, hedge screen, parents that must resolve |
| `transition_scan` (adjacent delta, strict >) | none (closest: `reasoning-gate` G-RES pairs) | — | order-preserving, keeps missing values as unresolved | — |
| `null_baseline_scan` | `null-harness/` (FP/TP bake-off with known-null and known-signal generators) | both run a gate on noise | records counts per replication | a positive control, and a grade that can say CONSTANT_FIRES |
| `threshold_sweep` | `null-harness.sweep_threshold` | both sweep | thresholds kept in the order given | minimum detectable amplitude |
| `order_permutation_probe` | `null-harness` shuffle nulls; `divergence-playground/null_ensemble.py` | shuffle nulls | per-pair appearance counts | p-values against the shuffle |
| `coupling_scan` | — | — | — (cannot separate factors, SAL_012) | — |
| `confound_record` (built here, SAL-WO2) | `claim-record` collapse/derivation fields; `uninstrumented` exclusions | alternative explanations as records | four test states | parents, clocks |
| claim registry (built here, SAL-WO4) | `model-provenance/` sessions log; `claim-record` clock | append-only, dated | two clocks per event | derived re-check dates |
| versioned schema (0.1 → 0.2 accepted) | `criteria-drift/` (versioned rulers) | versioning | old records stay valid | drift computed across versions |

## Measured, not argued (`fold_probe.py`)

The repo's `null-harness` graded the lab engine as a gate ("flags at least
one region"):

| regime | false-positive rate | true-positive rate | grade |
|---|---|---|---|
| the demo's own (uniform [0, 100], threshold 10) | 1.000 | 1.000 | CONSTANT_FIRES |
| quiet (normal sd 1, threshold 10) | 0.000 | 1.000 | OK |

So the two families compose. The repo's grader runs the lab's engine
without modification, and the result is the SAL_004 reading: the lab's
shipped null is a regime where the gate cannot discriminate.

## Options

| option | what it costs | what it keeps |
|---|---|---|
| A. keep separate | two record schemas under one rule; drift risk grows with every new type | the lab stays promotable as delivered |
| B. adapter (recommended) | a thin layer: run lab gates through `null-harness` (done, `fold_probe.py`) and export lab records into `claim-record` form | both stay intact; the lab gains a positive control and a grade, and claim-record gains the scan |
| C. merge | rewrite one schema into the other; delivered files edited or superseded | one schema |

The recommendation is B. The fit is shown, not assumed; neither delivered
artifact is edited; and the lab's real defects (SAL_004, SAL_011, SAL_012)
become visible through the repo's instruments instead of being absorbed
into a merged schema.

This is your call. Option C would edit delivered files, which this repo
does only on an explicit decision.
