#!/usr/bin/env python3
"""Checker for run 2. Stdlib only.   python3 check_run2.py   (exit 1 if a check fails)"""
import hashlib
import json
import os
import subprocess
import sys

import finalize2
import tighten

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(HERE)

rec = json.load(open(os.path.join(HERE, "records.json"), encoding="utf-8"))
res = []


def check(name, ok, detail=""):
    res.append((bool(ok), name, detail))


check("every part file has the hash recorded", all(hashlib.sha256(open(os.path.join(HERE, n), "rb").read()).hexdigest() == h for n, h in rec["parts"].items()))
check("records.json equals a rebuild (every count and table recomputed from the part files)", json.loads(json.dumps(finalize2.build(), ensure_ascii=False)) == rec)
check("run 1 files are unchanged since the commit before run 2",
      subprocess.run(["git", "-C", R1, "diff", "--quiet", "ca7fe199", "--", ".", ":(exclude)run_2"]).returncode == 0)
check("item 1: no verdict is attributed to an independent model; the model auditor reads NOT_RUN with a reason; agreement is void",
      rec["item_1"]["independent_model_auditor"] == "NOT_RUN" and rec["item_1"]["reason"] and rec["item_1"]["agreement_between_independent_auditors"] is None)
claims = {json.loads(l)["claim_id"]: json.loads(l) for l in open(os.path.join(R1, "claims.jsonl"), encoding="utf-8")}
check("item 2: all 8 side-note lines are present, quoted as in run 1, each with a class or a void reason; every class has its four cells",
      len(rec["item_2"]["claims"]) == 8 and all(p["quote"] == claims[p["claim_id"]]["quote"] and p["reason"] for p in rec["item_2"]["claims"])
      and all(len(p["cells"]) == 4 for p in rec["item_2"]["claims"] if p["class"]))
pr = json.load(open(os.path.join(HERE, "probe_readings.json"), encoding="utf-8"))["readings"]
r1 = json.load(open(os.path.join(R1, "records.json"), encoding="utf-8"))
probe1 = {v["claim_id"]: v["verdict"] for v in r1["verdicts"] if v["basis"] == "probe"}
check("item 3: exactly the 101 probe-based verdicts of run 1 are read, each quote as in run 1, each with a reason and an auditor",
      {p["claim_id"]: p["run_1_probe_verdict"] for p in pr} == probe1 and len(pr) == 101
      and all(p["quote"] == claims[p["claim_id"]]["quote"] and p["reason"] and p["auditor"] for p in pr))
check("item 4: tightened.json equals a rebuild; kept + removed = run 1 candidates", tighten.build() == json.load(open(os.path.join(HERE, "tightened.json")))
      and rec["item_4"]["kept"] + sum(rec["item_4"]["removed_by_rule"].values()) == len(claims))
s5 = rec["item_5"]
check("item 5: a spec with nothing testable is void, not MATCH; every rate prints n; no void inside a rate",
      all((s["fidelity"]["match"] is None) == (s["items_tested"] == 0) for s in s5["specs"])
      and all(c["n"] == c["MATCH"] + c["DRIFT"] for t in s5["tables"].values() for c in t.values()))
blob = json.dumps(rec).lower()
check("agency is void everywhere and no intent label is used", rec["agency"] is None and "sabotage" not in blob and all(p["agency"] is None for p in pr))
for ok, name, detail in res:
    print("%-5s %s  %s" % ("PASS" if ok else "FAIL", name, detail))
fails = sum(not ok for ok, _, _ in res)
print("checks: %d   failed: %d" % (len(res), fails))
sys.exit(1 if fails else 0)
