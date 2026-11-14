"""Tests for load-withheld. stdlib unittest. Run: python3 test_load_withheld.py"""
import ast
import json
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load_withheld as lw  # noqa: E402
import estimate as est      # noqa: E402


class Schema(unittest.TestCase):
    def test_all_none_record_accepted(self):
        c = lw.WithheldCase()
        self.assertEqual(lw.unfilled(c), list(lw.FIELD_NAMES))

    def test_unfilled_fields_kept_in_dict(self):
        d = lw.WithheldCase().to_dict()
        self.assertEqual(set(d), set(lw.FIELD_NAMES))
        self.assertTrue(all(v is None for v in d.values()))

    def test_void_fields_survive_json_round_trip(self):
        cases = [lw.WithheldCase(), lw.WithheldCase(case_id="x", status_tag="PROPOSED")]
        text = lw.to_json(cases)
        raw = json.loads(text)
        for r in raw:
            self.assertEqual(set(r), set(lw.FIELD_NAMES))
        back = lw.from_json(text)
        self.assertEqual([c.to_dict() for c in back], [c.to_dict() for c in cases])
        self.assertIsNone(back[1].withheld_by_choice)
        self.assertIsNone(back[1].coupled_systems)

    def test_seed_cases_round_trip_and_tagged_proposed(self):
        back = lw.from_json(lw.to_json(lw.SEED_CASES))
        self.assertEqual([c.to_dict() for c in back], [c.to_dict() for c in lw.SEED_CASES])
        self.assertEqual({c.status_tag for c in lw.SEED_CASES}, {"PROPOSED"})
        self.assertEqual(len(lw.SEED_CASES), 4)

    def test_rejects(self):
        for kw in ({"status_tag": "TRUE"}, {"eligible": "yes"}, {"withheld_by_choice": 1},
                   {"est_load_units": 3.0}, {"est_load_units": True, "est_method": "x"},
                   {"coupled_systems": "ems"}):
            with self.assertRaises(ValueError, msg=str(kw)):
                lw.WithheldCase(**kw)
        with self.assertRaises(ValueError):
            lw.WithheldCase.from_dict({"surname": "x"})

    def test_no_personal_identifier_fields(self):
        for n in lw.FIELD_NAMES:
            self.assertNotIn(n, {"name", "surname", "email", "phone", "address", "author"})


class Estimator(unittest.TestCase):
    def test_bins_never_merged(self):
        r = est.withheld_estimate(1000, 700, barrier_non_take_up=120, unaware=90,
                                  deliberate_withholding=40)
        self.assertEqual(set(r["bins"]), set(est.BINS))
        self.assertEqual(r["bins"], {"barrier_non_take_up": 120, "unaware": 90,
                                     "deliberate_withholding": 40})
        merged_keys = [k for k in r if k not in ("eligible_population", "claimants", "bins",
                                                 "flags", "non_claimants", "unattributed")]
        self.assertEqual(merged_keys, [])
        self.assertEqual(r["unattributed"], 50)

    def test_deliberate_unknown_unless_reported(self):
        r = est.withheld_estimate(1000, 700, barrier_non_take_up=120, unaware=90)
        self.assertIsNone(r["bins"]["deliberate_withholding"])
        self.assertIsNone(r["unattributed"])
        self.assertTrue(any(f.startswith("DELIBERATE_SHARE_UNKNOWN") for f in r["flags"]))
        self.assertEqual(r["non_claimants"], 300)

    def test_remainder_not_assigned_to_a_bin(self):
        r = est.withheld_estimate(1000, 700)
        self.assertEqual(r["bins"], {b: None for b in est.BINS})
        self.assertEqual(r["non_claimants"], 300)

    def test_missing_counts_unknown(self):
        r = est.withheld_estimate(None, 700)
        self.assertIsNone(r["non_claimants"])
        self.assertTrue(any(f.startswith("NON_CLAIMANTS_UNKNOWN") for f in r["flags"]))

    def test_flags_on_inconsistent_counts(self):
        self.assertTrue(any(f.startswith("CLAIMANTS_EXCEED")
                            for f in est.withheld_estimate(100, 120)["flags"]))
        self.assertTrue(any(f.startswith("BINS_EXCEED")
                            for f in est.withheld_estimate(100, 50, unaware=80)["flags"]))

    def test_no_code_path_sums_bins_into_one_total(self):
        src = open(os.path.join(HERE, "estimate.py"), encoding="utf-8").read()
        tree = ast.parse(src)
        names = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
        names |= {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
        for bad in ("total_withheld", "withheld_total", "merged", "all_bins"):
            self.assertNotIn(bad, names)

    def test_peak_and_average_separate(self):
        r = est.peak_vs_average([{"load": 3, "peak": False}, {"load": 4, "peak": False},
                                 {"load": 11, "peak": True}, {"load": 9, "peak": True},
                                 {"load": 5, "peak": None}, {"load": None, "peak": True}])
        self.assertEqual(r["average"], 32 / 5)
        self.assertEqual(r["peak"], 10)
        self.assertEqual(r["off_peak"], 3.5)
        self.assertEqual((r["unknown_peak"], r["unknown_load"]), (1, 1))
        e = est.peak_vs_average([])
        self.assertEqual((e["average"], e["peak"], e["off_peak"]), (None, None, None))


if __name__ == "__main__":
    unittest.main(verbosity=1)
