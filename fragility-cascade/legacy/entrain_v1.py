"""
entrain.py -- zeitgeber for the divergence log. CC0. stdlib only.
imports divlog.

A subsystem entrained to a primary reference stays in phase with it; if the
primary shifts and the subsystem does not, the subsystem is DRIFTED. If it
was never entrained, it is FREE_RUNNING. If no primary exists at all, the
phase question is NEVER-mode.

    reference_version(state)  -- a stable fingerprint of the primary state
                                 captured at ONE instant. Every subsystem
                                 that claims to entrain to the primary should
                                 snapshot this fingerprint at read time.

    phase(recorded, current)  -- read at audit time:
        NEVER         current is None (there IS no primary to align with)
        FREE_RUNNING  recorded is None/empty (never claimed alignment)
        ENTRAINED     recorded == current
        DRIFTED       recorded != current (was aligned; no longer)

reference_version() is the ENFORCEMENT: it is deterministic, canonical-JSON
based, and one-way. A subsystem cannot lie about which primary state it was
reading. If it recorded no fingerprint, it never claimed alignment; if it
recorded one that doesn't match, the divergence is visible.
"""

from dataclasses import asdict, is_dataclass
from hashlib import sha256
from typing import Any, Optional
import json

import divlog

# --------------------------------------------------------------- fingerprint

def _canonical(x: Any):
    """Deterministic, order-independent representation of nested state."""
    if is_dataclass(x):
        x = asdict(x)
    if isinstance(x, dict):
        return {k: _canonical(v) for k, v in sorted(x.items())}
    if isinstance(x, (list, tuple)):
        return [_canonical(v) for v in x]
    if isinstance(x, set):
        return sorted(_canonical(v) for v in x)
    return x


def reference_version(state: Any, prefix: str = "ref") -> str:
    """
    Fingerprint of a primary's state. Deterministic, one-way, short.

    Two calls with the SAME state (same dict, same list order, same values)
    return the same string. Any change -- a value, an added key, a re-cut
    volatility class -- changes the string. Same posture as content hashing
    a git tree.
    """
    if state is None:
        return ""
    canonical = _canonical(state)
    blob = json.dumps(canonical, sort_keys=True, ensure_ascii=False,
                      default=str).encode("utf-8")
    return f"{prefix}:{sha256(blob).hexdigest()[:16]}"


# --------------------------------------------------------------------- phase

PHASE_ENTRAINED    = "ENTRAINED"
PHASE_FREE_RUNNING = "FREE_RUNNING"
PHASE_DRIFTED      = "DRIFTED"
PHASE_NEVER        = "NEVER"

PHASES = (PHASE_ENTRAINED, PHASE_FREE_RUNNING, PHASE_DRIFTED, PHASE_NEVER)


def phase(recorded: Optional[str], current: Optional[str]) -> str:
    """
    Compare a recorded fingerprint against the primary's CURRENT fingerprint.

    NEVER         there is no primary at all right now
    FREE_RUNNING  the reader never claimed to be aligned (recorded is None/"")
    ENTRAINED     the reader captured a fingerprint that matches the primary
                  as it stands now
    DRIFTED       the reader captured a fingerprint that no longer matches
    """
    if current is None or current == "":
        return PHASE_NEVER
    if recorded is None or recorded == "":
        return PHASE_FREE_RUNNING
    return PHASE_ENTRAINED if recorded == current else PHASE_DRIFTED


# ----------------------------------------------------- convenience on Entry

def phase_pair(entry: divlog.Entry, current_ref: Optional[str]):
    """Read phase_a and phase_b out of an existing Entry against the current
    primary. Useful for auditing a stored log after the primary has moved."""
    return (phase(entry.phase_a, current_ref),
            phase(entry.phase_b, current_ref))
