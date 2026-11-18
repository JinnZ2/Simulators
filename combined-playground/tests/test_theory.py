"""G2: section 9c THEORY items 2, 3, 4, 8. Written before the module changes.

Sources NOT_CHECKED (VERIFY): JCGM 200 (VIM) and EA-4/02 could not be read from this session.
"""
import math, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import gates as G, trust as R, known_answer as K, tokens as T, axes as A  # noqa: E402


def _chain():
    return G.Chain("a", "b", system_a="A", system_b="B")


class Item2Identity(unittest.TestCase):
    """VIM: measurand = quantity intended to be measured; identity = same kind + same conditions."""
    def test_same_kind_same_conditions(self):
        a = G.Measurand(kind="mass flux of N", conditions={"boundary": "plot", "horizon": "1 yr"})
        b = G.Measurand(kind="mass flux of N", conditions={"horizon": "1 yr", "boundary": "plot"})
        ok, why = G.measurand_identity(a, b)
        self.assertTrue(ok)

    def test_kind_differs(self):
        a = G.Measurand(kind="N stock", conditions={"boundary": "plot"})
        b = G.Measurand(kind="N flux", conditions={"boundary": "plot"})
        ok, why = G.measurand_identity(a, b)
        self.assertFalse(ok)
        self.assertIn("kind", why)

    def test_condition_differs_or_missing_named(self):
        a = G.Measurand(kind="k", conditions={"boundary": "plot", "horizon": "1 yr"})
        b = G.Measurand(kind="k", conditions={"boundary": "plot", "horizon": "10 yr"})
        ok, why = G.measurand_identity(a, b)
        self.assertFalse(ok); self.assertIn("horizon", why)
        c = G.Measurand(kind="k", conditions={"boundary": "plot"})
        ok, why = G.measurand_identity(a, c)
        self.assertFalse(ok); self.assertIn("horizon", why)

    def test_chain_identity_from_measurands(self):
        ch = _chain()
        ch.identity_of(G.Measurand(kind="x", conditions={"c": 1}), G.Measurand(kind="y", conditions={"c": 1}))
        self.assertEqual(ch.outcome.state, "NOT_COMPARABLE")

    def test_kind_required(self):
        with self.assertRaises(G.GateError):
            G.Measurand(kind="", conditions={})

    def test_source_not_checked(self):
        self.assertIn("NOT_CHECKED", G.IDENTITY_SOURCE)


class Item3Comparison(unittest.TestCase):
    """En = |x1 - x2| / sqrt(U1^2 + U2^2); En <= 1 agree (EA-4/02, NOT_CHECKED)."""
    def test_en_known_values(self):
        c = G.en_compare(10.0, 0.3, 10.4, 0.4)          # |d| = 0.4, sqrt(0.09+0.16) = 0.5
        self.assertAlmostEqual(c.en, 0.8)
        self.assertAlmostEqual(c.difference, -0.4)
        self.assertAlmostEqual(c.u_combined, 0.5)
        self.assertEqual(c.token.state, "OK")
        c = G.en_compare(10.0, 0.3, 11.0, 0.4)
        self.assertAlmostEqual(c.en, 2.0)
        self.assertEqual(c.token.state, "FAILED")

    def test_boundary_en_equal_one_agrees(self):
        self.assertEqual(G.en_compare(0.0, 3.0, 5.0, 4.0).token.state, "OK")

    def test_zero_combined_uncertainty_void(self):
        self.assertEqual(G.en_compare(1.0, 0.0, 1.0, 0.0).token.state, "VOID")

    def test_negative_uncertainty_refused(self):
        with self.assertRaises(G.GateError):
            G.en_compare(1.0, -0.1, 1.0, 0.1)

    def test_chain_compare_values(self):
        ch = _chain()
        ch.identity(True, "same")
        ch.regime(G.RegimeDecl("A", "PASSIVE", "r"), G.RegimeDecl("B", "PASSIVE", "r"))
        c = ch.compare_values(10.0, 0.3, 10.4, 0.4)
        self.assertAlmostEqual(c.en, 0.8)
        self.assertEqual(ch.comparison.state, "OK")


class Item4Regimes(unittest.TestCase):
    def _arg(self, ok=True, indep=True):
        return R.TransferArgument(from_scope="PASSIVE", constraints=[("no reaction", ok)],
                                  independence_checked=indep)

    def _go(self, arg=None):
        ch = _chain()
        ch.identity(True, "same")
        ch.regime(G.RegimeDecl("A", "PASSIVE", "r"), G.RegimeDecl("B", "REACTIVITY", "r"),
                  transfer_argument=arg)
        return ch

    def test_different_regimes_refused_naming_both(self):
        ch = self._go()
        self.assertEqual(ch.outcome.state, "REFUSED")
        self.assertIn("PASSIVE", ch.outcome.reason)
        self.assertIn("REACTIVITY", ch.outcome.reason)

    def test_failing_transfer_argument_still_refused(self):
        self.assertEqual(self._go(self._arg(ok=False)).outcome.state, "REFUSED")
        self.assertEqual(self._go(self._arg(indep=False)).outcome.state, "REFUSED")

    def test_passing_transfer_argument_allows_comparison(self):
        ch = self._go(self._arg())
        self.assertIsNone(ch.outcome)
        ch.compare(T.Token("OK"))
        self.assertIsNotNone(ch.regime_transfer)

    def test_untyped_argument_refused(self):
        with self.assertRaises(G.GateError):
            self._go("they are basically the same")


class Item8PassRule(unittest.TestCase):
    TESTED = ("formula:f",)

    def _cases(self, oks):
        cs = [K.Case(case_id="c%d" % i, inputs=i, expected=i, provenance="hand calc") for i in range(len(oks))]
        table = dict(zip([c.case_id for c in cs], oks))
        return K.run_cases(cs, tested=self.TESTED, check=lambda c: table[c.case_id], module="m")

    def _plants(self, caught):
        ps = [K.Plant(plant_id="p%d" % i, expected_axis="PHYSICAL", is_null=False) for i in range(len(caught))]
        ps.append(K.Plant(plant_id="null", expected_axis=None, is_null=True))
        table = dict(zip([p.plant_id for p in ps], list(caught) + [False]))
        return K.harness(ps, fired=lambda p: table[p.plant_id])

    def test_all_pass_all_caught_ok_with_counts(self):
        r = K.ka_verdict(self._cases([True, True]), self._plants([True, True, True]))
        self.assertEqual((r.field, r.status), ("INSTRUMENT", "OK"))
        self.assertIn("cases 2/2", r.reason)
        self.assertIn("plants caught 3/3", r.reason)

    def test_one_case_fails_or_one_plant_missed_fails(self):
        r = K.ka_verdict(self._cases([True, False]), self._plants([True]))
        self.assertEqual(r.status, "FAILED"); self.assertIn("1/2", r.reason)
        r = K.ka_verdict(self._cases([True, True]), self._plants([True, False]))
        self.assertEqual(r.status, "FAILED"); self.assertIn("1/2", r.reason)

    def test_no_plants_untested_no_threshold(self):
        r = K.ka_verdict(self._cases([True]), K.harness([], fired=lambda p: False))
        self.assertEqual(r.status, "UNTESTED")

    def test_zero_cases_and_circular_pass_through(self):
        z = K.run_cases([], tested=self.TESTED, check=lambda c: True, module="m")
        self.assertEqual(K.ka_verdict(z, self._plants([True])).reason, "KA_NO_CASES")

    def test_crash_passes_through(self):
        def boom(c):
            raise ValueError("x")
        cr = K.run_cases([K.Case(case_id="c", inputs=1, expected=1, provenance="p")],
                         tested=self.TESTED, check=boom, module="m")
        self.assertEqual(K.ka_verdict(cr, self._plants([True])).status, "CRASHED")


if __name__ == "__main__":
    unittest.main()
