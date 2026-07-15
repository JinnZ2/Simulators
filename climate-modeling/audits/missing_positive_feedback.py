"""Missing Positive Feedback — CO2-driven growth loop the audit ignores.

Promoted from `frontier_stubs.py`. True system's growth rate scales with CO2
concentration; audit's growth is flat. Under a rising-CO2 ramp, the true
system's biomass diverges from the flat model — the classic warming-driven
amplifying loop that a modeler who ignores forcing coupling would miss."""

import numpy as np
from .base_audit import BaseAudit
from models.base import BaseModel
from forcing import LinearForcing


class _CO2SensitiveGrass(BaseModel):
    """Growth rises with CO2 above 380 ppm baseline. The amplifying loop."""

    def derivative(self, t, state, forcing_value):
        x = state[0]
        co2 = forcing_value.get('co2', 380.0)
        growth = 0.10 * x * (1.0 + 0.005 * (co2 - 380.0))
        death = 0.05 * x
        return [growth - death]


class _FlatGrass(BaseModel):
    """Audited: growth flat, insensitive to the CO2 driver."""

    def derivative(self, t, state, forcing_value):
        x = state[0]
        return [0.10 * x - 0.05 * x]


class MissingPositiveFeedbackAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Missing Positive Feedback",
            "True growth couples to a rising CO2 driver (380 -> 500 ppm over 100 h). "
            "Audited model treats growth as flat.")

    def duration(self):
        return 100.0

    def generate_true_system(self):
        return _CO2SensitiveGrass(), LinearForcing(380, 500, 100), [100.0]

    def generate_audited_model(self):
        return _FlatGrass()

    def compute_audit_metrics(self, true_output, audited_output):
        _, y_true = true_output
        _, y_aud = audited_output
        error = abs(float(y_true[0, -1]) - float(y_aud[0, -1]))
        failure = error > 20.0
        return {"final_biomass_error": error, "failure_detected": failure}
