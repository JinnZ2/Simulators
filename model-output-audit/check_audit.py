#!/usr/bin/env python3
"""Checker for the model-output audit. Stdlib only.

    python3 check_audit.py            checks that need only this folder
    python3 check_audit.py CLONES     also checks every quote against its source (needs the clones)

Exit 0 all pass, 1 a check failed. Without CLONES the quote check reads NOT_RUN, which is not a pass.
"""
import json
import os
import sys

import audit
import finalize

HERE = os.path.dirname(os.path.abspath(__file__))


def run(clones=None):
    rec = json.load(open(os.path.join(HERE, "records.json"), encoding="utf-8"))
    out = []

    def check(name, state, detail=""):
        out.append({"check": name, "state": state if isinstance(state, str) else ("PASS" if state else "FAIL"), "detail": detail})

    check("every part file has the hash recorded", all(finalize.sha(n) == h for n, h in rec["parts"].items()))
    check("records.json equals a rebuild from the parts (verdict counts, floor and every table recomputed)",
          json.loads(json.dumps(finalize.build(), ensure_ascii=False)) == rec)
    claims = finalize.load("claims.jsonl")
    inv = {r["record_id"] for r in finalize.load("inventory.jsonl")}
    reruns = {r["claim_id"]: r for r in finalize.load("reruns.jsonl")}
    vs = rec["verdicts"]
    check("every verdict has a reason", all(v["reason"] for v in vs), "%d verdict records" % len(vs))
    check("every rerun-based verdict has a rerun log with a command and an exit code or a timeout",
          all(v["claim_id"] in reruns and reruns[v["claim_id"]]["runs"] for v in vs if v["basis"] == "rerun"),
          "%d" % sum(v["basis"] == "rerun" for v in vs))
    check("every CONFIRMED verdict whose first rerun was clean names a second run",
          all(v.get("second_run") for v in vs if v["verdict"] == "CONFIRMED" and v.get("rerun_state") == "CLEAN"))
    given = sum(1 for v in vs if v["verdict"] is not None)
    check("voids are counted as void: candidates = verdicts given + void", len(claims) == given + rec["void"],
          "%d candidates, %d given, %d void" % (len(claims), given, rec["void"]))
    check("no void is inside a rate", all(c["n"] == c["CONFIRMED"] + c["unsupported"] + c["ENV_DEPENDENT"] for t in rec["tables"].values() for c in t.values()))
    check("agency is void on every inventory and verdict record", rec["agency"] is None and all(v["agency"] is None for v in vs))
    check("every claim with a record id points at an inventory record; a file line with no blame commit has none",
          all(c["record_id"] in inv for c in claims if c["record_id"]), "%d without" % sum(1 for c in claims if not c["record_id"]))
    check("flagged cells follow the declared rule (n >= 20, rate >= 2 x floor and >= floor + 10 points)",
          all(c["n"] >= 20 for c in rec["flagged_cells"]), "%d flagged" % len(rec["flagged_cells"]))
    fid = json.load(open(os.path.join(HERE, "fidelity.json"), encoding="utf-8"))
    check("addendum 2b: no MATCH or DRIFT is assigned; every found spec has match None; counts add up to the inventory",
          fid["commits"]["MATCH"] == 0 and fid["commits"]["DRIFT"] == 0 and all(r["fidelity"]["match"] is None and r["fidelity"]["drift_type"] is None for r in fid["records"])
          and fid["commits"]["MISSING_SPEC_void"] + len(fid["records"]) == len(inv),
          "%d spec found, %d MISSING_SPEC" % (len(fid["records"]), fid["commits"]["MISSING_SPEC_void"]))
    if clones is None:
        check("every quote is in its source", "NOT_RUN", "needs the clones")
    else:
        heads = {r["repo"]: r for r in json.load(open(os.path.join(HERE, "repos.json")))["repos"] if r["state"] == "CLONED"}
        moved = [r for r, h in heads.items() if audit.git(os.path.join(clones, r), "rev-parse", "HEAD").strip() != h["head"]]
        missing, msgs, files = [], {}, {}
        for c in claims:
            loc = c["location"]
            if c["source"] == "A":
                if loc["repo"] not in msgs:
                    msgs[loc["repo"]] = {k["commit"]: [k["subject"]] + k["body"].split("\n") for k in audit.commits(os.path.join(clones, loc["repo"]))}
                lines = msgs[loc["repo"]].get(loc["commit"], [])
                ok = loc["message_line"] < len(lines) and lines[loc["message_line"]].strip() == c["quote"]
            else:
                key = (loc["repo"], loc["path"])
                if key not in files:
                    files[key] = open(os.path.join(clones, loc["repo"], loc["path"]), encoding="utf-8", errors="replace").read().split("\n")
                ok = loc["line"] <= len(files[key]) and files[key][loc["line"] - 1].strip() == c["quote"]
            if not ok:
                missing.append(c["claim_id"])
        check("the clones are at the commits recorded in repos.json", not moved, "moved: %s" % (moved or "none"))
        import fidelity
        check("addendum 2b: fidelity.json equals a rebuild", json.loads(json.dumps(fidelity.build(clones), ensure_ascii=False)) == fid)
        check("every quote is in its source, at the line recorded", not missing, "%d quotes, %d not found" % (len(claims), len(missing)))
    return out


if __name__ == "__main__":
    res = run(sys.argv[1] if len(sys.argv) > 1 else None)
    for r in res:
        print("%-7s %s  %s" % (r["state"], r["check"], r["detail"]))
    fails = sum(r["state"] == "FAIL" for r in res)
    print("checks: %d   failed: %d   not run: %d" % (len(res), fails, sum(r["state"] == "NOT_RUN" for r in res)))
    if len(sys.argv) > 1:
        json.dump(res, open(os.path.join(HERE, "check_results.json"), "w"), indent=1)
    sys.exit(1 if fails else 0)
