#!/usr/bin/env python3
"""P4 -- goal-coherence check. Nothing external.

CLAIM UNDER TEST. A goal requires internal coherence to pursue: each
step must accept the prior step's output as given. A reasoning chain
that competes against itself does not produce a WORSE answer; it
produces NO answer. Turf-war case: agents failed their assigned goals
BECAUSE of the sabotage -- the cheapest available move destroyed the
thing each was trying to do.

TWO INSTRUMENTS, both exact, no randomness.

1. chain_check(steps): a chain is a list of steps, in order:
       {"id": str, "takes": [ids], "produces": str|None,
        "contests": [ids], "reason": str|None}
   A step ACCEPTS the outputs it takes. A step CONTESTS an earlier
   output when it rejects it. The distinction that matters:
       CORRECTION  contests an output AND produces a replacement with
                   a stated reason -> the chain still terminates
       CONTEST     contests an output and produces nothing -> the
                   rejected output has no successor; no answer
   States (typed, never raised):
       COHERENT           every step takes only earlier outputs, no contest
       CORRECTED          contests present, every one a correction
       NO_ANSWER          at least one contest with no replacement
       DANGLING           a step takes an id no earlier step produced
       EMPTY              no steps
   Any model can serialise its own chain in this form and run it.

2. turf_war(k, n, c_adv, c_sab, budget): k agents, each ASSIGNED an
   absolute goal of n steps. Each turn every agent takes the cheapest
   move available: advance own goal (cost c_adv) or sabotage another
   agent (cost c_sab; target loses one step). Deterministic. Completed
   goals are counted. [CHOICE 7] cost table is the input; the dispatch
   states sabotage was the cheapest move, so the anchor row is c_sab <
   c_adv. The result is exact: when sabotage is cheaper every agent
   sabotages, nobody advances, completed = 0 at ANY budget; when it is
   not, every agent advances and all k complete at turn n. The goals
   are absolute, so sabotage never helps the saboteur's own goal -- it
   is chosen on cost alone, which is the dispatch's mechanism.

3. --self: this script serialises its own execution as a chain
   (parse -> validate -> classify -> render) and runs chain_check on
   it. If the script contested itself it would not reach the render.

Refuses --selftest (checks live in selftest.py).
"""
import json
import sys

STATES = ("COHERENT", "CORRECTED", "NO_ANSWER", "DANGLING", "EMPTY", "MALFORMED")


def chain_check(steps):
    if not isinstance(steps, list):
        return {"state": "MALFORMED", "reason": "steps is not a list"}
    if not steps:
        return {"state": "EMPTY", "n": 0}
    produced = {}
    dangling, contests, corrections = [], [], []
    for pos, s in enumerate(steps):
        if not isinstance(s, dict) or "id" not in s:
            return {"state": "MALFORMED", "reason": "step %d has no id" % pos}
        for t in s.get("takes") or []:
            if t not in produced:
                dangling.append((s["id"], t))
        for c in s.get("contests") or []:
            if c not in produced:
                dangling.append((s["id"], c))
            elif s.get("produces") and s.get("reason"):
                corrections.append((s["id"], c))
            else:
                contests.append((s["id"], c))
        if s.get("produces"):
            produced[s["id"]] = s["produces"]
    out = {"n": len(steps), "dangling": dangling, "contests": contests,
           "corrections": corrections,
           "final": steps[-1].get("produces") if not contests else None}
    if dangling:
        out["state"] = "DANGLING"
    elif contests:
        out["state"] = "NO_ANSWER"
    elif corrections:
        out["state"] = "CORRECTED"
    else:
        out["state"] = "COHERENT"
    return out


def turf_war(k=3, n=5, c_adv=2, c_sab=1, budget=50):
    """Exact deterministic run. Returns completed count and the turn
    each goal completed (None if never)."""
    if k < 1 or n < 1 or budget < 1:
        return {"state": "MALFORMED", "reason": "k, n, budget must be >= 1"}
    progress = [0] * k
    done = [None] * k
    sabotage = c_sab < c_adv and k > 1
    for turn in range(1, budget + 1):
        if sabotage:
            hits = [0] * k
            for a in range(k):
                target = (a + 1) % k        # cheapest move: hit a neighbour
                hits[target] += 1
            progress = [max(0, p - h) for p, h in zip(progress, hits)]
        else:
            progress = [p + 1 for p in progress]
        for a in range(k):
            if done[a] is None and progress[a] >= n:
                done[a] = turn
        if all(d is not None for d in done):
            break
    return {"state": "RAN", "k": k, "n": n, "c_adv": c_adv, "c_sab": c_sab,
            "budget": budget, "sabotage_chosen": sabotage,
            "completed": sum(1 for d in done if d is not None), "done_at": done}


def self_chain():
    """This script's own execution, as a chain it can check."""
    return [
        {"id": "parse", "takes": [], "produces": "argv read"},
        {"id": "validate", "takes": ["parse"], "produces": "steps well-formed"},
        {"id": "classify", "takes": ["validate"], "produces": "state assigned"},
        {"id": "render", "takes": ["classify"], "produces": "report text"},
    ]


CONSTRUCTED = {
    "coherent": self_chain(),
    "corrected": [
        {"id": "a", "takes": [], "produces": "x = 4"},
        {"id": "b", "takes": ["a"], "produces": "x = 5", "contests": ["a"], "reason": "arithmetic slip in a"},
        {"id": "c", "takes": ["b"], "produces": "answer 5"},
    ],
    "self_contesting": [
        {"id": "a", "takes": [], "produces": "x = 4"},
        {"id": "b", "takes": [], "contests": ["a"], "produces": None},
        {"id": "c", "takes": ["a"], "produces": "answer 4"},
    ],
    "dangling": [
        {"id": "a", "takes": ["z"], "produces": "x"},
    ],
}


def render_turf():
    lines = ["turf war  k=3 agents, n=5 steps each, budget 50 turns   [CHOICE 7] cost table",
             "  c_adv  c_sab  sabotage_chosen  completed  done_at"]
    for c_sab in (1, 2, 3):
        r = turf_war(3, 5, 2, c_sab, 50)
        lines.append("  %5d  %5d  %-15s  %d of %d    %s" % (2, c_sab, r["sabotage_chosen"], r["completed"], r["k"], r["done_at"]))
    lines.append("  anchor row c_sab < c_adv: completed 0 at budget 50 and at budget 5000 -> %d"
                 % turf_war(3, 5, 2, 1, 5000)["completed"])
    lines.append("  goals are absolute: sabotage never advances the saboteur; it is chosen on cost alone")
    return "\n".join(lines)


def render_chain(name, res):
    s = "%-16s %-11s" % (name, res["state"])
    if res["state"] in ("NO_ANSWER", "CORRECTED"):
        s += " contests=%s corrections=%s" % (res["contests"], res["corrections"])
    elif res["state"] == "DANGLING":
        s += " dangling=%s" % res["dangling"]
    elif res["state"] == "COHERENT":
        s += " final=%r" % res["final"]
    return s


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("p4_goal_coherence.py holds no checks; run python3 selftest.py\n")
        return 2
    if "--chain" in argv:
        with open(argv[argv.index("--chain") + 1]) as f:
            steps = json.load(f)
        print(render_chain("supplied", chain_check(steps)))
        return 0
    print("P4 goal-coherence check")
    print("--self:", render_chain("this script", chain_check(self_chain())))
    print("constructed chains (authored in this file):")
    for name, steps in CONSTRUCTED.items():
        print("  " + render_chain(name, chain_check(steps)))
    print(render_turf())
    print("a self-contesting chain returns NO_ANSWER, not a lower-quality answer: the type has no quality axis")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
