"""
baseline.py -- paleoclimate analogs as PATTERN sources, not templates.

CC0. stdlib-only. Anti-freeze.

Each analog is a past episode where Atlantic/ocean overturning was disrupted.
We carry them for the *shape* of the transition they record -- rate, precip
behaviour, ecosystem lag -- NOT as a state to recreate. divergence.py is what
strips the parts of each analog that depended on a starting condition we no
longer have (continental ice, meltwater buffer, active permafrost cycle).

Honest-gap protocol (inherited from CONVERGENCE_TABLE_2026):
  - Every field carries a `confidence` and a `source_class`.
  - source_class "proxy_reconstruction" != "instrumental" != "keeper_supplied".
  - No field is AI-invented. Ranges are wide on purpose. If a value is genuinely
    unknown for a region, it is None and flagged, never quietly interpolated.

These numbers are order-of-magnitude scaffolding pulled from the published
paleoclimate literature on these events. They are starting points for the user
to replace with their own region's proxy data, not authority. Replace them.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Analog:
    name: str
    years_bp: tuple                 # approximate calendar years before present
    trigger: str                    # what disrupted overturning
    transition_decades: tuple       # how fast the flip happened (low, high)
    nh_cooling_C: tuple             # N. Hemisphere land cooling range (low, high)
    precip_signal: str              # qualitative precip regime change
    ecosystem_lag_decades: tuple    # vegetation/fauna lag behind climate
    starting_state: dict            # what the world looked like going in
    confidence: str                 # "low" | "medium" | "high"
    source_class: str               # provenance of the numbers
    inherits_to_now: Optional[bool] = None  # set by divergence.py
    notes: str = ""


# --- the analogs -------------------------------------------------------

YOUNGER_DRYAS = Analog(
    name="Younger Dryas",
    years_bp=(12900, 11700),
    trigger="meltwater pulse to N. Atlantic from retreating Laurentide ice "
            "(routing debated) -> AMOC slowdown",
    transition_decades=(1, 6),          # onset within decades; abrupt
    nh_cooling_C=(2.0, 6.0),            # regional, larger near N. Atlantic
    precip_signal="sharp drying + windier; monsoon weakening at low lat; "
                  "high interannual variability",
    ecosystem_lag_decades=(5, 30),
    starting_state={
        "continental_ice": True,        # Laurentide still present
        "meltwater_buffer": True,       # active glacial meltwater routing
        "permafrost_cycle": True,
        "sea_level_rising": True,
    },
    confidence="medium",
    source_class="proxy_reconstruction (ice cores, varves, pollen)",
    notes="Closest classic AMOC-shutdown analog. BUT starting state has "
          "continental ice we no longer have -> see divergence.py.",
)

EVENT_8200 = Analog(
    name="8.2 kiloyear event",
    years_bp=(8300, 8000),
    trigger="catastrophic drainage of glacial Lakes Agassiz/Ojibway into "
            "Hudson Bay/N. Atlantic -> brief AMOC reduction",
    transition_decades=(1, 2),          # very abrupt, short-lived
    nh_cooling_C=(1.0, 3.0),
    precip_signal="drier across N. Atlantic margins; weakened monsoons; "
                  "decadal-scale drought pulses",
    ecosystem_lag_decades=(2, 15),
    starting_state={
        "continental_ice": True,        # residual Laurentide
        "meltwater_buffer": True,       # the lakes themselves
        "permafrost_cycle": True,
        "sea_level_rising": True,
    },
    confidence="medium",
    source_class="proxy_reconstruction (Greenland ice, speleothem, lake)",
    notes="Best RATE analog -- shows how fast a freshwater pulse bites and "
          "how the system partly recovered. Recovery here depended on the "
          "pulse being finite. Antarctic/Greenland loading now is not finite.",
)

HEINRICH_1 = Analog(
    name="Heinrich Stadial 1",
    years_bp=(18000, 15000),
    trigger="massive iceberg discharge to N. Atlantic -> sustained AMOC "
            "weakening; coincided with peak ENSO amplification",
    transition_decades=(1, 10),
    nh_cooling_C=(2.0, 5.0),
    precip_signal="large-scale tropical rainbelt (ITCZ) shifts south; "
                  "amplified El Nino variability; megadrought + megaflood swings",
    ecosystem_lag_decades=(10, 50),
    starting_state={
        "continental_ice": True,
        "meltwater_buffer": True,
        "permafrost_cycle": True,
        "sea_level_rising": True,
    },
    confidence="low",
    source_class="proxy_reconstruction (marine sediment, Ti flux, foram)",
    notes="Carries the AMOC<->ENSO coupling signal: a weak Atlantic "
          "overturning rode WITH extreme El Nino swings. Directly relevant "
          "to a super-El-Nino-during-loading scenario. Confidence low; deep time.",
)

ANALOGS = {a.name: a for a in (YOUNGER_DRYAS, EVENT_8200, HEINRICH_1)}


def get(name: str) -> Analog:
    if name not in ANALOGS:
        raise KeyError(f"unknown analog {name!r}; have {list(ANALOGS)}")
    return ANALOGS[name]


def all_analogs() -> list:
    return list(ANALOGS.values())


if __name__ == "__main__":
    for a in all_analogs():
        print(f"{a.name:22s} rate={a.transition_decades} dec  "
              f"cool={a.nh_cooling_C} C  conf={a.confidence}")
        print(f"   {a.precip_signal}")
