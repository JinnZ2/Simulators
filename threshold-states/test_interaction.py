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


def cls(joint, sep, tol):
    """classify() with a bare-number tol read as absolute. The tests below
    were written in the response's own units; the module itself refuses a
    bare number (see Tolerance)."""
    if tol is not None and not isinstance(tol, dict):
        tol = ix.absolute(tol)
    return ix.classify(joint, sep, tol)


def rel(joint, sep=SEP, tol=TOL):
    return cls(joint, sep, tol)["relation"]


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
        got = [cls(j, SEP, TOL)["step"] for j in (7, 10, 12, 8.5, 4)]
        self.assertEqual(got, [1, 2, 3, 4, 5])
        self.assertEqual(cls(8, [1, 7], 1)["step"], 0)


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
        r = cls(10, SEP, TOL)
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
                r = cls(j, sep, tol)            # raises if 0 or 2+ rows
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
        r = cls(10, SEP, None)
        self.assertEqual(r["relation"], ix.UNRATED)
        self.assertIsNone(r["step"])
        self.assertNotEqual(rel(10, tol=0), ix.UNRATED)

    def test_unrated_precedes_step0(self):
        self.assertEqual(cls(8, [1, 7], None)["relation"], ix.UNRATED)

    def test_antagonistic_is_the_open_class(self):
        self.assertEqual(ix.OPEN_CLASSES, (ix.ANTAGONISTIC,))


def pre_split(joint, sep, tol):
    """The rule before the cue-sign split: S = sum of all cues, M = max of
    all cues, step 0 on S - M. Same rows. The archived root build
    (archive/interaction_class/) implements this rule."""
    S, M = sum(sep), max(sep)
    if S - M <= 2 * tol:
        return ix.BELOW_RESOLUTION
    for name, cond in ((ix.REDUNDANT, abs(joint - M) <= tol),
                       (ix.ADDITIVE, abs(joint - S) <= tol),
                       (ix.RESONANT, joint > S + tol),
                       (ix.ENHANCED_SUBADDITIVE, M + tol < joint < S - tol),
                       (ix.ANTAGONISTIC, joint < M - tol)):
        if cond:
            return name


SIGNED = ([3, 7, -1], [3, 7, -2], [3, 7, -5], [3, 7, -F(1, 2)],
          [2, 3, 7, -1, -1], [5, -3], [0, 7, -1], [3, 7], [1, 2, 7])


def sweep(sep, tol, lo=-12, hi=20, step=F(1, 8)):
    j = F(lo)
    while j <= hi:
        yield j
        j += step


class CueSign(unittest.TestCase):
    """Operator spec 2026-10-07 after OC-2: S+ / M over cues >= 0, N over
    cues < 0, S = S+ + N, step 0 on S+ - M."""

    def test_split_values(self):
        r = ix.split([3, 7, -2])
        self.assertEqual((r["S_plus"], r["M"], r["N"], r["S"]), (10, 7, -2, 8))
        self.assertEqual((r["n_facilitating"], r["n_suppressive"]), (2, 1))

    def test_classify_carries_N(self):
        r = cls(9, [3, 7, -2], F(1, 2))
        self.assertEqual((r["N"], r["S_plus"], r["S"], r["I"]), (-2, 10, 8, 1))

    def test_zero_is_facilitating(self):
        self.assertEqual(ix.split([0, -1])["M"], 0)

    def test_no_facilitating_cue(self):
        for tol in (1, 0, None):            # [CHOICE 3]: before the tol check
            r = cls(-3, [-1, -2], tol)
            self.assertEqual(r["relation"], ix.NO_FACILITATING_CUE)
            self.assertIsNone(r["M"])
            self.assertEqual(r["N"], -3)

    def test_oc2_still_below_resolution(self):
        # one facilitating cue: S+ - M = 0 <= 2*tol, whatever N and joint
        for j in sweep([5, -3], F(1, 10), -20, 20, 1):
            self.assertEqual(rel(j, [5, -3], F(1, 10)), ix.BELOW_RESOLUTION)

    def test_step0_reads_S_plus_not_S(self):
        # S+ - M = 3 > 2; S - M = 2: pre-split read BELOW_RESOLUTION
        sep = [3, 7, -1]
        self.assertEqual(pre_split(9, sep, 1), ix.BELOW_RESOLUTION)
        self.assertEqual(rel(F(19, 2), sep, 1), ix.ADDITIVE)
        self.assertEqual(rel(7, sep, 1), ix.REDUNDANT)
        self.assertEqual(rel(F(23, 2), sep, 1), ix.RESONANT)

    def test_touching_bands_raise_at_the_shared_point(self):
        # S = 9, M = 7, tol = 1: [6, 8] and [8, 10] share 8
        with self.assertRaises(ix.BandsOverlap) as cm:
            cls(8, [3, 7, -1], 1)
        self.assertEqual(cm.exception.rows, [(1, ix.REDUNDANT), (2, ix.ADDITIVE)])

    def test_S_below_M_unique_and_overlap(self):
        sep = [3, 7, -5]                    # S+ 10, M 7, S 5
        self.assertEqual(rel(20, sep, 1), ix.RESONANT)
        self.assertEqual(rel(0, sep, 1), ix.ANTAGONISTIC)
        for j, rows in ((7, [(1, ix.REDUNDANT), (3, ix.RESONANT)]),
                        (5, [(2, ix.ADDITIVE), (5, ix.ANTAGONISTIC)])):
            with self.assertRaises(ix.BandsOverlap) as cm:
                cls(j, sep, 1)
            self.assertEqual(cm.exception.rows, rows)

    def test_overlap_only_where_S_minus_M_within_2tol(self):
        hits = 0
        for sep in SIGNED:
            for tol in (0, F(1, 2), 1):
                S, M = ix.references(sep)
                for j in sweep(sep, tol):
                    try:
                        cls(j, sep, tol)        # never zero rows
                    except ix.BandsOverlap:
                        hits += 1
                        self.assertLessEqual(S - M, 2 * tol, (sep, tol, j))
        self.assertGreater(hits, 0)

    def test_split_changes_readings_only_in_the_gap_region(self):
        changed = 0
        for sep in SIGNED:
            r0 = ix.split(sep)
            for tol in (0, F(1, 2), 1):
                gap = r0["S"] - r0["M"] <= 2 * tol < r0["S_plus"] - r0["M"]
                for j in sweep(sep, tol):
                    old = pre_split(j, sep, tol)
                    try:
                        new = cls(j, sep, tol)["relation"]
                    except ix.BandsOverlap:
                        new = "OVERLAP"
                    if gap:
                        self.assertEqual(old, ix.BELOW_RESOLUTION)
                        changed += new != old
                    else:
                        self.assertEqual(new, old, (sep, tol, j))
        self.assertGreater(changed, 0)

    def test_without_suppression_nothing_changes(self):
        for sep in ([3, 7], [1, 2, 7], [0, 7], [F(5, 2), 7]):
            for tol in (0, F(1, 2), 1):
                for j in sweep(sep, tol):
                    self.assertEqual(rel(j, sep, tol), pre_split(j, sep, tol))


class Tolerance(unittest.TestCase):
    """Operator spec 2026-10-07 after OC-1: tol = {value, mode}, mode
    absolute | relative_to_M; mode undeclared -> refuse."""

    def test_bare_number_refuses(self):
        for tol in (1, 0, F(1, 10), 0.1):
            with self.assertRaises(ix.ToleranceModeUndeclared):
                ix.classify(10, SEP, tol)

    def test_missing_or_unknown_mode_refuses(self):
        for tol in ({"value": 1}, {"value": 1, "mode": None},
                    {"value": 1, "mode": "relative"}, {"value": 1, "mode": "ABSOLUTE"}):
            with self.assertRaises(ix.ToleranceModeUndeclared, msg=repr(tol)):
                ix.classify(10, SEP, tol)

    def test_unknown_key_refuses(self):
        with self.assertRaises(ix.InteractionError):
            ix.classify(10, SEP, {"value": 1, "mode": "absolute", "units": "s"})

    def test_refusal_is_an_interaction_error(self):
        self.assertTrue(issubclass(ix.ToleranceModeUndeclared, ix.InteractionError))

    def test_relative_scales_by_M(self):
        r = ix.classify(F(17, 2), SEP, ix.relative_to_M(F(1, 7)))   # M = 7
        self.assertEqual((r["tol"], r["tol_value"], r["tol_mode"]),
                         (1, F(1, 7), "relative_to_M"))
        self.assertEqual(r["relation"], ix.ENHANCED_SUBADDITIVE)

    def test_absolute_is_unscaled(self):
        r = ix.classify(F(17, 2), SEP, ix.absolute(1))
        self.assertEqual((r["tol"], r["tol_mode"]), (1, "absolute"))

    def test_oc1_modes_give_different_readings(self):
        # S = 10, M = 9, joint 9.5, value 0.1: OC-1 as authored
        a = ix.classify(F(19, 2), [9, 1], ix.absolute(F(1, 10)))["relation"]
        r = ix.classify(F(19, 2), [9, 1], ix.relative_to_M(F(1, 10)))["relation"]
        self.assertEqual((a, r), (ix.ENHANCED_SUBADDITIVE, ix.BELOW_RESOLUTION))

    def test_value_none_is_unrated_after_mode_check(self):          # [CHOICE 4]
        r = ix.classify(10, SEP, {"value": None, "mode": "absolute"})
        self.assertEqual(r["relation"], ix.UNRATED)
        with self.assertRaises(ix.ToleranceModeUndeclared):
            ix.classify(10, SEP, {"value": None})

    def test_relative_with_M_zero_is_zero_tol(self):
        r = ix.classify(0, [0, 0], ix.relative_to_M(5))
        self.assertEqual((r["tol"], r["relation"]), (0, ix.BELOW_RESOLUTION))

    def test_no_facilitating_cue_precedes_the_mode_check(self):     # [CHOICE 3]
        self.assertEqual(ix.classify(-1, [-1, -2], 1)["relation"],
                         ix.NO_FACILITATING_CUE)


class Refusals(unittest.TestCase):

    def test_bad_inputs_raise(self):
        bad = [(10, SEP, -1), (float("nan"), SEP, 1), (10, [7], 1),
               (10, [], 1), (10, [3, float("inf")], 1), (10, SEP, "1"),
               ("10", SEP, 1), (10, SEP, True)]
        for args in bad:
            with self.assertRaises(ix.InteractionError, msg=repr(args)):
                cls(*args)

    def test_module_refuses_selftest(self):
        p = subprocess.run([sys.executable, os.path.join(HERE, "interaction.py"),
                            "--selftest"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)
        self.assertIn("test_interaction.py", p.stderr)


if __name__ == "__main__":
    unittest.main()
