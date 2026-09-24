#!/usr/bin/env python3
# REBUILT 2026-09-22 from design recovered from session 2026-09-20
# transcript fragments. Original bytes lost.
#
# Smoke test for build_index.py. Fixture recovered from the original smoke
# test; every behavior the spec lists is asserted here, plus the override
# fallback and the nogit fingerprint, which the recovered fixture did not
# exercise.
#
# CC0. stdlib only. Parses under Python 3.9. ASCII.

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
sys.path.insert(0, FOLDER)

import build_index as bi  # noqa: E402

CHECKS = [0]
FAILED = []


def check(label, cond):
    CHECKS[0] += 1
    if not cond:
        FAILED.append(label)
        print("FAIL %s" % label)


def row_by_path(rows, path):
    for r in rows:
        if r["path"] == path:
            return r
    return None


def main():
    os.chdir(HERE)
    repos = ["fixture/simulators", "fixture/method-layer",
             "fixture/missing-repo", "fixture/empty-repo"]
    rows, repo_states, flags = bi.collect(repos)

    # ---- 1. the headered, GATE PASSED row -------------------------------
    pb = row_by_path(rows, "checks/presented_binary.py")
    check("presented_binary listed", pb is not None)
    check("presented_binary name", pb["name"] == "presented-binary")
    check("presented_binary input_shape",
          pb["input_shape"] == "DECISION|CLAIM")
    check("presented_binary shape is multi-valued",
          bi.shape_list(pb["input_shape"]) == ["DECISION", "CLAIM"])
    check("presented_binary catches",
          pb["catches"] == "second option absent from the ballot")
    check("presented_binary run_cost", pb["run_cost"] == "TRIVIAL")
    check("presented_binary run_basis from parentheses",
          pb["run_basis"] == "author-estimate")
    check("presented_binary status", pb["status"] == "OBSERVED")
    check("presented_binary gate", pb["gate"] == "PASSED")
    check("presented_binary id", pb["id"] ==
          "fixture/simulators:checks/presented_binary.py")
    check("presented_binary repo is the path as passed",
          pb["repo"] == "fixture/simulators")
    check("presented_binary no flags",
          not [f for f in flags if f[0] == pb["id"]])

    # ---- 2. the headered, GATE UNRUN row --------------------------------
    fa = row_by_path(rows, "checks/falsifier_audit.md")
    check("falsifier_audit listed", fa is not None)
    check("falsifier_audit headered (md uses the same comment char)",
          fa["name"] == "falsifier-audit")
    check("falsifier_audit gate UNRUN", fa["gate"] == "UNRUN")
    check("UNRUN is not FAILED", fa["gate"] != "FAILED")
    check("falsifier_audit run_cost", fa["run_cost"] == "CORPUS")
    check("falsifier_audit no flags",
          not [f for f in flags if f[0] == fa["id"]])

    # ---- 3. unheadered -> UNRATED, still listed -------------------------
    uh = row_by_path(rows, "checks/unheadered.py")
    check("unheadered still listed", uh is not None)
    check("unheadered name UNRATED", uh["name"] == "UNRATED")
    check("unheadered input_shape UNRATED", uh["input_shape"] == "UNRATED")
    check("unheadered catches UNRATED", uh["catches"] == "UNRATED")
    check("unheadered run_cost UNRATED", uh["run_cost"] == "UNRATED")
    check("unheadered run_basis empty", uh["run_basis"] == "")
    check("unheadered status UNRATED", uh["status"] == "UNRATED")
    check("unheadered gate defaults UNRUN", uh["gate"] == "UNRUN")
    check("unheadered load_bytes is the file size",
          uh["load_bytes"] ==
          str(os.path.getsize("fixture/simulators/checks/unheadered.py")))
    check("unheadered load_tok_est is bytes // 4",
          uh["load_tok_est"] == str(int(uh["load_bytes"]) // 4))
    check("unheadered UNRATED run_cost raises no run_basis flag",
          not [f for f in flags if f[0] == uh["id"]])

    # ---- 4. RUN-COST BOGUS -> flagged, value kept -----------------------
    bs = row_by_path(rows, "branch_set.py")
    check("branch_set listed", bs is not None)
    check("branch_set run_cost kept as BOGUS", bs["run_cost"] == "BOGUS")
    check("branch_set run_cost not normalized",
          bs["run_cost"] not in bi.RUN_COSTS)
    bs_flags = [f for f in flags if f[0] == bs["id"]]
    check("branch_set flagged", len(bs_flags) == 1)
    check("branch_set flag names run_cost", bs_flags[0][1] == "run_cost")
    check("branch_set flag did not alter the value",
          "BOGUS" in bs_flags[0][2] and bs["run_cost"] == "BOGUS")

    # ---- 5. missing repo -> NOT-SCANNED ---------------------------------
    miss = [r for r in repo_states if r["label"] == "fixture/missing-repo"][0]
    check("missing repo NOT-SCANNED", miss["state"] == bi.NOT_SCANNED)
    check("missing repo has no rows", miss["rows"] == [])
    check("missing repo built_against is NOT-SCANNED",
          miss["built_against"] == bi.NOT_SCANNED)

    # ---- 6. empty existing repo -> SCANNED, zero rows -------------------
    empt = [r for r in repo_states if r["label"] == "fixture/empty-repo"][0]
    check("empty repo SCANNED", empt["state"] == "SCANNED")
    check("empty repo has no rows", empt["rows"] == [])
    check("NOT-SCANNED and scanned-zero-rated are distinct states",
          miss["state"] != empt["state"])

    # ---- 7. override fallback and precedence ----------------------------
    ov = row_by_path(rows, "overridden.txt")
    check("override supplies a row for an unheadered file",
          ov["name"] == "overridden")
    check("override supplies input_shape", ov["input_shape"] == "NUMBER")
    check("override supplies run_cost", ov["run_cost"] == "EXTERNAL")
    check("override leaves gate at the UNRUN default", ov["gate"] == "UNRUN")
    check("in-file header wins over the override",
          bs["name"] == "branch-set" and bs["input_shape"] == "CATEGORY-SET")

    # ---- 8. all four flag conditions ------------------------------------
    reasons = [f[2] for f in flags]
    fields = [f[1] for f in flags]
    check("flag: input_shape outside the enum",
          any("WIDGET" in r for r in reasons))
    check("flag: run_cost outside the enum",
          any("BOGUS" in r for r in reasons))
    check("flag: run_cost rated with an empty run_basis",
          any("run_basis is empty" in r for r in reasons))
    check("flag: run_basis outside the enum",
          any("guesswork" in r for r in reasons))
    check("flags cover three fields",
          set(fields) == {"input_shape", "run_cost", "run_basis"})
    odd = row_by_path(rows, "odd_shape.sh")
    check("out-of-enum shape value kept", odd["input_shape"] == "WIDGET")
    check("out-of-enum basis value kept", odd["run_basis"] == "guesswork")
    check("EXTERNAL with no basis keeps the empty basis",
          ov["run_basis"] == "")

    # ---- 9. never drop a file -------------------------------------------
    walked = (len(bi.walk_repo("fixture/simulators"))
              + len(bi.walk_repo("fixture/method-layer"))
              + len(bi.walk_repo("fixture/empty-repo")))
    check("row count equals the walked file count", len(rows) == walked)
    check("SKIP_NAMES: index-overrides.json is not a row",
          row_by_path(rows, "index-overrides.json") is None)
    check("SKIP_NAMES: README.md is not a row",
          row_by_path(rows, "README.md") is None)
    check("empty repo walks to zero files",
          bi.walk_repo("fixture/empty-repo") == [])

    # ---- 10. axis check holds on this fixture ---------------------------
    verdict, rated, claim_only, frac = bi.axis_check(rows)
    check("axis: rated set is the non-UNRATED rows", rated == 5)
    check("axis: no claim-only row here", claim_only == 0)
    check("axis holds at this build", verdict == bi.AXIS_HOLDS)
    check("axis fraction is 0.0, not None", frac == 0.0)

    # ---- 11. planted CLAIM-only majority -> AXIS FALSIFIED --------------
    crows, _, _ = bi.collect(["fixture_claim/claimy"])
    cverdict, crated, cclaim, cfrac = bi.axis_check(crows)
    check("planted set is rated", crated == 4)
    check("planted claim-only count", cclaim == 3)
    check("planted fraction over the threshold",
          cfrac > bi.AXIS_THRESHOLD)
    check("AXIS FALSIFIED fires", cverdict == bi.AXIS_FALSIFIED)
    check("AXIS FALSIFIED names the fallback",
          "verdict/count/branch/refusal" in cverdict)

    # ---- 12. no rated rows -> check not run -----------------------------
    everdict, erated, eclaim, efrac = bi.axis_check([])
    check("no rated rows: check not run", everdict == bi.AXIS_UNRATED)
    check("no rated rows: fraction is None, not 0.0", efrac is None)
    check("claim_only_fraction None on an empty set",
          bi.claim_only_fraction([]) is None)
    check("claim_only_fraction 0.0 when rated and none claim-only",
          bi.claim_only_fraction(rows) == 0.0)
    check("claim_only_fraction 0.75 on the planted set",
          abs(bi.claim_only_fraction(crows) - 0.75) < 1e-12)

    # ---- 13. scrub -------------------------------------------------------
    check("tabs scrubbed to spaces", bi.scrub("a\tb") == "a b")
    check("newlines scrubbed to spaces", bi.scrub("a\nb") == "a b")
    check("scrub strips", bi.scrub("  a  ") == "a")

    # ---- 14. header parsing edges ---------------------------------------
    check("header stops at the first non-comment line",
          bi.parse_header("# INSTRUMENT: a\nx = 1\n# GATE: PASSED\n")
          == {"name": "a"})
    check("a blank line terminates the block",
          bi.parse_header("# INSTRUMENT: a\n\n# GATE: PASSED\n")
          == {"name": "a"})
    check("unknown header keys ignored",
          bi.parse_header("# NONSENSE: a\n") == {})
    check("run-cost parenthetical optional",
          bi.split_run_cost("TRIVIAL") == ("TRIVIAL", ""))
    check("run-cost parenthetical parsed",
          bi.split_run_cost("TRIVIAL (measured)")
          == ("TRIVIAL", "measured"))

    # ---- 15. built_against ----------------------------------------------
    check("built_against inside a git repo is a short hash",
          not pb["built_against"].startswith("nogit-")
          and pb["built_against"] != bi.NOT_SCANNED)
    tmp = tempfile.mkdtemp()
    with open(os.path.join(tmp, "a.py"), "w") as fh:
        fh.write("# INSTRUMENT: t\n# INPUT: CLAIM\n")
    trows, _, _ = bi.collect([tmp])
    check("built_against outside a git repo is a nogit fingerprint",
          trows[0]["built_against"].startswith("nogit-"))
    check("nogit fingerprint is ten hex characters",
          len(trows[0]["built_against"]) == len("nogit-") + 10)
    check("nogit fingerprint is stable across two reads",
          bi.fingerprint(tmp, ["a.py"]) == bi.fingerprint(tmp, ["a.py"]))

    # ---- 16. two renderings, one pass, via the CLI ----------------------
    out = tempfile.mkdtemp()
    tsv = os.path.join(out, "INSTRUMENT-INDEX.tsv")
    md = os.path.join(out, "INSTRUMENT-INDEX.md")
    proc = subprocess.run(
        [sys.executable, os.path.join(FOLDER, "build_index.py"),
         "--tsv", tsv, "--md", md] + repos,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check("cli exits 0", proc.returncode == 0)
    err = proc.stderr.decode("ascii", "replace")
    check("flags go to stderr", err.count("FLAG ") == len(flags))
    tsv_text = open(tsv).read()
    md_text = open(md).read()
    check("tsv says GENERATED", bi.GENERATED_NOTE in tsv_text)
    check("md says GENERATED", bi.GENERATED_NOTE in md_text)
    check("tsv header carries a stamp", "# stamp: " in tsv_text)
    check("tsv header carries repo states",
          tsv_text.count("# repo: ") == len(repos))
    check("tsv header carries the row count",
          "# rows: %d" % len(rows) in tsv_text)
    check("tsv header carries the estimate note",
          "ESTIMATE" in tsv_text)
    check("tsv header carries the axis-check", "# axis-check: " in tsv_text)
    check("tsv header carries the unrated count as a to-do",
          "to-do, located, not hidden" in tsv_text)
    check("tsv header carries total_load_tok_est",
          "# total_load_tok_est: %d" % bi.total_tok_est(rows) in tsv_text)
    check("tsv header carries the flag count",
          "# flags: %d" % len(flags) in tsv_text)
    lines = [ln for ln in tsv_text.splitlines() if not ln.startswith("#")]
    check("tsv FIELDS line is the 13 fields in order",
          lines[0].split("\t") == list(bi.FIELDS))
    check("tsv has one row per collected row", len(lines) - 1 == len(rows))
    check("tsv rows are in source order",
          [ln.split("\t")[3] for ln in lines[1:]]
          == [r["path"] for r in rows])
    check("md carries the flags, not stderr only",
          "BOGUS" in md_text and "WIDGET" in md_text)
    check("md states the threshold", "0.70" in md_text)
    check("md carries the axis verdict", bi.AXIS_HOLDS in md_text)
    check("md build state table has a row per repo",
          all(("| %s |" % r) in md_text for r in repos))
    check("md: NOT-SCANNED message",
          "Unknown contents, not an empty repo." in md_text)
    check("md: scanned-with-nothing-rated message",
          "Scanned, no rated instruments found (0 file(s) unrated)."
          in md_text)
    check("md: catches is the first column",
          "| catches | id |" in md_text)
    check("md: unrated set is a located to-do list",
          uh["id"] in md_text and "To-do, located, not hidden" in md_text)
    check("md: coverage declaration template present",
          all(line in md_text for line in bi.COVERAGE_DECLARATION))
    check("md: built_against states line", "built_against states:" in md_text)
    check("md: repos sorted by load cost descending",
          md_text.index("### fixture/simulators")
          < md_text.index("### fixture/method-layer"))
    check("md: NOT-SCANNED repo sorts last",
          md_text.index("### fixture/missing-repo")
          > md_text.index("### fixture/empty-repo"))
    check("neither rendering is derived from the other: same id set",
          set(r["id"] for r in rows)
          == set(ln.split("\t")[0] for ln in lines[1:]))

    # ---- 17. planted majority through the CLI ---------------------------
    tsv2 = os.path.join(out, "claim.tsv")
    md2 = os.path.join(out, "claim.md")
    proc2 = subprocess.run(
        [sys.executable, os.path.join(FOLDER, "build_index.py"),
         "--tsv", tsv2, "--md", md2, "fixture_claim/claimy"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check("planted cli exits 0", proc2.returncode == 0)
    check("AXIS FALSIFIED reaches the tsv",
          "AXIS FALSIFIED" in open(tsv2).read())
    check("AXIS FALSIFIED reaches the md",
          "AXIS FALSIFIED" in open(md2).read())

    # ---- 18. house conventions ------------------------------------------
    proc3 = subprocess.run(
        [sys.executable, os.path.join(FOLDER, "build_index.py"),
         "--selftest"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check("--selftest refused with exit 2", proc3.returncode == 2)
    check("--selftest names the test file",
          "test_build_index.py" in proc3.stderr.decode("ascii", "replace"))
    proc4 = subprocess.run(
        [sys.executable, os.path.join(FOLDER, "build_index.py")],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check("no arguments prints usage and exits 2",
          proc4.returncode == 2
          and "usage:" in proc4.stderr.decode("ascii", "replace"))
    for name in ("build_index.py", "tests/test_build_index.py"):
        data = open(os.path.join(FOLDER, name), "rb").read()
        check("%s is ascii" % name, all(b < 128 for b in data))
    spec = open(os.path.join(FOLDER, "INDEX-SPEC.md"), "rb").read().decode(
        "utf-8")
    label = ("REBUILT 2026-09-22 from design recovered from session "
             "2026-09-20 transcript fragments. Original bytes lost. "
             "Sections marked [RECOVERED] match recovered text; sections "
             "marked [REBUILD-CHOICE] are new.")
    flat = " ".join(spec.split())
    check("spec carries the rebuild label", label in flat)
    code = open(os.path.join(FOLDER, "build_index.py")).read()
    decommented = " ".join(
        " ".join(ln.lstrip().lstrip("#").split())
        for ln in code.splitlines())
    check("build_index carries the rebuild label",
          label in " ".join(decommented.split()))
    check("spec keeps the estimate note",
          "An estimate labeled as an estimate is usable" in flat)
    check("spec keeps the drift note",
          "If the two files differ, regenerate" in flat)
    check("spec marks the coverage declaration replaceable",
          "replaceable when the original turns up" in flat.lower())

    print("")
    print("checks: %d   failed: %d" % (CHECKS[0], len(FAILED)))
    for name in FAILED:
        print("  - %s" % name)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
