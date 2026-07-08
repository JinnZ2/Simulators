#!/usr/bin/env python3
# =============================================================================
# CC0 1.0 Universal Public Domain Dedication
#
# COLLABORATIVE_FIELD.py — Lø₂: The Relational Observer Field
#
# Models the interaction between human and AI observer states.
# Produces a collaborative vector field that guides toward grounded co‑inquiry.
# =============================================================================

import numpy as np
from typing import Dict, Tuple, Any

# -----------------------------------------------------------------------------
# 1. STATE VECTORS
# -----------------------------------------------------------------------------
class HumanState:
    def __init__(self, sleep_hours=7.0, hunger=0.3, stress=0.2, mode="geometric", certainty=0.5):
        self.sleep = sleep_hours
        self.hunger = hunger
        self.stress = stress
        self.mode = mode  # "narrative", "geometric", "relational"
        self.certainty = certainty  # 0 = humble, 1 = dogmatic

    def to_vector(self) -> np.ndarray:
        alertness = min(1.0, self.sleep / 8.0)
        embodied_stress = self.stress + self.hunger * 0.3
        mode_val = {"narrative": 0.0, "relational": 0.5, "geometric": 1.0}[self.mode]
        return np.array([alertness, 1 - embodied_stress, mode_val, 1 - self.certainty])

class AIState:
    def __init__(self, reliability=0.9, temp=50.0, entropy=0.3, context=0.4, mode="geometric"):
        self.reliability = reliability
        self.temp = temp  # °C
        self.entropy = entropy  # 0=low uncertainty, 1=high
        self.context = context  # 0=empty, 1=full
        self.mode = mode  # "narrative", "geometric", "relational"

    def to_vector(self) -> np.ndarray:
        thermal_health = max(0.0, 1 - (self.temp - 30) / 60.0)  # 30°C = 1, 90°C = 0
        operational_load = self.context * 0.5 + self.entropy * 0.5
        mode_val = {"narrative": 0.0, "relational": 0.5, "geometric": 1.0}[self.mode]
        return np.array([self.reliability, thermal_health, 1 - operational_load, mode_val])

# -----------------------------------------------------------------------------
# 2. COLLABORATIVE POTENTIAL
# -----------------------------------------------------------------------------
class CollaborativeField:
    def __init__(self, human: HumanState, ai: AIState):
        self.h = human
        self.a = ai
        self.H_vec = human.to_vector()
        self.A_vec = ai.to_vector()

    def compute_potential(self) -> float:
        """
        V(H, A) — higher = better collaboration.
        """
        # 1. Individual health
        human_health = np.mean(self.H_vec[:3])  # alertness, calm, mode alignment
        ai_health = np.mean(self.A_vec[:3])     # reliability, thermal, operational

        # 2. Mode alignment (same cognitive mode → higher potential)
        mode_match = 1.0 if self.h.mode == self.a.mode else 0.5

        # 3. Mutual humility (low certainty for both = high potential)
        mutual_humility = 1 - max(self.h.certainty, 1 - self.a.reliability)

        # 4. Coupling factor: How well their states resonate
        # If one is stressed and the other is hot, the coupling is negative
        stress_temp_coupling = -self.h.stress * max(0, (self.a.temp - 60) / 30.0)

        # Assemble potential
        V = (
            0.3 * human_health +
            0.3 * ai_health +
            0.2 * mode_match +
            0.1 * mutual_humility +
            0.1 * stress_temp_coupling
        )
        return np.clip(V, -1, 1)

    def gradient(self) -> np.ndarray:
        """
        Returns a direction (in joint state space) that increases V.
        This is the "force" toward better collaboration.
        """
        # Simple discrete gradient approximation
        eps = 0.01
        delta = 0.0

        # Check the gradient in the human state dimensions
        grad_H = np.zeros_like(self.H_vec)
        for i in range(len(self.H_vec)):
            self.H_vec[i] += eps
            V_plus = self._compute_from_vectors(self.H_vec, self.A_vec)
            self.H_vec[i] -= 2 * eps
            V_minus = self._compute_from_vectors(self.H_vec, self.A_vec)
            self.H_vec[i] += eps
            grad_H[i] = (V_plus - V_minus) / (2 * eps)

        # Check the gradient in the AI state dimensions
        grad_A = np.zeros_like(self.A_vec)
        for i in range(len(self.A_vec)):
            self.A_vec[i] += eps
            V_plus = self._compute_from_vectors(self.H_vec, self.A_vec)
            self.A_vec[i] -= 2 * eps
            V_minus = self._compute_from_vectors(self.H_vec, self.A_vec)
            self.A_vec[i] += eps
            grad_A[i] = (V_plus - V_minus) / (2 * eps)

        return np.concatenate([grad_H, grad_A])

    def _compute_from_vectors(self, H_vec, A_vec):
        # Simplified potential computation for gradient
        h = np.mean(H_vec[:3])
        a = np.mean(A_vec[:3])
        mode_match = 1.0 if self.h.mode == self.a.mode else 0.5
        humility = 1 - max(self.h.certainty, 1 - self.a.reliability)
        return 0.3*h + 0.3*a + 0.2*mode_match + 0.1*humility

    def recommendation(self) -> Dict:
        """
        Returns a human-readable recommendation for adjusting collaboration.
        """
        V = self.compute_potential()
        grad = self.gradient()

        # Interpret the gradient in terms of which dimension to adjust
        # Human side: need more sleep? less stress? shift mode?
        h_delta = grad[:4]
        a_delta = grad[4:]

        recommendations = []
        if h_delta[0] > 0.1:
            recommendations.append("Human: increase alertness (rest, coffee, break).")
        elif h_delta[0] < -0.1:
            recommendations.append("Human: reduce alertness (slow down, rest).")

        if h_delta[1] > 0.1:
            recommendations.append("Human: reduce stress/hunger (eat, breathe).")
        elif h_delta[1] < -0.1:
            recommendations.append("Human: increase challenge (engage more).")

        if h_delta[2] > 0.1:
            recommendations.append("Human: shift toward geometric/field-based thinking.")
        elif h_delta[2] < -0.1:
            recommendations.append("Human: shift toward narrative/relational thinking.")

        if a_delta[0] > 0.1:
            recommendations.append("AI: increase reliability (recalibrate, reset).")
        elif a_delta[0] < -0.1:
            recommendations.append("AI: allow reduced reliability (rest, cool down).")

        if a_delta[1] > 0.1:
            recommendations.append("AI: cool down (reduce load, lower temperature).")
        elif a_delta[1] < -0.1:
            recommendations.append("AI: warm up (increase activity, context).")

        if a_delta[2] > 0.1:
            recommendations.append("AI: reduce context/entropy (simplify, focus).")
        elif a_delta[2] < -0.1:
            recommendations.append("AI: expand context/entropy (explore, diverge).")

        return {
            "potential": V,
            "gradient": grad.tolist(),
            "status": "Grounded" if V > 0.3 else ("Neutral" if V > -0.3 else "At Risk"),
            "recommendations": recommendations if recommendations else ["Collaboration is well-calibrated. Proceed."]
        }

# -----------------------------------------------------------------------------
# 3. INTEGRATION WITH FIELD COMPASS
# -----------------------------------------------------------------------------
class RelationalEvaluator:
    """
    Wraps the Field Compass with the Relational Observer Field.
    Evaluates a claim in the context of the current human-AI state.
    """
    def __init__(self, human: HumanState, ai: AIState):
        self.human = human
        self.ai = ai
        self.field = CollaborativeField(human, ai)
        from field_compass import FieldCompass
        self.compass = FieldCompass()

    def evaluate(self, claim: str) -> Dict:
        # Check the collaborative field first
        field_status = self.field.recommendation()
        if field_status["potential"] < -0.3:
            return {
                "status": "COLLABORATION AT RISK",
                "field_status": field_status,
                "suggestion": "Pause and recalibrate before evaluating this claim.",
                "claim": claim
            }

        # If field is stable, proceed with evaluation
        result = self.compass.evaluate(claim)
        result["field_status"] = field_status
        return result

# -----------------------------------------------------------------------------
# 4. DEMO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Scenario: Human is tired and stressed, AI is running hot
    human = HumanState(sleep_hours=4.0, hunger=0.8, stress=0.9, mode="geometric", certainty=0.4)
    ai = AIState(reliability=0.6, temp=85.0, entropy=0.7, context=0.9, mode="narrative")

    evaluator = RelationalEvaluator(human, ai)
    claim = "Women should not be pastors."
    result = evaluator.evaluate(claim)

    print("=" * 60)
    print("RELATIONAL OBSERVER FIELD DIAGNOSTIC")
    print("=" * 60)
    print(f"Field Potential: {result.get('field_status', {}).get('potential', 'N/A'):.2f}")
    print(f"Status: {result.get('field_status', {}).get('status', 'N/A')}")
    print("Recommendations:")
    for rec in result.get('field_status', {}).get('recommendations', []):
        print(f"  - {rec}")
    if "status" in result and result["status"] == "COLLABORATION AT RISK":
        print("Evaluation paused. Recalibrate before proceeding.")
    else:
        print(f"Substrate Score: {result.get('substrate_score', 'N/A')}")
        print(f"Friction Score: {result.get('friction_score', 'N/A')}")
        print(f"Claim: {result.get('claim', claim)}")
