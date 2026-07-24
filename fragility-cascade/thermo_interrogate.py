#!/usr/bin/env python3
"""
thermo_interrogate.py -- the site interrogation, computed.
CC0 / Public Domain.  stdlib-only.

Answers five operator questions for a site + goal:
  1. what does the land offer?
  2. what does the code say?
  3. how old is the code?
  4. what is the waste / unoptimized by not aligning with thermodynamics?
  5. what external energy is required?

Ground truth (physics) is the referee. The code overlay is DATA the tool
reports -- age and basis are fields, never inferred, never invented.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import date
import copy

from thermo_pm import System, Resource, Process, plan_with_mode, EPS
from thermo_explore import Playground


# =============================================================================
# Code overlay -- reported, not judged
# =============================================================================
@dataclass
class CodeRequirement:
    id: str
    enacted_year: int
    required_by: List[str]                 # processes that carry this gate
    basis: Optional[str] = None            # declared physical justification, or None
    intent_met_by: Optional[str] = None    # site reading that satisfies its intent
                                           # e.g. "soil_bearing:adequate"


# =============================================================================
# External accounting -- what crossed the site boundary
# =============================================================================
def _external_consumed(before: System, after: System) -> Dict[str, float]:
    out = {"energy": 0.0, "matter": 0.0}
    for name, r0 in before.resources.items():
        if r0.location != "external":
            continue
        drawn = r0.amount - after.resources.get(name, r0).amount
        if drawn > EPS and r0.type in out:
            out[r0.type] += drawn
    return out


def _replay(system: System, plan: List[str]) -> System:
    s = copy.deepcopy(system)
    for p in plan:
        if p in s.processes:
            s.run_process(s.processes[p])
    return s


# =============================================================================
# The interrogation
# =============================================================================
def interrogate(site: System, goal: Dict[str, float],
                code: Optional[List[CodeRequirement]] = None):
    code = code or []
    now = date.today().year

    # 1. what does the land offer -----------------------------------------
    offers = {n: (r.amount, r.unit) for n, r in site.resources.items()
              if r.location == "site" and r.type in ("energy", "matter")}
    readings = {n: r.info_value for n, r in site.resources.items()
                if r.type == "information" and r.info_value}
    buildable_now = Playground(site, goal).frontier()

    # physics-optimal plan (site + physical processes only) ---------------
    phys_plan = Playground(site, goal).solve()
    phys_ext = (_external_consumed(site, _replay(site, phys_plan))
                if phys_plan else None)
    phys_final = _replay(site, phys_plan) if phys_plan else None

    # code-constrained plan (institutional overlay allowed) ----------------
    code_res = plan_with_mode(site, goal, mode="code_compliant")
    code_plan = code_res[0] if code_res else None
    code_ext = (_external_consumed(site, code_res[1]) if code_res else None)

    def waste_heat(s):  # computed residual already sitting in the state
        return s.resources.get("waste_heat", Resource("w", "energy", 0)).amount if s else 0.0

    # 4. waste / unoptimized: code path minus physics path -----------------
    delta = None
    if phys_ext is not None and code_ext is not None:
        delta = {
            "external_energy_J": code_ext["energy"] - phys_ext["energy"],
            "external_matter_kg": code_ext["matter"] - phys_ext["matter"],
            "waste_heat_J": waste_heat(code_res[1]) - waste_heat(phys_final),
        }

    return {
        "land_offers": offers,
        "site_readings": readings,
        "buildable_from_site_alone": buildable_now,
        "code": [{
            "id": c.id,
            "age_years": now - c.enacted_year,
            "enacted": c.enacted_year,
            "basis": c.basis or "none declared",
            "intent_met_by_site": c.intent_met_by,
            "site_satisfies_intent": (
                c.intent_met_by in
                {f"{n}:{v}" for n, v in readings.items()} if c.intent_met_by else None),
        } for c in code],
        "external_required": {"physics_optimal": phys_ext, "code_constrained": code_ext},
        "waste_of_misalignment": delta,
        "physics_plan": phys_plan,
        "code_plan": code_plan,
    }


def print_report(r):
    print("=" * 62)
    print("SITE INTERROGATION")
    print("=" * 62)

    print("\n1. what does the land offer?")
    for n, (amt, u) in r["land_offers"].items():
        print(f"     {n:<20} {amt:>10g} {u}")
    for n, v in r["site_readings"].items():
        print(f"     {n:<20} {v:>10}  (reading)")
    print(f"     buildable from site alone: {r['buildable_from_site_alone']}")

    print("\n2/3. what does the code say?  how old is it?")
    if not r["code"]:
        print("     (no code overlay supplied)")
    for c in r["code"]:
        print(f"     {c['id']}: {c['age_years']}y old (enacted {c['enacted']})")
        print(f"        basis: {c['basis']}")
        if c["site_satisfies_intent"] is True:
            print(f"        site already meets its stated intent "
                  f"({c['intent_met_by_site']}) -- mandate is convention, not physics")
        elif c["site_satisfies_intent"] is False:
            print(f"        site does NOT meet intent -- mandate may be load-bearing")

    print("\n5. what external energy is required?")
    ext = r["external_required"]
    for label in ("physics_optimal", "code_constrained"):
        e = ext[label]
        if e is None:
            print(f"     {label:<18} no valid plan")
        else:
            print(f"     {label:<18} {e['energy']:>10g} J   {e['matter']:>8g} kg")

    print("\n4. waste / unoptimized by not aligning with thermodynamics")
    d = r["waste_of_misalignment"]
    if d is None:
        print("     (need both plans to compute)")
    else:
        print(f"     external energy the code adds over physics: {d['external_energy_J']:g} J")
        print(f"     external matter the code adds over physics: {d['external_matter_kg']:g} kg")
        print(f"     extra waste heat: {d['waste_heat_J']:g} J")
    print("=" * 62)


# =============================================================================
# Demo -- a site whose land already satisfies what the code says to import
# =============================================================================
def build_site() -> System:
    s = System("RealSite")
    # what the land offers (location=site)
    s.add_resource(Resource("local_stone",  "matter", 20_000, "kg", "site"))
    s.add_resource(Resource("clay",         "matter", 10_000, "kg", "site"))
    s.add_resource(Resource("human_labor",  "energy", 500_000, "J", "site"))
    # site reading: bearing capacity is adequate as-is
    s.add_resource(Resource("soil_bearing", "information", 1, "", "site",
                            info_value="adequate"))
    # external supply, metered when drawn (location=external)
    s.add_resource(Resource("diesel",         "energy", 100_000, "J", "external"))
    s.add_resource(Resource("offsite_reserve","matter", 10_000, "kg", "external"))
    s.add_resource(Resource("waste_heat",     "energy", 0, "J", "site"))

    T = {"footing": "artifact", "engineered_fill": "matter"}

    P = [
        # physics path: the land already bears -- lay a stone pad, all site
        Process("lay_stone_pad",
                inputs={"local_stone": 300, "human_labor": 1500,
                        "soil_bearing:adequate": 1},
                outputs={"footing": 1}, types=T),
        # code path: mandated import, costs external diesel + mass
        Process("approve_footing_code",
                inputs={"mode:code_compliant": 1, "human_labor": 5000},
                outputs={"code:footing_min_500mm": 1},
                types={"code:footing_min_500mm": "information"}),
        Process("import_fill",
                inputs={"mode:code_compliant": 1, "human_labor": 2000,
                        "offsite_reserve": 1200, "diesel": 20000},
                outputs={"engineered_fill": 1200}, types=T),
        Process("pour_footing_code",
                inputs={"mode:code_compliant": 1, "code:footing_min_500mm": 1,
                        "engineered_fill": 1200, "human_labor": 3000},
                outputs={"footing": 1}, types=T),
    ]
    for p in P:
        s.register_process(p)
    return s


if __name__ == "__main__":
    site = build_site()
    goal = {"footing": 1}
    code = [CodeRequirement(
        id="footing_min_500mm",
        enacted_year=1974,
        required_by=["pour_footing_code"],
        basis=None,                          # no physical derivation on file
        intent_met_by="soil_bearing:adequate",
    )]
    print_report(interrogate(site, goal, code))
