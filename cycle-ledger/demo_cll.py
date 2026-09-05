# SPDX-License-Identifier: CC0-1.0
"""
A worked pass over both deliverables on their shipped example inputs:

  Deliverable 1 -- the SEED ledger (marker's corridor, AHEAD == 0, the claim's
  support absent here) and, for the NULL, a CONSTRUCTED cycle carrying a
  DECISION-bound element (AHEAD > 0, "the claim holds here").

  Deliverable 2 -- the CONSTRUCTED structural series (STRUCTURAL) and the
  CONSTRUCTED kept-up series (MATURITY_GAP).

No row is a measurement of any operation, county, road, or routing system;
nothing is a result. The emitted text is screened through
sheet-structure-scan/no_severity.

    python3 cycle-ledger/demo_cll.py            # print
    python3 cycle-ledger/demo_cll.py --write    # write samples/
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import cycle_ledger as cl        # noqa: E402
import rate_gap as rg            # noqa: E402
import no_severity               # noqa: E402


def render():
    L = []
    L.append("CYCLE LEDGER + RATE GAP -- CONSTRUCTED, NOT A RESULT")
    L.append("=" * 52)
    L.append("")
    L.append("Deliverable 1: SEED ledger (marker's corridor)")
    L.append("-" * 46)
    L.append(cl.render(cl.SEED))
    L.append("")
    L.append("NULL check -- a cycle with a DECISION-bound element:")
    decision_cycle = list(cl.SEED) + [
        cl.Element("route_choice", "bound by choosing, not executing",
                   cl.DECISION, decision_latency_binds=True)]
    c = cl.classify(decision_cycle)
    L.append("   AHEAD = %d  ->  claim_holds_here = %s"
             % (c["ahead"], c["claim_holds_here"]))
    L.append("")
    L.append("Deliverable 2: rate gap, two CONSTRUCTED seasons")
    L.append("-" * 46)
    ev, up = rg._demo_structural()
    L.append(rg.render(ev, up, label="CONSTRUCTED (structural)"))
    L.append("")
    ev, up = rg._demo_maturity()
    g = rg.gap_verdict(ev, up)
    L.append("kept-up season -> verdict %s" % g["verdict"])
    L.append("   (rate=%s, unrecorded=%d)"
             % (g["rate_verdict"], g["unrecorded_total"]))
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
        out = os.path.join(HERE, "samples", "cll_demo.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean)\n" % out)
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean)\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
