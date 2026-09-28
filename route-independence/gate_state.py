# SPDX-License-Identifier: CC0-1.0
"""gate_state.py -- AMENDMENT A-2 to FWO-5 / FWO-8 / A-1: gate state is time- and
jurisdiction-indexed; routes carry removal events.

    python3 gate_state.py             the fixtures, the events, the four expectations
    python3 gate_state.py --choices   every [CHOICE n] in force
    python3 test_gate_state.py        the checks; this module refuses --selftest

EXTENDS FWO-5 (dependency_chain_audit.py), FWO-8 (edge_taxonomy.py) and A-1
(settlement_split.py) and rebuilds none of them: every row is D.route()'s record,
carried through S.declare(), COPIED and given the amendment's fields.  The test asserts
by AST that no name of those three modules is defined here.

THE AMENDMENT'S OBSERVATION (section 1)
    A-1's F-A3 ("rainwater on own land, no permit regime") was CONSTRUCTED.  The clause
    "no permit regime" did the work and is false in named jurisdictions.  Where
    collection is restricted the route is gated, and the gate is a dollar fine,
    confiscation, escalation.  Subsistence routes that were ordinary practice are now
    closed or permit-gated: REMOVALS WITH DATES, not absent routes.

WHAT THIS ADDS, per route copy (section 3a)
    jurisdiction      required
    t_from, t_to      ISO date or None; the row is in force on [t_from, t_to)
    gate_state        OPEN | METERED_PERMISSION | PROHIBITED | DISCRETIONARY | UNKNOWN
                      UNKNOWN is the default and blocks scoring.  DISCRETIONARY: access
                      only at the gate-holder's pleasure, no enforceable claim (G-2).
    gate_instrument   statute / case / regulation id, or None
    gate_source       a section-2 source id, required unless UNKNOWN or the row is
                      tagged CONSTRUCTED_UNSOURCED
    gate_reading()    what the row READS: UNKNOWN where 3a says so (no jurisdiction,
                      no t, never migrated), else the declared state.  A row with no t
                      never reads OPEN, whatever was declared.

    gate_change_events (section 3b): route_id, jurisdiction, date, instrument,
                      from_state, to_state, source, grade.  Grade K stored, FLAGGED,
                      excluded from holds.  Direction is read off an enumerated
                      transition table [CHOICE 3]; closures and loosenings are counted
                      APART and never netted.

    obligation_origin NONE (section 3c): "no obligation present; origin inapplicable",
                      distinct from A-1's UNDECIDED ("not yet determined").  A row moves
                      UNDECIDED -> NONE only through declare_none() with stated grounds.
                      A-1's ORIGINS tuple is not edited; A-1's origin_tally() is not
                      called on a re-read case, since it has no key for NONE.

HOLDS
    A prediction holds at the grade of the weakest source it rests on: HELD(P) on
    primary text, HELD(S) where any input is a secondary summary.  Rows tagged
    CONSTRUCTED_UNSOURCED and grade-K rows or events are EXCLUDED from every hold;
    a prediction whose every input is excluded is NOT_EVALUABLE, never held.  Every
    source here is CARRIED: the egress allowlist refuses the statute, case and
    Wikisource hosts, so what this session read is the amendment's section 2 and
    nothing behind it.

CHOICES (printed by --choices; cited where each takes effect)
    1  a route that was never given gate fields reads UNKNOWN; the retired F-A3 is such
       a row and is kept as the record of the A-1 defect line, tagged CONSTRUCTED_UNSOURCED
    2  ISO reduced precision (YYYY, YYYY-MM) is admitted, the precision being the
       source's own; comparison is lexical on the ISO string; t_to is exclusive
    3  transition direction is an enumerated table: CLOSURE = OPEN -> any other, or
       METERED_PERMISSION -> PROHIBITED | DISCRETIONARY; LOOSENING the reverse pairs;
       PROHIBITED <-> DISCRETIONARY is LATERAL (not ordered); any UNKNOWN end is
       UNKNOWN_DIRECTION.  A table, not a rank.
    4  G-2 is graded P/S and carries hold grade S, the weaker; the court is carried as
       Common Pleas (peer-reviewed) and the conflict with the Wikipedia reading is an
       open record, not resolved here
    5  W-2 carries no date in section 2, so F-W3 has no t and READS UNKNOWN under 3a;
       the Utah statute year is not supplied from memory
    6  F-W4 takes t_from "2011" at year precision from W-3's own text ("SB 769 (2011)");
       the alternative reading (W-3 dates the HOA bar and not the cap's absence, so F-W4
       has no t and reads UNKNOWN) is printed beside it and moves no hold
    7  the 3c re-read is this session's reading with grounds per route; a route whose
       absence of obligation is stated in its own FWO-5 name moves to NONE; one whose
       medium or hop is undeclared stays UNDECIDED
    8  the requirement a fixture row serves (water, food) is declared from A-1's list;
       shelter has no sourced row here and E-A2-3 reports it NOT_EVALUABLE

KEY-HOLDER STATUS
    The amendment's section 5 is the EXPECTED block; the amendment was committed alone
    at 251e12a before this file existed (rule 1).  Inputs are the amendment's section 2,
    graded P / S / K by its author and CARRIED here unread (rule 2 met at grade S by the
    amendment's author; not re-read by this session).  Fail fixture: F-W1 vs F-W2 under
    the unamended code, plus a constructed all-OPEN set on which E-A2-3's falsifier fires
    (rule 3).  Failed predictions are printed first (rule 4).

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D  # noqa: E402  FWO-5, reused
import settlement_split as S        # noqa: E402  A-1, reused

STATES = ("OPEN", "METERED_PERMISSION", "PROHIBITED", "DISCRETIONARY", "UNKNOWN")
OPEN, METERED_PERMISSION, PROHIBITED, DISCRETIONARY, UNKNOWN_STATE = STATES
OPEN_STATES = (OPEN,)            # the only state a route is read as open in (E-A2-4)
GRADES = ("P", "S", "K", "P/S")
NONE_ORIGIN = "NONE"             # section 3c; not a member of S.ORIGINS, by design
CONSTRUCTED_UNSOURCED = "CONSTRUCTED_UNSOURCED"
EXPECTED_COMMIT_A2 = "251e12a"
REQUIREMENTS = S.BIOLOGICAL_LIST  # [CHOICE 8]

HB_16_1005_EFFECTIVE = "2016-08-10"
HB_16_1005_VERIFICATION = ("NOT_RUN: the statute host is not on the egress allowlist; the delivered date "
                           "is carried as delivered; a memory of the same date is grade K and is not a verification")

# ------------------------------------------------------- section 2, carried ---

SOURCES = {
    "G-1": {"grade": "P", "text": "England, gleaning before 1788: the customary license, Hale (Norfolk Summer "
                                  "Assizes 1668) as quoted in the Steel v Houghton report [Wikisource]"},
    "G-2": {"grade": "P/S", "text": "Steel v Houghton et Uxor (1788) 1 H Bl 51; 126 ER 32: no right at common law to "
                                    "glean in the harvest field, nor for the settled poor of a parish [P/S; swarb]",
            "conflict": {"wikipedia": "House of Lords", "king_lhr_doi_10.2307_743812": "Court of Common Pleas",
                         "carried": "Court of Common Pleas", "resolved": False}},   # [CHOICE 4]
    "G-3": {"grade": "K", "text": "Leviticus 19:9-10, 23:22; Deuteronomy 24:19-21: codified gleaning provision"},
    "W-1": {"grade": "S", "text": "Colorado, HB 16-1005 (2016); C.R.S. 37-96.5-103: residential rooftop collection "
                                  "up to 110 gal combined, max 2 containers; before 2016 effectively prohibited for "
                                  "most residential users [S, multiple]"},
    "W-2": {"grade": "S", "text": "Utah: collection up to 2,500 gal with registration; 100 gal without [S]"},
    "W-3": {"grade": "S", "text": "States with no volume cap on residential collection, e.g. Texas; SB 769 (2011) "
                                  "bars HOA prohibition [S]"},
}
NOT_SOURCED = (
    "US public-land foraging prohibitions and permit regimes (unit and regulation unnamed)",
    "UK Theft Act 1968 s.4(3), wild-plant carve-out [K]",
    "Colorado pre-2016 penalty schedule (fine amounts, confiscation) as statute text",
)

CHOICES = {
    1: "a route never given gate fields reads UNKNOWN; the retired F-A3 is kept, tagged CONSTRUCTED_UNSOURCED",
    2: "ISO reduced precision (YYYY, YYYY-MM) admitted at the source's own precision; lexical comparison; t_to exclusive",
    3: "direction from an enumerated transition table (CLOSURE / LOOSENING / LATERAL / UNKNOWN_DIRECTION); counts never netted",
    4: "G-2 carries hold grade S (the weaker of P/S); court carried as Common Pleas; the conflict is an open record",
    5: "W-2 carries no date, so F-W3 has no t and reads UNKNOWN under 3a; no Utah statute year supplied from memory",
    6: "F-W4 t_from '2011' at year precision from W-3's text; the no-t alternative reading (UNKNOWN) printed beside it",
    7: "3c re-read: a route whose own FWO-5 name states the absence moves to NONE; an undeclared medium or hop stays UNDECIDED",
    8: "requirement per fixture row declared from A-1's list; shelter has no sourced row and is NOT_EVALUABLE",
}


class GateError(ValueError):
    """A record the amendment's schema refuses; the message names the field."""


# ------------------------------------------------------------------ dates ---

_ISO = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")   # [CHOICE 2]


def _date(v, name, route_name):
    if v is None:
        return None
    if not isinstance(v, str) or not _ISO.match(v):
        raise GateError("%s on %r is an ISO date (YYYY, YYYY-MM or YYYY-MM-DD) or None; got %r" % (name, route_name, v))
    return v


def at(row, t):
    """Is the row in force at t?  [t_from, t_to); None is open-ended.  A row with no t
    at all is in force nowhere (it reads UNKNOWN by 3a)."""
    t = _date(t, "t", row.get("route", "?"))
    lo, hi = row.get("t_from"), row.get("t_to")
    if lo is None and hi is None:
        return False
    if lo is not None and t < lo:
        return False
    if hi is not None and t >= hi:
        return False
    return True


# ---------------------------------------------------------------- sources ---

def hold_grade(source_id):
    """P or S for a source a hold may rest on; None for grade K (excluded) or unknown."""
    src = SOURCES.get(source_id)
    if src is None:
        return None
    g = src["grade"]
    if g == "P":
        return "P"
    if g in ("S", "P/S"):
        return "S"     # [CHOICE 4]
    return None


def weakest(grades):
    """The hold grade a set of inputs supports: P only when every input is P; S when any
    is S; None when the set is empty."""
    grades = [g for g in grades]
    if not grades:
        return None
    return "S" if "S" in grades else "P"


# ------------------------------------------------------------------- rows ---

def gate(route, route_id, jurisdiction, t_from, t_to, gate_state, gate_instrument, gate_source,
         requirement=None, tag=None, note=""):
    """Give a COPY of an FWO-5 / A-1 route the amendment's gate fields.

    jurisdiction is required; a row tagged CONSTRUCTED_UNSOURCED or declared UNKNOWN may
    carry gate_source None; every other row names a section-2 source.
    """
    name = route["route"]
    if not isinstance(route_id, str) or not route_id:
        raise GateError("route_id is required on %r" % name)
    if not isinstance(jurisdiction, str) or not jurisdiction.strip():
        raise GateError("jurisdiction is required on %r (3a)" % name)
    if gate_state not in STATES:
        raise GateError("gate_state on %r is one of %s; got %r" % (name, STATES, gate_state))
    lo, hi = _date(t_from, "t_from", name), _date(t_to, "t_to", name)
    if lo is not None and hi is not None and not lo < hi:
        raise GateError("t_from < t_to on %r; got %r, %r" % (name, lo, hi))
    if tag not in (None, CONSTRUCTED_UNSOURCED):
        raise GateError("tag on %r is None or %s" % (name, CONSTRUCTED_UNSOURCED))
    if gate_source is None:
        if gate_state != UNKNOWN_STATE and tag != CONSTRUCTED_UNSOURCED:
            raise GateError("gate_source is required on %r unless gate_state is UNKNOWN or the row is tagged %s"
                            % (name, CONSTRUCTED_UNSOURCED))
    elif gate_source not in SOURCES:
        raise GateError("gate_source on %r is a section-2 id %s; got %r" % (name, sorted(SOURCES), gate_source))
    if requirement is not None and requirement not in REQUIREMENTS:
        raise GateError("requirement on %r is one of %s or None; got %r" % (name, REQUIREMENTS, requirement))
    out = dict(route)
    out["route_id"] = route_id
    out["jurisdiction"] = jurisdiction
    out["t_from"], out["t_to"] = lo, hi
    out["gate_state"] = gate_state
    out["gate_instrument"] = gate_instrument
    out["gate_source"] = gate_source
    out["gate_grade"] = None if gate_source is None else SOURCES[gate_source]["grade"]
    out["gate_tag"] = tag
    out["requirement"] = requirement
    out["gate_note"] = note
    out["hold_eligible"] = (tag is None and gate_source is not None and hold_grade(gate_source) is not None)
    return out


def gate_reading(row):
    """What a row READS.  UNKNOWN where 3a says so; never OPEN without a jurisdiction and a t."""
    if "gate_state" not in row:
        return UNKNOWN_STATE                                   # [CHOICE 1]
    if not row.get("jurisdiction"):
        return UNKNOWN_STATE
    if row.get("t_from") is None and row.get("t_to") is None:
        return UNKNOWN_STATE
    return row["gate_state"]


def is_open(reading):
    return reading in OPEN_STATES


def reading_at(rows, route_id, jurisdiction, t):
    """The reading of one route in one jurisdiction at t: the in-force row's reading,
    NO_ROW when none covers t, CONFLICT when more than one does."""
    mine = [r for r in rows if r.get("route_id") == route_id and r.get("jurisdiction") == jurisdiction]
    if not mine:
        return ("NO_ROW", None)
    hits = [r for r in mine if at(r, t)]
    if not hits:
        no_t = [r for r in mine if r.get("t_from") is None and r.get("t_to") is None]
        if no_t:
            return (gate_reading(no_t[0]), no_t[0])   # 3a: a row with no t reads UNKNOWN, at every t
        return ("NO_ROW_AT_T", None)
    if len(hits) > 1:
        return ("CONFLICT", hits)
    return (gate_reading(hits[0]), hits[0])


def separating_fields(a, b):
    """Keys on which two records differ."""
    return sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))


READING_FIELDS = ("gate_state",)
INDEX_FIELDS = ("t_from", "t_to", "jurisdiction")
LABEL_FIELDS = ("gate_instrument", "gate_source", "gate_grade", "gate_note", "hold_eligible", "route_id")


# ----------------------------------------------------------------- events ---

CLOSURES = {(OPEN, METERED_PERMISSION), (OPEN, PROHIBITED), (OPEN, DISCRETIONARY),
            (METERED_PERMISSION, PROHIBITED), (METERED_PERMISSION, DISCRETIONARY)}       # [CHOICE 3]
LOOSENINGS = set((b, a) for a, b in CLOSURES)
DIRECTIONS = ("CLOSURE", "LOOSENING", "LATERAL", "UNKNOWN_DIRECTION")


def direction(from_state, to_state):
    if UNKNOWN_STATE in (from_state, to_state):
        return "UNKNOWN_DIRECTION"
    if (from_state, to_state) in CLOSURES:
        return "CLOSURE"
    if (from_state, to_state) in LOOSENINGS:
        return "LOOSENING"
    return "LATERAL"


def event(route_id, jurisdiction, date, instrument, from_state, to_state, source, note=""):
    """One gate_change_events row.  Grade is read from the source table; K is stored and
    flagged and never enters a hold.  date None is an UNDATED event, flagged."""
    for nm, v in (("route_id", route_id), ("jurisdiction", jurisdiction)):
        if not isinstance(v, str) or not v:
            raise GateError("%s is required on an event" % nm)
    for nm, st in (("from_state", from_state), ("to_state", to_state)):
        if st not in STATES:
            raise GateError("%s on event %r is one of %s; got %r" % (nm, route_id, STATES, st))
    if from_state == to_state:
        raise GateError("event %r: from_state and to_state are equal; not a change" % route_id)
    d = _date(date, "date", route_id)
    if source == CONSTRUCTED_UNSOURCED:
        grade = None
    elif source in SOURCES:
        grade = SOURCES[source]["grade"]
    else:
        raise GateError("source on event %r is a section-2 id or %s; got %r" % (route_id, CONSTRUCTED_UNSOURCED, source))
    return {
        "route_id": route_id, "jurisdiction": jurisdiction, "date": d, "instrument": instrument,
        "from_state": from_state, "to_state": to_state, "source": source, "grade": grade,
        "direction": direction(from_state, to_state),
        "flagged": (grade == "K"), "undated": d is None,
        "hold_eligible": (grade is not None and grade != "K" and d is not None), "note": note,
    }


def tally_events(events, jurisdiction=None, route_id=None):
    """Counts per direction over hold-eligible events, with the excluded ones counted
    apart.  Nothing is netted."""
    out = dict((d, 0) for d in DIRECTIONS)
    out["excluded_k"] = 0
    out["excluded_unsourced"] = 0
    out["excluded_undated"] = 0
    for e in events:
        if jurisdiction is not None and e["jurisdiction"] != jurisdiction:
            continue
        if route_id is not None and e["route_id"] != route_id:
            continue
        if e["source"] == CONSTRUCTED_UNSOURCED:
            out["excluded_unsourced"] += 1
            continue
        if e["grade"] == "K":
            out["excluded_k"] += 1
            continue
        if e["undated"]:
            out["excluded_undated"] += 1
            continue
        out[e["direction"]] += 1
    return out


def route_count(rows, jurisdiction, t):
    """Distinct route_ids with a row in force at t in the jurisdiction, whatever the
    state.  The count E-A2-2 says misses a removal."""
    return len(set(r["route_id"] for r in rows if r.get("jurisdiction") == jurisdiction and at(r, t)))


def events_derived(rows):
    """Change events implied by consecutive rows of one (route_id, jurisdiction) whose
    intervals meet: the boundary date, from the earlier state to the later.  A
    derivation, compared against the declared table; never a substitute for it."""
    by = {}
    for r in rows:
        if "route_id" not in r:
            continue
        by.setdefault((r["route_id"], r["jurisdiction"]), []).append(r)
    out = []
    for (rid, jur), rs in sorted(by.items()):
        rs = sorted(rs, key=lambda r: (r["t_from"] is not None, r["t_from"] or ""))
        for a, b in zip(rs, rs[1:]):
            if a["t_to"] is not None and a["t_to"] == b["t_from"] and a["gate_state"] != b["gate_state"]:
                out.append({"route_id": rid, "jurisdiction": jur, "date": b["t_from"],
                            "from_state": a["gate_state"], "to_state": b["gate_state"],
                            "instrument": b["gate_instrument"], "source": b["gate_source"]})
    return out


def events_reconcile(declared, derived):
    """Which derived events have a declared row on (route_id, jurisdiction, date, from, to),
    and which declared dated events have no derivation from the rows."""
    key = lambda e: (e["route_id"], e["jurisdiction"], e["date"], e["from_state"], e["to_state"])  # noqa: E731
    dec = set(key(e) for e in declared if e["date"] is not None)
    der = set(key(e) for e in derived)
    return {"derived_declared": sorted(der & dec), "derived_undeclared": sorted(der - dec),
            "declared_underived": sorted(dec - der)}


# ------------------------------------------------------------- section 3c ---

def declare_none(route, grounds):
    """Move an UNDECIDED A-1 row to NONE on stated grounds.  Only an UNDECIDED row moves;
    a row already decided is refused, and so is a row without grounds."""
    if "obligation_origin" not in route:
        raise GateError("route %r has not been migrated under A-1" % route["route"])
    if route["obligation_origin"] != S.UNDECIDED:
        raise GateError("%r: only an UNDECIDED row moves to NONE; it is %s" % (route["route"], route["obligation_origin"]))
    if not isinstance(grounds, str) or not grounds.strip():
        raise GateError("grounds are required to move %r to NONE (3c)" % route["route"])
    out = dict(route)
    out["obligation_origin"] = NONE_ORIGIN
    out["settles_claim"] = False
    out["removes_gate"] = False
    out["origin_basis"] = grounds
    out["reads_requirement_as_claim"] = False
    return out


_NONE_GROUNDS = {   # [CHOICE 7]; keyed as A-1 keys the routes
    ("a_household_phenology", "instrument", "eye and memory"): (
        NONE_ORIGIN, "the body's own instrument; no party holds a claim on its use and nothing is interposed"),
    ("a_household_phenology", "energy", "daylight"): (
        NONE_ORIGIN, "no party holds a claim on daylight at the site and nothing is interposed; light is not on the "
                     "list, so the row is not BIOLOGICAL either"),
    ("a_household_phenology", "transport", "on foot"): (
        NONE_ORIGIN, "walking on own land incurs no claim and nothing is interposed"),
    ("a_household_phenology", "labor", "own time, no obligation"): (
        NONE_ORIGIN, "the route's own FWO-5 name states the absence"),
    ("a_household_phenology", "data_access", "own observation"): (
        NONE_ORIGIN, "observing one's own land incurs no claim and nothing is interposed"),
    ("a_household_phenology", "publication", "notebook, unshared; whether it is ever disseminated is undeclared"): (
        S.UNDECIDED, "whether dissemination ever occurs is undeclared and an obligation may attach at that hop; "
                     "NONE requires the absence to be stated, and it is not"),
    ("b_open_access_finding", "publication", "preprint deposit; no obligation at this hop"): (
        NONE_ORIGIN, "the route's own FWO-5 name states the absence at this hop (A-1 [CHOICE 6])"),
    ("c_bitcoin_exit", "instrument", "own ledger / wallet; holding incurs no obligation at this hop"): (
        NONE_ORIGIN, "the route's own FWO-5 name states the absence at this hop"),
    ("c_bitcoin_exit", "labor", "own time"): (
        NONE_ORIGIN, "own time with no counterparty named on the route; nothing is interposed"),
    ("c_bitcoin_exit", "data_access", "public chain"): (
        S.UNDECIDED, "whether access runs through a node one operates or a third party's is undeclared in FWO-5; "
                     "the medium of access is not stated, so the absence of an obligation is not stated either"),
}


def reread_undecided(cases=None):
    """The 3c re-read over A-1's declared cases: every UNDECIDED row is either moved to
    NONE with grounds or kept UNDECIDED with the reason; a row the table does not name
    is refused, never defaulted.  Returns the counts and the re-read cases."""
    cases = S.declared_cases() if cases is None else cases
    moved, stayed, out = [], [], []
    for c in cases:
        cc = {"name": c["name"], "source": c["source"], "dependencies": {}}
        for cat, dep in c["dependencies"].items():
            routes = []
            for r in dep["routes"]:
                if r["obligation_origin"] == S.UNDECIDED:
                    key = (c["name"], cat, r["route"])
                    if key not in _NONE_GROUNDS:
                        raise GateError("no 3c grounds for %s" % (key,))
                    origin, grounds = _NONE_GROUNDS[key]
                    if origin == NONE_ORIGIN:
                        routes.append(declare_none(r, grounds))
                        moved.append(key)
                    else:
                        kept = dict(r)
                        kept["origin_basis"] = grounds
                        routes.append(kept)
                        stayed.append(key)
                else:
                    routes.append(r)
            cc["dependencies"][cat] = {"category": cat, "routes": routes, "not_needed": dep["not_needed"]}
        out.append(cc)
    return {"moved_to_none": moved, "stayed_undecided": stayed, "cases": out,
            "undecided_before": len(moved) + len(stayed)}


# --------------------------------------------------------------- fixtures ---

_RAIN = "rainwater, residential rooftop collection"
_GLEAN = "gleaning after the harvest"


def _a1_row(name, src, requirement):
    r = D.route(name, D.NONE_MEDIUM, D.NONE_MEDIUM, src)
    return S.declare(r, S.BIOLOGICAL, False, False,
                     "%s is on A-1's list; the gate, if any, is carried on the A-2 fields and not on the split" % requirement)


def fixture_f_a3_retired():
    """F-A3 RETIRED: the A-1 row kept as the record of the defect line, tagged, no gate
    fields, reads UNKNOWN [CHOICE 1], excluded from holds."""
    r = dict(S.fixture_f_a3())
    r["gate_tag"] = CONSTRUCTED_UNSOURCED
    r["hold_eligible"] = False
    r["retired"] = True
    r["gate_note"] = "A-1 F-A3, retired by A-2 section 4; the clause 'no permit regime' was constructed and is false in named jurisdictions"
    return r


def fixture_f_w1():
    src = "CARRIED: A-2 section 2, W-1 (secondary summary); statute text unread here"
    return gate(_a1_row(_RAIN, src, "water"), "rainwater_rooftop", "Colorado", None, HB_16_1005_EFFECTIVE,
                PROHIBITED, "prior-appropriation regime before HB 16-1005 (statute text unread)", "W-1",
                requirement="water", note="F-W1")


def fixture_f_w2():
    src = "CARRIED: A-2 section 2, W-1 (secondary summary); statute text unread here"
    return gate(_a1_row(_RAIN, src, "water"), "rainwater_rooftop", "Colorado", HB_16_1005_EFFECTIVE, None,
                METERED_PERMISSION, "HB 16-1005 (2016); C.R.S. 37-96.5-103", "W-1",
                requirement="water", note="F-W2")


def fixture_f_w3():
    src = "CARRIED: A-2 section 2, W-2 (secondary summary); no date carried"
    return gate(_a1_row(_RAIN + ", over 100 gal, unregistered", src, "water"), "rainwater_rooftop", "Utah", None, None,
                PROHIBITED, None, "W-2", requirement="water",
                note="F-W3; declared PROHIBITED; W-2 carries no date, so the row has no t and reads UNKNOWN [CHOICE 5]")


def fixture_f_w4(strict=False):
    src = "CARRIED: A-2 section 2, W-3 (secondary summary); the cap's absence is undated in W-3"
    if strict:
        return gate(_a1_row(_RAIN, src, "water"), "rainwater_rooftop", "Texas", None, None, OPEN, "SB 769 (2011)", "W-3",
                    requirement="water", note="F-W4 strict reading: no t, reads UNKNOWN [CHOICE 6]")
    return gate(_a1_row(_RAIN, src, "water"), "rainwater_rooftop", "Texas", "2011", None, OPEN, "SB 769 (2011)", "W-3",
                requirement="water", note="F-W4; t_from at year precision from W-3's own text [CHOICE 6]")


def fixture_f_g1():
    src = "CARRIED: A-2 section 2, G-1 (primary, Wikisource, read by the amendment's author); unread here"
    return gate(_a1_row(_GLEAN, src, "food"), "gleaning", "England", None, "1788", OPEN,
                "customary license; Hale, Norfolk Summer Assizes 1668, as quoted in the Steel v Houghton report", "G-1",
                requirement="food", note="F-G1 OPEN (customary)")


def fixture_f_g2():
    src = "CARRIED: A-2 section 2, G-2 (P/S); unread here; court conflict open [CHOICE 4]"
    return gate(_a1_row(_GLEAN, src, "food"), "gleaning", "England", "1788", None, DISCRETIONARY,
                "Steel v Houghton et Uxor (1788) 1 H Bl 51; 126 ER 32", "G-2",
                requirement="food", note="F-G2 DISCRETIONARY: relief of the poor read as a religious duty, not a legal obligation")


def fixture_rows(strict_w4=False):
    return [fixture_f_w1(), fixture_f_w2(), fixture_f_w3(), fixture_f_w4(strict_w4), fixture_f_g1(), fixture_f_g2()]


def events_declared():
    return [
        event("gleaning", "England", "1788", "Steel v Houghton et Uxor (1788) 1 H Bl 51; 126 ER 32",
              OPEN, DISCRETIONARY, "G-2", note="EV-1; court carried as Common Pleas, conflict open [CHOICE 4]"),
        event("rainwater_rooftop", "Colorado", HB_16_1005_EFFECTIVE, "HB 16-1005 (2016); C.R.S. 37-96.5-103",
              PROHIBITED, METERED_PERMISSION, "W-1", note="EV-2; effective date carried, verification NOT_RUN"),
        event("gleaning", "Israel, codified provision", None, "Leviticus 19:9-10, 23:22; Deuteronomy 24:19-21",
              UNKNOWN_STATE, OPEN, "G-3", note="EV-3; grade K, undated: stored, flagged, in no hold"),
    ]


# ------------------------------------------------------------ E-A2-1, fail ---

def unamended_pair():
    """F-W1 and F-W2 through FWO-5 + A-1 alone: the same need, the same act, the same
    jurisdiction, only t differs, and neither module has a field for t or a gate."""
    src = "CARRIED: A-2 section 2, W-1 (secondary summary); statute text unread here"
    return _a1_row(_RAIN, src, "water"), _a1_row(_RAIN, src, "water")


def fail_fixture():
    """Rule 3.  (1) The amendment's own: F-W1 vs F-W2 under the unamended code return one
    identical record.  (2) A CONSTRUCTED_UNSOURCED set on which E-A2-3's falsifier
    fires: rainwater OPEN in every jurisdiction.  Excluded from every hold."""
    a, b = unamended_pair()
    src = "CONSTRUCTED: fail fixture for E-A2-3; no jurisdiction was read; excluded from holds"
    rows = [gate(_a1_row(_RAIN, src, "water"), "rainwater_rooftop", j, "2000", None, OPEN, None, None,
                 requirement="water", tag=CONSTRUCTED_UNSOURCED) for j in ("Colorado", "Utah", "Texas")]
    return {"unamended_identical": a == b, "unamended_pair": (a, b), "all_open_rows": rows}


# ------------------------------------------------------------- E-A2-3 ---

def per_jurisdiction(rows, t, requirements=REQUIREMENTS):
    """For each requirement and each route serving it, the reading per sourced
    jurisdiction at t, and a verdict on 'OPEN in every sourced jurisdiction'.  Rows not
    hold-eligible are read but the verdict carries hold_eligible False.  A requirement
    with no row is NOT_EVALUABLE.  Never pooled."""
    out = {}
    for req in requirements:
        rs = [r for r in rows if r.get("requirement") == req]
        if not rs:
            out[req] = {"verdict": "NOT_EVALUABLE", "routes": {}, "reason": "no sourced row serves this requirement"}
            continue
        routes = {}
        for rid in sorted(set(r["route_id"] for r in rs)):
            jurs = sorted(set(r["jurisdiction"] for r in rs if r["route_id"] == rid))
            readings = dict((j, reading_at(rs, rid, j, t)[0]) for j in jurs)
            opens = [j for j in jurs if is_open(readings[j])]
            known = [j for j in jurs if readings[j] not in (UNKNOWN_STATE, "NO_ROW", "NO_ROW_AT_T", "CONFLICT")]
            if len(opens) == len(jurs):
                v = "OPEN_IN_ALL"
            elif opens:
                v = "OPEN_IN_SOME"
            else:
                v = "OPEN_IN_NONE"
            routes[rid] = {"readings": readings, "verdict": v, "open_in": opens,
                           "known_jurisdictions": known,
                           "verdict_over_known": ("OPEN_IN_ALL" if known and len(opens) == len(known)
                                                  else ("OPEN_IN_SOME" if opens else "OPEN_IN_NONE")),
                           "hold_eligible": all(r["hold_eligible"] for r in rs if r["route_id"] == rid),
                           "grade": weakest([hold_grade(r["gate_source"]) for r in rs
                                             if r["route_id"] == rid and r["hold_eligible"]])}
        out[req] = {"verdict": "EVALUATED", "routes": routes}
    return out


def open_in_every_sourced(pj, include_ineligible=False):
    """E-A2-3's falsifier: any route OPEN_IN_ALL.  Over hold-eligible rows by default;
    include_ineligible shows the falsifier firing on a constructed set without letting
    that set into a hold."""
    fired = [(req, rid) for req, d in pj.items() for rid, r in d.get("routes", {}).items()
             if r["verdict"] == "OPEN_IN_ALL" and (r["hold_eligible"] or include_ineligible)]
    return fired


# ------------------------------------------------------------- holds ---

def hold(ok, grades, eligible):
    """HELD(grade) / FAILED / NOT_EVALUABLE.  A prediction whose inputs are all excluded
    is NOT_EVALUABLE."""
    if not eligible:
        return "NOT_EVALUABLE(no hold-eligible input)"
    g = weakest(grades)
    if g is None:
        return "NOT_EVALUABLE(no graded input)"
    return "HELD(%s)" % g if ok else "FAILED"


def check_expectations(t="2026", strict_w4=False):
    """The amendment's section 5, computed.  Returns rows (label, verdict, hold, note);
    the render prints MISMATCH rows first (rule 4)."""
    rows = []
    # E-A2-1
    a, b = unamended_pair()
    w1, w2 = fixture_f_w1(), fixture_f_w2()
    sep = separating_fields(w1, w2)
    on_reading = [k for k in sep if k in READING_FIELDS]
    outside = [k for k in sep if k not in READING_FIELDS + INDEX_FIELDS + LABEL_FIELDS]
    elig = w1["hold_eligible"] and w2["hold_eligible"]
    ok1_literal = (a == b) and sep == ["gate_state"]
    rows.append(("E-A2-1 (literal) the amended records differ on gate_state ALONE",
                 ok1_literal, hold(ok1_literal, [hold_grade("W-1")], elig),
                 "they differ on %s: t_from/t_to are the index the prediction itself names ('only t differs'), and the "
                 "instrument label differs because the regime before HB 16-1005 and HB 16-1005 are two instruments" % sep))
    ok1 = (a == b) and on_reading == ["gate_state"] and not outside and gate_reading(w1) != gate_reading(w2)
    rows.append(("E-A2-1 (reading) unamended code returns one record for F-W1 and F-W2; the amended READING parts on gate_state alone",
                 ok1, hold(ok1, [hold_grade("W-1")], elig),
                 "unamended identical %s; reading fields that differ: %s; fields outside reading/index/label: %s"
                 % (a == b, on_reading, outside or "[]")))
    # E-A2-2
    ev = events_declared()
    g_ev = [e for e in ev if e["route_id"] == "gleaning" and e["jurisdiction"] == "England"]
    frow = fixture_rows(strict_w4)
    rc_before, rc_after = route_count(frow, "England", "1700"), route_count(frow, "England", t)
    tl = tally_events(ev, jurisdiction="England")
    one_event = len(g_ev) == 1
    from_open = one_event and g_ev[0]["from_state"] == OPEN
    to_discretionary = one_event and g_ev[0]["to_state"] == DISCRETIONARY
    closure = one_event and g_ev[0]["direction"] == "CLOSURE"
    # kept as separate statements: the E-A2-4 scan reads any one expression naming both states
    ok2 = one_event and from_open and to_discretionary and closure and rc_before == rc_after == 1 and tl["CLOSURE"] == 1
    rows.append(("E-A2-2 F-G1 -> F-G2 registers as one change event OPEN -> DISCRETIONARY, not as route absence",
                 ok2, hold(ok2, [hold_grade("G-1"), hold_grade("G-2")], all(e["hold_eligible"] for e in g_ev)),
                 "route count England: 1700 -> %d, %s -> %d (the count does not move); closures counted: %d"
                 % (rc_before, t, rc_after, tl["CLOSURE"])))
    # E-A2-3
    pj = per_jurisdiction(frow, t)
    fired = open_in_every_sourced(pj)
    evaluated = [r for d in pj.values() for r in d.get("routes", {}).values() if r["hold_eligible"]]
    ok3 = not fired and bool(evaluated)
    rows.append(("E-A2-3 at t=%s no subsistence route reads OPEN in every sourced jurisdiction (per jurisdiction, not pooled)" % t,
                 ok3, hold(ok3, [r["grade"] for r in evaluated if r["grade"]], bool(evaluated)),
                 "falsifier fired on %s; shelter %s" % (fired or "nothing", pj["shelter"]["verdict"])))
    # E-A2-4
    not_open = not is_open(DISCRETIONARY)
    reads_discretionary = gate_reading(fixture_f_g2()) == DISCRETIONARY
    ok4 = not_open and reads_discretionary   # membership in OPEN_STATES and the AST walk are asserted in the test
    rows.append(("E-A2-4 DISCRETIONARY is not OPEN; no expression reads a DISCRETIONARY route as independent (AST in the test)",
                 ok4, hold(ok4, [hold_grade("G-2")], True), "OPEN_STATES = %s" % (OPEN_STATES,)))
    return [(label, "MATCH" if ok else "MISMATCH", h, note) for label, ok, h, note in rows]


# ------------------------------------------------------------------- render ---

def _fmt(v):
    return "--" if v is None else str(v)


def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("gate_state -- AMENDMENT A-2 over FWO-5 / FWO-8 / A-1; gate state indexed by (jurisdiction, t); removal events\n")
    w("every source CARRIED from the amendment's section 2 at its stated grade; nothing behind it was read here; "
      "EXPECTED registered at %s\n\n" % EXPECTED_COMMIT_A2)
    w("-- section 2, carried\n")
    for sid in sorted(SOURCES):
        s = SOURCES[sid]
        w("   %-4s grade %-4s hold %-4s %s\n" % (sid, s["grade"], _fmt(hold_grade(sid)), s["text"][:100]))
        if "conflict" in s:
            c = s["conflict"]
            w("        court conflict: wikipedia %r vs King (LHR, doi 10.2307/743812) %r; carried %r; resolved %s\n"
              % (c["wikipedia"], c["king_lhr_doi_10.2307_743812"], c["carried"], c["resolved"]))
    w("   not sourced, no fixture: %s\n" % "; ".join(NOT_SOURCED))
    w("   HB 16-1005 effective date carried as %s; verification %s\n\n" % (HB_16_1005_EFFECTIVE, HB_16_1005_VERIFICATION))
    w("-- fixture rows (declared state, then what the row READS under 3a)\n")
    w("   %-6s %-17s %-10s %-10s %-10s %-19s %-19s %-5s %-4s %s\n"
      % ("id", "route_id", "juris", "t_from", "t_to", "declared", "reads", "src", "grd", "hold"))
    for r in fixture_rows():
        w("   %-6s %-17s %-10s %-10s %-10s %-19s %-19s %-5s %-4s %s\n"
          % (r["gate_note"].split(";")[0][:6], r["route_id"], r["jurisdiction"][:10], _fmt(r["t_from"]), _fmt(r["t_to"]),
             r["gate_state"], gate_reading(r), _fmt(r["gate_source"]), _fmt(r["gate_grade"]), r["hold_eligible"]))
    fa3 = fixture_f_a3_retired()
    w("   F-A3   RETIRED, tag %s, reads %s [CHOICE 1], hold %s; %s\n\n"
      % (fa3["gate_tag"], gate_reading(fa3), fa3["hold_eligible"], fa3["gate_note"][:60]))
    w("-- E-A2-1, the unamended reading of F-W1 and F-W2\n")
    a, b = unamended_pair()
    w("   FWO-5 + A-1 records identical: %s (%s)\n" % (a == b, S.unamended_reading(a)))
    w("   amended records differ on: %s\n\n" % separating_fields(fixture_f_w1(), fixture_f_w2()))
    w("-- gate_change_events, declared (3b) and derived from the rows\n")
    ev = events_declared()
    for e in ev:
        w("   %-17s %-28s %-10s %-19s -> %-19s %-4s %-4s %-17s flagged %-5s undated %-5s hold %s\n"
          % (e["route_id"], e["jurisdiction"][:28], _fmt(e["date"]), e["from_state"], e["to_state"], e["source"],
             _fmt(e["grade"]), e["direction"], e["flagged"], e["undated"], e["hold_eligible"]))
    rec = events_reconcile(ev, events_derived(fixture_rows()))
    w("   derived and declared: %d; derived with no declared row: %s; declared dated with no derivation: %s\n"
      % (len(rec["derived_declared"]), rec["derived_undeclared"] or "[]", rec["declared_underived"] or "[]"))
    for jur in ("England", "Colorado"):
        tl = tally_events(ev, jurisdiction=jur)
        w("   %-9s route count 1700 %d, 2026 %d; events: closures %d, loosenings %d, lateral %d, unknown-direction %d\n"
          % (jur, route_count(fixture_rows(), jur, "1700"), route_count(fixture_rows(), jur, "2026"),
             tl["CLOSURE"], tl["LOOSENING"], tl["LATERAL"], tl["UNKNOWN_DIRECTION"]))
    tl = tally_events(ev)
    w("   excluded from every tally: grade K %d, unsourced %d, undated %d\n\n" % (tl["excluded_k"], tl["excluded_unsourced"], tl["excluded_undated"]))
    w("-- E-A2-3, per requirement, per route, per jurisdiction at t=2026 (never pooled)\n")
    for strict in (False, True):
        pj = per_jurisdiction(fixture_rows(strict), "2026")
        w("   F-W4 %s reading [CHOICE 6]\n" % ("strict (no t)" if strict else "year-precision"))
        for req in REQUIREMENTS:
            d = pj[req]
            if d["verdict"] != "EVALUATED":
                w("      %-8s %s: %s\n" % (req, d["verdict"], d["reason"]))
                continue
            for rid, r in d["routes"].items():
                w("      %-8s %-17s %s; verdict %s (over known jurisdictions %s); hold %s grade %s\n"
                  % (req, rid, r["readings"], r["verdict"], r["verdict_over_known"], r["hold_eligible"], _fmt(r["grade"])))
        w("      falsifier (OPEN in every sourced jurisdiction) fired on: %s\n" % (open_in_every_sourced(pj) or "nothing"))
    w("\n-- section 3c, the re-read of A-1's UNDECIDED rows\n")
    rr = reread_undecided()
    w("   UNDECIDED before: %d; moved to NONE: %d; stayed UNDECIDED: %d\n"
      % (rr["undecided_before"], len(rr["moved_to_none"]), len(rr["stayed_undecided"])))
    for c in rr["cases"]:
        for cat, r in S.routes_of(c):
            if r["obligation_origin"] in (NONE_ORIGIN, S.UNDECIDED):
                w("      %-22s %-12s %-46s %-9s %s\n" % (c["name"][:22], cat, r["route"][:46], r["obligation_origin"], r["origin_basis"][:70]))
    exp = check_expectations()
    w("\n-- expected (section 5), MISMATCH rows first\n")
    for label, verdict, h, note in sorted(exp, key=lambda x: x[1] != "MISMATCH"):
        w("expected %-8s %-38s %s\n         %s\n" % (verdict, h, label, note))
    ff = fail_fixture()
    pj_ff = per_jurisdiction(ff["all_open_rows"], "2026")
    w("\nfail fixture: F-W1 vs F-W2 unamended identical %s; constructed all-OPEN set: verdict %s, hold-eligible %s, "
      "falsifier fires on it %s, and over hold-eligible rows on %s\n"
      % (ff["unamended_identical"], pj_ff["water"]["routes"]["rainwater_rooftop"]["verdict"],
         pj_ff["water"]["routes"]["rainwater_rooftop"]["hold_eligible"],
         open_in_every_sourced(pj_ff, include_ineligible=True), open_in_every_sourced(pj_ff) or "nothing"))
    w("holds read HELD(S) at most: W-1..W-3 are secondary and G-2 carries S; rules 1 and 3 met; rule 2 met at grade S by "
      "the amendment's author, CARRIED here\n")
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_gate_state.py prints the check count; samples/gate_state.sample.txt is one recorded render, "
      "compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_gate_state.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
