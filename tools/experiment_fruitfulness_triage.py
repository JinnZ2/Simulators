#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
experiment_fruitfulness_triage.py -- the scorer for
tools/experiment_fruitfulness_triage.md.

TRIAGE, NOT VALIDATION. The rubric orders five reversible-loop experiment
sites by expected information per unit of a reader's resources, so a
reader picking the repository up cold can choose where to look first.
Nothing here validates any site; every site is a question with a designed
experiment, and none of the experiments has been run.

BIDIRECTIONAL IS NOT REVERSIBLE. A loop can pass signals both ways and
still erase at every step. The score is split in two: Q-LOOP (does
feedback or persistence do work, or the same work cheaper) and Q-REV (does
retain + recover change the cost). A variant whose experiment cannot test
recovery reads NOT_REACHED on Q-REV, never zero.

Everything scored is read from the rubric, never typed here:
    triage-table       fenced block, one row per experiment variant
    triage-basis       fenced block, one stated reason per scored component
    blind-fill         fenced block, the pre-registered site-2 fill (pinned)
    calibration-match  fenced block, each published fact -> rubric field
    Appendix A         the work order as delivered (source of the packet)

Usage
    python3 tools/experiment_fruitfulness_triage.py                report
    python3 tools/experiment_fruitfulness_triage.py --profile lab
    python3 tools/experiment_fruitfulness_triage.py --have compute=medium,lit=high
    python3 tools/experiment_fruitfulness_triage.py --blind-packet
    python3 tools/experiment_fruitfulness_triage.py --selftest

Exit: 0 every check passed; 1 a check failed; 3 could not run
(EXIT_CONTRACT.md). Stdlib only; parses under Python 3.9; no network.
"""

import ast
import hashlib
import math
import os
import re
import sys
import textwrap
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RUBRIC = os.path.join(HERE, "experiment_fruitfulness_triage.md")
README = os.path.join(ROOT, "README.md")
CLAUDE_MD = os.path.join(ROOT, "CLAUDE.md")
TOOL_NAME = "experiment_fruitfulness_triage"

LEVELS = ("low", "medium", "high")
RANK = {"low": 0, "medium": 1, "high": 2}
RESOURCES = ("compute", "data", "lit", "time")
COMPONENTS = ("d", "u", "k", "x", "r")
SITES = ("S1", "S2", "S3", "S4", "S5")
SITE_NAMES = {
    "S1": "STABILITY CONDITIONS",
    "S2": "COMPRESSION PAYOFF",
    "S3": "DORMANT-FACE COST",
    "S4": "LANDAUER / ERASURE JOIN",
    "S5": "INVERSE-DIRECTION REUSE",
}
QUESTIONS = ("LOOP", "REV")
NOT_REACHED = "NOT_REACHED"
NO_FEASIBLE = "NO_FEASIBLE_VARIANT"
TOL = 1e-9

# [CHOICE 1] reader profiles. A variant is FEASIBLE under a profile when
# every resource it needs is at or below the profile's level, otherwise
# BLOCKED with the short resources named. Profiles gate; they never weight.
PROFILES = {
    "phone": {"compute": "low", "data": "low", "lit": "low",
              "time": "low"},
    "this-session": {"compute": "medium", "data": "low", "lit": "medium",
                     "time": "low"},
    "laptop-online": {"compute": "medium", "data": "medium", "lit": "high",
                      "time": "medium"},
    "lab": {"compute": "high", "data": "high", "lit": "high",
            "time": "high"},
}
PROFILE_NOTES = {
    "phone": "stdlib Python, minutes, no download, no full text",
    "this-session": "measured 2026-10-13: stdlib and numpy present, web "
                    "search reachable, full-text hosts refused at DNS, no "
                    "dataset download attempted",
    "laptop-online": "numpy-class compute, public downloads, full text, "
                     "days",
    "lab": "every resource available",
}

# [CHOICE 2] cost per level.  [CHOICE 3] component weights.
COST_MAP = {"low": 1, "medium": 3, "high": 9}
WEIGHTS = {"u": 1, "k": 1, "x": 1}
# [CHOICE 4] the sweep every first-place reading is taken over:
# medium x high with high > medium (8 pairs) x weights {1,2}^3 = 64.
SWEEP_MEDIUM = (2, 3, 4)
SWEEP_HIGH = (4, 9, 16)
SWEEP_WEIGHTS = (1, 2)

# The site-2 blind fill, pinned when it was committed (d5f5c2a).
BLIND_FILL_SHA256 = (
    "a984019ae345e50456f8033ff2af46b576b0b4597526377b5c14975e791bad0c")

ORDER_BEGIN = "<!-- ORDER-BEGIN -->"
ORDER_END = "<!-- ORDER-END -->"

# The packet a blind filler may read: four parts of the work order, each
# from its start marker up to (not including) its end marker.
PACKET_PARTS = (
    ("THE FIVE SITES", "1. STABILITY"),
    ("2. COMPRESSION PAYOFF", "3. DORMANT-FACE"),
    ("HONEST EDGE", "RUBRIC SPEC"),
    ("RUBRIC SPEC", "SCORING:"),
)
# Removed from the packet, each with the space before it: the two
# sentences that name the published answer.
STRIP = (
    "Already has a published emergence case (the 2022 paper above) "
    "— this is the one site with a real worked instance to calibrate "
    "against.",
    "(site 2 has one; check whether 1, 3, 4, 5 do too before assuming "
    "they don't)",
)
# Key terms of the published result. None may appear in the packet or in
# the blind fill. A word list: a paraphrase steps around it, so a clean
# result bounds leakage of these words only.
LEAK_TERMS = ("2022", "emergence", "emergent", "patterns", "kietzmann",
              "energy", "worked instance", "preactivation",
              "pre-activation", "mnist", "lesion", "timescale", "variance",
              "prediction unit", "error unit", "site 2 has one")
NAME_TERMS = ("Ali",)

MATCH_STATES = ("MATCH", "PARTIAL", "NO_SLOT", "NOT_LOCATED")

CARRY = ("TRIAGE, NOT VALIDATION", "BIDIRECTIONAL IS NOT REVERSIBLE")
README_WORDS = ("TRIAGE", "BIDIRECTIONAL", "REVERSIBLE")

STDLIB_ALLOWED = ("ast", "hashlib", "math", "os", "re", "sys", "textwrap",
                  "fractions")


class RubricError(Exception):
    """The rubric is missing a block, or a block is malformed."""


# ---------------------------------------------------------------- reading

def read_doc(path=RUBRIC):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def fenced(doc, name):
    """Content of the one fenced block opened by a line reading three
    backticks and `name`, each line ending in a newline."""
    lines = doc.split("\n")
    opens = [i for i, ln in enumerate(lines) if ln.rstrip() == "```" + name]
    if len(opens) != 1:
        raise RubricError("block %r: %d opening fences, want 1"
                          % (name, len(opens)))
    body = []
    for ln in lines[opens[0] + 1:]:
        if ln.rstrip() == "```":
            return "".join(x + "\n" for x in body)
        body.append(ln)
    raise RubricError("block %r is not closed" % name)


def _live(text):
    for n, ln in enumerate(text.splitlines(), 1):
        if ln.strip() and not ln.lstrip().startswith("#"):
            yield n, ln


def parse_table(text):
    """Rows: id site d u k x r compute data lit time design."""
    rows, seen = [], set()
    for n, ln in _live(text):
        parts = ln.split(None, 11)
        if len(parts) != 12:
            raise RubricError("triage-table line %d: %d fields, want 12"
                              % (n, len(parts)))
        vid, site = parts[0], parts[1]
        if site not in SITES:
            raise RubricError("triage-table line %d: site %r not in %s"
                              % (n, site, ", ".join(SITES)))
        if not re.match(r"^S[1-5][a-z]$", vid) or not vid.startswith(site):
            raise RubricError("triage-table line %d: id %r does not name "
                              "site %s" % (n, vid, site))
        if vid in seen:
            raise RubricError("triage-table line %d: id %r repeated"
                              % (n, vid))
        comp = {}
        for name, raw in zip(COMPONENTS, parts[2:7]):
            if raw not in ("0", "1", "2"):
                raise RubricError("triage-table line %d: %s=%r, want 0..2"
                                  % (n, name, raw))
            comp[name] = int(raw)
        need = {}
        for name, raw in zip(RESOURCES, parts[7:11]):
            if raw not in LEVELS:
                raise RubricError("triage-table line %d: %s=%r, want one "
                                  "of %s" % (n, name, raw, "/".join(LEVELS)))
            need[name] = raw
        seen.add(vid)
        rows.append({"id": vid, "site": site, "comp": comp, "need": need,
                     "design": parts[11].strip()})
    if not rows:
        raise RubricError("triage-table is empty")
    return rows


BASIS_RE = re.compile(r"^(S[1-5][a-z])\.([dukxr])\s+(\S.*)$")


def parse_basis(text):
    """Lines 'S1a.d reason'. One reason per (variant, component)."""
    out = {}
    for n, ln in _live(text):
        m = BASIS_RE.match(ln.strip())
        if not m:
            raise RubricError("triage-basis line %d is not 'S1a.d reason'"
                              % n)
        key = (m.group(1), m.group(2))
        if key in out:
            raise RubricError("triage-basis line %d repeats %s.%s"
                              % ((n,) + key))
        out[key] = m.group(3).strip()
    return out


def missing_basis(rows, basis):
    return [(r["id"], c) for r in rows for c in COMPONENTS
            if (r["id"], c) not in basis]


def orphan_basis(rows, basis):
    ids = set(r["id"] for r in rows)
    return sorted(k for k in basis if k[0] not in ids)


MATCH_RE = re.compile(
    r"^(P\d+)\s*\|\s*([A-Z_]+)\s*\|\s*([^|]*?)\s*\|\s*(\S.*)$")


def parse_match(text):
    """Lines 'P1 | STATE | fields | note'."""
    rows = []
    for n, ln in _live(text):
        m = MATCH_RE.match(ln.strip())
        if not m:
            raise RubricError("calibration-match line %d is not "
                              "'P1 | STATE | fields | note'" % n)
        pid, state, fields, note = m.groups()
        if state not in MATCH_STATES:
            raise RubricError("calibration-match line %d: state %r not in "
                              "%s" % (n, state, ", ".join(MATCH_STATES)))
        rows.append({"id": pid, "state": state, "fields": fields,
                     "note": note})
    ids = [r["id"] for r in rows]
    if not rows:
        raise RubricError("calibration-match is empty")
    if len(set(ids)) != len(ids):
        raise RubricError("calibration-match repeats a fact id")
    return rows


def match_counts(rows):
    return dict((s, sum(1 for r in rows if r["state"] == s))
                for s in MATCH_STATES)


# ---------------------------------------------------------------- scoring

def site_ratio(d, u, k, x, r, compute, data, lit, time, question="LOOP",
               cost_map=None, weights=None):
    """Fruit per unit of resources for one experiment variant.

    fruit_LOOP = d * (wu*u + wk*k + wx*x)
    fruit_REV  = fruit_LOOP * r / 2, and NOT_REACHED when r == 0
    cost       = SUM over compute, data, lit, time of the cost map
    Returns a float, or the string NOT_REACHED (a state, never zero).
    """
    cm = COST_MAP if cost_map is None else cost_map
    w = WEIGHTS if weights is None else weights
    for name, v in zip(COMPONENTS, (d, u, k, x, r)):
        if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= 2:
            raise ValueError("%s must be an int in 0..2, got %r"
                             % (name, v))
    levels = (compute, data, lit, time)
    for lv in levels:
        if lv not in cm:
            raise ValueError("resource level %r not in %s"
                             % (lv, sorted(cm)))
    if question not in QUESTIONS:
        raise ValueError("question %r not in %s" % (question, QUESTIONS))
    fruit = d * (w["u"] * u + w["k"] * k + w["x"] * x)
    if question == "REV":
        if r == 0:
            return NOT_REACHED
        fruit = fruit * r / 2.0
    cost = sum(cm[lv] for lv in levels)
    return fruit / float(cost)


def variant_ratio(row, question, cost_map=None, weights=None):
    c, nd = row["comp"], row["need"]
    return site_ratio(c["d"], c["u"], c["k"], c["x"], c["r"],
                      nd["compute"], nd["data"], nd["lit"], nd["time"],
                      question, cost_map, weights)


def variant_cost(row, cost_map=None):
    cm = COST_MAP if cost_map is None else cost_map
    return sum(cm[row["need"][res]] for res in RESOURCES)


def shortfall(row, have):
    """Resources this variant needs beyond what the reader has."""
    return [res for res in RESOURCES
            if RANK[row["need"][res]] > RANK[have[res]]]


def best_by_site(rows, have, question, cost_map=None, weights=None):
    """Highest feasible ratio per site, as {site: (ratio, variant id)}.
    BLOCKED variants and NOT_REACHED readings are skipped, never scored 0."""
    best = {}
    for row in rows:
        if shortfall(row, have):
            continue
        v = variant_ratio(row, question, cost_map, weights)
        if v == NOT_REACHED:
            continue
        cur = best.get(row["site"])
        if cur is None or v > cur[0] + TOL:
            best[row["site"]] = (v, row["id"])
    return best


def first_set(best):
    if not best:
        return frozenset()
    top = max(v for v, _ in best.values())
    return frozenset(s for s, (v, _) in best.items() if v >= top - TOL)


def classify_first(first_sets):
    """Collapse first-place sets taken across settings into one reading.

    FIRST_ROBUST:<s>        s is the sole first in every setting
    FIRST_SCOPED:<s>        s is the sole first in a strict majority
    FIRST_UNRESOLVED:<a,b>  otherwise: the union of the first sets.
    A tie is held, never broken (tools/held_tie_precision.md).
    """
    sets = [frozenset(s) for s in first_sets]
    if not sets or any(not s for s in sets):
        raise ValueError("every setting needs a non-empty first set")
    n = len(sets)
    sole = {}
    for s in sets:
        if len(s) == 1:
            site = next(iter(s))
            sole[site] = sole.get(site, 0) + 1
    for site, c in sorted(sole.items()):
        if c == n:
            return "FIRST_ROBUST:" + site
    for site, c in sorted(sole.items()):
        if 2 * c > n:
            return "FIRST_SCOPED:" + site
    union = sorted(set().union(*sets))
    return "FIRST_UNRESOLVED:" + ",".join(union)


def sweep_settings():
    out = []
    for m in SWEEP_MEDIUM:
        for h in SWEEP_HIGH:
            if h <= m:
                continue
            cm = {"low": 1, "medium": m, "high": h}
            for wu in SWEEP_WEIGHTS:
                for wk in SWEEP_WEIGHTS:
                    for wx in SWEEP_WEIGHTS:
                        out.append((cm, {"u": wu, "k": wk, "x": wx}))
    return out


def sweep(rows, have, question):
    sets = [first_set(best_by_site(rows, have, question, cm, w))
            for cm, w in sweep_settings()]
    if any(not s for s in sets):
        return sets, NO_FEASIBLE
    return sets, classify_first(sets)


# ---------------------------------------------------------------- packet

def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def order_text(doc):
    """The work order between the Appendix A markers, fence removed."""
    if doc.count(ORDER_BEGIN) != 1 or doc.count(ORDER_END) != 1:
        raise RubricError("Appendix A: want one begin and one end marker")
    inner = doc.split(ORDER_BEGIN, 1)[1].split(ORDER_END, 1)[0]
    lines = inner.strip("\n").split("\n")
    if len(lines) < 3 or lines[0].strip() != "```text" \
            or lines[-1].strip() != "```":
        raise RubricError("Appendix A is not one text fence")
    return "\n".join(lines[1:-1]) + "\n"


def packet_parts(order):
    """The four packet parts, normalized, with STRIP removed."""
    t = norm(order)
    parts = []
    for start, end in PACKET_PARTS:
        for marker in (start, end):
            if t.count(marker) != 1:
                raise RubricError("packet marker %r occurs %d times, want 1"
                                  % (marker, t.count(marker)))
        i, j = t.index(start), t.index(end)
        if j <= i:
            raise RubricError("packet marker %r precedes %r" % (end, start))
        parts.append(t[i:j].strip())
    for target in STRIP:
        cut = " " + norm(target)
        hits = sum(p.count(cut) for p in parts)
        if hits != 1:
            raise RubricError("strip target occurs %d times, want 1: %r"
                              % (hits, target[:40]))
        parts = [p.replace(cut, "", 1) for p in parts]
    return parts


def packet_text(order):
    return " ".join(packet_parts(order))


def leak_hits(text):
    hits = []
    for term in LEAK_TERMS:
        if re.search(r"\b" + re.escape(term), text, re.IGNORECASE):
            hits.append(term)
    for term in NAME_TERMS:
        if re.search(r"\b" + re.escape(term) + r"\b", text):
            hits.append(term)
    return hits


def blind_fill_sha(block):
    return hashlib.sha256(block.encode("utf-8")).hexdigest()


QUOTE_RE = re.compile(r'"([^"]+)"')


def fill_quotes(block):
    out = []
    for ln in block.splitlines():
        if ln.startswith("SRC"):
            out.extend(QUOTE_RE.findall(ln))
    return out


def unsourced_quotes(block, packet):
    return [q for q in fill_quotes(block) if norm(q) not in packet]


def fill_scores(block):
    lines = [ln for ln in block.splitlines() if ln.startswith("SCORES")]
    if len(lines) != 1:
        raise RubricError("blind fill: %d SCORES lines, want 1"
                          % len(lines))
    kv = {}
    for tok in lines[0].split()[1:]:
        if "=" not in tok:
            raise RubricError("blind fill SCORES token %r" % tok)
        key, val = tok.split("=", 1)
        kv[key] = val
    try:
        comp = dict((c, int(kv[c])) for c in COMPONENTS)
        need = dict((res, kv[res]) for res in RESOURCES)
    except (KeyError, ValueError) as ex:
        raise RubricError("blind fill SCORES incomplete: %s" % ex)
    return {"id": "BLIND", "site": "S2", "comp": comp, "need": need,
            "design": "blind fill, section 7.2"}


# ------------------------------------------------- identities (R1, R2, C4)

def entropy(counts):
    total = float(sum(counts))
    return -sum(c / total * math.log2(c / total) for c in counts if c)


def hist(values):
    out = {}
    for v in values:
        out[v] = out.get(v, 0) + 1
    return list(out.values())


def merge_bits(rho, bits=12):
    """One step of x -> floor(rho * x) on a uniform b-bit grid, exact.
    Returns (bits merged by state count, bits merged under Shannon)."""
    f = Fraction(rho).limit_denominator(1000)
    n = 1 << bits
    ys = [(x * f.numerator) // f.denominator for x in range(n)]
    hartley = bits - math.log2(len(set(ys)))
    shannon = bits - entropy(hist(ys))
    return hartley, shannon


def r1_row(rho):
    h, s = merge_bits(rho)
    return ["%.2f" % rho, "%.4f" % h, "%.4f" % math.log2(1.0 / rho),
            "%.4f" % s, "%.4f" % (2.0 * (1.0 - rho))]


def _stage1(v):
    return (v * 37 + 11) % 61


def _stage2(v):
    return (v * v + 3) % 17


def _stage3(v):
    return v % 5


def telescope(bits=8):
    """R2 on a uniform input and three many-to-one stages, exact counts."""
    chain = [list(range(1 << bits))]
    for f in (_stage1, _stage2, _stage3):
        chain.append([f(v) for v in chain[-1]])
    hs = [entropy(hist(c)) for c in chain]
    cond = [entropy(hist(list(zip(chain[i - 1], chain[i])))) - hs[i]
            for i in range(1, len(chain))]
    hxy = entropy(hist(list(zip(chain[0], chain[-1])))) - hs[-1]
    return {"H": hs, "cond_sum": sum(cond), "hx_minus_hy": hs[0] - hs[-1],
            "hx_given_y": hxy, "blind": sum(hs[:-1]),
            "excess": sum(hs[1:])}


def coupling_check(bits=4):
    """An additive-coupling map built from two many-to-one functions is a
    bijection, and the inverse rebuilds every input (sites 4 and 5)."""
    m = 1 << bits

    def f_half(v):
        return (v * v) % m // 2

    def g_half(v):
        return (3 * v + 1) % m // 4

    outs, roundtrip = set(), True
    for x1 in range(m):
        for x2 in range(m):
            y1 = (x1 + f_half(x2)) % m
            y2 = (x2 + g_half(y1)) % m
            outs.add((y1, y2))
            r2 = (y2 - g_half(y1)) % m
            r1 = (y1 - f_half(r2)) % m
            if (r1, r2) != (x1, x2):
                roundtrip = False
    return {"m": m, "distinct": len(outs), "domain": m * m,
            "roundtrip": roundtrip,
            "f_image": len(set(f_half(v) for v in range(m))),
            "g_image": len(set(g_half(v) for v in range(m)))}


def doc_has_tokens(doc, tokens):
    want = list(tokens)
    return any(ln.split() == want for ln in doc.split("\n"))


def identity_checks(doc):
    """R1 and R2 numbers in the rubric, recomputed here."""
    out = []
    for rho in (0.50, 0.75, 0.90):
        row = r1_row(rho)
        out.append(("R1 row rho=%.2f recomputes as printed" % rho,
                    doc_has_tokens(doc, row), " ".join(row)))
    t = telescope()
    rows = [
        ["H", "per", "stage"] + ["%.4f" % h for h in t["H"]],
        ["SUM", "H(h_{l-1}", "|", "h_l)", "%.4f" % t["cond_sum"], "=",
         "H(X)", "-", "H(Y)", "=", "H(X|Y)", "=", "%.4f" % t["hx_given_y"]],
        ["blind", "overwrite", "SUM_{l<L}", "H(h_l)", "=",
         "%.4f" % t["blind"]],
        ["blind", "minus", "the", "floor", "SUM_{l>=1}", "H(h_l)", "=",
         "%.4f" % t["excess"]],
    ]
    for row in rows:
        out.append(("R2 line recomputes as printed: %s" % " ".join(row[:3]),
                    doc_has_tokens(doc, row), " ".join(row)))
    tele = (abs(t["cond_sum"] - t["hx_minus_hy"]) < 1e-12
            and abs(t["cond_sum"] - t["hx_given_y"]) < 1e-12)
    out.append(("R2 telescopes: SUM H(h_{l-1}|h_l) = H(X)-H(Y) = H(X|Y)",
                tele, "%.12f" % t["cond_sum"]))
    return out


# ---------------------------------------------------------------- loading

def load(path=RUBRIC):
    doc = read_doc(path)
    return build(doc)


def build(doc):
    rows = parse_table(fenced(doc, "triage-table"))
    basis = parse_basis(fenced(doc, "triage-basis"))
    match = parse_match(fenced(doc, "calibration-match"))
    fill = fenced(doc, "blind-fill")
    order = order_text(doc)
    return {"doc": doc, "rows": rows, "basis": basis, "match": match,
            "fill": fill, "order": order}


def integrity(st):
    """Checks on the rubric itself; each is (name, ok, detail)."""
    out = []
    rows = st["rows"]
    sites = sorted(set(r["site"] for r in rows))
    out.append(("every site has at least one variant",
                sites == list(SITES), ",".join(sites)))
    miss = missing_basis(rows, st["basis"])
    out.append(("every scored component has a stated basis", not miss,
                " ".join("%s.%s" % m for m in miss[:6])))
    orph = orphan_basis(rows, st["basis"])
    out.append(("no basis line names an unknown variant", not orph,
                " ".join("%s.%s" % m for m in orph[:6])))
    sha = blind_fill_sha(st["fill"])
    out.append(("blind fill unchanged since pinned (sha256)",
                sha == BLIND_FILL_SHA256, sha[:16]))
    packet = packet_text(st["order"])
    quotes = fill_quotes(st["fill"])
    bad = unsourced_quotes(st["fill"], packet)
    out.append(("every blind-fill quote is in the stripped packet",
                bool(quotes) and not bad,
                "%d quotes, %d unsourced" % (len(quotes), len(bad))))
    out.append(("no key term in the blind fill",
                not leak_hits(st["fill"]), ",".join(leak_hits(st["fill"]))))
    out.append(("no key term in the stripped packet",
                not leak_hits(packet), ",".join(leak_hits(packet))))
    for s in CARRY:
        out.append(("carry statement present: %s" % s, s in st["doc"], ""))
    out.extend(identity_checks(st["doc"]))
    return out


# ---------------------------------------------------------------- report

def _fmt(v):
    return v if v == NOT_REACHED else "%.3f" % v


def _short(level):
    return level[0].upper()


def readings(rows, have):
    out = {}
    for q in QUESTIONS:
        best = best_by_site(rows, have, q)
        sets, cls = sweep(rows, have, q)
        out[q] = {"best": best, "first": first_set(best), "sets": sets,
                  "class": cls}
    return out


def calibration(st, have):
    blind = fill_scores(st["fill"])
    res = {"blind": {}, "informed": {}, "moved": {}}
    for q in QUESTIONS:
        b = variant_ratio(blind, q)
        best = best_by_site(st["rows"], have, q).get("S2")
        res["blind"][q] = b
        res["informed"][q] = best
        if best is None or b == NOT_REACHED:
            res["moved"][q] = None
        else:
            res["moved"][q] = best[0] - b
    res["counts"] = match_counts(st["match"])
    return res


def is_g(row):
    """A field (g) EMERGENCE variant: its design opens with "(g)"."""
    return row["design"].startswith("(g)")


def g_readout(rows):
    """What the (g) variants do to the readings, over every profile and
    every sweep setting. Returns the per-variant ratios, the count of
    cells in which a (g) variant is some site's best, whether any reading
    changes when the (g) rows are removed, and the largest ratio of the
    best (g) variant to the top site over all cells."""
    g = [row for row in rows if is_g(row)]
    gids = set(row["id"] for row in g)
    plain = [row for row in rows if not is_g(row)]
    cells = best_cells = 0
    worst = {q: 0.0 for q in QUESTIONS}
    changed = []
    for name in sorted(PROFILES):
        have = PROFILES[name]
        for q in QUESTIONS:
            if sweep(rows, have, q)[1] != sweep(plain, have, q)[1]:
                changed.append("%s Q-%s" % (name, q))
            for cm, w in sweep_settings():
                best = best_by_site(rows, have, q, cm, w)
                cells += len(best)
                best_cells += sum(1 for _, vid in best.values()
                                  if vid in gids)
                top = max(v for v, _ in best.values())
                gv = [variant_ratio(row, q, cm, w) for row in g
                      if not shortfall(row, have)]
                gv = [v for v in gv if v != NOT_REACHED]
                if gv and top > 0:
                    worst[q] = max(worst[q], max(gv) / top)
    return {"rows": g, "cells": cells, "best_cells": best_cells,
            "changed": changed, "worst": worst}


def result_lines(rows, have=None):
    """The compact result the rubric prints in its triage-result block,
    under the phone profile and the declared choices. The selftest holds
    the block to this function, so the printed numbers cannot drift."""
    have = PROFILES["phone"] if have is None else have
    rd = readings(rows, have)
    out = []
    for q in QUESTIONS:
        r = rd[q]
        order = sorted(r["best"].items(), key=lambda kv: (-kv[1][0], kv[0]))
        out.append("Q-%-4s  %s" % (q, " | ".join(
            "%s %.3f %s" % (s, v, vid) for s, (v, vid) in order)))
        dist = {}
        for s in r["sets"]:
            key = ",".join(sorted(s)) or "none"
            dist[key] = dist.get(key, 0) + 1
        out.append("        %s   first across %d settings: %s" % (
            r["class"], len(r["sets"]), "  ".join(
                "{%s} x%d" % (k, v) for k, v in sorted(dist.items()))))
    unreached = [row["id"] for row in rows if row["comp"]["r"] == 0]
    out.append("not reached on Q-REV: %s" % (", ".join(unreached) or "none"))
    same = [name for name in sorted(PROFILES)
            if all(first_set(best_by_site(rows, PROFILES[name], q))
                   == rd[q]["first"] for q in QUESTIONS)]
    out.append("profiles with these first sets: %s" % ", ".join(same))
    for q in QUESTIONS:
        picks = []
        for name in sorted(PROFILES):
            b = best_by_site(rows, PROFILES[name], q).get("S2")
            picks.append("%s %s" % (name, b[1] if b else "none"))
        out.append("best site-2 variant, Q-%s: %s" % (q, ", ".join(picks)))
    gr = g_readout(rows)
    out.append("(g) variants, LOOP/REV: %s" % "  ".join(
        "%s %s/%s" % (row["id"], _fmt(variant_ratio(row, "LOOP")),
                      _fmt(variant_ratio(row, "REV")))
        for row in gr["rows"]))
    out.append("(g) a site's best in %d of %d site-cells (%d profiles x "
               "%d settings x 2 questions); readings changed by (g): %s"
               % (gr["best_cells"], gr["cells"], len(PROFILES),
                  len(sweep_settings()),
                  ", ".join(gr["changed"]) or "none"))
    out.append("(g) best over top, worst cell: LOOP %.3f  REV %.3f"
               % (gr["worst"]["LOOP"], gr["worst"]["REV"]))
    return out


def report(st, profile_name, have):
    rows = st["rows"]
    L = []
    L.append("EXPERIMENT FRUITFULNESS TRIAGE  (tools/%s.md)" % TOOL_NAME)
    L.append("TRIAGE, NOT VALIDATION: this orders where to look first; it "
             "validates no site.")
    L.append("BIDIRECTIONAL IS NOT REVERSIBLE: Q-REV is scored apart; r = 0 "
             "is NOT_REACHED, never 0.")
    L.append("goal     fruit per unit of the reader's resources "
             "(rubric section 2.3)")
    L.append("profile  %s  %s" % (profile_name, " ".join(
        "%s=%s" % (res, have[res]) for res in RESOURCES)))
    if profile_name in PROFILE_NOTES:
        L.append("         %s" % PROFILE_NOTES[profile_name])
    L.append("choices  [2] cost low=%d medium=%d high=%d   [3] weights "
             "u=%d k=%d x=%d   [4] sweep %d settings"
             % (COST_MAP["low"], COST_MAP["medium"], COST_MAP["high"],
                WEIGHTS["u"], WEIGHTS["k"], WEIGHTS["x"],
                len(sweep_settings())))
    L.append("")
    L.append("variant  LOOP   REV          cost  d u k x r  needs c d l t  "
             "state")
    for row in rows:
        c, nd = row["comp"], row["need"]
        short = shortfall(row, have)
        state = "FEASIBLE" if not short else "BLOCKED(%s)" % ",".join(short)
        L.append("%-7s  %-6s %-12s %4d  %d %d %d %d %d        %s %s %s %s  %s"
                 % (row["id"], _fmt(variant_ratio(row, "LOOP")),
                    _fmt(variant_ratio(row, "REV")), variant_cost(row),
                    c["d"], c["u"], c["k"], c["x"], c["r"],
                    _short(nd["compute"]), _short(nd["data"]),
                    _short(nd["lit"]), _short(nd["time"]), state))
    L.append("")
    rd = readings(rows, have)
    for q in QUESTIONS:
        r = rd[q]
        order = sorted(r["best"].items(), key=lambda kv: (-kv[1][0], kv[0]))
        rank = "  ".join("%s %s(%s)" % (s, "%.3f" % v, vid)
                         for s, (v, vid) in order)
        L.append("Q-%-4s  ranked sites, best feasible variant each:" % q)
        L.append("        %s" % (rank or "none feasible"))
        dist = {}
        for s in r["sets"]:
            key = ",".join(sorted(s)) or "none"
            dist[key] = dist.get(key, 0) + 1
        L.append("        first under declared choices: %s"
                 % (",".join(sorted(r["first"])) or "none"))
        L.append("        first across the sweep: %s"
                 % "  ".join("{%s} x%d" % (k, v)
                             for k, v in sorted(dist.items())))
        L.append("        reading: %s" % r["class"])
    unreached = [row["id"] for row in rows if row["comp"]["r"] == 0]
    L.append("NOT_REACHED on Q-REV (no recovery readout): %s"
             % (", ".join(unreached) or "none"))
    L.append("")
    top_u = max(row["comp"]["u"] for row in rows)
    L.append("discovery readout (highest openness u=%d; read apart, never "
             "merged into the ratio):" % top_u)
    for row in rows:
        if row["comp"]["u"] == top_u:
            short = shortfall(row, have)
            L.append("  %-4s %s  %s" % (
                row["id"], "FEASIBLE" if not short else
                "BLOCKED(%s)" % ",".join(short), row["design"]))
    L.append("")
    cal = calibration(st, have)
    L.append("calibration on site 2 (rubric section 7)")
    L.append("  blind fill (7.2)         LOOP %s  REV %s"
             % (_fmt(cal["blind"]["LOOP"]), _fmt(cal["blind"]["REV"])))
    for q in QUESTIONS:
        inf = cal["informed"][q]
        moved = cal["moved"][q]
        L.append("  informed best, Q-%-4s   %s  moved by %s" % (
            q, "none feasible" if inf is None else
            "%s %s" % (inf[1], "%.3f" % inf[0]),
            "n/a" if moved is None else "%+.3f" % moved))
    cts = cal["counts"]
    L.append("  published fact -> field  %s  (%d facts)" % (
        "  ".join("%s %d" % (s, cts[s]) for s in MATCH_STATES),
        sum(cts.values())))
    L.append("")
    L.append("profiles (gate only; first sets under declared choices):")
    for name in sorted(PROFILES):
        h = PROFILES[name]
        parts = []
        for q in QUESTIONS:
            fs = first_set(best_by_site(rows, h, q))
            parts.append("Q-%s {%s}" % (q, ",".join(sorted(fs))))
        L.append("  %-14s %s" % (name, "  ".join(parts)))
    return L


def run_report(profile_name, have, path=RUBRIC):
    try:
        st = load(path)
        lines = report(st, profile_name, have)
        checks = integrity(st)
    except (OSError, RubricError, ValueError) as ex:
        print("could not read the rubric: %s" % ex)
        print("VERDICT: SKIP   reason=%s" % type(ex).__name__)
        return 3
    for ln in lines:
        print(ln)
    print("")
    print("checks on the rubric")
    failed = 0
    for name, ok, detail in checks:
        failed += 0 if ok else 1
        print("  %s  %s%s" % ("PASS" if ok else "FAIL", name,
                              ("  [%s]" % detail) if detail and not ok
                              else ""))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if not failed else "FAIL", len(checks), failed))
    return 0 if not failed else 1


# ---------------------------------------------------------------- packet CLI

def run_blind_packet(path=RUBRIC):
    try:
        doc = read_doc(path)
        parts = packet_parts(order_text(doc))
    except (OSError, RubricError) as ex:
        print("could not build the packet: %s" % ex)
        print("VERDICT: SKIP   reason=%s" % type(ex).__name__)
        return 3
    print("BLIND PACKET for a clean calibration of site 2")
    print("Read this before section 7.3 of the rubric. Fill fields (a)-(f)")
    print("for site 2 from this text only; quote, on every line, the packet")
    print("phrase it rests on; hash the fill (sha256 of its lines, each")
    print("ending in a newline) before reading anything else.")
    print("-" * 72)
    for p in parts:
        print(textwrap.fill(p, 72))
        print("")
    print("-" * 72)
    text = " ".join(parts)
    checks = [
        ("both strip targets removed",
         all(norm(t) not in text for t in STRIP)),
        ("no key term in the packet", not leak_hits(text)),
    ]
    failed = sum(1 for _, ok in checks if not ok)
    for name, ok in checks:
        print("%s  %s" % ("PASS" if ok else "FAIL", name))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if not failed else "FAIL", len(checks), failed))
    return 0 if not failed else 1


# ---------------------------------------------------------------- selftest

def _expect_error(fn, *args):
    try:
        fn(*args)
    except (RubricError, ValueError):
        return True
    return False


def _imports(src):
    names = set()
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    return names


def _line_naming(path, word):
    try:
        text = read_doc(path)
    except OSError:
        return None
    for ln in text.split("\n"):
        if word in ln:
            return ln
    return None


def selftest():
    results = []

    def check(name, ok, detail=""):
        results.append((name, bool(ok), detail))

    # 1. known answers, pure arithmetic
    check("site_ratio: all 2, all low, LOOP = 12/4",
          abs(site_ratio(2, 2, 2, 2, 2, "low", "low", "low", "low")
              - 3.0) < TOL)
    check("site_ratio: d = 0 gives 0 fruit",
          site_ratio(0, 2, 2, 2, 2, "low", "low", "low", "low") == 0.0)
    check("site_ratio: r = 0 on REV is NOT_REACHED, never 0",
          site_ratio(2, 2, 2, 2, 0, "low", "low", "low", "low", "REV")
          == NOT_REACHED)
    check("site_ratio: r = 1 halves REV",
          abs(site_ratio(2, 2, 2, 2, 1, "low", "low", "low", "low", "REV")
              - 1.5) < TOL)
    check("site_ratio: all high costs 36",
          abs(site_ratio(2, 2, 2, 2, 2, "high", "high", "high", "high")
              - 12.0 / 36.0) < TOL)
    check("site_ratio: r is ignored by LOOP",
          site_ratio(2, 1, 1, 1, 0, "low", "low", "low", "low")
          == site_ratio(2, 1, 1, 1, 2, "low", "low", "low", "low"))
    check("site_ratio refuses a bool component",
          _expect_error(site_ratio, True, 1, 1, 1, 1, "low", "low", "low",
                        "low"))
    check("site_ratio refuses a component of 3",
          _expect_error(site_ratio, 3, 1, 1, 1, 1, "low", "low", "low",
                        "low"))
    check("site_ratio refuses an unknown level",
          _expect_error(site_ratio, 1, 1, 1, 1, 1, "cheap", "low", "low",
                        "low"))
    check("classify_first: sole first everywhere is ROBUST",
          classify_first([{"S1"}] * 4) == "FIRST_ROBUST:S1")
    check("classify_first: sole first in 3 of 4 is SCOPED",
          classify_first([{"S1"}] * 3 + [{"S2"}]) == "FIRST_SCOPED:S1")
    check("classify_first: sole first in 2 of 4 is UNRESOLVED",
          classify_first([{"S1"}] * 2 + [{"S2"}] * 2)
          == "FIRST_UNRESOLVED:S1,S2")
    check("classify_first: a tie in every setting is held, not broken",
          classify_first([{"S1", "S4"}] * 4) == "FIRST_UNRESOLVED:S1,S4")
    check("classify_first refuses an empty first set",
          _expect_error(classify_first, [{"S1"}, set()]))
    settings = sweep_settings()
    check("sweep: 64 settings, high > medium in each",
          len(settings) == 64 and all(cm["high"] > cm["medium"]
                                      for cm, _ in settings))
    keys = set(tuple(sorted(cm.items())) + tuple(sorted(w.items()))
               for cm, w in settings)
    check("sweep: settings are distinct", len(keys) == 64)

    # 2. feasibility gates, never weights
    row = {"id": "S9z", "site": "S2",
           "comp": {"d": 2, "u": 1, "k": 1, "x": 1, "r": 1},
           "need": {"compute": "medium", "data": "low", "lit": "high",
                    "time": "low"}, "design": "planted"}
    check("shortfall names each short resource",
          shortfall(row, PROFILES["phone"]) == ["compute", "lit"])
    check("shortfall is empty under lab", shortfall(row, PROFILES["lab"])
          == [])
    unreached = dict(row, comp=dict(row["comp"], r=0), need=dict(
        (res, "low") for res in RESOURCES))
    check("best_by_site skips NOT_REACHED instead of scoring it 0",
          best_by_site([unreached], PROFILES["phone"], "REV") == {})

    # 3. identities behind R1, R2 and the coupling designs
    for rho in (0.5, 0.6, 0.75, 0.9, 0.97):
        h, s = merge_bits(rho)
        check("R1 rho=%.2f: Shannon >= Hartley" % rho, s >= h - 1e-12)
        check("R1 rho=%.2f: Hartley ~ log2(1/rho)" % rho,
              abs(h - math.log2(1.0 / rho)) < 2e-3)
    cp = coupling_check()
    check("coupling map is a bijection on %d states" % cp["domain"],
          cp["distinct"] == cp["domain"])
    check("coupling inverse rebuilds every input", cp["roundtrip"])
    check("coupling halves are many-to-one (reversible from irreversible "
          "parts)", cp["f_image"] < cp["m"] and cp["g_image"] < cp["m"])

    # 4. the real rubric
    try:
        doc = read_doc(RUBRIC)
    except OSError as ex:
        print("could not read the rubric: %s" % ex)
        print("VERDICT: SKIP   reason=%s" % type(ex).__name__)
        return 3
    try:
        st = build(doc)
        built = True
    except RubricError as ex:
        built = False
        check("rubric blocks parse", False, str(ex))
    if built:
        check("rubric blocks parse", True)
        for name, ok, detail in integrity(st):
            check(name, ok, detail)
        rows = st["rows"]
        rd = readings(rows, PROFILES["phone"])
        for q in QUESTIONS:
            stated = "Q-%s reading" % q
            check("%s under phone is stated in the rubric (%s)"
                  % (stated, rd[q]["class"]),
                  rd[q]["class"] in doc, rd[q]["class"])
        want = "".join(ln + "\n" for ln in result_lines(rows))
        try:
            got = fenced(doc, "triage-result")
        except RubricError as ex:
            got = "missing: %s" % ex
        check("triage-result block equals the recomputed result",
              got == want, "rerun and paste result_lines()")
        gsites = set(row["site"] for row in rows if is_g(row))
        check("every site carries a field (g) variant",
              gsites == set(SITES), ",".join(sorted(set(SITES) - gsites)))
        capped = {"id": "S9g", "site": "S1",
                  "comp": {"d": 2, "u": 2, "k": 2, "x": 2, "r": 2},
                  "need": {"compute": "medium", "data": "low", "lit": "low",
                           "time": "low"}, "design": "(g) planted"}
        top = max(v for v, _ in best_by_site(
            rows, PROFILES["lab"], "LOOP").values())
        check("a (g) variant at compute medium is capped below the top "
              "(%.3f < %.3f) whatever its components"
              % (variant_ratio(capped, "LOOP"), top),
              variant_ratio(capped, "LOOP") < top - TOL)
        check("the contaminated calibration stays pinned (d5f5c2a named "
              "in section 9)", "d5f5c2a" in doc)
        check("the start-at-site-2 premise and its failure stay visible",
              '"Start at site 2" was the work order\'s premise' in doc
              and "costs 18 against" in doc)
        a = "\n".join(report(st, "phone", PROFILES["phone"]))
        b = "\n".join(report(st, "phone", PROFILES["phone"]))
        check("report is deterministic", a == b)
        cal = calibration(st, PROFILES["phone"])
        check("calibration: blind fill scores parse", all(
            cal["blind"][q] is not None for q in QUESTIONS))
        cts = cal["counts"]
        stated = "MATCH %d, PARTIAL %d, NO_SLOT %d, NOT_LOCATED %d" % (
            cts["MATCH"], cts["PARTIAL"], cts["NO_SLOT"],
            cts["NOT_LOCATED"])
        check("calibration counts are stated in the rubric (%s)" % stated,
              stated in norm(doc), stated)
        for q in QUESTIONS:
            moved = cal["moved"][q]
            if moved is None:
                check("calibration Q-%s: informed site 2 feasible" % q,
                      False)
                continue
            stated = "Q-%s moved by %+.3f" % (q, moved)
            check("calibration shift is stated in the rubric (%s)" % stated,
                  stated in norm(doc), stated)

        # 5. planted defects: each must be caught
        fill = st["fill"]
        packet = packet_text(st["order"])
        planted = fill.replace("SHAPE  ", "SHAPE  emergence ", 1)
        check("plant: a key term in the fill is caught",
              "emergence" in leak_hits(planted))
        planted = fill.replace('"predict the input top-down"',
                               '"predict the input from the top"', 1)
        check("plant: a quote absent from the packet is caught",
              unsourced_quotes(planted, packet) != [])
        check("plant: a one-character edit changes the pinned hash",
              blind_fill_sha(fill.replace("(a)", "(A)", 1))
              != BLIND_FILL_SHA256)
        basis = dict(st["basis"])
        basis.pop((rows[0]["id"], "k"), None)
        check("plant: a removed basis line is caught",
              missing_basis(rows, basis) == [(rows[0]["id"], "k")])
        check("plant: a component of 3 is refused",
              _expect_error(parse_table,
                            "S1z S1 3 1 1 1 1 low low low low x\n"))
        check("plant: an unknown site is refused",
              _expect_error(parse_table,
                            "S9z S9 1 1 1 1 1 low low low low x\n"))
        check("plant: an id not naming its site is refused",
              _expect_error(parse_table,
                            "S2z S1 1 1 1 1 1 low low low low x\n"))
        check("plant: an undeclared match state is refused",
              _expect_error(parse_match, "P1 | MAYBE | (a) | note\n"))
        check("plant: an order missing a strip target is refused",
              _expect_error(packet_parts,
                            st["order"].replace("Already has", "Has", 1)))
        check("plant: a second blind-fill block is refused",
              _expect_error(fenced, doc + "\n```blind-fill\nx\n```\n",
                            "blind-fill"))
        check("plant: a leak in the packet is caught",
              "energy" in leak_hits(packet + " energy"))

    # 6. the module itself, and where its distinction is carried
    with open(os.path.abspath(__file__), "r", encoding="utf-8") as fh:
        src = fh.read()
    extra = sorted(_imports(src) - set(STDLIB_ALLOWED))
    check("imports only the declared stdlib modules", not extra,
          ",".join(extra))
    try:
        ast.parse(src, feature_version=(3, 9))
        ok39 = True
    except SyntaxError:
        ok39 = False
    check("own source parses under the Python 3.9 grammar", ok39)
    line = _line_naming(README, TOOL_NAME)
    check("README line naming the tool carries TRIAGE, BIDIRECTIONAL, "
          "REVERSIBLE", line is not None
          and all(w in line for w in README_WORDS))
    line = _line_naming(CLAUDE_MD, TOOL_NAME + ".")
    check("CLAUDE.md names the tool and carries REVERSIBLE",
          line is not None and "REVERSIBLE" in line)

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

def parse_have(spec):
    have = dict(PROFILES["phone"])
    for item in spec.split(","):
        if not item.strip():
            continue
        if "=" not in item:
            raise ValueError("--have wants resource=level, got %r" % item)
        res, lv = [s.strip() for s in item.split("=", 1)]
        if res not in RESOURCES or lv not in LEVELS:
            raise ValueError("--have: %r=%r; resources %s, levels %s"
                             % (res, lv, "/".join(RESOURCES),
                                "/".join(LEVELS)))
        have[res] = lv
    return have


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if "--blind-packet" in argv:
        return run_blind_packet()
    profile, have = "phone", dict(PROFILES["phone"])
    if "--profile" in argv:
        i = argv.index("--profile")
        name = argv[i + 1] if i + 1 < len(argv) else ""
        if name not in PROFILES:
            print("unknown profile %r; known: %s"
                  % (name, ", ".join(sorted(PROFILES))))
            print("VERDICT: SKIP   reason=unknown_profile")
            return 3
        profile, have = name, dict(PROFILES[name])
    if "--have" in argv:
        i = argv.index("--have")
        try:
            have = parse_have(argv[i + 1] if i + 1 < len(argv) else "")
        except ValueError as ex:
            print(ex)
            print("VERDICT: SKIP   reason=bad_have")
            return 3
        profile = "custom"
    return run_report(profile, have)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
