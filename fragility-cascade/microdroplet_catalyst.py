#!/usr/bin/env python3
"""
microdroplet_catalysis.py

Model of spontaneous plastic degradation at microdroplet interfaces.
Maps to Coherens framework:
    - Interface = high‑damping region (γ high)
    - Radical generation = restoring force
    - Plastic = drive (ω) — stubbornness of C‑C bonds
    - Organic acids = lower‑entropy product

This is a phase change driven by geometric confinement.
"""

import math

def radical_generation(interface_curvature: float, oxygen_concentration: float) -> float:
    """
    Hydroxyl radical generation rate at microdroplet interface.
    Higher curvature → more radicals.
    """
    return interface_curvature * oxygen_concentration * 0.5

def bond_break_probability(radical_flux: float, bond_energy: float, temperature: float) -> float:
    """
    Probability of breaking a C‑C bond.
    Radical flux reduces the effective barrier.
    """
    barrier = bond_energy - radical_flux * 0.3
    if barrier < 0:
        return 1.0
    return math.exp(-barrier / (temperature * 0.008314))  # Arrhenius form

def plastic_degradation_rate(radical_flux: float, polymer_length: int) -> float:
    """
    Rate of chain scission.
    Longer chains are more vulnerable (more sites).
    """
    return radical_flux * math.log(polymer_length + 1) * 0.1

def coherens_at_interface(plastic_entropy: float, radical_flux: float) -> float:
    """
    Coherens of the system at the microdroplet interface.
    Higher radical flux → higher coherence (lower entropy).
    """
    return 1.0 / (1.0 + plastic_entropy / max(radical_flux, 0.01))

def main():
    print("\n" + "=" * 70)
    print("MICRODROPLET CATALYSIS — A Coherens Case Study")
    print("=" * 70)

    # CLAIM: the microdroplet Coherens verdict is monotone in `radical`
    # (which rises with curvature and oxygen) and monotone in `temp`.
    # SCOPE: curvature, oxygen in [0, 1]; bond, temp positive.
    # REFUTATION: two scenarios with the same `radical` and `temp` that
    #   produce different Coherens verdicts break the monotonicity claim.
    # UNKNOWNS: the exponent constants in radical_generation are
    #   illustrative; a wet-lab calibration would pin them.
    scenarios = [
        ("Low curvature",   dict(curvature=0.2, oxygen=0.2, bond=4.0, temp=300, length=1000)),
        ("High curvature",  dict(curvature=1.0, oxygen=0.5, bond=4.0, temp=300, length=1000)),
        ("High temperature", dict(curvature=0.5, oxygen=0.3, bond=4.0, temp=350, length=1000)),
    ]

    for name, params in scenarios:
        curvature = params["curvature"]
        oxygen = params["oxygen"]
        bond = params["bond"]
        temp = params["temp"]
        length = params["length"]
        radical = radical_generation(curvature, oxygen)
        prob = bond_break_probability(radical, bond, temp)
        rate = plastic_degradation_rate(radical, length)
        C = coherens_at_interface(0.8, radical)

        print(f"\n{name}:")
        print(f"  Radical flux: {radical:.3f}")
        print(f"  Bond break probability: {prob:.3f}")
        print(f"  Degradation rate: {rate:.3f}")
        print(f"  Coherens at interface: {C:.3f}")
        print(f"  Status: {'RECYCLING' if prob > 0.5 else 'STUBBORN' if prob > 0.1 else 'INERT'}")

    print("\n" + "=" * 70)
    print("DESIGN PRINCIPLE:")
    print("  • Microdroplet interfaces create high‑damping regions.")
    print("  • High curvature → more radicals → restoring force.")
    print("  • Plastic's stubbornness is overcome when radical flux > bond energy.")
    print("  • The phase change is driven by geometric confinement.")
    print("=" * 70)

if __name__ == "__main__":
    main()
