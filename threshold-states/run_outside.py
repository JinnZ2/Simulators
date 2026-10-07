# SPDX-License-Identifier: CC0-1.0
"""run_outside.py -- run outside_cases.json against interaction.py as authored.

Each case's expectation is the outside author's, read from the file. This
runner compares; it does not repair, reinterpret or skip. Per case:

    AGREE      the module's outcome satisfies the authored expectation
    DISAGREE   it does not

Expectation kinds (as delivered):
    EQUALS r   relation == r
    NOT r      relation != r, and the call returned (a refusal is not "not r";
               it is no reading)
    REFUSE     classify() raises InteractionError

Each case also carries a status, recorded after delivery (outside_cases.json
status_rule): INDEPENDENT, NON_INDEPENDENT (seen before the code change it
answers), or CASE_AUTHOR_ERROR (underspecified). Only INDEPENDENT cases
count toward the lift. STATE is OUTSIDE-AGREED when at least one case
counts and every counted case AGREEs; otherwise SELF-GRADED.

Two further columns are informational and decide nothing: the case read with
its bare tol declared absolute, and declared relative_to_M. OC-1 turns on
that difference.

Before the root build was archived (archive/interaction_class/), a column
here read the same cases through it; the two builds agreed on all five
(samples/run_outside.sample.txt @ bd7d055).

Exit 0 when STATE is OUTSIDE-AGREED, 1 otherwise. Refuses --selftest
(exit 2); the checks are in test_outside.py. Stdlib only.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interaction as ix  # noqa: E402

CASES = os.path.join(HERE, "outside_cases.json")
STATUSES = ("INDEPENDENT", "NON_INDEPENDENT", "CASE_AUTHOR_ERROR")


def load(path=CASES):
    with open(path) as f:
        return json.load(f)


def outcome(case, mode=None):
    """('RELATION', r) or ('REFUSE', message).

    mode None runs the case as authored. 'absolute' / 'relative_to_M' wrap a
    bare-number tol in that declared mode (informational only).
    """
    tol = case["tol"]
    if mode is not None and tol is not None and not isinstance(tol, dict):
        tol = {"value": tol, "mode": mode}
    try:
        r = ix.classify(case["joint"], case["separate"], tol)
    except ix.InteractionError as e:
        return ("REFUSE", str(e))
    return ("RELATION", r["relation"])


def judge(expect, got):
    kind, val = got
    k = expect["kind"]
    if k == "REFUSE":
        return kind == "REFUSE"
    if kind == "REFUSE":
        return False
    if k == "EQUALS":
        return val == expect["relation"]
    if k == "NOT":
        return val != expect["relation"]
    raise ValueError("unknown expectation kind %r" % k)


def run(data=None):
    data = data or load()
    rows = []
    for c in data["cases"]:
        status = c.get("status", "INDEPENDENT")
        if status not in STATUSES:
            raise ValueError("case %s: unknown status %r" % (c["id"], status))
        got = outcome(c)
        rows.append({
            "id": c["id"], "expect": c["expect"], "got": got,
            "verdict": "AGREE" if judge(c["expect"], got) else "DISAGREE",
            "status": status, "counts": status == "INDEPENDENT",
            "as_absolute": outcome(c, "absolute"),
            "as_relative": outcome(c, "relative_to_M"),
        })
    agree = sum(r["verdict"] == "AGREE" for r in rows)
    counted = [r for r in rows if r["counts"]]
    lifted = bool(counted) and all(r["verdict"] == "AGREE" for r in counted)
    return {"rows": rows, "agree": agree, "n": len(rows),
            "counted": len(counted),
            "counted_agree": sum(r["verdict"] == "AGREE" for r in counted),
            "state": "OUTSIDE-AGREED" if lifted else "SELF-GRADED",
            "authored_against": data.get("authored_against"),
            "author": data.get("author")}


def _fmt_expect(e):
    return e["kind"] if e["kind"] == "REFUSE" else "%s %s" % (e["kind"], e["relation"])


def _short(o):
    return o[1] if o[0] == "RELATION" else "REFUSE"


def render(res):
    out = ["outside cases (author: %s), cases authored against %s"
           % (res["author"], res["authored_against"]), ""]
    fmt = "%-5s %-25s %-21s %-9s %-18s %-21s %s"
    out.append(fmt % ("id", "expected", "got", "verdict", "status",
                      "as absolute", "as relative_to_M"))
    for r in res["rows"]:
        out.append(fmt % (r["id"], _fmt_expect(r["expect"]), _short(r["got"]),
                          r["verdict"], r["status"], _short(r["as_absolute"]),
                          _short(r["as_relative"])))
    out += ["", "agree %d of %d; counted toward the lift %d (agree %d)"
            % (res["agree"], res["n"], res["counted"], res["counted_agree"]),
            "STATE: %s" % res["state"],
            "(the last two columns are informational and decide no verdict)"]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("run_outside.py: checks are in "
                         "python3 threshold-states/test_outside.py\n")
        sys.exit(2)
    res = run()
    print(render(res))
    sys.exit(0 if res["state"] == "OUTSIDE-AGREED" else 1)
