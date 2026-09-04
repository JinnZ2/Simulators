#!/usr/bin/env python3
"""E7's cross-substrate term table, as a schema with the one worked cell
the pack supplies and every other cell UNRECORDED. Nothing is filled
from memory. A non-UNRECORDED cell needs a basis naming the pack items
it rests on; the discriminator field takes a number or None.

    python3 term_table.py
Refuses --selftest (checks live in selftest_evidence.py).
"""

import sys

TERMS = [
    "cost asymmetry",
    "whether the aggregate steers (incentive direction)",
    "what sits inside vs outside the accounting boundary",
    "whether a legitimate other is representable at all",
    "does the accounting stance PRESERVE OR DESTROY the measurement it depends on",
]
SUBSTRATES = ["foraging/predation ecology", "multiagent AI harnesses", "human societies and mutual aid",
              "morality/ethics claims", "nation-state sovereignty"]
STATES = ("MEASURED", "MISSING", "SCOPE_DIFFERENT", "UNRECORDED")

# (term index, substrate index) -> cell. The two cells are the pack's own
# worked example; the second rests on items the pack marks unverified.
TABLE = {
    (0, 0): {"state": "MEASURED", "basis": "E1.1-E1.3 (profitability = E / handling time; cost terms)",
             "basis_status": "UNVERIFIED-FULLTEXT", "prediction_in_substrate": None},
    (0, 1): {"state": "MISSING", "basis": "E2.1-E2.3 (no cost term reported in the harness account)",
             "basis_status": "UNVERIFIED-FULLTEXT", "prediction_in_substrate": None},
}


def validate(table=TABLE):
    findings = []
    for key, c in table.items():
        if c["state"] not in STATES:
            findings.append("%s: state %r outside %s" % (key, c["state"], STATES))
        if c["state"] != "UNRECORDED" and not c.get("basis"):
            findings.append("%s: a filled cell needs a basis" % (key,))
        p = c.get("prediction_in_substrate")
        if p is not None and not isinstance(p, (int, float)):
            findings.append("%s: prediction is a number or None" % (key,))
    return findings


def cell(t, s, table=TABLE):
    return table.get((t, s), {"state": "UNRECORDED", "basis": None, "prediction_in_substrate": None})


def experiments_sitting_there(table=TABLE):
    """A term MEASURED in one substrate and MISSING in another."""
    out = []
    for t in range(len(TERMS)):
        measured = [s for s in range(len(SUBSTRATES)) if cell(t, s, table)["state"] == "MEASURED"]
        missing = [s for s in range(len(SUBSTRATES)) if cell(t, s, table)["state"] == "MISSING"]
        for m in measured:
            for x in missing:
                out.append((TERMS[t], SUBSTRATES[m], SUBSTRATES[x]))
    return out


def summary(table=TABLE):
    n = len(TERMS) * len(SUBSTRATES)
    filled = sum(1 for t in range(len(TERMS)) for s in range(len(SUBSTRATES)) if cell(t, s, table)["state"] != "UNRECORDED")
    preds = sum(1 for c in table.values() if c.get("prediction_in_substrate") is not None)
    return {"cells": n, "filled": filled, "predictions": preds, "experiments": experiments_sitting_there(table),
            "findings": validate(table)}


def render(table=TABLE):
    s = summary(table)
    L = ["E7 cross-substrate term table: %d cells, %d filled, %d quantitative predictions" % (s["cells"], s["filled"], s["predictions"])]
    L.append("  %-28s " % "" + " ".join("%-15s" % sub[:15] for sub in SUBSTRATES))
    for t, term in enumerate(TERMS):
        L.append("  %-28s " % term[:28] + " ".join("%-15s" % cell(t, x, table)["state"] for x in range(len(SUBSTRATES))))
    for term, m, x in s["experiments"]:
        L.append("experiment sitting there: %r MEASURED in %s, MISSING in %s" % (term, m, x))
    L.append("discriminator: 0 of %d filled cells carry a quantitative prediction in a second substrate; "
             "on the pack's own rule that is the state before a shared structure is shown" % s["filled"])
    if s["findings"]:
        L.append("schema findings: " + "; ".join(s["findings"]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("term_table has no selftest; run selftest_evidence.py", file=sys.stderr)
        sys.exit(2)
    print(render())
