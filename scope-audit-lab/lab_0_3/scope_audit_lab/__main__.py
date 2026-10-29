"""Command-line interface and synthetic demonstrations."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from .core import (make_model, make_experiment, make_observation,
                   make_audit_event, make_transition_scan, write_jsonl, read_jsonl)
from .transitions import Case
from .experiments import (null_baseline_scan, threshold_sweep,
                          order_permutation_probe, coupling_scan,
                          make_experiment_record)


def load_cases(path, factor_label="factor", output_label="output"):
    """Read a JSON list of {case_id, factor, output, notes?} into Cases."""
    with open(path, "r", encoding="utf-8") as stream:
        raw = json.load(stream)
    if not isinstance(raw, list):
        raise SystemExit("cases file must contain a JSON list")
    return [
        Case(str(item["case_id"]), item.get("factor"), item.get("output"),
             factor_label, output_label, tuple(item.get("notes", ())))
        for item in raw
    ]


def build_transitions_demo_records():
    """Synthetic visibility-variation scan. Fabricated values; not field data."""
    cases = [
        Case("vis_100", 1.00, 100.0, "visibility_fraction", "bottle_count",
             ("synthetic reference level",)),
        Case("vis_075", 0.75, 96.0, "visibility_fraction", "bottle_count"),
        Case("vis_050", 0.50, 88.0, "visibility_fraction", "bottle_count"),
        Case("vis_025", 0.25, 61.0, "visibility_fraction", "bottle_count"),
        Case("vis_000", 0.00, 0.0, "visibility_fraction", "bottle_count",
             ("zero-valued output: relative change undefined for the final pair",)),
        Case("vis_missing", None, None, "visibility_fraction", "bottle_count",
             ("missing measurement preserved, not dropped",)),
    ]
    scan = make_transition_scan(
        cases=cases, threshold=10.0, threshold_kind="absolute",
        scan_label="synthetic visibility transition scan",
    )
    event = make_audit_event(
        subject_record_ids=[scan.record_id],
        event_kind="transition_scan_recorded",
        description="Adjacent output changes were recorded; candidate regions "
                    "were flagged by threshold exceedance only.",
        evidence=[f"{len(scan.payload['candidate_regions'])} candidate region(s) recorded"],
        unresolved_questions=list(scan.payload["unresolved"]),
        proposed_next_tests=[
            "repeat scan at finer synthetic visibility steps",
            "test a relative-threshold scan on the same cases",
            "test on held-out segments",
        ],
    )
    return [scan, event]


def build_experiments_demo_records():
    """One synthetic run of each v0.3 procedure. All data fabricated."""
    step_cases = [
        Case(f"step_{i}", float(i), out, "time_index", "measured_output",
             ("synthetic; two step changes planted by construction",))
        for i, out in enumerate([5.0, 6.0, 4.0, 31.0, 30.0, 8.0, 9.0, 60.0])
    ]
    records = []

    null_rec = make_experiment_record(null_baseline_scan(
        n_cases=12, n_replications=25, threshold=10.0, seed=7,
        distribution="uniform", low=0.0, high=100.0,
        factor_label="time_index", output_label="measured_output",
        label="demo_null"))
    records.append(null_rec)

    sweep_rec = make_experiment_record(threshold_sweep(
        step_cases, thresholds=[1.0, 5.0, 10.0, 20.0, 30.0],
        sweep_label="demo_sweep"))
    records.append(sweep_rec)

    permute_rec = make_experiment_record(order_permutation_probe(
        step_cases, n_permutations=25, threshold=10.0, seed=3,
        probe_label="demo_permute"))
    records.append(permute_rec)

    coupling_entries = [
        {"case_id": f"site_{i}", "factor_a": vis, "factor_b": tide,
         "output": out,
         "notes": ("synthetic; fabricated for coupling demonstration",)}
        for i, (vis, tide, out) in enumerate([
            (1.00, 0.2, 12.0), (0.75, 0.4, 14.0), (0.50, 0.9, 40.0),
            (0.25, 0.3, 38.0), (0.10, 0.2, 60.0), (0.00, 0.8, 61.0),
        ])
    ]
    couple_rec = make_experiment_record(coupling_scan(
        coupling_entries, threshold=10.0,
        factor_a_label="visibility_fraction", factor_b_label="tide_height_m",
        output_label="bottle_count", coupling_label="demo_couple"))
    records.append(couple_rec)

    event = make_audit_event(
        subject_record_ids=[r.record_id for r in records],
        event_kind="experiment_batch_recorded",
        description="Four instrument-level experiments were run on synthetic "
                    "data and recorded without interpretation.",
        evidence=[
            f"null_baseline: {null_rec.payload['recorded_summary']['max_candidate_regions']} "
            "max candidate region(s) over 25 noise replications",
            f"sweep: {len(sweep_rec.payload['region_appearances'])} distinct region(s) "
            "across 5 thresholds",
            f"permutation: {len(permute_rec.payload['region_appearances'])} distinct "
            "region(s) across 26 scans",
            f"coupling: {len(couple_rec.payload['coincidence_record']['coincident_pairs'])} "
            "coincident pair(s) across two factors",
        ],
        unresolved_questions=[
            "Do candidate-region counts on real data differ from the null record?",
            "Which regions persist across thresholds, and does persistence matter here?",
            "Does scan order affect regions on real, unordered case sets?",
            "Do coincident regions across factors indicate a confound?",
        ],
        proposed_next_tests=[
            "repeat each procedure on held-out synthetic generators",
            "run the same procedures on a documented real dataset",
        ],
    )
    records.append(event)
    return records


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


def emit_records(records, out, extra=None):
    if out:
        write_jsonl(out, records)
    for record in records:
        print(record.to_json())
    if extra is not None:
        print(json.dumps(extra, indent=2))


def main():
    parser = argparse.ArgumentParser(prog="scope-audit-lab")
    sub = parser.add_subparsers(dest="command", required=True)
    demo = sub.add_parser("demo", help="write synthetic demonstration records")
    demo.add_argument("--out", default="demo_output.jsonl")
    tdemo = sub.add_parser("transitions-demo",
                           help="write a synthetic transition-scan demonstration")
    tdemo.add_argument("--out", default="transitions_demo.jsonl")
    scan_p = sub.add_parser("transitions",
                            help="scan a cases JSON file for candidate transition regions")
    scan_p.add_argument("cases", help="JSON file: list of {case_id, factor, output, notes?}")
    scan_p.add_argument("--threshold", type=float, required=True)
    scan_p.add_argument("--kind", default="absolute", choices=("absolute", "relative"))
    scan_p.add_argument("--factor-label", default="factor")
    scan_p.add_argument("--output-label", default="output")
    scan_p.add_argument("--label", default=None)
    scan_p.add_argument("--out", default=None, help="append scan record to this JSONL stream")

    xdemo = sub.add_parser("experiments-demo",
                           help="write synthetic demonstrations of all v0.3 experiments")
    xdemo.add_argument("--out", default="experiments_demo.jsonl")
    null_p = sub.add_parser("null-scan",
                            help="record candidate regions on seeded synthetic noise")
    null_p.add_argument("--n-cases", type=int, default=12)
    null_p.add_argument("--replications", type=int, default=25)
    null_p.add_argument("--threshold", type=float, required=True)
    null_p.add_argument("--seed", type=int, required=True)
    null_p.add_argument("--distribution", default="uniform",
                        choices=("uniform", "normal"))
    null_p.add_argument("--kind", default="absolute", choices=("absolute", "relative"))
    null_p.add_argument("--label", default=None)
    null_p.add_argument("--out", default=None)
    sweep_p = sub.add_parser("sweep",
                             help="scan a cases JSON file across several thresholds")
    sweep_p.add_argument("cases", help="JSON file: list of {case_id, factor, output, notes?}")
    sweep_p.add_argument("--thresholds", type=float, nargs="+", required=True)
    sweep_p.add_argument("--kind", default="absolute", choices=("absolute", "relative"))
    sweep_p.add_argument("--factor-label", default="factor")
    sweep_p.add_argument("--output-label", default="output")
    sweep_p.add_argument("--label", default=None)
    sweep_p.add_argument("--out", default=None)
    perm_p = sub.add_parser("permute",
                            help="scan a cases JSON file in given and permuted orders")
    perm_p.add_argument("cases", help="JSON file: list of {case_id, factor, output, notes?}")
    perm_p.add_argument("--permutations", type=int, default=25)
    perm_p.add_argument("--threshold", type=float, required=True)
    perm_p.add_argument("--seed", type=int, required=True)
    perm_p.add_argument("--kind", default="absolute", choices=("absolute", "relative"))
    perm_p.add_argument("--factor-label", default="factor")
    perm_p.add_argument("--output-label", default="output")
    perm_p.add_argument("--label", default=None)
    perm_p.add_argument("--out", default=None)
    coup_p = sub.add_parser("couple",
                            help="scan a two-factor cases JSON file against each factor")
    coup_p.add_argument("cases", help="JSON file: list of {case_id, factor_a, factor_b, output, notes?}")
    coup_p.add_argument("--threshold", type=float, required=True)
    coup_p.add_argument("--kind", default="absolute", choices=("absolute", "relative"))
    coup_p.add_argument("--factor-a-label", default="factor_a")
    coup_p.add_argument("--factor-b-label", default="factor_b")
    coup_p.add_argument("--output-label", default="output")
    coup_p.add_argument("--label", default=None)
    coup_p.add_argument("--out", default=None)

    validate = sub.add_parser("validate", help="structurally validate a JSONL event stream")
    validate.add_argument("path")
    args = parser.parse_args()

    if args.command == "transitions-demo":
        path = Path(args.out)
        records = build_transitions_demo_records()
        count = write_jsonl(str(path), records)
        print(json.dumps({"output": str(path), "records_appended": count,
                          "candidate_regions":
                              len(records[0].payload["candidate_regions"]),
                          "data_status": "synthetic demonstration only",
                          "interpretation": "no boundary or model verdict assigned"},
                         indent=2))
        return
    if args.command == "transitions":
        cases = load_cases(args.cases, args.factor_label, args.output_label)
        record = make_transition_scan(cases=cases, threshold=args.threshold,
                                      threshold_kind=args.kind, scan_label=args.label)
        emit_records([record], args.out)
        return
    if args.command == "experiments-demo":
        path = Path(args.out)
        records = build_experiments_demo_records()
        count = write_jsonl(str(path), records)
        print(json.dumps({"output": str(path), "records_appended": count,
                          "experiment_kinds": [r.payload.get("experiment_kind")
                                               for r in records
                                               if r.record_type == "experiment"],
                          "data_status": "synthetic demonstration only",
                          "interpretation": "no boundary or model verdict assigned"},
                         indent=2))
        return
    if args.command == "null-scan":
        record = make_experiment_record(null_baseline_scan(
            n_cases=args.n_cases, n_replications=args.replications,
            threshold=args.threshold, seed=args.seed,
            distribution=args.distribution, threshold_kind=args.kind,
            label=args.label))
        emit_records([record], args.out)
        return
    if args.command == "sweep":
        cases = load_cases(args.cases, args.factor_label, args.output_label)
        record = make_experiment_record(threshold_sweep(
            cases, thresholds=args.thresholds, threshold_kind=args.kind,
            sweep_label=args.label))
        emit_records([record], args.out)
        return
    if args.command == "permute":
        cases = load_cases(args.cases, args.factor_label, args.output_label)
        record = make_experiment_record(order_permutation_probe(
            cases, n_permutations=args.permutations, threshold=args.threshold,
            seed=args.seed, threshold_kind=args.kind, probe_label=args.label))
        emit_records([record], args.out)
        return
    if args.command == "couple":
        with open(args.cases, "r", encoding="utf-8") as stream:
            entries = json.load(stream)
        if not isinstance(entries, list):
            raise SystemExit("cases file must contain a JSON list")
        record = make_experiment_record(coupling_scan(
            entries, threshold=args.threshold,
            factor_a_label=args.factor_a_label,
            factor_b_label=args.factor_b_label,
            output_label=args.output_label, threshold_kind=args.kind,
            coupling_label=args.label))
        emit_records([record], args.out)
        return
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
