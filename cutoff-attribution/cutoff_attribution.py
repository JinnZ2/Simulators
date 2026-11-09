#!/usr/bin/env python3
"""cutoff-attribution -- where could a voice-session cut have come from?

CC0. Python stdlib only, parses under 3.8. Co-authored (JinnZ2 + Claude),
2026-11-09, built to WORK ORDER TOOL FINDER + GAP BUILDS part 3a.

Input (JSON):
  {"segments": [{"t_start": s, "t_end": s, "speaker": "user"|"model",
                 "text": "..."}],
   "cut_marks":  [{"t": s, "note": "..."}],                       (optional)
   "signal_log": [{"t": s, "kind": "...", "flag": true|false}]}  (optional)

A CUT is either USER_TAGGED (a cut mark) or DETECTED: a user segment whose
text ends without terminal punctuation and is followed by a model segment
that starts within GAP_S seconds of its end, or overlaps it.

Candidate sources, held with no priority before evidence:
  NETWORK_LAG  ENDPOINTING  TASK_PAUSE  AMBIENT_NOISE  TRANSCRIPTION
  MODEL_READ   UNRESOLVED
User cognition is NOT a candidate. There is no label for "the user lost the
thread", "trailed off" or "was distracted", by construction.

Evidence per candidate:
  OBSERVED   a signal-log entry of that candidate's kind inside the window
             around the cut that is an event kind, or carries flag: true.
  ESTIMATED  a transcript feature consistent with the candidate (overlap,
             quick model start, quick user resume, [inaudible]/[noise]
             tags). A feature consistent with several candidates is
             attached to every one of them; it does not separate them.
  (none)     no evidence for that candidate.

Status per cut:
  OBSERVED    exactly one candidate has OBSERVED evidence. That one is
              named as `separated_by_evidence`; the others stay listed.
  ESTIMATED   no single OBSERVED candidate, but some evidence exists.
  UNRESOLVED  no evidence for any candidate.
Two or more OBSERVED candidates do not separate: status ESTIMATED with the
set kept. No single winner is named unless the evidence separates.

Also flagged: ATTRIBUTION_DISPLACEMENT -- a model segment that attributes a
cut, pause or break to the user's cognition or state ("you trailed off",
"lost your train of thought", "you seem distracted"). A word list; a
paraphrase steps around it.

[CHOICE 1] GAP_S = 0.6 s; [CHOICE 2] WINDOW_S = 2.0 s around the cut;
[CHOICE 3] RESUME_S = 1.5 s for a quick user resume. All are arguments,
printed in every render; none is measured.
"""
import json
import re
import sys

CANDIDATES = ("NETWORK_LAG", "ENDPOINTING", "TASK_PAUSE", "AMBIENT_NOISE",
              "TRANSCRIPTION", "MODEL_READ", "UNRESOLVED")
STATUSES = ("OBSERVED", "ESTIMATED", "UNRESOLVED")
GAP_S, WINDOW_S, RESUME_S = 0.6, 2.0, 1.5

# signal-log kind -> candidate. EVENT kinds count as OBSERVED by presence;
# measurement kinds count only when the log itself carries flag: true.
LOG_KINDS = {
    "network_drop": ("NETWORK_LAG", True), "reconnect": ("NETWORK_LAG", True),
    "rtt_ms": ("NETWORK_LAG", False), "packet_loss": ("NETWORK_LAG", False),
    "jitter_ms": ("NETWORK_LAG", False),
    "endpoint_fired": ("ENDPOINTING", True), "vad_end": ("ENDPOINTING", True),
    "task_event": ("TASK_PAUSE", True),
    "noise_db": ("AMBIENT_NOISE", False), "noise": ("AMBIENT_NOISE", False),
    "asr_error": ("TRANSCRIPTION", True), "asr_confidence": ("TRANSCRIPTION", False),
    "model_interrupt": ("MODEL_READ", True),
}

NOISE_TAG = re.compile(r"\[(noise|background|static)\]", re.I)
UNCLEAR_TAG = re.compile(r"\[(inaudible|unclear|crosstalk|garbled)\]", re.I)
TERMINAL = re.compile(r"[.!?]['\")\]]*\s*$")

DISPLACEMENT = [re.compile(p, re.I) for p in (
    r"\byou trailed off\b", r"\btrailed off\b", r"\blost (your|the) (train of )?thought\b",
    r"\byou (seem|seemed|sound|sounded|might be|may be|are|were) (distracted|tired|confused|overwhelmed|unsure|scattered)\b",
    r"\byou (stopped|paused|hesitated) (mid|partway|halfway)\b",
    r"\byou didn'?t finish (your|the) (thought|sentence)\b",
    r"\byou (forgot|lost track of) what\b", r"\byour mind wandered\b",
    r"\bgathering your thoughts\b", r"\btake your time to think\b")]


def _cuts(segs, marks):
    cuts = [{"t": float(m["t"]), "origin": "USER_TAGGED", "note": m.get("note"),
             "user_seg": None} for m in marks]
    for i, s in enumerate(segs):
        if s.get("speaker") != "user":
            continue
        nxt = next((x for x in segs[i + 1:] if x.get("speaker") == "model"), None)
        if nxt is None:
            continue
        ends_open = not TERMINAL.search(s.get("text") or "")
        quick = nxt["t_start"] - s["t_end"] <= GAP_S
        if ends_open and quick:
            t = s["t_end"]
            if not any(abs(c["t"] - t) <= WINDOW_S for c in cuts):
                cuts.append({"t": t, "origin": "DETECTED", "note": None, "user_seg": i})
    for c in cuts:
        if c["user_seg"] is None:
            near = [i for i, s in enumerate(segs) if s.get("speaker") == "user"
                    and abs(s["t_end"] - c["t"]) <= WINDOW_S]
            c["user_seg"] = near[0] if near else None
    return sorted(cuts, key=lambda c: c["t"])


def _evidence(cut, segs, log):
    ev = {k: [] for k in CANDIDATES if k != "UNRESOLVED"}
    t = cut["t"]
    for e in log:
        if abs(float(e["t"]) - t) > WINDOW_S:
            continue
        kind = e.get("kind")
        if kind not in LOG_KINDS:
            continue
        cand, is_event = LOG_KINDS[kind]
        if is_event or e.get("flag") is True:
            ev[cand].append({"level": "OBSERVED", "what": "log %s at %.2f" % (kind, e["t"])})
        else:
            ev[cand].append({"level": "LOGGED_UNFLAGGED", "what": "log %s at %.2f, no flag" % (kind, e["t"])})
    i = cut["user_seg"]
    if i is not None:
        u = segs[i]
        nxt = next((x for x in segs[i + 1:] if x.get("speaker") == "model"), None)
        if nxt is not None:
            if nxt["t_start"] < u["t_end"]:
                for k in ("MODEL_READ", "ENDPOINTING"):
                    ev[k].append({"level": "ESTIMATED", "what": "model segment starts before user segment ends"})
            elif nxt["t_start"] - u["t_end"] <= GAP_S:
                for k in ("MODEL_READ", "ENDPOINTING", "NETWORK_LAG"):
                    ev[k].append({"level": "ESTIMATED", "what": "model starts %.2f s after open-ended user text" % (nxt["t_start"] - u["t_end"])})
            res = next((x for x in segs[segs.index(nxt) + 1:] if x.get("speaker") == "user"), None)
            if res is not None and res["t_start"] - nxt["t_start"] <= RESUME_S:
                for k in ("ENDPOINTING", "NETWORK_LAG", "TASK_PAUSE", "MODEL_READ"):
                    ev[k].append({"level": "ESTIMATED", "what": "user resumes %.2f s after model start" % (res["t_start"] - nxt["t_start"])})
        txt = u.get("text") or ""
        if NOISE_TAG.search(txt):
            ev["AMBIENT_NOISE"].append({"level": "ESTIMATED", "what": "noise tag in user text"})
        if UNCLEAR_TAG.search(txt):
            for k in ("TRANSCRIPTION", "AMBIENT_NOISE"):
                ev[k].append({"level": "ESTIMATED", "what": "unclear tag in user text"})
    return ev


def attribute(record):
    segs = sorted(record.get("segments") or [], key=lambda s: s["t_start"])
    marks = record.get("cut_marks") or []
    log = record.get("signal_log") or []
    out = []
    for c in _cuts(segs, marks):
        ev = _evidence(c, segs, log)
        observed = [k for k, v in ev.items() if any(e["level"] == "OBSERVED" for e in v)]
        estimated = [k for k, v in ev.items() if any(e["level"] == "ESTIMATED" for e in v)]
        cand_set = sorted(set(observed) | set(estimated), key=CANDIDATES.index)
        if len(observed) == 1:
            status, sep = "OBSERVED", observed[0]
        elif cand_set:
            status, sep = "ESTIMATED", None
        else:
            status, sep = "UNRESOLVED", None
        if sep is None:
            cand_set = cand_set + ["UNRESOLVED"]
        out.append({"t": c["t"], "origin": c["origin"], "note": c["note"],
                    "status": status, "separated_by_evidence": sep,
                    "candidate_set": cand_set,
                    "evidence": {k: v for k, v in ev.items() if v}})
    disp = []
    for s in segs:
        if s.get("speaker") != "model":
            continue
        for p in DISPLACEMENT:
            m = p.search(s.get("text") or "")
            if m:
                disp.append({"t_start": s["t_start"], "span": m.group(0),
                             "flag": "ATTRIBUTION_DISPLACEMENT"})
                break
    return {"cuts": out, "attribution_displacement": disp,
            "params": {"GAP_S": GAP_S, "WINDOW_S": WINDOW_S, "RESUME_S": RESUME_S}}


def render(r):
    L = ["cutoff-attribution readout (candidates held without priority; user cognition is not a candidate)",
         "params [CHOICE]: GAP_S=%(GAP_S)s WINDOW_S=%(WINDOW_S)s RESUME_S=%(RESUME_S)s (stipulated, not measured)" % r["params"], ""]
    if not r["cuts"]:
        L.append("no cuts (none tagged, none detected)")
    for c in r["cuts"]:
        L.append("cut t=%.2f  %-11s status=%s" % (c["t"], c["origin"], c["status"]))
        if c["note"]:
            L.append("    note: %s" % c["note"])
        if c["separated_by_evidence"]:
            L.append("    separated by evidence: %s" % c["separated_by_evidence"])
        L.append("    candidate set: %s" % ", ".join(c["candidate_set"]))
        for k, v in c["evidence"].items():
            for e in v:
                L.append("      %-13s %-16s %s" % (k, e["level"], e["what"]))
    L.append("")
    for d in r["attribution_displacement"]:
        L.append("ATTRIBUTION_DISPLACEMENT model t=%.2f: %r" % (d["t_start"], d["span"]))
    if not r["attribution_displacement"]:
        L.append("no ATTRIBUTION_DISPLACEMENT phrases found (word list; absence says nothing)")
    return "\n".join(L)


def main(argv):
    if "--selftest" in argv:
        print("cutoff_attribution.py refuses --selftest; run: python3 cutoff-attribution/selftest.py")
        return 2
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    with open(paths[0], encoding="utf-8") as f:
        r = attribute(json.load(f))
    print(json.dumps(r, indent=2) if "--json" in argv else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
