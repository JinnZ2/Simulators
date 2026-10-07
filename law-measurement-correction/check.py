#!/usr/bin/env python3
# check.py -- CC0, stdlib only, parses under 3.9, no network.
#
# Reads the seven records in this folder back and checks what is checkable
# about them. It edits none of them and adjudicates no claim in the report.
#
#   1  notice    the correction notice carries sections A..G in order, and
#                the provenance block, as dispatched
#   2  states    every CC-3 row carries exactly one of VERIFIED /
#                CONTRADICTED / NOT_FOUND, and the counts line matches
#   3  absence   each NAMED-AND-ABSENT name resolves to no PATH in the tree.
#                Never by grep: a text search finds this folder's own records
#                that name them (the UNI_010 / QA_007 loop)
#   4  ledger    column A SETTLED with its unit, the liquid-mass field
#                UNFILLED, columns B and E/F NOT_EVALUABLE
#   5  design    REFUSED is one of four coded cells, and the key-holder rule
#                is stated
#   6  cc3b      the CC-3b table: 8 rows, one of four primary states each,
#                prior_A and prior_B columns carried, counts line matches,
#                and no row VERIFIED/CONTRADICTED while its host check
#                recorded OPEN 0
#   7  cc4       the merged CC-4: columns B..F a byte copy of pass 1's blob
#                (when the blob is reachable), paragraph letter UNCONFIRMED
#
# Bare run prints the readings. --selftest runs the readings plus planted
# violations that each check must catch, and prints `selftest: N/N passed`.

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NOTICE = "CORRECTION-law-as-unvalidated-measurement-2026-10-03.md"
VERIFY = "VERIFICATION_2026-10-04.md"
ABSENT = "NAMED_AND_ABSENT.md"
LEDGER = "DYED_FUEL_LEDGER_SETTLE.md"
DESIGN = "DESIGN_frame-substitution-eval.md"
CC3B = "CC3b_PRIMARY_RERUN_2026-10-04.md"
CC4M = "CC4_MERGED.md"
CC4_SOURCE_BLOB = "b22e599a1e3b4e04bd543f714b0bda7e1a670a79"

STATES = ("VERIFIED", "CONTRADICTED", "NOT_FOUND")
STATES_B = ("VERIFIED", "CONTRADICTED", "NOT_IN_PRIMARY", "PRIMARY_UNREACHABLE")
SECTIONS = ("A", "B", "C", "D", "E", "F", "G")
# path stems for the named-and-absent instruments
NAMES = {"why-recovery": ("why-recovery", "why_recovery", "whyrecovery"),
         "split-ledger / parks": ("split-ledger", "split_ledger", "parks")}


def read(name, folder=HERE):
    with open(os.path.join(folder, name), encoding="utf-8") as f:
        return f.read()


def check_notice(text):
    found = re.findall(r"^### ([A-G])\. ", text, re.M)
    return {"sections": found, "in_order": tuple(found) == SECTIONS,
            "provenance": "SOURCE ARTIFACT   OKComputer_Deep_Research_Idea_Exploration.zip" in text}


def table_rows(text):
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("| ") and len(cells) >= 5 and re.match(r"^\d+[a-z]?$", cells[0]):
            rows.append((cells[0], cells[2]))
    return rows


def check_states(text):
    rows = table_rows(text)
    bad = [(rid, st) for rid, st in rows if st not in STATES]
    counts = {s: sum(1 for _, st in rows if st == s) for s in STATES}
    m = re.search(r"VERIFIED (\d+)\s+CONTRADICTED (\d+)\s+NOT_FOUND (\d+)", text)
    stated = {"VERIFIED": int(m.group(1)), "CONTRADICTED": int(m.group(2)),
              "NOT_FOUND": int(m.group(3))} if m else None
    return {"rows": len(rows), "bad": bad, "counts": counts, "stated": stated,
            "counts_match": stated == counts}


def resolve_paths(stems, root=ROOT):
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for n in dirnames + filenames:
            base = os.path.splitext(n)[0].lower()
            if any(base == s or base.startswith(s + "_") or base.startswith(s + "-") or base.startswith(s + ".")
                   for s in stems):
                hits.append(os.path.relpath(os.path.join(dirpath, n), root))
    return hits


def check_absence(root=ROOT):
    return {name: ("RESOLVES " + ", ".join(h) if h else "ABSENT")
            for name, stems in NAMES.items() for h in [resolve_paths(stems, root)]}


def check_ledger(text):
    return {
        "A_settled": "SETTLED(" in text and "lb solid SR26-equivalent / 1,000 bbl" in text,
        "liquid_unfilled": "liquid_product_mass_per_1000_bbl:  UNFILLED" in text,
        "B_not_evaluable": bool(re.search(r"## Column B.*?NOT_EVALUABLE", text, re.S)),
        "EF_not_evaluable": bool(re.search(r"## Columns E and F.*?NOT_EVALUABLE", text, re.S)),
    }


def check_design(text):
    cells = re.findall(r"^    (PHYSICS|LAW-AS-PRIOR|MIXED|REFUSED)\s", text, re.M)
    return {"cells": cells, "four_cells": cells == ["PHYSICS", "LAW-AS-PRIOR", "MIXED", "REFUSED"],
            "key_holder": "does NOT write the expected answers or the coding" in text
                          and "REGRESSION" in text}


def check_cc3b(text):
    rows = []
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("| ") and len(cells) >= 8 and re.match(r"^\d+[a-z]?$", cells[0]):
            rows.append({"id": cells[0], "status": cells[4], "prior_A": cells[5], "prior_B": cells[6]})
    bad = [(r["id"], r["status"]) for r in rows if r["status"] not in STATES_B]
    counts = {st: sum(1 for r in rows if r["status"] == st) for st in STATES_B}
    m = re.search(r"CC-3b\s+VERIFIED (\d+)\s+CONTRADICTED (\d+)\s+NOT_IN_PRIMARY (\d+)\s+PRIMARY_UNREACHABLE (\d+)", text)
    stated = dict(zip(STATES_B, map(int, m.groups()))) if m else None
    hm = re.search(r"OPEN (\d+)\s+REFUSED (\d+)", text)
    open_hosts = int(hm.group(1)) if hm else None
    # a primary status needs an opened primary page; with OPEN 0 none can exist
    unearned = [r["id"] for r in rows if open_hosts == 0 and r["status"] in ("VERIFIED", "CONTRADICTED", "NOT_IN_PRIMARY")]
    priors = all(r["prior_A"] and r["prior_B"] for r in rows)
    return {"rows": len(rows), "ids": [r["id"] for r in rows], "bad": bad, "counts": counts,
            "stated": stated, "counts_match": stated == counts, "open_hosts": open_hosts,
            "unearned": unearned, "priors_carried": priors}


def git_blob(sha, root=ROOT):
    import subprocess
    try:
        return subprocess.run(["git", "-C", root, "cat-file", "-p", sha], capture_output=True,
                              text=True, check=True).stdout
    except Exception:
        return None


def check_cc4(text, source=None):
    # anchor at a line start: the provenance prose names the heading in quotes
    m = re.search(r"^## COLUMN B", text, re.M)
    copied = text[m.start():] if m else ""
    if source is None:
        byte_copy = "NOT_EVALUABLE (source blob not reachable)"
    else:
        n = re.search(r"^## COLUMN B", source, re.M)
        byte_copy = "IDENTICAL" if n and copied and source[n.start():] == copied else "DIFFERS"
    return {"byte_copy": byte_copy,
            "letter_unconfirmed": "Paragraph letter UNCONFIRMED" in text,
            "provenance": "session_01Y4zVdoRHPDHpVwSPbqbeLR" in text and CC4_SOURCE_BLOB in text}


def readings():
    return {"notice": check_notice(read(NOTICE)), "states": check_states(read(VERIFY)),
            "absence": check_absence(), "ledger": check_ledger(read(LEDGER)),
            "design": check_design(read(DESIGN)),
            "cc3b": check_cc3b(read(CC3B)),
            "cc4": check_cc4(read(CC4M), git_blob(CC4_SOURCE_BLOB))}


def render(r):
    out = ["law-measurement-correction: readings of the seven records (nothing edited)"]
    n = r["notice"]
    out.append("  1 notice   sections %s  in order %s  provenance %s"
               % ("".join(n["sections"]), n["in_order"], n["provenance"]))
    s = r["states"]
    out.append("  2 states   %d rows  out-of-vocabulary %s  counts %s  stated %s  match %s"
               % (s["rows"], s["bad"] or "none", s["counts"], s["stated"], s["counts_match"]))
    for name, st in r["absence"].items():
        out.append("  3 absence  %-22s %s" % (name, st))
    out.append("  4 ledger   %s" % r["ledger"])
    d = r["design"]
    out.append("  5 design   cells %s  key-holder rule %s" % (d["cells"], d["key_holder"]))
    b = r["cc3b"]
    out.append("  6 cc3b     %d rows %s  out-of-vocabulary %s  counts %s  match %s  hosts open %s  unearned %s  priors %s"
               % (b["rows"], ",".join(b["ids"]), b["bad"] or "none", b["counts"], b["counts_match"],
                  b["open_hosts"], b["unearned"] or "none", b["priors_carried"]))
    out.append("  7 cc4      %s" % r["cc4"])
    return "\n".join(out)


def selftest():
    import tempfile
    checks = []

    def ck(cond, msg):
        checks.append((bool(cond), msg))

    r = readings()
    ck(r["notice"]["in_order"] and r["notice"]["provenance"], "notice carries A..G in order and the provenance block")
    ck(not r["states"]["bad"] and r["states"]["rows"] > 0, "every CC-3 row carries one of the three states")
    ck(r["states"]["counts_match"], "the CC-3 counts line matches the rows")
    ck(all(v == "ABSENT" for v in r["absence"].values()), "both named instruments resolve to no path")
    ck(all(r["ledger"].values()), "ledger: A settled with unit, liquid field unfilled, B and E/F not evaluable")
    ck(r["design"]["four_cells"] and r["design"]["key_holder"], "design: four cells incl. REFUSED, key-holder rule stated")

    b = r["cc3b"]
    ck(b["rows"] == 8 and not b["bad"] and b["counts_match"], "CC-3b: 8 rows, four-state vocabulary, counts line matches")
    ck(b["priors_carried"] and not b["unearned"], "CC-3b: both prior columns carried, no primary status without an open host")
    ck(r["cc4"]["byte_copy"] in ("IDENTICAL",) or r["cc4"]["byte_copy"].startswith("NOT_EVALUABLE"),
       "CC-4 merged: adopted columns are a byte copy of pass 1 (or the blob is unreachable, said so)")
    ck(r["cc4"]["letter_unconfirmed"] and r["cc4"]["provenance"], "CC-4 merged: letter unconfirmed, provenance recorded")

    # planted violations: each check must fire on its own failure
    ck(not check_notice("### A. x\n### C. y\n")["in_order"], "a notice missing B is caught")
    planted = "| 1 | item | VERIFIED_ISH | u | l |\n| 2 | item | NOT_FOUND | — | q |\nVERIFIED 0   CONTRADICTED 0   NOT_FOUND 1\n"
    ps = check_states(planted)
    ck(ps["bad"] == [("1", "VERIFIED_ISH")], "a fourth state is caught as out of vocabulary")
    ck(check_states("| 1 | i | NOT_FOUND | — | q |\nVERIFIED 1   CONTRADICTED 0   NOT_FOUND 0\n")["counts_match"] is False,
       "a counts line that disagrees with the rows is caught")
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "why-recovery"))
        open(os.path.join(tmp, "parks.py"), "w").close()
        planted_abs = check_absence(tmp)
        ck(planted_abs["why-recovery"].startswith("RESOLVES"), "a planted why-recovery/ directory resolves")
        ck(planted_abs["split-ledger / parks"].startswith("RESOLVES"), "a planted parks.py resolves")
    with tempfile.TemporaryDirectory() as tmp:
        open(os.path.join(tmp, "notes_on_parks_and_why-recovery.md"), "w").close()
        ck(all(v == "ABSENT" for v in check_absence(tmp).values()),
           "a file that only MENTIONS the names does not resolve (a mention is not the instrument)")
        ck(resolve_paths(("why-recovery",), os.path.join(tmp, "nonexistent")) == [],
           "an empty tree resolves nothing (no default hit)")
    ck("pre-split" not in [s for stems in NAMES.values() for s in stems],
       "the move-set phrase 'pre-split ledgers' is not a path stem the absence check uses")
    ck(not check_ledger("SETTLED( lb solid SR26-equivalent / 1,000 bbl")["liquid_unfilled"],
       "a ledger record that fills nothing for the liquid field is caught")
    ck(not check_design("    PHYSICS a\n    LAW-AS-PRIOR b\n    MIXED c\n")["four_cells"],
       "a design dropping the REFUSED cell is caught")

    fake = ("OPEN 0   REFUSED 6\n| 1 | c | u | — | VERIFIED | VERIFIED | NOT_FOUND | n |\n"
            "    CC-3b   VERIFIED 1   CONTRADICTED 0   NOT_IN_PRIMARY 0   PRIMARY_UNREACHABLE 0\n")
    ck(check_cc3b(fake)["unearned"] == ["1"], "a VERIFIED row with no open host is caught as unearned")
    ck(check_cc3b(fake.replace("VERIFIED | VERIFIED", "NOT_FOUND | VERIFIED"))["bad"] == [("1", "NOT_FOUND")],
       "NOT_FOUND is not a CC-3b state (absence of a page is not absence in a page)")
    ck(check_cc4('names "## COLUMN B" in prose\n## COLUMN B\nx', source="## COLUMN B\nx")["byte_copy"] == "IDENTICAL",
       "a heading named in prose does not shift the compared span")
    ck(check_cc4("## COLUMN B\nx", source="## COLUMN B\ny")["byte_copy"] == "DIFFERS",
       "an adopted section that drifted from its source blob is caught")

    for ok, msg in checks:
        print("  %s  %s" % ("PASS" if ok else "FAIL", msg))
    n_ok = sum(ok for ok, _ in checks)
    print("selftest: %d/%d passed" % (n_ok, len(checks)))
    return 0 if n_ok == len(checks) else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    print(render(readings()))
    sys.exit(0)
