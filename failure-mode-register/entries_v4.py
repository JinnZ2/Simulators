#!/usr/bin/env python3
"""
Parser for WORK_ORDER_V4.md -- the fourth order, landed verbatim beside
WORK_ORDER.md, WORK_ORDER_V2.md and WORK_ORDER_V3.md so all four stay
inspectable (the supersession convention this repository already uses:
observer-exclusion SPEC_V2, design-basis SOURCE_DROP_V2, mining-increment
SOURCE_DROP_V2/V3).

Nothing here is retyped from the order, and nothing here is a fourth copy
of a parser. The gutter parser and the fence walker come from entries.py;
the boundary reader comes from entries_v2.py, generalised to take a
COLUMN LAYOUT rather than copied, because v4 rewrote the V-map into five
columns with word score tokens. One parser, four documents -- so an edit
to any of them that the parser cannot follow turns the suite red rather
than passing against a stale copy. MF_019 records what the alternative
costs: five stale copies of one gate across three drops.

v4 is a REWRITE of v3, not an insertion: measured with difflib in
test_register_v4.py rather than asserted here.

Two v4 format changes drive most of what is new below.

  A-12  the id is back INSIDE the field block. v3 moved it into the
        markdown heading and every entry became an UNRATED PART by the
        register's own rule, against a change that altered no content.
        F_N was added so a reformat is checked against the rating vector.
  A-13  score tokens are WORDS. v2 and v3 wrote amendments into the score
        column as an arrow plus a score, and a column cut landed on the
        arrow's hyphen and returned it as a V6 score. The amendment now
        has its own column, so entries_v2's sign parsers do not apply and
        the v4 score reader slices instead.

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

ORDER_NAME = "WORK_ORDER_V4.md"
ORDER_PATH_V4 = os.path.join(HERE, ORDER_NAME)

SCHEMA_COL = 19          # entry and schema fences use v1's gutter
PRIOR_ART_COL = 11       # 0-1's one-block-per-artifact fences (A-13/D-06)
AMEND_COL = 13           # section 10 amendment blocks
OPEN_COL = 6             # section 11 open-defect blocks

# The five-column V-map v4 rewrote section 1 into. Derived from the
# header row rather than asserted -- see vmap_columns() -- and stated
# here only as the fallback a reader can check the derivation against.
VMAP_COLS_V4 = {"id": (0, 5), "name": (5, 27), "classical": (27, 38),
                "ml_orig": (38, 47), "ml_amended": (47, 59),
                "amendment": (59, None)}

SCORE_TOKENS = ("PROT", "LOSS", "LOSS2")   # section 1's declared legend

# A-13's format rule, as the set of glyphs it names. A score or status
# cell carrying one of these is what a column cut can turn into a score.
FORBIDDEN_IN_SCORE_CELL = ("-", ">", "<", "|", "+", "*", "=")

CHOICES = {
    1: "entry blocks are located by their `### DUR-00n` heading and the "
       "id is then read from the FIELD BLOCK, which is where A-12 puts "
       "it; the heading is treated as presentation, as the order says.",
    2: "the V-map column layout is DERIVED from the header row rather "
       "than hard-coded, because A-13 changed the layout and a hard-coded "
       "one would have followed the old document silently.",
    3: "the candidate ambient sets are read as fixed-width tables in v4 "
       "(v2 carried them as indented free lists, v3 as fenced lists), and "
       "a candidate whose name wraps onto a continuation line is joined "
       "to the row above it rather than dropped.",
    4: "D-06 asks for a mechanical check rather than a rule in the text, "
       "so format_rule_scan walks EVERY fixed-width table in the whole "
       "document, not the V-map alone -- the recurrence D-06 records was "
       "in a table the V-map check did not look at.",
    5: "a fixed-width table is recognised at THREE or more columns. A "
       "two-column fixed-width block is the same shape as a gutter "
       "block, and both 0-1's STATUS block and DUR-006-B's TERM table "
       "are gutter blocks; the cost is that a genuine two-column table "
       "would not be scanned.",
    6: "a cell is a SCORE OR STATUS cell for A-13's glyph rule when its "
       "column label is not one of the free-text labels named in "
       "FREE_TEXT_COLUMNS -- a declared list, because whether a column "
       "holds a score is a reading of the header and not a lexical "
       "property of the cells under it.",
}

# Column labels whose cells are prose by construction, so A-13's glyph
# rule does not apply to them. [CHOICE 6]. Declared rather than derived:
# a word list deciding which columns hold scores would be T1-1 one level
# up, so the list is short, stated, and checkable against the headers.
FREE_TEXT_COLUMNS = ("CANDIDATE", "TERM", "MODE", "VAR", "NAME",
                     "AMENDMENT", "WHAT WOULD HAVE TO BE ENSURED",
                     "SHARED EXTERNAL REFERENT", "ARTIFACT", "CARRIERS",
                     "RESULT")


def order_text():
    with open(ORDER_PATH_V4) as fh:
        return fh.read()


def _lines():
    return order_text().split("\n")


def _section(heading_prefix, stop_prefix=("## ",)):
    """Same walk as entries._section, entries_v2._section and
    entries_v3._section, over v4's lines. Each binds its own document's
    text; everything below the walk is imported."""
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

def header_block():
    """v4 replaced v3's `Status:` line with a fenced block carrying the
    two things F_D and A-16 require in the header. Read as a gutter block
    rather than as a sentence."""
    block = E._fenced_blocks(_lines()[:20])[0]
    rows = E._parse_gutter(block, 21)
    return {"raw": block,
            "fields": dict((n, v) for n, v, _k in rows),
            "order": [n for n, _v, _k in rows]}


def version_line():
    for line in _lines()[:10]:
        if line.startswith("Version:"):
            return line
    raise ValueError("version line not found")


# ------------------------------------------------------ 0-1 PRIOR ART

def prior_art_status():
    """0-1's first fence: the gate's own status block."""
    lines = _section("### 0-1", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    rows = E._parse_gutter(block, 17)
    return dict((n, v) for n, v, _k in rows)


def prior_art_rows():
    """One fenced block per artifact -- the D-06 repair. v3 carried these
    as a fixed-width table and the column boundary cut a cross-reference
    in half; v4 rewrote them as gutter blocks, which have no column
    boundary to cut."""
    lines = _section("### 0-1", stop_prefix=("### ", "## "))
    out = []
    for block in E._fenced_blocks(lines)[1:]:
        rows = E._parse_gutter(block, PRIOR_ART_COL)
        rec = dict((n, v) for n, v, _k in rows)
        if "ARTIFACT" in rec:
            rec["_order"] = [n for n, _v, _k in rows]
            out.append(rec)
    return out


def prior_art_result():
    """The GATE RESULT sentence, verbatim."""
    lines = _section("### 0-1", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("GATE RESULT")
    return txt[i:] if i >= 0 else None


def entry_zero():
    return "\n".join(_section("### 0-2", stop_prefix=("---", "## ")))


# ------------------------------------------------------ 1  V-MAP

def _vmap_block():
    lines = _section("## 1. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
    blocks = E._fenced_blocks(lines)
    return blocks[0], blocks[1]      # legend, score table


def score_legend():
    """The three declared score tokens, read out of section 1's first
    fence rather than taken from SCORE_TOKENS."""
    legend, _ = _vmap_block()
    out = []
    for line in legend:
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            out.append((parts[0], parts[1].strip()))
    return out


def vmap_columns():
    """[CHOICE 2] Column starts derived from the header row. A-13 moved
    the amendment into its own column; a hard-coded layout would have
    followed v3's table into v4 without saying so."""
    _legend, table = _vmap_block()
    header = None
    for line in table:
        if line.startswith("VAR"):
            header = line
            break
    if header is None:
        raise ValueError("V-map header row not found")
    labels = ("VAR", "NAME", "CLASSICAL", "ML ORIG", "ML AMENDED",
              "AMENDMENT")
    keys = ("id", "name", "classical", "ml_orig", "ml_amended", "amendment")
    starts = []
    for lab in labels:
        k = header.find(lab)
        if k < 0:
            raise ValueError("V-map column not found: %r" % lab)
        starts.append(k)
    cols = {}
    for i, key in enumerate(keys):
        j = starts[i + 1] if i + 1 < len(starts) else None
        cols[key] = (starts[i], j)
    return cols, header


def _vmap_lines():
    """[(line_no, line_text)] for the score rows, line numbers into the
    delivered document so a locator can be checked against it."""
    _legend, table = _vmap_block()
    doc = _lines()
    out, cursor = [], 0
    for line in table:
        if not line.strip() or line.startswith("VAR"):
            continue
        vid = line.split()[0]
        if not (vid.startswith("V") and vid[1:].isdigit()):
            continue
        n = doc.index(line, cursor)
        cursor = n + 1
        out.append((n + 1, line))
    return out


def v_definitions():
    """[(id, name)] from the score table's own NAME column -- v4 carries
    the glosses as a prose paragraph under the table, not as a column."""
    cols, _hdr = vmap_columns()
    i, j = cols["name"]
    out = []
    for _n, line in _vmap_lines():
        out.append((line.split()[0], line[i:j].strip()))
    return out


def v_gloss():
    """The definitions paragraph under the table, verbatim and unsplit.
    v4 states them as running prose; splitting them on `V<n> ` would be a
    reader's guess about sentence boundaries, not a parse."""
    lines = _section("## 1. LOSS-VARIABLE MAP", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("Definitions:")
    return txt[i:] if i >= 0 else None


def v_scores():
    """[(id, classical, ml_orig, ml_amended, amendment)] -- the RAW read,
    no provenance, nothing scores off it. See amended_scores."""
    cols, _hdr = vmap_columns()
    rows = []
    for _n, line in _vmap_lines():
        cells = []
        for key in ("classical", "ml_orig", "ml_amended", "amendment"):
            i, j = cols[key]
            cells.append(line[i:j].strip() if j else line[i:].strip())
        rows.append(tuple([line.split()[0]] + cells))
    return rows


def amended_scores():
    """The authoritative score per variable, with provenance.

    v4's own format is why this is not entries_v2.amended_scores_from:
    there the amended score had to be PARSED OUT of an arrow expression
    sharing a cell with the original, and the sign parsers exist for
    that. A-13 gave the amended score its own column, so the value is a
    SLICE, and slice_sourced emits the span the extraction read from --
    which is section 6-2's fourth requirement satisfied by construction
    rather than by a later search."""
    cols, _hdr = vmap_columns()
    out = {}
    for n, line in _vmap_lines():
        vid = line.split()[0]
        rec = {"line_no": n}
        for key in ("classical", "ml_orig", "ml_amended"):
            i, j = cols[key]
            cell = line[i:j] if j else line[i:]
            loc = S.Locator(ORDER_NAME, n, i, j, "%s %s" % (vid, key))
            body = cell.strip()
            if not body:
                rec[key] = S.UNRATED
                rec[key + "_span"] = None
                continue
            k = cell.index(body)
            sc = S.gate(S.slice_sourced(cell, k, k + len(body), loc))
            rec[key] = S.value_of(sc)
            rec[key + "_span"] = (sc.span if isinstance(sc, S.Sourced)
                                  else None)
            ok, cuts = loc.boundary_clean(line)
            rec[key + "_boundary"] = "CLEAN" if ok else "CUTS:" + ",".join(cuts)
        i, j = cols["amendment"]
        rec["amendment"] = (line[i:j] if j else line[i:]).strip()
        rec["amended"] = rec["ml_amended"]
        rec["original"] = rec["ml_orig"]
        rec["declared_token"] = rec["ml_amended"] in SCORE_TOKENS
        out[vid] = rec
    return out


def vmap_boundary_report():
    """Column boundaries that cut a token in half, through entries_v2's
    reader with v4's derived layout handed to it."""
    cols, _hdr = vmap_columns()
    return E2.vmap_boundary_report_from(ORDER_NAME, _vmap_lines(), cols)


def undeclared_score_tokens():
    """Score cells whose token is not one of the three the legend
    declares. V14's ML AMENDED reads SPLIT."""
    declared = set(t for t, _g in score_legend())
    rows = []
    for vid, rec in amended_scores().items():
        for key in ("classical", "ml_orig", "ml_amended"):
            val = rec.get(key)
            if val and val != S.UNRATED and val not in declared:
                rows.append({"id": vid, "column": key, "token": val,
                             "line_no": rec["line_no"]})
    return {"declared": sorted(declared), "rows": rows, "n": len(rows)}


def protective_after_amendment():
    """Variables whose AUTHORITATIVE score protects. Computed from the
    map, not read from F3, so the two can disagree -- which is exactly
    what A-14 records happening."""
    out = []
    for vid, rec in amended_scores().items():
        if rec["amended"] == "PROT":
            out.append(vid)
    return sorted(out, key=lambda v: int(v[1:]))


def f3_claim():
    """F3's own restated arithmetic block, read out of 1-1 rather than
    counted from the table, so the two readings stay separable."""
    lines = _section("### 1-1", stop_prefix=("## ",))
    block = E._fenced_blocks(lines)[0]
    rows = E._parse_gutter(block, 23)
    rec = dict((n, v) for n, v, _k in rows)
    return {"raw": block, "fields": rec,
            "order": [n for n, _v, _k in rows]}


def findings_1_1():
    """[(label, text)] for F1, F2, F3."""
    lines = _section("### 1-1", stop_prefix=("## ",))
    out, cur = [], None
    for line in lines:
        if line.startswith("**F") and "--" not in line[:4]:
            label = line[2:].split(" ")[0].strip("*")
            cur = [label, line]
            out.append(cur)
        elif cur is not None:
            cur[1] += "\n" + line
    return [(a, b) for a, b in out]


# ---------------------------------------------------------- 2  SCHEMA

def schema_fields():
    """[(name, definition)] from section 2's fence."""
    lines = _section("## 2. ENTRY SCHEMA", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    return [(n, v) for n, v, _k in E._parse_gutter(block, SCHEMA_COL)]


def schema_field_names():
    return [n for n, _v in schema_fields()]


def declared_optional_fields():
    """A-15's repair: `note` is a DECLARED OPTIONAL field, present or
    absent without firing the UNRATED PART rule. Read out of the
    paragraph that declares it rather than assumed."""
    lines = _section("## 2. ENTRY SCHEMA", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("DECLARED OPTIONAL FIELD")
    if i < 0:
        return []
    tail = txt[i:]
    out = []
    for tok in tail.split("`"):
        if tok and tok.replace("_", "").isalnum() and tok.islower():
            out.append(tok)
    return sorted(set(out))


def projection_rule():
    lines = _section("## 2. ENTRY SCHEMA", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("RULE:")
    j = txt.find("FORMAT RULE:")
    return txt[i:j].strip() if i >= 0 and j > i else (txt[i:] if i >= 0
                                                     else None)


def format_rule():
    """The FORMAT RULE paragraph -- A-12's repair, stated in section 2."""
    lines = _section("## 2. ENTRY SCHEMA", stop_prefix=("### ", "## "))
    txt = " ".join(" ".join(lines).split())
    i = txt.find("FORMAT RULE:")
    return txt[i:] if i >= 0 else None


def measured_seeds():
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
    """[(id_from_heading, line_no)] -- the headings only. The
    AUTHORITATIVE id is the one in the field block; see entries_v4().
    [CHOICE 1]"""
    out = []
    for i, line in enumerate(_lines()):
        if not line.startswith("### DUR-00"):
            continue
        head = line[4:].strip().split()[0]
        if "-" in head[4:]:                     # DUR-005-B and friends
            continue
        out.append((head, i + 1))
    return out


def entries_v4():
    """Every entry block, using entries.py's own gutter parser. The id is
    read from the FIELD BLOCK per A-12, and the heading is carried
    separately so a disagreement between the two is visible rather than
    resolved."""
    out = []
    for head_id, n in entry_ids():
        lines = _section("### %s" % head_id, stop_prefix=("### ", "## "))
        block = E._fenced_blocks(lines)[0]
        fields = E._parse_gutter(block, SCHEMA_COL)
        rec, order = {}, []
        for name, value, _k in fields:
            rec[name] = value
            order.append(name)
        out.append({"id": rec.get("id", head_id),
                    "heading_id": head_id,
                    "id_in_field_block": "id" in rec,
                    "id_matches_heading": rec.get("id") == head_id,
                    "name": rec.get("name"),
                    "line_no": n, "fields": rec, "order": order,
                    "n_lines": len(block)})
    return out


def field_coverage(recs=None, names=None, optional=None):
    """Which schema fields each entry block carries, and which it does
    not. The order's own rule: an entry missing any field is an UNRATED
    PART, filed as such. A DECLARED OPTIONAL field absent does not fire
    the rule (A-15); an UNDECLARED field present is reported as extra and
    does not fire it either, since the rule is about absence."""
    names = schema_field_names() if names is None else names
    optional = (declared_optional_fields() if optional is None
                else optional)
    required = [f for f in names if f not in optional]
    rows = []
    for rec in (entries_v4() if recs is None else recs):
        missing = [f for f in required if f not in rec["fields"]]
        extra = [f for f in rec["order"]
                 if f not in names and f not in optional]
        rows.append({"id": rec["id"], "missing": missing, "extra": extra,
                     "n_fields": len(rec["order"]),
                     "unrated_part": bool(missing)})
    return {"schema_n": len(names), "required_n": len(required),
            "optional": list(optional), "rows": rows,
            "unrated_parts": [r["id"] for r in rows if r["unrated_part"]],
            "rating_vector": [(r["id"],
                               "UNRATED_PART" if r["unrated_part"] else "RATED")
                              for r in rows]}


def reconstruction_values(rec):
    return E2.reconstruction_values(rec)


def evidence_values(rec):
    return E2.evidence_values(rec)


# ----------------------------------------------------- ambient sets

def _table_rows(section_heading, index, header_startswith):
    """[CHOICE 3] v4 carries the candidate sets as fixed-width tables
    whose first column wraps onto an INDENTED continuation line, and the
    other columns arrive on whichever physical line has them -- in the
    carrier-side table that is the continuation, not the row start.

    So a row is returned as its GROUP of physical lines. Joining them
    into one string first would move every column boundary and read the
    wrong cells, which is what a first version of this reader did."""
    lines = _section(section_heading, stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[index]
    header = None
    rows = []
    for line in block:
        if not line.strip():
            continue
        if header is None and line.startswith(header_startswith):
            header = line
            continue
        if header is None:
            continue
        if line.startswith("  ") and rows:
            rows[-1].append(line)
            continue
        rows.append([line])
    return header, rows


def _cells(group, bounds):
    """One cell per (start, end) bound, taken from whichever physical
    line of the row supplies it. The first column is the JOIN of every
    line's first column, since that is the one that wraps."""
    out = []
    for k, (i, j) in enumerate(bounds):
        vals = []
        for line in group:
            cell = (line[i:j] if j is not None else line[i:]).strip()
            if cell:
                vals.append(cell)
        out.append(" ".join(vals) if k == 0 else (vals[-1] if vals else ""))
    return out


def artifact_side_ambient():
    """The 7 artifact-side candidates, names only -- the columns beside
    them are the EXPECTED LIFETIME and ADMITTED columns A-16 reports
    empty, read separately by artifact_side_table()."""
    return [r["candidate"] for r in artifact_side_table()["rows"]]


def artifact_side_table():
    header, rows = _table_rows("### DUR-005", 2, "CANDIDATE")
    i = header.find("EXPECTED LIFETIME")
    j = header.find("ADMITTED")
    bounds = [(0, i), (i, j), (j, None)]
    out = []
    for group in rows:
        cand, life, adm = _cells(group, bounds)
        out.append({"candidate": cand, "expected_lifetime": life,
                    "admitted": adm})
    return {"header": header, "rows": out, "n": len(out)}


def carrier_side_ambient():
    return [r["candidate"] for r in carrier_side_table()["rows"]]


def carrier_side_table():
    header, rows = _table_rows("### DUR-005", 4, "CANDIDATE")
    i = header.find("PRODUCING MECH")
    j = header.find("RATE")
    k = header.find("ADMITTED")
    bounds = [(0, i), (i, j), (j, k), (k, None)]
    out = []
    for group in rows:
        cand, mech, rate, adm = _cells(group, bounds)
        out.append({"candidate": " ".join(cand.split()),
                    "producing_mech": mech, "rate": rate, "admitted": adm})
    return {"header": header, "rows": out, "n": len(out)}


def instrument_status():
    """DUR-005's INSTRUMENT STATUS block -- the order's own reading of
    its active ambient set."""
    lines = _section("### DUR-005", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[1]
    return {"raw": block, "text": "\n".join(block)}


def screen_rule():
    """DUR-005-C, from its bold marker to the end of the DUR-005 section.

    The pseudo-code fence alone is not the screen: its no-null property
    is stated in the PROSE under it, and register_v2.screen_has_null
    reads that sentence. Returning the fence alone would have made the
    check silent without saying so."""
    lines = _section("### DUR-005", stop_prefix=("### ", "## "))
    out, inside = [], False
    for line in lines:
        if line.startswith("**DUR-005-C"):
            inside = True
        if inside:
            out.append(line)
    return "\n".join(out) if out else "\n".join(
        E._fenced_blocks(lines)[-1])


# ------------------------------------------------------ 4, 5, 6, 7

def transfer_modes():
    lines = _section("### DUR-006", stop_prefix=("### ", "## "))
    for block in E._fenced_blocks(lines):
        if block and block[0].startswith("MODE"):
            header = block[0]
            i = header.find("ARTIFACT")
            j = header.find("CARRIERS")
            k = header.find("RESULT")
            out = []
            for line in block[1:]:
                if not line.strip():
                    continue
                out.append({"mode": line[:i].strip(),
                            "artifact": line[i:j].strip(),
                            "carriers": line[j:k].strip(),
                            "result": line[k:].strip()})
            return out
    raise ValueError("transfer-mode table not found")


def conjunction_terms():
    lines = _section("### DUR-006", stop_prefix=("### ", "## "))
    for block in E._fenced_blocks(lines):
        if block and block[0].startswith("TERM"):
            i = block[0].find("WHAT WOULD")
            out = []
            for line in block[1:]:
                if not line.strip():
                    continue
                if line.startswith(" " * i):
                    if out:
                        out[-1]["ensured"] += " " + line.strip()
                    continue
                out.append({"term": line[:i].strip(),
                            "ensured": line[i:].strip()})
            return out
    raise ValueError("conjunction table not found")


def parser_gate():
    return "\n".join(_section("## 6. THE EXTRACTION GATE",
                              stop_prefix=("---", "## ")))


def parser_gate_fields():
    """6-1's three fields plus 6-2's fourth requirement. The fourth is
    the whole of A-18 and is read out of 6-2's own RULE line, not
    inferred from the three."""
    three = _section("### 6-1", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(three)[0]
    fields, buys, key = [], {}, None
    for line in block:
        s = line.strip()
        if not s:
            continue
        if line.startswith("THREE FIELDS"):
            key = "three"
            fields.append(line[15:].strip())
        elif line.startswith("BUYS"):
            key = "buys"
            buys["buys"] = line[15:].strip()
        elif line.startswith("DOES NOT BUY"):
            key = "does_not_buy"
            buys["does_not_buy"] = line[15:].strip()
        elif line.startswith("  "):
            # A continuation belongs to whichever key is open. Reading
            # every indented line as a field is what put the tail of
            # DOES NOT BUY into the three-field list.
            if key == "three":
                fields.append(s)
            elif key in buys:
                buys[key] += " " + s
    disc = _section("### 6-2", stop_prefix=("### ", "## "))
    dblock = E._fenced_blocks(disc)[0]
    drows = E._parse_gutter(dblock, 20)
    return {"three": fields, "buys": buys,
            "discriminator": dict((n, v) for n, v, _k in drows),
            "fourth_requirement_stated": any(
                "EMITTED BY THE EXTRACTION" in v
                for _n, v, _k in drows)}


def format_rule_6_4():
    return "\n".join(_section("### 6-4", stop_prefix=("---", "## ")))


def steps():
    lines = _section("## 7. PROCEDURE", stop_prefix=("### ", "## "))
    block = E._fenced_blocks(lines)[0]
    return E._parse_gutter(block, 8)


# ------------------------------------------------------- 8, 10, 11

def falsifiers_v4():
    """[(id, text)] from section 8's fence."""
    lines = _section("## 8. FALSIFIERS", stop_prefix=("---", "## "))
    block = E._fenced_blocks(lines)[0]
    out, cur = [], None
    for line in block:
        s = line.strip()
        if s.startswith("F_") and len(s) > 3 and s[3] == " ":
            cur = [s[:3], s[3:].strip()]
            out.append(cur)
        elif cur is not None and s:
            cur[1] += " " + s
    return [(a, b) for a, b in out]


def amendments():
    """{'A-01': text} -- the short-form block plus the v4 detail blocks."""
    lines = _section("## 10. AMENDMENT RECORD", stop_prefix=("---", "## "))
    blocks = E._fenced_blocks(lines)
    out = {}
    short = E._parse_gutter(blocks[0], 6)
    for name, value, _k in short:
        out[name] = {"form": "short", "text": value}
    for block in blocks[1:]:
        # v4 carries A-12..A-18 in ONE fence, each amendment a paragraph
        # separated by a blank line. Split on blank lines rather than on
        # fences, or only the first is read.
        para = []
        for line in list(block) + [""]:
            if line.strip():
                para.append(line)
                continue
            if not para:
                continue
            head = para[0].strip()
            aid = head.split()[0]
            rows = E._parse_gutter(para[1:], AMEND_COL)
            out[aid] = {"form": "full", "title": head[len(aid):].strip(),
                        "fields": dict((n, v) for n, v, _k in rows),
                        "order": [n for n, _v, _k in rows]}
            para = []
    return out


def still_open():
    """{'D-01': text} from section 11."""
    lines = _section("## 11. OPEN DEFECTS", stop_prefix=("---", "## "))
    block = E._fenced_blocks(lines)[0]
    rows = E._parse_gutter(block, OPEN_COL)
    return dict((n, v) for n, v, _k in rows)


# -------------------------------------- D-06: the mechanical check

def _is_table_block(block):
    """A fenced block is a fixed-width TABLE if its first non-blank line
    is an all-caps header with two or more column labels separated by two
    or more spaces, and at least one row follows it."""
    body = [l for l in block if l.strip()]
    if len(body) < 2:
        return None
    header = body[0]
    if header.startswith(" "):
        return None
    labels = [p for p in header.split("  ") if p.strip()]
    # [CHOICE 5] three columns, not two. A two-column fixed-width block
    # and a GUTTER block are the same shape -- 0-1's STATUS block and
    # DUR-006-B's TERM table both read as tables under a two-column rule,
    # and both are key-plus-wrapped-value. The cost is stated rather than
    # tuned away: a genuine two-column table is not scanned, and no
    # threshold separates the two cases because there is no difference
    # between them to separate.
    if len(labels) < 3:
        return None
    stripped = header.replace(" ", "")
    if not stripped.isupper() or not stripped.isalpha():
        return None
    return header


def _header_columns(header):
    """Column starts from an all-caps header row, by label position."""
    cols, i = [], 0
    while i < len(header):
        if header[i] != " ":
            j = i
            while j < len(header):
                if header[j] == " " and header[j:j + 2] == "  ":
                    break
                j += 1
            cols.append((i, header[i:j].strip()))
            i = j
        else:
            i += 1
    out = []
    for k, (start, label) in enumerate(cols):
        end = cols[k + 1][0] if k + 1 < len(cols) else None
        out.append((label, start, end))
    return out


def fixed_width_tables(doc=None):
    """Every fixed-width table in the whole document, with its line
    numbers. [CHOICE 4] D-06's recurrence was in a table the V-map check
    did not look at, so the scan is document-wide.

    `doc` takes another document's lines, so the check can be RUN against
    the versions whose defect it exists to catch. A check never shown
    firing is not known to discriminate."""
    doc = _lines() if doc is None else doc
    out, cursor = [], 0
    for block in E._fenced_blocks(doc):
        header = _is_table_block(block)
        if header is None:
            continue
        try:
            n0 = doc.index(header, cursor)
        except ValueError:
            continue
        cursor = n0 + 1
        rows, k = [], n0 + 1
        started = False
        for line in block[block.index(header) + 1:]:
            if line.strip():
                rows.append((k, line))
                started = True
            elif started:
                pass
            k += 1
        out.append({"header": header, "header_line": n0 + 1,
                    "columns": _header_columns(header), "rows": rows})
    return out


def format_rule_scan(doc=None, order_name=None):
    """D-06: the mechanical check, in the harness rather than in the text.

    Two readings of A-13's rule, reported apart because they fail
    differently:

      CUT        a column boundary falling inside a token. The locator is
                 then a false claim about where the cell ends -- the cell
                 to its left is truncated and the cell to its right
                 begins with somebody else's text. Found with the
                 imported boundary check, not by reading the table.
      GLYPH      a score or status cell carrying a hyphen, arrow or other
                 punctuation a cut can turn into a score. This is the
                 defect A-13 names; the rule against it is stated in
                 prose in 6-4, and D-06's finding is that a prose rule
                 does not propagate to new tables.
      COL0_WRAP  a row whose first column carries text and whose every
                 other column is blank. In a fixed-width table that is a
                 first-column line wrap, and it is INDISTINGUISHABLE from
                 a new row with only its first cell filled. Reported
                 rather than resolved: which one it is depends on the
                 sentence, and a reader guessing is the defect.
    """
    order_name = order_name or ORDER_NAME
    doc = _lines() if doc is None else doc
    tables = fixed_width_tables(doc)
    cuts, glyphs, wraps = [], [], []
    for tbl in tables:
        cols = tbl["columns"]
        for n, line in tbl["rows"]:
            for label, i, j in cols:
                loc = S.Locator(order_name, n, i, j, label)
                ok, which = loc.boundary_clean(line)
                if not ok:
                    cuts.append({"line_no": n, "column": label,
                                 "cuts": list(which),
                                 "header": tbl["header"],
                                 "cell": line[i:j] if j else line[i:],
                                 "spill": line[j:].strip() if j else ""})
                cell = (line[i:j] if j else line[i:]).strip()
                if not cell or label in FREE_TEXT_COLUMNS:   # [CHOICE 6]
                    continue
                bad = [g for g in FORBIDDEN_IN_SCORE_CELL if g in cell]
                if bad:
                    glyphs.append({"line_no": n, "column": label,
                                   "cell": cell, "glyphs": bad,
                                   "header": tbl["header"]})
        w0 = cols[0][2] or None

        def _col0(s):
            return s[:w0] if w0 else s

        def _rest(s):
            return "".join((s[i:j] if j else s[i:]) for _lab, i, j in cols[1:])

        rows = tbl["rows"]
        for k, (n, line) in enumerate(rows):
            if not _col0(line).strip() or _rest(line).strip():
                continue
            # A first-column-only row is the normal shape when the row's
            # other cells arrive on an INDENTED continuation line, which
            # is how both candidate tables wrap. It is ambiguous only
            # when nothing supplies them: then the line is either a wrap
            # of the row above or a new row with one cell filled, and
            # the table does not say which.
            nxt = rows[k + 1][1] if k + 1 < len(rows) else None
            if nxt is not None and nxt.startswith(" ") and _rest(nxt).strip():
                continue
            wraps.append({"line_no": n, "header": tbl["header"],
                          "cell": _col0(line).strip()})
    return {"document": order_name, "n_tables": len(tables),
            "cuts": cuts, "n_cuts": len(cuts),
            "glyphs": glyphs, "n_glyphs": len(glyphs),
            "col0_wraps": wraps, "n_col0_wraps": len(wraps),
            "clean": not cuts and not glyphs and not wraps,
            "choice": 4}


def render_choices():
    out = ["CHOICES -- entries_v4.py", ""]
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out)


def main(argv):
    if "--choices" in argv:
        print(render_choices())
        return 0
    if "--selftest" in argv:
        sys.stderr.write(
            "entries_v4.py is a parser. The checks live in "
            "test_register_v4.py; run `python3 test_register_v4.py`.\n")
        return 2
    print("WORK_ORDER_V4.md")
    print("  entries        %d" % len(entries_v4()))
    print("  schema fields  %d required, %s optional"
          % (field_coverage()["required_n"],
             declared_optional_fields() or "none"))
    print("  V-map rows     %d" % len(_vmap_lines()))
    print("  falsifiers     %d" % len(falsifiers_v4()))
    print("  amendments     %d" % len(amendments()))
    print("  open defects   %d" % len(still_open()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
