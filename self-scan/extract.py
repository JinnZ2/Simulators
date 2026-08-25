#!/usr/bin/env python3
"""S1 and S2 -- section CLAUDE.md, classify each section's stance, and
pull the checkable claims out of it.

WO10 points scan 4 at this repository's own documentation. A workbook
states a relationship in a prose cell and a formula either maintains it
or does not; CLAUDE.md states a relationship between a sentence and an
artifact, and a test either asserts it or does not. Same question, and
the target is prose all the way down, so extraction is where the whole
run can go wrong.

Two decisions, stated because both could have gone the other way:

EXTRACTION IS PROGRAMMATIC. Every claim below is found by pattern over
the file, never typed out by hand. A hand-listed claim set would be
selected by whoever read the file, which on this target is the same
party that wrote it.

BINDING IS DECLARED. Which artifact a claim is about is NOT inferred.
"247 selftest checks green across nine modules" names its folder in the
surrounding prose, and mapping that prose to a path is a judgement --
the same refusal `fold-matrix` FM_013 makes on `computed` and
`generation-capacity` GC_003 wanted on its denominator. An unbound
claim is reported as unbound, which is a state and not a pass.

The stance test is IMPORTED from sheet-structure-scan/selection.py
rather than reimplemented, so the screen and this scan cannot disagree
about what RETROSPECTIVE means.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import selection  # noqa: E402

RETROSPECTIVE = selection.RETROSPECTIVE
PROSPECTIVE = selection.PROSPECTIVE
NEITHER = selection.NEITHER

TARGET = os.path.join(ROOT, "CLAUDE.md")

COUNT = "COUNT"
IDENTITY = "IDENTITY"
NUMERIC = "NUMERIC"
KINDS = (COUNT, IDENTITY, NUMERIC)


# ---------------------------------------------------------------- sections

def sections(text):
    """(id, title, start_line, end_line, body) over CLAUDE.md.

    Two nesting levels are real in this file: `## ` headings, and inside
    `## Layout` a bullet list where each `- \\`name/\\`` item is one
    folder's whole description. The bullet is the useful unit -- a claim
    belongs to a folder, not to `## Layout` -- so a Layout bullet is a
    section and the heading is not.
    """
    lines = text.split("\n")
    marks = []
    for i, ln in enumerate(lines):
        if ln.startswith("## "):
            marks.append((i, "heading", ln[3:].strip()))
        elif re.match(r"^- `[^`]+`", ln):
            marks.append((i, "bullet", re.match(r"^- `([^`]+)`", ln).group(1)))
    out = []
    for n, (i, kind, title) in enumerate(marks):
        end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
        body = "\n".join(lines[i:end])
        out.append({
            "id": "%s:%s" % (kind, title),
            "kind": kind,
            "title": title,
            "start_line": i + 1,
            "end_line": end,
            "body": body,
        })
    return out


def stance(sec):
    """RETROSPECTIVE / PROSPECTIVE / NEITHER, by the imported test."""
    return selection.classify_stance(sec["body"])


# ---- WO10 S1 names three kinds of PROSPECTIVE section explicitly.
# The imported marker test reads a sentence; these read a section's job.
# Both are applied and both are reported, because they can disagree and
# that disagreement is information about the test rather than noise.
_ROADMAP_RE = [
    re.compile(p, re.I) for p in (
        r"\bwhat comes next\b",
        r"\broadmap\b",
        r"\bproposal\.md\b",
        r"\bavenues for taking\b",
        r"\bnot commitments; specifications\b",
    )
]


def roadmap_markers(sec):
    return [p.pattern for p in _ROADMAP_RE if p.search(sec["body"])]


# ---------------------------------------------------------------- claims

# Each pattern yields (kind, value, matched_text). `value` is what a
# resolution has to reproduce; `None` where the claim is an identity and
# there is no number.
_PATTERNS = [
    # ---- COUNT
    (COUNT, "tests_green",
     re.compile(r"\b(\d+)(\+?)\s+(?:audit-grade\s+|selftest\s+)?"
                r"(?:tests?|checks?)\s+(?:green|pass\b)", re.I)),
    (COUNT, "selftest_ratio",
     re.compile(r"selftest\s+(\d+)\s*/\s*(\d+)", re.I)),
    (COUNT, "pass_skip",
     re.compile(r"\b(\d+)\s+pass,\s*(\d+)\s+skip", re.I)),
    (COUNT, "files_total",
     re.compile(r"\b(\d+)\s+files?\s+total\b", re.I)),
    (COUNT, "selftest_checks",
     re.compile(r"\b(\d+)\s+selftest\s+checks?\b", re.I)),
    # ---- IDENTITY
    (IDENTITY, "byte_identical",
     re.compile(r"byte-identical", re.I)),
    (IDENTITY, "byte_reproducible",
     re.compile(r"byte-reproducibl[ey]", re.I)),
    (IDENTITY, "regenerates_identically",
     re.compile(r"regenerates?\s+byte-identically", re.I)),
]


def claims(text=None, secs=None):
    """Every pattern hit, tagged with the section it fell in."""
    if text is None:
        text = open(TARGET, encoding="utf-8").read()
    if secs is None:
        secs = sections(text)
    # line number for a character offset
    starts = [0]
    for ln in text.split("\n"):
        starts.append(starts[-1] + len(ln) + 1)

    def line_of(pos):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    spans = code_spans(text)
    out = []
    for kind, name, rx in _PATTERNS:
        for m in rx.finditer(text):
            ln = line_of(m.start())
            sec = None
            for s in secs:
                if s["start_line"] <= ln <= s["end_line"]:
                    sec = s
            groups = [g for g in m.groups() if g is not None]
            # "430+ tests green" is a LOWER BOUND, not a count. A bound
            # can only be contradicted from one side, and reporting it
            # as a count would make every folder that grew read as
            # differing.
            bound = "+" in groups
            groups = [g for g in groups if g not in ("", "+")]
            out.append({
                "kind": kind,
                "pattern": name,
                "bound": bound,
                "quoted": in_code_span(spans, m.start(), m.end()),
                "span": (m.start(), m.end()),
                "value": groups if groups else None,
                "text": m.group(0),
                "line": ln,
                "section": sec["id"] if sec else "NO_SECTION",
                "section_title": sec["title"] if sec else "NO_SECTION",
                "context": _context(text, m.start(), m.end()),
            })
    return _dedupe(out)


def _dedupe(rows):
    """Two patterns can match the same words -- `197 selftest checks`
    and `197 selftest checks green` are one claim seen twice. Keep the
    longer span; a shorter match inside a longer one is the same
    statement read less completely.
    """
    rows = sorted(rows, key=lambda r: (r["span"][0],
                                       -(r["span"][1] - r["span"][0])))
    kept = []
    for r in rows:
        a, b = r["span"]
        if any(x[0] <= a and b <= x[1] for x in
               [k["span"] for k in kept]):
            continue
        kept.append(r)
    kept.sort(key=lambda r: (r["line"], r["pattern"]))
    return kept


# ---- handoff item 3: quoted context ---------------------------------
#
# `CLAUDE.md` quotes other folders' claims constantly -- it is an index
# whose subject is other folders' claims -- so a pattern that matches
# text matches a claim under discussion exactly as readily as one being
# made. SS_016 recorded that after it happened.
#
# The test is STRUCTURAL, not semantic. Markdown puts a quoted claim in
# a code span and an asserted one in running prose, and that is a
# property of the markup rather than a guess about attribution. It is
# reported as a FLAG, never used to exclude: a flagged claim must be
# declared in bindings.py, which is where attribution decisions live.
#
# Both directions matter and the file supplies both:
#   line 236   430+ audit-grade tests green.        asserted, bare
#   line 6665  `430+\n  audit-grade tests green`    quoted, in a span


def code_spans(text):
    """(start, end) of every inline code span and fenced block.

    Fences first, so a backtick inside a fence does not open a span.
    Single-backtick spans may wrap a line, which is how this file's own
    quoted claim is written, so newlines are allowed inside one.
    """
    spans = []
    i = 0
    while True:
        f = text.find("```", i)
        if f < 0:
            break
        g = text.find("```", f + 3)
        if g < 0:
            spans.append((f, len(text)))
            break
        spans.append((f, g + 3))
        i = g + 3
    fenced = list(spans)

    def in_fence(pos):
        return any(a <= pos < b for a, b in fenced)

    i = 0
    while i < len(text):
        a = text.find("`", i)
        if a < 0:
            break
        if in_fence(a):
            i = a + 1
            continue
        b = text.find("`", a + 1)
        if b < 0:
            break
        if in_fence(b):
            i = b + 1
            continue
        spans.append((a, b + 1))
        i = b + 1
    return sorted(spans)


def in_code_span(spans, a, b):
    """Is the match wholly inside a code span?"""
    return any(s <= a and b <= e for s, e in spans)


def _context(text, a, b, width=180):
    lo = max(0, a - width)
    hi = min(len(text), b + width)
    return " ".join(text[lo:hi].split())


# ------------------------------------------------------- non-checkable

_SENT_RE = re.compile(r"(?<=[.!?])\s+")


def prose_census(text, cl):
    """Sentences in the file, and how many carry a claim we extract.

    WO10 S2 says non-checkable prose is counted, not tested. Counting it
    is the denominator that keeps the extracted set from reading as the
    file's whole content.
    """
    lines = text.split("\n")
    hit_lines = {c["line"] for c in cl}
    sents = [s for s in _SENT_RE.split(text) if len(s.strip()) > 25]
    return {
        "lines": len(lines),
        "chars": len(text),
        "sentences_over_25_chars": len(sents),
        "lines_carrying_an_extracted_claim": len(hit_lines),
    }


# -------------------------------------------------------------- selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- sectioning, on a known answer built here
    t = ("# T\n"
         "## Layout\n"
         "- `a/` - alpha. 3 tests green.\n"
         "  more alpha, selftest 4/4.\n"
         "- `b/` - beta, byte-identical.\n"
         "## After\n"
         "tail 9 tests green.\n")
    secs = sections(t)
    ids = [s["id"] for s in secs]
    chk("sections finds both headings and bullets",
        ids == ["heading:Layout", "bullet:a/", "bullet:b/", "heading:After"])
    # end_line is the LAST line of the section, not the first line of
    # the next one. Written the other way first and the test caught it.
    chk("a bullet section ends on its own last line",
        [s for s in secs if s["id"] == "bullet:a/"][0]["end_line"] == 4)
    chk("a bullet section keeps its continuation lines",
        "selftest 4/4" in [s for s in secs
                           if s["id"] == "bullet:a/"][0]["body"])

    cl = claims(t, secs)
    got = sorted((c["pattern"], c["section"]) for c in cl)
    chk("claims are attributed to the bullet, not to the heading",
        ("tests_green", "bullet:a/") in got)
    chk("a claim after the last bullet lands in the following heading",
        ("tests_green", "heading:After") in got)
    chk("selftest ratio is extracted", ("selftest_ratio", "bullet:a/") in got)
    chk("byte-identical is extracted",
        ("byte_identical", "bullet:b/") in got)

    # -- values
    v = {c["pattern"]: c["value"] for c in cl}
    chk("count value is captured", v["tests_green"] == ["3"]
        or v["tests_green"] == ["9"])
    chk("ratio captures both sides", v["selftest_ratio"] == ["4", "4"])
    chk("an identity claim carries no value",
        v["byte_identical"] is None)

    # -- overlapping matches collapse to the longer one
    t3 = "the folder has 197 selftest checks green today.\n"
    d = claims(t3, sections(t3))
    chk("overlapping patterns collapse to one claim", len(d) == 1)
    chk("the survivor is the longer match",
        d[0]["pattern"] == "tests_green")

    # -- N+ is a bound, not a count
    t4 = "430+ audit-grade tests green here. 12 tests green there.\n"
    b = {c["value"][0]: c["bound"] for c in claims(t4, sections(t4))}
    chk("N+ is marked a bound", b["430"] is True)
    chk("a plain N is not a bound", b["12"] is False)

    # -- quoted context, both directions, on the real file's own pair
    if os.path.exists(TARGET):
        rt = open(TARGET, encoding="utf-8").read()
        rc = claims(rt)
        q = [c for c in rc if c.get("quoted")]
        nq = [c for c in rc if not c.get("quoted")]
        chk("at least one real claim is inside a code span", bool(q))
        chk("most real claims are not", len(nq) > len(q))
        four30 = [c for c in rc if c["value"] and c["value"][0] == "430"]
        chk("the file carries the same claim quoted and bare",
            len(four30) == 2)
        chk("the quoted one is flagged and the bare one is not",
            len(four30) == 2
            and sorted(bool(c["quoted"]) for c in four30) == [False, True])

    # -- code_spans on known answers
    t5 = "a `b c` d ``` e `f` ``` g `h`\n"
    sp = code_spans(t5)
    chk("a fence swallows the backticks inside it",
        any(t5[a:b].startswith("```") for a, b in sp))
    chk("in_code_span is true inside a span",
        in_code_span(sp, t5.index("b c"), t5.index("b c") + 3))
    chk("in_code_span is false in running prose",
        not in_code_span(sp, t5.index(" d "), t5.index(" d ") + 2))
    t6 = "x `wrapped\nover a line` y\n"
    chk("a span may wrap a line",
        in_code_span(code_spans(t6), t6.index("wrapped"),
                     t6.index("line") + 4))

    # -- the patterns must not fire on ordinary prose
    quiet = "The folder holds nine modules and reads a workbook.\n"
    chk("no claim in prose with no claim in it", claims(quiet, sections(quiet))
        == [])

    # -- `40 pass, 2 skip` and `15 files total`
    t2 = "x 40 pass, 2 skip y. 15 files total in z.\n"
    p2 = {c["pattern"]: c["value"] for c in claims(t2, sections(t2))}
    chk("pass_skip captures both", p2.get("pass_skip") == ["40", "2"])
    chk("files_total captures one", p2.get("files_total") == ["15"])

    # -- stance is the imported test, not a local copy
    chk("stance test is imported",
        stance.__module__ == __name__
        and selection.classify_stance("Average of A and B.")
        == RETROSPECTIVE)
    chk("a prospective sentence classifies prospective",
        selection.classify_stance("Enter the total here.") == PROSPECTIVE)

    # -- roadmap markers are a separate reading, not folded in
    sec = {"body": "ten avenues for taking the framework, what comes next."}
    chk("roadmap markers fire on a roadmap section",
        len(roadmap_markers(sec)) == 2)
    chk("roadmap markers are quiet otherwise",
        roadmap_markers({"body": "the scan returns four bins."}) == [])

    # -- the real file
    if os.path.exists(TARGET):
        text = open(TARGET, encoding="utf-8").read()
        real = claims(text)
        chk("the real target yields claims", len(real) > 20)
        chk("every real claim has a section",
            all(c["section"] != "NO_SECTION" for c in real))
        chk("every real claim has a kind in KINDS",
            all(c["kind"] in KINDS for c in real))
        cen = prose_census(text, real)
        chk("census counts more lines than claim lines",
            cen["lines"] > cen["lines_carrying_an_extracted_claim"])

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    text = open(TARGET, encoding="utf-8").read()
    secs = sections(text)
    cl = claims(text, secs)
    if "--sections" in argv:
        print("%-46s %-6s %-15s %s" % ("section", "lines", "stance",
                                       "roadmap markers"))
        print("-" * 92)
        for s in secs:
            print("%-46s %-6s %-15s %s"
                  % (s["id"][:46], s["end_line"] - s["start_line"] + 1,
                     stance(s), len(roadmap_markers(s))))
        return 0
    print("%-6s %-9s %-22s %-30s %s"
          % ("line", "kind", "pattern", "section", "text"))
    print("-" * 100)
    for c in cl:
        print("%-6d %-9s %-22s %-30s %s"
              % (c["line"], c["kind"], c["pattern"],
                 c["section_title"][:30], c["text"][:28]))
    print("")
    print("claims: %d" % len(cl))
    cen = prose_census(text, cl)
    for k in sorted(cen):
        print("  %-38s %d" % (k, cen[k]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
