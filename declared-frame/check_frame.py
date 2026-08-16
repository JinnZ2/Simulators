#!/usr/bin/env python3
"""
check_frame.py -- validate declared frame blocks and test
two results for comparability.

    python3 check_frame.py result_a.json
    python3 check_frame.py result_a.json result_b.json

Does not resolve anything it cannot determine. Unknown
fields produce UNDETERMINED, never a pass or a fail.

CC0-1.0. stdlib only.
"""
import json
import sys

FIELDS = ("boundary", "horizon", "who_counts",
          "sign_source", "logic", "observer_access")

ACCESS = ("unknown", "partial", "verified")

# fields that must match for direct comparability
CORE = ("boundary", "horizon", "who_counts")


def validate(frame, label="frame"):
    problems = []
    for f in FIELDS:
        if f not in frame:
            problems.append(
                "OMITTED   %-16s -- write 'unknown' rather than "
                "leaving it out. An omitted field reads as "
                "absence." % f)
        elif not str(frame[f]).strip():
            problems.append("EMPTY     %-16s" % f)
    acc = str(frame.get("observer_access", "")).lower()
    if acc and acc not in ACCESS:
        problems.append(
            "BAD VALUE observer_access must be one of %r" % (ACCESS,))
    return problems


def unknowns(frame):
    return [f for f in FIELDS
            if str(frame.get(f, "")).strip().lower() == "unknown"]


def compare(a, b):
    print("COMPARABILITY\n")
    undet = []
    diffs = []
    for f in CORE:
        va = str(a.get(f, "")).strip()
        vb = str(b.get(f, "")).strip()
        if va.lower() == "unknown" or vb.lower() == "unknown":
            undet.append(f)
        elif va != vb:
            diffs.append((f, va, vb))

    la, lb = str(a.get("logic", "")), str(b.get("logic", ""))
    logic_diff = (la.lower() != "unknown" and lb.lower() != "unknown"
                  and la != lb)

    if undet:
        print("  UNDETERMINED -- unknown on: %s" % ", ".join(undet))
        print("  Not incomparable. Not comparable. Undetermined.")
        print()

    if diffs:
        print("  NOT DIRECTLY COMPARABLE")
        for f, va, vb in diffs:
            print("    %-12s A: %s" % (f, va))
            print("    %-12s B: %s" % ("", vb))
        print("  The difference between these results is a frame")
        print("  difference. Reporting it as a finding is an error.")
        print()

    if logic_diff:
        print("  LOGIC MISMATCH   A: %s   B: %s" % (la, lb))
        print("  Data may still compare. The inferences drawn from")
        print("  each are valid in different systems and do not.")
        print()

    if not undet and not diffs and not logic_diff:
        print("  DIRECTLY COMPARABLE on all declared fields.")
        print()


def load(path):
    with open(path) as fh:
        doc = json.load(fh)
    return doc.get("frame", doc)


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        return 2

    frames = [(p, load(p)) for p in sys.argv[1:]]

    rc = 0
    for path, fr in frames:
        print("=" * 62)
        print("FRAME  %s" % path)
        print("=" * 62)
        probs = validate(fr)
        for f in FIELDS:
            v = fr.get(f, "<omitted>")
            print("  %-16s %s" % (f, v))
        print()
        unk = unknowns(fr)
        if unk:
            print("  DECLARED UNKNOWN: %s" % ", ".join(unk))
            print("  These are visible gaps. Legal, and explorable.")
            print()
        if probs:
            rc = 1
            for p in probs:
                print("  " + p)
            print()

    if len(frames) == 2:
        print("=" * 62)
        compare(frames[0][1], frames[1][1])

    return rc


if __name__ == "__main__":
    sys.exit(main())
