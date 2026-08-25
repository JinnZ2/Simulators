#!/usr/bin/env python3
"""
provenance -- work order 5. Model provenance, forward and retrospective.

Two halves that do not share a mechanism, deliberately.

FORWARD (S1) is a write. One line per session: date, model identifier as
SELF-REPORTED, repo, branch. There is no code path in this file that
derives a model identifier from anything except an argument handed to it.
That is the whole of S1's "do not infer from behaviour" -- not a rule the
author is asked to remember, but an absence of the function that would
break it.

RETROSPECTIVE (S2) is a read. It never writes to history and cannot: it
shells out to `git log` with read-only verbs and emits a table alongside.

WHAT S2 IS DOING, stated once. It maps a commit DATE to a model VERSION
under an assumption -- always current-at-the-time. That assumption is
the claim (S3), so every decoded row carries the assumption string with
it, and `assumption_check()` scores the assumption against the record
rather than presuming it.

THE TABLE. S2 asks for the release-date table for the model line. It is
not reachable from here (allowlist egress) and a table from memory is
this repository's ANC_010 status. `releases.json` therefore ships
OBSERVED BOUNDS taken from this repo's own trailers, labelled as such:
a first appearance is an UPPER BOUND on a release date, never the date.
Every run prints that inheritance.

NO GRADING (S4). Output is screened through no_severity, with the same
measured-exemption arrangement scan 4 uses: the vocabulary this tool must
emit is declared, and the selftest asserts it is the only thing that
fires.

CC0. stdlib only. Parses under Python 3.9.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, os.pardir, "sheet-structure-scan"))
import no_severity                                    # noqa: E402

SESSIONS = os.path.join(HERE, "sessions.jsonl")
RELEASES = os.path.join(HERE, "releases.json")

# ------------------------------------------------------------------ S3

ASSUMPTION = ("the session ran on the version current at the commit date "
              "(always current-at-the-time)")

# [CHOICE 1] a commit within this many days either side of a version
# boundary is AMBIGUOUS. The delivery says "within a switchover window"
# and does not size it. 1 is the smallest window a date-resolution record
# can express; a larger one is defensible and is a different reading, so
# it is printed into every report header.
SWITCHOVER_DAYS = 1

# ------------------------------------------------------------------ verdicts

SINGLE = "SINGLE"
AMBIGUOUS = "AMBIGUOUS"
NOT_DECODABLE = "NOT_DECODABLE"

# ------------------------------------------------------------------ S1 states

SELF_REPORTED = "self_reported"
UNKNOWN = "UNKNOWN"

# S1 says: if the build string is unavailable, write UNKNOWN. UNAVAILABLE
# and WITHHELD are not the same state and this repository has recorded
# that repair a dozen times (PB_004, GC_004, MD_002, CC_002, CA_002,
# UNI_021, CR_027, ...). A model that cannot report its build string and
# one that is operating under a constraint against writing it into a repo
# produce the same blank and different facts. A bare UNKNOWN with no
# reason is refused.
UNKNOWN_REASONS = ("NO_BUILD_STRING", "WITHHELD")


class RefusedToInfer(Exception):
    """Raised if a caller asks this module to guess a model identifier."""


# ------------------------------------------------------------------ S1

def open_line(date, repo, branch, model=None, reason=None):
    """One session record. Self-reported only.

    `model` is whatever the caller states. This function does not look at
    the environment, the git history, the behaviour of anything, or any
    other signal -- there is nothing here to look at it with. If `model`
    is absent the record is UNKNOWN and a reason from the closed
    vocabulary is required.
    """
    if model is not None and str(model).strip():
        return {"date": date, "repo": repo, "branch": branch,
                "model_self_reported": str(model).strip(),
                "source": SELF_REPORTED, "unknown_reason": None}
    if reason not in UNKNOWN_REASONS:
        raise ValueError(
            "UNKNOWN needs a reason from %s. A blank is not a state: "
            "'could not report' and 'did not write' are different facts."
            % (UNKNOWN_REASONS,))
    return {"date": date, "repo": repo, "branch": branch,
            "model_self_reported": UNKNOWN,
            "source": UNKNOWN, "unknown_reason": reason}


def infer_model(*a, **k):
    """S1: do not infer from behaviour. This is the refusal, in code."""
    raise RefusedToInfer(
        "S1 is self-report only. There is no inference path here, and one "
        "added later would make every prior row a different measurement.")


def append_session(rec, path=SESSIONS):
    with open(path, "a") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")
    return rec


def read_sessions(path=SESSIONS):
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(json.loads(line))
    return out


# ------------------------------------------------------------------ table

def load_table(path=RELEASES):
    d = json.load(open(path))
    rows = sorted(d["rows"], key=lambda r: r["first_seen"])
    return d, rows


def _dnum(s):
    """YYYY-MM-DD -> day ordinal. stdlib date without importing datetime
    formats; kept explicit so the arithmetic is readable."""
    y, m, dd = (int(x) for x in s.split("-"))
    # days-from-civil, Howard Hinnant's algorithm.
    y -= m <= 2
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m + (-3 if m > 2 else 9)) + 2) // 5 + dd - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


# ------------------------------------------------------------------ S2

def decode(date, rows, window=SWITCHOVER_DAYS):
    """Version implied by a date, as an INTERVAL. No pick is ever made.

    Returns a dict; `candidates` is a list and is the answer. A single
    candidate is still a list, so a caller cannot read a point out of an
    ambiguous row by accident.
    """
    d = _dnum(date)
    if not rows or d < _dnum(rows[0]["first_seen"]) - window:
        return {"date": date, "verdict": NOT_DECODABLE, "candidates": [],
                "why": "predates the earliest row in the table",
                "derivation": ASSUMPTION}
    cand = []
    for i, r in enumerate(rows):
        lo = _dnum(r["first_seen"])
        hi = _dnum(rows[i + 1]["first_seen"]) if i + 1 < len(rows) else None
        # in the row's own span, widened by the switchover window at both
        # ends, because a boundary is a boundary from both sides.
        if d >= lo - window and (hi is None or d <= hi + window - 1):
            cand.append(r["version"])
    if not cand:
        return {"date": date, "verdict": NOT_DECODABLE, "candidates": [],
                "why": "falls in no row's span",
                "derivation": ASSUMPTION}
    return {"date": date,
            "verdict": SINGLE if len(cand) == 1 else AMBIGUOUS,
            "candidates": cand,
            "why": ("one row spans this date" if len(cand) == 1 else
                    "within %d day(s) of a boundary; both candidates "
                    "stand and no pick is made" % window),
            "derivation": ASSUMPTION}


# ------------------------------------------------------------------ git

def git_log(repo=".", limit=None):
    """Read-only. Commits as (sha, date, stamp, stated_model_or_None).

    The full timestamp is carried alongside the short date because the
    two are used for different jobs and one is not enough for both. The
    TABLE is date-granular, so a decode can only ever be date-granular.
    The ASSUMPTION CHECK is an ordering question, and on this repository
    the boundary it has to order across lasts about five hours inside one
    calendar day -- so a day-resolution ordering reports three
    counterexamples that are an artifact of the reading, not of the
    record. A G-RES pair: the feature is hours, the instrument was days.
    Found on real data; no constructed fixture would have shown it.
    """
    fmt = "%H\x1f%ad\x1f%(trailers:key=Co-Authored-By,valueonly,separator=%x2C)\x1e"
    cmd = ["git", "-C", repo, "log", "--format=" + fmt, "--date=iso"]
    if limit:
        cmd += ["-n", str(limit)]
    raw = subprocess.check_output(cmd).decode("utf-8", "replace")
    out = []
    for rec in raw.split("\x1e"):
        rec = rec.strip("\n")
        if not rec.strip():
            continue
        parts = rec.split("\x1f")
        if len(parts) < 3:
            continue
        sha, stamp, trailer = parts[0], parts[1], parts[2]
        out.append((sha, stamp[:10], stamp, parse_trailer(trailer)))
    return out


def parse_trailer(trailer):
    """The stated model in a Co-Authored-By trailer, or None.

    This reads what a commit SAYS. It is not inference: the string was
    written by the session that made the commit, so it is S1's
    self-report arriving through a channel nobody designed for it.
    """
    t = (trailer or "").strip()
    if not t:
        return None
    for piece in t.split(","):
        piece = piece.strip()
        if "<" in piece:
            piece = piece.split("<")[0].strip()
        if piece.lower().startswith("claude "):
            rest = piece[len("claude "):].strip()
            if rest and rest[0].isdigit() or rest.split(" ")[0].lower() in (
                    "opus", "sonnet", "haiku", "fable"):
                return piece
    return None


# ------------------------------------------------------------------ check

def assumption_check(commits, rows=None):
    """S3: score the assumption instead of presuming it.

    'Always current-at-the-time' implies the stated version never goes
    backwards as dates advance. Every commit that states an earlier
    version after a later one has appeared is a counterexample, and the
    count is the reading.

    Ordering comes from the table's own first_seen ordering, so a table
    replaced with real release dates re-scores this for free.
    """
    if rows is None:
        _, rows = load_table()
    order = {r["version"]: i for i, r in enumerate(rows)}
    stated = [(c[2], c[1], c[3]) for c in commits if c[3] and c[3] in order]
    stated.sort(key=lambda x: x[0])
    peak, back = -1, []
    for _stamp, date, m in stated:
        i = order[m]
        if i < peak:
            back.append((date, m))
        peak = max(peak, i)
    return {"n_stated": len(stated), "n_backwards": len(back),
            "backwards": back,
            "holds": not back,
            "reading": ASSUMPTION}


def assumption_sensitivity(commits, rows):
    """How much of the refutation rests on how little.

    A counterexample count is a claim about the record and inherits the
    table it was scored against. One table row resting on a single commit
    can turn a monotone record into a heavily refuted one, and the count
    alone does not say so. This drops each row in turn and re-scores.

    It picks nothing. Both numbers are reported and the reading is the
    operator's.
    """
    out = []
    base = assumption_check(commits, rows)["n_backwards"]
    for r in rows:
        kept = [x for x in rows if x["version"] != r["version"]]
        n = assumption_check(commits, kept)["n_backwards"] if kept else 0
        out.append({"row": r["version"],
                    "row_rests_on": r.get("n_commits"),
                    "backwards_without_it": n,
                    "attributable": base - n})
    return {"base": base, "rows": out}


def verify(commits, rows, window=SWITCHOVER_DAYS):
    """Score the date-decode against the commits that state a version.

    A decode with no check set is unfalsifiable, so this is the arm that
    makes S2 a measurement rather than a rendering. AGREES / DISAGREES
    are about the DECODE, never about the commit.
    """
    agree = disagree = ambiguous_hit = ambiguous_miss = unstated = 0
    misses = []
    for sha, date, _stamp, stated in commits:
        if stated is None:
            unstated += 1
            continue
        d = decode(date, rows, window)
        if d["verdict"] == NOT_DECODABLE:
            disagree += 1
            misses.append((sha[:8], date, stated, "NOT_DECODABLE"))
        elif d["verdict"] == SINGLE:
            if d["candidates"][0] == stated:
                agree += 1
            else:
                disagree += 1
                misses.append((sha[:8], date, stated, d["candidates"][0]))
        else:
            if stated in d["candidates"]:
                ambiguous_hit += 1
            else:
                ambiguous_miss += 1
                misses.append((sha[:8], date, stated,
                               "|".join(d["candidates"])))
    return {"agree": agree, "disagree": disagree,
            "ambiguous_contains": ambiguous_hit,
            "ambiguous_excludes": ambiguous_miss,
            "unstated": unstated, "misses": misses}


# ------------------------------------------------------------------ S4 screen

# The vocabulary this tool must emit and cannot reword: NOT_DECODABLE is
# a verdict name from the delivered order. Declared and measured, the
# same arrangement scan 4 uses -- one arm masks it, one arm asserts it is
# the only thing that fires.
DELIVERED_VOCABULARY = ()


def screened(text):
    masked = text
    for tok in DELIVERED_VOCABULARY:
        masked = masked.replace(tok, "#" * len(tok))
    return no_severity.check(masked)


def exemption_is_only_delivered(text):
    toks = tuple(t.lower() for t in DELIVERED_VOCABULARY)
    for _, word, _ in no_severity.hits(text):
        if word.lower() not in toks:
            return False
    return True


# ------------------------------------------------------------------ render

def table(head, rows):
    cols = [len(str(h)) for h in head]
    for r in rows:
        for i, c in enumerate(r):
            cols[i] = max(cols[i], len(str(c)))
    out = ["  ".join(str(h).ljust(cols[i]) for i, h in enumerate(head)),
           "  ".join("-" * c for c in cols)]
    for r in rows:
        out.append("  ".join(str(c).ljust(cols[i]) for i, c in enumerate(r)))
    return "\n".join(out)


def _header(meta, window):
    kind = meta.get("table_kind")
    L = ["model provenance -- retrospective decode (S2)",
         "table kind        %s" % kind,
         "table source      %s" % meta.get("source"),
         "switchover window %d day(s) either side  [CHOICE 1]" % window,
         "derivation        %s" % ASSUMPTION,
         ""]
    if kind == "observed_bound":
        L += ["THE TABLE IS NOT RELEASE DATES. Each row is a first and last",
              "appearance in this repository's own trailers. A first",
              "appearance is an UPPER BOUND on a release date and is never",
              "the date: the version existed at least that early, and may",
              "have existed long before anyone committed under it. Every",
              "candidate below inherits that.",
              ""]
    return L


def render_decode(commits, meta, rows, window=SWITCHOVER_DAYS, per_commit=False):
    L = _header(meta, window)
    counts = {SINGLE: 0, AMBIGUOUS: 0, NOT_DECODABLE: 0}
    body = []
    for sha, date, _stamp, stated in commits:
        d = decode(date, rows, window)
        counts[d["verdict"]] += 1
        body.append([sha[:8], date, d["verdict"],
                     "|".join(d["candidates"]) or "-",
                     stated or "-"])
    L.append(table(["verdict", "commits"],
                   [[k, counts[k]] for k in (SINGLE, AMBIGUOUS,
                                             NOT_DECODABLE)]))
    L.append("")
    if per_commit:
        L.append(table(["commit", "date", "verdict", "candidates",
                        "stated in trailer"], body))
        L.append("")
    L += ["The decode table is stored alongside and is not written back",
          "into history (S2). Nothing here ranks a commit, and no version",
          "is scored against another (S4)."]
    return "\n".join(L)


def render_verify(commits, meta, rows, window=SWITCHOVER_DAYS):
    v = verify(commits, rows, window)
    a = assumption_check(commits)
    L = _header(meta, window)
    L += ["S2 scored against the commits that state a version.",
          "The statement comes from the Co-Authored-By trailer, which is",
          "S1's self-report arriving through a channel nobody designed for",
          "it. Where a decode is AMBIGUOUS no pick is made, so the two",
          "ambiguous rows below are reported apart from the single ones.",
          ""]
    L.append(table(["outcome", "commits"],
                   [["decode SINGLE, matches trailer", v["agree"]],
                    ["decode SINGLE, differs from trailer", v["disagree"]],
                    ["decode AMBIGUOUS, contains trailer",
                     v["ambiguous_contains"]],
                    ["decode AMBIGUOUS, excludes trailer",
                     v["ambiguous_excludes"]],
                    ["no version stated", v["unstated"]]]))
    L += ["", "S3 -- the assumption scored rather than presumed.",
          ""]
    L.append(table(["quantity", "value"],
                   [["commits stating a table version", a["n_stated"]],
                    ["stating an earlier version after a later one",
                     a["n_backwards"]],
                    ["assumption holds on this record", a["holds"]]]))
    if a["backwards"]:
        roll = {}
        for d, m in a["backwards"]:
            roll[(d, m)] = roll.get((d, m), 0) + 1
        L += ["", "counterexamples to the derivation, by date:"]
        L.append(table(["date", "stated", "commits"],
                       [[d, m, n] for (d, m), n in sorted(roll.items())]))

    sens = assumption_sensitivity(commits, rows)
    L += ["",
          "How much of that count rests on how little. Each table row is",
          "dropped in turn and the count re-scored. Nothing is picked here:",
          "both readings stand and which table to use is the operator's.",
          ""]
    L.append(table(["table row", "row rests on", "backwards without it",
                    "attributable to it"],
                   [[r["row"], r["row_rests_on"], r["backwards_without_it"],
                     r["attributable"]] for r in sens["rows"]]))
    if v["misses"]:
        L += ["", "commits where the decode and the trailer part company:"]
        L.append(table(["commit", "date", "trailer", "decode"],
                       [list(m) for m in v["misses"][:40]]))
        if len(v["misses"]) > 40:
            L.append("... %d more not listed" % (len(v["misses"]) - 40))
    return "\n".join(L)


def render_sessions(recs):
    L = ["model provenance -- forward log (S1)",
         "records  %d" % len(recs),
         "",
         "Self-report only. This module has no path that derives a model",
         "identifier from behaviour, output, timing or history; the",
         "function that would is infer_model(), which raises.",
         ""]
    if not recs:
        L += ["The log is empty. That is a state, not a default: no session",
              "has written a row yet."]
        return "\n".join(L)
    L.append(table(["date", "model as self-reported", "source", "reason",
                    "repo", "branch"],
                   [[r["date"], r["model_self_reported"], r["source"],
                     r.get("unknown_reason") or "-", r["repo"], r["branch"]]
                    for r in recs]))
    n_unknown = sum(1 for r in recs if r["source"] == UNKNOWN)
    L += ["", table(["state", "records"],
                    [["self-reported", len(recs) - n_unknown],
                     ["UNKNOWN", n_unknown]])]
    return "\n".join(L)


# ------------------------------------------------------------------ selftest

def _selftest():
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-58s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("provenance selftest")

    # ---- S1: self-report only, and the refusal is in code.
    r = open_line("2026-01-01", "R", "B", model="Some Model 9")
    ck("a stated model is recorded as self-reported",
       (r["model_self_reported"], r["source"]), ("Some Model 9", SELF_REPORTED))
    r = open_line("2026-01-01", "R", "B", reason="NO_BUILD_STRING")
    ck("no model gives UNKNOWN, not a blank",
       (r["model_self_reported"], r["unknown_reason"]),
       (UNKNOWN, "NO_BUILD_STRING"))
    r = open_line("2026-01-01", "R", "B", reason="WITHHELD")
    ck("withheld is a different state from unavailable",
       r["unknown_reason"], "WITHHELD")
    try:
        open_line("2026-01-01", "R", "B")
        bare = "accepted"
    except ValueError:
        bare = "refused"
    ck("a bare UNKNOWN with no reason is refused", bare, "refused")
    try:
        infer_model("anything")
        inf = "returned"
    except RefusedToInfer:
        inf = "raised"
    ck("there is no inference path and asking for one raises", inf, "raised")
    ck("an empty model string is not a self-report",
       open_line("2026-01-01", "R", "B", model="   ",
                 reason="NO_BUILD_STRING")["source"], UNKNOWN)

    # ---- S2: the three verdicts, each reachable.
    rows = [{"version": "A", "first_seen": "2026-01-10"},
            {"version": "B", "first_seen": "2026-02-10"}]
    ck("a date inside one span decodes SINGLE",
       (decode("2026-01-20", rows)["verdict"],
        decode("2026-01-20", rows)["candidates"]), (SINGLE, ["A"]))
    ck("a date on a boundary decodes AMBIGUOUS with both, no pick",
       (decode("2026-02-10", rows)["verdict"],
        decode("2026-02-10", rows)["candidates"]), (AMBIGUOUS, ["A", "B"]))
    ck("a date before the table is NOT_DECODABLE",
       decode("2025-06-01", rows)["verdict"], NOT_DECODABLE)
    ck("and NOT_DECODABLE emits no candidate rather than a guess",
       decode("2025-06-01", rows)["candidates"], [])
    ck("a single candidate is still a list",
       isinstance(decode("2026-01-20", rows)["candidates"], list), True)

    # S3: the derivation travels with every row, including the ones that
    # decode to nothing.
    ck("every verdict carries the assumption as its derivation",
       [decode(d, rows)["derivation"] == ASSUMPTION
        for d in ("2026-01-20", "2026-02-10", "2025-06-01")],
       [True, True, True])

    # The window is a choice and changing it changes the answer -- which
    # is why it is printed rather than buried.
    ck("widening the window moves a SINGLE to AMBIGUOUS",
       (decode("2026-02-08", rows, 1)["verdict"],
        decode("2026-02-08", rows, 3)["verdict"]), (SINGLE, AMBIGUOUS))

    # ---- date arithmetic, known answers.
    ck("day arithmetic: one day apart", _dnum("2026-02-10") - _dnum("2026-02-09"), 1)
    ck("day arithmetic: across a month", _dnum("2026-03-01") - _dnum("2026-02-28"), 1)
    ck("day arithmetic: 2026 is not a leap year",
       _dnum("2027-01-01") - _dnum("2026-01-01"), 365)

    # ---- trailer parsing.
    ck("a trailer states a model",
       parse_trailer("Claude Opus 5 <noreply@anthropic.com>"), "Claude Opus 5")
    ck("a parenthetical survives",
       parse_trailer("Claude Opus 4.7 (1M context) <x@y>"),
       "Claude Opus 4.7 (1M context)")
    ck("a human co-author is not a model", parse_trailer("A Person <a@b>"), None)
    ck("an empty trailer is None, not a string", parse_trailer(""), None)

    # ---- verify: both arms, on constructed commits with known answers.
    def C(sha, date, m, hh="12:00:00"):
        return (sha, date, "%s %s +0000" % (date, hh), m)

    cs = [C("a" * 40, "2026-01-20", "A"),      # single, matches
          C("b" * 40, "2026-01-20", "B"),      # single, differs
          C("c" * 40, "2026-02-10", "B"),      # ambiguous, contains
          C("d" * 40, "2025-06-01", "A"),      # not decodable
          C("e" * 40, "2026-01-20", None)]     # unstated
    v = verify(cs, rows)
    ck("verify separates its five outcomes",
       (v["agree"], v["disagree"], v["ambiguous_contains"], v["unstated"]),
       (1, 2, 1, 1))

    # ---- the resolution repair, pinned. Two commits on ONE day, in
    # order within it. A day-resolution ordering reports a counterexample
    # here and a timestamp ordering does not; this is the real 2026-08-11
    # switchover in miniature.
    import json as _json
    _tbl = {"table_kind": "t", "source": "t",
            "rows": [{"version": "Claude Opus 4.7 (1M context)",
                      "first_seen": "2026-01-10"},
                     {"version": "Claude Opus 5", "first_seen": "2026-02-10"}]}
    _p = os.path.join(HERE, "_selftest_table.json")
    open(_p, "w").write(_json.dumps(_tbl))
    try:
        global RELEASES
        _save, RELEASES = RELEASES, _p
        sameday = [C("f" * 40, "2026-02-10", "Claude Opus 4.7 (1M context)",
                     "17:20:27"),
                   C("g" * 40, "2026-02-10", "Claude Opus 5", "22:34:13")]
        ck("a same-day switchover in order is not a counterexample",
           assumption_check(sameday)["n_backwards"], 0)
        ck("and reversing the clock within the day is one",
           assumption_check(
               [C("g" * 40, "2026-02-10", "Claude Opus 5", "01:00:00"),
                C("f" * 40, "2026-02-10", "Claude Opus 4.7 (1M context)",
                  "23:00:00")])["n_backwards"], 1)
    finally:
        RELEASES = _save
        os.remove(_p)

    # ---- S4 screen, two arms plus a plant.
    meta = {"table_kind": "observed_bound", "source": "test"}
    emitted = (render_decode(cs, meta, rows, per_commit=True) + "\n" +
               render_sessions([open_line("2026-01-01", "R", "B",
                                          model="M")]))
    ck("the emitted report is clean under the declared exemption",
       screened(emitted)[0], True)
    ck("and only the declared vocabulary fires without the mask",
       exemption_is_only_delivered(emitted), True)
    ck("a planted grading word is caught through the exemption",
       screened(emitted + "\nthis commit is worse")[0], False)

    # ---- S4 structurally: the only git verb in this module is `log`.
    # Promised in the README; asserted here over this file's own source,
    # so a write verb added later turns it red rather than being caught
    # by a reader.
    # The pattern is composed from tokens so it does not match its own
    # source -- a literal here fires on the line that defines it, which
    # is UNI_010's self-reference caught in the check that would have
    # reported it. Same move as residual-direction naming.py.
    import re as _re
    src = open(os.path.abspath(__file__)).read()
    verbs = set()
    _pat = "[" + chr(34) + "git" + chr(34) + ",([^" + chr(93) + "]*)" + chr(93)
    for m in _re.finditer(_re.escape("[") + _pat[1:], src):
        for a in m.group(1).split(","):
            a = a.strip().strip('"').strip("'")
            if a and not a.startswith("-") and a not in ("repo",):
                verbs.add(a)
                break
    ck("the only git verb in this module is a read", sorted(verbs), ["log"])

    # ---- S1 log rendering distinguishes empty from populated.
    ck("an empty forward log says so rather than rendering blank",
       "The log is empty" in render_sessions([]), True)

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  provenance.py open  --repo R --branch B (--model M | --reason %s)
  provenance.py log
  provenance.py decode [REPO] [--per-commit] [--window N]
  provenance.py verify [REPO] [--window N]
  provenance.py --selftest""" % ("|".join(UNKNOWN_REASONS),)


def _flag(argv, name, default=None):
    if name in argv:
        i = argv.index(name)
        if i + 1 < len(argv):
            return argv[i + 1]
    return default


def main(argv):
    if not argv or "--selftest" in argv:
        return _selftest() if "--selftest" in argv else (print(USAGE) or 0)
    cmd = argv[0]
    if cmd == "open":
        repo = _flag(argv, "--repo")
        branch = _flag(argv, "--branch")
        if not repo or not branch:
            print(USAGE)
            return 2
        try:
            rec = open_line(_flag(argv, "--date", _today()), repo, branch,
                            model=_flag(argv, "--model"),
                            reason=_flag(argv, "--reason"))
        except ValueError as e:
            sys.stderr.write("refused: %s\n" % e)
            return 2
        append_session(rec)
        print(json.dumps(rec, sort_keys=True))
        return 0
    if cmd == "log":
        print(render_sessions(read_sessions()))
        return 0
    if cmd in ("decode", "verify"):
        repo = argv[1] if len(argv) > 1 and not argv[1].startswith("-") else "."
        window = int(_flag(argv, "--window", SWITCHOVER_DAYS))
        meta, rows = load_table()
        commits = git_log(repo)
        if not commits:
            sys.stderr.write("no commits read from %s\n" % repo)
            return 2
        if cmd == "decode":
            print(render_decode(commits, meta, rows, window,
                                "--per-commit" in argv))
        else:
            print(render_verify(commits, meta, rows, window))
        return 0
    print(USAGE)
    return 2


def _today():
    out = subprocess.check_output(["date", "+%Y-%m-%d"]).decode().strip()
    return out


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
