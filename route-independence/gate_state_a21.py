# SPDX-License-Identifier: CC0-1.0
"""gate_state_a21.py -- AMENDMENT A-2.1: source upgrades + fixture corrections, over A-2.

    python3 gate_state_a21.py             the corrected fixtures and the A-2.1 expectations
    python3 gate_state_a21.py --choices   every [CHOICE n] in force (numbered on from A-2's 1..8)
    python3 test_gate_state_a21.py        the checks; this module refuses --selftest

EXTENDS gate_state.py (A-2) and rebuilds nothing: every row goes through G.gate() with
A-2.1's source table passed in, every reading through G.reading_at() /
G.per_jurisdiction(), and A-2's own four expectations are re-run over the corrected
rows through G.check_expectations(rows_in=..., pair=...).  A-2's module, sample and
records are untouched; the A-2 fixture rows the amendment calls WRONG stay in A-2 as
the record of the authoring line and are superseded here, not edited.

WHAT A-2.1 CHANGES (sections 1 and 2)
    W-1a  the signed HB 16-1005 text, grade S -> P; effective 2016-08-10 conditional on
          sine die 2016-05-11, the condition confirmed by a second document.  A-2's
          HB_16_1005_VERIFICATION NOT_RUN is resolved at grade P BY THE AMENDMENT'S
          AUTHOR; this session still did not read the PDF (egress), so the row is
          CARRIED at P.
    W-2a  UT SB 32 (2010) enacting Utah Code 73-3-1.5, grade P at YEAR precision; the
          current text (2022 codification) grade P: unregistered = at most two covered
          containers EACH <= 100 gal; registered = <= 2,500 gal aggregate per parcel.
    F-W3  was WRONG (read 100 gal as a total): replaced by F-W3a (<= 100 gal each,
          METERED_PERMISSION), F-W3b (any container > 100 gal, PROHIBITED), both from
          2010 at year precision, and F-W3c (t < 2010, UNKNOWN, no prior-state source).
          F-W3a and F-W3b are one route in one jurisdiction in force at once, carried on
          A-2's new `condition` field, so the reading is BY_CONDITION, not CONFLICT.
    F-W1  was WRONG on the instrument: pre-2016 Colorado had no prohibition statute;
          the gate was the prior appropriation doctrine.  Split into F-W1a (t < 2009,
          PROHIBITED, instrument the doctrine, grade S, constitutional article not yet
          sourced) and F-W1b (2009 .. 2016-08-09, UNKNOWN until the 2009 bill is
          sourced).
    F-W4  Texas OPEN is a claim of ABSENCE and no enacting statute sources it: UNKNOWN
          until an agency or attorney-general statement is attached.  A-2's [CHOICE 6]
          year-precision reading is SUPERSEDED by the alternative A-2 printed beside it.

WHAT A-2.1 FLAGS AND DOES NOT BUILD (section 3)
    access_is_right {TRUE, FALSE, UNKNOWN} and revocable_by {None | named office}: both
    CO (HB 16-1005 s.1, "does not constitute a water right"; curtailment under
    37-92-502(2)(a)) and UT (registration is not a water right, per a secondary source)
    grant access declared NOT a right and revocable by an official, which the enum
    cannot separate from OPEN-by-right.  Carried as PROPOSED with the amendment's
    question attached and status NOT_BUILT; no route record here carries either key,
    asserted in the test.

WHAT A-2.1 RECORDS AND DOES NOT ADOPT (section 4)
    UT 73-2-27 (Class B misdemeanor default) and UT 73-1-1 (waters declared property of
    the public), grade S, carried with `input: False`; a row naming either as its
    gate_source is REFUSED at load.

CHOICES (numbered on from A-2's 1..8; printed by --choices; cited where each takes effect)
    9   the source table is A-2's with A-2.1's entries overlaid; an A-2 id keeps its A-2
        grade, and a fixture row cites the upgraded id (W-1a, W-2a) to carry P
    10  UT year precision "2010" is the amendment's own precision (SB 32 (2010),
        effective date not read); the two UT sub-conditions are copied from the
        amendment's section 1 text verbatim into `condition`
    11  F-W1b and F-W3c carry gate_source None, which A-2's schema admits for UNKNOWN;
        F-W4 likewise, with the reason in its note; none is hold-eligible
    12  UNMEASURED_OPEN is read off per_jurisdiction's `open_status`: no jurisdiction
        reads open and at least one reads UNKNOWN; OPEN_IN_NONE_MEASURED needs every
        jurisdiction known.  Neither is a closure reading.
    13  the E-A2.1-2 grade comparison is per jurisdiction on the rows IN FORCE at t;
        A-2's rows are re-scored the same way for the before column

KEY-HOLDER STATUS
    The amendment's section 5 is the EXPECTED block; the amendment was committed alone
    at 09774de before this file existed (rule 1).  Inputs are the amendment's sections 1
    and 2, CARRIED at the author's grades (P for W-1a / W-2a as read by the author, not
    by this session).  Fail fixture (rule 3): the A-2 F-W3 row as written, which reads
    100 gal as a total -- under the corrected sub-conditions it is the row A-2.1 calls
    WRONG, and the suite shows the corrected pair separating where it did not.  Failed
    predictions first (rule 4).

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D  # noqa: E402  FWO-5, reused
import settlement_split as S        # noqa: E402  A-1, reused
import gate_state as G              # noqa: E402  A-2, reused

EXPECTED_COMMIT_A21 = "09774de"

SOURCES21 = dict(G.SOURCES)   # [CHOICE 9]
SOURCES21.update({
    "W-1a": {"grade": "P", "text": "Colorado HB 16-1005, signed bill text (content.leg.colorado.gov/sites/default/files/"
                                   "2016a_1005_signed.pdf); effective 2016-08-10, CONDITIONAL on sine die 2016-05-11; "
                                   "condition confirmed by the CO Division of Real Estate 2016 Annual Report [P, read by "
                                   "the amendment's author]",
             "upgrades": "W-1"},
    "W-2a": {"grade": "P", "text": "Utah SB 32 (2010) enacting Utah Code 73-3-1.5 (le.utah.gov/~2010), YEAR precision, "
                                   "effective date not read; current text (Justia 2022 codification): unregistered = at "
                                   "most two covered containers EACH <= 100 gal; registered = <= 2,500 gal aggregate per "
                                   "parcel [P, read by the amendment's author]",
             "upgrades": "W-2", "precision": "year"},
    "UT-73-2-27": {"grade": "S", "text": "Utah Code 73-2-27, criminal penalty (Class B misdemeanor default): the "
                                         "enforcement mechanism for W-2", "input": False},
    "UT-73-1-1": {"grade": "S", "text": "Utah Code 73-1-1, waters declared property of the public: the root gate for "
                                        "W-2", "input": False},
})

HB_16_1005_VERIFICATION_A21 = ("RESOLVED at grade P by the amendment's author: signed bill text read, effective "
                               "2016-08-10 conditional on sine die 2016-05-11, condition confirmed by the CO Division of "
                               "Real Estate 2016 Annual Report; CARRIED here, the PDF not read by this session")

PROPOSED = {
    "fields": {"access_is_right": ("TRUE", "FALSE", "UNKNOWN"), "revocable_by": "None | named office"},
    "status": "NOT_BUILT",
    "grounds": "CO: HB 16-1005 s.1 rain barrel use 'does not constitute a water right', State Engineer may curtail under "
               "37-92-502(2)(a); UT: the registration is not a water right (secondary). Access declared NOT a right and "
               "revocable by an official, which the enum cannot separate from OPEN-by-right.",
    "question": "is METERED_PERMISSION with access_is_right = FALSE a sub-case of DISCRETIONARY? The G-2 transition "
                "(right -> charity) and the CO/UT grants (no right -> permission, not a right) may be one state reached "
                "from opposite directions. Test, do not assume.",
    "what_a_test_would_read": "who holds the revocation: on G-2 a private landowner with no office (no enforceable claim "
                              "against anyone), on CO/UT a named public office acting under a statute. Whether that "
                              "difference is a second axis or a label on one state is what a built field would let a "
                              "case set answer; nothing here answers it.",
}

CHOICES = {
    9: "source table = A-2's with A-2.1 overlaid; A-2 ids keep A-2 grades; rows cite W-1a / W-2a to carry P",
    10: "UT t_from '2010' at the amendment's own year precision; the two sub-conditions copied from section 1 verbatim",
    11: "F-W1b, F-W3c and F-W4 carry gate_source None under A-2's UNKNOWN rule, each with its reason; none hold-eligible",
    12: "UNMEASURED_OPEN read off open_status: no jurisdiction open and one or more UNKNOWN; not a closure reading",
    13: "E-A2.1-2 grades compared per jurisdiction on the rows in force at t; A-2's rows re-scored the same way",
}

_SRC_W1a = "CARRIED: A-2.1 section 1, W-1a (signed bill text, grade P as read by the amendment's author); unread here"
_SRC_W1 = "CARRIED: A-2 section 2, W-1 (secondary summary); the constitutional article for the doctrine is not yet sourced"
_SRC_W2a = "CARRIED: A-2.1 section 1, W-2a (grade P at year precision as read by the amendment's author); unread here"
_SRC_NONE = "CARRIED: A-2.1 section 2; no source for this interval; UNKNOWN by construction"

_UT_A = "unregistered; at most two covered containers, each <= 100 gal"     # [CHOICE 10]
_UT_B = "unregistered; any container > 100 gal"


def _row(name, src, requirement="water"):
    return G._a1_row(name, src, requirement)


def fixture_f_w1a():
    return G.gate(_row(G._RAIN, _SRC_W1), "rainwater_rooftop", "Colorado", None, "2009", G.PROHIBITED,
                  "prior appropriation doctrine (constitutional article not yet sourced)", "W-1",
                  requirement="water", note="F-W1a", sources=SOURCES21)


def fixture_f_w1b():
    return G.gate(_row(G._RAIN, _SRC_NONE), "rainwater_rooftop", "Colorado", "2009", G.HB_16_1005_EFFECTIVE,
                  G.UNKNOWN_STATE, None, None, requirement="water",
                  note="F-W1b; a 2009 Colorado law allowed limited collection, bill number NOT sourced [CHOICE 11]",
                  sources=SOURCES21)


def fixture_f_w2_p():
    return G.gate(_row(G._RAIN, _SRC_W1a), "rainwater_rooftop", "Colorado", G.HB_16_1005_EFFECTIVE, None,
                  G.METERED_PERMISSION, "HB 16-1005 (2016); C.R.S. 37-96.5-103", "W-1a",
                  requirement="water", note="F-W2; source upgraded S -> P", sources=SOURCES21)


def fixture_f_w3a():
    return G.gate(_row(G._RAIN + ", " + _UT_A, _SRC_W2a), "rainwater_rooftop", "Utah", "2010", None,
                  G.METERED_PERMISSION, "Utah Code 73-3-1.5 (SB 32, 2010)", "W-2a",
                  requirement="water", note="F-W3a", condition=_UT_A, sources=SOURCES21)


def fixture_f_w3b():
    return G.gate(_row(G._RAIN + ", " + _UT_B, _SRC_W2a), "rainwater_rooftop", "Utah", "2010", None,
                  G.PROHIBITED, "Utah Code 73-3-1.5 (SB 32, 2010)", "W-2a",
                  requirement="water", note="F-W3b", condition=_UT_B, sources=SOURCES21)


def fixture_f_w3c():
    return G.gate(_row(G._RAIN, _SRC_NONE), "rainwater_rooftop", "Utah", None, "2010", G.UNKNOWN_STATE, None, None,
                  requirement="water", note="F-W3c; no prior-state source [CHOICE 11]", sources=SOURCES21)


def fixture_f_w4_unknown():
    src = "CARRIED: A-2.1 section 2; OPEN is a claim of absence and no enacting statute sources it"
    return G.gate(_row(G._RAIN, src), "rainwater_rooftop", "Texas", None, None, G.UNKNOWN_STATE, None, None,
                  requirement="water",
                  note="F-W4; UNKNOWN until an agency or attorney-general statement is attached; A-2 [CHOICE 6] superseded",
                  sources=SOURCES21)


def fixture_rows():
    return [fixture_f_w1a(), fixture_f_w1b(), fixture_f_w2_p(), fixture_f_w3a(), fixture_f_w3b(), fixture_f_w3c(),
            fixture_f_w4_unknown(), G.fixture_f_g1(), G.fixture_f_g2()]


def events_declared():
    ev = [e for e in G.events_declared() if not (e["route_id"] == "rainwater_rooftop" and e["jurisdiction"] == "Colorado")]
    ev.append(G.event("rainwater_rooftop", "Colorado", G.HB_16_1005_EFFECTIVE, "HB 16-1005 (2016); C.R.S. 37-96.5-103",
                      G.UNKNOWN_STATE, G.METERED_PERMISSION, "W-1a", sources=SOURCES21,
                      note="EV-2 under A-2.1: the from-state is F-W1b's UNKNOWN, so the direction is UNKNOWN_DIRECTION "
                           "until the 2009 bill is sourced; A-2's PROHIBITED -> METERED reading rested on W-1 (S)"))
    ev.append(G.event("rainwater_rooftop", "Utah", "2010", "Utah Code 73-3-1.5 (SB 32, 2010)",
                      G.UNKNOWN_STATE, G.METERED_PERMISSION, "W-2a", sources=SOURCES21,
                      note="EV-4; from F-W3c UNKNOWN; to-state is the <= 100 gal condition; the > 100 gal condition "
                           "stays PROHIBITED and is not an event"))
    return ev


def fail_fixture():
    """Rule 3: the A-2 F-W3 row AS WRITTEN (100 gal read as a total, no condition) beside
    the two corrected UT rows.  As written it has no t and reads UNKNOWN; given the
    amendment's year it would sit in force beside both corrected rows with no
    condition, and A-2's reading_at returns CONFLICT rather than BY_CONDITION."""
    wrong = G.fixture_f_w3()
    wrong_dated = G.gate(_row(G._RAIN + ", over 100 gal, unregistered", "CONSTRUCTED: fail fixture, the A-2 F-W3 row given "
                                                                           "A-2.1's year; no condition"),
                         "rainwater_rooftop", "Utah", "2010", None, G.PROHIBITED, None, None, requirement="water",
                         tag=G.CONSTRUCTED_UNSOURCED)
    corrected = [fixture_f_w3a(), fixture_f_w3b()]
    return {"as_written": wrong, "as_written_reads": G.gate_reading(wrong),
            "as_written_dated_beside_corrected": G.reading_at(corrected + [wrong_dated], "rainwater_rooftop", "Utah", "2026")[0],
            "corrected": G.reading_at(corrected, "rainwater_rooftop", "Utah", "2026")}


# ------------------------------------------------------------- expectations ---

def check_expectations(t="2026"):
    rows = []
    pj = G.per_jurisdiction(fixture_rows(), t)
    r = pj["water"]["routes"]["rainwater_rooftop"]
    rd, gbj = r["readings"], r["grade_by_jurisdiction"]
    ut = rd.get("Utah")
    ut_ok = isinstance(ut, dict) and set(ut.values()) == {G.METERED_PERMISSION, G.PROHIBITED}
    ok1 = (rd.get("Colorado") == G.METERED_PERMISSION and gbj.get("Colorado") == "P"
           and ut_ok and gbj.get("Utah") == "P"
           and rd.get("Texas") == G.UNKNOWN_STATE
           and r["open_status"] == "UNMEASURED_OPEN")   # [CHOICE 12]
    rows.append(("E-A2.1-1 rainwater at 2026: CO METERED_PERMISSION (P), UT METERED_PERMISSION or PROHIBITED by container "
                 "size (P), TX UNKNOWN; OPEN nowhere sourced, reported UNMEASURED_OPEN not closure",
                 ok1, G.hold(ok1, [g for g in gbj.values() if g], r["hold_eligible"]),
                 "readings %s; grades %s; open_status %s" % (rd, gbj, r["open_status"])))
    before = G.per_jurisdiction(G.fixture_rows(), t)["water"]["routes"]["rainwater_rooftop"]["grade_by_jurisdiction"]
    a2 = dict((l.split(" ")[0], (v, h)) for l, v, h, _ in G.check_expectations(t))
    a21 = dict((l.split(" ")[0], (v, h)) for l, v, h, _ in G.check_expectations(t, rows_in=fixture_rows(),
                                                                                   pair=(fixture_f_w1a(), fixture_f_w2_p())))
    held_before = a2["E-A2-3"][1].startswith("HELD")
    held_after = a21["E-A2-3"][1].startswith("HELD")
    ok2 = (held_before == held_after and before.get("Colorado") == "S" and before.get("Utah") is None
           and gbj.get("Colorado") == "P" and gbj.get("Utah") == "P")   # [CHOICE 13]
    rows.append(("E-A2.1-2 the E-A2-3 hold count does not change; its rainwater grade moves S -> P for CO and UT",
                 ok2, G.hold(ok2, ["P", "S"], r["hold_eligible"]),   # rests on E-A2-3, which carries the gleaning row's S
                 "E-A2-3 before %s after %s; rainwater grade by jurisdiction before %s after %s -- Utah reads S -> P from "
                 "NO in-force row under A-2 (F-W3 had no t), not from S" % (a2["E-A2-3"][1], a21["E-A2-3"][1], before, gbj)))
    return [(label, "MATCH" if ok else "MISMATCH", h, note) for label, ok, h, note in rows]


# ------------------------------------------------------------------- render ---

def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("gate_state_a21 -- AMENDMENT A-2.1 over A-2: source upgrades and fixture corrections\n")
    w("every source CARRIED at the amendment author's grade; W-1a and W-2a read by the author, not here; "
      "EXPECTED registered at %s\n\n" % EXPECTED_COMMIT_A21)
    w("-- sources added or upgraded (section 1), and recorded-not-adopted (section 4)\n")
    for sid in ("W-1a", "W-2a", "UT-73-2-27", "UT-73-1-1"):
        s = SOURCES21[sid]
        w("   %-10s grade %-2s hold %-4s input %-5s %s\n" % (sid, s["grade"], G._fmt(G.hold_grade(sid, SOURCES21)),
                                                           s.get("input", True), s["text"][:90]))
    w("   HB 16-1005 effective date: %s\n\n" % HB_16_1005_VERIFICATION_A21)
    w("-- corrected fixture rows (declared state, then what the row READS)\n")
    w("   %-6s %-10s %-10s %-10s %-19s %-19s %-5s %-3s %-5s %s\n"
      % ("id", "juris", "t_from", "t_to", "declared", "reads", "src", "grd", "hold", "condition"))
    for r in fixture_rows():
        w("   %-6s %-10s %-10s %-10s %-19s %-19s %-5s %-3s %-5s %s\n"
          % (r["gate_note"].split(";")[0][:6], r["jurisdiction"][:10], G._fmt(r["t_from"]), G._fmt(r["t_to"]),
             r["gate_state"], G.gate_reading(r), G._fmt(r["gate_source"]), G._fmt(r["gate_grade"]), r["hold_eligible"],
             G._fmt(r["condition"])))
    w("   A-2 rows F-W1, F-W3, F-W4 stay in gate_state.py as the record of the authoring line; superseded here, not edited\n\n")
    w("-- events under A-2.1\n")
    for e in events_declared():
        w("   %-17s %-28s %-10s %-19s -> %-19s %-5s %-3s %-17s hold %s\n"
          % (e["route_id"], e["jurisdiction"][:28], G._fmt(e["date"]), e["from_state"], e["to_state"], e["source"],
             G._fmt(e["grade"]), e["direction"], e["hold_eligible"]))
    w("   A-2's EV-2 read PROHIBITED -> METERED_PERMISSION on W-1 (S); with F-W1b UNKNOWN the from-state is unsourced and "
      "the direction is UNKNOWN_DIRECTION until the 2009 bill is attached\n")
    rec = G.events_reconcile(events_declared(), G.events_derived(fixture_rows()))
    w("   derived and declared: %d; derived with no declared row: %s (the 2009 boundary: its instrument is the unsourced "
      "bill, so no event is declared for it); declared dated with no derivation: %s\n\n"
      % (len(rec["derived_declared"]), rec["derived_undeclared"] or "[]", rec["declared_underived"] or "[]"))
    w("-- rainwater at t=2026, per jurisdiction (never pooled) [CHOICE 12]\n")
    pj = G.per_jurisdiction(fixture_rows(), "2026")
    for req in ("water", "food"):
        for rid, r in pj[req]["routes"].items():
            w("   %-6s %-17s readings %s\n            grade by jurisdiction %s; verdict %s; open_status %s; hold %s\n"
              % (req, rid, r["readings"], r["grade_by_jurisdiction"], r["verdict"], r["open_status"], r["hold_eligible"]))
    w("   shelter, air, warmth: %s\n\n" % pj["shelter"]["verdict"])
    w("-- A-2's four expectations re-run over the corrected rows (pair F-W1a / F-W2)\n")
    for label, verdict, h, _ in sorted(G.check_expectations(rows_in=fixture_rows(), pair=(fixture_f_w1a(), fixture_f_w2_p())),
                                       key=lambda x: x[1] != "MISMATCH"):
        w("   %-8s %-38s %s\n" % (verdict, h, label[:80]))
    w("\n-- section 3, PROPOSED and NOT BUILT\n")
    w("   fields %s; status %s\n   question: %s\n   what a test would read: %s\n\n"
      % (sorted(PROPOSED["fields"]), PROPOSED["status"], PROPOSED["question"], PROPOSED["what_a_test_would_read"]))
    w("-- expected (section 5), MISMATCH rows first\n")
    for label, verdict, h, note in sorted(check_expectations(), key=lambda x: x[1] != "MISMATCH"):
        w("expected %-8s %-38s %s\n         %s\n" % (verdict, h, label, note))
    ff = fail_fixture()
    w("\nfail fixture: A-2's F-W3 as written reads %s (no t); given A-2.1's year and no condition beside the two corrected "
      "rows it reads %s; the corrected pair alone reads %s\n"
      % (ff["as_written_reads"], ff["as_written_dated_beside_corrected"], ff["corrected"][0]))
    w("holds: rule 1 met (%s); rule 3 met; rule 2 met at grade P by the amendment's author for W-1a / W-2a and at S for "
      "the doctrine row, all CARRIED here\n" % EXPECTED_COMMIT_A21)
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_gate_state_a21.py prints the check count; samples/gate_state_a21.sample.txt is one recorded "
      "render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_gate_state_a21.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
