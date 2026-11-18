"""M6 trust (COMBINED_SPEC section 5; section 8 rows 12, 14). Written before cplay/trust.py."""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import trust as R  # noqa: E402
from cplay import axes as A  # noqa: E402


def _ok():
    return A.reading("INSTRUMENT", "OK")


def _fail():
    return A.reading("INSTRUMENT", "FAILED", reason="harness misses plants")


class Key(unittest.TestCase):
    def test_bare_model_name_refused(self):
        with self.assertRaises(R.TrustError):
            R.TrustKey("detector-v1", None, None)
        with self.assertRaises(R.TrustError):
            R.TrustKey("detector-v1", "forest", "")
        R.TrustKey("detector-v1", "forest", "steady")

    def test_reading_must_be_instrument_axis(self):
        reg = R.Registry()
        with self.assertRaises(R.TrustError):
            reg.certify(R.TrustKey("m", "s", "x"), A.reading("PHYSICAL", "OK"), harness_class="OK")


class Scope(unittest.TestCase):
    def setUp(self):
        self.reg = R.Registry()
        self.reg.certify(R.TrustKey("m", "forest", "steady"), _ok(), harness_class="OK")

    def test_no_transfer_without_certification(self):
        got = self.reg.lookup("m", "relational", "steady")
        self.assertEqual(got.state, "UNTESTED")
        self.assertIn("relational", got.reason)

    def test_untyped_transfer_argument_refused(self):           # 9c item 6 (test_reuse covers the rule)
        with self.assertRaises(R.TrustError):
            self.reg.lookup("m", "relational", "steady", transfer_argument="same ODE family")

    def test_same_key_returns_the_record(self):
        rec = self.reg.lookup("m", "forest", "steady")
        self.assertEqual(rec.reading.status, "OK")
        self.assertEqual(rec.harness_class, "OK")      # harness class sits beside the axis


class StartState(unittest.TestCase):
    def test_varying_verdict_flags_not_blanket_untrusted(self):
        reg = R.Registry()
        reg.certify(R.TrustKey("m", "s", "cold"), _ok(), harness_class="OK")
        reg.certify(R.TrustKey("m", "s", "warm"), _fail(), harness_class="NO_DISCRIMINATION")
        summary = reg.scope_summary("m", "s")
        self.assertEqual(summary["flag"], "START_STATE_SENSITIVE")
        self.assertEqual(sorted(summary["arms"]), ["cold", "warm"])
        self.assertEqual(summary["arms"]["cold"], "OK")
        self.assertNotEqual(summary.get("status"), "FAILED")

    def test_uniform_verdict_has_no_flag(self):
        reg = R.Registry()
        reg.certify(R.TrustKey("m", "s", "cold"), _ok(), harness_class="OK")
        reg.certify(R.TrustKey("m", "s", "warm"), _ok(), harness_class="OK")
        self.assertIsNone(reg.scope_summary("m", "s")["flag"])

    def test_empty_scope_untested(self):
        self.assertEqual(R.Registry().scope_summary("m", "s")["status"].state, "UNTESTED")

    def test_recertify_same_key_refused(self):
        reg = R.Registry()
        reg.certify(R.TrustKey("m", "s", "cold"), _ok(), harness_class="OK")
        with self.assertRaises(R.TrustError):
            reg.certify(R.TrustKey("m", "s", "cold"), _fail(), harness_class="OK")

    def test_harness_class_required(self):
        with self.assertRaises(R.TrustError):
            R.Registry().certify(R.TrustKey("m", "s", "c"), _ok(), harness_class="")


if __name__ == "__main__":
    unittest.main()
