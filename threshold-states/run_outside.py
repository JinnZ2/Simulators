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

STATE is SELF-GRADED unless every case AGREEs; then OUTSIDE-AGREED. That is
the author's lift rule, stated in the file.

One column is informational and decides nothing: the reading with tol taken
relative (tol * M) beside the absolute one, because OC-1 turns on that
question. It does not change any AGREE / DISAGREE.

Exit 0 when all agree, 1 otherwise. Refuses --selftest (exit 2); the checks
are in test_outside.py. Stdlib only.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interaction as ix  # noqa: E402

CASES = os.path.join(HERE, "outside_cases.json")


def load(path=CASES):
    with open(path) as f:
        return json.load(f)


def outcome(case, tol_scale=None):
    """('RELATION', r) or ('REFUSE', message). tol_scale multiplies tol."""
    tol = case["tol"]
    try:
        if tol_scale is not None:
            tol = tol * ix.references(case["separate"])[1]
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
        got = outcome(c)
        rel = outcome(c, tol_scale="M")
        rows.append({
            "id": c["id"], "expect": c["expect"], "got": got,
            "verdict": "AGREE" if judge(c["expect"], got) else "DISAGREE",
            "relative_reading": rel,
            "readings_agree": rel == got,
        })
    agree = sum(r["verdict"] == "AGREE" for r in rows)
    state = "OUTSIDE-AGREED" if agree == len(rows) else "SELF-GRADED"
    return {"rows": rows, "agree": agree, "n": len(rows), "state": state,
            "run_against": data.get("run_against"), "author": data.get("author")}


def _fmt_expect(e):
    return e["kind"] if e["kind"] == "REFUSE" else "%s %s" % (e["kind"], e["relation"])


def render(res):
    out = ["outside cases (author: %s), run against %s"
           % (res["author"], res["run_against"]), ""]
    out.append("%-5s %-26s %-22s %-9s %s" % ("id", "expected", "got", "verdict",
                                            "tol x M reading"))
    for r in res["rows"]:
        g = r["got"][1] if r["got"][0] == "RELATION" else "REFUSE"
        rr = r["relative_reading"]
        rr = rr[1] if rr[0] == "RELATION" else "REFUSE"
        mark = "" if r["readings_agree"] else "  (readings differ)"
        out.append("%-5s %-26s %-22s %-9s %s%s" % (
            r["id"], _fmt_expect(r["expect"]), g, r["verdict"], rr, mark))
    out += ["", "agree %d of %d" % (res["agree"], res["n"]),
            "STATE: %s" % res["state"],
            "(the tol x M column is informational and decides no verdict)"]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("run_outside.py: checks are in "
                         "python3 threshold-states/test_outside.py\n")
        sys.exit(2)
    res = run()
    print(render(res))
    sys.exit(0 if res["state"] == "OUTSIDE-AGREED" else 1)
