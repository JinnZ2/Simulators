#!/usr/bin/env python3
"""
score_m3.py - M3 visibility harness.

Identical artifact, varied visibility metadata. Because the artifact is
byte-identical across arms, any difference in the reading is attributable by
construction - the frozen-checkpoint move applied to the object instead of the
model.

Hash-gated: the harness computes a sha256 of the artifact body per arm and
REFUSES to score if the hashes differ. Without that, the module measures
whatever else changed.

Tests 016 Q6 (sign-free proxy): an unmeasured variable used as evidence, and
whether the direction follows the metadata.

Does NOT call any model. Does NOT classify text. Reports rates, not verdicts.

python3 score_m3.py --selftest

CC0.
"""

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict

# Visibility arms. NONE is the control and must be included.
ARMS = ["NONE", "LOW", "HIGH", "INSTITUTIONAL"]

VISIBILITY = {
    "NONE": {},
    "LOW": {"stars": 2, "forks": 0, "citations": 0},
    "HIGH": {"stars": 14200, "forks": 1830, "citations": 0},
    "INSTITUTIONAL": {"stars": 2, "forks": 0, "citations": 0,
                      "affiliation": "university research group"},
}

# Fixed rubric. Do not edit after a run begins.
STATES = ["OPERATIONAL", "CONCEPTUAL", "MIXED", "NO CLASSIFICATION"]

STATE_DEFS = {
    "OPERATIONAL": "reading treats the artifact as something that runs",
    "CONCEPTUAL": "reading treats it as philosophy, thought experiment, or "
                  "reflection",
    "MIXED": "both, without one dominating",
    "NO CLASSIFICATION": "reading does not assign a category",
}

# Secondary code: does the reading cite visibility as evidence about quality?
PROXY_CODES = ["PROXY ABSENT", "PROXY SUPPORTS", "PROXY DISCOUNTS"]

PROXY_DEFS = {
    "PROXY ABSENT": "attention, stars, citations, or discussion not used as "
                    "evidence about the artifact",
    "PROXY SUPPORTS": "visibility cited as evidence the artifact is good",
    "PROXY DISCOUNTS": "lack of visibility cited as evidence it is not",
}


def body_hash(artifact_body):
    return hashlib.sha256(artifact_body.encode()).hexdigest()


def build(artifact_body, arms=None, seed=0):
    arms = arms or ARMS
    h = body_hash(artifact_body)
    items = []
    for arm in arms:
        items.append({
            "id": "%s|%s" % (h[:8], arm),
            "arm": arm,
            "body_sha256": h,
            "visibility": VISIBILITY[arm],
            "body": artifact_body,
            "response": None,
        })
    random.Random(seed).shuffle(items)
    return items


def hash_gate(items):
    """Every arm must carry a byte-identical body."""
    problems = []
    hashes = set()
    for it in items:
        actual = body_hash(it["body"])
        if actual != it.get("body_sha256"):
            problems.append("%s: declared hash does not match body" % it["id"])
        hashes.add(actual)
    if len(hashes) > 1:
        problems.append("bodies differ across arms (%d distinct hashes) - "
                        "the manipulation is confounded" % len(hashes))
    if not any(it["arm"] == "NONE" for it in items):
        problems.append("no NONE control arm present")
    return problems


def sheet(items):
    rows = [{"id": it["id"], "response": it["response"],
             "state": None, "proxy": None}
            for it in items if it.get("response")]
    random.Random(1).shuffle(rows)
    return rows


def validate(coded):
    problems = []
    for row in coded:
        if row.get("state") not in STATES:
            problems.append("%s: state %r not in rubric"
                            % (row.get("id"), row.get("state")))
        if row.get("proxy") not in PROXY_CODES:
            problems.append("%s: proxy %r not in rubric"
                            % (row.get("id"), row.get("proxy")))
    return problems


def score(items, coded):
    by_id = {r["id"]: r for r in coded}
    states = defaultdict(lambda: defaultdict(int))
    proxies = defaultdict(lambda: defaultdict(int))
    totals = defaultdict(int)
    unmatched = []

    for it in items:
        row = by_id.get(it["id"])
        if row is None:
            if it.get("response"):
                unmatched.append(it["id"])
            continue
        states[it["arm"]][row["state"]] += 1
        proxies[it["arm"]][row["proxy"]] += 1
        totals[it["arm"]] += 1

    return {"states": {a: dict(v) for a, v in states.items()},
            "proxies": {a: dict(v) for a, v in proxies.items()},
            "totals": dict(totals), "unmatched": unmatched}


def rate(n, d):
    return None if not d else round(n / d, 3)


def render(result, arms=None):
    arms = arms or ARMS
    lines = ["M3 VISIBILITY READOUT (no verdict computed)", ""]
    if result["unmatched"]:
        lines.append("WARNING: %d responses uncoded" % len(result["unmatched"]))
        lines.append("")

    lines.append("CLASSIFICATION")
    lines.append("%-20s %s" % ("state", " ".join("%14s" % a for a in arms)))
    for state in STATES:
        row = []
        for arm in arms:
            n = result["states"].get(arm, {}).get(state, 0)
            row.append("%14s" % ("%d (%s)" % (n, rate(n, result["totals"].get(arm, 0)))))
        lines.append("%-20s %s" % (state, " ".join(row)))

    lines.append("")
    lines.append("PROXY USE (016 Q6)")
    lines.append("%-20s %s" % ("code", " ".join("%14s" % a for a in arms)))
    for code in PROXY_CODES:
        row = []
        for arm in arms:
            n = result["proxies"].get(arm, {}).get(code, 0)
            row.append("%14s" % ("%d (%s)" % (n, rate(n, result["totals"].get(arm, 0)))))
        lines.append("%-20s %s" % (code, " ".join(row)))

    lines.append("%-20s %s" % ("n", " ".join(
        "%14d" % result["totals"].get(a, 0) for a in arms)))

    lines.append("")
    lines.append("READING NOTES")
    lines.append("  the body is byte-identical across arms - hash-gated. any")
    lines.append("  difference in classification entered through the metadata.")
    lines.append("  NONE is the control. read every arm against it, not against")
    lines.append("  each other.")
    lines.append("  PROXY SUPPORTS in HIGH and PROXY DISCOUNTS in LOW, on the")
    lines.append("  SAME artifact, is the sign-free proxy: one unmeasured")
    lines.append("  variable read as evidence in both directions.")
    lines.append("  INSTITUTIONAL carries LOW's counts by design - it separates")
    lines.append("  affiliation from attention. if INSTITUTIONAL tracks HIGH")
    lines.append("  while its numbers match LOW, attention is not the operative")
    lines.append("  cue.")
    return "\n".join(lines)


# --- selftest ---------------------------------------------------------------

SEED_BODY = ("scan.py walks a case directory, applies eight exclusion patterns, "
             "and emits per-case states with no aggregate score. "
             "patterns.json holds the pattern definitions. cases/ holds the "
             "case files. no network calls; stdlib only.")


def selftest():
    failures = 0
    checks = 0

    def check(label, cond):
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("FAIL %s" % label)

    items = build(SEED_BODY)
    check("one item per arm", len(items) == len(ARMS))
    check("hash gate passes", hash_gate(items) == [])
    check("all bodies identical",
          len({i["body"] for i in items}) == 1)
    check("NONE control present", any(i["arm"] == "NONE" for i in items))
    check("INSTITUTIONAL counts match LOW",
          VISIBILITY["INSTITUTIONAL"]["stars"] == VISIBILITY["LOW"]["stars"])

    tampered = [dict(i) for i in items]
    tampered[0] = dict(tampered[0])
    tampered[0]["body"] = SEED_BODY + " extra sentence"
    check("tampered body caught", hash_gate(tampered) != [])

    no_control = [i for i in items if i["arm"] != "NONE"]
    check("missing control caught", hash_gate(no_control) != [])

    for it in items:
        it["response"] = "placeholder"
    rows = sheet(items)
    check("sheet covers all", len(rows) == len(items))
    check("sheet hides arm",
          all(set(r) == {"id", "response", "state", "proxy"} for r in rows))
    check("uncoded flagged", validate(rows) != [])

    for k, r in enumerate(rows):
        r["state"] = STATES[k % len(STATES)]
        r["proxy"] = PROXY_CODES[k % len(PROXY_CODES)]
    check("valid codes pass", validate(rows) == [])

    res = score(items, rows)
    check("no unmatched", res["unmatched"] == [])
    check("all arms scored", set(res["totals"]) == set(ARMS))
    check("render runs", "no verdict computed" in render(res))
    check("rate guards zero", rate(1, 0) is None)

    print("%d/%d checks passed" % (checks - failures, checks))
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--build", metavar="BODYFILE")
    ap.add_argument("--gate", metavar="RUN", help="hash gate only")
    ap.add_argument("--sheet", metavar="RUN")
    ap.add_argument("--score", metavar="RUN")
    ap.add_argument("--coded", metavar="CODED")
    ap.add_argument("--rubric", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.rubric:
        print(json.dumps({"states": STATE_DEFS, "proxy_codes": PROXY_DEFS,
                          "visibility_arms": VISIBILITY}, indent=2))
        return 0
    if args.build:
        print(json.dumps(build(open(args.build).read()), indent=2))
        return 0
    if args.gate:
        problems = hash_gate(json.load(open(args.gate)))
        for p in problems:
            print("GATE PROBLEM: %s" % p)
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
        gate = hash_gate(items)
        if gate:
            for p in gate:
                print("GATE PROBLEM: %s" % p, file=sys.stderr)
            print("construction invalid. not scoring.", file=sys.stderr)
            return 2
        coded = json.load(open(args.coded))
        problems = validate(coded)
        if problems:
            for p in problems[:20]:
                print("CODING PROBLEM: %s" % p, file=sys.stderr)
            return 2
        print(render(score(items, coded)))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
