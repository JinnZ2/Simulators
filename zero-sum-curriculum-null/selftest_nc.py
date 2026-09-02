#!/usr/bin/env python3
"""Checks for null_construction.py. The parse is asserted against the
delivered file, every logical result is checked in both directions on
constructed states, and the sibling import is exercised filled and
unfilled. Nothing here holds a value from the incident.

    python3 zero-sum-curriculum-null/selftest_nc.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import null_construction as NC  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_nc")
    p = NC.parse()

    # ---- the parse against the delivered file
    check("five branches parsed", sorted(p["branches"]) == ["N1", "N2", "N3", "N4", "N5"])
    check("every branch has requires/test/status",
          all(p["branches"][b][f] for b in p["branches"] for f in ("requires", "test", "status")))
    check("N3's wrapped test line is joined",
          "opponent rather than as terrain" in p["branches"]["N3"]["test"])
    check("RESULT block parsed with the survival line",
          any("survives only on the two branches" in l for l in p["result"]))
    check("header carries the conjunction word",
          any("each is a requirement" in l for l in p["header"]))
    check("every declared state quotes its status line",
          all(NC.check_states(p).values()))
    bad = NC.parse("N1  x\n      requires: r\n      test: t\n      status: nothing like it\nRESULT\n  z\n")
    check("a state whose quote is absent is reported false",
          NC.check_states({"branches": {**p["branches"], "N1": bad["branches"]["N1"]}})["N1"] is False)

    # ---- the two readings, both directions
    check("conjunction: one failing branch empties the set",
          NC.survival("conjunction") == set())
    allopen = {b: NC.OPEN for b in NC.STATE}
    check("conjunction: all surviving -> all carried",
          NC.survival("conjunction", states=allopen) == set(NC.STATE))
    check("disjunction on the delivered states: N2 and N4",
          NC.survival("disjunction") == {"N2", "N4"})
    check("stated RESULT matches the disjunction",
          NC.stated_result_set(p) == NC.survival("disjunction"))
    check("stated RESULT does not match the conjunction",
          NC.stated_result_set(p) != NC.survival("conjunction"))
    check("N1/N2 exclusivity holds on the delivered requires lines", NC.exclusive_holds())
    try:
        NC.survival("either"); check("unknown reading refused", False)
    except ValueError:
        check("unknown reading refused", True)

    # ---- dependencies, both directions
    check("with dependencies N2 drops (N3 is PARTIAL) and N4 stands",
          NC.survival("disjunction", depends=NC.DEPENDS) == {"N4"})
    n3open = dict({b: s for b, (s, _) in NC.STATE.items()}, N3=NC.OPEN)
    check("if N3 were open, N2 would carry again",
          NC.survival("disjunction", states=n3open, depends=NC.DEPENDS) == {"N2", "N3", "N4"})
    check("dependency edges name existing branches",
          all(a in NC.STATE and b in NC.STATE for a, b, _ in NC.DEPENDS))
    check("a dependency chain reaches a fixed point (A->B->C with C out)",
          NC.survival("disjunction",
                      states={"A": NC.OPEN, "B": NC.OPEN, "C": NC.FAILS},
                      depends=[("A", "B", ""), ("B", "C", "")]) == set())

    # ---- N2 through the sibling, unfilled and filled
    sheets = NC.n2_sheets()
    cmp_ = NC.n2_compare(sheets)
    check("six measures compared", len(cmp_) == 6)
    check("every diff None when both arms unmeasured",
          all(v["diff"] is None for v in cmp_.values()))
    check("arms differ only in the source block",
          {k for k in sheets["incident"] if sheets["incident"][k] != sheets["control"][k]} == {"source"})
    filled = json.loads(json.dumps(sheets))
    for arm, tc, ts in (("incident", 3, 4), ("control", 1, 4)):
        filled[arm]["t_characterize"].update({"value": tc, "unit": "days"})
        filled[arm]["t_solve"].update({"value": ts, "unit": "hours"})
    c2 = NC.n2_compare(filled)
    check("filled both arms: M1 diff computes (18 - 6 = 12)",
          abs(c2["M1_explore_ratio"]["diff"] - 12.0) < 1e-12)
    half = json.loads(json.dumps(sheets))
    half["incident"]["t_characterize"].update({"value": 3, "unit": "days"})
    half["incident"]["t_solve"].update({"value": 4, "unit": "hours"})
    check("one arm filled: diff stays None",
          NC.n2_compare(half)["M1_explore_ratio"]["diff"] is None
          and NC.n2_compare(half)["M1_explore_ratio"]["incident"] == 18.0)
    check("both N2 outcomes route the null through N3",
          all("N3" in v["null"] for v in NC.N2_OUTCOMES.values()))

    # ---- named artifacts, by content
    found = NC.named_present()
    cls = NC.classify_hits(found)
    check("the three named artifacts have no independent hit in the tree",
          all(not c["independent"] for c in cls.values()))
    check("any hit is in a root index file that quotes this folder",
          all(f in NC.INDEX_FILES for c in cls.values() for f in c["index"]))
    check("classify_hits keeps a non-index hit in the independent column",
          NC.classify_hits({"x": ["CLAUDE.md", "other/file.md"]})["x"]
          == {"index": ["CLAUDE.md"], "independent": ["other/file.md"]})
    tmp = os.path.join(HERE, "..", "hf-incident-extract", "_nc_plant.txt")
    with open(tmp, "w") as fh:
        fh.write("the depth-stack instrument lives here\n")
    try:
        check("a planted mention is found by content, in the independent column",
              any("_nc_plant" in f for f in
                  NC.classify_hits(NC.named_present())["depth-stack instrument"]["independent"]))
    finally:
        os.remove(tmp)
    check("this folder is excluded from its own scan",
          not any(f.startswith("zero-sum-curriculum-null") for v in found.values() for f in v))

    # ---- CLI and screen
    rc = subprocess.run([sys.executable, os.path.join(HERE, "null_construction.py"),
                         "--selftest"], capture_output=True).returncode
    check("module refuses --selftest with rc 2", rc == 2)
    out = NC.render()
    check("render screens clean", not no_severity.hits(out))
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))
    check("render states the exclusivity result", "cannot both hold (absent vs present): True" in out)
    with open(os.path.join(HERE, "samples", "render.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)

    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
