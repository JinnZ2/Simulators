"""M3 axes, statuses, COVERAGE, #257 mapping (COMBINED_SPEC section 2).

Written before cplay/axes.py, from the spec's own rules R-A1..R-A5.
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import axes as A  # noqa: E402
from cplay import tokens as T  # noqa: E402


def _cov(**kw):
    base = dict(kind="INFO", module="m", input=None, reason="r",
                missing_path=None, expiry_condition=None)
    base.update(kw)
    return A.CoverageEntry(**base)


class Shape(unittest.TestCase):
    def test_three_failure_axes_and_applicability_apart(self):
        self.assertEqual(A.AXES, ("PHYSICAL", "INSTRUMENT", "DETERMINATION"))
        self.assertNotIn("APPLICABILITY", A.AXES)
        self.assertNotIn("COVERAGE", A.AXES)
        self.assertEqual(A.FIELDS, A.AXES + ("APPLICABILITY",))

    def test_statuses_are_tokens_states(self):
        for s in A.STATUSES:
            self.assertIn(s, T.STATES)

    def test_reason_rules_per_status(self):
        A.reading("PHYSICAL", "OK")
        for s in ("FAILED", "INDETERMINATE", "UNTESTED"):
            with self.assertRaises(A.AxisError):
                A.reading("PHYSICAL", s)
            A.reading("PHYSICAL", s, reason="x")
        with self.assertRaises(A.AxisError):
            A.reading("INSTRUMENT", "CRASHED", reason="x")          # needs exception + path
        A.reading("INSTRUMENT", "CRASHED", exception="ZeroDivisionError", path="certify_tool")
        with self.assertRaises(A.AxisError):
            A.reading("PHYSICAL", "CLOSED_WITHIN", sigma=0.1)       # needs basis
        A.reading("PHYSICAL", "CLOSED_WITHIN", sigma=0.1, basis="declared per account")

    def test_closed_within_off_physical_is_void_not_a_reading(self):
        for f in ("INSTRUMENT", "DETERMINATION"):
            got = A.reading(f, "CLOSED_WITHIN", sigma=0.1, basis="b")
            self.assertIsInstance(got, T.Token)
            self.assertEqual(got.state, "VOID")
            self.assertIn("PHYSICAL only", got.reason)
            with self.assertRaises(A.AxisError):
                A.Record({f: got}, coverage=[])          # a VOID token cannot sit on an axis
        with self.assertRaises(A.AxisError):
            A.reading("APPLICABILITY", "OUTSIDE_DOMAIN")            # needs the bound
        A.reading("APPLICABILITY", "OUTSIDE_DOMAIN", bound="n <= 200")

    def test_field_restrictions_stated_in_spec(self):
        # CRASHED stays an INSTRUMENT status (R-A2)
        for f in ("PHYSICAL", "DETERMINATION", "APPLICABILITY"):
            with self.assertRaises(A.AxisError):
                A.reading(f, "CRASHED", exception="E", path="p")
        # OUTSIDE_DOMAIN is APPLICABILITY only; APPLICABILITY is on no failure axis
        for f in A.AXES:
            with self.assertRaises(A.AxisError):
                A.reading(f, "OUTSIDE_DOMAIN", bound="b")
        with self.assertRaises(A.AxisError):
            A.reading("APPLICABILITY", "FAILED", reason="x")
        with self.assertRaises(A.AxisError):
            A.reading("COVERAGE", "OK")


class Coverage(unittest.TestCase):
    def test_kinds_from_taf(self):
        self.assertEqual(A.COVERAGE_KINDS, ("UNKNOWN", "INFO", "GAP_INSTRUMENT_CRASH"))
        with self.assertRaises(A.AxisError):
            _cov(kind="SEVERE")

    def test_all_six_fields_must_be_passed_no_defaults(self):
        with self.assertRaises(TypeError):
            A.CoverageEntry(kind="INFO", module="m", reason="r")

    def test_coverage_never_feeds_severity(self):
        r1 = A.Record({"PHYSICAL": A.reading("PHYSICAL", "OK")}, coverage=[])
        r2 = A.Record({"PHYSICAL": A.reading("PHYSICAL", "OK")},
                      coverage=[_cov(kind="GAP_INSTRUMENT_CRASH", reason="x")] * 5)
        self.assertEqual(r1.severity(), r2.severity())

    def test_severity_has_no_composite(self):
        sev = A.Record({}, coverage=[]).severity()
        self.assertEqual(tuple(sev), A.AXES)
        self.assertEqual(A.COMPOSITE_SEVERITY.state, "VOID")


class Crash(unittest.TestCase):
    """R-A2: a crash is a record, on the coverage axis, never severity, never no-row."""
    def test_crash_gives_reading_and_coverage_entry(self):
        rd, cov = A.crash(ZeroDivisionError("division by zero"), path="certify_tool",
                          module="playground.tools", inputs={"harness": "null-only"},
                          expiry_condition=None)
        self.assertEqual((rd.field, rd.status), ("INSTRUMENT", "CRASHED"))
        self.assertEqual(rd.exception, "ZeroDivisionError")
        self.assertEqual(cov.kind, "GAP_INSTRUMENT_CRASH")
        self.assertEqual(cov.missing_path, "certify_tool")

    def test_record_from_crash_keeps_a_row_and_coverage(self):
        rd, cov = A.crash(ValueError("v"), path="p", module="m", inputs=None,
                          expiry_condition=None)
        rec = A.Record({"INSTRUMENT": rd}, coverage=[cov])
        self.assertEqual(rec.get("INSTRUMENT").status, "CRASHED")
        self.assertEqual(len(rec.coverage), 1)

    def test_crashed_without_coverage_entry_refused(self):
        rd = A.reading("INSTRUMENT", "CRASHED", exception="E", path="p")
        with self.assertRaises(A.AxisError):
            A.Record({"INSTRUMENT": rd}, coverage=[])

    def test_crash_does_not_change_severity_beyond_its_axis_status(self):
        rd, cov = A.crash(ValueError("v"), path="p", module="m", inputs=None,
                          expiry_condition=None)
        sev = A.Record({"INSTRUMENT": rd}, coverage=[cov]).severity()
        self.assertEqual(sev["INSTRUMENT"], "CRASHED")
        self.assertEqual(sev["PHYSICAL"], "UNTESTED")


class Untested(unittest.TestCase):
    """R-A3: a field no gate read is UNTESTED, never OK by default."""
    def test_unread_fields_untested(self):
        rec = A.Record({}, coverage=[])
        for f in A.FIELDS:
            g = rec.get(f)
            self.assertEqual(g.status, "UNTESTED")
            self.assertEqual(g.reason, "NO_GATE_READ")


class Map257(unittest.TestCase):
    def test_closure_fail_declared_complete_is_physical(self):
        r = A.map_257("l0.did_not_close", declared_complete=True)
        self.assertEqual((r.field, r.status), ("PHYSICAL", "FAILED"))

    def test_closure_fail_not_declared_is_determination(self):
        r = A.map_257("l0.did_not_close", declared_complete=False)
        self.assertEqual((r.field, r.status), ("DETERMINATION", "FAILED"))

    def test_R_A1_absent_flag_counts_as_not_declared(self):
        r = A.map_257("l0.did_not_close")
        self.assertEqual(r.field, "DETERMINATION")
        for truthy in (1, "yes", "True"):
            r = A.map_257("l0.did_not_close", declared_complete=truthy)
            self.assertEqual(r.field, "DETERMINATION")       # only literal True is a declaration

    def test_no_live_budget(self):
        r = A.map_257("l0.no_live_budget")
        self.assertEqual((r.field, r.status, r.reason), ("DETERMINATION", "UNTESTED", "NO_LIVE_BUDGET"))

    def test_noise_needs_sigma_and_basis(self):
        with self.assertRaises(A.AxisError):
            A.map_257("l0.noise")
        r = A.map_257("l0.noise", sigma=0.02, basis="declared for account N")
        self.assertEqual((r.field, r.status), ("PHYSICAL", "CLOSED_WITHIN"))

    def test_untrusted_no_cases_circular(self):
        self.assertEqual(A.map_257("certify.untrusted").status, "FAILED")
        r = A.map_257("trust.no_cases")
        self.assertEqual((r.field, r.status, r.reason), ("INSTRUMENT", "UNTESTED", "KA_NO_CASES"))
        r = A.map_257("known_answer.circular")
        self.assertEqual(r.reason, "CIRCULAR_KNOWN_ANSWER")

    def test_tool_raise_routes_to_crash(self):
        with self.assertRaises(A.AxisError):
            A.map_257("certify_tool.raise")      # use crash(); it carries the coverage entry

    def test_bound_hit_on_no_failure_axis(self):
        r = A.map_257("bound.hit", bound="population <= 500")
        self.assertEqual((r.field, r.status), ("APPLICABILITY", "OUTSIDE_DOMAIN"))

    def test_unknown_source_refused_not_defaulted(self):
        with self.assertRaises(A.AxisError):
            A.map_257("l0.something_new")


class Relabel(unittest.TestCase):
    """R-A5: step-1 code preserved; the COMBINED reading is a second column."""
    def test_two_columns(self):
        rd = A.map_257("trust.no_cases")
        row = A.relabel("NO_SLOT", rd)
        self.assertEqual(row.step1_code, "NO_SLOT")
        self.assertIs(row.combined, rd)
        with self.assertRaises(A.AxisError):
            A.relabel("", rd)


if __name__ == "__main__":
    unittest.main()
