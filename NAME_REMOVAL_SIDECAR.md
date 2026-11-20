# Name removal sidecar

Status: awaiting owner decision A. Nothing in these files has been changed.

Scope: files on each repository's default branch (and formula-audit `main`) at 2026-11-20 04:12Z that contain the personal name the
header removals replaced (case-insensitive whole-word match on the three strings in the removal commits' removed lines). The name
itself is not written here. ORDINARY files are handled by draft PRs; these two classes are held for a decision because changing
them changes a pinned hash or a quoted record.

Classes:

- PINNED: the file's sha256 or git blob id appears (as a hex prefix of 12+ characters) in another file in any of the 105 clones. Changing
  the file breaks that pin. `pinned by` gives one citing file.
- QUOTE-OR-HISTORY: a history / verbatim / relay / source / legacy / archive path, or a header that says verbatim or as received.

Counts: PINNED 68 files (150 lines), QUOTE-OR-HISTORY 61 files (118 lines).

## PINNED

| repo | path | lines | pinned by |
|---|---|---|---|
| JinnZ2 | `manifold/EXPERIMENT_REGISTER.md` | 5 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| JinnZ2 | `manifold/OPEN_E9_walking_criterion.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `AMOC/divergence.py` | 1 | `method-layer:reasoning-layer/READ_FIRST.md` |
| Simulators | `blind-reader-void12/reader_packet/sources/Simulators/playground-crossrun/COMBINED_SPEC.lines_1-390.md` | 2 | `Simulators:blind-reader-void12/PREREG.md` |
| Simulators | `blind-reader-void12/reader_packet/sources/thermodynamic-accountability-framework/calibration/unified_audit.py` | 2 | `Simulators:MULTI_HOME_REGISTER.json` |
| Simulators | `blind-reader-void12/reader_packet_v2/sources/Simulators/playground-crossrun/COMBINED_SPEC.lines_1-390.md` | 2 | `Simulators:blind-reader-void12/PREREG.md` |
| Simulators | `blind-reader-void12/reader_packet_v2/sources/thermodynamic-accountability-framework/calibration/unified_audit.py` | 2 | `Simulators:MULTI_HOME_REGISTER.json` |
| Simulators | `blind-reader-void12/studies/EMBEDDED_AUDIT_TESTS.md` | 3 | `Simulators:blind-reader-void12/studies/requests/AUDIT_EMBEDDED_TESTS_2026-11-19_DRAFT.md` |
| Simulators | `claim-audits/claim_audit_visibility.py` | 3 | `method-layer:reasoning-layer/READ_FIRST.md` |
| Simulators | `claim-audits/samples/claim_audit_visibility.sample.txt` | 2 | `method-layer:reasoning-layer/READ_FIRST.md` |
| Simulators | `coinage-log/COINAGE_LOG.md` | 12 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `coinage-log/vocabulary-gap-slots.md` | 6 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `docs/FOLDER_NOTES.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `emergence-stability-simulator/CITATION.cff` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `falsifier-survey/cell_records.csv` | 3 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `falsifier-survey/cell_records.jsonl` | 3 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `falsifier-survey/survey/batches/batch_0.jsonl` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `falsifier-survey/survey/batches/batch_0_hits.jsonl` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `falsifier-survey/survey/batches/batch_5.jsonl` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `falsifier-survey/survey/raw_hits.jsonl` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `fold-matrix/CLAIM_TABLE.md` | 4 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `fold-matrix/fold_register.py` | 7 | `method-layer:reasoning-layer/READ_FIRST.md` |
| Simulators | `fold-matrix/register_audit.py` | 4 | `method-layer:reasoning-layer/READ_FIRST.md` |
| Simulators | `fold-matrix/samples/register_audit.sample.txt` | 3 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `forest-model-ledger/runs/run_6.py` | 1 | `Simulators:forest-model-ledger/runs/run_6.md` |
| Simulators | `forest-model-ledger/runs/run_7.py` | 1 | `Simulators:forest-model-ledger/runs/run_7.md` |
| Simulators | `forest-model-ledger/runs/run_8.py` | 1 | `Simulators:forest-model-ledger/runs/run_8.md` |
| Simulators | `fragility-cascade/EXPERIMENT_register.md` | 5 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `fragility-cascade/OPEN_E9_walking_criterion.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `habitat-lag-dependency/SOURCE_DROP.md` | 3 | `Simulators:habitat-lag-dependency/check.py` |
| Simulators | `notes/markers/HELD_2026_08_31.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `notes/queue/DISPATCH_M0_SCOPE_2026_10_04.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `publication-loop-work-orders/WORK_ORDER_14.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `recommender-confound/WORK_ORDER_02.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `reporting-chain-loss/WORK_ORDER.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `research-stability-audit/CITATION.cff` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/AMENDMENT_A1_2026-09-28_settlement-vs-gate.md` | 3 | `Simulators:route-independence/repo_span_store.json` |
| Simulators | `route-independence/AMENDMENT_A2_2026-09-28_gate-state.md` | 1 | `Simulators:route-independence/repo_span_store.json` |
| Simulators | `route-independence/AMENDMENT_A3_2026-09-28_thermal.md` | 1 | `Simulators:route-independence/repo_span_store.json` |
| Simulators | `route-independence/AMENDMENT_A4_2026-09-28_route-chains.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/AMENDMENT_A5_2026-09-28_terminus-diversity.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/AMENDMENT_A6_2026-09-28_eligibility-recognition.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/WORK_ORDER_A6.2_2026-09-29_physical-sourcing.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/chains_a4.py` | 1 | `Simulators:route-independence/followup_a63.py` |
| Simulators | `route-independence/samples/thermal_gates.sample.txt` | 6 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/test_thermal_gates.py` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `route-independence/thermal_gates.py` | 1 | `Simulators:route-independence/followup_a63.py` |
| Simulators | `tools/natural_two_senses.md` | 5 | `method-layer:reasoning-layer/READ_FIRST.md` |
| Simulators | `tools/tool_inventory.json` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/AUDIT_NOTES.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/CLAIM_TABLE.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/OPEN_QUESTIONS.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/WORK_ORDER_03.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/cases/013compensationloadunattributed.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/cases/014offloadingevolutionaryframing.md` | 3 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/cases/020attributedagencyarrangement.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/cases/021sensesubstitutionundeclaredaxis.md` | 2 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/cases/023borrowedselectionvocabulary.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/playground/README.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/samples/case_013_audit.sample.txt` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/samples/case_021_audit.sample.txt` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/samples/playground_audit.sample.txt` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/specimens/INSTANCE_LOG_INDEX.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| Simulators | `uninstrumented/specimens/INSTANCE_LOG_SURVEY.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| chain-position-detectability | `work-orders/WO-5-hop-distance-and-pre-entry-loss.md` | 1 | `method-layer:reasoning-layer/layer3/INVENTORY_2026-10-14.txt` |
| method-layer | `tools/natural_two_senses.md` | 5 | `method-layer:reasoning-layer/READ_FIRST.md` |
| thermodynamic-accountability-framework | `calibration/unified_audit.py` | 2 | `Simulators:MULTI_HOME_REGISTER.json` |

## QUOTE-OR-HISTORY

| repo | path | lines | rule |
|---|---|---|---|
| AI-Consciousness-Sensors | `LICENSE_HISTORY.md` | 2 | path |
| JinnZ2 | `legacy/political_financial_vectors_v5.py` | 1 | path |
| JinnZ2 | `legacy/political_financial_vectors_v8.py` | 1 | path |
| JinnZ2 | `legacy/political_financial_vectors_v9.py` | 7 | path |
| JinnZ2 | `projects/symbolic-ai/relational-cognition/cognition_markers.py` | 3 | header says verbatim/as received |
| Mathematic-economics | `automation_metrology/README.md` | 1 | header says verbatim/as received |
| Mathematic-economics | `automation_metrology/automation_step_ledger.py` | 23 | header says verbatim/as received |
| Simulators | `CLAUDE.md` | 8 | header says verbatim/as received |
| Simulators | `TOOL_FINDER/REPORT_WO_FINDER.md` | 1 | header says verbatim/as received |
| Simulators | `blind-reader-void12/studies/K3_MODE_SEQUENCE_DEFAULT.md` | 1 | header says verbatim/as received |
| Simulators | `forest-model-ledger/CLAUDE.md` | 5 | header says verbatim/as received |
| Simulators | `forest-model-ledger/README.md` | 1 | header says verbatim/as received |
| Simulators | `forest-model-ledger/WORK_ORDER.md` | 1 | header says verbatim/as received |
| Simulators | `forest-model-ledger/ledger/STATUS_MAP.md` | 2 | header says verbatim/as received |
| Simulators | `habitat-lag-dependency/README.md` | 2 | header says verbatim/as received |
| Simulators | `held-gaps/OPEN_QUESTIONS.md` | 2 | header says verbatim/as received |
| Simulators | `playground-crossrun/ORIGIN_NOTE.md` | 1 | header says verbatim/as received |
| Simulators | `playground-crossrun/STEP1_REPORT.md` | 1 | header says verbatim/as received |
| Simulators | `relational-playground/SPEC_GPT.md` | 1 | header says verbatim/as received |
| Simulators | `relational-playground/WORK_ORDER.md` | 2 | header says verbatim/as received |
| drift-archive-audit | `GENDER-BY-TOPIC.md` | 10 | header says verbatim/as received |
| infrastructure-stability-model | `legacy/ledger.json` | 1 | path |
| method-layer | `reasoning-layer/cards/anchor-position--prompts.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/archive--assessor-coupling--conditions.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--assessor-coupling--disclosure_audit.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--assessor-coupling--pool_metric.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--assessor-coupling--precedent.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--assessor-coupling--run_all.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--assessor-coupling--selftest.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--clause_audit.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--dissimilar.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--horn_b.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--load_class.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--run_all.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--selftest.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--chain-position--trust_provenance.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--p1_dependency_records.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--p2_substrate.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--p3_comprehension.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--p4_goal_coherence.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--p5_lag_declaration.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--run_all.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--scope.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--cooperative-substrate-proof--selftest.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--crediting-rate--crediting_rate_v2.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--crediting-rate--make_fixtures_v2.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--instrument-index--build_index.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--instrument-index--coverage.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--interaction_class--interaction_class.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--stability-trigger-envelope--cases.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/archive--stability-trigger-envelope--descent_record.yaml` | 1 | path |
| method-layer | `reasoning-layer/cards/effective-redundancy-audit--worked_example.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/failure-mode-register--entries_v2.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/failure-mode-register--entries_v3.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/failure-mode-register--entries_v4.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/failure-mode-register--register_v2.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/failure-mode-register--register_v3.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/failure-mode-register--register_v4.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/falsifier-audit--extract.yaml` | 1 | header says verbatim/as received |
| method-layer | `reasoning-layer/cards/tools--conditional_claims.yaml` | 1 | header says verbatim/as received |
| thermodynamic-accountability-framework | `CONFLICTS.md` | 3 | header says verbatim/as received |

Source: classification run in the session of 2026-11-20 (Claude Code), counts by `git grep -I -i -w -c`. Observer slots: null.
