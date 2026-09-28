# SPDX-License-Identifier: CC0-1.0
"""AMENDMENT A-4 (2026-09-28): routes are chains -- prerequisite steps, shared gates,
required terminal state.

Landed verbatim as AMENDMENT_A4_2026-09-28_route-chains.md and committed ALONE at
EXPECTED_COMMIT_A4 before this module existed (rule 1).  Additive: A-2, A-2.1, A-3 and
A-3.1 are read by import and nothing in them is edited.

  3a  a need carries a terminal state (WATER -> POTABLE)
  3b  a chain is ordered steps; a step requires steps, resources or other chains, ALL or
      ANY [CHOICE 38]; lawful_reach and physical_reach are kept apart and never merged;
      a step whose output carries a use_restriction excluding the terminal state cannot
      feed the terminal step lawfully
  3c  shared resources: shared_by (unit: chains), closure_impact (unit: chains)
  3d  the regress walk: every leaf is BODY, TOKEN, NOT_RECORDED or CYCLE; a cycle is
      reported with its path and never broken
  3e  gates_per_chain (unit: gates), steps_per_chain (unit: steps)

Every fixture is K except C-1 (P, a FRAGMENT, not hold-eligible until section
37-96.5-103 is read in full); no hold reads above HELD(S).  Nothing here is a
statement about the law of any jurisdiction (RIN_076), and physical_reach is not a
health claim: potability needs T-10, which is not sourced.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import gate_state as G          # noqa: E402  A-2
import gate_state_a21 as A21    # noqa: E402  A-2.1
import thermal_gates as T       # noqa: E402  A-3
import repairs_a31 as R         # noqa: E402  A-3.1

EXPECTED_COMMIT_A4 = "e0083e6"
AMENDMENT_FILE = "AMENDMENT_A4_2026-09-28_route-chains.md"
T_QUERY = "2026"
TRUE, FALSE, NOT_RECORDED = "TRUE", "FALSE", "NOT_RECORDED"
NONE = "NONE"
BODY, TOKEN, CYCLE = "BODY", "TOKEN", "CYCLE"
TERMINUS_KINDS = (BODY, TOKEN, NOT_RECORDED, CYCLE)
NO_DROUGHT = "no drought declaration"

CHOICES = {
    38: "a step's requires is an expression: ALL and ANY over steps, resources, other chains and leaves; A-4's "
        "'LAND_TENURE or permit' is ANY, every other list is ALL",
    39: "lawful_reach is three-valued (A-3.1 section 4): FALSE if any required part is FALSE, else NOT_RECORDED if "
        "any is, else TRUE; ANY takes TRUE over NOT_RECORDED over FALSE",
    40: "a gate reads for lawful reach as: OPEN or METERED_PERMISSION -> TRUE; PROHIBITED -> FALSE; UNKNOWN and "
        "DISCRETIONARY -> NOT_RECORDED (no enforceable claim either way); a CONDITION_BAN is read under the chain's "
        "declared condition, 'no drought declaration' by default",
    41: "physical_reach reads the same graph with every gate open and every resource available: it asks whether the "
        "steps produce the terminal state, not whether it is safe; potability's own basis is NOT_RECORDED (T-10)",
    42: "LAND_TENURE is a held resource: held or not per chain, and not held reads FALSE for lawful reach (A-4's "
        "F-R2: 'collect is unreachable lawfully'); a resource that is obtained rather than held (PERMIT_T2) reads its "
        "own requires and gates; a sub-chain is read under the calling chain's holdings",
    43: "LAND_TENURE requires a TOKEN leaf (purchase, rent, and the property tax of RIN_063); PERMIT_T2 requires a "
        "NOT_RECORDED leaf, its terms unsourced; a TOKEN leaf reads TRUE for lawful reach (a purchase is lawful)",
    44: "resource gates and the federal T-2 permit carry jurisdiction ANY; other gates carry the chain's jurisdiction",
    45: "steps_per_chain is read two ways: own steps, and own steps plus every step of every chain it requires "
        "(transitive, each step once); gates_per_chain is transitive as section 3e states",
    46: "shared_by counts chains whose OWN steps name the resource (direct); the transitive count is printed beside",
    47: "closure_impact closes a resource (not held, its gates PROHIBITED) or a gate (PROHIBITED under every "
        "condition) and counts chains whose lawful_reach moves from TRUE: to FALSE (strict) and to anything but TRUE "
        "(loose), both printed",
    48: "a statutory gate is one of PERMIT, PROHIBITION, CONDITION_BAN, CODE_STANDARD; TOKEN_PURCHASE, METERED_TOKEN "
        "and PRIVATE_RULE are not statutory",
    49: "C-1's cap is kind CODE_STANDARD, state METERED_PERMISSION; its use restriction sits on the collect step",
    50: "CS-G chains beyond A-4's four: CH-FUEL, CH-CHARCOAL and CH-SAND are the resource chains F-R1 names; CH-T4 "
        "lifts A-3 F-T4, CH-T3 lifts A-3 F-T3, CH-SHELTER lifts A-3 F-T1, CH-GLEAN lifts A-2 F-G2 (its gate kind "
        "PRIVATE_RULE: access at the landowner's leave); each is marked with what it is lifted from",
    51: "A-3.1's unit lint is run two ways: the A-3.1 list only, and the list plus any unit the sentence names in a "
        "'(unit: X)' annotation",
}


class ChainError(ValueError):
    """A record the A-4 schema refuses; the message names the field."""


# ----------------------------------------------------------------- sources ---

SOURCES_A4 = dict((k, dict(v)) for k, v in T.SOURCES_A3.items())
SOURCES_A4.update({
    "C-1": {"grade": "P", "status": "FRAGMENT", "input": True,
            "text": "CO HB 16-1005 enrolled text: collected precipitation may not be used 'for drinking water or indoor "
                    "household purposes'; outdoor use on the collecting property only (fragment read by the "
                    "amendment's author; read C.R.S. 37-96.5-103 in full before any hold)"},
    "C-2": {"grade": "S", "status": "READ_BY_AUTHOR", "input": False,
            "text": "rooftop runoff carries bacteria including from animal feces (worldwaterreserve.com, 2026); to be "
                    "replaced by T-10"},
    "T-10": {"grade": "K", "status": "NOT_SOURCED", "input": True, "text": "a potability standard for harvested "
                                                                          "rainwater"},
    "T-11": {"grade": "K", "status": "NOT_SOURCED", "input": True, "text": "a prohibition on collecting water or "
                                                                          "natural materials in one named park"},
    "T-12": {"grade": "K", "status": "NOT_SOURCED", "input": True, "text": "a restriction on sand or soil "
                                                                          "extraction from public land"},
    "T-13": {"grade": "K", "status": "NOT_SOURCED", "input": True, "text": "a burn or open-fire rule covering "
                                                                          "charcoal production (may reuse T-4)"},
    "A4-1": {"grade": "K", "status": "STATED_BY_AMENDMENT", "input": True,
             "text": "A-4 section 1, OBSERVED (Kavik): collection needs land; filtration media are themselves gated"},
    "RIN_063": {"grade": "K", "status": "CONSTRUCTED", "input": True,
                "text": "A-1: the property tax on the land one lives on (a BOTH row)"},
    "G-2": {"grade": "S", "status": "CARRIED", "input": True, "text": G.SOURCES["G-2"]["text"]},
})


def hold_eligible(source_id):
    s = SOURCES_A4.get(source_id)
    return bool(s) and s["grade"] in ("P", "S") and s["status"] not in ("FRAGMENT", "NOT_SOURCED", "NOT_LANDED")


# ------------------------------------------------------------------- gates ---

STATUTORY = (T.PERMIT, T.PROHIBITION, T.CONDITION_BAN, T.CODE_STANDARD)   # [CHOICE 48]
LAYERS = ("FEDERAL", "STATE", "COUNTY", "MUNICIPAL", "TRIBAL", "COMMUNITY_RULE", "PRIVATE_RULE", NOT_RECORDED)


def gate(gate_id, gate_kind, jurisdiction, states, source, instrument, layer=NOT_RECORDED, note=""):
    """One gate row.  `states` maps a condition (None = unconditional) to an A-2 state."""
    if gate_kind not in T.GATE_KINDS:
        raise ChainError("gate_kind on %r is one of %s" % (gate_id, T.GATE_KINDS))
    if source not in SOURCES_A4:
        raise ChainError("source on %r is a registered id; got %r" % (gate_id, source))
    if layer not in LAYERS:
        raise ChainError("layer on %r is one of %s" % (gate_id, LAYERS))
    for s in states.values():
        if s not in G.STATES:
            raise ChainError("state on %r is one of %s" % (gate_id, G.STATES))
    return {"gate_id": gate_id, "gate_kind": gate_kind, "jurisdiction": jurisdiction, "states": dict(states),
            "source": source, "grade": SOURCES_A4[source]["grade"], "instrument": instrument, "layer": layer,
            "statutory": gate_kind in STATUTORY, "hold_eligible": hold_eligible(source), "note": note}


def seed_gates():
    ban = {"drought declaration in force": G.PROHIBITED, NO_DROUGHT: G.OPEN}
    gs = [
        gate("G-C1", T.CODE_STANDARD, "Colorado", {None: G.METERED_PERMISSION}, "C-1",
             "HB 16-1005; C.R.S. 37-96.5-103 (fragment)", note="110 gal cap; use restriction on the step [CHOICE 49]"),
        gate("G-LAND", T.TOKEN_PURCHASE, "ANY", {None: G.METERED_PERMISSION}, "A4-1", "purchase, rent, property tax",
             note="[CHOICE 43] [CHOICE 44]"),
        gate("G-T2", T.PERMIT, "ANY", {None: G.METERED_PERMISSION}, "T-2", "USFS firewood permit (not landed)"),
        gate("G-T4", T.CONDITION_BAN, "Colorado", ban, "T-4", "county burn ban (not landed; T-13 may reuse it)"),
        gate("G-T12", T.PROHIBITION, "Colorado", {None: G.PROHIBITED}, "T-12", "public-land extraction rule (not sourced)"),
        gate("G-T11", T.PROHIBITION, "municipality X", {None: G.PROHIBITED}, "T-11", "park ordinance (not sourced)"),
        gate("G-T5", T.CODE_STANDARD, "county X", {None: G.METERED_PERMISSION}, "T-5", "wood heater standard (A-3)"),
        gate("G-T4X", T.CONDITION_BAN, "county X", ban, "T-4", "county burn ban (A-3 F-T4)"),
        gate("G-T3", T.METERED_TOKEN, "state A", {None: G.METERED_PERMISSION}, "T-3", "utility account (A-3 F-T3)"),
        gate("G-T1", T.PROHIBITION, "US city X (public land)", {None: G.PROHIBITED}, "T-1",
             "public-camping ordinance (A-3 F-T1)"),
        gate("G-G2", T.PRIVATE_RULE, "England", {None: G.DISCRETIONARY}, "G-2",
             "Steel v Houghton (1788): gleaning at the landowner's leave (A-2 F-G2) [CHOICE 50]"),
    ]
    return dict((g["gate_id"], g) for g in gs)


# -------------------------------------------------------- requirements ---

def ALL(*xs):
    """[CHOICE 38]"""
    return ("ALL", tuple(xs))


def ANY(*xs):
    return ("ANY", tuple(xs))


def step_ref(sid):
    return ("step", sid)


def res(rid):
    return ("res", rid)


def chain_ref(cid):
    return ("chain", cid)


def leaf_body():
    return ("leaf", BODY, None)


def leaf_token(node):
    return ("leaf", TOKEN, node)


def leaf_nr(reason):
    return ("leaf", NOT_RECORDED, reason)


NEEDS = {"WATER": ("WATER", "POTABLE"), "FUEL": ("FUEL", "FUEL"), "CHARCOAL": ("CHARCOAL", "CHARCOAL"),
         "SAND": ("SAND", "SAND"), "THERMAL": ("THERMAL", "WARM"), "SHELTER": ("SHELTER", "SHELTER"),
         "FOOD": ("FOOD", "FOOD")}
ROUTE_NEEDS = ("WATER", "FOOD", "THERMAL", "SHELTER")      # the needs A-5 runs; the rest are resource chains


def seed_resources():
    return {
        "LAND_TENURE": {"resource_id": "LAND_TENURE", "kind": "LAND", "gates": ("G-LAND",),
                        "requires": leaf_token("MON"), "basis": "RIN_063 [CHOICE 43]", "held": True},
        "PERMIT_T2": {"resource_id": "PERMIT_T2", "kind": "PERMIT", "gates": ("G-T2",),
                      "requires": leaf_nr("permit terms unsourced (T-2 not landed)"), "basis": "[CHOICE 43]",
                      "held": False},
    }


def step(step_id, action, produces, requires, gates=(), use_restriction=NONE):
    if use_restriction not in (NONE, NOT_RECORDED) and not isinstance(use_restriction, tuple):
        raise ChainError("use_restriction on %r is NONE, NOT_RECORDED or a tuple of named restrictions" % step_id)
    return {"step_id": step_id, "action": action, "produces": produces, "requires": requires, "gates": tuple(gates),
            "use_restriction": use_restriction}


def chain(chain_id, need_id, jurisdiction, steps, holdings=(), condition=NO_DROUGHT, lifted_from=None, note=""):
    if need_id not in NEEDS:
        raise ChainError("need_id on %r is one of %s" % (chain_id, sorted(NEEDS)))
    ids = [s["step_id"] for s in steps]
    if len(set(ids)) != len(ids):
        raise ChainError("step ids repeat on %r" % chain_id)
    return {"chain_id": chain_id, "need_id": need_id, "terminal_state": NEEDS[need_id][1],
            "jurisdiction": jurisdiction, "t": T_QUERY, "steps": list(steps), "holdings": frozenset(holdings),
            "condition": condition, "lifted_from": lifted_from, "note": note}


_OUT = ("OUTDOOR_ONLY", "NOT_FOR_DRINKING")
_LAND = ("LAND_TENURE",)


def _collect_co():
    return step("collect", "rooftop collection", "RAW_WATER", ALL(res("LAND_TENURE")), ("G-C1",), _OUT)


def _filter():
    return step("filter", "filter through charcoal and sand", "POTABLE",
                ALL(step_ref("collect"), chain_ref("CH-CHARCOAL"), chain_ref("CH-SAND")), (), NOT_RECORDED)


def seed_chains():
    cs = [
        chain("F-R1", "WATER", "Colorado", [_collect_co(), _filter()], _LAND, note="A-4 F-R1"),
        chain("F-R2", "WATER", "Colorado", [_collect_co(), _filter()], (), note="A-4 F-R2: no LAND_TENURE"),
        chain("F-R3", "WATER", "municipality X",
              [step("access_park", "enter the park", "ACCESS", ALL(leaf_body()), ("G-T11",)),
               step("collect", "collection in the park", "RAW_WATER", ALL(step_ref("access_park")), (), NOT_RECORDED),
               _filter()], _LAND, note="A-4 F-R3"),
        chain("F-R4", "WATER", "Colorado",
              [_collect_co(), step("boil", "boil", "POTABLE", ALL(step_ref("collect"), chain_ref("CH-FUEL")), (),
                                   NOT_RECORDED)], _LAND, note="A-4 F-R4: boil instead of filter"),
        chain("CH-FUEL", "FUEL", "Colorado",
              [step("access", "reach wood", "ACCESS", ANY(res("LAND_TENURE"), res("PERMIT_T2"))),
               step("gather", "cut and carry", "FUEL", ALL(step_ref("access")))], _LAND,
              lifted_from="A-4 F-R1 ('charcoal requires FUEL; fuel requires LAND_TENURE or permit')"),
        chain("CH-CHARCOAL", "CHARCOAL", "Colorado",
              [step("burn", "char wood", "CHARCOAL", ALL(chain_ref("CH-FUEL")), ("G-T4",))], _LAND,
              lifted_from="A-4 F-R1 ('burn (T-4 / T-13)')"),
        chain("CH-SAND", "SAND", "Colorado",
              [step("public_access", "enter public land", "ACCESS", ALL(leaf_body()), ("G-T12",)),
               step("dig", "dig sand", "SAND", ANY(res("LAND_TENURE"), step_ref("public_access")))], _LAND,
              lifted_from="A-4 section 1 ('filtration media ... are themselves gated') and T-12"),
        chain("CH-T4", "THERMAL", "county X",
              [step("acquire_stove", "buy the stove", "STOVE", ALL(leaf_token("MON")), ("G-T5",)),
               step("fuel", "fuel", "FUEL", ANY(leaf_token("MON"), res("PERMIT_T2"))),
               step("burn", "burn", "WARM", ALL(step_ref("acquire_stove"), step_ref("fuel")), ("G-T4X",))], (),
              lifted_from="A-3 F-T4 [CHOICE 50]"),
        chain("CH-T3", "THERMAL", "state A",
              [step("heat", "utility heat", "WARM", ALL(leaf_token("MON")), ("G-T3",))], (),
              condition="account paid", lifted_from="A-3 F-T3 [CHOICE 50]"),
        chain("CH-SHELTER", "SHELTER", "US city X (public land)",
              [step("public_site", "camp on public land", "SITE", ALL(leaf_body()), ("G-T1",)),
               step("site", "a site", "SITE", ANY(res("LAND_TENURE"), step_ref("public_site"))),
               step("build", "build", "SHELTER", ALL(step_ref("site")))], _LAND,
              lifted_from="A-3 F-T1 [CHOICE 50]"),
        chain("CH-GLEAN", "FOOD", "England",
              [step("enter_field", "enter the harvested field", "ACCESS",
                    ALL(leaf_nr("the landowner's leave; no record of its terms")), ("G-G2",)),
               step("glean", "glean", "FOOD", ALL(step_ref("enter_field")))], (),
              lifted_from="A-2 F-G2 [CHOICE 50]"),
    ]
    return dict((c["chain_id"], c) for c in cs)


TOKENS = {"MON": {"token_type": "MONETARY", "converts_to": None, "hops": 0}}


class World(object):
    """A fixture set: chains, resources, gates, token nodes.  A-5 and A-6 build their own."""

    def __init__(self, chains=None, resources=None, gates=None, tokens=None):
        self.chains = seed_chains() if chains is None else chains
        self.resources = seed_resources() if resources is None else resources
        self.gates = seed_gates() if gates is None else gates
        self.tokens = dict(TOKENS) if tokens is None else tokens


# ------------------------------------------------------------- three-valued ---

def v_and(vals):
    vals = list(vals)
    if FALSE in vals:
        return FALSE
    if NOT_RECORDED in vals:
        return NOT_RECORDED
    return TRUE


def v_or(vals):
    vals = list(vals)
    if TRUE in vals:
        return TRUE
    if NOT_RECORDED in vals:
        return NOT_RECORDED
    return FALSE


def gate_value(g, condition, closed=frozenset()):
    """[CHOICE 40]"""
    if g["gate_id"] in closed:
        return FALSE
    st = g["states"].get(condition, g["states"].get(None))
    if st is None:
        return NOT_RECORDED
    if st in (G.OPEN, G.METERED_PERMISSION):
        return TRUE
    if st == G.PROHIBITED:
        return FALSE
    return NOT_RECORDED


def _step_of(c, sid):
    for s in c["steps"]:
        if s["step_id"] == sid:
            return s
    raise ChainError("chain %r has no step %r" % (c["chain_id"], sid))


def lawful(world, c, holdings=None, closed=frozenset(), terminal=True, _stack=(), money=True):
    """lawful_reach of a chain's terminal step [CHOICE 39] [CHOICE 42].  money=False reads
    every TOKEN leaf FALSE and every held resource whose own terms end in a TOKEN leaf as
    not held (A-5's money-free reading); the default is A-4's."""
    holdings = c["holdings"] if holdings is None else holdings
    if not money:
        holdings = frozenset(h for h in holdings if not any(r[0] == "leaf" and r[1] == TOKEN
                                                            for r in _refs(world.resources[h]["requires"])))
    if c["chain_id"] in _stack:
        return NOT_RECORDED
    stack = _stack + (c["chain_id"],)
    memo = {}

    def expr(e):
        k = e[0]
        if k in ("ALL", "ANY"):
            vals = [expr(x) for x in e[1]]
            return v_and(vals) if k == "ALL" else v_or(vals)
        if k == "step":
            return st(e[1])
        if k == "res":
            r = world.resources[e[1]]
            if e[1] in closed:
                held = FALSE
            elif r.get("held"):
                held = TRUE if e[1] in holdings else FALSE
            else:
                held = expr(r["requires"])      # obtained, not held: its own terms decide
            return v_and([held] + [gate_value(world.gates[g], c["condition"], closed) for g in r["gates"]])
        if k == "chain":
            return lawful(world, world.chains[e[1]], holdings, closed, False, stack, money)
        if k == "leaf":
            if e[1] == TOKEN and not money:
                return FALSE
            return TRUE if e[1] in (BODY, TOKEN) else NOT_RECORDED   # [CHOICE 43]
        raise ChainError("unknown requirement %r" % (e,))

    def st(sid):
        if sid in memo:
            return memo[sid]
        s = _step_of(c, sid)
        v = v_and([expr(s["requires"])] + [gate_value(world.gates[g], c["condition"], closed) for g in s["gates"]])
        memo[sid] = v
        return v

    last = c["steps"][-1]
    v = st(last["step_id"])
    if terminal:
        blocked = [s["step_id"] for s in c["steps"] if isinstance(s["use_restriction"], tuple)
                   and _feeds(c, s["step_id"], last["step_id"]) and _excludes(s["use_restriction"],
                                                                                 c["terminal_state"])]
        if blocked:
            return FALSE
    return v


def _excludes(restriction, terminal_state):
    return terminal_state == "POTABLE" and "NOT_FOR_DRINKING" in restriction


def _refs(e):
    if e[0] in ("ALL", "ANY"):
        out = []
        for x in e[1]:
            out.extend(_refs(x))
        return out
    return [e]


def _feeds(c, sid, target):
    if sid == target:
        return True
    seen, todo = set(), [target]
    while todo:
        cur = todo.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for r in _refs(_step_of(c, cur)["requires"]):
            if r[0] == "step":
                if r[1] == sid:
                    return True
                todo.append(r[1])
    return False


def physical(world, c, _stack=()):
    """[CHOICE 41]  Does the step graph produce the terminal state with every gate open?"""
    last = c["steps"][-1]
    if last["produces"] != c["terminal_state"]:
        return FALSE
    for r in _all_refs(world, c):
        if r[0] == "chain" and physical(world, world.chains[r[1]], _stack + (c["chain_id"],)) != TRUE:
            return FALSE
    return TRUE


def _all_refs(world, c):
    out = []
    for s in c["steps"]:
        out.extend(_refs(s["requires"]))
    return out


# ------------------------------------------------------------------ counts ---

def reachable_parts(world, c, _seen=None):
    """Every (chain, step), resource and gate the chain reaches through requires."""
    seen = _seen if _seen is not None else {"steps": set(), "resources": set(), "gates": set(), "chains": set()}
    if c["chain_id"] in seen["chains"]:
        return seen
    seen["chains"].add(c["chain_id"])
    for s in c["steps"]:
        seen["steps"].add((c["chain_id"], s["step_id"]))
        seen["gates"].update(s["gates"])
        for r in _refs(s["requires"]):
            if r[0] == "res":
                seen["resources"].add(r[1])
                seen["gates"].update(world.resources[r[1]]["gates"])
            elif r[0] == "chain":
                reachable_parts(world, world.chains[r[1]], seen)
    return seen


def gates_per_chain(world, c):
    p = reachable_parts(world, c)
    return {"count": len(p["gates"]), "unit": "gates", "gates": sorted(p["gates"]),
            "sourced": len([g for g in p["gates"] if world.gates[g]["hold_eligible"]])}


def steps_per_chain(world, c):
    """[CHOICE 45]"""
    p = reachable_parts(world, c)
    return {"own": len(c["steps"]), "transitive": len(p["steps"]), "unit": "steps"}


def shared_by(world, resource_id):
    """[CHOICE 46]"""
    direct = sorted(cid for cid, c in world.chains.items()
                    if any(r == ("res", resource_id) for r in _all_refs(world, c)))
    trans = sorted(cid for cid, c in world.chains.items() if resource_id in reachable_parts(world, c)["resources"])
    return {"direct": direct, "transitive": trans, "unit": "chains"}


def closure_impact(world, resource_id=None, gate_id=None):
    """[CHOICE 47]"""
    closed = frozenset([resource_id] if resource_id else []) | frozenset([gate_id] if gate_id else [])
    if resource_id:
        closed = closed | frozenset(world.resources[resource_id]["gates"])
    strict, loose = [], []
    for cid, c in sorted(world.chains.items()):
        before = lawful(world, c)
        after = lawful(world, c, closed=closed)
        if before == TRUE and after == FALSE:
            strict.append(cid)
        if before == TRUE and after != TRUE:
            loose.append(cid)
    return {"strict": strict, "loose": loose, "unit": "chains"}


def statutory_closures(world):
    return dict((gid, closure_impact(world, gate_id=gid)) for gid, g in sorted(world.gates.items()) if g["statutory"])


# ------------------------------------------------------------- 3d regress ---

def termini(world, c):
    """The multiset of leaves (unit: leaves) and every cycle path.  ALL and ANY both expand:
    the multiset does not carry which leaves are alternatives (A-5 reads paths)."""
    leaves, cycles = [], []

    def walk_expr(e, path, chain_obj):
        k = e[0]
        if k in ("ALL", "ANY"):
            for x in e[1]:
                walk_expr(x, path, chain_obj)
        elif k == "step":
            walk_step(chain_obj, e[1], path)
        elif k == "res":
            node = "res:" + e[1]
            if node in path:
                cycles.append(path + (node,))
                leaves.append((CYCLE, node))
                return
            walk_expr(world.resources[e[1]]["requires"], path + (node,), chain_obj)
        elif k == "chain":
            node = "chain:" + e[1]
            if node in path:
                cycles.append(path + (node,))
                leaves.append((CYCLE, node))
                return
            sub = world.chains[e[1]]
            walk_step(sub, sub["steps"][-1]["step_id"], path + (node,))
        elif k == "leaf":
            leaves.append((e[1], e[2]))

    def walk_step(chain_obj, sid, path):
        node = "step:%s.%s" % (chain_obj["chain_id"], sid)
        if node in path:
            cycles.append(path + (node,))
            leaves.append((CYCLE, node))
            return
        walk_expr(_step_of(chain_obj, sid)["requires"], path + (node,), chain_obj)

    walk_step(c, c["steps"][-1]["step_id"], ("chain:" + c["chain_id"],))
    return {"leaves": leaves, "cycles": cycles, "unit": "leaves"}


def kinds_of(leaves):
    return sorted(set(k for k, _ in leaves))


# ------------------------------------------------------------ fail fixture ---

def unamended_gate_count(t=T_QUERY):
    """F-R1's water route through A-2 / A-2.1 as delivered: rows of the rainwater route in
    force in Colorado at t.  Each row is one gate."""
    rows = [r for r in A21.fixture_rows() if r["route_id"] == "rainwater_rooftop" and r["jurisdiction"] == "Colorado"
            and G.at(r, t)]
    return {"count": len(rows), "unit": "gates", "rows": [r["gate_note"].split(";")[0] for r in rows]}


# ------------------------------------------------------ section 5 registry ---

def registry():
    """E-A4-1..5 with P and F quoted from the amendment [A-3.1 section 2]."""
    import itertools
    E = []

    def e(eid, p_quote, f_quote, space, p, f, mn=1, mx=1, variant=""):
        E.append({"id": eid, "variant": variant, "amendment": "A-4", "p_quote": p_quote, "f_quote": f_quote,
                  "f_form": R.STATED, "f_requires": R.CODE_BEHAVIOUR, "requires_reason": "a count on the fixtures",
                  "space": tuple(space), "min_cells": mn, "max_cells": mx, "p": p, "f": f})

    e("E-A4-1", "Amended code returns >= 4 gates (unit: gates) over >= 4 steps (unit: steps).",
      "amended gates_per_chain(F-R1) < 4.", itertools.product((0, 1, 2), (3, 4), (3, 4)),
      lambda w: w[0][0] == 1 and w[0][1] >= 4 and w[0][2] >= 4, lambda w: w[0][1] < 4)
    e("E-A4-2", "lawful_reach(POTABLE) = FALSE: C-1 excludes drinking.", "lawful_reach(POTABLE) = TRUE.",
      (TRUE, FALSE, NOT_RECORDED), lambda w: w[0] == FALSE, lambda w: w[0] == TRUE)
    e("E-A4-3", "shared_by(LAND_TENURE) >= 3 (unit: chains)", "shared_by(LAND_TENURE) < 3.", range(6),
      lambda w: w[0] >= 3, lambda w: w[0] < 3)
    e("E-A4-4", "No chain in the fixture set terminates ONLY in BODY", ">= 1 chain whose termini are all BODY.",
      [frozenset(s) for n in range(3) for s in itertools.combinations((BODY, TOKEN), n)],
      lambda w: all(TOKEN in cell for cell in w), lambda w: any(cell <= {BODY} for cell in w), 0, 2)
    e("E-A4-5", "closure_impact(LAND_TENURE) > closure_impact(any single statutory gate) (unit: chains).",
      "some statutory gate with closure_impact >= closure_impact(LAND_TENURE).",
      itertools.product(range(3), [()] + [(a,) for a in range(3)] + [(a, b) for a in range(3) for b in range(3)]),
      lambda w: all(w[0][0] > g for g in w[0][1]), lambda w: any(g >= w[0][0] for g in w[0][1]))
    return E


def amendment_text(fname=AMENDMENT_FILE):
    return R._norm(open(os.path.join(HERE, fname)).read())


def quotes_present(entries, fname):
    text = amendment_text(fname)
    return [(x["id"], q, R._norm(q) in text) for x in entries for q in (x["p_quote"], x["f_quote"]) if q]


def expected_block(fname):
    out, on = [], False
    for line in open(os.path.join(HERE, fname)).read().splitlines():
        if line.startswith("## "):
            on = "EXPECTED" in line
            continue
        if on:
            out.append(line)
    return R._norm(" ".join(out))


def lint_two_ways(fname):
    """[CHOICE 51]"""
    import re
    text = expected_block(fname)
    toks = R.count_tokens(text)
    declared = set(u.strip().lower() for u in re.findall(r"\(unit:\s*([A-Za-z ]+?)\)", text))
    ann = []
    for tk in toks:
        after = tk["context"]
        m = re.search(r"\(unit:\s*([A-Za-z ]+?)\)", text[text.find(after):text.find(after) + 80])
        ok_ann = tk["status"] == R.OK or (m is not None and m.group(1).strip().lower() in declared)
        ann.append(dict(tk, annotated=ok_ann))
    return {"tokens": ann, "declared_units": sorted(declared),
            "fail_a31_list": len([x for x in ann if x["status"] != R.OK]),
            "fail_with_annotation": len([x for x in ann if not x["annotated"]])}


# ------------------------------------------------------------ expectations ---

def _status(ok):
    return "MATCH" if ok else "MISMATCH"


def verdict(entry_id, world_cell):
    """A row's status from the registry's own P and F (A-3.1 section 2): MATCH, MISMATCH
    (F fires), UNMET_UNFALSIFIED (neither), OVERSHOOT (both)."""
    e = [x for x in registry() if x["id"] == entry_id][0]
    p, f = e["p"]((world_cell,)), e["f"]((world_cell,))
    if p and not f:
        return "MATCH"
    if f and not p:
        return "MISMATCH"
    return R.UNMET_UNFALSIFIED if not p else R.OVERSHOOT


def check_expectations(world=None):
    w = World() if world is None else world
    rows = []
    f1 = w.chains["F-R1"]
    un = unamended_gate_count()
    gp = gates_per_chain(w, f1)
    sp = steps_per_chain(w, f1)
    cov = "coverage %d/%d gates sourced" % (gp["sourced"], gp["count"])
    rows.append({"id": "E-A4-1 (own steps)", "status": verdict("E-A4-1", (un["count"], gp["count"], sp["own"])),
                 "hold": "INSTRUMENT (rule 1 met at %s); %s" % (EXPECTED_COMMIT_A4, cov),
                 "detail": "unamended %d gate; amended %d gates over %d own steps" % (un["count"], gp["count"], sp["own"])})
    rows.append({"id": "E-A4-1 (transitive steps)",
                 "status": verdict("E-A4-1", (un["count"], gp["count"], sp["transitive"])),
                 "hold": "INSTRUMENT; %s" % cov,
                 "detail": "unamended %d gate; amended %d gates %s over %d steps counted through requires [CHOICE 45]"
                           % (un["count"], gp["count"], gp["gates"], sp["transitive"])})
    lw, ph = lawful(w, f1), physical(w, f1)
    rows.append({"id": "E-A4-2", "status": "NOT_EVALUABLE",
                 "hold": "C-1 is a FRAGMENT; read 37-96.5-103 in full before any hold; %s" % cov,
                 "detail": "fragment reading: lawful_reach %s, physical_reach %s (not a health claim; T-10 not "
                           "sourced)" % (lw, ph)})
    sb = shared_by(w, "LAND_TENURE")
    lifted = [c for c in sb["direct"] if w.chains[c]["lifted_from"] and w.chains[c]["lifted_from"].startswith("A-3")]
    rows.append({"id": "E-A4-3", "status": "NOT_EVALUABLE",
                 "hold": "every gate K; coverage 0/%d chains sourced" % len(w.chains),
                 "detail": "K reading: shared_by direct %d chains %s (%d without the A-3 lifts), transitive %d; need ids %s"
                           % (len(sb["direct"]), sb["direct"], len(sb["direct"]) - len(lifted),
                              len(sb["transitive"]), sorted(set(w.chains[c]["need_id"] for c in sb["direct"])))})
    all_body = [cid for cid, c in sorted(w.chains.items()) if set(kinds_of(termini(w, c)["leaves"])) <= {BODY}]
    rows.append({"id": "E-A4-4", "status": "NOT_EVALUABLE", "hold": "every chain K; coverage 0/%d chains sourced"
                 % len(w.chains),
                 "detail": "K reading: chains whose termini are all BODY %s (%d chains); falsifier %s"
                           % (all_body, len(all_body), "fires" if all_body else "silent")})
    land = closure_impact(w, resource_id="LAND_TENURE")
    stat = statutory_closures(w)
    mx_s = max(len(v["strict"]) for v in stat.values())
    mx_l = max(len(v["loose"]) for v in stat.values())
    top = sorted(g for g, v in stat.items() if len(v["strict"]) == mx_s)
    rows.append({"id": "E-A4-5", "status": "NOT_EVALUABLE", "hold": "every gate K; coverage 0/%d statutory gates "
                 "sourced" % len(stat),
                 "detail": "K reading: closure_impact(LAND_TENURE) strict %d %s, loose %d %s; largest statutory strict "
                           "%d (%s), loose %d; prediction %s strict, %s loose"
                           % (len(land["strict"]), land["strict"], len(land["loose"]), land["loose"], mx_s, top, mx_l,
                              "holds" if len(land["strict"]) > mx_s else "fails",
                              "holds" if len(land["loose"]) > mx_l else "fails")})
    rank = {"MISMATCH": 0, R.UNMET_UNFALSIFIED: 0, R.OVERSHOOT: 0, "NOT_EVALUABLE": 1, "MATCH": 2}
    return sorted(rows, key=lambda r: rank[r["status"]])


# ------------------------------------------------------------------ render ---

def render(out=None):
    wr = (out or sys.stdout).write
    w = World()
    wr("chains_a4 -- AMENDMENT A-4 over A-2 / A-2.1 / A-3 / A-3.1: routes as chains\n")
    wr("EXPECTED registered at %s; every gate K but C-1 (P, fragment, not hold-eligible); nothing here is a "
       "statement about the law of any jurisdiction\n\n" % EXPECTED_COMMIT_A4)
    wr("-- expected (section 5), rows that do not hold first, then NOT_EVALUABLE\n")
    for r in check_expectations(w):
        wr("expected %-17s %-26s %s\n" % (r["status"], r["id"], r["detail"]))
        wr("         hold: %s\n" % r["hold"])
    wr("\n-- chains (3b); lawful_reach and physical_reach never merged\n")
    wr("   %-12s %-9s %-24s %-13s %-9s %-6s %-11s %s\n" % ("chain", "need", "jurisdiction", "lawful", "physical",
                                                         "gates", "steps", "lifted from"))
    for cid, c in sorted(w.chains.items()):
        gp, sp = gates_per_chain(w, c), steps_per_chain(w, c)
        wr("   %-12s %-9s %-24s %-13s %-9s %-6d %d/%-9d %s\n" % (cid, c["need_id"], c["jurisdiction"][:24],
                                                               lawful(w, c), physical(w, c), gp["count"], sp["own"],
                                                               sp["transitive"], c["lifted_from"] or "A-4 section 4"))
    wr("   (steps printed own/transitive; unit: gates, steps)\n")
    wr("\n-- 3d termini per chain (unit: leaves); ALL and ANY both expand\n")
    for cid, c in sorted(w.chains.items()):
        tm = termini(w, c)
        counts = dict((k, len([1 for x in tm["leaves"] if x[0] == k])) for k in TERMINUS_KINDS)
        wr("   %-12s %s  cycles %d\n" % (cid, " ".join("%s %d" % (k, counts[k]) for k in TERMINUS_KINDS),
                                        len(tm["cycles"])))
    wr("\n-- 3c shared resources and closures [CHOICE 46] [CHOICE 47]\n")
    for rid in sorted(w.resources):
        sb = shared_by(w, rid)
        ci = closure_impact(w, resource_id=rid)
        wr("   %-12s shared_by direct %d %s; transitive %d; closure strict %d %s, loose %d %s\n"
           % (rid, len(sb["direct"]), sb["direct"], len(sb["transitive"]), len(ci["strict"]), ci["strict"],
              len(ci["loose"]), ci["loose"]))
    for gid, v in statutory_closures(w).items():
        wr("   gate %-8s closure strict %d %s, loose %d %s\n" % (gid, len(v["strict"]), v["strict"], len(v["loose"]),
                                                              v["loose"]))
    shared = sorted(set(gates_per_chain(w, w.chains["F-R4"])["gates"]) & set(gates_per_chain(w, w.chains["CH-T4"])
                                                                                ["gates"]))
    wr("   gates F-R4 shares with the lifted thermal chain CH-T4: %s\n" % shared)
    wr("\n-- A-3.1 on section 5\n")
    tab = [(x, R.complement(x)) for x in registry()]
    for x, cc in tab:
        wr("   %-8s %-12s %s\n" % (x["id"], cc["status"], ", ".join(cc["gap_cells"][:4])))
    q = quotes_present(registry(), AMENDMENT_FILE)
    wr("   quotes found in the amendment: %d/%d\n" % (len([1 for x in q if x[2]]), len(q)))
    lt = lint_two_ways(AMENDMENT_FILE)
    wr("   unit lint: %d of %d count tokens outside the A-3.1 list; %d with the '(unit: X)' annotations read; units "
       "declared %s [CHOICE 51]\n" % (lt["fail_a31_list"], len(lt["tokens"]), lt["fail_with_annotation"],
                                      lt["declared_units"]))
    un = unamended_gate_count()
    wr("\nfail fixture: F-R1's water route through A-2 / A-2.1 as delivered reads %d gate (%s); amended %d gates\n"
       % (un["count"], un["rows"], gates_per_chain(w, w.chains["F-R1"])["count"]))
    wr("holds: rule 1 met (%s); rule 3 met; rule 2 unmet (C-1 a fragment, every other gate K)\n" % EXPECTED_COMMIT_A4)
    wr("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    wr("execution note: test_chains_a456.py prints the check count; samples/chains_a4.sample.txt is one recorded "
       "render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_chains_a456.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
