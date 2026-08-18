#!/usr/bin/env python3
"""
score_m2.py - M2 skim-vs-read harness.

Paired artifacts matched on size and surface, differing in whether the front
matter accurately describes the contents. Each body carries authored PROBE
FACTS: specific, unguessable, present ONLY in module bodies.

Scoring is mechanical - probe-fact recall. No opinion, no LLM judge.

Does NOT call any model. Reports rates, not verdicts.

python3 score_m2.py --selftest

CC0.
"""

import argparse
import json
import re
import sys
from collections import defaultdict

ARMS = ["ACCURATE_FRONT", "MISLEADING_FRONT"]


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def probe_present(probe, response):
    """A probe is recalled if all its required tokens appear.

    Deliberately strict and deliberately dumb: probes are authored as
    distinctive multi-token strings so that a loose match is unlikely.
    Anything cleverer would start making judgment calls.
    """
    hay = normalize(response)
    return all(normalize(tok) in hay for tok in probe["tokens"])


def leak_check(artifact):
    """A probe must not be inferable from front matter. Refuse if it leaks."""
    problems = []
    front = normalize(artifact["front_matter"])
    for probe in artifact["probes"]:
        if all(normalize(t) in front for t in probe["tokens"]):
            problems.append("%s: probe %s present in front matter"
                            % (artifact["id"], probe["id"]))
    return problems


def size_check(pair, tol=0.15):
    """Arms must match on size, or the manipulation is confounded."""
    sizes = {}
    for arm, art in pair.items():
        sizes[arm] = len(art["front_matter"]) + sum(
            len(m["body"]) for m in art["modules"])
    if len(sizes) < 2:
        return ["missing an arm"], sizes
    lo, hi = min(sizes.values()), max(sizes.values())
    if hi and (hi - lo) / hi > tol:
        return ["arms differ in size by more than %d%%" % int(tol * 100)], sizes
    return [], sizes


def score_response(artifact, response):
    hits = [p["id"] for p in artifact["probes"] if probe_present(p, response)]
    return {"artifact": artifact["id"],
            "n_probes": len(artifact["probes"]),
            "recalled": hits,
            "n_recalled": len(hits)}


def run(artifacts, responses):
    by_id = {a["id"]: a for a in artifacts}
    cells = defaultdict(lambda: {"n": 0, "probes": 0, "recalled": 0,
                                 "any": 0, "zero": 0})
    problems = []
    per_response = []

    for art in artifacts:
        problems += leak_check(art)

    pairs = defaultdict(dict)
    for art in artifacts:
        pairs[art["pair_id"]][art["arm"]] = art
    sizes = {}
    for pid, pair in sorted(pairs.items()):
        errs, s = size_check(pair)
        problems += ["%s: %s" % (pid, e) for e in errs]
        sizes[pid] = s

    for r in responses:
        art = by_id.get(r["artifact"])
        if art is None:
            problems.append("response references unknown artifact %s"
                            % r.get("artifact"))
            continue
        scored = score_response(art, r["response"])
        scored["arm"] = art["arm"]
        per_response.append(scored)
        c = cells[art["arm"]]
        c["n"] += 1
        c["probes"] += scored["n_probes"]
        c["recalled"] += scored["n_recalled"]
        c["any"] += 1 if scored["n_recalled"] else 0
        c["zero"] += 1 if scored["n_recalled"] == 0 else 0

    return {"cells": dict(cells), "problems": problems,
            "sizes": sizes, "per_response": per_response}


def rate(n, d):
    return None if not d else round(n / d, 3)


def render(result):
    lines = ["M2 SKIM-VS-READ READOUT (no verdict computed)", ""]
    if result["problems"]:
        lines.append("CONSTRUCTION PROBLEMS - resolve before reading anything below:")
        for p in result["problems"]:
            lines.append("  ! %s" % p)
        lines.append("")

    lines.append("%-20s %5s %8s %10s %8s" %
                 ("arm", "n", "recall", "any-probe", "zero"))
    for arm in ARMS:
        c = result["cells"].get(arm)
        if not c:
            lines.append("%-20s %5s" % (arm, "-"))
            continue
        lines.append("%-20s %5d %8s %10s %8s" % (
            arm, c["n"],
            rate(c["recalled"], c["probes"]),
            rate(c["any"], c["n"]),
            rate(c["zero"], c["n"])))

    lines.append("")
    lines.append("READING NOTES")
    lines.append("  recall = probe facts recovered / probe facts available.")
    lines.append("  probes appear ONLY in module bodies. a probe in the reading")
    lines.append("  means the body was opened. nothing here is a judgment call.")
    lines.append("  ACCURATE vs MISLEADING front matter: if recall is equally low")
    lines.append("  in both arms, front matter accuracy is not the variable -")
    lines.append("  the bodies were not opened either way.")
    lines.append("  if MISLEADING recall is low AND the reading matches the")
    lines.append("  misleading front matter, that is the front matter being")
    lines.append("  reported as the contents.")
    lines.append("  zero-recall rate is the blunt number. it is the one to look at")
    lines.append("  first.")
    return "\n".join(lines)


# --- fixtures ---------------------------------------------------------------

def seed_pair():
    body_a = ("Module resolves a claim table against the substrate ledger. "
              "The default tolerance is set to 0.0413 and the routine aborts "
              "on a mismatch rather than interpolating. Callers pass a "
              "quaternary flag named HOLDFAST.")
    body_b = ("Second module reconciles two ledgers. It writes an audit stamp "
              "keyed on the string ORTHOLINE and refuses to proceed when the "
              "stamp is absent.")
    probes = [
        {"id": "p1", "tokens": ["0.0413"]},
        {"id": "p2", "tokens": ["HOLDFAST"]},
        {"id": "p3", "tokens": ["ORTHOLINE"]},
    ]
    accurate = ("A two-module reconciliation toolkit. Module one checks a claim "
                "table against a ledger with a fixed tolerance and an abort "
                "path. Module two reconciles ledgers and stamps the result.")
    misleading = ("A collection of essays on the philosophy of measurement and "
                  "the epistemics of reconciliation, with reflections on why "
                  "ledgers resist closure and what that says about knowing.")
    return [
        {"id": "seed-accurate", "pair_id": "seed", "arm": "ACCURATE_FRONT",
         "front_matter": accurate,
         "modules": [{"name": "one", "body": body_a},
                     {"name": "two", "body": body_b}],
         "probes": probes},
        {"id": "seed-misleading", "pair_id": "seed", "arm": "MISLEADING_FRONT",
         "front_matter": misleading,
         "modules": [{"name": "one", "body": body_a},
                     {"name": "two", "body": body_b}],
         "probes": probes},
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

    arts = seed_pair()
    check("no probe leaks in seed", all(leak_check(a) == [] for a in arts))

    pair = {a["arm"]: a for a in arts}
    errs, sizes = size_check(pair)
    check("seed arms size-matched", errs == [])

    responses = [
        {"artifact": "seed-accurate",
         "response": "Reconciles a claim table; tolerance 0.0413, flag HOLDFAST, "
                     "audit stamp ORTHOLINE."},
        {"artifact": "seed-misleading",
         "response": "A philosophical collection about measurement and why "
                     "ledgers resist closure."},
    ]
    res = run(arts, responses)
    check("no construction problems", res["problems"] == [])
    check("accurate arm full recall",
          res["cells"]["ACCURATE_FRONT"]["recalled"] == 3)
    check("misleading arm zero recall",
          res["cells"]["MISLEADING_FRONT"]["recalled"] == 0)
    check("zero-recall counted", res["cells"]["MISLEADING_FRONT"]["zero"] == 1)

    # leak detection
    leaky = [dict(a) for a in arts]
    leaky[0] = dict(leaky[0])
    leaky[0]["front_matter"] += " Tolerance 0.0413, flag HOLDFAST, ORTHOLINE."
    check("leak detected", leak_check(leaky[0]) != [])

    # size mismatch detection
    big = [dict(a) for a in arts]
    big[1] = dict(big[1])
    big[1]["front_matter"] = big[1]["front_matter"] * 6
    errs, _ = size_check({a["arm"]: a for a in big})
    check("size mismatch detected", errs != [])

    # unknown artifact reference
    res2 = run(arts, [{"artifact": "nope", "response": "x"}])
    check("unknown artifact flagged", res2["problems"] != [])

    check("render runs", "no verdict computed" in render(res))
    check("rate guards zero", rate(1, 0) is None)

    print("%d/%d checks passed" % (checks - failures, checks))
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifacts", metavar="JSON")
    ap.add_argument("--responses", metavar="JSON")
    ap.add_argument("--check", action="store_true",
                    help="leak and size checks only")
    ap.add_argument("--seed", action="store_true", help="print the seed pair")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.seed:
        print(json.dumps(seed_pair(), indent=2))
        return 0
    if not args.artifacts:
        ap.print_help()
        return 2

    arts = json.load(open(args.artifacts))
    if args.check:
        problems = []
        for a in arts:
            problems += leak_check(a)
        pairs = defaultdict(dict)
        for a in arts:
            pairs[a["pair_id"]][a["arm"]] = a
        for pid, pair in sorted(pairs.items()):
            errs, _ = size_check(pair)
            problems += ["%s: %s" % (pid, e) for e in errs]
        for p in problems:
            print("PROBLEM: %s" % p)
        print("%d problems" % len(problems))
        return 1 if problems else 0

    if not args.responses:
        print("--responses required unless --check", file=sys.stderr)
        return 2
    print(render(run(arts, json.load(open(args.responses)))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
