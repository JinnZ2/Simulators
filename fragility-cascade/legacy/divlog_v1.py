"""
divlog.py -- append-only NDJSON log of module disagreements. No deps.
CC0. stdlib only.

A log entry is a factual record of a divergence between two axes on the same
subject at one observed instant. The entry classifies the divergence's KIND
from digests+bands only; it never picks a winner, never assigns cause, never
grades severity.

    digest_a, digest_b        <- same facts, or different facts?
    band_a, band_b            <- the disagreement

    same digest + different band  -> DIVERGENCE_SAME_FACTS
                                     (real module disagreement)
    different digest + different  -> DIVERGENCE_DIFFERENT_INPUTS
                                     (different inputs; kept in a separate
                                      bucket so it can never masquerade as
                                      module disagreement)
    different digest + same band  -> HOMOPLASY
                                     (agreement reached from different inputs;
                                      convergent, cheap, not evidence)
    same digest + same band       -> AGREEMENT_SAME_FACTS
                                     (trivial agreement; logged so the
                                      denominator is honest)

residual(history) classifies the SHAPE of a history, never the severity:
    n == 0  -> EMPTY
    n == 1  -> NEW (not a verdict)
    FLAT     -- gap constant across history: calibration offset
    WALKING  -- gap drifts monotonically: real drift
    WIDENING -- the set of governing channels grows over time; the
                divergence is spreading to new channels
"""

from dataclasses import dataclass, asdict, field
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
    No winner, no cause, no severity."""
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

@dataclass
class Entry:
    observed_at: str
    target: str                     # which target the divergence is about
    subject: str                    # what claim/thing is under audit

    axis_a: str                     # name of the first axis (module/mode/reading)
    axis_b: str                     # name of the second axis
    kind: str                       # one of KINDS

    band_a: str                     # FRESH | DECAYING | STALE | EXPIRED | ...
    band_b: str

    digest_a: str                   # fingerprint of the facts axis_a used
    digest_b: str                   # fingerprint of the facts axis_b used

    governing_a: Optional[str] = None   # which channel drove axis_a's band
    governing_b: Optional[str] = None

    ref_version: Optional[str] = None   # what primary was at the time
    phase_a: Optional[str] = None       # entrainment phase for axis_a
    phase_b: Optional[str] = None       # entrainment phase for axis_b

    supersedes: Optional[str] = None    # id of a prior entry this revisits
                                        # (revisit, not overwrite)
    note: str = ""                      # operator-only; never parsed


# --------------------------------------------------------------------- io

def to_json(e: Entry) -> str:
    return json.dumps(asdict(e), sort_keys=True, ensure_ascii=False)


def from_json(line: str) -> Entry:
    return Entry(**json.loads(line))


def append(path: str, e: Entry) -> None:
    """Append one entry as one NDJSON line. Creates the file if absent."""
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d)
    with open(path, "a", encoding="utf-8") as f:
        f.write(to_json(e) + "\n")


def read(path: str) -> List[Entry]:
    """Read the whole log. Empty file / missing file -> []."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [from_json(line) for line in f if line.strip()]


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


def residual(history: Iterable[Entry]) -> str:
    """
    Classify the SHAPE of a history. Never the severity.

    EMPTY    n == 0
    NEW      n == 1 (not a verdict)
    FLAT     the gap between band_a and band_b is constant across history
             (calibration offset -- two modules disagree by a fixed amount)
    WALKING  the gap changes across history (real drift)
    WIDENING the set of governing channels seen in the later half strictly
             contains a channel absent from the earlier half (the divergence
             is spreading to new channels)
    """
    entries = list(history)
    n = len(entries)
    if n == 0:
        return "EMPTY"
    if n == 1:
        return "NEW"

    # WIDENING takes precedence: a new governing channel is a structural
    # spread, not a mere drift in existing ones.
    half = n // 2 or 1
    early = set().union(*[_governing_set(e) for e in entries[:half]])
    late = set().union(*[_governing_set(e) for e in entries[half:]])
    if late - early:
        return "WIDENING"

    gaps = [_gap(e) for e in entries]
    if len(set(gaps)) == 1:
        return "FLAT"
    return "WALKING"
