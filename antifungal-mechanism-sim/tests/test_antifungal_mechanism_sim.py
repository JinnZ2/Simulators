"""
Tests for the antifungal mechanism discovery simulator.

The module exposes a Mechanism class, a scoring evaluate() method, and a
random crossover() function. The `main()` menu loop is interactive
(reads stdin) and is not exercised here; the tests cover the deterministic
surface (data, math) and pin the crossover invariants under a seeded RNG.

License: CC0
Dependencies: stdlib only (unittest)
"""

import os
import random
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antifungal_mechanism_sim import (
    INTERACTIONS,
    Mechanism,
    crossover,
)


class TestInteractionsShape(unittest.TestCase):
    EXPECTED_CODES = {'CW', 'EG', 'MD', 'PS', 'NA', 'SS', 'QP'}
    REQUIRED_FIELDS = {'name', 'efficacy', 'toxicity', 'resistance'}

    def test_seven_expected_codes(self):
        self.assertEqual(set(INTERACTIONS.keys()), self.EXPECTED_CODES)

    def test_every_entry_has_required_fields(self):
        for code, data in INTERACTIONS.items():
            with self.subTest(code=code):
                self.assertEqual(set(data.keys()), self.REQUIRED_FIELDS)

    def test_scores_are_non_negative_integers(self):
        for code, data in INTERACTIONS.items():
            with self.subTest(code=code):
                for field in ('efficacy', 'toxicity', 'resistance'):
                    self.assertIsInstance(data[field], int)
                    self.assertGreaterEqual(data[field], 0)


class TestMechanismEvaluate(unittest.TestCase):
    def test_empty_mechanism_scores_zero(self):
        m = Mechanism()
        self.assertEqual(m.evaluate(), (0, 0, 0, 0))

    def test_single_interaction_matches_data(self):
        m = Mechanism(['CW'])
        cw = INTERACTIONS['CW']
        eff, tox, res, score = m.evaluate()
        self.assertEqual(eff, cw['efficacy'])
        self.assertEqual(tox, cw['toxicity'])
        self.assertEqual(res, cw['resistance'])
        self.assertEqual(score, cw['efficacy'] - cw['toxicity'] - cw['resistance'])

    def test_multiple_interactions_sum(self):
        m = Mechanism(['CW', 'SS'])
        cw, ss = INTERACTIONS['CW'], INTERACTIONS['SS']
        eff, tox, res, score = m.evaluate()
        self.assertEqual(eff, cw['efficacy'] + ss['efficacy'])
        self.assertEqual(tox, cw['toxicity'] + ss['toxicity'])
        self.assertEqual(res, cw['resistance'] + ss['resistance'])
        self.assertEqual(score, eff - tox - res)

    def test_duplicate_interactions_are_deduplicated(self):
        # The class stores a set, so passing duplicates should collapse.
        m = Mechanism(['CW', 'CW', 'CW'])
        self.assertEqual(len(m.interactions), 1)
        cw = INTERACTIONS['CW']
        self.assertEqual(m.evaluate(),
                         (cw['efficacy'], cw['toxicity'], cw['resistance'],
                          cw['efficacy'] - cw['toxicity'] - cw['resistance']))


class TestMechanismStr(unittest.TestCase):
    def test_empty_mechanism_prints_none_marker(self):
        m = Mechanism(name='empty')
        s = str(m)
        self.assertIn('empty', s)
        self.assertIn('none', s)

    def test_named_mechanism_includes_all_scores(self):
        m = Mechanism(['CW', 'SS'], name='paired')
        s = str(m)
        self.assertIn('paired', s)
        for label in ('Efficacy', 'Toxicity', 'Resistance', 'OVERALL SCORE'):
            self.assertIn(label, s)


class TestCrossover(unittest.TestCase):
    def test_both_parents_empty_yields_empty_offspring(self):
        a = Mechanism()
        b = Mechanism()
        child = crossover(a, b, 'child')
        self.assertEqual(child.interactions, set())
        self.assertEqual(child.name, 'child')

    def test_offspring_only_uses_parent_genes(self):
        # Offspring should never contain a code that is not in either parent.
        random.seed(42)
        a = Mechanism(['CW', 'MD'])
        b = Mechanism(['SS', 'QP'])
        union = a.interactions.union(b.interactions)
        for _ in range(100):
            child = crossover(a, b)
            self.assertTrue(child.interactions.issubset(union))

    def test_offspring_has_at_least_one_interaction_when_union_nonempty(self):
        random.seed(7)
        a = Mechanism(['CW'])
        b = Mechanism(['MD'])
        for _ in range(20):
            child = crossover(a, b)
            self.assertGreater(len(child.interactions), 0)

    def test_offspring_size_bounded_by_union(self):
        random.seed(0)
        a = Mechanism(['CW', 'MD', 'PS'])
        b = Mechanism(['SS', 'QP', 'NA'])
        union_size = len(a.interactions.union(b.interactions))
        for _ in range(50):
            child = crossover(a, b)
            self.assertLessEqual(len(child.interactions), union_size)

    def test_crossover_is_deterministic_under_seed(self):
        # Same seed + same parents -> same child.
        a = Mechanism(['CW', 'EG', 'SS'])
        b = Mechanism(['MD', 'PS'])
        random.seed(123)
        first = crossover(a, b, 'x').interactions
        random.seed(123)
        second = crossover(a, b, 'x').interactions
        self.assertEqual(first, second)

    def test_offspring_name_preserved(self):
        a = Mechanism(['CW'])
        b = Mechanism(['MD'])
        child = crossover(a, b, 'custom_name')
        self.assertEqual(child.name, 'custom_name')


if __name__ == '__main__':
    unittest.main()
