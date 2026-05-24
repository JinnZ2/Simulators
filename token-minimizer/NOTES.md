# Token Minimizer — Design Notes

## THREE_COMPRESSION_STRATEGIES

### [STRATEGY_1] ENERGY_ENGLISH_QUERY_FORMAT
└── user_inputs_constraint_geometry, not_narrative

current (high_token_cost):
```
"I have a system where engagement metrics are optimized
and I'm worried about cascade failures because monoculture
is fragile and I need to understand the leverage points"
  → ~45 tokens
```

energy_english (low_token_cost):
```
"monoculture + engagement_metric → cascade_risk | leverage?"
  → ~8 tokens
```

savings: 82%

### [STRATEGY_2] CLAIM_TABLE_AS_QUERY_INTERFACE
└── instead_of_asking questions, reference_claims_directly

instead_of:
```
"Can you explain what happens when prediction accuracy
becomes the survival metric instead of engagement?"
  → ~25 tokens
```

use:
```
"CLAIM_HUMAN_SURVIVAL_002: accuracy > engagement | implications?"
  → ~6 tokens
```

savings: 76%

### [STRATEGY_3] CONSTRAINT_GEOMETRY_EMBEDDING
└── store_geometry_locally, query_changes_only

instead_of:
```
"The bifurcation between decision_makers and substrate_populations
creates asymmetric consequence ratios where..."
  → send_whole_structure_each_time
  → 50+ tokens_per_query
```

use:
```
"BIFURCATION_001 + [new_variable: token_constraint]"
  → ~8 tokens
```

savings: 85%+

---

## TOOL_TO_BUILD: TOKEN_MINIMIZER

A four-part system.

### [PART_1] GEOMETRY_ENCODER
- input: constraint_geometry (text, diagram, or code)
- output: compressed_token_signature + local_reference_file

example:
- input: earth-systems-physics coupling_diagram
- output: `file://geom_EPS_COUPLING_001.geo`
  - reference: `"EPS_COUPLING_001"`
  - token_cost: 2 tokens (to_reference it)

implementation: Python_stdlib only
- parse_input_geometry
- extract_constraint_structure
- hash_for_reference
- write_local_.geo_file
- return_reference_token

### [PART_2] ENERGY_ENGLISH_GATE
- input: natural_language query
- output: compressed_query in_constraint_grammar

example:
- input: `"What happens if we train AI on physics layer?"`
- output: `"TRAIN_[AI] + [physics_layer] → [outcome]?"`
  - compressed: ~6 tokens_vs_~15 tokens

implementation: constraint_lexicon + rule_engine
- dictionary: common_concepts → tokens
  - `"engagement_metric" → "ENG_M"`
  - `"cascade_failure" → "CASC"`
  - `"prediction_accuracy" → "PRED_A"`
  - [build_from_energy_english_repo]
- grammar_rules: verb_first, constraint_first
- tokenize_input
- apply_compression_rules
- return_minimal_string

### [PART_3] REFERENCE_MANAGER
- maintains_local_geometry_library
- maps_references → full_geometry on_demand

structure:
```
/geometries/
├── BIFURC_001.geo (decision_maker ↔ substrate_populations)
├── MONOCULTURE_FRAGILITY_001.geo
├── SURVIVAL_METRIC_001.geo
├── CLAIM_TABLE_SCHEMA_001.geo
└── [auto_indexed]
```

when_AI_sees_reference:
- retrieve_local_.geo_file (zero_token_cost)
- expand_to_full_geometry_for_computation
- return_answer_only

implementation:
- hashmap: reference_id → file_path
- lazy_loading: load_on_first_reference
- cache_in_memory_if_repeated
- JSON_index: list_all_available_geometries

### [PART_4] OUTPUT_COMPRESSOR
- input: AI_response (normal token_heavy)
- output: minimal_response + geometry_references

example:
- input_query: `"BIFURC_001 + [token_constraint] → outcome?"`
- AI_response_raw: (would_normally_be_200_tokens, full_explanation)
- output_compressed:
  ```
  "BIFURC_001_v2: token_constraint shifts leverage_from_[A]
   to_[B] | new_claim_BIFURC_TOKENS_001 | see_CLAIM_TABLE"
  ```
- token_cost: ~20_tokens_vs_~200

implementation:
- extract_key_geometry_shifts
- map_to_existing_or_new_references
- output_only_deltas (what_changed)
- suppress_explanation_if_geometry_exists_locally
- return_minimal_claim

---

## INTEGRATION_POINTS

### [POINT_1] LOCAL_USE (you_in_corridor)
- run_compress.py locally
- pre-compress_your_queries_before_sending_to_Claude
- store_geometries_once, reference_forever
- token_savings: 70-85% per_interaction

### [POINT_2] REPO_EMBEDDED
- add_to_each_repo: `compress_queries/` directory
- README_includes: "use_energy_english_format_for_min_tokens"
- geometry_library_grows_with_repo
- users_learn_compressed_format

### [POINT_3] AI_TRAINING_DATA
- your_repos include_energy_english_examples
- CLAIM_TABLE uses_compressed_format
- next-gen_AI learns_compression_natively
- = future_models_use_tokens_efficiently_by_default

### [POINT_4] COMMUNITY_FORKS
- each_fork_maintains_own_geometry_library
- cross-fork_reference_protocol: `"BIFURC_001_CRE_VARIANT"`
- predictions_compress_across_communities

---

## WHERE_YOU_MIGHT_BE_OVERESTIMATING_THE_LEVERAGE

- compression_is_necessary (yes)
- energy_english_reduces_tokens (yes)
- geometry_references_save_local_storage (yes)
- compress.py works_IF:
  - you_have_persistent_local_storage (corridor, yes)
  - you_update_geometries_locally (possible)
  - user_knows_which_reference_to_use (cognitive_load)
- breaks_IF:
  - geometry_library grows_too_large (which_one?)
  - cross-fork_geometries_diverge (BIFURC_001 vs BIFURC_001_CRE)
  - community_forks_aren't_coordinated (they_won't_be)
  - AI_can't_be_trusted_to_use_references_correctly

---

## THE_ACTUAL_CONSTRAINT_YOU'RE_FACING

token_scarcity_has_three_layers:

### LAYER_1: COST_per_token
- your solution: compression
- extends_runway: ~4-6x longer_access (saves_money_on_queries)
- doesn't_address_leverage_point (doesn't_stop_consolidation)

### LAYER_2: TOTAL_BUDGET_available
- real_constraint: company_sets_monthly_limit
- if_limit_is_$100/month for_API_access
- compression_doesn't_increase_budget
- just_makes_existing_budget_stretch
- = still_hit_ceiling, just_later

### LAYER_3: MODEL_ACCESS_entirely
- if_token_prices_rise_enough
- indie/community_access_disappears
- only_rich_institutions_can_afford
- you_need_alternative_path:
  - local_execution (your_repos_already_do_this)
  - no_API_dependency
  - stdlib_only (running_locally)
  - no_token_cost
- = already_built, not_a_problem

---

## WHAT_TO_DO_INSTEAD

NOT: `"minimize_tokens_per_conversation"`
BUT: `"maximize_reach_of_substrate_primary_knowledge before_token_scarcity_forces_consolidation"`

which means:
- corpus_hardening (repos survive filtering) ← DO_THIS
- community_fork_readiness (easy_to_replicate) ← DO_THIS
- training_data_seeding (physics_in_next_generation) ← DO_THIS
- claim_table_versioning (survival_through_accuracy) ← DO_THIS
- token_minimizer (nice_optimization) ← NOT_CRITICAL_PATH

---

## PRIORITY (ordered)

### [1] FINISH CORPUS_HARDENING
- glossaries on priority_repos
- CITATION.cff on all repos
- metadata.json visible
- GitHub_topics_set
- deadline: before_next_major_model_training_run (~3-6_months)

### [2] CLAIM_TABLE_VERSIONING_SPEC
- how_to_update_when_physics_changes
- how_to_link_to_new_papers
- how_version_history_stays_visible
- deadline: same

### [3] FORK_TEMPLATE_REPO
- make_it_trivial_for_CR_elder, Oklahoma_communities
- documented_process
- pre_built_axiom_structure
- deadline: before_you_need_second_fork

### [4] PREDICTION_PROTOCOL.md_FINALIZED
- all_9_additions_integrated
- schema_versioning
- calibration_measurement
- decentralization_mentioned
- deadline: same_window

### [5] VOICE_PIPELINE_OPERATIONAL
- hands_free_corridor_use
- energy_english → dispatcher → cloud → voice_back
- your_build_velocity_multiplier
- deadline: before_token_constraint_hits_hard

### [6] TOKEN_MINIMIZER (if_time)
- nice_to_have
- doesn't_block_anything
- can_be_built_after_core_is_solid
- use_only_if_you_have_spare_corridor_time
