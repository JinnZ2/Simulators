"""G5 item 12: vocabulary mapping rows, three branches (V-A label, V-B definition, V-C structure).

Written before cplay/vocab_branches.py. No branch is picked.
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import vocab_branches as V, pins as P  # noqa: E402


class Branches(unittest.TestCase):
    def test_va_exact_label(self):
        a = V.term("taf:UNKNOWN"); b = V.term("cplay:UNKNOWN")
        self.assertTrue(V.va(a, b))
        self.assertFalse(V.va(V.term("taf:GAP_INSTRUMENT_CRASH"), V.term("cplay:CRASHED")))

    def test_vb_uses_tool_cards_rule(self):
        self.assertTrue(V.vb_text("a  b\n c", "x a b c y"))        # WRAP_COLLAPSED containment
        self.assertTrue(V.vb_text("abc", "abc"))                    # VERBATIM
        self.assertFalse(V.vb_text("abc", "abd"))

    def test_vc_same_predicate_same_slots(self):
        self.assertTrue(V.vc(V.term("taf:GAP_INSTRUMENT_CRASH"), V.term("cplay:CRASHED")))
        self.assertFalse(V.vc(V.term("taf:UNKNOWN"), V.term("cplay:UNKNOWN")))

    def test_crashed_slots_read_from_code(self):
        from cplay import axes
        self.assertEqual(V.term("cplay:CRASHED").slots, tuple(axes.CoverageEntry._fields))


class Sources(unittest.TestCase):
    def test_every_definition_anchor_resolves_or_not_testable(self):
        for t in V.TERMS:
            state, why = P.resolve(t.pin)
            self.assertIn(state, ("RESOLVED", "NOT_TESTABLE"), (t.term_id, why))

    def test_anchor_inside_definition(self):
        for t in V.TERMS:
            self.assertIn(V.norm(t.pin.anchor), V.norm(t.definition), t.term_id)


class Table(unittest.TestCase):
    def test_rows_and_split(self):
        rows = {r["pair"]: r for r in V.table()}
        crash = rows["GAP_INSTRUMENT_CRASH | CRASHED"]
        self.assertEqual((crash["V-A"], crash["V-C"]), (False, True))
        self.assertTrue(crash["split"])
        void = rows["VOID | VOID"]
        self.assertEqual((void["V-A"], void["V-C"]), (True, False))     # homonym
        self.assertTrue(void["split"])
        self.assertIn("split", next(iter(rows.values())))
        self.assertNotIn("winner", next(iter(rows.values())))

    def test_all_pairs_cover_three_vocabularies(self):
        srcs = {t.term_id.split(":")[0] for t in V.TERMS}
        self.assertEqual(srcs, {"taf", "cplay", "fa"})


if __name__ == "__main__":
    unittest.main()
