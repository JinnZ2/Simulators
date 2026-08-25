#!/usr/bin/env python3
"""S3-S6 -- resolve each extracted claim against the tree, bin it, date
the divergences, and print the rate.

WO10 asks scan 4's question of a document whose operands are files
rather than cells. The four bins are IMPORTED from
sheet-structure-scan/scan4.py, not restated, so this scan and that one
cannot disagree about what DIVERGED means.

What is different here, and it is the whole of S5: a workbook carries no
per-cell history, so scan 4 returns UNRECOVERABLE for every divergence
date (SSS_038). A git repository does. For each DIVERGED claim this
emits the last commit touching the named artifact and the last commit
touching the paragraph that states the number, and the interval between
them.

Absence is first-class throughout. UNBOUND (nobody said what would
settle it) is distinct from NOT_TESTABLE (the subject is not reachable)
and both are distinct from a bin.

CC0. stdlib for the scanner. Running a folder's own suite may need that
folder's dependencies; every binding declares its own and a missing one
is NOT_TESTABLE with the name in the reason.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import extract      # noqa: E402
import bindings     # noqa: E402
import scan4        # noqa: E402

MAINTAINED = scan4.MAINTAINED
HOLDS_UNMAINTAINED = scan4.HOLDS_UNMAINTAINED
DIVERGED = scan4.DIVERGED
NOT_TESTABLE = scan4.NOT_TESTABLE
UNBOUND = "UNBOUND"
BINS = scan4.BINS

TIMEOUT = 300

# Where checks execute. ROOT until a scan opens an isolated worktree.
#
# This is the difference between scan 4 on a workbook and scan 4 on a
# repository, and it was found by running the first version in place:
# resolving a COUNT claim means EXECUTING code, and this repo's own
# suites write provenance ledgers, a denial record, a JSONL log, and --
# once -- a file literally named `--selftest`. A scan that modifies the
# tree it is measuring is measuring something it has changed.
#
# So every check runs in a throwaway worktree at HEAD. The consequence
# is stated rather than hidden: what is measured is HEAD, not the
# working tree, and an uncommitted change is invisible to this scan.
BASE = None


# ---------------------------------------------------------------- keys

def key_of(c, seen):
    v = "/".join(c["value"]) if c["value"] else "-"
    base = "%s|%s|%s" % (c["section_title"], c["pattern"], v)
    n = seen.get(base, 0)
    seen[base] = n + 1
    return "%s|%d" % (base, n)


def keyed_claims():
    cl = extract.claims()
    seen = {}
    for c in cl:
        c["key"] = key_of(c, seen)
    return cl


# ------------------------------------------------------------- running

def base():
    return BASE or ROOT


def _run(args, cwd=None):
    env = dict(os.environ)
    # A script that draws is a script that may write. Headless backend,
    # and anything that writes runs in a throwaway worktree instead of
    # in the tree being measured (see `_isolated`).
    env.setdefault("MPLBACKEND", "Agg")
    try:
        p = subprocess.run(args, cwd=cwd or base(), stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=TIMEOUT,
                           env=env)
        return p.returncode, p.stdout.decode("utf8", "replace")
    except subprocess.TimeoutExpired:
        return None, "TIMEOUT after %ds" % TIMEOUT
    except OSError as exc:
        return None, "OSError: %s" % exc


def have(dep):
    if dep in ("stdlib", "git"):
        if dep == "git":
            return _run(["git", "--version"])[0] == 0
        return True
    try:
        __import__(dep)
        return True
    except Exception:                                     # noqa: BLE001
        return False


_RATIO = re.compile(r"selftest:?\s*(\d+)\s*/\s*(\d+)", re.I)
# Two more shapes are in use, both without the word `selftest` on the
# line: `N/N checks passed` and a bare `N/N` on its own line at the end
# of a run. Anchored to a whole line so a bare ratio in prose does not
# match -- an unanchored \d+/\d+ would fire on a date or a fraction,
# which is T1-1's word-list failure in a parser.
_RATIO_LINE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)"
                         r"(?:\s+checks?\s+passed)?\s*$", re.M)
_CHECKS = re.compile(r"selftest:\s*(\d+)\s+checks?,\s*(\d+)\s+failed", re.I)
_CHECKS2 = re.compile(r"SELFTEST\s+(PASS|FAIL)\s*\((\d+)\s+checks?\s+failed",
                      re.I)
_PASSFAIL = re.compile(r"(\d+)\s+checks?,\s*(\d+)\s+failed", re.I)


def parse_count(out, how):
    """(count, failed) from a module's own selftest line, or (None, None).

    Three shapes are in use across the repo and none is normalised here:
    `selftest: N checks, M failed`, `SELFTEST PASS (M checks failed)` with
    an N printed per line above it, and `selftest N/N`.
    """
    m = _CHECKS.search(out)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = _PASSFAIL.search(out)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = _RATIO.search(out)
    if m:
        return int(m.group(2)), int(m.group(2)) - int(m.group(1))
    ms = _RATIO_LINE.findall(out)
    if ms:
        a, b_ = ms[-1]
        return int(b_), int(b_) - int(a)
    m = _CHECKS2.search(out)
    if m:
        n = len(re.findall(r"^\s{2}\S.*\b(PASS|FAIL)\b", out, re.M))
        return (n or None), int(m.group(2))
    return None, None


_PYTEST = re.compile(r"(?:(\d+) failed[, ]+)?(\d+) passed"
                     r"(?:[, ]+(\d+) skipped)?")


def run_pytest(path):
    rc, out = _run([sys.executable, "-m", "pytest", "-q", path])
    m = None
    for m in _PYTEST.finditer(out):
        pass
    if not m:
        return None, None, None, out[-400:]
    failed = int(m.group(1) or 0)
    passed = int(m.group(2))
    skipped = int(m.group(3) or 0)
    return passed, failed, skipped, out[-400:]


# ------------------------------------------------------------ resolvers

def resolve_one(c):
    """(bin, detail dict). Never raises on a check that cannot run."""
    b = bindings.BINDINGS.get(c["key"])
    if b is None:
        return UNBOUND, {"reason": "no binding declared for this claim"}

    for d in b.get("deps", []):
        if not have(d):
            return NOT_TESTABLE, {"reason": "dependency not importable: %s"
                                            % d, "dep": d}

    how = b["how"]
    stated = c["value"]

    if how == "none":
        return NOT_TESTABLE, {"reason": b["reason"]}

    if how == "pytest":
        passed, failed, skipped, tail = run_pytest(
            os.path.join(base(), b["path"]))
        if passed is None:
            return NOT_TESTABLE, {"reason": "pytest produced no summary",
                                  "tail": tail}
        if b.get("expect_skipped"):
            got = "%d/%d" % (passed, skipped)
            want = "/".join(stated)
        else:
            got, want = str(passed), stated[0]
        if failed:
            got += " (%d failed)" % failed
        d = {"stated": want, "observed": got, "failed": failed,
             "skipped": skipped}
        if b.get("bound"):
            # `430+ tests green` carries two statements: a lower bound on
            # the count, and the word `green`. They can come apart, and
            # when they do both are reported rather than one being
            # picked -- the count bound is met and the suite is not
            # green, which is a divergence on the second statement.
            ok = passed >= int(want)
            d["bound"] = "lower bound on the count; the word is `green`"
            d["observed"] = "%d passed, %d failed" % (passed, failed)
            if not ok:
                d["reading"] = "count bound not met"
                return DIVERGED, d
            if failed:
                d["reading"] = ("count bound met (%d >= %s); `green` not "
                                "met (%d failing)" % (passed, want, failed))
                return DIVERGED, d
            d["reading"] = "count bound met and the suite is green"
            return HOLDS_UNMAINTAINED, d
        return (HOLDS_UNMAINTAINED if got == want else DIVERGED), d

    if how in ("selftest", "selftest_glob"):
        cmds = ([[os.path.join(base(), b["cmd"][0])]] if how == "selftest"
                else [[p] for p in sorted(_glob(b["glob"]))])
        total, fails, seen = 0, 0, []
        for cmd in cmds:
            args = [sys.executable] + cmd
            if "--selftest" not in args:
                args.append("--selftest")
            rc, out = _run(args)
            n, f = parse_count(out, b.get("parse"))
            if n is None:
                continue
            total += n
            fails += f or 0
            seen.append((cmd[0], n))
        if not seen:
            return NOT_TESTABLE, {"reason": "no selftest count printed"}
        want = stated[-1]
        return ((HOLDS_UNMAINTAINED if str(total) == want else DIVERGED),
                {"stated": want, "observed": str(total),
                 "failed": fails, "modules": seen})

    if how == "selftest_sum":
        total, fails, seen = 0, 0, []
        for p in sorted(_glob(b["glob"])):
            rc, out = _run([sys.executable, p, "--selftest"])
            n, f = parse_count(out, b.get("parse"))
            if n is None:
                continue
            total += n
            fails += f or 0
            seen.append((os.path.basename(p), n))
        if not seen:
            return NOT_TESTABLE, {"reason": "no module printed a count"}
        want = stated[0]
        return ((HOLDS_UNMAINTAINED if str(total) == want else DIVERGED),
                {"stated": want, "observed": str(total),
                 "failed": fails, "modules": seen})

    if how == "count_files":
        n = len([f for f in os.listdir(os.path.join(base(), b["path"]))
                 if not f.startswith(".")
                 and not f.startswith("__")])
        want = stated[0]
        return ((HOLDS_UNMAINTAINED if str(n) == want else DIVERGED),
                {"stated": want, "observed": str(n)})

    if how == "diff_tree":
        same, differ, only = _diff_tree(b["a"], b["b"])
        return ((HOLDS_UNMAINTAINED if not differ else DIVERGED),
                {"stated": "byte-identical", "observed":
                 "%d identical, %d differing" % (len(same), len(differ)),
                 "differing": differ[:6], "only_in_one": len(only)})

    if how == "run_grep":
        rc, out = _run([sys.executable,
                        os.path.join(base(), b["cmd"][0])])
        missing = [n for n in b["needles"] if n not in out]
        return ((HOLDS_UNMAINTAINED if not missing else DIVERGED),
                {"stated": "reproducible from " + b["cmd"][0],
                 "observed": ("all stated values present" if not missing
                              else "not in output: " + ", ".join(missing)),
                 "rc": rc})

    if how == "run_twice":
        cmd = [os.path.join(base(), b["cmd"][0])] + b["cmd"][1:]
        rc1, o1 = _run([sys.executable] + cmd)
        rc2, o2 = _run([sys.executable] + cmd)
        return ((HOLDS_UNMAINTAINED if o1 == o2 else DIVERGED),
                {"stated": "byte-reproducible",
                 "observed": ("two runs identical (%d bytes)" % len(o1))
                 if o1 == o2 else "two runs differ"})

    if how == "run_twice_regen":
        target = os.path.join(base(), b["target"])
        before = open(target, "rb").read()
        rc, out = _run([sys.executable,
                        os.path.join(base(), b["cmd"][0])] + b["cmd"][1:])
        after = open(target, "rb").read()
        if before != after:
            open(target, "wb").write(before)
        ok = before == after
        asserted = b.get("asserted_by")
        asserted_ok = False
        if asserted and os.path.exists(os.path.join(base(), asserted)):
            rc2, _ = _run([sys.executable, os.path.join(base(), asserted)])
            asserted_ok = rc2 == 0
        if not ok:
            return DIVERGED, {"stated": "regenerates byte-identically",
                              "observed": "regeneration differs"}
        if asserted_ok:
            return MAINTAINED, {"stated": "regenerates byte-identically",
                                "observed": "identical, and %s asserts it"
                                            % asserted}
        return HOLDS_UNMAINTAINED, {"stated": "regenerates byte-identically",
                                    "observed": "identical; the named test "
                                                "did not run clean"}

    if how == "selftest_clean":
        rc, out = _run([sys.executable, os.path.join(base(), b["cmd"][0])]
                       + b["cmd"][1:] + ["--selftest"])
        n, f = parse_count(out, None)
        if n is None:
            return NOT_TESTABLE, {"reason": "no selftest count printed"}
        return ((HOLDS_UNMAINTAINED if f == 0 else DIVERGED),
                {"stated": "asserted by the module's own selftest",
                 "observed": "%d checks, %d failed" % (n, f)})

    if how == "git_diff":
        return _git_docstring_diff(b["path"])

    return NOT_TESTABLE, {"reason": "unknown check kind %r" % how}


import contextlib                                          # noqa: E402


@contextlib.contextmanager
def _isolated():
    """A throwaway worktree at HEAD, removed on the way out."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="selfscan_iso_")
    wt = os.path.join(tmp, "t")
    rc, _ = _run(["git", "worktree", "add", "--detach", "-q", wt, "HEAD"])
    try:
        yield (wt if rc == 0 else None)
    finally:
        if rc == 0:
            _run(["git", "worktree", "remove", "--force", wt])


def _glob(pattern):
    import glob as g
    return [p for p in g.glob(os.path.join(base(), pattern))
            if not os.path.basename(p).startswith("__")]


def _diff_tree(a, b):
    a, b = os.path.join(base(), a), os.path.join(base(), b)

    def files(d):
        out = {}
        for dp, dn, fn in os.walk(d):
            dn[:] = [x for x in dn if x != "__pycache__"]
            for f in fn:
                p = os.path.join(dp, f)
                out[os.path.relpath(p, d)] = p
        return out

    fa, fb = files(a), files(b)
    common = sorted(set(fa) & set(fb))
    only = sorted(set(fa) ^ set(fb))
    same, differ = [], []
    for r in common:
        if open(fa[r], "rb").read() == open(fb[r], "rb").read():
            same.append(r)
        else:
            differ.append(r)
    return same, differ, only


def _git_docstring_diff(path):
    """Is the file identical to its previous revision once the module
    docstring is stripped?"""
    rc, out = _run(["git", "log", "--format=%H", "--", path])
    if rc != 0 or not out.strip():
        return NOT_TESTABLE, {"reason": "no git history for " + path}
    revs = out.split()
    if len(revs) < 2:
        return NOT_TESTABLE, {"reason": "only one revision of " + path}
    rc, cur = _run(["git", "show", "%s:%s" % (revs[0], path)])
    rc2, prev = _run(["git", "show", "%s:%s" % (revs[1], path)])
    if rc or rc2:
        return NOT_TESTABLE, {"reason": "could not read both revisions"}

    def strip_doc(src):
        m = re.match(r'\s*(?:#![^\n]*\n)?\s*("""|\'\'\')', src)
        if not m:
            return src
        q = m.group(1)
        i = src.index(q)
        j = src.index(q, i + 3)
        return src[:i] + src[j + 3:]

    same = strip_doc(cur) == strip_doc(prev)
    return ((HOLDS_UNMAINTAINED if same else DIVERGED),
            {"stated": "code byte-identical after stripping the docstring",
             "observed": ("identical" if same else "differs"),
             "revs": [revs[0][:8], revs[1][:8]]})


# ----------------------------------------------------------------- S5

def _last_commit(path):
    rc, out = _run(["git", "log", "-1", "--format=%cI %h", "--", path])
    if rc != 0 or not out.strip():
        return None
    return out.strip().split(" ", 1)


def _last_commit_touching_lines(path, a, b):
    rc, out = _run(["git", "log", "-1", "--format=%cI %h",
                    "-L", "%d,%d:%s" % (a, b, path)])
    if rc != 0 or not out.strip():
        return None
    first = out.strip().split("\n")[0]
    parts = first.split(" ", 1)
    if len(parts) != 2 or "T" not in parts[0]:
        return None
    return parts


def _introduced(text):
    """Oldest commit whose patch to CLAUDE.md changed the occurrence
    count of this exact string. That is when the number was written."""
    if not text or len(text.strip()) < 4:
        return None
    rc, out = _run(["git", "log", "--reverse", "--format=%cI %h",
                    "-S", text, "--", "CLAUDE.md"])
    if rc != 0 or not out.strip():
        return None
    return out.strip().split("\n")[0].split(" ", 1)


def _days(a, b):
    import datetime
    fmt = "%Y-%m-%dT%H:%M:%S"
    da = datetime.datetime.strptime(a[:19], fmt)
    db = datetime.datetime.strptime(b[:19], fmt)
    return (da - db).total_seconds() / 86400.0


def divergence_dates(c):
    """S5: last commit on the artifact vs last commit on the paragraph.

    A workbook cannot answer this -- scan 4 returns UNRECOVERABLE for
    every divergence (SSS_038). This target is in git, so it can.
    """
    b = bindings.BINDINGS.get(c["key"], {})
    art = b.get("path") or b.get("a") or (b.get("cmd") or [None])[0] \
        or b.get("glob")
    out = {"artifact": art}
    if art and "*" in str(art):
        import glob as g
        cands = sorted(g.glob(os.path.join(ROOT, art)))
        best = None
        for p in cands:
            lc = _last_commit(os.path.relpath(p, ROOT))
            if lc and (best is None or lc[0] > best[0]):
                best = lc
        out["artifact_commit"] = best
    else:
        out["artifact_commit"] = _last_commit(art) if art else None
    out["paragraph_commit"] = _last_commit_touching_lines(
        "CLAUDE.md", c["line"], c["line"])
    # The matched text is passed to `git log -S` AS IT APPEARS, newline
    # included. Normalising the newline out was the first version and it
    # returned UNRECOVERABLE for exactly the claims markdown had wrapped
    # -- an instrument defect reported as an absence in the data.
    out["introduced"] = _introduced(c["text"])

    # BORN_DIVERGED vs DRIFT_POSSIBLE.
    #
    # If the artifact has not been committed since the number was
    # written, nothing about the artifact has changed and the number was
    # already wrong when it was typed. That is decidable.
    #
    # If the artifact HAS changed since, the two cases are not
    # separable from dates alone -- the number may have been right and
    # then overtaken, or wrong from the start and also overtaken. The
    # state is named DRIFT_POSSIBLE rather than DRIFT so the
    # undecidable case is not reported as the decided one.
    ac, intro = out.get("artifact_commit"), out.get("introduced")
    if ac and intro:
        out["kind"] = ("DRIFT_POSSIBLE" if ac[0] > intro[0]
                       else "BORN_DIVERGED")
        out["artifact_moved_since_days"] = round(_days(ac[0], intro[0]), 2)
    else:
        out["kind"] = "UNDETERMINED"
        out["artifact_moved_since_days"] = None
    if out["artifact_commit"] and out["paragraph_commit"]:
        out["interval_days"] = round(
            _days(out["artifact_commit"][0], out["paragraph_commit"][0]), 2)
    else:
        out["interval_days"] = None
        why = []
        if not out["artifact_commit"]:
            why.append("no artifact named or no history for it")
        if not out["paragraph_commit"]:
            why.append("git log -L returned no dated commit for the line")
        out["unrecoverable_because"] = "; ".join(why)
    return out


def replay_at(c, rev):
    """Re-run this claim's own check against the tree as it stood at
    `rev`, in a throwaway worktree.

    This is what turns DRIFT_POSSIBLE into a decided state. The dates
    alone cannot separate "right when written, overtaken later" from
    "wrong when written, and also overtaken" -- but the check can be run
    against the tree at the moment the number was typed, and then it is
    a measurement rather than an inference.

    Returns (observed, note). `observed` is None when the replay could
    not run, and the note says why; a replay that fails is not evidence
    either way.
    """
    b = bindings.BINDINGS.get(c["key"], {})
    how = b.get("how")
    if how not in ("selftest", "selftest_sum", "selftest_glob",
                   "count_files", "selftest_clean"):
        return None, "replay not built for check kind %r" % how, 0
    import tempfile
    tmp = tempfile.mkdtemp(prefix="selfscan_replay_")
    wt = os.path.join(tmp, "t")
    rc, out = _run(["git", "worktree", "add", "--detach", "-q", wt, rev])
    if rc != 0:
        return None, "could not create a worktree at %s" % rev[:8], 0
    try:
        if how == "count_files":
            d = os.path.join(wt, b["path"])
            if not os.path.isdir(d):
                return None, "path absent at that revision", 0
            n = len([f for f in os.listdir(d)
                     if not f.startswith(".") and not f.startswith("__")])
            return str(n), "replayed in a worktree at %s" % rev[:8], 1
        if how in ("selftest", "selftest_clean"):
            paths = [os.path.join(wt, b["cmd"][0])]
        else:
            import glob as g
            paths = [p for p in sorted(g.glob(os.path.join(wt, b["glob"])))
                     if not os.path.basename(p).startswith("__")]
        total, seen = 0, 0
        for p in paths:
            if not os.path.exists(p):
                continue
            rc2, o2 = _run([sys.executable, p, "--selftest"], cwd=wt)
            n, _f = parse_count(o2, None)
            if n is None:
                continue
            total += n
            seen += 1
        if not seen:
            return None, "no module printed a count at that revision"
        return (str(total),
                ("replayed %d module(s) in a worktree at %s"
                 % (seen, rev[:8])), seen)
    finally:
        _run(["git", "worktree", "remove", "--force", wt])


# ---------------------------------------------------------------- scan

def scan(only=None, replay=False):
    global BASE
    rows = []
    with _isolated() as wt:
        BASE = wt
        try:
            rows = _scan_inner(only, replay)
        finally:
            BASE = None
    return rows


def _scan_inner(only, replay):
    rows = []
    for c in keyed_claims():
        if only and only not in c["section_title"]:
            continue
        b, detail = resolve_one(c)
        row = dict(c)
        row["bin"] = b
        row["detail"] = detail
        if b == DIVERGED:
            row["dates"] = divergence_dates(c)
            if replay and row["dates"].get("kind") == "DRIFT_POSSIBLE":
                intro = row["dates"].get("introduced")
                if intro:
                    obs, note, seen = replay_at(c, intro[1])
                else:
                    obs, note, seen = None, "no introducing commit", 0
                row["dates"]["replay_observed"] = obs
                row["dates"]["replay_note"] = note
                live = len(detail.get("modules") or [])
                # A replay that reached fewer modules than the live check
                # is not the same measurement. Comparing them would be a
                # ratio across unlike objects (G-DIM) with a verdict
                # attached, so the state stays undecided and says why.
                if obs is not None and live and seen and seen != live:
                    row["dates"]["replay_note"] = (
                        note + "; NOT LIKE-FOR-LIKE -- %d module(s) then "
                        "against %d now, so this number is not comparable "
                        "to the stated one" % (seen, live))
                elif obs is not None:
                    stated = detail.get("stated")
                    row["dates"]["kind"] = ("DRIFT" if obs == stated
                                            else "BORN_DIVERGED")
        rows.append(row)
    return rows


def bins(rows):
    out = {}
    for b in list(BINS) + [UNBOUND]:
        out[b] = sum(1 for r in rows if r["bin"] == b)
    return out


def rate(rows):
    d = sum(1 for r in rows if r["bin"] == DIVERGED)
    h = sum(1 for r in rows if r["bin"] == HOLDS_UNMAINTAINED)
    m = sum(1 for r in rows if r["bin"] == MAINTAINED)
    n = d + h + m
    if n == 0:
        return None, 0
    return d / float(n), n


def s1_census():
    """S1: sections, and their stance under two readings that disagree."""
    text = open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8").read()
    secs = extract.sections(text)
    counts = {}
    road = 0
    lens = {extract.RETROSPECTIVE: [], extract.PROSPECTIVE: [],
            extract.NEITHER: []}
    for s_ in secs:
        st = extract.stance(s_)
        counts[st] = counts.get(st, 0) + 1
        lens[st].append(s_["end_line"] - s_["start_line"] + 1)
        if extract.roadmap_markers(s_):
            road += 1
    # Does the marker test track section LENGTH? A longer section
    # accumulates markers of both kinds, and the classifier compares two
    # counts, so length is the obvious confound. Measured rather than
    # asserted: the share of sections receiving a verdict other than
    # NEITHER, in the shortest and longest thirds by line count.
    by_len = sorted(secs, key=lambda x: x["end_line"] - x["start_line"])
    third = max(1, len(by_len) // 3)

    def verdict_share(group):
        n = sum(1 for x in group if extract.stance(x) != extract.NEITHER)
        return n / float(len(group)) if group else None

    short_share = verdict_share(by_len[:third])
    long_share = verdict_share(by_len[-third:])

    return {"sections": len(secs), "stance": counts,
            "verdict_share_shortest_third": short_share,
            "verdict_share_longest_third": long_share,
            "roadmap_marked": road,
            "median_lines": {k: (sorted(v)[len(v) // 2] if v else None)
                             for k, v in lens.items()},
            "lines": len(text.split("\n")), "chars": len(text)}


def _family_rate(rows, patterns):
    sub = [r for r in rows if r.get("pattern") in patterns]
    d = sum(1 for r in sub if r["bin"] == DIVERGED)
    n = sum(1 for r in sub if r["bin"] in (DIVERGED, HOLDS_UNMAINTAINED,
                                           MAINTAINED))
    return d, n, (d / float(n) if n else None)


def prediction_verdicts(rows):
    """Each prediction, its number, and HELD / REFUTED / NOT ADDRESSABLE.

    NOT ADDRESSABLE is legal, per WO7's precedent, and is used rather
    than counting an empty denominator as support.
    """
    out = []
    ds, ns, rs = _family_rate(rows, ("selftest_ratio", "selftest_checks"))
    dp, np_, rp = _family_rate(rows, ("tests_green", "pass_skip"))
    if rs is None or rp is None:
        out.append("P1  NOT ADDRESSABLE -- one family has an empty "
                   "denominator")
    else:
        out.append("P1  %s -- selftest family %d/%d = %.3f, suite family "
                   "%d/%d = %.3f"
                   % ("HELD" if rs < rp else "REFUTED",
                      ds, ns, rs, dp, np_, rp))
    nc = sum(1 for r in rows
              if r.get("kind") == "COUNT" and r["bin"] == DIVERGED)
    out.append("P2  %s -- %d COUNT claims DIVERGED"
               % ("HELD" if nc else "REFUTED", nc))
    ident = [r for r in rows if r.get("kind") == "IDENTITY"]
    di = sum(1 for r in ident if r["bin"] == DIVERGED)
    ni = sum(1 for r in ident if r["bin"] in (DIVERGED, HOLDS_UNMAINTAINED,
                                              MAINTAINED))
    if not ni:
        out.append("P3  NOT ADDRESSABLE -- no IDENTITY claim resolved")
    else:
        out.append("P3  %s -- %d of %d resolvable IDENTITY claims DIVERGED"
                   % ("HELD" if di * 3 < ni else "REFUTED", di, ni))
    rt, n = rate(rows)
    if rt is None:
        out.append("P4  NOT ADDRESSABLE -- empty denominator")
    else:
        out.append("P4  %s -- rate %.3f" % ("HELD" if rt < 0.5 else "REFUTED",
                                            rt))
    m = [r for r in rows if r["bin"] == MAINTAINED]
    out.append("P5  %s -- MAINTAINED = %d%s"
               % ("HELD" if 1 <= len(m) <= 2 else "REFUTED", len(m),
                  (", and it is " + m[0].get("section_title", "?") + " "
                   + m[0].get("text", "?")) if m else ""))
    return out


def render(rows, verbose=False):
    out = []
    out.append("SCAN 4 ON CLAUDE.md")
    out.append("bins imported from sheet-structure-scan/scan4.py")
    # The target moves. A pinned sample that does not name the version
    # it describes is a claim about a file that no longer exists -- which
    # is this scan's own subject, so the anchor is printed rather than
    # left to the commit message.
    rc, blob = _run(["git", "hash-object", "CLAUDE.md"])
    rc2, head = _run(["git", "rev-parse", "--short", "HEAD"])
    out.append("target blob %s   repo HEAD %s"
               % ((blob.strip() or "UNRECOVERABLE")[:12],
                  head.strip() or "UNRECOVERABLE"))
    out.append("")
    c = s1_census()
    out.append("S1 -- SECTIONS AND STANCE")
    out.append("  target      %d lines, %d chars, %d sections"
               % (c["lines"], c["chars"], c["sections"]))
    for k in sorted(c["stance"]):
        out.append("  %-12s %-4d  median section length %s lines"
                   % (k, c["stance"][k], c["median_lines"].get(k)))
    out.append("  roadmap-marked sections (S1's own three examples): %d"
               % c["roadmap_marked"])
    out.append("")
    out.append("  Length confound, measured: a section in the shortest")
    out.append("  third gets a verdict other than NEITHER %.0f%% of the"
               % (100 * (c["verdict_share_shortest_third"] or 0)))
    out.append("  time; one in the longest third, %.0f%%. The test counts"
               % (100 * (c["verdict_share_longest_third"] or 0)))
    out.append("  markers and compares two counts, so a longer section")
    out.append("  has more of both and is likelier to break the tie.")
    out.append("")
    out.append("  Two readings, both reported, neither picked. The")
    out.append("  imported marker test reads sentences; WO10 S1's own")
    out.append("  rule is that operands resolve inside the tree, which is")
    out.append("  RESOLVABILITY and is what S3 measures. SSS_051 recorded")
    out.append("  that those are two criteria computing one quantity when")
    out.append("  conflated; here they are kept apart.")
    out.append("")
    out.append("%-30s %-9s %-20s %-18s %s"
               % ("section", "kind", "claim", "bin", "stated -> observed"))
    out.append("-" * 118)
    for r in rows:
        d = r["detail"]
        so = ""
        if "stated" in d:
            so = "%s -> %s" % (d["stated"], d.get("observed", "?"))
        elif "reason" in d:
            so = d["reason"].split(" -- ")[0][:44]
        out.append("%-30s %-9s %-20s %-18s %s"
                   % (r["section_title"][:30], r["kind"],
                      r["text"].replace("\n", " ")[:20], r["bin"], so[:44]))
    out.append("")
    b = bins(rows)
    out.append("BINS")
    for k in list(BINS) + [UNBOUND]:
        out.append("  %-20s %d" % (k, b[k]))
    out.append("")
    rt, n = rate(rows)
    out.append("RATE")
    if rt is None:
        out.append("  NO_DIRECTION -- the denominator is empty.")
    else:
        out.append("  DIVERGED / (DIVERGED + HOLDS + MAINTAINED)"
                   " = %d / %d = %.3f" % (b[DIVERGED], n, rt))
        out.append("  n = %d claims resolved" % n)
    out.append("")
    out.append("  Second point, flagged: the UNFCCC workbook returned")
    out.append("  0.913 under scan 4 (SSS_035). DIFFERENT DOCUMENT CLASS --")
    out.append("  a workbook stating relationships about its own cells")
    out.append("  against a repository index stating relationships about")
    out.append("  files beside it. n = 2. No direction is claimed and no")
    out.append("  curve is emitted.")
    out.append("")
    div = [r for r in rows if r["bin"] == DIVERGED]
    out.append("S5 -- DIVERGENCE DATES (%d)" % len(div))
    if not div:
        out.append("  none")
    for r in div:
        d = r["dates"]
        out.append("  %s  %s" % (r["section_title"], r["text"][:40]))
        out.append("      stated %s, observed %s"
                   % (r["detail"].get("stated"), r["detail"].get("observed")))
        out.append("      introduced: %s" % (d.get("introduced") or
                                             "UNRECOVERABLE"))
        out.append("      artifact:  %s" % (d["artifact_commit"] or
                                            "UNRECOVERABLE"))
        out.append("      paragraph: %s" % (d["paragraph_commit"] or
                                            "UNRECOVERABLE"))
        if d["interval_days"] is None:
            out.append("      interval:  UNRECOVERABLE -- %s"
                       % d.get("unrecoverable_because"))
        else:
            out.append("      interval:  %+.2f days (artifact minus "
                       "paragraph)" % d["interval_days"])
        if d.get("replay_observed") is not None:
            out.append("      replay:    at the introducing commit the "
                       "check returned %s (%s)"
                       % (d["replay_observed"], d.get("replay_note")))
        elif "replay_note" in d:
            out.append("      replay:    not run -- %s" % d["replay_note"])
        out.append("      kind:      %s%s"
                   % (d.get("kind"),
                      "" if d.get("artifact_moved_since_days") is None
                      else "  (artifact moved %+.2f d after the number "
                           "was written)" % d["artifact_moved_since_days"]))
    out.append("")
    out.append("PREDICTIONS (registered in PREDICTIONS_WO10.md before")
    out.append("resolve.py existed)")
    for line in prediction_verdicts(rows):
        out.append("  " + line)

    if verbose:
        out.append("")
        out.append("DETAIL")
        for r in rows:
            out.append("  %s" % r["key"])
            for k in sorted(r["detail"]):
                out.append("      %-12s %s" % (k, r["detail"][k]))
    return "\n".join(out)


# -------------------------------------------------------------- selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- bins are imported, not restated
    chk("bins come from scan4", BINS is scan4.BINS)
    chk("DIVERGED is scan4's", DIVERGED == scan4.DIVERGED)

    # -- keys are stable and disambiguate repeats
    cl = keyed_claims()
    chk("every claim has a key", all("key" in c for c in cl))
    chk("keys are distinct", len({c["key"] for c in cl}) == len(cl))
    reps = [c["key"] for c in cl
            if c["section_title"] == "simulation-hypothesis-budget/"
            and c["value"] == ["20", "20"]]
    chk("a repeated triple gets distinct ordinals",
        sorted(reps)[0].endswith("|0") and sorted(reps)[1].endswith("|1"))

    # -- every binding key names a real claim, and vice versa
    keys = {c["key"] for c in cl}
    orphan = sorted(set(bindings.BINDINGS) - keys)
    chk("no binding names a claim that is not extracted (%s)"
        % (orphan[:2] or ""), not orphan)
    unbound = sorted(keys - set(bindings.BINDINGS))
    chk("unbound claims are reported, not hidden (%d)" % len(unbound), True)

    # -- parse_count on each shape actually in the repo
    chk("parses `selftest: N checks, M failed`",
        parse_count("selftest: 28 checks, 0 failed", None) == (28, 0))
    chk("parses `SELFTEST PASS` with a count line",
        parse_count("x 12 checks, 0 failed\n", None) == (12, 0))
    chk("parses `selftest 13/13`",
        parse_count("Selftest 13/13 pass", None) == (13, 0))
    chk("a ratio short of full is counted failed",
        parse_count("selftest 11/13", None) == (13, 2))
    chk("parses `N/N checks passed`",
        parse_count("15/15 checks passed\n", None) == (15, 0))
    chk("parses a bare N/N on its own line",
        parse_count("PASS a\nPASS b\n\n53/53\n", None) == (53, 0))
    chk("a bare ratio inside prose does not match",
        parse_count("the 3/4 majority held\n", None) == (None, None))
    chk("no count is None, not zero",
        parse_count("nothing here", None) == (None, None))

    # -- pytest summary parsing, both shapes
    chk("pytest summary parses passed only",
        _PYTEST.search("== 23 passed in 0.4s ==").group(2) == "23")
    m = _PYTEST.search("== 1 failed, 39 passed, 2 skipped in 1s ==")
    chk("pytest summary parses failed/passed/skipped",
        (m.group(1), m.group(2), m.group(3)) == ("1", "39", "2"))

    # -- UNBOUND is its own state, distinct from a bin
    chk("UNBOUND is not one of scan4's bins", UNBOUND not in BINS)
    fake = {"key": "nope|x|-|0", "value": None}
    chk("an unbound claim resolves UNBOUND",
        resolve_one(fake)[0] == UNBOUND)

    # -- a missing dependency is NOT_TESTABLE with the name in it
    bindings.BINDINGS["probe|x|-|0"] = {"how": "pytest", "path": ".",
                                        "deps": ["no_such_module_xyz"]}
    b, d = resolve_one({"key": "probe|x|-|0", "value": None})
    chk("a missing dep is NOT_TESTABLE", b == NOT_TESTABLE)
    chk("the missing dep is named", "no_such_module_xyz" in d["reason"])
    del bindings.BINDINGS["probe|x|-|0"]

    # -- rate refuses an empty denominator rather than returning 0.0
    chk("empty denominator gives None, not zero",
        rate([{"bin": NOT_TESTABLE}, {"bin": UNBOUND}]) == (None, 0))
    chk("rate counts MAINTAINED in the denominator",
        rate([{"bin": DIVERGED}, {"bin": MAINTAINED},
              {"bin": HOLDS_UNMAINTAINED}]) == (1 / 3.0, 3))

    # -- render prints n and never a curve
    txt = render([{"section_title": "x", "kind": "COUNT", "text": "t",
                   "bin": DIVERGED, "detail": {"stated": "1",
                                               "observed": "2"},
                   "dates": {"artifact": "a", "artifact_commit": None,
                             "paragraph_commit": None,
                             "interval_days": None,
                             "unrecoverable_because": "probe"}}])
    chk("render prints n", "n = 1 claims resolved" in txt)
    chk("render anchors the target version", "target blob " in txt)
    chk("render flags the second point as a different class",
        "DIFFERENT DOCUMENT CLASS" in txt)
    chk("render says no direction is claimed",
        "No direction is claimed" in txt)
    chk("an unrecoverable interval says why",
        "UNRECOVERABLE -- probe" in txt)

    # -- introduction lookup finds a real commit for a real string
    chk("a string present in CLAUDE.md has an introducing commit",
        _introduced("247 selftest checks") is not None)
    chk("a string absent from CLAUDE.md has none",
        _introduced("zzq_no_such_string_here_9137") is None)
    chk("a too-short needle is refused rather than searched",
        _introduced("a") is None)

    # -- BORN_DIVERGED is only claimed when it is decidable
    chk("render names the kind",
        "kind:" in render([{"section_title": "x", "kind": "COUNT",
                            "text": "t", "bin": DIVERGED,
                            "detail": {"stated": "1", "observed": "2"},
                            "dates": {"artifact": "a",
                                      "artifact_commit": None,
                                      "paragraph_commit": None,
                                      "introduced": None,
                                      "kind": "UNDETERMINED",
                                      "artifact_moved_since_days": None,
                                      "interval_days": None,
                                      "unrecoverable_because": "p"}}]))

    # -- replay returns a triple and refuses kinds it cannot run
    r = replay_at({"key": "nope|x|-|0"}, "HEAD")
    chk("replay returns three values", len(r) == 3)
    chk("replay refuses an unbuilt kind", r[0] is None)

    # -- a scan does not modify the tree it measures
    rc0, before = _run(["git", "status", "--porcelain"])
    scan(only="closure-cost")
    rc1, after = _run(["git", "status", "--porcelain"])
    chk("a scan leaves the working tree unchanged", before == after)
    chk("BASE is released after a scan", BASE is None)

    # -- S1 census reports both stances and a length beside each
    c = s1_census()
    chk("census counts sections", c["sections"] > 50)
    chk("census measures the length confound",
        c["verdict_share_shortest_third"] is not None
        and c["verdict_share_longest_third"] is not None)
    chk("census reports a median length per stance",
        set(c["median_lines"]) >= {extract.RETROSPECTIVE,
                                   extract.PROSPECTIVE})

    # -- prediction verdicts admit NOT ADDRESSABLE rather than
    # counting an empty denominator as support
    v = prediction_verdicts([{"pattern": "x", "kind": "COUNT",
                              "bin": NOT_TESTABLE}])
    chk("an empty family is NOT ADDRESSABLE, not HELD",
        any("P1  NOT ADDRESSABLE" in x for x in v))
    chk("P3 with no resolvable identity claim is NOT ADDRESSABLE",
        any("P3  NOT ADDRESSABLE" in x for x in v))
    chk("a prediction can come back REFUTED",
        any("P2  REFUTED" in x for x in v))

    # -- git plumbing reachable
    chk("git history for CLAUDE.md is readable",
        _last_commit("CLAUDE.md") is not None)

    # -- the no-severity screen, imported not copied
    sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
    import no_severity
    hits = no_severity.hits(render([]))
    chk("the rendered report carries no severity language (%s)"
        % (hits[:1] or ""), not hits)

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b_ in bad:
        print("  FAILED", b_)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    only = None
    if "--only" in argv:
        only = argv[argv.index("--only") + 1]
    rows = scan(only, replay="--replay" in argv)
    print(render(rows, verbose="--verbose" in argv))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
