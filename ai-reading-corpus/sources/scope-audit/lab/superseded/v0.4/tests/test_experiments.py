"""Tests for the v0.3 experiment procedures. Standard library only."""
from __future__ import annotations
import json
import math
import tempfile
import unittest
from pathlib import Path

from scope_audit_lab.core import (validate_record, read_jsonl, write_jsonl,
                                  Record)
from scope_audit_lab.transitions import Case
from scope_audit_lab.experiments import (
    null_baseline_scan, threshold_sweep, order_permutation_probe,
    coupling_scan, make_experiment_record, EXPERIMENT_KINDS,
    SYNTHETIC_LABEL,
)
from scope_audit_lab.__main__ import build_experiments_demo_records


def step_cases():
    outs = [5.0, 6.0, 4.0, 31.0, 30.0, 8.0, 9.0, 60.0]
    return [Case(f"s{i}", float(i), o, "t", "y") for i, o in enumerate(outs)]


class NullBaselineTests(unittest.TestCase):
    def test_deterministic_given_seed(self):
        a = null_baseline_scan(n_cases=10, n_replications=5, threshold=9.0,
                               seed=42)
        b = null_baseline_scan(n_cases=10, n_replications=5, threshold=9.0,
                               seed=42)
        self.assertEqual(a["replications"], b["replications"])

    def test_replication_count_and_shape(self):
        r = null_baseline_scan(n_cases=12, n_replications=7, threshold=10.0,
                               seed=1)
        self.assertEqual(len(r["replications"]), 7)
        for rep in r["replications"]:
            self.assertIsInstance(rep["candidate_region_count"], int)
            self.assertEqual(rep["candidate_region_count"],
                             len(rep["candidate_regions"]))
            self.assertEqual(rep["deltas_computed"], 11)

    def test_summary_matches_replications(self):
        r = null_baseline_scan(n_cases=12, n_replications=9, threshold=10.0,
                               seed=5)
        counts = [x["candidate_region_count"] for x in r["replications"]]
        s = r["recorded_summary"]
        self.assertEqual(s["min_candidate_regions"], min(counts))
        self.assertEqual(s["max_candidate_regions"], max(counts))
        self.assertAlmostEqual(s["mean_candidate_regions"],
                               sum(counts) / len(counts))

    def test_synthetic_label_present(self):
        r = null_baseline_scan(n_cases=5, n_replications=2, threshold=1.0,
                               seed=0)
        self.assertEqual(r["data_status"], SYNTHETIC_LABEL)
        self.assertEqual(r["planted_structure"], "none (by construction)")
        self.assertEqual(r["interpretation"], "unassigned")

    def test_higher_threshold_flags_no_more_than_lower(self):
        low = null_baseline_scan(n_cases=15, n_replications=6, threshold=5.0,
                                 seed=11)
        high = null_baseline_scan(n_cases=15, n_replications=6, threshold=50.0,
                                  seed=11)
        for rl, rh in zip(low["replications"], high["replications"]):
            self.assertLessEqual(rh["candidate_region_count"],
                                 rl["candidate_region_count"])

    def test_normal_distribution_recorded(self):
        r = null_baseline_scan(n_cases=8, n_replications=3, threshold=2.0,
                               seed=2, distribution="normal", mean=0.0,
                               sd=1.0)
        self.assertEqual(r["generator"]["distribution"], "normal")
        self.assertEqual(r["generator"]["parameters"]["sd"], 1.0)

    def test_invalid_arguments_rejected(self):
        with self.assertRaises(ValueError):
            null_baseline_scan(n_cases=1, n_replications=1, threshold=1.0,
                               seed=0)
        with self.assertRaises(ValueError):
            null_baseline_scan(n_cases=5, n_replications=0, threshold=1.0,
                               seed=0)
        with self.assertRaises(ValueError):
            null_baseline_scan(n_cases=5, n_replications=1, threshold=-1.0,
                               seed=0)
        with self.assertRaises(ValueError):
            null_baseline_scan(n_cases=5, n_replications=1, threshold=1.0,
                               seed=0, distribution="cauchy")
        with self.assertRaises(ValueError):
            null_baseline_scan(n_cases=5, n_replications=1, threshold=1.0,
                               seed=0, low=10.0, high=0.0)


class ThresholdSweepTests(unittest.TestCase):
    def test_counts_nonincreasing_with_sorted_thresholds(self):
        r = threshold_sweep(step_cases(), thresholds=[1.0, 5.0, 10.0, 20.0,
                                                      30.0])
        counts = [p["candidate_region_count"] for p in r["per_threshold"]]
        for a, b in zip(counts, counts[1:]):
            self.assertGreaterEqual(a, b)

    def test_threshold_order_preserved_not_sorted(self):
        r = threshold_sweep(step_cases(), thresholds=[20.0, 1.0, 10.0])
        self.assertEqual(r["thresholds_in_given_order"], [20.0, 1.0, 10.0])
        self.assertEqual([p["threshold"] for p in r["per_threshold"]],
                         [20.0, 1.0, 10.0])

    def test_appearances_consistent_with_per_threshold(self):
        r = threshold_sweep(step_cases(), thresholds=[5.0, 10.0, 20.0])
        tally = {}
        for p in r["per_threshold"]:
            for region in p["candidate_regions"]:
                key = "|".join(sorted(region["between"]))
                tally.setdefault(key, []).append(p["threshold"])
        self.assertEqual(len(tally), len(r["region_appearances"]))
        for app in r["region_appearances"]:
            key = "|".join(sorted(app["between"]))
            self.assertEqual(sorted(app["appears_at_thresholds"]),
                             sorted(tally[key]))
            self.assertEqual(app["appearance_count"], len(tally[key]))
            self.assertEqual(app["sweep_points"], 3)

    def test_case_order_recorded(self):
        cases = step_cases()
        r = threshold_sweep(cases, thresholds=[1.0])
        self.assertEqual(r["case_ids_in_given_order"],
                         [c.case_id for c in cases])

    def test_empty_and_invalid_rejected(self):
        with self.assertRaises(ValueError):
            threshold_sweep([], thresholds=[1.0])
        with self.assertRaises(ValueError):
            threshold_sweep(step_cases(), thresholds=[])
        with self.assertRaises(ValueError):
            threshold_sweep(step_cases(), thresholds=[float("nan")])


class OrderPermutationTests(unittest.TestCase):
    def test_identity_scan_first(self):
        r = order_permutation_probe(step_cases(), n_permutations=5,
                                    threshold=10.0, seed=3)
        self.assertEqual(r["scans"][0]["order_kind"], "given_order")
        self.assertEqual(r["scans"][0]["case_ids_in_scanned_order"],
                         [c.case_id for c in step_cases()])
        for s in r["scans"][1:]:
            self.assertEqual(s["order_kind"], "seeded_permutation")

    def test_total_scans_and_appearance_bounds(self):
        r = order_permutation_probe(step_cases(), n_permutations=9,
                                    threshold=10.0, seed=4)
        self.assertEqual(len(r["scans"]), 10)
        for app in r["region_appearances"]:
            self.assertLessEqual(app["appearance_count"], 10)
            self.assertEqual(app["total_scans"], 10)
            for idx in app["appears_in_scans"]:
                scan = r["scans"][idx]
                pairs = {"|".join(sorted(reg["between"]))
                         for reg in scan["candidate_regions"]}
                self.assertIn("|".join(app["between_pair_unordered"]), pairs)

    def test_permutation_preserves_membership(self):
        cases = step_cases()
        r = order_permutation_probe(cases, n_permutations=20, threshold=10.0,
                                    seed=8)
        original = sorted(c.case_id for c in cases)
        for s in r["scans"]:
            self.assertEqual(sorted(s["case_ids_in_scanned_order"]), original)

    def test_deterministic_given_seed(self):
        a = order_permutation_probe(step_cases(), n_permutations=6,
                                    threshold=10.0, seed=99)
        b = order_permutation_probe(step_cases(), n_permutations=6,
                                    threshold=10.0, seed=99)
        self.assertEqual(a["scans"], b["scans"])

    def test_invalid_arguments_rejected(self):
        with self.assertRaises(ValueError):
            order_permutation_probe([Case("only", 1.0, 1.0)],
                                    n_permutations=1, threshold=1.0, seed=0)
        with self.assertRaises(ValueError):
            order_permutation_probe(step_cases(), n_permutations=0,
                                    threshold=1.0, seed=0)


class CouplingScanTests(unittest.TestCase):
    def entries(self):
        rows = [(1.00, 0.2, 12.0), (0.75, 0.4, 14.0), (0.50, 0.9, 40.0),
                (0.25, 0.3, 38.0), (0.10, 0.2, 60.0), (0.00, 0.8, 61.0)]
        return [{"case_id": f"c{i}", "factor_a": a, "factor_b": b,
                 "output": o} for i, (a, b, o) in enumerate(rows)]

    def test_partition_is_exact(self):
        r = coupling_scan(self.entries(), threshold=10.0)
        cr = r["coincidence_record"]
        a_pairs = {"|".join(sorted(reg["between"]))
                   for reg in r["factor_a_scan"]["candidate_regions"]}
        b_pairs = {"|".join(sorted(reg["between"]))
                   for reg in r["factor_b_scan"]["candidate_regions"]}
        coinc = {"|".join(p) for p in cr["coincident_pairs"]}
        only_a = {"|".join(p) for p in cr["factor_a_only_pairs"]}
        only_b = {"|".join(p) for p in cr["factor_b_only_pairs"]}
        self.assertEqual(coinc, a_pairs & b_pairs)
        self.assertEqual(only_a, a_pairs - b_pairs)
        self.assertEqual(only_b, b_pairs - a_pairs)

    def test_coincidence_note_forbids_causal_reading(self):
        r = coupling_scan(self.entries(), threshold=10.0)
        self.assertIn("does not establish a shared cause",
                      r["coincidence_record"]["note"])

    def test_missing_factor_recorded_not_dropped(self):
        entries = self.entries()
        entries[2]["factor_b"] = None
        r = coupling_scan(entries, threshold=10.0)
        self.assertEqual(r["factor_b_scan"]["deltas_not_computed"], 2)
        self.assertTrue(r["factor_b_scan"]["unresolved"])

    def test_labels_recorded(self):
        r = coupling_scan(self.entries(), threshold=10.0,
                          factor_a_label="visibility",
                          factor_b_label="tide", output_label="count")
        self.assertEqual(r["factor_a_label"], "visibility")
        self.assertEqual(r["factor_b_label"], "tide")
        self.assertEqual(r["output_label"], "count")

    def test_duplicate_and_missing_ids_rejected(self):
        bad = [{"case_id": "x", "factor_a": 1, "factor_b": 1, "output": 1},
               {"case_id": "x", "factor_a": 2, "factor_b": 2, "output": 2}]
        with self.assertRaises(ValueError):
            coupling_scan(bad, threshold=1.0)
        with self.assertRaises(ValueError):
            coupling_scan([{"factor_a": 1, "factor_b": 1, "output": 1}],
                          threshold=1.0)


class ExperimentRecordTests(unittest.TestCase):
    def test_record_validates_and_roundtrips(self):
        for kind_payload in (
            null_baseline_scan(n_cases=6, n_replications=2, threshold=5.0,
                               seed=1),
            threshold_sweep(step_cases(), thresholds=[5.0, 10.0]),
            order_permutation_probe(step_cases(), n_permutations=3,
                                    threshold=10.0, seed=1),
            coupling_scan([{"case_id": "a", "factor_a": 1, "factor_b": 2,
                            "output": 3},
                           {"case_id": "b", "factor_a": 2, "factor_b": 1,
                            "output": 30}], threshold=5.0),
        ):
            record = make_experiment_record(kind_payload,
                                            linked_record_ids=["model_x"])
            validate_record(record.to_dict())
            self.assertEqual(record.record_type, "experiment")
            self.assertEqual(record.schema_version, "0.2")
            self.assertIn(kind_payload["experiment_kind"], EXPERIMENT_KINDS)
            with tempfile.TemporaryDirectory() as tmp:
                path = str(Path(tmp) / "s.jsonl")
                write_jsonl(path, [record])
                loaded, errors = read_jsonl(path)
                self.assertEqual(errors, [])
                self.assertEqual(loaded[0], record.to_dict())

    def test_unknown_kind_rejected(self):
        with self.assertRaises(ValueError):
            make_experiment_record({"experiment_kind": "horoscope"})

    def test_demo_records_validate_and_have_no_verdict(self):
        records = build_experiments_demo_records()
        kinds = [r.payload.get("experiment_kind") for r in records
                 if r.record_type == "experiment"]
        self.assertEqual(kinds, ["null_baseline_scan", "threshold_sweep",
                                 "order_permutation_probe", "coupling_scan"])
        for record in records:
            validate_record(record.to_dict())
            if "verdict" in record.payload:
                self.assertIsNone(record.payload["verdict"])
            blob = json.dumps(record.to_dict())
            self.assertNotIn('"interpretation": "assigned"', blob)
        event = records[-1]
        self.assertEqual(event.record_type, "audit_event")
        self.assertEqual(len(event.payload["subject_record_ids"]), 4)


if __name__ == "__main__":
    unittest.main()
