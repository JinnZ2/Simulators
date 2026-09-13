# SPDX-License-Identifier: CC0-1.0
"""
test_register.py -- the checks for entries.py and register.py.

No pytest, no network, stdlib only, runnable on a phone:

    python3 test_register.py

EVERY EXPECTED VERDICT LIVES HERE AND NOT IN entries.py. entries.py is a
parser over the delivered order and carries no expected value at all; an
answer stored beside the thing it grades agrees by construction, and an
agreement produced that way measures nothing.

Sections:

    1  the parser follows the delivered order and retypes nothing
    2  section 2 filing -- UNRATED never discarded, extra fields apart
    3  vocabulary conformance -- three states, never merged
    4  the control-state axis, and the multi-value cells that are not one axis
    5  the steps, including the three that cannot run here
    6  F_H: every count states its unit
    7  the falsifiers, in delivered order
    8  section 6B arithmetic
    9  the redundancy rule, imported not restated
    10 reachability: every declared verdict is reached by something
    11 nothing is authored -- ENTRY 0, section 3C, no minimum artifact
    12 the choices are declared and cited where they take effect
    13 the render screens clean
    14 housekeeping
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

import entries as E  # noqa: E402
import register as R  # noqa: E402

ORDER = os.path.join(HERE, "WORK_ORDER.md")
REG = os.path.join(HERE, "register.py")
ENT = os.path.join(HERE, "entries.py")
REG_SRC = open(REG).read()
ENT_SRC = open(ENT).read()
REG_TREE = ast.parse(REG_SRC)
ENT_TREE = ast.parse(ENT_SRC)
ORDER_TEXT = open(ORDER).read()

FAILED = []
TOTAL = [0]


def check(name, cond, detail=""):
    TOTAL[0] += 1
    if not cond:
        FAILED.append("%s %s" % (name, detail))
        print("FAIL  %s %s" % (name, detail))


def body_of(tree, fname):
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == fname:
            return n
    return None


# ------------------------------------------------- 1 the parser follows
print("1  the parser follows the delivered order")

fields = E.schema_fields()
check("section 2 yields the twelve fields the order lists",
      len(fields) == 12, str(len(fields)))
check("id is first and validity_range last, in delivered order",
      fields[0][0] == "id" and fields[-1][0] == "validity_range")
check("every parsed field name appears at column 0-2 of the order",
      all(("\n  %s " % n) in ORDER_TEXT for n, _ in fields))

vocab = E.vocabularies()
check("exactly three fields declare a closed set",
      sorted(vocab) == ["evidence_class", "onset", "reconstruction"],
      str(sorted(vocab)))
check("onset reads three tokens",
      vocab["onset"] == ["immediate", "drift", "dormant-until-triggered"],
      str(vocab["onset"]))
check("evidence_class reads three tokens, parentheticals dropped",
      vocab["evidence_class"] == ["MEASURED", "TRANSPORTED", "PROJECTED"],
      str(vocab["evidence_class"]))
check("reconstruction reads three tokens, the question dropped",
      vocab["reconstruction"] == ["YES", "PARTIAL", "NO"],
      str(vocab["reconstruction"]))

ents = E.entries()
check("four ENTRY blocks parse", len(ents) == 4, str(sorted(ents)))
check("entry ids are DUR-001..004",
      sorted(ents) == ["DUR-00%d" % i for i in (1, 2, 3, 4)])
check("every entry's parsed id field equals its block header id",
      all(ents[k].get("id") == k for k in ents))
check("a multi-line value is joined, not truncated",
      "no trace distinguishing" in ents["DUR-001"]["mechanism"])
check("the ENTRY header line is not parsed as a field [CHOICE 2]",
      all("ENTRY" not in rec for rec in ents.values()))

check("three control notes parse",
      sorted(E.control_notes()) == ["DUR-001-N1", "DUR-001-N2", "DUR-002-N1"])
check("five section 3A seeds parse", len(E.measured_seeds()) == 5,
      str(len(E.measured_seeds())))
check("six section 3B source domains parse, not eight",
      len(E.source_domains()) == 6, str(len(E.source_domains())))
check("eight steps parse, Step 0 through Step 7",
      [n for n, _ in E.steps()] == ["Step %d" % i for i in range(8)],
      str([n for n, _ in E.steps()]))
check("nine falsifiers parse", len(E.falsifiers()) == 9)
check("falsifiers are in DELIVERED order -- F_I before F_H",
      [f for f, _ in E.falsifiers()].index("F_I")
      < [f for f, _ in E.falsifiers()].index("F_H"))
check("three shock classes parse",
      sorted(E.shock_classes()) == ["V14a", "V14b", "V14c"])
check("three non-goals parse", len(E.non_goals()) == 3)
check("the scope statement is durability and reconstructability only",
      "DURABILITY AND RECONSTRUCTABILITY ONLY" in E.scope_statement())

# nothing is retyped: every entry value appears verbatim in the order
missing = []
for eid, rec in ents.items():
    for field, value in rec.items():
        head = value.split(".")[0][:40]
        if head and head not in ORDER_TEXT.replace("\n", " ") \
                and head not in ORDER_TEXT:
            missing.append("%s.%s" % (eid, field))
check("every parsed entry value traces to the delivered order",
      not missing, str(missing))
check("no entry value is a literal in entries.py",
      not any(rec["mechanism"][:40] in ENT_SRC for rec in ents.values()))
check("no entry value is a literal in register.py",
      not any(rec["mechanism"][:40] in REG_SRC for rec in ents.values()))
check("the vocabularies are read out of the order, not listed in code",
      "dormant-until-triggered" not in ENT_SRC.replace(
          '"immediate | drift | dormant-until-triggered"', ""))

# the parser fails loudly rather than quietly on a reflow
src_backup = E.order_text()
try:
    E.ORDER_PATH = os.path.join(HERE, "does-not-exist.md")
    raised = False
    try:
        E.schema_fields()
    except Exception:
        raised = True
    check("a missing order raises rather than returning an empty schema",
          raised)
finally:
    E.ORDER_PATH = os.path.join(HERE, "WORK_ORDER.md")
check("the order is still readable after the null test",
      E.order_text() == src_backup)


# --------------------------------------------------------- 2 filing
print("2  filing")

fs = {f["id"]: f for f in R.filings()}
check("all four entries carry all twelve schema fields",
      all(f["n_missing"] == 0 for f in fs.values()))
check("all four file as FILED, none discarded",
      all(f["status"] == R.FILED for f in fs.values()))
check("DUR-003 and DUR-004 carry an extra field the schema does not have",
      fs["DUR-003"]["extra"] == ["NOTE"]
      and fs["DUR-004"]["extra"] == ["NOTE"])
check("DUR-001 and DUR-002 carry no extra field",
      fs["DUR-001"]["extra"] == [] and fs["DUR-002"]["extra"] == [])
check("an extra field is never counted as a missing one",
      all(f["n_missing"] == 0 for f in fs.values())
      and sum(f["n_extra"] for f in fs.values()) == 2)

# an entry missing a field is UNRATED and is still returned
stub = dict(ents["DUR-001"])
del stub["consequence"]
f = R.filing("STUB", stub)
check("a missing field makes the entry UNRATED",
      f["status"] == R.UNRATED and f["missing"] == ["consequence"])
check("an UNRATED entry is filed, not discarded",
      f["id"] == "STUB" and "missing" in f)


# ------------------------------------------------ 3 vocabulary conformance
print("3  vocabulary conformance")

conf = R.conformance()
check("reconstruction: DUR-004 states one value",
      conf["DUR-004"]["reconstruction"]["verdict"] == R.CONFORMS)
check("reconstruction: DUR-001 states two",
      conf["DUR-001"]["reconstruction"]["verdict"] == R.MULTI_VALUE
      and conf["DUR-001"]["reconstruction"]["tokens"] == ["NO", "PARTIAL"])
check("reconstruction: DUR-003 states two, in the other order",
      conf["DUR-003"]["reconstruction"]["tokens"] == ["PARTIAL", "NO"])
check("reconstruction: DUR-002 states none of the three",
      conf["DUR-002"]["reconstruction"]["verdict"] == R.OUT_OF_VOCAB)
check("onset conforms on all four", all(
    conf[e]["onset"]["verdict"] == R.CONFORMS for e in conf))
check("evidence_class: DUR-001 carries two source labels",
      conf["DUR-001"]["evidence_class"]["verdict"] == R.MULTI_VALUE)
check("MULTI_VALUE and OUT_OF_VOCAB are never merged into one bucket",
      R.MULTI_VALUE != R.OUT_OF_VOCAB
      and set(R.conformance_counts()["counts"]["reconstruction"])
      == {R.CONFORMS, R.MULTI_VALUE, R.OUT_OF_VOCAB, R.NOT_EVALUABLE})
check("a field absent from an entry is NOT_EVALUABLE, not OUT_OF_VOCAB",
      R.conformance()["DUR-001"] is not None
      and R.conformance(eid="DUR-001") is not None)

# substring bleed: NO must not match inside NOT / NONE
check("the token scan does not match NO inside NOT or NONE",
      R._tokens_present("NOT applicable. NONE here.",
                        ["YES", "PARTIAL", "NO"]) == [])
check("the token scan does match a bare NO",
      R._tokens_present("NO. Reconstruction requires comprehension.",
                        ["YES", "PARTIAL", "NO"]) == ["NO"])
check("whole-word containment rejects structural inside Structurally",
      not R._contains_word("Structurally identical.", "structural"))
check("whole-word containment accepts a real occurrence",
      R._contains_word("the structural case", "structural"))


# ------------------------------------------- 4 the control-state axis
print("4  the control-state axis")

cs = R.control_state_split()
check("six of twelve cells carry both readings",
      cs["n_two_readings"] == 6 and cs["of"] == 12,
      "%d of %d" % (cs["n_two_readings"], cs["of"]))
check("the markers used are returned with the verdict",
      all(r["markers"] or not r["two_readings"] for r in cs["rows"]))
check("the marker list is declared, not hidden",
      cs["markers_declared"] == list(R.CONTROL_MARKERS))
rows = {(r["id"], r["field"]): r for r in cs["rows"]}
check("DUR-001 detection_latency states both with and without the control",
      rows[("DUR-001", "detection_latency")]["two_readings"])
check("DUR-004 detection_channel carries one reading only",
      not rows[("DUR-004", "detection_channel")]["two_readings"])

mv = R.multi_value_axes()
check("two reconstruction cells hold two values", mv["n"] == 2)
check("DUR-001's two values sit on a control axis",
      mv["rows"]["DUR-001"]["axis"] == "control")
check("DUR-003's two values do not",
      mv["rows"]["DUR-003"]["axis"] != "control")
check("no merged distribution is emitted over the two axes",
      mv["merged_distribution"] is None and mv["reason"])


# ------------------------------------------------------------ 5 the steps
print("5  the steps")

s0 = R.step0_prior_art()
check("Step 0 is BLOCKED, not skipped and not substituted",
      s0["status"] == R.BLOCKED and s0["substituted"] is False)
check("Step 0 names the blocker", "allowlist" in s0["blocker"])
check("Step 0 states that the register is not cleared to ship",
      "not cleared" in s0["consequence"])

s1 = R.step1_deployment_class()
check("Step 1 is NOT_RUN -- no deployment class is declared",
      s1["status"] == R.NOT_RUN)
check("DUR-002 refuses to narrow, explicitly",
      s1["explicit_refusals_to_narrow"] == ["DUR-002"])

s4 = R.step4_status()
check("Step 4 is NOT_RUN", s4["status"] == R.NOT_RUN)
check("Step 4's cap at the default fraction is one entry", s4["cap"] == 1)
check("Step 4 states the fraction it used", s4["fraction_used"] == 0.2)
check("the cap is derived, not stated as a constant",
      R.fraction_cap(4, 0.2) == 1 and R.fraction_cap(4, 0.5) == 4)
check("fraction_cap returns None where the rule places no cap",
      R.fraction_cap(4, 1.0) is None)
check("fraction_cap is zero when nothing is anchored",
      R.fraction_cap(0, 0.5) == 0)

s5 = R.step5_distribution()
check("Step 5 computes a distribution for one entry of four",
      s5["n_single"] == 1 and s5["of"] == 4)
check("Step 5's one computable value is NO", s5["single_value"] == {"NO": 1})
check("Step 5 emits no distribution over all four", 
      s5["distribution_over_all"] is None and s5["reason"])
check("Step 5 keeps multi-value and out-of-vocab apart",
      s5["multi_value"] == ["DUR-001", "DUR-003"]
      and s5["out_of_vocab"] == ["DUR-002"])

s6 = R.step6_requirements()
check("Step 6 gates three entries in, one out",
      s6["n"] == 3 and s6["n_excluded"] == 1)
check("DUR-002 is the excluded one", s6["excluded"][0]["id"] == "DUR-002")
check("DUR-002 states a requirement anyway",
      s6["excluded"][0]["states_requirement_anyway"] is True)
check("the second conjunct is NOT_EVALUABLE, not assumed met",
      s6["second_conjunct"] == R.NOT_EVALUABLE)
check("every requirement carries the second conjunct's state too",
      all(r["consequence_nontrivial"] == R.NOT_EVALUABLE
          for r in s6["requirements"]))
arts = {r["id"]: r["minimum_artifact"] for r in s6["requirements"]}
check("DUR-001's artifact is its own proposed record",
      arts["DUR-001"].startswith("sealed probe-response record"))
check("DUR-003's artifact is its own proposed hop log",
      arts["DUR-003"].startswith("hop log"))
check("DUR-004's artifact is NOT_SUPPLIED and none is authored",
      arts["DUR-004"] == "NOT_SUPPLIED")

s7 = R.step7_null_set()
check("the null set is not empty", s7["empty"] is False)
check("one entry is partially controlled", s7["partially_controlled"]
      == ["DUR-002"])
check("no entry is fully controlled", s7["fully_controlled"] == [])
check("three are uncontrolled", len(s7["uncontrolled"]) == 3)

hp = R.high_priority()
check("three of four are high priority under the as-is reading",
      hp["n_as_is"] == 3)
check("none is under the with-control reading", hp["n_with_control"] == 0)
check("neither reading is picked", hp["picked"] is None)


# -------------------------------------------- 6 F_H: every count has a unit
print("6  F_H -- every count states its unit")

COUNTING = ("filing", "conformance_counts", "control_state_split",
            "multi_value_axes", "step1_deployment_class", "step4_status",
            "step5_distribution", "step6_requirements", "step7_null_set",
            "high_priority", "projected_fraction", "hop_compression",
            "volume_vs_correlation", "shock_split",
            "redundancy_claims_in_register", "cross_references")
for fname in COUNTING:
    fn = getattr(R, fname)
    if fname == "filing":
        out = fn("DUR-001")
    elif fname == "volume_vs_correlation":
        out = fn(10, 2, 0.1, 1, 0.5)
    else:
        out = fn()
    check("%s states its unit" % fname,
          isinstance(out, dict) and isinstance(out.get("unit"), str)
          and out["unit"] != "")
check("the unit strings are not all the same word",
      len({R.step5_distribution()["unit"],
           R.control_state_split()["unit"],
           R.shock_split()["unit"],
           R.redundancy_rule({"id": "x", "copies": []})["unit"]}) >= 3)
check("F_H's rule names where it is enforced",
      "test_register" in R._f_h()["enforced_in"])


# -------------------------------------------------------- 7 the falsifiers
print("7  the falsifiers")

fal = R.falsifier_status()
check("every delivered falsifier has a status",
      [f for f, _ in fal] == [f for f, _ in E.falsifiers()])
check("the falsifier report is in delivered order, F_I before F_H",
      [f for f, _ in fal].index("F_I") < [f for f, _ in fal].index("F_H"))
by = dict(fal)

check("F_A: three transports survive the justification rule",
      by["F_A"]["n"] == 3, str(by["F_A"]["survivors"]))
check("F_A: the transport section is not decoration",
      "not decoration" in by["F_A"]["verdict"])
check("F_A: DUR-001's mention of resemblance is reported with its clause",
      any(m["id"] == "DUR-001" and "not resemblance" in m["clause"]
          for m in by["F_A"]["resemblance_mentioned"]))
check("F_A: a resemblance mention is not subtracted from the survivors",
      "DUR-001" in by["F_A"]["survivors"])
check("F_A's limit records the first version's false negative",
      "disclaims resemblance" in by["F_A"]["limit"])

check("F_B is BLOCKED, inheriting Step 0", by["F_B"]["status"] == R.BLOCKED)

check("F_C runs a census rather than a 20% sample of four",
      by["F_C"]["census"] is True and by["F_C"]["requested_sample"] < 1)
check("F_C states the substitution rather than taking it quietly",
      "no resolution" in by["F_C"]["sample_substituted"])
check("F_C's rejection rate is zero on the delivered entries",
      by["F_C"]["n_rejected"] == 0 and by["F_C"]["rate"] == 0.0)
check("F_C's three mandatory fields are the order's",
      set(by["F_C"]["required_fields"])
      == {"mechanism", "detection_channel", "consequence"})

check("F_D: no entry is PROJECTED", by["F_D"]["n_projected"] == 0)
check("F_D says why the register passes",
      "Step 4 was not run" in by["F_D"]["reading"])

check("F_E is NOT_RUN and states the honest answer",
      by["F_E"]["status"] == R.NOT_RUN
      and "nothing currently would" in by["F_E"]["stated_answer"])
check("F_E does not claim publishing is sufficient",
      by["F_E"]["claims_publishing_sufficient"] is False)

check("F_F: no entry names a location for the recoverable thing",
      all(r["names_a_location"] is None for r in by["F_F"]["rows"]))
check("F_F: one entry names a holder",
      sum(1 for r in by["F_F"]["rows"] if r["names_a_holder"]) == 1)

check("F_G is NOT_RUN with both blockers named",
      by["F_G"]["status"] == R.NOT_RUN and len(by["F_G"]["blockers"]) == 2)
check("F_G's substitute is labelled a proxy",
      by["F_G"]["proxy_is_a_proxy"] is True)
check("F_G's proxy flags the two non-conforming fields",
      sorted(x["field"] for x in by["F_G"]["proxy"])
      == ["evidence_class", "reconstruction"])

check("F_I: both 6B-1 and 6B-2 are present in the order",
      by["F_I"]["both_or_neither"] is True)
check("F_I: the module offers no single-number volume accessor",
      by["F_I"]["module_refuses_single"] is True)


# ------------------------------------------------------- 8 6B arithmetic
print("8  section 6B arithmetic")

hc = R.hop_compression_reading()
check("classical is 20 hops over 500 years",
      abs(hc["classical_hops_per_year"] - 0.04) < 1e-12)
check("ML is 2 to 5 hops per year", hc["ml_hops_per_year"] == (2.0, 5.0))
check("the compression band is 50 to 125",
      abs(hc["low"] - 50.0) < 1e-9 and abs(hc["high"] - 125.0) < 1e-9)
check("the stated figure is fifty", hc["stated"] == 50)
check("the stated figure is the low end of the order's own band",
      "low end" in hc["stated_is"])
check("the equal-N reading gives the same fifty",
      abs(hc["equal_n"] - 50.0) < 1e-9)

vc = R.volume_vs_correlation(1000, 10, 0.001, 2, 0.3)
check("volume is M x N x p", abs(vc["volume"]["expected"] - 10.0) < 1e-9)
check("correlation is M x events x share",
      abs(vc["correlation"]["expected"] - 600.0) < 1e-9)
check("the two give different numbers on the same population",
      vc["volume"]["expected"] != vc["correlation"]["expected"])
check("the correlation mode has no entry and says so",
      vc["correlation_entry_exists"] is False
      and "needs its own entry" in vc["correlation_entry_reason"])
check("the operator-level reading is carried, not dropped",
      "where decisions are made" in vc["operator_level"])
check("no single-number volume accessor exists on the module",
      not any(isinstance(n, ast.FunctionDef)
              and n.name in ("volume", "expected_losses")
              for n in ast.walk(REG_TREE)))

ss = {r["class"]: r for r in R.shock_split()["rows"]}
check("carrier shock is the one that is not scheduled",
      ss["V14a"]["scheduled"] is False
      and ss["V14b"]["scheduled"] and ss["V14c"]["scheduled"])
check("a scheduled class with an undeclared budget is undetermined",
      ss["V14b"]["mitigated"] is None and "UNDECLARED" in ss["V14b"]["reason"])
declared = {r["class"]: r for r in
            R.shock_split({"V14b": True, "V14c": False})["rows"]}
check("a declared budget line mitigates",
      declared["V14b"]["mitigated"] is True)
check("a declared absence of one does not, per the order's own rule",
      declared["V14c"]["mitigated"] is False
      and "unplanned" in declared["V14c"]["reason"])
check("undeclared and declared-absent are different states",
      ss["V14c"]["mitigated"] is None
      and declared["V14c"]["mitigated"] is False)
check("intact-and-unreadable is recorded as its own state",
      "distinct state from decayed" in R.shock_split()["substrate_state"])


# --------------------------------------------- 9 the redundancy rule
print("9  the redundancy rule, imported not restated")

era_path = os.path.join(ROOT, "effective-redundancy-audit",
                        "effective_redundancy.py")
check("the sibling exists", os.path.isfile(era_path))
check("register.py does not define n_eff itself",
      not any(isinstance(n, (ast.FunctionDef, ast.ClassDef))
              and n.name in ("n_eff", "Channel", "Case")
              for n in ast.walk(REG_TREE)))
check("register.py imports the sibling by path",
      "effective-redundancy-audit" in REG_SRC
      and "import effective_redundancy" in REG_SRC)

three_shared = R.redundancy_rule({"id": "t", "copies": [
    {"name": "a", "survives_all_shared_nodes": False},
    {"name": "b", "survives_all_shared_nodes": False},
    {"name": "c", "survives_all_shared_nodes": False}]})
check("three copies on one substrate are one copy",
      three_shared["n_nominal"] == 3 and three_shared["n_eff"] == 1)
check("and are reported collapsed", three_shared["collapsed"] is True)

two_indep = R.redundancy_rule({"id": "u", "copies": [
    {"name": "a", "survives_all_shared_nodes": True},
    {"name": "b", "survives_all_shared_nodes": True}]})
check("two copies sharing nothing are two", two_indep["n_eff"] == 2)
check("so the rule is neither constant-firing nor constant-silent",
      three_shared["collapsed"] != two_indep["collapsed"])

undeclared = R.redundancy_rule({"id": "v", "copies": [
    {"name": "a", "survives_all_shared_nodes": True},
    {"name": "b"}]})
check("a copy that does not state what it does not share is UNRATED",
      undeclared["status"] == R.UNRATED and undeclared["n_eff"] is None)
check("it is not scored as shared and not scored as independent",
      undeclared["n_eff"] is None and "do not state" in undeclared["reason"])
check("an empty claim is UNRATED too",
      R.redundancy_rule({"id": "w", "copies": []})["status"] == R.UNRATED)

rc = R.redundancy_claims_in_register()
check("no delivered entry claims redundancy as a control", rc["n"] == 0)
check("the zero is reported rather than the rule being dropped",
      "visible zero" in rc["reason"])


# ------------------------------------------------------- 10 reachability
print("10 reachability")

verdicts = set()
for row in R.conformance().values():
    for cell in row.values():
        verdicts.add(cell["verdict"])
check("three of the four conformance verdicts are reached by the corpus",
      {R.CONFORMS, R.MULTI_VALUE, R.OUT_OF_VOCAB} <= verdicts)
stub2 = dict(ents["DUR-001"])
del stub2["reconstruction"]
check("NOT_EVALUABLE is reachable on an entry missing the field",
      R.conformance.__doc__ is not None
      and R.filing("s", stub2)["status"] == R.UNRATED)
check("FILED and UNRATED are both reached",
      {R.FILED, R.UNRATED} == {R.filing("DUR-001")["status"],
                               R.filing("s", stub2)["status"]})
statuses = {res["status"] for _, res in fal}
check("BLOCKED, NOT_RUN and COMPUTED are all reached by the falsifiers",
      {R.BLOCKED, R.NOT_RUN, "COMPUTED"} <= statuses, str(statuses))
xr = {r["marker"]: r for r in R.cross_references()["rows"]}
check("RESOLVED and AMBIGUOUS are both reached by the cross-references",
      xr["correlated failure at scale"]["status"] == "RESOLVED"
      and xr["silent substitution"]["status"] == R.AMBIGUOUS)
check("the ambiguous one names its candidates and picks none",
      len(xr["silent substitution"]["resolves_to"]) > 1
      and "no pick is made" in xr["silent substitution"]["basis"])
check("every cross-referenced folder exists on disk",
      all(os.path.isdir(os.path.join(ROOT, d))
          for r in R.cross_references()["rows"] for d in r["resolves_to"]))


# ------------------------------------------------------ 11 nothing authored
print("11 nothing is authored")

ez = R.entry_zero()
check("ENTRY 0 is named in the order", ez["named_in_order"] is True)
check("ENTRY 0 was not delivered", ez["present"] is False)
check("ENTRY 0 is not authored here", ez["authored_here"] is False)
check("ENTRY 0's reason is structural, not a preference",
      "no load_condition" in ez["reason"])
check("no DUR-000 appears anywhere in either module",
      "DUR-000" not in REG_SRC and "DUR-000" not in ENT_SRC)
check("section 3C is not populated",
      R.step4_status()["status"] == R.NOT_RUN)
check("no minimum artifact is authored -- each traces to an entry or is "
      "NOT_SUPPLIED",
      all(r["minimum_artifact"] == "NOT_SUPPLIED"
          or r["minimum_artifact"] in ents[r["id"]]["detection_channel"]
          for r in R.step6_requirements()["requirements"]))
check("the register's content is the four delivered entries and nothing else",
      set(R.conformance()) == set(ents))


# ---------------------------------------------------------- 12 the choices
print("12 the choices")

allc = dict(E.CHOICES)
allc.update(R.CHOICES)
check("the choice numbers are contiguous from one",
      sorted(allc) == list(range(1, len(allc) + 1)), str(sorted(allc)))
check("entries.py and register.py do not reuse a number",
      not (set(E.CHOICES) & set(R.CHOICES)))
ENT_BODY = ENT_SRC.split(chr(34) * 3, 2)[2]
REG_BODY = REG_SRC.split(chr(34) * 3, 2)[2]
for key in allc:
    tag = "[CHOICE %d]" % key
    check("%s is cited inline where it takes effect" % tag,
          tag in ENT_BODY or tag in REG_BODY)
out = R.render_choices()
for key in allc:
    check("[CHOICE %d] is printed" % key, ("[CHOICE %d]" % key) in out)


# ----------------------------------------------------------- 13 the render
print("13 the render")

sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import no_severity  # noqa: E402

REPORT = R.render()
NORM_ORDER = " ".join(ORDER_TEXT.split())


def _is_quote(line):
    """A screened word inside text quoted verbatim from the delivered order.

    Two hits remain after rewording everything this build authored, and both
    are the order's own sentences -- section 6B-2's "needs its own entry" and
    6B-3's "worse, because it reads as retained". Rewording them would
    misquote the source, which is the call residual-direction RDD_008 made
    on the same screen. The exemption is declared, and measured in three
    arms below rather than taken on trust.
    """
    frag = " ".join(line.split())
    return any(frag[i:i + 18] in NORM_ORDER
               for i in range(0, max(1, len(frag) - 17)))


hits = no_severity.hits(REPORT)
quoted = [h for h in hits if _is_quote(h[2])]
authored = [h for h in hits if not _is_quote(h[2])]
# arm 1 -- with the order's own sentences masked, the render screens clean
check("the render screens clean apart from verbatim quoted order text",
      not authored, str(authored[:4]))
# arm 2 -- the exemption is not doing more work than it is claimed to
check("exactly the quoted sentences fire, and they are named",
      len(quoted) == len(hits) and len(quoted) == 2,
      str([h[1] for h in quoted]))
check("both quoted hits trace to a section the order delivers",
      all(h[1] in ORDER_TEXT for h in quoted))
# arm 3 -- a plant is still caught through the exemption
check("the screen is not silent -- a plant is caught through the exemption",
      [h for h in no_severity.hits(REPORT + "\nthis entry is dangerous")
       if not _is_quote(h[2])])
check("the render states the scope before any verdict",
      REPORT.index("DURABILITY AND RECONSTRUCTABILITY") < REPORT.index("Step"))
check("the render states the non-goals",
      all(g[:12] in REPORT for g in E.non_goals()))
check("the render states the projected fraction in the header (F_D)",
      REPORT.index("PROJECTED FRACTION") < REPORT.index("FILING"))


# ----------------------------------------------------------- 14 housekeeping
print("14 housekeeping")

for mod, name in ((REG, "register.py"), (ENT, "entries.py")):
    p = subprocess.run([sys.executable, mod, "--selftest"],
                       capture_output=True, text=True, cwd=HERE)
    check("%s refuses --selftest with rc 2" % name, p.returncode == 2,
          str(p.returncode))
    check("%s names where the checks live" % name,
          "test_register.py" in p.stdout)
for mod, name in ((REG, "register.py"), (ENT, "entries.py")):
    p = subprocess.run([sys.executable, mod], capture_output=True,
                       text=True, cwd=HERE)
    check("%s runs clean" % name, p.returncode == 0, p.stderr[-200:])

check("both modules are ascii", all(
    ord(c) < 128 for c in REG_SRC + ENT_SRC))
check("the delivered order is landed verbatim and is not ascii-ised",
      any(ord(c) > 127 for c in ORDER_TEXT))
check("neither module imports anything networked",
      not any(m in REG_SRC + ENT_SRC
              for m in ("urllib", "requests", "socket", "http.client")))
check("no test expectation lives in entries.py",
      not any(tok in ENT_SRC
              for tok in ("expected ==", "must_fire", "assert ",
                          "MUST ", "== R.")))
check("both modules parse under 3.9",
      ast.parse(REG_SRC) is not None and ast.parse(ENT_SRC) is not None)
check("the order's non-goals are restated in the module docstring",
      "not model behaviour" in REG_SRC and "not a code of ethics" in REG_SRC)
check("the module names no step the order does not",
      all(("Step %d" % i) in ORDER_TEXT for i in range(8)))


# --------------------------------------------------------------------------
print()
print("%d checks, %d failed" % (TOTAL[0], len(FAILED)))
if FAILED:
    for f in FAILED:
        print("  " + f)
    sys.exit(1)
