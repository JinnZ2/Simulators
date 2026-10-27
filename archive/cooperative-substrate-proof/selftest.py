#!/usr/bin/env python3
"""selftest.py -- every check here is null-tested: for each part a
PLANTED FAULT must fire, and the clean case must not. A suite whose
checks only ever pass has not shown it can fail. Prints the check
count; does not store it anywhere else.
"""
import ast
import io
import os
import random
import re
import subprocess
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scope, p1_dependency_records as p1, p2_substrate as p2, p3_comprehension as p3
import p4_goal_coherence as p4, p5_lag_declaration as p5

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


# ---------------------------------------------------------------- scope
section("scope: C1-C4 coding pass")
ok = {"conds": {"C1": "PRESENT", "C2": "PRESENT", "C3": "PRESENT", "C4": "PRESENT"}, "name": "x"}
check("all PRESENT -> ADMISSIBLE", scope.code_case(ok)["state"] == "ADMISSIBLE")
bad = {"conds": dict(ok["conds"], C4="ABSENT"), "name": "x"}
check("planted ABSENT C4 -> OUT_OF_SCOPE naming C4", scope.code_case(bad) == {"state": "OUT_OF_SCOPE", "absent": ["C4"], "uncoded": [], "name": "x"})
unc = {"conds": {"C1": "PRESENT", "C2": "PRESENT", "C4": "PRESENT"}, "name": "x"}
check("missing C3 -> UNDETERMINED, not OUT_OF_SCOPE", scope.code_case(unc)["state"] == "UNDETERMINED" and scope.code_case(unc)["uncoded"] == ["C3"])
check("ABSENT beats UNCODED", scope.code_case({"conds": {"C1": "ABSENT"}})["state"] == "OUT_OF_SCOPE")
check("value outside vocabulary -> MALFORMED, typed", scope.code_case({"conds": {"C1": "maybe"}})["state"] == "MALFORMED")
check("non-dict -> MALFORMED, not raised", scope.code_case(3)["state"] == "MALFORMED")
check("C1 from clocks: short window -> PRESENT", scope.c1_from_clocks(1.0, 10.0) == "PRESENT")
check("C1 from clocks: long window -> ABSENT", scope.c1_from_clocks(10.0, 1.0) == "ABSENT")
check("C1 from clocks: undeclared -> UNCODED, never ABSENT", scope.c1_from_clocks(None, 1.0) == "UNCODED" and scope.c1_from_clocks(1.0, 0) == "UNCODED")
coded = scope.code_corpus(scope.CONSTRUCTED)
check("constructed corpus reaches three states", all(len(coded[s]) == 1 for s in ("ADMISSIBLE", "OUT_OF_SCOPE", "UNDETERMINED")) and not coded["MALFORMED"])

# ---------------------------------------------------------------- P3
section("P3: comprehension")
rng = random.Random(1)
voc = "the instrument reads the field at the stated resolution and the calibration chain is recorded".split()
shared = [" ".join(rng.choice(voc) for _ in range(200)) for _ in range(4)]
r = p3.check(shared)
check("shared-vocabulary corpus -> CONVERGENT", r["state"] == "CONVERGENT" and r["gap"] > 0)
disj = [" ".join(rng.choice("alpha bravo charlie delta echo".replace("a", "abcd"[i]).split()) for _ in range(200)) for i in range(4)]
r = p3.check(disj)
check("planted disjoint-vocabulary corpus -> INDISTINGUISHABLE_FROM_NULL", r["state"] == "INDISTINGUISHABLE_FROM_NULL")
check("disjoint corpus gap sits on zero (|gap/sd| < 3)", abs(r["gap_over_sd"]) < 3)
check("one part -> NOT_EVALUABLE (null equals shared arm by construction)", p3.check([shared[0]])["state"] == "NOT_EVALUABLE")
check("short -> TOO_SHORT; empty -> EMPTY", p3.check(["a b"])["state"] == "TOO_SHORT" and p3.check([""])["state"] == "EMPTY" and p3.check([])["state"] == "EMPTY")
a, b = p3.remap(shared, 0, True), p3.remap(shared, 0, False)
check("both arms same length (letter-level control)", len(a) == len(b))
check("shared arm maps a shared word identically across parts", p3._pseudo("field", 0, 0) == p3._pseudo("field", 0, 0) and p3._pseudo("field", 0, 0) != p3._pseudo("field", 1, 0))
rs = p3.check(p3.self_corpus())
check("--self corpus -> CONVERGENT", rs["state"] == "CONVERGENT" and rs["n_parts"] >= 2)
check("script share reported, not gated", 0 < rs["script_share"] <= 1.0)

# ---------------------------------------------------------------- P4
section("P4: goal coherence")
check("self chain -> COHERENT", p4.chain_check(p4.self_chain())["state"] == "COHERENT")
check("correction (replacement + reason) -> CORRECTED, terminates", p4.chain_check(p4.CONSTRUCTED["corrected"])["state"] == "CORRECTED")
r = p4.chain_check(p4.CONSTRUCTED["self_contesting"])
check("planted contest without replacement -> NO_ANSWER, final None", r["state"] == "NO_ANSWER" and r["final"] is None)
check("dangling take -> DANGLING naming the id", p4.chain_check(p4.CONSTRUCTED["dangling"]) ["dangling"] == [("a", "z")])
check("empty -> EMPTY; non-list -> MALFORMED", p4.chain_check([])["state"] == "EMPTY" and p4.chain_check("x")["state"] == "MALFORMED")
check("contest with replacement but NO reason is a contest, not a correction",
      p4.chain_check([{"id": "a", "takes": [], "produces": "1"}, {"id": "b", "takes": [], "contests": ["a"], "produces": "2"}])["state"] == "NO_ANSWER")
t = p4.turf_war(3, 5, 2, 1, 50)
check("sabotage cheaper -> 0 of 3 complete", t["completed"] == 0 and t["sabotage_chosen"])
check("sabotage cheaper -> still 0 at budget 5000 (not a budget effect)", p4.turf_war(3, 5, 2, 1, 5000)["completed"] == 0)
t2 = p4.turf_war(3, 5, 2, 2, 50)
check("sabotage not cheaper -> 3 of 3 complete at turn n", t2["completed"] == 3 and t2["done_at"] == [5, 5, 5])
check("single agent cannot sabotage -> completes", p4.turf_war(1, 5, 2, 1, 50)["completed"] == 1)
check("malformed turf args -> typed", p4.turf_war(0, 5, 2, 1, 50)["state"] == "MALFORMED")
check("turf war is deterministic (no random module)", "random" not in {n.names[0].name for n in ast.walk(ast.parse(open(os.path.join(HERE, "p4_goal_coherence.py")).read())) if isinstance(n, ast.Import)})

# ---------------------------------------------------------------- P2
section("P2: substrate")
res = p2.run(os.path.join(HERE, "p2_substrate.py"))
check("on itself -> SUBSTRATE_HOLDS, no layer violated", res["state"] == "SUBSTRATE_HOLDS" and res["violated"] == [])
res2 = p2.run(os.path.join(HERE, "p2_substrate.py"))
check("second run reproduces sha256 and every count", res2["sha256"] == res["sha256"] and res2["layers"]["contracts"] == res["layers"]["contracts"] and res2["layers"]["compiler"] == res["layers"]["compiler"])
c = res["layers"]["contracts"]
check("unverified floor > 0 on its own source (no call verifies its contract by default)", c["unverified_floor"] > 0 and c["unverified_floor"] + c["verified_proxy"] == c["total_callsites"])
src = "x = f()\nif x is None:\n    pass\ntry:\n    g()\nexcept Exception:\n    pass\nh()\n"
cc = p2.contracts(src)
check("proxy fires on tested-next and try-wrapped, not on bare", cc == {"total_callsites": 3, "verified_proxy": 2, "unverified_floor": 1})


class _Fake:
    radix, mant_dig, max = 10, 24, 1e30


check("planted non-IEEE float_info -> numeric VIOLATED", p2.numeric_layer(_Fake())["state"] == "VIOLATED")
check("real float_info -> IEEE_754_BINARY64", p2.numeric_layer()["state"] == "IEEE_754_BINARY64")
check("faithful chain -> OUTPUT 7", p2.chain_demo(True) == {"state": "OUTPUT", "value": 7})
check("one planted adversarial link -> NO_OUTPUT, typed, not raised", p2.chain_demo(False)["state"] == "NO_OUTPUT" and p2.chain_demo(False)["broken_link"] == "link2")
check("scheduler count exact under lock", p2.scheduler_layer(500)["state"] == "HONOURED")
check("network layer is a socketpair: no connect() anywhere in P2", "connect" not in open(os.path.join(HERE, "p2_substrate.py")).read())

# ---------------------------------------------------------------- P1
section("P1: dependency records")
fx = open(os.path.join(HERE, "fixtures", "methods_CONSTRUCTED.txt"), encoding="utf-8").read()
check("fixture declares itself CONSTRUCTED on line 1", fx.splitlines()[0].startswith("CONSTRUCTED"))
m, a = p1.split_fixture(fx)
res = p1.enumerate_preconditions(m, a, "fx")
check("fixture: 15 sourced records, 0 unsourced", res["n"] == 15 and res["unsourced"] == 0)
check("fixture: exactly one argued (cores), ratio 14.0", res["unargued"] == 14 and res["ratio"] == 14.0)
check("every class in CLASSES reached except PRIOR_RESULT (fixture has none; visible zero)",
      {r["class"] for r in res["records"]} == set(p1.CLASSES) - {"PRIOR_RESULT"})
check("METHOD head is the cited author", [r["head"] for r in res["records"] if r["class"] == "METHOD"] == ["heiri"])
bad = dict(res["records"][0]); bad["source"] = dict(bad["source"], span=[0, 4])
check("planted wrong span -> UNSOURCED", p1.validate(bad, m)["state"] == "UNSOURCED")
check("every span slices out its own text", all(m[r["source"]["span"][0]:r["source"]["span"][1]] == r["source"]["text"] for r in res["records"]))
check("no dependency language -> EMPTY, ratio None", p1.enumerate_preconditions("We looked at it and it was fine.", "fine")["state"] == "EMPTY")
check("empty methods -> EMPTY, typed", p1.enumerate_preconditions("", "x")["state"] == "EMPTY")
check("nothing argued -> ratio undefined, never large", p1.enumerate_preconditions("a calibrated balance", "")["ratio"] is None)
check("no network module in P1", not ({"urllib", "socket", "http"} & {n.names[0].name.split(".")[0] for n in ast.walk(ast.parse(open(os.path.join(HERE, "p1_dependency_records.py")).read())) if isinstance(n, ast.Import)}))

# ---------------------------------------------------------------- P5
section("P5: lag declaration")
g = [p5.gate(x) for x in p5.ANCHORS]
check("antibiotic anchor -> DECLARED_UNKNOWN, ratio > 1000", g[0]["state"] == "DECLARED_UNKNOWN" and g[0]["ratio"] > 1000)
check("trial anchor -> DECLARED_UNKNOWN", g[1]["state"] == "DECLARED_UNKNOWN")
check("same-window -> TRACKED", g[2]["state"] == "TRACKED")
check("undeclared t_visible -> UNDECLARED with ratio None (not 0)", g[3]["state"] == "UNDECLARED" and g[3]["ratio"] is None)
check("planted zero t_scored -> UNDECLARED, no division", p5.gate({"t_visible_s": 5, "t_scored_s": 0})["state"] == "UNDECLARED")
check("threshold boundary: 10.0 -> DECLARED_UNKNOWN, 9.99 -> TRACKED", p5.gate({"t_visible_s": 10, "t_scored_s": 1})["state"] == "DECLARED_UNKNOWN" and p5.gate({"t_visible_s": 9.99, "t_scored_s": 1})["state"] == "TRACKED")
check("C1 coded from clocks on anchors: PRESENT PRESENT ABSENT UNCODED", [x["C1"] for x in g] == ["PRESENT", "PRESENT", "ABSENT", "UNCODED"])
check("gate blocks nothing: every action returns a state", all(x["state"] in p5.STATES for x in g))

# ---------------------------------------------------------------- folder
section("folder constraints")
files = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
stdlib = set(sys.stdlib_module_names)
local = {f[:-3] for f in files}
for f in files:
    tree = ast.parse(open(os.path.join(HERE, f)).read(), feature_version=(3, 9))
    mods = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            mods |= {a.name.split(".")[0] for a in n.names}
        elif isinstance(n, ast.ImportFrom) and n.module:
            mods.add(n.module.split(".")[0])
    check("%s: parses under 3.9, imports stdlib or this folder only" % f, mods <= (stdlib | local))
for f in files:
    if f in ("selftest.py", "run_all.py"):
        continue
    check("%s: under 300 lines" % f, len(open(os.path.join(HERE, f)).read().splitlines()) < 300)
    rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
    check("%s refuses --selftest (exit 2)" % f, rc == 2)
check("no cross-folder import (nothing from ../)", all(".." not in open(os.path.join(HERE, f)).read().split("sys.path")[1][:40] for f in files if "sys.path" in open(os.path.join(HERE, f)).read()))
buf = io.StringIO()
with redirect_stdout(buf):
    import run_all
    run_all.main()
out = buf.getvalue()
check("run_all prints the contamination declaration before any part", out.index("CONTAMINATION DECLARATION") < out.index("P2 substrate check"))

print("\nchecks: %d   failed: %d" % (N, len(FAILED)))
for f in FAILED:
    print("  FAILED: " + f)
sys.exit(1 if FAILED else 0)
