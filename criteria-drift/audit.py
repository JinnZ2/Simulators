#!/usr/bin/env python3
"""
audit.py — CLI for the Criteria Drift Auditor.

Commands:
  init              Create a new drift database
  ingest-criteria   Add a criteria version from JSON
  ingest-score      Add a model score
  drift             Compute drift history for an artifact
  regress           Run improvement-vs-drift regression
  report            Export full audit report to JSON
  list              Show artifacts and versions in DB

Usage:
  python audit.py init
  python audit.py ingest-criteria example_data/mmlu_v1.json
  python audit.py drift MMLU
  python audit.py regress MMLU --model "GPT-4" --score-type delta
"""
import argparse
import json
import sys
from pathlib import Path

from schema import CriteriaVersion, ModelScore, Frame
from store import DriftStore
from drift import DriftEngine, DriftMetrics
from regress import DriftRegressor


def cmd_init(args):
    store = DriftStore(args.db)
    print(f"Initialized database: {args.db}")
    store.close()


def cmd_ingest_criteria(args):
    with open(args.file) as f:
        data = json.load(f)
    cv = CriteriaVersion.from_dict(data)
    problems = cv.frame.validate()
    if problems:
        print("Frame validation issues:")
        for p in problems:
            print(f"  {p}")
        if args.strict:
            sys.exit(1)
    with DriftStore(args.db) as store:
        store.insert_criteria(cv)
    print(f"Ingested {cv.artifact_name} {cv.version_id}")


def cmd_ingest_score(args):
    with open(args.file) as f:
        data = json.load(f)
    ms = ModelScore.from_dict(data)
    with DriftStore(args.db) as store:
        store.insert_score(ms)
    print(f"Ingested score: {ms.model_name} on {ms.criteria_artifact} {ms.criteria_version}")


def cmd_drift(args):
    with DriftStore(args.db) as store:
        versions = store.get_criteria_history(args.artifact)
    if len(versions) < 2:
        print(f"Need >=2 versions for {args.artifact}, found {len(versions)}")
        sys.exit(1)
    engine = DriftEngine()
    metrics = engine.compute_history(versions)
    out = metrics.to_dict()
    if args.output:
        with open(args.output, "w") as f:
            json.dump(out, f, indent=2)
        print(f"Drift metrics written to {args.output}")
    else:
        print(json.dumps(out, indent=2))


def cmd_regress(args):
    with DriftStore(args.db) as store:
        versions = store.get_criteria_history(args.artifact)
        matrix = store.get_score_matrix(args.artifact)
    if len(versions) < 2:
        print(f"Need >=2 versions for {args.artifact}")
        sys.exit(1)
    engine = DriftEngine()
    drift_metrics = engine.compute_history(versions)
    regressor = DriftRegressor(matrix, drift_metrics)

    if args.model:
        result = regressor.regress(args.model, lag=args.lag, score_type=args.score_type)
        print(json.dumps(result.to_dict(), indent=2))
    else:
        results = regressor.regress_all_models(lag=args.lag, score_type=args.score_type)
        out = {k: v.to_dict() for k, v in results.items()}
        if args.output:
            with open(args.output, "w") as f:
                json.dump(out, f, indent=2)
            print(f"Regression results written to {args.output}")
        else:
            print(json.dumps(out, indent=2))


def cmd_report(args):
    with DriftStore(args.db) as store:
        artifacts = store.get_all_artifacts()
    full_report = {"artifacts": []}
    for art in artifacts:
        with DriftStore(args.db) as store:
            versions = store.get_criteria_history(art)
            matrix = store.get_score_matrix(art)
        engine = DriftEngine()
        drift_metrics = engine.compute_history(versions)
        regressor = DriftRegressor(matrix, drift_metrics)
        regressions = regressor.regress_all_models(score_type="delta")
        full_report["artifacts"].append({
            "name": art,
            "version_count": len(versions),
            "drift": drift_metrics.to_dict(),
            "regressions": {k: v.to_dict() for k, v in regressions.items()},
        })
    if args.output:
        with open(args.output, "w") as f:
            json.dump(full_report, f, indent=2)
        print(f"Full report written to {args.output}")
    else:
        print(json.dumps(full_report, indent=2))


def cmd_list(args):
    with DriftStore(args.db) as store:
        artifacts = store.get_all_artifacts()
    for art in artifacts:
        with DriftStore(args.db) as store:
            versions = store.get_criteria_history(art)
            scores = store.get_scores(art)
        print(f"\n{art}")
        print(f"  Versions: {len(versions)}")
        for v in versions:
            print(f"    {v.version_id} @ {v.timestamp}")
        print(f"  Scores: {len(scores)} records")
        models = set(s.model_name for s in scores)
        for m in sorted(models):
            count = sum(1 for s in scores if s.model_name == m)
            print(f"    {m}: {count} entries")


def main():
    parser = argparse.ArgumentParser(
        description="Criteria Drift Auditor — measure the ruler, not just the model.")
    parser.add_argument("--db", default="drift.db", help="SQLite database path")
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    sub.add_parser("init", help="Create a new drift database")

    # ingest-criteria
    p_ic = sub.add_parser("ingest-criteria", help="Add a criteria version from JSON")
    p_ic.add_argument("file", help="Path to JSON file")
    p_ic.add_argument("--strict", action="store_true", help="Fail on frame validation issues")

    # ingest-score
    p_is = sub.add_parser("ingest-score", help="Add a model score from JSON")
    p_is.add_argument("file", help="Path to JSON file")

    # drift
    p_d = sub.add_parser("drift", help="Compute drift history for an artifact")
    p_d.add_argument("artifact", help="Artifact name")
    p_d.add_argument("-o", "--output", help="Write JSON output to file")

    # regress
    p_r = sub.add_parser("regress", help="Run improvement-vs-drift regression")
    p_r.add_argument("artifact", help="Artifact name")
    p_r.add_argument("--model", help="Specific model name (default: all)")
    p_r.add_argument("--lag", type=int, default=0, help="Lag steps")
    p_r.add_argument("--score-type", default="delta", choices=["absolute", "delta", "relative"])
    p_r.add_argument("-o", "--output", help="Write JSON output to file")

    # report
    p_rep = sub.add_parser("report", help="Export full audit report")
    p_rep.add_argument("-o", "--output", help="Write JSON output to file")

    # list
    sub.add_parser("list", help="Show artifacts and versions")

    args = parser.parse_args()
    cmds = {
        "init": cmd_init,
        "ingest-criteria": cmd_ingest_criteria,
        "ingest-score": cmd_ingest_score,
        "drift": cmd_drift,
        "regress": cmd_regress,
        "report": cmd_report,
        "list": cmd_list,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
