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

# Exit codes. UNDETERMINED is deliberately not 1: it is neither a pass nor a
# failure, and a caller that treats it as either has resolved a gap the tool
# refused to resolve.
EXIT = {
    "DIRECTLY COMPARABLE": 0,
    "LOGIC MISMATCH": 1,
    "NOT DIRECTLY COMPARABLE": 1,
    "UNDETERMINED": 2,
}


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


def omitted(frame):
    """
    DF_002: the doc calls omission WORSE than 'unknown' -- it converts an
    open question into a settled one by silence. compare() read a missing
    field as "" and compared it as a VALUE, so omission produced NOT
    DIRECTLY COMPARABLE (settled) where the same gap declared as 'unknown'
    correctly produced UNDETERMINED (open). The more confident verdict for
    the worse case, in the function shipped to prevent exactly that.
    """
    return [f for f in CORE if f not in frame or frame.get(f) is None]


def compare(a, b):
    oa, ob = omitted(a), omitted(b)
    if oa or ob:
        return ("UNDETERMINED",
                "core field omitted: a=%s b=%s -- an omitted field is a gap, "
                "not a value. Write 'unknown' to make it visible."
                % (oa or "-", ob or "-"))
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
        # DF_004: main() returned 0 on every path, so
        # `check_frame.py a b && use_both` passed on two results the tool
        # had just said do not compare. v1 at least returned 1 on a
        # malformed block. The verdict is a value now, so it can be an exit
        # code -- the repair is only reachable because of the rewrite.
        return EXIT.get(verdict, 1)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
