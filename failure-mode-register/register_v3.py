#!/usr/bin/env python3
"""
Audit of WORK_ORDER_V3.md -- the third order, landed verbatim.

The order is delivered and is not edited. Everything here is computed
from it, from the two orders before it, or from this repository's own
instruments; nothing is retyped and nothing is a statement about any
deployed system, entity or person.

WHAT IS NEW IN THIS PASS. Three things the earlier orders did not put on
the table:

  1. Section 0-1 reports the prior-art gate RUN, with a named result.
     FMR_001 held the register as NOT CLEARED TO SHIP because Step 0 was
     blocked. The blocker is removed BY THE ORDER'S OWN REPORT, and the
     report is not verifiable from inside this environment -- the arXiv
     hosts refuse CONNECT. So the closure is by declaration, and the
     order says so itself ("Verify before citing").
  2. Section 6 is this session's own repair folded back into the order as
     a control. The audit direction inverts: instead of checking whether
     the register does what the order says, check whether the ORDER'S
     STATEMENT matches the gate the repository implements. It does not,
     by one field, and the missing field is the one that makes the gate
     work.
  3. v3 is a REWRITE, not a purely additive revision. v2 against v1 was
     694 lines inserted and 0 deleted; this one is measured in
     test_register_v3.py and is nothing like that.

The cell parsers, the gated score map, the boundary report, the F3
reader, the duration and rate rules, the reconstruction and projection
counts and the conjunction arithmetic are IMPORTED from entries_v2.py and
register_v2.py, which were generalised to take a document rather than
copied.

CC0. Stdlib only. Parses under 3.9. ASCII only.

    python3 register_v3.py            the audit
    python3 register_v3.py --choices  the open choices
"""

import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))

import entries as E1                                      # noqa: E402
import entries_v2 as E2                                   # noqa: E402
import entries_v3 as E3                                   # noqa: E402
import register as R1                                     # noqa: E402
import register_v2 as R2                                  # noqa: E402
import sourced as S                                       # noqa: E402

CHOICES = {
    12: "the prior-art gate's four artifacts are CARRIED, not verified: "
        "arxiv.org and export.arxiv.org refuse CONNECT from here and no "
        "probe runs at audit time (no network is a house rule). Recorded "
        "as NOT_VERIFIABLE_HERE rather than as agreement.",
    13: "a section-5 subsection counts as carrying a CITED INSTANCE only "
        "if it names a dated or identified case; `Worked case:` "
        "introducing a hypothetical does not count.",
    14: "the parser-gate conformance check reads section 6's own field "
        "list against tools/sourced.Sourced's constructor, and "
        "demonstrates the gap by replay rather than by argument.",
}

NOT_VERIFIABLE_HERE = "NOT_VERIFIABLE_HERE"


def choices_report():
    out = []
    for n in sorted(CHOICES):
        out.append((n, CHOICES[n]))
    for n, text in E3.render_choices():
        out.append((n, text + "  (entries_v3)"))
    return out


# ------------------------------------------------- the pair, measured

def pair_diff():
    """v3 against v2, measured rather than described. v2 against v1 was a
    pure insertion; this is not, and the claim that it is a revision of
    the same document has to survive the number."""
    a = E2.order_text().split("\n")
    b = E3.order_text().split("\n")
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ins = dele = repl = eq = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "insert":
            ins += j2 - j1
        elif tag == "delete":
            dele += i2 - i1
        elif tag == "replace":
            repl += max(i2 - i1, j2 - j1)
        else:
            eq += i2 - i1
    return {"v2_lines": len(a), "v3_lines": len(b), "equal": eq,
            "inserted": ins, "deleted": dele, "replaced": repl,
            "ratio": round(sm.ratio(), 4),
            "purely_additive": dele == 0 and repl == 0,
            "shorter": len(b) < len(a),
            "reading": ("v2 was a pure insertion over v1 and this is a "
                        "rewrite; it is also SHORTER than v2 while "
                        "carrying sections v2 does not have, so prose was "
                        "compressed rather than added to")}


def sections_added_and_dropped():
    """Top-level headings present in one order and not the other."""
    def heads(text):
        return [ln.strip() for ln in text.split("\n")
                if ln.startswith("## ")]
    h2 = heads(E2.order_text())
    h3 = heads(E3.order_text())
    return {"v2": h2, "v3": h3, "n_v2": len(h2), "n_v3": len(h3)}


# ----------------------------------------------- Step 0: the gate run

def step0_prior_art():
    """FMR_001 held the register NOT CLEARED TO SHIP because Step 0 was
    blocked. v3 reports it run. [CHOICE 12]: the report is carried."""
    rows = E3.prior_art_rows()
    result = E3.prior_art_result() or ""
    steps = dict(E3.steps())
    step0 = steps.get("Step 0", "")
    closest = [r[0] for r in rows if "CLOSEST PRIOR ART" in r[2]
               or "CLOSEST PRIOR ART" in r[1]]
    return {"step": "Step 0", "n_artifacts": len(rows),
            "artifacts": [r[0] for r in rows],
            "result": result,
            "declares_not_redundant": "not redundant" in result,
            "states_done_in_procedure": "DONE" in step0,
            "closest_prior_art": closest,
            "instructs_verify_before_citing":
                "Verify before citing" in "\n".join(
                    E3._section("### 0-1", stop_prefix=("### ", "## "))),
            "verification": NOT_VERIFIABLE_HERE,
            "verification_why": CHOICES[12],
            "blocked": False,
            "cleared_by": "the order's own report, not by a check here",
            "supersedes": "FMR_001"}


def step1_deployment_class():
    """FMR_002: Step 1 fixes the deployment class and nothing declares
    one. Recounted on v3."""
    steps = dict(E3.steps())
    txt = E3.order_text()
    declared = None
    for rec in E3.entries_v3():
        cell = rec["fields"].get("load_condition", "")
        if "In practice: all of them" in cell:
            declared = rec["id"]
    return {"step": "Step 1", "text": steps.get("Step 1", ""),
            "offers_two_classes": "Pick one" in steps.get("Step 1", ""),
            "declared_anywhere": False,
            "entry_declining_to_narrow": declared,
            "mentions": txt.count("deployment class"),
            "state": "NOT_RUN",
            "why": ("the order offers two classes and picks neither, and "
                    "one entry declines to narrow in as many words; "
                    "Step 5 and 7-2 both rest on it")}


# ----------------------------------------------------- the V-map

def amended_map():
    return {"rows": E3.amended_scores(),
            "boundary": E3.vmap_boundary_report()}


def f3_check():
    """F3 names the wins; the map computes them. FMR_027 found four
    protective variables against F3's two on v2. Recomputed on v3."""
    claim = E3.f3_claim()
    computed = E3.protective_after_amendment()
    f2 = " ".join(" ".join(
        E3._section("### 1-1", stop_prefix=("## ",))).split())
    unexplained = []
    for vid in computed:
        if vid in claim["wins"]:
            continue
        # F2 argues V9 away by name; nothing argues the others away.
        if vid + " is the usual reason" in f2:
            continue
        unexplained.append(vid)
    return {"f3_wins": claim["wins"], "f3_losses": claim["losses"],
            "f3_withdrawn_wins": claim["original_wins"],
            "original_marker": claim["original_marker"],
            "computed_protective": computed,
            "n_computed": len(computed),
            "n_claimed": len(claim["wins"]),
            "argued_away_by_name": [v for v in computed
                                    if v not in claim["wins"]
                                    and v + " is the usual reason" in f2],
            "unexplained": unexplained,
            "agrees": sorted(computed) == sorted(claim["wins"]),
            "carries_from": "FMR_027 / FMR_028, recomputed on v3"}


def v5_definition():
    """FMR_028: A-01 redefines a carrier as someone who can READ THE
    REPRESENTATION, and V5 still scores on re-performance. DUR-004 is the
    state where execution is continuous and the carrier population is
    near zero."""
    defs = dict((v[0], (v[1], v[2])) for v in E3.v_definitions())
    name, gloss = defs.get("V5", ("", ""))
    a01 = [a for a in E3.amendments() if a["id"] == "A-01"]
    rule = a01[0].get("replacement", "") if a01 else ""
    stranded = [r for r in E3.entries_v3() if r["id"] == "DUR-004"]
    return {"v5_name": name, "v5_gloss": gloss,
            "a01_rule": rule,
            "a01_defines_carrier_as_reader":
                "READ THE REPRESENTATION" in rule,
            "v5_scores_on_performance":
                "re-taught" in gloss or "re-performed" in gloss,
            "v5_amended": E3.amended_scores()["V5"]["amendment"],
            "stranded_entry": stranded[0]["title"] if stranded else None,
            "reading": ("V5 keeps a protective score on a gloss that "
                        "counts re-performance, and DUR-004 is the state "
                        "where performance is continuous and reading is "
                        "gone -- the same slip A-01 repairs one variable "
                        "over")}


# -------------------------------------------------- entries and steps

def field_coverage():
    """The order's own rule: an entry missing any schema field is an
    UNRATED PART. v3 moved `id` from the fence to the heading."""
    cov = E3.field_coverage()
    heads = dict((i, t) for i, t, _n in E3.entry_ids())
    cov["id_in_heading"] = sorted(heads)
    cov["reading"] = ("every entry block is one field short of the "
                      "schema and it is the same field on all of them; "
                      "the id moved into the `### DUR-00n` heading, so "
                      "the register's own UNRATED PART rule fires on 6 "
                      "of 6 entries against a format change rather than "
                      "an omission")
    return cov


def step5_reconstruction():
    return R2.reconstruction_distribution_v2(
        recs=E3.entries_v3(),
        axes={"DUR-001": "control state (without / with the control)",
              "DUR-003": "time (degrades from PARTIAL toward NO)"})


CONTROL_HEADS = ("NONE", "PARTIAL", "FULL")


def _control_head(cell):
    """The leading token of an existing_control cell, stripped of
    punctuation. Step 6 gates on `existing_control = NONE` and the field
    is FREE TEXT with no declared vocabulary, so the gate has to be read
    off something. A whole-word scan for NONE is the obvious rule and it
    is wrong on the one entry that scores PARTIAL deliberately, whose
    cell reads `Scored PARTIAL, not NONE` -- the word is there, in a
    sentence saying it does not apply. The head token is what the six
    delivered cells actually carry."""
    tok = cell.strip().split()[0] if cell.strip() else ""
    tok = tok.strip(".,;:")
    return tok if tok in CONTROL_HEADS else ("UNDECLARED" if not tok
                                             else "UNPARSED:" + tok)


def step6_requirements():
    """Step 6 gates on existing_control = NONE and consequence
    non-trivial. FMR_007: an entry scoring PARTIAL deliberately is gated
    out of its own requirement. FMR_008: the second conjunct has no test
    anywhere in the order."""
    rows = []
    for rec in E3.entries_v3():
        ctl = rec["fields"].get("existing_control", "")
        head = _control_head(ctl)
        rows.append({"id": rec["id"], "control": ctl[:60],
                     "head": head,
                     "gate_none": head == "NONE",
                     "word_scan_none": E2._word_in(ctl, "NONE"),
                     "declares_partial": head == "PARTIAL",
                     "proposes_control":
                         "PROPOSED" in rec["fields"].get(
                             "detection_channel", "")})
    word_scan_fp = [r["id"] for r in rows
                    if r["word_scan_none"] and not r["gate_none"]]
    return {"rows": rows,
            "heads": sorted(set(r["head"] for r in rows)),
            "field_has_a_declared_vocabulary": False,
            "gated_in": [r["id"] for r in rows if r["gate_none"]],
            "excluded": [{"id": r["id"],
                          "head": r["head"],
                          "states_requirement_anyway":
                              r["proposes_control"]}
                         for r in rows if not r["gate_none"]],
            "word_scan_false_positives": word_scan_fp,
            "second_conjunct": "consequence non-trivial",
            "second_conjunct_test": None,
            "second_conjunct_state": "NOT_EVALUABLE",
            "why": ("no scale, no threshold and no comparison for "
                    "`non-trivial` appears anywhere in the order, so the "
                    "gate runs on the first conjunct alone -- and the "
                    "first conjunct is an equality against a free-text "
                    "field, which a whole-word scan reads wrongly on the "
                    "entry that scores PARTIAL and says `not NONE`")}


def step7_null_set():
    """Step 7 asks for the NULL SET -- modes checked and found already
    controlled. Nothing in the register is one; the closest is a PARTIAL
    scored deliberately, which the entry names as the null-set
    discipline."""
    rows = []
    for rec in E3.entries_v3():
        ctl = rec["fields"].get("existing_control", "")
        rows.append({"id": rec["id"],
                     "already_controlled": E2._word_in(ctl, "FULL"),
                     "cites_null_set_discipline": "null-set" in ctl})
    return {"rows": rows,
            "n_already_controlled":
                sum(1 for r in rows if r["already_controlled"]),
            "cites_discipline": [r["id"] for r in rows
                                 if r["cites_null_set_discipline"]],
            "state": "EMPTY",
            "why": ("no entry reports a mode found already controlled; "
                    "one scores PARTIAL deliberately and names the "
                    "discipline while doing it")}


def projected_fraction():
    """F_D says state the fraction IN THE HEADER. Recount, and read the
    header."""
    rec = R2.projected_fraction_v2(recs=E3.entries_v3())
    head = E3.header_status()
    rec["header"] = head["body"]
    rec["header_states_a_fraction"] = any(
        ch.isdigit() or "%" in c for c in head["claims"] for ch in c)
    rec["header_claims"] = head["claims"]
    rec["f_d_satisfied"] = rec["header_states_a_fraction"]
    rec["why"] = ("F_D directs the fraction into the header; the header "
                  "states an entry count and a gate status and no "
                  "fraction")
    return rec


def header_entry_count():
    """The header claims six entries. Count them."""
    head = E3.header_status()
    ids = [i for i, _t, _n in E3.entry_ids()]
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
             "six": 6, "seven": 7, "eight": 8}
    stated = None
    for c in head["claims"]:
        for w, n in words.items():
            if c.strip().lower().startswith(w + " entr"):
                stated = n
    return {"stated": stated, "counted": len(ids), "ids": ids,
            "agrees": stated == len(ids)}


# ------------------------------------------------------- falsifiers

def f_k_bound():
    """F_K on v3's artifact-side set, through the SOURCED duration rule."""
    rec = R2.f_k_bound(conds=E3.artifact_side_ambient(),
                       order_name=E3.ORDER_NAME, text=E3.order_text())
    rec["prose_claims_finite_lifetimes"] = (
        "each with finite lifetime" in E3.order_text())
    return rec


def f_m_bound():
    """F_M on v3's carrier-side set."""
    return R2.f_m_bound(conds=E3.carrier_side_ambient())


def f_l_direction():
    """F_L states a direction. The direction is checkable and the
    amendment it rests on states none. FMR_029, recomputed against v3's
    own wording."""
    rec = R2.f_l_direction()
    txt = dict(E3.falsifiers_v3()).get("F_L", "")
    a07 = [a for a in E3.amendments() if a["id"] == "A-07"]
    rec["f_l_text"] = txt
    rec["f_l_states_higher"] = "HIGHER than the naive product" in txt
    rec["f_l_forbids_a_number"] = "DO NOT PUT A NUMBER ON IT" in txt
    rec["a07_replacement"] = a07[0].get("replacement", "") if a07 else ""
    rec["a07_states_a_direction"] = any(
        w in rec["a07_replacement"] for w in ("HIGHER", "higher", "lower",
                                              "LOWER"))
    rec["n_terms"] = len(E3.conjunction_terms())
    rec["carries_from"] = "FMR_029, unmoved by the rewrite"
    return rec


def f_j_scope():
    """F_J on v3's section 5. v2's F_J directed a marking at ENTRY blocks
    in a section that has none (FMR_034). v3 states the marking at
    section level and names two subsections as observable now --
    [CHOICE 13] observable is not the same as a CITED INSTANCE."""
    lines = E3._section("## 5. COMPOUNDING", stop_prefix=("## ",))
    blocks = [b for b in E1._fenced_blocks(lines)
              if b and b[0].strip().startswith("ENTRY")]
    subs = E3.compounding_subsections()
    rule = E3.compounding_projection_rule() or ""
    text = "\n".join(lines)
    cited = []
    for name, _n in subs:
        sid = name.split()[0]
        sec = E3._section("### " + sid, stop_prefix=("### ", "## "))
        body = " ".join(" ".join(sec).split())
        if any(ch.isdigit() for ch in body) and "arXiv" in body:
            cited.append(sid)
    named_observable = [s for s in ("5-1", "5-2", "5-5") if s in rule]
    return {"falsifier": "F_J", "section": "5",
            "entry_blocks": len(blocks), "n_subsections": len(subs),
            "subsections": [s for s, _n in subs],
            "rule": rule,
            "names_observable_now": named_observable,
            "cited_instances": cited, "n_cited": len(cited),
            "worked_case_is_hypothetical": "Worked case:" in text,
            "state": ("ALL_PROJECTED" if not cited else "PARTIAL"),
            "why": ("F_J lifts a subsection out of PROJECTED only when a "
                    "current instance is CITED; two are named observable "
                    "now and neither cites one, so the exemption is "
                    "named and not exercised"),
            "choice": 13}


def f_i_independence():
    """F_I: the volume argument and the correlation correction appear
    together or neither does. Enforced structurally -- there is no
    single-number accessor."""
    rec = R2.__dict__.get("volume_vs_correlation")
    txt = dict(E3.falsifiers_v3()).get("F_I", "")
    sec = " ".join(" ".join(
        E3._section("### 4-1", stop_prefix=("### ", "## "))).split())
    corr = " ".join(" ".join(
        E3._section("### 4-2", stop_prefix=("### ", "## "))).split())
    return {"falsifier": "F_I", "text": txt,
            "volume_section_names_correlation": "4-2" in sec
            or "independent" in sec,
            "correlation_section_present": bool(corr),
            "register_rule": E3.register_rule_redundancy(),
            "has_single_number_accessor": rec is None,
            "why": ("4-1 states the expected-count arithmetic and 4-2 "
                    "states why its independence assumption is false; the "
                    "REGISTER RULE turns the correction into a "
                    "requirement on any entry claiming redundancy")}


def redundancy_rule():
    """The 4-2 REGISTER RULE is effective-redundancy-audit's shared-node
    test. IMPORTED and run, not quoted -- three copies that share a
    substrate are one copy, and the sibling's own n_eff says so."""
    rule = E3.register_rule_redundancy() or ""
    shared = independent = None
    try:
        sys.path.insert(0, os.path.join(HERE, os.pardir,
                                        "effective-redundancy-audit"))
        import effective_redundancy as ERA              # noqa: E402
        ch = ERA.Channel
        case = ERA.Case
        shared = case("three copies, one platform", "ml", "failed",
                      channels=[ch("copy %d" % i, False)
                                for i in range(3)]).n_eff
        independent = case("three copies, nothing shared", "ml", "held",
                           channels=[ch("copy %d" % i, True)
                                     for i in range(3)]).n_eff
    except Exception as exc:                            # pragma: no cover
        shared = independent = "IMPORT_FAILED: %s" % exc
    return {"rule": rule,
            "states_what_copies_do_not_share": "DO NOT SHARE" in rule,
            "n_eff_three_sharing_a_substrate": shared,
            "n_eff_three_sharing_nothing": independent,
            "imported": not isinstance(shared, str),
            "sibling": "effective-redundancy-audit",
            "why": ("copies on one platform, in one format, under one "
                    "dependency stack are ONE COPY for substrate shock; "
                    "that is the sibling's n_eff, imported and run rather "
                    "than a second copy of the inequality")}


def screen_has_null():
    return R2.screen_has_null(text=E3.screen_rule())


# --------------------------------------------- section 6, the gate

GATE_FIELDS = ("value", "source_text", "locator")


def parser_gate_conformance():
    """Section 6 is this session's own repair delivered back as a control
    inside the order it repairs. So the check runs the other way: does
    the ORDER'S STATEMENT match the gate the repository implements?

    It does not, by one field. Section 6 names three -- value, source
    text, locator -- and tools/sourced refuses on a fourth, the SPAN, and
    the span is the field that makes the gate work. [CHOICE 14]."""
    fields = E3.parser_gate_fields()
    fence = "\n".join(E3.parser_gate())
    low = fence.lower()
    import inspect
    sig = list(inspect.signature(S.Sourced.__init__).parameters)
    implemented = [p for p in sig if p != "self"]
    return {"stated_fields": fields, "n_stated": len(fields),
            "implemented_fields": implemented,
            "names_span": "span" in low or "offset" in low,
            "names_derivation": "derivation" in low,
            "states_unrated": "UNRATED" in fence,
            "states_not_a_default": "not a default" in fence,
            "states_numeral_rule": "adjacent to the number" in fence,
            "states_completeness_rule": "expected count" in fence,
            "ties_to_dur_002":
                "OUT_OF_ENVELOPE" in "\n".join(
                    E3._section("## 6. THE PARSER GATE",
                                stop_prefix=("---", "## "))),
            "choice": 14}


def containment_replay():
    """The demonstration, replaying the ACTUAL defect rather than an
    imitation of it, and reading it three ways.

    The buggy path built the amended score as `_sign(cell.lstrip("-> "))`.
    lstrip takes a CHARACTER SET, so on `-> --   A-01` it removes every
    leading `-`, `>` and space -- the value's own `--` with them -- leaves
    `A-01`, finds no sign, and falls back to the ML cell's score. The
    amended score is then the UNAMENDED one, on a map whose own rule is
    that the amended score is authoritative.

    THREE READINGS, and only the third refuses both rows:

      CONTAINMENT      the value appears somewhere in the source text.
                       This is what section 6's three fields buy. Catches
                       V3 and PASSES V6, where the buggy `-` occurs in
                       the cell through the hyphen of the arrow.
      SEARCHED SPAN    find the value in the cell afterwards and record
                       where. Also passes V6, and points at offset 0 --
                       the arrow -- not at the score at offset 3. A span
                       found after the fact can name the wrong
                       occurrence.
      PRODUCED SPAN    the offsets come from the extraction. The buggy
                       path never located the value in the amendment cell
                       at all, so it has no offsets to offer, and the
                       gate refuses both rows with no_provenance.

    So the gap in section 6 is not only the missing word `span`. A span
    is only worth anything if it is PRODUCED BY THE EXTRACTION, and the
    section states neither."""
    rows = E3.amended_scores()
    out = []
    for vid in ("V3", "V6"):
        line = None
        for _n, ln in E3._vmap_lines():
            if ln.split()[0] == vid:
                line = ln
                break
        cell = line[57:]
        ml_cell = line[31:57]
        buggy = E2._sign(cell.lstrip("-> "))
        if not buggy:                       # the fallback the defect took
            buggy = E2._sign(ml_cell)
        correct = rows[vid]["amended"]
        loc = S.Locator(E3.ORDER_NAME, None, 57, None, vid + " amendment")
        searched = S.find_span(cell, buggy)
        searched_gate = (S.gate(S.Sourced(buggy, cell, loc, span=searched))
                         if searched
                         else S.Unrated("no_provenance",
                                        where=loc.describe()))
        produced = S.gate(S.Sourced(buggy, cell, loc, span=None))
        out.append({"id": vid, "cell": cell.rstrip(),
                    "buggy_value": buggy, "correct_value": correct,
                    "ml_cell": ml_cell.strip(),
                    "buggy_equals_correct": buggy == correct,
                    "containment_passes": buggy in cell,
                    "searched_span": searched,
                    "true_span": rows[vid]["amended_span"],
                    "searched_span_passes":
                        not isinstance(searched_gate, S.Unrated),
                    "produced_span_gate": produced.reason
                    if isinstance(produced, S.Unrated) else "PASSES"})
    wrong = [r for r in out if not r["buggy_equals_correct"]]
    return {"rows": out,
            "containment_catches":
                [r["id"] for r in wrong if not r["containment_passes"]],
            "containment_misses":
                [r["id"] for r in wrong if r["containment_passes"]],
            "searched_span_misses":
                [r["id"] for r in wrong if r["searched_span_passes"]],
            "produced_span_refuses":
                [r["id"] for r in out
                 if r["produced_span_gate"] != "PASSES"],
            "searched_span_points_elsewhere":
                [r["id"] for r in out
                 if r["searched_span"] and r["true_span"]
                 and r["searched_span"] != r["true_span"]],
            "why": ("containment is what section 6's three fields buy, "
                    "and on one of these two rows it passes a score "
                    "that is not the authoritative one. A span searched "
                    "for afterwards passes it too, at an offset that is "
                    "not the score's. What refuses both is a span "
                    "PRODUCED BY THE EXTRACTION, and section 6 names "
                    "neither the span nor where it has to come from")}


# --------------------------------------------------- boundaries, again

def boundary_report():
    """FMR_042 recurring, plus a second instance in the section v3 adds."""
    v = E3.vmap_boundary_report()
    p = E3.prior_art_boundary_report()
    return {"vmap": v, "prior_art": p,
            "vmap_rows_cut": sorted(set(r["id"] for r in v["cut"])),
            "n_prior_art_cut": p["n_cut"],
            "why": ("one row of the score map still runs its ML cell past "
                    "the column the amendment cell starts at, and the "
                    "prior-art table v3 adds does the same thing on one "
                    "line -- a second instance of the same shape, found "
                    "by the same check, in new material")}


# --------------------------------------------------- entry 0 and open

def entry_zero_constructibility():
    """FMR_012: ENTRY 0 is named and is not an entry. v3 delivers it as
    prose in 0-2. Does it construct under the schema?"""
    txt = E3.entry_zero()
    names = E3.schema_field_names()
    present = [n for n in names if n + " " in txt or n.upper() in txt]
    return {"section": "0-2", "words": len(txt.split()),
            "is_an_entry_block": False,
            "schema_fields_named": present,
            "n_named": len(present),
            "mechanism_is_about_the_register": True,
            "why": ("0-2 states a property of the REGISTER -- that a "
                    "failure with no detection channel cannot generate "
                    "the evidence that would force the entry -- "
                    "not a property of a deployment, so it has no "
                    "load_condition and its detection_channel is the "
                    "field itself. Not constructible under the schema, "
                    "and delivered as prose rather than forced into one"),
            "carries_from": "FMR_012"}


def still_open():
    items = E3.still_open()
    return {"n": len(items), "items": items,
            "name_a_missing_entry": [t for t, b in items
                                     if "no entry" in b.lower()]}


def amendment_record():
    rows = []
    want = ("superseded", "replacement", "consequence")
    for a in E3.amendments():
        missing = [f for f in want if f not in a]
        rows.append({"id": a["id"], "title": a["title"],
                     "has_forcing_case": "forcing_case" in a,
                     "missing": missing, "complete": not missing})
    return {"rows": rows, "n": len(rows),
            "complete": sum(1 for r in rows if r["complete"]),
            "incomplete": [r["id"] for r in rows if not r["complete"]],
            "with_forcing_case": [r["id"] for r in rows
                                  if r["has_forcing_case"]]}


# --------------------------------------------------------------- render

def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v) if v else "(none)"
    return str(v)


def _wrap(text, indent=4, width=74):
    words, line, out = str(text).split(), "", []
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
    A = L.append
    A("WORK_ORDER_V3.md -- AUDIT")
    A("=" * 62)
    A("")
    A("The order is landed verbatim and is not edited. Nothing below is a")
    A("statement about any deployed system, entity or person.")
    A("")

    A("-- 1  the pair, measured")
    d = pair_diff()
    A("   v2 lines %d   v3 lines %d   equal %d"
      % (d["v2_lines"], d["v3_lines"], d["equal"]))
    A("   inserted %d   deleted %d   replaced %d   ratio %s"
      % (d["inserted"], d["deleted"], d["replaced"], d["ratio"]))
    A("   purely additive: %s   shorter than v2: %s"
      % (_fmt(d["purely_additive"]), _fmt(d["shorter"])))
    A(_wrap(d["reading"]))
    A("")

    A("-- 2  Step 0, the prior-art gate")
    g = step0_prior_art()
    A("   artifacts %d   declares not redundant: %s   DONE in procedure: %s"
      % (g["n_artifacts"], _fmt(g["declares_not_redundant"]),
         _fmt(g["states_done_in_procedure"])))
    A("   closest prior art: %s" % _fmt(g["closest_prior_art"]))
    A("   verification: %s" % g["verification"])
    A(_wrap(g["verification_why"]))
    A("   cleared by: %s" % g["cleared_by"])
    A("")

    A("-- 3  Step 1, the deployment class")
    s1 = step1_deployment_class()
    A("   state %s   mentions %d   entry declining to narrow: %s"
      % (s1["state"], s1["mentions"], _fmt(s1["entry_declining_to_narrow"])))
    A(_wrap(s1["why"]))
    A("")

    A("-- 4  the loss-variable map")
    f = f3_check()
    A("   F3 wins %s   computed protective %s"
      % (_fmt(f["f3_wins"]), _fmt(f["computed_protective"])))
    A("   withdrawn wins %s   marker %r"
      % (_fmt(f["f3_withdrawn_wins"]), f["original_marker"]))
    A("   argued away by name: %s   unexplained: %s"
      % (_fmt(f["argued_away_by_name"]), _fmt(f["unexplained"])))
    v5 = v5_definition()
    A("   V5 gloss: %s" % v5["v5_gloss"])
    A(_wrap(v5["reading"]))
    A("")

    A("-- 5  column boundaries")
    b = boundary_report()
    A("   V-map rows cut: %s of %d"
      % (_fmt(b["vmap_rows_cut"]), b["vmap"]["n_rows"]))
    A("   prior-art lines cut: %d of %d"
      % (b["prior_art"]["n_cut"], b["prior_art"]["n_rows"]))
    for r in b["prior_art"]["cut"]:
        A("     line %d %-9s cell=%r spill=%r"
          % (r["line_no"], r["column"], r["cell"], r["spill"]))
    A(_wrap(b["why"]))
    A("")

    A("-- 6  the entry blocks")
    c = field_coverage()
    A("   schema fields %d   unrated parts %s"
      % (c["schema_n"], _fmt(c["unrated_parts"])))
    for r in c["rows"]:
        A("     %-8s fields %2d  missing %s"
          % (r["id"], r["n_fields"], _fmt(r["missing"])))
    A(_wrap(c["reading"]))
    A("")

    A("-- 7  Step 5, reconstruction")
    r5 = step5_reconstruction()
    A("   entries %d   single-valued %s   multi-valued %s   none %s"
      % (r5["n_entries"], _fmt(r5["single_valued"]),
         _fmt(r5["multi_valued"]), _fmt(r5["no_declared_value"])))
    A("   distribution over single-valued: %s"
      % _fmt(["%s %d" % (k, v) for k, v
              in sorted(r5["distribution_over_single_valued"].items())]))
    A("   merged distribution: %s" % _fmt(r5["merged_distribution"]))
    A(_wrap(r5["why_no_merge"]))
    A("")

    A("-- 8  Steps 6 and 7")
    s6 = step6_requirements()
    A("   gated in: %s" % _fmt(s6["gated_in"]))
    A("   excluded: %s"
      % _fmt(["%s head=%s (states a requirement anyway: %s)"
              % (e["id"], e["head"], _fmt(e["states_requirement_anyway"]))
              for e in s6["excluded"]]))
    A("   control heads observed: %s   declared vocabulary: %s"
      % (_fmt(s6["heads"]), _fmt(s6["field_has_a_declared_vocabulary"])))
    A("   a whole-word NONE scan would gate in as well: %s"
      % _fmt(s6["word_scan_false_positives"]))
    A("   second conjunct %r: %s"
      % (s6["second_conjunct"], s6["second_conjunct_state"]))
    A(_wrap(s6["why"]))
    s7 = step7_null_set()
    A("   null set: %s   cites the discipline: %s"
      % (s7["state"], _fmt(s7["cites_discipline"])))
    A("")

    A("-- 9  projection, and the header")
    p = projected_fraction()
    A("   entries %d   PROJECTED %s   cap %s   at cap %s"
      % (p["n_entries"], _fmt(p["projected"]), _fmt(p["cap"]),
         _fmt(p["at_cap"])))
    A("   header: %s" % p["header"])
    A("   F_D satisfied (fraction in the header): %s"
      % _fmt(p["f_d_satisfied"]))
    A(_wrap(p["why"]))
    h = header_entry_count()
    A("   header states %s entries, %d counted: %s"
      % (_fmt(h["stated"]), h["counted"], _fmt(h["agrees"])))
    A("")

    A("-- 10  F_K and F_M")
    k = f_k_bound()
    A("   F_K %s   conditions %d   with a stated lifetime %d"
      % (k["state"], k["n_conditions"], k["n_with_stated_lifetime"]))
    A("   prose claims finite lifetimes: %s   horizon has a value: %s"
      % (_fmt(k["prose_claims_finite_lifetimes"]),
         _fmt(k["retention_horizon_has_a_value"])))
    m = f_m_bound()
    A("   F_M active set %s (%d of %d)   empty: %s"
      % (_fmt(m["active_set"]), m["n_active"], m["n_conditions"],
         _fmt(m["active_set_empty"])))
    A("   names a rate in words with no value: %s"
      % _fmt([r["condition"][:40] for r in m["rows"]
              if r["names_rate_in_words"] and not r["states_a_rate_value"]]))
    sc = screen_has_null()
    A("   DUR-005-C states no null result: %s   intended: %s"
      % (_fmt(sc["states_no_null"]), _fmt(sc["states_intended"])))
    A("")

    A("-- 11  F_L, the direction")
    fl = f_l_direction()
    A("   F_L states joint failure HIGHER than the naive product: %s"
      % _fmt(fl["f_l_states_higher"]))
    A("   A-07 states a direction: %s   F_L forbids a number: %s"
      % (_fmt(fl["a07_states_a_direction"]),
         _fmt(fl["f_l_forbids_a_number"])))
    A("   failure at p=%s n=%d over rho: %s"
      % (fl["p"], fl["n"],
         _fmt(["%.4f" % r["failure"] for r in fl["rows"]])))
    A("   like-for-like verdict %s   cross-type %s (%d of %d)"
      % (fl["like_for_like_verdict"], fl["cross_type_verdict"],
         fl["cross_type_true_at"], fl["cross_type_of"]))
    A(_wrap(fl["note"]))
    A("")

    A("-- 12  F_J and F_I")
    fj = f_j_scope()
    A("   section 5: %d subsections, %d ENTRY blocks, %d cited instances"
      % (fj["n_subsections"], fj["entry_blocks"], fj["n_cited"]))
    A("   named observable now: %s   state %s"
      % (_fmt(fj["names_observable_now"]), fj["state"]))
    A(_wrap(fj["why"]))
    fi = f_i_independence()
    A("   single-number accessor for the volume argument: %s"
      % _fmt(not fi["has_single_number_accessor"]))
    rr = redundancy_rule()
    A("   4-2 REGISTER RULE states what copies do not share: %s"
      % _fmt(rr["states_what_copies_do_not_share"]))
    A("   n_eff from %s: three copies sharing a substrate -> %s, "
      "sharing nothing -> %s"
      % (rr["sibling"], _fmt(rr["n_eff_three_sharing_a_substrate"]),
         _fmt(rr["n_eff_three_sharing_nothing"])))
    A("")

    A("-- 13  section 6, the parser gate")
    pg = parser_gate_conformance()
    A("   fields the order states (%d): %s"
      % (pg["n_stated"], _fmt(pg["stated_fields"])))
    A("   fields the gate takes: %s" % _fmt(pg["implemented_fields"]))
    A("   order names a span or offset: %s   names a derivation: %s"
      % (_fmt(pg["names_span"]), _fmt(pg["names_derivation"])))
    A("   states UNRATED: %s   not a default: %s   numeral rule: %s   "
      "completeness rule: %s"
      % (_fmt(pg["states_unrated"]), _fmt(pg["states_not_a_default"]),
         _fmt(pg["states_numeral_rule"]),
         _fmt(pg["states_completeness_rule"])))
    cr = containment_replay()
    A("     %-4s %-18s %-5s %-5s %-11s %-11s %s"
      % ("row", "cell", "buggy", "true", "containment", "searched",
         "produced"))
    for r in cr["rows"]:
        A("     %-4s %-18r %-5r %-5r %-11s %-11s %s"
          % (r["id"], r["cell"], r["buggy_value"], r["correct_value"],
             "passes" if r["containment_passes"] else "refuses",
             ("passes at %s" % (r["searched_span"],))
             if r["searched_span_passes"] else "refuses",
             r["produced_span_gate"]))
    A("   containment catches %s and misses %s"
      % (_fmt(cr["containment_catches"]), _fmt(cr["containment_misses"])))
    A("   a searched span misses %s, pointing elsewhere on %s "
      "(true span %s)"
      % (_fmt(cr["searched_span_misses"]),
         _fmt(cr["searched_span_points_elsewhere"]),
         _fmt([r["true_span"] for r in cr["rows"]])))
    A("   a produced span refuses %s" % _fmt(cr["produced_span_refuses"]))
    A(_wrap(cr["why"]))
    A("")

    A("-- 14  entry 0, amendments, still open")
    e0 = entry_zero_constructibility()
    A("   0-2 words %d   constructs as an entry block: %s"
      % (e0["words"], _fmt(e0["is_an_entry_block"])))
    A(_wrap(e0["why"]))
    am = amendment_record()
    A("   amendments %d   complete %d   with a forcing case %s"
      % (am["n"], am["complete"], _fmt(am["with_forcing_case"])))
    so = still_open()
    A("   still open %d   naming a missing entry: %d"
      % (so["n"], len(so["name_a_missing_entry"])))
    for t, body in so["items"]:
        A("     %-32s %s" % (t, body[:38]))
    A("")

    A("-- 15  choices")
    for n, text in choices_report():
        A("   [CHOICE %d]" % n)
        A(_wrap(text, indent=6))
    A("")
    A("Counts are printed by the suite: python3 test_register_v3.py")
    return "\n".join(L)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "register_v3.py is an audit. The checks live in "
            "test_register_v3.py; run `python3 test_register_v3.py`.\n")
        return 2
    if "--choices" in argv:
        for n, text in choices_report():
            print("[CHOICE %d] %s" % (n, text))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
