"""
divlog.py -- append-only divergence log. v1.
CC0. stdlib only. Phone-buildable.

The log is not a list of problems. It is a BASELINE. Its value is not any
single entry; it is the history, which lets a future reading ask "is this
divergence the same one as before, or is it new?" -- unanswerable if entries
are ever mutated.

INVARIANTS ENFORCED HERE (SPEC I5, I6, I7):
    - append-only: entries are frozen; the file is opened "a"/"r", never "w"
    - no verdict fields: no winner/correct/cause/severity/score/rank
    - explicit time: observed_at is always an argument, never now()
    - resolution is a NEW entry that `supersedes` a prior id, not an edit

residual() classifies the SHAPE of a disagreement history, never its severity,
and never which side is right.
"""

from dataclasses import dataclass, asdict, field
from typing import Optional, List
import json, hashlib

# Fields that would encode a verdict or an interior state. Forbidden. (I6)
_BANNED = ("winner", "correct", "cause", "severity", "score", "rank")


@dataclass(frozen=True)
class Entry:
    observed_at: str                 # explicit now (I7)
    target: str                      # claim / mode_sensitivity / independence
    subject: str                     # what was read
    axis_a: str                      # module or axis name
    axis_b: str                      # peer, or "PRIMARY" for a trace check
    kind: str                        # Syndrome kind, verbatim
    band_a: Optional[str] = None
    band_b: Optional[str] = None
    digest_a: str = ""
    digest_b: str = ""
    governing_a: Optional[str] = None
    governing_b: Optional[str] = None
    ref_version: str = ""
    phase_a: Optional[str] = None
    phase_b: Optional[str] = None
    supersedes: Optional[str] = None  # id of a prior entry this one revisits
    note: str = ""                    # operator field; free text; never parsed

    @property
    def id(self) -> str:
        d = asdict(self)
        d.pop("note")                 # note is not identity
        blob = json.dumps(d, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode()).hexdigest()[:12]

    def to_line(self) -> str:
        d = asdict(self)
        d["id"] = self.id
        return json.dumps(d, sort_keys=True, separators=(",", ":"))


def _guard(entry: Entry) -> None:
    # structural guarantee that no verdict field ever entered the dataclass
    for b in _BANNED:
        if hasattr(entry, b):
            raise ValueError(f"Entry carries banned verdict field '{b}' (I6)")


def append(path: str, entry: Entry) -> str:
    """Append one entry. Opens 'a' only. Returns the entry id. (I5)"""
    _guard(entry)
    with open(path, "a") as f:            # never "w"
        f.write(entry.to_line() + "\n")
    return entry.id


def load(path: str) -> List[Entry]:
    """Read entries in file order. Missing file -> empty, not an error."""
    out: List[Entry] = []
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                d.pop("id", None)         # id is derived, not stored as state
                out.append(Entry(**d))
    except FileNotFoundError:
        pass
    return out


def history(path: str, target: str, subject: str,
            axis_a: str, axis_b: str) -> List[Entry]:
    """
    The baseline query: the same pair, same subject, in time order.
    Pair is order-insensitive (a vs b == b vs a).
    """
    want = {axis_a, axis_b}
    rows = [e for e in load(path)
            if e.target == target and e.subject == subject
            and {e.axis_a, e.axis_b} == want]
    rows.sort(key=lambda e: e.observed_at)
    return rows


# ------------------------------------------------------------- residual

@dataclass
class Residual:
    shape: str                       # NEW / FLAT / WALKING / INTERMITTENT / WIDENING
    n: int
    read_ids: List[str] = field(default_factory=list)
    loud: List[str] = field(default_factory=list)


# canonical band ordering, for detecting a monotone slide (D6)
_ORDER = {"FRESH": 0, "DECAYING": 1, "STALE": 2, "EXPIRED": 3}


def residual(entries: List[Entry]) -> Residual:
    """
    Classify the SHAPE of a disagreement history. Not severity. Never a winner.
    Reads only band_a/band_b sequences and governing-channel spread.
    """
    ids = [e.id for e in entries]
    n = len(entries)

    if n < 2:
        return Residual("NEW", n, ids,
                        ["n<2: no baseline yet -- one disagreement is not a "
                         "distribution (D7)"])

    pairs = [(e.band_a, e.band_b) for e in entries]

    # FLAT: every entry is the same kind AND same band pair (stable offset)
    same_kind = len({e.kind for e in entries}) == 1
    if same_kind and len(set(pairs)) == 1:
        return Residual("FLAT", n, ids,
                        ["stable offset across history -- reads as calibration, "
                         "not signal"])

    # WALKING: the gap between the two sides moves monotonically
    #
    # OPEN / E9 -- see OPEN_E9_walking_criterion.md, divlog entry 03efe4e41e61.
    # This rule fires on ANY monotone gap sequence. At small n, monotone and
    # trending are near-indistinguishable by chance, so the criterion is
    # false-alarm-prone. The repair is a number (min run length, or a
    # noise-robust trend test) and that number is EMPIRICAL. Do not patch it
    # with a guess. Resolution = a new divlog entry superseding 03efe4e41e61
    # plus a versioned rule change.
    def gap(p):
        a, b = _ORDER.get(p[0]), _ORDER.get(p[1])
        return None if a is None or b is None else a - b
    gaps = [gap(p) for p in pairs]
    if all(g is not None for g in gaps) and len(set(gaps)) > 1:
        diffs = [gaps[i + 1] - gaps[i] for i in range(len(gaps) - 1)]
        if all(d >= 0 for d in diffs) or all(d <= 0 for d in diffs):
            return Residual("WALKING", n, ids,
                            ["band gap moves monotonically -- reads as real "
                             "drift, act (D6)"])

    # WIDENING: the set of governing channels involved grows over time
    govs = []
    for e in entries:
        g = {x for x in (e.governing_a, e.governing_b) if x}
        govs.append(g)
    running = set()
    growth = 0
    for g in govs:
        before = len(running)
        running |= g
        if len(running) > before:
            growth += 1
    if growth >= 2 and running and len(running) > len(govs[0]):
        return Residual("WIDENING", n, ids,
                        [f"divergence spreading across governing channels "
                         f"{sorted(running)} -- new mechanisms entering"])

    # otherwise: comes and goes, no trend
    return Residual("INTERMITTENT", n, ids,
                    ["appears and clears without a trend -- keep logging, no "
                     "baseline claim yet"])
