#!/usr/bin/env python3
"""
scaffold.py -- a nomenclatural code for claims.
CC0 / Public Domain. stdlib-only. imports info_taxonomy.

Linnaeus's durable contribution was not the tree. It was the CODE: stable
names, type specimens, priority rules, and a defined revision procedure.
The tree was discovered (and continuously revised); the code was scaffold,
and scaffold is what ports.

Information has no single natural joint -- type, mode, source and support are
orthogonal. But one axis genuinely NESTS: scope of applicability.

    occasion  < instance < class < regime < universal

It nests properly (a claim demoted from class survives at instance), it is
testable (promotion means surviving at the wider scope), and it pairs with
the type-specimen idea: every claim is ANCHORED to the originating
observation, so it is re-checked against the specimen, not against its own
restatement.

CLOCK SUBSTITUTION: a reasoner without continuous duration cannot NOTICE
staleness -- noticing requires having been present while a thing aged. So
every claim carries absolute anchors (as_of, volatility) and freshness is
computed, never felt. due() is arithmetic standing in for a clock.

BOUNDARY: promotion and demotion are ELIGIBILITY reports. Nothing is
auto-promoted -- widening a claim's scope is an act with consequences and
belongs to the operator. Demotion eligibility is reported the same way.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from info_taxonomy import Corpus, MODES

# =============================================================================
# RANKS -- the ladder. lower index = narrower scope.
# =============================================================================
RANKS: List[str] = ["occasion", "instance", "class", "regime", "universal"]

RANK_MEANING = {
    "occasion":  "holds at this moment, this reading",
    "instance":  "holds for this site / this specimen",
    "class":     "holds for this kind of site / material",
    "regime":    "holds within a stated range of conditions",
    "universal": "holds wherever the stated conditions are met",
}

# SEED -- promotion thresholds. structure is the contribution; the numbers
# are a starting policy and belong to the operator.
PROMOTION_RULE = {
    # target rank: (min distinct anchors, min independent modes)
    "instance":  (1, 1),
    "class":     (3, 2),
    "regime":    (5, 3),
    "universal": (8, 3),
}


@dataclass
class Anchor:
    """Type specimen: the concrete observation a claim is pinned to.
    A claim with no anchor cannot be re-checked -- only re-argued."""
    key: str                  # corpus item key of the originating observation
    where: str                # site / specimen identity
    mode: str                 # how that anchor was obtained
    as_of: Optional[float] = None   # decimal year


@dataclass
class Scoped:
    key: str
    statement: str
    rank: str
    anchors: List[Anchor] = field(default_factory=list)
    volatility: Optional[str] = None      # static | slow | seasonal | volatile
    as_of: Optional[float] = None
    counterexamples: List[str] = field(default_factory=list)
    stated_conditions: Optional[str] = None   # required at regime/universal


# =============================================================================
class Register:
    """The nomenclatural register: stable keys, anchors, ranks, revisions."""

    def __init__(self, corpus: Corpus, now: float = 2026.5,
                 volatility_yr: Dict[str, Optional[float]] = None):
        self.c = corpus
        self.now = now
        self.items: Dict[str, Scoped] = {}
        self.vol = volatility_yr or {"static": None, "slow": 50.0,
                                     "seasonal": 0.5, "volatile": 0.05}

    def register(self, s: Scoped):
        self.items[s.key] = s

    # -- clock substitution: freshness computed, never felt -----------------
    def due(self, key: str) -> Dict:
        s = self.items[key]
        scale = self.vol.get(s.volatility) if s.volatility else "UNSET"
        if s.volatility is None:
            return {"status": "UNRECORDED",
                    "detail": "no volatility class -- elapsed time cannot be "
                              "interpreted; record it"}
        if scale is None:
            return {"status": "no_expiry",
                    "detail": f"referent is {s.volatility}; elapsed time "
                              f"carries no decay signal"}
        if s.as_of is None:
            return {"status": "UNDATED",
                    "detail": "no as_of anchor -- a reasoner without duration "
                              "has nothing to compute against"}
        elapsed = self.now - s.as_of
        return {"status": "DUE" if elapsed > scale else "current",
                "detail": f"elapsed {elapsed:.2f}yr vs {s.volatility} scale "
                          f"{scale:g}yr",
                "next_check": s.as_of + scale}

    # -- promotion: eligibility only, never automatic ------------------------
    def promotion(self, key: str) -> Dict:
        s = self.items[key]
        i = RANKS.index(s.rank)
        if i == len(RANKS) - 1:
            return {"eligible": False, "detail": "already at widest rank"}
        target = RANKS[i + 1]
        need_anchors, need_modes = PROMOTION_RULE[target]
        places = {a.where for a in s.anchors}
        modes = {a.mode for a in s.anchors}
        # independence rule inherited: distinct MODES, echoes don't count
        ok = len(places) >= need_anchors and len(modes) >= need_modes
        missing = []
        if len(places) < need_anchors:
            missing.append(f"{need_anchors - len(places)} more distinct anchor(s)")
        if len(modes) < need_modes:
            missing.append(f"{need_modes - len(modes)} more independent mode(s)")
        if target in ("regime", "universal") and not s.stated_conditions:
            ok = False
            missing.append("stated conditions (required at regime and above -- "
                           "an unbounded universal claim cannot be falsified)")
        if s.counterexamples:
            ok = False
            missing.append(f"open counterexamples: {s.counterexamples}")
        return {"eligible": ok, "target": target,
                "have": f"{len(places)} anchor(s), {len(modes)} mode(s)",
                "missing": missing}

    # -- demotion: a counterexample inside the claimed scope ----------------
    def demotion(self, key: str) -> Dict:
        s = self.items[key]
        if not s.counterexamples:
            return {"required": False}
        i = RANKS.index(s.rank)
        # the widest rank that survives is the one its anchors still support
        places = {a.where for a in s.anchors}
        survives = "occasion"
        for r in RANKS[1:]:
            need_anchors, need_modes = PROMOTION_RULE[r]
            if len(places) >= need_anchors and \
               len({a.mode for a in s.anchors}) >= need_modes:
                survives = r
        target = RANKS[min(RANKS.index(survives), max(i - 1, 0))]
        return {"required": True, "from": s.rank, "to": target,
                "because": s.counterexamples,
                "note": "the claim is not refuted -- its SCOPE was overstated"}

    def report(self, key: str):
        s = self.items[key]
        d, p, dm = self.due(key), self.promotion(key), self.demotion(key)
        print(f"\n  [{s.key}] {s.statement}")
        print(f"     rank: {s.rank:9s} ({RANK_MEANING[s.rank]})")
        print(f"     anchors: {len(s.anchors)} "
              f"({', '.join(sorted({a.where for a in s.anchors})) or 'NONE'})")
        if not s.anchors:
            print(f"     ! no type specimen -- cannot be re-checked, only re-argued")
        print(f"     freshness: {d['status']:12s} {d['detail']}")
        if dm["required"]:
            print(f"     DEMOTION REQUIRED: {dm['from']} -> {dm['to']}")
            print(f"        because {dm['because']}; {dm['note']}")
        elif p.get("eligible"):
            print(f"     promotion: ELIGIBLE -> {p['target']} ({p['have']})")
        else:
            miss = "; ".join(p.get("missing", [])) or p.get("detail", "")
            print(f"     promotion: not yet -> {p.get('target','-')}  needs {miss}")


# =============================================================================
if __name__ == "__main__":
    c = Corpus(current_year=2026)
    r = Register(c, now=2026.5)

    r.register(Scoped(
        "latent.vap.water", "water vaporizes at 2.26 MJ/kg",
        rank="universal", volatility="static", as_of=1953.0,
        stated_conditions="1 atm, pure water",
        anchors=[Anchor("lab.a", "lab A", "experiment", 1953),
                 Anchor("lab.b", "lab B", "experiment", 1961),
                 Anchor("lab.c", "lab C", "instrument", 1974),
                 Anchor("field.1", "field kettle", "direct_observation", 2020)]))

    r.register(Scoped(
        "clay.sand.firms", "clay-sand mix firms under compaction",
        rank="instance", volatility="slow", as_of=2019.0,
        anchors=[Anchor("site.1", "site 1", "repeated_practice", 2019),
                 Anchor("site.2", "site 2", "direct_observation", 2021),
                 Anchor("site.3", "site 3", "instrument", 2024)]))

    r.register(Scoped(
        "soil.moisture.ok", "surface moisture supports compaction",
        rank="occasion", volatility="seasonal", as_of=2025.8,
        anchors=[Anchor("site.4", "site 4", "direct_observation", 2025.8)]))

    r.register(Scoped(
        "fill.required", "0.5 m imported fill is required",
        rank="regime", volatility="slow", as_of=1974.0,
        stated_conditions=None,
        counterexamples=["site.penetrometer 240 kPa native"],
        anchors=[]))

    print("=" * 70)
    print("SCAFFOLD -- scope ranks, type anchors, computed freshness")
    print("=" * 70)
    for k in r.items:
        r.report(k)

    print("\n" + "=" * 70)
    print("constant: universal, 4 anchors across 3 modes, static -> no expiry.")
    print("clay-sand: 3 anchors, 3 modes -> ELIGIBLE for promotion to class.")
    print("moisture: seasonal, 0.7yr elapsed -> DUE. young but expired.")
    print("fill rule: regime rank with NO anchor and an open counterexample")
    print("           -> demotion required. the claim isn't refuted; its")
    print("              SCOPE was overstated.")
    print("=" * 70)
