#!/usr/bin/env python3
# thermal_sensor_degradation_audit.py -- CC0, stdlib-only
# Sustained-heat degradation audit for sensor packages on automated
# infrastructure. Dissimilar-material mounting, polymer/gasket creep,
# electronic drift, wet-bulb corrosion pathways.
# Refutation protocol: every model returns a falsifiable prediction,
# not a stored verdict. Update the claim, never retune the sim.

import math

# ---------------------------------------------------------------
# LAYER 1: MATERIAL PROPERTIES (engineering handbook ranges)
# cte: coefficient of thermal expansion, 1e-6 / K
# t_service_c: continuous service temp ceiling, C
# creep_onset_c: temp where time-dependent deformation accelerates
# ---------------------------------------------------------------
MATERIALS = {
    "steel_1018":      {"cte": 11.7, "t_service_c": 400, "creep_onset_c": 370},
    "stainless_304":   {"cte": 17.3, "t_service_c": 425, "creep_onset_c": 400},
    "aluminum_6061":   {"cte": 23.6, "t_service_c": 200, "creep_onset_c": 150},
    "concrete":        {"cte": 10.0, "t_service_c": 300, "creep_onset_c": 200},
    "asphalt":         {"cte": 35.0, "t_service_c": 60,  "creep_onset_c": 45},
    "abs_plastic":     {"cte": 90.0, "t_service_c": 80,  "creep_onset_c": 70},
    "nylon_66":        {"cte": 80.0, "t_service_c": 105, "creep_onset_c": 90},
    "polycarbonate":   {"cte": 68.0, "t_service_c": 115, "creep_onset_c": 100},
    "pvc":             {"cte": 60.0, "t_service_c": 60,  "creep_onset_c": 50},
    "epdm_rubber":     {"cte": 160.0,"t_service_c": 130, "creep_onset_c": 100},
    "nitrile_rubber":  {"cte": 110.0,"t_service_c": 100, "creep_onset_c": 80},
    "silicone_rubber": {"cte": 300.0,"t_service_c": 200, "creep_onset_c": 180},
    "fr4_pcb":         {"cte": 14.0, "t_service_c": 130, "creep_onset_c": 120},
    "solder_sac305":   {"cte": 21.0, "t_service_c": 150, "creep_onset_c": 100},
    "epoxy_potting":   {"cte": 55.0, "t_service_c": 130, "creep_onset_c": 110},
}

def f_to_c(f): return (f - 32.0) * 5.0 / 9.0

# ---------------------------------------------------------------
# LAYER 2: WET BULB (Stull 2011 approximation, valid 5-99% RH)
# t_c: dry bulb C, rh: relative humidity percent
# ---------------------------------------------------------------
def wet_bulb_c(t_c, rh):
    tw = (t_c * math.atan(0.151977 * math.sqrt(rh + 8.313659))
          + math.atan(t_c + rh) - math.atan(rh - 1.676331)
          + 0.00391838 * rh**1.5 * math.atan(0.023101 * rh)
          - 4.686035)
    return tw

# ---------------------------------------------------------------
# LAYER 3: SURFACE TEMP AMPLIFICATION
# Black/dark surfaces in full sun exceed air temp substantially.
# solar_w_m2: incident shortwave, wind_ms: convective relief
# Empirical envelope: asphalt runs +20 to +30C over air in full sun.
# ---------------------------------------------------------------
def surface_temp_c(air_c, absorptivity=0.90, solar_w_m2=1000.0, wind_ms=1.0):
    # simple radiative-convective balance, lumped
    h_conv = 5.7 + 3.8 * wind_ms            # W/m2K, flat plate empirical
    delta = (absorptivity * solar_w_m2) / (h_conv + 5.0)  # +5 radiative loss
    return air_c + delta

# ---------------------------------------------------------------
# LAYER 4: DIFFERENTIAL EXPANSION STRESS ACROSS A BOLTED PAIR
# Two materials clamped over span_mm, cycled delta_t.
# Returns mismatch strain (microstrain) and displacement (um).
# Rule-of-thumb flags: >500 microstrain repeated = fastener
# loosening / fretting risk; >1000 = joint redesign territory.
# ---------------------------------------------------------------
def pair_mismatch(mat_a, mat_b, span_mm, delta_t_k):
    cte_a = MATERIALS[mat_a]["cte"]
    cte_b = MATERIALS[mat_b]["cte"]
    d_cte = abs(cte_a - cte_b)                    # 1e-6 / K
    microstrain = d_cte * delta_t_k               # dimensionless *1e-6
    disp_um = d_cte * delta_t_k * span_mm / 1000.0
    if microstrain > 1000: flag = "RED"
    elif microstrain > 500: flag = "YELLOW"
    else: flag = "GREEN"
    return {"pair": [mat_a, mat_b], "d_cte_1e6K": round(d_cte, 1),
            "microstrain": round(microstrain, 0),
            "displacement_um": round(disp_um, 1), "flag": flag,
            "falsify": ("measure fastener torque loss and fretting "
                        "wear on this joint after 30 thermal cycles; "
                        "GREEN pairs should show <5% torque loss")}


# ---------------------------------------------------------------
# LAYER 5: GASKET / POLYMER COMPRESSION SET (Arrhenius-accelerated)
# Compression set = permanent deformation fraction after sustained
# clamp at temp. Base rates from elastomer handbook envelopes at
# reference 70C; each +10C roughly doubles rate (Q10 ~= 2).
# days at temp -> set fraction (0..1). >0.4 = seal integrity gone.
# ---------------------------------------------------------------
GASKET_BASE_SET_PER_DAY = {   # at 70C reference
    "epdm_rubber": 0.004, "nitrile_rubber": 0.008,
    "silicone_rubber": 0.002, "pvc": 0.010,
}

def compression_set(material, temp_c, days, q10=2.0, ref_c=70.0):
    base = GASKET_BASE_SET_PER_DAY.get(material)
    if base is None:
        return {"material": material, "note": "no gasket model"}
    accel = q10 ** ((temp_c - ref_c) / 10.0)
    setf = min(1.0, base * accel * days)
    if setf > 0.4: flag = "RED"
    elif setf > 0.2: flag = "YELLOW"
    else: flag = "GREEN"
    return {"material": material, "temp_c": temp_c, "days": days,
            "set_fraction": round(setf, 3), "flag": flag,
            "falsify": ("pull gasket after exposure window, measure "
                        "recovered thickness vs original; model claims "
                        f"~{round(setf*100)}% permanent set")}

# ---------------------------------------------------------------
# LAYER 6: ELECTRONIC DRIFT (Arrhenius, Ea ~= 0.7 eV typical
# semiconductor/electrolytic aging). Drift multiplier vs 25C rating.
# Sustained 50C internal = ~7x aging; 70C = ~30x+.
# Enclosure adds +10 to +25C over ambient in sun.
# ---------------------------------------------------------------
K_B = 8.617e-5  # eV/K

def aging_multiplier(temp_c, ea_ev=0.7, ref_c=25.0):
    """Arrhenius aging acceleration vs the reference temperature.

    IMPORTANT: pass the sensor's INTERNAL temperature — enclosure air
    inside the box, not ambient outdoor air. A dark enclosure in sun
    typically runs 10-25 C above ambient; `sensor_drift` handles this
    by adding `enclosure_rise_c` before calling this function. If you
    call `aging_multiplier(ambient)` directly you'll silently
    underestimate aging by the enclosure-rise factor.
    """
    t1, t0 = temp_c + 273.15, ref_c + 273.15
    return math.exp((ea_ev / K_B) * (1.0/t0 - 1.0/t1))

def sensor_drift(air_c, enclosure_rise_c, rated_drift_pct_yr, days):
    internal_c = air_c + enclosure_rise_c
    mult = aging_multiplier(internal_c)
    drift = rated_drift_pct_yr * mult * (days / 365.0)
    if drift > 2.0: flag = "RED"
    elif drift > 0.5: flag = "YELLOW"
    else: flag = "GREEN"
    return {"internal_c": round(internal_c, 1),
            "aging_multiplier_vs_25C": round(mult, 1),
            "projected_drift_pct": round(drift, 2), "flag": flag,
            "falsify": ("co-locate reference-grade sensor for the "
                        "exposure window; divergence should track "
                        "projected drift within 2x")}

# ---------------------------------------------------------------
# LAYER 7: MEASUREMENT CORRUPTION SIGNATURE
# Core TAF claim: corruption(trend) = corruption(measurement)
#                 x corruption(framework), multiplicative.
# Heat events degrade sensors DURING the events they measure, so
# extreme readings bias LOW exactly at the tail. Signature:
# variance collapse + clipped maxima + post-event step offset.
# ---------------------------------------------------------------
def _percentile_range(xs, lo_pct=5, hi_pct=95):
    """Spread between the lo/hi percentiles of xs. Robust to a single
    outlier at either end (which raw min/max was not).

    SCOPE: len(xs) >= 3 for the percentile idea to bite; below that the
    percentile indexes collapse to min/max and the check degrades
    gracefully to the old behaviour.
    """
    ordered = sorted(xs)
    n = len(ordered)
    lo_i = int(lo_pct / 100.0 * (n - 1))
    hi_i = int(hi_pct / 100.0 * (n - 1))
    return ordered[hi_i] - ordered[lo_i]


def corruption_signature(readings_before, readings_during):
    def var(xs):
        m = sum(xs)/len(xs)
        return sum((x-m)**2 for x in xs)/len(xs)
    v0, v1 = var(readings_before), var(readings_during)
    variance_collapse = v1 < 0.5 * v0
    # Percentile-based range comparison (5th/95th) so a single outlier
    # in `readings_before` cannot defeat the clipping check.
    clipped = _percentile_range(readings_during) < 0.5 * _percentile_range(readings_before)
    return {"variance_collapse": variance_collapse,
            "range_clipping": clipped,
            "read": ("LOW-BIAS LIKELY: extreme-event record "
                     "understates true tail" if (variance_collapse
                     and clipped) else "no corruption signature"),
            "falsify": ("independent mobile reference traverse during "
                        "heat event; fixed-network tail should read "
                        "low vs traverse if signature is real")}

# ---------------------------------------------------------------
# AUDIT DRIVER: one call, whole package verdict
# ---------------------------------------------------------------
def audit(air_f, rh_pct, days, pairs, gaskets, enclosure_rise_c=15.0,
          rated_drift_pct_yr=0.25, readings_before=None, readings_during=None):
    """One-call package verdict. Worst flag across L4/L5/L6 wins.

    If both `readings_before` and `readings_during` are supplied, the L7
    corruption-signature check runs and joins the flag aggregation: a
    signature-positive read (variance collapse + range clipping) fires
    RED, since the entire package record is then low-biased regardless
    of what the individual layer flags say.
    """
    air_c = f_to_c(air_f)
    tw = wet_bulb_c(air_c, rh_pct)
    surf = surface_temp_c(air_c)
    out = {"air_c": round(air_c,1), "wet_bulb_c": round(tw,1),
           "surface_c_full_sun": round(surf,1),
           "human_limit_note": "wet bulb >31C = severe human risk; "
                               "field maintenance window closes",
           "pairs": [pair_mismatch(a, b, span, surf - 20.0)
                     for (a, b, span) in pairs],
           "gaskets": [compression_set(g, surf, days) for g in gaskets],
           "electronics": sensor_drift(air_c, enclosure_rise_c,
                                       rated_drift_pct_yr, days)}
    flags = ([p["flag"] for p in out["pairs"]] +
             [g.get("flag","GREEN") for g in out["gaskets"]] +
             [out["electronics"]["flag"]])
    if readings_before is not None and readings_during is not None:
        corr = corruption_signature(readings_before, readings_during)
        out["corruption"] = corr
        # L7 headline: a positive signature means the record itself
        # is likely low-biased. That's RED for record trustworthiness
        # even if the physical-layer flags happen to be green.
        if corr["variance_collapse"] and corr["range_clipping"]:
            flags.append("RED")
    out["verdict"] = ("RED" if "RED" in flags else
                      "YELLOW" if "YELLOW" in flags else "GREEN")
    return out

if __name__ == "__main__":
    import json
    # Heat dome case: 110F air, 45% RH, 45 days sustained
    result = audit(air_f=110, rh_pct=45, days=45,
                   pairs=[("aluminum_6061", "abs_plastic", 150),
                          ("steel_1018", "nylon_66", 100),
                          ("concrete", "steel_1018", 300)],
                   gaskets=["epdm_rubber", "nitrile_rubber"])
    print(json.dumps(result, indent=1))
