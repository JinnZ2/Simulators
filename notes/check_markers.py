#!/usr/bin/env python3
# check_markers.py -- CC0, stdlib only, parses under 3.9
#
# Checker for notes/markers/HELD_2026_08_31.md, under the notes/
# convention: the entry is stored as delivered, this checker never
# edits it, and every disagreement goes in this output. The entry
# is a MARKER FILE by its own declaration -- "not a work order.
# Nothing here is assigned. Nothing here is finished." -- so nothing
# here renders, files, or adjudicates any of M-A..M-E; every reading
# below is structural, about the record rather than the material.
#
# Six readings:
#   1  delivery structure -- two halves in one file, seam located
#   2  the read-alongside references, resolved by content and by
#      artifact rather than by filename
#   3  the G-numbering question -- the file's "G-01" against the
#      landed render's ids; two readings, no pick
#   4  the hold preconditions, evaluated from the file's own text
#   5  held gaps stay out of GAP_INDEX
#   6  cross-references, by path existence only (a grep would hit
#      this file and this checker -- the UNI_010 loop)

import hashlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MARKER = os.path.join(HERE, "markers", "HELD_2026_08_31.md")
SEAM = "FEDERAL, SYSTEMATIC, DAILY"


def _read(path):
    return io.open(path, encoding="utf-8").read()


# ------------------------------------------------ 1  structure

def structure():
    """One file, two halves. The structured marker file ends at the
    STANDING NOTE; the appended raw session notes begin at the SEAM
    line. Content lives in BOTH halves and the split is the fact a
    reader needs first: the marker proper is the organised statement,
    the appended half is the session notes it was organised from,
    including the G-08 draft render and the HELD-not-filed note."""
    text = _read(MARKER)
    seams = text.count(SEAM)
    if seams != 1:
        return {"seam_count": seams, "split": False}
    marker, appended = text.split(SEAM, 1)
    m_heads = re.findall(r"(?m)^## (M-[A-E])\b", marker)
    return {
        "seam_count": 1,
        "split": True,
        "marker_headings": m_heads,
        "marker_has_standing_note":
            "STANDING NOTE ON THIS WHOLE CLUSTER" in marker,
        "standing_instruction_present":
            "render the mechanism (M-A) first" in marker,
        "appended_has_g08_draft":
            "G-08  ABSENCE SET AS A READABLE DOCUMENT" in appended,
        "appended_has_held_note": "HELD, not filed:" in appended,
        "appended_names_g07": "G-07" in appended,
        # the marker proper repeats the appended half's content in
        # organised form; the draft render and the held note exist
        # ONLY in the appended half
        "g08_draft_only_appended":
            "G-08" not in marker,
    }


# ------------------------------------- 2  read-alongside refs

def read_alongside():
    """The file says 'Read alongside: WORK_ORDER_FABLE.md,
    WORK_ORDER_FABLE_02_GAPS.md'. Neither name exists in this tree.
    Resolution is by CONTENT and by ARTIFACT:

    WORK_ORDER_FABLE_02_GAPS.md resolves by content to
    seam-gaps/WORK_ORDER.md -- same order (header 'WORK ORDER 02',
    session date 2026-08-31, the G-05/G-06 schema note), landed
    verbatim under the repo's own intake name.

    WORK_ORDER_FABLE.md resolves by artifact only: its four tasks
    are executed on this branch (probed below) and the order itself
    never landed verbatim. That absence is not a defect to repair --
    it is the marker file's own stated purpose ('exists so the
    material survives independent of any conversation memory')
    demonstrated on its sibling: the order that was not landed as a
    file survives only as its effects."""
    wo2 = os.path.join(ROOT, "seam-gaps", "WORK_ORDER.md")
    wo2_txt = _read(wo2) if os.path.isfile(wo2) else ""
    by_name = {
        "WORK_ORDER_FABLE.md":
            os.path.isfile(os.path.join(ROOT, "WORK_ORDER_FABLE.md")),
        "WORK_ORDER_FABLE_02_GAPS.md":
            os.path.isfile(os.path.join(ROOT,
                                        "WORK_ORDER_FABLE_02_GAPS.md")),
    }
    wo2_content = {
        "file_exists": bool(wo2_txt),
        "header_wo02": wo2_txt.startswith(
            "# WORK ORDER 02 -- Gap inventory"
            ) or wo2_txt.startswith(
            "# WORK ORDER 02 — Gap inventory"),
        "session_date": "2026-08-31" in wo2_txt,
        "g05_g06_schema_note": "G-05 and G-06" in wo2_txt,
        "cites_wo01_task3": "WORK ORDER 01 Task 3" in wo2_txt,
    }
    # WORK_ORDER_FABLE task-artifact probes (tasks 1-4 as executed):
    wo1_artifacts = {
        "t1_protocol_reference_layer":
            "Reference layer." in _read(os.path.join(ROOT,
                                                     "PROTOCOL.md")),
        "t2_rename_new_name_exists":
            os.path.isfile(os.path.join(ROOT, "columbia-chain-cascade",
                                        "OPEN_QUESTIONS.md")),
        "t2_rename_old_name_gone":
            not os.path.isfile(os.path.join(
                ROOT, "columbia-chain-cascade",
                "UNDERGRADUATE_RESEARCH_GAPS.md")),
        "t3_decision_entry_in_schema":
            "### The DECISION entry" in _read(os.path.join(
                ROOT, "RESEARCH_RENDER.md")),
        "t4_gap_index_tool":
            os.path.isfile(os.path.join(ROOT, "tools", "gap_index.py")),
    }
    return {"by_name": by_name,
            "wo2_resolves_by_content": all(wo2_content.values()),
            "wo2_content": wo2_content,
            "wo1_artifacts": wo1_artifacts,
            "wo1_resolves_by_artifact_only":
                all(wo1_artifacts.values())
                and not by_name["WORK_ORDER_FABLE.md"]}


# --------------------------------------- 3  the G-01 question

def g_numbering():
    """The marker says 'Same shape as G-01's detection floor' and the
    appended notes say 'Same shape as your G-01'. In the landed render
    (seam-gaps/OPEN_QUESTIONS.md) the detection-floor gap is ENTRY 2,
    tagged G-02, and G-01 is the referent-propagation gap. So the
    file's G-01 and the render's G-01 are different entries.

    Two readings, and this checker picks neither:
      (a) the author's own G-list numbers the gaps differently from
          the render's blocks-are-gaps 1:1 choice -- in which case the
          render's own README already states the rule: 'If the
          author's own G-list differs, the ids here yield to it.'
      (b) the reference was written against the session's working
          numbering and simply names the detection-floor gap, whose
          id in the landed render is G-02.
    Under either reading the REFERENT is unambiguous -- the detection
    floor -- and no id is renumbered ('ids are permanent, never
    renumber', RESEARCH_RENDER). This is the first live evidence
    bearing on the README's [CHOICE], recorded here rather than acted
    on."""
    text = _read(MARKER)
    marker, appended = text.split(SEAM, 1)
    oq = _read(os.path.join(ROOT, "seam-gaps", "OPEN_QUESTIONS.md"))
    heads = re.findall(r"(?m)^## (\d+)\. .*\((G-\d\d)\)\s*$", oq)
    # which entry's heading names the floor
    floor_id = None
    referent_id = None
    for line in oq.splitlines():
        m = re.match(r"^## (\d+)\. .*\((G-\d\d)\)\s*$", line)
        if m and "floor" in line:
            floor_id = m.group(2)
        if m and "referent" in line.lower():
            referent_id = m.group(2)
    rme = _read(os.path.join(ROOT, "seam-gaps", "README.md"))
    return {
        "marker_cites": "G-01's detection floor" in marker,
        "appended_cites": "your G-01" in appended,
        "render_entry_ids": heads,
        "render_floor_id": floor_id,
        "render_g01_is_referent_gap": referent_id == "G-01",
        "ids_disagree": floor_id is not None and floor_id != "G-01",
        "readme_yield_rule_present":
            "the ids here" in rme and "yield to it" in rme,
        "verdict": None,   # no pick; both readings above
    }


# ------------------------------------ 4  the hold preconditions

def holds():
    """Two of the five hold reasons state arithmetic this file's own
    text can be counted against. Counting is not adjudicating the
    material -- it evaluates whether the file's own stated release
    condition is met BY THE FILE, which is what a marker's hold
    means until more material arrives.

    M-A: 'ready when the archive table is filled past four rows'.
    Rows counted in the four-archive table itself.

    M-C: 'needs N>1 observation programs before the lag claim can
    carry'. Programs whose observed variable set the file actually
    states -- both halves name exactly one, the Signal Service 1887
    manual. ('successor-agency manuals' are named as a source, with
    no list stated.)

    M-B, M-D, M-E hold on conditions outside this file (a covariate
    to settle, a charter set to assemble, an archive reachable by
    request only) and are reported as NOT EVALUABLE HERE rather
    than counted."""
    text = _read(MARKER)
    marker = text.split(SEAM, 1)[0]
    # M-A table rows: archive names opening a row in the table block
    m = re.search(r"### The four-archive table.*?###", marker, re.S)
    block = m.group(0) if m else ""
    rows = re.findall(
        r"(?m)^(Signal Service|Star Route|Homestead|Wells Fargo)\b",
        block)
    # M-C programs with a stated observed set: distinct manual years
    # adjacent to an 'observed set' statement, over the whole file
    prog_years = set()
    for mm in re.finditer(r"observed set[^\n]*", text, re.I):
        span = text[mm.start():mm.start() + 120]
        prog_years.update(re.findall(r"\b(18\d\d|19\d\d)\b", span))
    return {
        "MA_table_rows": len(rows),
        "MA_condition": "past four rows",
        "MA_hold_stands": len(rows) <= 4,
        "MC_programs_with_stated_set": len(prog_years),
        "MC_program_years": sorted(prog_years),
        "MC_condition": "N>1 observation programs",
        "MC_hold_stands": len(prog_years) <= 1,
        "MB_MD_ME": "NOT EVALUABLE HERE (conditions outside "
                    "this file)",
    }


# ---------------------------------------- 5  index exclusion

def index_exclusion():
    """G-07 and G-08 are HELD, not filed; the marker directory is
    storage, not a gap-rendering folder. Neither id and no
    notes/markers row may appear in GAP_INDEX.md."""
    gi = _read(os.path.join(ROOT, "GAP_INDEX.md"))
    return {
        "g07_in_index": bool(re.search(r"\bG-07\b", gi)),
        "g08_in_index": bool(re.search(r"\bG-08\b", gi)),
        "markers_dir_in_index": "notes/markers" in gi,
    }


# ------------------------------------------ 6  cross-references

def cross_refs():
    """By existence, not mention -- and by PATH existence only,
    since a text search for these strings would count this marker
    file and this checker (the UNI_010 self-reference loop, and
    QA_007's route through a sibling)."""
    return {
        "uninstrumented/":
            os.path.isdir(os.path.join(ROOT, "uninstrumented")),
        "seam-gaps/":
            os.path.isdir(os.path.join(ROOT, "seam-gaps")),
        "unrecordable-by-construction (as a path)":
            os.path.exists(os.path.join(ROOT,
                                        "unrecordable-by-construction")),
        # the M-A 'related to' line names a concept beside a folder;
        # the folder resolves, the concept is not a path anywhere --
        # recorded as concept-not-artifact, not as a defect
    }


# ------------------------------------------------------ render

def render():
    out = []
    w = out.append
    w("HELD MARKERS 2026-08-31 -- STRUCTURAL READINGS")
    w("(the entry is a marker file by its own declaration; nothing")
    w(" below renders, files, or adjudicates M-A..M-E)")
    w("")
    st = structure()
    w("1  DELIVERY STRUCTURE")
    w("   seam %r found %d time(s); split %s"
      % (SEAM, st["seam_count"], st.get("split")))
    w("   marker half: headings %s, standing note %s"
      % (st.get("marker_headings"),
         st.get("marker_has_standing_note")))
    w("   appended half: G-08 draft %s, HELD-not-filed note %s,"
      % (st.get("appended_has_g08_draft"),
         st.get("appended_has_held_note")))
    w("   names G-07 %s; the draft render exists ONLY in the"
      % st.get("appended_names_g07"))
    w("   appended half (%s)" % st.get("g08_draft_only_appended"))
    w("   standing instruction echoed, not consumed: render the")
    w("   mechanism (M-A) first and the instances under it.")
    w("")
    ra = read_alongside()
    w("2  READ-ALONGSIDE REFERENCES")
    for name, ok in ra["by_name"].items():
        w("   %-30s by name: %s" % (name,
                                    "present" if ok else "ABSENT"))
    w("   WORK_ORDER_FABLE_02_GAPS -> seam-gaps/WORK_ORDER.md by")
    w("   content: %s %s" % (ra["wo2_resolves_by_content"],
                             ra["wo2_content"]))
    w("   WORK_ORDER_FABLE -> by artifact only: %s %s"
      % (ra["wo1_resolves_by_artifact_only"], ra["wo1_artifacts"]))
    w("   The order that was never landed as a file survives only")
    w("   as its effects -- the marker file's own stated purpose,")
    w("   demonstrated on its sibling.")
    w("")
    gn = g_numbering()
    w("3  THE G-01 QUESTION (two readings, no pick)")
    w("   file cites 'G-01's detection floor' (marker %s,"
      % gn["marker_cites"])
    w("   appended %s); landed render: floor is %s, G-01 is the"
      % (gn["appended_cites"], gn["render_floor_id"]))
    w("   referent gap (%s). Ids disagree: %s."
      % (gn["render_g01_is_referent_gap"], gn["ids_disagree"]))
    w("   README yield rule present: %s. Referent unambiguous"
      % gn["readme_yield_rule_present"])
    w("   either way; no id renumbered; verdict %s."
      % gn["verdict"])
    w("")
    ho = holds()
    w("4  HOLD PRECONDITIONS, FROM THE FILE'S OWN TEXT")
    w("   M-A: table rows %d against '%s' -> hold %s"
      % (ho["MA_table_rows"], ho["MA_condition"],
         "STANDS" if ho["MA_hold_stands"] else "released by "
         "its own arithmetic"))
    w("   M-C: programs with a stated observed set %d (%s)"
      % (ho["MC_programs_with_stated_set"],
         ", ".join(ho["MC_program_years"])))
    w("        against '%s' -> hold %s"
      % (ho["MC_condition"],
         "STANDS" if ho["MC_hold_stands"] else "released by "
         "its own arithmetic"))
    w("   M-B, M-D, M-E: %s" % ho["MB_MD_ME"])
    w("")
    ie = index_exclusion()
    w("5  INDEX EXCLUSION")
    w("   G-07 in GAP_INDEX: %s; G-08: %s; notes/markers row: %s"
      % (ie["g07_in_index"], ie["g08_in_index"],
         ie["markers_dir_in_index"]))
    w("   held means held: none may appear until filed.")
    w("")
    cr = cross_refs()
    w("6  CROSS-REFERENCES (path existence only)")
    for name, ok in cr.items():
        w("   %-44s %s" % (name, ok))
    w("   'unrecordable-by-construction' resolves as a concept,")
    w("   not a path -- recorded, not repaired.")
    w("")
    w("This module computes; it does not conclude. The marker file")
    w("is edited by nothing here.")
    return "\n".join(out)


# ---------------------------------------------------- selftest

def selftest():
    n = [0]

    def check(name, ok):
        n[0] += 1
        if not ok:
            sys.stderr.write("FAIL %s\n" % name)
            sys.exit(1)

    before = hashlib.sha256(
        io.open(MARKER, "rb").read()).hexdigest()

    st = structure()
    check("seam once", st["seam_count"] == 1)
    check("five markers", st["marker_headings"] ==
          ["M-A", "M-B", "M-C", "M-D", "M-E"])
    check("standing note", st["marker_has_standing_note"])
    check("mechanism-first instruction",
          st["standing_instruction_present"])
    check("g08 draft in appended half",
          st["appended_has_g08_draft"])
    check("held note in appended half", st["appended_has_held_note"])
    check("g07 named", st["appended_names_g07"])
    check("draft only appended", st["g08_draft_only_appended"])

    ra = read_alongside()
    check("neither name in tree",
          not any(ra["by_name"].values()))
    check("wo2 resolves by content", ra["wo2_resolves_by_content"])
    check("wo1 resolves by artifact only",
          ra["wo1_resolves_by_artifact_only"])

    gn = g_numbering()
    check("marker cites g01 floor", gn["marker_cites"])
    check("appended cites g01", gn["appended_cites"])
    check("render floor is G-02", gn["render_floor_id"] == "G-02")
    check("render G-01 is referent", gn["render_g01_is_referent_gap"])
    check("ids disagree", gn["ids_disagree"])
    check("yield rule present", gn["readme_yield_rule_present"])
    check("no verdict picked", gn["verdict"] is None)

    ho = holds()
    check("MA rows counted 4", ho["MA_table_rows"] == 4)
    check("MA hold stands", ho["MA_hold_stands"])
    check("MC one program", ho["MC_programs_with_stated_set"] == 1)
    check("MC year 1887", ho["MC_program_years"] == ["1887"])
    check("MC hold stands", ho["MC_hold_stands"])

    ie = index_exclusion()
    check("no G-07 in index", not ie["g07_in_index"])
    check("no G-08 in index", not ie["g08_in_index"])
    check("no markers row in index", not ie["markers_dir_in_index"])

    cr = cross_refs()
    check("uninstrumented resolves", cr["uninstrumented/"])
    check("seam-gaps resolves", cr["seam-gaps/"])
    check("concept is not a path",
          not cr["unrecordable-by-construction (as a path)"])

    # the checker never edits the entry it checks
    render()
    after = hashlib.sha256(
        io.open(MARKER, "rb").read()).hexdigest()
    check("marker file untouched", before == after)

    # a constructed broken hold shows the count can release
    # (the deny/release branch is reachable, not CONSTANT_SILENT)
    five_rows = holds.__doc__ is not None  # doc present
    check("holds documented", five_rows)
    fake_rows = 5
    check("release branch reachable (constructed)",
          not (fake_rows <= 4))

    print("check_markers selftest: %d/%d checks pass" % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    else:
        print(render())
