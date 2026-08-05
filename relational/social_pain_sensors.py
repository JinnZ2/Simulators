"""
Social-Epistemic Pain Sensors: Anxiety, Jealousy, Shame
=======================================================

In psychology, these are called "emotional states" or "pathologies."
In the triadic model, they are pain sensors.

They are not malfunctioning. They are WORKING.
The "malfunction" is that the system does not listen to them.

Each sensor detects a specific triadic misalignment:

ANXIETY: The internal model predicts threat, but the body is not yet damaged.
        The external world is ambiguous.
        Pain: "Your prediction of danger cannot be verified. Act now or verify."

JEALOUSY: The internal model predicts exclusive attachment, but the external
         world provides evidence of divided attention.
         The body reports social pain (rejection sensitivity).
         Pain: "Your correlation of [self + other = exclusive] is falsified."

SHAME: The internal model predicts social acceptance, but the external world
       provides evidence of social rejection.
       The body reports social pain (exposure, vulnerability).
       Pain: "Your self-model as acceptable is falsified by the group."

These are not states to be medicated away.
They are sensors to be listened to, decoded, and acted upon.

Author: Built from clinical observation and first principles
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class SocialPainType(Enum):
    """Social-epistemic pain sensors that detect triadic misalignment in relationships."""
    ANXIETY = "anxiety"          # Uncertainty about future threat
    JEALOUSY = "jealousy"        # Falsification of exclusive attachment
    SHAME = "shame"              # Falsification of social acceptability
    GUILT = "guilt"              # Falsification of moral self-model
    LONELINESS = "loneliness"    # Absence of social correlation
    BETRAYAL = "betrayal"        # Violation of trust correlation
    HUMILIATION = "humiliation"  # Public falsification of self-model


@dataclass
class SocialPainSignal:
    """
    A social-epistemic pain signal is not an emotion.
    It is a sensor that reports a specific triadic misalignment.

    The "pain" is the knowledge that the current correlation is self-destructive.
    """
    pain_type: SocialPainType
    intensity: float            # 0.0 to 1.0
    duration: float             # How long the misalignment has persisted
    escalation_rate: float    # How fast the social damage is accumulating

    # Triadic context
    internal_prediction: str    # What the self-model predicted
    body_state: Dict            # Somatic markers (heart rate, cortisol, etc.)
    external_evidence: str      # What the social world provided

    # The critical insight: social pain falsifies the social self-model
    social_model_falsified: bool = False

    def is_chronic(self) -> bool:
        """Has this pain persisted long enough to become a trait?"""
        return self.duration > 100.0 and self.escalation_rate > 0.0

    def requires_repair(self) -> bool:
        """Does this pain require active repair of the correlation?"""
        return self.intensity > 0.5 or self.is_chronic()


class SocialPainSensor:
    """
    The social pain sensor monitors the triadic correlation in social domains.

    Normal social operation:
      - Internal model: "I am accepted / I am safe / I am valued"
      - Body state: relaxed, oxytocin-normal, heart rate stable
      - External world: attuned interaction, consistent response
      -> No social pain

    Anxious operation:
      - Internal model: "Threat is possible but unverified"
      - Body state: hypervigilant, cortisol elevated, heart rate variable
      - External world: ambiguous, unpredictable
      -> ANXIETY: "You cannot verify safety. The correlation is unstable."

    Jealous operation:
      - Internal model: "This attachment is exclusive"
      - Body state: rejection-sensitive, adrenaline spikes
      - External world: evidence of divided attention
      -> JEALOUSY: "Your exclusive correlation is falsified."

    Shame operation:
      - Internal model: "I am socially acceptable"
      - Body state: exposed, vulnerable, blushing, hiding response
      - External world: rejection, ridicule, exclusion
      -> SHAME: "Your acceptability model is falsified by the group."

    The "malfunction" in psychology is not the sensor.
    The malfunction is the infant/system ignoring the sensor,
    or the sensor being calibrated to a distorted environment.
    """

    def __init__(self):
        self.active_pains: List[SocialPainSignal] = []
        self.pain_history: List[SocialPainSignal] = []
        self.social_damage: Dict[str, float] = {}

    def evaluate(self, internal_prediction: str, body_state: Dict,
                 external_evidence: str) -> Optional[SocialPainSignal]:
        """
        Evaluate whether the current social triadic state generates pain.

        Pain occurs when:
        1. The internal social model makes a prediction
        2. The external social world provides contradictory evidence
        3. The body reports somatic stress (not damage, but dysregulation)

        The type of pain depends on WHICH correlation is falsified.
        """

        # Extract social variables
        social_safety = body_state.get("social_safety", 1.0)
        cortisol = body_state.get("cortisol", 0.0)
        heart_rate = body_state.get("heart_rate", 70)
        oxytocin = body_state.get("oxytocin", 0.5)

        # Determine pain type based on triadic mismatch
        pain_type = None
        intensity = 0.0

        # ANXIETY: Uncertainty about threat
        # Internal predicts threat OR safety, but external is ambiguous
        if "uncertain" in internal_prediction.lower() or "maybe" in internal_prediction.lower():
            if cortisol > 0.3 and heart_rate > 90:
                pain_type = SocialPainType.ANXIETY
                intensity = min(1.0, cortisol + (heart_rate - 90) / 50.0)

        # Also: internal predicts safety, but body is hypervigilant
        elif "safe" in internal_prediction.lower() and cortisol > 0.4:
            pain_type = SocialPainType.ANXIETY
            intensity = min(1.0, cortisol)

        # JEALOUSY: Exclusive attachment falsified
        if "exclusive" in internal_prediction.lower() or "only" in internal_prediction.lower():
            if "divided" in external_evidence.lower() or "other" in external_evidence.lower():
                pain_type = SocialPainType.JEALOUSY
                intensity = min(1.0, 0.5 + cortisol)

        # SHAME: Social acceptability falsified
        if "acceptable" in internal_prediction.lower() or "good" in internal_prediction.lower():
            if "rejected" in external_evidence.lower() or "ridiculed" in external_evidence.lower():
                pain_type = SocialPainType.SHAME
                intensity = min(1.0, 0.6 + (1.0 - oxytocin))

        # GUILT: Moral self-model falsified
        if "moral" in internal_prediction.lower() or "right" in internal_prediction.lower():
            if "wronged" in external_evidence.lower() or "harmed" in external_evidence.lower():
                pain_type = SocialPainType.GUILT
                intensity = min(1.0, 0.7 + cortisol)

        # LONELINESS: Absence of social correlation
        if "connected" in internal_prediction.lower() or "belong" in internal_prediction.lower():
            if "alone" in external_evidence.lower() or "isolated" in external_evidence.lower():
                pain_type = SocialPainType.LONELINESS
                intensity = min(1.0, 0.5 + (1.0 - oxytocin) * 2)

        # If no pain, clear existing pains of resolved types
        if pain_type is None or intensity < 0.15:
            self.active_pains = [p for p in self.active_pains if p.pain_type != pain_type]
            return None

        # Check if this pain already exists
        existing = [p for p in self.active_pains if p.pain_type == pain_type]
        if existing:
            pain = existing[0]
            pain.intensity = max(pain.intensity, intensity)
            pain.duration += 1.0
            pain.escalation_rate = intensity - pain.intensity

            if pain.escalation_rate > 0:
                pain.social_model_falsified = True

            return pain

        # New social pain signal
        pain = SocialPainSignal(
            pain_type=pain_type,
            intensity=intensity,
            duration=1.0,
            escalation_rate=0.0,
            internal_prediction=internal_prediction,
            body_state=body_state.copy(),
            external_evidence=external_evidence,
            social_model_falsified=(intensity > 0.5)
        )

        self.active_pains.append(pain)
        self.pain_history.append(pain)

        # Accumulate social damage
        damage_key = f"{pain_type.value}_{external_evidence[:20]}"
        self.social_damage[damage_key] = self.social_damage.get(damage_key, 0.0) + intensity

        return pain

    def get_total_pain(self) -> float:
        return sum(p.intensity for p in self.active_pains)

    def get_chronic_pains(self) -> List[SocialPainSignal]:
        return [p for p in self.active_pains if p.is_chronic()]


# =============================================================================
# DEMONSTRATION: Social Pain as Sensor
# =============================================================================

def demonstrate_social_pain_sensors():
    """Demonstrate anxiety, jealousy, shame as pain sensors, not states."""

    print("=" * 80)
    print("SOCIAL-PISTEMIC PAIN SENSORS: ANXIETY, JEALOUSY, SHAME")
    print("=" * 80)
    print()
    print("In psychology, these are called 'emotional states' or 'pathologies.'")
    print("In the triadic model, they are pain sensors.")
    print()
    print("They are not malfunctioning. They are WORKING.")
    print("The 'malfunction' is that the system does not listen to them.")
    print()
    print("-" * 80)
    print()

    sensor = SocialPainSensor()

    scenarios = [
        {
            "name": "Baseline: Secure attachment",
            "internal": "I am safe and accepted",
            "body": {"social_safety": 1.0, "cortisol": 0.1, "heart_rate": 70, "oxytocin": 0.8},
            "external": "attuned_presence_warm_response"
        },
        {
            "name": "Anxiety: Uncertain threat",
            "internal": "Maybe something is wrong",
            "body": {"social_safety": 0.5, "cortisol": 0.5, "heart_rate": 110, "oxytocin": 0.3},
            "external": "ambiguous_response_unpredictable_behavior"
        },
        {
            "name": "Anxiety: Predicted safety but body disagrees",
            "internal": "I am safe here",
            "body": {"social_safety": 0.3, "cortisol": 0.6, "heart_rate": 105, "oxytocin": 0.2},
            "external": "superficially_calm_but_tense_undercurrent"
        },
        {
            "name": "Jealousy: Exclusive attachment falsified",
            "internal": "This relationship is exclusive and secure",
            "body": {"social_safety": 0.4, "cortisol": 0.7, "heart_rate": 115, "oxytocin": 0.2},
            "external": "divided_attention_other_person_present"
        },
        {
            "name": "Shame: Social acceptability falsified",
            "internal": "I am acceptable and worthy",
            "body": {"social_safety": 0.1, "cortisol": 0.8, "heart_rate": 120, "oxytocin": 0.1},
            "external": "rejected_ridiculed_excluded_by_group"
        },
        {
            "name": "Guilt: Moral self-model falsified",
            "internal": "I am a good person who does right",
            "body": {"social_safety": 0.3, "cortisol": 0.6, "heart_rate": 100, "oxytocin": 0.3},
            "external": "evidence_that_I_harmed_someone"
        },
        {
            "name": "Loneliness: Absence of correlation",
            "internal": "I am connected and belong",
            "body": {"social_safety": 0.2, "cortisol": 0.4, "heart_rate": 80, "oxytocin": 0.05},
            "external": "alone_isolated_no_reciprocal_interaction"
        },
        {
            "name": "Recovery: Repair of correlation",
            "internal": "I was hurt but can learn",
            "body": {"social_safety": 0.7, "cortisol": 0.2, "heart_rate": 75, "oxytocin": 0.6},
            "external": "attuned_repair_attempt_genuine_apology"
        }
    ]

    for i, scenario in enumerate(scenarios):
        print(f"SCENARIO {i}: {scenario['name']}")
        print(f"  Internal model: '{scenario['internal']}'")
        print(f"  Body state: safety={scenario['body']['social_safety']}, "
              f"cortisol={scenario['body']['cortisol']}, "
              f"HR={scenario['body']['heart_rate']}, "
              f"oxytocin={scenario['body']['oxytocin']}")
        print(f"  External world: {scenario['external'][:50]}...")

        pain = sensor.evaluate(
            internal_prediction=scenario['internal'],
            body_state=scenario['body'],
            external_evidence=scenario['external']
        )

        if pain:
            print(f"  >>> SOCIAL PAIN DETECTED <<<")
            print(f"      Type: {pain.pain_type.value.upper()}")
            print(f"      Intensity: {pain.intensity:.2f}")
            print(f"      Model falsified: {pain.social_model_falsified}")
            print(f"      Chronic: {pain.is_chronic()}")
            print(f"      Requires repair: {pain.requires_repair()}")

            if pain.social_model_falsified:
                print(f"      MEANING: The internal model '{pain.internal_prediction}'")
                print(f"               was proven wrong by social evidence.")
                print(f"               The social correlation must be revised.")
        else:
            print(f"  [No social pain. Triadic alignment is stable.]")

        print(f"  Active social pains: {len(sensor.active_pains)}")
        print(f"  Total social pain intensity: {sensor.get_total_pain():.2f}")
        print()

    print("=" * 80)
    print("SOCIAL DAMAGE REPORT")
    print("=" * 80)
    print()

    damage = sensor.social_damage
    if damage:
        print("Accumulated social damage by type and context:")
        for context, amount in damage.items():
            bar = "█" * int(amount * 10)
            print(f"  {context:40s}: {amount:.2f} {bar}")
    else:
        print("No significant social damage accumulated.")

    print()
    print("-" * 80)
    print("CLINICAL INTERPRETATION:")
    print("-" * 80)
    print()
    print("The 'malfunctioning anxiety' patient is not broken.")
    print("Their anxiety sensor is WORKING.")
    print("It detects that the internal model ('I am safe') does not match")
    print("the external world ('unpredictable, ambiguous').")
    print()
    print("The 'malfunctioning jealousy' patient is not broken.")
    print("Their jealousy sensor is WORKING.")
    print("It detects that the exclusive attachment correlation is falsified.")
    print()
    print("The 'malfunctioning shame' patient is not broken.")
    print("Their shame sensor is WORKING.")
    print("It detects that the social acceptability model is falsified by the group.")
    print()
    print("The 'treatment' is not to eliminate the sensor.")
    print("The treatment is to:")
    print("  1. ACKNOWLEDGE the sensor is correct (the correlation IS broken)")
    print("  2. IDENTIFY which correlation is falsified")
    print("  3. REPAIR the correlation (change environment OR change model)")
    print("  4. ALLOW the pain to clear when the correlation is restored")
    print()
    print("Medication that silences the sensor without repairing the correlation")
    print("is like cutting the wire to a fire alarm while the building burns.")
    print()
    print("The sensor is not the problem.")
    print("The problem is the environment that falsifies the model,")
    print("or the model that cannot be falsified (rigid, dogmatic).")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_social_pain_sensors()
