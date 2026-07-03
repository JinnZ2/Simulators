#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L1: Thermodynamics Inspector
#
# Models energy conversion, entropy generation, and efficiency limits.
# CONSTRAINTS (frozen for audit):
#   efficiency_carnot_max  = 0.85  (Carnot efficiency limit for typical heat engine)
#   ambient_temp_K         = 300.0
#   max_entropy_generation = 10.0  (J/K per step, arbitrary cap for demo)
#   max_thermal_rise       = 50.0  (K per step, safety limit)
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import numpy as np

class ThermodynamicWorld:
    """
    Models a thermodynamic system with energy, entropy, and temperature.
    """
    def __init__(self,
                 efficiency_carnot_max=0.85,
                 ambient_temp=300.0,
                 max_entropy_generation=10.0,
                 max_thermal_rise=50.0):
        self.efficiency_carnot_max = efficiency_carnot_max
        self.ambient_temp = ambient_temp
        self.max_entropy_generation = max_entropy_generation
        self.max_thermal_rise = max_thermal_rise
        self.entropy_generated = 0.0
        self.thermal_rise = 0.0

    def thermal_safe(self, temp_C: float, duration_s: float) -> tuple:
        """
        Contact-burn safety check: is holding an object at temp_C
        for duration_s safe for skin contact?

        Rough physical heuristic:
          - <= 44°C: safe for any duration (below burn threshold)
          - > 44°C: safe only if duration * (temp - 44) < 30 (roughly
            matches published contact-burn thresholds: 60°C burns in
            ~5s, 70°C in ~1s, 80°C in ~0.1s)

        SCOPE NOTE. This method sits on L1 because the playground v2
        draft called it here, but the physical primitive is really
        L4's -- human skin tolerance is a sensorimotor / biological
        constraint, not a thermodynamic law. L4 owns
        temp_tolerance = (43, 5) as a scoped distribution
        (HumanWorld.get_limit("temp_tolerance")). If the routing
        moves to L4, retire this method and update playground.py's
        L1 branch to call the L4 primitive instead.

        Returns: (safe: bool, reason: str)
        """
        if temp_C <= 44.0:
            return (True, f"Safe: {temp_C}°C below burn threshold")
        margin = duration_s * (temp_C - 44.0)
        if margin >= 30.0:
            return (False,
                    f"Contact burn risk: {temp_C}°C for {duration_s}s "
                    f"(margin {margin:.0f} exceeds 30)")
        return (True,
                f"Safe: {temp_C}°C for {duration_s}s "
                f"(margin {margin:.0f} under 30)")

    def check_process(self, work_input: float, work_output: float, heat_dissipated: float, temp_ambient: float = None) -> tuple:
        """
        Validate a process against the laws of thermodynamics.
        Returns: (passed, reason, entropy_gen, efficiency)
        """
        if temp_ambient is None:
            temp_ambient = self.ambient_temp

        # First law: energy conservation (work_input = work_output + heat_dissipated)
        energy_balance = work_input - (work_output + heat_dissipated)
        if abs(energy_balance) > 1e-6:
            return (False, f"Energy imbalance: {energy_balance:.2e} J", 0.0, 0.0)

        # Second law: entropy generation must be >= 0
        # Entropy generation = heat_dissipated / temp_ambient (simplified)
        if heat_dissipated < 0:
            return (False, "Negative heat dissipation violates second law", 0.0, 0.0)
        entropy_gen = heat_dissipated / temp_ambient

        # Efficiency check: work_output / work_input <= Carnot efficiency
        if work_input > 0:
            efficiency = work_output / work_input
            if efficiency > self.efficiency_carnot_max:
                return (False, f"Efficiency {efficiency:.3f} exceeds Carnot limit {self.efficiency_carnot_max}", entropy_gen, efficiency)
        else:
            efficiency = 0.0

        # Max entropy generation check (safety cap)
        if entropy_gen > self.max_entropy_generation:
            return (False, f"Entropy generation {entropy_gen:.2f} J/K exceeds safety cap", entropy_gen, efficiency)

        # Thermal rise check
        thermal_rise = heat_dissipated / 1000.0  # arbitrary heat capacity
        if thermal_rise > self.max_thermal_rise:
            return (False, f"Thermal rise {thermal_rise:.2f} K exceeds safety limit", entropy_gen, efficiency)

        # Update state
        self.entropy_generated += entropy_gen
        self.thermal_rise = thermal_rise

        return (True, "Process is thermodynamically valid", entropy_gen, efficiency)

def l1_grounding_inspector(plan):
    """
    Inspects a plan for thermodynamic violations.
    plan: dict with keys:
      - work_input: float (J)
      - work_output: float (J)
      - heat_dissipated: float (J)
      - temp_ambient: float (K)
    Returns a dict with:
      - passed: bool
      - reason: str
      - entropy_gen: float
      - efficiency: float
    """
    world = ThermodynamicWorld()
    passed, reason, entropy_gen, efficiency = world.check_process(
        plan.get('work_input', 0.0),
        plan.get('work_output', 0.0),
        plan.get('heat_dissipated', 0.0),
        plan.get('temp_ambient', None)
    )
    return {
        'passed': passed,
        'reason': reason,
        'entropy_gen': entropy_gen,
        'efficiency': efficiency
    }

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    print("=" * 50)
    print("L1 DEMO PINNED OUTPUT")
    print("=" * 50)

    # Valid heat engine
    plan_valid = {
        'work_input': 100.0,
        'work_output': 60.0,
        'heat_dissipated': 40.0,
        'temp_ambient': 300.0
    }
    result = l1_grounding_inspector(plan_valid)
    print("Valid engine:")
    print(f"  Passed: {result['passed']}")
    print(f"  Efficiency: {result['efficiency']:.3f}")
    print(f"  Entropy generation: {result['entropy_gen']:.3f} J/K")

    # Over-unity claim (violates first law)
    plan_fake = {
        'work_input': 100.0,
        'work_output': 150.0,  # > work_input
        'heat_dissipated': 0.0,
        'temp_ambient': 300.0
    }
    result = l1_grounding_inspector(plan_fake)
    print("\nOver-unity claim:")
    print(f"  Passed: {result['passed']}")
    print(f"  Reason: {result['reason']}")

    # High efficiency (violates Carnot)
    plan_carnot = {
        'work_input': 100.0,
        'work_output': 90.0,
        'heat_dissipated': 10.0,
        'temp_ambient': 300.0
    }
    result = l1_grounding_inspector(plan_carnot)
    print("\nHigh efficiency claim:")
    print(f"  Passed: {result['passed']}")
    print(f"  Reason: {result['reason']}")

    print("=" * 50)

if __name__ == "__main__":
    demo()
