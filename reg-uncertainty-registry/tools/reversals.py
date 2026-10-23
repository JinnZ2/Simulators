#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
reversals.py -- REVERSAL objects (WO-REG-1b) as a table by initiator, the
median time to reversal by direction, and an exact Mann-Whitney test of
whether restrictive -> permissive reversals come faster than permissive ->
restrictive ones.

    direction   restrictive (hold | decline) -> permissive (go_ahead | warn),
                or the reverse; C03 (go_ahead -> vacated, product left on the
                market) is neither and is listed under 'other'
    time        time_to_reversal_years as stored; date convention: a
                year-only date is read as July 1, a year-month date as the
                1st [CHOICE] (build.years_between)
    D01         one reversal measured from two anchors (REV-D01-2016, the
                2016 denial D03; REV-D01-1970, the original placement); each
                reading counts one of them and says which
    harm        harm count at reversal: the value with its basis, or
                NOT_FOUND -- never zero

The test is over 4 + 4 reversals drawn from a sample selected on permissive
anchors (NCR-N21): an exact p on a selected list is a property of the list.

Library + CLI; checks() is called by validate.py. Stdlib only.
"""

import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402
import stats  # noqa: E402
import build  # noqa: E402


def table(reg):
    rows = []
    for r in sorted(reg.of("REVERSAL"), key=lambda x: (x["initiator_type"], x["id"])):
        h = r["harm_at_reversal"]
        rows.append("%-14s %-24s %-8s->%-8s %6.2fy  %-21s harm %s%s" % (
            r["id"], r["initiator_type"], r["from_direction"], r["to_direction"],
            r["time_to_reversal_years"], r["mechanism"],
            h["state"] if h["value"] is None else h["value"][:40],
            ("  [alias of %s]" % r["alias_of"]) if r.get("alias_of") else ""))
    return rows


def render(reg):
    out = ["== REVERSAL objects by initiator type"] + table(reg)
    for anchor in ("2016", "1970"):
        rv = stats.reversals(reg.objects, anchor)
        out.append("== reading with D01 measured from %s" % anchor)
        for g in ("restrictive_to_permissive", "permissive_to_restrictive"):
            ts = [t for _, t, _ in rv["groups"][g]]
            out.append("%-26s n=%d  median %.2fy  %s" % (
                g, len(ts), statistics.median(ts), ", ".join("%.2f" % t for t in sorted(ts))))
        mw = rv["mann_whitney"]
        out.append("exact Mann-Whitney U=%.1f (pairs where restrictive->permissive took longer), "
                   "p two-sided = %.4f over %d arrangements" % (mw["U"], mw["p_two_sided"],
                                                                 mw["enumerated"]))
    return out


def checks(reg):
    errs, n = [], 0
    for r in reg.of("REVERSAL"):
        n += 1
        t = build.years_between(r["date_from"], r["date_to"])
        if t != r["time_to_reversal_years"]:
            errs.append("%s: stored %s, dates give %s" % (r["id"], r["time_to_reversal_years"], t))
        if t <= 0:
            errs.append("%s: reversal precedes its decision" % r["id"])
        if r["harm_at_reversal"]["value"] is None and r["harm_at_reversal"]["state"] != "NOT_FOUND":
            errs.append("%s: no harm count but state %s" % (r["id"], r["harm_at_reversal"]["state"]))
    # one reversal, two anchors: never both in one reading
    for anchor in ("2016", "1970"):
        n += 1
        ids = [i for g in stats.reversals(reg.objects, anchor)["groups"].values() for i, _, _ in g]
        if "REV-D01-2016" in ids and "REV-D01-1970" in ids:
            errs.append("both D01 anchors counted in one reading")
    # known answers for the exact test (definitions, not the implementation)
    for x, y, u, p in (([1, 2], [3, 4], 0.0, 1.0 / 3), ([1], [2], 0.0, 1.0),
                       ([5, 6, 7], [1, 2, 3], 9.0, 0.1), ([1, 2], [1, 2], 2.0, 1.0)):
        n += 1
        mw = stats.mann_whitney_exact(x, y)
        if abs(mw["U"] - u) > 1e-9 or abs(mw["p_two_sided"] - p) > 1e-9:
            errs.append("mann_whitney_exact(%s, %s) = U %s p %s, want U %s p %s"
                        % (x, y, mw["U"], mw["p_two_sided"], u, p))
    return n, errs


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("reversals.py: checks run in tools/validate.py --selftest\n")
        return 2
    print("\n".join(render(reglib.Registry())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
