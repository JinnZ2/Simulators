#!/usr/bin/env python3
# contributing_inflow.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# CONTRIBUTING INFLOW — urban runoff as a parameterized antecedent pool increment.
#
# The mechanism: impervious surfaces in upstream cities increase runoff
# coefficient, raising tributary inflows, raising antecedent pool levels at
# downstream dams. Standard breach modeling typically uses naturalized or
# gage-recorded inflows that may not capture recent urbanization. The effect
# is real, load-bearing, and undocumented in most dam-safety specs.
#
# See SCOPE_BOUNDARY.md for why standard modeling drops this mechanism and
# why this spec includes it.
#
# This module documents the mechanism, parameterizes the effect, and shows
# the sensitivity on the operator swap. It contains no calibrated magnitude
# for any city, no hydrologic simulation, and no claim about any real structure.
#
# TWO WAYS TO TREAT IT:
#
#   1. As a POOL INCREMENT: the urban contribution raises the antecedent pool
#      above the naturalized baseline. This widens the Module F disagreement
#      band by exactly the increment.
#
#   2. As a WAVE INCREMENT: urban runoff arriving during the event adds to
#      the incoming flood wave rather than the stored pool. This is distinct
#      from the antecedent state and should be modeled as a tributary
#      hydrograph, not a pool level.
#
# This module handles case 1 (pool increment). Case 2 belongs in the routing
# engine, not in arithmetic.

import sys

# Knowledge state for variables that are physically relevant but not yet
# quantified. See SCOPE_BOUNDARY.md and knowledge_state.py.
# The urban increment for each city is UNKNOWN_ATM — the mechanism is known
# to exist, but no current value is available in this environment.
URBAN_INCREMENT_KNOWLEDGE_STATE = "UNKNOWN_ATM"
URBAN_INCREMENT_KNOWLEDGE_REASON = (
    "NLCD impervious surface data and historical gage records vs. naturalized "
    "flow estimates are required to calibrate. Both data sources refuse "
    "CONNECT from this environment. The parameter remains synthetic.")

# ------------------------------------------------------------------
# The tributary cities with significant impervious area and their
# connection to the dam chain. These are geographic facts, not claims
# about magnitude.
# ------------------------------------------------------------------

TRIBUTARY_CITIES = [
    # (city, tributary, joins_at, nearest_downstream_node, jurisdiction)
    ("Spokane",          "Spokane River",   "Columbia",   "Grand Coulee",     "US"),
    ("Tri-Cities",       "Yakima River",    "Columbia",   "McNary",           "US"),
    ("Portland metro",   "Willamette River","Columbia",   "Bonneville",       "US"),
    ("Lewiston",         "Clearwater River","Snake",      "Lower Granite",    "US"),
]

# ------------------------------------------------------------------
# Parameterization: urban runoff as a pool increment fraction.
#
# pool_effective = pool_natural * (1 + urban_increment_fraction)
#
# The fraction is dimensionless and synthetic. No city-specific value
# is asserted.
# ------------------------------------------------------------------

URBAN_INCREMENT_MIN = 0.0   # no urban contribution above naturalized baseline
URBAN_INCREMENT_MAX = 0.30  # synthetic upper bound: urban runoff adds up to
                            # 30% of the natural antecedent pool


def effective_pool(pool_natural, urban_increment_fraction):
    """The antecedent pool including urban runoff contribution.

    pool_natural: the antecedent pool under naturalized conditions
    urban_increment_fraction: dimensionless fraction of pool_natural
                              attributable to urban runoff

    Returns pool_effective = pool_natural * (1 + urban_increment_fraction)."""
    return pool_natural * (1.0 + urban_increment_fraction)


# ------------------------------------------------------------------
# Effect on the operator swap (from module_f.py)
# ------------------------------------------------------------------

def combine(op, wave, pool):
    """The quantity fed to the breach test, under either operator."""
    if op == "max":
        return max(wave, pool)
    if op == "sum":
        return wave + pool
    raise ValueError(op)


def breaches(op, wave, pool, crest):
    """Breach iff the combined quantity reaches the crest."""
    return combine(op, wave, pool) >= crest


def disagreement_band(pool, crest):
    """The wave interval [lo, hi) on which max and sum disagree.

    Width equals pool. With urban increment, width equals pool_effective."""
    freeboard = crest - pool
    if pool <= 0:
        return {"lo": None, "hi": None, "width": 0.0}
    return {"lo": freeboard, "hi": crest, "width": float(pool)}


# ------------------------------------------------------------------
# Sensitivity: how does urban runoff change the breach verdict?
# ------------------------------------------------------------------

def urban_sensitivity(wave, pool_natural, crest, urban_increment_fraction):
    """The change in breach verdict due to urban runoff.

    Returns a dict showing:
    - whether the urban increment changes the verdict under each operator
    - the disagreement band width with and without urban increment
    - whether the urban increment is the decisive factor (makes coupled
      breach where independent does not, when natural pool alone would not)

    All inputs are synthetic scalars."""
    pool_eff = effective_pool(pool_natural, urban_increment_fraction)

    # Without urban increment
    ind_base = breaches("max", wave, pool_natural, crest)
    coup_base = breaches("sum", wave, pool_natural, crest)

    # With urban increment
    ind_urb = breaches("max", wave, pool_eff, crest)
    coup_urb = breaches("sum", wave, pool_eff, crest)

    band_base = disagreement_band(pool_natural, crest)
    band_urb = disagreement_band(pool_eff, crest)

    return {
        "wave": wave,
        "pool_natural": pool_natural,
        "pool_effective": pool_eff,
        "urban_increment_fraction": urban_increment_fraction,
        "crest": crest,
        "independent_base": ind_base,
        "coupled_base": coup_base,
        "independent_urban": ind_urb,
        "coupled_urban": coup_urb,
        "band_width_base": band_base["width"],
        "band_width_urban": band_urb["width"],
        "band_widening": band_urb["width"] - band_base["width"],
        "urban_decisive": (not coup_base) and coup_urb,
        "urban_changes_independent": ind_base != ind_urb,
        "urban_changes_coupled": coup_base != coup_urb,
    }


# ------------------------------------------------------------------
# Sweep: urban increment sensitivity across the parameter space
# ------------------------------------------------------------------

def sweep_urban_sensitivity():
    """Sweep urban increment effect across synthetic parameters.

    Returns True iff the urban increment never causes an independent-only
    breach (the one-sided bias is preserved) and the band widening is
    exactly pool_natural * urban_increment_fraction at every point."""
    for wave in [1.0, 3.0, 5.0, 7.0, 9.0]:
        for pool_nat in [2.0, 4.0, 6.0]:
            for crest in [8.0, 10.0, 12.0]:
                for uif in [0.0, 0.1, 0.2, 0.3]:
                    if pool_nat >= crest:
                        continue  # no freeboard, both breach anyway
                    r = urban_sensitivity(wave, pool_nat, crest, uif)
                    # The band widening must equal the urban increment
                    expected_widening = pool_nat * uif
                    if abs(r["band_widening"] - expected_widening) > 1e-12:
                        return False
                    # Urban increment cannot cause independent-only breach
                    if r["independent_urban"] and not r["coupled_urban"]:
                        return False
    return True


# ------------------------------------------------------------------
# Null tests
# ------------------------------------------------------------------

def null_tests():
    """The three null conditions for urban contribution.

    1. urban_increment = 0: pool_effective = pool_natural, no change.
    2. pool_natural = 0: pool_effective = 0, no effect regardless of increment.
    3. wave already breaches both operators: urban increment is moot."""
    r1 = urban_sensitivity(5.0, 4.0, 10.0, 0.0)
    null_1 = (r1["urban_changes_independent"] is False
              and r1["urban_changes_coupled"] is False)

    r2 = urban_sensitivity(5.0, 0.0, 10.0, 0.3)
    null_2 = (r2["urban_changes_independent"] is False
              and r2["urban_changes_coupled"] is False)

    r3 = urban_sensitivity(15.0, 4.0, 10.0, 0.3)
    null_3 = (r3["independent_base"] is True
              and r3["coupled_base"] is True
              and r3["independent_urban"] is True
              and r3["coupled_urban"] is True)

    return {
        "null_1_no_increment": null_1,
        "null_2_no_pool": null_2,
        "null_3_already_breached": null_3,
        "all_pass": null_1 and null_2 and null_3,
    }


# ------------------------------------------------------------------
# Render
# ------------------------------------------------------------------

def render():
    out = []
    w = out.append
    w("CONTRIBUTING INFLOW — urban runoff as an antecedent pool increment")
    w("")
    w("The mechanism: impervious surfaces in upstream cities increase")
    w("runoff coefficient, raising tributary inflows, raising antecedent")
    w("pool levels at downstream dams. Standard breach modeling typically")
    w("uses naturalized or gage-recorded inflows that may not capture")
    w("recent urbanization. The effect is real, load-bearing, and")
    w("undocumented in most dam-safety specs.")
    w("")
    w("TRIBUTARY CITIES (geographic facts, not magnitude claims):")
    for city, trib, joins, node, juris in TRIBUTARY_CITIES:
        w("  %-18s %-16s -> %-10s (node: %-14s, %s)"
          % (city, trib, joins, node, juris))
    w("")
    w("PARAMETERIZATION (synthetic, dimensionless):")
    w("  pool_effective = pool_natural * (1 + urban_increment_fraction)")
    w("  urban_increment_fraction: %.1f to %.1f"
      % (URBAN_INCREMENT_MIN, URBAN_INCREMENT_MAX))
    w("  No city-specific value is asserted. The fraction is a sensitivity")
    w("  parameter, not a calibrated coefficient.")
    w("")
    w("EFFECT ON THE OPERATOR SWAP:")
    w("  The disagreement band width equals pool_effective.")
    w("  Urban runoff widens the band by pool_natural * urban_increment.")
    w("  A wider band means more waves breach under coupled physics but")
    w("  NOT under independent-node evaluation.")
    w("")
    w("SENSITIVITY EXAMPLE (synthetic node, not a real structure):")
    w("  crest 10, pool_natural 4, wave 6")
    for uif in [0.0, 0.1, 0.2, 0.3]:
        r = urban_sensitivity(6.0, 4.0, 10.0, uif)
        w("    urban_increment %.1f: pool_eff %.2f, band_width %.2f, "
          "coupled_breaches %s, urban_decisive %s"
          % (uif, r["pool_effective"], r["band_width_urban"],
             r["coupled_urban"], r["urban_decisive"]))
    w("")
    w("  At urban_increment = 0.0: pool_eff = 4.0, band = 4.0, wave 6")
    w("    breaches under coupled (6+4 >= 10) but NOT under independent")
    w("    (max(6,4) = 6 < 10). This is the baseline Module F result.")
    w("")
    w("  At urban_increment = 0.2: pool_eff = 4.8, band = 4.8, wave 6")
    w("    still breaches under coupled (6+4.8 >= 10) but NOT under")
    w("    independent (max(6,4.8) = 6 < 10). The band is wider, so")
    w("    more waves fall into the decisive region.")
    w("")
    w("  At urban_increment = 0.3: pool_eff = 5.2, wave 6")
    w("    now breaches under BOTH operators (max(6,5.2) = 6 >= 10 is")
    w("    FALSE, but 6+5.2 = 11.2 >= 10 is TRUE). Wait — max(6,5.2) = 6,")
    w("    which is still < 10. So independent does NOT breach. The urban")
    w("    increment has not yet pushed the pool above the wave.")
    w("")
    w("  The urban increment is decisive when it pushes pool_effective")
    w("  above the wave but below the crest — i.e. when")
    w("    wave < pool_effective < crest")
    w("  which requires urban_increment > (wave / pool_natural) - 1.")
    w("")
    w("SWEEP — structural properties hold across the parameter space:")
    w("  %s" % ("PASS" if sweep_urban_sensitivity() else "FAIL"))
    w("")
    w("NULL TESTS:")
    n = null_tests()
    w("  no urban increment:     no change  %s" % ("PASS" if n["null_1_no_increment"] else "FAIL"))
    w("  no antecedent pool:     no effect  %s" % ("PASS" if n["null_2_no_pool"] else "FAIL"))
    w("  already breached:       moot       %s" % ("PASS" if n["null_3_already_breached"] else "FAIL"))
    w("")
    w("WHAT THIS IS AND IS NOT")
    w("  IS: the mechanism of urban runoff contribution to antecedent pool,")
    w("      parameterized as a dimensionless increment, with sensitivity")
    w("      analysis and structural proofs.")
    w("  IS NOT: a hydrologic simulation of any city, a calibrated runoff")
    w("      coefficient for any watershed, or a claim about the current")
    w("      urban increment at any real dam.")
    w("")
    w("  To calibrate this parameter for a real chain, you need:")
    w("    - impervious surface area per tributary watershed (NLCD)")
    w("    - historical gage records vs. naturalized flow estimates")
    w("    - reservoir operating records showing pool levels during")
    w("      storm events vs. baseflow conditions")
    w("  Those data sources refuse CONNECT from this environment, so the")
    w("  parameter remains synthetic and the module remains arithmetic.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "contributing_inflow.py has no checks of its own. The checks "
            "that exercise it live in selftest_ccc.py.\n"
            "    python3 columbia-chain-cascade/selftest_ccc.py\n")
        sys.exit(2)
    print(render())
