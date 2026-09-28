"""assessor-coupling -- the null-tested suite. Prints its own count."""
import ast
import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import conditions as cd          # noqa: E402
import pool_metric as pm         # noqa: E402
import disclosure_audit as da    # noqa: E402
import precedent as pr           # noqa: E402

N = 0
FAILED = []


def check(name, ok):
    global N
    N += 1
    print("  %-5s %s" % ("ok" if ok else "FAIL", name))
    if not ok:
        FAILED.append(name)


def section(t):
    print("\n" + t)


ORDER_TEXT = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()

# ---------------------------------------------------------------- conditions
section("conditions: the eight, parsed, scored, never composed")
C = cd.conditions()
check("eight conditions parsed from the order", sorted(C) == list(range(1, 9)))
check("condition 6 is PERSONAL LIABILITY ON THE ASSESSOR", C[6][0] == "PERSONAL LIABILITY ON THE ASSESSOR")
check("every condition but 8 carries a gloss line", all(C[i][1] for i in range(1, 8)))
short = ORDER_TEXT.replace("  8  CAPACITY PROPORTIONATE TO SCOPE\n", "")
try:
    cd.conditions(short)
    check("a retyped copy holding seven raises", False)
except ValueError:
    check("a retyped copy holding seven raises", True)
D = cd.defense()
check("common prior defense parses to four items", len(D) == 4 and D[0].startswith("no direct payment"))
S = cd.score(cd.carried_scoring())
check("carried scoring: FAILS 6, UNVERIFIABLE 1, UNDECLARED 1, MET 0", S["counts"] == {"MET": 0, "FAILS": 6, "UNVERIFIABLE": 1, "UNDECLARED": 1})
check("condition 1 is UNDECLARED: the order's current-position section scores 7 of 8", S["per_condition"][1] == "UNDECLARED" and S["undeclared"] == [1])
check("hop-1 is carried beside the eight and reaches none of them", S["hop1_stated"] is True and S["hop1_reaches_condition"] is None)
check("no composite key in the scoring", not any(k in S for k in ("score", "total", "index", "mean")))
allmet = dict(cd.carried_scoring(), states={i: "MET" for i in range(1, 9)})
check("an all-MET record scores MET 8 (branch reachable)", cd.score(allmet)["counts"]["MET"] == 8)
check("an unknown state is MALFORMED, not read", cd.score(dict(allmet, states={1: "OK"}))["state"] == "MALFORMED")
check("a missing states dict is eight UNDECLARED", cd.score({"subject": "field"})["counts"]["UNDECLARED"] == 8)
check("a name-shaped subject is REFUSED_NAMED_PARTY", cd.score(dict(allmet, subject="Example Inc."))["state"] == "REFUSED_NAMED_PARTY")
check("non-dict is MALFORMED", cd.score("x")["state"] == "MALFORMED")
de = cd.defense_effect(cd.carried_scoring())
check("stating all four defense items moves no condition (INVARIANT)", de["state"] == "INVARIANT" and de["conditions_moved"] == [])
check("defense_effect on a malformed record is NOT_EVALUABLE", cd.defense_effect({"states": {1: "OK"}})["state"] == "NOT_EVALUABLE")

# ---------------------------------------------------------------- pool metric
section("pool_metric: fractions on constructed graphs; the label reaches no arithmetic")
F = pm.constructed_fields()
sp = pm.field_distribution(F["single_pool"])
check("single pool: every assessor 1.0", sp["distribution"] == [1.0, 1.0, 1.0] and sp["measured"] == 3)
dj = pm.field_distribution(F["disjoint"])
check("disjoint sources: every assessor 0.0 (reachable negative)", dj["distribution"] == [0.0, 0.0])
mx = pm.field_distribution(F["mixed"])
check("mixed: A2 reads 0.2 (2 of 10 from the coupled source)", mx["per_assessor"]["A2"]["fraction"] == 0.2)
check("mixed: A3 coupled only through governance (second order)", mx["per_assessor"]["A3"]["paths"] == {"S2": ("governed_by_equity_holder",)})
check("mixed: A4 with an undeclared amount is UNDECLARED, not 0 and not measured", mx["per_assessor"]["A4"]["state"] == "UNDECLARED" and mx["undeclared"] == 1 and mx["measured"] == 3)
for name, f in F.items():
    check("relabel every edge 'salary' moves nothing on %s" % name,
          pm.field_distribution(pm.relabel(f, "salary"))["distribution"] == pm.field_distribution(f)["distribution"])
nf = pm.assessor_fraction("Z", F["mixed"]["sources"], F["mixed"]["sector"], {})
check("assessor with no recorded funding -> NO_RECORDED_FUNDING, fraction None", nf["state"] == "NO_RECORDED_FUNDING" and nf["fraction"] is None)
src = open(os.path.join(HERE, "pool_metric.py")).read()
tree = ast.parse(src)
arith = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("coupled", "assessor_fraction", "field_distribution")]
check("label is read by no arithmetic function (AST: no 'label' constant in them)",
      not any(isinstance(x, ast.Constant) and x.value == "label" for fn in arith for x in ast.walk(fn)))
cyc_gov = {"S": ["T"], "T": ["S"]}
check("a governance cycle terminates and reads no coupling", pm.coupled("S", {"funded_by": [], "equity_held_by": []}, cyc_gov) == ())
check("governance depth 0 reads no second-order coupling", pm.coupled("S2", F["mixed"]["sector"], F["mixed"]["governance"], depth=0) == ())
check("EGRESS carries a measured timestamp and the control host", re.match(r"\d{4}-\d\d-\d\dT\d\d:\d\dZ", pm.EGRESS["measured"]) and "github.com:443" in pm.EGRESS["hosts"])

# ---------------------------------------------------------------- disclosure
section("disclosure_audit: declared coverage, five verdicts, UNMEASURED never ABSENT")
I = {i["id"]: i for i in da.constructed()}
check("money-only instrument -> MONEY_ONLY, no_field is the other seven", da.audit(I["I-money"])["state"] == "MONEY_ONLY" and da.audit(I["I-money"])["no_field"] == [1, 3, 4, 5, 6, 7, 8])
check("money-plus -> BEYOND_MONEY with fields on 2, 3, 4", da.audit(I["I-money-plus"])["has_field"] == [2, 3, 4])
check("uncoded-only -> NOT_EVALUABLE, not NO_CONDITION_FIELD", da.audit(I["I-uncoded"])["state"] == "NOT_EVALUABLE")
check("empty instrument -> NO_CONDITION_FIELD", da.audit(I["I-empty"])["state"] == "NO_CONDITION_FIELD")
check("a cover outside 1..8 is MALFORMED", da.audit({"fields": [{"name": "x", "covers": [9]}]})["state"] == "MALFORMED")
renamed = {"fields": [dict(f, name="field-%d" % i) for i, f in enumerate(I["I-money-plus"]["fields"])]}
check("field NAME reaches no check (renamed, same verdict and coverage)", da.audit(renamed)["has_field"] == da.audit(I["I-money-plus"])["has_field"])
check("five non-financial couplings parsed from the order", len(da.couplings()) == 5)
ro = da.coupling_readout(I["I-money"])
check("coupling readout never returns ABSENT", set(ro.values()) <= {"COVERED", "UNMEASURED"} and "ABSENT" not in ro.values())
check("all five UNMEASURED on the money-only instrument", all(v == "UNMEASURED" for v in ro.values()))
check("COVERED reachable when a field declares the coupling", da.coupling_readout(I["I-money-plus"])["overlapping boards and advisory positions"] == "COVERED")

# ---------------------------------------------------------------- precedent
section("precedent: parsed from the order, carried, schemas empty")
E = pr.entries()
check("ten entries across three eras", len(E) == 10 and len({e["era"] for e in E}) == 3)
check("every entry CARRIED_NOT_VERIFIED", all(e["status"] == "CARRIED_NOT_VERIFIED" for e in E))
check("every number as written slices out of its own body", all(e["body"][n["span"][0]:n["span"][1]] == n["as_written"] for e in E for n in e["numbers_as_written"]))
check("three entries carry a digit-adjacent number as written", sum(1 for e in E if e["numbers_as_written"]) == 3)
boiler = [e for e in E if "boiler" in e["name"].lower()][0]
check("a number written as a word ('Thousands') is NOT extracted: stated limit of a digit reader", not boiler["numbers_as_written"] and "Thousands" in boiler["body"])
check("the three entries with no stated remedy are the three most recent in the table", [e["remedy_stated"] for e in E] == [True] * 7 + [False] * 3)
try:
    pr.entries(ORDER_TEXT.split("## THE PRECEDENT RECORD")[0])
    check("a text without the record raises", False)
except ValueError:
    check("a text without the record raises", True)
check("survey schema: every field UNMEASURED, NOT_RUN, frame stated", all(v == "UNMEASURED" for v in pr.survey_schema()["fields"].values()) and pr.survey_schema()["state"] == "NOT_RUN" and "selected on failure" in pr.survey_schema()["frame"])
check("decay schema: four remedies, every field UNMEASURED", len(pr.decay_schema()["remedies"]) == 4 and all(v == "UNMEASURED" for v in pr.decay_schema()["fields"].values()))
check("no numeral anywhere in either schema's values", not re.search(r"\d", " ".join(str(v) for v in list(pr.survey_schema()["fields"].values()) + list(pr.decay_schema()["fields"].values()))))

# ---------------------------------------------------------------- folder
section("folder: constraints read from the files")
mods = ["conditions.py", "pool_metric.py", "disclosure_audit.py", "precedent.py", "run_all.py", "selftest.py"]
LOCAL = {m[:-3] for m in mods}
STDLIB = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else None
NET = {"socket", "urllib", "http", "ssl", "ftplib", "smtplib", "requests"}
for m in mods:
    src = open(os.path.join(HERE, m)).read()
    t = ast.parse(src, feature_version=(3, 9))
    names = {a.name.split(".")[0] for n in ast.walk(t) if isinstance(n, ast.Import) for a in n.names}
    names |= {n.module.split(".")[0] for n in ast.walk(t) if isinstance(n, ast.ImportFrom) and n.module}
    ok = all(n in LOCAL or (STDLIB is None or n in STDLIB) for n in names) and not (names & NET)
    check("%s parses under 3.9, imports stdlib-or-local, no network module" % m, ok)
    check("%s under 300 lines" % m, src.count("\n") < 300)
for m in mods[:4]:
    p = subprocess.run([sys.executable, os.path.join(HERE, m), "--selftest"], capture_output=True)
    check("%s refuses --selftest with exit 2" % m, p.returncode == 2)
PARENT = '"' + "." * 2 + '"'
check("no module inserts a parent path", not any(PARENT in open(os.path.join(HERE, m)).read() for m in mods))
authored = mods + ["README.md", "CLAIM_TABLE.md"]
present = [f for f in authored if os.path.exists(os.path.join(HERE, f))]
# the names are taken from the parsed entries at run time, so this file
# does not carry them and cannot fire on itself (UNI_010; the first
# version wrote them as a literal and did)
ENTRY_NAMES = [e["name"] for e in E]
check("no authored file carries an entry name the order's table carries (parsed at call time only)",
      not any(n in open(os.path.join(HERE, f)).read() for f in present for n in ENTRY_NAMES))
check("the entry-name scan fires on a plant", any(n in "x " + ENTRY_NAMES[0] + " y" for n in ENTRY_NAMES))
buf = io.StringIO()
with redirect_stdout(buf):
    import run_all
    run_all.main()
out = buf.getvalue()
check("run_all prints the declaration before the first part", out.index("CONTAMINATION DECLARATION") < out.index("conditions --"))
check("declaration names position, parties, records, precedent, companions, interest", all(k in out for k in ("position", "parties", "records", "precedent", "companions", "interest")))
parent = os.path.dirname(HERE)
wo_heads = []
for d in os.listdir(parent):
    wo = os.path.join(parent, d, "WORK_ORDER.md")
    if os.path.isfile(wo):
        wo_heads.append(open(wo, encoding="utf-8").readline())
check("WO-4 and WO-5 are named by the order and no folder's WORK_ORDER.md is headed by either (named-and-absent, by artifact)",
      "WO-4" in ORDER_TEXT and "WO-5" in ORDER_TEXT and not any(h.startswith("# WO-4") or h.startswith("# WO-5") for h in wo_heads))
check("WORK_ORDER.md carries the delivered title line", ORDER_TEXT.startswith("# WO-6"))

print()
print("checks: %d   failed: %d" % (N, len(FAILED)))
for f in FAILED:
    print("  FAILED: " + f)
sys.exit(1 if FAILED else 0)
