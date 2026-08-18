#!/usr/bin/env python3
"""
DOMAIN LEDGER
Makes a confidence readout derived instead of asserted. Stdlib only.

A coverage number is not portable without its denominator. 61 percent over
one domain set is a different quantity than 61 percent over another. This
records the set.

COVERAGE IS NOT THE PRIMARY TERM. It resolves position inside a band that
anchor distance already set — see anchor.py. Reading further domains moves
the number within a band; it does not promote a shape between bands. Both
tools are needed to read a figure, and neither emits one alone.

Four readouts, deliberately not combined into one:

  coverage     domains where the shape held / domains read
  cycle depth  holds that survived a return / holds total
  adversarial  domains where the shape was pushed against / domains read
  truncated    reads cut short at a discomfort threshold / domains read

Coverage and cycle depth are different currencies. A shape can be wide and
shallow: sampled across many domains, never through a full turn. The tool
reports both and does not average them.

RESERVATION: a standing fraction held as unknown, applied to every shape.
It is not subtracted from coverage — coverage is over what was read. It caps
what the ledger will report as available headroom, and it is why a shape
with high coverage still does not coalesce.

The 0.2 default here encodes only the external-band ceiling of 0.8. The
30 floor for shapes with no external support, and the 99 band requiring
generational cycle survival, live in anchor.py where the source class is
recorded. Do not read a ceiling off this file alone.

Usage:
  ledger.py                    table over shapes/
  ledger.py --shape NAME       detail
  ledger.py --gaps NAME        unread and unpushed domains only
  ledger.py --new NAME         blank skeleton
  ledger.py --jsonl
  ledger.py --selftest
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SHAPEDIR = os.path.join(HERE, "shapes")

HOLD = "hold"
BREAK = "break"
MIXED = "mixed"
NOT_READ = "not_read"
READS = (HOLD, BREAK, MIXED, NOT_READ)

SINGLE = "single_look"
MULTIPLE = "multiple_looks"
CYCLE = "cycle_return"
DEPTHS = (SINGLE, MULTIPLE, CYCLE, None)

# how the reading was taken. live channels truncate at the point the other
# party's frame stops tolerating inspection; text channels do not truncate
# but cannot be asked a follow-up question.
CHANNELS = ("text", "live", "direct", "mixed", None)


def load(path=SHAPEDIR):
    out = []
    if not os.path.isdir(path):
        return out
    for f in sorted(os.listdir(path)):
        if f.endswith(".json"):
            with open(os.path.join(path, f), encoding="utf-8") as fh:
                out.append(json.load(fh))
    return out


def ratio(n, d):
    return None if not d else round(n / d, 3)


def score(shape):
    doms = shape.get("domains", [])
    read = [d for d in doms if d.get("read") not in (NOT_READ, None)]
    unread = [d for d in doms if d.get("read") in (NOT_READ, None)]
    holds = [d for d in read if d.get("read") == HOLD]
    breaks = [d for d in read if d.get("read") == BREAK]
    mixed = [d for d in read if d.get("read") == MIXED]
    cycled = [d for d in holds if d.get("depth") == CYCLE]
    pushed = [d for d in read if d.get("adversarial_run") is True]
    trunc = [d for d in read if d.get("truncated") is True]

    res = shape.get("reservation")
    cov = ratio(len(holds), len(read))
    asserted = shape.get("asserted_coverage")
    mismatch = None
    if cov is not None and asserted is not None:
        mismatch = round(abs(cov - asserted), 3)

    return {
        "shape": shape.get("shape"),
        "statement": shape.get("statement"),
        "domains_total": len(doms),
        "read": len(read),
        "unread": len(unread),
        "holds": len(holds),
        "breaks": len(breaks),
        "mixed": len(mixed),
        "coverage": cov,
        "asserted_coverage": asserted,
        "coverage_mismatch": mismatch,
        "cycle_depth": ratio(len(cycled), len(holds)),
        "cycles_observed": len(cycled),
        "adversarial": ratio(len(pushed), len(read)),
        "truncated": ratio(len(trunc), len(read)),
        "reservation": res,
        "ceiling": None if res is None else round(1 - res, 3),
        "break_domains": [d.get("domain") for d in breaks],
        "mixed_domains": [d.get("domain") for d in mixed],
        "unread_domains": [d.get("domain") for d in unread],
        "unpushed_domains": [d.get("domain") for d in read
                             if d.get("adversarial_run") is not True],
    }


def fmt(x):
    if x is None:
        return "--"
    if isinstance(x, float):
        return "%.2f" % x
    return str(x)


def table(scores):
    hdr = (f"{'shape':<26}{'read':>6}{'cov':>7}{'cyc':>7}"
           f"{'adv':>7}{'trunc':>7}{'unread':>8}")
    print(hdr)
    print("-" * len(hdr))
    for s in scores:
        print(f"{s['shape'][:26]:<26}{s['read']:>6}{fmt(s['coverage']):>7}"
              f"{fmt(s['cycle_depth']):>7}{fmt(s['adversarial']):>7}"
              f"{fmt(s['truncated']):>7}{s['unread']:>8}")
    print()
    print("cov    held / read. not a credence. not portable without the list.")
    print("cyc    holds that survived a return / holds. a separate currency.")
    print("adv    read domains where the shape was pushed against.")
    print("trunc  reads cut short at a discomfort threshold.")
    print()
    print("Unpushed domains are not neutral. Each is an untested surface.")


def wrap(t, w, ind=""):
    words, lines, cur = str(t).split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > w:
            lines.append(ind + cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(ind + cur)
    return lines


def detail(s, shape=None):
    print("SHAPE     %s" % s["shape"])
    for i, line in enumerate(wrap(s["statement"], 58)):
        print("%-10s%s" % ("STATEMENT" if i == 0 else "", line))
    print()
    print("DOMAINS   total=%s read=%s unread=%s"
          % (s["domains_total"], s["read"], s["unread"]))
    print("READS     hold=%s break=%s mixed=%s"
          % (s["holds"], s["breaks"], s["mixed"]))
    print()
    print("COVERAGE      %s   (held / read)" % fmt(s["coverage"]))
    if s["asserted_coverage"] is not None:
        print("  asserted    %s" % fmt(s["asserted_coverage"]))
        if s["coverage_mismatch"] is None:
            print("  derived     -- ledger not yet populated")
        else:
            print("  difference  %s" % fmt(s["coverage_mismatch"]))
    print("CYCLE DEPTH   %s   (%s holds survived a return)"
          % (fmt(s["cycle_depth"]), s["cycles_observed"]))
    print("ADVERSARIAL   %s" % fmt(s["adversarial"]))
    print("TRUNCATED     %s" % fmt(s["truncated"]))
    print("RESERVATION   %s   ceiling %s"
          % (fmt(s["reservation"]), fmt(s["ceiling"])))
    print()
    if s["break_domains"]:
        print("BROKE IN  %s" % ", ".join(str(x) for x in s["break_domains"]))
    if s["mixed_domains"]:
        print("MIXED IN  %s" % ", ".join(str(x) for x in s["mixed_domains"]))
    if s["unread_domains"]:
        print("UNREAD")
        for line in wrap(", ".join(str(x) for x in s["unread_domains"]),
                         58, "    "):
            print(line)
    if s["unpushed_domains"]:
        print("READ BUT NOT PUSHED")
        for line in wrap(", ".join(str(x) for x in s["unpushed_domains"]),
                         58, "    "):
            print(line)
    if shape:
        crit = shape.get("criterion_fixed_in_advance")
        if crit:
            print()
            print("CRITERION FIXED IN ADVANCE")
            for line in wrap(crit, 58, "    "):
                print(line)
        for o in shape.get("open", []):
            print()
            print("OPEN")
            for line in wrap(o, 58, "    "):
                print(line)


def gaps(s):
    print("SHAPE  %s" % s["shape"])
    print()
    print("UNREAD (%s)" % len(s["unread_domains"]))
    for d in s["unread_domains"]:
        print("  %s" % d)
    print()
    print("READ, NOT PUSHED (%s)" % len(s["unpushed_domains"]))
    for d in s["unpushed_domains"]:
        print("  %s" % d)


SKELETON = {
    "shape": "",
    "statement": "",
    "source": "",
    "reservation": 0.2,
    "asserted_coverage": None,
    "domains": [
        {"domain": "", "read": NOT_READ, "depth": None,
         "cycles_observed": None, "channel": None,
         "adversarial_run": False, "truncated": False, "note": ""}
    ]
}


def selftest():
    s = score({
        "shape": "t", "statement": "s", "reservation": 0.2,
        "asserted_coverage": 0.5,
        "domains": [
            {"domain": "a", "read": HOLD, "depth": CYCLE,
             "adversarial_run": True, "truncated": False},
            {"domain": "b", "read": HOLD, "depth": SINGLE,
             "adversarial_run": False, "truncated": True},
            {"domain": "c", "read": BREAK, "depth": SINGLE,
             "adversarial_run": True},
            {"domain": "d", "read": MIXED},
            {"domain": "e", "read": NOT_READ},
        ]})
    empty = score({"shape": "e", "domains": [
        {"domain": "x", "read": NOT_READ}]})
    checks = [
        ("read excludes not_read", s["read"] == 4),
        ("coverage is held over read", s["coverage"] == 0.5),
        ("mixed is not a hold", s["holds"] == 2),
        ("cycle depth over holds not read", s["cycle_depth"] == 0.5),
        ("adversarial over read", s["adversarial"] == 0.5),
        ("truncated counted", s["truncated"] == 0.25),
        ("ceiling from reservation", s["ceiling"] == 0.8),
        ("mismatch computed", s["coverage_mismatch"] == 0.0),
        ("break domains listed", s["break_domains"] == ["c"]),
        ("unpushed excludes unread", "e" not in s["unpushed_domains"]),
        ("unpushed lists b and d", sorted(s["unpushed_domains"]) == ["b", "d"]),
        ("empty ledger gives none not zero", empty["coverage"] is None),
        ("empty mismatch is none", empty["coverage_mismatch"] is None),
    ]
    ok = 0
    for n, r in checks:
        print(("PASS" if r else "FAIL"), n)
        ok += bool(r)
    print("\n%d/%d" % (ok, len(checks)))
    return 0 if ok == len(checks) else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if "--new" in a:
        i = a.index("--new")
        sk = json.loads(json.dumps(SKELETON))
        sk["shape"] = a[i + 1] if len(a) > i + 1 else "unnamed"
        print(json.dumps(sk, indent=2))
        return
    raw = load()
    scores = [score(x) for x in raw]
    if "--jsonl" in a:
        for s in scores:
            print(json.dumps(s))
        return
    for flag, fn in (("--shape", detail), ("--gaps", gaps)):
        if flag in a:
            i = a.index(flag)
            want = a[i + 1] if len(a) > i + 1 else None
            for s, r in zip(scores, raw):
                if s["shape"] == want:
                    if fn is detail:
                        fn(s, r)
                    else:
                        fn(s)
                    return
            print("no shape named %s" % want, file=sys.stderr)
            sys.exit(1)
    table(scores)


if __name__ == "__main__":
    main()
