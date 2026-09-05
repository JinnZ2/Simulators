#!/usr/bin/env python3
"""gaps.py -- the payoff. A gap is a term MEASURED (validly, with units)
in one substrate and MISSING in another. Each gap carries a transfer
question stated in the target substrate's own units; a gap whose
transfer cannot be so stated is flagged NO-TRANSFER, which is itself a
result on the projected-frame side of the discriminator.

The instrument does not invent the transfer answer -- that is a coding
task in CELLS.md (`transfer:` on the target cell, `no_transfer: yes` if
it cannot be stated). Absent both, the gap emits the open transfer
question, which is the research queue. Stdlib only.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import survey as S  # noqa: E402

SUB = dict(S.SUBSTRATES)
TRM = dict(S.TERMS)


def gaps(g=None):
    """One gap per (term, measured-substrate, missing-substrate) triple
    where the term is validly MEASURED in one and MISSING in the other."""
    g = g if g is not None else S.grid()
    out = []
    for t, _ in S.TERMS:
        measured = [s for s, _ in S.SUBSTRATES if S.is_valid_measured(g[(t, s)])]
        missing = [s for s, _ in S.SUBSTRATES if g[(t, s)]["effective_status"] == "MISSING"]
        for ms in measured:
            for xs in missing:
                mcell, xcell = g[(t, ms)], g[(t, xs)]
                # a transfer answer / no-transfer flag is coded on the MISSING
                # (target) cell; absent, the transfer question stays open.
                transfer = xcell.get("transfer", "")
                no_transfer = xcell.get("no_transfer", False)
                if no_transfer:
                    state = "NO-TRANSFER"
                elif transfer:
                    state = "TRANSFER-STATED"
                else:
                    state = "OPEN"
                out.append({
                    "term": t, "term_name": TRM[t],
                    "measured_in": ms, "measured_in_name": SUB[ms], "measured_as": mcell["measured_as"],
                    "missing_in": xs, "missing_in_name": SUB[xs],
                    "provisional": mcell.get("provisional") or xcell.get("provisional"),
                    "transfer_question": "what quantity in %s (%s) would be the analogue of '%s', in %s's own units?"
                    % (xs, SUB[xs], mcell["measured_as"], xs),
                    "transfer_answer": transfer, "state": state})
    return out


def render(g=None):
    gl = gaps(g)
    L = ["gap list -- terms MEASURED in one substrate, MISSING in another (the payoff)"]
    if not gl:
        L.append("  (none: no term is both validly MEASURED and MISSING across the coded cells)")
    for i, gp in enumerate(gl, 1):
        L.append("GAP %d  [%s]%s" % (i, gp["state"], "  PROVISIONAL" if gp["provisional"] else ""))
        L.append("  term            %s -- %s" % (gp["term"], gp["term_name"]))
        L.append("  measured in     %s (%s): %s" % (gp["measured_in"], gp["measured_in_name"], gp["measured_as"]))
        L.append("  missing in      %s (%s)" % (gp["missing_in"], gp["missing_in_name"]))
        L.append("  transfer Q      %s" % gp["transfer_question"])
        if gp["transfer_answer"]:
            L.append("  transfer answer %s" % gp["transfer_answer"])
        elif gp["state"] == "NO-TRANSFER":
            L.append("  -> NO-TRANSFER: the analogue cannot be stated in the target's own units; evidence on the projected-frame side")
        else:
            L.append("  -> OPEN: no transfer stated; this is the research question, not yet an experiment")
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("gaps has no selftest; run selftest_ds.py", file=sys.stderr)
        sys.exit(2)
    print(render())
