#!/usr/bin/env python3
"""
run_monte_carlo.py

Main entry point. Runs the full pipeline:
  1. Monte Carlo simulation (sim_engine.run_monte_carlo)
  2. Mode comparison for EMRG_007 / EMRG_008 (sim_engine.run_mode_comparison)
  3. Attractor quality test for EMRG_010 (sim_engine.run_attractor_quality_test)
  4. Generate falsifiable claims into CLAIM_TABLE.json
  5. Parameter sensitivity analysis + merge SENS_* claims
  6. Balance threshold analysis + merge EMRG_011/012/013/015 (balance_threshold)
  7. Generate ASCII analysis reports (analysis + sensitivity_viz)

CLI flags allow shrinking the workload for quick checks.

License: CC0
Dependencies: stdlib only
"""

import argparse
import json
from pathlib import Path

from sim_engine import (
    generate_claim_table,
    run_attractor_quality_test,
    run_mode_comparison,
    run_monte_carlo,
)
from sensitivity_analysis import run_full_sensitivity_analysis
from sensitivity_viz import generate_full_report as generate_sensitivity_viz_report
from analysis import generate_full_report
from balance_threshold import run_full_balance_analysis


def merge_claims_into_table(claim_table_path: str, new_claims: list) -> None:
    """
    Merge `new_claims` (a list of claim dicts) into CLAIM_TABLE.json.
    Existing claim_ids are updated in place; new ones are appended.
    Creates the file with the right headers if it does not exist.
    """
    path = Path(claim_table_path)
    if path.exists():
        with open(path) as f:
            table = json.load(f)
    else:
        table = {
            'schema_version': '1.0',
            'source_repo': 'emergence-stability-simulator',
            'claims': [],
        }
    table.setdefault('schema_version', '1.0')
    table.setdefault('source_repo', 'emergence-stability-simulator')

    by_id = {c['claim_id']: i for i, c in enumerate(table['claims'])}
    for c in new_claims:
        if c['claim_id'] in by_id:
            table['claims'][by_id[c['claim_id']]] = c
        else:
            table['claims'].append(c)

    with open(path, 'w') as f:
        json.dump(table, f, indent=2)


# Backwards-compatible alias retained because sensitivity tests / users
# may import this by its old name.
merge_sensitivity_claims = merge_claims_into_table


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
    parser.add_argument('--mode-runs', type=int, default=200,
                        help='Runs per scenario in mode comparison (EMRG_007/008)')
    parser.add_argument('--attractor-runs', type=int, default=80,
                        help='Runs per scenario in attractor quality test (EMRG_010)')
    parser.add_argument('--skip-sensitivity', action='store_true',
                        help='Skip parameter sensitivity analysis')
    parser.add_argument('--skip-mode-comparison', action='store_true',
                        help='Skip mode comparison (EMRG_007/008 stays proposed)')
    parser.add_argument('--skip-attractor-quality', action='store_true',
                        help='Skip attractor quality test (EMRG_010 stays proposed)')
    parser.add_argument('--balance-runs-per-cell', type=int, default=3,
                        help='Runs per cell in balance analysis (EMRG_011/012/013/015)')
    parser.add_argument('--skip-balance', action='store_true',
                        help='Skip balance threshold analysis')
    parser.add_argument('--skip-report', action='store_true',
                        help='Skip ASCII analysis report generation')
    args = parser.parse_args()

    print("=" * 60)
    print("EMERGENCE-STABILITY-SIMULATOR — PIPELINE")
    print("=" * 60)

    # 1. Monte Carlo
    aggregate = run_monte_carlo(runs=args.runs, timesteps=args.timesteps)

    # 2. Mode comparison (EMRG_007 / EMRG_008)
    mode_results = None
    if not args.skip_mode_comparison:
        mode_results = run_mode_comparison(
            runs=args.mode_runs,
            timesteps=args.timesteps,
        )

    # 3. Attractor quality test (EMRG_010)
    attractor_results = None
    if not args.skip_attractor_quality:
        attractor_results = run_attractor_quality_test(
            runs=args.attractor_runs,
            timesteps=args.timesteps,
        )

    # 4. Falsifiable claims (writes CLAIM_TABLE.json)
    generate_claim_table(
        aggregate,
        mode_results=mode_results,
        attractor_results=attractor_results,
    )

    # 5. Sensitivity analysis + merge sweep-derived claims + text report
    if not args.skip_sensitivity:
        sens_results = run_full_sensitivity_analysis(
            runs_per_value=args.sensitivity_runs,
            timesteps=args.timesteps,
        )
        sens_claims = sens_results.get('claims', [])
        merge_claims_into_table('CLAIM_TABLE.json', sens_claims)
        print(f"\nMerged {len(sens_claims)} sweep-derived claims into CLAIM_TABLE.json")

        # Rich visualization report (reads results/sensitivity_analysis.json
        # that run_full_sensitivity_analysis just wrote)
        generate_sensitivity_viz_report(
            results_path='results/sensitivity_analysis.json',
            output_path='results/sensitivity_report.txt',
        )

    # 6. Balance threshold analysis + merge EMRG_011/012/013/015
    if not args.skip_balance:
        balance_results = run_full_balance_analysis(
            output_path='results/balance_threshold.json',
            runs_per_cell=args.balance_runs_per_cell,
            timesteps=args.timesteps,
        )
        balance_claims = balance_results.get('claims', [])
        merge_claims_into_table('CLAIM_TABLE.json', balance_claims)
        print(f"\nMerged {len(balance_claims)} balance claims into CLAIM_TABLE.json")

    # 7. ASCII report
    if not args.skip_report:
        generate_full_report()
        print("\nFull ASCII report at results/full_report.txt")

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
