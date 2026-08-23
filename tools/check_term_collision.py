#!/usr/bin/env python3
"""
check_term_collision.py -- who uses the colliding terms, and who declares
which sense.

CC0-1.0. Stdlib only. Run from anywhere in the repo.

    python3 tools/check_term_collision.py [repo_root]

WHY THIS EXISTS
---------------
PREAMBLE.md carries a NOTE TO READERS -- TERM COLLISION. Two phrases each
name two distinct objects:

  "change of mind"  REVISION (provenance-bearing, cause named, move logged)
                    vs ASSERTION (no cause named, the criterion moved and
                    nothing records that it moved)

  "self-questioning" / "constant re-evaluation"
                    continuous calibration concurrent with operation, an
                    expertise marker in the surgical and aviation
                    literature -- NOT a confidence deficit

The note says to place it at the head of any module using these terms. This
finds them, and reports which of those carry the note.

WHAT IT FOUND, AND WHY THAT IS THE INTERESTING PART
---------------------------------------------------
Almost nothing. A literal-string scan of this repo returns a handful of hits
and the incidental ones dominated: the first run reported eight, of which
five were the substring `reEvaluat` inside `ObserverAwareEvaluator` -- a
missing word boundary, and the majority of the result. With `\b` in place
the count is three, one of which is this note's own placement. The repo uses
the CONCEPTS constantly (criteria-drift is a whole folder about rulers
moving) and the PHRASES almost never.

That is a real result about the instrument, not about the repo. A term
collision is about which sense is meant WHEN a term is used, so a scanner
keyed on the term's surface form cannot find the places where the collision
would actually bite -- those are the places doing the thing without naming
it. This scanner reports what it can see and says plainly that the set it
cannot see is the larger one. It is a placement aid, not a coverage claim.

A near-zero hit count must not be read as "the repo is clear". It means the
scan does not apply, which is a different state and is printed as one.
"""

import os
import re
import sys

# Surface forms only. This is the whole limitation and it is deliberate:
# a stemmer or a synonym list would widen the net without making the result
# mean more, and would hide the limitation behind a bigger number.
TERMS = {
    "change of mind": r"change[sd]?\s+of\s+mind|changed\s+(?:my|his|her|their|its)\s+mind",
    "self-questioning": r"self[-\s]question",
    "constant re-evaluation":
        r"\b(?:constant|continuous|ongoing)\s+re-?evaluat",
    # \b matters: without it this matches INSIDE `AwareEvaluator`, which
    # produced five of eight hits on the first run -- a word-boundary
    # false positive, and the majority of the result.
    "re-evaluation (bare)": r"\bre-?evaluat",
}

NOTE_MARKER = "TERM COLLISION"

SKIP_DIRS = {".git", "__pycache__", "node_modules", "legacy"}
EXTS = (".py", ".md")

RULE = "=" * 70


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            if name.endswith(EXTS):
                yield os.path.join(dirpath, name)


def scan(root):
    """Every hit, with its term, file and line. No interpretation here."""
    hits = []
    for path in walk(root):
        try:
            text = open(path, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        rel = os.path.relpath(path, root)
        if rel == os.path.join("tools", "check_term_collision.py"):
            continue                      # the scanner's own term list
        if rel == "PREAMBLE.md":
            continue                      # the note itself
        lines = text.splitlines()
        for term, pattern in TERMS.items():
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.I):
                    hits.append({"term": term, "file": rel, "line": i,
                                 "text": line.strip()[:88],
                                 "declares": NOTE_MARKER in text})
    return hits


def by_module(hits, root):
    out = {}
    for h in hits:
        mod = h["file"].split(os.sep)[0]
        if mod.endswith((".py", ".md")):
            mod = "<root>"
        out.setdefault(mod, []).append(h)
    return out


def note_in_preamble(root):
    p = os.path.join(root, "PREAMBLE.md")
    if not os.path.exists(p):
        return False
    return NOTE_MARKER in open(p, encoding="utf-8",
                               errors="replace").read()


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    root = os.path.abspath(root)
    print(RULE)
    print("TERM COLLISION CHECK  --  %s" % root)
    print(RULE)
    print()

    in_preamble = note_in_preamble(root)
    print("note present in PREAMBLE.md:  %s"
          % ("yes" if in_preamble else "NO"))
    print()

    hits = scan(root)
    mods = by_module(hits, root)

    print("terms scanned (surface form only):")
    for t in TERMS:
        n = sum(1 for h in hits if h["term"] == t)
        print("    %-26s %d" % (t, n))
    print()

    if not hits:
        print("no literal uses found outside PREAMBLE.md.")
    else:
        print("literal uses, by module:")
        print()
        for mod in sorted(mods):
            declared = sum(1 for h in mods[mod] if h["declares"])
            print("  %-24s %d hit%s, %d in files that declare the note"
                  % (mod, len(mods[mod]),
                     "" if len(mods[mod]) == 1 else "s", declared))
            for h in mods[mod]:
                print("      %s:%d  [%s]" % (h["file"], h["line"], h["term"]))
                print("        %s" % h["text"])
        print()

    undeclared = [h for h in hits if not h["declares"]]
    print(RULE)
    print()
    print("A NEAR-ZERO COUNT IS NOT A CLEAN BILL.")
    print()
    print("This scan keys on the surface form of the terms. A term")
    print("collision is about which sense is meant WHEN a term is used, so")
    print("the places where it bites hardest are the ones doing the thing")
    print("without naming it -- and those are invisible here. The repo uses")
    print("the concepts constantly and the phrases almost never.")
    print()
    print("Reported state: SCAN_DOES_NOT_APPLY, not CLEAR.")
    print()
    print("HITS ARE NOT CLASSIFIED BY SENSE, AND THAT IS THE JUDGEMENT")
    print("THAT MATTERS. A program re-computing a decayed claim and a")
    print("person describing how they operate both match the same string.")
    print("Only the second is what the note is about. Deciding which is")
    print("which is a reading of intent, so this tool lists and does not")
    print("sort -- the sense column would be a regex guessing at meaning.")
    print()
    print("%d literal use%s, %d in files that do not carry the note."
          % (len(hits), "" if len(hits) == 1 else "s", len(undeclared)))
    print()
    if not in_preamble:
        print("PREAMBLE.md does not carry the note. That is the one")
        print("placement the note names explicitly.")
        print(RULE)
        return 1
    print("PREAMBLE.md carries it, which is the placement the note names.")
    print("Per-module heads are a judgement about which modules use the")
    print("terms, and this tool does not make that judgement for anyone.")
    print(RULE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
