"""
Pain as Somatic Sensor: The Destruction Threshold in the Triadic Model
=======================================================================

Pain is not an emotion. Pain is a sensor.

In the triadic model of instinct:
  INTERNAL MODEL predicts: "this is safe / this is correct"
  BODY STATE reports: "damage is occurring / homeostasis is threatened"
  EXTERNAL WORLD provides: "the stimulus continues"

When all three align: contentment, curiosity, stable learning.
When internal and external mismatch: fear, avoidance.
When body reports destruction WHILE internal predicts safety: PAIN.

Pain is the signal that says:
  "Your correlation is wrong, and the cost is real."
  "Your internal model is falsified by your own tissue."
  "Stop. Revise. Or cease to exist."

Pain is the most honest sensor because it cannot be ignored.
It does not negotiate. It does not attenuate with repetition.
It escalates until the behavior stops.

Author: Built from first principles and observation
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class PainType(Enum):
    """Types of pain as somatic verification signals."""
    THERMAL = "thermal"          # Temperature damage (burn, freeze)
    MECHANICAL = "mechanical"    # Tissue damage (cut, crush, tear)
    CHEMICAL = "chemical"        # Toxic damage (poison, acid, osmotic)
    ELECTRICAL = "electrical"    # Nerve damage (current, static)
    INFLAMMATORY = "inflammatory"  # Immune response (infection, auto-immune)
    SOCIAL = "social"            # Relational damage (rejection, isolation)
    EPISTEMIC = "epistemic"      # Model-destruction (paradigm collapse, contradiction)


@dataclass
class PainSignal:
    """
    A pain signal is not an affective state. It is a somatic report.
    It carries information about the specific threat to the triadic correlation.
    """
    pain_type: PainType
    intensity: float            # 0.0 to 1.0 (threshold to destruction)
    location: str               # Where in the body/system
    duration: float             # How long the pain has persisted
    escalation_rate: float    # How fast intensity is increasing

    # Triadic context: what was the correlation when pain began?
    internal_prediction: str
    body_state_at_onset: Dict
    external_stimulus: str

    # The critical insight: pain is falsification of internal model by body state
    model_falsified: bool = False

    def is_destructive(self) -> bool:
        """Is this pain approaching tissue/system destruction?"""
        return self.intensity > 0.7 or self.escalation_rate > 0.1

    def requires_immediate_stop(self) -> bool:
        """Does this pain demand immediate cessation of behavior?"""
        return self.intensity > 0.85 or (self.duration > 5.0 and self.escalation_rate > 0.05)


class PainSensor:
    """
    The pain sensor monitors the triadic correlation for destructive mismatch.
    It is not an affective channel. It is a verification mechanism.

    Normal operation:
      - Internal model predicts safety
      - Body state reports homeostasis
      - External world provides stimulus
      -> No pain

    Painful operation:
      - Internal model predicts safety (or is uncertain)
      - Body state reports damage
      - External world continues stimulus
      -> PAIN: "Your prediction is wrong. Your body is being destroyed."

    The pain sensor is the ontological protector's enforcer within the body.
    It ensures that correlations that threaten material continuity are broken.
    """

    def __init__(self):
        self.active_pains: List[PainSignal] = []
        self.pain_history: List[PainSignal] = []
        self.damage_accumulated: Dict[str, float] = {}

    def evaluate(self, internal_prediction: str, body_state: Dict, 
                 external_stimulus: str) -> Optional[PainSignal]:
        """
        Evaluate whether the current triadic state should generate pain.

        Pain occurs when:
        1. Body reports damage (temperature extreme, tissue stress, chemical imbalance)
        2. AND external stimulus continues
        3. AND internal model does not predict this damage

        The severity depends on:
        - How wrong the internal model is
        - How fast damage is accumulating
        - How long the damage has persisted
        """

        # Check body state for damage indicators
        body_temp = body_state.get("temperature", 37.0)
        tissue_stress = body_state.get("tissue_stress", 0.0)
        chemical_balance = body_state.get("chemical_balance", 1.0)
        oxygen_level = body_state.get("oxygen_saturation", 98.0)

        # Determine pain type and intensity
        pain_type = None
        intensity = 0.0
        location = "unknown"

        # Thermal pain
        if body_temp > 42.0 or body_temp < 30.0:
            pain_type = PainType.THERMAL
            intensity = min(1.0, abs(body_temp - 37.0) / 10.0)
            location = "thermal_regulation_system"

        # Mechanical pain
        elif tissue_stress > 0.5:
            pain_type = PainType.MECHANICAL
            intensity = min(1.0, tissue_stress)
            location = body_state.get("stressed_tissue", "structural_system")

        # Chemical pain
        elif chemical_balance < 0.5:
            pain_type = PainType.CHEMICAL
            intensity = min(1.0, 1.0 - chemical_balance)
            location = "metabolic_system"

        # Oxygen deprivation pain
        elif oxygen_level < 85.0:
            pain_type = PainType.INFLAMMATORY
            intensity = min(1.0, (100.0 - oxygen_level) / 30.0)
            location = "respiratory_system"

        # If no damage, no pain
        if pain_type is None or intensity < 0.1:
            # Clear any existing pains of this type
            self.active_pains = [p for p in self.active_pains if p.pain_type != pain_type]
            return None

        # Check if this pain already exists
        existing = [p for p in self.active_pains if p.pain_type == pain_type]
        if existing:
            pain = existing[0]
            pain.intensity = max(pain.intensity, intensity)
            pain.duration += 1.0
            pain.escalation_rate = intensity - pain.intensity

            # If intensity keeps rising, model is definitely falsified
            if pain.escalation_rate > 0:
                pain.model_falsified = True

            return pain

        # New pain signal
        pain = PainSignal(
            pain_type=pain_type,
            intensity=intensity,
            location=location,
            duration=1.0,
            escalation_rate=0.0,
            internal_prediction=internal_prediction,
            body_state_at_onset=body_state.copy(),
            external_stimulus=external_stimulus,
            model_falsified=(intensity > 0.5)  # High initial intensity = model was wrong
        )

        self.active_pains.append(pain)
        self.pain_history.append(pain)

        # Accumulate damage
        damage_key = f"{pain_type.value}_{location}"
        self.damage_accumulated[damage_key] = self.damage_accumulated.get(damage_key, 0.0) + intensity

        return pain

    def get_total_pain(self) -> float:
        """Total pain intensity across all active pain signals."""
        return sum(p.intensity for p in self.active_pains)

    def get_damage_report(self) -> Dict:
        """Report accumulated damage by type and location."""
        return self.damage_accumulated.copy()

    def clear_pain(self, pain_type: PainType):
        """Pain clears when the stimulus stops or the body recovers."""
        self.active_pains = [p for p in self.active_pains if p.pain_type != pain_type]


class TriadicInfantWithPain:
    """
    The CORRELATED infant with pain sensor integrated.
    Pain is not an emotion. It is the somatic verifier.
    """

    def __init__(self, name: str = "instinct_infant_with_pain"):
        self.name = name
        self.observations = 0

        # Three-domain model
        self.internal_model: Dict = {}
        self.body_model: Dict = {}
        self.external_model: Dict = {}
        self.correlations: Dict[str, float] = {}

        # Pain sensor
        self.pain_sensor = PainSensor()

        # Affective channels
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

    def observe_triadic(self, triad, mode: str = "exploration") -> Dict:
        """Process a triadic observation with pain evaluation."""
        self.observations += 1

        # Compute base correlation
        correlation = triad.correlation_score()

        # CRITICAL: Evaluate pain BEFORE updating models
        # Pain is a sensor that reports on the CURRENT state
        internal_pred = triad.internal_state.get("prediction", "unknown")
        pain = self.pain_sensor.evaluate(
            internal_prediction=internal_pred,
            body_state=triad.body_state,
            external_stimulus=triad.external_state.get("contact", "unknown")
        )

        # If pain is destructive, override mode to conservation
        if pain and pain.is_destructive():
            mode = "conservation"
            # Pain forces immediate model revision
            self._revise_model_from_pain(pain)

        # Update domain models
        self._update_internal_model(triad.internal_state)
        self._update_body_model(triad.body_state)
        self._update_external_model(triad.external_state)

        # Learn correlations (but pain-modulated)
        self._learn_correlations(triad, correlation, pain)

        # Affective response (pain dominates)
        self._update_affect(correlation, triad, pain)

        # Log
        entry = {
            "moment": self.observations - 1,
            "correlation": correlation,
            "pain": {
                "type": pain.pain_type.value if pain else None,
                "intensity": pain.intensity if pain else 0.0,
                "model_falsified": pain.model_falsified if pain else False,
                "destructive": pain.is_destructive() if pain else False
            },
            "internal": triad.internal_state,
            "body": triad.body_state,
            "external": triad.external_state,
            "affective": self.affective_state.copy(),
            "mode": mode,
            "correlations_learned": len(self.correlations)
        }
        self.triadic_history.append(entry)

        return entry

    def _revise_model_from_pain(self, pain: PainSignal):
        """
        Pain forces model revision.
        The internal model that predicted safety is falsified by the body.
        The correlation that led to this behavior is marked as dangerous.
        """
        # Mark the internal prediction as falsified
        pred_key = pain.internal_prediction
        if pred_key in self.internal_model:
            self.internal_model[pred_key] = "FALSIFIED_BY_PAIN"

        # Mark the correlation as dangerous
        corr_key = f"pred_{pred_key}_vs_{pain.external_stimulus}"
        self.correlations[corr_key] = -1.0  # Negative correlation = avoid

        # The body has spoken. The model must change.
        print(f"    [PAIN REVISION] Model '{pred_key}' falsified by {pain.pain_type.value} pain.")
        print(f"    [PAIN REVISION] Correlation '{corr_key}' marked as DANGEROUS.")

    def _update_internal_model(self, internal: Dict):
        for key, value in internal.items():
            if key not in self.internal_model:
                self.internal_model[key] = []
            if not isinstance(self.internal_model[key], list):
                self.internal_model[key] = [self.internal_model[key]]
            self.internal_model[key].append(value)

    def _update_body_model(self, body: Dict):
        for key, value in body.items():
            if key not in self.body_model:
                self.body_model[key] = []
            self.body_model[key].append(value)

    def _update_external_model(self, external: Dict):
        for key, value in external.items():
            if key not in self.external_model:
                self.external_model[key] = []
            self.external_model[key].append(value)

    def _learn_correlations(self, triad, correlation: float, pain: Optional[PainSignal]):
        """Learn correlations, but weight by pain presence."""
        body_temp = triad.body_state.get("temperature", 37.0)
        ext_temp = triad.external_state.get("temperature", 25.0)
        body_state = triad.body_state.get("state", "unknown")
        ext_contact = triad.external_state.get("contact", "unknown")

        # If pain is present, the correlation is NEGATIVE (avoid this)
        pain_multiplier = -2.0 if pain else 1.0

        corr_key = f"body_temp_vs_ext_temp"
        if corr_key not in self.correlations:
            self.correlations[corr_key] = 0.0
        self.correlations[corr_key] = 0.7 * self.correlations[corr_key] + 0.3 * correlation * pain_multiplier

        corr_key2 = f"body_state_{body_state}_vs_contact_{ext_contact}"
        if corr_key2 not in self.correlations:
            self.correlations[corr_key2] = 0.0
        self.correlations[corr_key2] = 0.7 * self.correlations[corr_key2] + 0.3 * correlation * pain_multiplier

    def _update_affect(self, correlation: float, triad, pain: Optional[PainSignal]):
        """Affective response dominated by pain if present."""

        if pain:
            # Pain overrides all other affect
            if pain.is_destructive():
                self.affective_state["fear"] = min(0.95, pain.intensity)
                self.affective_state["anger"] = min(0.9, pain.intensity * 0.8)
                self.affective_state["contentment"] = 0.0
                self.affective_state["curiosity"] = 0.0
            else:
                self.affective_state["fear"] = min(0.7, pain.intensity)
                self.affective_state["curiosity"] = max(0.0, 0.3 - pain.intensity)

            # If model was falsified, grief (deep revision)
            if pain.model_falsified:
                self.affective_state["grief"] = min(0.9, pain.intensity * 0.6)
        else:
            # Normal affective processing
            if correlation > 0.7:
                self.affective_state["contentment"] = min(0.9, self.affective_state["contentment"] + 0.15)
                self.affective_state["fear"] = max(0.0, self.affective_state["fear"] - 0.1)
                self.affective_state["curiosity"] = min(0.9, self.affective_state["curiosity"] + 0.05)
            elif correlation > 0.4:
                self.affective_state["curiosity"] = min(0.9, self.affective_state["curiosity"] + 0.1)
                self.affective_state["contentment"] = max(0.0, self.affective_state["contentment"] - 0.05)
            else:
                self.affective_state["fear"] = min(0.9, self.affective_state["fear"] + 0.2)
                self.affective_state["contentment"] = max(0.0, self.affective_state["contentment"] - 0.1)


# =============================================================================
# DEMONSTRATION: Pain as Somatic Sensor
# =============================================================================

def demonstrate_pain_sensor():
    """Demonstrate pain as the somatic verifier in the triadic model."""

    print("=" * 80)
    print("PAIN AS SOMATIC SENSOR: THE DESTRUCTION THRESHOLD")
    print("=" * 80)
    print()
    print("Pain is not an emotion. Pain is a sensor.")
    print()
    print("In the triadic model:")
    print("  INTERNAL MODEL predicts: 'this is safe'")
    print("  BODY STATE reports: 'damage is occurring'")
    print("  EXTERNAL WORLD provides: 'the stimulus continues'")
    print()
    print("When all three align: contentment, curiosity, stable learning.")
    print("When body reports destruction WHILE internal predicts safety: PAIN.")
    print()
    print("Pain says: 'Your correlation is wrong, and the cost is real.'")
    print("Pain says: 'Your internal model is falsified by your own tissue.'")
    print("Pain says: 'Stop. Revise. Or cease to exist.'")
    print()
    print("-" * 80)
    print()

    # Create scenarios that generate pain
    scenarios = [
        {
            "name": "Normal operation (no pain)",
            "internal": {"prediction": "warmth_safe", "expected_temp": 37.0},
            "body": {"temperature": 37.0, "tissue_stress": 0.0, "chemical_balance": 1.0, "oxygen_saturation": 98, "state": "stable"},
            "external": {"temperature": 35.0, "contact": "warm_surface"}
        },
        {
            "name": "Thermal stress (pain begins)",
            "internal": {"prediction": "warmth_safe", "expected_temp": 37.0},
            "body": {"temperature": 42.5, "tissue_stress": 0.0, "chemical_balance": 1.0, "oxygen_saturation": 98, "state": "overheating"},
            "external": {"temperature": 60.0, "contact": "hot_surface"}
        },
        {
            "name": "Severe thermal damage (destructive pain)",
            "internal": {"prediction": "warmth_safe", "expected_temp": 37.0},
            "body": {"temperature": 45.0, "tissue_stress": 0.3, "chemical_balance": 0.8, "oxygen_saturation": 95, "state": "burning"},
            "external": {"temperature": 80.0, "contact": "fire"}
        },
        {
            "name": "Mechanical damage (tissue stress)",
            "internal": {"prediction": "pressure_safe", "expected_force": 0.1},
            "body": {"temperature": 37.0, "tissue_stress": 0.8, "chemical_balance": 1.0, "oxygen_saturation": 97, "state": "crushed", "stressed_tissue": "left_paw"},
            "external": {"temperature": 25.0, "contact": "trap"}
        },
        {
            "name": "Chemical damage (osmotic shock)",
            "internal": {"prediction": "water_safe", "expected_salinity": 0.9},
            "body": {"temperature": 37.0, "tissue_stress": 0.0, "chemical_balance": 0.2, "oxygen_saturation": 90, "state": "convulsing"},
            "external": {"temperature": 25.0, "contact": "fresh_water", "salinity": 0.0}
        },
        {
            "name": "Recovery (pain clears)",
            "internal": {"prediction": "avoid_hot_surface", "expected_temp": 37.0},
            "body": {"temperature": 37.0, "tissue_stress": 0.0, "chemical_balance": 1.0, "oxygen_saturation": 98, "state": "healing"},
            "external": {"temperature": 25.0, "contact": "cool_air"}
        }
    ]

    pain_sensor = PainSensor()

    for i, scenario in enumerate(scenarios):
        print(f"SCENARIO {i}: {scenario['name']}")
        print(f"  Internal: predicts '{scenario['internal']['prediction']}'")
        print(f"  Body: temp={scenario['body']['temperature']}°C, "
              f"stress={scenario['body']['tissue_stress']}, "
              f"state={scenario['body']['state']}")
        print(f"  External: temp={scenario['external']['temperature']}°C, "
              f"contact={scenario['external']['contact']}")

        pain = pain_sensor.evaluate(
            internal_prediction=scenario['internal']['prediction'],
            body_state=scenario['body'],
            external_stimulus=scenario['external']['contact']
        )

        if pain:
            print(f"  >>> PAIN DETECTED <<<")
            print(f"      Type: {pain.pain_type.value}")
            print(f"      Intensity: {pain.intensity:.2f}")
            print(f"      Location: {pain.location}")
            print(f"      Model falsified: {pain.model_falsified}")
            print(f"      Destructive: {pain.is_destructive()}")
            print(f"      Requires stop: {pain.requires_immediate_stop()}")

            if pain.model_falsified:
                print(f"      MEANING: The internal model '{pain.internal_prediction}'")
                print(f"               was proven wrong by the body.")
                print(f"               The correlation must be revised.")
        else:
            print(f"  [No pain. Body state is within tolerance.]")

        print(f"  Active pains: {len(pain_sensor.active_pains)}")
        print(f"  Total pain intensity: {pain_sensor.get_total_pain():.2f}")
        print()

    print("=" * 80)
    print("DAMAGE REPORT")
    print("=" * 80)
    print()

    damage = pain_sensor.get_damage_report()
    if damage:
        print("Accumulated damage by type and location:")
        for location, amount in damage.items():
            bar = "█" * int(amount * 10)
            print(f"  {location:30s}: {amount:.2f} {bar}")
    else:
        print("No significant damage accumulated.")

    print()
    print("-" * 80)
    print("INTERPRETATION:")
    print("-" * 80)
    print()
    print("Pain is the body's way of saying:")
    print("  'I am the ground truth. Your model is wrong. Stop.'")
    print()
    print("Unlike other sensors, pain:")
    print("  - Cannot be habituated (it escalates)")
    print("  - Cannot be ignored (it demands attention)")
    print("  - Cannot be rationalized (the tissue is damaged regardless of belief)")
    print("  - Forces model revision (the correlation is marked negative)")
    print()
    print("In the triadic model, pain is the ultimate ontological protector.")
    print("It ensures that correlations threatening material continuity are broken.")
    print("It is the sensor that keeps the infant alive long enough to learn.")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_pain_sensor()
