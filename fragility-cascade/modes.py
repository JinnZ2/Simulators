"""
modes.py -- mode-table harness. v2, built against the decay registry.
CC0. stdlib only.

A mode is an Umwelt. Its blind_to is not a limitation to be apologized for;
it is the shape of the world that mode inhabits. The tick runs on three cues
and is not thereby deficient. reads_well and blind_to are a PAIR -- two ends
of one sensitivity curve -- not a pro/con list.

v1 asked each row for one half-life. The registry has six channels, and a
row that states one of them has silently under-specified five. Fixed here:

    every channel is either PARAMETERIZED or DECLARED NOT APPLICABLE.
    silence is neither, and silence is what the audit hunts.

New required field, from signal detection theory:

    reads_well / blind_to   SENSITIVITY  -- what it can discriminate (d')
    criterion               BIAS         -- which way it errs when uncertain

These are independent. A mode can be highly sensitive and badly biased, and
a table that records only sensitivity will read the bias as sensitivity
failure. The two are never one number here, for the same reason source
track-record and claim support are never multiplied.

This file ships with ZERO rows. Rows are field content, not architecture.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict
import clock

REQUIRED = ("reads_well", "blind_to", "decays_by", "stays_fresh_by", "criterion")

# channel -> the Mode attribute that parameterizes it
CHANNEL_PARAM = {
    "time":         "mode_half_life_days",
    "disuse":       "practice_half_life_days",
    "use":          "retrieval_fidelity",
    "constancy":    "adaptation_half_life_days",
    "transmission": "hop_fidelity",
    "diffusion":    "field_mixing_half_life_days",
}


class IncompleteMode(ValueError):
    pass


@dataclass
class Mode:
    name: str

    # --- sensitivity (d') -----------------------------------------------
    reads_well: List[str]           # what it discriminates that others don't
    blind_to: List[str]             # what it structurally cannot see
                                    # constitutive, not deficient

    # --- decay, in words -------------------------------------------------
    decays_by: str                  # mechanism of erosion
    stays_fresh_by: str             # retest prescription; revalidate.py reuses it

    # --- bias -------------------------------------------------------------
    criterion: str = ""             # which way it errs when uncertain:
                                    # miss-prone, false-alarm-prone, or where
                                    # the threshold sits and who set it

    # --- decay, in parameters (one per registry channel) ------------------
    mode_half_life_days: Optional[float] = None          # time
    practice_half_life_days: Optional[float] = None      # disuse
    retrieval_fidelity: Optional[float] = None           # use
    adaptation_half_life_days: Optional[float] = None    # constancy
    hop_fidelity: Optional[float] = None                 # transmission
    field_mixing_half_life_days: Optional[float] = None  # diffusion

    tracks: Optional[str] = None    # slave time-decay to a clock.Volatility class

    # --- explicit inapplicability ----------------------------------------
    channels_na: Dict[str, str] = field(default_factory=dict)
    # channel name -> REASON it does not apply to this mode.
    # e.g. {"disuse": "instrument-mediated; no observer skill in the loop"}
    # A reason is required. "n/a" is not a reason.

    # --- provenance of the ROW itself -------------------------------------
    row_source: Optional[str] = None
    row_as_of: Optional[str] = None

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
                f"mode '{m.name}': {f} is empty. A row must state all five to "
                f"register. reads_well without blind_to is a supremacy claim; "
                f"sensitivity without criterion reads bias as blindness."
            )

    if m.tracks is not None and m.tracks not in clock.VOLATILITY:
        loud.append(f"tracks='{m.tracks}' not in clock.VOLATILITY -- "
                    f"register_volatility() first, or the slaving is dead")

    # per-channel: parameterized, declared NA with a reason, or silent
    for ch, attr in CHANNEL_PARAM.items():
        if ch not in clock.CHANNELS:
            continue
        has = getattr(m, attr) is not None
        na = m.channels_na.get(ch)
        if has and na:
            loud.append(f"channel '{ch}': parameterized AND declared "
                        f"not-applicable -- one of the two is wrong")
        elif not has and not na:
            if ch == "time" and m.tracks:
                continue        # time is covered by the volatility slaving
            tgt = clock.CHANNELS[ch].target
            loud.append(f"channel '{ch}' UNSTATED ({attr}) -- target '{tgt}' "
                        f"will read UNDETERMINED for every claim held by this "
                        f"mode; parameterize it or declare it not-applicable "
                        f"with a reason")
        elif na and not na.strip():
            loud.append(f"channel '{ch}': declared not-applicable with no "
                        f"reason -- inapplicability is a claim and needs one")

    for ch in m.channels_na:
        if ch not in CHANNEL_PARAM:
            loud.append(f"channels_na names unknown channel '{ch}'")

    if m.row_source is None or m.row_as_of is None:
        loud.append("row provenance incomplete (row_source / row_as_of) -- the "
                    "mode table is itself a set of claims and ages like one")

    return loud


def register_mode(m: Mode) -> Mode:
    """The door. Raises on the five. Flags LOUD on everything else."""
    m.loud = _validate(m)
    MODES[m.name] = m
    return m


# ------------------------------------------------------- clock integration

def to_observation(mode_name: str, now: str, **claim_facts) -> clock.Observation:
    """
    The single join between the mode table and the decay registry.

    The MODE supplies its own decay parameters. The CALLER supplies the
    claim-specific facts (as_of, last_practiced, retrievals, chain_hops,
    unchanged_since, independence_since, volatility). Anything neither
    supplies stays None and goes LOUD downstream -- never defaulted.
    """
    m = MODES.get(mode_name)
    o = clock.Observation(now=now)

    if m is None:
        for k, v in claim_facts.items():
            setattr(o, k, v)
        return o

    o.mode_half_life_days = m.mode_half_life_days
    if o.mode_half_life_days is None and m.tracks:
        v = clock.VOLATILITY.get(m.tracks)
        o.mode_half_life_days = v.span_days if v else None

    o.practice_half_life_days = m.practice_half_life_days
    o.retrieval_fidelity = m.retrieval_fidelity
    o.adaptation_half_life_days = m.adaptation_half_life_days
    o.hop_fidelity = m.hop_fidelity
    o.field_mixing_half_life_days = m.field_mixing_half_life_days

    for k, v in claim_facts.items():
        setattr(o, k, v)
    return o


def read(mode_name: str, now: str, **claim_facts) -> clock.Decay:
    """Mode row + claim facts -> per-target decay reading."""
    o = to_observation(mode_name, now, **claim_facts)
    d = clock.decay(o)
    m = MODES.get(mode_name)
    if m:
        for ch, reason in m.channels_na.items():
            d.loud.append(f"channel '{ch}' declared not-applicable for mode "
                          f"'{mode_name}': {reason}")
    return d


# ------------------------------------------------------------------- audit

def audit() -> List[str]:
    """Table-level report. Not a score. Names what the table cannot see."""
    out: List[str] = []
    if not MODES:
        return ["mode table EMPTY"]

    # channel coverage across the table
    for ch, attr in CHANNEL_PARAM.items():
        silent = [n for n, m in MODES.items()
                  if getattr(m, attr) is None and ch not in m.channels_na
                  and not (ch == "time" and m.tracks)]
        if silent:
            out.append(f"channel '{ch}' unstated in: {', '.join(sorted(silent))}")

    unprovenanced = [n for n, m in MODES.items() if not m.row_source]
    if unprovenanced:
        out.append(f"row unprovenanced: {', '.join(sorted(unprovenanced))}")

    nobias = [n for n, m in MODES.items() if not m.criterion.strip()]
    if nobias:
        out.append(f"criterion unstated: {', '.join(sorted(nobias))}")

    # the table's OWN blind spot: declared blind by some, read by none
    seen, blind = set(), set()
    for m in MODES.values():
        seen.update(x.lower().strip() for x in m.reads_well)
        blind.update(x.lower().strip() for x in m.blind_to)
    uncovered = sorted(blind - seen)
    if uncovered:
        out.append("declared blind, read by no mode in table: "
                   + ", ".join(uncovered))

    # degeneracy check: modes whose reads_well is a subset of another's
    #   identical coverage is REDUNDANCY (adds no robustness)
    #   different structure, same coverage is DEGENERACY (adds robustness)
    names = list(MODES)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            ra = {x.lower().strip() for x in MODES[a].reads_well}
            rb = {x.lower().strip() for x in MODES[b].reads_well}
            if ra and ra == rb:
                ba = {x.lower().strip() for x in MODES[a].blind_to}
                bb = {x.lower().strip() for x in MODES[b].blind_to}
                kind = "REDUNDANT" if ba == bb else "degenerate"
                out.append(f"{a} / {b}: identical reads_well -- {kind} "
                           + ("(same blind_to too: adds coverage, not robustness)"
                              if kind == "REDUNDANT"
                              else "(different blind_to: adds robustness)"))
    return out


# ---------------------------------------------------------------- rows: none
#
# register_mode(Mode(
#     name="",
#     reads_well=[],
#     blind_to=[],
#     decays_by="",
#     stays_fresh_by="",
#     criterion="",
#     mode_half_life_days=None,
#     practice_half_life_days=None,
#     retrieval_fidelity=None,
#     adaptation_half_life_days=None,
#     hop_fidelity=None,
#     field_mixing_half_life_days=None,
#     channels_na={},          # channel -> reason it does not apply
#     row_source="",
#     row_as_of="",
# ))
