#!/usr/bin/env python3
"""
Audit of WORK_ORDER_V4.md, the fourth order in the failure-mode-register
family. The order is landed VERBATIM and is modified by nothing here;
every disagreement goes into CLAIM_TABLE.md and into this module's
output, which is the uninstrumented/cases arrangement this repository
already uses.

Nothing here re-implements a reader. The order's structure comes from
entries_v4.py; the falsifier arithmetic (F_K's duration rule, F_M's rate
rule, F_L's survival computation, the reconstruction distribution and the
PROJECTED cap) comes from register_v2.py, imported with the functions
that take it, so the four documents cannot drift apart in the checkers
that read them.

WHAT THIS MODULE DOES NOT DO. It rates no deployed component and no
entity. No function takes an entity as an argument. Every number is a
property of the delivered text, of the order's own rules, or of this
build's arithmetic -- see FMR_069.

CC0. Stdlib only. Parses under 3.9. ASCII only.
"""

import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entries as E                                       # noqa: E402
import entries_v2 as E2                                   # noqa: E402
import entries_v3 as E3                                   # noqa: E402
import entries_v4 as E4                                   # noqa: E402
import register_v2 as R2                                  # noqa: E402
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))
import sourced as S                                       # noqa: E402

NOT_VERIFIABLE_HERE = "NOT_VERIFIABLE_HERE"

# Choices numbered on from the v3 instrument's 1..5 and entries_v4's
# 1..6, which are its own. Printed by --choices and cited inline.
CHOICES = {
    1: "the pair measured is v4 AGAINST V3, not against v1: v3 is what v4 "
       "supersedes, and the v1 pair is already measured in register_v2.",
    2: "F_N's rating vector is computed on BOTH documents with the SAME "
       "rule, so a difference is a property of the format change and not "
       "of two readers.",
    3: "a field present in an entry and absent from the schema is reported "
       "as UNDECLARED and does not fire the UNRATED PART rule, because "
       "that rule is about absence; the order says so and A-15 is the "
       "amendment that says so.",
    4: "section 6's fourth requirement is tested by CONSTRUCTING both "
       "spans the order distinguishes and passing each through the "
       "delivered gate, rather than by reading tools/sourced.py.",
    5: "the prior-art gate's status is read from 0-1's own STATUS block, "
       "not from the Version line and not from section 7's Step 0, so a "
       "disagreement among the three is visible.",
}


def choices_report():
    out = ["CHOICES -- register_v4.py", ""]
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    out.append("")
    out.append(E4.render_choices())
    return "\n".join(out)


# ------------------------------------------------ the pair, measured

def pair_diff():
    """[CHOICE 1] v4 against v3, by opcode. v2 against v1 was a pure
    insertion; v3 against v2 was a rewrite; this says which v4 is
    rather than asserting either."""
    a = E3.order_text().split("\n")
    b = E4.order_text().split("\n")
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    eq = ins = dele = rep = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            eq += i2 - i1
        elif tag == "insert":
            ins += j2 - j1
        elif tag == "delete":
            dele += i2 - i1
        else:
            rep += max(i2 - i1, j2 - j1)
    return {"v3_lines": len(a), "v4_lines": len(b), "equal": eq,
            "inserted": ins, "deleted": dele, "replaced": rep,
            "ratio": round(sm.ratio(), 4),
            "pure_insertion": dele == 0 and rep == 0,
            "kind": ("PURE_INSERTION" if (dele == 0 and rep == 0)
                     else "REWRITE" if sm.ratio() < 0.85 else "REVISION"),
            "choice": 1}


# ------------------------------------------- FMR_045  the gate reopens

def step0_prior_art():
    """[CHOICE 5] v3 reported the gate DONE and removed the ship blocker.
    v4 reports it RUN with the report NOT_VERIFIABLE_HERE and puts the
    blocker back. FMR_045 recorded the v3 state; this records the
    reversal, which is a fact about the order rather than a repair of
    it."""
    st = E4.prior_art_status()
    rows = E4.prior_art_rows()
    v3st = E3.prior_art_result()
    ver = E4.version_line()
    steps = dict((n, v) for n, v, _k in E4.steps())
    unverified = [r for r in rows
                  if "UNVERIFIED" in " ".join(r.get(k, "")
                                              for k in ("ID",))]
    return {"status": st.get("STATUS"),
            "report_status": st.get("REPORT STATUS"),
            "ship_blocker": st.get("SHIP BLOCKER"),
            "n_artifacts": len(rows),
            "n_unverified_ids": len(unverified),
            "closest_prior_art": [r["ARTIFACT"] for r in rows
                                  if "CLOSEST PRIOR ART" in r.get("STATUS", "")],
            "version_line_says_blocked": "SHIP BLOCKED" in ver,
            "step0_line": steps.get("Step 0"),
            "three_statements_agree": (
                st.get("STATUS") == "RUN"
                and "SHIP BLOCKED" in ver
                and "FMR_001 OPEN" in (steps.get("Step 0") or "")),
            "v3_gate_result": v3st,
            "reversal": ("v3 reported the gate DONE; v4 reports it RUN "
                         "with the report NOT_VERIFIABLE_HERE and "
                         "reinstates the ship blocker"),
            "fmr_001": "OPEN",
            "choice": 5}


def reversal_has_no_amendment():
    """The amendment record's own rule is that a superseded statement is
    retained and silent overwrite is not permitted. A gate status moving
    DONE -> RUN is a superseded statement. No amendment carries it, and
    the SHIP BLOCKER line's own cross-reference points at A-12, which is
    about the id field."""
    am = E4.amendments()
    st = E4.prior_art_status()
    blocker = st.get("SHIP BLOCKER", "")
    cited = [a for a in sorted(am) if a in blocker]
    about_gate = []
    for aid, rec in sorted(am.items()):
        txt = (rec.get("text") or "") + " " + " ".join(
            (rec.get("fields") or {}).values()) + " " + (rec.get("title") or "")
        low = txt.lower()
        if "prior art" in low or "prior-art" in low:
            about_gate.append(aid)
    a12 = am.get("A-12", {})
    return {"blocker_cites": cited,
            "n_amendments": len(am),
            "amendments_about_the_gate": about_gate,
            "a12_title": a12.get("title"),
            "a12_is_about_the_gate": "PRIOR" in (a12.get("title") or ""),
            "rule": ("Each entry retains the superseded statement. "
                     "Silent overwrite is not permitted."),
            "finding": ("the DONE -> RUN reversal is recorded in 0-1 and "
                        "in D-01 and in no amendment, and the one "
                        "cross-reference the blocker gives resolves to "
                        "the id-field amendment")}


# ------------------------------------------- FMR_046  F3 and V5

def f3_check():
    """A-14 restated F3 against the table. This recounts the table and
    compares, so the restatement is checked rather than accepted."""
    prot = E4.protective_after_amendment()
    block = E4.f3_claim()
    f = block["fields"]

    def _vars(cell):
        out = []
        for tok in cell.replace(",", " ").split():
            t = tok.strip()
            if t.startswith("V") and t[1:].isdigit():
                out.append(t)
        return out

    stated_prot = _vars(f.get("PROT after amendment", ""))
    disposed = _vars(f.get("disposed by F2", ""))
    claimed = _vars(f.get("claimed as wins by F3", ""))
    undisposed = _vars(f.get("UNDISPOSED", ""))
    computed_undisposed = [v for v in prot
                           if v not in disposed and v not in claimed]
    return {"protective_after_amendment": prot,
            "n_protective": len(prot),
            "stated_protective": stated_prot,
            "stated_matches_table": stated_prot == prot,
            "disposed_by_f2": disposed,
            "claimed_wins": claimed,
            "stated_undisposed": undisposed,
            "computed_undisposed": computed_undisposed,
            "undisposed_matches": undisposed == computed_undisposed,
            "v5_undisposed": "V5" in computed_undisposed,
            "routes_to": "D-04" in f.get("UNDISPOSED", ""),
            "a14_applied": ("A-14" in E4.amendments()
                            and "RESTATED" in " ".join(
                                E4._section("### 1-1",
                                            stop_prefix=("## ",))[:12])),
            "reading": ("FMR_046 recorded F3 naming two wins over a table "
                        "showing four. v4 restates it as four with one "
                        "disposed and one undisposed, and the restatement "
                        "reproduces from the table. What does not move is "
                        "V5 itself: still PROT, still unargued, D-04 open")}


def f3_block_carries_an_arrow():
    """A-13's rule is that no hyphen, arrow or punctuation glyph appears
    in any score or status cell. The F3 restatement block's own UNDISPOSED
    cell reads `V5 -> D-04`, one section after section 1 applies the rule.

    The document-wide scan does not reach it, and the reason is stated
    rather than repaired: a two-column fixed-width block and a gutter
    block are the same shape (entries_v4 [CHOICE 5]), and this is a
    gutter block. So the finding is reported here by name, and the scan's
    blind spot is reported with it."""
    f = E4.f3_claim()["fields"]
    cells = {}
    for name, val in f.items():
        bad = [g for g in E4.FORBIDDEN_IN_SCORE_CELL if g in val]
        if bad:
            cells[name] = {"cell": val, "glyphs": bad}
    scan = E4.format_rule_scan()
    reached = any(g["line_no"] in
                  range(139, 175) for g in scan["glyphs"])
    return {"cells_with_glyphs": cells, "n": len(cells),
            "reached_by_document_scan": reached,
            "why_not": ("the F3 block has two columns, and a two-column "
                        "fixed-width block is indistinguishable from a "
                        "gutter block; entries_v4 [CHOICE 5] states the "
                        "cost and this is the instance of it")}


# ------------------------------- FMR_047 / D-06  the mechanical check

def format_rule_check():
    """D-06 asks for a mechanical check in the harness rather than a rule
    in the text. This is that check, RUN on all three documents that
    carry the rule or its defect -- a check never shown firing is not
    known to discriminate."""
    out = {}
    for label, mod in (("v2", E2), ("v3", E3), ("v4", E4)):
        doc = mod.order_text().split("\n")
        out[label] = E4.format_rule_scan(doc, mod.ORDER_NAME)
    v3cuts = out["v3"]["cuts"]
    return {"by_version": out,
            "v4_cuts": out["v4"]["n_cuts"],
            "v3_cuts": out["v3"]["n_cuts"],
            "repair_holds": out["v4"]["n_cuts"] == 0
            and out["v3"]["n_cuts"] > 0,
            "v3_cut_lines": sorted(set(c["line_no"] for c in v3cuts)),
            "v3_cut_columns": sorted(set(c["column"] for c in v3cuts)),
            "residual_all_versions": sorted(set(
                (g["column"], g["cell"]) for g in out["v4"]["glyphs"])),
            "glyph_in_every_version": (out["v2"]["n_glyphs"] > 0
                                       and out["v3"]["n_glyphs"] > 0
                                       and out["v4"]["n_glyphs"] > 0),
            "reading": ("the cut D-06 records reproduces at v3's "
                        "prior-art table and is gone at v4, so the "
                        "change holds; the glyph class in section 5-1 is "
                        "present in v2, v3 and v4 alike, which is D-06's "
                        "own finding measured: a prose rule does not "
                        "propagate to a table nobody pointed a check at")}


# ------------------------------------- FMR_048 / F_N  rating vector

def _rating_vector(recs, names, optional):
    required = [f for f in names if f not in optional]
    return [(r["id"] if "id" in r["fields"] else r.get("id"),
             "UNRATED_PART" if [f for f in required
                                if f not in r["fields"]] else "RATED")
            for r in recs]


def f_n_rating_vector():
    """F_N: a format change that alters no content must not change any
    entry's rating. [CHOICE 2] both vectors are computed with the SAME
    rule over each document's own schema, so a difference is a property
    of the format and not of two readers."""
    v3_names = E3.schema_field_names()
    v4_names = E4.schema_field_names()
    v4_opt = E4.declared_optional_fields()
    v3_vec = _rating_vector(E3.entries_v3(), v3_names, ())
    v4_vec = _rating_vector(E4.entries_v4(), v4_names, v4_opt)
    v3_un = [i for i, s in v3_vec if s == "UNRATED_PART"]
    v4_un = [i for i, s in v4_vec if s == "UNRATED_PART"]
    return {"v3_vector": v3_vec, "v4_vector": v4_vec,
            "v3_unrated": v3_un, "v4_unrated": v4_un,
            "v3_n_unrated": len(v3_un), "v4_n_unrated": len(v4_un),
            "v3_schema_n": len(v3_names), "v4_schema_n": len(v4_names),
            "v4_optional": list(v4_opt),
            "id_in_field_block": all(r["id_in_field_block"]
                                     for r in E4.entries_v4()),
            "id_matches_heading": all(r["id_matches_heading"]
                                      for r in E4.entries_v4()),
            "f_n_states_6_of_6": any("6 of 6" in t for i, t
                                     in E4.falsifiers_v4() if i == "F_N"),
            "repaired": len(v3_un) == 6 and len(v4_un) == 0,
            "choice": 2}


# ------------------------------- FMR_013  note declared, name is not

def undeclared_fields():
    """[CHOICE 3] A-15 declares `note` optional, which closes FMR_013 as
    recorded. What it does not close is the class: `name` is carried by
    every entry and appears in no schema, so the defect A-15 repairs is
    present one field over in the revision that repairs it."""
    names = E4.schema_field_names()
    opt = E4.declared_optional_fields()
    recs = E4.entries_v4()
    used = {}
    for rec in recs:
        for f in rec["order"]:
            used.setdefault(f, []).append(rec["id"])
    undeclared = dict((f, ids) for f, ids in used.items()
                      if f not in names and f not in opt)
    optional_use = dict((f, used.get(f, [])) for f in opt)
    return {"schema": names, "declared_optional": list(opt),
            "undeclared_in_use": undeclared,
            "n_undeclared": len(undeclared),
            "undeclared_universal": sorted(
                f for f, ids in undeclared.items()
                if len(ids) == len(recs)),
            "optional_use": optional_use,
            "n_entries": len(recs),
            "fires_unrated_rule": False,
            "a15_title": E4.amendments().get("A-15", {}).get("title"),
            "reading": ("A-15 records a field used and not declared, then "
                        "silently removed. `name` is used by 6 of 6 and "
                        "declared nowhere. Same shape, one field over, "
                        "in the revision that names it"),
            "choice": 3}


# ------------------------------- FMR_049  section 6's fourth requirement

def gate_fourth_requirement():
    """[CHOICE 4] Section 6-2 adds a fourth requirement: the span must be
    EMITTED BY THE EXTRACTION, carrying the offset the extractor read
    from, and a locator computed by a later search FAILS the gate.

    Tested by constructing both spans on a real cell and passing each
    through the delivered gate, rather than by reading tools/sourced.py.
    The cell is v3's V6 amendment cell, which is the row the defect was
    found on."""
    fields = E4.parser_gate_fields()
    cell = None
    line_no = None
    for n, line in E3._vmap_lines():
        if line.split()[0] == "V6":
            cell, line_no = line[57:], n
            break
    loc = S.Locator(E3.ORDER_NAME, line_no, 57, None, "V6 amendment")
    searched = S.find_span(cell, "-")
    post_hoc = S.gate(S.Sourced("-", cell, loc, span=searched))
    read_at = cell.index("--")
    emitted = S.gate(S.slice_sourced(cell, read_at, read_at + 2, loc))
    return {"three_fields": fields["three"],
            "buys": fields["buys"],
            "fourth_requirement_stated": fields["fourth_requirement_stated"],
            "discriminator": fields["discriminator"],
            "cell": cell, "line_no": line_no,
            "searched_span": searched,
            "post_hoc_passes_gate": isinstance(post_hoc, S.Sourced),
            "post_hoc_offset": (post_hoc.span[0]
                                if isinstance(post_hoc, S.Sourced) else None),
            "emitted_span": (emitted.span
                             if isinstance(emitted, S.Sourced) else None),
            "emitted_offset": read_at,
            "offsets_differ": searched is not None and searched[0] != read_at,
            "gate_separates_them": False,
            "tool_ships_both": hasattr(S, "find_span") and hasattr(
                S, "slice_sourced"),
            "reading": ("the order's stated failure signature -- locator "
                        "at offset 0 while the value sits at offset 3 -- "
                        "reproduces exactly on the row it was found on. "
                        "The gate passes the post-hoc span, because the "
                        "gate sees fields and provenance is a property of "
                        "the CONSTRUCTOR. tools/sourced.py already ships "
                        "both constructors; what it does not do is refuse "
                        "the searched one, and no check of the three "
                        "fields can"),
            "choice": 4}


# ------------------------------------------- FMR_053  F_L, no sign

def f_l_no_sign():
    """A-17: F_L now prohibits a SIGN as well as a number. The
    computation that refuted the asserted sign is register_v2's, imported
    rather than restated, and run again so the prohibition is checked
    against what it is a prohibition about."""
    comp = R2.f_l_direction()
    txt = dict(E4.falsifiers_v4()).get("F_L", "")
    flat = " ".join(txt.split())
    a17 = E4.amendments().get("A-17", {})
    return {"survival_by_rho": comp.get("rows"),
            "joint_failure_non_increasing": comp.get(
                "survival_non_decreasing", comp.get("non_decreasing")),
            "v4_states_no_direction": "NO DIRECTION IS STATED HERE" in txt,
            "v4_prohibits_a_sign": "DO NOT PUT A SIGN ON IT" in flat,
            "v4_prohibits_a_number": "DO NOT PUT A NUMBER ON IT" in flat,
            "v4_still_asserts_higher": "HIGHER" in flat
            and "v3 asserted" not in flat,
            "a17_present": bool(a17),
            "a17_found_by": (a17.get("fields") or {}).get("found by"),
            "conclusion_unchanged": "inability to ensure each term" in flat,
            "reading": ("FMR_053 recorded F_L stating a direction "
                        "survival computation does not support. v4 "
                        "removes the direction, retains the superseded "
                        "statement, and widens the prohibition from a "
                        "number to a number and a sign. The conclusion is "
                        "where it always was: on the inability to ensure "
                        "each term")}


# ------------------------- FMR_054  the active ambient set is empty

def ambient_sets():
    """F_K and F_M applied to v4's own candidate sets, through
    register_v2's bounds. v4 states the result in its header; this
    recomputes it."""
    art = E4.artifact_side_table()
    car = E4.carrier_side_table()
    fk = R2.f_k_bound(conds=[r["candidate"] for r in art["rows"]],
                      order_name=E4.ORDER_NAME, text=E4.order_text())
    fm = R2.f_m_bound(conds=[r["candidate"] for r in car["rows"]])
    hdr = E4.header_block()["fields"]
    stated_empty = "EMPTY" in hdr.get("ACTIVE AMBIENT SET", "")
    lifetimes = [r["expected_lifetime"] for r in art["rows"]]
    rates = [r["rate"] for r in car["rows"]]
    mechs = [r["producing_mech"] for r in car["rows"]]
    return {"artifact_n": art["n"], "carrier_n": car["n"],
            "artifact_lifetime_column": sorted(set(lifetimes)),
            "carrier_rate_column": sorted(set(rates)),
            "carrier_mech_column": sorted(set(mechs)),
            "f_k_admitted": fk["n_with_stated_lifetime"],
            "f_k_state": fk["state"],
            "f_m_admitted": fm["n_active"],
            "f_m_active_set_empty": fm["active_set_empty"],
            "active_set_empty": (fk["n_with_stated_lifetime"] == 0
                                 and fm["n_active"] == 0),
            "header_states_empty": stated_empty,
            "header_line": hdr.get("ACTIVE AMBIENT SET"),
            "screen": R2.screen_has_null(text=E4.screen_rule()),
            "reading": ("A-16 records the candidate sets having been "
                        "presented as if admitted. v4 marks both EXCLUDED "
                        "with the empty columns visible and states the "
                        "empty set in the header. The recount agrees: "
                        "0 of 7 lifetimes, 0 of 5 rates, and the "
                        "falsifiers and the set they empty are still "
                        "delivered in one document")}


# --------------------------------- FMR_051  the header, and F_D

def header_check():
    """F_D requires the PROJECTED fraction in the header. v3 put it in a
    Status line; v4 puts it in a fenced block with the ambient-set state
    beside it."""
    hdr = E4.header_block()
    f = hdr["fields"]
    frac = R2.projected_fraction_v2(recs=E4.entries_v4())
    return {"fields": hdr["order"],
            "projected_fraction_line": f.get("PROJECTED FRACTION"),
            "states_projected": bool(f.get("PROJECTED FRACTION")),
            "cites_f_d": "F_D" in (f.get("PROJECTED FRACTION") or ""),
            "ambient_line": f.get("ACTIVE AMBIENT SET"),
            "recount": frac,
            "reading": ("the header states the fraction as a SCOPE -- "
                        "section 5 in full plus the DUR-005 candidate "
                        "sets -- rather than as a count over entries. "
                        "F_D asks for it in the header and it is there; "
                        "the entry-level recount is reported beside it "
                        "and the two are not the same quantity")}


# ---------------------------------------- carried checks from v3

def step5_reconstruction():
    return R2.reconstruction_distribution_v2(recs=E4.entries_v4())


def step6_requirements():
    """Step 6 gates on existing_control NONE and consequence non-trivial.
    The second conjunct has no test anywhere in the order -- no scale, no
    threshold, no comparison -- so it is reported NOT_EVALUABLE per entry
    rather than silently dropped."""
    rows = []
    for rec in E4.entries_v4():
        cell = rec["fields"].get("existing_control", "")
        head = cell.split(".")[0].strip().upper()
        is_none = head.startswith("NONE")
        rows.append({"id": rec["id"], "existing_control_head": head[:24],
                     "control_is_none": is_none,
                     "consequence_non_trivial": "NOT_EVALUABLE"})
    return {"rows": rows,
            "gated_in": [r["id"] for r in rows if r["control_is_none"]],
            "second_conjunct": "NOT_EVALUABLE",
            "why": ("`consequence non-trivial` has no scale, threshold or "
                    "comparison stated anywhere in the order, so the gate "
                    "runs on the first conjunct alone")}


def step7_null_set():
    """Step 7 asks for the modes checked and found already controlled."""
    rows = []
    for rec in E4.entries_v4():
        cell = rec["fields"].get("existing_control", "")
        head = cell.split(".")[0].strip().upper()
        rows.append({"id": rec["id"], "head": head[:24]})
    null_set = [r["id"] for r in rows if r["head"].startswith("FULL")]
    partial = [r["id"] for r in rows if r["head"].startswith("PARTIAL")]
    return {"rows": rows, "null_set": null_set, "n_null": len(null_set),
            "partial": partial,
            "reading": ("the null set is empty and one entry is PARTIAL, "
                        "which DUR-002's own cell says is scored PARTIAL "
                        "rather than NONE under this discipline")}


def undeclared_token_check():
    """V14's ML AMENDED cell reads SPLIT, a fourth token against a legend
    declaring three. Not a defect on its own -- A-03 splits V14 into
    V14a/b/c -- but the legend does not carry it, so a reader taking the
    legend as the vocabulary finds a value outside it."""
    u = E4.undeclared_score_tokens()
    a03 = E4.amendments().get("A-03", {})
    return dict(u, a03_text=a03.get("text") or a03.get("title"),
                split_is_amended=any(r["id"] == "V14" for r in u["rows"]),
                reading=("the legend declares three tokens and the table "
                         "uses four; the fourth is A-03's split, recorded "
                         "in the amendment record and not in the legend"))


def still_open():
    return E4.still_open()


def falsifier_inventory():
    """Which falsifiers v4 carries, which are new against v3, and what
    state each is in where this build can compute one."""
    v3 = dict(E3.falsifiers_v3())
    v4 = dict(E4.falsifiers_v4())
    added = sorted(set(v4) - set(v3))
    dropped = sorted(set(v3) - set(v4))
    changed = sorted(k for k in set(v3) & set(v4)
                     if " ".join(v3[k].split()) != " ".join(v4[k].split()))
    return {"v3_n": len(v3), "v4_n": len(v4), "added": added,
            "dropped": dropped, "changed": changed,
            "order": [k for k, _t in E4.falsifiers_v4()]}


# ------------------------------------------------------------- render

def _fmt(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if v is None:
        return "--"
    return str(v)


def _wrap(text, indent=4, width=74):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width - indent:
            out.append(" " * indent + line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(" " * indent + line)
    return "\n".join(out)


def render():
    L = []
    a = L.append
    a("WORK ORDER V4 -- AUDIT")
    a("=" * 70)
    a("")
    a(_wrap("The order is landed verbatim and modified by nothing here. "
            "Every disagreement is recorded rather than smoothed. No "
            "deployed component and no entity is rated anywhere in this "
            "module.", 0))
    a("")

    d = pair_diff()
    a("1. IS V4 A REVISION OR A REWRITE  [CHOICE 1]")
    a("   v3 %d lines, v4 %d lines, equal %d, ratio %s"
      % (d["v3_lines"], d["v4_lines"], d["equal"], d["ratio"]))
    a("   inserted %d, deleted %d, replaced %d  -> %s"
      % (d["inserted"], d["deleted"], d["replaced"], d["kind"]))
    a(_wrap("v2 against v1 was a pure insertion. v3 against v2 was a "
            "rewrite. This is a rewrite too, and shorter in no dimension: "
            "v4 is the longest of the four."))
    a("")

    p = step0_prior_art()
    a("2. THE PRIOR-ART GATE REOPENS  [CHOICE 5]")
    a("   0-1 STATUS          %s" % p["status"])
    a("   REPORT STATUS       %s" % p["report_status"])
    a("   version line        %s" % ("SHIP BLOCKED"
                                     if p["version_line_says_blocked"]
                                     else "no blocker stated"))
    a("   step 0              %s" % (p["step0_line"] or "--")[:52])
    a("   three agree         %s" % _fmt(p["three_statements_agree"]))
    a("   artifacts           %d, unverified ids %d"
      % (p["n_artifacts"], p["n_unverified_ids"]))
    a(_wrap("v3 reported this gate DONE and removed the ship blocker. v4 "
            "reports it RUN with the report unverifiable and puts the "
            "blocker back, so FMR_001 is OPEN again by the order's own "
            "declaration. arXiv still refuses CONNECT from here; "
            "github.com is the control, so the refusal is arXiv-specific "
            "and not general egress failure."))
    r = reversal_has_no_amendment()
    a("")
    a("   the reversal is not in the amendment record")
    a("     amendments                %d" % r["n_amendments"])
    a("     amendments about the gate %s"
      % (", ".join(r["amendments_about_the_gate"]) or "none"))
    a("     the blocker cites         %s"
      % (", ".join(r["blocker_cites"]) or "none"))
    a("     which is about            %s" % (r["a12_title"] or "--"))
    a(_wrap("Section 10's own rule is that a superseded statement is "
            "retained and silent overwrite is not permitted. A gate "
            "status moving DONE to RUN is a superseded statement. It is "
            "recorded in 0-1 and in D-01, in no amendment, and the one "
            "cross-reference the blocker gives resolves to the id-field "
            "amendment."))
    a("")

    f = f3_check()
    a("3. F3 RESTATED, AND V5 STILL UNDISPOSED")
    a("   protective after amendment, recounted  %s"
      % ", ".join(f["protective_after_amendment"]))
    a("   the order states                       %s"
      % ", ".join(f["stated_protective"]))
    a("   agree                                  %s"
      % _fmt(f["stated_matches_table"]))
    a("   disposed by F2 %s   claimed by F3 %s   undisposed %s"
      % (", ".join(f["disposed_by_f2"]), ", ".join(f["claimed_wins"]),
         ", ".join(f["stated_undisposed"])))
    a("   recomputed undisposed                  %s"
      % ", ".join(f["computed_undisposed"]))
    a(_wrap("FMR_046 recorded F3 claiming two wins over a table showing "
            "four, with V5 argued away by nothing. v4 restates F3 as "
            "four, disposes one, claims two, and routes V5 to D-04. The "
            "restatement reproduces from the table. What did not move is "
            "V5 itself."))
    g = f3_block_carries_an_arrow()
    if g["n"]:
        a("")
        a("   and the block restating it carries an arrow in a status cell")
        for name, rec in sorted(g["cells_with_glyphs"].items()):
            a("     %-24s %s" % (name, rec["cell"]))
        a(_wrap("Section 1's own format rule, applied one section "
                "earlier, is that no hyphen, arrow or punctuation glyph "
                "appears in any score or status cell. " + g["why_not"] +
                "."))
    a("")

    fr = format_rule_check()
    a("4. D-06: THE MECHANICAL CHECK, RUN ON ALL THREE  [CHOICE 4]")
    a("   %-4s %-7s %-6s %-7s %s" % ("", "tables", "cuts", "glyphs",
                                     "col0 wraps"))
    for label in ("v2", "v3", "v4"):
        s = fr["by_version"][label]
        a("   %-4s %-7d %-6d %-7d %d"
          % (label, s["n_tables"], s["n_cuts"], s["n_glyphs"],
             s["n_col0_wraps"]))
    a("   the change holds             %s" % _fmt(fr["repair_holds"]))
    a("   v3 cut lines                 %s"
      % ", ".join(str(n) for n in fr["v3_cut_lines"]))
    a("   v3 cut columns               %s" % ", ".join(fr["v3_cut_columns"]))
    a(_wrap("D-06 asks for a mechanical check in the harness rather than "
            "a rule in the text. This is it, and it is document-wide "
            "because the recurrence D-06 records was in a table the "
            "V-map check did not look at. It fires on v3's prior-art "
            "table and is silent on v4's, so the change holds and the "
            "check is not silent by construction."))
    if fr["glyph_in_every_version"]:
        a("")
        a("   residual, present in v2, v3 and v4 alike:")
        for col, cell in fr["residual_all_versions"]:
            a("     %-14s %s" % (col, cell))
        a(_wrap("Section 5-1's rate table carries a hyphenated line wrap "
                "in a rate cell in every version, and three rows whose "
                "first column is filled and whose other columns are "
                "blank, which is a first-column wrap and a one-cell row "
                "written the same way. Neither was repaired, because the "
                "rule was in prose and the only check looked at the "
                "V-map. That is D-06's finding, measured."))
    a("")

    n = f_n_rating_vector()
    a("5. F_N: THE RATING VECTOR ACROSS THE REFORMAT  [CHOICE 2]")
    a("   v3 schema %d fields, unrated parts %d of %d"
      % (n["v3_schema_n"], n["v3_n_unrated"], len(n["v3_vector"])))
    a("   v4 schema %d fields plus optional %s, unrated parts %d of %d"
      % (n["v4_schema_n"], ", ".join(n["v4_optional"]) or "none",
         n["v4_n_unrated"], len(n["v4_vector"])))
    a("   id in the field block        %s" % _fmt(n["id_in_field_block"]))
    a("   id matches its heading       %s" % _fmt(n["id_matches_heading"]))
    a("   F_N states v3 failed 6 of 6  %s" % _fmt(n["f_n_states_6_of_6"]))
    a(_wrap("FMR_048 recorded every entry becoming an UNRATED PART under "
            "v3's own rule against a change that altered no content. v4 "
            "puts the id back in the field block and the vector returns "
            "to rated on all six. F_N is the falsifier added so the next "
            "reformat is checked against the vector rather than "
            "inspected."))
    a("")

    u = undeclared_fields()
    a("6. `note` IS DECLARED NOW. `name` IS NOT.  [CHOICE 3]")
    a("   declared optional            %s" % ", ".join(u["declared_optional"]))
    a("   `note` carried by            %d of %d entries"
      % (len(u["optional_use"].get("note", [])), u["n_entries"]))
    for fld, ids in sorted(u["undeclared_in_use"].items()):
        a("   UNDECLARED `%s` carried by   %d of %d entries"
          % (fld, len(ids), u["n_entries"]))
    a(_wrap("A-15 records a field used without being declared and then "
            "removed without the removal being recorded, and repairs it "
            "by declaring `note` optional. FMR_013 closes on that. The "
            "class does not: `name` is carried by every entry, appears "
            "in no schema, and is the field a reader would look up "
            "first. Same shape, one field over, in the revision that "
            "names it. It does not fire the UNRATED PART rule, which is "
            "about absence."))
    a("")

    gf = gate_fourth_requirement()
    a("7. SECTION 6'S FOURTH REQUIREMENT  [CHOICE 4]")
    for t in gf["three_fields"]:
        a("   three fields   %s" % t)
    a("   buys           %s" % gf["buys"].get("buys"))
    a("   does not buy   %s" % gf["buys"].get("does_not_buy"))
    a("   fourth stated  %s" % _fmt(gf["fourth_requirement_stated"]))
    a("")
    a("   constructed on the row it was found on:")
    a("     cell                     %r" % gf["cell"])
    a("     searched span            %s, offset %s"
      % (gf["searched_span"], gf["post_hoc_offset"]))
    a("     span emitted by the read %s, offset %s"
      % (gf["emitted_span"], gf["emitted_offset"]))
    a("     post-hoc span passes     %s" % _fmt(gf["post_hoc_passes_gate"]))
    a("     offsets differ           %s" % _fmt(gf["offsets_differ"]))
    a(_wrap("The order's stated failure signature -- a locator resolving "
            "to offset 0 while the value sits at offset 3 -- reproduces "
            "exactly, on the row it was first found on. The gate "
            "passes the searched span, and no check of the three fields "
            "can refuse it, because provenance is a property of the "
            "constructor and the gate sees fields. tools/sourced.py "
            "already ships both constructors; what it does not do is "
            "refuse the searched one."))
    a("")

    l = f_l_no_sign()
    a("8. F_L PROHIBITS A SIGN NOW")
    a("   states no direction          %s" % _fmt(l["v4_states_no_direction"]))
    a("   prohibits a number           %s" % _fmt(l["v4_prohibits_a_number"]))
    a("   prohibits a sign             %s" % _fmt(l["v4_prohibits_a_sign"]))
    a("   conclusion unchanged         %s" % _fmt(l["conclusion_unchanged"]))
    a("   A-17 found by                %s" % (l["a17_found_by"] or "--"))
    a(_wrap("FMR_053 recorded F_L stating that correlation makes joint "
            "failure HIGHER, which computing survival across rho does "
            "not support. v4 removes the direction, retains the "
            "superseded statement in A-17, and widens the prohibition "
            "from a number to a number and a sign. The conclusion rests "
            "where it always did, on the inability to ensure each term."))
    a("")

    am = ambient_sets()
    a("9. THE ACTIVE AMBIENT SET IS EMPTY")
    a("   artifact-side candidates     %d, lifetimes stated %d"
      % (am["artifact_n"], am["f_k_admitted"]))
    a("   lifetime column reads        %s"
      % ", ".join(am["artifact_lifetime_column"]))
    a("   carrier-side candidates      %d, rates stated %d"
      % (am["carrier_n"], am["f_m_admitted"]))
    a("   rate column reads            %s"
      % ", ".join(am["carrier_rate_column"]))
    a("   active set empty             %s" % _fmt(am["active_set_empty"]))
    a("   header states it             %s" % _fmt(am["header_states_empty"]))
    a(_wrap("A-16 records both candidate sets having been presented as "
            "the ambient set when neither satisfies the register's own "
            "admission rules. v4 marks them EXCLUDED with the empty "
            "columns visible and states the empty set in the header. The "
            "recount agrees. The falsifiers and the set they empty are "
            "still delivered in one document, which is what makes the "
            "reading checkable at all."))
    a("")

    h = header_check()
    a("10. THE HEADER, AND F_D")
    a("    fields                      %s" % ", ".join(h["fields"]))
    a("    projected fraction stated   %s" % _fmt(h["states_projected"]))
    a("    cites F_D                   %s" % _fmt(h["cites_f_d"]))
    a(_wrap("F_D asks for the PROJECTED fraction in the header and it is "
            "there, stated as a SCOPE rather than as a count over "
            "entries. The entry-level recount is a different quantity "
            "and is not substituted for it.", 4))
    a("")

    t = undeclared_token_check()
    a("11. A FOURTH SCORE TOKEN")
    a("    legend declares             %s" % ", ".join(t["declared"]))
    for row in t["rows"]:
        a("    %s %s reads                %s"
          % (row["id"], row["column"], row["token"]))
    a(_wrap("A-03 splits V14 and the split is in the amendment record. "
            "The legend is not amended with it, so a reader taking the "
            "legend as the vocabulary finds a value outside it. Reported "
            "rather than scored: the split is the content and the legend "
            "is the presentation.", 4))
    a("")

    fi = falsifier_inventory()
    a("12. FALSIFIERS")
    a("    v3 %d, v4 %d, added %s"
      % (fi["v3_n"], fi["v4_n"], ", ".join(fi["added"]) or "none"))
    a("    changed                     %s"
      % (", ".join(fi["changed"]) or "none"))
    a("    dropped                     %s"
      % (", ".join(fi["dropped"]) or "none"))
    a("")

    s5 = step5_reconstruction()
    a("13. STEP 5, RECOUNTED")
    a("    entries %d   single-valued %s   multi-valued %s"
      % (s5["n_entries"], ", ".join(s5["single_valued"]) or "none",
         ", ".join(s5["multi_valued"]) or "none"))
    a("    over single-valued          %s"
      % _fmt(s5.get("distribution_over_single_valued")))
    a("    no declared value           %s"
      % (", ".join(s5.get("no_declared_value") or []) or "none"))
    a("    merged distribution         %s  (%s)"
      % (_fmt(s5.get("merged_distribution")),
         (s5.get("why_no_merge") or "")[:44]))
    s6 = step6_requirements()
    a("    step 6 gated in             %s" % ", ".join(s6["gated_in"]))
    a("    step 6 second conjunct      %s" % s6["second_conjunct"])
    s7 = step7_null_set()
    a("    step 7 null set             %s"
      % (", ".join(s7["null_set"]) or "empty"))
    a("    step 7 partial              %s"
      % (", ".join(s7["partial"]) or "none"))
    a("")

    a("14. STILL OPEN, AS DELIVERED")
    for k in sorted(still_open()):
        a("    %-6s %s" % (k, still_open()[k].split(".")[0][:58]))
    a("")
    a(_wrap("FMR_069: no deployed component was inspected and no entity "
            "is rated. No function in this module takes an entity as an "
            "argument. Every number above is a property of the delivered "
            "text, of the order's own rules, or of this build's "
            "arithmetic.", 4))
    return "\n".join(L)


def main(argv):
    if "--choices" in argv:
        print(choices_report())
        return 0
    if "--selftest" in argv:
        sys.stderr.write(
            "register_v4.py is an audit. The checks live in "
            "test_register_v4.py; run `python3 test_register_v4.py`.\n")
        return 2
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
