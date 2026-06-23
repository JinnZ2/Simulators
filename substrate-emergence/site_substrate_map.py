#!/usr/bin/env python3
# site_substrate_map.py
# CC0-1.0 / stdlib-only / re-injectable
#
# PRELUDE  (re-inject; same frame as substrate_emergence.py)
# -----------------------------------------------------------------
#   Document the ground that is actually here, not the lab.
#   Real field = contamination, mixture, weathering, water, season.
#   That mixture is not noise. It is the spec.
#   Map what abounds -> aggregate to a substrate profile ->
#   hand it to substrate_emergence.py and read what lives here.
# -----------------------------------------------------------------
#
# SHARED CONTRACT (same dict as substrate_emergence.py):
#   profile = {conducts, switches, dissipates, holds_heat,
#              costs_extract, abounds, bears_load, couples}  in 0..1
#
# This file SPEAKS that contract as output. No cross-import needed,
# so it runs alone on a phone. Paste its profile into the emergence file.

import json

AXES = ("conducts", "switches", "dissipates", "holds_heat",
        "costs_extract", "abounds", "bears_load", "couples")

# ----------------------------------------------------------------------
# MATERIAL LIBRARY
# Each known material contributes per-axis (0..1) the way THAT material
# pulls a substrate. These are seeds; correct them from your own ground.
# costs_extract here = cost to win+process LOCALLY (high = hard).
# ----------------------------------------------------------------------

MATERIALS = {
    "banded_iron":   {"conducts": 0.35, "switches": 0.25, "dissipates": 0.40,
                      "holds_heat": 0.70, "costs_extract": 0.30, "abounds": 0.85,
                      "bears_load": 0.75, "couples": 0.55},
    "magnetite":     {"conducts": 0.50, "switches": 0.35, "dissipates": 0.40,
                      "holds_heat": 0.60, "costs_extract": 0.35, "abounds": 0.65,
                      "bears_load": 0.70, "couples": 0.75},
    "hematite":      {"conducts": 0.30, "switches": 0.22, "dissipates": 0.42,
                      "holds_heat": 0.65, "costs_extract": 0.30, "abounds": 0.70,
                      "bears_load": 0.70, "couples": 0.50},
    "pyrite":        {"conducts": 0.55, "switches": 0.45, "dissipates": 0.45,
                      "holds_heat": 0.45, "costs_extract": 0.40, "abounds": 0.50,
                      "bears_load": 0.55, "couples": 0.50},
    "graphite":      {"conducts": 0.85, "switches": 0.55, "dissipates": 0.80,
                      "holds_heat": 0.35, "costs_extract": 0.45, "abounds": 0.35,
                      "bears_load": 0.40, "couples": 0.40},
    "native_copper": {"conducts": 0.95, "switches": 0.70, "dissipates": 0.85,
                      "holds_heat": 0.30, "costs_extract": 0.65, "abounds": 0.20,
                      "bears_load": 0.50, "couples": 0.30},
    "quartz_silica": {"conducts": 0.05, "switches": 0.10, "dissipates": 0.55,
                      "holds_heat": 0.45, "costs_extract": 0.55, "abounds": 0.95,
                      "bears_load": 0.85, "couples": 0.25},
    "iron_clay":     {"conducts": 0.30, "switches": 0.20, "dissipates": 0.35,
                      "holds_heat": 0.65, "costs_extract": 0.15, "abounds": 0.90,
                      "bears_load": 0.35, "couples": 0.80},
}

# ----------------------------------------------------------------------
# ENVIRONMENT MODIFIERS
# Field conditions bend the profile. Water, thermal swing, energy flux.
# Each returns axis deltas (added, then clamped). Coupling is the prize.
# ----------------------------------------------------------------------

def mod_water(wetness):
    """Water raises coupling + conduction (ionic), lowers load-bearing."""
    return {"couples": +0.20 * wetness,
            "conducts": +0.10 * wetness,
            "bears_load": -0.10 * wetness}

def mod_thermal_swing(swing):
    """Big annual/daily swing => season_sense via stored-heat lag,
       but stresses rigid structure."""
    return {"holds_heat": +0.10 * swing,
            "couples": +0.10 * swing,
            "bears_load": -0.10 * swing}

def mod_energy_flux(flux):
    """Available local energy (sun/hydro/wind/geo) eases extraction cost."""
    return {"costs_extract": -0.20 * flux}


# ----------------------------------------------------------------------
# AGGREGATE  --  mix materials by fraction, apply environment, clamp.
# ----------------------------------------------------------------------

def clamp(v):
    return 0.0 if v < 0.0 else 1.0 if v > 1.0 else v

def aggregate(materials_fractions, env=None):
    """
    materials_fractions: dict name -> fraction (need not sum to 1; normalized)
    env: dict with optional keys wetness, thermal_swing, energy_flux (0..1)
    returns: (profile, drivers)  where drivers says what pulls each axis
    """
    total = sum(materials_fractions.values()) or 1.0
    prof = {ax: 0.0 for ax in AXES}
    contrib = {ax: [] for ax in AXES}

    for name, frac in materials_fractions.items():
        w = frac / total
        m = MATERIALS.get(name)
        if not m:
            continue
        for ax in AXES:
            add = m[ax] * w
            prof[ax] += add
            if w >= 0.15:               # only name the real drivers
                contrib[ax].append((name, round(m[ax], 2)))

    env = env or {}
    deltas = {}
    for fn, key in ((mod_water, "wetness"),
                    (mod_thermal_swing, "thermal_swing"),
                    (mod_energy_flux, "energy_flux")):
        if key in env:
            for ax, dv in fn(env[key]).items():
                deltas[ax] = deltas.get(ax, 0.0) + dv

    for ax in AXES:
        prof[ax] = round(clamp(prof[ax] + deltas.get(ax, 0.0)), 3)

    drivers = {ax: contrib[ax] for ax in AXES if contrib[ax]}
    return prof, drivers


def show_site(name, prof, drivers, env=None):
    L = []
    L.append("=" * 58)
    L.append(f"SITE: {name}")
    L.append("=" * 58)
    L.append("SUBSTRATE PROFILE  (paste into substrate_emergence.py):")
    L.append("  " + json.dumps(prof))
    L.append("-" * 58)
    L.append("WHAT DRIVES EACH AXIS:")
    for ax in AXES:
        ds = drivers.get(ax)
        tag = ", ".join(f"{n}({v})" for n, v in ds) if ds else "mixed / env"
        L.append(f"  {ax:<13} {prof[ax]:<6} <- {tag}")
    if env:
        L.append("-" * 58)
        L.append("FIELD CONDITIONS APPLIED:")
        for k, v in env.items():
            L.append(f"  {k:<14} {v}")
    L.append("=" * 58)
    return "\n".join(L)


# ----------------------------------------------------------------------
# PRESET SITE  --  northern MN Canadian Shield, summer read.
# Iron-formation country: banded iron + magnetite + quartz, wet, swung.
# Correct fractions from your own ground truth.
# ----------------------------------------------------------------------

SHIELD_SUMMER = {
    "materials": {
        "banded_iron": 0.40,
        "magnetite":   0.20,
        "quartz_silica": 0.25,
        "iron_clay":   0.15,
    },
    "env": {"wetness": 0.6, "thermal_swing": 0.5, "energy_flux": 0.5},
}


def demo():
    prof, drivers = aggregate(SHIELD_SUMMER["materials"], SHIELD_SUMMER["env"])
    print(show_site("N. MN Canadian Shield — summer",
                    prof, drivers, SHIELD_SUMMER["env"]))


if __name__ == "__main__":
    demo()
    # build your own site:
    #   mats = {"banded_iron":0.5,"magnetite":0.3,"pyrite":0.2}
    #   env  = {"wetness":0.4,"thermal_swing":0.7,"energy_flux":0.3}
    #   prof, drv = aggregate(mats, env)
    #   print(show_site("my ridge — winter", prof, drv, env))
    #   then: emerge(prof) in substrate_emergence.py
