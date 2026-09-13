"""
Repo-level test: a value and its source travel together.

License: CC0
Dependencies: stdlib only (unittest)

Three defects landed in one folder in one session and all three have the
same shape -- a value that could not have named its source. A lstrip on a
character set that ate the value's own leading sign and returned the
unamended score; a bare-numeral test that read a cross-reference as a
lifetime; a register(...) call shadowed by a finally that never ran. None
was found by reading the code.

`tools/sourced.py` is the general repair: value, literal source text,
locator, and one gate that returns UNRATED for anything lacking all three.
This test runs its selftest as a subprocess (so the CLI contract is
exercised, not just the functions) and then asserts the four properties
that carry the rule, including the one that says containment is NOT
sufficient.

    python3 -m unittest discover tests
"""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "sourced.py")

sys.path.insert(0, os.path.join(ROOT, "tools"))
import sourced as S  # noqa: E402


class SelftestRuns(unittest.TestCase):

    def test_the_tool_exists(self):
        self.assertTrue(os.path.exists(TOOL))

    def test_selftest_exits_clean(self):
        p = subprocess.run([sys.executable, TOOL, "--selftest"],
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        self.assertIn("failed: 0", p.stdout)

    def test_bare_invocation_does_not_pass_silently(self):
        """A module that exits 0 on an invocation running no checks reports
        a pass nobody earned. This one prints what it is and says how to
        run the checks; the exit code belongs to the selftest."""
        p = subprocess.run([sys.executable, TOOL],
                           capture_output=True, text=True)
        self.assertIn("--selftest", p.stdout)
        self.assertNotIn("failed: 0", p.stdout)


class TheGate(unittest.TestCase):

    CELL = "-> --   A-02"

    def loc(self):
        return S.Locator("WORK_ORDER_V2.md", 74, 57, None, "V6 amendment")

    def test_containment_is_not_sufficient(self):
        """THE reason the primitive is a span. On the V6 row the buggy
        value '-' DOES occur in the amendment cell, through the hyphen of
        the arrow, so a containment check passes it."""
        self.assertIsNotNone(S.find_span(self.CELL, "-"))
        self.assertIsNone(S.find_span("-> --   A-01", "+"))

    def test_a_value_with_no_span_refuses(self):
        u = S.gate(S.Sourced("-", self.CELL, self.loc()))
        self.assertEqual(u, S.UNRATED)
        self.assertEqual(u.reason, "no_provenance")
        self.assertFalse(u)

    def test_a_value_whose_span_disagrees_refuses(self):
        u = S.gate(S.Sourced("+", "-> --   A-01", self.loc(), span=(3, 5)))
        self.assertEqual(u.reason, "span_mismatch")

    def test_a_sliced_value_passes(self):
        g = S.slice_sourced(self.CELL, 3, 5, self.loc())
        self.assertIs(S.gate(g), g)
        self.assertEqual(g.value, "--")

    def test_a_declared_derivation_passes_and_both_refuses(self):
        d = S.Sourced(0.5, "0.9^7", self.loc(), derivation="product")
        self.assertIs(S.gate(d), d)
        both = S.Sourced("--", self.CELL, self.loc(), span=(3, 5),
                         derivation="also")
        self.assertEqual(S.gate(both).reason, "ambiguous_provenance")

    def test_the_gate_is_not_constant(self):
        good = S.slice_sourced(self.CELL, 3, 5, self.loc())
        self.assertIs(S.gate(good), good)
        self.assertEqual(S.gate("--"), S.UNRATED)
        self.assertEqual(S.gate(None), S.UNRATED)

    def test_unrated_survives_a_second_gate(self):
        u = S.gate(None)
        self.assertIs(S.gate(u), u)

    def test_value_of_never_defaults_to_a_number(self):
        self.assertEqual(S.value_of(S.Sourced("-", self.CELL, self.loc())),
                         S.UNRATED)


class TheNumeralRule(unittest.TestCase):

    def loc(self):
        return S.Locator("d", 1, None, None, "condition")

    def test_the_two_false_positives_refuse(self):
        self.assertEqual(
            S.numeral_with_unit("a continuing custodian (see DUR-006)",
                                self.loc()), S.UNRATED)
        self.assertEqual(
            S.numeral_with_unit("hop count over the retention horizon "
                                "exceeds ~1", self.loc()), S.UNRATED)

    def test_a_real_duration_carries_its_span(self):
        d = S.numeral_with_unit("expected lifetime 18 months", self.loc())
        self.assertIsInstance(d, S.Sourced)
        self.assertEqual(d.value, "18 months")
        self.assertIs(S.gate(d), d)

    def test_a_unit_with_no_numeral_refuses(self):
        self.assertEqual(S.numeral_with_unit("several years", self.loc()),
                         S.UNRATED)


class TheRegistryRule(unittest.TestCase):

    def test_short_names_the_missing_registration(self):
        r = S.registry_complete(["a", "b"], ["a"], "t")
        self.assertEqual(r["state"], "SHORT")
        self.assertEqual(r["missing"], ["b"])
        self.assertFalse(r["ok"])

    def test_complete_is_reachable(self):
        r = S.registry_complete(["a"], ["a"], "t")
        self.assertEqual(r["state"], "COMPLETE")
        self.assertTrue(r["ok"])

    def test_both_directions_are_kept_apart(self):
        self.assertEqual(S.registry_complete(["a"], ["a", "b"])["state"],
                         "OVER")
        self.assertEqual(S.registry_complete(["a", "b"], ["a", "c"])["state"],
                         "DIVERGED")


class TheBoundaryRule(unittest.TestCase):

    LINE = ("V2      -- high (the ash)      "
            "-- high (versions, data state, hw)")

    def test_a_boundary_that_cuts_a_token_is_reported(self):
        ok, cuts = S.Locator("d", 2, 31, 57, "ml").boundary_clean(self.LINE)
        self.assertFalse(ok)
        self.assertIn("end", cuts)

    def test_a_clean_boundary_reports_clean(self):
        line = "V6      +  stone, parchment    -  format rot             -> --   A-02"
        ok, cuts = S.Locator("d", 6, 31, 57, "ml").boundary_clean(line)
        self.assertTrue(ok)
        self.assertEqual(cuts, ())


if __name__ == "__main__":
    unittest.main()
