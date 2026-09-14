#!/usr/bin/env python3
"""Two outside sweeps of one tree, compared.

The external review landed twice. The first pass surveyed the repository
as DOCUMENTED and executed none of it; the response asked for the
instruments to be run; the second pass ran them and published its own
execution record as a new section 0.

This repository also ran them, in `run_instruments.py`, before the second
pass arrived. So there are now two independent sweeps of one tree by two
parties in two sandboxes, plus the repository's own `self-scan/census.py`
as a third implementation. That is the decorrelated panel
`triad-playground` TP_008 says a consensus statistic is worthless
without, and it is available here for free because nobody coordinated.

WHAT THIS MODULE DOES: parses the second pass's own claims out of the
delivered document at call time -- never retyped, the MF_019 discipline --
and recomputes each against this tree, reporting AGREE, DISAGREE, or
NOT_COMPARABLE with the reason. A disagreement between two sweeps is a
measurement of the sweeps, not a verdict on either.

WHAT IT DOES NOT DO: adjudicate the substance of the report. The family
arithmetic is `recount.py`'s job and is unchanged -- the two renderings'
family tables are byte-identical, asserted below, so every EA_001..EA_014
finding carries to the second pass without recomputation.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

V1 = os.path.join(HERE, "DEEP_RESEARCH_2026_09_14.md")
V2 = os.path.join(HERE, "DEEP_RESEARCH_2026_09_14_V2.md")

# The revision `run_instruments.py` pins by its own [CHOICE 11]. The
# second pass states no revision at all, so the comparison has to
# establish one; see `revision_gap()`.
OURS_REV = "6633778"

TIMEOUT_S = 300

CHOICES = {
    1: "the second pass's failure list is parsed from its own numbered "
       "section 0.2, not transcribed",
    2: "only the union of the two failure sets is re-run here; a full "
       "300-module re-sweep would measure the sweep, not the disagreement",
    3: "each contested module is run at BOTH revisions, because the two "
       "sweeps ran at different ones and that is the first candidate "
       "explanation for every divergence",
    4: "a module whose verdict differs across revisions is reported "
       "REVISION_DEPENDENT, which attaches to neither party",
    5: "a module reading a path outside the repository is reported "
       "ENVIRONMENT_DEPENDENT and is not scored against either sweep",
    6: "file counts are taken at a COMMIT, never the working tree, since "
       "this audit is written into the tree it measures",
    7: "the three tools named in the mismatch claim are read out of the "
       "document and checked at every entry point in their folder",
}


def _run(cmd, cwd=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT"
    except OSError as e:
        return None, "OSERROR: %s" % e
    return p.returncode, p.stdout.decode("utf-8", "replace")


def _git(args):
    rc, out = _run(["git"] + args, cwd=ROOT)
    return out if rc == 0 else ""


# ---------------------------------------------------------------- diff

def version_diff():
    """How far apart the two renderings are, and where."""
    import difflib
    a = open(V1).read().splitlines()
    b = open(V2).read().splitlines()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    eq = ins = dele = 0
    body_changed = 0
    for t, i1, i2, j1, j2 in sm.get_opcodes():
        if t == "equal":
            eq += i2 - i1
        elif t == "insert":
            ins += j2 - j1
        elif t == "delete":
            dele += i2 - i1
        else:
            if i1 >= 100:
                body_changed += i2 - i1
    return {"v1_lines": len(a), "v2_lines": len(b), "equal": eq,
            "inserted": ins, "deleted": dele, "ratio": sm.ratio(),
            "body_lines_changed": body_changed}


def section_zero_kind():
    """v1's section 0 is a source-verification record; v2 REPLACES it."""
    def head(path):
        for ln in open(path):
            if ln.startswith("## 0."):
                return ln.strip()
        return ""
    h1, h2 = head(V1), head(V2)
    # v1's two tables (WITHDRAWN, NOT_VERIFIABLE_HERE) survive in v2 only
    # as prose bullets.
    v2txt = open(V2).read()
    return {"v1_heading": h1, "v2_heading": h2,
            "replaced": h1 != h2,
            "v1_withdrawn_table": "### 0.2 Claims WITHDRAWN" in open(V1).read(),
            "v2_withdrawn_table": "### 0.2 Claims WITHDRAWN" in v2txt,
            "v2_withdrawn_as_prose": "**WITHDRAWN**" in v2txt}


def family_tables_identical():
    """recount.py parses the report's own family tables. If the two
    renderings' tables agree, every EA_001..EA_014 finding carries."""
    import recount
    fam1 = recount.families(V1)
    fam2 = recount.families(V2)
    same = fam1 == fam2
    return {"v1_families": len(fam1), "v2_families": len(fam2),
            "identical": same}


# ------------------------------------------------- parse their claims

_FAILROW = re.compile(r"^\d+\.\s+\*\*`([^`]+)`\*\*")


def their_failures():
    """Section 0.2's numbered list, read from the document. [CHOICE 1]"""
    out = []
    inside = False
    for ln in open(V2):
        if ln.startswith("### 0.2"):
            inside = True
            continue
        if inside and ln.startswith("### 0.3"):
            break
        if inside:
            m = _FAILROW.match(ln)
            if m:
                out.append(m.group(1))
    return out


def their_zero_one_rows():
    """Section 0.1's instrument table, read from the document."""
    rows = []
    inside = False
    for ln in open(V2):
        if ln.startswith("### 0.1"):
            inside = True
            continue
        if inside and ln.startswith("### 0.2"):
            break
        if inside and ln.startswith("|") and "---" not in ln:
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 3 and cells[0] != "Instrument":
                rows.append(cells)
    return rows


def our_failures():
    """run_instruments.py's pinned sample, read from the file it wrote."""
    p = os.path.join(HERE, "samples", "instrument_sweep.sample.txt")
    if not os.path.exists(p):
        return None
    out, inside = [], False
    for ln in open(p):
        if ln.startswith("FAIL ("):
            inside = True
            continue
        if inside:
            if not ln.strip() or ln.startswith(("TIMEOUT", "DEP_MISSING")):
                break
            out.append(ln.split()[0])
    return out


# ------------------------------------------------- recompute contested

_WORKTREES = {}


def worktree(rev):
    """Throwaway checkout. self-scan SS_009: running a repository's own
    suites writes files, and a sweep that dirties the tree is measuring
    something it changed."""
    if rev in _WORKTREES:
        return _WORKTREES[rev]
    path = os.path.join("/tmp", "claude-0", "xc_" + re.sub(r"\W", "_", rev))
    if not os.path.isdir(os.path.join(path, ".git")):
        _run(["rm", "-rf", path])
        # A directory removed out from under git stays registered, so a
        # bare `add` fails with "missing but already registered". Prune
        # first and force, or the second run of this module reports a
        # worktree failure as a missing measurement.
        _run(["git", "worktree", "prune"], cwd=ROOT)
        rc, out = _run(["git", "worktree", "add", "-q", "--detach", "-f",
                        path, rev], cwd=ROOT)
        if rc != 0:
            return None
    _WORKTREES[rev] = path
    return path


_COUNTS = (
    re.compile(r"(\d+)\s*(?:/|of)\s*(\d+)\s+checks?\s+passed"),
    re.compile(r"selftest:\s*(\d+)\s+checks?,\s*(\d+)\s+failed"),
    re.compile(r"SELFTEST\s+(PASS|FAIL)\s*\((\d+)\s+checks?\s+failed\)"),
    re.compile(r"^checks:\s*(\d+)\s+failed:\s*(\d+)", re.M),
    re.compile(r"(\d+)\s+checks?,\s*(\d+)\s+failed", re.I),
)


def _verdict(rc, out):
    if rc is None:
        return "TIMEOUT", out[:80]
    if "Traceback (most recent call last)" in out:
        last = [l for l in out.strip().split("\n") if l.strip()]
        return "CRASH", (last[-1] if last else "")[:100]
    m = _COUNTS[0].search(out)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return ("PASS" if a == b else "FAIL"), "%d of %d checks passed" % (a, b)
    m = _COUNTS[1].search(out)
    if m:
        f = int(m.group(2))
        return ("PASS" if f == 0 else "FAIL"), \
            "selftest: %s checks, %d failed" % (m.group(1), f)
    m = _COUNTS[2].search(out)
    if m:
        return ("PASS" if m.group(1) == "PASS" else "FAIL"), \
            "SELFTEST %s (%s failed)" % (m.group(1), m.group(2))
    m = _COUNTS[3].search(out)
    if m:
        f = int(m.group(2))
        return ("PASS" if f == 0 else "FAIL"), \
            "checks: %s   failed: %d" % (m.group(1), f)
    m = _COUNTS[4].search(out)
    if m:
        f = int(m.group(2))
        return ("PASS" if f == 0 else "FAIL"), \
            "%s checks, %d failed" % (m.group(1), f)
    return "NO_VERDICT", (out.strip().split("\n")[-1] if out.strip() else "")[:100]


# A module reading a path outside the repository cannot be scored against
# either sweep: its verdict is a property of the sandbox. [CHOICE 5]
_EXTERNAL = re.compile(r'^\s*[A-Z_]+\s*=\s*"(/(?!home/user/Simulators)[^"]+)"',
                       re.M)


def external_reads(relpath, base):
    p = os.path.join(base, relpath)
    folder = os.path.dirname(p)
    hits = []
    if not os.path.isdir(folder):
        return hits
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".py"):
            continue
        try:
            src = open(os.path.join(folder, fn)).read()
        except OSError:
            continue
        for m in _EXTERNAL.finditer(src):
            hits.append((fn, m.group(1)))
    return hits


def contested(revs=(OURS_REV, "HEAD")):
    """Union of the two failure sets, re-run at each revision.

    Only the union is re-run [CHOICE 2]; each member is run at both
    revisions [CHOICE 3]; a member whose verdict moves between them is
    REVISION_DEPENDENT rather than either party being wrong [CHOICE 4].
    """
    theirs = set(their_failures())
    ours = set(our_failures() or [])
    union = sorted(theirs | ours)               # [CHOICE 2]
    rows = []
    for rel in union:
        by_rev = {}
        ext = []
        for rev in revs:                        # [CHOICE 3]
            base = worktree(rev)
            if base is None:
                by_rev[rev] = ("NO_WORKTREE", "")
                continue
            if not os.path.exists(os.path.join(base, rel)):
                by_rev[rev] = ("ABSENT", "not in tree at this revision")
                continue
            rc, out = _run([sys.executable, os.path.join(base, rel),
                            "--selftest"], cwd=base)
            by_rev[rev] = _verdict(rc, out)
            if not ext:
                ext = external_reads(rel, base)
        states = set(v[0] for v in by_rev.values())
        if ext:
            kind = "ENVIRONMENT_DEPENDENT"          # [CHOICE 5]
        elif len(states) > 1:
            kind = "REVISION_DEPENDENT"             # [CHOICE 4]
        else:
            kind = "STABLE"
        rows.append({"module": rel, "theirs": rel in theirs,
                     "ours": rel in ours, "by_rev": by_rev,
                     "kind": kind, "external": ext})
    return {"theirs": sorted(theirs), "ours": sorted(ours),
            "both": sorted(theirs & ours),
            "theirs_only": sorted(theirs - ours),
            "ours_only": sorted(ours - theirs),
            "rows": rows}


# ------------------------------------------- the known-answer divergence

def known_answer_denominators():
    """Both readings of one run are correct and they count different
    things. The second pass reports `84 PASS + 2 FAIL (pinned)`;
    run_instruments.py reported the tool's own headline, `cases
    disagreeing with the registry: 0`. Neither is a mistake: the headline
    counts disagreement with what the registry EXPECTS, and a pinned
    failure that fails agrees with its expectation. measurement-fork's
    VOID RATIO -- one name, two denominators -- on a summary line."""
    rc, out = _run([sys.executable, os.path.join(ROOT, "tools",
                                                 "known_answer.py")])
    if rc is None:
        return {"ran": False}
    raw_pass = len(re.findall(r"\bPASS\b", out))
    raw_fail = len(re.findall(r"\bFAIL \(pinned\)", out))
    m = re.search(r"cases disagreeing with the registry:\s*(\d+)", out)
    headline = int(m.group(1)) if m else None
    m2 = re.search(r"metrics registered:\s*(\d+)\s+expected:\s*(\d+)\s+(\w+)",
                   out)
    return {"ran": True, "raw_pass": raw_pass, "raw_fail_pinned": raw_fail,
            "headline_disagreeing": headline,
            "metrics": (int(m2.group(1)), int(m2.group(2)), m2.group(3))
            if m2 else None,
            "exit": rc,
            "two_readings_differ": headline is not None and
            headline != raw_fail}


# ------------------------------------------------- the revision question

def revision_gap():
    """The second pass states a survey date and no commit; its gate-check
    row reports a scanned-file count, and so does ours. The counts differ,
    and the difference is this audit folder landing -- UNI_010 / ANC_001 /
    QA_007 at repository scale, arriving through the measurement."""
    theirs = None
    for cells in their_zero_one_rows():
        m = re.search(r"\(([\d,]+)\s+files\)", " ".join(cells))
        if m:
            theirs = int(m.group(1).replace(",", ""))
    ours = None
    p = os.path.join(HERE, "samples", "named_instruments.sample.txt")
    if os.path.exists(p):
        m = re.search(r"files_scanned:\s*(\d+)", open(p).read())
        if m:
            ours = int(m.group(1))
    # Pinned to the HEAD COMMIT, never the working tree: this audit is
    # being written into the tree it measures, so a working-tree count
    # moves while the module that reports it is still being edited.
    # [CHOICE 6]
    live = None
    base = worktree("HEAD")
    if base:
        rc, out = _run([sys.executable,
                        os.path.join(base, "gate-check", "gate_check.py"),
                        base], cwd=base)
        if rc is not None:
            m = re.search(r"files_scanned:\s*(\d+)", out)
            if m:
                live = int(m.group(1))
    head = _git(["rev-parse", "--short", "HEAD"]).strip()
    return {"theirs": theirs, "ours_pinned_rev": OURS_REV, "ours": ours,
            "live_head": live, "head_rev": head,
            "ours_matches_pinned": ours is not None,
            "theirs_matches_live": theirs is not None and theirs == live}


# ------------------------------------------ verdict / exit-code mismatch

# Section 0.1's census row reads three tools as reporting "zero failed
# checks in their output while exiting nonzero -- an exit-code/verdict
# mismatch". The three are named in the document; they are read out of it
# rather than retyped, and each is checked at BOTH of its entry points,
# because the house convention puts the checks in a separate runner and
# has the module itself refuse. [CHOICE 7]
_MISMATCH_NAMED = re.compile(r"\(`?([a-z0-9\-]+(?:/[A-Za-z0-9_.\-]+)?)`?[,)]")


def their_mismatch_claim():
    txt = open(V2).read()
    m = re.search(r"three tools \(([^)]*)\)", txt)
    if not m:
        return []
    return [x.strip().strip("`") for x in m.group(1).split(",")]


def _entry_points(name):
    """A folder name yields its module and its runner; a path yields
    itself."""
    if name.endswith(".py"):
        return [name]
    out = []
    d = os.path.join(ROOT, name)
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"):
                out.append(os.path.join(name, fn))
    return out


def exit_verdict_mismatch(mods=None):
    """Is the reported mismatch a mismatch, or the refusal convention.

    A module that refuses `--selftest` exits 2, prints no failed-check
    count, and names the runner that holds the checks. A classifier with
    no REFUSED bin reads that as `zero failed checks, nonzero exit` and
    files it as a defect. That is EA_015's trap -- the same one this
    repository's own sweep fell into first -- reached by a third reader
    through the repository's own census output."""
    if mods is None:
        mods = ["notes/check_datasets.py"]
        for name in their_mismatch_claim():
            mods.extend(_entry_points(name))
    rows = []
    for rel in mods:
        if not os.path.exists(os.path.join(ROOT, rel)):
            rows.append({"module": rel, "exit": None, "verdict": "ABSENT",
                         "detail": "", "mismatch": False, "refusal": False})
            continue
        rc, out = _run([sys.executable, os.path.join(ROOT, rel),
                        "--selftest"], cwd=ROOT)
        state, detail = _verdict(rc, out)
        refusal = (rc not in (0, None) and state == "NO_VERDICT" and
                   ".py" in detail and "Traceback" not in out)
        rows.append({"module": rel, "exit": rc, "verdict": state,
                     "detail": detail, "refusal": refusal,
                     "mismatch": not refusal and
                                 ((state == "FAIL" and rc == 0) or
                                  (state == "PASS" and rc not in (0, None)))})
    return rows


def audit_folder_in_other_checks():
    """Does this folder appear in another folder's check output. It does,
    and the check is doing its job: notes/check_datasets.py now names
    external-audit/ among the files that give G-SPAN and MESA an
    antecedent independent of the note it was written to guard."""
    rc, out = _run([sys.executable,
                    os.path.join(ROOT, "notes", "check_datasets.py"),
                    "--selftest"], cwd=ROOT)
    if rc is None:
        return {"ran": False}
    named = sorted(set(re.findall(r"external-audit/[A-Za-z0-9_.\-/]+", out)))
    return {"ran": True, "named": named, "count": len(named)}


# ------------------------------------------------------------- render

def render():
    L = []
    w = L.append
    w("TWO OUTSIDE SWEEPS OF ONE TREE")
    w("=" * 72)
    w("")
    w("The external review landed twice. This compares the second pass's")
    w("own execution record against this repository's, and against the")
    w("repository's own census. Every claim below is parsed out of the")
    w("delivered document at call time and recomputed here. [CHOICE 1]")
    w("")

    d = version_diff()
    w("1. IS THE SECOND PASS A COPY")
    w("   v1 %d lines, v2 %d lines, %d equal, ratio %.4f"
      % (d["v1_lines"], d["v2_lines"], d["equal"], d["ratio"]))
    w("   inserted %d, deleted %d, body lines replaced %d"
      % (d["inserted"], d["deleted"], d["body_lines_changed"]))
    z = section_zero_kind()
    w("   section 0 replaced: %s" % z["replaced"])
    w("     v1: %s" % z["v1_heading"])
    w("     v2: %s" % z["v2_heading"])
    w("   v1's WITHDRAWN table survives in v2 as prose, not as a table:")
    w("     table in v1 %s / in v2 %s / prose in v2 %s"
      % (z["v1_withdrawn_table"], z["v2_withdrawn_table"],
         z["v2_withdrawn_as_prose"]))
    f = family_tables_identical()
    w("   family tables identical: %s (%d vs %d families) -- so every"
      % (f["identical"], f["v1_families"], f["v2_families"]))
    w("   EA_001..EA_014 arithmetic finding carries to the second pass")
    w("   without recomputation, including the two phantom folders.")
    w("")

    k = known_answer_denominators()
    w("2. THE KNOWN-ANSWER GATE: TWO READINGS, BOTH CORRECT")
    if k.get("ran"):
        w("   raw per-case verdicts   PASS %d   FAIL (pinned) %d"
          % (k["raw_pass"], k["raw_fail_pinned"]))
        w("   the tool's headline     cases disagreeing with the registry: %s"
          % k["headline_disagreeing"])
        if k["metrics"]:
            w("   metrics registered %d  expected %d  %s" % k["metrics"])
        w("   two readings differ: %s" % k["two_readings_differ"])
        w("   The second pass read the per-case verdicts and reported")
        w("   `84 PASS + 2 FAIL (pinned)`. run_instruments.py read the")
        w("   headline and reported 0. Neither reading is a misreading.")
        w("   counts disagreement with what the registry EXPECTS, and a")
        w("   pinned failure that fails agrees with its expectation --")
        w("   one name over two denominators, which is the shape")
        w("   measurement-fork calls a VOID RATIO, on a summary line.")
        w("   Two outside readers of one run reported 0 and 2. That is")
        w("   the evidence; neither reader had to be careless to get it.")
    else:
        w("   NOT RUN")
    w("")

    r = revision_gap()
    w("3. THE TWO SWEEPS RAN AT DIFFERENT REVISIONS")
    w("   gate-check files_scanned, second pass:  %s" % r["theirs"])
    w("   gate-check files_scanned, ours (%s):  %s"
      % (r["ours_pinned_rev"], r["ours"]))
    w("   gate-check files_scanned, HEAD commit %s: %s  [CHOICE 6]"
      % (r["head_rev"], r["live_head"]))
    w("   second pass matches live HEAD: %s" % r["theirs_matches_live"])
    w("   The second pass states a survey date and no commit. Ours pins")
    w("   %s by its own [CHOICE 11]. The gap between the two counts is"
      % r["ours_pinned_rev"])
    w("   this audit folder landing -- so the first candidate explanation")
    w("   for any divergence below is the revision, not the runner.")
    w("")

    c = contested()
    w("4. THE FAILURE SETS")
    w("   second pass: %d    ours: %d    agreeing: %d"
      % (len(c["theirs"]), len(c["ours"]), len(c["both"])))
    w("   each sweep carries exactly one the other missed:")
    w("     theirs only: %s" % (", ".join(c["theirs_only"]) or "none"))
    w("     ours only:   %s" % (", ".join(c["ours_only"]) or "none"))
    w("")
    w("   re-run at both revisions [CHOICE 2] [CHOICE 3] [CHOICE 4]:")
    for row in c["rows"]:
        w("   %-46s %s" % (row["module"], row["kind"]))
        for rev, (st, det) in sorted(row["by_rev"].items()):
            w("     %-10s %-12s %s" % (rev, st, det))
        for fn, path in row["external"]:
            w("     reads outside the tree: %s -> %s" % (fn, path))
    w("")
    w("   ENVIRONMENT_DEPENDENT is the sharp one. [CHOICE 5] A module")
    w("   whose selftest reads a path outside the repository has a")
    w("   verdict that is a property of the sandbox, not of the tree, so")
    w("   it cannot be scored against either sweep, and the divergence")
    w("   attaches to neither. evaluation-frame's own EF_009 records")
    w("   that its corpus is written by the run that reads it; this is")
    w("   that finding measured from outside, by a second party who")
    w("   could not have known to look for it.")
    w("")

    m = exit_verdict_mismatch()
    w("5. THE REPORTED EXIT / VERDICT MISMATCH [CHOICE 7]")
    w("   second pass, section 0.1: three tools \"report zero failed")
    w("   checks in their output while exiting nonzero\". Named in the")
    w("   document: %s" % (", ".join(their_mismatch_claim()) or "none parsed"))
    w("")
    for row in m:
        w("   %-44s exit=%-5s %-11s mismatch=%s refusal=%s"
          % (row["module"], row["exit"], row["verdict"], row["mismatch"],
             row["refusal"]))
        if row["detail"]:
            w("     %s" % row["detail"][:80])
    w("")
    w("   Every nonzero exit above is the house REFUSAL convention: the")
    w("   module prints no failed-check count and names the runner that")
    w("   holds the checks, and each of those runners is green. A")
    w("   classifier with no REFUSED bin files that as a finding. This")
    w("   repository's own sweep fell into the same trap first and")
    w("   recorded it as EA_015; the census bins it honestly as")
    w("   NONZERO_EXIT_NO_VERDICT and the second pass read the bin as a")
    w("   finding. Three readers, one trap, and the only one that did")
    w("   not fall in is the one that named a state for it.")
    w("")
    w("   notes/check_datasets.py is in the table as a control: it")
    w("   really does report FAIL, and it exits nonzero to match, so it")
    w("   is not a mismatch either -- a first pass here read its exit as")
    w("   0 by taking the exit code of a pipeline rather than the module.")
    w("")

    a = audit_folder_in_other_checks()
    w("6. THIS FOLDER CHANGED ANOTHER FOLDER'S CHECK")
    if a.get("ran"):
        w("   notes/check_datasets.py names %d file(s) under external-audit/"
          % a["count"])
        for n in a["named"]:
            w("     %s" % n)
        w("   At %s that check named only notes/memory-export/. The audit"
          % OURS_REV)
        w("   landed, the terms acquired an antecedent independent of the")
        w("   note, and the check said so and named the files. It is not")
        w("   malfunctioning -- it is reporting the loop UNI_010 / ANC_001")
        w("   / QA_007 describe, on the audit written to measure the tree.")
    else:
        w("   NOT RUN")
    w("")
    w("CHOICES")
    for n in sorted(CHOICES):
        w("  [CHOICE %d] %s" % (n, CHOICES[n]))
    return "\n".join(L)


# ------------------------------------------------------------ selftest

def _checks():
    out = []

    def ck(name, cond, detail=""):
        out.append((name, bool(cond), detail))

    # -- the two documents exist and are not the same file
    a, b = open(V1).read(), open(V2).read()
    ck("v1 present", len(a) > 100000)
    ck("v2 present", len(b) > 100000)
    ck("v2 is not v1", a != b)
    d = version_diff()
    ck("second pass is a revision, not a rewrite", d["ratio"] > 0.8,
       "ratio %.4f" % d["ratio"])
    ck("v2 deletes nothing wholesale", d["deleted"] == 0)

    z = section_zero_kind()
    ck("section 0 replaced", z["replaced"])
    ck("v1 carried a WITHDRAWN table", z["v1_withdrawn_table"])
    ck("v2 does not", not z["v2_withdrawn_table"])
    ck("v2 carries the withdrawal as prose", z["v2_withdrawn_as_prose"])

    f = family_tables_identical()
    ck("family tables identical across renderings", f["identical"])
    ck("nine families parsed from each", f["v1_families"] == 9 and
       f["v2_families"] == 9, "%d / %d" % (f["v1_families"], f["v2_families"]))

    # -- their claims are parsed, not retyped
    th = their_failures()
    ck("five failures parsed from section 0.2", len(th) == 5,
       "%d parsed" % len(th))
    ck("every parsed failure is a path ending .py",
       all(x.endswith(".py") and "/" in x for x in th))
    src = open(os.path.abspath(__file__)).read()
    body = src.split("def _checks", 1)[0]
    ck("no failure path is a literal in the module body",
       not any(x in body for x in th),
       "MF_019: parsed at call time, never retyped")
    rows = their_zero_one_rows()
    ck("section 0.1 instrument table parses", len(rows) >= 5,
       "%d rows" % len(rows))

    ours = our_failures()
    ck("our own sweep's failures readable", ours is not None and
       len(ours) == 5, "%s" % (len(ours) if ours else None))

    # -- the overlap is the result
    if ours is not None:
        both = set(th) & set(ours)
        ck("four of five agree", len(both) == 4, "%d agree" % len(both))
        ck("each sweep has exactly one the other missed",
           len(set(th) - set(ours)) == 1 and len(set(ours) - set(th)) == 1)

    # -- known-answer: the two readings differ and both are computable
    k = known_answer_denominators()
    ck("known-answer gate ran", k.get("ran"))
    if k.get("ran"):
        ck("raw verdicts carry two pinned failures",
           k["raw_fail_pinned"] == 2, "%d" % k["raw_fail_pinned"])
        ck("the tool's headline reads zero",
           k["headline_disagreeing"] == 0, "%s" % k["headline_disagreeing"])
        ck("so the two readings differ", k["two_readings_differ"])
        ck("the registry is complete",
           k["metrics"] and k["metrics"][2] == "COMPLETE")
        ck("and the gate still exits clean", k["exit"] == 0,
           "a pinned failure is expected, so a clean exit is correct")

    # -- revision
    r = revision_gap()
    ck("their file count parsed from the table", r["theirs"] is not None)
    ck("our pinned file count readable", r["ours"] is not None)
    ck("gate-check runs live", r["live_head"] is not None)
    ck("the two counts differ", r["theirs"] != r["ours"],
       "%s vs %s" % (r["theirs"], r["ours"]))
    ck("their count matches live HEAD", r["theirs_matches_live"],
       "so the second pass ran later, not differently")

    # -- the reported mismatch is the refusal convention [CHOICE 7]
    named = their_mismatch_claim()
    ck("the three named tools parse from the document", len(named) == 3,
       ", ".join(named))
    ck("none is retyped in the module body",
       not any(n in body for n in named))
    m = exit_verdict_mismatch()
    ck("check_datasets reports FAIL", m[0]["verdict"] == "FAIL")
    ck("and exits nonzero to match", m[0]["exit"] not in (0, None),
       "exit=%s; a first pass read a pipeline's exit code instead"
       % m[0]["exit"])
    ck("so it is not a mismatch", not m[0]["mismatch"])
    refusals = [r for r in m if r["refusal"]]
    ck("at least one named tool refuses rather than failing",
       len(refusals) >= 1, "; ".join(r["module"] for r in refusals))
    ck("every refusal exits nonzero with no failed-check count",
       all(r["exit"] not in (0, None) and r["verdict"] == "NO_VERDICT"
           for r in refusals))
    ck("no tool in the table is a real mismatch",
       not any(r["mismatch"] for r in m),
       "the reported defect is the refusal convention, EA_015's trap")
    runners = [r for r in m if r["verdict"] == "PASS"]
    ck("and the runners those refusals name are green", len(runners) >= 1,
       "; ".join(r["module"] for r in runners))

    # -- the verdict reader is not constant: null-test it both ways
    st, _ = _verdict(0, "selftest: 12 checks, 0 failed")
    ck("clean output reads PASS", st == "PASS")
    st, _ = _verdict(0, "selftest: 12 checks, 3 failed")
    ck("dirty output reads FAIL", st == "FAIL")
    st, _ = _verdict(0, "SELFTEST FAIL (2 checks failed)")
    ck("the fifth convention reads FAIL", st == "FAIL")
    st, _ = _verdict(0, "44 of 45 checks passed")
    ck("a short count reads FAIL", st == "FAIL")
    st, _ = _verdict(0, "checks: 142   failed: 0")
    ck("the `checks: N failed: M` convention reads PASS", st == "PASS",
       "the shape self-scan/census.py read as a failure until repaired")
    st, _ = _verdict(0, "209 checks, 0 failed")
    ck("and the prefixless `N checks, M failed` convention too",
       st == "PASS")
    st, _ = _verdict(1, "Traceback (most recent call last)\nFileNotFoundError")
    ck("a crash is CRASH, never FAIL and never PASS", st == "CRASH",
       "EA_015: a traceback names .py files and must not read as a refusal")
    st, _ = _verdict(None, "TIMEOUT")
    ck("a timeout is its own state", st == "TIMEOUT")
    st, _ = _verdict(0, "nothing here")
    ck("no parseable verdict is NO_VERDICT, not PASS", st == "NO_VERDICT")

    # -- the external-path detector fires and is not constant
    ext = external_reads("evaluation-frame/selftest_frame.py", ROOT)
    ck("evaluation-frame reads a path outside the tree", len(ext) > 0,
       "; ".join("%s -> %s" % e for e in ext[:2]))
    ck("that path is absolute and outside the repo",
       all(p.startswith("/") and not p.startswith(ROOT) for _, p in ext))
    quiet = external_reads("zero-sum-curriculum-null/selftest_nc.py", ROOT)
    ck("and the detector is silent on a folder that reads only the tree",
       len(quiet) == 0, "not CONSTANT_FIRES")

    # -- this folder appears in another folder's check
    a2 = audit_folder_in_other_checks()
    ck("notes/check_datasets.py names this folder", a2.get("ran") and
       a2["count"] >= 1, "%s" % (a2.get("named")))

    # -- house form
    ck("every choice is printed", all(("[CHOICE %d]" % n) in render()
                                      for n in CHOICES))
    ck("every choice is cited where it takes effect",
       all(src.count("[CHOICE %d]" % n) >= 2 for n in CHOICES))
    return out


def selftest():
    rows = _checks()
    bad = [r for r in rows if not r[1]]
    for name, ok, detail in rows:
        if not ok:
            print("FAIL  %s  %s" % (name, detail))
    print("selftest: %d checks, %d failed" % (len(rows), len(bad)))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--choices" in argv:
        for n in sorted(CHOICES):
            print("[CHOICE %d] %s" % (n, CHOICES[n]))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
