#!/usr/bin/env python3
"""radio_log input checks (FINDER ROUND 3). CC0, stdlib only. Prints checks: N failed: M."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutoff_attribution as ca  # noqa: E402
ok = total = 0
def check(c, lab):
    global ok, total
    total += 1; ok += bool(c)
    if not c: print("FAIL:", lab)
SEG = [{"t_start": 0, "t_end": 2, "speaker": "user", "text": "the left axle"},
       {"t_start": 3, "t_end": 4, "speaker": "model", "text": "Go on."}]
L = ca.radio_to_log([{"t": 1.0, "dbm": -70, "network": "lte"}, {"t": 2.1, "dbm": -95, "network": "wifi"}])
check([e["kind"] for e in L] == ["rssi_dbm", "rssi_dbm", "network_handover"], "dBm rows + one handover")
check(all("flag" not in e for e in L if e["kind"] == "rssi_dbm"), "no dBm threshold: rows stay unflagged")
c = ca.attribute({"segments": SEG, "cut_marks": [{"t": 2.0}],
                  "radio_log": [{"t": 1.5, "dbm": -60, "network": "lte"}]})["cuts"][0]
check(c["status"] == "UNRESOLVED" and "NETWORK_LAG" in c["candidate_set"], "dBm alone: UNRESOLVED, NETWORK_LAG kept")
rl = [{"t": 1.0, "dbm": -60, "network": "lte"}, {"t": 2.2, "dbm": -90, "network": "wifi"}]
c = ca.attribute({"segments": SEG, "cut_marks": [{"t": 2.0}], "radio_log": rl,
                  "reference_checks": [{"hop": "transmission", "injected": "a", "observed": "a"}]})["cuts"][0]
check(c["status"] == "OBSERVED" and c["separated_by_evidence"] == "NETWORK_LAG", "handover through checked hop separates")
c = ca.attribute({"segments": SEG, "cut_marks": [{"t": 2.0}], "radio_log": rl})["cuts"][0]
check(c["status"] == "ESTIMATED" and c["separated_by_evidence"] is None, "handover through unchecked hop does not")
try:
    ca.radio_to_log([{"dbm": -60}]); check(False, "entry without t refused")
except (ValueError, KeyError):
    check(True, "entry without t refused")
check("radio_log" in ca.RADIO_SCHEMA and "dBm" in ca.RADIO_SCHEMA, "schema stated in module")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
