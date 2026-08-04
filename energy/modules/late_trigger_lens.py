#!/usr/bin/env python3
"""
late_trigger_lens.py — Late-Time Trigger Lens
==============================================

Tests the class of dark-energy modifications that act ONLY at late times:
a free w_DE(a) = w0 + wa(1-a) + dw * sigmoid((a-a_t)/da)  (CPL + smooth kink).

No coupling, no early footprint: r_s is untouched by construction, so H0 is
pinned at 67.4 and the only CMB exposure is through chi (the distance to
last scattering). This is the "needle" identified by the success-geometry
analysis: the projection channel (w0, wa) can be placed anywhere — the
question is the price paid in sigma8 and theta*.

Background scheme (self-consistent): evolve lnH, lnΩm, lnΩr; Ω_DE by
closure. Since matter and radiation obey their conservation laws and the
total obeys Friedmann, the DE density automatically obeys
ρ_DE' = -3(1+w_DE)ρ_DE.

Conventions match unified_cq_ede.py: photon-only baryon loading in c_s,
r_s to z_* = 1090, correct kernel cs/(a^2 E), theta* = r_s/chi against
Planck 100θ* = 1.04109 ± 0.00030. Growth from the full w_tot (incl.
radiation), sigma8 normalized to the module's own w=-1 reference.

License: MIT
"""

import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.interpolate import interp1d

OM0, OR0, OB0, OG0 = 0.315, 9.2e-5, 0.049, 5.44e-5
S8_LCDM, H0_LCDM = 0.81, 67.4
N_I = -14.0
A_LS = 1.0 / 1090.0
C_OVER_H0 = 299792.458 / H0_LCDM
THS_PLANCK, THS_ERR = 1.04109, 0.00030
A_FINE = np.logspace(N_I / np.log(10), np.log10(A_LS), 3000)
A_CHI = np.logspace(np.log10(A_LS), 0.0, 3000)


def w_de(a, w0, wa, dw, a_t, da):
    return w0 + wa * (1.0 - a) + dw * (0.5 + 0.5 * np.tanh((a - a_t) / da))


def _integrate(w0, wa, dw, a_t, da, lnOde_i):
    """State: [lnE, lnΩr, lnΩde]; matter by closure (passive component)."""
    req = (OR0 / OM0) * np.exp(-N_I)
    z_i = req / (1.0 + req)
    a_i = np.exp(N_I)
    E_i = np.sqrt(OR0 * a_i**-4 / z_i)

    def rhs(N, y):
        lnE, lOr, lOde = y
        a = np.exp(N)
        Or, Ode = np.exp(lOr), np.exp(lOde)
        wde = w_de(a, w0, wa, dw, a_t, da)
        h = -1.5 * (1.0 + Or / 3.0 + wde * Ode)
        return [h, -4.0 - 2.0 * h, -3.0 * (1.0 + wde) - 2.0 * h]

    return solve_ivp(rhs, (N_I, 0.0), [np.log(E_i), np.log(z_i), lnOde_i],
                     dense_output=True, rtol=1e-9, atol=1e-13)


def run_background(w0, wa, dw=0.0, a_t=0.5, da=0.05):
    """Shoot lnΩde(N_i) so that Ωde(0) = 1-OM0-OR0."""
    target = 1.0 - OM0 - OR0
    lo, hi = -60.0, -0.1
    for _ in range(44):
        mid = 0.5 * (lo + hi)
        if np.exp(_integrate(w0, wa, dw, a_t, da, mid).sol(0.0)[2]) < target:
            lo = mid
        else:
            hi = mid
    return _integrate(w0, wa, dw, a_t, da, 0.5 * (lo + hi))


def _E(sol):
    return lambda N: np.exp(sol.sol(N)[0])


def growth_today(sol):
    def rhs(N, y):
        d, dd = y
        E = np.exp(sol.sol(N)[0])
        Om, Or = np.exp(sol.sol(N)[1]), np.exp(sol.sol(N)[2])
        a = np.exp(N)
        Ode = max(1.0 - Om - Or, 0.0)
        # h from lnE derivative: use reconstructed wtot
        return [dd, None]  # placeholder, replaced below
    # integrate h = d lnE/dN numerically
    Ns = np.linspace(N_I, 0.0, 4000)
    lnE = sol.sol(Ns)[0]
    h = np.gradient(lnE, Ns)
    Om = 1.0 - np.exp(sol.sol(Ns)[1]) - np.exp(sol.sol(Ns)[2])
    hI = interp1d(Ns, h, kind='cubic', fill_value='extrapolate')
    OmI = interp1d(Ns, Om, kind='cubic', fill_value='extrapolate')

    def gr(N, y):
        d, dd = y
        return [dd, -(2.0 + hI(N)) * dd + 1.5 * OmI(N) * d]

    g = solve_ivp(gr, (N_I, 0.0), [1e-5, 0.0], rtol=1e-9, atol=1e-12)
    return float(g.y[0, -1])


def sound_horizon(sol):
    E = np.exp(sol.sol(np.log(A_FINE))[0])
    Rb = (3.0 * OB0 / (4.0 * OG0)) * A_FINE
    cs = 1.0 / np.sqrt(3.0 * (1.0 + Rb))
    return C_OVER_H0 * float(simpson(cs / (A_FINE**2 * E), x=A_FINE))


def chi_ls(sol):
    E = np.exp(sol.sol(np.log(A_CHI))[0])
    return C_OVER_H0 * float(simpson(1.0 / (A_CHI**2 * E), x=A_CHI))


_REF = {}


def reference():
    if 'r' not in _REF:
        s = run_background(-1.0, 0.0)
        _REF['r'] = (growth_today(s), sound_horizon(s), chi_ls(s))
    return _REF['r']


def observables(w0, wa, dw=0.0, a_t=0.5, da=0.05):
    """Full gate vector for a late-trigger model."""
    sol = run_background(w0, wa, dw, a_t, da)
    g_ref, rs_ref, chi_ref = reference()
    g = growth_today(sol)
    rs = sound_horizon(sol)
    chi = chi_ls(sol)
    ths = 100.0 * rs / chi
    # effective CPL at z=0 (matching DESI extraction convention: local slope)
    ZS = np.linspace(0, 3, 31)
    wv = w_de(1.0 / (1.0 + ZS), w0, wa, dw, a_t, da)
    w0e = wv[0]
    a0, a1 = 1.0, 1.0 / (1.0 + ZS[1])
    wae = -(wv[1] - wv[0]) / (a1 - a0)
    return {'w0': float(w0e), 'wa': float(wae),
            'sigma8': float(S8_LCDM * g / g_ref),
            'H0': float(H0_LCDM * rs_ref / rs),
            'rs_ratio': float(rs / rs_ref),
            'theta_s': float(ths),
            'cmb_sigma': float(abs(ths - THS_PLANCK) / THS_ERR)}


def gate_vector(o, desi_mu=(-0.86, -0.53),
                desi_cov=((0.04**2, 0.4 * 0.04 * 0.16), (0.4 * 0.04 * 0.16, 0.16**2))):
    d = np.array([o['w0'] - desi_mu[0], o['wa'] - desi_mu[1]])
    desi = float(np.sqrt(d @ np.linalg.inv(np.array(desi_cov)) @ d))
    return np.array([desi, abs(o['sigma8'] - S8_LCDM) / 0.016,
                     max(0.0, 68.5 - o['H0']) / 0.5, o['cmb_sigma']])


def D_of(g):
    return float(np.sqrt(np.sum(np.log10(1.0 + np.maximum(g, 0))**2)))


if __name__ == '__main__':
    print('LambdaCDM self-test (w=-1):')
    o = observables(-1.0, 0.0)
    print(f"  s8={o['sigma8']:.4f}  H0={o['H0']:.2f}  100θ*={o['theta_s']:.5f} "
          f"(cmb {o['cmb_sigma']:.1f}σ)")
    print('DESI central point, no kink:')
    o = observables(-0.86, -0.53)
    print(f"  w0={o['w0']:+.3f} wa={o['wa']:+.3f}  s8={o['sigma8']:.4f} "
          f"H0={o['H0']:.2f}  100θ*={o['theta_s']:.5f} (cmb {o['cmb_sigma']:.1f}σ)")
