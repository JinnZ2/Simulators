#!/usr/bin/env python3
"""M2 instrument_registry -- one record per methodology change to BLS CES.

    record: effective_date, change_name, affected_sectors,
            direction_if_known, retroactively_applied (bool),
            recalculated_span

The SEED set below is the work order's minimum seed, transcribed verbatim
from the delivered text. It is **carried, not verified**: the BLS CES
history page (the source of record) is egress-blocked here
(www.bls.gov answered no on CONNECT, 2026-09-05T14:02Z), so no entry is
confirmed against the primary source and none is added from memory beyond
what the work order delivered. Every entry is marked `verified=False`.

Also registered as a RECURRING change: seasonal factors are re-estimated on
a rolling 5-year window at every benchmark, so history moves at every
benchmark -- not a one-time event. Stdlib only, parses under 3.9.
"""

import sys
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Change:
    effective_date: str            # ISO or year
    change_name: str
    affected_sectors: List[str]
    direction_if_known: Optional[str]      # "up" / "down" / None
    retroactively_applied: bool
    recalculated_span: Optional[str]       # the span re-computed, if any
    recurring: bool = False
    verified: bool = False                 # spec fetched from BLS? no (egress)
    note: str = ""


# ---- the work order's minimum seed set, verbatim (carried, not verified) ---
SEED: List[Change] = [
    Change("2003", "birth-death model enters national estimates",
           ["all"], None, False, None),
    Change("2011", "birth-death updated quarterly, not annually",
           ["all"], None, False, None),
    Change("2014", "annual -> quarterly sample rotation",
           ["all"], None, False, None),
    Change("2015", "X-12-ARIMA -> X-13ARIMA-SEATS",
           ["all"], None, False, None),
    Change("2012", "NAICS 2007 -> NAICS 2012",
           ["all"], None, True, None,
           note="boundary crossing: NAICS reclassification"),
    Change("2018", "NAICS 2012 -> NAICS 2017",
           ["all"], None, True, None,
           note="boundary crossing: NAICS reclassification"),
    Change("2026-01",
           "ARIMA component modified to incorporate current sample info",
           ["all"], "down", True,
           "Apr-Oct 2025 post-benchmark span + Nov-Dec 2025",
           note="net birth-death forecasts for that 7-month span came in "
                "185,000 lower than the forecasts used in monthly estimation"),
    Change("recurring", "seasonal factors re-estimated on a rolling 5-year "
           "window at every benchmark",
           ["all"], None, True, "rolling 5-year window",
           recurring=True,
           note="history moves at every benchmark; a recurring change, "
                "not one-time"),
]


class InstrumentRegistry:
    def __init__(self, changes=None):
        self.changes = list(changes if changes is not None else SEED)

    def between(self, date_a, date_b):
        """Changes effective within [date_a, date_b] (string compare on the
        ISO-ish dates), plus every recurring change (which fires at each
        benchmark and so is always in scope)."""
        lo, hi = sorted((date_a, date_b))
        out = []
        for c in self.changes:
            if c.recurring:
                out.append(c)
            elif lo <= c.effective_date <= hi:
                out.append(c)
        return out

    def boundary_changes(self, date_a, date_b):
        """Changes in the span that are NAICS reclassifications -- the ones
        that produce boundary crossings in M3."""
        return [c for c in self.between(date_a, date_b)
                if "NAICS" in c.change_name]

    def unverified(self):
        return [c for c in self.changes if not c.verified]


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("instrument_registry has no selftest; run selftest.py", file=sys.stderr)
        sys.exit(2)
    print("M2 instrument_registry -- seed set carried (not verified; BLS "
          "egress-blocked). Import InstrumentRegistry. Run selftest.py.",
          file=sys.stderr)
    sys.exit(2)
