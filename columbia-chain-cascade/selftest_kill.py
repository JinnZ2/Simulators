#!/usr/bin/env python3
# selftest_kill.py -- CC0, stdlib only, parses under 3.9
#
# The checks that exercise kill_audit.py: the three kill verdicts, the
# two findings the landing turned up, the pre-closure scan, and the
# cold-start table. Each verdict is checked against the delivered
# artifacts, and the two null-style checks confirm the adjudicators can
# come back the other way (a kill that could only ever confirm is not an
# adjudication).

import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import kill_audit as K  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    # ---- KILL 1: overlay artifact, carries an intended, sound conclusion
    k1 = K.kill1()
    chk("KILL 1: the self-correction trace is present in render()",
        k1["trace_present"])
    chk("KILL 1: the corrected line is arithmetically sound",
        k1["corrected_conclusion_is_right"])
    chk("KILL 1: verdict is CONFIRMED",
        k1["verdict"].startswith("CONFIRMED"))
    # null: the corrected conclusion check can fail -- the wrong pair of
    # verdicts would not be sound
    import contributing_inflow as CI
    chk("KILL 1 null: an incorrect verdict pair is NOT sound (the "
        "soundness check can fail)",
        not (CI.combine("max", 6.0, 5.2) >= 10.0))

    # ---- KILL 2: prose (max-flip) and code (sum-tip) diverge; resolved
    k2 = K.kill2()
    chk("KILL 2: the prose and code disagree on a nonzero share of "
        "cases", k2["prose_vs_code_disagreements"] > 0)
    chk("KILL 2: the sweep is one-sided (urban never independent-only)",
        k2["sweep_one_sided"])
    chk("KILL 2: verdict is CONFIRMED and resolved by physics",
        k2["verdict"].startswith("CONFIRMED"))
    # null: prose and code AGREE on the boundary cases where the
    # increment is zero -- so the disagreement is not a constant
    agree = 0
    for wave in (2.0, 6.0):
        for pn in (3.0, 5.0):
            for crest in (10.0,):
                r = CI.urban_sensitivity(wave, pn, crest, 0.0)
                pe = r["pool_effective"]
                if (wave < pe < crest) == r["urban_decisive"]:
                    agree += 1
    chk("KILL 2 null: prose and code agree on some cases (the "
        "disagreement is measured, not asserted everywhere)", agree > 0)

    # ---- KILL 3: asymmetry, and do-not-drop, both confirmed
    k3 = K.kill3()
    chk("KILL 3: owners are refused from memory", k3["owners_from_memory"] == 0)
    chk("KILL 3: node rows carry a knowledge_state field",
        k3["node_carries_knowledge_state"])
    chk("KILL 3: tribal rows are supplied from memory",
        k3["tribal_rows_from_memory"] == 6)
    chk("KILL 3: tribal rows carry NO knowledge_state field",
        not k3["tribal_has_knowledge_state"] and k3["tribal_row_arity"] == 4)
    chk("KILL 3: the authority bound is invariant to the tribal list",
        k3["bound_invariant_to_tribal"]
        and k3["bound_with_tribal"] == 2)
    chk("KILL 3: knowledge_state.py rejects INSTITUTIONAL_EXCLUSION",
        k3["exclusion_is_rejected_state"])
    chk("KILL 3: both verdicts are CONFIRMED",
        k3["verdict_asymmetry"].startswith("CONFIRMED")
        and k3["verdict_do_not_drop"].startswith("CONFIRMED"))

    # ---- FINDING: CCC_017 refuted on its delivered instance
    c17 = K.ccc017_delivered_instance()
    chk("CCC_017: the delivered module_f report is NOT clean on the "
        "screen", not c17["delivered_ccc017_holds"])
    chk("CCC_017: the token that fires is a certainty verb",
        c17["token"] == "proves")

    # ---- FINDING: the delivered v2 selftest exercises the v1 modules
    vt = K.v2_selftest_targets()
    chk("v2 selftest imports the bare v1 modules",
        vt["v2_selftest_imports_bare_v1"])
    chk("v2 selftest unpacks NODES as a 4-tuple (matches v1, not v2)",
        vt["v2_selftest_unpacks_4tuple"])
    chk("v2 selftest reads the v1 truncation key",
        vt["v2_selftest_reads_v1_truncation_key"]
        and vt["v1_audit_has_that_key"])
    chk("audit_v2 renamed that key, so the v2 audit is not the one "
        "under test", vt["audit_v2_renamed_the_key"])
    chk("eap_coverage_v2 NODES is a 5-tuple (a 4-unpack would raise)",
        vt["eap_v2_nodes_arity"] == 5)

    # ---- FINDING: the pre-closure scan
    pc = K.pre_closure_scan()
    chk("exactly one bare 'if published' pre-closure in the gap file",
        pc["count"] == 1)
    chk("and it is the Gap 6 seismic assessments line",
        any("seismic" in t.lower() for _n, t in pc["pre_closures"]))

    # ---- the cold-start table
    cs = K.cold_start()
    chk("the cold-start test covers fifteen gaps", cs["n"] == 15)
    chk("every gap names a falsifier a stranger can evaluate (Q2)",
        all(r["q"][1] for r in cs["rows"]))
    chk("every gap names a deliverable interface (Q3)",
        all(r["q"][2] for r in cs["rows"]))
    chk("not every gap is startable on public data alone (Q1 flags "
        "the hydraulic ones)",
        0 < cs["public_startable"] < cs["n"])
    chk("the clean count is a strict subset (the test discriminates)",
        0 < cs["clean_on_all_five"] < cs["n"])

    # ---- the delivered v1 selftest still passes untouched
    r = subprocess.run([sys.executable, os.path.join(HERE,
                        "selftest_ccc.py")],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("the delivered v1 selftest still passes (nothing v1 was edited)",
        r.returncode == 0 and b", 0 failed" in r.stdout)

    # ---- kill_audit refuses --selftest
    r2 = subprocess.run([sys.executable, os.path.join(HERE,
                        "kill_audit.py"), "--selftest"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("kill_audit.py refuses --selftest",
        r2.returncode == 2 and b"selftest_kill.py" in r2.stderr)

    # ---- the no-severity screen, with ONE declared exemption
    sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    out = K.render()
    # 'proves' is a delivered module_f token the CCC_017 finding reports;
    # echoing it verbatim is how the finding names which token fired, so
    # it is exempt. Measured with the three-arm harness.
    EXEMPT = ("proves",)
    chk("one declared exemption on the kill_audit report", len(EXEMPT) == 1)
    chk("and it is a delivered module_f token",
        "proves" in io.open(os.path.join(HERE, "module_f.py"),
                            encoding="utf-8").read())
    masked = out
    for wd in EXEMPT:
        masked = re.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), masked)
    chk("the report is clean apart from the exemption",
        not no_severity.hits(masked))
    fired = set(w for _n, w, _l in no_severity.hits(out))
    chk("and the exemption is the only token that fires",
        fired == set(EXEMPT))
    pmask = out + "\nthis design is broken and invalid\n"
    for wd in EXEMPT:
        pmask = re.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), pmask)
    chk("a planted violation is still caught through the exemption",
        bool(no_severity.hits(pmask)))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
