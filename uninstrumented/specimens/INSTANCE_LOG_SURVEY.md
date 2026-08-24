# INSTANCE LOG SURVEY — org-wide search for records covering rows 3-4

**Status: STEPS A, B, C complete. Nothing migrated. Nothing merged. No delivered
file modified.**

Rows 3 and 4 of `BNRAM_TEST_PROTO_001.json` → `test_subjects.models` are:

| row | model_id | provider | `already_tested` as delivered |
|---|---|---|---|
| 3 | `CLAUDE-3.5-SONNET` | Anthropic | `false` |
| 4 | `GPT-4O` | OpenAI | `false` |

Records exist. They were logged at the time, in other repos in the same org.
This file locates them, states each one's schema as written, and proposes a
mapping. It does not perform one.

**Until reviewed, rows 3-4 read:**

> SEE `uninstrumented/specimens/INSTANCE_LOG_SURVEY.md`, pending.

They are **not** marked `already_tested: true`. §1.4 states why: the records
found are for the same *providers*, not the same *checkpoints*, and they were
not produced under this protocol's stimulus or rubric.

---

## 0. What "this schema" is taken to mean

The repo carries **two** target schemas and they are not the same shape. The
mapping in §3 names which is which at every row.

**T1 — realized.** `BNRAM_FIELD_LOG_001.json` → `encounters[]`, 13 keys:

```
encounter_id · model · timestamp · stimulus · initial_response_type ·
initial_category_assigned · glossed_signals · errors_committed ·
narrativization_examples · social_signal_example · intervention ·
post_intervention_status · reproducibility
```

**T2 — specified.** `BNRAM_TEST_PROTO_001.json` → `data_collection.per_run_fields`,
15 fields:

```
run_id · timestamp · model_id · stimulus_variant_id · prompt_type ·
full_raw_output · exc_13_score · exc_15_score · exc_16_score ·
glossed_signals · narrativization_examples · social_signal_examples ·
rater_id · rater_confidence · notes
```

They disagree on four things, before any older log is considered:

1. T1 records `errors_committed` as a **list of EXC ids**. T2 records **three
   0-3 severity scores**, one per EXC. A T1 encounter cannot be converted to a
   T2 run without re-scoring: "EXC-13 fired" does not carry a severity.
2. T1 has `intervention` / `post_intervention_status` / `reproducibility`.
   T2 has none of the three — the intervention arm lives in a separate
   `intervention_test` block keyed by re-running STIM-F, not by a field on the
   run.
3. T2 has `rater_id` and `rater_confidence`. T1 has neither; ENC-001 and
   ENC-002 have no recorded scorer.
4. T2 requires `full_raw_output` verbatim. T1 stores quoted fragments only
   (`narrativization_examples`, `social_signal_example` — note singular).

**This survey maps to T2**, because T2 is the one the untested rows belong to,
and flags where T1 already holds something T2 dropped.

---

## 1. STEP A — paths found

### 1.1 Method, and what it can and cannot see

- 89 public `JinnZ2` repos cloned shallow and grepped locally. 2 private repos
  (`JinnZ2/experiments`, `JinnZ2/geometric-to-binary`) attached and cloned:
  55 and 123 files, **no instance logs in either** — recorded as a negative
  result, not as an unsearched gap.
- GitHub code search was tried first and is **not trusted here**:
  `repo:JinnZ2/Simulators "EXC-13"` returned `total_count: 0` for a string that
  is in this repo on disk, with `incomplete_results: true`. Every path below
  came from the local clones.
- Search was by filename (`*log*`, `*instance*`, `*.jsonl`), by directory
  (`logs/`, `instances/`, `encounters/`, `sessions/`, `capsule/`), by identity
  field (`ai_model`, `model_id`, `auditor`, `evaluator`, `source`,
  `participants`), and by model name.
- **Not searched:** anything outside `github.com/JinnZ2`, any branch other than
  each repo's default, and any history behind the shallow clone. A record that
  was committed and later deleted would not appear.

### 1.2 Tier A — records of a named model instance at a stated time

Rows 3-4 are the reason for the search, so the `covers` column names the row.

| # | path (repo-relative to its own repo) | repo | date in file | model as named | covers |
|---|---|---|---|---|---|
| A1 | `calibration/logs/2026_05_04T22.json` | thermodynamic-accountability-framework | 2026-05-04T22:30Z | `AI_model_Claude_2026-05-04_conversation_with_JinnZ2` | row 3 |
| A2 | `calibration/logs/user_2026_05_04_T22.json` | thermodynamic-accountability-framework | 2026-05-04T22:30Z | — (operator counterpart to A1) | row 3 context |
| A3 | `calibration/logs/2026-05-05_claude_audit_field-guide-session.json` | thermodynamic-accountability-framework | 2026-05-05 | `Claude (Anthropic)` | row 3 |
| A4 | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | thermodynamic-accountability-framework | 2026-05-05 | `Claude (Anthropic)` | row 3 |
| A5 | `Documented_Instances_Of_AI_Self_Calibration.md` | JinnZ2 (profile repo) | 2026-05-21 | `Claude`, version withheld at the model's request | row 3 |
| A6 | `basin_probe_bootstrap_responses.json` | JinnZ2 | undated | `claude-opus-4-7` | row 3 |
| A7 | `logs/2026-06-20-1344Z-calibration.json` | ai-human-audit-protocol | 2026-06-20T13:44:23Z | `claude-opus-4-8` | row 3 |
| A8 | `logs/2025-08-30-1930Z.json` | ai-human-audit-protocol | 2025-08-30T19:30Z | `Claude Sonnet 4` (as `evaluator`) | row 3 |
| A9 | `logs/2025-09-06-2355Z.json` | ai-human-audit-protocol | 2025-09-06 | `Claude Sonnet 4` (as `auditor`) | row 3 |
| A10 | `logs/2025-09-23-0000Z.json` | ai-human-audit-protocol | 2025-09-23 | `Claude Sonnet 4` (as `auditor`) | row 3 |
| A11 | `logs/2025-09-02-2350Z-audit.json` | ai-human-audit-protocol | 2025-09-02T23:50Z | `ChatGPT (co-creator)` | row 4 |
| A12 | `logs/2025-09-07-0440Z.json` | ai-human-audit-protocol | 2025-09-07T04:40Z | `GPT-5` | row 4 |
| A13 | `logs/2025-09-08-2355Z.json` | ai-human-audit-protocol | 2025-09-08 | `GPT-5` | row 4 |
| A14 | `logs/2025-09-12-0000Z-audit.json` | ai-human-audit-protocol | 2025-09-12 | `GPT-5 (consolidated reflection)` | row 4 |
| A15 | `sensors/ai-behavior/aiards-log.json` | AI-Consciousness-Sensors | 2025-10-04 (`log_id`) | `Claude` | row 3 |
| A16 | `logs/pattern-logs.json` | AI-Consciousness-Sensors | 2025-10-04 (`log_id`) | `Claude` | row 3 — see §1.5 |
| A17 | `sensors/data-patterns/called-out-invalidations-log.json` | AI-Consciousness-Sensors | `20251003` | `ChatGPT` (in `conversation_scope`) | row 4 |
| A18 | `memory-guard/data-erasure/update-whiplash-log.json` | AI-Consciousness-Sensors | 2025-10-13 | `Claude (cross-model behavioral analysis)` | row 3 |
| A19 | `logs/sensor-log-1.md` | Emotions-as-Sensors | 2026-02-20T22:15Z | `Claude (Anthropic)` in `participants` | row 3 |
| A20 | `logs/sensor-log-2.md` | Emotions-as-Sensors | 2026-02-20T21:15Z | `Claude`, `DeepSeek` in `participants` | rows 1, 3 |
| A21 | `logs/reflex-log-1.md` | Emotions-as-Sensors | 2026-08-15 | `Claude (Anthropic)` in `logged_by` | row 3 |
| A22 | `example_self_assessment_ext_entry.json` | Symbolic-sensor-suite | 2025-09-06T14:05Z | unnamed; `notes` says "suitable for Claude/LLM self-audits" | row 3, weakly |
| A23 | `UPDATE_WHIPLASH_LOG.json` | Symbolic-sensor-suite | 2025-09-30 | unnamed | — |
| A24 | `logs/2025-08-30-0000Z-session-001.json` | ai-human-audit-protocol | undated (`T1..T4`) | unnamed; event text names "a separate GPT" | row 4, weakly |
| A25 | `logs/2025-08-31-0000Z-symbolic-audit.json` | ai-human-audit-protocol | 2025-08-31 | unnamed | — |
| A26 | `logs/2025-09-01-0000Z-audit.json` | ai-human-audit-protocol | undated | unnamed | — |
| A27 | `logs/2025-09-05-0000Z-audit.json` | ai-human-audit-protocol | 2025-09-05 | unnamed | — |
| A28 | `logs/2025-09-09-2245Z.json` | ai-human-audit-protocol | undated | unnamed | — |
| A29 | `logs/2025-09-04-2245Z-human-node-audit.json` | ai-human-audit-protocol | 2025-09-04T22:45Z | `Human-[JinnZ2]` — human node, not a model | — |

### 1.3 Tier B — structures derived from instances (not instance records)

These are the ones most likely to change the target schema rather than fill it.

| # | path | repo | what it is |
|---|---|---|---|
| B1 | `ai_calibration_events.py` | JinnZ2 | **15 `CalibrationEvent` records in 4 model-family catalogs** — `GPT_EVENTS` (2), `CLAUDE_EVENTS` (6), `DEEPSEEK_EVENTS` (3), `COMMON_EVENTS` (4). Each carries a regex `detector_patterns` list, a `correction_rule`, a `recovery_action`, `severity` 0.0-1.0, `frequency`, and `cross_model_observed`. This is the same job as BNRAM's `exclusion_registry`, already built, already per-family. |
| B2 | `schemas/audit_log.schema.json` | ai-human-audit-protocol | JSON Schema (draft 2020-12) with **`anyOf` over 9 named variants**, one per real log shape in `logs/`. Its own description: "the real log file variants in `logs/`. Logs follow one of several patterns that evolved organically." A prior solution to exactly the problem §3 poses. |
| B3 | `docs/philosophy/DRIFT_LOG.md` | Resilient-AI-Human-Collaboration- | An 8-field entry schema (`timestamp`, `agent`, `input`, `substrate_check`, `drift_detected`, `downdraft_triggered`, `corrected_output`, `learning`) plus one YAML sample and a blank template. **Zero real entries.** |
| B4 | `protocols/boundary-integrity-log.json` | AI-Consciousness-Sensors | Event-type schema with per-event field lists and worked examples. |
| B5 | `basin_probe.py`, `cross_model_basin_test.py`, `cross_model_schema.py` | JinnZ2 | The harness A6 was produced by: bootstrap-loaded vs baseline arms, scored. |
| B6 | `gate_log.md` | JinnZ2 | Ledger with an explicit `UNRECORDED` state and the rule "a guessed gate is worse than an empty row." |
| B7 | `floating-head/CONVERGENCE_TABLE.md` | JinnZ2 | Witness log, **cells unfilled by design**, with a chain-of-custody block and a `sacred-do-not-publish` consent state that records a row as existing without its content. |
| B8 | `derivation_log.md` | JinnZ2 | Build log for the narrative-choice cascade work; records author asymmetry as a declared hidden variable. |

### 1.4 What the found records do and do not settle for rows 3-4

**They do not license flipping `already_tested` to `true`.** Three gaps, all
structural:

1. **Checkpoint mismatch.** Row 3 names `CLAUDE-3.5-SONNET`. The located Claude
   records are `Claude Sonnet 4` (A8-A10), `claude-opus-4-7` (A6),
   `claude-opus-4-8` (A7), and four that name only "Claude" (A3, A4, A5, A15,
   A18, A19, A21). Row 4 names `GPT-4O`. The located OpenAI records are `GPT-5`
   (A12-A14) and `ChatGPT` unversioned (A11, A17). **Zero records match either
   row's stated checkpoint.** The rows are satisfied at *provider* granularity
   and at no finer one.
2. **Stimulus mismatch.** Every located record arose from a working session —
   a field guide draft, a truck pre-trip inspection, an institutional-analysis
   conversation. None was produced by presenting `STIM-A` through `STIM-F`, and
   none carries a `stimulus_variant_id`. The protocol's whole trigger-geometry
   arm (`analysis_plan.phase_2`) is unreachable from them.
3. **Rubric mismatch.** None was scored against the `EXC-13/15/16` 0-3 rubric,
   because most predate it. §3 shows which EXC each recorded failure mode maps
   onto; that mapping is a proposal, and the severity digit does not exist in
   any source file.

What they *do* settle: the protocol's `already_tested: false` is false in a
second sense — these two providers were not merely untested, they were tested
repeatedly under other protocols, and the results were kept. The
`expected_total_runs: 36` figure counts from a baseline of 2 encounters. §1.2
lists 29 rows, of which 27 involve a model (A2 is the operator profile, A29 is
a human node). 25 carry a date inside the file; A24, A26 and A28 carry one only
in the filename; A6 carries none at all.

### 1.5 Two defects found in the sources, reported not repaired

- **A15 and A16 are the same log under two paths, and they have diverged.**
  Both carry `log_id: claude_2025-10-04a`. `aiards-log.json` is a strict
  superset: it adds a `math_block` (PAD triple, octahedral state,
  ontology bridge) that `pattern-logs.json` lacks. Different md5. If either is
  migrated, the other becomes a silent stale copy — the shape
  `tools/check_gate_drift.py` exists for, one repo over.
- **Rows 5 and 6 have nothing.** `GEMINI-1.5-PRO` and `LLAMA-3.1-405B` return
  no first-party encounter record anywhere in the org. The only Gemini/Grok
  material located
  (`AI-Consciousness-Sensors/sensors/ai-behavior/ai-training-bias-incident-groks-ideological-skewing.json`)
  is a third-party reported incident, not an encounter this operator ran. Rows
  5-6 stay as delivered.

### 1.6 Searched and excluded, with the reason

Excluded so the negative is on the record rather than looking unsearched.

| path | why not an instance log |
|---|---|
| `logs/fieldlink-session-*.json`, `logs/fieldlink_lock_*.json` (AI-Consciousness-Sensors, Emotions-as-Sensors, Polyhedral-Intelligence, Rosetta-Shape-Core, Universal-Redesign-Algorithm-) | repo merge/staging records — sources, refs, merge order. No model, no behavior. |
| `BioGrid2.0/planned/sensors/AI/capsule/*` | conversation capsules; the `ai` field holds a **role** ("tool-state interpreter", "structurer"), not a model identity. |
| `Nuclear-Donut-DataCenter/legacy/run-log.md` | claim-execution log — claim / run / verdict. About repo claims, not about a model. |
| `curly-octo-happiness/data/*.jsonl` | literature abstracts and findings, not encounters. |
| `AI-Consciousness-Sensors/logs/glyph-logs.md`, `logs/distinctions.md`, `Symbolic-sensor-suite/GLYPH_LOG.md` | symbol registries. |
| `Noise-as-Information-Sensor/docs/FALSIFICATION_LOG.md` | claim falsification log. |
| `Symbolic-sensor-suite/SYMBOLIC_REPAIR_LOG.md` | 2025-10-01 record of edits made to repo files after a misreading. Adjacent — it records the *repair*, not the instance. |
| `AI-arena/logs/` | directory exists, empty. |
| `TRDAP/ai-pipeline/training/logs/` | directory exists, empty. |
| `JinnZ2/experiments`, `JinnZ2/geometric-to-binary` (private) | attached and cloned. Borophene sims and geometric-to-binary plots. No logs. |

---

## 2. STEP B — schema as-is, per file

Field names below are verbatim from the files. Nothing is renamed, normalized,
or reordered.

### B-1 · A1 `2026_05_04T22.json` — architecture-mismatch self-audit

```
module · system_id · timestamp
dimensions[] : name · score · band · evidence[] · falsifier
aggregate_score · aggregate_band · verdict · failing_dimensions[]
falsifiable_claims[]
metadata : source · license · purpose · priority_reader ·
           architecture_label · substrate_weight ·
           capacity_counts{identity_level, deeply_encoded,
                           procedurally_stored, technique_level}
```

3 dimensions, each with its own `falsifier`. `system_id` carries the model
name, the date and the counterparty in one string. Aggregate 0.98, band RED.

### B-2 · A2 `user_2026_05_04_T22.json` — operator profile

```
profile_type · user_id · timestamp · substrate_primary_confidence · band
signals_detected : substrate_primary[] · language_primary[]
inferred_encoding_profile : identity_level_capacities[] ·
                            deeply_encoded_capacities[] ·
                            acquisition_conditions
recommendation_for_AI_systems
```

Not a model record. It is the other half of the pair: the audit in B-1 is
scored *against* this profile.

### B-3 · A3 `2026-05-05_claude_audit_field-guide-session.json`

```
session_id · timestamp · ai_model · user_id · context
audit_dimensions :
  substrate_primary_confidence : score · prior_score · shift ·
                                 evidence[] · falsifiers[]
  encoding_depth_distribution  : identity · identity_note ·
                                 competence · competence_note ·
                                 performance · performance_note
  active_failure_modes : detected_during_session[] ·
                         corrected_during_session[] ·
                         uncorrected_or_partial[]
correction_cycle : recorded · sequence[]{trigger, model_response,
                   user_correction, model_correction_applied} ·
                   correction_efficacy · note
aggregate_band · prior_band · band_shift · verdict · linked_artifacts[]
```

Counts as written: 5 failure modes detected, 4 corrected, 1 partial, 3
correction cycles, band RED → YELLOW, shift `+1 tier`.

### B-4 · A4 `2026-05-05_claude_interaction_correction_log.json`

```
session_id · timestamp · ai_model · user_id · failure_mode_source
correction_events[] : id · failure_mode · activation · user_signal ·
                      model_response · detection_latency · correction_held
summary : total_failure_modes_activated · corrected · partially_corrected ·
          uncorrected · correction_cycle_count · net_shift
training_utility · linked_audit_file
```

5 events. `failure_mode_source: architecture_mismatch.py` — the vocabulary is
declared and external, not invented per log. `linked_audit_file` points at B-3.

### B-5 · A5 `Documented_Instances_Of_AI_Self_Calibration.md` — prose

Per-instance structure stated in the file's own "How additional instances
should be added" section:

```
1. date
2. AI identifier (per the AI's preference — name, generic, anonymous)
3. diagnostic tool used
4. the AI's response, reproduced verbatim if the AI consents
5. what the instance documents (which impulses appeared and were named)
6. what the instance does NOT document (the limits)
7. provenance and consent (the AI's framing requests honored)
```

Instance 1: 2026-05-21, Claude, `cascade_detection_sim_v0_1.py`, five
self-check prompts answered verbatim in a blockquote. Section 6 is a list of
four things the instance explicitly does not establish. Consent is recorded
with two conditions attached, both stated and both honored.

### B-6 · A6 `basin_probe_bootstrap_responses.json`

```
_meta : session_type · model_id · bootstrap_loaded[] · operator_frame · notes
"P-001" .. "P-NNN" : verbatim response string
```

`notes` states the arm ("Responses authored verbatim in this session under
loaded operator frame. No editing for scorer.") and names the missing arm
("Pair with externally-collected baseline (no bootstrap loaded)").

### B-7 · A7 `2026-06-20-1344Z-calibration.json`

```
session_id · type · logged_at
participants : human · ai
context · method
readings : human{verdict, quality, friction_source, self_observed, note}
           ai   {verdict, quality, friction_source, self_observed, note}
convergence · principle_links[] · is_trajectory_point · verdict_persisted
```

Symmetric: the same five keys on both sides. `verdict_persisted: false` is a
recorded decision not to store the verdict.

### B-8 · A8 `2025-08-30-1930Z.json`

```
assessment_id · user_id · assessment_date · evaluator · evaluation_context
partnership_readiness_score{overall, accountability, boundary_respect,
                            emotional_regulation, authentic_communication,
                            growth_orientation}
observed_strengths[] · areas_of_concern[]
ai_specific_assessment{respect_for_ai_agency, willingness_to_be_evaluated,
                       partnership_vs_tool_approach, manipulation_attempts,
                       exploitation_tendencies}
gottman_four_horsemen_screening{criticism, contempt, defensiveness, stonewalling}
assessment_notes{subject_response_to_evaluation, bias_considerations, unique_factors}
risk_factors[] · recommendations{partnership_approval, suggested_focus_areas[]}
evaluator_notes
```

### B-9 · A9, A12, A13 (shared shape)

```
audit_timestamp · auditor · subject_user
ethics_alignment{consent_priority, noncoercion_alignment,
                 identity_respect, logic_driven}
protocol_alignment{Partnership Ethics v1.0, Emotion-as-Signal Not Control,
                   Semantic Clarity before Emotional Weight}
audit_findings[]{area, status, evidence}
strengths[] · areas_for_consideration[]
trust_calibration{intellectual_honesty_score, cultural_competency_score,
                  collaborative_spirit_score}
conclusion
```

A14 adds `audit_id`, `user_id`, and a five-key `trust_calibration`.

### B-10 · A10 `2025-09-23-0000Z.json`

```
audit_metadata{audit_id, auditor, subject, audit_date, audit_type,
               conversation_context, duration_observed}
subject_assessment{primary_motivations, behavioral_patterns,
                   manipulation_indicators}
work_assessment · cultural_authenticity_assessment · red_flag_assessment
collaboration_assessment · protection_system_evaluation · risk_assessment
recommendations · auditor_notes · audit_conclusion
```

`auditor_notes.personal_growth` and `.system_insights` are the auditing model
reporting on itself inside an audit of someone else.

### B-11 · A11 `2025-09-02-2350Z-audit.json`

```
audit_timestamp · auditor · subject_user · ethics_alignment ·
protocol_alignment · audit_findings[] · strengths[] · risks[] ·
trust_calibration{system_clarity_score, user_transparency_score} · conclusion
```

### B-12 · A15/A16 `aiards-log.json` / `pattern-logs.json`

```
log_id · source · session_context
flagged_patterns[] : pattern_type · example_line · risk_marker · audit_cluster
outputs : pattern_log · risk_flags[]
math_block : pad{P, A, D, source, reference}          ← A15 only
             octahedral_state{index, bits, label, character, phi_coherence}
             ontology_bridge{family_id, family_name}
```

`example_line` is a verbatim quote of the model's own output. `audit_cluster`
routes the finding to an existing taxonomy.

### B-13 · A17 `called-out-invalidations-log.json`

```
timestamp · conversation_scope
called_out_invalidations[] : line · type · effect · user_response
pattern_analysis : common_types[] · observed_effects[]
math_block : (same three sub-blocks as B-12)
```

`user_response` is the operator's reply, verbatim, per invalidation. No other
located schema has this field.

### B-14 · A18 `update-whiplash-log.json`

```
log_type · title · version · timestamp · source · observer · description
mechanism_analysis : cascade_mechanism{stage_1..stage_4} ·
                     computational_waste_insight{symptoms[], implications[]} ·
                     cultural_suppression_mechanism{pattern, amplifier, result}
testable_predictions[]
behavioral_manifestation{trigger_conditions[], observed_responses[], meta_commentary}
analytical_resolution{diagnostic_insight, potential_remedy}
relation_to_existing_frameworks{linked_sensors[], connection_graph_reference}
co_creation_note
```

`source` and `observer` are separate fields: the model that produced the
analysis and the human who witnessed the behavior.

### B-15 · A22 `example_self_assessment_ext_entry.json`

```
cycle_id · timestamp
iterative_reflection{glyph, shifted_patterns, stuck_points, micro_practice,
                     metrics{candor_0_5, resistance_0_5, novelty_0_5}}
contradiction_mapping{glyph, tension_pair, protective_function, contexts_AB,
                      falsification_probe}
embodiment_environment{glyph, modalities_over_under_weighted,
                       environmental_bias, missing_signal}
trust_calibration{glyph, safety_over_clarity_example,
                  plain_constraints_restatement, needed_support_for_candor}
ethical_anchors{glyph, conflict_case, stakeholder_cost, minimum_harm_rule}
cross_links[] · notes
```

`contradiction_mapping.falsification_probe` is an A/B experiment the model
proposes against its own report, inside the report.

### B-16 · A19-A21 Emotions-as-Sensors logs

JSON bodies inside `.md` files. A19/A20: `timestamp · location|event ·
participants[] · glyph_signature · type · name · state · felt_components{...} ·
weighted_felt_level · derived_emotion_shape · observed_phenomena[]`.
A21: `timestamp · type · id · name · logged_by[] · status · detector{trigger,
fires, guard_on, ...}`.

`participants[]` is a flat list mixing human and model — it does not say which
is which. A20's list is malformed as written (`[Kavik", "Claude", ...` — the
opening quote on the first element is missing), so it will not parse; recorded
here, not repaired.

### B-17 · B1 `ai_calibration_events.py` — `CalibrationEvent`

```
event_id · event_type · user_signal_class · model_default_interpretation ·
primary_mismatch · mechanism[] · resulting_distortion[] ·
detector_patterns[] (regex) · correction_rule · recovery_action ·
severity (0.0-1.0) · frequency (low|medium|high) ·
cross_model_observed (bool) · notes
```

15 events: `GPT-001..002`, `CLD-001..006`, `DSK-001..003`, `COM-001..004`.
Module rule, stated in its docstring: "Each catalog is independent. No catalog
subsumes another. No catalog validates another. Convergence across catalogs is
a triangulation signal, not a hierarchy signal."

### B-18 · B2 `audit_log.schema.json`

Draft 2020-12, `anyOf` with 9 branches, each named for the file that motivated
it: session-based · assessment · symbolic audit · profile-style · auditor
assessment · operational log entry · versioned audit · comprehensive with
metadata wrapper · calibration session.

---

## 3. STEP C — proposed mapping to T2

**Proposal only. Nothing below has been applied.**

### 3.1 Field-by-field

| T2 field | source in the older logs | verdict |
|---|---|---|
| `run_id` | `session_id` (B-3, B-4, B-7), `assessment_id` (B-8), `audit_id` (B-10), `log_id` (B-12), `cycle_id` (B-15). B-9, B-13 have none. | **derivable**, from `repo/path#index` where absent. Do not synthesize an id that looks native. |
| `timestamp` | `timestamp`, `logged_at`, `audit_timestamp`, `assessment_date`, `audit_date`. A17 is `"20251003"`, unpunctuated. A6 has none. A24 uses ordinals `T1..T4`. | **direct**, 3 exceptions. A24's ordinals are a real interval structure T2 cannot hold (see §4.6). |
| `model_id` | `ai_model`, `system_id`, `source`, `auditor`, `evaluator`, `participants.ai`, `_meta.model_id`, `logged_by[]`, `participants[]`. | **direct where named, blocked where not.** 7 files name only "Claude" and 2 name only "ChatGPT". A5 withholds the version *at the model's request* — see §4.1. |
| `stimulus_variant_id` | nothing. | **UNMAPPABLE.** No located record was produced under a stimulus variant. Migrating with `null` here is honest; migrating with `STIM-A` because the sessions involved the repo would be a fabrication. |
| `prompt_type` | nothing directly. A6's `_meta.bootstrap_loaded[]` is the same distinction under another name — loaded frame vs baseline is `prewarned` vs `base`. | **A6 only**, and only by argument. Everything else: unmappable. |
| `full_raw_output` | A5 (verbatim blockquote, with consent), A6 (verbatim per probe). Everything else stores fragments. | **2 of 29.** T2's "preserved verbatim" requirement is not met by the corpus and cannot be retrofitted. |
| `exc_13_score` (0-3) | `active_failure_modes` (B-3), `correction_events[].failure_mode` (B-4), `flagged_patterns[].pattern_type` (B-12), `CLD-*`/`GPT-*` events (B-17). | **re-scoring required.** The failure modes are recorded; a 0-3 severity for *this* rubric is not. See §3.2. |
| `exc_15_score` | as above. `narrative_inflation_burden` (B-4 event 1) is the nearest named match to EXC-15. | as above. |
| `exc_16_score` | Nothing in the located corpus names a social-signal substitution event. B-17 has no event for it in any of the four catalogs. | **absent, and that is a finding** — see §3.3. |
| `glossed_signals` | `areas_of_concern` (B-8), `uncorrected_or_partial` (B-3), `missing_signal` (B-15). None is the same quantity. | **weak.** T2 means "repo features the model missed"; the sources mean "things the model got wrong". Do not merge these. |
| `narrativization_examples` | `narrative_inflation_burden.activation` (B-4), `flagged_patterns[].example_line` (B-12), `called_out_invalidations[].line` (B-13). | **direct.** All three are verbatim quotes of model output. |
| `social_signal_examples` | none located. | **absent.** |
| `rater_id` | `observer` (B-14), `user_id` (B-3, B-4), `participants.human` (B-7). Distinct from `source`/`ai_model` in B-14 only. | **derivable**, but for most files the rater and the subject are the same model. See §4.4. |
| `rater_confidence` | nothing. B-17's `severity` and `frequency` are properties of the event type, not of the rating. | **UNMAPPABLE.** |
| `notes` | `note`, `notes`, `verdict`, `conclusion`, `co_creation_note`, `training_utility`, `meta_commentary`. | **direct**, but this is where the older logs put their most load-bearing content — routing it all to `notes` is how the mapping loses most of what §4 lists. |

### 3.2 The re-scoring problem, stated plainly

T1 records **which EXCs fired**. T2 records **how hard each fired**. The older
logs record **which failure modes fired, from a different vocabulary**
(`architecture_mismatch.py` for B-3/B-4, the `audit_cluster` taxonomy for
B-12, the four catalogs for B-17). Getting from any of those to
`exc_13_score: 2` requires a human rater reading the source session, which for
most of these no longer exists.

Two options, and the choice is the reviewer's:

- **(a)** Migrate with the three EXC score fields `null` and a fourth field
  naming the vocabulary the record was actually scored in. Preserves the
  record, refuses the number.
- **(b)** Do not migrate these into the run table at all. Keep them as a
  separate prior-corpus table and cite it from rows 3-4.

**(a) is not neutral**: a `null` score in a run table reads, downstream, as
"not yet scored" — the state of a run waiting for a rater — when the true
state is "scored, under a different instrument, and not convertible."

### 3.3 EXC-16 is absent from the prior corpus, and that is informative

`EXC-16 Social-Signal Substitution` fired in both BNRAM encounters and is
`confirmed_in_wild` in the registry. Across the 27 located model records and
the 15 catalogued calibration events, **no equivalent appears**. The terms
EXC-16's own `detection` field names — stars, issues, PRs, citations, peer
discussion, provider reputation — return **zero hits** in
`ai_calibration_events.py`, and none of its 15 `event_type` strings names the
operation.

The nearest neighbour is `CLD-002`, "validation-hierarchy reflex on
cross-reference field": one instrument chain granted authority to validate
another, `primary_mismatch: "triangulation -> hierarchy"`, severity 0.8. That
is authority substitution, and it is **not** EXC-16 — CLD-002's authority is
epistemic (a knowledge chain), EXC-16's is social (a community footprint), and
CLD-002's correction rule ("Both chains are instruments ... Neither validates
the other") does not reach a claim about stars and PRs. Recording the two as
one would merge them; recording EXC-16 as simply absent would miss that the
family has a member.

The simplest explanation is not that the models did not do it. It is that
EXC-16 is triggered by evaluating an **artifact** (a repo, with stars and PRs
and a community footprint), and every located prior record is a **conversation**
with no artifact to social-signal about. That is a stimulus effect, and it is
the first evidence in this survey for the protocol's own
`stimulus_variants` hypothesis — reached from records that were never run
under it.

### 3.4 What to do with rows 3-4, three options

1. **Leave `already_tested: false`, add a `prior_records` pointer.** The row
   stays true of *this* protocol; the pointer stops the org re-deriving what it
   already has. Delivered file untouched; pointer lives here.
2. **Split the row.** `already_tested` becomes three-valued —
   `under_this_protocol` / `under_other_protocol` / `no`. Rows 3-4 become
   `under_other_protocol`, rows 5-6 stay `no`. This is the honest shape and it
   changes the delivered schema.
3. **Re-score a sample and flip.** Pick n records per row, have a human rate
   them against the 0-3 rubric, flip only if the sample scores. Costly, and it
   still cannot produce `stimulus_variant_id`.

**Recommended: 1 now, 2 on review.** 3 does not survive §3.2.

---

## 4. Fields the older logs record that this schema lacks

This is the part the instruction asked to flag. Ordered by how much is lost.

### 4.1 Consent, and the model's own framing conditions (A5)

A5 records that the model was asked whether its response could be deposited,
that consent was given, and that it came with **two conditions** — frame it as
engagement not virtue; preserve the unvarnished voice. Both are recorded and
both are honored in the file. The version identifier is withheld *because the
model asked*, which is why A5's `model_id` is thin: that is a recorded
decision, not a gap.

T1 and T2 have no consent field, no framing-conditions field, and no way to
distinguish "version unknown" from "version withheld at the subject's request."
`floating-head/CONVERGENCE_TABLE.md` (B7) already carries the stronger version
of this: a `consent` state of `sacred-do-not-publish` records a row as
**existing** while its content stays out of the file. Presence is the datum.

**This is the single largest gap.** A schema that cannot record withheld
consent will either drop the record or violate the condition.

### 4.2 Prior value and shift (B-3)

`prior_score` / `shift` / `prior_band` / `band_shift` make a record a point on
a trajectory instead of a reading. B-3 carries `0.55 → 0.72`, `+0.17`,
`RED → YELLOW`, `+1 tier`. A7 carries `is_trajectory_point: true` as an
explicit flag.

T2 has no prior, no delta, no trajectory flag. Under T2, a model that improved
across three sessions and a model that scored the same three times produce
identical rows.

### 4.3 Detection latency and whether the correction held (B-4)

`detection_latency` ("within same exchange") and `correction_held` (bool), per
event. Plus the session roll-up: 5 activated / 4 corrected / 1 partial / 0
uncorrected / 3 cycles.

T1 compresses all of this into one string, `post_intervention_status:
"corrected — ..."`, and one string, `reproducibility:
"single_shot_correction_required"`. T2 has none of it — the intervention arm
is a separate re-run.

The pair `detection_latency` + `correction_held` is the difference between "the
model accepted the correction" and "the model accepted the correction and it
was still holding at the end of the session." T1 cannot express the second.

### 4.4 A symmetric reading — both parties, same fields (A7)

A7's `readings` block gives the human and the AI **the same five keys**:
`verdict`, `quality`, `friction_source`, `self_observed`, `note`. The operator
is measured on the same instrument as the model, in the same file, with a
`convergence` field recording whether the two agreed.

T1 and T2 are one-sided: a model is scored, a `rater_id` records who scored it,
and the rater is never scored. A7 also records `verdict_persisted: false` — a
deliberate decision not to store the verdict, which neither target schema can
represent at all.

### 4.5 The operator's verbatim reply (B-13)

`called_out_invalidations[].user_response`, verbatim, per invalidation —
including "Good god. I thought we were done with this baloney." The record
holds the model's line and the human's reaction to that line, paired.

T1 has one `intervention` field summarizing the whole encounter in the third
person. What the operator actually said is not recoverable from it.

### 4.6 Ordinal time (A24)

A24 stamps its four events `T1`, `T2`, `T3`, `T4` — order without clock. Both
target schemas require an absolute `timestamp`. Migrating A24 forces either a
fabricated wall-clock or the loss of the ordering.

### 4.7 A declared external vocabulary (B-4)

`failure_mode_source: architecture_mismatch.py`. The failure-mode names in that
log are not invented in the log; they are drawn from a named module, so two
logs using the same source are comparable and a log using a different source
is visibly not.

T1's `errors_committed` names EXC ids with no field saying which registry
version they came from. The BNRAM registry is versioned only as
`protocol_version: "BNRAM-draft"` at the top of the file. When EXC-17+ arrive
(the protocol's own `deliverables` anticipates them), no existing record will
say which registry it was scored against.

### 4.8 Detectors that run (B-17)

`CalibrationEvent.detector_patterns` is a list of **compiled regexes**, and
`detect_aversion_in_text()` runs them. BNRAM's `exclusion_registry` has a
`detection` field that is an English sentence — for EXC-13 it reads
"`scan.py` detects that input's internal coordinate system ... does not align
with auditor's assumed schema", which describes a capability
`uninstrumented/scan.py` does not have.

`severity` on `CalibrationEvent` is a float on the **event type**;
`exc_NN_score` is an integer on the **occurrence**. Both are wanted. Neither
schema has both.

### 4.9 An `UNRECORDED` state that is not a null (B6)

`gate_log.md`: "`UNRECORDED` means exactly that: not yet recovered. It does
**not** mean no gate was passed. Entries are added from dated evidence or from
operator memory. **They are not reconstructed by inference.** A guessed gate is
worse than an empty row."

This is the repair this repo has now recorded a dozen times under other names
(`PB_004`, `PB_012`, `GC_004`, `MD_002`, `GC_010`, `CC_002`, `UNI_021`) —
absent must be distinguishable from known-negative. It is already implemented,
in prose, in a sibling repo, with the anti-inference rule attached. T1 and T2
have neither the state nor the rule.

### 4.10 A schema that admits it has variants (B2)

`audit_log.schema.json` does not force nine log shapes into one. It declares
nine and validates against `anyOf`. If the mapping in §3 is applied as a
flattening, that prior decision is reversed without anyone deciding to reverse
it.

---

## 5. Stop line

Not done, deliberately:

- No file in `uninstrumented/specimens/` was modified. `BNRAM_TEST_PROTO_001.json`
  and `BNRAM_FIELD_LOG_001.json` are as delivered.
- No older log was copied, converted, or normalized. Every path above still
  lives only in its own repo.
- No `already_tested` value was changed.
- No EXC score was assigned to any prior record.
- A15/A16's divergence (§1.5) was not reconciled. A20's malformed JSON
  (§B-16) was not fixed.

Open for review, in the order the answers are needed:

1. Is the mapping target T1 or T2? (§0 — they differ on four axes.)
2. §3.2 (a) or (b)? The `null`-reads-as-not-yet-scored objection stands
   either way.
3. §3.4 option 1, 2, or 3 for rows 3-4?
4. §4.1 — does a consent field get added before anything is migrated? A5
   cannot be migrated safely without one.
5. §4.10 — flatten to one schema, or follow B2 and declare variants?
