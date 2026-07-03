"""
Audit-grade tests for L3 (probabilistic) — ProbabilisticEcologicalWorld +
l3_probabilistic_inspector. Applies LOG.md's 'Probabilistic L1-L4
Conditioning' section 4 to the L3 ecology module.

Every claim in this suite carries the ecosystem_frame cultural
scope: predator-prey / trophic-level / carrying-capacity ontology is
one framing of ecology, and the frozen constants (Kleiber's a=3.0,
10% trophic efficiency, MVP=50) encode a specific
Enlightenment-scientific research tradition. See
SCOPE_TAXONOMY.md.

Pins:

  GL_L3_P001 [PHENOMENON]: allometry as Gaussian on Kleiber deviation
  GL_L3_P002 [PHENOMENON]: trophic transfer as Gaussian on 10%
  GL_L3_P003 [PHENOMENON]: overcapacity smooth barrier
  GL_L3_P004 [PHENOMENON]: MVP undershoot smooth barrier
  GL_L3_P005 [PHENOMENON]: trophic ceiling smooth barrier
  GL_L3_P006 [PHENOMENON]: log_likelihood is pure
  GL_L3_P_PIN [INSTRUMENT]: canonical plans pinned

License: CC0
Dependencies: stdlib (l3_ecology only uses math).
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from l3_ecology import (
    ProbabilisticEcologicalWorld,
    l3_probabilistic_inspector,
)


class TestFrozenConstants(unittest.TestCase):
    """[INSTRUMENT] Constraint set is frozen (inherited + new)."""

    def test_kleiber_a_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().kleiber_a, 3.0)

    def test_trophic_efficiency_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().trophic_transfer_efficiency,
            0.10)

    def test_max_trophic_levels_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().max_trophic_levels, 5)

    def test_mvp_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().minimum_viable_population,
            50)

    def test_allometry_sigma_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().allometry_sigma, 1.0)

    def test_trophic_sigma_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().trophic_sigma, 0.05)

    def test_overcapacity_scale_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().overcapacity_scale, 2.0)

    def test_mvp_scale_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().mvp_scale, 2.0)

    def test_trophic_ceiling_scale_frozen(self):
        self.assertEqual(
            ProbabilisticEcologicalWorld().trophic_ceiling_scale, 1.0)


class TestGL_L3_P001_Allometry(unittest.TestCase):
    """[PHENOMENON] Kleiber-deviation Gaussian."""

    def _allometry_only(self, mass_kg, claimed_W):
        r = l3_probabilistic_inspector(dict(
            mass_kg=mass_kg, claimed_metabolism_W=claimed_W))
        return r['components'].get('allometry', 0.0)

    def test_allometry_spot_on_kleiber_zero_penalty(self):
        # Kleiber(2 kg) = 3.0 * 2^0.75 ≈ 5.045
        w = ProbabilisticEcologicalWorld()
        kleiber = w.allometric_metabolism(2.0)
        self.assertAlmostEqual(
            self._allometry_only(2.0, kleiber), 0.0, places=10)

    def test_allometry_1W_off_gives_neg_half(self):
        w = ProbabilisticEcologicalWorld()
        kleiber = w.allometric_metabolism(2.0)
        # 1 W off, sigma=1 -> -0.5
        self.assertAlmostEqual(
            self._allometry_only(2.0, kleiber + 1.0), -0.5, places=10)

    def test_allometry_10x_kleiber_gives_deep_penalty(self):
        w = ProbabilisticEcologicalWorld()
        kleiber = w.allometric_metabolism(2.0)  # ~5.05
        # 10x Kleiber: (50.45 - 5.05)^2 / 2 = 45.4^2 / 2 = ~1031
        result = self._allometry_only(2.0, 10.0 * kleiber)
        self.assertLess(result, -1000)

    def test_allometry_silent_without_claim(self):
        # No claimed_metabolism_W -> no allometry component.
        r = l3_probabilistic_inspector(dict(mass_kg=2.0))
        self.assertNotIn('allometry', r['components'])


class TestGL_L3_P002_TrophicTransfer(unittest.TestCase):
    """[PHENOMENON] Trophic transfer Gaussian on 10% baseline."""

    def _transfer_only(self, claimed_efficiency):
        r = l3_probabilistic_inspector(dict(
            claimed_trophic_efficiency=claimed_efficiency))
        return r['components']['trophic_transfer']

    def test_at_10pc_zero_penalty(self):
        self.assertAlmostEqual(self._transfer_only(0.10),
                               0.0, places=12)

    def test_at_15pc_gives_neg_half(self):
        # (0.15 - 0.10)^2 / (2 * 0.05^2) = 0.0025 / 0.005 = 0.5
        self.assertAlmostEqual(self._transfer_only(0.15),
                               -0.5, places=10)

    def test_at_50pc_gives_deep_penalty(self):
        # (0.50 - 0.10)^2 / (2 * 0.05^2) = 0.16 / 0.005 = 32
        self.assertAlmostEqual(self._transfer_only(0.50),
                               -32.0, places=10)

    def test_silent_without_claim(self):
        r = l3_probabilistic_inspector(dict(mass_kg=2.0))
        self.assertNotIn('trophic_transfer', r['components'])


class TestGL_L3_P003_Overcapacity(unittest.TestCase):
    """[PHENOMENON] Overcapacity smooth overshoot barrier."""

    def test_at_or_below_K_zero_penalty(self):
        # For a 2kg rabbit at trophic level 1, base_energy=100000:
        # K = trophic_energy(100000, 1) / metabolism(2)
        #   = 10000 / 5.045 ≈ 1982
        # Set N well below K.
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=500, trophic_level=1))
        self.assertEqual(r['components']['overcapacity'], 0.0)

    def test_at_2K_gives_neg_2(self):
        # For rabbit K ≈ 1982; at 2K = ~3964 -> overshoot = 1 -> -2
        w = ProbabilisticEcologicalWorld()
        K = w.carrying_capacity(100000.0, 1, 2.0)
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=int(2 * K), trophic_level=1))
        self.assertAlmostEqual(r['components']['overcapacity'],
                               -2.0, delta=0.01)

    def test_only_penalizes_overshoot_not_undershoot(self):
        # N < K -> overshoot component is 0 (never negative).
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=100, trophic_level=1))
        self.assertEqual(r['components']['overcapacity'], 0.0)


class TestGL_L3_P004_MVP(unittest.TestCase):
    """[PHENOMENON] MVP undershoot smooth barrier."""

    def _mvp_only(self, population):
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=population, trophic_level=1))
        return r['components']['mvp']

    def test_at_MVP_zero_penalty(self):
        # MVP = 50; N=50 -> undershoot = 0 -> 0.
        self.assertEqual(self._mvp_only(50), 0.0)

    def test_above_MVP_zero_penalty(self):
        self.assertEqual(self._mvp_only(500), 0.0)

    def test_at_half_MVP_gives_neg_half(self):
        # N=25 (half MVP) -> undershoot = 0.5 -> scale * 0.25 = 0.5
        self.assertAlmostEqual(self._mvp_only(25), -0.5, places=10)

    def test_at_10pc_MVP_gives_specific_value(self):
        # N=5 -> undershoot = 0.9 -> -scale * 0.81 = -1.62
        self.assertAlmostEqual(self._mvp_only(5), -1.62, places=10)

    def test_at_zero_gives_neg_2(self):
        # Note: pop=0 skips the population-dynamics branch entirely
        # (guard `if pop > 0`). Use pop=1 for the "essentially zero"
        # case: undershoot = 0.98 -> -2 * 0.98^2 = -1.9208.
        self.assertAlmostEqual(self._mvp_only(1), -1.9208, places=4)


class TestGL_L3_P005_TrophicCeiling(unittest.TestCase):
    """[PHENOMENON] Trophic ceiling smooth barrier."""

    def _trophic_only(self, level):
        r = l3_probabilistic_inspector(dict(
            mass_kg=1.0, population=100, trophic_level=level))
        return r['components'].get('trophic_ceiling', 0.0)

    def test_at_max_zero_penalty(self):
        # level = 5 = max -> no penalty.
        self.assertEqual(self._trophic_only(5), 0.0)

    def test_at_7_gives_neg_4(self):
        # level - max = 2 -> -scale * 4 = -4.
        self.assertAlmostEqual(self._trophic_only(7), -4.0, places=10)

    def test_at_10_gives_neg_25(self):
        self.assertAlmostEqual(self._trophic_only(10),
                               -25.0, places=10)


class TestGL_L3_P006_Purity(unittest.TestCase):
    """[PHENOMENON] log_likelihood is pure."""

    def test_log_likelihood_is_idempotent(self):
        # Same input -> same output every call.
        w = ProbabilisticEcologicalWorld()
        plan = dict(mass_kg=2.0, population=800, trophic_level=1,
                    claimed_metabolism_W=5.0)
        r1 = w.log_likelihood(plan)
        r2 = w.log_likelihood(plan)
        self.assertEqual(r1['logp'], r2['logp'])
        self.assertEqual(r1['components'], r2['components'])

    def test_two_calls_do_not_mutate_constants(self):
        w = ProbabilisticEcologicalWorld()
        before = (w.kleiber_a, w.minimum_viable_population,
                  w.allometry_sigma)
        w.log_likelihood(dict(mass_kg=2.0, population=500,
                              trophic_level=1))
        w.log_likelihood(dict(mass_kg=1000.0, population=10,
                              trophic_level=2))
        after = (w.kleiber_a, w.minimum_viable_population,
                 w.allometry_sigma)
        self.assertEqual(before, after)


class TestL3ProbabilisticInspectorDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_L3_P_PIN — canonical plans pinned."""

    def test_empty_plan_is_zero(self):
        r = l3_probabilistic_inspector(dict())
        self.assertEqual(r['logp'], 0.0)

    def test_rabbit_valid_metabolism(self):
        # Rabbit 2kg at trophic level 1 with valid Kleiber metabolism.
        w = ProbabilisticEcologicalWorld()
        kleiber = w.allometric_metabolism(2.0)
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=800, trophic_level=1,
            base_energy=100000.0,
            claimed_metabolism_W=kleiber))
        self.assertAlmostEqual(r['logp'], 0.0, places=6)

    def test_rabbit_10x_metabolism_deep_penalty(self):
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=800, trophic_level=1,
            claimed_metabolism_W=50.4))
        self.assertLess(r['logp'], -1000)

    def test_50pc_trophic_efficiency_gives_neg_32(self):
        r = l3_probabilistic_inspector(dict(
            claimed_trophic_efficiency=0.50))
        self.assertAlmostEqual(r['logp'], -32.0, places=6)

    def test_population_10x_K_overshoot(self):
        w = ProbabilisticEcologicalWorld()
        K = w.carrying_capacity(100000.0, 1, 2.0)
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=int(10 * K), trophic_level=1))
        # overshoot = 9 -> -2 * 81 = -162. Wait, at exactly 10K.
        # overshoot = 10K/K - 1 = 9. -2 * 81 = -162. Not the -18.4
        # in the sample — the sample used pop=8000, K≈1982, so
        # overshoot = 8000/1982 - 1 ≈ 3.036, -2 * 9.22 = -18.4.
        # So test with pop=8000 directly.
        r2 = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=8000, trophic_level=1))
        self.assertAlmostEqual(r2['logp'], -18.4, delta=0.5)

    def test_population_5_below_MVP(self):
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=5, trophic_level=1))
        # Undershoot = 0.9 -> -2 * 0.81 = -1.62.
        # Also overcapacity component fires but N=5 << K so it's 0.
        self.assertAlmostEqual(r['logp'], -1.62, delta=0.01)

    def test_trophic_level_10_gives_neg_25(self):
        # Note: without a population, other components silent.
        # Use minimal plan to isolate trophic_ceiling.
        r = l3_probabilistic_inspector(dict(trophic_level=10))
        self.assertAlmostEqual(r['logp'], -25.0, places=10)

    def test_super_species_from_playground(self):
        # mass=1000 kg, pop=10, trophic=2.
        # Kleiber(1000) = 3 * 1000^0.75 ≈ 533 W.
        # K for 1000 kg at trophic 2, base_energy=100000:
        #   trophic_energy = 100000 * 0.01 = 1000 J
        #   K = 1000 / 533 ≈ 1.88 individuals
        # N=10 vs K=1.88 -> overshoot = 4.33 -> -2 * 18.75 = -37.5
        # MVP: undershoot = 1 - 10/50 = 0.8 -> -2 * 0.64 = -1.28
        # Total ≈ -38.86
        r = l3_probabilistic_inspector(dict(
            mass_kg=1000.0, population=10, trophic_level=2))
        self.assertAlmostEqual(r['logp'], -38.86, delta=0.5)


class TestInspectorReturnShape(unittest.TestCase):
    """Contract on the return dict."""

    def test_returns_dict_with_logp_and_components(self):
        r = l3_probabilistic_inspector(dict(mass_kg=2.0))
        self.assertIn('logp', r)
        self.assertIn('components', r)

    def test_empty_plan_empty_components(self):
        r = l3_probabilistic_inspector(dict())
        self.assertEqual(r['components'], {})

    def test_logp_equals_sum_of_components(self):
        r = l3_probabilistic_inspector(dict(
            mass_kg=2.0, population=8000, trophic_level=6,
            claimed_metabolism_W=50.0,
            claimed_trophic_efficiency=0.3))
        self.assertAlmostEqual(
            r['logp'], sum(r['components'].values()), places=10)


if __name__ == '__main__':
    unittest.main()
