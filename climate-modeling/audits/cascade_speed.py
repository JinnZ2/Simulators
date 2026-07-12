"""Cascade Speed Blindness — combined threshold + feedback + memory + fat tails.

The flagship audit. Fat-tailed heatwaves compound with vulnerability memory and
soil feedback in the true system; the smooth-audited model has none of these and
consistently underestimates how fast collapse arrives."""

import numpy as np
from scipy.interpolate import interp1d
from .base_audit import BaseAudit
from models.grass import GrassCarbonBalance
from models.cascade_grass import CascadeGrass
from forcing import FatTailedForcing


class CascadeSpeedAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Cascade Speed Blindness",
            "True: threshold + feedback + memory + fat-tailed extremes. "
            "Audited: smooth, memoryless, Gaussian-driven.")

    def duration(self):
        return 240.0

    def generate_true_system(self):
        model = CascadeGrass()
        forcing = FatTailedForcing(T_mean=22.0, amplitude=6.0, df=3, scale=4.0, seed=42)
        return model, forcing, model.initial_state

    def generate_audited_model(self):
        return GrassCarbonBalance()

    def compute_audit_metrics(self, true_output, audited_output):
        t_true, y_true = true_output
        t_aud, y_aud = audited_output
        interp = interp1d(t_aud, y_aud[0], kind='linear', fill_value='extrapolate')
        y_aud_interp = interp(t_true)
        rmse = float(np.sqrt(np.mean((y_true[0] - y_aud_interp) ** 2)))
        # time until biomass < 10 (collapse marker)
        idx_true = np.argmax(y_true[0] < 10) if np.any(y_true[0] < 10) else len(t_true)
        idx_aud = np.argmax(y_aud_interp < 10) if np.any(y_aud_interp < 10) else len(t_true)
        collapse_true = float(t_true[min(idx_true, len(t_true) - 1)])
        collapse_aud = float(t_true[min(idx_aud, len(t_true) - 1)])
        time_diff = collapse_true - collapse_aud
        # audited model consistently underestimates speed (arrives later than truth)
        failure = rmse > 15.0 or time_diff < -20
        return {"rmse": rmse,
                "collapse_time_true_h": collapse_true,
                "collapse_time_audited_h": collapse_aud,
                "audited_late_by_h": -time_diff,
                "failure_detected": failure}
