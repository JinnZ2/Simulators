#!/usr/bin/env python3
"""Run 2 item 5, mechanical part: constants and state tokens a spec writes, looked for in the code beside it.

    python3 fidelity2.py CLONES   -> fidelity_candidates.json

Output is candidates for reading. This step assigns no MATCH and no DRIFT.
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R1 = os.path.dirname(HERE)
sys.path.insert(0, R1)
import audit  # noqa: E402

CONST = re.compile(r"^\s*([A-Z][A-Z0-9_]{2,})\s*=\s*(-?\d+(?:\.\d+)?)\s*(?:#.*)?$", re.M)
TOKEN = re.compile(r"\b([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)\b")   # widened after the first pass: see README (backticked-only found 1 token in 20 specs)
N = 20


def build(clones):
    fid = json.load(open(os.path.join(R1, "fidelity.json"), encoding="utf-8"))
    inv = {}
    for l in open(os.path.join(R1, "inventory.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        inv[(r["repo"], r["commit"])] = r
    pool = [s for s in fid["specs"] if s["code_files_in_folder"] > 0 and s["folder"] != "(repo root)"]
    pool.sort(key=lambda s: hashlib.sha256((s["repo"] + "/" + s["spec_source"]).encode()).hexdigest())
    out = []
    for s in pool[:N]:
        path = os.path.join(clones, s["repo"])
        spec = open(os.path.join(path, s["spec_source"]), encoding="utf-8", errors="replace").read()
        pys = [f for f in audit.git(path, "ls-files", "-z", "--", s["folder"]).split("\0") if f.endswith(".py")]
        code = "\n".join(open(os.path.join(path, f), encoding="utf-8", errors="replace").read() for f in pys)
        first = None
        for f in pys:
            h = audit.git(path, "log", "--diff-filter=A", "--format=%H %aI", "--", f).strip().split("\n")[-1]
            if h and (first is None or h.split()[1] < first.split()[1]):
                first = h
        rec = inv.get((s["repo"], first.split()[0])) if first else None
        consts = []
        for name, val in CONST.findall(spec):
            m = re.search(r"^\s*%s\s*(?::[^=]+)?=\s*(-?\d+(?:\.\d+)?)" % re.escape(name), code, re.M)
            consts.append({"name": name, "spec_value": val, "code_value": m.group(1) if m else None,
                           "state": "SAME" if m and float(m.group(1)) == float(val) else ("DIFFERENT" if m else "NAME_NOT_ASSIGNED_IN_CODE")})
        tokens = sorted(set(TOKEN.findall(spec)))
        absent = [t for t in tokens if t not in code]
        out.append({"repo": s["repo"], "spec_source": s["spec_source"], "spec_sha256": s["sha256"], "code_files": len(pys),
                    "model": rec and rec["model"], "model_version": rec and rec["model_version"], "date": rec and rec["date"][:10],
                    "constants": consts, "tokens_in_spec": len(tokens), "tokens_absent_from_code": absent})
    return {"pool": len(pool), "sampled": len(out), "specs": out}


if __name__ == "__main__":
    o = build(sys.argv[1])
    json.dump(o, open(os.path.join(HERE, "fidelity_candidates.json"), "w"), indent=1)
    print("pool", o["pool"], "sampled", o["sampled"])
    for s in o["specs"]:
        print("%-62s %s %s | const %d (diff %s) | tokens %d absent %s" % (s["spec_source"][:62], s["model"], s["model_version"], len(s["constants"]),
              [(c["name"], c["spec_value"], c["code_value"]) for c in s["constants"] if c["state"] != "SAME"], s["tokens_in_spec"], s["tokens_absent_from_code"][:8]))
