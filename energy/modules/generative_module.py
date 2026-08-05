#!/usr/bin/env python3
"""
generative_module.py
The Generative Module: when Gate 4 says CREATE_NEW_MATHEMATICS,
propose the functional form of the missing term from the residual array.

Primary backend: PySR (symbolic regression) if installed.
Fallback backend: a greedy search over a physics-motivated basis library
(exp, inv, square, z, z*exp(-z), 1/(1+z^2), ...) with BIC selection.
The fallback needs only numpy and runs on a phone.
License: CC0 1.0 Universal (public domain).
"""

import numpy as np


# ----------------------------------------------------------------------
# Fallback: basis-library symbolic regression (pure numpy)
# ----------------------------------------------------------------------
def _basis_library(z):
    z = np.asarray(z, dtype=float)
    lib = {
        "z": z,
        "z^2": z**2,
        "exp(-z)": np.exp(-z),
        "exp(-2*z)": np.exp(-2 * z),
        "z*exp(-z)": z * np.exp(-z),
        "z^2*exp(-z)": z**2 * np.exp(-z),
        "inv(1+z)": 1.0 / (1.0 + z),
        "inv(1+z^2)": 1.0 / (1.0 + z**2),
        "z*inv(1+z)": z / (1.0 + z),
        "log(1+z)": np.log1p(z),
        "(1-a) [CPL-like]": z / (1.0 + z),
    }
    return lib


def propose_new_term_fallback(redshift_bins, residuals_w, max_terms=2):
    """Greedy forward selection over the basis library, BIC-gated.
    Returns a sympy-style expression string and metadata."""
    z = np.asarray(redshift_bins, dtype=float)
    r = np.asarray(residuals_w, dtype=float)
    n = len(z)
    lib = _basis_library(z)
    chosen, res_current, expr_parts = [], r.copy(), []

    for _ in range(max_terms):
        best_name, best_coef, best_rss = None, 0.0, np.inf
        for name, basis in lib.items():
            if name in chosen:
                continue
            coef = float(basis @ res_current) / float(basis @ basis + 1e-30)
            rss = float(np.sum((res_current - coef * basis)**2))
            if rss < best_rss:
                best_name, best_coef, best_rss = name, coef, rss
        rss_now = float(np.sum(res_current**2))
        # BIC gate: only add the term if it earns its keep
        bic0 = n * np.log(max(rss_now, 1e-30) / n) + len(chosen) * np.log(n)
        bic1 = n * np.log(max(best_rss, 1e-30) / n) + (len(chosen) + 1) * np.log(n)
        if bic1 > bic0 - 6:
            break
        chosen.append(best_name)
        expr_parts.append(f"{best_coef:.4g}*{best_name}")
        res_current = res_current - best_coef * lib[best_name]

    if not expr_parts:
        return {"expression": "0", "terms": [], "residual_std_after": float(np.std(r)),
                "note": "No basis term survives the BIC gate. Residuals look like noise."}
    return {"expression": " + ".join(expr_parts),
            "terms": chosen,
            "residual_std_before": float(np.std(r)),
            "residual_std_after": float(np.std(res_current)),
            "backend": "basis_library (numpy fallback)",
            "note": "Insert this as a new alpha-like coupling in the field equations."}


def propose_new_term(redshift_bins, residuals_w, pysr_kwargs=None):
    """Unified entry point. Uses PySR when available, else the basis library."""
    try:
        from pysr import PySRRegressor  # noqa
    except ImportError:
        return propose_new_term_fallback(redshift_bins, residuals_w)

    kw = dict(niterations=40,
              binary_operators=["+", "*", "/", "-"],
              unary_operators=["exp", "log", "inv", "square"],
              extra_sympy_mappings={"inv": lambda x: 1 / x},
              progress=False, verbosity=0, random_state=0)
    if pysr_kwargs:
        kw.update(pysr_kwargs)
    model = PySRRegressor(**kw)
    model.fit(np.asarray(redshift_bins).reshape(-1, 1), np.asarray(residuals_w))
    expr = str(model.sympy())
    return {"expression": expr, "backend": "PySR",
            "note": "Insert this as a new alpha-like coupling in the field equations."}


def interpret(expression, source="residuals of w(z) vs baseline"):
    """The LLM-orchestrator-style one-liner a physicist reads."""
    return (f"The missing term in {source} is:  {expression}  . "
            "Its redshift dependence localizes the new physics; insert it into "
            "the field equations as a new coupling and re-run the 4-gate diagnostic.")


if __name__ == "__main__":
    print("=== GENERATIVE MODULE DEMO ===")
    rng = np.random.default_rng(3)
    z = np.linspace(0, 2, 40)
    hidden = 0.12 * np.exp(-2.3 * z) / (1 + z**2)      # the "true" missing term
    residuals = hidden + rng.normal(0, 0.005, len(z))
    out = propose_new_term(z, residuals)
    print("proposed:", out["expression"])
    print("backend :", out.get("backend"))
    print("std before/after:", out.get("residual_std_before"), "/", out.get("residual_std_after"))
    print()
    print(interpret(out["expression"]))
