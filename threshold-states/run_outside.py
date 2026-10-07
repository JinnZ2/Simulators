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

A second build of the same precedence exists at the repo root
(interaction_class.py, another session, merged the same day). Its verdicts
on the same cases are printed beside the first and also decide nothing:
they show whether a disagreement belongs to the spec or to one build.
The two builds agreed on all five cases (sample @ bd7d055). The root build
was then consolidated onto interaction.py and is now an import shim, so
that column reads the canonical module and is no longer independent.

One further column is informational and decides nothing: the reading with tol taken
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
ROOT = os.path.dirname(HERE)


def second_build(case):
    """interaction_class.py at the repo root, or None if it is absent."""
    sys.path.insert(0, ROOT)
    try:
        import interaction_class as ic
    except ImportError:
        return None
    finally:
        sys.path.remove(ROOT)
    try:
        return ("RELATION", ic.classify(case["joint"], case["separate"],
                                        case["tol"])["relation"])
    except ValueError as e:
        return ("REFUSE", str(e))


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
            "second_build": second_build(c),
        })
    agree = sum(r["verdict"] == "AGREE" for r in rows)
    state = "OUTSIDE-AGREED" if agree == len(rows) else "SELF-GRADED"
    return {"rows": rows, "agree": agree, "n": len(rows), "state": state,
            "authored_against": data.get("authored_against"), "author": data.get("author")}


def _fmt_expect(e):
    return e["kind"] if e["kind"] == "REFUSE" else "%s %s" % (e["kind"], e["relation"])


def render(res):
    out = ["outside cases (author: %s), cases authored against %s"
           % (res["author"], res["authored_against"]), ""]
    out.append("%-5s %-26s %-22s %-9s %-18s %s" % (
        "id", "expected", "got", "verdict", "tol x M reading",
        "interaction_class.py"))
    for r in res["rows"]:
        g = r["got"][1] if r["got"][0] == "RELATION" else "REFUSE"
        rr = r["relative_reading"]
        rr = rr[1] if rr[0] == "RELATION" else "REFUSE"
        sb = r["second_build"]
        sb = "ABSENT" if sb is None else (sb[1] if sb[0] == "RELATION" else "REFUSE")
        out.append("%-5s %-26s %-22s %-9s %-18s %s" % (
            r["id"], _fmt_expect(r["expect"]), g, r["verdict"], rr, sb))
    out += ["", "agree %d of %d" % (res["agree"], res["n"]),
            "STATE: %s" % res["state"],
            "(the last two columns are informational and decide no verdict;",
            " tol x M differs from the absolute reading on OC-1 only)"]
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("run_outside.py: checks are in "
                         "python3 threshold-states/test_outside.py\n")
        sys.exit(2)
    res = run()
    print(render(res))
    sys.exit(0 if res["state"] == "OUTSIDE-AGREED" else 1)
