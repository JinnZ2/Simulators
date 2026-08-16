#!/usr/bin/env python3
# scan.py -- uninstrumented candidate scanner
# CC0-1.0. Public domain. Standard library only.
#
# Searches text for the SIGNATURE OF AN EXCLUSION, not for topics.
# Every hit is a candidate for triage. Most hits are noise.
# This is a curiosity engine, not a classifier.
#
#   python3 scan.py FILE_OR_DIR [FILE_OR_DIR ...]
#   python3 scan.py --mech "SCORED AS WASTE" docs/
#   python3 scan.py --asym transcripts/          (audit-asymmetry count)
#   python3 scan.py --jsonl out.jsonl docs/      (machine-readable)

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERNS_PATH = os.path.join(HERE, "patterns.json")

TEXT_EXT = (".txt", ".md", ".rst", ".org", ".csv", ".json", ".jsonl", ".py")

# Sentence split. Deliberately crude: over-splitting costs nothing here.
SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\"'\[])|\n{2,}")

# Conditioning terms. Presence near a SCALAR DEMAND hit weakens it.
CONDITIONERS = re.compile(
    r"\b(when|during|if|context|situation|condition|domain|"
    r"depend(s|ing)?|varies|by (task|target|item|setting))\b",
    re.I,
)

HEDGES = re.compile(
    r"\b(anecdot\w+|self[- ]reported|subjective|unverified|"
    r"uncorroborated|with caution|may be biased|reportedly|"
    r"alleged\w*|claims? to)\b",
    re.I,
)

# Crude account-type split for --asym. Extend for your corpus.
OUTSIDE = re.compile(
    r"\b(driver|drivers|worker|workers|operator|operators|patient|"
    r"patients|resident|residents|user|users|respondent|respondents|"
    r"witness|witnesses|farmer|farmers|technician|technicians)\b",
    re.I,
)
INCUMBENT = re.compile(
    r"\b(agency|agencies|regulator\w*|institut\w+|department|"
    r"administration|committee|board|manufacturer|industry|"
    r"stud(y|ies)|literature|guideline\w*|standard\w*|official\w*)\b",
    re.I,
)


def load_patterns(path=PATTERNS_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        raw = json.load(fh)
    out = {}
    for mech, spec in raw.items():
        if mech.startswith("_"):
            continue
        out[mech] = {
            "reads": spec.get("reads", ""),
            "check": spec.get("check", ""),
            "rx": [re.compile(t, re.I) for t in spec.get("triggers", [])],
        }
    return out


def walk(targets):
    for t in targets:
        if os.path.isfile(t):
            yield t
        elif os.path.isdir(t):
            for root, _dirs, files in os.walk(t):
                for f in sorted(files):
                    if f.lower().endswith(TEXT_EXT):
                        yield os.path.join(root, f)


def sentences(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError as exc:
        sys.stderr.write("skip %s: %s\n" % (path, exc))
        return
    line = 1
    for chunk in SENT.split(text):
        if chunk is None:
            continue
        s = " ".join(chunk.split())
        if len(s) >= 20:
            yield line, s
        line += chunk.count("\n") + 1


def score(mech, sent):
    """Cheap confidence gradient. Reported, never used to filter."""
    if mech == "SCALAR DEMAND" and CONDITIONERS.search(sent):
        return "weak"     # conditioning present; may not be collapsed
    if mech == "AUDIT ASYMMETRY" and not HEDGES.search(sent):
        return "weak"
    if len(sent) > 400:
        return "weak"     # probably swept up a whole paragraph
    return "candidate"


def scan(targets, patterns, only=None):
    hits = []
    for path in walk(targets):
        for lineno, sent in sentences(path):
            for mech, spec in patterns.items():
                if only and mech != only:
                    continue
                for rx in spec["rx"]:
                    m = rx.search(sent)
                    if m:
                        hits.append({
                            "file": path,
                            "line": lineno,
                            "mechanism": mech,
                            "trigger": m.group(0),
                            "sentence": sent,
                            "check": spec["check"],
                            "strength": score(mech, sent),
                        })
                        break
    return hits


def asym(targets):
    """Count hedges by account type. Runs on transcripts you already have."""
    tally = {}
    for path in walk(targets):
        out_h = out_n = inc_h = inc_n = 0
        for _lineno, sent in sentences(path):
            hedged = bool(HEDGES.search(sent))
            if OUTSIDE.search(sent):
                out_n += 1
                out_h += hedged
            if INCUMBENT.search(sent):
                inc_n += 1
                inc_h += hedged
        if out_n or inc_n:
            tally[path] = (out_h, out_n, inc_h, inc_n)
    return tally


def report(hits):
    if not hits:
        print("no candidates")
        return
    by_mech = {}
    for h in hits:
        by_mech.setdefault(h["mechanism"], []).append(h)
    for mech in sorted(by_mech):
        group = by_mech[mech]
        print("=" * 62)
        print("%s  (%d)" % (mech, len(group)))
        print("=" * 62)
        print("CHECK: %s" % group[0]["check"])
        print()
        for h in group:
            s = h["sentence"]
            if len(s) > 300:
                s = s[:297] + "..."
            print("  [%s] %s:%d" % (h["strength"], h["file"], h["line"]))
            print("      trigger: %s" % h["trigger"])
            print("      %s" % s)
            print()


def report_asym(tally):
    print("AUDIT ASYMMETRY -- hedge rate by account type")
    print("ratio > 1 means the outside account is hedged more often.")
    print()
    for path in sorted(tally):
        oh, on_, ih, in_ = tally[path]
        r_out = (oh / on_) if on_ else 0.0
        r_inc = (ih / in_) if in_ else 0.0
        ratio = (r_out / r_inc) if r_inc else float("inf") if r_out else 0.0
        print("  %s" % path)
        print("    outside   %3d/%-4d  %.3f" % (oh, on_, r_out))
        print("    incumbent %3d/%-4d  %.3f" % (ih, in_, r_inc))
        print("    ratio     %s" % ("inf" if ratio == float("inf")
                                    else "%.2f" % ratio))
        print()
    print("NOTE: sentence-level co-occurrence, not attribution.")
    print("The number is a pointer. Read the flagged sentences.")


def main(argv):
    args = list(argv[1:])
    only = None
    jsonl = None
    mode = "scan"
    targets = []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--mech":
            i += 1
            only = args[i]
        elif a == "--jsonl":
            i += 1
            jsonl = args[i]
        elif a == "--asym":
            mode = "asym"
        elif a in ("-h", "--help"):
            print(__doc__ or "see header")
            return 0
        else:
            targets.append(a)
        i += 1

    if not targets:
        sys.stderr.write("usage: scan.py [--mech M] [--asym] "
                         "[--jsonl OUT] FILE_OR_DIR...\n")
        return 2

    if mode == "asym":
        report_asym(asym(targets))
        return 0

    patterns = load_patterns()
    if only and only not in patterns:
        sys.stderr.write("unknown mechanism: %s\nknown: %s\n"
                         % (only, ", ".join(sorted(patterns))))
        return 2

    hits = scan(targets, patterns, only)
    report(hits)
    if jsonl:
        with open(jsonl, "w", encoding="utf-8") as fh:
            for h in hits:
                fh.write(json.dumps(h) + "\n")
        print("wrote %d hits -> %s" % (len(hits), jsonl))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
