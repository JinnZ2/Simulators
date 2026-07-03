"""
Audit-grade tests for Lε (probabilistic) — Bayesian measurement
envelope + category-error guards.

Pins:

  GL_Le_P001 [PHENOMENON]: Gaussian measurement likelihood under
                             sigma^2 = noise^2 + (resolution/2)^2
  GL_Le_P002 [PHENOMENON]: out-of-range category-error guard
  GL_Le_P003 [PHENOMENON]: non-measuring ontological scope guard
  GL_Le_P004 [PHENOMENON]: inspector is pure
  GL_Le_P_PIN [INSTRUMENT]: canonical measurements pinned

License: CC0
Dependencies: numpy (l_epsilon_epistemic_v2 requires it).
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from l_epsilon_epistemic_v2 import (
    EpistemicInstrument,
    l_epsilon_probabilistic_inspector,
)


class TestGL_Le_P001_GaussianLikelihood(unittest.TestCase):
    """[PHENOMENON] Gaussian shape on measurement error."""

    def _score(self, measured, true):
        return l_epsilon_probabilistic_inspector(
            dict(measured_value=measured,
                 candidate_true_value=true))

    def _sigma(self):
        instr = EpistemicInstrument()
        return math.sqrt(instr.noise_std ** 2
                         + (instr.resolution / 2.0) ** 2)

    def test_self_consistent_measurement_zero_penalty(self):
        r = self._score(25.0, 25.0)
        self.assertFalse(r['category_error'])
        self.assertEqual(r['logp'], 0.0)

    def test_1sigma_error_gives_neg_half(self):
        sigma = self._sigma()
        r = self._score(25.0 + sigma, 25.0)
        self.assertAlmostEqual(r['logp'], -0.5, places=10)

    def test_2sigma_error_gives_neg_2(self):
        sigma = self._sigma()
        r = self._score(25.0 + 2 * sigma, 25.0)
        self.assertAlmostEqual(r['logp'], -2.0, places=10)

    def test_10sigma_error_gives_neg_50(self):
        sigma = self._sigma()
        r = self._score(25.0 + 10 * sigma, 25.0)
        self.assertAlmostEqual(r['logp'], -50.0, places=10)

    def test_quadratic_scaling(self):
        # Doubling error quadruples the penalty magnitude.
        r1 = self._score(26.0, 25.0)
        r2 = self._score(27.0, 25.0)
        self.assertAlmostEqual(r2['logp'], 4.0 * r1['logp'],
                                places=10)

    def test_gap_sigma_matches_closed_form(self):
        r = self._score(25.0, 25.0)
        self.assertAlmostEqual(r['gap_sigma'], self._sigma(),
                                places=10)


class TestGL_Le_P002_OutOfRangeGuard(unittest.TestCase):
    """[PHENOMENON] Out-of-range triggers category error."""

    def test_above_max_returns_category_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=200.0))
        self.assertTrue(r['category_error'])
        self.assertIsNone(r['logp'])
        self.assertFalse(r['measurement_scoped'])

    def test_below_min_returns_category_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=-50.0))
        self.assertTrue(r['category_error'])
        self.assertIsNone(r['logp'])

    def test_within_range_scores_normally(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=50.0, candidate_true_value=50.0))
        self.assertFalse(r['category_error'])
        self.assertEqual(r['logp'], 0.0)

    def test_at_max_boundary_scores(self):
        # At the exact boundary, in-range (inclusive).
        instr = EpistemicInstrument()
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=instr.max_val,
                 candidate_true_value=instr.max_val),
            instrument=instr)
        self.assertFalse(r['category_error'])

    def test_clipping_disabled_no_guard(self):
        # If the instrument has clipping=False, out-of-range values
        # score normally (no range to be out of).
        instr = EpistemicInstrument(clipping=False)
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=200.0, candidate_true_value=200.0),
            instrument=instr)
        self.assertFalse(r['category_error'])
        self.assertEqual(r['logp'], 0.0)

    def test_reason_names_the_range(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=200.0))
        self.assertIn('200', r['reason'])
        self.assertIn('range', r['reason'].lower())


class TestGL_Le_P003_NonMeasuringScopeGuard(unittest.TestCase):
    """[PHENOMENON] Non-measuring scopes trigger category error."""

    def test_pure_abstract_returns_category_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0),
            ontological_scope='pure_abstract')
        self.assertTrue(r['category_error'])
        self.assertIn('pure_abstract', r['reason'])

    def test_symbolic_only_returns_category_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0),
            ontological_scope='symbolic_only')
        self.assertTrue(r['category_error'])

    def test_any_measuring_entity_scores_normally(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0, candidate_true_value=25.0),
            ontological_scope='any_measuring_entity')
        self.assertFalse(r['category_error'])

    def test_ai_silicon_substrate_scores(self):
        # AI has sensors -> can measure -> not in the non-measuring
        # set. Scores normally.
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0, candidate_true_value=25.0),
            ontological_scope='AI_silicon_substrate')
        self.assertFalse(r['category_error'])

    def test_scope_carried_back_on_category_error(self):
        r = l_epsilon_probabilistic_inspector(
            {}, ontological_scope='pure_abstract')
        self.assertEqual(r['ontological_scope'], 'pure_abstract')


class TestGL_Le_P004_Purity(unittest.TestCase):
    """[PHENOMENON] Inspector is pure."""

    def test_two_calls_return_same_result(self):
        instr = EpistemicInstrument()
        claim = dict(measured_value=27.5, candidate_true_value=25.0)
        r1 = l_epsilon_probabilistic_inspector(claim, instrument=instr)
        r2 = l_epsilon_probabilistic_inspector(claim, instrument=instr)
        self.assertEqual(r1['logp'], r2['logp'])
        self.assertEqual(r1['gap_sigma'], r2['gap_sigma'])

    def test_calibration_offset_not_mutated(self):
        instr = EpistemicInstrument()
        before = instr.calibration_offset
        for _ in range(10):
            l_epsilon_probabilistic_inspector(
                dict(measured_value=25.0, candidate_true_value=24.0),
                instrument=instr)
        self.assertEqual(instr.calibration_offset, before)

    def test_frozen_constants_not_mutated(self):
        instr = EpistemicInstrument()
        before = (instr.noise_std, instr.resolution,
                  instr.min_val, instr.max_val)
        l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0, candidate_true_value=25.0),
            instrument=instr)
        after = (instr.noise_std, instr.resolution,
                 instr.min_val, instr.max_val)
        self.assertEqual(before, after)


class TestLeProbabilisticInspectorDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_Le_P_PIN — canonical measurements pinned."""

    def test_self_consistent(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0, candidate_true_value=25.0))
        self.assertEqual(r['logp'], 0.0)

    def test_small_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.5, candidate_true_value=25.0))
        self.assertAlmostEqual(r['logp'], -0.019, delta=0.001)

    def test_moderate_1sigma_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=27.5, candidate_true_value=25.0))
        self.assertAlmostEqual(r['logp'], -0.481, delta=0.002)

    def test_large_10sigma_error(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=50.0, candidate_true_value=25.0))
        self.assertAlmostEqual(r['logp'], -48.08, delta=0.02)

    def test_out_of_range_above(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=200.0))
        self.assertTrue(r['category_error'])

    def test_out_of_range_below(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=-50.0))
        self.assertTrue(r['category_error'])

    def test_symbolic_only_scope(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0),
            ontological_scope='symbolic_only')
        self.assertTrue(r['category_error'])

    def test_no_measured_value_silent_zero(self):
        r = l_epsilon_probabilistic_inspector({})
        self.assertFalse(r['category_error'])
        self.assertEqual(r['logp'], 0.0)


class TestReturnShape(unittest.TestCase):
    def test_normal_response_keys(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=25.0, candidate_true_value=25.0))
        for key in ('category_error', 'logp', 'gap_sigma',
                    'measurement_scoped', 'ontological_scope'):
            self.assertIn(key, r)

    def test_category_error_response_keys(self):
        r = l_epsilon_probabilistic_inspector(
            dict(measured_value=200.0))
        for key in ('category_error', 'reason', 'logp',
                    'measurement_scoped', 'ontological_scope'):
            self.assertIn(key, r)


if __name__ == '__main__':
    unittest.main()
