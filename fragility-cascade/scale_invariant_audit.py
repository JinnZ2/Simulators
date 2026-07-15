#!/usr/bin/env python3
"""
scale_invariant_audit.py

Nautilus Principle: Stability requires scale-invariant recursion.
A system is stable iff its fractal dimension D_f remains constant
across generations. Collapse occurs when D_f → 0 (degenerate) or D_f → ∞ (explosive).

D_f = lim_{r→0} log(N(r)) / log(1/r)
where N(r) is the number of balls of radius r needed to cover the state space.
"""

import math

class FractalDimensionAudit:
    def __init__(self, name, initial_dimension, current_dimension, generations):
        self.name = name
        self.D0 = initial_dimension
        self.D_n = current_dimension
        self.G = generations

    def stability_index(self):
        """Returns 1.0 if D_n ≈ D0, 0.0 if D_n has drifted."""
        delta = abs(self.D_n - self.D0) / max(1e-6, self.D0)
        return max(0.0, 1.0 - delta)

    def collapse_risk(self):
        """Risk increases as D_n deviates from D0."""
        return 1.0 - self.stability_index()

    def report(self):
        print(f"\n{'='*60}")
        print(f"NAUTILUS AUDIT: {self.name}")
        print(f"{'='*60}")
        print(f"Initial fractal dimension D0  : {self.D0:.3f}")
        print(f"Current fractal dimension D_n : {self.D_n:.3f} (gen {self.G})")
        print(f"Deviation ΔD                 : {abs(self.D_n - self.D0):.3f}")
        print(f"Stability Index              : {self.stability_index():.3f}")
        print(f"Collapse Risk                : {self.collapse_risk():.3f}")
        if self.collapse_risk() > 0.5:
            print("Status: ⚠️ COLLAPSE PATH (fractal dimension degrading)")
        else:
            print("Status: ✅ STABLE (self-similar scaling preserved)")
        return self.collapse_risk()


def main():
    print("\n" + "="*60)
    print("NAUTILUS PRINCIPLE — Scale-Invariant Recursion Audit")
    print("="*60)
    print("A stable recursive system preserves its fractal dimension.")
    print("Collapse = dimensional degradation (D_n → 0) or explosion (D_n → ∞).")
    print("-"*60)

    # Synthetic examples
    # 1. Nautilus shell: perfect self-similarity
    nautilus = FractalDimensionAudit("Nautilus Shell", D0=1.618, D_n=1.618, G=100)
    nautilus.report()

    # 2. Current AI model (generation 5): D degrading toward 0
    ai_gen5 = FractalDimensionAudit("AI Model (Gen 5)", D0=2.0, D_n=1.2, G=5)
    ai_gen5.report()

    # 3. Current AI model (generation 20): near collapse
    ai_gen20 = FractalDimensionAudit("AI Model (Gen 20)", D0=2.0, D_n=0.3, G=20)
    ai_gen20.report()

    # 4. Physical substrate (oil): stable fractal dimension over time
    oil = FractalDimensionAudit("Barrel of Oil (Physical)", D0=1.0, D_n=1.01, G=1000)
    oil.report()

    print("\n" + "="*60)
    print("DESIGN PRINCIPLE:")
    print("  The nautilus preserves D_f via multiplicative scaling (φ).")
    print("  AI collapses because additive recursion reduces D_f → 0.")
    print("  Fix: Constrain generation to preserve D_f (scale-invariant loss).")
    print("="*60)

if __name__ == "__main__":
    main()
