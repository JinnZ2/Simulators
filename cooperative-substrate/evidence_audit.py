#!/usr/bin/env python3
"""Reads EVIDENCE_PACK.md as a structure: every table row parsed, every
locator classified by syntax, every status mark counted, the arXiv
identifiers checked against the calendar, the DOI-embedded years
against the stated ones, and the pack's claims mapped onto artifacts
already in this tree. Opens no paper: every citation host refuses
CONNECT from here (probed once, recorded below). Nothing here is a
statement about any finding the pack carries.

    python3 evidence_audit.py
Refuses --selftest (checks live in selftest_evidence.py).
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
PACK = os.path.join(HERE, "EVIDENCE_PACK.md")

ROW = re.compile(r"^\| (E\d\.\d+) \| (.+?) \| (.+?) \| (.+?) \|$")
DOI = re.compile(r"\b10\.\d{4,9}/[^\s|)]+")
ARXIV = re.compile(r"\barXiv (\d{4})\.(\d{4,5})\b")
PMC = re.compile(r"\bPMC\d{6,8}\b")
URL = re.compile(r"\b[\w.-]+\.(?:net|org|com)/\S+")
PII = re.compile(r"\bS\d{16}\b")
YEAR = re.compile(r"\b(?:19|20)\d\d[a-z]?\b")
TODAY = (2026, 9)
HOST_PROBE = {"doi.org": "000 (no response)", "arxiv.org": "000 (no response)", "www.nature.com": "000 (no response)",
              "probed": "2026-09-04T17:37Z, one CONNECT each"}

# Declared cross-links: pack item -> artifact in this tree, with the
# relation stated. Existence is checked; the relation is a reading.
CROSS_LINKS = [
    ("E2.6", "label-position-test", "the pack states as a measurement (100% / 0%, transcript fixed) what "
     "LPT_009 holds UNVERIFIED: valence tracks position, not content; the pack cites no record for it"),
    ("E2.6", "report-typing", "same mechanism, routing by position; the marker's reverse arm is the blind form"),
    ("E2.1", "cooperative-substrate/WORK_ORDER.md", "the one-scale-up note, here with three sub-claims and no locator"),
    ("E4", "nonidentity-census", "selection history not held constant is the unmatched-pair shape (T6-3)"),
    ("E4", "shape-spec-audit", "SS_003: a second variable moved with the named one"),
    ("E7:3", "declared-frame", "the accounting boundary as a declared field"),
    ("E7:5", "extraction-blindness-sim", "an accounting stance that degrades the measurement it reads"),
    ("E3 recording-rate", "observer-exclusion", "recording rate as a censoring process, OE_002-OE_004"),
    ("E8 C1", "nonidentity-census", "window short vs coupling-formation rate is the G-RES pair T2-5 names"),
]


def parse(text=None):
    text = text if text is not None else open(PACK, encoding="utf-8").read()
    rows = []
    for line in text.splitlines():
        m = ROW.match(line)
        if m:
            rows.append({"id": m.group(1), "finding": m.group(2), "source": m.group(3), "status": m.group(4)})
    targets = re.findall(r"^- \"(.+?)\" — \*Nat Comms\* (10\.\d{4}/\S+)$", text, re.M)
    return rows, targets


def locator(source):
    if DOI.search(source):
        return "doi"
    if ARXIV.search(source):
        return "arxiv"
    if PMC.search(source):
        return "pmc"
    if URL.search(source):
        return "url"
    if PII.search(source):
        return "pii"
    if YEAR.search(source):
        return "author_year"
    return "name_only"


def census(rows):
    by_loc, by_status = {}, {}
    for r in rows:
        by_loc[locator(r["source"])] = by_loc.get(locator(r["source"]), 0) + 1
        st = "DISPUTED" if "DISPUTED" in r["status"] else ("UNVERIFIED-FULLTEXT" if "UNVERIFIED" in r["status"] else "OTHER")
        by_status[st] = by_status.get(st, 0) + 1
    sections = {}
    for r in rows:
        sections[r["id"].split(".")[0]] = sections.get(r["id"].split(".")[0], 0) + 1
    return {"rows": len(rows), "by_locator": by_loc, "by_status": by_status, "by_section": sections,
            "name_only_or_author_year": [r["id"] for r in rows if locator(r["source"]) in ("name_only", "author_year")]}


def arxiv_calendar(rows):
    out = []
    for r in rows:
        for yymm, num in ARXIV.findall(r["source"]):
            y, m = 2000 + int(yymm[:2]), int(yymm[2:])
            out.append({"id": r["id"], "arxiv": "%s.%s" % (yymm, num), "year_month": (y, m),
                        "month_valid": 1 <= m <= 12, "not_in_future": (y, m) <= TODAY})
    return out


def doi_years(rows, targets):
    """Nature Communications DOIs carry the year: s41467-YYY-NNNNN. Read
    against any year the same source states."""
    out = []
    srcs = [(r["id"], r["source"]) for r in rows] + [("E4 target", t[1]) for t in targets]
    for rid, src in srcs:
        for m in re.finditer(r"s41467-0(\d\d)-\d+", src):
            embedded = 2000 + int(m.group(1))
            stated = [int(y[:4]) for y in YEAR.findall(src)]
            out.append({"id": rid, "embedded_year": embedded, "stated_years": stated,
                        "consistent": (not stated) or embedded in stated})
    return out


def doi_syntax(rows, targets):
    dois = [d for r in rows for d in DOI.findall(r["source"])] + [t[1] for t in targets]
    return {"count": len(dois), "distinct": len(set(dois)), "duplicates": sorted({d for d in dois if dois.count(d) > 1}),
            "all_well_formed": all(re.fullmatch(r"10\.\d{4,9}/\S+", d) for d in dois)}


def cross_links():
    out = []
    for item, target, relation in CROSS_LINKS:
        path = os.path.join(ROOT, target)
        out.append({"item": item, "target": target, "exists": os.path.exists(path), "relation": relation})
    return out


def e33_vs_table(text=None):
    """E3.3 says competitive goal structure in games is a VARIABLE; the
    E8 table scores 'Austronesian games' all-y as a class. Both quoted."""
    text = text if text is not None else open(PACK, encoding="utf-8").read()
    e33 = "measured cross-cultural **variable**, not a constant" in text
    row = re.search(r"^Austronesian games\s+C1 y\s+C2 y\s+C3 y\s+C4 y", text, re.M) is not None
    return {"e33_says_variable": e33, "e8_scores_class_all_y": row, "both_present": e33 and row}


def render():
    rows, targets = parse()
    c = census(rows)
    L = ["evidence pack audit: %d table rows + %d target papers" % (len(rows), len(targets))]
    L.append("by section %s" % c["by_section"])
    L.append("by status  %s" % c["by_status"])
    L.append("by locator %s" % c["by_locator"])
    L.append("no locator beyond author/year or name: %s" % c["name_only_or_author_year"])
    d = doi_syntax(rows, targets)
    L.append("DOIs: %d, distinct %d, duplicates %s, all well-formed %s" % (d["count"], d["distinct"], d["duplicates"], d["all_well_formed"]))
    for a in arxiv_calendar(rows):
        L.append("  arXiv %s (%s) %d-%02d month_valid %s not_in_future %s" % (a["arxiv"], a["id"], a["year_month"][0], a["year_month"][1], a["month_valid"], a["not_in_future"]))
    for y in doi_years(rows, targets):
        L.append("  %-10s Nat Comms DOI year %d stated %s consistent %s" % (y["id"], y["embedded_year"], y["stated_years"], y["consistent"]))
    L.append("hosts: %s" % HOST_PROBE)
    L.append("E3.3 against the E8 row: %s" % e33_vs_table())
    L.append("cross-links into this tree:")
    for x in cross_links():
        L.append("  %-16s -> %-36s exists %-5s %s" % (x["item"], x["target"], x["exists"], x["relation"]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        print("evidence_audit has no selftest; run selftest_evidence.py", file=sys.stderr)
        sys.exit(2)
    print(render())
