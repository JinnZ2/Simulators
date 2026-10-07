#!/usr/bin/env python3
"""Output: per class per release, with the scope limits printed."""
import json, statistics, sys, collections
import subsystems as S

TAGS = [t for t, _d in S.TAGS]
LIMITS = """SCOPE LIMITS (printed with every result)
  author email is not who directed the work
  volunteer share is self-declared -- and is NOT_RUN here
  one project; nothing generalises
  activity, not code quality
  the 36-subsystem list is a convenience sample, not a random draw
  M2 UNKNOWN, M4 NOT_RUN, M5 NOT_RUN, M6-org BLOCKED (no employer map)
  classifier disagreement is 0.50-0.53; class membership is unstable"""


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.median(xs), 3) if xs else None


def load():
    return (json.load(open("measures.json")),
            json.load(open("kloc.json")),
            json.load(open("m3.json")))


def m1_cells(meas, kloc):
    """commits per KLOC, per (subsystem, interval-ending-tag)."""
    out = {}
    for i in range(1, len(TAGS)):
        key = "%s..%s" % (TAGS[i - 1], TAGS[i])
        tag = TAGS[i]
        out[key] = {}
        for p in S.PATHS:
            c = meas["intervals"][key][p]["commits"]
            lines = kloc[tag][p]["lines"]
            out[key][p] = (c / (lines / 1000.0)) if lines else None
    return out


def by_class(cells, key):
    agg = collections.defaultdict(list)
    for p, v in cells[key].items():
        agg[S.CLASS_A[p]].append(v)
    return agg


def main():
    meas, kloc, m3 = load()
    m1 = m1_cells(meas, kloc)
    print("=" * 74)
    print("M1  commits per KLOC  (median across subsystems in class)")
    print("=" * 74)
    print("%-14s %9s %9s %9s" % ("interval", "STAKE", "CORE", "MIXED"))
    for i in range(1, len(TAGS)):
        k = "%s..%s" % (TAGS[i - 1], TAGS[i])
        a = by_class(m1, k)
        print("%-14s %9s %9s %9s" % (
            k, med(a["STAKE_SPECIFIC"]), med(a["SHARED_CORE"]),
            med(a["MIXED/UNCLEAR"])))

    print()
    print("=" * 74)
    print("M6  bus factor  (median top-1 share / top-3 share, individuals)")
    print("=" * 74)
    print("%-14s %19s %19s %19s" % ("interval", "STAKE", "CORE", "MIXED"))
    for i in range(1, len(TAGS)):
        k = "%s..%s" % (TAGS[i - 1], TAGS[i])
        row = []
        for cl in ("STAKE_SPECIFIC", "SHARED_CORE", "MIXED/UNCLEAR"):
            t1 = med([meas["intervals"][k][p]["top1"] for p in S.PATHS
                      if S.CLASS_A[p] == cl])
            t3 = med([meas["intervals"][k][p]["top3"] for p in S.PATHS
                      if S.CLASS_A[p] == cl])
            row.append("%s / %s" % (t1, t3))
        print("%-14s %19s %19s %19s" % (k, row[0], row[1], row[2]))

    print()
    print("=" * 74)
    print("M3  maintainer count (median) / tenure years (median of medians)")
    print("=" * 74)
    print("%-8s %19s %19s %19s" % ("tag", "STAKE", "CORE", "MIXED"))
    for t in TAGS:
        row = []
        for cl in ("STAKE_SPECIFIC", "SHARED_CORE", "MIXED/UNCLEAR"):
            ps = [p for p in S.PATHS if S.CLASS_A[p] == cl]
            n = med([m3[t][p]["n_maintainers"] for p in ps])
            ten = med([m3[t][p]["tenure_median"] for p in ps])
            row.append("%s / %s" % (n, ten))
        print("%-8s %19s %19s %19s" % (t, row[0], row[1], row[2]))

    print()
    print("=" * 74)
    print("CONFOUND  path age in years at v6.12 (median)")
    print("=" * 74)
    from datetime import date
    end = date(2024, 11, 17)
    for cl in ("STAKE_SPECIFIC", "SHARED_CORE", "MIXED/UNCLEAR"):
        ages = []
        for p in S.PATHS:
            if S.CLASS_A[p] != cl:
                continue
            d = meas["first_commit"][p]
            ages.append((end - date(*map(int, d.split("-")))).days / 365.2425)
        print("  %-16s %6.1f y   (n=%d)" % (cl, statistics.median(ages),
                                            len(ages)))

    print()
    print("=" * 74)
    print("UNKNOWN / NOT_RUN share")
    print("=" * 74)
    cells = len(S.PATHS) * (len(TAGS) - 1)
    tcells = len(S.PATHS) * len(TAGS)
    m1n = sum(1 for k in m1 for p in m1[k] if m1[k][p] is None)
    ten = sum(1 for t in TAGS for p in S.PATHS
              if m3[t][p]["tenure_median"] is None)
    unres = sum(m3[t][p]["tenure_unresolved"] for t in TAGS for p in S.PATHS)
    m6n = sum(1 for i in range(1, len(TAGS))
              for p in S.PATHS
              if meas["intervals"]["%s..%s" % (TAGS[i-1], TAGS[i])][p]["top1"]
              is None)
    print("  M1 undefined (no lines)      %d / %d" % (m1n, cells))
    print("  M2 organizations             %d / %d   UNKNOWN (no employer map)"
          % (tcells, tcells))
    print("  M3 tenure unresolvable       %d / %d cells; %d maintainer-slots"
          % (ten, tcells, unres))
    print("  M4 review latency            %d / %d   NOT_RUN (lore unreachable)"
          % (cells, cells))
    print("  M5 volunteer share           %d / %d   NOT_RUN (no employer map)"
          % (tcells, tcells))
    print("  M6 no commits in interval    %d / %d" % (m6n, cells))
    print("  M6 organization-level        %d / %d   BLOCKED" % (cells, cells))
    print()
    print(LIMITS)


if __name__ == "__main__":
    main()
