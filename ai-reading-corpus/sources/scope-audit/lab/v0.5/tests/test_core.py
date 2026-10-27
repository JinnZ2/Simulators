import tempfile
import unittest
from pathlib import Path
from scope_audit_lab.core import (
    compare_numeric, make_model, make_experiment, make_observation,
    make_audit_event, validate_record, write_jsonl, read_jsonl,
)


class NumericComparisonTests(unittest.TestCase):
    def test_residual_is_observed_minus_predicted(self):
        result = compare_numeric(10, 13)
        self.assertEqual(result.residual, 3)
        self.assertEqual(result.absolute_residual, 3)
        self.assertEqual(result.comparison_status, "computed; interpretation unresolved")

    def test_combined_uncertainty(self):
        result = compare_numeric(10, 13, 3, 4)
        self.assertEqual(result.combined_uncertainty, 5)
        self.assertAlmostEqual(result.normalized_residual, 0.6)

    def test_relative_residual_undefined_at_zero_observation(self):
        result = compare_numeric(2, 0)
        self.assertIsNone(result.relative_residual)

    def test_negative_uncertainty_rejected(self):
        with self.assertRaises(ValueError):
            compare_numeric(1, 2, observation_uncertainty=-1)

    def test_nonfinite_values_rejected(self):
        with self.assertRaises(ValueError):
            compare_numeric(float("nan"), 2)


class RecordTests(unittest.TestCase):
    def test_unknowns_retained(self):
        model = make_model(name="M", version="1", purpose="estimate q",
                           target_quantity="q", scope_included=[], unknowns=["B unmeasured"])
        self.assertEqual(model.payload["unknowns"], ["B unmeasured"])

    def test_audit_has_no_verdict(self):
        event = make_audit_event(subject_record_ids=[], event_kind="mismatch",
                                 description="Residual observed")
        self.assertIsNone(event.payload["verdict"])

    def test_missing_value_means_comparison_not_computed(self):
        obs = make_observation(experiment_record_id="e", model_record_id="m",
                               quantity="q", predicted_value=None, observed_value=3, unit="m")
        self.assertEqual(obs.payload["comparison"]["comparison_status"], "not computed")
        self.assertEqual(obs.payload["interpretation"], "unassigned")

    def test_bad_experiment_status_rejected(self):
        with self.assertRaises(ValueError):
            make_experiment(model_record_id="m", question="q", conditions={},
                            changed_factors=[], control_description="control", status="pass")

    def test_structural_validation(self):
        model = make_model(name="M", version="1", purpose="p", target_quantity="q",
                           scope_included=[])
        self.assertEqual(validate_record(model.to_dict()), [])

    def test_jsonl_roundtrip(self):
        records = [
            make_model(name="M", version="1", purpose="p", target_quantity="q",
                       scope_included=[]),
            make_audit_event(subject_record_ids=[], event_kind="open",
                             description="No conclusion assigned"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "records.jsonl")
            self.assertEqual(write_jsonl(path, records), 2)
            loaded, errors = read_jsonl(path)
            self.assertEqual(len(loaded), 2)
            self.assertEqual(errors, [])
            self.assertEqual(loaded[0]["record_type"], "model")


if __name__ == "__main__":
    unittest.main()
