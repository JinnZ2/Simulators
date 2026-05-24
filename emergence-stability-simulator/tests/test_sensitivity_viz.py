"""
Tests for sensitivity_viz ASCII renderers and full-report generation.

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

from sensitivity_viz import (
    ascii_correlation_bar,
    ascii_table,
    ascii_line_plot,
    ascii_dual_line_plot,
    visualize_sweep,
    visualize_claim,
    visualize_all_claims,
    detect_direction_reversal,
    visualize_reversal,
    generate_full_report,
)


class TestCorrelationBar(unittest.TestCase):
    def test_positive_strong(self):
        out = ascii_correlation_bar(0.9)
        self.assertIn("+0.900", out)
        self.assertIn("strong positive", out)

    def test_negative_strong(self):
        out = ascii_correlation_bar(-0.9)
        self.assertIn("-0.900", out)
        self.assertIn("strong negative", out)

    def test_clamped_above_one(self):
        out = ascii_correlation_bar(5.0)
        self.assertIn("+1.000", out)

    def test_negligible(self):
        out = ascii_correlation_bar(0.05)
        self.assertIn("negligible", out)


class TestAsciiTable(unittest.TestCase):
    def test_renders_headers_and_rows(self):
        out = ascii_table(['a', 'b'], [['1', '2'], ['3', '4']])
        self.assertIn('a', out)
        self.assertIn('b', out)
        self.assertIn('1', out)
        self.assertIn('4', out)

    def test_empty_rows(self):
        self.assertEqual(ascii_table(['a'], []), "(no data)")


class TestLinePlots(unittest.TestCase):
    def test_line_plot_returns_string(self):
        out = ascii_line_plot([0, 1, 2], [1, 2, 3])
        self.assertIsInstance(out, str)
        self.assertGreater(len(out), 0)

    def test_dual_line_plot_includes_legend(self):
        out = ascii_dual_line_plot(
            [0, 1, 2],
            {'a': [1, 2, 3], 'b': [3, 2, 1]},
        )
        self.assertIn('Legend', out)
        self.assertIn('a', out)
        self.assertIn('b', out)

    def test_line_plot_no_data(self):
        self.assertEqual(ascii_line_plot([], []), "(no data)")

    def test_line_plot_length_mismatch(self):
        self.assertEqual(ascii_line_plot([1, 2], [1]), "(length mismatch)")


class TestVisualizeSweep(unittest.TestCase):
    def _build_sweep(self):
        return {
            'param_name': 'stable_recovery_rate',
            'scenario': 'mixed',
            'runs_per_value': 3,
            'sweeps': [
                {'param_value': 0.0, 'stable_avg_drift': 0.10,
                 'parasitic_avg_drift': 0.20, 'drift_ratio': 2.0,
                 'stable_win_rate': 0.5, 'bifurcation_rate': 0.0},
                {'param_value': 1.0, 'stable_avg_drift': 0.01,
                 'parasitic_avg_drift': 0.20, 'drift_ratio': 20.0,
                 'stable_win_rate': 1.0, 'bifurcation_rate': 0.0},
            ],
        }

    def test_visualize_sweep_includes_sections(self):
        out = visualize_sweep(self._build_sweep())
        self.assertIn('PARAMETER SWEEP', out)
        self.assertIn('CORRELATION ANALYSIS', out)
        self.assertIn('DIRECTION ANALYSIS', out)
        self.assertIn('SWEEP TABLE', out)
        self.assertIn('RECOVERY MECHANISM CONFIRMED', out)


class TestVisualizeClaim(unittest.TestCase):
    def test_confirmed_status_marker(self):
        claim = {
            'claim_id': 'EMRG_006',
            'parameter': 'parasitic_coupling_susceptibility',
            'statement': 's', 'prediction': 'p', 'falsification_criteria': 'f',
            'status': 'confirmed', 'probability': 1.0,
            'evidence_strength': 'high',
            'measured_outcome': {
                'correlation_coupling_to_parasitic_drift': -0.8,
            },
        }
        out = visualize_claim(claim)
        self.assertIn('CONFIRMED', out)
        self.assertIn('EMRG_006', out)
        self.assertIn('correlation_coupling_to_parasitic_drift', out)

    def test_context_dependent_marker(self):
        out = visualize_claim({
            'claim_id': 'SENS_003',
            'parameter': 'p', 'statement': 's', 'prediction': 'p',
            'falsification_criteria': 'f', 'status': 'context_dependent',
            'probability': 0.5, 'measured_outcome': {},
        })
        self.assertIn('CONTEXT-DEPENDENT', out)


class TestDirectionReversal(unittest.TestCase):
    def test_reversal_detected(self):
        a = {
            'param_name': 'parasitic_coupling_susceptibility',
            'scenario': 'parasitic_majority',
            'sweeps': [
                {'param_value': 0.2, 'parasitic_avg_drift': 0.1},
                {'param_value': 0.9, 'parasitic_avg_drift': 1.0},
            ],
        }
        b = {
            'param_name': 'parasitic_coupling_susceptibility',
            'scenario': 'stable_majority',
            'sweeps': [
                {'param_value': 0.2, 'parasitic_avg_drift': 1.0},
                {'param_value': 0.9, 'parasitic_avg_drift': 0.1},
            ],
        }
        reversal = detect_direction_reversal(a, b)
        self.assertTrue(reversal['reversal_detected'])
        self.assertGreater(reversal['correlation_a'], 0)
        self.assertLess(reversal['correlation_b'], 0)
        self.assertIn('REVERSAL', visualize_reversal(reversal))

    def test_no_reversal_when_same_direction(self):
        a = {
            'scenario': 'A',
            'sweeps': [{'param_value': 0.0, 'parasitic_avg_drift': 0.1},
                       {'param_value': 1.0, 'parasitic_avg_drift': 0.9}],
        }
        b = {
            'scenario': 'B',
            'sweeps': [{'param_value': 0.0, 'parasitic_avg_drift': 0.2},
                       {'param_value': 1.0, 'parasitic_avg_drift': 0.8}],
        }
        reversal = detect_direction_reversal(a, b)
        self.assertFalse(reversal['reversal_detected'])


class TestGenerateFullReport(unittest.TestCase):
    def test_full_report_writes_and_returns_string(self):
        sample = {
            'timestamp': '2026-05-24T00:00:00',
            'runs_per_value': 3,
            'timesteps': 100,
            'analyses': [{
                'param_name': 'stable_recovery_rate',
                'scenario': 'mixed',
                'runs_per_value': 3,
                'sweeps': [
                    {'param_value': 0.0, 'stable_avg_drift': 0.10,
                     'parasitic_avg_drift': 0.20, 'drift_ratio': 2.0,
                     'stable_win_rate': 0.5, 'bifurcation_rate': 0.0},
                    {'param_value': 1.0, 'stable_avg_drift': 0.01,
                     'parasitic_avg_drift': 0.20, 'drift_ratio': 20.0,
                     'stable_win_rate': 1.0, 'bifurcation_rate': 0.0},
                ],
            }],
            'claims': [{
                'claim_id': 'EMRG_006',
                'parameter': 'parasitic_coupling_susceptibility',
                'statement': 's', 'prediction': 'p',
                'falsification_criteria': 'f', 'status': 'confirmed',
                'probability': 1.0, 'evidence_strength': 'high',
                'measured_outcome': {
                    'correlation_coupling_to_parasitic_drift': -0.8,
                },
            }],
        }

        with tempfile.TemporaryDirectory() as tmp:
            results_path = Path(tmp) / 'sensitivity_analysis.json'
            output_path = Path(tmp) / 'report.txt'
            results_path.write_text(json.dumps(sample))

            report = generate_full_report(
                results_path=str(results_path),
                output_path=str(output_path),
            )
            self.assertTrue(output_path.exists())
            self.assertIn('FULL REPORT', report)
            self.assertIn('THERMODYNAMIC ATTRACTOR', report)
            self.assertIn('EMRG_006', report)

    def test_missing_results_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / 'nope.json'
            out = generate_full_report(
                results_path=str(missing),
                output_path=str(Path(tmp) / 'r.txt'),
            )
            self.assertIn('not found', out)


if __name__ == "__main__":
    unittest.main()
