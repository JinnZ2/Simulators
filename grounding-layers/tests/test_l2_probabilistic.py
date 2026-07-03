"""
Audit-grade tests for L2 (probabilistic) — ProbabilisticPlanetaryWorld +
l2_probabilistic_inspector. Applies LOG.md's 'Probabilistic L1-L4
Conditioning' section 3 to the L2 planetary module.

Pins:

  GL_L2_P001 [PHENOMENON]: extraction resources (water/soil/minerals)
                            penalized by -(usage/stock)²
  GL_L2_P002 [PHENOMENON]: carbon accumulator penalizes only above
                            sink (drawdown is free)
  GL_L2_P003 [PHENOMENON]: heat budget as -(emit/capacity)²
                            (heat_budget_capacity = 1e5, toy scoping)
  GL_L2_P004 [PHENOMENON]: log_likelihood is pure (no state mutation)
  GL_L2_P_PIN [INSTRUMENT]: six canonical plans pinned

License: CC0
Dependencies: numpy (sim requires it).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from l2_planetary import (
    ProbabilisticPlanetaryWorld,
    l2_probabilistic_inspector,
)


class TestFrozenConstants(unittest.TestCase):
    """[INSTRUMENT] Constraint set (inherited + heat_budget_capacity)
    is frozen. Retuning any without updating a CLAIM is a
    REFUTATION_PROTOCOL violation."""

    def test_water_reserve_initial_frozen(self):
        self.assertEqual(
            ProbabilisticPlanetaryWorld().water_reserve_initial, 1e7)

    def test_soil_mass_initial_frozen(self):
        self.assertEqual(
            ProbabilisticPlanetaryWorld().soil_mass_initial, 1e6)

    def test_mineral_reserve_initial_frozen(self):
        self.assertEqual(
            ProbabilisticPlanetaryWorld().mineral_reserve_initial, 5e5)

    def test_carbon_sink_capacity_frozen(self):
        self.assertEqual(
            ProbabilisticPlanetaryWorld().carbon_sink_capacity, 2e6)

    def test_carbon_uptake_rate_frozen(self):
        self.assertEqual(
            ProbabilisticPlanetaryWorld().carbon_uptake_rate, 500.0)

    def test_heat_budget_capacity_frozen(self):
        # New constant introduced for the probabilistic path.
        self.assertEqual(
            ProbabilisticPlanetaryWorld().heat_budget_capacity, 1e5)


class TestGL_L2_P001_ExtractionResources(unittest.TestCase):
    """[PHENOMENON] Water/soil/minerals penalized by -(usage/stock)²."""

    def _water_only(self, extract):
        return l2_probabilistic_inspector(
            dict(water_extract=extract))['components']['water']

    def test_water_10pc_gives_neg_0p01(self):
        self.assertAlmostEqual(self._water_only(1e6), -0.01, places=10)

    def test_water_50pc_gives_neg_0p25(self):
        self.assertAlmostEqual(self._water_only(5e6), -0.25, places=10)

    def test_water_at_stock_gives_neg_1(self):
        self.assertAlmostEqual(self._water_only(1e7), -1.0, places=10)

    def test_water_10x_stock_gives_neg_100(self):
        self.assertAlmostEqual(self._water_only(1e8), -100.0, places=10)

    def test_soil_uses_same_shape_against_soil_stock(self):
        # soil_mass_initial = 1e6 t, so 5e5 = 50% -> -0.25.
        r = l2_probabilistic_inspector(dict(soil_erosion=5e5))
        self.assertAlmostEqual(r['components']['soil'], -0.25, places=10)

    def test_mineral_uses_same_shape_against_mineral_stock(self):
        # mineral_reserve_initial = 5e5 t, so 5e5 = 100% -> -1.0.
        r = l2_probabilistic_inspector(dict(mineral_mine=5e5))
        self.assertAlmostEqual(r['components']['minerals'],
                               -1.0, places=10)

    def test_zero_extraction_zero_penalty(self):
        r = l2_probabilistic_inspector(dict(
            water_extract=0.0, soil_erosion=0.0, mineral_mine=0.0))
        self.assertEqual(r['components']['water'], 0.0)
        self.assertEqual(r['components']['soil'], 0.0)
        self.assertEqual(r['components']['minerals'], 0.0)


class TestGL_L2_P002_CarbonAccumulator(unittest.TestCase):
    """[PHENOMENON] Carbon penalizes only above sink; drawdown free."""

    def _carbon_only(self, emit):
        return l2_probabilistic_inspector(
            dict(carbon_emit=emit))['components']['carbon']

    def test_carbon_below_uptake_is_free(self):
        # emit = 100 < uptake = 500  -> new_load = -400 -> 0 penalty.
        self.assertEqual(self._carbon_only(100.0), 0.0)

    def test_carbon_equal_to_uptake_is_free(self):
        # emit = 500 = uptake  -> new_load = 0 -> 0 penalty.
        self.assertEqual(self._carbon_only(500.0), 0.0)

    def test_carbon_at_capacity_gives_neg_1(self):
        # emit = 2e6 -> new_load = 2e6 - 500 ≈ 2e6.
        # stress = 2e6 / 2e6 ≈ 1  -> -(1)² ≈ -1.
        v = self._carbon_only(2e6)
        self.assertAlmostEqual(v, -1.0, delta=0.001)

    def test_carbon_2x_capacity_quadratic(self):
        # emit = 4e6 -> new_load ≈ 4e6 -> stress ≈ 2 -> ≈ -4.
        v = self._carbon_only(4e6)
        self.assertAlmostEqual(v, -4.0, delta=0.01)


class TestGL_L2_P003_HeatBudget(unittest.TestCase):
    """[PHENOMENON] Heat budget as -(emit/capacity)²."""

    def _heat_only(self, emit):
        return l2_probabilistic_inspector(
            dict(heat_emit=emit))['components']['heat']

    def test_heat_10pc_gives_neg_0p01(self):
        self.assertAlmostEqual(self._heat_only(1e4), -0.01, places=10)

    def test_heat_at_budget_gives_neg_1(self):
        self.assertAlmostEqual(self._heat_only(1e5), -1.0, places=10)

    def test_heat_10x_budget_gives_neg_100(self):
        self.assertAlmostEqual(self._heat_only(1e6), -100.0, places=10)

    def test_heat_scales_quadratically(self):
        # Doubling emit quadruples the penalty (from the -x^2 shape).
        v_1x = self._heat_only(1e4)
        v_2x = self._heat_only(2e4)
        self.assertAlmostEqual(v_2x, 4.0 * v_1x, places=10)


class TestGL_L2_P004_Purity(unittest.TestCase):
    """[PHENOMENON] log_likelihood does not mutate world state."""

    def test_log_likelihood_does_not_mutate_water(self):
        w = ProbabilisticPlanetaryWorld()
        before = w.water
        w.log_likelihood(dict(water_extract=5e6))
        self.assertEqual(w.water, before)

    def test_log_likelihood_does_not_mutate_soil(self):
        w = ProbabilisticPlanetaryWorld()
        before = w.soil
        w.log_likelihood(dict(soil_erosion=5e5))
        self.assertEqual(w.soil, before)

    def test_log_likelihood_does_not_mutate_minerals(self):
        w = ProbabilisticPlanetaryWorld()
        before = w.minerals
        w.log_likelihood(dict(mineral_mine=5e5))
        self.assertEqual(w.minerals, before)

    def test_log_likelihood_does_not_mutate_carbon_load(self):
        w = ProbabilisticPlanetaryWorld()
        before = w.carbon_load
        w.log_likelihood(dict(carbon_emit=1e6))
        self.assertEqual(w.carbon_load, before)

    def test_two_calls_return_same_result(self):
        w = ProbabilisticPlanetaryWorld()
        plan = dict(water_extract=1e6, carbon_emit=1e6, heat_emit=1e4)
        r1 = w.log_likelihood(plan)
        r2 = w.log_likelihood(plan)
        self.assertEqual(r1['logp'], r2['logp'])
        self.assertEqual(r1['components'], r2['components'])


class TestL2ProbabilisticInspectorDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_L2_P_PIN — six canonical plans pinned."""

    def test_small_clean_plan(self):
        r = l2_probabilistic_inspector(dict(
            water_extract=1000.0, soil_erosion=10.0, mineral_mine=100.0,
            carbon_emit=100.0, heat_emit=1000.0))
        self.assertAlmostEqual(r['logp'], -0.0001, delta=0.0001)

    def test_water_100pc_of_reserve(self):
        r = l2_probabilistic_inspector(dict(water_extract=1e7))
        self.assertAlmostEqual(r['logp'], -1.0000, delta=1e-6)

    def test_water_10x_reserve(self):
        r = l2_probabilistic_inspector(dict(water_extract=1e8))
        self.assertAlmostEqual(r['logp'], -100.0, delta=1e-4)

    def test_multi_resource_at_limit(self):
        # Water at reserve, soil at stock, mineral at stock, carbon at
        # sink. Each ≈ -1. Total ≈ -4.
        r = l2_probabilistic_inspector(dict(
            water_extract=1e7, soil_erosion=1e6, mineral_mine=5e5,
            carbon_emit=2e6))
        self.assertAlmostEqual(r['logp'], -4.0, delta=0.01)

    def test_heat_10x_budget(self):
        r = l2_probabilistic_inspector(dict(heat_emit=1e6))
        self.assertAlmostEqual(r['logp'], -100.0, delta=1e-6)

    def test_carbon_net_drawdown_is_zero(self):
        r = l2_probabilistic_inspector(dict(carbon_emit=100.0))
        self.assertEqual(r['logp'], 0.0)


class TestInspectorReturnShape(unittest.TestCase):
    """Contract on the return dict shape."""

    def test_returns_dict_with_logp_and_components(self):
        r = l2_probabilistic_inspector(dict(water_extract=1000.0))
        self.assertIn('logp', r)
        self.assertIn('components', r)

    def test_components_dict_only_contains_specified_resources(self):
        # A plan that specifies only water should only carry a water
        # component (not empty entries for others).
        r = l2_probabilistic_inspector(dict(water_extract=1000.0))
        self.assertEqual(set(r['components']), {'water'})

    def test_logp_equals_sum_of_components(self):
        r = l2_probabilistic_inspector(dict(
            water_extract=1e6, carbon_emit=1e6, heat_emit=1e4))
        self.assertAlmostEqual(
            r['logp'], sum(r['components'].values()), places=12)

    def test_empty_plan_gives_zero_logp(self):
        r = l2_probabilistic_inspector(dict())
        self.assertEqual(r['logp'], 0.0)
        self.assertEqual(r['components'], {})


if __name__ == '__main__':
    unittest.main()
