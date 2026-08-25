#!/usr/bin/env python3
"""
fixture -- write the demo workbook the selftests read.

Written with zipfile and string templates, so the repository stays
text-only: nothing here is an opaque binary whose contents have to be
taken on trust. SHEETS below is the whole workbook, readable as a table,
and write_demo() is a mechanical transcription of it.

The workbook is built to carry one of each thing the scans look for AND
one of each thing they must not fire on:

  header collision      'total' appears three times with three
                        constructions; 'item' appears three times with
                        one, and must NOT flag
  row label collision   'widget' governs constants on one sheet and
                        formulas on two
  companion absence     Inputs!B9 sits alone, outside the label block;
                        Inputs!B2 has a unit in its header, a date, an n
                        and an sd across its row, and must report nothing
                        missing
  radius sensitivity    Inputs!B12 is a bare "n = 12" note three rows
                        below B9: reached at radius 3, not at radius 2
  depth chain           Inputs!B2 -> Model!B2 -> Model!C2 -> Summary!B2

CC0. stdlib only. Parses under Python 3.9.
"""

import sys
import zipfile

# sheet -> {address: (kind, value)} or, for a formula, (kind, value, cached)
# kind: 't' inline text, 'n' number, 'd' date serial, 'f' formula
#
# A formula cell may carry a THIRD element: the value Excel would have
# cached for it. Without one the writer emits <v>0</v>, which is fine for
# reading formulas and useless for checking an evaluator -- coupling.py's
# verify() compares against exactly that cache, so a fixture with a fake
# one cannot test it in either direction.
SHEETS = [
    ("Inputs", {
        "A1": ("t", "item"),      "B1": ("t", "unit price (USD)"),
        "C1": ("t", "as of"),     "D1": ("t", "n"),
        "E1": ("t", "sd"),        "F1": ("t", "total"),
        "A2": ("t", "widget"),    "B2": ("n", "12.5"),
        "C2": ("d", "45000"),     "D2": ("n", "30"),
        "E2": ("n", "1.2"),       "F2": ("n", "375"),
        "A3": ("t", "gadget"),    "B3": ("n", "8.0"),
        "C3": ("d", "45010"),     "D3": ("n", "25"),
        "E3": ("n", "0.9"),       "F3": ("n", "200"),
        "B9": ("n", "42"),
        "B12": ("t", "n = 12"),
    }),
    ("Model", {
        "A1": ("t", "item"),      "B1": ("t", "unit price"),
        "C1": ("t", "total"),     "D1": ("t", "margin"),
        "A2": ("t", "widget"),    "B2": ("f", "Inputs!B2*1.1"),
        "C2": ("f", "B2*Inputs!D2"), "D2": ("f", "C2*0.1"),
        "A3": ("t", "gadget"),    "B3": ("f", "Inputs!B3*1.1"),
        "C3": ("f", "B3*Inputs!D3"), "D3": ("f", "C3*0.1"),
    }),
    ("Summary", {
        "A1": ("t", "item"),      "B1": ("t", "total"),
        "A2": ("t", "widget"),    "B2": ("f", "Model!C2"),
        "A3": ("t", "gadget"),    "B3": ("f", "Model!C3"),
    }),
]

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
%s</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="1"><fill><patternFill patternType="none"/></fill></fills>
<borders count="1"><border/></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="2">
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="14" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>
</cellXfs>
</styleSheet>"""


def _esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _sheet_xml(cellmap):
    rows = {}
    for addr, spec in cellmap.items():
        kind, val = spec[0], spec[1]
        cached = spec[2] if len(spec) > 2 else 0
        i = 0
        while i < len(addr) and addr[i].isalpha():
            i += 1
        rows.setdefault(int(addr[i:]), []).append(
            (addr[:i], addr, kind, val, cached))
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
           '<worksheet xmlns="http://schemas.openxmlformats.org/'
           'spreadsheetml/2006/main"><sheetData>']
    for r in sorted(rows):
        out.append('<row r="%d">' % r)
        for col, addr, kind, val, cached in sorted(
                rows[r], key=lambda t: (len(t[0]), t[0])):
            if kind == "t":
                out.append('<c r="%s" t="inlineStr"><is><t>%s</t></is></c>'
                           % (addr, _esc(val)))
            elif kind == "d":
                out.append('<c r="%s" s="1"><v>%s</v></c>' % (addr, val))
            elif kind == "f":
                out.append('<c r="%s"><f>%s</f><v>%s</v></c>'
                           % (addr, _esc(val), cached))
            else:
                out.append('<c r="%s"><v>%s</v></c>' % (addr, val))
        out.append("</row>")
    out.append("</sheetData></worksheet>")
    return "".join(out)


def write_demo(path, sheets=None):
    sheets = sheets if sheets is not None else SHEETS
    overrides = "".join(
        '<Override PartName="/xl/worksheets/sheet%d.xml" ContentType='
        '"application/vnd.openxmlformats-officedocument.spreadsheetml.'
        'worksheet+xml"/>\n' % (i + 1) for i in range(len(sheets)))
    wb = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
          '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/'
          '2006/main" xmlns:r="http://schemas.openxmlformats.org/'
          'officeDocument/2006/relationships"><sheets>']
    rels = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships">']
    for i, (name, _) in enumerate(sheets):
        wb.append('<sheet name="%s" sheetId="%d" r:id="rId%d"/>'
                  % (_esc(name), i + 1, i + 1))
        rels.append('<Relationship Id="rId%d" Type="http://schemas.'
                    'openxmlformats.org/officeDocument/2006/relationships/'
                    'worksheet" Target="worksheets/sheet%d.xml"/>'
                    % (i + 1, i + 1))
    wb.append("</sheets></workbook>")
    rels.append('<Relationship Id="rIdS" Type="http://schemas.openxmlformats.'
                'org/officeDocument/2006/relationships/styles" '
                'Target="styles.xml"/>')
    rels.append("</Relationships>")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES % overrides)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("xl/workbook.xml", "".join(wb))
        z.writestr("xl/_rels/workbook.xml.rels", "".join(rels))
        z.writestr("xl/styles.xml", STYLES)
        for i, (_, cm) in enumerate(sheets):
            z.writestr("xl/worksheets/sheet%d.xml" % (i + 1), _sheet_xml(cm))
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "demo.xlsx"
    print(write_demo(out))
