"""M2 state tokens, expiry, scoped absence, claims (COMBINED_SPEC section 4)."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import tokens as T  # noqa: E402


class Tokens(unittest.TestCase):
    def test_every_listed_state_is_distinct(self):
        self.assertEqual(len(set(T.STATES)), len(T.STATES))
        for s in ("INDETERMINATE", "UNTESTED", "CRASHED", "CLOSED_WITHIN", "OUTSIDE_DOMAIN",
                  "NOT_COMPARABLE", "NOT_SCORED_STUB", "UNTYPED", "UNDECLARED", "REFUSED", "BRIEF_UNRECORDED"):
            self.assertIn(s, T.STATES)

    def test_non_verdict_needs_reason(self):
        for s in T.STATES:
            if s in T.VERDICTS:
                continue
            with self.assertRaises(T.TokenError):
                T.Token(s, "")
            with self.assertRaises(T.TokenError):
                T.Token(s, "   ")
        T.Token("OK")

    def test_unknown_state_refused(self):
        with self.assertRaises(T.TokenError):
            T.Token("MAYBE", "x")

    def test_never_reads_as_zero_ok_or_empty(self):
        t = T.Token("UNTESTED", "no check addressed it")
        self.assertFalse(t.is_verdict)
        with self.assertRaises(TypeError):
            float(t)
        with self.assertRaises(TypeError):
            bool(t)


class Expiry(unittest.TestCase):
    def test_typed_trigger_needs_all_fields(self):
        T.ExpiryTrigger("measurement_arrives", "K", "a measured value for K")
        for bad in (("", "K", "c"), ("k", "", "c"), ("k", "K", "")):
            with self.assertRaises(T.TokenError):
                T.ExpiryTrigger(*bad)

    def test_unknown_requires_typed_trigger(self):
        T.unknown("not measured", [T.ExpiryTrigger("measurement_arrives", "K", "value for K")])
        with self.assertRaises(T.TokenError):
            T.unknown("not measured", [])
        with self.assertRaises(T.TokenError):
            T.unknown("not measured", [T.untyped("a measured value arrives")])

    def test_free_text_is_untyped_and_counts_as_no_exit(self):
        u = T.untyped("someday")
        self.assertEqual(u.state, "UNTYPED")
        self.assertFalse(u.is_exit)

    def test_untyped_note_kept_beside_typed_trigger(self):
        v = T.unknown("x", [T.ExpiryTrigger("k", "K", "c"), T.untyped("also this")])
        self.assertEqual(len(v.typed), 1)
        self.assertEqual(len(v.untyped), 1)


class ScopedAbsence(unittest.TestCase):
    def test_needs_limit_basis_effect_and_conditions(self):
        a = T.absent_at_sensitivity(limit=0.1, basis="DECLARED", effect_size=0.5, conditions="25 C, sample A")
        self.assertEqual(a.state, "ABSENT_AT_SENSITIVITY")
        for drop in ("limit", "basis", "effect_size", "conditions"):
            kw = dict(limit=0.1, basis="DECLARED", effect_size=0.5, conditions="25 C")
            kw[drop] = None
            with self.assertRaises(T.TokenError):
                T.absent_at_sensitivity(**kw)

    def test_basis_is_ladder_or_declared(self):
        with self.assertRaises(T.TokenError):
            T.absent_at_sensitivity(limit=0.1, basis="GUESS", effect_size=0.5, conditions="c")
        with self.assertRaises(T.TokenError):
            T.absent_at_sensitivity(limit=0.1, basis="LADDER", effect_size=0.5, conditions="c")   # no ladder ref
        T.absent_at_sensitivity(limit=0.1, basis="LADDER", effect_size=0.5, conditions="c", ladder="lad-1")

    def test_limit_above_effect_size_is_flagged_not_hidden(self):
        a = T.absent_at_sensitivity(limit=0.1, basis="DECLARED", effect_size=0.01, conditions="c")
        self.assertFalse(a.covers_effect)
        self.assertTrue(T.absent_at_sensitivity(limit=0.1, basis="DECLARED", effect_size=0.5, conditions="c").covers_effect)


class Claims(unittest.TestCase):
    def test_untagged_claim_refused(self):
        with self.assertRaises(T.TokenError):
            T.Claim("the run closes", None, ["run 9 ledger"])
        with self.assertRaises(T.TokenError):
            T.Claim("the run closes", "CERTAIN", ["run 9 ledger"])

    def test_tag_and_record_linked_one_to_one(self):
        c = T.Claim("the run closes", "OBSERVED", ["run 9 ledger"])
        self.assertIs(c.record.claim, c)
        self.assertIs(c.tag.claim, c)
        self.assertEqual(c.tag.value, "OBSERVED")
        self.assertEqual(c.record.chain, ("run 9 ledger",))

    def test_record_needs_a_provenance_chain(self):
        with self.assertRaises(T.TokenError):
            T.Claim("x", "DERIVED", [])


class Vocabulary(unittest.TestCase):
    def test_mapping_table_is_void_with_reason(self):
        m = T.VOCABULARY_MAPPING
        self.assertEqual(m.state, "VOID")
        self.assertIn("spec", m.reason)


if __name__ == "__main__":
    unittest.main()
