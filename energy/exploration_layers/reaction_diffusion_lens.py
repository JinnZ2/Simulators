#!/usr/bin/env python3
"""
reaction_diffusion_lens.py -- F3 lens.  numpy + scipy.

Read the sub-horizon linear-growth channel of the coupled-quintessence
system as a reaction-diffusion problem in e-folds:

    delta''  +   F(N) delta'   -   R(N) delta   =   0
              \_____________/     \___________/
              damping (Hubble       reaction (matter
              friction 2 - q)       gravity + fifth force,
                                    rate 1.5 * Omega_m * (1+2 beta^2))

For beta = const, R = const, F ~ const, and the growing mode is a
fixed exponent p in delta ~ a^p.  For beta(N) that never turns off --
the F3 parameterization beta(z) = beta0 + beta1 * z/(1+z) saturates
at beta0 + beta1 as z -> infinity -- R stays elevated over the whole
matter era, and the accumulated growth compounds:

    ln[ D(a=1) / D(a_i) ]   =   integral_{N_i}^0 p(N) dN

The R-D question: is the coupling autocatalytic (integrated Damkohler-
analog dominates damping so the reaction runs to completion), or does
it saturate (damping keeps p bounded and total growth stays near LCDM)?

The lens: given (beta0, beta1, lam), report the local growing-mode
exponent p(N) across matter era, the Damkohler-analog Da(N) = R/F^2,
and the total-growth ratio D(0)/D_LCDM(0).  Ratio > few => F3's
"8x LCDM" fs8 anomaly is not integrator instability but parametric
runaway of a coupling that never turns off.

names_no: [intent, verdict].  reads a signature, does not judge.
"""

import numpy as np
from scipy.integrate import solve_ivp


# --- background approximation (matter + LCDM-like) -----------------------

def _background(N, Om0=0.315, Or0=9.2e-5):
    """LCDM background at e-fold N. Returns (Omega_m, deceleration q, w_eff)."""
    a = np.exp(N)
    E2 = Om0 * a**-3 + Or0 * a**-4 + (1 - Om0)
    Om = Om0 * a**-3 / E2
    Or = Or0 * a**-4 / E2
    # q = -a a'' / a'^2 = (1/2) (1 + 3 sum w_i Om_i)
    q = 0.5 * (Om + 2 * Or - 2 * (1 - Om - Or))
    w_eff = (Or / 3 - (1 - Om - Or)) / max(Om + Or + (1 - Om - Or), 1e-30)
    return Om, q, w_eff


# --- the coupling that F3 flagged ---------------------------------------

def beta_of_z(z, b0=0.0, b1=0.4):
    """F3's running coupling. z/(1+z) -> 1 at high z: NEVER turns off."""
    return b0 + b1 * z / (1.0 + z)


def beta_of_N(N, b0=0.0, b1=0.4):
    z = np.exp(-N) - 1.0
    return beta_of_z(z, b0, b1)


# --- R-D signature ------------------------------------------------------

def local_growing_mode(Om, q, beta):
    """
    Growing-mode exponent p such that delta ~ a^p locally, from
    p^2 + (2-q) p - 1.5 Om (1+2 beta^2) = 0.  Returns the positive root.
    """
    b, c = (2.0 - q), 1.5 * Om * (1.0 + 2.0 * beta**2)
    disc = b * b + 4.0 * c
    return 0.5 * (-b + np.sqrt(max(disc, 0.0)))


def damkohler(Om, q, beta):
    """R / F^2  --  autocatalytic when >~ 1 (reaction dominates friction)."""
    R = 1.5 * Om * (1.0 + 2.0 * beta**2)
    F = 2.0 - q
    return R / (F * F + 1e-30)


def read(b0=0.0, b1=0.4, N_i=-14.0, N_f=0.0, n=200):
    """
    Signature of the F3 running coupling as a reaction-diffusion trajectory.

    Returns dict with:
      N              e-fold grid (radiation start -> today)
      beta           beta(N) along the trajectory
      p_local        growing-mode exponent at each N
      damkohler      R/F^2 at each N
      p_lcdm         growing-mode exponent for the SAME background but beta=0
      growth_ratio   D_coupled(0) / D_lcdm(0)  along the same background
                     (evaluated as exp[int (p - p_lcdm) dN])
    """
    N = np.linspace(N_i, N_f, n)
    p, plc, da, bs = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    for i, Ni in enumerate(N):
        Om, q, _ = _background(Ni)
        bs[i] = beta_of_N(Ni, b0, b1)
        p[i] = local_growing_mode(Om, q, bs[i])
        plc[i] = local_growing_mode(Om, q, 0.0)
        da[i] = damkohler(Om, q, bs[i])
    growth_ratio = float(np.exp(np.trapezoid(p - plc, N)))
    return {"N": N, "beta": bs, "p_local": p, "damkohler": da,
            "p_lcdm": plc, "growth_ratio": growth_ratio}


# --- self-test ----------------------------------------------------------

def _t_uncoupled_matches_lcdm():
    r = read(b0=0.0, b1=0.0)
    assert abs(r["growth_ratio"] - 1.0) < 1e-9, r["growth_ratio"]


def _t_running_coupling_amplifies():
    # F3's suspect parameterization
    r = read(b0=0.0, b1=0.4)
    assert r["growth_ratio"] > 2.0, (
        f"expected multi-fold amplification from a coupling that never "
        f"turns off; got {r['growth_ratio']:.3f}")


def _t_static_small_beta_is_modest():
    # honest sanity: a constant small coupling should give a small effect
    r = read(b0=0.05, b1=0.0)
    assert 1.01 < r["growth_ratio"] < 1.5, r["growth_ratio"]


def _t_damkohler_stays_reaction_dominated_in_matter_era():
    r = read(b0=0.0, b1=0.4)
    # matter era is roughly N in [-6, -1]; damping ~ 1.5, reaction >> 1
    mask = (r["N"] > -6) & (r["N"] < -1)
    assert np.min(r["damkohler"][mask]) > 0.3, r["damkohler"][mask].min()


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass\n")


def _demo():
    print("--- F3 R-D reading: beta(z) = beta0 + beta1*z/(1+z), 14 e-folds ---")
    print(f"{'label':<26}{'growth_ratio':>14}{'p(N=0)':>10}"
          f"{'p_lcdm(N=0)':>14}{'Da_max':>10}")
    for label, (b0, b1) in [
        ("LCDM control      (0,0)", (0.0, 0.0)),
        ("static small      (0.05,0)", (0.05, 0.0)),
        ("static moderate   (0.10,0)", (0.10, 0.0)),
        ("F3 iteration-6    (0,0.20)", (0.0, 0.20)),
        ("F3 iteration-6    (0,0.40)", (0.0, 0.40)),
        ("large runaway     (0,0.60)", (0.0, 0.60)),
    ]:
        r = read(b0, b1)
        print(f"{label:<26}{r['growth_ratio']:>14.3f}"
              f"{r['p_local'][-1]:>10.3f}{r['p_lcdm'][-1]:>14.3f}"
              f"{r['damkohler'].max():>10.3f}")
    print()
    print("Reading: growth_ratio >> 1 with small local beta means the")
    print("coupling accumulated over the matter era. Da_max is Ω_m·(1+2β²)/(2-q)²")
    print("-- the R-D signature of a reaction that never turns off.")


if __name__ == "__main__":
    _run(); _demo()
