#!/usr/bin/env python3
"""
thermo_spine.py -- thread provenance through the whole stack.
CC0 / Public Domain.  stdlib-only.  imports thermo_know.

Every layer already handles values whose origin matters -- operator readings,
physical constants, code requirements, model guesses -- but the origin rides
in comments and discipline, not in structure. This spine makes it structure,
WITHOUT rewriting the eight working files: it is a registry that attaches
alongside. Tag a value once at entry; derivations auto-build inference
chains; any computed result can be asked "what modes back you, transitively?"

    spine.tag("site.soil_bearing", 240, how="instrument", year=2026)
    spine.tag("code.fill_depth",   0.5, how="authority",  year=1974)
    wd = spine.derive("audit.waste_delta", 24800,
                      parents=["code.fill_depth", "site.soil_bearing", ...])
    spine.report("audit.waste_delta")
        -> the headline number no longer floats free: it inherits the
           weakest link of everything it rests on (a 52-yr authority, here).

Invariants:
  * unrecorded provenance == unread field == empty dimension -> made LOUD.
    coverage() walks a thermo_pm System and flags every untagged resource.
  * a computed result IS an inference: derive() creates the Know item with
    parents automatically, so chains cannot silently break -- the chain is
    built by the act of computing.
  * weakest-link: a result's groundedness is bounded by its least-supported
    leaf input. backing() walks to the leaves and reads the mode census.

Bookkeeping note (mine, flagged as mine): one mode row is added here --
measured_constant -- for values like latent heats replicated across
independent labs and generations. Its blindness is real and stated:
the constant is solid; its APPLICABILITY at this site's conditions is
the assumption. The cultural cuts of the mode table remain the operator's.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from thermo_know import Corpus, Know, Mode, MODES

# -- bookkeeping mode for the spine's needs (flagged as assistant-added) ------
if "measured_constant" not in MODES:
    MODES["measured_constant"] = Mode(
        "measured_constant",
        reads_well="quantities replicated across independent labs/generations",
        blind_to="applicability at THIS site's temperature/pressure/purity",
        decays_by="site conditions leaving the constant's valid range",
        stays_fresh_by="checking range assumptions against site readings")


# =============================================================================
@dataclass
class Backing:
    key: str
    leaf_modes: Dict[str, int]        # mode -> count among leaf inputs
    independent: int                  # distinct modes at the leaves
    weakest: List[str]                # leaf keys that are single-mode + fragile
    flags: List[str]                  # provenance-audit flags inherited
    depth: int


class Spine:
    def __init__(self, current_year: int = 2026):
        self.corpus = Corpus()
        self.values: Dict[str, object] = {}
        self.year = current_year

    # -- entry points ---------------------------------------------------------
    def tag(self, key: str, value, how: str, year: Optional[int] = None,
            chain: List[str] = None, corroborates: List[str] = None,
            about: List[str] = None, note: str = "") -> object:
        """Attach provenance to a value at its point of entry. Returns the
        value unchanged so tagging can wrap assignments inline."""
        self.corpus.add(key, Know(
            claim=f"{key} = {value}", about=about or [key.split('.')[0]],
            how=how, chain=chain or [], year=year,
            corroborates=corroborates or [], note=note))
        self.values[key] = value
        return value

    def derive(self, key: str, value, parents: List[str],
               note: str = "") -> object:
        """A computed result is an inference. Parents recorded by the act of
        computing -- the chain cannot silently break."""
        missing = [p for p in parents if p not in self.corpus.items]
        self.corpus.add(key, Know(
            claim=f"{key} = {value}", about=[key.split('.')[0]],
            how="inference", parents=parents, year=self.year,
            note=note + (f" [MISSING PARENTS: {missing}]" if missing else "")))
        self.values[key] = value
        return value

    # -- coverage: unrecorded provenance made loud ----------------------------
    def coverage(self, sys=None) -> List[str]:
        """Walk a thermo_pm System (optional) and flag every resource whose
        quantity carries no provenance tag. Same move as UNREAD fields."""
        gaps = []
        if sys is not None:
            for name in sys.resources:
                if not any(k.endswith("." + name) or k == name
                           for k in self.corpus.items):
                    gaps.append(f"resource '{name}' has a quantity but no "
                                f"provenance -- who measured it, how, when?")
        gaps.extend(self.corpus.audit(self.year))
        return gaps

    # -- transitive backing ---------------------------------------------------
    def _leaves(self, key: str, seen: Set[str], depth: int = 0):
        k = self.corpus.items.get(key)
        if k is None or key in seen:
            return [], depth
        seen.add(key)
        if k.how != "inference" or not k.parents:
            return [key], depth
        out, maxd = [], depth
        for p in k.parents:
            if p not in self.corpus.items:
                out.append(f"<missing:{p}>")
                continue
            leaves, d = self._leaves(p, seen, depth + 1)
            out.extend(leaves)
            maxd = max(maxd, d)
        return out, maxd

    def backing(self, key: str) -> Backing:
        leaves, depth = self._leaves(key, set())
        census: Dict[str, int] = {}
        weakest: List[str] = []
        for leaf in leaves:
            if leaf.startswith("<missing:"):
                census["BROKEN_CHAIN"] = census.get("BROKEN_CHAIN", 0) + 1
                weakest.append(leaf)
                continue
            lk = self.corpus.items[leaf]
            census[lk.how] = census.get(lk.how, 0) + 1
            s = self.corpus.support(leaf)
            fragile = (lk.how == "model_generated" and s["strength"] <= 1) or \
                      (lk.how == "authority" and lk.year
                       and self.year - lk.year > 20) or \
                      (s["strength"] <= 1 and lk.how not in
                       ("measured_constant", "direct_observation",
                        "repeated_practice"))
            if fragile:
                weakest.append(leaf)
        # audit flags that touch any node in this tree
        tree = set(leaves) | {key}
        flags = [f for f in self.corpus.audit(self.year)
                 if any(t in f for t in tree if not t.startswith("<"))]
        return Backing(key, census, len(census), weakest, flags, depth)

    def report(self, key: str):
        b = self.backing(key)
        v = self.values.get(key, "?")
        print(f"\n  RESULT {key} = {v}")
        print(f"    rests on {sum(b.leaf_modes.values())} leaf input(s), "
              f"{b.independent} independent mode(s), depth {b.depth}:")
        for mode, n in sorted(b.leaf_modes.items()):
            blind = MODES[mode].blind_to if mode in MODES else "chain broken"
            print(f"       {mode:18s} x{n}   blind_to: {blind[:44]}")
        if b.weakest:
            print(f"    WEAKEST LINKS (bound the result's groundedness):")
            for w in b.weakest:
                print(f"       ! {w}")
        for f in b.flags:
            print(f"    audit: {f}")


# =============================================================================
# Demo -- the interrogation-site headline number, now carrying its chain
# =============================================================================
if __name__ == "__main__":
    sp = Spine()

    # entry-point tags: the operator's readings, the constants, the code, a guess
    sp.tag("site.soil_bearing_kPa", 240, how="instrument", year=2026,
           corroborates=["site.rig_test"])
    sp.tag("site.rig_test", "held 80k lb rig, no rutting",
           how="direct_observation", year=2026,
           corroborates=["site.soil_bearing_kPa"])
    sp.tag("const.diesel_J_per_L", 38.6e6, how="measured_constant")
    sp.tag("code.fill_depth_m", 0.5, how="authority", year=1974,
           note="county table; basis: none declared")
    sp.tag("model.span_guess_m", 4.0, how="model_generated")

    # computed results: derivations auto-chain
    sp.derive("plan.code_energy_J", 24800,
              parents=["code.fill_depth_m", "const.diesel_J_per_L"],
              note="diesel to truck+place mandated fill")
    sp.derive("plan.physics_energy_J", 0,
              parents=["site.soil_bearing_kPa", "site.rig_test"],
              note="native bearing adequate; no import needed")
    sp.derive("audit.waste_delta_J", 24800,
              parents=["plan.code_energy_J", "plan.physics_energy_J"],
              note="code-mode minus physics-mode")

    print("=" * 66)
    print("PROVENANCE SPINE -- the headline number carries its chain")
    print("=" * 66)
    sp.report("audit.waste_delta_J")

    print("\n" + "-" * 66)
    print("COVERAGE (unrecorded provenance made loud):")
    for g in sp.coverage():
        print(f"   ! {g}")

    print("\n" + "=" * 66)
    print("the waste delta now reads: rests on 1 aged authority (52 yr,")
    print("basis undeclared), 1 measured constant, and 2 mutually-")
    print("corroborating site readings. the number is the same 24800 J --")
    print("what changed is that its weakest link is VISIBLE at the point")
    print("of use, instead of buried three files upstream.")
    print("=" * 66)
