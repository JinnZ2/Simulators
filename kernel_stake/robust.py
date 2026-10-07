#!/usr/bin/env python3
"""Two robustness checks on M1, both ADDED -- neither is in the order.

R-A  denominator: driver trees carry generated register headers, which
     inflate KLOC and deflate commits/KLOC across the whole STAKE class,
     not just amdgpu.  Re-run M1 with files as the denominator.
R-B  class membership: A and B disagree on half the list.  Re-run M1
     under classifier B's repaired assignment.
"""
import json, statistics, collections, sys
import subsystems as S

TAGS = [t for t, _d in S.TAGS]


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 3) if xs else None


def table(assign, denom):
    meas = json.load(open("measures.json"))
    kloc = json.load(open("kloc.json"))
    rows = []
    for i in range(1, len(TAGS)):
        k = "%s..%s" % (TAGS[i - 1], TAGS[i])
        tag = TAGS[i]
        agg = collections.defaultdict(list)
        for p in S.PATHS:
            c = meas["intervals"][k][p]["commits"]
            d = kloc[tag][p][denom]
            agg[assign[p]].append(c / (d / 1000.0) if d else None)
        rows.append((k, med(agg["STAKE_SPECIFIC"]), med(agg["SHARED_CORE"]),
                     med(agg["MIXED/UNCLEAR"])))
    return rows


def show(title, rows, unit):
    print(title)
    print("%-14s %9s %9s %9s" % ("interval", "STAKE", "CORE", "MIXED"))
    for k, a, b, c in rows:
        print("%-14s %9s %9s %9s" % (k, a, b, c))
    print("  unit: commits per 1000 %s" % unit)
    flips = sum(1 for _k, a, b, _c in rows if a is not None and b is not None
                and a >= b)
    print("  intervals where STAKE >= CORE: %d of %d" % (flips, len(rows)))
    print()


def selftest():
    n = 0
    def chk(c, name):
        nonlocal n; n += 1; assert c, name
    chk(med([]) is None, "empty -> None not 0")
    chk(med([1, None, 3]) == 2.0, "None dropped from median")
    chk(med([2]) == 2.0, "single")
    b = json.load(open("classifier_b.json"))["repaired/core_first"]
    chk(set(b) == set(S.PATHS), "B covers every path")
    chk(len(table(S.CLASS_A, "lines")) == 7, "seven intervals")
    print("checks: %d  failed: 0" % n)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest(); sys.exit(0)
    b = json.load(open("classifier_b.json"))["repaired/core_first"]
    show("R-0  as pre-registered: classifier A, KLOC denominator",
         table(S.CLASS_A, "lines"), "lines")
    show("R-A  classifier A, FILES denominator (generated-header check)",
         table(S.CLASS_A, "files"), "files")
    show("R-B  classifier B (repaired/core_first), KLOC denominator",
         table(b, "lines"), "lines")
    show("R-AB classifier B, FILES denominator",
         table(b, "files"), "files")
