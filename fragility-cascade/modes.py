"""
modes.py -- mode-table harness + clock handshake.
CC0. stdlib only.

The four-field commitment from info_taxonomy.py is enforced here rather than
trusted: every row must state reads_well / blind_to / decays_by / stays_fresh_by.
A row missing any of the four does not register. That is the whole point of the
table -- a mode that cannot say what it is blind to is a supremacy claim wearing
a row.

New here (the clock handshake): decays_by is no longer free prose. It must
resolve to arithmetic, or say out loud that it cannot.

    decays_by       prose  -- WHAT erodes the reading (mechanism, human-readable)
    half_life_days  number -- HOW FAST that mode goes blind, or None
    tracks          str    -- name of a clock.Volatility class this mode's decay
                              is SLAVED TO, or None
                              (use when the mode does not decay on its own
                               schedule -- it decays only as its referent moves)

    half_life_days is None AND tracks is None  -> registers, flagged LOUD,
    and every freshness() call downstream reports UNDETERMINED for that mode.
    Incomplete is allowed. Silent is not.

This file ships with ZERO rows. Rows are field content, not architecture.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
import clock

REQUIRED = ("reads_well", "blind_to", "decays_by", "stays_fresh_by")


class IncompleteMode(ValueError):
    pass


@dataclass
class Mode:
    name: str

    # the four -- all mandatory, all non-empty
    reads_well: List[str]       # what this mode resolves that others don't
    blind_to: List[str]         # what it structurally cannot see. NOT "limitations".
    decays_by: str              # mechanism of erosion, in words
    stays_fresh_by: str         # the retest prescription -- reused by revalidate.py

    # clock handshake
    half_life_days: Optional[float] = None
    tracks: Optional[str] = None        # clock.VOLATILITY key

    # provenance of the ROW itself -- the table is a claim too
    row_source: Optional[str] = None    # who/what states this row
    row_as_of: Optional[str] = None     # ISO date

    notes: str = ""
    loud: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


MODES: Dict[str, Mode] = {}


def _validate(m: Mode) -> List[str]:
    loud: List[str] = []

    for f in REQUIRED:
        v = getattr(m, f)
        if not v or (isinstance(v, str) and not v.strip()):
            raise IncompleteMode(
                f"mode '{m.name}': {f} is empty. "
                f"A row must state all four to register."
            )

    if m.tracks is not None and m.tracks not in clock.VOLATILITY:
        loud.append(f"tracks='{m.tracks}' not in clock.VOLATILITY -- "
                    f"register_volatility() first, or the slaving is dead")

    if m.half_life_days is None and m.tracks is None:
        loud.append("no half_life_days and no tracks -- this mode has no clock; "
                    "freshness() will report UNDETERMINED for every claim held "
                    "by it until one is supplied")

    if m.half_life_days is not None and m.tracks is not None:
        loud.append("both half_life_days and tracks set -- clock.freshness() "
                    "takes the faster; confirm that is intended")

    if m.row_source is None or m.row_as_of is None:
        loud.append("row provenance incomplete (row_source / row_as_of) -- "
                    "the mode table is itself a set of claims and ages like one")

    return loud


def register_mode(m: Mode) -> Mode:
    """The door. Raises on the four. Flags LOUD on everything else."""
    m.loud = _validate(m)
    MODES[m.name] = m
    return m


def resolve_clock(mode_name: str, referent_volatility: Optional[str] = None):
    """
    Single call site joining the mode table to clock.py.
    Returns (half_life_days, volatility_name) ready for clock.freshness().

    A mode with tracks= and no half_life contributes no independent mode clock;
    its decay IS the referent's. A mode with half_life contributes its own, and
    clock.freshness() lets the faster of the two govern.
    """
    m = MODES.get(mode_name)
    if m is None:
        return None, referent_volatility or clock.UNRECORDED
    hl = m.half_life_days
    if hl is None and m.tracks:
        v = clock.VOLATILITY.get(m.tracks)
        hl = v.span_days if v else None
    return hl, referent_volatility or clock.UNRECORDED


def audit() -> List[str]:
    """Table-level report. Not a score. Names what the table cannot see."""
    out = []
    if not MODES:
        return ["mode table EMPTY"]
    clockless = [n for n, m in MODES.items()
                 if m.half_life_days is None and m.tracks is None]
    if clockless:
        out.append(f"no clock: {', '.join(clockless)}")
    unprovenanced = [n for n, m in MODES.items() if not m.row_source]
    if unprovenanced:
        out.append(f"row unprovenanced: {', '.join(unprovenanced)}")

    # what NO mode in this table claims to read -- the table's own blind spot
    seen, blind = set(), set()
    for m in MODES.values():
        seen.update(x.lower() for x in m.reads_well)
        blind.update(x.lower() for x in m.blind_to)
    uncovered = sorted(blind - seen)
    if uncovered:
        out.append("declared blind, read by no mode in table: " + ", ".join(uncovered))
    return out


# ---------------------------------------------------------------- rows: none
#
# register_mode(Mode(
#     name="",
#     reads_well=[],
#     blind_to=[],
#     decays_by="",
#     stays_fresh_by="",
#     half_life_days=None,
#     tracks=None,
#     row_source="",
#     row_as_of="",
# ))
