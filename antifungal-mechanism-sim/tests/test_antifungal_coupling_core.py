"""
Tests for the coupling-topology version of the antifungal scorer.

The coupling core replaces the additive scalar of the original simulator
with a signed pairwise efficacy matrix and multiplicative resistance across
orthogonal axes. The tests pin:

  - shape of TARGETS (7 codes, all required fields including the new p_res
    in [0, 1] and axis label)
  - _j symmetry (order-agnostic pair lookup) and default-zero
  - efficacy math on the three components (within-axis redundancy discount,
    cross-axis synergy, signed antagonism)
  - resistance_prob shape (empty is identity 1.0; same-axis takes the min;
    orthogonal axes multiply)
  - the rank-flip claim in the demo: additive_score REJECTS (CW, NA, SS)
    with a negative number; fitness ACCEPTS it with a positive number that
    beats the additive top candidate under the shipped weights

License: CC0
Dependencies: stdlib only (unittest)
"""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from antifungal_coupling_core import (
    DEMO,
    J,
    TARGETS,
    _j,
    additive_score,
    efficacy,
    fitness,
    resistance_prob,
    toxicity,
)


class TestTargetsShape(unittest.TestCase):
    EXPECTED_CODES = {'CW', 'EG', 'MD', 'PS', 'NA', 'SS', 'QP'}
    REQUIRED_FIELDS = {'name', 'eff', 'tox', 'res_old', 'p_res', 'axis'}

    def test_seven_expected_codes(self):
        self.assertEqual(set(TARGETS), self.EXPECTED_CODES)

    def test_every_entry_has_required_fields(self):
        for code, data in TARGETS.items():
            with self.subTest(code=code):
                self.assertEqual(set(data), self.REQUIRED_FIELDS)

    def test_p_res_in_unit_interval(self):
        for code, data in TARGETS.items():
            self.assertGreaterEqual(data['p_res'], 0.0)
            self.assertLessEqual(data['p_res'], 1.0)

    def test_shared_sterol_axis_documented(self):
        # EG and MD share the sterol axis by design -- this drives the
        # antagonism + no-product-bonus penalty in the demo.
        self.assertEqual(TARGETS['EG']['axis'], TARGETS['MD']['axis'])
        self.assertEqual(TARGETS['EG']['axis'], 'sterol')

    def test_all_other_targets_are_on_distinct_axes(self):
        # Only EG and MD share an axis; every other axis is unique.
        non_sterol = [t for t, d in TARGETS.items() if d['axis'] != 'sterol']
        axes = [TARGETS[t]['axis'] for t in non_sterol]
        self.assertEqual(len(axes), len(set(axes)))


class TestCouplingLookup(unittest.TestCase):
    def test_j_returns_zero_for_uncoupled_pair(self):
        # There is no J entry for (CW, NA); default must be 0.0.
        self.assertEqual(_j('CW', 'NA'), 0.0)
        self.assertEqual(_j('NA', 'CW'), 0.0)

    def test_j_is_order_agnostic(self):
        for (a, b), value in J.items():
            self.assertEqual(_j(a, b), value)
            self.assertEqual(_j(b, a), value)

    def test_azole_polyene_antagonism_is_negative(self):
        # The clinically-motivated antagonism between EG (azole) and MD
        # (polyene) is the demo's rank-flip pivot on the antagonism side.
        self.assertLess(_j('EG', 'MD'), 0.0)

    def test_echinocandin_azole_is_synergy(self):
        self.assertGreater(_j('CW', 'EG'), 0.0)


class TestEfficacy(unittest.TestCase):
    def test_empty_set_scores_zero(self):
        self.assertEqual(efficacy(set()), 0.0)

    def test_single_target_returns_its_efficacy(self):
        for code, data in TARGETS.items():
            with self.subTest(code=code):
                self.assertAlmostEqual(efficacy({code}), float(data['eff']),
                                       places=10)

    def test_within_axis_redundancy_discount(self):
        # {EG (eff 7), MD (eff 8)}: shared sterol axis, so base is
        #   max + 0.5*rest = 8 + 0.5*7 = 11.5
        # Plus antagonism -0.6*sqrt(7*8) = -0.6*sqrt(56).
        expected_base = 8 + 0.5 * 7
        expected_syn = -0.6 * math.sqrt(7 * 8)
        self.assertAlmostEqual(efficacy({'EG', 'MD'}),
                               expected_base + expected_syn, places=10)

    def test_orthogonal_axes_no_redundancy_discount(self):
        # {CW (cell_wall, eff 9), EG (sterol, eff 7)}: distinct axes ->
        #   base = 9 + 7 = 16.
        # Synergy +0.4 * sqrt(9*7).
        expected_base = 9 + 7
        expected_syn = 0.4 * math.sqrt(9 * 7)
        self.assertAlmostEqual(efficacy({'CW', 'EG'}),
                               expected_base + expected_syn, places=10)

    def test_three_orthogonal_targets_pick_up_only_present_couplings(self):
        # {CW, NA, SS}: all orthogonal, base = 9+5+4 = 18.
        # Present pair with a J entry: (SS, CW) = +0.4. Others: 0.
        expected_base = 9 + 5 + 4
        expected_syn = 0.4 * math.sqrt(9 * 4)
        self.assertAlmostEqual(efficacy({'CW', 'NA', 'SS'}),
                               expected_base + expected_syn, places=10)


class TestToxicity(unittest.TestCase):
    def test_empty_set_is_zero(self):
        self.assertEqual(toxicity(set()), 0)

    def test_sum_over_members(self):
        self.assertEqual(toxicity({'CW', 'NA', 'SS'}),
                         TARGETS['CW']['tox'] + TARGETS['NA']['tox']
                         + TARGETS['SS']['tox'])


class TestResistanceProb(unittest.TestCase):
    def test_empty_set_returns_identity(self):
        # Empty product = 1.0 (the identity), reflecting "no chosen target,
        # organism has nothing to resist against."
        self.assertEqual(resistance_prob(set()), 1.0)

    def test_single_target_returns_its_p_res(self):
        for code, data in TARGETS.items():
            with self.subTest(code=code):
                self.assertAlmostEqual(resistance_prob({code}),
                                       data['p_res'], places=10)

    def test_within_axis_uses_min_not_product(self):
        # EG (p_res 0.60) and MD (p_res 0.20) share the sterol axis.
        # Cross-resistance rule: min(0.60, 0.20) = 0.20, NOT their product.
        self.assertAlmostEqual(resistance_prob({'EG', 'MD'}), 0.20,
                               places=10)

    def test_orthogonal_axes_multiply(self):
        # CW (0.40), NA (0.70), SS (0.30) -- three orthogonal axes.
        expected = 0.40 * 0.70 * 0.30
        self.assertAlmostEqual(resistance_prob({'CW', 'NA', 'SS'}),
                               expected, places=10)


class TestFitnessAndAdditive(unittest.TestCase):
    def test_additive_matches_original_formula(self):
        S = {'CW', 'NA', 'SS'}
        expected = (sum(TARGETS[t]['eff'] for t in S)
                    - sum(TARGETS[t]['tox'] for t in S)
                    - sum(TARGETS[t]['res_old'] for t in S))
        self.assertEqual(additive_score(S), expected)

    def test_fitness_default_weights_match_demo(self):
        # Reproduce the shipped demo's numbers to two decimal places, so
        # any silent change to default weights (w_tox=1, w_res=12, c=1)
        # surfaces as a test failure.
        results = {label: (round(additive_score(S), 1),
                           round(fitness(S), 2),
                           round(resistance_prob(S), 3))
                   for label, S in DEMO}
        self.assertEqual(results['azole+polyene  (EG,MD)'],
                         (-3.0, -6.39, 0.200))
        self.assertEqual(results['echinocandin+azole  (CW,EG)'],
                         (1.0, 10.29, 0.240))
        self.assertEqual(results['echinocandin+5FC+Hsp90 (CW,NA,SS)'],
                         (-3.0, 10.39, 0.084))
        self.assertEqual(results['all seven'],
                         (-10.0, 22.89, 0.003))


class TestRankFlipClaim(unittest.TestCase):
    """The load-bearing claim of the coupling core: the additive scorer and
    the coupling scorer disagree on the SIGN of the top candidate, and the
    coupling scorer's answer is the clinically correct one (three
    orthogonal axes multiply escape probability into single digits)."""

    ORTHOGONAL_TRIPLE = {'CW', 'NA', 'SS'}
    AZOLE_POLYENE = {'EG', 'MD'}

    def test_additive_rejects_the_orthogonal_triple(self):
        self.assertLess(additive_score(self.ORTHOGONAL_TRIPLE), 0.0)

    def test_coupled_accepts_the_orthogonal_triple(self):
        self.assertGreater(fitness(self.ORTHOGONAL_TRIPLE), 0.0)

    def test_orthogonal_triple_resistance_is_tiny(self):
        # Three orthogonal axes multiply 0.40 * 0.70 * 0.30 -> ~0.084.
        self.assertLess(resistance_prob(self.ORTHOGONAL_TRIPLE), 0.10)

    def test_azole_polyene_is_penalized_more_by_coupling_than_additive(self):
        # Antagonism + shared sterol axis (no product bonus) makes the
        # coupled model strictly harsher than the additive model on this
        # combination.
        self.assertLess(fitness(self.AZOLE_POLYENE),
                        additive_score(self.AZOLE_POLYENE))

    def test_orthogonal_triple_beats_azole_polyene_under_coupling(self):
        # Under the additive model both score -3 and are indistinguishable.
        # Under coupling the orthogonal triple wins by an order of magnitude.
        self.assertGreater(fitness(self.ORTHOGONAL_TRIPLE),
                           fitness(self.AZOLE_POLYENE))
        self.assertGreater(
            fitness(self.ORTHOGONAL_TRIPLE) - fitness(self.AZOLE_POLYENE),
            10.0,
        )


if __name__ == '__main__':
    unittest.main()
