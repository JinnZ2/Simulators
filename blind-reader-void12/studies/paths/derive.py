"""Per-path counts from walks.jsonl. No score, no ranking, no winner. Stdlib only.
Run: python3 derive.py [walks.jsonl] [paths.json]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOMES = ("holds", "needs_exception", "breaks", "void")
EXPOSURE = ("yes", "no", "unknown")
FIELDS = ("path_id", "walk_id", "reader_family", "L", "exposure_prior_walks", "case", "outcome",
          "repair_needed", "provenance", "date")

def load(walks_path, paths_path):
    paths = {p["path_id"]: p for p in json.load(open(paths_path, encoding="utf-8"))["paths"]}
    walks = [json.loads(l) for l in open(walks_path, encoding="utf-8") if l.strip()]
    return paths, walks

def errors(paths, walks):
    errs, seen = [], set()
    for w in walks:
        wid = w.get("walk_id")
        for f in FIELDS:
            if f not in w: errs.append("%s: missing field %s" % (wid, f))
        if w.get("path_id") not in paths: errs.append("%s: unknown path %s" % (wid, w.get("path_id")))
        if w.get("outcome") not in OUTCOMES: errs.append("%s: outcome %r" % (wid, w.get("outcome")))
        if w.get("exposure_prior_walks") not in EXPOSURE: errs.append("%s: exposure %r" % (wid, w.get("exposure_prior_walks")))
        if w.get("L") is not None and w.get("L") not in (0, 1, 2, 3, 4): errs.append("%s: L %r" % (wid, w.get("L")))
        if wid in seen: errs.append("%s: duplicate walk_id" % wid)
        seen.add(wid)
    return errs

def column(w):
    e = w["exposure_prior_walks"]
    if e == "yes": return "traffic"
    if e == "unknown": return "exposure_unknown"
    return "independent" if (w["L"] is not None and w["L"] >= 2) else "dependent"

def derive(paths, walks):
    out = {}
    for pid, p in paths.items():
        ws = [w for w in walks if w["path_id"] == pid]
        cols = {c: [w for w in ws if column(w) == c] for c in ("independent", "traffic", "exposure_unknown", "dependent")}
        out[pid] = {"gap_id": p["gap_id"], "walks": len(ws),
                    "by_column": {c: len(v) for c, v in cols.items()},
                    "outcomes": {c: {o: sum(w["outcome"] == o for w in v) for o in OUTCOMES} for c, v in cols.items()},
                    "repairs": [w["repair_needed"] for w in ws if w["repair_needed"]],
                    "independent_cases": len({w["case"] for w in cols["independent"]}),
                    "independent_families": len({w["reader_family"] for w in cols["independent"]})}
    return out

def render(d):
    lines = ["path                   gap        walks  indep  traffic  exp?  dep  | independent: holds exc breaks void | cases fams"]
    for pid, r in d.items():
        o = r["outcomes"]["independent"]
        b = r["by_column"]
        lines.append("%-22s %-10s %5d  %5d  %7d  %4d  %3d  | %18d %3d %6d %4d | %5d %4d" % (
            pid, r["gap_id"], r["walks"], b["independent"], b["traffic"], b["exposure_unknown"], b["dependent"],
            o["holds"], o["needs_exception"], o["breaks"], o["void"], r["independent_cases"], r["independent_families"]))
    lines.append("no score, no ranking: traffic, unknown-exposure and dependent walks are counted apart and never added to independent")
    return "\n".join(lines)

if __name__ == "__main__":
    a = sys.argv[1:]
    paths, walks = load(a[0] if a else os.path.join(HERE, "walks.jsonl"), a[1] if len(a) > 1 else os.path.join(HERE, "paths.json"))
    e = errors(paths, walks)
    if e: print("\n".join(e)); sys.exit(1)
    print("walks recorded: %d" % len(walks)); print(render(derive(paths, walks)))
