#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# L4: Human Sensorimotor (Scoped Variability Model)
#
# No human limit is universal. This inspector uses distributions and
# scope annotations. If a claim is unscoped, it flags it and returns
# a probability estimate.
#
# CONSTRAINTS (frozen for audit, but expressed as distributions):
#   lift_mass: mean=35, std=15, source="general adult (WEIRD)"
#   wrist_flexion: mean=70, std=20, source="general adult (WEIRD)"
#   reaction_time: mean=0.25, std=0.05, source="general adult (WEIRD)"
#   temp_tolerance: mean=43, std=5, source="general adult (WEIRD)"
#   sustained_power: mean=150, std=50, source="general adult (WEIRD)"
#
# These constants are frozen. If a test fails, DO NOT retune them.
# Update the claims in CLAIMS.md instead.
# =============================================================================

import math
from typing import Dict, Optional, Tuple

class HumanProfile:
    """Defines a specific human context for scoping limits."""
    def __init__(self, name: str, lift_shift: float = 0.0, reaction_shift: float = 0.0,
                 temp_shift: float = 0.0, power_shift: float = 0.0):
        self.name = name
        self.lift_shift = lift_shift
        self.reaction_shift = reaction_shift
        self.temp_shift = temp_shift
        self.power_shift = power_shift

    def apply(self, base_mean: float, shift: float) -> float:
        return base_mean + shift

# Predefined profiles
PROFILES = {
    "general": HumanProfile("general"),
    "athlete": HumanProfile("athlete", lift_shift=15.0, reaction_shift=-0.05, power_shift=50.0),
    "elder": HumanProfile("elder", lift_shift=-10.0, reaction_shift=0.10, power_shift=-30.0),
    "child": HumanProfile("child", lift_shift=-20.0, reaction_shift=0.05, power_shift=-50.0),
    "trained": HumanProfile("trained", lift_shift=10.0, reaction_shift=-0.02, power_shift=30.0),
}

class HumanWorld:
    def __init__(self, profile: str = "general"):
        self.profile = PROFILES.get(profile, PROFILES["general"])
        self.profile_name = profile

        # Base distributions (mean, std) from WEIRD population
        self.lift_mass = (35.0, 15.0)
        self.wrist_flexion = (70.0, 20.0)
        self.reaction_time = (0.25, 0.05)
        self.temp_tolerance = (43.0, 5.0)
        self.sustained_power = (150.0, 50.0)

    def _apply_profile(self, base_mean: float, shift: float) -> float:
        return base_mean + shift

    def get_limit(self, parameter: str, profile: Optional[str] = None) -> Tuple[float, float]:
        """Return (mean, std) for the given parameter and profile."""
        if profile is None:
            profile = self.profile_name
        p = PROFILES.get(profile, PROFILES["general"])

        if parameter == "lift_mass":
            mean, std = self.lift_mass
            return (self._apply_profile(mean, p.lift_shift), std)
        elif parameter == "reaction_time":
            mean, std = self.reaction_time
            return (self._apply_profile(mean, p.reaction_shift), std)
        elif parameter == "temp_tolerance":
            mean, std = self.temp_tolerance
            return (self._apply_profile(mean, p.temp_shift), std)
        elif parameter == "sustained_power":
            mean, std = self.sustained_power
            return (self._apply_profile(mean, p.power_shift), std)
        else:
            return (0.0, 1.0)

    def is_within_95ci(self, value: float, mean: float, std: float) -> bool:
        """Check if value is within ±2σ of mean."""
        return (mean - 2 * std) <= value <= (mean + 2 * std)

    def probability_of_feasibility(self, value: float, mean: float, std: float) -> float:
        """
        Estimate probability that a randomly selected individual
        from this population can achieve this value.
        Uses a simple cumulative normal approximation.
        """
        if std <= 0:
            return 1.0 if value <= mean else 0.0
        z = (value - mean) / std
        # Approximate cumulative distribution (sigmoid)
        return 1.0 / (1.0 + math.exp(-z * 0.5))

def l4_grounding_inspector(plan: dict) -> dict:
    """
    plan: dict with keys:
      - lift_mass (kg)
      - wrist_flexion (degrees)
      - reaction_time (seconds)
      - temp_tolerance (C)
      - sustained_power (W)
      - human_profile (str): one of "general", "athlete", "elder", "child", "trained"
    Returns: dict with passed, reason, probability, and details.
    """
    world = HumanWorld(profile=plan.get('human_profile', 'general'))
    passed = True
    reasons = []
    details = {}
    probability = 1.0

    if 'lift_mass' in plan:
        mean, std = world.get_limit('lift_mass')
        value = plan['lift_mass']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Lift mass {value} kg outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f})")
        details['lift_mass'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    if 'reaction_time' in plan:
        mean, std = world.get_limit('reaction_time')
        value = plan['reaction_time']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Reaction time {value*1000:.0f} ms outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f}) s")
        details['reaction_time'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    if 'temp_tolerance' in plan:
        mean, std = world.get_limit('temp_tolerance')
        value = plan['temp_tolerance']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Temperature {value}°C outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f}°C)")
        details['temp_tolerance'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    if 'sustained_power' in plan:
        mean, std = world.get_limit('sustained_power')
        value = plan['sustained_power']
        prob = world.probability_of_feasibility(value, mean, std)
        probability = min(probability, prob)
        if not world.is_within_95ci(value, mean, std):
            passed = False
            reasons.append(f"Power {value} W outside 95% CI ({mean-2*std:.1f}–{mean+2*std:.1f} W)")
        details['sustained_power'] = {'value': value, 'mean': mean, 'std': std, 'prob': prob}

    # Scope check: if profile is not declared, flag it
    if 'human_profile' not in plan:
        reasons.append("No human_profile declared. Using 'general' as default.")
        details['scope_warning'] = "Unscoped claim; default profile used."

    return {
        'passed': passed,
        'reason': '; '.join(reasons) if reasons else 'All constraints satisfied.',
        'probability': probability,
        'details': details
    }

# -----------------------------------------------------------------------------
# Demo (pinned output)
# -----------------------------------------------------------------------------
def demo():
    print("=" * 60)
    print("L4 DEMO PINNED OUTPUT (Scoped Variability Model)")
    print("=" * 60)

    # Claim: general adult lifting 45 kg (within 95% CI)
    plan = {
        'lift_mass': 45.0,
        'human_profile': 'general',
        'reaction_time': 0.25,
        'temp_tolerance': 40.0,
        'sustained_power': 150.0
    }
    result = l4_grounding_inspector(plan)
    print(f"General adult, 45 kg lift: Passed={result['passed']}")
    print(f"  Probability: {result['probability']:.2f}")
    print(f"  Lift mean: {result['details']['lift_mass']['mean']:.1f} kg")

    # Claim: athlete lifting 60 kg (above mean but possible)
    plan = {
        'lift_mass': 60.0,
        'human_profile': 'athlete',
        'reaction_time': 0.20,
        'temp_tolerance': 45.0,
        'sustained_power': 200.0
    }
    result = l4_grounding_inspector(plan)
    print(f"\nAthlete, 60 kg lift: Passed={result['passed']}")
    print(f"  Probability: {result['probability']:.2f}")
    print(f"  Reaction time mean: {result['details']['reaction_time']['mean']:.2f} s")

    # Claim: child lifting 50 kg (likely outside 95% CI)
    plan = {
        'lift_mass': 50.0,
        'human_profile': 'child',
        'reaction_time': 0.30,
        'temp_tolerance': 35.0,
        'sustained_power': 100.0
    }
    result = l4_grounding_inspector(plan)
    print(f"\nChild, 50 kg lift: Passed={result['passed']}")
    if not result['passed']:
        print(f"  Reason: {result['reason']}")
        print(f"  Probability: {result['probability']:.2f}")

    # Unscoped claim (no profile)
    plan = {
        'lift_mass': 40.0,
        'reaction_time': 0.22,
        'temp_tolerance': 42.0,
        'sustained_power': 160.0
    }
    result = l4_grounding_inspector(plan)
    print(f"\nUnscoped claim: Passed={result['passed']}")
    print(f"  Scope warning: {result['details'].get('scope_warning', 'None')}")
    print("=" * 60)

if __name__ == "__main__":
    demo()
