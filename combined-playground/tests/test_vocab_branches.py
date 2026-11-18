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


class Tiers(unittest.TestCase):
    """Evidence round: V-C tiered; a label match with no shared predicate is a HOMONYM."""
    def test_tier_values(self):
        self.assertEqual(V.TIERS, ("MAPS", "PARTIAL", "HOMONYM", "NONE"))

    def test_tiers_per_pair(self):
        rel = {r["pair"]: r["relation"] for r in V.table()}
        self.assertEqual(rel["GAP_INSTRUMENT_CRASH | CRASHED"], "MAPS")
        self.assertEqual(rel["UNKNOWN | UNKNOWN"], "PARTIAL")
        self.assertEqual(rel["ABSENT_AT_SENSITIVITY | ABSENT_AT_SENSITIVITY"], "PARTIAL")
        self.assertEqual(rel["VOID | VOID"], "HOMONYM")
        self.assertEqual(rel["expiry_condition | ExpiryTrigger"], "PARTIAL")
        self.assertEqual(rel["UNDECIDED | UNRESOLVED"], "PARTIAL")
        self.assertEqual(rel["HOLDS | CLOSED_WITHIN"], "PARTIAL")
        self.assertEqual(rel["HOLDS | OK"], "NONE")

    def test_homonym_needs_label_match(self):
        a, b = V.term("fa:HOLDS"), V.term("cplay:OK")       # different labels, different predicates
        self.assertEqual(V.relation(a, b), "NONE")
        a, b = V.term("fa:VOID"), V.term("cplay:VOID")       # same label, different predicates
        self.assertEqual(V.relation(a, b), "HOMONYM")

    def test_predicates_flagged_single_reader(self):
        self.assertIn("single reader", V.PREDICATE_STATUS)


if __name__ == "__main__":
    unittest.main()
