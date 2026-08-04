#!/usr/bin/env python3
"""
singularity_cartographer.py
A metrology tool that hits mathematical brick walls on purpose,
tries every meaningful substitution, and classifies the wall:
  COORDINATE_GAUGE  - gauge artifact: change variables, it disappears
  SIMPLE_POLE       - 1/(x-x0): add a residue term
  DOUBLE_POLE       - 1/(x-x0)^2: sharp boundary (the 1+alpha*phi^2 pole)
  BRANCH_CUT        - log singularity: multi-valued physics, new sheet
  PHASE_TRANSITION  - sqrt threshold: tachyonic / imaginary beyond
  TRUE_HORIZON      - no substitution works: NEW MATH REQUIRED
License: CC0 1.0 Universal (public domain).
"""

import numpy as np
from scipy.stats import pearsonr


class SingularityCartographer:
    def __init__(self, param_ranges, residual_function, param_names=None,
                 blowup=1e10):
        self.ranges = param_ranges
        self.res_func = residual_function
        self.names = list(param_ranges.keys()) if param_names is None else param_names
        self.blowup = blowup
        self.brick_walls = []

    def _is_wall(self, params):
        try:
            val = self.res_func(params)
            return (not np.isfinite(val)) or abs(val) > self.blowup
        except (ZeroDivisionError, OverflowError, ValueError, FloatingPointError):
            return True

    def scan_for_singularities(self, grid_density=20):
        p1, p2 = self.names[0], self.names[1] if len(self.names) > 1 else self.names[0]
        v1 = np.linspace(*self.ranges[p1], grid_density)
        v2 = np.linspace(*self.ranges[p2], grid_density)
        walls = []
        for a in v1:
            for b in v2:
                params = {p1: a, p2: b}
                for name in self.names[2:]:
                    params[name] = sum(self.ranges[name]) / 2
                if self._is_wall(params):
                    walls.append((float(a), float(b)))
        self.brick_walls = walls
        return walls

    def probe_with_substitutions(self, wall_params, wall_axis=None):
        """Approach the wall along `wall_axis` (default: first param) and
        correlate the approach profile against candidate substitutions."""
        p_name = wall_axis or self.names[0]
        lo, hi = self.ranges[p_name]
        # Refine the wall location: the scan only lands NEAR the pole.
        # Maximize |res| on a fine local scan to pin the true divergence.
        w0 = wall_params[p_name]
        fine = np.linspace(max(w0 - 0.1, lo), min(w0 + 0.1, hi), 400)
        best_x, best_v = w0, 0.0
        for xv in fine:
            tp = dict(wall_params); tp[p_name] = xv
            try:
                vv = abs(self.res_func(tp))
                if np.isfinite(vv) and vv > best_v:
                    best_x, best_v = xv, vv
            except Exception:
                best_x = xv            # exact pole: error at this point
                break
        wall_value = best_x
        wall_params = dict(wall_params); wall_params[p_name] = wall_value
        # approach from the side that lies inside the allowed range
        if wall_value + 0.4 <= hi:
            approach = np.linspace(wall_value + 1e-3, wall_value + 0.4, 40)
        else:
            approach = np.linspace(wall_value - 0.4, wall_value - 1e-3, 40)

        vals = []
        for v in approach:
            tp = dict(wall_params); tp[p_name] = v
            try:
                vals.append(self.res_func(tp))
            except Exception:
                vals.append(np.nan)
        vals = np.asarray(vals, dtype=float)
        mask = np.isfinite(vals)
        if mask.sum() < 5:
            return {"verdict": "TRUE_HORIZON",
                    "note": "Function vanishes before the wall. No approach allowed.",
                    "wall_location": wall_params}
        x, y = approach[mask], vals[mask]
        d = x - wall_value

        scores = {}
        candidates = {
            'reciprocal': 1.0 / d,
            'inverse_square': 1.0 / d**2,
            'logarithmic': np.log(np.abs(d)),
            'sqrt': np.sqrt(np.abs(d)),
            'even_offset': d**2,
        }
        for name, xs in candidates.items():
            if np.all(np.isfinite(xs)) and np.std(xs) > 0 and np.std(y) > 0:
                scores[name] = abs(float(pearsonr(xs, y)[0]))

        if not scores:
            return {"verdict": "TRUE_HORIZON", "note": "No valid substitution data.",
                    "wall_location": wall_params}

        best_sub = max(scores, key=scores.get)
        best = scores[best_sub]
        notes = {
            'reciprocal': ("SIMPLE_POLE",
                f"Wall behaves like 1/(x - {wall_value:.3f}). Add a residue term with a new coupling."),
            'inverse_square': ("DOUBLE_POLE",
                "Wall behaves like 1/(x - x0)^2. Sharp boundary in the potential "
                "(the 1+alpha*phi^2 pole). Regularize or add a residue-squared term."),
            'logarithmic': ("BRANCH_CUT",
                "Logarithmic singularity: multi-valued physics. Add an analytic-continuation sheet."),
            'sqrt': ("PHASE_TRANSITION",
                "Square-root threshold: beyond the wall the mode goes imaginary (tachyonic)."),
            'even_offset': ("COORDINATE_GAUGE",
                f"Singularity vanishes under x' = x - {wall_value:.3f}. Pure coordinate artifact: "
                "keep the math, change the variable."),
        }
        if best > 0.95:
            verdict, note = notes[best_sub]
        else:
            verdict = "TRUE_HORIZON"
            note = (f"Best substitution score {best:.2f} ({best_sub}) < 0.95. "
                    "The wall is irreducible. Derive new mathematics.")
        return {"wall_location": wall_params,
                "substitution_scores": scores,
                "best_substitution": best_sub,
                "verdict": verdict,
                "note": note}

    def full_cartography_report(self, grid_density=20):
        walls = self.scan_for_singularities(grid_density)
        if not walls:
            return {"verdict": "NO_WALL_DETECTED",
                    "note": "Math is smooth in the scanned region.",
                    "n_walls": 0}
        wp = {self.names[0]: walls[0][0]}
        if len(self.names) > 1:
            wp[self.names[1]] = walls[0][1]
        for name in self.names[2:]:
            wp[name] = sum(self.ranges[name]) / 2
        report = self.probe_with_substitutions(wp)
        report["n_walls"] = len(walls)
        report["wall_fraction"] = len(walls) / grid_density**2
        return report


if __name__ == "__main__":
    print("SINGULARITY CARTOGRAPHER DEMO")
    print("Mapping the playground wall: 1 + alpha*phi^2 = 0 pole\n")

    def potential(params):
        alpha = params.get('alpha', 0.0)
        lam = params.get('lambda', 1.0)
        phi_sq = lam**2
        return 1.0 / (1.0 + alpha * phi_sq)

    ranges = {'alpha': (-1.5, 0.5), 'lambda': (0.8, 2.0), 'beta': (0.0, 0.5)}
    cart = SingularityCartographer(ranges, potential,
                                   param_names=['alpha', 'lambda', 'beta'],
                                   blowup=30.0)
    report = cart.full_cartography_report(grid_density=25)
    print("=" * 60)
    for k, v in report.items():
        print(f"{k}: {v}")
