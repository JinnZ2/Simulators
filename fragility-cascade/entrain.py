"""
entrain.py -- the zeitgeber. v1 against SPEC_drift_mesh.
CC0. stdlib only. imports clock.

Peripheral oscillators (scaffold, revalidate, echo, ...) run free between
pulls. They are not forced into lockstep; they are pulled back on a schedule.

reference_version() fingerprints the CURRENT primary (clock.CHANNELS +
clock.VOLATILITY). Changing a channel or a volatility class changes the
string; every peripheral inside its interval flips to FREE_RUNNING regardless
of schedule (D10, I8, T6).

phase() reads:
    ENTRAINED     within interval AND ref_version matches current
    FREE_RUNNING  within interval BUT ref_version is stale (primary moved)
    DRIFTED       past interval
    NEVER         last_entrained is None -> LOUD, UNDETERMINED (I4)

entrain() records the pull (sets last_entrained + ref_version). It does NOT
overwrite anyone's readings (D11).
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, Dict, List
import hashlib, json

import clock


PHASE_ENTRAINED    = "ENTRAINED"
PHASE_FREE_RUNNING = "FREE_RUNNING"
PHASE_DRIFTED      = "DRIFTED"
PHASE_NEVER        = "NEVER"

PHASES = (PHASE_ENTRAINED, PHASE_FREE_RUNNING, PHASE_DRIFTED, PHASE_NEVER)


# ---------------------------------------------------------- peripherals

@dataclass
class Peripheral:
    name: str                             # "scaffold", "revalidate", "echo"
    entrain_interval_days: float          # how often it must re-read primary
    last_entrained: Optional[str] = None  # ISO date, None = never
    ref_version: Optional[str] = None     # version of primary it last read


PERIPHERALS: Dict[str, Peripheral] = {}


def register_peripheral(p: Peripheral) -> Peripheral:
    """The door. No arithmetic here; downstream reads compute against clock."""
    PERIPHERALS[p.name] = p
    return p


def clear_peripherals():
    """Test isolation."""
    PERIPHERALS.clear()


# ---------------------------------------------- reference_version, no args

def reference_version() -> str:
    """
    Deterministic fingerprint of the CURRENT primary state.

    Reads clock.CHANNELS (channel name + target) and clock.VOLATILITY
    (volatility name + span_days). Anything else changing in clock leaves
    this string unchanged; anything named in these two dicts changing DOES.

    12-char sha256. That is enough to detect any change; not enough to be
    mistaken for a claim about content (compare divlog.Entry.id).
    """
    channels = sorted((n, c.target) for n, c in clock.CHANNELS.items())
    vols = sorted((n, v.span_days) for n, v in clock.VOLATILITY.items())
    blob = json.dumps({"channels": channels, "vols": vols},
                      sort_keys=True, default=str)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


# ---------------------------------------------------- phase + entrain

@dataclass
class Phase:
    name: str                                    # one of PHASES
    days_since_entrained: Optional[float] = None
    interval: Optional[float] = None
    recorded_ref: Optional[str] = None
    current_ref: Optional[str] = None
    loud: List[str] = field(default_factory=list)


def _as_date(x) -> Optional[date]:
    if x is None:
        return None
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    return date.fromisoformat(str(x)[:10])


def _days_between(a, b) -> Optional[float]:
    da, db = _as_date(a), _as_date(b)
    if da is None or db is None:
        return None
    return float((db - da).days)


def phase(name: str, now: str) -> Phase:
    """
    Compute phase for a registered peripheral against the current primary.
    `now` is always an explicit argument -- I7, no implicit present tense.
    """
    p = PERIPHERALS.get(name)
    if p is None:
        raise KeyError(f"peripheral '{name}' not registered")

    current = reference_version()

    if p.last_entrained is None:
        return Phase(PHASE_NEVER, None, p.entrain_interval_days,
                     recorded_ref=p.ref_version, current_ref=current,
                     loud=[f"peripheral '{name}' NEVER entrained -- LOUD, "
                           "UNDETERMINED (I4)"])

    days = _days_between(p.last_entrained, now)
    if days is None:
        return Phase(PHASE_NEVER, None, p.entrain_interval_days,
                     recorded_ref=p.ref_version, current_ref=current,
                     loud=["cannot compute elapsed days"])

    within_interval = days <= p.entrain_interval_days

    if within_interval and p.ref_version == current:
        return Phase(PHASE_ENTRAINED, days, p.entrain_interval_days,
                     recorded_ref=p.ref_version, current_ref=current)

    if within_interval and p.ref_version != current:
        # primary moved under this peripheral; pull is DUE regardless of clock
        return Phase(PHASE_FREE_RUNNING, days, p.entrain_interval_days,
                     recorded_ref=p.ref_version, current_ref=current,
                     loud=[f"reference moved: recorded {p.ref_version!r} != "
                           f"current {current!r} -- pull DUE regardless of "
                           f"schedule (D10, T6)"])

    # past interval
    return Phase(PHASE_DRIFTED, days, p.entrain_interval_days,
                 recorded_ref=p.ref_version, current_ref=current,
                 loud=[f"past interval: {days:g}d > {p.entrain_interval_days:g}d"])


def entrain(name: str, now: str) -> Phase:
    """
    Record the pull: set last_entrained = now, ref_version = current primary.
    Returns the resulting phase (ENTRAINED by construction, unless the
    peripheral is absent). Does NOT touch any module's readings (D11).
    """
    p = PERIPHERALS.get(name)
    if p is None:
        raise KeyError(f"peripheral '{name}' not registered")
    p.last_entrained = str(_as_date(now))
    p.ref_version = reference_version()
    return phase(name, now)
