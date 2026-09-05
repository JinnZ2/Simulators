#!/usr/bin/env python3
"""Checks for taxonomy_replication.py -- the cross-model replication
RESULT made checkable at the level the document fixes. Known answers,
both directions. The underlying sort is NOT reproduced (external corpus);
these check the transcription-consistency of the delivered §1 table and
the §6 count-refusal.

    python3 dependency-survey/selftest_taxrep.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import taxonomy_replication as T  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def main():
    print("selftest_taxrep")
    rc = subprocess.run([sys.executable, os.path.join(HERE, "taxonomy_replication.py"), "--selftest"],
                        capture_output=True).returncode
    check("taxonomy_replication refuses --selftest with rc 2", rc == 2)

    # ---- the headline: strictly nested (the delivered map is a function)
    ok, crosscut = T.strictly_nested()
    check("the delivered §1 map is strictly nested: every Perplexity group under exactly one Kimi kind, zero cross-cutting",
          ok and crosscut == [])
    inv = T.group_to_kinds()
    check("every assigned Perplexity group maps to exactly one Kimi kind",
          all(len(inv[g]) == 1 for g in T.perplexity_groups() if g != T.STRAGGLER_GROUP))
    check("the straggler G9 maps to no kind (unassigned, not cross-cut)", inv[T.STRAGGLER_GROUP] == [])

    # ---- null test: a constructed cross-cut is detected (not CONSTANT_SILENT)
    crossed = dict(T.KIMI_COVERS)
    crossed["K2"] = crossed["K2"] + ["G1"]   # G1 now under K1 and K2
    okc, cc = T.strictly_nested(crossed)
    check("a constructed cross-cut (G1 under two kinds) is detected as NOT nested", not okc and "G1" in cc)

    # ---- the counts §1 fixes
    check("11 Perplexity groups over 13 distinct records", len(T.perplexity_groups()) == 11 and T.DISTINCT_TOTAL == 13)
    check("4 Kimi kinds carry members; K4 has zero", len(T.KIMI_COVERS) == 4 and "K4" not in T.KIMI_COVERS and "K4" in T.KIMI_KINDS_ZERO_MEMBERS)
    check("the distinct counts sum to 13 (K1..K5 members plus the straggler)",
          sum(T.KIMI_DISTINCT.values()) + T.STRAGGLER_DISTINCT == T.DISTINCT_TOTAL)

    # ---- §6: kind_count is a REFUSAL, never an integer
    kc = T.kind_count()
    check("kind_count() returns the §6 refusal, not a number", isinstance(kc, str) and "UNSETTLED" in kc and not kc.strip().isdigit())
    sa = T.standing_answer()
    check("standing answer: SEVERAL / UNSETTLED / MEMBERSHIP",
          sa["one_or_several"].startswith("SEVERAL") and "UNSETTLED" in sa["how_many"] and sa["fixed"].startswith("MEMBERSHIP"))
    check("grain is reported as a disagreement (4 vs 11), not as THE count",
          T.grain()["kimi_kinds_with_members"] == 4 and T.grain()["perplexity_groups"] == 11)

    # ---- the report screens clean (authored framing; no delivered severity tokens quoted)
    out = T.report()
    check("report render screens clean", not no_severity.hits(out))
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))

    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "taxonomy_replication.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
