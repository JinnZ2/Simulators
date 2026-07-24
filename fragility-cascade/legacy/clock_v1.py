"""
clock.py -- shared volatility clock for the info_taxonomy ecosystem.
CC0. stdlib only. Domain-neutral.

Closes the seam: scaffold.py and revalidate.py each carried a private copy
of decay arithmetic. Both now import from here. Neither computes locally.

Two clocks compose, never merge:
    mode half_life      -- how fast the WAY OF KNOWING goes blind
    referent volatility -- how fast the THING ITSELF moves
Effective decay is the faster of the two, not their average.

`now` is always an explicit argument. There is no implicit present tense
here. Freshness is arithmetic over absolute anchors, not something felt.

No verdicts. Emits structure, numbers, and LOUD flags. Operator decides.
"""

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from typing import Optional, List, Dict

# ---------------------------------------------------------------- volatility

@dataclass(frozen=True)
class Volatility:
    """How fast the referent itself moves. Independent of how it was known."""
    name: str
    span_days: Optional[float]      # characteristic time to meaningful change
    reads: str                      # what stays true across that span
    examples: str

VOLATILITY: Dict[str, Volatility] = {}

def register_volatility(v: Volatility) -> Volatility:
    """The door. No supreme class; the table is meant to be re-cut per domain."""
    VOLATILITY[v.name] = v
    return v

for _v in [
    Volatility("constant",   None,        "holds until the substrate changes",
               "material densities, geometry, thermodynamic identities"),
    Volatility("structural", 365 * 25,    "holds across a generation of practice",
               "soil profile, watershed form, road grade, building envelope"),
    Volatility("regime",     365 * 5,     "holds while the governing conditions hold",
               "regulation, freight lane economics, species range"),
    Volatility("annual",     365,         "holds within a cycle, not across it",
               "seasonal reading, crop year, snowpack"),
    Volatility("seasonal",   90,          "holds within one phase of the cycle",
               "ice condition, forage state, road restriction"),
    Volatility("event",      1,           "holds only near the occasion",
               "weather, load status, dock queue"),
]:
    register_volatility(_v)

UNRECORDED = "UNRECORDED"

# --------------------------------------------------------------------- bands

BANDS = [          # (label, min remaining fraction)
    ("FRESH",     0.75),
    ("DECAYING",  0.35),
    ("STALE",     0.10),
    ("EXPIRED",   0.00),
]

def band_for(remaining: float) -> str:
    for label, floor in BANDS:
        if remaining >= floor:
            return label
    return "EXPIRED"

# ----------------------------------------------------------------- arithmetic

def _as_date(x) -> Optional[date]:
    if x is None:
        return None
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    return date.fromisoformat(str(x)[:10])

def elapsed_days(as_of, now) -> Optional[float]:
    a, n = _as_date(as_of), _as_date(now)
    if a is None or n is None:
        return None
    return float((n - a).days)

def effective_half_life(mode_half_life_days: Optional[float],
                        volatility_name: Optional[str]) -> tuple:
    """
    Returns (half_life_days_or_None, governing_source, loud[]).
    Faster clock governs. Either clock may be absent; both absent -> undetermined.
    """
    loud: List[str] = []
    v = VOLATILITY.get(volatility_name) if volatility_name else None
    if volatility_name in (None, UNRECORDED):
        loud.append("referent_volatility UNRECORDED -- referent clock missing, "
                    "decay computed from mode blindness alone")
    elif v is None:
        loud.append(f"volatility class '{volatility_name}' not in table -- "
                    "register_volatility() or re-cut for this domain")

    v_span = v.span_days if v else None
    m_span = mode_half_life_days

    if m_span is None:
        loud.append("mode half_life UNRECORDED -- mode table row incomplete")

    candidates = [(s, src) for s, src in
                  ((m_span, "mode"), (v_span, "referent")) if s is not None]
    if not candidates:
        return None, "undetermined", loud
    span, src = min(candidates, key=lambda c: c[0])
    return span, src, loud

# -------------------------------------------------------------------- report

@dataclass
class Freshness:
    as_of: Optional[str]
    now: Optional[str]
    elapsed_days: Optional[float]
    half_life_days: Optional[float]
    governing_clock: str            # "mode" | "referent" | "undetermined"
    half_lives_elapsed: Optional[float]
    remaining: Optional[float]      # 2 ** -half_lives_elapsed
    band: str                       # FRESH | DECAYING | STALE | EXPIRED | UNDETERMINED
    loud: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def freshness(as_of, now,
              mode_half_life_days: Optional[float] = None,
              volatility: Optional[str] = None) -> Freshness:
    """
    The only place decay is computed in this ecosystem.

    as_of      absolute anchor on the claim (required for any number)
    now        explicit present (never implicit -- caller supplies it)
    """
    loud: List[str] = []
    hl, src, hl_loud = effective_half_life(mode_half_life_days, volatility)
    loud += hl_loud

    el = elapsed_days(as_of, now)
    if el is None:
        loud.append("as_of UNRECORDED -- claim cannot be aged, only re-argued")
    elif el < 0:
        loud.append("as_of is later than now -- anchor or clock is wrong")

    if el is None or hl is None:
        return Freshness(_iso(as_of), _iso(now), el, hl, src,
                         None, None, "UNDETERMINED", loud)

    n = el / hl
    rem = 2.0 ** (-n)
    return Freshness(_iso(as_of), _iso(now), el, hl, src,
                     round(n, 4), round(rem, 4), band_for(rem), loud)

def _iso(x) -> Optional[str]:
    d = _as_date(x)
    return d.isoformat() if d else None

# ------------------------------------------------------------------ contract

# scaffold.py  : freshness() on each Anchor -> anchor still standing?
# revalidate.py: freshness() gates the temporal axis -> which of 5 outcomes
# Neither module redefines BANDS, half-life math, or the volatility table.
