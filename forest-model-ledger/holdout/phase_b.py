# SPDX-License-Identifier: CC0-1.0
"""Phase B (predict + seal): four one-change branches from the run_9 candidate
anchor, one dense reference fit, and the sealed prediction file.

    python3 holdout/phase_b.py            # runs everything, prints the record
    python3 holdout/phase_b.py --seal     # also writes predictions.json and
                                          # predictions_commitment.json; prints
                                          # nonce_B once (never written to disk)

READ SET (enforced by what this file opens, nothing else):
    holdout/anchor_studies.csv   (sha256 asserted)
    model/base.py, ledger/toolkit/budget_closure.py, runs/run_9.py (sha256 asserted)
No network call. Every number printed or sealed is computed here.

Branches change ONE component each. B1-B3 are parameter / initial-state
changes passed to the unedited base.simulate. B4 adds one pool; it extends the
base module's pool list IN MEMORY for the duration of the call (the file
model/base.py is not edited; its hash is asserted before and after).

Mapping (assumption M1, the run-1 analogue): the plant-soil feedback log ratio
is read as the NETWORK-EFFECT log ratio
    rr = ln( focal biomass on conditioned soil, fungal pool intact
           / focal biomass on the same soil, fungal pool removed )
M2 (self vs other-conditioned soil) is computed beside it and never merged.
"""
import contextlib
import csv
import hashlib
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import numpy as np  # noqa: E402
from model import base, l0_audit  # noqa: E402

CSV_PATH = os.path.join(HERE, "anchor_studies.csv")
CSV_SHA = "e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438"
ANCHOR_COMMIT = "55c651b8f7228b4d28a21ad442bf817752e80d21"
ANCHOR_FILES = {
    "model/base.py": "ebb656bbf9554f3a6ed08055a0787f1e3a4ab6c024006a11555aed45eaea4ec8",
    "ledger/toolkit/budget_closure.py": "796b76f69e069f082603c3ee4392d56a0261de3ef139fbe942f14a21ba05a456",
    "runs/run_9.py": "0bae61f9a04d989a2d58fd90a24290c8285d7f62f0de47b81d760d671765ef22",
}

# ---- declared experiment constants (hand-set; none fitted to anything) ----
SEEDS = [0, 1, 2, 3, 4]      # phase-1 fire sequences
COND_YEARS = 20              # phase 1 (conditioning) length, yr
SEEDLING = 0.5               # focal biomass at the start of phase 2, N units
AFF = 2.5                    # B1: affinity; aff*0.6 = 1.5 = run_9's b at E = 0
POT_V = 0.3                  # B3: pot soil volume as a fraction of the plot
LIG = 0.4                    # B4: fraction of tree mortality entering the lignin pool
K_LIG = 0.03                 # B4: slow-guild decay of the lignin pool, 1/yr
BOOT = 2000                  # cluster bootstrap replicates
BOOT_SEED = 20261122


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def assert_inputs():
    out = {}
    got = sha256_file(CSV_PATH)
    if got != CSV_SHA:
        raise SystemExit("STOP: anchor_studies.csv sha256 %s != asserted %s" % (got, CSV_SHA))
    out["anchor_studies.csv"] = got
    for rel, want in ANCHOR_FILES.items():
        got = sha256_file(os.path.join(ROOT, rel))
        if got != want:
            raise SystemExit("STOP: %s sha256 drifted from ANCHOR_run9.yaml" % rel)
        out[rel] = got
    # the anchor commit: asserted when the ref is present locally, and the three
    # pinned files at that commit must be the bytes in the working tree
    try:
        ref = subprocess.run(["git", "rev-parse", "origin/archive/anchor-run9"], cwd=ROOT,
                             capture_output=True, text=True).stdout.strip()
    except OSError:
        ref = ""
    if ref:
        if ref != ANCHOR_COMMIT:
            raise SystemExit("STOP: origin/archive/anchor-run9 is %s, not the pin" % ref)
        for rel, want in ANCHOR_FILES.items():
            blob = subprocess.run(["git", "show", "%s:forest-model-ledger/%s" % (ANCHOR_COMMIT, rel)],
                                  cwd=ROOT, capture_output=True).stdout
            if hashlib.sha256(blob).hexdigest() != want:
                raise SystemExit("STOP: %s at the anchor commit does not match its pin" % rel)
        out["anchor_ref"] = "origin/archive/anchor-run9 == %s; 3 pinned files match at that commit" % ANCHOR_COMMIT
    else:
        out["anchor_ref"] = "NOT RECORDED (ref not present locally); file hashes asserted"
    return out


# ---------------------------------------------------------------- closure log
class Closure:
    """Every simulate() call made for a branch is audited; nothing is sampled."""

    def __init__(self):
        self.n = 0
        self.max_n = 0.0
        self.max_w = 0.0
        self.not_closed = 0

    def add(self, res):
        a = l0_audit.audit(res)
        self.n += 1
        self.max_n = max(self.max_n, abs(a["N"]["misclosure"]))
        self.max_w = max(self.max_w, abs(a["water"]["misclosure"]))
        if a["_overall"] != "PASS":
            self.not_closed += 1
        return a

    def record(self):
        return {
            "sims_audited": self.n,
            "N": {"state": "pass" if self.not_closed == 0 else "misclosure",
                  "max_abs_misclosure": self.max_n},
            "water": {"state": "pass" if self.not_closed == 0 else "misclosure",
                      "max_abs_misclosure": self.max_w},
            "C": "not checkable (VOID in the base model)",
            "P": "not checkable (VOID in the base model)",
            "energy": "not checkable (VOID in the base model)",
            "sims_not_closed": self.not_closed,
        }


def run(clo, **kw):
    res = base.simulate(**kw)
    clo.add(res)
    return res


# ------------------------------------------------------------- B4: lignin pool
def _lignin_flux_table(y, t, p, pfac):
    S, T, G, F, Lt, Lg, Ll, W = (max(y[base.IX[k]], 0.0) for k in base.N_POOLS + base.W_POOLS)
    m = W / (W + p["Wh"])
    sat = S / (S + p["K"])
    fb = 1.0 + p["b"] * F / (F + p["Kf"])
    precip = p["P0"] * (1 - p["drought"]) * pfac * (1 + p["season"] * np.sin(2 * np.pi * t))
    lig = p.get("lig", 0.0)
    return [
        ("deposition", None, "S", p["dep"]),
        ("uptake_T", "S", "T", p["uT"] * T * sat * fb * max(0.0, 1 - (T + p["aG"] * G) / p["KT"]) * m),
        ("uptake_G", "S", "G", p["uG"] * G * sat * max(0.0, 1 - (G + p["aT"] * T) / p["KG"]) * m),
        ("payment", "T", "F", p["c"] * T * F / (F + p["Kf"])),
        ("mort_T", "T", "Lt", (1 - lig) * p["mT"] * T),
        ("mort_T_lignin", "T", "Ll", lig * p["mT"] * T),
        ("mort_G", "G", "Lg", p["mG"] * G),
        ("mort_F", "F", "Lg", p["mF"] * F),
        ("decomp_Lt", "Lt", "S", p["kT"] * Lt * m),
        ("decomp_Lg", "Lg", "S", p["kG"] * Lg * m),
        ("decomp_Ll", "Ll", "S", p.get("kL", 0.0) * Ll * m),
        ("leaching", "S", None, p["leach"] * S * W),
        ("precipitation", None, "W", precip),
        ("evapotranspiration", "W", None, p["et"] * (T + G) * W),
        ("drainage", "W", None, p["drain"] * W),
    ]


@contextlib.contextmanager
def lignin_model():
    """Adds pool Ll to the in-memory base module; restores it on exit."""
    saved = (list(base.N_POOLS), list(base.NAMES), dict(base.IX), base.flux_table)
    try:
        base.N_POOLS.append("Ll")                 # budget_closure.BUDGETS holds this list
        base.NAMES[:] = (base.N_POOLS + base.W_POOLS + base.N_BOUND_IN + base.N_BOUND_OUT
                         + base.W_BOUND_IN + base.W_BOUND_OUT)
        base.IX.clear()
        base.IX.update({n: i for i, n in enumerate(base.NAMES)})
        base.flux_table = _lignin_flux_table
        yield
    finally:
        base.N_POOLS[:] = saved[0]
        base.NAMES[:] = saved[1]
        base.IX.clear()
        base.IX.update(saved[2])
        base.flux_table = saved[3]


# ---------------------------------------------------------- the PSF experiment
SOIL = ["S", "F", "Lt", "Lg", "W"]


def soil_of(res, extra=()):
    return {k: float(res["y"][base.IX[k]]) for k in SOIL + list(extra)}


def experiment(clo, focal, t2_years, params=None, seed=0, neighbour=0.0, pot_v=1.0,
               cond_years=COND_YEARS, extra_pools=()):
    """Returns (rr_M1, rr_M2).

    phase 1  the focal guild alone conditions the soil for cond_years (fires on,
             as in the anchor); the OTHER guild alone conditions the 'away' soil
    phase 2  a seedling of the focal guild grows t2_years on each soil, fires off
             M1: home soil vs the same soil with the fungal pool moved to fast
                 litter (sterilised: necromass stays, so N is conserved)
             M2: home soil vs away soil
    pot_v    soil volume fraction applied in phase 2 (amounts scale by pot_v;
             half-saturations are concentrations, so K, Kf, Wh scale too, and
             the boundary inputs dep and P0 scale with the pot's area)
    """
    p = dict(params or {})
    other = "G" if focal == "T" else "T"
    zero = {k: 0.0 for k in extra_pools}
    home = run(clo, years=cond_years, seed=seed, params=p, init=dict(zero, **{other: 0.0}))
    away = run(clo, years=cond_years, seed=seed, params=p, init=dict(zero, **{focal: 0.0}))
    p2 = dict(p)
    if pot_v != 1.0:
        d = base.DEFAULTS
        for k in ("K", "Kf", "Wh", "dep", "P0"):
            p2[k] = p.get(k, d[k]) * pot_v

    def grow(soil):
        init = {k: v * pot_v for k, v in soil.items()}
        init[focal] = SEEDLING
        init[other] = neighbour
        years = max(1, int(math.ceil(t2_years)))
        n_steps = max(1, int(round(t2_years * 52)))
        res = run(clo, years=years, seed=seed, params=p2, init=init, fires=False)
        # base.simulate integrates whole years; the response is read at the
        # requested step from the trajectory (the audit covers the whole call)
        return float(res["traj"][min(n_steps, len(res["traj"]) - 1), base.IX[focal]])

    s_home = soil_of(home, extra_pools)
    s_ster = dict(s_home)
    s_ster["Lg"] = s_home["Lg"] + s_home["F"]
    s_ster["F"] = 0.0
    s_away = soil_of(away, extra_pools)
    b_home, b_ster, b_away = grow(s_home), grow(s_ster), grow(s_away)
    return math.log(b_home / b_ster), math.log(b_home / b_away)


def over_seeds(clo, **kw):
    r = [experiment(clo, seed=s, **kw) for s in SEEDS]
    m1 = [x[0] for x in r]
    m2 = [x[1] for x in r]
    return {"M1_mean": float(np.mean(m1)), "M1_min": float(min(m1)), "M1_max": float(max(m1)),
            "M2_mean": float(np.mean(m2)), "M2_min": float(min(m2)), "M2_max": float(max(m2)),
            "M1_by_seed": [float(v) for v in m1], "M2_by_seed": [float(v) for v in m2]}


def paired_direction(a, b, key="M1_by_seed"):
    """Sign of a - b, called only when every seed agrees; otherwise unresolved."""
    d = [x - y for x, y in zip(a[key], b[key])]
    if all(v > 0 for v in d):
        return "positive"
    if all(v < 0 for v in d):
        return "negative"
    return "unresolved (seeds disagree in sign)"


def zero_crossing(xs, ys):
    for i in range(len(xs) - 1):
        if ys[i] == 0:
            return float(xs[i])
        if ys[i] * ys[i + 1] < 0:
            return float(xs[i] + (xs[i + 1] - xs[i]) * ys[i] / (ys[i] - ys[i + 1]))
    return None


def sign(x, eps=1e-9):
    return "positive" if x > eps else ("negative" if x < -eps else "zero")


def monotone(xs, ys):
    d = np.diff(ys)
    if np.all(d > 0):
        return "increasing"
    if np.all(d < 0):
        return "decreasing"
    return "non-monotone"


# ------------------------------------------------------------------- data fits
def load_rows():
    with open(CSV_PATH, encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


def _wls(x, y, w):
    xm = np.sum(w * x) / np.sum(w)
    ym = np.sum(w * y) / np.sum(w)
    sxx = np.sum(w * (x - xm) ** 2)
    slope = np.sum(w * (x - xm) * (y - ym)) / sxx
    return slope, ym - slope * xm


def _tau2(x, y, v):
    """Method-of-moments between-row variance for a one-moderator meta-regression."""
    w = 1.0 / v
    slope, icpt = _wls(x, y, w)
    q = np.sum(w * (y - icpt - slope * x) ** 2)
    X = np.column_stack([np.ones_like(x), x])
    XtWX = X.T @ (X * w[:, None])
    XtW2X = X.T @ (X * (w ** 2)[:, None])
    c = np.sum(w) - np.trace(np.linalg.solve(XtWX, XtW2X))
    return max(0.0, (q - (len(y) - 2)) / c)


def fit(rows, xfun, yfun=lambda r: float(r["rr"]), label=""):
    """Slope of y on x, weights 1/(var + tau2); 80% interval by cluster bootstrap
    over Author (the study), tau2 held at its full-sample value."""
    xs, ys, vs, cl, dropped = [], [], [], [], 0
    for r in rows:
        try:
            x, y, v = xfun(r), yfun(r), float(r["var"])
        except (ValueError, KeyError):
            dropped += 1
            continue
        if x is None or not (v > 0) or not all(map(math.isfinite, (x, y, v))):
            dropped += 1
            continue
        xs.append(x), ys.append(y), vs.append(v), cl.append(r["Author"])
    x, y, v = np.array(xs), np.array(ys), np.array(vs)
    t2 = _tau2(x, y, v)
    w = 1.0 / (v + t2)
    slope, icpt = _wls(x, y, w)
    names = sorted(set(cl))
    idx = {n: [] for n in names}
    for i, n in enumerate(cl):
        idx[n].append(i)
    groups = [np.array(idx[n]) for n in names]
    rng = np.random.default_rng(BOOT_SEED)
    reps, degenerate = [], 0
    for _ in range(BOOT):
        pick = rng.integers(0, len(groups), size=len(groups))
        ii = np.concatenate([groups[k] for k in pick])
        xb = x[ii]
        if np.ptp(xb) == 0:
            degenerate += 1
            continue
        reps.append(_wls(xb, y[ii], w[ii])[0])
    lo, hi = np.percentile(reps, [10, 90])
    return {
        "label": label, "n_rows": len(y), "n_studies": len(names), "rows_dropped": dropped,
        "tau2": float(t2), "estimate": float(slope),
        "interval80": [float(lo), float(hi)],
        "interval_excludes_zero": bool(lo > 0 or hi < 0),
        "direction": sign(float(slope), 0.0),
        "bootstrap": {"replicates": BOOT, "degenerate_skipped": degenerate, "seed": BOOT_SEED,
                      "cluster": "Author"},
    }


def dummy(col, one, zero):
    def f(r):
        if r[col] == one:
            return 1.0
        if r[col] == zero:
            return 0.0
        return None
    return f


# ------------------------------------------------------------------ the branches
def anchor_check():
    res = base.simulate(years=300, seed=0)
    a = l0_audit.audit(res)
    return {"fires": len(res["events"]), "N_misclosure": a["N"]["misclosure"],
            "water_misclosure": a["water"]["misclosure"], "overall": a["_overall"],
            "final_T": float(res["y"][base.IX["T"]])}


def build(rows):
    t2_vals = []
    for r in rows:
        try:
            t2_vals.append(float(r["Phase2.time"]))
        except ValueError:
            pass                                   # 'NA' rows; counted as rows_dropped in the B2 fit
    t2_med = float(np.median(t2_vals))
    t2_default = t2_med / 12.0
    out = {}

    # anchor reading of the same experiment (the diff baseline for every branch)
    clo0 = Closure()
    anchor_T = over_seeds(clo0, focal="T", t2_years=t2_default)
    anchor_G = over_seeds(clo0, focal="G", t2_years=t2_default)
    out["_anchor_experiment"] = {"t2_months": t2_med, "woody_T": anchor_T, "nonwoody_G": anchor_G,
                                 "closure": clo0.record()}

    # ---- B1 stress-gated coupling
    clo = Closure()
    grid = [0.0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
    curve = []
    for E in grid:
        b = AFF * (0.6 - 0.8 * E)
        r = over_seeds(clo, focal="T", t2_years=t2_default, params={"b": b})
        curve.append({"E": E, "b": b, **r})
    m1 = [c["M1_mean"] for c in curve]
    shape = monotone(grid, m1)
    out["B1"] = {
        "atom": "stress-gated coupling",
        "column": ["AI", "MAP"],
        "change": "b = aff*(0.6-0.8E), aff = %.1f (aff*0.6 = run_9 b = 1.5 at E = 0); E = min(AI, 1)" % AFF,
        "model": {"curve": curve, "shape_M1_vs_E": shape,
                  "E_where_b_changes_sign": zero_crossing(grid, [c["b"] for c in curve]),
                  "E_where_M1_changes_sign": zero_crossing(grid, m1),
                  "M2_shape_vs_E": monotone(grid, [c["M2_mean"] for c in curve]), "M1_at_E0": m1[0], "M1_at_E1": m1[-1],
                  "diff_vs_anchor_M1": [c["M1_mean"] - anchor_T["M1_mean"] for c in curve]},
        "model_direction": {"decreasing": "negative", "increasing": "positive"}.get(shape, "non-monotone"),
        "fit": {"AI": fit(rows, lambda r: float(r["AI"]), label="rr ~ AI"),
                "MAP": fit(rows, lambda r: float(r["MAP"]) / 1000.0, label="rr ~ MAP per 1000 mm")},
        "closure": clo.record(),
    }

    # ---- B2 lag / slow response
    clo = Closure()
    months = [0.5, 1, 2, 3, 6, 12, 24, 36]
    curve = [{"months": mth, **over_seeds(clo, focal="T", t2_years=mth / 12.0)} for mth in months]
    absm1 = [abs(c["M1_mean"]) for c in curve]
    shape = monotone(months, absm1)
    out["B2"] = {
        "atom": "lag / slow response",
        "column": ["Phase2.time"],
        "change": "phase-2 duration T varied over %s months; nothing else" % months,
        "model": {"curve": curve, "shape_absM1_vs_T": shape,
                  "absM1_shortest": absm1[0], "absM1_longest": absm1[-1],
                  "absM1_peak_months": months[int(np.argmax(absm1))],
                  "shape_absM2_vs_T": monotone(months, [abs(c["M2_mean"]) for c in curve]),
                  "diff_vs_anchor_M1": [c["M1_mean"] - anchor_T["M1_mean"] for c in curve]},
        "model_direction": {"decreasing": "negative", "increasing": "positive"}.get(shape, "non-monotone"),
        "fit": {"Phase2.time": fit(rows, lambda r: float(r["Phase2.time"]),
                                   yfun=lambda r: abs(float(r["rr"])), label="|rr| ~ Phase2.time (months)")},
        "closure": clo.record(),
    }

    # ---- B3 instrument boundary
    clo = Closure()
    nb = base.INIT["G"]
    cells = {
        "field (neighbours %.1f, volume 1)" % nb: over_seeds(clo, focal="T", t2_years=t2_default, neighbour=nb),
        "neighbours removed only": over_seeds(clo, focal="T", t2_years=t2_default, neighbour=0.0),
        "pot volume only": over_seeds(clo, focal="T", t2_years=t2_default, neighbour=nb, pot_v=POT_V),
        "greenhouse (alone, volume %.1f)" % POT_V: over_seeds(clo, focal="T", t2_years=t2_default,
                                                               neighbour=0.0, pot_v=POT_V),
    }
    keys = list(cells)
    d = cells[keys[3]]["M1_mean"] - cells[keys[0]]["M1_mean"]
    out["B3"] = {
        "atom": "instrument boundary",
        "column": ["Experimental.setting"],
        "change": "phase-2 boundary: neighbour count (%.1f -> 0) and soil volume (1 -> %.1f)" % (nb, POT_V),
        "model": {"cells": cells, "greenhouse_minus_field_M1": d,
                  "neighbour_part_M1": cells[keys[1]]["M1_mean"] - cells[keys[0]]["M1_mean"],
                  "volume_part_M1": cells[keys[2]]["M1_mean"] - cells[keys[0]]["M1_mean"],
                  "greenhouse_minus_field_M2": cells[keys[3]]["M2_mean"] - cells[keys[0]]["M2_mean"],
                  "diff_vs_anchor_M1": {k: v["M1_mean"] - anchor_T["M1_mean"] for k, v in cells.items()}},
        "model_direction": paired_direction(cells[keys[3]], cells[keys[0]]),
        "model_direction_M2": paired_direction(cells[keys[3]], cells[keys[0]], "M2_by_seed"),
        "fit": {"Experimental.setting": fit(rows, dummy("Experimental.setting", "Greenhouse", "Field"),
                                            label="rr Greenhouse minus Field")},
        "closure": clo.record(),
    }

    # ---- B4 slow-pool coupling
    clo = Closure()
    with lignin_model():
        lp = {"lig": LIG, "kL": K_LIG}
        b4_T = over_seeds(clo, focal="T", t2_years=t2_default, params=lp, extra_pools=("Ll",))
        b4_G = over_seeds(clo, focal="G", t2_years=t2_default, params=lp, extra_pools=("Ll",))
        # the extended table with lig = 0 must return the anchor reading
        null_T = over_seeds(clo, focal="T", t2_years=t2_default, params={"lig": 0.0, "kL": K_LIG},
                            extra_pools=("Ll",))
    restored = (base.N_POOLS == ["S", "T", "G", "F", "Lt", "Lg"]
                and sha256_file(os.path.join(ROOT, "model/base.py")) == ANCHOR_FILES["model/base.py"])
    d = b4_T["M1_mean"] - b4_G["M1_mean"]
    d0 = anchor_T["M1_mean"] - anchor_G["M1_mean"]
    out["B4"] = {
        "atom": "slow-pool coupling",
        "column": ["Life.form"],
        "change": "lignin pool Ll: %.1f of tree mortality enters it, slow guild decays it at %.2f/yr" % (LIG, K_LIG),
        "model": {"woody_T": b4_T, "nonwoody_G": b4_G,
                  "woody_minus_nonwoody_M1": d, "woody_minus_nonwoody_M1_anchor": d0,
                  "woody_minus_nonwoody_M2": b4_T["M2_mean"] - b4_G["M2_mean"],
                  "woody_minus_nonwoody_M2_anchor": anchor_T["M2_mean"] - anchor_G["M2_mean"],
                  "diff_vs_anchor_M1": {"woody_T": b4_T["M1_mean"] - anchor_T["M1_mean"],
                                        "nonwoody_G": b4_G["M1_mean"] - anchor_G["M1_mean"]},
                  "lig0_returns_anchor_M1": abs(null_T["M1_mean"] - anchor_T["M1_mean"]),
                  "base_module_restored": bool(restored)},
        "model_direction": paired_direction(b4_T, b4_G),
        "model_direction_M2": paired_direction(b4_T, b4_G, "M2_by_seed"),
        "model_direction_anchor": paired_direction(anchor_T, anchor_G),
        "fit": {"Life.form": fit(rows, dummy("Life.form", "Woody", "Nonwoody"),
                                 label="rr Woody minus Nonwoody")},
        "closure": clo.record(),
    }

    # ---- R5 reference, no model run
    out["R5"] = {
        "atom": "REFERENCE: enemy release",
        "tag": "dense reference, no run_9 mechanism",
        "column": ["Sp.origin"],
        "change": "none; fit only, not a branch",
        "model": None,
        "model_direction": "NOT RECORDED (no model run; enemy release is not in run_9)",
        "fit": {"Sp.origin": fit(rows, dummy("Sp.origin", "Non-native", "Native"),
                                 label="rr Non-native minus Native")},
        "closure": "not checkable (no model run)",
    }
    return out


ASSUMPTIONS = {
    "B1": [
        ["A1", "fertility E maps onto aridity / water limitation: E = min(AI, 1); MAP is read as a second monotone proxy of E",
         "model and fit disagree in sign on AI, or AI and MAP fits disagree with each other"],
        ["A2", "the benefit term is linear in E and changes sign inside 0..1 (written into the equation; run_1 flag: partly circular)",
         "holdout rr vs AI is flat or curved with no sign change inside the sampled AI range"],
        ["A3", "aff is set so that b at E = 0 equals run_9's b",
         "direction holds but the magnitude is off by a constant factor"],
        ["A4", "E changes only b; precipitation, deposition and decay stay at run_9 values",
         "an aridity effect appears in sterilised-soil growth as well (not a coupling effect)"],
    ],
    "B2": [
        ["A1", "one model year = 12 Phase2.time units (months)", "the modelled lag sits at a time scale the data never samples"],
        ["A2", "the response is read as |rr| under M1 at the end of phase 2", "sign changes with duration cancel in the mean while |rr| moves"],
        ["A3", "the conditioned soil does not change with phase-2 duration (same phase 1 for all T)",
         "long experiments differ from short ones in phase-1 method, not duration"],
        ["A4", "no fire in phase 2", "none expected in pots; field rows with burns would break it"],
    ],
    "B3": [
        ["A1", "greenhouse = focal plant alone in a pot holding POT_V of the plot's soil; field = whole plot with the grass neighbour at INIT",
         "the greenhouse minus field difference tracks Phase2.grow (Alone / Competition) and not setting"],
        ["A2", "amounts scale with soil volume; half-saturations K, Kf, Wh are concentrations and scale with it; dep and P0 scale with pot area",
         "neighbour part and volume part have opposite signs and the sum hides both"],
        ["A3", "the neighbour is the run_9 grass guild", "woody neighbours in field rows change the competition term"],
        ["A4", "light ceiling KT is not rescaled for the pot", "pot-bound plants hit a ceiling the model does not have"],
    ],
    "B4": [
        ["A1", "Woody = the tree guild T (pays fungi, slow litter); Nonwoody = the grass guild G (no fungal partner, fast litter)",
         "nonwoody rows with strong mycorrhizal response; the difference then reads as partner presence, not litter"],
        ["A2", "a fraction LIG of tree mortality is lignin; a slow guild decays it at K_LIG per yr at full moisture; the pool does not burn",
         "the woody reading moves with fire frequency instead of with the pool"],
        ["A3", "grass litter carries no lignin", "nonwoody reading unchanged by the branch (holds by construction here)"],
        ["A4", "COND_YEARS of conditioning is long enough for the slow pool to matter", "the branch reading equals the anchor reading within seed range"],
    ],
    "R5": [
        ["A1", "no mechanism; a moderator fit on anchor studies only", "not applicable"],
    ],
}

MAPPING = {
    "id": "M1",
    "statement": "PSF log ratio rr is read as the network-effect log ratio: ln(focal biomass on its own conditioned soil with the fungal pool intact / on the same soil with the fungal pool moved to fast litter). Run-1 analogue.",
    "status": "ASSUMPTION, PROPOSED",
    "failure_signature": "Self-Other rows and Self-Sterilized rows give opposite moderator directions; M2 (self vs other-conditioned soil) is carried beside M1 for that reading",
    "known_limits": [
        "the model has one mutualist pool and no pathogen pool, so M1 cannot go negative except through b < 0 (B1)",
        "the sterilised arm keeps fungal necromass as fast litter (a nutrient flush)",
        "Response (aboveground / total biomass) is one pool here",
    ],
}


def predictions(branches, crowding):
    preds = {}
    for pid in ["B1", "B2", "B3", "B4", "R5"]:
        b = branches[pid]
        per_col = {}
        for col, f in b["fit"].items():
            per_col[col] = {
                "quantity": f["label"],
                "direction": f["direction"],
                "estimate": f["estimate"],
                "interval": f["interval80"],
                "interval_level": 0.8,
                "interval_excludes_zero": f["interval_excludes_zero"],
                "n_rows": f["n_rows"], "n_studies": f["n_studies"], "rows_dropped": f["rows_dropped"],
                "model_direction": b["model_direction"],
                "model_and_fit_agree": (b["model_direction"] == f["direction"]) if b["model"] else None,
            }
        preds[pid] = {
            "atom": b["atom"],
            "kind": "reference" if pid == "R5" else "branch",
            "tag": b.get("tag"),
            "column": b["column"],
            "change": b["change"],
            "model_direction": b["model_direction"],
            "model_direction_M2": b.get("model_direction_M2", "NOT RECORDED"),
            "direction": {c: v["direction"] for c, v in per_col.items()},
            "interval": {c: v["interval"] for c, v in per_col.items()},
            "per_column": per_col,
            "model_summary": None if b["model"] is None else {
                k: v for k, v in b["model"].items() if k not in ("curve", "cells")},
            "closure": b["closure"],
            "crowding": crowding[pid]["tag"],
            "crowding_basis": crowding[pid]["basis"],
            "assumptions": [{"id": a[0], "assumption": a[1], "failure_signature": a[2]} for a in ASSUMPTIONS[pid]],
            "mapping": MAPPING if pid != "R5" else "none (fit only)",
        }
    return preds


CROWDING = {pid: {"tag": "NOT RECORDED",
                  "basis": "probe not run: no tool-less fresh chat was available to this session; a sub-agent given only the question keeps file and network access to the repository, including the holdout files this run may not read"}
            for pid in ["B1", "B2", "B3", "B4"]}
CROWDING["R5"] = {"tag": "NOT RECORDED",
                  "basis": "not a branch; the order tags R5 a dense reference and asks for no probe"}


def main():
    hashes = assert_inputs()
    rows = load_rows()
    chk = anchor_check()
    branches = build(rows)
    doc = {
        "record": "forest-model-ledger holdout Phase B predictions",
        "license": "CC0-1.0",
        "date_utc": "2026-11-22",
        "anchor": {"run": "run_9", "commit": ANCHOR_COMMIT, "status": "candidate",
                   "rerun_here": chk},
        "inputs": hashes,
        "anchor_studies": {"rows": len(rows), "studies": len(set(r["Author"] for r in rows))},
        "interval_note": "interval = 80% cluster-bootstrap interval (studies resampled) of the moderator estimate on anchor studies; it is not widened for the holdout's own sampling error, whose size this run did not read",
        "direction_note": "direction and interval are the anchor-study fit; model_direction is the branch run's reading; they are sealed side by side and never merged",
        "constants": {"seeds": SEEDS, "cond_years": COND_YEARS, "seedling": SEEDLING, "aff": AFF,
                      "pot_v": POT_V, "lig": LIG, "k_lig": K_LIG, "bootstrap": BOOT, "bootstrap_seed": BOOT_SEED},
        "anchor_experiment": branches["_anchor_experiment"],
        "predictions": predictions(branches, CROWDING),
        "curves": {"B1": branches["B1"]["model"]["curve"], "B2": branches["B2"]["model"]["curve"],
                   "B3": branches["B3"]["model"]["cells"]},
    }
    data = (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=True) + "\n").encode("ascii")
    print(data.decode("ascii"))
    if "--seal" in sys.argv:
        ppath = os.path.join(HERE, "predictions.json")
        with open(ppath, "wb") as f:
            f.write(data)
        nonce = os.urandom(32)
        commit = hashlib.sha256(nonce + data).hexdigest()
        cdoc = {"record": "Phase B predictions commitment", "license": "CC0-1.0",
                "scheme": "sha256(nonce_B || predictions.json bytes), nonce_B = 32 random bytes, not committed",
                "commitment": commit,
                "predictions_sha256": hashlib.sha256(data).hexdigest(),
                "predictions_bytes": len(data), "date_utc": "2026-11-22"}
        with open(os.path.join(HERE, "predictions_commitment.json"), "wb") as f:
            f.write((json.dumps(cdoc, indent=1, sort_keys=True) + "\n").encode("ascii"))
        sys.stderr.write("nonce_B (hex, reported once, not written): %s\n" % nonce.hex())
        sys.stderr.write("commitment: %s\n" % commit)


if __name__ == "__main__":
    main()
