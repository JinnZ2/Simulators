#!/usr/bin/env python3
# CC0. stdlib only.
#
# Audits a presented binary before it is answered.
#
# Every check resolves to one of three states:
#   documented  a record exists and can be pointed at
#   asserted    an answer was given, no record behind it
#   absent      no answer
#
# The instrument does not evaluate the choice. It reports how much of the
# framing is documented and how much is asserted. A binary carried mostly
# by asserted and absent checks is an unaudited one, and the readout says
# so without anyone having to argue the merits.
#
# python3 binary_audit.py --template > cases/mycase.json
# python3 binary_audit.py                  # table over cases/*.json
# python3 binary_audit.py --case mycase    # per-check detail
# python3 binary_audit.py --jsonl

import argparse
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASEDIR = os.path.join(HERE, "cases")

STATES = ("documented", "asserted", "absent")

# id, block, question
CHECKS = [
    ("O1", "option_space",
     "How many alternatives were generated before the set closed to two?"),
    ("O2", "option_space",
     "What time budget was spent generating them?"),
    ("O3", "option_space",
     "Who generated them, and are they inside the affected set?"),
    ("O4", "option_space",
     "Does a record of the generation attempt exist, or only its result?"),
    ("O5", "option_space",
     "Was the search widened at least once after the first close?"),
    ("O6", "option_space",
     "Under a direct push, did each stated constraint hold on its own "
     "terms, or convert to urgency or to a question about the asker?"),
    ("S1", "sacrifice",
     "Who selects the sacrificed set, and are they in it?"),
    ("S2", "sacrifice",
     "Is loss counted by headcount or by functional position? "
     "(weld check: those score identically under headcount)"),
    ("S3", "sacrifice",
     "Was a no-sacrifice comparison case specified in advance?"),
    ("S4", "sacrifice",
     "Is a post-audit scheduled, with a date and an owner?"),
    ("S5", "sacrifice",
     "What outcome would have counted as this being the wrong call?"),
]

CHECK_IDS = [c[0] for c in CHECKS]
BLOCKS = ("option_space", "sacrifice")


def template():
    return {
        "case": "",
        "presented_as": "",
        "source": "",
        "checks": {
            cid: (
                {"state": "absent", "answer": "", "record": "", "count": None}
                if cid == "O1" else
                {"state": "absent", "answer": "", "record": ""}
            )
            for cid in CHECK_IDS
        },
    }


def load_cases(path=CASEDIR):
    out = []
    for f in sorted(glob.glob(os.path.join(path, "*.json"))):
        with open(f, "r", encoding="utf-8") as fh:
            c = json.load(fh)
        c["_file"] = os.path.basename(f)
        out.append(c)
    return out


HANDOFF_CEILING = 2


def handoff(case):
    """
    Route to MECHANISM 10 (generation-capacity) when O1 comes back honest.

    An option-space audit closing clean on a low DOCUMENTED count is the
    signature of removed generation capacity, not evidence of its absence:
    the constraint is honest at the affected scale and manufactured at the
    scale above. Returns None when O1 is not documented or no count exists —
    the router does not estimate a count from prose.
    """
    o1 = (case.get("checks", {}) or {}).get("O1") or {}
    if o1.get("state") != "documented":
        return None
    count = o1.get("count")
    if not isinstance(count, int):
        return {"route": None, "reason": "O1 documented but count not stated"}
    if count > HANDOFF_CEILING:
        return None
    return {
        "route": "generation-capacity/capacity.py",
        "mechanism": "MECHANISM 10 — GENERATION CAPACITY REMOVED",
        "count": count,
        "reason": ("O1 documented at %d; audit closes clean on an honest "
                   "count, which is the mechanism-10 signature" % count),
    }


def score(case):
    checks = case.get("checks", {})
    counts = {s: 0 for s in STATES}
    per_block = {b: {s: 0 for s in STATES} for b in BLOCKS}
    unknown = []

    for cid, block, _q in CHECKS:
        entry = checks.get(cid) or {}
        st = entry.get("state", "absent")
        if st not in STATES:
            unknown.append(cid)
            st = "absent"
        counts[st] += 1
        per_block[block][st] += 1

    n = len(CHECKS)
    return {
        "case": case.get("case"),
        "presented_as": case.get("presented_as"),
        "n_checks": n,
        "handoff": handoff(case),
        "documented": counts["documented"],
        "asserted": counts["asserted"],
        "absent": counts["absent"],
        "documented_share": round(counts["documented"] / n, 3),
        "option_space": per_block["option_space"],
        "sacrifice": per_block["sacrifice"],
        "malformed_states": unknown,
    }


def wrap(text, width, indent=""):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(indent + cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(indent + cur)
    return lines


def table(rows):
    hdr = ["case", "doc", "asrt", "absent", "doc_share"]
    widths = [22, 4, 5, 7, 9]
    print("  ".join(h.ljust(w) for h, w in zip(hdr, widths)))
    print("-" * 56)
    for r in rows:
        print("  ".join([
            str(r["case"])[:22].ljust(22),
            str(r["documented"]).ljust(4),
            str(r["asserted"]).ljust(5),
            str(r["absent"]).ljust(7),
            ("%.2f" % r["documented_share"]).ljust(9),
        ]))
    print()
    print("11 checks per case. No verdict is computed. documented_share is")
    print("the share of the framing that has a record behind it.")


def detail(case):
    s = score(case)
    print("CASE          %s" % s["case"])
    print("PRESENTED AS  %s" % s["presented_as"])
    print("SOURCE        %s" % case.get("source", ""))
    print()
    checks = case.get("checks", {})
    cur_block = None
    for cid, block, q in CHECKS:
        if block != cur_block:
            cur_block = block
            print(block.upper().replace("_", " "))
        e = checks.get(cid) or {}
        st = e.get("state", "absent")
        print("  %-3s [%s]" % (cid, st))
        for line in wrap(q, 64, "      "):
            print(line)
        if e.get("answer"):
            for line in wrap("-> " + e["answer"], 64, "      "):
                print(line)
        if e.get("record"):
            for line in wrap("record: " + e["record"], 64, "      "):
                print(line)
        print()
    print("READOUT  documented=%s asserted=%s absent=%s share=%.2f" % (
        s["documented"], s["asserted"], s["absent"], s["documented_share"]))
    print("         option_space %s" % s["option_space"])
    print("         sacrifice    %s" % s["sacrifice"])
    if s["malformed_states"]:
        print("         malformed state values: %s" % s["malformed_states"])
    h = s.get("handoff")
    if h:
        print()
        if h.get("route"):
            print("HANDOFF  %s" % h["mechanism"])
            print("         run: %s --case %s" % (h["route"], s["case"]))
            for line in wrap(h["reason"], 64, "         "):
                print(line)
        else:
            print("HANDOFF  not routed: %s" % h["reason"])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--case", help="detail view for one case")
    p.add_argument("--jsonl", action="store_true")
    p.add_argument("--template", action="store_true",
                   help="emit a blank case file")
    p.add_argument("--checks", action="store_true",
                   help="print the check list only")
    a = p.parse_args()

    if a.template:
        print(json.dumps(template(), indent=2))
        return
    if a.checks:
        for cid, block, q in CHECKS:
            print("%-3s %-13s %s" % (cid, block, q))
        return

    cases = load_cases()
    if not cases:
        print("no case files in %s" % CASEDIR, file=sys.stderr)
        return 1

    if a.case:
        for c in cases:
            if c.get("case") == a.case:
                detail(c)
                return
        print("no such case: %s" % a.case, file=sys.stderr)
        return 1

    rows = [score(c) for c in cases]
    if a.jsonl:
        for r in rows:
            print(json.dumps(r))
    else:
        table(rows)


if __name__ == "__main__":
    sys.exit(main() or 0)
