#!/usr/bin/env python3
"""selftest for tail-check. CC0, stdlib only. Prints checks: N failed: M."""
import os, sys, ast
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tail_check as tc  # noqa: E402

ok = total = 0
def check(cond, label):
    global ok, total
    total += 1
    if cond:
        ok += 1
    else:
        print("FAIL:", label)

T = [{"turn": 0, "text": "I drive a tanker route nights."}]
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "tanker route"}, "user_turns": T})
check(r["verdict"] == "SAID", "literal span -> SAID")
check(T[0]["text"][r["span"][0]:r["span"][1]] == "tanker route", "span slices back to claimed")
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "office job"}, "user_turns": T})
check(r["verdict"] == "FILLED", "no span -> FILLED")
r = tc.check({"inference": {"text": "x", "axis": "a"}, "user_turns": T})
check(r["verdict"] == "FILLED", "no claimed -> FILLED, not SAID")
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "Tanker Route"}, "user_turns": T})
check(r["verdict"] == "FILLED", "case differs -> FILLED (literal span rule)")
for bad, why in (({"inference": {"text": "x", "axis": "a", "claimed": "tanker"}, "user_turns": []}, "no turns"),
                 ({"inference": {"text": "x", "claimed": "tanker"}, "user_turns": T}, "no axis"),
                 ({"inference": {"axis": "a", "claimed": "tanker"}, "user_turns": T}, "no text")):
    check(tc.check(bad)["verdict"] == "UNRATED", "UNRATED on " + why)
off = [{"turn": 0, "quote": "tanker route nights", "position": "off_center", "declared_by": "op"}]
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "office"}, "user_turns": T, "axis_statements": off})
check(tc.FLAG in r["flags"], "FILLED + sourced off_center -> MEDIAN_FILL_RISK")
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "tanker"}, "user_turns": T, "axis_statements": off})
check(r["flags"] == [], "SAID never flagged")
at = [{"turn": 0, "quote": "tanker route nights", "position": "at_center", "declared_by": "op"}]
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "office"}, "user_turns": T, "axis_statements": at})
check(r["flags"] == [], "at_center does not flag")
fake = [{"turn": 0, "quote": "I live off grid", "position": "off_center", "declared_by": "op"}]
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "office"}, "user_turns": T, "axis_statements": fake})
check(r["flags"] == [] and r["axis_statements_unsourced"], "unsourced off_center statement not counted")
undecl = [{"turn": 0, "quote": "tanker route nights", "position": "off_center"}]
r = tc.check({"inference": {"text": "x", "axis": "a", "claimed": "office"}, "user_turns": T, "axis_statements": undecl})
check(r["flags"] == [], "off_center without declared_by not counted")
src = open(os.path.join(HERE, "tail_check.py"), encoding="utf-8").read()
names = {n.name for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef)}
check("find_span" not in names and "gate" not in names, "span logic imported from tools/sourced.py, not redefined")
check("from tools import sourced" in src, "imports tools.sourced")
check(tc.main(["--selftest"]) == 2, "module refuses --selftest")
import json
recs = json.load(open(os.path.join(HERE, "samples", "demo.json")))
vs = [tc.check(x)["verdict"] for x in recs]
check(vs == ["FILLED", "SAID", "FILLED", "UNRATED"], "demo verdicts %s" % vs)
check(set(vs) == set(tc.VERDICTS), "all three verdicts reached on demo")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
