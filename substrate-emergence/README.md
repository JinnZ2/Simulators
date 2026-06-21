# substrate-emergence

Reads a material substrate as a profile of relative axes and reports what
**architecture the ground wants** — not what the ground "lacks." A deficit
on one axis routes to a capability on another. Couple, then read what
emerges.

CC0. Python stdlib only. Two modules speaking a shared contract:

- `substrate_emergence.py` — given a profile, read the architecture the
  ground wants.
- `site_substrate_map.py` — given a mix of materials at a real site
  (plus optional environmental modifiers like wetness, thermal swing,
  energy flux), aggregate to a profile. Output is the dict the
  emergence module consumes. The two scripts share no imports — paste
  the profile across — so either can run standalone on a phone.

## Frame (the prelude — re-injectable into any session)

```
  Every material constraint carries information.
  A deficit on one axis ROUTES to a capability on another.
  Do not optimize a single number. COUPLE, then read what emerges.
  Output is a trajectory of relationships, never a stored verdict.

  The organism does not ask "what is wrong with this substrate."
  It asks "what does this substrate already do, and what lives here."
```

## Shared contract

A substrate profile is a plain dict. Keys are verb-first axes, values
are relative `0.0 .. 1.0` against silicon-era reference. Missing key →
read as `0.5` (neutral, neither help nor block).

| Axis | What it measures |
| --- | --- |
| `conducts` | electrons move how freely |
| `switches` | state flips how fast |
| `dissipates` | heat leaves how fast |
| `holds_heat` | thermal mass / how long state persists as warmth |
| `costs_extract` | energy to win + process it from local ground |
| `abounds` | how much is under your feet, here |
| `bears_load` | mechanical / structural stability |
| `couples` | how much the material registers its environment |

No part of this module scores a substrate "good" or "bad." It reads
couplings and tells you what architecture the ground wants.

## Surface

| Function | Returns |
| --- | --- |
| `read(profile, axis)` | value clamped to `[0, 1]`, missing → 0.5 |
| `route_clock(p)` | `(capability, why)` — `fast_clock` / `breathing_clock` / `slow_tide` |
| `route_topology(p)` | `(capability, why)` — `serial_spine` / `parallel_field` / `networked_organism` |
| `route_deficits(p)` | list of `(capability, why)` — where each apparent deficit points |
| `route_senses(p)` | list of `(capability, why)` — what the coupling gives you for free |
| `emerge(profile, name)` | dict with `clock`, `topology`, `deficit_routing`, `emergent_senses`, `frame`, `substrate` |
| `show(result)` | spatially-readable rendering |
| `PRESETS` | five rough seed profiles (banded_iron, pyrite, magnetite, native_copper, wet_clay_iron) |

## Anti-freeze

The `emerge` return dict carries a `frame` string that documents the
methodology: *deficits routed, not fixed; read as relationship*. The
tests pin this — the dictionary shape is part of the contract.
`show()` renders it as a trajectory of relationships, not a verdict.

## Site-substrate map (build the profile from a real site)

`site_substrate_map.py` is the companion. The frame:

```
  Document the ground that is actually here, not the lab.
  Real field = contamination, mixture, weathering, water, season.
  That mixture is not noise. It is the spec.
  Map what abounds -> aggregate to a substrate profile ->
  hand it to substrate_emergence.py and read what lives here.
```

| Function | Returns |
| --- | --- |
| `MATERIALS` | dict of eight seed materials (banded_iron, magnetite, hematite, pyrite, graphite, native_copper, quartz_silica, iron_clay), each profiled along the same eight axes |
| `mod_water(wetness)` / `mod_thermal_swing(swing)` / `mod_energy_flux(flux)` | per-axis deltas applied on top of the material mix |
| `aggregate(materials_fractions, env)` | `(profile, drivers)` — fractions auto-normalized, env applied, values clamped, drivers list names only materials at ≥15% weight |
| `show_site(name, prof, drivers, env)` | renders the site card with the profile, the per-axis drivers, and any field conditions |
| `SHIELD_SUMMER` | preset for northern MN Canadian Shield, summer read |

The two modules share *no imports*. The contract is the dict
(`AXES` membership, values in `[0, 1]`, missing key → 0.5). Paste
the profile from one into the other.

## Running

```
python3 substrate_emergence.py            # PRESETS demo
python3 site_substrate_map.py             # site-mapping demo (Shield, summer)
python3 -m unittest discover tests        # 48 tests
```

Representative demo outputs are at `samples/demo.sample.txt` and
`samples/site_substrate_map.sample.txt`.

Compose your own:

```python
from substrate_emergence import PRESETS, emerge, show
p = dict(PRESETS["banded_iron"])
p["couples"] = 0.8                                  # add magnetite contacts
print(show(emerge(p, "banded_iron + magnetite contacts")))
```

## How it connects to the other folders

- `continuity-audit/` audits an incentive field acting on a diversity
  field. `substrate-emergence/` is the *physical* substrate companion:
  given a material substrate's profile, it reports the architecture
  that fits, the senses that emerge for free, and where each deficit
  routes. Same anti-freeze stance, different domain.
- `emergence-stability-simulator/` and `research-stability-audit/`
  identify substrate-as-anchor at the agent and field levels;
  `substrate-emergence/` is what "substrate" looks like one level
  further down — the material the agents and fields actually run on.
- See `../SYNTHESIS.md` for the cross-folder reading.
