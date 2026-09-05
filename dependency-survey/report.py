#!/usr/bin/env python3
"""report.py -- the four things the instrument emits: the 5x5 table, the
full cell records (one block per non-UNKNOWN cell), the gap list, and the
UNKNOWN count stated explicitly with the cells listed. Absence
(MISSING) and not-yet-looked (UNKNOWN) are kept apart. Stdlib only.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import survey as S  # noqa: E402
import gaps as G  # noqa: E402


def cell_records(g):
    L = ["cell records (non-UNKNOWN cells; quantity, units, source -- no interpretation)"]
    any_ = False
    for t, _ in S.TERMS:
        for s, _ in S.SUBSTRATES:
            c = g[(t, s)]
            if c["status"] == "UNKNOWN":
                continue
            any_ = True
            L.append("%s x %s   status %s%s%s" % (
                t, s, c["status"], "" if c["valid"] else "  (inadmissible: %s)" % c["invalid_reason"],
                "  PROVISIONAL" if c["provisional"] else ""))
            if c["measured_as"]:
                L.append("  measured_as: %s" % c["measured_as"])
            for f in S.TRANSFORM_FIELDS:
                if c.get(f):
                    L.append("  %-11s %s" % (f + ":", c[f]))
            if c["scope_note"]:
                L.append("  scope_note:  %s" % c["scope_note"])
            if c["source"]:
                L.append("  source:      %s" % c["source"])
    if not any_:
        L.append("  (none coded)")
    return "\n".join(L)


def unknown_block(g):
    unk = [(t, s) for t, _ in S.TERMS for s, _ in S.SUBSTRATES if g[(t, s)]["status"] == "UNKNOWN"]
    inc = S.scope_incomplete_cells(g)
    typ = S.measured_type_only_cells(g)
    L = ["UNKNOWN cells: %d of 25 (not-yet-looked, NOT an absence of the term)" % len(unk)]
    for t, s in unk:
        L.append("  %s x %s" % (t, s))
    # ADDENDUM_01 sec.3: a separate line from the UNKNOWN count.
    L.append("SCOPE-DIFFERENT cells lacking a complete transform: %d "
             "(coded SCOPE-DIFFERENT, downgraded to UNKNOWN, counted apart from the %d never-coded UNKNOWN cells)"
             % (len(inc), len(unk)))
    for t, s in inc:
        L.append("  %s x %s -- %s" % (t, s, g[(t, s)]["invalid_reason"]))
    # ADDENDUM_02: MEASURED cells whose units field names a type, not a
    # scale. Emitted on its own line, visible as a zero when it is zero.
    L.append("MEASURED cells whose units field names a type rather than a scale: %d "
             "(ADDENDUM 02; coded MEASURED, downgraded to MISSING, counted apart from cells with no units at all)"
             % len(typ))
    for t, s in typ:
        L.append("  %s x %s -- %s" % (t, s, g[(t, s)]["invalid_reason"]))
    return "\n".join(L)


def full_report():
    g = S.grid()
    parts = [S.render(g), "", cell_records(g), "", G.render(g), "", unknown_block(g)]
    return "\n".join(parts)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("report has no selftest; run selftest_ds.py", file=sys.stderr)
        sys.exit(2)
    print(full_report())
