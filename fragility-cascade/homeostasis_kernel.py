#!/usr/bin/env python3
"""
homeostasis_kernel.py

Unified stability audit across physics, biology, networks, and information theory.
Computes the Restoring Force Index (RFI) and Effective Damping for any value substrate.

Kernel = conserved invariant (energy, set point, fixed point)
Restoring force = -k * (current_state - kernel_state)
Damping = entropy export capacity (thermal dissipation, metabolic rate, error correction)
"""

import math

# Physical constants (SI-like normalized)
PLANCK_CONSTANT = 1.0          # normalized action quantum
BOLTZMANN = 1.0                # normalized entropy constant

class KernelAudit:
    def __init__(self, name, kernel_value, restoring_constant_k, damping_gamma):
        """
        kernel_value: the invariant fixed point (e.g., 1 barrel oil energy content)
        restoring_constant_k: stiffness of return to kernel (0 = no restore, 1 = perfect)
        damping_gamma: entropy export rate (0 = no dissipation, 1 = critical damping)
        """
        self.name = name
        self.x0 = kernel_value
        self.k = restoring_constant_k
        self.gamma = damping_gamma

    def restoring_force(self, current_state):
        """F = -k * (x - x0). Negative pulls back to kernel."""
        return -self.k * (current_state - self.x0)

    def natural_frequency(self):
        """omega_0 = sqrt(k). The system's intrinsic return rate."""
        return math.sqrt(max(0.0, self.k))

    def damping_ratio(self):
        """zeta = gamma / (2 * omega_0). zeta < 1 = underdamped (oscillates), zeta >= 1 = overdamped (stable)."""
        omega0 = self.natural_frequency()
        if omega0 == 0:
            return float('inf')
        return self.gamma / (2.0 * omega0)

    def stability_index(self, current_state, drive_frequency):
        """
        Returns (stability, status).
        stability = 1.0 if drive_freq < omega0 AND damping_ratio >= 1.0 (overdamped).
        decays if drive_freq approaches omega0 (resonance).
        """
        omega0 = self.natural_frequency()
        zeta = self.damping_ratio()
        if omega0 == 0:
            return 0.0, "NO KERNEL — UNSTABLE"

        # Resonance risk: as drive_freq approaches omega0, stability drops
        resonance_risk = 1.0 / (1.0 + abs(omega0 - drive_frequency))
        # Damping benefit: overdamped (zeta >= 1) is stable; underdamped is oscillatory
        damping_benefit = min(1.0, zeta / 1.0)  # zeta=1 is critical

        stability = damping_benefit * resonance_risk

        if stability > 0.8:
            status = "STABLE (overdamped, far from resonance)"
        elif stability > 0.5:
            status = "MARGINAL (underdamped or near resonance)"
        else:
            status = "⚠️ COLLAPSE PRONE (resonant or undamped)"

        return min(1.0, stability), status

    def report(self, current_state, drive_frequency):
        F = self.restoring_force(current_state)
        omega0 = self.natural_frequency()
        zeta = self.damping_ratio()
        stab, status = self.stability_index(current_state, drive_frequency)

        print(f"\n{'='*60}")
        print(f"KERNEL AUDIT: {self.name}")
        print(f"{'='*60}")
        print(f"Kernel (x0)          : {self.x0:.3f}")
        print(f"Current state (x)    : {current_state:.3f}")
        print(f"Restoring force F    : {F:+.3f}  (pulls toward kernel)")
        print(f"Natural freq ω0      : {omega0:.3f}  (intrinsic return rate)")
        print(f"Damping γ            : {self.gamma:.3f}")
        print(f"Damping ratio ζ      : {zeta:.3f}  (>=1 = overdamped, stable)")
        print(f"Drive frequency      : {drive_frequency:.3f}  (AI release cadence)")
        print(f"Stability Index      : {stab:.3f}")
        print(f"Status               : {status}")
        return stab


# Instantiate real-world substrates
def main():
    print("\n" + "="*60)
    print("HOMEOSTASIS KERNEL — Cross-Disciplinary Stability Audit")
    print("="*60)

    # 1. Physical commodity: Barrel of oil (kernel = energy content)
    oil = KernelAudit(
        name="Barrel of Oil (Physical)",
        kernel_value=1.0,           # 1 barrel = 1 unit energy
        restoring_constant_k=0.95,  # very stiff; physics doesn't negotiate
        damping_gamma=1.2           # overdamped; dissipates heat steadily
    )
    oil.report(current_state=1.0, drive_frequency=0.5)  # slow drive

    # 2. Compute token (promise, no kernel)
    compute_token = KernelAudit(
        name="AI Compute Token (Promise)",
        kernel_value=0.0,           # no physical invariant
        restoring_constant_k=0.05,  # very weak; marketing claims drift
        damping_gamma=0.1           # underdamped; no entropy export path
    )
    compute_token.report(current_state=0.8, drive_frequency=6.0)  # fast AI releases

    # 3. Gold ETF (paper claim, thin kernel)
    gold_etf = KernelAudit(
        name="Gold ETF (Paper Claim)",
        kernel_value=0.9,           # loosely tied to physical gold
        restoring_constant_k=0.3,   # weak; redemption delays
        damping_gamma=0.4           # underdamped; market psychology
    )
    gold_etf.report(current_state=0.7, drive_frequency=2.0)

    # 4. Biological metabolic floor (human)
    human_metabolism = KernelAudit(
        name="Human Metabolism (Biological)",
        kernel_value=1.0,           # 100W basal rate
        restoring_constant_k=0.99,  # extremely stiff; homeostasis
        damping_gamma=2.0           # heavily overdamped; robust
    )
    human_metabolism.report(current_state=1.0, drive_frequency=0.1)  # circadian

    print("\n" + "="*60)
    print("DESIGN PRINCIPLE EXTRACTED:")
    print("  Stability requires: k > 0 (kernel), gamma >= omega0 (critical damping).")
    print("  Substrate (oil, metabolism) has high k, high gamma → stable.")
    print("  Promises (tokens, ETFs) have low k, low gamma → collapse-prone.")
    print("="*60)

if __name__ == "__main__":
    main()
