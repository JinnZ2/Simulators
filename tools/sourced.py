# SPDX-License-Identifier: CC0-1.0
"""
A value and its source travel together.

Three fields on every extracted value: the VALUE, the LITERAL SOURCE TEXT
it came from, and the LOCATOR -- which document, which line, which columns.
Then one gate. Anything entering a scoring function carries all three or the
scoring function returns UNRATED: not zero, not clean, not a default.

WHY THIS EXISTS. Three defects landed in one folder in one session and all
three have the same shape -- a value that could not have named its source:

  1. `entries_v2.amended_scores` built the amended score with
     `lstrip("-> ")`. lstrip takes a CHARACTER SET, so on an amendment cell
     reading `-> --   A-01` it stripped the value's own leading `--` along
     with the arrow and returned the UNAMENDED score, on the map whose own
     rule is that the amended score is authoritative.
  2. `register_v2._has_duration` first tested for a bare numeral, so the
     cross-reference `(see DUR-006)` scored as a stated lifetime and
     `exceeds ~1` scored as a retention horizon carrying a value. Both
     false positives ran toward reporting a falsifier as APPLICABLE.
  3. A `register(...)` call for a new metric landed after a `finally`
     inside a helper and never executed. The registry reported one fewer
     metric than the file contains and nothing said so.

Each produced a value whose stated source does not support it, and no
amount of reading the code found any of them. Running did.

WHY A SPAN AND NOT CONTAINMENT. Checking that the value appears ANYWHERE
in the source text is the obvious rule and it is not sufficient. On defect
1 it catches V3 -- the buggy value `+` does not occur in `-> --   A-01` --
and it MISSES V6, where the buggy value `-` does occur in `-> --   A-02`,
via the hyphen of the arrow and the hyphen of the amendment id. So the
primitive is a SPAN: offsets into the source text, verified by slicing.
Under the buggy path no span exists at all, because the value was never
located in the cell it claims to come from. Both cases refuse.

A value that is COMPUTED rather than sliced declares a `derivation`
instead. Exactly one of span and derivation, never both and never neither
-- a computed value with no stated derivation is the same silence in a
different place.

WHAT THIS DOES NOT DO. It does not check that the source is TRUE, or that
the locator points at the right cell. It checks that the three fields are
mutually consistent. A locator naming the wrong line with source text
copied from that same wrong line passes; that is a different failure and
`Locator.boundary_clean` addresses one narrow form of it (a fixed-width
column boundary that cuts a token in half) and nothing addresses the rest.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.

    python3 tools/sourced.py --selftest
"""

from __future__ import annotations

import sys

UNRATED = "UNRATED"

# Time units for numeral_with_unit's default vocabulary. A word list, and
# a paraphrase steps around it -- stated here rather than at the bottom.
TIME_UNITS = ("year", "yr", "month", "week", "day", "decade", "century",
              "generation", "hour", "minute", "second")


class Unrated(object):
    """The refusal. Falsy, so `if value:` cannot read it as a pass, and
    carrying the reason plus which of the three fields was missing.

    Equal to the string UNRATED so a render or a test can compare against
    the word without importing the class."""

    __slots__ = ("reason", "missing", "where")

    def __init__(self, reason, missing=(), where=None):
        self.reason = reason
        self.missing = tuple(missing)
        self.where = where

    def __bool__(self):
        return False

    __nonzero__ = __bool__

    def __repr__(self):
        w = " at %s" % self.where if self.where else ""
        m = " missing=%s" % (",".join(self.missing),) if self.missing else ""
        return "UNRATED(%s%s%s)" % (self.reason, m, w)

    def __eq__(self, other):
        if isinstance(other, Unrated):
            return self.reason == other.reason
        return other == UNRATED

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((UNRATED, self.reason))


class Locator(object):
    """Which document, which line, which columns. `col_start`/`col_end`
    are None for a whole-line locator."""

    __slots__ = ("doc", "line_no", "col_start", "col_end", "label")

    def __init__(self, doc, line_no, col_start=None, col_end=None,
                 label=None):
        self.doc = doc
        self.line_no = line_no
        self.col_start = col_start
        self.col_end = col_end
        self.label = label

    def describe(self):
        cols = ""
        if self.col_start is not None:
            cols = " cols %s:%s" % (self.col_start, self.col_end)
        lab = " (%s)" % self.label if self.label else ""
        return "%s line %s%s%s" % (self.doc, self.line_no, cols, lab)

    __str__ = describe

    def __repr__(self):
        return "Locator(%s)" % self.describe()

    def cell(self, line_text):
        if self.col_start is None:
            return line_text
        return line_text[self.col_start:self.col_end]

    def boundary_clean(self, line_text):
        """A fixed-width column boundary is a CLAIM about where a cell
        ends. If the character on each side of a boundary is non-space the
        boundary cuts a token in half and the claim is false: the cell to
        the left is truncated and the cell to the right begins with
        somebody else's text.

        Returns (ok, cuts) where cuts names the offending boundaries."""
        if self.col_start is None:
            return True, ()
        cuts = []
        for name, k in (("start", self.col_start), ("end", self.col_end)):
            if k is None or k <= 0 or k >= len(line_text):
                continue
            if not line_text[k - 1].isspace() and not line_text[k].isspace():
                cuts.append(name)
        return (not cuts), tuple(cuts)


class Sourced(object):
    """value + source_text + locator, with exactly one of span/derivation.

    `render` is how a slice of the source becomes the value; the default
    strips surrounding whitespace, which is what a fixed-width cell needs.
    A parser doing more than that says so."""

    __slots__ = ("value", "source_text", "locator", "span", "derivation",
                 "render")

    def __init__(self, value, source_text, locator, span=None,
                 derivation=None, render=None):
        self.value = value
        self.source_text = source_text
        self.locator = locator
        self.span = span
        self.derivation = derivation
        self.render = render or (lambda s: s.strip())

    def __repr__(self):
        how = ("span=%s" % (self.span,) if self.span is not None
               else "derivation=%r" % self.derivation)
        return "Sourced(%r, %s, %s)" % (self.value, how,
                                        self.locator.describe()
                                        if self.locator else None)


def gate(x, name="value"):
    """The one gate. Returns `x` when the three fields are present and
    mutually consistent, an `Unrated` otherwise. An `Unrated` handed in
    comes straight back out, so a gate can be applied twice without
    laundering a refusal."""
    if isinstance(x, Unrated):
        return x
    if not isinstance(x, Sourced):
        return Unrated("not_sourced", missing=("value", "source", "locator"),
                       where=name)
    missing = []
    if x.value is None or x.value == "":
        missing.append("value")
    if not isinstance(x.source_text, str) or x.source_text == "":
        missing.append("source")
    if x.locator is None or not isinstance(x.locator, Locator):
        missing.append("locator")
    if missing:
        return Unrated("field_absent", missing=missing, where=name)

    has_span = x.span is not None
    has_der = x.derivation is not None and x.derivation != ""
    if has_span and has_der:
        return Unrated("ambiguous_provenance", where=name)
    if not has_span and not has_der:
        return Unrated("no_provenance", where=name)

    if has_span:
        try:
            i, j = x.span
        except (TypeError, ValueError):
            return Unrated("malformed_span", where=name)
        if not isinstance(i, int) or not isinstance(j, int) \
                or i < 0 or j > len(x.source_text) or i >= j:
            return Unrated("span_out_of_range", where=name)
        if x.render(x.source_text[i:j]) != x.value:
            return Unrated("span_mismatch", where=name)
    return x


def gate_all(**named):
    """Gate several values at once. Returns the first `Unrated` in the
    order given, or None when every one passes. A scoring function that
    calls this and returns the result on a non-None is refusing, not
    defaulting."""
    for name in sorted(named):
        g = gate(named[name], name=name)
        if isinstance(g, Unrated):
            return g
    return None


def value_of(x, default=UNRATED):
    """The value, or the sentinel. Never a zero and never a blank -- the
    caller has to see the refusal or write the default out loud."""
    g = gate(x)
    return g.value if isinstance(g, Sourced) else default


def find_span(source_text, value, render=None):
    """Locate `value` in `source_text` and return the span, or None.

    Used by a parser to BUILD a Sourced honestly. It is not the gate: the
    gate verifies a span the parser claims, and a parser that cannot find
    one has a value from somewhere else and must say so."""
    render = render or (lambda s: s.strip())
    if not isinstance(value, str) or value == "":
        return None
    i = source_text.find(value)
    while i >= 0:
        j = i + len(value)
        if render(source_text[i:j]) == value:
            return (i, j)
        i = source_text.find(value, i + 1)
    return None


def slice_sourced(source_text, i, j, locator, render=None):
    """Build a Sourced from a slice. The value cannot disagree with its
    span by construction, which is the point: a parser that slices gets
    provenance free and a parser that computes has to declare it."""
    render = render or (lambda s: s.strip())
    return Sourced(render(source_text[i:j]), source_text, locator,
                   span=(i, j), render=render)


def numeral_with_unit(source_text, locator, units=TIME_UNITS, window=14):
    """A numeral with a unit token adjacent to it, or a refusal.

    `~1` is not a lifetime, `(see DUR-006)` is not a lifetime, and a bare
    numeral test reports both as one. The span returned covers the numeral
    and the unit together, so what the gate verifies is the quantity and
    not the digit."""
    low = source_text.lower()
    best = None
    for u in units:
        k = 0
        while True:
            k = low.find(u, k)
            if k < 0:
                break
            lo = max(0, k - window)
            seg = low[lo:k]
            start = None
            for idx in range(len(seg) - 1, -1, -1):
                if seg[idx].isdigit():
                    start = idx
                    while start > 0 and (seg[start - 1].isdigit()
                                         or seg[start - 1] in ".,"):
                        start -= 1
                    break
            if start is not None:
                i = lo + start
                j = k + len(u)
                while j < len(low) and low[j].isalpha():
                    j += 1
                if best is None or (j - i) < (best[1] - best[0]):
                    best = (i, j)
            k += len(u)
    if best is None:
        return Unrated("no_unit_adjacent_to_numeral",
                       where=locator.describe() if locator else None)
    return slice_sourced(source_text, best[0], best[1], locator)


def registry_complete(expected, registered, label="registry"):
    """Expected against registered at end of run.

    The same rule applied to a registry: a registration is a value whose
    source is the call site, and a call site that did not execute leaves a
    count that names it. This is what catches a `register(...)` shadowed by
    a `finally` -- a defect invisible in a diff and invisible in a passing
    run, because everything registered still passes."""
    exp = set(expected)
    reg = set(registered)
    missing = sorted(exp - reg)
    extra = sorted(reg - exp)
    if not missing and not extra:
        state = "COMPLETE"
    elif missing and not extra:
        state = "SHORT"
    elif extra and not missing:
        state = "OVER"
    else:
        state = "DIVERGED"
    return {"label": label, "expected": len(exp), "registered": len(reg),
            "missing": missing, "extra": extra, "state": state,
            "ok": state == "COMPLETE"}


# ---------------------------------------------------------------- selftest

def _checks():
    out = []

    def ck(name, cond, detail=""):
        out.append((name, bool(cond), detail))

    doc = "WORK_ORDER_V2.md"
    line = "V6      +  stone, parchment    -  format rot             " \
           "-> --   A-02"
    cell = line[57:]
    loc = Locator(doc, 6, 57, None, "amendment")

    # 1. THE DEFECT REPLAY. Under lstrip("-> ") the amended score for V6
    # came out as `-`, the UNAMENDED sign, with the amendment cell named as
    # its source. Containment passes; the gate refuses.
    ck("V6 buggy value IS contained in its claimed source", "-" in cell)
    buggy = Sourced("-", cell, loc, span=find_span(cell, "-"))
    ck("containment-only would pass V6",
       find_span(cell, "-") is not None)
    # the honest build: the value was never located in the amendment cell,
    # so a parser building it truthfully has no span to offer.
    honest = Sourced("-", cell, loc)
    ck("V6 no-span build refuses", gate(honest) == UNRATED)
    ck("V6 refusal names no_provenance",
       gate(honest).reason == "no_provenance")

    # 2. V3. The buggy value does not occur in the cell at all.
    cell3 = "-> --   A-01"
    ck("V3 buggy value is NOT contained", find_span(cell3, "+") is None)
    bad3 = Sourced("+", cell3, Locator(doc, 3, 57, None, "amendment"),
                   span=(0, 2))
    ck("V3 claimed span mismatches", gate(bad3).reason == "span_mismatch")

    # 3. THE CORRECT PARSE. `--` really is at offset 3:5 of the cell.
    good = slice_sourced(cell, 3, 5, loc)
    ck("correct amended value is --", good.value == "--")
    ck("correct amended value passes the gate",
       gate(good) is good)

    # 4. Each missing field refuses on its own.
    ck("no source refuses",
       gate(Sourced("--", "", loc, span=(0, 2))).reason == "field_absent")
    ck("no locator refuses",
       gate(Sourced("--", cell, None, span=(3, 5))).reason == "field_absent")
    ck("no value refuses",
       gate(Sourced("", cell, loc, span=(3, 5))).reason == "field_absent")
    ck("plain string refuses", gate("--").reason == "not_sourced")
    ck("None refuses", gate(None).reason == "not_sourced")

    # 5. Derivation is the other admissible provenance, and exactly one.
    der = Sourced(0.478, "0.9^7", loc, derivation="product of marginals")
    ck("declared derivation passes", gate(der) is der)
    both = Sourced("--", cell, loc, span=(3, 5), derivation="also computed")
    ck("span AND derivation refuses",
       gate(both).reason == "ambiguous_provenance")

    # 6. Unrated is falsy, equal to the word, and survives a second gate.
    u = gate(honest)
    ck("Unrated is falsy", not u)
    ck("Unrated equals the string", u == UNRATED)
    ck("Unrated re-gated is unchanged", gate(u) is u)
    ck("value_of returns the sentinel", value_of(honest) == UNRATED)
    ck("value_of returns the value", value_of(good) == "--")

    # 7. gate_all returns the first refusal in name order, None when clean.
    ck("gate_all clean is None", gate_all(a=good, b=der) is None)
    ck("gate_all refuses", gate_all(a=good, b=honest) == UNRATED)

    # 8. THE NUMERAL RULE. Both of _has_duration's false positives refuse.
    lc = Locator(doc, 1, None, None, "condition")
    ck("(see DUR-006) is not a lifetime",
       numeral_with_unit("(see DUR-006)", lc) == UNRATED)
    ck("exceeds ~1 is not a lifetime",
       numeral_with_unit("hop count over the retention horizon "
                         "exceeds ~1", lc) == UNRATED)
    ck("refusal names the unit",
       numeral_with_unit("~1", lc).reason == "no_unit_adjacent_to_numeral")
    d = numeral_with_unit("expected lifetime 18 months", lc)
    ck("18 months is a lifetime", gate(d) is d)
    ck("18 months span covers the quantity", d.value == "18 months")
    d2 = numeral_with_unit("retained for 7 years after decommissioning", lc)
    ck("7 years is a lifetime", d2.value == "7 years")
    ck("a unit with no numeral refuses",
       numeral_with_unit("several years", lc) == UNRATED)
    ck("a numeral far from the unit refuses",
       numeral_with_unit("DUR-006 discusses this at length in years", lc)
       == UNRATED)

    # 9. THE COLUMN BOUNDARY. The V2 row of the loss-variable map runs its
    # ML cell past column 57, so the slice cuts a token and the amendment
    # column reads `ate, hw)` -- text belonging to its left neighbour.
    v2line = "V2      -- high (the ash)      -- high (versions, data " \
             "state, hw)"
    ok, cuts = Locator(doc, 2, 31, 57, "ml").boundary_clean(v2line)
    ck("V2 column boundary cuts a token", not ok and "end" in cuts)
    ok6, cuts6 = Locator(doc, 6, 31, 57, "ml").boundary_clean(line)
    ck("V6 column boundary is clean", ok6 and not cuts6)
    ck("whole-line locator has no boundary to cut",
       Locator(doc, 2, None, None).boundary_clean(v2line)[0])

    # 10. THE REGISTRY RULE.
    r = registry_complete(["a", "b", "c"], ["a", "b", "c"], "t")
    ck("complete registry is COMPLETE", r["state"] == "COMPLETE" and r["ok"])
    r = registry_complete(["a", "b", "c"], ["a", "b"], "t")
    ck("a shadowed registration reads SHORT",
       r["state"] == "SHORT" and r["missing"] == ["c"] and not r["ok"])
    r = registry_complete(["a"], ["a", "b"], "t")
    ck("an unexpected registration reads OVER", r["state"] == "OVER")
    r = registry_complete(["a", "b"], ["a", "c"], "t")
    ck("both directions read DIVERGED", r["state"] == "DIVERGED")

    # 11. NULL TESTS. Every check above is a refusal or a pass; a gate
    # that refused everything would satisfy the refusals alone, so these
    # assert the clean direction is reachable and the dirty one is not
    # reachable by accident.
    ck("the gate is not CONSTANT_SILENT",
       gate(good) is good and gate(der) is der and gate(d) is d)
    ck("the gate is not CONSTANT_FIRES",
       gate(honest) == UNRATED and gate(bad3) == UNRATED
       and gate("--") == UNRATED)
    ck("find_span is not CONSTANT_SILENT",
       find_span(cell, "--") == (3, 5))
    ck("the buggy V6 build differs from the honest one only in the span",
       buggy.value == honest.value and buggy.span is not None
       and honest.span is None)

    return out


def selftest():
    rows = _checks()
    bad = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        print("%-4s %s%s" % ("ok" if ok else "FAIL", name,
                             (" -- " + detail) if detail else ""))
    print()
    print("checks: %d   failed: %d" % (len(rows), len(bad)))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(__doc__.strip())
    print()
    print("run with --selftest")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
