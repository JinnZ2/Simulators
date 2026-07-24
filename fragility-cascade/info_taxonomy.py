#!/usr/bin/env python3
"""
info_taxonomy.py -- a generalized taxonomy for information:
types of information, ways of obtaining it, ways to know it, and how any
claim's support can be read. Domain-neutral. CC0 / Public Domain. stdlib-only.

WHY: the existing landscape holds one axis each and drops the rest --
  epistemology     names the modes, carries no operations (no decay, no audit)
  GRADE/pyramids   operational but rank modes (mode supremacy: a fixed ladder)
  Admiralty code   two-axis grading, but grades the source, not the mode's
                   structural blindness
  W3C PROV         chains, content-neutral: records THAT a derivation
                   happened, no theory of what any mode can't see
  library science  categorization only; evidence law's independence rule
                   is buried in doctrine, not computable

DESIGN COMMITMENTS (each fixes a named failure above):
  1. faceted type, not a tree.
  2. acquisition modes carry blindness/decay/freshness as DATA; the table is
     extensible and no mode is supreme.
  3. two grades, never multiplied into one number: source track-record and
     claim support are different axes; flattening them loses both.
  4. support counts INDEPENDENT modes only; same-mode agreement is echo,
     weight zero.
  5. staleness is computed per mode, not assumed.
  6. chains are PROV-compatible (derived_from / attributed_to /
     generated_by) so every corpus exports to existing tooling.

BOUNDARY: this grades structure -- traceability, independence, freshness --
never truth. Contradictions are tracked and surfaced, never auto-resolved.
Interior verdicts (what a claim means to a person, whether a knower is
honest) are out of scope by construction.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

# =============================================================================
# AXIS 1 -- TYPE: faceted, not a tree. facets cross-cut; extend freely.
# =============================================================================
FACETS: Dict[str, Set[str]] = {
    "content": {"observation", "measurement", "claim", "rule", "procedure",
                "model_output", "story", "teaching", "record"},
    "form":    {"numeric", "text", "oral", "embodied", "instrument_trace",
                "drawing", "artifact"},
    # "about" is open vocabulary -- domain tags, uncontrolled on purpose
}


# =============================================================================
# AXIS 2 -- MODE: how the knowing was made. extensible; no supreme mode.
# every row must fill all four operational fields -- a mode you can't state
# the blindness of isn't understood yet.
# =============================================================================
@dataclass
class Mode:
    name: str
    reads_well: str
    blind_to: str
    decays_by: str
    stays_fresh_by: str
    half_life_yr: Optional[float] = None   # None = no simple age decay


MODES: Dict[str, Mode] = {}


def register_mode(m: Mode):
    """The table is meant to be re-cut. Cultures cut acquisition differently;
    a registrant supplies all four fields -- that is the only entry bar."""
    MODES[m.name] = m


for _m in [
    Mode("direct_observation", "what is present here, now, to the senses",
         "what the senses don't span; one vantage",
         "the world changing after the look", "re-observing"),
    Mode("repeated_practice", "what works, error-corrected over many trials",
         "why it works; conditions outside the practiced range",
         "disuse; conditions drifting off-range", "continued practice"),
    Mode("experiment", "causal response under varied conditions",
         "variables not varied; the test/field gap",
         "context drift from test conditions", "replication in context"),
    Mode("instrument", "the exact quantity the device registers",
         "every axis the device has no channel for",
         "calibration drift", "recalibration against a standard"),
    Mode("transmission", "pattern integrated over more generations than any "
         "instrument has run",
         "drift and loss in the chain; origin context fading",
         "broken lineage; practice detaching from telling",
         "living practice alongside the telling"),
    Mode("inference", "consequences of what is already known",
         "errors in its parents -- inherited silently",
         "any parent going stale", "re-checking parents"),
    Mode("authority", "the issuer's consensus at issue time",
         "everything since issue; the issuer's own basis",
         "age", "re-derivation from ground truth", half_life_yr=20),
    Mode("model_generated", "central tendency of a training distribution",
         "what the distribution under-sampled; its own defaults",
         "world drifting off-distribution",
         "grounding against independent modes", half_life_yr=3),
    Mode("measured_constant", "quantities replicated across independent "
         "labs and generations",
         "applicability at THIS context's conditions",
         "context leaving the constant's valid range",
         "checking range assumptions in context"),
]:
    register_mode(_m)


# =============================================================================
# AXIS 3 -- SOURCE: who/what supplied it. graded on TRACK RECORD, separately
# from any claim's support (the Admiralty split, kept split).
# =============================================================================
@dataclass
class Source:
    name: str
    kind: str                                  # person | lineage | device | org | model
    track: List[bool] = field(default_factory=list)   # past claims: held up?

    def reliability(self) -> Optional[float]:
        """fraction of checked past claims that held. None = no track yet --
        which is 'unknown', NOT 'bad'. never merged with claim support."""
        return (sum(self.track) / len(self.track)) if self.track else None


# =============================================================================
# THE ITEM -- one piece of information, all axes attached
# =============================================================================
@dataclass
class Item:
    key: str
    claim: str
    content: str                               # facet: content kind
    form: str                                  # facet: form
    about: List[str]                           # open domain tags
    mode: str                                  # acquisition mode
    source: Optional[str] = None               # Source key (attributed_to)
    chain: List[str] = field(default_factory=list)     # lineage hops
    derived_from: List[str] = field(default_factory=list)  # parent item keys
    year: Optional[int] = None
    refreshed: Optional[int] = None            # last re-check, if any
    corroborates: List[str] = field(default_factory=list)
    contradicts: List[str] = field(default_factory=list)
    note: str = ""


# =============================================================================
class Corpus:
    def __init__(self, current_year: int = 2026):
        self.items: Dict[str, Item] = {}
        self.sources: Dict[str, Source] = {}
        self.year = current_year

    def add_source(self, s: Source):
        self.sources[s.name] = s

    def add(self, it: Item):
        self.items[it.key] = it

    # -- AXIS 4: SUPPORT -- independent modes only; echoes weight zero -------
    def support(self, key: str) -> Dict:
        it = self.items[key]
        modes = {it.mode}
        echoes = 0
        for k2, o in self.items.items():
            if k2 == key:
                continue
            linked = key in o.corroborates or k2 in it.corroborates
            if linked:
                if o.mode in modes:
                    echoes += 1
                else:
                    modes.add(o.mode)
        contras = [k2 for k2, o in self.items.items() if k2 != key and
                   (key in o.contradicts or k2 in it.contradicts)]
        return {"independent_modes": sorted(modes), "strength": len(modes),
                "echoes": echoes, "contradicted_by": contras}

    # -- AXIS 5: FRESHNESS -- computed per mode, not assumed -----------------
    def staleness(self, key: str) -> Optional[str]:
        it = self.items[key]
        m = MODES.get(it.mode)
        if not m or m.half_life_yr is None or it.year is None:
            return None
        age = self.year - (it.refreshed or it.year)
        if age > m.half_life_yr:
            return (f"aged {age}yr > half-life {m.half_life_yr:g}yr for "
                    f"mode '{it.mode}' -- {m.stays_fresh_by}")
        return None

    # -- transitive backing: walk derived_from to the leaves -----------------
    def backing(self, key: str, _seen=None) -> Dict[str, int]:
        _seen = _seen or set()
        if key in _seen:
            return {}
        _seen.add(key)
        it = self.items.get(key)
        if it is None:
            return {"BROKEN_CHAIN": 1}
        if not it.derived_from:
            return {it.mode: 1}
        census: Dict[str, int] = {}
        for p in it.derived_from:
            for m, n in self.backing(p, _seen).items():
                census[m] = census.get(m, 0) + n
        return census

    # -- the audit: structure flags, never truth verdicts --------------------
    def audit(self) -> List[str]:
        f = []
        for key, it in self.items.items():
            if it.mode not in MODES:
                f.append(f"[{key}] unregistered mode '{it.mode}'")
            if it.mode == "transmission" and not it.chain:
                f.append(f"[{key}] transmission without lineage -- the chain "
                         f"IS the mode's strength; record it")
            if it.mode == "inference" and not it.derived_from:
                f.append(f"[{key}] inference with no parents")
            for p in it.derived_from:
                if p not in self.items:
                    f.append(f"[{key}] parent '{p}' missing -- chain broken")
            s = self.support(key)
            if it.mode == "model_generated" and s["strength"] <= 1:
                f.append(f"[{key}] model output, uncorroborated -- ground it")
            if s["echoes"] >= 2 and s["strength"] <= 1:
                f.append(f"[{key}] {s['echoes']} same-mode echoes, zero "
                         f"independent support -- an echo chamber, not evidence")
            st = self.staleness(key)
            if st:
                f.append(f"[{key}] {st}")
            if s["contradicted_by"]:
                f.append(f"[{key}] contradicted by {s['contradicted_by']} -- "
                         f"held open, not auto-resolved")
        return f

    # -- AXIS 6: PROV export -- interop for free -----------------------------
    def to_prov(self) -> Dict:
        """minimal PROV-JSON-shaped dict: entities, agents, derivations."""
        return {
            "entity": {k: {"prov:label": it.claim,
                           "mode": it.mode, "year": it.year}
                       for k, it in self.items.items()},
            "agent": {s.name: {"prov:type": s.kind}
                      for s in self.sources.values()},
            "wasAttributedTo": [{"entity": k, "agent": it.source}
                                for k, it in self.items.items() if it.source],
            "wasDerivedFrom": [{"generatedEntity": k, "usedEntity": p}
                               for k, it in self.items.items()
                               for p in it.derived_from],
        }


# =============================================================================
# Demo -- cross-domain on purpose: a site reading, a family teaching,
# a medical rule, a model guess. one structure holds all four.
# =============================================================================
if __name__ == "__main__":
    c = Corpus()
    c.add_source(Source("operator", "person", track=[True, True, True, True]))
    c.add_source(Source("grandmother_line", "lineage", track=[True, True]))
    c.add_source(Source("county_office", "org", track=[True, False]))
    c.add_source(Source("assistant_model", "model", track=[]))

    c.add(Item("soil.bearing", "ground holds 80k lb rig without rutting",
               "measurement", "embodied", ["soil"], "direct_observation",
               source="operator", year=2026,
               corroborates=["soil.penetrometer"]))
    c.add(Item("soil.penetrometer", "240 kPa at 0.5 m",
               "measurement", "instrument_trace", ["soil"], "instrument",
               source="operator", year=2026, corroborates=["soil.bearing"]))
    c.add(Item("siting.bench", "never build below the second bench",
               "teaching", "oral", ["siting", "water"], "transmission",
               source="grandmother_line",
               chain=["grandmother", "mother", "operator"],
               corroborates=["siting.silt"]))
    c.add(Item("siting.silt", "silt lines on valley trees at first-bench height",
               "observation", "text", ["siting", "water"], "direct_observation",
               source="operator", year=2025, corroborates=["siting.bench"]))
    c.add(Item("med.aspirin", "county clinic protocol: daily aspirin for all "
               "over 60", "rule", "written" if False else "text",
               ["medicine"], "authority", source="county_office", year=1998))
    c.add(Item("model.span", "4 m max clear span for that timber section",
               "model_output", "text", ["structure"], "model_generated",
               source="assistant_model", year=2026))
    c.add(Item("plan.waste", "24800 J avoidable under code mode",
               "claim", "numeric", ["audit"], "inference", source="operator",
               year=2026, derived_from=["soil.bearing", "soil.penetrometer"]))

    print("=" * 66)
    print("INFO TAXONOMY -- one structure, four domains")
    print("=" * 66)
    for key in c.items:
        it = c.items[key]
        s = c.support(key)
        rel = c.sources[it.source].reliability() if it.source else None
        rel_s = f"{rel:.2f}" if rel is not None else "no track yet"
        print(f"\n  [{key}] {it.claim}")
        print(f"     type: {it.content}/{it.form}  about: {','.join(it.about)}")
        print(f"     mode: {it.mode}   source: {it.source} "
              f"(track record: {rel_s})")
        print(f"     support: {s['strength']} independent mode(s) "
              f"{s['independent_modes']}  echoes: {s['echoes']}")

    print("\n  backing of plan.waste (transitive):", c.backing("plan.waste"))

    print("\n" + "-" * 66)
    print("AUDIT (structure, never truth):")
    for fl in c.audit():
        print(f"   ! {fl}")

    print("\n" + "-" * 66)
    print("PROV export (interop):",
          len(c.to_prov()["wasDerivedFrom"]), "derivation edge(s) emitted")
    print("=" * 66)
