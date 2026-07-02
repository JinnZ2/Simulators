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
