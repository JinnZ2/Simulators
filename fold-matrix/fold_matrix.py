#!/usr/bin/env python3
"""
fold_matrix -- work order 8. One term, one grid, not one number.

WHAT THIS EXTENDS AND WHAT WAS HERE. The order opens "Extends: folded-term
instrument. The downward arm already has a reading." There is no folded-term
instrument in this repository and no downward reading in it: `severed`,
`still_acting` and `deepest still-acting term` return nothing anywhere in
the tree. Seventh instance of the stated-thing-with-no-artifact shape
(MF_017 / CW_015 / DL_004 / GC_012 / UNI_013 / SSS_050), and the largest,
since it is the whole arm this order extends rather than one field.

So the grid holds both arms and the downward cells are filled only where
today's material fills them. Nothing is reconstructed: a level with no
reading emits ABSENT, never a plausible one. That is the PB_001 / CW_004
rule, and the one prior reconstruction in this repository is what it cost.

THE GRID (S1). Rows are levels indexed from the term outward -- negative
toward substrate, zero the term as used, positive toward the stated
purpose. Columns are severed / still_acting / clock / basis at every
level, and upward levels add `value_string`, the sign and magnitude of
the claimed relation between proxy and goal.

ABSENCE IS FIRST-CLASS (S7). Empty value_string, UNREAD, ABSENT and
NOT_EVALUABLE all emit as themselves. Nothing here defaults to a number,
and NOT_EVALUABLE is structurally unrankable rather than conventionally
so: score() raises on it.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, os.pardir, "sheet-structure-scan"))
import no_severity                                        # noqa: E402

TERMS = os.path.join(_HERE, "terms")

# ---- S1 / S2 vocabularies --------------------------------------------

MEASURED = "measured"
DERIVED = "derived"
ASSERTED = "ASSERTED"
ABSENT = "ABSENT"
BASIS = (MEASURED, DERIVED, ASSERTED, ABSENT)

# S2 (revised). value_string is a fixed format, not a free string: three
# fields, each independently ABSENT-able. The split is load-bearing --
# under the free-text version every upward cell in this folder read
# "empty", and a purpose claim usually states a DIRECTION and no size,
# which one string cannot record and three fields can.
VS_FIELDS = ("sign", "magnitude", "unit")
SIGNS = ("+", "-", ABSENT)

# FM_016 fix. How the downward level set was enumerated. Declared per
# term, never inferred -- the same refusal as FM_013 on `computed`: a
# grid loaded without this field DECLARES UNREAD, it does not get one
# assigned from how good the levels look.
DOCUMENT_NAMED = "document_named"
PHYSICAL_TRACED = "physical_traced"
AUTHOR_READ = "author_read"
ENUMERATION_BASES = (DOCUMENT_NAMED, PHYSICAL_TRACED, AUTHOR_READ, "UNREAD")

# S1a. Never merged into basis.
YES, NO, UNREAD_STATE = "yes", "no", "UNREAD"
PLAN_STATES = (YES, NO, UNREAD_STATE)

ENUMERATED = "enumerated"
PARTIAL = "PARTIAL"
UNREAD = "UNREAD"
FUNCTION_SET = (ENUMERATED, PARTIAL, UNREAD)

NOT_EVALUABLE = "NOT_EVALUABLE"
EVALUABLE = "EVALUABLE"


class NotEvaluable(Exception):
    """Raised by score(). S3 says do not score it, do not rank it, do not
    carry it into a comparison -- so the refusal is a control-flow fact
    rather than a convention a caller can forget."""


# ---- S3. The scope field ---------------------------------------------

# The three fields S3 requires. `boundary` and `horizon` are two of
# declared-frame's three CORE fields, and they are IMPORTED from it
# rather than retyped, so the two folders cannot drift about what a
# frame's core is. `with_respect_to` is S3's addition: declared-frame
# asks what is inside the accounting, S3 asks what the ratio is taken
# against, and those are different questions.
def _declared_frame_core():
    path = os.path.join(_HERE, os.pardir, "declared-frame", "v2",
                        "check_frame.py")
    try:
        src = open(path).read()
    except IOError:
        return None
    m = re.search(r"^CORE\s*=\s*\[([^\]]*)\]", src, re.M)
    if not m:
        return None
    return tuple(x.strip().strip("\"'") for x in m.group(1).split(",")
                 if x.strip())


_CORE = _declared_frame_core()
SCOPE_FIELDS = ("with_respect_to", "boundary", "horizon")

# Words that make a term efficiency-class and therefore require a scope.
EFFICIENCY_CLASS = ("efficient", "efficiency", "optimal", "optimum",
                    "optimize", "optimization", "optimised",
                    "better", "best", "faster", "fastest",
                    "improve", "improvement", "improved")

# S4. Names that assert a direction. A superset of the class above --
# every efficiency word carries a sign, and so do these, which do not
# trigger the scope requirement on their own.
SIGN_ASSERTING = EFFICIENCY_CLASS + (
    "waste", "wasteful", "loss", "losses", "lossy", "gain", "gains",
    "degradation", "degraded", "penalty", "benefit", "benefits",
    "savings", "overhead", "burden", "leakage", "shortfall", "surplus")

_WORD = {w: re.compile(r"\b%s\b" % re.escape(w), re.I)
         for w in set(SIGN_ASSERTING)}


def efficiency_class(name):
    """The efficiency words present in a term's name, in order."""
    return [w for w in EFFICIENCY_CLASS if _WORD[w].search(name or "")]


def sign_asserting(name):
    """S4. Every direction-asserting word in a name."""
    return [w for w in SIGN_ASSERTING if _WORD[w].search(name or "")]


def scope_check(term):
    """(verdict, missing, why). S3.

    NOT_EVALUABLE is returned for a MISSING field, and a field present
    but explicitly unknown is also missing -- `horizon: "unknown"` is an
    honest declaration and it still does not let a ratio be compared.
    The two are reported apart, because they call for different next
    steps: one is an omission, the other is a measurement nobody has.
    """
    words = efficiency_class(term.get("name", ""))
    if not words:
        return EVALUABLE, [], "not an efficiency-class term; no scope required"
    scope = term.get("scope") or {}
    absent, declared_unknown = [], []
    for f in SCOPE_FIELDS:
        v = scope.get(f)
        if v is None or not str(v).strip():
            absent.append(f)
        elif str(v).strip().lower() in ("unknown", "not stated", "unstated"):
            declared_unknown.append(f)
    missing = absent + declared_unknown
    if missing:
        return (NOT_EVALUABLE, missing,
                "efficiency-class on %s; scope missing: %s%s"
                % (", ".join(words),
                   ", ".join(absent) if absent else "-",
                   ("; declared unknown: " + ", ".join(declared_unknown))
                   if declared_unknown else ""))
    return EVALUABLE, [], "efficiency-class on %s; scope complete" \
        % ", ".join(words)


def replacement_check(term):
    """(verdict, why). S3's additional requirement.

    A replacement claim against an UNREAD function set is NOT_EVALUABLE,
    which S3 is explicit is not the same as unsupported: unsupported says
    the comparison was made and failed, and this says the baseline was
    never read, so no comparison was made at all.
    """
    rep = term.get("replacement")
    if not rep:
        return EVALUABLE, "not a replacement claim"
    fs = rep.get("Y_function_set")
    if fs not in FUNCTION_SET:
        return (NOT_EVALUABLE,
                "replacement claim with no Y_function_set declared; the "
                "field is required and takes %s" % (" | ".join(FUNCTION_SET)))
    if fs == UNREAD:
        return (NOT_EVALUABLE,
                "the comparison is against an unread baseline: %s. This is "
                "refused, not scored -- nothing was compared."
                % rep.get("Y", "Y"))
    if fs == PARTIAL:
        return (NOT_EVALUABLE,
                "Y_function_set is PARTIAL: %d of an unknown total "
                "enumerated, so the remainder is not bounded"
                % len(rep.get("Y_functions") or []))
    return EVALUABLE, "Y_function_set enumerated: %d function(s)" \
        % len(rep.get("Y_functions") or [])


# ---- S5. Clocks per level --------------------------------------------

def clock_of(level):
    """(value, units, basis) or None. A level with no clock has none;
    that is not a zero and not an inherited one."""
    c = level.get("clock")
    if not c:
        return None
    if c.get("value") is None:
        return None
    return (c.get("value"), c.get("units"), c.get("basis", ""))


def clock_mismatch(levels):
    """S5. Every clock, per level, never collapsed.

    Returns the distinct (value, units) pairs and whether they disagree.
    No pick is made and no reconciliation is attempted: a term whose
    levels disagree on horizon is the finding, so collapsing them would
    delete it.

    A DERIVED clock does not count toward the disagreement. S5 says "time
    constant ASSUMED at this level", and a level whose clock is computed
    from another level's is not a second assumption -- it is the first
    one carried forward. The H1 fixture produced this: level -1 assumes
    3.0 years and level 0 derives 3.403 from it by dividing by a measured
    coupling, and a naive distinct-count reads that as two horizons in
    conflict. It is one horizon and its own derivative.

    Derived clocks are still EMITTED, with what they were derived from.
    Only the disagreement count excludes them, so nothing is hidden.
    """
    seen = []
    for lv in levels:
        c = clock_of(lv)
        if c is None:
            continue
        cl = lv.get("clock") or {}
        seen.append({"index": lv["index"], "value": c[0], "units": c[1],
                     "basis": c[2],
                     "derived_from": cl.get("derived_from")})
    indep = [x for x in seen if x["derived_from"] is None]
    pairs = set((x["value"], x["units"]) for x in indep)
    return {"clocks": seen, "independent": len(indep),
            "derived": len(seen) - len(indep),
            "distinct": len(pairs),
            "mismatch": len(pairs) > 1,
            "collapsed": None}


# ---- S2. Upward cells -------------------------------------------------

def value_string(cell):
    """The fixed S2 triple, normalised. Missing fields read ABSENT.

    Each field is independent: a claim that states a direction and no
    size is `+ / ABSENT / ABSENT`, and that is the ordinary shape of a
    purpose claim. A magnitude of ABSENT is never rendered as 0 and a
    magnitude of 0 is a stated size, so the two never collide.
    """
    vs = cell.get("value_string")
    if isinstance(vs, str):
        # The v1 free-text form. Refused rather than coerced: an empty
        # string is not the same as three ABSENTs -- it is one field that
        # cannot say which of the three is missing -- and silently
        # widening it would delete the distinction the revision adds.
        raise ValueError(
            "value_string is a free string; the revised S2 takes three "
            "fields (sign, magnitude, unit), each independently "
            "ABSENT-able. An empty string cannot say which is missing.")
    vs = vs or {}
    out = {}
    for f in VS_FIELDS:
        v = vs.get(f, ABSENT)
        if v is None or (isinstance(v, str) and not v.strip()):
            v = ABSENT
        out[f] = v
    return out


def vs_render(vs):
    """One display string, with each field visible as itself."""
    return "%s / %s / %s" % (
        vs["sign"],
        vs["magnitude"] if vs["magnitude"] != ABSENT else ABSENT,
        vs["unit"])


def upward_cells(term):
    """Every positive level, with its basis and value_string triple.

    The triple is REQUIRED per S2 and all-ABSENT is the normal result. No
    field is ever rendered as 0, so a stated relation of zero and a
    relation nobody stated never collide.
    """
    out = []
    for lv in term.get("levels", []):
        if lv["index"] <= 0:
            continue
        b = lv.get("basis", ABSENT)
        vs = value_string(lv)
        out.append({
            "index": lv["index"],
            "goal": lv.get("goal", ""),
            "relation_claimed": lv.get("severed", ""),
            "basis": b,
            "value_string": vs,
            "vs_all_absent": all(vs[f] == ABSENT for f in VS_FIELDS),
            "cite": lv.get("cite", ""),
            # An empty value_string has more than one cause and the
            # order's four basis values do not separate them: nobody
            # stated a relation, and the source stated a goal and
            # explicitly declined to claim a relation, both land on
            # empty. Carried as its own field rather than folded in.
            "source_disclaims": lv.get("source_disclaims", ""),
        })
    return out


def upward_tally(terms):
    """P1 and P2 from PREDICTIONS_WO8.md, computed.

    Scope-refused terms are excluded: S3 says do not carry them into a
    comparison, and a tally is a comparison.
    """
    counts = dict((b, 0) for b in BASIS)
    field_absent = dict((f, 0) for f in VS_FIELDS)
    n_empty = n_cells = n_split = 0
    excluded = []
    for t in terms:
        sv, _m, _w = scope_check(t)
        rv, _w2 = replacement_check(t)
        if NOT_EVALUABLE in (sv, rv):
            excluded.append(t.get("id", "?"))
            continue
        for c in upward_cells(t):
            n_cells += 1
            counts[c["basis"]] = counts.get(c["basis"], 0) + 1
            vs = c["value_string"]
            for f in VS_FIELDS:
                if vs[f] == ABSENT:
                    field_absent[f] += 1
            if c["vs_all_absent"]:
                n_empty += 1
            elif any(vs[f] != ABSENT for f in VS_FIELDS):
                # A cell where the three fields do NOT fail together --
                # the state the free-text format could not record.
                n_split += 1
    soft = counts[ASSERTED] + counts[ABSENT]
    hard = counts[MEASURED] + counts[DERIVED]
    return {"counts": counts, "cells": n_cells,
            "all_absent_cells": n_empty, "split_cells": n_split,
            "field_absent": field_absent,
            "asserted_plus_absent": soft, "measured_plus_derived": hard,
            "P1_majority": (soft > hard) if n_cells else None,
            "P3_at_least_one_split": (n_split > 0) if n_cells else None,
            "P4_no_magnitude": (field_absent["magnitude"] == n_cells)
            if n_cells else None,
            "excluded_not_evaluable": excluded}


# ---- S1a. Stop rules, from the document set --------------------------

def upward_stop(term):
    """Highest positive level carrying a stated artifact.

    S1a: the stop is a property of the DOCUMENT SET, not an absolute. A
    level whose goal nobody wrote down anywhere is where the arm ends,
    and it ends at basis ABSENT rather than at a guess about what the
    organisation must have meant.
    """
    best = None
    for lv in term.get("levels", []):
        if lv["index"] <= 0:
            continue
        aid = (lv.get("artifact_id") or "").strip()
        if aid:
            if best is None or lv["index"] > best["index"]:
                best = {"index": lv["index"], "artifact_id": aid,
                        "basis": lv.get("basis")}
    if best is None:
        return {"index": None, "artifact_id": ABSENT, "basis": ABSENT,
                "why": "no positive level carries a stated artifact, so "
                       "the upward arm stops before it starts"}
    above = [lv for lv in term.get("levels", [])
             if lv["index"] > best["index"]]
    return dict(best, why=("highest level with a stated artifact; %d "
                           "level(s) above it carry none"
                           % len(above)) if above else
                "highest level with a stated artifact")


def downward_stop(term):
    """Deepest level carrying a quantity the organisation COMPUTES.

    S1a is precise about this and it is the rule most likely to be
    misread: the floor is the deepest QUANTIFIED quantity, not the
    deepest one that physically exists. Joules are not the floor unless
    joules were calculated. A level can name a real physical relation and
    still be below the stop, because nobody in the document set computed
    anything there.

    `computed` is a declared field. Nothing here infers that an
    organisation computed a quantity from the fact that the quantity
    exists -- that inference is the whole failure the rule names.
    """
    best = None
    for lv in term.get("levels", []):
        if lv["index"] > 0:
            continue
        q = lv.get("quantified")
        if not q or not q.get("computed"):
            continue
        if best is None or lv["index"] < best["index"]:
            best = {"index": lv["index"],
                    "quantity": q.get("quantity", ABSENT),
                    "unit": q.get("unit", ABSENT),
                    "by": q.get("by", "")}
    if best is None:
        return {"index": None, "quantity": ABSENT, "unit": ABSENT,
                "by": "", "why": "no level carries a quantity the "
                                 "organisation computes"}
    return dict(best, why="deepest computed quantity")


def enumeration_basis(term):
    """How the downward level set was arrived at. Declared, never
    inferred.

    A grid with no declaration reads UNREAD. It does not get a basis
    assigned from the levels looking well traced -- that inference is
    the same failure FM_013 refuses for `computed`, and it is worse
    here, because a plausible-looking level list is exactly what an
    author produces from general knowledge without tracing anything.
    """
    b = (term.get("enumeration_basis") or "UNREAD")
    return b if b in ENUMERATION_BASES else "UNREAD"


def unmeasured_span(term):
    """Their downward stop against where the physical chain continues.

    Emitted, never scored (S1a). The emitted number is
    `unmeasured_span_min` and the name is load-bearing: it counts levels
    between the deepest computed quantity and the deepest level the
    term's own grid NAMES, so it is a FLOOR on the real span, not a
    measurement of it. A grid that stops early reports a smaller number
    than the world has.

    `unmeasured_span: 3` reads as a fact about the world.
    `unmeasured_span_min: 3` reads as a floor, which is what it is. The
    honest reading used to live in a note string where nothing
    downstream could see it -- the same shape as a workbook stating a
    relationship in prose that no cell maintains.
    """
    ds = downward_stop(term)
    downs = [lv for lv in term.get("levels", []) if lv["index"] < 0]
    if not downs:
        deepest = None
    else:
        deepest = min(lv["index"] for lv in downs)
    basis = enumeration_basis(term)
    if ds["index"] is None or deepest is None:
        return {"stop": ds["index"], "physical_floor_named": deepest,
                "unmeasured_span_min": None,
                "enumeration_basis": basis,
                "note": "not computable: %s"
                        % ("no computed quantity" if ds["index"] is None
                           else "the grid names no level below the term")}
    span = ds["index"] - deepest
    return {"stop": ds["index"], "physical_floor_named": deepest,
            "unmeasured_span_min": span,
            "enumeration_basis": basis,
            "note": ("at least %d level(s) of the physical chain continue "
                     "below the deepest quantity anyone computed. A floor: "
                     "it counts what the grid names, enumerated by %s."
                     % (span, basis))
            if span > 0 else
            "the deepest computed quantity is the deepest level named"}


def plan_column(term):
    """S1a's separate column. Never merged into basis, and the code
    cannot merge it: it is read from its own key and returned in its own
    dict, and the selftest asserts neither value reaches a basis field.
    """
    p = term.get("plan") or {}
    pe = p.get("plan_exists", UNREAD_STATE)
    pt = p.get("practice_tracks_plan", UNREAD_STATE)
    bad = [v for v in (pe, pt) if v not in PLAN_STATES]
    return {"plan_exists": pe, "practice_tracks_plan": pt,
            "invalid": bad,
            "why": p.get("why", "")}


def compare_spans(terms):
    """Cross-document comparison of unmeasured_span_min.

    The amendment: a comparison requires MATCHING enumeration basis.
    Mismatched, emit both and refuse the difference -- two floors
    counted by different procedures are not two measurements of one
    quantity, and subtracting them produces a number about the two
    procedures.

    Returns groups by basis and a refusal list. No difference is
    computed across a mismatch anywhere in this function.
    """
    rows, groups = [], {}
    for t in terms:
        sp = unmeasured_span(t)
        row = {"id": t.get("id", "?"),
               "unmeasured_span_min": sp["unmeasured_span_min"],
               "enumeration_basis": sp["enumeration_basis"]}
        rows.append(row)
        if row["unmeasured_span_min"] is not None:
            groups.setdefault(row["enumeration_basis"], []).append(row)
    comparable, refused = [], []
    for b, g in sorted(groups.items()):
        if b == "UNREAD":
            refused.append((b, [r["id"] for r in g],
                            "basis UNREAD: the level set was not declared, "
                            "so nothing is known about what it counts"))
        elif len(g) >= 2:
            comparable.append((b, g))
        else:
            refused.append((b, [r["id"] for r in g],
                            "only one term on this basis; nothing to "
                            "compare it against"))
    cross = [b for b in groups if b != "UNREAD"]
    if len(cross) > 1:
        refused.append(("MISMATCH", sorted(
            r["id"] for b in cross for r in groups[b]),
            "these terms were enumerated on different bases (%s); both "
            "floors are emitted and the difference is refused"
            % ", ".join(sorted(cross))))
    return {"rows": rows, "comparable": comparable, "refused": refused,
            "difference": None}


# ---- scoring, which mostly refuses ------------------------------------

def score(term):
    """There is no score. S3 forbids one for NOT_EVALUABLE terms and the
    grid is not a number for the rest, so this exists to raise rather
    than to be forgotten about."""
    sv, missing, why = scope_check(term)
    rv, why2 = replacement_check(term)
    if sv == NOT_EVALUABLE:
        raise NotEvaluable(why)
    if rv == NOT_EVALUABLE:
        raise NotEvaluable(why2)
    raise NotEvaluable(
        "S1: one term, one grid, not one number. Read the grid.")


# ---- S4. The neutral reading ------------------------------------------

def neutral_reading(term):
    """S4. The flagged name, and the measured quantity plus its frame
    emitted alongside it.

    The neutral reading is NOT computed from the name -- a name that
    asserts a sign cannot be de-signed by string surgery, and guessing
    one would be inventing a measurement. It is a declared field, and a
    term that does not carry one says so.
    """
    words = sign_asserting(term.get("name", ""))
    if not words:
        return {"flagged": [], "neutral": "", "frame": "", "state": "clean"}
    n = term.get("neutral_reading") or {}
    q, fr = n.get("quantity", ""), n.get("frame", "")
    if not q or not fr:
        return {"flagged": words, "neutral": q, "frame": fr,
                "state": "NOT_SUPPLIED"}
    return {"flagged": words, "neutral": q, "frame": fr, "state": "supplied"}


# ---- I/O --------------------------------------------------------------

def load_terms(path=TERMS):
    out = []
    if not os.path.isdir(path):
        return out
    for fn in sorted(os.listdir(path)):
        if fn.endswith(".json"):
            d = json.load(open(os.path.join(path, fn)))
            d.setdefault("id", os.path.splitext(fn)[0])
            out.append(d)
    return out


def validate(term):
    """Structural refusals, at load rather than at read."""
    bad = []
    for lv in term.get("levels", []):
        if "index" not in lv:
            bad.append("a level with no index")
        if lv.get("basis") not in BASIS:
            bad.append("level %s: basis %r not in %s"
                       % (lv.get("index"), lv.get("basis"), list(BASIS)))
        if lv.get("index", 0) > 0:
            vs = lv.get("value_string")
            if vs is None:
                bad.append("level %s: upward cell with no value_string "
                           "(S2 requires it; all-ABSENT is legal, missing "
                           "is not)" % lv.get("index"))
            elif isinstance(vs, str):
                bad.append("level %s: value_string is a free string. The "
                           "revised S2 takes three fields %s, each "
                           "independently ABSENT-able."
                           % (lv.get("index"), list(VS_FIELDS)))
            else:
                if vs.get("sign", ABSENT) not in SIGNS:
                    bad.append("level %s: sign %r not in %s"
                               % (lv.get("index"), vs.get("sign"),
                                  list(SIGNS)))
                m = vs.get("magnitude", ABSENT)
                if m != ABSENT and not isinstance(m, (int, float)):
                    bad.append("level %s: magnitude %r is neither a number "
                               "nor ABSENT" % (lv.get("index"), m))
        q = lv.get("quantified")
        if q is not None:
            if "computed" not in q:
                bad.append("level %s: quantified block with no `computed` "
                           "field. S1a's floor is the deepest quantity the "
                           "organisation COMPUTES, and whether it did is "
                           "not inferable from the quantity existing."
                           % lv.get("index"))
            elif q.get("computed") and not q.get("unit"):
                bad.append("level %s: computed quantity with no unit"
                           % lv.get("index"))
    if "enumeration_basis" in term and \
            term["enumeration_basis"] not in ENUMERATION_BASES:
        bad.append("enumeration_basis %r not in %s"
                   % (term["enumeration_basis"], list(ENUMERATION_BASES)))
    pc = plan_column(term)
    if pc["invalid"]:
        bad.append("plan column: %s not in %s"
                   % (pc["invalid"], list(PLAN_STATES)))
    rep = term.get("replacement")
    if rep and rep.get("Y_function_set") not in FUNCTION_SET:
        bad.append("replacement claim: Y_function_set %r not in %s"
                   % (rep.get("Y_function_set"), list(FUNCTION_SET)))
    return bad


# ---- render -----------------------------------------------------------

def table(head, rows):
    cols = [len(str(h)) for h in head]
    for r in rows:
        for i, c in enumerate(r):
            cols[i] = max(cols[i], len(str(c)))
    out = ["  ".join(str(h).ljust(cols[i]) for i, h in enumerate(head)),
           "  ".join("-" * c for c in cols)]
    for r in rows:
        out.append("  ".join(str(c).ljust(cols[i]) for i, c in enumerate(r)))
    return "\n".join(out)


def _clip(s, n):
    s = "" if s is None else str(s)
    return s if len(s) <= n else s[:n - 1] + "…"


def render_term(term, width=44):
    L = ["term   %s" % term.get("id"),
         "name   %s" % term.get("name", ""),
         "source %s" % term.get("source", "not stated"),
         ""]

    sv, missing, why = scope_check(term)
    rv, why2 = replacement_check(term)
    L += ["S3 scope        %s -- %s" % (sv, why)]
    if term.get("replacement"):
        L += ["S3 replacement  %s -- %s" % (rv, why2)]
    if NOT_EVALUABLE in (sv, rv):
        L += ["",
              "This term is NOT_EVALUABLE. It is not scored, not ranked,",
              "and not carried into any comparison (S3). That is a refusal",
              "about what can be read from it, and is not a low reading."]

    nr = neutral_reading(term)
    if nr["flagged"]:
        L += ["", "S4 sign hygiene: the name asserts a direction (%s)"
              % ", ".join(nr["flagged"])]
        if nr["state"] == "supplied":
            L += ["   neutral quantity: %s" % nr["neutral"],
                  "   frame:            %s" % nr["frame"]]
        else:
            L += ["   neutral reading NOT_SUPPLIED. It is a declared field,",
                  "   not something a name can be de-signed into."]

    lv = sorted(term.get("levels", []), key=lambda x: x["index"])
    if lv:
        L += ["", "S1 grid"]
        L.append(table(
            ["level", "severed", "still_acting", "clock", "basis"],
            [[("%+d" % x["index"]) if x["index"] else " 0",
              _clip(x.get("severed"), width),
              _clip(x.get("still_acting"), width),
              ("%s %s" % (x["clock"]["value"], x["clock"].get("units", "")))
              if clock_of(x) else _clip(
                  (x.get("clock") or {}).get("state", "-"), 18),
              x.get("basis")] for x in lv]))

    up = upward_cells(term)
    if up:
        L += ["", "S2 upward cells"]
        L.append(table(
            ["level", "goal", "basis", "sign", "magnitude", "unit", "cite"],
            [[("%+d" % c["index"]), _clip(c["goal"], width), c["basis"],
              c["value_string"]["sign"],
              c["value_string"]["magnitude"],
              _clip(c["value_string"]["unit"], 22),
              _clip(c["cite"], 24)] for c in up]))
        split = [c for c in up if not c["vs_all_absent"]]
        if split:
            L += ["",
                  "   The three fields do not fail together on %d cell(s)."
                  % len(split),
                  "   A stated direction with no size is the ordinary shape",
                  "   of a purpose claim, and one free-text field recorded",
                  "   it as identical to a cell nobody wrote anything in."]
        dis = [c for c in up if c["source_disclaims"]]
        if dis:
            L += ["",
                  "   An empty value_string has more than one cause, and the",
                  "   four basis values do not separate them. On these cells",
                  "   the source states the goal and explicitly declines the",
                  "   relation, which is a different fact from nobody having",
                  "   stated one:"]
            for c in dis:
                L.append("     %+d  %s" % (c["index"],
                                           _clip(c["source_disclaims"], 62)))

    us = upward_stop(term)
    ds = downward_stop(term)
    sp = unmeasured_span(term)
    if "enumeration_basis" in term and \
            term["enumeration_basis"] not in ENUMERATION_BASES:
        bad.append("enumeration_basis %r not in %s"
                   % (term["enumeration_basis"], list(ENUMERATION_BASES)))
    pc = plan_column(term)
    L += ["", "S1a stops, from the document set"]
    L.append(table(
        ["stop", "level", "what", "why"],
        [["upward",
          ("%+d" % us["index"]) if us["index"] is not None else ABSENT,
          _clip(us["artifact_id"], 34), _clip(us["why"], 48)],
         ["downward",
          ("%+d" % ds["index"]) if ds["index"] not in (None, 0) else (
              " 0" if ds["index"] == 0 else ABSENT),
          _clip("%s [%s]" % (ds["quantity"], ds["unit"]), 34),
          _clip(ds["why"], 48)]]))
    L += ["", "   unmeasured_span_min: %s" % (
        "%d level(s)" % sp["unmeasured_span_min"]
        if sp["unmeasured_span_min"] is not None else "not computable"),
        "   enumeration_basis:   %s%s"
        % (sp["enumeration_basis"],
           "  (default; not declared, not inferred)"
           if sp["enumeration_basis"] == "UNREAD" else ""),
        "   %s" % _clip(sp["note"], 62),
        "   Emitted, not scored (S1a). The name is the reading: a floor,",
        "   not a measurement of the world."]
    L += ["",
          "   plan_exists %s | practice_tracks_plan %s"
          % (pc["plan_exists"], pc["practice_tracks_plan"]),
          "   Its own column. It is not a basis and does not enter one."]
    if pc["why"]:
        L.append("   %s" % _clip(pc["why"], 62))

    cm = clock_mismatch(lv)
    if cm["clocks"]:
        L += ["", "S5 clocks, per level, not collapsed"]
        L.append(table(["level", "value", "units", "assumed?", "basis"],
                       [[("%+d" % c["index"]) if c["index"] else " 0",
                         c["value"], c["units"],
                         ("derived from %+d" % c["derived_from"])
                         if c["derived_from"] is not None else "assumed",
                         _clip(c["basis"], 44)]
                        for c in cm["clocks"]]))
        if cm["derived"]:
            L += ["",
                  "   %d of these is derived from another level's clock and"
                  % cm["derived"],
                  "   does not count as a second horizon. It is emitted",
                  "   anyway; only the disagreement count excludes it."]
        if cm["mismatch"]:
            L += ["",
                  "   MISMATCH: %d distinct time constants independently"
                  % cm["distinct"],
                  "   assumed across levels.",
                  "   Both are emitted and no pick is made. A term whose",
                  "   levels disagree on horizon is the finding (S5)."]
    return "\n".join(L)


def render(terms):
    L = ["fold matrix -- work order 8",
         "terms: %d" % len(terms), ""]
    for t in terms:
        bad = validate(t)
        if bad:
            L += ["term %s does not load:" % t.get("id")]
            L += ["  %s" % b for b in bad] + [""]
            continue
        L += [render_term(t), "", "-" * 66, ""]
    tally = upward_tally([t for t in terms if not validate(t)])
    L += ["S2, across the terms a comparison may include", ""]
    L.append(table(["basis", "upward cells"],
                   [[b, tally["counts"][b]] for b in BASIS]))
    L += ["", "value_string, per field"]
    L.append(table(["field", "ABSENT on", "of cells"],
                   [[f, tally["field_absent"][f], tally["cells"]]
                    for f in VS_FIELDS]))
    L += ["",
          "cells: %d   all three ABSENT: %d   split: %d"
          % (tally["cells"], tally["all_absent_cells"],
             tally["split_cells"]),
          "ASSERTED + ABSENT: %d   measured + derived: %d"
          % (tally["asserted_plus_absent"], tally["measured_plus_derived"]),
          "P1 (soft majority): %s" % tally["P1_majority"],
          "P3 (at least one cell splits): %s"
          % tally["P3_at_least_one_split"],
          "P4 (no magnitude anywhere): %s" % tally["P4_no_magnitude"]]
    cs = compare_spans([t for t in terms if not validate(t)])
    rows = [r for r in cs["rows"] if r["unmeasured_span_min"] is not None]
    if rows:
        L += ["", "unmeasured_span_min, and what may be compared", ""]
        L.append(table(["term", "span_min", "enumeration_basis"],
                       [[r["id"], r["unmeasured_span_min"],
                         r["enumeration_basis"]] for r in rows]))
        for b, g in cs["comparable"]:
            L += ["", "   comparable on basis %s: %s"
                  % (b, ", ".join(r["id"] for r in g))]
        for b, ids, why in cs["refused"]:
            L += ["", "   REFUSED (%s): %s" % (b, ", ".join(ids)),
                  "     %s" % why]
        L += ["",
              "   No difference is computed across a mismatch. Two floors",
              "   counted by different procedures are not two measurements",
              "   of one quantity."]

    if tally["excluded_not_evaluable"]:
        L += ["",
              "excluded from this tally as NOT_EVALUABLE (S3): %s"
              % ", ".join(tally["excluded_not_evaluable"]),
              "A refused term is not a zero and does not enter a count."]
    return "\n".join(L)


# ---- S7 screen --------------------------------------------------------

# The one token this order's own vocabulary puts on the screened list.
# S3 names the efficiency class as "efficient/optimal/better/faster" and
# `better` is a screened interpretation word; the other three are not.
# The harness WO4's amendment kept "for a real exemption later" is spent
# here, on exactly one word, declared and measured.
DELIVERED_VOCABULARY = ("better",)


def screened(text):
    masked = text
    for tok in DELIVERED_VOCABULARY:
        masked = re.sub(r"\b%s\b" % re.escape(tok), "#" * len(tok), masked,
                        flags=re.I)
    return no_severity.check(masked)


def exemption_is_only_delivered(text):
    toks = tuple(t.lower() for t in DELIVERED_VOCABULARY)
    for _, word, _ in no_severity.hits(text):
        if word.lower() not in toks:
            return False
    return True


# ---- selftest ---------------------------------------------------------

def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("fold_matrix selftest")

    # ---- S3 scope.
    T = {"name": "panel efficiency", "scope": {}}
    ck("an efficiency-class term with no scope is NOT_EVALUABLE",
       scope_check(T)[0], NOT_EVALUABLE)
    ck("and every missing field is named, not just the first",
       sorted(scope_check(T)[1]), sorted(list(SCOPE_FIELDS)))
    T2 = {"name": "panel efficiency",
          "scope": {"with_respect_to": "incident photon flux",
                    "boundary": "the cell surface",
                    "horizon": "instantaneous"}}
    ck("a complete scope is evaluable", scope_check(T2)[0], EVALUABLE)
    T3 = {"name": "panel efficiency",
          "scope": {"with_respect_to": "x", "boundary": "y",
                    "horizon": "unknown"}}
    ck("a field declared unknown is still missing",
       scope_check(T3)[0], NOT_EVALUABLE)
    ck("and is reported apart from an omission",
       "declared unknown" in scope_check(T3)[2], True)
    ck("a term with no efficiency word takes no scope",
       scope_check({"name": "grid emission factor"})[0], EVALUABLE)

    # ---- S3 replacement.
    R = {"name": "x more efficient than y",
         "scope": {"with_respect_to": "a", "boundary": "b", "horizon": "c"},
         "replacement": {"Y": "leaf", "Y_function_set": UNREAD}}
    ck("an unread baseline refuses the comparison",
       replacement_check(R)[0], NOT_EVALUABLE)
    ck("and says it was not compared rather than not supported",
       "nothing was compared" in replacement_check(R)[1], True)
    R2 = dict(R, replacement={"Y": "leaf", "Y_function_set": PARTIAL,
                              "Y_functions": ["a", "b"]})
    ck("a partial baseline is also refused",
       replacement_check(R2)[0], NOT_EVALUABLE)
    R3 = dict(R, replacement={"Y": "leaf", "Y_function_set": ENUMERATED,
                              "Y_functions": ["a"]})
    ck("an enumerated baseline is evaluable",
       replacement_check(R3)[0], EVALUABLE)

    # ---- NOT_EVALUABLE is structurally unrankable.
    try:
        score(T)
        got = "returned"
    except NotEvaluable:
        got = "raised"
    ck("score() raises on a NOT_EVALUABLE term", got, "raised")
    try:
        score({"name": "grid emission factor"})
        got2 = "returned"
    except NotEvaluable:
        got2 = "raised"
    ck("and raises on an evaluable one too: there is no score", got2,
       "raised")

    # ---- S4 sign hygiene.
    ck("a name asserting a sign is flagged",
       sign_asserting("waste heat recovery"), ["waste"])
    ck("a neutral name is not",
       sign_asserting("outlet temperature"), [])
    ck("a flagged name with no declared neutral reading says so",
       neutral_reading({"name": "efficiency"})["state"], "NOT_SUPPLIED")
    ck("and one with a declared reading carries it",
       neutral_reading({"name": "efficiency", "neutral_reading":
                        {"quantity": "J out per J in", "frame": "cell "
                         "surface, instantaneous"}})["state"], "supplied")
    # Sign words that are not efficiency-class flag under S4 and do not
    # trigger S3's scope requirement. Both halves, because collapsing
    # them would make every mention of a loss need a horizon.
    ck("a sign word outside the efficiency class takes no scope",
       scope_check({"name": "leakage rate"})[0], EVALUABLE)
    ck("and is still flagged", sign_asserting("leakage rate"), ["leakage"])

    # ---- S5 clocks.
    lv = [{"index": 0, "clock": {"value": 3.0, "units": "years"}},
          {"index": 1, "clock": {"value": 30.0, "units": "years"}}]
    cm = clock_mismatch(lv)
    ck("two different clocks are a mismatch", cm["mismatch"], True)
    # A derived clock is the first assumption carried forward, not a
    # second horizon. Both halves: it does not count, and it still shows.
    dv = clock_mismatch([
        {"index": -1, "clock": {"value": 3.0, "units": "years"}},
        {"index": 0, "clock": {"value": 3.403, "units": "years",
                               "derived_from": -1}}])
    ck("a derived clock is not a second horizon", dv["mismatch"], False)
    ck("and is emitted anyway", len(dv["clocks"]), 2)
    ck("and is counted apart", (dv["independent"], dv["derived"]), (1, 1))
    ck("both are emitted", [c["value"] for c in cm["clocks"]], [3.0, 30.0])
    ck("and nothing is collapsed", cm["collapsed"], None)
    ck("two levels agreeing are not a mismatch",
       clock_mismatch([{"index": 0, "clock": {"value": 3.0, "units": "y"}},
                       {"index": 1, "clock": {"value": 3.0, "units": "y"}}]
                      )["mismatch"], False)
    ck("a level with no clock contributes none rather than a zero",
       clock_of({"index": 0, "clock": {"state": "UNMEASURED"}}), None)

    # ---- S2 upward cells and the empty value_string.
    ALL_ABSENT = {"sign": ABSENT, "magnitude": ABSENT, "unit": ABSENT}
    t = {"levels": [{"index": -1, "basis": MEASURED},
                    {"index": 0, "basis": MEASURED},
                    {"index": 1, "basis": ASSERTED,
                     "value_string": dict(ALL_ABSENT)},
                    {"index": 2, "basis": ABSENT,
                     "value_string": dict(ALL_ABSENT)}]}
    up = upward_cells(t)
    ck("only positive levels are upward cells",
       [c["index"] for c in up], [1, 2])
    ck("an all-ABSENT triple emits as ABSENT, never as zero",
       [c["value_string"]["magnitude"] for c in up], [ABSENT, ABSENT])
    ck("and all-ABSENT is flagged as such",
       [c["vs_all_absent"] for c in up], [True, True])

    # ---- S2 revised: the three fields are INDEPENDENT. A stated
    # direction with no size is the ordinary shape of a purpose claim,
    # and the free-text form recorded it as identical to an unwritten
    # cell. Both halves asserted.
    split = upward_cells({"levels": [
        {"index": 1, "basis": ASSERTED,
         "value_string": {"sign": "+", "magnitude": ABSENT,
                          "unit": ABSENT}}]})[0]
    ck("a sign with no magnitude is not all-ABSENT",
       split["vs_all_absent"], False)
    ck("and the sign survives", split["value_string"]["sign"], "+")
    ck("a missing field defaults to ABSENT, not to a blank",
       value_string({"value_string": {"sign": "-"}}),
       {"sign": "-", "magnitude": ABSENT, "unit": ABSENT})
    # A magnitude of 0 is a STATED size and must not read as absent.
    z = value_string({"value_string": {"sign": "+", "magnitude": 0,
                                       "unit": "kg CO2e per person"}})
    ck("a stated magnitude of zero is not ABSENT", z["magnitude"], 0)
    ck("and a cell carrying it does not read all-ABSENT",
       upward_cells({"levels": [{"index": 1, "basis": ASSERTED,
                                 "value_string": {"sign": "+",
                                                  "magnitude": 0,
                                                  "unit": "u"}}]}
                    )[0]["vs_all_absent"], False)

    # The v1 free-text form is REFUSED, not coerced: an empty string
    # cannot say which of the three fields is missing.
    try:
        value_string({"value_string": ""})
        got_vs = "coerced"
    except ValueError:
        got_vs = "refused"
    ck("a v1 free-text value_string is refused rather than widened",
       got_vs, "refused")

    # ---- validate refuses what the schema requires.
    ck("an upward cell with no value_string field does not load",
       len(validate({"levels": [{"index": 1, "basis": ASSERTED}]})), 1)
    ck("an unknown basis does not load",
       len(validate({"levels": [{"index": 0, "basis": "probably"}]})), 1)
    ck("a legal all-ABSENT triple does load",
       validate({"levels": [{"index": 1, "basis": ASSERTED,
                             "value_string": dict(ALL_ABSENT)}]}), [])
    ck("a sign outside the vocabulary does not load",
       len(validate({"levels": [{"index": 1, "basis": ASSERTED,
                                 "value_string": {"sign": "up"}}]})), 1)
    ck("a non-numeric magnitude does not load",
       len(validate({"levels": [{"index": 1, "basis": ASSERTED,
                                 "value_string": {"magnitude": "large"}}]})),
       1)

    # ---- S1a stop rules.
    T1 = {"levels": [
        {"index": -2, "basis": ABSENT,
         "quantified": {"quantity": "carbon", "unit": "kg", "computed": False}},
        {"index": -1, "basis": ABSENT,
         "quantified": {"quantity": "mix", "unit": "fraction",
                        "computed": False}},
        {"index": 0, "basis": MEASURED,
         "quantified": {"quantity": "emissions", "unit": "kg CO2e",
                        "computed": True}},
        {"index": 1, "basis": ASSERTED, "value_string": dict(ALL_ABSENT),
         "artifact_id": "charter"},
        {"index": 2, "basis": ABSENT, "value_string": dict(ALL_ABSENT)}]}
    ck("the upward stop is the highest level with an artifact",
       upward_stop(T1)["index"], 1)
    ck("and a level above it with none does not extend the arm",
       upward_stop(T1)["artifact_id"], "charter")
    ck("no artifact anywhere stops the arm at ABSENT",
       upward_stop({"levels": [{"index": 1, "basis": ASSERTED,
                                "value_string": dict(ALL_ABSENT)}]}
                   )["artifact_id"], ABSENT)
    # The rule most likely to be misread: the floor is the deepest
    # COMPUTED quantity, not the deepest one that exists. Levels -1 and
    # -2 name real physical quantities with units and are below the stop.
    ck("the downward stop is the deepest COMPUTED quantity",
       downward_stop(T1)["index"], 0)
    ck("a real physical quantity nobody computed is below the floor",
       downward_stop(T1)["quantity"], "emissions")
    ck("and the span counts what continues below it",
       unmeasured_span(T1)["unmeasured_span_min"], 2)
    ck("a term computing nothing has no floor rather than floor zero",
       downward_stop({"levels": [{"index": 0, "basis": ABSENT}]})["index"],
       None)
    ck("and its span is not computable rather than zero",
       unmeasured_span({"levels": [{"index": 0, "basis": ABSENT}]}
                       )["unmeasured_span_min"], None)
    ck("a quantified block with no `computed` field does not load",
       len(validate({"levels": [{"index": 0, "basis": MEASURED,
                                 "quantified": {"quantity": "x",
                                                "unit": "u"}}]})), 1)

    # ---- FM_016 fix: enumeration_basis, declared and never inferred.
    ck("an undeclared basis reads UNREAD",
       enumeration_basis({}), "UNREAD")
    ck("a well-traced-looking grid still reads UNREAD without a declaration",
       enumeration_basis(T1), "UNREAD")
    ck("a declared basis is carried",
       enumeration_basis({"enumeration_basis": DOCUMENT_NAMED}),
       DOCUMENT_NAMED)
    ck("an out-of-vocabulary basis does not load",
       len(validate({"enumeration_basis": "looked at it"})), 1)
    ck("and does not silently become UNREAD in a loaded term",
       "enumeration_basis" in validate(
           {"enumeration_basis": "looked at it"})[0], True)

    # The emitted number is named for what it is.
    sp = unmeasured_span(dict(T1, enumeration_basis=AUTHOR_READ))
    ck("the emitted number is unmeasured_span_min",
       sorted(k for k in sp if "span" in k), ["unmeasured_span_min"])
    ck("and the basis travels with it", sp["enumeration_basis"], AUTHOR_READ)
    ck("the note says floor, not measurement",
       sp["note"].startswith("at least"), True)

    # ---- comparison across documents requires a matching basis.
    A = dict(T1, id="A", enumeration_basis=AUTHOR_READ)
    B = dict(T1, id="B", enumeration_basis=DOCUMENT_NAMED)
    A2 = dict(T1, id="A2", enumeration_basis=AUTHOR_READ)
    U = dict(T1, id="U")
    cs = compare_spans([A, B])
    ck("a mismatched pair is refused", [r[0] for r in cs["refused"]].count(
        "MISMATCH"), 1)
    ck("and no difference is computed anywhere", cs["difference"], None)
    ck("both floors are still emitted",
       sorted(r["id"] for r in cs["rows"]), ["A", "B"])
    ck("a matching pair is comparable",
       [b for b, _g in compare_spans([A, A2])["comparable"]], [AUTHOR_READ])
    ck("an UNREAD basis is refused even against itself",
       [b for b, _g in compare_spans([U, dict(U, id="U2")])["comparable"]],
       [])
    # Composed from tokens so the check does not match its own source.
    src = open(os.path.abspath(__file__)).read()
    ck("no difference of two span_min values is computed in this module",
       ("span" + "_min\"] -" in src) or ("span" + "_min'] -" in src), False)

    # ---- S1a's plan column is separate and stays separate.
    pc = plan_column({"plan": {"plan_exists": YES,
                               "practice_tracks_plan": NO}})
    ck("the plan column reads its own key", (pc["plan_exists"],
                                             pc["practice_tracks_plan"]),
       (YES, NO))
    ck("an unstated plan column reads UNREAD, not no",
       plan_column({})["plan_exists"], UNREAD_STATE)
    ck("an out-of-vocabulary plan state does not load",
       len(validate({"plan": {"plan_exists": "maybe"}})), 1)
    ck("no plan value reaches a basis field",
       [c["basis"] for c in upward_cells(
           dict(T1, plan={"plan_exists": YES,
                          "practice_tracks_plan": YES}))],
       [ASSERTED, ABSENT])

    # ---- the tally excludes refused terms rather than zeroing them.
    tal = upward_tally([T, {"name": "plain", "levels": [
        {"index": 1, "basis": ASSERTED,
         "value_string": dict(ALL_ABSENT)}]}])
    ck("a NOT_EVALUABLE term is excluded from the tally, not counted as 0",
       (tal["cells"], tal["excluded_not_evaluable"]), (1, ["?"]))

    # ---- declared-frame is imported, not retyped.
    ck("boundary and horizon come from declared-frame's CORE",
       (_CORE is not None and
        set(("boundary", "horizon")).issubset(set(_CORE or ()))), True)

    # ---- S7 screen, three arms.
    txt = render([{"id": "x", "name": "grid emission factor",
                   "levels": [{"index": 1, "basis": ASSERTED,
                               "value_string": dict(ALL_ABSENT)}]}])
    ck("an emitted report is clean under the declared exemption",
       screened(txt)[0], True)
    ck("and only the declared token fires without it",
       exemption_is_only_delivered(txt), True)
    ck("a planted grading word is caught through the exemption",
       screened(txt + "\nthis term is wrong")[0], False)
    ck("the exemption is exactly one word", len(DELIVERED_VOCABULARY), 1)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  fold_matrix.py run [TERM_ID ...]
  fold_matrix.py --selftest"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if not argv or argv[0] != "run":
        print(USAGE)
        return 2
    terms = load_terms()
    if not terms:
        sys.stderr.write("no terms in %s\n" % TERMS)
        return 2
    want = [a for a in argv[1:] if not a.startswith("-")]
    if want:
        terms = [t for t in terms if t.get("id") in want]
        if not terms:
            sys.stderr.write("no such term\n")
            return 2
    print(render(terms))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
