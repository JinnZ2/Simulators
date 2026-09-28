#!/usr/bin/env python3
"""Checks on audit.py.  Prints its own count; nothing here stores one."""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import audit  # noqa: E402

N = [0]
FAIL = []


def ck(label, cond):
    N[0] += 1
    if not cond:
        FAIL.append(label)


# ------------------------------------------------ 1. the two renderings
r = audit.revision()
ck("v1 and v2 both present", r["v1_lines"] > 700 and r["v2_lines"] > 700)
ck("v2 is longer than v1", r["v2_bytes"] > r["v1_bytes"])
ck("TRA_001 v2 is a rewrite, not a pure insertion", not r["pure_insertion"])
ck("TRA_001 nothing was deleted", r["opcodes"]["delete"] == 0)
ck("TRA_001 lines were replaced", r["opcodes"]["replace"] > 0)

# ------------------------------------------------------ 2. the third copy
t = audit.third_copy()
if t["cited_object_resolves"]:
    ck("TRA_002 the cited blob is a byte-exact prefix of v1",
       t["is_prefix_of_v1"])
    ck("TRA_002 the prefix is most of v1", 0.4 < t["share"] < 0.8)
    ck("TRA_002 it names Kasuya", t["names_kasuya"])
    ck("TRA_002 it names Nian", t["names_nian"])
    ck("TRA_002 found by content as well as by the cited sha",
       audit.CITED_COMMIT in t["prefix_commits_by_content"])
    ck("TRA_002 verdict is REFUTED", t["verdict"].startswith("REFUTED"))
else:
    # The degradation is itself asserted: a clone without origin/main
    # must say so rather than reporting the claim as holding.
    ck("TRA_002 an unfetched object degrades to NOT_RESOLVABLE",
       t["verdict"] == "NOT_RESOLVABLE_IN_THIS_CLONE")
    ck("TRA_002 the degradation names the remedy", "git fetch" in t["note"])

# ------------------------------------------------------ 3. the repair log
rl = audit.repair_log()
ck("TRA_003 six rows parse", rl["n"] == 6)
ck("TRA_003 every row has a mechanical test", rl["untested"] == 0)
ck("TRA_003 all six are applied in v2", rl["applied"] == 6)
# the R2 false negative, pinned: a document-wide token test cannot see it
ck("TRA_003 v1 already uses UNVERIFIED for something else",
   "UNVERIFIED" in audit.src(audit.V1))
ck("TRA_003 the line-level test separates them",
   audit._all_lines_flagged(audit.src(audit.V2), "2.6 mm/yr", "UNVERIFIED")
   and not audit._any_line_flagged(audit.src(audit.V1), "2.6 mm/yr",
                                   "UNVERIFIED"))
# null: the line test must be able to say no
ck("TRA_003 the line test is not CONSTANT_FIRES",
   not audit._all_lines_flagged("a 2.6 mm/yr line\n", "2.6 mm/yr",
                                "UNVERIFIED"))

# --------------------------------------------- 4. did R1 reach downstream
rr = audit.repair_reach()
ck("TRA_026 v1 names Bradley and never Williams",
   any(x["file"] == "SOURCE_DROP.md" and x["bradley"] and not x["williams"]
       for x in rr["rows"]))
ck("TRA_026 v2 names Williams", any(x["file"] == "SOURCE_DROP_V2.md"
                                    and x["williams"] for x in rr["rows"]))
ck("TRA_026 the field brief is unrepaired",
   "WORKER_FIELD_BRIEF_DESIGN_LIFE.md" in rr["unrepaired"])
ck("TRA_026 the two documents with no citation are not flagged",
   "WARNING_CARD_SPEC.md" not in rr["unrepaired"]
   and "OPERATIONS_REDUNDANCY_AUDIT_TEMPLATE.md" not in rr["unrepaired"])

# ---------------------------------------------------------- 5. the inputs
ip = audit.inputs_present()
ck("TRA_004 nine input files are stated", ip["stated_total"] == 9)
ck("TRA_004 every stated input is named in the method note",
   all(s["named_in_method_note"] for s in ip["stated"]))
ck("TRA_004 none of them is in the delivery", not ip["reproducible"])

# -------------------------------------------------------------- 6. S1
s = audit.run_s1()
ck("TRA_005 both quoted S1 rows reproduce", s["all_match"])
ck("TRA_005 two rows were quoted", len(s["rows"]) == 2)
ck("TRA_005 the module says the zero is by construction",
   s["module_says_by_construction"])
ck("TRA_005 no Thwaites quantity enters", not s["thwaites_input"])

# ----------------------------------------------------------- 7. the chain
c = audit.run_chain()
ck("TRA_006 four rows were quoted", len(c["rows"]) == 4)
ck("TRA_006 every number is the shipped fixture's",
   c["all_numbers_identical"])
ck("TRA_006 the boundary inflow was parsed, not retyped",
   c["boundary_inflow"] == 6.0)
ck("TRA_008 the module's column names are not the document's",
   c["module_column_names"] != c["doc_column_names"])
ck("TRA_008 every row violates sum <= 2*max under the document's labels",
   len(c["rows_violating_sum_le_2max"]) == 4)
ck("TRA_007 the detector does not always fire",
   not c["detector_always_fires"])
ck("TRA_007 both null fixtures return REFUTED",
   all(v == "REFUTED" for v in c["null_fixtures"].values()))

# ------------------------------------------------------ 8. measurement-fork
fa = audit.fork_arms()
f = audit.run_fork()
ck("TRA_010 compare.py holds exactly three arms", fa["n_arms"] == 3)
ck("TRA_010 the arm names are the three generators",
   set(fa["arms"]) == {"conventional", "coupling", "widen"})
ck("TRA_010 a fourth arm is not expressible",
   fa["fourth_arm_expressible"] is False)
ck("TRA_012 MF_004 is unrepaired in compare.py",
   fa["residual_pools_every_arm"])
ck("TRA_009 the verdict sentence is a module constant",
   f["verdict_text_is_a_module_constant"])
ck("TRA_009 the shipped spec returns the same empty cell",
   f["shipped_spec_cell_empty"])
ck("TRA_009 the probe counts differ, so another spec was run",
   f["counts_differ"])
ck("TRA_012 the document carries a COVERED line", f["covered_in_document"])

# ----------------------------------------------------------- 9. the kappa
k = audit.kappa_constant_coder()
ck("TRA_013 62 non-degenerate codings were swept", k["n_codings"] == 62)
ck("TRA_013 none of them gives a non-zero kappa", k["kappa_nonzero"] == 0)
ck("TRA_013 two equal constant coders give 1.0, not 0",
   k["degenerate_both_constant"] == 1.0)
ck("TRA_013 the document reports 0.000", k["doc_reports_kappa_zero"])
ck("TRA_013 the document reports N_eff = 1", k["doc_reports_neff_1"])

# ------------------------------------------------------------- 10. AMOC
g = audit.stommel_grid()
ck("TRA_018 six grids were run", len(g["rows"]) == 6)
ck("TRA_018 the spinodal moves with the grid", g["spread"] > 0.005)
ck("TRA_018 the document's value is reproduced by one of them",
   len(g["document_value_reproduced_by"]) >= 1)
ck("TRA_018 the document's value is the lowest",
   g["document_value_is_lowest"])
cal = audit.calibration()
ck("TRA_019 0.50 Sv is the calibration's own anchor",
   cal["anchor_is_the_document_value"])
ck("TRA_019 the calibration hardcodes a third spinodal",
   cal["spinodal_F_hardcoded"] == 0.217)
ck("TRA_019 converting the document's own F does not give 0.50",
   abs(cal["F_to_sv_of_document_F"] - 0.50) > 0.01)
ck("TRA_020 the docstring supplies a band", cal["literature_cluster_added_Sv"]
   == (0.1, 0.4))
ck("TRA_020 the anchor's added flux sits inside that band",
   cal["anchor_inside_cluster"])

# ------------------------------------------------------- 11. the arithmetic
fx = audit.flux_arithmetic()
ck("TRA_021 2.6 mm/yr reproduces the document's 0.030 Sv", fx["sv_matches"])
ck("TRA_022 50-60 Gt as grounded ice brackets 0.15 mm",
   fx["mm_matches_as_grounded"])
ck("TRA_022 as floating shelf melt it is an order smaller",
   fx["overstatement_factor"] > 5)
ck("TRA_022 the document names basal melt",
   fx["quantity_named_by_document"] == "basal melt")
# known answer: the conversion must not silently accept a None
ck("TRA_021 sle_to_sv(None) is None, never 0.0",
   audit.sle_to_sv(None) is None)
ck("TRA_021 sle_to_sv(0) is 0.0", audit.sle_to_sv(0) == 0.0)

# ---------------------------------------------------------- 12. gap blocks
gb = audit.gap_blocks()
ck("TRA_023 four gap blocks parse", gb["n_blocks"] == 4)
ck("TRA_023 the register's own reader ingests none as delivered",
   gb["records_the_register_reader_sees_as_delivered"] == 0)
ck("TRA_023 every parsed block carries all seven fields",
   all(x["fields_present"] == 7 for x in gb["rows"]))
ck("TRA_023 every STATE is in the register's vocabulary",
   all(x["state_in_vocabulary"] for x in gb["rows"]))
ck("TRA_023 THW-05 is not a block", not gb["thw05_is_a_block"])
ck("TRA_023 exactly one block carries a composite KIND",
   gb["composite_kind"] == ["THW-02"])
ck("TRA_024 that block's STATE contradicts half its KIND",
   [x["id"] for x in gb["state_contradicts_kind"]] == ["THW-02"])
ck("TRA_024 the forced KIND is boundary-artifact",
   all(x["forced"] == "boundary-artifact"
       for x in gb["state_contradicts_kind"]))

# ------------------------------------------------------ 13. declared-frame
df = audit.declared_frame_surface()
ck("TRA_015 the checker emits no frame flag", not df["emits_the_word_flag"])
ck("TRA_016 observer_access is never compared",
   "observer_access" in df["recorded_never_compared"])
ck("TRA_015 the document asserts flags anyway",
   len(df["flags_asserted_in_document"]) >= 2)

# --------------------------------------------- 14. three smaller reads
ap = audit.authored_parenthetical()
ck("TRA_011 the document carries the annotation", len(ap["in_document"]) == 1)
ck("TRA_011 compare.py does not print it", not ap["in_compare_py"])
cl = audit.closure_labels()
ck("TRA_014 every quoted label is the module's", cl["all_from_the_module"])
ck("TRA_014 the document names its own restatement",
   cl["document_states_its_own_caveat"])
oi = audit.run_oir()
ck("TRA_017 the OIR pair reproduces", oi["reproduces"])
ck("TRA_017 both ensembles were read", len(oi["rates"]) == 2)
ck("TRA_017 the clean ensemble is 0.0/0.0", (0.0, 0.0) in oi["rates"])
ck("TRA_017 the document scopes the transfer down",
   oi["document_scopes_it_down"])

# --------------------------------------------------- 14. climate-modeling
cm = audit.climate_modeling_state()
ck("TRA_025 the state is measured, not assumed",
   cm["state"] in ("NOT_RUN", "RUNNABLE"))
ck("TRA_025 a NOT_RUN names what is absent",
   cm["state"] == "RUNNABLE" or cm["missing"])
ck("TRA_025 the document relabelled the block", cm["document_relabelled_it"])

# ------------------------------------------------------- 15. what is carried
ca = audit.carried()
ck("TRA_027 the document names DOIs", ca["dois_named"] > 5)
ck("TRA_027 none is verified here", ca["verified_here"] == 0)
ck("TRA_027 the reason is the egress gate", "egress" in ca["reason"])

# ---------------------------------------------------- the module's manners
text = audit.render()
ck("the render is non-trivial", len(text) > 4000)
ck("the render names every claim id",
   all(("TRA_%03d" % i) in text for i in
       list(range(1, 29))))
ck("--choices prints every choice", len(audit.choices()) == 6)
ck("every choice marker appears in the render",
   all(("[CHOICE %d]" % i) in text for i in range(1, 7)))
ck("audit.py refuses --selftest", audit.main(["--selftest"]) == 2)
ck("--choices exits clean", audit.main(["--choices"]) == 0)

# the delivered files are never opened for writing
tree = ast.parse(audit.src(os.path.join(HERE, "audit.py")))
writes = []
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
            and node.func.id == "open":
        mode = ""
        if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
            mode = node.args[1].value
        for kw in node.keywords:
            if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                mode = kw.value.value
        if "w" in mode or "a" in mode or "+" in mode:
            writes.append(ast.dump(node)[:40])
ck("audit.py never opens a file for writing", not writes)
# null: the detector must be able to see one
ck("that write detector is not silent",
   any(isinstance(n, ast.Call) for n in ast.walk(ast.parse(
       "open('x','w')"))))


def _writes_in(source):
    out = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "open":
            if len(node.args) > 1 and isinstance(node.args[1], ast.Constant) \
                    and "w" in node.args[1].value:
                out.append(1)
    return out


ck("planted write is caught", len(_writes_in("open('x','w')")) == 1)
ck("a read is not caught", len(_writes_in("open('x')")) == 0)

# ------------------------------------------------- the severity screen
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import no_severity  # noqa: E402

# ONE declared exemption, one token: INVALID AS RELIABILITY is the repair
# log's own status cell, used verbatim as the mechanical needle for R6.
# Rewording it would misquote the source.  Three arms.
EXEMPT = ("INVALID AS RELIABILITY",)
ck("the exemption is one token wide", len(EXEMPT) == 1)
masked = text
for tok in sorted(EXEMPT, key=len, reverse=True):
    masked = masked.replace(tok, "X" * len(tok))
ck("arm 1: masked, the render screens clean", not no_severity.hits(masked))
unmasked = no_severity.hits(text)
ck("arm 2: unmasked, only the exempted token fires",
   len(unmasked) == 1 and unmasked[0][1] == "invalid")
ck("arm 3: a planted word outside the exemption is caught",
   len(no_severity.hits(masked + "\nthis is a defect\n")) == 1)
ck("the exempted string is the delivered repair log's own cell",
   "INVALID AS RELIABILITY" in audit.src(audit.V2))

print("checks: %d   failed: %d" % (N[0], len(FAIL)))
for f in FAIL:
    print("  FAIL  " + f)
sys.exit(1 if FAIL else 0)
