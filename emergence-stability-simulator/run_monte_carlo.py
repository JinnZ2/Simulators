#!/usr/bin/env python3
"""
run_monte_carlo.py

Main entry point. Runs the full pipeline:
  1. Monte Carlo simulation (sim_engine.run_monte_carlo)
  2. Parameter sensitivity analysis (sensitivity_analysis)
  3. Merge sensitivity claims into CLAIM_TABLE.json
  4. Generate ASCII analysis report (analysis.generate_full_report)

CLI flags allow shrinking the workload for quick checks.

License: CC0
Dependencies: stdlib only
"""

import argparse
import json
from pathlib import Path

from sim_engine import run_monte_carlo, generate_claim_table
from sensitivity_analysis import (
    run_full_sensitivity_analysis,
    generate_sensitivity_report,
)
from analysis import generate_full_report


def merge_sensitivity_claims(claim_table_path: str, sens_claims: list) -> None:
    """Append SENS_* claims to CLAIM_TABLE.json (creates the file if missing)."""
    path = Path(claim_table_path)
    if path.exists():
        with open(path) as f:
            table = json.load(f)
    else:
        table = {'schema_version': '1.0', 'claims': []}

    existing_ids = {c['claim_id'] for c in table.get('claims', [])}
    for c in sens_claims:
        if c['claim_id'] not in existing_ids:
            table['claims'].append(c)
        else:
            # Update in place if re-run
            for i, existing in enumerate(table['claims']):
                if existing['claim_id'] == c['claim_id']:
                    table['claims'][i] = c
                    break

    with open(path, 'w') as f:
        json.dump(table, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Run emergence-stability-simulator end-to-end pipeline."
    )
    parser.add_argument('--runs', type=int, default=1000,
                        help='Monte Carlo runs (default 1000)')
    parser.add_argument('--timesteps', type=int, default=100,
                        help='Timesteps per run (default 100)')
    parser.add_argument('--sensitivity-runs', type=int, default=15,
                        help='Runs per parameter value in sensitivity sweep')
    parser.add_argument('--skip-sensitivity', action='store_true',
                        help='Skip parameter sensitivity analysis')
    parser.add_argument('--skip-report', action='store_true',
                        help='Skip ASCII analysis report generation')
    args = parser.parse_args()

    print("=" * 60)
    print("EMERGENCE-STABILITY-SIMULATOR — PIPELINE")
    print("=" * 60)

    # 1. Monte Carlo
    aggregate = run_monte_carlo(runs=args.runs, timesteps=args.timesteps)

    # 2. Falsifiable claims (writes CLAIM_TABLE.json)
    generate_claim_table(aggregate)

    # 3. Sensitivity analysis + merge sweep-derived claims + text report
    if not args.skip_sensitivity:
        sens_results = run_full_sensitivity_analysis(
            runs_per_value=args.sensitivity_runs,
            timesteps=args.timesteps,
        )
        sens_claims = sens_results.get('claims', [])
        merge_sensitivity_claims('CLAIM_TABLE.json', sens_claims)
        print(f"\nMerged {len(sens_claims)} sweep-derived claims into CLAIM_TABLE.json")

        report = generate_sensitivity_report(sens_results)
        Path('results').mkdir(exist_ok=True)
        with open('results/sensitivity_report.txt', 'w') as f:
            f.write(report)
        print("Sensitivity report at results/sensitivity_report.txt")

    # 4. ASCII report
    if not args.skip_report:
        generate_full_report()
        print("\nFull ASCII report at results/full_report.txt")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
