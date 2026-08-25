#!/usr/bin/env python3
"""
scans -- scan two (companion absence) and scan three (header collision),
ranked by dependent count times downstream depth.

    scans.py two   WORKBOOK.xlsx --flags FLAGS.txt [--radius N]
    scans.py three WORKBOOK.xlsx
    scans.py --selftest

WHAT THIS TOOL DOES NOT DO, and it is the first thing to say: it does
not label a site. Every column is a count, a set, or a name lifted off
the sheet. There is no verdict column, no ordering by consequence, and
no vocabulary of grading -- no_severity.py runs over the emitted report
and the selftest fails if a word of it appears. The ranking sorts by how
far a cell propagates, which is arithmetic on the dependency graph, not
a claim about how much it matters. The reading stays with the operator.

[CHOICE 1] SCAN ONE IS NOT IN THE DELIVERY. Scan two begins "for every flagged
cell" and nothing upstream of it was specified, so the flag set is an
INPUT -- a plain list of Sheet!A1 addresses -- and running scan two
without one is refused rather than defaulted. `--all` exists, is
explicit, and prints its own provenance in the report header. Inventing
a flagging rule here would put a framing in the operator's mouth and
then rank it.

TEN PARAMETERS THE DELIVERY LEFT OPEN are marked [CHOICE] at their
definitions and listed in SPEC.md. Each has a stated default and a way
to override it. They are not hidden in the code: the report header
prints the ones that were in force for that run, because an absence
measured over a radius of 2 and one measured over a radius of 6 are
different readings.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import re
import sys

import no_severity
import sheetmodel
from sheetmodel import (CONSTANT_DATE, CYCLE, DERIVED, num_to_col)

HERE = os.path.dirname(os.path.abspath(__file__))

# [CHOICE 2] neighborhood radius. A block of this many rows and columns
# either side of the flagged cell. 2 covers the adjacent record above
# and below; it does not reach across a table.
DEFAULT_RADIUS = 2

# [CHOICE 3] neighborhood SHAPE. Not a square block. A block of radius 2
# fails on the fixture in this folder: the sd column of a six-column
# table sits three columns from the flagged cell, so a correctly built
# table reports its own variance sibling absent. Widening the radius is
# the wrong repair -- it reaches into the adjacent record instead.
#
# The shape that matches how these sheets are actually built is a cross:
#   - the whole of the flagged cell's ROW, which is one record
#   - the flagged cell's COLUMN within +/- radius rows, which is the
#     neighbouring records
#   - the label-row cell above EVERY column the row touched, because a
#     unit, an n and an sd are named in the header and carried as bare
#     numbers underneath
# A sheet holding two tables side by side over-reaches on the row axis.
# That is a stated limit, not a hidden one.
COMPANION_KINDS = ("unit", "date", "sample_size", "variance_sibling")

ABSENT = "ABSENT"
PRESENT = "PRESENT"
NOT_SEARCHED = "NOT_SEARCHED"


# ---------------------------------------------------------------- patterns

def load_patterns(path=None):
    path = path or os.path.join(HERE, "patterns.json")
    with open(path) as fh:
        raw = json.load(fh)
    out = {}
    for k in COMPANION_KINDS:
        out[k] = [re.compile(p, re.I) for p in raw.get(k, [])]
    return out, path


def _matches(text, pats):
    if not text:
        return False
    for p in pats:
        if p.search(text):
            return True
    return False


# ---------------------------------------------------------------- labels

def _is_text(cell):
    return cell is not None and cell.kind == "CONSTANT_TEXT"


def label_row(wb, sheet):
    """[CHOICE 4] the first row whose non-empty cells are majority text.

    Returns None when no row qualifies. None is not row 0: a sheet with
    no label row has its column labels NOT_SEARCHED, not absent.
    """
    maxr, maxc = wb.extent(sheet)
    for r in range(1, min(maxr, 20) + 1):
        cells = [wb.at(sheet, r, c) for c in range(1, maxc + 1)]
        cells = [c for c in cells if c is not None]
        if len(cells) < 2:
            continue
        if sum(1 for c in cells if _is_text(c)) * 2 > len(cells):
            return r
    return None


def label_col(wb, sheet, lrow):
    """[CHOICE 4] the first column, below the label row, majority text."""
    maxr, maxc = wb.extent(sheet)
    start = (lrow or 0) + 1
    for c in range(1, min(maxc, 20) + 1):
        cells = [wb.at(sheet, r, c) for r in range(start, maxr + 1)]
        cells = [x for x in cells if x is not None]
        if len(cells) < 2:
            continue
        if sum(1 for x in cells if _is_text(x)) * 2 > len(cells):
            return c
    return None


def sheet_labels(wb, sheet):
    lrow = label_row(wb, sheet)
    lcol = label_col(wb, sheet, lrow)
    return lrow, lcol


# ---------------------------------------------------------------- scan two

def load_flags(path):
    """Sheet!A1 per line. '#' comments and blanks skipped."""
    out = []
    with open(path) as fh:
        for raw in fh:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if "!" not in line:
                raise ValueError(
                    "flag line %r has no sheet qualifier. Expected Sheet!A1"
                    % raw.strip())
            sh, addr = line.rsplit("!", 1)
            out.append((sh.strip().strip("'"), addr.strip().upper()))
    return out


def block_last_row(wb, sheet, lrow):
    """Last row of the contiguous block under the label row.

    A fully empty row ends the block. Used to decide whether a flagged
    cell is under the label row at all: a stray number eight rows below
    a table is not carrying that table's header, and reading it as
    though it were would report a unit PRESENT that nobody wrote for it.
    """
    if lrow is None:
        return None
    maxr, maxc = wb.extent(sheet)
    last = lrow
    r = lrow + 1
    while r <= maxr:
        if not any(wb.at(sheet, r, c) is not None for c in range(1, maxc + 1)):
            break
        last = r
        r += 1
    return last


def neighborhood(wb, key, radius):
    """(cells, unsearched). See CHOICE 3 for the shape.

    `unsearched` names what the search could not cover: N or S when the
    row band ran off the sheet, no-col-label when the cell sits outside
    any label block, no-row-label when the sheet has no label column. An
    ABSENT measured without a header is a different reading from an
    ABSENT measured with one, and the two must not print alike.
    """
    sheet, addr = key
    r, c = sheetmodel.rc(addr)
    maxr, maxc = wb.extent(sheet)
    lrow, lcol = sheet_labels(wb, sheet)
    unsearched = []
    found = {}
    cols_touched = set([c])

    for cc in range(1, maxc + 1):
        if cc == c:
            continue
        x = wb.at(sheet, r, cc)
        if x is not None:
            found[x.addr] = x
            cols_touched.add(cc)

    if r - radius < 1:
        unsearched.append("N")
    if r + radius > maxr:
        unsearched.append("S")
    for rr in range(max(1, r - radius), min(maxr, r + radius) + 1):
        if rr == r or rr == lrow:
            # The label row is reached by the label rule below or not at
            # all. Letting the band reach it would mean a large radius
            # silently supplies a header the block rule just withheld,
            # and the two halves of the report would disagree.
            continue
        x = wb.at(sheet, rr, c)
        if x is not None:
            found[x.addr] = x

    last = block_last_row(wb, sheet, lrow)
    under_labels = lrow is not None and lrow < r <= last
    if under_labels:
        for cc in sorted(cols_touched):
            x = wb.at(sheet, lrow, cc)
            if x is not None:
                found[x.addr] = x
    else:
        unsearched.append("no-col-label")
    if lcol is None:
        unsearched.append("no-row-label")
    if r == lrow or c == lcol:
        # The flagged cell is itself a label. Companion states are still
        # computed and still printed -- this marks the row rather than
        # suppressing it, because deciding that a header is not a site
        # is the operator's reading. It is here because with --all most
        # of the absences on a tidy sheet are label cells, and a report
        # that does not say so reads as a report about the data.
        unsearched.append("is-label")

    found.pop(addr, None)
    return list(found.values()), unsearched


def companion_states(cells, patterns):
    """Per kind: ABSENT, PRESENT, or NOT_SEARCHED.

    NOT_SEARCHED fires when the pattern file registers nothing for that
    kind. Without it a kind with an empty list reads ABSENT everywhere,
    which is a report of the pattern file rather than of the sheet.
    """
    texts = []
    has_date_cell = False
    for x in cells:
        if x.kind == CONSTANT_DATE:
            has_date_cell = True
        if isinstance(x.value, str):
            texts.append(x.value)
    out = {}
    for kind in COMPANION_KINDS:
        pats = patterns.get(kind) or []
        if not pats:
            out[kind] = NOT_SEARCHED
            continue
        hit = any(_matches(t, pats) for t in texts)
        if kind == "date" and has_date_cell:
            hit = True
        out[kind] = PRESENT if hit else ABSENT
    return out


def scan_two(wb, flags, radius=DEFAULT_RADIUS, patterns=None):
    patterns = patterns if patterns is not None else load_patterns()[0]
    rows = []
    for key in flags:
        cell = wb.cells.get(key)
        cells, unsearched = neighborhood(wb, key, radius)
        states = companion_states(cells, patterns)
        rows.append({
            "site": "%s!%s" % key,
            "kind": cell.kind if cell else "EMPTY",
            "pdepth": wb.precedent_depth(key) if cell else 0,
            "deps": len(wb.dependents().get(key, ())),
            "ddepth": wb.downstream_depth(key),
            "rank": wb.rank(key),
            "absent": [k for k in COMPANION_KINDS if states[k] == ABSENT],
            "not_searched": [k for k in COMPANION_KINDS
                             if states[k] == NOT_SEARCHED],
            "unsearched": unsearched,
            "n_neighbors": len(cells),
        })
    return rows


# -------------------------------------------------------------- scan three

# [CHOICE 5] normalization. Case, surrounding whitespace, internal
# whitespace runs, and leading/trailing punctuation. NOT parentheticals:
# "unit price (USD)" and "unit price" stay distinct, because deciding
# that a unit annotation does not change what a label names is a
# judgement about the sheet and belongs to the operator.
_PUNCT = " \t\r\n:;,.-_*#"


def normalize(label):
    s = re.sub(r"\s+", " ", (label or "").strip())
    return s.strip(_PUNCT).casefold()


def governed(wb, sheet, r, c, axis, lrow, lcol):
    """Cells a label governs. Column labels govern down, row labels right."""
    maxr, maxc = wb.extent(sheet)
    out = []
    if axis == "column":
        for rr in range((lrow or r) + 1, maxr + 1):
            x = wb.at(sheet, rr, c)
            if x is not None:
                out.append(x)
    else:
        for cc in range((lcol or c) + 1, maxc + 1):
            x = wb.at(sheet, r, cc)
            if x is not None:
                out.append(x)
    return out


def _construction(cells):
    """[CHOICE 6] composition, printed. Counts, for the operator to read.

    A majority vote would report a column of nine constants and one
    formula identically to a column of ten constants, and that single
    formula is the whole of what 'same name, different construction'
    is about.
    """
    nc = sum(1 for x in cells if x.kind.startswith("CONSTANT"))
    nd = sum(1 for x in cells if x.kind == DERIVED)
    parts = []
    if nc:
        parts.append("%dc" % nc)
    if nd:
        parts.append("%dd" % nd)
    return "+".join(parts) or "0"


def _construction_key(cells):
    """[CHOICE 6] what the LISTING decision is taken on: the kind set.

    Not the counts. Two sheets of a flat reference table carry the same
    headers over different numbers of rows, and comparing "12c" against
    "9c" lists every shared header on a difference in TABLE HEIGHT. That
    fired on a two-sheet fixture shaped like the target this criterion
    was written for, and it would have fired on the target -- as a
    finding, with a rank beside it.

    The delivery asks whether the cells are constants versus derived.
    Whether is a set. The counts stay in the printed column, so nine
    constants and one formula still reads differently from ten
    constants, which is the distinction the composition was for.
    """
    nc = any(x.kind.startswith("CONSTANT") for x in cells)
    nd = any(x.kind == DERIVED for x in cells)
    return "c+d" if (nc and nd) else ("d" if nd else "c")


def _depths(wb, cells):
    ds = set()
    for x in cells:
        ds.add(wb.precedent_depth(x.key))
    nums = sorted(d for d in ds if d != CYCLE)
    toks = [str(d) for d in nums]
    if CYCLE in ds:
        toks.append(CYCLE)
    return "{%s}" % ",".join(toks) if toks else "{}"


def _span(cells):
    if not cells:
        return "-"
    rs = [x.row for x in cells]
    cs = [x.col for x in cells]
    a = num_to_col(min(cs)) + str(min(rs))
    b = num_to_col(max(cs)) + str(max(rs))
    return a if a == b else "%s:%s" % (a, b)


def scan_three(wb, norm=normalize):
    groups = {}
    for sheet in wb.sheets:
        lrow, lcol = sheet_labels(wb, sheet)
        maxr, maxc = wb.extent(sheet)
        seen = []
        if lrow:
            for c in range(1, maxc + 1):
                x = wb.at(sheet, lrow, c)
                if _is_text(x):
                    seen.append((x, "column", lrow, c))
        if lcol:
            for r in range(1, maxr + 1):
                if lrow and r == lrow:
                    continue
                x = wb.at(sheet, r, lcol)
                if _is_text(x):
                    seen.append((x, "row", r, lcol))
        for x, axis, r, c in seen:
            cells = governed(wb, sheet, r, c, axis, lrow, lcol)
            if not cells:
                continue
            key = (norm(x.value), axis)
            groups.setdefault(key, []).append({
                "sheet": sheet,
                "at": "%s!%s" % (sheet, x.addr),
                "raw": x.value,
                "span": "%s!%s" % (sheet, _span(cells)),
                "depths": _depths(wb, cells),
                "construction": _construction(cells),
                "ckey": _construction_key(cells),
                "rank": _group_rank(wb, cells),
            })
    rows, same = [], 0
    for (label, axis), occ in sorted(groups.items()):
        if len(occ) < 2:
            continue
        differs = (len(set(o["depths"] for o in occ)) > 1
                   or len(set(o["ckey"] for o in occ)) > 1)
        if not differs:
            same += 1
            continue
        rows.append({
            "label": label,
            "axis": axis,
            "n": len(occ),
            "occurrences": occ,
            "rank": sum(o["rank"] for o in occ),
        })
    return rows, same, len(groups)


def _group_rank(wb, cells):
    """[CHOICE 9] a group's rank is the SUM over the cells it governs.

    A maximum would report a label governing one far-reaching cell and a
    label governing forty of them at the same height.
    """
    tot = 0
    for x in cells:
        v = wb.rank(x.key)
        if v == CYCLE:
            continue
        tot += v
    return tot


# ---------------------------------------------------------------- render

def _rankkey(v):
    return (0, 0) if v == CYCLE else (1, v)


def table(headers, rows):
    widths = [len(h) for h in headers]
    body = []
    for r in rows:
        cells = [str(x) for x in r]
        body.append(cells)
        for i, c in enumerate(cells):
            if len(c) > widths[i]:
                widths[i] = len(c)
    fmt = "  ".join("%-" + str(w) + "s" for w in widths)
    out = [fmt % tuple(headers), fmt % tuple("-" * w for w in widths)]
    for cells in body:
        out.append((fmt % tuple(cells)).rstrip())
    return "\n".join(out)


def render_two(wb, rows, radius, patterns_path, flag_source):
    rows = sorted(rows, key=lambda r: (_rankkey(r["rank"]), r["site"]),
                  reverse=True)
    head = [
        "scan two -- companion absence",
        "workbook        %s" % os.path.basename(wb.path or "-"),
        "reader          %s" % wb.reader,
        "flag source     %s" % flag_source,
        "radius          %d rows and columns, plus the two governing labels"
        % radius,
        "patterns        %s" % os.path.basename(patterns_path),
        "companions      %s" % ", ".join(COMPANION_KINDS),
        "rank            direct dependents x downstream depth",
        "",
        "absent       searched the neighborhood, no match",
        "not_searched no pattern registered for that companion",
        "unsearched   N/S row band ran off the sheet; no-col-label the",
        "             cell sits outside any label block; no-row-label the",
        "             sheet has no label column",
        "",
    ]
    body = table(
        ["rank", "site", "kind", "pdepth", "deps", "ddepth", "nbrs",
         "absent", "not_searched", "unsearched"],
        [[r["rank"], r["site"], r["kind"], r["pdepth"], r["deps"],
          r["ddepth"], r["n_neighbors"],
          ",".join(r["absent"]) or "-",
          ",".join(r["not_searched"]) or "-",
          ",".join(r["unsearched"]) or "-"] for r in rows])
    tail = ["", "flagged cells: %d   with at least one absent companion: %d"
            % (len(rows), sum(1 for r in rows if r["absent"]))]
    return "\n".join(head + [body] + tail)


def render_three(wb, rows, same, total):
    rows = sorted(rows, key=lambda r: (_rankkey(r["rank"]), r["label"]),
                  reverse=True)
    head = [
        "scan three -- header collision",
        "workbook        %s" % os.path.basename(wb.path or "-"),
        "reader          %s" % wb.reader,
        "sheets          %s" % ", ".join(wb.sheets),
        "normalization   case, whitespace, edge punctuation; parentheticals kept",
        "grouped on      normalized label and axis",
        "listed when     depth sets differ, or the kind set differs",
        "rank            sum over governed cells of dependents x downstream depth",
        "",
        "depths       set of precedent depths of the cells the label governs",
        "construction Nc = N constants, Nd = N derived",
        "",
    ]
    body_rows = []
    for r in rows:
        for i, o in enumerate(r["occurrences"]):
            body_rows.append([
                r["rank"] if i == 0 else "",
                r["label"] if i == 0 else "",
                r["axis"] if i == 0 else "",
                o["raw"], o["at"], o["span"], o["depths"], o["construction"]])
    body = table(["rank", "label", "axis", "as written", "label at",
                  "governs", "depths", "construction"], body_rows)
    tail = ["", "label groups with two or more occurrences: %d"
            % (len(rows) + same),
            "of those, listed: %d   not listed, construction and depths "
            "agree: %d" % (len(rows), same),
            "distinct labels seen: %d" % total]
    return "\n".join(head + [body] + tail)


# ---------------------------------------------------------------- selftest

def _selftest():
    import tempfile
    import fixture
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-52s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("scans selftest")
    d = tempfile.mkdtemp()
    path = fixture.write_demo(os.path.join(d, "t.xlsx"))
    wb = sheetmodel.read(path)
    pats, ppath = load_patterns()

    ck("label row found", sheet_labels(wb, "Inputs")[0], 1)
    ck("label col found", sheet_labels(wb, "Inputs")[1], 1)

    # --- scan two -------------------------------------------------------
    flags = [("Inputs", "B2"), ("Inputs", "B9"), ("Model", "D2")]
    rows = {r["site"]: r for r in scan_two(wb, flags, 2, pats)}

    # A cell with a unit in its header, a date, an n and an sd beside it
    # reports nothing missing. Without this case the scan passes by
    # reporting everything absent everywhere.
    ck("well-companioned cell reports nothing absent",
       rows["Inputs!B2"]["absent"], [])
    ck("lone cell reports all four absent",
       rows["Inputs!B9"]["absent"], list(COMPANION_KINDS))
    ck("derived cell in a bare block reports all four absent",
       rows["Model!D2"]["absent"], list(COMPANION_KINDS))
    ck("nothing not_searched when patterns are loaded",
       rows["Inputs!B2"]["not_searched"], [])

    empty = {k: [] for k in COMPANION_KINDS}
    r0 = scan_two(wb, [("Inputs", "B2")], 2, empty)[0]
    ck("empty pattern list is NOT_SEARCHED not ABSENT",
       (r0["absent"], r0["not_searched"]), ([], list(COMPANION_KINDS)))

    ck("row band clipping reported", "N" in rows["Inputs!B2"]["unsearched"], True)
    ck("a cell outside any label block says so",
       "no-col-label" in rows["Inputs!B9"]["unsearched"], True)

    # The radius is load-bearing and the report must be able to show it.
    # The radius decides the reading, and the fixture carries the case:
    # a bare "n = 12" note three rows below the flagged cell.
    wide = scan_two(wb, [("Inputs", "B9")], 3, pats)[0]
    ck("radius 2 does not reach the note",
       "sample_size" in rows["Inputs!B9"]["absent"], True)
    ck("radius 3 does",
       "sample_size" in wide["absent"], False)

    ck("rank of a propagating input",
       rows["Inputs!B2"]["rank"], 3)
    ck("rank of a terminal", rows["Model", ] if False else
       scan_two(wb, [("Summary", "B2")], 2, pats)[0]["rank"], 0)

    # --- scan three -----------------------------------------------------
    three, same, total = scan_three(wb)
    listed = {(r["label"], r["axis"]): r for r in three}
    ck("'total' collides across three sheets",
       ("total", "column") in listed, True)
    ck("'total' has three occurrences",
       listed[("total", "column")]["n"], 3)
    ck("constructions differ across them",
       sorted(o["construction"] for o in listed[("total", "column")]["occurrences"]),
       ["2c", "2d", "2d"])
    ck("depth sets differ across them",
       len(set(o["depths"] for o in listed[("total", "column")]["occurrences"])), 3)

    # 'item' appears on all three sheets governing text constants at the
    # same depth. A scan that lists it is listing repetition, not
    # collision.
    ck("'item' repeats and is NOT listed", ("item", "column") in listed, False)

    # Table height must not list a header. Two flat sheets sharing their
    # headers over different numbers of rows agree in construction and
    # differ in count; before CHOICE 6 took the kind set, every shared
    # header was listed on that difference alone -- on a fixture shaped
    # like the workbook the criterion in targets/ was written for.
    def _flat(name, n):
        r = {"A1": ("t", "Fuel Type"), "B1": ("t", "CO2 Factor (kg CO2/mmBtu)")}
        for i in range(2, n + 2):
            r["A%d" % i] = ("t", "Fuel %d" % (i - 1))
            r["B%d" % i] = ("n", "%d" % (90 + i))
        return (name, r)
    flat = sheetmodel.read(fixture.write_demo(
        os.path.join(d, "flat.xlsx"), [_flat("A", 12), _flat("B", 9)]))
    fl, fsame, _t = scan_three(flat)
    ck("differing table heights list nothing",
       len(fl), 0)
    ck("the shared headers are counted as agreeing, not dropped",
       fsame >= 2, True)
    ca = governed(flat, "A", 1, 2, "column", 1, 1)
    cb = governed(flat, "B", 1, 2, "column", 1, 1)
    ck("the printed counts differ and the kind sets do not",
       (_construction(ca), _construction(cb),
        _construction_key(ca) == _construction_key(cb)),
       ("12c", "9c", True))
    ck("a mixed column still separates from a pure one",
       _construction_key(ca) == _construction_key(ca + [
           sheetmodel.Cell("A", "Z9", sheetmodel.DERIVED, None, "=A1",
                           set(), set())]), False)
    ck("a same-construction group is counted, not dropped", same >= 1, True)

    ck("row-axis collision found", ("widget", "row") in listed, True)

    # --- the unit list, against hand-set answers -----------------------
    # Fixed before any real workbook was read. The negatives are the
    # half that matters: a loose unit pattern produces a false PRESENT,
    # which removes a row from a report about what is missing.
    unit_cases = [
        ("Heat Content (mmBtu/short ton)", True),
        ("CO2 Factor (kg CO2/mmBtu)", True),
        ("Electricity (kWh)", True),
        ("unit price (USD)", True),
        ("Natural Gas (therms)", True),
        ("Emissions (mt CO2e)", True),
        ("Total (see note 3)", False),
        ("Fuel Type", False),
        ("Scope 1", False),
        ("Notes (revised)", False),
    ]
    ck("unit patterns, 10 hand-set cases",
       [t for t, want in unit_cases
        if _matches(t, pats["unit"]) != want], [])

    # --- what --all costs, measured rather than asserted ---------------
    # The argument for CHOICE 1 is that the flag set decides the report.
    # This pins the composition so it cannot drift out from under that
    # claim: on a tidy three-sheet workbook most absences under --all
    # are label cells and strays, not values in a table.
    every = scan_two(wb, sorted(wb.cells), 2, pats)
    with_abs = [r for r in every if r["absent"]]
    lab = [r for r in with_abs if "is-label" in r["unsearched"]]
    stray = [r for r in with_abs
             if "no-col-label" in r["unsearched"]
             and "is-label" not in r["unsearched"]]
    intable = [r for r in with_abs
               if "is-label" not in r["unsearched"]
               and "no-col-label" not in r["unsearched"]]
    ck("--all: rows, absences, labels, strays, in-table",
       (len(every), len(with_abs), len(lab), len(stray), len(intable)),
       (38, 23, 13, 2, 8))
    ck("a flag list of five yields four, all in-table",
       len([r for r in scan_two(wb, [("Inputs", "B2"), ("Inputs", "B9"),
                                     ("Model", "D2"), ("Model", "C2"),
                                     ("Summary", "B2")], 2, pats)
            if r["absent"]]), 4)

    # Normalization is a choice with a consequence, and the fixture
    # carries the case: these two are NOT grouped.
    ck("parenthetical kept distinct",
       normalize("unit price (USD)") == normalize("unit price"), False)
    ck("case and spacing folded",
       normalize("  Unit   Price :") == normalize("unit price"), True)

    # --- the output constraint -----------------------------------------
    t2 = render_two(wb, scan_two(wb, flags, 2, pats), 2, ppath, "selftest list")
    t3 = render_three(wb, *scan_three(wb))
    ck("scan two output carries no screened word",
       no_severity.check(t2)[0], True)
    ck("scan three output carries no screened word",
       no_severity.check(t3)[0], True)
    ck("the screen would fire if it drifted",
       no_severity.check(t2 + "\nthis site is an error")[0], False)

    # --- the refusal ----------------------------------------------------
    try:
        load_flags(os.path.join(d, "nope.txt"))
        ck("missing flag file raises", False, True)
    except IOError:
        ck("missing flag file raises", True, True)
    fp = os.path.join(d, "f.txt")
    open(fp, "w").write("# a comment\n\nInputs!B9\nModel!D2  # trailing\n")
    ck("flags parsed", load_flags(fp), [("Inputs", "B9"), ("Model", "D2")])
    open(fp, "w").write("B9\n")
    try:
        load_flags(fp)
        ck("unqualified flag raises", False, True)
    except ValueError:
        ck("unqualified flag raises", True, True)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


# ---------------------------------------------------------------- cli

USAGE = """usage:
  scans.py two   WORKBOOK.xlsx --flags FLAGS.txt [--radius N] [--patterns P.json]
  scans.py two   WORKBOOK.xlsx --all             [--radius N] [--patterns P.json]
  scans.py three WORKBOOK.xlsx
  scans.py --selftest

FLAGS.txt is one Sheet!A1 per line; '#' begins a comment.
Scan two has no flagging rule of its own. See SPEC.md, choice 1."""


def _arg(argv, name, default=None):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return default


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(USAGE)
        return 2
    mode, path = argv[1], argv[2]
    wb = sheetmodel.read(path)
    if mode == "three":
        out = render_three(wb, *scan_three(wb))
    elif mode == "two":
        pats, ppath = load_patterns(_arg(argv, "--patterns"))
        radius = int(_arg(argv, "--radius", DEFAULT_RADIUS))
        fpath = _arg(argv, "--flags")
        if fpath:
            flags = load_flags(fpath)
            src = os.path.basename(fpath) + " (%d cells)" % len(flags)
        elif "--all" in argv:
            flags = sorted(wb.cells)
            src = "--all: every non-empty cell, no upstream scan"
        else:
            sys.stderr.write(
                "scan two takes a flag list. Scan one is not part of this\n"
                "tool, so there is no flagging rule to fall back on.\n"
                "Pass --flags FILE, or --all to state that the flag set is\n"
                "every cell.\n")
            return 2
        out = render_two(wb, scan_two(wb, flags, radius, pats),
                         radius, ppath, src)
    else:
        print(USAGE)
        return 2
    clean, hits = no_severity.check(out)
    print(out)
    if not clean:
        sys.stderr.write("\n" + no_severity.report(out, "emitted table") + "\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
