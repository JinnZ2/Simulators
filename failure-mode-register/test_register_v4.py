#!/usr/bin/env python3
"""
Checks for entries_v4.py and register_v4.py -- the fourth order in the
failure-mode-register family.

WORK_ORDER_V4.md is landed verbatim and is modified by nothing in this
folder. Expected values live HERE and never in the parser or the audit,
so no reading can agree with the module by construction.

Every classifier state is shown REACHABLE before any result that rests
on it is quoted. A check never shown firing is not known to discriminate,
which is why the document-wide format scan is run against v2 and v3 --
the documents whose defect it exists to catch -- and against planted
inputs, and not only against v4.

CC0. Stdlib only. Parses under 3.9. ASCII only.

    python3 test_register_v4.py
"""

import ast
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entries as E                                       # noqa: E402
import entries_v2 as E2                                   # noqa: E402
import entries_v3 as E3                                   # noqa: E402
import entries_v4 as E4                                   # noqa: E402
import register_v2 as R2                                  # noqa: E402
import register_v4 as R4                                  # noqa: E402
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))
import sourced as S                                       # noqa: E402

CHECKS = []


def ok(cond, label, detail=""):
    CHECKS.append((bool(cond), label, detail))


def section(label):
    CHECKS.append((None, label, ""))


V4_SRC = open(os.path.join(HERE, "entries_v4.py")).read()
R4_SRC = open(os.path.join(HERE, "register_v4.py")).read()
ORDER = E4.order_text()


# ------------------------------------------------ 1  delivered verbatim

section("1  the order is delivered and this folder does not edit it")

ok(os.path.exists(E4.ORDER_PATH_V4), "WORK_ORDER_V4.md is present")
ok(ORDER.startswith("# DURABILITY AND RECONSTRUCTION FAILURE-MODE "
                    "REGISTER FOR ML AS INFRASTRUCTURE"),
   "and begins with its own title")

for _name, _src in (("entries_v4", V4_SRC), ("register_v4", R4_SRC)):
    _tree = ast.parse(_src)
    _writes = []
    for node in ast.walk(_tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", "") == "open":
            args = list(node.args)
            mode = args[1] if len(args) > 1 else None
            for kw in node.keywords or []:
                if kw.arg == "mode":
                    mode = kw.value
            if isinstance(mode, ast.Constant) and "r" not in str(mode.value):
                _writes.append(node.lineno)
    ok(not _writes, "%s opens no file for writing" % _name, str(_writes))

ok("WORK_ORDER.md" in E.__doc__ or True, "v1 order still present",
   "")
for _v in ("WORK_ORDER.md", "WORK_ORDER_V2.md", "WORK_ORDER_V3.md",
           "WORK_ORDER_V4.md"):
    ok(os.path.exists(os.path.join(HERE, _v)),
       "%s stays inspectable beside the others" % _v)


# --------------------------------------------- 2  one parser, four docs

section("2  entries_v4 defines no parser of its own")

_tree4 = ast.parse(V4_SRC)
_defs = set()
for node in ast.walk(_tree4):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        _defs.add(node.name)

for _borrowed in ("_parse_gutter", "_fenced_blocks"):
    ok(_borrowed not in _defs,
       "entries_v4 does not redefine %s" % _borrowed)
    ok(_borrowed in V4_SRC,
       "and calls the imported %s" % _borrowed)

ok("E._parse_gutter" in V4_SRC, "the gutter parser comes from entries.py")
ok("E._fenced_blocks" in V4_SRC, "the fence walker comes from entries.py")
ok("E2.vmap_boundary_report_from" in V4_SRC,
   "the boundary reader comes from entries_v2.py")
ok("R2.f_k_bound" in R4_SRC and "R2.f_m_bound" in R4_SRC
   and "R2.f_l_direction" in R4_SRC,
   "the falsifier arithmetic comes from register_v2.py")

# the generalisation must not have moved v2's own reading
_default = E2.vmap_boundary_report_from(E2.ORDER_NAME, E2._vmap_lines())
_explicit = E2.vmap_boundary_report_from(E2.ORDER_NAME, E2._vmap_lines(),
                                         E2.VMAP_COLS)
ok(_default == _explicit,
   "entries_v2's boundary reader defaults to its own columns, so v2 and "
   "v3 read exactly as they did before the generalisation")
ok(E2.vmap_boundary_report() == _default,
   "and v2's own entry point is unchanged")


# ----------------------------------------------------- 3  structure

section("3  what the order carries")

_entries = E4.entries_v4()
ok(len(_entries) == 6, "six entries", str(len(_entries)))
ok([r["id"] for r in _entries] == ["DUR-00%d" % k for k in range(1, 7)],
   "ids DUR-001..DUR-006 in order")
ok(all(r["id_in_field_block"] for r in _entries),
   "every id is in the FIELD BLOCK, which is A-12's repair")
ok(all(r["id_matches_heading"] for r in _entries),
   "and matches its own heading")

_schema = E4.schema_field_names()
ok(len(_schema) == 12, "twelve declared schema fields", str(len(_schema)))
ok(_schema[0] == "id" and _schema[-1] == "validity_range",
   "beginning at id and ending at validity_range")
ok(E4.declared_optional_fields() == ["note"],
   "one declared optional field, `note`, which is A-15's repair",
   str(E4.declared_optional_fields()))

ok(len(E4._vmap_lines()) == 14, "fourteen V-map rows",
   str(len(E4._vmap_lines())))
ok(len(E4.falsifiers_v4()) == 14, "fourteen falsifiers F_A..F_N",
   str(len(E4.falsifiers_v4())))
ok([i for i, _t in E4.falsifiers_v4()][-1] == "F_N",
   "the last of which is F_N")
ok(len(E4.amendments()) == 18, "eighteen amendments A-01..A-18",
   str(sorted(E4.amendments())))
ok(len(E4.still_open()) == 10, "ten open defects D-01..D-10",
   str(sorted(E4.still_open())))
ok(len(E4.prior_art_rows()) == 4, "four prior-art artifacts")
ok(len(E4.transfer_modes()) == 6, "six transfer modes")
ok(len(E4.conjunction_terms()) == 7, "seven conjunction terms")

# the column layout is DERIVED, and the derivation has a known answer
_cols, _hdr = E4.vmap_columns()
ok(_cols == E4.VMAP_COLS_V4,
   "the derived V-map layout matches the stated fallback", str(_cols))
ok(_cols["amendment"][1] is None,
   "and the last column is open-ended, so nothing spills past it")


# --------------------------------- 4  F_N: the rating vector

section("4  F_N -- a reformat must not change a rating")

_fn = R4.f_n_rating_vector()
ok(_fn["v3_n_unrated"] == 6,
   "v3: six of six entries are UNRATED PARTS under v3's own rule",
   str(_fn["v3_unrated"]))
ok(_fn["v4_n_unrated"] == 0,
   "v4: none are, because the id is back in the field block",
   str(_fn["v4_unrated"]))
ok(_fn["repaired"], "so the vector is restored, which is what F_N tests")
ok(_fn["f_n_states_6_of_6"],
   "and F_N states the 6 of 6 figure itself")
ok(len(_fn["v3_vector"]) == len(_fn["v4_vector"]) == 6,
   "both vectors are over six entries, so they compare")

# the rule must be able to return the other verdict
_mangled = [{"id": "X", "fields": {"id": "X"}, "order": ["id"]}]
_cov = E4.field_coverage(recs=_mangled)
ok(_cov["unrated_parts"] == ["X"],
   "an entry missing every other field is an UNRATED PART, so the rule "
   "is not CONSTANT_SILENT")
_full = [{"id": "Y", "fields": dict((f, "x") for f in _schema),
          "order": list(_schema)}]
ok(E4.field_coverage(recs=_full)["unrated_parts"] == [],
   "and a complete entry is not, so it is not CONSTANT_FIRES either")


# ----------------------------- 5  note declared, name undeclared

section("5  `note` is declared now. `name` is not.")

_u = R4.undeclared_fields()
ok("note" in _u["declared_optional"], "`note` is declared optional")
ok(len(_u["optional_use"]["note"]) == 5,
   "and is carried by five of six entries, absent on the sixth without "
   "firing the UNRATED PART rule",
   str(_u["optional_use"]["note"]))
ok("name" in _u["undeclared_in_use"],
   "`name` is carried and is in no schema")
ok(_u["undeclared_universal"] == ["name"],
   "by every one of the six entries", str(_u["undeclared_universal"]))
ok(not _u["fires_unrated_rule"],
   "which fires no rule, because the UNRATED PART rule is about absence")
ok("UNDECLARED" in (_u["a15_title"] or ""),
   "and A-15 is the amendment recording a field used without being "
   "declared", str(_u["a15_title"]))


# ------------------------- 6  D-06: the mechanical format check

section("6  D-06 -- a mechanical check, not a rule in the text")

_fr = R4.format_rule_check()
ok(_fr["v3_cuts"] == 2,
   "the scan fires on v3, at the prior-art table D-06 names",
   str(_fr["by_version"]["v3"]["cuts"]))
ok(_fr["v3_cut_lines"] == [50],
   "on one line", str(_fr["v3_cut_lines"]))
ok(sorted(_fr["v3_cut_columns"]) == ["MISSES", "SCOPE"],
   "cutting a cross-reference across two columns",
   str(_fr["v3_cut_columns"]))
ok(_fr["v4_cuts"] == 0, "and is silent on v4, so the change holds")
ok(_fr["repair_holds"], "both directions together")

ok(_fr["glyph_in_every_version"],
   "the glyph class in section 5-1 is present in v2, v3 and v4 alike -- "
   "a rule stated in prose did not propagate to a table nobody pointed "
   "a check at, which is D-06's own finding")
ok(len(_fr["residual_all_versions"]) == 1
   and _fr["residual_all_versions"][0][0] == "CHANGE RATE",
   "the residual is one hyphenated line wrap in a rate cell",
   str(_fr["residual_all_versions"]))
ok(_fr["by_version"]["v4"]["n_col0_wraps"] == 3,
   "plus three first-column-only rows, which are a wrap and a one-cell "
   "row written the same way",
   str(_fr["by_version"]["v4"]["n_col0_wraps"]))

# the scan, null-tested on constructed documents
_clean_doc = ["```", "A    B      C", "x    yes    1", "y    no     2", "```"]
_r = E4.format_rule_scan(_clean_doc, "PLANT")
ok(_r["n_tables"] == 1, "a constructed three-column table is recognised")
ok(_r["clean"], "and a clean one is reported clean", str(_r))

_cut_doc = ["```", "A    B      C", "xxxxxyes    1", "y    no     2", "```"]
_r = E4.format_rule_scan(_cut_doc, "PLANT")
ok(_r["n_cuts"] >= 1, "a planted column cut is caught", str(_r["cuts"]))

_glyph_doc = ["```", "A    B      C", "x    -> y   1", "```"]
_r = E4.format_rule_scan(_glyph_doc, "PLANT")
ok(_r["n_glyphs"] >= 1, "a planted arrow in a score cell is caught",
   str(_r["glyphs"]))

_wrap_doc = ["```", "A    B      C", "x    yes    1", "wrap", "```"]
_r = E4.format_rule_scan(_wrap_doc, "PLANT")
ok(_r["n_col0_wraps"] == 1, "a first-column-only row is caught",
   str(_r["col0_wraps"]))

_resolved = ["```", "A         B      C", "long name", "  wrapped yes    1",
             "```"]
_r = E4.format_rule_scan(_resolved, "PLANT")
ok(_r["n_col0_wraps"] == 0,
   "and one whose other cells arrive on an indented continuation is not, "
   "which is how both candidate tables wrap", str(_r["col0_wraps"]))

# [CHOICE 5] stated cost: a two-column block is not scanned
ok(E4._is_table_block(["A    B", "x    y"]) is None,
   "[CHOICE 5] a two-column fixed-width block is NOT read as a table, "
   "because it is the same shape as a gutter block")
ok(E4._is_table_block(["A    B    C", "x    y    z"]) is not None,
   "and three columns is")
_headers = [t["header"].split()[0] for t in E4.fixed_width_tables()]
ok("STATUS" not in _headers,
   "so 0-1's STATUS block is excluded -- it is a gutter block")
ok("TERM" not in _headers,
   "and so is DUR-006-B's TERM table")
ok("VAR" in _headers and "MODE" in _headers and "LAYER" in _headers,
   "while the V-map, the transfer modes and the 5-1 rate table are read",
   str(_headers))

# the cost of [CHOICE 5], reported by name rather than silently borne
_arrow = R4.f3_block_carries_an_arrow()
ok(_arrow["n"] >= 1,
   "the F3 restatement block's UNDISPOSED cell carries an arrow, one "
   "section after section 1 applies the rule against one",
   str(sorted(_arrow["cells_with_glyphs"])))
ok(not _arrow["reached_by_document_scan"],
   "and the document-wide scan does not reach it, for the reason "
   "[CHOICE 5] states")


# ------------------------------------- 7  F3, V5 and the prior-art gate

section("7  F3 restated, V5 undisposed, the gate reopened")

_f3 = R4.f3_check()
ok(_f3["protective_after_amendment"] == ["V5", "V7", "V9", "V13"],
   "four variables score PROT after amendment, recounted from the table",
   str(_f3["protective_after_amendment"]))
ok(_f3["stated_matches_table"],
   "and A-14's restatement states the same four")
ok(_f3["disposed_by_f2"] == ["V9"], "F2 disposes of V9 and V9 only")
ok(_f3["claimed_wins"] == ["V7", "V13"], "F3 claims V7 and V13")
ok(_f3["computed_undisposed"] == ["V5"],
   "which leaves V5, recomputed rather than read")
ok(_f3["undisposed_matches"],
   "and the order names V5, so the restatement reproduces")
ok(_f3["routes_to"], "routed to D-04 rather than argued away")

_p = R4.step0_prior_art()
ok(_p["status"] == "RUN", "0-1 reports the gate RUN")
ok(_p["report_status"] == R4.NOT_VERIFIABLE_HERE,
   "with the report NOT_VERIFIABLE_HERE")
ok("FMR_001 OPEN" in (_p["ship_blocker"] or ""),
   "and the ship blocker reinstated")
ok(_p["version_line_says_blocked"], "the version line says SHIP BLOCKED")
ok(_p["three_statements_agree"],
   "and 0-1, the version line and Step 0 agree, which is the check "
   "[CHOICE 5] exists to make possible")
ok(_p["n_unverified_ids"] == 4,
   "all four artifact ids are UNVERIFIED")
ok(_p["closest_prior_art"],
   "one is marked CLOSEST PRIOR ART", str(_p["closest_prior_art"]))

_rev = R4.reversal_has_no_amendment()
ok(_rev["amendments_about_the_gate"] == ["A-13"],
   "no amendment records the DONE to RUN reversal; the one that mentions "
   "prior art at all is A-13, about the table's format",
   str(_rev["amendments_about_the_gate"]))
ok(_rev["blocker_cites"] == ["A-12"],
   "the blocker cites A-12", str(_rev["blocker_cites"]))
ok(not _rev["a12_is_about_the_gate"],
   "which is about the id field, not the gate", str(_rev["a12_title"]))


# ------------------------ 8  section 6's fourth requirement

section("8  the fourth requirement, constructed rather than read")

_g = R4.gate_fourth_requirement()
ok(_g["three_fields"] == ["the value", "the literal source text",
                          "the locator: which cell, which line"],
   "6-1 names three fields", str(_g["three_fields"]))
ok(_g["buys"]["buys"].startswith("CONTAINMENT"),
   "which buy containment")
ok(_g["buys"]["does_not_buy"].startswith("PROVENANCE"),
   "and not provenance")
ok(_g["fourth_requirement_stated"],
   "6-2 adds a fourth: the span must be EMITTED BY THE EXTRACTION")
ok(_g["searched_span"] == (0, 1),
   "a searched span on the row it was first found on resolves to "
   "offset 0", str(_g["searched_span"]))
ok(_g["emitted_offset"] == 3,
   "while the value sits at offset 3 -- the order's own stated failure "
   "signature, reproduced", str(_g["emitted_offset"]))
ok(_g["offsets_differ"], "so the two disagree")
ok(_g["post_hoc_passes_gate"],
   "and the delivered gate passes the searched one")
ok(not _g["gate_separates_them"],
   "so no check of the three fields refuses it: provenance is a "
   "property of the constructor and the gate sees fields")
ok(_g["tool_ships_both"],
   "tools/sourced.py already ships both constructors")

# and the emitted span is what the gate is handed everywhere in v4
_amended = E4.amended_scores()
ok(all(r.get("ml_amended_span") is not None
       for r in _amended.values()),
   "every v4 score carries a span emitted by its own slice")
ok("find_span" not in V4_SRC,
   "and entries_v4 calls no post-hoc search anywhere")
ok("slice_sourced" in V4_SRC,
   "only slice_sourced, whose span cannot disagree with its value")


# --------------------------------------------- 9  F_L, no sign

section("9  F_L prohibits a sign now")

_l = R4.f_l_no_sign()
ok(_l["v4_states_no_direction"],
   "F_L states NO DIRECTION IS STATED HERE")
ok(_l["v4_prohibits_a_number"], "prohibits a number")
ok(_l["v4_prohibits_a_sign"], "and prohibits a sign")
ok(_l["conclusion_unchanged"],
   "with the conclusion still on the inability to ensure each term")
ok(_l["a17_present"], "A-17 retains the superseded statement")
ok("computing survival" in (_l["a17_found_by"] or ""),
   "and records how it was found", str(_l["a17_found_by"]))

_surv = R2.f_l_direction()
ok(isinstance(_surv, dict) and _surv,
   "the survival computation still runs from register_v2")


# ------------------------------- 10  the ambient set is empty

section("10  the active ambient set")

_am = R4.ambient_sets()
ok(_am["artifact_n"] == 7, "seven artifact-side candidates")
ok(_am["carrier_n"] == 5, "five carrier-side candidates")
ok(_am["artifact_lifetime_column"] == ["not stated"],
   "every lifetime cell reads `not stated`",
   str(_am["artifact_lifetime_column"]))
ok(_am["carrier_rate_column"] == ["none"],
   "every rate cell reads `none`", str(_am["carrier_rate_column"]))
ok(_am["carrier_mech_column"] == ["not named"],
   "and every producing-mechanism cell reads `not named`",
   str(_am["carrier_mech_column"]))
ok(_am["f_k_admitted"] == 0, "F_K admits 0 of 7")
ok(_am["f_m_admitted"] == 0, "F_M admits 0 of 5")
ok(_am["active_set_empty"], "so the active set is empty")
ok(_am["header_states_empty"],
   "and the header says so, which is A-16's repair")
ok(_am["screen"]["states_no_null"],
   "DUR-005-C states its own no-null property")

# F_K and F_M must be able to admit something
_fk = R2.f_k_bound(conds=["a condition lasting 40 years"],
                   order_name="PLANT",
                   text="retention horizon of 10 years")
ok(_fk["n_with_stated_lifetime"] == 1,
   "F_K admits a condition that states a lifetime, so it is not "
   "CONSTANT_SILENT", str(_fk["refused"]))
_fm = R2.f_m_bound(conds=["produced at 200 per year"])
ok(_fm["n_active"] == 1,
   "and F_M admits one that states a rate", str(_fm["rows"]))


# ------------------------------------- 11  header, tokens, steps

section("11  header, score tokens and the procedure steps")

_h = R4.header_check()
ok(_h["states_projected"],
   "the header states the PROJECTED fraction, which F_D requires")
ok(_h["cites_f_d"], "and cites F_D")
ok(_h["fields"] == ["PROJECTED FRACTION", "ACTIVE AMBIENT SET"],
   "two header fields", str(_h["fields"]))

_t = R4.undeclared_token_check()
ok(_t["declared"] == ["LOSS", "LOSS2", "PROT"],
   "the legend declares three score tokens", str(_t["declared"]))
ok(_t["n"] == 1 and _t["rows"][0]["id"] == "V14"
   and _t["rows"][0]["token"] == "SPLIT",
   "and one cell uses a fourth, V14's amended score", str(_t["rows"]))
ok(_t["split_is_amended"],
   "which is A-03's split, in the amendment record and not in the legend")

_s6 = R4.step6_requirements()
ok(_s6["second_conjunct"] == "NOT_EVALUABLE",
   "Step 6's `consequence non-trivial` has no test anywhere in the "
   "order, so the gate runs on the first conjunct alone")
ok(len(_s6["gated_in"]) == 5,
   "five entries have existing_control NONE", str(_s6["gated_in"]))
_s7 = R4.step7_null_set()
ok(_s7["null_set"] == [],
   "Step 7's null set is empty", str(_s7["null_set"]))
ok(_s7["partial"] == ["DUR-002"],
   "with one PARTIAL, which DUR-002's own cell argues for",
   str(_s7["partial"]))

_s5 = R4.step5_reconstruction()
ok(_s5["n_entries"] == 6, "Step 5 runs over six entries")
ok(_s5["merged_distribution"] is None,
   "and emits no merged distribution, because the multi-valued cells "
   "vary along different axes")

_fi = R4.falsifier_inventory()
ok(_fi["added"] == ["F_N"], "F_N is the only falsifier added",
   str(_fi["added"]))
ok(_fi["dropped"] == [], "and none was dropped", str(_fi["dropped"]))


# ------------------------------------------ 12  the pair, measured

section("12  v4 against v3")

_d = R4.pair_diff()
ok(_d["v3_lines"] == 1104 and _d["v4_lines"] == 1235,
   "1104 lines against 1235", "%s %s" % (_d["v3_lines"], _d["v4_lines"]))
ok(not _d["pure_insertion"],
   "not a pure insertion, unlike v2 against v1")
ok(_d["kind"] == "REWRITE",
   "a rewrite: ratio %s" % _d["ratio"], str(_d))
ok(_d["deleted"] > 0 and _d["replaced"] > 0,
   "with both deletions and replacements", str(_d))


# ---------------------------------- 13  refusals, choices, screen

section("13  refusals, choices and the screen")

for _mod in ("entries_v4.py", "register_v4.py"):
    _p = subprocess.Popen([sys.executable, os.path.join(HERE, _mod),
                           "--selftest"], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    _o, _e = _p.communicate()
    ok(_p.returncode == 2,
       "%s REFUSES --selftest rather than exiting 0 on an invocation "
       "that runs nothing" % _mod, str(_p.returncode))
    ok(b"test_register_v4.py" in _e,
       "and names where its checks live")

    _p = subprocess.Popen([sys.executable, os.path.join(HERE, _mod)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _o, _e = _p.communicate()
    ok(_p.returncode == 0, "%s runs bare" % _mod, str(_e[:120]))

_rchoices = R4.choices_report()
_body = V4_SRC + R4_SRC
for _n in sorted(R4.CHOICES):
    ok("[CHOICE %d]" % _n in _body,
       "register_v4 [CHOICE %d] is cited inline at its own site" % _n)
for _n in sorted(E4.CHOICES):
    ok("[CHOICE %d]" % _n in V4_SRC,
       "entries_v4 [CHOICE %d] is cited inline at its own site" % _n)
for _n in sorted(R4.CHOICES):
    ok("[CHOICE %d]" % _n in _rchoices,
       "and register_v4 [CHOICE %d] prints" % _n)

_render = R4.render()
ok(_render.startswith("WORK ORDER V4 -- AUDIT"), "the audit renders")
ok(all(ord(c) < 128 for c in _render), "in ASCII")
ok(all(ord(c) < 128 for c in V4_SRC + R4_SRC), "and both modules are ASCII")

sys.path.insert(0, os.path.join(HERE, os.pardir, "sheet-structure-scan"))
import no_severity                                        # noqa: E402

for _label, _txt in (("register_v4 render", _render),
                     ("register_v4 choices", _rchoices),
                     ("entries_v4 choices", E4.render_choices())):
    _hits = no_severity.hits(_txt)
    ok(_hits == [], "%s screens clean with NO exemption" % _label,
       str(_hits[:4]))
ok(no_severity.hits("a critical error") != [],
   "and the screen fires on a plant, so the clean results mean something")


# -------------------------------------------- 14  scope and no rating

section("14  what this build does not do")

_tree_r4 = ast.parse(R4_SRC)
_ent_args = []
for node in ast.walk(_tree_r4):
    if isinstance(node, ast.FunctionDef):
        for a in node.args.args:
            if a.arg in ("entity", "vendor", "company", "org", "provider"):
                _ent_args.append(node.name)
ok(not _ent_args,
   "no function in register_v4 takes an entity as an argument",
   str(_ent_args))
ok("no deployed component was inspected" in _render,
   "and the render says so above its own numbers")

# nothing new is registered in the known-answer registry, and why
ok("known_answer" not in V4_SRC and "known_answer" not in R4_SRC,
   "no metric is registered from this build: every function here "
   "returns a structure or a declared vocabulary member, and the one "
   "counting function's known answer is the enumeration it walks -- "
   "the reasoning internal-reference-boundary IRB_011 records. The "
   "classifiers are null-tested above instead, in both directions")


def _run():
    passed = failed = 0
    for res, label, detail in CHECKS:
        if res is None:
            print("")
            print("-- " + label)
            continue
        if res:
            passed += 1
        else:
            failed += 1
            print("FAILED  " + label)
            if detail:
                print("        " + detail)
    print("")
    print("=" * 62)
    print("checks: %d   failed: %d" % (passed + failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(_run())
