"""
Tests for the balance_threshold module and the substrate-exhaustion
mechanics it builds on.

License: CC0
Dependencies: stdlib only (unittest)
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim_engine import Agent, EmergenceSimulation
from balance_threshold import (
    build_balance_scenario,
    test_sustainability,
    ratio_sweep,
    extraction_sweep,
    sustainability_surface,
    scale_builder_amplification_test,
    disruption_resilience_test,
    multi_community_reach_test,
    historical_overlay_test,
    identify_threshold,
    generate_balance_claims,
    run_full_balance_analysis,
)


# ============================================================
# AGENT-LEVEL SUSTAINABILITY MECHANICS
# ============================================================

class TestEnergyBudgetMechanics(unittest.TestCase):
    def test_default_budget_is_infinite_and_no_op(self):
        a = Agent('a', 'physics', 0.0, 0.8, 0.3, 0.1)
        self.assertEqual(a.energy_budget, float('inf'))
        # Many interact steps shouldn't push it off infinity.
        for _ in range(50):
            a.recovery_modifier = 0.0
            a.interact([], perturbation=0.3)
        self.assertEqual(a.energy_budget, float('inf'))
        self.assertFalse(a.exhausted)

    def test_finite_budget_drains_under_extraction(self):
        target = Agent('t', 'physics', 0.0, 0.8, 0.3, 0.1,
                       energy_budget=10.0, regeneration_rate=0.0)
        extractor = Agent('e', 'engagement', 0.0, 0.0, 0.9, 0.8,
                          extraction_rate=2.0)
        extractor.extract_from(target, 2.0)
        self.assertAlmostEqual(target.energy_budget, 8.0)
        self.assertEqual(target.total_extracted_from, 2.0)
        self.assertEqual(extractor.total_extracted_by, 2.0)

    def test_exhaustion_flips_physics_to_engagement(self):
        target = Agent('t', 'physics', 0.0, 0.8, 0.3, 0.1,
                       energy_budget=1.0, regeneration_rate=0.0)
        extractor = Agent('e', 'engagement', 0.0, 0.0, 0.9, 0.8,
                          extraction_rate=5.0)
        extractor.extract_from(target, 5.0)
        self.assertTrue(target.exhausted)
        self.assertEqual(target.baseline_type, 'engagement')
        self.assertEqual(target.recovery_rate, 0.0)
        self.assertEqual(target.energy_budget, 0.0)

    def test_regenerate_caps_at_initial_budget(self):
        a = Agent('a', 'physics', 0.0, 0.8, 0.3, 0.1,
                  energy_budget=10.0, regeneration_rate=3.0)
        a.energy_budget = 5.0
        a.regenerate()
        self.assertAlmostEqual(a.energy_budget, 8.0)
        a.regenerate()  # would go to 11, capped at 10
        self.assertAlmostEqual(a.energy_budget, 10.0)

    def test_scale_builder_does_NOT_contribute_to_substrate_energy(self):
        # Substrate civilizations sustain on their own at adequate
        # ratios -- they do not depend on narrative for survival.
        # Adding a scale_builder must not increase a substrate
        # neighbor's energy budget.
        sb = Agent('sb', 'scale_builder', 0.0, 0.6, 0.4, 0.1)
        target = Agent('t', 'physics', 0.0, 0.8, 0.3, 0.1,
                       energy_budget=10.0, regeneration_rate=0.0)
        target.energy_budget = 5.0
        sb.emit_effects_on_neighbors([target])
        self.assertEqual(target.energy_budget, 5.0)

    def test_contribute_to_neighbor_budget_primitive_still_available(self):
        # The primitive itself remains usable (other code can opt-in)
        # but scale_builder doesn't invoke it.
        sb = Agent('sb', 'scale_builder', 0.0, 0.6, 0.4, 0.1)
        target = Agent('t', 'physics', 0.0, 0.8, 0.3, 0.1,
                       energy_budget=10.0, regeneration_rate=0.0)
        target.energy_budget = 5.0
        actual = sb.contribute_to_neighbor_budget(target, 2.0)
        self.assertAlmostEqual(actual, 2.0)
        self.assertAlmostEqual(target.energy_budget, 7.0)


# ============================================================
# SIMULATION-LEVEL DYNAMICS
# ============================================================

class TestExtractionPhase(unittest.TestCase):
    def test_apply_extraction_no_op_when_no_extractors(self):
        agents = [Agent('a', 'physics', 0.0, 0.8, 0.3, 0.1,
                        energy_budget=10.0, regeneration_rate=1.0),
                  Agent('b', 'engagement', 0.0, 0.0, 0.9, 0.8)]
        sim = EmergenceSimulation(agents, timesteps=10, seed=1)
        sim.run()
        self.assertFalse(agents[0].exhausted)
        self.assertEqual(agents[0].energy_budget, 10.0)

    def test_collapse_timestep_detected_under_heavy_extraction(self):
        agents = build_balance_scenario(
            stable_count=1, parasitic_count=10, extraction_rate=2.0,
        )
        sim = EmergenceSimulation(agents, timesteps=100, seed=2)
        results = sim.run()
        self.assertIsNotNone(results['collapse_timestep'])
        self.assertEqual(results['final_exhausted_count'], 1)


# ============================================================
# BALANCE_THRESHOLD MODULE
# ============================================================

class TestScenarioBuilder(unittest.TestCase):
    def test_builds_agents_with_correct_counts_and_types(self):
        agents = build_balance_scenario(
            stable_count=3, parasitic_count=5, scale_builder_count=2,
            extraction_rate=0.5,
        )
        types = [a.baseline_type for a in agents]
        self.assertEqual(types.count('physics'), 3)
        self.assertEqual(types.count('engagement'), 5)
        self.assertEqual(types.count('scale_builder'), 2)

    def test_stable_agents_have_finite_budget_and_regen(self):
        agents = build_balance_scenario(stable_count=2, parasitic_count=4)
        physics = [a for a in agents if a.baseline_type == 'physics']
        for a in physics:
            self.assertNotEqual(a.energy_budget, float('inf'))
            self.assertGreater(a.regeneration_rate, 0.0)

    def test_parasitic_agents_have_extraction_rate(self):
        agents = build_balance_scenario(stable_count=2, parasitic_count=4,
                                        extraction_rate=0.5)
        parasites = [a for a in agents if a.baseline_type == 'engagement']
        for p in parasites:
            self.assertEqual(p.extraction_rate, 0.5)


class TestSustainabilityTest(unittest.TestCase):
    def test_high_ratio_low_extraction_is_sustainable(self):
        r = test_sustainability(stable_count=10, parasitic_count=5,
                                extraction_rate=0.1, runs=3, timesteps=80)
        self.assertGreater(r['avg_sustainability_score'], 0.5)
        self.assertTrue(r['sustainable'])

    def test_low_ratio_high_extraction_collapses(self):
        r = test_sustainability(stable_count=1, parasitic_count=15,
                                extraction_rate=2.0, runs=3, timesteps=80)
        self.assertGreater(r['collapse_rate'], 0.5)
        self.assertLess(r['avg_sustainability_score'], 0.3)


class TestSweeps(unittest.TestCase):
    def test_ratio_sweep_emits_one_row_per_cell(self):
        r = ratio_sweep(ratios=[0.1, 0.5], total_populations=[10],
                        runs_per_test=2, timesteps=40)
        self.assertEqual(len(r['results']), 2)
        for row in r['results']:
            self.assertIn('avg_sustainability_score', row)
            self.assertIn('stable_ratio', row)

    def test_extraction_sweep_emits_one_row_per_rate(self):
        r = extraction_sweep(extraction_rates=[0.1, 1.0],
                             runs_per_test=2, timesteps=40)
        self.assertEqual(len(r['results']), 2)

    def test_sustainability_surface_is_2d_grid(self):
        r = sustainability_surface(
            ratios=[0.1, 0.3], extraction_rates=[0.5, 1.5],
            runs_per_cell=2, total_population=10, timesteps=40,
        )
        self.assertEqual(len(r['surface']), 4)


class TestThresholdIdentification(unittest.TestCase):
    def test_threshold_curve_is_monotone_under_real_dynamics(self):
        surface = sustainability_surface(
            ratios=[0.1, 0.3, 0.5],
            extraction_rates=[0.2, 1.0, 2.0],
            runs_per_cell=3, total_population=10, timesteps=60,
        )
        thresholds = identify_threshold(surface)
        curve = thresholds['threshold_curve_by_ratio']
        max_extr = [t['max_sustainable_extraction'] for t in curve]
        # Monotone non-decreasing in stable_ratio: substrate that can
        # tolerate extraction at ratio R can also tolerate it at any
        # higher ratio.
        self.assertEqual(sorted(max_extr), max_extr)


class TestScaleBuilderAmplification(unittest.TestCase):
    def test_returns_both_regimes(self):
        r = scale_builder_amplification_test(
            scale_builder_counts=[0, 3], runs_per_test=2, timesteps=50)
        self.assertIn('sustainable_regime', r)
        self.assertIn('unsustainable_regime', r)
        self.assertEqual(len(r['sustainable_regime']['results']), 2)
        self.assertEqual(len(r['unsustainable_regime']['results']), 2)

    def test_scale_builders_reduce_drift_at_sustainable_ratios(self):
        # The honest empirical question: does narrative augmentation
        # reduce drift when substrate already sustains on its own?
        r = scale_builder_amplification_test(
            scale_builder_counts=[0, 5], runs_per_test=4, timesteps=80)
        sust = r['sustainable_regime']['results']
        no_sb = next(x for x in sust if x['scale_builder_count'] == 0)
        with_sb = next(x for x in sust if x['scale_builder_count'] == 5)
        self.assertLess(with_sb['avg_substrate_drift'],
                        no_sb['avg_substrate_drift'])

    def test_scale_builders_do_not_save_unsustainable_scenarios(self):
        # Substrate sustains on its own at adequate ratios; narrative
        # does NOT rescue substrate pushed below the threshold.
        r = scale_builder_amplification_test(
            scale_builder_counts=[0, 5], runs_per_test=3, timesteps=80)
        unsust = r['unsustainable_regime']['results']
        no_sb = next(x for x in unsust if x['scale_builder_count'] == 0)
        with_sb = next(x for x in unsust if x['scale_builder_count'] == 5)
        self.assertGreaterEqual(no_sb['collapse_rate'], 0.5)
        # Adding scale_builders must not dramatically reduce collapse.
        self.assertGreater(with_sb['collapse_rate'], 0.3)


class TestDisruptionResilience(unittest.TestCase):
    def test_scale_builders_accelerate_recovery_from_shock(self):
        r = disruption_resilience_test(
            scale_builder_counts=[0, 5], runs_per_test=4, timesteps=120,
            disruption_timestep=40, disruption_magnitude=2.0,
        )
        no_sb = next(x for x in r['results']
                     if x['scale_builder_count'] == 0)
        with_sb = next(x for x in r['results']
                       if x['scale_builder_count'] == 5)
        # Faster recovery -- fewer timesteps -- with scale_builders.
        self.assertLessEqual(with_sb['avg_timesteps_to_recover'],
                             no_sb['avg_timesteps_to_recover'])


class TestMultiCommunityReach(unittest.TestCase):
    """EMRG_015: scale_builders amplify reach, not survival."""

    def test_without_bridge_communities_diverge(self):
        r = multi_community_reach_test(runs_per_arm=4, timesteps=80,
                                       scale_builder_count=4)
        # Community B drifts on its own consensus when isolated.
        self.assertGreater(r['without_bridge']['avg_cross_community_gap'],
                           r['with_bridge']['avg_cross_community_gap'])

    def test_bridge_closes_cross_community_gap_substantially(self):
        r = multi_community_reach_test(runs_per_arm=4, timesteps=80,
                                       scale_builder_count=4)
        self.assertLess(r['with_bridge']['avg_cross_community_gap'], 5.0)

    def test_emrg_015_emitted_and_confirmed(self):
        r = multi_community_reach_test(runs_per_arm=3, timesteps=80,
                                       scale_builder_count=4)
        claims = generate_balance_claims({'multi_community_reach': r})
        e15 = next((c for c in claims if c['claim_id'] == 'EMRG_015'),
                   None)
        self.assertIsNotNone(e15)
        self.assertEqual(e15['status'], 'confirmed')
        outcome = e15['measured_outcome']
        self.assertIn('gap_without_bridge', outcome)
        self.assertIn('gap_with_bridge', outcome)
        self.assertGreater(outcome['gap_reduction'], 0.0)


class TestHistoricalOverlay(unittest.TestCase):
    def test_pre_industrial_more_sustainable_than_current_estimate(self):
        r = historical_overlay_test(runs_per_test=2, total_population=10,
                                    timesteps=80)
        by_label = {row['historical_label']: row for row in r['results']}
        self.assertIn('pre_industrial_typical', by_label)
        self.assertIn('current_estimate', by_label)
        self.assertGreater(
            by_label['pre_industrial_typical']['avg_sustainability_score'],
            by_label['current_estimate']['avg_sustainability_score'],
        )


class TestClaimGeneration(unittest.TestCase):
    def test_emrg_011_emitted_when_surface_present(self):
        surface = sustainability_surface(
            ratios=[0.1, 0.3, 0.5],
            extraction_rates=[0.2, 1.0, 2.0],
            runs_per_cell=2, total_population=10, timesteps=40,
        )
        claims = generate_balance_claims({'sustainability_surface': surface})
        ids = {c['claim_id'] for c in claims}
        self.assertIn('EMRG_011', ids)

    def test_emrg_012_emitted_when_historical_present(self):
        historical = historical_overlay_test(runs_per_test=2,
                                             total_population=10,
                                             timesteps=40)
        claims = generate_balance_claims({'historical_overlay': historical})
        ids = {c['claim_id'] for c in claims}
        self.assertIn('EMRG_012', ids)

    def test_emrg_013_emitted_when_scale_builder_present(self):
        sb = scale_builder_amplification_test(
            scale_builder_counts=[0, 3], runs_per_test=2, timesteps=40)
        claims = generate_balance_claims({'scale_builder_amplification': sb})
        ids = {c['claim_id'] for c in claims}
        self.assertIn('EMRG_013', ids)

    def test_no_claims_when_no_inputs(self):
        self.assertEqual(generate_balance_claims({}), [])


class TestFullBalanceAnalysis(unittest.TestCase):
    """End-to-end smoke test with very small parameters."""

    def test_run_full_balance_analysis_writes_claim_ready_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'balance.json'
            # Tiny config; we just need shape and writability.
            results = run_full_balance_analysis(
                output_path=str(output),
                runs_per_cell=2,
                timesteps=30,
            )
            self.assertTrue(output.exists())
            data = json.loads(output.read_text())
            self.assertEqual(data['schema_version'], '1.0')
            self.assertEqual(data['source_repo'],
                             'emergence-stability-simulator')
            self.assertIn('claims', data)
            self.assertIn('sustainability_surface', data)
            ids = {c['claim_id'] for c in results['claims']}
            # All four balance claims should be present in a full run.
            self.assertEqual(
                ids, {'EMRG_011', 'EMRG_012', 'EMRG_013', 'EMRG_015'})


if __name__ == '__main__':
    unittest.main()
