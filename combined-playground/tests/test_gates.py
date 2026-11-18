"""M5 gate order (COMBINED_SPEC section 3; section 8 rows 29-33). Written before cplay/gates.py."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import gates as G  # noqa: E402
from cplay import brief as B  # noqa: E402
from cplay import tokens as T  # noqa: E402


def _briefs():
    a = B.InputBrief("s-a", "2026-11-11", [B.Item("spec", verbatim="anchor return test")])
    b = B.InputBrief("#257", "2026-11-11", [B.Item("spec", verbatim="relational playground")])
    return a, b


class Regime(unittest.TestCase):
    def test_four_regimes_none_merged_passive_labelled(self):
        self.assertEqual(G.REGIMES, ("PASSIVE", "PERTURBATION", "REACTIVITY", "STRATEGY"))
        self.assertIn("chat-side", G.REGIME_SOURCE["PASSIVE"])
        for r in G.REGIMES[1:]:
            self.assertIn("4.4", G.REGIME_SOURCE[r])

    def test_declaration_needs_reason_and_known_regime(self):
        G.RegimeDecl("sysA", "PASSIVE", "null control run")
        with self.assertRaises(G.GateError):
            G.RegimeDecl("sysA", "PASSIVE", "")
        with self.assertRaises(G.GateError):
            G.RegimeDecl("sysA", "PASSIVE+REACTIVITY", "merged")


class Order(unittest.TestCase):
    def setUp(self):
        self.ch = G.Chain("x_A", "x_B", system_a="sysA", system_b="sysB")

    def test_identity_fail_records_not_comparable_and_no_card(self):
        self.ch.identity(False, "different measurands: N stock vs N flux")
        self.assertEqual(self.ch.outcome.state, "NOT_COMPARABLE")
        with self.assertRaises(G.GateError):
            self.ch.open_card(*_briefs(), cues={})

    def test_identity_needs_reason_either_way(self):
        with self.assertRaises(G.GateError):
            self.ch.identity(True, "")

    def test_regime_before_identity_refused(self):
        with self.assertRaises(G.GateError):
            self.ch.regime(G.RegimeDecl("sysA", "PASSIVE", "r"), G.RegimeDecl("sysB", "PASSIVE", "r"))

    def test_undeclared_regime_refuses_comparison(self):
        self.ch.identity(True, "same quantity, unit, scope")
        self.ch.regime(G.RegimeDecl("sysA", "PASSIVE", "r"), None)
        self.assertEqual(self.ch.outcome.state, "REFUSED")
        self.assertIn("sysB", self.ch.outcome.reason)
        with self.assertRaises(G.GateError):
            self.ch.compare(T.Token("OK"))

    def test_regime_must_name_its_system(self):
        self.ch.identity(True, "same")
        with self.assertRaises(G.GateError):
            self.ch.regime(G.RegimeDecl("sysZ", "PASSIVE", "r"), G.RegimeDecl("sysB", "PASSIVE", "r"))

    def test_card_only_after_comparison(self):
        self.ch.identity(True, "same")
        self.ch.regime(G.RegimeDecl("sysA", "PASSIVE", "r"), G.RegimeDecl("sysB", "PASSIVE", "r"))
        with self.assertRaises(G.GateError):
            self.ch.open_card(*_briefs(), cues={})
        self.ch.compare(T.Token("OK"))
        card = self.ch.open_card(*_briefs(), cues={"concept_level": "anchor"})
        self.assertEqual(card["shared_source_by_level"]["concept_level"].state, B.CUE_IN_ONE)
        self.assertEqual(card["regimes"], ("PASSIVE", "PASSIVE"))
        self.assertEqual(card["regime_mismatch_effect"].state, "OK")      # same regime (9c item 4)
        self.assertEqual(card["other_causes"]["model"].state, "UNDECLARED")   # 9c item 5

    def test_steps_run_once(self):
        self.ch.identity(True, "same")
        with self.assertRaises(G.GateError):
            self.ch.identity(True, "again")


class Rank(unittest.TestCase):
    def test_no_universal_ranking(self):
        with self.assertRaises(G.GateError):
            G.rank(["a", "b"])


if __name__ == "__main__":
    unittest.main()
