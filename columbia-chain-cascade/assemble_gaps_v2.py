#!/usr/bin/env python3
# assemble_gaps_v2.py -- CC0, stdlib only, parses under 3.9
#
# Generates UNDERGRADUATE_RESEARCH_GAPS_V2.md from three delivered inputs
# and one registry, deterministically:
#   v1   UNDERGRADUATE_RESEARCH_GAPS.md   (verbatim, byte-preserved)
#   14   GAP_14_mining_hydrology.md        (slotted in as "## 14.")
#   15   GAP_15_bridge_impoundment.md      (slotted in as "## 15.")
#   +    gap_addenda.json                  (tiers, routes, known answer,
#                                           consent step, schema pointer)
# Every addendum block and each slotted entry is fenced with a marker
# so a reader can strip them: stripping every ADDENDUM and SLOTTED block
# from V2 returns v1 byte-for-byte. The generator is the
# provenance; v1 is not edited.

import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OPEN = "<!-- ADDENDUM"
CLOSE = "<!-- /ADDENDUM -->"


def _read(n):
    return io.open(os.path.join(HERE, n), encoding="utf-8").read()


def _block(kind, body):
    return "%s %s -->\n%s\n%s\n" % (OPEN, kind, body.rstrip("\n"), CLOSE)


def _tier_block(entry):
    lines = ["**Access tiers (addendum — carried, not probed; a tier is a "
             "label, never a wall):**", ""]
    for t in entry["tiers"]:
        lines.append("- %s — **%s**; route: %s"
                     % (t["source"], t["tier"], t["route"]))
    return "\n".join(lines)


def _card_as_entry(num, text):
    """The card's '# GAP N — TITLE' becomes '## N. TITLE'; the draft
    line is dropped, since the entry is no longer a draft once slotted.
    Everything else is verbatim."""
    lines = text.splitlines()
    m = re.match(r"# GAP %d — (.+)$" % num, lines[0])
    assert m, lines[0]
    head = "## %d. %s" % (num, m.group(1))
    body = lines[1:]
    if body and body[0].strip() == "":
        body = body[1:]
    if body and body[0].startswith("*Draft entry for"):
        body = body[1:]
    return head + "\n" + "\n".join(body).rstrip("\n") + "\n"


def assemble():
    v1 = _read("UNDERGRADUATE_RESEARCH_GAPS.md")
    ad = json.load(io.open(os.path.join(HERE, "gap_addenda.json"),
                           encoding="utf-8"))["gaps"]
    # split v1 into head, entries, tail ("## How to Use This Document")
    parts = re.split(r"(?m)^(## \d+\. .+)$", v1)
    head = parts[0]
    entries = []
    for i in range(1, len(parts), 2):
        entries.append((parts[i], parts[i + 1]))
    tail_idx = entries[-1][1].find("\n## How to Use")
    last_hdr, last_body = entries[-1]
    tail = last_body[tail_idx + 1:]
    entries[-1] = (last_hdr, last_body[:tail_idx + 1])

    out = [head]
    for hdr, body in entries:
        num = int(re.match(r"## (\d+)\.", hdr).group(1))
        out.append(hdr + _insert(body, ad[str(num)], num))
    for num, card in ((14, "GAP_14_mining_hydrology.md"),
                      (15, "GAP_15_bridge_impoundment.md")):
        text = _card_as_entry(num, _read(card))
        hdr, body = text.split("\n", 1)
        out.append("<!-- SLOTTED %d -->\n" % num + hdr + "\n"
                   + _insert(body, ad[str(num)], num)
                   + "\n---\n\n<!-- /SLOTTED %d -->\n" % num)
    out.append(tail)
    return "".join(out)


def _insert(body, entry, num):
    """Insert the addendum blocks after the Data sources list, after
    the Method header (consent step, gap 3), after the Method list
    (known answer), and after the deliverable (schema pointer)."""
    # after the data-sources bullets: the tier block
    m = re.search(r"\*\*Data sources:\*\*\n(?:- .*\n|  .*\n)+", body)
    assert m, num
    body = body[:m.end()] + "\n" + _block("tiers", _tier_block(entry)) \
        + body[m.end():]
    # gap 3: consent step directly after the Method header
    if "consent_step" in entry:
        m = re.search(r"\*\*Method:\*\*\n", body)
        body = body[:m.end()] + _block("consent",
                                       entry["consent_step"]) + "\n" \
            + body[m.end():]
    # known-answer after the method list (before Expected deliverable)
    m = re.search(r"\*\*Expected deliverable:\*\*", body)
    assert m, num
    ka = _block("known-answer", "**Known-answer step (addendum):** "
                + entry["known_answer"])
    body = body[:m.start()] + ka + "\n" + body[m.start():]
    # schema pointer after the deliverable paragraph
    if "deliverable_schema" in entry:
        m = re.search(r"\*\*Expected deliverable:\*\*.*?\n\n", body, re.S)
        sc = _block("schema", "**Deliverable schema (addendum):** "
                    + entry["deliverable_schema"])
        body = body[:m.end()] + sc + "\n" + body[m.end():]
    return body


def strip_addenda(text):
    """Remove every ADDENDUM block (and the blank line it added), and
    the two slotted entries. Used to show V2 minus the additions is v1."""
    text = re.sub(r"\n?<!-- ADDENDUM .*? -->\n.*?<!-- /ADDENDUM -->\n",
                  "", text, flags=re.S)
    text = re.sub(r"<!-- SLOTTED \d+ -->\n.*?<!-- /SLOTTED \d+ -->\n", "",
                  text, flags=re.S)
    return text


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write("assemble_gaps_v2.py has no checks of its own; they live "
                         "in selftest_kill.py.\n")
        sys.exit(2)
    v2 = assemble()
    p = os.path.join(HERE, "UNDERGRADUATE_RESEARCH_GAPS_V2.md")
    io.open(p, "w", encoding="utf-8").write(v2)
    v1 = _read("UNDERGRADUATE_RESEARCH_GAPS.md")
    same = strip_addenda(v2) == v1
    print("V2 written: %d lines; strip(V2) == v1: %s; entries: %d"
          % (v2.count("\n"), same,
             len(re.findall(r"(?m)^## \d+\. ", v2))))
    if not same:
        sys.exit(1)
