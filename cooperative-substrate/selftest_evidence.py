#!/usr/bin/env python3
"""Checks for scope_test.py, term_table.py and evidence_audit.py against
the delivered EVIDENCE_PACK.md, which is parsed and never edited.

    python3 cooperative-substrate/selftest_evidence.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import scope_test as S  # noqa: E402
import term_table as T  # noqa: E402
import evidence_audit as E  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_evidence")
    for f in ("scope_test.py", "term_table.py", "evidence_audit.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)
    # ---- scope test, parsed from the pack
    conds, rows = S.parse()
    check("four conditions parsed with two-word names intact", list(conds) == ["C1", "C2", "C3", "C4"] and conds["C3"][0] == "narrow metric")
    check("five rows parsed, every cell y or n", len(rows) == 5 and all(set(r["cells"].values()) <= {"y", "n"} and len(r["cells"]) == 4 for r in rows))
    sep = S.separation(conds, rows)
    check("two distinct condition vectors over five rows; conditions do not vary independently",
          sep["distinct_vectors"] == 2 and not sep["conditions_vary_independently"])
    check("every condition separates alone and none is necessary", all(sep["separates_alone"].values()) and sep["necessary"] == [])
    check("conjunction: all-y competition, all-n not, a missing cell UNDETERMINED",
          S.conjunction({"cells": {"C1": "y", "C2": "y", "C3": "y", "C4": "y"}}, conds) == "COMPETITION_DOMINANT_OBSERVATION"
          and S.conjunction({"cells": {"C1": "n", "C2": "y", "C3": "y", "C4": "y"}}, conds).startswith("NOT_")
          and S.conjunction({"cells": {"C1": "y", "C2": "y", "C3": "y"}}, conds) == "UNDETERMINED")
    # a constructed off-diagonal row makes the separation question answerable: null in the other direction
    extra = rows + [{"name": "constructed", "cells": {"C1": "y", "C2": "n", "C3": "y", "C4": "y"}, "reported": "x"}]
    S.REPORTED_CLASS["constructed"] = "not_reported"
    sep2 = S.separation(conds, extra)
    S.REPORTED_CLASS.pop("constructed")
    check("one constructed off-diagonal row: C2 becomes necessary and C1/C3/C4 stop separating alone",
          sep2["necessary"] == ["C2"] and sep2["separates_alone"] == {"C1": False, "C2": True, "C3": False, "C4": False})
    ax = S.axes(rows, conds)
    both = [a for a in ax if a["both_axes_recorded"]]
    check("both axes recorded on exactly one row, E. coli, and they disagree there",
          len(both) == 1 and both[0]["row"] == "E. coli evolvability" and both[0]["e01_matches_reported"] is False)
    check("rows with no stated stress read UNRECORDED, not benign", sum(1 for a in ax if a["stress"] == "UNRECORDED") == 3)
    check("the benign test is stated NOT_RUN", S.benign_reading()["status"] == "NOT_RUN")
    # ---- term table
    sm = T.summary()
    check("25 cells, 2 filled, 0 predictions, one experiment sitting there", sm["cells"] == 25 and sm["filled"] == 2 and sm["predictions"] == 0 and len(sm["experiments"]) == 1)
    check("schema: a filled cell without a basis is a finding; a non-numeric prediction is a finding",
          T.validate({(1, 1): {"state": "MEASURED", "basis": ""}}) and T.validate({(1, 1): {"state": "MEASURED", "basis": "x", "prediction_in_substrate": "big"}}))
    check("schema: the delivered table validates clean", T.validate() == [])
    check("an unfilled cell reads UNRECORDED and never MISSING", T.cell(4, 4)["state"] == "UNRECORDED")
    # ---- evidence audit
    rows_e, targets = E.parse()
    c = E.census(rows_e)
    check("34 rows in six sections, two target papers", c["rows"] == 34 and c["by_section"] == {"E0": 8, "E1": 3, "E2": 6, "E3": 5, "E4": 5, "E5": 7} and len(targets) == 2)
    check("33 UNVERIFIED-FULLTEXT and 1 DISPUTED, nothing else", c["by_status"] == {"UNVERIFIED-FULLTEXT": 33, "DISPUTED": 1})
    check("15 rows carry no locator beyond author/year or a name", len(c["name_only_or_author_year"]) == 15)
    d = E.doi_syntax(rows_e, targets)
    check("15 well-formed distinct DOIs, no duplicates", d["count"] == 15 and d["distinct"] == 15 and d["all_well_formed"])
    check("four arXiv ids, calendar-valid and not in the future", len(E.arxiv_calendar(rows_e)) == 4 and all(a["month_valid"] and a["not_in_future"] for a in E.arxiv_calendar(rows_e)))
    check("an arXiv id from a future month is flagged", not E.arxiv_calendar([{"id": "x", "source": "arXiv 2701.00001"}])[0]["not_in_future"])
    check("Nat Comms DOI years consistent where a year is stated", all(y["consistent"] for y in E.doi_years(rows_e, targets)))
    check("a stated year against a different embedded year is flagged",
          not E.doi_years([{"id": "x", "source": "Nat Comms 2019 10.1038/s41467-024-00000-0"}], [])[0]["consistent"])
    check("locator classes: doi, arxiv, pmc, url, author_year, name_only all reachable",
          [E.locator(s) for s in ("10.1000/x", "arXiv 2501.00001", "PMC1234567", "site.net/a/1", "Smith 2001", "Smith")]
          == ["doi", "arxiv", "pmc", "url", "author_year", "name_only"])
    check("E3.3 variable and the E8 all-y class row are both in the pack", E.e33_vs_table()["both_present"])
    check("every declared cross-link target exists", all(x["exists"] for x in E.cross_links()))
    wo = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read().lower()
    check("the order names no 'build target' for E6 to be the second of", "build target" not in wo)
    rd = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
    pack = open(os.path.join(HERE, "EVIDENCE_PACK.md"), encoding="utf-8").read()
    note = pack.split("**Recording-rate note (belongs in README):** ")[1].split("\n")[0]
    check("the recording-rate note is in the README verbatim", note in rd)
    # ---- renders and the screen
    outs = {"scope": S.render(), "term": T.render(), "evidence": E.render()}
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    for k, v in outs.items():
        check("%s render screens clean" % k, not no_severity.hits(v))
        with open(os.path.join(HERE, "samples", "%s.sample.txt" % {"scope": "scope_test", "term": "term_table", "evidence": "evidence_audit"}[k]), "w", encoding="utf-8") as fh:
            fh.write(v + "\n")
    check("screen fires on a planted word", bool(no_severity.hits(outs["scope"] + "\nthis is wrong\n")))
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
