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

CHANNEL CHAIN (Amendment A1, 2026-11-09). No reading here is direct. Each
candidate sits at one hop of the voice chain, and its evidence is read through
that hop:
  sensor        AMBIENT_NOISE, TASK_PAUSE   (room, mic, the user's task)
  encoding      ENDPOINTING                 (VAD / endpointer, codec)
  transmission  NETWORK_LAG                 (network, relay)
  decoding      TRANSCRIPTION               (ASR, punctuation insertion)
  inference     MODEL_READ                  (the session model reading text)
A log entry counts as OBSERVED only when its hop passed a known-reference
check (`reference_checks` in the input: a known input injected at that hop and
what came out). Through an unchecked hop it is RECORDED_VIA_UNVERIFIED_HOP and
counts as ESTIMATED. A failed check marks the hop CHECK_FAILED and the entry
counts as ESTIMATED, with the failure printed. This tool's own reading is a
further inference hop, checked on every run against a built-in known cut.
Every cut is emitted as a tools/channel_chain.py record (SubstrateReading
field names plus the chain); its chain_class is never DIRECT.

TERMS (Amendment A2). ATTRIBUTION_DISPLACEMENT hits cite two terms from
Cross-Domain-Toolkit telemetry_vocabulary/terms.md, read from a sibling
checkout at run time and not re-coined: "Interiority substitution" for a
channel event attributed to the user's state, "Care inversion" for the same
delivered as care. The phrase-to-term mapping is this tool's reading, not the
toolkit's. With no checkout the term is carried as TERM_NOT_CHECKED.

[CHOICE 1] GAP_S = 0.6 s; [CHOICE 2] WINDOW_S = 2.0 s around the cut;
[CHOICE 3] RESUME_S = 1.5 s for a quick user resume. All are arguments,
printed in every render; none is measured.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from tools import channel_chain as cc  # noqa: E402  (import, not a copy)

CANDIDATES = ("NETWORK_LAG", "ENDPOINTING", "TASK_PAUSE", "AMBIENT_NOISE",
              "TRANSCRIPTION", "MODEL_READ", "UNRESOLVED")
STATUSES = ("OBSERVED", "ESTIMATED", "UNRESOLVED")
GAP_S, WINDOW_S, RESUME_S = 0.6, 2.0, 1.5

ESTIMATE_LEVELS = ("ESTIMATED", "RECORDED_VIA_UNVERIFIED_HOP", "RECORDED_VIA_FAILED_HOP")
HOP_OF = {"AMBIENT_NOISE": "sensor", "TASK_PAUSE": "sensor", "ENDPOINTING": "encoding",
          "NETWORK_LAG": "transmission", "TRANSCRIPTION": "decoding", "MODEL_READ": "inference"}
DEVIATION = {
    "sensor": ["room noise", "mic placement or clipping", "the user's concurrent task"],
    "encoding": ["endpointer / VAD timeout", "codec packet-loss concealment"],
    "transmission": ["network latency or drop", "relay reconnect"],
    "decoding": ["ASR misrecognition", "punctuation inserted or dropped", "[inaudible] tagging"],
    "inference": ["model reads a partial utterance as complete"],
}
TOOL_DEVIATION = ["punctuation rule misreads an unpunctuated transcriber",
                  "word list misses a paraphrase", "[CHOICE] window and gap constants"]

DISPLACEMENT_TERM = {"care": "Care inversion", "state": "Interiority substitution"}
CARE_PATTERNS = (r"\bgathering your thoughts\b", r"\btake your time to think\b")


def toolkit_terms():
    """{term: 'path:line'} from Cross-Domain-Toolkit telemetry_vocabulary/terms.md,
    or {} when no checkout is reachable."""
    env = os.environ.get("CROSS_DOMAIN_TOOLKIT_PATH")
    d = env or os.path.join(os.path.dirname(os.path.dirname(HERE)), "cross-domain-toolkit")
    p = os.path.join(d, "telemetry_vocabulary", "terms.md")
    if not os.path.isfile(p):
        return {}
    out = {}
    for i, line in enumerate(open(p, encoding="utf-8"), 1):
        if line.startswith("## "):
            out[line[3:].strip()] = "Cross-Domain-Toolkit telemetry_vocabulary/terms.md:%d" % i
    return out


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


def _evidence(cut, segs, log, hop_state=None):
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
            st = (hop_state or {}).get(HOP_OF[cand], "UNVERIFIED_HOP")
            if st == "CHECKED":
                ev[cand].append({"level": "OBSERVED", "what": "log %s at %.2f (hop %s CHECKED)" % (kind, e["t"], HOP_OF[cand])})
            else:
                ev[cand].append({"level": "RECORDED_VIA_UNVERIFIED_HOP" if st == "UNVERIFIED_HOP" else "RECORDED_VIA_FAILED_HOP",
                                 "what": "log %s at %.2f (hop %s %s)" % (kind, e["t"], HOP_OF[cand], st)})
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


SELF_REF = {"segments": [{"t_start": 0.0, "t_end": 2.0, "speaker": "user", "text": "the left axle reads"},
                         {"t_start": 2.1, "t_end": 3.0, "speaker": "model", "text": "Yes?"}]}


def _self_check():
    """Inject a known cut into this tool's own reading; expect one DETECTED
    cut at t=2.0. Returns the inference hop record for the tool."""
    got = [(c["t"], c["origin"]) for c in _cuts(SELF_REF["segments"], [])]
    return cc.hop("inference", TOOL_DEVIATION, injected=[(2.0, "DETECTED")], observed=got,
                  note="cutoff-attribution's own reading, known-cut reference")


def _hop_states(record):
    """Per hop: the caller's known-reference checks (injected vs observed)."""
    st, refs = {}, {}
    for rc in record.get("reference_checks") or []:
        h = rc.get("hop")
        if h not in cc.HOPS:
            continue
        state = cc.reference_check(rc.get("injected"), rc.get("observed"))
        if st.get(h) != "CHECK_FAILED":
            st[h], refs[h] = state, rc
    return st, refs


def attribute(record):
    hop_state, hop_refs = _hop_states(record)
    tool_hop = _self_check()
    terms = toolkit_terms()
    return _attribute(record, hop_state, hop_refs, tool_hop, terms)


def _attribute(record, hop_state, hop_refs, tool_hop, terms):
    segs = sorted(record.get("segments") or [], key=lambda s: s["t_start"])
    marks = record.get("cut_marks") or []
    log = record.get("signal_log") or []
    out = []
    for c in _cuts(segs, marks):
        ev = _evidence(c, segs, log, hop_state)
        observed = [k for k, v in ev.items() if any(e["level"] == "OBSERVED" for e in v)]
        estimated = [k for k, v in ev.items() if any(e["level"] in ESTIMATE_LEVELS for e in v)]
        cand_set = sorted(set(observed) | set(estimated), key=CANDIDATES.index)
        if len(observed) == 1:
            status, sep = "OBSERVED", observed[0]
        elif cand_set:
            status, sep = "ESTIMATED", None
        else:
            status, sep = "UNRESOLVED", None
        if sep is None:
            cand_set = cand_set + ["UNRESOLVED"]
        chain = []
        for h in cc.HOPS:
            r = hop_refs.get(h)
            chain.append(cc.hop(h, DEVIATION[h], injected=r.get("injected") if r else None,
                                observed=r.get("observed") if r else None))
        chain.append(tool_hop)
        rec = cc.reading(status, "voice_transcript", "label", chain, timestamp=c["t"],
                         provenance={"origin": c["origin"], "note": c["note"]})
        out.append({"t": c["t"], "origin": c["origin"], "note": c["note"], "record": rec,
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
                kind = "care" if any(re.search(c, m.group(0), re.I) for c in CARE_PATTERNS) else "state"
                term = DISPLACEMENT_TERM[kind]
                disp.append({"t_start": s["t_start"], "span": m.group(0),
                             "flag": "ATTRIBUTION_DISPLACEMENT", "term": term,
                             "term_source": terms.get(term, "TERM_NOT_CHECKED")})
                break
    return {"cuts": out, "attribution_displacement": disp, "tool_hop": tool_hop,
            "fields_source": cc.fields_source()[0],
            "params": {"GAP_S": GAP_S, "WINDOW_S": WINDOW_S, "RESUME_S": RESUME_S}}


def render(r):
    L = ["cutoff-attribution readout (candidates held without priority; user cognition is not a candidate)",
         "params [CHOICE]: GAP_S=%(GAP_S)s WINDOW_S=%(WINDOW_S)s RESUME_S=%(RESUME_S)s (stipulated, not measured)" % r["params"],
         "tool self-check (inference hop, known cut): %s; record fields: %s" % (r["tool_hop"]["check"], r["fields_source"]), ""]
    if not r["cuts"]:
        L.append("no cuts (none tagged, none detected)")
    for c in r["cuts"]:
        L.append("cut t=%.2f  %-11s status=%s" % (c["t"], c["origin"], c["status"]))
        if c["note"]:
            L.append("    note: %s" % c["note"])
        if c["separated_by_evidence"]:
            L.append("    separated by evidence: %s" % c["separated_by_evidence"])
        L.append("    candidate set: %s" % ", ".join(c["candidate_set"]))
        L.append("    chain: %s" % cc.render_chain(c["record"]["chain"]))
        L.append("    chain class: %s (never a direct observation)" % c["record"]["chain_class"])
        for k, v in c["evidence"].items():
            for e in v:
                L.append("      %-13s %-27s %s" % (k, e["level"], e["what"]))
    L.append("")
    for d in r["attribution_displacement"]:
        L.append("ATTRIBUTION_DISPLACEMENT model t=%.2f: %r -- term: %s (%s)" % (d["t_start"], d["span"], d["term"], d["term_source"]))
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
