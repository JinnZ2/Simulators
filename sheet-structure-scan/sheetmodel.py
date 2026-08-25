#!/usr/bin/env python3
"""
sheetmodel -- read a workbook into cells and a precedent graph.

The reader budget declared in SPEC.md is "stdlib plus one spreadsheet
reader". This module spends NONE of it: .xlsx is a zip of XML, formulas
live in xl/worksheets/sheetN.xml as <f> elements, and zipfile plus
xml.etree reach them. The one-reader slot stays open for a format this
cannot read.

That is not only frugal. The two scans need FORMULAS -- precedent depth
and constant-versus-derived are both properties of the formula layer --
and the common reader's value-only mode drops them. Reading the XML
directly means the layer under test cannot be silently discarded by the
reader.

WHAT IS NOT READ, stated rather than discovered later:
  - named ranges and structured table references. A formula using one
    records PRECEDENTS_UNRESOLVED for that term.
  - external workbook links ([1]Sheet1!A1). Recorded as EXTERNAL, never
    followed.
  - array formulas beyond their anchor cell. A cell carrying an <f>
    with no text and no resolvable shared master is still DERIVED, and
    records SHARED_MASTER_MISSING. It is never read as a constant: the
    first version of this reader did exactly that and turned 347 of one
    real workbook's 476 formula cells into constants.
  - merged regions: the anchor carries the value, the covered cells read
    empty. Scan two reports that as NOT_SEARCHED, not as absent.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS_PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"

# [CHOICE 8] a range wider than this is not expanded into per-cell edges.
# Stated because the alternative -- expanding silently -- turns one
# SUM(A1:A100000) into a hundred thousand edges and the rank column
# becomes a measure of range width.
RANGE_CELL_CAP = 4096

EMPTY = "EMPTY"
CONSTANT_NUMBER = "CONSTANT_NUMBER"
CONSTANT_TEXT = "CONSTANT_TEXT"
CONSTANT_DATE = "CONSTANT_DATE"
DERIVED = "DERIVED"

CYCLE = "CYCLE"
UNRESOLVED = "PRECEDENTS_UNRESOLVED"
TRUNCATED = "PRECEDENTS_TRUNCATED"
EXTERNAL = "EXTERNAL"
SHARED_MASTER_MISSING = "SHARED_MASTER_MISSING"

# Builtin number-format ids that are dates or times.
BUILTIN_DATE_IDS = set(list(range(14, 23)) + list(range(45, 48)))


# ---------------------------------------------------------------- addresses

def col_to_num(col):
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n


def num_to_col(n):
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def split_addr(addr):
    """'B12' -> ('B', 12). Dollar signs dropped."""
    m = re.match(r"^\$?([A-Z]{1,3})\$?(\d+)$", addr.upper())
    if not m:
        return None
    return m.group(1), int(m.group(2))


def rc(addr):
    """'B12' -> (12, 2), row and column as integers."""
    p = split_addr(addr)
    if p is None:
        return None
    return p[1], col_to_num(p[0])


# ---------------------------------------------------------------- formulas

# A cell reference: optional sheet qualifier, then A1 or A1:B9.
# The negative lookahead on '(' keeps LOG10( and similar function names
# out; the lookbehind keeps them out of the middle of an identifier.
_REF = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"(?:(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_.]*))!)?"
    r"(\$?[A-Z]{1,3}\$?[0-9]+)"
    r"(?::(\$?[A-Z]{1,3}\$?[0-9]+))?"
    # Not followed by more of an identifier, and not followed by an open
    # paren. Both are needed: without the first, LOG10( backtracks to
    # "LOG1" and is read as a cell reference, which the selftest caught.
    r"(?![A-Za-z0-9_.])"
    r"(?!\s*\()"
)
_STRLIT = re.compile(r'"[^"]*"')


def _mask_strings(text):
    """Blank out string literals, PRESERVING LENGTH so spans still line up.

    parse_precedents can use a shorter mask because it only reads spans
    on the masked copy. shift_formula edits the ORIGINAL by span, so the
    mask has to be the same length or every edit after the first string
    literal lands in the wrong place.
    """
    return _STRLIT.sub(lambda m: '"' + " " * (len(m.group(0)) - 2) + '"', text)


def _shift_ref(ref, drow, dcol):
    """Move one A1 reference. A $ pins that half and it does not move."""
    m = re.match(r"^(\$?)([A-Z]{1,3})(\$?)([0-9]+)$", ref.upper())
    if not m:
        return ref
    cabs, col, rabs, row = m.groups()
    c = col_to_num(col) + (0 if cabs else dcol)
    r = int(row) + (0 if rabs else drow)
    if c < 1 or r < 1:
        return "#REF!"
    return "%s%s%s%d" % (cabs, num_to_col(c), rabs, r)


def shift_formula(text, drow, dcol):
    """Translate a formula's relative references by (drow, dcol).

    This is what a shared formula is. The master cell carries the text
    once and every follower carries only the group index, inheriting the
    same formula with its relative references moved. A reader that does
    not do this reads 347 of a real workbook's 476 formula cells as
    constants -- which is what happened, and it is the whole of why this
    function exists.
    """
    if not text or (drow == 0 and dcol == 0):
        return text
    masked = _mask_strings(text)
    edits = []
    for m in _REF.finditer(masked):
        for gi in (3, 4):
            if m.group(gi):
                edits.append((m.start(gi), m.end(gi),
                              _shift_ref(m.group(gi), drow, dcol)))
    out = text
    for a, b, rep in sorted(edits, reverse=True):
        out = out[:a] + rep + out[b:]
    return out
_EXTERNAL = re.compile(r"\[\d+\]")


def parse_precedents(formula, home_sheet):
    """Cell references in a formula.

    Returns (set of (sheet, addr), set of note strings). Notes carry the
    states that are not a reference: EXTERNAL, TRUNCATED. A term this
    parser cannot resolve to cells is UNRESOLVED and is reported rather
    than dropped -- an unread precedent and a cell with no precedents
    must not land in the same bucket.
    """
    notes = set()
    if not formula:
        return set(), notes
    body = _mask_strings(formula)
    if _EXTERNAL.search(body):
        notes.add(EXTERNAL)
    out = set()
    consumed = []
    for m in _REF.finditer(body):
        sheet = m.group(1) or m.group(2) or home_sheet
        a1, a2 = m.group(3), m.group(4)
        consumed.append((m.start(), m.end()))
        if a2 is None:
            out.add((sheet, a1.replace("$", "").upper()))
            continue
        r1, c1 = rc(a1)
        r2, c2 = rc(a2)
        rlo, rhi = min(r1, r2), max(r1, r2)
        clo, chi = min(c1, c2), max(c1, c2)
        n = (rhi - rlo + 1) * (chi - clo + 1)
        if n > RANGE_CELL_CAP:
            notes.add(TRUNCATED)
            continue
        for r in range(rlo, rhi + 1):
            for c in range(clo, chi + 1):
                out.add((sheet, num_to_col(c) + str(r)))
    # A bare name that is not a function call and not a reference is a
    # named range or a table column: unresolved, not absent.
    stripped = body
    for s, e in sorted(consumed, reverse=True):
        stripped = stripped[:s] + " " * (e - s) + stripped[e:]
    for nm in re.finditer(r"(?<![A-Za-z0-9_.])[A-Za-z_][A-Za-z0-9_.]{1,}", stripped):
        tail = stripped[nm.end():].lstrip()
        if tail.startswith("("):
            continue
        if nm.group(0).upper() in ("TRUE", "FALSE"):
            continue
        notes.add(UNRESOLVED)
        break
    return out, notes


# ---------------------------------------------------------------- cells

class Cell(object):
    __slots__ = ("sheet", "addr", "row", "col", "kind", "value",
                 "formula", "precedents", "notes")

    def __init__(self, sheet, addr, kind, value, formula, precedents, notes):
        self.sheet = sheet
        self.addr = addr
        r, c = rc(addr)
        self.row, self.col = r, c
        self.kind = kind
        self.value = value
        self.formula = formula
        self.precedents = precedents
        self.notes = notes

    @property
    def key(self):
        return (self.sheet, self.addr)

    def ref(self):
        return "%s!%s" % (self.sheet, self.addr)

    def __repr__(self):
        return "<Cell %s %s>" % (self.ref(), self.kind)


# ---------------------------------------------------------------- reader

def _text(el):
    return "".join(el.itertext()) if el is not None else ""


def _date_style_ids(z):
    """Style indices whose number format is a date or time."""
    try:
        root = ET.fromstring(z.read("xl/styles.xml"))
    except KeyError:
        return set()
    custom = {}
    for nf in root.iter(NS + "numFmt"):
        fid = int(nf.get("numFmtId"))
        code = nf.get("formatCode") or ""
        bare = re.sub(r'"[^"]*"', "", code)
        bare = re.sub(r"\[[^\]]*\]", "", bare)
        if re.search(r"[ymdhs]", bare, re.I):
            custom[fid] = True
    out = set()
    xfs = root.find(NS + "cellXfs")
    if xfs is None:
        return out
    for i, xf in enumerate(list(xfs)):
        fid = int(xf.get("numFmtId") or 0)
        if fid in BUILTIN_DATE_IDS or custom.get(fid):
            out.add(i)
    return out


def _shared_strings(z):
    try:
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return [_text(si) for si in root.findall(NS + "si")]


def _sheet_targets(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    by_id = {}
    for rel in rels.iter(NS_PKG + "Relationship"):
        t = rel.get("Target")
        if t.startswith("/"):
            t = t[1:]
        elif not t.startswith("xl/"):
            t = "xl/" + t
        by_id[rel.get("Id")] = t
    out = []
    for sh in wb.iter(NS + "sheet"):
        rid = sh.get(NS_R + "id")
        out.append((sh.get("name"), by_id.get(rid)))
    return out


class Workbook(object):
    """Cells plus the precedent graph over them."""

    def __init__(self, cells, sheets, path=None, reader="stdlib-xlsx"):
        self.cells = {c.key: c for c in cells}
        self.sheets = sheets
        self.path = path
        self.reader = reader
        self.capabilities = {"cell_values": True, "cell_kind": True,
                             "precedents": True, "formula_text": True}
        self.file_dates = {}
        self._dependents = None
        self._pdepth = None
        self._ddepth = None

    # -- graph ----------------------------------------------------------

    def dependents(self):
        """Direct dependents. Reverse of the precedent edges."""
        if self._dependents is None:
            d = {}
            for c in self.cells.values():
                for p in c.precedents:
                    d.setdefault(p, set()).add(c.key)
            self._dependents = d
        return self._dependents

    def _longest(self, key, edges, memo, stack):
        if key in memo:
            return memo[key]
        if key in stack:
            return CYCLE
        stack.add(key)
        best = 0
        for nxt in edges.get(key, ()):  # missing key -> no edges
            sub = self._longest(nxt, edges, memo, stack)
            if sub == CYCLE:
                stack.discard(key)
                memo[key] = CYCLE
                return CYCLE
            if sub + 1 > best:
                best = sub + 1
        stack.discard(key)
        memo[key] = best
        return best

    def precedent_depth(self, key):
        """Longest path back to a cell with no precedents.

        [CHOICE 10] a constant is 0. A cycle returns CYCLE, not a number -- the
        distinction between "measured zero" and "not measurable here" is
        the one this repo has had to repair a dozen times, and it is
        free at construction.
        """
        if self._pdepth is None:
            self._pdepth = {}
            self._pedges = {k: set(c.precedents) & set(self.cells)
                            for k, c in self.cells.items()}
        return self._longest(key, self._pedges, self._pdepth, set())

    def downstream_depth(self, key):
        """Longest path forward along dependents. A terminal is 0."""
        if self._ddepth is None:
            self._ddepth = {}
        return self._longest(key, self.dependents(), self._ddepth, set())

    def rank(self, key):
        """dependent count times downstream depth.

        [CHOICE 7] dependent count is DIRECT dependents, not transitive.
        Transitive count and downstream depth measure overlapping things,
        so their product double-counts the same reach. Direct x depth
        keeps the two factors independent: how many cells read this one,
        and how far the furthest chain from it runs.

        A cell in a cycle has no finite depth; rank is CYCLE, which sorts
        apart from every number rather than to the top or the bottom.
        """
        n = len(self.dependents().get(key, ()))
        d = self.downstream_depth(key)
        if d == CYCLE:
            return CYCLE
        return n * d

    # -- access ---------------------------------------------------------

    def sheet_cells(self, sheet):
        return [c for c in self.cells.values() if c.sheet == sheet]

    def at(self, sheet, row, col):
        if row < 1 or col < 1:
            return None
        return self.cells.get((sheet, num_to_col(col) + str(row)))

    def extent(self, sheet):
        cs = self.sheet_cells(sheet)
        if not cs:
            return (0, 0)
        return (max(c.row for c in cs), max(c.col for c in cs))


def read_xlsx(path):
    """Read an .xlsx into a Workbook. stdlib only."""
    cells = []
    sheets = []
    with zipfile.ZipFile(path) as z:
        shared_strings = _shared_strings(z)
        datestyles = _date_style_ids(z)
        for name, target in _sheet_targets(z):
            if not target:
                continue
            sheets.append(name)
            root = ET.fromstring(z.read(target))

            # Pass 1: the shared-formula masters. A master carries the
            # text once, tagged with a group index; every follower in the
            # group carries the index and nothing else.
            shared = {}
            for c in root.iter(NS + "c"):
                f = c.find(NS + "f")
                if f is None or f.get("t") != "shared":
                    continue
                si = f.get("si")
                body = _text(f)
                if si is not None and body and si not in shared:
                    shared[si] = (c.get("r"), body)

            for c in root.iter(NS + "c"):
                addr = c.get("r")
                if not addr or rc(addr) is None:
                    continue
                t = c.get("t")
                s_i = c.get("s")
                f = c.find(NS + "f")
                v = c.find(NS + "v")
                isel = c.find(NS + "is")
                formula = _text(f) if f is not None else None
                notes = set()
                if f is not None and not formula:
                    # A follower, or an array formula outside its anchor.
                    si = f.get("si")
                    if si is not None and si in shared:
                        m_addr, m_text = shared[si]
                        mr, mc = rc(m_addr)
                        r_, c_ = rc(addr)
                        formula = shift_formula(m_text, r_ - mr, c_ - mc)
                    else:
                        formula = ""
                        notes.add(SHARED_MASTER_MISSING)
                if t == "s" and v is not None:
                    try:
                        value = shared_strings[int(v.text)]
                    except (ValueError, IndexError, TypeError):
                        value = None
                elif t == "inlineStr":
                    value = _text(isel)
                elif v is not None:
                    value = v.text
                else:
                    value = None
                if f is not None:
                    kind = DERIVED
                    prec, n2 = parse_precedents(formula, name)
                    notes |= n2
                elif value is None or value == "":
                    kind = EMPTY
                    prec = set()
                else:
                    prec = set()
                    if t in ("s", "str", "inlineStr"):
                        kind = CONSTANT_TEXT
                    elif s_i is not None and int(s_i) in datestyles:
                        kind = CONSTANT_DATE
                    else:
                        kind = CONSTANT_NUMBER
                if kind == EMPTY:
                    continue
                cells.append(Cell(name, addr, kind, value, formula, prec,
                                  notes))
    return Workbook(cells, sheets, path=path)


def xlsx_dates(path):
    """Dates docProps/core.xml records. Both, never one -- see the note
    in xlsreader.summary_dates: the WO6 legacy target's two are eight
    years apart, so the format that carries two is asked for two."""
    out = {}
    try:
        with zipfile.ZipFile(path) as z:
            if "docProps/core.xml" not in z.namelist():
                return out
            x = ET.fromstring(z.read("docProps/core.xml"))
    except Exception:
        return out
    for tag, key in (("created", "created"), ("modified", "modified")):
        for el in x.iter():
            if el.tag.endswith("}" + tag) and el.text:
                out[key] = el.text[:10]
                break
    return out


def read(path):
    """Dispatch on extension. The one-reader slot is spent here or not."""
    ext = os.path.splitext(path)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        w = read_xlsx(path)
        w.file_dates = xlsx_dates(path)
        return w
    if ext == ".xls":
        # Legacy BIFF8, work order 6 S1. Imported here rather than at
        # module scope because xlsreader imports this module. The one
        # spreadsheet reader beyond stdlib is STILL unspent: a .xls is a
        # compound-file container and struct reaches the records,
        # formulas included.
        import xlsreader
        return xlsreader.read_xls(path)
    if ext == ".doc":
        # Legacy binary Word. A document is not a workbook, so this
        # reader refuses it -- it has no cells, no formulas and no
        # precedent graph, and returning an empty Workbook would let a
        # caller read "no cells" as a fact about the file. Text comes
        # from docreader.read_doc(), which is built.
        raise NotImplementedError(
            "legacy .doc is a document, not a workbook: no cells, no "
            "formulas, no precedent graph. Text extraction is built and "
            "lives in docreader.read_doc(); this reader refuses rather "
            "than returning an empty Workbook a caller could misread.")
    raise NotImplementedError(
        "no reader for %s. The declared budget allows ONE spreadsheet "
        "reader beyond stdlib and it is unspent: install it and wire it "
        "here rather than widening this module." % ext)


# ---------------------------------------------------------------- selftest

def _selftest():
    import tempfile
    import fixture
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-46s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("sheetmodel selftest")
    ck("col_to_num A", col_to_num("A"), 1)
    ck("col_to_num AA", col_to_num("AA"), 27)
    ck("num_to_col roundtrip", num_to_col(col_to_num("BZ")), "BZ")

    p, _ = parse_precedents("=A1+B2", "S")
    ck("simple refs", p, {("S", "A1"), ("S", "B2")})
    p, _ = parse_precedents("=SUM(A1:A3)", "S")
    ck("range expands", p, {("S", "A1"), ("S", "A2"), ("S", "A3")})
    p, _ = parse_precedents("=LOG10(A1)", "S")
    ck("function name not a ref", p, {("S", "A1")})
    p, _ = parse_precedents("=SUM(A1:A2)/COUNT(A1:A2)", "S")
    ck("two functions one range", p, {("S", "A1"), ("S", "A2")})

    # Shared-formula translation. Answers fixed by the A1 rules, not by
    # what the function happens to return. A reader without this read 696
    # of one real workbook's 825 formula cells as constants.
    shifts = [
        ("A1", 1, 0, "A2"),
        ("$A$1", 5, 5, "$A$1"),
        ("$A1", 1, 1, "$A2"),
        ("A$1", 1, 1, "B$1"),
        ("SUM(A1:A3)", 1, 0, "SUM(A2:A4)"),
        ("Sheet2!B4", 2, 0, "Sheet2!B6"),
        ('IF(A1>0,"A1 text",0)', 1, 0, 'IF(A2>0,"A1 text",0)'),
        ("LOG10(A1)", 1, 0, "LOG10(A2)"),
        ("A1+$B2*C$3", 2, 1, "B3+$B4*D$3"),
        ("A1", 0, 0, "A1"),
        ("A1", -5, 0, "#REF!"),
    ]
    ck("shift_formula, 11 hand-set cases",
       [t for t, dr, dc, want in shifts
        if shift_formula(t, dr, dc) != want], [])
    p, _ = parse_precedents("=Other!B4", "S")
    ck("qualified ref", p, {("Other", "B4")})
    p, _ = parse_precedents("='My Sheet'!B4", "S")
    ck("quoted sheet", p, {("My Sheet", "B4")})
    p, n = parse_precedents('=IF(A1>0,"B2 is text",0)', "S")
    ck("ref inside a string literal is not a ref", p, {("S", "A1")})
    p, n = parse_precedents("=SUM(Revenue)", "S")
    ck("named range unresolved not absent", UNRESOLVED in n, True)
    p, n = parse_precedents("=[1]Sheet1!A1", "S")
    ck("external flagged", EXTERNAL in n, True)
    p, n = parse_precedents("=SUM(A1:ZZ99999)", "S")
    ck("oversize range truncated not expanded", (len(p), TRUNCATED in n), (0, True))

    d = tempfile.mkdtemp()
    path = os.path.join(d, "t.xlsx")
    fixture.write_demo(path)
    wb = read(path)
    ck("sheets read", wb.sheets, ["Inputs", "Model", "Summary"])
    ck("constant number", wb.cells[("Inputs", "B2")].kind, CONSTANT_NUMBER)
    ck("constant text", wb.cells[("Inputs", "A2")].kind, CONSTANT_TEXT)
    ck("date style detected", wb.cells[("Inputs", "C2")].kind, CONSTANT_DATE)
    ck("formula read", wb.cells[("Model", "B2")].kind, DERIVED)
    ck("precedent depth of a constant", wb.precedent_depth(("Inputs", "B2")), 0)
    ck("precedent depth of a chain", wb.precedent_depth(("Summary", "B2")), 3)
    ck("downstream depth of a terminal", wb.downstream_depth(("Summary", "B2")), 0)
    ck("downstream depth of an input", wb.downstream_depth(("Inputs", "B2")), 3)
    ck("rank of a terminal is 0", wb.rank(("Summary", "B2")), 0)

    # A planted cycle must report CYCLE, not a number and not a hang.
    cyc = Cell("S", "A1", DERIVED, None, "=B1", {("S", "B1")}, set())
    cyc2 = Cell("S", "B1", DERIVED, None, "=A1", {("S", "A1")}, set())
    w2 = Workbook([cyc, cyc2], ["S"])
    ck("cycle is CYCLE not a number", w2.precedent_depth(("S", "A1")), CYCLE)
    ck("cycle rank is CYCLE", w2.rank(("S", "A1")), CYCLE)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    if len(sys.argv) > 1:
        w = read(sys.argv[1])
        print("reader: %s" % w.reader)
        for s in w.sheets:
            print("%s  %d cells  extent r%d c%d"
                  % (s, len(w.sheet_cells(s)), w.extent(s)[0], w.extent(s)[1]))
    else:
        print(__doc__.strip())
