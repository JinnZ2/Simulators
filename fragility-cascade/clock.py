"""
clock.py -- decay registry.
CC0. stdlib only. Domain-neutral.

v1 had one decay term: elapsed calendar time.
That was the mode-supremacy move performed on clocks.

Decay runs on at least six channels. Each is a different function of a
different variable, and for embodied and transmitted knowing, calendar
time is not the dominant one.

    time          calendar aging                      as_of
    disuse        observer out of practice            last_practiced
    use           retrieval rewrites the record       retrievals
    constancy     unchanging stimulus -> no signal     unchanged_since
    transmission  per-hop fidelity, error threshold    chain_hops
    diffusion     independence itself decaying         independence_since

CRITICAL -- channels do not all decay the same OBJECT:

    claim             the content is less likely to still hold
    mode_sensitivity  the reader can still be right and report nothing
    independence      content may be fine; the SUPPORT COUNT is not

Taking the minimum across channels that decay different objects is a
category error. The governing channel is computed WITHIN each target,
never across. A claim can be fresh, unreadable, and no longer
independently supported at the same time -- three separate readings with
three separate consequences.

register_decay_channel() is the door. Same commitment as the mode table:
every channel row must state what it measures and what it is blind to.

`now` is always an explicit argument. No implicit present tense.
No verdicts. Numbers, targets, and LOUD flags.
"""

from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from math import log
from typing import Optional, List, Dict, Callable, Tuple

# ---------------------------------------------------------------- volatility

@dataclass(frozen=True)
class Volatility:
    """How fast the referent itself moves. Independent of how it was known."""
    name: str
    span_days: Optional[float]
    reads: str
    examples: str

VOLATILITY: Dict[str, Volatility] = {}

def register_volatility(v: Volatility) -> Volatility:
    VOLATILITY[v.name] = v
    return v

for _v in [
    Volatility("constant",   None,     "holds until the substrate changes",
               "material densities, geometry, thermodynamic identities"),
    Volatility("structural", 365 * 25, "holds across a generation of practice",
               "soil profile, watershed form, road grade, building envelope"),
    Volatility("regime",     365 * 5,  "holds while governing conditions hold",
               "regulation, freight lane economics, species range"),
    Volatility("annual",     365,      "holds within a cycle, not across it",
               "seasonal reading, crop year, snowpack"),
    Volatility("seasonal",   90,       "holds within one phase of the cycle",
               "ice condition, forage state, road restriction"),
    Volatility("event",      1,        "holds only near the occasion",
               "weather, load status, dock queue"),
]:
    register_volatility(_v)

UNRECORDED = "UNRECORDED"

# --------------------------------------------------------------------- bands

BANDS = [("FRESH", 0.75), ("DECAYING", 0.35), ("STALE", 0.10), ("EXPIRED", 0.0)]

def band_for(remaining: Optional[float]) -> str:
    if remaining is None:
        return "UNDETERMINED"
    for label, floor in BANDS:
        if remaining >= floor:
            return label
    return "EXPIRED"

# --------------------------------------------------------------------- dates

def _as_date(x) -> Optional[date]:
    if x is None:
        return None
    if isinstance(x, datetime):
        return x.date()
    if isinstance(x, date):
        return x
    return date.fromisoformat(str(x)[:10])

def _iso(x) -> Optional[str]:
    d = _as_date(x)
    return d.isoformat() if d else None

def elapsed_days(as_of, now) -> Optional[float]:
    a, n = _as_date(as_of), _as_date(now)
    return None if (a is None or n is None) else float((n - a).days)

def _halflife_decay(elapsed: Optional[float], hl: Optional[float]):
    if elapsed is None or hl is None or hl <= 0:
        return None
    return 2.0 ** (-(elapsed / hl))

# --------------------------------------------------------------- observation

@dataclass
class Observation:
    """Everything the channels can read. Absent fields go LOUD, never default."""
    now: Optional[str] = None

    # time
    as_of: Optional[str] = None
    volatility: Optional[str] = None
    mode_half_life_days: Optional[float] = None

    # disuse -- observer as instrument
    last_practiced: Optional[str] = None
    practice_half_life_days: Optional[float] = None

    # use -- retrieval rewrites
    retrievals: Optional[int] = None
    retrieval_fidelity: Optional[float] = None      # retained per retrieval

    # constancy -- adaptation
    unchanged_since: Optional[str] = None
    adaptation_half_life_days: Optional[float] = None

    # transmission -- per-hop fidelity
    chain_hops: Optional[int] = None
    hop_fidelity: Optional[float] = None

    # diffusion -- independence aging
    independence_since: Optional[str] = None
    field_mixing_half_life_days: Optional[float] = None

# ------------------------------------------------------------------ channels

TARGETS = ("claim", "mode_sensitivity", "independence")

@dataclass
class DecayChannel:
    name: str
    target: str                 # WHAT this channel decays -- see TARGETS
    measures: str               # the variable it reads
    blind_to: str               # what it structurally cannot see
    fn: Callable                # Observation -> (remaining|None, loud[])
    note: str = ""

CHANNELS: Dict[str, DecayChannel] = {}

def register_decay_channel(c: DecayChannel) -> DecayChannel:
    """The door. Refuses a row that will not state its own blindness."""
    for f in ("measures", "blind_to"):
        if not getattr(c, f, "").strip():
            raise ValueError(f"channel '{c.name}': {f} is empty -- a decay "
                             "channel that will not state what it cannot see "
                             "is a supremacy claim wearing a row")
    if c.target not in TARGETS:
        raise ValueError(f"channel '{c.name}': target must be one of {TARGETS}")
    CHANNELS[c.name] = c
    return c

# --- time ------------------------------------------------------------------

def effective_half_life(mode_half_life_days, volatility_name) -> Tuple:
    """Mode blindness and referent motion compose. Faster governs."""
    loud: List[str] = []
    v = VOLATILITY.get(volatility_name) if volatility_name else None
    if volatility_name in (None, UNRECORDED):
        loud.append("referent_volatility UNRECORDED -- referent clock missing, "
                    "decay computed from mode blindness alone")
    elif v is None:
        loud.append(f"volatility class '{volatility_name}' not in table -- "
                    "register_volatility() or re-cut for this domain")
    if mode_half_life_days is None:
        loud.append("mode half_life UNRECORDED -- mode table row incomplete")

    cands = [(s, src) for s, src in
             ((mode_half_life_days, "mode"),
              (v.span_days if v else None, "referent")) if s is not None]
    if not cands:
        return None, "undetermined", loud
    span, src = min(cands, key=lambda c: c[0])
    return span, src, loud

def _time(o: Observation):
    hl, src, loud = effective_half_life(o.mode_half_life_days, o.volatility)
    el = elapsed_days(o.as_of, o.now)
    if el is None:
        loud.append("as_of UNRECORDED -- claim cannot be aged, only re-argued")
    elif el < 0:
        loud.append("as_of later than now -- anchor or clock is wrong")
    return _halflife_decay(el, hl), loud

register_decay_channel(DecayChannel(
    "time", "claim",
    measures="calendar days since the anchor, against the faster of mode "
             "half_life and referent volatility",
    blind_to="whether the observer is still competent, whether the record has "
             "been rewritten, and whether the reading was ever independent",
    fn=_time))

# --- disuse ----------------------------------------------------------------

def _disuse(o: Observation):
    loud = []
    if o.last_practiced is None:
        loud.append("last_practiced UNRECORDED -- observer-as-instrument "
                    "cannot be calibrated")
    if o.practice_half_life_days is None:
        loud.append("practice_half_life_days UNRECORDED -- skill decay rate "
                    "not stated for this mode")
    return _halflife_decay(elapsed_days(o.last_practiced, o.now),
                           o.practice_half_life_days), loud

register_decay_channel(DecayChannel(
    "disuse", "mode_sensitivity",
    measures="time the observer has been out of the practice the mode requires",
    blind_to="the referent entirely -- a fully-practiced observer reads a "
             "vanished referent at full sensitivity",
    fn=_disuse,
    note="a 20-year-old reading by someone still in daily practice decays "
         "differently from a 1-year-old reading by someone who left the work"))

# --- use -------------------------------------------------------------------

def _use(o: Observation):
    loud = []
    if o.retrievals is None:
        loud.append("retrievals UNRECORDED -- record may have been rewritten "
                    "an unknown number of times")
        return None, loud
    f = o.retrieval_fidelity
    if f is None:
        loud.append("retrieval_fidelity UNRECORDED -- per-retrieval retention "
                    "not stated")
        return None, loud
    if not 0 < f <= 1:
        loud.append("retrieval_fidelity outside (0,1]")
        return None, loud
    return f ** max(o.retrievals, 0), loud

register_decay_channel(DecayChannel(
    "use", "claim",
    measures="retrievals x per-retrieval retention; recall makes a record "
             "labile and rewrites it on storage",
    blind_to="elapsed time -- an untouched record scores perfect here at any age",
    fn=_use,
    note="dominant channel for oral and testimonial anchors; inert for "
         "instrumented ones"))

# --- constancy -------------------------------------------------------------

def _constancy(o: Observation):
    loud = []
    if o.unchanged_since is None:
        loud.append("unchanged_since UNRECORDED -- adaptation state unknown")
    if o.adaptation_half_life_days is None:
        loud.append("adaptation_half_life_days UNRECORDED -- mode may report "
                    "nothing while the referent is fully present")
    return _halflife_decay(elapsed_days(o.unchanged_since, o.now),
                           o.adaptation_half_life_days), loud

register_decay_channel(DecayChannel(
    "constancy", "mode_sensitivity",
    measures="duration of unchanging stimulus; receptors report change, not level",
    blind_to="the truth of the claim -- this channel falling to zero means the "
             "mode reports nothing, NOT that the referent is gone",
    fn=_constancy,
    note="a blind_to that only appears with duration; invisible at registration"))

# --- transmission ----------------------------------------------------------

def _transmission(o: Observation):
    loud = []
    if o.chain_hops is None:
        loud.append("chain_hops UNRECORDED -- chain depth not stored")
        return None, loud
    f = o.hop_fidelity
    if f is None:
        loud.append("hop_fidelity UNRECORDED -- per-hop retention not stated")
        return None, loud
    if not 0 < f <= 1:
        loud.append("hop_fidelity outside (0,1]")
        return None, loud
    return f ** max(o.chain_hops, 0), loud

def max_chain_hops(hop_fidelity: float, floor: float = 0.35) -> Optional[float]:
    """Eigen-style error threshold: depth past which content is not maintained."""
    if not 0 < hop_fidelity < 1 or not 0 < floor < 1:
        return None
    return log(floor) / log(hop_fidelity)

register_decay_channel(DecayChannel(
    "transmission", "claim",
    measures="chain depth x per-hop fidelity; above an error threshold content "
             "is not maintained across hops",
    blind_to="whether the chain is independent -- a perfectly faithful chain "
             "of one source is still one source",
    fn=_transmission,
    note="bounds chain DEPTH; the data processing inequality bounds support "
         "WIDTH; same graph, different limit"))

# --- diffusion -------------------------------------------------------------

def _diffusion(o: Observation):
    loud = []
    if o.independence_since is None:
        loud.append("independence_since UNRECORDED -- support count is being "
                    "treated as permanent")
    if o.field_mixing_half_life_days is None:
        loud.append("field_mixing_half_life_days UNRECORDED -- rate at which "
                    "sources read each other not stated for this domain")
    return _halflife_decay(elapsed_days(o.independence_since, o.now),
                           o.field_mixing_half_life_days), loud

register_decay_channel(DecayChannel(
    "diffusion", "independence",
    measures="time since independence was established, against the rate at "
             "which sources in this field read each other",
    blind_to="content entirely -- the claim may be perfectly true and fresh "
             "while its support count is no longer honest",
    fn=_diffusion,
    note="two sources independent in 2019 need not be independent now; the "
         "echo test is evaluated at an instant and then assumed permanent"))

# ------------------------------------------------------------------ readings

@dataclass
class ChannelReading:
    channel: str
    target: str
    remaining: Optional[float]
    band: str
    loud: List[str] = field(default_factory=list)

@dataclass
class Decay:
    now: Optional[str]
    channels: List[ChannelReading]
    governing: Dict[str, Optional[str]]     # target -> channel name
    band: Dict[str, str]                    # target -> band
    loud: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def decay(o: Observation, channels: Optional[List[str]] = None) -> Decay:
    """
    Reads every registered channel. Governing channel is the fastest WITHIN
    each target. Nothing is averaged across targets.
    """
    names = channels or list(CHANNELS)
    readings, loud = [], []
    for n in names:
        c = CHANNELS[n]
        rem, l = c.fn(o)
        readings.append(ChannelReading(
            n, c.target, None if rem is None else round(rem, 4),
            band_for(rem), l))

    governing, bands = {}, {}
    for t in TARGETS:
        live = [r for r in readings if r.target == t and r.remaining is not None]
        if not live:
            silent = [r.channel for r in readings if r.target == t]
            governing[t], bands[t] = None, "UNDETERMINED"
            if silent:
                loud.append(f"target '{t}': no channel computable "
                            f"({', '.join(silent)}) -- unaged, not fresh")
            continue
        g = min(live, key=lambda r: r.remaining)
        governing[t], bands[t] = g.channel, g.band
    return Decay(_iso(o.now), readings, governing, bands, loud)

def channel_table() -> List[dict]:
    """The registry as data. Every row states its own blindness."""
    return [{"channel": c.name, "target": c.target, "measures": c.measures,
             "blind_to": c.blind_to, "note": c.note} for c in CHANNELS.values()]

# --------------------------------------------------- v1 API (echo.py client)

@dataclass
class Freshness:
    as_of: Optional[str]
    now: Optional[str]
    elapsed_days: Optional[float]
    half_life_days: Optional[float]
    governing_clock: str
    half_lives_elapsed: Optional[float]
    remaining: Optional[float]
    band: str
    loud: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

def freshness(as_of, now, mode_half_life_days=None, volatility=None) -> Freshness:
    """Time channel only. Retained for callers holding no other inputs."""
    hl, src, loud = effective_half_life(mode_half_life_days, volatility)
    el = elapsed_days(as_of, now)
    if el is None:
        loud.append("as_of UNRECORDED -- claim cannot be aged, only re-argued")
    elif el < 0:
        loud.append("as_of later than now -- anchor or clock is wrong")
    rem = _halflife_decay(el, hl)
    n = None if (el is None or hl is None) else round(el / hl, 4)
    return Freshness(_iso(as_of), _iso(now), el, hl, src, n,
                     None if rem is None else round(rem, 4),
                     band_for(rem), loud)

# ------------------------------------------------------------------ contract

# scaffold.py   : decay() per Anchor -> is this anchor still standing?
# revalidate.py : governing channel per target routes the five outcomes
# echo.py       : freshness() on cut members -> retest queue
# modes.py      : supplies mode_half_life, practice_half_life, adaptation_half_life
#
# Nothing downstream redefines BANDS, half-life math, the volatility table,
# or the channel set.
