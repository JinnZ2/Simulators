# SPDX-License-Identifier: CC0-1.0
"""
STUDY-WATCH. Retrieval notification for entries that carry a WOULD MEASURE.

Runs on GitHub Actions, where the runner network reaches Crossref, OpenAlex
and arXiv -- the three the local egress gate refuses. That reach is the
reason the action exists; the schedule is incidental.

PATH NOTE. The work order writes `mundane/`. The folder it names is this
one, `notes/`, which is the mundanely-labelled folder created for it. Paths
below use `notes/`. If the literal name is wanted it is a `git mv`, and the
work order's other paths (`mundane/watch/YYYY-MM-DD.md`) map straight across.

HARD OUTPUT CONSTRAINT -- NOTIFICATION ONLY.
No count, no rate, no trend, no "N papers this month." A keyword query
selects its frame on searchability, so any number computed over its results
measures the query and not the field. `assert_no_metric()` enforces this on
every line this module authors and raises rather than writing the file.
Retrieved titles are exempt and marked, because a paper called "Trends in X"
is not this action emitting a trend.

TWO STAGES, and the split is the design.

  STAGE 1  RETRIEVE. Coarse, lexical, bias admitted. The query is built
           from the entry's own terms, logged verbatim per run, and nothing
           is filtered, scored or ranked here. NEVER EXECUTED from this
           machine -- the three sources are refused by the local egress
           gate, so `retrieve()` has been written and has never run. A first
           run on the runner is a first run of untested code and says so on
           stderr.

  STAGE 2  FILTER. Predicate structure, local, never folded into the query.
           Per candidate: front the main claim, drop the subject, read the
           residue. The reading is a JUDGEMENT and the action does not make
           it -- it proposes one, reports HOW the proposal was reached
           (`decided_by`, LEXICAL or PREDICATE, carried from T1), and leaves
           the residue in the run file for a human to read. The PR is the
           gate.

WHAT STAGE 2 CAN AND CANNOT DECIDE, established before the first run:

  CAN     assessability. A candidate whose main claim has no frontable verb
          or no extractable subject returns no reading and is recorded
          NOT_ASSESSABLE with the reason. That is stage 2's only mechanical
          reject.

  CANNOT  match against WOULD MEASURE. All eight `uninstrumented.ENTRIES`
          WOULD MEASURE strings return UNDECIDABLE under the same test,
          because a WOULD MEASURE is a DESIGN -- an instrument, an interval,
          a comparison -- and not a causal claim with a subject to read. The
          match target and the candidates are different grammatical kinds of
          thing. `matches_would_measure` is therefore emitted
          `UNADJUDICATED` for every candidate, with the entry's WOULD
          MEASURE quoted beside it so the reviewer can decide in the PR.
          Filling that column mechanically would be inventing a matcher the
          work order did not specify.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WATCH_DIR = os.path.join(HERE, "watch")

sys.path.insert(0, os.path.join(ROOT, "nonidentity-census"))
sys.path.insert(0, os.path.join(ROOT, "uninstrumented"))

import t1_predicate_unit as t1          # noqa: E402
import t1_verb_first as vf              # noqa: E402

ENTITY, PROCESS = "ENTITY", "PROCESS"
NOT_ASSESSABLE = "NOT_ASSESSABLE"
UNADJUDICATED = "UNADJUDICATED"
NOT_WATCHABLE = "NOT_WATCHABLE"

READING_FROM_LABEL = {t1.IDENTITY: ENTITY, t1.NONIDENTITY: PROCESS}

SOURCES = ("crossref", "openalex", "arxiv")


class MetricEmitted(Exception):
    """Raised when a line this module authors contains a count or a rate."""


# --------------------------------------------------------------------------
# The output constraint, enforced.
# --------------------------------------------------------------------------

_METRIC_PATTERNS = [
    (r"\b\d+\s+(papers?|candidates?|results?|hits?|matches|studies|works)\b",
     "a count of retrieved items"),
    (r"\b\d+(\.\d+)?\s*%", "a percentage"),
    (r"\b(rate|trend|trending|increase|decrease|rose|fell|growth|decline)\b",
     "a rate or trend word"),
    (r"\bper\s+(month|year|quarter|week|run)\b", "a per-interval figure"),
    (r"\b(more|fewer|less)\s+than\s+\d+", "a threshold comparison"),
    (r"\b(up|down)\s+\d+", "a change figure"),
]


def assert_no_metric(text, where="authored text"):
    """
    Refuses a count, rate or trend in text this module wrote. Raises rather
    than writing the file, because a README statement is a checklist and a
    guard is a property -- UNI_082.
    """
    hits = []
    for pat, why in _METRIC_PATTERNS:
        m = re.search(pat, text, re.I)
        if m:
            hits.append("%r (%s)" % (m.group(0), why))
    if hits:
        raise MetricEmitted(
            "%s emits %s. NOTIFICATION ONLY: a number computed over a "
            "keyword query's results measures the query." % (where,
                                                             "; ".join(hits)))
    return True


# --------------------------------------------------------------------------
# Entries and their WOULD MEASURE.
# --------------------------------------------------------------------------

def _would_measure_from_markdown(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    m = re.search(r"WOULD MEASURE[:\s]*(.+?)(?=\n\s*\n|\nCONFIDENCE|\Z)",
                  text, re.S | re.I)
    if not m:
        return None
    body = " ".join(m.group(1).split())
    return body or None


def load_entries():
    """
    Every entry that could be watched, with its WOULD MEASURE or None.
    None is NOT WATCHABLE. Nothing is invented for an entry that lacks one.
    """
    out = []
    import uninstrumented as U
    for i, e in enumerate(U.ENTRIES, 1):
        out.append({"entry_id": "ENTRIES[%d]" % i,
                    "path": "uninstrumented/uninstrumented.py",
                    "terms": e["quantity"],
                    "would_measure": e["would_measure"] or None})
    cases = os.path.join(ROOT, "uninstrumented", "cases")
    for name in sorted(os.listdir(cases)):
        if not name.endswith(".md"):
            continue
        p = os.path.join(cases, name)
        out.append({"entry_id": name[:-3],
                    "path": "uninstrumented/cases/" + name,
                    "terms": name[:-3],
                    "would_measure": _would_measure_from_markdown(p)})
    ops = os.path.join(HERE, "operators")
    if os.path.isdir(ops):
        for name in sorted(os.listdir(ops)):
            if not name.endswith(".md"):
                continue
            p = os.path.join(ops, name)
            out.append({"entry_id": "operators/" + name[:-3],
                        "path": "notes/operators/" + name,
                        "terms": name[:-3],
                        "would_measure": _would_measure_from_markdown(p)})
    return out


def split_watchable(entries):
    watchable = [e for e in entries if e["would_measure"]]
    unwatchable = [e for e in entries if not e["would_measure"]]
    return watchable, unwatchable


# --------------------------------------------------------------------------
# STAGE 1 -- retrieve. Coarse and lexical, and it says so.
# --------------------------------------------------------------------------

_STOP = {"the", "a", "an", "of", "in", "on", "for", "with", "and", "or",
         "to", "from", "as", "at", "by", "is", "are", "that", "which",
         "it", "its", "this", "each", "own", "not", "no", "any", "would",
         "measure", "per", "than", "into", "over", "under", "side", "sets"}


def build_query(entry, max_terms=6):
    """
    Built from the entry's own terms. Broad net, no scoring. This is the
    instrument and it is logged verbatim per run.
    """
    src = "%s %s" % (entry["terms"], entry["would_measure"] or "")
    toks = [t for t in re.findall(r"[a-zA-Z][a-zA-Z-]{2,}", src.lower())
            if t not in _STOP]
    seen, keep = set(), []
    for t in toks:
        if t not in seen:
            seen.add(t)
            keep.append(t)
        if len(keep) >= max_terms:
            break
    return " ".join(keep)


def retrieve(query, source, rows=20):
    """
    NEVER EXECUTED. Crossref, OpenAlex and arXiv are keyless and free and
    all three are refused by this machine's egress gate. Written for the
    runner; a first run there is a first run of untested code.
    """
    import urllib.parse
    import urllib.request
    sys.stderr.write(
        "NOTE: retrieve() has never been executed. It was written after the "
        "local egress gate refused all three sources. Treat a first run as "
        "untested code.\n")
    q = urllib.parse.quote(query)
    if source == "crossref":
        url = ("https://api.crossref.org/works?rows=%d&select=title,DOI,"
               "abstract&query=%s" % (rows, q))
    elif source == "openalex":
        url = ("https://api.openalex.org/works?per-page=%d"
               "&select=id,title,abstract_inverted_index&search=%s"
               % (rows, q))
    elif source == "arxiv":
        url = ("https://export.arxiv.org/api/query?search_query=all:%s"
               "&max_results=%d" % (q, rows))
    else:
        raise ValueError("unknown source %r" % source)
    req = urllib.request.Request(url, headers={"User-Agent":
                                               "JinnZ2-Simulators/study-watch"})
    with urllib.request.urlopen(req, timeout=45) as fh:
        return fh.read().decode("utf-8", "replace")


# --------------------------------------------------------------------------
# STAGE 2 -- filter on predicate structure. Local. Never inside the query.
# --------------------------------------------------------------------------

def stage2(claim, entry=None):
    """
    Fronts the main claim, drops the subject, reads what is left. Returns a
    PROPOSED reading plus how the proposal was reached. The bearer
    judgement itself is left to the reviewer; `residue` is what they read.
    """
    f = vf.front(claim)
    c = t1.classify(claim)
    out = {"claim": claim, "residue": f["residue"], "head": c["head"],
           "reading": NOT_ASSESSABLE, "decided_by": None,
           "matches_would_measure": UNADJUDICATED, "why": ""}
    if not f["fronted"]:
        out["why"] = f["why"]
        return out
    if c["label"] == t1.UNDECIDABLE:
        out["why"] = "no reading proposable: " + c["why"]
        return out
    out["reading"] = READING_FROM_LABEL[c["label"]]
    out["decided_by"] = ("LEXICAL" if c["decided_by"] == t1.BY_TABLE
                         else "PREDICATE")
    out["why"] = c["why"]
    return out


def assessable(row):
    return row["reading"] in (ENTITY, PROCESS)


# --------------------------------------------------------------------------
# NULL TEST -- before the first real run.
# --------------------------------------------------------------------------

# Arms matched on head noun. Each noun appears in both arms, so `decided_by`
# cannot track which arm a candidate is in -- the T6 lesson.
NULL_PAIRS = [
    ("population",
     "We show that populations declined across all sampled sites.",
     "Populations."),
    ("allocation",
     "Allocation proceeds without any central coordinator.",
     "On allocation."),
    ("market",
     "The market allocates scarce goods without a designer.",
     "Regarding the market."),
]

# Second arm-pair, on the READING rather than on assessability. Constructible
# only where T1 decides by predicate -- see null_test().
READING_PAIRS = [
    ("market",
     "The labour market tightened over the following two quarters.",
     "The market allocates scarce goods without a designer."),
]


def null_test(verbose=True):
    """
    Two constructions, and only one of them is buildable for every head noun.
    Raises nothing; returns a dict and prints the STOP condition if it fires.
    """
    surv, fail = [], []
    for noun, yes, no in NULL_PAIRS:
        surv.append((noun, stage2(yes)))
        fail.append((noun, stage2(no)))
    ok_arms = all(assessable(r) for _, r in surv) and \
        not any(assessable(r) for _, r in fail)
    nouns_a = sorted(n for n, _ in surv)
    nouns_b = sorted(n for n, _ in fail)
    matched = nouns_a == nouns_b
    dby_a = sorted(r["decided_by"] for _, r in surv)
    dby_b = sorted(str(r["decided_by"]) for _, r in fail)

    reading_rows = []
    for noun, a, b in READING_PAIRS:
        reading_rows.append((noun, stage2(a), stage2(b)))
    reading_separates = all(x["reading"] != y["reading"]
                            for _, x, y in reading_rows)

    # The nouns for which a reading-matched pair is NOT constructible.
    blocked = []
    for noun, _, _ in NULL_PAIRS:
        r = stage2("The %s declined." % noun)
        if r["decided_by"] == "LEXICAL":
            blocked.append(noun)

    if verbose:
        print("NULL TEST -- before the first real run\n")
        print("ARMS: assessable vs not, matched on head noun")
        for (noun, a), (_, b) in zip(surv, fail):
            print("  %-11s survives=%-15s does-not=%-15s"
                  % (noun, a["reading"], b["reading"]))
        print("  arms matched on head noun : %s" % matched)
        print("  decided_by in surviving arm: %s" % dby_a)
        print("  decided_by in other arm    : %s (no reading proposed)"
              % dby_b)
        print("  arms separate on assessability: %s" % ok_arms)
        print()
        print("ARMS: ENTITY vs PROCESS, matched on head noun")
        for noun, a, b in reading_rows:
            print("  %-11s %-8s vs %-8s  decided_by %s / %s"
                  % (noun, a["reading"], b["reading"], a["decided_by"],
                     b["decided_by"]))
        print("  arms separate on reading: %s" % reading_separates)
        print()
        print("  NOT CONSTRUCTIBLE on the reading arm for: %s"
              % (", ".join(blocked) or "none"))
        print("  Where T1 decides by word list, the head noun FIXES the")
        print("  reading, so holding the noun constant across arms holds")
        print("  the reading constant too and the arms collapse. The")
        print("  reading-matched pair is buildable only on the claim-level")
        print("  nouns, which is T1-1 showing up in the null test's own")
        print("  construction requirement.")
        if not (ok_arms and matched):
            print()
            print("STOP: arms could not be built or could not be matched.")
    return {"assessability_arms_ok": ok_arms and matched,
            "reading_arms_ok": reading_separates,
            "blocked_nouns": blocked}


# --------------------------------------------------------------------------
# Run file.
# --------------------------------------------------------------------------

HEADER = ("| entry_id | query_string | candidate | source | "
          "matches_would_measure | decided_by | notes |")
RULE = "|---|---|---|---|---|---|---|"


def render_run(rows, unwatchable, nil_results, stamp):
    """
    Rows are retrieved data and are exempt from the metric guard; every
    other line is authored here and is checked.
    """
    authored = []
    authored.append("# study-watch %s" % stamp)
    authored.append("")
    # Worded around the guard's own vocabulary on purpose. The first
    # draft of this line said "No count, rate or trend is emitted" and
    # assert_no_metric refused it on the word `rate` -- the guard cannot
    # tell a rate from the word for one, so the file declaring the
    # constraint cannot state it in the constraint's own terms. Recorded in
    # FINDINGS_STUDY_WATCH.md; the guard is left strict, because
    # over-refusing an authored line is the cheap direction.
    authored.append("Notification only. This file reports what a query "
                    "returned and nothing computed over what it returned. "
                    "See `README.md` in this directory for why that is a "
                    "constraint and not a style choice.")
    authored.append("")
    authored.append("`matches_would_measure` is `UNADJUDICATED` for every "
                    "candidate by design. The entry's WOULD MEASURE is a "
                    "design and a candidate is a claim, so no mechanical "
                    "test here compares them. A reviewer decides, in the "
                    "pull request.")
    authored.append("")
    assert_no_metric("\n".join(authored), "run-file preamble")

    body = list(authored)
    body.append(HEADER)
    body.append(RULE)
    for r in rows:
        body.append("| %s | `%s` | %s | %s | %s | %s | %s |" % (
            r["entry_id"], r["query_string"],
            r["candidate"].replace("|", "\\|"), r["source"],
            r["matches_would_measure"], r["decided_by"] or "--",
            r["notes"].replace("|", "\\|")))
    if not rows:
        body.append("| -- | -- | -- | -- | -- | -- | no rows this run |")

    # EXEMPTION BOUNDARY, fixed by the guard refusing a legitimate query.
    # A NIL RESULT line carries the query string, which is built from the
    # ENTRY's own terms -- one of them contains the word `rate` -- and a
    # table row carries a retrieved title. Both are DATA. Everything this
    # module composes is checked. The split is by line, not by section.
    tail_prose = ["", "## NIL RESULT", "",
                  "A query that came back with nothing. Recorded, not "
                  "omitted.", "",
                  "## NOT WATCHABLE", "",
                  "Entries with no WOULD MEASURE. Skipped. None was "
                  "invented."]
    assert_no_metric("\n".join(tail_prose), "run-file tail prose")

    tail = tail_prose[:5]
    for n in nil_results:
        tail.append("- `%s` :: `%s` :: %s" % (n["entry_id"], n["query"],
                                              n["source"]))
    if not nil_results:
        tail.append("- none recorded this run")
    tail.extend(tail_prose[5:])
    tail.append("")
    for e in unwatchable:
        tail.append("- `%s` -- `%s`" % (e["entry_id"], e["path"]))
    if not unwatchable:
        tail.append("- none")
    return "\n".join(body + tail) + "\n"


def write_run(rows, unwatchable, nil_results, stamp=None, out_dir=None):
    stamp = stamp or datetime.date.today().isoformat()
    out_dir = out_dir or WATCH_DIR
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    text = render_run(rows, unwatchable, nil_results, stamp)
    path = os.path.join(out_dir, "%s.md" % stamp)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def selftest():
    fails = []
    try:
        assert_no_metric("we found 12 papers this month")
        fails.append("the metric guard must refuse a count")
    except MetricEmitted:
        pass
    try:
        assert_no_metric("publication rate rose")
        fails.append("the metric guard must refuse a trend word")
    except MetricEmitted:
        pass
    try:
        assert_no_metric("a candidate was retrieved and is listed below")
    except MetricEmitted as ex:
        fails.append("the metric guard refuses ordinary notification: %s"
                     % ex)
    entries = load_entries()
    watchable, unwatchable = split_watchable(entries)
    if not watchable:
        fails.append("no watchable entries found")
    if not unwatchable:
        fails.append("no NOT WATCHABLE entries found; the skip path would "
                     "be unexercised")
    ids = [e["entry_id"] for e in unwatchable]
    if "024refusalfalsepositiverate" not in ids:
        fails.append("case 024 carries no WOULD MEASURE and must be listed "
                     "NOT WATCHABLE; got %r" % ids)
    if "operators/D2" not in ids:
        fails.append("operators/D2 carries no WOULD MEASURE and must be "
                     "listed NOT WATCHABLE")
    import uninstrumented as U
    undec = [e for e in U.ENTRIES
             if t1.classify(e["would_measure"])["label"] == t1.UNDECIDABLE]
    if len(undec) != len(U.ENTRIES):
        fails.append("the docstring says every ENTRIES WOULD MEASURE reads "
                     "UNDECIDABLE; that is no longer true and the claim "
                     "about what stage 2 cannot decide must be restated")
    r = stage2("We show that populations declined across all sampled sites.")
    if r["reading"] != ENTITY:
        fails.append("stage2 lost the worked ENTITY case: %r" % r["reading"])
    if r["matches_would_measure"] != UNADJUDICATED:
        fails.append("matches_would_measure must be UNADJUDICATED")
    r2 = stage2("Populations.")
    if assessable(r2):
        fails.append("a claim with no frontable verb must not be assessable")
    nt = null_test(verbose=False)
    if not nt["assessability_arms_ok"]:
        fails.append("null test: assessability arms did not build or match")
    if not nt["reading_arms_ok"]:
        fails.append("null test: reading arms did not separate")
    if not nt["blocked_nouns"]:
        fails.append("no noun blocked on the reading arm; the finding about "
                     "word-list-decided nouns would be unearned")
    try:
        assert_no_metric("no count, rate or trend is emitted here")
        fails.append("the guard must refuse its own constraint sentence; "
                     "the use/mention limit is recorded and is not fixed")
    except MetricEmitted:
        pass
    txt = render_run([], unwatchable, [], "0000-00-00")
    if "NOT WATCHABLE" not in txt or "NIL RESULT" not in txt:
        fails.append("run file missing a required section")
    if re.search(r"\bauto[- ]?merge\b", txt, re.I):
        fails.append("run file mentions auto-merge")
    print("SELFTEST %s (%d checks failed)"
          % ("FAIL" if fails else "PASS", len(fails)))
    for f in fails:
        print("  " + f)
    return 1 if fails else 0


def cmd_entries():
    entries = load_entries()
    watchable, unwatchable = split_watchable(entries)
    print("WATCHABLE -- entry, then the query stage 1 would send\n")
    for e in watchable:
        print("  %-34s %s" % (e["entry_id"], build_query(e)))
    print()
    print("NOT WATCHABLE -- no WOULD MEASURE, skipped, none invented\n")
    for e in unwatchable:
        print("  %-34s %s" % (e["entry_id"], e["path"]))
    return 0


def cmd_run(argv):
    """The real run. Stage 1 has never executed from this machine."""
    entries = load_entries()
    watchable, unwatchable = split_watchable(entries)
    rows, nil = [], []
    live = "--live" in argv
    for e in watchable:
        q = build_query(e)
        for source in SOURCES:
            if not live:
                nil.append({"entry_id": e["entry_id"], "query": q,
                            "source": source + " (not queried: stage 1 not "
                            "run)"})
                continue
            try:
                raw = retrieve(q, source)
            except Exception as ex:                    # noqa: BLE001
                nil.append({"entry_id": e["entry_id"], "query": q,
                            "source": "%s (error: %s)" % (source,
                                                          type(ex).__name__)})
                continue
            titles = re.findall(r'"title"\s*:\s*\[?\s*"([^"]{10,300})"', raw)
            titles += re.findall(r"<title>([^<]{10,300})</title>", raw)
            if not titles:
                nil.append({"entry_id": e["entry_id"], "query": q,
                            "source": source})
                continue
            for t_ in titles:
                s2 = stage2(t_)
                rows.append({"entry_id": e["entry_id"], "query_string": q,
                             "candidate": t_, "source": source,
                             "matches_would_measure":
                                 s2["matches_would_measure"],
                             "decided_by": s2["decided_by"],
                             "notes": "residue: %s" % (s2["residue"] or
                                                       s2["why"])})
    out_dir = (os.path.join(HERE, "samples") if "--dry" in argv
               else WATCH_DIR)
    stamp = "dry-run" if "--dry" in argv else None
    path = write_run(rows, unwatchable, nil, stamp=stamp, out_dir=out_dir)
    print(path)
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--null" in argv:
        null_test()
        return 0
    if "--entries" in argv:
        return cmd_entries()
    if "--run" in argv:
        return cmd_run(argv)
    print(__doc__.strip())
    print("\nusage: study_watch.py [--selftest | --null | --entries | "
          "--run [--live]]")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
