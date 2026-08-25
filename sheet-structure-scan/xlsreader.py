#!/usr/bin/env python3
"""
xlsreader -- legacy .xls (BIFF8) support for work order 6 S1.

WHAT THE ORDER ASSUMES AND WHAT IS TRUE. S1 states the constraint as
"legacy readers may not expose formulas, only cached values". That is
true of the reader this repository already tested (SSS_023: xlrd 2.0.2
hands back cached values with no formula text) and it is NOT true of the
FILE. A .xls is a CFB container holding a BIFF record stream, and the
formulas are in it: this target carries 336 FORMULA and 23 SHRFMLA
records. The constraint is about a reader, not about the format.

So this reader is stdlib -- `struct` over the container -- and the
one-reader budget stays unspent for a second file format. What it can
and cannot do is declared per capability rather than claimed in prose,
and the caller marks scans NOT_RUN from the declaration:

  cell_values     yes -- NUMBER / RK / MULRK / LABELSST / cached results
  cell_kind       yes -- a FORMULA record is what DERIVED means here
  precedents      yes -- decoded from the ptg token array
  formula_text    NO  -- the tokens are not rendered back to a string

That last line is the honest cut and it has a consequence: `coupling.py`
evaluates formulas, so coupling is NOT_RUN on this file. A value-only
substitute for it -- ranking by dependent count and calling it coupling
-- is exactly what S1 forbids, and is not offered.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import struct
import sys

import sheetmodel
from sheetmodel import (CONSTANT_NUMBER, CONSTANT_TEXT, CONSTANT_DATE,
                        DERIVED, num_to_col)

# ------------------------------------------------------------------ CFB

class CFBError(Exception):
    pass


def _cfb_streams(path):
    """{name: bytes} for the streams in a compound-file container."""
    d = open(path, "rb").read()
    if d[:8] != b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        raise CFBError("not a compound-file container")
    ssz = 1 << struct.unpack_from("<H", d, 0x1E)[0]
    msz = 1 << struct.unpack_from("<H", d, 0x20)[0]
    n_fat = struct.unpack_from("<I", d, 0x2C)[0]
    dir0 = struct.unpack_from("<I", d, 0x30)[0]
    cutoff = struct.unpack_from("<I", d, 0x38)[0]
    mfat0 = struct.unpack_from("<I", d, 0x3C)[0]
    n_mfat = struct.unpack_from("<I", d, 0x40)[0]
    difat0 = struct.unpack_from("<I", d, 0x44)[0]
    n_difat = struct.unpack_from("<I", d, 0x48)[0]
    FREE = 0xFFFFFFFA

    def sect(i):
        o = 512 + i * ssz
        return d[o:o + ssz]

    difat = list(struct.unpack_from("<109I", d, 0x4C))
    nxt = difat0
    for _ in range(n_difat):
        if nxt >= FREE:
            break
        s = sect(nxt)
        difat += list(struct.unpack_from("<%dI" % (ssz // 4 - 1), s, 0))
        nxt = struct.unpack_from("<I", s, ssz - 4)[0]
    difat = [x for x in difat[:n_fat] if x < FREE]

    fat = []
    for f in difat:
        fat += list(struct.unpack_from("<%dI" % (ssz // 4), sect(f), 0))

    def chain(start):
        out, i, seen = [], start, set()
        while i < FREE and i not in seen:
            seen.add(i)
            out.append(i)
            i = fat[i] if i < len(fat) else 0xFFFFFFFE
        return out

    def stream(start, size=None):
        b = b"".join(sect(i) for i in chain(start))
        return b[:size] if size else b

    dirb = stream(dir0)
    entries = []
    for o in range(0, len(dirb) - 127, 128):
        e = dirb[o:o + 128]
        nlen = struct.unpack_from("<H", e, 0x40)[0]
        name = e[:max(0, nlen - 2)].decode("utf-16-le", "replace")
        typ = e[0x42]
        start = struct.unpack_from("<I", e, 0x74)[0]
        size = struct.unpack_from("<Q", e, 0x78)[0]
        if typ in (1, 2, 5):
            entries.append((name, typ, start, size))

    roots = [e for e in entries if e[1] == 5]
    mini = stream(roots[0][2], roots[0][3]) if roots and roots[0][2] < FREE \
        else b""
    mfat, nx = [], mfat0
    for _ in range(n_mfat):
        if nx >= FREE:
            break
        mfat += list(struct.unpack_from("<%dI" % (ssz // 4), sect(nx), 0))
        nx = fat[nx] if nx < len(fat) else 0xFFFFFFFE

    def mstream(start, size):
        out, i, seen = b"", start, set()
        while i < FREE and i not in seen:
            seen.add(i)
            out += mini[i * msz:(i + 1) * msz]
            i = mfat[i] if i < len(mfat) else 0xFFFFFFFE
        return out[:size]

    out = {}
    for n, t, st, sz in entries:
        if t != 2:
            continue
        out[n] = mstream(st, sz) if sz < cutoff else stream(st, sz)
    return out


# ------------------------------------------------------------------ BIFF

BOF, EOF_ = 0x0809, 0x000A
BOUNDSHEET, SST, CONTINUE, EXTERNSHEET = 0x0085, 0x00FC, 0x003C, 0x0017
LABELSST, LABEL, NUMBER, RK, MULRK = 0x00FD, 0x0204, 0x0203, 0x027E, 0x00BD
BLANK, MULBLANK, BOOLERR = 0x0201, 0x00BE, 0x0205
FORMULA, SHRFMLA, ARRAY, STRING = 0x0006, 0x04BC, 0x0221, 0x0207
XF, FORMAT = 0x00E0, 0x041E


def _records(b):
    o = 0
    while o + 4 <= len(b):
        rid, ln = struct.unpack_from("<HH", b, o)
        yield o, rid, b[o + 4:o + 4 + ln]
        o += 4 + ln


def _xlunicode(b, o, cch, two_byte_len=True):
    """XLUnicodeString body at o with cch characters. Returns (text, next)."""
    grbit = b[o]
    o += 1
    rich = struct.unpack_from("<H", b, o)[0] if grbit & 0x08 else 0
    o += 2 if grbit & 0x08 else 0
    ext = struct.unpack_from("<I", b, o)[0] if grbit & 0x04 else 0
    o += 4 if grbit & 0x04 else 0
    if grbit & 0x01:
        txt = b[o:o + cch * 2].decode("utf-16-le", "replace")
        o += cch * 2
    else:
        txt = b[o:o + cch].decode("cp1252", "replace")
        o += cch
    o += rich * 4 + ext
    return txt, o


def _sst(chunks):
    """Shared strings across SST plus its CONTINUE records.

    The awkward part of BIFF8: a string can straddle a CONTINUE boundary
    and the flag byte is REPEATED at the start of the continuation, which
    may also change the encoding mid-string. Handled explicitly rather
    than by joining the payloads and hoping.
    """
    data = chunks[0]
    total, unique = struct.unpack_from("<II", data, 0)
    pos, ci = 8, 0
    out = []
    cur = data
    while len(out) < unique:
        if pos + 2 > len(cur):
            ci += 1
            if ci >= len(chunks):
                break
            cur, pos = chunks[ci], 0
            continue
        cch = struct.unpack_from("<H", cur, pos)[0]
        pos += 2
        grbit = cur[pos]
        pos += 1
        rich = 0
        ext = 0
        if grbit & 0x08:
            rich = struct.unpack_from("<H", cur, pos)[0]
            pos += 2
        if grbit & 0x04:
            ext = struct.unpack_from("<I", cur, pos)[0]
            pos += 4
        wide = grbit & 0x01
        got, need = [], cch
        while need > 0:
            avail = (len(cur) - pos) // (2 if wide else 1)
            take = min(avail, need)
            raw = cur[pos:pos + take * (2 if wide else 1)]
            got.append(raw.decode("utf-16-le" if wide else "cp1252",
                                  "replace"))
            pos += take * (2 if wide else 1)
            need -= take
            if need > 0:
                ci += 1
                if ci >= len(chunks):
                    need = 0
                    break
                cur = chunks[ci]
                wide = cur[0] & 0x01
                pos = 1
        skip = rich * 4 + ext
        while skip > 0:
            avail = len(cur) - pos
            take = min(avail, skip)
            pos += take
            skip -= take
            if skip > 0:
                ci += 1
                if ci >= len(chunks):
                    break
                cur, pos = chunks[ci], 0
        out.append("".join(got))
    return out


def _rk(v):
    cents = v & 1
    if v & 2:
        n = float(v >> 2 if v >> 2 < 0x20000000 else (v >> 2) - 0x40000000)
    else:
        n = struct.unpack("<d", struct.pack("<Q", (v & 0xFFFFFFFC) << 32))[0]
    return n / 100.0 if cents else n


# ------------------------------------------------------------------ ptgs

# Operand sizes, excluding the token byte. Only what is needed to WALK
# the array correctly; a token whose size is unknown stops the walk and
# the cell records that its precedents are partial rather than empty.
_PTG_SIZE = {
    0x01: 4, 0x02: 4, 0x03: 0, 0x04: 0, 0x05: 0, 0x06: 0, 0x07: 0,
    0x08: 0, 0x09: 0, 0x0A: 0, 0x0B: 0, 0x0C: 0, 0x0D: 0, 0x0E: 0,
    0x0F: 0, 0x10: 0, 0x11: 0, 0x12: 0, 0x13: 0, 0x14: 0, 0x15: 0,
    0x16: 0, 0x17: None, 0x18: None, 0x19: None, 0x1C: 1, 0x1D: 1,
    0x1E: 2, 0x1F: 8, 0x40: 0,
}
_REF = (0x24, 0x44, 0x64)
_AREA = (0x25, 0x45, 0x65)
_REFN = (0x2C, 0x4C, 0x6C)
_AREAN = (0x2D, 0x4D, 0x6D)
_REF3D = (0x3A, 0x5A, 0x7A)
_AREA3D = (0x3B, 0x5B, 0x7B)
_REFERR = (0x2A, 0x4A, 0x6A, 0x2B, 0x4B, 0x6B,
           0x3C, 0x5C, 0x7C, 0x3D, 0x5D, 0x7D)
_NAME = (0x23, 0x43, 0x63)
_NAMEX = (0x39, 0x59, 0x79)
_FUNC = (0x21, 0x41, 0x61)
_FUNCVAR = (0x22, 0x42, 0x62)
_MEM = (0x26, 0x46, 0x66, 0x27, 0x47, 0x67, 0x29, 0x49, 0x69,
        0x2E, 0x4E, 0x6E, 0x2F, 0x4F, 0x6F)
_TBL = (0x02,)


def _rel(rw, gcol, base):
    """A relative ptg reference resolved against the cell that holds it.

    Relative refs are stored as deltas: the row as a signed 16-bit value,
    the column as a signed 8-BIT value in the low byte. Reading the column
    as 14 bits, which is what an absolute ref uses, gives 192 for -64 and
    puts the precedent in a column that does not exist.
    """
    frow_rel = bool(gcol & 0x8000)
    fcol_rel = bool(gcol & 0x4000)
    if frow_rel:
        row = base[0] + struct.unpack("<h", struct.pack("<H", rw & 0xFFFF))[0]
    else:
        row = rw & 0x3FFF
    if fcol_rel:
        col = base[1] + struct.unpack("<b", bytes([gcol & 0xFF]))[0]
    else:
        col = gcol & 0x3FFF
    return row, col


def _cellref(row, colflags):
    col = colflags & 0x3FFF
    return row, col


def _addr(row, col):
    return "%s%d" % (num_to_col(col + 1), row + 1)


def parse_ptgs(rgce, home_sheet, sheets, xti, base=None):
    """Precedent cell keys from a ptg token array.

    Returns (precedents, complete). `complete` is False when a token the
    walk does not know is hit -- the refs found so far are kept and the
    cell says its list is partial. An unknown token silently truncating a
    precedent list would make the graph wrong in a way nothing reports.
    """
    out, o, n = [], 0, len(rgce)
    complete = True

    def add(sheet, r1, c1, r2=None, c2=None):
        if sheet is None:
            return
        r2 = r1 if r2 is None else r2
        c2 = c1 if c2 is None else c2
        if (r2 - r1 + 1) * (c2 - c1 + 1) > 65536:
            return
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                out.append((sheet, _addr(r, c)))

    def sheet_of(ixti):
        if xti is None or ixti >= len(xti):
            return None
        first = xti[ixti][1]
        return sheets[first] if 0 <= first < len(sheets) else None

    while o < n:
        t = rgce[o]
        o += 1
        if t in _REF:
            r, cf = struct.unpack_from("<HH", rgce, o)
            o += 4
            add(home_sheet, *_cellref(r, cf))
        elif t in _AREA:
            r1, r2, c1, c2 = struct.unpack_from("<HHHH", rgce, o)
            o += 8
            add(home_sheet, r1, c1 & 0x3FFF, r2, c2 & 0x3FFF)
        elif t in _REFN:
            rw, gc = struct.unpack_from("<HH", rgce, o)
            o += 4
            if base:
                add(home_sheet, *_rel(rw, gc, base))
            else:
                complete = False
        elif t in _AREAN:
            r1, r2, g1, g2 = struct.unpack_from("<HHHH", rgce, o)
            o += 8
            if base:
                a = _rel(r1, g1, base)
                b = _rel(r2, g2, base)
                add(home_sheet, min(a[0], b[0]), min(a[1], b[1]),
                    max(a[0], b[0]), max(a[1], b[1]))
            else:
                complete = False
        elif t in _REF3D:
            ixti, r, cf = struct.unpack_from("<HHH", rgce, o)
            o += 6
            add(sheet_of(ixti), *_cellref(r, cf))
        elif t in _AREA3D:
            ixti, r1, r2, c1, c2 = struct.unpack_from("<HHHHH", rgce, o)
            o += 10
            add(sheet_of(ixti), r1, c1 & 0x3FFF, r2, c2 & 0x3FFF)
        elif t in _REFERR:
            o += 6 if t in (0x3C, 0x5C, 0x7C) else (
                10 if t in (0x3D, 0x5D, 0x7D) else (
                    4 if t in (0x2A, 0x4A, 0x6A) else 8))
        elif t in _NAME:
            o += 4
        elif t in _NAMEX:
            o += 6
        elif t in _FUNC:
            o += 2
        elif t in _FUNCVAR:
            o += 3
        elif t in _MEM:
            o += 6
        elif t == 0x19:                      # ptgAttr
            grbit = rgce[o]
            cnt = struct.unpack_from("<H", rgce, o + 1)[0]
            o += 3
            if grbit & 0x04:                 # ptgAttrChoose
                o += (cnt + 1) * 2
        elif t == 0x17:                      # ptgStr
            cch = rgce[o]
            _, o = _xlunicode(rgce, o + 1, cch)
        elif t in _PTG_SIZE and _PTG_SIZE[t] is not None:
            o += _PTG_SIZE[t]
        else:
            complete = False
            break
    return out, complete


# ------------------------------------------------------------------ read

DATE_FORMATS = set(range(14, 23)) | {27, 28, 29, 30, 31, 36, 45, 46, 47,
                                     50, 51, 52, 53, 54, 55, 56, 57, 58}


def read_xls(path):
    streams = _cfb_streams(path)
    wb = streams.get("Workbook") or streams.get("Book")
    if wb is None:
        raise CFBError("no Workbook stream; not a BIFF workbook")

    sheets, sst_chunks, xfs, fmts, xti = [], [], [], {}, None
    positions = []
    last_sst = False
    for off, rid, data in _records(wb):
        if rid == BOUNDSHEET:
            pos = struct.unpack_from("<I", data, 0)[0]
            cch = data[6]
            name = (data[8:8 + cch * 2].decode("utf-16-le", "replace")
                    if data[7] & 1 else
                    data[8:8 + cch].decode("cp1252", "replace"))
            sheets.append(name)
            positions.append(pos)
        elif rid == SST:
            sst_chunks = [data]
            last_sst = True
            continue
        elif rid == CONTINUE and last_sst:
            sst_chunks.append(data)
            continue
        elif rid == XF:
            xfs.append(struct.unpack_from("<H", data, 2)[0])
        elif rid == FORMAT:
            ifmt = struct.unpack_from("<H", data, 0)[0]
            cch = struct.unpack_from("<H", data, 2)[0]
            txt, _ = _xlunicode(data, 4, cch)
            fmts[ifmt] = txt
        elif rid == EXTERNSHEET:
            cnt = struct.unpack_from("<H", data, 0)[0]
            xti = [struct.unpack_from("<HHH", data, 2 + i * 6)
                   for i in range(cnt)]
        if rid != CONTINUE:
            last_sst = (rid == SST)
    strings = _sst(sst_chunks) if sst_chunks else []

    def is_date(ixfe):
        if ixfe >= len(xfs):
            return False
        ifmt = xfs[ixfe]
        if ifmt in DATE_FORMATS:
            return True
        f = fmts.get(ifmt, "")
        return bool(f) and any(ch in f for ch in "ymdhs") and "0.00" not in f

    cells = []
    shared = {}
    deferred = []
    pending_string = None

    # Sheet substreams, located by the BOUNDSHEET offsets.
    for si, start in enumerate(positions):
        sheet = sheets[si]
        end = min([p for p in positions if p > start] + [len(wb)])
        sub = wb[start:end]
        for off, rid, data in _records(sub):
            if rid == EOF_:
                break
            if rid in (LABELSST, LABEL, NUMBER, RK, BLANK, BOOLERR, FORMULA):
                r, c, ixfe = struct.unpack_from("<HHH", data, 0)
            if rid == LABELSST:
                isst = struct.unpack_from("<I", data, 6)[0]
                v = strings[isst] if isst < len(strings) else ""
                cells.append(sheetmodel.Cell(sheet, _addr(r, c),
                                             CONSTANT_TEXT, v, None, [], ""))
            elif rid == LABEL:
                cch = struct.unpack_from("<H", data, 6)[0]
                v, _ = _xlunicode(data, 8, cch)
                cells.append(sheetmodel.Cell(sheet, _addr(r, c),
                                             CONSTANT_TEXT, v, None, [], ""))
            elif rid == NUMBER:
                v = struct.unpack_from("<d", data, 6)[0]
                cells.append(sheetmodel.Cell(
                    sheet, _addr(r, c),
                    CONSTANT_DATE if is_date(ixfe) else CONSTANT_NUMBER,
                    v, None, [], ""))
            elif rid == RK:
                v = _rk(struct.unpack_from("<I", data, 6)[0])
                cells.append(sheetmodel.Cell(
                    sheet, _addr(r, c),
                    CONSTANT_DATE if is_date(ixfe) else CONSTANT_NUMBER,
                    v, None, [], ""))
            elif rid == MULRK:
                r, c1 = struct.unpack_from("<HH", data, 0)
                nrk = (len(data) - 6) // 6
                for i in range(nrk):
                    ixfe, rkv = struct.unpack_from("<HI", data, 4 + i * 6)
                    cells.append(sheetmodel.Cell(
                        sheet, _addr(r, c1 + i),
                        CONSTANT_DATE if is_date(ixfe) else CONSTANT_NUMBER,
                        _rk(rkv), None, [], ""))
            elif rid == SHRFMLA:
                r1, r2, c1, c2 = struct.unpack_from("<HHBB", data, 0)
                cce = struct.unpack_from("<H", data, 8)[0]
                shared[(sheet, r1, c1)] = data[10:10 + cce]
            elif rid == FORMULA:
                res = data[6:14]
                cce = struct.unpack_from("<H", data, 20)[0]
                rgce = data[22:22 + cce]
                val = None
                if res[6:8] == b"\xff\xff":
                    if res[0] == 0:
                        pending_string = (sheet, _addr(r, c))
                    elif res[0] == 1:
                        val = bool(res[2])
                else:
                    val = struct.unpack("<d", res)[0]
                base = (r, c)
                cell = sheetmodel.Cell(sheet, _addr(r, c), DERIVED, val,
                                       None, [], "")
                if rgce[:1] == b"\x01" and len(rgce) >= 5:
                    # ptgExp: the tokens live on a SHRFMLA record that is
                    # written AFTER the first formula referring to it, so
                    # this cannot be resolved in stream order. Deferred to
                    # a second pass rather than resolved to nothing --
                    # resolving to nothing here would have given 23 cells
                    # an empty precedent list that read as "no precedents".
                    sr, sc = struct.unpack_from("<HH", rgce, 1)
                    deferred.append((cell, sheet, base, (sheet, sr, sc)))
                else:
                    pre, ok = parse_ptgs(rgce, sheet, sheets, xti, base)
                    cell.precedents = sorted(set(pre))
                    cell.notes = "" if ok else "PARTIAL_PRECEDENTS"
                cells.append(cell)
            elif rid == STRING and pending_string:
                cch = struct.unpack_from("<H", data, 0)[0]
                txt, _ = _xlunicode(data, 2, cch)
                for cl in reversed(cells):
                    if (cl.sheet, cl.addr) == pending_string:
                        cl.value = txt
                        break
                pending_string = None

    # Second pass: shared-formula followers, now that every SHRFMLA has
    # been seen. A key that still does not resolve says so.
    for cell, sheet, base, key in deferred:
        toks = shared.get(key)
        if toks is None:
            cell.notes = "SHARED_MASTER_NOT_FOUND"
            continue
        pre, ok = parse_ptgs(toks, sheet, sheets, xti, base)
        cell.precedents = sorted(set(pre))
        cell.notes = "" if ok else "PARTIAL_PRECEDENTS"

    w = sheetmodel.Workbook(cells, sheets, path=path,
                            reader="stdlib-xls-biff8")
    w.capabilities = CAPABILITIES_XLS
    return w


# What this reader can and cannot supply. Callers mark scans NOT_RUN from
# this rather than from a guess about the format.
CAPABILITIES_XLS = {
    "cell_values": True,
    "cell_kind": True,
    "precedents": True,
    "formula_text": False,
}
CAPABILITIES_XLSX = {
    "cell_values": True,
    "cell_kind": True,
    "precedents": True,
    "formula_text": True,
}


def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-56s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("xlsreader selftest")

    # RK decoding, four known answers -- the four flag combinations.
    ck("RK integer", _rk((100 << 2) | 2), 100.0)
    ck("RK integer / 100", _rk((100 << 2) | 3), 1.0)
    ck("RK negative integer", _rk(((-5 & 0x3FFFFFFF) << 2) | 2), -5.0)
    ck("RK float", round(_rk(struct.unpack("<I", struct.pack(
        "<d", 1.25)[4:])[0] & 0xFFFFFFFC), 6), 1.25)

    # Address arithmetic.
    ck("address is 1-based in both axes", _addr(0, 0), "A1")
    ck("column carries past Z", _addr(0, 26), "AA1")

    # ptg walk: a local ref, an area, and a token the walk does not know.
    rgce = bytes([0x24]) + struct.pack("<HH", 0, 0)
    ck("a local ref decodes", parse_ptgs(rgce, "S", ["S"], None),
       ([("S", "A1")], True))
    rgce = bytes([0x25]) + struct.pack("<HHHH", 0, 1, 0, 0)
    ck("an area expands to its cells",
       parse_ptgs(rgce, "S", ["S"], None)[0], [("S", "A1"), ("S", "A2")])
    ck("an unknown token truncates and SAYS so",
       parse_ptgs(bytes([0xFE, 0x24]), "S", ["S"], None), ([], False))
    # An addition of two refs walks through the operator.
    rgce = (bytes([0x24]) + struct.pack("<HH", 0, 0) + bytes([0x24]) +
            struct.pack("<HH", 1, 0) + bytes([0x03]))
    ck("an operator does not stop the walk",
       parse_ptgs(rgce, "S", ["S"], None), ([("S", "A1"), ("S", "A2")], True))

    # Relative refs, the shape shared formulas use. The column delta is a
    # signed BYTE and the row delta a signed SHORT; reading the column as
    # 14 bits puts a -1 offset in column 16384.
    ck("a relative ref resolves against its base",
       _rel(0xFFFF, 0xC000, (11, 6)), (10, 6))
    ck("a negative column delta is a signed byte",
       _rel(0x0000, 0xC0FF, (11, 6)), (11, 5))
    ck("an absolute row inside a relative ref stays absolute",
       _rel(3, 0x4000, (11, 6)), (3, 6))
    rgce = bytes([0x2D]) + struct.pack("<HHHH", 0xFFFE, 0xFFFF, 0xC000,
                                       0xC000)
    ck("a relative AREA decodes rather than being walked past",
       parse_ptgs(rgce, "S", ["S"], None, (11, 6))[0],
       [("S", "G10"), ("S", "G11")])
    ck("and with no base it says the walk is partial",
       parse_ptgs(rgce, "S", ["S"], None, None)[1], False)

    # 3d refs need the EXTERNSHEET map; without it the ref is dropped
    # rather than attributed to the home sheet.
    rgce = bytes([0x3A]) + struct.pack("<HHH", 0, 0, 0)
    ck("a 3d ref with no xti map is dropped, not misattributed",
       parse_ptgs(rgce, "S", ["S", "T"], None)[0], [])
    ck("and resolves with one",
       parse_ptgs(rgce, "S", ["S", "T"], [(0, 1, 1)])[0], [("T", "A1")])

    # Capability declaration is the contract the caller marks NOT_RUN from.
    ck("formula text is declared unavailable for xls",
       CAPABILITIES_XLS["formula_text"], False)
    ck("and precedents are declared available",
       CAPABILITIES_XLS["precedents"], True)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    w = read_xls(sys.argv[1])
    print("reader", w.reader, "sheets", len(w.sheets), "cells", len(w.cells))
    for s in w.sheets:
        print("  %-40s %d" % (s, len(w.sheet_cells(s))))
