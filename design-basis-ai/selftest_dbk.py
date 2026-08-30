#!/usr/bin/env python3
# selftest_dbk.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises the delivered design_basis_checks.py and
# the audit. The delivered file is landed verbatim and not edited.
#
# The load-bearing checks: the coverage matrix's uncarried load is
# COMPUTED and the computation can fail (a constructed doc with A
# carried comes back covered); the n_eff equivalence sweep against the
# sibling's instrument is exhaustive to length 8; and the posture --
# class-level certification declined by the document's own Section 3 --
# is asserted to be stated in the report rather than assumed.

import io
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402
import audit as A  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    doc = io.open(os.path.join(HERE, "SOURCE_DROP.md"),
                  encoding="utf-8").read()

    # ---- the delivered harness is verbatim from Section 4
    src = io.open(os.path.join(HERE, "design_basis_checks.py"),
                  encoding="utf-8").read()
    chk("the delivered harness appears verbatim in the drop",
        src.strip() in doc)
    chk("no --selftest handling was added to the delivered file",
        "--selftest" not in src)

    # ---- the parse: 8 provisions, complete fields, 7 loads
    provs = A.provisions()
    chk("eight provisions parse", sorted(provs) ==
        ["P%d" % i for i in range(1, 9)])
    for p in sorted(provs):
        for f in A.FIELDS:
            chk("%s has %s" % (p, f), f in provs[p])
    chk("P6 carries the extra RATIONALE field", "RATIONALE" in provs["P6"])
    chk("seven load cases parse",
        A.load_cases() == ["A", "B1", "B2", "C", "D", "E", "F"])

    # the parser can fail: a constructed provision missing FALSIFY
    fake = ('### P1 — X\n```\nPROVISION  a\nCARRIES    E. b\n'
            'VERIFY     c\n```\n')
    fp = A.provisions(fake)
    chk("the parser reports a missing field rather than inventing one",
        "FALSIFY" not in fp["P1"])

    # ---- THE COVERAGE MATRIX, and its null
    cov = A.coverage()
    chk("load case A is carried by no provision",
        cov["uncarried"] == ["A"])
    chk("D is attacked-only", cov["attacked_only"] == ["D"])
    chk("E is carried three times and attacked once",
        cov["carried"]["E"] == ["P1", "P5", "P6"]
        and cov["attacked"]["E"] == ["P3"])
    chk("F is carried by P2, P7, P8",
        cov["carried"]["F"] == ["P2", "P7", "P8"])
    chk("B2 is carried by P3 and P4 (the governing load has provisions)",
        cov["carried"]["B2"] == ["P3", "P4"])
    # null: a constructed doc where A IS carried comes back covered,
    # so the uncarried finding is a property of the delivered text
    fake2 = doc.replace("CARRIES    E. an undeclared envelope",
                        "CARRIES    A, E. an undeclared envelope")
    cov2 = A.coverage(fake2)
    chk("the uncarried finding CAN fail (a doc carrying A reads covered)",
        cov2["uncarried"] == [])

    # ---- the delivered n_eff vs the sibling's, exhaustively
    eq = A.n_eff_equivalence()
    chk("the sweep is exhaustive to length 8 (511 lists)",
        eq["lists"] == 511)
    chk("zero disagreements with the sibling instrument",
        eq["mismatches"] == 0)
    chk("the zero-channel edge recurs in the second delivery",
        eq["zero_channel_edge_recurs"] and DB.n_eff([]) == 0)
    # the sibling is imported, not copied, in the audit
    asrc = io.open(os.path.join(HERE, "audit.py"), encoding="utf-8").read()
    chk("the audit imports the sibling instrument",
        "import effective_redundancy" in asrc)
    # "def n_eff" alone matches inside def n_eff_equivalence -- the
    # UNI_009 substring bleed, caught here in this file's own first
    # draft. The paren pins the definition.
    chk("and defines no n_eff of its own",
        "def n_eff(" not in asrc)

    # ---- the reframe reproduces through the delivered arithmetic
    rf = A.reframe_through_instrument()
    chk("all-collapsed gives N_eff = 1 at every scale",
        set(rf.values()) == {1})
    chk("and the report marks it consistency, not truth",
        "CONSISTENCY" in A.render())

    # ---- P7 prose vs code
    dt = A.dissent_threshold()
    chk("no fire at equality (reachable negative)",
        dt["fires_at_equality"] is False)
    chk("fires at 4 over 3 (the code's threshold is any excess)",
        dt["fires_at_4_over_3"] is True)
    chk("fires on a zero-source base",
        dt["fires_on_zero_sources"] is True)
    chk("the prose really says '>>' where the code says '> 1'",
        "concurrence >> independent" in doc and "> 1  # tune threshold" in doc)

    # ---- independence_ratio's designed-in split, both directions
    r0 = DB.independence_ratio(0, 0)
    chk("empty evidence base is NaN", math.isnan(r0))
    chk("and NaN is not zero", not (r0 == 0.0))
    chk("a real zero-upstream base IS zero",
        DB.independence_ratio(0, 5) == 0.0)
    chk("the two states are distinguishable",
        DB.independence_ratio(0, 5) == 0.0 and math.isnan(r0))
    chk("the over-one edge is unguarded (recorded, not repaired)",
        DB.independence_ratio(5, 3) > 1.0)

    # ---- egress measured; the prediction not fabricated
    chk("all three metadata sources refused",
        all(code == "000" for _h, code in A.EGRESS))
    chk("no synthetic evidence base exists in the folder",
        "n_supporting=" not in asrc and "replication_data" not in asrc)

    # ---- the posture: Section 3 applied to this audit
    out = A.render()
    one = " ".join(out.split())
    chk("the report declares the auditor is in-class",
        "member of the class" in one)
    chk("class-level verdicts are declined by construction",
        "DECLINED by construction" in one)
    chk("the report calls itself an instance of Section 3",
        "worked instance of Section 3" in one)
    chk("the mechanical/declared split is stated",
        "mechanical layer" in one and "recomputable by" in one)
    chk("the uncarried load is the headline",
        "CARRIED BY NO PROVISION" in out)
    chk("the report states what declining establishes",
        "not modesty" in one)

    # ---- audit refuses --selftest
    r = subprocess.run([sys.executable, os.path.join(HERE, "audit.py"),
                        "--selftest"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("audit.py refuses --selftest", r.returncode == 2)
    chk("and names where its checks live", b"selftest_dbk.py" in r.stderr)

    # ---- the no-severity screen, no exemptions
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
