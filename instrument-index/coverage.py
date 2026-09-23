#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
coverage.py -- the consuming side of INSTRUMENT-INDEX.tsv (INDEX-SPEC.md).

Two subcommands, one per half of the measurand:

    select   SELECTION.  Given the shape(s) of what the reader is holding,
             list the instruments whose input_shape includes one of them.
             UNRATED rows are never selected and are COUNTED, because a row
             that cannot be selected by shape is a row the reader has to
             read to know about, and that number belongs in the output.

    declare  COVERAGE.  Emit the six-line block every assessment that uses
             the index carries:

                 INDEX-VERSION: ...
                 APPLICABLE:    n  ids: ...
                 RUN:           n  ids: ...
                 OMITTED:       n  ids: ...
                 OMIT-REASON:   CONTEXT_BUDGET | NOT_APPLICABLE | TOOL_FAILED | UNREAD
                 INDEX-GAP:     ...

             OMITTED is COMPUTED as APPLICABLE minus RUN, never typed. An
             OMITTED set with no reason REFUSES; RUN not a subset of
             APPLICABLE refuses; an id in APPLICABLE or RUN that the index
             does not carry is moved to INDEX-GAP rather than counted, and
             the move is printed. INDEX-GAP is the return path -- the one
             line where the consumer reports back on the index.

What this does NOT do: it does not decide what is applicable. The reader
declares that. The tool holds the reader to the arithmetic and to the
index that was actually loaded, and it stamps which index that was.

CC0. Stdlib only. Parses under Python 3.9. No network.
"""

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_index as BI   # noqa: E402  (read_tsv, INPUT_SHAPES, UNRATED)

OMIT_REASONS = ("CONTEXT_BUDGET", "NOT_APPLICABLE", "TOOL_FAILED", "UNREAD")
DEFAULT_INDEX = os.path.join(HERE, "INSTRUMENT-INDEX.tsv")


class DeclarationRefused(Exception):
    """A coverage block that would misstate the arithmetic or the reason."""


def load_index(path=DEFAULT_INDEX):
    with io.open(path, encoding="utf-8") as fh:
        return BI.read_tsv(fh.read())


def index_version(rows):
    """One `repo@built_against` per repo, NOT-SCANNED repos carried as such.
    The version of an index with a NOT-SCANNED repo in it is not the version
    of a whole index, and the string says so."""
    seen = {}
    for r in rows:
        seen.setdefault(r["repo"], r["built_against"])
    return ";".join("%s@%s" % (k, seen[k]) for k in sorted(seen))


def select(rows, shapes):
    """Rows whose input_shape carries ANY of `shapes`. Returns
    (selected_rows, unrated_count, not_scanned_repos)."""
    for s in shapes:
        if s not in BI.INPUT_SHAPES:
            raise DeclarationRefused("shape %r not in the input_shape enum %r"
                                     % (s, BI.INPUT_SHAPES))
    want = set(shapes)
    sel, unrated, not_scanned = [], 0, []
    for r in rows:
        if r["path"] == BI.NOT_SCANNED:
            not_scanned.append(r["repo"])
            continue
        if r["input_shape"] == BI.UNRATED:
            unrated += 1
            continue
        if want & set(r["input_shape"].split("|")):
            sel.append(r)
    return sel, unrated, not_scanned


def declare(rows, applicable, run, omit_reason=None, expected=()):
    """Compute the coverage block. Raises DeclarationRefused on arithmetic
    that would misstate coverage. Returns a dict; render() prints it."""
    ids = {r["id"] for r in rows if r["path"] != BI.NOT_SCANNED}
    applicable = list(dict.fromkeys(applicable))
    run = list(dict.fromkeys(run))
    gap = [i for i in list(applicable) + list(run) + list(expected)
           if i not in ids]
    gap = list(dict.fromkeys(gap))
    moved = [i for i in gap if i in applicable or i in run]
    applicable = [i for i in applicable if i in ids]
    run = [i for i in run if i in ids]
    not_in_applicable = [i for i in run if i not in applicable]
    if not_in_applicable:
        raise DeclarationRefused(
            "RUN carries ids not declared APPLICABLE: %s. An instrument that "
            "was run was applicable; declare it, do not let RUN exceed the "
            "denominator." % not_in_applicable)
    omitted = [i for i in applicable if i not in run]
    if omitted and not omit_reason:
        raise DeclarationRefused(
            "%d applicable instrument(s) not run and no OMIT-REASON given: %s. "
            "The discard is permitted; the discard without a record is what "
            "this block exists to prevent." % (len(omitted), omitted))
    if omit_reason is not None and omit_reason not in OMIT_REASONS:
        raise DeclarationRefused("OMIT-REASON %r not in %r"
                                 % (omit_reason, OMIT_REASONS))
    if not omitted and omit_reason:
        # A reason with nothing to explain is recorded as such, not dropped:
        # the reader typed it and the block shows it did no work.
        pass
    return {"index_version": index_version(rows),
            "applicable": applicable, "run": run, "omitted": omitted,
            "omit_reason": omit_reason if omitted else None,
            "index_gap": gap, "moved_to_gap": moved}


def render(block):
    L = []
    L.append("INDEX-VERSION: %s" % block["index_version"])
    L.append("APPLICABLE:    %d  ids: %s"
             % (len(block["applicable"]), ", ".join(block["applicable"]) or "-"))
    L.append("RUN:           %d  ids: %s"
             % (len(block["run"]), ", ".join(block["run"]) or "-"))
    L.append("OMITTED:       %d  ids: %s"
             % (len(block["omitted"]), ", ".join(block["omitted"]) or "-"))
    L.append("OMIT-REASON:   %s" % (block["omit_reason"] or "-"))
    L.append("INDEX-GAP:     %s" % (", ".join(block["index_gap"]) or "-"))
    if block["moved_to_gap"]:
        L.append("# note: %d id(s) declared applicable or run are not in the "
                 "loaded index and were moved to INDEX-GAP, not counted: %s"
                 % (len(block["moved_to_gap"]), ", ".join(block["moved_to_gap"])))
    return "\n".join(L) + "\n"


def render_select(sel, unrated, not_scanned, shapes):
    L = ["SELECT shape in {%s}" % ", ".join(shapes),
         "applicable: %d" % len(sel)]
    for r in sel:
        L.append("  %-58s %-24s tok~%-6s cost %-9s gate %s"
                 % (r["id"], r["input_shape"], r["load_tok_est"],
                    r["run_cost"], r["gate"]))
    L.append("UNRATED rows not selectable by shape: %d  (read the list to "
             "know about them)" % unrated)
    if not_scanned:
        L.append("repos NOT-SCANNED in this index: %s" % ", ".join(not_scanned))
    L.append("load_tok_est is bytes/4, an ESTIMATE.")
    return "\n".join(L) + "\n"


def _split(v):
    return [x for x in (v or "").split(",") if x]


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "coverage.py has no --selftest. The checks are in "
            "test_index.py:\n    python3 %s\n"
            % os.path.join(HERE, "test_index.py"))
        return 2
    if not argv or argv[0] not in ("select", "declare"):
        sys.stderr.write(__doc__)
        return 2
    cmd = argv[0]
    index = DEFAULT_INDEX
    shapes, applicable, run, expected, reason = [], [], [], [], None
    i = 1
    while i < len(argv):
        a = argv[i]
        nxt = argv[i + 1] if i + 1 < len(argv) else None
        if a == "--index":
            index = nxt; i += 1
        elif a == "--shape":
            shapes = _split(nxt); i += 1
        elif a == "--applicable":
            applicable = _split(nxt); i += 1
        elif a == "--run":
            run = _split(nxt); i += 1
        elif a == "--expected":
            expected = _split(nxt); i += 1
        elif a == "--omit-reason":
            reason = nxt; i += 1
        else:
            sys.stderr.write("unknown argument %r\n" % a)
            return 2
        i += 1
    try:
        rows = load_index(index)
        if cmd == "select":
            if not shapes:
                raise DeclarationRefused("select needs --shape")
            sel, unrated, ns = select(rows, shapes)
            sys.stdout.write(render_select(sel, unrated, ns, shapes))
        else:
            block = declare(rows, applicable, run, reason, expected)
            sys.stdout.write(render(block))
    except (DeclarationRefused, BI.BuildRefused) as ex:
        sys.stderr.write("REFUSED: %s\n" % ex)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
