#!/usr/bin/env python3
"""
selftest_gr -- checks on gap_register.py and on the shipped register.

Run: python3 selftest_gr.py
The count is printed at the end rather than stored anywhere.

Two things this file is careful about. The schema, the type set and the
status enum are read OUT OF WORK_ORDER.md at run time rather than
retyped, so an edit to the delivered order and not to the module turns
this red. And every check that can fire is shown to be able to stay
silent as well: a checker that refuses everything passes an
all-negative suite.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import gap_register as gr          # noqa: E402
import no_severity                 # noqa: E402

ORDER = open(os.path.join(HERE, "WORK_ORDER.md")).read()
CHECKS = []


def ck(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    if not cond:
        print("FAIL  %s  %s" % (name, detail))


def run(args, cwd=HERE):
    p = subprocess.Popen([sys.executable, "gap_register.py"] + args,
                         cwd=cwd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, out.decode(), err.decode()


def rec(**kw):
    """A minimal well-formed entry; keyword arguments override."""
    base = {
        "id": "GR-9001", "type": "T1",
        "quantity": "a quantity held outside the method",
        "index_terms": ["alpha", "beta", "gamma"],
        "excluding_method": "the method, which returns something else",
        "measured_instead": "the something else",
        "venue_check": "a venue",
        "closure_condition": "a published table carrying the column",
        "refutation": "the column is already there and reported",
        "status": "UNKNOWN",
        "provenance": ["selftest_gr.py (constructed)"],
        "confound": None,
        "opened": "2026-09-11",
    }
    base.update(kw)
    return base


def verdicts(checks):
    return dict((c.rule, c.verdict) for c in checks)


# ------------------------------------------------ 1. module against order

order_schema = re.search(r"## 4\. RECORD SCHEMA.*?```json\n(.*?)\n```",
                         ORDER, re.S)
ck("order schema block located", order_schema)
keys = re.findall(r'^\s*"([a-z_]+)"\s*:', order_schema.group(1), re.M)
ck("FIELDS is the order's schema, in order", tuple(keys) == gr.FIELDS,
   "%s vs %s" % (keys, list(gr.FIELDS)))

enum = re.search(r"return enum:\s*(.*?)\n\n", ORDER, re.S).group(1)
enum_terms = re.findall(r"[A-Z][A-Z_]+", enum)
ck("STATUS is the order's enum", tuple(enum_terms) == gr.STATUS,
   "%s vs %s" % (enum_terms, list(gr.STATUS)))
ck("four types, not three (order section 9 O1 is open)",
   gr.TYPES == ("T1", "T2", "T3", "T4"))
ck("nullable is venue_check and confound only",
   gr.NULLABLE == ("venue_check", "confound"))
ck("provenance is not scanned by V4", "provenance" not in gr.V4_SCANNED)
for rule in ("V1", "V2", "V3", "V4", "V5", "V6"):
    ck("order names %s" % rule, re.search(r"^%s\s" % rule, ORDER, re.M))

# ------------------------------------------------ 2. the shipped register

records = gr.load(gr.REGISTER)
ck("register carries 7 entries", len(records) == 7, str(len(records)))
ids = [r["id"] for r in records]
ck("ids are GR-0001..GR-0007",
   ids == ["GR-%04d" % i for i in range(1, 8)], str(ids))

seed = re.search(r"## 7\. SEED ENTRIES.*?```\n(.*?)\n```", ORDER, re.S).group(1)
seed_types = dict(re.findall(r"(GR-\d{4})\s+(T\d)", seed))
ck("order lists 7 seeds", len(seed_types) == 7, str(len(seed_types)))
ck("every entry's type is the type the order gives it",
   all(r["type"] == seed_types[r["id"]] for r in records),
   str([(r["id"], r["type"], seed_types[r["id"]]) for r in records]))

results = gr.validate_all(records)
counts = gr.tally(results)
ck("no FAIL on the shipped register", counts[gr.FAIL] == 0, str(counts))
ck("V5 returns UNDETERMINED on all 7", counts[gr.UNDETERMINED] == 7,
   str(counts))
ck("the 7 UNDETERMINED are all V5",
   all(c.rule == "V5" for _i, cs in results for c in cs
       if c.verdict == gr.UNDETERMINED))
ck("35 PASS", counts[gr.PASS] == 35, str(counts))
ck("every shipped status is UNKNOWN",
   set(r["status"] for r in records) == set(["UNKNOWN"]),
   str(set(r["status"] for r in records)))
ck("every entry names a quantity and a closure condition",
   all(r["quantity"].strip() and r["closure_condition"].strip()
       for r in records))
ck("every entry's provenance points at the order",
   all(any("WORK_ORDER.md" in p for p in r["provenance"]) for r in records))

# Every all-caps identifier the register uses is one the order supplies:
# the register introduces no standard, body or coinage of its own.
acr = set()
for r in records:
    for f in gr.V4_SCANNED:
        for t in re.findall(r"\b[A-Z]{2,}\b", str(r.get(f) or "")):
            acr.add(t)
ck("the register uses at least one all-caps identifier", acr, str(acr))
ck("every all-caps identifier is in the order",
   all(t in ORDER for t in acr), str([t for t in acr if t not in ORDER]))

# ----------------------------------------------------------- 3. the demo

code, out, err = run(["validate", "demo/fails.jsonl"])
ck("demo exits nonzero", code != 0, "exit=%d" % code)
demo = gr.load(os.path.join(HERE, "demo", "fails.jsonl"))
dres = gr.validate_all(demo)
bad = sorted((i, c.rule) for i, cs in dres for c in cs
             if c.verdict == gr.FAIL)
ck("the demo fails on exactly V4 and V2, one each",
   bad == [("GX-0001", "V4"), ("GX-0002", "V2")], str(bad))
ck("the V4 demo entry names the span it tripped on",
   any("Alex Hartley" in c.detail for i, cs in dres for c in cs
       if c.rule == "V4" and i == "GX-0001"))
ck("the demo exercises the V5 PASS branch",
   all(verdicts(cs)["V5"] == gr.PASS for _i, cs in dres))
code, out, err = run(["validate"])
ck("the shipped register exits zero", code == 0, "exit=%d" % code)

# ------------------------------------------- 4. every branch is reachable

ck("V1 PASS", gr.v1_fields(rec()).verdict == gr.PASS)
r = rec()
del r["venue_check"]
ck("V1 FAIL on an absent field", gr.v1_fields(r).verdict == gr.FAIL)
ck("V1 FAIL on null outside the two nullable fields",
   gr.v1_fields(rec(quantity=None)).verdict == gr.FAIL)
ck("V1 PASS on null inside them",
   gr.v1_fields(rec(venue_check=None, confound=None)).verdict == gr.PASS)
ck("V1 FAIL on an empty index_terms list",
   gr.v1_fields(rec(index_terms=[])).verdict == gr.FAIL)
ck("V1 FAIL on a malformed id", gr.v1_fields(rec(id="0001")).verdict == gr.FAIL)
ck("V1 FAIL on a malformed date",
   gr.v1_fields(rec(opened="11 Sep 2026")).verdict == gr.FAIL)

ck("V2 PASS on an observable noun", gr.v2_closure(rec()).verdict == gr.PASS)
ck("V2 FAIL on modal-only",
   gr.v2_closure(rec(closure_condition="the arrangement should change "
                     "and practice ought to follow")).verdict == gr.FAIL)
ck("V2 FAIL with neither noun nor modal",
   gr.v2_closure(rec(closure_condition="it is otherwise")).verdict == gr.FAIL)

ck("V3 PASS", gr.v3_refutation(rec()).verdict == gr.PASS)
ck("V3 FAIL when refutation restates the closure condition",
   gr.v3_refutation(rec(refutation=rec()["closure_condition"])).verdict
   == gr.FAIL)
ck("V3 FAIL when refutation is empty",
   gr.v3_refutation(rec(refutation="  ")).verdict == gr.FAIL)

ck("V4 PASS", gr.v4_placement(rec()).verdict == gr.PASS)
c = gr.v4_placement(rec(measured_instead="the count Alex Hartley keeps"))
ck("V4 FAIL on a name-shaped span", c.verdict == gr.FAIL)
ck("V4 names the span", "Alex Hartley" in c.detail, c.detail)
ck("V4 FAIL on an accusatory construction",
   gr.v4_placement(rec(excluding_method="the form, which was deliberately "
                       "left short")).verdict == gr.FAIL)
c = gr.v4_placement(rec(excluding_method="the form, kept short as a matter "
                        "of motive"))
ck("V4 FAIL on a motive term", c.verdict == gr.FAIL)
ck("V4 routes a motive term to the order's section 2 return",
   "OUT_OF_ENVELOPE" in c.detail, c.detail)
ck("V4 is silent on a name inside provenance[]",
   gr.v4_placement(rec(provenance=["Alex Hartley, field note, 2026-09-11"]))
   .verdict == gr.PASS)

others = [rec(id="GR-9002", index_terms=["alpha", "beta", "gamma"])]
ck("V5 PASS when every term is used elsewhere",
   gr.v5_index(rec(), others).verdict == gr.PASS)
ck("V5 FAIL below three terms",
   gr.v5_index(rec(index_terms=["alpha", "beta"]), others).verdict == gr.FAIL)
ck("V5 FAIL when no term is used elsewhere",
   gr.v5_index(rec(index_terms=["x1", "x2", "x3"]), others).verdict == gr.FAIL)
ck("V5 UNDETERMINED when the two readings part",
   gr.v5_index(rec(index_terms=["alpha", "x1", "x2"]), others).verdict
   == gr.UNDETERMINED)
c = gr.v5_index(rec(), [])
ck("V5 NOT_EVALUABLE on a register of one", c.verdict == gr.NOT_EVALUABLE)
ck("V5 says why a register of one cannot be scored",
   "any other entry" in c.detail, c.detail)

ck("V6 PASS", gr.v6_status(rec()).verdict == gr.PASS)
ck("V6 FAIL outside the enum",
   gr.v6_status(rec(status="CLOSED")).verdict == gr.FAIL)
ck("V6 PASS on each of the five returns",
   all(gr.v6_status(rec(status=s)).verdict == gr.PASS for s in gr.STATUS))

# ------------------------------------------- 5. the name shape, both ways

ck("name shape fires on two adjacent capitalised tokens",
   gr.name_shaped("kept by Alex Hartley in a drawer") == ["Alex Hartley"])
ck("name shape fires on an honorific",
   gr.name_shaped("as Dr. Alvarez recorded") != [])
ck("name shape fires on et al",
   gr.name_shaped("reported in Hartley et al. 2026") != [])
ck("an all-caps acronym is not a name",
   gr.name_shaped("the AAHA and LEEP tables") == [])
ck("a sentence-initial capital is not a name",
   gr.name_shaped("Mediation outcome reporting scores closure only.") == [])
ck("an ordinary lowercase sentence is not a name",
   gr.name_shaped("the intake form carries no field for it") == [])

# --------------------------------------------------------- 6. subcommands

tmp = tempfile.mkdtemp()
copy = os.path.join(tmp, "REGISTER.jsonl")
open(copy, "w").write(open(gr.REGISTER).read())
cand = dict(rec(index_terms=["mediation", "negotiation", "consent"]))
del cand["id"]
code, out, err = run(["--register", copy, "add", json.dumps(cand)])
ck("add exits zero on a clean entry", code == 0, err)
ck("add assigns the next id", "GR-0008" in out, out)
ck("add appended one line", len(gr.load(copy)) == 8)
code, out, err = run(["--register", copy, "add",
                      json.dumps(dict(cand, closure_condition="it should "
                                      "be otherwise"))])
ck("add refuses an entry that FAILs", code == 1, "exit=%d" % code)
ck("the refused entry was not appended", len(gr.load(copy)) == 8)
code, out, err = run(["--register", copy, "add",
                      json.dumps(dict(cand, id="GR-0003"))])
ck("add refuses an id already in the register", code == 2, "exit=%d" % code)

code, out, err = run(["check", "GR-0003"])
ck("check exits zero", code == 0, err)
ck("check prints the closure condition and nothing else",
   out.strip() == records[2]["closure_condition"], out)
ck("check prints one line", len(out.strip().splitlines()) == 1)
code, out, err = run(["check", "GR-9999"])
ck("check refuses an absent id", code == 2, "exit=%d" % code)

code, out, err = run(["search", "analgesia"])
ck("search matches on index terms",
   sorted(re.findall(r"GR-\d{4}", out)) == ["GR-0002", "GR-0004"], out)
code, out, err = run(["search", "analgesia", "cervical"])
ck("search is an AND over terms",
   sorted(re.findall(r"GR-\d{4}", out)) == ["GR-0004"], out)
code, out, err = run(["search", "quantity-that-is-not-here"])
ck("search on nothing exits zero and reports zero", code == 0 and
   "0 of 7" in out, out)

code, export, err = run(["export", "--md"])
ck("export exits zero", code == 0, err)
ck("export carries one block per entry",
   len(re.findall(r"^## GR-\d{4}", export, re.M)) == 7)
code, out, err = run(["export"])
ck("export without --md is refused", code == 2, "exit=%d" % code)

code, out, err = run(["--selftest"])
ck("the instrument refuses --selftest", code == 2, "exit=%d" % code)
ck("and points at this file", "selftest_gr.py" in err, err)
code, out, err = run([])
ck("no arguments prints usage and exits 2", code == 2)
code, out, err = run(["--register", os.path.join(tmp, "absent.jsonl"),
                      "validate"])
ck("an absent register is refused by path", code == 2 and "absent.jsonl"
   in err, err)

# ------------------------------------------------------------- 7. screens

clean, hits = no_severity.check(export)
ck("the export render screens clean", clean, str(hits[:3]))
code, sout, _e = run(["search", "mediation"])
ck("the search render screens clean", no_severity.check(sout)[0])
code, vout, _e = run(["validate"])
ck("the register validate render screens clean",
   no_severity.check(vout)[0], str(no_severity.check(vout)[1][:3]))
code, dout, _e = run(["validate", "demo/fails.jsonl"])
dhits = set(w for _l, w, _t in no_severity.check(dout)[1])
ck("the demo validate render fires only on the constructed demo text",
   dhits <= set(["should", "ought"]), str(dhits))
ck("the screen fires when a graded word is planted",
   not no_severity.check(export + "\nthis entry is incorrect\n")[0])

# ------------------------------------------ 8. order section 9 left open

src = open(os.path.join(HERE, "gap_register.py")).read()
ck("O1 left open: T4 is not collapsed into T2", len(gr.TYPES) == 4)
ck("O2 left open: status is one field per entry, not per reader",
   all(isinstance(r["status"], str) for r in records))
ck("O3 left open: the store is bare JSONL, no dialect emitted",
   "@context" not in src and "@context" not in open(gr.REGISTER).read())

print("")
print("gap-register selftest: %d checks, %d not passing"
      % (len(CHECKS), len([1 for _n, ok, _d in CHECKS if not ok])))
sys.exit(1 if [1 for _n, ok, _d in CHECKS if not ok] else 0)
