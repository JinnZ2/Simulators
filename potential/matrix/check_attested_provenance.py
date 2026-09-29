"""check_attested_provenance.py -- the matrix's own [A] PROVENANCE RULE,
applied mechanically to the matrix. P-16 in the work order.

FUNCTIONALITY_MATRIX_COMPLETE.txt states:

    [A] PROVENANCE RULE: every [A] cell ships with whose action, which
    seat, when - or carries the standing note: "attested by the matrix
    author's direct observation; single witness; survivorship applies;
    not independently reproduced."

This scans a matrix text for [A]-tagged cells and reports, per cell,
whether it carries the standing note, whether it carries a date (the
one of the three provenance fields -- whose / seat / when -- that a
scanner can test for without a word list of names and seats), or
neither. It prints a count and line numbers. It rewrites nothing.

What a CELL is here: a field row of the matrix. A row starts at a line
whose text begins at column 2 and runs through the continuation lines
(text at column >= 14) beneath it; a line starting at column 0 (section
rule, section title, blank) ends it. Only lines after the first
section rule are scanned, so the FOOTING KEY, which defines [A] in a
column-2 line, is not counted as a cell.

What a TAG is here: a bracket group in the trailing bracket run of a
line -- `[A]`, `[A][F]`, `[F][A]`, or an unclosed `[A - ...` that runs
to the end of the line. A `[A]` in mid-line prose (`moves [A]/[J] ->
[F]`) is a MENTION of the tag and is not counted (DF_010 / UNI_010:
the document names its own vocabulary, and a scanner that cannot tell
use from mention fires on the definition of the thing it checks).

STATED LIMIT: the date test is a regex for a four-digit year. A cell
carrying "last winter" or "the 2019 outage" as its `when` reads
NO-DATE and DATE respectively; a cell carrying a year that is not its
provenance (a case citation) reads DATE. The count is therefore an
UPPER bound on cells that satisfy the rule by date, and the standing
note test is exact (a literal phrase). Nothing here decides whether a
provenance is true.

Return, per matrix: attested (n), standing_note (n), date (n),
neither (n), and the lines. `unprovenanced_attested(text)` returns the
`neither` count, or None when the document carries no [A] cell at all
-- a document with nothing to check is not a document that passed.

Stdlib only. Parses under 3.9. CC0.
"""

import re
import sys
from pathlib import Path

STANDING_NOTE = "attested by the matrix author"
YEAR = re.compile(r"\b(?:1[89]|20)\d{2}\b")
# trailing bracket run: one or more closed groups, or an unclosed [A - ...
TRAILING = re.compile(r"((?:\[[^\[\]]*\]\s*)+|\[A\s*-[^\]]*)\s*$")
SECTION_RULE = re.compile(r"^=+\s*$")


def _tag_present(line):
    """True if the line's trailing bracket run carries an [A] tag."""
    m = TRAILING.search(line.rstrip())
    if not m:
        return False
    run = m.group(1)
    return bool(re.search(r"\[A(\]|\s*-)", run))


def cells(text):
    """Yield dicts: {start, end, lines, field, section} for every field
    row after the first section rule."""
    lines = text.split("\n")
    started = False
    section = ""
    cur = None
    out = []
    for i, raw in enumerate(lines, 1):
        if SECTION_RULE.match(raw):
            started = True
            if cur:
                out.append(cur); cur = None
            continue
        if not started:
            continue
        if raw.strip() == "" or not raw.startswith(" "):
            # column-0 line: section title, blank, prose paragraph
            if cur:
                out.append(cur); cur = None
            if raw.strip() and not raw.startswith(" "):
                section = raw.strip()
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent <= 6:
            if cur:
                out.append(cur)
            cur = {"start": i, "end": i, "lines": [raw],
                   "field": raw.strip().split("  ")[0][:40], "section": section}
        else:
            if cur is None:
                cur = {"start": i, "end": i, "lines": [raw],
                       "field": "(continuation with no row start)", "section": section}
            else:
                cur["end"] = i
                cur["lines"].append(raw)
    if cur:
        out.append(cur)
    return out


def scan(text):
    rows = []
    for c in cells(text):
        tag_lines = [c["start"] + k for k, l in enumerate(c["lines"]) if _tag_present(l)]
        if not tag_lines:
            continue
        # whitespace-normalized: a tag or a note may wrap across the
        # continuation column, and a phrase split by a newline is the
        # same phrase.
        body = " ".join("\n".join(c["lines"]).split())
        note = STANDING_NOTE in body
        date = bool(YEAR.search(body))
        rows.append({
            "tag_line": tag_lines[0],
            "cell": (c["start"], c["end"]),
            "section": c["section"],
            "field": c["field"],
            "standing_note": note,
            "date": date,
            "neither": not (note or date),
        })
    return {
        "attested": len(rows),
        "standing_note": sum(r["standing_note"] for r in rows),
        "date": sum(r["date"] for r in rows),
        "neither": sum(r["neither"] for r in rows),
        "rows": rows,
    }


def unprovenanced_attested(text):
    """Count of [A] cells carrying neither the standing note nor a date.
    None when the document carries no [A] cell: absent is not zero."""
    r = scan(text)
    if r["attested"] == 0:
        return None
    return r["neither"]


def render(path, r):
    lines = [
        "check_attested_provenance -- %s" % path,
        "",
        "  [A] cells:                 %d" % r["attested"],
        "  carry standing note:       %d" % r["standing_note"],
        "  carry a year (date test):  %d   (upper bound on 'when'; see STATED LIMIT)" % r["date"],
        "  carry NEITHER:             %d" % r["neither"],
        "",
        "  %-6s %-9s %-34s %-22s %s" % ("line", "cell", "section", "field", "provenance"),
    ]
    for row in r["rows"]:
        prov = "standing-note" if row["standing_note"] else ("date" if row["date"] else "NEITHER")
        lines.append("  %-6d %-9s %-34s %-22s %s" % (
            row["tag_line"], "%d-%d" % row["cell"], row["section"][:34], row["field"][:22], prov))
    lines.append("")
    lines.append("  no cell rewritten. a count is what the rule permits a scanner to produce;")
    lines.append("  whose action, which seat, and whether the date is the provenance are readings.")
    return "\n".join(lines)


# --- selftest -------------------------------------------------------------

CONSTRUCTED = """FIXTURE -- constructed, not a matrix about anything
FOOTING KEY
  [A] ATTESTED    first-person action                (key line: NOT a cell)
[A] PROVENANCE RULE: every [A] cell ships ...        (column 0: NOT a cell)

================================================================
F1  A SECTION
================================================================
  purpose       something the author did in 2019 at the
                counter, as the applicant                  [A]
  breaks when   the note case                              [A - attested by the
                matrix author's direct observation; single witness]
  cost bearer   nobody named, no seat, no date             [A][J]
  vertex dep    a finding, not attested                    [F]

================================================================
OPEN CONVERSIONS
================================================================
  C1  Diary study
      -> ease table moves [A]/[J] -> [F]                   (mention, NOT a tag)
"""

NO_ATTESTED = """FIXTURE
================================================================
F1  A SECTION
================================================================
  purpose       a finding                                  [F]
  cost bearer   a judgment                                 [J]
"""


def _selftest():
    checks = 0
    def check(cond, msg):
        nonlocal checks
        checks += 1
        if not cond:
            raise AssertionError(msg)

    r = scan(CONSTRUCTED)
    check(r["attested"] == 3, "expected 3 [A] cells, got %d" % r["attested"])
    check(r["standing_note"] == 1, "standing note count")
    check(r["date"] == 1, "date count")
    check(r["neither"] == 1, "neither count")
    fields = [row["field"] for row in r["rows"]]
    check(any(f.startswith("cost bearer") for f in fields), "the NEITHER cell is named")
    neither = [row for row in r["rows"] if row["neither"]]
    check(len(neither) == 1 and neither[0]["field"].startswith("cost bearer"), "NEITHER lands on the right cell")
    # the key line and the mention are not cells / tags
    check(all(row["section"] != "" for row in r["rows"]), "cells are inside sections")
    check(not any(row["section"] == "OPEN CONVERSIONS" for row in r["rows"]), "a mid-line [A]/[J] mention is not a tag")
    check(_tag_present("  x  [A]") and _tag_present("  x  [A][F]") and _tag_present("  x  [F][A]"), "tag forms")
    check(_tag_present("  x  [A - attested;") , "unclosed [A - runs to EOL")
    check(not _tag_present("      -> ease table moves [A]/[J] -> [F]"), "mention refused")
    check(not _tag_present("  x  [F]"), "[F] alone is not [A]")
    # metric: None vs 0 vs n
    check(unprovenanced_attested(CONSTRUCTED) == 1, "metric on fixture")
    check(unprovenanced_attested(NO_ATTESTED) is None, "no [A] cell is None, not 0")
    all_prov = CONSTRUCTED.replace("nobody named, no seat, no date", "done 2021 by the author at the desk")
    check(unprovenanced_attested(all_prov) == 0, "every cell provenanced is 0, distinct from None")
    # null test: the scanner fires on a plant and is silent on an all-[F] doc
    check(scan(NO_ATTESTED)["attested"] == 0, "silent on a document with no [A]")
    print("checks: %d" % checks)
    print("PASS")
    return 0


def _main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) != 2:
        print(__doc__)
        return 2
    path = Path(argv[1])
    if not path.exists():
        print("missing: %s" % path, file=sys.stderr)
        return 3
    print(render(path, scan(path.read_text())))
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
