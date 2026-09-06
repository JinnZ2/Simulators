#!/usr/bin/env python3
"""Checks for queue_check.py against the delivered UPGRADE_QUEUE.md. Known
answers, both directions. Verifies the parse, the NOT-ADOPTED invariant,
the cross-reference resolution, and that the checker adopts nothing.

    python3 upgrade-queue/selftest_uq.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import queue_check as Q  # noqa: E402
import no_severity       # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_uq")
    rc = subprocess.run([sys.executable, os.path.join(HERE, "queue_check.py"), "--selftest"],
                        capture_output=True).returncode
    check("queue_check refuses --selftest with rc 2", rc == 2)

    p = Q.parse_queue()
    # ---- structure: 13 entries, tiers 4/5/4, matching the queue's declaration
    check("13 entries parse (U-01..U-13)", len(p["entries"]) == 13
          and set(p["entries"]) == {"U-%02d" % i for i in range(1, 14)})
    tc = Q.tier_counts(p)
    check("tier counts are FORCED=4, CANDIDATE=5, SPECULATIVE=4",
          (tc[1], tc[2], tc[3]) == (4, 5, 4) and Q.EXPECTED_TIER_COUNTS == {1: 4, 2: 5, 3: 4})
    check("tiers carry their declared names",
          p["entries"]["U-01"]["tier_name"] == "FORCED"
          and p["entries"]["U-05"]["tier_name"] == "CANDIDATE"
          and p["entries"]["U-10"]["tier_name"] == "SPECULATIVE")

    # ---- NOT-ADOPTED invariant, both the global line and the per-entry status
    check("the global 'status of every entry: NOT ADOPTED' line is present", p["global_not_adopted"])
    check("every Tier-1/2 entry with a status line says NOT ADOPTED (never ADOPTED)",
          p["status_lines"] and all(p["status_lines"].values()))
    # the checker adopts nothing: its report emits no ADOPTED verdict token
    # (only "NOT ADOPTED"/"NOT-ADOPTED", and lowercase prose "is adopted").
    import re as _re
    rep0 = Q.report().replace("NOT ADOPTED", "").replace("NOT-ADOPTED", "")
    check("the checker adopts nothing: its report emits no ADOPTED verdict token",
          not _re.search(r"\bADOPTED\b", rep0))

    # ---- cross-reference resolution: declared in-repo paths must exist
    refs = Q.resolve_refs()
    missing = [(eid, r["path"]) for eid, rows in refs.items() for r in rows if r["state"] == "MISSING"]
    check("every declared in-repo cross-reference path exists (no MISSING)", missing == [])
    inrepo_total = sum(1 for rows in refs.values() for r in rows if r["state"] == "IN-REPO")
    ext_total = sum(1 for rows in refs.values() for r in rows if r["state"] == "EXTERNAL")
    check("both IN-REPO and EXTERNAL references are present (the split is real)",
          inrepo_total > 0 and ext_total > 0)
    # null test: a constructed bad path resolves MISSING (not silently IN-REPO)
    saved = Q.CROSS_REFS.get("U-04")
    Q.CROSS_REFS["U-04"] = [("bogus", "dependency-survey/does-not-exist.md")]
    bad = Q.resolve_refs()["U-04"]
    Q.CROSS_REFS["U-04"] = saved
    check("a non-existent declared in-repo path resolves MISSING (not IN-REPO)",
          any(r["state"] == "MISSING" for r in bad))

    # ---- adopt-rule classification: exactly the entries the queue flags as a
    # rewrite are CHANGES; the rest ADD a field or are UNKNOWN (speculative)
    check("U-09 (the queue's own 'most likely a format rewrite') is the CHANGES entry",
          Q.KIND["U-09"] == "CHANGES"
          and [e for e in Q.KIND if Q.KIND[e] == "CHANGES"] == ["U-09"])
    check("Tier 3 entries are kind UNKNOWN (speculative, placement stated Unknown)",
          all(Q.KIND["U-%02d" % i] == "UNKNOWN" for i in (10, 11, 12, 13)))

    # ---- adopt-test runnability: most are BLOCKED here (external corpus / unlanded)
    runnable = [e for e in Q.ADOPT_TEST if Q.ADOPT_TEST[e] == "RUNNABLE_HERE"]
    blocked = [e for e in Q.ADOPT_TEST if Q.ADOPT_TEST[e].startswith("BLOCKED")]
    check("at least one adopt-test is BLOCKED by an external/unlanded dependency", len(blocked) >= 1)
    check("U-07's adopt-test is BLOCKED_UNLANDED (the FSRI report has not landed)",
          Q.ADOPT_TEST["U-07"] == "BLOCKED_UNLANDED")
    check("U-04 needs no adopt-test (the nesting result is the demonstration, in-repo)",
          Q.ADOPT_TEST["U-04"] == "NONE_NEEDED")

    # ---- the NOT-ON-THIS-LIST exclusions are recorded (the disciplines the repo already holds)
    check("the three NOT-ON-THIS-LIST exclusions are parsed", len(p["exclusions"]) == 3)

    # ---- the report screens clean
    out = Q.report()
    check("report render screens clean", not no_severity.hits(out))
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))

    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "queue_check.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
