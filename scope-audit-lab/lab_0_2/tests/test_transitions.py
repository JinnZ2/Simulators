"""Tests for the scope-transition experiment engine (v0.2).

Mandated coverage from the v0.2 specification: threshold behavior,
input-order preservation, missing measurements, and zero-valued outputs.
"""
import json
import tempfile
import unittest
from pathlib import Path

from scope_audit_lab.core import (SCHEMA_VERSION, make_transition_scan,
                                  validate_record, write_jsonl, read_jsonl)
from scope_audit_lab.transitions import (Case, adjacent_deltas,
                                         scan_transitions)


def make_cases(specs):
    return [Case(cid, f, o, "visibility", "count") for cid, f, o in specs]


class ThresholdBehaviorTests(unittest.TestCase):
    def test_strictly_greater_than_threshold(self):
        # deltas between adjacent pairs: +5, +10, +15
        cases = make_cases([("a", 1, 0), ("b", 2, 5), ("c", 3, 15), ("d", 4, 30)])
        result = scan_transitions(cases, threshold=10.0)
        flagged = [(c["between"][0], c["between"][1])
                   for c in result["candidate_regions"]]
        self.assertNotIn(("a", "b"), flagged)   # 5 < 10: not flagged
        self.assertNotIn(("b", "c"), flagged)   # 10 == 10: NOT flagged (strict)
        self.assertIn(("c", "d"), flagged)      # 15 > 10: flagged

    def test_relative_threshold_kind(self):
        cases = make_cases([("a", 1, 100), ("b", 2, 150), ("c", 3, 160)])
        result = scan_transitions(cases, threshold=0.25, threshold_kind="relative")
        flagged = [c["between"] for c in result["candidate_regions"]]
        self.assertEqual(flagged, [["a", "b"]])  # 50% jump flagged; 6.7% not

    def test_candidate_records_direction_and_interval(self):
        cases = make_cases([("a", 1.0, 10), ("b", 2.0, 40)])
        result = scan_transitions(cases, threshold=5.0)
        region = result["candidate_regions"][0]
        self.assertEqual(region["direction"], "increase")
        self.assertEqual(region["factor_interval"], [1.0, 2.0])
        self.assertIn("unassigned", region["classification"])

    def test_invalid_threshold_rejected(self):
        cases = make_cases([("a", 1, 1), ("b", 2, 2)])
        with self.assertRaises(ValueError):
            scan_transitions(cases, threshold=-1.0)
        with self.assertRaises(ValueError):
            scan_transitions(cases, threshold=float("nan"))
        with self.assertRaises(ValueError):
            scan_transitions(cases, threshold=1.0, threshold_kind="big")

    def test_empty_and_single_case_scans(self):
        self.assertEqual(scan_transitions([], threshold=1.0)["candidate_regions"], [])
        single = scan_transitions(make_cases([("a", 1, 5)]), threshold=1.0)
        self.assertEqual(single["candidate_regions"], [])
        self.assertEqual(single["deltas_computed"], 0)


class OrderPreservationTests(unittest.TestCase):
    def test_input_order_never_sorted(self):
        # factor values deliberately non-monotonic; order must be preserved
        cases = make_cases([("hi", 9.0, 10), ("lo", 1.0, 12), ("mid", 5.0, 60)])
        result = scan_transitions(cases, threshold=1000.0)  # nothing flagged
        ids = [c["case_id"] for c in result["cases"]]
        self.assertEqual(ids, ["hi", "lo", "mid"])
        self.assertEqual([c["order_index"] for c in result["cases"]], [0, 1, 2])

    def test_regions_reference_adjacent_pairs_in_given_order(self):
        cases = make_cases([("z", 9.0, 10), ("a", 1.0, 12), ("m", 5.0, 60)])
        result = scan_transitions(cases, threshold=10.0)
        region = result["candidate_regions"][0]
        self.assertEqual(region["between"], ["a", "m"])   # not ["z", "a"]
        self.assertEqual(region["order_indices"], [1, 2])
        self.assertEqual(region["factor_interval"], [1.0, 5.0])  # unsorted

    def test_deltas_follow_given_adjacency(self):
        cases = make_cases([("c3", 3, 1), ("c1", 1, 2), ("c2", 2, 4)])
        deltas = adjacent_deltas(cases)
        pairs = [(d.left_case_id, d.right_case_id) for d in deltas]
        self.assertEqual(pairs, [("c3", "c1"), ("c1", "c2")])


class MissingMeasurementTests(unittest.TestCase):
    def test_missing_output_preserved_with_reason(self):
        cases = make_cases([("a", 1, 10), ("gap", 2, None), ("b", 3, 12)])
        result = scan_transitions(cases, threshold=1.0)
        self.assertEqual(result["deltas_computed"], 0)
        self.assertEqual(result["deltas_not_computed"], 2)
        self.assertEqual(result["candidate_regions"], [])
        joined = " ".join(result["unresolved"])
        self.assertIn("right output missing", joined)
        self.assertIn("left output missing", joined)
        # the case itself is still in the record
        self.assertIn("gap", [c["case_id"] for c in result["cases"]])

    def test_missing_factor_does_not_drop_case(self):
        cases = make_cases([("a", None, 5), ("b", 2, 9)])
        deltas = adjacent_deltas(cases)
        self.assertEqual(deltas[0].delta_status, "not_computed")
        self.assertIn("factor missing", deltas[0].notes[0])

    def test_nonfinite_values_recorded_not_raised(self):
        cases = make_cases([("a", 1, 1.0), ("b", 2, float("inf"))])
        deltas = adjacent_deltas(cases)
        self.assertEqual(deltas[0].delta_status, "not_computed")
        self.assertIn("non-finite", deltas[0].notes[0])

    def test_scan_continues_after_gap(self):
        cases = make_cases([("a", 1, 10), ("gap", 2, None), ("b", 3, 11),
                            ("c", 4, 40)])
        result = scan_transitions(cases, threshold=5.0)
        flagged = [c["between"] for c in result["candidate_regions"]]
        self.assertEqual(flagged, [["b", "c"]])  # later valid pair still flagged


class ZeroValuedOutputTests(unittest.TestCase):
    def test_zero_left_output_absolute_ok_relative_undefined(self):
        cases = make_cases([("zero", 1, 0.0), ("next", 2, 8.0)])
        deltas = adjacent_deltas(cases)
        self.assertEqual(deltas[0].delta_status, "computed")
        self.assertEqual(deltas[0].absolute_delta, 8.0)
        self.assertIsNone(deltas[0].relative_delta)
        self.assertIn("Relative change undefined", deltas[0].notes[0])

    def test_zero_output_absolute_scan_still_flags(self):
        cases = make_cases([("zero", 1, 0.0), ("next", 2, 8.0)])
        result = scan_transitions(cases, threshold=5.0)
        self.assertEqual(len(result["candidate_regions"]), 1)

    def test_zero_output_relative_scan_records_unresolved(self):
        cases = make_cases([("zero", 1, 0.0), ("next", 2, 8.0)])
        result = scan_transitions(cases, threshold=0.1, threshold_kind="relative")
        self.assertEqual(result["candidate_regions"], [])
        self.assertTrue(any("metric undefined" in u for u in result["unresolved"]))

    def test_zero_tolerance_override(self):
        cases = make_cases([("tiny", 1, 0.001), ("next", 2, 1.0)])
        deltas = adjacent_deltas(cases, zero_tolerance=0.01)
        self.assertIsNone(deltas[0].relative_delta)


class RecordIntegrationTests(unittest.TestCase):
    def test_scan_record_validates_and_roundtrips(self):
        cases = make_cases([("a", 1, 10), ("b", 2, 30)])
        record = make_transition_scan(cases=cases, threshold=5.0,
                                      scan_label="integration test")
        self.assertEqual(validate_record(record.to_dict()), [])
        self.assertEqual(record.schema_version, SCHEMA_VERSION)
        self.assertEqual(record.payload["interpretation"], "unassigned")
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "scan.jsonl")
            self.assertEqual(write_jsonl(path, [record]), 1)
            loaded, errors = read_jsonl(path)
            self.assertEqual(errors, [])
            self.assertEqual(loaded[0]["record_type"], "transition_scan")

    def test_v01_records_still_validate(self):
        old = {"schema_version": "0.1", "record_type": "model",
               "record_id": "model_x", "created_utc": "2026-10-20T00:00:00+00:00",
               "payload": {"name": "M", "version": "1", "purpose": "p",
                           "target_quantity": "q"}}
        self.assertEqual(validate_record(old), [])

    def test_scan_links_to_existing_records(self):
        record = make_transition_scan(cases=make_cases([("a", 1, 1), ("b", 2, 2)]),
                                      threshold=0.5,
                                      linked_record_ids=["model_1", "experiment_1"])
        self.assertEqual(record.payload["linked_record_ids"],
                         ["model_1", "experiment_1"])

    def test_cli_demo_records_validate(self):
        from scope_audit_lab.__main__ import build_transitions_demo_records
        records = build_transitions_demo_records()
        self.assertEqual(len(records), 2)
        for r in records:
            self.assertEqual(validate_record(r.to_dict()), [])
        self.assertIsNone(records[1].payload["verdict"])


if __name__ == "__main__":
    unittest.main()
