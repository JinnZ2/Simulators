#!/usr/bin/env python3
"""Checks on SOURCE_DROP.md (Habitat Loss, Lag, and AI Dependency).

Reads the delivered document. Never edits it. Reports three things:

  1. Tag census: per section, how many claim lines carry one of the four
     declared status tags (OBSERVED / DERIVED / PROPOSED / GAP) and which
     lines carry none.
  2. Tag consistency: the two figures the document itself marks "verify"
     are tagged two different ways.
  3. Arithmetic on the figures this audit checked against a source, so
     the document's wording can be compared with what the source counts.

What it does NOT do: verify anything. Every source fact below is carried
from search-result text (see SOURCES.md), not from a primary document.

    python3 check.py              render the report
    python3 check.py --selftest   run the checks
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOC = HERE / "SOURCE_DROP.md"
PINNED_SHA256 = "3861c9faf2d1fc92a1a15dbd1f34aabdec11a83a32548927497eb0ec2debbf0c"
TAGS = ("OBSERVED", "DERIVED", "PROPOSED", "GAP")


def text():
    return DOC.read_text(encoding="utf-8")


def sha():
    return hashlib.sha256(DOC.read_bytes()).hexdigest()


def declared_tags(t):
    """The tag vocabulary as the header states it, read from the text."""
    m = re.search(r"Status tags:(.*?)\n", t)
    return tuple(re.findall(r"\b([A-Z]{3,})\b \(", m.group(1))) if m else ()


def sections(t):
    """[(heading, [lines])] for every '## ' section."""
    out, cur = [], None
    for line in t.splitlines():
        if line.startswith("## "):
            cur = (line[3:].strip(), [])
            out.append(cur)
        elif cur is not None:
            cur[1].append(line)
    return out


def claim_lines(lines):
    """Bullets, table body rows and bold-led paragraphs. Not headers, blanks,
    the table header row or its separator."""
    out = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("|"):
            if set(s) <= set("|- ") or s.startswith("| Source"):
                continue
            out.append(s)
        elif s.startswith("- ") or s.startswith("**") or re.match(r"\d+\. ", s):
            out.append(s)
        else:
            out.append(s)
    return out


def tag_of(line):
    """Leading tag only: a tag word inside the sentence is not a status."""
    body = re.sub(r"^(- |\d+\. )", "", line)
    for tg in TAGS:
        if body.startswith(tg):
            return tg
    return None


def census(t):
    rows = []
    for head, lines in sections(t):
        cl = claim_lines(lines)
        tagged = [c for c in cl if tag_of(c)]
        rows.append((head, len(cl), len(tagged), [c for c in cl if not tag_of(c)]))
    return rows


def verify_marked(t):
    """Lines the document itself flags for verification, with the tag each carries."""
    out = []
    for ln in t.splitlines():
        s = ln.strip()
        if re.search(r"\bverify\b", s, re.I) and s.startswith("- ") and tag_of(s):
            out.append((tag_of(s), s))
    return out


# Figures carried from search-result text (SOURCES.md). Not primary reads.
GAO_1994 = {"listed": 781, "some_nonfederal": 712, "over_60pct_nonfederal": 516}
MORA_2011 = {"eukaryotes_million": 8.7, "land_undescribed": 0.86, "ocean_undescribed": 0.91}


def gao_shares():
    g = GAO_1994
    return (g["some_nonfederal"] / g["listed"], g["over_60pct_nonfederal"] / g["listed"])


def render():
    t = text()
    out = ["habitat-lag-dependency / check.py", "=" * 60,
           f"SOURCE_DROP.md sha256 {sha()[:16]}...  pinned: {sha() == PINNED_SHA256}",
           f"declared tags: {', '.join(declared_tags(t))}", "",
           "1. TAG CENSUS (leading tag only)",
           f"{'section':<42} {'lines':>5} {'tagged':>6}"]
    total = tagged_total = 0
    for head, n, k, untagged in census(t):
        total += n
        tagged_total += k
        out.append(f"{head[:42]:<42} {n:>5} {k:>6}")
    out.append(f"{'TOTAL':<42} {total:>5} {tagged_total:>6}")
    out += ["", "   sections with no tagged line at all:"]
    for head, n, k, _ in census(t):
        if n and not k:
            out.append(f"     - {head}  ({n} lines)")
    out += ["", "2. LINES THE DOCUMENT MARKS 'verify', AND THEIR TAG"]
    for tg, s in verify_marked(t):
        out.append(f"   {tg:<9} {s[:72]}")
    out.append("   -> two unchecked general-knowledge figures, two different tags")
    a, b = gao_shares()
    out += ["", "3. ARITHMETIC ON CHECKED FIGURES (search-result depth)",
            f"   GAO/RCED-95-16 (1994): {GAO_1994['some_nonfederal']}/{GAO_1994['listed']}"
            f" = {a:.3f} have SOME habitat on nonfederal land",
            f"                          {GAO_1994['over_60pct_nonfederal']}/{GAO_1994['listed']}"
            f" = {b:.3f} have OVER 60% of habitat on nonfederal land",
            "   document: 'more than two-thirds ... at least some habitat on private land'",
            "   -> 'two-thirds' matches the >60%-of-habitat row, not the 'some' row;",
            "      that row is 0.661, just UNDER two-thirds, so 'more than' fails on it too;",
            "      and GAO counts NONFEDERAL (state, tribal, private), not private alone.",
            "", "Nothing above is a statement about any species, parcel or rule's effect."]
    return "\n".join(out)


def selftest():
    t = text()
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    ok("document unedited (sha pinned)", sha() == PINNED_SHA256)
    ok("declared tags read from header == TAGS", declared_tags(t) == TAGS)
    secs = [h for h, _ in sections(t)]
    ok("nine sections parsed (Purpose + 1..8)", len(secs) == 9)
    cen = {h: (n, k) for h, n, k, _ in census(t)}
    ok("section 6 carries no tagged line", cen["6. What we're losing"][1] == 0)
    ok("section 8 carries no tagged line", cen["8. Related records"][1] == 0)
    ok("section 1 fully tagged", cen["1. Regulatory change"][0] == cen["1. Regulatory change"][1])
    vm = verify_marked(t)
    ok("two verify-marked tagged lines", len(vm) == 2)
    ok("verify-marked lines carry two different tags", len({tg for tg, _ in vm}) == 2)
    ok("tag_of reads leading tag only", tag_of("- this is OBSERVED later") is None
       and tag_of("- GAP: x") == "GAP")
    a, b = gao_shares()
    ok("GAO some-habitat share > 0.9", a > 0.9)
    ok("GAO >60% share is about two-thirds", abs(b - 2 / 3) < 0.01)
    ok("two-thirds sits nearer the >60% row than the some row", abs(b - 2 / 3) < abs(a - 2 / 3))
    ok("GAO >60% share is BELOW two-thirds", b < 2 / 3)
    failed = [n for n, c in checks if not c]
    for n, c in checks:
        print(("PASS " if c else "FAIL ") + n)
    print(f"checks: {len(checks)}   failed: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    print(render())
