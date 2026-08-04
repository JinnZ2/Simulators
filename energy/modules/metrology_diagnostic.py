#!/usr/bin/env python3
"""
metrology_diagnostic.py
The Universal 4-Gate Diagnostic for any AI or model.
Detects whether a failure lives in: Mathematics, Formulation,
Instrumentation, or Equipment.
Inspired by the coupled-quintessence tomographic verdict
(rank-2 w0-wa projection S_min ~ 0.03  ->  rank-3 tomography S_min ~ 5.2).
License: MIT
"""

import numpy as np
from scipy.linalg import svd


class MetrologyDiagnostic:
    """
    Inputs:
        x: independent variable (redshift z, time, energy, ...)
        y_obs: observed data points
        y_pred_model: model prediction at best-fit parameters
        param_names: e.g. ['lambda', 'beta', 'alpha']
        param_values: best-fit values
        covariance_matrix: parameter covariance (or None -> BIC fallback at Gate 4)
        residuals_func: (optional) params -> residuals array, for finite-diff Hessian
        fisher_matrix: (optional) Fisher information matrix; overrides Hessian estimate
    """

    S_MIN_THRESHOLD = 0.05   # the degeneracy threshold (0.029 -> 5.2 jump)
    COND_THRESHOLD = 1e5

    def __init__(self, x, y_obs, y_pred_model, param_names, param_values,
                 covariance_matrix=None, residuals_func=None, fisher_matrix=None):
        self.x = np.asarray(x, dtype=float)
        self.y_obs = np.asarray(y_obs, dtype=float)
        self.y_pred = np.asarray(y_pred_model, dtype=float)
        self.params = np.asarray(param_values, dtype=float)
        self.names = list(param_names)
        self.n_params = len(self.params)
        self.cov = None if covariance_matrix is None else np.asarray(covariance_matrix, dtype=float)
        self.fisher = None if fisher_matrix is None else np.asarray(fisher_matrix, dtype=float)
        self.res_func = residuals_func

        self.residuals = self.y_obs - self.y_pred
        self.rss = float(np.sum(self.residuals**2))
        self.n_points = len(self.x)

    def _estimate_hessian(self):
        if self.fisher is not None:
            return self.fisher
        if self.cov is not None:
            return np.linalg.inv(self.cov)
        if self.res_func is None:
            raise ValueError("Need fisher_matrix, covariance_matrix, or residuals_func.")
        eps = 1e-6
        n = self.n_params
        hess = np.zeros((n, n))
        base = self.res_func(self.params)
        rss0 = float(np.sum(base**2))
        for i in range(n):
            for j in range(n):
                pij = self.params.copy(); pij[i] += eps; pij[j] += eps
                pi = self.params.copy(); pi[i] += eps
                pj = self.params.copy(); pj[j] += eps
                hess[i, j] = (np.sum(self.res_func(pij)**2)
                              - np.sum(self.res_func(pi)**2)
                              - np.sum(self.res_func(pj)**2) + rss0) / eps**2
        return (hess + hess.T) / 2

    def run(self):
        results = {"gates": {}, "verdict": {}, "metrics": {}}

        # -------- GATE 1: Scale/Coarsening (Equipment vs. Signal) --------
        if self.n_points > 4:
            idx = np.argsort(self.x)
            half = len(idx) // 2
            res_coarse = (np.mean(np.abs(self.residuals[idx[:half]]))
                          + np.mean(np.abs(self.residuals[idx[half:]]))) / 2
            res_fine = np.mean(np.abs(self.residuals))
            ratio1 = res_fine / max(res_coarse, 1e-12)
            if ratio1 > 1.8:
                gate1, action1 = "EQUIPMENT_NOISE", "Build better hardware / reduce shot noise."
            else:
                gate1, action1 = "SYSTEMATIC_SIGNAL", "Signal is real; proceed to theory."
            results["metrics"]["residual_ratio"] = float(ratio1)
        else:
            gate1, action1 = "INSUFFICIENT_DATA", "Gather more epochs."
            results["metrics"]["residual_ratio"] = np.nan
        results["gates"]["Gate1_Scale"] = gate1
        results["verdict"]["Gate1"] = action1

        # -------- GATE 2: Cross-Validation (Calibration vs. Data) --------
        if self.n_points > 4:
            odd = np.mean(np.abs(self.residuals[::2]))
            even = np.mean(np.abs(self.residuals[1::2]))
            ratio2 = abs(odd - even) / max(odd, even, 1e-12)
            if ratio2 > 0.4:
                gate2, action2 = "EQUIPMENT_CALIBRATION", "Cross-calibrate instrument (split offset)."
            else:
                gate2, action2 = "INTRINSIC_DATA", "Data is self-consistent."
            results["metrics"]["split_ratio"] = float(ratio2)
        else:
            gate2, action2 = "INSUFFICIENT_DATA", "Cannot cross-validate."
            results["metrics"]["split_ratio"] = np.nan
        results["gates"]["Gate2_CrossVal"] = gate2
        results["verdict"]["Gate2"] = action2

        # -------- GATE 3: Hessian/Fisher Eigenspectrum (Formulation vs. Instrumentation) --------
        try:
            hess = self._estimate_hessian()
            _, S, _ = svd(hess)
            S_min, S_max = float(np.min(S)), float(np.max(S))
            cond = S_max / S_min if S_min > 1e-15 else np.inf
            results["metrics"]["S_min"] = S_min
            results["metrics"]["S_max"] = S_max
            results["metrics"]["condition_number"] = float(cond)
            results["metrics"]["fisher_eigenvalues"] = [float(s) for s in S]
            if S_min < self.S_MIN_THRESHOLD:
                gate3 = "INSTRUMENTATION_DEGENERATE"
                action3 = (f"The instrument is blind (S_min={S_min:.4f}). Increase its rank: "
                           f"add redshift-resolved (tomographic) channels.")
            elif cond > self.COND_THRESHOLD:
                gate3 = "FORMULATION_TOO_CRUDE"
                action3 = "Parameterization ill-posed. Reformulate basis (bins/PCA modes)."
            else:
                gate3 = "WELL_POSED"
                action3 = "Parameter space is observable."
        except Exception as e:
            gate3, action3 = "HESSIAN_FAILED", f"Could not compute Hessian: {e}"
            results["metrics"]["S_min"] = np.nan
        results["gates"]["Gate3_Hessian"] = gate3
        results["verdict"]["Gate3"] = action3

        # -------- GATE 4: Prior Independence / Residual Curvature --------
        if self.cov is not None and self.n_params > 0:
            try:
                Ci = np.linalg.inv(self.cov)
                mahal_actual = float(np.sqrt(self.params @ Ci @ self.params))
                mahal_flat = float(np.sqrt(self.params @ self.params))
                results["metrics"]["mahalanobis_actual"] = mahal_actual
                results["metrics"]["mahalanobis_flat"] = mahal_flat
                if mahal_flat < 2.0 and mahal_actual > 4.0:
                    gate4, action4 = "CREATE_NEW_FORMULATION", "Prior over-constraining. Re-fit flat."
                elif mahal_flat > 4.0 and mahal_actual > 4.0:
                    gate4, action4 = "CREATE_NEW_MATHEMATICS", \
                        "Theory fails even with flat priors. Derive new field equations."
                else:
                    gate4, action4 = "VALID_MODEL", "Model is consistent with data."
            except np.linalg.LinAlgError:
                gate4, action4 = "PRIOR_ERROR", "Covariance matrix is singular."
        else:
            z = self.x
            A = np.vstack([np.ones_like(z), z, z**2]).T
            coeff, *_ = np.linalg.lstsq(A, self.residuals, rcond=None)
            rss_poly = float(np.sum((self.residuals - A @ coeff)**2))
            rss = max(self.rss, 1e-30); rss_poly = max(rss_poly, 1e-30)
            bic_model = self.n_points * np.log(rss / self.n_points) + self.n_params * np.log(self.n_points)
            bic_poly = self.n_points * np.log(rss_poly / self.n_points) + 3 * np.log(self.n_points)
            results["metrics"]["bic_model"] = float(bic_model)
            results["metrics"]["bic_poly_residual"] = float(bic_poly)
            results["metrics"]["residual_poly_coeffs"] = [float(c) for c in coeff]
            if bic_poly < bic_model - 6:
                gate4 = "CREATE_NEW_MATHEMATICS"
                action4 = (f"Residuals carry curvature. Proposed term: "
                           f"{coeff[2]:.4f}*z^2 + {coeff[1]:.4f}*z + {coeff[0]:.4f}")
            else:
                gate4, action4 = "VALID_MODEL", "No residual curvature detected."
        results["gates"]["Gate4_Prior"] = gate4
        results["verdict"]["Gate4"] = action4

        # -------- FINAL SYNTHESIS --------
        g = (gate1, gate2, gate3, gate4)
        decision_matrix = {
            ("SYSTEMATIC_SIGNAL", "INTRINSIC_DATA", "INSTRUMENTATION_DEGENERATE", "CREATE_NEW_MATHEMATICS"):
                "CRITICAL: Build new tomographic instrument AND derive new field equations.",
            ("SYSTEMATIC_SIGNAL", "INTRINSIC_DATA", "INSTRUMENTATION_DEGENERATE", "VALID_MODEL"):
                "ACTION: Build new tomographic instrument (increase rank). The math is fine.",
            ("SYSTEMATIC_SIGNAL", "INTRINSIC_DATA", "INSTRUMENTATION_DEGENERATE", "CREATE_NEW_FORMULATION"):
                "ACTION: Build new tomographic instrument; then reformulate basis on the richer data.",
            ("SYSTEMATIC_SIGNAL", "INTRINSIC_DATA", "WELL_POSED", "CREATE_NEW_MATHEMATICS"):
                "ACTION: Derive new mathematics. Existing instruments are sufficient.",
            ("SYSTEMATIC_SIGNAL", "INTRINSIC_DATA", "WELL_POSED", "VALID_MODEL"):
                "VALIDATED: Model, formulation, and instrument all pass.",
            ("EQUIPMENT_NOISE", "INTRINSIC_DATA", "WELL_POSED", "VALID_MODEL"):
                "ACTION: Reduce hardware noise. Theory and instruments validated.",
            ("SYSTEMATIC_SIGNAL", "INTRINSIC_DATA", "WELL_POSED", "CREATE_NEW_FORMULATION"):
                "ACTION: Reformulate the parameter basis (e.g., w0-wa -> PCA modes).",
        }
        final_action = None
        for key, act in decision_matrix.items():
            if all(k == "*" or k == gi for k, gi in zip(key, g)):
                final_action = act
                break
        if final_action is None:
            if gate3 == "INSTRUMENTATION_DEGENERATE":
                final_action = ("ACTION: Build a higher-rank (tomographic) instrument. "
                                "The current compression has a zero eigenvalue.")
            elif gate1 == "EQUIPMENT_NOISE" or gate2 == "EQUIPMENT_CALIBRATION":
                final_action = "ACTION: Calibrate hardware against standards. Redesign survey."
            else:
                final_action = "ACTION: Manual review required. Unrecognized diagnostic signature."
        results["final_action"] = final_action
        results["summary"] = f"Gate1={gate1}, Gate2={gate2}, Gate3={gate3}, Gate4={gate4}"
        return results


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    z = np.linspace(0, 2, 50)
    params = np.array([1.1, 0.2, 0.5])
    y_obs = 1.0 / (1 + z) + 0.1 * z * np.exp(-z) + rng.normal(0, 0.02, len(z))
    y_pred = 1.0 / (1 + z)

    # Real Fisher matrices from the playground grid (geodesic foot, lambda=1.1)
    print("--- BLIND instrument (rank-2 w0-wa projection) ---")
    F_proj = np.array([[89.5, 0.0, -79.6], [0.0, 0.0, 0.0], [-79.6, 0.0, 79.0]])
    r = MetrologyDiagnostic(z, y_obs, y_pred, ['lambda', 'beta', 'alpha'],
                            params, fisher_matrix=F_proj).run()
    print(f"S_min = {r['metrics']['S_min']:.2e}")
    print(r["summary"]); print(r["final_action"])

    print("\n--- TOMOGRAPHIC instrument (rank-3, w(z)+fs8(z) bins) ---")
    F_tomo = np.array([[213.0, 0.0, -142.0], [0.0, 60.0, -10.0], [-142.0, -10.0, 200.0]])
    r2 = MetrologyDiagnostic(z, y_obs, y_pred, ['lambda', 'beta', 'alpha'],
                             params, fisher_matrix=F_tomo).run()
    print(f"S_min = {r2['metrics']['S_min']:.2f}")
    print(r2["summary"]); print(r2["final_action"])
