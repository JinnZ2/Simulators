#!/usr/bin/env python3
"""
EXTRACT
Reader and filter over cases.json and sources.json. Stdlib only. CC0.

It does one thing beyond reading: it scores each case twice, on the criterion
and on all five cuts, and reports where the two disagree. The criterion names
two cuts; the CUTS block names five. Either the criterion is incomplete or
three cuts are diagnostics rather than criteria, and which of those is true is
decided by whether a disagreeing case exists. That is a measurement, so it is
computed rather than argued.
"""

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name):
    with open(os.path.join(HERE, name), "r") as handle:
        return json.load(handle)


def _favourable(schema):
    return schema["_schema"]["favourable"]


def criterion_verdict(case, schema):
    """BUFFER iff self-custodied AND locally verifiable. The one-line rule."""

    fav = _favourable(schema)
    cuts = schema["_schema"]["criterion_cuts"]
    return "BUFFER" if all(case[c] == fav[c] for c in cuts) else "BELT"


def cut_profile(case, schema):
    """(favourable count, total, list of unfavourable cut names)."""

    fav = _favourable(schema)
    names = sorted(fav)
    unfav = [c for c in names if case[c] != fav[c]]
    return len(names) - len(unfav), len(names), unfav


def disagreements(schema):
    """Cases where the criterion and the full five-cut reading part company.

    Two directions, and they are different defects:

      PASSES_CRITERION_FAILS_CUTS   the rule calls it a buffer while cuts it
                                    does not read are unfavourable. The rule
                                    is incomplete.
      FAILS_CRITERION_PASSES_CUTS   the rule calls it a belt while most cuts
                                    are favourable. The rule over-rejects.
    """

    out = []
    for case in schema["cases"]:
        verdict = criterion_verdict(case, schema)
        good, total, unfav = cut_profile(case, schema)
        unread = [c for c in unfav if c not in schema["_schema"]["criterion_cuts"]]
        if verdict == "BUFFER" and unread:
            out.append((case["id"], "PASSES_CRITERION_FAILS_CUTS", good, total, unread))
        elif verdict == "BELT" and good >= total - 1:
            out.append((case["id"], "FAILS_CRITERION_PASSES_CUTS", good, total, unfav))
    return out


def report(stream=sys.stdout):
    schema = load("cases.json")
    sources = load("sources.json")
    w = stream.write

    w("CUSTODY VERIFICATION BAND\n")
    w("criterion reads %s; CUTS names %d\n\n"
      % (", ".join(schema["_schema"]["criterion_cuts"]),
         len(_favourable(schema))))

    w("  %-24s %-8s %-6s %-5s %s\n"
      % ("case", "verdict", "cuts", "conf", "unfavourable"))
    for case in schema["cases"]:
        good, total, unfav = cut_profile(case, schema)
        w("  %-24s %-8s %d/%-4d %-5.2f %s\n"
          % (case["id"], criterion_verdict(case, schema), good, total,
             case["confidence"], ",".join(unfav) or "-"))

    w("\nDISAGREEMENTS -- criterion against the full cut set\n")
    found = disagreements(schema)
    if not found:
        w("  none\n")
    for cid, kind, good, total, cuts in found:
        w("  %-24s %-30s %d/%d  %s\n" % (cid, kind, good, total, ",".join(cuts)))
    w("\n  A disagreement in either direction says the one-line criterion and\n")
    w("  the five-cut reading are not the same instrument. Both are kept and\n")
    w("  reported separately rather than one being folded into the other.\n")

    w("\nCORPUS\n")
    for s in sources["sources"]:
        w("  %-28s read=%-5s arithmetic_checked=%s\n"
          % (s["id"], s["read"], s["arithmetic_checked"]))
    unread = [s["id"] for s in sources["sources"] if not s["read"]]
    w("  %d of %d unread. No case in cases.json is CITED.\n"
      % (len(unread), len(sources["sources"])))

    seeds = [c for c in schema["cases"] if c["status"] == "SEED"]
    w("\n  %d of %d cases are SEED: structural placeholders written to exercise\n"
      % (len(seeds), len(schema["cases"])))
    w("  the criterion, not observations. None is evidence.\n")


def filter_cases(cut, value, stream=sys.stdout):
    schema = load("cases.json")
    if cut not in _favourable(schema):
        raise ValueError("unknown cut: %s" % cut)
    for case in schema["cases"]:
        if case[cut] == value:
            stream.write("%s\n" % case["id"])


def selftest(stream=sys.stdout):
    schema = load("cases.json")
    sources = load("sources.json")
    checks = []

    def check(name, cond):
        checks.append((name, bool(cond)))

    fav = _favourable(schema)
    check("five cuts declared", len(fav) == 5)
    check("criterion reads two of them",
          len(schema["_schema"]["criterion_cuts"]) == 2)
    check("every case declares every cut",
          all(all(c in case for c in fav) for case in schema["cases"]))
    check("every cut value is in its vocabulary",
          all(case[c] in schema["_schema"]["cuts"][c]
              for case in schema["cases"] for c in fav))
    check("every case carries a confidence",
          all(0.0 <= case["confidence"] <= 1.0 for case in schema["cases"]))
    check("every case names what would measure it",
          all(case["measured_by"] for case in schema["cases"]))
    check("no case is cited yet",
          all(case["status"] == "SEED" for case in schema["cases"]))

    by_id = dict((c["id"], c) for c in schema["cases"])
    check("self-custodied and locally verifiable reads BUFFER",
          criterion_verdict(by_id["owner_operator_trucking"], schema) == "BUFFER")
    check("opaque verification reads BELT despite self custody",
          criterion_verdict(by_id["index_fund_holder"], schema) == "BELT")
    check("external custody reads BELT",
          criterion_verdict(by_id["franchise_operator"], schema) == "BELT")

    kinds = dict((cid, kind) for cid, kind, _, _, _ in disagreements(schema))
    check("the criterion is shown incomplete by a case",
          kinds.get("owner_operator_trucking") == "PASSES_CRITERION_FAILS_CUTS")
    check("the criterion is shown to over-reject by a case",
          kinds.get("cooperative_member") == "FAILS_CRITERION_PASSES_CUTS")
    check("agreeing cases raise no disagreement",
          "platform_gig_driver" not in kinds)

    check("every source carries a citation",
          all(len(s["cite"]) > 30 for s in sources["sources"]))
    check("no source is marked read",
          all(not s["read"] for s in sources["sources"]))
    check("the WBE arithmetic is marked checked",
          any(s["id"] == "west-brown-enquist-1997" and s["arithmetic_checked"]
              for s in sources["sources"]))
    check("unknown cut is rejected",
          _raises(filter_cases, "nonsense", "SELF"))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        stream.write("  %s  %s\n" % ("ok  " if ok else "FAIL", name))
    stream.write("\nselftest %d/%d\n" % (passed, len(checks)))
    return passed == len(checks)


def _raises(fn, *a):
    try:
        fn(*a, stream=open(os.devnull, "w"))
    except ValueError:
        return True
    except TypeError:
        try:
            fn(*a)
        except ValueError:
            return True
    return False


def main(argv=None):
    p = argparse.ArgumentParser(description="custody-verification-band reader")
    p.add_argument("--cut", help="filter cases by cut, e.g. --cut custody")
    p.add_argument("--value", help="value to match with --cut")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)
    if a.selftest:
        return 0 if selftest() else 1
    if a.cut:
        if not a.value:
            p.error("--cut requires --value")
        filter_cases(a.cut, a.value)
        return 0
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main())
