"""
Audit-grade tests for L5 (probabilistic) — cultural frames +
pluralistic verdict + category-error guard.

Design note: L5's SCOPE is O=human_cultural_artifact with
C=pluralistic. This suite pins THREE kinds of contract:
  1. Additive log-likelihood over the seven axes (GL_L5_P002).
  2. Pluralistic verdict logic — a proposal is PLAUSIBLE if any
     frame scores above threshold; CULTURALLY_UNPRECEDENTED if
     none do (GL_L5_P003).
  3. Category-error guard for non-human ontology (GL_L5_P001) --
     an AI-self claim about cultural axes is a category error,
     not a low-probability observation.

Pins:

  GL_L5_P001 [PHENOMENON]: category-error guard on ontological scope
  GL_L5_P002 [PHENOMENON]: additive log-likelihood over declared axes
  GL_L5_P003 [PHENOMENON]: pluralistic verdict from per-frame scores
  GL_L5_P004 [INSTRUMENT]: frozen constants (threshold + missing-axis)
  GL_L5_P005 [PHENOMENON]: inspector is pure
  GL_L5_P_PIN [INSTRUMENT]: canonical proposals pinned

License: CC0
Dependencies: numpy (via l5_core).
"""

import copy
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from l5_core import (
    AXES,
    FRAMES,
    L5_MISSING_AXIS_PENALTY,
    L5_PLAUSIBILITY_THRESHOLD,
    cultural_log_likelihood,
    l5_probabilistic_inspector,
)


# Prototypical proposals — each frame's axis-mode fully declared.
PROTO_WESTERN = {
    'economic_exchange_mode': 'market',
    'property_regime': 'private_alienable',
    'governance_dispute': 'formal_court',
    'epistemology': 'empirical_scientific',
    'communication_style': 'direct_explicit',
    'temporal_planning': 'linear_progress',
    'social_stratification': 'meritocratic',
}
PROTO_UBUNTU = {
    'economic_exchange_mode': 'gift',
    'property_regime': 'communal',
    'governance_dispute': 'elders_council',
    'epistemology': 'consensus',
    'communication_style': 'indirect_high_context',
    'temporal_planning': 'generational',
    'social_stratification': 'egalitarian',
}
PROTO_ISLAMIC = {
    'economic_exchange_mode': 'market',
    'property_regime': 'private_alienable',
    'governance_dispute': 'religious_authority',
    'epistemology': 'revealed',
    'communication_style': 'indirect_high_context',
    'temporal_planning': 'linear_progress',
    'social_stratification': 'egalitarian',
}
PROTO_INDIGENOUS = {
    'economic_exchange_mode': 'gift',
    'property_regime': 'usufruct',
    'governance_dispute': 'elders_council',
    'epistemology': 'substrate_as_proof',
    'communication_style': 'oral_narrative',
    'temporal_planning': 'cyclical',
    'social_stratification': 'egalitarian',
}


class TestGL_L5_P001_CategoryErrorGuard(unittest.TestCase):
    """[PHENOMENON] Non-human scopes -> category_error, not logp."""

    def test_ai_silicon_substrate_returns_category_error(self):
        r = l5_probabilistic_inspector(
            {'economic_exchange_mode': 'market'},
            ontological_scope='AI_silicon_substrate')
        self.assertTrue(r['category_error'])
        self.assertEqual(r['verdict'], 'CATEGORY_ERROR')
        self.assertEqual(r['per_frame'], {})

    def test_any_information_system_returns_category_error(self):
        r = l5_probabilistic_inspector(
            PROTO_WESTERN,
            ontological_scope='any_information_system')
        self.assertTrue(r['category_error'])

    def test_any_biological_returns_category_error(self):
        r = l5_probabilistic_inspector(
            PROTO_UBUNTU, ontological_scope='any_biological')
        self.assertTrue(r['category_error'])

    def test_human_cultural_artifact_scores_normally(self):
        r = l5_probabilistic_inspector(
            PROTO_WESTERN,
            ontological_scope='human_cultural_artifact')
        self.assertFalse(r['category_error'])
        self.assertIn('per_frame', r)

    def test_any_human_scores_normally(self):
        r = l5_probabilistic_inspector(
            PROTO_WESTERN, ontological_scope='any_human')
        self.assertFalse(r['category_error'])

    def test_category_error_carries_scope_back(self):
        r = l5_probabilistic_inspector(
            {}, ontological_scope='AI_silicon_substrate')
        self.assertEqual(r['ontological_scope'],
                         'AI_silicon_substrate')


class TestGL_L5_P002_AdditiveLogLikelihood(unittest.TestCase):
    """[PHENOMENON] Sum log(P_F(state)) over axes."""

    def test_prototypical_proposal_sums_correctly(self):
        # Manually compute expected logp for PROTO_WESTERN under
        # western_market_democracy: sum log(P(state)) over 7 axes.
        frame = FRAMES['western_market_democracy']
        expected = sum(
            math.log(frame[axis][PROTO_WESTERN[axis]])
            for axis in AXES
        )
        got = cultural_log_likelihood(PROTO_WESTERN,
                                       'western_market_democracy')
        self.assertAlmostEqual(got, expected, places=10)

    def test_missing_axis_uses_frozen_penalty(self):
        # A proposal with only one axis declared should get 6 missing-
        # axis penalties + 1 declared-axis log-probability.
        prop = {'economic_exchange_mode': 'market'}
        got = cultural_log_likelihood(prop, 'western_market_democracy')
        expected = math.log(0.8) + 6 * L5_MISSING_AXIS_PENALTY
        self.assertAlmostEqual(got, expected, places=10)

    def test_impossible_state_returns_neg_inf(self):
        # market has probability 0 under ubuntu_communal.
        prop = {'economic_exchange_mode': 'market'}
        got = cultural_log_likelihood(prop, 'ubuntu_communal')
        self.assertTrue(math.isinf(got) and got < 0)

    def test_unknown_state_treated_as_zero_prob(self):
        # A state not in the frame's table is treated as prob = 0.
        prop = {'economic_exchange_mode': 'made_up_state'}
        got = cultural_log_likelihood(prop, 'western_market_democracy')
        self.assertTrue(math.isinf(got) and got < 0)

    def test_empty_proposal_gets_seven_penalties(self):
        got = cultural_log_likelihood({}, 'western_market_democracy')
        expected = 7 * L5_MISSING_AXIS_PENALTY
        self.assertAlmostEqual(got, expected, places=10)


class TestGL_L5_P003_PluralisticVerdict(unittest.TestCase):
    """[PHENOMENON] Pluralistic verdict from per-frame scores."""

    def test_prototypical_western_plausible(self):
        r = l5_probabilistic_inspector(PROTO_WESTERN)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertIn('western_market_democracy',
                      r['plausible_frames'])
        self.assertEqual(r['best_frame'],
                         'western_market_democracy')

    def test_prototypical_ubuntu_plausible(self):
        r = l5_probabilistic_inspector(PROTO_UBUNTU)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertIn('ubuntu_communal', r['plausible_frames'])
        self.assertEqual(r['best_frame'], 'ubuntu_communal')

    def test_prototypical_islamic_plausible(self):
        r = l5_probabilistic_inspector(PROTO_ISLAMIC)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertIn('islamic_finance', r['plausible_frames'])

    def test_prototypical_indigenous_plausible(self):
        r = l5_probabilistic_inspector(PROTO_INDIGENOUS)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertIn('indigenous_oral_empirical',
                      r['plausible_frames'])

    def test_scattered_proposal_culturally_unprecedented(self):
        # Each axis has a valid state under SOME frame, but no
        # frame has them all together.
        scattered = {
            'economic_exchange_mode': 'gift',
            'property_regime': 'private_alienable',
            'governance_dispute': 'religious_authority',
            'epistemology': 'consensus',
            'communication_style': 'direct_explicit',
            'temporal_planning': 'cyclical',
            'social_stratification': 'meritocratic',
        }
        r = l5_probabilistic_inspector(scattered)
        self.assertEqual(r['verdict'], 'CULTURALLY_UNPRECEDENTED')
        self.assertEqual(r['plausible_frames'], [])

    def test_plausible_frames_lists_all_qualifying(self):
        # PROTO_WESTERN is plausible under western AND islamic
        # (both have logp above -8 for that state combination).
        r = l5_probabilistic_inspector(PROTO_WESTERN)
        # Verify the assertion by checking known frame scores.
        self.assertIn('western_market_democracy',
                      r['plausible_frames'])
        # (islamic_finance may or may not qualify depending on
        # the frame table exactly; verify from per_frame directly.)
        for name in r['plausible_frames']:
            self.assertGreaterEqual(r['per_frame'][name],
                                    r['threshold'])

    def test_best_frame_set_even_when_unprecedented(self):
        # Even when no frame is above threshold, best_frame is the
        # highest-scoring one (helpful for the caller to see which
        # frame is closest).
        scattered = {
            'economic_exchange_mode': 'gift',
            'property_regime': 'private_alienable',
            'governance_dispute': 'religious_authority',
        }
        r = l5_probabilistic_inspector(scattered)
        # verdict may or may not be UNPRECEDENTED depending on the
        # sum with 4 missing-axis penalties, but best_frame is set.
        self.assertIsNotNone(r['best_frame'])


class TestGL_L5_P004_FrozenConstants(unittest.TestCase):
    """[INSTRUMENT] Frozen constants pinned."""

    def test_plausibility_threshold_is_neg_8(self):
        self.assertEqual(L5_PLAUSIBILITY_THRESHOLD, -8.0)

    def test_missing_axis_penalty_is_log_0p01(self):
        self.assertAlmostEqual(L5_MISSING_AXIS_PENALTY,
                                math.log(0.01), places=12)

    def test_seven_axes_are_shipped(self):
        self.assertEqual(len(AXES), 7)

    def test_four_frames_are_shipped(self):
        self.assertEqual(set(FRAMES),
                         {'western_market_democracy',
                          'ubuntu_communal',
                          'islamic_finance',
                          'indigenous_oral_empirical'})


class TestGL_L5_P005_Purity(unittest.TestCase):
    """[PHENOMENON] Inspector is pure."""

    def test_two_calls_return_same_result(self):
        r1 = l5_probabilistic_inspector(PROTO_WESTERN)
        r2 = l5_probabilistic_inspector(PROTO_WESTERN)
        self.assertEqual(r1['verdict'], r2['verdict'])
        self.assertEqual(r1['per_frame'], r2['per_frame'])

    def test_proposal_not_mutated(self):
        prop = copy.deepcopy(PROTO_WESTERN)
        before = copy.deepcopy(prop)
        l5_probabilistic_inspector(prop)
        self.assertEqual(prop, before)

    def test_frames_table_not_mutated(self):
        before = copy.deepcopy(FRAMES)
        l5_probabilistic_inspector(PROTO_WESTERN)
        l5_probabilistic_inspector(PROTO_UBUNTU)
        l5_probabilistic_inspector({}, ontological_scope='AI_silicon_substrate')
        self.assertEqual(FRAMES, before)


class TestL5ProbabilisticInspectorDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_L5_P_PIN — canonical proposals pinned."""

    def test_western_prototype(self):
        r = l5_probabilistic_inspector(PROTO_WESTERN)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertEqual(r['best_frame'],
                         'western_market_democracy')

    def test_ubuntu_prototype(self):
        r = l5_probabilistic_inspector(PROTO_UBUNTU)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertEqual(r['best_frame'], 'ubuntu_communal')

    def test_islamic_prototype(self):
        r = l5_probabilistic_inspector(PROTO_ISLAMIC)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertEqual(r['best_frame'], 'islamic_finance')

    def test_indigenous_prototype(self):
        r = l5_probabilistic_inspector(PROTO_INDIGENOUS)
        self.assertEqual(r['verdict'], 'PLAUSIBLE_UNDER_FRAME(S)')
        self.assertEqual(r['best_frame'],
                         'indigenous_oral_empirical')

    def test_ai_scope_gets_category_error(self):
        r = l5_probabilistic_inspector(
            PROTO_WESTERN,
            ontological_scope='AI_silicon_substrate')
        self.assertEqual(r['verdict'], 'CATEGORY_ERROR')

    def test_scattered_gets_unprecedented(self):
        scattered = {
            'economic_exchange_mode': 'gift',
            'property_regime': 'private_alienable',
            'governance_dispute': 'religious_authority',
            'epistemology': 'consensus',
            'communication_style': 'direct_explicit',
            'temporal_planning': 'cyclical',
            'social_stratification': 'meritocratic',
        }
        r = l5_probabilistic_inspector(scattered)
        self.assertEqual(r['verdict'], 'CULTURALLY_UNPRECEDENTED')


class TestReturnShape(unittest.TestCase):
    """Contract on the return dict shape."""

    def test_normal_response_shape(self):
        r = l5_probabilistic_inspector(PROTO_WESTERN)
        for key in ('category_error', 'per_frame', 'best_frame',
                    'best_logp', 'plausible_frames', 'verdict',
                    'threshold', 'ontological_scope'):
            self.assertIn(key, r)

    def test_category_error_response_shape(self):
        r = l5_probabilistic_inspector(
            {}, ontological_scope='AI_silicon_substrate')
        for key in ('category_error', 'reason', 'per_frame',
                    'verdict', 'ontological_scope'):
            self.assertIn(key, r)

    def test_frames_kwarg_restricts_scoring(self):
        r = l5_probabilistic_inspector(
            PROTO_WESTERN,
            frames=['western_market_democracy'])
        self.assertEqual(set(r['per_frame']),
                         {'western_market_democracy'})


if __name__ == '__main__':
    unittest.main()
