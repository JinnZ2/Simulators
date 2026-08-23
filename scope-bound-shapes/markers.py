#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
markers.py - marker | stability | bindings_tested | known_exceptions.

    python3 markers.py [--selftest]

Marker under exploration. Delivered spec: SPEC_SHAPES.md.

STABILITY WITHOUT BINDINGS_TESTED IS NOT A CLAIM, AND THE TABLE REFUSES TO
PRINT ONE WITHOUT THE OTHER. That is the spec's rule and it is enforced in
two places rather than stated once: `set_stability()` raises if the bindings
list is empty, and `row()` raises if a stability value is present with no
bindings behind it. A stability that survived only the first guard would
still reach a reader through the second.

A marker's stability is a claim about recurrence across bindings. One binding
is where a marker was found, not where it was tested -- the shape is defined
across domains, so a marker verified inside a single scope binding has been
checked exactly where it came from.

ZERO KNOWN EXCEPTIONS WITH ZERO BINDINGS TESTED IS NOT_LOOKED, NOT CLEAN.
An empty exception list reads as a clean record and here it is an empty
record. The two are distinguished by the bindings count beside them and by an
explicit state on every row, never by the emptiness of the list.

WHAT IS IN THE TABLE, AND WHY IT IS ALL UNTESTED. The delivered material
gives a shape, its selection rule, and two bindings. It gives no test record.
So the markers below are the ones the shape itself names -- one per sequence
step, plus the selection rule's own signature -- and every one of them carries
stability None, bindings_tested empty, state UNTESTED. That is the honest
state of the table on delivery, not a placeholder to be filled by whoever
reads it next.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import scope as S                                              # noqa: E402

STATES = ("UNTESTED", "TESTED", "REFUTED")

# A marker verified in one binding has been checked where it was found. The
# shape is defined across domains, so a stability claim needs more than one.
MIN_BINDINGS_FOR_STABILITY = 2


class MarkerError(Exception):
    pass


class Marker(object):
    """One row. stability and bindings_tested move together or not at all."""

    def __init__(self, name, what_it_indicates, derived_from):
        self.name = name
        self.what_it_indicates = what_it_indicates
        self.derived_from = derived_from
        self.stability = None
        self.bindings_tested = []
        self.known_exceptions = []

    def set_stability(self, value, bindings_tested, attributed_to):
        if not bindings_tested:
            raise MarkerError(
                "stability without bindings_tested is not a claim. A "
                "stability value is a statement about recurrence ACROSS "
                "bindings, and with no bindings behind it there is nothing "
                "for it to be a statement about")
        if len(bindings_tested) < MIN_BINDINGS_FOR_STABILITY:
            raise MarkerError(
                "one binding is where a marker was found, not where it was "
                "tested. The shape is defined across domains, so a stability "
                "claim from a single binding has been checked exactly where "
                "it came from")
        if not attributed_to:
            raise MarkerError(
                "a stability claim carries who tested it. Otherwise the "
                "table records a number with no one behind it")
        self.stability = value
        self.bindings_tested = list(bindings_tested)
        self.attributed_to = attributed_to
        return self

    def add_exception(self, binding, note):
        if binding not in self.bindings_tested:
            raise MarkerError(
                "an exception is a failure observed in a binding that was "
                "tested. %r is not in bindings_tested, so this records a "
                "failure in a place nobody looked" % binding)
        self.known_exceptions.append({"binding": binding, "note": note})
        return self

    def state(self):
        if not self.bindings_tested:
            return "UNTESTED"
        if self.known_exceptions and self.stability is None:
            return "REFUTED"
        return "TESTED"

    def exceptions_state(self):
        """Empty is not clean unless something was looked at."""
        if not self.bindings_tested:
            return "NOT_LOOKED"
        return "NONE_FOUND" if not self.known_exceptions else "FOUND"

    def row(self):
        """The four columns. Refuses to emit a stability with no bindings."""
        if self.stability is not None and not self.bindings_tested:
            raise MarkerError(
                "refusing to emit a row with a stability value and no "
                "bindings_tested. The guard on set_stability() is not the "
                "only way a value reaches this field, and a stability that "
                "got past it must not reach a reader")
        return {"marker": self.name,
                "stability": self.stability,
                "bindings_tested": list(self.bindings_tested),
                "n_bindings": len(self.bindings_tested),
                "known_exceptions": list(self.known_exceptions),
                "exceptions_state": self.exceptions_state(),
                "state": self.state(),
                "indicates": self.what_it_indicates,
                "derived_from": self.derived_from}


class MarkerTable(object):
    def __init__(self, shape):
        self.shape = shape
        self.markers = []

    def add(self, marker):
        self.markers.append(marker)
        return marker

    def rows(self):
        return [m.row() for m in self.markers]

    def counts(self):
        out = dict((s, 0) for s in STATES)
        for m in self.markers:
            out[m.state()] += 1
        return out

    def established(self):
        """Rows carrying a stability claim with bindings behind it."""
        return [r for r in self.rows()
                if r["stability"] is not None
                and r["n_bindings"] >= MIN_BINDINGS_FOR_STABILITY]


def table():
    """The markers the shape itself names. No test record was delivered."""
    t = MarkerTable(S.STRAIN)
    t.add(Marker("strain accumulation is observable",
                 "step 1 of the sequence is in progress",
                 "shape sequence, step 1"))
    t.add(Marker("a limit is crossed rather than approached",
                 "step 2: the transition is a passage, not an asymptote",
                 "shape sequence, step 2"))
    t.add(Marker("release is localised to one path",
                 "step 3: release goes somewhere specific",
                 "shape sequence, step 3"))
    t.add(Marker("the release path is the weakest available path",
                 "the selection rule itself, which is half the invariant",
                 "shape selection rule"))
    return t


def confidence():
    return {"the_table": "four markers, zero stability claims, zero "
                         "bindings tested. That is the delivered state: a "
                         "shape and two bindings arrived with no test "
                         "record",
            "the_markers": "derived from the shape's own sequence and "
                           "selection rule, which is the only source "
                           "available. Whether they are the RIGHT markers "
                           "is untested and is a different question from "
                           "whether they are stable",
            "MIN_BINDINGS": "two, chosen because one binding is where a "
                            "marker was found. Two is a floor, not a "
                            "sufficient number, and nothing here establishes "
                            "what a sufficient number would be",
            "empty_exceptions": "NOT_LOOKED on every row. An empty exception "
                                "list beside zero bindings is an empty "
                                "record, not a clean one",
            "resolved": False}


def breaks():
    return [
        "EVERY ROW IS UNTESTED AND THE TABLE'S ONLY REAL OUTPUT IS THAT. "
        "Four markers, zero stability claims, zero bindings tested, zero "
        "known exceptions -- and the last of those reads as a clean record "
        "when it is an empty one. The exceptions_state column exists to say "
        "NOT_LOOKED rather than let an empty list imply NONE_FOUND, which is "
        "the whole difference between a marker nobody has challenged and a "
        "marker that survived a challenge",
        "THE MARKERS WERE DERIVED FROM THE SHAPE, WHICH IS THE ONLY SOURCE "
        "AVAILABLE AND IS ALSO CIRCULAR. Each row is one step of the "
        "sequence or the selection rule restated as something observable. A "
        "marker built that way cannot fail to indicate the shape when the "
        "shape holds; what it can do is fail to be observable, or fail to "
        "discriminate, and neither has been checked in any binding",
        "TWO BINDINGS IS THE FLOOR AND IT IS ARBITRARY. MIN_BINDINGS_FOR_"
        "STABILITY is set at two on the reasoning that one binding is where "
        "a marker was found rather than where it was tested. Nothing "
        "establishes that two is enough, and the two bindings actually "
        "delivered collide totally -- so even a two-binding stability claim "
        "over slab_concrete and metamorphic_rock would be a claim across a "
        "pair that scope.py says are not corroborating each other",
        "THE REFUSAL IS ENFORCED TWICE AND CAN STILL BE WALKED AROUND. "
        "set_stability() guards the write and row() guards the read, so a "
        "value assigned directly to .stability is caught on the way out. A "
        "caller who sets .stability and .bindings_tested together, with "
        "nothing behind either, passes both guards -- the table checks that "
        "the columns move together, not that the bindings were really "
        "tested",
    ]


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


def report():
    L = ["MARKER TABLE -- %s" % S.STRAIN.name, "=" * 72, ""]
    t = table()
    L.append("  stability without bindings_tested is not a claim.")
    L.append("  The table refuses to print one without the other.")
    L.append("")
    L.append("  %-38s %-10s %-6s %s"
             % ("marker", "stability", "bind", "exceptions"))
    L.append("  " + "-" * 70)
    for r in t.rows():
        L.append("  %-38s %-10s %-6d %s"
                 % (r["marker"][:38],
                    "None" if r["stability"] is None else r["stability"],
                    r["n_bindings"], r["exceptions_state"]))
    L.append("")
    c = t.counts()
    L.append("  states: %s"
             % ", ".join("%s=%d" % (k, v) for k, v in sorted(c.items())))
    L.append("  rows carrying an established stability claim: %d"
             % len(t.established()))
    L.append("")
    L.append("  Every row is UNTESTED. The delivered material gives a shape,")
    L.append("  a selection rule and two bindings, and no test record. The")
    L.append("  markers are the ones the shape itself names.")
    L.append("")
    L.append("  exceptions read NOT_LOOKED, not NONE_FOUND. An empty")
    L.append("  exception list beside zero bindings is an empty record.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  THE REFUSALS, EXERCISED")
    L.append("")
    m = Marker("demo", "demo", "demo")
    try:
        m.set_stability(0.9, [], attributed_to="someone")
        r1 = "ACCEPTED -- a stability with nothing behind it"
    except MarkerError:
        r1 = "REFUSED"
    L.append("    stability, no bindings:        %s" % r1)
    try:
        m.set_stability(0.9, ["slab_concrete"], attributed_to="someone")
        r2 = "ACCEPTED -- one binding read as tested"
    except MarkerError:
        r2 = "REFUSED (found != tested)"
    L.append("    stability, one binding:        %s" % r2)
    m2 = Marker("demo2", "demo", "demo")
    m2.stability = 0.9                       # written straight past the guard
    try:
        m2.row()
        r3 = "ACCEPTED -- it reached the reader"
    except MarkerError:
        r3 = "REFUSED at the read as well"
    L.append("    written past set_stability():  %s" % r3)
    m3 = Marker("demo3", "demo", "demo")
    try:
        m3.add_exception("slab_concrete", "failed here")
        r4 = "ACCEPTED -- a failure in a place nobody looked"
    except MarkerError:
        r4 = "REFUSED (not in bindings_tested)"
    L.append("    exception, binding untested:   %s" % r4)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  AND IF IT WERE TESTED, THE TWO AVAILABLE BINDINGS COLLIDE")
    L.append("")
    w = S.worked_example()
    L.append("    compare(%s," % w["a"])
    L.append("            %s)" % w["b"])
    L.append("      -> %s, %d variables"
             % (w["verdict"], w["n_collisions"]))
    L.append("")
    L.append("    So a two-binding stability claim over the only two")
    L.append("    bindings delivered would be a claim across a pair that")
    L.append("    scope.py says are not corroborating each other. The floor")
    L.append("    of two is met and the claim is still not what it looks")
    L.append("    like.")
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


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    t = table()
    ck("the table has the four columns the spec names",
       set(("marker", "stability", "bindings_tested",
            "known_exceptions")) <= set(t.rows()[0]))
    ck("every delivered row is UNTESTED -- no test record arrived",
       t.counts()["UNTESTED"] == len(t.markers) == 4)
    ck("and zero rows carry an established stability claim",
       len(t.established()) == 0)
    ck("stability is None everywhere, not zero",
       all(r["stability"] is None for r in t.rows()))
    ck("empty exceptions read NOT_LOOKED, never NONE_FOUND",
       all(r["exceptions_state"] == "NOT_LOOKED" for r in t.rows()))

    m = Marker("m", "i", "d")
    try:
        m.set_stability(0.9, [], attributed_to="op")
        ok = False
    except MarkerError:
        ok = True
    ck("stability with no bindings_tested is refused at the write", ok)
    try:
        m.set_stability(0.9, ["one"], attributed_to="op")
        ok = False
    except MarkerError:
        ok = True
    ck("one binding is refused: that is where it was found, not tested", ok)
    try:
        m.set_stability(0.9, ["one", "two"], attributed_to=None)
        ok = False
    except MarkerError:
        ok = True
    ck("a stability claim carries who tested it", ok)

    m2 = Marker("m2", "i", "d")
    m2.stability = 0.9
    try:
        m2.row()
        ok = False
    except MarkerError:
        ok = True
    ck("a stability written straight past the guard is refused at the read "
       "as well -- one guard is not enough", ok)

    m3 = Marker("m3", "i", "d")
    try:
        m3.add_exception("slab_concrete", "failed")
        ok = False
    except MarkerError:
        ok = True
    ck("an exception in an untested binding is refused: it records a "
       "failure where nobody looked", ok)

    good = Marker("g", "i", "d")
    good.set_stability(0.8, ["slab_concrete", "metamorphic_rock"],
                       attributed_to="operator")
    r = good.row()
    ck("a properly attributed two-binding claim is accepted and emits",
       r["stability"] == 0.8 and r["n_bindings"] == 2
       and r["state"] == "TESTED")
    ck("and its exceptions now read NONE_FOUND rather than NOT_LOOKED",
       r["exceptions_state"] == "NONE_FOUND")
    good.add_exception("slab_concrete", "did not fire below the limit")
    ck("an exception in a tested binding is accepted",
       good.row()["exceptions_state"] == "FOUND")

    w = S.worked_example()
    ck("and the only two bindings available collide, so even a two-binding "
       "claim would sit on a non-corroborating pair",
       w["verdict"] == "SCOPE_COLLISION" and w["corroborate"] is False)

    ck("everything-untested leads the breaks list",
       "EVERY ROW IS UNTESTED" in breaks()[0])
    ck("the markers being derived from the shape, and circular, is "
       "disclosed",
       any("is also circular" in b.lower() for b in breaks()))
    ck("the walk-around on the double guard is disclosed",
       any("passes both guards" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders and exercises the refusals",
       "THE REFUSALS, EXERCISED" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="marker table")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
