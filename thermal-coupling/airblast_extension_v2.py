"""
airblast_extension.py — corrections to thermal_coupling.py forced by the
Langtang 2015 reconstruction.

CC0. stdlib only. Extends thermal_coupling.py, does not replace it.

SOURCE
  Zhuang, Dawadi, Steiner, Dash, Buehler, Munch & Bartelt (2024),
  Commun Earth Environ 5:465, doi 10.1038/s43247-024-01624-z
  RAMMS::RockIce. SLF Davos.

WHAT THIS FIXES IN thermal_coupling.py
  F1. The module used SNOWPACK temperature as the thermal driver.
      The paper states ambient AIR temperature can matter MORE than
      snowpack temperature for meltwater and runout. Existing rock-ice
      models treat the sliding mass as thermally insulated; that is the
      gap the paper closes. My C1 used the weaker variable.
  F2. The module had NO air blast term at all. At Langtang the core
      never reached the village. The air blast killed 350+ people
      OUTSIDE the core footprint. Every runout-based term I wrote is
      blind to the lethal area.
  F3. The module's fastest lag class was hours-days. Langtang occurred
      at noon; the paper states a night event would have produced a
      smaller runout and impact area. DIURNAL is a real lag class,
      one order faster than anything the module had.

NEW TERM THE PAPER SUPPLIES
  Heat transfer scales as r^-1.5 to r^-2.0 in particle radius.
  snow r=7cm, ice r=10cm, rock r=30cm
  -> snow exchanges heat with air at 8.9-18.4x rock, same volume.
  So SNOW FRACTION is the thermal coupling coefficient between the
  moving mass and the atmosphere. At Langtang snow was >70% of volume.
"""

import math

# ---------------------------------------------------------------------------
# LAG CLASSES, revised
# ---------------------------------------------------------------------------
LAG = {
    "diurnal":       ("hours",           1.0 / 8760),   # NEW (F3)
    "snowpack":      ("hours-days",      1.0 / 365),
    "active_layer":  ("seasonal",        1.0),
    "bedrock_pf":    ("years-decades",   30.0),
    "debuttress":    ("decades-cent.",   100.0),
    "sediment":      ("decades-cent.",   80.0),
}

# Langtang anchors
PARTICLE_R = {"snow": 0.07, "ice": 0.10, "rock": 0.30}   # m
LETHAL_KPA = 1.0        # blows a human to the ground
HOUSE_KPA = 15.0        # stone-slab houses flattened at Langtang


# ---------------------------------------------------------------------------
# F1 + new term: ambient-air coupling weighted by snow fraction
# ---------------------------------------------------------------------------
def thermal_coupling_coefficient(f_snow, f_ice, f_rock, exponent=1.75):
    """Heat transfer ~ r^-1.5 to r^-2.0. Normalize to rock = 1.0.
    Returns the volume-weighted exchange rate relative to an all-rock mass."""
    tot = f_snow + f_ice + f_rock
    if tot <= 0:
        return 0.0
    ref = PARTICLE_R["rock"] ** -exponent
    w = (f_snow * PARTICLE_R["snow"] ** -exponent
         + f_ice * PARTICLE_R["ice"] ** -exponent
         + f_rock * PARTICLE_R["rock"] ** -exponent) / tot
    return w / ref


def meltwater_index(t_air_c, f_snow, f_ice, f_rock, duration_s=180.0,
                    t_ref_c=-1.0):
    """Relative meltwater production, normalized to the -1 C case = 1.0.

    CORRECTED FORM. A first attempt used melt ~ k * (T_air - T_core),
    linear in ambient. That returns a -1 C -> +19 C ratio of 6.0 against
    the published 2.3 — wrong by 2.6x.

    Why: frictional shearing supplies the BASELINE melt. Ambient air is
    a MODIFIER on top of it, and the driving dT collapses as the core
    warms toward T_melt (the model caps core temperature at melting).
    So:
        melt = M_friction + c * k_coupling * (T_air - T_ref)

    Calibrated to the published pair:
        74,000 t at -1 C  ->  170,000 t at +19 C   (ratio 2.30)
        slope ~ 4,800 t per K of air temperature on a 74,000 t base
    """
    k = thermal_coupling_coefficient(f_snow, f_ice, f_rock)
    k_langtang = thermal_coupling_coefficient(0.72, 0.20, 0.08)
    ambient_gain = 0.0649 * (k / k_langtang)      # per K, normalized
    return (1.0 + ambient_gain * (t_air_c - t_ref_c)) * (duration_s / 180.0)


def friction_from_water(m_w, mu_dry=0.32, mu_min=0.09, m_0=1.0):
    """Vera Valero et al. 2018 rheology as used in the paper:
       mu_w = mu_min + (mu_dry - mu_min) * exp(-m_w / m_0)
    Ever-decreasing Coulomb resistance with increasing water content."""
    return mu_min + (mu_dry - mu_min) * math.exp(-m_w / m_0)


# ---------------------------------------------------------------------------
# F2: air blast footprint — the term the core module lacked entirely
# ---------------------------------------------------------------------------
def powder_cloud_pressure(u_core_ms, snow_entrained_frac, rho_cloud=8.0,
                          turbulence_magnification=1.9):
    """Mean and peak dynamic pressure of the powder cloud.
    P = 0.5 * rho_cloud * u^2, with turbulent fluctuation magnifying peak.
    Langtang anchor: mean >15 kPa and peak 28 kPa at the village
    (peak/mean ~1.9), 10 kPa mean / 18 kPa peak at the opposite toe."""
    u_cloud = u_core_ms * (0.55 + 0.45 * snow_entrained_frac)
    mean_kpa = 0.5 * rho_cloud * u_cloud ** 2 / 1000.0
    return {"mean_kPa": mean_kpa,
            "peak_kPa": mean_kpa * turbulence_magnification,
            "u_cloud_ms": u_cloud}


def blast_footprint_km2(mean_kpa, threshold_kpa=LETHAL_KPA):
    """Crude scaling of destructive area with overpressure above threshold.
    Langtang anchor: 0.8 km2 tree breakage, 1 km up and down valley,
    550 m up the opposite mountain, at ~10 kPa mean on that slope."""
    if mean_kpa <= threshold_kpa:
        return 0.0
    return 0.8 * (mean_kpa / 10.0) ** 1.5


def lethal_area_outside_core(mean_kpa, core_area_km2):
    """THE STRUCTURAL POINT: at Langtang the core never reached the
    village. Runout-based hazard maps bound the core. This returns the
    area that is lethal but OUTSIDE any core-based boundary."""
    return max(0.0, blast_footprint_km2(mean_kpa) - core_area_km2)


# ---------------------------------------------------------------------------
# F3: diurnal gate
# ---------------------------------------------------------------------------
def diurnal_air_temp(t_mean_c, diurnal_amp_c, hour):
    """Warmest mid-afternoon, coldest pre-dawn. Langtang fired at 11:56."""
    return t_mean_c + diurnal_amp_c * math.sin(2 * math.pi * (hour - 9.0) / 24.0)


# ---------------------------------------------------------------------------
# CLAIM_TABLE additions
# ---------------------------------------------------------------------------
CLAIM_TABLE_ADD = [
    ("TC-07", "Ambient AIR temperature can dominate snowpack temperature "
              "as the thermal driver of runout; treating the mass as "
              "thermally insulated removes the larger term",
              "a case where snowpack temperature dominates ambient in a "
              "coupled run"),
    ("TC-08", "Snow fraction is the thermal coupling coefficient between "
              "a moving mass and the atmosphere (heat transfer ~ r^-1.5 "
              "to r^-2.0; snow 8.9-18.4x rock by volume)",
              "measured exchange independent of grain size"),
    ("TC-09", "The lethal footprint of a rock-ice avalanche can lie "
              "entirely OUTSIDE the core runout, so runout-bounded hazard "
              "maps omit the fatality area",
              "an event set where fatalities fall inside the core boundary"),
    ("TC-10", "Deep snow and warm air raise lethality by DIFFERENT "
              "mechanisms and extend the footprint in different "
              "directions: entrainment/dispersion extends it laterally "
              "via blast, meltwater lubrication extends it longitudinally "
              "via runout",
              "the two channels producing the same footprint change"),
    ("TC-11", "Hour of day is a lag class: the same release at night "
              "produces materially smaller runout and impact area",
              "no diurnal dependence in a controlled reconstruction"),
]


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print("LANGTANG ANCHOR — published values")
    print("=" * 70)
    print("  released ice           3.50e6 m3   (above 6000 m asl)")
    print("  total volume          14.38e6 m3   (78% ENTRAINED en route)")
    print("  snow share of volume     >70%")
    print("  max core velocity        >90 m/s")
    print("  velocity at far toe       57 m/s")
    print("  village hit by CORE?       NO")
    print("  deaths                   >350   (air blast)")
    print("  village blast     mean >15 kPa, peak 28 kPa")
    print("  far slope         mean  10 kPa, peak 18 kPa")
    print("  tree breakage           0.8 km2, 1 km up+down valley")
    print()

    print("=" * 70)
    print("F2 — snow entrainment sweep vs published (temperature fixed)")
    print("=" * 70)
    print(f"{'snow @ release':>16}{'mean kPa':>11}{'peak kPa':>11}"
          f"{'blast km2':>12}{'published':>26}")
    pub = {0.0: "core stops short, 2.5 kPa",
           3.0: "matches observed, >15 kPa"}
    for depth in [0.0, 1.0, 2.0, 3.0]:
        frac = depth / 3.0
        p = powder_cloud_pressure(57.0, frac)
        print(f"{depth:>13.1f} m{p['mean_kPa']:>11.1f}{p['peak_kPa']:>11.1f}"
              f"{blast_footprint_km2(p['mean_kPa']):>12.2f}"
              f"{pub.get(depth,''):>26}")
    print()

    print("=" * 70)
    print("F1 — ambient air sweep (snow fixed), meltwater relative")
    print("=" * 70)
    print(f"{'T_air @3862m':>13}{'melt idx':>10}{'ratio':>8}{'mu_w':>8}"
          f"{'published':>26}")
    base = 1.0
    pubm = {-1.0: "74,000 t, 600 mm/m3",
            9.0: "actual event",
            19.0: "170,000 t, >1800 mm/m3"}
    for t in [-1.0, 4.0, 9.0, 14.0, 19.0]:
        m = meltwater_index(t, 0.72, 0.20, 0.08)
        print(f"{t:>13.0f}{m:>10.1f}{m/base:>8.2f}"
              f"{friction_from_water(m):>8.3f}{pubm.get(t,''):>26}")
    print("  published meltwater ratio -1 C -> 19 C : 2.30")
    print()

    print("=" * 70)
    print("TC-08 — thermal coupling by composition")
    print("=" * 70)
    print(f"{'composition':<28}{'coupling vs all-rock':>22}")
    for name, (s, i, r) in {
        "all rock":            (0.0, 0.0, 1.0),
        "rock-ice, no snow":   (0.0, 0.5, 0.5),
        "Langtang (>70% snow)": (0.72, 0.20, 0.08),
        "all snow":            (1.0, 0.0, 0.0),
    }.items():
        print(f"{name:<28}{thermal_coupling_coefficient(s,i,r):>22.1f}")
    print()

    print("=" * 70)
    print("TC-09 — lethal area outside a runout-bounded map")
    print("=" * 70)
    core = 0.35
    print(f"  assumed core deposit footprint: {core} km2")
    print(f"{'snow @ release':>16}{'blast km2':>12}{'OUTSIDE core':>15}"
          f"{'ratio':>8}")
    for depth in [0.0, 1.0, 2.0, 3.0]:
        p = powder_cloud_pressure(57.0, depth / 3.0)
        b = blast_footprint_km2(p["mean_kPa"])
        out = lethal_area_outside_core(p["mean_kPa"], core)
        print(f"{depth:>13.1f} m{b:>12.2f}{out:>15.2f}"
              f"{(b/core if core else 0):>8.1f}")
    print()

    print("=" * 70)
    print("TC-11 — diurnal gate on the same release")
    print("=" * 70)
    print(f"{'hour':>6}{'T_air C':>10}{'melt idx':>10}{'mu_w':>8}")
    for h in [0, 3, 6, 9, 12, 15, 18, 21]:
        t = diurnal_air_temp(9.0, 8.0, h)
        m = meltwater_index(t, 0.72, 0.20, 0.08)
        print(f"{h:>6}{t:>10.1f}{m:>10.1f}{friction_from_water(m):>8.3f}")
    print()
    print("  Langtang fired at 11:56 local.")
    print()

    print("LAG CLASSES (revised)")
    for k, (label, yrs) in LAG.items():
        print(f"  {k:<15}{label:<18}tau ~ {yrs:>9.5f} yr")
