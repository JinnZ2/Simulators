#!/usr/bin/env python3
"""
scan4 -- stated-relationship maintenance.

    scan4.py run BOOK.xlsx [--tolerance R] [--verbose]
    scan4.py rate BOOK.xlsx [BOOK2.xlsx ...]
    scan4.py --selftest

Work order 4. Independent of scans 1-3: those read structure, this one
reads what the workbook SAYS about its own numbers and checks whether
the file still does it.

The occasion is SSS_032. The UNFCCC workbook states at
`Info and sources!E10` that the Palestine grid factor is the average of
five named neighbours, and the cell reproduces that mean to 1.1e-16 --
as a VALUE. No formula maintains it. The relationship is a record of how
the number was produced, and nothing in the file would show if it
stopped being true.

FOUR BINS AND NO SCORE. A stated relationship whose target is a formula
is MAINTAINED; a constant that still satisfies it is
HOLDS_UNMAINTAINED; a constant that does not is DIVERGED; operands that do
not resolve are NOT_TESTABLE. The bins are the finding. There is no
aggregate, no ranking, and DIVERGED is not called an error -- a workbook
may have every reason to hold a number that no longer matches the note
beside it, and that reading is the operator's.

WHAT AN UNTESTABLE RELATIONSHIP MUST NOT DO IS SCORE. If an operand
names something outside the workbook -- a published index, a national
dataset -- the relationship is NOT_TESTABLE and stops there. Falling
through to a comparison would turn "we cannot check this" into "this
is broken", which is the failure the fixtures guard hardest.

CC0. stdlib plus the reader. Parses under Python 3.9. ASCII only.
"""

import math
import os
import re
import sys

import no_severity
import sheetmodel
from sheetmodel import CONSTANT_NUMBER, CONSTANT_TEXT, DERIVED

# [CHOICE 1] a sheet carries provenance prose if its NAME or its label
# row contains one of these. Keyword, not fixed sheet name, per S1.
PROVENANCE_WORDS = ("info", "source", "sources", "note", "notes", "method",
                    "methodology", "reference", "references", "assumption",
                    "assumptions", "provenance", "documentation")

# [CHOICE 2] relative tolerance. Printed with every run; never compared
# against without being stated.
DEFAULT_TOLERANCE = 1e-9

# [CHOICE 3] a cell is prose rather than a label if it is text and longer
# than this. A four-word column header is not a stated relationship.
PROSE_MIN_CHARS = 25

MAINTAINED = "MAINTAINED"
HOLDS_UNMAINTAINED = "HOLDS_UNMAINTAINED"
DIVERGED = "DIVERGED"
NOT_TESTABLE = "NOT_TESTABLE"
NOT_ARITHMETIC = "NOT_ARITHMETIC"
BINS = (MAINTAINED, HOLDS_UNMAINTAINED, DIVERGED, NOT_TESTABLE)

# The no-labelling constraint (S8) is enforced by no_severity over every
# emitted report, exactly as scan two and scan three are.
#
# THE EXEMPTION IS EMPTY, and that is the point of the amendment. The bin
# was BROKEN, which put a screened word in the delivered vocabulary and
# bought an exemption to carry it. Renaming it DIVERGED -- "the cell and
# the stated relation differ", no ruling on which is wrong and no damage
# asserted -- removes the need for one: no token in this order fires, so
# no file fires, and nothing is masked.
#
# The three-arm harness below stays. It is the right structure for a real
# exemption later, and with an empty list it still runs: arm one requires
# a clean report, arm two requires that nothing fires unmasked (which is
# now the same statement, and stops being the same the moment a token is
# added), arm three plants a grading word and requires it caught. Keeping
# a harness with nothing to exempt costs three checks and means the next
# exemption arrives measured instead of argued.
DELIVERED_VOCABULARY = ()


def screened(text):
    """(clean, hits) with the delivered bin vocabulary masked."""
    masked = text
    for tok in DELIVERED_VOCABULARY:
        masked = masked.replace(tok, "#" * len(tok))
    return no_severity.check(masked)


def exemption_is_only_the_bin(text):
    """True if every hit in the unmasked report is a delivered bin token.

    With an empty vocabulary this is "nothing fires at all". It is kept
    separate from screened() because masking a token would also hide any
    sentence containing it, and that hole has to be visible the moment a
    token is added rather than discovered then.
    """
    toks = tuple(t.lower() for t in DELIVERED_VOCABULARY)
    for _, word, _ in no_severity.hits(text):
        if word.lower() not in toks:
            return False
    return True


# ---------------------------------------------------------------- S2

def _mean(v):
    return sum(v) / float(len(v))


def _median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def _quartile(v, upper):
    """Nearest-rank, and the rule is printed with the verdict.

    Quartile has several conventions and they disagree on small samples.
    Naming the one used is the difference between a comparison and a
    coincidence.
    """
    s = sorted(v)
    k = 0.75 if upper else 0.25
    i = max(0, min(len(s) - 1, int(math.ceil(k * len(s))) - 1))
    return s[i]


OPS = {
    "mean": (_mean, "arithmetic mean"),
    "average": (_mean, "arithmetic mean"),
    "sum": (lambda v: sum(v), "sum"),
    "product": (lambda v: math.prod(v), "product"),
    "median": (_median, "median"),
    "upper quartile": (lambda v: _quartile(v, True),
                       "upper quartile, nearest-rank"),
    "lower quartile": (lambda v: _quartile(v, False),
                       "lower quartile, nearest-rank"),
    "quartile": (None, "quartile, side unstated"),
    "ratio": (lambda v: v[0] / v[1] if len(v) == 2 and v[1] else None,
              "ratio, first over second"),
    "times": (lambda v: math.prod(v), "product"),
    "weighted by": (None, "weighted, weights unstated"),
    "scaled by": (lambda v: math.prod(v), "product"),
}

# Longest first, so "upper quartile" is not read as "quartile".
_OP_RE = re.compile(
    r"\b(" + "|".join(sorted((re.escape(k) for k in OPS), key=len,
                             reverse=True)) + r")\b", re.I)

# Provenance that is not arithmetic. Counted, not tested, per S2.
_NONARITH = re.compile(
    r"\b(estimated from|based on|sourced from|taken from|derived from|"
    r"according to|see |published|dataset|report|version|edition|"
    r"[0-9]{4})\b", re.I)


def _split_operands(text):
    """Fallback split, used only when no index is available.

    Commas only. NOT on "and": the workbook this was built for names
    "Antigua and Barbuda", "Bonaire, Sint Eustatius and Saba" and
    "Heard Island and McDonald Islands", so splitting on "and" -- or on
    every comma -- invents operands that were never written. The
    index-driven split below is the real one.
    """
    return [p for p in (q.strip(" \t\r\n.;:") for q in text.split(","))
            if p]


_KEYPAT = {}


def _keypat(key):
    """A key match that tolerates the workbook's own double spaces.

    Matching on the ORIGINAL text rather than a whitespace-collapsed
    copy keeps offsets aligned, so the name that comes back is the one
    the prose actually wrote -- casing, spacing and all. A normalized
    name would be this tool's rendering of the operand rather than the
    workbook's.
    """
    if key not in _KEYPAT:
        _KEYPAT[key] = re.compile(
            r"\s+".join(re.escape(t) for t in key.split()) + r"(?=$|[\s,.;:])",
            re.I)
    return _KEYPAT[key]


def split_by_index(text, idx):
    """Split a written list using the WORKBOOK's own vocabulary.

    A comma-separated list of names whose members contain commas and
    "and" cannot be split by punctuation, and guessing the boundaries
    invents operands. So the split is RESOLVED rather than guessed: at
    each position take the longest label the workbook itself carries.
    Text that matches nothing is emitted as written, comma-split, and
    goes on to fail resolution -- which is the honest outcome, not a
    silent repair.

    Returns (names, how) where `how` records how many were matched
    against the index and how many were left as fragments.
    """
    if not idx:
        return _split_operands(text), {"by_index": 0, "fragments": 0}
    keys = sorted(idx, key=len, reverse=True)
    by_first = {}
    for k in keys:
        if k:
            by_first.setdefault(k[:1].lower(), []).append(k)
    names, i, matched, frags = [], 0, 0, 0
    n = len(text)
    while i < n:
        if text[i] in " \t\r\n,.;:":
            i += 1
            continue
        best = None
        for k in by_first.get(text[i].lower(), ()):
            m = _keypat(k).match(text, i)
            if m:
                best = m
                break
        if best:
            names.append(text[i:best.end()])
            matched += 1
            i = best.end()
            continue
        j = text.find(",", i)
        j = n if j < 0 else j
        frag = text[i:j].strip(" \t\r\n.;:")
        if frag:
            names.append(frag)
            frags += 1
        i = j + 1
    return names, {"by_index": matched, "fragments": frags}


def extract(prose, idx=None):
    """S2. Arithmetic relationships only, recorded as written.

    A relationship may carry MORE THAN ONE target: the workbook this was
    built for states one average for twenty-two territories at once, and
    each is a separate claim about a separate cell.
    """
    out = []
    for m in _OP_RE.finditer(prose):
        op = m.group(1).lower()
        # operands: after the following " of ", to the sentence end
        tail = prose[m.end():]
        mo = re.match(r"\s*(?:\w+\s+){0,3}?\bof\b\s*(.+)", tail,
                      re.S | re.I)
        if not mo:
            # The operator is stated and no operands follow it. That is a
            # stated relationship with an empty operand list, not an
            # absence of one -- the workbook this was built for says
            # "All hotels upper quartile emission factor value", where
            # the distribution is a published index and is nowhere in
            # the file. Recording it as NOT_ARITHMETIC would let an
            # untestable relationship leave the count entirely.
            out.append({
                "operator": op,
                "operator_reads": OPS[op][1],
                "operands_as_written": [],
                "operand_split": {"by_index": 0, "fragments": 0},
                "targets_as_written": [],
                "target_split": {"by_index": 0, "fragments": 0},
                "no_operand_clause": True,
                "quoted": (prose[max(0, m.start() - 40):m.end() + 90]
                           .replace("\n", " ")),
            })
            continue
        rest = mo.group(1)
        cut = re.search(r"\.(?:\s|$)", rest)
        operand_text = rest[:cut.start()] if cut else rest
        # target: what precedes the colon before the operator
        head = prose[:m.start()]
        seg = re.split(r"(?<=[.;])\s", head)[-1]
        tgt_text = ""
        if ":" in seg:
            tgt_text = seg.rsplit(":", 1)[0]
        tgt_text = re.sub(r"^\s*(for|the)\s+", "", tgt_text, flags=re.I)
        ops_names, ops_how = split_by_index(operand_text, idx)
        tgt_names, tgt_how = (split_by_index(tgt_text, idx) if tgt_text
                              else ([], {"by_index": 0, "fragments": 0}))
        out.append({
            "operator": op,
            "operator_reads": OPS[op][1],
            "operands_as_written": ops_names,
            "operand_split": ops_how,
            "targets_as_written": tgt_names,
            "target_split": tgt_how,
            "quoted": (prose[max(0, m.start() - 40):m.end() + 90]
                       .replace("\n", " ")),
        })
    return out


def classify_prose(prose):
    """Arithmetic, or counted and left alone."""
    if _OP_RE.search(prose):
        return "ARITHMETIC"
    return NOT_ARITHMETIC


# ---------------------------------------------------------------- S1

def provenance_sheets(wb):
    """By keyword, in the sheet name or in the label row. Not by name."""
    out = []
    for sh in wb.sheets:
        why = None
        low = sh.lower()
        if any(w in low for w in PROVENANCE_WORDS):
            why = "sheet name contains %r" % next(
                w for w in PROVENANCE_WORDS if w in low)
        else:
            maxr, maxc = wb.extent(sh)
            for r in range(1, min(maxr, 12) + 1):
                labels = [wb.at(sh, r, c) for c in range(1, maxc + 1)]
                txt = " ".join(str(x.value).lower() for x in labels
                               if x is not None and x.kind == CONSTANT_TEXT)
                hit = next((w for w in PROVENANCE_WORDS if w in txt), None)
                if hit and len(txt) > 8:
                    why = "row %d label contains %r" % (r, hit)
                    break
        if why:
            out.append((sh, why))
    return out


def prose_cells(wb, sheet):
    return [c for c in wb.sheet_cells(sheet)
            if c.kind == CONSTANT_TEXT
            and len(str(c.value)) >= PROSE_MIN_CHARS]


# ---------------------------------------------------------------- S3

def _norm(s):
    s = re.sub(r"\s+", " ", str(s)).strip().strip(".,;:")
    return s.casefold()


def build_index(wb):
    """label text -> [(cell, value)] for every text cell with a number beside it.

    The number is the nearest numeric cell to the right on the same row.
    """
    idx = {}
    for sh in wb.sheets:
        maxr, maxc = wb.extent(sh)
        for c in wb.sheet_cells(sh):
            if c.kind != CONSTANT_TEXT:
                continue
            for cc in range(c.col + 1, min(c.col + 4, maxc) + 1):
                v = wb.at(sh, c.row, cc)
                if v is None:
                    continue
                if v.kind in (CONSTANT_NUMBER, DERIVED):
                    idx.setdefault(_norm(c.value), []).append((v, c))
                break
    return idx


def resolve(name, idx, prefer_sheet=None):
    """S3. Ambiguity is not guessed.

    SCOPE, declared rather than assumed: when the target resolves on
    one sheet, operands are looked for on that sheet first. A country
    name in this workbook is a grid factor on one sheet and a hotel
    factor on another, and unscoped it is ambiguous for a reason that
    has nothing to do with the relationship being tested. Scoping is
    not guessing -- the rule is stated, applied to every operand alike,
    printed with the verdict, and the ambiguity guard survives inside
    the scope: two candidates on the target's own sheet are still
    AMBIGUOUS.

    Exact match first. Failing that, a UNIQUE whole-name containment
    match -- the prose says "Palestine" where the sheet says "State of
    Palestine" -- and the report records that the match was by
    containment rather than exactly. More than one containment match is
    AMBIGUOUS with the candidates listed, never a pick.

    Two candidates with DIFFERENT values are NOT_TESTABLE with both
    listed. Two candidates with the same value are not an ambiguity --
    the answer does not depend on which is chosen -- and that is stated
    rather than left as a silent tie-break.
    """
    key = _norm(name)
    hits = idx.get(key, [])
    how = "exact"
    if prefer_sheet and hits:
        scoped = [h for h in hits if h[0].sheet == prefer_sheet]
        if scoped:
            hits = scoped
            how = "exact, scoped to %r" % prefer_sheet
    if not hits and len(key) >= 4:
        cands = [k for k in idx
                 if re.search(r"(^|\W)%s($|\W)" % re.escape(key), k)]
        if len(cands) == 1:
            hits = idx[cands[0]]
            how = "containment: %r matched %r" % (name, cands[0])
            if prefer_sheet:
                scoped = [h for h in hits if h[0].sheet == prefer_sheet]
                if scoped:
                    hits = scoped
                    how += ", scoped to %r" % prefer_sheet
        elif len(cands) > 1:
            return {"state": "AMBIGUOUS", "name": name,
                    "candidates": ["label %r" % c for c in cands[:6]],
                    "how": "containment, %d candidates" % len(cands)}
    if not hits:
        return {"state": "UNRESOLVED", "name": name, "candidates": []}
    vals = []
    for v, lab in hits:
        try:
            vals.append(float(v.value))
        except (TypeError, ValueError):
            vals.append(None)
    distinct = sorted(set(x for x in vals if x is not None))
    cands = ["%s = %r" % (v.ref(), v.value) for v, _ in hits]
    if len(distinct) > 1:
        return {"state": "AMBIGUOUS", "name": name, "candidates": cands}
    if not distinct:
        return {"state": "NOT_NUMERIC", "name": name, "candidates": cands}
    return {"state": "OK", "name": name, "cell": hits[0][0],
            "value": distinct[0], "candidates": cands, "how": how,
            "same_value_duplicates": len(hits) - 1}


# ---------------------------------------------------------------- S4

def test_relationship(wb, rel, idx, tolerance):
    """S4. One row per TARGET; a relationship may state several."""
    fn = OPS[rel["operator"]][0]
    rows = []
    targets = rel["targets_as_written"] or [None]
    for tname in targets:
        tr = resolve(tname, idx) if tname else {"state": "UNRESOLVED",
                                                "name": None,
                                                "candidates": []}
        # Operands are scoped to the sheet the target resolved on. The
        # rule is declared here and printed with every row.
        scope = tr["cell"].sheet if tr.get("state") == "OK" else None
        ops = [resolve(n, idx, scope) for n in rel["operands_as_written"]]
        bad = [o for o in ops if o["state"] != "OK"]
        row = {"operator": rel["operator"],
               "operator_reads": rel["operator_reads"],
               "target_as_written": tname,
               "n_operands": len(rel["operands_as_written"]),
               "scope": scope,
               "quoted": rel["quoted"]}
        if fn is None:
            row.update(bin=NOT_TESTABLE,
                       why="the operator is stated without the part that "
                           "would make it computable: %s"
                           % rel["operator_reads"])
            rows.append(row)
            continue
        if tr["state"] != "OK":
            row.update(bin=NOT_TESTABLE,
                       why="the target %r did not resolve (%s)"
                           % (tname, tr["state"]),
                       unresolved=[{"name": tname, "state": tr["state"],
                                    "candidates": tr["candidates"]}])
            rows.append(row)
            continue
        if not rel["operands_as_written"]:
            row.update(bin=NOT_TESTABLE,
                       why="the operator is stated and no operands are "
                           "named in the prose, so there is nothing in "
                           "this workbook to recompute from. Where the "
                           "distribution is external the relationship is "
                           "untestable from the file alone, and an "
                           "untestable relationship does not score.")
            rows.append(row)
            continue
        if bad or not ops:
            row.update(bin=NOT_TESTABLE,
                       why="%d of %d operands did not resolve in this "
                           "workbook" % (len(bad) or 1, len(ops)),
                       unresolved=[{"name": o["name"], "state": o["state"],
                                    "candidates": o["candidates"]}
                                   for o in bad][:6])
            rows.append(row)
            continue
        try:
            expect = fn([o["value"] for o in ops])
        except (ZeroDivisionError, ValueError, TypeError):
            expect = None
        if expect is None:
            row.update(bin=NOT_TESTABLE,
                       why="the stated operation did not evaluate on the "
                           "resolved operands")
            rows.append(row)
            continue
        got = tr["value"]
        tcell = tr["cell"]
        delta = got - expect
        scale = max(abs(got), abs(expect), 1e-300)
        holds = abs(delta) <= tolerance * scale
        same_sheet = all(o["cell"].sheet == tcell.sheet for o in ops)
        row.update(target=tcell.ref(), target_kind=tcell.kind,
                   expected=expect, actual=got, delta=delta,
                   relative=abs(delta) / scale,
                   same_sheet=same_sheet,
                   operand_cells=[o["cell"].ref() for o in ops])
        if tcell.kind == DERIVED:
            row["bin"] = MAINTAINED
            row["why"] = ("the target is a formula, so the workbook "
                          "recomputes the stated relationship")
        elif holds:
            row["bin"] = HOLDS_UNMAINTAINED
            row["why"] = ("the target is a constant and still satisfies "
                          "the stated relationship; nothing in the file "
                          "maintains it")
        else:
            row["bin"] = DIVERGED
            row["why"] = ("the target is a constant and does not satisfy "
                          "the stated relationship at the stated tolerance")
            row["divergence"] = revision_history(wb)
        rows.append(row)
    return rows


def revision_history(wb):
    """S4's when-did-it-diverge, answered honestly.

    An .xlsx carries no per-cell history unless tracked changes are on,
    and this format keeps none by default. Saying so is the answer; a
    guess would be worse than the gap.
    """
    return ("UNRECOVERABLE: this file format carries no per-cell revision "
            "history, so the workbook cannot say when the value and the "
            "note stopped agreeing. A version series of the same workbook "
            "would bracket it.")


# ---------------------------------------------------------------- run

def scan(wb, tolerance=DEFAULT_TOLERANCE):
    idx = build_index(wb)
    sheets = provenance_sheets(wb)
    rows, nonarith, prose_n = [], 0, 0
    for sh, _why in sheets:
        for c in prose_cells(wb, sh):
            prose_n += 1
            if classify_prose(str(c.value)) == NOT_ARITHMETIC:
                nonarith += 1
                continue
            rels = extract(str(c.value), idx)
            if not rels:
                nonarith += 1
                continue
            for rel in rels:
                for row in test_relationship(wb, rel, idx, tolerance):
                    row["prose_cell"] = c.ref()
                    rows.append(row)
    fd = getattr(wb, "file_dates", {}) or {}
    return {"rows": rows, "sheets": sheets, "prose_cells": prose_n,
            "not_arithmetic": nonarith, "tolerance": tolerance,
            "workbook": os.path.basename(wb.path or "-"),
            "reader": getattr(wb, "reader", "-"),
            "capabilities": dict(getattr(wb, "capabilities", {})),
            "file_dates": fd,
            # S3 asks for "file date" and both containers record two,
            # eight years apart on the legacy target. Both are carried
            # and both are printed; the column names which is which
            # rather than picking one and calling it the file date.
            "version_date": ("%s / %s" % (fd.get("created", "?"),
                                          fd.get("modified", "?"))
                             if fd else "not stated")}


def bins(rows):
    out = dict((b, 0) for b in BINS)
    for r in rows:
        out[r["bin"]] = out.get(r["bin"], 0) + 1
    return out


# ---------------------------------------------------------------- render

def table(headers, rows):
    w = [len(h) for h in headers]
    body = [[str(x) for x in r] for r in rows]
    for r in body:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(c))
    fmt = "  ".join("%-" + str(x) + "s" for x in w)
    out = [fmt % tuple(headers), fmt % tuple("-" * x for x in w)]
    for r in body:
        out.append((fmt % tuple(r)).rstrip())
    return "\n".join(out)


def render(res, verbose=False):
    b = bins(res["rows"])
    L = ["scan 4 -- stated-relationship maintenance",
         "workbook          %s" % res["workbook"],
         "tolerance         %g relative, stated here and not hardcoded"
         % res["tolerance"],
         "provenance sheets %s" % ", ".join(
             "%s (%s)" % s for s in res["sheets"]) or "none found",
         "prose cells read  %d" % res["prose_cells"],
         "not arithmetic    %d  (counted, not tested)" % res["not_arithmetic"],
         "",
         "The four bins are the finding. There is no aggregate score and",
         "no ranking. A bin name is a description of what the file does,",
         "not a grade: a workbook may have every reason to hold a number",
         "the note beside it no longer describes. The reading stays with",
         "the operator.",
         ""]
    L.append(table(["bin", "count"], [[k, b[k]] for k in BINS]))
    L.append("")
    body = []
    for r in sorted(res["rows"], key=lambda r: (r["bin"],
                                                r.get("target") or "",
                                                r.get("target_as_written")
                                                or "")):
        body.append([r["bin"], r["prose_cell"], r["operator"],
                     r["n_operands"],
                     (r.get("target_as_written") or "-")[:26],
                     r.get("target") or "-",
                     "-" if r.get("expected") is None
                     else "%.10g" % r["expected"],
                     "-" if r.get("actual") is None
                     else "%.10g" % r["actual"],
                     "-" if r.get("relative") is None
                     else "%.3g" % r["relative"],
                     "-" if r.get("same_sheet") is None
                     else ("same" if r["same_sheet"] else "cross")])
    L.append(table(["bin", "prose", "op", "n", "target as written",
                    "target cell", "expected", "actual", "rel delta",
                    "operands"], body))
    for r in res["rows"]:
        if r["bin"] == DIVERGED:
            L += ["", "%s -- %s" % (r.get("target"),
                                    r.get("target_as_written")),
                  "  stated: %s" % r["operator_reads"],
                  "  quoted: ...%s..." % r["quoted"][:150],
                  "  expected %.17g, holds %.17g, delta %.6g"
                  % (r["expected"], r["actual"], r["delta"]),
                  "  when it diverged: %s" % r["divergence"]]
    if verbose:
        for r in res["rows"]:
            if r["bin"] == NOT_TESTABLE and r.get("unresolved"):
                L += ["", "%s NOT_TESTABLE: %s" % (r["prose_cell"], r["why"])]
                for u in r["unresolved"]:
                    L.append("    %r -> %s %s" % (u["name"], u["state"],
                                                  u["candidates"][:2]))
    return "\n".join(L)


# ---------------------------------------------------------------- S6

# Which scans stop when a capability is absent. Named here so the
# NOT_RUN list is derived from the reader's declaration rather than from
# a note somebody keeps up to date.
DEPENDENT_SCANS = {
    "formula_text": "coupling.py (elasticity by perturbation)",
    "precedents": "scan three depth, ranking",
    "cell_values": "scan four, coupling",
    "cell_kind": "scan two, scan three",
}


def operand_bins(res):
    """S3: operand count per relationship, and the bin it landed in.

    Grouped by (prose cell, operator, operand count) so one relationship
    stated over many targets is one row rather than twenty-one, with the
    target count kept. Returns [] when nothing is testable -- which is a
    state and is rendered as one, not as an absent section.
    """
    groups = {}
    for r in res["rows"]:
        k = (r["prose_cell"], r["operator"], r["n_operands"])
        g = groups.setdefault(k, {"bins": {}, "targets": 0})
        g["bins"][r["bin"]] = g["bins"].get(r["bin"], 0) + 1
        g["targets"] += 1
    out = []
    for (cell, op, n_ops), g in sorted(groups.items(),
                                       key=lambda kv: (-kv[0][2], kv[0][0])):
        out.append({"prose_cell": cell, "operator": op, "n_operands": n_ops,
                    "targets": g["targets"],
                    "bins": "  ".join("%s x%d" % (b, c)
                                      for b, c in sorted(g["bins"].items()))})
    return out


OUT_OF_SCOPE = "OUT_OF_SCOPE"


def scope_of(res):
    """WO7 S4. A workbook whose provenance prose states no relationship
    is OUT_OF_SCOPE, not a zero.

    It stays in the table -- the reader should see it and see its zero --
    and it never enters a denominator, because a workbook that cannot
    state a relationship is not evidence that relationships are or are
    not maintained. SSS_043 argued this in prose; this is the field.

    The stance test lives in selection.py and is imported rather than
    reimplemented, so the screen that admits a candidate and the emission
    that scores it cannot disagree about what RETROSPECTIVE means.
    """
    b = bins(res["rows"])
    # MAINTAINED counts. A workbook whose relationship IS enforced by a
    # formula is the most in-scope thing there is, and reading scope off
    # the share's denominator alone would call it out of scope -- which
    # is what the first version did, caught by the G1 fixture.
    if b[DIVERGED] + b[HOLDS_UNMAINTAINED] + b[MAINTAINED] > 0:
        return "IN_SCOPE"
    return OUT_OF_SCOPE


def diverged_share(res):
    """DIVERGED / (DIVERGED + HOLDS). None when nothing is testable.

    None is not zero. A workbook with no testable relationship has an
    EMPTY denominator, and returning 0.0 would put it at the good end of
    a scale it is not on -- the PCH_001 shape, and the twelfth instance
    of this repair in this repository.
    """
    b = bins(res["rows"])
    den = b[DIVERGED] + b[HOLDS_UNMAINTAINED]
    return None if not den else b[DIVERGED] / float(den)


def direction(results):
    """S3: two points give a direction, not a rate, and only if the sign
    is the same.

    Returns (verdict, why). The verdict is never a number.
    """
    shares = [(r["workbook"], diverged_share(r)) for r in results]
    have = [(w, v) for w, v in shares if v is not None]
    if len(have) < 2:
        missing = [w for w, v in shares if v is None]
        return ("NO_DIRECTION",
                "a direction takes two defined points and only %d in-scope "
                "workbook(s) have one%s"
                % (len(have),
                   (" (empty denominator: %s)" % ", ".join(missing))
                   if missing else ""))
    signs = set()
    for i in range(1, len(have)):
        d = have[i][1] - have[i - 1][1]
        signs.add(0 if d == 0 else (1 if d > 0 else -1))
    if len(signs) > 1:
        return ("NO_DIRECTION",
                "the steps do not share a sign, so no direction is stated")
    sgn = signs.pop()
    return (("FLAT" if sgn == 0 else
             ("HIGHER_IN_LATER" if sgn > 0 else "LOWER_IN_LATER")),
            "n = %d. A direction, not a rate." % len(have))


def rate(results):
    """S6 + S3. Accumulates across workbooks. n is stated on every
    emission, and no curve is emitted at any n reached here."""
    n = len(results)
    L = ["scan 4 -- cross-file, stated-relationship maintenance",
         "workbooks in this emission: n = %d" % n, ""]
    body = []
    tot = {"DIVERGED": 0, "HOLDS_UNMAINTAINED": 0}
    n_oos = 0
    for res in results:
        b = bins(res["rows"])
        # OUT_OF_SCOPE stays in the table and out of the sum. Skipping
        # the whole loop body here would drop the row, which is the
        # opposite of what S4 asks for -- and is what the first version
        # of this did.
        if scope_of(res) == OUT_OF_SCOPE:
            n_oos += 1
        else:
            tot["DIVERGED"] += b[DIVERGED]
            tot["HOLDS_UNMAINTAINED"] += b[HOLDS_UNMAINTAINED]
        ops = [r["n_operands"] for r in res["rows"]]
        cross = sum(1 for r in res["rows"] if r.get("same_sheet") is False)
        sh = diverged_share(res)
        scope = scope_of(res)
        body.append([res["workbook"], res.get("version_date", "not stated"),
                     scope, res.get("reader", "-"),
                     b[MAINTAINED], b[HOLDS_UNMAINTAINED], b[DIVERGED],
                     b[NOT_TESTABLE],
                     "%.3g" % (sum(ops) / float(len(ops))) if ops else "-",
                     cross,
                     ("out of scope" if scope == OUT_OF_SCOPE else
                      ("empty denominator" if sh is None
                       else "%.3f" % sh))])
    L.append(table(["workbook", "created / modified", "scope", "reader",
                    "MAINT", "HOLDS",
                    "DIVERGED", "NOT_TEST", "mean operands", "cross-sheet",
                    "DIVERGED/(D+H)"], body))
    caps = [(r["workbook"], r.get("capabilities", {})) for r in results]
    missing = [(w, k) for w, c in caps for k, v in sorted(c.items())
               if v is False]
    if missing:
        L += ["", "Reader capabilities not available, and the scans that",
              "depend on them are NOT_RUN rather than substituted (S1):",
              ""]
        L.append(table(["workbook", "capability", "scans NOT_RUN"],
                       [[w, k, DEPENDENT_SCANS.get(k, "-")]
                        for w, k in missing]))

    L += ["", "Operand count per relationship, and the bin it landed in.",
          "One row per stated relationship, not per target.", ""]
    any_rel = False
    for res in results:
        ob = operand_bins(res)
        L.append("  %s" % res["workbook"])
        if not ob:
            L.append("    no testable relationship stated in this workbook")
        else:
            any_rel = True
            L.append("    " + table(
                ["prose cell", "operator", "operands", "targets", "bins"],
                [[o["prose_cell"], o["operator"], o["n_operands"],
                  o["targets"], o["bins"]] for o in ob]
            ).replace("\n", "\n    "))
        L.append("")

    in_scope = [r for r in results if scope_of(r) != OUT_OF_SCOPE]
    verdict, why = direction(in_scope)
    L += ["direction across the emission: %s" % verdict, "  %s" % why]

    den = tot["DIVERGED"] + tot["HOLDS_UNMAINTAINED"]
    L += ["", "pooled DIVERGED/(DIVERGED+HOLDS_UNMAINTAINED): %s"
          % ("empty denominator" if not den
             else "%.3f" % (tot["DIVERGED"] / float(den))),
          "  over %d in-scope workbook(s); %d out of scope, in the table"
          % (len(results) - n_oos, n_oos),
          "  above and in no denominator here (S4)."]
    L += ["",
          "NO CURVE IS REPORTED. n = %d. A decay curve takes a series of"
          % n,
          "workbooks with version dates; two points give a direction and",
          "a point is not a rate."]
    if not any_rel:
        L += ["", "No workbook in this emission states a testable",
              "relationship, so nothing here bears on operand count."]
    return "\n".join(L)


# ---------------------------------------------------------------- fixtures

def _g_sheets(which):
    """G1, G3, G4 as small workbooks. G2 and G5 are the real file."""
    notes = {"A1": ("t", "Notes and sources"),
             "A2": ("t", "Item"), "B2": ("t", "Value")}
    data = {"A1": ("t", "Country"), "B1": ("t", "Factor")}
    if which == "G1":
        for i, (n, v) in enumerate([("Alpha", 2.0), ("Beta", 4.0),
                                    ("Gamma", 6.0)], start=2):
            data["A%d" % i] = ("t", n)
            data["B%d" % i] = ("n", str(v))
        data["A5"] = ("t", "Delta")
        data["B5"] = ("f", "AVERAGE(B2:B4)", 4.0)
        notes["A3"] = ("t", "note")
        notes["B3"] = ("t", "For Delta: Average of Alpha, Beta, Gamma.")
    elif which == "G3":
        for i, (n, v) in enumerate([("Alpha", 2.0), ("Beta", 4.0),
                                    ("Gamma", 99.0)], start=2):
            data["A%d" % i] = ("t", n)
            data["B%d" % i] = ("n", str(v))
        data["A5"] = ("t", "Delta")
        data["B5"] = ("n", "4.0")     # was the mean before Gamma was edited
        notes["A3"] = ("t", "note")
        notes["B3"] = ("t", "For Delta: Average of Alpha, Beta, Gamma.")
    elif which == "G4":
        data["A2"] = ("t", "Alpha")
        data["B2"] = ("n", "2.0")
        data["A3"] = ("t", "Delta")
        data["B3"] = ("n", "5.0")
        notes["A3"] = ("t", "note")
        notes["B3"] = ("t", "For Delta: Average of Alpha, Omega, Zeta.")
    return [("Info and sources", notes), ("Data", data)]


def fixture_workbook(which, path):
    import fixture
    return sheetmodel.read(fixture.write_demo(path, _g_sheets(which)))


# ---------------------------------------------------------------- selftest

def _selftest():
    import tempfile
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("scan4 selftest")
    d = tempfile.mkdtemp()

    # S2 extraction, on the shape the real workbook uses.
    rels = extract("For Palestine: Average EF of Iraq, Jordan, Lebanon, "
                   "Syrian Arab Republic, Turkey. For Holy See: Italy EF")
    ck("one arithmetic relationship extracted", len(rels), 1)
    ck("the operator is read", rels[0]["operator"], "average")
    ck("the operands are recorded as written",
       rels[0]["operands_as_written"],
       ["Iraq", "Jordan", "Lebanon", "Syrian Arab Republic", "Turkey"])
    ck("and the target too", rels[0]["targets_as_written"], ["Palestine"])
    ck("non-arithmetic provenance is classified, not parsed",
       classify_prose("Full set of factors for kg CO2e from DEFRA"),
       NOT_ARITHMETIC)
    ck("a date-only note is not arithmetic",
       classify_prose("2020 Cornell Hotel Sustainability Benchmarking "
                      "Index"), NOT_ARITHMETIC)

    # G1: formula target.
    r1 = scan(fixture_workbook("G1", os.path.join(d, "g1.xlsx")))
    ck("G1 is MAINTAINED", [x["bin"] for x in r1["rows"]], [MAINTAINED])

    # G3: constant, one operand edited afterwards.
    r3 = scan(fixture_workbook("G3", os.path.join(d, "g3.xlsx")))
    ck("G3 is DIVERGED", [x["bin"] for x in r3["rows"]], [DIVERGED])
    g3 = r3["rows"][0]
    ck("G3 reports the delta",
       (round(g3["expected"], 6), g3["actual"], round(g3["delta"], 6)),
       (35.0, 4.0, -31.0))
    ck("and says the divergence date is unrecoverable",
       "UNRECOVERABLE" in g3["divergence"], True)

    # G4: an operand that is not in the workbook.
    r4 = scan(fixture_workbook("G4", os.path.join(d, "g4.xlsx")))
    ck("G4 is NOT_TESTABLE", [x["bin"] for x in r4["rows"]], [NOT_TESTABLE])
    ck("G4 names what did not resolve and guesses nothing",
       sorted(u["name"] for u in r4["rows"][0]["unresolved"]),
       ["Omega", "Zeta"])
    ck("G4 emits no expected value",
       r4["rows"][0].get("expected"), None)

    # S1 by keyword, not by fixed name.
    wb1 = fixture_workbook("G1", os.path.join(d, "g1b.xlsx"))
    ck("the provenance sheet is found", [s[0] for s in
                                         provenance_sheets(wb1)],
       ["Info and sources"])

    # S3 ambiguity.
    idx = {"x": [(type("C", (), {"ref": lambda s: "A!B1", "value": "1.0",
                                 "kind": CONSTANT_NUMBER, "sheet": "A"})(),
                  None),
                 (type("C", (), {"ref": lambda s: "B!B1", "value": "2.0",
                                 "kind": CONSTANT_NUMBER, "sheet": "B"})(),
                  None)]}
    ck("two candidates with different values is AMBIGUOUS, not a guess",
       resolve("x", idx)["state"], "AMBIGUOUS")

    # G5. The operator is stated, the distribution is external, and the
    # relationship must NOT reach a testable verdict. S8 names this as
    # the selftest requirement.
    g5 = extract("Hotel Carbon Footprint Per Occupied Room | All hotels "
                 "upper quartile emission factor value", {})
    ck("G5 extracts a relationship rather than dropping it", len(g5), 1)
    ck("with the operator read and no operands named",
       (g5[0]["operator"], g5[0]["operands_as_written"]),
       ("upper quartile", []))
    g5rows = test_relationship(None, g5[0], {}, DEFAULT_TOLERANCE)
    ck("G5 is NOT_TESTABLE", [r["bin"] for r in g5rows], [NOT_TESTABLE])
    ck("G5 produces no testable verdict",
       any(r["bin"] in (DIVERGED, HOLDS_UNMAINTAINED, MAINTAINED)
           for r in g5rows), False)
    ck("and no expected value is emitted for it",
       g5rows[0].get("expected"), None)

    # S6 refuses a curve from one workbook.
    ck("n=1 emits no curve and says so",
       "NO CURVE IS REPORTED" in rate([r1]), True)
    ck("and n is stated", "n = 1" in rate([r1]), True)

    # ---- WO7 S4: an out-of-scope workbook stays in the TABLE and out
    # of the DENOMINATOR. Both halves asserted, because the first
    # implementation of this dropped the row entirely.
    _oos = {"rows": [{"bin": NOT_TESTABLE, "prose_cell": "S!A1",
                      "operator": "times", "n_operands": 0,
                      "same_sheet": True}],
            "sheets": [], "prose_cells": 1, "not_arithmetic": 0,
            "tolerance": 1e-9, "workbook": "empty.xlsx",
            "reader": "stub", "capabilities": {}, "file_dates": {},
            "version_date": "-"}
    ck("a workbook with nothing testable is OUT_OF_SCOPE",
       scope_of(_oos), OUT_OF_SCOPE)
    ck("and one with a testable row is not", scope_of(r1), "IN_SCOPE")
    _both = rate([r1, _oos])
    ck("the out-of-scope workbook stays in the table",
       "empty.xlsx" in _both, True)
    ck("and is named out of scope there", "out of scope" in _both, True)
    ck("and is excluded from the pooled denominator",
       "1 out of scope" in _both, True)
    ck("a direction is not stated from one in-scope point",
       "NO_DIRECTION" in _both, True)

    # S8, the no-labelling constraint, enforced over what is emitted.
    # Two arms, because a one-armed exemption check passes on a screen
    # that hides everything.
    emitted = render(r1, True) + "\n" + rate([r1])
    ck("the emitted report is clean under the (empty) exemption",
       screened(emitted)[0], True)
    ck("and nothing fires unmasked, the exemption list being empty",
       exemption_is_only_the_bin(emitted), True)
    ck("a planted grading word is caught through the exemption",
       screened(emitted + "\nthis cell is wrong")[0], False)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  scan4.py run  BOOK.xlsx [--tolerance R] [--verbose]
  scan4.py rate BOOK.xlsx [BOOK2.xlsx ...]
  scan4.py --selftest"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(USAGE)
        return 2
    tol = DEFAULT_TOLERANCE
    if "--tolerance" in argv:
        tol = float(argv[argv.index("--tolerance") + 1])
    paths = [a for a in argv[2:] if not a.startswith("--")
             and not a.replace(".", "").replace("e", "").replace("-", "")
             .isdigit()]
    if argv[1] == "run":
        wb = sheetmodel.read(paths[0])
        print(render(scan(wb, tol), "--verbose" in argv))
        return 0
    if argv[1] == "rate":
        print(rate([scan(sheetmodel.read(p), tol) for p in paths]))
        return 0
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
