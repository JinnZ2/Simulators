"""Base model: mass-conserving forest N + water system (rebuild of run 6).

Every continuous transfer is a row in a FLUX TABLE (name, source, sink, rate).
The derivative is assembled only from that table, so pool sums close by
construction for anything routed through it. The L0 audit (model/l0_audit.py)
compares pool change against accumulated boundary flux; a code path that moves
mass OUTSIDE the table shows up there as misclosure. `leak` plants exactly
such a path, for testing the audit -- it is not a reconstruction of the
original pre-run-6 model, whose code is not in this tree.

Units: N pools in arbitrary "N units", water in "W units", time in years.
Parameters are hand-set, not fitted to anything.
numpy only (scipy unavailable in the build environment): fixed-step RK4.
"""
import numpy as np

N_POOLS = ["S", "T", "G", "F", "Lt", "Lg"]   # soil mineral, trees, grasses, fungi, tree litter, fast litter
W_POOLS = ["W"]
# boundary accumulators. Terms carried at zero are VOID (not modelled), kept so
# the boundary audit line always prints them.
N_BOUND_IN = ["deposition", "fixation", "dust", "animal_in"]
N_BOUND_OUT = ["leaching", "fire_volatilisation", "groundwater_n", "animal_out"]
W_BOUND_IN = ["precipitation"]
W_BOUND_OUT = ["evapotranspiration", "drainage"]
VOID_TERMS = ["fixation", "dust", "animal_in", "groundwater_n", "animal_out"]

NAMES = N_POOLS + W_POOLS + N_BOUND_IN + N_BOUND_OUT + W_BOUND_IN + W_BOUND_OUT
IX = {n: i for i, n in enumerate(NAMES)}

DEFAULTS = dict(
    dep=1.0,                 # N deposition, N units / yr
    uT=1.2, uG=3.0,          # max specific uptake, 1/yr
    K=2.0,                   # half-saturation soil N
    b=1.5, Kf=1.0,           # fungal benefit multiplier and its half-saturation
    KT=60.0, KG=12.0,        # light ceilings (N-equivalent standing stock)
    aG=0.2, aT=0.25,         # competition: grass on tree, tree on grass
    c=0.08,                  # tree -> fungus payment, 1/yr
    mT=0.04, mG=0.9, mF=1.5, # turnover, 1/yr
    kT=0.25, kG=2.0,         # litter decomposition, 1/yr at full moisture
    leach=0.05,              # leaching coefficient
    P0=1.0, season=0.6,      # precipitation mean and seasonal amplitude
    et=0.02, drain=0.8,      # water losses
    Wh=0.5,                  # moisture half-saturation for biology
    drought_sd=0.35,         # lognormal sd of annual precipitation factor
    drought=0.0,             # mean precipitation reduction, 0..1
    # fire (discrete events, checked every step)
    fuel_th=6.0, W_dry=0.55, p_ign=4.0,   # ignition hazard per yr once fuel AND dryness thresholds are met
    burn=0.8, vol=0.6,       # litter fraction burned; burned N fraction volatilised
    kill_G=0.7, kill_T=0.03,
    leak=0.0,                # PLANTED defect: fraction of the fungal payment that vanishes
)
INIT = dict(S=3.0, T=10.0, G=3.0, F=0.5, Lt=2.0, Lg=0.5, W=1.0)


def flux_table(y, t, p, pfac):
    """Rows: (name, source, sink, rate/yr). 'source' None = from outside the system."""
    S, T, G, F, Lt, Lg, W = (max(y[IX[k]], 0.0) for k in N_POOLS + W_POOLS)
    m = W / (W + p["Wh"])
    sat = S / (S + p["K"])
    fb = 1.0 + p["b"] * F / (F + p["Kf"])
    precip = p["P0"] * (1 - p["drought"]) * pfac * (1 + p["season"] * np.sin(2 * np.pi * t))
    return [
        ("deposition", None, "S", p["dep"]),
        ("uptake_T", "S", "T", p["uT"] * T * sat * fb * max(0.0, 1 - (T + p["aG"] * G) / p["KT"]) * m),
        ("uptake_G", "S", "G", p["uG"] * G * sat * max(0.0, 1 - (G + p["aT"] * T) / p["KG"]) * m),
        ("payment", "T", "F", p["c"] * T * F / (F + p["Kf"])),
        ("mort_T", "T", "Lt", p["mT"] * T),
        ("mort_G", "G", "Lg", p["mG"] * G),
        ("mort_F", "F", "Lg", p["mF"] * F),
        ("decomp_Lt", "Lt", "S", p["kT"] * Lt * m),
        ("decomp_Lg", "Lg", "S", p["kG"] * Lg * m),
        ("leaching", "S", None, p["leach"] * S * W),
        ("precipitation", None, "W", precip),
        ("evapotranspiration", "W", None, p["et"] * (T + G) * W),
        ("drainage", "W", None, p["drain"] * W),
    ]


def deriv(y, t, p, pfac):
    d = np.zeros(len(NAMES))
    for name, src, dst, r in flux_table(y, t, p, pfac):
        if src is not None:
            d[IX[src]] -= r
        else:
            d[IX[name]] += r          # boundary-in accumulator
        if dst is not None:
            d[IX[dst]] += r
        else:
            d[IX[name]] += r          # boundary-out accumulator
        if name == "payment" and p["leak"]:
            d[IX["F"]] -= p["leak"] * r   # PLANTED: mass leaves F with no ledger row
    return d


def fire(y, p):
    """Discrete event with explicit bookkeeping. Returns N volatilised."""
    out = 0.0
    for k in ("Lt", "Lg"):
        b = p["burn"] * y[IX[k]]
        y[IX[k]] -= b
        out += p["vol"] * b
        y[IX["S"]] += (1 - p["vol"]) * b
    kg = p["kill_G"] * y[IX["G"]]
    y[IX["G"]] -= kg
    out += p["vol"] * kg
    y[IX["S"]] += (1 - p["vol"]) * kg
    kt = p["kill_T"] * y[IX["T"]]
    y[IX["T"]] -= kt
    y[IX["Lt"]] += kt
    y[IX["fire_volatilisation"]] += out
    return out


def simulate(years=300, dt=1.0 / 52, seed=0, params=None, init=None, fires=True):
    p = dict(DEFAULTS)
    p.update(params or {})
    rng = np.random.default_rng(seed)
    pfacs = rng.lognormal(-0.5 * p["drought_sd"] ** 2, p["drought_sd"], size=years)
    y = np.zeros(len(NAMES))
    for k, v in {**INIT, **(init or {})}.items():
        y[IX[k]] = v
    y0 = y.copy()
    n = int(round(years / dt))
    traj = np.empty((n + 1, len(NAMES)))
    traj[0] = y
    events = []
    for i in range(n):
        t = i * dt
        pf = pfacs[min(int(t), years - 1)]
        k1 = deriv(y, t, p, pf)
        k2 = deriv(y + 0.5 * dt * k1, t + 0.5 * dt, p, pf)
        k3 = deriv(y + 0.5 * dt * k2, t + 0.5 * dt, p, pf)
        k4 = deriv(y + dt * k3, t + dt, p, pf)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if fires:
            fuel = y[IX["Lt"]] + y[IX["Lg"]]
            if fuel > p["fuel_th"] and y[IX["W"]] < p["W_dry"] and rng.random() < p["p_ign"] * dt:
                events.append((t + dt, fuel, fire(y, p)))
        traj[i + 1] = y
    return dict(t=np.arange(n + 1) * dt, traj=traj, y0=y0, y=y, events=events, params=p, seed=seed, dt=dt, years=years)
