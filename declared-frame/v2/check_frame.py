#!/usr/bin/env python3
# check_frame.py -- validate and compare declared frame blocks
# CC0-1.0. Public domain. Standard library only.
#
#   python3 check_frame.py result_a.json [result_b.json]

import json
import sys

FIELDS = ["boundary", "horizon", "who_counts",
          "sign_source", "logic", "observer_access"]
ACCESS = ["unknown", "partial", "verified"]
CORE = ["boundary", "horizon", "who_counts"]


def validate(frame, label="frame"):
    problems = []
    for f in FIELDS:
        if f not in frame:
            problems.append(
                "%s: OMITTED field '%s'. Write 'unknown' instead -- "
                "omission reads as absence of the issue." % (label, f))
            continue
        v = frame[f]
        if v is None or (isinstance(v, str) and not v.strip()):
            problems.append("%s: EMPTY field '%s'" % (label, f))
    acc = frame.get("observer_access")
    if isinstance(acc, str) and acc.strip() and acc not in ACCESS:
        problems.append(
            "%s: BAD VALUE observer_access='%s' (expected %s)"
            % (label, acc, "|".join(ACCESS)))
    return problems


def unknowns(frame):
    return [f for f in FIELDS
            if str(frame.get(f, "")).strip().lower() == "unknown"]


def compare(a, b):
    ua, ub = unknowns(a), unknowns(b)
    if ua or ub:
        return ("UNDETERMINED",
                "unknown fields present: a=%s b=%s" % (ua or "-", ub or "-"))
    diffs = [f for f in CORE if a.get(f) != b.get(f)]
    if diffs:
        return ("NOT DIRECTLY COMPARABLE",
                "differs on %s -- this is a frame difference, "
                "not a finding" % ", ".join(diffs))
    if a.get("logic") != b.get("logic"):
        return ("LOGIC MISMATCH",
                "data may compare, conclusions do not (%s vs %s)"
                % (a.get("logic"), b.get("logic")))
    return ("DIRECTLY COMPARABLE", "core fields match")


def load(path):
    with open(path, "r", encoding="utf-8") as fh:
        doc = json.load(fh)
    return doc.get("frame", doc)


def main(argv):
    args = argv[1:]
    if not args:
        sys.stderr.write("usage: check_frame.py A.json [B.json]\n")
        return 2
    a = load(args[0])
    problems = validate(a, args[0])
    for p in problems:
        print(p)
    if not problems:
        print("%s: all six fields declared" % args[0])
    u = unknowns(a)
    if u:
        print("%s: unknown -> %s" % (args[0], ", ".join(u)))
    if len(args) > 1:
        b = load(args[1])
        for p in validate(b, args[1]):
            print(p)
        verdict, why = compare(a, b)
        print()
        print("VERDICT: %s" % verdict)
        print("         %s" % why)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
