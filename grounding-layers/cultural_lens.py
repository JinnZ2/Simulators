#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# cultural_lens.py — Lψ: Cultural Epistemology Layer
#
# Audits claims for cultural, cognitive, and epistemic biases.
# This module implements a pluggable bias detector system.
# =============================================================================

import re
from typing import Dict, List, Any, Optional

class CulturalLens:
    """
    A meta-auditor that checks the epistemic assumptions and biases
    in a claim or evaluation context.
    """

    def __init__(self):
        self.active_lens = "linear_propositional"  # default Western scientific lens
        self.lens_modes = {
            "linear_propositional": "Privileges narrative, logic, and falsification.",
            "geometric_field": "Privileges topology, probability, and pattern-recognition.",
            "relational": "Privileges relationship, context, and emergent meaning.",
        }
        # Bias registry: each detector returns (flag_id, description) if triggered.
        self.bias_detectors = [
            self._detect_human_centrism,
            # Add more detectors here as we implement them:
            # self._detect_in_group_out_group,
            # self._detect_confirmation_bias,
            # etc.
        ]

    # -------------------------------------------------------------------------
    # Bias Detectors (each returns a flag string if triggered)
    # -------------------------------------------------------------------------

    def _detect_human_centrism(self, text: str) -> Optional[str]:
        """Flags anthropocentric claims (GL_B_015)."""
        patterns = [
            "only true intelligence",
            "human is the measure",
            "human exceptionalism",
            "we are special",
            "the universe revolves around",
            "humanity is the pinnacle",
            "human-centric",
            "anthropocentric",
            "humans are the only",
            "man is the measure",
        ]
        for p in patterns:
            if p in text.lower():
                return "GL_B_015"
        return None

    # -------------------------------------------------------------------------
    # Lens Detection (cognitive mode inference)
    # -------------------------------------------------------------------------

    def _is_field_based(self, text: str) -> bool:
        field_indicators = ["likely", "probably", "maybe", "tends to", "field", "gradient", "distribution"]
        return any(ind in text.lower() for ind in field_indicators)

    def _is_relational(self, text: str) -> bool:
        relational_indicators = ["relationship", "between", "context", "system", "emergence"]
        return any(ind in text.lower() for ind in relational_indicators)

    def _infer_lens(self, text: str) -> str:
        if self._is_field_based(text):
            return "geometric_field"
        elif self._is_relational(text):
            return "relational"
        else:
            return "linear_propositional"

    # -------------------------------------------------------------------------
    # Main Annotation Method
    # -------------------------------------------------------------------------

    def annotate(self, claim: str, test_results: Dict) -> Dict:
        """
        Attach a lens annotation and bias flags to the test results.
        """
        inferred_lens = self._infer_lens(claim)
        active_lens = self.active_lens

        annotation = {
            "active_lens": active_lens,
            "inferred_lens": inferred_lens,
            "lens_description": self.lens_modes.get(inferred_lens, "Unknown"),
            "warning": None,
        }

        # Check for lens mismatch
        if inferred_lens != active_lens:
            annotation["warning"] = (
                f"This claim appears to be {inferred_lens}, but was evaluated using "
                f"{active_lens}. Results may reflect methodological bias."
            )

        # Run all bias detectors
        bias_flags = []
        for detector in self.bias_detectors:
            flag = detector(claim)
            if flag:
                bias_flags.append(flag)

        # Attach to results
        test_results["cultural_lens"] = annotation
        test_results["bias_flags"] = bias_flags

        return test_results


# -----------------------------------------------------------------------------
# Demo
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    lens = CulturalLens()
    sample_claims = [
        "Human intelligence is the only true intelligence in the universe.",
        "The economic system will likely stabilize, but there are multiple gradients.",
        "The relationship between soil health and crop yield is systemic.",
        "Women must never be pastors."
    ]
    for claim in sample_claims:
        result = lens.annotate(claim, {})
        print(f"\nClaim: {claim}")
        print(f"  Inferred Lens: {result['cultural_lens']['inferred_lens']}")
        print(f"  Bias Flags: {result['bias_flags']}")
        if result['cultural_lens'].get('warning'):
            print(f"  ⚠️  {result['cultural_lens']['warning']}")



#!/usr/bin/env python3
# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
#
# CULTURAL_LENS.py — Lψ: The Cultural Epistemology Layer
#
# Audits the testing framework itself for cultural and cognitive bias.
# Attaches a "lens annotation" to every claim evaluation.
# =============================================================================

class CulturalLens:
    """
    A meta-auditor that checks the epistemic assumptions
    of the testing process itself.
    """
    def __init__(self):
        self.lens_modes = {
            "linear_propositional": "Privileges narrative, logic, and falsification.",
            "geometric_field": "Privileges topology, probability, and pattern-recognition.",
            "relational": "Privileges relationship, context, and emergent meaning.",
        }
        self.active_lens = "linear_propositional"  # Default for Western science

    def annotate(self, claim: str, test_results: dict) -> dict:
        """
        Attach a lens annotation to the test results.
        """
        # Detect if the claim appears to be framed in a non-linear way
        if self._is_field_based(claim):
            lens = "geometric_field"
        elif self._is_relational(claim):
            lens = "relational"
        else:
            lens = "linear_propositional"

        annotation = {
            "active_lens": lens,
            "description": self.lens_modes[lens],
            "warning": None,
        }

        # If the claim was evaluated with a lens that doesn't match its mode,
        # flag a potential bias.
        if lens != self.active_lens:
            annotation["warning"] = (
                f"This claim appears to be {lens}, but was evaluated using "
                f"{self.active_lens}. Results may reflect methodological bias."
            )

        test_results["cultural_lens"] = annotation
        return test_results

    def _is_field_based(self, text: str) -> bool:
        # Heuristic: look for terms indicating probabilistic/geometric thinking
        field_indicators = ["likely", "probably", "maybe", "tends to", "field", "gradient", "distribution"]
        return any(ind in text.lower() for ind in field_indicators)

    def _is_relational(self, text: str) -> bool:
        # Heuristic: look for terms indicating relational thinking
        relational_indicators = ["relationship", "between", "context", "system", "emergence"]
        return any(ind in text.lower() for ind in relational_indicators)

# -----------------------------------------------------------------------------
# INTEGRATION WITH FIELD COMPASS
# -----------------------------------------------------------------------------
def evaluate_with_lens(compass, claim: str):
    """
    Evaluate a claim, but first pass it through the Cultural Lens.
    """
    lens = CulturalLens()
    result = compass.evaluate(claim)
    annotated = lens.annotate(claim, result)
    return annotated

# -----------------------------------------------------------------------------
# DEMO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    from field_compass import FieldCompass
    compass = FieldCompass()

    claims = [
        "The economic system will likely stabilize, but there are multiple gradients.",
        "The relationship between soil health and crop yield is systemic.",
        "Women must never be pastors.",
    ]

    for claim in claims:
        result = evaluate_with_lens(compass, claim)
        print(f"\nClaim: {claim}")
        print(f"  Lens: {result['cultural_lens']['active_lens']}")
        print(f"  Description: {result['cultural_lens']['description']}")
        if result['cultural_lens'].get('warning'):
            print(f"  ⚠️  Warning: {result['cultural_lens']['warning']}")
        print(f"  Substrate Score: {result.get('substrate_score', 'N/A')}")
        print(f"  Friction Score: {result.get('friction_score', 'N/A')}")
