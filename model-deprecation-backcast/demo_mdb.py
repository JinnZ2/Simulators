# SPDX-License-Identifier: CC0-1.0
"""
A worked pass over the instrument on CONSTRUCTED data: the seven columns and
their nulls, the C6 fad-axis lag both directions, the guardrail-clock
contamination, and the C3 accepted-side censoring. No row is a measurement of
any model, vendor, or population; nothing is a result. Screened through
sheet-structure-scan/no_severity.

    python3 model-deprecation-backcast/demo_mdb.py            # print
    python3 model-deprecation-backcast/demo_mdb.py --write    # write samples/
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import instrument as ins           # noqa: E402
import null_check as nc            # noqa: E402
import guardrail_clock as gc       # noqa: E402
import no_severity                 # noqa: E402


def render():
    L = []
    L.append("MODEL DEPRECATION BACKCAST INSTRUMENT -- CONSTRUCTED, NOT A RESULT")
    L.append("=" * 66)
    L.append("")
    L.append("seven columns; each carries a NULL -- the condition under which "
             "it measures nothing:")
    for c in ins.COLUMNS:
        tail = ("  (collapses into %s)" % c.collapses_into
                if c.collapses_into else "")
        L.append("  %s %s" % (c.cid, c.name))
        L.append("      null: %s%s" % (c.null, tail))
    L.append("")
    L.append("separate layer -- guardrail clock (%s), on %s"
             % (ins.GUARDRAIL_CLOCK.clock, ins.GUARDRAIL_CLOCK.columns_clock))
    L.append("open node: held, un-named, un-graded (per instruction)")

    x = gc._discourse_series(72)
    lags = list(range(0, 31))
    inband = [x[t - 20] if t - 20 >= 0 else 0.0 for t in range(72)]
    outband = [x[t - 8] if t - 8 >= 0 else 0.0 for t in range(72)]
    L.append("")
    L.append("C6 fad-axis lag (discourse vs discards, argmax cross-corr):")
    L.append("   discards lagged 20 mo    -> %s" % nc.c6_fad_driving(x, inband, lags))
    L.append("   discards lagged 8 mo     -> %s" % nc.c6_fad_driving(x, outband, lags))
    L.append("   uniform discards         -> %s (the null)"
             % nc.c6_fad_driving(x, [1.0] * 72, lags))

    demo = gc.contamination_demo()
    L.append("")
    L.append("guardrail-clock contamination of C6:")
    L.append("   separated (discards only) -> lag %s, %s"
             % (demo["separated_lag"], demo["separated_verdict"]))
    L.append("   pooled with guardrail     -> lag %s, %s  (misread to the "
             "news-time lag)" % (demo["contaminated_lag"],
                                 demo["contaminated_verdict"]))

    exits = ([("complainer", True)] * 2 + [("complainer", False)] * 1 +
             [("jumper", False)] * 4 + [("paid_then_lapsed", True)] * 3)
    c3 = nc.c3_censoring(exits)
    L.append("")
    L.append("C3 accepted-side censoring (three exit forms, one leaves a record):")
    L.append("   %d discard-affected, %d recorded (fraction %.2f); the other "
             "%d are censored, not absent"
             % (c3["total_affected"], c3["recorded"], c3["recorded_fraction"],
                c3["censored"]))
    L.append("   recorded signal carries a paying-tier filter: %.2f"
             % c3["paying_tier_fraction_of_recorded"])

    L.append("")
    L.append("stated up front (carried, not verified): %s -- excluded by %s"
             % (ins.SAMPLING_ABSENCE.quantity, ins.SAMPLING_ABSENCE.excluded_by))
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
        out = os.path.join(HERE, "samples", "mdb_demo.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean)\n" % out)
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
