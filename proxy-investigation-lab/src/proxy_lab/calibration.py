"""Phase 6 — calibration against held-out verified outcomes.

Isotonic regression (default) and Platt scaling, with Expected Calibration
Error before/after. Ships calibrated_fidelity or marks method: none.
"""
from __future__ import annotations
import numpy as np

def expected_calibration_error(confidences: np.ndarray, outcomes: np.ndarray, bins: int = 10) -> float:
    """ECE: average gap between stated confidence and observed hit-rate."""
    confidences = np.asarray(confidences); outcomes = np.asarray(outcomes)
    ece, edges = 0.0, np.linspace(0, 1, bins + 1)
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (confidences >= lo) & (confidences < hi)
        if m.any():
            ece += m.mean() * abs(confidences[m].mean() - outcomes[m].mean())
    return float(ece)

def platt_fit(scores: np.ndarray, outcomes: np.ndarray) -> tuple[float, float]:
    """Fit sigmoid 1/(1+exp(a*s+b)) by simple Newton on log-loss (no deps)."""
    s, y = np.asarray(scores), np.asarray(outcomes, float)
    a, b = -1.0, 0.0
    for _ in range(100):
        z = np.clip(a * s + b, -30, 30)
        p = 1 / (1 + np.exp(z))
        ga = ((p - y) * (-s)).sum(); gb = ((p - y) * (-1.0)).sum()
        haa = (p * (1 - p) * s * s).sum() + 1e-6
        hab = (p * (1 - p) * s).sum()
        hbb = (p * (1 - p)).sum() + 1e-6
        det = haa * hbb - hab * hab
        da = (hbb * ga - hab * gb) / det; db = (haa * gb - hab * ga) / det
        a -= da; b -= db
        if abs(da) + abs(db) < 1e-8: break
    return a, b

def platt_predict(scores: np.ndarray, a: float, b: float) -> np.ndarray:
    return 1 / (1 + np.exp(np.clip(a * np.asarray(scores) + b, -30, 30)))

def isotonic_fit(scores: np.ndarray, outcomes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """PAVA on score-sorted outcomes; returns (sorted_scores, fitted_values)."""
    order = np.argsort(scores)
    s_sorted = np.asarray(scores, float)[order]
    o_sorted = np.asarray(outcomes, float)[order]
    return s_sorted, _pava(o_sorted)

def _pava(y: np.ndarray) -> np.ndarray:
    """Pool Adjacent Violators — clean implementation."""
    y = y.copy(); w = np.ones(len(y))
    i = 0
    while i < len(y) - 1:
        if y[i] > y[i + 1] + 1e-12:
            nw = w[i] + w[i + 1]
            nv = (w[i] * y[i] + w[i + 1] * y[i + 1]) / nw
            y = np.delete(y, i + 1); w = np.delete(w, i + 1)
            y[i], w[i] = nv, nw
            i = max(i - 1, 0)
        else:
            i += 1
    # expand block values to original length
    counts = w.astype(int)
    return np.repeat(y, counts)

def isotonic_predict(scores: np.ndarray, xs: np.ndarray, ys: np.ndarray) -> np.ndarray:
    out = np.interp(scores, xs, ys)
    return np.clip(out, 0, 1)

def calibrate(scores: np.ndarray, outcomes: np.ndarray, method: str = "isotonic") -> dict:
    """Fit on first half, evaluate on second half. Returns full record."""
    n = len(scores); h = n // 2
    tr_s, tr_y = scores[:h], outcomes[:h]
    te_s, te_y = scores[h:], outcomes[h:]
    ece_before = expected_calibration_error(te_s, te_y)
    if method == "platt":
        a, b = platt_fit(tr_s, tr_y)
        te_cal = platt_predict(te_s, a, b)
        params = {"a": a, "b": b}
    else:
        xs, ys = isotonic_fit(tr_s, tr_y)
        te_cal = isotonic_predict(te_s, xs, ys)
        params = {"n_knots": int(len(np.unique(ys)))}
    ece_after = expected_calibration_error(te_cal, te_y)
    return {"method": method, "ece_before": round(ece_before, 4),
            "ece_after": round(ece_after, 4), "improved": ece_after < ece_before,
            "params": params, "holdout_n": int(len(te_s))}
