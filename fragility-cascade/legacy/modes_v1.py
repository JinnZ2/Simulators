#!/usr/bin/env python3
"""
modes.py -- harness for B. Zero rows.
CC0 / Public Domain.  stdlib-only.

The mode table always came with content. This is the harness ONLY:
zero rows, hard validation on registration, plus a self-audit that
reports the table's own blind spots.

ENFORCED at register (raises, does not register):
   reads_well / blind_to / decays_by / stays_fresh_by all non-empty
   -> a mode that won't state its blindness is a supremacy claim
      wearing a row.

CLOCK HANDSHAKE (new):
   decays_by       prose      WHAT erodes this mode's grasp
   half_life_days  number     its own blindness rate (self-paced)
   tracks          str        slaved to a clock.Volatility class
                              instead -- the mode doesn't decay on
                              its own schedule; it decays only as
                              the referent moves.
   neither set -> registers, LOUD, downstream reports UNDETERMINED.
   incomplete allowed. silent not.

ROW PROVENANCE:
   row_source / row_as_of on every mode row -- the mode table is
   itself a set of claims and ages like one.

AUDIT reports the table's OWN blind spot:
   for every blind_to declared by some mode, whether any OTHER
   mode's reads_well covers it (content-token overlap). Uncovered
   blindnesses name what the whole registered set fails to see --
   what to fetch a new mode row FOR.

BOUNDARY: this harness invents no rows. It refuses empty ones and
loud-flags incomplete ones. Semantic coverage is a token-overlap
heuristic; false positives and negatives are expected. Operator
tightens by editing prose (or later, by adding an explicit
`covers` field to Mode) -- neither happens here.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import re

# --- optional handshake with clock.py's Volatility table ---
try:
    from clock import VOLATILITY as _VOL
except ImportError:
    _VOL = {}


# =============================================================================
# The row
# =============================================================================
@dataclass(frozen=True)
class Mode:
    name: str
    reads_well: str
    blind_to: str
    decays_by: str
    stays_fresh_by: str
    half_life_days: Optional[float] = None
    tracks: Optional[str] = None
    row_source: Optional[str] = None
    row_as_of: Optional[str] = None      # ISO date string


# =============================================================================
# The registry (zero rows shipped)
# =============================================================================
MODES: Dict[str, Mode] = {}
_LOUD: List[str] = []


def register_mode(m: Mode) -> Mode:
    """The only door in. Raises on empty required prose; registers with
    loud accumulator on missing clock pairing."""
    required = {
        "name": m.name, "reads_well": m.reads_well, "blind_to": m.blind_to,
        "decays_by": m.decays_by, "stays_fresh_by": m.stays_fresh_by,
    }
    for k, v in required.items():
        if not v or not str(v).strip():
            raise ValueError(
                f"mode {m.name!r} missing required field {k!r} -- a mode "
                f"that won't state its blindness is a supremacy claim "
                f"wearing a row")

    # tracks must reference a known clock.Volatility class if set
    if m.tracks is not None and _VOL and m.tracks not in _VOL:
        _LOUD.append(
            f"[{m.name}] tracks={m.tracks!r} not in clock.VOLATILITY -- "
            f"register_volatility() first or fix the class name")

    # clock handshake: at least one of half_life_days / tracks
    if m.half_life_days is None and m.tracks is None:
        _LOUD.append(
            f"[{m.name}] neither half_life_days nor tracks set -- "
            f"downstream freshness will report UNDETERMINED")

    MODES[m.name] = m
    return m


def clear_registry():
    """Reset MODES and the loud accumulator. For test isolation."""
    MODES.clear()
    _LOUD.clear()


# =============================================================================
# Coverage heuristic (content-token overlap; explicit false-positive/negative)
# =============================================================================
_STOP = {
    "the", "a", "an", "of", "to", "in", "on", "at", "by", "for", "with",
    "from", "not", "is", "are", "and", "or", "that", "this", "its", "it",
    "as", "into", "over", "under", "any", "no", "each", "what", "how",
    "why", "which", "when", "where", "was", "were", "has", "have", "had",
    "own", "off", "out", "so", "just", "one", "own", "own",
}


def _content_tokens(s: str) -> set:
    words = re.findall(r"[a-z]+", s.lower())
    return {w for w in words if len(w) > 2 and w not in _STOP}


def _covers(reads_well: str, blind_to: str) -> bool:
    """Any content-token overlap counts as coverage. Heuristic.
    False positives when unrelated modes share generic words;
    false negatives when related modes use different vocabulary."""
    return bool(_content_tokens(reads_well) & _content_tokens(blind_to))


# =============================================================================
# The audit -- reports the table's own blind spot
# =============================================================================
def audit() -> Dict:
    """
    Structural audit of the currently-registered mode set.

    Returns:
      n_rows                how many modes registered
      loud                  accumulated warnings from register_mode()
      uncovered_blindness   for each mode, its blind_to plus the list of
                            OTHER modes whose reads_well covers it (by
                            token overlap); empty covered_by = uncovered
                            by anything in the table
      row_provenance        rows lacking row_source or row_as_of
      clock_pairing         which rows are self-paced / slaved / undetermined
    """
    uncovered: List[Dict] = []
    for name, m in MODES.items():
        others = [(o_name, o) for o_name, o in MODES.items() if o_name != name]
        covered_by = [o_name for o_name, o in others
                      if _covers(o.reads_well, m.blind_to)]
        uncovered.append({
            "mode": name,
            "blind_to": m.blind_to,
            "covered_by": covered_by,
        })

    undated = [n for n, m in MODES.items() if not m.row_as_of]
    unsourced = [n for n, m in MODES.items() if not m.row_source]
    self_paced = [(n, m.half_life_days) for n, m in MODES.items()
                  if m.half_life_days is not None and m.tracks is None]
    slaved = [(n, m.tracks) for n, m in MODES.items()
              if m.tracks is not None]
    undetermined = [n for n, m in MODES.items()
                    if m.half_life_days is None and m.tracks is None]

    return {
        "n_rows": len(MODES),
        "loud": list(_LOUD),
        "uncovered_blindness": uncovered,
        "row_provenance": {"undated": undated, "unsourced": unsourced},
        "clock_pairing": {
            "self_paced": self_paced,
            "slaved": slaved,
            "undetermined": undetermined,
        },
    }


def print_audit():
    a = audit()
    print(f"\n  n_rows: {a['n_rows']}")
    if a["loud"]:
        print("\n  LOUD:")
        for msg in a["loud"]:
            print(f"    ! {msg}")
    print("\n  clock_pairing:")
    if a["clock_pairing"]["slaved"]:
        print("    slaved to referent clock:")
        for n, t in a["clock_pairing"]["slaved"]:
            print(f"      {n} -> tracks {t!r}")
    if a["clock_pairing"]["self_paced"]:
        print("    self-paced (own half-life):")
        for n, h in a["clock_pairing"]["self_paced"]:
            print(f"      {n} -> {h:g} days")
    if a["clock_pairing"]["undetermined"]:
        print("    undetermined (neither clock set):")
        for n in a["clock_pairing"]["undetermined"]:
            print(f"      {n}")
    print("\n  uncovered_blindness (declared blind, no other mode reads it):")
    any_uncovered = False
    for u in a["uncovered_blindness"]:
        if not u["covered_by"]:
            any_uncovered = True
            print(f"    ! [{u['mode']}] {u['blind_to']}")
    if not any_uncovered:
        print("    (every declared blindness is covered by SOME other row)")
    if a["row_provenance"]["undated"]:
        print(f"\n  rows without row_as_of: {a['row_provenance']['undated']}")
    if a["row_provenance"]["unsourced"]:
        print(f"  rows without row_source: {a['row_provenance']['unsourced']}")


# =============================================================================
# Demo -- registers a few example rows to exercise validation + audit.
# The rows are ILLUSTRATIVE, not shipped defaults. Ships zero rows.
# =============================================================================
if __name__ == "__main__":
    print("=" * 66)
    print("modes.py -- harness for B. zero rows shipped.")
    print("=" * 66)

    # 1. attempt to register an invalid row -> ValueError expected
    print("\n[1] register with empty blind_to (expects ValueError):")
    try:
        register_mode(Mode(
            name="bad", reads_well="x", blind_to="", decays_by="x",
            stays_fresh_by="x"))
    except ValueError as e:
        print(f"    RAISED: {e}")

    # 2. properly-specified, slaved to a clock.Volatility class
    register_mode(Mode(
        name="direct_observation",
        reads_well="what is present here, now, to the senses",
        blind_to="what the senses don't span; one vantage",
        decays_by="the referent itself moving",
        stays_fresh_by="re-observing",
        tracks="event",
        row_source="operator", row_as_of="2026-06-30"))

    # 3. self-paced (own half-life, no clock slaving)
    register_mode(Mode(
        name="authority",
        reads_well="the issuer's consensus at issue time",
        blind_to="everything since issue; the issuer's own basis",
        decays_by="age -- the world moving on while the rule sits still",
        stays_fresh_by="re-derivation from ground truth",
        half_life_days=20 * 365,
        row_source="operator", row_as_of="2026-06-30"))

    # 4. neither clock set -> registers loud
    register_mode(Mode(
        name="transmission",
        reads_well="pattern integrated over more generations than any "
                   "instrument has run",
        blind_to="drift and loss in the chain; origin context fading",
        decays_by="broken lineage; practice detaching from telling",
        stays_fresh_by="living practice alongside the telling",
        row_source="operator", row_as_of="2026-06-30"))

    # 5. slaved to an unknown volatility class -> registers loud
    register_mode(Mode(
        name="misnamed_clock",
        reads_well="anything the operator points it at",
        blind_to="everything else",
        decays_by="the referent moving",
        stays_fresh_by="re-check",
        tracks="not_a_real_class",
        row_source="operator", row_as_of="2026-06-30"))

    print_audit()

    print("\n" + "=" * 66)
    print("harness posture: refuses empty rows, loud-flags incomplete ones,")
    print("names its own coverage gaps. content is the operator's.")
    print("=" * 66)
