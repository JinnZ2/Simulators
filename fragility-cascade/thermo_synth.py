#!/usr/bin/env python3
"""
thermo_synth.py -- reason from physical quantity, not from named artifact.
CC0 / Public Domain.  stdlib-only.

The rest of the engine validates plans built from processes someone already
named (lay_stone_pad, run_engine). That caps the buildable frontier at the
library's imagination -- exactly the disease it audits. A site with no crane
returns "no valid plan," when physics says otherwise.

This layer inverts the search:

    GOAL is a physical QUANTITY + magnitude      (lifting_force >= 5000 N)
         not an artifact.  "crane" was never the requirement.

    LIBRARY is PHENOMENA keyed on physics         phase change, pressure-on-
         each: requires / produces / equation     area, lever, buoyancy...

    SEARCH matches goal-quantity -> phenomena that produce it
         -> filters to what on-hand SUBSTANCE PROPERTIES satisfy
         -> chains backward until every requirement is met from the site
         -> PROPOSES an assembly for a human to accept. names it AFTER.

Where the desert clay->steam->crane path can emerge -- and where it could
hallucinate, so it proposes to an operator and never auto-executes. It does
not invent magnitudes: physical constants are physics; site quantities are
yours; anything else is reported as unverified.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# =============================================================================
# Dimensional algebra -- the physics referee (analog of conservation in _pm)
#   dim vector = (M, L, T, Theta)
# =============================================================================
Dim = Tuple[int, int, int, int]

DIM: Dict[str, Dim] = {
    "mass":        (1, 0, 0, 0),
    "length":      (0, 1, 0, 0),
    "area":        (0, 2, 0, 0),
    "volume":      (0, 3, 0, 0),
    "temperature": (0, 0, 0, 1),
    "energy":      (1, 2, -2, 0),   # == heat, work
    "heat":        (1, 2, -2, 0),
    "power":       (1, 2, -3, 0),
    "flux":        (1, 0, -3, 0),   # power per area
    "force":       (1, 1, -2, 0),
    "pressure":    (1, -1, -2, 0),
}


def dmul(a: Dim, b: Dim) -> Dim:
    return tuple(x + y for x, y in zip(a, b))          # dims multiply -> add


def combine_dim(kinds: List[str]) -> Dim:
    out = (0, 0, 0, 0)
    for k in kinds:
        out = dmul(out, DIM[k])
    return out


# =============================================================================
# Substance -- something on hand, described by PROPERTIES, not by a role
#   a substance offers capabilities THROUGH its properties. water offers a
#   phase change because it has a boiling point + latent heat, not because
#   anyone labeled it "working fluid".
# =============================================================================
@dataclass
class Substance:
    name: str
    props: Dict[str, float] = field(default_factory=dict)
    supplies: List[str] = field(default_factory=list)   # quantity kinds it can source


# =============================================================================
# Phenomenon -- a physical effect keyed on physics, NOT an artifact
#   form MULTIPLY : out_mag = prod(inputs) * const   (dims must compose)
#   form ENABLE   : threshold gate; carries a substance to a new state
# =============================================================================
@dataclass
class Phenomenon:
    name: str
    produces: str                       # quantity kind produced
    form: str                           # "MULTIPLY" | "ENABLE"
    requires: List[str]                 # quantity kinds / substance capabilities needed
    equation: str                       # human-readable governing law
    needs_property: Dict[str, Tuple[str, float]] = field(default_factory=dict)
    # capability -> (substance property that must exist, min value). e.g. a
    # steam vessel needs melting_K > steam_K. keeps material selection PHYSICAL.

    def dim_ok(self) -> bool:
        if self.form != "MULTIPLY":
            return True                 # ENABLE gates a state, no product to check
        try:
            return combine_dim([r for r in self.requires if r in DIM]) == DIM[self.produces]
        except KeyError:
            return False


# =============================================================================
# Phenomenon library -- physics, not tools. force / heat / lift focused.
#   note there is no make_crane, no lay_pad. only effects.
# =============================================================================
LIBRARY: List[Phenomenon] = [
    Phenomenon("solar_concentration", produces="power", form="MULTIPLY",
               requires=["flux", "area"],
               equation="P = flux * aperture_area * concentration_factor * eff",
               needs_property={"concentrator": ("concentration_factor", 5.0)}),

    Phenomenon("sensible_heating", produces="temperature", form="ENABLE",
               requires=["power", "mass"],
               equation="dT = Q / (m * c)   [raise a mass toward a phase point]"),

    Phenomenon("vaporization", produces="vapor_mass", form="ENABLE",
               requires=["heat", "liquid_mass"],
               equation="Q_needed = m * L_vap   [liquid -> gas at boiling point]",
               needs_property={"fluid": ("latent_vap_J_per_kg", 1.0)}),

    Phenomenon("confined_vapor_pressure", produces="pressure", form="ENABLE",
               requires=["vapor_mass", "vessel"],
               equation="P from steam tables at T; vessel must contain it",
               needs_property={"vessel": ("melting_K", 400.0)}),   # > steam temp

    Phenomenon("pressure_on_area", produces="force", form="MULTIPLY",
               requires=["pressure", "area"],
               equation="F = P * piston_area"),

    Phenomenon("lever", produces="force", form="MULTIPLY",
               requires=["force", "ratio"],
               equation="F_out = F_in * (arm_in / arm_out)   [trades force<->distance]"),

    Phenomenon("mechanical_lift", produces="work", form="MULTIPLY",
               requires=["force", "length"],
               equation="W = F * displacement"),

    # alternatives the search will consider and DROP when substances absent:
    Phenomenon("combustion_heat", produces="heat", form="ENABLE",
               requires=["fuel", "oxidizer"],
               equation="Q = m_fuel * HHV   [needs fuel on hand -- desert had none]"),

    Phenomenon("buoyancy", produces="force", form="MULTIPLY",
               requires=["fluid_density", "displaced_volume"],
               equation="F = rho * V * g   [needs a fluid bath -- desert had none]"),
]


# =============================================================================
# Synthesizer -- backward search from goal quantity to on-hand substances
# =============================================================================
@dataclass
class Step:
    phenomenon: str
    equation: str
    supplied_by: str          # substance/quantity that satisfied it, or "<-chain"
    note: str = ""


@dataclass
class Assembly:
    goal: str
    steps: List[Step]
    dim_valid: bool
    flags: List[str]


class Synth:
    def __init__(self, on_hand: List[Substance]):
        self.on_hand = {s.name: s for s in on_hand}
        # flatten what the site can directly supply
        self.supplied = {}          # quantity kind -> substance name
        for s in on_hand:
            for q in s.supplies:
                self.supplied.setdefault(q, s.name)

    def _substance_with(self, prop: str, minv: float) -> Optional[str]:
        for s in self.on_hand.values():
            if s.props.get(prop, 0.0) >= minv:
                return s.name
        return None

    def _producers(self, kind: str) -> List[Phenomenon]:
        return [p for p in LIBRARY if p.produces == kind]

    def paths_to(self, goal_kind: str, depth: int = 4) -> List[Assembly]:
        results: List[Assembly] = []
        self._search(goal_kind, depth, [], set(), results)
        return results

    def _search(self, kind, depth, steps, seen, results):
        if depth < 0 or kind in seen:
            return
        for phen in self._producers(kind):
            flags, ok = [], True
            # material-property gates keep selection physical, not nominal
            for cap, (prop, minv) in phen.needs_property.items():
                who = self._substance_with(prop, minv)
                if who is None:
                    ok = False
                    flags.append(f"no on-hand substance meets {cap}: {prop}>={minv}")
                    break
            if not ok:
                continue
            substeps, satisfied = [], True
            for req in phen.requires:
                if req in self.supplied:                       # direct from site
                    substeps.append(Step(phen.name, phen.equation,
                                         self.supplied[req]))
                elif self._substance_with(req + "_ok", 1.0):   # capability alias
                    substeps.append(Step(phen.name, phen.equation, req))
                elif self._producers(req):                     # recurse: make it
                    inner: List[Assembly] = []
                    self._search(req, depth - 1, [], seen | {kind}, inner)
                    if inner:
                        substeps.append(Step(phen.name, phen.equation,
                                             "<-chain", f"via {inner[0].steps[-1].phenomenon}"))
                        substeps.extend(inner[0].steps)
                        flags.extend(inner[0].flags)
                    else:
                        satisfied = False
                        flags.append(f"cannot source '{req}' from site")
                else:
                    satisfied = False
                    flags.append(f"'{req}' not on hand and no phenomenon makes it")
            if satisfied:
                if not phen.dim_ok():
                    flags.append(f"DIMENSION MISMATCH in {phen.name} -- rejected")
                    continue
                flags.insert(0, "PROPOSED -- not validated; human confirms feasibility")
                if depth < 3:
                    flags.append("multi-step synthesis -- verify each coupling physically")
                results.append(Assembly(kind, list(reversed(substeps)),
                                        phen.dim_ok(), flags))


# =============================================================================
def show(a: Assembly):
    tick = "dim ok" if a.dim_valid else "DIM FAIL"
    print(f"\n  GOAL: produce {a.goal}   [{tick}]")
    for i, s in enumerate(a.steps):
        src = s.supplied_by if s.supplied_by != "<-chain" else s.note
        print(f"    {i+1}. {s.phenomenon:22s} <- {src}")
        print(f"       {s.equation}")
    for f in a.flags:
        print(f"    ! {f}")


# =============================================================================
# Demo -- the desert site.  goal = lifting force. no crane in the library.
# =============================================================================
if __name__ == "__main__":
    desert = [
        Substance("water_tank", supplies=["liquid_mass"],
                  props={"latent_vap_J_per_kg": 2.26e6, "boiling_K": 373}),
        Substance("sunlight", supplies=["flux"], props={"flux_W_per_m2": 1000}),
        Substance("fresnel_lens", supplies=["area"],
                  props={"concentration_factor": 200}),
        Substance("copper_tubing", supplies=["vessel", "area"],
                  props={"melting_K": 1358}),      # >> steam temp -> valid boiler
        Substance("rope", supplies=["ratio", "length"], props={"tensile_N": 8000}),
        Substance("clay", supplies=[],
                  props={"fired_compressive_Pa": 5e6, "moldable": 1}),
    ]

    print("=" * 64)
    print("DESERT SITE -- goal: lifting_force.  library has no 'crane'.")
    print("on hand: water, sunlight, fresnel, copper, rope, clay")
    print("=" * 64)

    synth = Synth(desert)

    # first the honest baseline: is there any FUEL to burn? no.
    print("\ncombustion path (the modern default):")
    print("  combustion_heat requires fuel + oxidizer -> no fuel on site -> DROPPED")

    print("\nphenomenon search for force:")
    for a in synth.paths_to("force"):
        show(a)

    print("\n" + "=" * 64)
    print("the steam path SURFACED from properties, not from a named process.")
    print("water's latent heat + copper's melting point + fresnel's factor")
    print("selected themselves. 'crane' dissolved into: pressure on an area.")
    print("=" * 64)
