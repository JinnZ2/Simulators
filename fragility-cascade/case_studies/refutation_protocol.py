#!/usr/bin/env python3
"""
refutation_protocol.py  (v2)

WHAT CHANGED FROM v1
  v1 computed  C = (A * gamma) / omega  and read a truth verdict off it.
  Four things broke:
    - the `claim` argument was never read; verdict was a pure function of
      three hand-chosen numbers
    - gamma ("violates thermodynamics") sat in the NUMERATOR, so more
      violation raised C, and C > 1.5 printed "STANDING -- build on it".
      A `if gamma > 0.8` guard was bolted on to patch the sign, and that
      guard shadowed C entirely in the module's own demo (C=1.069, unused)
    - low omega drove C -> 250; the module measured how loudly a claim is
      repeated and returned that as truth
    - coherens.py defines C = (A + gamma)/omega with gamma as DAMPING
      (stabilizing, matching resonance_audit's omega_0^2 + gamma^2).
      v1 reused the symbol with inverted sign and a different operator.

THE ACTUAL ERROR
  Propagation and truth are different objects. v1 multiplied them.
  How hard a claim is pushed is measurable. Whether it is true is not a
  function of how hard it is pushed. This module DIVIDEs them and never
  recombines them into a single scalar.

CLAIM (C29-v2)
  A claim with quantitative physical content can be refuted by computing
  the horizon at which its own rate crosses a named conservation bound.
  The output is a horizon in years and the identity of the binding bound
  -- not a verdict scalar.

SCOPE
  Applies ONLY to claims that assert a rate against a bounded stock or
  flux. Claims without quantitative physical content are OUT OF SCOPE and
  this module returns NOT_APPLICABLE rather than inventing a score for
  them. v1 scored every claim; that was the bug, not a feature.

REFUTATION
  (R1) Show a sustained decoupling rate d >= g over a multi-decade window
       and the physical bound never binds -- the claim survives and C29-v2
       is refuted for that claim. This is the real argument and it is
       exposed here as a free parameter, not buried.
  (R2) Attack the bound itself (is 1.74e17 W the right ceiling?), the rate,
       or the coupling. Each is a separate, separately-refutable number.
  (R3) If a claim is refuted by this module but is observed to hold past
       its computed horizon, the bound or the coupling is wrong. Update the
       claim. Do not retune.

UNKNOWNS
  - Decoupling rate d is historically ~1.0-1.5 %/yr for energy intensity of
    GDP, but that is a fitted past, not a bound. It is a free parameter here.
  - Propagation scores A, omega remain hand-fed. They are NOT laundered into
    a truth verdict, so hand-feeding them is now honest instead of load-bearing.

stdlib only. CC0. No moral labels in returned structures.
"""

from __future__ import annotations

import math

# ------------------------------------------------------- physical bounds
# Each is a real number with a source and an attack surface.
BOUNDS = {
    "solar_intercepted": dict(
        watts=1.74e17,
        note="total solar power intercepted by Earth's disk",
    ),
    "waste_heat_boiling": dict(
        watts=4.37e17,
        note="human flux raising surface to 373K via Stefan-Boltzmann, "
             "sigma*T^4 = 1097 W/m^2 minus ~240 W/m^2 solar, over 5.1e14 m^2. "
             "Independent of energy SOURCE -- all use ends as heat.",
    ),
}

HUMAN_PRIMARY_POWER_W = 2.0e13   # ~620 EJ/yr, ~20 TW


# ------------------------------------------- object 1: propagation state
def propagation_state(claim: str, anchoring: float, drive: float) -> dict:
    """How a claim is carried. Says NOTHING about whether it is true.

    anchoring : how foundational the claim is in the frame that holds it
    drive     : how constantly it is re-broadcast

    Returns a description. No verdict. No recommendation. This is the half
    of v1 that was measuring something real -- it just was not measuring truth.
    """
    return {
        "claim": claim,
        "anchoring": anchoring,
        "drive": drive,
        "carriage": "high_drive" if drive > 0.6 else
                    "low_drive" if drive < 0.3 else "mid_drive",
        "note": "propagation only; not evidence for or against the claim",
    }


# --------------------------------------- object 2: thermodynamic horizon
def thermodynamic_horizon(claim: str,
                          growth_rate: float,
                          decoupling_rate: float = 0.0,
                          current_power_w: float = HUMAN_PRIMARY_POWER_W) -> dict:
    """Compute when a compounding rate crosses each named bound.

    growth_rate     : fractional per year, e.g. 0.03 for 3 %/yr
    decoupling_rate : fractional per year that physical throughput per unit
                      of the growing quantity declines. Effective physical
                      growth = growth_rate - decoupling_rate.

    Returns horizons + the binding bound. If effective growth <= 0, the
    bound never binds and the claim is NOT refuted by this route.
    """
    g_eff = growth_rate - decoupling_rate
    out = {
        "claim": claim,
        "growth_rate": growth_rate,
        "decoupling_rate": decoupling_rate,
        "effective_physical_growth": g_eff,
        "horizons_years": {},
        "binding_bound": None,
        "status": None,
    }
    if g_eff <= 0:
        out["status"] = "UNBOUNDED_ROUTE_OPEN"
        out["note"] = ("effective physical growth <= 0; no conservation bound "
                       "binds. C29-v2 does not refute this claim. R1 satisfied.")
        return out

    for name, b in BOUNDS.items():
        yrs = math.log(b["watts"] / current_power_w) / g_eff
        out["horizons_years"][name] = round(yrs, 1)

    binding = min(out["horizons_years"], key=out["horizons_years"].get)
    out["binding_bound"] = binding
    out["status"] = "BOUNDED"
    out["horizon_years"] = out["horizons_years"][binding]
    out["note"] = (f"at {g_eff*100:.2f} %/yr effective physical growth, "
                   f"{binding} binds in {out['horizon_years']:.0f} yr")
    return out


def applicability(claim: str, has_quantitative_rate: bool) -> str:
    """v1 scored every claim. Most claims are out of scope. Say so."""
    return "IN_SCOPE" if has_quantitative_rate else "NOT_APPLICABLE"


# --------------------------------------------------------------- demo
def main():
    print("=" * 70)
    print("REFUTATION PROTOCOL v2 -- propagation and truth held separate")
    print("=" * 70)

    claim = "The economy requires constant growth to be healthy."

    print("\nOBJECT 1 -- PROPAGATION (no truth content)")
    p = propagation_state(claim, anchoring=0.9, drive=0.8)
    for k, v in p.items():
        print(f"  {k:<12}: {v}")

    print("\nOBJECT 2 -- THERMODYNAMIC HORIZON (computed, not scored)")
    print(f"  {'g %/yr':>7} {'d %/yr':>7} {'g_eff':>7} {'solar':>9} "
          f"{'boiling':>9}  binding")
    for g, d in [(0.03, 0.0), (0.03, 0.015), (0.03, 0.029),
                 (0.03, 0.03), (0.023, 0.0), (0.07, 0.015)]:
        r = thermodynamic_horizon(claim, g, d)
        if r["status"] == "UNBOUNDED_ROUTE_OPEN":
            print(f"  {g*100:>7.1f} {d*100:>7.1f} {r['effective_physical_growth']*100:>7.2f} "
                  f"{'--':>9} {'--':>9}  none (R1 satisfied)")
        else:
            h = r["horizons_years"]
            print(f"  {g*100:>7.1f} {d*100:>7.1f} {r['effective_physical_growth']*100:>7.2f} "
                  f"{h['solar_intercepted']:>9.0f} {h['waste_heat_boiling']:>9.0f}"
                  f"  {r['binding_bound']}")

    print("\n  Bounds are attackable numbers, not vibes:")
    for name, b in BOUNDS.items():
        print(f"    {name:<20} {b['watts']:.2e} W")
        print(f"      {b['note']}")

    print("\nOUT-OF-SCOPE HANDLING")
    for c, q in [("Markets are self-correcting.", False),
                 ("AI is a neutral tool.", False),
                 ("Energy use grows 3%/yr indefinitely.", True)]:
        print(f"  {applicability(c, q):<15} {c}")
    print("  v1 returned FALSE NARRATIVE + DISENGAGE for all of these.")
    print("  Two have no quantitative physical content. There is nothing to")
    print("  compute. Returning a verdict anyway was the laundering step.")

    print("\n" + "=" * 70)
    print("WHAT v2 REFUSES TO EMIT")
    print("=" * 70)
    print("  no scalar 'Coherens' fusing propagation with truth")
    print("  no 'FALSE NARRATIVE' / 'STANDING' moral labels in the dict")
    print("  no sovereign_calibration() ENGAGE/DISENGAGE instruction")
    print("  no verdict for claims with no quantitative content")
    print()
    print("  The live edge is R1: sustained d >= g for decades and the")
    print("  physical bound never binds. That is the real argument against")
    print("  C29-v2, and it is a free parameter above, not a hidden one.")
    print("=" * 70)


if __name__ == "__main__":
    main()
