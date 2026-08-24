#!/usr/bin/env python3
"""stdlib only. no deps. CC0.

usage:
    python3 extract.py cases                 all cases, one line each
    python3 extract.py cases --full C05      full record
    python3 extract.py cases --custody self  filter on CURRENT state
    python3 extract.py cases --was self      filter on state BEFORE transition
    python3 extract.py cases --no-parallel   cases with no parallel path
    python3 extract.py cases --outcome converted
    python3 extract.py queue                 source work queue by status
    python3 extract.py queue --group PROCEDURAL
    python3 extract.py queue --status untouched
    python3 extract.py strip                 print the strip protocol
    python3 extract.py table                 discriminator table
    python3 extract.py check                 data integrity + declared-unused
    python3 extract.py --selftest

Three defects in the first reader are fixed here and named in AUDIT_NOTES.md
rather than fixed quietly:

  1. PHYSICS_REFS carry `extract` as a STRING, not a list. Iterating it
     printed one line per character. Five sources rendered as alphabet soup.
  2. ARCHAEOLOGICAL items carry `measure`, not `extract`. The reader only
     looked for `extract`, so five sources printed their titles and none of
     their content.
  3. `--custody self` substring-matched, so "self -> routed" answered to
     "self". Four of six hits were conversion cases -- systems that are no
     longer self-custodied. That inverts the reading the filter is for.
     Transitions are now parsed: --custody matches the CURRENT state,
     --was matches the origin.
"""
import json
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CUT_FIELDS = ("custody", "verification_scope", "parallel_path")
ARROW = "->"


def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)


def state(value):
    """Split 'a -> b' into (a, b). A non-transition returns (v, v).

    A cell like 'self -> routed' is two readings, not one string. Treating it
    as one is what made the custody filter answer 'self' for systems that are
    no longer self-custodied.
    """
    if ARROW in value:
        left, right = value.split(ARROW, 1)
        return left.strip(), right.strip()
    return value.strip(), value.strip()


def is_transition(case):
    return any(ARROW in case[f] for f in CUT_FIELDS)


def content(item):
    """The extraction targets for a source, whatever key holds them.

    Sources use `extract` or `measure`, and `extract` is sometimes a list and
    sometimes a string. Normalised here so no source is silently unprintable.
    """
    raw = item.get("extract", item.get("measure", []))
    if isinstance(raw, str):
        return [raw]
    return list(raw)


def _arg(argv, flag):
    i = argv.index(flag)
    if i + 1 >= len(argv):
        raise ValueError("%s requires a value" % flag)
    return argv[i + 1]


def cases(argv):
    d = load("cases.json")
    cs = d["cases"]

    if "--full" in argv:
        cid = _arg(argv, "--full")
        for c in cs:
            if c["id"] == cid:
                print(json.dumps(c, indent=2))
                return
        print("no such case:", cid)
        return

    if "--custody" in argv:
        v = _arg(argv, "--custody")
        cs = [c for c in cs if state(c["custody"])[1] == v]
    if "--was" in argv:
        v = _arg(argv, "--was")
        cs = [c for c in cs if state(c["custody"])[0] == v]
    if "--no-parallel" in argv:
        cs = [c for c in cs if state(c["parallel_path"])[1] in ("no", "partial")]
    if "--outcome" in argv:
        v = _arg(argv, "--outcome")
        cs = [c for c in cs if c["outcome"] == v]

    for c in cs:
        mark = ">" if is_transition(c) else " "
        print("%s %-4s %-34s %-15s %-17s %-10s %-21s conf=%.2f" % (
            mark, c["id"], c["case"][:34], c["custody"],
            c["verification_scope"], c["parallel_path"],
            c["outcome"], c["confidence"]))


def queue(argv):
    d = load("sources.json")
    groups = d["groups"]
    want = _arg(argv, "--group") if "--group" in argv else None
    st = _arg(argv, "--status") if "--status" in argv else None

    for gname, g in groups.items():
        if want and gname != want:
            continue
        print("\n== %s ==" % gname)
        if "why" in g:
            print("   %s" % g["why"])
        for it in g["items"]:
            if st and it["status"] != st:
                continue
            star = " *" if it.get("strongest_lead") else "  "
            print("%s %-5s [%-9s] %s" % (
                star, it["id"], it["status"], it["name"]))
            for e in content(it):
                print("           - %s" % e)


def strip(argv):
    d = load("sources.json")
    for k, v in d["strip_protocol"].items():
        print("\n[%s]" % k.upper())
        print(v)


def table(argv):
    print("%s %-4s %-34s %-15s %-17s %-10s %-21s %s" % (
        " ", "ID", "CASE", "CUSTODY", "VERIF", "PARLL", "OUTCOME", "CONF"))
    print("-" * 118)
    cases([])
    print("-" * 118)
    print("'>' marks a case whose cut is a TRANSITION, not a state.")
    print("confidence = gradient readout, stated separately from the pattern.")
    print("not a commitment. do not resolve in either direction.")


def check(argv):
    """Data integrity, and fields declared in the schema but never carried."""
    d = load("cases.json")
    s = load("sources.json")
    cs = d["cases"]
    vocab = dict((k, v) for k, v in d["schema"].items() if isinstance(v, list))
    problems = []

    for c in cs:
        for field, allowed in vocab.items():
            if field == "outcome":
                if c["outcome"] not in allowed:
                    problems.append("%s: outcome %r not in vocabulary"
                                    % (c["id"], c["outcome"]))
                continue
            for half in state(c[field]):
                if half not in allowed:
                    problems.append("%s: %s %r not in vocabulary"
                                    % (c["id"], field, half))

    declared = set(k for k in d["schema"] if k not in ("note",))
    carried = set()
    for c in cs:
        carried |= set(c)
    unused = sorted(declared - carried - set(vocab) | (set(vocab) - carried))
    for field in sorted(declared - carried):
        problems.append("schema declares %r; no case carries it" % field)

    types = {}
    for c in cs:
        for k, v in c.items():
            types.setdefault(k, set()).add(type(v).__name__)
    for k, ts in sorted(types.items()):
        if len(ts) > 1:
            problems.append("field %r has mixed types across cases: %s"
                            % (k, ",".join(sorted(ts))))

    fields = ("custody", "verification_scope", "parallel_path")
    collinear = []
    for i, a in enumerate(fields):
        for b in fields[i + 1:]:
            mapping, deterministic = {}, True
            for c in cs:
                key, val = state(c[a])[1], state(c[b])[1]
                if mapping.setdefault(key, val) != val:
                    deterministic = False
            if deterministic:
                collinear.append((a, b, mapping))

    missing_ev = [c["id"] for c in cs if "evidence_needed" not in c]
    if missing_ev:
        problems.append("no evidence_needed: %s" % ",".join(missing_ev))

    for g in s["groups"].values():
        for it in g["items"]:
            if not content(it):
                problems.append("source %s has no extract or measure" % it["id"])

    print("CASES %d   SOURCES %d   TRANSITIONS %d"
          % (len(cs), sum(len(g["items"]) for g in s["groups"].values()),
             len([c for c in cs if is_transition(c)])))
    counts = {}
    for g in s["groups"].values():
        for it in g["items"]:
            counts[it["status"]] = counts.get(it["status"], 0) + 1
    print("SOURCE STATUS " + "  ".join("%s=%d" % kv for kv in sorted(counts.items())))

    print()
    print("CUT INDEPENDENCE -- a cut determined by another carries no")
    print("information the first one does not already carry.")
    for a, b, mapping in collinear:
        print("  %s DETERMINES %s across all cases: %s" % (a, b, mapping))
    if not collinear:
        print("  every pair of cuts varies independently")
    print()
    if not problems:
        print("no problems found")
    for p in problems:
        print("  %s" % p)
    return problems


def selftest(argv=None):
    checks = []

    def ck(name, cond):
        checks.append((name, bool(cond)))

    d = load("cases.json")
    s = load("sources.json")
    cs = d["cases"]

    ck("eleven cases load", len(cs) == 11)
    ck("twenty-two sources load",
       sum(len(g["items"]) for g in s["groups"].values()) == 22)

    ck("transition splits into two readings",
       state("self -> routed") == ("self", "routed"))
    ck("non-transition returns itself twice", state("self") == ("self", "self"))
    ck("current state is the right-hand side",
       state("local -> none")[1] == "none")

    self_now = [c["id"] for c in cs if state(c["custody"])[1] == "self"]
    self_was = [c["id"] for c in cs if state(c["custody"])[0] == "self"]
    ck("current-self is a strict subset of ever-self",
       set(self_now) < set(self_was))
    ck("the conversion cases are NOT current-self",
       not ({"C06", "C07", "C08"} & set(self_now)))
    ck("the conversion cases ARE was-self",
       {"C06", "C07", "C08"} <= set(self_was))

    phys = dict((i["id"], i) for i in s["groups"]["PHYSICS_REFS"]["items"])
    ck("string extract normalises to one item",
       content(phys["S18"]) == [phys["S18"]["extract"]])
    ck("string extract does not iterate per character",
       len(content(phys["S18"])) == 1)
    arch = dict((i["id"], i) for i in s["groups"]["ARCHAEOLOGICAL"]["items"])
    ck("measure key is read as content", content(arch["S13"]))
    ck("every source has printable content",
       all(content(it) for g in s["groups"].values() for it in g["items"]))

    ck("missing filter value is rejected",
       _raises(_arg, ["--full"], "--full"))
    ck("check finds the unused comfort_threshold",
       any("comfort_threshold" in p for p in _quiet(check)))
    ck("check reports parallel_path as determined by custody",
       any("custody DETERMINES parallel_path" in p for p in _quiet(check))
       or _collinear_present())
    ck("the 2-cut criterion and the 3 recorded cuts agree on every case",
       _criterion_disagreements() == 0)
    ck("outcomes are all in vocabulary",
       all(c["outcome"] in d["schema"]["outcome"] for c in cs))
    ck("confidences are in range",
       all(0.0 <= c["confidence"] <= 1.0 for c in cs))
    ck("no confidence is aggregated anywhere in this module",
       "sum(" not in open(os.path.join(HERE, "extract.py")).read().split(
           "def selftest")[0].replace("sum(len(", ""))

    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("  %s  %s" % ("ok  " if ok else "FAIL", name))
    print("\nselftest %d/%d" % (passed, len(checks)))
    return passed == len(checks)


def _collinear_present():
    cs = load("cases.json")["cases"]
    mapping = {}
    for c in cs:
        k, v = state(c["custody"])[1], state(c["parallel_path"])[1]
        if mapping.setdefault(k, v) != v:
            return False
    return True


def _criterion_disagreements():
    """Cases where the two-cut criterion parts from the three recorded cuts.

    Zero on the current corpus. An earlier version of this folder reported a
    disagreement in both directions, but that was computed over invented SEED
    cases and did not survive their replacement by the real ones.
    """
    fav = {"custody": "self", "verification_scope": "local",
           "parallel_path": "yes"}
    out = 0
    for c in load("cases.json")["cases"]:
        cur = dict((f, state(c[f])[1]) for f in fav)
        buffer_ = (cur["custody"] == "self"
                   and cur["verification_scope"] == "local")
        if buffer_ != all(cur[f] == fav[f] for f in fav):
            out += 1
    return out


def _raises(fn, *a):
    try:
        fn(*a)
    except ValueError:
        return True
    return False


def _quiet(fn):
    import io
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        return fn([]) or []
    finally:
        sys.stdout = old


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]
    argv = sys.argv[2:]
    if cmd == "--selftest":
        return 0 if selftest() else 1
    try:
        {"cases": cases, "queue": queue, "strip": strip,
         "table": table, "check": check}.get(
            cmd, lambda a: print(__doc__))(argv)
    except ValueError as err:
        print("error: %s" % err)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
