"""WO-2 step 1 -- the four-part decomposition as a coding schema.

Each case is coded on the order's five fields (signal present, signal
reported, holder count, join assigned, time from first signal to event)
plus how the failure was described afterwards. Every signal field is
three-valued: PRESENT / ABSENT (searched, and absent) / UNSEARCHED (not a
measurement). A missing field reads UNSEARCHED, never ABSENT.

classify() returns the class the decomposition puts a case in, or
NOT_EVALUABLE naming the field it lacks. separation() is the order's
step-1 test -- do "sudden" cases separate from genuinely unsignalled
ones -- run WITHIN a corpus of failures. base_rate() refuses: an
accident corpus is selected on failure and yields no rate over systems
(the order's own scope limit, "No base rate is claimed").

The order's four cases are parsed out of WORK_ORDER.md at call time and
coded from the order's own sentences, each code carrying the span it
rests on; that coding is this session's reading and says so.
Library module: refuses --selftest; the suite is selftest.py.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = os.path.join(HERE, "WORK_ORDER.md")

EGRESS = {"measured": "2026-09-20T02:58Z",
          "hosts": {"www.ntsb.gov:443": "CONNECT 403",
                    "www.csb.gov:443": "CONNECT 403",
                    "www.gov.uk:443": "CONNECT 403",
                    "onlinelibrary.wiley.com:443": "CONNECT 403",
                    "github.com:443": "connects (control)"}}

SIGNAL = ("PRESENT", "ABSENT", "UNSEARCHED")
JOIN = ("ASSIGNED", "UNASSIGNED", "UNSEARCHED")
DESCRIBED = ("SUDDEN", "QUIET", "NEITHER", "UNDECLARED")
FIELDS = ("signal_present", "signal_reported", "holder_count",
          "join_assigned", "time_first_signal_to_event", "described_as")
CLASSES = ("SIGNALLED_UNJOINED", "SIGNALLED_JOINED", "GENUINELY_UNSIGNALLED",
           "REPORTED_NOWHERE", "NOT_EVALUABLE", "MALFORMED")


def order_text(path=ORDER):
    return open(path, encoding="utf-8").read()


def parts(text=None):
    """The four numbered parts of the structural decomposition, parsed."""
    text = text or order_text()
    m = re.search(r"## Structural decomposition \(DERIVED\)\n\n(.*?)\n\n\"Quiet\"", text, re.S)
    if not m:
        raise ValueError("decomposition section not found")
    items = re.findall(r"^\d\. (.*?)(?=\n\d\. |\Z)", m.group(1), re.S | re.M)
    items = [re.sub(r"\s+", " ", i).strip() for i in items]
    if len(items) != 4:
        raise ValueError("expected four parts, found %d" % len(items))
    return items


def _field(rec, name, vocab, absent):
    v = rec.get(name, absent)
    if v not in vocab:
        return None
    return v


def classify(rec):
    """One case -> its class under the decomposition, or a refusal.
    A missing signal field is UNSEARCHED (not ABSENT); an UNSEARCHED field
    the class turns on makes the case NOT_EVALUABLE naming it."""
    if not isinstance(rec, dict):
        return {"state": "MALFORMED", "why": "record is not a dict"}
    sp = _field(rec, "signal_present", SIGNAL, "UNSEARCHED")
    sr = _field(rec, "signal_reported", SIGNAL, "UNSEARCHED")
    ja = _field(rec, "join_assigned", JOIN, "UNSEARCHED")
    if None in (sp, sr, ja):
        return {"state": "MALFORMED", "why": "a field carries a value outside its vocabulary"}
    if sp == "UNSEARCHED":
        return {"state": "NOT_EVALUABLE", "lacks": ["signal_present"]}
    if sp == "ABSENT":
        return {"state": "GENUINELY_UNSIGNALLED", "rests_on": ["signal_present"]}
    if sr == "UNSEARCHED":
        return {"state": "NOT_EVALUABLE", "lacks": ["signal_reported"]}
    if sr == "ABSENT":
        return {"state": "REPORTED_NOWHERE", "rests_on": ["signal_present", "signal_reported"],
                "note": "signal existed and reached no channel: part 1 of the decomposition does not hold"}
    if ja == "UNSEARCHED":
        return {"state": "NOT_EVALUABLE", "lacks": ["join_assigned"]}
    if ja == "ASSIGNED":
        return {"state": "SIGNALLED_JOINED", "rests_on": ["signal_present", "signal_reported", "join_assigned"],
                "note": "a join was assigned and the failure occurred anyway: counter-case to part 3"}
    return {"state": "SIGNALLED_UNJOINED", "rests_on": ["signal_present", "signal_reported", "join_assigned"]}


def holder_count(rec):
    """Int if declared, UNDECLARED otherwise; a count is never inferred."""
    v = rec.get("holder_count", "UNDECLARED")
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        return "UNDECLARED" if v == "UNDECLARED" else "MALFORMED"
    return v


def lead_time(rec):
    """{'value','unit'} if declared with a unit; UNDECLARED otherwise.
    A number with no unit is UNDECLARED: hours and years are not one scale."""
    v = rec.get("time_first_signal_to_event", "UNDECLARED")
    if v == "UNDECLARED":
        return "UNDECLARED"
    if isinstance(v, dict) and isinstance(v.get("value"), (int, float)) and v.get("unit"):
        return {"value": v["value"], "unit": v["unit"]}
    return "UNDECLARED"


def separation(corpus):
    """Step 1's test, run within a failure corpus: does the DESCRIBED axis
    (sudden / quiet / neither) separate from the SIGNAL axis (signalled /
    unsignalled)? Returns the cross-tab and a verdict. NOT_EVALUABLE when
    the signal axis has one level -- a corpus with no genuinely
    unsignalled case cannot separate anything (CONSTANT_FIRES)."""
    tab = {}
    skipped = {"NOT_EVALUABLE": 0, "MALFORMED": 0, "UNDECLARED_description": 0}
    for rec in corpus:
        c = classify(rec)
        if c["state"] in ("NOT_EVALUABLE", "MALFORMED"):
            skipped[c["state"]] += 1
            continue
        d = rec.get("described_as", "UNDECLARED")
        if d not in DESCRIBED or d == "UNDECLARED":
            skipped["UNDECLARED_description"] += 1
            continue
        sig = "UNSIGNALLED" if c["state"] == "GENUINELY_UNSIGNALLED" else "SIGNALLED"
        tab[(d, sig)] = tab.get((d, sig), 0) + 1
    levels = {k[1] for k in tab}
    n = sum(tab.values())
    out = {"n_coded": n, "skipped": skipped,
           "table": {"%s|%s" % k: v for k, v in sorted(tab.items())}}
    if n == 0:
        out["state"] = "NOT_EVALUABLE"
        out["why"] = "no case reached the table"
        return out
    if len(levels) < 2:
        out["state"] = "NOT_EVALUABLE"
        out["why"] = "signal axis has one level (%s); nothing to separate from" % levels.pop()
        return out
    sudden_sig = tab.get(("SUDDEN", "SIGNALLED"), 0)
    sudden_all = sum(v for k, v in tab.items() if k[0] == "SUDDEN")
    out["sudden_cases_signalled"] = [sudden_sig, sudden_all]
    out["state"] = "SEPARATES" if sudden_sig and sudden_all and sudden_sig == sudden_all else "DOES_NOT_SEPARATE"
    out["rule"] = "SEPARATES iff every case described SUDDEN classifies SIGNALLED [CHOICE 1: strict]"
    return out


def base_rate(corpus, frame="accident_investigation_corpus"):
    """Refused. A corpus of investigated accidents is selected on failure;
    a rate of signalled-unjoined failures over SYSTEMS wants the
    population of systems that did not fail, which such a corpus does
    not carry. Returns the refusal and what would lift it."""
    return {"state": "REFUSED_SAMPLING_FRAME", "frame": frame,
            "why": "corpus selected on the outcome; no denominator over systems",
            "lifts_on": "a frame chosen before outcome (systems instrumented, then followed)",
            "n_in_corpus": len(corpus)}


def order_cases(text=None):
    """The order's Cases bullets, parsed: name (upper-case lead) and body."""
    text = text or order_text()
    m = re.search(r"## Cases\n\n(.*?)\n\n## Evidence", text, re.S)
    if not m:
        raise ValueError("Cases section not found")
    bullets = re.split(r"\n(?=- )", m.group(1).strip())
    out = []
    for b in bullets:
        body = re.sub(r"\s+", " ", b[2:]).strip()
        name = re.match(r"([A-Z][A-Z ,0-9]+?)(?:,| in |\.)", body)
        out.append({"name": name.group(1).strip() if name else body[:30], "body": body,
                    "status": "CARRIED_NOT_VERIFIED"})
    return out


def _span(body, phrase):
    i = body.find(phrase)
    if i < 0:
        raise ValueError("phrase not in body: %r" % phrase)
    return [i, i + len(phrase)]


def carried_codings(text=None):
    """This session's coding of the order's cases FROM THE ORDER'S OWN
    SENTENCES. Each code carries the phrase it rests on (span into the
    case body); a field the order's text does not reach is UNSEARCHED or
    UNDECLARED. This is a reading, not a blind coding (step 2)."""
    cases = {c["name"]: c for c in order_cases(text)}
    sb, co = cases["SILVER BRIDGE"], cases["COLUMBIA"]
    tq = [c for c in cases.values() if c["name"].startswith("TACOMA")][0]
    qf = [c for c in cases.values() if c["name"].startswith("QUIET")][0]
    return [
        {"case": sb["name"], "coder": "this session", "saw_decomposition": True,
         "signal_present": "PRESENT", "signal_reported": "ABSENT",
         "join_assigned": "UNSEARCHED", "holder_count": "UNDECLARED",
         "time_first_signal_to_event": "UNDECLARED", "described_as": "UNDECLARED",
         "basis": {"signal_present": _span(sb["body"], "Fracture initiated inside a joint"),
                   "signal_reported": _span(sb["body"], "not inspectable without disassembly"),
                   "event_duration": _span(sb["body"], "in under a minute")},
         "note": "'in under a minute' is the duration of the collapse, not how it was described afterwards; described_as stays UNDECLARED"},
        {"case": co["name"], "coder": "this session", "saw_decomposition": True,
         "signal_present": "PRESENT", "signal_reported": "PRESENT",
         "join_assigned": "UNASSIGNED", "holder_count": "UNDECLARED",
         "time_first_signal_to_event": "UNDECLARED", "described_as": "UNDECLARED",
         "basis": {"signal_present": _span(co["body"], "Foam strike known during flight"),
                   "signal_reported": _span(co["body"], "Imaging requests made and denied through proper channels"),
                   "join_assigned": _span(co["body"], "Every step in procedure")}},
        {"case": tq["name"], "coder": "this session", "saw_decomposition": True,
         "signal_present": "UNSEARCHED", "signal_reported": "UNSEARCHED",
         "join_assigned": "UNSEARCHED", "holder_count": "UNDECLARED",
         "time_first_signal_to_event": "UNDECLARED", "described_as": "UNDECLARED",
         "basis": {"note": _span(tq["body"], "The failures that wrote the")}},
        {"case": qf["name"], "coder": "this session", "saw_decomposition": True,
         "signal_present": "PRESENT", "signal_reported": "UNSEARCHED",
         "join_assigned": "UNSEARCHED", "holder_count": "UNDECLARED",
         "time_first_signal_to_event": "UNDECLARED", "described_as": "QUIET",
         "basis": {"signal_present": _span(qf["body"], "inspectable in principle"),
                   "described_as": _span(qf["body"], "invisible to the operating system itself")}},
    ]


def constructed_corpus():
    """A CONSTRUCTED corpus that reaches every class and both separation
    verdicts. Not a case list; the names say so."""
    base = {"holder_count": 3, "time_first_signal_to_event": {"value": 14, "unit": "month"}}
    mk = lambda **kw: dict(base, **kw)
    return {
        "separates": [
            mk(case="C-1", signal_present="PRESENT", signal_reported="PRESENT", join_assigned="UNASSIGNED", described_as="SUDDEN"),
            mk(case="C-2", signal_present="PRESENT", signal_reported="PRESENT", join_assigned="UNASSIGNED", described_as="QUIET"),
            mk(case="C-3", signal_present="ABSENT", signal_reported="ABSENT", join_assigned="UNSEARCHED", described_as="NEITHER"),
        ],
        "does_not": [
            mk(case="C-4", signal_present="ABSENT", signal_reported="ABSENT", join_assigned="UNSEARCHED", described_as="SUDDEN"),
            mk(case="C-5", signal_present="PRESENT", signal_reported="PRESENT", join_assigned="UNASSIGNED", described_as="SUDDEN"),
            mk(case="C-6", signal_present="PRESENT", signal_reported="PRESENT", join_assigned="ASSIGNED", described_as="QUIET"),
        ],
        "one_level": [
            mk(case="C-7", signal_present="PRESENT", signal_reported="PRESENT", join_assigned="UNASSIGNED", described_as="SUDDEN"),
            mk(case="C-8", signal_present="PRESENT", signal_reported="ABSENT", join_assigned="UNSEARCHED", described_as="SUDDEN"),
        ],
    }


def render(corpus_path=None):
    lines = ["decomposition -- step 1 as a coder; the order's cases coded from its own text",
             "  egress (measured %s): %s" % (EGRESS["measured"], "; ".join("%s %s" % kv for kv in EGRESS["hosts"].items())),
             "  no accident corpus was read; the codings below are THIS SESSION'S READING of the order's sentences",
             "  parts (parsed from the order):"]
    for i, p in enumerate(parts(), 1):
        lines.append("    %d. %s" % (i, p[:88]))
    lines.append("  order's cases, coded from the order's text (span = the phrase the code rests on):")
    for rec in carried_codings():
        c = classify(rec)
        lines.append("    %-40s -> %-22s holders %s  lead %s  described %s" % (
            rec["case"][:40], c["state"], holder_count(rec), lead_time(rec), rec["described_as"]))
        for f, sp in rec["basis"].items():
            body = [x for x in order_cases() if x["name"] == rec["case"]][0]["body"]
            lines.append("        %-16s %-11s <- %r" % (f, rec.get(f, ""), body[sp[0]:sp[1]]))
    sep = separation(carried_codings())
    lines.append("  separation on the order's cases: %s -- %s" % (sep["state"], sep.get("why", sep.get("rule", ""))))
    lines.append("  base rate: %s (%s)" % (base_rate(carried_codings())["state"], base_rate([])["why"]))
    if corpus_path:
        corpus = json.load(open(corpus_path))
        lines.append("  supplied corpus (%d records):" % len(corpus))
        for rec in corpus:
            lines.append("    %-20s -> %s" % (str(rec.get("case", "?"))[:20], classify(rec)["state"]))
        lines.append("  separation: %s" % json.dumps(separation(corpus), sort_keys=True))
    else:
        cc = constructed_corpus()
        lines.append("  CONSTRUCTED corpora (not cases): separates -> %s; does_not -> %s; one_level -> %s" % (
            separation(cc["separates"])["state"], separation(cc["does_not"])["state"], separation(cc["one_level"])["state"]))
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("library module; run: python3 selftest.py")
        sys.exit(2)
    p = sys.argv[sys.argv.index("--corpus") + 1] if "--corpus" in sys.argv else None
    print(render(p))
