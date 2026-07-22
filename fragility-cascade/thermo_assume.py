#!/usr/bin/env python3
"""
thermo_assume.py -- make omissions loud.
CC0 / Public Domain.  stdlib-only.

The binding constraint on this whole tool is not the engine, it is the
completeness of the assumption space. An unlisted energy source or an
unmodeled constraint does not surface as an error -- it surfaces as a
confident wrong answer (diesel assumed sole energy; labor assumed to
breathe free).

This layer does NOT fill gaps -- filling them with invented numbers is
the fabrication we are fighting. It reports which assumption DIMENSIONS
have zero coverage, and ships parameterized templates so the operator
can fill them with real figures.
"""

from dataclasses import dataclass
from typing import List, Optional
from thermo_pm import System, Resource, Process

FUEL = {"diesel", "gasoline", "petrol", "propane", "natural_gas", "gas",
        "wood", "biomass", "woodgas", "coal", "kerosene"}
EMISSION = {"exhaust", "emission", "emissions", "particulate", "pm",
            "pm25", "pm10", "co2", "smoke", "fumes", "soot"}
AIR = {"air", "air_quality", "aqi", "particulate", "pm25", "pm10"}
HUMAN_FACTOR = {"air", "air_quality", "aqi", "heat", "temperature",
                "water", "hydration", "rest", "shade"}


@dataclass
class Flag:
    dimension: str
    detail: str
    fix: str


# =============================================================================
# Assumption-coverage audit -- flags gaps, invents nothing
# =============================================================================
def audit_assumptions(sys: System) -> List[Flag]:
    flags: List[Flag] = []
    procs = list(sys.processes.values())

    def base(k): return k.partition(":")[0]

    # 1. energy diversity -- is diesel (or any one source) the silent default?
    energy_sources = set()
    for p in procs:
        for k in p.inputs:
            b = base(k)
            r = sys.resources.get(b)
            if r and r.type == "energy" and b != "human_labor" and b != "waste_heat":
                energy_sources.add(b)
    if len(energy_sources) <= 1:
        one = next(iter(energy_sources), "none")
        flags.append(Flag(
            "energy diversity",
            f"only one process-energy source modeled: {one}",
            "add alternatives from the library (solar_pv, grid_tie, "
            "human_power, biomass_gasifier); let the referee compare them"))

    # 2. air quality -- state, gate, and emission sink all present?
    has_air_state = any(any(w in n for w in AIR) for n in sys.resources)
    combustion = [p for p in procs if any(base(k) in FUEL for k in p.inputs)]
    emits = any(any(w in n for w in EMISSION)
                for p in procs for n in (set(p.outputs) | set(p.byproducts)))
    if combustion and not has_air_state:
        flags.append(Flag(
            "air quality",
            f"{len(combustion)} combustion process(es), no air state modeled",
            "add air_quality_kit(threshold); combustion should emit into it, "
            "labor should gate on it, ventilation should cost energy to restore it"))
    if combustion and not emits:
        flags.append(Flag(
            "emission sink",
            "combustion produces no exhaust/particulate byproduct",
            "declare an emission byproduct so the air debt is visible, not free"))

    # 3. human factors -- is labor gated by anything it actually needs?
    labor_procs = [p for p in procs if "human_labor" in {base(k) for k in p.inputs}]
    gated = [p for p in labor_procs
             if any(any(w in base(k) for w in HUMAN_FACTOR) for k in p.inputs)]
    if labor_procs and not gated:
        flags.append(Flag(
            "human factors",
            f"{len(labor_procs)} labor process(es), none gated by "
            "air/heat/water/rest",
            "labor modeled as unconstrained -- gate at least air and heat "
            "where the site demands it"))

    # 4. origin balance -- all-site (no import reality) or all-external?
    origins = {r.location for r in sys.resources.values()
               if r.type in ("energy", "matter")}
    if origins == {"site"}:
        flags.append(Flag(
            "origin", "no external supply modeled -- import cost invisible",
            "mark trucked-in resources location=external so draws are metered"))
    elif origins == {"external"}:
        flags.append(Flag(
            "origin", "nothing sourced from the land -- 'what does it offer?' unasked",
            "mark on-site resources location=site"))

    # 5. temporal -- any lifespan / decay dimension at all?
    has_decay = any(getattr(r, "info_value", None) in
                    ("temporary", "permanent") or "life" in n or "decay" in n
                    for n, r in sys.resources.items())
    if not has_decay:
        flags.append(Flag(
            "temporal",
            "no lifespan/decay dimension -- design life and end-of-life unmodeled",
            "attach intended design-life to the goal; it changes what's optimal"))

    return flags


def print_audit(sys: System):
    flags = audit_assumptions(sys)
    print("=" * 62)
    print(f"ASSUMPTION AUDIT -- {sys.name}")
    print("=" * 62)
    if not flags:
        print("  no empty dimensions detected (does not mean complete)")
    for f in flags:
        print(f"\n  [{f.dimension}]")
        print(f"     gap: {f.detail}")
        print(f"     fix: {f.fix}")
    print("=" * 62)


# =============================================================================
# Source library -- structure supplied, NUMBERS come from the operator
# =============================================================================
def solar_pv(name: str, joules_available: float) -> Resource:
    """Site energy, zero on-site emission. joules from real panel*hours."""
    return Resource(name, "energy", joules_available, "J", "site")


def grid_tie(name: str, joules: float) -> Resource:
    """External energy, ~0 on-site emission. Needs infra present on the site."""
    return Resource(name, "energy", joules, "J", "external")


def human_power(name: str, joules: float) -> Resource:
    """Site energy, food-sourced, low power, zero emission -- the old default."""
    return Resource(name, "energy", joules, "J", "site")


def diesel(name: str, joules: float) -> Resource:
    return Resource(name, "energy", joules, "J", "external")


def biomass_gasifier(name: str, fuel_in: float, work_out: float,
                     ash_kg: float, exhaust_kg: float) -> Process:
    """Site energy IF forested. Carries its own air/ash coupling."""
    return Process(name,
                   inputs={"biomass": fuel_in},
                   outputs={name + "_work": work_out},
                   byproducts={"ash": ash_kg, "exhaust": exhaust_kg},
                   types={name + "_work": "energy", "ash": "matter",
                          "exhaust": "matter"})


def air_quality_kit(threshold: float = 50.0):
    """Returns (air_state_resource, ventilation_factory).
    air_state is information (a reading, read-only when used as a gate)."""
    air = Resource("air_quality", "information", 100.0, "%", "site",
                   info_value="clean")

    def ventilation(energy_cost: float, restored: float) -> Process:
        return Process("ventilation",
                       inputs={"grid_power": energy_cost},
                       outputs={},
                       side_effects={"air_quality": +restored})
    return air, ventilation, threshold


def emit_into_air(proc: Process, particulate_kg: float,
                  air_hit: float) -> Process:
    """Wrap a combustion process so it degrades air state -- the coupling."""
    proc.byproducts = {**proc.byproducts, "exhaust": particulate_kg}
    proc.side_effects = {**proc.side_effects, "air_quality": -air_hit}
    proc.types.setdefault("exhaust", "matter")
    return proc


def gate_labor_on_air(proc: Process, min_air: float) -> Process:
    """Labor cannot proceed unless air_quality >= min_air (read-only gate)."""
    proc.inputs = {**proc.inputs, "air_quality": min_air}
    return proc


# =============================================================================
# Demo -- audit the interrogation site, then close two gaps with real structure
# =============================================================================
if __name__ == "__main__":
    from thermo_interrogate import build_site

    site = build_site()
    print_audit(site)          # flags: single energy source (diesel), air
                               # unmodeled, labor unconstrained, no temporal

    print("\n>>> closing two gaps with the library (numbers still yours):\n")
    site.add_resource(solar_pv("solar", 80_000))        # alt energy source
    site.add_resource(human_power("crew_power", 40_000))
    air, ventilation, thr = air_quality_kit(threshold=50)
    site.add_resource(air)
    site.add_resource(Resource("grid_power", "energy", 30_000, "J", "external"))
    site.register_process(ventilation(energy_cost=2000, restored=20))
    # couple the diesel import to the air it fouls, and gate the pour on it
    emit_into_air(site.processes["import_fill"], particulate_kg=3, air_hit=25)
    gate_labor_on_air(site.processes["pour_footing_code"], min_air=50)

    print_audit(site)          # energy + air + human-factor flags now clear;
                               # diesel's air debt is now visible to the referee
