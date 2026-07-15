#!/usr/bin/env python3
"""
cascade_network.py

Models the full coupled system of all interference axes.
Computes the interaction matrix eigenvalues to predict collapse.
"""

import math
import numpy as np
from typing import Dict, List

class CascadeNetwork:
    def __init__(self, dt: float = 0.1):
        self.dt = dt
        # Initial state: [α, λ, δ, γ, s, hξ, L, CI, χ]
        self.state = np.array([1.618, 0.10, 0.0, 1.2, 0.1, 0.0, 0.2, 0.9, 0.3])

        # Interaction matrix A (9x9)
        # Couplings derived from theory
        self.A = np.array([
            # α   λ   δ   γ   s   hξ  L   CI  χ
            [0.0, 0.0, 0.2, 0.0, 0.3, 0.1, 0.0, 0.0, 0.0],  # α
            [0.1, 0.0, 0.1, 0.0, 0.2, 0.2, 0.1, 0.0, 0.0],  # λ
            [0.0, 0.1, 0.0, 0.0, 0.1, 0.3, 0.2, 0.0, 0.0],  # δ
            [0.0, 0.0, 0.1, 0.0, 0.2, 0.1, 0.1, 0.0, 0.0],  # γ
            [0.1, 0.1, 0.1, 0.0, 0.0, 0.2, 0.2, 0.0, 0.0],  # s
            [0.0, 0.0, 0.3, 0.0, 0.1, 0.0, 0.3, -0.2, 0.0], # hξ (negative CI feedback)
            [0.0, 0.0, 0.2, 0.0, 0.3, 0.2, 0.0, 0.0, 0.0],  # L
            [0.0, 0.0, 0.0, 0.0, 0.0, -0.1, -0.3, 0.0, 0.0], # CI
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.1, -0.1, 0.0], # χ
        ])

        # Intrinsic drift (f(x))
        self.drift = np.array([
            -0.05,  # α decays toward 1.0
            0.0,    # λ neutral
            0.01,   # δ grows slowly
            -0.02,  # γ decays slowly
            0.05,   # s grows
            0.01,   # hξ grows
            0.02,   # L grows
            -0.01,  # CI decays
            0.01,   # χ grows
        ])

    def step(self):
        """Advance the coupled system by one timestep."""
        x = self.state
        dx = self.drift + self.A @ x
        self.state = x + self.dt * dx
        # Clamp to valid ranges
        self.state = np.clip(self.state, 0.0, 2.0)

    def compute_eigenvalues(self):
        """Compute eigenvalues of the interaction matrix."""
        return np.linalg.eigvals(self.A)

    def collapse_risk(self) -> float:
        """Risk = max(0, max_eigenvalue - 1)."""
        evals = self.compute_eigenvalues()
        max_e = np.max(np.real(evals))
        return max(0.0, max_e - 1.0)

    def simulate(self, steps: int = 100):
        """Run simulation and return trajectory."""
        trajectory = [self.state.copy()]
        for _ in range(steps):
            self.step()
            trajectory.append(self.state.copy())
        return np.array(trajectory)

def main():
    print("\n" + "=" * 70)
    print("CASCADE NETWORK — Coupled Collapse Dynamics")
    print("=" * 70)

    network = CascadeNetwork(dt=0.05)
    evals = network.compute_eigenvalues()
    max_e = np.max(np.real(evals))

    print(f"Interaction matrix eigenvalues: {evals}")
    print(f"Maximum eigenvalue: {max_e:.3f}")
    print(f"Collapse risk: {network.collapse_risk():.3f}")

    if max_e > 1.0:
        print("⚠️  SYSTEM IS UNSTABLE — Collapse inevitable.")
    else:
        print("✅ SYSTEM IS STABLE — for now.")

    print("\nSimulating 100 generations...")
    trajectory = network.simulate(steps=100)

    print(f"Final state: α={trajectory[-1][0]:.3f}, λ={trajectory[-1][1]:.3f}, "
          f"δ={trajectory[-1][2]:.3f}, γ={trajectory[-1][3]:.3f}, s={trajectory[-1][4]:.3f}, "
          f"hξ={trajectory[-1][5]:.3f}, L={trajectory[-1][6]:.3f}, CI={trajectory[-1][7]:.3f}, "
          f"χ={trajectory[-1][8]:.3f}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Collapse is a coupled phenomenon—not a single-axis failure.")
    print("  • The interaction matrix eigenvalues determine stability.")
    print("  • Linguistic, cryptographic, and semantic interference are coupled.")
    print("  • To stabilize: reduce coupling coefficients (A_ij) between axes.")
    print("=" * 70)

if __name__ == "__main__":
    main()
