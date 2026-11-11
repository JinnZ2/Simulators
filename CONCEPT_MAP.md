# CONCEPT_MAP

Generated from `concept_map.json` by `check_concept_map.py --write`. Edit the JSON, not this file.
One block per concept. No code is moved. As of 2026-11-11.

home: CANONICAL (decided), CANDIDATE (two or more homes, undecided), SINGLE (one copy), NOT_LOCATED.

## playground (equation-substitution laboratory)

- home: CANDIDATE
- status: two independent builds; neither on a main branch in full (Simulators copy is on a draft branch)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:relational-playground/` | Claude Code, to a GPT spec (SPEC_GPT.md) | draft PR 257 |
| candidate | `study-aperture@origin/main:experimental/playground/` | Perplexity (commit trailer) | 18 commits; organised around determinations, equation families deferred |

## known-answer / null harness

- home: CANDIDATE
- status: three implementations; the relational-playground gate restates the rule in stdlib
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:tools/known_answer.py` | Claude Code (commit trailer) | repo registry; refuses a metric with no cases |
| candidate | `Simulators:null-harness/null_harness.py` | not recorded | needs numpy |
| candidate | `study-aperture@origin/main:experimental/playground/validation/known_answer.py` | Perplexity (commit trailer) |  |
| candidate | `study-aperture@origin/main:experimental/playground/validation/null_harness.py` | Perplexity (commit trailer) |  |
| copy | `Simulators:relational-playground/playground/known_answer_gate.py` | Claude Code (commit trailer) | FP 0 / TP 1 gate per model |

## UNKNOWN expiry

- home: CANDIDATE
- status: three builds; TAF register holds real slots, the other two are mechanisms
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `thermodynamic-accountability-framework@origin/main:calibration/expiry_register.py` | Claude Code (commit trailer) | register on main |
| copy | `thermodynamic-accountability-framework@origin/main:docs/expiry_register.json` | Claude Code | stage-1 register data |
| candidate | `study-aperture@origin/main:experimental/playground/lifecycle/unknown_expiry.py` | Perplexity (commit trailer) |  |
| candidate | `Simulators:relational-playground/playground/uncertainty.py` | Claude Code (commit trailer) | expiry on every UNKNOWN / NOT MEASURED |

## scoped absence (ABSENT_AT_SENSITIVITY)

- home: CANDIDATE
- status: defined in TAF glossary; built in two playgrounds
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/detection/scoped_absence.py` | Perplexity (commit trailer) |  |
| candidate | `Simulators:relational-playground/playground/uncertainty.py` | Claude Code (commit trailer) | same file as expiry |
| copy | `thermodynamic-accountability-framework@origin/main:docs/glossary.md` | Claude Code | status definition only |

## failure axes (PHYSICAL / INSTRUMENT / DETERMINATION)

- home: SINGLE
- status: built; no counterpart in Simulators
- decided by: single copy

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/failures.py` | Perplexity (commit trailer) |  |

## coincidence card

- home: CANDIDATE
- status: C1-C6 tests in one file, the card record in another; a third calls both
- decided by: pending cross-run
- note: divergence-playground/coincidence.py on this branch was taken from claude/healing-folder-additions-u5aojl, which is not on main

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:divergence-playground/coincidence.py` | Claude Code (commit trailer) | C1-C6 elicitation tests |
| candidate | `Simulators:forest-model-ledger/ledger/toolkit/coincidence_card.py` | Claude Code (commit trailer) | card record; draft PR 255 |
| copy | `Simulators:relational-playground/playground/analysis/coincidence.py` | Claude Code (commit trailer) | wires the two |

## assessor reliability

- home: SINGLE
- status: built, 114 tests pass, not merged
- decided by: single copy
- note: Simulators assessor-coupling/ is a different concept (independence of assessor from assessed)

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/experimental/assessor-reliability-pilot:experimental/assessor_reliability/` | Manus (commit trailer) | one commit off main |

## attribution directionality

- home: NOT_LOCATED
- status: no file carries the term
- decided by: pending: a definition or a path from Kavik
- searched: 2026-11-11: GitHub code search over user:JinnZ2 (default branches only), 0 hits; grep of local checkouts of Simulators (this branch), study-aperture, method-layer, TAF, decision-aperture, 0 hits

| role | where | builder | note |
|---|---|---|---|
| nearest | `thermodynamic-accountability-framework@origin/main:judgment_registry/experiments.py` | Claude Code | ATTRIBUTION_ORDER flag; nearest, not shown to be the same concept |
| nearest | `Simulators:measurand-partition/common.py` | not recorded | attribution() UNPARTITIONED; nearest, not shown to be the same concept |

## L0 gate (budget closure)

- home: CANDIDATE
- status: three builds
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:forest-model-ledger/ledger/toolkit/budget_closure.py` | Claude Code (commit trailer) | needs numpy; sha-pinned |
| candidate | `Simulators:relational-playground/playground/l0.py` | Claude Code (commit trailer) | stdlib; LIVE / VOID budgets |
| candidate | `study-aperture@origin/main:experimental/playground/gates/l0_closure.py` | Perplexity (commit trailer) |  |

## anchor / return

- home: CANDIDATE
- status: rule text in the forest METHOD BRIEF; two code builds
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:forest-model-ledger/CLAUDE.md` | Kavik + Claude (METHOD BRIEF) | the rule as text |
| copy | `Simulators:forest-model-ledger/ledger/anchors/ANCHOR_run9.yaml` | Claude Code (commit trailer) | one anchor record |
| candidate | `Simulators:relational-playground/playground/anchor.py` | Claude Code (commit trailer) |  |
| candidate | `study-aperture@origin/main:experimental/playground/reference/anchor.py` | Perplexity (commit trailer) |  |
| copy | `study-aperture@origin/main:experimental/playground/reference/return_test.py` | Perplexity (commit trailer) |  |

## percolation

- home: CANDIDATE
- status: two equation-family builds plus the original run code
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:relational-playground/playground/equations/percolation.py` | Claude Code (commit trailer) | with spotting |
| candidate | `study-aperture@origin/main:experimental/playground/equations/percolation.py` | Perplexity (commit trailer) | finite percolation |
| copy | `Simulators:forest-model-ledger/runs/run_7.py` | chat-side original, filed verbatim | ODE vs grid run |
| nearest | `Simulators:energy/exploration_layers/percolation_lens.py` | not recorded | graph-threshold lens, a different use |

## branching

- home: CANDIDATE
- status: two builds
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:relational-playground/playground/equations/branching.py` | Claude Code (commit trailer) | with die-out |
| copy | `Simulators:relational-playground/playground/equations/branching_math.py` | Claude Code (commit trailer) | extinction probability |
| candidate | `study-aperture@origin/main:experimental/playground/equations/branching.py` | Perplexity (commit trailer) | finite branching |

## ROTL

- home: NOT_LOCATED
- status: term not found; expansion not known to this session
- decided by: pending: expansion and a path from Kavik
- searched: 2026-11-11: GitHub code search over user:JinnZ2 (default branches only), 0 hits; grep of local checkouts of Simulators (this branch), study-aperture, method-layer, TAF, decision-aperture, 0 hits

## correctness gradients

- home: NOT_LOCATED
- status: term not found
- decided by: pending: a definition or a path from Kavik
- searched: 2026-11-11: GitHub code search over user:JinnZ2 (default branches only), 0 hits; grep of local checkouts of Simulators (this branch), study-aperture, method-layer, TAF, decision-aperture, 0 hits
