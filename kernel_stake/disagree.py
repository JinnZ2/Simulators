#!/usr/bin/env python3
"""A vs B disagreement.  Published, not reconciled.  Neither is ground truth."""
import json, collections, sys
import subsystems as S

def load():
    return json.load(open("classifier_b.json"))

def rate(b):
    d = [p for p in S.PATHS if S.CLASS_A[p] != b[p]]
    return len(d) / len(S.PATHS), d

def matrix(b):
    m = collections.Counter((S.CLASS_A[p], b[p]) for p in S.PATHS)
    return m

def selftest():
    n = 0
    def chk(c, name):
        nonlocal n; n += 1; assert c, name
    chk(rate(dict(S.CLASS_A))[0] == 0.0, "identical -> 0.0")
    flip = {p: "MIXED/UNCLEAR" for p in S.PATHS}
    r, d = rate(flip)
    chk(len(d) == 36 - len(S.MIXED), "only non-mixed disagree")
    chk(abs(r - (36 - 9) / 36) < 1e-12, "rate arithmetic")
    chk(sum(matrix(dict(S.CLASS_A)).values()) == 36, "matrix totals 36")
    print("checks: %d  failed: 0" % n)

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    allb = load()
    for k in sorted(allb):
        b = allb[k]
        r, d = rate(b)
        print("=== B variant: %s ===" % k)
        print("disagreement rate: %d/36 = %.3f" % (len(d), r))
        m = matrix(b)
        print("  A \\ B            STAKE  CORE  MIXED")
        for a in ("STAKE_SPECIFIC", "SHARED_CORE", "MIXED/UNCLEAR"):
            print("  %-16s %5d %5d %6d" % (
                a, m[(a, "STAKE_SPECIFIC")], m[(a, "SHARED_CORE")],
                m[(a, "MIXED/UNCLEAR")]))
        print()
