"""Stationarity Assumption — model calibrated to stationary window, forcing trends."""

import numpy as np
from .base_audit import BaseAudit
from models.grass import GrassCarbonBalance
from forcing import TrendForcing, DiurnalTemperature


class StationarityAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Stationarity Assumption",
            "True forcing has a slow warming trend; audited model was tuned to stationary early window.")

    def duration(self):
        return 200.0

    def generate_true_system(self):
        model = GrassCarbonBalance()
        forcing = TrendForcing(T_start=20.0, trend_rate=0.03, amplitude=5.0)
        return model, forcing, [100.0]

    def generate_audited_model(self):
        return GrassCarbonBalance()

    def run(self):
        # override run to give audited model a stationary forcing (the wrong assumption)
        true_model, forcing, init = self.generate_true_system()
        t_true, y_true = true_model.simulate(forcing, init, t_span=(0, self.duration()))
        audited_model = self.generate_audited_model()
        stat_forcing = DiurnalTemperature(T_mean=20.0, amplitude=5.0)
        t_aud, y_aud = audited_model.simulate(stat_forcing, init, t_span=(0, self.duration()))
        metrics = self.compute_audit_metrics((t_true, y_true), (t_aud, y_aud))
        return {
            "audit_name": self.name,
            "failure_detected": metrics.pop("failure_detected"),
            "metrics": metrics,
            "true_final": float(y_true[0, -1]),
            "audited_final": float(y_aud[0, -1]),
        }

    def compute_audit_metrics(self, true_output, audited_output):
        _, y_true = true_output
        _, y_aud = audited_output
        final_err = abs(float(y_true[0, -1]) - float(y_aud[0, -1]))
        failure = final_err > 10.0
        return {"final_biomass_error": final_err, "failure_detected": failure}
