# invariant.py -- WO-4 step 1: a formal statement of the invariant, made checkable.
#
# The order's step 1:
#   "Attempt a formal statement of the invariant: minimum conditions under
#    which local correctness plus an unowned join produces undetectable
#    failure. If it can be stated formally, it can be checked."
#
# THE STATEMENT
#
#   Let O be a set of observables.
#   Let K = {k_1 .. k_n} be components, each carrying a DECLARED scope
#   S(k) subset of O -- the observables that component's own correctness
#   condition ranges over.
#   Let J subset of O be a join: a set of observables whose relation is the
#   property in question.
#
#   A1  n >= 2
#   A2  for every k: k is correct with respect to S(k)      (LOCAL CORRECTNESS)
#   A3  J is non-empty                                       (a join exists)
#   A4  for every k: NOT (J subset of S(k))                  (UNOWNED)
#
#   Then no check confined to a single S(k) can decide the property on J.
#
# The inference in that last line is immediate once A1-A4 are written down.
# That is the result of attempting step 1 rather than a defect of it: the
# difficulty is not in the inference, it is in A4 being CHECKABLE AT ALL,
# which requires every S(k) to be declared. Nothing in the failures the
# order lists declares S(k) anywhere. See CLAIM_TABLE UJ_002.
#
# Two coverage states are kept apart, because merging them loses the
# distinction the order's face 3 turns on:
#   UNOWNED_BY_UNION  the union of scopes covers J, no single scope does
#                     -- every part is visible to somebody, the relation to
#                     nobody
#   UNOWNED           some observable in J lies in no scope at all
#
# NOT A TERM. "unowned join" is the order's own descriptive phrase (its
# title). It is used here as a description. Nothing here coins a term for
# the structure; coin() refuses. [CHOICE 3]
#
# CONSTRUCTED. Every structure this module is run on is a declared reading,
# not a measurement of any system.
#
# stdlib only, parses under 3.9, ASCII.

import sys
from collections import namedtuple

UNDECLARED = "UNDECLARED"

# verdicts
OWNED = "OWNED"
UNOWNED_BY_UNION = "UNOWNED_BY_UNION"
UNOWNED = "UNOWNED"
LOCAL_FAULT = "LOCAL_FAULT"
NOT_EVALUABLE = "NOT_EVALUABLE"

VERDICTS = (OWNED, UNOWNED_BY_UNION, UNOWNED, LOCAL_FAULT, NOT_EVALUABLE)

CHOICES = {
    1: "a join is OWNED only when a SINGLE scope covers it; coverage by the "
       "union of scopes is its own state (UNOWNED_BY_UNION), not ownership.",
    2: "a component whose scope is UNDECLARED makes the structure "
       "NOT_EVALUABLE. An undeclared scope is not an empty scope, and "
       "reading it as one would report the shape from a silence.",
    3: "the phrase 'unowned join' is the order's own and is used as a "
       "description. No term is coined here; coin() raises.",
    4: "LOCAL_FAULT pre-empts the two unowned verdicts, so a structure can "
       "be both locally faulty and carry an unowned join and the verdict "
       "names only the first. The coverage figure is reported regardless, "
       "so the second is not lost.",
}


class TermCoinageRefused(Exception):
    pass


def coin(*_a, **_k):
    """The order: 'NOT COINED HERE.' This is that instruction as code."""
    raise TermCoinageRefused(
        "WO-4 registers the term gap and does not coin. See WORK_ORDER.md, "
        "section TERM GAP."
    )


Component = namedtuple("Component", "cid scope locally_correct")
Structure = namedtuple("Structure", "sid components join basis")


def component(cid, scope, locally_correct=True):
    """scope: an iterable of observable ids, or the UNDECLARED sentinel.

    locally_correct: True, False, or UNDECLARED.
    """
    if scope == UNDECLARED:
        sc = UNDECLARED
    else:
        sc = frozenset(scope)
        if not sc:
            raise ValueError(
                "%s: an empty declared scope and an undeclared scope are "
                "different states; pass UNDECLARED for the second" % cid
            )
    if locally_correct not in (True, False, UNDECLARED):
        raise ValueError("%s: locally_correct must be True/False/UNDECLARED"
                         % cid)
    return Component(cid, sc, locally_correct)


def structure(sid, components, join, basis):
    if len(components) < 2:
        raise ValueError("%s: A1 requires at least two components" % sid)
    if not basis:
        raise ValueError("%s: a structure with no stated basis is a guess"
                         % sid)
    return Structure(sid, tuple(components), frozenset(join), basis)


def join_coverage(scopes, join):
    """Fraction of the join's observables lying in the union of the scopes.

    Returns None for an empty join and for a scope set carrying an
    UNDECLARED member -- neither is a coverage of zero. A zero here is a
    measurement: the join is declared, every scope is declared, and no
    scope reaches any part of it.
    """
    j = frozenset(join)
    if not j:
        return None
    union = set()
    for s in scopes:
        if s == UNDECLARED:
            return None
        union |= set(s)
    return len(union & j) / float(len(j))


def verdict(st):
    """The A1-A4 test. Returns a member of VERDICTS."""
    # [CHOICE 2] an undeclared scope is not an empty scope
    if any(c.scope == UNDECLARED or c.locally_correct == UNDECLARED
           for c in st.components):
        return NOT_EVALUABLE
    if not st.join:
        return NOT_EVALUABLE
    if any(c.locally_correct is False for c in st.components):
        return LOCAL_FAULT  # [CHOICE 4] pre-empts the unowned verdicts
    for c in st.components:
        if st.join <= c.scope:
            return OWNED  # [CHOICE 1] a SINGLE scope, never the union
    cov = join_coverage([c.scope for c in st.components], st.join)
    if cov is not None and cov >= 1.0:
        return UNOWNED_BY_UNION
    return UNOWNED


def shape_holds(st):
    """A1-A4 all satisfied. True only on the two unowned verdicts."""
    return verdict(st) in (UNOWNED, UNOWNED_BY_UNION)


def locally_detectable(st):
    """Can any check confined to one component's scope decide the join?

    None when the structure is not evaluable -- an unanswered question is
    not a negative answer.
    """
    v = verdict(st)
    if v == NOT_EVALUABLE:
        return None
    return v == OWNED


def owner(st):
    """The component whose scope covers the join, or None."""
    if verdict(st) != OWNED:
        return None
    for c in st.components:
        if st.join <= c.scope:
            return c.cid
    return None


def uncovered(st):
    """Join observables lying in no declared scope. None if not evaluable."""
    if any(c.scope == UNDECLARED for c in st.components):
        return None
    union = set()
    for c in st.components:
        union |= set(c.scope)
    return tuple(sorted(st.join - union))


def report(st):
    v = verdict(st)
    return {
        "sid": st.sid,
        "verdict": v,
        "shape_holds": shape_holds(st),
        "locally_detectable": locally_detectable(st),
        "owner": owner(st),
        "coverage": join_coverage([c.scope for c in st.components], st.join),
        "uncovered": uncovered(st),
        "n_components": len(st.components),
        "basis": st.basis,
    }


# --- constructed structures exercising every verdict -------------------

def _controls():
    """One declared structure per verdict. CONSTRUCTED, for reachability."""
    out = []
    out.append(structure(
        "ctl_owned",
        [component("a", ["x", "y"]), component("b", ["y"])],
        ["x", "y"],
        "constructed: one scope covers the join, so the shape does not hold",
    ))
    out.append(structure(
        "ctl_union",
        [component("a", ["x"]), component("b", ["y"])],
        ["x", "y"],
        "constructed: every part visible to somebody, the relation to nobody",
    ))
    out.append(structure(
        "ctl_unowned",
        [component("a", ["x"]), component("b", ["w"])],
        ["x", "y"],
        "constructed: y lies in no declared scope",
    ))
    out.append(structure(
        "ctl_local_fault",
        [component("a", ["x"], False), component("b", ["y"])],
        ["x", "y"],
        "constructed: a component is not locally correct, so A2 fails and "
        "the failure is attributable inside one scope",
    ))
    out.append(structure(
        "ctl_undeclared",
        [component("a", UNDECLARED), component("b", ["y"])],
        ["x", "y"],
        "constructed: a scope is undeclared, so A4 is not checkable",
    ))
    return out


def controls():
    return _controls()


def _fmt(v):
    return "--" if v is None else str(v)


def render():
    lines = []
    lines.append("UNOWNED JOIN -- the invariant as a checkable predicate")
    lines.append("")
    lines.append("A1 n >= 2   A2 each component correct within its declared")
    lines.append("scope   A3 the join is non-empty   A4 no single scope")
    lines.append("covers the join. A1-A4 => no check confined to one scope")
    lines.append("can decide the join.")
    lines.append("")
    lines.append("CONSTRUCTED. Every row below is a declared structure.")
    lines.append("")
    lines.append("%-18s %-17s %-6s %-9s %s"
                 % ("structure", "verdict", "cover", "local?", "owner"))
    for st in _controls():
        r = report(st)
        cov = "--" if r["coverage"] is None else "%.2f" % r["coverage"]
        lines.append("%-18s %-17s %-6s %-9s %s"
                     % (r["sid"], r["verdict"], cov,
                        _fmt(r["locally_detectable"]), _fmt(r["owner"])))
    lines.append("")
    seen = sorted(set(verdict(st) for st in _controls()))
    lines.append("verdicts reached by the controls: %d of %d"
                 % (len(seen), len(VERDICTS)))
    lines.append("")
    lines.append("no term is coined here; coin() raises. [CHOICE 3]")
    return "\n".join(lines) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "invariant is a library and a render; the checks live in "
            "unowned-join/test_unowned.py -- run "
            "python3 unowned-join/test_unowned.py\n")
        return 2
    if "--choices" in argv:
        for n in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (n, CHOICES[n]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
