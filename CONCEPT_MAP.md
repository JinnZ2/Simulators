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
- decided by: pending: a definition or a path from JinnZ2
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
| candidate | `Simulators:forest-model-ledger/CLAUDE.md` | JinnZ2 + Claude (METHOD BRIEF) | the rule as text |
| copy | `Simulators:forest-model-ledger/ledger/anchors/ANCHOR_run9.yaml` | Claude Code (commit trailer) | one anchor record |
| candidate | `Simulators:relational-playground/playground/anchor.py` | Claude Code (commit trailer) |  |
| candidate | `study-aperture@origin/main:experimental/playground/reference/anchor.py` | Perplexity (commit trailer) |  |
| copy | `study-aperture@origin/main:experimental/playground/reference/return_test.py` | Perplexity (commit trailer) |  |
| copy | `Simulators@origin/archive/anchor-run9:forest-model-ledger/ledger/anchors/ANCHOR_run9.yaml` | Claude Code (commit trailer) | archive branch standing in for the anchor tag; pinned |

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
- decided by: pending: expansion and a path from JinnZ2
- searched: 2026-11-11: GitHub code search over user:JinnZ2 (default branches only), 0 hits; grep of local checkouts of Simulators (this branch), study-aperture, method-layer, TAF, decision-aperture, 0 hits

## correctness gradients

- home: NOT_LOCATED
- status: term not found
- decided by: pending: a definition or a path from JinnZ2
- searched: 2026-11-11: GitHub code search over user:JinnZ2 (default branches only), 0 hits; grep of local checkouts of Simulators (this branch), study-aperture, method-layer, TAF, decision-aperture, 0 hits

## stated_purpose / scope_valid (law purpose and scope against first principle intent)

- home: CANDIDATE
- status: one concept under two names; the Simulators card imports the TAF module (law-audit-card/card.py names regulatory_scope_audit) and reads undeclared intent as VOID where TAF reads it as applying
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:law-audit-card/card.py` | Claude Code (commit trailer) | imports the TAF module; undeclared intent -> VOID |
| candidate | `thermodynamic-accountability-framework@origin/main:core/regulatory_scope_audit.py` | not recorded (add commit b15e629 has no trailer; git author Claude) | undeclared intent -> intent applies (TAF CLAUDE.md note 2026-11-10) |

## system continuity vs configuration continuity

- home: CANDIDATE
- status: two independent builds (crossrun row, location on both sides)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/reference/continuity.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) |  |
| candidate | `Simulators:relational-playground/playground/continuity.py` | Claude Code (commit trailer) |  |

## observer declared before comparison

- home: CANDIDATE
- status: two independent builds (crossrun row, location on both sides)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/applicability/mapping.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) |  |
| candidate | `Simulators:relational-playground/playground/controls.py` | Claude Code (commit trailer) |  |

## observer regime partition (names differ: PASSIVE vs REACTIVITY; not merged)

- home: CANDIDATE
- status: two independent builds; the names differ (PASSIVE vs REACTIVITY) and are not merged
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/observation/__init__.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) |  |
| candidate | `Simulators:relational-playground/playground/controls.py` | Claude Code (commit trailer) |  |

## no universal ranking

- home: CANDIDATE
- status: two independent builds (crossrun row, location on both sides)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/applicability/mapping.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) |  |
| candidate | `Simulators:relational-playground/playground/experiments/comparison.py` | Claude Code (commit trailer) |  |

## applicability / domain of validity

- home: CANDIDATE
- status: two independent builds (crossrun row, location on both sides)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/applicability/mapping.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) |  |
| candidate | `Simulators:relational-playground/playground/analysis/applicability.py` | Claude Code (commit trailer) |  |

## value / condition basis vocabulary

- home: CANDIDATE
- status: two independent builds (crossrun row, location on both sides)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `study-aperture@origin/main:experimental/playground/applicability/mapping.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) |  |
| candidate | `Simulators:relational-playground/playground/uncertainty.py` | Claude Code (commit trailer) |  |

## READING_PROTOCOL (how a folder is to be read)

- home: CANDIDATE
- status: three files of one name; the study-aperture and TAF copies have the same blob (601fdd196ceb), the Simulators file differs (ae6dd1146a38)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:READING_PROTOCOL.md` | not recorded (add commit e9594f8 has no trailer; git author Claude) | differs from the other two |
| candidate | `study-aperture@origin/main:READING_PROTOCOL.md` | Claude Code (commit trailer) | same blob as the TAF copy |
| candidate | `thermodynamic-accountability-framework@origin/main:READING_PROTOCOL.md` | Claude Code (commit trailer) | same blob as the study-aperture copy |

## driver-hours evidence register

- home: CANDIDATE
- status: one file in two places, drifted (88 diff lines at the pinned commits)
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:automation-gap/driver_hours_evidence_register.py` | Claude Code (commit trailer) |  |
| candidate | `thermodynamic-accountability-framework@origin/main:labor_thermodynamics/driver_hours_evidence_register.py` | Claude Code (commit trailer) |  |

## conditional_claims (vendored tool)

- home: CANONICAL
- status: vendored copy, same blob at the pinned commits; can drift
- decided by: study-aperture vendored/PROVENANCE.md and vendored/SHA256SUMS (vendored from Simulators)

| role | where | builder | note |
|---|---|---|---|
| canonical | `Simulators:tools/conditional_claims.py` | Claude Code (commit trailer) | upstream |
| copy | `study-aperture@origin/main:vendored/conditional_claims.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) | vendored copy; do-not-modify rule in study-aperture CLAUDE.md |

## false_agree (vendored tool)

- home: CANONICAL
- status: vendored copy, same blob at the pinned commits; can drift
- decided by: study-aperture vendored/PROVENANCE.md and vendored/SHA256SUMS (vendored from Simulators)

| role | where | builder | note |
|---|---|---|---|
| canonical | `Simulators:tools/false_agree.py` | Claude Code (commit trailer) | upstream |
| copy | `study-aperture@origin/main:vendored/false_agree.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) | vendored copy; do-not-modify rule in study-aperture CLAUDE.md |

## provenance_graph (vendored tool)

- home: CANONICAL
- status: vendored copy, same blob at the pinned commits; can drift
- decided by: study-aperture vendored/PROVENANCE.md and vendored/SHA256SUMS (vendored from Simulators)

| role | where | builder | note |
|---|---|---|---|
| canonical | `Simulators:tools/provenance_graph.py` | Claude Code (commit trailer) | upstream |
| copy | `study-aperture@origin/main:vendored/provenance_graph.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) | vendored copy; do-not-modify rule in study-aperture CLAUDE.md |

## measurand declaration (measurand vs indication / declared identity)

- home: CANDIDATE
- status: candidate match only: decomposition (instrument-epistemology) vs declared identity on linked runs (playground); same word, possibly two concepts, not decided
- decided by: pending cross-run

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:instrument-epistemology/src/instrum/measurand.py` | Claude Code (commit trailer) | measurand vs indication decomposition |
| candidate | `study-aperture@origin/main:experimental/playground/equations/measurand.py` | not recorded (add commit c26fbd2 has no trailer; git author JinnZ2) | declared measurand identity on linked runs |

## thermodynamic audit inside an economic sim

- home: SINGLE
- status: single home: a stand-in in Simulators; earth_economic_sim.py says 'In reality, this would import modules from TAF' and no TAF file is declared as its counterpart
- decided by: evidence: the file's own line; no cross-run needed

| role | where | builder | note |
|---|---|---|---|
| candidate | `Simulators:earth_economics/earth_economic_sim.py` | not recorded (add commit 7632c2a has no trailer; git author JinnZ2) | stand-in auditor inside the sim |
| nearest | `thermodynamic-accountability-framework@origin/main:calibration/unified_audit.py` | not recorded (add commit c81a758 has no trailer; git author Claude) | nearest auditor module read; not a declared counterpart, not shown to be the same concept |
