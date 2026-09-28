# SPDX-License-Identifier: CC0-1.0
"""AMENDMENT A-6 (2026-09-28): eligibility-gated terminus count, and the recognition
asymmetry.

Landed verbatim as AMENDMENT_A6_2026-09-28_eligibility-recognition.md and committed ALONE
at EXPECTED_COMMIT_A6 before this module existed (rule 1).  Additive: A-4 and A-5 are
read by import; A-5's terminus_kinds is kept and answers a different question.

  2a  each case set has an entry chain (A-4 shape), eligibility basis, acquirable-by-
      outsider (NOT_RECORDED unless a source states the rule), entry_revocable_by
  2b  person profiles: CONSTRUCTED test cases, never a real individual
  2c  eligible_sets (unit: case sets), reachable_terminus_kinds (unit: kinds),
      reachable_nonmonetary_chains (unit: chains), exists_vs_reachable_gap (the set)
  2d  a route documented only in an unrecognized people's practice: lawful_reach
      NOT_RECORDED, never TRUE and never FALSE; recognition status with dated events
  3   residence_presuming_criteria over 25 CFR 83.11: NOT_EVALUABLE until RA-1 is read
      in full; never filled from memory

No real person, family or people is named or described.  Nothing here is legal advice
or a statement of law beyond a cited text (RIN_076), and section 3 makes no claim about
any petition's merits.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import gate_state as G      # noqa: E402  A-2 event shape
import chains_a4 as C       # noqa: E402  A-4
import termini_a5 as F      # noqa: E402  A-5
import repairs_a31 as R     # noqa: E402  A-3.1

EXPECTED_COMMIT_A6 = "f8f3135"
AMENDMENT_FILE = "AMENDMENT_A6_2026-09-28_eligibility-recognition.md"
NOT_EVALUABLE = F.NOT_EVALUABLE
TRUE, FALSE, NOT_RECORDED = C.TRUE, C.FALSE, C.NOT_RECORDED
BASES = ("BIRTH", "DESCENT_DOCUMENTED", "ENROLLMENT_BY_NATION", "RECOGNITION_BY_STATE", "COMMUNITY_ADMISSION",
         "DEFAULT_RESIDENT", NOT_RECORDED)
ACQUIRABLE = (TRUE, FALSE, "RARE", NOT_RECORDED)
RECOGNITION = ("RECOGNIZED", "UNRECOGNIZED", "TERMINATED", "RESTORED", NOT_RECORDED)
REFUSED_AT = "CONNECT refused 2026-09-28T13:14:37Z (ecfr.gov, law.cornell.edu); github.com connected as the control"

CHOICES = {
    59: "an entry chain is an ALL / ANY expression over profile attributes and dated recognition states, read "
        "three-valued as A-4 reads lawful reach; a nation's recognition at t comes from its event table",
    60: "CS-R's nation is the amendment's own 'CS-R nation', whose RECOGNIZED status P-1 presumes (grade K, stated by "
        "the fixture); P-4's nation is a second reservation case set, CS-R4, whose timeline is RA-3's candidate pair "
        "(1954, 1973), grade K, the dates the order's",
    61: "entry_condition text is NOT_RECORDED for every set: no source stating an entry rule was read; the entry "
        "structure is the amendment's fixture text; acquirable_by_outsider NOT_RECORDED throughout (section 6)",
    62: "a case set NOT_EVALUABLE under A-5 contributes unknown kinds: a reachable set built over it is partial and "
        "the gap over all sets is NOT_EVALUABLE; kinds are compared without hops, A-5's second reading",
    63: "E-A6-4 evaluates P-4 at the two dates the order names, 1954 and 1973, each read as the first day of its year",
    65: "a profile's enrollments and admissions are exactly those its fixture line names, others FALSE; every "
        "profile is a resident of the general set, as P-0's line and every other line's 'CS-G' state",
    64: "an instrument-only case set CS-X (constructed, one chain whose token leaf never reaches money) shows the gap "
        "can be non-empty; it enters no expectation",
}


# ----------------------------------------------------------- recognition ---

def recognition_event(nation, date, from_state, to_state, source, instrument, note=""):
    """Same keys as A-2's gate_change_events row; states from the recognition enum."""
    for st in (from_state, to_state):
        if st not in RECOGNITION:
            raise C.ChainError("recognition state is one of %s; got %r" % (RECOGNITION, st))
    d = G._date(date, "date", nation)
    grade = SOURCES_A6[source]["grade"]
    return {"route_id": "recognition:" + nation, "jurisdiction": "FEDERAL", "date": d, "instrument": instrument,
            "from_state": from_state, "to_state": to_state, "source": source, "grade": grade,
            "direction": "%s->%s" % (from_state, to_state), "flagged": grade == "K", "undated": d is None,
            "hold_eligible": grade != "K" and d is not None, "note": note}


SOURCES_A6 = {
    "RA-1": {"grade": "K", "status": "NOT_LANDED", "text": "25 CFR Part 83, the federal acknowledgment criteria "
                                                           "(83.11), to be read in full"},
    "RA-2": {"grade": "K", "status": "NOT_LANDED", "text": "the criterion on members predominantly members of another "
                                                           "acknowledged tribe"},
    "RA-3": {"grade": "K", "status": "NOT_LANDED", "text": "one Termination-era act and its restoration act (the order's "
                                                           "candidate pair: termination 1954, restoration 1973)"},
    "RA-4": {"grade": "K", "status": "NOT_LANDED", "text": "one nation's published enrollment criteria"},
    "RA-5": {"grade": "K", "status": "NOT_LANDED", "text": "an Amish-conversion rate or count from published "
                                                           "ethnography"},
    "A6-4": {"grade": "K", "status": "STATED_BY_AMENDMENT", "text": "A-6 section 4 fixture text"},
}


def events_r4():
    """[CHOICE 60]"""
    return [recognition_event("CS-R4 nation", "1954", "RECOGNIZED", "TERMINATED", "RA-3", "termination act (RA-3)"),
            recognition_event("CS-R4 nation", "1973", "TERMINATED", "RESTORED", "RA-3", "restoration act (RA-3)")]


def recognition_at(events, initial, t):
    st = initial
    for e in sorted(events, key=lambda e: e["date"]):
        if e["date"] is not None and e["date"] <= t:
            st = e["to_state"]
    return st


RECOGNITION_TABLE = {"CS-R nation": ([], "RECOGNIZED"), "CS-R4 nation": (events_r4(), "RECOGNIZED")}


# ------------------------------------------------------------- case sets ---

def attr(name):
    return ("attr", name)


def recognized(nation):
    return ("recognized", nation)


CASE_SETS = {
    "CS-G": {"entry": C.ALL(attr("resident")), "basis": "DEFAULT_RESIDENT", "revocable_by": NOT_RECORDED},
    "CS-R": {"entry": C.ALL(recognized("CS-R nation"), attr("enrolled_CS-R")), "basis": "ENROLLMENT_BY_NATION",
             "revocable_by": NOT_RECORDED},
    "CS-R4": {"entry": C.ALL(recognized("CS-R4 nation"), attr("enrolled_CS-R4")), "basis": "ENROLLMENT_BY_NATION",
              "revocable_by": "Congress (RA-3 structure, K)"},
    "CS-A": {"entry": C.ALL(attr("community_admitted")), "basis": "COMMUNITY_ADMISSION", "revocable_by": NOT_RECORDED},
}
for _v in CASE_SETS.values():
    _v["entry_condition"] = NOT_RECORDED          # [CHOICE 61]
    _v["acquirable_by_outsider"] = NOT_RECORDED


def entry_value(expr, profile, t):
    """[CHOICE 59]"""
    k = expr[0]
    if k in ("ALL", "ANY"):
        vals = [entry_value(x, profile, t) for x in expr[1]]
        return C.v_and(vals) if k == "ALL" else C.v_or(vals)
    if k == "attr":
        v = profile["attributes"].get(expr[1], NOT_RECORDED)
        return v if v in (TRUE, FALSE, NOT_RECORDED) else NOT_RECORDED
    if k == "recognized":
        events, initial = RECOGNITION_TABLE[expr[1]]
        st = recognition_at(events, initial, t)
        return TRUE if st in ("RECOGNIZED", "RESTORED") else (NOT_RECORDED if st == NOT_RECORDED else FALSE)
    raise C.ChainError("unknown entry term %r" % (expr,))


# -------------------------------------------------------------- profiles ---

def profile(pid, **attributes):
    return {"profile_id": pid, "constructed": True, "attributes": dict(attributes)}


def profiles():
    """2b: CONSTRUCTED test cases, nothing about any real person.  A profile's enrollments
    and admissions are exactly the ones its fixture line names; any other reads FALSE
    [CHOICE 65]."""
    base = {"resident": TRUE, "enrolled_CS-R": FALSE, "enrolled_CS-R4": FALSE, "community_admitted": FALSE}

    def mk(pid, **kw):
        a = dict(base)
        a.update(kw)
        return profile(pid, **a)
    return [
        mk("P-0"),
        mk("P-1", **{"enrolled_CS-R": TRUE}),
        mk("P-2", community_admitted=TRUE),
        mk("P-3", descent_documented_several=TRUE),
        mk("P-4", **{"enrolled_CS-R4": TRUE}),
    ]


def get_profile(pid):
    return [p for p in profiles() if p["profile_id"] == pid][0]


def eligible_sets(p, t="2026"):
    vals = dict((cs, entry_value(v["entry"], p, t)) for cs, v in sorted(CASE_SETS.items()))
    return {"eligible": sorted(cs for cs, v in vals.items() if v == TRUE),
            "undetermined": sorted(cs for cs, v in vals.items() if v == NOT_RECORDED), "values": vals,
            "unit": "case sets"}


# -------------------------------------------------------------- measurands ---

def set_kinds(cs, need, world=None):
    """[CHOICE 62]  CS-G is A-5's world; CS-X the instrument set; the rest NOT_EVALUABLE."""
    if cs == "CS-G":
        w = F.layered_world() if world is None else world
        return set(F.terminus_kinds(w, need, with_hops=False)["kinds"])
    if cs == "CS-X":
        return set(F.terminus_kinds(world_x(), need, with_hops=False)["kinds"])
    return None


def world_x():
    """[CHOICE 64]  One constructed chain whose token leaf stops at CITATION."""
    nodes = F.token_nodes()
    nodes["CIT_END"] = {"token_type": "CITATION", "converts_to": None, "hops": 0}
    w = C.World(chains={}, tokens=nodes)
    w.chains["X-1"] = C.chain("X-1", "FOOD", "constructed", [
        C.step("exchange", "exchange standing for food", "FOOD", C.ALL(C.leaf_token("CIT_END")))], (),
        lifted_from="CONSTRUCTED A-6 instrument set; enters no expectation")
    return w


def _kinds_x(need):
    w = world_x()
    out = set()
    for c in F.chains_of(w, need):
        for l in C.termini(w, c)["leaves"]:
            out.add(F.resolved_leaf(l, w.tokens)[:2])
    return out


def reachable_terminus_kinds(p, need, sets=None, t="2026"):
    sets = sorted(CASE_SETS) if sets is None else sets
    el = [cs for cs in eligible_sets(p, t)["eligible"] if cs in sets]
    known, unknown = set(), []
    for cs in el:
        k = _kinds_x(need) if cs == "CS-X" else set_kinds(cs, need)
        if k is None:
            unknown.append(cs)
        else:
            known |= k
    return {"kinds": sorted(known, key=repr), "partial_over": unknown, "eligible": el, "unit": "kinds"}


def exists_vs_reachable_gap(p, need, sets=None, extra=None, t="2026"):
    sets = sorted(CASE_SETS) if sets is None else sets
    allk, unknown = set(), []
    for cs in sets + (extra or []):
        k = _kinds_x(need) if cs == "CS-X" else set_kinds(cs, need)
        if k is None:
            unknown.append(cs)
        else:
            allk |= k
    reach = reachable_terminus_kinds(p, need, sets + (extra or []), t)
    if unknown:
        return {"status": NOT_EVALUABLE, "gap": None, "unsourced_sets": unknown, "unit": "kinds"}
    gap = sorted(allk - set(reach["kinds"]), key=repr)
    return {"status": "COMPUTED", "gap": gap, "unsourced_sets": [], "unit": "kinds"}


def reachable_nonmonetary_chains(p, need, reading="LAWFUL_STRICT", t="2026"):
    el = eligible_sets(p, t)["eligible"]
    if el != ["CS-G"] and any(set_kinds(cs, need) is None for cs in el if cs != "CS-G"):
        return {"status": NOT_EVALUABLE, "count": None, "unit": "chains"}
    v = F.nonmonetary_chains(F.layered_world(), need)[reading]
    return {"status": "COMPUTED", "count": len(v), "chains": v, "unit": "chains"}


def a5_pooled_kinds(need):
    """The fail fixture: A-5's terminus_kinds pools every set, so every profile reads the
    same kinds whatever sets it may enter."""
    k = set(set_kinds("CS-G", need)) | _kinds_x(need)
    return sorted(k, key=repr)


def lawful_reach_unrecognized_practice(route_note):
    """2d: a route documented only in the practice of a people with no recognized legal
    status reads NOT_RECORDED, never TRUE and never FALSE."""
    return {"lawful_reach": NOT_RECORDED, "basis": "2d: " + route_note}


# ------------------------------------------------------- section 3 ---

def residence_presuming_criteria():
    return {"status": NOT_EVALUABLE, "count": None, "unit": "criteria",
            "reason": "RA-1 (25 CFR 83.11) not read in full; %s; not filled from memory" % REFUSED_AT}


# ----------------------------------------------------------- registry ---

def registry():
    import itertools
    E = []

    def e(eid, pq, fq, space, p, f, mn=1, mx=1):
        E.append({"id": eid, "variant": "", "amendment": "A-6", "p_quote": pq, "f_quote": fq, "f_form": R.STATED,
                  "f_requires": R.CODE_BEHAVIOUR, "requires_reason": "a reading of constructed profiles",
                  "space": tuple(space), "min_cells": mn, "max_cells": mx, "p": p, "f": f})
    e("E-A6-1", "eligible_sets(P-3) = 1 (unit: case sets).", "eligible_sets(P-3) >= 2.", range(4),
      lambda w: w[0] == 1, lambda w: w[0] >= 2)
    e("E-A6-2", "exists_vs_reachable_gap is non-empty for >= 1 of P-0..P-4 for some need (unit: profiles).",
      "the gap is empty for every profile and need.", ("NONEMPTY", "EMPTY", NOT_EVALUABLE),
      lambda w: "NONEMPTY" in w, lambda w: all(c == "EMPTY" for c in w), 1, 2)
    e("E-A6-3", "residence_presuming_criteria >= 1 (unit: criteria) on reading RA-1 in full.",
      "0 criteria after a full read.", (0, 1, 2, NOT_EVALUABLE),
      lambda w: w[0] != NOT_EVALUABLE and w[0] >= 1, lambda w: w[0] == 0)
    e("E-A6-4", "under RA-3, eligible_sets for P-4 differs between the termination date and the restoration date",
      "identical at both dates.", ("DIFFER", "IDENTICAL"), lambda w: w[0] == "DIFFER", lambda w: w[0] == "IDENTICAL")
    return E


# ------------------------------------------------------- expectations ---

def check_expectations():
    rows = []
    p3 = eligible_sets(get_profile("P-3"))
    rows.append({"id": "E-A6-1", "status": NOT_EVALUABLE,
                 "hold": "entry rules unsourced (RA-4, A-3s not read); coverage 0/%d entry chains sourced"
                         % len(CASE_SETS),
                 "detail": "K reading: eligible_sets(P-3) = %d case set %s, undetermined %s; matches the "
                           "prediction by construction of the fixture" % (len(p3["eligible"]), p3["eligible"],
                                                                         p3["undetermined"])})
    gaps = dict(((p["profile_id"], n), exists_vs_reachable_gap(p, n)) for p in profiles() for n in C.ROUTE_NEEDS)
    ne = sorted(set(k[0] for k, v in gaps.items() if v["status"] == NOT_EVALUABLE))
    rows.append({"id": "E-A6-2", "status": NOT_EVALUABLE,
                 "hold": "coverage 1/%d case sets built (CS-G)" % len(CASE_SETS),
                 "detail": "the gap is NOT_EVALUABLE for %d of %d profiles on every need: %s carry no kinds until "
                           "sourced; not filled from CS-G" % (len(ne), len(profiles()),
                                                             sorted(set(s for v in gaps.values()
                                                                        for s in v["unsourced_sets"])))})
    rp = residence_presuming_criteria()
    rows.append({"id": "E-A6-3", "status": NOT_EVALUABLE, "hold": "coverage 0/1 RA-1 read", "detail": rp["reason"]})
    p4 = get_profile("P-4")
    a, b = eligible_sets(p4, "1954-01-01"), eligible_sets(p4, "1973-01-01")
    rows.append({"id": "E-A6-4", "status": NOT_EVALUABLE, "hold": "RA-3 grade K; coverage 0/2 events sourced",
                 "detail": "K reading at the order's dates [CHOICE 63]: %s at 1954, %s at 1973; %s"
                           % (a["eligible"], b["eligible"], "differ" if a["eligible"] != b["eligible"] else
                              "identical")})
    return rows


def consistency_check():
    """Section 5's consistency check: where A-5's E-A5-1 holds under a reading,
    reachable_nonmonetary_chains(P-3) = 0 on that reading.  Asserted, not scored."""
    out = []
    p3 = get_profile("P-3")
    w = F.layered_world()
    for reading in F.READINGS:
        holds = all(not F.nonmonetary_chains(w, n)[reading] for n in C.ROUTE_NEEDS)
        rn = [reachable_nonmonetary_chains(p3, n, reading)["count"] for n in C.ROUTE_NEEDS]
        ok = (not holds) or all(x == 0 for x in rn)
        out.append({"reading": reading, "e_a5_1_holds": holds, "p3_counts": rn, "implication_holds": ok})
    assert all(r["implication_holds"] for r in out), out
    return out


def fail_fixture():
    p3 = get_profile("P-3")
    pooled = a5_pooled_kinds("FOOD")
    reach = reachable_terminus_kinds(p3, "FOOD", ["CS-G", "CS-X"])
    return {"a5_pooled": pooled, "a6_reachable": reach["kinds"],
            "gap": exists_vs_reachable_gap(p3, "FOOD", ["CS-G"], ["CS-X"])}


# ---------------------------------------------------------------- render ---

def render(out=None):
    wr = (out or sys.stdout).write
    wr("eligibility_a6 -- AMENDMENT A-6 over A-4 / A-5: eligible sets, reachable termini, recognition\n")
    wr("EXPECTED registered at %s; profiles are CONSTRUCTED; every entry rule and every recognition event K\n\n"
       % EXPECTED_COMMIT_A6)
    wr("-- expected (section 5); every row NOT_EVALUABLE, the K reading beside it\n")
    for r in check_expectations():
        wr("expected %-13s %-8s %s\n" % (r["status"], r["id"], r["detail"]))
        wr("         hold: %s\n" % r["hold"])
    wr("\n-- case sets (2a) [CHOICE 61]\n")
    for cs, v in sorted(CASE_SETS.items()):
        wr("   %-6s basis %-21s entry_condition %-13s acquirable_by_outsider %-13s revocable_by %s\n"
           % (cs, v["basis"], v["entry_condition"], v["acquirable_by_outsider"], v["revocable_by"]))
    wr("\n-- eligible_sets per constructed profile at 2026 (unit: case sets)\n")
    for p in profiles():
        es = eligible_sets(p)
        wr("   %-4s eligible %s; undetermined %s\n" % (p["profile_id"], es["eligible"], es["undetermined"]))
    wr("   P-4 at 1954: %s; at 1973: %s [CHOICE 63]\n" % (eligible_sets(get_profile("P-4"), "1954-01-01")["eligible"],
                                                         eligible_sets(get_profile("P-4"), "1973-01-01")["eligible"]))
    wr("\n-- recognition events (A-2 event keys; RA-3, K)\n")
    for e in events_r4():
        wr("   %s %s %s  source %s grade %s flagged %s\n" % (e["route_id"], e["date"], e["direction"], e["source"],
                                                           e["grade"], e["flagged"]))
    wr("   2d: %s\n" % lawful_reach_unrecognized_practice("documented only in the practice of an unrecognized "
                                                           "people")["lawful_reach"])
    wr("\n-- section 3: residence_presuming_criteria %s (%s)\n" % (residence_presuming_criteria()["status"],
                                                                  residence_presuming_criteria()["reason"]))
    for sid in sorted(SOURCES_A6):
        s = SOURCES_A6[sid]
        wr("   %-5s %s %-19s %s\n" % (sid, s["grade"], s["status"], s["text"][:80]))
    wr("\n-- consistency check (asserted, not scored)\n")
    for r in consistency_check():
        wr("   %-14s E-A5-1 holds %-5s P-3 reachable nonmonetary per need %s; implication holds %s\n"
           % (r["reading"], r["e_a5_1_holds"], r["p3_counts"], r["implication_holds"]))
    wr("\n-- A-3.1 on section 5\n")
    for x in registry():
        cc = R.complement(x)
        wr("   %-8s %-12s %s\n" % (x["id"], cc["status"], ", ".join(cc["gap_cells"][:4])))
    q = C.quotes_present(registry(), AMENDMENT_FILE)
    wr("   quotes found in the amendment: %d/%d\n" % (len([1 for x in q if x[2]]), len(q)))
    lt = C.lint_two_ways(AMENDMENT_FILE)
    wr("   unit lint: %d of %d count tokens outside the A-3.1 list; %d with '(unit: X)' read; units declared %s\n"
       % (lt["fail_a31_list"], len(lt["tokens"]), lt["fail_with_annotation"], lt["declared_units"]))
    ff = fail_fixture()
    wr("\nfail fixture: A-5's pooled FOOD kinds %s; P-3's reachable kinds %s; the gap %s [CHOICE 64]\n"
       % (ff["a5_pooled"], ff["a6_reachable"], ff["gap"]["gap"]))
    wr("holds: rule 1 met (%s); rule 3 met; rule 2 unmet (RA-1..RA-5 not read)\n" % EXPECTED_COMMIT_A6)
    wr("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    wr("execution note: test_chains_a456.py prints the check count; samples/eligibility_a6.sample.txt is one "
       "recorded render, compare before quoting\n")


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
