#!/usr/bin/env python3
"""
certificate_validity_lens.py -- DP-17 companion.  numpy + scipy + matplotlib.

DP-9 stated that its LP escape cone is a "linear mirage" -- the real
CMB wall is nonlinear (13σ → 141σ between β₁ = 0.05 → 0.1).  This lens
measures how far the linear certificate is trustworthy from a given
base point by sweeping β₁ while pinning every other parameter, fitting
the local tangent, and locating the knee where the actual θ*(β₁)
curve peels away from the linear extrapolation.

Output:
    r̂ = |β₁_onset − β₁_certified| / β₁_certified   [dimensionless]

This is the exportable quantity -- no cosmology in it -- and if it
is stable across base points it names the intrinsic radius of the
LP-certificate around any nonlinear wall.  If it moves with the base
point, it names the certificate radius as a state-dependent property
(also useful, also a puzzle piece).

Reads the same-engine Δθ*_σ per DP-13 -- absolute-vs-Planck σ is
uninterpretable in isolation.

names_no: [intent, verdict].
"""

import os, sys, csv, warnings
import numpy as np
import matplotlib
matplotlib.use('Agg')          # headless
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))
import unified_cq_ede as uc

# per DP-13, theta* is only trustworthy in this mode
uc.R_EQ_MODE = 'physical'
warnings.filterwarnings('ignore', category=RuntimeWarning, module='unified_cq_ede')

# --- base-point definition (see PROVENANCE DP-17) --------------------------
# "Certification point" per DP-9's LP escape cone: closest to the survivable
# frontier the ledger names (DP-8: "survivable combined strength <~ 0.05").
# We take the tip: lambda=1.1 (headline), beta1=0.05, f_ede=0.05, z_c=3162.
CERT_LAM     = 1.1
CERT_BETA1   = 0.05
CERT_FEDE    = 0.05
CERT_ZC      = 3162.0     # matches edelens A3 anchor

BETA1_GRID   = [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.10, 0.12]


def _lcdm_theta_s():
    """Same-engine ΛCDM zero point for Δθ* reporting (per DP-13)."""
    y_i = uc._shoot_y(0.01, 0.0, 0.0, 0.0, 0.0)
    s1, s2, N_c = uc._run_once(0.01, 0.0, 0.0, 0.0, y_i, 0.0, rtol=1e-9)
    _, _, ts = uc.cmb_observables(s1, s2, N_c)
    return ts


def evaluate(lam, beta1, f_ede, z_c=CERT_ZC):
    """Full observable dict at (lam, beta1, f_ede) with same-engine Δθ*_σ."""
    o = uc.solve_unified(lam=lam, beta=0.0, f_ede=f_ede, z_c=z_c, b1=beta1)
    # Δθ*_σ vs same-engine ΛCDM (DP-13); Planck σ = 3e-4 -> 100·|Δ|/0.0003
    delta_ths_sigma = abs(o['theta_s'] - _LCDM_TS) / 0.0003
    return {**o,
            'delta_theta_s_sigma': float(delta_ths_sigma),
            'lcdm_theta_s': _LCDM_TS}


def sweep(lam=CERT_LAM, f_ede=CERT_FEDE, beta1_grid=None):
    if beta1_grid is None:
        beta1_grid = BETA1_GRID
    rows = []
    for b1 in beta1_grid:
        o = evaluate(lam, b1, f_ede)
        rows.append({'lam': lam, 'beta1': b1, 'f_ede': f_ede,
                     'w0': o['w0'], 'wa': o['wa'],
                     'sigma8': o['sigma8'], 'H0': o['H0'],
                     'theta_s': o['theta_s'],
                     'delta_theta_s_sigma': o['delta_theta_s_sigma']})
    return rows


# --- shape analysis --------------------------------------------------------

def _fit_slope(x, y):
    """Least-squares slope + R² for y = slope*x + intercept."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    y_pred = slope * x + intercept
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1.0 - ss_res / (ss_tot + 1e-30)
    return float(slope), float(intercept), float(r2)


DEV_TOL = 0.20   # LP-tangent deviation threshold: 20% off = certificate broken


def analyze(rows, beta1_certified):
    """
    Find the LP-certificate onset: the first β₁ where the actual
    Δθ*(β₁) curve deviates from a **linear-in-β₁** tangent taken at
    beta1_certified by more than DEV_TOL (20%).  The LP escape cone
    from DP-9 IS a linear-in-parameter-space certificate, so this is
    the physically-meaningful criterion.  Also reports log-log and
    log-linear fits as shape diagnostics (which functional class
    dominates the curve).

    Returns:
      - power_slope, power_r2   log-log fit; θ*_σ ∝ β₁^p
      - exp_slope,  exp_r2      log-linear fit; θ*_σ ∝ e^{k·β₁}
      - tangent_slope           dΔθ*/dβ₁ at beta1_certified [σ per β₁]
      - onset_beta1             first β₁ where actual deviates from
                                linear tangent by > DEV_TOL
      - r_hat                   |onset − certified| / certified
    """
    b1 = np.array([r['beta1'] for r in rows])
    ts = np.array([r['delta_theta_s_sigma'] for r in rows])
    mask = (ts > 0)
    b1m, tsm = b1[mask], ts[mask]

    ps, _, pr2 = _fit_slope(np.log(b1m), np.log(tsm))
    es, _, er2 = _fit_slope(b1m, np.log(tsm))

    # linear-in-β₁ tangent at the certification point
    i0 = int(np.argmin(np.abs(b1m - beta1_certified)))
    if 0 < i0 < len(b1m) - 1:
        tangent = (tsm[i0 + 1] - tsm[i0 - 1]) / (b1m[i0 + 1] - b1m[i0 - 1])
    elif i0 == 0:
        tangent = (tsm[1] - tsm[0]) / (b1m[1] - b1m[0])
    else:
        tangent = (tsm[-1] - tsm[-2]) / (b1m[-1] - b1m[-2])
    ts_at_cert = tsm[i0]

    # scan outward from certified point: linear extrapolation vs actual
    onset = None
    for j in range(i0 + 1, len(b1m)):
        predicted = ts_at_cert + tangent * (b1m[j] - beta1_certified)
        actual = tsm[j]
        rel_dev = abs(actual - predicted) / max(abs(predicted), 1e-9)
        if rel_dev > DEV_TOL:
            onset = float(b1m[j])
            break

    r_hat = float('nan') if onset is None else abs(onset - beta1_certified) / beta1_certified

    return {'power_slope': ps, 'power_r2': pr2,
            'exp_slope': es, 'exp_r2': er2,
            'log_log_wins': pr2 >= er2,
            'tangent_slope': float(tangent),
            'ts_at_certified': float(ts_at_cert),
            'onset_beta1': onset,
            'r_hat': r_hat}


# --- I/O -------------------------------------------------------------------

def write_csv(rows, path):
    keys = ['lam', 'beta1', 'f_ede', 'w0', 'wa', 'sigma8', 'H0',
            'theta_s', 'delta_theta_s_sigma']
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in keys})


def plot(rows_a, rows_b, out_path, cert_beta1):
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    for rows, lam, marker in [(rows_a, rows_a[0]['lam'], 'o'),
                              (rows_b, rows_b[0]['lam'], 's')]:
        b1 = [r['beta1'] for r in rows]
        ts = [r['delta_theta_s_sigma'] for r in rows]
        # log-log
        ax[0].loglog(b1, ts, marker + '-', label=f'λ = {lam}')
        # log-linear
        ax[1].semilogy(b1, ts, marker + '-', label=f'λ = {lam}')
    for a in ax:
        a.axvline(cert_beta1, ls=':', c='k', alpha=0.5,
                  label=f'certified β₁ = {cert_beta1}')
        a.set_ylabel(r'$\Delta\theta_*$  [same-engine σ]')
        a.grid(True, which='both', alpha=0.3)
        a.legend(fontsize=9)
    ax[0].set_xlabel(r'$\beta_1$'); ax[0].set_title('log–log (power law)')
    ax[1].set_xlabel(r'$\beta_1$'); ax[1].set_title('log–linear (exponential)')
    fig.suptitle('DP-17 Certificate validity radius: Δθ*(β₁) vs certified point')
    fig.tight_layout()
    fig.savefig(out_path, dpi=110, bbox_inches='tight')
    plt.close(fig)


# --- LCDM zero point (memoized) --------------------------------------------
_LCDM_TS = _lcdm_theta_s()


# --- self-test -------------------------------------------------------------

def _t_lcdm_zero_point_matches_bisect():
    assert abs(_LCDM_TS - 1.04020) < 1e-4, _LCDM_TS


def _t_evaluate_returns_positive_theta_sigma():
    o = evaluate(1.1, 0.05, 0.05)
    assert o['delta_theta_s_sigma'] >= 0
    assert 'theta_s' in o


def _t_sweep_monotone_growth_of_theta_shift():
    rows = sweep(lam=1.1, f_ede=0.05, beta1_grid=[0.02, 0.05, 0.10])
    ts = [r['delta_theta_s_sigma'] for r in rows]
    assert ts[-1] > ts[0], ts   # bigger coupling -> bigger CMB shift


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith('_t_'):
            fn(); print('ok', name)
    print('all pass\n')


def _demo():
    here = os.path.dirname(__file__)
    print(f"same-engine ΛCDM 100θ* = {_LCDM_TS:.5f}  (Δ column is against this)")
    print()

    # base point A: DP-9 certification point
    print(f"=== base point A: λ={CERT_LAM}, β₁_certified={CERT_BETA1}, "
          f"f_ede={CERT_FEDE} ===")
    rows_a = sweep(lam=CERT_LAM, f_ede=CERT_FEDE)
    for r in rows_a:
        marker = ' <- certified' if abs(r['beta1'] - CERT_BETA1) < 1e-6 else ''
        print(f"  β₁={r['beta1']:.2f}  Δθ*={r['delta_theta_s_sigma']:>7.2f}σ"
              f"  w0={r['w0']:+.3f}  σ8={r['sigma8']:.3f}"
              f"  H0={r['H0']:.2f}{marker}")
    ana_a = analyze(rows_a, CERT_BETA1)
    print(f"  power fit:  slope = {ana_a['power_slope']:+.2f}, R² = {ana_a['power_r2']:.4f}")
    print(f"  exp fit:    slope = {ana_a['exp_slope']:+.2f}, R² = {ana_a['exp_r2']:.4f}")
    print(f"  winner:     {'log-log (power law)' if ana_a['log_log_wins'] else 'log-linear (exponential)'}")
    print(f"  linear tangent dΔθ*/dβ₁ at cert: {ana_a['tangent_slope']:+.1f} σ per β₁")
    print(f"  onset β₁ (LP extrapolation >20% off): {ana_a['onset_beta1']}")
    print(f"  r̂ = {ana_a['r_hat']}")

    # base point B: shift lambda to test r̂ stability
    print()
    LAM_B = 0.9
    print(f"=== base point B: λ={LAM_B}, β₁_certified={CERT_BETA1}, "
          f"f_ede={CERT_FEDE}  (r̂-stability test) ===")
    rows_b = sweep(lam=LAM_B, f_ede=CERT_FEDE)
    for r in rows_b:
        marker = ' <- certified' if abs(r['beta1'] - CERT_BETA1) < 1e-6 else ''
        print(f"  β₁={r['beta1']:.2f}  Δθ*={r['delta_theta_s_sigma']:>7.2f}σ"
              f"  w0={r['w0']:+.3f}  σ8={r['sigma8']:.3f}"
              f"  H0={r['H0']:.2f}{marker}")
    ana_b = analyze(rows_b, CERT_BETA1)
    print(f"  power slope = {ana_b['power_slope']:+.2f} (R² {ana_b['power_r2']:.4f}), "
          f"exp slope = {ana_b['exp_slope']:+.2f} (R² {ana_b['exp_r2']:.4f})")
    print(f"  onset β₁ = {ana_b['onset_beta1']},  r̂ = {ana_b['r_hat']}")

    # write artifacts
    csv_path = os.path.join(here, '..', 'sweeps', 'certificate_validity.csv')
    write_csv(rows_a + rows_b, csv_path)
    print(f"\nwrote {os.path.relpath(csv_path, start=os.path.dirname(here))}"
          f"  ({len(rows_a) + len(rows_b)} rows)")

    fig_path = os.path.join(here, '..', 'figures', 'certificate_validity.png')
    plot(rows_a, rows_b, fig_path, CERT_BETA1)
    print(f"wrote {os.path.relpath(fig_path, start=os.path.dirname(here))}")

    # interpret
    print()
    if np.isfinite(ana_a['r_hat']) and np.isfinite(ana_b['r_hat']):
        rel = abs(ana_a['r_hat'] - ana_b['r_hat']) / max(ana_a['r_hat'], ana_b['r_hat'], 1e-9)
        print(f"r̂(λ=1.1) = {ana_a['r_hat']:.3f},   r̂(λ=0.9) = {ana_b['r_hat']:.3f}"
              f"   (relative difference {rel*100:.0f}%)")
        if rel < 0.30:
            print("→ r̂ is stable across base points: property of the wall.")
        else:
            print("→ r̂ moves with the base point: state-dependent certificate radius.")
    else:
        print("→ onset not localized in the swept range at one or both base points.")
        print("  DP-17 records this as a regime tag, not a failure.")


if __name__ == '__main__':
    _run(); _demo()
