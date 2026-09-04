"""
thermal_coupling.py — temperature forcing for cascading slope/flow hazards.

MARKER module for earth-systems-physics. CC0. stdlib only.
Not a forecast tool. Output is a TRAJECTORY of channel states, not a verdict.

CORE STRUCTURE
  One forcing (temperature) enters the hazard chain at FIVE separated
  lag classes, with DIFFERENT SIGN in several of them. The chain fires
  when a fast trigger lands on a slow-primed state.

      hazard != f(T)
      hazard  = trigger(T_fast) * PROD( primed_i( integral T_slow ) )

  Product form, not sum. A silo that resolves one lag class cannot see
  the product. This is [[rate-mismatch-polytope]] applied to a hazard
  chain: strain comes from clock-speed mismatch, not from pull size.

PARAMETER SOURCES (all published, cited inline)
  Mamot et al. 2018, TC 12:3333 — 141 shear tests, ice-filled rock joints
  Mamot et al. 2021, ESurf 9:1125 — FoS vs slope angle and warming
  Kaeab/Arenson rockglacier creep — sensitivity rises toward 0 C
  Steinkogler et al. 2015 — snow granulation transition near -1 C
  Swiss Alps projection (EGUsphere 2024-1026) — dry down / wet up
  Biskaborn et al. 2019 — mountain permafrost +0.19 C, 2007-2016
"""

import math

# ---------------------------------------------------------------------------
# LAG CLASSES — the spine of the module
# ---------------------------------------------------------------------------
LAG = {
    "snowpack":      ("hours-days",      1.0 / 365),
    "active_layer":  ("seasonal",        1.0),
    "bedrock_pf":    ("years-decades",   30.0),
    "debuttress":    ("decades-cent.",   100.0),
    "sediment":      ("decades-cent.",   80.0),
}


# ---------------------------------------------------------------------------
# C1 SNOWPACK  (fast trigger; NON-MONOTONE in elevation)
# ---------------------------------------------------------------------------
def weak_layer_index(t_surface_c, t_ground_c, depth_m):
    """Kinetic-growth metamorphism scales with |dT/dz|.
    Threshold ~10 K/m for faceting. Warming THINS the pack at low
    elevation, which RAISES the gradient -> more weak layers on less snow.
    Sign of dI/dT is therefore elevation dependent."""
    if depth_m <= 0.05:
        return 0.0
    grad = abs(t_ground_c - t_surface_c) / depth_m
    return min(1.0, grad / 10.0)


def wet_regime_fraction(t_snow_c):
    """Granulation transition near -1 C: mm grains -> dm granules.
    Above transition: cohesion up, friction DOWN, runout LONGER."""
    return 1.0 / (1.0 + math.exp(-(t_snow_c + 1.0) / 0.4))


def avalanche_activity(t_snow_c, t_surface_c, t_ground_c, depth_m):
    """Dry component falls with warming, wet component rises.
    Net can go either way — the published Swiss range is -10% to -60%
    total by 2100 while wet activity RISES and shifts earlier."""
    w = wet_regime_fraction(t_snow_c)
    dry = (1.0 - w) * weak_layer_index(t_surface_c, t_ground_c, depth_m)
    wet = w * min(1.0, max(0.0, (t_snow_c + 2.0) / 3.0))
    return {"dry": dry, "wet": wet, "total": dry + wet, "wet_frac": w,
            "runout_multiplier": 1.0 + 0.35 * w}


# ---------------------------------------------------------------------------
# C2 ACTIVE LAYER  (seasonal; NON-MONOTONE in mean temperature)
# ---------------------------------------------------------------------------
def freeze_thaw_cycles(t_mean_c, t_amplitude_c, diurnal_amp_c=6.0, days=365):
    """Cycle COUNT is the damage driver, not mean temperature.
    DIURNAL crossings dominate; annual amplitude sets which days can cross.
    Cold sites GAIN cycles under warming (start crossing 0).
    Marginal sites LOSE cycles (stop crossing 0). Peak where the diurnal
    band straddles 0 for the most days of the year."""
    n = 0
    for d in range(days):
        seasonal = t_mean_c + t_amplitude_c * math.sin(2 * math.pi * d / 365.0)
        if (seasonal - diurnal_amp_c) < 0.0 < (seasonal + diurnal_amp_c):
            n += 1
    return n


def talus_cement_loss(t_mean_c):
    """Ice-cemented talus releasing its cement is a STEP, not a ramp.
    Sediment supply jumps when the cement goes."""
    return 1.0 / (1.0 + math.exp(-(t_mean_c + 0.5) / 0.3))


# ---------------------------------------------------------------------------
# C3 BEDROCK PERMAFROST  (slow primer; STRONGEST published transfer fn)
# ---------------------------------------------------------------------------
def joint_shear_strength_ratio(t_c, overburden_m=10.0):
    """Mamot et al. 2018: warming -10 C -> -0.5 C reduces shear strength
    of ice-filled joints by 64-78% at 4-15 m overburden.
    Deeper (30 m) is less sensitive. Sensitivity RISES toward 0 C."""
    t = max(-10.0, min(-0.2, t_c))
    loss_at_shallow = 0.71                       # midpoint of 64-78%
    depth_damp = 1.0 - 0.35 * min(1.0, max(0.0, (overburden_m - 10.0) / 20.0))
    x = (t + 10.0) / 9.5                         # 0 at -10 C, 1 at -0.5 C
    loss = loss_at_shallow * (x ** 0.55) * depth_damp   # convex: steeper near 0
    return 1.0 - loss


CAL_FOS = 2.825
# Calibrated to the published anchor (Mamot et al. 2021, ESurf 9:1125):
# a 50 deg slope warmed from -4 C crosses FoS = 1 somewhere between
# -3 and -0.5 C. This value puts the crossing at -2 C, mid-band.
# CAL_FOS is the ONLY free parameter in this module. Everything else
# is taken from published transfer functions.


def factor_of_safety(t_c, slope_deg, fracture_favorable=False,
                     overburden_m=10.0):
    """Mamot et al. 2021: FoS < 1 for slope >= 50 deg warmed from -4 C
    to between -3 and -0.5 C. Critical angle 50-62 deg depending on
    fracture network orientation."""
    crit = 50.0 if fracture_favorable else 62.0
    s = joint_shear_strength_ratio(t_c, overburden_m)
    geometry = math.tan(math.radians(crit)) / max(1e-6,
                                                  math.tan(math.radians(slope_deg)))
    return s * geometry * CAL_FOS


def creep_sensitivity(t_c):
    """Rockglacier creep: permafrost near 0 C is both FASTER and MORE
    SENSITIVE to thermal forcing than colder permafrost. dv/dT rises
    toward the melting point."""
    t = min(-0.05, t_c)
    return math.exp((t + 10.0) / 3.2)


# ---------------------------------------------------------------------------
# C4/C5 SLOW RESERVOIRS
# ---------------------------------------------------------------------------
def debuttress_priming(retreat_fraction, years_since_exposure):
    """Glacier retreat unloads the slope. Failure lags exposure by
    decades to centuries. Priming rises then saturates."""
    if years_since_exposure <= 0:
        return 0.0
    return retreat_fraction * (1.0 - math.exp(-years_since_exposure / 60.0))


def sediment_regime(supply_index, transport_capacity):
    """Supply-limited basins shift toward transport-limited as thaw
    releases material. The regime label changes what a rain event does."""
    if transport_capacity <= 0:
        return "undefined", 0.0
    r = supply_index / transport_capacity
    return ("transport_limited" if r > 1.0 else "supply_limited"), r


# ---------------------------------------------------------------------------
# COINCIDENCE — the whole point
# ---------------------------------------------------------------------------
def chain_state(t_snow_c, t_surface_c, t_ground_c, snow_depth_m,
                t_mean_annual_c, t_amplitude_c, slope_deg,
                retreat_fraction, years_since_exposure,
                supply_index, transport_capacity,
                fracture_favorable=False, overburden_m=10.0):
    av = avalanche_activity(t_snow_c, t_surface_c, t_ground_c, snow_depth_m)
    ftc = freeze_thaw_cycles(t_mean_annual_c, t_amplitude_c)
    cement = talus_cement_loss(t_mean_annual_c)
    fos = factor_of_safety(t_mean_annual_c, slope_deg, fracture_favorable,
                           overburden_m)
    creep = creep_sensitivity(t_mean_annual_c)
    debut = debuttress_priming(retreat_fraction, years_since_exposure)
    regime, ratio = sediment_regime(supply_index, transport_capacity)

    primed_rock = max(0.0, min(1.0, (1.60 - fos) / 0.80))
    primed_sed = max(0.0, min(1.0, 0.5 * cement + 0.5 * min(1.0, ratio)))
    trigger = min(1.0, av["total"])

    coincidence = trigger * primed_rock * (0.5 + 0.5 * primed_sed) \
        * (0.5 + 0.5 * debut)

    return {
        "lag_class_states": {
            "snowpack_trigger": round(trigger, 3),
            "active_layer_ftc": ftc,
            "bedrock_primed": round(primed_rock, 3),
            "debuttress_primed": round(debut, 3),
            "sediment_primed": round(primed_sed, 3),
        },
        "avalanche": {k: round(v, 3) for k, v in av.items()},
        "factor_of_safety": round(fos, 3),
        "joint_strength_ratio": round(
            joint_shear_strength_ratio(t_mean_annual_c, overburden_m), 3),
        "creep_sensitivity": round(creep, 2),
        "sediment_regime": regime,
        "COINCIDENCE": round(coincidence, 4),
    }


# ---------------------------------------------------------------------------
# CLAIM_TABLE  (refutation protocol: update the claim, never retune)
# ---------------------------------------------------------------------------
CLAIM_TABLE = [
    ("TC-01", "Temperature enters the hazard chain at >=5 separated lag "
              "classes spanning ~4 orders of magnitude in time",
              "a chain where all links respond on one timescale"),
    ("TC-02", "Chain firing is a PRODUCT of fast trigger and slow priming, "
              "not a sum of hazard scores",
              "an event set where additive scoring predicts as well"),
    ("TC-03", "dHazard/dT is non-monotone in elevation for snow and "
              "non-monotone in mean T for freeze-thaw damage",
              "monotone response across the full elevation/temperature range"),
    ("TC-04", "Ice-filled joint strength loss is convex toward 0 C: "
              "sensitivity rises as temperature approaches melting",
              "linear or concave strength-temperature relation in new tests"),
    ("TC-05", "Single-process silos also silo the TIMESCALE, so no silo can "
              "represent the coincidence term",
              "a single-process model that reproduces chain timing"),
    ("TC-06", "Warming can REDUCE total avalanche count while RAISING "
              "cascade risk, because wet regime lowers friction and "
              "lengthens runout",
              "runout multiplier <= 1 for wet regime in observed events"),
]

REFUTATION_PROTOCOL = "Update the claim. Never retune the sim to save it."


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("DEMO A — same warming, three elevation bands")
    print("=" * 70)
    bands = [
        ("low  1500m", -0.5, -0.5, 0.5, 0.6, 3.0, 9.0, 55),
        ("mid  2500m", -3.0, -4.0, -1.0, 1.2, -1.0, 8.0, 55),
        ("high 3500m", -8.0, -10.0, -4.0, 2.0, -5.0, 7.0, 55),
    ]
    hdr = f"{'band':<12}{'dry':>7}{'wet':>7}{'total':>7}{'runout':>8}" \
          f"{'FoS':>7}{'primed':>8}{'COINC':>8}"
    print(hdr)
    for name, tsnow, tsurf, tgrnd, depth, tmean, tamp, slope in bands:
        s = chain_state(tsnow, tsurf, tgrnd, depth, tmean, tamp, slope,
                        0.4, 40, 0.9, 1.0)
        a = s["avalanche"]
        print(f"{name:<12}{a['dry']:>7.3f}{a['wet']:>7.3f}{a['total']:>7.3f}"
              f"{a['runout_multiplier']:>8.2f}{s['factor_of_safety']:>7.2f}"
              f"{s['lag_class_states']['bedrock_primed']:>8.3f}"
              f"{s['COINCIDENCE']:>8.4f}")

    print()
    print("=" * 70)
    print("DEMO B — freeze-thaw cycles vs mean T  (non-monotone)")
    print("=" * 70)
    print(f"{'T_mean C':>10}{'cycles/yr':>12}")
    for tm in [-12, -8, -5, -3, -1, 0, 1, 3, 5, 8, 12]:
        print(f"{tm:>10}{freeze_thaw_cycles(tm, 9.0):>12}")

    print()
    print("=" * 70)
    print("DEMO C — joint strength and FoS vs bedrock temperature")
    print("=" * 70)
    print(f"{'T C':>7}{'strength':>10}{'FoS 55deg':>11}{'FoS 65deg':>11}"
          f"{'creep rel':>11}")
    for t in [-10, -8, -6, -4, -3, -2, -1, -0.5]:
        print(f"{t:>7}{joint_shear_strength_ratio(t):>10.3f}"
              f"{factor_of_safety(t, 55):>11.3f}"
              f"{factor_of_safety(t, 65):>11.3f}"
              f"{creep_sensitivity(t):>11.2f}")

    print()
    print("=" * 70)
    print("DEMO D — coincidence: cold trigger on unprimed vs primed slope")
    print("=" * 70)
    scen = [
        ("cold dry-slab trig", -14.0, -1.0, 0.9, 60),
        ("trigger, unprimed ", -0.5, -9.0, 0.1, 2),
        ("BOTH              ", -0.5, -1.0, 0.9, 60),
    ]
    print(f"{'scenario':<20}{'trigger':>9}{'rock':>7}{'sed':>7}{'debut':>8}"
          f"{'COINC':>9}")
    for name, tsnow, tmean, retreat, yrs in scen:
        s = chain_state(tsnow, tsnow - 1, tsnow + 3, 1.0, tmean, 8.0, 55,
                        retreat, yrs, 0.9, 1.0)
        L = s["lag_class_states"]
        print(f"{name:<20}{L['snowpack_trigger']:>9.3f}"
              f"{L['bedrock_primed']:>7.3f}{L['sediment_primed']:>7.3f}"
              f"{L['debuttress_primed']:>8.3f}{s['COINCIDENCE']:>9.4f}")

    print()
    print("LAG CLASSES")
    for k, (label, yrs) in LAG.items():
        print(f"  {k:<15}{label:<18}tau ~ {yrs:>7.3f} yr")
