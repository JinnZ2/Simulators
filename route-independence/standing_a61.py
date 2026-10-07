# SPDX-License-Identifier: CC0-1.0
"""AMENDMENT A-6.1 (2026-09-28): access standing, the imposed-scarcity coupling, and the
consolidation chain.

Landed verbatim as AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md and
committed ALONE at EXPECTED_COMMIT_A61 before this module existed (rule 1).  Additive:
A-6's eligibility_a6.py is read by import and not edited; its boolean eligible_sets and
its residence_presuming_criteria (unit: criteria) are kept and answer the older question.

  2a  access_standing {MEMBER, ADMITTED_NOT_MEMBER, EXCLUDED, NOT_RECORDED}; eligible
      sets become (case_set, standing) pairs
  2b  per-route min_standing and allocation_limited; standing_gap (unit: routes)
  2c  IMPOSED_SCARCITY couplings from an external gate (A-2/A-3 gate_id, A-5 layer);
      allocation_limited TRUE with no such row is SCARCITY_UNATTRIBUTED, never internal
  2d  consolidation_events; residence_presumption_chain as an ordered pair, the missing
      link named, never collapsed into one criterion read
  3   CE-1..CE-5 carried at the amendment's grades; nothing here read a source

Profiles are CONSTRUCTED.  No person, family or people is described; section 1's
statement is carried in the amendment file in general form and nowhere else.  Nothing
here is legal advice or a statement of law beyond a cited text.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import chains_a4 as C          # noqa: E402  A-4
import termini_a5 as F         # noqa: E402  A-5 (gate layers)
import eligibility_a6 as E6    # noqa: E402  A-6
import repairs_a31 as R        # noqa: E402  A-3.1

EXPECTED_COMMIT_A61 = "7729a07"
AMENDMENT_FILE = "AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md"
EXPECTED_COMMIT_ERRATUM = "a2f6ec2"
ERRATUM_FILE = "ERRATUM_A6.1_2026-09-29.md"
CONSTRUCTED_PASS = "CONSTRUCTED_PASS"
UNFALSIFIABLE_AS_RUN = "UNFALSIFIABLE_AS_RUN"
NOT_EVALUABLE = F.NOT_EVALUABLE
TRUE, FALSE, NOT_RECORDED = C.TRUE, C.FALSE, C.NOT_RECORDED
MEMBER, ADMITTED, EXCLUDED = "MEMBER", "ADMITTED_NOT_MEMBER", "EXCLUDED"
STANDING = (MEMBER, ADMITTED, EXCLUDED, NOT_RECORDED)
MIN_STANDING = (ADMITTED, MEMBER, NOT_RECORDED)
RANK = {EXCLUDED: 0, ADMITTED: 1, MEMBER: 2}                     # [CHOICE 66]
MECHANISMS = ("REMOVAL", "CONSOLIDATION", "CONVERSION_TO_CORPORATE", "TERMINATION", "RESTORATION")
PRIOR_MODES = ("TERRITORIAL", "MOBILE", "MIXED", NOT_RECORDED)
EXTERNAL_LAYERS = ("FEDERAL", "STATE", "COUNTY", "MUNICIPAL", "PRIVATE_RULE")
IMPOSED_SCARCITY = "IMPOSED_SCARCITY"
SCARCITY_UNATTRIBUTED = "SCARCITY_UNATTRIBUTED"
GRADE_RANK = {"P": 2, "S": 1, "K": 0}

CHOICES = {
    66: "standing is ordered EXCLUDED < ADMITTED_NOT_MEMBER < MEMBER; NOT_RECORDED is not on the order, and a "
        "comparison with it returns NOT_RECORDED, never TRUE and never FALSE",
    67: "a profile's standing in a set: A-6's entry value TRUE -> MEMBER; else the set's admitted attribute "
        "TRUE -> ADMITTED_NOT_MEMBER; both FALSE -> EXCLUDED; any NOT_RECORDED on the path -> NOT_RECORDED",
    68: "standing_gap counts routes whose effective min_standing is above the profile's standing; a route "
        "whose comparison is NOT_RECORDED is counted apart as undetermined, and the gap is reported as a band "
        "[gap, gap + undetermined] (unit: routes), never with the undetermined routes folded into zero",
    69: "an IMPOSED_SCARCITY row declares raises_to; effective min_standing is the highest of the route's "
        "declared value and every coupling's raises_to; a row without raises_to is refused",
    70: "a coupling source is a gate id in A-5's LAYER_OF; its layer is external if it is in EXTERNAL_LAYERS; "
        "a TRIBAL or COMMUNITY_RULE layer is refused as internal to the set; a NOT_RECORDED layer is accepted "
        "and flagged LAYER_NOT_RECORDED",
    71: "CS-R's routes are three CONSTRUCTED_UNSOURCED rows (water, fuel allotment, housing assignment); no "
        "tribal code or trust-land rule was read (A-5 R-1..R-3 unread), so every row is K",
    72: "A-6's reachable_terminus_kinds stays NOT_EVALUABLE on CS-R, which has no A-4 chains; the 2b rule is "
        "applied to the route table as reachable_routes (unit: routes)",
    73: "E-A6.1-2 counts a candidate chain whose join (same peoples, same unit) is unsourced as NOT_RECORDED, "
        "not as absent: the count is a band [0, candidates] (unit: chains) and the row is NOT_EVALUABLE",
    74: "a CE-4 evidence path presumes residence if its own text names residence; of (i)..(iv) only (i) does; "
        "the list is TRUNCATED, so the count is a lower bound that further paths can only raise; since the "
        "erratum, [CHOICE 80] prints that bound beside the status and does not score it",
    75: "CE-1's two figures are stored per scope and never summed or averaged; the NPS line carries no grade in "
        "the amendment, so its grade is recorded NOT_RECORDED rather than borrowed from the S line above it",
    76: "Metlakatla is the amendment's control: recorded with mechanism None (no ANCSA conversion event) and "
        "excluded from E-A6.1-3's count by the amendment's own clause; the rest of ANCSA is one aggregate case",
    77: "P-ADMITTED is a CONSTRUCTED profile: resident, admitted to CS-R, not enrolled; every other attribute "
        "as A-6's base; P-NR has CS-R admission NOT_RECORDED so the fourth standing is reachable",
    78: "a '(unit: X)' annotation attaches to ONE count token: the nearest one ending before it, and only if the "
        "gap between that token's end and the annotation is at most 80 characters; a token is credited only by "
        "an annotation it owns.  Token positions are recovered by searching each token's own 40-character "
        "context forward from the previous token, and a recovered position must start with the token",
    79: "the erratum's '>= 3' and '>= 11' are carried from the operator (grade NOT_RECORDED, not borrowed from "
        "CE-4's P); they are read two ways, as bounds on the source and as the threshold E-A6-3 is scored "
        "against, and both readings give NOT_EVALUABLE on the retrieved list, so neither is picked",
    80: "a list is complete only if it is declared complete by the caller; the retrieved (i)..(iv) is declared "
        "TRUNCATED, so E-A6-3 is NOT_EVALUABLE on it under either threshold; the retrieved count is printed "
        "beside the status and is not scored",
    81: "status gate over a raw MATCH: if the cases that could fire the falsifier are not enumerated in the run, "
        "UNFALSIFIABLE_AS_RUN; else if any input is below grade S (K, CONSTRUCTED_UNSOURCED, NOT_LANDED), "
        "CONSTRUCTED_PASS; carried grades count as sourced, because the amendment's own E-A6.1-2 uses '>= S'",
    82: "open sourcing targets are recorded as data: target, the row it blocks, the state now; none is sourced "
        "here and none is filled from memory",
    83: "the gate is applied READ-ONLY to every prior MATCH row (A-1..A-5): each row's input grade is a declared "
        "reading in PRIOR_INPUTS, not inferred from its hold text; an input that is this repository's own text or "
        "code, read here, is graded P; the prior modules are not edited and their own renders are unchanged",
}


class StandingError(C.ChainError):
    pass


class ScopePooled(ValueError):
    """Raised when two figures of different scope are combined (section 6)."""


# ------------------------------------------------------------------ 2a ---

ADMITTED_ATTR = {"CS-R": "admitted_CS-R", "CS-R4": "admitted_CS-R4"}


def profiles():
    """A-6's five profiles, each given CS-R/CS-R4 admission FALSE, plus P-ADMITTED and P-NR
    [CHOICE 77].  CONSTRUCTED; nothing about any real person."""
    out = []
    for p in E6.profiles():
        p = dict(p, attributes=dict(p["attributes"]))
        p["attributes"].setdefault("admitted_CS-R", FALSE)
        p["attributes"].setdefault("admitted_CS-R4", FALSE)
        out.append(p)
    base = dict(get_a6("P-0")["attributes"])
    base.update({"admitted_CS-R": FALSE, "admitted_CS-R4": FALSE})
    out.append(E6.profile("P-ADMITTED", **dict(base, **{"admitted_CS-R": TRUE})))
    out.append(E6.profile("P-NR", **dict(base, **{"admitted_CS-R": NOT_RECORDED})))
    return out


def get_a6(pid):
    return E6.get_profile(pid)


def get_profile(pid):
    return [p for p in profiles() if p["profile_id"] == pid][0]


def standing_in(p, cs, t="2026"):
    """[CHOICE 67]"""
    ev = E6.entry_value(E6.CASE_SETS[cs]["entry"], p, t)
    if ev == TRUE:
        return MEMBER
    attr = ADMITTED_ATTR.get(cs)
    adm = p["attributes"].get(attr, NOT_RECORDED) if attr else FALSE
    if adm == TRUE:
        return ADMITTED
    if ev == NOT_RECORDED or adm == NOT_RECORDED:
        return NOT_RECORDED
    return EXCLUDED


def eligible_sets(p, t="2026"):
    """2a: (case_set, standing) pairs over every case set; nothing dropped."""
    pairs = [(cs, standing_in(p, cs, t)) for cs in sorted(E6.CASE_SETS)]
    return {"pairs": pairs, "unit": "case sets"}


def at_least(standing, minimum):
    """[CHOICE 66] three-valued standing >= minimum."""
    if standing == NOT_RECORDED or minimum == NOT_RECORDED:
        return NOT_RECORDED
    if standing not in RANK or minimum not in RANK:
        raise StandingError("standing is one of %s; got %r / %r" % (STANDING, standing, minimum))
    return TRUE if RANK[standing] >= RANK[minimum] else FALSE


# ------------------------------------------------------------------ 2b/2c ---

def route(route_id, case_set, min_standing, allocation_limited, note):
    if min_standing not in MIN_STANDING:
        raise StandingError("min_standing is one of %s; got %r" % (MIN_STANDING, min_standing))
    if allocation_limited not in (TRUE, FALSE, NOT_RECORDED):
        raise StandingError("allocation_limited is TRUE / FALSE / NOT_RECORDED; got %r" % (allocation_limited,))
    return {"route_id": route_id, "case_set": case_set, "min_standing": min_standing,
            "allocation_limited": allocation_limited, "source": "CONSTRUCTED_UNSOURCED", "grade": "K", "note": note}


def seed_routes():
    """[CHOICE 71]"""
    return [
        route("CS-R:water", "CS-R", ADMITTED, FALSE, "constructed; no allocation limit declared"),
        route("CS-R:fuel_allotment", "CS-R", ADMITTED, TRUE, "constructed; the coupling row below raises it"),
        route("CS-R:housing_assignment", "CS-R", NOT_RECORDED, TRUE, "constructed; limited, no coupling row"),
    ]


def coupling(source_gate, target_route, raises_to, note="", routes=None):
    """2c: one IMPOSED_SCARCITY row.  [CHOICE 69] [CHOICE 70]"""
    if source_gate not in F.LAYER_OF:
        raise StandingError("coupling source %r is not an A-2/A-3 gate id with an A-5 layer" % source_gate)
    layer = F.LAYER_OF[source_gate][0]
    if layer in ("TRIBAL", "COMMUNITY_RULE"):
        raise StandingError("coupling source %r is layer %s: internal to the set, not imposed" % (source_gate, layer))
    if raises_to not in (ADMITTED, MEMBER):
        raise StandingError("raises_to is ADMITTED_NOT_MEMBER or MEMBER; got %r" % (raises_to,))
    rt = dict((r["route_id"], r) for r in (routes or seed_routes()))
    if target_route not in rt:
        raise StandingError("coupling target %r is not a route" % target_route)
    if rt[target_route]["allocation_limited"] == FALSE:
        raise StandingError("coupling target %r is not allocation_limited" % target_route)
    flags = []
    if layer == NOT_RECORDED:
        flags.append("LAYER_NOT_RECORDED")
    if rt[target_route]["allocation_limited"] == NOT_RECORDED:
        flags.append("TARGET_LIMIT_NOT_RECORDED")
    return {"type": IMPOSED_SCARCITY, "source": source_gate, "layer": layer, "target": target_route,
            "raises_to": raises_to, "flags": flags, "provenance": "CONSTRUCTED_UNSOURCED", "note": note}


def seed_couplings():
    """The one constructed row E-A6.1-1 names: a state-layer gate (A-3's T-3, K, not landed)
    tightening the fuel allotment."""
    return [coupling("G-T3", "CS-R:fuel_allotment", MEMBER, "constructed for E-A6.1-1")]


def effective_min(r, couplings):
    """[CHOICE 69]"""
    vals = [r["min_standing"]] + [c["raises_to"] for c in couplings if c["target"] == r["route_id"]]
    if NOT_RECORDED in vals:
        known = [v for v in vals if v != NOT_RECORDED]
        return NOT_RECORDED if not known else ("AT_LEAST:" + max(known, key=lambda v: RANK[v]))
    return max(vals, key=lambda v: RANK[v])


def _min_for_compare(m):
    return NOT_RECORDED if m.startswith("AT_LEAST:") else m


def scarcity_flags(routes=None, couplings=None):
    """RULE 2c: allocation_limited TRUE and no IMPOSED_SCARCITY row -> SCARCITY_UNATTRIBUTED."""
    routes = seed_routes() if routes is None else routes
    couplings = seed_couplings() if couplings is None else couplings
    out = []
    for r in routes:
        rows = [c for c in couplings if c["target"] == r["route_id"]]
        if r["allocation_limited"] == TRUE and not rows:
            out.append((r["route_id"], SCARCITY_UNATTRIBUTED))
        elif r["allocation_limited"] == TRUE:
            out.append((r["route_id"], IMPOSED_SCARCITY + " from " + ",".join(c["source"] for c in rows)))
        else:
            out.append((r["route_id"], "allocation_limited " + r["allocation_limited"]))
    return out


def standing_gap(p, cs, routes=None, couplings=None, t="2026"):
    """2b [CHOICE 68]: routes in cs whose effective min_standing is above p's standing.
    reachable_routes is the 2b inclusion rule applied to the route table [CHOICE 72]."""
    routes = [r for r in (seed_routes() if routes is None else routes) if r["case_set"] == cs]
    couplings = seed_couplings() if couplings is None else couplings
    st = standing_in(p, cs, t)
    gap, und, reach = [], [], []
    for r in routes:
        m = _min_for_compare(effective_min(r, couplings))
        ok = at_least(st, m)
        (reach if ok == TRUE else gap if ok == FALSE else und).append(r["route_id"])
    return {"standing": st, "gap": len(gap), "gap_routes": gap, "undetermined": und,
            "band": (len(gap), len(gap) + len(und)), "reachable_routes": reach, "unit": "routes"}


# ------------------------------------------------------------------ 3 / 2d ---

SOURCES_A61 = {
    "CE-1a": {"grade": "P", "input": True, "text": "Indian Removal Act, May 28 1830, 4 Stat. 411 (citation)"},
    "CE-1b": {"grade": "S", "input": True, "text": "history.state.gov: removal treaties approached seventy; nearly "
                                                   "50,000 moved by the end of Jackson's presidency; destination "
                                                   "intended as what became eastern Oklahoma"},
    "CE-1c": {"grade": NOT_RECORDED, "input": True, "text": "NPS: about 100,000 removed in total across five "
                                                            "nations (the amendment states no grade) [CHOICE 75]"},
    "CE-2": {"grade": "S", "input": True, "text": "Worcester v. Georgia (1832)"},
    "CE-3": {"grade": "S", "input": True, "text": "ANCSA, PL 92-203, Dec 18 1971 (several sources)"},
    "CE-3f": {"grade": "S", "input": True, "text": "Kodiak ANCSA history PDF (1971): leasing / state selection frozen "
                                                   "by unresolved Native title"},
    "CE-3k": {"grade": "K", "input": False, "text": "the Prudhoe Bay / pipeline link (Grokipedia only); pull an "
                                                    "agency or congressional source before any hold"},
    "CE-4": {"grade": "P", "input": True, "text": "25 CFR 83.11(b), current (eCFR), retrieved TRUNCATED"},
    "CE-4e": {"grade": NOT_RECORDED, "input": True, "text": "erratum 2026-09-29 (operator, carried): >= 3 residence-"
                                                             "presuming paths, >= 11 paths in total [CHOICE 79]"},
    "CE-5": {"grade": "S", "input": True, "text": "1994 rule 83.7(f) and 83.1; retention in the current rule "
                                                  "NOT_RECORDED"},
}
STILL_TO_SOURCE = ("S-1", "S-2", "S-3", "S-4", "S-5")
READ_HERE = ("nothing: every CE line is carried at the amendment author's grade; CONNECT to ecfr.gov, "
             "law.cornell.edu and leg.colorado.gov refused 2026-09-28T13:14:37Z, github.com the control")


def consolidation_event(event_id, instrument, date, grade, peoples_in, unit_out, mechanism, prior_mode, source):
    if mechanism is not None and mechanism not in MECHANISMS:
        raise StandingError("mechanism is one of %s; got %r" % (MECHANISMS, mechanism))
    if prior_mode not in PRIOR_MODES:
        raise StandingError("prior_mode_of_peoples_in is one of %s; got %r" % (PRIOR_MODES, prior_mode))
    if peoples_in != NOT_RECORDED and not isinstance(peoples_in, list):
        raise StandingError("peoples_in is a list or NOT_RECORDED")
    return {"event_id": event_id, "instrument": instrument, "date": date, "grade": grade,
            "peoples_in": peoples_in, "unit_out": unit_out, "mechanism": mechanism,
            "prior_mode_of_peoples_in": prior_mode, "source": source}


def consolidation_events():
    return [
        consolidation_event("CE-1", "Indian Removal Act, 4 Stat. 411", "1830-05-28", "P", NOT_RECORDED,
                            "destination intended: what became eastern Oklahoma (S)", "REMOVAL", NOT_RECORDED,
                            "CE-1a"),
        consolidation_event("CE-3", "ANCSA, PL 92-203", "1971-12-18", "S", NOT_RECORDED,
                            "12 regional and 200+ village corporations", "CONVERSION_TO_CORPORATE", NOT_RECORDED,
                            "CE-3"),
    ]


def ce1_figures():
    """[CHOICE 75] two scopes, two records."""
    return [{"scope": "removal treaties under the Act, to the end of Jackson's presidency", "figure": "nearly 50,000",
             "unit": "people moved", "source": "CE-1b", "grade": SOURCES_A61["CE-1b"]["grade"]},
            {"scope": "removed in total across five nations", "figure": "about 100,000", "unit": "people removed",
             "source": "CE-1c", "grade": SOURCES_A61["CE-1c"]["grade"]}]


def pool_figures(a, b):
    """Section 6: figures from different scopes are never pooled."""
    if a["scope"] != b["scope"]:
        raise ScopePooled("refused: %r and %r cover different scopes" % (a["scope"], b["scope"]))
    raise ScopePooled("refused: no pooling rule is declared even within one scope")


def worcester_split():
    """CE-2: the A-4 split with a ruling attached."""
    return {"case": "CE-2", "lawful_reach": FALSE, "lawful_basis": "Georgia could not extend its law over "
            "Cherokee land (the ruling, S)", "physical_outcome": "removal proceeded (S)", "diverge": True,
            "grade": "S"}


def alaska_cases():
    """[CHOICE 76]"""
    return [{"case": "ANCSA aggregate (all reservations revoked except Metlakatla)",
             "mechanism": "CONVERSION_TO_CORPORATE", "control": False, "grade": "S",
             "units_enumerated": 0, "units_named": "12 regional + 200+ village corporations"},
            {"case": "Metlakatla", "mechanism": None, "control": True, "grade": "S",
             "units_enumerated": 1, "units_named": "the single non-converted control"}]


def ce3_other_mechanism():
    rows = [c for c in alaska_cases() if not c["control"]]
    other = [c["case"] for c in rows if c["mechanism"] != "CONVERSION_TO_CORPORATE"]
    return {"count": len(other), "cases": other, "over": len(rows), "unit": "cases",
            "coverage": "1 aggregate case; 0 of the 200+ village corporations enumerated; S-4 unsourced",
            "forcing_link": {"S": "CE-3f", "K": "CE-3k (not an input)"}}


EVIDENCE_PATHS_83_11_B2 = [
    {"path": "(i)", "text": ">50% reside in an area almost exclusively of members", "names_residence": True},
    {"path": "(ii)", "text": ">=50% married within the entity", "names_residence": False},
    {"path": "(iii)", "text": ">=50% keep distinct cultural patterns", "names_residence": False},
    {"path": "(iv)", "text": "distinct social institutions covering >=50%", "names_residence": False},
]
FLEXIBILITY_CLAUSE = ('distinct community from 1900 to present, "understood flexibly" in context of history, '
                      'geography, culture, social organization')


ERRATUM_BOUNDS = {"residence_presuming_paths": 3, "total_paths": 11, "was": 1, "source": "CE-4e",
                  "grade": NOT_RECORDED}


DERIVED_VIA = ("CE-4e", "CE-4")


def derived_grade(parents):
    """A-6.2 item 2: a derived value inherits its weakest parent's grade; a parent off the
    grade order (NOT_RECORDED) makes the derived value NOT_RECORDED, as in [CHOICE 66]."""
    gs = [SOURCES_A61[x]["grade"] for x in parents]
    if any(g not in GRADE_RANK for g in gs):
        return NOT_RECORDED
    return min(gs, key=lambda g: GRADE_RANK[g])


def derived_tag(parents=DERIVED_VIA):
    return "[grade %s via %s]" % (derived_grade(parents), ", ".join(parents))


def residence_presuming_paths(paths=None, complete=False):
    """E-A6-3 under the erratum [CHOICE 79] [CHOICE 80]: the retrieved count over the paths
    supplied; the list is scored only if the caller declares it complete."""
    paths = EVIDENCE_PATHS_83_11_B2 if paths is None else paths
    n = len([x for x in paths if x["names_residence"]])
    return {"count": n, "unit": "evidence paths", "retrieved": len(paths),
            "list": "COMPLETE" if complete else "TRUNCATED",
            "carried_bounds": {"residence_presuming": ">= %d" % ERRATUM_BOUNDS["residence_presuming_paths"],
                               "total": ">= %d" % ERRATUM_BOUNDS["total_paths"], "source": "CE-4e",
                               "grade": ERRATUM_BOUNDS["grade"]},
            "outside_retrieved_text": {"residence_presuming": ">= %d" % max(
                0, ERRATUM_BOUNDS["residence_presuming_paths"] - n),
                "total": ">= %d" % max(0, ERRATUM_BOUNDS["total_paths"] - len(paths)),
                "grade": derived_grade(DERIVED_VIA), "via": DERIVED_VIA},
            "flexibility_clause": FLEXIBILITY_CLAUSE,
            "sufficiency": "the residence path is one route to sufficiency, not a requirement", "source": "CE-4",
            "grade": SOURCES_A61["CE-4"]["grade"]}


def score_e_a6_3(paths=None, complete=False):
    """[CHOICE 80] Both readings of the erratum; NOT_EVALUABLE on any list not declared complete."""
    rp = residence_presuming_paths(paths, complete)
    out = {}
    grades = ["K"] if paths is not None else [SOURCES_A61["CE-4"]["grade"]]    # supplied lists are constructed
    for eid in ("E-A6-3 REVISED", "E-A6-3 ERRATUM"):
        out[eid] = gate_status(_v(eid, rp["count"]), grades, True) if complete else NOT_EVALUABLE
    return {"rp": rp, "status": out}


def presumption_chains():
    """2d: ordered pairs, each link graded, the join named when missing."""
    return [{"chain_id": "RPC-1", "consolidation_link": ("CE-1", "S"), "recognition_link": ("CE-4(i)", "P"),
             "join": NOT_RECORDED, "missing": "join: same peoples, same unit (S-2 / S-3 unsourced)"}]


def chain_count(chains=None):
    """[CHOICE 73]"""
    chains = presumption_chains() if chains is None else chains
    ge_s = lambda g: GRADE_RANK.get(g, -1) >= GRADE_RANK["S"]
    both = [c for c in chains if ge_s(c["consolidation_link"][1]) and ge_s(c["recognition_link"][1])]
    admitted = [c for c in both if c["join"] == TRUE]
    pending = [c for c in both if c["join"] == NOT_RECORDED]
    return {"literal_links_only": len(both), "admitted": len(admitted), "pending_join": len(pending),
            "band": (len(admitted), len(admitted) + len(pending)), "unit": "chains"}


# ------------------------------------------------------------ registry ---

def registry():
    E = []

    def e(eid, pq, fq, space, p, f, form=R.STATED):
        E.append({"id": eid, "variant": "", "amendment": "A-6.1", "p_quote": pq, "f_quote": fq, "f_form": form,
                  "f_requires": R.CODE_BEHAVIOUR, "requires_reason": "a count over carried and constructed rows",
                  "space": tuple(space), "min_cells": 1, "max_cells": 1, "p": p, "f": f})
    e("E-A6.1-1", "standing_gap(P-ADMITTED) >= 1 (unit: routes).", "FALSIFIER: standing_gap = 0 (unit: routes).",
      range(4), lambda w: w[0] >= 1, lambda w: w[0] == 0)
    e("E-A6.1-2", "At least one residence_presumption_chain has BOTH links sourced at grade >= S (unit: chains).",
      "FALSIFIER: 0 chains with both links sourced.", (0, 1, 2, NOT_EVALUABLE),
      lambda w: w[0] != NOT_EVALUABLE and w[0] >= 1, lambda w: w[0] == 0)
    e("E-A6.1-3", "every Alaska case except Metlakatla carries mechanism CONVERSION_TO_CORPORATE",
      "FALSIFIER: >= 1 non-Metlakatla case with another mechanism.", range(3),
      lambda w: w[0] == 0, lambda w: w[0] >= 1)
    e("E-A6-3 REVISED", "residence_presuming_paths >= 1 (unit: evidence paths) HELD(P) on current text.", None,
      (0, 1, 2, NOT_EVALUABLE), lambda w: w[0] != NOT_EVALUABLE and w[0] >= 1, lambda w: w[0] == 0,
      form=R.UNDECLARED)
    e("E-A6-3 ERRATUM", "residence_presuming_paths >= 3", None, (0, 1, 2, 3, 4, NOT_EVALUABLE),
      lambda w: w[0] != NOT_EVALUABLE and w[0] >= 3, lambda w: False, form=R.UNDECLARED)
    E[-1]["source_file"] = ERRATUM_FILE
    return E


def _v(eid, cell):
    x = [r for r in registry() if r["id"] == eid][0]
    p, f = x["p"]((cell,)), x["f"]((cell,))
    return "MATCH" if p and not f else "MISMATCH" if f and not p else (R.UNMET_UNFALSIFIED if not p else R.OVERSHOOT)


def gate_status(raw, input_grades, falsifier_cases_enumerated):
    """[CHOICE 81] No prediction reads MATCH without sourced input."""
    if raw != "MATCH":
        return raw
    if not falsifier_cases_enumerated:
        return UNFALSIFIABLE_AS_RUN
    if any(GRADE_RANK.get(g, -1) < GRADE_RANK["S"] for g in input_grades):
        return CONSTRUCTED_PASS
    return raw


def check_expectations():
    rows = []
    cc = chain_count()
    rows.append({"id": "E-A6.1-2", "status": NOT_EVALUABLE, "raw": NOT_EVALUABLE,
                 "hold": "none; the join is unsourced (S-2, S-3); coverage 0/1 joins sourced",
                 "detail": "band %s (unit: chains) [CHOICE 73]; counting links only reads %d (%s); reading the "
                           "unsourced join as absent reads 0 and the falsifier fires (%s)"
                           % (list(cc["band"]), cc["literal_links_only"], _v("E-A6.1-2", cc["literal_links_only"]),
                              _v("E-A6.1-2", cc["admitted"]))})
    sc = score_e_a6_3()
    rp = sc["rp"]
    rows.append({"id": "E-A6-3", "status": NOT_EVALUABLE, "raw": NOT_EVALUABLE,
                 "hold": "none; list TRUNCATED (%d retrieved of %s total, erratum %s at %s) [CHOICE 80]"
                         % (rp["retrieved"], rp["carried_bounds"]["total"], ERRATUM_FILE, EXPECTED_COMMIT_ERRATUM),
                 "detail": "retrieved %d residence-presuming path (unit: evidence paths), not scored; carried bound "
                           "%s puts %s residence-presuming paths outside the retrieved text %s; threshold >= 1 "
                           "(as delivered) %s, threshold >= 3 (erratum) %s; supersedes RIN_131's MATCH"
                           % (rp["count"], rp["carried_bounds"]["residence_presuming"],
                              rp["outside_retrieved_text"]["residence_presuming"], derived_tag(),
                              sc["status"]["E-A6-3 REVISED"], sc["status"]["E-A6-3 ERRATUM"])})
    o = ce3_other_mechanism()
    raw3 = _v("E-A6.1-3", o["count"])
    rows.append({"id": "E-A6.1-3", "status": gate_status(raw3, ["S"], falsifier_cases_enumerated=False),
                 "raw": raw3,
                 "hold": "none until S-4 is sourced; coverage: %s" % o["coverage"],
                 "detail": "%d of %d non-control cases carry another mechanism; the one case is the aggregate, whose "
                           "mechanism is the amendment's reading of the act, so no enumerated case can fire the "
                           "falsifier [CHOICE 81]" % (o["count"], o["over"])})
    p = get_profile("P-ADMITTED")
    g = standing_gap(p, "CS-R")
    g0 = standing_gap(p, "CS-R", couplings=[])
    raw1 = _v("E-A6.1-1", g["gap"])
    grades1 = [r["grade"] for r in seed_routes()] + ["K"]            # G-T3: A-3's T-3, K, NOT_LANDED
    rows.append({"id": "E-A6.1-1", "status": gate_status(raw1, grades1, falsifier_cases_enumerated=True),
                 "raw": raw1,
                 "hold": "none on sourced input; INSTRUMENT only (rule 1 met at %s); coverage 0/%d routes sourced, "
                         "0/1 couplings sourced (G-T3 unsourced)" % (EXPECTED_COMMIT_A61, len(seed_routes())),
                 "detail": "with the constructed row: gap %d %s, band %s; without it: gap %d, band %s (the falsifier "
                           "cell is reachable) [CHOICE 81]" % (g["gap"], g["gap_routes"], list(g["band"]), g0["gap"],
                                                               list(g0["band"]))})
    return rows


def unsourced_matches(rows=None):
    """The check behind the erratum's item 3: rows reading MATCH with any input below S."""
    rows = check_expectations() if rows is None else rows
    return [r["id"] for r in rows if r["status"] == "MATCH"]


# ------------------------------------------------------ erratum item 4 ---

_ANN = __import__("re").compile(r"\(unit:\s*([A-Za-z ]+?)\)")


def _positions(text, toks):
    """[CHOICE 78]"""
    cur, out = 0, []
    for t in toks:
        pos = text.find(t["context"], cur)
        if pos < 0 or text[pos:pos + len(t["token"])] != t["token"]:
            raise StandingError("token %r not recovered at its own context" % (t["token"],))
        out.append(pos)
        cur = pos + 1
    return out


def attach_nearest(text):
    """[CHOICE 78] each annotation owned by the nearest preceding count token."""
    toks = R.count_tokens(text)
    pos = _positions(text, toks)
    owner = {}
    for m in _ANN.finditer(text):
        prev = [i for i, q in enumerate(pos) if q + len(toks[i]["token"]) <= m.start()]
        if prev and m.start() - (pos[prev[-1]] + len(toks[prev[-1]]["token"])) <= 80:
            owner[prev[-1]] = m.group(1).strip().lower()
    return [dict(t, pos=pos[i], owns=owner.get(i), annotated=(t["status"] == R.OK or i in owner))
            for i, t in enumerate(toks)]


def lint_nearest(fname):
    ann = attach_nearest(C.expected_block(fname))
    return {"tokens": ann, "fail_a31_list": len([x for x in ann if x["status"] != R.OK]),
            "fail_with_annotation": len([x for x in ann if not x["annotated"]]),
            "credited": [x["context"][:24] for x in ann if x["status"] != R.OK and x["annotated"]]}


ANNOTATION_FIXTURES = (
    ("adjacent_other_count", "Expected: one route, standing_gap(P-ADMITTED) >= 1 (unit: routes).", "1"),
    ("two_counts_one_unit", "Expected: 3 cases held and 2 (unit: routes) open.", "2"),
)


def annotation_fixture():
    """Erratum item 4: the adjacent annotation belongs to a different count.  Run through the
    A-4 window rule (chains_a4.lint_two_ways, [CHOICE 51]) and through [CHOICE 78]."""
    import tempfile
    out = []
    d = tempfile.mkdtemp()
    try:
        for name, body, owner in ANNOTATION_FIXTURES:
            path = os.path.join(d, name + ".md")
            with open(path, "w") as fh:
                fh.write("## EXPECTED\n\n%s\n" % body)
            old = C.lint_two_ways(path)
            new = attach_nearest(C.expected_block(path))
            out.append({"fixture": name, "owner": owner,
                        "window_credits": [t["token"] for t in old["tokens"] if t["annotated"]],
                        "nearest_credits": [t["token"] for t in new if t["annotated"]]})
            os.remove(path)
    finally:
        os.rmdir(d)
    return out


def lint_comparison():
    """Both attachment rules over every landed amendment carrying an annotation."""
    import glob
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "AMENDMENT_A*.md"))):
        f = os.path.basename(f)
        if "(unit:" not in C.expected_block(f):
            continue
        a, b = C.lint_two_ways(f), lint_nearest(f)
        moved = [(y["context"][:30], x["annotated"], y["annotated"]) for x, y in zip(a["tokens"], b["tokens"])
                 if x["annotated"] != y["annotated"]]
        rows.append({"file": f, "window": a["fail_with_annotation"], "nearest": b["fail_with_annotation"],
                     "of": len(b["tokens"]), "moved": moved})
    return rows


PRIOR_INPUTS = (   # [CHOICE 83] module, row id prefix, input grades, basis
    ("settlement_split", "E-A1 majority CONSTRUCTED", ["K"], "the coded route rows are CONSTRUCTED"),
    ("settlement_split", "E-A1 at least 2 of 3", ["K"], "the three cases' edges are CONSTRUCTED"),
    ("gate_state", "E-A2-1 (reading)", ["S"], "F-W1/F-W2 carried at S (W-1)"),
    ("gate_state", "E-A2-2", ["S"], "F-G1/F-G2 carried at S"),
    ("gate_state", "E-A2-3", ["S", "P"], "sourced jurisdictions only"),
    ("gate_state", "E-A2-4", ["P"], "this repository's code, read here (AST)"),
    ("gate_state_a21", "E-A2.1-1", ["P"], "W-1, W-2 at P by the author's read"),
    ("gate_state_a21", "E-A2.1-2", ["S", "P"], "the E-A2-3 rows, S and P"),
    ("thermal_gates", "E-A3-1 (reading)", ["K"], "F-T4 fixture K"),
    ("thermal_gates", "E-A3-5", ["K"], "T-1 and T-8 K"),
    ("repairs_a31", "E-A3.1-1 (LITERAL_ALL)", ["P"], "the landed EXPECTED blocks, read here"),
    ("repairs_a31", "E-A3.1-1 (DECLARED_LITERAL)", ["P"], "the landed EXPECTED blocks, read here"),
    ("repairs_a31", "E-A3.1-2 (EVIDENCE)", ["K"], "63 prior rows, CONSTRUCTED"),
    ("repairs_a31", "E-A3.1-2 (SCHEMA_DEFAULT)", ["K"], "63 prior rows, CONSTRUCTED"),
    ("chains_a4", "E-A4-1 (transitive steps)", ["K"], "0/5 gates sourced"),
    ("termini_a5", "E-A5-1 (LAWFUL_STRICT)", ["K"], "K rows"),
    ("termini_a5", "E-A5-4 (without hops)", ["K"], "FWO-5 routes CONSTRUCTED"),
)


def _prior_rows(modname):
    import importlib
    mod = importlib.import_module(modname)
    rows = mod.check_expectations(mod.declared_cases()) if modname == "settlement_split" else mod.check_expectations()
    out = []
    for r in rows:
        if isinstance(r, dict):
            out.append((r["id"], r["status"]))
        else:
            out.append((r[0], r[1]))
    return out


def prior_sweep():
    """[CHOICE 83] every prior MATCH row, gated; DRIFT if a declared row no longer reads as declared."""
    live = {}
    for mod in sorted(set(x[0] for x in PRIOR_INPUTS) | {"eligibility_a6"}):
        live[mod] = _prior_rows(mod)
    out = []
    for mod, prefix, grades, basis in PRIOR_INPUTS:
        hit = [st for rid, st in live[mod] if rid.startswith(prefix)]
        raw = hit[0] if len(hit) == 1 else "DRIFT"
        out.append({"module": mod, "row": prefix, "raw": raw, "gated": gate_status(raw, grades, True),
                    "grades": grades, "basis": basis})
    declared = set((x[0], x[1]) for x in PRIOR_INPUTS)
    undeclared = [(m, rid) for m, rows in sorted(live.items()) for rid, st in rows
                  if st == "MATCH" and not any(m == d[0] and rid.startswith(d[1]) for d in declared)]
    return {"rows": out, "undeclared_matches": undeclared}


# ------------------------------------------------------ erratum item 5 ---

OPEN_TARGETS = (
    {"target": "same-peoples / same-unit join (S-2, S-3)", "blocks": "E-A6.1-2", "now": "NOT_RECORDED"},
    {"target": "A-3 statute text for T-3 (the G-T3 gate)", "blocks": "E-A6.1-1", "now": "K, NOT_LANDED"},
    {"target": "S-4", "blocks": "E-A6.1-3", "now": "unsourced"},
    {"target": "individual ANCSA village corporations (200+)", "blocks": "E-A6.1-3", "now": "0 enumerated"},
    {"target": "complete 25 CFR 83.11(b)(2) path list", "blocks": "E-A6-3", "now": "4 of >= 11 retrieved"},
)


def fail_fixture():
    """A-6's boolean cannot represent ADMITTED_NOT_MEMBER: P-0 and P-ADMITTED read identically
    under eligibility_a6.eligible_sets and differ under 2a."""
    a, b = get_profile("P-0"), get_profile("P-ADMITTED")
    return {"a6_P-0": E6.eligible_sets(a)["eligible"], "a6_P-ADMITTED": E6.eligible_sets(b)["eligible"],
            "a61_P-0": dict(eligible_sets(a)["pairs"])["CS-R"], "a61_P-ADMITTED": dict(eligible_sets(b)["pairs"])["CS-R"]}


# ---------------------------------------------------------------- render ---

def render(out=None):
    wr = (out or sys.stdout).write
    wr("standing_a61 -- AMENDMENT A-6.1 over A-6: standing pairs, imposed scarcity, consolidation chains\n")
    wr("EXPECTED registered at %s; profiles and routes CONSTRUCTED; every CE line carried, none read here\n\n"
       % EXPECTED_COMMIT_A61)
    wr("-- expected (section 5); the row not holding first\n")
    for r in check_expectations():
        wr("expected %-20s %-9s %s\n" % (r["status"], r["id"], r["detail"]))
        wr("         raw %s; hold: %s\n" % (r["raw"], r["hold"]))
    um = unsourced_matches()
    wr("rows reading MATCH on input below S: %d%s [CHOICE 81]\n" % (len(um), " %s" % um if um else ""))
    wr("\n-- 2a standing pairs at 2026 (unit: case sets) [CHOICE 67]\n")
    for p in profiles():
        wr("   %-10s %s\n" % (p["profile_id"], " ".join("%s:%s" % x for x in eligible_sets(p)["pairs"])))
    wr("\n-- 2b/2c CS-R routes [CHOICE 71]\n")
    cps = seed_couplings()
    for r in seed_routes():
        wr("   %-24s min %-19s effective %-19s allocation_limited %s\n"
           % (r["route_id"], r["min_standing"], effective_min(r, cps), r["allocation_limited"]))
    for c in cps:
        wr("   coupling %s: %s (layer %s) -> %s raises_to %s flags %s\n"
           % (c["type"], c["source"], c["layer"], c["target"], c["raises_to"], c["flags"] or "none"))
    for rid, fl in scarcity_flags():
        wr("   flag %-24s %s\n" % (rid, fl))
    wr("\n-- standing_gap on CS-R (unit: routes) [CHOICE 68]\n")
    for p in profiles():
        g = standing_gap(p, "CS-R")
        wr("   %-10s standing %-19s gap %d band %s reachable %s undetermined %s\n"
           % (p["profile_id"], g["standing"], g["gap"], list(g["band"]), g["reachable_routes"], g["undetermined"]))
    wr("\n-- 2d consolidation events\n")
    for ev in consolidation_events():
        wr("   %s %s %s grade %s mechanism %s peoples_in %s prior_mode %s\n      unit_out %s\n"
           % (ev["event_id"], ev["date"], ev["instrument"], ev["grade"], ev["mechanism"], ev["peoples_in"],
              ev["prior_mode_of_peoples_in"], ev["unit_out"]))
    for fg in ce1_figures():
        wr("   CE-1 figure %-14s %-14s scope: %s (grade %s)\n" % (fg["figure"], fg["unit"], fg["scope"], fg["grade"]))
    wr("   CE-1 figures pooled: refused (ScopePooled) [CHOICE 75]\n")
    ws = worcester_split()
    wr("   CE-2 lawful_reach %s / physical outcome: %s; diverge %s (grade %s)\n"
       % (ws["lawful_reach"], ws["physical_outcome"], ws["diverge"], ws["grade"]))
    for a in alaska_cases():
        wr("   CE-3 %-58s mechanism %-23s control %s\n" % (a["case"], a["mechanism"], a["control"]))
    wr("   CE-3 forcing link (S, CE-3f): %s\n   CE-3 pipeline link: K (CE-3k), not an input\n"
       % SOURCES_A61["CE-3f"]["text"])
    for c in presumption_chains():
        wr("   chain %s: %s -> %s; join %s; missing: %s\n" % (c["chain_id"], c["consolidation_link"],
                                                            c["recognition_link"], c["join"], c["missing"]))
    rp = residence_presuming_paths()
    wr("\n-- CE-4 evidence paths (83.11(b)(2), list %s, %d retrieved; erratum: total %s, residence-presuming %s, "
       "grade %s) [CHOICE 74] [CHOICE 79]\n" % (rp["list"], rp["retrieved"], rp["carried_bounds"]["total"],
                                              rp["carried_bounds"]["residence_presuming"],
                                              rp["carried_bounds"]["grade"]))
    for x in EVIDENCE_PATHS_83_11_B2:
        wr("   %-5s names residence %-5s %s\n" % (x["path"], x["names_residence"], x["text"]))
    wr("   outside the retrieved text: >= %s paths, of them >= %s residence-presuming %s\n"
       % (rp["outside_retrieved_text"]["total"][3:], rp["outside_retrieved_text"]["residence_presuming"][3:],
          derived_tag()))
    for label, cnt in (("1 of 11, residence in (i) only", 1), ("3 of 11, residence in three", 3)):
        paths = [{"names_residence": i < cnt} for i in range(11)]
        sc = score_e_a6_3(paths, complete=True)
        wr("   complete constructed list, %s: >= 1 %s, >= 3 %s\n"
           % (label, sc["status"]["E-A6-3 REVISED"], sc["status"]["E-A6-3 ERRATUM"]))
    wr("   flexibility clause: %s\n   %s\n" % (rp["flexibility_clause"], rp["sufficiency"]))
    wr("   CE-5: 1994 83.7(f) retention in the current rule %s; E-A6-3 scored on current text only\n"
       % NOT_RECORDED)
    wr("\n-- sources: %s\n" % READ_HERE)
    for sid in sorted(SOURCES_A61):
        s = SOURCES_A61[sid]
        wr("   %-6s %-12s input %-5s %s\n" % (sid, s["grade"], s["input"], s["text"][:78]))
    wr("   still to source: %s\n" % ", ".join(STILL_TO_SOURCE))
    wr("\n-- A-3.1 on section 5\n")
    for x in registry():
        cc = R.complement(x)
        wr("   %-15s %-12s %s\n" % (x["id"], cc["status"], ", ".join(cc["gap_cells"][:4])))
    q = C.quotes_present([x for x in registry() if "source_file" not in x], AMENDMENT_FILE)
    qe = C.quotes_present([x for x in registry() if "source_file" in x], ERRATUM_FILE)
    wr("   quotes found in the amendment: %d/%d; in the erratum: %d/%d\n"
       % (len([1 for x in q if x[2]]), len(q), len([1 for x in qe if x[2]]), len(qe)))
    lt = C.lint_two_ways(AMENDMENT_FILE)
    ln = lint_nearest(AMENDMENT_FILE)
    wr("   unit lint: %d of %d count tokens outside the A-3.1 list; %d with '(unit: X)' read by the A-4 window "
       "[CHOICE 51]; %d by the nearest-count rule [CHOICE 78]; units declared %s\n"
       % (lt["fail_a31_list"], len(lt["tokens"]), lt["fail_with_annotation"], ln["fail_with_annotation"],
          lt["declared_units"]))
    wr("\n-- erratum item 4: an annotation adjacent to a different count [CHOICE 78]\n")
    for fx in annotation_fixture():
        wr("   %-21s owner %-2s window credits %-10s nearest credits %s\n"
           % (fx["fixture"], fx["owner"], fx["window_credits"], fx["nearest_credits"]))
    for row in lint_comparison():
        wr("   %-62s uncredited window %d, nearest %d of %d\n" % (row["file"], row["window"], row["nearest"], row["of"]))
        for ctx, a, b in row["moved"]:
            wr("      moved %-32r %s -> %s\n" % (ctx, a, b))
    ps = prior_sweep()
    wr("\n-- prior MATCH rows under the gate, read-only; A-1..A-5 modules not edited [CHOICE 83]; the gate here is "
       "[CHOICE 81], superseded by rule 0 (sourcing_a62.py)\n")
    for x in ps["rows"]:
        wr("   %-16s %-28s raw %-6s gated %-17s input %s (%s)\n"
           % (x["module"], x["row"], x["raw"], x["gated"], "/".join(x["grades"]), x["basis"]))
    wr("   of %d prior MATCH rows, %d read CONSTRUCTED_PASS under the gate; undeclared MATCH rows: %d\n"
       % (len(ps["rows"]), len([x for x in ps["rows"] if x["gated"] == CONSTRUCTED_PASS]),
          len(ps["undeclared_matches"])))
    wr("\n-- open sourcing targets (erratum item 5) [CHOICE 82]\n")
    for t in OPEN_TARGETS:
        wr("   %-46s blocks %-9s now %s\n" % (t["target"], t["blocks"], t["now"]))
    ff = fail_fixture()
    wr("\nfail fixture: A-6 eligible sets P-0 %s, P-ADMITTED %s (identical); A-6.1 CS-R standing P-0 %s, "
       "P-ADMITTED %s\n" % (ff["a6_P-0"], ff["a6_P-ADMITTED"], ff["a61_P-0"], ff["a61_P-ADMITTED"]))
    wr("holds: rule 1 met (%s; erratum %s); rule 3 met; rule 2 unmet (S-1..S-5 unsourced; nothing read here)\n"
       % (EXPECTED_COMMIT_A61, EXPECTED_COMMIT_ERRATUM))
    wr("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    wr("execution note: test_standing_a61.py prints the check count; samples/standing_a61.sample.txt is one "
       "recorded render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_standing_a61.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
