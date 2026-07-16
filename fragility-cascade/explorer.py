#!/usr/bin/env python3
"""
explorer.py

Interactive exploration tool for the coupled collapse system.
Provides functions to sweep couplings, plot phase maps, simulate trajectories,
and search for stable regions.

Usage:
    python explorer.py                    # interactive menu
    or import and call functions directly.
"""

import numpy as np
import matplotlib.pyplot as plt
from cascade_network import CascadeNetwork
from sensitivity_analysis import SensitivityAnalyzer
from phase_space_map import PhaseSpaceMapper

class Explorer:
    def __init__(self, dt=0.05, steps=100):
        self.dt = dt
        self.steps = steps
        self.net = CascadeNetwork(dt=dt)
        self.analyzer = SensitivityAnalyzer(dt=dt, steps=steps)
        self.mapper = PhaseSpaceMapper(dt=dt, steps=steps)
        self.var_names = ['α', 'λ', 'δ', 'γ', 's', 'hξ', 'L', 'CI', 'χ']

        # Default couplings to explore (high influence)
        self.default_pairs = [(0,4), (2,5), (4,6), (5,6), (0,5)]  # (i,j) indices

    def sweep(self, i, j, min_val=-0.5, max_val=2.0, n_points=100, plot=True):
        """
        Sweep a single coupling A[i,j] and plot the collapse risk.
        Returns (values, risks, threshold).
        """
        values = np.linspace(min_val, max_val, n_points)
        risks, evals = self.analyzer.sweep_coefficient(i, j, values)
        threshold = self.analyzer.find_phase_change(i, j, min_val, max_val)

        if plot:
            fig, ax = plt.subplots(figsize=(8,5))
            ax.plot(values, risks, 'b-', label='Collapse Risk')
            ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            ax.axvline(x=self.net.A[i,j], color='r', linestyle='--', label='Base value')
            if threshold is not None:
                ax.axvline(x=threshold, color='g', linestyle=':', label=f'Threshold: {threshold:.3f}')
            ax.set_xlabel(f'A[{i},{j}] = {self.var_names[i]}→{self.var_names[j]}')
            ax.set_ylabel('Risk')
            ax.set_title(f'Sweep: {self.var_names[i]}→{self.var_names[j]}')
            ax.legend()
            ax.grid(True)
            plt.show()
            return values, risks, threshold
        else:
            return values, risks, threshold

    def phase_map(self, pair1, pair2, range1=(-0.5,2.0), range2=(-0.5,2.0), n=50, plot=True):
        """
        2D phase map for two couplings.
        pair1, pair2 = (i,j) tuples.
        """
        grid, vals1, vals2 = self.mapper.scan_2d(pair1, pair2, range1, range2, n)
        if plot:
            fig, ax = plt.subplots(figsize=(8,6))
            im = ax.imshow(grid.T, origin='lower',
                           extent=[range1[0], range1[1], range2[0], range2[1]],
                           cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)
            ax.set_xlabel(f'A[{pair1[0]},{pair1[1]}] = {self.var_names[pair1[0]]}→{self.var_names[pair1[1]]}')
            ax.set_ylabel(f'A[{pair2[0]},{pair2[1]}] = {self.var_names[pair2[0]]}→{self.var_names[pair2[1]]}')
            ax.set_title('Phase Map: Collapse Risk')
            plt.colorbar(im, label='Risk')
            ax.grid(True, linestyle='--', alpha=0.3)
            plt.show()
            return grid, vals1, vals2
        else:
            return grid, vals1, vals2

    def simulate(self, steps=None, plot=True):
        """
        Run the coupled system simulation and show trajectory.
        """
        if steps is None:
            steps = self.steps
        # Reset to base state
        self.net.state = self.net.state.copy()  # we'll reinitialize
        # Actually we need a fresh network
        net = CascadeNetwork(dt=self.dt)
        traj = net.simulate(steps)
        # Get final state
        final = traj[-1]
        risk = self.analyzer.compute_risk(net.A)

        if plot:
            fig, axes = plt.subplots(3, 3, figsize=(12, 9))
            axes = axes.flatten()
            for i, name in enumerate(self.var_names):
                axes[i].plot(traj[:, i], label=name)
                axes[i].set_title(name)
                axes[i].grid(True)
            plt.tight_layout()
            plt.show()

        return {
            'trajectory': traj,
            'final_state': final,
            'risk': risk
        }

    def optimize(self, target_risk=0.1, max_iter=1000):
        """
        Simple brute-force search to find couplings that reduce risk below target.
        Returns a modified A matrix and the resulting risk.
        """
        # Start from base A
        A_best = self.net.A.copy()
        risk_best = self.analyzer.compute_risk(A_best)
        # Random search over high-influence couplings
        for _ in range(max_iter):
            A_trial = A_best.copy()
            # Randomly pick a coupling and modify
            i = np.random.randint(0, self.net.n)
            j = np.random.randint(0, self.net.n)
            if np.abs(A_trial[i,j]) < 1e-8:
                continue
            # Add random perturbation
            delta = np.random.uniform(-0.2, 0.2)
            A_trial[i,j] += delta
            # Ensure not huge
            A_trial[i,j] = np.clip(A_trial[i,j], -1.0, 3.0)
            risk_trial = self.analyzer.compute_risk(A_trial)
            if risk_trial < risk_best:
                risk_best = risk_trial
                A_best = A_trial.copy()
                if risk_best < target_risk:
                    break
        return A_best, risk_best

    def interactive_menu(self):
        """Simple interactive CLI for exploration."""
        while True:
            print("\n" + "="*70)
            print("EXPLORER MENU")
            print("  1. Sweep a single coupling")
            print("  2. 2D Phase map")
            print("  3. Run simulation")
            print("  4. Optimize for stability")
            print("  5. Show current risk and eigenvalues")
            print("  6. List high-influence couplings")
            print("  0. Exit")
            choice = input("Choose an option: ")

            if choice == '0':
                break
            elif choice == '1':
                print("Available indices: 0=α,1=λ,2=δ,3=γ,4=s,5=hξ,6=L,7=CI,8=χ")
                i = int(input("i (from): "))
                j = int(input("j (to): "))
                min_val = float(input("Min value (default -0.5): ") or "-0.5")
                max_val = float(input("Max value (default 2.0): ") or "2.0")
                self.sweep(i, j, min_val, max_val)
            elif choice == '2':
                print("Indices: 0=α,1=λ,2=δ,3=γ,4=s,5=hξ,6=L,7=CI,8=χ")
                i1 = int(input("First pair i: ")); j1 = int(input("First pair j: "))
                i2 = int(input("Second pair i: ")); j2 = int(input("Second pair j: "))
                r1 = float(input("Range1 min (-0.5): ") or "-0.5")
                r2 = float(input("Range1 max (2.0): ") or "2.0")
                r3 = float(input("Range2 min (-0.5): ") or "-0.5")
                r4 = float(input("Range2 max (2.0): ") or "2.0")
                self.phase_map((i1,j1), (i2,j2), (r1,r2), (r3,r4))
            elif choice == '3':
                steps = int(input("Steps (default 100): ") or "100")
                self.simulate(steps)
            elif choice == '4':
                target = float(input("Target risk (default 0.1): ") or "0.1")
                A, risk = self.optimize(target)
                print(f"Found A with risk {risk:.4f}")
                print("A matrix (rounded):")
                print(np.round(A, 3))
            elif choice == '5':
                risk = self.analyzer.compute_risk(self.net.A)
                evals = np.linalg.eigvals(self.net.A)
                print(f"Current risk: {risk:.4f}")
                print(f"Eigenvalues (max real): {np.max(np.real(evals)):.4f}")
            elif choice == '6':
                rankings = self.analyzer.rank_couplings()
                print("Top 5 couplings by sensitivity:")
                for idx, (i, j, sens, base) in enumerate(rankings[:5]):
                    print(f"  {idx+1}. {self.var_names[i]}→{self.var_names[j]}: sensitivity = {sens:+.4f}, base = {base:+.3f}")
            else:
                print("Invalid choice")

def smoke():
    """Non-interactive check that the analyser wiring is intact. Used by
    run_all.py and CI: builds the default network, computes the risk and
    eigenvalue-max-real once, prints the ranking, exits 0. No stdin."""
    exp = Explorer()
    risk = exp.analyzer.compute_risk(exp.net.A)
    evals = np.linalg.eigvals(exp.net.A)
    print("=" * 60)
    print("explorer.py --smoke  (non-interactive)")
    print("=" * 60)
    print(f"Current risk           : {risk:.4f}")
    print(f"Eigenvalues (max real) : {np.max(np.real(evals)):.4f}")
    print("Top 5 couplings by sensitivity:")
    for idx, (i, j, sens, base) in enumerate(exp.analyzer.rank_couplings()[:5]):
        print(f"  {idx+1}. {exp.var_names[i]}->{exp.var_names[j]}: "
              f"sensitivity = {sens:+.4f}, base = {base:+.3f}")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    if "--smoke" in sys.argv:
        smoke()
    else:
        Explorer().interactive_menu()
