#!/usr/bin/env python3
"""
sensitivity_viz.py

ASCII visualization for sensitivity_analysis sweep results.
Stdlib only. Generates plots, comparison tables, correlation indicators.

License: CC0
Dependencies: stdlib only (uses sensitivity_analysis output)
"""

import json
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================
# CORE PLOTTING PRIMITIVES
# ============================================================

def ascii_line_plot(
    x_values: List[float],
    y_values: List[float],
    height: int = 12,
    width: int = 60,
    x_label: str = "x",
    y_label: str = "y",
    title: str = "",
) -> str:
    """
    ASCII line plot showing y as function of x.
    Used for parameter sweeps.
    """
    if not x_values or not y_values:
        return "(no data)"
    if len(x_values) != len(y_values):
        return "(length mismatch)"

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    x_range = x_max - x_min if x_max != x_min else 1.0
    y_range = y_max - y_min if y_max != y_min else 1.0

    # Create grid
    grid = [[' '] * width for _ in range(height)]

    # Plot points and connect with lines
    plotted_points = []
    for i in range(len(x_values)):
        gx = int(((x_values[i] - x_min) / x_range) * (width - 1))
        gy = int(((y_values[i] - y_min) / y_range) * (height - 1))
        gy = height - 1 - gy  # invert
        plotted_points.append((gx, gy))

    # Draw connecting lines (simple interpolation)
    for i in range(len(plotted_points) - 1):
        x1, y1 = plotted_points[i]
        x2, y2 = plotted_points[i + 1]
        steps = max(abs(x2 - x1), abs(y2 - y1))
        if steps == 0:
            continue
        for s in range(steps + 1):
            ix = int(x1 + (x2 - x1) * s / steps)
            iy = int(y1 + (y2 - y1) * s / steps)
            if 0 <= ix < width and 0 <= iy < height:
                if grid[iy][ix] == ' ':
                    grid[iy][ix] = '·'

    # Mark actual data points more prominently
    for gx, gy in plotted_points:
        if 0 <= gx < width and 0 <= gy < height:
            grid[gy][gx] = '●'

    # Build output
    lines = []
    if title:
        lines.append(title)
        lines.append("─" * width)

    # Y axis labels and grid
    for i, row in enumerate(grid):
        y_val = y_max - (i / max(height - 1, 1)) * y_range
        lines.append(f"  {y_val:7.3f} │ {''.join(row)}")

    # X axis
    lines.append(f"          └{'─' * width}")

    # X axis labels (start, mid, end)
    x_axis_line = "           "
    x_axis_line += f"{x_min:.2f}"
    middle_padding = width // 2 - len(f"{x_min:.2f}")
    x_axis_line += " " * max(middle_padding, 1)
    x_mid = (x_min + x_max) / 2
    x_axis_line += f"{x_mid:.2f}"
    end_padding = width // 2 - len(f"{x_mid:.2f}")
    x_axis_line += " " * max(end_padding, 1)
    x_axis_line += f"{x_max:.2f}"
    lines.append(x_axis_line)

    # Axis label
    lines.append(f"\n           {x_label}")

    return "\n".join(lines)


def ascii_dual_line_plot(
    x_values: List[float],
    y_series: Dict[str, List[float]],
    height: int = 12,
    width: int = 60,
    title: str = "",
    x_label: str = "x",
) -> str:
    """
    ASCII plot showing multiple y-series on same axes.
    Each series gets a different character.

    y_series: dict of label → list of values
    """
    if not x_values or not y_series:
        return "(no data)"

    # Collect all y values to determine range
    all_y = []
    for values in y_series.values():
        all_y.extend(values)

    if not all_y:
        return "(no data)"

    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(all_y), max(all_y)
    x_range = x_max - x_min if x_max != x_min else 1.0
    y_range = y_max - y_min if y_max != y_min else 1.0

    # Markers for each series
    markers = ['●', '○', '◆', '◇', '▲', '△']
    series_markers = {}

    grid = [[' '] * width for _ in range(height)]

    for series_idx, (label, y_values) in enumerate(y_series.items()):
        marker = markers[series_idx % len(markers)]
        series_markers[label] = marker

        if len(y_values) != len(x_values):
            continue

        # Plot points
        plotted_points = []
        for i in range(len(x_values)):
            gx = int(((x_values[i] - x_min) / x_range) * (width - 1))
            gy = int(((y_values[i] - y_min) / y_range) * (height - 1))
            gy = height - 1 - gy
            plotted_points.append((gx, gy))

        # Draw lines
        line_char = '·' if series_idx == 0 else '∙'
        for i in range(len(plotted_points) - 1):
            x1, y1 = plotted_points[i]
            x2, y2 = plotted_points[i + 1]
            steps = max(abs(x2 - x1), abs(y2 - y1))
            if steps == 0:
                continue
            for s in range(steps + 1):
                ix = int(x1 + (x2 - x1) * s / steps)
                iy = int(y1 + (y2 - y1) * s / steps)
                if 0 <= ix < width and 0 <= iy < height:
                    if grid[iy][ix] == ' ':
                        grid[iy][ix] = line_char

        # Mark data points
        for gx, gy in plotted_points:
            if 0 <= gx < width and 0 <= gy < height:
                grid[gy][gx] = marker

    # Build output
    lines = []
    if title:
        lines.append(title)
        lines.append("─" * width)

    # Legend
    legend_parts = [f"{marker} {label}" for label, marker in series_markers.items()]
    lines.append("Legend: " + "  ".join(legend_parts))
    lines.append("")

    # Y axis and grid
    for i, row in enumerate(grid):
        y_val = y_max - (i / max(height - 1, 1)) * y_range
        lines.append(f"  {y_val:7.3f} │ {''.join(row)}")

    # X axis
    lines.append(f"          └{'─' * width}")
    x_axis_line = f"           {x_min:.2f}"
    middle_padding = width // 2 - len(f"{x_min:.2f}")
    x_axis_line += " " * max(middle_padding, 1)
    x_mid = (x_min + x_max) / 2
    x_axis_line += f"{x_mid:.2f}"
    end_padding = width // 2 - len(f"{x_mid:.2f}")
    x_axis_line += " " * max(end_padding, 1)
    x_axis_line += f"{x_max:.2f}"
    lines.append(x_axis_line)
    lines.append(f"\n           {x_label}")

    return "\n".join(lines)


def ascii_correlation_bar(correlation: float, width: int = 40) -> str:
    """
    Show correlation as bidirectional bar.

    -1.0 ←─────●────→ +1.0
    """
    correlation = max(-1.0, min(1.0, correlation))
    center = width // 2

    # Position on bar
    if correlation >= 0:
        pos = center + int(correlation * center)
    else:
        pos = center + int(correlation * center)

    # Build bar
    bar = list('─' * width)
    bar[center] = '│'  # zero marker

    if 0 <= pos < width:
        bar[pos] = '●'

    bar_str = ''.join(bar)

    # Label
    label = f"-1.0 {bar_str} +1.0"

    # Interpretation
    if abs(correlation) < 0.2:
        strength = "negligible"
    elif abs(correlation) < 0.4:
        strength = "weak"
    elif abs(correlation) < 0.7:
        strength = "moderate"
    else:
        strength = "strong"

    direction = "positive" if correlation > 0 else "negative" if correlation < 0 else "zero"

    return f"{label}\n  correlation: {correlation:+.3f} ({strength} {direction})"


def ascii_table(
    headers: List[str],
    rows: List[List[str]],
    title: str = "",
) -> str:
    """ASCII table for sweep result comparison."""
    if not rows:
        return "(no data)"

    # Compute column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))

    # Add padding
    col_widths = [w + 2 for w in col_widths]

    # Build table
    lines = []
    if title:
        lines.append(title)
        lines.append("=" * sum(col_widths))

    # Header row
    header_line = "│"
    for i, h in enumerate(headers):
        header_line += f" {h:^{col_widths[i]-2}} │"
    lines.append(header_line)

    # Separator
    sep_line = "├"
    for w in col_widths:
        sep_line += "─" * w + "┼"
    sep_line = sep_line[:-1] + "┤"
    lines.append(sep_line)

    # Data rows
    for row in rows:
        data_line = "│"
        for i, cell in enumerate(row):
            if i < len(col_widths):
                data_line += f" {str(cell):^{col_widths[i]-2}} │"
        lines.append(data_line)

    return "\n".join(lines)


# ============================================================
# SWEEP-SPECIFIC VISUALIZATIONS
# ============================================================

def visualize_sweep(analysis: Dict, height: int = 10, width: int = 60) -> str:
    """
    Visualize a single parameter sweep showing all relevant metrics.
    """
    param_name = analysis.get('param_name', 'unknown')
    sweeps = analysis.get('sweeps', [])
    scenario = analysis.get('scenario', 'unknown')

    if not sweeps:
        return f"No sweep data for {param_name}"

    x_values = [s['param_value'] for s in sweeps]
    stable_drifts = [s.get('stable_avg_drift', 0.0) for s in sweeps]
    parasitic_drifts = [s.get('parasitic_avg_drift', 0.0) for s in sweeps]

    output = []
    output.append("=" * 70)
    output.append(f"PARAMETER SWEEP: {param_name}")
    output.append(f"Scenario: {scenario}")
    output.append(f"Values tested: {x_values}")
    output.append(f"Runs per value: {analysis.get('runs_per_value', '?')}")
    output.append("=" * 70)

    # Dual-series plot: stable vs parasitic drift
    output.append("\nDRIFT vs PARAMETER VALUE")
    output.append(ascii_dual_line_plot(
        x_values=x_values,
        y_series={
            'stable_drift': stable_drifts,
            'parasitic_drift': parasitic_drifts,
        },
        height=height,
        width=width,
        title="",
        x_label=param_name,
    ))

    # Correlation analysis
    output.append("\n" + "=" * 70)
    output.append("CORRELATION ANALYSIS")
    output.append("=" * 70)

    # Compute correlations
    stable_corr = _correlation(x_values, stable_drifts)
    parasitic_corr = _correlation(x_values, parasitic_drifts)

    output.append(f"\nStable drift correlation with {param_name}:")
    output.append(ascii_correlation_bar(stable_corr))

    output.append(f"\nParasitic drift correlation with {param_name}:")
    output.append(ascii_correlation_bar(parasitic_corr))

    # Direction detection
    output.append("\n" + "=" * 70)
    output.append("DIRECTION ANALYSIS")
    output.append("=" * 70)

    output.append(_direction_interpretation(param_name, stable_corr, parasitic_corr, scenario))

    # Sweep table
    output.append("\n" + "=" * 70)
    output.append("SWEEP TABLE")
    output.append("=" * 70)

    headers = ['param', 'stable_drift', 'parasitic_drift', 'drift_ratio', 'win_rate', 'bifurc_rate']
    rows = []
    for s in sweeps:
        rows.append([
            f"{s['param_value']:.2f}",
            f"{s['stable_avg_drift']:.3f}",
            f"{s['parasitic_avg_drift']:.3f}",
            f"{s['drift_ratio']:.2f}x",
            f"{s['stable_win_rate']*100:.0f}%",
            f"{s['bifurcation_rate']*100:.0f}%",
        ])
    output.append(ascii_table(headers, rows))

    return "\n".join(output)


def _correlation(x_values: List[float], y_values: List[float]) -> float:
    """Pearson correlation, stdlib only."""
    import math
    if len(x_values) < 2 or len(y_values) < 2:
        return 0.0
    n = len(x_values)
    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n
    num = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
    denom_x = math.sqrt(sum((x - mean_x) ** 2 for x in x_values))
    denom_y = math.sqrt(sum((y - mean_y) ** 2 for y in y_values))
    if denom_x == 0 or denom_y == 0:
        return 0.0
    return num / (denom_x * denom_y)


def _direction_interpretation(
    param_name: str,
    stable_corr: float,
    parasitic_corr: float,
    scenario: str,
) -> str:
    """Plain-language interpretation of correlation directions."""
    output = []

    # Stable agent
    if abs(stable_corr) < 0.2:
        output.append(f"  Stable drift: largely independent of {param_name} ({stable_corr:+.3f})")
    elif stable_corr > 0:
        output.append(f"  Stable drift INCREASES with {param_name} ({stable_corr:+.3f})")
    else:
        output.append(f"  Stable drift DECREASES with {param_name} ({stable_corr:+.3f})")

    # Parasitic agent
    if abs(parasitic_corr) < 0.2:
        output.append(f"  Parasitic drift: largely independent of {param_name} ({parasitic_corr:+.3f})")
    elif parasitic_corr > 0:
        output.append(f"  Parasitic drift INCREASES with {param_name} ({parasitic_corr:+.3f})")
    else:
        output.append(f"  Parasitic drift DECREASES with {param_name} ({parasitic_corr:+.3f})")

    # Special interpretations
    if 'parasitic_coupling' in param_name and parasitic_corr < -0.3:
        output.append("")
        output.append("  >>> ATTRACTOR EFFECT DETECTED (EMRG_006) <<<")
        output.append("  Higher coupling pulls parasite TOWARD stable baseline.")
        output.append("  Confirms: stable baseline acts as thermodynamic attractor.")
    elif 'parasitic_persistence' in param_name and parasitic_corr > 0.3:
        output.append("")
        output.append("  >>> INTRINSIC DRIFT CONFIRMED (SENS_002) <<<")
        output.append("  Higher persistence amplifies drift regardless of environment.")
    elif 'stable_recovery' in param_name and stable_corr < -0.3:
        output.append("")
        output.append("  >>> RECOVERY MECHANISM CONFIRMED (SENS_001) <<<")
        output.append("  Higher recovery rate reduces stable drift, as expected.")

    return "\n".join(output)


# ============================================================
# DIRECTION REVERSAL DETECTION
# ============================================================

def detect_direction_reversal(
    analysis_a: Dict,
    analysis_b: Dict,
    metric: str = 'parasitic_avg_drift',
) -> Dict:
    """
    Compare two analyses of same parameter in different scenarios.
    Detect whether direction of effect reverses.
    """
    sweeps_a = analysis_a.get('sweeps', [])
    sweeps_b = analysis_b.get('sweeps', [])

    if not sweeps_a or not sweeps_b:
        return {'reversal_detected': False, 'reason': 'insufficient data'}

    x_a = [s['param_value'] for s in sweeps_a]
    y_a = [s.get(metric, 0.0) for s in sweeps_a]
    x_b = [s['param_value'] for s in sweeps_b]
    y_b = [s.get(metric, 0.0) for s in sweeps_b]

    corr_a = _correlation(x_a, y_a)
    corr_b = _correlation(x_b, y_b)

    # Reversal: correlations have opposite signs AND both are non-trivial
    sign_reversal = (corr_a > 0.2 and corr_b < -0.2) or (corr_a < -0.2 and corr_b > 0.2)

    return {
        'reversal_detected': sign_reversal,
        'scenario_a': analysis_a.get('scenario', 'unknown'),
        'scenario_b': analysis_b.get('scenario', 'unknown'),
        'correlation_a': corr_a,
        'correlation_b': corr_b,
        'parameter': analysis_a.get('param_name', '?'),
        'metric': metric,
    }


def visualize_reversal(reversal: Dict) -> str:
    """Visualize direction reversal finding."""
    if not reversal.get('reversal_detected'):
        return f"No direction reversal detected for {reversal.get('parameter', '?')}"

    output = []
    output.append("=" * 70)
    output.append("DIRECTION REVERSAL DETECTED")
    output.append("=" * 70)
    output.append(f"Parameter: {reversal['parameter']}")
    output.append(f"Metric: {reversal['metric']}")
    output.append("")
    output.append(f"Scenario A: {reversal['scenario_a']}")
    output.append(f"  Correlation: {reversal['correlation_a']:+.3f}")
    output.append(ascii_correlation_bar(reversal['correlation_a']))
    output.append("")
    output.append(f"Scenario B: {reversal['scenario_b']}")
    output.append(f"  Correlation: {reversal['correlation_b']:+.3f}")
    output.append(ascii_correlation_bar(reversal['correlation_b']))
    output.append("")
    output.append("INTERPRETATION:")
    output.append("  Effect direction depends on environment composition.")
    output.append("  This is emergent behavior, not a measurement error.")
    output.append("  Indicates that parameter is RELATIONAL, not INTRINSIC.")

    return "\n".join(output)


# ============================================================
# CLAIM VISUALIZATION
# ============================================================

def visualize_claim(claim: Dict) -> str:
    """ASCII display of a single claim's status and evidence."""
    output = []
    output.append("─" * 70)
    output.append(f"[{claim['claim_id']}] {claim.get('parameter', 'unknown')}")
    output.append("─" * 70)
    output.append(f"Statement: {claim['statement']}")
    output.append(f"Prediction: {claim['prediction']}")
    output.append(f"Falsification: {claim['falsification_criteria']}")

    # Status indicator
    status = claim.get('status', 'unknown')
    if status == 'confirmed':
        status_marker = "✓ CONFIRMED"
    elif status == 'refuted':
        status_marker = "✗ REFUTED"
    elif status == 'context_dependent':
        status_marker = "◐ CONTEXT-DEPENDENT"
    else:
        status_marker = "? " + status.upper()

    output.append(f"\nStatus: {status_marker}")
    output.append(f"Probability: {claim.get('probability', 0.0):.2f}")
    output.append(f"Evidence strength: {claim.get('evidence_strength', 'unknown')}")

    # Show correlation if present
    outcome = claim.get('measured_outcome', {})
    for key, value in outcome.items():
        if 'correlation' in key and isinstance(value, (int, float)):
            output.append(f"\n{key}:")
            output.append(ascii_correlation_bar(value))

    # Show implications if present
    implications = claim.get('implications', [])
    if implications:
        output.append("\nImplications:")
        for imp in implications:
            output.append(f"  • {imp}")

    # Notes
    if claim.get('notes'):
        output.append(f"\nNotes: {claim['notes']}")

    return "\n".join(output)


def visualize_all_claims(claims: List[Dict]) -> str:
    """Display all generated claims with status summary at top."""
    output = []
    output.append("=" * 70)
    output.append("SENSITIVITY ANALYSIS CLAIMS SUMMARY")
    output.append("=" * 70)

    # Status summary
    statuses = {}
    for claim in claims:
        status = claim.get('status', 'unknown')
        statuses[status] = statuses.get(status, 0) + 1

    output.append("\nStatus Distribution:")
    for status, count in statuses.items():
        bar = '█' * count
        output.append(f"  {status:20} {bar} {count}")

    output.append(f"\nTotal claims: {len(claims)}")

    # Individual claims
    output.append("\n")
    for claim in claims:
        output.append(visualize_claim(claim))
        output.append("")

    return "\n".join(output)


# ============================================================
# FULL REPORT GENERATION
# ============================================================

def generate_full_report(
    results_path: str = 'results/sensitivity_analysis.json',
    output_path: str = 'results/sensitivity_report.txt',
) -> str:
    """Generate complete ASCII report from sensitivity analysis results."""
    results_file = Path(results_path)
    if not results_file.exists():
        return f"Results file not found: {results_path}"

    with open(results_file, 'r') as f:
        data = json.load(f)

    analyses = data.get('analyses', [])
    claims = data.get('claims', [])

    output = []
    output.append("=" * 70)
    output.append("SENSITIVITY ANALYSIS - FULL REPORT")
    output.append("=" * 70)
    output.append(f"Generated: {data.get('timestamp', '?')}")
    output.append(f"Runs per value: {data.get('runs_per_value', '?')}")
    output.append(f"Timesteps: {data.get('timesteps', '?')}")
    output.append(f"Parameters analyzed: {len(analyses)}")
    output.append("")

    # Per-parameter analysis
    output.append("=" * 70)
    output.append("INDIVIDUAL PARAMETER SWEEPS")
    output.append("=" * 70)

    for analysis in analyses:
        output.append("\n")
        output.append(visualize_sweep(analysis))

    # Claims summary
    output.append("\n\n")
    output.append(visualize_all_claims(claims))

    # Check for direction reversals
    output.append("\n\n")
    output.append("=" * 70)
    output.append("CROSS-SCENARIO ANALYSIS")
    output.append("=" * 70)

    # Look for parasitic_coupling in different scenarios
    parasitic_coupling_analyses = [
        a for a in analyses
        if a.get('param_name') == 'parasitic_coupling_susceptibility'
    ]
    if len(parasitic_coupling_analyses) >= 2:
        for i in range(len(parasitic_coupling_analyses)):
            for j in range(i + 1, len(parasitic_coupling_analyses)):
                reversal = detect_direction_reversal(
                    parasitic_coupling_analyses[i],
                    parasitic_coupling_analyses[j],
                )
                if reversal['reversal_detected']:
                    output.append("\n")
                    output.append(visualize_reversal(reversal))

    # Conclusions
    output.append("\n\n")
    output.append("=" * 70)
    output.append("KEY FINDINGS")
    output.append("=" * 70)

    confirmed_count = sum(1 for c in claims if c.get('status') == 'confirmed')
    refuted_count = sum(1 for c in claims if c.get('status') == 'refuted')
    context_dep_count = sum(1 for c in claims if c.get('status') == 'context_dependent')

    output.append(f"  Confirmed claims:        {confirmed_count}")
    output.append(f"  Refuted claims:          {refuted_count}")
    output.append(f"  Context-dependent:       {context_dep_count}")

    # Specifically highlight EMRG_006
    emrg_006 = next((c for c in claims if c['claim_id'] == 'EMRG_006'), None)
    if emrg_006:
        output.append("")
        output.append("THERMODYNAMIC ATTRACTOR FINDING (EMRG_006):")
        if emrg_006.get('status') == 'confirmed':
            corr = emrg_006.get('measured_outcome', {}).get(
                'correlation_coupling_to_parasitic_drift', 0.0
            )
            output.append(f"  ✓ CONFIRMED with correlation {corr:+.3f}")
            output.append("  ✓ Stable baseline acts as thermodynamic attractor")
            output.append("  ✓ Grounding propagates through coupling")
        else:
            output.append(f"  Status: {emrg_006.get('status')}")

    output.append("\n" + "=" * 70)
    output.append("End of report")
    output.append("=" * 70)

    report = "\n".join(output)

    # Save to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(report)

    print(f"Report saved to {output_path}")
    return report


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import sys

    # If called with a specific results file
    if len(sys.argv) > 1:
        results_path = sys.argv[1]
    else:
        results_path = 'results/sensitivity_analysis.json'

    report = generate_full_report(results_path=results_path)
    print(report)
