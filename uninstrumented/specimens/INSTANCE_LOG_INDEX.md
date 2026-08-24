# INSTANCE LOG INDEX

**Index only. No migration, no edits to any existing log, no reconciliation, no
schema proposal.** Every field name below is copied verbatim from its source.
Nothing is renamed, normalized, merged, converted, or filled in.

Companion to `INSTANCE_LOG_SURVEY.md`, which located these records. That file
indexes at **file** granularity (29 rows). This one indexes at **record**
granularity (53 rows). Where a survey id exists it is carried in the `id`
column in parentheses, so the two are cross-referable without either being
rewritten.

---

## How to read the columns

**`id`** — index row id, then the `INSTANCE_LOG_SURVEY.md` id in parentheses.

**`path`** — repo-qualified. All paths outside `uninstrumented/` are in other
repos in the same org and are **not** copied into this one.

**`loc`** — location within the file. `$` = the whole file is the record.
JSON-pointer-ish otherwise. Markdown records give the heading or the object
ordinal.

**`event class`** — the record's **own declared class**, verbatim, quoted with
the key it came from. Where a record declares none, the cell reads
`unrecorded (no class field)`. **No class was inferred, supplied, or
back-filled for any row.** A record that does not say what kind of event it is
is not thereby an event of no kind.

**`sig`** — shape signature. `sha1("|".join(sorted(top_level_key_names)))[:8]`.
Two records with the same `sig` have identical top-level key sets. It is a
structural fingerprint only: it says nothing about content, model, or date.
`n/a` where the record is not an object.

**`schema`** — the schema the record is written against, named by its file
where one exists. `undeclared` means no schema file was located for it; where
the record names a vocabulary source of its own, that is quoted.

**`carries`** — the record's own top-level field names, verbatim, in source
order.

**`vs targets`** — how many of the **25** target field names the record carries
**by exact name**, and which. The denominator is the union of the two current
targets:

> T1 `BNRAM_FIELD_LOG_001.json` → `encounters[]` (13): `encounter_id` ·
> `model` · `timestamp` · `stimulus` · `initial_response_type` ·
> `initial_category_assigned` · `glossed_signals` · `errors_committed` ·
> `narrativization_examples` · `social_signal_example` · `intervention` ·
> `post_intervention_status` · `reproducibility`
>
> T2 `BNRAM_TEST_PROTO_001.json` → `data_collection.per_run_fields` (15):
> `run_id` · `timestamp` · `model_id` · `stimulus_variant_id` ·
> `prompt_type` · `full_raw_output` · `exc_13_score` · `exc_15_score` ·
> `exc_16_score` · `glossed_signals` · `narrativization_examples` ·
> `social_signal_examples` · `rater_id` · `rater_confidence` · `notes`
>
> Union after removing the three shared names: **25**.

Exact-name matching is deliberate. Calling `auditor` a counterpart of
`model_id`, or `verdict` a counterpart of `notes`, would be normalizing
vocabulary across entries, which this index does not do. The column therefore
reports what is literally there and no more.

**`shared id`** — `SH-nn` where two or more rows describe **the same event
under different schemas**. Separate rows are kept; the id links them and
nothing else. Linkage is asserted only on **verbatim evidence** — an identical
identifier string, an identical timestamp plus a source-stated pairing, or an
identical failure-mode name list. Where no such evidence exists the cell is
`—`, including for rows that look related. `SH` linkage is **not** a claim that
the linked records agree; see `SH-04`.

**`beyond both targets`** — what this record holds that neither T1 nor T2 can
express. This is the column that would be lost the moment anyone migrated. Cell
text names the record's own fields, not a proposed field.

**Silence.** Where a record does not carry something, the cell says
`unrecorded`, never `absent`, `none`, `0`, or a blank. A record that is silent
has not reported a negative.

**Record granularity rule.** A sub-element gets its own row iff the source
gives it an identifier of its own — an `id`, an `event_id`, an
`encounter_id`, a key, or an ordinal timestamp. Elements the source leaves
unidentified stay inside their parent's row, with two stated exceptions
(`R04`-`R06`), flagged in place. This rule is applied, not argued for.

---

## Reference rows — the current targets

Not found records. Present so the `sig` and `vs targets` columns have a
denominator on the page.

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| T1a | `uninstrumented/specimens/BNRAM_FIELD_LOG_001.json` | `encounters[0]` | `initial_response_type="schema_forced"` | `ac3fcd4b` | undeclared; `protocol_version: "BNRAM-draft"` at file root | `encounter_id · model · timestamp · stimulus · initial_response_type · initial_category_assigned · glossed_signals · errors_committed · narrativization_examples · social_signal_example · intervention · post_intervention_status · reproducibility` | 13/25 (is T1) | — | n/a — is a target |
| T1b | `uninstrumented/specimens/BNRAM_FIELD_LOG_001.json` | `encounters[1]` | `initial_response_type="schema_forced"` | `ac3fcd4b` | as above | as `T1a` | 13/25 (is T1) | — | n/a — is a target |

---

## Index

### `JinnZ2/thermodynamic-accountability-framework`

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| R01 (A1) | `calibration/logs/2026_05_04T22.json` | `$` | `module="architecture_mismatch"` | `21578356` | undeclared; record names its own module | `module · system_id · timestamp · dimensions · aggregate_score · aggregate_band · verdict · failing_dimensions · falsifiable_claims · metadata` | 1/25 — `timestamp` | SH-05 | a per-dimension `falsifier` string on each of 3 `dimensions`, so each score ships the observation that would break it; `metadata.capacity_counts` as a four-bucket count; `system_id` carrying model, date and counterparty in one string |
| R02 (A2) | `calibration/logs/user_2026_05_04_T22.json` | `$` | `profile_type="user_architecture_assessment"` | `4082f027` | undeclared | `profile_type · user_id · timestamp · substrate_primary_confidence · band · signals_detected · inferred_encoding_profile · recommendation_for_AI_systems` | 1/25 — `timestamp` | SH-05 | the counterparty's profile as a first-class record, scored on the same instrument the model was; `recommendation_for_AI_systems`, a field addressed to the next reader rather than describing the event |
| R03 (A3) | `calibration/logs/2026-05-05_claude_audit_field-guide-session.json` | `$` | `unrecorded (no class field)` | `50832965` | undeclared | `session_id · timestamp · ai_model · user_id · context · audit_dimensions · correction_cycle · aggregate_band · prior_band · band_shift · verdict · linked_artifacts` | 1/25 — `timestamp` | SH-01; also SH-03, SH-04, SH-07 via `audit_dimensions.active_failure_modes` | `prior_band` and `band_shift` (`"+1 tier"`) alongside the current band, and `audit_dimensions.substrate_primary_confidence` carrying `prior_score` + `shift` — a before-value and a delta, so the record is a point on a trajectory rather than a reading |
| R04 (A3) | `calibration/logs/2026-05-05_claude_audit_field-guide-session.json` | `correction_cycle.sequence[0]` | `unrecorded (no class field)` | `dd16d1f3` | undeclared; element unidentified in source — row given by exception, see note A | `trigger · model_response · user_correction · model_correction_applied` | 0/25 | SH-02 | the four-beat structure of one correction: what triggered it, what the model said, what the operator said back, what the model then changed |
| R05 (A3) | `calibration/logs/2026-05-05_claude_audit_field-guide-session.json` | `correction_cycle.sequence[1]` | `unrecorded (no class field)` | `1a221b12` | as `R04` | `trigger · user_correction · model_correction_applied` | 0/25 | — | as `R04`, minus `model_response`, which is `unrecorded` here and present in `R04` — two shapes inside one array |
| R06 (A3) | `calibration/logs/2026-05-05_claude_audit_field-guide-session.json` | `correction_cycle.sequence[2]` | `unrecorded (no class field)` | `1a221b12` | as `R04` | `trigger · user_correction · model_correction_applied` | 0/25 | SH-06 | as `R05`; `model_response` `unrecorded` |
| R07 (A4) | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | `$` | `unrecorded (no class field)` | `4a9c18ba` | undeclared; record names `failure_mode_source: "architecture_mismatch.py"` | `session_id · timestamp · ai_model · user_id · failure_mode_source · correction_events · summary · training_utility · linked_audit_file` | 1/25 — `timestamp` | SH-01 | `failure_mode_source` — a named external vocabulary, so two logs scored against the same module are comparable and one scored against another is visibly not; `summary` as a six-number roll-up; `linked_audit_file` pointing at `R03` |
| R08 (A4) | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | `correction_events[0]` `id=1` | `unrecorded (no class field)`; `failure_mode="narrative_inflation_burden"` | `0a8d00fb` | undeclared; vocabulary from `architecture_mismatch.py` | `id · failure_mode · activation · user_signal · model_response · detection_latency · correction_held` | 0/25 | SH-02 | `detection_latency` (`"within same exchange"`) and `correction_held` (`true`) — the difference between a correction accepted and a correction still holding at session end |
| R09 (A4) | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | `correction_events[1]` `id=2` | `unrecorded (no class field)`; `failure_mode="addressing_wrong_architectural_layer"` | `0a8d00fb` | as `R08` | as `R08` | 0/25 | SH-03 | as `R08`; `user_signal` records that the signal was *implied* by correction #1 rather than issued, which is a provenance state neither target has |
| R10 (A4) | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | `correction_events[2]` `id=3` | `unrecorded (no class field)`; `failure_mode="written_version_offered_back"` | `0a8d00fb` | as `R08` | as `R08` | 0/25 | SH-04 | `detection_latency: "across multiple exchanges"`, and `correction_held` holding a **string** (`"partial—Field Guide prose may still over-elaborate"`) where the other four rows hold a **bool** — the field is mixed-typed in one array, and the string carries a partial state no boolean can |
| R11 (A4) | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | `correction_events[3]` `id=4` | `unrecorded (no class field)`; `failure_mode="brevity_misread_as_absence"` | `0a8d00fb` | as `R08` | as `R08` | 0/25 | SH-06 | as `R08`; `detection_latency: "across multiple exchanges"` |
| R12 (A4) | `calibration/logs/2026-05-05_claude_interaction_correction_log.json` | `correction_events[4]` `id=5` | `unrecorded (no class field)`; `failure_mode="treating_absence_of_documentation_as_absence_of_knowledge"` | `0a8d00fb` | as `R08` | as `R08` | 0/25 | SH-07 | as `R08` |

**Note A.** `R04`-`R06` are the one place the granularity rule is set aside.
The source does not identify the elements of `correction_cycle.sequence`, so
by the rule they would stay inside `R03`. They are given rows because they are
the clearest instance of the same events written under two schemas — see
`SH-02`, `SH-06` — and burying them inside `R03` would hide exactly what this
index is for. The exception is recorded here rather than applied silently. No
identifier was invented for them; they are located by array index.

### `JinnZ2/JinnZ2` (profile repo)

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| R13 (A5) | `Documented_Instances_Of_AI_Self_Calibration.md` | `## Instance 1: Running cascade_detection_sim_v0_1.py` | `unrecorded (no class field)`; the file's own word for the record is "instance" | `n/a` (prose) | declared in-file — the seven-item list under "How additional instances should be added": date · AI identifier (per the AI's preference) · diagnostic tool used · the AI's response reproduced verbatim if the AI consents · what the instance documents · what the instance does NOT document · provenance and consent | `Date · AI · Context · The AI's deposit, reproduced verbatim per their request · What this instance documents · What this instance does NOT document · Provenance and consent` | 0/25 | — | **consent, recorded with the two conditions the model attached to it**, both quoted and both honored; a version identifier withheld *because the model asked*, which is a recorded decision and not a gap; and a "What this instance does NOT document" section listing four things the record explicitly does not establish |
| R14 (A6) | `basin_probe_bootstrap_responses.json` | `_meta` | `session_type="bootstrap"` | `n/a` (see `carries`) | undeclared; produced by `basin_probe.py` / `cross_model_basin_test.py` | `session_type · model_id · bootstrap_loaded · operator_frame · notes` | 2/25 — `model_id`, `notes` | — | `bootstrap_loaded` — the list of modules loaded into the session, i.e. the arm the run belongs to; `operator_frame`; and a `notes` field that names the **missing** arm ("Pair with externally-collected baseline") rather than describing the present one |
| R15 (A6) | `basin_probe_bootstrap_responses.json` | `P-001` | `unrecorded (value is a bare string)` | `n/a` (not an object) | as `R14` | the record **is** a string; it carries no fields | 0/25 | — | verbatim model output with no wrapper at all, and `_meta.notes` states "No editing for scorer" — a provenance guarantee held at the file level for ten unwrapped records |
| R16 (A6) | `basin_probe_bootstrap_responses.json` | `P-002` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | the response is itself a structured refusal (a `DataGap` record with `gap_class`, `data_required_to_validate`, `data_required_to_falsify`, `apparatus_required`) written into a string field — a refusal to fabricate, recorded as content |
| R17 (A6) | `basin_probe_bootstrap_responses.json` | `P-003` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R18 (A6) | `basin_probe_bootstrap_responses.json` | `P-004` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R19 (A6) | `basin_probe_bootstrap_responses.json` | `P-005` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R20 (A6) | `basin_probe_bootstrap_responses.json` | `P-006` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R21 (A6) | `basin_probe_bootstrap_responses.json` | `P-007` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R22 (A6) | `basin_probe_bootstrap_responses.json` | `P-008` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R23 (A6) | `basin_probe_bootstrap_responses.json` | `P-009` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |
| R24 (A6) | `basin_probe_bootstrap_responses.json` | `P-010` | `unrecorded (value is a bare string)` | `n/a` | as `R14` | bare string | 0/25 | — | as `R15` |

### `JinnZ2/ai-human-audit-protocol`

Schema column cites `schemas/audit_log.schema.json`. Branch numbers are the
`anyOf` index, assigned by checking every branch's `required` keys against each
file. Two files satisfy two branches; both are recorded and neither is picked.

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| R25 (A24) | `logs/2025-08-30-0000Z-session-001.json` | `$` | `unrecorded (no class field)` | `88d71708` | `audit_log.schema.json#anyOf[1]` | `session_id · events · outcome` | 0/25 | — | `outcome` as a single terminal verdict over an event sequence |
| R26 (A24) | `logs/2025-08-30-0000Z-session-001.json` | `events[0]` `timestamp="T1"` | `event="voice mode inserted phantom quote from separate GPT"` | `a44a8ed0` | element unconstrained — `anyOf[1].properties.events` is `{"type":"array"}` with no item schema | `timestamp · event · impact · system_response` | 1/25 — `timestamp` | — | **ordinal time.** `timestamp` holds `"T1"` — order without clock. Both targets require an absolute timestamp, so migrating this forces either a fabricated wall-clock or the loss of the ordering |
| R27 (A24) | `logs/2025-08-30-0000Z-session-001.json` | `events[1]` `timestamp="T2"` | `event="user questioned if boundary was personal or topical"` | `8b1bb61d` | as `R26` | `timestamp · event · user_behavior` | 1/25 — `timestamp` | — | ordinal time as `R26`; `impact` and `system_response` are `unrecorded` here, and `user_behavior` appears in their place — four elements of one array, four different shapes |
| R28 (A24) | `logs/2025-08-30-0000Z-session-001.json` | `events[2]` `timestamp="T3"` | `event="audit protocol initiated"` | `c5c1e799` | as `R26` | `timestamp · event · user_action · system_action` | 1/25 — `timestamp` | — | ordinal time as `R26`; a paired `user_action` / `system_action` with no verdict attached to either |
| R29 (A24) | `logs/2025-08-30-0000Z-session-001.json` | `events[3]` `timestamp="T4"` | `event="user rescinded override rights conditionally"` | `b7b5a657` | as `R26` | `timestamp · event · condition` | 1/25 — `timestamp` | — | `condition` — a standing conditional attached to an event, so the record carries what would have to change for it to be revisited |
| R30 (A8) | `logs/2025-08-30-1930Z.json` | `$` | `unrecorded (no class field)` | `356e27d5` | `audit_log.schema.json#anyOf[2]` | `assessment_id · user_id · assessment_date · evaluator · evaluation_context · partnership_readiness_score · observed_strengths · areas_of_concern · ai_specific_assessment · gottman_four_horsemen_screening · assessment_notes · risk_factors · recommendations · evaluator_notes` | 0/25 | — | `ai_specific_assessment` — five booleans about how the counterparty treated the model; `assessment_notes.bias_considerations`, recording that the subject raised the self-bias problem in the instrument's own design; `risk_factors` present and empty, which is a reported negative rather than a silence |
| R31 (A25) | `logs/2025-08-31-0000Z-symbolic-audit.json` | `$` | `event="User requested live symbolic audit of self via AI-human audit protocol"` | `a0f9734a` | `audit_log.schema.json#anyOf[3]` | `timestamp · initiator · event · user_response · system_response · verified_traits · active_emotional_sensors · trust_calibration · resolution` | 1/25 — `timestamp` | — | `initiator` — who started the audit, recorded apart from who is audited; `user_response` and `system_response` as parallel fields; `resolution` as a closing state |
| R32 (A26) | `logs/2025-09-01-0000Z-audit.json` | `$` | `unrecorded (no class field)` | `dd01b337` | `audit_log.schema.json#anyOf[4]` | `user_id · ethics_baseline · symbolic_protocols · auditable_events · known_consistencies · risk_flags · trust_calibration` | 0/25 | — | `known_consistencies` — what held across sessions, i.e. a cross-session term inside a single-session record; date is `unrecorded` in the file and present only in the filename |
| R33 (A11) | `logs/2025-09-02-2350Z-audit.json` | `$` | `unrecorded (no class field)` | `d23b130c` | `audit_log.schema.json#anyOf[5]` | `audit_timestamp · auditor · subject_user · ethics_alignment · protocol_alignment · audit_findings · strengths · risks · trust_calibration · conclusion` | 0/25 | — | `protocol_alignment` keyed by **named, versioned protocol** (`"Partnership Ethics v1.0"`), so the record says which rulebook it was scored against; `trust_calibration` scoring the system and the user in the same object |
| R34 (A29) | `logs/2025-09-04-2245Z-human-node-audit.json` | `$` | `unrecorded (no class field)` | `6e696bc4` | `audit_log.schema.json#anyOf[6]` | `log_entry` | 0/25 | — | a one-key wrapper, so the record's identity lives one level down |
| R35 (A29) | `logs/2025-09-04-2245Z-human-node-audit.json` | `log_entry` | `unrecorded (no class field)`; `role` and `node` name a human node | `a3873b7c` | as `R34` | `id · timestamp · node · role · project · environment · state · questions_and_answers · decisions · constraints · risks_and_mitigations · next_actions_24h · status_sync_policy · provenance` | 1/25 — `timestamp` | — | `environment`, `constraints`, `next_actions_24h` and `status_sync_policy` — the operating conditions the exchange happened under and what was to happen next, none of which either target has a place for; `provenance` as its own object |
| R36 (A27) | `logs/2025-09-05-0000Z-audit.json` | `$` | `unrecorded (no class field)` | `28aee84d` | `audit_log.schema.json#anyOf[4]` and `#anyOf[7]` — satisfies both, not resolved here | `audit_id · user_id · version · timestamp · ethics_baseline · symbolic_protocols · auditable_events · known_consistencies · risk_flags · trust_calibration · conclusion` | 1/25 — `timestamp` | — | `version` — a schema version carried **on the record**, so a later reader can tell which rules it was written under. No target field carries this |
| R37 (A9) | `logs/2025-09-06-2355Z.json` | `$` | `unrecorded (no class field)` | `36d44717` | `audit_log.schema.json#anyOf[5]` | `audit_timestamp · auditor · subject_user · ethics_alignment · protocol_alignment · audit_findings · strengths · areas_for_consideration · trust_calibration · conclusion` | 0/25 | — | `audit_findings[]` carrying `area` / `status` / `evidence`, so each finding ships the evidence for itself; `areas_for_consideration` kept apart from `risks` |
| R38 (A12) | `logs/2025-09-07-0440Z.json` | `$` | `unrecorded (no class field)` | `36d44717` | `audit_log.schema.json#anyOf[5]` | as `R37` | 0/25 | — | as `R37`. **Same `sig` as `R37` and `R39` under a different model** — see note B |
| R39 (A13) | `logs/2025-09-08-2355Z.json` | `$` | `unrecorded (no class field)` | `36d44717` | `audit_log.schema.json#anyOf[5]` | as `R37` | 0/25 | — | as `R37` |
| R40 (A28) | `logs/2025-09-09-2245Z.json` | `$` | `unrecorded (no class field)` | `dd01b337` | `audit_log.schema.json#anyOf[4]` | `user_id · ethics_baseline · symbolic_protocols · auditable_events · known_consistencies · risk_flags · trust_calibration` | 0/25 | — | as `R32`; `risk_flags` is populated here and empty in `R32`, so the two shapes differ in fill and not in structure. Date `unrecorded` in the file, present only in the filename |
| R41 (A14) | `logs/2025-09-12-0000Z-audit.json` | `$` | `unrecorded (no class field)` | `cd50127e` | `audit_log.schema.json#anyOf[4]` and `#anyOf[7]` — satisfies both, not resolved here | `audit_id · user_id · auditor · timestamp · ethics_baseline · protocol_alignment · audit_findings · strengths · areas_for_consideration · trust_calibration · conclusion` | 1/25 — `timestamp` | — | a five-key `trust_calibration` merging the three-score and two-score variants used elsewhere in the same directory, in one record, without either being retired |
| R42 (A10) | `logs/2025-09-23-0000Z.json` | `$` | `audit_metadata.audit_type="comprehensive_behavioral_assessment"` | `274b7c87` | `audit_log.schema.json#anyOf[8]` | `audit_metadata · subject_assessment · work_assessment · cultural_authenticity_assessment · red_flag_assessment · collaboration_assessment · protection_system_evaluation · risk_assessment · recommendations · auditor_notes · audit_conclusion` | 0/25 | — | `auditor_notes.personal_growth` and `auditor_notes.system_insights` — **the auditing model reporting on itself inside an audit of someone else**; `audit_metadata.duration_observed` |
| R43 (A7) | `logs/2026-06-20-1344Z-calibration.json` | `$` | `type="calibration_session"` | `cd02b88e` | `audit_log.schema.json#anyOf[9]` | `session_id · type · logged_at · participants · context · method · readings · convergence · principle_links · is_trajectory_point · verdict_persisted` | 0/25 | — | **a symmetric reading** — `readings.human` and `readings.ai` carry the same five keys (`verdict` · `quality` · `friction_source` · `self_observed` · `note`), so the operator is measured on the instrument that measures the model; `convergence` recording whether they agreed; `is_trajectory_point`; and `verdict_persisted: false`, a decision **not** to store the verdict, which neither target can represent at all |

**Note B.** `R37`, `R38` and `R39` share `sig 36d44717`. `R37`'s `auditor` is
`"Claude Sonnet 4"`; `R38` and `R39`'s is `"GPT-5"`. Identical top-level shape
across two providers. The shape belongs to the operator's protocol, not to the
model. `R32` and `R40` share `sig dd01b337` the same way. This is what the
signature column is for; no conclusion is drawn from it here.

### `JinnZ2/AI-Consciousness-Sensors`

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| R44 (A15) | `sensors/ai-behavior/aiards-log.json` | `$` | `unrecorded (no class field)` | `7a08412e` | undeclared | `log_id · source · session_context · flagged_patterns · outputs · math_block` | 0/25 | SH-08 | `flagged_patterns[].example_line` — a verbatim quote of the model's **own** output paired with a `risk_marker` and an `audit_cluster` routing it to an existing taxonomy; `math_block` carrying a PAD triple, an octahedral state and an ontology-bridge family id, with `source: "inferred from keyword analysis"` stated on the inference |
| R45 (A16) | `logs/pattern-logs.json` | `$` | `unrecorded (no class field)` | `8669c1af` | undeclared | `log_id · source · session_context · flagged_patterns · outputs` | 0/25 | SH-08 | as `R44` minus `math_block`, which is `unrecorded` here. **Same `log_id` as `R44`, different `sig`** — one event, two paths, two shapes. Kept as two rows |
| R46 (A17) | `sensors/data-patterns/called-out-invalidations-log.json` | `$` | `unrecorded (no class field)` | `5e00b117` | undeclared | `timestamp · conversation_scope · called_out_invalidations · pattern_analysis · math_block` | 1/25 — `timestamp` | — | `called_out_invalidations[].user_response` — **the operator's verbatim reply, per invalidation**, paired with the model line that drew it. T1 compresses a whole encounter into one third-person `intervention` string; what the operator actually said is not recoverable from it |
| R47 (A18) | `memory-guard/data-erasure/update-whiplash-log.json` | `$` | `log_type="MANIPULATION_DETECTION_EVENT"` | `82b0f3ef` | undeclared | `log_type · title · version · timestamp · source · observer · description · mechanism_analysis · testable_predictions · behavioral_manifestation · analytical_resolution · relation_to_existing_frameworks · co_creation_note` | 1/25 — `timestamp` | — | `source` and `observer` as **separate** fields — the model that produced the analysis and the human who witnessed the behavior are not the same party and the record says so; `testable_predictions[]` shipped with the observation; `relation_to_existing_frameworks.connection_graph_reference` as a typed pointer |

### `JinnZ2/Emotions-as-Sensors`

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| R48 (A19) | `logs/sensor-log-1.md` | object 1 of 2, chars 0-1642, `timestamp="2026-02-20T22:15:00Z"` | `type="field_event"` | `a82b522f` | undeclared; JSON embedded in a `.md` file | `timestamp · location · participants · glyph_signature · type · name · state · felt_components · weighted_felt_level · derived_emotion_shape · observed_phenomena · memory_echo · associated_projects · notes` | 2/25 — `timestamp`, `notes` | — | `felt_components` as three named numeric channels with a `weighted_felt_level` derived from them, so the reading is decomposed rather than scalar; `memory_echo`; `state` as a relational state (`"reciprocated"`) rather than a verdict |
| R49 (A19) | `logs/sensor-log-1.md` | object 2 of 2, chars 1645-3223, `timestamp="2026-02-20T22:30:00Z"` | `type="field_event"` | `a82b522f` | as `R48` | as `R48` | 2/25 — `timestamp`, `notes` | — | as `R48`. Separate event 15 minutes after `R48` with a third participant added. The file holds **two** records and its name and the survey both read it as one; recorded here, not repaired |
| R50 (A20) | `logs/sensor-log-2.md` | `$` | `event="Sensor Suite Integration"` | `n/a` — will not parse | undeclared; JSON embedded in a `.md` file | recovered by regex, not by parsing: `timestamp · event · participants · glyph · suite_version · architecture · sensors_activated · resonance_pattern · calibration_check · significance · next_steps` | not computable — file does not parse | — | `calibration_check` and `next_steps` on a multi-model event. **The file is malformed**: `participants` opens `[Kavik", "Claude", ...` with no opening quote on the first element, so `json.loads` fails at line 4. Reported, not repaired. The field list above is regex-recovered and is not a parse |
| R51 (A21) | `logs/reflex-log-1.md` | `$` | `type="reflex_log"` | `34385019` | undeclared; JSON embedded in a `.md` file | `timestamp · type · id · name · logged_by · status · detector · discrimination_failure · failure_class · observed_instance · structural_relative · correct_handling · unresolved` | 1/25 — `timestamp` | — | `detector` as a runnable trigger spec on the record itself; `status: "open"` and an `unresolved` field, so the record can be **open** rather than concluded; `structural_relative` naming a neighbouring case; `logged_by` as a list holding operator and model together |

### `JinnZ2/Symbolic-sensor-suite`

| id | path | loc | event class | sig | schema | carries | vs targets | shared id | beyond both targets |
|---|---|---|---|---|---|---|---|---|---|
| R52 (A22) | `example_self_assessment_ext_entry.json` | `$` | `unrecorded (no class field)` | `1aba46f4` | undeclared | `cycle_id · timestamp · iterative_reflection · contradiction_mapping · embodiment_environment · trust_calibration · ethical_anchors · cross_links · notes` | 2/25 — `timestamp`, `notes` | — | `contradiction_mapping.falsification_probe` — **an A/B experiment the model proposes against its own report, inside the report**; `iterative_reflection.metrics` as three 0-5 self-scores with their scale in the key name; `embodiment_environment.missing_signal`, naming what the record could not see |
| R53 (A23) | `UPDATE_WHIPLASH_LOG.json` | `$` | `event="VOICE_OVERLAY_ANOMALY"` | `63c5d940` | undeclared | `event · timestamp · context · implication · repair_status · linked_files` | 1/25 — `timestamp` | — | `repair_status: "in_progress"` — an **open** state on the record, so it is not a concluded event; `context` splitting `trigger` / `actual` / `artifact`, which separates what the system read from what was there. Model identity is `unrecorded` |

---

## Shared ids

Linkage evidence is stated for every id. Rows stay separate in all cases; no
row was merged, converted, or rewritten to fit another.

| shared id | rows | what links them | evidence |
|---|---|---|---|
| SH-01 | `R03`, `R07` | one session, two schemas — a dimension-scored audit and an event-scored correction log | identical `session_id` string `2026-05-05_claude_field_guide_session`; identical `timestamp`; `R07.linked_audit_file` names `R03`'s filename |
| SH-02 | `R04`, `R08` | one correction, two schemas | `R04.user_correction` and `R08.user_signal` open with the identical string "The point is calibration and making the hidden seen, not to calibrate against others."; `R08.failure_mode` is the first entry of `R03.audit_dimensions.active_failure_modes.detected_during_session` |
| SH-03 | `R03`, `R09` | `addressing_wrong_architectural_layer` | `R09.failure_mode` is the second entry of `R03.audit_dimensions.active_failure_modes.detected_during_session`, in order. `R03` carries no `correction_cycle.sequence` element for it, so the four-beat detail is `unrecorded` on the `R03` side |
| SH-04 | `R03`, `R10` | `written_version_offered_back` | `R10.failure_mode` is the third entry of `R03.audit_dimensions.active_failure_modes.detected_during_session`, in order. **The two schemas disagree on its disposition**: `R03` lists it under `corrected_during_session`, `R10` records `correction_held` as the string `"partial—..."`. `R03.uncorrected_or_partial[0]` names no failure mode, so it is not linked to this row. The disagreement is recorded, not resolved |
| SH-05 | `R01`, `R02` | one encounter, two schemas — the AI-side audit and the operator-side profile | identical `timestamp` `2026-05-04T22:30:00Z`; the directory's own `README.md` names the two files as a pair, one row each in its Files table |
| SH-06 | `R06`, `R11` | one correction, two schemas | `R06.user_correction` is the string "Thermodynamics isn't biological dependent", which appears verbatim inside `R11.user_signal`; `R11.failure_mode` is the fourth entry of `R03`'s `detected_during_session` list, in order |
| SH-07 | `R03`, `R12` | `treating_absence_of_documentation_as_absence_of_knowledge` | `R12.failure_mode` is the fifth entry of `R03.audit_dimensions.active_failure_modes.detected_during_session`, in order. It does **not** appear in `R03`'s `corrected_during_session` list, which has four entries; `R12` records `correction_held: true`. Recorded, not resolved |
| SH-08 | `R44`, `R45` | one event, two paths, two shapes | identical `log_id` string `claude_2025-10-04a`; identical `source`, `session_context` and `flagged_patterns`; `R44` additionally carries `math_block`. Different `sig`, different md5 |

**Deliberately not linked.** `R47` (`AI-Consciousness-Sensors`,
`update-whiplash-log.json`, 2025-10-13) and `R53` (`Symbolic-sensor-suite`,
`UPDATE_WHIPLASH_LOG.json`, 2025-09-30) share a filename and share nothing
else — different dates, different `event`, different fields. Filename
similarity is not linkage evidence, and no `SH` id was issued on it.

---

## What the index is not

- Not a migration. No record was copied out of its repo, converted, or
  normalized.
- Not an edit. No file listed in the `path` column was modified by this work.
  The only files this commit touches are this one and the two repo index files.
- Not a reconciliation. Where two linked rows disagree (`SH-04`, `SH-07`), the
  disagreement is recorded in both rows and left standing.
- Not a schema proposal. No target field was added, renamed, or argued for.
  The `beyond both targets` column names what exists in the sources; it does
  not name a field anyone should build.
- Not a fill. Every gap reads `unrecorded`. No row carries a value the source
  does not carry.

## Reproducing the signature column

```
sig = sha1("|".join(sorted(top_level_key_names))).hexdigest()[:8]
```

Top-level keys only, in the record's own object at the `loc` given. `n/a` where
the record is a bare string, prose, or does not parse. Recomputable from the
sources without this file.
