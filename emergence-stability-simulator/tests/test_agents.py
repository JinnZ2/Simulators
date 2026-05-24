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

from sim_engine import Agent, EmergenceSimulation
from agent_variants import (
    make_pure_stable,
    make_pure_parasitic,
    make_balanced_hybrid,
    scenario_invasion,
    scenario_parasitic_monoculture,
    scenario_diverse_stable_ecosystem,
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


if __name__ == "__main__":
    unittest.main()
