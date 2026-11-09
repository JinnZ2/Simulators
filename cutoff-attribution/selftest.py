#!/usr/bin/env python3
"""selftest for cutoff-attribution. CC0, stdlib only. Prints checks: N failed: M."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutoff_attribution as ca  # noqa: E402

ok = total = 0
def check(cond, label):
    global ok, total
    total += 1
    if cond:
        ok += 1
    else:
        print("FAIL:", label)

r = ca.attribute(json.load(open(os.path.join(HERE, "samples", "demo.json"))))
st = [c["status"] for c in r["cuts"]]
check(st == ["OBSERVED", "ESTIMATED", "UNRESOLVED"], "demo statuses %s" % st)
check(set(st) == set(ca.STATUSES), "all three statuses reached")
c0, c1, c2 = r["cuts"]
check(c0["separated_by_evidence"] == "NETWORK_LAG", "one OBSERVED candidate separates")
check(len(c0["candidate_set"]) > 1, "separated cut still lists the other candidates")
check(c1["separated_by_evidence"] is None and "UNRESOLVED" in c1["candidate_set"],
      "evidence through unchecked / failed hops does not separate; UNRESOLVED kept")
lv = {e["level"] for v in c1["evidence"].values() for e in v}
check({"RECORDED_VIA_UNVERIFIED_HOP", "RECORDED_VIA_FAILED_HOP"} <= lv,
      "log events through unchecked and failed hops are not OBSERVED")
check({"ENDPOINTING", "TRANSCRIPTION"} <= set(c1["candidate_set"]), "both recorded candidates kept in set")
# two hops checked -> two OBSERVED -> no single winner
two = {"segments": [{"t_start": 0, "t_end": 2, "speaker": "user", "text": "and the"},
                    {"t_start": 2.2, "t_end": 3, "speaker": "model", "text": "Yes?"}],
       "signal_log": [{"t": 1.9, "kind": "endpoint_fired"}, {"t": 2.0, "kind": "asr_error"}],
       "reference_checks": [{"hop": "encoding", "injected": "a", "observed": "a"},
                            {"hop": "decoding", "injected": "b", "observed": "b"}]}
r2 = ca.attribute(two)["cuts"][0]
check(r2["status"] == "ESTIMATED" and r2["separated_by_evidence"] is None,
      "two OBSERVED candidates (both hops checked) do not separate")
# same input, no reference checks -> nothing OBSERVED
two_nochk = dict(two, reference_checks=[])
check(all(e["level"] != "OBSERVED" for v in ca.attribute(two_nochk)["cuts"][0]["evidence"].values() for e in v),
      "no reference check -> no OBSERVED evidence")
check(all(c["record"]["chain_class"] in ("VIA_CHECKED_CHAIN", "VIA_UNVERIFIED_HOP", "VIA_FAILED_HOP")
          for c in r["cuts"]), "every cut record has a chain class; none DIRECT")
check(r["tool_hop"]["check"] == "CHECKED", "tool self-check on a known cut passes")
saved = ca.GAP_S
ca.GAP_S = -1.0
check(ca._self_check()["check"] == "CHECK_FAILED", "self-check fails when the detector is broken")
ca.GAP_S = saved
check(set(["value", "native_confidence", "role", "modality", "units", "correlation_group",
           "timestamp", "provenance", "chain"]) <= set(c0["record"]), "record carries SubstrateReading fields + chain")
d0 = r["attribution_displacement"][0]
check(d0["term"] == "Interiority substitution" and (d0["term_source"].startswith("Cross-Domain-Toolkit")
      or d0["term_source"] == "TERM_NOT_CHECKED"), "displacement cites a toolkit term with its source")
care = ca.attribute({"segments": [{"t_start": 0, "t_end": 1, "speaker": "model", "text": "Take your time to think."}]})
check(care["attribution_displacement"][0]["term"] == "Care inversion", "care-framed displacement -> Care inversion")
src = open(os.path.join(HERE, "cutoff_attribution.py")).read()
check('"Interiority substitution"' in src and "def toolkit_terms" in src, "terms are read from the toolkit, names quoted")
check(c2["candidate_set"] == ["UNRESOLVED"], "unflagged measurement is not evidence")
check(c1["origin"] == "DETECTED" and c0["origin"] == "USER_TAGGED", "tagged and detected cuts")
check(len(r["attribution_displacement"]) == 1 and "trailed off" in r["attribution_displacement"][0]["span"],
      "ATTRIBUTION_DISPLACEMENT flagged once")
bad = ("USER", "USER_COGNITION", "DISTRACTION", "ATTENTION", "FATIGUE")
check(not any(b in ca.CANDIDATES for b in bad), "user cognition is not a candidate")
check(all(c in ca.CANDIDATES and c != "UNRESOLVED" for c, _ in ca.LOG_KINDS.values()), "every log kind maps to a named candidate")
none = ca.attribute({"segments": [{"t_start": 0, "t_end": 1, "speaker": "user", "text": "Done."},
                                  {"t_start": 3, "t_end": 4, "speaker": "model", "text": "Ok."}]})
check(none["cuts"] == [], "terminal punctuation + slow reply -> no detected cut")
ov = ca.attribute({"segments": [{"t_start": 0, "t_end": 2, "speaker": "user", "text": "so the"},
                                {"t_start": 1.5, "t_end": 3, "speaker": "model", "text": "Yes?"}]})
check(ov["cuts"][0]["status"] == "ESTIMATED" and "MODEL_READ" in ov["cuts"][0]["candidate_set"],
      "overlap -> ESTIMATED MODEL_READ, not OBSERVED")
neutral = ca.attribute({"segments": [{"t_start": 0, "t_end": 1, "speaker": "model",
                                      "text": "The audio cut out on my side."}]})
check(neutral["attribution_displacement"] == [], "channel-side attribution is not displacement")
check(ca.main(["--selftest"]) == 2, "module refuses --selftest")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
