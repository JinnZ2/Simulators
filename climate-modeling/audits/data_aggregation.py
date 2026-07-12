"""Data Aggregation Error — daily-mean fits vs hourly stochastic truth."""

import numpy as np
from scipy.interpolate import interp1d
from .base_audit import BaseAudit
from models.grass import GrassCarbonBalance
from forcing import StochasticForcing


class DataAggregationAudit(BaseAudit):
    def __init__(self):
        super().__init__(
            "Data Aggregation Error",
            "Fitting to daily-mean data yields biased parameters; predictions diverge from hourly truth.")

    def duration(self):
        return 200.0

    def generate_true_system(self):
        true_params = {"P_max": 12.0, "T_opt": 24.0, "sigma": 7.0, "R_base": 0.4, "Q10": 2.2}
        return GrassCarbonBalance(true_params), \
               StochasticForcing(T_mean=20.0, amplitude=8.0, noise_std=3.0, seed=123), \
               [100.0]

    def generate_audited_model(self):
        # parameters as if fit to daily-mean data (biased toward smoother, warmer response)
        biased_params = {"P_max": 11.0, "T_opt": 25.5, "sigma": 8.5, "R_base": 0.35, "Q10": 1.9}
        return GrassCarbonBalance(biased_params)

    def compute_audit_metrics(self, true_output, audited_output):
        t_true, y_true = true_output
        t_aud, y_aud = audited_output
        # interpolate audited onto true time grid
        interp = interp1d(t_aud, y_aud[0], kind='linear', fill_value='extrapolate')
        y_aud_interp = interp(t_true)
        rmse = float(np.sqrt(np.mean((y_true[0] - y_aud_interp) ** 2)))
        max_err = float(np.max(np.abs(y_true[0] - y_aud_interp)))
        failure = rmse > 5.0
        return {"rmse": rmse, "max_error": max_err, "failure_detected": failure}
