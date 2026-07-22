#!/usr/bin/env python3
"""
thermo_survey.py -- read the site's fields before naming any phenomenon.
CC0 / Public Domain.  stdlib-only.  sits ABOVE thermo_synth.

The synthesizer starts from an on-hand material list. That is not where an
operator starts. An operator scans physical DOMAINS -- chemistry, pressure,
atmosphere, topology, biology, geology, materials, water, sun, wind, weather
-- and the phenomena fall out of what those fields are already doing.

The unifying read across every domain: each exposes an AMBIENT GRADIENT,
energy already flowing through the site at no import cost. Modern engineering
is blind to these and trucks in a gradient (diesel) instead. This layer reads
the gradients first, then hands the synthesizer both the substances AND the
ambient sources.

It invents nothing about a given site. It is a checklist of fields to read
(an unread field is a silent assumption -- ties to thermo_assume) and, per
field, what to look for and which phenomena it characteristically unlocks.
The observations are the operator's.
"""

from dataclasses import dataclass, field
from typing import Dict, List
from thermo_synth import Substance, Phenomenon, LIBRARY, DIM

# -- extend the dimension table for ambient-gradient quantities --------------
DIM.update({
    "velocity":   (0, 1, -1, 0),
    "density":    (1, -3, 0, 0),
    "g_field":    (0, 1, -2, 0),     # gravitational field the site already has
})

# -- ambient / natural phenomena the domains unlock (added to the core lib) --
AMBIENT = [
    Phenomenon("gravity_potential", produces="energy", form="MULTIPLY",
               requires=["mass", "length", "g_field"],
               equation="W = m * g * h   [height already stores this]"),

    Phenomenon("wind_kinetic", produces="pressure", form="MULTIPLY",
               requires=["density", "velocity", "velocity"],
               equation="q = 0.5 * rho * v^2   [moving air already carries this]"),

    Phenomenon("freeze_thaw_split", produces="force", form="ENABLE",
               requires=["liquid_mass", "temperature_cycle", "confinement"],
               equation="water expands ~9% on freezing -> splitting force "
                        "[how nature quarries stone]",
               needs_property={"confinement": ("crack_or_mold", 1.0)}),

    Phenomenon("evaporative_cooling", produces="temperature", form="ENABLE",
               requires=["liquid_mass", "dry_air"],
               equation="dT via latent heat carried off by evaporation"),

    Phenomenon("fermentation", produces="heat", form="ENABLE",
               requires=["biomass", "liquid_mass"],
               equation="metabolic exotherm + gas over time [biology, already warm]"),

    Phenomenon("gravity_feed", produces="work", form="ENABLE",
               requires=["height_difference", "liquid_mass"],
               equation="siphon / drop moves fluid with no pump"),
]
for p in AMBIENT:
    if p.name not in {x.name for x in LIBRARY}:
        LIBRARY.append(p)


# =============================================================================
# The domain scan -- your survey method, as a coverage checklist
#   gradient = the ambient energy the field may expose
#   unlocks  = phenomena that become available once the field is read
# =============================================================================
@dataclass
class Domain:
    name: str
    reads: str            # what the operator looks for
    gradient: str         # ambient energy this field may carry
    unlocks: List[str]    # phenomena keyed to it


DOMAINS: List[Domain] = [
    Domain("chemistry",  "reactive substances: fuels, lime, salts, minerals",
           "chemical potential", ["combustion_heat", "fermentation"]),
    Domain("pressure",   "confinement options, differentials, vessels",
           "pressure differential",
           ["confined_vapor_pressure", "pressure_on_area", "wind_kinetic"]),
    Domain("atmosphere", "air composition, humidity, temp, oxidizer",
           "thermal / humidity", ["evaporative_cooling", "vaporization"]),
    Domain("topology",   "height differences, slopes, drainage",
           "gravitational potential", ["gravity_potential", "gravity_feed"]),
    Domain("biology",    "plants, fiber, microbes, animal/human power",
           "metabolic", ["fermentation"]),
    Domain("geology",    "clay, stone, sand, thermal mass, bearing",
           "thermal-mass storage",
           ["confined_vapor_pressure", "freeze_thaw_split"]),
    Domain("materials",  "direct inventory on hand",
           "(none -- direct stock)", []),
    Domain("water",      "volume, quality, source",
           "phase / buoyancy / thermal mass",
           ["vaporization", "freeze_thaw_split", "evaporative_cooling"]),
    Domain("sunlight",   "flux, hours, angle, concentrator options",
           "radiant flux", ["solar_concentration", "sensible_heating"]),
    Domain("wind",       "direction, speed, consistency",
           "kinetic", ["wind_kinetic", "evaporative_cooling"]),
    Domain("weather",    "temp cycles, precip, seasonal swing",
           "thermal cycling", ["freeze_thaw_split"]),
]


# =============================================================================
# SiteScan -- operator records observations; scan emits substances + coverage
# =============================================================================
@dataclass
class SiteScan:
    name: str
    found: Dict[str, List[Substance]] = field(default_factory=dict)   # domain -> substances
    ambient: Dict[str, str] = field(default_factory=dict)             # domain -> gradient noted

    def observe(self, domain: str, substances: List[Substance] = None,
                gradient_present: bool = False):
        """Operator logs what a field actually offered on THIS site."""
        self.found[domain] = substances or []
        if gradient_present:
            d = next((x for x in DOMAINS if x.name == domain), None)
            if d:
                self.ambient[domain] = d.gradient

    def on_hand(self) -> List[Substance]:
        out = []
        for subs in self.found.values():
            out.extend(subs)
        return out

    def unlocked(self) -> List[str]:
        out = set()
        for domain in self.found:
            d = next((x for x in DOMAINS if x.name == domain), None)
            if d:
                out.update(d.unlocks)
        return sorted(out)

    def coverage(self):
        print("=" * 62)
        print(f"SITE SCAN -- {self.name}   (unread field = silent assumption)")
        print("=" * 62)
        for d in DOMAINS:
            if d.name in self.found:
                grad = self.ambient.get(d.name, "no gradient tapped")
                print(f"  [read]   {d.name:11s} gradient: {grad}")
            else:
                print(f"  [UNREAD] {d.name:11s} -- {d.gradient} not surveyed")
        print("\n  phenomena unlocked by read fields:")
        print("   ", ", ".join(self.unlocked()) or "none")
        print("=" * 62)


# =============================================================================
# Demo -- the desert site expressed as a domain scan, feeding the synthesizer
# =============================================================================
if __name__ == "__main__":
    from thermo_synth import Synth

    scan = SiteScan("desert_site")

    scan.observe("geology", [
        Substance("clay", supplies=["confinement"],
                  props={"fired_compressive_Pa": 5e6, "crack_or_mold": 1}),
    ], gradient_present=True)
    scan.observe("water", [
        Substance("water_tank", supplies=["liquid_mass"],
                  props={"latent_vap_J_per_kg": 2.26e6, "boiling_K": 373}),
    ], gradient_present=True)
    scan.observe("sunlight", [
        Substance("sunlight", supplies=["flux"], props={"flux_W_per_m2": 1000}),
        Substance("fresnel_lens", supplies=["area"],
                  props={"concentration_factor": 200}),
    ], gradient_present=True)
    scan.observe("materials", [
        Substance("copper_tubing", supplies=["vessel", "area"],
                  props={"melting_K": 1358}),
        Substance("rope", supplies=["ratio", "length"], props={"tensile_N": 8000}),
    ])
    # wind, biology, chemistry, weather, topology, atmosphere, pressure: UNREAD
    # the scan makes those omissions loud rather than assuming "nothing there"

    scan.coverage()

    print("\n>>> feeding scanned substances to the synthesizer, goal=force:\n")
    from thermo_synth import show
    synth = Synth(scan.on_hand())
    for a in synth.paths_to("force"):
        show(a)

    print("\n" + "=" * 62)
    print("the scan read 4 fields, left 7 UNREAD (loud, not assumed-empty).")
    print("even so, the read fields carried enough gradient -- sun's flux,")
    print("water's phase, copper's melting point -- to synthesize lift.")
    print("the unread fields (wind, weather freeze-thaw, biology) are")
    print("further gradients still on the table, now VISIBLE as unread.")
    print("=" * 62)
