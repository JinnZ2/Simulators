"""Phase 1 — measurand / indication / bridge-model decomposition."""
from dataclasses import dataclass

@dataclass
class MeasurandDecomposition:
    measurand: str       # what you want to know about nature
    indication: str      # what the instrument actually outputs
    bridge_model: str    # the math mapping indication -> measurand
    model_rung: str      # M0 | M1 | M2 | M3

    def dominant_uncertainty(self) -> str:
        return {"M0": "instrument physics", "M1": "reference standard quality",
                "M2": "empirical model transferability",
                "M3": "inverse-problem assumptions and priors"}[self.model_rung]
