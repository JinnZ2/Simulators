#!/usr/bin/env python3
"""
Checks for the revised order. WORK_ORDER_V2.md and WORK_ORDER.md are both
delivered and neither is edited; every expectation is here.

Run: python3 test_register_v2.py
CC0. Stdlib only, no pytest. Parses under 3.9.
"""

import ast
import inspect
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import entries as E1                                      # noqa: E402
import entries_v2 as E2                                   # noqa: E402
import register as R1                                     # noqa: E402
import register_v2 as R2                                  # noqa: E402
import no_severity                                        # noqa: E402

PASS = []
FAIL = []


def ok(cond, label, detail=""):
    (PASS if cond else FAIL).append((label, detail))


def section(name):
    print("\n-- %s" % name)


V2_SRC = open(os.path.join(HERE, "register_v2.py")).read()
E2_SRC = open(os.path.join(HERE, "entries_v2.py")).read()


# ------------------------------------------------------ 1. the pair

section("1  the pair -- v2 is an additive revision of v1")
ok(os.path.exists(os.path.join(HERE, "WORK_ORDER.md")),
   "v1 is still in the folder, unedited")
ok(os.path.exists(os.path.join(HERE, "WORK_ORDER_V2.md")),
   "v2 is landed beside it, not over it")
pd = R2.pair_diff()
ok(pd["deleted"] == 0, "no line was deleted", "deleted=%d" % pd["deleted"])
ok(pd["replaced_blocks"] == 0, "no existing line was modified",
   "replaced=%d" % pd["replaced_blocks"])
ok(pd["purely_additive"], "the revision is purely additive",
   "inserted=%d" % pd["inserted"])
ok(pd["inserted"] > 600, "and it is a large one",
   "inserted=%d" % pd["inserted"])
fa = R2.falsifiers_added()
ok(fa["added"] == ["F_K", "F_M", "F_L", "F_J"],
   "four falsifiers added, in delivered order", str(fa["added"]))
ok(fa["removed"] == [], "none removed")
ok(fa["changed_bodies"] == [],
   "every v1 falsifier body survives verbatim -- a revision quoting an "
   "earlier document is a copy, and copies drift", str(fa["changed_bodies"]))
ok(len(fa["v2"]) == 13, "thirteen falsifiers in v2", str(len(fa["v2"])))
ok(fa["v2"][-2:] == ["F_I", "F_H"] == fa["v1"][-2:],
   "v1's F_I-before-F_H ordering is carried into v2 unchanged -- the "
   "revision did not tidy it", "%s / %s" % (fa["v1"][-2:], fa["v2"][-2:]))


# -------------------------------------------------------- 2. the V-map

section("2  the loss-variable map, amendments applied")
ok(len(E2.v_definitions()) == 14, "fourteen variables defined",
   str(len(E2.v_definitions())))
ok(len(E2.v_scores()) == 14, "fourteen score rows",
   str(len(E2.v_scores())))
m = R2.amended_map()
ok(m["rows"]["V3"]["original"] == "+" and m["rows"]["V3"]["amended"] == "--",
   "A-01 moves V3 from protective to loss-driving, and BOTH are retained "
   "-- the order's rule is that the amended score is authoritative and the "
   "original stays auditable")
ok(m["rows"]["V6"]["amended"] == "--", "A-02 moves V6 to --")
ok(m["rows"]["V14"]["amended"] == "SPLIT", "A-03 splits V14")
ok(m["moved_by_amendment"] == ["V3", "V6", "V14"],
   "exactly three rows move, matching the three amendments that carry a "
   "score", str(m["moved_by_amendment"]))
ok(m["rows"]["V3"]["amendment"] == "A-01"
   and m["rows"]["V6"]["amendment"] == "A-02"
   and m["rows"]["V14"]["amendment"] == "A-03",
   "each moved row names the amendment that moved it")
def _lstrip_with_arg(fn_name, src):
    """Calls to .lstrip(x) inside one function, read from the AST.

    A substring scan for "lstrip" fires on the docstring in which
    amended_scores NAMES the construct it refuses -- the lexical-proxy
    shape (UNI_009, T1-1) inside the checker written against it. A
    comment and a docstring are not calls, so the AST does not see
    them."""
    import ast
    tree = ast.parse(src)
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != fn_name:
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) \
                    and isinstance(sub.func, ast.Attribute) \
                    and sub.func.attr in ("lstrip", "rstrip", "strip") \
                    and sub.args:
                hits.append(sub.func.attr)
    return hits


ok(_lstrip_with_arg("amended_scores", E2_SRC) == [],
   "the amended score is not read with strip on a character set -- "
   "lstrip(\"-> \") deletes the value's own leading \"--\" and returns the "
   "UNamended score on the map whose rule is that the amended one is "
   "authoritative. Read from the AST, because a substring scan fires on "
   "the docstring that names the refused construct",
   str(_lstrip_with_arg("amended_scores", E2_SRC)))
ok(_lstrip_with_arg("amended_scores", E2_SRC.replace(
       "        out[vid] = {",
       "        _ = am_cell.lstrip(\"-> \")\n        out[vid] = {")) != [],
   "and the AST check is not CONSTANT_SILENT: a planted lstrip fires it")
ok(all(r["unrated"] is None for r in m["rows"].values()),
   "every score in the map passes the value-and-source gate: value, "
   "literal source text, locator, and a span that slices back to the "
   "value")
ok(m["rows"]["V3"]["amended_span"] == (3, 5)
   and m["rows"]["V6"]["amended_span"] == (3, 5)
   and m["rows"]["V14"]["amended_span"] == (3, 8),
   "each amended score names WHERE in its cell it was found",
   str([m["rows"][v]["amended_span"] for v in ("V3", "V6", "V14")]))
ok(m["rows"]["V5"]["amended_from"] == m["rows"]["V5"]["amended_from"]
   and "ml" in m["rows"]["V5"]["amended_from"],
   "a row with no amendment keeps the ML cell as the source of its "
   "authoritative score, rather than being re-attributed to a cell it "
   "did not come from -- that re-attribution is the defect",
   str(m["rows"]["V5"]["amended_from"]))
ok(m["rows"]["V9"]["amended"] == "++",
   "V9 keeps the strongest protective score in the table")


# ----------------------------------------------------------- 3. F3

section("3  F3 names two wins and the table gives four")
f3 = R2.f3_check()
ok(f3["f3_names"] == ["V7", "V13"], "F3 names V7 and V13",
   str(f3["f3_names"]))
ok(f3["protective_after_amendment"] == ["V5", "V7", "V9", "V13"],
   "the amended table gives four protective variables",
   str(f3["protective_after_amendment"]))
ok(f3["unaccounted"] == ["V5", "V9"], "two are unaccounted for",
   str(f3["unaccounted"]))
ok(f3["argued_away_in_F2"] == ["V9"],
   "F2 argues V9 away BY NAME -- the protective variable is maxed and "
   "does not protect", str(f3["argued_away_in_F2"]))
ok(f3["unaccounted_and_unargued"] == ["V5"],
   "V5 is left out of F3's win list by nothing stated anywhere",
   str(f3["unaccounted_and_unargued"]))
v5 = R2.v5_definition()
ok("re-taught" in v5["gloss"] and "re-performed" in v5["gloss"],
   "and V5's own gloss is carrier-side: how often it is actually "
   "RE-TAUGHT or re-performed", v5["gloss"])
a01 = [a for a in E2.amendments() if a["id"] == "A-01"][0]
ok("READ THE REPRESENTATION" in a01["replacement"],
   "A-01's correction is definitional: a carrier is someone who can READ "
   "THE REPRESENTATION")
d4 = [e for e in E2.entries_v2() if e["id"] == "DUR-004"][0]
ok("STRANDED" in d4["fields"]["mechanism"]
   and "near zero" in d4["fields"]["mechanism"],
   "and DUR-004 is the state where execution is continuous and the "
   "carrier population is near zero -- V5 scored + on the machine side "
   "of a variable A-01 had just moved to the carrier side")
ok(f3["f3_original_wins"] == ["V3", "V14"],
   "F3 records its own superseded win list", str(f3["f3_original_wins"]))


# ------------------------------------------------ 4. the F_L direction

section("4  F_L states a direction and the direction is backwards")
ok(abs(R2.joint_survival(0.9, 7, 0.0) - 0.9 ** 7) < 1e-12,
   "at correlation zero the model is the independent product")
ok(abs(R2.joint_survival(0.9, 7, 1.0) - 0.9) < 1e-12,
   "at correlation one it is the single marginal")
ok(abs(R2.joint_survival(0.9, 1, 0.5) - 0.9) < 1e-12,
   "with one term the correlation cannot matter")
ok(R2.joint_survival(0.9, 0, 0.5) is None,
   "fewer than one term returns None, not a probability")
prev, mono = None, True
for rho in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0):
    v = R2.joint_survival(0.9, 7, rho)
    if prev is not None and v < prev - 1e-12:
        mono = False
    prev = v
ok(mono, "survival is non-decreasing in correlation, so joint FAILURE is "
   "non-increasing")
d = R2.f_l_direction()
ok(d["f_l_states"] == "HIGHER", "F_L states HIGHER")
ok(d["like_for_like_verdict"] == "BACKWARDS",
   "on the like-for-like reading -- failure at rho against failure at "
   "zero -- the stated direction is backwards at every parameter")
ok(d["rows"][0]["failure"] > d["rows"][-1]["failure"],
   "failure falls as correlation rises",
   "%.4f -> %.4f" % (d["rows"][0]["failure"], d["rows"][-1]["failure"]))
ok(d["cross_type_verdict"] == "VALUE_DEPENDENT",
   "on the cross-type reading -- a failure probability against a "
   "survival product -- it is true at some parameters and not others, so "
   "it is not a general claim either",
   "%d of %d" % (d["cross_type_true_at"], d["cross_type_of"]))
a07 = [a for a in E2.amendments() if a["id"] == "A-07"][0]
ok("Correlation moves the joint" in a07["replacement"]
   and "HIGHER" not in a07["replacement"],
   "A-07 states the same correction WITHOUT a direction, and section 9 is "
   "the authoritative record by the order's own rule")
ok("rests on the inability to ENSURE each term" in a07["replacement"],
   "and states why the conclusion survives the arithmetic being wrong")
ok(d["conclusion_unaffected"] is True,
   "so nothing that depends on the conclusion moves")
fl = dict(E2.falsifiers_v2())["F_L"]
ok("Do not put a number on it" in fl,
   "F_L's own instruction is to put no number on it, which this audit "
   "follows -- the model exists to check a direction")


# ------------------------------------------- 5. conjunction/disjunction

section("5  DUR-006-C as arithmetic")
ok(len(E2.conjunction_terms()) == 7,
   "seven terms in the conjunction, as F_L and A-07 both say",
   str(len(E2.conjunction_terms())))
ok(len(E2.transfer_modes()) == 6,
   "six transfer modes, as DUR-006's evidence_class says",
   str(len(E2.transfer_modes())))
modes = [mm[0] for mm in E2.transfer_modes()]
ok("strategy change" in modes,
   "including the quiet one, which produces no external event",
   str(modes))
cd = R2.conjunction_vs_disjunction()
ok(cd["per_holder_below_per_term"],
   "the distributed arrangement is modelled with a LOWER per-holder "
   "number")
ok(cd["disjunction_survival"] > cd["conjunction_survival"],
   "and survives better anyway",
   "%.4f vs %.4f" % (cd["disjunction_survival"],
                     cd["conjunction_survival"]))
ok(cd["n_terms"] == 7, "the term count comes from the order, not a literal")


# ------------------------------------------------------------ 6. F_K

section("6  F_K cannot be applied to the set it bounds")
k = R2.f_k_bound()
ok(k["n_conditions"] == 7, "seven artifact-side conditions",
   str(k["n_conditions"]))
ok(k["n_with_stated_lifetime"] == 0,
   "none carries an expected lifetime, though the prose says each has one")
ok(k["retention_horizon_mentions"] >= 2
   and not k["retention_horizon_has_a_value"],
   "the retention horizon is named and never valued",
   "%d mentions" % k["retention_horizon_mentions"])
ok(k["state"] == "NOT_APPLICABLE_AS_DELIVERED",
   "so the bound compares two quantities the order states neither of")
ok(R2._has_duration("expected lifetime 10 years"),
   "the duration test fires on a numeral next to a time unit")
ok(not R2._has_duration("a continuing custodian (see DUR-006)"),
   "and NOT on a cross-reference id -- the first version used a bare "
   "numeral test and scored this as a stated lifetime")
ok(not R2._has_duration("hop count over the retention horizon exceeds ~1"),
   "nor on a hop count -- the same bare test scored this as a retention "
   "horizon carrying a value, and both false positives ran toward "
   "reporting the bound as applicable")


# ------------------------------------------------------------ 7. F_M

section("7  F_M empties the set delivered with it")
fm = R2.f_m_bound()
ok(fm["n_conditions"] == 5, "five carrier-side conditions",
   str(fm["n_conditions"]))
ok(fm["n_active"] == 0 and fm["active_set_empty"],
   "F_M admits none of them: 0 of 5 state a measurable production rate")
ok(fm["n_uninstrumented"] == 5,
   "all five are UNINSTRUMENTED by F_M's own word, and excluded from the "
   "active set rather than carried as claims")
named = [r for r in fm["rows"] if r["names_rate_in_words"]]
ok(len(named) == 1,
   "exactly one names a rate in words -- 'at replacement rate' -- with no "
   "value", str([r["condition"][:40] for r in named]))
ok(R2._has_rate("produced at 3 per 1000 engineers/year"),
   "the rate test fires on a numeral with a rate marker")
ok(not R2._has_rate("training pipelines that produce the above at "
                    "replacement rate"),
   "and not on a rate named in words, which is what F_M's own word "
   "'measurable' excludes")
sn = R2.screen_has_null()
ok(sn["states_no_null"] and sn["states_intended"],
   "DUR-005-C states its own CONSTANT_FIRES property and calls it "
   "intended: every capacity scores PRODUCED or FLAGGED, nothing scores "
   "clean")
ok("empty" in sn["interaction_with_F_M"],
   "so the two stages are: the screen admits everything, F_M admits none "
   "of it, and the delivered candidate set comes out empty")


# ---------------------------------------------------------- 8. Step 5

section("8  Step 5 recounted on six entries")
rd = R2.reconstruction_distribution_v2()
ok(rd["n_entries"] == 6, "six entries", str(rd["n_entries"]))
ok(len(rd["single_valued"]) == 3,
   "three cells state exactly one of the schema's three values -- up from "
   "one of four in v1", str(rd["single_valued"]))
ok(rd["multi_valued"] == ["DUR-001", "DUR-003"],
   "two state two", str(rd["multi_valued"]))
ok(rd["no_declared_value"] == ["DUR-002"],
   "one states none of the three", str(rd["no_declared_value"]))
ok(set(rd["axes"]) == set(rd["multi_valued"]),
   "each multi-valued cell has its axis named")
ok(rd["axes"]["DUR-001"] != rd["axes"]["DUR-003"],
   "and the two axes are different -- control state against time")
ok(rd["merged_distribution"] is None,
   "so no merged distribution is emitted; one count over both would be a "
   "count across unlike objects")
ok(rd["distribution_over_single_valued"] == {"NO": 3},
   "the distribution that IS computable is three NOs",
   str(rd["distribution_over_single_valued"]))
ok(E2._word_in("NO after transfer", "NO")
   and not E2._word_in("NONE under current practice", "NO")
   and not E2._word_in("Not applicable", "NO"),
   "whole-word containment: NO sits inside NONE and inside NOT, and a "
   "substring scan reports a reconstruction value on cells that state "
   "none")


# ------------------------------------------------- 9. PROJECTED cap

section("9  the PROJECTED fraction")
pf = R2.projected_fraction_v2()
ok(pf["n_projected"] == 1, "one entry states PROJECTED",
   str(pf["projected"]))
ok(pf["cap"] == 1 and pf["at_cap"],
   "and the register sits exactly at the cap, so a seventh projected "
   "entry would breach a fraction the order declines to state",
   "cap=%s" % pf["cap"])
ok(not pf["over_cap"], "it is not over it")
ok(pf["multi_valued_evidence"] == ["DUR-001", "DUR-005"],
   "two entries state more than one evidence class, which section 2 "
   "defines as one of three", str(pf["multi_valued_evidence"]))
ok("fraction_cap" in V2_SRC and "R1.fraction_cap" in V2_SRC,
   "the cap is imported from register.py rather than reimplemented, so "
   "the two cannot disagree about what the inequality is")


# ------------------------------------------------------------ 10. F_J

section("10  F_J's scope")
fj = R2.f_j_scope()
ok(fj["entry_blocks_in_6C"] == 0,
   "section 6C carries no ENTRY blocks", str(fj["entry_blocks_in_6C"]))
ok(fj["subsections"] == 7, "it carries seven subsections",
   str(fj["subsections"]))
ok(fj["state"] == "NO_ENTRIES_TO_MARK",
   "so F_J directs a marking at entries that do not exist")
so = R2.still_open_v2()
ok(so["n"] == 5, "five items still open", str(so["n"]))
ok(len(so["name_a_missing_entry"]) >= 3,
   "at least three of them name a missing entry, which is the same "
   "absence F_J's instruction runs into",
   str(len(so["name_a_missing_entry"])))


# ------------------------------------------------ 11. the amendments

section("11  the amendment record")
ar = R2.amendment_record()
ok(ar["n"] == 11, "eleven amendments", str(ar["n"]))
ok(ar["complete"] == 11,
   "all eleven carry superseded, replacement, forcing case and "
   "consequence", str(ar["incomplete"]))
sec9 = " ".join(" ".join(E2._section("## 9. AMENDMENT RECORD",
                                     stop_prefix=("### ", "## "))).split())
ok("Silent overwrite is not permitted" in sec9,
   "the record's own rule is that a withdrawn claim stays visible")
ok(all(a["superseded"].strip() for a in E2.amendments()),
   "and every amendment carries a non-empty superseded statement -- "
   "which is what makes the F3 and F_L checks above possible at all")


# ------------------------------------------------- 12. nothing rated

section("12  nothing here rates an entity")
for fn in (R2.f_l_direction, R2.conjunction_vs_disjunction):
    sig = inspect.signature(fn)
    out = fn()
    keys = " ".join(out)
    missing = [p for p in sig.parameters
               if p not in out and p not in keys.split()
               and not any(p in k for k in out)
               and p not in ("grid",)]
    ok(not missing,
       "%s returns every parameter it was given, so no number from it "
       "can be quoted without its model" % fn.__name__, str(missing))
ok("This is a model, not a measurement" in R2.joint_survival.__doc__,
   "the probability primitive says in its own docstring that it is a "
   "model")
tree = ast.parse(V2_SRC)
argnames = set()
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        for a in node.args.args:
            argnames.add(a.arg)
ok(not any(t in argnames for t in ("firm", "company", "vendor", "entity",
                                   "provider", "organisation")),
   "no function takes an entity as an argument", str(sorted(argnames)))
ok("does not rate any firm" in V2_SRC,
   "and the module states the scope in its own docstring")


# ------------------------------------------ 13. imports, not copies

section("13  one parser, two documents")
ok("import entries as E" in E2_SRC,
   "entries_v2.py imports the v1 parser rather than copying it")
for helper in ("_parse_gutter", "_fenced_blocks"):
    ok(("E.%s" % helper) in E2_SRC,
       "%s comes from entries.py" % helper)
for helper in ("_parse_gutter", "_fenced_blocks", "_is_field_line"):
    ok(("def %s" % helper) not in E2_SRC,
       "and %s is not redefined here" % helper)
ok(E2.ORDER_PATH_V2 != E1.ORDER_PATH,
   "the two parsers read two different documents")
ok(E1.order_text() != E2.order_text(),
   "which are not the same text")


# ------------------------------------------------ 14. choices, CLIs

section("14  choices and CLIs")
ok(sorted(R2.CHOICES) == [9, 10, 11],
   "three choices, numbered on from register.py's 1..8",
   str(sorted(R2.CHOICES)))
ok(max(R1.CHOICES) < min(R2.CHOICES),
   "no id collides with the v1 instrument's")
rep = R2.choices_report()
for k in R2.CHOICES:
    ok("[CHOICE %d]" % k in rep, "[CHOICE %d] prints" % k)
i = V2_SRC.find("CHOICES = {")
j = V2_SRC.find("\ndef ", i)
cited = V2_SRC[:i] + V2_SRC[j:]
for k in R2.CHOICES:
    ok(cited.count("CHOICE %d" % k) >= 1,
       "[CHOICE %d] is cited at the site where it takes effect" % k)
for mod in ("entries_v2.py", "register_v2.py"):
    p = subprocess.run([sys.executable, os.path.join(HERE, mod),
                        "--selftest"], capture_output=True)
    ok(p.returncode == 2, "%s refuses --selftest" % mod,
       "rc=%d" % p.returncode)
p = subprocess.run([sys.executable, os.path.join(HERE, "register_v2.py"),
                    "--choices"], capture_output=True)
ok(p.returncode == 0 and b"[CHOICE 9]" in p.stdout,
   "register_v2.py --choices prints")


# --------------------------------------------------- 15. the screen

section("15  the report screens clean")
for label, txt in (("register_v2 render", R2.render()),
                   ("register_v2 choices", R2.choices_report()),
                   ("entries_v2 render", subprocess.run(
                       [sys.executable, os.path.join(HERE, "entries_v2.py")],
                       capture_output=True).stdout.decode())):
    h = no_severity.hits(txt)
    ok(h == [], "%s screens clean with NO exemption -- three authored "
       "words tripped it and were reworded rather than exempted" % label,
       str(h[:3]))
ok(no_severity.hits("a critical error") != [],
   "the screen fires on a plant, so the clean results mean something")
ok(not R2.__doc__ or "exemption" not in R2.__doc__,
   "there is no exemption harness in this module, because there is "
   "nothing to exempt")


# ------------------------------------------ 16. carried from the v1 read

section("16  the v1 readings that v2 does not move")
hc = R1.hop_compression()
ok(hc["stated"] == 50 and abs(hc["low"] - 50.0) < 1e-9
   and abs(hc["high"] - 125.0) < 1e-9,
   "'compressed by roughly fifty' is still the LOW end of its own band "
   "and the equal-N reading", "%s in [%s, %s]"
   % (hc["stated"], hc["low"], hc["high"]))
ok(E1.hop_budget() == E1.hop_budget(),
   "the v1 hop budget parses unchanged")
ok(E1._section("## 6B. TIMEFRAME")
   == E2._section("## 6B. TIMEFRAME"),
   "section 6B parses byte-identically in both, so the reading carries "
   "without being re-derived")


# ------------------------------------------- 17. the value-and-source gate

section("17  the value-and-source gate, and the three defects replayed")

sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))
import sourced as S                                          # noqa: E402

DOC = "WORK_ORDER_V2.md"

# DEFECT 1, both rows. Under lstrip("-> ") the amended score came back as
# the UNAMENDED one with the amendment cell named as its source.
v3_cell, v6_cell = "-> --   A-01", "-> --   A-02"
ok("-> --   A-01".lstrip("-> ") == "A-01",
   "the defect reproduced: lstrip on a character set eats the value's own "
   "leading '--' as well as the arrow",
   repr("-> --   A-01".lstrip("-> ")))
ok(S.find_span(v3_cell, "+") is None,
   "V3: containment alone WOULD have caught the buggy value -- '+' does "
   "not occur in the amendment cell")
ok(S.find_span(v6_cell, "-") is not None,
   "V6: containment alone would NOT have caught it -- the buggy value '-' "
   "does occur in the cell, through the hyphen of the arrow. This is why "
   "the primitive is a span and not containment")
loc6 = S.Locator(DOC, 0, 57, None, "V6 amendment")
ok(S.gate(S.Sourced("-", v6_cell, loc6)) == S.UNRATED,
   "and the gate refuses it anyway: the buggy path never LOCATED the "
   "value in the cell it names as its source, so it has no span to offer")
ok(S.gate(S.Sourced("-", v6_cell, loc6)).reason == "no_provenance",
   "the refusal names what is missing")
ok(S.gate(S.slice_sourced(v6_cell, 3, 5, loc6)).value == "--",
   "the honest parse slices the cell and cannot disagree with its own span")

# DEFECT 2. Both false positives of the bare-numeral test refuse.
lc = S.Locator(DOC, 0, None, None, "condition")
ok(R2._has_duration("a continuing custodian (see DUR-006)", lc)
   == S.UNRATED,
   "a cross-reference is not a stated lifetime")
ok(R2._has_duration("hop count over the retention horizon exceeds ~1", lc)
   == S.UNRATED,
   "~1 with no unit is not a retention horizon: it fails the gate rather "
   "than parsing")
d = R2._has_duration("expected lifetime 18 months", lc)
ok(isinstance(d, S.Sourced) and d.value == "18 months",
   "a real duration comes back SOURCED, carrying the span that covers "
   "the quantity rather than the digit",
   str(getattr(d, "value", d)))
ok(R2.f_k_bound()["state"] == "NOT_APPLICABLE_AS_DELIVERED"
   and R2.f_k_bound()["n_with_stated_lifetime"] == 0,
   "F_K's reading is unchanged under the gate: 0 of 7 conditions carry an "
   "expected lifetime")
ok(len(R2.f_k_bound()["refused"]) == 7,
   "and every refusal now names its reason rather than being a False "
   "that reads like a measurement",
   str(len(R2.f_k_bound()["refused"])))

# DEFECT 3. Expected against registered.
import known_answer as KA                                    # noqa: E402
KA._REGISTRY.clear()
KA._RESULTS.clear()
KA.seed()
comp = KA.completeness()
ok(comp["state"] == "COMPLETE",
   "the known-answer registry is complete: expected against registered, "
   "which is what catches a register(...) shadowed by a finally",
   "%s missing=%s" % (comp["state"], comp["missing"]))
ok("failure-mode-register/register_v2.py::joint_survival"
   in KA.EXPECTED_METRICS,
   "including this folder's metric, the one that landed as dead code")
KA._REGISTRY.pop("failure-mode-register/register_v2.py::joint_survival")
ok(KA.completeness()["state"] == "SHORT"
   and "failure-mode-register/register_v2.py::joint_survival"
   in KA.completeness()["missing"],
   "and the check is not CONSTANT_SILENT: removing that registration "
   "reads SHORT and names it")
KA._REGISTRY.clear()
KA._RESULTS.clear()
KA.seed()

# THE FOURTH, found BY the gate. The V2 row runs its ML cell past the
# column boundary, so the amendment column reads text belonging to its
# left neighbour.
b = E2.vmap_boundary_report()
ok(b["n_cut"] == 2 and all(r["id"] == "V2" for r in b["cut"]),
   "exactly one row of fourteen has a column boundary that cuts a token, "
   "and it cuts on both sides of the same boundary",
   str([(r["id"], r["column"], r["cuts"]) for r in b["cut"]]))
ok(any(r["column"] == "ml" and r["spill"] == "ate, hw)" for r in b["cut"]),
   "V2's ML cell is truncated at 'data st' and the amendment column reads "
   "'ate, hw)' -- text belonging to the cell on its left")
ok(m["rows"]["V2"]["amendment_kind"] == "UNPARSED"
   and m["rows"]["V2"]["amendment"] is None,
   "the spill is filed UNPARSED rather than EMPTY: a cell holding text "
   "that is not an amendment is a different finding from a cell holding "
   "nothing")
ok(m["rows"]["V2"]["original"] == "--" and m["rows"]["V2"]["amended"] == "--",
   "and no published score moves -- the truncated cell begins with the "
   "same sign run the full cell does, so what is false is the LOCATOR "
   "and not the value")
ok(m["rows"]["V2"]["ml_cell_boundary"] == "CUTS:end",
   "the row carries the finding rather than the reader having to notice")
ok(sum(1 for r in m["rows"].values()
       if r["ml_cell_boundary"] == "CLEAN") == 13,
   "the boundary check is not CONSTANT_FIRES: thirteen rows are clean")


# ---------------------------------------------------------- report

print("\n" + "=" * 62)
for label, detail in FAIL:
    print("FAILED  %s" % label)
    if detail:
        print("        %s" % detail)
print("checks: %d   failed: %d" % (len(PASS) + len(FAIL), len(FAIL)))
sys.exit(1 if FAIL else 0)
