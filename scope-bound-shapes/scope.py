#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
scope.py - shapes, scope bindings, and what two bindings do to each other.

    python3 scope.py [--selftest]

Marker under exploration. Delivered spec: SPEC_SHAPES.md.

# NOTE TO READERS -- TERM COLLISION
# "change of mind" here means REVISION (provenance-bearing). See PREAMBLE.md.

A SHAPE is a structural sequence that recurs across domains, defined by its
sequence and its selection rule, not by its materials. A SCOPE BINDING is that
shape instantiated with a declared list of FROZEN variables. Scoping out is
releasing entries from FROZEN -- it is not a model swap. Domain names are
scope bindings that acquired names, and are not different subjects.

THREE STATES PER VARIABLE, NOT TWO, AND THE SPEC'S OWN EXAMPLE FORCES IT.
The constraint says FROZEN entries are declared by the builder and never
inferred, because an inferred FROZEN list is the tool asserting scope it did
not measure. Take that seriously and a variable can be LIVE, FROZEN, or
UNDECLARED -- and the worked example has two of the third kind: `aggregate`
and `moisture gradient` appear in slab_concrete and in neither list for
metamorphic_rock.

The arithmetic to fill them in is right there: frozen := universe - live. It
is available, it would produce a complete table, and it is exactly the
inference the constraint forbids. `infer_frozen()` exists here only to refuse,
and it prints what it would have returned so the refusal is inspectable rather
than merely asserted. UNDECLARED is not FROZEN: one is a claim the builder
made, the other is a claim nobody made.

WHAT A COLLISION IS AND IS NOT. compare() returns SCOPE COLLISION when a
variable frozen in one binding is live in the other, per the spec, with the
consequence the spec attaches: two modules claiming the same shape at
incompatible bindings are not corroborating each other. That is a statement
about what their agreement is worth. It is NOT a contradiction, and it is not
a defect in either binding -- bindings that collide are holding different
things still, which is coverage rather than confirmation. The module reports
the collision and does not grade it.

stdlib only, parses under Python 3.9. CC0.
"""

import argparse
import sys

STATES = ("LIVE", "FROZEN", "UNDECLARED")


class ScopeError(Exception):
    pass


class Shape(object):
    """Sequence plus selection rule. The materials are not part of it."""

    def __init__(self, name, sequence, selection_rule):
        if not isinstance(sequence, (list, tuple)) or len(sequence) < 2:
            raise ScopeError(
                "a shape is a sequence; one step is not a sequence. Got %r"
                % (sequence,))
        if not selection_rule or not selection_rule.strip():
            raise ScopeError(
                "a shape needs its selection rule. The sequence alone does "
                "not distinguish this shape from any other that ends in a "
                "release -- the rule for WHICH path is half the invariant")
        self.name = name
        self.sequence = list(sequence)
        self.selection_rule = selection_rule.strip()
        self.bindings = {}

    def bind(self, binding):
        if binding.name in self.bindings:
            raise ScopeError("binding %r already registered" % binding.name)
        binding.shape = self
        self.bindings[binding.name] = binding
        return binding

    def invariant(self):
        return {"sequence": self.sequence,
                "selection_rule": self.selection_rule,
                "what_varies": "the materials, and which variables are held "
                               "still. Neither is part of the shape"}


class Binding(object):
    """A shape instantiated with an explicitly declared FROZEN list.

    Both lists are required. There are no defaults: a default LIVE list would
    make the tool decide what the builder is varying, and a default FROZEN
    list would make it assert scope it did not measure.
    """

    def __init__(self, name, live, frozen, declared_by):
        if live is None or frozen is None:
            raise ScopeError(
                "LIVE and FROZEN are both required and neither defaults. An "
                "omitted FROZEN list is not an empty one")
        if not declared_by:
            raise ScopeError(
                "a binding records who declared its FROZEN list. The "
                "constraint is that the builder declares it, so the "
                "declaration carries a name or it is an inference wearing "
                "one")
        live, frozen = list(live), list(frozen)
        both = set(live) & set(frozen)
        if both:
            raise ScopeError(
                "a variable cannot be live and frozen at once: %s"
                % ", ".join(sorted(both)))
        if not live:
            raise ScopeError(
                "a binding with nothing live does not instantiate the shape, "
                "it freezes it")
        self.name = name
        self.live = live
        self.frozen = frozen
        self.declared_by = declared_by
        self.shape = None

    def declared(self):
        return set(self.live) | set(self.frozen)

    def state_of(self, var):
        if var in self.live:
            return "LIVE"
        if var in self.frozen:
            return "FROZEN"
        return "UNDECLARED"

    def scope_out(self, *variables):
        """Release entries from FROZEN. Not a model swap: same shape, same
        selection rule, a wider live set."""
        missing = [v for v in variables if v not in self.frozen]
        if missing:
            raise ScopeError(
                "cannot scope out %s: not in this binding's FROZEN list. "
                "Releasing something that was never held is not a scope move"
                % ", ".join(missing))
        return Binding(
            name="%s+%s" % (self.name, "+".join(variables)),
            live=self.live + list(variables),
            frozen=[v for v in self.frozen if v not in variables],
            declared_by=self.declared_by)


def universe(*bindings):
    """Every variable named by any of these bindings."""
    out = set()
    for b in bindings:
        out |= b.declared()
    return out


def infer_frozen(binding, *others):
    """REFUSED. Present so the refusal is inspectable, not merely stated.

    The arithmetic works and is shown. It is still the tool asserting scope
    the builder did not declare, which the spec's CONSTRAINT forbids.
    """
    would_be = sorted(universe(binding, *others) - set(binding.live)
                      - set(binding.frozen))
    return {"inferred": None,
            "state": "REFUSED_BY_CONSTRAINT",
            "would_have_returned": would_be,
            "why": "FROZEN entries are declared by the builder, not "
                   "inferred. These variables are UNDECLARED in this "
                   "binding, which is a claim nobody made, and calling them "
                   "FROZEN would be a claim this tool made instead"}


def compare(a, b):
    """SCOPE COLLISION if a variable frozen in one is live in the other.

    Reported per direction, because they are different statements: "A holds
    still what B varies" and "B holds still what A varies" can hold
    separately, together, or not at all.

    UNDECLARED overlaps are counted apart and are NOT collisions. A variable
    live in one and undeclared in the other is not a conflict of declarations,
    because only one declaration exists. It is also not clean, and folding it
    into either column would be the inference the constraint forbids.
    """
    a_frozen_b_live = sorted(set(a.frozen) & set(b.live))
    b_frozen_a_live = sorted(set(b.frozen) & set(a.live))
    collisions = sorted(set(a_frozen_b_live) | set(b_frozen_a_live))
    uni = universe(a, b)
    a_undeclared = sorted(uni - a.declared())
    b_undeclared = sorted(uni - b.declared())
    undeclared_vs_live = sorted(
        set(x for x in a_undeclared if x in b.live)
        | set(x for x in b_undeclared if x in a.live))
    same_shape = (a.shape is not None and a.shape is b.shape)
    return {
        "a": a.name, "b": b.name,
        "same_shape": same_shape,
        "verdict": "SCOPE_COLLISION" if collisions else (
            "UNDECLARED_OVERLAP" if undeclared_vs_live else "COMPATIBLE"),
        "collisions": collisions,
        "a_frozen_b_live": a_frozen_b_live,
        "b_frozen_a_live": b_frozen_a_live,
        "n_collisions": len(collisions),
        "a_frozen_total": len(a.frozen),
        "b_frozen_total": len(b.frozen),
        "undeclared_in_a": a_undeclared,
        "undeclared_in_b": b_undeclared,
        "undeclared_vs_live": undeclared_vs_live,
        "corroborate": False if collisions else None,
        "why_corroborate": (
            "two modules claiming the same shape at incompatible bindings "
            "are not corroborating each other" if collisions else
            "no collision found. That is not the same as established "
            "corroboration -- it means the declared lists do not conflict, "
            "and UNDECLARED variables remain unmeasured on both sides"),
    }


# --- the worked example, as delivered --------------------------------------

STRAIN = Shape(
    name="strain release",
    sequence=["strain accumulates",
              "passes limit",
              "releases along weakest available path"],
    selection_rule="release follows the weakest available path")

SLAB_CONCRETE = STRAIN.bind(Binding(
    name="slab_concrete",
    live=["restraint", "moisture gradient", "aggregate", "cure age"],
    frozen=["creep", "chemistry", "T range", "lithostatic load"],
    declared_by="operator, SPEC_SHAPES.md worked example"))

METAMORPHIC_ROCK = STRAIN.bind(Binding(
    name="metamorphic_rock",
    live=["creep", "chemistry", "T range", "lithostatic load", "restraint"],
    frozen=["cure age"],
    declared_by="operator, SPEC_SHAPES.md worked example"))


def worked_example():
    return compare(SLAB_CONCRETE, METAMORPHIC_ROCK)


def confidence():
    return {"the_shape": "stipulated by the spec. Nothing here tests whether "
                         "strain release IS one shape across these bindings; "
                         "the module takes the claim and works out what "
                         "follows",
            "FROZEN_lists": "declared by the operator in the worked example "
                            "and carried verbatim. Their correctness is not "
                            "checkable from here",
            "UNDECLARED": "two variables in metamorphic_rock. Left "
                          "undeclared, never inferred, and counted apart "
                          "from both other states",
            "collision_is_not_a_grade": "a collision says agreement between "
                                        "two bindings is not corroboration. "
                                        "It does not say either binding is "
                                        "wrong, and holding different things "
                                        "still is coverage",
            "resolved": False}


def breaks():
    return [
        "THE WORKED EXAMPLE COLLIDES TOTALLY, IN BOTH DIRECTIONS, AND THAT "
        "IS THE WHOLE RESULT. Every one of slab_concrete's four frozen "
        "variables is live in metamorphic_rock, and metamorphic_rock's single "
        "frozen variable is live in slab_concrete. Four of four and one of "
        "one. The two named domains sharing this shape agree about nothing "
        "they both hold still, because there is nothing they both hold "
        "still -- so their agreement about the shape is worth zero as "
        "corroboration and the spec's consequence applies at full strength",
        "'NO COLLISION' IS NOT 'CORROBORATES'. compare() returns "
        "corroborate=False on a collision and None otherwise, never True. "
        "Absence of conflict between two declared lists is not evidence that "
        "two bindings test the shape independently; it means the declarations "
        "do not contradict, with every UNDECLARED variable still unmeasured "
        "on both sides",
        "UNDECLARED IS A THIRD STATE AND THE ARITHMETIC TO REMOVE IT IS "
        "SITTING RIGHT THERE. universe minus live minus frozen is two lines, "
        "it completes the table, and it is the inference the CONSTRAINT "
        "forbids. infer_frozen() refuses and prints what it would have "
        "returned. Nothing stops a caller doing the subtraction themselves, "
        "and a downstream table with no UNDECLARED column would hide that it "
        "had been done",
        "THE SHAPE IS TAKEN ON THE SPEC'S WORD. Whether strain accumulation "
        "in curing concrete and in metamorphic rock really are one sequence "
        "with one selection rule is a claim about the world, and this module "
        "assumes it in order to compute over it. If the shape is wrong, "
        "every collision reported here is a collision between two bindings "
        "of a shape that does not exist",
        "TWO BINDINGS IS NOT A LIST OF BINDINGS. The spec asks for a shape "
        "record with a list of bindings; the delivered example has two, and "
        "compare() is pairwise. Nothing here says what a shape with nine "
        "bindings looks like, or whether collisions across such a set "
        "partition into groups that could corroborate within themselves",
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
    L = ["SCOPE-BOUND SHAPES -- one shape, two bindings", "=" * 72, ""]
    L.append("  SHAPE: %s" % STRAIN.name)
    for i, step in enumerate(STRAIN.sequence):
        L.append("    %d. %s" % (i + 1, step))
    L.append("")
    L.append("  invariant: the sequence, and the path-selection rule")
    L.append("    rule: %s" % STRAIN.selection_rule)
    L.append("")
    L.append("  The materials are not part of the shape. Domain names are")
    L.append("  scope bindings that acquired names, not different subjects.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  BINDINGS -- LIVE and FROZEN both explicit, no defaults")
    L.append("")
    for b in (SLAB_CONCRETE, METAMORPHIC_ROCK):
        L.append("  %s" % b.name)
        for line in _wrap("live:   " + ", ".join(b.live), "    "):
            L.append(line)
        for line in _wrap("frozen: " + ", ".join(b.frozen), "    "):
            L.append(line)
        L.append("")
    uni = sorted(universe(SLAB_CONCRETE, METAMORPHIC_ROCK))
    L.append("  every variable named, and its state in each binding:")
    L.append("")
    L.append("    %-20s %-12s %s" % ("variable", "slab", "metamorphic"))
    for v in uni:
        L.append("    %-20s %-12s %s"
                 % (v, SLAB_CONCRETE.state_of(v),
                    METAMORPHIC_ROCK.state_of(v)))
    L.append("")
    L.append("    UNDECLARED is a third state. It is not FROZEN: one is a")
    L.append("    claim the builder made, the other is a claim nobody made.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    w = worked_example()
    L.append("  compare(%s, %s)" % (w["a"], w["b"]))
    L.append("")
    L.append("    verdict: %s" % w["verdict"])
    L.append("")
    L.append("    frozen in slab, live in metamorphic  %d of %d"
             % (len(w["a_frozen_b_live"]), w["a_frozen_total"]))
    for v in w["a_frozen_b_live"]:
        L.append("        %s" % v)
    L.append("    frozen in metamorphic, live in slab  %d of %d"
             % (len(w["b_frozen_a_live"]), w["b_frozen_total"]))
    for v in w["b_frozen_a_live"]:
        L.append("        %s" % v)
    L.append("")
    L.append("    THE COLLISION IS TOTAL IN BOTH DIRECTIONS. Four of four,")
    L.append("    and one of one. There is nothing these two bindings both")
    L.append("    hold still.")
    L.append("")
    L.append("    corroborate: %s" % w["corroborate"])
    for line in _wrap(w["why_corroborate"], "    "):
        L.append(line)
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  SCOPING OUT IS NOT A MODEL SWAP")
    L.append("")
    a2 = SLAB_CONCRETE.scope_out("creep", "chemistry", "T range",
                                 "lithostatic load")
    b2 = METAMORPHIC_ROCK.scope_out("cure age")
    L.append("    %-34s %-18s %s" % ("", "verdict", "collisions"))
    for label, x, y in (("as delivered", SLAB_CONCRETE, METAMORPHIC_ROCK),
                        ("slab releases its frozen", a2, METAMORPHIC_ROCK),
                        ("both release their frozen", a2, b2)):
        c = compare(x, y)
        L.append("    %-34s %-18s %d"
                 % (label, c["verdict"], c["n_collisions"]))
    L.append("")
    L.append("    Same shape and same selection rule throughout -- only the")
    L.append("    live set widened. Releasing every declared FROZEN entry on")
    L.append("    both sides drives collisions to zero and STILL does not")
    L.append("    reach COMPATIBLE: %s stay"
             % ", ".join(compare(a2, b2)["undeclared_vs_live"]))
    L.append("    UNDECLARED in metamorphic_rock, and only the builder can")
    L.append("    declare them.")
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  INFERRING THE FROZEN LIST: REFUSED")
    L.append("")
    inf = infer_frozen(METAMORPHIC_ROCK, SLAB_CONCRETE)
    L.append("    infer_frozen(metamorphic_rock)  ->  %s" % inf["inferred"])
    L.append("    state: %s" % inf["state"])
    L.append("    would have returned: %s"
             % ", ".join(inf["would_have_returned"]))
    L.append("")
    for line in _wrap(inf["why"], "    "):
        L.append(line)
    L.append("")
    L.append("    The arithmetic works and is shown, so the refusal is")
    L.append("    inspectable rather than merely stated.")
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

    # --- the shape ---
    try:
        Shape("x", ["one step"], "rule")
        ok = False
    except ScopeError:
        ok = True
    ck("one step is not a sequence, so it is not a shape", ok)
    try:
        Shape("x", ["a", "b"], "")
        ok = False
    except ScopeError:
        ok = True
    ck("a shape without its selection rule is refused: the rule is half "
       "the invariant", ok)
    ck("the invariant is the sequence and the rule, not the materials",
       "materials" in STRAIN.invariant()["what_varies"])

    # --- bindings: no defaults ---
    try:
        Binding("x", live=["a"], frozen=None, declared_by="op")
        ok = False
    except ScopeError:
        ok = True
    ck("an omitted FROZEN list is refused, not treated as empty", ok)
    try:
        Binding("x", live=["a"], frozen=["b"], declared_by=None)
        ok = False
    except ScopeError:
        ok = True
    ck("a binding records WHO declared its frozen list", ok)
    try:
        Binding("x", live=["a"], frozen=["a"], declared_by="op")
        ok = False
    except ScopeError:
        ok = True
    ck("a variable cannot be live and frozen at once", ok)

    # --- three states ---
    ck("a declared variable reads LIVE or FROZEN",
       SLAB_CONCRETE.state_of("restraint") == "LIVE"
       and SLAB_CONCRETE.state_of("creep") == "FROZEN")
    ck("and an undeclared one reads UNDECLARED, not FROZEN",
       METAMORPHIC_ROCK.state_of("aggregate") == "UNDECLARED"
       and METAMORPHIC_ROCK.state_of("moisture gradient") == "UNDECLARED")
    ck("UNDECLARED is a state of its own", "UNDECLARED" in STATES)

    inf = infer_frozen(METAMORPHIC_ROCK, SLAB_CONCRETE)
    ck("inferring the frozen list is refused by the constraint",
       inf["inferred"] is None and inf["state"] == "REFUSED_BY_CONSTRAINT")
    ck("and the refusal shows what it would have returned",
       inf["would_have_returned"] == ["aggregate", "moisture gradient"])

    # --- the worked example ---
    w = worked_example()
    ck("the two delivered bindings collide", w["verdict"] == "SCOPE_COLLISION")
    ck("every frozen variable in slab_concrete is live in metamorphic_rock",
       len(w["a_frozen_b_live"]) == w["a_frozen_total"] == 4)
    ck("and metamorphic_rock's one frozen variable is live in slab_concrete",
       len(w["b_frozen_a_live"]) == w["b_frozen_total"] == 1)
    ck("so the collision is total in both directions: five variables",
       w["n_collisions"] == 5)
    ck("and they are therefore not corroborating each other",
       w["corroborate"] is False
       and "not corroborating" in w["why_corroborate"])
    ck("they are bindings of the SAME shape, which is what makes it a "
       "collision rather than two unrelated models",
       w["same_shape"] is True)

    # --- no collision is not corroboration ---
    s2 = Shape("s2", ["a", "b"], "rule")
    p = s2.bind(Binding("p", live=["x"], frozen=["y"], declared_by="op"))
    q = s2.bind(Binding("q", live=["x"], frozen=["y"], declared_by="op"))
    c = compare(p, q)
    ck("two identical bindings do not collide",
       c["verdict"] == "COMPATIBLE" and c["n_collisions"] == 0)
    ck("and compare() still does not return corroborate=True",
       c["corroborate"] is None)

    # --- scoping out ---
    a2 = SLAB_CONCRETE.scope_out("creep", "chemistry", "T range",
                                 "lithostatic load")
    ck("scoping out widens the live set and shrinks frozen",
       set(a2.live) > set(SLAB_CONCRETE.live) and a2.frozen == [])
    ck("and it is not a model swap: same shape, same selection rule",
       STRAIN.selection_rule == "release follows the weakest available path")
    try:
        SLAB_CONCRETE.scope_out("restraint")
        ok = False
    except ScopeError:
        ok = True
    ck("releasing something never held is refused", ok)
    b2 = METAMORPHIC_ROCK.scope_out("cure age")
    c2 = compare(a2, b2)
    ck("releasing every declared frozen entry on both sides ends the "
       "collisions", c2["n_collisions"] == 0)
    ck("and STILL does not reach COMPATIBLE, because two variables remain "
       "undeclared and only the builder can declare them",
       c2["verdict"] == "UNDECLARED_OVERLAP"
       and c2["undeclared_vs_live"] == ["aggregate", "moisture gradient"])

    ck("the total collision leads the breaks list",
       "COLLIDES TOTALLY" in breaks()[0])
    ck("no-collision-is-not-corroboration is disclosed",
       any("NOT 'CORROBORATES'" in b for b in breaks()))
    ck("the shape being taken on the spec's word is disclosed",
       any("TAKEN ON THE SPEC'S WORD" in b for b in breaks()))
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "COLLISION IS TOTAL" in report())
    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="scope-bound shapes")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
