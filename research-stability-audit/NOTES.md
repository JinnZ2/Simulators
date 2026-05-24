# Research Stability Audit — Source Notes

## WHAT_THE_DATA_ACTUALLY_SHOWS

### RETRACTION_STATISTICS
- 0-5.5% of papers formally_retracted (Clinical Medicine highest)
- but retraction_LAGS_far_behind_actual_failure
  - many_broken_studies_never_retracted
- retraction_rate_increasing:
  - 10x increase_in_retractions_2000-2020 (Nature, 2024)
  - rate_of_increase_accelerating

### REPRODUCIBILITY_CRISIS (what_actually_matters)
- 40% psychology_studies_replicate (vs should_be_80-90%)
- 50% social_science_studies_replicate (3,900 paper study, Nature)
- 70% researchers_failed_to_replicate_someone_else's_work (Nature survey)
- 50% of_researchers_failed_to_replicate_their_OWN_work
- → real_failure_rate_is_40-60%, not_0-5%

### MODEL_DRIFT_IN_AI
- 91% of_ML_models_degrade_over_time (Nature study, 2025)
- performance_degrades_in_weeks_to_months (not years)
- especially_severe_in_fast-changing_domains
  - COVID example: Spotify_recommendation_drift_in_days
- → AI_model_obsolescence_FASTER_than_research_papers

### FIELD-SPECIFIC_PATTERNS
- fast-moving_fields (AI, medicine, biotech):
  - citation_half_life: 3-5_years
  - 50-70% research_becomes_outdated/wrong
  - model_performance_degrades_monthly
- slower_fields (mathematics, physics_fundamentals):
  - citation_half_life: 10-15_years
  - foundational_work_persists
  - core_laws_stay_true
- implication: ORIGINAL_OBSERVATION_WAS_CONSERVATIVE
  - 80% in 2-5 years was_understating
  - faster_domains: 50-70% in 6-18 months
  - AI_models: 80-90% in 30-60 days

---

## KEY_CITATIONS

### [CLAIM_RES_001] Research Failure Rate Exceeds Official Retractions
- Source: Nature (2024) — "Biomedical paper retractions have quadrupled in 20 years"
  - Freijedo-Farinas et al., Scientometrics 129, 2867-2882
  - retraction_rate increased 4x in 20_years
- Source: Nature (7-year project) — "Half of social-science studies fail replication test"
  - tested 3,900 papers, 50% failed replication
- Source: PNAS — "Replication success varies by discipline"
  - Psychology: ~40% replicate successfully
  - Implies: ~60% fail_to_replicate
- Claim: "Research_failure_rate_is_40-60% but only 0-5% formally retracted"
  - falsifiable: replicate_same_studies_independently

### [CLAIM_MDL_001] AI Model Degradation Accelerates Knowledge Obsolescence
- Source: Nature (2025) — AI Model Degradation Study
  - 91% of_ML_models_degrade_over_time
  - degradation_timescale: weeks_to_months
- Source: Splunk / IBM Model Drift Documentation
  - concept_drift_occurs_as_data_distribution_changes
  - continuous_monitoring_required
- Claim: "AI_systems_degrade_faster_than_traditional_research (days vs months vs years)"
  - falsifiable: track_model_performance_over_time

### [CLAIM_BIF_001] Bifurcation Prevents Knowledge_Recovery During Crisis
- Source: Santa Fe Institute — "The race between innovation and obsolescence"
  - Lee, West, Kempes model
  - Schumpeterian_dynamics: innovation_vs_obsolescence_race
- Claim: "Once_substrate_knowledge_stops_being_taught, recovery_requires_>1_generation"
  - falsifiable: historical_case_studies_of_knowledge_loss

---

## CROSS_REFERENCE_TO_EMERGENCE_SIMULATOR

AI_models_degrade_like_failed_research: same_physics.

- Engagement-driven models (no physics baseline) behave like parasitic
  agents in `emergence-stability-simulator`: they amplify pressure,
  spend more energy, and accumulate cascade.
- Falsifiable methodology behaves like the physics baseline: it damps
  cascade and pulls neighbors toward it (EMRG_006 attractor effect).
- A corpus that embeds falsifiable claims is to a field what a stable
  agent is to a multi-agent system.

The audit framework here exists so the *same* methodology
(falsifiability + cascade detection) that runs on simulated agents
can be applied to real research and real models.
