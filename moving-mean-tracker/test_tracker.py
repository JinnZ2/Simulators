"""
moving-mean-tracker/test_tracker.py -- fixtures for tracker.py and
provider.py.

SELF-GRADED: these tests and the module they test share an author. A
passing run shows that the code does what this author wrote it to do. It
is not an independent check that the instrument measures what it claims
to measure.

The four tests the dispatch names come first:
  1. A tail added to the top segment only: G1 widens, the median does not
     move, and the other segments on that axis are unchanged.
  2. A segment dropped by a filter: G3 rises for that segment only.
  3. A segment definition changed between runs: the change is flagged
     CROSS_VERSION and no delta is computed. The same change under an
     unchanged version label is refused.
  4. A missing population reference: G2 is UNRATED, never 0.
Then the refusals and states the rules require.

Run: python3 test_tracker.py
"""

from __future__ import annotations

import ast
import copy
import io
import json
import os
import sys
import tempfile
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import tracker as T  # noqa: E402
from provider import FixtureProvider  # noqa: E402

RESULTS = []


def check(name, ok):
    RESULTS.append((name, bool(ok)))


def cfg():
    with open(os.path.join(HERE, "config.example.json"),
              encoding="utf-8") as fh:
        return json.load(fh)


def run(c, knobs, period, run_at):
    return T.compute_run(c, FixtureProvider(**knobs).pull(period, run_at),
                         period, run_at)


def refused(fn, *a, **k):
    try:
        fn(*a, **k)
    except T.TrackerRefused as exc:
        return str(exc)
    return None


def two_runs(knobs_a, knobs_b, cfg_a=None, cfg_b=None):
    d = tempfile.mkdtemp()
    log = os.path.join(d, "log.jsonl")
    T.append_run(log, run(cfg_a or cfg(), knobs_a, "2026Q4", "2026-10-08"))
    T.append_run(log, run(cfg_b or cfg(), knobs_b, "2027Q1", "2027-01-08"))
    return log, T.gauges(T.read_log(log))


def tests():
    base = cfg()

    # ---- 1. tail on the top segment only -> G1 widens, median unchanged
    log, g = two_runs({}, {"tail": {"band": "high", "top_fraction": 0.1,
                                    "factor": 10}})
    hi = g["band"]["high"]
    check("1 tail: G1 for high widens",
          hi[1]["g1"]["consumption"] > hi[0]["g1"]["consumption"] + 1000)
    check("1 tail: median for high unchanged",
          hi[1]["median"]["consumption"] == hi[0]["median"]["consumption"])
    check("1 tail: delta G1 for high is positive and comparable",
          hi[1]["delta"]["state"] is None and
          hi[1]["delta"]["g1"]["consumption"] > 0)
    for s in ("low", "mid"):
        pts = g["band"][s]
        check("1 tail: %s on the band axis unchanged (G1 delta 0.0)" % s,
              pts[1]["delta"]["g1"]["consumption"] == 0.0 and
              pts[1]["median"] == pts[0]["median"])
    check("1 tail: G4 (dollars per kcal) rises for high, physical unchanged",
          hi[1]["g4"]["consumption"] > hi[0]["g4"]["consumption"] and
          hi[1]["delta"]["g4_drift"]["consumption"] > 0)

    # ---- 2. a segment dropped by a filter -> G3 rises for that one only
    log, g = two_runs({}, {"drop": {"band": "low", "fraction": 0.5,
                                    "rule": "below_floor_as_noise"}})
    low = g["band"]["low"]
    check("2 drop: G3 for low rises from 0.0 to 0.5",
          low[0]["g3"] == 0.0 and low[1]["g3"] == 0.5 and
          low[1]["delta"]["g3"] == 0.5)
    check("2 drop: G3 for mid and high stays 0.0",
          all(g["band"][s][1]["g3"] == 0.0 and
              g["band"][s][1]["delta"]["g3"] == 0.0 for s in ("mid", "high")))
    entry = T.read_log(log)[1]
    check("2 drop: every dropped record is logged with its rule",
          len(entry["dropped_log"]) == 30 and
          all(d["drop_rule"] == "below_floor_as_noise"
              for d in entry["dropped_log"]))
    check("2 drop: the filter is in each record's filters_applied",
          all("drop:below_floor_as_noise" in p["filters_applied"]
              for p in entry["provenance"]))
    check("2 drop: removing low's cheapest half moves its median up",
          low[1]["median"]["consumption"] > low[0]["median"]["consumption"])
    log, g = two_runs({}, {"drop": {"band": "high", "fraction": 1.0,
                                    "rule": "top_band_removed"}})
    h1 = g["band"]["high"][1]
    check("2 drop: a whole segment dropped -> G3 1.0 and "
          "INSUFFICIENT_SAMPLE, not a value",
          h1["g3"] == 1.0 and h1["n_kept"] == 0 and
          h1["g1"]["consumption"] == T.INSUFFICIENT and
          h1["g4"]["consumption"] == T.INSUFFICIENT)
    check("2 drop: G1 delta into an INSUFFICIENT_SAMPLE segment is not a "
          "number", h1["delta"]["g1"]["consumption"] == T.INSUFFICIENT)

    # ---- 3. segment definition changed between runs -> flagged
    changed = copy.deepcopy(base)
    changed["axes"]["band"]["segments"]["mid"] = {
        "field": "band_label", "equals": "middle"}
    msg = refused(two_runs, {}, {}, base, changed)
    check("3 version: a changed definition under the same version label "
          "is refused", msg is not None and "same version label" in msg)
    changed["axes"]["band"]["version"] = "band-v2"
    changed["axes"]["band"]["dated"] = "2027-01-02"
    log, g = two_runs({}, {}, base, changed)
    for s in ("low", "mid", "high"):
        dl = g["band"][s][1]["delta"]
        check("3 version: %s delta across band-v1 -> band-v2 is "
              "CROSS_VERSION with no numbers" % s,
              dl["state"] == T.CROSS_VERSION and "g1" not in dl and
              "band-v1 -> band-v2" in dl["why"])
    check("3 version: an axis whose definitions did not change stays "
          "comparable", g["region"]["north"][1]["delta"]["state"] is None)
    relabel = copy.deepcopy(base)
    relabel["axes"]["band"]["version"] = "band-v1b"
    log, g = two_runs({}, {}, base, relabel)
    check("3 version: a relabel that changes no rule is still comparable "
          "(the hash covers rules, not the label)",
          g["band"]["low"][1]["delta"]["state"] is None)
    check("3 version: the render prints CROSS_VERSION and 'not compared'",
          "CROSS_VERSION" in T.render_gauges(T.read_log(two_runs(
              {}, {}, base, changed)[0])) and "not compared" in
          T.render_gauges(T.read_log(two_runs({}, {}, base, changed)[0])))
    metric_change = copy.deepcopy(base)
    metric_change["metrics"][0]["unit"] = "EUR"
    check("3 version: a metric change under the same config_version is "
          "refused", refused(two_runs, {}, {}, base, metric_change)
          is not None)
    metric_change["config_version"] = "v2"
    log, g = two_runs({}, {}, base, metric_change)
    check("3 version: a metric change under a new config_version is "
          "CROSS_VERSION", g["band"]["low"][1]["delta"]["state"] ==
          T.CROSS_VERSION and "metric" in g["band"]["low"][1]["delta"]["why"])

    # ---- 4. missing population reference -> UNRATED, never 0
    e = run(base, {}, "2026Q4", "2026-10-08")
    check("4 reference: region has no reference -> G2 UNRATED on every "
          "segment",
          all(seg["g2"] == T.UNRATED
              for seg in e["axes"]["region"]["segments"].values()))
    check("4 reference: UNRATED is not 0 and not None",
          e["axes"]["region"]["segments"]["north"]["g2"] not in (0, 0.0,
                                                                  None))
    check("4 reference: band has a reference -> G2 is a number",
          all(isinstance(seg["g2"], float)
              for seg in e["axes"]["band"]["segments"].values()))
    for missing in ("name", "date"):
        c2 = copy.deepcopy(base)
        del c2["population_reference"]["band"][missing]
        e2 = run(c2, {}, "2026Q4", "2026-10-08")
        check("4 reference: a reference with no %s is not a reference -> "
              "UNRATED" % missing,
              e2["axes"]["band"]["segments"]["low"]["g2"] == T.UNRATED and
              e2["axes"]["band"]["population_reference"] is None)
    c3 = copy.deepcopy(base)
    c3["population_reference"]["band"]["shares"] = {"low": 0.5, "mid": 0.5}
    e3 = run(c3, {}, "2026Q4", "2026-10-08")
    check("4 reference: a segment the reference gives no share for -> "
          "UNRATED for that segment only",
          e3["axes"]["band"]["segments"]["high"]["g2"] == T.UNRATED and
          isinstance(e3["axes"]["band"]["segments"]["low"]["g2"], float))
    check("4 reference: a measured 0.0 gap is reachable and is a number",
          T.share_gap(0.25, 0.25) == 0.0 and
          T.share_gap(0.25, None) == T.UNRATED)
    check("4 reference: G2 on the fixture equals sample minus pop share",
          abs(e["axes"]["band"]["segments"]["high"]["g2"] -
              (1 / 3 - 0.2)) < 1e-12)

    # ---- min_n -> INSUFFICIENT_SAMPLE
    small = copy.deepcopy(base)
    small["min_n"] = 61
    e = run(small, {}, "2026Q4", "2026-10-08")
    st = e["axes"]["band"]["segments"]["low"]["metrics"]["consumption"]
    check("min_n: n 60 under min_n 61 -> INSUFFICIENT_SAMPLE, no mean",
          st["state"] == T.INSUFFICIENT and st["mean"] is None and
          st["n"] == 60)
    check("min_n: region segments (n 90) still compute under min_n 61",
          e["axes"]["region"]["segments"]["north"]["metrics"][
              "consumption"]["state"] is None)

    # ---- declared before run 1
    for key in ("metrics", "axes"):
        c = copy.deepcopy(base)
        del c[key]
        msg = refused(T.validate_config, c)
        check("declare: config without %s is refused" % key,
              msg is not None and key in msg)
    check("declare: a run dated before the config's declared date is "
          "refused",
          refused(run, base, {}, "2026Q3", "2026-09-30") is not None)
    nodefault = copy.deepcopy(base)
    del nodefault["schedule"]
    e = run(nodefault, {}, "2026Q4", "2026-10-08")
    check("declare: a missing interval reads quarterly and is recorded as "
          "a default", e["interval"] == "quarterly" and
          e["interval_source"] == "default")
    bad_sum = copy.deepcopy(base)
    bad_sum["population_reference"]["band"]["shares"]["high"] = 0.5
    check("declare: reference shares that do not sum to 1 are refused, "
          "not UNRATED", refused(T.validate_config, bad_sum) is not None)

    # ---- records and provenance
    recs = FixtureProvider().pull("2026Q4", "2026-10-08")
    r = copy.deepcopy(recs)
    r[0]["provenance"]["dropped"] = True
    check("record: dropped with no drop_rule is refused",
          refused(T.compute_run, base, r, "2026Q4", "2026-10-08")
          is not None)
    r = copy.deepcopy(recs)
    del r[0]["values"]["consumption"]
    check("record: a kept record with no metric value is refused (a "
          "silent exclusion is a drop with no rule)",
          refused(T.compute_run, base, r, "2026Q4", "2026-10-08")
          is not None)
    r = copy.deepcopy(recs)
    r[0]["provenance"]["dropped"] = True
    r[0]["provenance"]["drop_rule"] = "x"
    del r[0]["values"]["consumption"]
    check("record: a dropped record with no value is accepted (it carries "
          "its rule)",
          refused(T.compute_run, base, r, "2026Q4", "2026-10-08") is None)
    for k in T.PROVENANCE_KEYS:
        r = copy.deepcopy(recs)
        del r[3]["provenance"][k]
        check("record: provenance without %s is refused" % k,
              refused(T.compute_run, base, r, "2026Q4", "2026-10-08")
              is not None)
    overlap = copy.deepcopy(base)
    overlap["axes"]["band"]["segments"]["low_again"] = {
        "field": "band_label", "equals": "low"}
    check("record: a record matching two segments on one axis is refused",
          refused(run, overlap, {}, "2026Q4", "2026-10-08") is not None)
    e = run(base, {"omit_region": True}, "2026Q4", "2026-10-08")
    check("record: records without the region attr are counted UNASSIGNED, "
          "and the region shares go undefined (None), not 0",
          e["axes"]["region"]["unassigned"] == {"kept": 180, "dropped": 0}
          and e["axes"]["region"]["segments"]["north"]["sample_share"]
          is None)

    # ---- run log: append-only, chained, scheduled
    d = tempfile.mkdtemp()
    log = os.path.join(d, "log.jsonl")
    T.append_run(log, run(base, {}, "2026Q4", "2026-10-08"))
    check("log: the same period again is refused, never overwritten",
          refused(T.append_run, log, run(base, {}, "2026Q4", "2026-10-09"))
          is not None and len(T.read_log(log)) == 1)
    T.append_run(log, run(base, {}, "2027Q2", "2027-04-08"))
    st = T.read_log(log)[1]["schedule_status"]
    check("log: a skipped quarter is accepted and stamped OFF_SCHEDULE with "
          "the expected period", st == {"status": "OFF_SCHEDULE",
                                        "expected": "2027Q1",
                                        "last": "2026Q4"})
    ok, _ = T.verify_log(log)
    check("log: the chain verifies", ok)
    with open(log, "rb") as fh:
        raw = fh.read()
    with open(log, "wb") as fh:
        fh.write(raw.replace(b'"n_dropped": 0', b'"n_dropped": 1', 1))
    ok, problems = T.verify_log(log)
    check("log: an edit to an earlier entry breaks the chain", not ok and
          problems)
    check("log: appending to a broken chain is refused",
          refused(T.append_run, log, run(base, {}, "2027Q3", "2027-07-08"))
          is not None)
    check("log: next_period wraps the year",
          T.next_period("2026Q4", "quarterly") == "2027Q1" and
          T.next_period("2026-12", "monthly") == "2027-01" and
          T.next_period("2026", "annual") == "2027")

    # ---- G4 when no physical unit is declared
    nophys = copy.deepcopy(base)
    del nophys["metrics"][0]["physical"]
    log, g = two_runs({}, {}, nophys, nophys)
    p = g["band"]["low"][1]
    check("G4: no physical unit declared -> NOT_DECLARED, not a number",
          p["g4"]["consumption"] == T.NOT_DECLARED and
          p["delta"]["g4_drift"]["consumption"] == T.NOT_DECLARED)
    log, g = two_runs({}, {"price_index": 1.25})
    p = g["band"]["mid"][1]
    check("G4: a price index of 1.25 with the physical quantity unchanged "
          "reads as a token drift of 0.25 while G1 also moves",
          abs(p["delta"]["g4_drift"]["consumption"] - 0.25) < 1e-12 and
          p["delta"]["g1"]["consumption"] != 0.0)

    # ---- quantile
    check("quantile: [1,2,3,4] median 2.5", T.quantile([1, 2, 3, 4], 0.5)
          == 2.5)
    check("quantile: empty -> None", T.quantile([], 0.5) is None)
    check("quantile: p90 of 1..5 is 4.6",
          abs(T.quantile([1, 2, 3, 4, 5], 0.9) - 4.6) < 1e-12)

    # ---- the provider stays dumb
    src = open(os.path.join(HERE, "provider.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(a.name for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.add(node.module)
    check("provider: imports no statistics module and not tracker",
          "statistics" not in imports and "tracker" not in imports)
    check("provider: every record has exactly id, attrs, values, provenance",
          all(sorted(x) == sorted(T.RECORD_KEYS) for x in recs))
    check("provider: no key in a record or its provenance names a "
          "statistic or a score",
          not any(k in ("mean", "median", "score", "share", "gap")
                  for x in recs for k in list(x) + list(x["provenance"])))
    check("provider: unknown knobs are refused",
          _raises(lambda: FixtureProvider(colour="red")))

    # ---- CLI
    with redirect_stdout(io.StringIO()):
        check("cli: --selftest refused with rc 2",
              T.main(["--selftest"]) == 2)
        d = tempfile.mkdtemp()
        cwd = os.getcwd()
        try:
            os.chdir(d)
            rc = T.main(["--run", os.path.join(HERE, "config.example.json"),
                         "--period", "2026Q4", "--run-at", "2026-10-08",
                         "--log", "--out"])
        finally:
            os.chdir(cwd)
    check("cli: a path starting with '--' is refused, no file written",
          rc == 2 and not os.path.exists(os.path.join(d, "--out")))

    # ---- output vocabulary
    sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
    import no_severity
    log, _ = two_runs({}, {"tail": {"band": "high", "top_fraction": 0.1,
                                    "factor": 10}}, base, changed)
    text = T.render_gauges(T.read_log(log))
    clean, hits = no_severity.check(text)
    check("render: no severity or interpretation vocabulary (%d hits)"
          % len(hits), clean)
    check("source: tracker.py and provider.py are ASCII",
          all(open(os.path.join(HERE, f), "rb").read().isascii()
              for f in ("tracker.py", "provider.py", "test_tracker.py")))
    for f in ("tracker.py", "provider.py", "test_tracker.py"):
        ast.parse(open(os.path.join(HERE, f)).read(), feature_version=(3, 9))
    check("source: parses under Python 3.9", True)


def _raises(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


if __name__ == "__main__":
    tests()
    failed = [n for n, ok in RESULTS if not ok]
    for n, ok in RESULTS:
        print("%s  %s" % ("PASS" if ok else "FAIL", n))
    print("checks: %d   failed: %d" % (len(RESULTS), len(failed)))
    sys.exit(1 if failed else 0)
