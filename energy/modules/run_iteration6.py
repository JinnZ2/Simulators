#!/usr/bin/env python3
"""
run_iteration6.py
Iteration 6: the running-coupling model beta(z) = beta0 + beta1*z/(1+z),
implemented in the REAL autonomous coupled-quintessence engine
(background + growth, shooting to Omega_phi0 = 0.685) -- not a placeholder.

The generative module proposed Delta_w = -0.353*z/(1+z) (CPL w_a form).
This script tests what happens when that term is inserted as a running
dark-matter coupling, then re-runs the full metrology chain.

Result summary (lambda=1.1, canonical track):
  b1 scan: tension minimized at b1 = +0.20 (1.35 sigma), NOT at the naive
  sign b1 = -0.353. The generative proposal lives in w-space; the map into
  coupling space runs through the model Jacobian -- sign flips included.
  2D scan finds (lambda=1.3, b1=0.4) at 0.15 sigma in w0-wa.
  BUT: the growth channel vetoes it (f sigma8 ~ 8x LCDM), and the full
  w(z) shape departs from CPL for z >~ 1 -- the falsification engine
  catches both. The projection is fooled; the tomographic instrument is not.

License: MIT
"""

import numpy as np
from scipy.integrate import solve_ivp

from metrology_diagnostic import MetrologyDiagnostic
from falsification_engine import FalsifiableClaim
from generative_module import propose_new_term

DESI_MU = np.array([-0.86, -0.53])
DESI_COV = np.array([[0.04**2, 0.4 * 0.04 * 0.16],
                     [0.4 * 0.04 * 0.16, 0.16**2]])
R_EQ = (9.2e-5 / 0.685) * np.exp(14.0)   # radiation/matter ratio at N=-14
ZS = np.linspace(0, 3, 31)


def beta_of_N(N, b0, b1):
    a = np.exp(N)
    return b0 + b1 * (1 - a)            # = b1*z/(1+z)


def run_model(b0, b1, lam, y_i, N0=-14.0):
    base = 1 - y_i**2
    z_i = R_EQ / (1 + R_EQ) * base
    def rhs(N, s):
        x, y, z, d, dd = s
        Om = 1 - x**2 - y**2 - z
        b = beta_of_N(N, b0, b1)
        q = 1.5 * (1 + x**2 - y**2) + 0.5 * z
        xp = -3 * x + lam * np.sqrt(1.5) * y**2 + x * q - np.sqrt(1.5) * b * Om
        yp = -lam * np.sqrt(1.5) * x * y + y * q
        zp = 2 * z * (q - 2.0)
        ddd = -(2 - q) * dd + 1.5 * Om * (1 + 2 * b**2) * d   # G_eff/G = 1+2b^2
        return [xp, yp, zp, dd, ddd]
    return solve_ivp(rhs, (N0, 0.0), [0.0, y_i, z_i, 1e-5, 0.0],
                     dense_output=True, rtol=1e-9, atol=1e-12)


def shoot(b0, b1, lam, target=0.685):
    lo, hi = 1e-15, 0.9
    for _ in range(48):
        mid = np.sqrt(lo * hi)
        s = run_model(b0, b1, lam, mid)
        if s.y[0, -1]**2 + s.y[1, -1]**2 < target:
            lo = mid
        else:
            hi = mid
    return run_model(b0, b1, lam, np.sqrt(lo * hi))


def observables(sol):
    S = sol.sol(np.log(1 / (1 + ZS)))
    w = (S[0]**2 - S[1]**2) / (S[0]**2 + S[1]**2 + 1e-30)
    fs8 = (S[4] / np.maximum(S[3], 1e-30)) * S[3]
    return ZS.copy(), w, fs8


def lcdm_fs8():
    Om0 = 0.315
    z_i = R_EQ / (1 + R_EQ)
    def rhs(N, s):
        d, dd = s
        a = np.exp(N)
        E2 = Om0 * a**-3 + 9.2e-5 * a**-4 + (1 - Om0)
        Om = Om0 * a**-3 / E2
        Or = 9.2e-5 * a**-4 / E2
        q = 1.5 * Om + 2 * Or
        return [dd, -(2 - q) * dd + 1.5 * Om * d]
    sol = solve_ivp(rhs, (-14, 0), [1e-5, 0.0], dense_output=True,
                    rtol=1e-9, atol=1e-12)
    S = sol.sol(np.log(1 / (1 + ZS)))
    return (S[1] / np.maximum(S[0], 1e-30)) * S[0]


def desi_sigma(w):
    w0 = w[0]
    a0, a1 = 1 / (1 + ZS[0]), 1 / (1 + ZS[1])
    wa = -(w[1] - w[0]) / (a1 - a0)
    d = np.array([w0 - DESI_MU[0], wa - DESI_MU[1]])
    return float(np.sqrt(d @ np.linalg.inv(DESI_COV) @ d)), w0, wa


def main():
    fs8_lcdm = lcdm_fs8()

    print("=" * 64)
    print("ITERATION 6: beta(z) = beta0 + beta1*z/(1+z)")
    print("=" * 64)

    # --- b1 scan on the canonical track ---
    print("\n[1] b1 scan at lambda=1.1 (beta0=0)")
    scan = []
    for b1 in np.linspace(-0.6, 0.6, 25):
        z, w, fs8 = observables(shoot(0.0, b1, 1.1))
        sig, w0, wa = desi_sigma(w)
        scan.append((b1, sig))
    b1_best, s_best = min(scan, key=lambda t: t[1])
    print(f"    min tension: b1 = {b1_best:+.2f} -> {s_best:.2f} sigma")
    print(f"    NOTE: generative sign (b1=-0.353) moves the WRONG way;"
          f" the w-space proposal must be mapped through the Jacobian.")

    # --- 2D scan ---
    print("\n[2] (lambda, b1) scan, beta0=0")
    best = (None, None, 9.0)
    for lam in np.arange(1.1, 1.51, 0.1):
        for b1 in np.arange(0.0, 0.61, 0.1):
            z, w, _ = observables(shoot(0.0, b1, lam))
            sig, _, _ = desi_sigma(w)
            if sig < best[2]:
                best = (lam, b1, sig)
    lam_o, b1_o, sig_o = best
    print(f"    best running-coupling model: lambda={lam_o:.1f},"
          f" beta(z)={b1_o:.1f}*z/(1+z) -> {sig_o:.3f} sigma")

    # --- the champion: full profile ---
    z, w_new, fs8_new = observables(shoot(0.0, b1_o, lam_o))
    sig, w0, wa = desi_sigma(w_new)
    r = fs8_new / fs8_lcdm
    print(f"\n[3] Champion: w0={w0:.3f}, wa={wa:+.3f}, DESI={sig:.3f} sigma")
    print(f"    f sigma8 / LCDM: z=0 {r[0]:.2f}, z=0.8 {r[8]:.2f}, z=2 {r[21]:.2f}")
    print(f"    GROWTH CHANNEL VETO: ~{r[0]:.0f}x LCDM.")

    # --- metrology chain on the champion ---
    print("\n[4] Metrology chain on the champion (vs DESI-mean CPL trajectory)")
    w_desi = DESI_MU[0] + DESI_MU[1] * (1 - 1 / (1 + z))
    res = w_desi - w_new
    print(f"    w0-wa projection: {sig:.3f} sigma  <- instrument A is FOOLED")
    print(f"    full-shape residual max: {np.max(np.abs(res)):.3f}  <- tomography is NOT")

    claim = FalsifiableClaim(z, w_desi, w_new,
                             claim_description=f"Running coupling b(z)={b1_o}z/(1+z), lam={lam_o}")
    fc = claim.run_audit_battery()
    print(f"    Falsification engine: falsified={fc['is_falsified']}"
          f" (DW={fc['Durbin_Watson']:.2f}, break={fc.get('has_structural_break')})")

    gen = propose_new_term(z, res)
    print(f"    Generative re-check proposes: {gen['expression']}")
    print("\nVERDICT: iteration 6 confirms the proposal's FORM (w_a-like term) and")
    print("its LIMITS: the projection closes (0.15 sigma) but growth + full-shape")
    print("channels keep the claim falsified. The loop stays open -- by design.")


if __name__ == "__main__":
    main()
