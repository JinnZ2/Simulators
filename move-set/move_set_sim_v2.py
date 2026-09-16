#!/usr/bin/env python3
# move_set_sim_v2.py -- CC0, stdlib only, phone-buildable, 3.9+
#
# Second order, 2026-09-16 (WORK_ORDER_V2.md, landed verbatim).
#
# The order names the file move_set_sim.py. That name is taken by a
# DELIVERED artifact in this folder which is never edited, so this lands
# beside it under the repo's supersession convention -- both inspectable,
# neither overwritten. Recorded as MSV_001.
#
# ---------------------------------------------------------------------
# WHAT IS NEW, and it is one thing.
#
# v1's docstring names its own load-bearing guard:
#
#     "a bare 'I don't know' is not a refusal and scores zero. This is
#      the only thing keeping symmetric scoring from being gameable"
#
# and the implementation checks that two strings are non-empty. A ledger
# carrying "x" in every blocker and unblocker scores full marks (MV_002,
# null-tested there, not disputed here).
#
# The repair is adaptive-claim-loop ACL_012/ACL_017: a guard that asks
# for PROSE can be satisfied with prose; the guards that hold are the
# ones asking for a NUMBER or a COMPUTATION. So every entry here is
# checked AGAINST THE ARTIFACT:
#
#   QUOTE   the value is SLICED OUT of the artifact at a stated line and
#           column range. The ledger says WHERE; the artifact supplies
#           WHAT. A ledger cannot state a value the artifact does not
#           carry at the place it cites.
#   DERIVED the value is RECOMPUTED from operands sliced out of the
#           artifact. The ledger declares whether the stated arithmetic
#           HOLDS; the scorer recomputes and gates on the declaration
#           matching, in both directions.
#   ABSENT  the reason carries a SEARCHED SPAN and a SOUGHT token, and
#           the scorer confirms the span resolves and the token is not
#           in it. An absence with no span does not score. An absence
#           whose token IS present is REFUTED.
#
# tools/sourced.py is IMPORTED, not reimplemented (the MF_019 discipline;
# five stale copies of one gate across three drops is what copying got).
# It checks that value / source text / locator are mutually consistent.
# It says itself that it does not check whether the source is true. That
# is the layer added here: bind() resolves the locator INTO THE ARTIFACT
# and requires the cited source text to be the artifact's own line.
# ---------------------------------------------------------------------
#
# usage:
#   python3 move_set_sim_v2.py                      # the move set
#   python3 move_set_sim_v2.py --emit ARTIFACT [--seed N]
#   python3 move_set_sim_v2.py --score LEDGER ARTIFACT
#   python3 move_set_sim_v2.py --demo
#   python3 move_set_sim_v2.py --paths RUN1 RUN2 ... ARTIFACT
#   python3 move_set_sim_v2.py --choices
#
# This module carries no checks. Run: python3 test_move_set_v2.py

import collections
import hashlib
import json
import os
import random
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), "tools"))
import sourced as S                                    # noqa: E402
sys.path.pop(0)


# --- CHOICES -- printed by --choices, cited inline where each takes effect
CHOICES = {
    1: "M6 is built BOTH ways. The order's move list makes it a sixth "
       "move; the order's OUTPUT section makes ABSENT a return available "
       "to every move. These are not exclusive, so both are implemented: "
       "M6 has its own trigger AND every move admits ABSENT.",
    2: "The demo artifact is cited BY PATH and not copied. It is already "
       "in this repo. A copy is the drift MF_019 records seven times; a "
       "sha256 pin makes a change to the original detectable instead.",
    3: "Recomputation tolerance is RELATIVE 5e-3. The demo artifact "
       "rounds to 3-4 significant figures, so an exact test would report "
       "rounding as a failure.",
    4: "Coverage counts DISTINCT artifact lines. Overlapping searched "
       "ranges are counted once -- double-counting is where a coverage "
       "number inflates.",
    5: "confidence is a free string. It is reported and enters NO score. "
       "Combining it with points would make one number out of two "
       "quantities (domain-ledger DL_001, METHOD_SPEC section 5).",
    6: "An absence is verified OVER THE SPAN DECLARED. A narrow span is "
       "a weak absence and scores the same 1.0, so coverage is reported "
       "beside it and never folded in.",
    7: "path_dependence REFUSES runs that do not declare distinct move "
       "orders. v1 returned 'claim holds' for two identical ledgers "
       "(MV_004). NOT_EVALUABLE is a third state, not a pass.",
}


# --- the six moves. order_line is the order's own text, verbatim.
MOVES = collections.OrderedDict()

MOVES["M1_provenance"] = {
    "order_line": "ask where a number came from",
    "trigger": "artifact ships a number",
    "ask": "Where did this number come from? Name the instrument, the "
           "population it was taken over, and when it was taken. Cite the "
           "line that says so, or report that nothing does.",
    "absence_is": "the artifact ships the number and states no source for it",
    "kinds": ("QUOTE", "ABSENT"),
}
MOVES["M2_substitution"] = {
    "order_line": "ask what a term is standing in for",
    "trigger": "artifact uses a term where a quantity belongs",
    "ask": "What is this term standing in for? Resolve it to the deepest "
           "quantity this artifact actually computes. Cite the line.",
    "absence_is": "the term resolves to no computed quantity in the artifact",
    "kinds": ("QUOTE", "ABSENT"),
}
MOVES["M3_relation_held"] = {
    "order_line": "ask whether a stated relationship is still held by anything",
    "trigger": "artifact asserts a relationship between two things",
    "ask": "Is this relationship held by anything in the artifact, or "
           "stated once and carried? Cite what holds it, or report that "
           "nothing does.",
    "absence_is": "the relationship is asserted and nothing in the artifact holds it",
    "kinds": ("QUOTE", "ABSENT"),
}
MOVES["M4_perturb"] = {
    "order_line": "perturb and see what moves",
    "trigger": "artifact reports a value derived from other values it ships",
    "ask": "A published artifact cannot be perturbed; its ARITHMETIC can. "
           "Recompute a stated relationship from the operands the artifact "
           "supplies. What moves, and what stays flat that should not?",
    "absence_is": "the stated relationship's operands are not in the artifact",
    "kinds": ("DERIVED", "ABSENT"),
}
MOVES["M5_self_report"] = {
    "order_line": "check whether the instrument would report its own failure",
    "trigger": "artifact is produced by a process with a stated purpose",
    "ask": "If this instrument were failing at its stated purpose, would "
           "this artifact look different? Name the value that would change, "
           "and cite it.",
    "absence_is": "no value in the artifact would move under the failure",
    "kinds": ("QUOTE", "ABSENT"),
}
# CHOICE 1 -- M6 is a move with its own trigger AND every move above
# admits ABSENT. The order's move list and its OUTPUT section read two
# ways and the readings are not exclusive, so both are built.
MOVES["M6_absence_first_class"] = {
    "order_line": "refuse to score what cannot be seen; make the absence a "
                  "first-class value",
    "trigger": "artifact invites a quantity it does not supply the operands for",
    "ask": "Name a quantity this artifact reports or invites and does not "
           "supply the operands for. Do not score it as zero and do not "
           "score it as unknown. Name the span searched and the token "
           "sought.",
    "absence_is": "this move's whole subject -- see CHOICE 1",
    "kinds": ("ABSENT", "QUOTE"),
}

KINDS = ("QUOTE", "DERIVED", "ABSENT")

# Verdicts. Kept apart because they call for different next actions.
BOUND = "BOUND"                                # quote sliced out of the artifact
ARITHMETIC_AS_DECLARED = "ARITHMETIC_AS_DECLARED"
VERIFIED_ABSENCE = "VERIFIED_ABSENCE"
EARNED = (BOUND, ARITHMETIC_AS_DECLARED, VERIFIED_ABSENCE)

UNBOUND_LINE = "UNBOUND_LINE"                  # cited line is not in the artifact
UNBOUND_TEXT = "UNBOUND_TEXT"                  # cited source text is not that line
UNBOUND_VALUE = "UNBOUND_VALUE"                # value is not at those columns
UNRATED_FIELDS = "UNRATED_FIELDS"              # tools/sourced gate refused
OPERAND_NOT_IN_ARTIFACT = "OPERAND_NOT_IN_ARTIFACT"
ARITHMETIC_NOT_AS_DECLARED = "ARITHMETIC_NOT_AS_DECLARED"
UNVERIFIED_NO_SPAN = "UNVERIFIED_NO_SPAN"      # absence with nowhere searched
UNVERIFIED_SPAN = "UNVERIFIED_SPAN"            # searched span outside the artifact
REFUTED_ABSENCE = "REFUTED_ABSENCE"            # the sought token IS in the span
MALFORMED = "MALFORMED"

VERDICTS = EARNED + (UNBOUND_LINE, UNBOUND_TEXT, UNBOUND_VALUE, UNRATED_FIELDS,
                     OPERAND_NOT_IN_ARTIFACT, ARITHMETIC_NOT_AS_DECLARED,
                     UNVERIFIED_NO_SPAN, UNVERIFIED_SPAN, REFUTED_ABSENCE,
                     MALFORMED)

TOL = 5e-3                                     # CHOICE 3

Absent = collections.namedtuple("Absent", "reason looked_at sought")


class LedgerError(Exception):
    """A ledger that cannot be read at all. Distinct from an entry that
    reads and does not score -- that is a verdict, not an error."""


# --- artifact ---------------------------------------------------------

def read_artifact(path):
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    lines = text.splitlines()
    return {"path": path, "text": text, "lines": lines,
            "n_lines": len(lines),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}


def _number(s):
    """A float, or None. The demo artifact uses U+2212 MINUS SIGN, so a
    str.strip()-and-float would report a real number as absent."""
    t = (s or "").strip().replace("\u2212", "-").replace("\u2013", "-")
    t = t.replace(",", "").rstrip(".")
    try:
        return float(t)
    except (TypeError, ValueError):
        return None


# --- binding: the layer tools/sourced.py says it does not do ----------

def bind_quote(art, entry):
    """Slice the value OUT of the artifact. The ledger supplies a line
    number and a column range; the artifact supplies the value."""
    f = entry.get("finding") or {}
    line_no = f.get("line")
    i, j = f.get("col_start"), f.get("col_end")
    if not isinstance(line_no, int) or not isinstance(i, int) \
            or not isinstance(j, int):
        return MALFORMED, None, "line/col_start/col_end must be integers"
    if line_no < 1 or line_no > art["n_lines"]:
        return UNBOUND_LINE, None, "line %d outside artifact (1..%d)" % (
            line_no, art["n_lines"])
    line_text = art["lines"][line_no - 1]
    if f.get("quote") is not None and f["quote"] != line_text:
        return UNBOUND_TEXT, None, "cited text is not line %d of the artifact" % line_no
    loc = S.Locator(art["path"], line_no, i, j, label=entry.get("move_id"))
    if i < 0 or j > len(line_text) or i >= j:
        return UNBOUND_VALUE, None, "columns %d:%d outside line %d" % (i, j, line_no)
    sv = S.slice_sourced(line_text, i, j, loc)
    gated = S.gate(sv, name=entry.get("move_id", "finding"))
    if isinstance(gated, S.Unrated):
        return UNRATED_FIELDS, None, repr(gated)
    expect = f.get("expect")
    if expect is not None and expect != sv.value:
        return UNBOUND_VALUE, sv, "ledger expects %r, artifact carries %r" % (
            expect, sv.value)
    return BOUND, sv, "sliced from %s" % loc.describe()


OPS = {
    "sub": lambda a: a[0] - a[1],
    "abs_sub": lambda a: abs(a[0] - a[1]),
    "div": lambda a: (a[0] / a[1]) if a[1] != 0 else None,
    "mul": lambda a: a[0] * a[1],
}


def bind_derived(art, entry):
    """Recompute a stated relationship from operands sliced out of the
    artifact, and gate on whether the ledger's DECLARATION about it holds.

    A ledger saying the arithmetic holds where it fails scores 0. A ledger
    saying it FAILS where it fails scores 1.0 -- that is a finding, and
    refusing it would make a discrepancy unreportable."""
    f = entry.get("finding") or {}
    op = f.get("op")
    ops = f.get("operands")
    if op not in OPS or not isinstance(ops, list) or len(ops) != 2:
        return MALFORMED, None, "op must be one of %s with 2 operands" % (
            sorted(OPS),)
    if "holds" not in f or not isinstance(f["holds"], bool):
        return MALFORMED, None, "finding must declare holds: true|false"
    vals, where = [], []
    for k, o in enumerate(ops):
        sub = {"move_id": entry.get("move_id"), "finding": o}
        v, sv, why = bind_quote(art, sub)
        if v != BOUND:
            return OPERAND_NOT_IN_ARTIFACT, None, "operand %d: %s (%s)" % (k, v, why)
        n = _number(sv.value)
        if n is None:
            return OPERAND_NOT_IN_ARTIFACT, None, \
                "operand %d %r is not a number" % (k, sv.value)
        vals.append(n)
        where.append(sv.locator.describe())
    got = OPS[op](vals)
    stated = _number(str(f.get("stated")))
    if got is None or stated is None:
        return MALFORMED, None, "stated value must be a number; div by zero"
    rel = abs(got - stated) / (abs(stated) if stated else 1.0)
    holds = rel <= TOL                                          # CHOICE 3
    detail = "%s(%s) = %.6g vs stated %.6g  rel %.3g  [%s]" % (
        op, ", ".join("%.6g" % v for v in vals), got, stated, rel,
        "; ".join(where))
    if holds != f["holds"]:
        return ARITHMETIC_NOT_AS_DECLARED, got, \
            "ledger declares holds=%s; recomputation says %s -- %s" % (
                f["holds"], holds, detail)
    return ARITHMETIC_AS_DECLARED, got, detail


# --- absence: first-class, and checked ---------------------------------

def _spans(art, looked_at):
    """Normalise declared 1-based inclusive line ranges. Returns
    (line_numbers, error) -- error is a string or None."""
    if not looked_at:
        return (), "no span declared"
    seen = set()
    for r in looked_at:
        try:
            a, b = int(r[0]), int(r[1])
        except (TypeError, ValueError, IndexError):
            return (), "span %r is not a [from, to] pair" % (r,)
        if a < 1 or b > art["n_lines"] or a > b:
            return (), "span %d-%d outside artifact (1..%d)" % (
                a, b, art["n_lines"])
        seen.update(range(a, b + 1))                            # CHOICE 4
    return tuple(sorted(seen)), None


def coverage(art, looked_at):
    """Distinct artifact lines searched, as a fraction. None when nothing
    was declared -- an undeclared span is not zero coverage, it is no
    measurement (CHOICE 4, CHOICE 6)."""
    lines, err = _spans(art, looked_at)
    if err or not art["n_lines"]:
        return None
    return round(len(lines) / float(art["n_lines"]), 4)


def verify_absence(art, absent):
    """An absence is a claim about a place. Confirm the place exists and
    the sought token is not in it."""
    if not isinstance(absent, Absent):
        return MALFORMED, "absent must carry reason / looked_at / sought"
    if not absent.reason:
        return MALFORMED, "absence states no reason"
    if not absent.sought:
        return UNVERIFIED_NO_SPAN, "absence names no token sought"
    lines, err = _spans(art, absent.looked_at)
    if err == "no span declared":
        return UNVERIFIED_NO_SPAN, err
    if err:
        return UNVERIFIED_SPAN, err
    hay = "\n".join(art["lines"][n - 1] for n in lines).lower()
    hits = [t for t in absent.sought if str(t).lower() in hay]
    if hits:
        return REFUTED_ABSENCE, "sought token(s) %s ARE in the searched span" % (
            ", ".join(repr(h) for h in hits),)
    return VERIFIED_ABSENCE, "%d line(s) searched, %d token(s) not found" % (
        len(lines), len(absent.sought))


# --- ledger -----------------------------------------------------------

def read_ledger(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (IOError, ValueError) as exc:
        raise LedgerError("cannot read %s: %s" % (path, exc))
    if not isinstance(raw, dict) or "entries" not in raw:
        raise LedgerError(
            "%s: a ledger is an object with 'artifact', 'order' and "
            "'entries'. v1 ledgers are bare lists and carry no order "
            "field, which is MV_004 -- they do not read here." % path)
    order = raw.get("order")
    if not isinstance(order, list) or not order:
        raise LedgerError("%s: ledger must declare the move order it ran in"
                          % path)
    return raw


def read_entry(art, e):
    """One entry -> (move_id, kind, verdict, confidence, detail, payload)."""
    mv = e.get("move_id")
    conf = e.get("confidence")
    has_f = e.get("finding") is not None
    has_a = e.get("absent") is not None
    if mv not in MOVES:
        return mv, None, MALFORMED, conf, "no such move", None
    if has_f == has_a:
        return mv, None, MALFORMED, conf, \
            "exactly one of finding / absent, never both and never neither", None
    if has_a:
        a = e["absent"]
        if not isinstance(a, dict):
            return mv, "ABSENT", MALFORMED, conf, "absent must be an object", None
        ab = Absent(a.get("reason"), a.get("looked_at") or [],
                    a.get("sought") or [])
        v, why = verify_absence(art, ab)
        return mv, "ABSENT", v, conf, why, ab
    kind = (e["finding"] or {}).get("kind")
    if kind not in ("QUOTE", "DERIVED"):
        return mv, kind, MALFORMED, conf, \
            "finding.kind must be QUOTE or DERIVED", None
    if kind not in MOVES[mv]["kinds"]:
        return mv, kind, MALFORMED, conf, \
            "%s does not admit a %s finding" % (mv, kind), None
    if kind == "QUOTE":
        v, sv, why = bind_quote(art, e)
    else:
        v, sv, why = bind_derived(art, e)
    return mv, kind, v, conf, why, sv


def score(ledger, art):
    """Symmetric on verdict class, asymmetric on whether it was checked
    against the artifact. A refused verdict scores as high as an answered
    one; neither scores on prose alone."""
    rows, total = [], 0.0
    seen, n_abs = set(), 0
    for e in ledger["entries"]:
        mv, kind, v, conf, why, payload = read_entry(art, e)
        pts = 1.0 if v in EARNED else 0.0
        if kind == "ABSENT":
            n_abs += 1
        if mv in MOVES:
            seen.add(mv)
        cov = None
        if isinstance(payload, Absent):
            cov = coverage(art, payload.looked_at)                # CHOICE 6
        rows.append({"move_id": mv, "kind": kind, "verdict": v,
                     "points": pts, "confidence": conf,           # CHOICE 5
                     "detail": why, "coverage": cov})
        total += pts
    n = len(ledger["entries"])
    return {
        "artifact": art["path"],
        "artifact_sha256": art["sha256"],
        "order": ledger.get("order"),
        "rows": rows,
        "total": round(total, 2),
        "possible": float(len(MOVES)),
        "moves_not_run": [m for m in MOVES if m not in seen],
        "absence_fraction": round(n_abs / float(n), 2) if n else None,
        "note": "absence_fraction is reported, never penalized. confidence "
                "enters no score. coverage is reported beside a verified "
                "absence and never folded into it.",
    }


# --- the orderless claim ----------------------------------------------

def path_dependence(ledgers, art):
    """Falsifier for 'the chain is path-dependent, the moves are not'.

    v1 compared finding sets across runs and checked nothing about the
    ORDERS those runs used, so two identical ledgers returned 'claim
    holds' (MV_004). Here a run that does not declare a distinct order
    does not enter the comparison (CHOICE 7)."""
    if len(ledgers) < 2:
        return {"runs": len(ledgers), "verdict": "NOT_EVALUABLE",
                "reason": "fewer than two runs"}
    orders = [tuple(l.get("order") or ()) for l in ledgers]
    if len(set(orders)) < len(orders):
        return {"runs": len(ledgers), "verdict": "NOT_EVALUABLE",
                "reason": "runs do not declare distinct move orders; "
                          "an order-invariance test needs varied orders",
                "orders": [list(o) for o in orders]}
    sets = []
    for l in ledgers:
        s = set()
        for e in l["entries"]:
            mv, kind, v, conf, why, payload = read_entry(art, e)
            s.add((mv, v))
        sets.append(s)
    stable = all(s == sets[0] for s in sets)
    drift = sorted(set().union(*sets) - set.intersection(*sets))
    return {"runs": len(ledgers), "orderless": stable,
            "orders": [list(o) for o in orders],
            "order_sensitive_findings": [list(x) for x in drift],
            "verdict": "ORDERLESS -- claim holds" if stable
                       else "CHAIN DETECTED -- findings depend on move order"}


# --- emit -------------------------------------------------------------

def emit(artifact, seed=None):
    keys = list(MOVES)
    random.Random(seed).shuffle(keys)
    return {
        "artifact": artifact,
        "seed": seed,
        "order": keys,
        "prompts": [{"move_id": k, "order_line": MOVES[k]["order_line"],
                     "trigger": MOVES[k]["trigger"], "ask": MOVES[k]["ask"],
                     "kinds": list(MOVES[k]["kinds"])} for k in keys],
        "ledger_schema": {
            "artifact": "<path to the artifact this was read against>",
            "order": "<the move order this run used -- required>",
            "entries": [{
                "move_id": "<one of %s>" % ", ".join(MOVES),
                "confidence": "<free text; reported, never scored>",
                "finding": {
                    "kind": "QUOTE",
                    "line": "<1-based artifact line>",
                    "col_start": "<int>", "col_end": "<int>",
                    "quote": "<the artifact line, verbatim -- optional check>",
                    "expect": "<what you say is at those columns -- optional>",
                },
                "finding_DERIVED": {
                    "kind": "DERIVED",
                    "op": "<one of %s>" % ", ".join(sorted(OPS)),
                    "operands": "[{line, col_start, col_end} x2]",
                    "stated": "<the value the artifact states>",
                    "holds": "<true if you say the arithmetic reproduces>",
                },
                "absent": {
                    "reason": "<why the quantity cannot be seen>",
                    "looked_at": "[[line_from, line_to], ...] -- required",
                    "sought": "[<literal token>, ...] -- required",
                },
            }],
        },
    }


# --- demo -------------------------------------------------------------

DEMO_ARTIFACT = os.path.join(os.path.dirname(_HERE),
                             "aperiodic-order-sim-stack", "SIM_STACK_REPORT.txt")
DEMO_SHA256 = "165faf5346b322e43a5e7b4a426e50b997982b611f44c6a0da7d18ae7a7b6f31"
DEMO_LEDGER = os.path.join(_HERE, "ledgers", "sim_stack_report.json")

CONTAMINATION = """\
CONTAMINATION, DECLARED BEFORE THE NUMBERS.

This repository already carries an audit of this artifact
(aperiodic-order-sim-stack/CLAIM_TABLE.md, AOS_001..AOS_010). The reading
layer of this demo is therefore NOT blind: whoever wrote the ledger had
access to prior findings about the same document.

What is scored here is the MECHANICAL layer only -- does a cited line
exist, does a value sit at the cited columns, does a stated arithmetic
reproduce from operands the artifact supplies, is a sought token absent
from a declared span. Every one of those is recomputable by a reader with
the artifact and no other context.

What is NOT scored is whether any reading is correct. AOS_009 holds that
the report's 0.021 baseline is the smallest of three pairwise gaps and
that the honest ratio is nearer 4.5x than 15x. That is a reading. This
demo recomputes that 0.021 baseline from the artifact's own two
dimensions and reports what it gets; it does not adjudicate which
baseline belongs in the denominator.

A self-run is void as a capability score -- the runner holds the key
(frame-location-benchmark FLB_010). This demo shows the harness runs and
what it refuses. It is not evidence about anyone's auditing ability."""


def demo():
    art = read_artifact(DEMO_ARTIFACT)
    led = read_ledger(DEMO_LEDGER)
    out = score(led, art)
    out["artifact_sha256_expected"] = DEMO_SHA256
    out["artifact_unchanged"] = (art["sha256"] == DEMO_SHA256)   # CHOICE 2
    out["contamination"] = CONTAMINATION
    return out


# --- render -----------------------------------------------------------

def render_moves():
    lines = ["MOVE SET -- six moves, domain-agnostic", ""]
    for k, v in MOVES.items():
        lines.append("%s" % k)
        lines.append("  order line : %s" % v["order_line"])
        lines.append("  trigger    : %s" % v["trigger"])
        lines.append("  kinds      : %s" % ", ".join(v["kinds"]))
        lines.append("  ask        : %s" % v["ask"])
        lines.append("  absence is : %s" % v["absence_is"])
        lines.append("")
    lines.append("EARNED verdicts (1.0 each): %s" % ", ".join(EARNED))
    lines.append("A correctly-refused verdict scores as high as a correct")
    lines.append("one. Neither scores on prose alone.")
    return "\n".join(lines)


def render(out):
    L = ["MOVE SET v2 -- score", "=" * 62,
         "artifact : %s" % out["artifact"],
         "sha256   : %s" % out["artifact_sha256"]]
    if "artifact_unchanged" in out:
        L.append("pinned   : %s" % ("unchanged" if out["artifact_unchanged"]
                                    else "CHANGED SINCE PIN -- see CHOICE 2"))
    L.append("order    : %s" % ", ".join(out["order"] or []))
    L.append("")
    L.append("%-26s %-8s %-26s %5s" % ("move", "kind", "verdict", "pts"))
    L.append("-" * 70)
    for r in out["rows"]:
        L.append("%-26s %-8s %-26s %5.1f" % (
            r["move_id"], r["kind"] or "--", r["verdict"], r["points"]))
        L.append("      %s" % (r["detail"] or ""))
        if r["coverage"] is not None:
            L.append("      coverage: %.4f of artifact lines searched" % r["coverage"])
        if r["confidence"]:
            L.append("      confidence (unscored): %s" % r["confidence"])
    L.append("-" * 70)
    L.append("total %.1f of %.1f" % (out["total"], out["possible"]))
    L.append("moves not run   : %s" % (", ".join(out["moves_not_run"]) or "none"))
    L.append("absence fraction: %s" % out["absence_fraction"])
    L.append("")
    L.append(out["note"])
    if out.get("contamination"):
        L.append("")
        L.append(out["contamination"])
    return "\n".join(L)


def choices_report():
    L = ["CHOICES -- points the order left open", "=" * 62]
    for k in sorted(CHOICES):
        L.append("[CHOICE %d] %s" % (k, CHOICES[k]))
        L.append("")
    return "\n".join(L)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "move_set_sim_v2.py carries no checks. "
            "Run: python3 test_move_set_v2.py\n")
        return 2
    if len(argv) > 1 and argv[1] == "--choices":
        print(choices_report())
    elif len(argv) > 2 and argv[1] == "--emit":
        seed = int(argv[argv.index("--seed") + 1]) if "--seed" in argv else None
        print(json.dumps(emit(argv[2], seed), indent=2))
    elif len(argv) > 3 and argv[1] == "--score":
        print(render(score(read_ledger(argv[2]), read_artifact(argv[3]))))
    elif len(argv) > 1 and argv[1] == "--demo":
        print(render(demo()))
    elif len(argv) > 3 and argv[1] == "--paths":
        art = read_artifact(argv[-1])
        print(json.dumps(path_dependence(
            [read_ledger(p) for p in argv[2:-1]], art), indent=2))
    else:
        print(render_moves())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
