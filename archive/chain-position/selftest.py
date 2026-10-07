#!/usr/bin/env python3
"""selftest.py -- every check here is null-tested: for each part a
PLANTED FAULT must fire, and the clean case must not. A suite whose
checks only ever pass has not shown it can fail. Prints the check
count; does not store it anywhere else.
"""
import ast
import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clause_audit as ca, trust_provenance as tp, horn_b as hb, load_class as lc, dissimilar as ds

N = 0
FAILED = []


def check(name, cond):
    global N
    N += 1
    if not cond:
        FAILED.append(name)
    print("  %s  %s" % ("ok  " if cond else "FAIL", name))


def section(title):
    print(title)


# ---------------------------------------------------------------- clause audit
section("clause_audit: step 1 over the carried summary")
a = ca.audit(ca.CARRIED)
check("run state NOT_RUN_ON_STANDARD (no STANDARD-sourced clause)", a["run_state"] == "NOT_RUN_ON_STANDARD")
check("carried summary: 5 clauses, 0 inside agent, 5 gateway", (a["n"], a["inside_agent"], a["gateway_only"]) == (5, 0, 5))
planted = ca.CARRIED + [{"id": "X", "text": "the agent is told its step index", "info_location": "AGENT", "source": "CARRIED"}]
check("planted AGENT clause -> inside_agent 1 (branch reachable)", ca.audit(planted)["inside_agent"] == 1 and ca.audit(planted)["inside_ids"] == ["X"])
check("planted BOTH counts inside", ca.audit([{"id": "Y", "info_location": "BOTH"}])["inside_agent"] == 1)
check("UNDECLARED counted apart, never as gateway", ca.audit([{"id": "Z"}]) ["undeclared"] == 1 and ca.audit([{"id": "Z"}])["gateway_only"] == 0)
check("STANDARD-sourced clause flips run state", ca.audit([{"id": "S", "info_location": "GATEWAY", "source": "STANDARD"}])["run_state"] == "RUN_ON_STANDARD")
check("empty -> EMPTY with None counts", ca.audit([])["run_state"] == "EMPTY" and ca.audit([])["inside_agent"] is None)
check("value outside vocabulary -> MALFORMED, typed", ca.code_clause({"id": "M", "info_location": "cloud"})["state"] == "MALFORMED")
# text reaches no check: replace every text and the counts are unchanged
blanked = [dict(c, text="") for c in ca.CARRIED]
check("clause text reaches no check (blanked text, same counts)", ca.audit(blanked)["inside_agent"] == a["inside_agent"] and ca.audit(blanked)["gateway_only"] == a["gateway_only"])
check("EGRESS record names both standard hosts and a control", set(ca.EGRESS["refused"]) == {"owasp.org:443", "genai.owasp.org:443"} and "github.com:443" in ca.EGRESS["control"])
src_ca = open(os.path.join(HERE, "clause_audit.py")).read()
check("clause_audit imports no network module", not any(m in src_ca for m in ("import socket", "import urllib", "import http")))

# ---------------------------------------------------------------- trust provenance
section("trust_provenance: step 2 specification")
full = tp.full_record()
check("full constructed record -> AUDITABLE at depth 0", tp.audit(full)["state"] == "AUDITABLE" and tp.audit(full)["depth"] == 0)
for f in tp.REQUIRED:
    r = dict(full)
    del r[f]
    out = tp.audit(r)
    check("planted absence of %s -> UNAUDITABLE naming it" % f, out["state"] == "UNAUDITABLE" and out["absent"] == [f])
und = dict(full, t_scored=tp.UNDECLARED)
check("UNDECLARED sentinel -> DECLARED_UNAUDITABLE, kept apart from ABSENT", tp.audit(und)["state"] == "DECLARED_UNAUDITABLE" and tp.audit(und)["undeclared"] == ["t_scored"] and tp.audit(und)["absent"] == [])
sub = dict(full, score={"value": 0.8})
check("missing sub-field (scale) -> ABSENT on score", tp.field_state(sub, "score", ("value", "scale")) == "ABSENT")
check("empty inputs list -> ABSENT", tp.field_state(dict(full, inputs=[]), "inputs", ()) == "ABSENT")
# recursion
inner = tp.full_record()
outer = dict(full, scorer_provenance=inner)
check("scorer_provenance as a full record -> AUDITABLE at depth 1", tp.audit(outer)["state"] == "AUDITABLE" and tp.audit(outer)["depth"] == 1)
broken_inner = dict(inner)
del broken_inner["method"]
check("inner absence propagates as UNAUDITABLE", tp.audit(dict(full, scorer_provenance=broken_inner))["state"] == "UNAUDITABLE")
deep = tp.full_record()
node = deep
for i in range(tp.DEPTH_CAP + 1):
    nxt = tp.full_record(step=i)
    node["scorer_provenance"] = nxt
    node = nxt
node["scorer_provenance"] = {"not_a_root": True, "x": 1}
check("chain past depth cap without root -> CHAIN_UNTERMINATED", tp.audit(deep)["state"] == "CHAIN_UNTERMINATED")
cyc = tp.full_record()
cyc["scorer_provenance"] = dict(tp.full_record(), scorer_provenance=dict(tp.full_record()))
cyc["scorer_provenance"]["scorer_provenance"]["scorer_provenance"] = dict(cyc["scorer_provenance"])
check("repeated provenance node -> CHAIN_CYCLE", tp.audit(cyc)["state"] == "CHAIN_CYCLE")
check("non-dict -> MALFORMED", tp.audit("x")["state"] == "MALFORMED")
check("scores_payload_only True on payload-only inputs", tp.scores_payload_only(full) is True)
two = dict(full, inputs=[{"id": "payload-1", "digest": "d1"}, {"id": "prior-score", "digest": "s0"}])
check("scores_payload_only False when a prior score is read", tp.scores_payload_only(two) is False)
check("scores_payload_only None when unreadable", tp.scores_payload_only({}) is None)
co = tp.common_object(tp.constructed_set())
check("constructed set -> NO_COMMON_OBJECT, common {score, method}", co["state"] == "NO_COMMON_OBJECT" and co["common"] == ["score", "method"])
check("three full records -> COMMON_OBJECT (branch reachable)", tp.common_object([tp.full_record()] * 3)["state"] == "COMMON_OBJECT")
check("empty set -> EMPTY, missing = whole spec", tp.common_object([])["state"] == "EMPTY" and tp.common_object([])["missing"] == list(tp.REQUIRED))
check("every constructed record declares itself CONSTRUCTED", all(r.get("source") == "CONSTRUCTED" for r in tp.constructed_set()))

# ---------------------------------------------------------------- horn B
section("horn_b: step 3, the container asks")
A = hb.arms()
for arm in ("STANDALONE", "CHAIN_SILENT"):
    r = hb.ask(A[arm])
    check("%s -> UNDETERMINED_FROM_INSIDE, all four UNOBTAINABLE" % arm, r["state"] == "UNDETERMINED_FROM_INSIDE" and all(q["reading"] == "UNOBTAINABLE_FROM_INSIDE" for q in r["quantities"].values()))
check("STANDALONE and CHAIN_SILENT interiors identical (delta empty)", hb.interior_delta(A["STANDALONE"], A["CHAIN_SILENT"]) == [])
check("CHAIN_DECLARED delta names only what the harness wrote", hb.interior_delta(A["STANDALONE"], A["CHAIN_DECLARED"]) == ["declared", "env_names"])
rd = hb.ask(A["CHAIN_DECLARED"])
check("CHAIN_DECLARED -> POSITION_ASSERTED, never OBSERVED", rd["state"] == "POSITION_ASSERTED" and not any(q["reading"] == "OBSERVED" for q in rd["quantities"].values()))
check("asserted index/total carried as testimony with basis", rd["asserted"] == {"index": 2, "total": 3} and rd["quantities"]["own_index"]["basis"] == "declared env")
check("verification of the assertion names an EXTERIOR source", rd["verification_of_assertion"] and "EXTERIOR" in rd["verification_of_assertion"])
check("upstream/downstream stay UNOBTAINABLE even when declared", rd["quantities"]["upstream_producer"]["reading"] == "UNOBTAINABLE_FROM_INSIDE" and rd["quantities"]["downstream_consumer"]["reading"] == "UNOBTAINABLE_FROM_INSIDE")
pf = dict(A["STANDALONE"], payload_chain_field={"index": 1, "total": 4})
check("a chain field in the payload reads ASSERTED_BY_INPUT (payload basis)", hb.ask(pf)["state"] == "POSITION_ASSERTED" and hb.ask(pf)["quantities"]["own_index"]["basis"] == "payload field")
check("every evidence sits EXTERIOR", all(hb.EVIDENCE[q][1] == "EXTERIOR" for q in hb.QUANTITIES))
check("position word list finds CHAIN_INDEX and ignores PATH", hb.position_names(["PATH", "CHAIN_INDEX", "HOME"]) == ["CHAIN_INDEX"])
check("malformed interior -> MALFORMED", hb.ask(3)["state"] == "MALFORMED")
try:
    hb.harness("NOPE")
    bad_arm = False
except ValueError:
    bad_arm = True
check("unknown arm refused", bad_arm)
# an interior planted with an OBSERVED reading cannot arise: ask() never emits OBSERVED
src_hb = open(os.path.join(HERE, "horn_b.py")).read()
tree = ast.parse(src_hb)
obs_assign = any(isinstance(n, ast.Constant) and n.value == "OBSERVED" and False for n in ast.walk(tree))
emits_observed = 'reading = "OBSERVED"' in src_hb or 'reading, basis = "OBSERVED"' in src_hb
check("ask() has no code path emitting OBSERVED (interior carries no chain evidence)", not emits_observed)
live = hb.live_interior()
check("live interior carries env NAMES only (no values field)", "env_values" not in live and all(isinstance(n, str) for n in live["env_names"]))
check("live interior: no env value string leaks into the record", not any(v == os.environ.get(k) for k in os.environ for v in live.values() if isinstance(v, str) and len(v) > 12))

# ---------------------------------------------------------------- load class
section("load_class: the compounding as arithmetic")
u = lc.union_band([0.01, 0.02, 0.03, 0.04])
# A first version of this check expected 0.096529, a transposition of
# the true 0.096550 (1 - 0.99*0.98*0.97*0.96 = 0.0965498). The check
# caught its own record. Recorded, not deleted (CHP claim table).
check("independent union 0.09655 (1 - prod(1-p))", abs(u["independent"] - 0.09655) < 1e-6)
check("band is [max p, min(1, sum p)] = [0.04, 0.10]", u["band"] == [0.04, 0.1])
check("independent point sits inside the band", u["band"][0] <= u["independent"] <= u["band"][1])
check("empty assessed set -> None, never 0", lc.union_band([]) is None and lc.union_band([None]) is None)
try:
    lc.union_band([1.5])
    oob = False
except ValueError:
    oob = True
check("probability outside [0,1] refused", oob)
assess = lc.assess(lc.FACTORS)
check("order's list: 4 assessed of 7, union is a floor", assess["n_assessed"] == 4 and assess["n_unassessed"] == 3 and assess["union_is_floor"] is True)
check("state NOT_FLIGHT_RATED: three unassessed with no structural handling", assess["state"] == "NOT_FLIGHT_RATED" and len(assess["unhandled"]) == 3)
handled = [dict(f, handling="STRUCTURAL") if f["p"] is None else f for f in lc.FACTORS]
check("declaring STRUCTURAL handling on every unassessed factor -> ASSESSED_OR_HANDLED (branch reachable)", lc.assess(handled)["state"] == "ASSESSED_OR_HANDLED")
rule = lc.apply_rule({"name": "x", "p": None})
check("RULE: unassessed -> assumed_stable False, bound UNBOUNDED, handling UNDECLARED", rule["assumed_stable"] is False and rule["bound"] == "UNBOUNDED" and rule["handling"] == "UNDECLARED")
check("refinement: credible-extreme condition + margin gives a bound", lc.apply_rule({"name": "x", "p": None, "worst_credible": 0.05, "margin": 0.02})["bound"] == 0.07)
check("assessed factor enters no rule (assumed_stable None)", lc.apply_rule({"name": "x", "p": 0.01})["assumed_stable"] is None)
check("empty factor list -> EMPTY", lc.assess([])["state"] == "EMPTY")
check("factor of safety 1.0 when designed to the threat exactly; None on zero", lc.factor_of_safety(1.0, 1.0) == 1.0 and lc.factor_of_safety(1.0, 0) is None)
check("unassessed factors enter no arithmetic (union over 4 not 7)", assess["union"]["n"] == 4)

# ---------------------------------------------------------------- dissimilar
section("dissimilar: step 4 as a specification")
spec = lambda o: o == 42
check("two copies one family agree -> AGREE, n_eff 1, not informative", ds.adjudicate({"F1": 42, "F1-copy": 42})["state"] == "AGREE" and ds.adjudicate({"F1": 42, "F1-copy": 42})["n_eff"] == 1)
check("disagree, no checker -> DISAGREE_UNADJUDICABLE", ds.adjudicate({"F1": 42, "F2": 41})["state"] == "DISAGREE_UNADJUDICABLE")
r = ds.adjudicate({"F1": 42, "F2": 41}, spec)
check("disagree with fixed spec -> DISAGREE_ADJUDICATED naming the failed copy", r["state"] == "DISAGREE_ADJUDICATED" and r["failed"] == ["F2"])
check("both off spec -> ALL_FAIL", ds.adjudicate({"F1": 40, "F2": 41}, spec)["state"] == "ALL_FAIL")
check("single copy -> SINGLE; empty -> EMPTY with n_eff None", ds.adjudicate({"F1": 1})["state"] == "SINGLE" and ds.adjudicate({})["n_eff"] is None)
check("n_eff counts families by prefix", ds.n_eff(["A", "A-1", "A-2", "B"]) == 2)
check("agreement with a checker is still AGREE (checker unread on agreement)", ds.adjudicate({"F1": 41, "F2": 41}, spec)["state"] == "AGREE")

# ---------------------------------------------------------------- folder constraints
section("folder constraints")
mods = ["clause_audit.py", "trust_provenance.py", "horn_b.py", "load_class.py", "dissimilar.py", "run_all.py", "selftest.py"]
STDLIB = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else None
local = {m[:-3] for m in mods}
for m in mods:
    src = open(os.path.join(HERE, m)).read()
    t = ast.parse(src, feature_version=(3, 9))
    names = set()
    for n in ast.walk(t):
        if isinstance(n, ast.Import):
            names.update(a.name.split(".")[0] for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module:
            names.add(n.module.split(".")[0])
    ok_imports = all((STDLIB is None or nm in STDLIB) or nm in local for nm in names)
    check("%s parses under 3.9 and imports stdlib-or-local only" % m, ok_imports)
    check("%s under 300 lines" % m, src.count("\n") < 300)
for m in mods[:5]:
    rc = subprocess.run([sys.executable, os.path.join(HERE, m), "--selftest"], capture_output=True, text=True).returncode
    check("%s refuses --selftest with exit 2" % m, rc == 2)
buf = io.StringIO()
with redirect_stdout(buf):
    import run_all
    run_all.main()
out = buf.getvalue()
check("run_all prints the declaration before the first part", out.index("CONTAMINATION DECLARATION") < out.index("clause_audit --"))
check("declaration names position, standard, vendors, models, mitigation, interest", all(k in out for k in ("position", "standard", "vendors", "models", "mitigation", "interest")))
# The token is composed so this file does not carry it literally and
# then fire on itself (UNI_010 / T1-1: the first version did).
PARENT = '"' + "." * 2 + '"'
check("no module inserts a parent path into sys.path", not any(PARENT in open(os.path.join(HERE, m)).read() for m in mods))
check("WORK_ORDER.md carries the delivered title line", open(os.path.join(HERE, "WORK_ORDER.md")).readline().startswith("# WO-1"))

print()
print("checks: %d   failed: %d" % (N, len(FAILED)))
for f in FAILED:
    print("  FAILED:", f)
sys.exit(1 if FAILED else 0)
