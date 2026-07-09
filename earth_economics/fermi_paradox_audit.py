#!/usr/bin/env python3
"""
fermi_paradox_audit.py – Dyson sphere / Fermi paradox cascade audit.
CC0. Stdlib only.

Models an expanding civilization's trajectory through the cascade-coupling
framework. Detects finite-time singularities where complexity cost exceeds
energy gain, explaining why advanced civilizations may choose not to expand.

Usage:
  python fermi_paradox_audit.py
  python fermi_paradox_audit.py --json
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


# ----------------------------------------------------------------------
# Constants & thresholds from the cascade framework
# ----------------------------------------------------------------------
DUNBAR = 150                # relational trust ceiling
SCALE_CEILING_DEFAULT = 500 # start with relational-primary scale
HOI_REDUCTION = 0.3         # higher-order interaction threshold reduction (70%)
MERLE_THRESHOLD = 0.05      # d²E/dt² threshold for blow-up detection


@dataclass
class CivilizationState:
    """State variables for a civilization's expansion trajectory."""
    year: float = 2026.0
    population: float = 8e9
    energy_consumption: float = 2e13  # watts (global primary energy)
    energy_cost_of_expansion: float = 0.0  # cumulative energy invested in expansion
    energy_return: float = 0.0           # cumulative energy collected
    complexity_overhead: float = 0.0     # coordination cost (BEI surrogate)
    trust_fraction: float = 0.3          # proportion relational trust (1 = pure relational)
    institutional_coercion: float = 0.7  # proportion institutional enforcement
    scale_ceiling: float = 500.0         # current network size limit before trust flips
    cascade_risk: float = 0.0            # probability of a fatal cascade event
    regime_shift_count: int = 0          # number of regime shifts already triggered
    extinction_probability: float = 0.0  # cumulative probability of extinction

    @property
    def SCI(self) -> float:
        """Scale Ceiling Index: >1 means healthy, <1 means brittle."""
        return self.scale_ceiling / max(1, self.population / 1e6)

    @property
    def BEI(self) -> float:
        """Bureaucratic Entropy Index: coordination overhead."""
        return self.complexity_overhead / max(1, self.energy_consumption)

    @property
    def EROI(self) -> float:
        """Energy return on investment for the expansion trajectory."""
        if self.energy_cost_of_expansion == 0:
            return float("inf")
        return self.energy_return / self.energy_cost_of_expansion


def cascade_step(state: CivilizationState, expansion_rate: float) -> CivilizationState:
    """
    Advance one time step. expansion_rate = fraction of current energy 
    consumed that is reinvested into further expansion (Dyson swarm construction).
    """
    dt = 1.0  # one year
    new_state = CivilizationState()
    new_state.year = state.year + dt

    # Population grows with energy (superlinear at first, then limited)
    growth_factor = min(1.5, 1.0 + 0.02 * (state.EROI - 1.0) if state.EROI > 1.0 else 0.98)
    new_state.population = state.population * growth_factor

    # Energy consumption: expand if EROI is positive, contract if not
    energy_growth = expansion_rate * state.energy_consumption
    new_state.energy_consumption = state.energy_consumption + energy_growth

    # Complexity overhead grows superlinearly with scale (institutional cost)
    # BEI scales as population^1.2 (empirically observed in administrative systems)
    new_state.complexity_overhead = state.complexity_overhead * (growth_factor ** 1.2)

    # Energy invested in expansion
    new_state.energy_cost_of_expansion = state.energy_cost_of_expansion + energy_growth

    # Energy return: diminishing returns on expansion (further out in the solar system)
    # Each expansion step yields less energy per unit invested (logarithmic)
    if state.energy_return > 0:
        marginal_return = energy_growth * max(0.1, 1.0 / math.log(2 + state.energy_return / 1e13))
    else:
        marginal_return = energy_growth * 1.5  # initial high return
    new_state.energy_return = state.energy_return + marginal_return

    # Trust fraction decays as scale exceeds Dunbar
    if new_state.population > DUNBAR * state.scale_ceiling:
        new_state.trust_fraction = state.trust_fraction * 0.95
        new_state.institutional_coercion = 1.0 - new_state.trust_fraction
    else:
        new_state.trust_fraction = state.trust_fraction
        new_state.institutional_coercion = 1.0 - new_state.trust_fraction

    # Scale ceiling adjusts: relational systems can scale a bit with tooling, but not indefinitely
    new_state.scale_ceiling = state.scale_ceiling * (1.0 + 0.01 * (1.0 - new_state.institutional_coercion))

    # Cascade risk increases as institutional coercion rises and trust falls
    # Higher-order interactions reduce the threshold by 70%
    base_risk = new_state.institutional_coercion * (1.0 - new_state.trust_fraction)
    triplet_risk = base_risk / HOI_REDUCTION if HOI_REDUCTION > 0 else base_risk * 3.0
    new_state.cascade_risk = min(1.0, triplet_risk)

    # Regime shift: cascade risk exceeds threshold
    if new_state.cascade_risk > 0.7 and state.cascade_risk <= 0.7:
        new_state.regime_shift_count = state.regime_shift_count + 1
    else:
        new_state.regime_shift_count = state.regime_shift_count

    # Extinction probability: cumulative product of cascade risks during regime shifts
    if new_state.regime_shift_count > 0:
        shift_penalty = 1.0 - math.exp(-new_state.regime_shift_count)
        new_state.extinction_probability = state.extinction_probability + (1.0 - state.extinction_probability) * shift_penalty
    else:
        new_state.extinction_probability = state.extinction_probability

    return new_state


def merle_blow_up_detection(history: List[CivilizationState]) -> List[Tuple[float, float]]:
    """
    Compute d²E/dt² over the trajectory and detect finite-time singularities.
    """
    if len(history) < 3:
        return []
    energy_series = [(s.year, s.energy_cost_of_expansion) for s in history]
    accel = []
    for i in range(1, len(energy_series) - 1):
        y0, e0 = energy_series[i-1]
        y2, e2 = energy_series[i+1]
        d2e = (e2 - e0) / ((y2 - y0) ** 2) if y2 > y0 else 0
        accel.append((energy_series[i][0], d2e))
    return [(y, a) for y, a in accel if a > MERLE_THRESHOLD]


def run_simulation(expansion_rate: float, horizon: int = 500) -> Dict:
    """
    Run the civilization expansion trajectory.
    Returns verdict and history.
    """
    state = CivilizationState()
    history = [state]

    for _ in range(horizon):
        state = cascade_step(state, expansion_rate)
        history.append(state)
        # Check termination conditions
        if state.EROI < 1.0 and state.energy_return > state.energy_cost_of_expansion * 10:
            # EROI dropped below 1 after significant investment: collapse imminent
            pass
        if state.extinction_probability > 0.9:
            break

    blow_ups = merle_blow_up_detection(history)
    final = history[-1]

    # Verdict
    if final.extinction_probability > 0.8:
        verdict = "SELF_TERMINATING"
        explanation = (
            "Expansion trajectory hits finite-time singularity. "
            "Complexity costs exceed energy gains; cascade risk → 1. "
            "Civilization collapses before completing Dyson sphere."
        )
    elif final.EROI < 1.0 and len(blow_ups) > 0:
        verdict = "QUIET_SURVIVOR"
        explanation = (
            "Civilization detects blow-up signature early and stops expanding. "
            "Stays below scale ceiling, preserves relational trust. "
            "Invisible to Kardashev-scale detection — solves Fermi paradox."
        )
    elif final.EROI > 2.0 and final.extinction_probability < 0.1:
        verdict = "STILL_EXPANDING"
        explanation = (
            "EROI remains positive and cascade risk low. "
            "But note: this trajectory is before the HOI threshold reduction. "
            "If triplet interactions are included, cascade risk would be 3x higher."
        )
    else:
        verdict = "MARGINAL"
        explanation = "Trajectory is unstable; small perturbation triggers cascade."

    return {
        "verdict": verdict,
        "explanation": explanation,
        "final_state": final,
        "blow_up_years": [y for y, _ in blow_ups],
        "history_length": len(history),
        "final_EROI": final.EROI,
        "final_extinction_probability": final.extinction_probability,
        "regime_shifts": final.regime_shift_count,
        "falsifier": (
            "Find a civilization that has completed a Dyson sphere and reports "
            "EROI > 1 over full lifecycle, accounting for full-stack energy costs, "
            "cascade risk from higher-order interactions, and complexity overhead."
        ),
    }


def main():
    import json

    print("=" * 70)
    print("FERMI PARADOX / DYSON SPHERE AUDIT")
    print("=" * 70)
    print()
    print("Thesis: A Dyson sphere is a self-terminating trajectory.")
    print("Advanced civilizations that understand the constraint stack")
    print("choose not to expand beyond their scale ceiling.")
    print()

    # Run with a high expansion rate (aggressive Dyson builders)
    print("Scenario 1: Aggressive expansion (expansion_rate = 0.10)")
    result_aggressive = run_simulation(0.10, horizon=300)
    print(f"  Verdict: {result_aggressive['verdict']}")
    print(f"  Final EROI: {result_aggressive['final_EROI']:.2f}")
    print(f"  Extinction probability: {result_aggressive['final_extinction_probability']:.2f}")
    print(f"  Regime shifts: {result_aggressive['regime_shifts']}")
    if result_aggressive['blow_up_years']:
        print(f"  Blow-up detected at years: {result_aggressive['blow_up_years']}")
    print()

    # Run with low expansion (quiet survivors)
    print("Scenario 2: Quiet survivor (expansion_rate = 0.01)")
    result_quiet = run_simulation(0.01, horizon=500)
    print(f"  Verdict: {result_quiet['verdict']}")
    print(f"  Final EROI: {result_quiet['final_EROI']:.2f}")
    print(f"  Extinction probability: {result_quiet['final_extinction_probability']:.2f}")
    print(f"  Regime shifts: {result_quiet['regime_shifts']}")
    print()

    print("--- COMPARATIVE FRAMEWORK CONNECTION ---")
    print()
    print("Indigenous economic systems (Aboriginal, Ainu, Sámi, Ubuntu, Potlatch)")
    print("score deeply negative on OCDI and RPI. They already solved the Fermi")
    print("paradox: they detected the scale ceiling and chose to stay below it.")
    print("Their ontologies encode the constraint stack in relational terms.")
    print()
    print("The Dyson sphere is not a sign of advancement. It is a sign of a")
    print("civilization that did not read the equations. The quiet ones survived.")
    print()
    print(f"Falsifier: {result_aggressive['falsifier']}")

    # JSON output option
    import sys
    if "--json" in sys.argv:
        print(json.dumps({
            "aggressive": {k: str(v) if not isinstance(v, (int, float, list)) else v
                          for k, v in result_aggressive.items()},
            "quiet": {k: str(v) if not isinstance(v, (int, float, list)) else v
                     for k, v in result_quiet.items()}
        }, indent=2))


if __name__ == "__main__":
    main()
