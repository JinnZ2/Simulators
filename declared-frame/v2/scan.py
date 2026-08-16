#!/usr/bin/env python3
"""
scan.py -- run patterns.json over text.

CC0-1.0. Standard library only. Deterministic.

    python3 scan.py FILE [FILE ...]
    python3 scan.py --raw FILE          # no word boundaries (see below)

RECONSTRUCTED. patterns.json was delivered without a runner, so the
behaviours the trigger list does not fix are marked [CHOICE] below and are
the first place to look if a result here disagrees with the intent.

    [CHOICE] case-insensitive matching. The triggers are written lowercase
             with alternations, and prose capitalizes sentence-initially.

    [CHOICE] word boundaries (\\b) around each trigger by default. Without
             them "lean" matches "cleaning" and "clean"; "slack" matches
             "slacken". `--raw` turns them off so the cost of the choice can
             be measured rather than assumed -- see scan_audit.py section 4.

    [CHOICE] one hit per (mechanism, trigger, line). Two triggers in one
             mechanism matching the same line are two hits, because they are
             independent tells; the same trigger matching twice on a line is
             one.

The file's own framing is load-bearing and is not a hedge to be discounted:

    "Triggers are surface tells, not classifiers. Every hit is a candidate
     for triage, not a finding. 'check' is the question a human answers to
     keep or discard the hit."

So the quantity that decides whether the scanner is usable is not precision.
It is TRIAGE LOAD: how many candidates a human must answer `check` on per
unit of text. scan_audit.py measures it.
"""

from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATTERNS = os.path.join(HERE, "patterns.json")


def load_patterns(path=PATTERNS):
    with open(path, encoding="utf-8") as fh:
        doc = json.load(fh)
    return {k: v for k, v in doc.items() if not k.startswith("_")}


def compile_triggers(patterns, boundaries=True):
    out = {}
    for mech, spec in patterns.items():
        rules = []
        for t in spec["triggers"]:
            pat = r"\b(?:%s)\b" % t if boundaries else t
            rules.append((t, re.compile(pat, re.IGNORECASE)))
        out[mech] = rules
    return out


def scan_text(text, rules):
    """Returns [(mechanism, trigger, lineno, matched_text, line)]."""
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for mech, triggers in rules.items():
            for trig, rx in triggers:
                m = rx.search(line)
                if m:
                    hits.append((mech, trig, lineno, m.group(0), line.strip()))
    return hits


def scan_file(path, rules):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return scan_text(fh.read(), rules)


def word_count(text):
    return len(text.split())


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    boundaries = "--raw" not in argv
    if not args:
        print(__doc__)
        return 2

    patterns = load_patterns()
    rules = compile_triggers(patterns, boundaries)

    total = 0
    for path in args:
        hits = scan_file(path, rules)
        total += len(hits)
        print("=" * 68)
        print("%s -- %d candidate%s" % (path, len(hits),
                                        "" if len(hits) == 1 else "s"))
        print("=" * 68)
        by_mech = {}
        for mech, trig, lineno, matched, line in hits:
            by_mech.setdefault(mech, []).append((trig, lineno, matched, line))
        for mech in sorted(by_mech):
            print("\n  %s -- %s" % (mech, patterns[mech]["reads"]))
            print("  check: %s" % patterns[mech]["check"])
            for trig, lineno, matched, line in by_mech[mech]:
                snip = line if len(line) <= 60 else line[:57] + "..."
                print("    L%-5d %-22r %s" % (lineno, matched, snip))
        if not hits:
            print("\n  (no candidates)")
    print()
    print("%d candidate%s across %d file%s"
          % (total, "" if total == 1 else "s", len(args),
             "" if len(args) == 1 else "s"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
