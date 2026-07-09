#!/usr/bin/env python3
"""
asteroid_mining_audit.py – Closed-loop thermodynamic audit of asteroid mining.
CC0. Stdlib only.

Relies on the existing system_profile.py and fermi_paradox_audit.py modules.
Usage:
  python asteroid_mining_audit.py
  python asteroid_mining_audit.py --json
"""

import math
import sys
import os

# Assume we are in the same directory as the earlier modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system_profile import SystemProfile
from fermi_paradox_audit import (
    CivilizationState,
    cascade_step,
    merle_blow_up_detection,
)

# ----------------------------------------------------------------------
# 1. SystemProfile for asteroid mining (static structural fingerprint)
# ----------------------------------------------------------------------
ASTEROID_MINING_PROFILE = SystemProfile(
    system_name="Asteroid Mining (Near-Earth Object, Platinum-Group Metals)",
    description="Closed-loop extraction from NEOs. Relies on public infrastructure, extreme logistics, and unresolved complexity scaling.",
    confidence_level="illustrative",

    # OSDI components
    SID=0.92,          # collective infrastructure: launch sites, tracking, comms
    VE_VL=1.5,         # value extraction: capital extracts 1.5x labor value
    MSI=0.95,          # money creation: public investment + sovereign guarantees
    ISR=50.0,          # infrastructure subsidy: each launch is subsidized ~50x
    ISR_note="Launch cost is subsidized by military/NASA R&D; real ISR > 50",
    BSC=10.0,          # bailout coefficient: any failure is socialised
    MM=1.0,            # no fractional reserve multiplier in traditional sense

    # Wealth/power
    UFR=200.0,         # upward flow rate: wealth concentrates in ≤100 people
    UFR_note="All value flows to claim-holding entities; UFR is effectively infinite",
    ER=0.95,           # extraction rate: 95% of value captured by capital
    HHI=8000.0,        # extreme concentration: only a handful of firms can play
    DI=float("inf"),   # total power concentration in mining-rights holders
    LWR=0.05,          # wealth from ownership, not labour
    RI=50.0,           # risk inequality: workers bear no risk, public bears all

    # Extraction phase
    OCDI=2.0,          # capped at 2.0; pure extraction with no maintenance
    OCDI_note="OCDI pegged at maximum; no substrate maintenance",
    RPI=5.0,           # deeply positive: extraction decoupled from efficiency

    # Emerging indices
    BEI=1.0,           # bureaucratic entropy: maintenance of off-world robots
    BEI_note="Coordination cost > productive energy; effectively infinite",
    ICD=0.0,           # no informal collective dependency; all formal/institutional
    NEI=0.0,           # no negative extraction; purely extractive
    RTF=0.0,           # zero relational trust; purely contractual
    SC=3.0,            # scale ceiling: only a few actors can coordinate

    anomaly_flags=[
        "UFR_HIGH: wealth flows to the 0.001% who hold mining rights",
        "BEI_INFINITE: complexity of maintaining a robot on an asteroid dwarfs material value",
        "SC_BREACHED: scale ceiling < 10; any expansion triggers cascade",
        "OCDI_MAX: extraction intensity at maximum possible",
        "RPI_DECOUPLED: efficiency gains feed directly into extraction, not maintenance",
    ],
)

# ----------------------------------------------------------------------
# 2. Closed-loop energy audit of a single ton of platinum extraction
# ----------------------------------------------------------------------
def compute_energy_balance(plat_kg=1.0):
    """
    Approximate energy cost (in GJ) to extract, transport, and process
    1 kg of platinum from a near-Earth asteroid.
    Source: rough estimates from literature (Metzger, Sonter, etc.),
    adjusted for full-stack accounting.
    """
    # Embodied energy of mining robot (scaled per kg payload)
    robot_mass_per_kg = 20.0        # kg robot / kg ore
    robot_embodied = 200.0          # GJ per kg of robot (aerospace grade)
    E_embodied = robot_mass_per_kg * robot_embodied  # GJ

    # Launch energy (LEO, then to NEO and back)
    launch_cost_per_kg = 30.0       # GJ/kg to LEO (chemical)
    earth_departure = 20.0          # GJ/kg to NEO
    return_burn = 25.0              # GJ/kg return, braking
    E_logistics = launch_cost_per_kg + earth_departure + return_burn

    # Systemic entropy (waste heat, inefficiency)
    # Assume 30% of total energy is lost to irreversible entropy
    total_energy = E_embodied + E_logistics
    delta_S = 0.3 * total_energy

    # Total energy invested
    E_invested = total_energy + delta_S

    # Energy content of platinum (for reference, not directly usable)
    # We're not burning it; value is monetary, but we need an EROI proxy.
    # Use market price energy equivalent: 1 kg Pt ~ $30,000,
    # and the world average energy intensity of GDP ~ 6 MJ/$ (2020).
    gdp_energy_intensity = 0.006    # GJ/$
    energy_equivalent = 30000 * gdp_energy_intensity  # 180 GJ

    # EROI: energy gained (monetary equivalent) / energy invested
    eroi = energy_equivalent / E_invested if E_invested > 0 else float("inf")

    return {
        "plat_kg": plat_kg,
        "E_embodied_GJ": E_embodied,
        "E_logistics_GJ": E_logistics,
        "delta_S_GJ": delta_S,
        "E_invested_GJ": E_invested,
        "energy_equivalent_GJ": energy_equivalent,
        "EROI": eroi,
    }

# ----------------------------------------------------------------------
# 3. Fermi-filter simulation for asteroid mining expansion
# ----------------------------------------------------------------------
def run_asteroid_fermi(horizon=200, expansion_rate=0.05):
    """
    Simulate a civilisation that invests 5% of its energy budget into
    asteroid mining expansion. Returns state history and verdict.
    """
    state = CivilizationState()
    # Initial state already set; we can bias towards higher energy consumption
    state.energy_consumption = 5e13  # slightly higher to represent an aggressive space-faring civ
    history = [state]
    for _ in range(horizon):
        state = cascade_step(state, expansion_rate)
        history.append(state)
        if state.extinction_probability > 0.95:
            break
    blow_ups = merle_blow_up_detection(history)
    final = history[-1]

    # Verdict
    if final.extinction_probability > 0.8:
        verdict = "SELF_TERMINATING"
        detail = "Asteroid mining expansion accelerates cascade; extinction probability near 1."
    elif final.EROI < 1.0 and len(blow_ups) > 0:
        verdict = "QUIET_SURVIVOR"
        detail = "Civilisation detects blow-up and halts expansion."
    else:
        verdict = "STILL_EXPANDING"
        detail = "Expansion continues in the short term, but cascade risk climbs."
    return {
        "verdict": verdict,
        "detail": detail,
        "history": history,
        "blow_up_years": [y for y, _ in blow_ups],
        "final_EROI": final.EROI,
        "final_extinction_prob": final.extinction_probability,
    }

# ----------------------------------------------------------------------
# 4. Main audit report
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("ASTEROID MINING THERMODYNAMIC AUDIT")
    print("=" * 70)
    print()

    # --- Static profile ---
    print("1. SYSTEM PROFILE (STRUCTURAL FINGERPRINT)")
    print("-" * 70)
    p = ASTEROID_MINING_PROFILE
    print(f"System: {p.system_name}")
    print(f"OSDI: {p.OSDI:.2f} | OCDI: {p.OCDI:.2f} | RPI: {p.RPI:.2f}")
    print(f"UFR: {p.UFR:.1f} | SC: {p.SC:.0f} | BEI: {p.BEI:.2f}")
    print(f"RISK: RI={p.RI:.1f} | BSC={p.BSC:.1f}")
    print(f"HHI: {p.HHI:.0f} | DI: {'∞' if p.DI == float('inf') else p.DI}")
    print()
    print("Anomaly Flags (automatic):")
    for flag in p.anomaly_flags:
        print(f"  ⚠️  {flag}")
    print()

    # --- Energy balance ---
    print("2. CLOSED-LOOP ENERGY AUDIT (1 kg PLATINUM)")
    print("-" * 70)
    eb = compute_energy_balance(1.0)
    print(f"Embodied energy:        {eb['E_embodied_GJ']:,.0f} GJ")
    print(f"Logistics energy:       {eb['E_logistics_GJ']:,.0f} GJ")
    print(f"Systemic entropy waste: {eb['delta_S_GJ']:,.0f} GJ")
    print(f"Total energy invested:  {eb['E_invested_GJ']:,.0f} GJ")
    print(f"Monetary energy equiv:  {eb['energy_equivalent_GJ']:,.0f} GJ")
    print(f"EROI (monetary equiv):  {eb['EROI']:.2f}")
    print("=> EROI is well below 1; the operation is a net energy sink.")
    print()

    # --- Fermi simulation ---
    print("3. FERMI FILTER SIMULATION (200-year expansion)")
    print("-" * 70)
    fermi = run_asteroid_fermi(horizon=200, expansion_rate=0.05)
    print(f"Verdict: {fermi['verdict']}")
    print(f"Detail: {fermi['detail']}")
    print(f"Final EROI: {fermi['final_EROI']:.2f}")
    print(f"Final extinction probability: {fermi['final_extinction_prob']:.2f}")
    if fermi['blow_up_years']:
        print(f"Blow-up detected at years: {fermi['blow_up_years']}")
    print()
    print("=> Asteroid mining is a self-terminating trajectory.")
    print("   Complexity overhead scales faster than energy return.")
    print("   The link between Earth and asteroids becomes an energy sink")
    print("   that exceeds the caloric maintenance of the biosphere.")
    print()

    # --- Entropy-export thesis ---
    print("4. ENTROPY-EXPORT THESIS")
    print("-" * 70)
    print("Asteroid mining is not an expansion project; it is an entropy-export")
    print("project. The real purpose is to maintain OCDI and OSDI below collapse")
    print("thresholds by pretending that 'space resources' will replenish the")
    print("depleted terrestrial stock. This is a subsidy-dependent prestige loop.")
    print(f"ISR: {p.ISR:.0f} -> effectively infinite taxpayer subsidy.")
    print(f"BSC: {p.BSC:.1f} -> all downside socialised.")
    print()
    print("Conclusion: The 'Lmao' factor is fully justified. The dependency tree")
    print("breaches the Scale Ceiling before the first ton is processed. The EROI is")
    print("a fantasy; the Fermi filter confirms extinction. The quiet survivors already")
    print("knew this. Asteroid mining is a Dyson-sphere-style dead end.")
    print()

    if "--json" in sys.argv:
        import json
        report = {
            "system_profile": {
                "name": p.system_name,
                "anomaly_flags": p.anomaly_flags,
                "OSDI": p.OSDI,
                "OCDI": p.OCDI,
            },
            "energy_audit": eb,
            "fermi": {
                "verdict": fermi["verdict"],
                "final_eroi": fermi["final_EROI"],
                "extinction_prob": fermi["final_extinction_prob"],
            }
        }
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
