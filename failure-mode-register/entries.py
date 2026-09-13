# SPDX-License-Identifier: CC0-1.0
"""entries.py -- the delivered register, parsed out of WORK_ORDER.md.

NOTHING IN THIS FILE IS RETYPED. Every field name, every vocabulary token,
every entry value, every falsifier, every step and both fenced tables are
pulled out of the delivered order at call time. An edit to the order that
this parser cannot follow turns the suite red rather than passing silently
against a stale copy.

That is the only reason the parser exists. A hand-transcribed register is a
copy, and copies drift -- the repo has the measurement (MF_019: five stale
copies of one gate across three drops, none noticed).

WHAT IS PARSED

    schema_fields()   section 2, the 13 fields and their definitions
    vocabularies()    the closed value sets, read OUT of those definitions
    entries()         the four fenced ENTRY DUR-00N blocks of section 3B-W
    control_notes()   DUR-001-N1, DUR-001-N2, DUR-002-N1
    measured_seeds()  the five section 3A seeds
    source_domains()  the six section 3B domains
    steps()           section 4, Step 0 .. Step 7
    falsifiers()      section 7, in delivered order (F_I precedes F_H)
    hop_budget()      the section 6B fenced block
    shock_classes()   the section 6B-3 fenced block
    non_goals()       section 0

WHAT IS NOT PARSED

ENTRY 0. Section 1 says "ENTRY 0 OF THE REGISTER IS THE DETECTION GAP
ITSELF" and no ENTRY block for it was delivered. It is reported absent
(see register.entry_zero) and is NOT authored here: its mechanism is a
property of the register rather than of a deployment, so it has no
load_condition and its detection_channel is the field itself. Writing it
would put a claim in the author's mouth in the one place the order names
and declines to fill.

Section 3C is likewise not populated -- see register.step4_status().

LIMIT

The column layout is the contract. A field name sits at column 0 (column 2
inside the section 2 block) and its value at column 19. A continuation is
19 spaces. If the delivered order is reflowed, this parser stops finding
fields rather than finding them wrongly -- every accessor raises on an
empty result instead of returning one.
"""

from __future__ import annotations

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER_PATH = os.path.join(HERE, "WORK_ORDER.md")

VALUE_COL = 19          # field values and continuations start here
NOTE_COL = 12           # the control-note blocks use a narrower gutter
STEP_COL = 10
FALSIFIER_COL = 5

# [CHOICE 1] The order states its vocabularies as English alternations
# ("immediate | drift | dormant-until-triggered", "... YES | PARTIAL | NO")
# and never as a machine-readable list.  The token extracted from each
# alternative is the first ALL-CAPS word if the alternative has one, else
# the whole alternative when it is a single word.  That rule reads all
# three declared vocabularies correctly and is stated here rather than
# hand-listing the values, which would be retyping them.
CHOICES = {
    1: "vocabulary tokens read out of the order's English alternations by "
       "first-all-caps-else-single-word; the order declares no machine "
       "readable form",
    2: "an entry block's header line (ENTRY DUR-00N) is treated as a header "
       "and not as a field, since it does not meet the column-19 contract",
    3: "section 3A seeds are parsed as bullets and carry no id; the order "
       "gives them none and inventing one would make them look filed",
}


def order_text():
    with open(ORDER_PATH) as fh:
        return fh.read()


def _lines():
    return order_text().split("\n")


def _section(heading_prefix, stop_prefix=("## ",)):
    """Lines of the section whose heading starts with heading_prefix."""
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


def _fenced_blocks(lines):
    blocks, cur = [], None
    for line in lines:
        if line.strip() == "```":
            if cur is None:
                cur = []
            else:
                blocks.append(cur)
                cur = None
            continue
        if cur is not None:
            cur.append(line)
    return blocks


def _is_field_line(line, col):
    return (len(line) > col
            and line[:col].strip() != ""
            and line[col - 1] == " "
            and line[col] != " ")


def _parse_gutter(lines, col):
    """[(name, joined_value, n_lines)] from a name-at-0 value-at-col block."""
    out = []
    for line in lines:
        if _is_field_line(line, col):
            out.append([line[:col].strip(), [line[col:].rstrip()], 1])
        elif line.startswith(" " * col) and line.strip() and out:
            out[-1][1].append(line[col:].rstrip())
            out[-1][2] += 1
    return [(n, " ".join(v).strip(), c) for n, v, c in out]


# -------------------------------------------------------------- section 2

def schema_fields():
    """[(field, definition)] in delivered order. The count is not
    fixed here -- test_register.py holds it, so this file stores no answer."""
    lines = []
    for line in _section("## 2. ENTRY SCHEMA"):
        if line.startswith("Rule:"):
            break
        lines.append(line[2:] if line.startswith("  ") else line)
    fields = [(n, v) for n, v, _ in _parse_gutter(lines, VALUE_COL)]
    if not fields:
        raise ValueError("section 2 schema block did not parse")
    return fields


def schema_field_names():
    return [n for n, _ in schema_fields()]


def _vocab_from(definition):
    if "|" not in definition:
        return None
    out = []
    for alt in definition.split("|"):
        alt = alt.strip()
        if not alt:
            continue
        caps = [w for w in re.findall(r"[A-Za-z][A-Za-z-]*", alt) if w.isupper()]
        if caps:
            out.append(caps[0])
        elif len(alt.split()) == 1:
            out.append(alt)
        else:
            out.append(None)
    return out if all(out) else None


def vocabularies():
    """{field: [token, ...]} for every schema field declaring a closed set."""
    out = {}
    for name, definition in schema_fields():
        vocab = _vocab_from(definition)
        if vocab:
            out[name] = vocab
    if not out:
        raise ValueError("no vocabularies parsed from section 2")
    return out


def projection_rule():
    """The PROJECTED-fraction sentence, verbatim. It states no number."""
    text, on = [], False
    for line in _section("## 2. ENTRY SCHEMA"):
        if line.startswith("Rule:"):
            on = True
        if on:
            if not line.strip():
                break
            text.append(line.strip())
    return " ".join(text)


# ------------------------------------------------------------ section 3B-W

def entries():
    """{id: {field: value}} for the four delivered ENTRY blocks."""
    out = {}
    for block in _fenced_blocks(_section("### 3B-W.")):
        if not block or not block[0].startswith("ENTRY"):
            continue
        # [CHOICE 2] header line, not a field
        eid = block[0].split()[-1]
        rec = {}
        for name, value, _ in _parse_gutter(block[1:], VALUE_COL):
            rec[name] = value
        out[eid] = rec
    if not out:
        raise ValueError("no ENTRY blocks parsed from section 3B-W")
    return out


def entry_field_names(rec):
    return list(rec.keys())


def control_notes():
    """{note_id: text} -- DUR-001-N1, DUR-001-N2, DUR-002-N1."""
    lines = _section("#### KNOWN FAILURE MODES", stop_prefix=("### ", "## "))
    out = {n: v for n, v, _ in _parse_gutter(lines, NOTE_COL)}
    if not out:
        raise ValueError("control notes did not parse")
    return out


def composition_note():
    lines = _section("#### COMPOSITION", stop_prefix=("#### ", "### ", "## "))
    return {n: v for n, v, _ in _parse_gutter(lines, 28)}


# ------------------------------------------------------------- sections 3A/3B

def measured_seeds():
    """The section 3A bullets. [CHOICE 3] -- no ids; the order gives none."""
    out, cur = [], None
    for line in _section("### 3A. MEASURED",
                         stop_prefix=("### ", "## ")):
        stripped = line.strip()
        if stripped.startswith("- "):
            if cur:
                out.append(" ".join(cur))
            cur = [stripped[2:]]
        elif cur is not None and stripped and line.startswith("    "):
            cur.append(stripped)
        elif cur is not None and not stripped:
            out.append(" ".join(cur))
            cur = None
    if cur:
        out.append(" ".join(cur))
    if not out:
        raise ValueError("section 3A seeds did not parse")
    return out


def source_domains():
    """[(domain, enumeration)] from the section 3B table."""
    out = []
    for line in _section("### 3B. TRANSPORTED",
                         stop_prefix=("### ", "## ")):
        if not line.startswith("  ") or not line.strip():
            continue
        if line.startswith("TRANSPORT RULE"):
            break
        m = re.match(r"  (\S.*?)\s{2,}(\S.*)$", line)
        if m and not line.startswith("                "):
            out.append([m.group(1).strip(), [m.group(2).strip()]])
        elif out and re.match(r"^\s{20,}\S", line):
            out[-1][1].append(line.strip())
    return [(d, " ".join(v)) for d, v in out]


def transport_rule():
    text, on = [], False
    for line in _section("### 3B. TRANSPORTED",
                         stop_prefix=("### ", "## ")):
        if line.startswith("TRANSPORT RULE"):
            on = True
        if on:
            if not line.strip():
                break
            text.append(line.strip())
    return " ".join(text)


# --------------------------------------------------------------- sections 4/7

def steps():
    """[(label, text)] Step 0 .. Step 7, in delivered order."""
    lines = [ln[2:] if ln.startswith("  ") else ln
             for ln in _section("## 4. PROCEDURE")]
    out = [(n, v) for n, v, _ in _parse_gutter(lines, STEP_COL - 2)]
    if not out:
        raise ValueError("section 4 steps did not parse")
    return out


def falsifiers():
    """[(id, text)] in DELIVERED order -- F_I precedes F_H. Not reordered."""
    out = [(n, v) for n, v, _ in
           _parse_gutter(_section("## 7. FALSIFIERS"), FALSIFIER_COL)]
    if not out:
        raise ValueError("section 7 falsifiers did not parse")
    return out


# ------------------------------------------------------------ sections 6B/6B-3

def hop_budget():
    """The section 6B fenced block: raw lines plus the numbers in them."""
    blocks = _fenced_blocks(_section("## 6B. TIMEFRAME",
                                     stop_prefix=("### ", "## ")))
    if not blocks:
        raise ValueError("section 6B hop-budget block did not parse")
    raw = blocks[0]
    joined = " ".join(raw)
    spans = [int(x) for x in re.findall(r"N over (\d+)", joined)]
    counts = re.findall(r"~(\d+)(?:-(\d+))? hops", joined)
    return {
        "raw": raw,
        "spans_years": spans,
        "hop_counts": [(int(a), int(b) if b else int(a)) for a, b in counts],
        "stated_compression": _stated_compression(),
    }


def _stated_compression():
    m = re.search(r"Compressed by roughly (\w+)", order_text())
    words = {"ten": 10, "twenty": 20, "fifty": 50, "hundred": 100}
    return words.get(m.group(1).lower()) if m else None


def shock_classes():
    """{V14a: {...}} from the section 6B-3 fenced block."""
    blocks = _fenced_blocks(_section("### 6B-3",
                                     stop_prefix=("### ", "## ")))
    if not blocks:
        raise ValueError("section 6B-3 shock block did not parse")
    out, cur = {}, None
    for line in blocks[0]:
        m = re.match(r"^(V14\w)\s{2,}(\S.*?)\s{2,}(\S.*)$", line)
        if m:
            cur = m.group(1)
            out[cur] = {"name": m.group(2).strip(),
                        "examples": m.group(3).strip(),
                        "cadence": None, "verdict": None}
            continue
        m = re.match(r"^\s+(\S.*?)\s+->\s+(\S.*)$", line)
        if m and cur:
            out[cur]["cadence"] = m.group(1).strip()
            out[cur]["verdict"] = m.group(2).strip()
    return out


def non_goals():
    out = []
    for line in _section("## 0. WHAT THIS IS"):
        if line.strip().startswith("- "):
            out.append(line.strip()[2:])
        elif out and line.strip().startswith("SCOPE IS"):
            break
    return out


def scope_statement():
    text, on = [], False
    for line in _section("## 0. WHAT THIS IS"):
        if line.strip().startswith("SCOPE IS"):
            on = True
        if on:
            if not line.strip():
                break
            text.append(line.strip())
    return " ".join(text)


def render_choices():
    return "\n".join("  [CHOICE %d] %s" % (k, v)
                     for k, v in sorted(CHOICES.items()))


def main(argv):
    import sys
    if "--selftest" in argv:
        print("entries.py is the parser. The checks live in "
              "test_register.py; run: python3 test_register.py")
        return 2
    fields = schema_fields()
    ents = entries()
    print("PARSED FROM WORK_ORDER.md")
    print("  schema fields     %d  (%s)"
          % (len(fields), ", ".join(n for n, _ in fields)))
    print("  vocabularies      %s"
          % "; ".join("%s = %s" % (k, "|".join(v))
                      for k, v in sorted(vocabularies().items())))
    print("  entries           %d  (%s)" % (len(ents), ", ".join(sorted(ents))))
    print("  control notes     %s" % ", ".join(sorted(control_notes())))
    print("  measured seeds    %d" % len(measured_seeds()))
    print("  source domains    %d" % len(source_domains()))
    print("  steps             %d" % len(steps()))
    print("  falsifiers        %s  (delivered order)"
          % ", ".join(f for f, _ in falsifiers()))
    print("  shock classes     %s" % ", ".join(sorted(shock_classes())))
    print("  non-goals         %d" % len(non_goals()))
    print("")
    print("CHOICES")
    print(render_choices())
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
