#!/usr/bin/env python3
"""
Parser for WORK_ORDER_V3.md -- the third order, landed verbatim beside
WORK_ORDER.md and WORK_ORDER_V2.md so all three stay inspectable (the
supersession convention this repository already uses: observer-exclusion
SPEC_V2, design-basis SOURCE_DROP_V2, mining-increment SOURCE_DROP_V2/V3).

Nothing here is retyped from the order. The gutter parser, the fence
walker and the field-line test are IMPORTED from entries.py; the
fixed-width cell parsers, the amendment reader, the gated score map, the
column-boundary report and the F3 reader are IMPORTED from entries_v2.py,
which was generalised to take a document rather than copied. One parser,
three documents -- so an edit to any of them that the parser cannot
follow turns the suite red rather than passing against a stale copy.

v3 is NOT a purely additive revision of v2, unlike v2 against v1. It is a
rewrite: measured with difflib in test_register_v3.py rather than
asserted here. Only the section walk and the blocks v3 shapes differently
are new.

CC0. Stdlib only. Parses under 3.9. ASCII only.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entries as E                                       # noqa: E402
import entries_v2 as E2                                   # noqa: E402
sys.path.insert(0, os.path.join(HERE, os.pardir, "tools"))
import sourced as S                                       # noqa: E402

ORDER_NAME = "WORK_ORDER_V3.md"
ORDER_PATH_V3 = os.path.join(HERE, ORDER_NAME)

SCHEMA_COL = 19          # entry and schema fences use v1's gutter
AMEND_COL = 13           # section 10 amendment blocks
STEP_COL = 8             # section 7 procedure steps
OPEN_COL = 33            # section 11 still-open blocks

# Every open choice this parser makes, printed by --choices and cited at
# the site where it takes effect.
CHOICES = {
    1: "entry blocks are located by their `### DUR-00n` heading, because "
       "v3 moved the id out of the fence; v2 located them by an `ENTRY` "
       "first line.",
    2: "the candidate ambient sets are read as fenced lists in v3 (v2 "
       "carried them as indented free lists, which is why entries_v2."
       "_indented_list is not used here).",
}

# The duration rule F_K needs and the rate rule F_M needs are NOT choices
# of this parser: they are register_v2's [CHOICE 11] and [CHOICE 10],
# imported with the functions that take them.


def order_text():
    with open(ORDER_PATH_V3) as fh:
        return fh.read()


def _lines():
    return order_text().split("\n")


def _section(heading_prefix, stop_prefix=("## ",)):
    """Same walk as entries._section and entries_v2._section, over v3's
    lines. Each binds its own document's text; everything below the walk
    is imported."""
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


# ------------------------------------------------------------- header

def header_status():
    """The status line, and what it states. F_D requires the PROJECTED
    fraction in the header; whether it is there is a property of this
    string."""
    for line in _lines()[:10]:
        if line.startswith("Status:"):
            body = line[len("Status:"):].strip()
            return {"line": line, "body": body,
                    "claims": [c.strip() for c in body.split(",")]}
    raise ValueError("status line not found")


# ------------------------------------------------------ 0-1 PRIOR ART

PRIOR_ART_COLS = {"artifact": (0, 37), "scope": (37, 66), "misses": (66, None)}


def prior_art_rows():
    """[(artifact, scope, misses)] from 0-1's fence. Rows are separated by
    a blank line and the artifact column continues onto further lines, so
    the split is on blank lines and not on indentation -- one of the four
    rows carries its arXiv id on a second unindented line."""
    lines = _section("### 0-1", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    groups, cur = [], []
    for line in block:
        if line.startswith("ARTIFACT"):
            continue
        if not line.strip():
            if cur:
                groups.append(cur)
                cur = []
            continue
        cur.append(line)
    if cur:
        groups.append(cur)
    i, j = PRIOR_ART_COLS["artifact"]
    k, m = PRIOR_ART_COLS["scope"]
    n = PRIOR_ART_COLS["misses"][0]
    rows = []
    for g in groups:
        a = " ".join(x[i:j].strip() for x in g if x[i:j].strip())
        b = " ".join(x[k:m].strip() for x in g if x[k:m].strip())
        c = " ".join(x[n:].strip() for x in g if x[n:].strip())
        rows.append((a, b, c))
    return rows


def prior_art_boundary_report():
    """Prior-art rows whose fixed-width column boundary cuts a token in
    half -- the same check the V-map carries, on the section v3 adds.
    A locator is a claim about where a cell ends; a boundary inside a
    token makes the claim false, and the joined cell then reads as text
    nobody wrote."""
    lines = _section("### 0-1", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    doc = _lines()
    out, cursor, n_rows = [], 0, 0
    for line in block:
        if not line.strip() or line.startswith("ARTIFACT"):
            continue
        n_rows += 1
        n = doc.index(line, cursor)
        cursor = n + 1
        for name, (i, j) in sorted(PRIOR_ART_COLS.items()):
            loc = S.Locator(ORDER_NAME, n + 1, i, j, name)
            ok, cuts = loc.boundary_clean(line)
            if not ok:
                out.append({"line_no": n + 1, "column": name,
                            "cuts": list(cuts), "cell": loc.cell(line),
                            "spill": line[j:].strip() if j else ""})
    return {"n_rows": n_rows, "cut": out, "n_cut": len(out)}


def prior_art_result():
    """The GATE RESULT sentence and whether it declares the gate run."""
    lines = _section("### 0-1", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("GATE RESULT:")
    return txt[i:] if i >= 0 else None


def entry_zero():
    """0-2, the detection-gap section, as delivered text."""
    return "\n".join(_section("### 0-2", stop_prefix=("---", "## ")))


# --------------------------------------------------------- 1  V-MAP

def v_definitions():
    """[(id, name, gloss)] from the first fence of section 1."""
    lines = _section("## 1. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    out = []
    for line in block:
        if not line.strip():
            continue
        vid = line.split()[0]
        if not (vid.startswith("V") and vid[1:].isdigit()):
            continue
        out.append((vid, line[5:28].strip(), line[28:].strip()))
    return out


def _vmap_lines():
    """[(line_no, line_text)] for the score rows, line numbers into the
    delivered document so a locator can be checked against it."""
    lines = _section("## 1. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
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
    """[(id, classical, ml, amendment)] -- the RAW read, no provenance,
    nothing scores off it. See amended_scores."""
    rows = []
    for _n, line in _vmap_lines():
        rows.append((line.split()[0],
                     line[8:31].strip(), line[31:57].strip(),
                     line[57:].strip()))
    return rows


def amended_scores():
    """The order's rule applied -- amended authoritative, original
    retained -- through the gated reader in entries_v2."""
    return E2.amended_scores_from(ORDER_NAME, _vmap_lines())


def vmap_boundary_report():
    """Column boundaries that cut a token in half, through the same
    reader."""
    return E2.vmap_boundary_report_from(ORDER_NAME, _vmap_lines())


def f3_claim():
    """The wins, losses and withdrawn wins F3 names, read out of its own
    text through the shared reader."""
    return E2.f3_claim_from(_section("### 1-1", stop_prefix=("## ",)))


def protective_after_amendment():
    """Variables whose AUTHORITATIVE score protects. Computed from the
    map, not read from F3, so the two can disagree."""
    out = []
    for vid, rec in amended_scores().items():
        val = rec["amended"]
        if isinstance(val, str) and val.startswith("+"):
            out.append(vid)
    return sorted(out, key=lambda v: int(v[1:]))


# ---------------------------------------------------------- 2  SCHEMA

def schema_fields():
    """[(name, definition)] from section 2's fence."""
    lines = _section("## 2. ENTRY SCHEMA", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    return [(n, v) for n, v, _k in E._parse_gutter(block, SCHEMA_COL)]


def schema_field_names():
    return [n for n, _v in schema_fields()]


def projection_rule():
    """The RULE sentence under the schema."""
    lines = _section("## 2. ENTRY SCHEMA", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("RULE:")
    return txt[i:] if i >= 0 else None


def measured_seeds():
    """2-A's bullet list, one entry per bullet."""
    lines = _section("### 2-A", stop_prefix=("### ", "## "))
    out = []
    for line in lines:
        s = line.strip()
        if s.startswith("- "):
            out.append(s[2:])
        elif out and s:
            out[-1] += " " + s
    return out


def transport_rule():
    return "\n".join(_section("### 2-B", stop_prefix=("---", "## ")))


# --------------------------------------------------------- 3  ENTRIES

def entry_ids():
    """[(id, title, line_no)] from the `### DUR-00n` headings.

    [CHOICE 1] v3 moved the id out of the fence and into the heading, so
    the blocks are located by heading. v2 located them by an `ENTRY`
    first line, which v3 does not have."""
    out = []
    for i, line in enumerate(_lines()):
        if not line.startswith("### DUR-00"):
            continue
        rest = line[4:].strip()
        head = rest.split()[0]
        if "-" in head[4:]:                     # DUR-005-B and friends
            continue
        title = rest[len(head):].strip(" -").strip()
        out.append((head, title, i + 1))
    return out


def entries_v3():
    """Every entry block, using entries.py's own gutter parser."""
    out = []
    for eid, title, n in entry_ids():
        lines = _section("### %s " % eid, stop_prefix=("### ", "## "))
        block = E._fenced_blocks(lines)[0]
        fields = E._parse_gutter(block, SCHEMA_COL)
        rec, order = {}, []
        for name, value, _k in fields:
            rec[name] = value
            order.append(name)
        out.append({"id": eid, "title": title, "line_no": n,
                    "fields": rec, "order": order, "n_lines": len(block)})
    return out


def field_coverage():
    """Which schema fields each entry block carries, and which it does
    not. The order's own rule: an entry missing any field is an UNRATED
    PART, filed as such."""
    names = schema_field_names()
    rows = []
    for rec in entries_v3():
        missing = [f for f in names if f not in rec["fields"]]
        extra = [f for f in rec["order"] if f not in names]
        rows.append({"id": rec["id"], "missing": missing, "extra": extra,
                     "n_fields": len(rec["order"]),
                     "unrated_part": bool(missing)})
    return {"schema_n": len(names), "rows": rows,
            "unrated_parts": [r["id"] for r in rows if r["unrated_part"]]}


def reconstruction_values(rec):
    """Which of the schema's three declared values a reconstruction cell
    states. Imported word test -- 'NO' sits inside 'NONE' and 'NOT'."""
    return E2.reconstruction_values(rec)


def evidence_values(rec):
    return E2.evidence_values(rec)


# ----------------------------------------------------- ambient sets

def _fence_items(section_heading, index):
    """[CHOICE 2] v3 carries the candidate sets as fenced lists."""
    lines = _section(section_heading, stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[index]
    return [ln.rstrip() for ln in block if ln.strip()]


def artifact_side_ambient():
    """DUR-005's candidate artifact-side set."""
    return _fence_items("### DUR-005 ", 1)


def carrier_side_ambient():
    """DUR-005-B's candidate carrier-side set."""
    return _fence_items("### DUR-005 ", 3)


def ambient_classes():
    """DUR-005-B's two-class fence, as delivered text."""
    return "\n".join(_fence_items("### DUR-005 ", 2))


def screen_rule():
    """DUR-005-C, the intrinsic-vs-produced screen, as delivered text --
    the whole sub-block, fence AND the prose after it, because the
    property the screen states about itself (no null result) is in the
    prose and not in the pseudocode."""
    lines = _section("### DUR-005 ", stop_prefix=("### ", "## "))
    out, inside = [], False
    for line in lines:
        if line.startswith("**DUR-005-C"):
            inside = True
        if inside:
            out.append(line)
    if not out:
        raise ValueError("DUR-005-C not found")
    return "\n".join(out)


# ------------------------------------------------------- DUR-006

def transfer_modes():
    """[(mode, artifact, carriers, result)] from DUR-006-A's fence."""
    lines = _section("### DUR-006 ", stop_prefix=("### ", "## "))
    block = None
    for b in E._fenced_blocks(lines):
        if b and b[0].startswith("MODE"):
            block = b
            break
    if block is None:
        raise ValueError("transfer-mode fence not found")
    rows = []
    for line in block:
        if not line.strip() or line.startswith("MODE"):
            continue
        rows.append((line[0:20].strip(), line[20:42].strip(),
                     line[42:65].strip(), line[65:].strip()))
    return rows


def conjunction_terms():
    """[(term, what_would_have_to_be_ensured)] from DUR-006-B's fence."""
    lines = _section("### DUR-006 ", stop_prefix=("### ", "## "))
    block = None
    for b in E._fenced_blocks(lines):
        if b and b[0].startswith("TERM"):
            block = b
            break
    if block is None:
        raise ValueError("conjunction fence not found")
    rows, cur = [], None
    for line in block:
        if not line.strip() or line.startswith("TERM"):
            continue
        if line[0] != " ":
            if cur:
                rows.append(cur)
            cur = [line[0:24].strip(), line[24:].strip()]
        elif cur:
            cur[1] = (cur[1] + " " + line[24:].strip()).strip()
    if cur:
        rows.append(cur)
    return [tuple(r) for r in rows]


# ------------------------------------------------- 4  HOPS AND VOLUME

def hop_budget():
    """The hop-budget fence, as delivered lines."""
    lines = _section("## 4. TIMEFRAME", stop_prefix=("### ", "## "))
    return E._fenced_blocks(lines)[0]


def stated_compression():
    """The compression factor the hop budget states, if it states one."""
    for line in hop_budget():
        if "Compressed by" in line:
            return line.strip()
    return None


def shock_classes():
    """[(id, name, gloss)] from 4-3's re-cut fence."""
    lines = _section("### 4-3", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    out, cur = [], None
    for line in block:
        if not line.strip():
            continue
        tok = line.split()[0]
        if tok.startswith("V14"):
            if cur:
                out.append(cur)
            cur = [tok, line[6:23].strip(), line[23:].strip()]
        elif cur:
            cur[2] = (cur[2] + " " + line.strip()).strip()
    if cur:
        out.append(cur)
    return [tuple(r) for r in out]


def register_rule_redundancy():
    """4-2's REGISTER RULE sentence."""
    lines = _section("### 4-2", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("REGISTER RULE:")
    return txt[i:] if i >= 0 else None


# ------------------------------------------------------ 5  COMPOUNDING

def compounding_subsections():
    """[(heading, text)] for every 5-n subsection."""
    out = []
    lines = _lines()
    for i, line in enumerate(lines):
        if line.startswith("### 5-"):
            out.append((line[4:].strip(), i + 1))
    return out


def compounding_projection_rule():
    """The sentence in section 5 that applies F_J."""
    lines = _section("## 5. COMPOUNDING", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("Mark all of Section 5")
    return txt[i:] if i >= 0 else None


# ----------------------------------------------------- 6  PARSER GATE

def parser_gate():
    """Section 6's fence, as delivered lines."""
    lines = _section("## 6. THE PARSER GATE", stop_prefix=("---", "## "))
    return E._fenced_blocks(lines)[0]


def parser_gate_fields():
    """The items under THREE FIELDS."""
    out, inside = [], False
    for line in parser_gate():
        if line.startswith("THREE FIELDS"):
            inside = True
            continue
        if inside:
            if not line.startswith("    "):
                break
            out.append(line.strip())
    return out


# -------------------------------------------------------- 7  PROCEDURE

def steps():
    """[(id, text)] from section 7's fence."""
    lines = _section("## 7. PROCEDURE", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    out = []
    for line in block:
        if line.startswith("Step "):
            sid = " ".join(line.split()[:2])
            out.append([sid, line[STEP_COL:].strip()])
        elif out and line.startswith(" " * STEP_COL):
            out[-1][1] += " " + line.strip()
    return [(a, b) for a, b in out]


def load_rating_terms():
    """[(term, definition)] from 7-1's fence."""
    lines = _section("### 7-1", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    return [(n, v) for n, v, _k in E._parse_gutter(block, 20)]


def custody_axis():
    return "\n".join(_section("### 7-2", stop_prefix=("---", "## ")))


# ---------------------------------------------------- 8  FALSIFIERS

def falsifiers_v3():
    """[(id, text)] in delivered order."""
    lines = _section("## 8. FALSIFIERS")
    block = E._fenced_blocks(lines)[0]
    out = []
    for line in block:
        if line.startswith("F_"):
            fid = line.split()[0]
            out.append([fid, line[len(fid):].strip()])
        elif out and line.startswith("     "):
            out[-1][1] += " " + line.strip()
    return [(a, b) for a, b in out]


# ---------------------------------------------------- 10 AMENDMENTS

def amendments():
    """[{id, title, superseded, replacement, forcing_case, consequence}]
    from section 10's fence."""
    lines = _section("## 10. AMENDMENT RECORD", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    out, cur, buf = [], None, []
    for line in block:
        if line.startswith("A-"):
            if cur:
                out.append((cur, buf))
            head = line.strip()
            cur = (head.split()[0], head[len(head.split()[0]):].strip())
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur:
        out.append((cur, buf))
    recs = []
    for (aid, title), body in out:
        rec = {"id": aid, "title": title}
        for name, value, _k in E._parse_gutter(body, AMEND_COL):
            rec[name.replace(" ", "_")] = value
        recs.append(rec)
    return recs


# --------------------------------------------------- 11 STILL OPEN

def still_open():
    """[(topic, text)] from section 11's fence."""
    lines = _section("## 11. STILL OPEN", stop_prefix=("## ",))
    block = E._fenced_blocks(lines)[0]
    out = []
    for line in block:
        if not line.strip():
            continue
        if line[0] != " ":
            out.append([line[0:OPEN_COL].strip(), line[OPEN_COL:].strip()])
        elif out:
            out[-1][1] = (out[-1][1] + " " + line.strip()).strip()
    return [(a, b) for a, b in out]


def render_choices():
    return [(n, CHOICES[n]) for n in sorted(CHOICES)]


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "entries_v3.py is a parser. The checks live in "
            "test_register_v3.py; run `python3 test_register_v3.py`.\n")
        return 2
    if "--choices" in argv:
        for n, text in render_choices():
            print("[CHOICE %d] %s" % (n, text))
        return 0
    print(ORDER_NAME)
    print("  status               %s" % header_status()["body"])
    print("  prior-art rows       %d" % len(prior_art_rows()))
    print("  V-map variables      %d" % len(v_definitions()))
    print("  V-map score rows     %d" % len(v_scores()))
    print("  schema fields        %d" % len(schema_fields()))
    print("  ENTRY blocks         %s"
          % ", ".join(e["id"] for e in entries_v3()))
    print("  artifact-side ambient %d" % len(artifact_side_ambient()))
    print("  carrier-side ambient  %d" % len(carrier_side_ambient()))
    print("  transfer modes        %d" % len(transfer_modes()))
    print("  conjunction terms     %d" % len(conjunction_terms()))
    print("  shock classes         %s"
          % ", ".join(s[0] for s in shock_classes()))
    print("  steps                 %d" % len(steps()))
    print("  falsifiers            %s"
          % ", ".join(f for f, _ in falsifiers_v3()))
    print("  amendments            %s"
          % ", ".join(a["id"] for a in amendments()))
    print("  still open            %d" % len(still_open()))
    b = vmap_boundary_report()
    print("  V-map column boundaries cutting a token: %d of %d rows"
          % (len(set(r["id"] for r in b["cut"])), b["n_rows"]))
    p = prior_art_boundary_report()
    print("  prior-art column boundaries cutting a token: %d of %d lines"
          % (p["n_cut"], p["n_rows"]))
    for r in p["cut"]:
        print("    line %d %-9s cuts %-6s cell=%r spill=%r"
              % (r["line_no"], r["column"], ",".join(r["cuts"]),
                 r["cell"], r["spill"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
