#!/usr/bin/env python3
"""Build GAP_INDEX.md -- one row per open question, across every folder.

WHAT THIS READS

  Each folder renders its open questions in one of two places:

    a standalone  OPEN_QUESTIONS.md
    a section     "## OPEN_QUESTIONS.md" inside OPEN_RESEARCH.md

  and in one of two shapes:

    field form    **Gap:** ... / **Knowledge state:** ...
    table form    | Gap: ... | 中文 ... |          (bilingual folders)

  All four combinations occur in this tree, so the reader is written
  against the CONTENT and not against a filename or a heading level.
  That is OR_015's lesson: two passes globbed for a name and two passes
  missed everything not called that.

WHAT THIS DOES NOT DO

  It does not infer. Every emitted cell is a field the document declared,
  or the string 'unrecorded'. There is no keyword classifier deciding
  what a gap needs or which discipline it belongs to, because a word list
  deciding meaning is the failure nonidentity-census T1-1 measured at
  10 of 12.

  A folder with no open-questions document is skipped in silence. That is
  not a finding about the folder; most folders here were never rendered.

USAGE
  python3 tools/gap_index.py            print the index to stdout
  python3 tools/gap_index.py --write    write GAP_INDEX.md at the repo root
  python3 tools/gap_index.py --selftest run the checks

Stdlib only. Parses under 3.9. CC0.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

GAPS_DOC = "OPEN_QUESTIONS.md"
BATCH_DOC = "OPEN_RESEARCH.md"
UNRECORDED = "unrecorded"

# a heading or a bare line that opens a numbered entry:  "3. CLASS — Title"
# and the Q-notation a prose question list uses:           "## Q3 — Title"
ENTRY_RE = re.compile(r"^#{0,4}\s*(\d+)\.\s+(.+?)\s*$")
QENTRY_RE = re.compile(r"^#{1,4}\s*Q(\d+)\s*[—–-]\s*(.+?)\s*$")
# a declared field in field form.  Two renderings occur: the colon outside
# the bold (**Gap:** value) and inside it (**State: value**).
FIELD_RE = re.compile(
    r"^\*\*([A-Z][A-Za-z /-]*?):(?:\*\*\s*(.*)|\s*(.*?)\*\*)\s*$")
# a declared field inside the English cell of a bilingual table row
CELL_RE = re.compile(r"^\|\s*([A-Z][A-Za-z /-]*?):\s*(.*?)\s*\|")
# the section that ends the gaps region
END_RE = re.compile(r"^#{1,3}\s*SCOPE_BOUNDARY", re.I)
START_RE = re.compile(r"^#{1,3}\s*(OPEN[ _]QUESTIONS)", re.I)

WANT = {
    "gap": "gap",
    "knowledge state": "state",
    "state": "state",
    "disciplines": "disciplines",
    "data sources": "needs",
    "falsifier": "falsifier",
    "research question": "question",
    "expected deliverable": "deliverable",
    # the DECISION template's own fields (RESEARCH_RENDER section 3)
    "fork": "fork",
    "winning condition": "winning",
    "discriminator": "discriminator",
    "blocked by": "blocked",
    "who could run it": "runner",
    "if you run it": "opens",
}

# the three source kinds RESEARCH_RENDER section 3 specifies; detected as
# literal declared markers, never inferred from wording
KINDS = ("EXISTING RECORD", "YOUR OWN DATA", "SOMEONE'S HANDS")
NO_SLOT = "no slot (DECISION)"

DASHES = ("—", "–", " - ")


def _clean(s):
    s = re.sub(r"[*`]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def split_class(title):
    """CLASS — Title  ->  (class, title). No dash means no declared class."""
    t = _clean(title)
    # bilingual entries append ' / 中文'; keep the English side
    for d in DASHES:
        if d in t:
            head, rest = t.split(d, 1)
            head = head.strip()
            # a class token is short and not a sentence
            if head and len(head) <= 60:
                return head, rest.strip()
            return UNRECORDED, t
    return UNRECORDED, t


def entry_type(cls):
    return "DECISION" if cls.upper().startswith("DECISION") else "GAP"


def gaps_region(lines):
    """Return the slice of lines holding the open-questions document."""
    start = None
    for i, l in enumerate(lines):
        if START_RE.match(l.strip()):
            start = i + 1
            break
    if start is None:
        return None
    for j in range(start, len(lines)):
        if END_RE.match(lines[j].strip()):
            return lines[start:j]
    return lines[start:]


def _next_nonblank(lines, i):
    for j in range(i + 1, min(i + 4, len(lines))):
        if lines[j].strip():
            return lines[j].strip()
    return ""


def is_opener(lines, i):
    """True iff line i opens a numbered entry.

    A numbered method step is also a numbered line, and some of them carry
    an em dash, so a dash is not the discriminator. Two shapes open an
    entry and nothing else does: a numbered HEADING (field form), and a
    bare numbered line immediately followed by a table (bilingual form).
    """
    l = lines[i]
    if QENTRY_RE.match(l.strip()):
        return True
    if not ENTRY_RE.match(l.strip()):
        return False
    if l.lstrip().startswith("#"):
        return True
    return _next_nonblank(lines, i).startswith("|")


def _list_below(lines, i):
    """A field whose inline value is empty continues as a list beneath it."""
    vals = []
    for j in range(i + 1, len(lines)):
        t = lines[j].strip()
        if not t:
            if vals:
                break
            continue
        if t.startswith(("- ", "* ")) or re.match(r"^\d+\.\s", t):
            vals.append(_clean(re.sub(r"^([-*]|\d+\.)\s*", "", t)))
            continue
        if any(t.startswith(k) for k in KINDS):
            vals.append(_clean(t))
            continue
        break
    return "; ".join(vals)


def parse_entries(lines):
    """Split a gaps region into entries, reading declared fields only."""
    out = []
    cur = None
    for i, raw in enumerate(lines):
        l = raw.rstrip()
        if is_opener(lines, i):
            if cur:
                out.append(cur)
            m = QENTRY_RE.match(l.strip()) or ENTRY_RE.match(l.strip())
            cls, title = split_class(m.group(2))
            cur = {"n": m.group(1), "class": cls, "title": title, "fields": {}}
            continue
        if cur is None:
            continue
        fm = FIELD_RE.match(l.strip()) or CELL_RE.match(l.strip())
        if fm:
            key = fm.group(1).strip().lower()
            if key in WANT:
                groups = [g for g in fm.groups()[1:] if g]
                val = _clean(groups[0]) if groups else ""
                val = val or _list_below(lines, i)
                if val and WANT[key] not in cur["fields"]:
                    cur["fields"][WANT[key]] = val
    if cur:
        out.append(cur)
    return out


def find_docs(root=ROOT):
    """Every open-questions document in the tree, by content."""
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        rel = os.path.relpath(dirpath, root)
        folder = "." if rel == "." else rel
        for fn in sorted(filenames):
            if fn not in (GAPS_DOC, BATCH_DOC):
                continue
            path = os.path.join(dirpath, fn)
            lines = open(path, encoding="utf-8").read().split("\n")
            region = gaps_region(lines)
            if region is None:
                continue
            found.append((folder, fn, region))
    return sorted(found)


def build_row(folder, fn, e):
    """One index row from one parsed entry.

    A DECISION entry's columns are mapped from its own template fields:
    disciplines carries Who-could-run-it and needs carries Blocked-by —
    the schema's routing pair — and state reads NO_SLOT, because the
    DECISION template has no knowledge-state field. A slot that does not
    exist is a different statement from one left empty, so NO_SLOT and
    'unrecorded' are kept apart. A declared field always wins over the
    mapping.
    """
    f = e["fields"]
    t = entry_type(e["class"])
    if t == "DECISION":
        disciplines = f.get("disciplines") or f.get("runner", UNRECORDED)
        needs = f.get("needs") or f.get("blocked", UNRECORDED)
        state = f.get("state") or NO_SLOT
        complete = all(k in f for k in
                       ("fork", "winning", "discriminator", "blocked",
                        "runner"))
    else:
        disciplines = f.get("disciplines", UNRECORDED)
        needs = f.get("needs", UNRECORDED)
        state = f.get("state", UNRECORDED)
        complete = all(k in f for k in
                       ("gap", "state", "disciplines", "needs",
                        "falsifier"))
    return {
        "id": "%s#%s" % (os.path.basename(folder), e["n"]),
        "folder": folder,
        "file": fn,
        "type": t,
        "class": e["class"],
        "title": e["title"],
        "disciplines": disciplines,
        "needs": needs,
        "state": state,
        "complete": complete,
    }


def collect(root=ROOT, silent_docs=None):
    rows = []
    for folder, fn, region in find_docs(root):
        entries = parse_entries(region)
        if not entries and silent_docs is not None:
            silent_docs.append((folder, fn))
        for e in entries:
            rows.append(build_row(folder, fn, e))
    return _disambiguate(rows)


# One id must name one entry. A folder can carry BOTH gap-bearing
# documents (uninstrumented/ does: OPEN_RESEARCH.md from the batch
# restoration, OPEN_QUESTIONS.md from WORK ORDER 03), and folder#n
# alone then names two different gaps -- the one-id-two-claims defect
# AUDIT_OPEN_RESEARCH.md records at file level, arriving at index
# level. The tag is derived from the FILENAME, never from content,
# and only appears where the collision exists, so every single-doc
# folder keeps its existing id.
_DOC_TAG = {"OPEN_QUESTIONS.md": "OQ", "OPEN_RESEARCH.md": "OR"}


def _disambiguate(rows):
    per_folder = {}
    for r in rows:
        per_folder.setdefault(r["folder"], set()).add(r["file"])
    for r in rows:
        if len(per_folder[r["folder"]]) > 1:
            base, n = r["id"].split("#")
            r["id"] = "%s/%s#%s" % (base, _DOC_TAG[r["file"]], n)
    return rows


def _first(s, limit=64):
    s = s.split(";")[0].split(",")[0].strip()
    return s if len(s) <= limit else s[:limit - 1] + "…"


def _split_list(s):
    if s == UNRECORDED:
        return [UNRECORDED]
    parts = re.split(r"[,;/]| and ", s)
    return [p.strip().lower() for p in parts if p.strip()]


def _tally(rows, key, splitter=None):
    d = {}
    for r in rows:
        vals = splitter(r[key]) if splitter else [r[key].lower()]
        for v in vals:
            d[v] = d.get(v, 0) + 1
    return sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))


def render(rows, silent_docs=()):
    L = []
    A = L.append
    A("# GAP_INDEX.md")
    A("")
    A("Every open question in this repository, one row each. Generated by")
    A("`tools/gap_index.py`; do not edit by hand — regenerate.")
    A("")
    A("A folder appears here only if it carries an open-questions document,")
    A("either as `OPEN_QUESTIONS.md` or as the section of that name inside")
    A("its `OPEN_RESEARCH.md`. Folders without one are skipped in silence:")
    A("most folders here have never been rendered, which is a fact about")
    A("the rendering pass and not about the folder.")
    A("")
    A("Every cell is a field the document declared. Where a document did")
    A("not declare one the cell reads `unrecorded`, which is a different")
    A("statement from a gap having no discipline or needing no data.")
    A("Nothing here is inferred from wording.")
    A("")
    if not rows:
        A("**No open-questions document found.**")
        return "\n".join(L) + "\n"
    folders = sorted(set(r["folder"] for r in rows))
    dec = sum(1 for r in rows if r["type"] == "DECISION")
    inc = sum(1 for r in rows if not r["complete"])
    A("```")
    A("entries        %d" % len(rows))
    A("folders        %d" % len(folders))
    A("of type GAP    %d" % (len(rows) - dec))
    A("of type DECISION %d" % dec)
    A("entries missing at least one of the five core fields   %d" % inc)
    A("```")
    A("")
    A("---")
    A("")
    A("## The index")
    A("")
    A("For a `DECISION` entry the columns are mapped from its own template")
    A("fields — `disciplines` carries *Who could run it* and `needs`")
    A("carries *Blocked by*, the schema's routing pair — and `state` reads")
    A("`no slot (DECISION)`, because a fork carries no knowledge-state")
    A("field. A slot that does not exist is a different statement from one")
    A("left empty.")
    A("")
    A("| id | folder | type | class | disciplines | needs | state |")
    A("|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (r["folder"], int(r["id"].split("#")[1]))):
        A("| `%s` | `%s` | %s | %s | %s | %s | `%s` |" % (
            r["id"], r["folder"], r["type"], _first(r["class"], 40),
            _first(r["disciplines"]), _first(r["needs"]), r["state"]))
    A("")
    A("---")
    A("")
    A("## By discipline")
    A("")
    A("Split on commas, semicolons, slashes and *and*, lowercased. A gap")
    A("naming three disciplines is counted under all three, so the column")
    A("sums past the entry count.")
    A("")
    tal = _tally(rows, "disciplines", _split_list)
    shown = [kv for kv in tal if kv[1] > 1]
    A("| discipline | entries |")
    A("|---|---|")
    for k, v in shown:
        A("| %s | %d |" % (k, v))
    A("")
    A("%d distinct strings in all, of which **%d appear once**. The field is"
      % (len(tal), len(tal) - len(shown)))
    A("free text, so it groups weakly; a discipline named two ways is two")
    A("rows here. Only the repeated ones are listed above.")
    A("")
    A("---")
    A("")
    A("## By what it needs")
    A("")
    A("Grouped on the first declared data source, verbatim and lowercased.")
    A("This is a string grouping and not a taxonomy: `RESEARCH_RENDER.md`")
    A("§3 specifies three source kinds — EXISTING RECORD, YOUR OWN DATA,")
    kinded = sum(1 for r in rows if any(k in r["needs"] for k in KINDS))
    A("SOMEONE'S HANDS — and **%d of %d entries declare one**; the rest"
      % (kinded, len(rows)))
    A("declare sources with no kind, so above the raw line there is")
    A("nothing to group them on.")
    A("")
    tal2 = _tally(rows, "needs", lambda s: [_first(s).lower()])
    shown2 = [kv for kv in tal2 if kv[1] > 1]
    A("| first declared source | entries |")
    A("|---|---|")
    for k, v in shown2:
        A("| %s | %d |" % (k, v))
    A("")
    A("%d distinct strings in all, of which **%d appear once**. Only the"
      % (len(tal2), len(tal2) - len(shown2)))
    A("repeated ones are listed above.")
    A("")
    A("---")
    A("")
    A("## By knowledge state")
    A("")
    A("`RESEARCH_RENDER.md` §5 KNOWLEDGE STATE. A value outside that")
    A("vocabulary is reported as written rather than mapped into it.")
    A("")
    VOCAB = ("measured", "unknown_atm", "under_study", "not_studied",
             "undefined", "unmeasured")
    tal3 = _tally(rows, "state")
    onvocab = sum(v for k, v in tal3 if k.split(" (")[0] in VOCAB)
    A("| state | entries |")
    A("|---|---|")
    for k, v in tal3:
        A("| `%s` | %d |" % (k, v))
    A("")
    A("**%d of %d** entries state one of the six §5 values, alone or with a"
      % (onvocab, len(rows)))
    A("parenthetical. The remaining %d carry something else — a sentence, a"
      % (len(rows) - onvocab))
    A("verdict, `no slot (DECISION)` (a fork has no knowledge-state field),")
    A("or nothing. They are listed as written above rather than sorted into")
    A("the vocabulary, because deciding which of the six a sentence means")
    A("is the inference this reader does not make.")
    A("")
    A("---")
    A("")
    A("## Documents this reader could not parse")
    A("")
    A("An open-questions document from which zero entries were read. The")
    A("entry shapes this reader knows are a numbered heading, a bare")
    A("numbered line above a table, and `Q<n>`. A document using a fourth")
    A("shape lands here rather than being reported as an empty folder,")
    A("because a folder with nine open questions and no rows is the one")
    A("outcome that reads as agreement with a silence.")
    A("")
    if silent_docs:
        for folder, fn in silent_docs:
            A("- `%s/%s`" % (folder, fn))
    else:
        A("None. Every document found yielded at least one entry.")
    A("")
    A("---")
    A("")
    A("CC0.")
    return "\n".join(L) + "\n"


# ------------------------------------------------------------------ checks

FIELD_FIXTURE = """
## OPEN_QUESTIONS.md

### 1. EMPIRICAL — A measurement nobody made

**Gap:** the thing is unmeasured

**Knowledge state:** NOT_STUDIED

**Research question:** what is it

**Disciplines:** Soil science, heat transfer

**Data sources:**

- Field measurements
- USDA NRCS soil surveys

**Method:**

1. do the thing
2. do the other thing

**Expected deliverable:** a number

**Falsifier:** the number does not move

### 2. DECISION — which convention

**Fork:** two conventions, both defensible

**Options:**
  A. convention one — what follows
  B. convention two — what follows

**Winning condition:** one transfers where the other does not

**Discriminator:** the overlap comparison

**Blocked by:** access to the operator's log

**Who could run it:** anyone inside the operator

**If you run it:** the fork closes

## SCOPE_BOUNDARY.md

### 1. NOT A GAP — this is past the end
""".split("\n")

KIND_FIXTURE = """
## OPEN_QUESTIONS.md

### 1. EMPIRICAL — kinds declared

**Gap:** g

**Knowledge state:** NOT_STUDIED

**Disciplines:** d

**Data sources:**
  EXISTING RECORD: the public archive
  YOUR OWN DATA: a coded corpus

**Falsifier:** f
""".split("\n")

TABLE_FIXTURE = """
## OPEN_QUESTIONS.md / 开放问题

1. Empirical — Table to predicate / 经验性

| English | 中文 |
|---|---|
| Gap: the classifier uses a word list | 空白： ... |
| Knowledge state: UNDEFINED | 知识状态： UNDEFINED |
| Disciplines: Computational linguistics, NLP | 学科： ... |
| Data sources: an annotated corpus | 数据来源： ... |
| Falsifier: it generalizes | 证伪： ... |

## SCOPE_BOUNDARY.md / 范围边界
""".split("\n")


def selftest():
    ok = fail = 0

    def check(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print("  FAIL  %s" % name)

    # -- field form
    r = gaps_region(FIELD_FIXTURE)
    check("field: region stops at SCOPE_BOUNDARY",
          r is not None and not any("past the end" in l for l in r))
    e = parse_entries(r)
    check("field: two entries", len(e) == 2)
    check("field: class read", e[0]["class"] == "EMPIRICAL")
    check("field: title read", e[0]["title"] == "A measurement nobody made")
    check("field: state read", e[0]["fields"]["state"] == "NOT_STUDIED")
    check("field: disciplines read",
          e[0]["fields"]["disciplines"] == "Soil science, heat transfer")
    check("field: numbered method steps are not entries",
          all(x["n"] in ("1", "2") for x in e))
    check("field: DECISION typed", entry_type(e[1]["class"]) == "DECISION")
    check("field: GAP typed", entry_type(e[0]["class"]) == "GAP")

    # -- the DECISION mapping, on the template's own fields
    dr = build_row("x", "OPEN_QUESTIONS.md", e[1])
    check("decision: needs carries Blocked by",
          dr["needs"] == "access to the operator's log")
    check("decision: disciplines carries Who could run it",
          dr["disciplines"] == "anyone inside the operator")
    check("decision: state is the no-slot marker, not unrecorded",
          dr["state"] == NO_SLOT)
    check("decision: template-complete", dr["complete"])
    gr = build_row("x", "OPEN_QUESTIONS.md", e[0])
    check("gap rows unchanged by the mapping",
          gr["state"] == "NOT_STUDIED" and gr["complete"])

    # -- declared source-kind lines are collected without bullets
    ek = parse_entries(gaps_region(KIND_FIXTURE))
    check("kind lines read from beneath the label",
          ek[0]["fields"].get("needs") ==
          "EXISTING RECORD: the public archive; YOUR OWN DATA: a coded corpus")
    check("field: a list-valued field is read from beneath its label",
          e[0]["fields"].get("needs") ==
          "Field measurements; USDA NRCS soil surveys")
    check("field: a numbered method step carrying a dash is not an entry",
          all("do the thing" not in x["title"] for x in e))
    inbold = parse_entries(["### 1. X — Y", "", "**State: yes, it is.**", ""])
    check("field: colon-inside-bold rendering is read",
          inbold[0]["fields"].get("state") == "yes, it is.")

    # -- table form
    r2 = gaps_region(TABLE_FIXTURE)
    e2 = parse_entries(r2)
    check("table: one entry", len(e2) == 1)
    check("table: state read from cell",
          e2 and e2[0]["fields"].get("state") == "UNDEFINED")
    check("table: English cell only",
          e2 and "空白" not in e2[0]["fields"].get("gap", ""))

    # -- no inference.  Read from the AST, not from the text: the first
    # version of this check grepped its own source for "def classify" and
    # fired on the line asserting the absence, which is IS_007 / RDD_008
    # in this module's own selftest.  A comment does not appear in an AST.
    import ast
    tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
    names = [n.name for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    check("no function infers a category from wording",
          not any(re.search(r"classif|infer|guess|categoriz", n) for n in names))

    # -- absent is not blank
    e3 = parse_entries(["### 1. X — Y", "", "**Gap:** g", ""])
    check("absent field is not silently blank",
          "disciplines" not in e3[0]["fields"])

    # -- render refuses nothing and says so on an empty corpus
    check("empty corpus renders a stated absence",
          "No open-questions document found" in render([]))

    # -- the Q-notation shape a prose question list uses
    qfx = ["## OPEN QUESTIONS", "", "## Q3 — IS IT MEASURED", "",
           "**State: yes, and it runs against the assumption.**", "",
           "**Gap:** the conflation is unexamined", ""]
    eq = parse_entries(gaps_region(qfx))
    check("Q-notation: entry read", len(eq) == 1 and eq[0]["n"] == "3")
    check("Q-notation: title read",
          eq and eq[0]["title"] == "IS IT MEASURED")

    # -- a document the reader cannot parse is named, not dropped
    check("unparsed document is reported",
          "could not parse" in render([{"id": "a#1", "folder": "a",
                                        "file": "x", "type": "GAP",
                                        "class": "C", "title": "t",
                                        "disciplines": "d", "needs": "n",
                                        "state": "s", "complete": True}],
                                      [("z", "OPEN_QUESTIONS.md")]))

    # -- id disambiguation: a folder carrying BOTH documents must not
    # let one id name two entries; a single-doc folder keeps its id
    twin = [{"id": "x#1", "folder": "x", "file": "OPEN_QUESTIONS.md"},
            {"id": "x#1", "folder": "x", "file": "OPEN_RESEARCH.md"},
            {"id": "y#1", "folder": "y", "file": "OPEN_QUESTIONS.md"}]
    twin = _disambiguate(twin)
    check("disambiguate: collision tagged",
          {r["id"] for r in twin[:2]} == {"x/OQ#1", "x/OR#1"})
    check("disambiguate: single-doc id untouched",
          twin[2]["id"] == "y#1")

    # -- live tree
    rows = collect()
    check("live: at least one document found", len(rows) > 0)
    check("live: every row has a folder", all(r["folder"] for r in rows))
    check("live: state never blank",
          all(r["state"] for r in rows))
    check("live: ids unique",
          len({r["id"] for r in rows}) == len(rows))
    print("selftest %d/%d" % (ok, ok + fail))
    return 0 if fail == 0 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    silent = []
    rows = collect(silent_docs=silent)
    if not rows:
        sys.stderr.write("no open-questions document found under %s\n" % ROOT)
        return 2
    text = render(rows, silent)
    if "--write" in argv:
        open(os.path.join(ROOT, "GAP_INDEX.md"), "w",
             encoding="utf-8").write(text)
        sys.stderr.write("wrote GAP_INDEX.md  (%d entries)\n" % len(rows))
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
