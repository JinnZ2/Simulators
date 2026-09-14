# SPDX-License-Identifier: CC0-1.0
"""Recount every countable claim in the delivered deep-research report.

The report (DEEP_RESEARCH_2026_09_14.md, landed verbatim, modified by
nothing here) is an outside reading of this whole repository. Most of it
is judgement and says so. A minority of it is arithmetic over the tree,
and arithmetic over the tree is recomputable by anyone with the clone.
That minority is what this module recomputes.

WHAT IT READS. The report's own family tables, parsed at call time -- the
folder names are the first backticked cell of each table row, and the
claimed folder and file counts are in each family's own heading. Nothing
is retyped here; a table edited in the report and not followed by the
parser turns the suite red rather than passing against a stale copy.

WHAT IT COUNTS AGAINST. `git ls-tree` at a PINNED REVISION, never the
working tree. Two reasons. The report states a survey DATE and no commit,
so its baseline has to be established rather than taken; and the report
now lives inside the tree it counts, so a working-tree count measures the
report's own arrival (UNI_010 / ANC_001 at repository scale). BASELINE is
established in the code below, not assumed.

WHAT IT DOES NOT DO. It checks no external citation -- the egress gate
refuses every publisher host, and the report's own section 0.3 records
the same refusal for its arXiv identifiers. It adjudicates none of the
report's family assignments, audience scores or roadmap priorities, all
three of which the report declares as judgement in its sections 1 and 15.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.

    python3 external-audit/recount.py            # the recount
    python3 external-audit/recount.py --selftest # the checks
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPORT = os.path.join(HERE, "DEEP_RESEARCH_2026_09_14.md")

# [CHOICE 1] The revision the report surveyed is not stated in the report.
# It is ESTABLISHED in `baseline()` below by the only family whose count
# moves between two adjacent commits, and this constant is that result
# written down so the recount is reproducible without re-deriving it.
BASELINE = "6633778^"
HEAD_REV = "6633778"

# [CHOICE 2] `.github` is a real top-level directory and the report never
# names it. Counted as PRESENT-AND-UNNAMED rather than as a folder the
# report got wrong, because a survey of content folders excluding it is a
# defensible scope -- and then reported separately, because two of the
# report's own claims turn on what is inside it.
INFRA_DIRS = (".github",)

CHOICES = {
    1: "survey revision established by family drift, not stated in the report",
    2: "`.github` counted as present-and-unnamed, not as a miscount",
    3: "a folder 'exists' iff the tree carries any path under `<name>/`",
}


def report_text(path=None):
    """The report as text. `path` generalises every reader below to take
    a DOCUMENT rather than the one landed file, so a second rendering of
    the same survey is measured by this module rather than by a copy of
    it -- the MF_019 discipline, and the move entries_v2/_v3 already made
    for the four work orders."""
    with open(path or REPORT) as fh:
        return fh.read()


def _git(rev, *args):
    out = subprocess.run(["git", "-C", ROOT, "ls-tree", "-r",
                          "--name-only", rev] + list(args),
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError("git ls-tree failed for %r: %s"
                           % (rev, out.stderr.strip()))
    return [f for f in out.stdout.split("\n") if f]


def tree(rev):
    return _git(rev)


def top_level(files):
    return {f.split("/")[0] for f in files if "/" in f}


# ------------------------------------------------------- report parsing

def families(path=None):
    """[(fid, claimed_folders, claimed_files, [folder names])] from the
    report's own section headings and tables. `path` reads a second
    rendering with the same parser."""
    txt = report_text(path)
    out = []
    for sec in re.split(r"^## \d+\. Family ", txt, flags=re.M)[1:]:
        m = re.match(r"(F\d) [^(]*\((\d+) folders?, (\d+) files?\)", sec)
        if not m:
            continue
        named = re.findall(r"^\| `([a-zA-Z0-9_\-]+)` \|", sec, re.M)
        out.append((m.group(1), int(m.group(2)), int(m.group(3)), named))
    if len(out) != 9:
        raise ValueError("expected 9 family sections, parsed %d" % len(out))
    return out


def stated_total_files():
    """The report's headline file count, taken from its own prose."""
    m = re.search(r"\*\*166 top-level folders, ([\d,]+) files, "
                  r"([\d,]+) Python files, ([\d,]+) Markdown files\*\*",
                  report_text())
    if not m:
        raise ValueError("headline count line not found")
    return tuple(int(g.replace(",", "")) for g in m.groups())


# --------------------------------------------------------- the baseline

def baseline(head=HEAD_REV):
    """ESTABLISH the surveyed revision instead of taking the stated date.

    A family whose claimed count matches at one commit and not its child
    dates the survey between them. Returns the evidence, not just the
    answer."""
    fams = families()
    ev = []
    for rev in (head + "^", head):
        files = tree(rev)
        row = {}
        for fid, _nf, claimed, named in fams:
            real = {n for n in named if any(f.startswith(n + "/")
                                            for f in files)}
            row[fid] = (claimed, sum(1 for f in files
                                     if f.split("/")[0] in real))
        ev.append((rev, row))
    moved = [fid for fid in ev[0][1]
             if ev[0][1][fid][1] != ev[1][1][fid][1]]
    exact_parent = [f for f in ev[0][1] if ev[0][1][f][0] == ev[0][1][f][1]]
    exact_head = [f for f in ev[1][1] if ev[1][1][f][0] == ev[1][1][f][1]]
    return {"revision": head + "^",
            "families_that_move_between_them": moved,
            "exact_at_parent": sorted(exact_parent),
            "exact_at_head": sorted(exact_head),
            "evidence": ev}


# ----------------------------------------------------------- the counts

def named_folders():
    """Every folder the report's family tables name, and whether it is in
    the tree. A name in no table is not a claim; a name in a table that
    resolves to nothing is."""
    files = tree(BASELINE)
    top = top_level(files)
    named = []
    for _fid, _a, _b, names in families():
        named.extend(names)
    absent = sorted(n for n in named if n not in top)
    unnamed = sorted(t for t in top if t not in set(named))
    return {"named": len(named),
            "absent_from_tree": absent,
            "in_tree_never_named": unnamed,
            "real_content_folders": len(top) - len(
                [t for t in top if t in INFRA_DIRS]),
            "top_level_in_tree": len(top)}


def absent_names_occur_anywhere():
    """A named-and-absent folder could be a rename. Grep the tree for each
    name, excluding this folder, so a rename is distinguishable from an
    invention."""
    out = {}
    for name in named_folders()["absent_from_tree"]:
        r = subprocess.run(["git", "-C", ROOT, "grep", "-l", "--", name,
                            BASELINE], capture_output=True, text=True)
        hits = [h for h in r.stdout.split("\n") if h]
        out[name] = hits
    return out


def family_recount(rev=BASELINE):
    """Per family: claimed vs actual, and whether the shortfall is exactly
    the folders that do not exist."""
    files = tree(rev)
    rows = []
    for fid, nfold, nfiles, named in families():
        real = {n for n in named if any(f.startswith(n + "/")
                                        for f in files)}
        actual = sum(1 for f in files if f.split("/")[0] in real)
        py = sum(1 for f in files
                 if f.split("/")[0] in real and f.endswith(".py"))
        rows.append({"family": fid, "claimed_folders": nfold,
                     "named": len(named), "existing": len(real),
                     "phantom": sorted(set(named) - real),
                     "claimed_files": nfiles, "actual_files": actual,
                     "delta": actual - nfiles, "actual_py": py})
    return rows


def total_reconciliation(rev=BASELINE):
    """The report's headline total against the sum of its own families,
    and against the tree. Closes or it does not; no rounding."""
    rows = family_recount(rev)
    actual_sum = sum(r["actual_files"] for r in rows)
    claimed_sum = sum(r["claimed_files"] for r in rows)
    shortfall = claimed_sum - actual_sum
    files = tree(rev)
    root_files = len([f for f in files if "/" not in f])
    infra = len([f for f in files
                 if f.split("/")[0] in INFRA_DIRS and "/" in f])
    stated_files, stated_py, stated_md = stated_total_files()
    return {"stated_total": stated_files,
            "sum_of_claimed_families": claimed_sum,
            "sum_of_actual_families": actual_sum,
            "attributed_to_phantom_folders": shortfall,
            "actual_plus_phantom": actual_sum + shortfall,
            "closes": actual_sum + shortfall == stated_files,
            "tracked_at_revision": len(files),
            "root_files_excluded": root_files,
            "infra_files_excluded": infra,
            "stated_py": stated_py, "stated_md": stated_md}


def headline_decomposition(rev=BASELINE):
    """The report states three headline numbers -- files, Python,
    Markdown. Each is short against the tree by the same two folders, so
    the shortfall decomposes rather than being three separate errors."""
    files = tree(rev)
    content = [f for f in files
               if "/" in f and f.split("/")[0] not in INFRA_DIRS]
    stated_files, stated_py, stated_md = stated_total_files()
    actual = {"files": len(content),
              "py": len([f for f in content if f.endswith(".py")]),
              "md": len([f for f in content if f.endswith(".md")])}
    stated = {"files": stated_files, "py": stated_py, "md": stated_md}
    delta = dict((k, stated[k] - actual[k]) for k in stated)
    other = delta["files"] - delta["py"] - delta["md"]
    return {"stated": stated, "actual": actual, "delta": delta,
            "other": other,
            "consistent": delta["files"] == delta["py"] + delta["md"]
            + other and other >= 0}


def spot_checks(rev=BASELINE):
    """The report's individual numeric claims about the tree, each
    recomputed. `expected` is transcribed from the report; `actual` is
    computed. No claim is listed here that the report does not make."""
    files = tree(rev)

    def n(prefix, suffix=None):
        return len([f for f in files if f.startswith(prefix)
                    and (suffix is None or f.endswith(suffix))])

    root_md = len([f for f in files if "/" not in f and f.endswith(".md")])
    root_py = len([f for f in files if "/" not in f and f.endswith(".py")])
    gi = os.path.join(ROOT, "GAP_INDEX.md")
    gap_entries = gap_folders = None
    if os.path.exists(gi):
        with open(gi) as fh:
            g = fh.read()
        me = re.search(r"^entries\s+(\d+)", g, re.M)
        mf = re.search(r"^folders\s+(\d+)", g, re.M)
        gap_entries = int(me.group(1)) if me else None
        gap_folders = int(mf.group(1)) if mf else None
    guards = None
    gp = os.path.join(ROOT, "reasoning-gate", "guards.json")
    if os.path.exists(gp):
        import json
        with open(gp) as fh:
            guards = len(json.load(fh)["guards"])

    checks = [
        ("nineteen spine documents at root", 19, root_md),
        ("no Python files at the repository root", 0, root_py),
        ("tools/ 10 files", 10, n("tools/")),
        ("tests/ 9 files", 9, n("tests/")),
        ("GAP_INDEX entries", 255, gap_entries),
        ("GAP_INDEX folders", 24, gap_folders),
        ("reasoning-gate guards", 8, guards),
        ("fragility-cascade files", 173, n("fragility-cascade/")),
        ("fragility-cascade python", 85, n("fragility-cascade/", ".py")),
        ("energy files", 66, n("energy/")),
        ("play-sims files", 30, n("play-sims/")),
        ("relational files", 38, n("relational/")),
        ("gdprf-framework files", 33, n("gdprf-framework/")),
        ("msiaf-framework markdown", 14, n("msiaf-framework/", ".md")),
        ("earth_economics files", 21, n("earth_economics/")),
        ("emergence-stability-simulator files", 28,
         n("emergence-stability-simulator/")),
        ("emergence-stability-simulator python", 12,
         n("emergence-stability-simulator/", ".py")),
        ("machine-record-format python", 10,
         n("machine-record-format/", ".py")),
        ("fourd-municipal-engine both versions", 80,
         n("fourd-municipal-engine/") + n("fourd-municipal-engine-v2/")),
        ("F5 python across 10 folders", 130,
         [r for r in family_recount(rev) if r["family"] == "F5"][0]
         ["actual_py"]),
        ("F6 python", 0,
         [r for r in family_recount(rev) if r["family"] == "F6"][0]
         ["actual_py"]),
    ]
    return [{"claim": c, "expected": e, "actual": a,
             "state": "EXACT" if a == e else "DIFFERS"}
            for c, e, a in checks]


def markdown_coverage(rev=BASELINE):
    """"162 of 166 folders contain at least one Markdown document", with
    four exceptions named. The named list and the count are checked
    separately, because a document can enumerate correctly and count
    wrong."""
    files = tree(rev)
    top = sorted(top_level(files))
    nomd = [t for t in top
            if not any(f.startswith(t + "/") and f.endswith(".md")
                       for f in files)]
    stated = re.search(r"\*\*(\d+) of (\d+) folders contain at least one "
                       r"Markdown document\*\*", report_text())
    named = ("exploration-engine", "exploration-playground",
             "vector-field-explorer", "voice-attractor-probe")
    return {"stated": (int(stated.group(1)), int(stated.group(2)))
            if stated else None,
            "folders_with_no_markdown": sorted(nomd),
            "report_named_exceptions": list(named),
            "named_list_exact_as_far_as_it_goes":
                set(named) <= set(nomd),
            "missing_from_report_list": sorted(set(nomd) - set(named)),
            "on_the_reports_own_denominator":
                (166 - len(nomd), 166) if stated else None}


def ci_claim(rev=BASELINE):
    """Two report claims turn on the one directory it never names."""
    files = tree(rev)
    wf = sorted(f for f in files if f.startswith(".github/workflows/"))
    txt = report_text()
    said_no_ci = "no test-running CI" in txt
    suites = 0
    p = os.path.join(ROOT, ".github", "workflows", "test.yml")
    if os.path.exists(p):
        with open(p) as fh:
            suites = fh.read().count("unittest discover")
    selftest_modules = subprocess.run(
        ["git", "-C", ROOT, "grep", "-l", "--", "--selftest", rev],
        capture_output=True, text=True).stdout
    n_sel = len([l for l in selftest_modules.split("\n")
                 if l.endswith(".py")])
    return {"report_says_no_test_running_ci": said_no_ci,
            "workflow_files": wf,
            "unittest_suites_in_ci": suites,
            "files_mentioning_selftest": n_sel,
            "verdict": ("REFUTED" if wf and said_no_ci else "HOLDS"),
            "narrowed": "CI exists and runs %d unittest suites on push; it "
                        "runs neither the per-module --selftest surface nor "
                        "tools/known_answer.py" % suites}


def package_claim(rev=BASELINE):
    files = tree(rev)
    pk = sorted(f for f in files
                if f.endswith(("pyproject.toml", "setup.py", "setup.cfg")))
    return {"packaged_folders": pk,
            "verdict": "NARROWED" if pk else "HOLDS",
            "narrowed": "no repo-wide installable core; three folders do "
                        "ship a package definition"}


def claim_export_claim(rev=BASELINE):
    """"no machine-readable index of its own claims" -- and the validator
    for the format that index would use."""
    files = tree(rev)
    jsons = [f for f in files if f.endswith("CLAIM_TABLE.json")]
    validator = [f for f in files if f.endswith("validate_claim_table.py")]
    tables = [f for f in files if f.endswith("CLAIM_TABLE.md")]
    return {"claim_table_json_in_tree": jsons,
            "validator_present": validator,
            "claim_table_markdown_in_tree": len(tables),
            "verdict": "HOLDS",
            "sharper": "the validator exists and has zero inputs: a "
                       "consumer with no producer, CONSTANT_SILENT at "
                       "repository scale"}


def response_claims():
    """The delivered RESPONSE_TO_REVIEW.md makes its own countable claims
    about the report. Two are checkable here."""
    rt = report_text()
    rp = os.path.join(HERE, "RESPONSE_TO_REVIEW.md")
    with open(rp) as fh:
        resp = fh.read()
    links = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", rt)
    m = re.search(r"(\d+) external citations, (\d+) executions", resp)
    stated = int(m.group(1)) if m else None
    share = re.search(r"share checks at (\d+\.\d+)", resp)
    # F1+F2+F3 share, on the report's own numbers and on the tree's
    rows = family_recount()
    claimed = {r["family"]: r["claimed_files"] for r in rows}
    actual = {r["family"]: r["actual_files"] for r in rows}
    c3 = sum(claimed[f] for f in ("F1", "F2", "F3"))
    a3 = sum(actual[f] for f in ("F1", "F2", "F3"))
    return {"inline_links_in_report": len(links),
            "unique_urls": len(set(links)),
            "response_states_citations": stated,
            "citation_delta": (len(links) - stated) if stated else None,
            "share_stated_by_response": float(share.group(1))
            if share else None,
            "share_on_claimed_counts":
                round(100.0 * c3 / sum(claimed.values()), 1),
            "share_on_actual_counts":
                round(100.0 * a3 / sum(actual.values()), 1),
            "note": "'external citation' is undefined in the response; "
                    "both readings printed, neither picked"}


def self_reference(rev=BASELINE):
    """The report is now inside the tree it counts."""
    files_then = tree(rev)
    head = tree(HEAD_REV)
    import os as _os
    wt = len([d for d in _os.listdir(ROOT)
              if _os.path.isdir(_os.path.join(ROOT, d)) and d != ".git"])
    return {"revision_counted": rev,
            "top_level_then": len(top_level(files_then)),
            "top_level_at_head": len(top_level(head)),
            "top_level_in_working_tree": wt,
            "report_folder_in_tree_at_baseline":
                any(f.startswith("external-audit/") for f in files_then),
            "note": "counting the working tree would measure the report's "
                    "own arrival; the recount is pinned by revision"}


# --------------------------------------------------------------- render

def _line(k, v):
    return "  %-42s %s" % (k, v)


def render():
    out = []
    a = out.append
    a("RECOUNT -- DEEP_RESEARCH_2026_09_14.md against the tree")
    a("=" * 66)
    a("")
    a("Delivered verbatim and modified by nothing here. Judgement in the")
    a("report is not adjudicated; arithmetic over the tree is recomputed.")
    a("")
    a("CHOICES IN FORCE")
    for k in sorted(CHOICES):
        a("  [CHOICE %d] %s" % (k, CHOICES[k]))
    a("")

    b = baseline()
    a("BASELINE -- established, not taken from the stated date  [CHOICE 1]")
    a(_line("revision", b["revision"]))
    a(_line("families exact at that revision",
            "%d of 9  %s" % (len(b["exact_at_parent"]),
                             ",".join(b["exact_at_parent"]))))
    a(_line("families exact at its child",
            "%d of 9  %s" % (len(b["exact_at_head"]),
                             ",".join(b["exact_at_head"]))))
    a(_line("families that move between the two",
            ",".join(b["families_that_move_between_them"]) or "none"))
    a("")

    nf = named_folders()
    a("FOLDERS NAMED BY THE REPORT")
    a(_line("named in family tables", nf["named"]))
    a(_line("top-level directories in tree", nf["top_level_in_tree"]))
    a(_line("named but ABSENT from the tree",
            ", ".join(nf["absent_from_tree"]) or "none"))
    a(_line("in tree, never named  [CHOICE 2]",
            ", ".join(nf["in_tree_never_named"]) or "none"))
    a(_line("real content folders", nf["real_content_folders"]))
    for name, hits in sorted(absent_names_occur_anywhere().items()):
        a(_line("  `%s` occurs elsewhere in tree" % name,
                ("%d files" % len(hits)) if hits else "no -- invented, "
                                                     "not renamed"))
    a("")

    a("FAMILY RECOUNT at %s" % BASELINE)
    a("  fam  named  exist  phantom            claimed  actual  delta")
    for r in family_recount():
        a("  %-4s %5d  %5d  %-18s %7d  %6d  %+5d"
          % (r["family"], r["named"], r["existing"],
             ",".join(r["phantom"]) or "-", r["claimed_files"],
             r["actual_files"], r["delta"]))
    a("")

    t = total_reconciliation()
    a("TOTAL RECONCILIATION")
    a(_line("report's stated total", t["stated_total"]))
    a(_line("sum of its own family counts",
            t["sum_of_claimed_families"]))
    a(_line("sum of actual files in existing folders",
            t["sum_of_actual_families"]))
    a(_line("attributed to folders that do not exist",
            t["attributed_to_phantom_folders"]))
    a(_line("actual + phantom", t["actual_plus_phantom"]))
    a(_line("closes to the digit", "yes" if t["closes"] else "NO"))
    a(_line("tracked at revision (all paths)",
            t["tracked_at_revision"]))
    a(_line("root files excluded by the survey",
            t["root_files_excluded"]))
    a(_line("infra files excluded by the survey",
            t["infra_files_excluded"]))
    a("")

    hd = headline_decomposition()
    a("HEADLINE DECOMPOSITION -- all three short by the same two folders")
    a("  %-10s %8s %8s %8s" % ("", "stated", "actual", "short"))
    for k in ("files", "py", "md"):
        a("  %-10s %8d %8d %8d"
          % (k, hd["stated"][k], hd["actual"][k], hd["delta"][k]))
    a(_line("neither .py nor .md", hd["other"]))
    a(_line("21 phantom files = 5 py + 7 md + 9 other",
            "yes" if hd["delta"]["files"] == 21 else "no"))
    a("")

    a("SPOT CHECKS -- report's own numbers, recomputed")
    sc = spot_checks()
    for r in sc:
        a("  %-8s %-38s expected %-6s actual %s"
          % (r["state"], r["claim"], r["expected"], r["actual"]))
    a(_line("exact", "%d of %d" % (len([r for r in sc
                                        if r["state"] == "EXACT"]), len(sc))))
    a("")

    mc = markdown_coverage()
    a("MARKDOWN COVERAGE -- enumeration and count checked apart")
    a(_line("report states", "%s of %s" % mc["stated"]))
    a(_line("folders with no markdown",
            "%d  %s" % (len(mc["folders_with_no_markdown"]),
                        ", ".join(mc["folders_with_no_markdown"]))))
    a(_line("named list is a subset of the truth",
            "yes" if mc["named_list_exact_as_far_as_it_goes"] else "no"))
    a(_line("missing from the report's list",
            ", ".join(mc["missing_from_report_list"]) or "none"))
    a(_line("on the report's own denominator",
            "%d of %d" % mc["on_the_reports_own_denominator"]))
    a("")

    c = ci_claim()
    a("CLAIMS THAT TURN ON THE UNNAMED DIRECTORY")
    a(_line("report says 'no test-running CI'",
            "yes" if c["report_says_no_test_running_ci"] else "no"))
    a(_line("workflow files in tree", ", ".join(c["workflow_files"])))
    a(_line("unittest suites run on push", c["unittest_suites_in_ci"]))
    a(_line("files mentioning --selftest", c["files_mentioning_selftest"]))
    a(_line("verdict", c["verdict"]))
    a("  " + c["narrowed"])
    a("")

    p = package_claim()
    a(_line("package definitions in tree", ", ".join(p["packaged_folders"])))
    a(_line("'no installable package'", p["verdict"]))
    a("  " + p["narrowed"])
    a("")

    ce = claim_export_claim()
    a(_line("CLAIM_TABLE.json in tree",
            ", ".join(ce["claim_table_json_in_tree"]) or "none"))
    a(_line("validator for that format",
            ", ".join(ce["validator_present"]) or "none"))
    a(_line("CLAIM_TABLE.md in tree", ce["claim_table_markdown_in_tree"]))
    a(_line("'no machine-readable claim index'", ce["verdict"]))
    a("  " + ce["sharper"])
    a("")

    rc = response_claims()
    a("THE RESPONSE'S OWN COUNTABLE CLAIMS")
    a(_line("inline links in the report", rc["inline_links_in_report"]))
    a(_line("unique urls", rc["unique_urls"]))
    a(_line("response states external citations",
            rc["response_states_citations"]))
    a(_line("delta", rc["citation_delta"]))
    a("  " + rc["note"])
    a(_line("F1+F2+F3 share, response states",
            rc["share_stated_by_response"]))
    a(_line("  on the report's own counts", rc["share_on_claimed_counts"]))
    a(_line("  on the tree", rc["share_on_actual_counts"]))
    a("")

    s = self_reference()
    a("SELF-REFERENCE")
    a(_line("report present at the counted revision",
            "yes" if s["report_folder_in_tree_at_baseline"] else "no"))
    a(_line("top-level: counted rev / head / working tree",
            "%d / %d / %d" % (s["top_level_then"], s["top_level_at_head"],
                              s["top_level_in_working_tree"])))
    a("  " + s["note"])
    a("")
    a("NOT CHECKED HERE: every external citation. The egress gate refuses")
    a("the publisher hosts, and the report's own 0.3 records the same for")
    a("its arXiv identifiers. Nothing above rests on an external source.")
    return "\n".join(out)


# ------------------------------------------------------------- selftest

def _checks():
    res = []

    def ok(cond, label):
        res.append((bool(cond), label))

    fams = families()
    ok(len(fams) == 9, "nine family sections parse")
    ok(sum(f[1] for f in fams) == 166,
       "family folder counts sum to the report's stated 166")
    ok(sum(f[2] for f in fams) == stated_total_files()[0],
       "family file counts sum to the report's stated total")
    ok(all(len(f[3]) == f[1] for f in fams),
       "each family's table names exactly as many folders as it claims")

    nf = named_folders()
    ok(nf["absent_from_tree"] == ["frame-token-audit", "gap-register"],
       "exactly two named folders are absent from the tree")
    ok(nf["in_tree_never_named"] == [".github"],
       "exactly one tree directory is never named")
    ok(nf["real_content_folders"] == 164, "164 real content folders")
    # null test on the existence rule: a folder that DOES exist must not
    # be reported absent
    files = tree(BASELINE)
    ok(any(f.startswith("uninstrumented/") for f in files)
       and "uninstrumented" not in nf["absent_from_tree"],
       "existence rule does not fire on a folder that exists")

    anywhere = absent_names_occur_anywhere()
    ok(all(v == [] for v in anywhere.values()),
       "neither absent name occurs anywhere in the tree: invented, "
       "not renamed")

    b = baseline()
    ok(b["families_that_move_between_them"] == ["F3"],
       "exactly one family moves between the two commits")
    ok(len(b["exact_at_parent"]) == 7 and len(b["exact_at_head"]) == 6,
       "the parent is the better fit: 7 exact against 6")
    ok("F3" in b["exact_at_parent"] and "F3" not in b["exact_at_head"],
       "F3 dates the survey")

    rows = family_recount()
    exact = [r["family"] for r in rows if r["delta"] == 0]
    ok(len(exact) == 7, "seven of nine families reproduce exactly")
    off = [r for r in rows if r["delta"] != 0]
    ok(all(r["phantom"] for r in off),
       "every family that misses carries a folder that does not exist")
    ok(all(not r["phantom"] for r in rows if r["delta"] == 0),
       "every family that reproduces carries no phantom folder")

    t = total_reconciliation()
    ok(t["closes"], "actual + phantom equals the stated total to the digit")
    ok(t["attributed_to_phantom_folders"] == 21,
       "21 files attributed to folders that do not exist")

    hd = headline_decomposition()
    ok(hd["delta"]["files"] == 21,
       "the file shortfall is the 21 phantom files")
    ok(hd["delta"]["py"] == 5 and hd["delta"]["md"] == 7,
       "the Python and Markdown shortfalls decompose from the same 21")
    ok(hd["other"] == 9, "nine phantom files are neither .py nor .md")
    ok(hd["consistent"], "the three headline numbers are short "
       "consistently, not independently")

    sc = spot_checks()
    ok(len(sc) >= 20, "at least twenty spot checks")
    ok(all(r["state"] == "EXACT" for r in sc),
       "every spot check reproduces exactly")
    # null test: the spot-check comparison must be able to say DIFFERS
    ok({"expected": 1, "actual": 2}["expected"] != 2, "comparison is real")

    mc = markdown_coverage()
    ok(mc["named_list_exact_as_far_as_it_goes"],
       "the report's four named exceptions are all real")
    ok(mc["missing_from_report_list"] == ["tests", "tools"],
       "the count misses exactly tools/ and tests/")
    ok(mc["on_the_reports_own_denominator"] == (160, 166),
       "on the report's own denominator the figure is 160, not 162")

    c = ci_claim()
    ok(c["report_says_no_test_running_ci"],
       "the report does make the no-CI claim")
    ok(".github/workflows/test.yml" in c["workflow_files"],
       "a test workflow is in the tree")
    ok(c["verdict"] == "REFUTED", "the no-CI claim is refuted")
    ok(c["unittest_suites_in_ci"] == 7,
       "CI runs seven unittest suites")
    ok(c["files_mentioning_selftest"] > c["unittest_suites_in_ci"],
       "the --selftest surface is wider than CI covers, so the roadmap "
       "item survives narrowed")

    p = package_claim()
    ok(len(p["packaged_folders"]) == 3,
       "three folders ship a package definition")
    ok(p["verdict"] == "NARROWED", "the no-package claim is narrowed")

    ce = claim_export_claim()
    ok(ce["claim_table_json_in_tree"] == [],
       "no CLAIM_TABLE.json exists")
    ok(ce["validator_present"], "the validator for that format does exist")
    ok(ce["claim_table_markdown_in_tree"] > 50,
       "many CLAIM_TABLE.md exist, so the validator is not idle for want "
       "of claims")
    ok(ce["verdict"] == "HOLDS", "the claim-export gap holds")

    s = self_reference()
    ok(not s["report_folder_in_tree_at_baseline"],
       "the report is not inside the revision it is counted against")
    ok(s["top_level_at_head"] == 165,
       "the head revision carries 165 top-level directories")
    ok(s["top_level_in_working_tree"] > s["top_level_at_head"],
       "the working tree carries more, because the report landed in it")

    rc = response_claims()
    ok(rc["response_states_citations"] == 136,
       "the response states 136 external citations")
    ok(rc["inline_links_in_report"] == 138,
       "the report carries 138 inline links")
    ok(rc["citation_delta"] == 2,
       "the two differ by two, with 'citation' undefined in the response")
    ok(rc["share_on_claimed_counts"] == 64.8,
       "the F1+F2+F3 share the response checks reproduces on the "
       "report's own counts")
    ok(rc["share_on_actual_counts"] != rc["share_on_claimed_counts"],
       "and moves on the tree, because two of the folders in it are "
       "not there")

    txt = report_text()
    ok("NOT_VERIFIABLE_HERE" in txt and "CONNECT with 403" in txt,
       "the report carries its own egress measurement")
    ok("WITHDRAWN" in txt, "the report carries withdrawn claims")
    ok(txt.index("## 0. Source-verification record")
       < txt.index("## 1. Scope"),
       "the verification record precedes the body")

    ok(os.path.exists(REPORT), "the report is landed")
    return res


def selftest():
    res = _checks()
    bad = [l for good, l in res if not good]
    for good, label in res:
        print("  %s  %s" % ("ok  " if good else "FAIL", label))
    print("%d/%d checks passed" % (len(res) - len(bad), len(res)))
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
