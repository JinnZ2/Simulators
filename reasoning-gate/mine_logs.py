# mine_logs.py  — CC0-1.0, stdlib only
# reads a dir of gate_*.json, reports what fired, what never
# fired, and divergences no guard caught.
import json, glob, os, sys
from collections import Counter

def load(d):
    for p in sorted(glob.glob(os.path.join(d, "gate_*.json"))):
        with open(p) as fh:
            yield p, json.load(fh)

def mine(d, guards_path="guards.json"):
    all_ids = [g["id"] for g in json.load(open(guards_path))["guards"]]
    fires, runs, uncaught, voids = Counter(), 0, [], 0
    for path, r in load(d):
        runs += 1
        fired = set()
        for f in r.get("findings", []):
            fires[f["guard"]] += 1
            fired.add(f["guard"])
        voids += len(r.get("voided_ratios", []))
        exp = (r.get("expected") or "").strip()
        obs = (r.get("observed") or "").strip()
        if exp and obs and exp != obs and not fired:
            uncaught.append((r["sim_id"], exp, obs))
    print("runs: %d   voided ratios: %d" % (runs, voids))
    print("\nguard hit rate")
    for gid in all_ids:
        n = fires[gid]
        print("  %-8s %3d  %5.1f%%%s" % (
            gid, n, 100.0*n/runs if runs else 0,
            "   NEVER FIRED" if n == 0 else ""))
    print("\ndivergences with no guard attached  (the growth edge)")
    if not uncaught:
        print("  none")
    for sim, exp, obs in uncaught:
        print("  %s\n    expected: %s\n    observed: %s" % (sim, exp, obs))
    return {"runs": runs, "fires": dict(fires), "uncaught": uncaught}

if __name__ == "__main__":
    mine(sys.argv[1] if len(sys.argv) > 1 else ".",
         sys.argv[2] if len(sys.argv) > 2 else "guards.json")
