#!/usr/bin/env python3
# r1v2_audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# Audit of SOURCE_DROP_V2.md -- the main design-basis document revised
# with the audit chain folded back in. The original stays beside it
# untouched, per the revision's own effective-date rule (supersession
# recorded forward, the superseded entry unedited). This module edits
# neither.
#
# Two jobs. (1) A REPAIR MAP: each standing finding the revision
# addresses, checked mechanically against the new text rather than
# taken from the revision's own account. (2) A RE-TYPING: the WO3
# provision classes recomputed against the revised document, with the
# class derived from the text (a STATUS marker, an in-block incident
# name) and never hand-carried where the text can decide.
#
# Nothing here re-rates a prior DBK id: the WO2/WO3 findings keep
# their original ratings and their original targets (the files as
# delivered then); what this module records is the forward state.

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402
import wo3_return as W3  # noqa: E402

RUN_DATE = "2026-08-30"
V2 = "SOURCE_DROP_V2.md"
R1 = "SOURCE_DROP.md"


def _read(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read()


def p_block(doc, i):
    end = "### P%d" % (i + 1) if i < 8 else "## 3."
    return doc.split("### P%d" % i)[1].split(end)[0]


# ------------------------------------------------------ repair map

def repair_map():
    """Each standing finding the revision addresses, checked against
    the new text. 'closed' means the forward state no longer has the
    gap; the original finding keeps its rating on the original file."""
    v2 = _read(V2)
    r1 = _read(R1)
    blocks = dict((i, p_block(v2, i)) for i in range(1, 9))
    out = []

    out.append(("DBK_030 (P1/P6 declared-reading link)",
                "Fukushima" in blocks[1]
                and "Fukushima Daiichi" in blocks[6]
                and "~14 m wave" in blocks[1]
                and "Fukushima" not in p_block(r1, 1),
                "the incident is now named beside its number, and the "
                "~14 m arrived wave beside the 5.7 m figure -- the "
                "one-word amendment, taken, plus the load's other "
                "half"))

    status = dict((i, "STATUS     PROVISIONAL (DBK_030)" in blocks[i])
                  for i in range(1, 9))
    out.append(("DBK_030 (three of five unmarked assumptions)",
                all(status[i] for i in (2, 5, 8))
                and not any(status[i] for i in (1, 3, 4, 6, 7)),
                "P2, P5, P8 now open with a STATUS block naming the "
                "derivation path and citing the finding; the other "
                "five provisions carry no such block, so the marker "
                "is a state, not a header style"))

    fp = W3.falsify_parentheticals(v2)
    out.append(("DBK_031 (pre-answered FALSIFY parentheticals)",
                sum(1 for v in fp.values() if v == "asserted") == 0
                and fp["P3"] == "incident-backed",
                "the four asserted parentheticals are removed and the "
                "one incident-backed parenthetical (P3's aviation "
                "citation) is kept -- exactly the split the finding "
                "drew"))

    out.append(("DBK_014 (P3 VERIFY amendment)",
                "all THREE dissimilarity axes are ESTABLISHED"
                in blocks[3]
                and "KNOWN-same-builder pair fails this" in blocks[3]
                and "(DBK_014:" in blocks[3],
                "the amendment R2 promised: dissimilarity has to be "
                "established per axis, and a known-same-builder pair "
                "fails outright -- its agreement reads as N_eff 2 and "
                "is N_eff 1"))

    out.append(("WO2 T2 / DBK_027 (per-load provenance granularity)",
                "CUSTODY CHAIN" in v2
                and len(custody_rows()) == 9,
                "the custody table now exists in a delivered file, at "
                "the granularity WO2 found absent -- and it arrives "
                "already carrying its own intersection test"))

    out.append(("WO2 T3b / DBK_028 (effective-date clause)",
                "EFFECTIVE-DATE RULE" in v2
                and "append-only in BOTH senses" in v2
                and "EFFECTIVE-DATE RULE" not in r1,
                "the clause that previously existed only in a work "
                "order is now a delivered custody clause, and its four "
                "rules are the append-only practice the claim table "
                "already runs under"))

    return {"rows": out, "all_closed": all(ok for _n, ok, _w in out)}


# ------------------------------------------------- custody table

CUSTODY_ID = re.compile(r"^(A|B1|B2|C|D|E|F|P3|P0\.3)\s+(.*)$")

INCIDENT_KEY = {
    "Katrina": "Katrina", "East Palestine": "East Palestine",
    "aviation": "aviation", "Kerr County": "Kerr County",
    "BP Texas City": "BP Texas City", "Fukushima": "Fukushima",
}


def custody_rows():
    v2 = _read(V2)
    sec = v2.split("CUSTODY CHAIN")[1].split("WHY THE MULTI-SOURCING")[0]
    rows = {}
    current = None
    for line in sec.splitlines():
        m = CUSTODY_ID.match(line)
        if m:
            current = m.group(1)
            rows[current] = m.group(2)
        elif current and line.startswith(" "):
            rows[current] += " " + line.strip()
    return rows


def provenance_check():
    """The revision runs the doc's own P7 on its provenance and
    reports the measured value; this recomputes the pieces."""
    rows = custody_rows()
    keyed = {}
    for rid, text in rows.items():
        keyed[rid] = sorted(k for k in INCIDENT_KEY if k in text)
    shared = []
    ids = sorted(rows)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            common = set(keyed[ids[i]]) & set(keyed[ids[j]])
            if common:
                shared.append(("%s∩%s" % (ids[i], ids[j]),
                               sorted(common)))
    v2 = _read(V2)
    one = " ".join(v2.split())  # the phrase wraps across a line
    return {"n_positions": len(rows),
            "doc_states_nine": "of ~9 grounded" in v2,
            "shared_pairs": shared,
            "doc_names_both": "E ∩ F" in v2 and "B2 ∩ P3" in v2,
            "alarm_recomputed": DB.dissent_alarm(2, 1),
            "doc_states_alarm_fires":
                "dissent_alarm fires on (2 concurring loads" in v2,
            "b1_b2_adopt_dbk032":
                "East Palestine" in rows.get("B1", "")
                and "aviation" in rows.get("B2", "")
                and "DBK_032" in rows.get("B2", ""),
            "phrase_count": one.count("disjoint by construction"),
            "phrase_in_correction":
                '"disjoint by construction" was the schema framing'
                in one,
            "join_still_single_node":
                "genuinely different-builder" in v2}


# ------------------------------------------------------ re-typing

def retyping():
    """The WO3 typing recomputed against the revision. The class is
    derived from the v2 text: a STATUS marker makes PROVISIONAL, an
    in-block incident name makes DERIVED, P7's pending path is checked
    still present. Outline rows are carried from the WO3 tables, since
    the outline is not what this revision revises."""
    v2 = _read(V2)
    classes = {}
    for i in range(1, 9):
        pid = "P%d" % i
        blk = p_block(v2, i)
        if "STATUS     PROVISIONAL (DBK_030)" in blk:
            classes[pid] = "PROVISIONAL"
        elif "Fukushima" in blk or "AOA" in blk:
            classes[pid] = "DERIVED"
        elif pid == "P7" and "prediction to pre-register" in v2:
            classes[pid] = "PROVISIONAL"
        else:
            classes[pid] = "ASSUMPTION"
    # outline rows, unchanged by this revision
    for pid in W3.ORDER:
        if pid in classes:
            continue
        if pid in W3.DERIVED:
            classes[pid] = "DERIVED"
        elif pid in W3.PROVISIONAL:
            classes[pid] = "PROVISIONAL"
        else:
            classes[pid] = "ASSUMPTION"
    counts = dict((c, sum(1 for v in classes.values() if v == c))
                  for c in ("DERIVED", "PROVISIONAL", "ASSUMPTION"))
    unmarked = sorted(p for p, c in classes.items()
                      if c == "ASSUMPTION"
                      and p not in ("AX1", "AX2", "AX3", "AX4",
                                    "S5", "S6", "S7"))
    return {"classes": classes, "counts": counts,
            "was": {"DERIVED": 5, "PROVISIONAL": 3, "ASSUMPTION": 12},
            "unmarked_in_provision_form": unmarked,
            "result": "RETYPED"}


# ------------------------------------------------ what stays open

def open_items():
    v2 = _read(V2)
    v2out = _read("R2_OUTLINE_V2.md")
    return [
        ("P0.2 and P0.5 stay unmarked assumptions",
         "STATUS" not in v2out.split("P0.2  THE GATE")[1]
         .split("## 3.")[0],
         "they live in the outline, which this revision does not "
         "revise -- the remaining two of DBK_030's five"),
        ("DBK_022's D-row split stands in the outline",
         "D, F" in v2out and "P1-bounded, uncarried" in v2out,
         "one document, two answers, untouched by this revision"),
        ("the t constant stays unpinned",
         "# tune threshold" in v2,
         "per WO3's own NOT-ASKED: a load derived from the exposure "
         "sample, not a value to select"),
        ("one vocabulary residue",
         "worst-case behavior" in v2
         and "bound edge-case performance" in v2,
         "§5.3 keeps the original phrasing for the quantity P8's "
         "FALSIFY now calls edge-case performance -- same referent, "
         "two words, in a document that renamed it one section over"),
        ("the join stays single-node",
         "genuinely different-builder" in v2,
         "restated by the doc itself: DBK_014's gap is uncloseable "
         "from inside the pair, and the revision says so in its own "
         "provenance section"),
    ]


def harness_unchanged():
    src = _read("design_basis_checks.py")
    return src.strip() in _read(V2)


# ---------------------------------------------------------- render

def _wrap(s, n=66):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def render():
    out = []
    w = out.append
    w("SOURCE_DROP_V2 -- THE REVISION, AUDITED AS A CLOSURE MAP")
    w("")
    w("The original stays beside it untouched, per the revision's own")
    w("effective-date rule. Prior DBK ids keep their ratings on the")
    w("files as then delivered; this records the forward state, dated")
    w("%s." % RUN_DATE)
    w("")

    rm = repair_map()
    w("CLOSURE MAP (each closure checked against the new text)")
    for name, ok, why in rm["rows"]:
        w("  %-52s %s" % (name, "closed" if ok else "NOT CLOSED"))
        for ln in _wrap(why, 60):
            w("      " + ln)
    w("  all checked closures hold: %s" % rm["all_closed"])
    w("")

    pv = provenance_check()
    w("THE PROVENANCE SECTION'S OWN P7, RECOMPUTED")
    w("  custody positions parsed: %d (doc says ~9: %s)"
      % (pv["n_positions"], pv["doc_states_nine"]))
    w("  shared pairs at incident granularity:")
    for pair, common in pv["shared_pairs"]:
        w("    %-8s share %s" % (pair, ", ".join(common)))
    w("  the doc names both pairs itself: %s" % pv["doc_names_both"])
    w("  dissent_alarm(2,1) recomputed: %s (doc states it fires: %s)"
      % (pv["alarm_recomputed"], pv["doc_states_alarm_fires"]))
    w("  B1/B2 rows adopt the DBK_032 resolution: %s"
      % pv["b1_b2_adopt_dbk032"])
    w("  'disjoint by construction' occurs %d time(s), inside the"
      % pv["phrase_count"])
    w("  correction sentence: %s" % pv["phrase_in_correction"])
    for ln in _wrap(
            "The phrase WO2 could find in no delivered file now "
            "exists in one -- as the schema framing being corrected. "
            "The section quotes the two intersections from the audit "
            "record and arrives already carrying its measured value "
            "rather than the adopted claim; a third shared pair at "
            "finer granularity stays possible, which is what the "
            "doc's own 'at least' concedes."):
        w("  " + ln)
    w("")

    rt = retyping()
    w("THE TYPING, RECOMPUTED AGAINST THE REVISION")
    w("  was  : DERIVED 5 / PROVISIONAL 3 / ASSUMPTION 12")
    w("  now  : DERIVED %(DERIVED)d / PROVISIONAL %(PROVISIONAL)d / "
      "ASSUMPTION %(ASSUMPTION)d" % rt["counts"])
    w("  unmarked assumptions in provision-form text: %s (was 5)"
      % ", ".join(rt["unmarked_in_provision_form"]))
    for ln in _wrap(
            "The three in-doc unmarked assumptions took exactly the "
            "STATUS blocks the WO3 return specified; the remaining "
            "two live in the outline, which this revision does not "
            "touch. The class here is derived from the text -- a "
            "STATUS marker, an in-block incident name -- not carried "
            "from the prior table."):
        w("  " + ln)
    w("")

    w("WHAT STAYS OPEN, FORWARD")
    for name, ok, why in open_items():
        w("  %-46s %s" % (name, "" if ok else "(CHECK RED)"))
        for ln in _wrap(why, 60):
            w("      " + ln)
    w("")
    w("  the delivered harness block is byte-identical to")
    w("  design_basis_checks.py: %s" % harness_unchanged())
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("CLAIM_TABLE.md as DBK_034..DBK_036.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "r1v2_audit.py has no checks of its own. The checks that "
            "exercise it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    print(render())
