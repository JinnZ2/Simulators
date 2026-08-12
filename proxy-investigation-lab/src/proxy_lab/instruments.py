"""Phase 3 — instrument model: precision, noise floor, bias, provenance."""
from dataclasses import dataclass

GRADE_WEIGHT = {"measured": 1.0, "estimated": 0.5, "assumed": 0.0}

@dataclass
class Instrument:
    sensor_type: str
    precision: float
    noise_floor: float
    systematic_bias: float
    precision_source: str = "assumed"
    noise_floor_source: str = "assumed"
    systematic_bias_source: str = "assumed"

    def snr(self, effect_size: float) -> float:
        nf = max(self.noise_floor, 1e-9)
        return abs(effect_size) / nf

    def provenance_summary(self) -> dict:
        return {"precision": self.precision_source,
                "noise_floor": self.noise_floor_source,
                "systematic_bias": self.systematic_bias_source}
