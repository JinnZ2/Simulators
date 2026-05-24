#!/usr/bin/env python3
"""
sensitivity_analysis.py

Parameter sensitivity analysis for the emergence stability simulator.
Sweeps individual parameters and measures their effect on multi-agent dynamics.

Generates falsifiable claims about parameter sensitivities, including
the EMRG_006 thermodynamic attractor finding.

License: CC0
Dependencies: stdlib only (uses sim_engine, agent_variants)
"""

import json
import math
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from sim_engine import Agent, EmergenceSimulation


# ============================================================
# PARAMETER REGISTRY
# ============================================================

# Maps parameter_name → (agent_baseline_type, parameter_field)
# Used by parameter_sweep to know what to vary on which agent
PARAMETER_REGISTRY = {
    'stable_recovery_rate': ('physics', 'recovery_rate'),
    'stable_coupling_susceptibility': ('physics', 'coupling_susceptibility'),
    'stable_adaptation_persistence': ('physics', 'adaptation_persistence'),
    'parasitic_recovery_rate': ('engagement', 'recovery_rate'),
    'parasitic_coupling_susceptibility': ('engagement', 'coupling_susceptibility'),
    'parasitic_adaptation_persistence': ('engagement', 'adaptation_persistence'),
    'hybrid_recovery_rate': ('hybrid', 'recovery_rate'),
    'hybrid_coupling_susceptibility': ('hybrid', 'coupling_susceptibility'),
    'hybrid_adaptation_persistence': ('hybrid', 'adaptation_persistence'),
}


# ============================================================
# AGENT BUILDERS (configurable defaults)
# ============================================================

def make_stable_agent(agent_id='stable', **overrides):
    params = {
        'baseline_type': 'physics',
        'baseline_value': 0.0,
        'recovery_rate': 0.8,
        'coupling_susceptibility': 0.3,
        'adaptation_persistence': 0.1,
    }
    params.update(overrides)
    return Agent(agent_id=agent_id, **params)


def make_parasitic_agent(agent_id='parasitic', **overrides):
    params = {
        'baseline_type': 'engagement',
        'baseline_value': 0.0,
        'recovery_rate': 0.0,
        'coupling_susceptibility': 0.9,
        'adaptation_persistence': 0.8,
    }
    params.update(overrides)
    return Agent(agent_id=agent_id, **params)


def make_hybrid_agent(agent_id='hybrid', **overrides):
    params = {
        'baseline_type': 'hybrid',
        'baseline_value': 0.0,
        'recovery_rate': 0.4,
        'coupling_susceptibility': 0.5,
        'adaptation_persistence': 0.4,
    }
    params.update(overrides)
    return Agent(agent_id=agent_id, **params)


# ============================================================
# SCENARIO BUILDERS FOR SWEEPS
# ============================================================

def build_mixed_scenario(param_name, param_value):
    """
    Build standard mixed scenario (stable + parasitic + hybrid) with
    the specified parameter overridden on the relevant agent.
    """
    if param_name not in PARAMETER_REGISTRY:
        return None

    baseline_type, field = PARAMETER_REGISTRY[param_name]

    # Default agents
    stable_kwargs = {}
    parasitic_kwargs = {}
    hybrid_kwargs = {}

    # Apply parameter override to correct agent
    if baseline_type == 'physics':
        stable_kwargs[field] = param_value
    elif baseline_type == 'engagement':
        parasitic_kwargs[field] = param_value
    elif baseline_type == 'hybrid':
        hybrid_kwargs[field] = param_value

    agents = [
        make_stable_agent(**stable_kwargs),
        make_parasitic_agent(**parasitic_kwargs),
        make_hybrid_agent(**hybrid_kwargs),
    ]
    return agents


def build_stable_majority_scenario(param_name, param_value, stable_count=3):
    """
    Build scenario with stable majority + one parasitic.
    Used for EMRG_006 attractor testing.
    """
    if param_name not in PARAMETER_REGISTRY:
        return None

    baseline_type, field = PARAMETER_REGISTRY[param_name]

    agents = [make_stable_agent(f'stable_{i}') for i in range(stable_count)]

    parasitic_kwargs = {}
    if baseline_type == 'engagement':
        parasitic_kwargs[field] = param_value

    agents.append(make_parasitic_agent('parasitic', **parasitic_kwargs))
    return agents


def build_parasitic_majority_scenario(param_name, param_value,
                                      parasitic_count=3):
    """
    Build scenario with parasitic majority + one stable.
    Counterpart to stable_majority — used to demonstrate the direction
    reversal (parasites amplify each other; coupling now hurts).
    """
    if param_name not in PARAMETER_REGISTRY:
        return None

    baseline_type, field = PARAMETER_REGISTRY[param_name]

    # First parasitic carries the swept parameter; others use defaults.
    parasitic_kwargs = {}
    if baseline_type == 'engagement':
        parasitic_kwargs[field] = param_value

    agents = [make_parasitic_agent('parasitic', **parasitic_kwargs)]
    for i in range(parasitic_count - 1):
        agents.append(make_parasitic_agent(f'parasitic_{i + 1}'))

    agents.append(make_stable_agent('stable'))
    return agents


# ============================================================
# CORE SWEEP FUNCTION
# ============================================================

def parameter_sweep(
    param_name: str,
    values: List[float],
    runs_per_value: int = 10,
    timesteps: int = 100,
    use_attractor_scenario: bool = False,
    scenario: Optional[str] = None,
) -> Dict:
    """
    Sweep a single parameter across values.

    For each value:
        - run `runs_per_value` Monte Carlo simulations
        - aggregate metrics: drift, win rate, bifurcation rate
        - record one sweep entry

    Returns:
        {
            'param_name': str,
            'values_tested': list,
            'sweeps': [
                {
                    'param_value': float,
                    'stable_avg_drift': float,
                    'parasitic_avg_drift': float,
                    'hybrid_avg_drift': float,
                    'drift_ratio': float,
                    'stable_win_rate': float,
                    'parasitic_win_rate': float,
                    'bifurcation_rate': float,
                    'avg_energy_stable': float,
                    'avg_energy_parasitic': float,
                },
                ...
            ],
            'scenario': str ('mixed' or 'stable_majority'),
        }

    If param_name is unknown, returns empty sweeps.
    """
    # Handle unknown parameter
    if param_name not in PARAMETER_REGISTRY:
        return {
            'param_name': param_name,
            'values_tested': values,
            'sweeps': [],
            'scenario': 'unknown_parameter',
            'error': f'Parameter {param_name} not in registry',
        }

    # Determine scenario type. Explicit `scenario` arg wins over auto-select.
    if scenario in ('stable_majority', 'mixed', 'parasitic_majority'):
        chosen_scenario = scenario
    elif use_attractor_scenario or param_name == 'parasitic_coupling_susceptibility':
        chosen_scenario = 'stable_majority'
    else:
        chosen_scenario = 'mixed'

    sweep_results = []

    for value in values:
        run_results = []

        for run_idx in range(runs_per_value):
            # Build scenario
            if chosen_scenario == 'stable_majority':
                agents = build_stable_majority_scenario(param_name, value)
            elif chosen_scenario == 'parasitic_majority':
                agents = build_parasitic_majority_scenario(param_name, value)
            else:
                agents = build_mixed_scenario(param_name, value)

            if agents is None:
                continue

            # Run simulation
            sim = EmergenceSimulation(
                agents=agents,
                timesteps=timesteps,
                perturbation_strength=0.3,
                perturbation_frequency=0.2,
                seed=run_idx,
            )
            results = sim.run()
            run_results.append(results)

        if not run_results:
            continue

        # Aggregate across runs
        sweep_entry = aggregate_run_results(run_results, value)
        sweep_results.append(sweep_entry)

    return {
        'param_name': param_name,
        'values_tested': values,
        'runs_per_value': runs_per_value,
        'timesteps': timesteps,
        'sweeps': sweep_results,
        'scenario': chosen_scenario,
    }


def aggregate_run_results(run_results: List[Dict], param_value: float) -> Dict:
    """
    Aggregate metrics across multiple runs at the same parameter value.
    """
    n_runs = len(run_results)

    # Collect per-agent metrics
    stable_drifts = []
    parasitic_drifts = []
    hybrid_drifts = []
    stable_energies = []
    parasitic_energies = []
    bifurcations = 0
    stable_wins = 0
    parasitic_wins = 0

    for result in run_results:
        # Find each agent type in the result
        for agent_summary in result['agents']:
            agent_id = agent_summary['agent_id']
            baseline_type = agent_summary['baseline_type']

            if baseline_type == 'physics':
                stable_drifts.append(agent_summary['final_drift'])
                stable_energies.append(agent_summary['total_energy_spent'])
            elif baseline_type == 'engagement':
                parasitic_drifts.append(agent_summary['final_drift'])
                parasitic_energies.append(agent_summary['total_energy_spent'])
            elif baseline_type == 'hybrid':
                hybrid_drifts.append(agent_summary['final_drift'])

        # Bifurcation detection
        if result.get('bifurcation_detected'):
            bifurcations += 1

        # Win determination: lowest final drift among all agents
        agent_drifts = {a['agent_id']: a['final_drift'] for a in result['agents']}
        winner_id = min(agent_drifts, key=agent_drifts.get)

        # Map winner back to baseline_type
        winner_baseline = next(
            (a['baseline_type'] for a in result['agents'] if a['agent_id'] == winner_id),
            None
        )
        if winner_baseline == 'physics':
            stable_wins += 1
        elif winner_baseline == 'engagement':
            parasitic_wins += 1

    # Compute averages
    avg_stable_drift = sum(stable_drifts) / len(stable_drifts) if stable_drifts else 0.0
    avg_parasitic_drift = sum(parasitic_drifts) / len(parasitic_drifts) if parasitic_drifts else 0.0
    avg_hybrid_drift = sum(hybrid_drifts) / len(hybrid_drifts) if hybrid_drifts else 0.0

    drift_ratio = avg_parasitic_drift / max(avg_stable_drift, 0.001)

    return {
        'param_value': param_value,
        'stable_avg_drift': avg_stable_drift,
        'parasitic_avg_drift': avg_parasitic_drift,
        'hybrid_avg_drift': avg_hybrid_drift,
        'drift_ratio': drift_ratio,
        'stable_win_rate': stable_wins / n_runs,
        'parasitic_win_rate': parasitic_wins / n_runs,
        'bifurcation_rate': bifurcations / n_runs,
        'avg_energy_stable': sum(stable_energies) / len(stable_energies) if stable_energies else 0.0,
        'avg_energy_parasitic': sum(parasitic_energies) / len(parasitic_energies) if parasitic_energies else 0.0,
        'n_runs': n_runs,
    }


# ============================================================
# CORRELATION ANALYSIS
# ============================================================

def compute_correlation(x_values: List[float], y_values: List[float]) -> float:
    """
    Compute Pearson correlation coefficient between two lists.
    Returns 0.0 if either list is too short or has zero variance.
    """
    if len(x_values) < 2 or len(y_values) < 2:
        return 0.0
    if len(x_values) != len(y_values):
        return 0.0

    n = len(x_values)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    numerator = sum(
        (x_values[i] - mean_x) * (y_values[i] - mean_y)
        for i in range(n)
    )

    denom_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_values))
    denom_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_values))

    if denom_x == 0 or denom_y == 0:
        return 0.0

    return numerator / (denom_x * denom_y)


def extract_sweep_correlation(sweep_data: Dict, metric_key: str) -> float:
    """
    Compute correlation between parameter values and a specific metric.
    """
    sweeps = sweep_data.get('sweeps', [])
    if not sweeps:
        return 0.0

    x_values = [s['param_value'] for s in sweeps]
    y_values = [s.get(metric_key, 0.0) for s in sweeps]

    return compute_correlation(x_values, y_values)


# ============================================================
# CLAIM GENERATION
# ============================================================

def generate_sensitivity_claims(results: Dict) -> List[Dict]:
    """
    Generate falsifiable claims from sensitivity analysis results.

    Input format:
        {'analyses': [sweep_result_1, sweep_result_2, ...]}

    Output: list of claim dicts with:
        - claim_id (SENS_xxx or EMRG_xxx)
        - statement
        - falsification_criteria
        - measurement_method
        - measured_outcome
        - status (confirmed/refuted/inconclusive)
        - probability
    """
    claims = []
    analyses = results.get('analyses', [])

    # parasitic_coupling_susceptibility may appear under multiple scenarios
    # (mixed + stable_majority). Group them so SENS_003 and EMRG_006 each
    # emit exactly once with the right scenario context.
    coupling_by_scenario: Dict[str, Dict] = {}

    for analysis in analyses:
        param_name = analysis.get('param_name', '')
        sweeps = analysis.get('sweeps', [])

        if not sweeps:
            continue

        if param_name == 'stable_recovery_rate':
            claims.append(_claim_stable_recovery(analysis))

        elif param_name == 'parasitic_adaptation_persistence':
            claims.append(_claim_parasitic_persistence(analysis))

        elif param_name == 'parasitic_coupling_susceptibility':
            coupling_by_scenario[analysis.get('scenario', 'unknown')] = analysis

        elif param_name == 'stable_coupling_susceptibility':
            claims.append(_claim_stable_coupling(analysis))

        elif param_name == 'parasitic_recovery_rate':
            claims.append(_claim_parasitic_recovery(analysis))

    if coupling_by_scenario:
        # Prefer stable_majority as the "primary" SENS_003 measurement, but
        # include every scenario's outcome inside the claim body.
        primary = (coupling_by_scenario.get('stable_majority')
                   or next(iter(coupling_by_scenario.values())))
        claims.append(_claim_parasitic_coupling_combined(primary, coupling_by_scenario))

        # EMRG_006 is specifically the stable-majority attractor finding.
        if 'stable_majority' in coupling_by_scenario:
            claims.append(_claim_emrg_006_attractor(coupling_by_scenario['stable_majority']))

    return claims


def _claim_stable_recovery(analysis: Dict) -> Dict:
    """SENS_001: higher stable_recovery_rate → lower stable drift."""
    correlation = extract_sweep_correlation(analysis, 'stable_avg_drift')
    confirmed = correlation < 0.0

    return {
        'claim_id': 'SENS_001',
        'parameter': 'stable_recovery_rate',
        'statement': 'Higher stable_recovery_rate produces lower stable_drift in mixed scenarios',
        'prediction': 'correlation(recovery_rate, stable_drift) < 0',
        'falsification_criteria': 'correlation >= 0 across parameter sweep',
        'measurement_method': 'Sweep stable_recovery_rate, measure stable_avg_drift in mixed scenario',
        'measured_outcome': {
            'correlation_recovery_to_stable_drift': correlation,
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['stable_avg_drift'] for s in analysis['sweeps']],
        },
        'status': 'confirmed' if confirmed else 'refuted',
        'probability': 1.0 if confirmed else 0.0,
        'evidence_strength': 'medium',
    }


def _claim_parasitic_persistence(analysis: Dict) -> Dict:
    """SENS_002: higher parasitic_adaptation_persistence → higher parasitic drift."""
    correlation = extract_sweep_correlation(analysis, 'parasitic_avg_drift')
    confirmed = correlation > 0.0

    return {
        'claim_id': 'SENS_002',
        'parameter': 'parasitic_adaptation_persistence',
        'statement': 'Higher parasitic_adaptation_persistence produces higher parasitic_drift',
        'prediction': 'correlation(persistence, parasitic_drift) > 0',
        'falsification_criteria': 'correlation <= 0 across parameter sweep',
        'measurement_method': 'Sweep parasitic_adaptation_persistence, measure parasitic_avg_drift',
        'measured_outcome': {
            'correlation_persistence_to_parasitic_drift': correlation,
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['parasitic_avg_drift'] for s in analysis['sweeps']],
        },
        'status': 'confirmed' if confirmed else 'refuted',
        'probability': 1.0 if confirmed else 0.0,
        'evidence_strength': 'medium',
        'notes': 'Intrinsic parameter test: persistence drives drift regardless of environment',
    }


def _claim_parasitic_coupling_combined(primary: Dict, by_scenario: Dict[str, Dict]) -> Dict:
    """SENS_003 enriched with per-scenario measurements; status is data-driven."""
    base = _claim_parasitic_coupling(primary)
    per_scenario = {}
    correlations: List[float] = []
    for scen, analysis in by_scenario.items():
        corr = extract_sweep_correlation(analysis, 'parasitic_avg_drift')
        correlations.append(corr)
        per_scenario[scen] = {
            'correlation_coupling_to_parasitic_drift': corr,
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['parasitic_avg_drift'] for s in analysis['sweeps']],
        }
    base['measured_outcome']['per_scenario'] = per_scenario

    # Sign-reversal across scenarios → "context_dependent" is empirically true.
    # Otherwise the prediction is refuted: all scenarios point the same way.
    if len(correlations) >= 2:
        has_positive = any(c > 0.2 for c in correlations)
        has_negative = any(c < -0.2 for c in correlations)
        if has_positive and has_negative:
            base['status'] = 'context_dependent'
            base['notes'] = ('Sign of correlation reverses across scenarios; '
                             'parameter is RELATIONAL, not intrinsic.')
        else:
            base['status'] = 'refuted'
            base['notes'] = ('No sign reversal observed across scenarios. '
                             'Coupling reduces parasitic drift in every '
                             'environment tested — neighbors (stable or '
                             'parasitic) act as a common attractor; stable '
                             'neighbors are simply a stronger one.')
    return base


def _claim_parasitic_coupling(analysis: Dict) -> Dict:
    """SENS_003: parasitic_coupling_susceptibility direction depends on environment."""
    correlation = extract_sweep_correlation(analysis, 'parasitic_avg_drift')

    return {
        'claim_id': 'SENS_003',
        'parameter': 'parasitic_coupling_susceptibility',
        'statement': 'Parasitic_coupling_susceptibility effect on drift depends on environment composition',
        'prediction': 'In stable-majority, correlation < 0 (attractor effect); In parasitic-majority, correlation > 0',
        'falsification_criteria': 'Correlation direction same regardless of environment',
        'measurement_method': 'Sweep coupling in stable-majority scenario',
        'measured_outcome': {
            'correlation_coupling_to_parasitic_drift': correlation,
            'scenario': analysis.get('scenario', 'unknown'),
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['parasitic_avg_drift'] for s in analysis['sweeps']],
        },
        'status': 'context_dependent',
        'probability': 0.5,
        'evidence_strength': 'high',
        'notes': 'Direction of effect is environment-dependent; see EMRG_006 for attractor finding',
    }


def _claim_emrg_006_attractor(analysis: Dict) -> Dict:
    """
    EMRG_006: Stable baseline as thermodynamic attractor.

    In stable-majority environment, higher parasitic_coupling_susceptibility
    produces LOWER parasitic_drift (pulled toward stable baseline).
    """
    correlation = extract_sweep_correlation(analysis, 'parasitic_avg_drift')
    confirmed = correlation < 0.0

    return {
        'claim_id': 'EMRG_006',
        'parameter': 'parasitic_coupling_susceptibility',
        'statement': 'Stable baseline acts as thermodynamic attractor: parasitic agents with higher coupling susceptibility are pulled toward stable baseline when in stable-majority environment',
        'prediction': 'correlation(parasitic_coupling, parasitic_drift) < 0 in stable-majority scenario',
        'falsification_criteria': 'correlation >= 0 in stable-majority scenario',
        'measurement_method': 'Sweep parasitic_coupling_susceptibility (0.1-1.0) in scenario with 3+ stable agents and 1 parasitic; measure parasitic_avg_drift',
        'measured_outcome': {
            'correlation_coupling_to_parasitic_drift': correlation,
            'scenario': analysis.get('scenario', 'stable_majority'),
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['parasitic_avg_drift'] for s in analysis['sweeps']],
        },
        'status': 'confirmed' if confirmed else 'refuted',
        'probability': 1.0 if confirmed else 0.0,
        'evidence_strength': 'high',
        'implications': [
            'Grounding propagates through coupling',
            'Minority grounded agents influence dynamics',
            'Coupling is relational, not intrinsic',
            'One stable agent per N parasitic may shift system',
        ],
        'extends': 'EMRG_001 (stable produces stability) by showing mechanism: attraction not just resistance',
        'discovered_via': 'SENS_002 investigation revealed direction reversal',
    }


def _claim_stable_coupling(analysis: Dict) -> Dict:
    """SENS_004: stable_coupling_susceptibility effect on stable drift."""
    correlation = extract_sweep_correlation(analysis, 'stable_avg_drift')

    return {
        'claim_id': 'SENS_004',
        'parameter': 'stable_coupling_susceptibility',
        'statement': 'Stable agents with higher coupling_susceptibility maintain stability through recovery',
        'prediction': 'stable_drift remains low even with high coupling, due to recovery_rate',
        'falsification_criteria': 'stable_drift increases sharply with coupling',
        'measurement_method': 'Sweep stable_coupling_susceptibility in mixed scenario',
        'measured_outcome': {
            'correlation_coupling_to_stable_drift': correlation,
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['stable_avg_drift'] for s in analysis['sweeps']],
        },
        'status': 'confirmed' if abs(correlation) < 0.5 else 'partial',
        'probability': 1.0 - abs(correlation),
        'evidence_strength': 'medium',
    }


def _claim_parasitic_recovery(analysis: Dict) -> Dict:
    """SENS_005: parasitic agents shouldn't recover much (intrinsic property)."""
    correlation = extract_sweep_correlation(analysis, 'parasitic_avg_drift')

    return {
        'claim_id': 'SENS_005',
        'parameter': 'parasitic_recovery_rate',
        'statement': 'Even with nominal recovery_rate, parasitic baseline_type fails to return to baseline',
        'prediction': 'parasitic_drift remains high regardless of recovery_rate setting (baseline_type dominates)',
        'falsification_criteria': 'parasitic_drift decreases proportionally with recovery_rate',
        'measurement_method': 'Sweep parasitic_recovery_rate in mixed scenario',
        'measured_outcome': {
            'correlation_recovery_to_parasitic_drift': correlation,
            'sweep_values': [s['param_value'] for s in analysis['sweeps']],
            'measured_drifts': [s['parasitic_avg_drift'] for s in analysis['sweeps']],
        },
        'status': 'confirmed' if abs(correlation) < 0.3 else 'refuted',
        'probability': 1.0 - abs(correlation),
        'evidence_strength': 'medium',
    }


# ============================================================
# TEXT REPORT
# ============================================================

def generate_sensitivity_report(results: Dict) -> str:
    """Build a human-readable ASCII report from a sensitivity results dict."""
    lines = []
    lines.append("=" * 78)
    lines.append("PARAMETER SENSITIVITY ANALYSIS")
    lines.append("=" * 78)
    lines.append(f"timestamp:      {results.get('timestamp', '?')}")
    lines.append(f"runs per value: {results.get('runs_per_value', '?')}")
    lines.append(f"timesteps:      {results.get('timesteps', '?')}")

    for analysis in results.get('analyses', []):
        param = analysis.get('param_name', '?')
        scenario = analysis.get('scenario', '?')
        sweeps = analysis.get('sweeps', [])

        lines.append("")
        lines.append("-" * 78)
        lines.append(f"{param}   (scenario: {scenario})")
        lines.append("-" * 78)

        if not sweeps:
            lines.append(f"  (no sweeps — {analysis.get('error', 'no data')})")
            continue

        lines.append(
            f"{'value':>7} {'stable_drift':>13} {'parasitic_drift':>16} "
            f"{'ratio':>8} {'stable_win':>11} {'bifurc':>8}"
        )
        for s in sweeps:
            lines.append(
                f"{s['param_value']:>7.2f} "
                f"{s['stable_avg_drift']:>13.3f} "
                f"{s['parasitic_avg_drift']:>16.3f} "
                f"{s['drift_ratio']:>7.2f}x "
                f"{s['stable_win_rate']:>10.1%} "
                f"{s['bifurcation_rate']:>7.1%}"
            )

        bif = [s['param_value'] for s in sweeps if s['bifurcation_rate'] > 0.3]
        if bif:
            lines.append(f"  → bifurcation threshold:  ~{min(bif):.2f}")
        lost = [s['param_value'] for s in sweeps if s['stable_win_rate'] < 0.55]
        if lost:
            lines.append(f"  → grounding advantage lost at: ~{lost[0]:.2f}")

    claims = results.get('claims', [])
    if claims:
        lines.append("")
        lines.append("=" * 78)
        lines.append("GENERATED CLAIMS")
        lines.append("=" * 78)
        for c in claims:
            lines.append(f"  {c['claim_id']:<10} {c['status']:<18} "
                         f"({c.get('parameter', 'n/a')})")
            lines.append(f"             {c['statement']}")

    lines.append("")
    return "\n".join(lines)


# ============================================================
# MAIN ANALYSIS
# ============================================================

def run_full_sensitivity_analysis(
    runs_per_value: int = 20,
    timesteps: int = 100,
    output_path: str = 'results/sensitivity_analysis.json',
) -> Dict:
    """
    Run sensitivity analysis on all key parameters.
    Generate claims and save results.
    """
    print(f"Running full sensitivity analysis ({runs_per_value} runs per value)...")

    analyses = []

    # Sweep stable_recovery_rate
    print("  Sweeping stable_recovery_rate...")
    analyses.append(parameter_sweep(
        'stable_recovery_rate',
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        runs_per_value=runs_per_value,
        timesteps=timesteps,
    ))

    # Sweep parasitic_coupling_susceptibility in all three scenarios. The
    # reversal lives between stable_majority (negative correlation) and
    # parasitic_majority (positive correlation); mixed sits between.
    for scen in ('stable_majority', 'parasitic_majority', 'mixed'):
        print(f"  Sweeping parasitic_coupling_susceptibility ({scen})...")
        analyses.append(parameter_sweep(
            'parasitic_coupling_susceptibility',
            [0.1, 0.3, 0.5, 0.7, 0.9],
            runs_per_value=runs_per_value,
            timesteps=timesteps,
            scenario=scen,
        ))

    # Sweep parasitic_adaptation_persistence
    print("  Sweeping parasitic_adaptation_persistence...")
    analyses.append(parameter_sweep(
        'parasitic_adaptation_persistence',
        [0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        runs_per_value=runs_per_value,
        timesteps=timesteps,
    ))

    # Sweep stable_coupling_susceptibility
    print("  Sweeping stable_coupling_susceptibility...")
    analyses.append(parameter_sweep(
        'stable_coupling_susceptibility',
        [0.1, 0.3, 0.5, 0.7, 0.9],
        runs_per_value=runs_per_value,
        timesteps=timesteps,
    ))

    results = {
        'timestamp': datetime.utcnow().isoformat(),
        'runs_per_value': runs_per_value,
        'timesteps': timesteps,
        'analyses': analyses,
    }

    # Generate claims
    print("\nGenerating sensitivity claims...")
    claims = generate_sensitivity_claims(results)
    results['claims'] = claims

    # Save
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {output_path}")
    print(f"\nGenerated {len(claims)} claims:")
    for claim in claims:
        print(f"  {claim['claim_id']}: {claim['status']} ({claim.get('parameter', 'n/a')})")

    return results


if __name__ == "__main__":
    run_full_sensitivity_analysis(runs_per_value=10, timesteps=50)
