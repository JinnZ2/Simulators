#!/usr/bin/env python3
"""
thermo_purpose.py -- close the loop at end-of-life, not just at build.
CC0 / Public Domain.  stdlib-only.

thermo_pm checks matter closes at BUILD. Western "design life" draws the box
around build->serve and lets end-of-life fall off the ledger: build, serve,
fail, demolish, landfill -- matter leaves the pool, the loop never closes.

This layer keeps the ledger open the whole way. Every kilogram borrowed from
the site carries a return, and the return is judged fresh at end-of-life on
three independent gates:

    QUANTITY  returned / borrowed  ~ 1.0      give back what was given
    FORM      returns as something a CURRENT need takes, or the ground takes
              directly -- else it is a harm debt (mass closed, harm open)
    TIMING    lands back within the window the PURPOSE sets
                 seasonal structure -> fast return
                 star-guide college -> ~1000 yr slow return

Harm is not a fixed table. It is resolved by MATCHING returning matter to a
need read at the moment of return (this year, this millennium -- not build
year). When the direct path doesn't close, a fallback ladder:

    1. degraded as intended + a need/ground takes the form  -> return directly
    2. NOT degraded (still intact) -> find a use that does work AND converts
       toward a returnable form  (burn intact timber -> heat a tribe needs
       + ash the earth needs: one move, serves a need, advances the return)
    3. no current need for the form -> hold, keep tracking (delta open, not harm)

Governing invariant over every branch:  minimize |site_delta| against the
shape the site was found in.  "leave it the way you found it, or better."

The tool invents nothing: purpose windows, end-of-life condition, current
needs, what the ground takes, and the AXES of "same shape" are all operator
readings. The tool does the matching and the accounting.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# =============================================================================
@dataclass
class Purpose:
    name: str
    active_life_yr: float        # how long it serves
    return_window_yr: float      # budget from end-of-life until matter is back
    # timing gate measures the actual return against this window


@dataclass
class ReturnState:
    """Read AT end-of-life, not assumed at build."""
    condition: str                       # degraded_as_intended | intact | partial
    mass_by_form: Dict[str, float]       # form -> kg present now


@dataclass
class Conversion:
    """An end-of-life transform that does work WHILE converting to a return form.
    ratios are operator-supplied from the real material, never guessed."""
    name: str
    takes: str
    gives: Dict[str, float]              # output form -> kg (or service units) per kg in
    note: str = ""


# a minimal, operator-extensible conversion set. burn is the archetype:
# intact combustible -> heat (a need) + ash (a need) in one move.
DEFAULT_CONVERSIONS = [
    Conversion("burn", takes="timber",
               gives={"heat": 1.0, "ash": 0.05},
               note="serves warming need; yields ash for ground that needs ash"),
    Conversion("burn", takes="biomass",
               gives={"heat": 1.0, "ash": 0.03}),
]


# =============================================================================
@dataclass
class Routing:
    form: str
    mass: float
    outcome: str          # to_need | to_ground | reused | converted | held | HARM
    detail: str


def close_return(purpose: Purpose,
                 ret: ReturnState,
                 borrowed: Dict[str, float],      # form -> kg taken from site at build
                 need: Dict[str, float],          # form/service -> wanted, read NOW
                 ground_takes: set,               # forms this site's soil takes directly
                 conversions: List[Conversion] = None) -> Dict:
    conv = conversions or DEFAULT_CONVERSIONS
    need = dict(need)                              # consume as we route
    routes: List[Routing] = []
    returned = held = harm = 0.0

    def find_conversion(form) -> Optional[Conversion]:
        for c in conv:
            if c.takes == form:
                usable = all((o in need and need[o] > 0) or (o in ground_takes)
                             for o in c.gives)
                if usable:
                    return c
        return None

    def route_returnable(form, mass, via):
        """form is already in a returnable state -- match to need, then ground."""
        nonlocal returned
        if need.get(form, 0) > 0:
            need[form] -= mass
            routes.append(Routing(form, mass, "to_need",
                                  f"{via}; meets current need for {form}"))
        elif form in ground_takes:
            routes.append(Routing(form, mass, "to_ground",
                                  f"{via}; ground takes {form} directly"))
        else:
            routes.append(Routing(form, mass, "held",
                                  f"{via}; no need yet, tracked"))
            return False
        returned += mass
        return True

    for form, mass in ret.mass_by_form.items():
        if ret.condition == "degraded_as_intended":
            # matter already broken into its return form
            if not route_returnable(form, mass, "degraded as intended"):
                held += mass
            elif routes[-1].outcome == "held":
                held += mass
        else:
            # intact / partial: NOT yet returnable as-is -> convert or reuse
            c = find_conversion(form)
            if c:
                routes.append(Routing(form, mass, "converted",
                                      f"{c.name}: {c.note or 'converts to return forms'}"))
                for out_form, ratio in c.gives.items():
                    out_mass = mass * ratio
                    if out_form == "heat":
                        # heat does work (warming a need); not a mass return
                        if need.get("heat", 0) > 0:
                            need["heat"] -= out_mass
                            routes.append(Routing("heat", out_mass, "to_need",
                                                  "warms tribe -- work done in the return"))
                    else:
                        if route_returnable(out_form, out_mass,
                                            f"from {c.name}"):
                            pass
                        else:
                            held += out_mass
                returned += mass * sum(r for f, r in c.gives.items() if f != "heat")
            elif form in ground_takes or need.get(form, 0) > 0:
                # intact but directly reusable/placeable (restack stone, reuse beam)
                route_returnable(form, mass, "intact, reused/placed")
            else:
                # nothing takes it, no conversion, not reusable -> harm debt
                harm += mass
                routes.append(Routing(form, mass, "HARM",
                                      "no need, ground won't take it, not convertible"))

    borrowed_total = sum(borrowed.values()) or 1.0
    site_delta = borrowed_total - returned     # mass not yet back in the pool

    gates = {
        "QUANTITY": (returned / borrowed_total >= 0.95,
                     f"returned {returned:.1f} / borrowed {borrowed_total:.1f} kg"),
        "FORM":     (harm == 0.0,
                     f"harm debt {harm:.1f} kg (form nothing takes)"),
        "TIMING":   (held == 0.0,
                     f"held {held:.1f} kg unrouted within {purpose.return_window_yr:g} yr"),
    }
    return {"routes": routes, "returned": returned, "held": held, "harm": harm,
            "site_delta": site_delta, "gates": gates}


def report(purpose: Purpose, result: Dict):
    print("=" * 64)
    print(f"LIFECYCLE CLOSE -- {purpose.name}  "
          f"(serves {purpose.active_life_yr:g}yr, return window {purpose.return_window_yr:g}yr)")
    print("=" * 64)
    for r in result["routes"]:
        mark = "!!" if r.outcome == "HARM" else "  "
        print(f" {mark} {r.form:10s} {r.mass:8.2f}  {r.outcome:10s} {r.detail}")
    print(f"\n  site_delta (mass not back): {result['site_delta']:.2f} kg  "
          f"[objective -> 0]")
    allpass = True
    for name, (ok, detail) in result["gates"].items():
        print(f"  {name:9s} {'PASS' if ok else 'FAIL'}   {detail}")
        allpass &= ok
    print(f"\n  VERDICT: {'feeds the earth without harm' if allpass else 'return does not close'}")
    print("=" * 64)


# =============================================================================
# Demo -- three structures, judged at end-of-life
# =============================================================================
if __name__ == "__main__":

    # 1. seasonal shelter: earth + fiber, built to go back when the season ends
    seasonal = Purpose("seasonal_shelter", active_life_yr=0.5, return_window_yr=1)
    r1 = close_return(
        seasonal,
        ReturnState("degraded_as_intended", {"earth": 800, "fiber": 40}),
        borrowed={"earth": 800, "fiber": 40},
        need={"mulch": 0},
        ground_takes={"earth", "fiber", "ash"})
    report(seasonal, r1)

    # 2. star-guide college: fired clay + stone, feeds earth after ~1000 yr
    college = Purpose("star_guide_college", active_life_yr=1000, return_window_yr=1000)
    r2 = close_return(
        college,
        ReturnState("degraded_as_intended", {"mineral_dust": 5000, "stone": 12000}),
        borrowed={"mineral_dust": 5000, "stone": 12000},
        need={},
        ground_takes={"mineral_dust", "stone", "ash"})
    report(college, r2)

    # 3. branch-2: intact timber lodge, migration moved on, structure still solid.
    #    NOT degraded -> burn: heat the tribe needs + ash the ground needs.
    lodge = Purpose("migration_lodge", active_life_yr=15, return_window_yr=2)
    r3 = close_return(
        lodge,
        ReturnState("intact", {"timber": 3000}),
        borrowed={"timber": 3000},
        need={"heat": 3000, "ash": 100},         # tribe needs warming, ground needs ash
        ground_takes={"ash"})
    report(lodge, r3)

    # 4. concrete slab -- mass closes, harm open. the failure Western design hides
    slab = Purpose("concrete_slab", active_life_yr=50, return_window_yr=1)
    r4 = close_return(
        slab,
        ReturnState("intact", {"concrete_rubble": 20000}),
        borrowed={"concrete_rubble": 20000},
        need={},
        ground_takes=set())                       # ground takes none of it
    report(slab, r4)
