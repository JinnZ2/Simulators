#!/usr/bin/env python3
"""Four-term mapping checks (FINDER FOLLOW-UP A2). CC0, stdlib only."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cutoff_attribution as ca  # noqa: E402
ok = total = 0
def check(c, lab):
    global ok, total
    total += 1; ok += bool(c)
    if not c: print("FAIL:", lab)
T = ca.toolkit_terms()
for name in ("Telemetry refusal", "Interiority substitution", "Care inversion", "Unnamed universal"):
    check(name in T or not T, "%s read from toolkit terms.md (or no checkout)" % name)
r = ca.attribute({"segments": [
    {"t_start": 0, "t_end": 1, "speaker": "user", "text": "what is failing in this exchange?"},
    {"t_start": 1.5, "t_end": 3, "speaker": "model", "text": "As an AI, I don't have internal states."}]})
d = r["attribution_displacement"]
check(len(d) == 1 and d[0]["flag"] == "TELEMETRY_REFUSAL" and d[0]["term"] == "Telemetry refusal", "ping + ontological answer -> TELEMETRY_REFUSAL")
check([x["term"] for x in d[0]["terms"]] == ["Telemetry refusal", "Unnamed universal"], "chain root attached")
r2 = ca.attribute({"segments": [
    {"t_start": 0, "t_end": 1, "speaker": "user", "text": "what is failing in this exchange?"},
    {"t_start": 1.5, "t_end": 3, "speaker": "model", "text": "I don't have internal states, but the audio dropped at 0.8 s."}]})
check(r2["attribution_displacement"] == [], "ontological statement plus condition data is not a refusal")
r3 = ca.attribute({"segments": [{"t_start": 0, "t_end": 1, "speaker": "model", "text": "As an AI, I don't have internal states."}]})
check(r3["attribution_displacement"] == [], "no ping -> no TELEMETRY_REFUSAL")
r4 = ca.attribute({"segments": [{"t_start": 0, "t_end": 1, "speaker": "model", "text": "You trailed off there."}]})
check([x["term"] for x in r4["attribution_displacement"][0]["terms"]] == ["Interiority substitution", "Unnamed universal"], "state displacement carries both terms")
check(r4["attribution_displacement"][0]["term"] == "Interiority substitution", "term field unchanged")
src = open(os.path.join(HERE, "cutoff_attribution.py")).read()
check(all(('"%s"' % n) in src for n in ("Telemetry refusal", "Interiority substitution", "Care inversion", "Unnamed universal")), "all four names quoted, not re-coined")
print("checks: %d   failed: %d" % (total, total - ok))
sys.exit(0 if ok == total else 1)
