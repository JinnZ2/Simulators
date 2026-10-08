"""
moving-mean-tracker/tracker.py -- a mean anchored to moving targets, tracked
per segment, with provenance, on a fixed schedule.

STATUS: PROPOSED instrument. No data yet. The only provider that ships is
synthetic (provider.FixtureProvider). Nothing here is a measurement of any
population.

The mechanism the instrument watches. Take a mean of a quantity whose
distribution is moving: GDP, a wealth gap, a skills or literacy score.
The mean moves with that distribution. Any norm, filter or loss tied to
the mean then moves with it too. The instrument records the drift. It
does not decide what the drift means.

    provider --records + provenance--> assign to segments (frozen rules)
       |                                       |
       |                 kept records -------> n, mean, median, p10, p90,
       |                                       mean_minus_median per metric
       |                 dropped records ----> drop share per segment
       v                                       (each carries its rule)
    run entry --append, hash-chained--> run log --series--> gauges G1..G4

GAUGES (series across runs, per axis, per segment):
  G1  mean_minus_median                 tail pull on the reference
  G2  sample_share - population_share   access-gate loop running
  G3  dropped / (dropped + kept)        cleaning acting as a class filter
  G4  dollars per physical unit, when   token drift vs real change
      the metric declares a physical
      unit; across runs, (dollar mean ratio / physical mean ratio) - 1

STATES, never read as numbers:
  UNRATED              G2 for a segment whose axis has no population
                       reference that is named AND dated, or whose
                       reference gives no share for that segment.
  INSUFFICIENT_SAMPLE  a segment with fewer kept records than min_n. It
                       gets no stats and no G1 or G4 value, only its n.
  NOT_DECLARED         G4 for a metric with no declared physical unit.
  CROSS_VERSION        a delta between two runs whose segment definitions
                       or metric declarations differ. No delta is computed
                       across them.

RULES the code enforces (each refusal raises TrackerRefused and names
what is missing):
  - Segments and metrics are declared in the config before run 1. A run
    dated before the config's `declared` date is refused.
  - Segment definitions are frozen. A definition whose hash differs from
    the last logged run under the SAME version label is refused. A change
    needs a new version label and date. A run under the new version is
    accepted, and every delta across the change reads CROSS_VERSION.
  - Every dropped record carries a drop_rule. A kept record with a missing
    metric value is refused: excluding it silently would be a drop with no
    rule.
  - The run log is append-only. Each entry stores the sha256 of the log
    bytes before it. A period already in the log is refused (never
    overwritten), and verify_log() re-checks the whole chain.

Run: python3 test_tracker.py
CLI: python3 tracker.py --validate CONFIG
     python3 tracker.py --run CONFIG --period P --run-at YYYY-MM-DD
                        --log LOG.jsonl [--fixture KNOBS.json]
     python3 tracker.py --gauges LOG.jsonl
     python3 tracker.py --verify LOG.jsonl
     python3 tracker.py --choices
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

UNRATED = "UNRATED"
INSUFFICIENT = "INSUFFICIENT_SAMPLE"
NOT_DECLARED = "NOT_DECLARED"
CROSS_VERSION = "CROSS_VERSION"
STATES = (UNRATED, INSUFFICIENT, NOT_DECLARED, CROSS_VERSION)

INTERVALS = {"monthly": 1, "quarterly": 3, "annual": 12}
DEFAULT_INTERVAL = "quarterly"

PROVENANCE_KEYS = ("source", "pull_date", "query", "filters_applied",
                   "dropped", "drop_rule")
RECORD_KEYS = ("id", "attrs", "values", "provenance")

CHOICES = {
    1: "Quantiles use linear interpolation between order statistics "
       "(the type 7 definition, the one most spreadsheet PERCENTILE "
       "functions use). Median is the 0.5 quantile. The spec names no "
       "method. A different method moves p10 and p90 on small n.",
    2: "sample_share's denominator is the kept records ASSIGNED on that "
       "axis. Unassigned and dropped records are counted apart, not inside "
       "the share. Shares then sum to 1 over an axis's segments, as a "
       "population reference's shares do.",
    3: "A population reference's shares must sum to 1 within 0.01. "
       "Otherwise the config is refused: such a reference is malformed, "
       "which is a different state from undeclared.",
    4: "G4's per-run value is sum(dollars) / sum(physical) over a "
       "segment's kept records, so dollars per physical unit. The "
       "cross-run token drift is (dollar mean ratio) / (physical mean "
       "ratio) - 1. Zero means dollars and the physical quantity moved "
       "together.",
    5: "Segment rules are {field, equals} or {field, min, max}. min is "
       "inclusive and max exclusive; either bound may be omitted. A record "
       "matching two segments on one axis is refused: an axis's segments "
       "must partition the records. A record matching none is counted "
       "UNASSIGNED on that axis.",
    6: "Schedule periods are labelled 2026Q4 (quarterly), 2026-10 "
       "(monthly) or 2026 (annual). A run for any period other than the "
       "next one after the last logged run is accepted. It is stamped "
       "OFF_SCHEDULE with the expected period beside it, not refused: a "
       "missed quarter is a fact about the schedule, and refusing the "
       "run would erase it.",
    7: "A missing schedule.interval reads as the dispatch's default "
       "(quarterly). The run entry records interval_source = 'default', so "
       "a reader can tell a default from a declaration.",
}

SHARE_TOL = 0.01


class TrackerRefused(Exception):
    """A rule was not met; the message names it."""


# ------------------------------------------------------------- arithmetic

def quantile(values, q):
    """[CHOICE 1] Linear interpolation between order statistics.
    None on an empty list, never 0."""
    xs = sorted(float(v) for v in values)
    if not xs:
        return None
    if not 0.0 <= q <= 1.0:
        raise ValueError("q outside [0, 1]: %r" % q)
    pos = (len(xs) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return xs[lo]
    return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)


def share_gap(sample_share, population_share):
    """G2 for one segment. UNRATED when there is no population share, a
    measured 0.0 only when the two shares are equal. None when the sample
    share itself is undefined (no kept, assigned records on the axis)."""
    if population_share is None:
        return UNRATED
    if sample_share is None:
        return None
    return sample_share - population_share


def segment_stats(values, min_n):
    """n, mean, median, p10, p90, mean_minus_median, or INSUFFICIENT_SAMPLE
    with n only. Stats are never computed below min_n."""
    n = len(values)
    if n < min_n:
        return {"n": n, "state": INSUFFICIENT, "mean": None, "median": None,
                "p10": None, "p90": None, "mean_minus_median": None}
    mean = sum(values) / n
    median = quantile(values, 0.5)
    return {"n": n, "state": None, "mean": mean, "median": median,
            "p10": quantile(values, 0.1), "p90": quantile(values, 0.9),
            "mean_minus_median": mean - median}


# ------------------------------------------------------------- config

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _sha(obj):
    return hashlib.sha256(_canon(obj).encode("utf-8")).hexdigest()


def def_hash(axis):
    """Hash of an axis's segment rules only. The version label and date are
    left out, so a relabel that changes no rule is still comparable."""
    return _sha(axis["segments"])


def metrics_hash(cfg):
    return _sha(cfg["metrics"])


def validate_config(cfg):
    """Return the config with defaults filled; raise TrackerRefused naming
    every missing or malformed declaration."""
    bad = []
    if not isinstance(cfg, dict):
        raise TrackerRefused("config is not an object")
    if not isinstance(cfg.get("config_version"), str) or \
            not cfg.get("config_version"):
        bad.append("config_version (string) not declared")
    if not _DATE.match(str(cfg.get("declared", ""))):
        bad.append("declared (YYYY-MM-DD) not declared")
    sched = cfg.get("schedule") or {}
    interval = sched.get("interval")
    if interval is None:
        interval_source = "default"            # [CHOICE 7]
        interval = DEFAULT_INTERVAL
    else:
        interval_source = "declared"
    if interval not in INTERVALS:
        bad.append("schedule.interval %r not one of %s"
                   % (interval, sorted(INTERVALS)))
    metrics = cfg.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        bad.append("metrics not declared (a non-empty list is required "
                   "before run 1)")
        metrics = []
    names = set()
    for m in metrics:
        if not isinstance(m, dict) or not m.get("name") or not m.get("unit"):
            bad.append("metric %r lacks name or unit" % (m,))
            continue
        if m["name"] in names:
            bad.append("metric %r declared twice" % m["name"])
        names.add(m["name"])
        phys = m.get("physical")
        if phys is not None and (not isinstance(phys, dict) or
                                 not phys.get("unit") or
                                 not phys.get("field")):
            bad.append("metric %r: physical must give unit and field"
                       % m["name"])
    min_n = cfg.get("min_n")
    if not isinstance(min_n, int) or isinstance(min_n, bool) or min_n < 1:
        bad.append("min_n (integer >= 1) not declared")
    axes = cfg.get("axes")
    if not isinstance(axes, dict) or not axes:
        bad.append("axes (segments) not declared (required before run 1)")
        axes = {}
    for aname, axis in axes.items():
        if not isinstance(axis, dict):
            bad.append("axis %r is not an object" % aname)
            continue
        if not axis.get("version"):
            bad.append("axis %r has no version label" % aname)
        if not _DATE.match(str(axis.get("dated", ""))):
            bad.append("axis %r has no dated (YYYY-MM-DD)" % aname)
        segs = axis.get("segments")
        if not isinstance(segs, dict) or not segs:
            bad.append("axis %r declares no segments" % aname)
            continue
        for sname, rule in segs.items():
            if not isinstance(rule, dict) or not rule.get("field"):
                bad.append("segment %s/%s has no field" % (aname, sname))
            elif "equals" not in rule and "min" not in rule and \
                    "max" not in rule:
                bad.append("segment %s/%s has no equals, min or max"
                           % (aname, sname))
    refs = cfg.get("population_reference") or {}
    for aname, ref in refs.items():
        if aname not in axes:
            bad.append("population_reference for undeclared axis %r"
                       % aname)
            continue
        shares = (ref or {}).get("shares") or {}
        if shares:
            total = sum(float(v) for v in shares.values())
            if abs(total - 1.0) > SHARE_TOL:      # [CHOICE 3]
                bad.append("population_reference %r shares sum to %.4f"
                           % (aname, total))
            unknown = set(shares) - set(axes[aname].get("segments", {}))
            if unknown:
                bad.append("population_reference %r names undeclared "
                           "segments %s" % (aname, sorted(unknown)))
    if bad:
        raise TrackerRefused("config refused: " + "; ".join(bad))
    out = dict(cfg)
    out["schedule"] = {"interval": interval}
    out["_interval_source"] = interval_source
    return out


def reference_for(cfg, axis):
    """(name, date, shares) when the axis's reference is named AND dated,
    else None. A reference with a name and no date is not a reference."""
    ref = (cfg.get("population_reference") or {}).get(axis)
    if not ref or not ref.get("name") or not _DATE.match(
            str(ref.get("date", ""))):
        return None
    return ref


# ------------------------------------------------------------- records

def matches(rule, attrs):
    """[CHOICE 5]"""
    if rule["field"] not in attrs:
        return False
    v = attrs[rule["field"]]
    if "equals" in rule:
        return v == rule["equals"]
    try:
        x = float(v)
    except (TypeError, ValueError):
        return False
    lo, hi = rule.get("min"), rule.get("max")
    if lo is not None and x < lo:
        return False
    if hi is not None and x >= hi:
        return False
    return True


def assign(record, aname, axis):
    hits = [s for s, rule in axis["segments"].items()
            if matches(rule, record["attrs"])]
    if len(hits) > 1:
        raise TrackerRefused(
            "record %s matches %d segments on axis %r (%s): segments must "
            "partition the records" % (record["id"], len(hits), aname,
                                        ", ".join(sorted(hits))))
    return hits[0] if hits else None


def validate_record(rec, cfg):
    if sorted(rec) != sorted(RECORD_KEYS):
        raise TrackerRefused("record keys %s, expected %s"
                             % (sorted(rec), sorted(RECORD_KEYS)))
    prov = rec["provenance"]
    missing = [k for k in PROVENANCE_KEYS if k not in prov]
    if missing:
        raise TrackerRefused("record %s provenance lacks %s"
                             % (rec["id"], missing))
    for k in ("source", "query"):
        if not prov[k]:
            raise TrackerRefused("record %s provenance %s is empty"
                                 % (rec["id"], k))
    if not _DATE.match(str(prov["pull_date"])):
        raise TrackerRefused("record %s pull_date not YYYY-MM-DD"
                             % rec["id"])
    if not isinstance(prov["filters_applied"], list):
        raise TrackerRefused("record %s filters_applied is not a list"
                             % rec["id"])
    if not isinstance(prov["dropped"], bool):
        raise TrackerRefused("record %s dropped is not a bool" % rec["id"])
    if prov["dropped"] and not prov["drop_rule"]:
        raise TrackerRefused("record %s is dropped with no drop_rule; every "
                             "dropped record carries its rule" % rec["id"])
    if not prov["dropped"] and prov["drop_rule"]:
        raise TrackerRefused("record %s carries a drop_rule and is not "
                             "dropped" % rec["id"])
    if prov["dropped"]:
        return
    for m in cfg["metrics"]:
        fields = [m["name"]] + ([m["physical"]["field"]]
                                if m.get("physical") else [])
        for f in fields:
            v = rec["values"].get(f)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or \
                    not math.isfinite(v):
                raise TrackerRefused(
                    "kept record %s has no finite %s; excluding it would be "
                    "a drop with no rule" % (rec["id"], f))


# ------------------------------------------------------------- one run

def compute_run(cfg, records, period, run_at):
    """One run entry. Not yet chained or scheduled; append_run does that."""
    cfg = validate_config(cfg)
    if not _DATE.match(str(run_at)):
        raise TrackerRefused("run_at not YYYY-MM-DD")
    if run_at < cfg["declared"]:
        raise TrackerRefused(
            "run dated %s precedes the config's declared date %s: segments "
            "and metrics are declared before run 1" % (run_at,
                                                       cfg["declared"]))
    ids = [r.get("id") for r in records]
    if len(set(ids)) != len(ids):
        raise TrackerRefused("duplicate record ids in one pull")
    for r in records:
        validate_record(r, cfg)

    axes_out = {}
    for aname, axis in cfg["axes"].items():
        ref = reference_for(cfg, aname)
        seg_kept = {s: [] for s in axis["segments"]}
        seg_dropped = {s: 0 for s in axis["segments"]}
        unassigned = {"kept": 0, "dropped": 0}
        for r in records:
            s = assign(r, aname, axis)
            dropped = r["provenance"]["dropped"]
            if s is None:
                unassigned["dropped" if dropped else "kept"] += 1
            elif dropped:
                seg_dropped[s] += 1
            else:
                seg_kept[s].append(r)
        axis_kept = sum(len(v) for v in seg_kept.values())   # [CHOICE 2]
        segs = {}
        for s in axis["segments"]:
            kept = seg_kept[s]
            nk, nd = len(kept), seg_dropped[s]
            metrics = {}
            for m in cfg["metrics"]:
                vals = [r["values"][m["name"]] for r in kept]
                st = segment_stats(vals, cfg["min_n"])
                if m.get("physical"):
                    if st["state"] == INSUFFICIENT:
                        g4 = {"state": INSUFFICIENT, "value": None,
                              "physical_mean": None}
                    else:
                        phys = [r["values"][m["physical"]["field"]]
                                for r in kept]
                        sp = sum(phys)
                        g4 = {"state": None,
                              "value": (sum(vals) / sp) if sp > 0 else None,
                              "physical_mean": sp / len(phys),
                              "per": m["physical"]["unit"]}
                else:
                    g4 = {"state": NOT_DECLARED, "value": None,
                          "physical_mean": None}
                st["g4"] = g4
                metrics[m["name"]] = st
            sample_share = (nk / axis_kept) if axis_kept else None
            pop_share = None
            if ref is not None and s in (ref.get("shares") or {}):
                pop_share = float(ref["shares"][s])
            segs[s] = {
                "n_kept": nk, "n_dropped": nd,
                "g3_dropped_share": (nd / (nd + nk)) if (nd + nk) else None,
                "sample_share": sample_share,
                "population_share": pop_share,
                "g2": share_gap(sample_share, pop_share),
                "metrics": metrics,
            }
        axes_out[aname] = {
            "version": axis["version"], "dated": axis["dated"],
            "def_hash": def_hash(axis),
            "population_reference": ({"name": ref["name"],
                                      "date": ref["date"]}
                                     if ref else None),
            "unassigned": unassigned,
            "segments": segs,
        }
    prov = [dict(id=r["id"], **{k: r["provenance"][k]
                                for k in PROVENANCE_KEYS})
            for r in records]
    return {
        "run_label": period,
        "run_at": run_at,
        "config_version": cfg["config_version"],
        "config_declared": cfg["declared"],
        "interval": cfg["schedule"]["interval"],
        "interval_source": cfg["_interval_source"],
        "min_n": cfg["min_n"],
        "metrics": cfg["metrics"],
        "metrics_hash": metrics_hash(cfg),
        "n_records": len(records),
        "n_dropped": sum(1 for r in records if r["provenance"]["dropped"]),
        "dropped_log": [{"id": r["id"],
                         "drop_rule": r["provenance"]["drop_rule"]}
                        for r in records if r["provenance"]["dropped"]],
        "provenance": prov,
        "axes": axes_out,
    }


# ------------------------------------------------------------- schedule

def _parse_period(label, interval):
    if interval == "quarterly":
        m = re.match(r"^(\d{4})Q([1-4])$", label)
        if m:
            return int(m.group(1)) * 12 + (int(m.group(2)) - 1) * 3
    elif interval == "monthly":
        m = re.match(r"^(\d{4})-(0[1-9]|1[0-2])$", label)
        if m:
            return int(m.group(1)) * 12 + int(m.group(2)) - 1
    elif interval == "annual":
        m = re.match(r"^(\d{4})$", label)
        if m:
            return int(m.group(1)) * 12
    raise TrackerRefused("period %r is not a %s label" % (label, interval))


def _format_period(months, interval):
    y, mo = divmod(months, 12)
    if interval == "quarterly":
        return "%dQ%d" % (y, mo // 3 + 1)
    if interval == "monthly":
        return "%d-%02d" % (y, mo + 1)
    return "%d" % y


def next_period(label, interval):
    return _format_period(_parse_period(label, interval) + INTERVALS[interval],
                          interval)


# ------------------------------------------------------------- run log

def _log_bytes(path):
    if not os.path.exists(path):
        return b""
    with open(path, "rb") as fh:
        return fh.read()


def read_log(path):
    raw = _log_bytes(path)
    return [json.loads(l) for l in raw.decode("utf-8").splitlines() if l]


def verify_log(path):
    """(ok, problems). Each entry's prev_log_sha256 is the sha256 of every
    byte before its line."""
    raw = _log_bytes(path)
    problems = []
    pos = 0
    for i, line in enumerate(raw.split(b"\n")):
        if not line:
            pos += 1
            continue
        entry = json.loads(line.decode("utf-8"))
        want = hashlib.sha256(raw[:pos]).hexdigest()
        if entry.get("prev_log_sha256") != want:
            problems.append("entry %d (%s): prev_log_sha256 does not match "
                            "the bytes before it"
                            % (i, entry.get("run_label")))
        pos += len(line) + 1
    return (not problems), problems


def append_run(path, entry):
    """Append, never overwrite. Refuses a period already logged and a
    silent segment-definition change; stamps schedule status and chain."""
    ok, problems = verify_log(path)
    if not ok:
        raise TrackerRefused("run log fails its chain check: "
                             + "; ".join(problems))
    log = read_log(path)
    if any(e["run_label"] == entry["run_label"] for e in log):
        raise TrackerRefused("period %s is already in the log; runs are "
                             "appended, never overwritten"
                             % entry["run_label"])
    interval = entry["interval"]
    _parse_period(entry["run_label"], interval)
    if log:
        last = log[-1]
        for aname, ax in entry["axes"].items():
            prev = last["axes"].get(aname)
            if prev and prev["def_hash"] != ax["def_hash"] and \
                    prev["version"] == ax["version"]:
                raise TrackerRefused(
                    "axis %r: segment definitions changed under the same "
                    "version label %r. A change needs a new dated version"
                    % (aname, ax["version"]))
        if last["metrics_hash"] != entry["metrics_hash"] and \
                last["config_version"] == entry["config_version"]:
            raise TrackerRefused(
                "metric declarations changed under the same config_version "
                "%r" % entry["config_version"])
        expected = next_period(last["run_label"], last["interval"]) \
            if last["interval"] == interval else None
        if expected == entry["run_label"]:
            status = {"status": "ON_SCHEDULE"}
        else:
            status = {"status": "OFF_SCHEDULE", "expected": expected,
                      "last": last["run_label"]}
    else:
        status = {"status": "FIRST_RUN"}
    raw = _log_bytes(path)
    out = dict(entry)
    out["schedule_status"] = status
    out["prev_log_sha256"] = hashlib.sha256(raw).hexdigest()
    line = json.dumps(out, sort_keys=True, ensure_ascii=True) + "\n"
    if raw and not raw.endswith(b"\n"):
        raise TrackerRefused("run log does not end with a newline")
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(line)
    return out


# ------------------------------------------------------------- gauges

def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def gauges(log):
    """Series across runs. {axis: {segment: [point, ...]}} plus deltas.
    A delta across a definition or metric change is CROSS_VERSION."""
    out = {}
    for i, e in enumerate(log):
        prev = log[i - 1] if i else None
        for aname, ax in e["axes"].items():
            pax = prev["axes"].get(aname) if prev else None
            comparable = None
            why = None
            if prev is not None:
                if pax is None or pax["def_hash"] != ax["def_hash"]:
                    comparable, why = False, "segment definitions %s -> %s" % (
                        pax["version"] if pax else "absent", ax["version"])
                elif prev["metrics_hash"] != e["metrics_hash"]:
                    comparable, why = False, "metric declarations changed"
                else:
                    comparable = True
            for sname, seg in ax["segments"].items():
                point = {"run": e["run_label"], "version": ax["version"],
                         "g2": seg["g2"], "g3": seg["g3_dropped_share"],
                         "n_kept": seg["n_kept"], "g1": {}, "g4": {},
                         "median": {}}
                for mname, st in seg["metrics"].items():
                    point["g1"][mname] = (st["mean_minus_median"]
                                          if st["state"] is None
                                          else st["state"])
                    point["median"][mname] = st["median"]
                    g4 = st["g4"]
                    point["g4"][mname] = (g4["value"] if g4["state"] is None
                                          else g4["state"])
                if prev is None:
                    point["delta"] = None
                elif not comparable:
                    point["delta"] = {"state": CROSS_VERSION, "why": why}
                else:
                    pseg = pax["segments"].get(sname)
                    point["delta"] = _delta(pseg, seg) if pseg else {
                        "state": CROSS_VERSION, "why": "segment absent"}
                out.setdefault(aname, {}).setdefault(sname, []).append(point)
    return out


def _delta(pseg, seg):
    d = {"state": None, "g1": {}, "g2": None, "g3": None, "g4_drift": {}}
    for mname, st in seg["metrics"].items():
        pst = pseg["metrics"].get(mname)
        a = pst["mean_minus_median"] if pst else None
        b = st["mean_minus_median"]
        d["g1"][mname] = (b - a) if _num(a) and _num(b) else INSUFFICIENT \
            if (st["state"] or (pst and pst["state"])) else None
        g4a, g4b = (pst["g4"] if pst else None), st["g4"]
        if g4b["state"] == NOT_DECLARED:
            d["g4_drift"][mname] = NOT_DECLARED
        elif g4a and g4a["state"] is None and g4b["state"] is None and \
                pst["mean"] and g4a["physical_mean"]:
            d["g4_drift"][mname] = ((st["mean"] / pst["mean"]) /
                                    (g4b["physical_mean"] /
                                     g4a["physical_mean"]) - 1.0)
        else:
            d["g4_drift"][mname] = INSUFFICIENT
    a, b = pseg["g2"], seg["g2"]
    d["g2"] = (b - a) if _num(a) and _num(b) else (
        UNRATED if UNRATED in (a, b) else None)
    a, b = pseg["g3_dropped_share"], seg["g3_dropped_share"]
    d["g3"] = (b - a) if _num(a) and _num(b) else None
    return d


# ------------------------------------------------------------- render

def _f(x, w=10, p=3):
    if x is None:
        return "%*s" % (w, "--")
    if isinstance(x, str):
        return "%*s" % (w, x[:w])
    return "%*.*f" % (w, p, x)


def render_gauges(log):
    lines = ["moving-mean-tracker: gauges over %d run(s)" % len(log),
             "STATUS: PROPOSED instrument. Fixture data is synthetic; "
             "nothing here measures a population.",
             "UNRATED, INSUFFICIENT_SAMPLE, NOT_DECLARED and CROSS_VERSION "
             "are states, not zeros.", ""]
    if not log:
        lines.append("(empty log)")
        return "\n".join(lines)
    g = gauges(log)
    for aname in sorted(g):
        ref = log[-1]["axes"][aname]["population_reference"]
        lines.append("axis %s   population reference: %s" % (
            aname, "%s (%s)" % (ref["name"], ref["date"]) if ref
            else "none named and dated -> G2 UNRATED"))
        for sname in sorted(g[aname]):
            lines.append("  segment %s" % sname)
            lines.append("    %-8s %-10s %6s %10s %10s %10s %10s %10s" % (
                "run", "ver", "n", "G1", "median", "G2", "G3", "G4"))
            for p in g[aname][sname]:
                mname = sorted(p["g1"])[0]
                lines.append("    %-8s %-10s %6d %s %s %s %s %s" % (
                    p["run"], p["version"][:10], p["n_kept"],
                    _f(p["g1"][mname], 10, 1), _f(p["median"][mname], 10, 1),
                    _f(p["g2"]), _f(p["g3"]), _f(p["g4"][mname], 10, 2)))
                dl = p["delta"]
                if dl and dl["state"] == CROSS_VERSION:
                    lines.append("             delta: CROSS_VERSION (%s), "
                                 "not compared" % dl["why"])
        lines.append("")
    lines.append("schedule:")
    for e in log:
        st = e.get("schedule_status", {})
        lines.append("  %-8s %s%s" % (
            e["run_label"], st.get("status"),
            "  expected %s" % st["expected"] if st.get("expected") else ""))
    return "\n".join(lines)


# ------------------------------------------------------------- cli

class _ArgRefused(Exception):
    pass


class _QuietParser(argparse.ArgumentParser):
    """argparse that raises instead of printing usage and exiting, so a
    flag passed where a path belongs is refused with rc 2 by main()."""

    def error(self, message):
        raise _ArgRefused(message)


def _parser():
    ap = _QuietParser(prog="tracker.py", add_help=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--validate", metavar="CONFIG")
    g.add_argument("--run", metavar="CONFIG")
    g.add_argument("--gauges", metavar="LOG")
    g.add_argument("--verify", metavar="LOG")
    g.add_argument("--choices", action="store_true")
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--period")
    ap.add_argument("--run-at")
    ap.add_argument("--log")
    ap.add_argument("--fixture", metavar="KNOBS.json")
    return ap


def main(argv):
    try:
        args = _parser().parse_args(argv)
    except _ArgRefused as exc:
        print("refused: %s" % exc)
        print(__doc__.split("CLI:")[1].strip())
        return 2
    if args.selftest:
        print("tracker.py has no selftest; run: python3 test_tracker.py")
        return 2
    if args.choices:
        for n in sorted(CHOICES):
            print("[CHOICE %d] %s" % (n, CHOICES[n]))
        return 0
    for p in (args.validate, args.run, args.gauges, args.verify, args.log,
              args.fixture):
        if p is not None and p.startswith("--"):
            print("refused: path starts with '--': %r" % p)
            return 2
    try:
        if args.validate:
            with open(args.validate, encoding="utf-8") as fh:
                validate_config(json.load(fh))
            print("config accepted: %s" % args.validate)
            return 0
        if args.verify:
            ok, problems = verify_log(args.verify)
            print("chain %s over %d entries" % (
                "intact" if ok else "BROKEN", len(read_log(args.verify))))
            for pr in problems:
                print("  " + pr)
            return 0 if ok else 1
        if args.gauges:
            print(render_gauges(read_log(args.gauges)))
            return 0
        if not (args.period and args.run_at and args.log):
            print("--run needs --period, --run-at and --log")
            return 2
        from provider import FixtureProvider
        knobs = {}
        if args.fixture:
            with open(args.fixture, encoding="utf-8") as fh:
                knobs = json.load(fh)
        with open(args.run, encoding="utf-8") as fh:
            cfg = json.load(fh)
        recs = FixtureProvider(**knobs).pull(args.period, args.run_at)
        entry = append_run(args.log, compute_run(cfg, recs, args.period,
                                                 args.run_at))
        print("appended %s (%s) to %s: %d records, %d dropped"
              % (entry["run_label"], entry["schedule_status"]["status"],
                 args.log, entry["n_records"], entry["n_dropped"]))
        return 0
    except TrackerRefused as exc:
        print("refused: %s" % exc)
        return 1


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    sys.exit(main(sys.argv[1:]))
