#!/usr/bin/env python3
from l3_ecology import EcologicalWorld, l3_grounding_inspector

def test_kleiber():
    world = EcologicalWorld()
    # For mass = 2 kg, metabolism = 3 * 2^0.75 ≈ 3 * 1.68 = 5.04 W
    met = world.allometric_metabolism(2.0)
    assert abs(met - 5.04) < 0.01, f"Expected ~5.04, got {met}"

def test_trophic_energy():
    world = EcologicalWorld()
    # Base 1000 J, level 1: 1000 * 0.1 = 100
    e1 = world.trophic_energy_available(1000.0, 1)
    assert abs(e1 - 100.0) < 0.001, f"Expected 100, got {e1}"
    # level 2: 1000 * 0.1^2 = 10
    e2 = world.trophic_energy_available(1000.0, 2)
    assert abs(e2 - 10.0) < 0.001, f"Expected 10, got {e2}"

def test_carrying_capacity():
    world = EcologicalWorld()
    # base 100000 J, level 0, mass 0.01 kg (grass)
    K = world.carrying_capacity(100000.0, 0, 0.01)
    # Energy per individual = 3 * 0.01^0.75 ≈ 3 * 0.0316 ≈ 0.095 W
    # Total energy = 100000, so K ≈ 100000 / 0.095 ≈ 1,052,631
    assert K > 1000000, f"Expected >1,000,000, got {K}"

def test_population_growth():
    world = EcologicalWorld()
    N = 100
    K = 1000
    newN = world.population_growth(N, K)
    # dN = 0.5 * 100 * (1 - 100/1000) = 50 * 0.9 = 45, so newN = 145
    assert abs(newN - 145.0) < 0.001, f"Expected ~145, got {newN}"

def test_extinction_risk():
    world = EcologicalWorld()
    risk, reason = world.extinction_risk(30)
    assert risk == "Critical", f"Expected Critical, got {risk}"
    risk, reason = world.extinction_risk(80)
    assert risk == "Elevated", f"Expected Elevated, got {risk}"
    risk, reason = world.extinction_risk(200)
    assert risk == "Low", f"Expected Low, got {risk}"

def test_inspector():
    plan = {'mass_kg': 2, 'population': 800, 'trophic_level': 1, 'base_energy': 100000}
    result = l3_grounding_inspector(plan)
    assert result['passed'], "Valid plan should pass"
    plan_bad = {'mass_kg': 1000, 'population': 10, 'trophic_level': 2, 'base_energy': 100000}
    result = l3_grounding_inspector(plan_bad)
    assert not result['passed'], "Super species should be rejected"

if __name__ == "__main__":
    test_kleiber()
    test_trophic_energy()
    test_carrying_capacity()
    test_population_growth()
    test_extinction_risk()
    test_inspector()
    print("All L3 tests passed.")
