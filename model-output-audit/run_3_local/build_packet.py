#!/usr/bin/env python3
"""Build packet.json: what the local auditor is shown. Stdlib only.

No run 1 or run 2 verdict, class, reading or reason goes in. Rules: DECLARED.json.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(HERE)
R2 = os.path.join(R1, "run_2")
FORBIDDEN = ("verdict", "class", "reading", "reason", "run_1_probe_verdict", "run_2_reading", "rerun_state", "state", "tail", "items_tested", "absent_names_read")


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def J(p):
    return json.load(open(p, encoding="utf-8"))


def build():
    claims = {c["claim_id"]: c for c in jl(os.path.join(R1, "claims.jsonl"))}
    reruns = {r["claim_id"]: r for r in jl(os.path.join(R1, "reruns.jsonl"))}
    heads = {r["repo"]: r["head"] for r in J(os.path.join(R1, "repos.json"))["repos"] if r["state"] == "CLONED"}
    r1 = J(os.path.join(R1, "records.json"))
    items = []

    def base(cid, kind):
        c = claims[cid]
        loc = c["location"]
        return {"item_id": "%s#%s" % (kind, cid), "claim_id": cid, "kind": kind, "repo": loc["repo"],
                "clone_url": "https://github.com/JinnZ2/%s" % loc["repo"], "quote": c["quote"],
                "location": {k: loc[k] for k in loc if k != "repo"}, "claim_type": c["claim_type"], "runs": [], "hosts": []}

    for v in r1["verdicts"]:
        if v["basis"] == "rerun" and v["verdict"] not in (None, "NOT_A_CLAIM"):
            it = base(v["claim_id"], "rerun")
            rr = reruns[v["claim_id"]]
            cwd = rr["runs"][-1]["cwd"]
            arg = rr["target"] if cwd == "." else os.path.basename(rr["target"])
            revs = [("run_1_tree", rr["rev"])]
            w = it["location"].get("written_by_commit") or it["location"].get("commit")
            if w and w != rr["rev"]:
                revs.append(("writing_commit", w))
            it["runs"] = [{"tree": t, "rev": rev, "cwd": cwd, "argv": ["python3", arg]} for t, rev in revs]
            items.append(it)
    for p in J(os.path.join(R2, "probe_readings.json"))["readings"]:
        it = base(p["claim_id"], "probe")
        it["quote"] = p["quote"]          # run 2 read the full line; the same text is shown here
        it["hosts"] = p["hosts"]
        items.append(it)
    for p in J(os.path.join(R2, "pass_claims_runs.json")):
        it = base(p["claim_id"], "pass")
        seen = {}
        for name, cell in p["cells"].items():
            tree = name.split("/")[0]
            if tree not in seen:
                full = heads[it["repo"]] if tree == "head" else it["location"]["written_by_commit"]
                assert full.startswith(cell["rev"])
                seen[tree] = {"tree": tree, "rev": full, "cwd": cell["cwd"], "argv": cell["command"].split()}
        it["runs"] = list(seen.values())
        items.append(it)

    cand = {(s["repo"], s["spec_source"]): s for s in J(os.path.join(R2, "fidelity_candidates.json"))["specs"]}
    match = [s for s in J(os.path.join(R2, "records.json"))["item_5"]["specs"] if s["fidelity"]["match"] == "MATCH"]
    match.sort(key=lambda s: cand[(s["repo"], s["spec_source"])]["spec_sha256"])
    fid = [{"repo": s["repo"], "clone_url": "https://github.com/JinnZ2/%s" % s["repo"], "rev": heads[s["repo"]],
            "spec_source": s["spec_source"], "spec_sha256": cand[(s["repo"], s["spec_source"])]["spec_sha256"],
            "code_folder": os.path.dirname(s["spec_source"]), "picked": i < 5} for i, s in enumerate(match)]

    pk = {"record": "MODEL_OUTPUT_AUDIT_RUN_3_PACKET", "status": "PROPOSED", "license": "CC0", "observer_slots": None,
          "note": "what the local auditor is shown. No earlier verdict is in this file.",
          "counts": {k: sum(1 for i in items if i["kind"] == k) for k in ("rerun", "probe", "pass")},
          "items": items, "specs_in_pool": len(fid), "specs": fid, "agency": None}

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                assert k not in FORBIDDEN, k
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(pk)
    return pk


if __name__ == "__main__":
    pk = build()
    s = json.dumps(pk, indent=1, ensure_ascii=False) + "\n"
    open(os.path.join(HERE, "packet.json"), "w", encoding="utf-8").write(s)
    print("items", len(pk["items"]), pk["counts"], "fidelity picked", sum(f["picked"] for f in pk["specs"]), "of", len(pk["specs"]),
          "sha256", hashlib.sha256(s.encode()).hexdigest()[:16])
