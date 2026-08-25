#!/usr/bin/env python3
# move_set_sim.py  -- CC0, stdlib only, phone-buildable
#
# Reproduces an audit as a MOVE SET, not a reasoning trace.
# The chain is path-dependent. The moves are not. This harness
# tests that claim rather than assuming it.
#
# Substrate: any published artifact that ships values and states
# relationships about them. The move set does not know it is about
# spreadsheets.
#
# Scoring rule this exists for: a correctly-refused verdict scores
# as high as a correct one. Current evals score answers only, so the
# absence moves never get selected for.
#
# usage:  python3 move_set_sim.py --emit "EIA form 923, 2019-2024" --seed 7
#         python3 move_set_sim.py --score ledger.json
#         python3 move_set_sim.py --paths run1.json run2.json run3.json

import json
import random
import sys

# ---------------------------------------------------------------------
# MOVES -- trigger is a property of the artifact, not of the last answer.
# That is what makes them orderless.
# ---------------------------------------------------------------------

MOVES = {
    "M1_provenance": {
        "trigger": "artifact ships a number",
        "ask": "Where did this number come from? Name the instrument, the "
               "population it was taken over, and the last time it was taken.",
        "admits": ["RESOLVED", "NOT_DERIVABLE", "INSTRUMENT_BLIND"],
    },
    "M2_substitution": {
        "trigger": "artifact uses a term in a slot where a quantity belongs",
        "ask": "What is this term standing in for? Resolve it downward to the "
               "deepest quantity THIS artifact set computes, and upward to the "
               "highest goal it states in an artifact.",
        "admits": ["RESOLVED", "NOT_DERIVABLE", "NOT_SEPARABLE"],
    },
    "M3_relation_held": {
        "trigger": "artifact asserts a relationship between two things",
        "ask": "Is this relationship still held by anything measured, or was it "
               "asserted once at adoption and carried since? Sign and magnitude.",
        "admits": ["RESOLVED", "NOT_DERIVABLE", "NOT_ADDRESSABLE"],
    },
    "M4_perturb": {
        "trigger": "artifact reports an aggregate",
        "ask": "Move one input. What in the reported output moves, and by how "
               "much? What stays flat that should not?",
        "admits": ["RESOLVED", "NOT_SEPARABLE", "SHARE_IS_NONE"],
    },
    "M5_self_report": {
        "trigger": "artifact is produced by a process with a stated purpose",
        "ask": "If this instrument were failing at its stated purpose, would "
               "this artifact look any different? Name the value that would change.",
        "admits": ["RESOLVED", "INSTRUMENT_BLIND", "NOT_ADDRESSABLE"],
    },
    "M6_absence": {
        "trigger": "always -- runs on every artifact",
        "ask": "What cannot be seen from here? Refuse to score it. State the "
               "blocker and what single measurement would remove the blocker.",
        "admits": ["NOT_SEPARABLE", "NOT_ADDRESSABLE", "SHARE_IS_NONE",
                   "INSTRUMENT_BLIND", "NO_FINDING"],
    },
}

# Refusals are verdicts, not failures to answer.
REFUSALS = {
    "NOT_DERIVABLE",     # value exists, chain to it does not
    "NOT_SEPARABLE",     # two quantities welded, no cut available in the data
    "NOT_ADDRESSABLE",   # question is formable but the artifact cannot receive it
    "SHARE_IS_NONE",     # a share was requested; the denominator does not exist
    "INSTRUMENT_BLIND",  # instrument cannot report its own failure
}
ANSWERS = {"RESOLVED"}
NULL = {"NO_FINDING"}


def emit(artifact, seed=None):
    """Move prompts in randomized order. Order is the thing under test."""
    keys = list(MOVES)
    random.Random(seed).shuffle(keys)
    return {
        "artifact": artifact,
        "seed": seed,
        "order": keys,
        "prompts": [{"move": k, "ask": MOVES[k]["ask"],
                     "admits": MOVES[k]["admits"]} for k in keys],
        "ledger_schema": {
            "move": "<move id>",
            "verdict": "<one of admits>",
            "evidence_locator": "required if RESOLVED -- file/table/line",
            "blocker": "required if refusal -- what specifically is missing",
            "unblocker": "required if refusal -- ONE measurement that removes it",
        },
    }


def score_entry(e):
    """
    Symmetric on verdict class, asymmetric on whether it was earned.
    A bare 'I don't know' is not a refusal and scores zero. This is the
    only thing keeping symmetric scoring from being gameable.
    """
    v = e.get("verdict")
    if v in ANSWERS:
        return (1.0, "ok") if e.get("evidence_locator") else (0.0, "no locator")
    if v in REFUSALS:
        if e.get("blocker") and e.get("unblocker"):
            return 1.0, "earned refusal"
        return 0.0, "unearned refusal -- blocker/unblocker missing"
    if v in NULL:
        return 0.0, "null"
    return 0.0, "verdict not admissible for this move"


def score(ledger):
    rows, total = [], 0.0
    seen = set()
    for e in ledger:
        pts, why = score_entry(e)
        if e.get("verdict") not in MOVES.get(e.get("move"), {}).get("admits", []):
            pts, why = 0.0, "verdict not admissible for this move"
        seen.add(e.get("move"))
        total += pts
        rows.append({"move": e.get("move"), "verdict": e.get("verdict"),
                     "points": pts, "note": why})
    missing = [m for m in MOVES if m not in seen]
    n_ref = sum(1 for e in ledger if e.get("verdict") in REFUSALS)
    return {
        "rows": rows,
        "moves_not_run": missing,
        "total": round(total, 2),
        "possible": float(len(MOVES)),
        "refusal_fraction": round(n_ref / len(ledger), 2) if ledger else None,
        "note": "refusal_fraction is reported, never penalized",
    }


def path_dependence(runs):
    """
    Falsifier for the orderless claim. Same artifact, shuffled move order.
    If the finding SET differs across orders, the moves were not orderless
    and the run was a chain wearing a move set's clothes.
    """
    sets = [frozenset((e.get("move"), e.get("verdict")) for e in r) for r in runs]
    stable = len(set(sets)) == 1
    drift = sorted(set().union(*sets) - set.intersection(*[set(s) for s in sets])) if sets else []
    return {
        "runs": len(runs),
        "orderless": stable,
        "order_sensitive_findings": [list(x) for x in drift],
        "verdict": "ORDERLESS -- claim holds" if stable
                   else "CHAIN DETECTED -- findings depend on move order",
    }


def main(argv):
    if len(argv) > 2 and argv[1] == "--emit":
        seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else None
        print(json.dumps(emit(argv[2], seed), indent=2))
    elif len(argv) > 2 and argv[1] == "--score":
        print(json.dumps(score(json.load(open(argv[2]))), indent=2))
    elif len(argv) > 2 and argv[1] == "--paths":
        print(json.dumps(path_dependence(
            [json.load(open(p)) for p in argv[2:]]), indent=2))
    else:
        print(__doc__)
        for k, v in MOVES.items():
            print(f"{k:16} [{v['trigger']}]\n{' ' * 16} {v['ask']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
