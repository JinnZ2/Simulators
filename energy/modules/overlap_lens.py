"""
overlap_lens.py — Unified theory-space lens: CQ x EDE in the common observable plane.

Bridges the two engines by mapping both manifolds into (sigma8, H0) space and asking:

  1. CLOSEST PAIR — where do the theories come nearest to each other, in
     Mahalanobis units of the canonical (2% sigma8, 1 km/s/Mpc H0) covariance?
  2. AMBIGUITY BAND — which EDE points live within <thresh> sigma of ANY CQ point?
     (data cannot separate those regions: same observables, different physics)
  3. HOLOGRAPHIC CANCELLATION — scan composite models (coupling beta x f_EDE):
     does the CQ growth enhancement cancel the EDE growth suppression, leaving
     a LCDM-like sigma8 while H0 stays raised?

Data-space convention: both manifolds are taken RELATIVE to their own LCDM anchor,
so only physically meaningful (ratio) information crosses the bridge — the CQ
engine's absolute-normalization artifact never contaminates the comparison.

Usage:
    python overlap_lens.py            # full demo (needs playground_data.json + edelens.py)
"""

import numpy as np
import json, os

# Canonical observable covariance: 2% on sigma8, 1 km/s/Mpc on H0, rho = -0.4
S8_REF, H0_REF = 0.81, 67.4
COV = np.array([[(0.02 * S8_REF)**2, -0.4 * 0.02 * S8_REF * 1.0],
                [-0.4 * 0.02 * S8_REF * 1.0, 1.0**2]])
ICOV = np.linalg.inv(COV)


def mahalanobis(p, q, icov=ICOV):
    d = np.asarray(p) - np.asarray(q)
    return float(np.sqrt(d @ icov @ d))


def closest_pair(cq, ede):
    """cq, ede: lists of dicts with keys 's8','H0' (+labels). Returns dict."""
    best = None
    for c in cq:
        for e in ede:
            D = mahalanobis((c['s8'], c['H0']), (e['s8'], e['H0']))
            if best is None or D < best['D']:
                best = {'D': D, 'cq': c, 'ede': e}
    return best


def ambiguity_band(cq, ede, thresholds=(1.0, 2.0)):
    """Fraction of EDE points within <t> sigma of the nearest CQ point."""
    out = {}
    for t in thresholds:
        n = sum(1 for e in ede
                if min(mahalanobis((c['s8'], c['H0']), (e['s8'], e['H0'])) for c in cq) < t)
        out[t] = (n, len(ede))
    return out


def cancellation_scan(cq, ede, s8_target=S8_REF, s8_window=0.016,
                      h0_min=68.5, h0_window=1.0):
    """
    Composite model: sigma8 = sigma8_CQ * sigma8_EDE / S8_REF  (relative-to-anchor product),
    H0 = H0_EDE. Flag pairs that land within s8_window of the LCDM sigma8 while H0 > h0_min.
    """
    hits = []
    for c in cq:
        for e in ede:
            s8 = c['s8'] * e['s8'] / S8_REF
            H0 = e['H0']
            if abs(s8 - s8_target) < s8_window and abs(H0 - h0_min) < h0_window and H0 > h0_min:
                hits.append({'s8': s8, 'H0': H0, 'cq': c, 'ede': e})
    return hits


def load_cq_manifold(path='../app/playground_data.json', alpha0=-0.2):
    """CQ line from the playground scan, per-lambda fs8-normalized (physical ratios).

    Models are keyed '{lam}_{beta}_{alpha}'; fs8 arrays are sampled on the z-grid
    (index 8 = z 0.8). One alpha slice (nearest to alpha0) defines the manifold.
    """
    raw = json.load(open(path))
    pts = []
    for key, m in raw['models'].items():
        lam, beta, alpha = (float(t) for t in key.split('_'))
        pts.append({'lam': lam, 'beta': beta, 'alpha': alpha,
                    'fs8_008': m['fs8'][8], 'w0': m['w'][0]})
    alphas = sorted({p['alpha'] for p in pts})
    a_sel = min(alphas, key=lambda a: abs(a - alpha0))
    sl = [p for p in pts if p['alpha'] == a_sel]
    base = {}
    for p in sl:
        if abs(p['beta']) < 1e-12:
            base[round(p['lam'], 2)] = p['fs8_008']
    cq = []
    for p in sl:
        lam = round(p['lam'], 2)
        if lam not in base:
            continue
        cq.append({'lam': p['lam'], 'beta': p['beta'],
                   's8': S8_REF * p['fs8_008'] / base[lam], 'H0': 67.4})
    return cq


def build_ede_manifold():
    """EDE arc from the edelens engine (falls back to a labeled stand-in if absent)."""
    try:
        import edelens
        cache = {}
        ede = []
        for lz in np.linspace(3.0, 4.0, 5):
            for fe in np.linspace(0.01, 0.15, 8):
                ob = edelens.observables(10.0 ** lz, fe, cache)
                ede.append({'lz': lz, 'f': fe,
                            'H0': 67.4 * ob['H0'], 's8': S8_REF * ob['s8']})
        return ede, 'edelens engine'
    except Exception as ex:
        # Labeled stand-in: rough EDE arc (NOT for science, keeps the demo runnable)
        print(f'  [stand-in EDE grid: {ex}]')
        ede = []
        for lz in np.linspace(3.0, 4.0, 5):
            for fe in np.linspace(0.01, 0.15, 8):
                ede.append({'lz': lz, 'f': fe,
                            'H0': 67.4 + 28.0 * fe * (1 - 0.4 * (lz - 3.0)),
                            's8': S8_REF * (1 + 1.35 * fe)})
        return ede, 'STAND-IN (not physical)'


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    cq = load_cq_manifold(os.path.join(here, '..', 'app', 'playground_data.json'))
    ede, src = build_ede_manifold()
    print(f'CQ manifold: {len(cq)} pts | EDE manifold: {len(ede)} pts [{src}]')

    cp = closest_pair(cq, ede)
    print(f"\nCLOSEST PAIR: D = {cp['D']:.2f} sigma")
    print(f"  CQ : lam={cp['cq']['lam']}, beta={cp['cq']['beta']:+.2f}  "
          f"(s8={cp['cq']['s8']:.3f}, H0={cp['cq']['H0']:.1f})")
    print(f"  EDE: log10zc={cp['ede']['lz']:.2f}, f={cp['ede']['f']:.2f}  "
          f"(s8={cp['ede']['s8']:.3f}, H0={cp['ede']['H0']:.1f})")

    band = ambiguity_band(cq, ede)
    for t, (n, N) in band.items():
        print(f'AMBIGUITY: {n}/{N} EDE points within {t:.0f} sigma of CQ manifold')

    hits = cancellation_scan(cq, ede)
    print(f'\nHOLOGRAPHIC CANCELLATION: {len(hits)} composite pairs with '
          f'sigma8 ~ LCDM and H0 > 68.5')
    for h in hits[:5]:
        print(f"  beta={h['cq']['beta']:+.2f} x f_EDE={h['ede']['f']:.2f} "
              f"(logzc={h['ede']['lz']:.2f}) -> s8={h['s8']:.3f}, H0={h['H0']:.1f}")


if __name__ == '__main__':
    main()
