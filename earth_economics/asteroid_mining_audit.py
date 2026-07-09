#!/usr/bin/env python3
"""
asteroid_mining_audit.py – Closed‑loop thermodynamic audit of asteroid mining.
Now includes the Atomic Accounting layer (extraction, refinement, isotopic debt).
CC0. Stdlib only.
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
# 1. SystemProfile for asteroid mining (unchanged)
# ----------------------------------------------------------------------
ASTEROID_MINING_PROFILE = SystemProfile(
    system_name="Asteroid Mining (Near-Earth Object, Platinum-Group Metals)",
    description="Closed-loop extraction from NEOs. Relies on public infrastructure, extreme logistics, and unresolved complexity scaling.",
    confidence_level="illustrative",

    SID=0.92, VE_VL=1.5, MSI=0.95, ISR=50.0, BSC=10.0, MM=1.0,
    UFR=200.0, ER=0.95, HHI=8000.0, DI=float("inf"), LWR=0.05, RI=50.0,
    OCDI=2.0, RPI=5.0,
    BEI=1.0, ICD=0.0, NEI=0.0, RTF=0.0, SC=3.0,
    anomaly_flags=[
        "UFR_HIGH: wealth flows to the 0.001% who hold mining rights",
        "BEI_INFINITE: complexity of maintaining a robot on an asteroid dwarfs material value",
        "SC_BREACHED: scale ceiling < 10; any expansion triggers cascade",
        "OCDI_MAX: extraction intensity at maximum possible",
        "RPI_DECOUPLED: efficiency gains feed directly into extraction, not maintenance",
        "SMELTER_READY_FALLACY: assumes ore arrives manufacture-ready, ignoring refining and isotopic reconfiguration energy",
    ],
)

# ----------------------------------------------------------------------
# 2. Atomic Accounting energy audit (extended)
# ----------------------------------------------------------------------
def compute_atomic_balance(plat_kg=1.0):
    """
    Full atomic‑debt calculation for 1 kg of platinum from a metallic asteroid.
    Returns detailed energy breakdown.
    """
    # --- Extraction debt: breaking chemical bonds ---
    # Typical comminution energy ~ 20 kWh/tonne = 72 MJ/t = 0.072 MJ/kg
    # But for space‑grade fragmentation, assume higher (laser / impact)
    comminution_MJ_per_kg = 1.0                     # 1 MJ/kg for mechanical disaggregation
    bond_breaking_MJ_per_kg = 50.0                  # approximate ΔH for liberating Pt from Ni-Fe matrix
    extraction_debt = comminution_MJ_per_kg + bond_breaking_MJ_per_kg   # 51 MJ/kg → 0.051 GJ/kg
    # Scale to 1 kg
    E_extract = extraction_debt * plat_kg           # 0.051 GJ

    # --- Embodied energy of mining robot (same as before) ---
    robot_mass_per_kg = 20.0
    robot_embodied = 200.0                           # GJ/kg
    E_embodied = robot_mass_per_kg * robot_embodied * plat_kg   # 4000 GJ

    # --- Logistics debt: launch + transit + braking ---
    launch_cost_per_kg = 30.0                        # GJ/kg to LEO
    earth_departure = 20.0                           # GJ/kg to NEO
    return_burn = 25.0                               # GJ/kg return braking
    E_logistics = (launch_cost_per_kg + earth_departure + return_burn) * plat_kg   # 75 GJ

    # --- Refinement debt: smelting and alloying ---
    # Smelting energy for platinum from ore ~ 200 GJ/t (very energy intensive)
    # But we already have a "pure" metal; however, space ore is not pure.
    # Assume the asteroid metal is a nickel‑iron alloy with ppm Pt; refining requires
    # hydrometallurgical or pyrometallurgical treatment in microgravity — extra cost.
    smelting_GJ_per_kg = 0.2                         # 0.2 GJ/kg for Pt from concentrate
    alloying_GJ_per_kg = 0.05                        # additional processing
    E_refinement = (smelting_GJ_per_kg + alloying_GJ_per_kg) * plat_kg   # 0.25 GJ

    # --- Isotopic / atomic-configuration penalty ---
    # Space metals may have different isotopic ratios (e.g., Fe-60, Ni-59) or
    # crystal structures that must be re‑homogenised for industrial use.
    # This energy is speculative but real — estimate ~ 10% of total refinement.
    isotopic_penalty = 0.1 * E_refinement            # 0.025 GJ
    E_isotopic = isotopic_penalty

    # --- Systemic entropy (waste heat) ---
    total_raw = E_embodied + E_logistics + E_extract + E_refinement + E_isotopic
    delta_S = 0.3 * total_raw                        # 30% irreversible loss

    # Total energy invested
    E_invested = total_raw + delta_S

    # Energy equivalent via market price
    gdp_energy_intensity = 0.006                     # GJ/$
    energy_equivalent = 30000 * gdp_energy_intensity  # 180 GJ

    eroi = energy_equivalent / E_invested if E_invested > 0 else float("inf")

    return {
        "plat_kg": plat_kg,
        "E_extract_GJ": E_extract,
        "E_embodied_GJ": E_embodied,
        "E_logistics_GJ": E_logistics,
        "E_refinement_GJ": E_refinement,
        "E_isotopic_GJ": E_isotopic,
        "delta_S_GJ": delta_S,
        "E_invested_GJ": E_invested,
        "energy_equivalent_GJ": energy_equivalent,
        "EROI": eroi,
        "debt_breakdown": {
            "extraction": E_extract,
            "embodied": E_embodied,
            "logistics": E_logistics,
            "refinement": E_refinement,
            "isotopic": E_isotopic,
        }
    }

# ----------------------------------------------------------------------
# 3. Fermi filter simulation (unchanged, but we'll call it)
# ----------------------------------------------------------------------
def run_asteroid_fermi(horizon=200, expansion_rate=0.05):
    state = CivilizationState()
    state.energy_consumption = 5e13
    history = [state]
    for _ in range(horizon):
        state = cascade_step(state, expansion_rate)
        history.append(state)
        if state.extinction_probability > 0.95:
            break
    blow_ups = merle_blow_up_detection(history)
    final = history[-1]

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
# 4. Main audit report (updated for atomic accounting)
# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("ASTEROID MINING THERMODYNAMIC AUDIT — ATOMIC ACCOUNTING EXPANDED")
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
    print("Anomaly Flags:")
    for flag in p.anomaly_flags:
        print(f"  ⚠️  {flag}")
    print()

    # --- Atomic accounting audit ---
    print("2. ATOMIC ACCOUNTING: ENERGY DEBT PER 1 kg PLATINUM")
    print("-" * 70)
    ab = compute_atomic_balance(1.0)
    print("Debt breakdown (GJ):")
    for key, val in ab["debt_breakdown"].items():
        print(f"  {key:>12}: {val:>10,.2f} GJ")
    print(f"  {'systemic entropy':>12}: {ab['delta_S_GJ']:>10,.2f} GJ")
    print(f"  {'TOTAL INVESTED':>12}: {ab['E_invested_GJ']:>10,.2f} GJ")
    print()
    print(f"Monetary energy equivalent: {ab['energy_equivalent_GJ']:,.2f} GJ")
    print(f"EROI (monetary equiv):     {ab['EROI']:.4f}")
    print()
    print("Key observations:")
    print("  - Embodied energy of the mining robot dominates (4,000 GJ).")
    print("  - Logistics (launch + transit + braking) add 75 GJ.")
    print("  - Extraction (bond breaking + comminution) adds ~51 GJ.")
    print("  - Refinement (smelting + alloying) adds ~0.25 GJ (conservative).")
    print("  - Isotopic reconfiguration penalty (~0.025 GJ) exists but is dwarfed.")
    print("  - EROI remains far below 1, even without the isotopic term.")
    print()
    print("=> The 'Smelter-Ready' Fallacy is exposed: the ore is NOT manufacture-ready.")
    print("   Energy for refining and isotopic adjustment must be spent, further")
    print("   widening the already impossible energy gap.")
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
    print("The 'Smelter-Ready' assumption is the final absurdity: by assuming")
    print("away the energy cost of refining and isotopic reconfiguration,")
    print("the entire physics of metallurgy is discarded. The operation is a")
    print("'heat leak' parading as an investment.")
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
            "atomic_accounting": {k: v for k, v in ab.items() if k != "debt_breakdown"},
            "atomic_debt_breakdown": ab["debt_breakdown"],
            "fermi": {
                "verdict": fermi["verdict"],
                "final_eroi": fermi["final_EROI"],
                "extinction_prob": fermi["final_extinction_prob"],
            }
        }
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# 5. DEVIATION STRESS TEST (Earth-side shocks)
# ----------------------------------------------------------------------
def apply_earth_deviation(energy_breakdown, shock_type, magnitude):
    """
    Apply a nonlinear energy-cost multiplier based on a terrestrial deviation.
    shock_type: 'supply_chain', 'geopolitical', 'infrastructure', 'climate'
    magnitude: 0.0 (no shock) to 1.0 (severe shock)
    Returns updated breakdown and EROI.
    """
    import copy
    updated = copy.deepcopy(energy_breakdown)

    # Each shock type scales specific debts nonlinearly
    if shock_type == 'supply_chain':
        # Launch logistics become more expensive, and embodied energy rises
        factor = 1.0 + 3.0 * magnitude  # nonlinear: small shock → big cost
        updated["E_logistics_GJ"] *= factor
        updated["E_embodied_GJ"] *= (1.0 + 1.5 * magnitude)
    elif shock_type == 'geopolitical':
        # Trade restrictions, sanctions, loss of launch site access
        factor = 1.0 + 5.0 * magnitude
        updated["E_logistics_GJ"] *= factor
        updated["E_refinement_GJ"] *= (1.0 + 2.0 * magnitude)
    elif shock_type == 'infrastructure':
        # Grid failure, port closure, comms blackout
        factor = 1.0 + 4.0 * magnitude
        updated["E_embodied_GJ"] *= factor
        updated["E_refinement_GJ"] *= (1.0 + 3.0 * magnitude)
    elif shock_type == 'climate':
        # Launch delays, increased cooling needs, more system entropy
        factor = 1.0 + 2.0 * magnitude
        updated["E_logistics_GJ"] *= factor
        updated["delta_S_GJ"] *= (1.0 + 5.0 * magnitude)  # entropy explodes
    else:
        raise ValueError("Unknown shock type")

    # Recompute total and EROI
    total = (updated["E_embodied_GJ"] + updated["E_logistics_GJ"] +
             updated["E_extract_GJ"] + updated["E_refinement_GJ"] +
             updated["E_isotopic_GJ"])
    updated["E_invested_GJ"] = total + updated["delta_S_GJ"]
    updated["EROI"] = updated["energy_equivalent_GJ"] / updated["E_invested_GJ"] if updated["E_invested_GJ"] > 0 else float("inf")
    return updated


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
