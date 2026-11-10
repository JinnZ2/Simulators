"""Minimal bend-growth + cutoff toy with a mass-conserving sediment ledger. stdlib only.

PROPOSED form, not verified against Ikeda, Parker & Sawai (1981): the kinematic
upstream-weighted migration rule usually attributed to Howard & Knutson (1984) as a
reduction of that linear bend theory. Neither paper has been read in this tree
(egress allowlist); the form is written from the work order's naming and recall.

    M_i = Omega * R0_i + Gamma * sum_k R0_{i-k} G_k / sum_k G_k ,  G_k = exp(-alpha * k * ds)
    R0_i = E * W * C_i            (C = signed curvature, W = width)
    alpha = 2 * Cf / H            (H = depth, Cf = friction coefficient)

Nodes move along the outward normal by M_i * dt. A cutoff happens when two nodes
more than `cut_gap` nodes apart come within `neck * W`; the loop between them is
abandoned as an oxbow.

Units: lengths in units of the initial width W0 = 1; time in model steps. Nothing is
calibrated. Every parameter is in DEFAULTS and printed with each run.

L0 ledgers (closed every run by model/l0_audit.py, independent counters):
  sediment  d(active bed store) = inflow_load + bank_input - point_bar - oxbow_fill - outflow
  water     Q_in - Q_out (steady discharge; closes by construction)
  energy    rho g Q dZ_valley vs rho g Q S_channel L_channel (an identity in this model)
"""
import math, random

DEFAULTS = dict(
    W=1.0,                 # channel width
    aspect=20.0,           # W / H; depth H = W / aspect
    Cf=0.01,               # friction coefficient
    Omega=-1.0, Gamma=2.5, # Howard-Knutson weights (recalled, not checked)
    E=0.05,                # bank erodibility (the "bank strength" knob is 1/E)
    veg=0.0,               # vegetation 0..1: multiplies E by (1 - 0.7 veg); raises point-bar trap
    supply=1.0,            # inflow sediment load per step, as a multiple of capacity
    capacity=1.0,          # outflow transport capacity per step (bed-store units)
    porosity=0.4,
    L0=120.0,              # initial valley length
    ds=0.5,                # node spacing
    noise=0.05,            # initial lateral perturbation amplitude
    bank_noise=0.3,        # per-step relative scatter in erodibility along the bank (heterogeneity)
    jitter=0.002,          # per-step additive lateral displacement sd: the only source of NEW bends
    dt=0.4,
    steps=2500,
    neck=1.0,              # cutoff when two distant nodes come within neck * W
    cut_gap=12,            # minimum node separation along the channel for a cutoff
    S_valley=1e-3,         # valley slope (energy ledger only)
    Q=1.0,                 # discharge (water ledger only)
    leak=0.0,              # planted sediment leak per step (tests only)
)


def curvature(x, y):
    n = len(x)
    C = [0.0] * n
    for i in range(1, n - 1):
        ax, ay = x[i] - x[i - 1], y[i] - y[i - 1]
        bx, by = x[i + 1] - x[i], y[i + 1] - y[i]
        cross = ax * by - ay * bx
        la, lb = math.hypot(ax, ay), math.hypot(bx, by)
        lc = math.hypot(x[i + 1] - x[i - 1], y[i + 1] - y[i - 1])
        den = la * lb * lc
        C[i] = 2 * cross / den if den > 0 else 0.0
    # light smoothing: suppresses grid-scale noise, not physics
    S = C[:]
    for i in range(2, n - 2):
        S[i] = (C[i - 2] + 2 * C[i - 1] + 3 * C[i] + 2 * C[i + 1] + C[i + 2]) / 9.0
    return S


def resample(x, y, ds):
    out_x, out_y = [x[0]], [y[0]]
    carry = 0.0
    for i in range(1, len(x)):
        sx, sy = x[i - 1], y[i - 1]
        seg = math.hypot(x[i] - sx, y[i] - sy)
        t = ds - carry
        while t <= seg:
            f = t / seg
            out_x.append(sx + f * (x[i] - sx)); out_y.append(sy + f * (y[i] - sy))
            t += ds
        carry = seg - (t - ds)
    if math.hypot(x[-1] - out_x[-1], y[-1] - out_y[-1]) > 1e-9:
        out_x.append(x[-1]); out_y.append(y[-1])
    return out_x, out_y


def length(x, y):
    return sum(math.hypot(x[i] - x[i - 1], y[i] - y[i - 1]) for i in range(1, len(x)))


def find_cutoff(x, y, thresh, gap):
    cell = thresh
    grid = {}
    for i in range(len(x)):
        grid.setdefault((int(x[i] // cell), int(y[i] // cell)), []).append(i)
    best = None
    for i in range(len(x)):
        cx, cy = int(x[i] // cell), int(y[i] // cell)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for j in grid.get((cx + dx, cy + dy), ()):
                    if j - i > gap and math.hypot(x[j] - x[i], y[j] - y[i]) < thresh:
                        if best is None or (j - i) < (best[1] - best[0]):
                            best = (i, j)          # the tightest neck: the loop that closes first
    return best


def inflections(x, y, C):
    idx = [i for i in range(3, len(C) - 3) if C[i] * C[i + 1] < 0]
    return idx


def wavelength(x, y, C):
    """Leopold-style: twice the mean straight-line distance between successive inflections."""
    idx = inflections(x, y, C)
    if len(idx) < 3:
        return None
    d = [math.hypot(x[b] - x[a], y[b] - y[a]) for a, b in zip(idx, idx[1:])]
    return 2.0 * sum(d) / len(d)


def run(params=None, seed=0, record_every=50):
    p = dict(DEFAULTS, **(params or {}))
    rng = random.Random(seed)
    W, H = p["W"], p["W"] / p["aspect"]
    alpha = 2 * p["Cf"] / H
    E = p["E"] * (1 - 0.7 * p["veg"])
    trap = min(1.0, 0.9 + 0.1 * p["veg"])          # fraction of trailing-side area filled per step, supply permitting
    n0 = int(p["L0"] / p["ds"]) + 1
    x = [i * p["ds"] for i in range(n0)]
    y = [0.0 if i < 6 or i > n0 - 7 else rng.gauss(0, p["noise"]) for i in range(n0)]
    K = max(1, int(6.0 / (alpha * p["ds"])))         # window: G down to e^-6
    G = [math.exp(-alpha * k * p["ds"]) for k in range(K + 1)]
    sG = sum(G)
    vol = H * (1 - p["porosity"])                    # bed-store units per unit area swept
    led = dict(store=10.0 * p["capacity"] * 0 + 50.0, inflow=0.0, bank_input=0.0, point_bar=0.0,
               oxbow_fill=0.0, outflow=0.0, leak_hidden=0.0)
    store0 = led["store"]
    hist = []
    cutoffs = 0
    Lv = x[-1] - x[0]
    for step in range(p["steps"]):
        C = curvature(x, y)
        n = len(x)
        R0 = [E * W * c for c in C]
        M = [0.0] * n
        for i in range(n):
            acc = 0.0
            for k in range(min(K, i) + 1):
                acc += R0[i - k] * G[k]
            M[i] = p["Omega"] * R0[i] + p["Gamma"] * acc / sG
        # move along outward normal; ends pinned
        nx, ny = x[:], y[:]
        swept = 0.0
        for i in range(6, n - 6):
            tx, ty = x[i + 1] - x[i - 1], y[i + 1] - y[i - 1]
            tl = math.hypot(tx, ty) or 1.0
            ux, uy = -ty / tl, tx / tl                # left normal
            d = M[i] * p["dt"] * (1.0 + p["bank_noise"] * rng.gauss(0, 1)) + p["jitter"] * rng.gauss(0, 1)
            nx[i] = x[i] - ux * d
            ny[i] = y[i] - uy * d
            swept += abs(d) * p["ds"]
        x, y = resample(nx, ny, p["ds"])
        # sediment ledger: eroded leading bank enters the bed store; trailing side fills from it
        bank = swept * vol
        inflow = p["supply"] * p["capacity"]
        led["inflow"] += inflow
        led["bank_input"] += bank
        led["store"] += inflow + bank
        dep = min(trap * bank, led["store"])
        led["store"] -= dep
        led["point_bar"] += dep
        out = min(p["capacity"], led["store"])
        led["store"] -= out
        led["outflow"] += out
        if p["leak"]:
            lk = min(p["leak"], led["store"])
            led["store"] -= lk                          # removed, recorded in no flux counter
            led["leak_hidden"] += lk
        # cutoffs
        if True:
            cut = find_cutoff(x, y, p["neck"] * W, p["cut_gap"])
            while cut is not None:
                i, j = cut
                loop_len = length(x[i:j + 1], y[i:j + 1])
                fill = min(loop_len * W * vol * 0.5, led["store"])   # oxbow traps half its channel volume, supply permitting
                led["store"] -= fill
                led["oxbow_fill"] += fill
                x = x[:i + 1] + x[j:]
                y = y[:i + 1] + y[j:]
                cutoffs += 1
                x, y = resample(x, y, p["ds"])
                cut = find_cutoff(x, y, p["neck"] * W, p["cut_gap"])
        if step % record_every == 0 or step == p["steps"] - 1:
            Cn = curvature(x, y)
            Lc = length(x, y)
            lam = wavelength(x, y, Cn)
            hist.append(dict(step=step, sinuosity=Lc / Lv, lam_W=(lam / W if lam else None), cutoffs=cutoffs,
                             nodes=len(x)))
    Lc = length(x, y)
    dZ = p["S_valley"] * Lv
    energy = dict(source=p["Q"] * dZ, dissipation=p["Q"] * (dZ / Lc) * Lc)   # rho g omitted (common factor)
    water = dict(Q_in=p["Q"], Q_out=p["Q"])
    return dict(params=p, seed=seed, history=hist, ledger=led, store0=store0, x=x, y=y,
                energy=energy, water=water, H=H, alpha=alpha, K=K,
                channel_length=Lc, valley_length=Lv, cutoffs=cutoffs)
