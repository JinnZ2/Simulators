#!/usr/bin/env python3
"""
rg_flow_lens.py -- F4 lens: fixed points and moving walls.  numpy + scipy.

F4 called out that the singularity classifier fixed the wall
1 + alpha * phi_hat^2 = 0 at the attractor value phi_hat ~ lambda,
producing "alpha ~ -1/lambda^2".  But phi_hat is a dynamical field,
not a static coupling.  It flows.  So the wall flows.

The RG language:  the autonomous system (x, y) at Omega_r = 0 has
fixed points.  Cosmologists usually call these "attractor solutions"
but the machinery is textbook RG:  find fixed points, linearize,
classify by Jacobian eigenvalues, then track how observables
transform along the flow.

The lens:  for a given (lambda, beta), find the fixed points of
    x' = -3x + sqrt(3/2) lam y^2
         + 1.5 x (1 + x^2 - y^2) - sqrt(3/2) beta (1 - x^2 - y^2)
    y' = -sqrt(3/2) lam x y + 1.5 y (1 + x^2 - y^2)
and classify each by the Jacobian eigenvalues.  For the F4 wall,
integrate the flow forward from a physical initial condition and
report phi_hat(N) = phi_hat_i + sqrt(6) * integral x dN, so the
apparent wall alpha_wall(N) = -1 / phi_hat(N)^2 can be plotted as
a trajectory in (N, alpha) space rather than a static line.

If the wall crosses the report's fixed value at exactly one epoch,
the static classifier read a snapshot of a moving boundary.

names_no: [intent, verdict].  Reports numbers and shape; the F4
correction is that the alpha-wall is a trajectory, not a coupling.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve


SQ32 = np.sqrt(1.5)


# --- dynamical system (Omega_r = 0, post-radiation) ------------------------

def _rhs(x, y, lam, beta):
    Om = 1.0 - x * x - y * y
    xp = (-3.0 * x + SQ32 * lam * y * y
          + 1.5 * x * (1.0 + x * x - y * y)
          - SQ32 * beta * Om)
    yp = -SQ32 * lam * x * y + 1.5 * y * (1.0 + x * x - y * y)
    return np.array([xp, yp])


def _jacobian(x, y, lam, beta, h=1e-6):
    """Numerical Jacobian; small enough for classification only."""
    fx = (_rhs(x + h, y, lam, beta) - _rhs(x - h, y, lam, beta)) / (2 * h)
    fy = (_rhs(x, y + h, lam, beta) - _rhs(x, y - h, lam, beta)) / (2 * h)
    return np.array([[fx[0], fy[0]], [fx[1], fy[1]]])


def _classify(J):
    ev = np.linalg.eigvals(J)
    re = ev.real
    if np.all(re < -1e-8):
        return "ATTRACTOR"
    if np.all(re > 1e-8):
        return "REPELLER"
    if np.any(re > 1e-8) and np.any(re < -1e-8):
        return "SADDLE"
    return "MARGINAL"


# --- fixed points ----------------------------------------------------------

def fixed_points(lam, beta, seeds=None):
    """
    Find fixed points of the (x, y) system by seeded root-finding.
    Standard seeds cover: trivial, kinetic, field-dominated, scaling.
    """
    if seeds is None:
        seeds = [(0.0, 0.0), (0.9, 0.1), (-0.9, 0.1),
                 (lam / np.sqrt(6.0), np.sqrt(max(1.0 - lam * lam / 6.0, 1e-3))),
                 (SQ32 / max(lam, 0.5), SQ32 / max(lam, 0.5))]
    found, seen = [], []
    for s in seeds:
        try:
            r = fsolve(lambda v: _rhs(v[0], v[1], lam, beta), s,
                       full_output=True, xtol=1e-10)
            xy, info, ier, _ = r
            if ier != 1:
                continue
            x, y = float(xy[0]), float(xy[1])
            if y < 0 or (x * x + y * y) > 1.001:
                continue                # physical region: Om_phi <= 1, y > 0
            if any(abs(x - a) + abs(y - b) < 1e-4 for a, b in seen):
                continue
            seen.append((x, y))
            J = _jacobian(x, y, lam, beta)
            found.append({"x": x, "y": y,
                          "Om_phi": x * x + y * y,
                          "w_phi": (x * x - y * y) / (x * x + y * y + 1e-30),
                          "eigenvalues": [complex(e) for e in np.linalg.eigvals(J)],
                          "class": _classify(J)})
        except Exception:
            continue
    return found


# --- flow: phi_hat(N) and the moving wall ---------------------------------

def flow(lam, beta, x0=1e-6, y0=1e-3, phi_hat_i=1e-3, N_i=-6.0, N_f=0.0, n=61):
    """
    Integrate (x, y) forward from a small-field initial condition and
    accumulate phi_hat(N).  Returns N, x(N), y(N), phi_hat(N), and the
    apparent wall alpha_wall(N) = -1 / phi_hat(N)^2.
    """
    def rhs(N, s):
        x, y, phi = s
        d = _rhs(x, y, lam, beta)
        return [d[0], d[1], np.sqrt(6.0) * x]
    sol = solve_ivp(rhs, (N_i, N_f), [x0, y0, phi_hat_i],
                    dense_output=True, rtol=1e-9, atol=1e-12)
    N = np.linspace(N_i, N_f, n)
    S = sol.sol(N)
    x, y, phi = S[0], S[1], S[2]
    alpha_wall = -1.0 / np.maximum(phi * phi, 1e-30)
    return {"N": N, "x": x, "y": y, "phi_hat": phi, "alpha_wall": alpha_wall}


# --- self-test -------------------------------------------------------------

def _t_field_dominated_attractor_exists_for_shallow_potential():
    fps = fixed_points(lam=1.0, beta=0.0)
    fda = [p for p in fps if p["y"] > 0.5]
    assert fda, "expected a field-dominated fixed point at lam=1.0"
    assert any(p["class"] == "ATTRACTOR" for p in fda), (
        f"expected attractor: {fda}")


def _t_no_field_attractor_for_steep_potential():
    # lam^2 > 6 makes the field-dominated FP no longer physical (y^2 < 0)
    fps = fixed_points(lam=3.0, beta=0.0)
    assert not any(p["y"] > 0.5 and p["class"] == "ATTRACTOR" for p in fps)


def _t_phi_hat_grows_monotonically_along_flow():
    tr = flow(lam=1.0, beta=0.0)
    assert np.all(np.diff(tr["phi_hat"]) >= -1e-9), "phi_hat must not decrease"
    assert tr["phi_hat"][-1] > 10 * tr["phi_hat"][0]


def _t_alpha_wall_moves():
    # F4's claim: the wall alpha = -1/phi_hat^2 is not a static value
    tr = flow(lam=1.0, beta=0.0)
    a0, a1 = tr["alpha_wall"][0], tr["alpha_wall"][-1]
    # both negative; |a0| >> |a1| because phi_hat starts small and grows
    assert a0 < 0 and a1 < 0
    assert abs(a0) > 100 * abs(a1), (a0, a1)


def _run():
    for name, fn in sorted(globals().items()):
        if name.startswith("_t_"):
            fn(); print("ok", name)
    print("all pass\n")


def _demo():
    print("--- Fixed points of the (x, y) system at lambda=1.10, beta=0 ---")
    fps = fixed_points(lam=1.10, beta=0.0)
    print(f"{'x':>9}{'y':>9}{'Om_phi':>10}{'w_phi':>9}"
          f"{'class':>13}{'eigenvalues':>28}")
    for p in fps:
        ev = ", ".join(f"{e:+.2f}" for e in p["eigenvalues"])
        print(f"{p['x']:>9.3f}{p['y']:>9.3f}{p['Om_phi']:>10.3f}"
              f"{p['w_phi']:>9.3f}{p['class']:>13}   {ev}")
    print()
    print("--- F4 wall alpha_wall(N) = -1/phi_hat(N)^2 along the flow ---")
    tr = flow(lam=1.10, beta=0.0)
    print(f"{'N':>7}{'phi_hat':>10}{'alpha_wall':>13}")
    for i in [0, 15, 30, 45, 60]:
        print(f"{tr['N'][i]:>7.2f}{tr['phi_hat'][i]:>10.4f}"
              f"{tr['alpha_wall'][i]:>13.4g}")
    print()
    a_span = abs(tr["alpha_wall"][0]) / abs(tr["alpha_wall"][-1])
    print(f"alpha_wall spans {a_span:.1e} between N={tr['N'][0]:+.1f} "
          f"and N={tr['N'][-1]:+.1f}.")
    print("Report classifier fixed this wall at alpha = -1/lambda^2 = "
          f"{-1/1.10**2:.3f}.")
    # find where alpha_wall crosses -1/lam^2
    target = -1.0 / (1.10 ** 2)
    for i in range(1, len(tr["N"])):
        if tr["alpha_wall"][i - 1] < target <= tr["alpha_wall"][i] \
                or tr["alpha_wall"][i] < target <= tr["alpha_wall"][i - 1]:
            print(f"  -> the trajectory crosses alpha = {target:.3f} at "
                  f"N ~ {tr['N'][i]:+.2f} (phi_hat ~ {tr['phi_hat'][i]:.3f}).")
            print("     Fixing this ONE epoch as if it were a coupling is the")
            print("     F4 error: the wall is a trajectory, not a constant.")
            break
    else:
        print("  -> trajectory never reaches the report's static value in "
              "this window; F4 stands more strongly.")


if __name__ == "__main__":
    _run(); _demo()
