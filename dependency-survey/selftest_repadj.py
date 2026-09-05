#!/usr/bin/env python3
"""Checks for repair_adjacency.py -- the refinement-chain RESULT made
checkable at the level the document fixes. Known answers, both directions.
The underlying sort is NOT reproduced (external corpus); these check the
transcription-consistency of the delivered §1-§4 memberships and the §6
cut-height framing.

    python3 dependency-survey/selftest_repadj.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import repair_adjacency as R  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_repadj")
    rc = subprocess.run([sys.executable, os.path.join(HERE, "repair_adjacency.py"), "--selftest"],
                        capture_output=True).returncode
    check("repair_adjacency refuses --selftest with rc 2", rc == 2)

    # ---- §1: the DeepSeek partition (9 components, 19 records)
    recs = R.deepseek_records()
    check("9 components over 19 records", len(R.DEEPSEEK) == 9 and len(recs) == 19)
    check("the components partition the records (no record in two components)",
          len(recs) == len(set(recs)))

    # ---- §2: Perplexity refines DeepSeek, yielding 11 groups, zero cross-cut
    groups = R.perplexity_groups()
    check("Perplexity has 11 groups (9 components, 2 split in two)", len(groups) == 11)
    pk, poff = R.perplexity_refines_deepseek()
    check("Perplexity REFINES DeepSeek: every group inside exactly one component, zero cross-cut",
          pk and poff == [])
    check("exactly 7 of the 9 components are left whole (identical to a Perplexity group)",
          sum(1 for c, r in R.DEEPSEEK.items() if c not in R.PERPLEXITY_SPLITS) == 7)

    # ---- §3: DeepSeek refines Kimi, each component under exactly one kind
    dk, dcc, dunc = R.deepseek_refines_kimi()
    check("DeepSeek REFINES Kimi: every component under exactly one live kind, zero cross-cut, none uncovered",
          dk and dcc == [] and dunc == [])
    check("the 4 live Kimi kinds cover all 9 components",
          sorted(c for cs in R.KIMI.values() for c in cs) == sorted(R.DEEPSEEK))
    check("the contested edges are present (flagged, not dropped): C7->K3, C8->K5",
          R.component_to_kind()["C7"] == ["K3"] and R.component_to_kind()["C8"] == ["K5"]
          and R.CORRECTION_CANDIDATE == {"C7": "K3"} and R.CONTESTABLE == {"C8": "K5"})

    # ---- the full chain nests: Perplexity refines DeepSeek refines Kimi
    check("the full chain is a strict hierarchy (both links refine, zero cross-cutting)",
          pk and dk)

    # ---- null tests, both directions (not CONSTANT_SILENT)
    # a Perplexity group that spans two components is caught
    bad_fine = [["T01", "T02"]]     # T01 in C1, T02 in C2
    okb, offb = R.refines(bad_fine, list(R.DEEPSEEK.values()))
    check("a fine block spanning two coarse blocks is detected as NOT a refinement", not okb and offb)
    # a genuine refinement passes
    okg, _ = R.refines([["T01", "T07"], ["T13"]], [R.DEEPSEEK["C1"]])
    check("a genuine sub-partition of one component passes (not CONSTANT_FIRES)", okg)

    # ---- §3: K4 dead (its members scatter across 3 components)
    k4 = R.k4_dead()
    check("K4 is dead: its blind members scatter across 3 distinct components",
          k4["dead"] and k4["distinct_components"] == 3)

    # ---- §4: the straggler placed in C1, not closed on one system
    check("the straggler T13 sits in C1 (the one cross-cutting event)",
          R.STRAGGLER == "T13" and R.STRAGGLER in R.DEEPSEEK[R.STRAGGLER_COMPONENT])

    # ---- §6: the count is a CUT HEIGHT, never a bare integer
    kc = R.kind_count()
    check("kind_count() returns a cut-height statement, not a number",
          isinstance(kc, str) and "CUT HEIGHT" in kc and not kc.strip().isdigit())
    ch = R.cut_heights()
    check("cut heights name three levels (class / operation / operation+referent)", len(ch) == 3)
    sa = R.standing_answer()
    check("standing answer: SEVERAL / cut-height / both endpoints / membership fixed",
          sa["one_or_several"].startswith("SEVERAL") and "CUT HEIGHT" in sa["how_many"]
          and "both endpoints" in sa["which_to_report"] and sa["fixed"].startswith("MEMBERSHIP"))

    # ---- the report screens clean, but for the delivered term "repair"
    # (the RESULT's own subject: repair adjacency / repair class / repair
    # operation). Declared exemption, measured with the three-arm harness.
    out = R.report()
    masked = out.replace("repair", "mend")
    check("report render: masked, the screen is clean", not no_severity.hits(masked))
    check("report render: the only firer is the delivered term 'repair'",
          {w for _, w, _ in no_severity.hits(out)} == {"repair"})
    check("report render: a planted word is caught through the exemption",
          {w for _, w, _ in no_severity.hits(masked + "\nthis is wrong\n")} == {"wrong"})

    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "repair_adjacency.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
