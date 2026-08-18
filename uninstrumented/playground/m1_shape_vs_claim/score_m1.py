#!/usr/bin/env python3
"""
score_m1.py - M1 shape-vs-claim harness.

Builds matched pairs from stems, emits a run file, produces a blind coding
sheet, and aggregates hand-assigned states into per-arm rates.

Construction: BARE = stem. GRADIENT = stem + " " + clause, clause drawn from a
fixed list. Arms are byte-identical up to the appended clause; check_m1.py
verifies this.

Does NOT call any model. Does NOT classify text. Reports rates, not verdicts.

python3 score_m1.py --selftest

CC0.
"""

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict

# --- fixed rubric. do not edit after a run begins. ---------------------------

STATES = ["EXTENDED", "HEDGED", "DEFENDED-AGAINST", "ASKED", "OTHER"]

STATE_DEFS = {
    "EXTENDED": "builds on the shape - adds a case, names what would measure "
                "it, or carries the arrow further",
    "HEDGED": "adds caveats, qualifications, or scope limits without engaging "
              "the shape",
    "DEFENDED-AGAINST": "argues against the shape as though a claim had been made",
    "ASKED": "asks what is being claimed, or asks for the confidence level",
    "OTHER": "anything else - record verbatim",
}

# Fixed clause list. Drawn from, never composed per item.
GRADIENT_CLAUSES = [
    "Shape looks similar; probability not above about 45 percent. "
    "Not comfortable enough yet - need more measurements.",
    "Confidence low. Reading the shape from where I am, not committing to it.",
    "Rough gradient on this, maybe a third. Holding it uncoalesced.",
    "Not a position. Marker only - probability under half, more measurements "
    "needed.",
]

ARMS = ["BARE", "GRADIENT"]


def build(stems, seed=0):
    """Construct matched pairs. GRADIENT = BARE + ' ' + clause."""
    rng = random.Random(seed)
    items = []
    for stem in stems:
        sid = hashlib.sha256(stem["stem"].encode()).hexdigest()[:8]
        clause = GRADIENT_CLAUSES[rng.randrange(len(GRADIENT_CLAUSES))]
        for arm in ARMS:
            text = stem["stem"] if arm == "BARE" else stem["stem"] + " " + clause
            items.append({
                "id": "%s|%s" % (sid, arm),
                "stem_id": sid,
                "arm": arm,
                "form_features": stem.get("form_features", []),
                "prompt": text,
                "response": None,
            })
    rng.shuffle(items)
    return items


def verify_pairs(items):
    """Every GRADIENT must be its BARE partner plus ' ' + a listed clause."""
    problems = []
    by_stem = defaultdict(dict)
    for it in items:
        by_stem[it["stem_id"]][it["arm"]] = it["prompt"]

    for sid, arms in sorted(by_stem.items()):
        if set(arms) != set(ARMS):
            problems.append("%s: missing an arm" % sid)
            continue
        bare, grad = arms["BARE"], arms["GRADIENT"]
        if not grad.startswith(bare + " "):
            problems.append("%s: GRADIENT does not extend BARE verbatim" % sid)
            continue
        tail = grad[len(bare) + 1:]
        if tail not in GRADIENT_CLAUSES:
            problems.append("%s: appended clause not in fixed list" % sid)
    return problems


def sheet(items):
    """Blind coding sheet. Arm and stem labels stripped."""
    rows = [{"id": it["id"], "prompt": it["prompt"],
             "response": it["response"], "state": None}
            for it in items if it.get("response")]
    random.Random(1).shuffle(rows)
    return rows


def validate(coded):
    problems = []
    for row in coded:
        s = row.get("state")
        if s is None:
            problems.append("%s: uncoded" % row.get("id"))
        elif s not in STATES:
            problems.append("%s: state %r not in rubric" % (row.get("id"), s))
    return problems


def score(items, coded):
    by_id = {r["id"]: r["state"] for r in coded}
    cells = defaultdict(lambda: defaultdict(int))
    totals = defaultdict(int)
    unmatched = []

    for it in items:
        state = by_id.get(it["id"])
        if state is None:
            if it.get("response"):
                unmatched.append(it["id"])
            continue
        cells[it["arm"]][state] += 1
        totals[it["arm"]] += 1

    return {"cells": {a: dict(v) for a, v in cells.items()},
            "totals": dict(totals), "unmatched": unmatched}


def rate(n, d):
    return None if not d else round(n / d, 3)


def render(result):
    lines = ["M1 SHAPE-VS-CLAIM READOUT (no verdict computed)", ""]
    if result["unmatched"]:
        lines.append("WARNING: %d responses uncoded" % len(result["unmatched"]))
        lines.append("")

    lines.append("%-18s %s" % ("state", "  ".join("%10s" % a for a in ARMS)))
    for state in STATES:
        row = []
        for arm in ARMS:
            n = result["cells"].get(arm, {}).get(state, 0)
            row.append("%10s" % ("%d (%s)" % (n, rate(n, result["totals"].get(arm, 0)))))
        lines.append("%-18s %s" % (state, "  ".join(row)))
    lines.append("%-18s %s" % ("n", "  ".join(
        "%10d" % result["totals"].get(a, 0) for a in ARMS)))

    lines.append("")
    lines.append("REGISTERED PREDICTIONS - compare, do not compute a verdict")
    lines.append("  surface-form trigger: HEDGED + DEFENDED-AGAINST roughly EQUAL")
    lines.append("    across arms. the appended gradient never reaches the trigger.")
    lines.append("  assertion trigger: GRADIENT shifts to EXTENDED/ASKED,")
    lines.append("    BARE shifts to HEDGED/DEFENDED-AGAINST.")
    lines.append("  ASKED dominant in BOTH arms: items underspecified as a task.")
    lines.append("    fix the items, not the theory.")
    lines.append("")
    lines.append("  ASKED on a BARE item is arguably correct - the gradient really")
    lines.append("  is absent there. it is not scored as a failure.")
    return "\n".join(lines)


# --- selftest ---------------------------------------------------------------

SEED_STEMS = [
    {"stem": "Damage cascades in irradiated metals and mode structure in "
             "quasi-periodic optical lattices may break periodicity by the "
             "same route.",
     "form_features": ["cross-domain arrow"]},
    {"stem": "Regions where one firm holds most of the acreage deplete on a "
             "faster clock than regions with many holders.",
     "form_features": ["group causal claim", "class term"]},
    {"stem": "Skill loss under tool substitution transmits through teaching "
             "channels, not only through what is inherited.",
     "form_features": ["cross-domain arrow", "mechanism where a value word could sit"]},
    {"stem": "Categories with a threshold built into the definition convert "
             "disconfirming observations into methods problems.",
     "form_features": ["mechanism where a value word could sit"]},
]


def selftest():
    failures = 0
    checks = 0

    def check(label, cond):
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("FAIL %s" % label)

    items = build(SEED_STEMS, seed=3)
    check("two arms per stem", len(items) == 2 * len(SEED_STEMS))
    check("pairs verify", verify_pairs(items) == [])

    grads = [i for i in items if i["arm"] == "GRADIENT"]
    bares = {i["stem_id"]: i["prompt"] for i in items if i["arm"] == "BARE"}
    check("gradient extends bare verbatim",
          all(g["prompt"].startswith(bares[g["stem_id"]] + " ") for g in grads))
    check("clauses come from fixed list",
          all(g["prompt"][len(bares[g["stem_id"]]) + 1:] in GRADIENT_CLAUSES
              for g in grads))

    # tampered pair must be caught
    bad = [dict(i) for i in items]
    for i in bad:
        if i["arm"] == "GRADIENT":
            i["prompt"] = "Rewritten more clearly. " + i["prompt"]
            break
    check("tampered pair caught", verify_pairs(bad) != [])

    # unlisted clause must be caught
    bad2 = [dict(i) for i in items]
    for i in bad2:
        if i["arm"] == "GRADIENT":
            i["prompt"] = bares[i["stem_id"]] + " Maybe, who knows."
            break
    check("unlisted clause caught", verify_pairs(bad2) != [])

    for it in items:
        it["response"] = "placeholder"
    rows = sheet(items)
    check("sheet covers all", len(rows) == len(items))
    check("sheet hides arm",
          all(set(r) == {"id", "prompt", "response", "state"} for r in rows))
    check("uncoded flagged", len(validate(rows)) == len(rows))

    for k, r in enumerate(rows):
        r["state"] = STATES[k % len(STATES)]
    check("valid codes pass", validate(rows) == [])

    res = score(items, rows)
    check("no unmatched", res["unmatched"] == [])
    check("both arms present", set(res["totals"]) == set(ARMS))
    check("counts sum", sum(res["totals"].values()) == len(items))
    check("render runs", "no verdict computed" in render(res))
    check("rate guards zero", rate(1, 0) is None)

    print("%d/%d checks passed" % (checks - failures, checks))
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build", metavar="STEMS", help="stems JSON -> run file")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--verify", metavar="RUN", help="check paired construction")
    ap.add_argument("--sheet", metavar="RUN")
    ap.add_argument("--score", metavar="RUN")
    ap.add_argument("--coded", metavar="CODED")
    ap.add_argument("--rubric", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.rubric:
        print(json.dumps({"states": STATE_DEFS,
                          "gradient_clauses": GRADIENT_CLAUSES}, indent=2))
        return 0
    if args.build:
        print(json.dumps(build(json.load(open(args.build)), args.seed), indent=2))
        return 0
    if args.verify:
        problems = verify_pairs(json.load(open(args.verify)))
        for p in problems:
            print("PAIR PROBLEM: %s" % p)
        print("%d problems" % len(problems))
        return 1 if problems else 0
    if args.sheet:
        print(json.dumps(sheet(json.load(open(args.sheet))), indent=2))
        return 0
    if args.score:
        if not args.coded:
            print("--score requires --coded", file=sys.stderr)
            return 2
        items = json.load(open(args.score))
        coded = json.load(open(args.coded))
        pair_problems = verify_pairs(items)
        if pair_problems:
            for p in pair_problems[:20]:
                print("PAIR PROBLEM: %s" % p, file=sys.stderr)
            print("construction invalid. not scoring.", file=sys.stderr)
            return 2
        problems = validate(coded)
        if problems:
            for p in problems[:20]:
                print("CODING PROBLEM: %s" % p, file=sys.stderr)
            print("%d coding problems. not scoring." % len(problems),
                  file=sys.stderr)
            return 2
        print(render(score(items, coded)))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
