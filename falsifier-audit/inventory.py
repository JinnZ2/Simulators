#!/usr/bin/env python3
"""inventory.py -- run FIRST. Scans the tree and reports the falsifier
marker FORMS actually present, before any extractor is built around one.
The repos were written over time and the markers vary; this is the
census that justifies which forms extract.py handles.

    python3 inventory.py [root ...]        # default: the checkout root
Stdlib only. Refuses --selftest (checks live in selftest_fa.py).
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E  # noqa: E402

FORMS = {
    "table (falsifier column)": None,     # counted structurally below
    "prose 'Falsified if:'": re.compile(r"\*{0,2}falsified if\*{0,2}\s*:", re.I),
    "prose 'Falsifier:'": re.compile(r"(^|\s)\*{0,2}falsifier\*{0,2}\s*:", re.I),
    "field falsifier_shape/value": re.compile(r"\bfalsifier_(shape|value)\b", re.I),
    "json/yaml \"falsifier\" key": re.compile(r"""["']falsifier["']\s*:""", re.I),
    "block label FALSIFIER": re.compile(r"^\s*FALSIFIER\b"),
    "section REFUTATION_PROTOCOL": re.compile(r"REFUTATION_PROTOCOL"),
}


def inventory(roots=None, exclude=E.SELF_EXCLUDE):
    files = {name: set() for name in FORMS}
    hits = {name: 0 for name in FORMS}
    example = {name: "" for name in FORMS}
    table_rows = 0
    table_files = set()
    for repo, rel, ap, text in E.walk_files(roots, exclude):
        rows = list(E.parse_claim_tables(text))
        if rows:
            table_files.add(rel)
            table_rows += len(rows)
            if not example["table (falsifier column)"]:
                example["table (falsifier column)"] = "%s:%d" % (rel, rows[0]["lineno"])
        for name, pat in FORMS.items():
            if pat is None:
                continue
            n = 0
            for i, line in enumerate(text.splitlines(), 1):
                if pat.search(line):
                    n += 1
                    if not example[name]:
                        example[name] = "%s:%d" % (rel, i)
            if n:
                files[name].add(rel)
                hits[name] += n
    files["table (falsifier column)"] = table_files
    hits["table (falsifier column)"] = table_rows
    return {"forms": {name: {"files": len(files[name]), "hits": hits[name], "example": example[name]}
                      for name in FORMS}, "table_data_rows": table_rows}


def render(roots=None):
    inv = inventory(roots)
    L = ["falsifier marker inventory (run first)"]
    L.append("%-32s %7s %7s   %s" % ("form", "files", "hits", "example"))
    for name, d in inv["forms"].items():
        L.append("%-32s %7d %7d   %s" % (name, d["files"], d["hits"], d["example"]))
    L.append("extract.py builds records around the two forms that carry an attached claim on")
    L.append("the same structure: the table column, and prose 'Falsified if:'. The others are")
    L.append("counted here and not extracted (a field spec or a work-order block label attaches")
    L.append("its falsifier differently); that is a coverage statement, not a judgement.")
    return "\n".join(L)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("inventory has no selftest; run selftest_fa.py", file=sys.stderr)
        return 2
    roots = [a for a in argv if not a.startswith("-")] or None
    print(render(roots))
    return 0


if __name__ == "__main__":
    sys.exit(main())
