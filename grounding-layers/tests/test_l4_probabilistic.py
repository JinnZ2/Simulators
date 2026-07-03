"""
Audit-grade tests for L4 (probabilistic) — ProbabilisticHumanWorld +
l4_probabilistic_inspector. Applies LOG.md's 'Probabilistic L1-L4
Conditioning' section 5 to the L4 human module.

Design note: L4's SCOPE is O=any_WEIRD_human, so this suite pins TWO
kinds of contract:
  1. Gaussian scoring under human ontology (GL_L4_P002..P003).
  2. Category-error guard for non-human ontology (GL_L4_P001) --
     the load-bearing move for "grounding not dictated by human
     narrative". An AI-self-claim about lift capacity is NOT a
     low-probability human observation; it's a category error.

Pins:

  GL_L4_P001 [PHENOMENON]: category-error guard on ontological scope
  GL_L4_P002 [PHENOMENON]: Gaussian scoring for declared parameters
  GL_L4_P003 [PHENOMENON]: profile shifts apply per-parameter
  GL_L4_P004 [PHENOMENON]: inspector is pure
  GL_L4_P_PIN [INSTRUMENT]: canonical claims pinned

License: CC0
Dependencies: stdlib only (uses math internally, no numpy).
"""

import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from l4_human import (
    ProbabilisticHumanWorld,
    l4_probabilistic_inspector,
)


class TestGL_L4_P001_CategoryErrorGuard(unittest.TestCase):
    """[PHENOMENON] Non-human scopes -> category error, not logp."""

    def test_ai_silicon_substrate_returns_category_error(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=200.0),
            ontological_scope='AI_silicon_substrate')
        self.assertTrue(r['category_error'])
        self.assertIsNone(r['logp'])
        self.assertIn('category error', r['reason'].lower())

    def test_any_information_system_returns_category_error(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=1.0),
            ontological_scope='any_information_system')
        self.assertTrue(r['category_error'])
        self.assertIsNone(r['logp'])

    def test_any_biological_returns_category_error(self):
        # A dog's lift capacity is a different distribution -- not
        # this layer's scope. Category error.
        r = l4_probabilistic_inspector(
            dict(lift_mass=5.0),
            ontological_scope='any_biological')
        self.assertTrue(r['category_error'])

    def test_any_measuring_entity_returns_category_error(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=1.0),
            ontological_scope='any_measuring_entity')
        self.assertTrue(r['category_error'])

    def test_earth_like_biosphere_returns_category_error(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=100.0),
            ontological_scope='earth_like_biosphere')
        self.assertTrue(r['category_error'])

    def test_any_WEIRD_human_scores_normally(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=35.0),
            ontological_scope='any_WEIRD_human')
        self.assertFalse(r['category_error'])
        self.assertIsInstance(r['logp'], float)

    def test_any_human_scores_normally(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=35.0),
            ontological_scope='any_human')
        self.assertFalse(r['category_error'])

    def test_none_scope_scores_with_default_assumed_flag(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=35.0),
            ontological_scope=None)
        self.assertFalse(r['category_error'])
        self.assertTrue(r['scope_default_assumed'])

    def test_category_error_carries_scope_back(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=200.0),
            ontological_scope='AI_silicon_substrate')
        self.assertEqual(r['ontological_scope'],
                         'AI_silicon_substrate')


class TestGL_L4_P002_GaussianScoring(unittest.TestCase):
    """[PHENOMENON] Gaussian shape on declared parameters."""

    def _score(self, plan):
        return l4_probabilistic_inspector(
            plan, ontological_scope='any_WEIRD_human')

    def test_lift_mass_at_mean_zero_penalty(self):
        # general profile mean = 35, std = 15.
        r = self._score(dict(lift_mass=35.0))
        self.assertAlmostEqual(
            r['components']['lift_mass'], 0.0, places=10)

    def test_lift_mass_2sigma_gives_neg_2(self):
        # 35 + 2*15 = 65 -> z = 2 -> -2.
        r = self._score(dict(lift_mass=65.0))
        self.assertAlmostEqual(
            r['components']['lift_mass'], -2.0, places=10)

    def test_lift_mass_100_gives_approx_neg_9p4(self):
        # 100 - 35 = 65; 65/15 = 4.333; z^2/2 ≈ 9.39.
        r = self._score(dict(lift_mass=100.0))
        self.assertAlmostEqual(
            r['components']['lift_mass'], -9.39, delta=0.01)

    def test_reaction_time_at_mean_zero_penalty(self):
        # mean = 0.25, std = 0.05.
        r = self._score(dict(reaction_time=0.25))
        self.assertAlmostEqual(
            r['components']['reaction_time'], 0.0, places=10)

    def test_reaction_time_2sigma_below(self):
        # 0.25 - 2*0.05 = 0.15 -> z = -2 -> -2.
        r = self._score(dict(reaction_time=0.15))
        self.assertAlmostEqual(
            r['components']['reaction_time'], -2.0, places=10)

    def test_temp_tolerance_scales_quadratically(self):
        # mean = 43, std = 5. temp = 60 -> z = 3.4 -> -5.78.
        r = self._score(dict(temp_tolerance=60.0))
        self.assertAlmostEqual(
            r['components']['temp_tolerance'], -5.78, delta=0.01)

    def test_sustained_power_scales_quadratically(self):
        # mean = 150, std = 50. power = 500 -> z = 7 -> -24.5.
        r = self._score(dict(sustained_power=500.0))
        self.assertAlmostEqual(
            r['components']['sustained_power'], -24.5, places=10)

    def test_undeclared_parameters_absent_from_components(self):
        # A plan with only lift_mass should NOT have reaction_time,
        # temp_tolerance, or sustained_power components.
        r = self._score(dict(lift_mass=35.0))
        self.assertEqual(set(r['components']), {'lift_mass'})

    def test_total_logp_is_sum_of_components(self):
        r = self._score(dict(lift_mass=65.0, reaction_time=0.35,
                             temp_tolerance=53.0,
                             sustained_power=250.0))
        self.assertAlmostEqual(
            r['logp'], sum(r['components'].values()), places=10)


class TestGL_L4_P003_ProfileShifts(unittest.TestCase):
    """[PHENOMENON] Profile shifts change the mean per-parameter."""

    def _score(self, plan, profile):
        return l4_probabilistic_inspector(
            {**plan, 'human_profile': profile},
            ontological_scope='any_WEIRD_human')

    def test_athlete_shift_on_lift_mass(self):
        # Athlete mean = 35 + 15 = 50. Lift = 50 -> z = 0 -> 0.
        r = self._score(dict(lift_mass=50.0), 'athlete')
        self.assertAlmostEqual(
            r['components']['lift_mass'], 0.0, places=10)

    def test_child_shift_on_lift_mass(self):
        # Child mean = 35 - 20 = 15. Lift = 15 -> z = 0 -> 0.
        r = self._score(dict(lift_mass=15.0), 'child')
        self.assertAlmostEqual(
            r['components']['lift_mass'], 0.0, places=10)

    def test_elder_shift_reduces_lift(self):
        # Elder mean = 35 - 10 = 25. Lift = 40 -> z = 1 -> -0.5.
        r = self._score(dict(lift_mass=40.0), 'elder')
        self.assertAlmostEqual(
            r['components']['lift_mass'], -0.5, places=10)

    def test_temp_tolerance_no_profile_shift(self):
        # temp_shift = 0 for all shipped profiles.
        # temp = 43 (mean) -> 0 under any profile.
        for prof in ('general', 'athlete', 'elder', 'child', 'trained'):
            r = self._score(dict(temp_tolerance=43.0), prof)
            self.assertAlmostEqual(
                r['components']['temp_tolerance'], 0.0, places=10,
                msg=f'profile {prof} shouldn\'t shift temp_tolerance')

    def test_trained_shift_on_reaction_time(self):
        # Trained: reaction mean = 0.25 - 0.02 = 0.23.
        # Reaction = 0.23 -> z = 0 -> 0.
        r = self._score(dict(reaction_time=0.23), 'trained')
        self.assertAlmostEqual(
            r['components']['reaction_time'], 0.0, places=10)


class TestGL_L4_P004_Purity(unittest.TestCase):
    """[PHENOMENON] Inspector is pure."""

    def test_log_likelihood_is_idempotent(self):
        w = ProbabilisticHumanWorld()
        plan = dict(lift_mass=45.0, reaction_time=0.22,
                    temp_tolerance=42.0, sustained_power=160.0,
                    human_profile='general')
        r1 = w.log_likelihood(plan, ontological_scope='any_WEIRD_human')
        r2 = w.log_likelihood(plan, ontological_scope='any_WEIRD_human')
        self.assertEqual(r1['logp'], r2['logp'])
        self.assertEqual(r1['components'], r2['components'])

    def test_log_likelihood_does_not_mutate_plan(self):
        w = ProbabilisticHumanWorld()
        plan = dict(lift_mass=45.0, human_profile='general')
        before = copy.deepcopy(plan)
        w.log_likelihood(plan, ontological_scope='any_WEIRD_human')
        self.assertEqual(plan, before)

    def test_log_likelihood_does_not_mutate_world(self):
        w = ProbabilisticHumanWorld()
        before = (w.lift_mass, w.reaction_time,
                  w.temp_tolerance, w.sustained_power)
        w.log_likelihood(dict(lift_mass=45.0),
                         ontological_scope='any_WEIRD_human')
        w.log_likelihood(dict(reaction_time=0.30),
                         ontological_scope='any_WEIRD_human')
        after = (w.lift_mass, w.reaction_time,
                 w.temp_tolerance, w.sustained_power)
        self.assertEqual(before, after)


class TestL4ProbabilisticInspectorDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_L4_P_PIN — canonical claims pinned."""

    def test_ai_lift_200kg_category_error(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=200.0),
            ontological_scope='AI_silicon_substrate')
        self.assertTrue(r['category_error'])
        self.assertIsNone(r['logp'])

    def test_general_lift_40kg(self):
        # z = (40 - 35)/15 = 1/3 -> logp = -1/18 ≈ -0.0556.
        r = l4_probabilistic_inspector(
            dict(lift_mass=40.0),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -0.0556, delta=0.001)

    def test_general_lift_100kg(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=100.0),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -9.39, delta=0.01)

    def test_athlete_lift_60kg(self):
        # Athlete mean 50, std 15. z = (60-50)/15 = 2/3 -> -2/9 ≈ -0.222.
        r = l4_probabilistic_inspector(
            dict(lift_mass=60.0, human_profile='athlete'),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -0.222, delta=0.005)

    def test_elder_lift_40kg(self):
        # Elder mean 25, std 15. z = (40-25)/15 = 1 -> -0.5.
        r = l4_probabilistic_inspector(
            dict(lift_mass=40.0, human_profile='elder'),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -0.5, places=10)

    def test_reaction_time_2sigma_below(self):
        r = l4_probabilistic_inspector(
            dict(reaction_time=0.15),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -2.0, places=10)

    def test_temp_60C(self):
        r = l4_probabilistic_inspector(
            dict(temp_tolerance=60.0),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -5.78, delta=0.01)

    def test_sustained_500W(self):
        r = l4_probabilistic_inspector(
            dict(sustained_power=500.0),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], -24.5, places=10)

    def test_full_plan_at_means(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=35.0, reaction_time=0.25,
                 temp_tolerance=43.0, sustained_power=150.0),
            ontological_scope='any_WEIRD_human')
        self.assertAlmostEqual(r['logp'], 0.0, places=10)

    def test_information_system_gets_category_error(self):
        r = l4_probabilistic_inspector(
            dict(sustained_power=1e12),
            ontological_scope='any_information_system')
        self.assertTrue(r['category_error'])


class TestInspectorReturnShape(unittest.TestCase):
    """Contract on the return dict."""

    def test_category_error_response_shape(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=200.0),
            ontological_scope='AI_silicon_substrate')
        for key in ('category_error', 'reason', 'logp',
                    'components', 'ontological_scope'):
            self.assertIn(key, r)

    def test_normal_response_shape(self):
        r = l4_probabilistic_inspector(
            dict(lift_mass=35.0),
            ontological_scope='any_WEIRD_human')
        for key in ('category_error', 'logp', 'components',
                    'ontological_scope', 'scope_default_assumed',
                    'human_profile'):
            self.assertIn(key, r)

    def test_empty_plan_gives_zero_logp(self):
        r = l4_probabilistic_inspector(
            dict(), ontological_scope='any_WEIRD_human')
        self.assertEqual(r['logp'], 0.0)
        self.assertEqual(r['components'], {})


if __name__ == '__main__':
    unittest.main()
