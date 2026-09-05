#!/usr/bin/env python3
"""report.py -- §6: emits MERGE_REPORT.md. No ranking of registrars, no
"ours is better" framing (§7). The report states the egress fact once,
lists every real registrar's UNVERIFIED / NO-MERGE outcome with its
breaks_at, and shows the residual machinery firing on the declared test
doubles -- COERCED and ADDED reported alongside DROPPED, never only
DROPPED. Stdlib only, parses under 3.9.

    python3 merge-path/report.py            # print MERGE_REPORT.md
    python3 merge-path/report.py --write     # (re)write MERGE_REPORT.md
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import registrars as RG            # noqa: E402
import residual as R              # noqa: E402
import run_all as RA              # noqa: E402


def merge_report():
    L = ["# MERGE_REPORT — claim registrars <-> falsifier format", "",
         "Emitted by `report.py`. A transform survey, not a new format (§0). No",
         "ranking; every registrar is reported on its own terms.", "",
         "## Egress status (load-bearing)", "",
         "The work order's §1 requires fetching each registrar's own specification",
         "before mapping. In this environment the egress proxy is an allowlist and",
         "every registrar spec host answered **403 to CONNECT** (probed",
         "2026-09-05T03:30Z). So **no spec was fetched**, every real registrar below",
         "is **UNVERIFIED**, and per §7 every statement about it inherits UNVERIFIED.",
         "What is verified is the machinery, exercised on declared test doubles.", "",
         "## Real registrars — UNVERIFIED, NO-MERGE (§0: a valid outcome)", "",
         "| registrar | verified | verdict | breaks_at | spec (identifier, unfetched) |",
         "|---|---|---|---|---|"]
    for row in RA.real_registrar_report():
        L.append("| `%s` | %s | %s | %s | %s |"
                 % (row["registrar"], row["verified"], row["verdict"],
                    "spec unfetched (egress 403)", row["spec_url"]))
    L.append("")
    L.append("Every NO-MERGE carries a `breaks_at` (§0, S5): the correspondence cannot")
    L.append("be established because the spec was not fetched. A NO-MERGE with a stated")
    L.append("breaks_at is worth more than a forced mapping — filling these in requires a")
    L.append("network fetch by someone whose egress reaches the spec hosts.")
    L.append("")
    L.append("## Machinery — the residual classes, on declared test doubles")
    L.append("")
    L.append("No row below is a claim about any real registrar; each mock is built to")
    L.append("exercise one residual class so the classifier is shown to fire on it.")
    L.append("")
    L.append("| fixture | test double | residual classes |")
    L.append("|---|---|---|")
    for row in RA.mock_round_trips():
        cls = row["classes"]
        active = ", ".join("%s=%d" % (c, cls[c]) for c in R.RESIDUAL_CLASSES if cls[c]) or "lossless"
        L.append("| %s… | `%s` | %s |" % (row["fixture"][:34], row["registrar"], active))
    L.append("")
    L.append("`COERCED` and `ADDED` are the silent-wrongness classes and are counted")
    L.append("alongside `DROPPED` (visible as a zero when zero); a report of only")
    L.append("`DROPPED` counts is not finished (§3).")
    return "\n".join(L)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("report has no selftest; run selftest.py", file=sys.stderr)
        return 2
    out = merge_report()
    if "--write" in argv:
        with open(os.path.join(HERE, "MERGE_REPORT.md"), "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
