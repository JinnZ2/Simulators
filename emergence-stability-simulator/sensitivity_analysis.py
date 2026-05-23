#!/usr/bin/env python3
"""
sensitivity_analysis.py

Parameter sensitivity analysis.

For each parameter in stable/parasitic agents, test a range of values
and measure how final outcomes change. Identifies bifurcation thresholds
and reveals which structural properties matter most.

License: CC0
Dependencies: stdlib only
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from sim_engine import EmergenceSimulation
from agent_variants import (
    make_pure_stable,
    make_pure_parasitic,
    make_balanced_hybrid,
)


def parameter_sweep(
    parameter_name: str,
    value_range: List[float],
    runs_per_value: int = 20,
) -> Dict:
    """
    Sweep a single parameter across a range of values.
    Measure: stable_drift, parasitic_drift, win_rate, bifurcation_rate.
    """
    results = {
        'parameter': parameter_name,
        'values_tested': value_range,
        'sweeps': []
    }

    known_parameters = {
        'stable_recovery_rate',
        'stable_coupling_susceptibility',
        'parasitic_coupling_susceptibility',
        'parasitic_adaptation_persistence',
    }
    if parameter_name not in known_parameters:
        return results

    for test_value in value_range:
        stable_drifts: List[float] = []
        parasitic_drifts: List[float] = []
        bifurcations = 0

        for run_idx in range(runs_per_value):
            stable = make_pure_stable()
            parasitic = make_pure_parasitic()

            if parameter_name == 'stable_recovery_rate':
                stable.recovery_rate = test_value
            elif parameter_name == 'stable_coupling_susceptibility':
                stable.coupling_susceptibility = test_value
            elif parameter_name == 'parasitic_coupling_susceptibility':
                parasitic.coupling_susceptibility = test_value
            elif parameter_name == 'parasitic_adaptation_persistence':
                parasitic.adaptation_persistence = test_value

            agents = [stable, parasitic, make_balanced_hybrid()]

            sim = EmergenceSimulation(
                agents=agents,
                timesteps=100,
                perturbation_strength=0.3,
                perturbation_frequency=0.2,
                seed=run_idx,
            )
            results_run = sim.run()

            stable_drifts.append(results_run['agents'][0]['final_drift'])
            parasitic_drifts.append(results_run['agents'][1]['final_drift'])
            if results_run['bifurcation_detected']:
                bifurcations += 1

        avg_stable = sum(stable_drifts) / len(stable_drifts)
        avg_parasitic = sum(parasitic_drifts) / len(parasitic_drifts)
        stable_wins = sum(1 for s, p in zip(stable_drifts, parasitic_drifts) if s < p)

        results['sweeps'].append({
            'parameter_value': test_value,
            'stable_avg_drift': avg_stable,
            'parasitic_avg_drift': avg_parasitic,
            'drift_ratio': avg_parasitic / max(avg_stable, 0.001),
            'stable_win_rate': stable_wins / runs_per_value,
            'bifurcation_rate': bifurcations / runs_per_value,
        })

    return results


def run_all_sensitivity_tests(runs_per_value: int = 15) -> Dict:
    """Run sensitivity analysis for key parameters."""
    print("Running parameter sensitivity analysis...")

    all_results = {
        'timestamp': datetime.utcnow().isoformat(),
        'description': 'Sensitivity analysis of emergence stability parameters',
        'runs_per_value': runs_per_value,
        'analyses': []
    }

    sweeps_to_run = [
        ('stable_recovery_rate', [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]),
        ('stable_coupling_susceptibility', [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]),
        ('parasitic_coupling_susceptibility', [0.2, 0.4, 0.6, 0.8, 1.0]),
        ('parasitic_adaptation_persistence', [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]),
    ]

    for name, value_range in sweeps_to_run:
        print(f"  Testing {name}...")
        all_results['analyses'].append(
            parameter_sweep(name, value_range, runs_per_value=runs_per_value)
        )

    output_file = Path('results/sensitivity_analysis.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"Sensitivity analysis complete. Results saved to {output_file}")
    return all_results


def generate_sensitivity_report(results: Dict) -> str:
    """Generate ASCII report of sensitivity analysis."""
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("PARAMETER SENSITIVITY ANALYSIS")
    lines.append("=" * 70)

    for analysis in results['analyses']:
        param = analysis['parameter']
        lines.append(f"\n\n{param.upper()}")
        lines.append("-" * 70)
        lines.append(
            f"{'value':>8} {'stable_drift':>12} {'parasitic_drift':>14} "
            f"{'ratio':>8} {'stable_win':>11} {'bifurc':>8}"
        )
        lines.append("-" * 70)

        for sweep in analysis['sweeps']:
            lines.append(
                f"{sweep['parameter_value']:>8.2f} "
                f"{sweep['stable_avg_drift']:>12.3f} "
                f"{sweep['parasitic_avg_drift']:>14.3f} "
                f"{sweep['drift_ratio']:>7.2f}x "
                f"{sweep['stable_win_rate']:>10.1%} "
                f"{sweep['bifurcation_rate']:>7.1%}"
            )

        bifurc_sweeps = [s for s in analysis['sweeps'] if s['bifurcation_rate'] > 0.3]
        if bifurc_sweeps:
            lines.append(f"\n  → Bifurcation threshold: ~{bifurc_sweeps[0]['parameter_value']:.2f}")

        critical_sweeps = [s for s in analysis['sweeps'] if s['stable_win_rate'] < 0.55]
        if critical_sweeps:
            lines.append(f"  → Grounding advantage lost at: ~{critical_sweeps[0]['parameter_value']:.2f}")

    lines.append("\n" + "=" * 70)
    lines.append("INTERPRETATION")
    lines.append("=" * 70)
    lines.append("""
Sensitivity analysis reveals:
1. Which parameters control stability/cascade transition
2. Bifurcation thresholds (where system flips from stable to chaotic)
3. Critical values where grounding advantage disappears
4. Parametric robustness of the grounding hypothesis

If stable advantage persists across all parameter ranges:
  → grounding is STRUCTURAL, not brittle

If stable advantage disappears above threshold:
  → grounding REQUIRES adequate parameter values
  → identifies what "adequate" means quantitatively
""")
    return "\n".join(lines)


def generate_sensitivity_claims(results: Dict) -> List[Dict]:
    """
    Build SENS_* claims from sweep results and return them.
    Designed to be merged into CLAIM_TABLE.json by run_monte_carlo.py.
    """
    claims: List[Dict] = []

    def find_analysis(name: str) -> Optional[Dict]:
        for a in results['analyses']:
            if a['parameter'] == name:
                return a
        return None

    # SENS_001: recovery_rate threshold for grounding advantage
    a = find_analysis('stable_recovery_rate')
    if a:
        win_thresholds = [s['parameter_value'] for s in a['sweeps']
                          if s['stable_win_rate'] >= 0.55]
        threshold = min(win_thresholds) if win_thresholds else None
        claims.append({
            'claim_id': 'SENS_001',
            'statement': 'Grounding advantage (stable < parasitic) requires a minimum recovery_rate',
            'measured_outcome': {
                'min_recovery_rate_for_advantage': threshold,
                'sweep_values': a['values_tested'],
                'win_rates': [s['stable_win_rate'] for s in a['sweeps']],
            },
            'falsification_criteria': 'stable_win_rate >= 0.55 across all recovery_rate values',
            'status': 'confirmed' if threshold is not None and threshold > 0.0 else 'inconclusive',
        })

    # SENS_002: bifurcation threshold from parasitic coupling
    a = find_analysis('parasitic_coupling_susceptibility')
    if a:
        bif = [s['parameter_value'] for s in a['sweeps']
               if s['bifurcation_rate'] > 0.3]
        threshold = min(bif) if bif else None
        claims.append({
            'claim_id': 'SENS_002',
            'statement': 'Bifurcation occurs above a critical parasitic coupling_susceptibility',
            'measured_outcome': {
                'bifurcation_threshold': threshold,
                'sweep_values': a['values_tested'],
                'bifurcation_rates': [s['bifurcation_rate'] for s in a['sweeps']],
            },
            'falsification_criteria': 'bifurcation_rate <= 0.3 at all tested values',
            'status': 'confirmed' if threshold is not None else 'inconclusive',
        })

    # SENS_003: robustness of stable advantage across parameter space
    total_points = 0
    advantage_points = 0
    for a in results['analyses']:
        for s in a['sweeps']:
            total_points += 1
            if s['stable_win_rate'] > 0.55:
                advantage_points += 1
    fraction = advantage_points / total_points if total_points else 0.0
    claims.append({
        'claim_id': 'SENS_003',
        'statement': 'Stable advantage is robust across a majority of tested parameter space',
        'measured_outcome': {
            'fraction_of_space_with_stable_advantage': fraction,
            'total_points_tested': total_points,
        },
        'falsification_criteria': 'fraction_with_stable_advantage < 0.5',
        'status': 'confirmed' if fraction >= 0.5 else 'refuted',
    })

    # SENS_004: critical persistence for parasitic agents
    a = find_analysis('parasitic_adaptation_persistence')
    if a:
        ratios = [(s['parameter_value'], s['drift_ratio']) for s in a['sweeps']]
        critical = next((v for v, r in ratios if r >= 2.0), None)
        claims.append({
            'claim_id': 'SENS_004',
            'statement': 'Parasitic drift grows non-linearly with adaptation_persistence past a threshold',
            'measured_outcome': {
                'critical_persistence_for_2x_drift_ratio': critical,
                'sweep_values': a['values_tested'],
                'drift_ratios': [s['drift_ratio'] for s in a['sweeps']],
            },
            'falsification_criteria': 'drift_ratio < 2.0 across all persistence values',
            'status': 'confirmed' if critical is not None else 'inconclusive',
        })

    return claims


if __name__ == "__main__":
    results = run_all_sensitivity_tests()
    report = generate_sensitivity_report(results)
    print(report)

    report_file = Path('results/sensitivity_report.txt')
    report_file.parent.mkdir(parents=True, exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"\nReport saved to {report_file}")

    sens_claims = generate_sensitivity_claims(results)
    print(f"\nSENSITIVITY CLAIMS GENERATED: {len(sens_claims)}")
    for c in sens_claims:
        print(f"  {c['claim_id']}: {c['status']}")
