#!/usr/bin/env python3
"""extract.py -- tree walk and FALSIFIER RECORDs. Walks one or more local
repo roots (argv, default the checkout root), reads .md and .py text
files, and pulls every falsifier with its attachment context, verbatim.

The corpus markers vary (see inventory.py). This extractor handles the
two that carry an attached claim on the same structure:
  - markdown claim tables, falsifier found by a HEADER named falsifier /
    "falsified by" / "falsified if" (position varies across the corpus),
    claim by a header named claim / statement / hypothesis / rule;
  - prose "Falsified if:" lines, attached to the nearest claim marker
    above (a bold **ID** line or a heading).

`attach_status: NOT-FOUND` is emitted, never dropped. Nothing is edited;
the tool's own emitted outputs are excluded from the default scan so a
re-run does not read its own queue. Stdlib only.
"""

import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.abspath(os.path.join(HERE, ".."))

SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv",
             ".mypy_cache", ".pytest_cache", ".ruff_cache", "legacy"}
# The tool's own outputs and authored docs, excluded by default: a scan
# that reads its own queue -- or a README/AUDIT_NOTES that quotes a marker
# verbatim to document it -- is the UNI_010 self-reference loop. WORK_ORDER.md
# (the delivered spec) is left scannable; it carries no attachable marker.
SELF_EXCLUDE = (os.path.join("falsifier-audit", "QUEUE.md"),
                os.path.join("falsifier-audit", "README.md"),
                os.path.join("falsifier-audit", "AUDIT_NOTES.md"),
                os.path.join("falsifier-audit", "samples"))

FALSIFIER_HEADERS = ("falsifier", "falsified by", "falsified if", "falsifies", "refuted by")
CLAIM_HEADERS = ("claim", "statement", "hypothesis", "rule", "assertion")
ID_HEADERS = ("id", "claim id", "#")

FALSIFIED_IF = re.compile(r"\*{0,2}falsified if\*{0,2}\s*:\s*(.+)$", re.I)
BOLD_ID = re.compile(r"\*\*([A-Z][A-Za-z]*[_-]?\d[\w.]*)\b.*?\*\*")
HEADING = re.compile(r"^#{1,6}\s+(.*\S)\s*$")


def is_text(path):
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(4096)
        if b"\x00" in chunk:
            return False
        chunk.decode("utf-8")
        return True
    except (OSError, UnicodeDecodeError):
        return False


def walk_files(roots=None, exclude=SELF_EXCLUDE):
    """Yield (repo, relpath, abspath, text) for .md/.py text files under
    each root. `repo` is the top-level folder name under the root (the
    sub-unit); a file at the root has repo '.'."""
    roots = roots or [DEFAULT_ROOT]
    for root in roots:
        root = os.path.abspath(root)
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in sorted(filenames):
                if not fn.endswith((".md", ".py")):
                    continue
                ap = os.path.join(dirpath, fn)
                rel = os.path.relpath(ap, root)
                if any(x in rel for x in exclude):
                    continue
                if not is_text(ap):
                    continue
                repo = rel.split(os.sep)[0] if os.sep in rel else "."
                try:
                    text = open(ap, encoding="utf-8").read()
                except (OSError, UnicodeDecodeError):
                    continue
                yield repo, rel, ap, text


def _cells(line):
    s = line.strip()
    if not s.startswith("|"):
        return None
    inner = s[1:-1] if s.endswith("|") else s[1:]
    return [c.strip() for c in inner.split("|")]


def _is_sep(line):
    c = _cells(line)
    return c is not None and all(re.fullmatch(r":?-{2,}:?", x or "-") for x in c if x != "")


def _header_index(headers, names):
    low = [h.lower() for h in headers]
    for i, h in enumerate(low):
        if h in names:
            return i
    return None


def parse_claim_tables(text):
    """Yield dicts for each data row of a claim table that has a
    falsifier column: {lineno, id, claim, falsifier, headers}."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) - 1:
        cells = _cells(lines[i])
        if cells and len(cells) >= 2 and _is_sep(lines[i + 1]):
            headers = cells
            fi = _header_index(headers, FALSIFIER_HEADERS)
            if fi is not None:
                ci = _header_index(headers, CLAIM_HEADERS)
                idi = _header_index(headers, ID_HEADERS)
                j = i + 2
                while j < len(lines):
                    row = _cells(lines[j])
                    if row is None or _is_sep(lines[j]):
                        break
                    def cell(k):
                        return row[k] if k is not None and k < len(row) else ""
                    yield {"lineno": j + 1, "id": cell(idi) or cell(0),
                           "claim": cell(ci), "falsifier": cell(fi), "headers": headers}
                    j += 1
                i = j
                continue
        i += 1


def _preceding_claim(lines, idx):
    """Nearest claim marker above line idx: a bold **ID ...** or a
    heading. Returns (text, lineno) or (None, None)."""
    for k in range(idx - 1, max(-1, idx - 40), -1):
        m = BOLD_ID.search(lines[k])
        if m:
            return lines[k].strip().strip("*"), k + 1
        h = HEADING.match(lines[k])
        if h and not h.group(1).lower().startswith(("refutation", "status", "claim")):
            return h.group(1), k + 1
    return None, None


def parse_prose(text):
    """Yield dicts for each prose 'Falsified if:' line."""
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        m = FALSIFIED_IF.search(line)
        if not m:
            continue
        claim, cl_ln = _preceding_claim(lines, idx)
        yield {"lineno": idx + 1, "id": "", "claim": claim or "",
               "falsifier": m.group(1).strip().strip("*"), "claim_line": cl_ln}


def rid(repo, rel, lineno):
    return "%s:%s:%d" % (repo, rel.replace(os.sep, "/"), lineno)


def _clean(cell):
    return cell.strip().strip("`").strip()


def records(roots=None, exclude=SELF_EXCLUDE):
    """FALSIFIER RECORDs across the tree. A falsifier cell that is empty
    or bare punctuation (—, -) carries no falsifier and is not a record;
    it is counted in coverage instead."""
    out, empty = [], 0
    for repo, rel, ap, text in walk_files(roots, exclude):
        for r in parse_claim_tables(text):
            fals = _clean(r["falsifier"])
            if len(re.sub(r"[^\w]", "", fals)) < 3:
                empty += 1
                continue
            claim = _clean(r["claim"])
            out.append({"id": rid(repo, rel, r["lineno"]), "row_id": _clean(r["id"]),
                        "text": fals, "attached_to": claim,
                        "attach_status": "LOCATED" if claim else "NOT-FOUND",
                        "repo": repo, "form": "table", "path": rel.replace(os.sep, "/"), "line": r["lineno"]})
        for r in parse_prose(text):
            fals = _clean(r["falsifier"])
            if len(re.sub(r"[^\w]", "", fals)) < 3:
                empty += 1
                continue
            claim = _clean(r["claim"])
            out.append({"id": rid(repo, rel, r["lineno"]), "row_id": "",
                        "text": fals, "attached_to": claim,
                        "attach_status": "LOCATED" if claim else "NOT-FOUND",
                        "repo": repo, "form": "falsified_if", "path": rel.replace(os.sep, "/"), "line": r["lineno"]})
    out.sort(key=lambda r: r["id"])
    return out, empty


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if "--selftest" in argv:
        print("extract has no selftest; run selftest_fa.py", file=sys.stderr)
        return 2
    roots = [a for a in argv if not a.startswith("-")] or None
    recs, empty = records(roots)
    for r in recs:
        print("%-8s %-6s %s" % (r["attach_status"], r["form"], r["id"]))
        print("  falsifier: %s" % r["text"][:160])
        if r["attach_status"] == "LOCATED":
            print("  claim:     %s" % r["attached_to"][:160])
    print("-- %d records, %d empty/punctuation falsifier cells skipped" % (len(recs), empty))
    return 0


if __name__ == "__main__":
    sys.exit(main())
