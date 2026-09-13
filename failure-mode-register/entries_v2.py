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
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entries as E                                       # noqa: E402

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


def v_scores():
    """[(id, classical, ml, amendment)] from the second fence of 1B.

    Columns are fixed-width in the delivered text. The amendment column
    carries `-> X  A-nn` where an amendment applies and is empty
    otherwise; the order states that the AMENDED score is authoritative
    and the original is retained, so both come back."""
    lines = _section("## 1B. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[1]
    rows = []
    for line in block:
        if not line.strip() or line.lstrip().startswith("CLASSICAL"):
            continue
        vid = line.split()[0]
        if not (vid.startswith("V") and vid[1:].isdigit()):
            continue
        classical = line[8:31].strip()
        ml = line[31:57].strip()
        amend = line[57:].strip()
        rows.append((vid, classical, ml, amend))
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


def amended_scores():
    """{id: {original, amended, amendment, note}} with the order's rule
    applied: the amended score is authoritative, the original retained."""
    out = {}
    for vid, classical, ml, amend in v_scores():
        orig = _sign(ml)
        amended, aid, note = orig, None, None
        if amend:
            # NOT lstrip("-> "). lstrip takes a CHARACTER SET, so on a
            # cell reading "-> --   A-01" it strips the value's own
            # leading "--" as well and the amended score comes back as
            # the unamended one -- on the map whose own rule is that the
            # amended score is authoritative. Found by printing the
            # table, not by reading the line.
            body = amend[2:].strip() if amend.startswith("->") \
                else amend.strip()
            parts = body.split()
            if parts and parts[0].startswith("A-"):
                aid = parts[0]
                note = body
            elif parts:
                cand = _sign(parts[0])
                if cand:
                    amended = cand
                for p in parts:
                    if p.startswith("A-"):
                        aid = p
                note = body
            if body.startswith("split"):
                amended = "SPLIT"
                note = body
        out[vid] = {"classical": _sign(classical), "original": orig,
                    "amended": amended, "amendment": aid, "note": note}
    return out


def f3_claim():
    """The wins and losses F3 names, read out of its own text."""
    lines = _section("### 1B-1", stop_prefix=("## ",))
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
    k = txt.find("ORIGINAL FORM of F3 listed ")
    if k >= 0:
        seg = txt[k + len("ORIGINAL FORM of F3 listed "):].split(" among")[0]
        original = [w.strip() for w in seg.replace(" and ", ",").split(",")
                    if w.strip().startswith("V")]
    return {"wins": wins, "losses": losses, "original_wins": original}


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
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
