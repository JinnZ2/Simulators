"""G5 item 7: harness classes by information source (H-A) and by measured power (H-B).

Written before cplay/harness_branches.py. No branch is picked; the SPLIT table is the output.
"""
import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cplay import harness_branches as H  # noqa: E402


class HA(unittest.TestCase):
    def test_labels_are_m7s(self):
        self.assertEqual(H.HA_LABELS, ("KNOWN_ANSWER", "NULL_ONLY", "PLANTED_FAULT", "CIRCULAR"))

    def test_classify_by_source(self):
        by = {h.name: H.classify_source(h) for h in H.HARNESSES}
        self.assertEqual(by["en_strong"], "KNOWN_ANSWER")
        self.assertEqual(by["en_weak"], "KNOWN_ANSWER")
        self.assertEqual(by["g_table"], "CIRCULAR")
        self.assertEqual(by["en_null_only"], "NULL_ONLY")
        self.assertEqual(by["en_plants_only"], "PLANTED_FAULT")


class HB(unittest.TestCase):
    def test_rates_measured_not_thresholded(self):
        r = H.measure_power(H.get("en_strong"))
        self.assertEqual(r["catch"], (r["caught"], r["n_faults"]))
        self.assertEqual(r["bin_catch"], "CATCHES_ALL" if r["caught"] == r["n_faults"] else
                         ("CATCHES_NONE" if r["caught"] == 0 else "PARTIAL"))

    def test_measured_weaknesses_kept_not_tuned_away(self):
        s = H.measure_power(H.get("en_strong"))
        w = H.measure_power(H.get("en_weak"))
        self.assertEqual((s["bin_catch"], s["missed"]), ("CATCHES_ALL", ()))        # after added cases
        self.assertEqual((w["bin_catch"], w["caught"]), ("CATCHES_NONE", 0))
        self.assertEqual(H.measure_power(H.get("poisson"))["missed"], ())
        self.assertEqual(H.measure_power(H.get("poisson"), base_only=True)["missed"], ("critical_strict",))
        self.assertEqual(H.measure_power(H.get("en_strong"), base_only=True)["missed"], ("uc_linear_sum",))
        self.assertEqual(H.measure_power(H.get("g_table"))["missed"], ("floor_out_of_u",))

    def test_equivalent_nulls_raise_no_false_alarm_on_good_harness(self):
        s = H.measure_power(H.get("en_strong"))
        self.assertEqual((s["false_alarms"], s["bin_false_alarm"]), (0, "QUIET"))

    def test_no_cases_power_none(self):
        r = H.measure_power(H.get("en_null_only"))
        self.assertIsNone(r["catch_rate"])
        self.assertEqual(r["bin_catch"], "NOT_MEASURABLE")

    def test_original_passes_its_own_cases(self):
        for h in H.HARNESSES:
            if h.cases:
                self.assertEqual(H.failures(h, h.fn), [], h.name)


class Split(unittest.TestCase):
    def test_split_rows(self):
        rows = H.table()
        split = [r["harness"] for r in rows if r["split"]]
        self.assertEqual(split, ["en_weak"])            # after the evidence round
        circ = next(r for r in rows if r["harness"] == "g_table")
        self.assertEqual(circ["H-A"], "CIRCULAR")    # reported beside its measured power

    def test_no_winner_field(self):
        for r in H.table():
            self.assertNotIn("winner", r)


if __name__ == "__main__":
    unittest.main()


class EvidenceRound(unittest.TestCase):
    """Added cases: RSS vs linear-sum separation, Poisson lam = 1. Before/after kept."""
    def test_added_cases_are_hand_known(self):
        self.assertEqual(H.ADDED["en_strong"][0].expected, "FAILED")     # RSS En 1.2, linear 0.857
        self.assertEqual(H.ADDED["poisson"][0].inputs, (1.0,))

    def test_before_after_catch_counts(self):
        rows = {r["harness"]: r for r in H.table()}
        self.assertEqual((rows["en_strong"]["catch_before"], rows["en_strong"]["catch"]), ((4, 5), (5, 5)))
        self.assertEqual((rows["poisson"]["catch_before"], rows["poisson"]["catch"]), ((3, 4), (4, 4)))
        self.assertEqual(rows["en_strong"]["power"], "CATCHES_ALL")
        self.assertEqual(rows["poisson"]["power"], "CATCHES_ALL")

    def test_provenance_field_and_power_rating(self):
        r = next(r for r in H.table() if r["harness"] == "en_weak")
        self.assertEqual((r["provenance"], r["power"]), ("KNOWN_ANSWER", "CATCHES_NONE"))

    def test_added_cases_raise_no_false_alarm(self):
        for name in ("en_strong", "poisson"):
            self.assertEqual(H.measure_power(H.get(name))["false_alarms"], 0)
