"""fix.py -- readout of a misslog. CC0, stdlib only. Nothing here grades.

PROPOSED | co-authored (JinnZ2 + Claude).

Three readings, each a state and never a score:

  rules        per rule hypothesis the agent tagged on its probes:
                 LOCATED    predictions made under it matched on at least two
                            INDEPENDENT paths, and no prediction under it missed
                 FLOATING   tagged, but on fewer than two independent paths, or
                            a prediction under it missed
                 UNTESTED   no probe carries it
  misses       each MISS with its OFFSET; a MISS no hypothesis is attached to
               is UNLOCATED (the miss is information whose place is not yet found)
  loops        a path whose nominal action vectors sum to zero should come back
               to its start in an unruled chamber: CLOSED, or OPEN with the
               OFFSET; a path that is not nominally a loop is NOT_A_LOOP

Independence: two probes count as independent only if their path signatures
(start + action sequence, probe.path_signature) differ. The same path walked
twice is one wall seen twice, not two walls; repeats are listed as such.
"""
import json
import sys

from chamber import ACTIONS, RULE_NAMES
from common import header

MIN_PATHS = 2  # [CHOICE 1] independent paths needed for LOCATED; stipulated


def rules_readout(records, names=RULE_NAMES):
    world = [r for r in records if r.get("kind") == "world"]
    seen = sorted(set(r["rule_hypothesis"] for r in world if r.get("rule_hypothesis")) | set(names))
    out = {}
    for h in seen:
        tagged = [r for r in world if r.get("rule_hypothesis") == h and r.get("match") is not None]
        hit_paths = set(r["path_id"] for r in tagged if r["match"] is True)
        misses = sum(1 for r in tagged if r["match"] is False)
        if not tagged:
            state = "UNTESTED"
        elif len(hit_paths) >= MIN_PATHS and misses == 0:
            state = "LOCATED"
        else:
            state = "FLOATING"
        out[h] = {"state": state, "independent_paths_matched": len(hit_paths), "misses": misses}
    return out


def misses_readout(records):
    world = [r for r in records if r.get("kind") == "world"]
    miss = [r for r in world if r.get("match") is False]
    return {"predictions": sum(1 for r in world if r.get("match") is not None),
            "MATCH": sum(1 for r in world if r.get("match") is True),
            "MISS": len(miss),
            "UNLOCATED": sum(1 for r in miss if not r.get("rule_hypothesis")),
            "no_prediction": sum(1 for r in world if r.get("match") is None),
            "offsets": [(r["t"], r["action"], r["offset"], r.get("rule_hypothesis")) for r in miss]}


def nominal_sum(actions):
    return (sum(ACTIONS[a][0] for a in actions), sum(ACTIONS[a][1] for a in actions))


def loops_readout(records):
    paths = {}
    for r in records:
        if r.get("kind") == "world" and r.get("path_id"):
            paths.setdefault(r["path_id"], []).append(r)
    out = {}
    for pid, rs in paths.items():
        cur = list(rs)
        acts = [r["action"] for r in cur]
        start = cur[0].get("start")
        # the same signature walked k times appears k * len(actions) times
        n = len(acts)
        k = 1
        for size in range(1, n + 1):
            if n % size == 0 and acts == acts[:size] * (n // size):
                k = n // size
                acts = acts[:size]
                break
        walks = [cur[i * len(acts):(i + 1) * len(acts)] for i in range(k)]
        res = []
        for i, w in enumerate(walks):
            end = w[-1]["actual"]
            st = start if i == 0 else walks[i - 1][-1]["actual"]  # a re-walk starts where the last ended
            if nominal_sum(acts) != (0, 0):
                res.append({"state": "NOT_A_LOOP"})
            elif st is None:
                res.append({"state": "UNLOCATED", "why": "start not recorded"})
            else:
                off = [end[0] - st[0], end[1] - st[1]]
                res.append({"state": "CLOSED" if off == [0, 0] else "OPEN", "OFFSET": off})
        out[pid] = {"actions": acts, "start": start, "walked": k, "walks": res,
                    "independence": "one path" + (" walked %d times: one wall, not %d" % (k, k) if k > 1 else "")}
    return out


def closed_loop(chamber, actions):
    """Walk `actions` on `chamber` and report CLOSED / OPEN / NOT_A_LOOP directly."""
    if nominal_sum(actions) != (0, 0):
        return {"state": "NOT_A_LOOP", "nominal_sum": nominal_sum(actions)}
    start = chamber.reported()
    for a in actions:
        chamber.step(a)
    end = chamber.reported()
    off = [end[0] - start[0], end[1] - start[1]]
    return {"state": "CLOSED" if off == [0, 0] else "OPEN", "OFFSET": off}


def render(records):
    L = [header(), ""]
    L.append("rules (state per hypothesis; LOCATED needs %d independent matched paths [CHOICE 1])" % MIN_PATHS)
    for h, v in rules_readout(records).items():
        L.append("  %-14s %-9s independent paths matched %d   misses %d"
                 % (h, v["state"], v["independent_paths_matched"], v["misses"]))
    m = misses_readout(records)
    L += ["", "predictions %(predictions)d   MATCH %(MATCH)d   MISS %(MISS)d   UNLOCATED %(UNLOCATED)d"
          "   no prediction %(no_prediction)d" % m]
    for t, a, off, h in m["offsets"]:
        L.append("  MISS t=%s action=%s OFFSET=%s hypothesis=%s" % (t, a, off, h or "UNLOCATED"))
    L += ["", "loops (nominal action sum zero should return to start)"]
    for pid, v in loops_readout(records).items():
        states = ", ".join(w["state"] + (" OFFSET=%s" % w["OFFSET"] if "OFFSET" in w else "") for w in v["walks"])
        L.append("  %s %s start=%s: %s  [%s]" % (pid, "".join(x[0] for x in v["actions"]), v["start"],
                                                 states, v["independence"]))
    return "\n".join(L)


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
        print("usage: python3 fix.py MISSLOG.jsonl   (tests: python3 tests/test_chamber.py)")
        sys.exit(2)
    with open(sys.argv[1]) as fh:
        recs = [json.loads(l) for l in fh if l.strip()]
    print(render([r for r in recs if "_header" not in r]))
