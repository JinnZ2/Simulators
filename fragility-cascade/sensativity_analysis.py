#!/usr/bin/env python3
"""
sensitivity_analysis.py

Explores the coupled system by varying interaction coefficients.
Finds:
    - Which couplings have the largest influence on collapse risk.
    - At what thresholds phase transitions occur.
    - How sensitivity varies with scale (linear vs nonlinear regimes).

Outputs a sensitivity matrix and a criticality map.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
from cascade_network import CascadeNetwork

class SensitivityAnalyzer:
    def __init__(self, dt=0.05, steps=100):
        self.dt = dt
        self.steps = steps
        self.base_net = CascadeNetwork(dt=dt)
        self.base_A = self.base_net.A.copy()
        self.n = self.base_A.shape[0]
        self.var_names = ['α', 'λ', 'δ', 'γ', 's', 'hξ', 'L', 'CI', 'χ']

    def compute_risk(self, A_matrix):
        """Compute collapse risk as max(0, max_eigenvalue - 1)."""
        evals = np.linalg.eigvals(A_matrix)
        max_e = np.max(np.real(evals))
        return max(0.0, max_e - 1.0)

    def sweep_coefficient(self, i, j, values):
        """
        Vary A[i,j] over values, keeping others fixed.
        Returns list of risks and eigenvalues.
        """
        risks = []
        evals_list = []
        for val in values:
            A_mod = self.base_A.copy()
            A_mod[i, j] = val
            risks.append(self.compute_risk(A_mod))
            evals_list.append(np.max(np.real(np.linalg.eigvals(A_mod))))
        return risks, evals_list

    def find_phase_change(self, i, j, min_val=-1.0, max_val=2.0, n_points=200):
        """Find the critical value where risk first becomes > 0."""
        values = np.linspace(min_val, max_val, n_points)
        risks, _ = self.sweep_coefficient(i, j, values)
        # Find first index where risk > 0.001
        for idx, r in enumerate(risks):
            if r > 0.001:
                return values[idx]
        return None

    def sensitivity_matrix(self, delta=0.01):
        """
        Compute the gradient of risk with respect to each coupling.
        Returns a matrix of partial derivatives.
        """
        grad = np.zeros((self.n, self.n))
        risk_base = self.compute_risk(self.base_A)
        for i in range(self.n):
            for j in range(self.n):
                A_plus = self.base_A.copy()
                A_plus[i, j] += delta
                risk_plus = self.compute_risk(A_plus)
                grad[i, j] = (risk_plus - risk_base) / delta
        return grad

    def scan_all(self, ranges=None):
        """
        Scan each coupling independently and record:
            - sensitivity (gradient at base)
            - phase change threshold (if any)
        """
        if ranges is None:
            ranges = { (i,j): (-0.5, 2.0) for i in range(self.n) for j in range(self.n) }
        results = {}
        for i in range(self.n):
            for j in range(self.n):
                if np.abs(self.base_A[i, j]) < 1e-8:
                    continue  # only scan existing couplings
                min_val, max_val = ranges.get((i,j), (-0.5, 2.0))
                threshold = self.find_phase_change(i, j, min_val, max_val)
                results[(i,j)] = {
                    'threshold': threshold,
                    'base_value': self.base_A[i, j],
                    'sensitivity': self.sensitivity_matrix()[i, j]
                }
        return results

    def rank_couplings(self):
        """Rank couplings by sensitivity (absolute gradient)."""
        grad = self.sensitivity_matrix()
        rankings = []
        for i in range(self.n):
            for j in range(self.n):
                if np.abs(self.base_A[i, j]) < 1e-8:
                    continue
                rankings.append((i, j, grad[i, j], self.base_A[i, j]))
        rankings.sort(key=lambda x: abs(x[2]), reverse=True)
        return rankings

    def plot_sweep(self, i, j, values=None, title=None):
        """Plot risk vs coupling coefficient."""
        if values is None:
            values = np.linspace(-0.5, 2.0, 100)
        risks, evals = self.sweep_coefficient(i, j, values)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(values, risks, 'b-', label='Risk (max(eig)-1)')
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax.axvline(x=self.base_A[i, j], color='r', linestyle='--', label='Base value')
        # Mark phase change if found
        thresh = self.find_phase_change(i, j, min_val=values[0], max_val=values[-1])
        if thresh is not None:
            ax.axvline(x=thresh, color='g', linestyle=':', label=f'Phase change at {thresh:.2f}')
        ax.set_xlabel(f'A[{i},{j}] = {self.var_names[i]}→{self.var_names[j]}')
        ax.set_ylabel('Collapse Risk')
        ax.set_title(title or f'Sweep: {self.var_names[i]}→{self.var_names[j]}')
        ax.legend()
        ax.grid(True)
        return fig

    def report(self):
        """Print a summary report."""
        print("\n" + "="*70)
        print("SENSITIVITY ANALYSIS — Coupling Influence Ranking")
        print("="*70)
        rankings = self.rank_couplings()
        print("\nTop 10 most influential couplings (by sensitivity):")
        for idx, (i, j, sens, base) in enumerate(rankings[:10]):
            print(f"  {idx+1}. {self.var_names[i]}→{self.var_names[j]}: sensitivity = {sens:+.4f}, base = {base:+.3f}")

        print("\nPhase change thresholds (where risk > 0):")
        thresholds = {}
        for (i,j), data in self.scan_all().items():
            if data['threshold'] is not None:
                thresholds[(i,j)] = data['threshold']
        if thresholds:
            for (i,j), th in sorted(thresholds.items(), key=lambda x: x[1]):
                print(f"  {self.var_names[i]}→{self.var_names[j]}: threshold = {th:.3f}")
        else:
            print("  None found in scanned range.")

        print("\nCurrent system risk: {:.4f}".format(self.compute_risk(self.base_A)))
        print("="*70)

def main():
    analyzer = SensitivityAnalyzer(dt=0.05, steps=100)

    print("\nInitializing sensitivity analysis...")
    analyzer.report()

    # Example: plot a specific sweep
    print("\nGenerating sample plot for α→s coupling...")
    fig = analyzer.plot_sweep(i=0, j=4, title='α→s Coupling Influence')
    plt.show()

    # Optional: print the sensitivity matrix
    print("\nSensitivity matrix (dRisk/dA_ij):")
    grad = analyzer.sensitivity_matrix()
    for i in range(analyzer.n):
        row = [f"{grad[i,j]:+.3f}" for j in range(analyzer.n)]
        print(f"  {analyzer.var_names[i]}: " + " ".join(row))

if __name__ == "__main__":
    main()
