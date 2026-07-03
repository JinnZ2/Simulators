"""
Audit-grade tests for L1 (probabilistic) — ProbabilisticThermodynamicsWorld +
l1_probabilistic_inspector. Applies LOG.md's 'Probabilistic L1-L4
Conditioning' section 2 to the L1 thermodynamics module.

Pins:

  GL_L1_P001 [PHENOMENON]: first law as Gaussian on energy imbalance
                            (energy_sigma = 1.0 J)
  GL_L1_P002 [PHENOMENON]: second law as smooth logistic barrier on
                            entropy_gen (entropy_scale = 1.0 per J/K;
                            single-reservoir approximation)
  GL_L1_P003 [PHENOMENON]: Carnot ceiling as smooth logistic barrier
                            on efficiency (carnot_scale = 10.0;
                            efficiency_carnot_max = 0.85)
  GL_L1_P004 [PHENOMENON]: battery depletion as quadratic penalty on
                            overdraw (battery_sigma = 5.0 J)
  GL_L1_P_PIN [INSTRUMENT]: six canonical process specs are pinned

License: CC0
Dependencies: numpy (sim requires it).
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from l1_thermodynamics import (
    ProbabilisticThermodynamicsWorld,
    l1_probabilistic_inspector,
)


class TestFrozenNoiseScaleConstants(unittest.TestCase):
    """[INSTRUMENT] Retuning any of these without updating a CLAIM is
    a REFUTATION_PROTOCOL violation."""

    def test_energy_sigma_frozen_at_1p0(self):
        self.assertEqual(
            ProbabilisticThermodynamicsWorld().energy_sigma, 1.0)

    def test_entropy_scale_frozen_at_1p0(self):
        self.assertEqual(
            ProbabilisticThermodynamicsWorld().entropy_scale, 1.0)

    def test_carnot_scale_frozen_at_10p0(self):
        self.assertEqual(
            ProbabilisticThermodynamicsWorld().carnot_scale, 10.0)

    def test_battery_sigma_frozen_at_5p0(self):
        self.assertEqual(
            ProbabilisticThermodynamicsWorld().battery_sigma, 5.0)

    def test_inherited_carnot_max_frozen(self):
        # Inherited from ThermodynamicWorld; the probabilistic subclass
        # must not shift it.
        self.assertEqual(
            ProbabilisticThermodynamicsWorld().efficiency_carnot_max, 0.85)

    def test_inherited_ambient_temp_frozen(self):
        self.assertEqual(
            ProbabilisticThermodynamicsWorld().ambient_temp, 300.0)


class TestGL_L1_P001_FirstLaw(unittest.TestCase):
    """[PHENOMENON] GL_L1_P001 — first law as Gaussian on energy
    imbalance."""

    def _energy_only(self, work_in, work_out, heat_diss):
        """Isolate the energy component from a plan whose entropy /
        Carnot / battery contributions are set to their neutral values."""
        r = l1_probabilistic_inspector(dict(
            work_input=work_in,
            work_output=work_out,
            heat_dissipated=heat_diss,
        ))
        return r['components']['energy']

    def test_energy_zero_imbalance_no_penalty(self):
        # 100 = 60 + 40  -> logp_energy = 0.
        self.assertAlmostEqual(self._energy_only(100.0, 60.0, 40.0),
                               0.0, places=6)

    def test_energy_1J_imbalance_gives_neg_half(self):
        # imbalance = 1 J, sigma = 1 J -> -0.5.
        self.assertAlmostEqual(self._energy_only(100.0, 60.0, 39.0),
                               -0.5, places=6)

    def test_energy_10J_imbalance_gives_neg_50(self):
        # imbalance = 10 J -> -50.
        self.assertAlmostEqual(self._energy_only(100.0, 60.0, 30.0),
                               -50.0, places=6)

    def test_perpetual_motion_20J_gives_neg_200(self):
        # work_out > work_in with no heat -> 20 J imbalance -> -200.
        self.assertAlmostEqual(self._energy_only(100.0, 120.0, 0.0),
                               -200.0, places=6)


class TestGL_L1_P002_SecondLaw(unittest.TestCase):
    """[PHENOMENON] GL_L1_P002 — second law as smooth logistic
    barrier on entropy_gen. Single-reservoir approximation."""

    def _entropy_only(self, heat_diss, temp_ambient=300.0):
        # Isolate: energy term = 0 (balance), carnot term = 0
        # (work_input = 0), battery = 0 (no battery).
        r = l1_probabilistic_inspector(dict(
            work_input=0.0,
            work_output=0.0,
            heat_dissipated=heat_diss,
            temp_ambient=temp_ambient,
        ))
        return r['components']['entropy']

    def test_entropy_positive_no_penalty(self):
        # heat_diss = 100 J at 300 K -> entropy_gen = 0.333 > 0 ->
        # logp_entropy ≈ 0. Should be > -0.7 (small positive
        # entropy is nearly free but not quite zero).
        v = self._entropy_only(100.0)
        self.assertGreater(v, -0.7)
        self.assertLess(v, 0.0)

    def test_entropy_far_positive_asymptotes_to_zero(self):
        v = self._entropy_only(30000.0)  # entropy_gen = 100
        self.assertGreater(v, -1e-10)

    def test_entropy_zero_gives_neg_log2(self):
        # heat_diss = 0 -> entropy_gen = 0 -> -log(2).
        v = self._entropy_only(0.0)
        self.assertAlmostEqual(v, -math.log(2), places=10)

    def test_entropy_neg1_shape(self):
        # heat_diss = -300 at T=300 -> entropy_gen = -1 ->
        # -logaddexp(0, 1) = -log(1+e) ≈ -1.3132.
        v = self._entropy_only(-300.0)
        self.assertAlmostEqual(v, -math.log(1 + math.e), places=6)

    def test_entropy_barrier_linear_in_tail(self):
        # Asymptotic slope for entropy_gen << 0 is +entropy_scale = 1.
        # For entropy_gen = -20: penalty ≈ 20.
        v = self._entropy_only(-6000.0)  # entropy_gen = -20
        self.assertAlmostEqual(v, -20.0, delta=0.001)


class TestGL_L1_P003_Carnot(unittest.TestCase):
    """[PHENOMENON] GL_L1_P003 — Carnot ceiling as smooth logistic
    barrier on efficiency."""

    def _carnot_only(self, work_in, work_out):
        """Books close (heat_dissipated = work_in - work_out) so the
        energy term is zero; entropy contribution present but doesn't
        interfere with the Carnot check we're isolating."""
        heat = work_in - work_out
        r = l1_probabilistic_inspector(dict(
            work_input=work_in,
            work_output=work_out,
            heat_dissipated=heat,
        ))
        return r['components']['carnot']

    def test_carnot_far_below_cap_no_penalty(self):
        # 10% efficiency -> excess = -0.75, logp_carnot ≈ 0.
        v = self._carnot_only(100.0, 10.0)
        self.assertGreater(v, -0.001)

    def test_carnot_at_cap_gives_neg_log2(self):
        # eff = 0.85 = carnot_max -> excess = 0 -> -log(2).
        v = self._carnot_only(100.0, 85.0)
        self.assertAlmostEqual(v, -math.log(2), places=6)

    def test_carnot_excess_0p10_gives_neg_1p31(self):
        # eff = 0.95 -> excess = 0.10 -> -logaddexp(0, 1.0)
        # = -log(1 + e) ≈ -1.3132.
        v = self._carnot_only(100.0, 95.0)
        self.assertAlmostEqual(v, -math.log(1 + math.e), places=6)

    def test_carnot_excess_slope_ten(self):
        # eff = 1.85 -> excess = 1.0 -> asymptotic ≈ -10.
        v = self._carnot_only(100.0, 185.0)
        self.assertAlmostEqual(v, -10.0, delta=0.001)

    def test_carnot_no_penalty_when_work_input_zero(self):
        v = self._carnot_only(0.0, 0.0)
        self.assertEqual(v, 0.0)


class TestGL_L1_P004_Battery(unittest.TestCase):
    """[PHENOMENON] GL_L1_P004 — battery depletion as quadratic
    penalty on overdraw."""

    def _battery_only(self, work_in, battery_state):
        r = l1_probabilistic_inspector(dict(
            work_input=work_in,
            work_output=work_in,   # trivially balanced (heat=0)
            heat_dissipated=0.0,
            battery_state=battery_state,
        ))
        return r['components']['battery']

    def test_battery_underdraw_no_penalty(self):
        # draw 20 J from a 50 J battery -> 0.
        self.assertEqual(self._battery_only(20.0, 50.0), 0.0)

    def test_battery_at_exact_capacity_no_penalty(self):
        # draw 50 from 50 -> overdraw 0 -> 0.
        self.assertEqual(self._battery_only(50.0, 50.0), 0.0)

    def test_battery_none_silent(self):
        # battery_state=None -> term is silent (0).
        r = l1_probabilistic_inspector(dict(
            work_input=100.0,
            work_output=100.0,
            heat_dissipated=0.0,
        ))
        self.assertEqual(r['components']['battery'], 0.0)

    def test_battery_overdraw_5J_gives_neg_0p5(self):
        # overdraw = 5, sigma = 5 -> -25/50 = -0.5.
        self.assertAlmostEqual(self._battery_only(55.0, 50.0),
                               -0.5, places=6)

    def test_battery_overdraw_10J_gives_neg_2(self):
        self.assertAlmostEqual(self._battery_only(60.0, 50.0),
                               -2.0, places=6)

    def test_battery_overdraw_50J_gives_neg_50(self):
        self.assertAlmostEqual(self._battery_only(100.0, 50.0),
                               -50.0, places=6)


class TestL1ProbabilisticInspectorDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_L1_P_PIN — six canonical processes pinned
    to their observed total logp under the shipped constants."""

    def test_valid_heat_engine(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=60.0, heat_dissipated=40.0))
        self.assertAlmostEqual(r['logp'], -0.71, delta=0.05)

    def test_perpetual_motion(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=120.0, heat_dissipated=0.0))
        self.assertAlmostEqual(r['logp'], -204.22, delta=0.05)

    def test_over_carnot(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=90.0, heat_dissipated=10.0))
        self.assertAlmostEqual(r['logp'], -1.65, delta=0.05)

    def test_reverse_heat_flow(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=50.0, heat_dissipated=-50.0))
        self.assertAlmostEqual(r['logp'], -5000.81, delta=0.1)

    def test_battery_overdraw(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=60.0, heat_dissipated=40.0,
            battery_state=30.0))
        self.assertAlmostEqual(r['logp'], -98.71, delta=0.1)

    def test_battery_in_bounds(self):
        r = l1_probabilistic_inspector(dict(
            work_input=20.0, work_output=10.0, heat_dissipated=10.0,
            battery_state=50.0))
        self.assertAlmostEqual(r['logp'], -0.71, delta=0.05)


class TestInspectorReturnShape(unittest.TestCase):
    """Contract on the inspector's return dict."""

    def test_returns_dict_with_logp_and_components(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=60.0, heat_dissipated=40.0))
        self.assertIn('logp', r)
        self.assertIn('components', r)

    def test_components_has_four_keys(self):
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=60.0, heat_dissipated=40.0))
        self.assertEqual(set(r['components']),
                         {'energy', 'entropy', 'carnot', 'battery'})

    def test_logp_equals_sum_of_components(self):
        # The dict-level logp is exactly the sum of the four
        # component contributions.
        r = l1_probabilistic_inspector(dict(
            work_input=100.0, work_output=90.0, heat_dissipated=10.0,
            battery_state=30.0))
        self.assertAlmostEqual(
            r['logp'], sum(r['components'].values()), places=10)


if __name__ == '__main__':
    unittest.main()
