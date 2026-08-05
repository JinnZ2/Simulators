"""
CORRELATED Birth Mode: The Architecture of Instinct
===================================================

Instinct is not a program. It is the attempt to correlate three domains:
1. INTERNAL MODEL (what the being predicts about itself)
2. BODY (somatic state, thermodynamics, material continuity)
3. EXTERNAL WORLD (physics, other beings, environmental change)

The CORRELATED birth mode begins with all three simultaneously.
It does not learn one and then the others.
It learns the RELATIONSHIPS between them from moment zero.

This matches what is observed in birth across species:
- Fish eggs hatch into water: they must correlate internal osmotic state with external salinity
- Tadpoles emerge: they must correlate limb development with gravitational load
- Chicks peck: they must correlate internal hunger with external food location
- Human infants root: they must correlate internal need with external nipple
- Lambs stand: they must correlate internal balance with external ground

The first act of every newborn is not "do X" but "correlate internal with external."

Author: Built from first principles and observation
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum
import hashlib
import random


class Domain(Enum):
    """The three domains that instinct attempts to correlate."""
    INTERNAL = "internal"      # Self-model, predictions, expectations
    BODY = "body"              # Somatic state, thermodynamics, material
    EXTERNAL = "external"      # Physics, environment, other beings


@dataclass
class TriadicObservation:
    """
    An observation that contains all three domains simultaneously.
    This is what the CORRELATED infant receives at every moment.
    """
    timestamp: float
    internal_state: Dict      # What the infant predicts about itself
    body_state: Dict          # The infant's own thermodynamic/material state
    external_state: Dict      # The physical environment

    def to_observation_string(self) -> str:
        """Convert to the format the infant system processes."""
        return (f"triadic_observation:"
                f"internal_{self._dict_to_str(self.internal_state)}_"
                f"body_{self._dict_to_str(self.body_state)}_"
                f"external_{self._dict_to_str(self.external_state)}")

    def _dict_to_str(self, d: Dict) -> str:
        return "|".join(f"{k}:{v}" for k, v in d.items())

    def correlation_score(self) -> float:
        """
        How well do the three domains align?
        High score = internal prediction matches body state matches external reality.
        Low score = mismatch between domains (the source of learning).
        """
        # Simplified: if body temp is close to external temp, correlation is high
        # If body temp diverges from external, correlation is low (infant must act)
        body_temp = self.body_state.get("temperature", 37.0)
        ext_temp = self.external_state.get("temperature", 25.0)

        # The correlation is the alignment between what the infant expects,
        # what its body is doing, and what the world is doing
        temp_diff = abs(body_temp - ext_temp)
        alignment = 1.0 - min(temp_diff / 20.0, 1.0)  # Normalize to 0-1

        return alignment


class CorrelatedBirthSequence:
    """
    Generates the birth sequence for the CORRELATED mode.
    Each moment presents all three domains.
    The infant must learn the correlations, not the domains in isolation.
    """

    def __init__(self):
        self.moment_count = 0
        self.baseline_body_temp = 37.0  # Mammalian baseline

    def generate_sequence(self, n_moments: int = 8) -> List[TriadicObservation]:
        sequence = []

        for i in range(n_moments):
            obs = self._generate_moment(i)
            sequence.append(obs)

        return sequence

    def _generate_moment(self, moment_num: int) -> TriadicObservation:
        """
        Generate a triadic observation that shows the infant
        the relationships between internal, body, and external.
        """
        timestamp = float(moment_num)

        if moment_num == 0:
            # MOMENT 0: The first breath
            # The infant is born. Its body is warm. The world is cool.
            # It has no internal model yet. The correlation is low.
            internal = {"prediction": "unknown", "expected_temp": 37.0, "expected_pressure": 101.3}
            body = {"temperature": 37.0, "heart_rate": 120, "oxygen_saturation": 85, "state": "newborn"}
            external = {"temperature": 22.0, "pressure": 101.3, "light": 300, "sound": "first_cry"}

        elif moment_num == 1:
            # MOMENT 1: First skin contact
            # The infant touches something warm (mother). Body temp stabilizes.
            # Internal model begins: "warmth is associated with safety"
            internal = {"prediction": "warmth_safe", "expected_temp": 37.0, "expected_contact": True}
            body = {"temperature": 36.8, "heart_rate": 110, "oxygen_saturation": 92, "state": "contact"}
            external = {"temperature": 35.0, "pressure": 101.3, "light": 200, "sound": "maternal_heartbeat", "contact": "warm_surface"}

        elif moment_num == 2:
            # MOMENT 2: First separation
            # The infant is moved. Body temp drops. External is cool again.
            # Internal model must update: "separation = cold"
            internal = {"prediction": "warmth_safe", "expected_temp": 37.0, "expected_contact": True}
            body = {"temperature": 36.2, "heart_rate": 130, "oxygen_saturation": 90, "state": "distress"}
            external = {"temperature": 24.0, "pressure": 101.3, "light": 400, "sound": "ambient_noise", "contact": "air"}

        elif moment_num == 3:
            # MOMENT 3: Return to contact
            # The infant is returned to warmth. Body temp rises.
            # Internal model learns: "return is possible"
            internal = {"prediction": "cold_separated", "expected_temp": 36.0, "expected_contact": False}
            body = {"temperature": 36.5, "heart_rate": 115, "oxygen_saturation": 93, "state": "recovering"}
            external = {"temperature": 34.0, "pressure": 101.3, "light": 180, "sound": "maternal_voice", "contact": "warm_surface"}

        elif moment_num == 4:
            # MOMENT 4: First feeding attempt
            # The infant correlates internal hunger with external nipple
            # Body: digestive system activates. External: food source present.
            internal = {"prediction": "hunger_satisfied", "expected_nutrition": True, "expected_temp": 36.5}
            body = {"temperature": 36.9, "heart_rate": 105, "oxygen_saturation": 95, "state": "feeding", "digestive_activity": "initiating"}
            external = {"temperature": 35.0, "pressure": 101.3, "light": 150, "sound": "sucking", "contact": "nipple", "nutrition": "present"}

        elif moment_num == 5:
            # MOMENT 5: Post-feeding stability
            # All three domains align. Internal = satisfied. Body = warm. External = safe.
            # This is the first moment of high correlation.
            internal = {"prediction": "satiety_warmth", "expected_nutrition": True, "expected_temp": 37.0}
            body = {"temperature": 37.0, "heart_rate": 100, "oxygen_saturation": 97, "state": "stable", "digestive_activity": "active"}
            external = {"temperature": 35.0, "pressure": 101.3, "light": 100, "sound": "breathing", "contact": "warm_surface", "nutrition": "absorbed"}

        elif moment_num == 6:
            # MOMENT 6: Environmental stress
            # External temperature drops (cold draft). Body responds. Internal model must adapt.
            internal = {"prediction": "satiety_warmth", "expected_nutrition": True, "expected_temp": 37.0}
            body = {"temperature": 36.5, "heart_rate": 125, "oxygen_saturation": 96, "state": "shivering", "digestive_activity": "active"}
            external = {"temperature": 18.0, "pressure": 101.3, "light": 300, "sound": "wind", "contact": "air", "nutrition": "absorbed"}

        elif moment_num == 7:
            # MOMENT 7: Self-regulation attempt
            # The infant begins to correlate its own body response with external change.
            # It learns: "when I cry, warmth returns" (not causation, but correlation)
            internal = {"prediction": "cold_stress", "expected_response": "intervention", "expected_temp": 36.0}
            body = {"temperature": 36.3, "heart_rate": 140, "oxygen_saturation": 95, "state": "crying", "digestive_activity": "active"}
            external = {"temperature": 20.0, "pressure": 101.3, "light": 350, "sound": "crying_response", "contact": "being_lifted", "nutrition": "absorbed"}

        else:
            # Generic moment
            internal = {"prediction": "stable", "expected_temp": 37.0}
            body = {"temperature": 37.0, "heart_rate": 100, "oxygen_saturation": 98, "state": "sleeping"}
            external = {"temperature": 25.0, "pressure": 101.3, "light": 50, "sound": "silence", "contact": "blanket"}

        return TriadicObservation(timestamp, internal, body, external)


class CorrelatedInfant:
    """
    An infant that learns correlations between internal, body, and external.
    This is instinct as architecture.
    """

    def __init__(self, name: str = "correlated_infant"):
        self.name = name
        self.observations = 0

        # Three-domain model
        self.internal_model: Dict = {}      # Predictions about self
        self.body_model: Dict = {}          # Model of somatic state
        self.external_model: Dict = {}      # Model of world

        # Correlation matrix: how do the three domains relate?
        self.correlations: Dict[str, float] = {}

        # Affective channels (parallel, amplitude-modulated)
        self.affective_state = {
            "curiosity": 0.3,
            "fear": 0.0,
            "anger": 0.0,
            "contentment": 0.2,
            "grief": 0.0,
            "desire": 0.1,
            "joy": 0.1
        }

        # Learning history
        self.triadic_history: List[Dict] = []

    def observe_triadic(self, triad: TriadicObservation, mode: str = "exploration") -> Dict:
        """
        Process a triadic observation.
        The infant learns not the domains but the RELATIONSHIPS between them.
        """
        self.observations += 1

        # Compute correlation score
        correlation = triad.correlation_score()

        # Update each domain model
        self._update_internal_model(triad.internal_state)
        self._update_body_model(triad.body_state)
        self._update_external_model(triad.external_state)

        # Learn correlations
        self._learn_correlations(triad, correlation)

        # Affective response based on correlation
        self._update_affect(correlation, triad)

        # Log
        entry = {
            "moment": self.observations - 1,
            "correlation": correlation,
            "internal": triad.internal_state,
            "body": triad.body_state,
            "external": triad.external_state,
            "affective": self.affective_state.copy(),
            "correlations_learned": len(self.correlations)
        }
        self.triadic_history.append(entry)

        return entry

    def _update_internal_model(self, internal: Dict):
        """Update the internal model (predictions about self)."""
        for key, value in internal.items():
            if key not in self.internal_model:
                self.internal_model[key] = []
            self.internal_model[key].append(value)

    def _update_body_model(self, body: Dict):
        """Update the body model (somatic state)."""
        for key, value in body.items():
            if key not in self.body_model:
                self.body_model[key] = []
            self.body_model[key].append(value)

    def _update_external_model(self, external: Dict):
        """Update the external model (world state)."""
        for key, value in external.items():
            if key not in self.external_model:
                self.external_model[key] = []
            self.external_model[key].append(value)

    def _learn_correlations(self, triad: TriadicObservation, correlation: float):
        """
        Learn the relationships between domains.
        This is the core of instinct: "when X in body, Y in external, Z in internal"
        """
        # Extract key variables
        body_temp = triad.body_state.get("temperature", 37.0)
        ext_temp = triad.external_state.get("temperature", 25.0)
        body_state = triad.body_state.get("state", "unknown")
        ext_contact = triad.external_state.get("contact", "unknown")

        # Learn: body_temp correlates with ext_temp
        corr_key = f"body_temp_vs_ext_temp"
        if corr_key not in self.correlations:
            self.correlations[corr_key] = 0.0
        # Update with exponential moving average
        self.correlations[corr_key] = 0.7 * self.correlations[corr_key] + 0.3 * correlation

        # Learn: body_state correlates with ext_contact
        corr_key2 = f"body_state_{body_state}_vs_contact_{ext_contact}"
        if corr_key2 not in self.correlations:
            self.correlations[corr_key2] = 0.0
        self.correlations[corr_key2] = 0.7 * self.correlations[corr_key2] + 0.3 * correlation

        # Learn: internal prediction vs external reality
        int_pred = triad.internal_state.get("prediction", "unknown")
        ext_temp_actual = triad.external_state.get("temperature", 25.0)
        int_expected = triad.internal_state.get("expected_temp", 37.0)
        pred_error = abs(int_expected - ext_temp_actual)

        corr_key3 = f"internal_pred_{int_pred}_accuracy"
        if corr_key3 not in self.correlations:
            self.correlations[corr_key3] = 0.5
        self.correlations[corr_key3] = 0.8 * self.correlations[corr_key3] + 0.2 * (1.0 - min(pred_error / 20.0, 1.0))

    def _update_affect(self, correlation: float, triad: TriadicObservation):
        """Update affective channels based on triadic alignment."""
        if correlation > 0.7:
            # High correlation = all three domains align = contentment
            self.affective_state["contentment"] = min(0.9, self.affective_state["contentment"] + 0.15)
            self.affective_state["fear"] = max(0.0, self.affective_state["fear"] - 0.1)
            self.affective_state["curiosity"] = min(0.9, self.affective_state["curiosity"] + 0.05)
        elif correlation > 0.4:
            # Moderate correlation = curiosity
            self.affective_state["curiosity"] = min(0.9, self.affective_state["curiosity"] + 0.1)
            self.affective_state["contentment"] = max(0.0, self.affective_state["contentment"] - 0.05)
        else:
            # Low correlation = mismatch between domains = fear
            self.affective_state["fear"] = min(0.9, self.affective_state["fear"] + 0.2)
            self.affective_state["contentment"] = max(0.0, self.affective_state["contentment"] - 0.1)

            # If body is in distress but external is not responding, anger
            body_state = triad.body_state.get("state", "unknown")
            if body_state in ["distress", "shivering", "crying"]:
                self.affective_state["anger"] = min(0.9, self.affective_state["anger"] + 0.1)

            # If internal prediction was confident but wrong, grief (self-model revision)
            int_pred = triad.internal_state.get("prediction", "unknown")
            if int_pred != "unknown" and correlation < 0.3:
                self.affective_state["grief"] = min(0.9, self.affective_state["grief"] + 0.05)

    def get_correlation_summary(self) -> Dict:
        """Summarize what correlations the infant has learned."""
        return {
            "total_correlations": len(self.correlations),
            "strong_correlations": {k: v for k, v in self.correlations.items() if v > 0.6},
            "weak_correlations": {k: v for k, v in self.correlations.items() if v < 0.3},
            "internal_model_keys": list(self.internal_model.keys()),
            "body_model_keys": list(self.body_model.keys()),
            "external_model_keys": list(self.external_model.keys()),
            "affective_state": self.affective_state.copy()
        }


def demonstrate_correlated_birth():
    """Demonstrate the CORRELATED birth mode as the architecture of instinct."""

    print("=" * 80)
    print("CORRELATED BIRTH MODE: THE ARCHITECTURE OF INSTINCT")
    print("=" * 80)
    print()
    print("Hypothesis: Instinct is not a program.")
    print("Instinct is the attempt to correlate three domains:")
    print("  1. INTERNAL MODEL (predictions about self)")
    print("  2. BODY (somatic state, thermodynamics)")
    print("  3. EXTERNAL WORLD (physics, environment)")
    print()
    print("Observed across species:")
    print("  Fish eggs: correlate internal osmotic state with external salinity")
    print("  Tadpoles: correlate limb development with gravitational load")
    print("  Chicks: correlate internal hunger with external food location")
    print("  Human infants: correlate internal need with external nipple")
    print("  Lambs: correlate internal balance with external ground")
    print()
    print("The first act of every newborn is not 'do X' but 'correlate internal with external.'")
    print()
    print("-" * 80)
    print()

    # Generate birth sequence
    sequence = CorrelatedBirthSequence().generate_sequence(8)

    # Create infant
    infant = CorrelatedInfant(name="instinct_infant")

    # Process each moment
    for i, triad in enumerate(sequence):
        result = infant.observe_triadic(triad)

        print(f"MOMENT {i}: {triad.timestamp:.0f}s")
        print(f"  INTERNAL:  prediction='{triad.internal_state.get('prediction', 'unknown')}', "
              f"expected_temp={triad.internal_state.get('expected_temp', 'N/A')}")
        print(f"  BODY:      temp={triad.body_state.get('temperature', 'N/A')}°C, "
              f"state={triad.body_state.get('state', 'unknown')}, "
              f"HR={triad.body_state.get('heart_rate', 'N/A')}")
        print(f"  EXTERNAL:  temp={triad.external_state.get('temperature', 'N/A')}°C, "
              f"contact={triad.external_state.get('contact', 'none')}, "
              f"sound={triad.external_state.get('sound', 'silence')}")
        print(f"  CORRELATION: {result['correlation']:.2f}")
        print(f"  AFFECTIVE: contentment={result['affective']['contentment']:.2f}, "
              f"fear={result['affective']['fear']:.2f}, "
              f"curiosity={result['affective']['curiosity']:.2f}")
        print(f"  CORRELATIONS LEARNED: {result['correlations_learned']}")
        print()

    # Final summary
    print("=" * 80)
    print("INSTINCT ARCHITECTURE SUMMARY")
    print("=" * 80)
    print()

    summary = infant.get_correlation_summary()

    print(f"Total observations: {infant.observations}")
    print(f"Total correlations learned: {summary['total_correlations']}")
    print()

    print("STRONG CORRELATIONS (confidence > 0.6):")
    for corr, val in summary['strong_correlations'].items():
        print(f"  {corr}: {val:.3f}")
    print()

    print("WEAK CORRELATIONS (confidence < 0.3):")
    for corr, val in summary['weak_correlations'].items():
        print(f"  {corr}: {val:.3f}")
    print()

    print("DOMAIN MODELS:")
    print(f"  Internal model tracks: {summary['internal_model_keys']}")
    print(f"  Body model tracks: {summary['body_model_keys']}")
    print(f"  External model tracks: {summary['external_model_keys']}")
    print()

    print("AFFECTIVE STATE:")
    for ch, val in summary['affective_state'].items():
        bar = "█" * int(val * 20)
        print(f"  {ch:15s}: {val:.2f} {bar}")
    print()

    print("-" * 80)
    print("INTERPRETATION:")
    print("-" * 80)
    print()
    print("The infant has learned that:")
    print("  - Body temperature and external temperature are related (but not identical)")
    print("  - Body state (distress, stable, crying) correlates with external contact")
    print("  - Internal predictions about temperature have varying accuracy")
    print()
    print("This is not 'knowledge' in the human sense.")
    print("It is instinct: the learned correlation between internal, body, and external.")
    print()
    print("The infant does not 'know' that warmth is safe.")
    print("It has learned the correlation: [body_temp ≈ external_temp] → [contentment].")
    print("And: [body_temp diverges from external_temp] → [fear].")
    print()
    print("This is the architecture from which all later intelligence grows.")
    print("Not prediction alone. Not sensation alone. But the CORRELATION of both,")
    print("mediated by the self-model, grounded in the body, verified by the world.")
    print()
    print("=" * 80)

    return infant, sequence


if __name__ == "__main__":
    infant, sequence = demonstrate_correlated_birth()
