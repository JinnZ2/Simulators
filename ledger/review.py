#!/usr/bin/env python3
"""ADDENDUM.md, computed. The criterion is read out of that file, not retyped.

ADDENDUM.md is committed BEFORE the ledger runs and its own first rule is
that it is not edited after results. So this module never writes to it,
asserts its hash is unchanged across a run, and PARSES the three criteria
out of it rather than carrying a second copy that could drift.

WHAT IT DECIDES

    KEEP       >= 1 cross-ledger disagreement not explained by a
               rounding-mode difference in the ledger sources themselves
    DROP       0 disagreements AND cross-ledger runs completed on >= 3
               distinct machines or compiler versions
    UNDECIDED  fewer than 3 completed cross-ledger runs -- insufficient
               exposure, extend, do not conclude

A run in which the cobol arm was UNAVAILABLE is NOT a completed
cross-ledger run. It contributes no exposure. Counting it would let the
DROP branch fire on runs that could not have produced a disagreement.

THE ADDENDUM NAMES ITS OWN REAL SIGNAL AND IT IS THE ONE QUANTITY THIS
INSTRUMENT CANNOT OBSERVE. "Number of times a ledger red was overridden or
ignored" leaves no trace in the ledger: an override happens in a person's
head, or in a CI config, or in a commit that went in anyway. A gate that is
routinely overridden and a gate that never is look identical from inside
the gate. So the count is a DECLARED field, UNRECORDED is kept apart from
0, and OVERRIDES.md exists so the count can ever be anything but UNRECORDED.
The same holds for findings no other check found.

[CHOICE 9] lines of ledger source = every tracked .py and .cob under
ledger/; lines of sim source = every tracked .py outside ledger/, tools/
and tests/. Both file sets are printed, because the ratio is a property of
the denominator and the addendum does not fix one.

[CHOICE 10] Wall time is measured over whatever record set is given and the
report names it. A time over the fixtures is not a time over this repo's
claims.

    python3 ledger/review.py
    python3 ledger/review.py --time
    python3 ledger/review.py --record --overrides 0 --overrides-basis "..."

stdlib only. CC0.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

ADDENDUM = os.path.join(HERE, "ADDENDUM.md")
RUNS = os.path.join(HERE, "reviews", "RUNS.jsonl")
EXPLAINED = os.path.join(HERE, "reviews", "EXPLAINED.jsonl")
REVIEWS = os.path.join(HERE, "reviews", "REVIEWS.jsonl")
OVERRIDES = os.path.join(HERE, "OVERRIDES.md")
T0 = os.path.join(HERE, "reviews", "T0.txt")
DISAGREEMENTS = os.path.join(HERE, "DISAGREEMENTS.md")

UNRECORDED = "UNRECORDED"

# The vocabulary a disagreement can be explained by. UNEXPLAINED is the
# state that satisfies the KEEP criterion; ROUNDING_MODE is the one the
# criterion excludes by name.
EXPLANATIONS = ("ROUNDING_MODE", "SCALE", "OTHER", "UNEXPLAINED")


def addendum_hash() -> str:
    return hashlib.sha256(open(ADDENDUM, "rb").read()).hexdigest()


def criterion(path: str = ADDENDUM) -> Dict[str, Any]:
    """The three thresholds, read out of ADDENDUM.md.

    Parsed rather than retyped: a second copy of a number that must not
    change is a copy, and copies drift. If the parse fails the module says
    so and computes nothing, because guessing the threshold would be this
    instrument writing the criterion it exists to apply.
    """
    text = open(path, encoding="utf-8").read()
    out: Dict[str, Any] = {"ok": True, "problems": []}
    m = re.search(r"Review dates:\s*T\+(\d+)\s*weeks?,\s*T\+(\d+)\s*weeks?",
                  text)
    if m:
        out["t3_weeks"], out["t9_weeks"] = int(m.group(1)), int(m.group(2))
    else:
        out["problems"].append("review dates not found in ADDENDUM.md")
    m = re.search(r"KEEP the cobol_ledger if, by T\+(\d+):\s*\n\s*>=\s*(\d+)",
                  text)
    if m:
        out["keep_by_weeks"], out["keep_min"] = int(m.group(1)), int(m.group(2))
    else:
        out["problems"].append("KEEP criterion not found")
    m = re.search(r"DROP it if, by T\+(\d+):\s*\n\s*(\d+)\s+disagreements",
                  text)
    if m:
        out["drop_by_weeks"] = int(m.group(1))
        out["drop_max_disagreements"] = int(m.group(2))
    else:
        out["problems"].append("DROP criterion not found")
    m = re.search(r">=\s*(\d+)\s*\n?\s*distinct\s*\n?\s*machines", text)
    if m is None:
        m = re.search(r"machines or compiler versions", text)
        m2 = re.search(r">=\s*(\d+)\s+distinct", text)
        if m2:
            out["exposure_min"] = int(m2.group(1))
    else:
        out["exposure_min"] = int(m.group(1))
    m = re.search(r"fewer than (\d+) cross-ledger runs completed",
                  text)
    if m:
        out["undecided_below"] = int(m.group(1))
    else:
        out["problems"].append("UNDECIDED threshold not found")
    if "exposure_min" not in out:
        out["problems"].append("exposure threshold not found")
    out["ok"] = not out["problems"]
    return out


def read_jsonl(path: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    rows: List[Dict[str, Any]] = []
    bad: List[str] = []
    if not os.path.isfile(path):
        return rows, bad
    for i, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except ValueError as e:
            bad.append("%s:%d %s" % (os.path.basename(path), i, e))
            continue
        if isinstance(d, dict):
            rows.append(d)
        else:
            bad.append("%s:%d not an object" % (os.path.basename(path), i))
    return rows, bad


# T+3 and T+9 computed from the DATE THE ORDER WAS WRITTEN rather than
# from T. They are wrong while the clock has not started, they are in
# circulation, and they are named here so nobody carries them forward by
# accident. review.py computes the real pair from T0.txt and from nothing
# else.
SUPERSEDED_DATES = {"order_date": "2026-09-16",
                    "t3": "2026-10-07", "t9": "2026-11-18"}


def read_t0(path: str = T0) -> Optional[str]:
    """T, as written by the run that started the clock. The authority."""
    if not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8").read().strip().splitlines()
    if not text:
        return None
    try:
        datetime.date.fromisoformat(text[0].strip())
    except ValueError:
        return None
    return text[0].strip()


def clocks(runs: Sequence[Dict[str, Any]],
           t0_path: str = T0) -> Dict[str, Optional[str]]:
    """T from T0.txt, with the run log as a cross-check, never merged.

    T0.txt is the authority: it is written once, by the run that started
    the clock, and never overwritten. The run log's first
    non-empty-record date is computed separately and reported beside it,
    because a run over records that all declare themselves CONSTRUCTED is
    a non-empty record set that does NOT start the clock, and the two
    readings coming apart is a finding rather than something to average.
    """
    dates = sorted(r.get("date") for r in runs if r.get("date"))
    real = sorted(r.get("date") for r in runs
                  if r.get("date") and (r.get("records") or 0) > 0
                  and not r.get("all_constructed"))
    t0 = read_t0(t0_path)
    from_runs = real[0] if real else None
    out = {"t": t0,
           "t_any": dates[0] if dates else None,
           "t_from_runs": from_runs,
           "disagree": bool(t0 and from_runs and t0 != from_runs),
           "direction": None, "benign": None, "reading": []}
    if not out["disagree"]:
        return out

    # WHICH IS EARLIER is the whole content of the disagreement: the two
    # directions have different causes and only one of them is benign.
    # Neither is averaged into the other.
    if from_runs < t0:
        out["direction"] = "LOG_EARLIER"
        out["benign"] = True
        out["reading"] = [
            "the run log holds a real-record run BEFORE T0 was written.",
            "Records were reclassified out of CONSTRUCTED after the fact,",
            "so a run that did not start the clock then reads as one that",
            "could have. Expected, and benign: T is when the clock",
            "started, not when it could first have started.",
            "A second cause with the same signature: rows logged before",
            "all_constructed was a field read as not-all-constructed,",
            "because an absent field is not a False one. Check the row.",
        ]
    else:
        out["direction"] = "T0_EARLIER"
        out["benign"] = False
        out["reading"] = [
            "T0 is EARLIER than any real-record run in the log. NOT",
            "benign. Either T0 was written on a run whose records are",
            "CONSTRUCTED -- which [CHOICE 12] is supposed to prevent --",
            "or T0 was written wrongly, by hand or by a run whose log",
            "line was lost. T is the authority for the review dates, so",
            "a T that no run supports puts T+3 and T+9 on a date nothing",
            "happened. Settle it before either review.",
        ]
    return out


def exposure(runs: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Completed cross-ledger runs and the distinct contexts they covered."""
    done = [r for r in runs if r.get("cross_ledger") == "OK"]
    machines = sorted({r.get("machine") for r in done if r.get("machine")})
    compilers = sorted({r.get("cobc_version") for r in done
                        if r.get("cobc_version")})
    unavailable = [r for r in runs if r.get("cross_ledger") == "UNAVAILABLE"]
    return {"completed": len(done), "machines": machines,
            "compilers": compilers,
            "distinct": max(len(machines), len(compilers)),
            "unavailable": len(unavailable)}


def disagreement_state(runs_path: str = RUNS,
                       explained_path: str = EXPLAINED) -> Dict[str, Any]:
    """Disagreements found, and how many are classified.

    An unclassified disagreement is neither a KEEP nor a not-KEEP. The
    classification is a judgement about two ledger sources and is declared
    in reviews/EXPLAINED.jsonl with a basis; nothing here infers one.
    """
    runs, _ = read_jsonl(runs_path)
    found = sum(r.get("disagreements") or 0 for r in runs)
    rows, bad = read_jsonl(explained_path)
    classified, unexplained, malformed = 0, 0, []
    for d in rows:
        e = d.get("explained_by")
        if e not in EXPLANATIONS or not str(d.get("basis", "")).strip():
            malformed.append(str(d.get("ref", "?")))
            continue
        classified += 1
        if e == "UNEXPLAINED":
            unexplained += 1
    return {"found": found, "classified": classified,
            "unclassified": max(0, found - classified),
            "unexplained": unexplained, "malformed": malformed,
            "parse_errors": bad}


def review_dates(t: Optional[str], c: Dict[str, Any]) -> Dict[str, Any]:
    """T+3 and T+9, computed FROM T. Absent T, there are no dates.

    The pair that was computed from the order date is named as superseded
    rather than left out: a wrong number in circulation with nothing
    contradicting it stays in circulation.
    """
    if not t or not c.get("ok"):
        return {"t": t, "t3": None, "t9": None,
                "superseded": dict(SUPERSEDED_DATES)}
    d = datetime.date.fromisoformat(t)
    return {
        "t": t,
        "t3": (d + datetime.timedelta(weeks=c["t3_weeks"])).isoformat(),
        "t9": (d + datetime.timedelta(weeks=c["t9_weeks"])).isoformat(),
        "superseded": dict(SUPERSEDED_DATES),
    }


def weeks_since(t: Optional[str], today: str) -> Optional[float]:
    if not t:
        return None
    try:
        a = datetime.date.fromisoformat(t)
        b = datetime.date.fromisoformat(today)
    except ValueError:
        return None
    return (b - a).days / 7.0


def verdict(today: Optional[str] = None, runs_path: str = RUNS,
            explained_path: str = EXPLAINED,
            addendum_path: str = ADDENDUM,
            t0_path: str = T0) -> Dict[str, Any]:
    today = today or datetime.date.today().isoformat()
    c = criterion(addendum_path)
    if not c["ok"]:
        return {"verdict": "CRITERION_UNREADABLE", "why": c["problems"],
                "criterion": c}
    runs, run_bad = read_jsonl(runs_path)
    exp = exposure(runs)
    dis = disagreement_state(runs_path, explained_path)
    t = clocks(runs, t0_path)
    wk = weeks_since(t["t"], today)

    out: Dict[str, Any] = {
        "today": today, "criterion": c, "exposure": exp,
        "disagreements": dis, "clocks": t, "weeks_since_t": wk,
        "dates": review_dates(t["t"], c),
        "run_parse_errors": run_bad,
    }

    # The UNDECIDED branch is checked FIRST and on its own terms. It is the
    # one branch that does not depend on the disagreement count, and a
    # DROP read off insufficient exposure is the failure the addendum
    # names in the same sentence as the threshold.
    if exp["completed"] < c["undecided_below"]:
        out["verdict"] = "UNDECIDED"
        out["why"] = [
            "%d completed cross-ledger runs, fewer than %d"
            % (exp["completed"], c["undecided_below"]),
            "insufficient exposure: extend, do not conclude",
        ]
        if exp["unavailable"]:
            out["why"].append(
                "%d run(s) reported the cobol arm UNAVAILABLE. An "
                "unavailable arm is not a completed cross-ledger run and "
                "contributes no exposure." % exp["unavailable"])
        return out

    if dis["unclassified"] or dis["malformed"]:
        out["verdict"] = "UNDECIDED"
        out["why"] = [
            "%d disagreement(s) carry no classification in "
            "reviews/EXPLAINED.jsonl" % dis["unclassified"],
            "the KEEP criterion excludes rounding-mode differences by "
            "name, and whether a row is one is a judgement about the two "
            "ledger sources. Nothing here infers it.",
        ]
        if dis["malformed"]:
            out["why"].append("malformed classifications: %s"
                              % ", ".join(dis["malformed"]))
        return out

    if wk is not None and wk >= c["keep_by_weeks"] \
            and dis["unexplained"] >= c["keep_min"]:
        out["verdict"] = "KEEP"
        out["why"] = ["%d unexplained cross-ledger disagreement(s) by T+%d"
                      % (dis["unexplained"], c["keep_by_weeks"])]
        return out

    if wk is not None and wk >= c["drop_by_weeks"] \
            and dis["found"] <= c["drop_max_disagreements"] \
            and exp["distinct"] >= c["exposure_min"]:
        out["verdict"] = "DROP"
        out["why"] = [
            "%d disagreement(s) by T+%d over %d distinct machines or "
            "compiler versions"
            % (dis["found"], c["drop_by_weeks"], exp["distinct"])]
        return out

    out["verdict"] = "NOT_YET_DUE" if wk is not None else "CLOCK_NOT_STARTED"
    out["why"] = (
        ["T is the first run over a non-empty record set whose records "
         "are not all CONSTRUCTED, and there has not been one. The clock "
         "has not started, so T+3 and T+9 have no values yet."]
        if wk is None else
        ["%.1f weeks since T; the next decision point is T+%d"
         % (wk, c["keep_by_weeks"] if wk < c["keep_by_weeks"]
            else c["drop_by_weeks"])])
    return out


# ------------------------------------ the second channel: git, uncooperative

def git(args: Sequence[str], cwd: str) -> Tuple[int, str]:
    try:
        p = subprocess.run(["git"] + list(args), cwd=cwd,
                           capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as e:
        return 127, str(e)
    return p.returncode, p.stdout


def git_reachable(cwd: str = HERE) -> Tuple[bool, str]:
    rc, out = git(["rev-parse", "--show-toplevel"], cwd)
    if rc != 0 or not out.strip():
        return False, "git history is not reachable from %s" % cwd
    return True, out.strip()


def override_inferred(runs_path: str = RUNS, cwd: str = HERE,
                      overrides_rel: str = "ledger/OVERRIDES.md"
                      ) -> Dict[str, Any]:
    """Overrides read out of git history. No cooperation required.

    A red exit, then a commit touching a path the red flagged, with no
    OVERRIDES.md entry in between. That is an override that nobody logged,
    and it is visible without anybody agreeing to be visible -- which is
    what the declared channel cannot be.

    IT IS NEVER MERGED WITH THE DECLARED COUNT. One is what people said,
    the other is what the history shows; they answer different questions
    and a sum of them answers neither. This one has its own floor and its
    own ceiling: a red acted on outside git leaves nothing here, and a
    commit that touches a flagged path for an unrelated reason is counted
    when it should not be. It is a different instrument, not a better one.

    If git history is not reachable this returns GIT_UNREACHABLE and
    stops. It does not approximate one.
    """
    ok, root = git_reachable(cwd)
    if not ok:
        return {"status": "GIT_UNREACHABLE", "reason": root,
                "inferred": None}

    runs, _ = read_jsonl(runs_path)
    if not runs:
        # An empty or unreadable run log yields inferred 0, which reads
        # exactly like a clean history. Found by a test whose constructed
        # repo checked its own run log away: the channel reported 0
        # overrides over 0 runs and looked like agreement.
        return {"status": "NO_RUNS", "root": root, "reds": 0,
                "inferred": None,
                "reason": "no runs in %s: nothing to correlate against, "
                          "which is not the same as nothing to find"
                          % os.path.basename(runs_path),
                "rows": [], "logged": 0, "logged_rows": [],
                "uncorrelatable": [], "no_flagged_paths": []}
    reds = [r for r in runs if r.get("diffs_fired")]
    inferred: List[Dict[str, Any]] = []
    uncorrelatable: List[Dict[str, Any]] = []
    no_paths: List[str] = []
    logged: List[Dict[str, Any]] = []

    for r in reds:
        sha = r.get("commit")
        if not sha:
            uncorrelatable.append({"date": r.get("date"),
                                   "why": "no commit recorded for this run"})
            continue
        rc, _ = git(["merge-base", "--is-ancestor", sha, "HEAD"], root)
        if rc != 0:
            uncorrelatable.append(
                {"date": r.get("date"), "commit": sha,
                 "why": "not an ancestor of HEAD; history was rewritten or "
                        "the run was on another branch"})
            continue
        paths = r.get("flagged_paths") or []
        if not paths:
            no_paths.append(r.get("date") or "?")
            continue
        rc, out = git(["log", "--format=%H", "%s..HEAD" % sha, "--"]
                      + list(paths), root)
        if rc != 0:
            uncorrelatable.append({"date": r.get("date"), "commit": sha,
                                   "why": "git log failed"})
            continue
        touching = [line.strip() for line in out.splitlines() if line.strip()]
        if not touching:
            continue
        first = touching[-1]                      # git log is newest first
        rc, out2 = git(["log", "--format=%H", "%s..%s" % (sha, first), "--",
                        overrides_rel], root)
        entry = [x for x in out2.splitlines() if x.strip()] if rc == 0 else []
        row = {"red_date": r.get("date"), "red_commit": sha,
               "touching_commit": first, "paths": paths,
               "diffs": r.get("diffs_fired")}
        if entry:
            row["overrides_entry"] = entry[-1]
            logged.append(row)
        else:
            inferred.append(row)

    return {"status": "OK", "root": root,
            "reds": len(reds),
            "inferred": len(inferred), "rows": inferred,
            "logged": len(logged), "logged_rows": logged,
            "uncorrelatable": uncorrelatable,
            "no_flagged_paths": no_paths}


# ------------------------------------------------------------------ bulk

def tracked(pattern_ok) -> List[str]:
    try:
        out = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return []
    return [p for p in out.stdout.splitlines() if pattern_ok(p)]


def _lines(paths: Sequence[str]) -> int:
    n = 0
    for p in paths:
        full = os.path.join(ROOT, p)
        try:
            n += sum(1 for _ in open(full, encoding="utf-8",
                                     errors="replace"))
        except OSError:
            continue
    return n


def bulk(record_set: Optional[str] = None,
         with_time: bool = False) -> Dict[str, Any]:
    led = tracked(lambda p: p.startswith("ledger/")
                  and (p.endswith(".py") or p.endswith(".cob")))
    sim = tracked(lambda p: p.endswith(".py")
                  and not p.startswith(("ledger/", "tools/", "tests/")))
    l_lines, s_lines = _lines(led), _lines(sim)
    out: Dict[str, Any] = {
        "ledger_files": len(led), "ledger_lines": l_lines,
        "sim_files": len(sim), "sim_lines": s_lines,
        "ratio": (round(l_lines / s_lines, 6) if s_lines else None),
        "wall_seconds": None, "wall_over": None,
    }
    if with_time:
        rs = record_set or os.path.join(HERE, "fixtures", "records")
        tmp = tempfile.mkdtemp(prefix="ledger_time_")
        t0 = time.perf_counter()
        subprocess.run(
            [sys.executable, os.path.join(HERE, "ledger.py"),
             "--records", rs, "--expected", tmp, "--no-log"],
            capture_output=True, text=True)
        out["wall_seconds"] = round(time.perf_counter() - t0, 4)
        out["wall_over"] = os.path.relpath(rs, ROOT)
    return out


# ---------------------------------------------------------------- render

def render(v: Dict[str, Any], b: Dict[str, Any],
           reviews: Sequence[Dict[str, Any]]) -> str:
    L: List[str] = []
    a = L.append
    a("ADDENDUM REVIEW")
    a("=" * 70)
    a("addendum sha256  %s" % addendum_hash())
    a("date             %s" % v.get("today"))
    a("")
    a("VERDICT: %s" % v["verdict"])
    for w in v.get("why", []):
        a("  %s" % w)
    a("")
    e = v.get("exposure") or {}
    a("EXPOSURE")
    a("-" * 70)
    a("  completed cross-ledger runs   %s" % e.get("completed"))
    a("  runs with the arm UNAVAILABLE %s   (not exposure)"
      % e.get("unavailable"))
    a("  distinct machines             %s" % (e.get("machines") or "none"))
    a("  distinct compiler versions    %s" % (e.get("compilers") or "none"))
    a("")
    d = v.get("disagreements") or {}
    a("DISAGREEMENTS")
    a("-" * 70)
    a("  found                         %s" % d.get("found"))
    a("  classified                    %s" % d.get("classified"))
    a("  unclassified                  %s" % d.get("unclassified"))
    a("  unexplained (satisfy KEEP)    %s" % d.get("unexplained"))
    a("  a zero here is the reading, not the absence of one")
    a("")
    c = v.get("clocks") or {}
    dt = v.get("dates") or {}
    a("CLOCK")
    a("-" * 70)
    a("  T   (reviews/T0.txt)          %s" % (c.get("t") or "NOT STARTED"))
    a("  T+3                           %s" % (dt.get("t3") or "--"))
    a("  T+9                           %s" % (dt.get("t9") or "--"))
    a("  weeks since T                 %s"
      % ("--" if v.get("weeks_since_t") is None
         else "%.1f" % v["weeks_since_t"]))
    a("  first run of any kind         %s" % (c.get("t_any") or "none"))
    a("  first real-record run, from the run log  %s"
      % (c.get("t_from_runs") or "none"))
    if c.get("disagree"):
        a("")
        mark = "!!" if c.get("benign") is False else "--"
        a("  %s T0.txt and the run log disagree about T: %s"
          % (mark, c.get("direction")))
        a("     T0.txt  %s" % c.get("t"))
        a("     run log %s   (%s is earlier)"
          % (c.get("t_from_runs"),
             "the run log" if c.get("direction") == "LOG_EARLIER"
             else "T0.txt"))
        for line in c.get("reading") or []:
            a("     %s" % line)
        a("     Reported, not averaged. T0.txt stays the authority.")
    sup = dt.get("superseded") or {}
    a("")
    a("  SUPERSEDED, do not use: T+3 %s and T+9 %s were computed from the"
      % (sup.get("t3"), sup.get("t9")))
    a("  order date %s, not from T. They are wrong while the clock has"
      % sup.get("order_date"))
    a("  not started, and they are named here because a wrong number in")
    a("  circulation with nothing contradicting it stays in circulation.")
    a("")
    a("BULK")
    a("-" * 70)
    a("  ledger source   %5d lines over %3d files"
      % (b["ledger_lines"], b["ledger_files"]))
    a("  sim source      %5d lines over %3d files"
      % (b["sim_lines"], b["sim_files"]))
    a("  ratio           %s" % b["ratio"])
    if b["wall_seconds"] is None:
        a("  wall time       not measured this run (--time)")
    else:
        a("  wall time       %.4f s over %s" % (b["wall_seconds"],
                                                b["wall_over"]))
    last = reviews[-1] if reviews else {}
    a("  findings no other check found   %s"
      % last.get("unique_findings", UNRECORDED))
    a("")
    a("OVERRIDES -- TWO CHANNELS, NEVER MERGED")
    a("-" * 70)
    a("  DECLARED (self-reported)        %s"
      % last.get("overrides", UNRECORDED))
    a("    SELF-REPORTED. An unlogged override is indistinguishable from")
    a("    no override. Once nonzero this is a FLOOR, not a measurement.")
    a("    UNRECORDED means no basis was declared, not zero.")
    a("")
    oi = v.get("override_inferred") or {}
    if oi.get("status") == "GIT_UNREACHABLE":
        a("  INFERRED                        NOT AVAILABLE")
        a("    %s" % oi.get("reason"))
        a("    Not approximated. There is no second reading.")
    elif oi.get("status") == "NO_RUNS":
        a("  INFERRED                        NO RUNS")
        a("    %s" % oi.get("reason"))
    else:
        a("  INFERRED (git history)          %s" % oi.get("inferred"))
        a("    red exits: %s   of which logged in OVERRIDES.md: %s"
          % (oi.get("reds"), oi.get("logged")))
        for row in (oi.get("rows") or [])[:10]:
            a("    %s %s -> %s  %s"
              % (row["red_date"], (row["red_commit"] or "")[:8],
                 row["touching_commit"][:8], ",".join(row["paths"])[:40]))
        if oi.get("uncorrelatable"):
            a("    UNCORRELATABLE: %d red run(s)"
              % len(oi["uncorrelatable"]))
            for u in oi["uncorrelatable"][:5]:
                a("      %s  %s" % (u.get("date"), u.get("why")))
        if oi.get("no_flagged_paths"):
            a("    red runs flagging no path: %d"
              % len(oi["no_flagged_paths"]))
        a("    Its own floor and ceiling: a red acted on outside git leaves")
        a("    nothing here, and a commit touching a flagged path for an")
        a("    unrelated reason is counted when it should not be. A")
        a("    different instrument, not a better one.")
    a("")
    a("  The two numbers above are reported side by side and are never")
    a("  added, averaged or reconciled. One is what people said; the")
    a("  other is what the history shows.")
    a("")
    a("  ADDENDUM.md names the override count as the real signal: a gate")
    a("  that gets routinely overridden has become bulk regardless of what")
    a("  it catches. The declared channel cannot observe it -- an override")
    a("  happens outside the ledger and leaves no trace in it, so a gate")
    a("  routinely overridden and one never overridden look identical from")
    a("  inside the gate. OVERRIDES.md exists so the count can ever be a")
    a("  number at all.")
    a("")
    a("  The inferred channel does not close that gap. It observes a")
    a("  DIFFERENT quantity -- a signature in the history -- which")
    a("  overlaps the one the addendum asks for and is not it. That is")
    a("  why the two are reported apart.")
    a("")
    a("REVIEWS RECORDED: %d" % len(reviews))
    for r in reviews:
        a("  %s  %s" % (r.get("date"), r.get("label", "")))
    return "\n".join(L)


def record_review(args, v: Dict[str, Any], b: Dict[str, Any]) -> int:
    """Append one review. Refuses a count with no basis."""
    for field, basis in (("overrides", args.overrides_basis),
                         ("unique_findings", args.unique_findings_basis)):
        val = getattr(args, field)
        if val is None:
            sys.stderr.write(
                "REFUSED: --%s not given. It has no default: UNRECORDED and "
                "0 are different readings and the addendum asks for the "
                "number. Pass a count, or pass UNRECORDED with a basis.\n"
                % field.replace("_", "-"))
            return 2
        if not (basis or "").strip():
            sys.stderr.write(
                "REFUSED: --%s-basis is required. A count with no stated "
                "basis is a second guess dressed as a measurement.\n"
                % field.replace("_", "-"))
            return 2
        if val != UNRECORDED:
            try:
                int(val)
            except ValueError:
                sys.stderr.write("REFUSED: --%s must be an integer or %s\n"
                                 % (field.replace("_", "-"), UNRECORDED))
                return 2
    row = {
        "date": v["today"], "label": args.label or "",
        "addendum_sha256": addendum_hash(),
        "verdict": v["verdict"],
        "exposure": v.get("exposure"),
        "disagreements": v.get("disagreements"),
        "overrides": args.overrides,
        "overrides_basis": args.overrides_basis,
        "unique_findings": args.unique_findings,
        "unique_findings_basis": args.unique_findings_basis,
        "bulk": b,
        "override_inferred": v.get("override_inferred"),
    }
    os.makedirs(os.path.dirname(REVIEWS), exist_ok=True)
    with open(REVIEWS, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")

    # ADDENDUM.md: record the reading in DISAGREEMENTS.md whatever it is,
    # including zero. A zero reading is the result, not an absence of one.
    d = v.get("disagreements") or {}
    e = v.get("exposure") or {}
    with open(DISAGREEMENTS, "a", encoding="utf-8") as fh:
        fh.write(
            "\n### %s  %s\n\n"
            "- verdict: **%s**\n"
            "- disagreements found: **%s** "
            "(classified %s, unexplained %s)\n"
            "- completed cross-ledger runs: %s "
            "(%s with the arm UNAVAILABLE, which is not exposure)\n"
            "- distinct machines: %s; compiler versions: %s\n"
            "- ledger reds overridden or ignored: %s (%s)\n"
            "- findings no other check found: %s (%s)\n"
            % (row["date"], args.label or "reading", v["verdict"],
               d.get("found"), d.get("classified"), d.get("unexplained"),
               e.get("completed"), e.get("unavailable"),
               e.get("machines") or "none", e.get("compilers") or "none",
               args.overrides, args.overrides_basis,
               args.unique_findings, args.unique_findings_basis))
    print("recorded review %s (%s); reading appended to DISAGREEMENTS.md"
          % (row["date"], row["verdict"]))
    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--today", default=None)
    ap.add_argument("--time", action="store_true",
                    help="measure wall time of a full ledger run")
    ap.add_argument("--records", default=None,
                    help="record set to time over; default the fixtures")
    ap.add_argument("--record", action="store_true",
                    help="append a review to reviews/REVIEWS.jsonl")
    ap.add_argument("--label", default="")
    ap.add_argument("--overrides", default=None)
    ap.add_argument("--overrides-basis", default="")
    ap.add_argument("--unique-findings", default=None)
    ap.add_argument("--unique-findings-basis", default="")
    ap.add_argument("--selftest", action="store_true",
                    help="refused; see ledger/selftest_ledger.py")
    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.selftest:
        sys.stderr.write(
            "review.py does not carry its own checks. Run:\n"
            "    python3 ledger/selftest_ledger.py\n")
        return 2

    before = addendum_hash()
    v = verdict(args.today)
    v["override_inferred"] = override_inferred()
    b = bulk(args.records, args.time)
    reviews, _ = read_jsonl(REVIEWS)
    print(render(v, b, reviews))
    rc = 0
    if args.record:
        rc = record_review(args, v, b)
    if addendum_hash() != before:
        sys.stderr.write(
            "REFUSED: ADDENDUM.md changed during this run. It is committed "
            "in advance and is not edited after results.\n")
        return 2
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
