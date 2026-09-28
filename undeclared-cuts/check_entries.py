#!/usr/bin/env python3
"""check_entries.py -- header validation for entries/, and the REGISTRY writer.

WHAT IT DOES
    Reads every entries/*.md, parses the leading header block, and reports
    per entry which required keys are absent or empty. Writes REGISTRY.txt.

WHAT IT DOES NOT DO
    No scoring. No ranking. No interpretation of any header VALUE beyond
    membership in a closed vocabulary where the spec declares one. It does
    not read entry bodies at all.

    UNSET / UNOWNED / NONE_KNOWN are VALID values. The check is that a key
    was DECLARED, not that it was filled. An entry every one of whose
    optional-sentinel fields reads UNSET passes.

HEADER BLOCK
    The leading contiguous run of lines at the top of the file, after any
    blank lines, ending at the first blank line. Every line in it must be
    "key: value". A line that is not turns the whole block MALFORMED and
    the file is reported with the offending line number; nothing is
    inferred from a malformed block.

EXIT
    0   every entry carries all required keys, non-empty
    1   at least one entry is incomplete or malformed
    2   invoked with --selftest (checks live in test_entries.py)
    3   entries/ absent or unreadable

USAGE
    python3 check_entries.py                 report + write REGISTRY.txt
    python3 check_entries.py --no-write      report only
    python3 check_entries.py --dir DIR       read entries from DIR
"""

import os
import sys

REQUIRED = (
    "id",
    "title",
    "status",
    "term_status",
    "measurand",
    "control",
    "scope_limits",
    "thin_links",
    "would_change",
    "reinspect",
    "owner",
    "decay_class",
)

# Closed vocabularies the spec declares. Membership is a STRUCTURAL check --
# it asks whether the token is one the schema defines, never whether the
# choice was a good one. A key with no entry here takes any non-empty value.
VOCAB = {
    "status": ("NOT_MEASURED", "UNDERMEASURED", "OBSERVED", "HELD", "PROPOSED"),
    "term_status": ("NAMED", "UNNAMED"),
    "decay_class": ("COUPLED", "CONTINUOUS", "REVISABLE", "CONSTITUTIVE", "UNSET"),
}

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_DIR = os.path.join(HERE, "entries")
REGISTRY = os.path.join(HERE, "REGISTRY.txt")


class Report(object):
    """One file's result. Nothing here is a judgement about content."""

    def __init__(self, path):
        self.path = path
        self.header = {}
        self.lines = {}          # key -> 1-based line number
        self.missing = []        # required key absent entirely
        self.empty = []          # (key, line) present with no value
        self.duplicate = []      # (key, line) second and later occurrences
        self.off_vocab = []      # (key, line, value) not in a declared vocabulary
        self.malformed = None    # (line_number, text) or None

    @property
    def complete(self):
        return not (self.missing or self.empty or self.duplicate
                    or self.off_vocab or self.malformed)

    def get(self, key):
        return self.header.get(key, "")


def read_header(path):
    """Parse the leading header block. Returns a Report.

    A header line is "key: value". The key is everything before the first
    colon, stripped; the value everything after, stripped. An empty value
    is recorded as PRESENT-AND-EMPTY, which is a different finding from
    absent and is reported as such.
    """
    rep = Report(path)
    with open(path, "r") as fh:
        raw = fh.read().split("\n")

    i = 0
    while i < len(raw) and raw[i].strip() == "":
        i += 1

    while i < len(raw):
        line = raw[i]
        if line.strip() == "":
            break
        if ":" not in line:
            rep.malformed = (i + 1, line.rstrip())
            return rep
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key == "" or " " in key:
            rep.malformed = (i + 1, line.rstrip())
            return rep
        if key in rep.header:
            rep.duplicate.append((key, i + 1))
        else:
            rep.header[key] = value
            rep.lines[key] = i + 1
        i += 1

    for key in REQUIRED:
        if key not in rep.header:
            rep.missing.append(key)
        elif rep.header[key] == "":
            rep.empty.append((key, rep.lines[key]))

    for key, allowed in VOCAB.items():
        if key in rep.header and rep.header[key] != "":
            if rep.header[key] not in allowed:
                rep.off_vocab.append((key, rep.lines[key], rep.header[key]))

    return rep


def entry_paths(directory):
    if not os.path.isdir(directory):
        return None
    names = [n for n in os.listdir(directory) if n.endswith(".md")]
    names.sort()
    return [os.path.join(directory, n) for n in names]


def check_all(directory):
    paths = entry_paths(directory)
    if paths is None:
        return None
    return [read_header(p) for p in paths]


def render(reports, directory):
    out = []
    out.append("check_entries.py")
    out.append("entries dir: %s" % directory)
    out.append("entries read: %d" % len(reports))
    out.append("required keys: %d" % len(REQUIRED))
    out.append("")

    for rep in reports:
        rel = os.path.basename(rep.path)
        if rep.complete:
            out.append("OK          %s" % rel)
            continue
        out.append("INCOMPLETE  %s" % rel)
        if rep.malformed is not None:
            ln, text = rep.malformed
            out.append("    malformed header line   %s:%d   %s"
                       % (rel, ln, text))
            continue
        for key in rep.missing:
            out.append("    key absent              %s   (no line)" % key)
        for key, ln in rep.empty:
            out.append("    key present, empty      %s   %s:%d" % (key, rel, ln))
        for key, ln in rep.duplicate:
            out.append("    key repeated            %s   %s:%d" % (key, rel, ln))
        for key, ln, value in rep.off_vocab:
            out.append("    value off vocabulary    %s   %s:%d   %r"
                       % (key, rel, ln, value))

    out.append("")
    ok = sum(1 for r in reports if r.complete)
    out.append("complete: %d of %d" % (ok, len(reports)))
    out.append("")
    out.append("UNSET / UNOWNED / NONE_KNOWN are valid values. This check asks")
    out.append("whether a key was declared, never whether it was filled.")
    return "\n".join(out)


def registry_text(reports):
    rows = []
    for rep in reports:
        rows.append((
            rep.get("id") or "(no id)",
            rep.get("title") or "(no title)",
            rep.get("status") or "(no status)",
            rep.get("owner") or "(no owner)",
        ))
    rows.sort(key=lambda r: r[0])

    head = ("id", "title", "status", "owner")
    widths = [len(h) for h in head]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt(row):
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip()

    out = []
    out.append("REGISTRY.txt -- generated by check_entries.py; do not hand-edit.")
    out.append("")
    out.append(fmt(head))
    out.append("  ".join("-" * w for w in widths))
    for row in rows:
        out.append(fmt(row))
    out.append("")
    out.append("%d entries." % len(rows))
    out.append("Every entry here is an instrument that has not been run.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "check_entries.py carries no selftest.\n"
            "Run: python3 test_entries.py\n")
        return 2

    directory = ENTRY_DIR
    if "--dir" in argv:
        directory = argv[argv.index("--dir") + 1]
    write = "--no-write" not in argv

    reports = check_all(directory)
    if reports is None:
        sys.stderr.write("entries directory not found: %s\n" % directory)
        return 3

    print(render(reports, directory))

    if write:
        target = REGISTRY
        if directory != ENTRY_DIR:
            target = os.path.join(os.path.dirname(directory) or ".", "REGISTRY.txt")
        with open(target, "w") as fh:
            fh.write(registry_text(reports))
        print("")
        print("wrote %s" % target)

    return 0 if all(r.complete for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
