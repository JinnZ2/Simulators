"""Phase Change Blindness — smooth mortality curve vs true step threshold."""

import numpy as np
from .base_audit import BaseAudit
from models.grass import GrassCarbonBalance
from forcing import RampForcing


class _StepMortalityGrass(GrassCarbonBalance):
    """True system: sharp respiration jump above 35°C."""
    def _respiration(self, T):
        base = super()._respiration(T)
        if T > 35.0:
            base += 8.0
        return base


class PhaseChangeAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Phase Change Blindness",
            "True system has a sharp threshold at 35°C; audited model uses smooth response.")

    def duration(self):
        return 140.0

    def generate_true_system(self):
        model = _StepMortalityGrass()
        forcing = RampForcing(T_start=20, T_end=42, duration=120, amplitude=5.0)
        return model, forcing, [100.0]

    def generate_audited_model(self):
        return GrassCarbonBalance()

    def compute_audit_metrics(self, true_output, audited_output):
        _, y_true = true_output
        _, y_aud = audited_output
        final_err = abs(float(y_true[0, -1]) - float(y_aud[0, -1]))
        failure = final_err > 15.0
        return {"final_biomass_error": final_err, "failure_detected": failure}
