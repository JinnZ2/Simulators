"""M8 continuity (COMBINED_SPEC section 8 rows 21-26, Q7). Written before cplay/continuity.py."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import continuity as C  # noqa: E402
from cplay import tokens as T  # noqa: E402


def _anchor():
    return C.Anchor("a0", {"N": 10.0, "P": 2.0})


class Anchor(unittest.TestCase):
    def test_frozen(self):
        a = _anchor()
        with self.assertRaises(TypeError):
            a.values["N"] = 11.0


class Return(unittest.TestCase):
    def test_tolerance_declared_per_variable(self):
        with self.assertRaises(C.ContinuityError):
            C.return_to_anchor(_anchor(), {"N": 10.1, "P": 2.0}, tolerance={"N": 0.5})

    def test_verdict_and_deltas_both_returned(self):
        r = C.return_to_anchor(_anchor(), {"N": 10.1, "P": 2.0}, tolerance={"N": 0.5, "P": 0.1})
        self.assertEqual(r.state, "OK")
        self.assertAlmostEqual(r.deltas["N"], 0.1)
        r = C.return_to_anchor(_anchor(), {"N": 12.0, "P": 2.0}, tolerance={"N": 0.5, "P": 0.1})
        self.assertEqual(r.state, "FAILED")
        self.assertIn("N", r.reason)
        self.assertAlmostEqual(r.deltas["N"], 2.0)

    def test_missing_variable_untested_not_ok(self):
        r = C.return_to_anchor(_anchor(), {"N": 10.0}, tolerance={"N": 0.5, "P": 0.1})
        self.assertEqual(r.state, "UNTESTED")
        self.assertIn("P", r.reason)


class TwoFields(unittest.TestCase):
    def test_no_composite_and_branch_keeps_both(self):
        ret = C.return_to_anchor(_anchor(), {"N": 10.0, "P": 2.0}, tolerance={"N": 0.5, "P": 0.1})
        rec = C.Continuity(identity_check=T.Token("FAILED", "different configuration"),
                           return_to_anchor=ret)
        self.assertEqual(rec.identity_check.state, "FAILED")
        self.assertEqual(rec.return_to_anchor.state, "OK")
        self.assertTrue(rec.disagree)
        with self.assertRaises(C.ContinuityError):
            rec.composite()
        self.assertFalse(hasattr(rec, "status"))

    def test_identity_check_is_a_token(self):
        ret = C.return_to_anchor(_anchor(), {"N": 10.0, "P": 2.0}, tolerance={"N": 0.5, "P": 0.1})
        with self.assertRaises(C.ContinuityError):
            C.Continuity(identity_check=True, return_to_anchor=ret)


class Branch(unittest.TestCase):
    def test_one_change_branch(self):
        b = C.branch({"k": 1, "r": 2}, {"k": 1, "r": 3})
        self.assertEqual(b, ("r",))
        with self.assertRaises(C.ContinuityError) as cm:
            C.branch({"k": 1, "r": 2}, {"k": 5, "r": 3})
        self.assertIn("k", str(cm.exception)); self.assertIn("r", str(cm.exception))
        with self.assertRaises(C.ContinuityError):
            C.branch({"k": 1}, {"k": 1})
        with self.assertRaises(C.ContinuityError):
            C.branch({"k": 1}, {"k": 1, "new": 2})


class Revision(unittest.TestCase):
    def test_reevaluation_keeps_original(self):
        orig = T.Token("OK")
        rev = C.reevaluate(orig, T.Token("FAILED", "new data"), reason="run 11")
        self.assertIs(rev.original, orig)
        self.assertEqual(rev.revised.state, "FAILED")
        with self.assertRaises(C.ContinuityError):
            C.reevaluate(orig, T.Token("FAILED", "x"), reason="")


class Tracks(unittest.TestCase):
    def test_crossing_refused(self):
        t = C.Tracks(("system", "configuration"))
        t.append("system", "s1")
        with self.assertRaises(C.ContinuityError):
            t.append("configuration", "s1", source_track="system")
        with self.assertRaises(C.ContinuityError):
            t.append("other", "x")


if __name__ == "__main__":
    unittest.main()
