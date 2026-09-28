"""WO-2 suite. Prints its own count; nothing here is stored elsewhere."""
import ast
import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decomposition as dc     # noqa: E402
import evidence as ev          # noqa: E402
import ownability as ow        # noqa: E402
import blind_coding as bc      # noqa: E402

N = 0
FAILED = []
ORDER_TEXT = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()


def check(name, ok):
    global N
    N += 1
    print("  %s  %s" % ("ok  " if ok else "FAIL", name))
    if not ok:
        FAILED.append(name)


def section(t):
    print("\n== " + t)


# ------------------------------------------------------------ decomposition
section("decomposition: parts parsed, classes reachable, absent kept from unsearched")
P = dc.parts()
check("four parts parsed from the order", len(P) == 4 and P[0].startswith("The signal exists"))
try:
    dc.parts(ORDER_TEXT.replace("3. No one is assigned the JOIN.", "No one is assigned the JOIN."))
    check("a retyped copy holding three parts raises", False)
except ValueError:
    check("a retyped copy holding three parts raises", True)
full = {"signal_present": "PRESENT", "signal_reported": "PRESENT", "join_assigned": "UNASSIGNED"}
check("signalled, reported, unassigned -> SIGNALLED_UNJOINED", dc.classify(full)["state"] == "SIGNALLED_UNJOINED")
check("join ASSIGNED -> SIGNALLED_JOINED (counter-case to part 3)", dc.classify(dict(full, join_assigned="ASSIGNED"))["state"] == "SIGNALLED_JOINED")
check("signal ABSENT (searched) -> GENUINELY_UNSIGNALLED", dc.classify(dict(full, signal_present="ABSENT"))["state"] == "GENUINELY_UNSIGNALLED")
check("reported ABSENT -> REPORTED_NOWHERE, part 1 does not hold", dc.classify(dict(full, signal_reported="ABSENT"))["state"] == "REPORTED_NOWHERE")
check("a missing signal_present reads UNSEARCHED -> NOT_EVALUABLE naming it, never ABSENT", dc.classify({"signal_reported": "PRESENT"}) == {"state": "NOT_EVALUABLE", "lacks": ["signal_present"]})
check("UNSEARCHED join -> NOT_EVALUABLE naming join_assigned", dc.classify(dict(full, join_assigned="UNSEARCHED"))["lacks"] == ["join_assigned"])
check("ABSENT and UNSEARCHED on one field give different classes", dc.classify(dict(full, signal_present="ABSENT"))["state"] != dc.classify(dict(full, signal_present="UNSEARCHED"))["state"])
check("a value outside the vocabulary is MALFORMED", dc.classify(dict(full, signal_present="yes"))["state"] == "MALFORMED")
check("non-dict is MALFORMED", dc.classify("x")["state"] == "MALFORMED")
check("every class in CLASSES is reachable", {dc.classify(r)["state"] for r in [full, dict(full, join_assigned="ASSIGNED"), dict(full, signal_present="ABSENT"), dict(full, signal_reported="ABSENT"), {}, "x"]} == set(dc.CLASSES))
check("holder_count: int kept, missing UNDECLARED, bool MALFORMED, negative MALFORMED", (dc.holder_count({"holder_count": 3}), dc.holder_count({}), dc.holder_count({"holder_count": True}), dc.holder_count({"holder_count": -1})) == (3, "UNDECLARED", "MALFORMED", "MALFORMED"))
check("lead_time: a number with no unit is UNDECLARED, with a unit it is kept", dc.lead_time({"time_first_signal_to_event": 14}) == "UNDECLARED" and dc.lead_time({"time_first_signal_to_event": {"value": 14, "unit": "month"}}) == {"value": 14, "unit": "month"})
CC = dc.constructed_corpus()
check("separation SEPARATES on the constructed corpus built to", dc.separation(CC["separates"])["state"] == "SEPARATES")
check("separation DOES_NOT_SEPARATE when a SUDDEN case is unsignalled", dc.separation(CC["does_not"])["state"] == "DOES_NOT_SEPARATE")
check("separation NOT_EVALUABLE when the signal axis has one level (CONSTANT_FIRES guard)", dc.separation(CC["one_level"])["state"] == "NOT_EVALUABLE" and "one level" in dc.separation(CC["one_level"])["why"])
check("separation on an empty corpus is NOT_EVALUABLE, not a verdict", dc.separation([])["state"] == "NOT_EVALUABLE")
check("NOT_EVALUABLE and MALFORMED cases are skipped and counted, not tabled", dc.separation([{}, "x"] + CC["separates"])["skipped"] == {"NOT_EVALUABLE": 1, "MALFORMED": 1, "UNDECLARED_description": 0})
check("an undeclared description is skipped and counted apart", dc.separation([dict(full, described_as="UNDECLARED")] + CC["separates"])["skipped"]["UNDECLARED_description"] == 1)
check("separation carries its rule and [CHOICE 1]", "[CHOICE 1" in dc.separation(CC["separates"])["rule"])
check("base_rate REFUSES on any corpus, naming the frame and what lifts it", dc.base_rate(CC["separates"])["state"] == "REFUSED_SAMPLING_FRAME" and "lifts_on" in dc.base_rate([]))
src = open(os.path.join(HERE, "decomposition.py")).read()
fn = [n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "base_rate"][0]
check("base_rate divides nothing (AST: no Div in it)", not any(isinstance(x, ast.Div) for x in ast.walk(fn)))
OC = dc.order_cases()
check("four cases parsed from the order, CARRIED", len(OC) == 4 and all(c["status"] == "CARRIED_NOT_VERIFIED" for c in OC))
check("case names parsed: SILVER BRIDGE, COLUMBIA, TACOMA NARROWS, QUIET FAILURE CLASS", [c["name"] for c in OC] == ["SILVER BRIDGE", "COLUMBIA", "TACOMA NARROWS", "QUIET FAILURE CLASS"])
try:
    dc.order_cases(ORDER_TEXT.replace("## Cases", "## Case"))
    check("a text without the Cases section raises", False)
except ValueError:
    check("a text without the Cases section raises", True)
K = dc.carried_codings()
bodies = {c["name"]: c["body"] for c in OC}
check("four codings, every one declares saw_decomposition True", len(K) == 4 and all(k["saw_decomposition"] is True for k in K))
check("every basis span slices a non-empty phrase out of its own case body", all(bodies[k["case"]][s[0]:s[1]] for k in K for s in k["basis"].values()))
check("every coded signal/join field with a value carries a basis span", all(f in k["basis"] for k in K for f in ("signal_present", "signal_reported", "join_assigned") if k[f] != "UNSEARCHED"))
KS = {k["case"]: dc.classify(k) for k in K}
check("the order's anchor case codes REPORTED_NOWHERE from its own sentence: part 1 does not hold on it", KS["SILVER BRIDGE"]["state"] == "REPORTED_NOWHERE")
check("the anchor's described_as is UNDECLARED: 'in under a minute' is an event duration, not a description", K[0]["described_as"] == "UNDECLARED" and "event_duration" in K[0]["basis"])
check("the second case codes SIGNALLED_UNJOINED", KS["COLUMBIA"]["state"] == "SIGNALLED_UNJOINED")
check("the third and fourth cases are NOT_EVALUABLE on the order's text", KS["TACOMA NARROWS"]["state"] == "NOT_EVALUABLE" and KS["QUIET FAILURE CLASS"]["state"] == "NOT_EVALUABLE")
check("holder count and lead time UNDECLARED on all four (the order states none)", all(dc.holder_count(k) == "UNDECLARED" and dc.lead_time(k) == "UNDECLARED" for k in K))
check("separation on the order's own cases is NOT_EVALUABLE: one signal level", dc.separation(K)["state"] == "NOT_EVALUABLE")
check("EGRESS carries a measured timestamp, four refused hosts and the control", re.match(r"\d{4}-\d\d-\d\dT\d\d:\d\dZ", dc.EGRESS["measured"]) and sum(1 for v in dc.EGRESS["hosts"].values() if "403" in v) == 4 and "github.com:443" in dc.EGRESS["hosts"])

# ----------------------------------------------------------------- evidence
section("evidence: parsed, carried, the flat reading split by clause")
F = ev.findings()
check("three findings parsed, every one CARRIED_NOT_VERIFIED, the order's tag carried apart", len(F) == 3 and all(f["status"] == "CARRIED_NOT_VERIFIED" and f["orders_status"] == "fetched, verified" for f in F))
n0 = F[0]["numbers_as_written"][0]
# compared through the span, not a literal: a literal here would put the
# number into an authored module and fire the scan below on this file (UNI_010)
check("the one number as written slices out of its own body and is a percentage", F[0]["body"][n0["span"][0]:n0["span"][1]] == n0["as_written"] and n0["as_written"].endswith("%") and len(F[0]["numbers_as_written"]) == 1)
check("two of three bullets state an absence of RECORD; the third does not", [f["states_record_absent"] for f in F] == [True, True, False])
FR = ev.flat_reading()
check("flat reading clause 1 (not recorded) is stated by 2 of 3 bullets", FR["record_absent_clause"]["n"] == 2)
check("flat reading clause 2 (no cost comparison) is in the flat sentence and stated by 0 bullets", FR["act_absent_clause"]["present_in_flat"] and FR["act_absent_clause"]["stated_by_bullets"] == [])
S = ev.source_line()
check("source parsed as written: author, venue, year; CARRIED", (S["author"], S["year"], S["status"]) == ("Hutchinson", "2024", "CARRIED_NOT_VERIFIED"))
check("the adjacent safety-economics sentence parses across its line break", S["adjacent"].startswith("safety-economics literature") and S["so"].startswith("cheapness arguments"))
try:
    ev.findings(ORDER_TEXT.replace("## Evidence", "## Evidenc"))
    check("a text without the Evidence section raises", False)
except ValueError:
    check("a text without the Evidence section raises", True)
check("record-absent markers are a word list, stated as one in the module", "word list" in open(os.path.join(HERE, "evidence.py")).read() or "composed at call time" in open(os.path.join(HERE, "evidence.py")).read())

# --------------------------------------------------------------- ownability
section("ownability: bounded nulls, role records, open question derived")
ON = ow.order_null()
check("the order's null states 'two' searches and no corpus, terms or date", ON["searches_stated"] == "two" and not (ON["corpus_stated"] or ON["terms_stated"] or ON["date_stated"]))
check("the order's null is UNBOUNDED lacking all four fields", ON["bounded"]["state"] == "UNBOUNDED" and ON["bounded"]["lacks"] == list(ow.NULL_FIELDS))
CN = ow.constructed()["nulls"]
check("a full null record is BOUNDED; hits 0 reads NULL_IN_STATED_CORPUS", ow.bounded(CN[0]) == {"state": "BOUNDED", "hits": 0, "reading": "NULL_IN_STATED_CORPUS"})
check("hits > 0 reads INVERSE_CASE_CANDIDATES", ow.bounded(CN[1])["reading"] == "INVERSE_CASE_CANDIDATES")
check("a non-integer hit count is MALFORMED", ow.bounded(dict(CN[0], hits="none"))["state"] == "MALFORMED")
check("hits 0 is BOUNDED and hits absent is UNBOUNDED: zero is not absent", ow.bounded(CN[0])["state"] == "BOUNDED" and ow.bounded({k: v for k, v in CN[0].items() if k != "hits"})["state"] == "UNBOUNDED")
check("inverse_search over unbounded nulls only is NOT_MEASURED, entering no count", ow.inverse_search([CN[2], {}])["state"] == "NOT_MEASURED")
check("inverse_search: all bounded at 0 -> NULL_IN_STATED_CORPORA", ow.inverse_search([CN[0]])["state"] == "NULL_IN_STATED_CORPORA")
check("inverse_search: a bounded hit -> CANDIDATES_TO_READ, unbounded listed apart", ow.inverse_search(CN)["state"] == "CANDIDATES_TO_READ" and len(ow.inverse_search(CN)["unbounded"]) == 1)
CR = ow.constructed()["roles"]
check("role records reach EXISTENCE_PROOF / ROLE_NOT_THE_JOIN / ROLE_WITHOUT_AUTHORITY / UNDECLARED", [ow.role_record(r)["state"] for r in CR] == ["EXISTENCE_PROOF", "ROLE_NOT_THE_JOIN", "ROLE_WITHOUT_AUTHORITY", "UNDECLARED"])
check("a record missing a field is UNDECLARED naming it", ow.role_record({"regulator": "x"})["lacks"] == ["role_name", "authority", "holds_the_join"])
check("a value outside the vocabulary is MALFORMED", ow.role_record(dict(CR[0], authority="yes"))["state"] == "MALFORMED")
check("the regulator and role NAME reach no branch (renamed, same state)", all(ow.role_record(dict(r, regulator="Z", role_name="z"))["state"] == ow.role_record(r)["state"] for r in CR))
check("ownability with one proof -> NEVER_ASSIGNED", ow.ownability(CR)["open_question"] == "NEVER_ASSIGNED")
check("ownability with no records -> UNDETERMINED", ow.ownability([])["open_question"] == "UNDETERMINED")
check("ownability with only non-proof roles -> UNDETERMINED, not UNOWNABLE", ow.ownability(CR[1:])["open_question"] == "UNDETERMINED" and "UNOWNABLE" not in ow.ownability(CR[1:])["open_question"])
check("UNOWNABLE is returned by no path (absence of a proof is not a proof of absence)", "UNOWNABLE" not in {ow.ownability(x)["open_question"] for x in ([], CR, CR[1:], [{}])})
check("the order's current read is carried with its tag", ow.order_read()["tag"] == "OBSERVED" and ow.order_read()["status"] == "CARRIED")

# ------------------------------------------------------------- blind coding
section("blind_coding: the gate refuses this session; agreement per field, no composite")
check("a coding that saw the decomposition is REFUSED", bc.admit(dict(full, case="c", coder="me", saw_decomposition=True))["state"] == "REFUSED")
check("an undeclared saw_decomposition is REFUSED, not admitted by default", "not declared" in bc.admit(dict(full, case="c", coder="me"))["why"])
check("a coding with coder and case that did not see it is ADMITTED", bc.admit(dict(full, case="c", coder="me", saw_decomposition=False))["state"] == "ADMITTED")
check("every one of this session's codings is REFUSED", all(bc.admit(k)["state"] == "REFUSED" for k in K))
a, b = bc.constructed_pairs()[0]
G = bc.agreement(a, b)
check("agreement per field: AGREE, DISAGREE and UNSEARCHED_ON_ONE_SIDE all reached", set(G["per_field"].values()) == {"AGREE", "DISAGREE", "UNSEARCHED_ON_ONE_SIDE"})
check("agreement on different cases is NOT_EVALUABLE", bc.agreement(a, dict(b, case="K-9"))["state"] == "NOT_EVALUABLE")
check("agreement with a refused coding is NOT_EVALUABLE", bc.agreement(a, dict(b, saw_decomposition=True))["state"] == "NOT_EVALUABLE")
CA = bc.corpus_agreement([])
check("corpus_agreement over no pairs is NOT_RUN", CA["state"] == "NOT_RUN")
check("no composite key in the agreement readout", not any(k in CA for k in ("score", "total", "kappa", "mean", "overall")))
check("corpus_agreement with a refused pair lists it and evaluates 0", bc.corpus_agreement([(a, dict(b, saw_decomposition=True))])["pairs_evaluated"] == 0)

# ------------------------------------------------------------------- folder
section("folder: constraints read from the files")
mods = ["decomposition.py", "evidence.py", "ownability.py", "blind_coding.py", "run_all.py", "selftest.py"]
LOCAL = {m[:-3] for m in mods}
STDLIB = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else None
NET = {"socket", "urllib", "http", "ssl", "ftplib", "smtplib", "requests"}
for m in mods:
    s = open(os.path.join(HERE, m)).read()
    t = ast.parse(s, feature_version=(3, 9))
    names = {x.name.split(".")[0] for n in ast.walk(t) if isinstance(n, ast.Import) for x in n.names}
    names |= {n.module.split(".")[0] for n in ast.walk(t) if isinstance(n, ast.ImportFrom) and n.module}
    check("%s parses under 3.9, imports stdlib-or-local, no network module" % m, all(n in LOCAL or (STDLIB is None or n in STDLIB) for n in names) and not (names & NET))
    check("%s under 300 lines" % m, s.count("\n") < 300)
for m in mods[:4]:
    p = subprocess.run([sys.executable, os.path.join(HERE, m), "--selftest"], capture_output=True)
    check("%s refuses --selftest with exit 2" % m, p.returncode == 2)
PARENT = '"' + "." * 2 + '"'
check("no module inserts a parent path", not any(PARENT in open(os.path.join(HERE, m)).read() for m in mods))
authored = [f for f in mods + ["README.md", "CLAIM_TABLE.md"] if os.path.exists(os.path.join(HERE, f))]
# company and site names come from the parsed findings at run time (UNI_010)
ORG_NAMES = [f["name"] for f in F]
check("no authored file carries a company or site name the evidence section carries (parsed at call time only)", not any(n in open(os.path.join(HERE, f)).read() for f in authored for n in ORG_NAMES))
check("the name scan fires on a plant", any(n in "x " + ORG_NAMES[0] + " y" for n in ORG_NAMES))
check("no authored module carries a number the evidence section states as written", not any(n["as_written"] in open(os.path.join(HERE, m)).read() for m in mods for f in F for n in f["numbers_as_written"]))
buf = io.StringIO()
with redirect_stdout(buf):
    import run_all
    run_all.main()
out = buf.getvalue()
check("run_all prints the declaration before the first part", out.index("CONTAMINATION DECLARATION") < out.index("decomposition --"))
check("declaration names position, coding, parties, records, evidence, rate", all(k in out for k in ("position", "coding", "parties", "records", "evidence", "rate")))
check("run_all renders every part", all(k in out for k in ("decomposition --", "evidence --", "ownability --", "blind_coding --")))
check("WORK_ORDER.md carries the delivered title line", ORDER_TEXT.startswith("# WO-2"))

print()
print("checks: %d   failed: %d" % (N, len(FAILED)))
for f in FAILED:
    print("  FAILED: " + f)
sys.exit(1 if FAILED else 0)
