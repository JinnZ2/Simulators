# mine_logs.py  — CC0-1.0, stdlib only
# reads a dir of gate_*.json, reports what fired, what never
# fired, and divergences no guard caught.
#
# Reads BOTH outcomes a run can have:
#   gate_<SIM>.json          the run closed
#   gate_<SIM>.denied.json   a guard stopped it
#
# The denied records matter more than the closed ones. A guard that
# denies raises before close(), so before gate.py wrote denial records
# there was no log of it at all -- and a guard doing its job reported
# as NEVER FIRED. Pruning guards on that signal would delete the
# effective ones first.
import json, glob, os, sys
from collections import Counter

def load(d):
    for p in sorted(glob.glob(os.path.join(d, "gate_*.json"))):
        with open(p) as fh:
            yield p, json.load(fh)

def mine(d, guards_path="guards.json"):
    with open(guards_path) as fh:
        all_ids = [g["id"] for g in json.load(fh)["guards"]]

    fires = Counter()          # guard -> times it produced a finding
    denies = Counter()         # guard -> times it stopped a run outright
    closed = denied = voids = 0
    uncaught, unassessed = [], []

    for path, r in load(d):
        if r.get("outcome") == "DENIED":
            denied += 1
            denies[r.get("denied_by", "?")] += 1
        else:
            closed += 1
        voids += len(r.get("voided_ratios", []))

        fired = set()
        for f in r.get("findings", []):
            fires[f["guard"]] += 1
            fired.add(f["guard"])

        # Divergence is the author's explicit call, recorded at close().
        # It is NOT inferred by comparing expected to observed: those are
        # prose, two descriptions of one outcome never compare equal, and
        # testing them for inequality flags every sound run in the corpus.
        if r.get("outcome") == "DENIED":
            continue
        div = r.get("diverged")
        if div is True and not fired:
            uncaught.append((r["sim_id"], r.get("expected"), r.get("observed")))
        elif div is None:
            unassessed.append(r["sim_id"])

    runs = closed + denied
    print("runs: %d   (closed %d, denied %d)   voided ratios: %d"
          % (runs, closed, denied, voids))

    print("\nguard activity")
    print("  %-8s %8s %8s %8s" % ("guard", "findings", "denials", "total"))
    for gid in all_ids:
        n, k = fires[gid], denies[gid]
        print("  %-8s %8d %8d %8d%s"
              % (gid, n, k, n + k, "   NEVER FIRED" if n + k == 0 else ""))
    if denied == 0:
        print("\n  no denial records in this corpus. if any run was stopped by")
        print("  a guard, its log is missing and the counts above understate.")

    print("\ndivergences with no guard attached  (the growth edge)")
    if not uncaught:
        print("  none")
    for sim, exp, obs in uncaught:
        print("  %s\n    expected: %s\n    observed: %s" % (sim, exp, obs))

    if unassessed:
        print("\nclosed without a divergence call  (nobody has looked)")
        for sim in unassessed:
            print("  %s" % sim)

    return {"runs": runs, "closed": closed, "denied": denied,
            "fires": dict(fires), "denies": dict(denies),
            "uncaught": uncaught, "unassessed": unassessed}

if __name__ == "__main__":
    mine(sys.argv[1] if len(sys.argv) > 1 else ".",
         sys.argv[2] if len(sys.argv) > 2 else "guards.json")
