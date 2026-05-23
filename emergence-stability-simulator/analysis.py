#!/usr/bin/env python3
"""
analysis.py

ASCII plotting and statistical analysis of Monte Carlo results.

Reads results/monte_carlo_results.json (if present) for aggregate stats
and runs a single fresh simulation to produce trajectory visualizations.

Outputs:
- ASCII histogram of final drift per agent type
- ASCII line chart of agent position trajectories
- ASCII line chart of system entropy over time
- Summary statistics report
- Saves: results/full_report.txt

License: CC0
Dependencies: stdlib only
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Optional

from sim_engine import Agent, EmergenceSimulation


# ============================================================
# ASCII PLOT PRIMITIVES
# ============================================================

def ascii_histogram(values: List[float], bins: int = 20, width: int = 50,
                    title: str = "") -> str:
    """Horizontal ASCII histogram of a value distribution."""
    if not values:
        return "(no data)"

    lo, hi = min(values), max(values)
    if lo == hi:
        hi = lo + 1e-9

    counts = [0] * bins
    for v in values:
        idx = min(int((v - lo) / (hi - lo) * bins), bins - 1)
        counts[idx] += 1

    max_count = max(counts)
    if max_count == 0:
        return "(no data)"

    lines = []
    if title:
        lines.append(title)
        lines.append("-" * max(len(title), 20))

    for i, c in enumerate(counts):
        bin_lo = lo + (hi - lo) * i / bins
        bar = "#" * int(c / max_count * width)
        lines.append(f"{bin_lo:>8.3f} | {bar} {c}")

    return "\n".join(lines)


def ascii_line_chart(named_series: Dict[str, List[float]], width: int = 60,
                     height: int = 15, title: str = "") -> str:
    """Render multiple time series on shared ASCII axes."""
    if not named_series:
        return "(no data)"

    all_values: List[float] = []
    for vals in named_series.values():
        all_values.extend(vals)
    if not all_values:
        return "(no data)"

    y_min, y_max = min(all_values), max(all_values)
    if y_min == y_max:
        y_max = y_min + 1e-9

    n_points = max(len(v) for v in named_series.values())
    if n_points < 2:
        return "(insufficient data)"

    # Downsample x-axis to chart width
    sample_indices = [int(i * (n_points - 1) / (width - 1)) for i in range(width)]

    markers = ['*', 'o', '+', 'x', '.', '#']
    series_markers = {name: markers[i % len(markers)]
                      for i, name in enumerate(named_series)}

    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for name, vals in named_series.items():
        marker = series_markers[name]
        for col, src_idx in enumerate(sample_indices):
            if src_idx >= len(vals):
                continue
            v = vals[src_idx]
            row = int((y_max - v) / (y_max - y_min) * (height - 1))
            row = max(0, min(height - 1, row))
            if grid[row][col] == ' ':
                grid[row][col] = marker

    lines = []
    if title:
        lines.append(title)
        lines.append("-" * max(len(title), 20))

    for r, row in enumerate(grid):
        y_label = y_max - (y_max - y_min) * r / (height - 1)
        lines.append(f"{y_label:>8.3f} | {''.join(row)}")

    lines.append("         +" + "-" * width)
    end_label = f"t={n_points - 1}"
    lines.append("          t=0" + " " * (width - 3 - len(end_label)) + end_label)
    lines.append("")
    lines.append("Legend: " + ", ".join(f"{m}={name}"
                                        for name, m in series_markers.items()))
    return "\n".join(lines)


def ascii_scatter(x_values: List[float], y_values: List[float],
                  width: int = 60, height: int = 20, title: str = "",
                  x_label: str = "x", y_label: str = "y") -> str:
    """ASCII scatter plot."""
    if not x_values or not y_values:
        return "(no data)"

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    if x_min == x_max:
        x_max = x_min + 1e-9
    if y_min == y_max:
        y_max = y_min + 1e-9

    grid = [[' ' for _ in range(width)] for _ in range(height)]
    for x, y in zip(x_values, y_values):
        col = int((x - x_min) / (x_max - x_min) * (width - 1))
        row = int((y_max - y) / (y_max - y_min) * (height - 1))
        col = max(0, min(width - 1, col))
        row = max(0, min(height - 1, row))
        cell = grid[row][col]
        if cell == ' ':
            grid[row][col] = '.'
        elif cell == '.':
            grid[row][col] = ':'
        elif cell == ':':
            grid[row][col] = '*'
        else:
            grid[row][col] = '#'

    lines = []
    if title:
        lines.append(title)
        lines.append("-" * max(len(title), 20))

    for r, row in enumerate(grid):
        y_at = y_max - (y_max - y_min) * r / (height - 1)
        lines.append(f"{y_at:>8.3f} | {''.join(row)}")

    lines.append("         +" + "-" * width)
    lines.append(f"          {x_min:.3f}" + " " * (width - 16) + f"{x_max:.3f}")
    lines.append(f"          ({x_label}, density: . < : < *)")
    return "\n".join(lines)


# ============================================================
# STATISTICS
# ============================================================

def summarize(values: List[float]) -> Dict[str, float]:
    """Mean, stdev, min, max, median for a list of floats."""
    if not values:
        return {'n': 0, 'mean': 0, 'stdev': 0, 'min': 0, 'max': 0, 'median': 0}
    n = len(values)
    mean = sum(values) / n
    var = sum((v - mean) ** 2 for v in values) / n
    sorted_v = sorted(values)
    median = sorted_v[n // 2] if n % 2 else (sorted_v[n // 2 - 1] + sorted_v[n // 2]) / 2
    return {
        'n': n,
        'mean': mean,
        'stdev': math.sqrt(var),
        'min': min(values),
        'max': max(values),
        'median': median,
    }


# ============================================================
# REPORT BUILDERS
# ============================================================

def trajectory_section(timesteps: int = 100, seed: int = 42) -> str:
    """Run one simulation and render trajectory + entropy plots."""
    agents = [
        Agent('stable', 'physics', 0.0, 0.8, 0.3, 0.1),
        Agent('parasitic', 'engagement', 0.0, 0.0, 0.9, 0.8),
        Agent('mixed', 'hybrid', 0.0, 0.4, 0.5, 0.4),
    ]
    sim = EmergenceSimulation(agents, timesteps=timesteps,
                              perturbation_strength=0.3,
                              perturbation_frequency=0.2,
                              seed=seed)
    sim.run()

    trajectory_chart = ascii_line_chart(
        {a.agent_id: a.position_history for a in agents},
        width=70, height=15,
        title=f"Agent position trajectories (single run, seed={seed})",
    )
    entropy_chart = ascii_line_chart(
        {'system_entropy': sim.system_entropy_history,
         'coupling_strength': sim.coupling_strength_history},
        width=70, height=10,
        title="System entropy and coupling strength over time",
    )
    return trajectory_chart + "\n\n" + entropy_chart


def aggregate_section(results_path: str) -> str:
    """Load Monte Carlo aggregate file and render histograms + stats."""
    path = Path(results_path)
    if not path.exists():
        return f"(no aggregate results at {results_path} — run sim_engine.py first)"

    with open(path) as f:
        data = json.load(f)

    individual = data.get('individual_runs', [])
    aggregate = data.get('aggregate', {})

    # Collect per-agent drift distributions
    drifts_by_id: Dict[str, List[float]] = {}
    for run in individual:
        for agent in run['agents']:
            drifts_by_id.setdefault(agent['agent_id'], []).append(agent['final_drift'])

    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("AGGREGATE MONTE CARLO RESULTS")
    lines.append("=" * 70)
    lines.append(f"Total runs:      {aggregate.get('total_runs', len(individual))}")
    lines.append(f"Timesteps/run:   {aggregate.get('timesteps_per_run', '?')}")
    lines.append(f"Bifurcations:    {aggregate.get('bifurcations', '?')} "
                 f"({aggregate.get('bifurcation_rate', 0) * 100:.1f}%)")

    win_rates = aggregate.get('win_rates', {})
    if win_rates:
        lines.append("\nWin rates (lowest final drift):")
        for k, v in win_rates.items():
            lines.append(f"  {k:<12} {v * 100:5.1f}%")

    lines.append("\nPer-agent drift statistics:")
    for agent_id, drifts in drifts_by_id.items():
        s = summarize(drifts)
        lines.append(f"  {agent_id:<12} n={s['n']:>4} mean={s['mean']:.3f} "
                     f"stdev={s['stdev']:.3f} median={s['median']:.3f}")

    for agent_id, drifts in drifts_by_id.items():
        lines.append("\n" + ascii_histogram(
            drifts, bins=15, width=50,
            title=f"Final drift distribution: {agent_id}",
        ))

    # Phase diagram: system_entropy vs coupling_strength across runs
    entropies = [r['final_system_entropy'] for r in individual]
    couplings = [r['avg_coupling_strength'] for r in individual]
    if entropies and couplings:
        lines.append("\n" + ascii_scatter(
            couplings, entropies, width=60, height=15,
            title="Phase diagram: system entropy vs avg coupling strength",
            x_label="avg coupling strength",
        ))

    return "\n".join(lines)


def generate_full_report(results_path: str = "results/monte_carlo_results.json",
                         report_path: str = "results/full_report.txt") -> str:
    """Build the full ASCII report and write it to disk."""
    sections = []
    sections.append("=" * 70)
    sections.append("EMERGENCE-STABILITY-SIMULATOR — FULL ANALYSIS REPORT")
    sections.append("=" * 70)

    sections.append("\nTRAJECTORY VISUALIZATION (single representative run)")
    sections.append(trajectory_section())

    sections.append(aggregate_section(results_path))

    report = "\n".join(sections)

    out = Path(report_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, 'w') as f:
        f.write(report)

    return report


if __name__ == "__main__":
    report = generate_full_report()
    print(report)
    print(f"\nReport saved to results/full_report.txt")
