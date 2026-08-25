#!/usr/bin/env python3
"""The shadow read of METHOD_SPEC.md section 4, made decidable.

Section 4 says:

    the shape is not pointed at directly. It is described by the GAPS IT
    CASTS. Each statement is one gap. The object is what they are all
    tangent to.

and gives a completion condition:

    the shadow read is complete when the gaps constrain the object to one
    form. Until then it is under-outlined, and that is a stated state,
    not a failure.

The metaphor is exact enough to compute with, and doing so supplies the
two things the prose lacks.

    A tangent line to a convex body is a SUPPORTING HALF-PLANE. Statement
    i says: the object does not extend past distance h_i in direction
    u_i, i.e. x . u_i <= h_i. "What they are all tangent to" is then the
    intersection of those half-planes -- and for a convex body the
    intersection over all directions recovers it exactly (Minkowski).

What the prose lacks, and what falls out:

    1. A FAILURE MODE. Section 4 offers one reading of statements that
       appear to conflict: "separate tangents to one boundary, not
       competing claims." But a set of half-planes can have EMPTY
       intersection, and then there is no boundary they are tangent to
       and the statements really are inconsistent. Section 4 has no cell
       for that state, so every apparent conflict routes to the
       reassuring reading. Decidable here.

    2. A COMPLETION NUMBER. "Constrain the object to one form" is the
       intersection being bounded, and how far from complete is its AREA.
       Under-outlined stops being a stated state and becomes a measured
       one.

And one limitation the formalisation makes visible rather than creates:

    3. TANGENTS RECOVER ONLY A CONVEX HULL. No number of supporting
       half-planes distinguishes a non-convex body from its hull. So if
       the object is non-convex, section 4's completion condition can
       NEVER be met -- not for want of statements, by construction. That
       is a property of the read path, and it is worth knowing before
       anyone concludes that an outline which will not close means the
       reader has not said enough.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.

    python3 shadow_read.py
    python3 shadow_read.py --selftest
"""

import itertools
import math
import sys

TOL = 1e-9

INCONSISTENT = "INCONSISTENT"
UNDER_OUTLINED = "UNDER_OUTLINED"
OUTLINED = "OUTLINED"


class Gap(object):
    """One statement. A supporting half-plane x . u <= h.

    `u` is a direction, normalised on construction. `h` is how far the
    object is permitted to extend that way. `said` is the statement the
    gap came from, carried so a result can be traced to a sentence.
    """

    def __init__(self, ux, uy, h, said=""):
        n = math.hypot(ux, uy)
        if n < TOL:
            raise ValueError("a gap needs a direction; got the zero vector")
        self.ux, self.uy, self.h = ux / n, uy / n, h / n
        self.said = said

    def holds(self, p, tol=1e-7):
        return self.ux * p[0] + self.uy * p[1] <= self.h + tol

    def __repr__(self):
        return "Gap(%.3f, %.3f, %.3f)" % (self.ux, self.uy, self.h)


def _corner(a, b):
    """Where two gap boundaries meet, or None if parallel."""
    det = a.ux * b.uy - a.uy * b.ux
    if abs(det) < TOL:
        return None
    return ((a.h * b.uy - a.uy * b.h) / det,
            (a.ux * b.h - a.h * b.ux) / det)


def _hull(pts):
    """Andrew monotone chain. Returns the hull counter-clockwise."""
    pts = sorted(set((round(x, 9), round(y, 9)) for x, y in pts))
    if len(pts) < 3:
        return pts

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2:
                (x1, y1), (x2, y2) = out[-2], out[-1]
                if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) > TOL:
                    break
                out.pop()
            out.append(p)
        return out

    return half(pts)[:-1] + half(reversed(pts))[:-1]


def _area(poly):
    if len(poly) < 3:
        return 0.0
    s = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def _positively_spans(gaps):
    """Do the gap directions positively span the plane?

    If they do not, some direction is unconstrained and the intersection
    runs to infinity there. Checked independently of the vertex
    enumeration so the two can be asserted to agree.
    """
    angs = sorted(math.atan2(g.uy, g.ux) for g in gaps)
    if len(angs) < 3:
        return False
    for i in range(len(angs)):
        nxt = angs[(i + 1) % len(angs)]
        gap = nxt - angs[i]
        if i == len(angs) - 1:
            gap += 2 * math.pi
        if gap >= math.pi - 1e-12:
            return False
    return True


def outline(gaps, box=1e6):
    """Read a set of gaps. Returns state, vertices, area, and why.

    A bounding box is added so that an unbounded intersection still has
    vertices to find; a vertex sitting on the box is how unboundedness is
    detected, and it is cross-checked against the spanning test.
    """
    if not gaps:
        return {"state": UNDER_OUTLINED, "vertices": [], "area": None,
                "why": "no statements", "n_gaps": 0}

    walls = [Gap(1, 0, box), Gap(-1, 0, box),
             Gap(0, 1, box), Gap(0, -1, box)]
    allg = list(gaps) + walls

    verts = []
    for a, b in itertools.combinations(allg, 2):
        p = _corner(a, b)
        if p is None:
            continue
        if all(g.holds(p) for g in allg):
            verts.append(p)

    if not verts:
        return {"state": INCONSISTENT, "vertices": [], "area": None,
                "why": ("no point satisfies every statement, so there is no "
                        "boundary they are all tangent to"),
                "n_gaps": len(gaps)}

    on_box = any(max(abs(x), abs(y)) > box * 0.5 for x, y in verts)
    spans = _positively_spans(gaps)
    if on_box != (not spans):
        raise AssertionError(
            "boundedness disagrees: box-touching=%s, positively-spans=%s"
            % (on_box, spans))

    if on_box:
        return {"state": UNDER_OUTLINED, "vertices": [], "area": None,
                "why": ("the statements leave at least one direction "
                        "unconstrained; the outline runs to infinity there"),
                "n_gaps": len(gaps)}

    poly = _hull(verts)
    return {"state": OUTLINED, "vertices": poly, "area": _area(poly),
            "why": "bounded on every side; the area is what is still open",
            "n_gaps": len(gaps)}


def outline_area(name):
    """Metric. Float area when OUTLINED, else the state name.

    Registered in tools/known_answer.py -- the standing step is that no
    metric ships without a case whose answer was fixed in advance.
    """
    r = outline(FIXTURES[name]())
    return r["area"] if r["state"] == OUTLINED else r["state"]


# --------------------------------------------------------------------------
# Fixtures whose answers are known before the code runs.
# --------------------------------------------------------------------------

def _square():
    """Four tangents at distance 1. A 2x2 square: area exactly 4."""
    return [Gap(1, 0, 1, "does not extend right past 1"),
            Gap(-1, 0, 1, "does not extend left past 1"),
            Gap(0, 1, 1, "does not extend up past 1"),
            Gap(0, -1, 1, "does not extend down past 1")]


def _hexagon():
    """Six tangents at distance 1 about a unit circle.

    A regular hexagon circumscribing the unit circle: area 2*sqrt(3).
    """
    return [Gap(math.cos(k * math.pi / 3), math.sin(k * math.pi / 3), 1,
                "tangent %d" % k) for k in range(6)]


def _strip():
    """Two opposing statements only. Unbounded up and down."""
    return [Gap(1, 0, 1, "not right of 1"), Gap(-1, 0, 1, "not left of -1")]


def _contradiction():
    """x <= 0 and x >= 1. No object is tangent to both."""
    return [Gap(1, 0, 0, "does not extend right past 0"),
            Gap(-1, 0, -1, "extends at least to 1"),
            Gap(0, 1, 1, "not above 1"), Gap(0, -1, 1, "not below -1")]


def _one_statement():
    return [Gap(1, 0, 1, "a single tangent")]


FIXTURES = {
    "square": _square,
    "hexagon": _hexagon,
    "strip": _strip,
    "contradiction": _contradiction,
    "one_statement": _one_statement,
}

KNOWN = {
    "square": 4.0,
    "hexagon": 2.0 * math.sqrt(3.0),
    "strip": UNDER_OUTLINED,
    "contradiction": INCONSISTENT,
    "one_statement": UNDER_OUTLINED,
}


def convexity_note():
    """Point 3: tangents recover a hull, so a non-convex object never closes.

    Demonstrated rather than asserted: an L-shape and its convex hull cast
    identical gaps in every direction, so no set of statements separates
    them.
    """
    ell = [(0, 0), (2, 0), (2, 1), (1, 1), (1, 2), (0, 2)]
    hull = _hull(ell)
    same = []
    for k in range(72):
        a = k * math.pi / 36.0
        ux, uy = math.cos(a), math.sin(a)
        s_ell = max(x * ux + y * uy for x, y in ell)
        s_hull = max(x * ux + y * uy for x, y in hull)
        same.append(abs(s_ell - s_hull) < 1e-12)
    return {"directions": len(same), "identical": sum(same),
            "area_ell": 3.0, "area_hull": _area(hull)}


def report():
    print("THE SHADOW READ, MADE DECIDABLE")
    print("METHOD_SPEC.md section 4. The spec is not modified.\n")
    print("%-16s %-16s %-12s %s" % ("statements", "state", "area", "known"))
    print("-" * 66)
    for name in ("square", "hexagon", "strip", "contradiction",
                 "one_statement"):
        r = outline(FIXTURES[name]())
        area = "%.6f" % r["area"] if r["area"] is not None else "--"
        k = KNOWN[name]
        kk = "%.6f" % k if isinstance(k, float) else k
        print("%-16s %-16s %-12s %s" % (name, r["state"], area, kk))
    print()
    print("Section 4 names ONE of these three states. It offers")
    print("UNDER_OUTLINED, and reads apparent conflict as 'separate")
    print("tangents to one boundary, not competing claims'. But")
    print("INCONSISTENT is reachable and is what a genuine conflict looks")
    print("like: no point satisfies every statement, so there is no")
    print("boundary they are all tangent to. Without that state every")
    print("apparent conflict routes to the reassuring reading.")
    print()
    print("And OUTLINED carries a NUMBER. 'Complete when the gaps")
    print("constrain the object to one form' is the area going to zero;")
    print("until then the area is how much is still open. Under-outlined")
    print("stops being a stated state and becomes a measured one.")
    print()
    c = convexity_note()
    print("THE LIMIT THE FORMALISATION MAKES VISIBLE")
    print("  an L-shape and its convex hull, support value compared in")
    print("  %d directions: identical in %d of %d"
          % (c["directions"], c["identical"], c["directions"]))
    print("  true area %.1f vs hull area %.1f" % (c["area_ell"],
                                                  c["area_hull"]))
    print("  Tangents recover a convex hull and nothing finer. If the")
    print("  object is non-convex, section 4's completion condition can")
    print("  NEVER be met -- not for want of statements, by construction.")
    print("  Worth knowing before an outline that will not close is read")
    print("  as the reader not having said enough.")
    print()


def selftest():
    fails = []
    for name, expect in KNOWN.items():
        got = outline_area(name)
        if isinstance(expect, float):
            if not isinstance(got, float) or abs(got - expect) > 1e-6:
                fails.append("%s: expected %.6f, got %r" % (name, expect, got))
        elif got != expect:
            fails.append("%s: expected %s, got %r" % (name, expect, got))

    # The failure mode section 4 lacks must be REACHABLE, or this module
    # is CONSTANT_SILENT on the only state it adds.
    states = set(outline(f())["state"] for f in FIXTURES.values())
    for s in (OUTLINED, UNDER_OUTLINED, INCONSISTENT):
        if s not in states:
            fails.append("state %s is unreachable in the fixtures" % s)

    # Adding a statement must never widen the outline.
    a = outline(_square())["area"]
    b = outline(_square() + [Gap(1, 1, 1.0, "a further gap")])["area"]
    if not (b <= a + 1e-9):
        fails.append("a further statement widened the outline: %.6f -> %.6f"
                     % (a, b))

    # The convexity limit must hold in every direction, or point 3 is wrong.
    c = convexity_note()
    if c["identical"] != c["directions"]:
        fails.append("an L-shape and its hull differ in %d directions; the "
                     "convex-hull limit must be restated"
                     % (c["directions"] - c["identical"]))

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
