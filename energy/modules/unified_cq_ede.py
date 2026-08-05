#!/usr/bin/env python3
"""
unified_cq_ede.py — Unified CQ+EDE Integration Engine
======================================================

Merges the coupled-quintessence field (lambda, beta) with an early dark energy
scalar (f_ede, z_c) into ONE ODE system in N = ln(a). No multiplicative
composition — true nonlinear coexistence: both fields share the same Hubble
friction, the same closure budget, and the same growth equation.

Design notes (validated conventions, not the naive draft):
  * CQ sector replicates run_iteration6.py EXACTLY:
      x' = -3x + lam*sqrt(3/2) y^2 + x q - sqrt(3/2) beta Omega_m
      y' = -lam*sqrt(3/2) x y + y q
      z' = 2 z (q - 2)
      growth: d'' = -(2-q) d' + 1.5 Omega_m (1+2 beta^2) d
    with q = 1.5(1+x^2-y^2) + 0.5 z + (EDE contribution).
  * EDE sector replicates edelens.py phenomenology: a thawing quadratic
    scalar (m^2 = 3 H^2(z_c), field frozen until H ~ m) integrated as a
    physical Klein-Gordon component up to a_c, then switched to a
    w = 1/3 fluid (rho ~ a^-4) afterwards.
  * State is a hybrid: autonomous fractions (x, y, z) for CQ + radiation,
    physical (phi_e, pi_e) for the EDE scalar, L = ln(H/H0) carried as an
    extra ODE (L' = -q) so the EDE mass scale has an absolute reference.
  * Two shooting loops, weakly coupled -> fixed-point iteration:
      y_i   -> Omega_cq(0) + Omega_ede(0) = 0.685
      phi_ei -> Omega_ede(z_c) = f_ede

Observables: w0, wa (CQ field), sigma8 (growth ratio vs per-lambda LCDM
reference), H0 (sound-horizon ratio vs the engine's own LCDM reference,
r_s = ∫ c_s da / (a^2 H) to the drag epoch on a dense 3000-point grid).

License: CC0 1.0 Universal (public domain).
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from scipy.integrate import simpson

# --- cosmological constants (match both parent engines) ---
OM0 = 0.315
OR0 = 9.2e-5
OB0 = 0.049
OG0 = 5.44e-5   # photons only (baryon loading in c_s)
ODE0 = 0.685
S8_LCDM = 0.81
H0_LCDM = 67.4
N_I = -14.0
A_DRAG = 1.0 / 1060.0
R_EQ_MODE = 'it6'        # 'it6' (legacy, matches run_iteration6) | 'physical' (Omega_m0=0.315)
def _req():
    return (OR0 / (ODE0 if R_EQ_MODE == 'it6' else OM0)) * np.exp(-N_I)
SQ = np.sqrt(1.5)
A_FINE = np.logspace(np.log10(np.exp(N_I)), np.log10(1.0/1090.0), 3000)  # to z_*


# ---------------------------------------------------------------- RHS phases
def _rhs_kg(N, S, lam, beta, M2, b1=0.0, npl=0.0):
    """Phase 1 (N < N_c): CQ autonomous + EDE Klein-Gordon."""
    x, y, z, pe, pie, L, d, dd = S
    E2 = np.exp(2.0 * L)
    Ae = 0.5 * pie**2
    Be = 0.5 * M2 * pe**2 / E2
    Oe = (Ae + Be) / 3.0
    Om = 1.0 - z - x * x - y * y - Oe
    b = (beta + b1 * (1.0 - np.exp(N))) * np.exp(npl * N)   # a^n late trigger (n=0: const)
    # q = 1.5*Sum Omega_i (1+w_i); matter closure absorbs the EDE budget, so
    # the net EDE contribution is 1.5*Oe*w_e = 0.5*(Ae-Be)  [NOT Ae]
    q = 1.5 * (1.0 + x * x - y * y) + 0.5 * z + 0.5 * (Ae - Be)
    return [
        -3.0 * x + lam * SQ * y * y + x * q - SQ * b * Om,
        -lam * SQ * x * y + y * q,
        2.0 * z * (q - 2.0),
        pie,
        -(3.0 - q) * pie - M2 * pe / E2,
        -q,
        dd,
        -(2.0 - q) * dd + 1.5 * Om * (1.0 + 2.0 * b**2) * d,
    ]


def _rhs_fluid(N, S, lam, beta, b1=0.0, npl=0.0):
    """Phase 2 (N > N_c): CQ autonomous + EDE as w=1/3 fluid (R ~ a^-4)."""
    x, y, z, R, L, d, dd = S
    E2 = np.exp(2.0 * L)
    Oe = R / (3.0 * E2)
    Om = 1.0 - z - x * x - y * y - Oe
    b = (beta + b1 * (1.0 - np.exp(N))) * np.exp(npl * N)   # a^n late trigger (n=0: const)
    # net EDE contribution is 1.5*Oe*w_e = 0.5*Oe for w=1/3  [NOT 2*Oe]
    q = 1.5 * (1.0 + x * x - y * y) + 0.5 * z + 0.5 * Oe
    return [
        -3.0 * x + lam * SQ * y * y + x * q - SQ * b * Om,
        -lam * SQ * x * y + y * q,
        2.0 * z * (q - 2.0),
        -4.0 * R,
        -q,
        dd,
        -(2.0 - q) * dd + 1.5 * Om * (1.0 + 2.0 * b**2) * d,
    ]


# ------------------------------------------------------------------- driver
def _initial_state(y_i, pe_i):
    req = _req()
    z_i = req / (1.0 + req) * (1.0 - y_i**2)
    a_i = np.exp(N_I)
    rho_r = OR0 * a_i**-4                       # rho_crit0 units
    E_i = np.sqrt(rho_r / z_i)                  # E^2 = rho_tot/rho_crit0
    return [0.0, y_i, z_i, pe_i, 0.0, np.log(E_i), 1e-5, 0.0]


def _run_once(lam, beta, zc, M2, y_i, pe_i, rtol=1e-8, b1=0.0, npl=0.0):
    """Integrate both phases; return (sol1, sol2, N_c). sol2 None if zc<=0."""
    y0 = _initial_state(y_i, pe_i)
    if zc <= 0:                                  # no EDE phase switch
        sol = solve_ivp(_rhs_kg, (N_I, 0.0), y0, args=(lam, beta, M2, b1, npl),
                        dense_output=True, rtol=rtol, atol=1e-12)
        return sol, None, 0.0
    N_c = -np.log(1.0 + zc)
    s1 = solve_ivp(_rhs_kg, (N_I, N_c), y0, args=(lam, beta, M2, b1, npl),
                   dense_output=True, rtol=rtol, atol=1e-12)
    x, y, z, pe, pie, L, d, dd = s1.y[:, -1]
    E2 = np.exp(2.0 * L)
    R_c = 3.0 * E2 * (0.5 * pie**2 + 0.5 * M2 * pe**2 / E2) / 3.0
    s2 = solve_ivp(_rhs_fluid, (N_c, 0.0), [x, y, z, R_c, L, d, dd],
                   args=(lam, beta, b1, npl), dense_output=True, rtol=rtol, atol=1e-12)
    return s1, s2, N_c


def _ede_frac_at(sol, N, M2):
    x, y, z, pe, pie, L, d, dd = sol.sol(N)
    E2 = np.exp(2.0 * L)
    return float((0.5 * pie**2 + 0.5 * M2 * pe**2 / E2) / 3.0)


def _de0(s1, s2):
    if s2 is None:
        x, y = s1.y[0, -1], s1.y[1, -1]
        pe, pie, L = s1.y[3, -1], s1.y[4, -1], s1.y[5, -1]
        Oe = 0.0  # KG tail negligible today
    else:
        x, y = s2.y[0, -1], s2.y[1, -1]
        R, L = s2.y[3, -1], s2.y[4, -1]
        Oe = R / (3.0 * np.exp(2.0 * L))
    return x**2 + y**2 + Oe


def solve_unified(lam, beta, f_ede=0.0, z_c=0.0, outer=2, verbose=False, b1=0.0, npl=0.0):
    """
    Full nested-shooting solve. Returns dict of observables + solution handles.
    z_c <= 0 or f_ede <= 0 switches the EDE sector off (pure CQ).
    """
    ede_on = (f_ede > 0.0) and (z_c > 0.0)
    N_c = -np.log(1.0 + z_c) if ede_on else 0.0

    # ---- pass 0: EDE mass scale from the EDE-free background (edelens convention)
    M2 = 0.0
    y_i = _shoot_y(lam, beta, 0.0, 0.0, 0.0, b1=b1, npl=npl)
    if ede_on:
        s1, _, _ = _run_once(lam, beta, 0.0, 0.0, y_i, 0.0, b1=b1, npl=npl)
        E_zc = np.exp(s1.sol(N_c)[5])
        M2 = 3.0 * E_zc**2                        # m^2 = 3 H^2(z_c)  [edelens]

    # ---- fixed-point loop over the two shooting targets
    pe_i = 0.0
    for _ in range(outer if ede_on else 1):
        y_i = _shoot_y(lam, beta, z_c if ede_on else 0.0, M2, pe_i, b1=b1, npl=npl)
        if ede_on:
            pe_i = _shoot_pe(lam, beta, z_c, M2, y_i, f_ede, b1=b1, npl=npl)
    if verbose:
        print(f'    shot: y_i={y_i:.3e}, phi_ei={pe_i:.3e}, M2={M2:.3e}')

    s1, s2, N_c = _run_once(lam, beta, z_c if ede_on else 0.0, M2, y_i, pe_i,
                            rtol=1e-9, b1=b1, npl=npl)
    return _observables(lam, beta, s1, s2, N_c, M2, z_c, f_ede, b1)


def _shoot_y(lam, beta, z_c, M2, pe_i, target=ODE0, b1=0.0, npl=0.0):
    lo, hi = 1e-15, 0.9
    for _ in range(44):
        mid = np.sqrt(lo * hi)
        s1, s2, _ = _run_once(lam, beta, z_c, M2, mid, pe_i, b1=b1, npl=npl)
        if _de0(s1, s2) < target:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


def _shoot_pe(lam, beta, z_c, M2, y_i, f_target, b1=0.0, npl=0.0):
    N_c = -np.log(1.0 + z_c)
    lo, hi = 1e-8, 5.0
    for _ in range(40):
        mid = np.sqrt(lo * hi)
        s1, _, _ = _run_once(lam, beta, z_c, M2, y_i, mid, b1=b1, npl=npl)
        if _ede_frac_at(s1, N_c, M2) < f_target:
            lo = mid
        else:
            hi = mid
    return np.sqrt(lo * hi)


# --------------------------------------------------------------- observables
def _observables(lam, beta, s1, s2, N_c, M2, z_c, f_ede, b1=0.0):
    # --- w(z) of the CQ field on z = 0..3
    ZS = np.linspace(0, 3, 31)
    NS = np.log(1.0 / (1.0 + ZS))
    w = np.empty(31)
    for i, n in enumerate(NS):
        S = s2.sol(n) if (s2 is not None and n >= N_c) else s1.sol(n)
        x, y = S[0], S[1]
        w[i] = (x * x - y * y) / (x * x + y * y + 1e-30)
    w0 = w[0]
    a0, a1 = 1.0, 1.0 / (1.0 + ZS[1])
    wa = -(w[1] - w[0]) / (a1 - a0)

    # --- growth: sigma8 vs per-lambda LCDM reference (cached)
    d_today = s2.y[5, -1] if s2 is not None else s1.y[6, -1]
    d_ref = _growth_ref(lam)
    s8 = S8_LCDM * d_today / d_ref

    # --- sound horizon on the dense early grid -> H0
    rs = _sound_horizon(s1, s2, N_c, M2)
    rs_ref = _rs_ref()
    H0 = H0_LCDM * rs_ref / rs
    rs_mpc, chi_mpc, ths = cmb_observables(s1, s2, N_c)
    Nn = np.linspace(N_I, 0.0, 2000)
    xs = np.array([(s1.sol(n) if (s2 is None or n < N_c) else s2.sol(n))[0] for n in Nn])
    dphi = float(np.sqrt(6.0) * np.trapezoid(xs, Nn))

    out = {'lam': lam, 'beta': beta, 'b1': b1, 'f_ede': f_ede, 'z_c': z_c,
           'w0': float(w0), 'wa': float(wa),
           'sigma8': float(s8), 'H0': float(H0), 'rs_ratio': float(rs / rs_ref),
           'rs_mpc': float(rs_mpc), 'chi_mpc': float(chi_mpc), 'theta_s': float(ths),
           'cmb_sigma': float(abs(ths - THS_PLANCK) / THS_ERR),
           'Delta_phi': float(abs(dphi))}
    if s2 is not None:
        out['f_peak'] = _ede_frac_at(s1, N_c, M2)
        out['Omega_ede0'] = float(s2.y[3, -1] / (3.0 * np.exp(2.0 * s2.y[4, -1])))
    return out


_GREF, _RSREF = {}, {}


def _growth_ref(lam):
    if lam not in _GREF:
        y_i = _shoot_y(lam, 0.0, 0.0, 0.0, 0.0)
        s1, _, _ = _run_once(lam, 0.0, 0.0, 0.0, y_i, 0.0, rtol=1e-9)
        _GREF[lam] = s1.y[6, -1]
    return _GREF[lam]


def _rs_ref():
    if 'v' not in _RSREF:
        y_i = _shoot_y(1.1, 0.0, 0.0, 0.0, 0.0)
        s1, _, _ = _run_once(1.1, 0.0, 0.0, 0.0, y_i, 0.0, rtol=1e-9)
        _RSREF['v'] = _sound_horizon(s1, None, 0.0, 0.0)
    return _RSREF['v']


def _sound_horizon(s1, s2, N_c, M2):
    Ns = np.log(A_FINE)
    E = np.empty_like(Ns)
    for i, n in enumerate(Ns):
        S = s1.sol(n) if (s2 is None or n < N_c) else s2.sol(n)
        E[i] = np.exp(S[5] if s2 is None or n < N_c else S[4])
    Rb = (3.0 * OB0 / (4.0 * OG0)) * A_FINE
    cs = 1.0 / np.sqrt(3.0 * (1.0 + Rb))
    return float(simpson(cs / (A_FINE**2 * E), x=A_FINE))


# ------------------------------------------------------ CMB channel (theta_s)
C_KMS = 299792.458
A_LS = 1.0 / 1090.0
THS_PLANCK, THS_ERR = 1.04109, 0.00030      # 100 theta_*, Planck 2018

def _E_on_grid(s1, s2, N_c, Ns):
    out = np.empty_like(Ns)
    for i, n in enumerate(Ns):
        if s2 is None or n < N_c:
            out[i] = np.exp(s1.sol(n)[5])
        else:
            out[i] = np.exp(s2.sol(n)[4])
    return out

def cmb_observables(s1, s2, N_c):
    """Absolute r_s [Mpc], chi(z_ls) [Mpc], 100*theta_s.

    REQUIRES R_EQ_MODE='physical' -- the 'it6' default gives r_s ~ 115 Mpc
    (25% off) because it uses OR0/ODE0 for the radiation initial condition
    instead of OR0/OM0. See PROVENANCE.md DP-13 for the bisect.
    """
    if R_EQ_MODE != 'physical':
        import warnings
        warnings.warn(
            "cmb_observables called with R_EQ_MODE='{}'. Only "
            "R_EQ_MODE='physical' gives calibrated r_s / theta*; "
            "'it6' mode returns r_s ~ 115 Mpc (25% off). Any theta* "
            "verdict from this call is invalid. See PROVENANCE.md DP-13."
            .format(R_EQ_MODE), RuntimeWarning, stacklevel=2)
    rs_int = _sound_horizon(s1, s2, N_c, None)
    rs_mpc = (C_KMS / H0_LCDM) * rs_int
    a = np.logspace(np.log10(A_LS), 0.0, 4000)
    E = _E_on_grid(s1, s2, N_c, np.log(a))
    chi = (C_KMS / H0_LCDM) * simpson(1.0 / (a**2 * E), x=a)
    return rs_mpc, chi, 100.0 * rs_mpc / chi


# ------------------------------------------------------------------- anchors
def anchors():
    """Validation: (1) CQ-only vs run_iteration6, (2) EDE-only vs edelens."""
    print('ANCHOR 1: pure CQ (f_ede=0) vs run_iteration6 engine')
    import run_iteration6 as it6
    for lam, b0 in [(1.1, 0.0), (1.1, 0.2), (0.7, -0.1)]:
        u = solve_unified(lam, b0)
        s6 = it6.shoot(b0, 0.0, lam)
        zs, w6, f6 = it6.observables(s6)
        print(f'  lam={lam}, beta={b0:+.1f}:  w0 unified={u["w0"]:+.5f} '
              f'vs it6={w6[0]:+.5f}   d(w0)={u["w0"]-w6[0]:+.2e}')

    print('ANCHOR 2: pure EDE (beta=0) vs edelens engine')
    import edelens
    cache = {}
    for lz, fe in [(3.5, 0.05), (3.0, 0.10)]:
        zc = 10.0 ** lz
        u = solve_unified(1.1, 0.0, f_ede=fe, z_c=zc)
        e = edelens.observables(zc, fe, cache)
        print(f'  zc={zc:.0f}, f={fe}:  rs_ratio unified={u["rs_ratio"]:.4f} '
              f'vs edelens={e["rs"]:.4f} | s8 unified={u["sigma8"]:.4f} '
              f'vs edelens={S8_LCDM * e["s8"]:.4f}')


if __name__ == '__main__':
    anchors()
