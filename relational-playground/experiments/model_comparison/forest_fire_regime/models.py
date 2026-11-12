"""Two experiment-local models, registered through the same interface as the families.

forest_n       port of forest-model-ledger/model/base.py (N + water, fire as a discrete
               event). Same flux table, row for row; same RK4; stdlib arithmetic.
ode_meanfield  mean field of the grid fire rules (see PREREG.md).
"""
import math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from playground.equations.base import ModelOutput, from_transfers, register as register_model, REGISTRY
from playground import known_answer_gate as gate

N_POOLS = ("S", "T", "G", "F", "Lt", "Lg")
POOLS = N_POOLS + ("W",)
# forest-model-ledger/model/base.py DEFAULTS and INIT, transcribed; tests compare them when that file is present
DEFAULTS = dict(dep=1.0, uT=1.2, uG=3.0, K=2.0, b=1.5, Kf=1.0, KT=60.0, KG=12.0, aG=0.2, aT=0.25, c=0.08,
                mT=0.04, mG=0.9, mF=1.5, kT=0.25, kG=2.0, leach=0.05, P0=1.0, season=0.6, et=0.02, drain=0.8,
                Wh=0.5, drought_sd=0.35, drought=0.0, fuel_th=6.0, W_dry=0.55, p_ign=4.0, burn=0.8, vol=0.6,
                kill_G=0.7, kill_T=0.03, leak=0.0, fires=1)
INIT = dict(S=3.0, T=10.0, G=3.0, F=0.5, Lt=2.0, Lg=0.5, W=1.0)


def forest_n(state, env, rel, ctl, p):
    S, T, G, F, Lt, Lg, W = (max(state[k], 0.0) for k in POOLS)
    pfacs = env["pfacs"]
    pf = pfacs[min(int(env["t_step"]), len(pfacs) - 1)]
    t = env["t"]
    m = W / (W + p["Wh"])
    sat = S / (S + p["K"])
    fb = 1.0 + p["b"] * F / (F + p["Kf"])
    precip = p["P0"] * (1 - p["drought"]) * pf * (1 + p["season"] * math.sin(2 * math.pi * t))
    tr = [
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
    d = from_transfers(tr, POOLS)
    if p["leak"]:
        d["F"] -= p["leak"] * tr[3][3]            # PLANTED: mass leaves F with no ledger row
    return ModelOutput(d, transfers=tr, uncertainty="hand-set parameters; one well-mixed stand; N and water only")


def fire(state, env, p):
    if not p["fires"]:
        return None
    fuel = state["Lt"] + state["Lg"]
    if not (fuel > p["fuel_th"] and state["W"] < p["W_dry"] and env["rng"].random() < p["p_ign"] * env["dt"]):
        return None
    tr = []
    for k in ("Lt", "Lg"):
        b = p["burn"] * state[k]
        tr += [("fire_volatilisation", k, None, p["vol"] * b), ("fire_ash_" + k, k, "S", (1 - p["vol"]) * b)]
    kg = p["kill_G"] * state["G"]
    tr += [("fire_volatilisation", "G", None, p["vol"] * kg), ("fire_ash_G", "G", "S", (1 - p["vol"]) * kg)]
    tr.append(("fire_kill_T", "T", "Lt", p["kill_T"] * state["T"]))
    return tr


def ode_meanfield(state, env, rel, ctl, p):
    u, b = max(state["unburned"], 0.0), max(state["burning"], 0.0)
    tr = [("ignite", "unburned", "burning", p["beta"] * u * b), ("burn_out", "burning", "burned", b)]
    return ModelOutput(from_transfers(tr, ("unburned", "burning", "burned", "bare")), transfers=tr,
                       uncertainty="every burning cell reaches every unburned cell equally: no space")


def final_size(u0, b0, beta):
    """u at the end: the root below min(u0, 1/beta) of ln(u/u0) + beta (u0 + b0 - u) = 0."""
    f = lambda u: math.log(u / u0) + beta * (u0 + b0 - u)
    lo, hi = 1e-300, min(u0, 1.0 / beta)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def _u(rng, lo, hi):
    return lo + (hi - lo) * rng.random()


def _forest_case(rng):
    p = dict(DEFAULTS, season=0.0, fires=0)
    p["dep"], p["leach"], p["P0"], p["drain"] = _u(rng, 0.5, 2.0), _u(rng, 0.02, 0.2), _u(rng, 0.5, 1.5), _u(rng, 0.4, 1.2)
    ws, T_end = p["P0"] / p["drain"], 5.0
    base = dict(S=0.0, T=0.0, G=0.0, F=0.0, Lt=0.0, Lg=0.0, W=ws)
    live = dict(N=list(N_POOLS), water=["W"])
    common = dict(model="forest_n", params=p, t_end=T_end, dt=1.0 / 52, live=live, output="S", tol=1e-6, forcing=dict(pfacs=[1.0]))
    if rng.random() < 0.5:        # bare soil: deposition against leaching, water at its balance point
        s0 = _u(rng, 0.0, 5.0)
        ss = p["dep"] / (p["leach"] * ws)
        return dict(common, initial=dict(base, S=s0), expected=dict(S=ss + (s0 - ss) * math.exp(-p["leach"] * ws * T_end), W=ws))
    lt0 = _u(rng, 1.0, 5.0)        # tree litter only: first-order decay at the moisture factor
    m = ws / (ws + p["Wh"])
    a, lam = p["kT"] * m, p["leach"] * ws         # litter decays into soil; soil gains it and deposition, loses to leaching
    s_end = p["dep"] / lam * (1 - math.exp(-lam * T_end)) + a * lt0 * (math.exp(-a * T_end) - math.exp(-lam * T_end)) / (lam - a)
    return dict(common, initial=dict(base, Lt=lt0), expected=dict(Lt=lt0 * math.exp(-a * T_end), S=s_end, W=ws))


def _ode_case(rng):
    beta = _u(rng, 2.0, 6.0)
    u0 = _u(rng, 0.05, 0.7 / beta) if rng.random() < 0.5 else _u(rng, 1.6 / beta, 0.9)
    b0 = _u(rng, 0.005, 0.02)
    uinf = final_size(u0, b0, beta)
    return dict(model="ode_meanfield", params=dict(beta=beta), initial=dict(unburned=u0, burning=b0, burned=0.0, bare=1 - u0 - b0),
                t_end=400.0, dt=0.01, live=dict(mass=["unburned", "burning", "burned", "bare"]), output="burned",
                expected=dict(burned=u0 + b0 - uinf, unburned=uinf), tol=1e-6)


if "forest_n" not in REGISTRY:
    register_model("forest_n", "nonlinear", "port of forest-model-ledger model/base.py @ sha ebb656bb", forest_n, "rate",
             requires=tuple(DEFAULTS), limitations=("N and water only; C, P, energy not modelled", "one well-mixed stand",
                                                     "parameters hand-set, fitted to nothing")).event = fire
    register_model("ode_meanfield", "nonlinear", "0.1", ode_meanfield, "rate", requires=("beta",),
             limitations=("no space: cannot hold a spatial threshold", "burn-out rate fixed at 1 per step"))
    gate.add_builder("forest_n", _forest_case)
    gate.add_builder("ode_meanfield", _ode_case)


def certify():
    return dict(forest_n=gate.certify("forest_n", gate.default_make_config), ode_meanfield=gate.certify("ode_meanfield", gate.default_make_config))
