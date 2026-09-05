#!/usr/bin/env python3
"""Checks for the falsifier-audit instrument. Known answers first, both
directions, on constructed inputs; the corpus is read but not asserted
against beyond stable structural facts. Writes samples/ and QUEUE.md.

    python3 falsifier-audit/selftest_fa.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import extract as E  # noqa: E402
import inventory as I  # noqa: E402
import checks as C  # noqa: E402
import axes as X  # noqa: E402
import queue as Q  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


TABLE_LAST = """
| id | claim | status | falsifier |
|---|---|---|---|
| X1 | the widget count rises with load | y | a run where the widget count falls as load rises |
| X2 | the frame is stable | y | — |
"""
TABLE_MID = """
| id | claim | falsified by | status |
|----|-------|--------------|--------|
| B1 | two-option situations occur only in descriptions | a physical two-option situation | open |
"""
PROSE = """
**RC_9 — smoke is late.**
Devices smoked seconds before igniting.
*Falsified if:* off-gas is not detectable before flaming by a usable margin.
"""


def main():
    print("selftest_fa")
    for f in ("inventory.py", "extract.py", "checks.py", "queue.py", "run_all.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)

    # ---- table parse, both header shapes, falsifier found by header name not position
    rows = list(E.parse_claim_tables(TABLE_LAST))
    check("falsifier-last table: X1 parsed, falsifier is the last column, claim the claim column",
          len(rows) == 2 and rows[0]["id"] == "X1" and "falls as load rises" in rows[0]["falsifier"] and "rises with load" in rows[0]["claim"])
    rows_m = list(E.parse_claim_tables(TABLE_MID))
    check("'falsified by' middle-column table: B1 parsed with the falsifier from the named column",
          len(rows_m) == 1 and rows_m[0]["id"] == "B1" and "physical two-option" in rows_m[0]["falsifier"])
    pr = list(E.parse_prose(PROSE))
    check("prose 'Falsified if:' parsed with the claim attached from the bold line above",
          len(pr) == 1 and "usable margin" in pr[0]["falsifier"] and pr[0]["claim"])

    # ---- records: empty falsifier skipped, NOT-FOUND emitted, ids stable
    import tempfile
    d = tempfile.mkdtemp()
    open(os.path.join(d, "t.md"), "w").write(TABLE_LAST + "\n" + TABLE_MID)
    recs, empty = E.records([d])
    check("the '—' falsifier cell (X2) is skipped as empty, counted not recorded", empty == 1 and all("X2" not in r["row_id"] for r in recs))
    check("records carry stable repo:path:line ids and a LOCATED attach status", recs and all(":" in r["id"] for r in recs) and recs[0]["attach_status"] == "LOCATED")
    recs2, _ = E.records([d])
    check("re-running on the unchanged tree emits the same ids (append-stable)", [r["id"] for r in recs] == [r["id"] for r in recs2])

    # ---- A1 both directions
    vague = {"id": "r:1", "repo": "r", "text": "the framework is internally coherent", "attach_status": "LOCATED", "attached_to": "c"}
    quantified = {"id": "r:2", "repo": "r", "text": "a run where the count exceeds 10", "attach_status": "LOCATED", "attached_to": "c"}
    check("A1 fires on a falsifier with no quantity, threshold, or observable outcome", C.a1(vague) is not None)
    check("A1 is silent on a falsifier stating a number and an observable", C.a1(quantified) is None)

    # ---- A2 both directions
    drift = {"id": "r:3", "repo": "r", "text": "a photobiont turnover predicted from temperature and precipitation", "attach_status": "LOCATED", "attached_to": "the market steers the aggregate incentive"}
    aligned = {"id": "r:4", "repo": "r", "text": "a temperature turnover not predicted from temperature", "attach_status": "LOCATED", "attached_to": "temperature turnover predicted from temperature and precipitation"}
    check("A2 fires when the falsifier's terms are absent from the claim", C.a2(drift) is not None)
    check("A2 is silent when the falsifier's terms are in the claim", C.a2(aligned) is None)
    check("A2 does not run on a NOT-FOUND record", C.a2(dict(drift, attach_status="NOT-FOUND")) is None)

    # ---- A3 null test (the load-bearing one): fires cross-repo, silent same-repo
    a = {"id": "repoA/x.md:1", "repo": "repoA", "text": "the drift ratio rises above 0.5", "attach_status": "LOCATED", "attached_to": "c"}
    b = {"id": "repoB/y.md:1", "repo": "repoB", "text": "the drift ratio falls below 0.2", "attach_status": "LOCATED", "attached_to": "c"}
    check("A3 fires on two records, same axis, different repos, conflicting cutoffs/directions", len(X.incompatibilities([a, b])) >= 1)
    check("A3 is silent when both records are in one repo (a scope-difference needs two contexts)",
          len(X.incompatibilities([a, dict(b, id="repoA/z.md:1", repo="repoA")])) == 0)
    check("A3 is silent when the two records carry the same cutoff and direction",
          len(X.incompatibilities([a, dict(b, id="repoB/y.md:1", repo="repoB", text="the drift ratio rises above 0.5")])) == 0)

    # ---- A4 both directions
    ref = {"id": "r:5", "repo": "r", "text": "a value that clears the null baseline", "attach_status": "LOCATED", "attached_to": "c"}
    noref = {"id": "r:6", "repo": "r", "text": "a run where the widget count falls", "attach_status": "LOCATED", "attached_to": "c"}
    check("A4 fires on an undeclared reference term (baseline / null)", C.a4(ref) is not None)
    check("A4 is silent with no reference term", C.a4(noref) is None)

    # ---- the corpus runs; queue entries are questions with status OPEN only
    crecs, cempty = E.records()
    ent = Q.entries(crecs, cempty)
    check("the corpus yields falsifier records and queue entries", len(crecs) > 50 and len(ent) > 20)
    check("every queue entry has status OPEN and a question, never a fix", all(e["status"] == "OPEN" and e["question"] and "fix" not in e["question"].lower() for e in ent))
    check("both LOCATED and NOT-FOUND appear in the corpus records", any(r["attach_status"] == "LOCATED" for r in crecs) and any(r["attach_status"] == "NOT-FOUND" for r in crecs))
    cov = Q.coverage()
    check("coverage reports scanned and skipped files, and the tool's own outputs are self-excluded from records",
          cov["scanned_md_py"] > 100 and not any("falsifier-audit/QUEUE.md" in r["path"] or "falsifier-audit/samples" in r["path"] for r in crecs))

    # ---- the tool's own framing screens clean (the queue BODY quotes corpus
    # falsifier text verbatim, which is data, not the tool's prose)
    inv = I.render()
    check("inventory render screens clean (authored framing)", not no_severity.hits(inv))
    q = Q.render()
    framing = "\n".join(l for l in q.splitlines() if not l.startswith("  falsifier:") and not l.startswith("  detail:"))
    check("the queue's authored framing (coverage, questions, notes) screens clean",
          not no_severity.hits(framing))
    check("screen fires on a planted word", bool(no_severity.hits(framing + "\nthis is wrong\n")))

    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "inventory.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(inv + "\n")
    with open(os.path.join(HERE, "samples", "queue_head.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(q.splitlines()[:40]) + "\n")
    Q.main(["--write"])
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
