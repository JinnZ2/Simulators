#!/usr/bin/env python3
"""
test_descent_record.py -- the entry point for stability-trigger-envelope/.

REGRESSION on CONSTRUCTED fixtures: the checks below show the code still
does what it was written to do. They are not validation; nothing here
reads a real descent. Exit 0 all checks pass, 1 any check fails, per
EXIT_CONTRACT.md.

CC0. stdlib only. Parses under Python 3.9.
"""

import ast
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import descent_record as D            # noqa: E402
import no_severity                    # noqa: E402

CHECKS = []

# Digest of the shipped log prefix, seq 1-16. An in-place edit of any of
# these entries changes it; an appended entry does not.
PINNED_PREFIX_LEN = 16
PINNED_PREFIX_SHA256 = (
    "2cb4c329cb27e9a0b0f5f1dd86631d53ece140ec1c56049120199203b8405405")


def ok(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))


current, log = D.load_thresholds()

# --- the order's fixtures fire, and the other side of each gate fires ------

for fid, desc, exp, got, det in D.run_fixtures(current):
    ok("%s %s -> %s" % (fid, desc, exp), exp == got, "got %s" % got)

labels = set(got for _, _, _, got, _ in D.run_fixtures(current))
ok("classify reaches six distinct labels across fixtures",
   {D.GEOMETRIC_CAB_MODE, D.TRAILER_ROLL_RISK, D.TRAILER_CHANNEL_ABSENT,
    D.NOT_EVALUABLE, D.OUT_OF_ENVELOPE, D.NEITHER_MODE} <= labels)

# --- every reading carries the threshold status ----------------------------

for fid, _, _, _, det in D.run_fixtures(current):
    if isinstance(det, D.Reading):
        ok("%s reading carries threshold status PLACEHOLDER" % fid,
           det.thresholds == "PLACEHOLDER", det.thresholds)

# --- thresholds: all PLACEHOLDER, append-only prefix pinned ---------------

ok("every shipped threshold is PLACEHOLDER",
   all(e["status"] == "PLACEHOLDER" for e in log))
prefix = json.dumps(log[:PINNED_PREFIX_LEN], sort_keys=True).encode()
ok("shipped log prefix (seq 1-16) unchanged",
   hashlib.sha256(prefix).hexdigest() == PINNED_PREFIX_SHA256)


def _load_mutated(mutate):
    with open(D.THRESHOLDS_PATH) as fh:
        data = json.load(fh)
    mutate(data)
    fd, p = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as fh:
        json.dump(data, fh)
    try:
        D.load_thresholds(p)
        return None
    except D.ThresholdFileError as exc:
        return str(exc)
    finally:
        os.remove(p)


def _append(data):
    data["log"].append(dict(data["log"][4], seq=len(data["log"]) + 1,
                            value=2.0, date="2099-01-01"))


def _skip_seq(data):
    data["log"][3]["seq"] = 99


def _bad_status(data):
    data["log"][0]["status"] = "GUESSED"


def _clock_over(data):
    data["log"].append(dict(data["log"][12], seq=len(data["log"]) + 1,
                            value=5.0))


ok("an appended entry loads and becomes current",
   _load_mutated(_append) is None)
ok("a broken seq is refused", _load_mutated(_skip_seq) is not None)
ok("an unknown status is refused", _load_mutated(_bad_status) is not None)
ok("clock tolerance at/over the phase window floor is refused",
   _load_mutated(_clock_over) is not None)

# --- relocation_tally counts, never scores --------------------------------

x5 = [f for f in D.fixtures() if f[0] == "X5"][0][3]
t = D.relocation_tally(x5, current)
ok("relocation_tally has no total or score key",
   not any(k in t for k in ("total", "score", "sum", "index")))
ok("by_event carries every declared event, zeros included",
   list(t["by_event"]) == list(D.DOWNSTREAM_EVENTS))
ok("by_event counts conserve records", sum(t["by_event"].values()) == len(x5))
ok("V2 bins: 0 | 1 | 2 | 3+ | UNMEASURED",
   [D.v2_bin(c, [1, 2, 3]) for c in (0, 1, 2, 3, 7, None)]
   == ["0", "1", "2", "3+", "3+", "UNMEASURED"])

# --- envelope_edge: every status reachable ---------------------------------

cab = D.constructed_trace(6.0, 8.0, 1)
trl = D.constructed_trace(0.6, 12.0, 2)
overlap = [D._rec("R", 30.0, cab, trl), D._rec("R", 32.0, None, None, ts=None),
           D._rec("R", 34.0, cab, trl)]
ok("ONSET_OVERLAP when a quiet run is at/above a fired speed",
   D.envelope_edge(overlap, "R")["status"] == D.ONSET_OVERLAP)
none_fired = [D._rec("Q", s, None, None, ts=None) for s in (25.0, 28.0, 31.0)]
e = D.envelope_edge(none_fired, "Q")
ok("NO_TRIGGER_OBSERVED gives a lower bound, not an onset",
   e["status"] == D.NO_TRIGGER_OBSERVED and "onset_mph" not in e
   and e["quiet_up_to_mph"] == 31.0)
mixed = [D._rec("M", 30.0, cab, trl, grade=9.0),
         D._rec("M", 31.0, cab, trl, grade=13.0, surface="dry"),
         D._rec("M", 26.0, None, None, ts=None)]
ok("mixed grade/surface on one road is reported, not pooled silently",
   set(D.envelope_edge(mixed, "M")["mixed_conditions"])
   == {"grade_pct", "surface_state"})
ok("INSUFFICIENT_RUNS is < 3, exactly",
   D.envelope_edge(overlap[:2], "R")["status"] == D.INSUFFICIENT_RUNS
   and D.envelope_edge(overlap, "R")["status"] != D.INSUFFICIENT_RUNS)

# --- CSV path reads the same as the constructed dict ----------------------

tmpd = tempfile.mkdtemp()
paths = []
for name, tr in (("cab", cab), ("trl", trl)):
    p = os.path.join(tmpd, name + ".csv")
    with open(p, "w") as fh:
        fh.write("# sync_ts=%r\n" % tr["sync_ts"])
        fh.write("t_s,roll_dps\n")
        for a, b in zip(tr["t"], tr["roll_dps"]):
            fh.write("%r,%r\n" % (a, b))
    paths.append(p)
r_dict = D.classify(D._rec("C", 34.0, cab, trl), current)
r_csv = D.classify(D._rec("C", 34.0, paths[0], paths[1]), current)
ok("CSV trace classifies as its dict source",
   r_dict.label == r_csv.label == D.GEOMETRIC_CAB_MODE
   and r_dict.evidence == r_csv.evidence)
for p in paths:
    os.remove(p)
os.rmdir(tmpd)

# --- record validation, sync rule ------------------------------------------

for bad in (dict(surface="slush"), dict(event="crash")):
    try:
        D._rec("V", 30.0, cab, trl, **bad)
        ok("record refuses %s" % bad, False)
    except ValueError:
        ok("record refuses %s" % bad, True)
nosync = dict(trl, sync_ts=None)
ok("missing sync mark -> NOT_EVALUABLE, not a shifted guess",
   D.classify(D._rec("S", 34.0, cab, nosync), current).label
   == D.NOT_EVALUABLE)
ok("no esp_event_ts -> NOT_EVALUABLE",
   D.classify(D._rec("S", 34.0, cab, trl, ts=None), current).label
   == D.NOT_EVALUABLE)

# --- render: deterministic, screens clean ----------------------------------

R = D.render()
ok("render is deterministic across calls", R == D.render())
h = no_severity.hits(R)
ok("render screens clean through no_severity (no exemption)", not h,
   str(h)[:200])
ok("render states REGRESSION and NOT_RUN",
   "REGRESSION" in R and "NOT_RUN" in R)

# --- module hygiene ----------------------------------------------------------

for fn in ("descent_record.py", "test_descent_record.py"):
    b = open(os.path.join(HERE, fn), "rb").read()
    ok("%s is ASCII" % fn, all(x < 128 for x in b))
    ast.parse(b.decode("ascii"), feature_version=(3, 9))
    ok("%s parses under 3.9" % fn, True)

p = subprocess.run([sys.executable, os.path.join(HERE, "descent_record.py"),
                    "--selftest"], capture_output=True)
ok("descent_record.py refuses --selftest with exit 2", p.returncode == 2)
p = subprocess.run([sys.executable, os.path.join(HERE, "descent_record.py")],
                   capture_output=True)
ok("descent_record.py runs with exit 0", p.returncode == 0)

# --- report ------------------------------------------------------------------

failed = [c for c in CHECKS if not c[1]]
for name, passed, detail in CHECKS:
    print("%s  %s%s" % ("PASS" if passed else "FAIL", name,
                        "" if passed or not detail else "  -- " + detail))
print("")
print("%d checks, %d passed, %d failed  (REGRESSION on CONSTRUCTED data)"
      % (len(CHECKS), len(CHECKS) - len(failed), len(failed)))
sys.exit(1 if failed else 0)
