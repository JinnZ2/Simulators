#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
check_citations.py -- the checker for
tools/external_report_audit_okcomputer.md.

Takes a ledger of cited IDs/URLs with the value each report claims for
them, and writes the four-state table:

    VERIFIED     the source was seen and says what the report says
    CORRECTED    the source was seen and says something else; the row
                 carries the correct value
    NOT FOUND    the source is not at that ID: the ID resolves to another
                 work, or two or more searches on a searchable identifier
                 returned nothing while the channel answered
    UNREACHABLE  could not check: host refused, identifier not indexed,
                 or the source was seen but the claimed value was not

The state is DERIVED from four recorded observations (reached, queries,
exists, says). It is never typed by hand. UNREACHABLE and NOT FOUND are
kept apart: absence on fewer than two searches is not a check, and a
source that exists but whose figure was not seen is not missing.

Rows are never dropped. A row the rules cannot classify is refused and
named; it does not disappear from the count.

The checker also recomputes the audit's internal arithmetic and its
Part C rerank. The rerank imports the WO-3 scorer
(tools/experiment_fruitfulness_triage.py), applies the component changes
declared in the audit, and adds the sixth-site variants. A component may
move only on an anchor that passed Part A.

Usage
    python3 tools/check_citations.py                  check the audit
    python3 tools/check_citations.py --ledger FILE    four-state table for
                                                      any ledger file
    python3 tools/check_citations.py --render         print the generated
                                                      blocks
    python3 tools/check_citations.py --reports DIR    also check report
                                                      hashes, the URL
                                                      inventory and the
                                                      quote budget
    python3 tools/check_citations.py --selftest

Ledger line:  id | rep | sec | cite | claim | reached | queries | exists |
              says | found | depth

Exit: 0 every check that ran passed; 1 a check failed; 3 could not run
(EXIT_CONTRACT.md). A check that could not run prints NOT_RUN and is
counted apart; it is never a pass. Stdlib only; parses under Python 3.9;
no network.
"""

import hashlib
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
AUDIT = os.path.join(HERE, "external_report_audit_okcomputer.md")
SCORER = os.path.join(HERE, "experiment_fruitfulness_triage.py")

VERIFIED = "VERIFIED"
CORRECTED = "CORRECTED"
NOT_FOUND = "NOT_FOUND"
UNREACHABLE = "UNREACHABLE"
STATES = (VERIFIED, CORRECTED, NOT_FOUND, UNREACHABLE)

REACHED = ("Y", "N", "?")
EXISTS = ("Y", "N", "OTHER", "?")
SAYS = ("MATCH", "DIFFERS", "UNSEEN")
DEPTHS = ("primary", "secondary", "search-index", "none")
REPORTS = ("P", "C")
NOT_FOUND_QUERIES = 2

TOP_NOTE = ("this is an audit of outside work, kept with its mismatches on "
            "purpose. It does not endorse the reports or the glyph roles "
            "they propose")
CREDIT = ("OKComputer", "2026-10-14")
QUOTE_BUDGET = 40          # longest verbatim run from a report, in words
TERM_CERTIF = 41           # B.1: "certif" in the companion
TERM_READOUT = 0           # B.1: "readout" in either report
NGRAM = 8


class LedgerError(Exception):
    pass


# ---------------------------------------------------------------- blocks

def read_doc(path=AUDIT):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def fenced(doc, name):
    """Content of the one block opened by three backticks and `name`."""
    lines = doc.split("\n")
    opens = [i for i, ln in enumerate(lines) if ln.rstrip() == "```" + name]
    if len(opens) != 1:
        raise LedgerError("block %r: %d opening fences, want 1"
                          % (name, len(opens)))
    body = []
    for ln in lines[opens[0] + 1:]:
        if ln.rstrip() == "```":
            return "".join(x + "\n" for x in body)
        body.append(ln)
    raise LedgerError("block %r is not closed" % name)


def _live(text):
    for n, ln in enumerate(text.splitlines(), 1):
        if ln.strip() and not ln.lstrip().startswith("#"):
            yield n, ln


# ---------------------------------------------------------------- ledger

FIELDS = ("id", "rep", "sec", "cite", "claim", "reached", "queries",
          "exists", "says", "found", "depth")


def parse_ledger(text):
    """Every live line becomes a row or a refusal. Returns (rows, refused);
    refused is a list of (line number, id or None, reason)."""
    rows, refused, seen = [], [], set()
    for n, ln in _live(text):
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) != len(FIELDS):
            refused.append((n, None, "%d fields, want %d"
                            % (len(parts), len(FIELDS))))
            continue
        row = dict(zip(FIELDS, parts))
        why = row_problem(row)
        if row["id"] in seen:
            why = why or "id %s repeated" % row["id"]
        seen.add(row["id"])
        if why:
            refused.append((n, row["id"], why))
            continue
        row["queries"] = int(row["queries"])
        rows.append(row)
    return rows, refused


def row_problem(row):
    """None when the row's observations are consistent, else the reason."""
    if not re.match(r"^A\d{2,3}$", row["id"]):
        return "id %r is not A<nn>" % row["id"]
    reps = [r for r in row["rep"].split(",") if r]
    if not reps or any(r not in REPORTS for r in reps):
        return "rep %r, want P, C or P,C" % row["rep"]
    if row["reached"] not in REACHED:
        return "reached %r not in %s" % (row["reached"], "/".join(REACHED))
    if not re.match(r"^\d+$", row["queries"]):
        return "queries %r is not a count" % row["queries"]
    if row["exists"] not in EXISTS:
        return "exists %r not in %s" % (row["exists"], "/".join(EXISTS))
    if row["says"] not in SAYS:
        return "says %r not in %s" % (row["says"], "/".join(SAYS))
    if row["depth"] not in DEPTHS:
        return "depth %r not in %s" % (row["depth"], "/".join(DEPTHS))
    if not row["cite"] or not row["claim"]:
        return "cite and claim are required"
    if row["says"] in ("MATCH", "DIFFERS") and \
            (row["reached"] != "Y" or row["exists"] != "Y"):
        return ("says %s on a source not reached or not shown to exist: a "
                "reading nobody saw" % row["says"])
    if row["says"] == "DIFFERS" and not row["found"]:
        return "DIFFERS with no found value: a correction must give it"
    if row["exists"] == "N" and row["says"] != "UNSEEN":
        return "exists N but says %s" % row["says"]
    if row["exists"] == "N" and row["reached"] != "Y":
        return ("exists N on a channel that did not answer: that is '?', "
                "not absence")
    return None


def citation_state(reached, queries, exists, says):
    """The four-state rule. Derived, never declared."""
    if exists == "OTHER":
        return NOT_FOUND
    if exists == "N":
        return NOT_FOUND if queries >= NOT_FOUND_QUERIES else UNREACHABLE
    if reached != "Y" or exists != "Y":
        return UNREACHABLE
    if says == "MATCH":
        return VERIFIED
    if says == "DIFFERS":
        return CORRECTED
    return UNREACHABLE


def state_of(row):
    return citation_state(row["reached"], row["queries"], row["exists"],
                          row["says"])


def render_table(rows):
    out = ["# id   state        depth         rep  cite"]
    for r in rows:
        out.append("%-5s  %-11s  %-12s  %-3s  %s"
                   % (r["id"], state_of(r), r["depth"], r["rep"],
                      r["cite"][:44]))
    return out


def counts(rows):
    tab = {s: {"all": 0, "P": 0, "C": 0} for s in STATES}
    for r in rows:
        s = state_of(r)
        tab[s]["all"] += 1
        for rep in r["rep"].split(","):
            tab[s][rep] += 1
    return tab


def render_counts(rows):
    tab = counts(rows)
    out = ["# state        all    P    C   (a row citing both reports "
           "counts once in all)"]
    for s in STATES:
        out.append("%-12s  %4d %4d %4d" % (s, tab[s]["all"], tab[s]["P"],
                                           tab[s]["C"]))
    out.append("%-12s  %4d %4d %4d"
               % ("total", sum(tab[s]["all"] for s in STATES),
                  sum(tab[s]["P"] for s in STATES),
                  sum(tab[s]["C"] for s in STATES)))
    depth = {}
    for r in rows:
        depth[r["depth"]] = depth.get(r["depth"], 0) + 1
    out.append("depth: " + "  ".join("%s %d" % (d, depth[d])
                                     for d in DEPTHS if d in depth))
    return out


# ---------------------------------------------------------------- arithmetic

K_B = 1.380649e-23          # J/K, exact (SI 2019)
E_CHARGE = 1.602176634e-19  # C, exact (SI 2019)


def _agree(stated, computed, halfwidth):
    return "AGREES" if abs(stated - computed) <= halfwidth + 1e-12 \
        else "DIFFERS"


FIG4_TAU = (1, 2, 3, 5, 8, 13, 21, 34, 40)
# Marker heights read off fig4_landauer.png by eye, in kT. A declared
# reading of an image, not a measurement; tolerance 0.1 kT.
FIG4_READ = (8.85, 4.75, 3.4, 2.3, 1.7, 1.3, 1.1, 0.95, 0.9)


def arith_rows():
    """(name, stated, computed, verdict, note). Every stated value is the
    report's own; every computed value is recomputed here."""
    rows = []
    kt = K_B * 300.0
    ln2 = math.log(2.0)
    ev = kt * ln2 / E_CHARGE
    rows.append(("kT ln 2 at 300 K, eV", "0.018", "%.5f" % ev,
                 _agree(0.018, ev, 0.0005), "parent 2.6, 6"))
    rows.append(("kT ln 2 at 300 K, J", "3e-21", "%.3e" % (kt * ln2),
                 _agree(3e-21, kt * ln2, 0.5e-21), "parent 6"))
    frac = 32.8e6 / 176e9 * 100.0
    rows.append(("32.8M of 176B, %", "0.019", "%.5f" % frac,
                 _agree(0.019, frac, 0.0005), "parent table row 1, 4.1"))
    rows.append(("coverage left when 0.019% is missed, %", "99.98",
                 "%.3f" % (100.0 - 0.019),
                 _agree(99.98, 100.0 - 0.019, 0.005), "companion 4.4"))
    rel = (4.062 - 3.889) / 4.062 * 100.0
    rows.append(("DRMoET excess loss 4.062 -> 3.889, %", "4.3",
                 "%.2f" % rel, _agree(4.3, rel, 0.05),
                 "companion 3.2; source values from A33"))
    fold = 34.9 / 1.2
    rows.append(("retention 1.2% -> 34.9%, fold", "28", "%.2f" % fold,
                 _agree(28.0, fold, 0.5),
                 "the source states 28-fold; 28 needs naive retention "
                 "%.3f-%.3f%%, so 1.2 is rounded"
                 % (34.9 / 28.5, 34.9 / 27.5)))
    for tau, read in zip(FIG4_TAU, FIG4_READ):
        val = ln2 + 8.15 / tau
        rows.append(("fig4 marker at tau=%d, kT" % tau, "%.2f" % read,
                     "%.3f" % val, _agree(read, val, 0.1),
                     "ln 2 + 8.15/tau; read off the image"))
    return rows


def render_arith():
    out = ["# check                                    stated     "
           "computed   verdict"]
    for name, st, comp, ver, _ in arith_rows():
        out.append("%-40s %-10s %-10s %s" % (name, st, comp, ver))
    return out


# ---------------------------------------------------------------- frontier

def majority_fail(p, r):
    """P(a majority of r independent copies flipped), r odd."""
    need = r // 2 + 1
    return sum(math.comb(r, j) * p ** j * (1 - p) ** (r - j)
               for j in range(need, r + 1))


def bits_frontier(reps=(1, 3, 5, 7), p=0.01, facts=100, capacity=1000):
    """The S6b toy, all axes in bits. Per redundancy r:
         survive   probability a fact survives one round, majority vote
         erased    syndrome bits reset per correction round, facts*(r-1)
         free      capacity left for new facts, capacity - facts*r
    Returns (points, dominated) where dominated counts points that
    another point beats on all three axes."""
    pts = []
    for r in reps:
        pts.append({"r": r, "survive": 1.0 - majority_fail(p, r),
                    "erased": facts * (r - 1),
                    "free": capacity - facts * r})
    return pts, dominated_count(pts)


def dominated_count(pts):
    n = 0
    for a in pts:
        for b in pts:
            if b is a:
                continue
            ge = (b["survive"] >= a["survive"] and b["erased"] <= a["erased"]
                  and b["free"] >= a["free"])
            gt = (b["survive"] > a["survive"] or b["erased"] < a["erased"]
                  or b["free"] > a["free"])
            if ge and gt:
                n += 1
                break
    return n


# ---------------------------------------------------------------- Part C

def load_scorer(path=SCORER):
    import importlib.util
    spec = importlib.util.spec_from_file_location("_eft_for_audit", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DELTA_RE = re.compile(r"^(S[1-5][a-z])\s+([dukxr])\s+([0-2])\s*->\s*([0-2])"
                      r"\s+anchors\s+([A0-9,]+)\s*(corrected-sense)?\s*\|"
                      r"\s*(\S.*)$")


def parse_deltas(text):
    out = []
    for n, ln in _live(text):
        m = DELTA_RE.match(ln.strip())
        if not m:
            raise LedgerError("partc-deltas line %d unreadable: %r"
                              % (n, ln))
        out.append({"id": m.group(1), "comp": m.group(2),
                    "frm": int(m.group(3)), "to": int(m.group(4)),
                    "anchors": [a for a in m.group(5).split(",") if a],
                    "corrected_sense": bool(m.group(6)),
                    "reason": m.group(7)})
    return out


def parse_variants(text, sc):
    """S6 rows in the triage-table format, site S6."""
    rows = []
    for n, ln in _live(text):
        parts = ln.split(None, 11)
        if len(parts) != 12 or parts[1] != "S6" or \
                not re.match(r"^S6[a-z]$", parts[0]):
            raise LedgerError("partc-variants line %d unreadable" % n)
        comp = {}
        for name, raw in zip(sc.COMPONENTS, parts[2:7]):
            if raw not in ("0", "1", "2"):
                raise LedgerError("partc-variants line %d: %s=%r"
                                  % (n, name, raw))
            comp[name] = int(raw)
        need = {}
        for name, raw in zip(sc.RESOURCES, parts[7:11]):
            if raw not in sc.LEVELS:
                raise LedgerError("partc-variants line %d: %s=%r"
                                  % (n, name, raw))
            need[name] = raw
        rows.append({"id": parts[0], "site": "S6", "comp": comp,
                     "need": need, "design": parts[11].strip()})
    return rows


def anchor_problems(deltas, ledger_rows):
    """A delta may move a component only on anchors that passed Part A:
    VERIFIED, or CORRECTED with the delta declared corrected-sense."""
    by_id = {r["id"]: r for r in ledger_rows}
    probs = []
    for d in deltas:
        for a in d["anchors"]:
            if a not in by_id:
                probs.append("%s.%s cites %s, not in the ledger"
                             % (d["id"], d["comp"], a))
                continue
            s = state_of(by_id[a])
            if s == VERIFIED:
                continue
            if s == CORRECTED and d["corrected_sense"]:
                continue
            probs.append("%s.%s cites %s, which is %s"
                         % (d["id"], d["comp"], a, s))
    return probs


def apply_deltas(base, deltas):
    rows = [dict(r, comp=dict(r["comp"])) for r in base]
    by_id = {r["id"]: r for r in rows}
    for d in deltas:
        if d["id"] not in by_id:
            raise LedgerError("delta names %s, not in the triage table"
                              % d["id"])
        cur = by_id[d["id"]]["comp"][d["comp"]]
        if cur != d["frm"]:
            raise LedgerError("delta %s.%s says from %d, table has %d"
                              % (d["id"], d["comp"], d["frm"], cur))
        by_id[d["id"]]["comp"][d["comp"]] = d["to"]
    return rows


def _fmt(v):
    return v if isinstance(v, str) else "%.3f" % v


def rerank(doc, ledger_rows, sc=None):
    sc = sc or load_scorer()
    base = sc.parse_table(sc.fenced(sc.read_doc(), "triage-table"))
    deltas = parse_deltas(fenced(doc, "partc-deltas"))
    variants = parse_variants(fenced(doc, "partc-variants"), sc)
    after = apply_deltas(base, deltas) + variants
    readings = []
    for prof in ("phone", "lab"):
        have = sc.PROFILES[prof]
        for q in sc.QUESTIONS:
            readings.append((prof, q, sc.sweep(base, have, q)[1],
                             sc.sweep(after, have, q)[1]))
    moved = []
    for d in deltas:
        b = next(r for r in base if r["id"] == d["id"])
        a = next(r for r in after if r["id"] == d["id"])
        for q in sc.QUESTIONS:
            moved.append((d["id"], q, sc.variant_ratio(b, q),
                          sc.variant_ratio(a, q)))
    var = []
    for v in variants:
        short = sc.shortfall(v, sc.PROFILES["phone"])
        var.append((v["id"], sc.variant_ratio(v, "LOOP"),
                    sc.variant_ratio(v, "REV"), short))
    best = {}
    for q in sc.QUESTIONS:
        best[q] = sc.best_by_site(after, sc.PROFILES["phone"], q)
    g_sites = sorted(set(r["site"] for r in after
                         if r["design"].startswith("(g)")))
    return {"readings": readings, "moved": moved, "variants": var,
            "best": best, "deltas": deltas, "g_sites": g_sites,
            "problems": anchor_problems(deltas, ledger_rows)}


def render_rerank(rr):
    out = ["# profile  question  before                    after"]
    for prof, q, b, a in rr["readings"]:
        out.append("%-8s  %-8s  %-24s  %s" % (prof, q, b, a))
    out.append("# components moved (default setting, ratio before -> after)")
    for vid, q, b, a in rr["moved"]:
        out.append("%-4s %-4s %s -> %s" % (vid, q, _fmt(b), _fmt(a)))
    out.append("# sixth-site variants (default setting)")
    for vid, lo, rev, short in rr["variants"]:
        out.append("%-4s LOOP %s  REV %s  phone %s"
                   % (vid, _fmt(lo), _fmt(rev),
                      "BLOCKED(%s)" % ",".join(short) if short
                      else "feasible"))
    out.append("# best per site after, phone, default setting")
    for q in ("LOOP", "REV"):
        cells = ["%s %s %s" % (s, _fmt(v), vid)
                 for s, (v, vid) in sorted(rr["best"][q].items())]
        out.append("%-4s %s" % (q, " | ".join(cells)))
    pts, dom = bits_frontier()
    out.append("# S6b bits-only frontier: r, P(fact lost per round), "
               "bits erased per round, free bits; dominated %d of %d"
               % (dom, len(pts)))
    for p in pts:
        out.append("r=%d  %.3e  %d  %d" % (p["r"], 1.0 - p["survive"],
                                           p["erased"], p["free"]))
    return out


# ---------------------------------------------------------------- reports

URL_RE = re.compile(r"https?://[^)\s]+")


def report_urls(text):
    return sorted(set(URL_RE.findall(text)))


def parse_inventory(text):
    out = {}
    for n, ln in _live(text):
        if "|" not in ln:
            raise LedgerError("url-inventory line %d has no '|'" % n)
        url, ids = [p.strip() for p in ln.split("|", 1)]
        if url in out:
            raise LedgerError("url-inventory repeats %s" % url)
        out[url] = [i for i in re.split(r"[,\s]+", ids) if re.match(
            r"^A\d{2,3}$", i)]
    return out


def parse_hashes(text):
    out = {}
    for n, ln in _live(text):
        parts = ln.split()
        if len(parts) != 3 or parts[0] not in REPORTS:
            raise LedgerError("report-hashes line %d unreadable" % n)
        out[parts[0]] = (parts[1], parts[2])
    return out


def _words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def longest_verbatim(doc_text, source_text, n=NGRAM):
    """Longest run of consecutive words in doc_text that appears verbatim
    in source_text, in words; 0 when no n-gram is shared."""
    src = _words(source_text)
    grams = set(tuple(src[i:i + n]) for i in range(len(src) - n + 1))
    doc = _words(doc_text)
    best, run = 0, 0
    for i in range(len(doc) - n + 1):
        if tuple(doc[i:i + n]) in grams:
            run += 1
            best = max(best, run + n - 1)
        else:
            run = 0
    return best


def parse_groups(text):
    out = []
    for n, ln in _live(text):
        if "|" not in ln:
            raise LedgerError("unreachable-groups line %d has no '|'" % n)
        cause, ids = [p.strip() for p in ln.split("|", 1)]
        out.append((cause, ids.split()))
    return out


# Each pattern is a count the audit states in prose; each group names the
# computed quantity it must equal. A pattern that matches nothing fails:
# a stated count that moved out of reach of its check is not checked.
PROSE = (
    (r"ledger, (\d+) rows", ("total",)),
    (r"The (\d+) UNREACHABLE rows", (UNREACHABLE,)),
    (r"(\d+) of (\d+) rows unreachable and (\d+) corrected",
     (UNREACHABLE, "total", CORRECTED)),
    (r"The other (\d+) links", ("context",)),
    (r"(\d+) rows at search-index depth, (\d+) secondary",
     ("search-index", "secondary")),
    (r"Full-text reads for the (\d+) UNREACHABLE rows", (UNREACHABLE,)),
)


def prose_problems(doc, rows, context):
    flat = re.sub(r"\s+", " ", doc)
    tab = counts(rows)
    val = {s: tab[s]["all"] for s in STATES}
    val["total"] = len(rows)
    val["context"] = context
    for d in DEPTHS:
        val[d] = sum(1 for r in rows if r["depth"] == d)
    bad = []
    for pat, keys in PROSE:
        hits = re.findall(pat, flat)
        if not hits:
            bad.append("no match for %r" % pat)
            continue
        for h in hits:
            nums = h if isinstance(h, tuple) else (h,)
            for k, num in zip(keys, nums):
                if int(num) != val[k]:
                    bad.append("%r states %s=%s, computed %d"
                               % (pat, k, num, val[k]))
    return bad


# ---------------------------------------------------------------- checks

def audit_checks(doc, reports_dir=None):
    """Returns (rows, refused, checks) where checks is a list of
    (name, status, detail); status PASS / FAIL / NOT_RUN."""
    checks = []
    led_text = fenced(doc, "citation-ledger")
    rows, refused = parse_ledger(led_text)
    n_live = sum(1 for _ in _live(led_text))
    checks.append(("every ledger row classified, none refused",
                   "PASS" if not refused else "FAIL",
                   "; ".join("line %d %s: %s" % r for r in refused)))
    checks.append(("rows in = rows classified + refused",
                   "PASS" if n_live == len(rows) + len(refused) else "FAIL",
                   "%d live, %d + %d" % (n_live, len(rows), len(refused))))
    for block, want in (("citation-table", render_table(rows)),
                        ("citation-counts", render_counts(rows)),
                        ("internal-arith", render_arith())):
        got = fenced(doc, block).rstrip("\n").split("\n")
        checks.append(("%s block equals the computed one" % block,
                       "PASS" if got == want else "FAIL",
                       _first_diff(got, want)))
    rr = rerank(doc, rows)
    got = fenced(doc, "partc-rerank").rstrip("\n").split("\n")
    want = render_rerank(rr)
    checks.append(("partc-rerank block equals the computed one",
                   "PASS" if got == want else "FAIL",
                   _first_diff(got, want)))
    checks.append(("every Part C component change rests on a Part A pass",
                   "PASS" if not rr["problems"] else "FAIL",
                   "; ".join(rr["problems"])))
    want_g = ["S%d" % i for i in range(1, 7)]
    checks.append(("Part C reads the seven-field rubric: a (g) variant at "
                   "every site, S6 included",
                   "PASS" if rr["g_sites"] == want_g else "FAIL",
                   "(g) at %s" % ",".join(rr["g_sites"])))
    by_state = {s: set(r["id"] for r in rows if state_of(r) == s)
                for s in STATES}
    cor = set(re.findall(r"^(A\d{2,3})\s", fenced(doc, "corrected-rows"),
                         re.M))
    checks.append(("A.3 lists exactly the CORRECTED rows",
                   "PASS" if cor == by_state[CORRECTED] else "FAIL",
                   "listed %s computed %s" % (sorted(cor),
                                              sorted(by_state[CORRECTED]))))
    groups = parse_groups(fenced(doc, "unreachable-groups"))
    union, dup = set(), set()
    for _, ids in groups:
        dup |= union & set(ids)
        union |= set(ids)
    checks.append(("A.4 groups are disjoint and cover exactly the "
                   "UNREACHABLE rows",
                   "PASS" if union == by_state[UNREACHABLE] and not dup
                   else "FAIL",
                   "repeated %s; missing %s; extra %s"
                   % (sorted(dup), sorted(by_state[UNREACHABLE] - union),
                      sorted(union - by_state[UNREACHABLE]))))
    ver = set(re.findall(r"^(A\d{2,3})\s", fenced(doc, "verified-notes"),
                         re.M))
    checks.append(("A.5 notes only VERIFIED rows",
                   "PASS" if ver <= by_state[VERIFIED] else "FAIL",
                   "not VERIFIED: %s" % sorted(ver - by_state[VERIFIED])))
    inv = parse_inventory(fenced(doc, "url-inventory"))
    ids = set(r["id"] for r in rows)
    named = set(i for v in inv.values() for i in v)
    missing = sorted(ids - named)
    stray = sorted(named - ids)
    checks.append(("every ledger row appears in the URL inventory",
                   "PASS" if not missing else "FAIL", ", ".join(missing)))
    checks.append(("every inventory id is a ledger row",
                   "PASS" if not stray else "FAIL", ", ".join(stray)))
    context = sum(1 for v in inv.values() if not v)
    bad = prose_problems(doc, rows, context)
    checks.append(("every count stated in prose equals the computed one",
                   "PASS" if not bad else "FAIL", "; ".join(bad)))
    note = re.sub(r"\s+", " ", re.sub(r"(?m)^>\s?", "", doc))
    checks.append(("the top note and the credit line are present",
                   "PASS" if TOP_NOTE in note and all(c in doc for c in
                                                      CREDIT) else "FAIL",
                   ""))
    hashes = parse_hashes(fenced(doc, "report-hashes"))
    if reports_dir is None:
        for name in ("report hashes match the files",
                     "the URL inventory is exactly the reports' URLs",
                     "B.1 term counts",
                     "quote budget: longest verbatim run <= %d words"
                     % QUOTE_BUDGET):
            checks.append((name, "NOT_RUN",
                           "pass --reports DIR; the reports are not "
                           "in the repository"))
        return rows, refused, checks
    texts, bad = {}, []
    for rep, (sha, fname) in sorted(hashes.items()):
        path = os.path.join(reports_dir, fname)
        try:
            with open(path, "rb") as fh:
                raw = fh.read()
        except OSError as ex:
            bad.append("%s: %s" % (fname, ex))
            continue
        if hashlib.sha256(raw).hexdigest() != sha:
            bad.append("%s: sha256 differs" % fname)
        texts[rep] = raw.decode("utf-8")
    checks.append(("report hashes match the files",
                   "PASS" if not bad and len(texts) == 2 else "FAIL",
                   "; ".join(bad)))
    urls = set()
    for t in texts.values():
        urls.update(report_urls(t))
    extra = sorted(set(inv) - urls)
    lack = sorted(urls - set(inv))
    checks.append(("the URL inventory is exactly the reports' URLs",
                   "PASS" if urls and not extra and not lack else "FAIL",
                   "%d in reports, %d listed; missing %s; extra %s"
                   % (len(urls), len(inv), lack[:3], extra[:3])))
    cert = len(re.findall(r"certif", texts.get("C", ""), re.I))
    readout = sum(len(re.findall(r"readout", t, re.I))
                  for t in texts.values())
    checks.append(("B.1 term counts: 'certif' %d in C, 'readout' %d in both"
                   % (cert, readout),
                   "PASS" if (cert, readout) == (TERM_CERTIF, TERM_READOUT)
                   else "FAIL", "the audit states %d and %d"
                   % (TERM_CERTIF, TERM_READOUT)))
    run = max([longest_verbatim(doc, t) for t in texts.values()] or [0])
    checks.append(("quote budget: longest verbatim run <= %d words"
                   % QUOTE_BUDGET, "PASS" if run <= QUOTE_BUDGET
                   else "FAIL", "longest %d words" % run))
    return rows, refused, checks


def _first_diff(got, want):
    for i, (g, w) in enumerate(zip(got, want)):
        if g != w:
            return "line %d: have %r, computed %r" % (i + 1, g, w)
    if len(got) != len(want):
        return "%d lines, computed %d" % (len(got), len(want))
    return ""


def run_audit(reports_dir=None, path=AUDIT):
    try:
        doc = read_doc(path)
        rows, refused, checks = audit_checks(doc, reports_dir)
    except (OSError, LedgerError, ValueError, KeyError) as ex:
        print("could not run the audit checks: %s" % ex)
        print("VERDICT: SKIP   reason=%s" % type(ex).__name__)
        return 3
    for ln in render_counts(rows):
        print(ln)
    print("")
    failed = not_run = 0
    for name, status, detail in checks:
        failed += status == "FAIL"
        not_run += status == "NOT_RUN"
        print("  %-7s %s%s" % (status, name,
                               ("  [%s]" % detail) if detail and
                               status != "PASS" else ""))
    ran = len(checks) - not_run
    print("VERDICT: %s   checks=%d failed=%d not_run=%d"
          % ("PASS" if not failed else "FAIL", ran, failed, not_run))
    return 0 if not failed else 1


def run_ledger(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as ex:
        print("could not read %s: %s" % (path, ex))
        print("VERDICT: SKIP   reason=%s" % type(ex).__name__)
        return 3
    rows, refused = parse_ledger(text)
    for ln in render_table(rows) + [""] + render_counts(rows):
        print(ln)
    for n, rid, why in refused:
        print("REFUSED line %d %s: %s" % (n, rid or "-", why))
    print("VERDICT: %s   rows=%d refused=%d"
          % ("PASS" if not refused else "FAIL", len(rows), len(refused)))
    return 0 if not refused else 1


def run_render(path=AUDIT):
    try:
        doc = read_doc(path)
        rows, _ = parse_ledger(fenced(doc, "citation-ledger"))
        rr = rerank(doc, rows)
    except (OSError, LedgerError, ValueError, KeyError) as ex:
        print("could not render: %s" % ex)
        return 3
    for name, lines in (("citation-table", render_table(rows)),
                        ("citation-counts", render_counts(rows)),
                        ("internal-arith", render_arith()),
                        ("partc-rerank", render_rerank(rr))):
        print("```" + name)
        for ln in lines:
            print(ln)
        print("```")
        print("")
    return 0


# ---------------------------------------------------------------- selftest

def _row(rid, reached="Y", queries="1", exists="Y", says="MATCH",
         found="x", depth="search-index", rep="P"):
    return " | ".join((rid, rep, "S1", "cite", "claim", reached, queries,
                       exists, says, found, depth))


def selftest():
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # known answers: one row per branch of the rule
    plant = "\n".join([
        _row("A01"),                                         # VERIFIED
        _row("A02", says="DIFFERS", found="true value"),     # CORRECTED
        _row("A03", exists="OTHER", says="UNSEEN"),          # NOT_FOUND
        _row("A04", queries="2", exists="N", says="UNSEEN"),  # NOT_FOUND
        _row("A05", queries="1", exists="N", says="UNSEEN"),  # UNREACHABLE
        _row("A06", says="UNSEEN"),                          # UNREACHABLE
        _row("A07", reached="N", exists="?", says="UNSEEN"),  # UNREACHABLE
        _row("A08", reached="?", queries="2", exists="?",
             says="UNSEEN"),                                 # UNREACHABLE
    ])
    rows, refused = parse_ledger(plant)
    got = [state_of(r) for r in rows]
    want = [VERIFIED, CORRECTED, NOT_FOUND, NOT_FOUND, UNREACHABLE,
            UNREACHABLE, UNREACHABLE, UNREACHABLE]
    check("each branch of the four-state rule", got == want and not refused,
          "%s" % got)
    check("one search finding nothing is not NOT FOUND",
          citation_state("Y", 1, "N", "UNSEEN") == UNREACHABLE)
    check("two searches finding nothing is NOT FOUND",
          citation_state("Y", 2, "N", "UNSEEN") == NOT_FOUND)
    check("a seen source with an unseen figure is not NOT FOUND",
          citation_state("Y", 5, "Y", "UNSEEN") == UNREACHABLE)
    check("all four states reachable", set(got) == set(STATES))

    # refusals: malformed rows are refused and counted, never dropped
    bad = "\n".join([
        _row("A10", says="DIFFERS", found=""),      # correction w/o value
        _row("A11", reached="N", says="MATCH"),     # reading nobody saw
        _row("A12", exists="N", says="MATCH"),      # absent but matched
        _row("A13", exists="N", reached="?", says="UNSEEN"),
        _row("A14", depth="vibes"),
        "A15 | P | only three",
        _row("A01"), _row("A01"),                   # repeat
    ])
    rows, refused = parse_ledger(bad)
    check("malformed rows refused", len(refused) == 7,
          "%d refused" % len(refused))
    check("rows in = classified + refused",
          len(rows) + len(refused) == 8, "%d + %d" % (len(rows),
                                                      len(refused)))
    check("a refused row names its reason",
          all(r[2] for r in refused))

    # counts: a row citing both reports counts once in all
    rows, _ = parse_ledger("\n".join([_row("A01", rep="P,C"),
                                      _row("A02", rep="C", says="UNSEEN")]))
    tab = counts(rows)
    check("both-report row counted once in all, once per report",
          tab[VERIFIED] == {"all": 1, "P": 1, "C": 1} and
          tab[UNREACHABLE] == {"all": 1, "P": 0, "C": 1})


    # arithmetic known answers
    ar = {r[0]: r for r in arith_rows()}
    check("kT ln 2 at 300 K is 0.01792 eV",
          ar["kT ln 2 at 300 K, eV"][2] == "0.01792")
    check("34.9/1.2 differs from 28 at stated precision",
          ar["retention 1.2% -> 34.9%, fold"][3] == "DIFFERS")
    check("32.8M/176B agrees with 0.019%",
          ar["32.8M of 176B, %"][3] == "AGREES")
    check("fig4 tau=1 marker is ln 2 + 8.15",
          abs(float(ar["fig4 marker at tau=1, kT"][2]) -
              (math.log(2) + 8.15)) < 1e-3)

    # frontier: the bits toy is all-efficient; a planted dominated point
    # is counted
    pts, dom = bits_frontier()
    check("bits-only frontier: no point dominated", dom == 0,
          "%d" % dom)
    worse = dict(pts[1], survive=pts[0]["survive"] - 0.01,
                 erased=pts[1]["erased"] + 1, free=pts[1]["free"] - 1)
    check("a planted dominated point is counted",
          dominated_count(pts + [worse]) == 1)
    check("majority of 3 at p=0.01 by hand",
          abs(majority_fail(0.01, 3) - (3 * 0.01 ** 2 * 0.99 + 0.01 ** 3))
          < 1e-15)

    # anchor gate: a delta citing an unreachable row is refused
    lrows, _ = parse_ledger(plant)
    dl = parse_deltas("S4b k 1 -> 2 anchors A06 | plant\n"
                      "S4b k 1 -> 2 anchors A02 | plant\n"
                      "S4b k 1 -> 2 anchors A02 corrected-sense | plant\n"
                      "S4b k 1 -> 2 anchors A01 | plant\n")
    probs = anchor_problems(dl, lrows)
    check("delta on UNREACHABLE refused; on CORRECTED refused unless "
          "corrected-sense; on VERIFIED admitted", len(probs) == 2,
          "; ".join(probs))
    try:
        apply_deltas([{"id": "S4b", "comp": {"k": 2}}],
                     parse_deltas("S4b k 1 -> 2 anchors A01 | x"))
        ok = False
    except LedgerError:
        ok = True
    check("a delta whose 'from' disagrees with the table is refused", ok)

    # quote budget
    src = " ".join("w%d" % i for i in range(200))
    check("a copied 50-word run is measured as 50",
          longest_verbatim("x y " + " ".join("w%d" % i for i in
                                             range(10, 60)) + " z", src)
          == 50)
    check("no shared 8-gram measures 0",
          longest_verbatim("a b c d e f g h i", src) == 0)

    # rerank on the real scorer: baseline readings reproduce WO-3
    try:
        sc = load_scorer()
        base = sc.parse_table(sc.fenced(sc.read_doc(), "triage-table"))
        lo = sc.sweep(base, sc.PROFILES["phone"], "LOOP")[1]
        rv = sc.sweep(base, sc.PROFILES["phone"], "REV")[1]
        check("WO-3 baseline reproduces: LOOP S1,S4 tie, REV S4",
              lo == "FIRST_UNRESOLVED:S1,S4" and rv == "FIRST_ROBUST:S4",
              "%s %s" % (lo, rv))
    except Exception as ex:                          # noqa: BLE001
        check("WO-3 baseline reproduces", False, "%s: %s"
              % (type(ex).__name__, ex))

    # the audit itself, when present, and planted drift in a copy of it
    if os.path.exists(AUDIT):
        doc = read_doc(AUDIT)
        _, refused, checks = audit_checks(doc)
        fails = [c for c in checks if c[1] == "FAIL"]
        check("the audit's own checks pass", not fails,
              "; ".join("%s [%s]" % (c[0], c[2]) for c in fails))
        plants = (
            ("an edited count", "NOT_FOUND        0",
             "NOT_FOUND        1", "citation-counts block"),
            ("a row moved out of A.3", "\nA90  P 3.7", "\nX90  P 3.7",
             "A.3 lists exactly"),
            ("a row dropped from A.4", " A97\n", " \n",
             "A.4 groups"),
            ("a stated count changed", "The other 39 links",
             "The other 38 links", "every count stated in prose"),
            ("a delta on an unreachable row", "anchors A52,A54",
             "anchors A52,A56", "Part A pass"),
            ("S6 without a (g) variant", "medium (g) small associative",
             "medium small associative", "seven-field rubric"),
        )
        for label, old, new, name in plants:
            if old not in doc:
                check("plant %s: target text present" % label, False, old)
                continue
            try:
                _, _, pc = audit_checks(doc.replace(old, new, 1))
                hit = [c for c in pc if name in c[0] and c[1] == "FAIL"]
            except LedgerError as ex:
                hit = [str(ex)]
            check("plant %s is caught" % label, hit)

    failed = 0
    for name, ok, detail in results:
        failed += 0 if ok else 1
        print("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                            ("  [%s]" % detail) if detail and not ok
                            else ""))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if not failed else "FAIL", len(results), failed))
    return 0 if not failed else 1


# ---------------------------------------------------------------- main

def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--render" in argv:
        return run_render()
    if "--ledger" in argv:
        i = argv.index("--ledger")
        if i + 1 >= len(argv):
            print("--ledger wants a file")
            print("VERDICT: SKIP   reason=no_file")
            return 3
        return run_ledger(argv[i + 1])
    reports = None
    if "--reports" in argv:
        i = argv.index("--reports")
        if i + 1 >= len(argv) or not os.path.isdir(argv[i + 1]):
            print("--reports wants a directory holding both reports")
            print("VERDICT: SKIP   reason=no_dir")
            return 3
        reports = argv[i + 1]
    return run_audit(reports)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
