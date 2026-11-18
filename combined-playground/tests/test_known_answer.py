"""M7 known-answer gate and CIRCULAR_KNOWN_ANSWER (COMBINED_SPEC section 6; section 8 rows 9-13).

Written before cplay/known_answer.py.
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import known_answer as K  # noqa: E402


def _case(cid="c1", src="hand calc, ladder 1"):
    return K.Case(case_id=cid, inputs={"x": 2}, expected=4, provenance=src)


TESTED = ("formula:branching_closed_form", "model:forest_v6")


class Cases(unittest.TestCase):
    def test_provenance_required(self):
        with self.assertRaises(K.KAError):
            K.Case(case_id="c", inputs={}, expected=1, provenance="")

    def test_circular_when_provenance_names_tested(self):
        c = _case(src="derived from formula:branching_closed_form")
        self.assertEqual(K.circular_source(c, TESTED), "formula:branching_closed_form")
        self.assertIsNone(K.circular_source(_case(), TESTED))

    def test_tested_set_must_be_declared(self):
        with self.assertRaises(K.KAError):
            K.run_cases([_case()], tested=(), check=lambda c: True, module="m")


class Run(unittest.TestCase):
    def test_zero_cases_untested(self):
        r = K.run_cases([], tested=TESTED, check=lambda c: True, module="m")
        self.assertEqual((r.reading.status, r.reading.reason), ("UNTESTED", "KA_NO_CASES"))

    def test_all_circular_is_untested_and_counts_nothing(self):
        cs = [_case("a", "copied from model:forest_v6 fluxes"),
              _case("b", "formula:branching_closed_form evaluated")]
        r = K.run_cases(cs, tested=TESTED, check=lambda c: True, module="m")
        self.assertEqual(r.reading.status, "UNTESTED")
        self.assertIn("CIRCULAR_KNOWN_ANSWER", r.reading.reason)
        self.assertEqual(r.counted, ())
        self.assertEqual(len(r.circular), 2)

    def test_circular_excluded_from_counts(self):
        cs = [_case("a"), _case("b", "model:forest_v6")]
        r = K.run_cases(cs, tested=TESTED, check=lambda c: True, module="m")
        self.assertEqual([x.case_id for x, _ in r.counted], ["a"])
        self.assertEqual([x.case_id for x, _ in r.circular], ["b"])

    def test_verdict_needs_plant_harness(self):
        r = K.run_cases([_case()], tested=TESTED, check=lambda c: True, module="m")
        self.assertIsNone(r.reading)                  # no axis status without a verdict rule
        self.assertEqual(r.verdict.state, "UNTESTED")          # 9c item 8: ka_verdict needs plants
        self.assertEqual(r.passed, 1)
        self.assertEqual(r.failed, 0)

    def test_crash_in_check_is_a_record(self):
        def boom(c):
            raise ZeroDivisionError("0/0")
        r = K.run_cases([_case()], tested=TESTED, check=boom, module="harness")
        self.assertEqual(r.reading.status, "CRASHED")
        self.assertEqual(r.coverage[0].kind, "GAP_INSTRUMENT_CRASH")
        self.assertEqual(r.coverage[0].input["case_id"], "c1")

    def test_check_must_return_bool(self):
        r = K.run_cases([_case()], tested=TESTED, check=lambda c: 1, module="m")
        self.assertEqual(r.reading.status, "CRASHED")


class Plants(unittest.TestCase):
    """Rows 10-12: each plant names its axis; null-only harness gives a record; FP/TP carried."""
    def test_plant_names_axis(self):
        with self.assertRaises(K.KAError):
            K.Plant(plant_id="p", expected_axis="SOMEWHERE", is_null=False)
        K.Plant(plant_id="p", expected_axis="PHYSICAL", is_null=False)

    def test_null_only_harness_gives_record_not_crash(self):
        plants = [K.Plant(plant_id="n%d" % i, expected_axis=None, is_null=True) for i in range(3)]
        r = K.harness(plants, fired=lambda p: False)
        self.assertEqual(r["fp"], 0)
        self.assertIsNone(r["tp_rate"])               # no signal plants: not a crash, not 0/0
        self.assertEqual(r["tp_rate_reason"], "NO_SIGNAL_PLANTS")
        self.assertEqual(r["harness_class"].state, "VOID")

    def test_fp_tp_counts(self):
        plants = [K.Plant(plant_id="s", expected_axis="PHYSICAL", is_null=False),
                  K.Plant(plant_id="n", expected_axis=None, is_null=True)]
        r = K.harness(plants, fired=lambda p: True)
        self.assertEqual((r["tp"], r["fp"], r["tp_rate"], r["fp_rate"]), (1, 1, 1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
