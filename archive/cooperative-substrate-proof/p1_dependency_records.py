#!/usr/bin/env python3
"""P1 -- dependency records. RECORDS, not prose.

THE MOVE. Given any result, enumerate what it REQUIRED that does not
appear in its argument: instruments, calibration chains, inherited
methods, materials, infrastructure, prior results. Every record carries
a SOURCE -- the document, the line, the character span, and the literal
text -- and a record whose span does not slice out its own text is
refused as UNSOURCED (typed), never scored.

    enumerate_preconditions(methods_text, argument_text, doc)
        -> records + ratio(unargued / total)

`in_argument` is true when the requirement's head token occurs in the
ARGUMENT text (the results/claims section). The reading the dispatch
asks for is the complement: requirements the argument does not mention.

PIPELINE. Open-access methods sections. None is reachable from this
environment (egress is an allowlist) and none is transcribed from
memory, so the shipped input is `fixtures/methods_CONSTRUCTED.txt`,
labelled so in its first line. Paste a real one:

    python3 p1_dependency_records.py --methods m.txt --argument r.txt

LIMITS, stated at the top. [CHOICE 9] the pattern set is a word list in
both directions: a dependency stated outside its vocabulary is not
counted (recall floor), and prose in the methods register can match
without being a dependency (precision is a reading, not a count). The
ratio is `undefined` when nothing is argued, never a large number.

STATES per record: SOURCED | UNSOURCED.  Corpus: RECORDS | EMPTY.
Refuses --selftest (checks live in selftest.py).
"""
import json
import re
import sys

CLASSES = ("INSTRUMENT", "CALIBRATION", "METHOD", "MATERIAL", "INFRASTRUCTURE", "PRIOR_RESULT")

# [CHOICE 9] pattern set, one dict, every entry a (class, regex).
PATTERNS = {
    "INSTRUMENT": r"\b(sampler|balance|oven|spectrometer|sensor|probe|thermometer|gauge|microscope|counter|telescope|DEM)\b",
    "CALIBRATION": r"\b(calibrated|traceable|reference mass|reference standard|standard reference|NIST|BIPM|certified)\b",
    "METHOD": r"\b(following|according to|as described in|protocol of)\s+[A-Z][A-Za-z\-]+ et al\.? \(\d{4}\)",
    "MATERIAL": r"\b(reagent|solvent|primer|antibody|standard solution|split-tube|core[s]?)\b",
    "INFRASTRUCTURE": r"\b(database|field station|grid power|network|repository|archive|laboratory)\b",
    "PRIOR_RESULT": r"\b(previously reported|prior work|established by|known from)\b",
}
STOP = {"the", "a", "an", "of", "on", "in", "at", "to", "and", "with", "by", "for", "was", "were"}


def _head(text, cls=None):
    """Head token: the cited author for METHOD, else the last content word."""
    if cls == "METHOD":
        caps = re.findall(r"\b[A-Z][A-Za-z\-]+", text)
        if caps:
            return caps[0].lower()
    toks = [t.lower() for t in re.findall(r"[A-Za-z][A-Za-z\-]+", text) if t.lower() not in STOP]
    return toks[-1] if toks else text.lower()


def enumerate_preconditions(methods, argument, doc="<methods>"):
    """The reusable move. Returns {state, records, n, unargued, ratio}."""
    if not methods or not methods.strip():
        return {"state": "EMPTY", "records": [], "n": 0, "unargued": 0, "ratio": None}
    arg_tokens = set(t.lower() for t in re.findall(r"[A-Za-z][A-Za-z\-]+", argument or ""))
    line_starts = [0]
    for i, ch in enumerate(methods):
        if ch == "\n":
            line_starts.append(i + 1)
    records = []
    for cls, pat in PATTERNS.items():
        for m in re.finditer(pat, methods):
            line = max(i for i, s in enumerate(line_starts) if s <= m.start()) + 1
            head = _head(m.group(0), cls)
            records.append({"class": cls, "requirement": m.group(0), "head": head,
                            "in_argument": head in arg_tokens,
                            "source": {"doc": doc, "line": line, "span": [m.start(), m.end()],
                                       "text": m.group(0)}})
    records = [validate(r, methods) for r in records]
    sourced = [r for r in records if r["state"] == "SOURCED"]
    unargued = sum(1 for r in sourced if not r["in_argument"])
    argued = len(sourced) - unargued
    return {"state": "RECORDS" if records else "EMPTY", "records": records, "n": len(sourced),
            "unsourced": len(records) - len(sourced), "unargued": unargued,
            "ratio": (unargued / argued) if argued else None}


def validate(rec, methods):
    """A record is SOURCED only if its span slices out its own text."""
    s = rec.get("source") or {}
    span = s.get("span")
    ok = (isinstance(span, list) and len(span) == 2 and methods[span[0]:span[1]] == s.get("text"))
    rec = dict(rec)
    rec["state"] = "SOURCED" if ok else "UNSOURCED"
    return rec


def render(res, label):
    lines = ["P1 dependency records  input=%s" % label, "state   %s" % res["state"]]
    for r in res["records"]:
        src = r["source"]
        lines.append("  %-9s %-15s %-28s in_argument=%-5s %s:%d[%d:%d]"
                     % (r["state"], r["class"], r["requirement"][:28], r["in_argument"],
                        src["doc"], src["line"], src["span"][0], src["span"][1]))
    lines.append("records %d sourced, %d unsourced; %d unargued; ratio unargued/argued = %s"
                 % (res["n"], res.get("unsourced", 0), res["unargued"],
                    "undefined" if res["ratio"] is None else "%.2f" % res["ratio"]))
    lines.append("[CHOICE 9] pattern set is a word list; counts are a recall floor, precision is a reading")
    return "\n".join(lines)


def split_fixture(text):
    m = text.find("RESULTS")
    return (text[:m], text[m:]) if m >= 0 else (text, "")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("p1_dependency_records.py holds no checks; run python3 selftest.py\n")
        return 2
    import os
    if "--methods" in argv:
        mp = argv[argv.index("--methods") + 1]
        ap = argv[argv.index("--argument") + 1] if "--argument" in argv else None
        methods = open(mp, encoding="utf-8").read()
        argument = open(ap, encoding="utf-8").read() if ap else ""
        label = mp
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        label = "fixtures/methods_CONSTRUCTED.txt (CONSTRUCTED; no published section reachable)"
        methods, argument = split_fixture(open(os.path.join(here, "fixtures", "methods_CONSTRUCTED.txt"), encoding="utf-8").read())
    res = enumerate_preconditions(methods, argument, doc=label.split(" ")[0])
    print(render(res, label))
    if "--json" in argv:
        print(json.dumps(res["records"], indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
