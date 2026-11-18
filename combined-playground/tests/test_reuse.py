"""G1: section 9c REUSE items 1, 5, 6, 10, 11 -- pins resolve, no logic copied, decisions wired.

Written before the module changes.
"""
import ast, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import pins as P, axes as A, gates as G, trust as R, uncertainty as U, tokens as T  # noqa
from cplay import brief as B  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Pins(unittest.TestCase):
    def test_every_pin_well_formed_and_items_covered(self):
        for p in P.PINS:
            self.assertTrue(P.well_formed(p), p.pin_id)
        self.assertEqual(sorted({p.item for p in P.PINS}), [1, 5, 6, 10, 11])

    def test_pins_resolve_or_are_not_testable_never_mismatch(self):
        for p in P.PINS:
            state, why = P.resolve(p)
            self.assertIn(state, ("RESOLVED", "NOT_TESTABLE"), (p.pin_id, why))

    def test_mismatch_is_detected(self):
        p = P.PINS[3]._replace(sha256="0" * 64)          # the in-repo Simulators pin
        state, _ = P.resolve(p)
        self.assertIn(state, ("MISMATCH", "NOT_TESTABLE"))
        if P.resolve(P.PINS[3])[0] == "RESOLVED":
            self.assertEqual(state, "MISMATCH")

    def test_no_checkout_is_not_testable(self):
        old = os.environ.get("COMBINED_PIN_ROOTS")
        os.environ["COMBINED_PIN_ROOTS"] = os.path.join(HERE, "no-such-root")
        try:
            self.assertEqual(P.resolve(P.PINS[0])[0], "NOT_TESTABLE")
        finally:
            if old is None:
                del os.environ["COMBINED_PIN_ROOTS"]
            else:
                os.environ["COMBINED_PIN_ROOTS"] = old

    def test_no_logic_copied(self):
        for f in os.listdir(os.path.join(HERE, "cplay")):
            if not f.endswith(".py"):
                continue
            tree = ast.parse(open(os.path.join(HERE, "cplay", f)).read())
            names = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
            for foreign in ("expiry_check", "check_relation", "replay", "Interval", "update_ladder"):
                self.assertNotIn(foreign, names, f)
            for n in ast.walk(tree):
                if isinstance(n, (ast.Import, ast.ImportFrom)):
                    mod = getattr(n, "module", None) or n.names[0].name
                    self.assertFalse(mod.startswith(("numcheck", "infer", "calibration")), f)


class Item1(unittest.TestCase):
    def test_no_composite_decided(self):
        self.assertEqual(A.COMPOSITE_SEVERITY.state, "REFUSED")
        self.assertIn("P1-taf-unknown-axis", A.COMPOSITE_SEVERITY.reason)
        self.assertEqual(tuple(A.Record({}, coverage=[]).severity()), A.AXES)


class Item5(unittest.TestCase):
    def _card(self, causes=None):
        ch = G.Chain("a", "b", system_a="A", system_b="B")
        ch.identity(True, "same")
        ch.regime(G.RegimeDecl("A", "PASSIVE", "r"), G.RegimeDecl("B", "PASSIVE", "r"))
        ch.compare(T.Token("OK"))
        a = B.InputBrief("x", "2026-11-18", [B.Item("s", verbatim="t")])
        return ch.open_card(a, a, cues={}, causes=causes)

    def test_independence_list(self):
        self.assertEqual(G.INDEPENDENCE_CAUSES,
                         ("shared_source", "method", "model", "training_data", "code", "axioms"))

    def test_undeclared_causes_are_tokens_not_absent(self):
        card = self._card()
        for c in G.INDEPENDENCE_CAUSES[1:]:
            self.assertEqual(card["other_causes"][c].state, "UNDECLARED")
        self.assertIn("shared_source_by_level", card)

    def test_declared_cause_carried_and_must_be_token(self):
        card = self._card({"model": T.Token("FAILED", "both runs used one model")})
        self.assertEqual(card["other_causes"]["model"].state, "FAILED")
        with self.assertRaises(G.GateError):
            self._card({"model": "same"})
        with self.assertRaises(G.GateError):
            self._card({"weather": T.Token("OK")})


class Item6(unittest.TestCase):
    def setUp(self):
        from cplay import axes
        self.reg = R.Registry()
        self.reg.certify(R.TrustKey("m", "forest", "steady"), axes.reading("INSTRUMENT", "OK"),
                         harness_class="OK")

    def _arg(self, matched=(True, True), indep=True, src="forest"):
        return R.TransferArgument(from_scope=src,
                                  constraints=[("mass balance", matched[0]), ("same ODE", matched[1])],
                                  independence_checked=indep)

    def test_all_matched_and_independent_transfers(self):
        got = self.reg.lookup("m", "relational", "steady", transfer_argument=self._arg())
        self.assertIsInstance(got, R.TransferredTrust)
        self.assertEqual(got.source.key.scope, "forest")

    def test_unmatched_or_unchecked_refused(self):
        got = self.reg.lookup("m", "relational", "steady", transfer_argument=self._arg((True, False)))
        self.assertEqual(got.state, "REFUSED")
        self.assertIn("same ODE", got.reason)
        got = self.reg.lookup("m", "relational", "steady", transfer_argument=self._arg(indep=False))
        self.assertEqual(got.state, "REFUSED")

    def test_source_must_be_certified_and_argument_typed(self):
        got = self.reg.lookup("m", "relational", "steady", transfer_argument=self._arg(src="ocean"))
        self.assertEqual(got.state, "UNTESTED")
        with self.assertRaises(R.TrustError):
            self.reg.lookup("m", "relational", "steady", transfer_argument="same ODE family")
        with self.assertRaises(R.TrustError):
            R.TransferArgument(from_scope="forest", constraints=[], independence_checked=True)


class Item10And11(unittest.TestCase):
    def test_propagation_delegated_to_pin(self):
        self.assertEqual(U.PROPAGATION.state, "REFUSED")
        self.assertIn("P10-numcheck", U.PROPAGATION.reason)

    def test_expiry_vocabulary_pinned(self):
        self.assertIn("P11-taf-expiry-register", T.EXPIRY_VOCABULARY.reason)
        self.assertEqual(T.TAF_EXPIRY_KEYS, ("instrument_class", "sensitivity", "protocol", "provenance"))


if __name__ == "__main__":
    unittest.main()
