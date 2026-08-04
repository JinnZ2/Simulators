#!/usr/bin/env python3
"""
falsification_engine.py
A general-purpose metrology and audit tool for any AI.
Lets the AI make a claim, falsify it against residual topology,
search for hidden variables, evolve the claim, and retest.
Pure Karl Popper, translated into linear algebra. Runs on a phone.
License: MIT - use freely, let the machines think critically.
"""

import numpy as np
import json
from collections import deque


class FalsifiableClaim:
    """A scientific claim (model) that can test itself against data.
    Discipline-agnostic: cosmology, economics, epidemiology, engineering."""

    def __init__(self, X, Y_observed, Y_predicted, parameter_names=None,
                 claim_description="Untitled Claim"):
        self.X = np.atleast_2d(np.asarray(X, dtype=float))
        if self.X.shape[0] != len(np.atleast_1d(Y_observed)) and self.X.shape[1] == len(np.atleast_1d(Y_observed)):
            self.X = self.X.T
        self.Y_obs = np.asarray(Y_observed, dtype=float)
        self.Y_pred = np.asarray(Y_predicted, dtype=float)
        self.n_samples = len(self.Y_obs)
        self.claim = claim_description
        self.param_names = parameter_names or [f"p{i}" for i in range(self.X.shape[1])]

        self.residuals = self.Y_obs - self.Y_pred
        self.RSS = float(np.sum(self.residuals**2))
        self.TSS = float(np.sum((self.Y_obs - np.mean(self.Y_obs))**2))
        self.R2 = 1 - self.RSS / self.TSS if self.TSS > 0 else 0.0

        self.history = deque(maxlen=10)
        self.current_round = 0
        self.last_tests = None

    def run_audit_battery(self):
        tests = {}

        # Test 1: BIC vs null model
        k = self.X.shape[1]
        rss = max(self.RSS, 1e-30); tss = max(self.TSS, 1e-30)
        bic_model = self.n_samples * np.log(rss / self.n_samples) + k * np.log(self.n_samples)
        bic_null = self.n_samples * np.log(tss / self.n_samples) + 1 * np.log(self.n_samples)
        tests['BIC_improvement'] = float(bic_null - bic_model)
        tests['is_explanatory'] = bool(tests['BIC_improvement'] > 0)

        # Test 2: Durbin-Watson (hidden trend / hidden variable)
        dw = float(np.sum(np.diff(self.residuals)**2) / (self.RSS + 1e-12))
        tests['Durbin_Watson'] = dw
        tests['has_trend_residual'] = bool(dw < 1.2 or dw > 2.8)

        # Test 3: Structural break (the "memory horizon" detector)
        if self.n_samples > 10:
            cumsum = np.cumsum(self.residuals)
            max_cum = float(np.max(np.abs(cumsum))
                            / (np.std(self.residuals) * np.sqrt(self.n_samples) + 1e-12))
            tests['structural_break_score'] = max_cum
            tests['has_structural_break'] = bool(max_cum > 1.5)
            tests['break_location'] = float(self.X[np.argmax(np.abs(cumsum)), 0])
        else:
            tests['has_structural_break'] = False

        # Test 4: Heteroskedasticity (missed interaction)
        if self.X.shape[1] >= 1 and np.std(self.residuals) > 0:
            rho = float(np.corrcoef(np.abs(self.residuals), self.X[:, 0])[0, 1])
            tests['variance_correlation'] = rho
            tests['has_heteroskedasticity'] = bool(np.abs(rho) > 0.3)
        else:
            tests['has_heteroskedasticity'] = False

        tests['is_falsified'] = bool(
            tests['has_trend_residual'] or
            tests.get('has_structural_break', False) or
            tests['has_heteroskedasticity'] or
            self.R2 < 0.1)
        tests['R2'] = float(self.R2)
        tests['claim'] = self.claim
        tests['round'] = self.current_round
        self.last_tests = tests
        return tests

    def search_for_hidden_variable(self):
        """Reverse-engineer residuals into candidate new terms."""
        suggestions = []
        if self.X.shape[1] == 1:
            x = self.X[:, 0]
            coeffs = np.polyfit(x, self.residuals, 2)
            if abs(coeffs[0]) > 0.01:
                suggestions.append({
                    "type": "polynomial_curvature",
                    "term": f"{coeffs[0]:.4f}*x^2 + {coeffs[1]:.4f}*x",
                    "equation": f"Y_new = Y_old + {coeffs[0]:.4f}*X^2 + {coeffs[1]:.4f}*X",
                    "strength": float(abs(coeffs[0]))})
            cumsum = np.cumsum(self.residuals)
            bi = int(np.argmax(np.abs(cumsum)))
            if 0 < bi < self.n_samples - 1:
                bx = float(x[bi])
                suggestions.append({
                    "type": "structural_break",
                    "term": f"Heaviside(X - {bx:.3f})",
                    "equation": f"Y_new = Y_old + gamma * (X > {bx:.3f})",
                    "strength": float(np.std(self.residuals[:bi])
                                      / (np.std(self.residuals[bi:]) + 1e-12))})
        if self.X.shape[1] == 2:
            x1, x2 = self.X[:, 0], self.X[:, 1]
            corr = float(np.corrcoef(self.residuals, x1 * x2)[0, 1])
            if abs(corr) > 0.2:
                suggestions.append({
                    "type": "interaction",
                    "term": f"X1 * X2 (correlation = {corr:.2f})",
                    "equation": "Y_new = Y_old + gamma * X1 * X2",
                    "strength": abs(corr)})
        return suggestions

    def evolve_claim(self, suggestions=None):
        if suggestions is None:
            suggestions = self.search_for_hidden_variable()
        if not suggestions:
            return None
        best = max(suggestions, key=lambda s: s['strength'])
        if self.X.shape[1] == 1:
            x = self.X[:, 0]
            if best['type'] == 'polynomial_curvature':
                c = np.polyfit(x, self.residuals, 2)
                delta = c[0] * x**2 + c[1] * x
                desc = f"{self.claim} + {c[0]:.3f}*X^2 + {c[1]:.3f}*X"
            elif best['type'] == 'structural_break':
                bx = float(best['term'].split('(')[-1].split(')')[0].split('-')[-1])
                mask = x > bx
                delta = np.where(mask,
                                 np.mean(self.residuals[mask]) if np.any(mask) else 0.0,
                                 np.mean(self.residuals[~mask]) if np.any(~mask) else 0.0)
                desc = f"{self.claim} + Shift at X={bx:.3f}"
            else:
                return None
        elif best['type'] == 'interaction':
            x1, x2 = self.X[:, 0], self.X[:, 1]
            coef = float(np.polyfit(x1 * x2, self.residuals, 1)[0])
            delta = coef * x1 * x2
            desc = f"{self.claim} + {coef:.3f}*X1*X2"
        else:
            return None

        evolved = FalsifiableClaim(self.X, self.Y_obs, self.Y_pred + delta,
                                   self.param_names, desc)
        evolved.current_round = self.current_round + 1
        self.history.append({'round': self.current_round, 'claim': self.claim,
                             'R2': self.R2, 'tests': self.last_tests,
                             'suggestions': suggestions, 'evolved_to': desc})
        return evolved

    def iterative_falsification(self, max_rounds=5, tolerance=0.01, verbose=True):
        current = self
        results = []
        for i in range(max_rounds):
            tests = current.run_audit_battery()
            results.append({'round': i, 'claim': current.claim, 'R2': current.R2,
                            'is_falsified': tests['is_falsified'], 'tests': tests})
            if verbose:
                print(f"--- Round {i} ---")
                print(f"Claim: {current.claim}")
                print(f"R2: {current.R2:.4f}  Falsified: {tests['is_falsified']}")
            if not tests['is_falsified']:
                if verbose:
                    print("CLAIM VALIDATED. No further falsification found.")
                break
            suggestions = current.search_for_hidden_variable()
            if not suggestions:
                if verbose:
                    print("Claim falsified, but no hidden variable found. Manual theory required.")
                break
            if verbose:
                print(f"Hidden variables found: {[s['term'] for s in suggestions]}")
            new_claim = current.evolve_claim(suggestions)
            if new_claim is None:
                break
            if abs(new_claim.R2 - current.R2) < tolerance and i > 0:
                if verbose:
                    print("Converged. Further evolution yields no improvement.")
                current = new_claim
                break
            current = new_claim
        return current, results


if __name__ == "__main__":
    print("=== FALSIFICATION ENGINE DEMO ===")
    z = np.linspace(0, 2, 50)
    Y_true = 1.0 / (1 + z) + 0.2 * z**2 * np.exp(-z)   # hidden curvature term
    Y_pred_naive = 1.0 / (1 + z)
    claim = FalsifiableClaim(z, Y_true, Y_pred_naive,
                             parameter_names=['H0', 'Omega_m'],
                             claim_description="Baseline expansion without late-time curvature.")
    final_claim, history = claim.iterative_falsification(max_rounds=3)
    print("\n" + "=" * 50)
    print("FINAL DIAGNOSTIC REPORT (JSON):")
    print(json.dumps({
        "final_claim": final_claim.claim,
        "final_R2": final_claim.R2,
        "final_residual_std": float(np.std(final_claim.residuals)),
        "iterations": len(history),
        "is_validated": not history[-1]['is_falsified'],
        "metrology_verdict": "MATHEMATICS_NEEDS_UPDATE" if history[-1]['is_falsified']
                             else "INSTRUMENT_VALIDATED"}, indent=2))
