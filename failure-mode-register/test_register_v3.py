#!/usr/bin/env python3
"""
Checks for WORK_ORDER_V3.md, its parser and its audit.

No pytest. Run it:  python3 test_register_v3.py
The check count is printed by this file and is not stored in prose.

CC0. Stdlib only. Parses under 3.9. ASCII only.
"""

import ast
import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))

import entries as E1                                      # noqa: E402
import entries_v2 as E2                                   # noqa: E402
import entries_v3 as E3                                   # noqa: E402
import register_v2 as R2                                  # noqa: E402
import register_v3 as R3                                  # noqa: E402
import sourced as S                                       # noqa: E402

CHECKS = []


def ok(cond, label, detail=""):
    CHECKS.append((bool(cond), label, detail))


def section(name):
    CHECKS.append((None, name, ""))


V3_SRC = open(os.path.join(HERE, "entries_v3.py")).read()
R3_SRC = open(os.path.join(HERE, "register_v3.py")).read()
ORDER = E3.order_text()


# ------------------------------------------- 1  the order, as landed

section("1  the order, landed verbatim")

ok(os.path.exists(os.path.join(HERE, "WORK_ORDER_V3.md")),
   "WORK_ORDER_V3.md is landed beside WORK_ORDER.md and WORK_ORDER_V2.md, "
   "all three inspectable (the supersession convention)")
ok(all(os.path.exists(os.path.join(HERE, f)) for f in
       ("WORK_ORDER.md", "WORK_ORDER_V2.md")),
   "and neither earlier order was replaced")
_bad = sorted({c for c in ORDER if ord(c) > 127})
ok(_bad == [chr(0x2014)],
   "the only non-ASCII character in the delivered order is the em dash, "
   "the recorded exception for delivered text",
   str([hex(ord(c)) for c in _bad]))
ok(ORDER.startswith("# DURABILITY AND RECONSTRUCTION FAILURE-MODE REGISTER"),
   "the order's own title is the first line")
ok("License: CC0" in ORDER, "the order declares CC0")


# ------------------------------------------------ 2  the pair, measured

section("2  v3 against v2, measured")

d = R3.pair_diff()
ok(d["v2_lines"] == 1218 and d["v3_lines"] == 1104,
   "both orders' line counts are read from the files",
   "%d / %d" % (d["v2_lines"], d["v3_lines"]))
ok(not d["purely_additive"],
   "v3 is NOT a purely additive revision -- v2 against v1 was 694 lines "
   "inserted and 0 deleted, and this deletes and replaces",
   "deleted %d replaced %d" % (d["deleted"], d["replaced"]))
ok(d["shorter"],
   "and it is SHORTER than v2 while carrying sections v2 does not have, "
   "so prose was compressed rather than added to")
ok(d["ratio"] < 0.5,
   "the similarity ratio is below a half: a rewrite, not an edit",
   str(d["ratio"]))
_h = R3.sections_added_and_dropped()
ok(any(x.startswith("## 6. THE PARSER GATE") for x in _h["v3"])
   and not any(x.startswith("## 6. THE PARSER GATE") for x in _h["v2"]),
   "section 6, the parser gate, is new in v3",
   str([x for x in _h["v3"] if "PARSER" in x]))


# ------------------------------------- 3  Step 0, the prior-art gate

section("3  Step 0 -- FMR_001's blocker")

g = R3.step0_prior_art()
ok(g["n_artifacts"] == 4,
   "0-1 tables four adjacent artifacts", str(g["artifacts"]))
ok(g["declares_not_redundant"] and g["states_done_in_procedure"],
   "the order reports the gate RUN, with a result, and marks Step 0 DONE "
   "in the procedure -- FMR_001 held the register NOT CLEARED TO SHIP on "
   "exactly this")
ok(len(g["closest_prior_art"]) == 1,
   "one artifact is marked CLOSEST PRIOR ART and must be cited",
   str(g["closest_prior_art"]))
ok(g["verification"] == R3.NOT_VERIFIABLE_HERE and not g["blocked"],
   "and the report is CARRIED, not verified: the arXiv hosts refuse "
   "CONNECT from here, so the closure is by declaration [CHOICE 12]")
ok(g["instructs_verify_before_citing"],
   "the order says so itself -- `Verify before citing` is in 0-1")
ok("network" not in R3_SRC.split("def main")[0].lower()
   or "no network" in R3_SRC,
   "and no probe runs at audit time; the refusal is recorded in the "
   "claim table, not measured inside the module")

s1 = R3.step1_deployment_class()
ok(s1["state"] == "NOT_RUN" and s1["offers_two_classes"],
   "Step 1 offers two deployment classes and the order picks neither -- "
   "FMR_002, unmoved")
ok(s1["entry_declining_to_narrow"] == "DUR-002",
   "and one entry declines to narrow in as many words",
   str(s1["entry_declining_to_narrow"]))


# ------------------------------------------------- 4  the V-map

section("4  the loss-variable map")

f = R3.f3_check()
ok(f["f3_wins"] == ["V7", "V13"],
   "F3 names two wins after amendment", str(f["f3_wins"]))
ok(f["computed_protective"] == ["V5", "V7", "V9", "V13"],
   "and the amended map computes four -- FMR_027 recurs unchanged across "
   "the rewrite", str(f["computed_protective"]))
ok(f["argued_away_by_name"] == ["V9"],
   "F2 argues one of the two extras away BY NAME", str(f["argued_away_by_name"]))
ok(f["unexplained"] == ["V5"],
   "and nothing anywhere in the order argues the other away -- FMR_028",
   str(f["unexplained"]))
ok(f["f3_withdrawn_wins"] == ["V3", "V14"],
   "F3 records its own withdrawn wins", str(f["f3_withdrawn_wins"]))
ok(f["original_marker"] == "Original F3 listed ",
   "v3 words the withdrawal differently from v2, and the shared reader "
   "takes a tuple of markers rather than a second copy",
   repr(f["original_marker"]))

v5 = R3.v5_definition()
ok(v5["a01_defines_carrier_as_reader"] and v5["v5_scores_on_performance"],
   "A-01 redefines a carrier as SOMEONE WHO CAN READ THE REPRESENTATION "
   "and V5 still scores on re-performance")
ok(v5["v5_amended"] is None,
   "V5 carries no amendment", str(v5["v5_amended"]))
ok("STRANDED" in (v5["stranded_entry"] or "").upper(),
   "and the register's own DUR-004 is the state where performance is "
   "continuous and reading is gone", str(v5["stranded_entry"]))


# --------------------------------------------- 5  column boundaries

section("5  column boundaries -- FMR_042, twice")

b = R3.boundary_report()
ok(b["vmap_rows_cut"] == ["V2"],
   "one score row still runs its ML cell past the column the amendment "
   "cell starts at -- FMR_042 recurs in the rewrite",
   str(b["vmap_rows_cut"]))
ok(E3.amended_scores()["V2"]["amendment_kind"] == "UNPARSED",
   "and that row's amendment cell files UNPARSED, kept apart from EMPTY")
ok(all(r["unrated"] is None for r in E3.amended_scores().values()),
   "every score in the map still passes the value-and-source gate")
ok(b["n_prior_art_cut"] == 2,
   "and the prior-art table v3 ADDS carries the same defect on one line "
   "-- a second instance, in new material, found by the same check",
   str(b["n_prior_art_cut"]))
_cut = b["prior_art"]["cut"]
ok(any(r["column"] == "scope" and r["cell"].endswith("DUR-")
       for r in _cut),
   "the cut truncates a cross-reference mid-token",
   str([r["cell"] for r in _cut]))
ok(any(r["column"] == "misses" and r["cell"] == "005" for r in _cut),
   "and prefixes its right-hand neighbour with somebody else's text",
   str([r["cell"] for r in _cut]))


# ------------------------------------------------ 6  the entry blocks

section("6  the entry blocks")

c = R3.field_coverage()
ok(c["schema_n"] == 12, "the schema declares twelve fields")
ok(len(c["rows"]) == 6, "six entry blocks", str([r["id"] for r in c["rows"]]))
ok(all(r["missing"] == ["id"] for r in c["rows"]),
   "every block is one field short and it is the SAME field on all six")
ok(len(c["unrated_parts"]) == 6,
   "so the order's own UNRATED PART rule fires on 6 of 6 entries",
   str(c["unrated_parts"]))
ok(all(i in c["id_in_heading"] for i in ("DUR-001", "DUR-006")),
   "because the id moved into the heading, which is a format change and "
   "not an omission")
ok(all(not r["extra"] for r in c["rows"]),
   "and no block carries a field the schema does not declare -- v2's "
   "NOTE field is gone, FMR_013 resolved by the rewrite")

h = R3.header_entry_count()
ok(h["agrees"] and h["stated"] == 6,
   "the header states six entries and six are delivered",
   "%s / %d" % (h["stated"], h["counted"]))


# ----------------------------------------------- 7  Steps 5, 6, 7

section("7  Steps 5, 6 and 7")

r5 = R3.step5_reconstruction()
ok(r5["n_entries"] == 6 and len(r5["single_valued"]) == 3,
   "three of six reconstruction cells state a single value",
   str(r5["single_valued"]))
ok(r5["distribution_over_single_valued"] == {"NO": 3},
   "and all three are NO", str(r5["distribution_over_single_valued"]))
ok(r5["merged_distribution"] is None,
   "no merged distribution is emitted: the two multi-valued cells vary "
   "along different axes")
ok(r5["no_declared_value"] == ["DUR-002"],
   "one cell states none of the three declared values",
   str(r5["no_declared_value"]))

s6 = R3.step6_requirements()
ok(s6["gated_in"] == ["DUR-001", "DUR-003", "DUR-004", "DUR-005",
                      "DUR-006"],
   "Step 6 gates in five entries", str(s6["gated_in"]))
ok([e["id"] for e in s6["excluded"]] == ["DUR-002"]
   and s6["excluded"][0]["states_requirement_anyway"],
   "and excludes the one that scores PARTIAL deliberately, which states "
   "a requirement anyway -- FMR_007")
ok(s6["word_scan_false_positives"] == ["DUR-002"],
   "a whole-word NONE scan reads that cell wrongly, because it says "
   "`not NONE` -- the lexical-proxy shape, avoided rather than found",
   str(s6["word_scan_false_positives"]))
ok(not s6["field_has_a_declared_vocabulary"],
   "existing_control is free text with no declared vocabulary, so the "
   "gate has to be read off the head token")
ok(s6["second_conjunct_state"] == "NOT_EVALUABLE",
   "the second conjunct has no test anywhere in the order -- FMR_008")
ok("non-trivial" in ORDER and not any(
    line.strip().startswith("non-trivial") for line in ORDER.split("\n")),
   "`non-trivial` appears and is never defined")

s7 = R3.step7_null_set()
ok(s7["state"] == "EMPTY",
   "Step 7's NULL SET is empty: no entry reports a mode already "
   "controlled")
ok(s7["cites_discipline"] == ["DUR-002"],
   "and the one entry that names the null-set discipline is the one that "
   "scores PARTIAL rather than NONE", str(s7["cites_discipline"]))


# ------------------------------------------ 8  projection and F_D

section("8  projection, and the header F_D asks for")

p = R3.projected_fraction()
ok(p["n_projected"] == 1 and p["cap"] == 1 and p["at_cap"],
   "the register sits exactly at the PROJECTED cap -- FMR_033",
   "%d of %d, cap %s" % (p["n_projected"], p["n_entries"], p["cap"]))
ok(not p["over_cap"], "and not over it")
ok(not p["f_d_satisfied"],
   "F_D directs the PROJECTED fraction into the header and the header "
   "states an entry count and a gate status and no fraction",
   p["header"])
ok(p["multi_valued_evidence"] == ["DUR-001", "DUR-005"],
   "two entries declare more than one evidence class at once, and the "
   "count reports both rather than resolving either",
   str(p["multi_valued_evidence"]))


# ------------------------------------------------ 9  F_K and F_M

section("9  F_K and F_M")

k = R3.f_k_bound()
ok(k["n_conditions"] == 7, "seven artifact-side conditions")
ok(k["n_with_stated_lifetime"] == 0,
   "and none states an expected lifetime", str(k["with_stated_lifetime"]))
ok(k["prose_claims_finite_lifetimes"],
   "while the prose introducing them says each has a finite lifetime")
ok(not k["retention_horizon_has_a_value"],
   "and no retention horizon carries a value, so F_K's bound compares "
   "two quantities the order states neither of")
ok(k["state"] == "NOT_APPLICABLE_AS_DELIVERED",
   "F_K is NOT_APPLICABLE_AS_DELIVERED -- FMR_030, recomputed on v3")
ok(all(r["reason"] for r in k["refused"]),
   "every refusal names a reason rather than returning a silent False")

m = R3.f_m_bound()
ok(m["n_conditions"] == 5, "five carrier-side conditions")
ok(m["active_set_empty"],
   "F_M's active set is EMPTY: none states a measurable production rate "
   "-- FMR_031, and the falsifier and the set it empties are still "
   "delivered in the same document")
ok(any(r["names_rate_in_words"] and not r["states_a_rate_value"]
       for r in m["rows"]),
   "one names a rate in words and carries no value")

sc = R3.screen_has_null()
ok(sc["states_no_null"] and sc["states_intended"],
   "DUR-005-C states its own CONSTANT_FIRES property and calls it "
   "intended -- read out of the delivered text, case-insensitively, "
   "because v3 capitalises where v2 did not")


# -------------------------------------------------- 10  F_L, F_J, F_I

section("10  F_L, F_J, F_I")

fl = R3.f_l_direction()
ok(fl["f_l_states_higher"],
   "F_L still states that correlation makes joint failure HIGHER than "
   "the naive product")
ok(fl["like_for_like_verdict"] == "BACKWARDS",
   "and survival is non-decreasing in correlation under any model that "
   "preserves the marginals, so joint failure is non-increasing -- "
   "FMR_029, unmoved by the rewrite",
   str(["%.4f" % r["failure"] for r in fl["rows"]]))
ok(not fl["a07_states_a_direction"],
   "while A-07, which section 10's own rule makes authoritative, states "
   "the same correction WITHOUT a direction and is right")
ok(fl["f_l_forbids_a_number"] and fl["conclusion_unaffected"],
   "and the conclusion is untouched: it rests on the inability to ensure "
   "each term, and no number goes on it")
ok(fl["n_terms"] == 7, "seven conjunction terms", str(fl["n_terms"]))

fj = R3.f_j_scope()
ok(fj["entry_blocks"] == 0 and fj["n_subsections"] == 6,
   "section 5 carries six subsections and no ENTRY blocks -- FMR_034's "
   "shape, in the renumbered section")
ok(fj["n_cited"] == 0,
   "and no subsection cites a current instance", str(fj["cited_instances"]))
ok(fj["names_observable_now"],
   "while the order names subsections that are observable now",
   str(fj["names_observable_now"]))
ok(fj["state"] == "ALL_PROJECTED",
   "so under F_J's own rule -- a CITED instance, not an observable one -- "
   "all of section 5 stays PROJECTED and the exemption is named and not "
   "exercised [CHOICE 13]")
ok(fj["worked_case_is_hypothetical"],
   "the one worked case in the section is introduced as a case, not "
   "cited as an instance")

fi = R3.f_i_independence()
ok(fi["has_single_number_accessor"],
   "F_I is enforced structurally: there is no accessor returning the "
   "volume figure alone")
rr = R3.redundancy_rule()
ok(rr["states_what_copies_do_not_share"],
   "the 4-2 REGISTER RULE requires any entry claiming redundancy to "
   "state what the copies DO NOT SHARE")
ok(rr["imported"] and rr["n_eff_three_sharing_a_substrate"] == 1
   and rr["n_eff_three_sharing_nothing"] == 3,
   "and that is effective-redundancy-audit's n_eff, IMPORTED and run: "
   "three copies sharing a substrate are one copy",
   "%s / %s" % (rr["n_eff_three_sharing_a_substrate"],
                rr["n_eff_three_sharing_nothing"]))


# ------------------------------- 11  section 6, the gate, folded back

section("11  section 6 -- this session's repair, delivered back")

pg = R3.parser_gate_conformance()
ok(pg["n_stated"] == 3,
   "section 6 names THREE fields on every extracted value",
   str(pg["n_stated"]))
ok("span" in pg["implemented_fields"]
   and "derivation" in pg["implemented_fields"],
   "and tools/sourced takes span and derivation as well",
   str(pg["implemented_fields"]))
ok(not pg["names_span"] and not pg["names_derivation"],
   "neither word appears anywhere in section 6")
ok(pg["states_unrated"] and pg["states_not_a_default"],
   "the return state is stated exactly: UNRATED, not zero, not clean, "
   "not a default")
ok(pg["states_numeral_rule"] and pg["states_completeness_rule"],
   "and both additions are stated -- a unit adjacent to the number, and "
   "expected count against registered count at end of run")
ok(pg["ties_to_dur_002"],
   "section 6 ties UNRATED to DUR-002's OUT_OF_ENVELOPE, which is the "
   "same return state one layer up")

cr = R3.containment_replay()
ok(cr["containment_catches"] == ["V3"],
   "replayed: containment catches the defect on one row",
   str(cr["containment_catches"]))
ok(cr["containment_misses"] == ["V6"],
   "and MISSES it on the other, where the buggy value occurs in the cell "
   "through the hyphen of the arrow -- containment is what section 6's "
   "three fields buy", str(cr["containment_misses"]))
ok(cr["searched_span_misses"] == ["V6"],
   "a span searched for AFTERWARDS misses it too",
   str(cr["searched_span_misses"]))
ok(cr["searched_span_points_elsewhere"] == ["V6"],
   "and points at the wrong occurrence -- offset 0, the arrow, not the "
   "score", str([(r["id"], r["searched_span"], r["true_span"])
                 for r in cr["rows"]]))
ok(sorted(cr["produced_span_refuses"]) == ["V3", "V6"],
   "what refuses both is a span PRODUCED BY THE EXTRACTION, and section "
   "6 names neither the span nor where it has to come from")
ok(all(r["produced_span_gate"] == "no_provenance" for r in cr["rows"]),
   "with the same reason on both rows")

# the numeral rule section 6 states, run against the gate it describes
_loc = S.Locator("test", 1, 0, None, "probe")
ok(isinstance(S.numeral_with_unit("exceeds ~1", _loc), S.Unrated),
   "`~1` with no unit FAILS THE GATE rather than parsing, exactly as "
   "section 6 says")
ok(isinstance(S.numeral_with_unit("about 3 years", _loc), S.Sourced),
   "and a numeral with an adjacent time unit passes -- the rule is not "
   "CONSTANT_SILENT")
_comp = S.registry_complete(("a", "b"), ("a",), "probe")
ok(_comp["state"] == "SHORT" and "b" in _comp["missing"],
   "and the completeness rule names what did not register")


# ------------------------------------- 12  entry 0, amendments, open

section("12  entry 0, the amendment record, still open")

e0 = R3.entry_zero_constructibility()
ok(not e0["is_an_entry_block"],
   "ENTRY 0 is delivered as prose in 0-2 and is not an entry block -- "
   "FMR_012, and v3 does not force it into one")
ok(e0["words"] > 50, "with the reasoning kept", str(e0["words"]))

am = R3.amendment_record()
ok(am["n"] == 11, "eleven amendments", str(am["n"]))
ok(am["complete"] == 11,
   "each carrying superseded, replacement and consequence",
   str(am["incomplete"]))
ok(len(am["with_forcing_case"]) == 1,
   "one carries a forcing case, which the schema treats as optional",
   str(am["with_forcing_case"]))

so = R3.still_open()
ok(so["n"] == 5, "five still-open items", str(so["n"]))
ok(len(so["name_a_missing_entry"]) == 3,
   "three of them name a missing entry rather than a missing answer",
   str(so["name_a_missing_entry"]))


# -------------------------------------------- 13  parser discipline

section("13  one parser, three documents")

_tree = ast.parse(V3_SRC)
_defs = [n.name for n in ast.walk(_tree) if isinstance(n, ast.FunctionDef)]
ok("_sign" not in _defs and "_amend_parse" not in _defs
   and "_parse_gutter" not in _defs and "_fenced_blocks" not in _defs,
   "entries_v3 defines none of the cell parsers, the gutter parser or "
   "the fence walker; it imports them",
   str([d for d in _defs if d.startswith("_")]))
ok("E2.amended_scores_from" in V3_SRC
   and "E2.vmap_boundary_report_from" in V3_SRC
   and "E2.f3_claim_from" in V3_SRC,
   "the gated score map, the boundary report and the F3 reader are one "
   "object across two documents -- a second copy is the drift "
   "tools/check_gate_drift.py exists to catch")
ok("R2.reconstruction_distribution_v2" in R3_SRC
   and "R2.projected_fraction_v2" in R3_SRC
   and "R2.f_k_bound" in R3_SRC and "R2.f_m_bound" in R3_SRC
   and "R2.f_l_direction" in R3_SRC,
   "and the audit's counts and arithmetic come from register_v2, "
   "generalised to take a document rather than copied")

# the generalisation did not change v2's own readings
ok(E2.f3_claim()["wins"] == ["V7", "V13"]
   and E2.f3_claim()["original_marker"]
   == "ORIGINAL FORM of F3 listed ",
   "v2's own F3 reading is unchanged by the generalisation")
ok(len(E2.amended_scores()) == 14
   and E2.amended_scores()["V6"]["amended"] == "--",
   "and so is v2's own score map")

_r3tree = ast.parse(R3_SRC)
_calls = [n for n in ast.walk(_r3tree) if isinstance(n, ast.Call)]
_names = set()
for n in _calls:
    if isinstance(n.func, ast.Name):
        _names.add(n.func.id)
    elif isinstance(n.func, ast.Attribute):
        _names.add(n.func.attr)
ok("urlopen" not in _names and "socket" not in _names
   and "run" not in _names and "Popen" not in _names,
   "no network and no subprocess at audit time",
   str(sorted(x for x in _names if "open" in x or "run" in x)))


# ----------------------------------------------- 14  housekeeping

section("14  housekeeping")

for name in ("entries_v3.py", "register_v3.py", "test_register_v3.py"):
    src = open(os.path.join(HERE, name), "rb").read()
    ok(all(b < 128 for b in src),
       "%s is ASCII" % name)
    ast.parse(src.decode())
    ok(True, "%s parses" % name)

for mod, path in (("entries_v3", "entries_v3.py"),
                  ("register_v3", "register_v3.py")):
    src = open(os.path.join(HERE, path)).read()
    ok("--selftest" in src and "return 2" in src,
       "%s refuses --selftest rather than exiting 0 on an invocation "
       "that runs nothing" % path)

_choice_nums = set(R3.CHOICES) | set(E3.CHOICES)
ok(_choice_nums == {1, 2, 12, 13, 14},
   "every open choice is numbered, and the numbers continue the "
   "instrument's own run rather than colliding with register.py's or "
   "register_v2's",
   str(sorted(_choice_nums)))
ok("[CHOICE 11]" in open(os.path.join(HERE, "register_v2.py")).read()
   and "[CHOICE 10]" in open(os.path.join(HERE,
                                          "register_v2.py")).read(),
   "and the duration and rate rules F_K and F_M run on are register_v2's "
   "choices, imported with the functions that take them, not renumbered "
   "here")
for n in _choice_nums:
    body = V3_SRC + R3_SRC
    ok("[CHOICE %d]" % n in body,
       "[CHOICE %d] is cited inline at the site where it takes effect" % n)

_render = R3.render()
ok("WORK_ORDER_V3.md -- AUDIT" in _render, "the audit renders")
for n in sorted(_choice_nums):
    ok("[CHOICE %d]" % n in _render,
       "and prints [CHOICE %d]" % n)

# the no-severity screen, imported from sheet-structure-scan
sys.path.insert(0, os.path.join(HERE, os.pardir, "sheet-structure-scan"))
import no_severity                                        # noqa: E402

for _label, _txt in (("register_v3 render", _render),
                     ("register_v3 choices",
                      "\n".join(t for _n, t in R3.choices_report())),
                     ("entries_v3 choices",
                      "\n".join(t for _n, t in E3.render_choices()))):
    _h = no_severity.hits(_txt)
    ok(_h == [], "%s screens clean with NO exemption" % _label,
       str(_h[:4]))
ok(no_severity.hits("a critical error") != [],
   "the screen fires on a plant, so the clean results mean something")


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
