"""
instruments.py -- registry of measuring instruments that DO NOT YET EXIST. v1.
CC0. stdlib only. Phone-buildable.

WHY THIS MODULE EXISTS (D1)
    Today blind_to is a flat declared field. It hides a distinction that
    routes to different repairs. The measurement chain is

        phenomenon -> transducer -> channel -> reading

    Every drift-mesh axis (trace / phase / parity) checks from the CHANNEL
    rightward. A claim can lack evidence because nothing was ever built at
    the TRANSDUCER position -- a break upstream of any mode. Nothing feeds
    the mode, so no mode row can name it, so it reads as "unsupported" and
    is filed as fringe. That is a graph location the framework had no node
    for. This file is that node.

    Running example (operator's): human magnetoreception. Fields reported
    sensible in the head; no non-invasive instrument exists for the human
    pathway; therefore no channel; therefore "no evidence"; therefore
    fringe. The absence of evidence here is an absence of an INSTRUMENT.

NON-EXISTENCE IS TIMESTAMPED, NOT ESSENTIAL (D2)
    "Not conceivable" is the wrong frame. The state is "not in existence as
    of DATE, because X." X routes the repair. The state decays. It flips.
    Hence every entry carries as_of, and as_of is always an explicit
    argument (I7) -- this module never calls now().

WHAT THIS REGISTRY IS
    A proposal generator with a hard falsifier gate. A workbench.
    Every entry is UNVALIDATED_PENDING_FIELD, emitted FOR external
    validation by people in contact with the real world. It is not
    evidence, and it never becomes evidence in here.

THE REGISTRY'S OWN blind_to (D9, the recursion)
    You cannot enumerate instruments nobody has conceived. This module is
    structurally unable to close its own coverage, exactly as blind_to is
    unclosable one level down. Declared, not apologized for. See
    REGISTRY_BLIND_TO.

INVARIANTS: I5 append-only log reuse, I6 no verdict fields, I7 explicit now.
Ships with ZERO rows. Rows are field content, not architecture.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Tuple
import json
import divlog


# ---------------------------------------------------------------------------
# why_absent taxonomy (D3)
#
# Typed by WHAT PRODUCED THE ABSENCE, because each type has a different
# unlock and -- the load-bearing part -- a different ACTOR. The taxonomy
# exists to answer "whose move is it," not to grade the absence.
#
# The field is named why_absent and never `cause`: `cause` is a banned
# verdict field under I6, and the checker is right to ban it.
# ---------------------------------------------------------------------------
WHY_ABSENT: Dict[str, Dict[str, str]] = {
    "R1": {"label": "frontier",
           "unlock": "science reaches the effect the instrument would exploit",
           "actor": "NOT AI"},
    "R2": {"label": "framework-barred",
           "unlock": "a value-frame shifts, or the contest closes",
           "actor": "HUMANS -- NOT AI"},
    "R3": {"label": "uncombined",
           "unlock": "cross-DOMAIN transfer: every transduction principle "
                     "already exists somewhere; nobody recombined them for "
                     "THIS phenomenon in THIS field",
           "actor": "AI CAN"},
    "R4": {"label": "temporal",
           "unlock": "cross-TEMPORAL reach: a duration/cadence no current "
                     "instrument spans, or an instrument that existed in "
                     "another era and was disused",
           "actor": "AI CAN"},
    "R5": {"label": "specced-unbuilt",
           "unlock": "funding / fabrication",
           "actor": "BUILDER"},
    "R6": {"label": "exists-unapplied",
           "unlock": "point the existing instrument at this claim",
           "actor": "FIELD"},
}

# D4 -- AI's honest lane is R3 + R4, and they unify under REACH, not smarts.
# Humans are parochial in two directions: domain silos (R3) and recency bias
# (R4). A model holds the whole map and the whole timeline flat. The
# contribution is WIDER, not better. Recency bias is TEMPORAL, not moral:
# much of what gets filed R2 ("not respectable") is misfiled R4.
AI_LANE = ("R3", "R4")

# R2 resolution states (D6, D7)
OPEN = "OPEN"              # a settled barrier: harm named, party named
CONTESTED = "CONTESTED"    # a live disagreement BETWEEN value-frames
RESOLUTIONS = (OPEN, CONTESTED)

HANDOFF_STATE = "UNVALIDATED_PENDING_FIELD"

REGISTRY_BLIND_TO = (
    "instruments nobody has conceived -- unenumerable by construction",
    "invented principles that sound like real ones; the door checks that a "
    "principle is NAMED, not that it is real. Naming is the operator's and "
    "the field's job.",
    "value-frames not yet articulated by anyone, which cannot be recorded "
    "as priors under a CONTESTED entry",
    "phenomena with no reporter at all -- nobody has said 'I sense this', "
    "so no claim exists to hang an absent instrument on",
)


class IncompleteInstrument(ValueError):
    pass


class MissingFalsifier(IncompleteInstrument):
    """Its own exception type. (D5)

    Every entry is emitted for validation by others, by the scientific
    method, in the field. Without a falsifier there is nothing to hand
    over -- it is a story, not a proposal. Same door discipline as
    modes.py refusing a row with no blind_to. AI-generated R5 proposals
    pass through this identical door; being model-generated buys nothing.
    """


class ContestedEntry(ValueError):
    """Raised when a CONTESTED entry is malformed, never when it is unresolved.
    Unresolved is the correct state and is not an error."""


# ---------------------------------------------------------------------------
# Recorded prior for a CONTESTED entry (D8)
#
# Frames are RECORDED, never ranked. There is no ordering field here and
# none may be added. Evolution ran the experiment; every extant practice is
# a configuration physics did not veto. Ranking value-frames claims the
# universe's calculations up to now got it wrong, and no operator has
# standing for that. So: name the configurations, say where and when, hand
# it forward.
#
# The three operator verbs this dataclass implements:
#     LOOK BACK    -- provenance + era
#     HOLD OPEN    -- no ordering, no closer
#     HAND FORWARD -- tomorrow's frame decides on MORE evidence, not less
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Frame:
    name: str            # the frame, named as it names itself where possible
    practice: str        # what it does about the phenomenon in question
    provenance: str      # where this is recorded from
    era: str             # when. explicit; never inferred, never now()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Instrument:
    name: str

    # --- what it would do ------------------------------------------------
    measures: str          # the claim / phenomenon it would put a channel on
    transduces: str        # phenomenon -> signal: WHICH physical variable to
                           # WHICH readout. Vague here = no proposal.
    principle: str         # a NAMED real effect. Empty or hand-waving is
                           # magic and is refused at the door.
    blind_to: List[str]    # declared like every mode. Constitutive.
    falsifier: str         # an observation that would show this does NOT
                           # measure the claim. Hard requirement.

    # --- why it isn't here yet -------------------------------------------
    why_absent: str        # R1..R6
    as_of: str             # timestamped non-existence (D2, I7)

    # --- reach provenance -------------------------------------------------
    borrowed_from: List[str] = field(default_factory=list)
    # which existing instrument / domain / era it recombines. Required for
    # R3 and R4: a reach claim that cannot name what it reaches ACROSS is
    # not a reach claim.

    # --- R2 only ----------------------------------------------------------
    harm: str = ""            # the SPECIFIC harm the barrier prevents
    harmed_party: str = ""    # WHO is harmed
    resolution: str = ""      # OPEN | CONTESTED, R2 only
    frames: List[Frame] = field(default_factory=list)
    contest: str = ""         # what exactly the frames disagree ON

    # --- provenance of the ROW itself -------------------------------------
    row_source: Optional[str] = None
    notes: str = ""
    loud: List[str] = field(default_factory=list)

    @property
    def actor(self) -> str:
        return WHY_ABSENT[self.why_absent]["actor"]

    @property
    def held_open(self) -> bool:
        return self.why_absent == "R2" and self.resolution == CONTESTED

    def to_dict(self) -> dict:
        d = asdict(self)
        d["actor"] = self.actor
        d["state"] = HANDOFF_STATE
        return d


REGISTRY: Dict[str, Instrument] = {}

_REQUIRED = ("measures", "transduces", "principle", "falsifier",
             "why_absent", "as_of")

# Words that name no effect. A principle field holding one of these is a
# placeholder wearing a lab coat. Not exhaustive and cannot be -- see
# REGISTRY_BLIND_TO line 2.
_NON_PRINCIPLES = {"unknown", "novel", "new physics", "tbd", "n/a", "none",
                   "some effect", "quantum", "energy", "resonance"}


def _door(inst: Instrument) -> List[str]:
    """The hard door. Raises rather than registering a malformed proposal.

    Refusal is the whole point: a registry that accepts anything is a wish
    list, and a wish list handed to a field scientist wastes the one
    resource this design cannot manufacture -- their time.
    """
    loud: List[str] = []

    if not (inst.falsifier or "").strip():
        raise MissingFalsifier(
            f"instrument '{inst.name}': no falsifier. Nothing to hand to the "
            f"field. A proposal without a way to be wrong is a story. (D5)")

    for f in _REQUIRED:
        v = getattr(inst, f)
        if not v or (isinstance(v, str) and not v.strip()):
            raise IncompleteInstrument(
                f"instrument '{inst.name}': {f} is empty.")

    if not inst.blind_to:
        raise IncompleteInstrument(
            f"instrument '{inst.name}': blind_to is empty. Every channel is "
            f"blind somewhere; a proposal claiming otherwise is a supremacy "
            f"claim, refused here as in modes.py.")

    if inst.why_absent not in WHY_ABSENT:
        raise IncompleteInstrument(
            f"instrument '{inst.name}': why_absent='{inst.why_absent}' not in "
            f"{tuple(WHY_ABSENT)}.")

    if inst.principle.strip().lower() in _NON_PRINCIPLES:
        raise IncompleteInstrument(
            f"instrument '{inst.name}': principle='{inst.principle}' names no "
            f"effect. An unnamed principle is magic. (door rule, D5)")

    # R3/R4 are REACH claims. Name what is being reached across. (D4)
    if inst.why_absent in AI_LANE and not inst.borrowed_from:
        raise IncompleteInstrument(
            f"instrument '{inst.name}': {inst.why_absent} claims reach "
            f"({WHY_ABSENT[inst.why_absent]['label']}) but borrowed_from is "
            f"empty. A reach that cannot name what it reaches across is a "
            f"guess wearing a taxonomy code.")

    if inst.why_absent == "R2":
        loud += _r2_door(inst)
    else:
        if inst.resolution or inst.frames or inst.harm or inst.harmed_party:
            loud.append(
                f"{inst.why_absent} row carries R2-only fields "
                f"(resolution/frames/harm/harmed_party) -- ignored downstream")

    return loud


def _r2_door(inst: Instrument) -> List[str]:
    """R2 is the danger bin. (D6, D7)

    It holds two unlike things: arbitrary taboo, and load-bearing ethics.
    An entry must carry WHICH, and AI never overrules the second.

    The discriminator first proposed was 'names a specific harm and a
    harmed party'. The operator broke it: autopsy, fetal tissue, a
    stillborn eaten by the pack -- whether a harmed party exists there IS
    the contested question. The test smuggled in the thing it was meant to
    decide. Same failure shape as a detector that fires on surface form.

    Repair: a third state. Not 'settled ethics' and not 'mere fashion' --
    CONTESTED, a live disagreement BETWEEN value-frames. Held open. Logged,
    timestamped, frames named, never auto-resolved.

    NO AUTO-RECLASSIFICATION. An entry that is neither harm-named nor
    CONTESTED is REFUSED, not silently moved to R3/R4. The door declines;
    it does not decide. Moving it is an operator act, because deciding
    that a barrier is 'merely' fashion is itself a value judgment, and
    auto-resolution is exactly what this framework forbids everywhere else.
    """
    loud: List[str] = []

    if inst.resolution not in RESOLUTIONS:
        raise ContestedEntry(
            f"instrument '{inst.name}': why_absent=R2 requires resolution in "
            f"{RESOLUTIONS}. R2 is the danger bin; an unlabelled R2 row hides "
            f"load-bearing ethics and arbitrary taboo in one place. (D6)")

    if inst.resolution == OPEN:
        # The settled branch. Both fields required -- this is the version of
        # the harmed-party test that survives, because it is only applied
        # where the operator has already asserted the contest is NOT live.
        if not (inst.harm or "").strip() or not (inst.harmed_party or "").strip():
            raise ContestedEntry(
                f"instrument '{inst.name}': R2/OPEN requires BOTH harm and "
                f"harmed_party. If neither can be named, the row is not "
                f"settled -- it is either CONTESTED or it was never R2. "
                f"Reclassification is the operator's move, not the door's. "
                f"(D6: no auto-resolution)")
        loud.append(
            f"R2/OPEN: load-bearing ethical barrier. actor={inst.actor}. "
            f"AI hands this back untouched -- no repair route is offered.")

    if inst.resolution == CONTESTED:
        if len(inst.frames) < 2:
            raise ContestedEntry(
                f"instrument '{inst.name}': CONTESTED requires >= 2 frames "
                f"recorded. A contest with one side named is a verdict with "
                f"extra steps. (D8)")
        if not (inst.contest or "").strip():
            raise ContestedEntry(
                f"instrument '{inst.name}': CONTESTED requires `contest` -- "
                f"WHAT the frames disagree on. 'They disagree' is not a "
                f"record.")
        for fr in inst.frames:
            if not (fr.provenance or "").strip() or not (fr.era or "").strip():
                raise ContestedEntry(
                    f"instrument '{inst.name}': frame '{fr.name}' missing "
                    f"provenance or era. LOOK BACK is the only move available "
                    f"here; an undated frame is not a look back. (D8)")
        loud.append(
            f"R2/CONTESTED: held open. {len(inst.frames)} frames recorded, "
            f"none ranked. Not resolvable in this module, by construction.")

    return loud


def register(inst: Instrument) -> Instrument:
    """Register a proposal. Raises at the door rather than accepting a
    malformed one. Returns the instrument with loud lines attached."""
    inst.loud = list(inst.loud) + _door(inst)
    REGISTRY[inst.name] = inst
    return inst


# ---------------------------------------------------------------------------
# Reclassification -- the enforcement with teeth (D10)
#
# The dangerous move is not disagreement. It is a CONTESTED subject quietly
# relabelled R3 or R4 so the machinery routes around the disagreement while
# nobody is looking. That is burial by paperwork, and it is detectable,
# because it is just another syndrome: a classification that changed while
# the contest stayed open.
#
# So reclassify() cannot be called without a log path and an explicit
# observed_at. There is no silent path. The move is ALLOWED -- blocking it
# would be this module issuing a verdict on the operator -- but it cannot
# be made invisible.
# ---------------------------------------------------------------------------
RECLASSIFIED_WHILE_CONTESTED = "RECLASSIFIED_WHILE_CONTESTED"


def reclassify(name: str, new_why_absent: str, observed_at: str,
               log_path: str, note: str = "",
               contest_closed: bool = False) -> Tuple[Instrument, Optional[str]]:
    """Change an entry's why_absent. Returns (instrument, syndrome_id|None).

    contest_closed is an operator assertion, never inferred here. Asserting
    it does not close the contest -- it records that the operator says it
    closed, and the entry still logs.
    """
    if new_why_absent not in WHY_ABSENT:
        raise IncompleteInstrument(f"unknown why_absent '{new_why_absent}'")
    inst = REGISTRY[name]
    was_held_open = inst.held_open
    prior = inst.why_absent

    syndrome_id = None
    if was_held_open and new_why_absent != "R2" and not contest_closed:
        entry = divlog.Entry(
            observed_at=observed_at,
            target="why_absent",
            subject=name,
            axis_a=f"{prior}:{CONTESTED}",
            axis_b=new_why_absent,
            kind=RECLASSIFIED_WHILE_CONTESTED,
            note=note,
        )
        syndrome_id = divlog.append(log_path, entry)
        inst.loud.append(
            f"LOUD: {prior}/{CONTESTED} -> {new_why_absent} with contest still "
            f"open. Logged as {syndrome_id}. The frames remain recorded; the "
            f"route around them does not erase them.")

    inst.why_absent = new_why_absent
    if new_why_absent != "R2":
        inst.resolution = ""       # frames are KEPT. history is not deleted.
    return inst, syndrome_id


def record_frame(name: str, frame: Frame) -> Instrument:
    """Add a recorded prior to a CONTESTED entry. LOOK BACK.

    There is deliberately no close_contest(). Closing is not an operation
    this module has standing to perform, and providing a function for it
    would make the overreach a one-liner. A contest closes when an operator
    edits the entry to R2/OPEN with a harm and a party named, and that edit
    goes through the same door as everything else.
    """
    inst = REGISTRY[name]
    if not inst.held_open:
        raise ContestedEntry(
            f"'{name}' is not R2/CONTESTED; frames are only recorded against "
            f"a held-open contest.")
    inst.frames = list(inst.frames) + [frame]
    return inst


def emit(name: str) -> str:
    """Handoff record. JSON, one object, for a human in contact with the
    real world to accept or destroy. Carries state=UNVALIDATED_PENDING_FIELD
    and the falsifier, because the falsifier is what makes it hand-overable."""
    d = REGISTRY[name].to_dict()
    d["registry_blind_to"] = list(REGISTRY_BLIND_TO)
    return json.dumps(d, sort_keys=True, separators=(",", ":"))


def by_actor(actor: str) -> List[str]:
    """Route by whose move it is -- the operational point of the taxonomy."""
    return sorted(n for n, i in REGISTRY.items() if i.actor == actor)


def held_open() -> List[str]:
    return sorted(n for n, i in REGISTRY.items() if i.held_open)
