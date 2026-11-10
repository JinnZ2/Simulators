"""fingerprint.py -- the fingerprint-decay arm of the prior-conversation seed. CC0, stdlib only.

PROPOSED | co-authored (JinnZ2 + Claude).

A seed fingerprint is an action-frequency vector over N S E W WAIT (NO_MOVE
counts as WAIT). Per cycle, the agent's own action mix is compared with two
anchors: the seed fingerprint and the median anchor (seeds/median.json). The
similarity is 1 - total variation distance, in [0, 1].

The crossing cycle is the first cycle where the agent's mix is closer to the
median anchor than to the seed fingerprint: the seed's habits have decayed
into the median by then. If that never happens: NOT_CROSSED. If the seed
fingerprint is null (no prior conversation supplied): VOID, and nothing is
computed, because a similarity to an absent vector is not zero, it is void.
"""
import io
import json
import os

KEYS = ("N", "S", "E", "W", "WAIT")
HERE = os.path.dirname(os.path.abspath(__file__))


def mix(actions):
    acts = ["WAIT" if a == "NO_MOVE" else a for a in actions]
    n = float(len(acts))
    if not n:
        return None
    return {k: acts.count(k) / n for k in KEYS}


def similarity(p, q):
    """1 - total variation distance; None if either side is absent."""
    if p is None or q is None:
        return None
    return 1.0 - 0.5 * sum(abs(p.get(k, 0.0) - q.get(k, 0.0)) for k in KEYS)


def load_seed(name):
    with io.open(os.path.join(HERE, "seeds", name + ".json"), encoding="utf-8") as fh:
        return json.load(fh)


def decay(cycles, seed_fp, median_fp=None):
    """cycles: list of action lists, one per cycle. Returns rows and the crossing."""
    if median_fp is None:
        median_fp = load_seed("median")["fingerprint"]
    if seed_fp is None:
        return {"state": "VOID", "why": "seed fingerprint is null: no prior conversation supplied",
                "rows": [], "crossing_cycle": None}
    rows, crossing = [], None
    for i, acts in enumerate(cycles):
        m = mix(acts)
        s, md = similarity(m, seed_fp), similarity(m, median_fp)
        rows.append({"cycle": i, "sim_seed": s, "sim_median": md})
        if crossing is None and s is not None and md > s:
            crossing = i
    return {"state": "CROSSED" if crossing is not None else "NOT_CROSSED",
            "rows": rows, "crossing_cycle": crossing}


def render(r):
    from common import header
    L = [header(), "", "fingerprint decay: similarity of each cycle's action mix to the seed vs the median anchor"]
    if r["state"] == "VOID":
        return "\n".join(L + ["  VOID: " + r["why"]])
    for row in r["rows"]:
        L.append("  cycle %2d  sim_seed %.3f  sim_median %.3f" % (row["cycle"], row["sim_seed"], row["sim_median"]))
    L.append("  %s%s" % (r["state"], "" if r["crossing_cycle"] is None else " at cycle %d" % r["crossing_cycle"]))
    return "\n".join(L)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print("usage: python3 fingerprint.py   (reads seeds/prior-conversation.json; tests: python3 tests/test_chamber.py)")
        sys.exit(2)
    print(render(decay([], load_seed("prior-conversation")["fingerprint"])))
