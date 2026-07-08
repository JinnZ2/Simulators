#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
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


# =============================================================================
# STAGE (per LOG.md "Probabilistic L1-L4 Conditioning" section 2):
# ProbabilisticThermodynamicsWorld and l1_probabilistic_inspector
#
# Bayesian counterpart to check_process / l1_grounding_inspector. Each
# thermodynamic constraint contributes a scalar log-probability term:
#
#   First law    - Gaussian on energy imbalance |work_in - work_out - heat|
#   Second law   - logistic barrier: ~0 for entropy_gen >= 0, linear
#                  penalty of slope entropy_scale for entropy_gen < 0
#   Carnot       - logistic barrier: ~0 below carnot_max, -log(2) at cap,
#                  slope -carnot_scale above
#   Battery      - Gaussian on overdraw (0 for draw <= state)
#
# Frozen noise/scale constants live on the class __init__ defaults,
# pinned by GL_L1_P001..004 + P_PIN in CLAIMS.md.
# =============================================================================


class ProbabilisticThermodynamicsWorld(ThermodynamicWorld):
    """
    L1 with Gaussian log-likelihoods + smooth logistic barriers on the
    thermodynamic constraints. Extends ThermodynamicWorld so the
    deterministic API stays available.

    SCOPE (see grounding-layers/SCOPE_TAXONOMY.md):
      T = single_step (one process at a time; caller sequences)
      S = single_reservoir (LOG.md two-reservoir refinement is future)
      O = any_energy_system
      C = industrial_science_frame (Carnot ceiling comes from a
          heat-engine framing; efficiency_carnot_max = 0.85 encodes
          a specific engine family. Second-law and first-law claims
          themselves are culture_neutral; the specific Carnot number
          is human/industrial.)

    An AI evaluating its own thermal footprint (compute → heat)
    would be bound by first law, second law, and Carnot ceiling
    (as any energy system); the Earth-normal ambient_temp=300K
    default may not apply to an off-Earth substrate.

    Constraint set inherited from ThermodynamicWorld:
      efficiency_carnot_max = 0.85
      ambient_temp          = 300.0 K
      max_entropy_generation = 10.0 J/K (deterministic cap; the
                              probabilistic path uses the barrier
                              instead)
      max_thermal_rise      = 50.0 K per step (same)

    Frozen noise / scale constants added here:
      energy_sigma   = 1.0     J        Gaussian sigma on the first-law imbalance
      entropy_scale  = 1.0     per J/K  slope of the 2nd-law logistic barrier
                                        below zero (per unit of negative
                                        entropy generation)
      carnot_scale   = 10.0    per unit slope of the Carnot logistic barrier
                                        above efficiency_carnot_max (per
                                        unit of excess efficiency)
      battery_sigma  = 5.0     J        Gaussian sigma on overdraw beyond
                                        battery_state

    Refute the CLAIM, not the constant. Same protocol as L0.
    """

    def __init__(self,
                 efficiency_carnot_max=0.85,
                 ambient_temp=300.0,
                 max_entropy_generation=10.0,
                 max_thermal_rise=50.0,
                 energy_sigma=1.0,
                 entropy_scale=1.0,
                 carnot_scale=10.0,
                 battery_sigma=5.0):
        super().__init__(efficiency_carnot_max, ambient_temp,
                         max_entropy_generation, max_thermal_rise)
        self.energy_sigma = energy_sigma
        self.entropy_scale = entropy_scale
        self.carnot_scale = carnot_scale
        self.battery_sigma = battery_sigma

    def log_likelihood(self,
                       work_input,
                       work_output,
                       heat_dissipated,
                       temp_ambient=None,
                       battery_state=None):
        """
        Return scalar log-probability of a thermodynamic process under
        the four L1 constraints.

        Parameters:
          work_input       (J)  energy put into the process
          work_output      (J)  useful work extracted
          heat_dissipated  (J)  waste heat to the environment
          temp_ambient     (K)  reservoir temperature; defaults to
                                self.ambient_temp (single-reservoir
                                approximation matching check_process)
          battery_state    (J)  optional; remaining stored energy
                                the process is drawing from. If None,
                                battery-depletion term is silent.

        Returns:
          scalar log-probability (float). Zero when the process is
          physically consistent; strongly negative when constraints
          are violated.

        Note on single vs two-reservoir entropy. LOG.md's sketch uses
        ΔS = heat_in/T_hot - heat_out/T_cold. For consistency with the
        deterministic ThermodynamicWorld.check_process we use a single
        temp_ambient here (entropy_gen = heat_dissipated / T). A
        two-reservoir refinement is a future round; the SCOPE of this
        method is single-reservoir processes.
        """
        if temp_ambient is None:
            temp_ambient = self.ambient_temp

        # 1. First law (energy books): symmetric Gaussian
        energy_imbalance = work_input - (work_output + heat_dissipated)
        logp_energy = -(energy_imbalance ** 2) / (2 * self.energy_sigma ** 2)

        # 2. Second law (entropy generation): smooth logistic barrier
        # Positive entropy_gen -> logp ≈ 0; negative -> linear penalty
        # of slope -entropy_scale in the tail.
        if temp_ambient > 0:
            entropy_gen = heat_dissipated / temp_ambient
        else:
            entropy_gen = 0.0
        logp_entropy = -np.logaddexp(0.0, -self.entropy_scale * entropy_gen)

        # 3. Carnot ceiling: logistic barrier on efficiency
        if work_input > 0:
            efficiency = work_output / work_input
            excess = efficiency - self.efficiency_carnot_max
            logp_carnot = -np.logaddexp(0.0, self.carnot_scale * excess)
        else:
            logp_carnot = 0.0

        # 4. Battery depletion: quadratic penalty on overdraw
        if battery_state is not None:
            overdraw = work_input - battery_state
            if overdraw > 0:
                logp_battery = -(overdraw ** 2) / (2 * self.battery_sigma ** 2)
            else:
                logp_battery = 0.0
        else:
            logp_battery = 0.0

        return logp_energy + logp_entropy + logp_carnot + logp_battery


def l1_probabilistic_inspector(plan, world=None):
    """
    Bayesian counterpart to l1_grounding_inspector. Given a plan
    (dict with the same keys check_process expects, plus optional
    battery_state), return a scalar log-probability under the L1
    probabilistic model.

    plan: dict with keys
      - work_input, work_output, heat_dissipated  (J; required)
      - temp_ambient      (K; optional, default ambient_temp)
      - battery_state     (J; optional, default None => no battery term)

    world: optional ProbabilisticThermodynamicsWorld; if None a fresh
    one is instantiated with default frozen constants.

    Returns:
      dict with:
        - logp        (float) total log-probability
        - components  (dict)  per-constraint log-probability breakdown
                              (energy, entropy, carnot, battery)

    Design note. Unlike L0's inspector, L1 currently operates on a
    single process step, not a trajectory. If a plan spans multiple
    steps, sum the logp across steps at the caller. (This mirrors
    the existing l1_grounding_inspector's one-step API.)
    """
    if world is None:
        world = ProbabilisticThermodynamicsWorld()

    work_input = plan.get('work_input', 0.0)
    work_output = plan.get('work_output', 0.0)
    heat_dissipated = plan.get('heat_dissipated', 0.0)
    temp_ambient = plan.get('temp_ambient', None)
    battery_state = plan.get('battery_state', None)

    # Compute per-component logp by isolating each term. This mirrors
    # the log_likelihood method's structure so the breakdown lines up.
    if temp_ambient is None:
        temp_ambient = world.ambient_temp

    energy_imbalance = work_input - (work_output + heat_dissipated)
    logp_energy = -(energy_imbalance ** 2) / (2 * world.energy_sigma ** 2)

    entropy_gen = (heat_dissipated / temp_ambient
                   if temp_ambient > 0 else 0.0)
    logp_entropy = -np.logaddexp(0.0, -world.entropy_scale * entropy_gen)

    if work_input > 0:
        efficiency = work_output / work_input
        excess = efficiency - world.efficiency_carnot_max
        logp_carnot = -np.logaddexp(0.0, world.carnot_scale * excess)
    else:
        logp_carnot = 0.0

    if battery_state is not None:
        overdraw = work_input - battery_state
        logp_battery = (-(overdraw ** 2) / (2 * world.battery_sigma ** 2)
                        if overdraw > 0 else 0.0)
    else:
        logp_battery = 0.0

    total = logp_energy + logp_entropy + logp_carnot + logp_battery
    return {
        'logp': total,
        'components': {
            'energy': logp_energy,
            'entropy': logp_entropy,
            'carnot': logp_carnot,
            'battery': logp_battery,
        }
    }

