#!/usr/bin/env python3
# substrate_emergence.py
# CC0-1.0 / stdlib-only / re-injectable
#
# PRELUDE  (re-inject at top of any session; it is the whole frame)
# -----------------------------------------------------------------
#   Every material constraint carries information.
#   A deficit on one axis ROUTES to a capability on another.
#   Do not optimize a single number. COUPLE, then read what emerges.
#   Output is a trajectory of relationships, never a stored verdict.
#   The organism does not ask "what is wrong with this substrate."
#   It asks "what does this substrate already do, and what lives here."
# -----------------------------------------------------------------
#
# SHARED CONTRACT  (spoken by site_substrate_map.py too):
#   A substrate profile is a plain dict. Keys are verb-first axes.
#   Values are relative, 0.0 .. 1.0, against silicon-era reference.
#   Missing key => assume 0.5 (unknown, neither help nor block).
#
#   conducts        electrons move how freely
#   switches        state flips how fast
#   dissipates      heat leaves how fast
#   holds_heat      thermal mass / how long state persists as warmth
#   costs_extract   energy to win + process it from local ground
#   abounds         how much is under your feet, here
#   bears_load      mechanical / structural stability
#   couples         how much the material registers its environment
#
# No part of this scores a substrate "good" or "bad".
# It reads couplings and tells you what architecture the ground wants.

import json

AXES = ("conducts", "switches", "dissipates", "holds_heat",
        "costs_extract", "abounds", "bears_load", "couples")


def read(profile, axis):
    """Read an axis; unknown reads as 0.5 (neutral), never as failure."""
    v = profile.get(axis, 0.5)
    return 0.0 if v < 0.0 else 1.0 if v > 1.0 else v


# ----------------------------------------------------------------------
# ROUTING  --  the heart. A low value is not a loss; it points somewhere.
# Each router reads the constraint and returns (capability, why) pairs.
# ----------------------------------------------------------------------

def route_deficits(p):
    """Turn each apparent deficit into where it routes. Verb-first."""
    out = []

    if read(p, "conducts") < 0.45:
        out.append((
            "build_bigger / go_parallel",
            "weak conduction does not carry a fast serial clock; "
            "it carries many slow paths at once. width replaces speed."))

    if read(p, "switches") < 0.45:
        out.append((
            "widen_error_window",
            "slow flips mean each decision sits longer; "
            "that dwell IS the correction time. settle, then commit."))

    if read(p, "dissipates") < 0.45 and read(p, "holds_heat") > 0.55:
        out.append((
            "heat_becomes_memory",
            "heat that will not leave is not waste; it is stored state. "
            "warmth carries the recent past forward."))

    if read(p, "costs_extract") > 0.55:
        out.append((
            "use_less / use_whats_loose",
            "expensive to win means design wants the surface find, "
            "the weathered seam, the already-broken — not the deep dig."))

    if read(p, "bears_load") < 0.45:
        out.append((
            "let_structure_be_soft",
            "low stiffness routes to flex; a flexing body survives the "
            "bend, the frost-heave, the cycle that snaps a rigid one."))

    if not out:
        out.append((
            "no_dominant_deficit",
            "this ground is balanced; emergence comes from coupling, "
            "not from compensating any single lack."))
    return out


def route_clock(p):
    """What timing regime lives here."""
    s, d = read(p, "switches"), read(p, "dissipates")
    speed = (s + d) / 2.0
    if speed > 0.66:
        return ("fast_clock",
                "flips quick and sheds heat quick: tight serial timing works.")
    if speed > 0.40:
        return ("breathing_clock",
                "moderate flip + shed: pace in bursts, rest between, like a pulse.")
    return ("slow_tide",
            "flips slow, holds heat: think in tides, not cycles. "
            "responsiveness lives in integration, not in clock rate.")


def route_topology(p):
    """Serial spine, parallel field, or networked organism."""
    c, a = read(p, "conducts"), read(p, "abounds")
    if c > 0.6 and a < 0.5:
        return ("serial_spine",
                "good conduction, scarce material: few fast lines, kept short.")
    if c < 0.5 and a > 0.6:
        return ("parallel_field",
                "weak conduction, abundant ground: spread wide, many slow nodes, "
                "let the answer come from the crowd.")
    return ("networked_organism",
            "mixed: couple fast cores to a slow abundant field around them — "
            "spine where you can afford it, field where you cannot.")


def route_senses(p):
    """What extra senses the coupling itself gives you, for free."""
    k = read(p, "couples")
    senses = []
    if k > 0.35:
        senses.append(("thermal_sense",
                       "the substrate's own warmth reports load + recent history."))
    if k > 0.50:
        senses.append(("moisture_sense",
                       "conductivity shifts with water; the ground reads its own wetness."))
    if k > 0.50 and read(p, "holds_heat") > 0.5:
        senses.append(("season_sense",
                       "stored heat lags the air; the body knows where it is in the year."))
    if k > 0.65:
        senses.append(("stress_sense",
                       "mechanical strain re-routes current; pressure becomes a signal."))
    if k > 0.75:
        senses.append(("field_sense",
                       "neighboring nodes shift together; distant state arrives by relation, "
                       "not by wire — the forest-network read."))
    if not senses:
        senses.append(("decoupled",
                       "loosely coupled ground gives few free senses; "
                       "raise 'couples' (wet clay, magnetite, contact area) to gain them."))
    return senses


# ----------------------------------------------------------------------
# EMERGE  --  run all routers, return the trajectory (relationships).
# ----------------------------------------------------------------------

def emerge(profile, name="unnamed-substrate"):
    return {
        "substrate": name,
        "clock": route_clock(profile),
        "topology": route_topology(profile),
        "deficit_routing": route_deficits(profile),
        "emergent_senses": route_senses(profile),
        "frame": "deficits routed, not fixed; read as relationship",
    }


def show(result):
    """Spatially-readable whole. Reads top-to-bottom from memory."""
    L = []
    L.append("=" * 58)
    L.append(f"SUBSTRATE: {result['substrate']}")
    L.append("=" * 58)
    cap, why = result["clock"]
    L.append(f"CLOCK     -> {cap}")
    L.append(f"             {why}")
    cap, why = result["topology"]
    L.append(f"TOPOLOGY  -> {cap}")
    L.append(f"             {why}")
    L.append("-" * 58)
    L.append("DEFICITS ROUTE TO:")
    for cap, why in result["deficit_routing"]:
        L.append(f"  + {cap}")
        L.append(f"      {why}")
    L.append("-" * 58)
    L.append("SENSES THAT EMERGE FROM COUPLING:")
    for cap, why in result["emergent_senses"]:
        L.append(f"  ~ {cap}")
        L.append(f"      {why}")
    L.append("=" * 58)
    return "\n".join(L)


# ----------------------------------------------------------------------
# PRESETS  --  rough relative profiles. Edit freely; these are seeds.
# ----------------------------------------------------------------------

PRESETS = {
    "banded_iron": {
        "conducts": 0.35, "switches": 0.25, "dissipates": 0.40,
        "holds_heat": 0.70, "costs_extract": 0.30, "abounds": 0.85,
        "bears_load": 0.75, "couples": 0.55,
    },
    "pyrite": {
        "conducts": 0.55, "switches": 0.45, "dissipates": 0.45,
        "holds_heat": 0.45, "costs_extract": 0.40, "abounds": 0.50,
        "bears_load": 0.55, "couples": 0.50,
    },
    "magnetite": {
        "conducts": 0.50, "switches": 0.35, "dissipates": 0.40,
        "holds_heat": 0.60, "costs_extract": 0.35, "abounds": 0.65,
        "bears_load": 0.70, "couples": 0.75,   # magnetic -> field coupling
    },
    "native_copper": {
        "conducts": 0.95, "switches": 0.70, "dissipates": 0.85,
        "holds_heat": 0.30, "costs_extract": 0.65, "abounds": 0.20,
        "bears_load": 0.50, "couples": 0.30,
    },
    "wet_clay_iron": {   # iron-bearing clay, water-coupled
        "conducts": 0.30, "switches": 0.20, "dissipates": 0.35,
        "holds_heat": 0.65, "costs_extract": 0.15, "abounds": 0.90,
        "bears_load": 0.35, "couples": 0.80,
    },
}


def demo():
    for name, prof in PRESETS.items():
        print(show(emerge(prof, name)))
        print()


if __name__ == "__main__":
    demo()
    # compose your own:
    #   p = dict(PRESETS["banded_iron"]); p["couples"] = 0.8
    #   print(show(emerge(p, "banded_iron + magnetite contacts")))
    #   json.dump(emerge(p, "..."), open("out.json","w"), indent=2)
