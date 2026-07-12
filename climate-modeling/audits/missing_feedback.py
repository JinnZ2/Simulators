"""Missing Feedback — true system has soil-plant coupling; audit ignores it."""

import numpy as np
from .base_audit import BaseAudit
from models.base import BaseModel
from forcing import DiurnalTemperature


class _TwoStateGrassSoil(BaseModel):
    """Grass biomass C coupled to soil carbon S. S enhances P via fertility."""

    def __init__(self, feedback_strength=0.02):
        self.feedback_strength = feedback_strength
        self.P_max = 10.0
        self.T_opt = 25.0
        self.sigma = 8.0
        self.R_base = 0.1
        self.Q10 = 2.0
        self.transfer = 0.05
        self.decomp_base = 0.01

    def derivative(self, t, state, forcing_value):
        C, S = state
        T = forcing_value['temperature']
        light = forcing_value['light']
        P = self.P_max * np.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2))
        P *= (1 + self.feedback_strength * S) if light else 0.0
        if not light:
            P = 0.0
        R = self.R_base * self.Q10 ** ((T - 20) / 10)
        dC = P - R * C * 0.1 - self.transfer * C
        dS = self.transfer * C - self.decomp_base * S * self.Q10 ** ((T - 20) / 10)
        return [dC, dS]


class _SimpleGrassNoFeedback(BaseModel):
    """Audited: grass only, no soil coupling."""

    def __init__(self):
        self.P_max = 10.0
        self.T_opt = 25.0
        self.sigma = 8.0
        self.R_base = 0.1
        self.Q10 = 2.0
        self.transfer = 0.05

    def derivative(self, t, state, forcing_value):
        C = state[0]
        T = forcing_value['temperature']
        light = forcing_value['light']
        P = self.P_max * np.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2))
        if not light:
            P = 0.0
        R = self.R_base * self.Q10 ** ((T - 20) / 10)
        dC = P - R * C * 0.1 - self.transfer * C
        return [dC]


class MissingFeedbackAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Missing Feedback",
            "True system: grass-soil fertility feedback. Audited: single-state grass, no soil.")

    def duration(self):
        return 200.0

    def generate_true_system(self):
        return _TwoStateGrassSoil(feedback_strength=0.02), DiurnalTemperature(T_mean=22.0, amplitude=8.0), [100.0, 200.0]

    def generate_audited_model(self):
        return _SimpleGrassNoFeedback()

    def compute_audit_metrics(self, true_output, audited_output):
        _, y_true = true_output
        _, y_aud = audited_output
        final_err = abs(float(y_true[0, -1]) - float(y_aud[0, -1]))
        failure = final_err > 5.0
        return {"final_biomass_error": final_err, "failure_detected": failure}
