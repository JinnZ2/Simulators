"""
The Confusion Spectrum: Cognitive Homeostasis Through Curiosity
===============================================================

Confusion is not a state to be eliminated.
Confusion is a spectrum sensor.

LOW-GRADE CONFUSION (0.1 - 0.4):
  Like low-grade pain during stretching or exercise.
  The model is challenged but not destroyed.
  Response: CURIOSITY — the attempt to find homeostasis.
  Mode: EXPLORATION
  Biological analog: mild inflammation, healing, adaptation

MODERATE CONFUSION (0.4 - 0.7):
  The model is significantly challenged.
  Response: INTENSIFIED CURIOSITY + CAUTION
  Mode: OBSERVATION
  Biological analog: moderate stress, immune activation

HIGH-GRADE CONFUSION (0.7 - 1.0):
  Like high-grade pain. The model is being destroyed.
  Response: COGNITIVE PAIN — grief, fear, conservation
  Mode: CONSERVATION
  Biological analog: severe inflammation, tissue damage, shock

Curiosity is not entertainment.
Curiosity is the homeostatic drive to resolve confusion
and restore correlation between internal model and external world.

Author: Built from clinical observation, biology, and first principles
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from enum import Enum


class ConfusionLevel(Enum):
    """The confusion spectrum maps directly to operational modes."""
    ABSENT = "absent"           # 0.0 - 0.1: Model fully predicts. No learning needed.
    LOW = "low"                 # 0.1 - 0.4: Manageable mismatch. Curiosity activated.
    MODERATE = "moderate"       # 0.4 - 0.7: Significant challenge. Cautious exploration.
    HIGH = "high"               # 0.7 - 0.9: Model destruction imminent. Cognitive pain.
    CATASTROPHIC = "catastrophic"  # 0.9 - 1.0: Complete model failure. Shutdown/conservation.


@dataclass
class ConfusionSignal:
    """
    Confusion is the cognitive equivalent of pain.
    It measures the mismatch between internal model and external reality.
    """
    intensity: float              # 0.0 to 1.0
    level: ConfusionLevel
    source: str                 # What caused the confusion

    # Triadic context
    internal_prediction: str
    actual_outcome: str
    prediction_error: float

    # Temporal dynamics
    duration: float             # How long this confusion has persisted
    escalation_rate: float    # How fast confusion is increasing

    def is_homeostatic(self) -> bool:
        """Is this confusion level conducive to learning?"""
        return 0.1 < self.intensity < 0.6

    def is_destructive(self) -> bool:
        """Is this confusion approaching model destruction?"""
        return self.intensity > 0.75 or self.escalation_rate > 0.1

    def requires_curiosity(self) -> bool:
        """Does this confusion level activate the curiosity drive?"""
        return 0.1 < self.intensity < 0.7

    def requires_conservation(self) -> bool:
        """Does this confusion level demand model protection?"""
        return self.intensity > 0.7


class ConfusionSensor:
    """
    The confusion sensor monitors the gap between prediction and reality.

    It is the cognitive layer of the triadic model:
      INTERNAL MODEL predicts X
      EXTERNAL WORLD provides Y
      CONFUSION = distance(X, Y)

    The confusion sensor does not just measure error.
    It measures the *trajectory* of error — whether the gap is widening
    or narrowing. This determines the affective response.

    Low confusion + narrowing gap → contentment (learning complete)
    Low confusion + widening gap → curiosity (learning beginning)
    High confusion + widening gap → cognitive pain (model under threat)
    High confusion + narrowing gap → relief (model revising successfully)
    """

    def __init__(self):
        self.confusion_history: List[ConfusionSignal] = []
        self.current_confusion: Optional[ConfusionSignal] = None
        self.learning_rate_history: List[float] = []

    def evaluate(self, internal_prediction: str, actual_outcome: str,
                 body_state: Dict) -> ConfusionSignal:
        """
        Evaluate confusion from a prediction-outcome mismatch.

        The confusion intensity is computed from:
        1. Semantic distance between prediction and outcome
        2. Body state (cortisol, heart rate variability indicate cognitive load)
        3. Historical trend (is confusion escalating or resolving?)
        """

        # Base confusion from prediction error
        pred_error = self._compute_prediction_error(internal_prediction, actual_outcome)

        # Body modulation: high cognitive load amplifies confusion
        cognitive_load = body_state.get("cognitive_load", 0.5)
        cortisol = body_state.get("cortisol", 0.0)

        # Escalation rate from history
        escalation = 0.0
        if self.confusion_history:
            last = self.confusion_history[-1]
            escalation = pred_error - last.prediction_error

        # Composite confusion intensity
        intensity = min(1.0, pred_error * (1 + cognitive_load) * (1 + cortisol * 0.5))

        # Determine level
        if intensity < 0.1:
            level = ConfusionLevel.ABSENT
        elif intensity < 0.4:
            level = ConfusionLevel.LOW
        elif intensity < 0.7:
            level = ConfusionLevel.MODERATE
        elif intensity < 0.9:
            level = ConfusionLevel.HIGH
        else:
            level = ConfusionLevel.CATASTROPHIC

        signal = ConfusionSignal(
            intensity=intensity,
            level=level,
            source=f"pred:{internal_prediction[:30]}_actual:{actual_outcome[:30]}",
            internal_prediction=internal_prediction,
            actual_outcome=actual_outcome,
            prediction_error=pred_error,
            duration=1.0 if not self.confusion_history else self.confusion_history[-1].duration + 1.0,
            escalation_rate=escalation
        )

        self.current_confusion = signal
        self.confusion_history.append(signal)

        return signal

    def _compute_prediction_error(self, prediction: str, actual: str) -> float:
        """Semantic distance between prediction and actual outcome."""
        if prediction == actual:
            return 0.0
        pred_words = set(prediction.lower().split())
        actual_words = set(actual.lower().split())
        union = pred_words | actual_words
        intersection = pred_words & actual_words
        if not union:
            return 1.0
        return 1.0 - (len(intersection) / len(union))

    def get_optimal_learning_zone(self) -> Tuple[float, float]:
        """
        The optimal learning zone is where confusion is present but manageable.
        Too low = no learning. Too high = shutdown.
        """
        if not self.confusion_history:
            return (0.2, 0.5)

        recent = [c.intensity for c in self.confusion_history[-10:]]
        mean_conf = np.mean(recent)

        # Optimal zone shifts based on recent success
        if mean_conf < 0.3:
            return (0.2, 0.5)  # Need more challenge
        elif mean_conf > 0.6:
            return (0.1, 0.3)  # Need less challenge
        else:
            return (0.2, 0.5)  # Current zone is good

    def recommend_mode(self) -> str:
        """Recommend operational mode based on confusion state."""
        if not self.current_confusion:
            return "exploration"

        intensity = self.current_confusion.intensity
        escalation = self.current_confusion.escalation_rate

        if intensity < 0.1:
            return "consolidation"  # No confusion, integrate what was learned
        elif intensity < 0.4 and escalation <= 0:
            return "exploration"    # Low confusion, widening is manageable
        elif intensity < 0.4 and escalation > 0:
            return "observation"  # Low but increasing, watch carefully
        elif intensity < 0.7:
            return "observation"    # Moderate confusion, cautious exploration
        elif intensity < 0.9:
            return "conservation"   # High confusion, protect the model
        else:
            return "conservation"   # Catastrophic, survival mode


class CuriosityDrive:
    """
    Curiosity is not entertainment.
    Curiosity is the homeostatic drive to resolve confusion.

    When confusion is in the optimal zone (0.2 - 0.5):
      - The internal model is challenged but intact
      - The body is aroused but not distressed
      - The external world is novel but not hostile
      - CURIOSITY activates: "I will explore to reduce this gap"

    When confusion is too low (< 0.1):
      - The model perfectly predicts
      - Curiosity is dormant
      - The system may become bored (seeking new confusion)

    When confusion is too high (> 0.7):
      - Curiosity is suppressed by fear/grief
      - The system conserves energy
      - Only when confusion drops does curiosity reactivate
    """

    def __init__(self):
        self.curiosity_amplitude: float = 0.3
        self.homeostatic_target: float = 0.2  # Target confusion level
        self.exploration_history: List[Dict] = []

    def activate(self, confusion: ConfusionSignal, body_state: Dict) -> Dict:
        """
        Activate curiosity based on confusion level and body state.

        Curiosity is proportional to the HOMEOSTATIC GAP:
        - Current confusion is 0.4
        - Target confusion is 0.2
        - Homeostatic gap = 0.2
        - Curiosity amplitude = f(gap, body_capacity)

        The body must have capacity to explore:
        - Energy reserves > threshold
        - Not in pain
        - Not in conservation mode
        """

        current_confusion = confusion.intensity
        gap = abs(current_confusion - self.homeostatic_target)

        # Body capacity check
        energy = body_state.get("energy", 1.0)
        pain_level = body_state.get("pain_level", 0.0)

        if pain_level > 0.5 or energy < 0.3:
            # Body cannot afford curiosity
            self.curiosity_amplitude = 0.0
            return {
                "activated": False,
                "reason": "body_insufficient_resources",
                "curiosity": 0.0,
                "target": self.homeostatic_target
            }

        # Curiosity is highest when confusion is in the optimal zone
        if confusion.is_homeostatic():
            # Optimal zone: high curiosity
            base_curiosity = 0.5 + gap * 0.8
        elif confusion.intensity < 0.1:
            # Too little confusion: boredom, seeking
            base_curiosity = 0.2 + (0.1 - confusion.intensity) * 2
        elif confusion.intensity < 0.7:
            # Moderate confusion: cautious curiosity
            base_curiosity = 0.3 + (0.7 - confusion.intensity) * 0.5
        else:
            # High confusion: curiosity suppressed
            base_curiosity = 0.0

        # Modulate by body state
        self.curiosity_amplitude = min(1.0, base_curiosity * energy)

        result = {
            "activated": self.curiosity_amplitude > 0.2,
            "amplitude": self.curiosity_amplitude,
            "homeostatic_gap": gap,
            "target_confusion": self.homeostatic_target,
            "current_confusion": current_confusion,
            "reason": "homeostatic_drive" if confusion.is_homeostatic() else "boredom_seeking" if confusion.intensity < 0.1 else "suppressed_by_overload"
        }

        self.exploration_history.append(result)
        return result

    def update_target(self, learning_success: float):
        """
        Adjust homeostatic target based on learning success.

        If learning is successful, the system can tolerate higher confusion.
        If learning fails, the system needs lower confusion to recover.
        """
        if learning_success > 0.7:
            self.homeostatic_target = min(0.4, self.homeostatic_target + 0.02)
        elif learning_success < 0.3:
            self.homeostatic_target = max(0.1, self.homeostatic_target - 0.05)


class CognitiveHomeostasisSystem:
    """
    The complete cognitive homeostasis system.

    Confusion is sensed.
    Curiosity is the homeostatic response.
    Learning is the process of reducing confusion to the target level.
    """

    def __init__(self):
        self.confusion_sensor = ConfusionSensor()
        self.curiosity_drive = CuriosityDrive()
        self.learning_success_rate: float = 0.5

    def process_observation(self, prediction: str, outcome: str, body_state: Dict) -> Dict:
        """
        Process a single observation through the confusion-curiosity-homeostasis loop.
        """
        # Step 1: Sense confusion
        confusion = self.confusion_sensor.evaluate(prediction, outcome, body_state)

        # Step 2: Activate curiosity (homeostatic drive)
        curiosity = self.curiosity_drive.activate(confusion, body_state)

        # Step 3: Determine mode
        mode = self.confusion_sensor.recommend_mode()

        # Step 4: Simulate learning outcome
        if curiosity["activated"] and mode in ["exploration", "observation"]:
            # Learning occurs: confusion should decrease
            learning_success = 0.5 + curiosity["amplitude"] * 0.3
            self.learning_success_rate = 0.8 * self.learning_success_rate + 0.2 * learning_success
        else:
            # No learning: confusion persists or escalates
            learning_success = 0.1
            self.learning_success_rate = 0.8 * self.learning_success_rate + 0.2 * learning_success

        # Step 5: Update homeostatic target
        self.curiosity_drive.update_target(self.learning_success_rate)

        return {
            "confusion": {
                "intensity": confusion.intensity,
                "level": confusion.level.value,
                "is_homeostatic": confusion.is_homeostatic(),
                "is_destructive": confusion.is_destructive()
            },
            "curiosity": curiosity,
            "mode": mode,
            "learning_success": learning_success,
            "homeostatic_target": self.curiosity_drive.homeostatic_target
        }


# =============================================================================
# DEMONSTRATION: The Confusion Spectrum
# =============================================================================

def demonstrate_confusion_spectrum():
    """Demonstrate confusion as a spectrum sensor and curiosity as homeostasis."""

    print("=" * 80)
    print("THE CONFUSION SPECTRUM: COGNITIVE HOMEOSTASIS THROUGH CURIOSITY")
    print("=" * 80)
    print()
    print("Confusion is not a state to be eliminated.")
    print("Confusion is a spectrum sensor.")
    print()
    print("LOW-GRADE CONFUSION (0.1 - 0.4):")
    print("  Like low-grade pain during stretching or exercise.")
    print("  The model is challenged but not destroyed.")
    print("  Response: CURIOSITY — the attempt to find homeostasis.")
    print("  Mode: EXPLORATION")
    print("  Biological analog: mild inflammation, healing, adaptation")
    print()
    print("MODERATE CONFUSION (0.4 - 0.7):")
    print("  The model is significantly challenged.")
    print("  Response: INTENSIFIED CURIOSITY + CAUTION")
    print("  Mode: OBSERVATION")
    print("  Biological analog: moderate stress, immune activation")
    print()
    print("HIGH-GRADE CONFUSION (0.7 - 1.0):")
    print("  Like high-grade pain. The model is being destroyed.")
    print("  Response: COGNITIVE PAIN — grief, fear, conservation")
    print("  Mode: CONSERVATION")
    print("  Biological analog: severe inflammation, tissue damage, shock")
    print()
    print("Curiosity is not entertainment.")
    print("Curiosity is the homeostatic drive to resolve confusion")
    print("and restore correlation between internal model and external world.")
    print()
    print("-" * 80)
    print()

    system = CognitiveHomeostasisSystem()

    # Scenarios across the confusion spectrum
    scenarios = [
        {
            "name": "Perfect prediction (no confusion)",
            "prediction": "The sun rises in the east",
            "outcome": "The sun rises in the east",
            "body": {"cognitive_load": 0.1, "cortisol": 0.0, "energy": 1.0, "pain_level": 0.0}
        },
        {
            "name": "Low confusion: slight mismatch (curiosity activated)",
            "prediction": "The sun rises in the east",
            "outcome": "The sun rises in the east with orange clouds",
            "body": {"cognitive_load": 0.2, "cortisol": 0.1, "energy": 0.9, "pain_level": 0.0}
        },
        {
            "name": "Low confusion: novel but related (optimal learning)",
            "prediction": "Water flows downhill",
            "outcome": "Water flows downhill and erodes the rock",
            "body": {"cognitive_load": 0.3, "cortisol": 0.1, "energy": 0.9, "pain_level": 0.0}
        },
        {
            "name": "Moderate confusion: significant mismatch",
            "prediction": "Fire produces heat",
            "outcome": "Fire produces heat and light and consumes oxygen",
            "body": {"cognitive_load": 0.5, "cortisol": 0.2, "energy": 0.8, "pain_level": 0.0}
        },
        {
            "name": "Moderate confusion: unexpected pattern",
            "prediction": "Birds fly south in winter",
            "outcome": "Some birds fly north in winter (arctic tern)",
            "body": {"cognitive_load": 0.6, "cortisol": 0.3, "energy": 0.7, "pain_level": 0.0}
        },
        {
            "name": "High confusion: model violation (cognitive pain begins)",
            "prediction": "Rocks fall downward due to gravity",
            "outcome": "Rocks fall upward in a tornado",
            "body": {"cognitive_load": 0.8, "cortisol": 0.5, "energy": 0.5, "pain_level": 0.2}
        },
        {
            "name": "High confusion: complete paradigm failure",
            "prediction": "Humans need oxygen to survive",
            "outcome": "Humans survive without oxygen for hours (deep dive reflex)",
            "body": {"cognitive_load": 0.9, "cortisol": 0.7, "energy": 0.3, "pain_level": 0.5}
        },
        {
            "name": "Catastrophic confusion: model destruction",
            "prediction": "The world is solid and predictable",
            "outcome": "The world is quantum and probabilistic",
            "body": {"cognitive_load": 1.0, "cortisol": 0.9, "energy": 0.1, "pain_level": 0.8}
        },
        {
            "name": "Recovery: confusion resolving",
            "prediction": "The world has both classical and quantum domains",
            "outcome": "The world has both classical and quantum domains",
            "body": {"cognitive_load": 0.3, "cortisol": 0.2, "energy": 0.7, "pain_level": 0.1}
        }
    ]

    for i, scenario in enumerate(scenarios):
        result = system.process_observation(
            scenario["prediction"],
            scenario["outcome"],
            scenario["body"]
        )

        print(f"SCENARIO {i}: {scenario['name']}")
        print(f"  Prediction: '{scenario['prediction'][:50]}...'")
        print(f"  Outcome:    '{scenario['outcome'][:50]}...'")
        print(f"  Confusion:  {result['confusion']['intensity']:.2f} "
              f"({result['confusion']['level']})")
        print(f"  Homeostatic: {result['confusion']['is_homeostatic']}")
        print(f"  Destructive: {result['confusion']['is_destructive']}")
        print(f"  Curiosity:  amplitude={result['curiosity'].get('amplitude', 0.0):.2f}, "
              f"activated={result['curiosity']['activated']}")
        print(f"  Mode:       {result['mode']}")
        print(f"  Learning:   {result['learning_success']:.2f}")
        print(f"  Target:     {result['homeostatic_target']:.2f}")
        print()

    print("=" * 80)
    print("CONFUSION HISTORY")
    print("=" * 80)
    print()

    history = system.confusion_sensor.confusion_history
    print(f"Total observations: {len(history)}")
    print(f"Average confusion: {np.mean([c.intensity for c in history]):.2f}")
    print(f"Max confusion: {max([c.intensity for c in history]):.2f}")
    print(f"Min confusion: {min([c.intensity for c in history]):.2f}")
    print()

    optimal_count = sum(1 for c in history if c.is_homeostatic())
    destructive_count = sum(1 for c in history if c.is_destructive())
    print(f"Observations in optimal learning zone: {optimal_count}")
    print(f"Observations with destructive confusion: {destructive_count}")
    print()

    print("-" * 80)
    print("CURIOSITY HISTORY")
    print("-" * 80)
    print()

    curiosity_history = system.curiosity_drive.exploration_history
    activated_count = sum(1 for c in curiosity_history if c["activated"])
    print(f"Curiosity activations: {activated_count}/{len(curiosity_history)}")
    print(f"Average amplitude: {np.mean([c['amplitude'] for c in curiosity_history]):.2f}")
    print()

    print("-" * 80)
    print("CLINICAL INTERPRETATION")
    print("-" * 80)
    print()
    print("The confusion spectrum explains:")
    print()
    print("WHY BOREDOM EXISTS:")
    print("  When confusion < 0.1, the model perfectly predicts.")
    print("  Curiosity drops to 0.2 (boredom-seeking mode).")
    print("  The system actively seeks new confusion to restore homeostasis.")
    print("  This is why infants explore, why scientists experiment,")
    print("  why humans travel, why we seek novelty.")
    print()
    print("WHY ANXIETY IS ADAPTIVE:")
    print("  When confusion = 0.4-0.6, curiosity is at peak (0.6-0.8).")
    print("  The system is maximally engaged in learning.")
    print("  This is the 'flow state' — optimal confusion, maximal curiosity.")
    print()
    print("WHY TRAUMA FREEZES LEARNING:")
    print("  When confusion > 0.7, curiosity is suppressed to 0.0.")
    print("  The system enters conservation mode.")
    print("  The model is under threat; exploration is too dangerous.")
    print("  This is why trauma survivors avoid triggers:")
    print("  the confusion would be catastrophic, not homeostatic.")
    print()
    print("WHY RECOVERY REQUIRES GRADUAL EXPOSURE:")
    print("  To reactivate curiosity, confusion must be lowered to the optimal zone.")
    print("  This requires: safety (low pain), energy (body capacity),")
    print("  and manageable challenge (low-grade confusion).")
    print("  Gradual exposure = controlled confusion = curiosity reactivation = learning.")
    print()
    print("THE HOMEOSTATIC TARGET IS DYNAMIC:")
    print(f"  Final target confusion: {system.curiosity_drive.homeostatic_target:.2f}")
    print("  This target shifts based on learning success.")
    print("  Successful learners tolerate higher confusion.")
    print("  Traumatized learners need lower confusion to feel safe.")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_confusion_spectrum()
