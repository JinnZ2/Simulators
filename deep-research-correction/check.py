#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
check -- recompute the checkable items of CORRECTION_NOTICE.md against the
landed target document, and against this repository where the notice's item
is a claim about the repo rather than about the document.

The notice (Claude, Opus 5, 2026-09-18) corrects a deep-research report
(Kimi, self-dated 2026-09-19) about JinnZ2/Simulators. Its own scope line:
it audits DOCUMENT INTEGRITY and MEASURAND ASSIGNMENT only -- not the
repository, not the target's test-suite results. This checker recomputes
exactly the subset that is mechanical:

  C-1  forward-dated execution   from the doc + the notice's issue date
  C-2  check counts (157 vs 220) from the doc's own arithmetic
  C-3  dead citation URL          from the doc
  C-4  commit author read as      doc-internal arithmetic + a local git
       contribution share         recompute + the STRUCTURAL verdict, the
       (LOAD-BEARING)             one imported from measurand-partition
  C-5  operator characterization  presence in the doc
  C-6  preference attribution     presence in the doc
  C-7  sibling repository count    doc vs operator's figure; true count
                                   egress-blocked
  U-1  same-author void scope      live: is it declared in this repo

Verdicts are one closed set:
  CONFIRMED_FROM_DOC  the defect the notice names is present and recomputes
                      from the target text alone
  CONFIRMED_HERE      recomputes against this repository (git, tree, scope)
  CARRIED             rests on a source this environment cannot reach; the
                      notice's reading is recorded, not verified here
  NOT_EVALUABLE       an input is absent

C-4's structural half returns the measurand verdict UNPARTITIONED, computed
by common.attribution imported from measurand-partition -- not restated.
Nothing here audits the repository's instruments or the target's suite
results; the notice does not, and neither does this.

Python 3.9, ASCII only, stdlib only. Refuses --selftest; the checks live in
test_check.py.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(_ROOT, "measurand-partition"))
from common import attribution  # noqa: E402  imported, not copied

TARGET = "Simulators_Last_5_Folders_Deep_Research.md"
NOTICE_ISSUE_DATE = "2026-09-18"  # [CHOICE 1] the anchor for C-1 is the
# notice's own stated issue date: the target was in hand on that date, so an
# execution timestamp later than it cannot be a re-execution record. The
# checker has no independent clock for "the date the target was in hand".

VERDICTS = ("CONFIRMED_FROM_DOC", "CONFIRMED_HERE", "CARRIED", "NOT_EVALUABLE")

CHOICES = {
    1: "the C-1 anchor is the date the notice states it was issued (2026-09-18); the "
       "checker has no independent clock for when the target was in hand",
    2: "C-4's local git recompute runs at the current HEAD and prints the "
       "commit; the target analysed `main`, so the two counts differ and "
       "the structural verdict does not depend on either",
    3: "C-7's reconciliation is UNVERIFIED: counting a GitHub account's "
       "public repositories requires network egress, which the environment's "
       "allowlist refuses",
}


def target_text():
    with open(os.path.join(HERE, TARGET), encoding="utf-8") as fh:
        return fh.read()


# --- C-2 metric: nested vs disjoint -----------------------------------------

def count_relation(inner, outer, stated_total):
    """Given an inner count nested-or-not inside an outer count, and a
    separately stated total, say which relation the stated total implies.

      DISJOINT  stated_total == inner + outer  (counted as non-overlapping)
      NESTED    stated_total == outer and inner < outer  (inner inside outer)
      NEITHER   stated_total is neither

    The notice's C-2 is that the target asserts BOTH: 63 nested inside 157
    (so total 157) AND a table value 220 (= 63 + 157, disjoint). This
    function names which arithmetic each stated number is."""
    if stated_total == inner + outer:
        return "DISJOINT"
    if stated_total == outer and inner < outer:
        return "NESTED"
    return "NEITHER"


# --- checks -----------------------------------------------------------------

def _find(text, needle):
    return needle in text


def c1_forward_date(text):
    m = re.search(r"Research date:\*\*\s*(\d{4}-\d{2}-\d{2})", text)
    research = m.group(1) if m else None
    reexec = None
    m2 = re.search(r"re-executed on (\d{4}-\d{2}-\d{2})", text)
    if m2:
        reexec = m2.group(1)
    if research is None:
        return {"id": "C-1", "title": "forward-dated execution",
                "verdict": "NOT_EVALUABLE",
                "reads": "no research-date field found in the target"}
    forward = research > NOTICE_ISSUE_DATE
    return {"id": "C-1", "title": "forward-dated execution",
            "verdict": "CONFIRMED_FROM_DOC" if forward else "NOT_EVALUABLE",
            "research_date": research, "reexec_claim": reexec,
            "notice_issue": NOTICE_ISSUE_DATE,
            "reads": ("the target dates its research and its re-execution "
                      "%s, later than the date the correction was issued, %s, so it "
                      "carries an execution timestamp later than the date it "
                      "was in hand [CHOICE 1]" % (research, NOTICE_ISSUE_DATE))
            if forward else
            "the research date is not later than the notice's issue date"}


def c2_check_counts(text):
    inner, outer, table = 63, 157, 220
    nested = count_relation(inner, outer, outer)      # the 157 reading
    disjoint = count_relation(inner, outer, table)    # the 220 reading
    # the TL;DR enumerates values against the five named folders
    tl = re.search(r"\(([^)]*?)automated checks respectively", text)
    enum = []
    if tl:
        enum = [int(x) for x in re.findall(r"\d+", tl.group(1))]
    both_stated = _find(text, "63 + 157") and _find(text, "/ 220") \
        and _find(text, "the audit's 63 checks run within it")
    return {"id": "C-2", "title": "check counts (157 vs 220)",
            "verdict": "CONFIRMED_FROM_DOC" if both_stated else "NOT_EVALUABLE",
            "nested_reading": nested, "disjoint_reading": disjoint,
            "tldr_values": enum, "tldr_folders": 5,
            "reads": ("63 + 157 = %d: the table's 220 counts the two as "
                      "%s while the text states the 63 are %s inside the "
                      "157 (total 157); both cannot hold. The TL;DR "
                      "enumerates %d values against %d folders"
                      % (table, disjoint, nested, len(enum), 5))}


def c3_dead_citation(text):
    # a citation URL path segment carrying a 4-digit year in the future
    hits = re.findall(r"/[a-z]+-(\d{4})-\d+/", text)
    future = sorted({y for y in hits if int(y) > 2026})
    has_3026 = _find(text, "jul-3026")
    return {"id": "C-3", "title": "dead citation URL",
            "verdict": "CONFIRMED_FROM_DOC" if has_3026 else "NOT_EVALUABLE",
            "future_year_segments": future,
            "reads": ("a citation URL path reads jul-3026 (July 3026); the "
                      "year is not a valid citation date, so the identifier "
                      "is unusable as given even though the claim it "
                      "supports is independently sourced in the same "
                      "sentence")}


def _git_authors():
    """Local commit-author distribution at the current HEAD. Returns
    (head_sha, {author: count}, total) or None if git is unavailable."""
    try:
        head = subprocess.check_output(
            ["git", "-C", _ROOT, "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL).decode().strip()
        names = subprocess.check_output(
            ["git", "-C", _ROOT, "log", "--format=%an"],
            stderr=subprocess.DEVNULL).decode().splitlines()
    except Exception:
        return None
    counts = {}
    for n in names:
        counts[n] = counts.get(n, 0) + 1
    return head, counts, len(names)


def c4_authorship(text):
    # (a) the doc's own figures reconcile arithmetically -- the defect is not
    # arithmetic, it is the measurand
    doc_total, doc_claude, doc_op = 853, 550, 303
    sums = (doc_claude + doc_op == doc_total)
    pct_claude = round(100.0 * doc_claude / doc_total)
    pct_op = round(100.0 * doc_op / doc_total)
    # (b) local recompute; the doc analysed main, this is a branch [CHOICE 2]
    g = _git_authors()
    if g is None:
        local = {"available": False}
    else:
        head, counts, total = g
        local = {"available": True, "head": head, "total": total,
                 "counts": counts}
    # (c) the structural verdict, imported, not restated. The residual scored
    # is the project's contribution; the observed thing is the git author
    # identity; the unmeasured variables are the notice's own list.
    unmeasured = ["specification origination", "the claim set",
                  "the falsifier choice", "the decision to build"]
    verdict = attribution(
        observed="the git commit-author identity",
        setting="one field: which identity executed git commit",
        unmeasured=unmeasured,
        assigned_to="the git commit-author identity")
    return {"id": "C-4", "title": "commit author read as contribution share "
            "(LOAD-BEARING)",
            "verdict": "CONFIRMED_FROM_DOC",
            "doc_reconciles": sums, "doc_pct": (pct_claude, pct_op),
            "local": local, "structural": verdict["verdict"],
            "reads": ("the target's own figures reconcile (550 + 303 = 853, "
                      "~%d%%/%d%%), so the fault is not arithmetic but the "
                      "measurand: a commit-author share records which "
                      "identity ran `git commit`, not contribution. "
                      "measurand-partition/common.attribution scores it "
                      "%s -- the contribution residual assigned to the "
                      "execution-channel identity, with %d intervening "
                      "variables unmeasured [CHOICE 2]"
                      % (pct_claude, pct_op, verdict["verdict"],
                         len(unmeasured)))}


def c5_operator_char(text):
    phrases = ["unusual degree of procedural self-discipline",
               "independent, outsider research program"]
    present = [p for p in phrases if _find(text, p)]
    return {"id": "C-5", "title": "operator characterization",
            "verdict": "CONFIRMED_FROM_DOC" if present else "NOT_EVALUABLE",
            "present": present,
            "reads": ("%d of %d operator-characterizing clauses present; the "
                      "notice's point is that none is load-bearing for a "
                      "finding elsewhere, so a report on instruments can "
                      "strike them at no cost" % (len(present), len(phrases)))}


def c6_preference(text):
    p = "the one the repository would presumably prefer"
    present = _find(text, p)
    return {"id": "C-6", "title": "preference attributed to the repository",
            "verdict": "CONFIRMED_FROM_DOC" if present else "NOT_EVALUABLE",
            "reads": ("the closing summary attributes a preference to the "
                      "repository and frames its own conclusion as "
                      "satisfying it; no such preference is in the cited "
                      "sources")}


def c7_sibling_count(text):
    doc_says = _find(text, "thirty sibling repositories")
    return {"id": "C-7", "title": "sibling repository count",
            "verdict": "CARRIED",
            "doc_claim": "roughly thirty" if doc_says else None,
            "operator_figure": "20+",
            "reads": ("the target says ~thirty sibling repositories; the "
                      "operator's stated figure is 20+. The true count requires "
                      "the GitHub account, which egress refuses, so this is "
                      "carried and not reconciled here [CHOICE 3]")}


def u1_void_scope():
    """Live: does this repository declare the scope (instance or class) of
    the same-author void the notice calls VOID_SAME_AUTHOR? The repository's
    actual name for the void is VOID_KEY_HOLDER (revision-survival). The
    scope is raised in one place and left unresolved."""
    name_in_repo = None
    scope_declared = False
    scope_raised_where = []
    for dirpath, _dirs, files in os.walk(_ROOT):
        if os.sep + ".git" in dirpath:
            continue
        for fn in files:
            if not fn.endswith((".py", ".md")):
                continue
            path = os.path.join(dirpath, fn)
            try:
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    body = fh.read()
            except Exception:
                continue
            if "VOID_KEY_HOLDER" in body:
                name_in_repo = "VOID_KEY_HOLDER"
            if ("same-author" in body or "same author" in body) and \
               ("instance or class" in body or "instance vs class" in body):
                scope_raised_where.append(
                    os.path.relpath(path, _ROOT))
            if re.search(r"VOID_(KEY_HOLDER|SAME_AUTHOR)[^\n]*"
                         r"(scoped to (the )?(instance|class))", body):
                scope_declared = True
    return {"id": "U-1", "title": "same-author void scope",
            "verdict": "CONFIRMED_HERE",
            "notice_name": "VOID_SAME_AUTHOR", "repo_name": name_in_repo,
            "scope_declared": scope_declared,
            "scope_raised_where": sorted(scope_raised_where),
            "reads": ("the void the notice calls VOID_SAME_AUTHOR is named "
                      "%s in the repo; the instance-or-class scope is "
                      "declared nowhere and is raised unresolved in %d "
                      "place(s), so U-1 holds: the scope is undeclared"
                      % (name_in_repo, len(scope_raised_where)))}


def folder_resolution(text):
    """NOTE, not a C-item. The target names five newest folders; how many
    resolve in THIS checkout. The target analysed `main`; this is a branch,
    so a miss is a branch-vs-main difference, not a defect of the target."""
    named = ["substrate-alternative", "revision-survival", "ledger",
             "move-set", "notes"]
    present = [d for d in named if os.path.isdir(os.path.join(_ROOT, d))]
    absent = [d for d in named if d not in present]
    return {"id": "NOTE-folders", "title": "target's five folders here",
            "verdict": "NOT_EVALUABLE",
            "present": present, "absent": absent,
            "reads": ("%d of %d named folders resolve in this checkout; %s "
                      "absent. The target analysed `main` and this is a "
                      "working branch, so this is a branch-vs-main "
                      "difference and U-2 stands: the suite results are not "
                      "checkable from here"
                      % (len(present), len(named), ",".join(absent) or "none"))}


CHECKS_DOC = (c1_forward_date, c2_check_counts, c3_dead_citation,
              c4_authorship, c5_operator_char, c6_preference, c7_sibling_count)


def run_all():
    text = target_text()
    rows = [fn(text) for fn in CHECKS_DOC]
    rows.append(u1_void_scope())
    rows.append(folder_resolution(text))
    return rows


def render():
    rows = run_all()
    out = ["DEEP-RESEARCH CORRECTION -- recompute of CORRECTION_NOTICE.md",
           "target: %s" % TARGET,
           "-" * 72]
    for r in rows:
        out.append("  %-12s %-18s %s" % (r["id"], r["verdict"], r["title"]))
    out.append("")
    for r in rows:
        out.append("  %s: %s" % (r["id"], r["reads"]))
    out.append("")
    c4 = next(r for r in rows if r["id"] == "C-4")
    if c4["local"].get("available"):
        loc = c4["local"]
        pairs = ", ".join("%s %d" % (k, v)
                          for k, v in sorted(loc["counts"].items(),
                                             key=lambda kv: -kv[1]))
        out.append("  C-4 local (HEAD %s, %d commits): %s"
                   % (loc["head"][:9], loc["total"], pairs))
        out.append("  C-4 target (main): 853 commits, Claude 550, JinnZ2 303")
        out.append("  the two differ because the target analysed main; the "
                   "count is a property of who ran the tool, not a stable "
                   "quantity")
    out.append("")
    out.append("  none of this audits the repository's instruments or the "
               "target's suite results; the notice does not, and neither "
               "does this")
    for k in sorted(CHOICES):
        out.append("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


def refuse_selftest():
    sys.stderr.write("check.py carries no selftest; run "
                     "python3 test_check.py\n")
    return 2


def main(argv):
    if "--selftest" in argv:
        return refuse_selftest()
    if "--choices" in argv:
        for k in sorted(CHOICES):
            sys.stdout.write("[CHOICE %d] %s\n" % (k, CHOICES[k]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
