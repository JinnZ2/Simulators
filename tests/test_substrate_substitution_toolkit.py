"""
Tests for the substrate_substitution_toolkit module.

License: CC0
Dependencies: stdlib only (unittest)
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.substrate_substitution_toolkit import (
    SUBSTITUTION_CATEGORIES,
    apply_substitution,
    test_claim_with_substitution,
    find_best_ecological_match,
    evaluate_balanced_view,
    categorize_claim_honesty,
    evaluate_substrate_narrative_claim,
)


class TestCategoryShape(unittest.TestCase):
    """Every category must have description + non-empty examples,
    and every example must carry the four required keys."""

    REQUIRED_CATEGORIES = {
        'pure_consumer', 'commensal', 'symbiotic', 'reach_amplifier',
        'parasitic', 'mutualistic_scale', 'cascading_dynamics',
    }
    EXAMPLE_KEYS = {'substrate', 'narrative', 'relationship', 'reality_check'}

    def test_all_seven_categories_present(self):
        self.assertEqual(set(SUBSTITUTION_CATEGORIES.keys()),
                         self.REQUIRED_CATEGORIES)

    def test_every_category_has_description_and_examples(self):
        for name, data in SUBSTITUTION_CATEGORIES.items():
            self.assertIn('description', data, name)
            self.assertIn('examples', data, name)
            self.assertGreater(len(data['examples']), 0, name)

    def test_every_example_has_required_keys(self):
        for cat_name, data in SUBSTITUTION_CATEGORIES.items():
            for i, ex in enumerate(data['examples']):
                with self.subTest(category=cat_name, index=i):
                    self.assertEqual(set(ex.keys()), self.EXAMPLE_KEYS)
                    for key in self.EXAMPLE_KEYS:
                        self.assertTrue(ex[key])


class TestApplySubstitution(unittest.TestCase):
    def test_simple_word_substitution(self):
        sub = SUBSTITUTION_CATEGORIES['pure_consumer']['examples'][0]
        out = apply_substitution('substrate sustains itself', sub)
        self.assertIn('grass', out)

    def test_compound_substrate_populations_phrase(self):
        sub = SUBSTITUTION_CATEGORIES['pure_consumer']['examples'][0]
        out = apply_substitution('substrate populations grow', sub)
        # Must not strand as 'grass populations'; needs the community
        # rewrite.
        self.assertIn('grass community', out)
        self.assertNotIn('grass populations', out)

    def test_compound_narrative_populations_phrase(self):
        sub = SUBSTITUTION_CATEGORIES['pure_consumer']['examples'][0]
        out = apply_substitution('narrative populations grow', sub)
        self.assertIn('grasshoppers group', out)

    def test_empty_string_passes_through(self):
        sub = SUBSTITUTION_CATEGORIES['pure_consumer']['examples'][0]
        self.assertEqual(apply_substitution('', sub), '')

    def test_no_substrate_or_narrative_unchanged(self):
        sub = SUBSTITUTION_CATEGORIES['pure_consumer']['examples'][0]
        text = 'reproducibility failure rate exceeds 50 percent'
        self.assertEqual(apply_substitution(text, sub), text)


class TestTestClaimWithSubstitution(unittest.TestCase):
    def test_runs_against_every_example_when_no_category(self):
        report = test_claim_with_substitution('narrative supports substrate')
        total_examples = sum(len(c['examples'])
                             for c in SUBSTITUTION_CATEGORIES.values())
        self.assertEqual(len(report['tests']), total_examples)

    def test_filters_by_category(self):
        report = test_claim_with_substitution(
            'narrative supports substrate', category='pure_consumer')
        self.assertEqual(
            len(report['tests']),
            len(SUBSTITUTION_CATEGORIES['pure_consumer']['examples']),
        )
        for t in report['tests']:
            self.assertEqual(t['category'], 'pure_consumer')

    def test_unknown_category_raises(self):
        with self.assertRaises(ValueError):
            test_claim_with_substitution('claim', category='not_a_category')

    def test_each_test_carries_full_metadata(self):
        report = test_claim_with_substitution(
            'narrative supports substrate', category='symbiotic')
        for t in report['tests']:
            self.assertIn('transformed_claim', t)
            self.assertIn('ecological_relationship', t)
            self.assertIn('reality_check', t)


class TestFindBestEcologicalMatch(unittest.TestCase):
    def test_amplify_maps_to_reach_amplifier(self):
        report = find_best_ecological_match(['amplify'])
        cats = [m['matched_category']
                for m in report['category_suggestions']]
        self.assertIn('reach_amplifier', cats)

    def test_consume_maps_to_pure_consumer(self):
        report = find_best_ecological_match(['consume'])
        cats = [m['matched_category']
                for m in report['category_suggestions']]
        self.assertIn('pure_consumer', cats)

    def test_unknown_keyword_yields_no_match(self):
        report = find_best_ecological_match(['parasitology'])
        # 'parasitology' contains 'parasit' which substrings... well,
        # actually no, 'parasitology' contains nothing in _KEYWORD_TO_CATEGORY
        # because the table keys are short verbs. Confirm zero matches.
        self.assertEqual(report['category_suggestions'], [])


class TestEvaluateBalancedView(unittest.TestCase):
    def test_returns_seven_steps(self):
        ev = evaluate_balanced_view('narrative supports substrate')
        self.assertEqual(len(ev['evaluation_steps']), 7)

    def test_steps_cover_each_substitution_category(self):
        ev = evaluate_balanced_view('narrative supports substrate')
        # The first six steps each pull a sample from a category;
        # step 7 is the synthesis. Verify the categories referenced.
        sampled_categories = {
            step['instruction'].split('against ')[1].split(' ')[0]
            for step in ev['evaluation_steps'][:6]
        }
        self.assertEqual(sampled_categories, {
            'PURE_CONSUMER', 'PARASITIC', 'COMMENSAL', 'SYMBIOTIC',
            'REACH_AMPLIFIER', 'MUTUALISTIC_SCALE',
        })

    def test_includes_common_errors_list(self):
        ev = evaluate_balanced_view('narrative supports substrate')
        self.assertGreaterEqual(len(ev['common_errors']), 4)


class TestCategorizeClaimHonesty(unittest.TestCase):
    def test_returns_default_methodology(self):
        framework = categorize_claim_honesty()
        self.assertIn('PURE_CONSUMER', framework['methodology'])
        self.assertIn('narrative_instinct_bias_indicators',
                      framework['evaluation_framework'])


class TestMainEntryPoint(unittest.TestCase):
    def test_evaluate_substrate_narrative_claim_returns_full_shape(self):
        out = evaluate_substrate_narrative_claim(
            'scale_builder narrative amplifies substrate reach')
        self.assertIn('claim', out)
        self.assertIn('all_category_tests', out)
        self.assertIn('balanced_view', out)
        self.assertIn('honesty_framework', out)
        self.assertIn('final_instruction', out)


if __name__ == '__main__':
    unittest.main()
