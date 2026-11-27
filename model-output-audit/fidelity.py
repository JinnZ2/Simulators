#!/usr/bin/env python3
"""Addendum 2b, first step: where is a spec recoverable. Stdlib only. Rule: DECLARED.json, amendments[0].

    python3 fidelity.py CLONES     -> fidelity.json

Assigns MISSING_SPEC (void) or None (spec found, not yet compared). Never MATCH, never DRIFT.
"""
import collections
import hashlib
import json
import os
import re
import sys

import audit

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = re.compile(r"^(WORK_ORDER|DISPATCH|SPEC|SOURCE_DROP|ADDENDUM|ORDER)[\w.-]*\.(md|txt)$")


def build(clones):
    repos = [r for r in json.load(open(os.path.join(HERE, "repos.json")))["repos"] if r["state"] == "CLONED"]
    specs, by_folder = [], {}
    for r in repos:
        path = os.path.join(clones, r["repo"])
        for f in audit.git(path, "ls-files", "-z").split("\0"):
            if f and SPEC.match(os.path.basename(f)):
                folder = os.path.dirname(f)
                code = [g for g in audit.git(path, "ls-files", "-z", "--", folder or ".").split("\0") if g.endswith(".py")] if folder else []
                specs.append({"repo": r["repo"], "spec_source": f, "sha256": hashlib.sha256(open(os.path.join(path, f), "rb").read()).hexdigest(),
                              "folder": folder or "(repo root)", "code_files_in_folder": len(code)})
                by_folder.setdefault(r["repo"], {}).setdefault(folder, []).append(f)
    records, counts = [], collections.Counter()
    per_model = collections.defaultdict(collections.Counter)
    for l in open(os.path.join(HERE, "inventory.jsonl"), encoding="utf-8"):
        rec = json.loads(l)
        folders = by_folder.get(rec["repo"], {})
        found = sorted({s for p in rec["paths"] for fo, ss in folders.items() if fo and (p == fo or p.startswith(fo + "/")) for s in ss})
        state = "SPEC_FOUND_NOT_COMPARED" if found else "MISSING_SPEC"
        counts[state] += 1
        per_model[str(rec["model"]) + (" " + rec["model_version"] if rec["model_version"] else "")][state] += 1
        if found:
            records.append({"record_id": rec["record_id"], "model": rec["model"], "model_version": rec["model_version"], "date": rec["date"][:10],
                            "fidelity": {"spec_source": found, "match": None, "drift_type": None}})
    return {"record": "SPEC_FIDELITY_STEP_2B", "date": "2026-11-27", "status": "PROPOSED", "observer_slots": None,
            "order": "ADDENDUM_2b.md (received cut off)", "rule": "DECLARED.json amendments[0]",
            "spec_files": len(specs), "repos_with_a_spec_file": len({s["repo"] for s in specs}),
            "commits": {"total": sum(counts.values()), "MISSING_SPEC_void": counts["MISSING_SPEC"],
                        "spec_found_match_None": counts["SPEC_FOUND_NOT_COMPARED"], "MATCH": 0, "DRIFT": 0},
            "by_model": {k: dict(v) for k, v in sorted(per_model.items())},
            "missing_spec_fidelity": {"spec_source": None, "match": "MISSING_SPEC", "drift_type": None},
            "note": "paths are the first 50 changed paths recorded per commit in inventory.jsonl; a commit touching more may be undercounted",
            "specs": specs, "records": records}


if __name__ == "__main__":
    out = build(sys.argv[1])
    json.dump(out, open(os.path.join(HERE, "fidelity.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print({k: out[k] for k in ("spec_files", "repos_with_a_spec_file", "commits")})
    for k, v in out["by_model"].items():
        print("  %-24s %s" % (k, v))
    import collections as c
    print(c.Counter(s["repo"] for s in out["specs"]).most_common(8))
