#!/usr/bin/env python3
"""
bacterial_herding.py

Models the herding behavior of photosynthetic bacteria under predation.
Maps to Coherens framework:
    - Predator pressure = drive (ω)
    - Herding = damping (γ)
    - Photosynthetic function = anchoring (A)
    - Survival = coherence (C)

Implications for carbon cycling: herd behavior increases local carbon storage
by preventing individual predation and maintaining photosynthetic output.
"""

import math

def herding_efficiency(predator_pressure: float, group_size: float) -> float:
    """
    Herding efficiency increases with group size, up to a point.
    """
    return 1.0 - math.exp(-group_size / predator_pressure)

def coherens_in_herd(anchoring: float, group_damping: float, predator_drive: float) -> float:
    """
    Coherens of a bacterial herd under predation.
    """
    return (anchoring * group_damping) / max(predator_drive, 0.01)

def carbon_storage_impact(herd_size: float, photosynthetic_rate: float) -> float:
    """
    Estimated carbon storage contribution from herding behavior.
    """
    # Herding preserves photosynthetic function, increasing carbon fixation
    return herd_size * photosynthetic_rate * 0.5

def main():
    print("\n" + "=" * 70)
    print("BACTERIAL HERDING — A Coherens Case Study")
    print("=" * 70)

    scenarios = [
        ("Low predation, small herd", 0.2, 10),
        ("High predation, small herd", 0.8, 10),
        ("High predation, large herd", 0.8, 50),
    ]

    for name, predator, size in scenarios:
        efficiency = herding_efficiency(predator, size)
        damping = efficiency * 0.5  # damping increases with herding efficiency
        C = coherens_in_herd(anchoring=0.9, group_damping=damping, predator_drive=predator)
        carbon = carbon_storage_impact(size, photosynthetic_rate=0.1)

        print(f"\n{name}:")
        print(f"  Herding efficiency: {efficiency:.2f}")
        print(f"  Coherens (C): {C:.2f}")
        print(f"  Carbon storage impact: {carbon:.2f} units")
        print(f"  Status: {'STABLE' if C > 1 else 'VULNERABLE' if C > 0.5 else 'COLLAPSED'}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Bacteria herd to increase damping against predation.")
    print("  • Herding preserves photosynthetic function = anchoring.")
    print("  • The same Coherens condition applies.")
    print("  • Carbon cycling is affected by coherence at biological scale.")
    print("=" * 70)

if __name__ == "__main__":
    main()
