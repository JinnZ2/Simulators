"""Omitted Variable — true growth needs moisture; audit assumes it constant."""

import numpy as np
from .base_audit import BaseAudit
from models.base import BaseModel
from forcing import DiurnalTemperature


class _MoistureDependentGrass(BaseModel):
    def __init__(self):
        self.P_max = 10.0
        self.T_opt = 25.0
        self.sigma = 8.0
        self.R_base = 0.1
        self.Q10 = 2.0

    def derivative(self, t, state, forcing_value):
        C = state[0]
        T = forcing_value['temperature']
        light = forcing_value['light']
        moisture = forcing_value.get('moisture', 0.5)
        P = self.P_max * np.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2)) * moisture
        if not light:
            P = 0.0
        R = self.R_base * self.Q10 ** ((T - 20) / 10)
        dC = P - R * C * 0.1
        return [dC]


class _NaiveGrass(BaseModel):
    """Modeler assumes moisture is constant 0.7."""

    def __init__(self, assumed_moisture=0.7):
        self.assumed_moisture = assumed_moisture
        self.P_max = 10.0
        self.T_opt = 25.0
        self.sigma = 8.0
        self.R_base = 0.1
        self.Q10 = 2.0

    def derivative(self, t, state, forcing_value):
        C = state[0]
        T = forcing_value['temperature']
        light = forcing_value['light']
        P = self.P_max * np.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2)) * self.assumed_moisture
        if not light:
            P = 0.0
        R = self.R_base * self.Q10 ** ((T - 20) / 10)
        dC = P - R * C * 0.1
        return [dC]


class _MoistureForcing:
    def __init__(self, base_forcing):
        self.base = base_forcing

    def __call__(self, t):
        raw = self.base(t)
        # slow oscillation between 0.2 and 0.8
        moisture = 0.5 + 0.3 * np.sin(2 * np.pi * t / 50.0)
        raw['moisture'] = moisture
        return raw


class OmittedVariableAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Omitted Variable",
            "True growth depends on hidden soil-moisture cycle; audit assumes constant moisture.")

    def duration(self):
        return 200.0

    def generate_true_system(self):
        forcing = _MoistureForcing(DiurnalTemperature(T_mean=22, amplitude=8))
        return _MoistureDependentGrass(), forcing, [100.0]

    def generate_audited_model(self):
        return _NaiveGrass(assumed_moisture=0.7)

    def compute_audit_metrics(self, true_output, audited_output):
        _, y_true = true_output
        _, y_aud = audited_output
        final_err = abs(float(y_true[0, -1]) - float(y_aud[0, -1]))
        failure = final_err > 5.0
        return {"final_biomass_error": final_err, "failure_detected": failure}
