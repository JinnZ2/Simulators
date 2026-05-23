"""
Tests for sensitivity_analysis sweeps and generated claims.

License: CC0
Dependencies: stdlib only (unittest)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sensitivity_analysis import parameter_sweep, generate_sensitivity_claims


class TestParameterSweepShape(unittest.TestCase):
    def test_sweep_returns_one_entry_per_value(self):
        results = parameter_sweep(
            'stable_recovery_rate',
            [0.0, 0.5, 1.0],
            runs_per_value=3,
        )
        self.assertEqual(len(results['sweeps']), 3)
        for sweep in results['sweeps']:
            for key in ('stable_avg_drift', 'parasitic_avg_drift',
                        'drift_ratio', 'stable_win_rate', 'bifurcation_rate'):
                self.assertIn(key, sweep)

    def test_unknown_parameter_is_skipped(self):
        results = parameter_sweep('not_a_param', [0.0, 1.0], runs_per_value=2)
        self.assertEqual(results['sweeps'], [])


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


class TestSensitivityClaims(unittest.TestCase):
    def test_claims_generated_with_required_fields(self):
        results = {
            'analyses': [
                parameter_sweep('stable_recovery_rate', [0.0, 0.5, 1.0],
                                runs_per_value=3),
                parameter_sweep('parasitic_coupling_susceptibility',
                                [0.4, 0.8], runs_per_value=3),
                parameter_sweep('parasitic_adaptation_persistence',
                                [0.2, 0.8], runs_per_value=3),
            ]
        }
        claims = generate_sensitivity_claims(results)
        self.assertGreater(len(claims), 0)
        for c in claims:
            self.assertIn('claim_id', c)
            self.assertIn('statement', c)
            self.assertIn('falsification_criteria', c)
            self.assertIn('status', c)
            self.assertTrue(c['claim_id'].startswith('SENS_'))


if __name__ == "__main__":
    unittest.main()
