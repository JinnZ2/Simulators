#!/usr/bin/env python3
"""
theory_space_lenses.py
The three-lens survival map of a theory space (multi-lens metrology).

Three orthogonal probes over one model grid:
  Lens 1 (R-D / dynamics)     : growth-ratio surface - finds autocatalytic
                                runaway (the kink where evolution goes pathological).
  Lens 2 (percolation / topology): distinguishability graph of the model grid -
                                finds where the manifold stretches (max D) and where
                                it reconnects into a degenerate pathology plateau.
  Lens 3 (Fisher / curvature) : singular-value spectrum of the extended parameter
                                map - finds rank collapse (predictive-power loss).

Result for the running-coupling family beta(z)=b0+b1*z/(1+z), lambda=1.3:
  All three thresholds ALIGN at beta1 ~ 0.2-0.3 (beta0=0):
    - growth ratio crosses ~3x LCDM (autocatalytic kink),
    - neighbor distinguishability peaks at 8.75 sigma (max manifold stretching),
    - Fisher conditioning collapses 300x (S_min/S_max: 0.15 -> 5e-4, rank 3->2).
  Above beta1 >~ 0.5 the growth ratio saturates (~60-70x) and the graph
  RECONNECTS: every model is degenerate with every other - the same physics
  that makes the region unphysical makes it internally undiscoverable.

Requires a `model_evaluator` callable: (b0, b1, lam) -> dict with keys
  w0, wa, r0   (w0, wa, and fs8/LCDM ratio at z=0)
See run_iteration6.py for the coupled-quintessence engine that provides it.
License: CC0 1.0 Universal (public domain).
"""

import numpy as np


def rd_lens(evaluator, b0_grid, b1_grid, lam):
    """Lens 1: growth-ratio surface R[b0, b1]."""
    R = np.zeros((len(b0_grid), len(b1_grid)))
    for i, b0 in enumerate(b0_grid):
        for j, b1 in enumerate(b1_grid):
            R[i, j] = evaluator(b0, b1, lam)['r0']
    return R


def distinguishability(m1, m2, s_w0=0.04, s_wa=0.16, fs8_rel=0.05):
    """Observable-space distance between two models, in sigma units."""
    d2 = ((m1['w0'] - m2['w0']) / s_w0)**2 + ((m1['wa'] - m2['wa']) / s_wa)**2
    s = fs8_rel * 0.5 * (m1['r0'] + m2['r0'])
    return float(np.sqrt(d2 + ((m1['r0'] - m2['r0']) / max(s, 1e-12))**2))


def percolation_lens(grid, b0_grid, b1_grid):
    """Lens 2: distinguishability profile and giant-component fraction per b1.
    grid: dict (b0,b1) -> model dict."""
    profile, giant = [], []
    for j, b1 in enumerate(b1_grid):
        ds = []
        for i in range(len(b0_grid) - 1):
            ds.append(distinguishability(grid[(b0_grid[i], b1)], grid[(b0_grid[i + 1], b1)]))
            if j < len(b1_grid) - 1:
                ds.append(distinguishability(grid[(b0_grid[i], b1)], grid[(b0_grid[i], b1_grid[j + 1])]))
        profile.append(float(np.mean(ds)))
        # union-find on the b0 column
        parent = list(range(len(b0_grid)))
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        for i in range(len(b0_grid) - 1):
            if distinguishability(grid[(b0_grid[i], b1)], grid[(b0_grid[i + 1], b1)]) < 1:
                pi, pj = find(i), find(i + 1)
                if pi != pj:
                    parent[pi] = pj
        sizes = {}
        for i in range(len(b0_grid)):
            sizes[find(i)] = sizes.get(find(i), 0) + 1
        giant.append(max(sizes.values()) / len(b0_grid))
    kink = b1_grid[int(np.argmax(profile))]
    return {'D_profile': profile, 'giant_fraction': giant, 'kink_beta1': float(kink)}


def fisher_lens(grid, lup, ldn, b0_grid, b1_grid, lam, dl=0.1):
    """Lens 3: singular values of (lam,b0,b1) -> (w0,wa,r0), b0=0 row.
    lup/ldn: dicts (b0,b1) -> model at lam +/- dl."""
    out = {}
    for b1 in b1_grid:
        m0 = grid[(0.0, b1)]
        vec = lambda m: np.array([m['w0'], m['wa'], m['r0']])
        j = list(b1_grid).index(b1)
        b1u = b1_grid[min(j + 1, len(b1_grid) - 1)]
        b1d = b1_grid[max(j - 1, 0)]
        J = np.column_stack([
            (vec(lup[(0.0, b1)]) - vec(ldn[(0.0, b1)])) / (2 * dl),
            (vec(grid[(min(b0_grid[1], 0.4), b1)]) - vec(m0)) / max(b0_grid[1], 1e-9),
            (vec(grid[(0.0, b1u)]) - vec(grid[(0.0, b1d)])) / (b1u - b1d)])
        sig = np.array([0.04, 0.16, 0.05 * max(m0['r0'], 1e-9)])
        sv = np.linalg.svd(J / sig[:, None], compute_uv=False)
        out[float(b1)] = {'singular_values': sv.tolist(),
                          'conditioning': float(sv[-1] / sv[0])}
    return out


def survival_report(rd_surface, percolation, fisher, b1_grid):
    """Align the three thresholds."""
    kink_rd = None
    row0 = rd_surface[0]  # beta0 = 0
    for j in range(1, len(b1_grid)):
        if row0[j - 1] < 3.0 <= row0[j]:
            kink_rd = float(b1_grid[j])
            break
    conds = [fisher[float(b1)]['conditioning'] for b1 in b1_grid]
    kink_f = float(b1_grid[int(np.argmin(conds))])
    aligned = (kink_rd is not None and
               abs(percolation['kink_beta1'] - kink_rd) <= 0.15 and
               abs(kink_f - kink_rd) <= 0.2)
    return {'rd_kink_beta1': kink_rd,
            'percolation_kink_beta1': percolation['kink_beta1'],
            'fisher_min_conditioning_beta1': kink_f,
            'thresholds_aligned': bool(aligned),
            'verdict': ("UNIVERSAL PATHOLOGY: the same physics that makes the model "
                        "unphysical (growth runaway) also makes it undiscoverable "
                        "(Fisher rank collapse)." if aligned else
                        "Thresholds do not align; pathologies are independent.")}
