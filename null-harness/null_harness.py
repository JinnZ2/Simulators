#!/usr/bin/env python3
"""
null_harness.py -- calibrate any gate against known-answer controls.
CC0.  stdlib + numpy only.

CONTRACT
    A "gate" is any callable  f(data) -> bool | str verdict.
    The harness knows nothing else about it.
    "Fires" defaults to bool(verdict) -- non-empty string / True fires,
    False / '' / None does not.  Wrap the gate if a specific string
    verdict should count as fire (see the M2-Gate-1 demo).

NEGATIVE CONTROLS   correct answer known: gate should NOT fire.
    gen_white_noise(N, sigma)          no scale structure
    gen_wellposed_fisher(k)            identity, cond = 1
    gen_null_residual(N, sigma)        Y_obs = Y_pred + noise
    gen_smooth_surface(N)              no singularity anywhere

POSITIVE CONTROLS   correct answer known: gate MUST fire.
    gen_noise_with_z2_term(N, amp)     real hidden variable
    gen_degenerate_fisher(k, eps)      true rank deficiency
    gen_true_pole(N, x0, strength)     actual 1/(x - x0)
    gen_scale_dependent_noise(N, r)    real heteroskedasticity

RUN
    for gate in registry:
        FP = mean(gate fires on N draws of NEG)
        TP = mean(gate fires on N draws of POS)
        sweep amp/eps -> smallest positive-control amplitude at which
                          TP >= 0.5  (min detectable amplitude)

OUTPUT
    One row per gate:  name | FP | TP | min detectable amplitude

FAIL CONDITIONS
    FP > 0.10          -> not a gate         (too many false alarms)
    FP >= 0.90         -> constant-fires      (always says "yes")
    FP + TP < 0.10     -> constant-silent     (always says "no")
    |TP - FP| < 0.10   -> no discrimination   (fires at same rate on both)
    otherwise          -> "OK"

    A gate that returns FP = TP = 0 on these controls is diagnosed
    as "constant-silent, not a gate."  Same shape, other direction:
    FP = TP = 1 is "constant-fires."  Either is the diagnosis.
"""

import numpy as np
from typing import Callable, Dict, List, Optional, Tuple


# ============================================================================
# NEGATIVE CONTROLS
# ============================================================================

def gen_white_noise(N: int = 200, sigma: float = 1.0):
    """Pure IID Gaussian noise on a regular grid.  No scale structure."""
    def draw(rng):
        x = np.linspace(0.0, 1.0, N)
        y = rng.normal(0.0, sigma, size=N)
        return {"x": x, "y_obs": y, "y_pred": np.zeros(N),
                "residuals": y}
    return draw


def gen_wellposed_fisher(k: int = 3):
    """Identity Fisher matrix, condition = 1, S_min = 1."""
    def draw(rng):
        return {"fisher": np.eye(k, dtype=float)}
    return draw


def gen_null_residual(N: int = 200, sigma: float = 0.05):
    """Model matches truth, residual is pure noise."""
    def draw(rng):
        x = np.linspace(0.0, 1.0, N)
        y_true = np.sin(2.0 * np.pi * x)
        y_pred = y_true.copy()
        y_obs = y_true + rng.normal(0.0, sigma, size=N)
        return {"x": x, "y_obs": y_obs, "y_pred": y_pred,
                "residuals": y_obs - y_pred}
    return draw


def gen_smooth_surface(N: int = 200):
    """A polynomial with no singularity anywhere in the support."""
    def draw(rng):
        x = np.linspace(-1.0, 1.0, N)
        y = 1.0 + 0.5 * x + 0.25 * x * x
        return {"x": x, "y_obs": y, "y_pred": np.zeros_like(y),
                "residuals": y, "function": y}
    return draw


# ============================================================================
# POSITIVE CONTROLS   (amp / eps / strength = the sweep knob)
# ============================================================================

def gen_noise_with_z2_term(N: int = 200, amp: float = 0.3,
                           sigma: float = 0.05):
    """Residuals = noise + amp * z^2  -- a real hidden curvature term."""
    def draw(rng):
        x = np.linspace(0.0, 1.0, N)
        y_pred = np.zeros(N)
        y_obs = amp * x * x + rng.normal(0.0, sigma, size=N)
        return {"x": x, "y_obs": y_obs, "y_pred": y_pred,
                "residuals": y_obs - y_pred, "amp": amp}
    return draw


def gen_degenerate_fisher(k: int = 3, eps: float = 1e-6):
    """Fisher matrix with one small eigenvalue eps; true rank deficiency."""
    def draw(rng):
        d = np.ones(k, dtype=float); d[0] = eps
        # random orthogonal basis so it isn't diagonal in the obvious way
        Q, _ = np.linalg.qr(rng.normal(size=(k, k)))
        F = Q @ np.diag(d) @ Q.T
        return {"fisher": F, "eps": eps}
    return draw


def gen_true_pole(N: int = 200, x0: float = 0.5,
                  strength: float = 1.0, floor: float = 0.02):
    """1D grid of  f(x) = strength / (x - x0 + floor·sign(x-x0)).

    Actual 1/(x-x0) singularity clipped by floor so the array is finite.
    `strength` is the amplitude knob.
    """
    def draw(rng):
        x = np.linspace(0.0, 1.0, N)
        d = x - x0
        d = np.where(np.abs(d) < floor, np.sign(d + 1e-30) * floor, d)
        y = strength / d
        return {"x": x, "y_obs": y, "y_pred": np.zeros_like(y),
                "residuals": y, "function": y, "x0": x0,
                "strength": strength}
    return draw


def gen_scale_dependent_noise(N: int = 200, ratio: float = 5.0,
                              base_sigma: float = 0.05):
    """Residual std varies across x by a factor `ratio`."""
    def draw(rng):
        x = np.linspace(0.0, 1.0, N)
        sig = base_sigma * (1.0 + (ratio - 1.0) * x)  # sigma(x=1) = ratio * base
        y = rng.normal(0.0, sig)
        return {"x": x, "y_obs": y, "y_pred": np.zeros_like(y),
                "residuals": y, "ratio": ratio}
    return draw


# ============================================================================
# THE HARNESS
# ============================================================================

def _fire(v) -> bool:
    """Default fire predicate: Python truthiness (works for bool AND str)."""
    return bool(v)


def run_gate(gate: Callable, gen: Callable, n_draws: int = 1000,
             seed: int = 42, fire: Callable = _fire) -> float:
    """Fraction of draws on which the gate fires."""
    rng = np.random.default_rng(seed)
    hits = 0
    for _ in range(n_draws):
        data = gen(rng)
        try:
            verdict = gate(data)
        except Exception:
            verdict = False
        if fire(verdict):
            hits += 1
    return hits / n_draws


def bake_off(gate: Callable, neg_gen: Callable, pos_gen: Callable,
             n_draws: int = 1000, seed: int = 42,
             fire: Callable = _fire) -> Dict:
    """FP + TP on the two controls."""
    fp = run_gate(gate, neg_gen, n_draws=n_draws, seed=seed, fire=fire)
    tp = run_gate(gate, pos_gen, n_draws=n_draws, seed=seed + 1, fire=fire)
    return {"FP": fp, "TP": tp, "verdict": _verdict(fp, tp)}


def _verdict(fp: float, tp: float) -> str:
    """Fail-condition classifier, in the order the spec listed them."""
    if fp >= 0.90 and tp >= 0.90:
        return "CONSTANT_FIRES  (always says yes; not a gate)"
    if fp + tp < 0.10:
        return "CONSTANT_SILENT (never says yes; not a gate)"
    if fp > 0.10:
        return "TOO_MANY_FALSE_ALARMS (FP > 10%)"
    if abs(tp - fp) < 0.10:
        return "NO_DISCRIMINATION (TP ≈ FP)"
    return "OK"


def sweep_threshold(gate: Callable, pos_gen_factory: Callable,
                    amps: List[float], n_draws: int = 200,
                    seed: int = 42, fire: Callable = _fire,
                    tp_target: float = 0.5) -> Optional[float]:
    """
    Given a family gen_factory(amp) -> generator, find the smallest amp
    at which TP >= tp_target.  Returns None if no amp in the list qualifies.
    """
    for amp in sorted(amps):
        gen = pos_gen_factory(amp)
        tp = run_gate(gate, gen, n_draws=n_draws, seed=seed, fire=fire)
        if tp >= tp_target:
            return amp
    return None


# ============================================================================
# REPORTING
# ============================================================================

def report(rows: List[Dict], out=print) -> None:
    """One row per gate.  Columns: name, FP, TP, min-detectable-amp, verdict."""
    hdr = (f"{'gate':<28}{'FP':>8}{'TP':>8}"
           f"{'min_amp':>12}   verdict")
    out(hdr)
    out("-" * len(hdr))
    for r in rows:
        amp = "n/a" if r.get('min_amp') is None else f"{r['min_amp']:.4g}"
        out(f"{r['name']:<28}{r['FP']:>8.3f}{r['TP']:>8.3f}"
            f"{amp:>12}   {r['verdict']}")


# ============================================================================
# SELF-TEST
# ============================================================================

def _always_true(data):    return True
def _always_false(data):   return False
def _random_gate(data):    return bool(np.random.default_rng(0).integers(2))


def _t_always_true_is_constant_fires():
    r = bake_off(_always_true, gen_white_noise(50),
                 gen_noise_with_z2_term(50, 0.5), n_draws=100)
    assert r["FP"] == 1.0 and r["TP"] == 1.0
    assert "CONSTANT_FIRES" in r["verdict"]


def _t_always_false_is_constant_silent():
    r = bake_off(_always_false, gen_white_noise(50),
                 gen_noise_with_z2_term(50, 0.5), n_draws=100)
    assert r["FP"] == 0.0 and r["TP"] == 0.0
    assert "CONSTANT_SILENT" in r["verdict"]


def _t_real_gate_z2_detector():
    """A gate that fits a quadratic to residuals and fires if |a2| > 3-sigma."""
    def z2_gate(data):
        x, r = data["x"], data["residuals"]
        A = np.vstack([np.ones_like(x), x, x * x]).T
        coef, *_ = np.linalg.lstsq(A, r, rcond=None)
        # Standard error on coef[2] from OLS
        y_hat = A @ coef
        resid = r - y_hat
        sig2 = np.sum(resid ** 2) / max(len(x) - 3, 1)
        cov = sig2 * np.linalg.inv(A.T @ A)
        se_a2 = float(np.sqrt(cov[2, 2]))
        return abs(coef[2]) > 3.0 * se_a2
    # negative and positive controls
    r = bake_off(z2_gate, gen_white_noise(200),
                 gen_noise_with_z2_term(200, amp=0.5), n_draws=200, seed=1)
    assert r["FP"] < 0.10, r
    assert r["TP"] > 0.90, r
    assert r["verdict"] == "OK"


def _t_fisher_smin_gate():
    """S_min < 0.05 = degenerate.  Should discriminate identity from small-eig."""
    def smin(data):
        F = data["fisher"]
        S = np.linalg.svd(F, compute_uv=False)
        return float(np.min(S)) < 0.05
    r = bake_off(smin, gen_wellposed_fisher(3),
                 gen_degenerate_fisher(3, eps=1e-4), n_draws=200)
    assert r["FP"] == 0.0
    assert r["TP"] == 1.0
    assert r["verdict"] == "OK"


def _t_sweep_finds_threshold():
    def z2_gate(data):
        x, r = data["x"], data["residuals"]
        A = np.vstack([np.ones_like(x), x, x * x]).T
        coef, *_ = np.linalg.lstsq(A, r, rcond=None)
        y_hat = A @ coef
        sig2 = np.sum((r - y_hat) ** 2) / max(len(x) - 3, 1)
        se = float(np.sqrt(sig2 * np.linalg.inv(A.T @ A)[2, 2]))
        return abs(coef[2]) > 3.0 * se
    amps = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0]
    thr = sweep_threshold(z2_gate,
                          lambda a: gen_noise_with_z2_term(200, amp=a),
                          amps, n_draws=100, seed=1)
    assert thr is not None and thr <= 0.5, thr


def _run_tests():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass\n")


# ============================================================================
# DEMO
# ============================================================================

def _demo():
    print("=" * 78)
    print("null_harness demo -- calibrating gates against known-answer controls")
    print("=" * 78)
    print()

    rows = []

    # trivial controls -- proves the harness catches the two failure modes
    rows.append({
        "name": "always_true_gate",
        **bake_off(_always_true, gen_white_noise(100),
                   gen_noise_with_z2_term(100, 0.5), n_draws=200),
        "min_amp": None,
    })
    rows.append({
        "name": "always_false_gate",
        **bake_off(_always_false, gen_white_noise(100),
                   gen_noise_with_z2_term(100, 0.5), n_draws=200),
        "min_amp": None,
    })

    # a working gate: z^2 detector via 3-sigma OLS
    def z2_gate(data):
        x, r = data["x"], data["residuals"]
        A = np.vstack([np.ones_like(x), x, x * x]).T
        coef, *_ = np.linalg.lstsq(A, r, rcond=None)
        y_hat = A @ coef
        sig2 = np.sum((r - y_hat) ** 2) / max(len(x) - 3, 1)
        se = float(np.sqrt(sig2 * np.linalg.inv(A.T @ A)[2, 2]))
        return abs(coef[2]) > 3.0 * se

    z2_row = bake_off(z2_gate, gen_white_noise(200),
                      gen_noise_with_z2_term(200, amp=0.5),
                      n_draws=500, seed=7)
    z2_row["min_amp"] = sweep_threshold(
        z2_gate,
        lambda a: gen_noise_with_z2_term(200, amp=a),
        amps=[0.01, 0.02, 0.03, 0.05, 0.07, 0.10, 0.20, 0.50],
        n_draws=200, seed=7)
    rows.append({"name": "z2_ols_3sigma", **z2_row})

    # Fisher rank test
    def smin_gate(data):
        S = np.linalg.svd(data["fisher"], compute_uv=False)
        return float(np.min(S)) < 0.05
    smin_row = bake_off(smin_gate, gen_wellposed_fisher(3),
                        gen_degenerate_fisher(3, eps=1e-4),
                        n_draws=500, seed=11)
    smin_row["min_amp"] = None    # 'eps' works backwards; sweep separately below
    rows.append({"name": "fisher_smin<0.05", **smin_row})

    # M2's Gate 1 -- the predicted failure
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..',
                                    'energy', 'modules'))
    try:
        from metrology_diagnostic import MetrologyDiagnostic

        def m2_gate1(data):
            md = MetrologyDiagnostic(
                x=data["x"], y_obs=data["y_obs"], y_pred_model=data["y_pred"],
                param_names=['a'], param_values=[1.0],
                covariance_matrix=np.eye(1))
            r = md.run()
            return r["gates"]["Gate1_Scale"] == "EQUIPMENT_NOISE"

        m2_row = bake_off(m2_gate1, gen_white_noise(200),
                          gen_scale_dependent_noise(200, ratio=10.0),
                          n_draws=200, seed=17)
        m2_row["min_amp"] = sweep_threshold(
            m2_gate1,
            lambda r: gen_scale_dependent_noise(200, ratio=r),
            amps=[1.5, 2.0, 3.0, 5.0, 10.0, 50.0, 100.0],
            n_draws=100, seed=17)
        rows.append({"name": "M2_Gate1_EQUIPMENT_NOISE", **m2_row})
    except ImportError:
        print("(skipping M2 Gate 1 demo -- energy/modules not importable)")

    report(rows)
    print()
    print("Reading:")
    print("  * always_true / always_false are the two trivial-fail shapes")
    print("    the harness must catch.")
    print("  * z2_ols_3sigma is a proper gate: low FP, high TP, min_amp")
    print("    names the smallest z^2 amplitude it detects at TP ≥ 0.5.")
    print("  * fisher_smin<0.05 discriminates identity from degenerate.")
    print("  * M2_Gate1_EQUIPMENT_NOISE: predicted (from static reading)")
    print("    to be CONSTANT_SILENT because for equal-size halves,")
    print("    res_coarse = mean(mean|first|, mean|second|) equals")
    print("    res_fine = mean|all| by construction, so ratio ≡ 1.")
    print("    The harness verifies the prediction empirically -- if it")
    print("    fires at 0.0 on both controls it is not a gate.")


if __name__ == "__main__":
    _run_tests()
    _demo()
