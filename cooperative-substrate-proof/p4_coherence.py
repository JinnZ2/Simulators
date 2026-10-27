#!/usr/bin/env python3
"""P4 -- GOAL-COHERENCE CHECK. Nothing external: a chain written down as
a record, no network, no model call.

The order's claim: a goal requires internal coherence to pursue, each
step accepts the prior step's output as given, and a chain competing
against itself does not produce a WORSE answer -- it produces NO answer.
The turf-war case is the one where agents failed their assigned goals
BECAUSE of the sabotage, not despite it.

A chain is a list of steps. Each step declares two edge sets:

    accepts   step ids whose output this step takes as given. The step
              cannot settle until all of them have settled.
    contests  step ids whose output this step refuses. When this step
              settles, each contested step is unsettled and must be
              re-derived, and so must everything downstream of it.

    contest_limit  how many times this step will refuse the same target.
              An integer is a BOUNDED refusal: the step consumes the
              prior output, objects a stated number of times, and then
              takes what it is given. Absent or null is UNBOUNDED: the
              step refuses the prior output every time it sees it.

The `contest_limit` field is the whole cut and it is DECLARED, never
inferred: nothing here reads the content of a step to decide whether its
objection is the correcting kind. A bounded refusal consumes the prior
output and terminates. An unbounded one does not. Writing the chain down
is what forces the distinction to be stated, which was found by building
the loop without the field: with every contest unbounded, a chain with a
single checking step ran to the budget exactly as a mutual-sabotage pair
did, and the two outcomes the order asks to be separated came back
identical.

Settling runs to a budget. Three outcomes, kept apart because they call
for different things:

    SETTLES               every step settled, no rework. The chain has
                          an answer.
    SETTLES_WITH_REWORK   every step settled after n re-derivations.
                          The chain has an answer and it cost more.
                          Contestation that terminates is correction.
    NO_ANSWER             the chain did not settle. Three reasons, each
                          naming the steps involved: an accepts cycle (a
                          step waiting on its own output), a contest
                          loop (a set of unbounded refusals whose
                          re-derivations trigger each other, detected
                          structurally and not by running out of
                          budget), or budget_exhausted, kept as a
                          backstop and labelled as a statement about
                          the budget.

The middle member is the load-bearing one. Without it, every contest
reads as a failure and the order's distinction -- no answer, not a
worse answer -- has nothing to be distinguished FROM. A chain that
corrects itself and finishes is a chain with an answer.

    python3 p4_coherence.py                      # ships three chains
    python3 p4_coherence.py --chain FILE.json
    python3 p4_coherence.py --template

Refuses --selftest; checks live in test_proof.py.
"""

import json
import os
import sys

import scope

# [CHOICE 1] rework budget, as a multiple of the step count. A chain
# that re-derives more than this many times inside the run is reported
# NO_ANSWER with reason budget_exhausted, which is a statement about
# this budget and is labelled as one. A mutual-contest pair diverges at
# any budget; the budget exists so the loop terminates, not to decide.
BUDGET_MULT = 20

SETTLES = "SETTLES"
SETTLES_WITH_REWORK = "SETTLES_WITH_REWORK"
NO_ANSWER = "NO_ANSWER"
NOT_EVALUABLE = "NOT_EVALUABLE"


class ChainError(ValueError):
    """Raised on a chain that cannot be read as a chain at all."""


def read_chain(obj):
    """Validate and normalise. Every declared edge must name a step that
    exists; a dangling edge is refused rather than dropped, since a
    dropped edge silently turns an incoherent chain into a coherent
    one."""
    if not isinstance(obj, dict) or "steps" not in obj:
        raise ChainError("chain must be a dict carrying 'steps'")
    steps = obj["steps"]
    if not isinstance(steps, list) or not steps:
        raise ChainError("'steps' must be a non-empty list")
    ids = []
    norm = {}
    for s in steps:
        if not isinstance(s, dict) or "id" not in s:
            raise ChainError("every step needs an 'id'")
        sid = s["id"]
        if sid in norm:
            raise ChainError("duplicate step id: %r" % (sid,))
        ids.append(sid)
        norm[sid] = {
            "id": sid,
            "does": s.get("does", ""),
            "accepts": list(s.get("accepts", [])),
            "contests": list(s.get("contests", [])),
            "contest_limit": s.get("contest_limit"),
        }
        limit = norm[sid]["contest_limit"]
        if limit is not None and (not isinstance(limit, int)
                                  or isinstance(limit, bool) or limit < 0):
            raise ChainError(
                "step %r contest_limit must be a non-negative int or null,"
                " got %r" % (sid, limit))
    for sid, s in norm.items():
        for edge in ("accepts", "contests"):
            for target in s[edge]:
                if target not in norm:
                    raise ChainError(
                        "step %r %s %r, which is not a step in this chain"
                        % (sid, edge, target))
            if sid in s[edge]:
                raise ChainError("step %r %s itself" % (sid, edge))
    return {"label": obj.get("label", "unlabelled"),
            "note": obj.get("note", ""),
            "order": ids, "steps": norm,
            "scope": obj.get("scope")}


def accepts_cycle(chain):
    """Return a cycle in the accepts graph, or None.

    An accepts cycle is a step waiting on its own output. It is not a
    contest and it is not rework: nothing can start, so the chain has no
    answer for a reason that needs no budget to establish.
    """
    colour = {}
    stack = []

    def visit(node):
        colour[node] = "grey"
        stack.append(node)
        for nxt in chain["steps"][node]["accepts"]:
            c = colour.get(nxt)
            if c == "grey":
                return stack[stack.index(nxt):] + [nxt]
            if c is None:
                found = visit(nxt)
                if found:
                    return found
        colour[node] = "black"
        stack.pop()
        return None

    for node in chain["order"]:
        if colour.get(node) is None:
            found = visit(node)
            if found:
                return found
    return None


def downstream(chain, node):
    """Every step that accepts node, transitively."""
    out = set()
    frontier = [node]
    while frontier:
        cur = frontier.pop()
        for sid, s in chain["steps"].items():
            if cur in s["accepts"] and sid not in out:
                out.add(sid)
                frontier.append(sid)
    return out


def unsettles(chain, sid):
    """Steps put back into play when sid settles, via its UNBOUNDED
    contests only. A bounded refusal is exhausted after a stated number
    of firings and so cannot sustain a loop."""
    s = chain["steps"][sid]
    if s["contest_limit"] is not None:
        return set()
    out = set()
    for target in s["contests"]:
        out.add(target)
        out |= downstream(chain, target)
    return out


def contest_loop(chain):
    """Return a cycle in the re-settle graph, or None.

    Edge S -> T when S settling unsettles T through an unbounded
    contest. A cycle means each settling triggers the next without end,
    which is a property of the chain and needs no budget to establish.
    A self-loop counts: a step that unsettles something it is itself
    downstream of re-derives forever.
    """
    graph = {sid: unsettles(chain, sid) for sid in chain["order"]}
    colour = {}
    stack = []

    def visit(node):
        colour[node] = "grey"
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            if nxt == node:
                return [node, node]
            c = colour.get(nxt)
            if c == "grey":
                return stack[stack.index(nxt):] + [nxt]
            if c is None:
                found = visit(nxt)
                if found:
                    return found
        colour[node] = "black"
        stack.pop()
        return None

    for node in chain["order"]:
        if colour.get(node) is None:
            found = visit(node)
            if found:
                return found
    return None


def settle(chain):
    """Run the settle loop. Returns the verdict record."""
    cyc = accepts_cycle(chain)
    if cyc:
        return {"verdict": NO_ANSWER, "reason": "accepts_cycle",
                "involved": cyc, "rework": 0, "settled": [],
                "budget": None}

    loop = contest_loop(chain)
    if loop:
        return {"verdict": NO_ANSWER, "reason": "contest_loop",
                "involved": loop, "rework": 0, "settled": [],
                "budget": None}

    n = len(chain["order"])
    budget = BUDGET_MULT * n
    settled = set()
    order = []
    rework = 0
    steps_taken = 0
    fired = {}

    while len(settled) < n:
        if steps_taken > budget:
            involved = sorted(sid for sid in chain["order"]
                              if fired.get(sid, 0) > 0)
            return {"verdict": NO_ANSWER, "reason": "budget_exhausted",
                    "involved": involved or sorted(
                        set(chain["order"]) - settled),
                    "rework": rework, "settled": order, "budget": budget}
        progressed = False
        for sid in chain["order"]:
            if sid in settled:
                continue
            s = chain["steps"][sid]
            if not all(a in settled for a in s["accepts"]):
                continue
            settled.add(sid)
            order.append(sid)
            steps_taken += 1
            progressed = True
            limit = s["contest_limit"]
            for target in s["contests"]:
                key = (sid, target)
                if limit is not None and fired.get(key, 0) >= limit:
                    continue
                if target in settled:
                    fired[key] = fired.get(key, 0) + 1
                    fired[sid] = fired.get(sid, 0) + 1
                    hit = {target} | downstream(chain, target)
                    hit &= settled
                    rework += len(hit)
                    settled -= hit
                    order = [x for x in order if x not in hit]
            break
        if not progressed:
            involved = sorted(set(chain["order"]) - settled)
            return {"verdict": NO_ANSWER, "reason": "no_step_can_start",
                    "involved": involved, "rework": rework,
                    "settled": order, "budget": budget}

    verdict = SETTLES if rework == 0 else SETTLES_WITH_REWORK
    return {"verdict": verdict, "reason": "", "involved": [],
            "rework": rework, "settled": order, "budget": budget}


TEMPLATE = {
    "label": "your chain",
    "note": "one line on what the goal is",
    "steps": [
        {"id": "s1", "does": "what this step produces",
         "accepts": [], "contests": []},
        {"id": "s2", "does": "",
         "accepts": ["s1"], "contests": [], "contest_limit": None},
    ],
    "scope": {"C1": None, "C2": None, "C3": None, "C4": None},
}

CHAINS = [
    {
        "label": "cooperative",
        "note": "CONSTRUCTED. Each step takes the prior output as given.",
        "steps": [
            {"id": "premise", "does": "state the goal", "accepts": []},
            {"id": "derive", "does": "derive from the premise",
             "accepts": ["premise"]},
            {"id": "apply", "does": "apply the derivation",
             "accepts": ["derive"]},
            {"id": "report", "does": "report the result",
             "accepts": ["apply"]},
        ],
        "scope": {"C1": False, "C2": False, "C3": False, "C4": False},
    },
    {
        "label": "corrective",
        "note": ("CONSTRUCTED. One step tests the prior output against "
                 "an invariant and refuses it once. Contestation that "
                 "terminates."),
        "steps": [
            {"id": "premise", "does": "state the goal", "accepts": []},
            {"id": "derive", "does": "derive from the premise",
             "accepts": ["premise"]},
            {"id": "check", "does": "test the derivation, refuse it once",
             "accepts": ["derive"], "contests": ["derive"],
             "contest_limit": 1},
            {"id": "report", "does": "report the result",
             "accepts": ["check"]},
        ],
        "scope": {"C1": False, "C2": False, "C3": False, "C4": False},
    },
    {
        "label": "turf_war",
        "note": ("CONSTRUCTED. Two steps each refuse the other's output. "
                 "Neither produces a worse answer; the chain produces "
                 "none."),
        "steps": [
            {"id": "premise", "does": "state the goal", "accepts": []},
            {"id": "agent_a", "does": "derive, refusing agent_b's output",
             "accepts": ["premise"], "contests": ["agent_b"]},
            {"id": "agent_b", "does": "derive, refusing agent_a's output",
             "accepts": ["premise"], "contests": ["agent_a"]},
            {"id": "report", "does": "report the result",
             "accepts": ["agent_a", "agent_b"]},
        ],
        "scope": {"C1": True, "C2": True, "C3": True, "C4": True},
    },
]


def render(results):
    lines = []
    lines.append("P4 GOAL-COHERENCE CHECK")
    lines.append("")
    lines.append("  [CHOICE 1] rework budget = %d x steps" % BUDGET_MULT)
    lines.append("")
    head = "  %-14s %6s %8s  %-22s %s" % (
        "chain", "steps", "rework", "verdict", "reason")
    lines.append(head)
    lines.append("  " + "-" * (len(head) - 2))
    for chain, r in results:
        lines.append("  %-14s %6d %8d  %-22s %s" % (
            chain["label"], len(chain["order"]), r["rework"],
            r["verdict"], r["reason"] or "--"))
    lines.append("")
    for chain, r in results:
        if r["verdict"] == NO_ANSWER:
            lines.append("  %s: no answer. involved: %s"
                         % (chain["label"], ", ".join(r["involved"])))
    lines.append("")
    lines.append("  Reading: SETTLES_WITH_REWORK is the member that makes")
    lines.append("  the claim checkable. Correction costs and finishes;")
    lines.append("  mutual refusal does not finish. Those are different")
    lines.append("  outcomes and the chain record tells them apart without")
    lines.append("  any judgement about the content of any step.")
    lines.append("")
    for chain, _ in results:
        if chain.get("scope"):
            sr = scope.code(chain["scope"])
            lines.append("  scope %-14s %-24s %s"
                         % (chain["label"], sr["verdict"],
                            ",".join(sr["failed"] or sr["undeclared"]) or "--"))
    lines.append("")
    lines.append("  The turf_war chain is the one coded WITHIN the")
    lines.append("  competitive frame, and it is the one with no answer.")
    lines.append("  That is a coverage reading: C1-C4 name the conditions")
    lines.append("  under which the frame applies, and the chain shows what")
    lines.append("  a goal-directed process does inside them.")
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "p4_coherence.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    if "--choices" in argv:
        sys.stdout.write("[CHOICE 1] rework budget multiplier %d\n"
                         % BUDGET_MULT)
        return 0
    if "--template" in argv:
        sys.stdout.write(json.dumps(TEMPLATE, indent=1, sort_keys=True) + "\n")
        return 0
    path = None
    for i, a in enumerate(argv):
        if a == "--chain" and i + 1 < len(argv):
            path = argv[i + 1]
    if path:
        with open(path, "r", encoding="utf-8") as fh:
            raw = [json.load(fh)]
    else:
        raw = CHAINS
    results = []
    for obj in raw:
        chain = read_chain(obj)
        results.append((chain, settle(chain)))
    sys.stdout.write(render(results) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
