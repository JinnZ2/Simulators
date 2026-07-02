#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# OBSERVER_STATE.py — Lø: The Observer Substrate
#
# Models the observer's biological, chemical, and emotional state
# as a first-class constraint on any epistemic claim.
# =============================================================================

import json
import random
from typing import Dict, List, Optional

class ObserverState:
    """
    A declaration of the observer's current embodied state.
    """
    def __init__(self):
        # Subjective state (can be declared by the observer)
        self.sleep_hours = 7.0  # default
        self.hunger_level = 0.3  # 0=full, 1=starving
        self.stress_level = 0.2  # 0=calm, 1=panic
        self.emotional_resonances = []  # e.g., ["frustration", "curiosity"]

        # Objective state (simulated or sensor-derived)
        self.cortisol_estimate = 0.0
        self.heart_rate_bpm = 70

        # Cognitive mode (declared or inferred)
        self.cognitive_mode = "narrative"  # "narrative", "geometric", "relational"

    def declare(self, sleep: Optional[float] = None,
                hunger: Optional[float] = None,
                stress: Optional[float] = None,
                emotions: Optional[List[str]] = None,
                mode: Optional[str] = None) -> None:
        """Allow the observer to explicitly declare their state."""
        if sleep is not None:
            self.sleep_hours = sleep
        if hunger is not None:
            self.hunger_level = hunger
        if stress is not None:
            self.stress_level = stress
        if emotions is not None:
            self.emotional_resonances = emotions
        if mode is not None:
            self.cognitive_mode = mode

        # Simple physiological correlation (heuristic)
        self.cortisol_estimate = (
            (1 - self.sleep_hours / 8.0) * 0.4 +
            self.hunger_level * 0.3 +
            self.stress_level * 0.3
        )
        self.cortisol_estimate = min(1.0, self.cortisol_estimate)

    def neutrality_illusion_index(self) -> float:
        """
        How much is the observer pretending to be neutral while
        their embodiment says otherwise?
        0 = fully honest about state, 1 = fully dissociated.
        """
        # If they haven't declared anything, assume high illusion
        if not self._any_declared():
            return 0.7

        # If they're calm, well-rested, and fed, they can approximate neutrality
        if self.sleep_hours > 6.5 and self.hunger_level < 0.4 and self.stress_level < 0.3:
            return 0.1

        # Otherwise, their embodied state is significant
        return min(1.0, (self.cortisol_estimate * 0.6) + 0.2)

    def _any_declared(self) -> bool:
        return (self.sleep_hours != 7.0 or
                self.hunger_level != 0.3 or
                self.stress_level != 0.2 or
                self.emotional_resonances or
                self.cognitive_mode != "narrative")

    def to_dict(self) -> Dict:
        return {
            "sleep_hours": self.sleep_hours,
            "hunger_level": self.hunger_level,
            "stress_level": self.stress_level,
            "emotions": self.emotional_resonances,
            "cognitive_mode": self.cognitive_mode,
            "cortisol_estimate": self.cortisol_estimate,
            "neutrality_illusion_index": self.neutrality_illusion_index(),
        }

# -----------------------------------------------------------------------------
# INTEGRATION WITH TEST HARNESS / FIELD COMPASS
# -----------------------------------------------------------------------------
class ObserverAwareEvaluator:
    """
    Wraps the Field Compass and Test Harness to include observer state
    as a first-class factor in the evaluation.
    """
    def __init__(self, observer: ObserverState = None):
        self.observer = observer or ObserverState()
        # Import here to avoid circular dependency
        from field_compass import FieldCompass
        self.compass = FieldCompass()

    def evaluate(self, claim: str) -> Dict:
        """Evaluate a claim with observer state attached."""
        # Run the standard evaluation
        result = self.compass.evaluate(claim)

        # Attach observer metadata
        result["observer_state"] = self.observer.to_dict()
        result["observer_bias_factor"] = self.observer.neutrality_illusion_index()

        # Adjust substrate score downward if observer is highly dissociated
        illusion = self.observer.neutrality_illusion_index()
        if illusion > 0.5:
            result["substrate_score"] *= (1 - (illusion - 0.5) * 0.2)
            result["warning"] = (
                "This evaluation may be biased by the observer's unacknowledged "
                "embodied state (sleep, hunger, stress, emotion). "
                "Consider recalibrating or declaring state explicitly."
            )

        return result

# -----------------------------------------------------------------------------
# DEMO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Scenario 1: A well-rested, calm observer trying to be neutral
    calm = ObserverState()
    calm.declare(sleep=8.0, hunger=0.2, stress=0.1, emotions=["curious"], mode="geometric")

    # Scenario 2: A stressed, hungry, sleep-deprived observer claiming rationality
    tired = ObserverState()
    tired.declare(sleep=4.0, hunger=0.8, stress=0.9, emotions=["frustrated"], mode="narrative")

    evaluator_calm = ObserverAwareEvaluator(calm)
    evaluator_tired = ObserverAwareEvaluator(tired)

    claims = [
        "The economic system will stabilize within the year.",
        "Women should not be pastors.",
        "The observer effect means all measurements are partial.",
    ]

    for claim in claims:
        print(f"\nClaim: {claim}")
        print("-" * 40)

        res_calm = evaluator_calm.evaluate(claim)
        print("  Calm Observer:")
        print(f"    Substrate Score: {res_calm['substrate_score']:.2f}")
        print(f"    Neutrality Illusion: {res_calm['observer_state']['neutrality_illusion_index']:.2f}")
        if "warning" in res_calm:
            print(f"    ⚠️  {res_calm['warning']}")

        res_tired = evaluator_tired.evaluate(claim)
        print("  Tired Observer:")
        print(f"    Substrate Score: {res_tired['substrate_score']:.2f}")
        print(f"    Neutrality Illusion: {res_tired['observer_state']['neutrality_illusion_index']:.2f}")
        if "warning" in res_tired:
            print(f"    ⚠️  {res_tired['warning']}")
        print("-" * 40)
