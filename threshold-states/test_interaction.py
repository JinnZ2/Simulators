# SPDX-License-Identifier: CC0-1.0
"""Checks for interaction.py: one case per row, the band edges, step 0.

Fixture: separate = [3, 7], so S = 10, M = 7; tol = 1. S - M = 3 > 2*tol.
Bands: ANTAG (<6)  REDUNDANT [6, 8]  ENH (8, 9)  ADDITIVE [9, 11]  RESONANT (>11).
Integers and halves are exact in binary, so every edge below is tested
exactly; the sweep uses Fraction.

SELF-GRADED: the module and these checks share an author, so a pass is a
regression result, not validation.

Run: python3 threshold-states/test_interaction.py
"""
import os
import subprocess
import sys
import unittest
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interaction as ix  # noqa: E402

SEP, TOL = [3, 7], 1


def rel(joint, sep=SEP, tol=TOL):
    return ix.classify(joint, sep, tol)["relation"]


class OnePerRow(unittest.TestCase):

    def test_row0_below_resolution(self):
        self.assertEqual(rel(8, [1, 7]), ix.BELOW_RESOLUTION)   # S-M = 1 < 2

    def test_row1_redundant(self):
        self.assertEqual(rel(7), ix.REDUNDANT)

    def test_row2_additive(self):
        self.assertEqual(rel(10), ix.ADDITIVE)

    def test_row3_resonant(self):
        self.assertEqual(rel(12), ix.RESONANT)

    def test_row4_enhanced_subadditive(self):
        self.assertEqual(rel(8.5), ix.ENHANCED_SUBADDITIVE)

    def test_row5_antagonistic(self):
        self.assertEqual(rel(4), ix.ANTAGONISTIC)

    def test_step_numbers(self):
        got = [ix.classify(j, SEP, TOL)["step"] for j in (7, 10, 12, 8.5, 4)]
        self.assertEqual(got, [1, 2, 3, 4, 5])
        self.assertEqual(ix.classify(8, [1, 7], 1)["step"], 0)


class Boundaries(unittest.TestCase):

    def test_M_minus_tol_is_redundant_and_below_is_antagonistic(self):
        self.assertEqual(rel(6), ix.REDUNDANT)
        self.assertEqual(rel(5.5), ix.ANTAGONISTIC)

    def test_M_plus_tol_is_redundant_and_above_is_enhanced(self):
        self.assertEqual(rel(8), ix.REDUNDANT)
        self.assertEqual(rel(8.25), ix.ENHANCED_SUBADDITIVE)

    def test_S_minus_tol_is_additive_and_below_is_enhanced(self):
        self.assertEqual(rel(9), ix.ADDITIVE)
        self.assertEqual(rel(8.75), ix.ENHANCED_SUBADDITIVE)

    def test_S_plus_tol_is_additive_and_above_is_resonant(self):
        self.assertEqual(rel(11), ix.ADDITIVE)
        self.assertEqual(rel(11.5), ix.RESONANT)

    def test_S_minus_M_equal_2tol_is_below_resolution(self):
        # [2, 7]: S - M = 2 = 2*tol. The bands [6, 8] and [8, 10] touch at 8.
        for j in (5, 7, 8, 9, 12):
            self.assertEqual(rel(j, [2, 7]), ix.BELOW_RESOLUTION, j)

    def test_S_minus_M_just_above_2tol_resolves(self):
        # [2.5, 7]: S - M = 2.5 > 2. ENH band (8, 8.5) is open and non-empty.
        self.assertEqual(rel(8.25, [2.5, 7]), ix.ENHANCED_SUBADDITIVE)
        self.assertEqual(rel(8, [2.5, 7]), ix.REDUNDANT)
        self.assertEqual(rel(8.5, [2.5, 7]), ix.ADDITIVE)


class Correction(unittest.TestCase):

    def test_joint_equal_S_is_additive_not_subadditive(self):
        self.assertEqual(rel(10), ix.ADDITIVE)
        self.assertEqual(rel(10, tol=0), ix.ADDITIVE)

    def test_additive_has_I_near_zero(self):
        r = ix.classify(10, SEP, TOL)
        self.assertEqual(r["I"], 0)


class ZeroTolerance(unittest.TestCase):

    def test_tol_zero_rows(self):
        cases = {7: ix.REDUNDANT, 10: ix.ADDITIVE, 11: ix.RESONANT,
                 8: ix.ENHANCED_SUBADDITIVE, 6: ix.ANTAGONISTIC}
        for j, want in cases.items():
            self.assertEqual(rel(j, tol=0), want, j)

    def test_tol_zero_one_cue_silent_is_below_resolution(self):
        self.assertEqual(rel(7, [0, 7], 0), ix.BELOW_RESOLUTION)


class DisjointAndExhaustive(unittest.TestCase):

    def test_sweep_every_point_gets_one_row_and_every_row_occurs(self):
        seen = set()
        for sep, tol in (([3, 7], 1), ([F(5, 2), 7], 1), ([1, 2, 7], F(1, 2)),
                         ([3, 7], 0), ([F(21, 10), 7], F(1, 20))):
            S, M = ix.references(sep)
            j = F(-5)
            while j <= 20:
                r = ix.classify(j, sep, tol)            # raises if 0 or 2+ rows
                seen.add(r["relation"])
                j += F(1, 8)
        self.assertEqual(seen, set(ix.RELATIONS))


class NumberTypes(unittest.TestCase):

    def test_decimal_and_fraction_are_accepted(self):
        from decimal import Decimal as D
        self.assertEqual(rel(D("8.5"), [D(3), D(7)], D(1)),
                         ix.ENHANCED_SUBADDITIVE)
        self.assertEqual(rel(F(17, 2), [3, 7], F(1)), ix.ENHANCED_SUBADDITIVE)


class NotRelations(unittest.TestCase):

    def test_undeclared_tol_is_unrated_not_zero(self):
        r = ix.classify(10, SEP, None)
        self.assertEqual(r["relation"], ix.UNRATED)
        self.assertIsNone(r["step"])
        self.assertNotEqual(rel(10, tol=0), ix.UNRATED)

    def test_unrated_precedes_step0(self):
        self.assertEqual(ix.classify(8, [1, 7], None)["relation"], ix.UNRATED)

    def test_antagonistic_is_the_open_class(self):
        self.assertEqual(ix.OPEN_CLASSES, (ix.ANTAGONISTIC,))


class Refusals(unittest.TestCase):

    def test_bad_inputs_raise(self):
        bad = [(10, SEP, -1), (float("nan"), SEP, 1), (10, [7], 1),
               (10, [], 1), (10, [3, float("inf")], 1), (10, SEP, "1"),
               ("10", SEP, 1), (10, SEP, True)]
        for args in bad:
            with self.assertRaises(ix.InteractionError, msg=repr(args)):
                ix.classify(*args)

    def test_module_refuses_selftest(self):
        p = subprocess.run([sys.executable, os.path.join(HERE, "interaction.py"),
                            "--selftest"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("test_interaction.py", p.stderr)


if __name__ == "__main__":
    unittest.main()
