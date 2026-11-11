"""Ports of the delivered run 6, 7, 8 code to the standard library.

Source: forest-model-ledger/runs/run_6.py, run_7.py, run_8.py (filed verbatim
2026-11-11). Each function below follows its source statement for statement;
the comments name the source lines' expressions. Random draws come from
playground/numpy_stream.py in the same order numpy makes them.

Differences from the source, all of them:
  arrays      numpy arrays -> lists; matrix products and sums are plain loops
              (np_sum copies numpy's pairwise order for 8 or more terms)
  root        scipy brentq -> bisection (ode_fraction)
  exp         numpy exp -> math.exp (run 6 structure only)
Targets and tolerances: PREREG_ORIGINALS.md. Checked against
fixtures/originals_expected.json by tests/test_originals.py.
"""
import math, os, sys
from collections import deque

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from playground import numpy_stream as ns


def np_sum(v):
    """numpy add.reduce order for a 1-d float array of up to 128 terms."""
    n = len(v)
    if n < 8:
        s = 0.0
        for x in v:
            s += x
        return s
    if n > 128:
        raise ValueError("np_sum: more than 128 terms is not copied here")
    r = list(v[:8])
    i = 8
    while i < n - (n % 8):
        for j in range(8):
            r[j] += v[i + j]
        i += 8
    s = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]))
    while i < n:
        s += v[i]
        i += 1
    return s


def np_mean_std(v):
    n = len(v)
    m = np_sum(v) / n
    return m, math.sqrt(np_sum([(x - m) * (x - m) for x in v]) / n)


def ode_fraction(dens, p):
    """run 7 ode_burn / run 8 ode: root of z = 1 - exp(-R0 z) on [1e-9, 1], R0 = 4 p dens."""
    R0 = 4 * p * dens
    if R0 <= 1:
        return 0.0
    f = lambda z: z - (1 - math.exp(-R0 * z))
    lo, hi = 1e-9, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


NEIGH = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _veg(rng, L, dens):
    return [[rng.random() < dens for _ in range(L)] for _ in range(L)]


def run7_grid_burn(rng, dens, p, L=120, reps=12, keep=None):
    out = []
    for _ in range(reps):
        veg = _veg(rng, L, dens)
        c = L // 2
        veg[c][c] = True
        burned = [[False] * L for _ in range(L)]
        burned[c][c] = True
        nb, q = 1, deque([(c, c)])
        while q:
            i, j = q.popleft()
            for di, dj in NEIGH:
                a, b = i + di, j + dj
                if 0 <= a < L and 0 <= b < L and veg[a][b] and not burned[a][b] and rng.random() < p:
                    burned[a][b] = True
                    nb += 1
                    q.append((a, b))
        out.append(nb / max(sum(map(sum, veg)), 1))
    if keep is not None:
        keep.extend(out)
    return np_mean_std(out)


def run7(seed=3, L=120, reps=12):
    rng, rows = ns.default_rng(seed), []
    for k in range(11):
        dr = 1.0 if k == 10 else k * (1.0 / 10)          # np.linspace(0, 1, 11)
        p = 0.2 + 0.75 * dr
        g, s = run7_grid_burn(rng, 0.8, p, L, reps)
        rows.append(dict(drought=dr, p=p, R0=4 * p * 0.8, ode=ode_fraction(0.8, p), grid_mean=g, grid_sd=s))
    return rows


def run8_burn(rng, dens, p, spot, L=100, reps=10, keep=None):
    res = []
    for _ in range(reps):
        veg = _veg(rng, L, dens)
        c = L // 2
        veg[c][c] = True
        b = [[False] * L for _ in range(L)]
        b[c][c] = True
        nb, q = 1, deque([(c, c)])
        while q:
            i, j = q.popleft()
            for _k in range(4):
                if rng.random() < spot:
                    a = rng.integers(L)
                    bb = rng.integers(L)
                else:
                    di, dj = NEIGH[_k]
                    a, bb = i + di, j + dj
                if 0 <= a < L and 0 <= bb < L and veg[a][bb] and not b[a][bb] and rng.random() < p:
                    b[a][bb] = True
                    nb += 1
                    q.append((a, bb))
        res.append(nb / sum(map(sum, veg)))
    if keep is not None:
        keep.extend(res)
    return np_mean_std(res)


RUN8_DROUGHTS, RUN8_SPOTS = (0.2, 0.4, 0.5, 0.6, 0.7), (0, 0.05, 0.2, 1.0)


def run8(seed=4, L=100, reps=10, droughts=RUN8_DROUGHTS, spots=RUN8_SPOTS):
    rng, rows = ns.default_rng(seed), []
    for dr in droughts:
        p = 0.2 + 0.75 * dr
        cells = []
        for s in spots:
            m, sd = run8_burn(rng, 0.8, p, s, L, reps)
            cells.append(dict(spot=s, mean=m, sd=sd))
        rows.append(dict(drought=dr, ode=ode_fraction(0.8, p), cells=cells))
    return rows


# ---------------------------------------------------------------- run 6
nP, nF = 8, 4
TREE = [i < 5 for i in range(nP)]
DT, T_END = 0.05, 3000
STEPS = int(T_END / DT)


def run6_structure(seed=2):
    r0 = ns.default_rng(seed)
    u = [[r0.random() for _ in range(nP)] for _ in range(nP)]                 # r0.uniform(0,1,(nP,nP))
    trait = [[0.0 if i == j else (u[i][j] + u[j][i]) / 2 for j in range(nP)] for i in range(nP)]
    a1 = [[r0.random() for _ in range(nF)] for _ in range(nP)]                # r0.uniform(0,1,(nP,nF))
    a2 = [[r0.random() < 0.7 for _ in range(nF)] for _ in range(nP)]          # r0.random((nP,nF)) < 0.7
    aff = [[a1[i][j] * a2[i][j] for j in range(nF)] for i in range(nP)]
    niche = [r0.random() for _ in range(nF)]                                  # r0.uniform(0,1,nF)
    return trait, aff, niche


def _dot(u, v):
    s = 0.0
    for x, y in zip(u, v):
        s += x * y
    return s


def run6_old(struct=None):
    """old(): the run-4 equations audited as an N budget (source header's wording)."""
    trait, aff, niche = struct or run6_structure()
    dt, comp = DT, 0.1
    N, F = [0.3] * nP, [0.2] * nF
    Bac = WR = 0.2
    Lf = Ls = 0.3
    R = 0.5
    a = [[-1.0 if i == j else -comp * math.exp(-2 * trait[i][j]) - 0.1 * comp for j in range(nP)] for i in range(nP)]
    d = [[0.0] * nF for _ in range(nF)]
    for i in range(nF):
        for j in range(nF):
            nd = abs(niche[i] - niche[j])
            d[i][j] = -1.0 if i == j else (0.5 if nd > 0.4 else -0.3 * (1 - nd))
    mort = [0.03 if t else 0.12 for t in TREE]
    affT04 = [[aff[i][j] * 0.4 for i in range(nP)] for j in range(nF)]
    ext_in = ext_out = 0
    tot0 = np_sum(N) + np_sum(F) + Bac + WR + Lf + Ls + R
    mis = []
    for k in range(STEPS):
        up = R / (0.5 + R)
        fF = [f / (1 + f) for f in F]
        ben = [_dot(aff[i], fF) for i in range(nP)]
        gN = [0.6 * up + ben[i] * up for i in range(nP)]
        dN = [N[i] * (gN[i] + _dot(a[i], N) - mort[i]) for i in range(nP)]
        sN = np_sum(N)
        cF = [_dot(affT04[j], N) / (1 + sN) for j in range(nF)]
        dF = [F[j] * (cF[j] + _dot(d[j], F) - 0.05) + 0.001 for j in range(nF)]
        decf = 0.8 * Bac * Lf / (0.5 + Lf)
        decs = 0.08 * WR * Ls / (1 + Ls)
        sF = np_sum(F)
        dBac = Bac * (0.4 * Lf / (0.5 + Lf) - 0.15) + 0.001
        dWR = WR * (0.3 * Ls / (1 + Ls) - 0.03 - 0.02 * sF) + 0.001
        lit = [mort[i] * N[i] for i in range(nP)]
        dLf = np_sum(lit[5:]) + 0.05 * sF - decf
        dLs = np_sum(lit[:5]) - decs
        dR = 0.02 + decf + decs - 0.3 * _dot(gN, N) - 0.05 * R
        ext_in += 0.02 * dt
        ext_out += 0.05 * R * dt
        N = [N[i] + dt * dN[i] for i in range(nP)]
        F = [F[j] + dt * dF[j] for j in range(nF)]
        Bac += dt * dBac
        WR += dt * dWR
        Lf += dt * dLf
        Ls += dt * dLs
        R += dt * dR
        if k % 2000 == 0:
            tot = np_sum(N) + np_sum(F) + Bac + WR + Lf + Ls + R
            mis.append(tot - (tot0 + ext_in - ext_out))
    return mis


def run6_conserved(fire_thr=0.6, seed=0, struct=None):
    """conserved(): returns dict(mis, fires, B) with B rows (t, sum N, sum tree N, Ls, R) every 200 steps."""
    trait, aff, niche = struct or run6_structure()
    rng = ns.default_rng(seed)
    dt, comp = DT, 0.1
    a = [[0.0 if i == j else -comp * math.exp(-2 * trait[i][j]) - 0.1 * comp for j in range(nP)] for i in range(nP)]
    N, F = [0.3] * nP, [0.2] * nF
    Bac = WR = 0.2
    Lf = Ls = 0.3
    R = 0.5
    mort = [0.03 if t else 0.12 for t in TREE]
    tot0 = np_sum(N) + np_sum(F) + Bac + WR + Lf + Ls + R
    dep = fix = leach = volat = 0.0
    mis, fires, B = [], 0, []
    affT = [[aff[i][j] for i in range(nP)] for j in range(nF)]
    for k in range(STEPS):
        upR = R / (0.5 + R)
        u_direct = [0.3 * upR * n for n in N]
        fung_up = [0.3 * upR * f for f in F]
        share = [[aff[i][j] * N[i] for j in range(nF)] for i in range(nP)]
        for j in range(nF):
            cs = 0.0
            for i in range(nP):
                cs += share[i][j]
            cs += 1e-9
            for i in range(nP):
                share[i][j] /= cs
        f_to_p = [0.4 * F[j] * (1.0 if _dot(N, affT[j]) > 0 else 0.0) for j in range(nF)]
        to_plants = [_dot(share[i], f_to_p) for i in range(nP)]
        crowd = [-(_dot(a[i], N)) * N[i] * 0.5 + 0.5 * N[i] ** 2 for i in range(nP)]
        mN = [mort[i] * N[i] + crowd[i] for i in range(nP)]
        mF = [0.05 * f + 0.3 * f ** 2 for f in F]
        decf = 0.8 * Bac * Lf / (0.5 + Lf)
        decs = 0.08 * WR * Ls / (1 + Ls)
        gB, gW = 0.3 * decf, 0.3 * decs
        mB, mW = 0.15 * Bac, 0.03 * WR
        dN = [u_direct[i] + to_plants[i] - mN[i] for i in range(nP)]
        dF = [fung_up[j] - f_to_p[j] - mF[j] for j in range(nF)]
        dBac, dWR = gB - mB, gW - mW
        dLf = np_sum(mN[5:]) + np_sum(mF) + mB + mW - decf
        dLs = np_sum(mN[:5]) - decs
        dR = (decf - gB) + (decs - gW) - np_sum(u_direct) - np_sum(fung_up) + 0.02 + 0.01 - 0.05 * R
        dep += 0.02 * dt
        fix += 0.01 * dt
        leach += 0.05 * R * dt
        N = [N[i] + dt * dN[i] for i in range(nP)]
        F = [F[j] + dt * dF[j] for j in range(nF)]
        Bac += dt * dBac
        WR += dt * dWR
        Lf += dt * dLf
        Ls += dt * dLs
        R += dt * dR
        h = 0.02 * max(Ls + 0.5 * Lf - fire_thr, 0) ** 2
        if rng.random() < h * dt:
            fires += 1
            burn = 0.9 * Ls + 0.9 * Lf + 0.7 * np_sum(N[:5]) + 0.3 * np_sum(N[5:]) + 0.4 * np_sum(F)
            volat += 0.5 * burn
            R += 0.5 * burn
            Ls *= 0.1
            Lf *= 0.1
            N = [N[i] * 0.3 if TREE[i] else N[i] * 0.7 for i in range(nP)]
            F = [f * 0.6 for f in F]
        if k % 2000 == 0:
            tot = np_sum(N) + np_sum(F) + Bac + WR + Lf + Ls + R
            mis.append(tot - (tot0 + dep + fix - leach - volat))
        if k % 200 == 0:
            B.append((k * dt, np_sum(N), np_sum(N[:5]), Ls, R))
    return dict(mis=mis, fires=fires, B=B, boundary=dict(dep=dep, fix=fix, leach=leach, volat=volat))


def run6_stats(B):
    late = [r for r in B if r[0] > 1000]
    tot = [r[1] for r in late]
    return dict(B_mean=math.fsum(tot) / len(tot), swing=max(tot) - min(tot),
                tree_share=math.fsum(r[2] / r[1] for r in late) / len(late),
                Ls_min=min(r[3] for r in late), Ls_max=max(r[3] for r in late), last_row=list(B[-1]))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("originals.py has no selftest; run: python3 selftest_originals.py")
        sys.exit(2)
    print("ports of forest-model-ledger runs 6, 7, 8; driven by run.py part 3")
