#!/usr/bin/env python3
"""
cascade_redesign_vulnerability.py

T_crit — the windows stop closing.
Updated with M_collapse (model degeneration half-life, 18 mo) from 2024–2026
synthetic-feedback studies. The real T_crit is the shorter of (redesign+audit)
and (M_collapse / 2). Result: current AI release cadence already saturates.
"""

import math

# Physical constants (months)
W_REDESIGN = 6.0        # months to redesign downstream layer
A_AUDIT = 9.0           # months to audit a new release
M_COLLAPSE = 18.0       # frontier model degeneration half-life

# Derived T_crit
T_CRIT_OLD = W_REDESIGN + A_AUDIT
T_CRIT_NEW = min(T_CRIT_OLD, M_COLLAPSE / 2.0)


def compute_exposure(release_cadence_months):
    """
    Returns (downstream_exposure, substrate_exposure).
    Downstream: 1.0 if cadence < T_crit (faster than closure), else 0.0.
    Substrate: 0.0 always (decoupling result).
    """
    # Old model (for reference)
    old_exposure = 1.0 if release_cadence_months < T_CRIT_OLD else 0.0
    # New model: stricter threshold
    new_exposure = 1.0 if release_cadence_months < T_CRIT_NEW else 0.0
    # Substrate is invariant
    substrate_exposure = 0.0
    return old_exposure, new_exposure, substrate_exposure


def main():
    print("=" * 72)
    print("CASCADE REDESIGN VULNERABILITY — T_CRIT UPDATED")
    print("=" * 72)
    print(f"W_redesign   = {W_REDESIGN} mo")
    print(f"A_audit      = {A_AUDIT} mo")
    print(f"M_collapse   = {M_COLLAPSE} mo (synthetic-feedback half-life)")
    print(f"T_crit (old) = {T_CRIT_OLD} mo  (redesign + audit)")
    print(f"T_crit (new) = {T_CRIT_NEW} mo  (min(old, M_collapse/2))")
    print("-" * 72)
    print(f"{'Release (mo)':>12} | {'Old Exp':>8} | {'New Exp':>8} | {'Substrate':>10} | Status")
    print("-" * 72)

    # Test cadences from 1 to 24 months
    for cadence in [1, 3, 6, 9, 12, 15, 18, 24]:
        old_e, new_e, sub_e = compute_exposure(cadence)
        if new_e == 1.0:
            status = "⚠️  PERMANENTLY OPEN" if cadence < T_CRIT_NEW else "OPEN"
        else:
            status = "CLOSED (safe)"
        print(f"{cadence:>12} | {old_e:>8.1f} | {new_e:>8.1f} | {sub_e:>10.1f} | {status}")

    print("-" * 72)
    print("\nREFUTATION CHECK:")
    print(f"  If release cadence >= {T_CRIT_NEW:.1f} months, new exposure = 0.0.")
    print(f"  Current frontier cadence (~3–6 mo) is < {T_CRIT_NEW:.1f} mo → saturation at 1.0.")
    print("  Substrate dE/dT = 0.0 (flat). Ground holds; AI runs free without dragging downstream.")
    print("=" * 72)


if __name__ == "__main__":
    main()
