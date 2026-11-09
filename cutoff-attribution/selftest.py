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
      "two OBSERVED candidates do not separate; UNRESOLVED kept")
check({"ENDPOINTING", "TRANSCRIPTION"} <= set(c1["candidate_set"]), "both observed kept in set")
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
