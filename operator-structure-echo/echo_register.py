#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
echo_register.py - one line per module, and the module refuses to fill it.

    python3 echo_register.py [--selftest]

Marker under exploration. Delivered spec: SPEC_ECHO.md.

THE OBSERVATION. Instruments built in this ecosystem recur to the same
structural shape the operator uses to process the domain by hand. Not a defect
claim, not a discipline failure. It is a property of a single-builder
instrument and cannot be removed by effort -- only counted.

THE INSTRUCTION IS "DO NOT CORRECT. LOG." So this module logs and does not
correct, and the one line it keeps per module is:

    does this shape match a procedure the operator already runs unaided?
    YES / NO / UNEXAMINED, default UNEXAMINED.

ONLY THE OPERATOR CAN FILL IT, AND THAT IS ENFORCED RATHER THAN STATED.
mark() refuses a YES or a NO without operator attribution. The downstream
model cannot answer "does this match a procedure you already run unaided"
about someone else, and a register it could fill itself would be a register
of its guesses.

UNEXAMINED IS NOT NO. This is the load-bearing line in the whole module. The
default is UNEXAMINED for every module in the repo, and the consequence the
spec names -- that agreement between two modules may be inherited rather than
found -- runs on the register's contents. Read UNEXAMINED as NO and every
module comes back independent, the shared generator disappears, and the
readout inverts while looking unchanged. So UNEXAMINED is a third state
throughout, never folded into either answer.

TWO KINDS, BECAUSE THE DELIVERED LIST HOLDS TWO. The spec names three
instances and then separates them: the first two are "the instrument missing
a case", the third is "the instrument REPRODUCING the operator's own
processing structure in a domain the operator did not intend to model", and
the third is what raises this from a per-repo note to a subject. Those are
different observations and they are logged apart. The count of three is a
count of two kinds.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

VERDICTS = ("YES", "NO", "UNEXAMINED")

# Not modules: infrastructure, archives, and the docs tree.
NOT_MODULES = ("docs", "tests", "tools", "legacy", "samples", "__pycache__")

KINDS = ("OMISSION", "REPRODUCTION")

KIND_GLOSS = {
    "OMISSION": "the instrument is missing a case, and it is the case the "
                "operator's own frame omits",
    "REPRODUCTION": "the instrument reproduces the operator's processing "
                    "structure in a domain the operator did not intend to "
                    "model",
}


class RegisterError(Exception):
    pass


def modules(root=None):
    """Read the module list off the filesystem, not off a hardcoded list.

    A hardcoded list drifts from the tree, and this repo has already had one
    partial copy of its own folder index go stale.
    """
    root = root or REPO
    if not os.path.isdir(root):
        return []
    out = []
    for name in sorted(os.listdir(root)):
        if name.startswith(".") or name in NOT_MODULES:
            continue
        if os.path.isdir(os.path.join(root, name)):
            out.append(name)
    return out


class Register(object):
    """One row per module. Default UNEXAMINED. Only the operator fills it."""

    def __init__(self, root=None):
        self.rows = {}
        for m in modules(root):
            self.rows[m] = {"module": m, "verdict": "UNEXAMINED",
                            "kind": None, "attributed_to": None, "note": None}

    def mark(self, module, verdict, attributed_to=None, kind=None, note=None):
        if module not in self.rows:
            raise RegisterError(
                "%r is not a module in the tree. The register is read off "
                "the filesystem so it cannot drift from it" % module)
        if verdict not in VERDICTS:
            raise RegisterError("verdict must be one of %s, got %r"
                                % (VERDICTS, verdict))
        if verdict in ("YES", "NO") and not attributed_to:
            raise RegisterError(
                "a YES or a NO must be attributed to the operator. The "
                "question is whether this shape matches a procedure the "
                "OPERATOR already runs unaided, and nobody else can answer "
                "it. An unattributed verdict is this module guessing about "
                "someone else's unaided procedure")
        if verdict == "YES" and kind not in KINDS:
            raise RegisterError(
                "a YES needs a kind: %s. The delivered instance list holds "
                "two different observations and the spec separates them -- "
                "an instrument missing a case is not an instrument "
                "reproducing a procedure" % (KINDS,))
        r = self.rows[module]
        r.update({"verdict": verdict, "kind": kind,
                  "attributed_to": attributed_to, "note": note})
        return r

    def verdict(self, module):
        return self.rows[module]["verdict"]

    def counts(self):
        out = dict((v, 0) for v in VERDICTS)
        for r in self.rows.values():
            out[r["verdict"]] += 1
        return out

    def kind_counts(self):
        out = dict((k, 0) for k in KINDS)
        for r in self.rows.values():
            if r["kind"]:
                out[r["kind"]] += 1
        return out

    def examined(self):
        return [r for r in self.rows.values()
                if r["verdict"] in ("YES", "NO")]

    def base_rate(self):
        """Refused, and the reason is a selection effect, not a small n.

        The examined set is not a sample of the modules. It is the set of
        cases that were salient enough for someone to notice, and noticing
        an echo is the same act as finding one. Three YES out of three
        examined is what that selection produces whether the base rate is
        0.9 or 0.03.
        """
        ex = self.examined()
        yes = [r for r in ex if r["verdict"] == "YES"]
        return {"n_modules": len(self.rows),
                "n_examined": len(ex),
                "n_yes": len(yes),
                "rate": None,
                "state": "REFUSED_SELECTION_EFFECT",
                "why": "the examined set is not a sample. Every row in it "
                       "is there because someone noticed an echo, and "
                       "noticing one is the same act as finding one. A "
                       "denominator built that way cannot carry a rate, at "
                       "any n"}


# --- the delivered instances, at the granularity they were delivered -------
# The spec lists three. They are logged here as delivered, and the register
# above is per MODULE, which is not the same granularity -- see overlap().

INSTANCES = [
    {"ref": "s4",
     "module": "instrument-bias-sims",
     "kind": "OMISSION",
     "shape": "no doe: the selecting agent is absent from the model, and "
              "absent from the literature the model was built against"},
    {"ref": "allocation_coupling",
     "module": "instrument-bias-sims",
     "kind": "OMISSION",
     "shape": "no untenured continuous observer; presence is derived from "
              "tenure"},
    {"ref": "allocation ledger",
     "module": "instrument-bias-sims",
     "kind": "REPRODUCTION",
     "shape": "the module's cost accounting is the same accounting the "
              "operator runs manually before a social retest"},
]

SH = os.path.join(REPO, "instrument-bias-sims")


def already_logged():
    """Which delivered instances are already in the excluded-by-construction
    register, imported rather than restated.

    instrument-bias-sims/excluded_subject.py holds the repo's EXCLUDED-BY-
    CONSTRUCTION list. If the OMISSION instances here are the same entries,
    then two registers agreeing about S4 is one observation counted twice --
    which is the spec's own concern about inherited agreement, arriving in
    the register that was built to track it.
    """
    if not os.path.isdir(SH):
        return {"available": False, "overlap": [], "new": [],
                "why": "instrument-bias-sims is absent, so this is NOT "
                       "CHECKED rather than no overlap"}
    sys.path.insert(0, SH)
    try:
        import excluded_subject as X                          # noqa: E402
    except ImportError:
        return {"available": False, "overlap": [], "new": [],
                "why": "excluded_subject did not import; NOT CHECKED"}
    missing = [(i["sim"], i["missing"]) for i in X.INSTANCES]
    overlap, new = [], []
    for inst in INSTANCES:
        hit = None
        for sim, miss in missing:
            words = [w for w in inst["shape"].lower().split()
                     if len(w) > 3]
            if miss.lower() in inst["shape"].lower() or any(
                    w in miss.lower() for w in words):
                hit = "%s (missing %s)" % (sim, miss)
                break
        (overlap if hit else new).append(
            {"ref": inst["ref"], "kind": inst["kind"], "excluded_as": hit})
    return {"available": True, "overlap": overlap, "new": new,
            "why": "imported from excluded_subject.py; that file is the "
                   "source of truth for the excluded-by-construction list"}


def overlap():
    """What the three instances actually are, once counted."""
    al = already_logged()
    mods = sorted(set(i["module"] for i in INSTANCES))
    return {
        "n_instances": len(INSTANCES),
        "n_modules_touched": len(mods),
        "modules": mods,
        "n_already_excluded": len(al["overlap"]),
        "n_new_to_this_subject": len(al["new"]),
        "checked": al["available"],
        "kinds": dict((k, sum(1 for i in INSTANCES if i["kind"] == k))
                      for k in KINDS),
    }


def seeded():
    """The register with the delivered verdicts in, and nothing else."""
    reg = Register()
    for m in sorted(set(i["module"] for i in INSTANCES)):
        if m in reg.rows:
            reg.mark(m, "YES", attributed_to="operator, delivered spec",
                     kind="REPRODUCTION",
                     note="three instances delivered against this module; "
                          "two OMISSION and one REPRODUCTION. The row "
                          "carries the kind that raises the subject")
    return reg


def confidence():
    return {"who_can_fill_it": "the operator, and only the operator. mark() "
                               "refuses an unattributed YES or NO because "
                               "the question is about someone else's "
                               "unaided procedure",
            "default": "UNEXAMINED for every module, and it is a third "
                       "state, not a soft NO",
            "base_rate": "REFUSED on a selection effect, not on n. The "
                         "examined set is the set of cases someone noticed",
            "the_three_instances": "two are already in the excluded-by-"
                                   "construction register and one is new. "
                                   "All three sit in one module, so the "
                                   "per-module register carries one row",
            "what_a_YES_means": "shared structure between instrument and "
                                "builder. Not a defect, not a discipline "
                                "failure, and not a claim about whether "
                                "the instrument is right",
            "resolved": False}


def breaks():
    return [
        "THE THREE DELIVERED INSTANCES ARE NOT THREE INDEPENDENT "
        "OBSERVATIONS. All three sit inside instrument-bias-sims, which is "
        "one row in a per-module register, and two of the three are already "
        "logged in that folder's excluded-by-construction list -- the same "
        "S4 missing doe and the same S10 missing untenured observer. What is "
        "new to this subject is one instance, the REPRODUCTION one, which is "
        "exactly the one the spec says raises it from a note to a subject. "
        "The count of three is a count of two kinds across one module and "
        "two registers",
        "AND THE MODULE THEY SIT IN IS THE MODULE THAT GOT AUDITED HARDEST. "
        "instrument-bias-sims carries the most scrutiny in this repo, so it "
        "is where echoes would be found first whether or not it is where "
        "they are densest. The instance list is a map of where someone "
        "looked",
        "THE BASE RATE IS NOT MISSING FOR WANT OF n. Every row in the "
        "examined set is there because someone noticed an echo, and noticing "
        "one is the same act as finding one. Three YES out of three examined "
        "is what that selection produces whether the true rate is nine in "
        "ten or three in a hundred, and examining more modules the same way "
        "does not fix it -- only examining modules chosen BEFORE looking "
        "would",
        "NO METHOD IS PROPOSED FOR DETECTING THIS FROM INSIDE, AND THIS "
        "MODULE IS INSIDE. The spec lists that open and nothing here closes "
        "it. mark() refuses to let the downstream model fill a row, which "
        "prevents the register from filling with guesses and does not "
        "produce a detector",
        "THIS MODULE HAS ITS OWN ROW AND IT IS UNEXAMINED. A register of "
        "single-builder echoes, built by the same single builder, is subject "
        "to its own subject. Whether the YES/NO/UNEXAMINED shape is itself a "
        "procedure the operator already runs unaided is a question this file "
        "cannot answer about itself",
    ]


def report():
    L = ["OPERATOR-STRUCTURE ECHO -- the register", "=" * 72, ""]
    L.append("  Observed: instruments built in this ecosystem recur to the")
    L.append("  same structural shape the operator uses to process the")
    L.append("  domain by hand. Not a defect claim. Not a discipline")
    L.append("  failure. A property of a single-builder instrument that")
    L.append("  cannot be removed by effort -- only counted.")
    L.append("")
    L.append("  Do not correct. Log.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    reg = seeded()
    c = reg.counts()
    L.append("  ONE LINE PER MODULE")
    L.append("")
    L.append("    does this shape match a procedure the operator already")
    L.append("    runs unaided?")
    L.append("")
    for v in VERDICTS:
        L.append("    %-12s %d" % (v, c[v]))
    L.append("")
    L.append("    of %d modules read off the tree." % len(reg.rows))
    L.append("")
    for m in sorted(reg.rows):
        r = reg.rows[m]
        if r["verdict"] != "UNEXAMINED":
            L.append("    %-24s %-4s %s"
                     % (m, r["verdict"], r["kind"] or ""))
            for line in _wrap("attributed to: %s" % r["attributed_to"],
                              " " * 6):
                L.append(line)
    L.append("")
    L.append("    every other row is UNEXAMINED, which is a third state.")
    L.append("    Only the operator can change one, and mark() refuses an")
    L.append("    unattributed YES or NO:")
    L.append("")
    try:
        Register().mark("null-harness", "NO")
        r = "ACCEPTED -- the register filled itself"
    except RegisterError:
        r = "REFUSED"
    L.append("      unattributed NO: %s" % r)
    try:
        Register().mark("null-harness", "YES", attributed_to="operator")
        r = "ACCEPTED -- a YES with no kind"
    except RegisterError:
        r = "REFUSED (a YES needs OMISSION or REPRODUCTION)"
    L.append("      YES without a kind: %s" % r)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE TWO KINDS, BECAUSE THE DELIVERED LIST HOLDS TWO")
    L.append("")
    for k in KINDS:
        L.append("    %s" % k)
        for line in _wrap(KIND_GLOSS[k], "      "):
            L.append(line)
    L.append("")
    L.append("  THE THREE DELIVERED INSTANCES, ONCE COUNTED")
    L.append("")
    o = overlap()
    L.append("    instances delivered          %d" % o["n_instances"])
    L.append("    modules they touch           %d  (%s)"
             % (o["n_modules_touched"], ", ".join(o["modules"])))
    L.append("    already excluded-by-constr.  %d" % o["n_already_excluded"])
    L.append("    new to this subject          %d"
             % o["n_new_to_this_subject"])
    L.append("    overlap checked              %s" % o["checked"])
    L.append("")
    for k, n in sorted(o["kinds"].items()):
        L.append("    %-14s %d" % (k, n))
    L.append("")
    al = already_logged()
    for x in al["overlap"]:
        L.append("    %-20s %-13s already logged" % (x["ref"], x["kind"]))
        L.append("      as %s" % x["excluded_as"])
    for x in al["new"]:
        L.append("    %-20s %-13s NEW to this subject"
                 % (x["ref"], x["kind"]))
    L.append("")
    L.append("    The split lands on the kind: both OMISSION instances were")
    L.append("    already registered, and the one REPRODUCTION instance is")
    L.append("    the only new one -- which is the one the spec says raises")
    L.append("    this from a per-repo note to a subject.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE BASE RATE IS REFUSED, AND NOT FOR WANT OF n")
    L.append("")
    br = reg.base_rate()
    L.append("    modules   %d" % br["n_modules"])
    L.append("    examined  %d" % br["n_examined"])
    L.append("    YES       %d" % br["n_yes"])
    L.append("    rate      %s   %s" % (br["rate"], br["state"]))
    L.append("")
    for line in _wrap(br["why"], "    "):
        L.append(line)
    L.append("")
    L.append("  CONFIDENCE, reported separately and not resolved")
    for k in sorted(confidence()):
        L.append("    %s" % k)
        for line in _wrap(str(confidence()[k]), "      "):
            L.append(line)
    L.append("")
    L.append("  WHERE IT BREAKS")
    for b in breaks():
        for line in _wrap("- " + b, "    "):
            L.append(line)
    return "\n".join(L)


def _wrap(t, ind, w=72):
    words, lines, cur = t.split(), [], ind
    for x in words:
        if len(cur) + len(x) + 1 > w and cur.strip():
            lines.append(cur.rstrip())
            cur = ind + x + " "
        else:
            cur += x + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return lines


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    reg = Register()
    ck("the module list is read off the tree, not hardcoded",
       len(reg.rows) > 40 and "null-harness" in reg.rows)
    ck("infrastructure is not a module", "tools" not in reg.rows
       and "tests" not in reg.rows and "docs" not in reg.rows)
    ck("every row defaults UNEXAMINED",
       reg.counts()["UNEXAMINED"] == len(reg.rows))

    try:
        reg.mark("null-harness", "NO")
        ok = False
    except RegisterError:
        ok = True
    ck("an unattributed NO is refused -- only the operator can answer", ok)
    try:
        reg.mark("null-harness", "YES", attributed_to="operator")
        ok = False
    except RegisterError:
        ok = True
    ck("a YES with no kind is refused: the delivered list holds two", ok)
    try:
        reg.mark("not-a-real-folder", "UNEXAMINED")
        ok = False
    except RegisterError:
        ok = True
    ck("a row outside the tree is refused, so the register cannot drift",
       ok)
    reg.mark("null-harness", "NO", attributed_to="operator")
    ck("an attributed NO is accepted and recorded",
       reg.verdict("null-harness") == "NO"
       and reg.rows["null-harness"]["attributed_to"] == "operator")

    ck("UNEXAMINED is a verdict in its own right, not the absence of one",
       "UNEXAMINED" in VERDICTS)

    o = overlap()
    ck("the overlap check actually ran", o["checked"] is True)
    ck("three delivered instances, and they touch ONE module",
       o["n_instances"] == 3 and o["n_modules_touched"] == 1)
    ck("two of three are already in the excluded-by-construction register",
       o["n_already_excluded"] == 2 and o["n_new_to_this_subject"] == 1)
    ck("the kinds split two OMISSION and one REPRODUCTION",
       o["kinds"] == {"OMISSION": 2, "REPRODUCTION": 1})
    al = already_logged()
    ck("and the split lands on the kind: the new one is the REPRODUCTION",
       len(al["new"]) == 1 and al["new"][0]["kind"] == "REPRODUCTION")
    ck("both already-logged ones are the OMISSION kind",
       all(x["kind"] == "OMISSION" for x in al["overlap"]))

    br = Register().base_rate()
    ck("the base rate is refused, and on a selection effect",
       br["rate"] is None and br["state"] == "REFUSED_SELECTION_EFFECT"
       and "same act" in br["why"])

    s = seeded()
    ck("the seeded register carries exactly one YES",
       s.counts()["YES"] == 1 and s.counts()["NO"] == 0)
    ck("and this module's own row is UNEXAMINED",
       s.verdict("operator-structure-echo") == "UNEXAMINED")

    ck("the three-is-not-three finding leads the breaks list",
       "NOT THREE INDEPENDENT OBSERVATIONS" in breaks()[0])
    ck("the selection effect is disclosed as not-a-small-n problem",
       any("NOT MISSING FOR WANT OF n" in b for b in breaks()))
    ck("the module being subject to its own subject is disclosed",
       any("subject to its own subject" in b for b in breaks()))
    ck("no defect claim is made anywhere in the readout",
       "Not a defect claim" in report())
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "ONE LINE PER MODULE" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="operator-structure echo")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
