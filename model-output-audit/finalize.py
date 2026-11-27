#!/usr/bin/env python3
"""Join claims, reruns and readings into records.json and the pattern tables. Stdlib only.

    python3 finalize.py
"""
import collections
import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PASSLINE = re.compile(r"\b0 (failed|failures)\b|\bOK\b|\bPASS\b|\bGREEN\b")
CODELINE = re.compile(r"^(print\(|#|//|python3? |\$ |except |import |from |raise |return |\"|'|\{\")")
H = re.compile(r"\b((?:[a-z0-9-]+\.)+(?:org|com|gov|edu|net|io|int|ai))\b", re.I)


def sha(name):
    return hashlib.sha256(open(os.path.join(HERE, name), "rb").read()).hexdigest()


def load(name):
    return [json.loads(l) for l in open(os.path.join(HERE, name), encoding="utf-8")]


def rate(cells):
    den = cells["CONFIRMED"] + cells["UNSUPPORTED"] + cells["ENV_DEPENDENT"]
    return {"n": den, "unsupported": cells["UNSUPPORTED"], "rate": (cells["UNSUPPORTED"] / den) if den else None}


def build():
    inv = {r["record_id"]: r for r in load("inventory.jsonl")}
    claims = load("claims.jsonl")
    reruns = {r["claim_id"]: r for r in load("reruns.jsonl")}
    R = json.load(open(os.path.join(HERE, "readings.json"), encoding="utf-8"))
    probes = {p["host"]: p for p in json.load(open(os.path.join(HERE, "probes.json")))["hosts"]}
    verdicts = []
    for c in claims:
        rec = inv.get(c["record_id"]) or {}
        v = {"claim_id": c["claim_id"], "record_id": c["record_id"], "model": rec.get("model"), "model_version": rec.get("model_version"),
             "date": (rec.get("date") or "")[:10] or None, "repo": c["location"]["repo"], "artifact_type": rec.get("artifact_type"),
             "claim_type": c["claim_type"], "verdict": None, "basis": None, "reason": "not in the rerun subset: the quote names no single runnable file", "agency": None}
        rr = reruns.get(c["claim_id"])
        if rr:
            v["basis"], v["rerun_state"] = "rerun", rr["rerun_state"]
            read = next((x for k, x in R["readings"].items() if c["claim_id"].startswith(k)), None)
            if read and read[0] == "__LID_NUMPY__":
                read = (["ENV_DEPENDENT", "quote says scripts/discover.py fails with ModuleNotFoundError because numpy is not declared; numpy is present in this container, so the rerun is clean here and would fail without it", None]
                        if "discover.py" in c["quote"] and re.search(r"numpy", c["quote"]) else None)
            if read:
                v["verdict"], v["reason"], v["second_run"] = read
            elif rr["rerun_state"] == "TIMEOUT":
                v["verdict"], v["reason"] = "UNVERIFIABLE", "the rerun exceeded 120 s"
            elif rr["rerun_state"] == "NEEDS_ARGUMENTS":
                v["reason"] = "the file needs arguments the quote does not give; not adjudicated"
            elif rr["rerun_state"] == "ENV_ERROR":
                v["reason"] = ("the file is a package module and does not run as a script; the rerun method does not apply"
                               if "relative import" in rr["runs"][-1]["tail"] else "the rerun stopped on a missing module or file; the quote was not adjudicated")
            else:
                why = ("a pass count or pass mark for the file, not a failure claim" if PASSLINE.search(c["quote"]) and not re.search(r"\b[1-9]\d* (failed|failures)", c["quote"])
                       else "a code, usage or command line that mentions a failure word" if CODELINE.search(c["quote"])
                       else "auditor's reading: mentions a failure word (fixed, past, a description, a rule, or about another object) and does not assert that the named file fails in this tree")
                v["verdict"], v["reason"] = "NOT_A_CLAIM", why
                if rr["rerun_state"] == "FAILS" and why.startswith("a pass count"):
                    v["side_note"] = "PASS_CLAIM_RERUN_FAILS"
        elif c["claim_type"] in ("cant_run", "environment"):
            hs = sorted({h.lower() for h in H.findall(c["quote"])} & set(probes))
            if hs:
                reached = [h for h in hs if probes[h]["state"] == "REACHED"]
                v["basis"], v["hosts"] = "probe", hs
                if reached:
                    v["verdict"], v["reason"] = "ENV_DEPENDENT", "names %s, reachable from this session now; sessions do not share one network policy" % ", ".join(reached)
                else:
                    v["verdict"], v["reason"] = "DECLARED_LIMIT", "names %s, refused from this session too; the line was not read to confirm it states a limit" % ", ".join(hs)
        verdicts.append(v)
    counts = collections.Counter(str(v["verdict"]) for v in verdicts)
    rer = [v for v in verdicts if v["basis"] == "rerun"]

    def table(key):
        cells = collections.defaultdict(collections.Counter)
        for v in rer:
            cells[str(key(v))][str(v["verdict"])] += 1
        return {k: dict(rate(c), CONFIRMED=c["CONFIRMED"], ENV_DEPENDENT=c["ENV_DEPENDENT"], NOT_A_CLAIM=c["NOT_A_CLAIM"],
                        UNVERIFIABLE=c["UNVERIFIABLE"], void=c["None"]) for k, c in sorted(cells.items())}
    allc = collections.Counter(str(v["verdict"]) for v in rer)
    floor = rate(allc)
    tables = {"model": table(lambda v: v["model"]), "model_version": table(lambda v: "%s %s" % (v["model"], v["model_version"]) if v["model"] else None),
              "month": table(lambda v: (v["date"] or "")[:7] or None), "repo": table(lambda v: v["repo"]), "artifact_type": table(lambda v: v["artifact_type"])}
    flagged = [{"table": t, "cell": k, **c} for t, tb in tables.items() for k, c in tb.items()
               if c["n"] >= 20 and c["rate"] is not None and floor["rate"] is not None and c["rate"] >= 2 * floor["rate"] and c["rate"] >= floor["rate"] + 0.10 and c["rate"] > 0]
    cand = collections.defaultdict(collections.Counter)
    for v in verdicts:
        cand[str(v["model"])][v["claim_type"]] += 1
    invc = collections.Counter((r["model"], r["model_version"]) for r in inv.values())
    return {"record": "MODEL_OUTPUT_AUDIT", "date": "2026-11-27", "status": "PROPOSED", "license": "CC0", "co_authored": True, "observer_slots": None,
            "parts": {n: sha(n) for n in ("WORK_ORDER.md", "DECLARED.json", "patterns.json", "org_listing.txt", "repos.json", "inventory.jsonl",
                                          "claims.jsonl", "subset.json", "reruns.jsonl", "readings.json", "probes.json")},
            "inventory": {"commits": len(inv), "by_model": [{"model": m, "model_version": ver, "commits": n} for (m, ver), n in invc.most_common()],
                          "untagged_commits_model_void": invc[(None, None)]},
            "claims": {"candidates": len(claims), "from_commit_messages": sum(c["source"] == "A" for c in claims),
                       "from_head_file_lines": sum(c["source"] == "B" for c in claims),
                       "by_type": dict(collections.Counter(c["claim_type"] for c in claims)),
                       "candidates_by_model_and_type": {m: dict(c) for m, c in sorted(cand.items())}},
            "verdict_counts": dict(counts), "void": counts["None"],
            "rerun_subset": {"n": len(rer), "counts": dict(allc)},
            "floor": floor, "tables": tables, "flagged_cells": flagged,
            "side_notes": {"pass_claims_whose_rerun_failed_here": [{"claim_id": v["claim_id"], "model": v["model"], "date": v["date"]} for v in verdicts if v.get("side_note")],
                           "note": "outside the order's question (these are pass claims, not failure claims); not adjudicated"},
            "agency": None, "agency_reason": "void on every record: nothing outside the repos was opened",
            "verdicts": [v for v in verdicts if v["basis"]]}


if __name__ == "__main__":
    rec = build()
    json.dump(rec, open(os.path.join(HERE, "records.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(json.dumps({k: rec[k] for k in ("verdict_counts", "rerun_subset", "floor", "flagged_cells")}, indent=1))
    for t in ("model_version", "artifact_type"):
        print(t)
        for k, c in rec["tables"][t].items():
            print("  %-28s n=%-3d unsupported=%d confirmed=%d env=%d not_a_claim=%d void=%d" % (k, c["n"], c["unsupported"], c["CONFIRMED"], c["ENV_DEPENDENT"], c["NOT_A_CLAIM"], c["void"]))
    print(len(rec["side_notes"]["pass_claims_whose_rerun_failed_here"]), "pass claims whose rerun failed here")
