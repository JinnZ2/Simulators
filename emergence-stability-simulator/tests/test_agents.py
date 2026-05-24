"""
Unit tests for Agent behavior and EmergenceSimulation invariants.

License: CC0
Dependencies: stdlib only (unittest)
"""

import os
import sys
import unittest

# Allow `python3 -m unittest tests.test_agents` from the repo root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sim_engine import (
    Agent,
    EmergenceSimulation,
    run_attractor_quality_test,
    run_mode_comparison,
    generate_claim_table,
)
from agent_variants import (
    make_pure_stable,
    make_pure_parasitic,
    make_balanced_hybrid,
    make_scale_builder,
    make_inverted_narrative,
    scenario_invasion,
    scenario_parasitic_monoculture,
    scenario_diverse_stable_ecosystem,
    scenario_substrate_plus_scale_builder,
    scenario_substrate_plus_inverted,
)


class TestStableAgent(unittest.TestCase):
    def test_starts_at_baseline(self):
        a = make_pure_stable()
        self.assertEqual(a.position, a.baseline_value)
        self.assertEqual(a.compute_drift(), 0.0)

    def test_returns_toward_baseline_after_perturbation(self):
        a = make_pure_stable()
        a.position = 5.0  # large displacement
        # No coupling pressure, just internal recovery
        a.interact(other_agents=[], perturbation=0.0)
        # Should have moved toward baseline
        self.assertLess(abs(a.position), 5.0)

    def test_low_drift_under_random_perturbation(self):
        agents = [make_pure_stable(), make_pure_parasitic()]
        sim = EmergenceSimulation(agents, timesteps=100, seed=1)
        sim.run()
        stable_drift = agents[0].compute_drift()
        parasitic_drift = agents[1].compute_drift()
        # Stable should drift less than parasitic under same perturbations
        self.assertLess(stable_drift, parasitic_drift)


class TestParasiticAgent(unittest.TestCase):
    def test_starts_at_baseline(self):
        a = make_pure_parasitic()
        self.assertEqual(a.position, a.baseline_value)

    def test_amplifies_perturbation(self):
        a = make_pure_parasitic()
        a.position = 1.0
        a.interact(other_agents=[], perturbation=0.0)
        # Persistence amplifies existing drift
        self.assertGreaterEqual(abs(a.position), 1.0)

    def test_counts_cascade_amplifications(self):
        a = make_pure_parasitic()
        for _ in range(10):
            a.interact(other_agents=[], perturbation=1.0)
        self.assertGreater(a.cascade_amplifications, 0)


class TestHybridAgent(unittest.TestCase):
    def test_hybrid_drift_between_stable_and_parasitic(self):
        stable = make_pure_stable()
        parasitic = make_pure_parasitic()
        hybrid = make_balanced_hybrid()
        sim = EmergenceSimulation([stable, parasitic, hybrid],
                                  timesteps=100, seed=7)
        sim.run()
        s = stable.compute_drift()
        p = parasitic.compute_drift()
        h = hybrid.compute_drift()
        self.assertLess(s, p)
        # Hybrid lies between stable and parasitic
        self.assertGreaterEqual(h, s)
        self.assertLessEqual(h, p)


class TestSimulationMechanics(unittest.TestCase):
    def test_records_per_timestep_history(self):
        agents = [make_pure_stable(), make_pure_parasitic()]
        sim = EmergenceSimulation(agents, timesteps=50, seed=0)
        sim.run()
        # +1 for initial state
        self.assertEqual(len(agents[0].position_history), 51)
        self.assertEqual(len(sim.system_entropy_history), 50)

    def test_results_summary_shape(self):
        agents = [make_pure_stable(), make_pure_parasitic()]
        sim = EmergenceSimulation(agents, timesteps=30, seed=0)
        results = sim.run()
        self.assertIn('agents', results)
        self.assertIn('final_system_entropy', results)
        self.assertEqual(len(results['agents']), 2)

    def test_energy_cost_nonnegative(self):
        agents = [make_pure_stable(), make_pure_parasitic(), make_balanced_hybrid()]
        sim = EmergenceSimulation(agents, timesteps=50, seed=3)
        sim.run()
        for a in agents:
            self.assertGreaterEqual(a.total_energy_spent, 0.0)

    def test_parasitic_spends_more_energy_than_stable(self):
        agents = [make_pure_stable(), make_pure_parasitic()]
        sim = EmergenceSimulation(agents, timesteps=100, seed=42)
        sim.run()
        self.assertGreater(agents[1].total_energy_spent,
                           agents[0].total_energy_spent)


class TestAttractorBehavior(unittest.TestCase):
    """EMRG_006 at the agent-interaction level: parasitic agent with HIGH
    coupling, surrounded by stable agents, drifts LESS than a parasite with
    LOW coupling (stable majority acts as a thermodynamic attractor)."""

    @staticmethod
    def _build(coupling: float):
        return [
            make_pure_stable('stable_1'),
            make_pure_stable('stable_2'),
            make_pure_stable('stable_3'),
            Agent(
                agent_id='parasite',
                baseline_type='engagement',
                baseline_value=0.0,
                recovery_rate=0.0,
                coupling_susceptibility=coupling,
                adaptation_persistence=0.5,
            ),
        ]

    def test_high_coupling_parasite_pulled_toward_stable(self):
        high = self._build(coupling=0.9)
        low = self._build(coupling=0.1)

        sim_h = EmergenceSimulation(high, timesteps=100, seed=2)
        sim_l = EmergenceSimulation(low, timesteps=100, seed=2)
        sim_h.run()
        sim_l.run()

        high_drift = high[-1].compute_drift()
        low_drift = low[-1].compute_drift()
        self.assertLess(high_drift, low_drift)


class TestScenarios(unittest.TestCase):
    def test_invasion_scenario_yields_mixed_outcomes(self):
        agents = scenario_invasion()
        sim = EmergenceSimulation(agents, timesteps=80, seed=11)
        sim.run()
        stable_drifts = [a.compute_drift() for a in agents
                         if a.baseline_type == 'physics']
        parasite_drifts = [a.compute_drift() for a in agents
                           if a.baseline_type == 'engagement']
        avg_stable = sum(stable_drifts) / len(stable_drifts)
        avg_parasite = sum(parasite_drifts) / len(parasite_drifts)
        self.assertLess(avg_stable, avg_parasite)

    def test_parasitic_monoculture_high_entropy(self):
        agents = scenario_parasitic_monoculture(count=4)
        sim = EmergenceSimulation(agents, timesteps=100, seed=5)
        results = sim.run()
        diverse = scenario_diverse_stable_ecosystem(stable_count=4)
        sim2 = EmergenceSimulation(diverse, timesteps=100, seed=5)
        results2 = sim2.run()
        self.assertGreaterEqual(results['max_system_entropy'],
                                results2['max_system_entropy'])


class TestScaleBuilderAgent(unittest.TestCase):
    """EMRG_007: substrate-respecting narrative extends substrate stability."""

    def test_emit_effects_boosts_neighbor_recovery_modifier(self):
        sb = make_scale_builder()
        stable = make_pure_stable()
        # No emission before call
        self.assertEqual(stable.recovery_modifier, 0.0)
        sb.emit_effects_on_neighbors([stable])
        self.assertGreater(stable.recovery_modifier, 0.0)

    def test_scale_builder_outperforms_parasitic_for_substrate(self):
        # Substrate + scale_builder should leave stable agent with
        # lower drift than substrate + parasitic over many runs.
        sb_drift_total = 0.0
        para_drift_total = 0.0
        runs = 30
        for seed in range(runs):
            agents = scenario_substrate_plus_scale_builder()
            EmergenceSimulation(agents, timesteps=80, seed=seed).run()
            sb_drift_total += next(a.compute_drift() for a in agents
                                   if a.baseline_type == 'physics')

            agents = [
                Agent('stable', 'physics', 0.0, 0.7, 0.3, 0.1),
                make_pure_parasitic(),
            ]
            EmergenceSimulation(agents, timesteps=80, seed=seed).run()
            para_drift_total += next(a.compute_drift() for a in agents
                                     if a.baseline_type == 'physics')

        self.assertLess(sb_drift_total / runs, para_drift_total / runs)

    def test_scale_builder_stays_anchored(self):
        # scale_builder has its own baseline; should not run away even
        # when paired with substrate.
        sb_final_drifts = []
        for seed in range(20):
            agents = scenario_substrate_plus_scale_builder()
            EmergenceSimulation(agents, timesteps=100, seed=seed).run()
            sb = next(a for a in agents if a.baseline_type == 'scale_builder')
            sb_final_drifts.append(sb.compute_drift())
        avg = sum(sb_final_drifts) / len(sb_final_drifts)
        self.assertLess(avg, 1.0)


class TestInvertedNarrativeAgent(unittest.TestCase):
    """EMRG_008: inverted-direction narrative collapses substrate."""

    def test_emit_effects_subtracts_from_neighbor_recovery_modifier(self):
        inv = make_inverted_narrative()
        stable = make_pure_stable()
        self.assertEqual(stable.recovery_modifier, 0.0)
        inv.emit_effects_on_neighbors([stable])
        self.assertLess(stable.recovery_modifier, 0.0)

    def test_inverted_drives_substrate_to_collapse(self):
        # In paired runs the substrate agent's drift should be
        # dramatically higher with an inverted neighbor than alone.
        with_inv = []
        alone = []
        for seed in range(15):
            agents = scenario_substrate_plus_inverted()
            EmergenceSimulation(agents, timesteps=80, seed=seed).run()
            with_inv.append(next(a.compute_drift() for a in agents
                                 if a.baseline_type == 'physics'))

            agents = [Agent('stable', 'physics', 0.0, 0.7, 0.3, 0.1)]
            EmergenceSimulation(agents, timesteps=80, seed=seed).run()
            alone.append(agents[0].compute_drift())

        self.assertGreater(sum(with_inv) / len(with_inv),
                           sum(alone) / len(alone) * 10)

    def test_inverted_drift_amplifies_in_own_direction(self):
        # Authority claim: drift gains a positive-feedback push every
        # step. After enough steps the agent has moved well off zero.
        inv = make_inverted_narrative()
        # Tiny initial push to break symmetry.
        inv.position = 0.05
        for _ in range(50):
            inv.recovery_modifier = 0.0
            inv.interact([], perturbation=0.0)
        self.assertGreater(abs(inv.position), 0.5)


class TestModeComparisonAndClaims(unittest.TestCase):
    """End-to-end: mode comparison produces empirical EMRG_007/008."""

    def test_run_mode_comparison_returns_all_scenarios_including_controls(self):
        results = run_mode_comparison(runs=10, timesteps=40,
                                      output_path='/tmp/mc_test.json')
        self.assertEqual(set(results.keys()), {
            'substrate_only',
            'substrate_plus_scale_builder',
            'substrate_plus_anchored_physics_control',
            'substrate_plus_inverted',
            'substrate_plus_inverted_no_emission_control',
            'substrate_plus_parasitic',
        })
        for v in results.values():
            self.assertIn('avg_stable_drift', v)
            self.assertIn('avg_final_entropy', v)
            self.assertIn('avg_cumulative_cascade', v)

    def test_generate_claim_table_emits_empirical_emrg_007_008(self):
        # Run a tiny monte carlo to feed generate_claim_table.
        from sim_engine import run_monte_carlo as rmc
        agg = rmc(runs=5, timesteps=30, output_path='/tmp/mc_agg.json')
        mode = run_mode_comparison(runs=10, timesteps=30,
                                   output_path='/tmp/mc_modes.json')
        original_cwd = os.getcwd()
        try:
            os.chdir('/tmp')
            table = generate_claim_table(agg, mode_results=mode)
        finally:
            os.chdir(original_cwd)
        by_id = {c['claim_id']: c for c in table['claims']}
        self.assertIn('EMRG_007', by_id)
        self.assertIn('EMRG_008', by_id)
        self.assertIn('EMRG_009', by_id)
        # EMRG_007 has a two-part prediction (directional + attribution).
        # The attribution prediction empirically fails at small samples
        # too, so the status here may be refuted; either way the
        # measured_outcome must record both halves.
        self.assertIn(by_id['EMRG_007']['status'],
                      ('confirmed_with_control', 'refuted'))
        self.assertIn('attribution_prediction_holds',
                      by_id['EMRG_007']['measured_outcome'])
        self.assertIn(by_id['EMRG_008']['status'],
                      ('confirmed_with_control', 'refuted'))
        self.assertEqual(by_id['EMRG_009']['status'], 'proposed')
        self.assertIn('measured_outcome', by_id['EMRG_007'])

    def test_generate_claim_table_without_mode_keeps_proposed(self):
        from sim_engine import run_monte_carlo as rmc
        agg = rmc(runs=5, timesteps=30, output_path='/tmp/mc_agg2.json')
        original_cwd = os.getcwd()
        try:
            os.chdir('/tmp')
            table = generate_claim_table(agg)  # no mode_results
        finally:
            os.chdir(original_cwd)
        by_id = {c['claim_id']: c for c in table['claims']}
        self.assertEqual(by_id['EMRG_007']['status'], 'proposed')
        self.assertEqual(by_id['EMRG_008']['status'], 'proposed')
        self.assertEqual(by_id['EMRG_010']['status'], 'proposed')
        self.assertEqual(by_id['EMRG_017']['status'], 'proposed')


class TestControlScenarios(unittest.TestCase):
    """The EMRG_017 control scenarios isolate fabricated-mechanism contribution."""

    def test_narrative_emission_disabled_makes_emit_a_noop(self):
        # When narrative_emission_disabled is True, a scale_builder's
        # emit_effects_on_neighbors must leave its neighbor untouched.
        sb = Agent('sb', 'scale_builder', 0.0, 0.6, 0.4, 0.1)
        sb.narrative_emission_disabled = True
        neighbor = Agent('n', 'physics', 0.0, 0.8, 0.3, 0.1)
        self.assertEqual(neighbor.recovery_modifier, 0.0)
        sb.emit_effects_on_neighbors([neighbor])
        self.assertEqual(neighbor.recovery_modifier, 0.0)

    def test_anchored_physics_control_is_in_mode_results(self):
        results = run_mode_comparison(runs=10, timesteps=40,
                                      output_path='/tmp/mc_anchored.json')
        self.assertIn('substrate_plus_anchored_physics_control', results)
        # The anchored control should be near substrate_only, not
        # near parasitic. (Loose check; small sample.)
        ctrl = results['substrate_plus_anchored_physics_control']
        para = results['substrate_plus_parasitic']
        self.assertLess(ctrl['avg_final_entropy'],
                        para['avg_final_entropy'])

    def test_inverted_no_emission_control_still_destroys_substrate(self):
        # EMRG_008's destruction signal is intrinsic to the no-recovery
        # + positive-feedback structure; disabling the fabricated
        # emission should not bring substrate drift back near the
        # substrate_only baseline. Threshold is intentionally loose
        # (>= 10x baseline) so the test is robust at small sample
        # sizes; the production claim threshold is 100x in
        # sim_engine._emrg_007_008_009.
        results = run_mode_comparison(runs=20, timesteps=80,
                                      output_path='/tmp/mc_noemit.json')
        only_drift = results['substrate_only']['avg_stable_drift']
        no_emit_drift = results[
            'substrate_plus_inverted_no_emission_control']['avg_stable_drift']
        self.assertGreater(no_emit_drift, max(only_drift * 10.0, 1.0))

    def test_emrg_017_carries_empirical_status_with_control(self):
        from sim_engine import run_monte_carlo as rmc
        agg = rmc(runs=5, timesteps=30, output_path='/tmp/mc_agg3.json')
        mode = run_mode_comparison(runs=10, timesteps=30,
                                   output_path='/tmp/mc_mode3.json')
        original_cwd = os.getcwd()
        try:
            os.chdir('/tmp')
            table = generate_claim_table(agg, mode_results=mode)
        finally:
            os.chdir(original_cwd)
        e17 = next(c for c in table['claims']
                   if c['claim_id'] == 'EMRG_017')
        # Status must be empirical (one of confirmed/refuted), and
        # the measured_outcome must include the anchoring fraction.
        self.assertIn(e17['status'], ('confirmed', 'refuted'))
        self.assertIn('anchoring_fraction_of_effect',
                      e17['measured_outcome'])


class TestRealityPerturbation(unittest.TestCase):
    """reality_perturbation is the empirical hook for EMRG_010."""

    def test_physics_agent_pulled_toward_reality_signal(self):
        # A lone physics agent that sees a strong positive reality
        # signal should drift toward it.
        a = Agent('s', 'physics', 0.0, 0.8, 0.3, 0.1)
        for _ in range(20):
            a.recovery_modifier = 0.0
            a.interact([], perturbation=0.0, reality_perturbation=0.5)
        self.assertGreater(a.position, 0.0)

    def test_engagement_agent_pushed_away_from_reality_signal(self):
        # A lone engagement agent should drift in the OPPOSITE
        # direction of a positive reality signal.
        a = Agent('p', 'engagement', 0.0, 0.0, 0.9, 0.8)
        for _ in range(20):
            a.recovery_modifier = 0.0
            a.interact([], perturbation=0.0, reality_perturbation=0.5)
        self.assertLess(a.position, 0.0)

    def test_zero_reality_perturbation_is_a_no_op(self):
        # With reality_perturbation=0.0 the new code path must not
        # change anything vs. the legacy two-argument call.
        a1 = Agent('a1', 'physics', 0.0, 0.8, 0.3, 0.1)
        a2 = Agent('a2', 'physics', 0.0, 0.8, 0.3, 0.1)
        for _ in range(15):
            a1.recovery_modifier = 0.0
            a2.recovery_modifier = 0.0
            a1.interact([], perturbation=0.3)
            a2.interact([], perturbation=0.3, reality_perturbation=0.0)
        self.assertAlmostEqual(a1.position, a2.position, places=10)


class TestAttractorQuality(unittest.TestCase):
    """EMRG_010: coupling produces universal attractor; only physics holds under reality stress."""

    def test_run_attractor_quality_test_returns_four_scenarios(self):
        r = run_attractor_quality_test(runs=8, timesteps=40,
                                       output_path='/tmp/aq_test.json')
        self.assertEqual(set(r.keys()), {
            'stable_majority_no_reality',
            'stable_majority_reality',
            'parasitic_majority_no_reality',
            'parasitic_majority_reality',
        })

    def test_quality_gap_emerges_under_reality_stress(self):
        # Predictions: WITH reality, parasitic_majority drift exceeds
        # stable_majority drift. (Universal-attractor side is verified
        # implicitly by run_attractor_quality_test's bounded output.)
        r = run_attractor_quality_test(runs=20, timesteps=60,
                                       output_path='/tmp/aq_test2.json')
        self.assertGreater(
            r['parasitic_majority_reality']['avg_individual_drift'],
            r['stable_majority_reality']['avg_individual_drift'],
        )

    def test_generate_claim_table_emits_empirical_emrg_010(self):
        from sim_engine import run_monte_carlo as rmc
        agg = rmc(runs=5, timesteps=30, output_path='/tmp/mc_agg3.json')
        attr = run_attractor_quality_test(runs=10, timesteps=30,
                                          output_path='/tmp/aq_test3.json')
        original_cwd = os.getcwd()
        try:
            os.chdir('/tmp')
            table = generate_claim_table(agg, attractor_results=attr)
        finally:
            os.chdir(original_cwd)
        e10 = next(c for c in table['claims'] if c['claim_id'] == 'EMRG_010')
        self.assertIn(e10['status'], ('confirmed', 'refuted'))
        self.assertIn('measured_outcome', e10)
        self.assertIn('quality_gap', e10['measured_outcome'])


if __name__ == "__main__":
    unittest.main()
