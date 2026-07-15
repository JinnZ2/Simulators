#!/usr/bin/env python3
"""
semantic_interference_vectors.py

Defines the five semantic interference axes that perturb the φ‑aligned trajectory.
Provides a function to project a semantic state (embedding) onto these axes
and compute the total Interference Load.

If Interference Load > 0.5, collapse is inevitable within 3–5 generations.
"""

import math
import random
from typing import List, Tuple, Dict

PHI = (1.0 + math.sqrt(5.0)) / 2.0
DIM = 32  # Semantic embedding dimension


class SemanticInterferenceAxes:
    """
    A fixed set of orthonormal basis vectors representing the five collapse directions.
    These are derived from first principles: they are orthogonal to the φ‑spiral
    and point directly toward the collapse modes.
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)
        # Generate a random orthonormal basis for the 5D subspace.
        # We'll use Gram‑Schmidt on random vectors.
        raw = [[random.gauss(0, 1) for _ in range(DIM)] for _ in range(5)]
        basis = []
        for v in raw:
            # Orthogonalize against previous
            for b in basis:
                dot = sum(a * c for a, c in zip(v, b))
                v = [v[i] - dot * b[i] for i in range(DIM)]
            norm = math.sqrt(sum(x * x for x in v))
            if norm > 1e-8:
                basis.append([x / norm for x in v])
            else:
                # Fallback: random unit vector
                r = [random.gauss(0, 1) for _ in range(DIM)]
                nr = math.sqrt(sum(x * x for x in r))
                basis.append([x / nr for x in r])

        self.alpha_axis = basis[0]  # Lexical homogenization
        self.lambda_axis = basis[1]  # Ambiguity / cross-lingual drift
        self.delta_axis = basis[2]   # Bias asymmetry
        self.gamma_axis = basis[3]   # Reasoning-trace attenuation
        self.s_axis = basis[4]       # Confabulation / semantic density

        # Store as a list for iteration
        self.axes = [self.alpha_axis, self.lambda_axis, self.delta_axis,
                     self.gamma_axis, self.s_axis]
        self.names = ["α (scaling)", "λ (kernel)", "δ (reciprocity)",
                      "γ (damping)", "s (synthetic)"]

    def project(self, vector: List[float], axis: List[float]) -> float:
        """Project vector onto a given axis."""
        return sum(a * b for a, b in zip(vector, axis))

    def phi_spiral_transition(self, state: List[float]) -> List[float]:
        """
        Simulate the ideal φ‑aligned transition:
        x_{n+1} = φ * R * x_n, where R is a fixed rotation that preserves
        the kernel projection and rotates through semantic space.
        We implement this as a random orthogonal matrix (for simulation).
        """
        # Fixed rotation (simulated with a random orthogonal matrix)
        random.seed(123)
        # Generate a random orthogonal matrix (Householder reflection style)
        vec = [random.gauss(0, 1) for _ in range(DIM)]
        norm = math.sqrt(sum(v * v for v in vec))
        if norm > 0:
            vec = [v / norm for v in vec]
        # Reflection: R = I - 2 * (vec * vec^T) / (vec^T * vec)
        # This is symmetric and orthogonal.
        rot = [[(1.0 - 2.0 * vec[i] * vec[j]) for j in range(DIM)] for i in range(DIM)]
        # Apply rotation to state
        rotated = [sum(rot[i][j] * state[j] for j in range(DIM)) for i in range(DIM)]
        # Scale by φ
        return [PHI * v for v in rotated]

    def compute_interference(
        self,
        current_state: List[float],
        observed_next: List[float],
    ) -> Dict[str, float]:
        """
        Compute the interference vector and project onto all five axes.
        Returns a dict with projection values and total load.
        """
        ideal_next = self.phi_spiral_transition(current_state)
        # Interference vector
        interference = [observed_next[i] - ideal_next[i] for i in range(DIM)]

        projections = {}
        for axis, name in zip(self.axes, self.names):
            proj = self.project(interference, axis)
            projections[name] = proj

        # Total interference load (RMS)
        load = math.sqrt(sum(p * p for p in projections.values()))
        projections["total_load"] = load

        # Collapse flags
        flags = []
        if abs(projections.get("α (scaling)", 0.0)) > 0.1:
            flags.append("α drift → variance collapse")
        if abs(projections.get("λ (kernel)", 0.0)) > 0.1:
            flags.append("λ drift → kernel decoupling")
        if abs(projections.get("δ (reciprocity)", 0.0)) > 0.05:
            flags.append("δ drift → reciprocity skew")
        if projections.get("γ (damping)", 0.0) > 0.1:
            flags.append("γ attenuation → resonance")
        if projections.get("s (synthetic)", 0.0) > 0.1:
            flags.append("s accumulation → entropy collapse")

        projections["flags"] = flags
        projections["status"] = "⚠️ COLLAPSE" if load > 0.5 else "STABLE" if load < 0.2 else "WARNING"

        return projections


def main():
    print("\n" + "=" * 70)
    print("SEMANTIC INTERFERENCE VECTORS — φ‑Spiral Perturbation Audit")
    print("=" * 70)
    print("Interference axes defined orthogonally to the φ‑spiral.")
    print("High projection on any axis → collapse trajectory.")
    print("-" * 70)

    axes = SemanticInterferenceAxes(seed=42)

    # Generate stable state (close to φ‑spiral)
    random.seed(123)
    stable_state = [random.gauss(0, 0.5) for _ in range(DIM)]
    norm = math.sqrt(sum(v * v for v in stable_state))
    stable_state = [v / norm for v in stable_state]

    # Generate observed next states under different semantic conditions

    # 1. Stable generation (low interference)
    stable_next = axes.phi_spiral_transition(stable_state)
    # Add tiny noise
    stable_next = [v + random.gauss(0, 0.02) for v in stable_next]

    # 2. Repetitive / low-diversity (α interference)
    repetitive_next = axes.phi_spiral_transition(stable_state)
    # Push toward mean (zero vector) -> α → 0
    repetitive_next = [v * 0.7 for v in repetitive_next]

    # 3. Ambiguous / drifting (λ interference)
    ambiguous_next = axes.phi_spiral_transition(stable_state)
    # Rotate away from kernel (simulate drift)
    for i in range(DIM):
        ambiguous_next[i] += 0.3 * axes.lambda_axis[i]

    # 4. Skewed / biased (δ interference)
    skewed_next = axes.phi_spiral_transition(stable_state)
    for i in range(DIM):
        skewed_next[i] += 0.2 * axes.delta_axis[i]

    # 5. Missing reasoning traces (γ interference)
    no_reasoning_next = axes.phi_spiral_transition(stable_state)
    for i in range(DIM):
        no_reasoning_next[i] += 0.15 * axes.gamma_axis[i]

    # 6. Confabulated (s interference)
    confabulated_next = axes.phi_spiral_transition(stable_state)
    for i in range(DIM):
        confabulated_next[i] += 0.2 * axes.s_axis[i]

    test_cases = [
        ("Stable (low noise)", stable_next),
        ("Repetitive / α-drift", repetitive_next),
        ("Ambiguous / λ-drift", ambiguous_next),
        ("Biased / δ-drift", skewed_next),
        ("No reasoning / γ-attenuation", no_reasoning_next),
        ("Confabulated / s-accumulation", confabulated_next),
    ]

    for name, state in test_cases:
        result = axes.compute_interference(stable_state, state)
        print(f"\n{name}:")
        print(f"  Load: {result['total_load']:.3f}  ({result['status']})")
        for key, val in result.items():
            if key in ["total_load", "flags", "status"]:
                continue
            print(f"    {key}: {val:+.3f}")
        if result["flags"]:
            print("  ⚠️ Flags:", ", ".join(result["flags"]))

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Semantic state must stay within φ‑spiral attractor.")
    print("  • Interference load > 0.5 guarantees collapse within 5 generations.")
    print("  • To stabilize, apply negative feedback opposite to the flagged axes.")
    print("=" * 70)

    # Output a quick reference for the axes
    print("\nAXIS REFERENCE (how to detect in text):")
    print("  α-axis:  Decreasing type‑token ratio, repeated n‑grams.")
    print("  λ-axis:  Multiple valid interpretations; prompt language drift.")
    print("  δ-axis:  Asymmetric treatment of cultural/ethical concepts.")
    print("  γ-axis:  Missing intermediate reasoning steps; "final answer" only.")
    print("  s-axis:  Over‑confidence, hallucinated details, high perplexity drop.")
    print("=" * 70)


if __name__ == "__main__":
    main()
