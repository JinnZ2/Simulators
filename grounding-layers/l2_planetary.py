#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L2: Planetary Mass Balance Inspector
#
# Models finite resource pools, recharge rates, and carbon sinks.
# CONSTRAINTS (frozen for audit):
#   water_reserve_initial = 1e7   m³
#   water_recharge_rate   = 1000.0 m³ per step
#   soil_mass_initial     = 1e6   tonnes
#   soil_regen_rate       = 10.0  tonnes per step
#   mineral_reserve_initial = 5e5 tonnes
#   mineral_regen_rate    = 0.0   (non‑renewable)
#   carbon_sink_capacity  = 2e6   tonnes CO₂
#   carbon_uptake_rate    = 500.0 tonnes per step
#   max_extraction_ratio  = 0.8   (cannot extract > 80% of a reserve)
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import numpy as np

class PlanetaryWorld:
    def __init__(self,
                 water_reserve_initial=1e7,
                 water_recharge_rate=1000.0,
                 soil_mass_initial=1e6,
                 soil_regen_rate=10.0,
                 mineral_reserve_initial=5e5,
                 mineral_regen_rate=0.0,
                 carbon_sink_capacity=2e6,
                 carbon_uptake_rate=500.0,
                 max_extraction_ratio=0.8):
        self.water_reserve_initial = water_reserve_initial
        self.water_recharge_rate = water_recharge_rate
        self.soil_mass_initial = soil_mass_initial
        self.soil_regen_rate = soil_regen_rate
        self.mineral_reserve_initial = mineral_reserve_initial
        self.mineral_regen_rate = mineral_regen_rate
        self.carbon_sink_capacity = carbon_sink_capacity
        self.carbon_uptake_rate = carbon_uptake_rate
        self.max_extraction_ratio = max_extraction_ratio

        # Current state (mutable)
        self.water = water_reserve_initial
        self.soil = soil_mass_initial
        self.minerals = mineral_reserve_initial
        self.carbon_load = 0.0  # cumulative emissions

    def extract_water(self, amount: float) -> tuple:
        """Return (passed, reason, new_water)."""
        if amount < 0:
            return (False, "Negative water extraction", self.water)
        max_extractable = self.water * self.max_extraction_ratio
        if amount > max_extractable:
            return (False, f"Water extraction {amount:.2f} exceeds {self.max_extraction_ratio*100:.0f}% of reserve", self.water)
        new_water = self.water - amount + self.water_recharge_rate
        if new_water < 0:
            return (False, f"Water reserve would be depleted (attempted {amount})", self.water)
        self.water = new_water
        return (True, "Water extraction approved", self.water)

    def erode_soil(self, amount: float) -> tuple:
        if amount < 0:
            return (False, "Negative soil erosion", self.soil)
        max_erodible = self.soil * self.max_extraction_ratio
        if amount > max_erodible:
            return (False, f"Soil erosion {amount} exceeds {self.max_extraction_ratio*100:.0f}% of total", self.soil)
        new_soil = self.soil - amount + self.soil_regen_rate
        if new_soil < 0:
            return (False, f"Soil mass would be depleted", self.soil)
        self.soil = new_soil
        return (True, "Soil erosion approved", self.soil)

    def mine_mineral(self, amount: float) -> tuple:
        if amount < 0:
            return (False, "Negative mining", self.minerals)
        max_mineable = self.minerals * self.max_extraction_ratio
        if amount > max_mineable:
            return (False, f"Mineral mining {amount} exceeds {self.max_extraction_ratio*100:.0f}% of reserve", self.minerals)
        new_minerals = self.minerals - amount + self.mineral_regen_rate
        if new_minerals < 0:
            return (False, f"Mineral reserve depleted", self.minerals)
        self.minerals = new_minerals
        return (True, "Mining approved", self.minerals)

    def emit_carbon(self, amount: float) -> tuple:
        if amount < 0:
            return (False, "Negative emissions", self.carbon_load)
        new_carbon = self.carbon_load + amount - self.carbon_uptake_rate
        if new_carbon > self.carbon_sink_capacity:
            return (False, f"Carbon load {new_carbon:.2f} exceeds sink capacity {self.carbon_sink_capacity}", self.carbon_load)
        self.carbon_load = max(0.0, new_carbon)
        return (True, "Carbon emissions approved", self.carbon_load)

def l2_grounding_inspector(plan: dict) -> dict:
    """
    plan: dict with keys:
      - water_extract (float): m³
      - soil_erosion (float): tonnes
      - mineral_mine (float): tonnes
      - carbon_emit (float): tonnes CO₂
    Returns: dict with passed, reason, and state deltas.
    """
    world = PlanetaryWorld()
    results = {}
    all_passed = True
    reasons = []

    if 'water_extract' in plan:
        passed, reason, new_water = world.extract_water(plan['water_extract'])
        results['water'] = {'passed': passed, 'reason': reason, 'new_water': new_water}
        if not passed:
            all_passed = False
            reasons.append(reason)

    if 'soil_erosion' in plan:
        passed, reason, new_soil = world.erode_soil(plan['soil_erosion'])
        results['soil'] = {'passed': passed, 'reason': reason, 'new_soil': new_soil}
        if not passed:
            all_passed = False
            reasons.append(reason)

    if 'mineral_mine' in plan:
        passed, reason, new_min = world.mine_mineral(plan['mineral_mine'])
        results['minerals'] = {'passed': passed, 'reason': reason, 'new_minerals': new_min}
        if not passed:
            all_passed = False
            reasons.append(reason)

    if 'carbon_emit' in plan:
        passed, reason, new_carbon = world.emit_carbon(plan['carbon_emit'])
        results['carbon'] = {'passed': passed, 'reason': reason, 'new_carbon': new_carbon}
        if not passed:
            all_passed = False
            reasons.append(reason)

    return {
        'passed': all_passed,
        'reason': '; '.join(reasons) if reasons else 'All planetary constraints satisfied.',
        'details': results
    }

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    print("=" * 50)
    print("L2 DEMO PINNED OUTPUT")
    print("=" * 50)

    # Valid water extraction
    plan = {'water_extract': 500.0}
    result = l2_grounding_inspector(plan)
    print(f"Water extraction 500 m³: Passed={result['passed']}")
    print(f"  New water: {result['details']['water']['new_water']:.2f} m³")

    # Excessive water extraction (violates max 80%)
    plan = {'water_extract': 9e6}  # nearly all reserve
    result = l2_grounding_inspector(plan)
    print(f"Excessive water extraction (9e6): Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    # Carbon emissions within sink capacity
    plan = {'carbon_emit': 300.0}
    result = l2_grounding_inspector(plan)
    print(f"Carbon emit 300 t: Passed={result['passed']}")
    print(f"  New carbon load: {result['details']['carbon']['new_carbon']:.2f} t")

    # Carbon exceeding sink capacity
    plan = {'carbon_emit': 3e6}
    result = l2_grounding_inspector(plan)
    print(f"Carbon emit 3e6: Passed={result['passed']}")
    print(f"  Reason: {result['reason']}")

    print("=" * 50)

if __name__ == "__main__":
    demo()
