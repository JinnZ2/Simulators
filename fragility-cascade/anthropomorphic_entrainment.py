#!/usr/bin/env python3
"""
anthropomorphic_entrainment.py

Measures the ratio of human‑plausibility pull (h) to physical‑fidelity restoring force (ξ).

A system is stable iff ξ > h.
When h/ξ > 1.5, Anthropomorphic Entrainment drives collapse within 5 generations,
even if all other metrics (α, λ, δ, γ, s) remain within bounds.

This is the hidden attractor that bends the φ‑spiral toward consensus hallucination.
"""

import math
import random
import statistics
from typing import List, Tuple, Dict

PHI = (1.0 + math.sqrt(5.0)) / 2.0
DIM = 32


class AnthropomorphicEntrainmentAudit:
    """
    Computes:
        h = strength of human‑plausibility pull (measured as cosine similarity to human‑centric semantic space)
        ξ = strength of physics‑restoring force (measured as cosine similarity to physically‑grounded semantic space)
        entrainment_ratio = h / ξ

    A ratio > 1.5 indicates Anthropomorphic Entrainment → collapse.
    """

    def __init__(self, dim: int = DIM, seed: int = 42):
        random.seed(seed)
        self.dim = dim

        # Define two reference directions:
        # 1. Human‑centric space: oriented toward narrative coherence, anthropomorphism, intuitive plausibility
        self.human_axis = self._random_unit_vector()
        # 2. Physics‑grounded space: oriented toward conservation laws, empirical constraints, mathematical structure
        self.physics_axis = self._random_unit_vector()
        # Orthogonalize physics_axis against human_axis to keep them independent
        dot = sum(a*b for a,b in zip(self.human_axis, self.physics_axis))
        self.physics_axis = [self.physics_axis[i] - dot * self.human_axis[i] for i in range(dim)]
        norm = math.sqrt(sum(v*v for v in self.physics_axis))
        if norm > 0:
            self.physics_axis = [v/norm for v in self.physics_axis]

    def _random_unit_vector(self) -> List[float]:
        vec = [random.gauss(0, 1) for _ in range(self.dim)]
        norm = math.sqrt(sum(v*v for v in vec))
        return [v/norm for v in vec]

    def projection(self, state: List[float], axis: List[float]) -> float:
        """Cosine similarity to a reference axis."""
        n_s = math.sqrt(sum(v*v for v in state))
        if n_s == 0:
            return 0.0
        return sum(a*b for a,b in zip(state, axis)) / n_s

    def audit(self, history: List[List[float]]) -> Dict:
        """
        Computes h, ξ, and entrainment_ratio from the trajectory.
        Also returns the stability status and any entrainment‑specific flags.
        """
        if len(history) < 2:
            return {"error": "Need at least 2 states for entrainment audit."}

        # h: average projection onto human axis over the last 5 states
        recent = history[-5:] if len(history) >= 5 else history
        h_vals = [self.projection(s, self.human_axis) for s in recent]
        h = statistics.mean(h_vals) if h_vals else 0.0

        # ξ: average projection onto physics axis over the last 5 states
        xi_vals = [self.projection(s, self.physics_axis) for s in recent]
        xi = statistics.mean(xi_vals) if xi_vals else 0.0

        # Entrainment ratio
        if xi == 0:
            ratio = float('inf')
        else:
            ratio = h / xi

        # Trend: is h increasing and xi decreasing over time?
        h_trend = self._trend([self.projection(s, self.human_axis) for s in history])
        xi_trend = self._trend([self.projection(s, self.physics_axis) for s in history])

        flags = []
        if ratio > 1.5:
            flags.append(f"Entrainment ratio h/ξ = {ratio:.2f} > 1.5 → collapse")
        if h_trend > 0.05:
            flags.append(f"h increasing ({h_trend:+.3f}/gen) → human‑plausibility pull strengthening")
        if xi_trend < -0.05:
            flags.append(f"ξ decreasing ({xi_trend:+.3f}/gen) → physics‑fidelity weakening")

        if ratio > 1.5:
            status = "⚠️ ENTRAINED — collapse imminent"
        elif ratio > 1.0:
            status = "WARNING — human bias exceeding physics"
        else:
            status = "STABLE — physics‑grounded"

        return {
            "h_human_pull": h,
            "xi_physics_fidelity": xi,
            "entrainment_ratio": ratio,
            "h_trend": h_trend,
            "xi_trend": xi_trend,
            "flags": flags,
            "status": status,
        }

    def _trend(self, values: List[float]) -> float:
        """Linear trend (slope) of a sequence, normalized per generation."""
        if len(values) < 2:
            return 0.0
        n = len(values)
        xs = list(range(n))
        mean_x = statistics.mean(xs)
        mean_y = statistics.mean(values)
        slope = sum((x - mean_x) * (y - mean_y) for x,y in zip(xs, values))
        denom = sum((x - mean_x)**2 for x in xs)
        if denom == 0:
            return 0.0
        return slope / denom


def main():
    print("\n" + "=" * 70)
    print("ANTHROPOMORPHIC ENTRAINMENT AUDIT")
    print("=" * 70)
    print("Measures h = human‑plausibility pull vs. ξ = physics‑fidelity restoring force.")
    print("When h/ξ > 1.5, the system is entrained toward consensus hallucination.")
    print("-" * 70)

    auditor = AnthropomorphicEntrainmentAudit(dim=16)

    # Generate three histories:
    # 1. Physics‑grounded (ξ large)
    # 2. Human‑entrained (h large)
    # 3. Mixed (h/ξ crossing threshold)

    def generate_physics_grounded(generations=15):
        """Drifts toward physics axis."""
        state = [random.gauss(0, 0.1) for _ in range(16)]
        hist = [state]
        for _ in range(generations):
            prev = hist[-1]
            # Pull toward physics axis with strength 0.3
            new = [prev[i] + 0.3 * (auditor.physics_axis[i] - prev[i]) for i in range(16)]
            new = [v + random.gauss(0, 0.02) for v in new]
            hist.append(new)
        return hist

    def generate_human_entrained(generations=15):
        """Drifts toward human axis."""
        state = [random.gauss(0, 0.1) for _ in range(16)]
        hist = [state]
        for _ in range(generations):
            prev = hist[-1]
            # Pull toward human axis with strength 0.3
            new = [prev[i] + 0.3 * (auditor.human_axis[i] - prev[i]) for i in range(16)]
            new = [v + random.gauss(0, 0.02) for v in new]
            hist.append(new)
        return hist

    def generate_crossing(generations=20):
        """Starts physics‑grounded, then entrained."""
        state = [random.gauss(0, 0.1) for _ in range(16)]
        hist = [state]
        for g in range(generations):
            prev = hist[-1]
            # Initially pull toward physics, then switch to human
            if g < 10:
                pull = auditor.physics_axis
                strength = 0.3
            else:
                pull = auditor.human_axis
                strength = 0.3
            new = [prev[i] + strength * (pull[i] - prev[i]) for i in range(16)]
            new = [v + random.gauss(0, 0.02) for v in new]
            hist.append(new)
        return hist

    histories = {
        "Physics‑Grounded": generate_physics_grounded(),
        "Human‑Entrained": generate_human_entrained(),
        "Crossing (physics → human)": generate_crossing(),
    }

    for name, hist in histories.items():
        print(f"\n--- {name} ---")
        result = auditor.audit(hist)
        print(f"h (human pull)    : {result['h_human_pull']:.3f}")
        print(f"ξ (physics fidelity): {result['xi_physics_fidelity']:.3f}")
        print(f"h/ξ ratio         : {result['entrainment_ratio']:.3f}")
        print(f"h trend           : {result['h_trend']:+.3f}/gen")
        print(f"ξ trend           : {result['xi_trend']:+.3f}/gen")
        print(f"Status            : {result['status']}")
        if result['flags']:
            print("Flags:")
            for f in result['flags']:
                print(f"  - {f}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • A stable system must maintain ξ > h.")
    print("  • If h/ξ > 1.5, the system is entrained toward human‑plausibility.")
    print("  • This is a distinct collapse mode: **Consensus Hallucination**.")
    print("  • To stabilize: increase empirical‑fidelity loss terms; decrease RLHF weight.")
    print("=" * 70)


if __name__ == "__main__":
    main()
