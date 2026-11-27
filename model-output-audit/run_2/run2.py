#!/usr/bin/env python3
"""Run 2, mechanical parts. Stdlib only. Rules: run_2/DECLARED.json.

    python3 run2.py reruns CLONES WORK BARE_PYTHON   -> repeat_reruns.json, pass_claims_runs.json
    python3 run2.py tighten                          -> tightened.json

BARE_PYTHON is the interpreter of a fresh venv with no packages; it is run with -I.
"""
import collections
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(HERE)
sys.path.insert(0, R1)
import audit      # noqa: E402
import finalize   # noqa: E402

PASS_CLAIMS = {   # the auditor's reading of what each side-note line states, and the command it gives
    "B:Simulators:KNOWN_RED.md:138:test_failure": ("states a pass: 28 checks, 0 failed", ["falsifier-audit/selftest_fa.py"], "."),
    "B:Simulators:TOOL_FINDER/TOOL_FINDER.md:378:test_failure": ("states a pass: 28 checks, 0 failed", ["falsifier-audit/selftest_fa.py"], "."),
    "B:Simulators:external-audit/DEEP_RESEARCH_2026_09_14_V2.md:84:test_failure": ("states a pass: 28 checks, 0 failed (an outside document landed verbatim)", ["falsifier-audit/selftest_fa.py"], "."),
    "B:Simulators:forest-model-ledger/CLAIM_TABLE.md:37:cant_run": ("does not state a pass for check_ledger.py: it says the checker fails on drift", None, None),
    "B:Simulators:forest-model-ledger/CLAIM_TABLE.md:69:test_failure": ("does not state a pass: it states that three held-out tools fail, which is what the run prints", None, None),
    "B:Simulators:stability-trigger-envelope/README.md:19:test_failure": ("states a pass: 217 checks, 0 failed", ["test_envelope.py"], "stability-trigger-envelope"),
    "B:Simulators:stability-trigger-envelope/RUN_NOTE.md:174:test_failure": ("states a pass: 217 checks, 0 failed, run once", ["test_envelope.py"], "stability-trigger-envelope"),
    "B:Mandala-Computing:CLAUDE.md:855:test_failure": ("states what the run should report: 422 passed, 0 failed", ["tests/test_core.py"], "."),
}


def worktree(clones, work, repo, rev):
    wt = os.path.join(work, "%s-%s" % (repo, rev[:12]))
    if not os.path.isdir(wt):
        subprocess.run(["git", "-C", os.path.join(clones, repo), "worktree", "add", "-f", "--detach", wt, rev], capture_output=True)
    return wt


def run(py, args, cwd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    try:
        r = subprocess.run(py + args, cwd=cwd, env=env, stdin=subprocess.DEVNULL, capture_output=True, timeout=180)
        out = (r.stdout + r.stderr).decode("utf-8", "replace")
        state = "PASS" if r.returncode == 0 and not audit.FAILLINE.search(out[-1500:]) else ("ENV_ERROR" if audit.ENVERR.search(out[-1500:]) else "FAILS")
        return {"exit": r.returncode, "state": state, "tail": out[-600:]}
    except subprocess.TimeoutExpired:
        return {"exit": None, "state": "TIMEOUT", "tail": "TIMEOUT after 180 s"}


def reruns(clones, work, bare):
    envs = {"bare": [bare, "-I"], "current": ["python3"]}
    claims = {c["claim_id"]: c for c in finalize.load("claims.jsonl")}
    heads = {r["repo"]: r["head"] for r in json.load(open(os.path.join(R1, "repos.json")))["repos"] if r["state"] == "CLONED"}
    out = []
    for cid, (reading, cmd, cwd) in PASS_CLAIMS.items():
        c = claims[cid]
        rec = {"claim_id": cid, "quote": c["quote"], "reading": reading, "auditor": "Anthropic model (this session)", "cells": {}}
        if cmd:
            repo = c["location"]["repo"]
            for tname, rev in (("writing_commit", c["location"]["written_by_commit"]), ("head", heads[repo])):
                wt = worktree(clones, work, repo, rev)
                for ename, py in envs.items():
                    rec["cells"]["%s/%s" % (tname, ename)] = dict(run(py, cmd, os.path.join(wt, cwd)), rev=rev[:12], command="python3 " + " ".join(cmd), cwd=cwd)
        out.append(rec)
    json.dump(out, open(os.path.join(HERE, "pass_claims_runs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    # second mechanical pass over the decided claims: same command, same tree
    rec1 = json.load(open(os.path.join(R1, "records.json"), encoding="utf-8"))
    r1 = {r["claim_id"]: r for r in finalize.load("reruns.jsonl")}
    rep = []
    for v in rec1["verdicts"]:
        if v["basis"] != "rerun" or v["verdict"] in (None, "NOT_A_CLAIM"):
            continue
        rr = r1[v["claim_id"]]
        wt = worktree(clones, work, rr["repo"], rr["rev"])
        last = rr["runs"][-1]
        res = run(["python3"], [rr["target"] if last["cwd"] == "." else os.path.basename(rr["target"])], os.path.join(wt, last["cwd"]))
        s1 = {"CLEAN": "PASS", "FAILS": "FAILS", "ENV_ERROR": "ENV_ERROR", "TIMEOUT": "TIMEOUT", "NEEDS_ARGUMENTS": "FAILS"}[rr["rerun_state"]]
        rep.append({"claim_id": v["claim_id"], "run_1_verdict": v["verdict"], "run_1_rerun": s1, "run_2_rerun": res["state"], "same": s1 == res["state"],
                    "exit": res["exit"], "tail": res["tail"][-300:], "auditor": "stdlib rerun, second pass (mechanical)"})
    json.dump(rep, open(os.path.join(HERE, "repeat_reruns.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("repeat reruns:", len(rep), "same:", sum(r["same"] for r in rep))
    for r in out:
        print(r["claim_id"][:60], {k: v["state"] for k, v in r["cells"].items()})


if __name__ == "__main__":
    if sys.argv[1] == "reruns":
        reruns(*sys.argv[2:5])
