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
