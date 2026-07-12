"""Baseline grass carbon-balance model. Photosynthesis - respiration."""

import numpy as np
from .base import BaseModel
from config import GRASS_DEFAULTS


class GrassCarbonBalance(BaseModel):
    def __init__(self, params=None):
        p = GRASS_DEFAULTS.copy()
        if params:
            p.update(params)
        self.P_max = p["P_max"]
        self.T_opt = p["T_opt"]
        self.sigma = p["sigma"]
        self.R_base = p["R_base"]
        self.Q10 = p["Q10"]
        self.M = p["M"]
        self.G = p["G"]

    def _photosynthesis(self, T, light_flag):
        if not light_flag:
            return 0.0
        return self.P_max * np.exp(-((T - self.T_opt) ** 2) / (2 * self.sigma ** 2))

    def _respiration(self, T):
        return self.R_base * self.Q10 ** ((T - 20.0) / 10.0)

    def derivative(self, t, state, forcing_value):
        C = state[0]
        T = forcing_value['temperature']
        light = forcing_value['light']
        P = self._photosynthesis(T, light)
        R = self._respiration(T)
        dCdt = P - R * C * 0.01 - self.M - self.G
        return [dCdt]
