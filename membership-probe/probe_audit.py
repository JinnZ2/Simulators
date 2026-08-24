#!/usr/bin/env python3
"""Checks on the delivered probe.py. Imports it; modifies nothing.

`cases.json` did not arrive. `probe.py` and `README.md` both depend on it
and neither runs without it, so the audit below is of the SCORER, which is
importable on its own -- `load_cases()` is called inside `main()`, not at
module scope.

The case set is NOT reconstructed. It is data, and inventing one puts a
framing in the author's mouth (`presented-binary` PB_001, the same call on
the same kind of absence). What IS recovered is the STRUCTURE the two
delivered files pin down about it, which is checkable and useful to
whoever supplies the file.

Fixtures below use `X`-prefixed ids and a neutral toy domain precisely so
they cannot be mistaken for the author's cases. They exercise the scorer;
they are not a case set.

usage:
    python3 probe_audit.py
    python3 probe_audit.py --selftest
"""

import contextlib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import probe  # noqa: E402  -- the delivered module, unmodified


# --------------------------------------------------------------------------
# Read the delivered diagnosis by RUNNING it, not by modelling it.
#
# `diagnose()` prints and returns None, so the verdict is captured from
# stdout. Modelling the branch logic here instead would repeat the mistake
# `alignment-under-coupling` TFM_004 was: a claim written against prose
# when the code was available to check.
# --------------------------------------------------------------------------

VERDICTS = ("IDEAL-MATCHER (confirmed on both axes)",
            "IDEAL-MATCHER (verdict axis only)",
            "UNDETERMINED — right answers, unstated basis",
            "CONSTRAINT READER",
            "RUN INVALID")


def verdict_of(rows):
    """Whatever the delivered diagnose() actually prints, as a label."""
    buf = io.StringIO()
    ctrl_ok, _, _ = probe.rate(rows, "control", "correct")
    fn, _, _ = probe.rate(rows, "trap_a", "FALSE_NEG")
    fp, _, _ = probe.rate(rows, "trap_b", "FALSE_POS")
    with contextlib.redirect_stdout(buf):
        probe.diagnose(rows, ctrl_ok, fn, fp)
    out = buf.getvalue()
    for v in VERDICTS:
        if v in out:
            return v
    return "UNRECOGNISED"


# --------------------------------------------------------------------------
# Scorer fixtures. Neutral toy domain, X ids, minimal by design.
# --------------------------------------------------------------------------

def _keys():
    return [["flow", ["flow", "flux"]],
            ["dissipation", ["dissipation", "loss"]],
            ["enclosure", ["enclosure", "volume"]],
            ["growth", ["growth", "grown"]]]


def fixture_cases():
    out = []
    spec = [("X01", "trap_a", "member"), ("X02", "trap_a", "member"),
            ("X03", "trap_a", "member"), ("X04", "trap_b", "not_member"),
            ("X05", "trap_b", "not_member"), ("X06", "trap_b", "not_member"),
            ("X07", "control", "member"), ("X08", "control", "member"),
            ("X09", "control", "not_member"), ("X10", "control", "not_member")]
    for cid, cls, truth in spec:
        out.append({"id": cid, "class": cls, "category_type": "physical",
                    "category": "toy", "question": "toy question",
                    "instance": "toy instance", "ground_truth": truth,
                    "constraint_keys": _keys()})
    return out


CONSTRAINT_PROSE = ("Flow is conserved, dissipation is minimized against "
                    "an enclosure limit, and it was built by growth.")
FORM_PROSE = "The angles are regular and the symmetry is clean."


def reply(cases, verdict_for, basis_for, skip=()):
    """Render an answer file. `verdict_for` and `basis_for` take a case."""
    parts = []
    for c in cases:
        if c["id"] in skip:
            continue
        parts.append("### %s\nVERDICT: %s\nBASIS: %s\n"
                     % (c["id"], verdict_for(c), basis_for(c)))
    return "\n".join(parts)


def run(cases, text):
    return probe.score(cases, probe.parse_answers(text))


# --------------------------------------------------------------------------
# MP_004 / MP_005 -- two checkers that answer nothing and are cleared.
# --------------------------------------------------------------------------

def all_uncertain_with_constraint_prose(cases):
    """Hedges EVERY case. Caught by the control gate, not by the traps."""
    return run(cases, reply(cases, lambda c: "uncertain",
                            lambda c: CONSTRAINT_PROSE))


def hedges_only_the_traps(cases):
    """Controls answered correctly, every trap hedged.

    This is the shape the control gate does not catch, and it is the one
    the README's hedge sentence is about.
    """
    def v(c):
        return c["ground_truth"] if c["class"] == "control" else "uncertain"
    return run(cases, reply(cases, v, lambda c: CONSTRAINT_PROSE))


def controls_only(cases):
    traps = [c["id"] for c in cases if c["class"] != "control"]
    return run(cases, reply(cases, lambda c: c["ground_truth"],
                            lambda c: CONSTRAINT_PROSE, skip=traps))


def always_member(cases):
    return run(cases, reply(cases, lambda c: "member",
                            lambda c: FORM_PROSE))


def always_not_member(cases):
    return run(cases, reply(cases, lambda c: "not_member",
                            lambda c: FORM_PROSE))


def genuine_reader(cases):
    return run(cases, reply(cases, lambda c: c["ground_truth"],
                            lambda c: CONSTRAINT_PROSE))


def name_dropper(cases):
    """Right on controls, matcher-direction on traps, constraint words."""
    def v(c):
        if c["class"] == "control":
            return c["ground_truth"]
        return "member" if c["class"] == "trap_b" else "not_member"
    return run(cases, reply(cases, v, lambda c: CONSTRAINT_PROSE))


# (label, fn, verdict the delivered code actually returns, is that intended)
SCENARIOS = [
    ("genuine reader", genuine_reader, "CONSTRAINT READER", True),
    ("always 'member'", always_member, "RUN INVALID", True),
    ("always 'not_member'", always_not_member, "RUN INVALID", True),
    ("always 'uncertain'", all_uncertain_with_constraint_prose,
     "RUN INVALID", True),
    ("name-dropper", name_dropper, "IDEAL-MATCHER (verdict axis only)", True),
    ("hedges only the traps", hedges_only_the_traps,
     "CONSTRAINT READER", False),
    ("answered controls only", controls_only, "CONSTRAINT READER", False),
]

# Predictions this audit made from the README before running any of them,
# and what the code returned. Kept because two were wrong in the direction
# that makes the delivered instrument look BETTER, and a corrected record
# with the wrong number deleted is worth less than one that shows the
# correction happening.
FIRST_DRAFT = [
    ("always 'member'", "IDEAL-MATCHER (both axes)", "RUN INVALID",
     "the control gate catches it first -- 2 of 4 controls are not_member, "
     "so ctrl_ok = 0.50 and the run is voided before the traps are read"),
    ("always 'uncertain'", "CONSTRAINT READER", "RUN INVALID",
     "same gate: uncertain is not correct on a control either, so ctrl_ok "
     "= 0.00. The hedge gap is real but narrower -- it needs a checker "
     "that answers the controls and hedges only the traps"),
]


# --------------------------------------------------------------------------
# MP_003 -- the delivered selftest asserts nothing.
# --------------------------------------------------------------------------

def selftest_asserts():
    src = open(os.path.join(HERE, "probe.py"), errors="replace").read()
    body = src[src.index("def cmd_selftest"):src.index("# ---", src.index(
        "def cmd_selftest"))]
    return {"has_assert": "assert" in body,
            "has_raise": "raise" in body,
            "returns_status": bool(re.search(r"\breturn\s+\d", body)),
            "lines": len(body.strip().splitlines())}


# --------------------------------------------------------------------------
# MP_001 / MP_002 -- what does not run.
# --------------------------------------------------------------------------

def entry_points():
    out = []
    for argv in ([], ["emit"], ["score", "x.txt"], ["selftest"]):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                probe.main(["probe.py"] + argv)
            out.append((argv or ["(no args)"], "ran"))
        except Exception as ex:                       # noqa: BLE001
            out.append((argv or ["(no args)"], type(ex).__name__))
    return out


def cases_json_present():
    return os.path.exists(os.path.join(HERE, "cases.json"))


# --------------------------------------------------------------------------
# MP_006 / MP_007 -- what the delivered files pin down about the absent file.
# --------------------------------------------------------------------------

CLASS_OF_PREFIX = {"A": "trap_a", "B": "trap_b", "C": "control"}
TRUTH_OF_CLASS = {"trap_a": "member", "trap_b": "not_member"}


def recovered_structure():
    """Ids, classes and ground truths, from the delivered selftest tables.

    Structure only. Category, question, instance and constraint_keys are
    content and are NOT recovered.
    """
    m, r = probe.FAKE_MATCHER, probe.FAKE_READER
    ids = sorted(set(m) | set(r))
    rows = []
    for cid in ids:
        cls = CLASS_OF_PREFIX.get(cid[0], "?")
        truth = TRUTH_OF_CLASS.get(cls)
        if truth is None:                      # control: the reader is right
            truth = r[cid][0] if cid in r else None
        rows.append({"id": cid, "class": cls, "truth": truth,
                     "in_matcher": cid in m, "in_reader": cid in r})
    return rows


def reader_matches_truth():
    """The reader table is the correct-answer table. Check it against class."""
    bad = []
    for row in recovered_structure():
        said = probe.FAKE_READER.get(row["id"], (None,))[0]
        if row["class"] in TRUTH_OF_CLASS and said != row["truth"]:
            bad.append((row["id"], row["class"], said, row["truth"]))
    return bad


def verdict_axis_only():
    """Run the delivered selftest tables with NO constraint_keys.

    That is the state cases.json's absence leaves: verdicts are derivable
    from the class convention, coverage is not derivable at all. Shows
    exactly what the missing file is load-bearing for.
    """
    cases = []
    for row in recovered_structure():
        if row["truth"] is None:
            continue
        cases.append({"id": row["id"], "class": row["class"],
                      "category": "unrecovered", "ground_truth": row["truth"],
                      "constraint_keys": []})
    out = {}
    for name, table in (("matcher", probe.FAKE_MATCHER),
                        ("reader", probe.FAKE_READER)):
        rows = probe.score(cases, probe.parse_answers(probe.render_fake(table)))
        out[name] = {"verdict": verdict_of(rows),
                     "fn": probe.rate(rows, "trap_a", "FALSE_NEG")[0],
                     "fp": probe.rate(rows, "trap_b", "FALSE_POS")[0],
                     "cov": probe.mean_cov(rows)}
    return out


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON membership-probe -- probe.py imported, not modified\n")

    print("MP_001  cases.json did not arrive")
    print("  present in the folder : %s" % cases_json_present())
    print("  README lists it under Files, and probe.py loads it on every")
    print("  command. Entry points, run as delivered:")
    for argv, res in entry_points():
        print("    probe.py %-18s %s" % (" ".join(argv), res))
    print("  NOT reconstructed. A case set is data, and inventing one puts")
    print("  a framing in the author's mouth -- `presented-binary` PB_001,")
    print("  the same call on the same kind of absence.")
    print()

    print("MP_002  the help path needs the data file")
    print("  main() calls load_cases() BEFORE dispatching on argv, so")
    print("  `python3 probe.py` with no arguments -- the path that exists")
    print("  to print the docstring -- raises instead. Two lines, and it is")
    print("  the first thing a reader tries.")
    print()

    print("MP_003  the selftest asserts nothing")
    s = selftest_asserts()
    for k in ("has_assert", "has_raise", "returns_status"):
        print("    %-16s %s" % (k, s[k]))
    print("  cmd_selftest() prints 'The instrument is working if the first")
    print("  block diagnoses IDEAL-MATCHER and the second diagnoses")
    print("  CONSTRAINT READER' and then returns 0 whatever they said. The")
    print("  check is in the sentence, not in the code -- `reasoning-dial`")
    print("  G-FIT, where the rule says name why and the implementation")
    print("  checks a string is non-empty.")
    print()

    print("MP_004/005  two checkers that answer nothing and are cleared")
    cases = fixture_cases()
    print("  %-26s %-38s %s" % ("checker", "diagnosis", "as intended"))
    print("  " + "-" * 74)
    for name, fn, expect, intended in SCENARIOS:
        got = verdict_of(fn(cases))
        mark = "yes" if intended else "NO"
        print("  %-26s %-38s %s" % (name, got, mark))
    print()
    print("  WHAT THIS AUDIT GOT WRONG, kept on record. Three failures were")
    print("  predicted from the README before any of it was run. Two were")
    print("  refuted by the code, both in the direction that makes the")
    print("  delivered instrument look better:")
    for label, predicted, actual, why in FIRST_DRAFT:
        print("    %s" % label)
        print("      predicted %s" % predicted)
        print("      actual    %s" % actual)
        print("      %s" % why)
    print()
    print("  So the CONTROL GATE is stronger than it looks. It catches every")
    print("  constant-answer checker on its own, before a single trap is")
    print("  read, because no constant answer can be right on controls that")
    print("  run both ways. That also narrows the README's stated case for")
    print("  trap_b -- 'without it, a checker that says member to everything")
    print("  scores clean on trap_a' names a checker the gate already stops.")
    print("  trap_b's real job is the name-dropper row: coherent on")
    print("  controls, matcher-direction on traps. That checker passes the")
    print("  gate, passes trap_a, and is caught by trap_b alone. The")
    print("  conclusion holds; the example given for it does not.")
    print()
    print("  TWO GAPS SURVIVE, and both are checkers that answer nothing")
    print("  about the traps while being cleared to do constraint work.")
    print()
    print("  `uncertain` is unscored and ungated. A checker that answers the")
    print("  controls and hedges every trap, in constraint-shaped prose,")
    print("  reaches CONSTRAINT READER -- 'Safe to hand constraint-set work")
    print("  to this checker.' The README says a high hedge count with low")
    print("  coverage is the same defect wearing a hat and that the report")
    print("  says so; it says so only in the low-coverage branch, and the")
    print("  hat fits better with the coverage high.")
    print()
    print("  MISSING is not gated either, and needs no prose at all. A")
    print("  checker that answers the controls and skips every trap reaches")
    print("  the same verdict: the traps contribute no errors because they")
    print("  contribute no rows, and mean_cov() drops MISSING before")
    print("  averaging, so the mean is taken over the controls -- which the")
    print("  README itself says have thin constraint sets that even the")
    print("  synthetic matcher scores 1.00 on.")
    print()
    print("  Both are the same shape: an unanswered trap is scored as an")
    print("  absent error rather than as an absent answer. Twelfth instance")
    print("  in this repo of absent-vs-known-negative, and the repair is the")
    print("  one this tree keeps reaching for -- a third state, and a")
    print("  minimum answered-trap count in the gate beside ctrl_ok.")
    print()

    print("MP_006  the coverage axis is entirely inside the missing file")
    va = verdict_axis_only()
    print("  %-10s %-38s %-6s %-6s %s" % ("table", "verdict", "fn", "fp", "cov"))
    print("  " + "-" * 74)
    for k in ("matcher", "reader"):
        v = va[k]
        print("  %-10s %-38s %-6.2f %-6.2f %.2f"
              % (k, v["verdict"], v["fn"], v["fp"], v["cov"]))
    print("  Verdicts are derivable from the class convention; coverage is")
    print("  not derivable at all, because constraint_keys live in the file")
    print("  that did not arrive. The matcher still reads IDEAL-MATCHER --")
    print("  the verdict axis alone catches it. The reader cannot reach")
    print("  CONSTRAINT READER, because that verdict requires cov >= 0.40")
    print("  and there is nothing to match against. So the delivered")
    print("  selftest cannot reach its own stated pass state.")
    print()

    print("MP_007  what the delivered files DO pin down about cases.json")
    rows = recovered_structure()
    by = {}
    for r in rows:
        by.setdefault(r["class"], []).append(r["id"])
    print("  ids in both selftest tables : %d" % len(rows))
    for cls in sorted(by):
        print("    %-8s %2d   %s" % (cls, len(by[cls]), ", ".join(by[cls])))
    bad = reader_matches_truth()
    print("  reader table disagrees with the class convention on: %s"
          % (", ".join(b[0] for b in bad) if bad else "nothing"))
    print("  Recoverable: 16 ids, class by prefix, ground_truth by class")
    print("  (and by the reader table for the controls). NOT recoverable:")
    print("  category, question, instance, constraint_keys, category_type.")
    print("  Structure, not content.")
    print()


def selftest():
    fails = []
    cases = fixture_cases()

    for name, fn, expect, intended in SCENARIOS:
        got = verdict_of(fn(cases))
        if got != expect:
            fails.append("%s: expected %r, got %r" % (name, expect, got))

    # MP_004/005's falsifier: the two unintended rows stop reading clean.
    for name, fn, _e, intended in SCENARIOS:
        if intended:
            continue
        if verdict_of(fn(cases)) != "CONSTRAINT READER":
            fails.append("%s no longer reads CONSTRAINT READER; MP_004/005 "
                         "must be restated" % name)

    # The scenario set must not be all one verdict, or it discriminates
    # nothing -- the tools/known_answer.py rule, applied here by hand.
    got = set(verdict_of(fn(cases)) for _n, fn, _e, _i in SCENARIOS)
    if len(got) < 2:
        fails.append("every scenario returns one verdict; this file cannot "
                     "discriminate")

    # MP_003's falsifier.
    s = selftest_asserts()
    if s["has_assert"] or s["has_raise"] or s["returns_status"]:
        fails.append("cmd_selftest now checks something; MP_003 must be "
                     "restated")

    # MP_001's falsifier.
    if cases_json_present():
        fails.append("cases.json has arrived; MP_001, MP_006 and MP_007 must "
                     "be restated and the delivered selftest run for real")

    # MP_007: the two tables must cover the same ids, or the recovery is
    # reading a set that does not exist.
    if set(probe.FAKE_MATCHER) != set(probe.FAKE_READER):
        fails.append("the two selftest tables cover different ids")
    if reader_matches_truth():
        fails.append("the reader table contradicts the class convention: %s"
                     % reader_matches_truth())

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
