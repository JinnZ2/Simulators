# stability-trigger-envelope/descent_record.py
#
# DISPATCH ESP-1, section 6. One instrument, built on CONSTRUCTED data.
#
# It reads a descent record and says WHICH BODY was carrying the motion --
# the tractor the sensor is mounted on, or the trailer that carries the
# at-risk mass. That is FAULT A: the measured body and the at-risk body can
# come apart, and when they do, a correct reading of the wrong body is
# indistinguishable from a finding about the right one.
#
# WHAT IT DOES NOT DO
#   It does not evaluate the stability system. Which system the reference
#   unit runs is UNREAD and no branch here depends on it.
#   It does not score an operator. There is no field for one -- see the
#   identity check in the selftest, which reads the schema rather than
#   trusting this sentence.
#   It does not claim any intervention caused any crash.
#
# TWO REFUSALS BUILT IN
#   1. TRAILER_CHANNEL_ABSENT is an absence and is never inferred. A trailer
#      that was not instrumented has not been shown to be quiet, and the
#      whole of FAULT A turns on that difference.
#   2. Where the amplitude ratio and the onset timing point opposite ways the
#      verdict is NOT_EVALUABLE, not a verdict with a caveat. Two readings
#      disagreeing is not a finding.
#
# ONSET, NOT PHASE
#   An earlier design read the lead as a phase lead from a cross-correlation
#   of the raw traces. On a serpentine descent the forcing is periodic, so a
#   phase lead is fixed only modulo one curve-reversal period: a cab leading
#   the trailer by exactly one reversal and a cab leading by nothing produce
#   the same correlation peak. Since the case predicts a lead of about one
#   reversal, that is precisely the value phase cannot read. Onset timing --
#   first exceedance of the amplitude envelope, and the envelope lag inside
#   one period of the event -- is well posed there. See RUN_NOTE.md CHOICE 1.
#
# Standard library only. Parses under Python 3.9.

from __future__ import annotations

import math
import os
import sys
from typing import Dict, List, Optional, Sequence

HERE = os.path.dirname(os.path.abspath(__file__))
THRESHOLD_FILE = os.path.join(HERE, "thresholds.txt")
CHAIN_FILE = os.path.join(HERE, "threshold_chain.txt")

# --------------------------------------------------------------------------
# closed vocabularies
# --------------------------------------------------------------------------

VERDICTS = (
    "GEOMETRIC_CAB_MODE",      # cab high, trailer low, cab first
    "TRAILER_ROLL_RISK",       # the trailer is the body moving
    "TRAILER_CHANNEL_ABSENT",  # no trailer trace. NOT a quiet trailer.
    "NOT_EVALUABLE",           # the record cannot answer the question asked
    "OUT_OF_ENVELOPE",         # outside what this reader declares it can read
)

SURFACES = ("dry", "wet", "snow", "ice")

DOWNSTREAM_EVENTS = ("none", "pass", "near_miss", "incident", "closure")

#: onset states. NO_EVENT and NO_RISE are kept apart from a measured onset and
#: from each other: nothing moved, versus already moving when the record
#: started, versus moved at a time we can name.
ONSET_STATES = ("MEASURED", "NO_EVENT", "NO_RISE")


class SchemaError(ValueError):
    """Raised at the boundary on an undeclared value."""


# --------------------------------------------------------------------------
# thresholds
# --------------------------------------------------------------------------

def _read_thresholds() -> Dict[str, str]:
    rows = {}
    with open(THRESHOLD_FILE) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise SchemaError("malformed threshold row: " + repr(line))
            key, value = line.split("=", 1)
            rows[key.strip()] = value.strip()
    return rows


def _chain_keys() -> List[str]:
    keys = []
    with open(CHAIN_FILE) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("threshold:"):
                spec = line.split(":", 1)[1].strip()
                for part in spec.split("/"):
                    keys.append(part.strip())
    return keys


def threshold(key: str):
    """One threshold, parsed. Raises on an undeclared key rather than
    defaulting: a default is a value nobody can see they are relying on."""
    rows = _read_thresholds()
    if key not in rows:
        raise SchemaError("threshold %r is not declared in thresholds.txt" % key)
    raw = rows[key]
    if "," in raw:
        out = []
        for part in raw.split(","):
            part = part.strip()
            try:
                out.append(float(part))
            except ValueError:
                out.append(part)
        return out
    try:
        return float(raw)
    except ValueError:
        return raw


def threshold_report() -> List[str]:
    """One line per declared threshold, printed by every render. A value that
    never appears in an output is a stipulation nobody can see."""
    rows = _read_thresholds()
    chain = _chain_keys()
    out = []
    for key in sorted(rows):
        mark = "provenanced" if key in chain else "UNPROVENANCED"
        out.append("  %-24s %-14s %s" % (key, rows[key], mark))
    return out


# --------------------------------------------------------------------------
# input
# --------------------------------------------------------------------------

def trace(t0_s: float, rate_hz: float, samples: Sequence[float],
          gaps: int = 0) -> Dict[str, object]:
    """One IMU channel.

    gaps is the number of dropped segments the logger reported. A trace with
    a gap is refused rather than interpolated: an interpolated sample is a
    number the instrument made up, and onset timing is exactly the quantity
    a made-up sample moves.
    """
    if rate_hz <= 0:
        raise SchemaError("sample rate must be positive")
    if gaps < 0:
        raise SchemaError("gap count cannot be negative")
    return {"t0_s": float(t0_s), "rate_hz": float(rate_hz),
            "samples": [float(x) for x in samples], "gaps": int(gaps)}


def descent_record(region: str, road_id: str, grade_pct: float,
                   curve_reversals: int, access_count_to_drop: int,
                   alternate_route_hours: float, slow_users_present: bool,
                   surface_state: str, speed_mph: float,
                   esp_event_ts: Optional[float],
                   cab_imu: Optional[Dict[str, object]],
                   trailer_imu: Optional[Dict[str, object]],
                   downstream_event: str = "none",
                   note: str = "") -> Dict[str, object]:
    """One descent.

    There is no field for the operator, the carrier or the unit, and none is
    accepted. The schema is the guarantee; the selftest reads the field names
    rather than trusting this docstring.

    trailer_imu is None when the trailer was not instrumented. That is a
    different state from an instrumented trailer that stayed quiet, and the
    two return different verdicts.
    """
    if surface_state not in SURFACES:
        raise SchemaError("surface_state %r is outside %r"
                          % (surface_state, SURFACES))
    if downstream_event not in DOWNSTREAM_EVENTS:
        raise SchemaError("downstream_event %r is outside %r"
                          % (downstream_event, DOWNSTREAM_EVENTS))
    if curve_reversals < 0:
        raise SchemaError("curve_reversals cannot be negative")
    return {"region": region, "road_id": road_id,
            "grade_pct": float(grade_pct),
            "curve_reversals": int(curve_reversals),
            "access_count_to_drop": int(access_count_to_drop),
            "alternate_route_hours": float(alternate_route_hours),
            "slow_users_present": bool(slow_users_present),
            "surface_state": surface_state,
            "speed_mph": float(speed_mph),
            "esp_event_ts": esp_event_ts,
            "cab_imu": cab_imu, "trailer_imu": trailer_imu,
            "downstream_event": downstream_event, "note": note}


#: field names the schema must never carry. Checked against the record's own
#: keys by the selftest, so the promise is structural rather than editorial.
IDENTITY_TOKENS = ("operator", "driver", "carrier", "fleet", "unit", "vin",
                   "name", "employee", "cdl", "company")


# --------------------------------------------------------------------------
# envelope and onset
# --------------------------------------------------------------------------

def _mean(xs: Sequence[float]) -> Optional[float]:
    xs = list(xs)
    if not xs:
        return None
    return sum(xs) / len(xs)


def _rms(xs: Sequence[float]) -> Optional[float]:
    xs = list(xs)
    if not xs:
        return None
    m = sum(xs) / len(xs)
    total = 0.0
    for x in xs:
        total += (x - m) * (x - m)
    return math.sqrt(total / len(xs))


def envelope(samples: Sequence[float], window: int) -> List[float]:
    """Moving RMS about the series mean. Centred, edges shortened rather than
    padded -- a padded edge invents the quiet the onset is measured against."""
    xs = list(samples)
    n = len(xs)
    if n == 0:
        return []
    if window < 1:
        window = 1
    m = sum(xs) / n
    half = window // 2
    out = []
    for i in range(n):
        lo = i - half
        if lo < 0:
            lo = 0
        hi = i + half + 1
        if hi > n:
            hi = n
        total = 0.0
        for j in range(lo, hi):
            total += (xs[j] - m) * (xs[j] - m)
        out.append(math.sqrt(total / (hi - lo)))
    return out


def onset(env: Sequence[float], rate_hz: float, t0_s: float,
          frac: float, floor: float) -> Dict[str, object]:
    """First exceedance of `frac` of this body's OWN peak envelope.

    Relative to itself on purpose: onset says WHEN a body started, never how
    much it moved. Size is the amplitude ratio's job, and merging the two
    would let a large late body and a small early one report the same.

    Three states, kept apart:
      MEASURED  a rise was found and can be timed
      NO_EVENT  the envelope never clears the floor; nothing to time
      NO_RISE   already above threshold at the first sample, so the record
                started mid-event and the onset is outside it. Not t = 0.
    """
    env = list(env)
    if not env:
        return {"state": "NO_EVENT", "reason": "empty trace"}
    peak = max(env)
    if peak <= floor:
        return {"state": "NO_EVENT",
                "reason": "peak envelope %.3g is at or below the floor %.3g"
                          % (peak, floor)}
    thr = frac * peak
    # The record has to START QUIET or there is no rise inside it to time.
    # A steady oscillation is the case this catches: its envelope is flat, so
    # the first sample is already near the peak and any index the scan
    # returns is an artifact of the window shortening at the edge rather than
    # an arrival. Half the threshold, so a genuine burst (whose envelope
    # starts at zero) is unaffected.
    if env[0] >= thr:
        return {"state": "NO_RISE",
                "reason": "already above threshold at the first sample; the "
                          "record starts mid-event and the onset is outside it"}
    if env[0] > 0.5 * thr:
        return {"state": "NO_RISE",
                "reason": "the record does not start quiet (first envelope "
                          "sample %.3g against a threshold of %.3g), so the "
                          "rise is not contained in it" % (env[0], thr)}
    idx = None
    for i, v in enumerate(env):
        if v >= thr:
            idx = i
            break
    if idx is None:
        return {"state": "NO_EVENT", "reason": "threshold never reached"}
    return {"state": "MEASURED", "index": idx, "t_s": t0_s + idx / rate_hz,
            "threshold": thr, "peak": peak}


def _pearson(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = 0.0
    dx = 0.0
    dy = 0.0
    for i in range(n):
        a = xs[i] - mx
        b = ys[i] - my
        num += a * b
        dx += a * a
        dy += b * b
    if dx <= 0 or dy <= 0:
        return None
    return num / math.sqrt(dx * dy)


def envelope_lag(cab_env: Sequence[float], trl_env: Sequence[float],
                 rate_hz: float, period_s: float,
                 search_periods: float) -> Dict[str, object]:
    """Lag at maximum cross-correlation of the two ENVELOPES, searched within
    `search_periods` of the event.

    Envelopes rather than raw traces, because an envelope is not periodic at
    the forcing frequency -- which is the whole reason this replaces a phase
    lead. Positive lead_s means the cab envelope rose first.
    """
    a = list(cab_env)
    b = list(trl_env)
    n = min(len(a), len(b))
    if n < 4:
        return {"state": "NOT_EVALUABLE", "reason": "trace too short"}
    a = a[:n]
    b = b[:n]
    max_lag = int(round(search_periods * period_s * rate_hz))
    if max_lag < 1:
        return {"state": "NOT_EVALUABLE",
                "reason": "the search window is under one sample"}
    if max_lag >= n:
        max_lag = n - 2
    if max_lag < 1:
        return {"state": "NOT_EVALUABLE",
                "reason": "the record is shorter than the search window"}
    best_lag = None
    best_r = None
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            xs = a[lag:]
            ys = b[:n - lag]
        else:
            xs = a[:n + lag]
            ys = b[-lag:]
        m = min(len(xs), len(ys))
        if m < 3:
            continue
        r = _pearson(xs[:m], ys[:m])
        if r is None:
            continue
        if best_r is None or r > best_r:
            best_r = r
            best_lag = lag
    if best_r is None:
        return {"state": "NOT_EVALUABLE",
                "reason": "no lag produced a computable correlation"}
    return {"state": "MEASURED", "lead_samples": -best_lag,
            "lead_s": -best_lag / rate_hz, "peak_correlation": best_r,
            "search_samples": max_lag}


# --------------------------------------------------------------------------
# classify
# --------------------------------------------------------------------------

def classify(record: Dict[str, object]) -> Dict[str, object]:
    """Which body was carrying the motion. One of VERDICTS."""
    surfaces = threshold("surfaces_in_envelope")
    if not isinstance(surfaces, list):
        surfaces = [surfaces]
    g_min = threshold("grade_pct_min")
    g_max = threshold("grade_pct_max")

    # 1. is this record inside what the READER declares it can read?
    #    This is not the vehicle's validation envelope and must not be read
    #    as one: measuring that is T2 and T5, and neither has been run.
    if record["surface_state"] not in surfaces:
        return {"verdict": "OUT_OF_ENVELOPE",
                "reason": "surface %r is outside the declared reading set %r; "
                          "on snow or ice the margin and the sensor behaviour "
                          "are different and this reader does not reach them"
                          % (record["surface_state"], surfaces)}
    if record["grade_pct"] < g_min or record["grade_pct"] > g_max:
        return {"verdict": "OUT_OF_ENVELOPE",
                "reason": "grade %.2f%% is outside the declared reading range "
                          "%.2f..%.2f%%" % (record["grade_pct"], g_min, g_max)}

    # 2. absence, never inferred
    if record["trailer_imu"] is None:
        return {"verdict": "TRAILER_CHANNEL_ABSENT",
                "reason": "no trailer trace. The trailer has NOT been shown to "
                          "be quiet, and fault A turns on that difference: a "
                          "correct reading of the cab says nothing about the "
                          "body carrying the at-risk mass."}
    if record["cab_imu"] is None:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "no cab trace; there is no measured body to compare"}

    cab = record["cab_imu"]
    trl = record["trailer_imu"]

    # 3. can the two traces be compared at all?
    if cab["gaps"] > 0 or trl["gaps"] > 0:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "gap in a trace (cab %d, trailer %d); an "
                          "interpolated sample is a number the instrument "
                          "made up, and onset is what it would move"
                          % (cab["gaps"], trl["gaps"])}
    clock_tol = threshold("clock_tolerance_s")
    offset = abs(cab["t0_s"] - trl["t0_s"])
    if offset > clock_tol:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "trace start times differ by %.4g s, above the %.4g s "
                          "tolerance; a lead between two clocks is not a lead "
                          "between two bodies" % (offset, clock_tol)}
    rate_tol = threshold("rate_tolerance_frac")
    hi_rate = max(cab["rate_hz"], trl["rate_hz"])
    mismatch = abs(cab["rate_hz"] - trl["rate_hz"]) / hi_rate
    if mismatch > rate_tol:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "sample rates differ by %.2f%% (%g Hz vs %g Hz), "
                          "above the %.2f%% tolerance"
                          % (100 * mismatch, cab["rate_hz"], trl["rate_hz"],
                             100 * rate_tol)}
    n = min(len(cab["samples"]), len(trl["samples"]))
    if n < 8:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "%d overlapping samples is too few to read an "
                          "envelope" % n}
    if record["curve_reversals"] < 1:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "no curve reversals declared, so there is no forcing "
                          "period and no window to search within"}

    rate = cab["rate_hz"]
    duration_s = n / rate
    period_s = duration_s / record["curve_reversals"]
    win = int(round(threshold("envelope_window_frac") * period_s * rate))
    if win < 1:
        win = 1

    cab_env = envelope(cab["samples"][:n], win)
    trl_env = envelope(trl["samples"][:n], win)

    cab_rms = _rms(cab["samples"][:n])
    trl_rms = _rms(trl["samples"][:n])
    if cab_rms is None or trl_rms is None:
        return {"verdict": "NOT_EVALUABLE", "reason": "a trace is empty"}
    if cab_rms == 0 and trl_rms == 0:
        return {"verdict": "NOT_EVALUABLE",
                "reason": "neither body moved; there is no motion to place"}
    if trl_rms == 0:
        ratio = float("inf")
    else:
        ratio = cab_rms / trl_rms

    floor = threshold("onset_variance_floor")
    frac = threshold("onset_frac")
    cab_onset = onset(cab_env, rate, cab["t0_s"], frac, floor)
    trl_onset = onset(trl_env, rate, trl["t0_s"], frac, floor)
    lag = envelope_lag(cab_env, trl_env, rate, period_s,
                       threshold("onset_search_periods"))

    # onset lead: positive means the cab rose first
    if cab_onset["state"] == "MEASURED" and trl_onset["state"] == "MEASURED":
        onset_lead_s = trl_onset["t_s"] - cab_onset["t_s"]
        onset_basis = "both bodies timed"
    elif cab_onset["state"] == "MEASURED" and trl_onset["state"] == "NO_EVENT":
        onset_lead_s = None
        onset_basis = ("the cab has an onset and the trailer has none; the "
                       "cab is first by default and the lead has no value")
    elif trl_onset["state"] == "MEASURED" and cab_onset["state"] == "NO_EVENT":
        onset_lead_s = None
        onset_basis = ("the trailer has an onset and the cab has none")
    else:
        onset_lead_s = None
        onset_basis = ("cab %s, trailer %s"
                       % (cab_onset["state"], trl_onset["state"]))

    hi = threshold("amplitude_ratio_hi")
    lo = threshold("amplitude_ratio_lo")

    common = {"amplitude_ratio": ratio, "cab_rms": cab_rms,
              "trailer_rms": trl_rms, "cab_onset": cab_onset,
              "trailer_onset": trl_onset, "onset_lead_s": onset_lead_s,
              "onset_basis": onset_basis, "envelope_lag": lag,
              "forcing_period_s": period_s, "envelope_window_samples": win,
              "decided_by": "amplitude_ratio, checked against onset timing"}

    if ratio >= hi:
        candidate = "GEOMETRIC_CAB_MODE"
        reason = ("cab rms is %.3gx the trailer, at or above the declared "
                  "ratio %g" % (ratio, hi))
    elif ratio <= lo:
        candidate = "TRAILER_ROLL_RISK"
        reason = ("cab rms is %.3gx the trailer, at or below the declared "
                  "ratio %g" % (ratio, lo))
    else:
        out = dict(common)
        out["verdict"] = "NOT_EVALUABLE"
        out["reason"] = ("amplitude ratio %.3g sits between the declared "
                         "bounds %g and %g; the two bodies move comparably "
                         "and this record does not separate them"
                         % (ratio, lo, hi))
        return out

    # onset agreement. Undetermined is not agreement and is not disagreement.
    agrees = None
    if onset_lead_s is not None and abs(onset_lead_s) > 1e-12:
        if candidate == "GEOMETRIC_CAB_MODE":
            agrees = onset_lead_s > 0
        else:
            agrees = onset_lead_s < 0
    elif (candidate == "GEOMETRIC_CAB_MODE"
          and cab_onset["state"] == "MEASURED"
          and trl_onset["state"] == "NO_EVENT"):
        agrees = True
    elif (candidate == "TRAILER_ROLL_RISK"
          and trl_onset["state"] == "MEASURED"
          and cab_onset["state"] == "NO_EVENT"):
        agrees = True

    if agrees is False:
        out = dict(common)
        out["verdict"] = "NOT_EVALUABLE"
        out["onset_agrees"] = False
        out["reason"] = ("amplitude reads %s while onset has the other body "
                         "moving first (lead %+.4g s); two readings pointing "
                         "opposite ways is not a verdict"
                         % (candidate, onset_lead_s))
        return out

    out = dict(common)
    out["verdict"] = candidate
    out["reason"] = reason
    out["onset_agrees"] = agrees
    return out


# --------------------------------------------------------------------------
# envelope_edge -- the measured edge of the validation envelope (T2)
# --------------------------------------------------------------------------

def envelope_edge(records: Sequence[Dict[str, object]],
                  road_id: str) -> Dict[str, object]:
    """Onset speed with spread for one road, or INSUFFICIENT_RUNS.

    Runs where the trigger did NOT fire are kept and reported separately
    rather than dropped. They bound the edge from below: a run at 40 mph with
    no trigger is information about where the edge is not, and discarding it
    leaves the edge looking tighter than the data supports.
    """
    on_road = [r for r in records if r["road_id"] == road_id]
    fired = [r for r in on_road if r["esp_event_ts"] is not None]
    quiet = [r for r in on_road if r["esp_event_ts"] is None]
    need = int(threshold("min_runs_for_edge"))
    if len(fired) < need:
        return {"state": "INSUFFICIENT_RUNS", "road_id": road_id,
                "runs_with_trigger": len(fired),
                "runs_without_trigger": len(quiet),
                "required": need,
                "no_trigger_speeds": sorted(r["speed_mph"] for r in quiet),
                "reason": ("%d run(s) with a trigger on this road against a "
                           "declared minimum of %d. Two points give a speed "
                           "and no spread, and an edge quoted without a "
                           "spread is a point pretending to be a measurement."
                           % (len(fired), need))}
    speeds = sorted(r["speed_mph"] for r in fired)
    mid = len(speeds) // 2
    if len(speeds) % 2 == 1:
        median = speeds[mid]
    else:
        median = 0.5 * (speeds[mid - 1] + speeds[mid])
    return {"state": "MEASURED", "road_id": road_id,
            "runs_with_trigger": len(fired),
            "runs_without_trigger": len(quiet),
            "onset_speed_min": speeds[0], "onset_speed_max": speeds[-1],
            "onset_speed_median": median,
            "spread_mph": speeds[-1] - speeds[0],
            "speeds": speeds,
            "no_trigger_speeds": sorted(r["speed_mph"] for r in quiet),
            "note": ("the no-trigger speeds bound this edge from below and "
                     "are reported beside it, not folded into it")}


# --------------------------------------------------------------------------
# relocation_tally -- ORDER 2..4, the cost the safety score does not see
# --------------------------------------------------------------------------

def _bin_label(value: int, edges: Sequence[float]) -> str:
    edges = sorted(edges)
    for e in edges:
        if value <= e:
            return "<=%g" % e
    return ">%g" % edges[-1]


def relocation_tally(records: Sequence[Dict[str, object]]) -> Dict[str, object]:
    """Counts by downstream_event, and by V2 access-road bin.

    Nothing here is summed into a single score, and no function in this module
    returns one. A relocation index would be the same move the safety score
    already makes -- collapsing several different costs into one number that
    can then be compared against a number built a different way.
    """
    edges = threshold("access_bins")
    if not isinstance(edges, list):
        edges = [edges]
    by_event = {}
    for name in DOWNSTREAM_EVENTS:
        by_event[name] = 0
    by_bin = {}
    for r in records:
        by_event[r["downstream_event"]] = by_event[r["downstream_event"]] + 1
        label = _bin_label(r["access_count_to_drop"], edges)
        if label not in by_bin:
            by_bin[label] = {}
            for name in DOWNSTREAM_EVENTS:
                by_bin[label][name] = 0
        by_bin[label][r["downstream_event"]] += 1
    return {"n_records": len(records), "by_event": by_event,
            "by_access_bin": by_bin, "bin_edges": edges,
            "score": None,
            "score_note": ("no composite is emitted. The counts are the "
                           "reading; collapsing them would repeat the move "
                           "that lost orders 2 to 4 in the first place.")}


# --------------------------------------------------------------------------
# render
# --------------------------------------------------------------------------

def render_classify(result: Dict[str, object]) -> List[str]:
    out = ["  VERDICT: %s" % result["verdict"], "    %s" % result["reason"]]
    if "amplitude_ratio" not in result:
        return out
    out.append("    amplitude ratio cab/trailer: %.4g   (cab rms %.4g, "
               "trailer rms %.4g)" % (result["amplitude_ratio"],
                                      result["cab_rms"],
                                      result["trailer_rms"]))
    co = result["cab_onset"]
    to = result["trailer_onset"]
    if co["state"] == "MEASURED":
        out.append("    cab onset:     t = %.4g s" % co["t_s"])
    else:
        out.append("    cab onset:     %s -- %s" % (co["state"], co["reason"]))
    if to["state"] == "MEASURED":
        out.append("    trailer onset: t = %.4g s" % to["t_s"])
    else:
        out.append("    trailer onset: %s -- %s" % (to["state"], to["reason"]))
    if result["onset_lead_s"] is None:
        out.append("    onset lead:    no value -- %s" % result["onset_basis"])
    else:
        out.append("    onset lead:    %+.4g s (positive = cab first)"
                   % result["onset_lead_s"])
    lag = result["envelope_lag"]
    if lag["state"] == "MEASURED":
        out.append("    envelope lag:  %+.4g s within %g period(s) of the "
                   "event, peak r %.3f"
                   % (lag["lead_s"], threshold("onset_search_periods"),
                      lag["peak_correlation"]))
    else:
        out.append("    envelope lag:  NOT_EVALUABLE -- %s" % lag["reason"])
    out.append("    forcing period: %.4g s   envelope window: %d samples"
               % (result["forcing_period_s"],
                  result["envelope_window_samples"]))
    if "onset_agrees" in result:
        out.append("    onset agrees with amplitude: %s"
                   % result["onset_agrees"])
    return out


def render_edge(result: Dict[str, object]) -> List[str]:
    if result["state"] == "INSUFFICIENT_RUNS":
        return ["  %s on %s -- %s" % (result["state"], result["road_id"],
                                      result["reason"]),
                "    runs with a trigger: %d   without: %d   required: %d"
                % (result["runs_with_trigger"],
                   result["runs_without_trigger"], result["required"]),
                "    no-trigger speeds kept: %s" % result["no_trigger_speeds"]]
    return ["  %s on %s" % (result["state"], result["road_id"]),
            "    onset speed  min %.4g  median %.4g  max %.4g  spread %.4g mph"
            % (result["onset_speed_min"], result["onset_speed_median"],
               result["onset_speed_max"], result["spread_mph"]),
            "    speeds with a trigger: %s" % result["speeds"],
            "    speeds without a trigger: %s" % result["no_trigger_speeds"],
            "    %s" % result["note"]]


def render_tally(result: Dict[str, object]) -> List[str]:
    out = ["  records: %d" % result["n_records"], "  by downstream_event:"]
    for name in DOWNSTREAM_EVENTS:
        out.append("    %-12s %d" % (name, result["by_event"][name]))
    out.append("  by access-road bin (V2), edges %s:" % result["bin_edges"])
    for label in sorted(result["by_access_bin"]):
        row = result["by_access_bin"][label]
        parts = []
        for name in DOWNSTREAM_EVENTS:
            if row[name]:
                parts.append("%s=%d" % (name, row[name]))
        if not parts:
            parts.append("empty")
        out.append("    %-8s %s" % (label, "  ".join(parts)))
    out.append("  score: %s" % result["score"])
    out.append("  %s" % result["score_note"])
    return out


def main() -> int:
    import cases
    print("DISPATCH ESP-1 -- stability-trigger-envelope")
    print("=" * 72)
    print()
    print(cases.FIXTURE_NOTE)
    for name, builder, expected in cases.FIXTURES:
        print("%s -> expected %s" % (name, expected))
        rec = builder()
        if name.startswith("F5"):
            for line in render_edge(envelope_edge(rec, "constructed-road-5")):
                print(line)
        else:
            for line in render_classify(classify(rec)):
                print(line)
        print()
    print("RELOCATION TALLY over the constructed set")
    for line in render_tally(relocation_tally(cases.tally_set())):
        print(line)
    print()
    print("thresholds in force (every one PLACEHOLDER unless marked):")
    for line in threshold_report():
        print(line)
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("descent_record.py is the instrument; its checks live in "
              "test_envelope.py. Run: python3 test_envelope.py")
        raise SystemExit(2)
    raise SystemExit(main())
