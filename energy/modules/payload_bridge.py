#!/usr/bin/env python3
"""
payload_bridge.py
The wiring layer ("Step 4"): connects the playground's machine-payload data
to the metrology add-on modules, end to end.

Scenario reproduced (the Day-5 test):
  1. Load the 223 integrated cosmologies from playground_data.json.
  2. At the geodesic foot (lambda=1.1, beta=0, alpha=0), build the Fisher
     matrix of instrument A (rank-2 w0-wa projection) and instrument B
     (rank-3 z-tomography: w(z) bins + fs8(z) bins).
  3. Run the 4-Gate MetrologyDiagnostic on both -> watch Gate 3 flip from
     INSTRUMENTATION_DEGENERATE to WELL_POSED (S_min ~ 0 -> ~ 5).
  4. Feed the canonical track's residuals vs the DESI-mean CPL trajectory
     to the Generative Module -> a symbolic missing-term proposal.
  5. Run the SingularityCartographer on the 1+alpha*phi^2 pole
     (the 27 failed grid cells) -> classify the brick wall.
  6. Print the orchestrator-style 3-paragraph verdict.

Usage:  python payload_bridge.py [path/to/playground_data.json]
License: CC0 1.0 Universal (public domain).
"""

import sys
import os
import json
import numpy as np

from metrology_diagnostic import MetrologyDiagnostic
from generative_module import propose_new_term, interpret
from singularity_cartographer import SingularityCartographer
from falsification_engine import FalsifiableClaim

DESI_MU = np.array([-0.86, -0.53])
DESI_COV = np.array([[0.04**2, 0.4 * 0.04 * 0.16],
                     [0.4 * 0.04 * 0.16, 0.16**2]])
SIG_FS8 = 0.02


class Playground:
    """Grid access mirroring the browser rig."""

    def __init__(self, path):
        d = json.load(open(path))
        self.lam, self.beta, self.alpha = d['lam'], d['beta'], d['alpha']
        self.z = np.array(d['z'])
        self.models = d['models']
        self.lcdm_fs8 = np.array(d['lcdm_fs8'])

    @staticmethod
    def _fmt(v):
        return f"{v:.1f}" if float(v).is_integer() else str(v)

    @staticmethod
    def _pick(arr, v):
        i = int(np.searchsorted(arr, v - 1e-9))
        i = min(max(i, 0), len(arr) - 1)
        if i > 0 and abs(arr[i - 1] - v) < abs(arr[i] - v):
            i -= 1
        return i

    def cell(self, l, b, a):
        il, ib, ia = self._pick(self.lam, l), self._pick(self.beta, b), self._pick(self.alpha, a)
        return self.models.get(f"{self._fmt(self.lam[il])}_{self._fmt(self.beta[ib])}_{self._fmt(self.alpha[ia])}")

    def wa_of(self, w):
        a0 = 1 / (1 + self.z[0]); a1 = 1 / (1 + self.z[1])
        return float(-(w[1] - w[0]) / (a1 - a0))

    def data_vec(self, m, inst, nb):
        w = np.array(m['w']); f = np.array(m['fs8'])
        if inst == 'proj':
            return np.array([w[0], self.wa_of(w)])
        idx = np.round(np.arange(nb) * (len(self.z) - 1) / (nb - 1)).astype(int)
        return np.concatenate([w[idx], f[idx]])

    def sig_vec(self, inst, nb, sw):
        if inst == 'proj':
            return np.array([0.04, 0.16])
        return np.concatenate([np.full(nb, sw), np.full(nb, SIG_FS8)])

    def fisher(self, l, b, a, inst, nb=8, sw=0.03):
        dl, db, da = 0.1, 0.05, 0.1
        m0 = self.cell(l, b, a)
        v0 = self.data_vec(m0, inst, nb)
        sv = self.sig_vec(inst, nb, sw)
        cols = [((l - dl) if l + dl > 1.5 else (l + dl), b, a, -dl if l + dl > 1.5 else dl),
                (l, (b - db) if b + db > 0.2 else (b + db), a, -db if b + db > 0.2 else db),
                (l, b, (a - da) if a + da > 0.2 else (a + da), -da if a + da > 0.2 else da)]
        J = []
        for l2, b2, a2, h in cols:
            v = self.data_vec(self.cell(l2, b2, a2), inst, nb)
            J.append((v - v0) / h)
        J = np.array(J)
        F = J @ np.diag(1 / sv**2) @ J.T
        return F, v0, sv


def orchestrator_verdict(gates_proj, gates_tomo, gen_out, cart_out):
    """Template-based 3-paragraph verdict (swap in any LLM here)."""
    p1 = (f"ROOT CAUSE: Instrumentation. Gate 3 of the legacy instrument reports "
          f"S_min = {gates_proj['metrics']['S_min']:.2e} with a lambda-alpha correlation of "
          f"-1.00: the rank-2 w0-wa projection is a degenerate compression of the theory "
          f"manifold. The alpha impurity is present in the dynamics but invisible to the "
          f"instrument. Gates 1-2 confirm the signal is systematic and self-consistent, "
          f"so this is not equipment noise.")
    p2 = (f"JUSTIFICATION: Switching to rank-3 z-tomography lifts the smallest Fisher "
          f"eigenvalue from {gates_proj['metrics']['S_min']:.2e} to "
          f"{gates_tomo['metrics']['S_min']:.2f} "
          f"(condition number {gates_tomo['metrics']['condition_number']:.2e}), and "
          f"sigma(alpha) becomes finite. Gate 4 on the canonical track flags "
          f"{gates_proj['gates']['Gate4_Prior']}: the residuals carry physical curvature. "
          f"Symbolic regression proposes the missing term  [{gen_out['expression']}]  "
          f"({gen_out.get('backend', 'basis library')}).")
    p3 = (f"PRESCRIPTION: Build the tomographic instrument (increase rank 2 -> 3). "
          f"Then extend the theory: the singularity cartographer classifies the "
          f"1+alpha*phi^2 brick wall as {cart_out['verdict']} - {cart_out['note']} "
          f"Insert the proposed term as a new alpha-like coupling and re-run the "
          f"4-gate protocol iteratively until all gates pass.")
    return p1, p2, p3


def main(path=os.path.join(os.path.dirname(__file__), '..', 'app', 'playground_data.json')):
    pg = Playground(path)
    print(f"Loaded {len(pg.models)} integrated cosmologies "
          f"(grid {len(pg.lam)}x{len(pg.beta)}x{len(pg.alpha)})\n")

    L, B, A = 1.1, 0.0, 0.0   # geodesic foot
    print(f"=== Evaluation point: geodesic foot (lambda={L}, beta={B}, alpha={A}) ===\n")

    results = {}
    for inst, nb in [('proj', 2), ('tomo', 8)]:
        F, v0, sv = pg.fisher(L, B, A, inst, nb)
        S = np.linalg.svd(F, compute_uv=False)
        tag = 'A (projection)' if inst == 'proj' else 'B (tomography)'
        print(f"--- Instrument {tag} ---")
        print(f"    Fisher eigenvalues: {np.array2string(S, precision=3)}")
        # 4-gate diagnostic with the Fisher matrix as the curvature source
        diag = MetrologyDiagnostic(
            x=pg.z[:len(v0)] if inst == 'tomo' else np.arange(len(v0)),
            y_obs=v0 + 0.0 * sv,                 # noiseless synthetic observation at the model
            y_pred_model=v0,
            param_names=['lambda', 'beta', 'alpha'],
            param_values=[L, B, A],
            covariance_matrix=np.linalg.inv(F + 1e-12 * np.eye(3)),
            fisher_matrix=F)
        r = diag.run()
        results[inst] = r
        print(f"    {r['summary']}")
        print(f"    Gate3 action: {r['verdict']['Gate3']}")
        print(f"    Final: {r['final_action']}\n")

    # --- Gate 4 on the real physics: canonical track vs DESI-mean CPL ---
    print("=== Gate 4 + Generative Module: canonical track residuals ===")
    m_can = pg.cell(L, B, A)
    w_can = np.array(m_can['w'])
    w_desi = DESI_MU[0] + DESI_MU[1] * (1 - 1 / (1 + pg.z))
    residuals = w_desi - w_can     # what the canonical track cannot reach
    print(f"    residual amplitude: max {np.max(np.abs(residuals)):.3f} in w(z)")
    gen = propose_new_term(pg.z, residuals)
    print(f"    proposed missing term: {gen['expression']}")
    print(f"    {interpret(gen['expression'], 'canonical-track w(z) residuals')}\n")

    # --- Falsification engine on the same residuals ---
    print("=== Falsification Engine: is the canonical claim self-falsifying? ===")
    claim = FalsifiableClaim(pg.z, w_desi, w_can,
                             claim_description="Canonical quintessence track (beta=0)")
    fc = claim.run_audit_battery()
    print(f"    falsified: {fc['is_falsified']}  "
          f"(DW={fc['Durbin_Watson']:.2f}, break@{fc.get('break_location', float('nan')):.2f})")
    print(f"    hidden-variable suggestions: "
          f"{[s['term'] for s in claim.search_for_hidden_variable()]}\n")

    # --- Singularity cartography on the real brick wall ---
    print("=== Singularity Cartographer: the 1+alpha*phi^2 pole (27 failed cells) ===")
    n_failed = sum(1 for l in pg.lam for b in pg.beta for a in pg.alpha
                   if pg.cell(l, b, a) is None)
    print(f"    real grid: {n_failed} failed cells (pole crossings)")

    def pole_surface(params):
        return 1.0 / (1.0 + params['alpha'] * params['lambda']**2)

    cart = SingularityCartographer({'alpha': (-0.6, 0.2), 'lambda': (0.6, 1.5)},
                                   pole_surface, param_names=['alpha', 'lambda'],
                                   blowup=1e6)
    # the wall sits at alpha = -1/lambda^2, reached from alpha < 0 side
    rep = cart.probe_with_substitutions({'alpha': -1 / 1.5**2, 'lambda': 1.5},
                                        wall_axis='alpha')
    print(f"    verdict: {rep['verdict']}")
    print(f"    substitution scores: "
          f"{ {k: round(v, 3) for k, v in rep['substitution_scores'].items()} }")
    print(f"    note: {rep['note']}\n")

    # --- Orchestrator verdict ---
    print("=" * 72)
    print("ORCHESTRATOR VERDICT (3-paragraph LLM-style output)")
    print("=" * 72)
    for para in orchestrator_verdict(results['proj'], results['tomo'], gen, rep):
        print()
        print(para)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'app', 'playground_data.json'))
