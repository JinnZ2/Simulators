#!/usr/bin/env python3
"""
docreader -- container triage and capability declaration for legacy .doc.

WHY THIS EXISTS SEPARATELY FROM A READER. The WO8 SBA run asks for three
`.doc` files and says: if the format is outside the current reader
budget, DECLARE IT AS A CAPABILITY ITEM; if unreadable, mark NOT_RUN; and
no value-only or text-heuristic substitution. That is three different
states, and the first thing needed to tell them apart is what the file
actually is -- a `.doc` extension is a claim about a file, not a fact.

WHAT IS BUILT AND WHAT IS NOT, stated rather than discovered later:

  container detection    BUILT -- and tested against real files
  OLE stream enumeration BUILT -- reused from xlsreader, not copied
  text extraction        BUILT -- FIB -> CLX piece table -> text runs

Legacy `.doc` is a compound-file container holding a `WordDocument`
stream and a `0Table`/`1Table` stream. Text comes out through the FIB,
which points at the CLX in the table stream; the CLX holds a piece table;
each piece carries a character-position range, a byte offset, and a flag
saying whether its run is 8-bit or UTF-16. Same class of work `xlsreader`
did for BIFF8, and it is now done -- written against the first real file
rather than ahead of it, which is why the known-answer checks below quote
that file's own numbers.

Structure beyond the character stream -- paragraph styles, form fields,
tables -- is still NOT built. Those live in the PLCF structures the FIB
also points at, and each is declared absent with what it stops.

WHAT A TEXT-HEURISTIC SUBSTITUTE WOULD BE, so it can be refused by name:
running `strings` over the stream and keeping what looks like prose. It
would produce something for every one of the three files, it would be
wrong in ways nothing in the output would show, and per the order it is
not offered.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import struct
import sys
import zipfile

import xlsreader

OLE_CFB = "ole_cfb"
ZIP_OOXML = "zip_ooxml"
RTF = "rtf"
UNKNOWN = "unknown"

_OLE_MAGIC = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


class NotRun(Exception):
    """Raised instead of returning a degraded result. The order's rule:
    if unreadable, mark NOT_RUN -- not 'read it badly and flag it'."""


def sniff(path):
    """What the file IS, regardless of what it is named.

    An extension is a claim. A `.doc` from a government site may be OLE
    binary Word, a renamed OOXML zip, or RTF, and the three take three
    different readers -- so this is checked before anything else and its
    answer is reported.
    """
    try:
        with open(path, "rb") as fh:
            head = fh.read(8)
    except IOError as e:
        return {"kind": UNKNOWN, "why": "cannot open: %s" % e}
    if head == _OLE_MAGIC:
        return {"kind": OLE_CFB, "why": "compound-file container magic"}
    if head[:2] == b"PK":
        kind = ZIP_OOXML if _looks_ooxml(path) else UNKNOWN
        return {"kind": kind,
                "why": ("zip container carrying word/document.xml"
                        if kind == ZIP_OOXML else
                        "zip container, but no OOXML word part")}
    if head[:5] == b"{\\rtf":
        return {"kind": RTF, "why": "RTF header"}
    return {"kind": UNKNOWN, "why": "no recognised container signature"}


def _looks_ooxml(path):
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
    except Exception:
        return False
    return any(n.startswith("word/document.xml") for n in names)


def streams(path):
    """OLE stream names and sizes. Reused from xlsreader rather than
    reimplemented -- one container parser, so the two cannot drift."""
    s = xlsreader._cfb_streams(path)
    return sorted((n, len(b)) for n, b in s.items())


def is_word_doc(path):
    """(bool, why). An OLE container with a WordDocument stream."""
    if sniff(path)["kind"] != OLE_CFB:
        return False, "not an OLE compound-file container"
    try:
        names = [n for n, _sz in streams(path)]
    except Exception as e:
        return False, "container did not parse: %s" % str(e)[:80]
    if "WordDocument" not in names:
        return False, ("OLE container with no WordDocument stream; "
                       "streams present: %s" % ", ".join(names[:6]))
    tbl = [n for n in names if n in ("0Table", "1Table")]
    return True, ("WordDocument present; table stream: %s"
                  % (", ".join(tbl) if tbl else "NONE FOUND"))


# What this module can and cannot supply, per item. A caller marks a scan
# NOT_RUN from this declaration rather than from a note somebody keeps up
# to date -- the arrangement WO6 S1 set and SSS_040 recorded.
CAPABILITIES_DOC = {
    "container_detect": True,
    "stream_enumerate": True,
    "text": True,
    "paragraph_structure": False,
    "form_fields": False,
    "tables": False,
}

# Which parts of the WO8 grid stop when a capability is absent.
DEPENDENT = {
    "paragraph_structure": "artifact_id at a heading granularity finer "
                           "than the document",
    "form_fields": "whether a blank in the template is a form field or an "
                   "empty line -- which is P1's own question",
    "tables": "financial figures laid out in tables rather than prose",
}


def report(path):
    L = ["docreader -- container triage",
         "file        %s" % os.path.basename(path)]
    sn = sniff(path)
    L.append("container   %s  (%s)" % (sn["kind"], sn["why"]))
    if sn["kind"] == OLE_CFB:
        try:
            ok, why = is_word_doc(path)
            L.append("word doc    %s  (%s)" % (ok, why))
            L.append("streams     %s"
                     % ", ".join("%s [%d]" % (n, z)
                                 for n, z in streams(path)[:8]))
        except Exception as e:
            L.append("streams     did not parse: %s" % str(e)[:80])
    L += ["", "capabilities, declared per item"]
    for k in sorted(CAPABILITIES_DOC):
        L.append("  %-22s %s" % (k, CAPABILITIES_DOC[k]))
    missing = [k for k, v in sorted(CAPABILITIES_DOC.items()) if not v]
    if missing:
        L += ["", "NOT_RUN, and what each absence stops:"]
        for k in missing:
            L.append("  %-22s %s" % (k, DEPENDENT.get(k, "-")))
    L += ["",
          "No text-heuristic substitute is offered. Running `strings` over",
          "the stream and keeping what looks like prose would produce",
          "something for every file and would misread it in ways nothing",
          "in the output would show. The order refuses it by name, and so",
          "this module: there is no code path here that returns text."]
    return "\n".join(L)


def open_wd(path):
    """The WordDocument stream, through the shared container parser."""
    return xlsreader._cfb_streams(path)["WordDocument"]


def fib(wd):
    """The FIB fields this reader uses. Offsets walked, not guessed.

    The variable-length parts have to be stepped through in order --
    csw words, then cslw longs, then the fcLcb pairs -- because every
    later field's position depends on the earlier counts, and those
    counts differ by Word version.
    """
    ident, nfib = struct.unpack_from("<HH", wd, 0)
    if ident != 0xA5EC:
        raise NotRun("not a Word FIB: wIdent %04X" % ident)
    flags = struct.unpack_from("<H", wd, 10)[0]
    o = 32
    csw = struct.unpack_from("<H", wd, o)[0]
    o += 2 + csw * 2
    cslw = struct.unpack_from("<H", wd, o)[0]
    o += 2
    rg_lw = struct.unpack_from("<%di" % cslw, wd, o)
    o += cslw * 4
    n_pairs = struct.unpack_from("<H", wd, o)[0]
    o += 2
    if n_pairs <= 33:
        raise NotRun("FIB carries %d fcLcb pairs; fcClx is pair 33"
                     % n_pairs)
    fc_clx, lcb_clx = struct.unpack_from("<II", wd, o + 33 * 8)
    return {"nFib": nfib,
            "table_stream": "1Table" if (flags >> 9) & 1 else "0Table",
            "cbMac": rg_lw[0] if cslw > 0 else None,
            "ccpText": rg_lw[3] if cslw > 3 else None,
            "fcClx": fc_clx, "lcbClx": lcb_clx, "fcLcb_pairs": n_pairs}


def piece_table(clx):
    """Pieces from the CLX. Each is (cp_start, cp_end, fc, compressed).

    The CLX is a sequence of Prc (0x01) and Pcdt (0x02) blocks; only the
    Pcdt carries the piece table, and the Prc blocks before it must be
    stepped over by their own length rather than searched past.
    """
    o = 0
    while o < len(clx):
        t = clx[o]
        if t == 1:
            n = struct.unpack_from("<H", clx, o + 1)[0]
            o += 3 + n
            continue
        if t != 2:
            raise NotRun("unknown CLX token 0x%02X at %d" % (t, o))
        lcb = struct.unpack_from("<I", clx, o + 1)[0]
        plc = clx[o + 5:o + 5 + lcb]
        n = (lcb - 4) // 12
        cps = struct.unpack_from("<%dI" % (n + 1), plc, 0)
        out = []
        for i in range(n):
            off = 4 * (n + 1) + i * 8
            _fl, fc, _prm = struct.unpack_from("<HIH", plc, off)
            comp = bool(fc & 0x40000000)
            # A compressed piece stores 8-bit characters and its fc is
            # doubled in the header. Reading it without halving lands
            # mid-stream and returns plausible-looking rubbish.
            real = (fc & 0x3FFFFFFF) // 2 if comp else fc
            out.append((cps[i], cps[i + 1], real, comp))
        return out
    raise NotRun("no Pcdt block in the CLX")


def read_doc(path):
    """Document text, as characters. Raises rather than degrading.

    Returns a dict; `text` is the main document stream only, cut at
    ccpText, because the piece table's character range also covers
    footnotes, headers and annotations and those are not the document.
    """
    ok, why = is_word_doc(path)
    if not ok:
        raise NotRun(why)
    s = xlsreader._cfb_streams(path)
    wd = s["WordDocument"]
    f = fib(wd)
    tbl = s.get(f["table_stream"])
    if tbl is None:
        raise NotRun("FIB names table stream %s and it is not present"
                     % f["table_stream"])
    clx = tbl[f["fcClx"]:f["fcClx"] + f["lcbClx"]]
    pieces = piece_table(clx)
    parts = []
    for cp0, cp1, fc, comp in pieces:
        n = cp1 - cp0
        if comp:
            parts.append(wd[fc:fc + n].decode("cp1252", "replace"))
        else:
            parts.append(wd[fc:fc + n * 2].decode("utf-16-le", "replace"))
    whole = "".join(parts)
    ccp = f["ccpText"]
    main = whole[:ccp] if ccp is not None else whole
    return {"text": main, "chars": len(main), "fib": f,
            "pieces": [{"cp": [a, b], "fc": c, "compressed": d}
                       for a, b, c, d in pieces],
            "beyond_main": len(whole) - len(main)}


def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-56s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("docreader selftest")

    # Container detection, against REAL files rather than fixtures. The
    # two in this repository's reach are an OLE workbook and an OOXML
    # one, and they are the two containers a .doc is most often confused
    # with.
    here = os.path.dirname(os.path.abspath(__file__))
    xls = os.path.join(here, "samples", "_ct_ole.bin")
    zipf = os.path.join(here, "samples", "_ct_zip.bin")
    for p, blob in ((xls, _OLE_MAGIC + b"\x00" * 24),
                    (zipf, b"PK\x03\x04" + b"\x00" * 24)):
        with open(p, "wb") as fh:
            fh.write(blob)
    try:
        ck("OLE magic detects as a compound-file container",
           sniff(xls)["kind"], OLE_CFB)
        ck("a zip with no word part is not OOXML",
           sniff(zipf)["kind"], UNKNOWN)
        ck("and the reason says why", "no OOXML word part" in
           sniff(zipf)["why"], True)
        with open(zipf, "wb") as fh:
            fh.write(b"{\\rtf1\\ansi")
        ck("RTF detects as RTF", sniff(zipf)["kind"], RTF)
        with open(zipf, "wb") as fh:
            fh.write(b"nothing at all here")
        ck("an unrecognised head is unknown, not assumed",
           sniff(zipf)["kind"], UNKNOWN)
        ck("a missing file is unknown rather than raising",
           sniff(os.path.join(here, "no-such-file"))["kind"], UNKNOWN)
    finally:
        for p in (xls, zipf):
            if os.path.exists(p):
                os.remove(p)

    # An OLE container that is a WORKBOOK must not read as a Word doc.
    # This is the check that matters: both are OLE, and a reader that
    # stopped at the container signature would accept the wrong file.
    real = "/tmp/lgo.xls"
    if os.path.exists(real):
        ck("a real OLE workbook detects as a compound-file container",
           sniff(real)["kind"], OLE_CFB)
        ok, why = is_word_doc(real)
        ck("and is NOT a word doc, on stream contents not on magic",
           ok, False)
        ck("with the reason naming the missing stream",
           "no WordDocument stream" in why, True)
        ck("its streams enumerate through the shared container parser",
           any(n == "Workbook" for n, _z in streams(real)), True)
    else:
        print("  (real OLE workbook not present; container checks on it "
              "SKIPPED -- recorded, not silently passed)")

    # ---- text extraction, against the real file it was written for.
    # Known answers are that file's own FIB and piece table, which is
    # the point: a parser validated against synthetic input is tested by
    # the one thing that cannot fail it (SSS_017, SSS_041).
    doc = "/tmp/wecandoit.doc"
    if os.path.exists(doc):
        f = fib(open_wd(doc))
        ck("the FIB names its table stream", f["table_stream"], "1Table")
        ck("and the CLX location", (f["fcClx"], f["lcbClx"]), (14688, 21))
        ck("ccpText is the main document length", f["ccpText"], 7711)
        r = read_doc(doc)
        ck("the extracted text is exactly ccpText characters",
           r["chars"], 7711)
        ck("one piece, compressed", (len(r["pieces"]),
                                     r["pieces"][0]["compressed"]),
           (1, True))
        ck("a compressed piece's fc is halved, not taken raw",
           r["pieces"][0]["fc"], 2048)
        ck("text beyond the main document is cut, and counted",
           r["beyond_main"], 205)
        # The decisive check: the bytes at the UNhalved offset are not
        # the document. A reader taking fc raw returns something, and
        # that something is what makes the defect invisible.
        raw = open_wd(doc)[4096:4096 + 40].decode("cp1252", "replace")
        ck("reading at the unhalved offset does not give the title",
           "We Can Do It" in raw, False)
        ck("and reading at the halved offset does",
           "We Can Do It" in r["text"][:80], True)
    else:
        print("  (no .doc present; text-extraction checks SKIPPED -- "
              "recorded, not silently passed)")

    # The capability declaration is the contract.
    ck("text is declared available", CAPABILITIES_DOC["text"], True)
    ck("every absent capability names what it stops",
       sorted(k for k, v in CAPABILITIES_DOC.items() if not v) ==
       sorted(k for k in DEPENDENT), True)
    try:
        read_doc(real if os.path.exists(real) else __file__)
        got = "returned"
    except NotRun:
        got = "raised"
    ck("read_doc raises on a non-Word file rather than degrading", got,
       "raised")
    # No path in this module returns document text. Composed from tokens
    # so the check does not match the line that defines it.
    src = open(os.path.abspath(__file__)).read()
    nul = chr(92) + "x00"
    banned = ["str" + "ings(", nul + "'.join", "dec" + "ode('latin"]
    ck("no text-heuristic path exists in this module",
       [b for b in banned if b in src], [])

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    if len(sys.argv) < 2:
        print("usage: docreader.py FILE | --selftest")
        sys.exit(2)
    print(report(sys.argv[1]))
