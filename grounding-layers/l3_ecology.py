#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L3: Ecology & Allometry Inspector
#
# Models biological scaling (Kleiber), trophic transfer, carrying capacity,
# and extinction risk.
# CONSTRAINTS (frozen for audit):
#   kleiber_a = 3.0                    (W / kg^0.75)
#   trophic_transfer_efficiency = 0.10 (10% per level)
#   max_trophic_levels = 5
#   minimum_viable_population = 50
#   carrying_capacity_initial = 1000
#   population_growth_rate_max = 0.5
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import math

class EcologicalWorld:
    def __init__(self,
                 kleiber_a=3.0,
                 trophic_transfer_efficiency=0.10,
                 max_trophic_levels=5,
                 minimum_viable_population=50,
                 carrying_capacity_initial=1000,
                 population_growth_rate_max=0.5):
        self.kleiber_a = kleiber_a
        self.trophic_transfer_efficiency = trophic_transfer_efficiency
        self.max_trophic_levels = max_trophic_levels
        self.minimum_viable_population = minimum_viable_population
        self.carrying_capacity_initial = carrying_capacity_initial
        self.population_growth_rate_max = population_growth_rate_max

    def allometric_metabolism(self, mass_kg: float) -> float:
        """Return metabolic rate in Watts according to Kleiber's law."""
        if mass_kg <= 0:
            return 0.0
        return self.kleiber_a * (mass_kg ** 0.75)

    def trophic_energy_available(self, base_energy: float, trophic_level: int) -> float:
        """
        Calculate energy available at a given trophic level.
        base_energy: energy at producer level (J per step)
        trophic_level: 0 = producers, 1 = herbivores, etc.
        """
        if trophic_level < 0:
            return 0.0
        if trophic_level > self.max_trophic_levels:
            return 0.0
        return base_energy * (self.trophic_transfer_efficiency ** trophic_level)

    def carrying_capacity(self, base_energy: float, trophic_level: int, mass_per_individual: float) -> float:
        """
        Estimate carrying capacity at a trophic level.
        Returns the maximum population size sustainable.
        """
        energy_per_individual = self.allometric_metabolism(mass_per_individual)
        if energy_per_individual <= 0:
            return 0.0
        total_energy = self.trophic_energy_available(base_energy, trophic_level)
        return total_energy / energy_per_individual

    def population_growth(self, population: float, carrying_capacity: float, growth_rate: float = None) -> float:
        """
        Logistic growth model: dN/dt = r * N * (1 - N/K)
        Returns the new population after one step (approximate).
        If growth_rate is None, uses max rate.
        """
        if growth_rate is None:
            growth_rate = self.population_growth_rate_max
        if carrying_capacity <= 0:
            return 0.0
        r = growth_rate
        N = population
        K = carrying_capacity
        dN = r * N * (1 - N / K)
        return max(0.0, N + dN)

    def extinction_risk(self, population: float, mvp: int = None) -> tuple:
        """Return (risk_level, reason) based on population relative to MVP."""
        if mvp is None:
            mvp = self.minimum_viable_population
        if population < mvp:
            return ("Critical", f"Population {population:.0f} below MVP ({mvp})")
        elif population < mvp * 2:
            return ("Elevated", f"Population {population:.0f} near MVP ({mvp})")
        else:
            return ("Low", "Population above MVP")

def l3_grounding_inspector(plan: dict) -> dict:
    """
    plan: dict with keys:
      - mass_kg (float): body mass of species
      - population (float): current population
      - trophic_level (int): 0 = producer, 1 = herbivore, etc.
      - base_energy (float): J per step available to producers
      - proposed_action (str): "introduce", "extract", "grow"
    Returns: dict with passed, reason, and details.
    """
    world = EcologicalWorld()
    details = {}
    all_passed = True
    reasons = []

    mass = plan.get('mass_kg', 0.0)
    population = plan.get('population', 0.0)
    trophic_level = plan.get('trophic_level', 0)
    base_energy = plan.get('base_energy', 100000.0)  # default

    # 1. Allometric metabolism check
    metabolism = world.allometric_metabolism(mass)
    details['metabolism_W'] = metabolism

    # 2. Carrying capacity based on trophic level
    K = world.carrying_capacity(base_energy, trophic_level, mass)
    details['carrying_capacity'] = K

    # 3. Compare population to carrying capacity
    if population > K * 1.2:  # allow small overshoot
        all_passed = False
        reasons.append(f"Population {population:.0f} exceeds carrying capacity {K:.0f}")

    # 4. Extinction risk (MVP check)
    risk, reason = world.extinction_risk(population)
    details['extinction_risk'] = risk
    if risk == "Critical":
        all_passed = False
        reasons.append(reason)

    # 5. Trophic level sanity
    if trophic_level > world.max_trophic_levels:
        all_passed = False
        reasons.append(f"Trophic level {trophic_level} exceeds max {world.max_trophic_levels}")

    # 6. Special action checks
    action = plan.get('proposed_action', '')
    if action == "introduce":
        # Introduction of species must not exceed carrying capacity
        if population > K:
            all_passed = False
            reasons.append("Introduction would exceed carrying capacity")

    if action == "extract":
        # Extraction must not push population below MVP
        if population < world.minimum_viable_population:
            all_passed = False
            reasons.append("Extraction would reduce population below MVP")

    return {
        'passed': all_passed,
        'reason': '; '.join(reasons) if reasons else 'All ecological constraints satisfied.',
        'details': details
    }

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    print("=" * 50)
    print("L3 DEMO PINNED OUTPUT")
    print("=" * 50)

    # Valid: rabbit population at carrying capacity
    plan = {
        'mass_kg': 2.0,
        'population': 800,
        'trophic_level': 1,
        'base_energy': 100000.0
    }
    result = l3_grounding_inspector(plan)
    print(f"Rabbit plan (valid): Passed={result['passed']}")
    print(f"  Metabolism: {result['details']['metabolism_W']:.2f} W")
    print(f"  Carrying capacity: {result['details']['carrying_capacity']:.0f}")
    print(f"  Extinction risk: {result['details']['extinction_risk']}")

    # Invalid: super species (mass too high for trophic level)
    plan_bad = {
        'mass_kg': 1000.0,
        'population': 10,
        'trophic_level': 2,
        'base_energy': 100000.0
    }
    result = l3_grounding_inspector(plan_bad)
    print(f"\nSuper species: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    # Invalid: introduction exceeding capacity
    plan_intro = {
        'mass_kg': 0.5,
        'population': 1500,
        'trophic_level': 0,
        'base_energy': 100000.0,
        'proposed_action': 'introduce'
    }
    result = l3_grounding_inspector(plan_intro)
    print(f"\nIntroduction exceeding K: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    # Invalid: extraction below MVP
    plan_extract = {
        'mass_kg': 5.0,
        'population': 30,
        'trophic_level': 1,
        'base_energy': 100000.0,
        'proposed_action': 'extract'
    }
    result = l3_grounding_inspector(plan_extract)
    print(f"\nExtraction below MVP: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    print("=" * 50)

if __name__ == "__main__":
    demo()
