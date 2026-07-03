"""
Audit-grade tests for integrated_stack — product-of-experts across
L0-L4 probabilistic layers. Applies LOG.md's section 6 with the
category-error rule from SCOPE_TAXONOMY.md.

Pins:

  GL_INT_001 [PHENOMENON]: additive product of experts on applicable
                            layers
  GL_INT_002 [PHENOMENON]: layer selection by plan-key presence;
                            skip is silent
  GL_INT_003 [PHENOMENON]: category error at any layer refuses the
                            whole plan (total_logp=None)
  GL_INT_004 [PHENOMENON]: inspector is pure
  GL_INT_PIN [INSTRUMENT]: canonical multi-layer plans pinned

License: CC0
Dependencies: numpy (transitively via L0/L2/L3).
"""

import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from integrated_stack import (
    LAYER_ORDER,
    integrated_probabilistic_inspector,
)


class TestGL_INT_001_ProductOfExperts(unittest.TestCase):
    """[PHENOMENON] total = sum over applicable layers."""

    def test_total_equals_sum_over_applicable_layers(self):
        r = integrated_probabilistic_inspector({
            'L1': dict(work_input=100.0, work_output=120.0,
                       heat_dissipated=0.0),
            'L2': dict(water_extract=1e7),
        })
        expected = (r['per_layer']['L1']['logp']
                    + r['per_layer']['L2']['logp'])
        self.assertAlmostEqual(r['total_logp'], expected, places=10)

    def test_multi_layer_L1_L2_L3_sums_correctly(self):
        r = integrated_probabilistic_inspector({
            'L1': dict(work_input=100.0, work_output=120.0,
                       heat_dissipated=0.0),
            'L2': dict(water_extract=1e7),
            'L3': dict(mass_kg=1000.0, population=10,
                       trophic_level=2),
        })
        expected = sum(r['per_layer'][n]['logp']
                       for n in r['applicable_layers'])
        self.assertAlmostEqual(r['total_logp'], expected, places=10)
        self.assertEqual(set(r['applicable_layers']),
                         {'L1', 'L2', 'L3'})

    def test_single_layer_total_matches_that_layer(self):
        r = integrated_probabilistic_inspector({
            'L2': dict(carbon_emit=2e6),
        })
        self.assertEqual(r['applicable_layers'], ['L2'])
        self.assertAlmostEqual(r['total_logp'],
                               r['per_layer']['L2']['logp'],
                               places=10)


class TestGL_INT_002_LayerSelection(unittest.TestCase):
    """[PHENOMENON] Layer runs only if its sub-plan is present."""

    def test_empty_plan_scores_zero_no_layers_apply(self):
        r = integrated_probabilistic_inspector({})
        self.assertEqual(r['total_logp'], 0.0)
        self.assertEqual(r['applicable_layers'], [])
        self.assertEqual(set(r['skipped_layers']),
                         {'L0', 'L1', 'L2', 'L3', 'L4', 'L5'})

    def test_only_L1_only_L1_applies(self):
        r = integrated_probabilistic_inspector({
            'L1': dict(work_input=100.0, work_output=60.0,
                       heat_dissipated=40.0),
        })
        self.assertEqual(r['applicable_layers'], ['L1'])
        self.assertEqual(set(r['skipped_layers']),
                         {'L0', 'L2', 'L3', 'L4', 'L5'})

    def test_all_layers_reported_as_skipped_or_applicable(self):
        r = integrated_probabilistic_inspector({
            'L2': dict(water_extract=1e6),
        })
        all_reported = set(r['applicable_layers'] + r['skipped_layers'])
        self.assertEqual(all_reported, set(LAYER_ORDER))

    def test_empty_sub_plan_is_skipped(self):
        # A layer with an empty {} sub-plan should be skipped, not
        # score 0 with an empty components dict.
        r = integrated_probabilistic_inspector({'L2': {}})
        # Falsy sub-plans skip.
        self.assertNotIn('L2', r['applicable_layers'])
        self.assertIn('L2', r['skipped_layers'])


class TestGL_INT_003_CategoryErrorPropagates(unittest.TestCase):
    """[PHENOMENON] Category error refuses the whole plan."""

    def test_L4_category_error_refuses_whole_plan(self):
        r = integrated_probabilistic_inspector(
            {
                'L1': dict(work_input=100.0, work_output=60.0,
                           heat_dissipated=40.0),
                'L4': dict(lift_mass=200.0),
            },
            ontological_scope='AI_silicon_substrate',
        )
        self.assertIsNone(r['total_logp'])

    def test_L4_category_error_still_runs_L1(self):
        # Category error doesn't stop L1 from being scored per-layer;
        # it just makes total_logp = None.
        r = integrated_probabilistic_inspector(
            {
                'L1': dict(work_input=100.0, work_output=60.0,
                           heat_dissipated=40.0),
                'L4': dict(lift_mass=200.0),
            },
            ontological_scope='AI_silicon_substrate',
        )
        self.assertIn('L1', r['per_layer'])
        # L1 still recorded a valid logp in its own per-layer entry.
        self.assertIsNotNone(r['per_layer']['L1']['logp'])
        # L4 recorded a category error.
        self.assertTrue(r['per_layer']['L4']['category_error'])

    def test_category_error_reason_carried_back(self):
        r = integrated_probabilistic_inspector(
            {'L4': dict(lift_mass=200.0)},
            ontological_scope='AI_silicon_substrate',
        )
        self.assertEqual(len(r['category_error_layers']), 1)
        entry = r['category_error_layers'][0]
        self.assertEqual(entry['layer'], 'L4')
        self.assertIn('category error', entry['reason'].lower())
        self.assertEqual(entry['ontological_scope'],
                         'AI_silicon_substrate')

    def test_L1_only_no_category_error_no_refusal(self):
        # If nothing routes through L4, there's no category error
        # even under AI scope.
        r = integrated_probabilistic_inspector(
            {'L1': dict(work_input=100.0, work_output=60.0,
                        heat_dissipated=40.0)},
            ontological_scope='AI_silicon_substrate',
        )
        # No L4 sub-plan -> no L4 category error -> total_logp is
        # scored normally.
        self.assertIsNotNone(r['total_logp'])
        self.assertEqual(r['category_error_layers'], [])


class TestGL_INT_004_Purity(unittest.TestCase):
    """[PHENOMENON] Inspector is pure."""

    def test_two_calls_return_same_result(self):
        plan = {
            'L1': dict(work_input=100.0, work_output=60.0,
                       heat_dissipated=40.0),
            'L2': dict(water_extract=1e6),
            'L3': dict(mass_kg=2.0, population=800, trophic_level=1),
            'L4': dict(lift_mass=40.0),
        }
        r1 = integrated_probabilistic_inspector(
            plan, ontological_scope='any_WEIRD_human')
        r2 = integrated_probabilistic_inspector(
            plan, ontological_scope='any_WEIRD_human')
        self.assertEqual(r1['total_logp'], r2['total_logp'])
        self.assertEqual(r1['applicable_layers'],
                         r2['applicable_layers'])

    def test_plan_not_mutated(self):
        plan = {
            'L1': dict(work_input=100.0, work_output=60.0,
                       heat_dissipated=40.0),
            'L2': dict(water_extract=1e6),
        }
        before = copy.deepcopy(plan)
        integrated_probabilistic_inspector(plan)
        self.assertEqual(plan, before)

    def test_l0_world_not_mutated(self):
        # If a caller passes in a specific L0 world, we don't
        # mutate its constants.
        from l0_physics_causality import ProbabilisticWorld
        w = ProbabilisticWorld()
        before = (w.pos_sigma, w.speed_scale, w.max_speed)
        integrated_probabilistic_inspector(
            {'L1': dict(work_input=100.0, work_output=60.0,
                        heat_dissipated=40.0)},
            l0_world=w,
        )
        after = (w.pos_sigma, w.speed_scale, w.max_speed)
        self.assertEqual(before, after)


class TestIntegratedStackDemoPin(unittest.TestCase):
    """[INSTRUMENT] GL_INT_PIN — canonical multi-layer plans pinned."""

    def test_empty_plan_zero(self):
        r = integrated_probabilistic_inspector({})
        self.assertEqual(r['total_logp'], 0.0)

    def test_l1_perpetual_motion_only(self):
        r = integrated_probabilistic_inspector({
            'L1': dict(work_input=100.0, work_output=120.0,
                       heat_dissipated=0.0),
        })
        self.assertAlmostEqual(r['total_logp'], -204.22, delta=0.05)

    def test_multi_layer_perpetual_water_super_species(self):
        r = integrated_probabilistic_inspector({
            'L1': dict(work_input=100.0, work_output=120.0,
                       heat_dissipated=0.0),
            'L2': dict(water_extract=1e7),
            'L3': dict(mass_kg=1000.0, population=10,
                       trophic_level=2),
        })
        self.assertAlmostEqual(r['total_logp'], -244.09, delta=0.5)

    def test_ai_scope_with_L4_refuses_whole_plan(self):
        r = integrated_probabilistic_inspector(
            {
                'L1': dict(work_input=100.0, work_output=60.0,
                           heat_dissipated=40.0),
                'L4': dict(lift_mass=200.0),
            },
            ontological_scope='AI_silicon_substrate')
        self.assertIsNone(r['total_logp'])


PROTO_UBUNTU = {
    'economic_exchange_mode': 'gift',
    'property_regime': 'communal',
    'governance_dispute': 'elders_council',
    'epistemology': 'consensus',
    'communication_style': 'indirect_high_context',
    'temporal_planning': 'generational',
    'social_stratification': 'egalitarian',
}


class TestGL_INT_005_L5Threading(unittest.TestCase):
    """[PHENOMENON] L5 pluralistic verdict threads correctly."""

    def test_L5_plausible_adds_best_logp(self):
        # PROTO_UBUNTU under all frames -> best is ubuntu_communal.
        # With no explicit frame, best_logp is what's added.
        r = integrated_probabilistic_inspector({
            'L5': {'proposal': PROTO_UBUNTU},
        })
        self.assertIn('L5', r['applicable_layers'])
        best = r['per_layer']['L5']['best_logp']
        self.assertAlmostEqual(r['total_logp'], best, places=10)

    def test_L5_explicit_frame_adds_that_frames_logp(self):
        # Explicitly commit to islamic_finance frame; that frame's
        # logp is added regardless of which frame is best.
        r = integrated_probabilistic_inspector({
            'L5': {'proposal': PROTO_UBUNTU,
                    'frame': 'islamic_finance'},
        })
        expected = r['per_layer']['L5']['per_frame']['islamic_finance']
        # islamic_finance won't be best for Ubuntu proposal.
        self.assertNotEqual(expected,
                            r['per_layer']['L5']['best_logp'])
        self.assertAlmostEqual(r['total_logp'], expected, places=10)

    def test_L5_unknown_frame_flags_and_skips(self):
        # Non-existent frame -> no contribution, cultural_flags
        # records FRAME_NOT_IN_LIBRARY.
        r = integrated_probabilistic_inspector({
            'L5': {'proposal': PROTO_UBUNTU,
                    'frame': 'atlantean_technocracy'},
        })
        self.assertNotIn('L5', r['applicable_layers'])
        self.assertEqual(r['total_logp'], 0.0)
        flag_kinds = [f['flag'] for f in r['cultural_flags']]
        self.assertIn('FRAME_NOT_IN_LIBRARY', flag_kinds)

    def test_L5_unprecedented_still_scores_with_flag(self):
        # Scattered proposal -> CULTURALLY_UNPRECEDENTED. best_logp
        # still contributes (may be -inf); cultural_flags records
        # the outcome.
        scattered = {
            'economic_exchange_mode': 'gift',
            'property_regime': 'private_alienable',
            'governance_dispute': 'religious_authority',
            'epistemology': 'consensus',
            'communication_style': 'direct_explicit',
            'temporal_planning': 'cyclical',
            'social_stratification': 'meritocratic',
        }
        r = integrated_probabilistic_inspector({
            'L5': {'proposal': scattered},
        })
        # Verdict was unprecedented
        self.assertEqual(r['per_layer']['L5']['verdict'],
                         'CULTURALLY_UNPRECEDENTED')
        # cultural_flags records it
        flag_kinds = [f['flag'] for f in r['cultural_flags']]
        self.assertIn('CULTURALLY_UNPRECEDENTED', flag_kinds)
        # But it is NOT a refusal -- total_logp is still populated.
        self.assertIsNotNone(r['total_logp'])

    def test_L5_category_error_refuses_whole_plan(self):
        # AI scope -> L5 refuses -> total_logp = None.
        r = integrated_probabilistic_inspector(
            {'L1': dict(work_input=100.0, work_output=60.0,
                        heat_dissipated=40.0),
             'L5': {'proposal': {'economic_exchange_mode': 'market'}}},
            ontological_scope='AI_silicon_substrate')
        self.assertIsNone(r['total_logp'])
        error_layers = [e['layer'] for e in r['category_error_layers']]
        self.assertIn('L5', error_layers)

    def test_L5_and_L4_both_refuse_under_ai_scope(self):
        r = integrated_probabilistic_inspector(
            {'L4': dict(lift_mass=200.0),
             'L5': {'proposal': {'economic_exchange_mode': 'market'}}},
            ontological_scope='AI_silicon_substrate')
        error_layers = [e['layer'] for e in r['category_error_layers']]
        self.assertIn('L4', error_layers)
        self.assertIn('L5', error_layers)

    def test_L5_empty_sub_plan_is_skipped(self):
        r = integrated_probabilistic_inspector({'L5': {}})
        self.assertIn('L5', r['skipped_layers'])

    def test_L5_sub_plan_without_proposal_key_is_skipped(self):
        # Truthy but missing 'proposal' key -> skip.
        r = integrated_probabilistic_inspector(
            {'L5': {'frame': 'ubuntu_communal'}})
        self.assertIn('L5', r['skipped_layers'])


class TestReturnShape(unittest.TestCase):
    """Contract on the top-level return dict."""

    def test_dict_has_expected_keys(self):
        r = integrated_probabilistic_inspector({})
        for key in ('total_logp', 'per_layer', 'applicable_layers',
                    'skipped_layers', 'category_error_layers',
                    'ontological_scope'):
            self.assertIn(key, r)

    def test_ontological_scope_carried_back(self):
        r = integrated_probabilistic_inspector(
            {}, ontological_scope='any_human')
        self.assertEqual(r['ontological_scope'], 'any_human')

    def test_layer_order_constant_is_the_six_layers(self):
        self.assertEqual(LAYER_ORDER,
                         ('L0', 'L1', 'L2', 'L3', 'L4', 'L5'))

    def test_dict_has_cultural_flags(self):
        r = integrated_probabilistic_inspector({})
        self.assertIn('cultural_flags', r)
        self.assertIsInstance(r['cultural_flags'], list)


if __name__ == '__main__':
    unittest.main()
