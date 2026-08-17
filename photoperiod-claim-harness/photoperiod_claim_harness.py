#!/usr/bin/env python3
# photoperiod_claim_harness.py
# CC0-1.0 / public domain. stdlib only. phone-buildable. single file.
#
# WHAT THIS IS
#   A marker for a sensed shape that needs more exploration -- not a thesis,
#   not a refutation of any paper. It encodes four inconsistencies found in a
#   published closed-loop-LLM greenhouse result as RUNNABLE, FALSIFIABLE sims,
#   plus a harness that lets a model (or a person) run them, log provenance,
#   propose mechanism edits under protocol, and emit a hypothesis for a human.
#
#   Correct reader response: test whether it fits, extend it, or report where
#   it breaks. A break is a measurement and goes in the claim table.
#
# THE ONE HARD RULE (refutation protocol)
#   When a sim contradicts a claim: UPDATE THE CLAIM. NEVER RETUNE THE SIM.
#   A sim may only be edited by declaring a MECHANISM change, with the
#   prediction registered BEFORE the run. The harness refuses edits whose
#   stated reason is that a claim failed. See MechanismEdit.
#
# ANTI-FREEZE
#   Output is a trajectory, not a stored verdict. Hypothesis blocks carry a
#   confidence gradient and a comfort threshold as SEPARATE readouts, and name
#   the measurement that would move them. No sim in here decides anything.
#
# USAGE
#   python3 photoperiod_claim_harness.py run-all
#   python3 photoperiod_claim_harness.py run C2        # CLAIM id, not sim id
#   python3 photoperiod_claim_harness.py sweep S2      # SIM id -- different
#                                                      # registry, on purpose
#   python3 photoperiod_claim_harness.py claims
#   python3 photoperiod_claim_harness.py protocol      # bench measurements
#   python3 photoperiod_claim_harness.py bench C1 ...  # record a MEASUREMENT
#   python3 photoperiod_claim_harness.py hypothesis
#   python3 photoperiod_claim_harness.py log           # provenance chain

import hashlib
import json
import math
import os
import sys
import time

VERSION = "0.1.0"
LOGPATH = os.environ.get("PCH_LOG", "pch_log.jsonl")

# ----------------------------------------------------------------------------
# 0. PROVENANCE TYPES
#    Every number carries where it came from. Three sources never merge.
# ----------------------------------------------------------------------------

SOURCE = {
    "REPORTED": "asserted in the source publication; not independently measured here",
    "PHYSICS": "textbook mechanism with an independent literature basis",
    "SIM": "produced by code in this file from stated parameters",
    "BENCH": "produced by a physical measurement; empty until someone runs one",
}


def require(condition, why):
    """
    Guard for a predicate whose input may be empty. run_claim() catches a
    raising predicate and records UNDECIDED, which is the correct third
    verdict -- C1's `signature_spread < 1.5` used to return SUPPORTED from a
    run in which zero cells reproduced the signature, because the spread of
    an empty set was reported as 0.0. A pass an empty result set returns is
    not a pass, and "the sim cannot produce the reported package at all" is
    neither of the two verdicts on offer.
    """
    if not condition:
        raise ValueError(why)
    return True


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def self_hash():
    """Content hash of this file. Any sim edit changes it. Logged per run."""
    try:
        with open(os.path.abspath(__file__), "r") as f:
            return sha(f.read())
    except Exception:
        return "unhashable"


# ----------------------------------------------------------------------------
# 1. CLAIM TABLE
#    predicate: a function of the sim output dict -> bool. Falsifiable or it
#    does not belong in this table.
# ----------------------------------------------------------------------------

CLAIM_TABLE = [
    {
        "id": "C1",
        "sim": "S1",
        "source": "REPORTED",
        "statement": (
            "Energy per unit output fell ~68% while biomass rate held, "
            "fiber fell, hydration rose, juice yield rose 20-25%."
        ),
        "test": (
            "Scan light reduction x shade-avoidance x sink strength. Across all "
            "cells that reproduce the reported signature, how wide is the range "
            "of ACTUAL energy-per-dry-gram? Narrow means the published metrics "
            "pin the real efficiency down. Wide means they do not."
        ),
        "predicate": lambda o: (
            require(o["signature_cells"] > 0,
                    "no cell reproduces the reported signature: the sim "
                    "cannot produce the package at all, which is neither "
                    "verdict")
            and o["signature_spread"] < 1.5
        ),
        "reads": (
            "TRUE  -> the reported metrics pin the real efficiency down.\n"
            "FALSE -> NON-DIAGNOSTIC OF MAGNITUDE: the same reported "
            "signature is produced across a wide range of true "
            "per-photosynthate efficiencies. Read `signature_sign_agreement` "
            "before reading this as 'the signature means nothing' -- on the "
            "shipped parameters every signature cell also improves energy "
            "per dry gram, so the package licenses the SIGN and not the "
            "SIZE. Dry mass is the missing measurement; 68% is a size.\n"
            "UNDECIDED -> zero signature cells. The sim did not reproduce "
            "the reported package, so it has nothing to say about it."
        ),
    },
    {
        "id": "C2",
        "sim": "S2",
        "source": "PHYSICS",
        "statement": (
            "PREMISE (literature): wheat is an angiosperm; protochlorophyllide "
            "reduction is light-dependent, POR only, no DPOR. Net chlorophyll "
            "synthesis in darkness is not available.\n"
            "HYPOTHESIS UNDER TEST: dark intervals could still raise final "
            "chlorophyll at equal photon dose by recharging the Pchlide/POR/"
            "NADPH pool between pulses."
        ),
        "test": (
            "Can intermittent dark still raise final chlorophyll at EQUAL total "
            "photon dose, via dark regeneration of the Pchlide/POR/NADPH pool?"
        ),
        "predicate": lambda o: o["best_duty"] < 0.99,
        "reads": (
            "TRUE  -> pool-charging is a live mechanism; the finding can be real "
            "without violating angiosperm biosynthesis.\n"
            "FALSE -> continuous light dominates, because the FLU clamp acts on "
            "POOL SIZE: a full pool SLOWS synthesis, so draining it continuously "
            "maximises flux. The reported effect then needs a different "
            "mechanism. Named candidate, not yet simulated: shade acclimation "
            "(antenna investment per unit leaf area rises under low light). "
            "See PENDING_EDITS."
        ),
    },
    {
        "id": "C3",
        "sim": "S2",
        "source": "PHYSICS",
        "statement": (
            "Dark drives two opposed processes: substrate pool charging (gain) "
            "and senescence-linked chlorophyll degradation (loss). Different "
            "time constants imply a crossover in dark-interval length."
        ),
        "test": "Sweep dark-interval length. Does the sign of dChl flip?",
        "predicate": lambda o: o["crossover_h"] is not None,
        "reads": (
            "TRUE  -> there is a finite optimal dark interval and 'long dark "
            "intervals' is an underspecified control setting.\n"
            "FALSE -> no crossover in this regime; one process dominates "
            "throughout."
        ),
    },
    {
        "id": "C4",
        "sim": "S3",
        "source": "PHYSICS",
        "statement": (
            "Chlorophyll was read by multispectral reflectance. Reflectance "
            "indices move with leaf water content and thickness. The control "
            "strategy changes water content and thickness."
        ),
        "test": (
            "Run a controller that maximizes the INDEX. Does the index rise "
            "while chlorophyll-per-dry-gram falls?"
        ),
        "predicate": lambda o: o["index_gain"] > 0.0 and o["true_chl_gain"] < 0.0,
        "reads": (
            "TRUE  -> the reported signature is reproducible from measurement "
            "artifact alone, so it is not diagnostic of physiology.\n"
            "FALSE -> index and truth move together here; artifact does not "
            "explain the signature."
        ),
    },
    {
        "id": "C5",
        "sim": "S4",
        "source": "PHYSICS",
        "statement": (
            "A shared calibration bias is NOT cancelled by adding channels. "
            "Independence is a property of the calibration path, not of N."
        ),
        "test": (
            "Inject a common-mode calibration bias across all channels. Does "
            "channel count reduce the error in the derived quantity?"
        ),
        "predicate": lambda o: o["err_49ch"] > 0.5 * o["err_1ch"],
        "reads": (
            "TRUE  -> common-mode bias survives 49 channels; only a second, "
            "differently-calibrated instrument removes it.\n"
            "FALSE -> channel count did reduce the error; the bias was not "
            "common-mode in this run."
        ),
    },
]


# ----------------------------------------------------------------------------
# 2. SIMS
#    Deterministic. Euler integration, 1 h steps. No dependencies.
#    Parameters are DECLARED, not fitted. Change them by MechanismEdit only.
# ----------------------------------------------------------------------------

def _s1_run(scale, sae, sink_k, days=8, dt=0.5):
    """
    One growth trajectory. Declared mechanism, no fitted parameters.

      V      tissue volume (mL)      expansion: turgor + wall-loosening limited
      C_str  wall / structural (g)   CARBON limited, rate law on the pool
      C_sol  soluble dry carbon (g)  photosynthate; feeds back on assimilation
      W      water (g) = rho*V - dry tracks volume, costs ~no photons

    Mechanisms encoded (each has an independent literature basis; change only
    by MechanismEdit):
      M1 area interception with a footprint ceiling (self-shading / tray edge)
      M2 sink feedback: soluble sugar accumulation downregulates assimilation
      M3 shade-avoidance elongation: lower light raises expansion rate
      M4 wall deposition is a rate law on the soluble pool, so fast expansion
         under a thin pool yields a THINNER wall per unit volume
    """
    V, C_str, C_sol = 1.0, 0.05, 0.02
    A_max, K_I = 0.020, 0.45
    k_a, A_sat = 0.9, 22.0   # canopy closes early in a tray; footprint is the cap
    r_resp = 0.0025
    k_e, Kc = 0.018, 0.02
    w_target, k_dep = 0.10, 0.05
    c_ref, rho, V_max = 0.020, 0.95, 400.0
    K_sae = 0.5
    kWh = 0.0
    for _ in range(int(days * 24 / dt)):
        I = scale
        A_eff = A_sat * (1.0 - math.exp(-(k_a * V) / A_sat))          # M1
        sink = 1.0 / (1.0 + sink_k * (C_sol / (V * c_ref)) ** 2)      # M2
        gross = A_max * (I / (I + K_I)) * A_eff * sink
        C_sol += (gross - r_resp * (C_str + C_sol)) * dt
        boost = 1.0 + sae * (K_sae / (K_sae + I))                     # M3
        g = C_sol / (C_sol + Kc)
        dV = k_e * boost * V * (1.0 - V / V_max) * g * dt
        dep = min(w_target * dV, k_dep * max(0.0, C_sol) * dt)        # M4
        C_sol -= dep
        C_str += dep
        V += dV
        kWh += 0.20 * scale * dt
    dry = max(1e-9, C_str + max(0.0, C_sol))
    fresh = rho * V
    W = max(0.0, fresh - dry)
    return {
        "V_mL": V, "dry_g": dry, "fresh_g": fresh, "water_g": W,
        "water_frac": W / fresh,
        "fiber_frac_dry": C_str / dry,
        "wall_density": C_str / V,           # g wall per mL -- the juicer's fiber
        "juice_L": W * (1.0 - 2.0 * (C_str / V)) / 1000.0,
        "kWh": kWh,
    }


def s1_mass_denominator(dli_scale=0.40, sae=0.8, sink_k=1.0, days=8, **kw):
    """
    S1 -- MASS / DENOMINATOR SWAP, run as a REGIME MAP, not a single verdict.

    Scans light reduction x shade-avoidance strength. For each cell it asks two
    separate questions and never merges them:

      (a) does the cell reproduce the REPORTED side-effect signature?
          fresh mass held or up, wall density down, water fraction up, juice up
      (b) inside that signature, does energy per DRY gram improve?

    A cell where (a) is TRUE and (b) is FALSE is a configuration in which the
    whole reported package appears with no gain per unit photosynthate.
    """
    base = _s1_run(1.0, sae, sink_k, days=days)
    grid = []
    hits = []
    for s in (0.70, 0.55, 0.40, 0.30, 0.20):
      for sk in (0.2, 1.0, 4.0):
        for sa in (0.0, 0.4, 0.8, 1.2, 1.6):
            t = _s1_run(s, sa, sk, days=days)
            b = _s1_run(1.0, sa, sk, days=days)
            sig = (
                t["fresh_g"] >= 0.95 * b["fresh_g"]
                and t["wall_density"] < b["wall_density"]
                and t["water_frac"] > b["water_frac"]
                and t["juice_L"] > b["juice_L"]
            )
            per_dry = (t["kWh"] / t["dry_g"]) / (b["kWh"] / b["dry_g"])
            per_fresh = (t["kWh"] / t["fresh_g"]) / (b["kWh"] / b["fresh_g"])
            per_juice = (t["kWh"] / t["juice_L"]) / (b["kWh"] / b["juice_L"])
            cell = {"dli": s, "sae": sa, "sink_k": sk, "signature": sig,
                    "kWh_per_dry": per_dry, "kWh_per_fresh": per_fresh,
                    "kWh_per_juice": per_juice,
                    "dry_ratio": t["dry_g"] / b["dry_g"]}
            grid.append(cell)
            if sig and per_dry >= 1.0:
                hits.append(cell)
    ref = _s1_run(dli_scale, sae, sink_k, days=days)
    sig_dry = [c["kWh_per_dry"] for c in grid if c["signature"]]
    spread = (max(sig_dry) / min(sig_dry)) if sig_dry else 0.0
    # Separate readouts, deliberately not merged: how WIDE the true ratio
    # ranges across signature cells, and whether they all sit on one side of
    # 1.0. A wide spread with unanimous sign is non-diagnostic of magnitude
    # and diagnostic of direction, which is a different finding from "the
    # signature means nothing".
    below = sum(1 for x in sig_dry if x < 1.0)
    agreement = (below / len(sig_dry)) if sig_dry else None
    return {
        "signature_kWh_per_dry_min": min(sig_dry) if sig_dry else None,
        "signature_kWh_per_dry_max": max(sig_dry) if sig_dry else None,
        "signature_spread": spread,
        "signature_sign_agreement": agreement,
        "signature_cells_below_1": below,
        "base": base,
        "test": ref,
        "grid": grid,
        "signature_cells": sum(1 for c in grid if c["signature"]),
        "signature_no_dry_gain_cells": len(hits),
        "example_hit": hits[0] if hits else None,
        "kWh_per_g_dry_ratio": (ref["kWh"] / ref["dry_g"]) / (base["kWh"] / base["dry_g"]),
        "kWh_per_g_fresh_ratio": (ref["kWh"] / ref["fresh_g"]) / (base["kWh"] / base["fresh_g"]),
        "kWh_per_L_juice_ratio": (ref["kWh"] / ref["juice_L"]) / (base["kWh"] / base["juice_L"]),
        "notes": "ratio < 1.0 means the test regime is cheaper in that denominator",
    }


def _pchlide_run(duty, dark_block_h, days=6, dt=0.1,
                 k_syn=0.06, P_max=1.0, k_cat=0.50, Km=0.30,
                 K_light=0.60, I_on=1.0,
                 k_deg_light=0.002, k_deg_dark=0.012, **kw):
    """
    Shared engine for C2 (duty sweep) and C3 (dark-interval sweep).

      dP/dt   = k_syn * (1 - P/P_max)          <- FLU-clamped synthesis: the
                                                  clamp is ON POOL SIZE, so a
                                                  FULL pool SLOWS synthesis
                - v_conv
      v_conv  = k_cat * P/(P+Km) * I/(I+K_light)   <- POR is an enzyme: finite
                                                      turnover, saturates in
                                                      BOTH substrate and photons
      dChl/dt = v_conv - k_deg * Chl,  k_deg higher in dark

    Total photon dose is held CONSTANT across duty settings (I_eff = I_on/duty),
    so any difference is SCHEDULING, not dose.

    INSTRUMENT EDIT -- readout only, no mechanism or parameter changed.

    Chl is returned as the MEAN OVER THE FINAL COMPLETE PERIOD, not as the
    value at the last integration step. The endpoint reading is sampled at
    whatever phase the run happens to end on, and at duty=0.5 the period is
    2*dark_block, so a 144 h run ends mid-cycle for every block that does
    not divide it. Every arm that broke the monotonicity of the C3
    dark-interval curve was one of those; the cycle average is monotone.

    Registered as InstrumentEdit, not MechanismEdit: it removes a sampling
    artifact and changes no mechanism. It changes no verdict either -- C3
    tests for a sign flip and both readouts are negative throughout.
    """
    if duty <= 0.0:
        duty = 1e-6
    I_eff = I_on / duty
    period = dark_block_h / max(1e-9, (1.0 - duty)) if duty < 1.0 else 1.0
    P, Chl = P_max * 0.5, 0.10
    t = 0.0
    T = days * 24
    avg_from = max(0.0, T - period)
    acc, n = 0.0, 0
    for _ in range(int(T / dt)):
        phase = math.fmod(t, period) / period if period > 0 else 0.0
        lit = phase < duty
        I = I_eff if lit else 0.0
        v = k_cat * (P / (P + Km)) * (I / (I + K_light)) if lit else 0.0
        P = max(0.0, P + (k_syn * (1.0 - P / P_max) - v) * dt)
        Chl = max(0.0, Chl + (v - (k_deg_light if lit else k_deg_dark) * Chl) * dt)
        t += dt
        if t >= avg_from:
            acc += Chl
            n += 1
    return {"Chl": acc / max(n, 1), "Chl_endpoint": Chl, "P_final": P}


def s2_pool_charging(days=6, **kw):
    """
    S2 -- PCHLIDE POOL CHARGING under equal total photon dose.
    Sweeps duty cycle. Also locates the dark-interval crossover for C3.
    """
    duties = [round(0.05 * i, 2) for i in range(1, 21)]  # 0.05 .. 1.00
    curve = []
    for d in duties:
        r = _pchlide_run(duty=d, dark_block_h=4.0, days=days, **kw)
        curve.append((d, r["Chl"]))
    best_duty, best_chl = max(curve, key=lambda p: p[1])
    cont_chl = dict(curve)[1.0]

    # C3: dark-interval sweep at fixed duty -> find sign flip vs continuous
    blocks = [0.5, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24]
    dark_curve = []
    for b in blocks:
        r = _pchlide_run(duty=0.5, dark_block_h=float(b), days=days, **kw)
        dark_curve.append((float(b), r["Chl"] - cont_chl))
    crossover = None
    for i in range(1, len(dark_curve)):
        a, bb = dark_curve[i - 1][1], dark_curve[i][1]
        if a > 0.0 >= bb:
            crossover = dark_curve[i][0]
            break

    return {
        "duty_curve": curve,
        "best_duty": best_duty,
        "best_chl": best_chl,
        "continuous_chl": cont_chl,
        "gain_vs_continuous": (best_chl - cont_chl) / cont_chl if cont_chl else 0.0,
        "dark_interval_curve": dark_curve,
        "crossover_h": crossover,
        "notes": (
            "best_duty < 1.0 means intermittent dark beats continuous light at "
            "EQUAL total photon dose. crossover_h is where dark stops paying."
        ),
    }


def s3_index_artifact(days=6, steps=40, **kw):
    """
    S3 -- REFLECTANCE INDEX ARTIFACT, closed loop.

    index = a*Chl_area + b*water_frac + c*(1/thickness)

    A hill-climbing controller maximizes the INDEX by adjusting dark fraction.
    Truth (chlorophyll per dry gram) is computed but never shown to it.
    This is the same loop topology as the source system.
    """
    a, b, c = 1.00, 0.85, 0.25

    def state(dark_frac):
        duty = max(0.05, 1.0 - dark_frac)
        p = _pchlide_run(duty=duty, dark_block_h=6.0, days=days)
        m = s1_mass_denominator(dli_scale=max(0.10, duty))
        t = m["test"]
        water_frac = t["water_g"] / t["fresh_g"]
        thickness = 0.4 + 6.0 * t["wall_density"]
        chl_per_dry = p["Chl"] / max(t["dry_g"], 1e-9)
        chl_area = p["Chl"] / max(thickness, 1e-9)
        idx = a * chl_area + b * water_frac + c * (1.0 / thickness)
        return {"index": idx, "chl_per_dry": chl_per_dry,
                "water_frac": water_frac, "thickness": thickness,
                "chl": p["Chl"], "dry_g": t["dry_g"]}

    dark = 0.10
    s0 = state(dark)
    step = 0.06
    traj = [(dark, s0["index"], s0["chl_per_dry"])]
    cur = s0
    for _ in range(steps):
        cand = min(0.90, dark + step)
        sc = state(cand)
        if sc["index"] > cur["index"]:
            dark, cur = cand, sc
        else:
            step *= 0.5
            if step < 0.005:
                break
        traj.append((dark, cur["index"], cur["chl_per_dry"]))
    return {
        "trajectory": traj,
        "final_dark_frac": dark,
        "index_gain": (cur["index"] - s0["index"]) / s0["index"],
        "true_chl_gain": (cur["chl_per_dry"] - s0["chl_per_dry"]) / s0["chl_per_dry"],
        "notes": (
            "index_gain > 0 with true_chl_gain < 0 is proxy divergence: the "
            "controller improved its own reading and degraded the quantity."
        ),
    }


def s4_common_mode(bias=0.12, noise_seed=7, n_draws=400, **kw):
    """
    S4 -- CHANNEL COUNT vs COMMON-MODE BIAS.

    Independent per-channel noise averages down as 1/sqrt(N).
    A shared calibration bias does not. Deterministic LCG, no imports.
    """
    st = noise_seed

    def rnd():
        nonlocal st
        st = (1103515245 * st + 12345) % (1 << 31)
        return st / float(1 << 31) - 0.5

    def err(nch):
        tot = 0.0
        for _ in range(n_draws):
            est = sum((1.0 + bias + 0.30 * rnd()) for _ in range(nch)) / nch
            tot += abs(est - 1.0)
        return tot / n_draws

    e1, e49 = err(1), err(49)
    return {
        "err_1ch": e1,
        "err_49ch": e49,
        "reduction": 1.0 - e49 / e1,
        "bias_floor": bias,
        "notes": (
            "error floors at the shared bias regardless of channel count. "
            "Independence is a property of the calibration path, not of N."
        ),
    }


SIMS = {
    "S1": ("mass / denominator swap", s1_mass_denominator),
    "S2": ("Pchlide pool charging + dark crossover", s2_pool_charging),
    "S3": ("reflectance index artifact, closed loop", s3_index_artifact),
    "S4": ("channel count vs common-mode bias", s4_common_mode),
}


# ----------------------------------------------------------------------------
# 3. MECHANISM EDIT PROTOCOL
#    The only legal way to change a sim. Registers the prediction first.
# ----------------------------------------------------------------------------

FORBIDDEN_REASONS = [
    "claim failed", "to pass", "to match", "tune", "fit the data",
    "get the expected", "make it work", "align with paper",
]


class MechanismEdit(object):
    """
    An AI or person proposing a sim change must supply:
      mechanism   -- the physical process being added or corrected
      basis       -- an independent source for that process (not this run)
      prediction  -- what the edited sim will output, REGISTERED BEFORE RUNNING
      affects     -- which claim ids the edit could move
    """

    def __init__(self, sim_id, mechanism, basis, prediction, affects, reason=""):
        # Screen EVERY free-text field the caller supplies. Screening only
        # `reason` and `mechanism` left `basis` and `prediction` open, and
        # those are the two fields that ask for justification -- which is
        # where outcome reasoning goes when it is going anywhere.
        low = " ".join(str(x) for x in
                       (reason, mechanism, basis, prediction)).lower()
        for bad in FORBIDDEN_REASONS:
            if bad in low:
                raise ValueError(
                    "REFUSED: edit justified by outcome, not mechanism -> " + bad
                    + "\nRefutation protocol: update the claim, never retune the sim."
                )
        self.rec = {
            "kind": "MECHANISM_EDIT",
            "sim": sim_id,
            "mechanism": mechanism,
            "basis": basis,
            "prediction": prediction,
            "affects": affects,
            "registered_at": time.time(),
            "file_hash_before": self_hash(),
        }
        log(self.rec)

    def settle(self, observed, held):
        """
        `held` is REQUIRED and must be a bool: did the registered prediction
        hold. It used to default to None with a comment saying a human would
        fill it in, and nothing ever did -- so a registered prediction could
        be settled with the comparison never made, and the log would show a
        complete-looking record.

        Settling also requires that the file actually changed. The protocol
        exists to gate sim edits; an edit registered, settled and never
        performed was indistinguishable in the log from one carried out. Use
        abandon() for the case where the edit was decided against.
        """
        if not isinstance(held, bool):
            raise ValueError(
                "REFUSED: settle(observed, held) requires held=True|False. "
                "A registered prediction that is never adjudicated is not a "
                "registered prediction.")
        after = self_hash()
        if after == self.rec["file_hash_before"]:
            raise ValueError(
                "REFUSED: file hash unchanged, so no sim edit was made. "
                "Settling an edit that did not happen records it as one. "
                "Use abandon(reason) if the edit was decided against.")
        rec = dict(self.rec)
        rec["kind"] = "MECHANISM_EDIT_SETTLED"
        rec["observed"] = observed
        rec["file_hash_after"] = after
        rec["file_changed"] = True
        rec["prediction_held"] = held
        log(rec)
        return rec

    def abandon(self, reason):
        """Registered, then decided against. Logged, so the trail is intact."""
        rec = dict(self.rec)
        rec["kind"] = "MECHANISM_EDIT_ABANDONED"
        rec["abandon_reason"] = reason
        rec["file_hash_after"] = self_hash()
        rec["file_changed"] = rec["file_hash_after"] != rec["file_hash_before"]
        log(rec)
        return rec


class InstrumentEdit(object):
    """
    The edit category MechanismEdit does not cover.

    MechanismEdit gates changes to what the sim MODELS. A change to where a
    number is READ -- sampling phase, integration step, which statistic is
    returned -- changes sim output while changing no mechanism and no
    parameter, and the protocol had no category for it. That gap is the same
    one the provenance types already anticipate: REPORTED / PHYSICS / SIM /
    BENCH separates where a number came from, and generator / physical /
    instrument separates what a number is a property OF.

    An instrument edit must name the artifact it removes and the quantity
    that is unchanged by it. It does NOT take a prediction, because it is
    not a claim about the world -- if it changes a verdict, that is a
    finding about the old readout and goes in the claim table.
    """

    def __init__(self, sim_id, readout, artifact, unchanged, reason=""):
        low = " ".join(str(x) for x in
                       (reason, readout, artifact, unchanged)).lower()
        for bad in FORBIDDEN_REASONS:
            if bad in low:
                raise ValueError(
                    "REFUSED: readout change justified by outcome -> " + bad)
        self.rec = {
            "kind": "INSTRUMENT_EDIT",
            "sim": sim_id,
            "readout": readout,
            "artifact_removed": artifact,
            "unchanged_by_this": unchanged,
            "registered_at": time.time(),
            "file_hash_before": self_hash(),
        }
        log(self.rec)


# ----------------------------------------------------------------------------
# 4. HARNESS
# ----------------------------------------------------------------------------

def log(record):
    record.setdefault("t", time.time())
    record.setdefault("harness_version", VERSION)
    try:
        with open(LOGPATH, "a") as f:
            f.write(json.dumps(record, default=str) + "\n")
    except Exception:
        pass
    return record


def run_claim(cid, params=None, reasoning=""):
    claim = next(c for c in CLAIM_TABLE if c["id"] == cid)
    sim_id = claim["sim"]
    name, fn = SIMS[sim_id]
    params = params or {}
    t0 = time.time()
    out = fn(**params)
    try:
        held = bool(claim["predicate"](out))
        status = "SUPPORTED" if held else "REFUTED"
    except Exception as e:
        held, status = None, "UNDECIDED:" + str(e)
    rec = {
        "kind": "RUN",
        "claim": cid,
        "sim": sim_id,
        "sim_name": name,
        "source_of_claim": claim["source"],
        "params": params,
        "file_hash": self_hash(),
        "status": status,
        "elapsed_s": round(time.time() - t0, 3),
        "reasoning": reasoning,
        "output": {k: v for k, v in out.items() if k not in ("trajectory",)},
    }
    # The README puts the residual router in the pipeline --
    #   run -> provenance record -> residual router -> hypothesis block
    # -- and it was defined and never called. It attaches on the runs where
    # it is the point: a claim that did not hold, or one the predicate could
    # not decide. Four questions, unanswered by construction; the router
    # routes, it does not resolve.
    if held is not True:
        rec["residual_route"] = residual_route(rec, out)
    log(rec)
    return rec, out, claim


def residual_route(rec, out):
    """
    Residual router, same fork as field_claim_loop: before updating anything,
    ask which layer the difference lives in.
    """
    return {
        "instrument": "is the discrepancy in the sim's own numerics (dt, "
                      "integration, saturation form)?",
        "noise": "is it stochastic, and can that noise be read as a second "
                 "channel rather than discarded?",
        "novel": "is it outside the regime any parameter here was declared for?",
        "missing_variable": "is there an unmodelled cycle -- temperature, "
                            "nutrient, circadian phase, tissue age distribution "
                            "-- that would explain it without changing the "
                            "mechanism?",
    }


def record_bench(claim_id, quantity, value, units, method, kit, note=""):
    """
    Ingest a MEASURED value. SOURCE declares four provenance types and three
    of them had code paths; BENCH was declared and unreachable, so "empty
    until someone runs one" was true by absence rather than by construction.

    This does not merge with SIM. It is logged as its own kind, and
    bench_records() reads them back so a hypothesis block can say which
    claims have a physical exit and which do not.
    """
    if claim_id not in [c["id"] for c in CLAIM_TABLE]:
        raise ValueError("unknown claim id: " + str(claim_id))
    if not (isinstance(method, str) and method.strip()):
        raise ValueError(
            "REFUSED: a BENCH record needs a method. A number with no "
            "method is SIM provenance wearing a BENCH label.")
    return log({
        "kind": "BENCH",
        "claim": claim_id,
        "quantity": quantity,
        "value": value,
        "units": units,
        "method": method,
        "kit": kit,
        "note": note,
        "file_hash": self_hash(),
    })


def bench_records(path=None):
    """Every BENCH record in the log. Empty is the honest default."""
    path = path or LOGPATH
    out = []
    if not os.path.exists(path):
        return out
    try:
        with open(path) as f:
            for line in f:
                try:
                    r = json.loads(line)
                except Exception:
                    continue
                if r.get("kind") == "BENCH":
                    out.append(r)
    except Exception:
        pass
    return out


def run_id(results):
    """
    Deterministic identifier for a set of runs: the file hash plus the claim
    ids and statuses. hypothesis_block() used to stamp the wall clock into
    its header, one line above the file hash it prints for provenance, so
    two runs of the same file produced two different documents. The clock
    belongs in the log, where every record already carries one.
    """
    parts = [self_hash(), VERSION]
    for rec, _out, _claim in results:
        parts.append(rec["claim"] + ":" + rec["status"])
    return sha("|".join(parts))


def hypothesis_block(results):
    """
    Output for a human. Trajectory, not verdict.
    Confidence gradient and comfort threshold are SEPARATE readouts and are
    left for whoever runs this to set; nothing here resolves them.
    """
    lines = []
    lines.append("HYPOTHESIS BLOCK")
    lines.append("file hash: " + self_hash() + "   harness: " + VERSION)
    lines.append("run id:    " + run_id(results)
                 + "   (file hash + claim statuses; the clock is in the log)")
    lines.append("")
    lines.append("STATUS OF EACH CLAIM (from SIM only; no BENCH data exists yet)")
    KEY = {
        "C1": ["signature_cells", "signature_spread",
               "signature_kWh_per_dry_min", "signature_kWh_per_dry_max"],
        "C2": ["best_duty", "gain_vs_continuous"],
        "C3": ["crossover_h"],
        "C4": ["index_gain", "true_chl_gain"],
        "C5": ["err_1ch", "err_49ch", "reduction"],
    }
    for rec, out, claim in results:
        lines.append("  " + rec["claim"] + " [" + claim["source"] + "] -> "
                     + rec["status"])
        for k in KEY.get(rec["claim"], []):
            v = out.get(k)
            lines.append("        " + k + " = "
                         + (("%.4f" % v) if isinstance(v, float) else str(v)))
    lines.append("")
    bench = bench_records()
    have = sorted({b["claim"] for b in bench})
    lines.append("BENCH COVERAGE")
    if not bench:
        lines.append("  none. Every number above is SIM provenance.")
        lines.append("  `protocol` lists what a person with plants and a "
                     "scale would do;")
        lines.append("  `bench` records the result when they have.")
    else:
        lines.append("  %d record(s) across claims: %s"
                     % (len(bench), ", ".join(have)))
        for c in [x["id"] for x in CLAIM_TABLE]:
            mine = [b for b in bench if b["claim"] == c]
            lines.append("    %s  %s" % (c, ("%d measurement(s)" % len(mine))
                                         if mine else "no physical exit yet"))
    lines.append("")
    lines.append("WHAT THE SIM CANNOT SETTLE")
    lines.append("  Every number above is SIM provenance. A sim can show that an")
    lines.append("  artifact is SUFFICIENT to produce a reported signature. It")
    lines.append("  cannot show that the artifact is what happened.")
    lines.append("")
    lines.append("CONFIDENCE READOUT (fill separately, do not merge)")
    lines.append("  shape match:        ____ %")
    lines.append("  comfort threshold:  ____ %")
    lines.append("  state independently; a gradient is not a commitment.")
    lines.append("")
    lines.append("MEASUREMENTS THAT WOULD MOVE THIS -- see: protocol")
    return "\n".join(lines)


# ----------------------------------------------------------------------------
# 5. BENCH PROTOCOL -- what a person with plants and a scale actually does
# ----------------------------------------------------------------------------

BENCH = [
    ("C1", "dry matter",
     "Harvest both regimes at the same clock time. Fresh weight, then 65 C to "
     "constant mass (48-72 h). Report kWh/g DRY, not kWh/g fresh.",
     "scale (0.01 g), oven or dehydrator, kWh meter on the lamp circuit"),
    ("C1", "fiber",
     "NDF/ADF by detergent fiber, or ash-corrected crude fiber. Fiber fraction "
     "on a dry basis is the structural-carbon readout.",
     "lab service, or muffle/ash proxy"),
    ("C2/C3", "chlorophyll ground truth",
     "Solvent extraction (80% acetone or DMSO), read A645/A663, Arnon or "
     "Lichtenthaler equations. Report per g DRY, per g FRESH, and per leaf "
     "AREA -- all three. Their divergence is the result.",
     "spectrophotometer or a filtered-LED photometer"),
    ("C2", "substrate pool",
     "Sample at the END of a dark interval vs the end of a light interval. "
     "Protochlorophyllide by 77K fluorescence or HPLC. A pool that charges in "
     "dark and empties in light is the mechanism; a flat pool refutes it.",
     "77K fluorimeter or HPLC (service lab)"),
    ("C3", "crossover",
     "Dark-interval ladder at fixed duty: 1, 2, 4, 8, 12, 16 h blocks. Equal "
     "total photon dose in every arm. Find the sign flip.",
     "programmable driver, PAR quantum sensor to verify equal dose"),
    ("C4", "index vs truth",
     "Log the reflectance index and destructively sample the same tray. Plot "
     "index against extracted chlorophyll per dry gram. Divergence is the test.",
     "the same multispectral head + the extraction above"),
    ("C5", "independent stack",
     "Second sensor of different make/calibration path, same tissue, same hour. "
     "Common-mode bias only shows against a different instrument, never against "
     "more channels of the same one.",
     "any second instrument not from the first vendor"),
    ("ALL", "controls",
     "Concurrent periodic-control arm, same chamber, same seed lot, same water. "
     "Randomize tray position. Hold out untouched trays the controller cannot "
     "see or act on.",
     "seed lot record, tray map"),
]




# ----------------------------------------------------------------------------
# 5b. PENDING MECHANISM EDITS -- named, not yet run. Registering them here is
#     the alternative to quietly retuning a sim that came out the wrong way.
# ----------------------------------------------------------------------------

PENDING_EDITS = [
    {
        "sim": "S2",
        "mechanism": "shade acclimation: chlorophyll per unit leaf area rises "
                     "under low light via increased antenna/LHCII investment",
        "basis": "standard sun-vs-shade leaf acclimation literature; "
                 "independent of anything measured in this file",
        "prediction_to_register": "final chlorophyll PER LEAF AREA rises as "
                                  "mean irradiance falls, while chlorophyll per "
                                  "PLANT falls -- i.e. the denominator, again",
        "affects": ["C2", "C4"],
        "status": "UNRUN",
    },
    {
        "sim": "S2",
        "mechanism": "photoinhibition / POR photodamage at the high instantaneous "
                     "irradiance that equal-dose low-duty schedules require",
        "basis": "photoinhibition literature",
        "prediction_to_register": "penalises LOW duty further; widens the "
                                  "continuous-light advantage rather than "
                                  "reversing it",
        "affects": ["C2"],
        "status": "UNRUN",
    },
    {
        "sim": "S1",
        "mechanism": "tissue-age distribution: continuously emerging leaf blades "
                     "keep a young-tissue fraction with different wall density",
        "basis": "developmental gradient in monocot leaves",
        "prediction_to_register": "shifts wall density without changing the "
                                  "energy accounting",
        "affects": ["C1"],
        "status": "UNRUN",
    },
]


def cmd_pending():
    for e in PENDING_EDITS:
        print("[" + e["status"] + "] " + e["sim"] + " affects " + ",".join(e["affects"]))
        print("   mechanism : " + e["mechanism"])
        print("   basis     : " + e["basis"])
        print("   predicts  : " + e["prediction_to_register"])
        print("")


# ----------------------------------------------------------------------------
# 6. CLI
# ----------------------------------------------------------------------------

def fmt(x):
    if isinstance(x, float):
        return ("%.4f" % x)
    return str(x)


def cmd_claims():
    for c in CLAIM_TABLE:
        print("[" + c["id"] + "] sim=" + c["sim"] + "  source=" + c["source"])
        print("   claim: " + c["statement"])
        print("   test : " + c["test"])
        print("   reads: " + c["reads"].replace("\n", "\n          "))
        print("")


def cmd_run(ids):
    results = []
    for cid in ids:
        rec, out, claim = run_claim(cid)
        print("=" * 68)
        print(cid + "  [" + claim["source"] + "]  sim " + rec["sim"]
              + " -- " + rec["sim_name"])
        print("STATUS: " + rec["status"])
        for k, v in out.items():
            if k in ("duty_curve", "dark_interval_curve", "trajectory",
                     "base", "test", "grid"):
                continue
            print("   " + k.ljust(24) + " " + fmt(v))
        if "base" in out:
            for tag in ("base", "test"):
                print("   " + tag + ": " + ", ".join(
                    k + "=" + fmt(v) for k, v in out[tag].items()))
        print("")
        results.append((rec, out, claim))
    return results


def cmd_sweep(sim_id):
    if sim_id != "S2":
        print("sweep implemented for S2")
        return
    out = s2_pool_charging()
    mx = max(c for _, c in out["duty_curve"])
    print("duty  final Chl   (equal total photon dose in every row)")
    for d, c in out["duty_curve"]:
        bar = "#" * int(40 * c / max(1e-9, mx))
        print(" %.2f  %.5f  %s" % (d, c, bar))
    print("")
    print("dark block (h)   Chl minus continuous")
    for b, dv in out["dark_interval_curve"]:
        print("  %5.1f          %+.5f" % (b, dv))
    print("")
    print("best duty: %.2f   crossover: %s h"
          % (out["best_duty"], out["crossover_h"]))


def cmd_protocol():
    print("BENCH PROTOCOL -- each row turns a SIM claim into a BENCH measurement")
    print("")
    for cid, name, how, kit in BENCH:
        print("[" + cid + "] " + name)
        print("   do : " + how)
        print("   kit: " + kit)
        print("")


def cmd_log():
    if not os.path.exists(LOGPATH):
        print("no log yet at " + LOGPATH)
        return
    with open(LOGPATH) as f:
        for line in f:
            r = json.loads(line)
            print(r.get("kind", "?"), r.get("claim", r.get("sim", "")),
                  r.get("status", ""), r.get("file_hash", "")[:12])


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "run-all"
    if cmd == "claims":
        cmd_claims()
    elif cmd == "run-all":
        res = cmd_run([c["id"] for c in CLAIM_TABLE])
        print(hypothesis_block(res))
    elif cmd == "run":
        cmd_run(argv[2:])
    elif cmd == "sweep":
        cmd_sweep(argv[2] if len(argv) > 2 else "S2")
    elif cmd == "protocol":
        cmd_protocol()
    elif cmd == "hypothesis":
        res = []
        for c in CLAIM_TABLE:
            rec, out, claim = run_claim(c["id"])
            res.append((rec, out, claim))
        print(hypothesis_block(res))
    elif cmd == "pending":
        cmd_pending()
    elif cmd == "bench":
        if len(argv) < 8:
            print("usage: bench CLAIM QUANTITY VALUE UNITS METHOD KIT [NOTE]")
            print("  e.g. bench C1 kWh_per_g_dry 0.42 kWh/g "
                  "'65C to constant mass, 72h' 'scale 0.01g, kWh meter'")
            print("")
            print("A BENCH record is a MEASUREMENT. It never merges with SIM.")
            return
        r = record_bench(argv[2], argv[3], float(argv[4]), argv[5],
                         argv[6], argv[7],
                         argv[8] if len(argv) > 8 else "")
        print("recorded BENCH for " + r["claim"] + ": "
              + str(r["value"]) + " " + r["units"])
    elif cmd == "log":
        cmd_log()
    else:
        print(__doc__ or "")
        print("commands: claims run-all run <claim-id..> sweep S2 protocol "
              "bench pending hypothesis log")


if __name__ == "__main__":
    main(sys.argv)
