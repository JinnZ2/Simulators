#!/usr/bin/env python3
"""S3 bindings -- which artifact each extracted claim is about.

DECLARED, never inferred. `extract.py` finds a claim by pattern; this
file says what would settle it. The mapping from "247 selftest checks
green across nine modules" to a list of nine paths is a judgement, and
a scanner that guessed it would be reporting its own guess.

An unbound claim is UNBOUND, which is a state. A claim whose subject is
not in the tree is NOT_TESTABLE with the reason named, which is a
different state, and the difference matters here: a large share of this
file's IDENTITY claims are about files delivered in a drop, checked at
the time, and never committed. Those are not divergences and they are
not oversights either.

Key format: "<section title>|<pattern>|<value or ->|<nth>", where nth
counts repeats of that exact triple inside the section, in file order.

DEPS is per item, per WO10 S7. `stdlib` means the scanner alone;
anything else names what must be importable for the check to run, and a
missing one is NOT_TESTABLE with that name in the reason.

CC0. stdlib only. Parses under Python 3.9.
"""

# how:
#   pytest      run pytest on `path`, compare passed (+skipped) counts
#   selftest    run `cmd`, parse a count out of stdout with `parse`
#   selftest_sum  run each of `cmds`, sum the parsed counts
#   diff_tree   byte-compare two path sets already in the tree
#   run_twice   run `cmd` twice, compare stdout bytes
#   run_grep    run `cmd`, require every string in `needles` in stdout
#   git_diff    compare a path against an earlier revision of itself
#   count_files count files under `path` matching `glob`
#   none        not testable; `reason` says why

BINDINGS = {

    # ---- COUNT: pytest suites ------------------------------------
    "thermal-sensor-degradation-audit/|tests_green|23|0": {
        "how": "pytest", "path": "thermal-sensor-degradation-audit",
        "deps": ["pytest"],
    },
    "grounding-layers/|tests_green|430|0": {
        "how": "pytest", "path": "grounding-layers",
        "deps": ["pytest", "numpy", "scipy", "matplotlib", "psutil"],
        "bound": True,
    },
    "fourd-municipal-engine-v2/|pass_skip|40/2|0": {
        "how": "pytest", "path": "fourd-municipal-engine-v2",
        "deps": ["pytest"], "expect_skipped": True,
    },
    "gdprf-framework/|tests_green|23|0": {
        "how": "pytest", "path": "gdprf-framework",
        "deps": ["pytest", "jsonschema"],
    },
    "msiaf-gdprf-bridge/|tests_green|7|0": {
        "how": "pytest", "path": "msiaf-gdprf-bridge",
        "deps": ["pytest"],
    },
    "proxy-investigation-lab/|tests_green|13|0": {
        "how": "pytest", "path": "proxy-investigation-lab",
        "deps": ["pytest", "numpy"],
    },
    "instrument-epistemology/|tests_green|9|0": {
        "how": "pytest", "path": "instrument-epistemology",
        "deps": ["pytest", "numpy"],
    },
    "reasoning-gate/|tests_green|46|0": {
        "how": "none",
        "reason": "SUPERSEDED_IN_THE_SAME_SECTION -- the section states 46 "
                  "and then states 69 later for the same suite. The 46 is "
                  "the count at an earlier drop, left in place as the "
                  "record of that drop.",
    },
    "reasoning-gate/|tests_green|69|0": {
        "how": "pytest", "path": "reasoning-gate", "deps": ["pytest"],
    },
    "instrument-bias-sims/|tests_green|197|0": {
        "how": "selftest_sum", "glob": "instrument-bias-sims/*.py",
        "parse": "checks", "deps": ["stdlib"],
    },
    "notes/study_watch.py|tests_green|84|0": {
        "how": "pytest", "path": "tests", "deps": ["pytest"],
    },
    "sheet-structure-scan/|tests_green|247|0": {
        "how": "selftest_sum", "glob": "sheet-structure-scan/*.py",
        "parse": "checks", "deps": ["stdlib"],
    },

    # ---- COUNT: one module printing its own selftest count -------
    "uninstrumented/|selftest_ratio|14/14|0": {
        "how": "selftest", "cmd": ["uninstrumented/selfreport_probe.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "uninstrumented/|selftest_ratio|13/13|0": {
        "how": "selftest", "cmd": ["uninstrumented/acquiescence.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "uninstrumented/|selftest_ratio|13/13|1": {
        "how": "selftest",
        "cmd": ["uninstrumented/selection_cuts.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "uninstrumented/|selftest_ratio|25/25|0": {
        "how": "selftest",
        "cmd": ["uninstrumented/coupling_audit/provisioning.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "domain-ledger/|selftest_ratio|13/13|0": {
        "how": "selftest", "cmd": ["domain-ledger/ledger.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "domain-ledger/|selftest_ratio|14/14|0": {
        "how": "selftest", "cmd": ["domain-ledger/anchor.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "closure-cost/|selftest_ratio|15/15|0": {
        "how": "selftest", "cmd": ["closure-cost/closure.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "constraint-assembly/|selftest_ratio|18/18|0": {
        "how": "selftest", "cmd": ["constraint-assembly/assemble.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "adaptive-claim-loop/|selftest_ratio|39/39|0": {
        "how": "none",
        "reason": "SUPERSEDED_IN_THE_SAME_SECTION -- the section states 39 "
                  "and then 53 for the same module after a repair.",
    },
    "adaptive-claim-loop/|selftest_ratio|53/53|0": {
        "how": "selftest", "cmd": ["adaptive-claim-loop/adaptive_loop.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|15/15|0": {
        "how": "selftest", "cmd": ["simulation-hypothesis-budget/budget.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|13/13|0": {
        "how": "selftest",
        "cmd": ["simulation-hypothesis-budget/multiscale.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|17/17|0": {
        "how": "selftest",
        "cmd": ["simulation-hypothesis-budget/consequence_frame.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|16/16|0": {
        "how": "selftest",
        "cmd": ["simulation-hypothesis-budget/ladder_audit.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|18/18|0": {
        "how": "selftest",
        "cmd": ["simulation-hypothesis-budget/era_metaphor_audit.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|20/20|0": {
        "how": "selftest",
        "cmd": ["simulation-hypothesis-budget/earth_transitions.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "simulation-hypothesis-budget/|selftest_ratio|20/20|1": {
        "how": "selftest",
        "cmd": ["simulation-hypothesis-budget/scaling_classes.py"],
        "parse": "ratio", "deps": ["stdlib"],
    },
    "search-substitution/|selftest_ratio|23/23|0": {
        "how": "selftest_glob", "glob": "search-substitution/*.py",
        "parse": "ratio", "deps": ["stdlib"],
    },
    "notes/study_watch.py|selftest_checks|28|0": {
        "how": "selftest", "cmd": ["notes/check_uploads.py"],
        "parse": "checks", "deps": ["stdlib"],
    },
    "claim-record/|selftest_checks|93|0": {
        "how": "selftest_sum", "glob": "claim-record/*.py",
        "parse": "checks", "deps": ["stdlib"],
    },
    "residual-direction/|selftest_checks|49|0": {
        "how": "selftest_sum", "glob": "residual-direction/*.py",
        "parse": "checks", "deps": ["stdlib"],
    },
    "model-provenance/|selftest_checks|29|0": {
        "how": "selftest_sum", "glob": "model-provenance/*.py",
        "parse": "checks", "deps": ["stdlib"],
    },
    "fold-matrix/|selftest_checks|74|0": {
        "how": "selftest_sum", "glob": "fold-matrix/*.py",
        "parse": "checks", "deps": ["stdlib"],
    },

    # ---- COUNT: file counts --------------------------------------
    "relational/|files_total|15|0": {
        "how": "none",
        "reason": "SUPERSEDED_IN_THE_SAME_SECTION -- the section states 15 "
                  "files total and then 17 later, both as counts at the "
                  "time of a drop.",
    },
    "relational/|files_total|17|0": {
        "how": "count_files", "path": "relational", "glob": "*",
        "recursive": False, "deps": ["stdlib"],
    },

    # ---- IDENTITY -------------------------------------------------
    "relational/|byte_reproducible|-|0": {
        "how": "run_grep",
        "cmd": ["relational/council_of_protectors.py"],
        "needles": ["0.65", "0.12", "80"],
        "deps": ["stdlib"],
        "note": "council_of_protectors is stdlib; its sibling "
                "nurturing_environment imports numpy and matplotlib, so "
                "the two halves of one sentence have different deps.",
    },
    "relational/|byte_reproducible|-|1": {
        "how": "run_grep",
        "cmd": ["relational/nurturing_environment.py"],
        "needles": ["SOCIAL"],
        "deps": ["numpy", "matplotlib"],
    },
    "fourd-municipal-engine-v2/|byte_identical|-|0": {
        "how": "diff_tree",
        "a": "fourd-municipal-engine/fourd_municipal_engine",
        "b": "fourd-municipal-engine-v2/fourd_municipal_engine",
        "common_only": True, "deps": ["stdlib"],
    },
    "instrument-epistemology/|byte_identical|-|0": {
        "how": "none",
        "reason": "SUBJECT_NOT_IN_TREE -- the claim compares the printed "
                  "output BEFORE a repair against the output after it, and "
                  "the pre-repair file was never committed.",
    },
    "reasoning-gate/|regenerates_identically|-|0": {
        "how": "run_twice_regen",
        "cmd": ["reasoning-gate/make_docs.py"],
        "target": "reasoning-gate/GUARDS.md",
        "asserted_by": "tests/test_gate_drift.py",
        "deps": ["stdlib"],
    },
    "measurement-fork/|byte_identical|-|0": {
        "how": "none",
        "reason": "SUBJECT_NOT_IN_TREE -- the claim is about uploaded "
                  "copies compared at the time of a drop. The uploads were "
                  "not committed; the repo copies they were compared to "
                  "are here, the other side is not.",
    },
    "uninstrumented/|byte_identical|-|0": {
        "how": "none",
        "reason": "SUBJECT_NOT_IN_TREE -- re-delivery check against an "
                  "upload that was not committed.",
    },
    "uninstrumented/|byte_identical|-|1": {
        "how": "selftest_clean",
        "cmd": ["uninstrumented/playground/m1_shape_vs_claim/score_m1.py"],
        "deps": ["stdlib"],
        "note": "the claim is that M1's two arms are byte-identical by "
                "construction; the module's own selftest is what asserts "
                "it, so this resolves to whether that assertion runs.",
    },
    "criteria-drift/|byte_identical|-|0": {
        "how": "run_grep",
        "cmd": ["criteria-drift/drift_sign.py"],
        "needles": ["0.9000"],
        "deps": ["stdlib"],
    },
    "photoperiod-claim-harness/|byte_reproducible|-|0": {
        "how": "run_twice",
        "cmd": ["photoperiod-claim-harness/photoperiod_claim_harness.py",
                "run-all"],
        "deps": ["stdlib"],
    },
    "presented-binary/|byte_identical|-|0": {
        "how": "none",
        "reason": "SUBJECT_NOT_IN_TREE -- two uploaded copies compared to "
                  "each other and to the repo copy. Neither upload was "
                  "committed.",
    },
    "domain-ledger/|byte_identical|-|0": {
        "how": "git_diff",
        "path": "domain-ledger/ledger.py",
        "strip": "module_docstring",
        "deps": ["stdlib", "git"],
    },
    # ---- a claim this file QUOTES rather than asserts ------------
    "self-scan/|tests_green|430|0": {
        "how": "none",
        "reason": "QUOTED_NOT_ASSERTED -- this occurrence is inside the "
                  "self-scan paragraph discussing grounding-layers' claim, "
                  "not a claim about self-scan. The extractor matches "
                  "pattern, not attribution, so a claim under discussion "
                  "reads identically to one being made. Use-mention, the "
                  "UNI_009 / DF_010 shape, arriving in this scanner.",
    },

    "sheet-structure-scan/|byte_identical|-|0": {
        "how": "none",
        "reason": "SUBJECT_NOT_IN_TREE -- two of three uploaded candidate "
                  "workbooks compared to each other. No workbook binary is "
                  "committed in this repository by design.",
    },
}
