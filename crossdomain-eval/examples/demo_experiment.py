"""Demo: parameter sweep, sensitivity analysis, DOE plan, and a report.

Run: python examples/demo_experiment.py
Outputs are written to a temporary directory (printed at the end).
"""

from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np

from crossdomain_eval.experiments import parameter_sweep, propose_experiments
from crossdomain_eval.report import markdown_report, plot_sweep


def objective(temp: float, pressure: float) -> float:
    """Two-variable test function: peak near temp=3, mild pressure effect."""
    return float(np.exp(-((temp - 3.0) ** 2) / 4.0) * (1.0 + 0.1 * np.sin(pressure)))


def main() -> None:
    """Run the demo experiment workflow."""
    outdir = tempfile.mkdtemp(prefix="cdeval_demo_")

    sweep = parameter_sweep(
        objective, {"temp": (0.0, 6.0, 41), "pressure": (0.0, 4.0, 21)}
    )
    sens = sweep.sensitivity()
    best = sweep.best(maximize=True)
    print("sensitivity:", sens)
    print("best config:", best)

    plan = propose_experiments("maximize objective", ["temp", "pressure", "speed"], levels=3)
    print(f"DOE plan: {len(plan)} runs, first run: {plan[0]}")

    fig = plot_sweep(sweep, "temp", f"{outdir}/sweep.png")
    report = markdown_report(
        "Demo Experiment Report",
        [
            {
                "heading": "Sweep",
                "text": f"Best objective {best['value']:.4f} at temp={best['temp']:.2f}, "
                        f"pressure={best['pressure']:.2f}.",
                "figure": fig,
                "table": {"parameter": list(sens), "sensitivity": [f"{v:.3f}" for v in sens.values()]},
            },
            {
                "heading": "DOE Plan",
                "text": f"Full factorial with {len(plan)} runs at 3 coded levels.",
                "figure": None,
                "table": {"run": [r["run"] for r in plan],
                          "temp": [r["temp"] for r in plan],
                          "pressure": [r["pressure"] for r in plan],
                          "speed": [r["speed"] for r in plan]},
            },
        ],
        f"{outdir}/report.md",
    )
    print(f"\nOutputs written to {outdir} (report.md, sweep.png)")
    print("--- report preview ---")
    print("\n".join(report.splitlines()[:12]))


if __name__ == "__main__":
    main()
