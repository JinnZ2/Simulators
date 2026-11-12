import unittest
from helpers import *
from playground.uncertainty import Value, UncertaintyMatrix, UnknownValue, STATUSES


class T(unittest.TestCase):
    def test_unknown_never_becomes_a_number(self):
        m = UncertaintyMatrix(dict(a=Value(None, "UNKNOWN", "p", expiry_condition="VOID"), b=A(1.0)))
        self.assertRaises(UnknownValue, m.resolve)
        self.assertRaises(ValueError, Value, 0.0, "UNKNOWN", "p", None, "VOID")

    def test_number_and_provenance_required(self):
        self.assertRaises(ValueError, Value, None, "MEASURED", "p")
        self.assertRaises(ValueError, Value, 1.0, "MEASURED", "")
        self.assertRaises(ValueError, Value, 1.0, "GUESSED", "p")

    def test_expiry_required_and_void_counted(self):
        self.assertRaises(ValueError, Value, None, "UNKNOWN", "p")
        self.assertRaises(ValueError, Value, None, "NOT MEASURED", "p")
        m = UncertaintyMatrix(dict(a=Value(None, "UNKNOWN", "p", expiry_condition="VOID"),
                                   b=Value(None, "NOT MEASURED", "p", expiry_condition="gauge installed")))
        r = m.expiry_report()
        self.assertEqual((r["open_slots"], r["no_exit_defined"]), (2, 1))

    def test_absent_at_sensitivity(self):
        self.assertIn("ABSENT_AT_SENSITIVITY", STATUSES)
        v = Value(None, "ABSENT_AT_SENSITIVITY", "assay", sensitivity="0.1 ppm")
        self.assertEqual(v.label(), "ABSENT_AT_SENSITIVITY(0.1 ppm)")
        self.assertRaises(UnknownValue, v.number)
        self.assertRaises(ValueError, Value, None, "ABSENT_AT_SENSITIVITY", "assay")

    def test_interval_propagation(self):
        m = UncertaintyMatrix(dict(a=Value(2.0, "MEASURED", "p", (1.0, 3.0)), b=A(10.0)))
        r = m.propagate(lambda d: d["a"] * d["b"], ["a", "b"])
        self.assertEqual((r["low"], r["high"], r["no_interval"]), (10.0, 30.0, ["b"]))


if __name__ == "__main__":
    unittest.main()
