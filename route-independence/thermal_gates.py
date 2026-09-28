# SPDX-License-Identifier: CC0-1.0
"""thermal_gates.py -- AMENDMENT A-3 to FWO-5 / FWO-8 / A-1 / A-2 / A-2.1: thermal
regulation as actuators, gates stacked in series, direction never pooled, a condition
index, and cross-stock couplings.

    python3 thermal_gates.py             the seed, the fixtures, the six expectations
    python3 thermal_gates.py --choices   every [CHOICE n] in force
    python3 test_thermal_gates.py        the checks; this module refuses --selftest

EXTENDS A-2 (gate_state.py) and A-2.1 (gate_state_a21.py) and rebuilds neither: the
date grammar, the in-force interval, the five gate states and the grade table's hold
rule are A-2's; access_is_right and revocable_by are A-2.1's section-3 PROPOSED fields,
built here because A-3 adopts them.  A-2's row carries one gate_state per route; A-3's
unit is the ACTUATOR and its state is the ordered SERIES of its gates, which no function
here reduces to one state.

    actuator ---- gate(order 1) -- gate(order 2) -- ... -- gate(order n)
                   same order number = alternatives; different orders = in series
    stock A ---- coupling row ----> stock B      (the only route across stocks)

TWO FAULT CLASSES, KEPT APART (section 1)
    a gate is an ACTUATOR fault; a coupling row whose sensor_effect is SENSOR_CORRUPTED
    carries a SENSOR fault.  propagate() returns effects labelled by class; nothing
    adds a propagated effect to a gate count.

DIRECTION IS NEVER POOLED (section 2e)
    refuse_pooled() raises DirectionPooled on any input whose rows carry more than one
    direction; the test scans this file's AST so that no BoolOp, Compare, BinOp or IfExp
    names a heat-in and a heat-out direction together.

EVERY ROW IS GRADE K (section 5)
    T-1..T-9 are named and not landed; no fixture is hold-eligible, so each expectation
    about the SOURCED set reads NOT_EVALUABLE on an empty set.  The same computation over
    the K rows is printed beside it and labelled hold-ineligible.

CHOICES (numbered on from A-2.1's 9..13; printed by --choices; cited where each takes effect)

Nothing here is a statement about the law of any jurisdiction (RIN_076).
Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import gate_state as G          # noqa: E402  A-2, reused
import gate_state_a21 as A21    # noqa: E402  A-2.1, whose PROPOSED fields are built here

EXPECTED_COMMIT_A3 = "87f83ce"
AMENDMENT_FILE = "AMENDMENT_A3_2026-09-28_thermal.md"

STOCKS = ("THERMAL", "WATER", "FOOD", "AIR", "SLEEP")
HEAT_DIRECTIONS = ("WARM", "COOL", "RETAIN", "SHED")
WARM, COOL, RETAIN, SHED = HEAT_DIRECTIONS
LOCI = ("BODY", "EXTERNAL_OBJECT", "EXTERNAL_ENERGY", "EXTERNAL_STRUCTURE", "LAND_ACCESS")
BODY = LOCI[0]
GATE_KINDS = ("TOKEN_PURCHASE", "METERED_TOKEN", "PERMIT", "PROHIBITION", "CONDITION_BAN", "CODE_STANDARD",
              "PRIVATE_RULE")
TOKEN_PURCHASE, METERED_TOKEN, PERMIT, PROHIBITION, CONDITION_BAN, CODE_STANDARD, PRIVATE_RULE = GATE_KINDS
MARKET_2D = (TOKEN_PURCHASE,)                                                     # section 2d
NONMARKET_E32A = (PERMIT, PROHIBITION, CONDITION_BAN, CODE_STANDARD, PRIVATE_RULE)  # E-A3-2a's own list
MARKET_E32A = tuple(k for k in GATE_KINDS if k not in NONMARKET_E32A)             # [CHOICE 22]
ACCESS = ("TRUE", "FALSE", "UNKNOWN")
SENSOR_EFFECTS = ("NONE", "SENSOR_CORRUPTED")
FAULT_ACTUATOR, FAULT_SENSOR, FAULT_COUPLED = "ACTUATOR", "SENSOR", "COUPLED"
HEAT_IN, HEAT_OUT = "HEAT_IN", "HEAT_OUT"
SIDE = {WARM: HEAT_IN, RETAIN: HEAT_IN, COOL: HEAT_OUT, SHED: HEAT_OUT}          # [CHOICE 14]
ANY_JURISDICTION = "ANY"
MARKET_INSTRUMENT = "market purchase"
NOT_EVALUABLE = "NOT_EVALUABLE"
PROVENANCE = {"K": "OBSERVED (Kavik)", "C": "PROPOSED (Claude), marked C"}
T_QUERY = "2026"
T_WINTER = "2026-01-15"      # [CHOICE 18]

# ------------------------------------------------------- section 3, named ---

SOURCES_A3 = {
    "T-1": "Grants Pass v. Johnson (US Sup. Ct. 2024): public-camping bans are enforceable; closes self-built "
           "shelter on public land",
    "T-2": "USFS firewood permits: one named national forest, with its permit rule",
    "T-3": "winter utility disconnection: one state WITH a seasonal moratorium and one WITHOUT; statute or "
           "commission rule text",
    "T-4": "burn ban: one county-level ban with its trigger condition in the text",
    "T-5": "wood heater emission standard: EPA NSPS for residential wood heaters, rule and effective year",
    "T-6": "public indecency statute, one state: gates the SHED direction",
    "T-7": "PRIVATE_RULE: one real lease or HOA clause banning window AC units or restricting window opening; "
           "an actual document",
    "T-8": "physiology citation for cold diuresis / thirst suppression (for the coupling row)",
    "T-9": "human thermoneutral range, unclothed (for the section 1 claim that the internal regulator is narrow)",
}
SOURCES_A3 = dict((k, {"grade": "K", "input": True, "status": "NOT_LANDED", "text": v}) for k, v in SOURCES_A3.items())

A21_FIELDS_BUILT = tuple(sorted(A21.PROPOSED["fields"]))

CHOICES = {
    14: "E-A3-3 read on sides: WARM and RETAIN are HEAT_IN, COOL and SHED are HEAT_OUT; pooling refused between ANY two "
        "distinct directions, which fail fixture 2 (SHED with RETAIN) requires and 2e's WARM/COOL wording does not name",
    15: "the seed's BOTH is not a member of the direction enum and would itself be a pooled value; each body-only "
        "actuator enters as two rows, .warm and .cool; no physiological claim about which a body action serves",
    16: "locus is single-valued and names what the actuator IS; the land or energy it also takes is in its note; no "
        "expectation reads more than BODY against EXTERNAL, so the choice among external loci moves no verdict",
    17: "gates sharing an order number are alternatives (any passes); different order numbers are in series; F-T4's "
        "fuel position (purchase OR permit) is the case",
    18: "every t on a K fixture is constructed at year precision 2024 (F-T1's 't >= 2024' is the only t the order "
        "names); expectations read at 2026; F-T3 compared at the constructed winter date 2026-01-15",
    19: "jurisdictions are constructed placeholders; a gate row's jurisdiction is where the actuator is used, not "
        "who issued the gate, so F-T4 carries a national standard, a forest permit and a county ban in one "
        "county X series; F-T6's zero declaration is jurisdiction ANY, constructed only",
    20: "an actuator with no gate row and no zero declaration is UNSEARCHED, never residue; a zero declaration "
        "beside an in-force gate row is CONTRADICTED",
    21: "gate_state on every K fixture is a constructed reading of an unread source; access_is_right is UNKNOWN and "
        "revocable_by None on every row, since no fixture states either",
    22: "non-market gates counted two ways and neither picked: section 2d (excludes TOKEN_PURCHASE) and E-A3-2a's "
        "own list (excludes TOKEN_PURCHASE and METERED_TOKEN)",
    23: "a TOKEN_PURCHASE gate may be unsourced when tagged CONSTRUCTED_UNSOURCED (a gate by definition, section 5); "
        "its instrument is 'market purchase'",
}


class ThermalError(G.GateError):
    """A record the A-3 schema refuses; the message names the field."""


class DirectionPooled(ThermalError):
    """Section 2e: one input carries gates of more than one direction."""


# --------------------------------------------------------------- actuators ---

def actuator(actuator_id, stock, direction, locus, provenance, note=""):
    if not isinstance(actuator_id, str) or not actuator_id.strip():
        raise ThermalError("actuator_id is a non-empty string; got %r" % (actuator_id,))
    if stock not in STOCKS:
        raise ThermalError("stock on %r is one of %s; got %r" % (actuator_id, STOCKS, stock))
    if direction not in HEAT_DIRECTIONS:
        raise ThermalError("direction on %r is one of %s; got %r (BOTH is not a member: [CHOICE 15])"
                           % (actuator_id, HEAT_DIRECTIONS, direction))
    if locus not in LOCI:
        raise ThermalError("locus on %r is one of %s; got %r" % (actuator_id, LOCI, locus))
    if provenance not in PROVENANCE:
        raise ThermalError("provenance on %r is one of %s; got %r" % (actuator_id, sorted(PROVENANCE), provenance))
    return {"actuator_id": actuator_id, "stock": stock, "direction": direction, "locus": locus,
            "provenance": PROVENANCE[provenance], "note": note}


_SEED = (   # section 2a; K = hers, C = Claude's additions
    ("clothing.retain", RETAIN, "EXTERNAL_OBJECT", "K", "the seed's clothing (RETAIN; SHED), first direction"),
    ("clothing.shed", SHED, "EXTERNAL_OBJECT", "K", "the seed's clothing (RETAIN; SHED), second direction"),
    ("fans", COOL, "EXTERNAL_OBJECT", "K", "also takes EXTERNAL_ENERGY [CHOICE 16]"),
    ("ventilation", COOL, "EXTERNAL_STRUCTURE", "K", "air circulation / ventilation"),
    ("heating.utility", WARM, "EXTERNAL_ENERGY", "K", "heating by utility"),
    ("open_fire", WARM, "EXTERNAL_ENERGY", "K", "also takes LAND_ACCESS, a place to burn [CHOICE 16]"),
    ("wood_stove", WARM, "EXTERNAL_OBJECT", "C", "also takes EXTERNAL_ENERGY, fuel"),
    ("shelter.selfbuilt", RETAIN, "EXTERNAL_STRUCTURE", "C", "also takes LAND_ACCESS, a place to stand it"),
    ("shade", COOL, "LAND_ACCESS", "C", "the seed's 'shade and water immersion', first"),
    ("water_immersion", COOL, "LAND_ACCESS", "C", "the seed's 'shade and water immersion', second"),
)
_BODY_ONLY = ("posture", "activity", "huddling", "sleep_timing")


def seed_actuators():
    rows = [actuator(aid, "THERMAL", d, locus, prov, note) for aid, d, locus, prov, note in _SEED]
    for name in _BODY_ONLY:
        for d in (WARM, COOL):
            rows.append(actuator(name + "." + d.lower(), "THERMAL", d, BODY, "C",
                                 "the seed's body-only BOTH, split by side [CHOICE 15]"))
    return rows


def _index(actuators):
    out = {}
    for a in actuators:
        if a["actuator_id"] in out:
            raise ThermalError("actuator_id %r appears twice" % a["actuator_id"])
        out[a["actuator_id"]] = a
    return out


def is_external(a):
    return a["locus"] != BODY


# ------------------------------------------------------------------- gates ---

def _name(v, field, owner):
    if v is not None and (not isinstance(v, str) or not v.strip()):
        raise ThermalError("%s on %r is a non-empty string or None" % (field, owner))


def tgate(gate_id, actuator_id, order, gate_kind, jurisdiction, t_from, t_to=None, gate_state=G.UNKNOWN_STATE,
          trigger_condition=None, condition=None, access_is_right="UNKNOWN", revocable_by=None, source=None,
          instrument=None, tag=None, note="", actuators=None, sources=None):
    """One row of section 2b.  Rows sharing a gate_id are one gate under different
    conditions; the actuator's direction, stock and locus are copied, never supplied."""
    acts = _index(seed_actuators() if actuators is None else actuators)
    table = SOURCES_A3 if sources is None else sources
    if not isinstance(gate_id, str) or not gate_id.strip():
        raise ThermalError("gate_id is a non-empty string; got %r" % (gate_id,))
    if actuator_id not in acts:
        raise ThermalError("actuator_id on %r is a declared actuator; got %r" % (gate_id, actuator_id))
    if not isinstance(order, int) or isinstance(order, bool) or order < 1:
        raise ThermalError("order on %r is an integer >= 1; got %r" % (gate_id, order))
    if gate_kind not in GATE_KINDS:
        raise ThermalError("gate_kind on %r is one of %s; got %r" % (gate_id, GATE_KINDS, gate_kind))
    if not isinstance(jurisdiction, str) or not jurisdiction.strip():
        raise ThermalError("jurisdiction is required on %r" % gate_id)
    if gate_state not in G.STATES:
        raise ThermalError("gate_state on %r is one of %s; got %r" % (gate_id, G.STATES, gate_state))
    lo, hi = G._date(t_from, "t_from", gate_id), G._date(t_to, "t_to", gate_id)
    if lo is not None and hi is not None and not lo < hi:
        raise ThermalError("t_from < t_to on %r; got %r, %r" % (gate_id, lo, hi))
    _name(trigger_condition, "trigger_condition", gate_id)
    _name(condition, "condition", gate_id)
    if condition is not None and trigger_condition is None:
        raise ThermalError("condition on %r names a state of a trigger_condition; none is named" % gate_id)
    if access_is_right not in ACCESS:
        raise ThermalError("access_is_right on %r is one of %s; got %r" % (gate_id, ACCESS, access_is_right))
    _name(revocable_by, "revocable_by", gate_id)
    if tag not in (None, G.CONSTRUCTED_UNSOURCED):
        raise ThermalError("tag on %r is None or %s" % (gate_id, G.CONSTRUCTED_UNSOURCED))
    if source is None:
        if tag != G.CONSTRUCTED_UNSOURCED:
            raise ThermalError("source is required on %r unless the row is tagged %s (R2)"
                               % (gate_id, G.CONSTRUCTED_UNSOURCED))
        if instrument is None:
            raise ThermalError("an unsourced gate %r names its instrument [CHOICE 23]" % gate_id)
    elif source not in table:
        raise ThermalError("source on %r is a section-3 id %s; got %r" % (gate_id, sorted(table), source))
    elif table[source].get("input") is False:
        raise ThermalError("source %r on %r is recorded and NOT adopted as input" % (source, gate_id))
    a = acts[actuator_id]
    return {"gate_id": gate_id, "actuator_id": actuator_id, "order": order, "gate_kind": gate_kind,
            "jurisdiction": jurisdiction, "t_from": lo, "t_to": hi, "trigger_condition": trigger_condition,
            "condition": condition, "gate_state": gate_state, "access_is_right": access_is_right,
            "revocable_by": revocable_by, "source": source,
            "grade": None if source is None else table[source]["grade"],
            "instrument": source if instrument is None else instrument, "tag": tag, "note": note,
            "direction": a["direction"], "stock": a["stock"], "locus": a["locus"], "fault_class": FAULT_ACTUATOR,
            "hold_eligible": tag is None and source is not None and G.hold_grade(source, table) is not None}


def _applies(row, jurisdiction, t, condition):
    if row["jurisdiction"] != jurisdiction:
        return False
    if not G.at(row, t):
        return False
    rc = row.get("condition")
    if condition is None or rc is None:
        return True
    return rc == condition


def refuse_pooled(rows):
    """Section 2e at run time.  One input is one actuator in one direction."""
    dirs = sorted(set(r["direction"] for r in rows))
    if len(dirs) > 1:
        raise DirectionPooled("2e: one input carries gates of directions %s; direction is never pooled [CHOICE 14]"
                              % dirs)
    ids = sorted(set(r["actuator_id"] for r in rows))
    if len(ids) > 1:
        raise ThermalError("one series is one actuator; this input carries %s" % ids)


def _gate_reading(mine):
    if len(mine) == 1:
        return mine[0]["gate_state"]
    conds = [r.get("condition") for r in mine]
    if all(c is not None for c in conds) and len(set(conds)) == len(conds):
        return ("BY_CONDITION", dict((r["condition"], r["gate_state"]) for r in mine))
    return ("CONFLICT", [r["gate_state"] for r in mine])


def series_of(rows, jurisdiction, t, condition=None):
    """The state of one actuator at (jurisdiction, t, condition): a tuple of positions in
    order, each position a tuple of alternatives [CHOICE 17].  Never one gate_state."""
    refuse_pooled(rows)
    live = [r for r in rows if _applies(r, jurisdiction, t, condition)]
    out = []
    for n in sorted(set(r["order"] for r in live)):
        alts = []
        for gid in sorted(set(r["gate_id"] for r in live if r["order"] == n)):
            mine = [r for r in live if r["gate_id"] == gid]
            alts.append({"gate_id": gid, "gate_kind": mine[0]["gate_kind"], "instrument": mine[0]["instrument"],
                         "reading": _gate_reading(mine)})
        out.append({"order": n, "alternatives": tuple(alts)})
    return tuple(out)


def series(gates, actuator_id, jurisdiction, t, condition=None):
    return series_of([g for g in gates if g["actuator_id"] == actuator_id], jurisdiction, t, condition)


def declare_zero(actuator_id, jurisdiction, t_from, t_to=None, source=None, tag=None, note="", actuators=None):
    """A declaration that an actuator carries no gate: the residue's only way in [CHOICE 20]."""
    acts = _index(seed_actuators() if actuators is None else actuators)
    if actuator_id not in acts:
        raise ThermalError("actuator_id is a declared actuator; got %r" % (actuator_id,))
    if source is None and tag != G.CONSTRUCTED_UNSOURCED:
        raise ThermalError("a zero declaration on %r names a source or is tagged %s"
                           % (actuator_id, G.CONSTRUCTED_UNSOURCED))
    if jurisdiction == ANY_JURISDICTION and tag != G.CONSTRUCTED_UNSOURCED:
        raise ThermalError("jurisdiction ANY is admitted on a constructed declaration only [CHOICE 19]")
    return {"actuator_id": actuator_id, "jurisdiction": jurisdiction, "t_from": G._date(t_from, "t_from", actuator_id),
            "t_to": G._date(t_to, "t_to", actuator_id), "source": source, "tag": tag, "note": note,
            "hold_eligible": tag is None and source is not None and G.hold_grade(source, SOURCES_A3) is not None}


# --------------------------------------------------------------- couplings ---

def coupling(coupling_id, from_stock, to_stock, mechanism, sign, sensor_effect, source=None, tag=None, sources=None):
    table = SOURCES_A3 if sources is None else sources
    if from_stock not in STOCKS or to_stock not in STOCKS or from_stock == to_stock:
        raise ThermalError("a coupling joins two distinct stocks of %s; got %r -> %r" % (STOCKS, from_stock, to_stock))
    if sensor_effect not in SENSOR_EFFECTS:
        raise ThermalError("sensor_effect on %r is one of %s; got %r" % (coupling_id, SENSOR_EFFECTS, sensor_effect))
    if source is None and tag != G.CONSTRUCTED_UNSOURCED:
        raise ThermalError("source is required on %r unless tagged (R2)" % coupling_id)
    if source is not None and source not in table:
        raise ThermalError("source on %r is a section-3 id; got %r" % (coupling_id, source))
    return {"coupling_id": coupling_id, "from_stock": from_stock, "to_stock": to_stock, "mechanism": mechanism,
            "sign": sign, "sensor_effect": sensor_effect, "source": source,
            "grade": None if source is None else table[source]["grade"],
            "hold_eligible": tag is None and source is not None and G.hold_grade(source, table) is not None}


def seed_couplings():
    return [coupling("C-1", "THERMAL", "WATER", "cold diuresis; thirst suppression", "- (sensor opposite to stock)",
                     "SENSOR_CORRUPTED", source="T-8")]


def propagate(rows, couplings):
    """Section 2c's RULE: a gate reaches another stock ONLY through a declared row."""
    out = []
    for r in rows:
        for c in couplings:
            if c["from_stock"] == r["stock"]:
                cls = FAULT_SENSOR if c["sensor_effect"] == "SENSOR_CORRUPTED" else FAULT_COUPLED
                out.append({"coupling_id": c["coupling_id"], "gate_id": r["gate_id"], "from_stock": c["from_stock"],
                            "to_stock": c["to_stock"], "fault_class": cls,
                            "hold_eligible": r["hold_eligible"] and c["hold_eligible"]})
    return out


# ---------------------------------------------------------------- fixtures ---

_FT_NOTE = "K fixture; source named in section 3 and not landed; gate_state a constructed reading [CHOICE 21]"


def fixture_f_t1():
    return [tgate("F-T1.ban", "shelter.selfbuilt", 1, PROHIBITION, "US city X (public land)", "2024",
                  gate_state=G.PROHIBITED, source="T-1", note=_FT_NOTE)]


def fixture_f_t2():
    trig = "drought declaration"
    return [tgate("F-T2.ban", "open_fire", 1, CONDITION_BAN, "county X", "2024", gate_state=G.PROHIBITED,
                  trigger_condition=trig, condition="drought declaration in force", source="T-4", note=_FT_NOTE),
            tgate("F-T2.ban", "open_fire", 1, CONDITION_BAN, "county X", "2024", gate_state=G.OPEN,
                  trigger_condition=trig, condition="no drought declaration", source="T-4", note=_FT_NOTE)]


def fixture_f_t3():
    trig = "nonpayment in the winter season"
    out = []
    for j, gid, winter_state in (("state A", "F-T3.A.meter", G.METERED_PERMISSION),
                                 ("state B", "F-T3.B.meter", G.PROHIBITED)):
        out.append(tgate(gid, "heating.utility", 1, METERED_TOKEN, j, "2024", gate_state=G.METERED_PERMISSION,
                         trigger_condition=trig, condition="account paid", source="T-3", note=_FT_NOTE))
        out.append(tgate(gid, "heating.utility", 1, METERED_TOKEN, j, "2024", gate_state=winter_state,
                         trigger_condition=trig, condition="nonpayment, winter", source="T-3",
                         note=_FT_NOTE + ("; the moratorium keeps service on" if j == "state A"
                                          else "; no moratorium, disconnected")))
    return out


def fixture_f_t4():
    trig = "drought declaration"
    return [
        tgate("F-T4.device", "wood_stove", 1, TOKEN_PURCHASE, "county X", "2024", gate_state=G.METERED_PERMISSION,
              instrument=MARKET_INSTRUMENT, tag=G.CONSTRUCTED_UNSOURCED, note="device purchase [CHOICE 23]"),
        tgate("F-T4.standard", "wood_stove", 2, CODE_STANDARD, "county X", "2024", gate_state=G.METERED_PERMISSION,
              source="T-5", note=_FT_NOTE + "; issued nationally, read where the stove is used [CHOICE 19]"),
        tgate("F-T4.fuel.purchase", "wood_stove", 3, TOKEN_PURCHASE, "county X", "2024",
              gate_state=G.METERED_PERMISSION, instrument=MARKET_INSTRUMENT, tag=G.CONSTRUCTED_UNSOURCED,
              note="fuel purchase, alternative to the permit [CHOICE 17]"),
        tgate("F-T4.fuel.permit", "wood_stove", 3, PERMIT, "county X", "2024", gate_state=G.METERED_PERMISSION,
              source="T-2", note=_FT_NOTE + "; forest permit, alternative to purchase [CHOICE 17]"),
        tgate("F-T4.ban", "wood_stove", 4, CONDITION_BAN, "county X", "2024", gate_state=G.PROHIBITED,
              trigger_condition=trig, condition="drought declaration in force", source="T-4", note=_FT_NOTE),
        tgate("F-T4.ban", "wood_stove", 4, CONDITION_BAN, "county X", "2024", gate_state=G.OPEN,
              trigger_condition=trig, condition="no drought declaration", source="T-4", note=_FT_NOTE),
    ]


def fixture_f_t5():
    return [tgate("F-T5.indecency", "clothing.shed", 1, PROHIBITION, "state X", "2024", gate_state=G.PROHIBITED,
                  source="T-6", note=_FT_NOTE + "; gates the SHED direction")]


def fixture_f_t6():
    return [declare_zero(aid, ANY_JURISDICTION, "2024", tag=G.CONSTRUCTED_UNSOURCED,
                         note="F-T6: body-only huddling, zero gates; CONSTRUCTED, flagged, not hold-eligible")
            for aid in ("huddling.warm", "huddling.cool")]


def fixture_gates():
    return fixture_f_t1() + fixture_f_t2() + fixture_f_t3() + fixture_f_t4() + fixture_f_t5()


def jurisdictions(gates):
    return sorted(set(g["jurisdiction"] for g in gates))


def sourced(rows):
    return [r for r in rows if r["hold_eligible"]]


# ----------------------------------------------- constructed, not admitted ---

def row_retain_purchase():
    """The clothing RETAIN row fail fixture 2 pools with F-T5.  Constructed; its only gate is
    TOKEN_PURCHASE, so it is also the case that reaches E-A3-2a's falsifier."""
    return tgate("X.retain.purchase", "clothing.retain", 1, TOKEN_PURCHASE, "state X", "2024",
                 gate_state=G.METERED_PERMISSION, instrument=MARKET_INSTRUMENT, tag=G.CONSTRUCTED_UNSOURCED,
                 note="constructed for fail fixture 2; not admitted to the fixture set")


def row_fan_purchase():
    """Constructed: a HEAT_OUT object carrying a purchase gate; reaches E-A3-3's falsifier."""
    return tgate("X.fans.purchase", "fans", 1, TOKEN_PURCHASE, "state X", "2024", gate_state=G.METERED_PERMISSION,
                 instrument=MARKET_INSTRUMENT, tag=G.CONSTRUCTED_UNSOURCED, note="constructed; not admitted")


def zero_fans():
    """Constructed: a zero declaration on an external actuator; reaches E-A3-4's falsifier."""
    return declare_zero("fans", ANY_JURISDICTION, "2024", tag=G.CONSTRUCTED_UNSOURCED, note="constructed; not admitted")


def pooled_input():
    return fixture_f_t5() + [row_retain_purchase()]


# --------------------------------------------------------- derived (2d) ---

def gates_per_actuator(gates, jurisdiction, t, condition=None):
    """Distinct gates in force per actuator, also split by gate_kind.  Nothing is summed
    across actuators."""
    out = {}
    for aid in sorted(set(g["actuator_id"] for g in gates)):
        live = [g for g in gates if g["actuator_id"] == aid and _applies(g, jurisdiction, t, condition)]
        if not live:
            continue
        kinds = {}
        seen = {}
        for g in live:
            seen[g["gate_id"]] = g["gate_kind"]
        for gid in sorted(seen):
            kinds[seen[gid]] = kinds.get(seen[gid], 0) + 1
        out[aid] = {"count": len(seen), "by_kind": kinds}
    return out


def nonmarket_gates(gates, jurisdiction, t, condition=None, market=MARKET_2D):
    per = gates_per_actuator(gates, jurisdiction, t, condition)
    return dict((aid, sum(n for k, n in v["by_kind"].items() if k not in market)) for aid, v in per.items())


def ungated_residue(gates, zeros, actuators, jurisdiction, t, condition=None):
    per = gates_per_actuator(gates, jurisdiction, t, condition)
    zero_ids = set(z["actuator_id"] for z in zeros
                   if z["jurisdiction"] in (jurisdiction, ANY_JURISDICTION) and G.at(z, t))
    residue, unsearched, contradicted = [], [], []
    for a in actuators:
        aid = a["actuator_id"]
        if aid in per and aid in zero_ids:
            contradicted.append(aid)
        elif aid in per:
            continue
        elif aid in zero_ids:
            residue.append(aid)
        else:
            unsearched.append(aid)
    return {"residue": residue, "unsearched": unsearched, "contradicted": contradicted}


def residue_capacity(*args, **kwargs):
    return {"value": None, "status": NOT_EVALUABLE,
            "reason": "whether the ungated residue holds core temperature under a condition takes physiological data "
                      "not supplied (T-9 is named and not landed); section 2d leaves it uncomputed"}


def coincidence(gates, weather=None):
    """E-A3-6: a burn ban in force during a cold event.  Registered open, not predicted."""
    return {"status": NOT_EVALUABLE, "wants": "a dated weather series per jurisdiction beside the CONDITION_BAN rows",
            "weather_supplied": weather is not None}


def side_instruments(gates, side, exclude_kinds=()):
    return set(g["instrument"] for g in gates if SIDE[g["direction"]] == side and g["gate_kind"] not in exclude_kinds)


# ------------------------------------------------------------ fail fixtures ---

def unamended_f_t4(t=T_QUERY):
    """F-T4 run through A-2's row, unamended: one reading back, whatever the encoding."""
    route = G._a1_row("wood stove (A-3 F-T4 carried onto A-2 rows)",
                      "CONSTRUCTED: A-3 F-T4, one A-2 row per A-3 gate row", "warmth")
    rows = [G.gate(route, "wood_stove", r["jurisdiction"], r["t_from"], r["t_to"], r["gate_state"], r["instrument"],
                   None, requirement="warmth", tag=G.CONSTRUCTED_UNSOURCED, condition=r["condition"])
            for r in fixture_f_t4()]
    per_row = G.reading_at(rows, "wood_stove", "county X", t)[0]
    one = G.gate(route, "wood_stove", "county X", "2024", None, G.UNKNOWN_STATE, None, None, requirement="warmth")
    return {"n_gates": len(set(r["gate_id"] for r in fixture_f_t4())), "one_row_per_gate": per_row,
            "one_row_per_route": G.gate_reading(one)}


def unamended_pooled(t=T_QUERY):
    """F-T5 (SHED) and a RETAIN row on one A-2 route: A-2 has no direction field and accepts it."""
    route = G._a1_row("clothing (F-T5 SHED and a RETAIN row on one A-2 route)",
                      "CONSTRUCTED: A-3 fail fixture 2", "warmth")
    rows = [G.gate(route, "clothing", r["jurisdiction"], r["t_from"], r["t_to"], r["gate_state"], r["instrument"],
                   None, requirement="warmth", tag=G.CONSTRUCTED_UNSOURCED) for r in pooled_input()]
    return G.reading_at(rows, "clothing", "state X", t)[0]


def fail_fixture(t=T_QUERY):
    before = unamended_f_t4(t)
    after = series(fixture_f_t4(), "wood_stove", "county X", t)
    pooled_before = unamended_pooled(t)
    try:
        series_of(pooled_input(), "state X", t)
        pooled_after = "ACCEPTED"
    except DirectionPooled as e:
        pooled_after = "REFUSED: %s" % e
    return {"f_t4_before": before, "f_t4_after_positions": len(after), "pooled_before": pooled_before,
            "pooled_after": pooled_after}


# ------------------------------------------------------------ expectations ---

def _cells(gates, zeros, actuators, t):
    out = []
    for j in jurisdictions(gates):
        per = gates_per_actuator(gates, j, t)
        nm2d = nonmarket_gates(gates, j, t)
        nme = nonmarket_gates(gates, j, t, market=MARKET_E32A)
        res = ungated_residue(gates, zeros, actuators, j, t)
        for a in actuators:
            if not is_external(a):
                continue
            aid = a["actuator_id"]
            if aid in per:
                kinds = sorted(per[aid]["by_kind"])
                out.append({"j": j, "aid": aid, "state": "GATED", "kinds": kinds, "nm_2d": nm2d[aid],
                            "nm_e32a": nme[aid], "only_purchase": kinds == [TOKEN_PURCHASE]})
            elif aid in res["residue"]:
                out.append({"j": j, "aid": aid, "state": "DECLARED_ZERO", "kinds": [], "nm_2d": 0, "nm_e32a": 0,
                            "only_purchase": False})
            else:
                out.append({"j": j, "aid": aid, "state": "UNSEARCHED", "kinds": None, "nm_2d": None,
                            "nm_e32a": None, "only_purchase": False})
    return out


def e32a_reading(gates, zeros, actuators, t=T_QUERY):
    cells = _cells(gates, zeros, actuators, t)
    gated = [c for c in cells if c["state"] == "GATED"]
    return {"cells": cells, "n_cells": len(cells), "n_gated": len(gated),
            "n_unsearched": len([c for c in cells if c["state"] == "UNSEARCHED"]),
            "met_2d": [c for c in gated if c["nm_2d"] >= 1], "met_e32a": [c for c in gated if c["nm_e32a"] >= 1],
            "parted": [c for c in gated if c["nm_2d"] >= 1 and c["nm_e32a"] == 0],
            "falsifier": [c for c in gated if c["only_purchase"]]}


def e33_reading(gates):
    a_in = side_instruments(gates, HEAT_IN)
    a_out = side_instruments(gates, HEAT_OUT)
    m_in = side_instruments(gates, HEAT_IN, MARKET_2D)
    m_out = side_instruments(gates, HEAT_OUT, MARKET_2D)
    return {"in": sorted(a_in), "out": sorted(a_out), "shared_all": sorted(a_in & a_out),
            "shared_nonmarket": sorted(m_in & m_out)}


def e34_reading(gates, zeros, actuators, t=T_QUERY):
    by_j = {}
    for j in jurisdictions(gates):
        res = ungated_residue(gates, zeros, actuators, j, t)
        loci = dict((a["actuator_id"], a["locus"]) for a in actuators)
        by_j[j] = {"residue": res["residue"], "non_body_residue": [a for a in res["residue"] if loci[a] != BODY],
                   "n_unsearched": len(res["unsearched"]), "contradicted": res["contradicted"]}
    return by_j


def _order(rows):
    rank = {"MISMATCH": 0, NOT_EVALUABLE: 1, "MATCH": 2}
    return sorted(rows, key=lambda r: rank[r["status"]])


def check_expectations(t=T_QUERY):
    acts = seed_actuators()
    gates = fixture_gates()
    zeros = fixture_f_t6()
    src = sourced(gates)
    rows = []

    ff = fail_fixture(t)
    n_gates = ff["f_t4_before"]["n_gates"]
    rows.append({"id": "E-A3-1 (literal)", "status": "MATCH" if n_gates == 4 else "MISMATCH",
                 "hold": "the order's count against the order's own fixture",
                 "claim": "F-T4 is a series of four gates",
                 "detail": "F-T4 as delivered carries %d gates in %d positions: its fuel position is 'purchase OR "
                           "permit', two gates at one order number [CHOICE 17]; 'four' counts positions"
                           % (n_gates, ff["f_t4_after_positions"])})
    one_before = not isinstance(ff["f_t4_before"]["one_row_per_gate"], (tuple, list, dict))
    ok1 = (one_before and ff["f_t4_after_positions"] == 4 and ff["pooled_after"].startswith("REFUSED")
           and not isinstance(ff["pooled_before"], (tuple, list, dict)))
    rows.append({"id": "E-A3-1 (reading)", "status": "MATCH" if ok1 else "MISMATCH",
                 "hold": "INSTRUMENT (rule 1 met at %s; rule 3 met; a property of the code)" % EXPECTED_COMMIT_A3,
                 "claim": "unamended code returns one reading for F-T4 and accepts pooled SHED+RETAIN; amended does "
                          "neither",
                 "detail": "before: %r per gate row, %r per route, pooled read %r; after: %d positions, pooled %s"
                           % (ff["f_t4_before"]["one_row_per_gate"], ff["f_t4_before"]["one_row_per_route"],
                              ff["pooled_before"], ff["f_t4_after_positions"], ff["pooled_after"].split(":")[0])})

    k = e32a_reading(gates, zeros, acts, t)
    reach = e32a_reading(gates + [row_retain_purchase()], zeros, acts, t)["falsifier"]
    rows.append({"id": "E-A3-2a", "status": NOT_EVALUABLE,
                 "hold": "sourced set empty (%d of %d rows hold-eligible)" % (len(src), len(gates)),
                 "claim": "WEAKNESS FIRST: counting TOKEN_PURCHASE every EXTERNAL_OBJECT is gated trivially; so: every "
                          "external actuator carries >= 1 non-market gate in each sourced jurisdiction",
                 "detail": "K rows, hold-ineligible: %d of %d (jurisdiction, external actuator) cells carry a gate row, "
                           "%d UNSEARCHED; met under 2d %d, under E-A3-2a's list %d; the two readings part on %s; "
                           "falsifier silent on the K rows, reached on the constructed RETAIN row (%s)"
                           % (k["n_gated"], k["n_cells"], k["n_unsearched"], len(k["met_2d"]), len(k["met_e32a"]),
                              sorted(set(c["aid"] for c in k["parted"])), [c["aid"] for c in reach])})

    s = e33_reading(src)
    kk = e33_reading(gates)
    reach3 = e33_reading(gates + [row_fan_purchase()])
    rows.append({"id": "E-A3-3", "status": NOT_EVALUABLE,
                 "hold": "sourced set empty; HEAT_IN %s, HEAT_OUT %s" % (s["in"], s["out"]),
                 "claim": "the HEAT_IN and HEAT_OUT gating instruments are disjoint in the sourced set",
                 "detail": "K rows, hold-ineligible: HEAT_IN %s, HEAT_OUT %s, shared %s; with one constructed "
                           "purchase gate on a HEAT_OUT object the shared set reads %s counting market purchase and "
                           "%s without it: the E-A3-2 weakness, unstated for E-A3-3 [CHOICE 14]"
                           % (kk["in"], kk["out"], kk["shared_all"], reach3["shared_all"],
                              reach3["shared_nonmarket"])})

    r4 = e34_reading(gates, zeros, acts, t)
    reach4 = e34_reading(gates, zeros + [zero_fans()], acts, t)
    nb = sorted(set(a for v in r4.values() for a in v["non_body_residue"]))
    rows.append({"id": "E-A3-4", "status": NOT_EVALUABLE,
                 "hold": "sourced set empty; no zero declaration is sourced",
                 "claim": "ungated_residue at 2026 holds BODY-locus actuators only",
                 "detail": "K rows, hold-ineligible: residue in every jurisdiction %s, non-body residue %s, "
                           "UNSEARCHED per jurisdiction %s, contradicted %s; one constructed zero on fans puts %s in "
                           "the non-body residue [CHOICE 20]"
                           % (sorted(set(a for v in r4.values() for a in v["residue"])), nb,
                              sorted(set(v["n_unsearched"] for v in r4.values())),
                              sorted(set(a for v in r4.values() for a in v["contradicted"])),
                              sorted(set(a for v in reach4.values() for a in v["non_body_residue"])))})

    live = [g for g in fixture_f_t1() if _applies(g, g["jurisdiction"], t, None)]
    with_row = propagate(live, seed_couplings())
    without = propagate(live, [])
    ok5 = (len(with_row) == 1 and with_row[0]["to_stock"] == "WATER" and with_row[0]["fault_class"] == FAULT_SENSOR
           and without == [])
    rows.append({"id": "E-A3-5", "status": "MATCH" if ok5 else "MISMATCH",
                 "hold": "INSTRUMENT (the propagated effect itself is hold-ineligible: T-1 and T-8 are K)",
                 "claim": "the F-T1 gate reaches the water loop only via the coupling row; removing the row removes it",
                 "detail": "with C-1: %s; without: %s"
                           % ([(e["gate_id"], e["to_stock"], e["fault_class"]) for e in with_row], without)})

    c6 = coincidence(gates)
    rows.append({"id": "E-A3-6", "status": NOT_EVALUABLE, "hold": "registered open, not predicted",
                 "claim": "a burn ban in force during a cold event", "detail": "wants %s" % c6["wants"]})
    return _order(rows)


def revocation_record(gates):
    return {"rows": len(gates), "revocable_by_named": len([g for g in gates if g["revocable_by"] is not None]),
            "access_known": len([g for g in gates if g["access_is_right"] != "UNKNOWN"])}


# ------------------------------------------------------------------ render ---

def _fmt(v):
    return "--" if v is None else str(v)


def render(out=None):
    w = (out or sys.stdout).write
    acts = seed_actuators()
    gates = fixture_gates()
    zeros = fixture_f_t6()
    w("thermal_gates -- AMENDMENT A-3 over A-2 / A-2.1: actuators, gates in series, direction never pooled\n")
    w("every source grade K (named, not landed); no row is hold-eligible; EXPECTED registered at %s\n\n"
      % EXPECTED_COMMIT_A3)

    w("-- section 3 sources, all K\n")
    for sid in sorted(SOURCES_A3):
        s = SOURCES_A3[sid]
        w("   %-4s %s %-10s %s\n" % (sid, s["grade"], s["status"], s["text"][:78]))

    w("\n-- actuators (section 2a); provenance per row\n")
    for a in acts:
        w("   %-18s %-8s %-6s %-18s %s\n" % (a["actuator_id"], a["stock"], a["direction"], a["locus"], a["provenance"]))

    w("\n-- gate rows (section 2b)\n")
    w("   %-18s %-17s ord %-14s %-24s %-19s %-4s %s\n" % ("gate", "actuator", "kind", "jurisdiction", "state", "src",
                                                          "condition"))
    for g in gates:
        w("   %-18s %-17s %-3d %-14s %-24s %-19s %-4s %s\n"
          % (g["gate_id"], g["actuator_id"], g["order"], g["gate_kind"], g["jurisdiction"], g["gate_state"],
             _fmt(g["source"]), _fmt(g["condition"])))
    rv = revocation_record(gates)
    w("   access_is_right / revocable_by (A-2.1's proposal, built): %d rows, access known on %d, an office named on "
      "%d; revocable_by None reads both 'no office' and 'not recorded'\n" % (rv["rows"], rv["access_known"],
                                                                           rv["revocable_by_named"]))

    w("\n-- F-T4, wood stove, county X at %s: the series, never one state [CHOICE 17]\n" % T_QUERY)
    for cond in (None, "drought declaration in force", "no drought declaration"):
        s = series(gates, "wood_stove", "county X", T_QUERY, cond)
        w("   condition %s\n" % _fmt(cond))
        for p in s:
            w("      %d  %s\n" % (p["order"], "  OR  ".join("%s %s %s" % (x["gate_id"], x["gate_kind"], x["reading"])
                                                          for x in p["alternatives"])))

    w("\n-- F-T2 and F-T3 by condition\n")
    for cond in ("drought declaration in force", "no drought declaration"):
        w("   open_fire county X, %-30s %s\n" % (cond, series(gates, "open_fire", "county X", T_QUERY,
                                                                   cond)[0]["alternatives"][0]["reading"]))
    for j in ("state A", "state B"):
        s = series(gates, "heating.utility", j, T_WINTER, "nonpayment, winter")
        w("   heating.utility %s at %s, nonpayment in winter: %s\n" % (j, T_WINTER, s[0]["alternatives"][0]["reading"]))

    w("\n-- derived at %s, per jurisdiction (section 2d); nothing summed across actuators\n" % T_QUERY)
    for j in jurisdictions(gates):
        per = gates_per_actuator(gates, j, T_QUERY)
        n2 = nonmarket_gates(gates, j, T_QUERY)
        ne = nonmarket_gates(gates, j, T_QUERY, market=MARKET_E32A)
        res = ungated_residue(gates, zeros, acts, j, T_QUERY)
        for aid in sorted(per):
            w("   %-24s %-17s gates %d %s  non-market 2d %d, E-A3-2a list %d\n"
              % (j, aid, per[aid]["count"], per[aid]["by_kind"], n2[aid], ne[aid]))
        w("   %-24s residue %s; UNSEARCHED %d of %d actuators; contradicted %s\n"
          % (j, res["residue"], len(res["unsearched"]), len(acts), res["contradicted"]))
    rc = residue_capacity()
    w("   residue_capacity: %s (%s)\n" % (rc["status"], rc["reason"]))

    w("\n-- couplings (section 2c): the only route across stocks\n")
    for c in seed_couplings():
        w("   %s %s -> %s  %s  sign %s  %s  source %s grade %s\n" % (c["coupling_id"], c["from_stock"], c["to_stock"],
                                                                    c["mechanism"], c["sign"], c["sensor_effect"],
                                                                    c["source"], c["grade"]))
    live = [g for g in fixture_f_t1() if _applies(g, g["jurisdiction"], T_QUERY, None)]
    w("   F-T1 with C-1: %s\n" % [(e["gate_id"], e["to_stock"], e["fault_class"], e["hold_eligible"])
                                 for e in propagate(live, seed_couplings())])
    w("   F-T1 without C-1: %s\n" % propagate(live, []))

    w("\n-- expected (section 6), MISMATCH rows first, then NOT_EVALUABLE\n")
    for r in check_expectations():
        w("expected %-13s %-16s %s\n" % (r["status"], r["id"], r["claim"]))
        w("         hold: %s\n" % r["hold"])
        w("         %s\n" % r["detail"])

    ff = fail_fixture()
    w("\nfail fixture 1: F-T4 through unamended A-2 reads %r (one row per gate) and %r (one row per route) for %d "
      "gates; amended reads %d positions\n" % (ff["f_t4_before"]["one_row_per_gate"],
                                               ff["f_t4_before"]["one_row_per_route"], ff["f_t4_before"]["n_gates"],
                                               ff["f_t4_after_positions"]))
    w("fail fixture 2: F-T5 SHED pooled with a RETAIN row: unamended A-2 reads %r; amended %s\n"
      % (ff["pooled_before"], ff["pooled_after"].split(";")[0]))
    w("holds: rule 1 met (%s); rule 3 met; rule 2 unmet on every row (T-1..T-9 grade K, not landed)\n"
      % EXPECTED_COMMIT_A3)
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_thermal_gates.py prints the check count; samples/thermal_gates.sample.txt is one "
      "recorded render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_thermal_gates.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
