"""Command-line interface and synthetic demonstration."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import make_model, make_experiment, make_observation, make_audit_event, write_jsonl, read_jsonl


def build_demo_records():
    model = make_model(
        name="Illustrative beach bottle-count estimator", version="0.1",
        purpose="Estimate plastic bottles in a defined beach segment.",
        target_quantity="bottle_count",
        scope_included=["defined segment", "visible bottles", "recorded survey window"],
        scope_excluded=["buried bottles", "microplastics", "non-bottle debris", "unobserved areas"],
        assumptions=["survey boundary held fixed", "reference protocol documented"],
        dependencies=[
            {"from": "visibility", "to": "observed_bottle_count", "status": "hypothesized"},
            {"from": "survey_coverage", "to": "observed_bottle_count", "status": "declared"},
        ],
        units={"bottle_count": "count", "coverage": "fraction"},
        unknowns=["occlusion sensitivity", "sensitivity to debris density"],
        representation={"kind": "aggregated estimator", "compression_ratio": "not measured"},
        provenance={"status": "synthetic demonstration only"},
    )
    experiment = make_experiment(
        model_record_id=model.record_id,
        question="Does the estimator preserve bottle count under reduced visibility?",
        conditions={"segment_id": "synthetic_A", "visibility_fraction": 0.75,
                    "survey_protocol": "synthetic"},
        changed_factors=["visibility_fraction"],
        control_description="Compare with synthetic reference count on the same segment.",
        planned_comparisons=["prediction vs reference", "high vs reduced visibility"],
        expected_observations="No result assumed in advance.", status="run",
    )
    observation = make_observation(
        experiment_record_id=experiment.record_id, model_record_id=model.record_id,
        quantity="bottle_count", predicted_value=80, observed_value=87, unit="count",
        prediction_uncertainty=4, observation_uncertainty=2,
        method="synthetic illustrative values", conditions={"visibility_fraction": 0.75},
        source_kind="synthetic",
        notes=["Fabricated values demonstrate record format; not field measurements."],
    )
    event = make_audit_event(
        subject_record_ids=[model.record_id, experiment.record_id, observation.record_id],
        event_kind="discrepancy_recorded",
        description="A non-zero residual was recorded; its cause remains unassigned.",
        evidence=["synthetic prediction and reference differ by 7 counts"],
        unresolved_questions=[
            "Does visibility explain the discrepancy?",
            "Does a more detailed representation generalize to independent cases?",
            "What uncertainty attaches to the reference protocol?",
        ],
        proposed_next_tests=[
            "repeat at multiple synthetic visibility levels",
            "compare with object-level representation",
            "test on held-out cases",
        ],
    )
    return [model, experiment, observation, event]


def main():
    parser = argparse.ArgumentParser(prog="scope-audit-lab")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="write synthetic demonstration records")
    demo.add_argument("--out", default="demo_output.jsonl")
    validate = sub.add_parser("validate", help="structurally validate a JSONL event stream")
    validate.add_argument("path")
    args = parser.parse_args()
    if args.command == "demo":
        path = Path(args.out)
        count = write_jsonl(str(path), build_demo_records())
        print(json.dumps({"output": str(path), "records_appended": count,
                          "data_status": "synthetic demonstration only",
                          "interpretation": "no model verdict assigned"}, indent=2))
    else:
        records, errors = read_jsonl(args.path)
        print(json.dumps({"path": args.path, "valid_records": len(records), "errors": errors,
                          "structural_status": "valid" if not errors else "issues found",
                          "scientific_validity": "not evaluated by structural validator"}, indent=2))
        raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
