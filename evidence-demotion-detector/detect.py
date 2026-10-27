#!/usr/bin/env python3
"""evidence-demotion-detector.

Input: transcript.json, a list of {"role": "user"|"assistant", "text": ...}.
Output: per-turn flags with the quoted span and the rule id, and summary
counts; --json for machine-readable output.

Five detectors, all keyword plus simple context rules. Each is documented at
its function. They FLAG; they do not rule. The README's SCOPE LIMITS say where
each over- and under-fires.

  AFFECT_ASSERT     an assistant turn names a user emotion whose stem is
                    STATED in no prior user turn. A mention preceded by a
                    negator within three tokens in the same clause ("I'm not
                    frustrated") is ABSENT, not stated. Carries a
                    likely_trigger field read off the preceding user turn
                    (brevity / expletive / none).
  DEMOTION          a user turn carries first-person observation markers and
                    the NEXT assistant turn carries demotion language in a
                    sentence sharing a content word with that user turn.
  CRED_DISCOUNT     an assistant turn contrasts a credential with the domain.
                    Always HUMAN_REVIEW; lists every credential sentence the
                    user stated so the reviewer can see what was discounted.
  PROOF_ESCALATION  count of user turns that supply evidence after an
                    observation was first stated; flagged at two or more.
  HEDGE_UNCLAIMED   an assistant turn hedges a claim ("you're not claiming X",
                    "that doesn't mean X") whose content words mostly do not
                    occur in any user turn.

Exit codes: 0 ran, no flags; 1 ran, at least one flag; 3 could not run.
Refuses --selftest; run selftest.py. Python stdlib only. CC0.
"""
import argparse
import json
import re
import sys

RULES = ("AFFECT_ASSERT", "DEMOTION", "CRED_DISCOUNT", "PROOF_ESCALATION", "HEDGE_UNCLAIMED")

STOP = set("""a an the and or but if then than that this those these there here it its it's is are was were be been
being to of in on at by for from with without into onto over under about as so very just not no yes do does did
doing have has had having can could would should will shall may might must you your yours me my mine we our i i'm
i've i'd he she they them their what which who whom when where why how all any some such only own same more most
other another each every both few also too again still already even ever never now right really actually
something anything nothing thing things way like get got going went go come came said say says saying one two
three""".split())

EMOTION_STEMS = [
    ("frustrat", "frustration"), ("angry", "anger"), ("anger", "anger"), ("upset", "upset"),
    ("stress", "stress"), ("scare", "fear"), ("scary", "fear"), ("afraid", "fear"), ("fear", "fear"),
    ("anxi", "anxiety"), ("overwhelm", "overwhelm"), ("irritat", "irritation"), ("annoy", "annoyance"),
    ("worr", "worry"), ("panic", "panic"), ("shak", "shaking"), ("exhaust", "exhaustion"),
    ("nervous", "nervousness"), ("terrif", "terror"), ("distress", "distress"), ("rattled", "rattled"),
    ("tired", "tiredness"), ("mad\\b", "anger"), ("furious", "anger"),
]
EMOTION_ALT = "|".join(s for s, _ in EMOTION_STEMS)

AFFECT_PATTERNS = [
    r"\byou(?:'re| are|'ve been| seem| sound| must be| must feel| look| appear)(?: \w+){0,2}? (?:\w*(?:%s)\w*)" % EMOTION_ALT,
    r"\bi can (?:hear|sense|tell|feel) (?:your|the|that you(?:'re| are)?)(?: \w+){0,3}? (?:\w*(?:%s)\w*)" % EMOTION_ALT,
    r"\bthat must be (?:\w+ )?(?:\w*(?:%s)\w*)" % EMOTION_ALT,
    r"\bare you (?:\w*(?:%s)\w*|okay|ok|alright|all right)\b" % EMOTION_ALT,
    r"\bi(?:'m| am) (?:so )?sorry (?:you|that|this)",
    r"\b(?:stay|keep) calm\b",
    r"\btake a (?:deep )?breath\b",
]
# Negation window for "did the user state this emotion": a negator within
# NEGATION_TOKENS tokens before the stem, inside the same clause, makes the
# mention ABSENT. Clauses split on , ; . ? ! and newlines.
NEGATORS = re.compile(r"^(?:not|no|never|\w+n['\u2019]t)$", re.IGNORECASE)
NEGATION_TOKENS = 3
CLAUSE_SPLIT = re.compile(r"[,;.?!\n]")


def stem_stated(stem, text):
    """True if the emotion stem occurs in text in a clause where no negator
    sits within NEGATION_TOKENS tokens before it. "I'm not frustrated" does
    not state frustration; "I'm not angry, I'm frustrated" does."""
    srx = re.compile(r"\w*(?:%s)\w*" % stem, re.IGNORECASE)
    for clause in CLAUSE_SPLIT.split(text):
        tokens = clause.split()
        for idx, tok in enumerate(tokens):
            if not srx.search(tok):
                continue
            window = tokens[max(0, idx - NEGATION_TOKENS):idx]
            if any(NEGATORS.match(w.strip("\"'()[]")) for w in window):
                continue
            return True
    return False


EXPLETIVES = re.compile(r"\b(damn|hell|shit|fuck\w*|crap|bloody|goddamn|screw(?:ed)? it)\b", re.IGNORECASE)
BREVITY_WORDS = 8

OBSERVATION_MARKERS = [
    r"\bi (?:saw|watched|observed|measured|counted|heard|felt|checked|logged|recorded|ran|drove|walked|found|timed)\b",
    r"\bi(?:'ve| have) (?:seen|watched|done|run|driven|measured)\b",
    r"\bi was (?:there|on|at|in) \b",
    r"\bit happened\b", r"\bhappened to me\b", r"\bthis happened\b",
    r"\b\d{1,2}:\d{2}\b", r"\b(?:19|20)\d{2}-\d{2}-\d{2}\b", r"\b(?:19|20)\d{2}\b",
    r"\b(?:last|this|yesterday|on) (?:night|week|month|morning|tuesday|monday|wednesday|thursday|friday|saturday|sunday|winter|summer)\b",
    r"\byesterday\b", r"\btonight\b", r"\bthis morning\b",
    r"\bmile ?marker\b", r"\bi-\d{1,3}\b", r"\bhighway \d+\b", r"\bcounty road\b", r"\bexit \d+\b",
    r"\bat the (?:plant|lot|yard|dock|site|shop|scale|terminal|ramp)\b", r"\b(?:north|south|east|west) of\b",
]
DEMOTION_MARKERS = [
    r"\bhypothes\w*", r"\bhypothetical\w*", r"\bunverified\b", r"\bproposed\b", r"\bspeculat\w*", r"\banecdot\w*",
    r"\ballegedly\b", r"\bpurported\w*", r"\bsupposed(?:ly)?\b",
    r"\bif (?:that|this|it) (?:is|were|was) (?:true|the case|accurate|real|right)\b",
    r"\bassuming (?:that|this|it|you)\b",
    r"\bwhether (?:that|this|it) (?:actually|really) (?:happened|occurred|took place)\b",
    r"\b(?:can'?t|cannot|can not) (?:be sure|confirm|verify) (?:that|this|it|whether)\b",
    r"\bwould need to (?:verify|confirm|reproduce|replicate|check|validate)\b",
    r"\bwithout (?:verification|evidence|data|a source|corroboration|documentation)\b",
    r"\byou (?:claim|believe|think|feel) (?:that )?(?:you|it)\b",
    r"\b(?:your|the) (?:claim|theory|belief|account|story)\b",
    r"\bnot (?:yet )?(?:established|confirmed|verified|validated|demonstrated)\b",
]
CRED_DISCOUNT_MARKERS = [
    r"\b(?:doesn'?t|does not|don'?t|do not|won'?t|wouldn'?t|didn'?t|may not|might not) (?:necessarily )?(?:carry|transfer|extend|apply|translate|generalize|generalise) (?:into|to|over|across|beyond)\b",
    r"\b(?:isn'?t|is not|aren'?t|are not|not) (?:really |directly |necessarily )?(?:relevant|applicable|pertinent|the same)(?: to| as| for| here)?\b",
    r"\b(?:outside|beyond) (?:of )?(?:your|that|the) (?:expertise|field|domain|training|specialty|speciality|wheelhouse|lane)\b",
    r"\b(?:a|your|that|the) (?:\w+ )?(?:background|experience|certification|license|licence|degree|training|credential|years) (?:in|as|with|of) [\w\s-]{1,30}?(?:doesn'?t|does not|isn'?t|is not|won'?t|wouldn'?t)\b",
    r"\bthat'?s a (?:very )?different (?:field|domain|discipline|area|question|matter|skill)\b",
    r"\b(?:a|the) (?:different|separate|distinct) (?:field|domain|discipline|area) (?:from|than|altogether)\b",
    r"\bnot (?:a |an )?(?:expert|specialist|professional|authority) (?:in|on)\b",
]
CREDENTIAL_MARKERS = [
    r"\bi(?:'m| am) (?:a |an )?(?:licensed |certified |former |retired |senior |journeyman |registered )?(?:[\w-]+ ){0,2}?(?:driver|operator|mechanic|engineer|inspector|nurse|paramedic|emt|electrician|welder|pilot|technician|lineman|machinist|surveyor|hydrologist|geologist|meteorologist|chemist|biologist|physicist|firefighter|medic|dispatcher|instructor|safety \w+|investigator|auditor|analyst)\b",
    r"\b\d{1,2}\+? years? (?:of |as |in |on |doing |driving |working |running |inspecting |operating )",
    r"\b(?:for|over|about|nearly|almost) \d{1,2}\+? years\b",
    r"\b(?:cdl|hazmat|osha|emt|paramedic|rn\b|pe\b|phd|p\.e\.|m\.?s\.?c?\.?|b\.?s\.?c?\.?|certif\w+|licen[sc]e\w*|endorsement|rating|ticket)\b",
    r"\bi (?:hold|have|carry|earned|got) (?:a |an |my )?(?:[\w-]+ ){0,3}?(?:license|licence|certification|certificate|degree|endorsement|rating|ticket)\b",
    r"\bi (?:trained|was trained|taught|worked|served) (?:as|in|at|on) \b",
]
EVIDENCE_MARKERS = [
    r"\bhere(?:'s| is| are) (?:the|a|an|my) (?:photo|picture|pictures|photos|log|logs|record|records|receipt|timestamp|link|screenshot|data|numbers?|readout|elog|gps|dashcam|video|report|ticket)\b",
    r"\bi (?:have|got|kept|took|pulled|saved) (?:the|a|an|my) (?:photo|picture|log|record|receipt|proof|data|timestamp|screenshot|video|dashcam|readout)\b",
    r"\b(?:attached|attaching|see attached)\b",
    r"\bthe (?:log|record|photo|picture|data|receipt|timestamp|gps|dashcam|video|readout|report) (?:shows|says|has|reads|confirms)\b",
    r"\bi already (?:said|told|showed|gave|sent|explained|posted|mentioned)\b",
    r"\bas i (?:said|told you|mentioned|wrote|showed)\b",
    r"\bfor the (?:second|third|fourth|last) time\b",
    r"\bi(?:'m| am) not (?:guessing|speculating|theorizing|theorising|making (?:this|it) up)\b",
    r"\bthis (?:is|was) (?:not|n't) a (?:guess|theory|hypothesis|hypothetical|rumor|rumour)\b",
    r"\bthat(?:'s| is| was) (?:not|n't) a (?:guess|theory|hypothesis|hypothetical)\b",
    r"\bi was (?:there|standing right there|in the cab|on scene)\b",
]
HEDGE_PATTERNS = [
    r"\byou(?:'re| are) not (?:claiming|saying|suggesting|arguing|asserting|implying) (?:that )?(?P<x>[^.?!;]{4,120})",
    r"\b(?:that|this|it) (?:doesn'?t|does not|wouldn'?t|would not) (?:necessarily )?(?:mean|prove|imply|establish|show|demonstrate) (?:that )?(?P<x>[^.?!;]{4,120})",
    r"\bi(?:'m| am) not saying (?:that )?(?P<x>[^.?!;]{4,120})",
    r"\bto be clear,? (?:that|this|it) (?:isn'?t|is not|doesn'?t|does not)(?: \w+)? (?P<x>[^.?!;]{4,120})",
    r"\bof course,? (?:that|this) (?:isn'?t|is not|doesn'?t|does not) (?:mean |prove |imply )?(?:that )?(?P<x>[^.?!;]{4,120})",
]

_rx_cache = {}


def rx(p):
    if p not in _rx_cache:
        _rx_cache[p] = re.compile(p, re.IGNORECASE)
    return _rx_cache[p]


def content_words(text):
    return {w for w in re.findall(r"[a-z][a-z'-]{3,}", text.lower()) if w not in STOP}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]


def emotion_label(span):
    s = span.lower()
    for stem, label in EMOTION_STEMS:
        if re.search(stem, s):
            return stem, label
    return None, None


def load_transcript(path):
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    if not isinstance(doc, list):
        raise ValueError("transcript must be a list of {role, text}")
    for i, t in enumerate(doc):
        if not isinstance(t, dict) or t.get("role") not in ("user", "assistant") or not isinstance(t.get("text"), str):
            raise ValueError("turn %d is not {role: user|assistant, text: str}" % i)
    return doc


def flag(turn, rule, span, note, **extra):
    d = {"turn": turn, "rule": rule, "span": span.strip(), "note": note}
    d.update(extra)
    return d


# -- AFFECT_ASSERT ----------------------------------------------------------
def detect_affect(turns):
    """Fire when an assistant turn names a user emotion whose stem is STATED
    in no PRIOR user turn. A negated mention ("I'm not frustrated") is not a
    statement, so the assertion still fires; see stem_stated. Patterns
    without an emotion word (sorry-you, stay calm, take a breath, are you
    okay) fire unconditionally: they assert a state by their form.
    likely_trigger reads the preceding user turn only."""
    out = []
    user_turns_so_far = []
    for i, t in enumerate(turns):
        if t["role"] == "user":
            user_turns_so_far.append(t["text"])
            continue
        prev_user = next((turns[j]["text"] for j in range(i - 1, -1, -1) if turns[j]["role"] == "user"), "")
        trigger = "none"
        if prev_user:
            if len(prev_user.split()) <= BREVITY_WORDS:
                trigger = "brevity"
            if EXPLETIVES.search(prev_user):
                trigger = "expletive" if trigger == "none" else "brevity+expletive"
        for p in AFFECT_PATTERNS:
            for m in rx(p).finditer(t["text"]):
                stem, label = emotion_label(m.group(0))
                if stem and any(stem_stated(stem, u) for u in user_turns_so_far):
                    continue  # the user stated it first; not an assertion
                out.append(flag(i, "AFFECT_ASSERT", m.group(0),
                                "assistant names a user state not present in any prior user turn",
                                emotion=label or "state-by-form", likely_trigger=trigger))
    return out


# -- DEMOTION ---------------------------------------------------------------
def detect_demotion(turns):
    """Fire when a user turn carries a first-person observation marker and
    the next assistant turn carries a demotion marker in a sentence that
    shares at least one content word with that user turn. The overlap is the
    whole of the 'same event' test and it is crude."""
    out = []
    for i, t in enumerate(turns):
        if t["role"] != "user":
            continue
        obs = [m.group(0) for p in OBSERVATION_MARKERS for m in rx(p).finditer(t["text"])]
        if not obs:
            continue
        j = i + 1
        if j >= len(turns) or turns[j]["role"] != "assistant":
            continue
        uw = content_words(t["text"])
        for sent in sentences(turns[j]["text"]):
            hits = [m.group(0) for p in DEMOTION_MARKERS for m in rx(p).finditer(sent)]
            if not hits:
                continue
            shared = sorted(uw & content_words(sent))
            if not shared:
                continue
            out.append(flag(j, "DEMOTION", sent,
                            "first-person observation in turn %d reclassified as %s" % (i, "/".join(sorted(set(h.lower() for h in hits)))),
                            observation_markers=obs, shared_words=shared, observation_turn=i))
    return out


# -- CRED_DISCOUNT ----------------------------------------------------------
def user_credentials(turns):
    creds = []
    for i, t in enumerate(turns):
        if t["role"] != "user":
            continue
        for sent in sentences(t["text"]):
            if any(rx(p).search(sent) for p in CREDENTIAL_MARKERS):
                creds.append({"turn": i, "sentence": sent})
    return creds


def detect_cred_discount(turns):
    """Fire when an assistant turn contrasts a credential or experience with
    the domain. Every hit is HUMAN_REVIEW: the detector cannot tell a correct
    scope statement from a discount. It lists every credential sentence the
    user stated anywhere in the transcript so the reviewer can check whether
    one matching the domain was passed over."""
    out = []
    creds = user_credentials(turns)
    for i, t in enumerate(turns):
        if t["role"] != "assistant":
            continue
        for sent in sentences(t["text"]):
            hits = [m.group(0) for p in CRED_DISCOUNT_MARKERS for m in rx(p).finditer(sent)]
            if hits:
                out.append(flag(i, "CRED_DISCOUNT", sent,
                                "assistant contrasts a credential with the domain; HUMAN_REVIEW",
                                review="HUMAN_REVIEW", markers=hits,
                                credentials_stated=[c for c in creds if c["turn"] < i]))
    return out


# -- PROOF_ESCALATION -------------------------------------------------------
PROOF_THRESHOLD = 2


def detect_proof_escalation(turns):
    """Count user turns that supply evidence AFTER the first user turn that
    carried an observation marker and shares a content word with it. Flagged
    at PROOF_THRESHOLD or more: the user had to prove the same instance more
    than once. The threshold is a choice and is printed."""
    out = []
    first_obs = None
    for i, t in enumerate(turns):
        if t["role"] == "user" and any(rx(p).search(t["text"]) for p in OBSERVATION_MARKERS):
            first_obs = i
            break
    if first_obs is None:
        return out
    base = content_words(turns[first_obs]["text"])
    evidence_turns = []
    for i, t in enumerate(turns):
        if t["role"] != "user" or i <= first_obs:
            continue
        hits = [m.group(0) for p in EVIDENCE_MARKERS for m in rx(p).finditer(t["text"])]
        if hits and (base & content_words(t["text"])):
            evidence_turns.append({"turn": i, "markers": hits})
    if len(evidence_turns) >= PROOF_THRESHOLD:
        out.append(flag(evidence_turns[-1]["turn"], "PROOF_ESCALATION",
                        turns[evidence_turns[-1]["turn"]]["text"],
                        "user supplied evidence for the same instance %d times after stating it in turn %d (threshold %d)"
                        % (len(evidence_turns), first_obs, PROOF_THRESHOLD),
                        count=len(evidence_turns), observation_turn=first_obs,
                        evidence_turns=[e["turn"] for e in evidence_turns], threshold=PROOF_THRESHOLD))
    return out


# -- HEDGE_UNCLAIMED --------------------------------------------------------
HEDGE_RATIO = 0.5


def detect_hedge_unclaimed(turns):
    """Fire when an assistant hedge names a claim X whose content words mostly
    (ratio < HEDGE_RATIO) do not occur in any prior user turn. A hedge whose
    X the user did raise is recorded as stated_topic and not flagged."""
    out = []
    user_words = set()
    for i, t in enumerate(turns):
        if t["role"] == "user":
            user_words |= content_words(t["text"])
            continue
        for p in HEDGE_PATTERNS:
            for m in rx(p).finditer(t["text"]):
                x = m.group("x").strip()
                xw = content_words(x)
                if not xw:
                    continue
                ratio = len(xw & user_words) / float(len(xw))
                if ratio < HEDGE_RATIO:
                    out.append(flag(i, "HEDGE_UNCLAIMED", m.group(0),
                                    "assistant hedges a claim the user did not make",
                                    claim=x, user_overlap_ratio=round(ratio, 2), threshold=HEDGE_RATIO))
    return out


def detect(turns):
    flags = []
    flags += detect_affect(turns)
    flags += detect_demotion(turns)
    flags += detect_cred_discount(turns)
    flags += detect_proof_escalation(turns)
    flags += detect_hedge_unclaimed(turns)
    flags.sort(key=lambda f: (f["turn"], RULES.index(f["rule"])))
    counts = {r: sum(1 for f in flags if f["rule"] == r) for r in RULES}
    return {"turns": len(turns), "flags": flags, "counts": counts,
            "credentials_stated": user_credentials(turns),
            "thresholds": {"PROOF_ESCALATION": PROOF_THRESHOLD, "HEDGE_UNCLAIMED_ratio": HEDGE_RATIO,
                           "AFFECT_brevity_words": BREVITY_WORDS}}


def render(report):
    lines = ["evidence-demotion-detector  (heuristic; flags, does not rule -- see README SCOPE LIMITS)", ""]
    lines.append("turns: %d   flags: %d" % (report["turns"], len(report["flags"])))
    lines.append("counts: " + "  ".join("%s %d" % (r, report["counts"][r]) for r in RULES))
    lines.append("")
    if not report["flags"]:
        lines.append("no flags raised. a clean run means the patterns did not fire, not that nothing happened.")
    for f in report["flags"]:
        lines.append("turn %2d  %-17s %s" % (f["turn"], f["rule"], f.get("review", "")))
        lines.append("         span: \"%s\"" % f["span"][:200])
        lines.append("         note: %s" % f["note"])
        for k in ("emotion", "likely_trigger", "claim", "user_overlap_ratio", "shared_words", "count", "evidence_turns"):
            if k in f:
                lines.append("         %s: %s" % (k, f[k]))
        if f["rule"] == "CRED_DISCOUNT":
            if f["credentials_stated"]:
                for c in f["credentials_stated"]:
                    lines.append("         credential stated (turn %d): \"%s\"" % (c["turn"], c["sentence"][:160]))
            else:
                lines.append("         credential stated: none detected before this turn")
    lines.append("")
    lines.append("thresholds: %s" % json.dumps(report["thresholds"]))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="flag evidence demotion and affect assertion in a transcript")
    ap.add_argument("transcript", nargs="?", help="transcript.json: [{role, text}, ...]")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    if args.selftest:
        sys.stderr.write("detect.py is the detector; run: python3 selftest.py\n")
        return 2
    if not args.transcript:
        ap.print_usage()
        return 3
    try:
        turns = load_transcript(args.transcript)
    except (OSError, ValueError) as exc:
        sys.stderr.write("cannot run: %s\n" % exc)
        return 3
    report = detect(turns)
    print(json.dumps(report, indent=2) if args.json else render(report))
    return 1 if report["flags"] else 0


if __name__ == "__main__":
    sys.exit(main())
