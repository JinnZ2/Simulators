#!/usr/bin/env python3
"""
phase_space_map.py

Scans the full parameter space of the coupled system.
Maps stability regions, phase transitions, and collapse basins.

Outputs a heatmap of collapse risk across two dimensions at a time.
"""

import numpy as np
import matplotlib.pyplot as plt
from cascade_network import CascadeNetwork

class PhaseSpaceMapper:
    def __init__(self, dt=0.05, steps=100):
        self.dt = dt
        self.steps = steps
        self.base_net = CascadeNetwork(dt=dt)

    def risk_for_params(self, param_idx1, val1, param_idx2, val2):
        """Return collapse risk for a given pair of parameter values."""
        A_mod = self.base_net.A.copy()
        A_mod[param_idx1[0], param_idx1[1]] = val1
        A_mod[param_idx2[0], param_idx2[1]] = val2
        evals = np.linalg.eigvals(A_mod)
        max_e = np.max(np.real(evals))
        return max(0.0, max_e - 1.0)

    def scan_2d(self, param1, param2, range1, range2, n=50):
        """
        Scan two couplings over their ranges.
        Returns a 2D grid of collapse risk.
        """
        grid = np.zeros((n, n))
        vals1 = np.linspace(range1[0], range1[1], n)
        vals2 = np.linspace(range2[0], range2[1], n)

        for i, v1 in enumerate(vals1):
            for j, v2 in enumerate(vals2):
                grid[i, j] = self.risk_for_params(param1, v1, param2, v2)

        return grid, vals1, vals2

    def plot_phase_map(self, param1, param2, range1, range2, n=50,
                       title=None, save_as=None):
        """Plot a 2D phase map of collapse risk."""
        grid, vals1, vals2 = self.scan_2d(param1, param2, range1, range2, n)

        fig, ax = plt.subplots(figsize=(8, 6))
        im = ax.imshow(grid.T, origin='lower',
                       extent=[range1[0], range1[1], range2[0], range2[1]],
                       cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)

        ax.set_xlabel(f'A[{param1[0]},{param1[1]}]')
        ax.set_ylabel(f'A[{param2[0]},{param2[1]}]')
        ax.set_title(title or f"Phase Map: Collapse Risk")
        plt.colorbar(im, label='Collapse Risk')
        ax.grid(True, linestyle='--', alpha=0.3)

        if save_as:
            plt.savefig(save_as, dpi=150)
        return fig

def main():
    print("\n" + "="*70)
    print("PHASE SPACE MAP — Exploring the Stability Terrain")
    print("="*70)

    mapper = PhaseSpaceMapper()

    # Example: scan two high-sensitivity couplings
    # α→s and δ→hξ
    param1 = (0, 4)  # α→s
    param2 = (2, 5)  # δ→hξ

    print(f"Scanning A[{param1[0]},{param1[1]}] and A[{param2[0]},{param2[1]}]...")
    fig = mapper.plot_phase_map(
        param1, param2,
        range1=(-0.5, 2.0),
        range2=(-0.5, 2.0),
        title="Phase Map: α→s vs δ→hξ"
    )
    plt.show()

    # Find the stable region
    grid, vals1, vals2 = mapper.scan_2d(param1, param2, (-0.5, 2.0), (-0.5, 2.0), n=100)
    stable_count = np.sum(grid < 0.001)
    total = grid.size
    print(f"Stable region size: {stable_count/total*100:.2f}% of parameter space")

    print("\nExploration is now interactive. You can scan any two couplings.")

if __name__ == "__main__":
    main()
