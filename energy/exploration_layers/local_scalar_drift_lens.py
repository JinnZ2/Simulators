#!/usr/bin/env python3
"""
local_scalar_drift_lens.py -- F-10 D corrected + anchored.
numpy + matplotlib.

Project the late-time kink (a_t, delta_w, Delta_a) down to a
laboratory-testable observable: the secular drift rate of a
fundamental constant X that couples to the scalar via
    d ln X / dt = beta_X * phi_dot / M_P                (natural units)
where beta_X is a Damour-Polyakov-class coupling (dimensionless,
scalar-mediated).  With phi_dot today = sqrt((1+w0) * Omega_phi * rho_c),
the champion kink's drift landscape becomes a present-day, lab-scale
falsification channel that does not need ET-era instruments.

Corrects the F-10 D paste (see claim-audits/claim_audit_pasted_2026_08_05.py):
    D2  paste had yr_to_GeVinv = 1.956e8    (off by 2.45e23 orders)
    D3  paste had rho_crit /(8pi)           (extraneous /(8pi) for the
                                             REDUCED Planck mass)
    combined: drift prefactor was 1.23e24 too small.  Paste's plot said
    beta > 4e17 needed for alpha detection; correct value is beta > 3e-7.

ANCHOR TESTS at import (raise if any physical constant drifts):
    A_D1  H0 [GeV]                = 1.438e-42     (67.4 km/s/Mpc via hbar)
    A_D2  yr_to_GeVinv            = 4.795e+31 GeV^-1
    A_D3  rho_crit today          = 3.678e-47 GeV^4  (textbook match)
    A_D4  drift prefactor at 1+w=1 = 6.90e-11 /yr per beta=1

names_no: [intent, verdict].  Reports numbers and shape; the
lens does not decide whether a given beta_X is "allowed" -- it
plots the constraint and lets the operator read the limit.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# =========================================================================
# PHYSICAL CONSTANTS  (all natural units, hbar = c = 1)
# =========================================================================

HBAR_GeV_s   = 6.582119569e-25     # ℏ [GeV*s]
YR_SECONDS   = 3.15576e7            # Julian year [s]
KM_PER_MPC   = 3.086e19             # [km/Mpc]
M_P_GeV      = 2.435e18             # reduced Planck mass [GeV]

# derived
YR_GeVINV    = YR_SECONDS / HBAR_GeV_s        # 1 yr in GeV^-1  (~ 4.795e31)
KM_PER_S_PER_MPC_TO_GeV = HBAR_GeV_s / KM_PER_MPC   # 1 (km/s/Mpc) = 2.133e-44 GeV

# cosmology (matches energy/modules; see PROVENANCE §7.1 "Named denominators")
H0_KM_S_MPC  = 67.4
OMEGA_PHI0   = 0.685

# derived
H0_GeV       = H0_KM_S_MPC * KM_PER_S_PER_MPC_TO_GeV     # H0 in GeV
RHO_C_GeV4   = 3.0 * H0_GeV**2 * M_P_GeV**2               # reduced-Planck ρ_c
# NB: for the REDUCED Planck mass M_P, ρ_c = 3H^2 M_P^2 (no /(8π)).
#     For the FULL Planck mass M_Pl = sqrt(8π)*M_P, ρ_c = 3H^2 M_Pl^2/(8π).
#     Same number, different bookkeeping.  Paste used reduced M_P AND /(8π);
#     that's the F-10-D3 bug.


# ---- current lab limits (per year, ~1sigma) -----------------------------

LIMIT_ALPHA_DOT = 1.0e-17     # atomic clocks (Al+/Yb+ optical clock ratios)
LIMIT_G_DOT     = 2.0e-13     # lunar laser ranging (Muller & Biskupek)


# =========================================================================
# ANCHOR TESTS (fail loudly at import if any of these drift)
# =========================================================================

def _anchor(name, actual, expected, rtol=1e-3):
    rel = abs(actual - expected) / abs(expected)
    if rel > rtol:
        raise RuntimeError(
            f"ANCHOR {name} FAILED: got {actual:.6e}, expected "
            f"{expected:.6e} (rel err {rel:.2e} > {rtol})")

_anchor("A_D1  H0 in GeV",       H0_GeV,     1.438e-42)
_anchor("A_D2  yr_to_GeVinv",    YR_GeVINV,  4.795e31, rtol=1e-2)
_anchor("A_D3  rho_c today",     RHO_C_GeV4, 3.678e-47, rtol=1e-2)


# =========================================================================
# KINK (matches late_trigger_lens.w_de in energy/modules)
# =========================================================================

def w_kink(z, a_t=0.92, delta_w=0.10, Delta_a=0.05, w_base=-1.0):
    """
    w(z) = w_base + delta_w * sigmoid((a - a_t) / Delta_a),  a = 1/(1+z).
    Champion (PROVENANCE DP-11): a_t=0.92, delta_w=0.10, Delta_a=0.05.
    """
    a = 1.0 / (1.0 + z)
    return w_base + delta_w / (1.0 + np.exp(-(a - a_t) / Delta_a))


# =========================================================================
# DRIFT PREFACTOR
# =========================================================================

def drift_prefactor(w0, omega_phi=OMEGA_PHI0):
    """
    d ln X / dt (per year) = beta_X * drift_prefactor(w0)
    for any dimensionless coupling beta_X.  Requires 1+w0 > 0
    (canonical scalar rolling with kinetic energy).

    Physics:
      rho_K   = 0.5 * (1+w0) * Omega_phi * rho_c        [GeV^4]
      phi_dot = sqrt(2 rho_K)                            [GeV^2]
      d ln X/dt = beta_X * phi_dot / M_P                 [GeV = 1/time]
      per year = above * YR_GeVINV                       [dimensionless/yr]
    """
    one_plus_w = 1.0 + w0
    if one_plus_w <= 0:
        raise ValueError(f"1+w0 = {one_plus_w:.3f} <= 0: no kinetic energy "
                         "(pure Lambda or phantom); scalar-drift lens N/A.")
    rho_K   = 0.5 * one_plus_w * omega_phi * RHO_C_GeV4
    phi_dot = np.sqrt(2.0 * rho_K)
    return (phi_dot / M_P_GeV) * YR_GeVINV       # /yr per unit beta


# A_D4 anchor: at (1+w) = 1, prefactor should be H0 in per-year (approx)
_prefactor_at_1 = drift_prefactor(w0=0.0, omega_phi=1.0)  # 1+w=1, full-DE
# H0 in /yr = H0_KM_S_MPC / (KM_PER_MPC * seconds-per-year-inverse) * YR_SECONDS
_H0_per_yr = (H0_KM_S_MPC / KM_PER_MPC) * YR_SECONDS       # ~ 6.89e-11
# prefactor = sqrt(2 * 0.5 * 1 * rho_c) / M_P * yr_GeVinv
#           = sqrt(rho_c) / M_P * yr_GeVinv
#           = sqrt(3) * H0 * yr_GeVinv          (from rho_c = 3 H^2 M_P^2)
_anchor("A_D4  prefactor at 1+w=1", _prefactor_at_1,
        np.sqrt(3.0) * _H0_per_yr, rtol=1e-2)


# =========================================================================
# LENS: constraint landscape
# =========================================================================

def sensitivity_threshold(w0, limit_per_yr, omega_phi=OMEGA_PHI0):
    """Smallest |beta| that a limit-per-year would detect for this w0."""
    return limit_per_yr / drift_prefactor(w0, omega_phi)


def read(a_t=0.92, delta_w=0.10, Delta_a=0.05, w_base=-1.0,
         omega_phi=OMEGA_PHI0):
    """
    Full lens signature for one kink configuration.
    """
    w0 = float(w_kink(0.0, a_t, delta_w, Delta_a, w_base))
    pref = drift_prefactor(w0, omega_phi)
    return {
        "kink": {"a_t": a_t, "delta_w": delta_w, "Delta_a": Delta_a,
                 "w_base": w_base},
        "w0": w0,
        "one_plus_w0": 1.0 + w0,
        "phi_dot_over_M": pref / YR_GeVINV,       # dimensionless (GeV/GeV)
        "drift_prefactor_per_yr": pref,
        "beta_alpha_sensitivity": sensitivity_threshold(w0, LIMIT_ALPHA_DOT,
                                                        omega_phi),
        "beta_G_sensitivity":     sensitivity_threshold(w0, LIMIT_G_DOT,
                                                        omega_phi),
    }


# =========================================================================
# PLOT
# =========================================================================

def plot(configs, out_path):
    """
    configs : list of dicts {"label": str, "kink": (a_t, dw, Da)}
    Draws drift vs beta for each config, plus current exclusion bands.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    betas = np.logspace(-9, 1, 400)

    for cfg in configs:
        a_t, dw, Da = cfg["kink"]
        w0 = float(w_kink(0.0, a_t, dw, Da))
        pref = drift_prefactor(w0)
        drift = betas * pref
        ax.loglog(betas, drift, lw=2,
                  label=f'{cfg["label"]}  (w0={w0:+.3f}, 1+w={1+w0:.3f})')

    # laboratory limits
    ax.axhline(LIMIT_ALPHA_DOT, ls='--', c='#1f77b4', alpha=0.7,
               label=fr'$|\dot\alpha/\alpha|$ limit = {LIMIT_ALPHA_DOT:.0e} /yr'
                     ' (atomic clocks)')
    ax.axhline(LIMIT_G_DOT, ls='--', c='#d62728', alpha=0.7,
               label=fr'$|\dot G/G|$ limit = {LIMIT_G_DOT:.0e} /yr (LLR)')

    ax.set_xlabel(r'coupling  $\beta_X$  (dimensionless)', fontsize=12)
    ax.set_ylabel(r'drift rate  $|d\ln X/dt|$  [/yr]', fontsize=12)
    ax.set_title(
        'Local scalar drift from late-time kink (F-10 D corrected)\n'
        r'$\dot X/X = \beta_X \cdot \dot\phi/M_P$ with '
        r'$\dot\phi = \sqrt{(1{+}w_0)\,\Omega_\phi\,\rho_c}$',
        fontsize=12)
    ax.legend(loc='lower right', fontsize=9)
    ax.grid(True, which='both', ls=':', alpha=0.4)
    ax.set_xlim(1e-9, 1e1)
    ax.set_ylim(1e-25, 1e-5)
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches='tight')
    plt.close(fig)


# =========================================================================
# SELF-TEST
# =========================================================================

def _t_prefactor_scales_with_sqrt_one_plus_w():
    # doubling (1+w) should multiply prefactor by sqrt(2)
    r_small = drift_prefactor(w0=-0.99)
    r_big   = drift_prefactor(w0=-0.98)   # 1+w doubled from 0.01 to 0.02
    assert abs(r_big / r_small - np.sqrt(2.0)) < 1e-3, (r_small, r_big)


def _t_champion_within_order_of_magnitude():
    # Corrected value should be ~ 1e-11 /yr per beta=1 for champion.
    # Paste's broken version returned ~ 2.5e-35.
    sig = read(a_t=0.92, delta_w=0.10, Delta_a=0.05)
    pref = sig["drift_prefactor_per_yr"]
    assert 1e-12 < pref < 1e-10, pref
    # sensitivities in physical range
    assert 1e-7 < sig["beta_alpha_sensitivity"] < 1e-5, sig["beta_alpha_sensitivity"]
    assert 1e-3 < sig["beta_G_sensitivity"]     < 1e-1, sig["beta_G_sensitivity"]


def _t_reject_phantom_kink():
    # A w0 < -1 (phantom) should refuse: no kinetic energy for canonical field.
    try:
        drift_prefactor(w0=-1.05)
    except ValueError:
        return
    raise AssertionError("phantom w0 should raise")


def _t_anchors_hold():
    # Re-verify the four anchors are still tight (they ran at import,
    # but tests exercise them if constants get edited later).
    _anchor("t A_D1", H0_GeV, 1.438e-42)
    _anchor("t A_D2", YR_GeVINV, 4.795e31, rtol=1e-2)
    _anchor("t A_D3", RHO_C_GeV4, 3.678e-47, rtol=1e-2)


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass\n")


# =========================================================================
# DEMO
# =========================================================================

def _demo():
    here = os.path.dirname(__file__)
    print("=" * 70)
    print("Local scalar drift lens -- F-10 D corrected")
    print("=" * 70)
    print()
    print("Constants (all anchored at import):")
    print(f"  H0                    = {H0_KM_S_MPC} km/s/Mpc  = {H0_GeV:.3e} GeV")
    print(f"  yr_to_GeVinv          = {YR_GeVINV:.3e} GeV^-1")
    print(f"  rho_c today           = {RHO_C_GeV4:.3e} GeV^4")
    print(f"  Reduced Planck M_P    = {M_P_GeV:.3e} GeV")
    print(f"  atomic-clock limit    = {LIMIT_ALPHA_DOT:.0e} /yr  (|α̇/α|)")
    print(f"  lunar-laser limit     = {LIMIT_G_DOT:.0e} /yr  (|Ġ/G|)")
    print()
    configs = [
        {"label": "champion kink (DP-11)",   "kink": (0.92, 0.10, 0.05)},
        {"label": "shallow kink",             "kink": (0.95, 0.05, 0.05)},
        {"label": "strong kink",              "kink": (0.92, 0.20, 0.05)},
        {"label": "quintessence limit 1+w=1", "kink": None},   # handled below
    ]
    print(f"{'label':<28}{'w0':>10}{'1+w0':>9}"
          f"{'β for α detection':>21}{'β for G detection':>21}")
    print("-" * 89)
    for cfg in configs:
        if cfg["kink"] is None:
            # quintessence-limit reference: 1+w = 1
            w0 = 0.0
            pref = drift_prefactor(w0, omega_phi=1.0)
            b_a = LIMIT_ALPHA_DOT / pref
            b_g = LIMIT_G_DOT / pref
        else:
            r = read(*cfg["kink"])
            w0 = r["w0"]
            b_a = r["beta_alpha_sensitivity"]
            b_g = r["beta_G_sensitivity"]
        print(f"{cfg['label']:<28}{w0:>+10.4f}{1+w0:>9.4f}"
              f"{b_a:>21.3e}{b_g:>21.3e}")

    print()
    print("Reading:")
    print("  * Atomic clocks already exclude β_α above a few × 1e-7 for the")
    print("    champion kink -- a present-day laboratory falsifier, no ET-era")
    print("    instrument needed.  This is the surviving DP-11 kink family")
    print("    (energy/PROVENANCE §4 'Still alive') meeting a real gate.")
    print("  * G limit is much looser (β_G ~ 1e-2 required); LLR does not")
    print("    yet touch generic couplings, and improved lunar/atom-int tests")
    print("    would.")
    print("  * Paste's broken version required β > 4e17 for α detection --")
    print("    24 orders too weak.  See F-10 D2/D3 for the two unit bugs.")

    # Plot
    plot_cfgs = [c for c in configs if c["kink"] is not None]
    out_path = os.path.join(here, "..", "figures", "local_scalar_drift.png")
    plot(plot_cfgs, out_path)
    rel = os.path.relpath(out_path, start=os.path.dirname(here))
    print(f"\nwrote {rel}")


if __name__ == "__main__":
    _run()
    _demo()
