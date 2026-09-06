# SPDX-License-Identifier: CC0-1.0
"""
A worked pass over the instrument on CONSTRUCTED data: the required contents
and the two structural absences, the claim table's refutation coverage, the
dE/dt vs dM/dt rate form, the RDL-5 survey decay, and the F6 upstream
pattern. No row is a measurement of any road, dock, or routing system;
nothing is a result. Screened through sheet-structure-scan/no_severity with
no exemption (the verdict constants keep the marker's severity vocabulary
inside underscored tokens, e.g. VENDOR_DEFECT, which the word-boundary screen
does not fire on).

    python3 routing-data-layer/demo_rdl.py            # print
    python3 routing-data-layer/demo_rdl.py --write    # write samples/
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import envelope as ev             # noqa: E402
import rate_form as rf            # noqa: E402
import upstream as up             # noqa: E402
import no_severity                # noqa: E402


def render():
    L = []
    L.append("ROUTING DATA LAYER -- CONSTRUCTED, NOT A RESULT")
    L.append("=" * 52)
    L.append("")
    L.append("required contents (R1-R10), by record state:")
    for r in ev.REQUIRED:
        L.append("  %-3s %-9s %s" % (r.rid, r.record_state, r.name))
    L.append("  never created (paying to CREATE, not to fund): %s"
             % ", ".join(ev.never_created()))

    L.append("")
    L.append("claim table (RDL-1..RDL-7) -- every claim carries a refutation:")
    L.append("  falsifiable: %d of %d"
             % (sum(1 for c in ev.CLAIMS if c.falsifiable()), len(ev.CLAIMS)))

    L.append("")
    L.append("Section 5 rate form (dE/dt vs dM/dt):")
    L.append("  dE outruns dM sustained  -> %s"
             % rf.rate_verdict([2.0] * 10, [1.0] * 10))
    L.append("  refresh keeps up         -> %s"
             % rf.rate_verdict([1.0] * 10, [2.0] * 10))
    L.append("  excess near half         -> %s"
             % rf.rate_verdict([2, 1, 2, 1, 2, 1], [1, 2, 1, 2, 1, 2]))

    L.append("")
    L.append("RDL-5 survey decay (5%/mo stale over a 12-mo season):")
    ot = rf.survey_decay([0.05] * 12, refresh_interval=0)
    st = rf.survey_decay([0.05] * 12, refresh_interval=3)
    L.append("  one-time survey: final accuracy %.2f, held=%s"
             % (ot["final_accuracy"], ot["held"]))
    L.append("  standing (refresh q3): final accuracy %.2f, held=%s  "
             "-> cost is standing, not capital"
             % (st["final_accuracy"], st["held"]))

    L.append("")
    L.append("F6 upstream pattern (two systems vs ground truth 10):")
    L.append("  systems 12 and 8 (both off, opposite)  -> %s  "
             "(closable by one vendor: %s)"
             % (up.upstream_verdict(10.0, 12.0, 8.0),
                up.single_vendor_fix_closes(up.upstream_verdict(10, 12, 8))))
    L.append("  systems 12 and 10 (one off)            -> %s  "
             "(closable by one vendor: %s)"
             % (up.upstream_verdict(10.0, 12.0, 10.0),
                up.single_vendor_fix_closes(up.upstream_verdict(10, 12, 10))))
    return "\n".join(L)


def main(argv):
    text = render()
    clean, h = no_severity.check(text)
    if not clean:
        sys.stderr.write("no_severity FAILED on the demo:\n")
        for lineno, word, line in h:
            sys.stderr.write("  line %d: %r in %r\n" % (lineno, word, line))
        return 1
    if "--write" in argv:
        out = os.path.join(HERE, "samples", "rdl_demo.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean)\n" % out)
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
