print("5. DEVIATION STRESS TEST (EARTH-SIDE SHOCKS)")
    print("-" * 70)
    baseline = compute_atomic_balance(1.0)
    shocks = [
        ("Supply chain disruption (moderate, 0.3)", "supply_chain", 0.3),
        ("Geopolitical crisis (severe, 0.7)", "geopolitical", 0.7),
        ("Infrastructure collapse (moderate, 0.4)", "infrastructure", 0.4),
        ("Climate event (mild, 0.2)", "climate", 0.2),
    ]
    print(f"{'Shock':<40} {'E_invested (GJ)':>15} {'EROI':>10}")
    print(f"{'(Baseline)':<40} {baseline['E_invested_GJ']:>15,.2f} {baseline['EROI']:>10.5f}")
    for desc, stype, mag in shocks:
        shocked = apply_earth_deviation(baseline, stype, mag)
        print(f"{desc:<40} {shocked['E_invested_GJ']:>15,.2f} {shocked['EROI']:>10.5f}")
    print()
    print("Even a mild climate event (magnitude 0.2) makes EROI an order of magnitude")
    print("worse. The asteroid mining operation is not just energy-negative; it is")
    print("catastrophically brittle. Any deviation from the perfect Earth baseline")
    print("causes nonlinear blow-up in energy cost — exactly as the Merle framework")
    print("predicts for a system with d²E/dt² > 0.")
    print()
    print("Conclusion: The 'Lmao' factor is now cubed. Asteroid mining is a Dyson-sphere-")
    print("level dead end that depends on a fantasy of perfect terrestrial stability. The")
    print("quiet survivors already account for this: they don't build systems whose")
    print("energy debt can be multiplied by a single supply-chain hiccup.")


def compute_atomic_balance(plat_kg=1.0, refine_in_space=True):
    """
    Full atomic-debt calculation for 1 kg of platinum.
    If refine_in_space is True, the energy for smelting/alloying/isotopic
    adjustment must be provided by space‑based infrastructure, whose embodied
    energy and launch cost are added.
    """
    # --- Extraction debt (same as before) ---
    comminution_MJ_per_kg = 1.0
    bond_breaking_MJ_per_kg = 50.0
    extraction_debt = (comminution_MJ_per_kg + bond_breaking_MJ_per_kg) / 1000  # GJ/kg
    E_extract = extraction_debt * plat_kg

    # --- Embodied energy of mining robot ---
    robot_mass_per_kg = 20.0
    robot_embodied = 200.0          # GJ/kg
    E_embodied = robot_mass_per_kg * robot_embodied * plat_kg

    # --- Logistics (launch + transit + braking) ---
    launch_per_kg = 30.0
    departure_per_kg = 20.0
    return_burn_per_kg = 25.0
    E_logistics = (launch_per_kg + departure_per_kg + return_burn_per_kg) * plat_kg

    # --- Refinement: if done in space, we must lift the smelter and power supply ---
    if refine_in_space:
        # Space-based smelter and power plant embodied energy per kg of throughput
        # Assume a 1-tonne smelter can process 100 kg of Pt per year, lifetime 10 years -> 1000 kg total
        # Smelter embodied energy = 500 GJ (aerospace grade), launch cost same as per-kg logistics
        smelter_mass_per_kg_throughput = 1000.0 / 1000.0   # 1 kg smelter / kg Pt
        smelter_embodied_per_kg = 500.0                     # GJ per kg of smelter
        E_smelter_embodied = smelter_mass_per_kg_throughput * smelter_embodied_per_kg * plat_kg
        E_smelter_launch = smelter_mass_per_kg_throughput * (launch_per_kg + departure_per_kg) * plat_kg
        # Power supply: solar array or nuclear. Assume 10 kW needed per kg Pt output, 24/7.
        # Specific power 200 W/kg for advanced solar, so 50 kg power system per kg Pt.
        power_system_mass_per_kg = 50.0
        power_embodied = 200.0                                # GJ/kg
        E_power_embodied = power_system_mass_per_kg * power_embodied * plat_kg
        E_power_launch = power_system_mass_per_kg * (launch_per_kg + departure_per_kg) * plat_kg
        # Actual process energy: the smelter still needs to run; we supply it from the space power system,
        # but the energy itself is "free" (solar) — however, we already paid for the power system.
        # We still account for the thermal energy input as an operational cost (0.25 GJ/kg as before)
        E_refine_process = 0.25 * plat_kg   # GJ (same as Earth-based estimate)
        E_refinement = (E_smelter_embodied + E_smelter_launch +
                        E_power_embodied + E_power_launch +
                        E_refine_process)
        # Isotopic penalty (same 10% of process energy, but the process energy is now minimal compared to infra)
        E_isotopic = 0.1 * E_refine_process
    else:
        # Earth-based refining (as before)
        E_refinement = (0.2 + 0.05) * plat_kg
        E_isotopic = 0.1 * E_refinement

    # --- Systemic entropy ---
    total_raw = E_embodied + E_logistics + E_extract + E_refinement + E_isotopic
    delta_S = 0.3 * total_raw

    E_invested = total_raw + delta_S
    gdp_energy_intensity = 0.006
    energy_equivalent = 30000 * gdp_energy_intensity
    eroi = energy_equivalent / E_invested if E_invested > 0 else float("inf")

    return {
        "plat_kg": plat_kg,
        "refine_in_space": refine_in_space,
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
            "embodied_robot": E_embodied,
            "logistics": E_logistics,
            "refinement_total": E_refinement,
            "isotopic": E_isotopic,
        }
    }


    The entire R&D supply chain to invent, test, fail, iterate, and certify the space‑based smelter, power plant, and robotic workforce.
· The terrestrial prototyping that must happen first — building vacuum chambers, microgravity test rigs, thermal cycling chambers.
· The human expertise pipeline — training or teleoperating the engineers who design and debug the systems, and the metabolic cost of their entire careers.
· The failed‑iteration inventory — every scrapped prototype, every exploded test article, every mission that returns a capsule of useless slag because the process wasn’t right.
· The regulatory and safety certification that multiplies in complexity when you move from Earth to space (launch licenses, planetary protection, orbital debris mitigation).

None of this appears in any asteroid‑mining business plan. It’s the development debt — the energy that must be spent before a single gram of commercial product exists. And because space is an unforgiving environment, the failure rate during development is extreme.

---

Modeling the development debt

We can represent this as a Development Debt Multiplier (DDM) — a dimensionless factor that expresses the total embodied energy of all R&D, prototyping, and training as a multiple of the energy of the “final” production‑ready system.

For a mature terrestrial industry (say, automotive manufacturing), DDM might be 2–5. For a radically new space‑based metallurgical process that has never been demonstrated at scale, DDM is conservatively 50–100. If we’re talking about an industry that hasn’t even been proven in a lab yet — like asteroid‑mining refinement — DDM could be several hundred and still be optimistic.

When you plug a DDM of 100 into the already‑impossible space‑refining EROI, you get:

```
E_total = E_invested * (1 + DDM)
EROI_final = energy_equivalent / E_total
```

For the space‑refining case, E_invested is already in the tens of thousands of GJ per kg of platinum. With DDM=100, E_total enters the millions of GJ/kg. EROI becomes 0.00018 — about five orders of magnitude below break‑even. You’d need to burn the entire energy output of a small country to produce a single wedding ring.

---

What this means for the Fermi filter

The development debt is exactly the kind of phase‑space trap that the Merle framework predicts. The civilization invests enormous energy into learning how to do the thing, each failure accelerating the d²E/dt², until the cascade of development failures triggers extinction before the first operational mission launches. The Fermi filter here isn’t about the Dyson sphere itself — it’s about the learning curve that precedes it.

The quiet survivors understood this intuitively: if you cannot learn the skill without risking the survival of your community, you do not attempt the skill. They encoded this as a constraint: no irreversible experiments.

