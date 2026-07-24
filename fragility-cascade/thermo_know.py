#!/usr/bin/env python3
"""
thermo_know.py -- a taxonomy for information: WHAT is claimed, HOW it was
gotten, and how claims CROSS-REFERENCE. Provenance is first-class.
CC0 / Public Domain.  stdlib-only.

Every layer of this stack already gestures at provenance -- the referee
splits "operator-supplied" from "physical constant", the survey marks fields
UNREAD, the value lens traces pointers to referents. This module codes the
axis itself:

    WHAT    the claim + domain tags                       (categorize)
    HOW     acquisition mode -- how the knowing was made   (provenance)
    LINKS   corroborates / derives_from / contradicts      (cross-reference)

The structural fact about HOW: every mode reads one axis well and carries a
blindness it cannot escape. No mode is supreme. Ranking knowledge by its
MODE (instrument > tradition, written > oral) is the "primitive" error --
reading the label on the meter instead of the meter's properties.

Corroboration strength = INDEPENDENCE of the corroborating modes.
Two readings through the same mode share the same blindness: echo, not
confirmation. (LiDAR + trowel = both residue-mode = echo. Oral tradition +
excavation = independent axes = real corroboration -- the Upano case.)

Boundary held: the tool records how knowledge was gotten and measures
structure (traceability, independence, staleness, mode-masquerade). It does
not rank modes as inherently superior, and it does not rule on truth --
it reports how well-supported and how traceable a claim is, and stops.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# =============================================================================
# Acquisition modes -- each with its axis, blindness, and decay behavior
# =============================================================================
@dataclass
class Mode:
    name: str
    reads_well: str          # the axis this mode is strong on
    blind_to: str            # the axis it structurally cannot read
    decays_by: str           # how its reliability degrades over time
    stays_fresh_by: str      # what keeps it calibrated


MODES: Dict[str, Mode] = {m.name: m for m in [
    Mode("direct_observation",
         reads_well="what is present here, now, to the senses",
         blind_to="what the senses don't span; one vantage",
         decays_by="site changes after the observation",
         stays_fresh_by="re-observing"),
    Mode("repeated_practice",
         reads_well="what works -- embodied, error-corrected over many trials",
         blind_to="why it works; conditions outside the practiced range",
         decays_by="disuse; conditions drifting off the practiced range",
         stays_fresh_by="continued practice"),
    Mode("experiment",
         reads_well="causal response under deliberately varied conditions",
         blind_to="variables not varied; the lab/site gap",
         decays_by="context drift from test conditions",
         stays_fresh_by="replication in current conditions"),
    Mode("instrument",
         reads_well="the exact quantity the device is built to register",
         blind_to="every axis the device has no channel for "
                  "(the trowel reads residue, not return)",
         decays_by="calibration drift; the world moving off the sensor's axis",
         stays_fresh_by="recalibration against a known standard"),
    Mode("transmission",
         reads_well="deep time -- pattern integrated over more generations "
                    "than any instrument has run",
         blind_to="drift and loss in the chain; context of origin fading",
         decays_by="broken lineage; practice detaching from the telling",
         stays_fresh_by="living practice alongside the telling"),
    Mode("inference",
         reads_well="consequences of what is already known",
         blind_to="errors in its parents -- inherits every one silently",
         decays_by="any parent going stale",
         stays_fresh_by="re-checking parents"),
    Mode("authority",
         reads_well="consensus of whoever issued it, at issue time",
         blind_to="everything since issue; the issuer's own basis",
         decays_by="age -- the 1974 code, still commanding",
         stays_fresh_by="re-derivation from current ground truth"),
    Mode("model_generated",
         reads_well="the central tendency of its training distribution",
         blind_to="what the distribution under-sampled; its own defaults "
                  "(token-primary, diesel-assumed, residue-read)",
         decays_by="world drifting off the training distribution",
         stays_fresh_by="grounding against operator observation"),
]}


# =============================================================================
# A knowledge item: WHAT + HOW + lineage + links
# =============================================================================
@dataclass
class Know:
    claim: str
    about: List[str]                       # domain tags (categorize axis)
    how: str                               # acquisition mode key
    chain: List[str] = field(default_factory=list)   # lineage: who/what -> who
    year: Optional[int] = None             # when gotten / issued
    parents: List[str] = field(default_factory=list) # for inference: source claims
    corroborates: List[str] = field(default_factory=list)
    contradicts: List[str] = field(default_factory=list)
    note: str = ""


class Corpus:
    def __init__(self):
        self.items: Dict[str, Know] = {}

    def add(self, key: str, k: Know):
        self.items[key] = k

    # -- cross-reference reads ------------------------------------------------
    def support(self, key: str) -> Dict:
        """corroboration strength = number of INDEPENDENT modes agreeing.
        same-mode agreement is echo -- counted separately, weighted zero."""
        k = self.items[key]
        modes_agreeing = {k.how}
        echoes = 0
        for other_key, other in self.items.items():
            if other_key == key:
                continue
            if key in other.corroborates or other_key in k.corroborates:
                if other.how in modes_agreeing:
                    echoes += 1
                else:
                    modes_agreeing.add(other.how)
        contradictions = [o for o, ot in self.items.items()
                          if o != key and (key in ot.contradicts
                                           or o in k.contradicts)]
        return {"independent_modes": sorted(modes_agreeing),
                "strength": len(modes_agreeing),
                "echoes_same_mode": echoes,
                "contradicted_by": contradictions}

    # -- provenance audit -----------------------------------------------------
    def audit(self, current_year: int = 2026) -> List[str]:
        flags = []
        for key, k in self.items.items():
            if k.how not in MODES:
                flags.append(f"[{key}] unknown mode '{k.how}' -- untraceable")
                continue
            if k.how == "authority" and k.year and current_year - k.year > 20:
                flags.append(f"[{key}] authority aged {current_year - k.year}yr "
                             f"-- decays by age; re-derive from ground truth")
            if k.how == "inference" and not k.parents:
                flags.append(f"[{key}] inference with no parents -- "
                             f"inherits errors from sources it doesn't name")
            if k.how == "inference":
                for p in k.parents:
                    if p not in self.items:
                        flags.append(f"[{key}] parent '{p}' not in corpus -- "
                                     f"chain broken")
            if k.how == "transmission" and not k.chain:
                flags.append(f"[{key}] transmission without lineage -- "
                             f"strength of the mode IS the chain; record it")
            if k.how == "model_generated" and not k.corroborates:
                flags.append(f"[{key}] model-generated, uncorroborated -- "
                             f"central tendency of a training set; ground it")
        return flags


# =============================================================================
def show(corpus: Corpus, key: str):
    k = corpus.items[key]
    m = MODES[k.how]
    s = corpus.support(key)
    print(f"\n  [{key}]  {k.claim}")
    print(f"     about: {', '.join(k.about)}")
    print(f"     how:   {k.how}  (reads: {m.reads_well[:46]}...)"
          if len(m.reads_well) > 46 else
          f"     how:   {k.how}  (reads: {m.reads_well})")
    print(f"            blind:  {m.blind_to}")
    if k.chain:
        print(f"     chain: {' -> '.join(k.chain)}")
    if k.year:
        print(f"     year:  {k.year}")
    print(f"     support: {s['strength']} independent mode(s) "
          f"{s['independent_modes']}  echoes(same-mode): {s['echoes_same_mode']}")
    if s["contradicted_by"]:
        print(f"     CONTRADICTED by: {s['contradicted_by']}")


# =============================================================================
# Demo -- one quantity known five ways; independence vs echo; the audit
# =============================================================================
if __name__ == "__main__":
    c = Corpus()

    # the same soil, known through different modes:
    c.add("bearing_obs", Know(
        "this ground holds an 80k lb rig without rutting",
        about=["soil", "bearing"], how="direct_observation", year=2026,
        corroborates=["bearing_practice", "bearing_penetrometer"]))
    c.add("bearing_practice", Know(
        "clay-sand mix here firms under compaction; sites like this bore "
        "every structure I built on them",
        about=["soil", "bearing"], how="repeated_practice",
        corroborates=["bearing_obs"]))
    c.add("bearing_penetrometer", Know(
        "penetrometer reads 240 kPa at 0.5 m",
        about=["soil", "bearing"], how="instrument", year=2026,
        corroborates=["bearing_obs"]))
    c.add("bearing_county", Know(
        "county table: assume 150 kPa for this soil class",
        about=["soil", "bearing"], how="authority", year=1974,
        contradicts=["bearing_penetrometer"],
        note="the interrogate-layer case: aged authority vs current reading"))

    # deep-time transmission WITH its lineage recorded, corroborated by
    # an independent mode -- the Upano structure:
    c.add("floodplain_teaching", Know(
        "do not build below the second bench; the river takes the first",
        about=["siting", "water"], how="transmission",
        chain=["grandmother", "mother", "operator"],
        corroborates=["flood_marks"]))
    c.add("flood_marks", Know(
        "silt lines on the valley trees at first-bench height",
        about=["siting", "water"], how="direct_observation", year=2025,
        corroborates=["floodplain_teaching"]))

    # a model claim, uncorroborated -- flagged, not banned:
    c.add("ai_span_guess", Know(
        "model suggests 4 m max clear span for that timber section",
        about=["structure", "timber"], how="model_generated"))

    # an inference with a named parent chain:
    c.add("steam_feasible", Know(
        "confined steam at site temps can drive the lift piston",
        about=["energy", "phase"], how="inference",
        parents=["bearing_obs"]))   # wrong parent on purpose? no -- keep honest:
    c.items["steam_feasible"].parents = ["water_latent"]  # parent not in corpus

    print("=" * 66)
    print("KNOWLEDGE CORPUS -- what / how / cross-reference")
    print("=" * 66)
    for key in ["bearing_obs", "bearing_practice", "bearing_penetrometer",
                "bearing_county", "floodplain_teaching", "flood_marks",
                "ai_span_guess"]:
        show(c, key)

    print("\n" + "-" * 66)
    print("PROVENANCE AUDIT:")
    for f in c.audit():
        print(f"   ! {f}")

    print("\n" + "=" * 66)
    print("bearing: 3 INDEPENDENT modes agree (observation, practice,")
    print("instrument) -- strong. the 1974 authority contradicts the live")
    print("reading and is aged: flagged for re-derivation, not obeyed, not")
    print("erased. the teaching carries its lineage and is corroborated by")
    print("an independent mode -- deep time + present marks. the model's")
    print("span guess stands alone: usable, but named as ungrounded.")
    print("=" * 66)
