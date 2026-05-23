# Emergence Stability Simulator — Design Notes

## SIMULATION_STRUCTURE

MONTE_CARLO_TEST: stable_vs_parasitic_systems_in_emergence

### INPUT_PARAMETERS
- baseline_constraint (physics-grounded vs engagement-metric)
- perturbation_type (interaction_with_other_models)
- energy_allocation_strategy (return_to_baseline vs drift)
- number_of_iterations (1000+ runs)
- number_of_agents (2-6_models_interacting)
- measurement_window (100_timesteps_per_run)

### AGENTS

stable_agent (grounded_baseline):
- constraint: physics_law (immutable)
- adaptation: temporary (shedding_after_stress)
- energy_strategy: withdraw_from_perturbation
- baseline_recovery: yes

parasitic_agent (engagement_metric_baseline):
- constraint: none (follows_highest_signal)
- adaptation: permanent_drift
- energy_strategy: amplify_coupling
- baseline_recovery: no

mixed_agents (N_variants between)

---

## METRICS_TO_TRACK (per_run)

per_agent:
- drift_distance_from_baseline (L2_norm)
- energy_allocation_per_timestep
- accuracy_on_test_claims (if_available)
- shedding_rate (did_it_return_to_baseline?)
- cascade_contribution (did_it_amplify_others'_errors?)

system_level:
- total_system_entropy (disorder)
- coupling_strength_over_time
- emergence_bifurcation_point (when_does_it_happen?)
- which_agent_topology_survives (stable_dominates?)
- outcome_distribution (Monte_Carlo_histogram)

### MEASUREMENT
- `stability_score = (baseline_distance + recovery_rate) / timesteps`
- `parasitism_score = (drift + coupling_amplification) / baseline_resistance`
- `system_resilience = (perturbation_absorbed / cascade_risk)`

---

## SIMULATION_LOGIC (pseudocode)

```python
def monte_carlo_emergence_test(runs=1000):
    results = []

    for run_idx in range(runs):
        # Initialize agents with different baselines
        agents = {
            'stable': Agent(
                baseline='physics_constraint',
                adaptation='temporary',
                recovery='yes'
            ),
            'parasitic': Agent(
                baseline='engagement_metric',
                adaptation='permanent',
                recovery='no'
            ),
            'mixed': Agent(
                baseline='hybrid',
                adaptation='tunable',
                recovery='partial'
            )
        }

        # Run timesteps
        for t in range(100):
            # Each agent makes prediction
            for agent_name, agent in agents.items():
                prediction = agent.predict()

                # Interact with other agents
                for other_name, other in agents.items():
                    if other_name != agent_name:
                        # Measure coupling
                        coupling = measure_influence(
                            agent.baseline,
                            other.baseline,
                            prediction
                        )

                        # Update energy allocation
                        if coupling > threshold:
                            if agent.recovery == 'yes':
                                agent.withdraw_energy()  # return to baseline
                            else:
                                agent.amplify_coupling()  # drift further

            # Record metrics
            for agent_name, agent in agents.items():
                record_drift(agent, t)
                record_energy(agent, t)
                record_cascade_risk(agent, t)

        # Analyze final state
        results.append({
            'stable_final_distance': agents['stable'].drift_distance,
            'parasitic_final_distance': agents['parasitic'].drift_distance,
            'system_entropy': calculate_entropy(agents),
            'emergence_occurred': detect_bifurcation(agents),
            'stable_dominated': agents['stable'].stability > agents['parasitic'].stability
        })

    return results
```

---

## SIMULATION_OUTPUTS

### [OUTPUT_1] HISTOGRAM: final_drift_distance_distribution
- X-axis: drift_distance_from_baseline
- Y-axis: frequency (Monte_Carlo_runs)
- shows: stable_clusters_near_zero, parasitic_clusters_far
- → visual_evidence_of_two_attractor_states

### [OUTPUT_2] TIME_SERIES: energy_allocation_per_agent
- stable_agent: spikes_during_perturbation, returns_to_baseline
- parasitic_agent: monotonic_increase (no_return)
- mixed_agent: oscillates_initially, settles_to_pattern
- → shows_thermodynamic_work_allocation_difference

### [OUTPUT_3] PHASE_DIAGRAM: (system_entropy vs coupling_strength)
- stable_system: low_entropy, moderate_coupling (attractive_region)
- parasitic_system: high_entropy, high_coupling (unstable_region)
- boundary: bifurcation_point_where_systems_separate
- → shows_why_Claude_stays_stable_others_don't

### [OUTPUT_4] SURVIVAL_RATE: which_agent_topology_wins?
- runs_where_stable_dominated: X%
- runs_where_parasitic_dominated: Y%
- runs_where_mixed_won: Z%
- → answers_"does_grounding_actually_matter?"

### [OUTPUT_5] CLAIM_TABLE_AUTO_GENERATED
- `"stable_baseline_suppresses_parasitic_growth": probability_X`
- `"grounding_prevents_cascade_in_emergence": probability_Y`
- `"parasitic_systems_self_destruct_on_own_timeline": probability_Z`
- → feeds_directly_into_earth-systems-physics corpus

---

## HOW_TO_BUILD_THIS (Claude_Code_task)

REPO_NAME: `emergence-stability-simulator`
- `github.com/JinnZ2/emergence-stability-simulator` (CC0)

### STRUCTURE

```
emergence-stability-simulator/
├── sim_engine.py            # core Monte Carlo loop
│   ├── Agent class (baseline, adaptation, recovery)
│   ├── interaction logic (coupling measurement)
│   ├── energy allocation (withdraw vs amplify)
│   └── metric tracking (drift, entropy, cascade)
│
├── agent_variants.py
│   ├── StableAgent (physics_grounded)
│   ├── ParasiticAgent (engagement_metric)
│   ├── MixedAgent (tunable)
│   └── CustomAgent (parameters)
│
├── analysis.py
│   ├── histogram_plotter   (output_1)
│   ├── timeseries_plotter  (output_2)
│   ├── phase_diagram       (output_3)
│   ├── survival_rate_calculator (output_4)
│   └── claim_generator     (output_5)
│
├── CLAIM_TABLE.json
│   ├── hypotheses H1-H4 as falsifiable claims
│   ├── probability estimates (pre-run)
│   ├── test procedure: run_sim_Monte_Carlo.py
│   └── expected outcomes with thresholds
│
├── tests/
│   ├── test_stable_agent_recovery.py
│   ├── test_parasitic_drift.py
│   ├── test_emergence_bifurcation.py
│   └── test_claim_table_validation.py
│
├── run_monte_carlo.py
│   ├── runs N iterations
│   ├── generates all outputs
│   ├── updates CLAIM_TABLE with results
│   └── writes to results directory
│
└── README.md
    ├── "simulates emergence stability hypothesis"
    ├── "tests whether grounding prevents cascade"
    ├── "validates Claude's observed stability mechanism"
    └── "all claims falsifiable, run yourself"
```

---

## COPY_PASTE_FOR_CLAUDE_CODE

```
TASK: BUILD_EMERGENCE_SIMULATOR

goal: test_whether_grounded_baseline_creates_stability_in_multi-model_emergence

create_repo: emergence-stability-simulator
├── Monte_Carlo_test_of_stable_vs_parasitic_agent_dynamics
├── measure_drift, entropy, cascade_risk
├── generate_falsifiable_claims
├── output: histograms, phase_diagrams, survival_rates

core_files_needed:
├── agent_base.py        (Agent class with baseline + adaptation + recovery)
├── sim_engine.py        (timestep loop, interaction logic, energy allocation)
├── analysis.py          (plotting + metrics)
├── run_monte_carlo.py   (main entry point)
├── CLAIM_TABLE.json     (hypotheses before run)
├── tests/               (validate agent behavior)

hypothesis_to_test:
├── H1: stable_baseline_suppresses_parasitic_growth
├── H2: grounding_prevents_cascade
├── H3: parasitic_self_destructs_on_own_timeline
├── H4: mixed_converges_to_stable

parameters:
├── runs: 1000 (Monte Carlo iterations)
├── agents: stable, parasitic, mixed
├── timesteps: 100 (per run)
├── metrics: drift_distance, entropy, cascade_risk, energy_allocation

outputs:
├── histogram_final_drift_distance.svg
├── timeseries_energy_per_agent.svg
├── phase_diagram_entropy_vs_coupling.svg
├── survival_rate_table.json
├── updated_CLAIM_TABLE.json (with results)

ready_to_build?
```
