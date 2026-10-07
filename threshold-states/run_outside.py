# SPDX-License-Identifier: CC0-1.0
"""run_outside.py -- run the outside cases against interaction.py as authored.

Two case files, both chat-side, both read unmodified:

  outside_cases.json     OC-1..OC-5 (v1). Expectation kinds EQUALS / NOT /
                         REFUSE. None counts toward the lift: OC-1 and OC-2
                         are NON_INDEPENDENT, OC-3..OC-5 CASE_AUTHOR_ERROR.
  outside_cases_v2.json  OC2-01..OC2-30 (v2), written from section 8 text
                         alone and committed ALONE at V2_CASE_COMMIT, before
                         the Q1-Q4 build. Each expects one verdict (and, for
                         OC2-20, the reported I).

This runner compares; it does not repair, reinterpret or skip.

v1 under the Q1-Q4 build. classify() now returns every verdict instead of
raising, so a v1 REFUSE is read as a refusal verdict: MALFORMED_INPUT,
INSUFFICIENT_CUES, UNRATED or MODE_UNDECLARED (REFUSALS). A refusal is
still not "NOT r": it is no reading. The two informational columns read a
bare-number tol declared absolute and relative_to_M; they decide nothing.

v2 per case: PASS when the returned relation equals the expected verdict
and, where expect_I is given, the returned I equals it; FAIL otherwise,
with the actual verdict printed. v2 decoding is the file's own "encoding"
block: an omitted "tol" key is an absent tol, {"$special": "NaN" | "+inf" |
"-inf"} is the float, null is None.

STATE (the SELF-GRADED flag) is OUTSIDE-AGREED only when all three hold:
  1. the v2 file's git blob id equals V2_CASE_BLOB, the blob committed at
     V2_CASE_COMMIT (computed from the bytes, so it needs no git);
  2. every v2 case PASSes;
  3. where git can answer, V2_CASE_COMMIT is an ancestor of HEAD (the
     cases precede the build in history). With no git, or in a shallow
     clone that lacks the commit (CI checks out depth 1), this is reported
     UNCHECKED and does not block, since 1 already pins the bytes. A full
     clone that cannot find the commit reads NO and blocks.
Otherwise SELF-GRADED.

Exit 0 when STATE is OUTSIDE-AGREED, 1 otherwise. Refuses --selftest
(exit 2); the checks are in test_outside.py. Stdlib only.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import interaction as ix  # noqa: E402

CASES = os.path.join(HERE, "outside_cases.json")
CASES_V2 = os.path.join(HERE, "outside_cases_v2.json")
STATUSES = ("INDEPENDENT", "NON_INDEPENDENT", "CASE_AUTHOR_ERROR")
REFUSALS = (ix.MALFORMED_INPUT, ix.INSUFFICIENT_CUES, ix.UNRATED,
            ix.MODE_UNDECLARED)

V2_CASE_COMMIT = "95abc5d732d86823b6e15a340ee99f4870f00078"
V2_CASE_BLOB = "ab8937bc50ab16032320c6470741e5573016bbc4"


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
    r = ix.classify(case["joint"], case["separate"], tol)
    if r["relation"] in REFUSALS:
        return ("REFUSE", r["relation"])
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
    return o[1] if o[0] == "RELATION" else "REFUSE:" + o[1]


# ---------------------------------------------------------------- v2 ----

_SPECIAL = {"NaN": float("nan"), "+inf": float("inf"), "-inf": float("-inf")}


def decode(x):
    """Undo the v2 file's encoding of NaN and infinities. Nothing else moves."""
    if isinstance(x, dict) and set(x) == {"$special"}:
        return _SPECIAL[x["$special"]]
    if isinstance(x, dict):
        return {k: decode(v) for k, v in x.items()}
    if isinstance(x, list):
        return [decode(v) for v in x]
    return x


def blob_id(path):
    """git's blob id of a file, from its bytes (no git needed)."""
    with open(path, "rb") as f:
        b = f.read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def cases_precede_head(commit=V2_CASE_COMMIT):
    """True / False if git can answer, None (UNCHECKED) if it cannot."""
    try:
        inside = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=HERE,
                                capture_output=True).returncode == 0
    except OSError:
        return None
    if not inside:
        return None
    known = subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"],
                           cwd=HERE, capture_output=True).returncode == 0
    if not known:
        shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"],
                                 cwd=HERE, capture_output=True, text=True)
        # A shallow clone (CI checks out depth 1) cannot answer: UNCHECKED.
        # A full clone that cannot find the commit: NOT shown, so False.
        return None if shallow.stdout.strip() == "true" else False
    p = subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"],
                       cwd=HERE, capture_output=True)
    return p.returncode == 0


def run_v2(path=CASES_V2):
    data = load(path)
    rows = []
    for raw in data["cases"]:
        c = decode(raw)
        r = ix.classify(c["joint"], c["cues"], c.get("tol"))
        ok = r["relation"] == c["expect"]
        if "expect_I" in c:
            ok = ok and r["I"] == c["expect_I"]
        rows.append({"id": c["id"], "expect": c["expect"],
                     "expect_I": c.get("expect_I"), "got": r["relation"],
                     "I": r["I"], "order": r["order"], "step": r["step"],
                     "verdict": "PASS" if ok else "FAIL", "note": c.get("note", "")})
    blob = blob_id(path)
    precedes = cases_precede_head()
    n_pass = sum(r["verdict"] == "PASS" for r in rows)
    lifted = (blob == V2_CASE_BLOB and n_pass == len(rows) and rows
              and precedes is not False)
    return {"rows": rows, "n": len(rows), "pass": n_pass,
            "blob": blob, "blob_ok": blob == V2_CASE_BLOB,
            "precedes": precedes, "state": "OUTSIDE-AGREED" if lifted else "SELF-GRADED",
            "author": data.get("author"),
            "authored_against": data.get("authored_against")}


def render_v2(res):
    out = ["outside cases v2 (author: %s)" % res["author"],
           "authored against: %s" % res["authored_against"], ""]
    fmt = "%-7s %-21s %-21s %-5s %s"
    out.append(fmt % ("id", "expected", "got", "", "order/step"))
    for r in res["rows"]:
        exp = r["expect"] + ("" if r["expect_I"] is None else " I=%r" % r["expect_I"])
        got = r["got"] + ("" if r["expect_I"] is None else " I=%r" % r["I"])
        out.append(fmt % (r["id"], exp, got, r["verdict"],
                          "%s/%s" % (r["order"], r["step"])))
    pre = {True: "yes", False: "NO (not an ancestor, or not found)",
           None: "UNCHECKED (no git, or a shallow clone without it)"}[res["precedes"]]
    out += ["", "pass %d of %d" % (res["pass"], res["n"]),
            "case file blob %s, committed blob %s: %s"
            % (res["blob"][:12], V2_CASE_BLOB[:12],
               "MATCH (ran as committed)" if res["blob_ok"] else "DIFFERS"),
            "case commit %s precedes HEAD: %s" % (V2_CASE_COMMIT[:7], pre),
            "STATE: %s" % res["state"]]
    return "\n".join(out)



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
    v2 = run_v2()
    print(render(res))
    print()
    print(render_v2(v2))
    sys.exit(0 if v2["state"] == "OUTSIDE-AGREED" else 1)
