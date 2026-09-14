#!/usr/bin/env python3
"""
Parser for WORK_ORDER_V2.md -- the revised order, landed verbatim beside
WORK_ORDER.md so both stay inspectable (the supersession convention this
repository already uses: observer-exclusion SPEC_V2, design-basis
SOURCE_DROP_V2, fold-matrix WORK_ORDER_V2, mining-increment
SOURCE_DROP_V2).

Nothing here is retyped from the order. The gutter parser, the fence
walker, the field-line test and the vocabulary reader are IMPORTED from
entries.py -- one parser, two documents -- so an edit to either that the
parser cannot follow turns the suite red rather than passing against a
stale copy. Only the section walk is new, because v2 adds sections v1
does not have.

The revision is PURELY ADDITIVE against v1: 694 lines inserted, 0 deleted,
0 modified, checked by difflib in test_register_v2.py rather than asserted
here.

CC0. Stdlib only. Parses under 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entries as E                                       # noqa: E402
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))
import sourced as S                                       # noqa: E402

ORDER_NAME = "WORK_ORDER_V2.md"

ORDER_PATH_V2 = os.path.join(HERE, "WORK_ORDER_V2.md")


def order_text():
    with open(ORDER_PATH_V2) as fh:
        return fh.read()


def _lines():
    return order_text().split("\n")


def _section(heading_prefix, stop_prefix=("## ",)):
    """Same walk as entries._section, over v2's lines. The helper there
    binds v1's text through its own _lines(), which is why this one
    exists; everything below it is imported."""
    out, inside = [], False
    for line in _lines():
        if line.startswith(heading_prefix):
            inside = True
            continue
        if inside and any(line.startswith(p) for p in stop_prefix) \
                and not line.startswith(heading_prefix):
            break
        if inside:
            out.append(line)
    if not out:
        raise ValueError("section not found: %r" % heading_prefix)
    return out


# --------------------------------------------------------- 1B  V-MAP

def v_definitions():
    """[(id, name, gloss)] from the first fence of section 1B."""
    lines = _section("## 1B. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    out = []
    for line in block:
        if not line.strip():
            continue
        vid = line.split()[0]
        rest = line[len(vid):].strip()
        # name is the ALL-CAPS run, gloss is what follows
        words, name = rest.split(), []
        for w in words:
            if w.upper() == w and w.isalpha():
                name.append(w)
            else:
                break
        nm = " ".join(name)
        out.append((vid, nm, rest[len(nm):].strip()))
    return out


VMAP_COLS = {"id": (0, 8), "classical": (8, 31), "ml": (31, 57),
             "amended": (57, None)}


def _vmap_lines():
    """[(line_no, line_text)] for the score rows, line numbers into the
    delivered document so a locator can be checked against it."""
    lines = _section("## 1B. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[1]
    doc = _lines()
    out, cursor = [], 0
    for line in block:
        if not line.strip() or line.lstrip().startswith("CLASSICAL"):
            continue
        vid = line.split()[0]
        if not (vid.startswith("V") and vid[1:].isdigit()):
            continue
        n = doc.index(line, cursor)
        cursor = n + 1
        out.append((n + 1, line))
    return out


def v_scores():
    """[(id, classical, ml, amendment)] from the second fence of 1B.

    Columns are fixed-width in the delivered text. The amendment column
    carries `-> X  A-nn` where an amendment applies and is empty
    otherwise; the order states that the AMENDED score is authoritative
    and the original is retained, so both come back.

    This is the RAW read. It carries no provenance and nothing scores off
    it -- see v_scores_sourced and amended_scores."""
    rows = []
    for _n, line in _vmap_lines():
        rows.append((line.split()[0],
                     line[8:31].strip(), line[31:57].strip(),
                     line[57:].strip()))
    return rows


def _sign(cell):
    """The leading +/- run of a score cell, or '' if the cell has none."""
    c = cell.strip()
    run = ""
    for ch in c:
        if ch in "+-":
            run += ch
        else:
            break
    return run


def _sign_span(cell):
    """(i, j) covering the leading +/- run WITHIN `cell`, or None.

    A span, not a value. `_sign` answers what the score is; this answers
    where it is, and the gate needs both."""
    i = 0
    while i < len(cell) and cell[i].isspace():
        i += 1
    j = i
    while j < len(cell) and cell[j] in "+-":
        j += 1
    return (i, j) if j > i else None


_AID = re.compile(r"A-\d+")


def _amend_parse(cell):
    """Spans into the amendment cell: (score_span, id_span, kind).

    Kinds: SCORE (a +/- run), SPLIT, ID_ONLY (an amendment that carries no
    score), EMPTY, UNPARSED. UNPARSED is kept apart from EMPTY because a
    cell holding text that is not an amendment is a different finding from
    a cell holding nothing -- and on this document one row has exactly
    that, its left neighbour spilling past the column boundary."""
    k = 0
    if cell.startswith("->"):
        k = 2
    while k < len(cell) and cell[k].isspace():
        k += 1
    rest = cell[k:]
    if not rest.strip():
        return None, None, "EMPTY"
    m = _AID.search(cell)
    id_span = (m.start(), m.end()) if m else None
    tok = rest.split()[0]
    ti = k + rest.find(tok)
    tj = ti + len(tok)
    if tok.startswith("A-"):
        return None, id_span, "ID_ONLY"
    if tok == "split":
        return (ti, tj), id_span, "SPLIT"
    if _sign(tok) == tok:
        return (ti, tj), id_span, "SCORE"
    return None, id_span, "UNPARSED"


def _upper(s):
    return s.strip().upper()


def amended_scores():
    """{id: {...}} with the order's rule applied: the amended score is
    authoritative, the original retained.

    Every score here is a Sourced -- value, literal source text, locator --
    and passes tools/sourced.gate before it is read. The defect this
    replaces built the amended score with `lstrip("-> ")`, which takes a
    CHARACTER SET and so stripped the value's own leading `--` along with
    the arrow, returning the UNAMENDED score on the map whose own rule is
    that the amended one is authoritative.

    Containment of the value in the cell would not have caught it: on V6
    the buggy value `-` does occur in `-> --   A-02`, through the hyphen
    of the arrow. What catches both rows is that the buggy path never
    LOCATED the value in the cell it names as its source, so it has no
    span to offer and the gate refuses. See tools/sourced.py.

    The document is a PARAMETER. WORK_ORDER_V3.md carries the same map in
    the same fixed-width columns under a different heading, and a second
    copy of this function is exactly the drift tools/check_gate_drift.py
    exists to catch (MF_019: five stale copies of one gate across three
    drops). entries_v3 supplies its own rows and its own order name; the
    cell parsers, the gate calls and the authoritative-score rule are
    this one object."""
    return amended_scores_from(ORDER_NAME, _vmap_lines())


def amended_scores_from(order_name, rows):
    """amended_scores over an arbitrary (order_name, [(line_no, line)])."""
    out = {}
    for n, line in rows:
        vid = line.split()[0]
        cls_i, cls_j = VMAP_COLS["classical"]
        ml_i, ml_j = VMAP_COLS["ml"]
        am_i, am_j = VMAP_COLS["amended"]
        cls_cell, ml_cell, am_cell = (line[cls_i:cls_j], line[ml_i:ml_j],
                                      line[am_i:])

        ml_loc = S.Locator(order_name, n, ml_i, ml_j, vid + " ml")
        am_loc = S.Locator(order_name, n, am_i, am_j, vid + " amendment")
        b_ok, b_cuts = ml_loc.boundary_clean(line)

        def _score(cell, loc, span, render=None):
            if span is None:
                return S.Unrated("no_provenance", where=loc.describe())
            return S.gate(S.slice_sourced(cell, span[0], span[1], loc,
                                          render=render))

        classical = _score(cls_cell,
                           S.Locator(order_name, n, cls_i, cls_j,
                                     vid + " classical"),
                           _sign_span(cls_cell))
        original = _score(ml_cell, ml_loc, _sign_span(ml_cell))

        sc_span, id_span, kind = _amend_parse(am_cell)
        if kind == "SCORE":
            amended = _score(am_cell, am_loc, sc_span)
        elif kind == "SPLIT":
            amended = _score(am_cell, am_loc, sc_span, render=_upper)
        else:
            # No amendment score in the cell, so the authoritative value is
            # the original -- and it keeps the original's own provenance
            # rather than being re-attributed to a cell it did not come
            # from. That re-attribution is the defect.
            amended = original
        aid = (S.gate(S.slice_sourced(am_cell, id_span[0], id_span[1],
                                      am_loc)) if id_span else None)

        refusal = S.gate_all(amended=amended, original=original)
        out[vid] = {
            "classical": S.value_of(classical),
            "original": S.value_of(original),
            "amended": S.value_of(amended),
            "amendment": S.value_of(aid, default=None) if aid else None,
            "note": am_cell.strip() or None,
            "amendment_kind": kind,
            "amended_span": (amended.span
                             if isinstance(amended, S.Sourced) else None),
            "amended_from": (amended.locator.describe()
                             if isinstance(amended, S.Sourced) else None),
            "unrated": refusal.reason if refusal is not None else None,
            "ml_cell_boundary": "CLEAN" if b_ok else "CUTS:" + ",".join(b_cuts),
            "line_no": n,
        }
    return out


def vmap_boundary_report():
    """Which score rows have a fixed-width column boundary that cuts a
    token in half. A locator is a CLAIM about where a cell ends; a
    boundary falling inside a token makes the claim false, truncating the
    cell to its left and prefixing the cell to its right with somebody
    else's text. Found by the gate, not by reading the table."""
    return vmap_boundary_report_from(ORDER_NAME, _vmap_lines())


def vmap_boundary_report_from(order_name, vmap_rows):
    """vmap_boundary_report over an arbitrary document's score rows."""
    rows = []
    for n, line in vmap_rows:
        vid = line.split()[0]
        for name, (i, j) in sorted(VMAP_COLS.items()):
            loc = S.Locator(order_name, n, i, j, vid + " " + name)
            ok, cuts = loc.boundary_clean(line)
            if not ok:
                rows.append({"id": vid, "line_no": n, "column": name,
                             "cuts": list(cuts),
                             "cell": loc.cell(line),
                             "spill": line[j:].strip() if j else ""})
    return {"n_rows": len(vmap_rows), "cut": rows, "n_cut": len(rows)}


ORIGINAL_MARKERS = ("ORIGINAL FORM of F3 listed ", "Original F3 listed ")


def f3_claim():
    """The wins and losses F3 names, read out of its own text."""
    return f3_claim_from(_section("### 1B-1", stop_prefix=("## ",)))


def f3_claim_from(lines):
    """f3_claim over an arbitrary section's lines. The two documents word
    the withdrawal differently -- v2 "ORIGINAL FORM of F3 listed", v3
    "Original F3 listed" -- so the marker is a tuple and a document
    matching neither returns an empty original_wins rather than silently
    reporting that nothing was withdrawn."""
    txt = " ".join(" ".join(lines).split())
    wins, losses, original = [], [], []
    i = txt.find("Wins after amendment are ")
    if i >= 0:
        seg = txt[i + len("Wins after amendment are "):].split(":")[0]
        wins = [w.strip() for w in seg.replace(" and ", ",").split(",")
                if w.strip().startswith("V")]
    j = txt.find("Losses are ")
    if j >= 0:
        seg = txt[j + len("Losses are "):].split(":")[0]
        losses = [w.strip() for w in seg.replace(" and ", ",").split(",")
                  if w.strip().startswith("V")]
    marker = None
    for cand in ORIGINAL_MARKERS:
        k = txt.find(cand)
        if k >= 0:
            marker = cand
            break
    if marker is not None:
        seg = txt[k + len(marker):].split(" among")[0]
        original = [w.strip() for w in seg.replace(" and ", ",").split(",")
                    if w.strip().startswith("V")]
    return {"wins": wins, "losses": losses, "original_wins": original,
            "original_marker": marker}


# -------------------------------------------------------- entries

def entries_v2():
    """Every ENTRY block in v2, using entries.py's own gutter parser."""
    out = []
    lines = _lines()
    for block in E._fenced_blocks(lines):
        if not block or not block[0].strip().startswith("ENTRY"):
            continue
        fields = E._parse_gutter(block[1:], 19)
        rec = {}
        order = []
        for name, value, n in fields:
            rec[name] = value
            order.append(name)
        out.append({"id": rec.get("id"), "fields": rec, "order": order,
                    "n_lines": len(block)})
    return out


def reconstruction_values(rec):
    """Which of the schema's three declared values a reconstruction cell
    states. A cell stating none of them, or more than one, is reported
    as such rather than coerced -- the order defines three."""
    cell = rec["fields"].get("reconstruction", "")
    found = [v for v in ("YES", "PARTIAL", "NO")
             if _word_in(cell, v)]
    return found


def _word_in(text, word):
    """Whole-word containment. 'NO' is inside 'NONE' and inside 'NOT', so
    a substring scan reports a reconstruction value on cells that state
    none -- the UNI_009 shape, avoided rather than found."""
    i = 0
    while True:
        i = text.find(word, i)
        if i < 0:
            return False
        before = text[i - 1] if i else " "
        after = text[i + len(word):i + len(word) + 1] or " "
        if not before.isalnum() and before != "_" \
                and not after.isalnum() and after != "_":
            return True
        i += len(word)


def evidence_values(rec):
    cell = rec["fields"].get("evidence_class", "")
    return [v for v in ("MEASURED", "TRANSPORTED", "PROJECTED")
            if _word_in(cell, v)]


# ----------------------------------------------------- ambient sets

def _indented_list(lines, min_indent):
    """Items of an indented free list: a new item starts a line at
    min_indent, continuations are indented further."""
    out = []
    for line in lines:
        if not line.strip():
            continue
        ind = len(line) - len(line.lstrip())
        if ind == min_indent:
            out.append(line.strip())
        elif ind > min_indent and out:
            out[-1] = out[-1] + " " + line.strip()
        else:
            if out:
                break
    return out


def artifact_side_ambient():
    """DUR-005's candidate set, from the AMBIENT ENUMERATION PROCEDURE."""
    lines = _section("### AMBIENT ENUMERATION PROCEDURE",
                     stop_prefix=("### ", "## "))
    start = None
    for i, line in enumerate(lines):
        if line.startswith("Candidate ambient set"):
            start = i
            break
    if start is None:
        raise ValueError("candidate ambient set not found")
    return _indented_list(lines[start:], 4)


def carrier_side_ambient():
    """DUR-005-B's candidate set."""
    lines = _section("### DUR-005-B", stop_prefix=("### ", "## "))
    start = None
    for i, line in enumerate(lines):
        if line.startswith("Candidate carrier-side set"):
            start = i
            break
    if start is None:
        raise ValueError("candidate carrier-side set not found")
    return _indented_list(lines[start:], 4)


def screen_rule():
    """DUR-005-C, the intrinsic-vs-produced screen, as delivered text."""
    return "\n".join(_section("### DUR-005-C", stop_prefix=("```", "## ")))


# ------------------------------------------------------- DUR-006

def transfer_modes():
    """[(mode, artifact, carriers, result)] from DUR-006-A's fence."""
    lines = _section("### DUR-006-A", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    rows, cur = [], None
    for line in block:
        if not line.strip():
            continue
        if line.startswith("MODE"):
            continue
        if line[0] != " ":
            if cur:
                rows.append(cur)
            cur = [line[0:20].strip(), line[20:42].strip(),
                   line[42:64].strip(), line[64:].strip()]
        elif cur:
            cur[1] = (cur[1] + " " + line[20:42].strip()).strip()
            cur[2] = (cur[2] + " " + line[42:64].strip()).strip()
            cur[3] = (cur[3] + " " + line[64:].strip()).strip()
    if cur:
        rows.append(cur)
    return [tuple(r) for r in rows]


def conjunction_terms():
    """[(term, what_would_have_to_be_ensured)] from DUR-006-B's fence."""
    lines = _section("### DUR-006-B", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    rows, cur = [], None
    for line in block:
        if not line.strip() or line.startswith("TERM"):
            continue
        if line[0] != " ":
            if cur:
                rows.append(cur)
            cur = [line[0:33].strip(), line[33:].strip()]
        elif cur:
            cur[1] = (cur[1] + " " + line[33:].strip()).strip()
    if cur:
        rows.append(cur)
    return [tuple(r) for r in rows]


# ---------------------------------------------------- falsifiers

def falsifiers_v2():
    """[(id, text)] in delivered order. entries.falsifiers() reads v1."""
    lines = _section("## 7. FALSIFIERS")
    out = []
    for line in lines:
        if line.startswith("F_") and "  " in line:
            fid = line.split()[0]
            out.append([fid, line[len(fid):].strip()])
        elif out and line.startswith("     "):
            out[-1][1] += " " + line.strip()
    return [(a, b) for a, b in out]


# ---------------------------------------------------- amendments

def amendments():
    """[{id, title, superseded, replacement, forcing_case, consequence}]
    from section 9's fences."""
    lines = _section("## 9. AMENDMENT RECORD", stop_prefix=("### ", "## "))
    out = []
    for block in E._fenced_blocks(lines):
        if not block or not block[0].strip().startswith("A-"):
            continue
        head = block[0].strip()
        aid = head.split()[0]
        title = head[len(aid):].strip()
        fields = E._parse_gutter(block[1:], 13)
        rec = {"id": aid, "title": title}
        for name, value, n in fields:
            rec[name.replace(" ", "_")] = value
        out.append(rec)
    return out


def still_open():
    """The 9-1 bullet list, one entry per bullet."""
    lines = _section("### 9-1", stop_prefix=("## ",))
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith("- "):
            out.append(s[2:])
        elif out and s:
            out[-1] += " " + s
    return out


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "entries_v2.py is a parser. The checks live in "
            "test_register_v2.py; run `python3 test_register_v2.py`.\n")
        return 2
    print("WORK_ORDER_V2.md")
    print("  V-map variables      %d" % len(v_definitions()))
    print("  V-map score rows     %d" % len(v_scores()))
    print("  ENTRY blocks         %s"
          % ", ".join(e["id"] for e in entries_v2()))
    print("  artifact-side ambient %d" % len(artifact_side_ambient()))
    print("  carrier-side ambient  %d" % len(carrier_side_ambient()))
    print("  transfer modes        %d" % len(transfer_modes()))
    print("  conjunction terms     %d" % len(conjunction_terms()))
    print("  falsifiers            %s"
          % ", ".join(f for f, _ in falsifiers_v2()))
    print("  amendments            %s"
          % ", ".join(a["id"] for a in amendments()))
    print("  still open            %d" % len(still_open()))
    b = vmap_boundary_report()
    print("  V-map column boundaries cutting a token: %d of %d rows"
          % (len(set(r["id"] for r in b["cut"])), b["n_rows"]))
    for r in b["cut"]:
        print("    %s line %d %-9s cuts %-6s cell=%r"
              % (r["id"], r["line_no"], r["column"],
                 ",".join(r["cuts"]), r["cell"]))
    if b["cut"]:
        print("    a locator is a claim about where a cell ends; a "
              "boundary inside a")
        print("    token makes the claim false. No score moves here -- "
              "what is false is")
        print("    the locator and not the value.")
    a = amended_scores()
    ungated = [v for v in a if a[v]["unrated"]]
    print("  V-map scores failing the value-and-source gate: %d"
          % len(ungated))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
