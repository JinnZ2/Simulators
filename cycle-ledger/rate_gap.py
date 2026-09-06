# SPDX-License-Identifier: CC0-1.0
"""
DELIVERABLE 2 -- rate_gap.py.

Tests the structural-vs-maturity distinction (marker Section 5) on a data
layer. Input is two dated lists for ONE jurisdiction over ONE construction
season:

  environment_events -- closures, reopenings, structure removals, seasonal
                        weight-restriction changes, repaints, resurfacings
  record_updates     -- when each of those appeared in a routing data source
                        (matched to its event by event_id)

Output:

  dE/dt      environment state-change rate (events per window)
  dM/dt      achieved record refresh rate  (updates per window)
  lag distribution, per event class (recorded events only)
  unrecorded set -- events that never appeared in the record at all

Readout (the marker's Section 5):

  dE/dt > dM/dt SUSTAINED, with a NONZERO unrecorded set
    -> STRUCTURAL. Not a maturity gap. A faster refresh does not close it.
  dM/dt >= dE/dt with the unrecorded set EMPTY
    -> MATURITY_GAP. Closes with funding.
  anything else -> UNDETERMINED, with the failing condition named.

The two inputs are kept visible: the rate verdict (from the paired series)
and the unrecorded count are reported side by side and never collapsed into
one number. An unrecorded event has lag UNRECORDED, never a large lag -- an
absent record is a different state than a slow one.

The rate machinery (`sustained_excess`, `rate_verdict`) is IMPORTED from
routing-data-layer/rate_form.py, not copied -- the verdict this instrument
returns is the same object that folder registered and tested.

Nothing here is a result: no county's events or updates are measured (the DOT
feeds are egress-blocked); the example series is CONSTRUCTED and marked so.
The marker's cheapest test -- both rates for one county over one season -- is
named and not run here.

Stdlib only. Parses under Python 3.9. ASCII only. Output <= 60 columns. CC0.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import date
from statistics import median
from typing import Dict, List, Optional

# import, do not copy: the rate verdict is routing-data-layer's object.
_HERE = os.path.dirname(os.path.abspath(__file__))
_RDL = os.path.join(os.path.dirname(_HERE), "routing-data-layer")
if _RDL not in sys.path:
    sys.path.insert(0, _RDL)
import rate_form  # noqa: E402
from rate_form import (  # noqa: E402
    STRUCTURAL, MATURITY_GAP, UNDETERMINED, sustained_excess, rate_verdict,
)

# closed set of event classes named by the work order.
CLOSURE = "CLOSURE"
REOPENING = "REOPENING"
STRUCTURE_REMOVAL = "STRUCTURE_REMOVAL"
WEIGHT_RESTRICTION = "WEIGHT_RESTRICTION"
REPAINT = "REPAINT"
RESURFACING = "RESURFACING"
EVENT_CLASSES = (CLOSURE, REOPENING, STRUCTURE_REMOVAL, WEIGHT_RESTRICTION,
                 REPAINT, RESURFACING)

# distinct non-numeric lag states (absent-vs-known-negative kept apart):
UNRECORDED = "UNRECORDED"        # no record update for this event, ever
NO_RECORDED = "NO_RECORDED"      # an event class with zero recorded events

# [CHOICE 1] window size in days for binning the season into a rate series.
WINDOW_DAYS = 7


class BadEvent(Exception):
    pass


@dataclass
class EnvEvent:
    event_id: str
    event_class: str
    day: str            # ISO 'YYYY-MM-DD'


@dataclass
class RecordUpdate:
    event_id: str       # which environment event this records
    day: str            # ISO 'YYYY-MM-DD'


def _d(iso: str) -> date:
    return date.fromisoformat(iso)


def validate(events: List[EnvEvent], updates: List[RecordUpdate]) -> None:
    ids = set()
    for e in events:
        if e.event_class not in EVENT_CLASSES:
            raise BadEvent("%s: event_class must be one of %r; got %r"
                           % (e.event_id, EVENT_CLASSES, e.event_class))
        _d(e.day)
        if e.event_id in ids:
            raise BadEvent("duplicate event_id %r" % e.event_id)
        ids.add(e.event_id)
    for u in updates:
        _d(u.day)


# ---- rate series (dE/dt, dM/dt) -------------------------------------------

def _span(events, updates):
    days = [_d(e.day) for e in events] + [_d(u.day) for u in updates]
    if not days:
        return None, None
    return min(days), max(days)


def rate_series(events: List[EnvEvent], updates: List[RecordUpdate],
                window_days: int = WINDOW_DAYS):
    """Bin the season into fixed windows; count events per window (dE) and
    record updates per window (dM). Returns the two paired series plus the
    window count -- the input `sustained_excess`/`rate_verdict` reads."""
    lo, hi = _span(events, updates)
    if lo is None:
        return {"dE": [], "dM": [], "windows": 0, "window_days": window_days}
    total_days = (hi - lo).days + 1
    nwin = (total_days + window_days - 1) // window_days
    dE = [0] * nwin
    dM = [0] * nwin
    for e in events:
        b = (_d(e.day) - lo).days // window_days
        dE[b] += 1
    for u in updates:
        b = (_d(u.day) - lo).days // window_days
        dM[b] += 1
    return {"dE": dE, "dM": dM, "windows": nwin, "window_days": window_days}


# ---- lag distribution per event class -------------------------------------

def lag_distribution(events: List[EnvEvent], updates: List[RecordUpdate]):
    """Per event class, the lag (record day minus event day, days) for every
    recorded event. Unrecorded events do not enter a distribution -- they are
    counted in the unrecorded set instead. A record dated before its event is
    kept apart as `anomalous`, not folded into the lag."""
    # earliest record per event_id (a record can be revised; first appearance
    # is the refresh that matters).
    first: Dict[str, date] = {}
    for u in updates:
        d = _d(u.day)
        if u.event_id not in first or d < first[u.event_id]:
            first[u.event_id] = d
    per: Dict[str, List[int]] = {c: [] for c in EVENT_CLASSES}
    anomalous: Dict[str, int] = {c: 0 for c in EVENT_CLASSES}
    for e in events:
        if e.event_id not in first:
            continue
        lag = (first[e.event_id] - _d(e.day)).days
        if lag < 0:
            anomalous[e.event_class] += 1
        else:
            per[e.event_class].append(lag)
    out: Dict[str, object] = {}
    for c in EVENT_CLASSES:
        lags = sorted(per[c])
        if not lags:
            out[c] = {"state": NO_RECORDED, "count": 0,
                      "anomalous": anomalous[c]}
        else:
            out[c] = {"state": "OK", "count": len(lags),
                      "min": lags[0], "median": median(lags),
                      "max": lags[-1], "anomalous": anomalous[c]}
    return out


# ---- unrecorded set -------------------------------------------------------

def unrecorded_set(events: List[EnvEvent], updates: List[RecordUpdate]):
    """Events with NO record update at all -- lag UNRECORDED, an absent record,
    not a slow one. Reported as its own set, per class."""
    recorded = {u.event_id for u in updates}
    un = [e for e in events if e.event_id not in recorded]
    by_class: Dict[str, int] = {c: 0 for c in EVENT_CLASSES}
    for e in un:
        by_class[e.event_class] += 1
    return {"events": [e.event_id for e in un], "total": len(un),
            "by_class": by_class, "lag": UNRECORDED}


# ---- combined readout -----------------------------------------------------

# distinct verdicts for the combined structural-vs-maturity readout.
GAP_STRUCTURAL = "STRUCTURAL"
GAP_MATURITY = "MATURITY_GAP"
GAP_UNDETERMINED = "UNDETERMINED"


def gap_verdict(events: List[EnvEvent], updates: List[RecordUpdate],
                window_days: int = WINDOW_DAYS,
                hi: float = rate_form.HI, lo: float = rate_form.LO):
    """The marker's Section 5 readout. Two inputs, kept visible and not
    collapsed: the rate verdict on the paired series, and the unrecorded
    count. STRUCTURAL requires BOTH a sustained dE>dM excess AND a nonzero
    unrecorded set; MATURITY_GAP requires the refresh to keep up AND the
    unrecorded set empty; anything else is UNDETERMINED with the failing
    condition named."""
    series = rate_series(events, updates, window_days)
    dE, dM = series["dE"], series["dM"]
    rv = rate_verdict(dE, dM, hi=hi, lo=lo)
    f = sustained_excess(dE, dM)
    un = unrecorded_set(events, updates)
    un_nonzero = un["total"] > 0

    if rv == STRUCTURAL and un_nonzero:
        verdict = GAP_STRUCTURAL
        note = ("sustained dE>dM AND a nonzero unrecorded set: a faster "
                "refresh does not close it")
    elif rv == MATURITY_GAP and not un_nonzero:
        verdict = GAP_MATURITY
        note = "refresh keeps up and nothing is unrecorded: closes with funding"
    else:
        verdict = GAP_UNDETERMINED
        # name which of the two conditions did not line up.
        if rv == STRUCTURAL and not un_nonzero:
            note = ("dE>dM sustained but the unrecorded set is empty: "
                    "a refresh gap, not a structural absence")
        elif rv == MATURITY_GAP and un_nonzero:
            note = ("refresh keeps up on rate but the unrecorded set is "
                    "nonzero: some events never enter the record")
        else:
            note = "rate excess is neither sustained nor kept-up (mixed)"
    return {"verdict": verdict, "rate_verdict": rv, "sustained_excess": f,
            "unrecorded_total": un["total"], "unrecorded_nonzero": un_nonzero,
            "note": note, "series": series}


# --------------------------------------------------------------------------
# CONSTRUCTED example -- NOT a county, NOT a measurement. Egress-blocked, so
# no real DOT feed is read. This exists only so the readout renders; replace
# it with a real dated event list and a real record-update list.
# --------------------------------------------------------------------------

def _demo_structural():
    """Events outrun the record and several are never recorded -> STRUCTURAL."""
    events, updates = [], []
    # a construction season: many closures/restrictions across the season.
    for i in range(24):
        eid = "ev%02d" % i
        cls = EVENT_CLASSES[i % len(EVENT_CLASSES)]
        day = _add_days(date(2026, 4, 1), i * 5)
        events.append(EnvEvent(eid, cls, day.isoformat()))
        # record only the first ~8, and those slowly; the rest never appear.
        if i < 8:
            rec = _add_days(day, 9 + (i % 4))
            updates.append(RecordUpdate(eid, rec.isoformat()))
    return events, updates


def _demo_maturity():
    """Every event recorded, promptly -> MATURITY_GAP (closes with funding)."""
    events, updates = [], []
    for i in range(12):
        eid = "mv%02d" % i
        cls = EVENT_CLASSES[i % len(EVENT_CLASSES)]
        day = _add_days(date(2026, 4, 1), i * 10)
        events.append(EnvEvent(eid, cls, day.isoformat()))
        rec = _add_days(day, 2)
        updates.append(RecordUpdate(eid, rec.isoformat()))
    return events, updates


def _add_days(d: date, n: int) -> date:
    from datetime import timedelta
    return d + timedelta(days=n)


def _wrap(s: str, width: int = 57) -> List[str]:
    # 57 so a 3-space-indented wrapped line lands at <= 60 columns.
    out, line = [], ""
    for w in s.split():
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


def render(events: List[EnvEvent], updates: List[RecordUpdate],
           label: str = "CONSTRUCTED") -> str:
    """Plain text, every line <= 60 columns."""
    validate(events, updates)
    L = ["RATE GAP  (columns <= 60)", "=" * 25, ""]
    for s in _wrap("INPUT: %s -- not a county, not a measurement. Replace "
                   "with a real dated event list and record-update list."
                   % label):
        L.append(s)
    L.append("")
    g = gap_verdict(events, updates)
    ser = g["series"]
    L.append("dE/dt vs dM/dt  (per %d-day window, %d windows)"
             % (ser["window_days"], ser["windows"]))
    L.append("   events (dE): %s" % _short(ser["dE"]))
    L.append("   record (dM): %s" % _short(ser["dM"]))
    L.append("   sustained dE>dM fraction: %.2f" % g["sustained_excess"])
    L.append("   rate verdict: %s" % g["rate_verdict"])
    L.append("")
    L.append("LAG DISTRIBUTION (recorded events, days)")
    ld = lag_distribution(events, updates)
    for c in EVENT_CLASSES:
        row = ld[c]
        if row["state"] == NO_RECORDED:
            L.append("   %-18s %s" % (c, NO_RECORDED))
        else:
            L.append("   %-18s n=%d min=%d med=%g max=%d"
                     % (c, row["count"], row["min"], row["median"],
                        row["max"]))
        if row["anomalous"]:
            L.append("      (%d anomalous: record before event)"
                     % row["anomalous"])
    L.append("")
    un = unrecorded_set(events, updates)
    L.append("UNRECORDED SET (never in the record): %d" % un["total"])
    L.append("   lag state: %s (absent, not a large lag)" % un["lag"])
    nz = [c for c in EVENT_CLASSES if un["by_class"][c]]
    for c in nz:
        L.append("   %-18s %d" % (c, un["by_class"][c]))
    L.append("")
    L.append("READOUT")
    L.append("   verdict: %s" % g["verdict"])
    L.append("   (rate=%s, unrecorded=%d)"
             % (g["rate_verdict"], g["unrecorded_total"]))
    for s in _wrap(g["note"]):
        L.append("   " + s)
    return "\n".join(L)


def _short(series, cap: int = 12):
    if len(series) <= cap:
        return " ".join(str(x) for x in series)
    head = " ".join(str(x) for x in series[:cap])
    return head + " ..(+%d)" % (len(series) - cap)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("rate_gap.py runs; its checks live in "
                         "cycle-ledger/selftest_cll.py.\n")
        sys.exit(2)
    ev, up = _demo_structural()
    print(render(ev, up, label="CONSTRUCTED (structural)"))
