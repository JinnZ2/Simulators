#!/usr/bin/env python3
"""Checks for the v2 instruments against the delivered v2/p4_goal.py and
the seed ../scope_test.py, neither of which is edited. Known answers
first, both directions. Writes v2/samples/.

    python3 cooperative-substrate/v2/selftest_v2.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "sheet-structure-scan"))
import p5_lag as P5  # noqa: E402
import scope_check as SC  # noqa: E402
import v2_audit as A  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_v2")
    for f in ("p5_lag.py", "scope_check.py", "v2_audit.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)

    # ---- delivered p4_goal.py is truncated, structurally
    t = A.truncation()
    check("p4_goal.py parses but is structurally incomplete", t["parses"] and not t["complete"])
    check("run() has no return, no __main__ guard, only 'accept' of three stances in the body",
          not t["run_has_return"] and not t["has_main_guard"] and t["stances_in_body"] == ["accept"])
    check("the last delivered line binds an undefined name (the truncation tell)", t["binds_undefined_last"])
    check("it is 1282 bytes as delivered", t["bytes"] == 1282)

    # ---- manifest map
    mm = A.manifest_map()
    check("manifest counts: 1 delivered-truncated, 5 rename v1, 1 new, 1 seeded, 1 declined, 1 present",
          mm["counts"] == {"DELIVERED_TRUNCATED": 1, "RENAMES_V1": 5, "NEW": 1, "SEEDED": 1, "DECLINED": 1, "PRESENT": 1})
    check("every manifest target exists in the folder", all(v["target_exists"] for v in mm["map"].values()))

    # ---- v1 P4 cannot represent the v2 cut
    v1 = A.v1_has_correct_mode()
    check("v1 p4_goal_coherence has no three-stance model (accept/correct/contest)", not v1["has_three_stances"])
    check("the delivered v2 p4_goal.py names the cut as the stance column", v1["v2_delivered_names_the_cut"])

    # ---- P5 known answers
    anti = P5.evaluate(P5.ANCHORS[0])
    check("antibiotic anchor: ratio ~101.5, DECLARED_UNKNOWN, preconditions enumerated",
          abs(anti["gate"]["ratio"] - 101.5) < 0.5 and anti["gate"]["verdict"] == "DECLARED_UNKNOWN" and anti["precondition"]["state"] == "ENUMERATED")
    same = P5.evaluate(P5.ANCHORS[1])
    # the anchor is one month over six months = 1/6; the render shows 0.2 at %.1f,
    # and a first draft of this check read that rounded display rather than the value
    check("same-window action: ratio 1/6, TRACKED", abs(same["gate"]["ratio"] - 1.0 / 6) < 1e-9 and same["gate"]["verdict"] == "TRACKED")
    und = P5.evaluate(P5.ANCHORS[2])
    check("undeclared-variable action: ratio undefined (None), UNDECLARED, empty precondition set flagged",
          und["gate"]["ratio"] is None and und["gate"]["verdict"] == "UNDECLARED" and und["precondition"]["state"] == "EMPTY_SET_FLAGGED")
    check("UNDECLARED is a distinct state from TRACKED at a small ratio, not the same cell",
          P5.gate({"t_visible_s": None, "t_scored_s": 100})["verdict"] == "UNDECLARED"
          and P5.gate({"t_visible_s": 1, "t_scored_s": 100})["verdict"] == "TRACKED")
    check("the >= 10 gate: ratio exactly 10 is DECLARED_UNKNOWN, just under is TRACKED",
          P5.gate({"t_visible_s": 100, "t_scored_s": 10})["verdict"] == "DECLARED_UNKNOWN"
          and P5.gate({"t_visible_s": 99, "t_scored_s": 10})["verdict"] == "TRACKED")
    check("an empty precondition set is flagged, not read as no dependencies",
          P5.precondition_constraint({"preconditions": []})["state"] == "EMPTY_SET_FLAGGED"
          and P5.precondition_constraint({"preconditions": None})["state"] == "NOT_ENUMERATED")
    check("the compliance pairing is a 2x2 cell, recorded not scored",
          P5.compliance_pairing(P5.ANCHORS[2])["cell"] == ("compliance_required", "UNDECLARED"))

    # ---- scope_check null
    conds, cases = SC.seed_cases()
    check("five seed cases, one harsh (E. coli), three all-C1-C4-present",
          len(cases) == 5 and [c["name"] for c in cases if c["harsh"]] == ["E. coli evolvability"]
          and len([c for c in cases if SC.all_present(c)]) == 3)
    ns = SC.null_search(cases)
    check("the null's antecedent is met by E. coli and the verdict is UNRESOLVED_HARSHNESS_ENTANGLED",
          ns["antecedent_met_by"] == ["E. coli evolvability"] and ns["verdict"] == "UNRESOLVED_HARSHNESS_ENTANGLED")
    # constructed: a harsh case with INDEPENDENT harshness resolves the null the order's way
    resolved = SC.extend(cases, [{"name": "constructed independent-harsh", "cells": {c: "y" for c in SC.CONDS},
                                  "reported": "competition_reported", "harsh": True, "harsh_independent": (True, "constructed: harshness is environmental, not the scoring")}])
    check("a constructed case with independent harshness fires SCOPE_NOT_SUFFICIENT (the null is not CONSTANT_SILENT)",
          SC.null_search(resolved)["verdict"] == "SCOPE_NOT_SUFFICIENT")
    # constructed: no harsh case at all -> absence is the finding
    none_harsh = SC.extend([c for c in cases if not c["harsh"]], [])
    check("with no harsh case the null reads ABSENCE_IS_THE_FINDING", SC.null_search(none_harsh)["verdict"] == "ABSENCE_IS_THE_FINDING")
    check("scope_check imports the seed rather than restating it", "scope_test" in open(os.path.join(HERE, "scope_check.py"), encoding="utf-8").read())
    try:
        SC.extend(cases, [{"name": "bad", "cells": {"C1": "maybe"}, "reported": "x", "harsh": False}])
        check("a malformed case is refused", False)
    except ValueError:
        check("a malformed case is refused", True)

    # ---- §6 non-goal scan: sections and bylines, not prose mentions
    ng = A.non_goal_scan()
    check("§6 scan is clean over the deliverables, with the scanner excluded and said so",
          ng["clean"] and ng["excluded"] and "v2_audit.py" in ng["excluded"][0])
    check("the §6 scan flags an author SECTION, not a prose mention of the non-goal (both directions)",
          A.scan_flags("## About the author\nwritten by someone") and not A.scan_flags("this folder has no author or working-style section, and makes no claim that cooperation outperforms competition"))

    # ---- renders and the screen
    outs = {"p5_lag": P5.render(), "scope_check": SC.render(), "v2_audit": A.render()}
    for k, v in outs.items():
        check("%s render screens clean" % k, not no_severity.hits(v))
    check("screen fires on a planted word", bool(no_severity.hits(outs["v2_audit"] + "\nthis is wrong\n")))
    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    for k, v in outs.items():
        with open(os.path.join(HERE, "samples", k + ".sample.txt"), "w", encoding="utf-8") as fh:
            fh.write(v + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
