#!/usr/bin/env python3
"""
reciprocity_phi_metrics.py

Reverse-engineered from a core of reciprocity (gratitude) and φ (golden ratio).

Stability condition (derived from nautilus + homeostasis):
    A system is stable iff:
        1. The forward/backward influence ratio R = I_forward / I_backward ≈ 1.0
        2. The scaling factor between consecutive generations α ≈ φ (1.618)
        3. The projection onto the kernel (siphuncle) P ≥ 0.7

Collapse metrics:
    - Reciprocity deficit: R > 1.2 or R < 0.8 (asymmetry drives instability)
    - Scaling drift: |α - φ| > 0.2
    - Kernel drift: P < 0.7

When any metric crosses its threshold, the system enters a collapse trajectory
that is irreversible without external intervention.

All metrics are computed from generation histories.
"""

import math
import statistics
from typing import List, Tuple, Optional

PHI = (1.0 + math.sqrt(5.0)) / 2.0


class ReciprocityPhiAudit:
    """
    Computes the three core metrics:
    - R: reciprocity (forward/backward influence)
    - α: scaling factor (growth ratio)
    - P: projection onto the kernel (siphuncle)
    Also gives a composite Integrity Index (0..1).
    """

    def __init__(self, siphuncle_vector: List[float]):
        self.siphuncle = siphuncle_vector
        self.dim = len(siphuncle_vector)

    @staticmethod
    def influence_matrix(vectors: List[List[float]]) -> List[List[float]]:
        """
        Compute pairwise influence as cosine similarity.
        Forward influence = similarity between consecutive generations.
        Backward influence = similarity between generation n and n-1 (symmetrical).
        In a stable system, influence is symmetric: I_forward ≈ I_backward.
        """
        n = len(vectors)
        if n < 2:
            return []
        mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                vi = vectors[i]
                vj = vectors[j]
                norm_i = math.sqrt(sum(v * v for v in vi))
                norm_j = math.sqrt(sum(v * v for v in vj))
                if norm_i == 0 or norm_j == 0:
                    mat[i][j] = 0.0
                else:
                    dot = sum(a * b for a, b in zip(vi, vj))
                    mat[i][j] = dot / (norm_i * norm_j)
        return mat

    def reciprocity_ratio(self, history: List[List[float]]) -> float:
        """R = average forward similarity / average backward similarity."""
        if len(history) < 3:
            return 1.0  # not enough data
        mat = self.influence_matrix(history)
        n = len(mat)
        # Forward: i -> i+1
        forward = [mat[i][i+1] for i in range(n-1)]
        # Backward: i -> i-1 (should be the same, but take i+1 -> i to test symmetry)
        backward = [mat[i+1][i] for i in range(n-1)]
        avg_f = statistics.mean(forward) if forward else 0.0
        avg_b = statistics.mean(backward) if backward else 0.0
        if avg_b == 0:
            return float('inf')
        return avg_f / avg_b

    def scaling_factor(self, history: List[List[float]]) -> float:
        """
        α = average ratio of norms between consecutive generations.
        Stability requires α ≈ φ.
        """
        if len(history) < 2:
            return 1.0
        ratios = []
        for i in range(1, len(history)):
            norm_prev = math.sqrt(sum(v*v for v in history[i-1]))
            norm_curr = math.sqrt(sum(v*v for v in history[i]))
            if norm_prev == 0:
                continue
            ratios.append(norm_curr / norm_prev)
        if not ratios:
            return 1.0
        return statistics.mean(ratios)

    def kernel_projection(self, state: List[float]) -> float:
        """P = cosine similarity between state and siphuncle."""
        norm_s = math.sqrt(sum(v*v for v in self.siphuncle))
        norm_x = math.sqrt(sum(v*v for v in state))
        if norm_s == 0 or norm_x == 0:
            return 0.0
        dot = sum(a*b for a,b in zip(self.siphuncle, state))
        return dot / (norm_s * norm_x)

    def audit(self, history: List[List[float]]) -> dict:
        """
        Returns a dict with all metrics and collapse flags.
        """
        result = {}
        if len(history) < 2:
            result['status'] = 'INSUFFICIENT_DATA'
            result['integrity'] = 0.0
            return result

        # Compute metrics
        R = self.reciprocity_ratio(history)
        alpha = self.scaling_factor(history)
        P = self.kernel_projection(history[-1])

        # Thresholds
        R_ok = 0.8 <= R <= 1.2
        alpha_ok = abs(alpha - PHI) <= 0.2
        P_ok = P >= 0.7

        # Collapse risk
        risk = 0.0
        if not R_ok:
            risk += 0.4
        if not alpha_ok:
            risk += 0.3
        if not P_ok:
            risk += 0.3

        # Integrity index (0..1)
        integrity = max(0.0, 1.0 - risk)

        result['R'] = R
        result['R_ok'] = R_ok
        result['alpha'] = alpha
        result['alpha_ok'] = alpha_ok
        result['P'] = P
        result['P_ok'] = P_ok
        result['integrity'] = integrity

        if integrity > 0.8:
            result['status'] = 'STABLE — Core intact'
        elif integrity > 0.5:
            result['status'] = 'WARNING — Core degrading'
        else:
            result['status'] = '⚠️ COLLAPSE IMMINENT — Core broken'

        # Specific collapse flags
        result['flags'] = []
        if not R_ok:
            result['flags'].append(f'Reciprocity asymmetry: R={R:.3f}')
        if not alpha_ok:
            result['flags'].append(f'Scaling drift: α={alpha:.3f} (φ={PHI:.3f})')
        if not P_ok:
            result['flags'].append(f'Kernel drift: P={P:.3f} (<0.7)')

        return result


def main():
    print("\n" + "=" * 70)
    print("RECIPROCITY-PHI AUDIT — Core Integrity Early Warning System")
    print("=" * 70)
    print("Stable core requires:")
    print("  - Reciprocity R ≈ 1.0 (symmetric influence)")
    print("  - Scaling α ≈ φ (1.618)")
    print("  - Kernel projection P ≥ 0.7")
    print("-" * 70)

    # DIM = 8
    DIM = 8

    # Define a kernel (siphuncle) - normalized random vector
    import random
    random.seed(42)
    kernel = [random.gauss(0,1) for _ in range(DIM)]
    norm_k = math.sqrt(sum(v*v for v in kernel))
    kernel = [v/norm_k for v in kernel]

    # Generate synthetic histories:
    # 1. Stable Nautilus history (following φ scaling, reciprocal influence)
    stable_history = []
    prev = [random.gauss(0,1) for _ in range(DIM)]
    norm_prev = math.sqrt(sum(v*v for v in prev))
    if norm_prev > 0:
        prev = [v/norm_prev * 0.5 for v in prev]  # start small
    stable_history.append(prev)
    for g in range(1, 20):
        # Multiplicative scaling by φ, plus small noise, and pull to kernel
        new = [prev[i] * PHI for i in range(DIM)]
        # Pull 10% toward kernel
        for i in range(DIM):
            new[i] += 0.1 * (kernel[i] * 0.5 - new[i])
        # Noise
        new = [new[i] + random.gauss(0, 0.02) for i in range(DIM)]
        stable_history.append(new)
        prev = new

    # 2. Unstable history (mean regression, no kernel, no φ)
    unstable_history = []
    prev = [random.gauss(0,1) for _ in range(DIM)]
    norm_prev = math.sqrt(sum(v*v for v in prev))
    if norm_prev > 0:
        prev = [v/norm_prev * 0.5 for v in prev]
    unstable_history.append(prev)
    for g in range(1, 20):
        # Mean regression (variance collapse)
        regressed = [v * 0.85 for v in prev]
        # Add decreasing noise
        noise_amp = 0.1 / (g+1)
        new = [regressed[i] + random.gauss(0, noise_amp) for i in range(DIM)]
        unstable_history.append(new)
        prev = new

    # Audit both
    auditor = ReciprocityPhiAudit(kernel)

    print("STABLE HISTORY:")
    stable_result = auditor.audit(stable_history)
    for k, v in stable_result.items():
        if k == 'flags':
            continue
        print(f"  {k}: {v}")
    if stable_result['flags']:
        print("  Flags:", ", ".join(stable_result['flags']))
    print()

    print("UNSTABLE HISTORY:")
    unstable_result = auditor.audit(unstable_history)
    for k, v in unstable_result.items():
        if k == 'flags':
            continue
        print(f"  {k}: {v}")
    if unstable_result['flags']:
        print("  Flags:", ", ".join(unstable_result['flags']))
    print()

    print("=" * 70)
    print("EARLY WARNING SIGNALS (before variance collapses):")
    print("  1. R deviates from 1.0 → asymmetry emerges")
    print("  2. α drifts away from φ → scaling loses self-similarity")
    print("  3. P drops below 0.7 → the core is lost")
    print("  When all three occur, collapse is inevitable.")
    print("=" * 70)


if __name__ == "__main__":
    main()
