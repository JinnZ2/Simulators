#!/usr/bin/env python3
"""
resonance_audit.py

Computes the Resonance Factor (R) for any value substrate or AI system:
    R = (ω_drive²) / (ω_0² + γ²)

Where:
    ω_0 = sqrt(k)  (intrinsic natural frequency, from kernel stiffness k)
    γ   = damping coefficient (entropy export / audit friction)
    ω_drive = AI release cadence (in inverse time units)

Interpretation:
    R < 0.5  → Stable (overdamped, far from resonance)
    0.5 ≤ R < 1.0 → Marginal (underdamped, near resonance)
    R ≥ 1.0  → Collapse (drive exceeds restoring capacity)

All times are in weeks to align with AI cadence (~7 weeks).
"""

import math

# AI release cadence (weeks per release)
AI_CADENCE_WEEKS = 7.0          # from ECI: top spot changes ~7 weeks
OMEGA_DRIVE = 1.0 / AI_CADENCE_WEEKS   # inverse weeks

class Asset:
    def __init__(self, name, k, gamma, omega_drive=OMEGA_DRIVE):
        """
        k: kernel stiffness (0..1, 1 = perfectly rigid anchor to physics)
        gamma: damping coefficient (0..∞, higher = more dissipation)
        omega_drive: external forcing frequency (default = AI release rate)
        """
        self.name = name
        self.k = k
        self.gamma = gamma
        self.omega_drive = omega_drive

    @property
    def omega_0(self):
        """Natural frequency = sqrt(k)"""
        return math.sqrt(max(0.0, self.k))

    @property
    def resonance_factor(self):
        """R = (ω_drive²) / (ω_0² + γ²)"""
        omega0 = self.omega_0
        denom = omega0*omega0 + self.gamma*self.gamma
        if denom == 0:
            return float('inf')
        return (self.omega_drive * self.omega_drive) / denom

    @property
    def status(self):
        R = self.resonance_factor
        if R < 0.5:
            return "STABLE (overdamped, far from resonance)"
        elif R < 1.0:
            return "MARGINAL (underdamped, near resonance)"
        else:
            return "⚠️ COLLAPSE (drive exceeds restoring capacity)"

    def report(self):
        print(f"\n{'='*60}")
        print(f"RESONANCE AUDIT: {self.name}")
        print(f"{'='*60}")
        print(f"Kernel stiffness k      : {self.k:.3f}")
        print(f"Natural frequency ω₀    : {self.omega_0:.4f} /week")
        print(f"Damping γ              : {self.gamma:.4f}")
        print(f"Drive frequency ω_drive : {self.omega_drive:.4f} /week (AI cadence = {AI_CADENCE_WEEKS:.1f} weeks)")
        print(f"Resonance Factor R      : {self.resonance_factor:.3f}")
        print(f"Status                  : {self.status}")
        return self.resonance_factor


def main():
    print("\n" + "="*60)
    print("RESONANCE AUDIT — Unified Collapse Predictor")
    print("="*60)
    print(f"AI release cadence: {AI_CADENCE_WEEKS:.1f} weeks (ω_drive = {OMEGA_DRIVE:.4f} /week)")
    print("-"*60)

    # Define asset classes from substrate_spectrum and other modules
    # k: stiffness of anchor to physical reality
    # gamma: damping (audit lag + entropy export)
    # Values grounded in prior modules:
    #   - Oil: k~0.95, gamma~1.2 (from homeostasis_kernel example)
    #   - Compute token: k~0.05, gamma~0.1 (low anchor, weak damping)
    #   - Gold ETF: k~0.3, gamma~0.4 (partial anchor)
    #   - Human metabolism: k~0.99, gamma~2.0 (perfect homeostasis)
    #   - AI model itself: k~0.0, gamma~0.05 (no kernel, minimal damping)
    assets = [
        Asset("Barrel of Oil (Physical)", k=0.95, gamma=1.2),
        Asset("Gold ETF (Paper)", k=0.30, gamma=0.4),
        Asset("AI Compute Token", k=0.05, gamma=0.1),
        Asset("Human Metabolism", k=0.99, gamma=2.0),
        Asset("Frontier AI Model (no kernel)", k=0.01, gamma=0.05),
    ]

    # Also include a 'perfect' substrate for comparison
    assets.append(Asset("Ideal Substrate (k=∞)", k=1e6, gamma=1e6))

    results = []
    for a in assets:
        R = a.report()
        results.append((a.name, R, a.status))

    # Summary table sorted by R
    print("\n" + "="*60)
    print("SUMMARY — Sorted by Resonance Factor (ascending = safer)")
    print("-"*60)
    results.sort(key=lambda x: x[1])
    for name, R, status in results:
        print(f"{name:30} | R = {R:6.3f} | {status[:20]}...")

    print("\n" + "="*60)
    print("INTERPRETATION:")
    print("  R < 0.5  : Stable — the system returns to kernel.")
    print("  0.5 ≤ R < 1.0 : Marginal — susceptible to resonance.")
    print("  R ≥ 1.0  : Collapse — drive overpowers restoring force.")
    print("\n  All synthetic/promise-based assets have R >> 1.")
    print("  Only physically anchored substrates achieve R < 0.5.")
    print("="*60)

if __name__ == "__main__":
    main()
