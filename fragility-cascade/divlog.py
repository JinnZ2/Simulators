"""
divlog.py -- append-only divergence log. v1 against SPEC_drift_mesh. No deps.
CC0. stdlib only.

Entry is frozen; id = sha256 of all fields except `note` (operator-only field
never enters the identity). Append opens only in "a" -- there is no overwrite
path, and E3 greps for it. `supersedes` is a REVISIT pointer to a prior id,
not a delete: resolutions land as NEW entries that supersede, per D5.

    kind is classified from digest x band ONLY (D2, D4):
        same digest, same band       -> AGREEMENT_SAME_FACTS
        same digest, different band  -> DIVERGENCE_SAME_FACTS (module disagreement)
        different digest, same band  -> HOMOPLASY (convergent, not evidence)
        different digest, different  -> DIVERGENCE_DIFFERENT_INPUTS (separate bucket)

    residual(history) classifies the SHAPE of a history, never the severity:
        n == 0  -> EMPTY
        n == 1  -> NEW (not a verdict; D7)
        FLAT           -- all gaps equal (calibration offset)
        WALKING        -- diffs all non-negative or all non-positive (monotone)
        INTERMITTENT   -- diffs have BOTH signs (direction reverses)
        WIDENING       -- a governing channel appears in the later half that
                          was not in the earlier half (new channels, D1)

    OPEN_E9: the specific gap sequence [-1, 0, +2] lands as WALKING under this
    rule (monotone increasing). SPEC_intent for that sequence was INTERMITTENT.
    Held OPEN in OPEN_E9_walking_criterion.md; resolution comes as a NEW entry
    that supersedes the entry recording the divergence, per D5. No untracked
    edit.
"""

from dataclasses import dataclass, asdict, field, fields
from hashlib import sha256
from typing import List, Optional, Iterable
import json
import os

# --------------------------------------------------------------- entry kinds

KIND_DIVERGENCE_SAME_FACTS      = "DIVERGENCE_SAME_FACTS"
KIND_DIVERGENCE_DIFFERENT_INPUTS = "DIVERGENCE_DIFFERENT_INPUTS"
KIND_HOMOPLASY                  = "HOMOPLASY"
KIND_AGREEMENT_SAME_FACTS       = "AGREEMENT_SAME_FACTS"

KINDS = (KIND_DIVERGENCE_SAME_FACTS, KIND_DIVERGENCE_DIFFERENT_INPUTS,
         KIND_HOMOPLASY, KIND_AGREEMENT_SAME_FACTS)


def classify_kind(digest_a: str, digest_b: str,
                  band_a: str, band_b: str) -> str:
    """Classify the divergence pattern from digests+bands ONLY.
    No winner, no cause, no severity (D2, D4, D8)."""
    same_digest = (digest_a == digest_b)
    same_band = (band_a == band_b)
    if same_digest and same_band:
        return KIND_AGREEMENT_SAME_FACTS
    if same_digest and not same_band:
        return KIND_DIVERGENCE_SAME_FACTS
    if not same_digest and same_band:
        return KIND_HOMOPLASY
    return KIND_DIVERGENCE_DIFFERENT_INPUTS


# --------------------------------------------------------------------- entry

@dataclass(frozen=True)
class Entry:
    observed_at: str
    target: str                     # which target the divergence is about
    subject: str                    # what claim/thing is under audit

    axis_a: str                     # name of the first axis (module/mode/reading)
    axis_b: str
    kind: str                       # one of KINDS

    band_a: str                     # FRESH | DECAYING | STALE | EXPIRED | ...
    band_b: str

    digest_a: str                   # fingerprint of the facts axis_a used
    digest_b: str

    governing_a: Optional[str] = None
    governing_b: Optional[str] = None

    ref_version: Optional[str] = None
    phase_a: Optional[str] = None
    phase_b: Optional[str] = None

    supersedes: Optional[str] = None    # id of a prior entry this revisits
    note: str = ""                      # operator-only; never parsed;
                                        # NOT included in the id

    @property
    def id(self) -> str:
        """sha256 of all fields except `note`, truncated to 12 hex.
        `note` is operator-only and never parsed -- see D8. Freezing Entry
        makes the id stable for the object's lifetime."""
        d = {f.name: getattr(self, f.name) for f in fields(self)
             if f.name != "note"}
        blob = json.dumps(d, sort_keys=True, ensure_ascii=False,
                          default=str).encode("utf-8")
        return sha256(blob).hexdigest()[:12]


# --------------------------------------------------------------------- io

def to_json(e: Entry) -> str:
    d = asdict(e)
    d["id"] = e.id
    return json.dumps(d, sort_keys=True, ensure_ascii=False)


def from_json(line: str) -> Entry:
    d = json.loads(line)
    d.pop("id", None)                   # id is computed, not stored on Entry
    return Entry(**d)


def append(path: str, e: Entry) -> None:
    """Append one entry as one NDJSON line. Opens in 'a' only -- no
    overwrite path exists in this module (D5, E3)."""
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d)
    with open(path, "a", encoding="utf-8") as f:
        f.write(to_json(e) + "\n")


def load(path: str) -> List[Entry]:
    """Load the whole log. Empty file / missing file -> []."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [from_json(line) for line in f if line.strip()]


def history(entries: Iterable[Entry], subject: str) -> List[Entry]:
    """The baseline query: every entry recorded for a subject, in order.
    'Off the same way as in March, or is this new?' is answerable only via
    this list."""
    return [e for e in entries if e.subject == subject]


# --------------------------------------------------------------- residual

_BAND_ORD = {
    "FRESH": 4, "DECAYING": 3, "STALE": 2, "EXPIRED": 1,
    "UNDETERMINED": 0, "": 0, None: 0,
}


def _band_ord(b) -> int:
    return _BAND_ORD.get(b, 0)


def _gap(e: Entry) -> int:
    return _band_ord(e.band_a) - _band_ord(e.band_b)


def _governing_set(e: Entry) -> set:
    return {g for g in (e.governing_a, e.governing_b) if g}


def residual(history_or_iter: Iterable[Entry]) -> str:
    """Classify the SHAPE of a history. Never the severity (D6).

    EMPTY         n == 0
    NEW           n == 1                                            (D7)
    WIDENING      a governing channel present in the later half is absent
                  from the earlier half -- the divergence is spreading   (D1)
    FLAT          all gaps equal across history (calibration offset)
    WALKING       consecutive diffs all non-negative OR all non-positive
                  (monotone drift, one direction)
    INTERMITTENT  consecutive diffs contain BOTH signs (direction reverses)
    """
    entries = list(history_or_iter)
    n = len(entries)
    if n == 0:
        return "EMPTY"
    if n == 1:
        return "NEW"

    # WIDENING takes precedence -- a new channel is a structural spread,
    # not a mere drift in existing ones.
    half = n // 2 or 1
    early = set().union(*[_governing_set(e) for e in entries[:half]])
    late = set().union(*[_governing_set(e) for e in entries[half:]])
    if late - early:
        return "WIDENING"

    gaps = [_gap(e) for e in entries]
    if len(set(gaps)) == 1:
        return "FLAT"

    diffs = [gaps[i + 1] - gaps[i] for i in range(len(gaps) - 1)]
    has_pos = any(d > 0 for d in diffs)
    has_neg = any(d < 0 for d in diffs)
    if has_pos and has_neg:
        return "INTERMITTENT"
    return "WALKING"
