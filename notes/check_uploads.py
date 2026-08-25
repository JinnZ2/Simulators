"""Check a re-obtained copy of a filed dataset against what was recorded.

notes/datasets/uploads_2026_08_25.md indexes four files whose bytes are
not in this repository. The bytes were measured once, on the day they
arrived, and then the container that held them was reclaimed. This module
is what makes that entry checkable afterwards: point it at a directory
holding a re-obtained copy and it reports, per recorded file, whether
what is on disk is the same object.

Three states, not two:

    PRESENT_MATCH    found, sha256 equal, shape re-derives
    PRESENT_DIFFERS  found by name, and it is not the recorded bytes
    NOT_PRESENT      no candidate found

NOT_PRESENT is not a pass. A checker that silently returns clean when
there is nothing to check reports on the caller's directory listing and
not on the file, and this repository has recorded that repair often
enough (PB_004, GC_004, MD_002, CC_002, CR_027, FM_005) that it is built
in here rather than found later.

The shape numbers are re-derived rather than trusted: a file can carry
the recorded size and still not be the recorded file, and a hash match
plus a shape mismatch would mean this module's own derivation had
drifted. Both are reported.

Usage
    python3 check_uploads.py --selftest
    python3 check_uploads.py --check DIR
"""

import csv
import hashlib
import io
import os
import re
import sys
import zipfile

ENTRY = "notes/datasets/uploads_2026_08_25.md"

PRESENT_MATCH = "PRESENT_MATCH"
PRESENT_DIFFERS = "PRESENT_DIFFERS"
NOT_PRESENT = "NOT_PRESENT"


# ---------------------------------------------------------------- shapes

def shape_practice_zip(path):
    """Zip entries (directories included) and formula cells.

    `entries` is deliberately not called `members`: shape_uci_zip counts
    files only, and two different quantities under one key name is the
    kind of thing someone later divides one by the other.
    """
    out = {}
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        out["entries"] = len(names)
        books = [n for n in names if n.lower().endswith(".xlsx")]
        out["xlsx"] = len(books)
        f_cells = []
        for n in books:
            inner = zipfile.ZipFile(io.BytesIO(z.read(n)))
            for m in inner.namelist():
                if re.match(r"xl/worksheets/sheet\d+\.xml$", m):
                    s = inner.read(m).decode("utf8", "replace")
                    f_cells.extend(re.findall(r'<c r="([A-Z]+\d+)"[^>]*>'
                                              r'<f[^>]*>', s))
        out["formula_cells"] = len(f_cells)
    return out


def shape_epa_xlsx(path):
    with zipfile.ZipFile(path) as z:
        wb = z.read("xl/workbook.xml").decode("utf8", "replace")
        sheets = re.findall(r'<sheet name="([^"]+)"', wb)
        s = z.read("xl/worksheets/sheet1.xml").decode("utf8", "replace")
        return {
            "sheets": len(sheets),
            "sheet_name": sheets[0] if sheets else "",
            "rows": len(re.findall(r"<row ", s)),
            "hyperlinks": len(re.findall(r"<hyperlink ", s)),
            "formula_cells": len(re.findall(r"<f[ />]", s)),
        }


def shape_uci_zip(path):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        return {"members": len(names), "names": sorted(names)}


def shape_wb_csv(path):
    fh = open(path, newline="", encoding="utf-8-sig")
    try:
        r = csv.reader(fh)
        head = next(r)
        rows = sum(1 for _ in r)
    finally:
        fh.close()
    return {"cols": len(head), "rows": rows, "first_col": head[0]}


SHAPES = {
    "practice_zip": shape_practice_zip,
    "epa_xlsx": shape_epa_xlsx,
    "uci_zip": shape_uci_zip,
    "wb_csv": shape_wb_csv,
}


# ---------------------------------------------------------------- record

RECORD = [
    {
        "id": "practice_datasets_for_excel",
        "sha256": "e1d498901b15cc558589c576a433a6fa2a0183f677979aa"
                  "7603c1f4fd884132d",
        "size": 14326846,
        "match": r"PracticeDatasetsforExcel.*\.zip$",
        "shape_fn": "practice_zip",
        "shape": {"entries": 61, "xlsx": 26, "formula_cells": 3},
    },
    {
        "id": "epa_safer_choice_dfe",
        "sha256": "32b170f44d906be06ec48346dfdce5eb67a87e427a20fc0a"
                  "1bfa8bb92baeff9a",
        "size": 327250,
        "match": r"\.xlsx$",
        "shape_fn": "epa_xlsx",
        "shape": {
            "sheets": 1,
            "sheet_name": "t_safer_choice_and_design_for_t",
            "rows": 4969,
            "hyperlinks": 4968,
            "formula_cells": 0,
        },
    },
    {
        "id": "uci_mechanical_analysis",
        "sha256": "efe80d7c384b38518333d4c6e7f9f0333d261440953760d8"
                  "53a7e294077f4a78",
        "size": 1774660,
        "match": r"mechanicalanalysis.*\.zip$",
        "shape_fn": "uci_zip",
        "shape": {
            "members": 7,
            "names": [
                "Index",
                "PUMPS-DATA-SET/DISTRIBUTION.Z",
                "PUMPS-DATA-SET/Index",
                "older-version/Index",
                "older-version/mechanical-analysis.data",
                "older-version/mechanical-analysis.names",
                "older-version/mechanical-analysis.notused-instances",
            ],
        },
    },
    {
        "id": "world_bank_data_catalog",
        "sha256": "3baefe4d06a597cfece21c499395692a354dc6b766e8dd8e"
                  "abf6195836271a92",
        "size": 164877,
        "match": r"world_bank_data_catalog.*\.csv$",
        "shape_fn": "wb_csv",
        "shape": {"cols": 26, "rows": 160, "first_col": "DataCatalog_id"},
    },
]


# ---------------------------------------------------------------- engine

def sha256(path):
    h = hashlib.sha256()
    fh = open(path, "rb")
    try:
        while True:
            b = fh.read(1 << 20)
            if not b:
                break
            h.update(b)
    finally:
        fh.close()
    return h.hexdigest()


def candidates(directory, pattern):
    if not os.path.isdir(directory):
        return []
    rx = re.compile(pattern)
    out = []
    for n in sorted(os.listdir(directory)):
        p = os.path.join(directory, n)
        if os.path.isfile(p) and rx.search(n):
            out.append(p)
    return out


def diff_shape(want, got):
    """Keys that disagree. A key absent from got counts as a disagreement."""
    bad = []
    for k in sorted(want):
        if k not in got:
            bad.append((k, want[k], "ABSENT"))
        elif got[k] != want[k]:
            bad.append((k, want[k], got[k]))
    return bad


def check_one(rec, directory):
    row = {
        "id": rec["id"],
        "state": NOT_PRESENT,
        "path": None,
        "size": None,
        "sha256": None,
        "shape_diff": None,
        "shape_error": None,
    }
    found = candidates(directory, rec["match"])
    if not found:
        return row

    # Prefer a candidate whose bytes match; otherwise report the first.
    chosen = None
    for p in found:
        if sha256(p) == rec["sha256"]:
            chosen = p
            break
    if chosen is None:
        chosen = found[0]

    row["path"] = chosen
    row["size"] = os.path.getsize(chosen)
    row["sha256"] = sha256(chosen)
    if row["sha256"] != rec["sha256"]:
        row["state"] = PRESENT_DIFFERS
        return row

    row["state"] = PRESENT_MATCH
    try:
        got = SHAPES[rec["shape_fn"]](chosen)
    except Exception as exc:                      # noqa: BLE001
        row["shape_error"] = "%s: %s" % (type(exc).__name__, exc)
        return row
    row["shape_diff"] = diff_shape(rec["shape"], got)
    return row


def check(directory):
    return [check_one(r, directory) for r in RECORD]


def report(rows, directory):
    out = []
    out.append("CHECK UPLOADS")
    out.append("entry:     %s" % ENTRY)
    out.append("directory: %s" % directory)
    out.append("")
    out.append("%-32s %-16s %s" % ("id", "state", "detail"))
    out.append("-" * 78)
    for r in rows:
        if r["state"] == NOT_PRESENT:
            detail = "no candidate matched"
        elif r["state"] == PRESENT_DIFFERS:
            detail = "size %d, sha256 %s..." % (r["size"], r["sha256"][:12])
        elif r["shape_error"]:
            detail = "bytes match, shape not derivable (%s)" % r["shape_error"]
        elif r["shape_diff"]:
            detail = "bytes match, shape differs on %s" % ", ".join(
                k for k, _, _ in r["shape_diff"])
        else:
            detail = "bytes and shape as recorded"
        out.append("%-32s %-16s %s" % (r["id"], r["state"], detail))
    for r in rows:
        if r["shape_diff"]:
            out.append("")
            out.append("%s shape:" % r["id"])
            for k, want, got in r["shape_diff"]:
                out.append("  %-14s recorded %r  derived %r" % (k, want, got))
    out.append("")
    n = len(rows)
    tally = {}
    for r in rows:
        tally[r["state"]] = tally.get(r["state"], 0) + 1
    out.append("n = %d   %s" % (n, "   ".join(
        "%s %d" % (k, tally[k]) for k in sorted(tally))))
    out.append("")
    out.append("NOT_PRESENT is not a pass. It reports that this run had")
    out.append("nothing to compare, which is a fact about the directory.")
    return "\n".join(out)


# -------------------------------------------------------------- selftest

def _mini_zip(path, members):
    with zipfile.ZipFile(path, "w") as z:
        for n, data in members:
            z.writestr(n, data)


def _mini_csv(path, cols, rows):
    fh = open(path, "w", newline="", encoding="utf-8")
    try:
        w = csv.writer(fh)
        w.writerow(cols)
        for i in range(rows):
            w.writerow([i] + [""] * (len(cols) - 1))
    finally:
        fh.close()


def selftest():
    import tempfile
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    tmp = tempfile.mkdtemp()

    # -- known answers for the shape derivations, on files built here
    # with counts fixed in advance.
    zp = os.path.join(tmp, "ka.zip")
    _mini_zip(zp, [("Index", b"x"), ("a/Index", b"y"), ("a/b.data", b"z")])
    chk("uci shape counts members, not dirs",
        shape_uci_zip(zp)["members"] == 3)
    chk("uci shape lists sorted names",
        shape_uci_zip(zp)["names"] == ["Index", "a/Index", "a/b.data"])

    cp = os.path.join(tmp, "ka.csv")
    _mini_csv(cp, ["DataCatalog_id", "Name", "Acronym"], 7)
    s = shape_wb_csv(cp)
    chk("csv shape cols", s["cols"] == 3)
    chk("csv shape rows excludes header", s["rows"] == 7)
    chk("csv shape first col", s["first_col"] == "DataCatalog_id")

    # A BOM must not become part of the first column name -- the real
    # file has one, and reading it as utf-8 would put  in the key.
    fh = open(cp, "w", encoding="utf-8-sig", newline="")
    fh.write("DataCatalog_id,Name\r\n1,x\r\n")
    fh.close()
    chk("csv shape strips BOM", shape_wb_csv(cp)["first_col"]
        == "DataCatalog_id")

    # -- diff_shape: absent key is a disagreement, not a skip
    chk("diff_shape absent key",
        diff_shape({"a": 1}, {})[0][2] == "ABSENT")
    chk("diff_shape equal is empty",
        diff_shape({"a": 1}, {"a": 1, "b": 2}) == [])
    chk("diff_shape unequal",
        diff_shape({"a": 1}, {"a": 2})[0] == ("a", 1, 2))

    # -- the three states, each reached
    d = os.path.join(tmp, "dir")
    os.mkdir(d)

    rec = {
        "id": "probe",
        "sha256": None,
        "size": None,
        "match": r"probe.*\.zip$",
        "shape_fn": "uci_zip",
        "shape": {"members": 3},
    }

    chk("empty dir gives NOT_PRESENT",
        check_one(rec, d)["state"] == NOT_PRESENT)
    chk("missing dir gives NOT_PRESENT",
        check_one(rec, os.path.join(tmp, "nope"))["state"] == NOT_PRESENT)

    good = os.path.join(d, "probe_a.zip")
    _mini_zip(good, [("Index", b"x"), ("a/Index", b"y"), ("a/b.data", b"z")])
    rec["sha256"] = sha256(good)
    rec["size"] = os.path.getsize(good)
    r = check_one(rec, d)
    chk("matching bytes give PRESENT_MATCH", r["state"] == PRESENT_MATCH)
    chk("matching bytes give empty shape diff", r["shape_diff"] == [])

    # A file that matches the name pattern and not the bytes.
    other = os.path.join(d, "probe_b.zip")
    _mini_zip(other, [("Index", b"different")])
    rec2 = dict(rec, match=r"probe_b.*\.zip$")
    chk("differing bytes give PRESENT_DIFFERS",
        check_one(rec2, d)["state"] == PRESENT_DIFFERS)

    # With both present, the matching one is chosen over the first by name.
    r = check_one(rec, d)
    chk("chooses the matching candidate, not the first listed",
        r["state"] == PRESENT_MATCH and r["path"] == good)

    # -- bytes right, shape recorded wrong: reported, not swallowed
    rec3 = dict(rec, shape={"members": 99})
    r = check_one(rec3, d)
    chk("shape mismatch under a byte match is reported",
        r["state"] == PRESENT_MATCH and r["shape_diff"]
        and r["shape_diff"][0][0] == "members")

    # -- a shape function that raises is recorded, not treated as clean
    rec4 = dict(rec, shape_fn="epa_xlsx")
    r = check_one(rec4, d)
    chk("shape error is recorded", r["shape_error"] is not None)
    chk("shape error leaves shape_diff unset", r["shape_diff"] is None)

    # -- the record itself
    chk("record has four entries", len(RECORD) == 4)
    chk("every record names a built shape fn",
        all(r["shape_fn"] in SHAPES for r in RECORD))
    chk("every record carries a 64-hex sha256",
        all(re.match(r"^[0-9a-f]{64}$", r["sha256"]) for r in RECORD))
    chk("record ids are distinct",
        len({r["id"] for r in RECORD}) == len(RECORD))

    # -- the entry this module exists to make checkable
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    entry = os.path.join(root, ENTRY)
    chk("the indexed entry is in the tree", os.path.exists(entry))
    if os.path.exists(entry):
        text = open(entry, encoding="utf-8").read()
        chk("every recorded sha256 appears in the entry",
            all(r["sha256"] in text for r in RECORD))
        chk("every recorded size appears in the entry",
            all(str(r["size"]) in text for r in RECORD))

    # -- report renders each state without needing the real files
    rows = [
        {"id": "a", "state": NOT_PRESENT, "path": None, "size": None,
         "sha256": None, "shape_diff": None, "shape_error": None},
        {"id": "b", "state": PRESENT_DIFFERS, "path": "p", "size": 1,
         "sha256": "0" * 64, "shape_diff": None, "shape_error": None},
        {"id": "c", "state": PRESENT_MATCH, "path": "p", "size": 1,
         "sha256": "0" * 64, "shape_diff": [], "shape_error": None},
    ]
    txt = report(rows, "dir")
    chk("report names all three states",
        all(s in txt for s in (NOT_PRESENT, PRESENT_DIFFERS, PRESENT_MATCH)))
    chk("report prints n", "n = 3" in txt)
    chk("report says NOT_PRESENT is not a pass",
        "NOT_PRESENT is not a pass" in txt)

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--check" in argv:
        i = argv.index("--check")
        if i + 1 >= len(argv):
            sys.stderr.write("--check needs a directory\n")
            return 2
        d = argv[i + 1]
        print(report(check(d), d))
        return 0
    sys.stderr.write(__doc__.split("Usage")[-1].strip() + "\n")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
