"""Cascade grass: threshold + feedback + memory. The true system whose collapse
speed the smooth-model audits systematically underestimate."""

import numpy as np
from .base import BaseModel


class CascadeGrass(BaseModel):
    """Threshold respiration jump above T_crit; soil-carbon fertility feedback;
    vulnerability memory that amplifies future heat damage."""

    def __init__(self, params=None):
        self.P_max = 12.0
        self.T_opt = 25.0
        self.sigma = 8.0
        self.R_base = 0.1
        self.Q10 = 2.0
        self.threshold_temp = 35.0
        self.respiration_jump = 8.0
        self.feedback_strength = 0.02
        self.vulnerability_rate = 0.1
        self.vuln_decay = 0.01
        self.decomp_base = 0.01
        self.transfer = 0.05
        self.initial_state = np.array([100.0, 200.0, 0.0])

    def derivative(self, t, state, forcing_value):
        C, S, V = state
        T = forcing_value['temperature']
        light = forcing_value.get('light', 1.0)

        if light:
            P = self.P_max * np.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2))
            P *= (1 + self.feedback_strength * S)
        else:
            P = 0.0

        R = self.R_base * self.Q10 ** ((T - 20.0) / 10.0)
        if T > self.threshold_temp:
            R += self.respiration_jump * (1 + V)

        if T > self.threshold_temp:
            dV = self.vulnerability_rate - self.vuln_decay * V
        else:
            dV = -self.vuln_decay * V

        decomp = self.decomp_base * S * self.Q10 ** ((T - 20.0) / 10.0)
        dC = P - R * C * 0.1 - self.transfer * C
        dS = self.transfer * C - decomp
        return [dC, dS, dV]
