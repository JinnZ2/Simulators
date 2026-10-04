#!/usr/bin/env python3
# check.py -- CC0, stdlib only, parses under 3.9, no network.
#
# Reads the five records in this folder back and checks what is checkable
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

STATES = ("VERIFIED", "CONTRADICTED", "NOT_FOUND")
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


def readings():
    return {"notice": check_notice(read(NOTICE)), "states": check_states(read(VERIFY)),
            "absence": check_absence(), "ledger": check_ledger(read(LEDGER)),
            "design": check_design(read(DESIGN))}


def render(r):
    out = ["law-measurement-correction: readings of the five records (nothing edited)"]
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
