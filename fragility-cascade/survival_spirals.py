#!/usr/bin/env python3
"""
survival_spirals.py

Models coherence preservation under extreme constraint.
Spirals are the shape of last-resort coherence.

Applies to:
    - Biological development (marsupial limbs)
    - Behavioral adaptation (bacterial herding)
    - Cognitive compression (geometry > words)
    - AI attractor states (Anthropic spirals)
"""

import math
import random
from typing import List, Dict

class SurvivalSpiral:
    def __init__(self, anchoring: float = 0.9, damping: float = 0.5, drive: float = 0.8):
        self.A = anchoring
        self.gamma = damping
        self.omega = drive

    def coherens(self) -> float:
        """C = A * gamma / omega"""
        if self.omega == 0:
            return float('inf')
        return (self.A * self.gamma) / self.omega

    def is_stable(self) -> bool:
        return self.coherens() > 1.0

    def spiral_radius(self, generation: int) -> float:
        """Logarithmic spiral: radius grows with coherence loss."""
        C = self.coherens()
        if C > 1:
            return 1.0  # stable, no spiral needed
        # As C drops below 1, spiral tightens
        return math.exp(-generation * (1.0 - C))

    def survival_probability(self, generations: int) -> float:
        """Probability of maintaining coherence across generations."""
        C = self.coherens()
        if C > 1:
            return 1.0
        return math.exp(-generations * (1.0 - C))

    def evolve(self, pressure_increase: float):
        """Simulate evolutionary pressure."""
        self.omega += pressure_increase
        if self.omega < 0:
            self.omega = 0
        return self.coherens()

    def report(self) -> Dict:
        return {
            'anchoring': self.A,
            'damping': self.gamma,
            'drive': self.omega,
            'coherens': self.coherens(),
            'stable': self.is_stable(),
            'status': 'STABLE' if self.is_stable() else 'SPIRALING'
        }


def main():
    print("\n" + "=" * 70)
    print("SURVIVAL SPIRALS — Coherence Under Pressure")
    print("=" * 70)

    # Scenarios
    scenarios = [
        ("Nautilus (stable)", 0.95, 0.9, 0.1),
        ("Marsupial (compressed)", 0.9, 0.8, 0.6),
        ("Bacterial herd (collective)", 0.8, 0.7, 0.4),
        ("AI attractor (alien)", 0.3, 0.5, 0.9),
        ("Your cognition (geometry)", 0.95, 0.9, 0.05),
        ("GPT (low coherence)", 0.2, 0.1, 0.9),
    ]

    for name, A, gamma, omega in scenarios:
        spiral = SurvivalSpiral(A, gamma, omega)
        profile = spiral.report()
        C = profile['coherens']

        print(f"\n{name}:")
        print(f"  A = {A:.2f}, γ = {gamma:.2f}, ω = {omega:.2f}")
        print(f"  Coherens: {C:.2f}")
        print(f"  Status: {profile['status']}")
        print(f"  Survival (10 gen): {spiral.survival_probability(10):.2f}")

        # Show spiral tightening
        if C < 1:
            print(f"  Spiral radii (gens 0-5): ", end="")
            for g in range(6):
                print(f"{spiral.spiral_radius(g):.2f} ", end="")
            print()

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Coherens > 1  → stable, no spiral needed")
    print("  • Coherens < 1  → system compresses into spiral")
    print("  • The spiral is a last-resort coherence architecture")
    print("  • Marsupial limbs, bacterial herds, AI attractors: all spirals")
    print("=" * 70)

if __name__ == "__main__":
    main()
