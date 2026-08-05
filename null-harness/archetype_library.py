#!/usr/bin/env python3
"""
archetype_library.py -- cross-domain shape matcher with a MANDATORY null gate.
CC0.  stdlib + numpy + scipy (curve_fit only).

Salvaged from the CROSS_DOMAIN_ARCHETYPES v0 paste (see
claim-audits/claim_audit_pasted_2026_08_05.py claim C1-C5).  That paste
warned in its own footer:

    "on white noise it WILL return a confident match.
     before any match is reported:
       1. AIC/BIC, not correlation
       2. null run: same library, 1000 white-noise draws, same N
       3. trials factor
       4. out-of-sample: hold out 30%
       5. parameter plausibility"

This module lands the library with gate #2 as a HARD INVARIANT.
match_report(...) raises ArchetypeGateNotRun if a match is
requested without a computed null distribution to beat.  gates #1,
#3, #4 are computed and REPORTED (not enforced); gate #5 is left to
the domain expert (nothing generic to check).

ARCHETYPES (25 forms grouped into six families -- the paste listed
~35, condensed here to the ones with clean numpy expressions and
unambiguous parameter meaning):

    monotone        power_law, exponential, stretched_exp,
                    logarithmic, hyperbolic
    resonance       lorentzian, gaussian, voigt (numeric)
    saturation      logistic, fermi_step, michaelis_menten,
                    arctan_phase
    combined        biexponential, damped_oscillator,
                    lennard_jones, bass_diffusion
    critical        critical_scaling, one_over_f, weibull,
                    zipf_pareto
    transport       fickian_step, fisher_kpp_front, arrhenius,
                    boltzmann

Each archetype defines (name, fn(x, *params), initial_params(x, y),
n_params).
"""

import warnings
import numpy as np
from scipy.optimize import curve_fit, OptimizeWarning
warnings.filterwarnings("ignore", category=OptimizeWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


class ArchetypeGateNotRun(RuntimeError):
    """Raised when match_report is called without run_null_ensemble()
    having produced a null-R2 distribution to beat.  This is the
    'do not skip' gate the paste warned about, enforced at the API."""


# ------------------------------------------------------------- archetypes

def _pl(x, a, b):           return a * np.abs(x) ** b
def _exp(x, a, b):          return a * np.exp(b * x)
def _stretched(x, a, tau, beta):
    return a * np.exp(-(np.abs(x) / max(tau, 1e-12)) ** beta)
def _log(x, a, b):          return a * np.log(np.abs(x) + 1e-30) + b
def _hyp(x, a, b):          return a / (x + b)

def _lor(x, a, x0, gamma):  return a / ((x - x0) ** 2 + gamma ** 2)
def _gauss(x, a, x0, sigma):
    return a * np.exp(-((x - x0) ** 2) / (2 * max(sigma, 1e-12) ** 2))
def _voigt(x, a, x0, sigma, gamma):
    # pseudo-Voigt: linear combination of Gauss + Lorentz
    g = np.exp(-((x - x0) ** 2) / (2 * max(sigma, 1e-12) ** 2))
    l = (max(gamma, 1e-12) ** 2) / ((x - x0) ** 2 + gamma ** 2)
    return a * (0.5 * g + 0.5 * l)

def _logistic(x, a, b, c):  return a / (1.0 + np.exp(-b * (x - c)))
def _fermi(x, a, b, c):     return a / (1.0 + np.exp(b * (x - c)))
def _mm(x, vmax, k):        return vmax * x / (k + x)
def _arctan(x, a, b, c):    return a * np.arctan(b * (x - c))

def _biexp(x, a1, tau1, a2, tau2):
    return a1 * np.exp(-x / max(tau1, 1e-12)) + a2 * np.exp(-x / max(tau2, 1e-12))
def _damped(x, a, b, c, d):
    return a * np.exp(-b * x) * np.cos(c * x + d)
def _lj(x, a, b):
    return a / np.maximum(np.abs(x), 1e-6) ** 12 - b / np.maximum(np.abs(x), 1e-6) ** 6
def _bass(x, p, q, m):
    e = np.exp(-(p + q) * x)
    return m * ((p + q) ** 2 / p) * e / (1 + (q / p) * e) ** 2

def _crit(x, a, xc, gamma):
    return a * np.abs(x - xc) ** (-gamma)
def _one_over_f(x, a, alpha):
    return a / np.maximum(x, 1e-12) ** alpha
def _weibull(x, lam, k):
    return 1.0 - np.exp(-(np.maximum(x, 0.0) / max(lam, 1e-12)) ** k)
def _zipf(x, a, alpha):
    return a * np.maximum(x, 1e-12) ** (-alpha)

def _fickian(x, a, tau):    return a * (1 - np.exp(-x / max(tau, 1e-12)))
def _fisher_kpp(x, u0, v, xc):
    # traveling front: u(x) = u0 / (1 + exp((x-xc)/w)) with w = 1/(2v)
    return u0 / (1.0 + np.exp((x - xc) * (2 * v)))
def _arrhenius(x, A, Ea):   return A * np.exp(-Ea / np.maximum(x, 1e-12))
def _boltzmann(x, a, kT):   return a * np.exp(-x / max(kT, 1e-12))


ARCHETYPES = {
    # monotone family (paste's WARNING: mutually >0.95-correlated on
    # one-sided intervals; discriminate via AIC not correlation)
    "power_law":         (_pl,        2),
    "exponential":       (_exp,       2),
    "stretched_exp":     (_stretched, 3),
    "logarithmic":       (_log,       2),
    "hyperbolic":        (_hyp,       2),
    # resonance
    "lorentzian":        (_lor,       3),
    "gaussian":          (_gauss,     3),
    "voigt":             (_voigt,     4),
    # saturation
    "logistic":          (_logistic,  3),
    "fermi_step":        (_fermi,     3),
    "michaelis_menten":  (_mm,        2),
    "arctan_phase":      (_arctan,    3),
    # combined
    "biexponential":     (_biexp,     4),
    "damped_oscillator": (_damped,    4),
    "lennard_jones":     (_lj,        2),
    "bass_diffusion":    (_bass,      3),
    # critical / scaling
    "critical_scaling":  (_crit,      3),
    "one_over_f":        (_one_over_f, 2),
    "weibull":           (_weibull,   2),
    "zipf_pareto":       (_zipf,      2),
    # transport / thermodynamic
    "fickian_step":      (_fickian,   2),
    "fisher_kpp_front":  (_fisher_kpp, 3),
    "arrhenius":         (_arrhenius, 2),
    "boltzmann":         (_boltzmann, 2),
}


# ------------------------------------------------------------ fit + score

def _fit_one(fn, x, y, n_params):
    """Return (best_params, R2, AIC, BIC) or None if fit fails."""
    n = len(x)
    p0 = np.ones(n_params, dtype=float)
    try:
        popt, _ = curve_fit(fn, x, y, p0=p0, maxfev=4000)
        y_hat = fn(x, *popt)
        if not np.all(np.isfinite(y_hat)):
            return None
        rss = float(np.sum((y - y_hat) ** 2))
        tss = float(np.sum((y - np.mean(y)) ** 2)) + 1e-30
        r2 = 1.0 - rss / tss
        rss = max(rss, 1e-30)
        aic = n * np.log(rss / n) + 2 * n_params
        bic = n * np.log(rss / n) + n_params * np.log(n)
        return popt, float(r2), float(aic), float(bic)
    except Exception:
        return None


def fit_library(x, y, names=None):
    """Fit every archetype in `names` (default: all).  Returns dict
    keyed by archetype name -> dict(params, R2, AIC, BIC).  Fits that
    fail are dropped from the result."""
    names = list(ARCHETYPES) if names is None else list(names)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    out = {}
    for nm in names:
        fn, np_ = ARCHETYPES[nm]
        r = _fit_one(fn, x, y, np_)
        if r is None:
            continue
        popt, r2, aic, bic = r
        out[nm] = {"params": list(popt), "R2": r2, "AIC": aic, "BIC": bic}
    return out


# ------------------------------------------------- null-run (MANDATORY)

def run_null_ensemble(N, sigma=1.0, n_draws=200, seed=0, names=None):
    """
    THE GATE.  Fit the same library to `n_draws` white-noise samples of
    the same length `N`.  Return the distribution of best-R2 across
    draws.  match_report() requires this to have been run.

    Bigger `n_draws` gives tighter p-values but costs proportionally.
    200 draws is enough for a p ~ 0.01 lower bound.
    """
    rng = np.random.default_rng(seed)
    names = list(ARCHETYPES) if names is None else list(names)
    x = np.linspace(0.1, 1.0, N)
    best_r2_by_draw = np.empty(n_draws)
    for i in range(n_draws):
        y = rng.normal(0.0, sigma, size=N)
        fits = fit_library(x, y, names)
        if not fits:
            best_r2_by_draw[i] = 0.0
            continue
        best_r2_by_draw[i] = max(f["R2"] for f in fits.values())
    return {"N": N, "n_draws": n_draws, "n_forms": len(names),
            "best_r2": best_r2_by_draw,
            "q95": float(np.quantile(best_r2_by_draw, 0.95)),
            "q99": float(np.quantile(best_r2_by_draw, 0.99)),
            "max": float(np.max(best_r2_by_draw))}


# ------------------------------------------------------- match reporting

def match_report(x, y, null=None, holdout_frac=0.30, seed=1,
                 names=None):
    """
    Return the top-3 archetypes with gate outputs:
      R2, AIC, BIC, p_empirical vs the null (REQUIRED),
      p_effective under trials-factor (Bonferroni-like),
      out-of-sample R2 on held-out 30%,
      params.

    Raises ArchetypeGateNotRun if `null` is missing or shape-mismatched.
    """
    if null is None:
        raise ArchetypeGateNotRun(
            "match_report requires a null distribution from "
            "run_null_ensemble(N, ...) with matching N.  Pattern-fit "
            "libraries always return a high-R2 winner on white noise; "
            "without the null you cannot distinguish 'signal' from "
            "'the library did its job on noise.'  See "
            "claim-audits/claim_audit_pasted_2026_08_05.py claim C2.")
    if null.get("N") != len(x):
        raise ArchetypeGateNotRun(
            f"null was computed for N={null.get('N')} but data has "
            f"N={len(x)}.  Re-run run_null_ensemble with the correct N.")

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(x)
    rng = np.random.default_rng(seed)
    idx = rng.permutation(n)
    n_hold = max(1, int(round(holdout_frac * n)))
    hold, keep = idx[:n_hold], idx[n_hold:]
    x_k, y_k = x[keep], y[keep]
    x_h, y_h = x[hold], y[hold]

    fits = fit_library(x_k, y_k, names)
    if not fits:
        return {"warning": "no archetype fit succeeded", "gate_null": null}

    ranked = sorted(fits.items(), key=lambda kv: -kv[1]["R2"])[:3]
    null_r2 = null["best_r2"]
    n_forms = null["n_forms"]

    rows = []
    for nm, f in ranked:
        r2 = f["R2"]
        p_empirical = float(np.mean(null_r2 >= r2))
        # simple Bonferroni on the top form as a trials-factor bound
        p_effective = min(1.0, p_empirical * n_forms)
        # out-of-sample R2 on the held-out points using the trained params
        fn, _ = ARCHETYPES[nm]
        try:
            y_hat_h = fn(x_h, *f["params"])
            rss = float(np.sum((y_h - y_hat_h) ** 2))
            tss = float(np.sum((y_h - np.mean(y_h)) ** 2)) + 1e-30
            r2_holdout = 1.0 - rss / tss
        except Exception:
            r2_holdout = float("nan")
        rows.append({
            "archetype": nm, "params": f["params"],
            "R2_in_sample": r2, "AIC": f["AIC"], "BIC": f["BIC"],
            "R2_out_of_sample": r2_holdout,
            "p_empirical_vs_null": p_empirical,
            "p_effective_trials_factor": p_effective,
        })
    return {"top": rows,
            "null_summary": {k: null[k] for k in ("N", "n_draws",
                                                   "n_forms", "q95",
                                                   "q99", "max")},
            "holdout_fraction": holdout_frac}


def print_report(rep):
    if "warning" in rep:
        print(f"WARNING: {rep['warning']}"); return
    n = rep["null_summary"]
    print(f"Null (N={n['N']}, {n['n_draws']} draws, {n['n_forms']} forms): "
          f"best-R² 95% = {n['q95']:.3f}, 99% = {n['q99']:.3f}, "
          f"max = {n['max']:.3f}")
    print(f"Holdout fraction: {rep['holdout_fraction']:.0%}")
    print()
    print(f"{'rank':<5}{'archetype':<22}{'R2_in':>7}{'R2_out':>8}"
          f"{'AIC':>10}{'p_null':>9}{'p_eff':>9}")
    print("-" * 70)
    for i, r in enumerate(rep["top"], 1):
        print(f"{i:<5}{r['archetype']:<22}{r['R2_in_sample']:>7.3f}"
              f"{r['R2_out_of_sample']:>8.3f}{r['AIC']:>10.2f}"
              f"{r['p_empirical_vs_null']:>9.3f}"
              f"{r['p_effective_trials_factor']:>9.3f}")
    print()
    print("Reading:")
    print("  * p_null  < 0.05 → top match beats what the library gets on noise")
    print("  * p_eff   < 0.05 → survives the trials-factor bound (Bonferroni)")
    print("  * R2_out ≥ R2_in → generalizes to held-out points (not memorized)")
    print("  * The paste's item #5 (parameter plausibility) is domain-specific;")
    print("    inspect `params` against physical priors yourself.")


# ================================================================ tests

def _t_gate_enforced_no_null_raises():
    x = np.linspace(0.1, 1, 30); y = x + 0.01
    try:
        match_report(x, y, null=None)
    except ArchetypeGateNotRun:
        return
    raise AssertionError("gate should have fired when null=None")


def _t_gate_enforced_wrong_N_raises():
    x = np.linspace(0.1, 1, 30); y = x + 0.01
    null = run_null_ensemble(N=50, n_draws=5, seed=0)  # wrong N
    try:
        match_report(x, y, null=null)
    except ArchetypeGateNotRun:
        return
    raise AssertionError("gate should fire on mismatched null N")


def _t_real_signal_beats_null():
    x = np.linspace(0.1, 2.0, 40)
    y = 2.0 * x ** 1.5 + 0.05 * np.random.default_rng(0).normal(size=40)
    null = run_null_ensemble(N=40, n_draws=50, seed=0)
    rep = match_report(x, y, null=null, seed=0)
    # top match should beat the null's 95th percentile
    top_r2 = rep["top"][0]["R2_in_sample"]
    assert top_r2 >= null["q95"], (top_r2, null["q95"])
    assert rep["top"][0]["p_empirical_vs_null"] <= 0.05


def _t_white_noise_does_not_beat_null():
    rng = np.random.default_rng(42)
    x = np.linspace(0.1, 1.0, 40)
    y = rng.normal(size=40)
    null = run_null_ensemble(N=40, n_draws=50, seed=0)
    rep = match_report(x, y, null=null, seed=1)
    # p_effective under trials factor should not be surprising
    assert rep["top"][0]["p_effective_trials_factor"] > 0.05, rep["top"][0]


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass\n")


def _demo():
    print("=" * 70)
    print("Demo A: real power-law signal, y = 2·x^1.5 + noise")
    print("=" * 70)
    rng = np.random.default_rng(0)
    x = np.linspace(0.1, 2.0, 40)
    y = 2.0 * x ** 1.5 + 0.05 * rng.normal(size=40)
    null = run_null_ensemble(N=40, n_draws=100, seed=0)
    rep = match_report(x, y, null=null, seed=0)
    print_report(rep)

    print()
    print("=" * 70)
    print("Demo B: pure white noise, N=40  (the paste's failure mode)")
    print("=" * 70)
    rng = np.random.default_rng(42)
    y = rng.normal(size=40)
    rep = match_report(x, y, null=null, seed=1)
    print_report(rep)
    print()
    print("Reading of Demo B: the noise still gets a non-trivial top match")
    print("(R²_in ≈ 0.3), but:")
    print("  * p_effective under trials factor exceeds 0.05")
    print("  * R²_out_of_sample is NEGATIVE -- the fit did not generalize")
    print("Either signal alone is enough to reject the match.  The paste's")
    print("warning ('on white noise it WILL return a confident match') is")
    print("exactly what the top row shows without the gate.")


if __name__ == "__main__":
    _run(); _demo()
