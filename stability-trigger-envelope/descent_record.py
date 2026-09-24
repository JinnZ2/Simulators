#!/usr/bin/env python3
"""
descent_record.py -- the one instrument ESP-1 orders built.

WORK_ORDER.md sec.6. A DESCENT_RECORD per loaded descent, three readings:

    classify(record)            which body was moving when the stability
                                system fired: the cab, the trailer, or
                                not readable from these traces
    envelope_edge(recs, road)   the speed at which the trigger starts to
                                fire on one road, with its spread
    relocation_tally(recs)      what happened downstream of the slowdown,
                                counted by kind and by access-road bin,
                                never summed into one score

EVERYTHING THIS FILE RUNS ON IS CONSTRUCTED. The fixtures below are
authored by the same hand that wrote classify(), so F1-F5 firing is
REGRESSION (the code still does what it was written to do), not
VALIDATION (the code reads a real descent correctly). The real run --
two phones on a loaded descent, WO T1 -- is NOT_RUN.

Thresholds live in thresholds.json, append-only, every value PLACEHOLDER.
Every reading carries that status so no output can be quoted without it.

Trace format (cab_imu_file / trailer_imu_file). Either a path to a CSV:

    # sync_ts=12.40            <- shared physical tap, this phone's clock
    t_s,roll_dps
    0.00,0.012
    ...

or, for constructed fixtures, a dict {"t": [...], "roll_dps": [...],
"sync_ts": float or None}. roll_dps is roll rate about the phone's long
axis, mounted fore-aft. A phone on a cab mount is not the frame-mounted
OEM sensor (WO sec.7); T1 compares cab against trailer, not phone
against OEM.

Clock rule. Both phones log the same physical sync tap. If either mark
is missing the alignment is unverified; if the marks disagree by more
than clock_misalign_max_s the run is NOT_EVALUABLE. The instrument does
NOT shift one trace by the offset: a single offset assumes zero drift
over the run, and drift is not measured by one mark.

CC0. stdlib only. Parses under Python 3.9. Phone-buildable.
"""

import csv
import json
import math
import os
import random
import statistics
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple, Union

HERE = os.path.dirname(os.path.abspath(__file__))
THRESHOLDS_PATH = os.path.join(HERE, "thresholds.json")

SURFACES = ("dry", "wet", "snow", "ice")
DOWNSTREAM_EVENTS = ("none", "pass", "near_miss", "incident", "closure")
STATUSES = ("PLACEHOLDER", "DERIVED", "MEASURED")
MIN_RUNS = 3          # WO sec.6: INSUFFICIENT_RUNS below 3 runs on a road

# classify() labels. The first five are the order's; NEITHER_MODE is an
# addition, declared in README: a run where neither body reads high, or
# the cab reads high but the lead is unresolved or reversed, is not one
# of the order's five and is not forced into one.
GEOMETRIC_CAB_MODE = "GEOMETRIC_CAB_MODE"
TRAILER_ROLL_RISK = "TRAILER_ROLL_RISK"
TRAILER_CHANNEL_ABSENT = "TRAILER_CHANNEL_ABSENT"
NOT_EVALUABLE = "NOT_EVALUABLE"
OUT_OF_ENVELOPE = "OUT_OF_ENVELOPE"
NEITHER_MODE = "NEITHER_MODE"

INSUFFICIENT_RUNS = "INSUFFICIENT_RUNS"
NO_TRIGGER_OBSERVED = "NO_TRIGGER_OBSERVED"
EDGE_BRACKETED = "EDGE_BRACKETED"
ONSET_OVERLAP = "ONSET_OVERLAP"


# ---------------------------------------------------------------------------
# thresholds: append-only log, last entry per key is current
# ---------------------------------------------------------------------------

class ThresholdFileError(Exception):
    """thresholds.json is unreadable or breaks the append-only form."""


def load_thresholds(path=THRESHOLDS_PATH):
    """
    Read the append-only threshold log.

    path : str, JSON file with a "log" list of entries
           {seq, date, key, value, unit, status, basis}
    returns: (current, log) -- current is {key: entry} holding the last
             entry per key; log is the full list, oldest first
    raises ThresholdFileError on a non-contiguous seq, an unknown status,
           or a clock tolerance that would let an offset read as a lead
    """
    try:
        with open(path) as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        raise ThresholdFileError("cannot read %s: %s" % (path, exc))
    log = data.get("log")
    if not isinstance(log, list) or not log:
        raise ThresholdFileError("no log entries")
    current = OrderedDict()
    for i, e in enumerate(log, 1):
        for k in ("seq", "date", "key", "value", "unit", "status", "basis"):
            if k not in e:
                raise ThresholdFileError("entry %d lacks %r" % (i, k))
        if e["seq"] != i:
            raise ThresholdFileError(
                "seq %r at position %d: log must be contiguous from 1"
                % (e["seq"], i))
        if e["status"] not in STATUSES:
            raise ThresholdFileError("entry %d status %r" % (i, e["status"]))
        current[e["key"]] = e
    need = ("analysis_pre_s", "analysis_post_s", "trigger_halfwidth_s",
            "cab_high_rms_dps", "trailer_high_rms_dps", "amp_ratio_min",
            "phase_window_min_s", "phase_window_max_s", "lead_corr_min",
            "envelope_window_s", "grid_dt_s", "gap_max_s",
            "clock_misalign_max_s", "grade_pct_declared",
            "surfaces_declared", "v2_bin_edges")
    missing = [k for k in need if k not in current]
    if missing:
        raise ThresholdFileError("missing keys: %s" % ", ".join(missing))
    if (current["clock_misalign_max_s"]["value"]
            >= current["phase_window_min_s"]["value"]):
        raise ThresholdFileError(
            "clock_misalign_max_s must sit below phase_window_min_s, "
            "else a clock offset reads as a lead")
    return current, log


def thr(current, key):
    """Current value of one threshold."""
    return current[key]["value"]


def threshold_status(current):
    """One word for the status of every value in use."""
    s = sorted(set(e["status"] for e in current.values()))
    return s[0] if len(s) == 1 else "MIXED(" + ",".join(s) + ")"


# ---------------------------------------------------------------------------
# the record
# ---------------------------------------------------------------------------

TraceRef = Union[str, Dict, None]


@dataclass
class DescentRecord:
    """
    One loaded descent (WO sec.6 DESCENT_RECORD).

    region, road_id        : str labels; never an operator, carrier or unit
    grade_pct              : float, % grade of the descent          (V1)
    curve_reversals        : int, reversals over the descent        (V1)
    access_count_to_drop   : int or None, access roads to the drop  (V2)
    alternate_route_hours  : float or None, reroute hours           (V3)
    slow_users_present     : bool or None                           (V4)
    surface_state          : 'dry' | 'wet' | 'snow' | 'ice'         (V5)
    speed_mph              : float, speed on the grade at the trigger
                             (or the run's holding speed if none fired)
    esp_event_ts           : float s in the cab clock, or None when the
                             system did not fire on this run
    cab_imu_file           : CSV path or constructed dict, or None
    trailer_imu_file       : CSV path or constructed dict, or None
    downstream_event       : 'none' | 'pass' | 'near_miss' | 'incident'
                             | 'closure'
    tag                    : free label for fixtures and logs
    """
    region: str
    road_id: str
    grade_pct: float
    curve_reversals: int
    access_count_to_drop: Optional[int]
    alternate_route_hours: Optional[float]
    slow_users_present: Optional[bool]
    surface_state: str
    speed_mph: float
    esp_event_ts: Optional[float]
    cab_imu_file: TraceRef
    trailer_imu_file: TraceRef
    downstream_event: str = "none"
    tag: str = ""

    def __post_init__(self):
        if self.surface_state not in SURFACES:
            raise ValueError("surface_state %r not in %s"
                             % (self.surface_state, SURFACES))
        if self.downstream_event not in DOWNSTREAM_EVENTS:
            raise ValueError("downstream_event %r not in %s"
                             % (self.downstream_event, DOWNSTREAM_EVENTS))


# ---------------------------------------------------------------------------
# traces
# ---------------------------------------------------------------------------

@dataclass
class Trace:
    t: List[float]
    roll_dps: List[float]
    sync_ts: Optional[float]
    source: str = ""


def load_trace(ref):
    """
    Read one IMU trace.

    ref : str path to a CSV (header t_s,roll_dps; optional '# sync_ts=' line)
          or a dict {"t", "roll_dps", "sync_ts"}
    returns: Trace, times ascending
    raises ValueError on unequal lengths, non-ascending time, empty trace
    """
    if isinstance(ref, dict):
        t = [float(x) for x in ref["t"]]
        r = [float(x) for x in ref["roll_dps"]]
        sync = ref.get("sync_ts")
        src = ref.get("source", "constructed")
    else:
        t, r, sync = [], [], None
        with open(ref) as fh:
            rows = []
            for line in fh:
                s = line.strip()
                if s.startswith("#"):
                    body = s[1:].strip()
                    if body.startswith("sync_ts="):
                        sync = float(body.split("=", 1)[1])
                    continue
                if s:
                    rows.append(s)
        for row in csv.DictReader(rows):
            t.append(float(row["t_s"]))
            r.append(float(row["roll_dps"]))
        src = str(ref)
    if not t or len(t) != len(r):
        raise ValueError("trace %s: empty or unequal columns" % src)
    if any(b <= a for a, b in zip(t, t[1:])):
        raise ValueError("trace %s: time not strictly ascending" % src)
    return Trace(t, r, None if sync is None else float(sync), src)


def _interp(tr, x):
    """Linear interpolation of tr.roll_dps at time x (x inside tr.t)."""
    t, y = tr.t, tr.roll_dps
    lo, hi = 0, len(t) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if t[mid] <= x:
            lo = mid
        else:
            hi = mid
    if t[hi] == t[lo]:
        return y[lo]
    f = (x - t[lo]) / (t[hi] - t[lo])
    return y[lo] + f * (y[hi] - y[lo])


def _grid(tr, a, b, dt):
    n = int(round((b - a) / dt)) + 1
    xs = [a + i * dt for i in range(n)]
    return xs, [_interp(tr, x) for x in xs]


def _rms(v):
    return math.sqrt(sum(x * x for x in v) / len(v)) if v else 0.0


def _max_gap(tr, a, b):
    """Longest gap between samples that falls inside [a, b]."""
    g = 0.0
    for p, q in zip(tr.t, tr.t[1:]):
        if q >= a and p <= b:
            g = max(g, q - p)
    return g


def _moving_rms(v, w):
    """Centered moving RMS, window w samples."""
    h = max(1, w // 2)
    out = []
    n = len(v)
    for i in range(n):
        seg = v[max(0, i - h):min(n, i + h + 1)]
        out.append(_rms(seg))
    return out


def _pearson(a, b):
    if len(a) < 3:
        return None
    ma, mb = statistics.fmean(a), statistics.fmean(b)
    da = [x - ma for x in a]
    db = [y - mb for y in b]
    sa = math.sqrt(sum(x * x for x in da))
    sb = math.sqrt(sum(y * y for y in db))
    if sa == 0 or sb == 0:
        return None
    return sum(x * y for x, y in zip(da, db)) / (sa * sb)


def trailer_lag(cab_env, trl_env, dt, max_lag_s):
    """
    Lag of the trailer envelope behind the cab envelope.

    cab_env, trl_env : equal-length envelopes on a grid of step dt
    max_lag_s        : search +/- this many seconds
    returns: (lag_s, r) with lag_s > 0 meaning the trailer lags (cab
             leads); (None, None) when no lag gives a defined correlation
    """
    best = (None, None)
    k_max = int(round(max_lag_s / dt))
    n = len(cab_env)
    for k in range(-k_max, k_max + 1):
        if k >= 0:
            a, b = cab_env[:n - k], trl_env[k:]
        else:
            a, b = cab_env[-k:], trl_env[:n + k]
        r = _pearson(a, b)
        if r is not None and (best[1] is None or r > best[1]):
            best = (k * dt, r)
    return best


# ---------------------------------------------------------------------------
# classify
# ---------------------------------------------------------------------------

@dataclass
class Reading:
    label: str
    reason: str = ""
    evidence: Dict = field(default_factory=dict)
    thresholds: str = "PLACEHOLDER"

    def show(self):
        if self.label == NOT_EVALUABLE:
            return "NOT_EVALUABLE(%s)" % self.reason
        if self.reason:
            return "%s  [%s]" % (self.label, self.reason)
        return self.label


def classify(rec, current=None):
    """
    Which body was moving when the stability system fired.

    rec     : DescentRecord
    current : threshold dict from load_thresholds() (loaded if None)
    returns : Reading, label one of GEOMETRIC_CAB_MODE, TRAILER_ROLL_RISK,
              TRAILER_CHANNEL_ABSENT, NOT_EVALUABLE, OUT_OF_ENVELOPE,
              NEITHER_MODE; evidence carries every number the label
              rests on; thresholds carries their status
    Order of gates: declared envelope, trigger present, cab channel,
    trailer channel, clock agreement, coverage and gaps, then amplitudes
    and lead. A later gate never runs on a run an earlier gate refused.
    """
    if current is None:
        current, _ = load_thresholds()
    st = threshold_status(current)

    def out(label, reason="", **ev):
        return Reading(label, reason, ev, st)

    lo, hi = thr(current, "grade_pct_declared")
    if rec.surface_state not in thr(current, "surfaces_declared"):
        return out(OUT_OF_ENVELOPE,
                   "surface %s: thresholds not declared there; "
                   "unassessed, not clear" % rec.surface_state)
    if not (lo <= rec.grade_pct <= hi):
        return out(OUT_OF_ENVELOPE,
                   "grade %.1f%% outside declared %.1f-%.1f%%"
                   % (rec.grade_pct, lo, hi))
    if rec.esp_event_ts is None:
        return out(NOT_EVALUABLE, "no esp_event_ts: classify reads a trigger")
    if rec.cab_imu_file is None:
        return out(NOT_EVALUABLE, "no cab trace")
    if rec.trailer_imu_file is None:
        return out(TRAILER_CHANNEL_ABSENT,
                   "no trailer trace; trailer state not inferred")

    cab = load_trace(rec.cab_imu_file)
    trl = load_trace(rec.trailer_imu_file)

    if cab.sync_ts is None or trl.sync_ts is None:
        return out(NOT_EVALUABLE, "sync mark missing: alignment unverified")
    mis = abs(cab.sync_ts - trl.sync_ts)
    if mis > thr(current, "clock_misalign_max_s"):
        return out(NOT_EVALUABLE,
                   "clocks misaligned %.2f s > %.2f s tolerance"
                   % (mis, thr(current, "clock_misalign_max_s")),
                   clock_misalign_s=round(mis, 3))

    a = rec.esp_event_ts - thr(current, "analysis_pre_s")
    b = rec.esp_event_ts + thr(current, "analysis_post_s")
    for name, tr in (("cab", cab), ("trailer", trl)):
        if tr.t[0] > a or tr.t[-1] < b:
            return out(NOT_EVALUABLE,
                       "%s trace does not cover %.1f-%.1f s" % (name, a, b))
        g = _max_gap(tr, a, b)
        if g > thr(current, "gap_max_s"):
            return out(NOT_EVALUABLE,
                       "gap %.2f s in %s trace > %.2f s"
                       % (g, name, thr(current, "gap_max_s")))

    dt = thr(current, "grid_dt_s")
    _, cv = _grid(cab, a, b, dt)
    _, tv = _grid(trl, a, b, dt)
    cab_rms, trl_rms = _rms(cv), _rms(tv)
    h = thr(current, "trigger_halfwidth_s")
    _, tv_at = _grid(trl, rec.esp_event_ts - h, rec.esp_event_ts + h, dt)
    trl_at = _rms(tv_at)
    ratio = cab_rms / trl_rms if trl_rms > 0 else None

    w = int(round(thr(current, "envelope_window_s") / dt))
    lag, r = trailer_lag(_moving_rms(cv, w), _moving_rms(tv, w), dt,
                         thr(current, "phase_window_max_s"))
    if r is None or r < thr(current, "lead_corr_min"):
        lead = "UNRESOLVED"
    elif thr(current, "phase_window_min_s") <= lag \
            <= thr(current, "phase_window_max_s"):
        lead = "CAB_LEADS"
    elif lag <= -thr(current, "phase_window_min_s"):
        lead = "TRAILER_LEADS"
    else:
        lead = "SIMULTANEOUS"

    ev = dict(cab_rms_dps=round(cab_rms, 3), trailer_rms_dps=round(trl_rms, 3),
              trailer_rms_at_trigger_dps=round(trl_at, 3),
              amp_ratio=None if ratio is None else round(ratio, 2),
              trailer_lag_s=None if lag is None else round(lag, 2),
              lag_corr=None if r is None else round(r, 3), lead=lead,
              clock_misalign_s=round(mis, 3))

    if trl_rms >= thr(current, "trailer_high_rms_dps"):
        return out(TRAILER_ROLL_RISK, "trailer channel high", **ev)
    cab_high = cab_rms >= thr(current, "cab_high_rms_dps")
    ratio_ok = ratio is None or ratio >= thr(current, "amp_ratio_min")
    if cab_high and ratio_ok and lead == "CAB_LEADS":
        return out(GEOMETRIC_CAB_MODE, "", **ev)
    if not cab_high:
        why = "neither channel high"
    elif not ratio_ok:
        why = "cab/trailer ratio below amp_ratio_min"
    else:
        why = "cab high, lead %s" % lead
    return out(NEITHER_MODE, why, **ev)


# ---------------------------------------------------------------------------
# envelope_edge
# ---------------------------------------------------------------------------

def envelope_edge(records, road_id):
    """
    Trigger-onset speed on one road (WO T2 primitive).

    records : iterable of DescentRecord
    road_id : the road to read
    returns : dict with status one of INSUFFICIENT_RUNS, NO_TRIGGER_OBSERVED,
              EDGE_BRACKETED, ONSET_OVERLAP, and the speeds behind it.
              EDGE_BRACKETED: every quiet run is slower than every fired
              run; the edge lies between the fastest quiet and slowest
              fired speed. ONSET_OVERLAP: a quiet run is at or above a
              fired speed -- the edge is not one speed on this road, and
              something other than speed (grade, bank, surface, load)
              moves it. mixed_conditions lists any grade/surface spread.
    """
    runs = [x for x in records if x.road_id == road_id]
    n = len(runs)
    base = dict(road_id=road_id, n_runs=n, min_runs=MIN_RUNS)
    if n < MIN_RUNS:
        base.update(status=INSUFFICIENT_RUNS)
        return base
    fired = sorted(x.speed_mph for x in runs if x.esp_event_ts is not None)
    quiet = sorted(x.speed_mph for x in runs if x.esp_event_ts is None)
    mixed = {}
    grades = sorted(set(x.grade_pct for x in runs))
    surfaces = sorted(set(x.surface_state for x in runs))
    if len(grades) > 1:
        mixed["grade_pct"] = grades
    if len(surfaces) > 1:
        mixed["surface_state"] = surfaces
    base.update(n_fired=len(fired), n_quiet=len(quiet),
                mixed_conditions=mixed)
    if not fired:
        base.update(status=NO_TRIGGER_OBSERVED,
                    quiet_up_to_mph=quiet[-1])
        return base
    spread = dict(min=fired[0], max=fired[-1],
                  stdev=round(statistics.stdev(fired), 2)
                  if len(fired) > 1 else None)
    base.update(onset_mph=fired[0], fired_spread_mph=spread)
    below = [s for s in quiet if s < fired[0]]
    if len(below) < len(quiet):
        base.update(status=ONSET_OVERLAP,
                    quiet_at_or_above_onset_mph=[s for s in quiet
                                                 if s >= fired[0]])
    else:
        base.update(status=EDGE_BRACKETED,
                    bracket_mph=(below[-1] if below else None, fired[0]))
    return base


# ---------------------------------------------------------------------------
# relocation_tally
# ---------------------------------------------------------------------------

def v2_bin(count, edges):
    """Bin an access-road count: edges [1,2,3] -> '0','1','2','3+'."""
    if count is None:
        return "UNMEASURED"
    labels = []
    prev = 0
    for e in edges:
        labels.append((prev, e, str(prev) if e - prev == 1
                       else "%d-%d" % (prev, e - 1)))
        prev = e
    for lo, hi, lab in labels:
        if lo <= count < hi:
            return lab
    return "%d+" % edges[-1]


def relocation_tally(records, current=None):
    """
    Downstream events, counted two ways (WO T4 primitive).

    records : iterable of DescentRecord
    returns : dict with by_event, by_v2_bin, by_v2_bin_event (counts only).
              There is no total and no score key: the order's point is
              that orders 2-4 never enter a score, and adding one here
              would rebuild the same collapse.
    """
    if current is None:
        current, _ = load_thresholds()
    edges = thr(current, "v2_bin_edges")
    by_event = OrderedDict((e, 0) for e in DOWNSTREAM_EVENTS)
    by_bin = OrderedDict()
    cross = OrderedDict()
    for x in records:
        by_event[x.downstream_event] += 1
        b = v2_bin(x.access_count_to_drop, edges)
        by_bin[b] = by_bin.get(b, 0) + 1
        cross.setdefault(b, OrderedDict((e, 0) for e in DOWNSTREAM_EVENTS))
        cross[b][x.downstream_event] += 1
    return dict(by_event=by_event, by_v2_bin=by_bin,
                by_v2_bin_event=cross,
                note="counts only; never summed into a single score")


# ---------------------------------------------------------------------------
# CONSTRUCTED fixtures -- REGRESSION, not validation
# ---------------------------------------------------------------------------

def _wave(t, amp, period, start, ramp):
    """Sine at amp, envelope ramping 0->1 over [start, start+ramp]."""
    if t < start:
        return 0.0
    g = min(1.0, (t - start) / ramp)
    return amp * g * math.sin(2 * math.pi * (t - start) / period)


def constructed_trace(amp, start, seed, period=8.0, ramp=6.0, span=40.0,
                      dt=0.05, noise=0.05, sync_ts=2.0, gap=None):
    """
    A CONSTRUCTED roll-rate trace. Seeded, deterministic, no field data.

    amp      : deg/s peak once the ramp completes
    start    : s, oscillation onset
    seed     : RNG seed for the noise
    gap      : (t0, t1) to drop samples, or None
    """
    rng = random.Random(seed)
    n = int(round(span / dt)) + 1
    t, y = [], []
    for i in range(n):
        x = i * dt
        if gap and gap[0] < x < gap[1]:
            continue
        t.append(round(x, 6))
        y.append(_wave(x, amp, period, start, ramp) + rng.gauss(0, noise))
    return {"t": t, "roll_dps": y, "sync_ts": sync_ts,
            "source": "CONSTRUCTED seed=%d" % seed}


def _rec(road, speed, cab, trl, ts=20.0, surface="wet", grade=11.0,
         event="none", access=1, tag=""):
    return DescentRecord(region="REGION_A", road_id=road, grade_pct=grade,
                         curve_reversals=14, access_count_to_drop=access,
                         alternate_route_hours=3.0, slow_users_present=True,
                         surface_state=surface, speed_mph=speed,
                         esp_event_ts=ts, cab_imu_file=cab,
                         trailer_imu_file=trl, downstream_event=event,
                         tag=tag)


def fixtures():
    """
    The order's F1-F5 plus the other side of each gate (X-cases), so no
    gate is shown only in the state it was written to reach.

    returns: list of (fid, description, expected, record_or_records, road)
    """
    cab_osc = constructed_trace(6.0, 8.0, 1)
    trl_lag = constructed_trace(0.6, 12.0, 2)            # 4 s behind, small
    trl_roll = constructed_trace(5.0, 8.0, 3)            # trailer moving
    cab_small = constructed_trace(3.0, 8.0, 4)
    trl_off = constructed_trace(0.6, 12.0, 5, sync_ts=5.0)   # 3 s off
    trl_gap = constructed_trace(0.6, 12.0, 6, gap=(15.0, 16.5))
    quiet_cab = constructed_trace(0.2, 8.0, 7)
    quiet_trl = constructed_trace(0.2, 8.0, 9)
    trl_lead = constructed_trace(0.6, 4.0, 8)            # trailer first

    f5 = [_rec("ROAD_2", 31.0, None, None, ts=None),
          _rec("ROAD_2", 34.0, cab_osc, trl_lag)]
    x5 = [_rec("ROAD_3", 24.0, None, None, ts=None, event="pass"),
          _rec("ROAD_3", 27.0, None, None, ts=None, event="near_miss"),
          _rec("ROAD_3", 30.0, cab_osc, trl_lag, event="none"),
          _rec("ROAD_3", 33.0, cab_osc, trl_lag, event="closure",
               access=2)]
    return [
        ("F1", "serpentine, cab-only oscillation", GEOMETRIC_CAB_MODE,
         _rec("ROAD_1", 34.0, cab_osc, trl_lag), None),
        ("F2", "real trailer roll", TRAILER_ROLL_RISK,
         _rec("ROAD_1", 38.0, cab_small, trl_roll), None),
        ("F3", "no trailer IMU", TRAILER_CHANNEL_ABSENT,
         _rec("ROAD_1", 34.0, cab_osc, None), None),
        ("F4", "clocks misaligned > window", NOT_EVALUABLE,
         _rec("ROAD_1", 34.0, cab_osc, trl_off), None),
        ("F5", "two runs on a road", INSUFFICIENT_RUNS, f5, "ROAD_2"),
        ("X1", "gap in trailer trace", NOT_EVALUABLE,
         _rec("ROAD_1", 34.0, cab_osc, trl_gap), None),
        ("X2", "snow surface", OUT_OF_ENVELOPE,
         _rec("ROAD_1", 30.0, cab_osc, trl_lag, surface="snow"), None),
        ("X3", "both channels quiet", NEITHER_MODE,
         _rec("ROAD_1", 30.0, quiet_cab, quiet_trl), None),
        ("X4", "cab high but trailer leads", NEITHER_MODE,
         _rec("ROAD_1", 34.0, cab_osc, trl_lead), None),
        ("X5", "four runs on a road", EDGE_BRACKETED, x5, "ROAD_3"),
    ]


def run_fixtures(current=None):
    """Run every fixture; returns list of (fid, desc, expected, got, detail)."""
    if current is None:
        current, _ = load_thresholds()
    rows = []
    for fid, desc, expected, obj, road in fixtures():
        if road is None:
            rd = classify(obj, current)
            rows.append((fid, desc, expected, rd.label, rd))
        else:
            e = envelope_edge(obj, road)
            rows.append((fid, desc, expected, e["status"], e))
    return rows


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------

def render():
    """The report, as text. CONSTRUCTED data only."""
    current, log = load_thresholds()
    L = []
    L.append("descent_record -- ESP-1 instrument, CONSTRUCTED fixtures")
    L.append("fixtures are implementation-authored: REGRESSION, not "
             "validation. Real run: NOT_RUN.")
    L.append("thresholds: %d log entries, %d keys, status %s"
             % (len(log), len(current), threshold_status(current)))
    L.append("")
    L.append("fid  expected                got                     case")
    for fid, desc, exp, got, det in run_fixtures(current):
        mark = "ok " if exp == got else "MISS"
        L.append("%-4s %-23s %-23s %s  %s" % (fid, exp, got, mark, desc))
        if isinstance(det, Reading):
            if det.reason:
                L.append("       reason: %s" % det.reason)
            if det.evidence:
                ev = det.evidence
                keys = ("cab_rms_dps", "trailer_rms_dps",
                        "trailer_rms_at_trigger_dps", "amp_ratio",
                        "trailer_lag_s", "lag_corr", "lead",
                        "clock_misalign_s")
                L.append("       " + "  ".join("%s=%s" % (k, ev[k])
                                               for k in keys if k in ev))
        else:
            keep = ("n_runs", "n_fired", "n_quiet", "onset_mph",
                    "bracket_mph", "fired_spread_mph", "mixed_conditions")
            L.append("       " + "  ".join("%s=%s" % (k, det[k])
                                           for k in keep if k in det))
    L.append("")
    x5 = [f for f in fixtures() if f[0] == "X5"][0][3]
    t = relocation_tally(x5, current)
    L.append("relocation_tally on X5 (counts only, no total):")
    L.append("  by_event   " + "  ".join("%s=%d" % kv
                                         for kv in t["by_event"].items()))
    L.append("  by_v2_bin  " + "  ".join("%s=%d" % kv
                                         for kv in t["by_v2_bin"].items()))
    return "\n".join(L)


def main(argv):
    if "--selftest" in argv:
        print("descent_record.py has no selftest; run test_descent_record.py")
        return 2
    try:
        print(render())
    except ThresholdFileError as exc:
        print("could not run: %s" % exc)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
