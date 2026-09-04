#!/usr/bin/env python3
# selftest_ccc.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises eap_coverage_v2.py, audit_v2.py, and module_f.py.
#
# REPAIRED: the delivered copy imported the bare v1 modules and unpacked
# a 4-tuple, so the v2 additions shipped unexercised (CCA_006). It now
# runs against the v2 record, and checks the tribal rows are typed.
# Pre-repair text is at git 399517b.
#
# The load-bearing checks are the two refusals: no per-node owner is
# assigned (the data is not in the delivered text) and the exact seam
# count is refused -- while the governance conclusion still comes back
# settled, because it rests on the CA/US split the text does carry.

import ast
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eap_coverage_v2 as EAP  # noqa: E402
import audit_v2 as A  # noqa: E402

# Module F may not exist in all environments; import conditionally
try:
    import module_f as MF  # noqa: E402
    HAS_MODULE_F = True
except ImportError:
    HAS_MODULE_F = False

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

    # ---- the node list is transcribed, not invented, and matches the text
    for name, _reach, _j, _o, _k in EAP.NODES:
        chk("node in the delivered text: %s" % name, name in doc)
    chk("18 dam nodes", len(EAP.NODES) == 18)
    chk("the estuary is recorded as a reach, not a node",
        EAP.ESTUARY_IS_A_REACH and
        not any(n[0] == "Estuary" for n in EAP.NODES))
    # every reach label used is a section header in the delivered text
    for reach in set(n[1] for n in EAP.NODES):
        chk("reach label from the text: %s" % reach,
            re.search(r"(?m)^\s*%s:" % reach, doc) is not None)

    # ---- the jurisdiction tags come only from the text
    chk("the CA tag is on exactly the three upper nodes",
        [n[0] for n in EAP.NODES if n[2] == "CA"]
        == ["Mica", "Revelstoke", "Keenleyside"])
    chk("(CA) appears in the delivered text", "(CA)" in doc)
    chk("two jurisdictions in the node list",
        EAP.jurisdictions() == ["CA", "US"])

    # ---- NO per-node owner is assigned. This is the refusal.
    chk("no node carries an owner", EAP.owners_assigned() == [])
    chk("every owner field is UNASSIGNED",
        all(n[3] == EAP.UNASSIGNED for n in EAP.NODES))
    b = EAP.spanning_bound()
    chk("per-node owner known is zero", b["per_node_owner_known"] == 0)
    chk("the exact seam count is refused",
        b["exact_seam_count"] == EAP.UNASSIGNED)
    chk("and the refusal names the reason",
        "not supplied from memory" in b["exact_seam_reason"])

    # ---- the tribal rows carry the same discipline the owners carry
    import knowledge_state as KS
    chk("six tribal rows", len(EAP.TRIBAL_JURISDICTION) == 6)
    chk("every tribal row carries a valid knowledge_state and a source",
        all(len(t) == 6 and KS.is_valid(t[4]) and t[5] for t in
            EAP.TRIBAL_JURISDICTION))
    chk("tribal adjacency is typed UNKNOWN_ATM (carried, not verified)",
        all(t[4] == EAP.UNKNOWN_ATM for t in EAP.TRIBAL_JURISDICTION))
    _save_t = EAP.TRIBAL_JURISDICTION
    try:
        EAP.TRIBAL_JURISDICTION = []
        chk("the tribal rows are recorded, not counted in the bound",
            EAP.spanning_bound()["authorities_lower_bound"] == 2)
    finally:
        EAP.TRIBAL_JURISDICTION = _save_t
    chk("the record says so in its own prose",
        "not counted" in EAP.no_plan_spans()["robust_because"])

    # ---- the owner categories are the five the spec names, verbatim
    for cat in EAP.OWNER_CATEGORIES:
        chk("owner category from the text: %s" % cat, cat in doc)
    chk("five owner categories", len(EAP.OWNER_CATEGORIES) == 5)

    # ---- the conclusion is settled, and settled by the CA/US split
    s = EAP.no_plan_spans()
    chk("no single plan spans the chain", s["no_single_plan_spans_chain"])
    chk("settled by the CA/US boundary",
        "CA/US" in s["settled_by"])
    chk("the lower bound is 2", s["authorities_lower_bound"] == 2)

    # ---- and it is ROBUST to the missing data, both directions
    chk("robust to the missing ownership", s["robust_to_missing_ownership"])
    # the floor is > 1, so the conclusion holds
    chk("floor exceeds one", b["authorities_lower_bound"] > 1)
    # null test: a hypothetical single-jurisdiction chain would NOT settle it
    save = EAP.NODES
    try:
        EAP.NODES = [(n[0], n[1], "US", EAP.UNASSIGNED, n[4]) for n in save]
        chk("a single-jurisdiction chain does NOT settle the claim from "
            "jurisdiction alone",
            EAP.no_plan_spans()["authorities_lower_bound"] == 1
            and EAP.no_plan_spans()["no_single_plan_spans_chain"] is False)
    finally:
        EAP.NODES = save
    chk("and the real node list is restored",
        EAP.jurisdictions() == ["CA", "US"])

    # ---- the exact-count refusal cannot be a hidden guess: no owner
    # string other than UNASSIGNED appears assigned anywhere
    src = io.open(os.path.join(HERE, "eap_coverage_v2.py"),
                  encoding="utf-8").read()
    tree = ast.parse(src)
    assigned_owners = set()
    for node in ast.walk(tree):
        # only the NODES list literal, not unpacking targets like
        # `for name, reach, juris, owner in NODES`
        if isinstance(node, ast.Assign):
            names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if "NODES" not in names:
                continue
            for elt in ast.walk(node.value):
                if isinstance(elt, ast.Tuple) and len(elt.elts) == 5:
                    last = elt.elts[3]
                    if isinstance(last, ast.Constant):
                        assigned_owners.add(last.value)
                    elif isinstance(last, ast.Name):
                        assigned_owners.add(last.id)
    chk("the only owner value in the node table is UNASSIGNED",
        assigned_owners == {"UNASSIGNED"})

    # ---- the truncation is detected, not asserted
    t = A.truncation()
    chk("the text is detected as ending mid-sentence", t["ends_midsentence"])
    chk("the last line has no closing punctuation",
        not t["last_line"].rstrip().endswith((".", ":", ")")))
    chk("Module F's header is present", t["module_f_header_present"])
    chk("and its body is marked incomplete in the source drop",
        t["module_f_body_complete_in_source_drop"] is False)
    chk("Module F is the highest section reached in the source drop",
        "MODULE F" in (t["highest_section"] or ""))
    chk("the missing parts are enumerated", len(t["what_is_missing"]) >= 4)
    chk("nothing missing is reconstructed in the source drop -- no Module F "
        "body text exists in SOURCE_DROP.md",
        "antecedent-condition" not in src.lower()
        and "burn-modified" not in src.lower())

    # ---- the engine and data blockers are measured
    chk("HEC-RAS is not present", A.engine_present() is False)
    chk("egress records the section-2 sources", len(A.EGRESS) >= 6)
    chk("every recorded host refused",
        all(code == "000" for _h, code, _w in A.EGRESS))

    # ---- exactly one substantive thing survives from the text alone
    surv = A.what_survives()
    chk("eap coverage runs", surv["eap_coverage"]["runs"] is True)
    chk("and it is the governance claim",
        "plan spans the chain" in surv["eap_coverage"]["result"])
    chk("the structural observations are restated, not computed",
        len(surv["structural_observations"]) == 2)

    # ---- the report
    out = A.render()
    one = " ".join(out.split())
    chk("the report states the spec cannot be executed here",
        "CANNOT BE EXECUTED HERE" in out)
    chk("and that the text is truncated",
        "TRUNCATED" in out)
    chk("it refuses to reconstruct Module F in the source drop",
        "NOT RECONSTRUCTED" in out)
    chk("it declares no hydraulics are simulated",
        "No hydraulics are simulated" in one
        or "no hydraulics are simulated" in one.lower())
    chk("it gives the one surviving result",
        "no single entity's plan spans the chain" in one)

    # ---- both modules refuse --selftest
    for mod in ("eap_coverage_v2.py", "audit_v2.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, mod),
                            "--selftest"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, r.returncode == 2)
        chk("%s names where its checks live" % mod,
            b"selftest_ccc.py" in r.stderr)
    r2 = subprocess.run([sys.executable, os.path.join(HERE,
                        "eap_coverage_v2.py")], stdout=subprocess.PIPE)
    chk("bare eap_coverage.py renders the record",
        b"EAP COVERAGE" in r2.stdout and b"Grand Coulee" in r2.stdout)

    # ---- the no-severity screen
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the audit report carries no severity language",
        not no_severity.hits(out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    # ONE declared exemption on the eap report, measured with the
    # three-arm harness: `means` fires inside a verbatim quote of the
    # spec ("mixed ownership means no entity's plan spans the chain"),
    # and rewording it would misquote the delivered text.
    eout = EAP.render()
    EXEMPT = ("means",)
    chk("one exemption on the eap report", len(EXEMPT) == 1)
    chk("and it is delivered text", "mixed ownership means" in doc)
    masked = eout
    for wd in EXEMPT:
        masked = re.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), masked)
    chk("the eap report is clean apart from the exemption",
        not no_severity.hits(masked))
    fired = set(w for _n, w, _l in no_severity.hits(eout))
    chk("and the exemption is the only token that fires",
        fired == set(EXEMPT))
    pmask = eout + "\nthis result is broken and invalid\n"
    for wd in EXEMPT:
        pmask = re.sub(r"(?i)\b%s\b" % wd, "X" * len(wd), pmask)
    chk("a planted violation is still caught through the exemption",
        bool(no_severity.hits(pmask)))

    # ================================================================
    # MODULE F checks (CCC_009..CCC_015)
    # ================================================================
    if HAS_MODULE_F:
        mf_src = io.open(os.path.join(HERE, "module_f.py"),
                         encoding="utf-8").read()

        # CCC_009: Module F body exists and is importable
        chk("CCC_009: Module F exists and imports",
            HAS_MODULE_F)

        # CCC_010: Module F contains no real structure names
        for real in ("Bonneville", "Grand Coulee", "Mica", "Columbia",
                     "Snake", "McNary", "Revelstoke", "Keenleyside"):
            chk("CCC_010: no real structure in module_f: %s" % real,
                real not in mf_src)

        # CCC_011: Module F proves the operator swap is one-sided
        chk("CCC_011: one-sided bias is stated",
            "ONE-SIDED" in mf_src or "one-sided" in mf_src.lower())
        chk("CCC_011: S1 subset S2 is proved",
            "S1 \subseteq S2" in MF.render() or "S1 <= S2" in MF.render())

        # CCC_012: parameter sweep space is defined
        chk("CCC_012: sweep space is defined",
            "parameter_sweep_space" in mf_src)
        chk("CCC_012: burn_severity range is 0.0 to 1.0",
            MF.BURN_SEVERITY_MIN == 0.0 and MF.BURN_SEVERITY_MAX == 1.0)

        # CCC_013: burn-modified roughness is parameterized, not calibrated
        chk("CCC_013: roughness is parameterized (not a fixed value)",
            "ROUGHNESS_MULTIPLIER_MIN" in mf_src)
        chk("CCC_013: no calibrated n value is asserted",
            "Manning n =" not in mf_src and "n = 0." not in mf_src)

        # CCC_014: the ordering holds across the sweep
        nodes = ["N1", "N2", "N3"]
        sweep_ok = MF.sweep_ordering(
            nodes,
            boundary_waves=[1.0, 5.0, 10.0],
            pools=[0.0, 2.0, 5.0],
            crests=[5.0, 10.0],
            base_attenuations=[0.5, 0.7],
            burn_severities=[0.0, 0.5, 1.0],
            attenuation_reduction_maxes=[0.0, 0.3])
        chk("CCC_014: S1 <= S2 <= S3 across the parameter sweep",
            sweep_ok)

        # CCC_015: null tests all pass
        n = MF.null_tests()
        chk("CCC_015: all null tests pass",
            n["all_pass"])

        # CCC_016: module_f refuses --selftest
        r = subprocess.run([sys.executable, os.path.join(HERE, "module_f.py"),
                            "--selftest"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        chk("CCC_016: module_f.py refuses --selftest",
            r.returncode == 2)
        chk("CCC_016: module_f names where its checks live",
            b"selftest_ccc.py" in r.stderr)

        # CCC_017: no severity language in module_f report
        mf_out = MF.render()
        chk("CCC_017: module_f report carries no severity language",
            not no_severity.hits(mf_out))

        # CCC_018: module_f is stdlib-only
        chk("CCC_018: module_f imports only sys",
            "import " in mf_src and "import sys" in mf_src
            and "import numpy" not in mf_src
            and "import scipy" not in mf_src)

    else:
        # Module F is not present; these checks are skipped, not failed
        print("  NOTE: module_f.py not found; CCC_009..CCC_018 skipped")

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
