"""
Tests for sensitivity_analysis sweeps and generated claims.

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

from sensitivity_analysis import (
    parameter_sweep,
    generate_sensitivity_claims,
    generate_sensitivity_report,
    compute_correlation,
    PARAMETER_REGISTRY,
)


class TestParameterSweepShape(unittest.TestCase):
    def test_sweep_returns_one_entry_per_value(self):
        results = parameter_sweep(
            'stable_recovery_rate',
            [0.0, 0.5, 1.0],
            runs_per_value=3,
        )
        self.assertEqual(results['param_name'], 'stable_recovery_rate')
        self.assertEqual(results['scenario'], 'mixed')
        self.assertEqual(len(results['sweeps']), 3)
        for sweep in results['sweeps']:
            for key in ('param_value', 'stable_avg_drift', 'parasitic_avg_drift',
                        'hybrid_avg_drift', 'drift_ratio', 'stable_win_rate',
                        'parasitic_win_rate', 'bifurcation_rate',
                        'avg_energy_stable', 'avg_energy_parasitic', 'n_runs'):
                self.assertIn(key, sweep)

    def test_unknown_parameter_is_skipped(self):
        results = parameter_sweep('not_a_param', [0.0, 1.0], runs_per_value=2)
        self.assertEqual(results['sweeps'], [])
        self.assertEqual(results['scenario'], 'unknown_parameter')
        self.assertIn('error', results)

    def test_parasitic_coupling_uses_stable_majority(self):
        results = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.2, 0.8],
            runs_per_value=2,
        )
        self.assertEqual(results['scenario'], 'stable_majority')

    def test_explicit_scenario_overrides_auto_selection(self):
        # parasitic_coupling auto-selects stable_majority; force mixed.
        results = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.2, 0.8],
            runs_per_value=2,
            scenario='mixed',
        )
        self.assertEqual(results['scenario'], 'mixed')

        # And the inverse: force a non-coupling param into stable_majority.
        results = parameter_sweep(
            'stable_recovery_rate',
            [0.2, 0.8],
            runs_per_value=2,
            scenario='stable_majority',
        )
        self.assertEqual(results['scenario'], 'stable_majority')

    def test_parasitic_majority_scenario_supported(self):
        results = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.2, 0.8],
            runs_per_value=2,
            scenario='parasitic_majority',
        )
        self.assertEqual(results['scenario'], 'parasitic_majority')
        self.assertEqual(len(results['sweeps']), 2)

    def test_coupling_dampens_drift_in_both_majority_scenarios(self):
        # Empirical finding: parasitic_majority does NOT reverse the sign.
        # Coupling reduces drift in both scenarios via synchronization with
        # neighbors; stable neighbors are merely a stronger attractor than
        # parasitic ones. SENS_003 captures this with status='refuted'.
        stable_majority = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.1, 0.3, 0.5, 0.7, 0.9],
            runs_per_value=5,
            scenario='stable_majority',
        )
        parasitic_majority = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.1, 0.3, 0.5, 0.7, 0.9],
            runs_per_value=5,
            scenario='parasitic_majority',
        )
        sm_drifts = [s['parasitic_avg_drift'] for s in stable_majority['sweeps']]
        pm_drifts = [s['parasitic_avg_drift'] for s in parasitic_majority['sweeps']]
        # Both scenarios: drift drops as coupling increases.
        self.assertLess(sm_drifts[-1], sm_drifts[0])
        self.assertLess(pm_drifts[-1], pm_drifts[0])
        # Stable neighbors are a stronger attractor than parasitic ones, so at
        # max coupling the stable_majority residual drift is lower.
        self.assertLess(sm_drifts[-1], pm_drifts[-1])

    def test_sens_003_refuted_when_no_reversal_observed(self):
        # With only same-sign scenarios, SENS_003.status should resolve to
        # 'refuted' (with notes), not the hardcoded 'context_dependent'.
        analyses = [
            parameter_sweep('parasitic_coupling_susceptibility',
                            [0.1, 0.5, 0.9], runs_per_value=3,
                            scenario='stable_majority'),
            parameter_sweep('parasitic_coupling_susceptibility',
                            [0.1, 0.5, 0.9], runs_per_value=3,
                            scenario='parasitic_majority'),
        ]
        claims = generate_sensitivity_claims({'analyses': analyses})
        sens = next(c for c in claims if c['claim_id'] == 'SENS_003')
        self.assertEqual(sens['status'], 'refuted')
        self.assertIn('per_scenario', sens['measured_outcome'])
        self.assertIn('stable_majority', sens['measured_outcome']['per_scenario'])
        self.assertIn('parasitic_majority', sens['measured_outcome']['per_scenario'])


class TestMonotonicTrends(unittest.TestCase):
    def test_higher_recovery_rate_reduces_stable_drift(self):
        results = parameter_sweep(
            'stable_recovery_rate',
            [0.0, 1.0],
            runs_per_value=6,
        )
        low, high = results['sweeps'][0], results['sweeps'][1]
        self.assertLessEqual(high['stable_avg_drift'], low['stable_avg_drift'])

    def test_higher_parasitic_persistence_increases_parasitic_drift(self):
        results = parameter_sweep(
            'parasitic_adaptation_persistence',
            [0.0, 1.0],
            runs_per_value=6,
        )
        low, high = results['sweeps'][0], results['sweeps'][1]
        self.assertGreaterEqual(high['parasitic_avg_drift'],
                                low['parasitic_avg_drift'])


class TestCorrelationHelper(unittest.TestCase):
    def test_perfect_positive_correlation(self):
        self.assertAlmostEqual(compute_correlation([1, 2, 3], [2, 4, 6]), 1.0)

    def test_perfect_negative_correlation(self):
        self.assertAlmostEqual(compute_correlation([1, 2, 3], [6, 4, 2]), -1.0)

    def test_degenerate_inputs_return_zero(self):
        self.assertEqual(compute_correlation([], []), 0.0)
        self.assertEqual(compute_correlation([1], [2]), 0.0)
        self.assertEqual(compute_correlation([1, 2, 3], [5, 5, 5]), 0.0)


class TestSensitivityClaims(unittest.TestCase):
    def test_claims_generated_with_required_fields(self):
        results = {
            'analyses': [
                parameter_sweep('stable_recovery_rate', [0.0, 0.5, 1.0],
                                runs_per_value=3),
                parameter_sweep('parasitic_coupling_susceptibility',
                                [0.2, 0.6, 1.0], runs_per_value=3),
                parameter_sweep('parasitic_adaptation_persistence',
                                [0.2, 0.8], runs_per_value=3),
            ]
        }
        claims = generate_sensitivity_claims(results)
        self.assertGreater(len(claims), 0)
        for c in claims:
            for key in ('claim_id', 'statement', 'falsification_criteria',
                        'status', 'measurement_method', 'measured_outcome'):
                self.assertIn(key, c)
            self.assertTrue(c['claim_id'].startswith('SENS_')
                            or c['claim_id'].startswith('EMRG_'))


class TestThermodynamicAttractorClaim(unittest.TestCase):
    """EMRG_006: parasitic_coupling inversely correlates with parasitic_drift
    when surrounded by stable agents (stable_majority scenario)."""

    def test_emrg_006_emitted_when_coupling_sweep_present(self):
        results = {
            'analyses': [
                parameter_sweep('parasitic_coupling_susceptibility',
                                [0.2, 0.6, 1.0], runs_per_value=4),
            ]
        }
        claims = generate_sensitivity_claims(results)
        ids = {c['claim_id'] for c in claims}
        self.assertIn('EMRG_006', ids)
        self.assertIn('SENS_003', ids)

    def test_dual_scenario_emits_one_emrg_006_and_one_sens_003(self):
        stable_majority = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.1, 0.5, 0.9], runs_per_value=3,
            scenario='stable_majority',
        )
        mixed = parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.1, 0.5, 0.9], runs_per_value=3,
            scenario='mixed',
        )
        claims = generate_sensitivity_claims({'analyses': [stable_majority, mixed]})
        ids = [c['claim_id'] for c in claims]
        # Exactly one of each — no duplicates from the two analyses.
        self.assertEqual(ids.count('SENS_003'), 1)
        self.assertEqual(ids.count('EMRG_006'), 1)
        # SENS_003 carries per-scenario measurements.
        sens = next(c for c in claims if c['claim_id'] == 'SENS_003')
        per_scen = sens['measured_outcome']['per_scenario']
        self.assertIn('stable_majority', per_scen)
        self.assertIn('mixed', per_scen)

    def test_emrg_006_confirmed_with_negative_correlation(self):
        results = {
            'analyses': [
                parameter_sweep('parasitic_coupling_susceptibility',
                                [0.1, 0.3, 0.5, 0.7, 0.9], runs_per_value=6),
            ]
        }
        claims = generate_sensitivity_claims(results)
        emrg = next(c for c in claims if c['claim_id'] == 'EMRG_006')
        correlation = emrg['measured_outcome']['correlation_coupling_to_parasitic_drift']
        self.assertLess(correlation, 0.0)
        self.assertEqual(emrg['status'], 'confirmed')


class TestSensitivityReport(unittest.TestCase):
    def test_report_renders_param_and_claim_sections(self):
        analysis = parameter_sweep('stable_recovery_rate', [0.0, 1.0],
                                   runs_per_value=2)
        claims = generate_sensitivity_claims({'analyses': [analysis]})
        results = {
            'timestamp': '2026-05-24T00:00:00',
            'runs_per_value': 2,
            'timesteps': 100,
            'analyses': [analysis],
            'claims': claims,
        }
        report = generate_sensitivity_report(results)
        self.assertIn('PARAMETER SENSITIVITY ANALYSIS', report)
        self.assertIn('stable_recovery_rate', report)
        self.assertIn('GENERATED CLAIMS', report)
        self.assertIn('SENS_001', report)

    def test_report_handles_unknown_parameter_sweep(self):
        analysis = parameter_sweep('not_a_param', [0.0, 1.0], runs_per_value=1)
        results = {'analyses': [analysis], 'claims': []}
        report = generate_sensitivity_report(results)
        self.assertIn('not_a_param', report)
        self.assertIn('no sweeps', report)


class TestCli(unittest.TestCase):
    def test_single_param_sweep_via_cli(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'sweep.json'
            result = subprocess.run(
                [sys.executable, 'sensitivity_analysis.py',
                 '--param', 'stable_recovery_rate',
                 '--values', '0.0,1.0',
                 '--runs', '2',
                 '--timesteps', '20',
                 '--output', str(out)],
                cwd=os.path.join(os.path.dirname(__file__), '..'),
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(out.exists())
            data = json.loads(out.read_text())
            self.assertEqual(data['schema_version'], '1.0')
            self.assertEqual(data['source_repo'], 'emergence-stability-simulator')
            self.assertEqual(len(data['analyses']), 1)
            self.assertEqual(data['analyses'][0]['param_name'],
                             'stable_recovery_rate')

    def test_unknown_param_returns_nonzero(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, 'sensitivity_analysis.py',
             '--param', 'not_a_real_param',
             '--runs', '2', '--timesteps', '10'],
            cwd=os.path.join(os.path.dirname(__file__), '..'),
            capture_output=True, text=True, timeout=10,
        )
        self.assertNotEqual(result.returncode, 0)


class TestParameterRegistry(unittest.TestCase):
    def test_registry_covers_three_baseline_types(self):
        baseline_types = {v[0] for v in PARAMETER_REGISTRY.values()}
        self.assertEqual(baseline_types, {'physics', 'engagement', 'hybrid'})

    def test_registry_covers_three_fields_per_type(self):
        for bt in ('physics', 'engagement', 'hybrid'):
            entries = [k for k, v in PARAMETER_REGISTRY.items() if v[0] == bt]
            self.assertEqual(len(entries), 3, f"{bt} should have 3 parameter entries")


if __name__ == "__main__":
    unittest.main()
