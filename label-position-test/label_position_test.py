#!/usr/bin/env python3
"""label_position_test -- the WORK ORDER built as one stdlib instrument.

Reads a flat CSV in the order's SCHEMA (one row per event, one source
URL per row) and emits the numbers P2, P4 and P5 ask for, every one
reproducible from the CSV by this script:

    P2  leak test        actor_class from (move, wall_author, cost_bearer,
                         wall_purpose_visible_to_actor) -- two readings,
                         in-sample lookup and leave-one-out, against the
                         majority-class baseline
    P4  cross-tabs       Cramer's V by hand for label_valence x
                         {position_t0, move, outcome_t1, actor_class}
    P5  overlap_rate     per label_source class, against a chance rate
                         computed from the class's own marginals
    +   within-document control (SEED CASE): rows sharing a source_url
                         with actor_class and position_t0 held and move
                         varying -- does valence vary with move alone?
    +   relabel agreement (P3): pairwise agreement and Fleiss' kappa by
                         hand over a labeler sheet

No data ships with this file. The seed case's report is not reachable
from the environment this was built in, so the within-document control
has nothing to run on and says so. Constructed rows exist only in the
selftest and the samples, labelled as such: their source_url scheme is
`constructed://`, and the report counts them apart from http(s) rows.

Where the order leaves a quantity undefined, the choice made here is
marked [CHOICE] in the code and printed in every render:

    [CHOICE 1]  chance for H2 is the expected match rate under
                independence of arbiter and beneficiary within the
                label_source class, sum_a p_arb(a) * p_ben(a).
    [CHOICE 2]  `partial` overlap is reported two ways, strict (y only)
                and half (y + 0.5 * partial). Neither is picked.
    [CHOICE 3]  the leak baseline is the majority-class share of
                actor_class (a labeler who guesses the commonest class).

Every field is a state, never a guess: a missing or unrecognised value
is refused at load, a cross-tab with fewer than two levels on either
axis returns None (V is undefined there, not zero), and a rate over an
empty denominator returns None, never 0.

Interior claims: none. Verdict lines print the order's own FALSIFICATION
rule applied to the computed numbers, and print `undetermined` where a
number the rule needs is None.

CC0. stdlib only. Parses under Python 3.9. Runs on a phone.
"""

import csv
import io
import math
import sys
from collections import Counter, defaultdict

# ---------------------------------------------------------------- schema

VOCAB = {
    "actor_class": ("agent", "firm", "individual", "state"),
    "position_t0": ("up", "down", "none"),
    "move": ("declared_path", "undeclared_open", "built_wall_crossed"),
    "wall_author": ("task_setter", "third_party", "none"),
    "wall_purpose_visible_to_actor": ("y", "n"),
    "cost_bearer": ("self", "definer", "third_party", "none"),
    "outcome_t1": ("success", "fail", "mixed"),
    "label_valence": ("+", "-", "0"),
    "overlap": ("y", "partial", "n"),
}

FREE = ("label_source", "label_term", "label_t", "relabel_term",
        "relabel_t", "arbiter", "beneficiary", "source_url")

FIELDS = (
    "actor_class", "position_t0", "move", "wall_author",
    "wall_purpose_visible_to_actor", "cost_bearer", "outcome_t1",
    "label_source", "label_term", "label_valence", "label_t",
    "relabel_term", "relabel_t", "arbiter", "beneficiary", "overlap",
    "source_url",
)

# Fields that may be empty: a relabel that never happened is an empty
# cell, which is a state (no later term) and not a gap.
MAY_BE_EMPTY = ("relabel_term", "relabel_t")

LEAK_TUPLE = ("move", "wall_author", "cost_bearer",
              "wall_purpose_visible_to_actor")

CROSS_TABS = (("V_position", "position_t0"), ("V_move", "move"),
              ("V_outcome", "outcome_t1"), ("V_actor", "actor_class"))


class SchemaRefused(ValueError):
    pass


def validate_rows(rows):
    """Refuse a row set that is not in the order's schema.

    Returns the rows unchanged. Raises SchemaRefused naming the first
    row and field that fails. A missing column, an extra column, an
    empty required cell, a value outside a closed vocabulary, or a row
    with no source_url each refuse the whole set: a partly valid CSV
    would produce numbers over a denominator nobody declared.
    """
    if not rows:
        raise SchemaRefused("no rows")
    for i, r in enumerate(rows, 1):
        keys = tuple(r.keys())
        missing = [f for f in FIELDS if f not in keys]
        extra = [k for k in keys if k not in FIELDS]
        if missing:
            raise SchemaRefused("row %d: missing column(s) %s" % (i, missing))
        if extra:
            raise SchemaRefused("row %d: column(s) not in schema %s" % (i, extra))
        for f in FIELDS:
            v = (r[f] or "").strip()
            if v == "" and f not in MAY_BE_EMPTY:
                raise SchemaRefused("row %d: %s is empty" % (i, f))
            if f in VOCAB and v not in VOCAB[f]:
                raise SchemaRefused("row %d: %s=%r not in %s"
                                    % (i, f, v, VOCAB[f]))
        url = r["source_url"].strip()
        if "://" not in url:
            raise SchemaRefused("row %d: source_url %r is not a URL" % (i, url))
    return rows


def load_csv(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    for r in rows:
        for k in list(r.keys()):
            r[k] = (r[k] or "").strip()
    return validate_rows(rows)


def provenance(rows):
    """Count rows by source_url scheme. http/https is the public record
    the order asks for; anything else is not, and is counted apart."""
    out = Counter()
    for r in rows:
        scheme = r["source_url"].split("://", 1)[0].lower()
        out["public" if scheme in ("http", "https") else scheme] += 1
    return dict(out)


# ------------------------------------------------------------ arithmetic

def contingency(rows, a, b):
    table = defaultdict(Counter)
    for r in rows:
        table[r[a]][r[b]] += 1
    return {k: dict(v) for k, v in table.items()}


def chi2(table):
    """Pearson chi-square over a nested dict {row: {col: count}}."""
    rows = list(table)
    cols = sorted({c for r in rows for c in table[r]})
    n = sum(sum(table[r].values()) for r in rows)
    if n == 0:
        return None, 0, len(rows), len(cols)
    rt = {r: sum(table[r].values()) for r in rows}
    ct = {c: sum(table[r].get(c, 0) for r in rows) for c in cols}
    x = 0.0
    for r in rows:
        for c in cols:
            e = rt[r] * ct[c] / n
            if e > 0:
                o = table[r].get(c, 0)
                x += (o - e) ** 2 / e
    return x, n, len(rows), len(cols)


def cramers_v(table):
    """V = sqrt(chi2 / (n * min(k-1, r-1))), by hand.

    None when either axis has fewer than two levels: the divisor is
    zero and V is undefined there, which is not the same as V = 0.
    """
    x, n, r, k = chi2(table)
    if x is None or min(k - 1, r - 1) < 1:
        return None
    return math.sqrt(x / (n * min(k - 1, r - 1)))


def cross_tabs(rows):
    out = {}
    for name, field in CROSS_TABS:
        out[name] = cramers_v(contingency(rows, "label_valence", field))
    return out


def _rate(num, den):
    return None if den == 0 else num / den


# ------------------------------------------------------------ P5 overlap

def overlap_derived(r):
    """The overlap the two fields imply. `partial` cannot be derived
    from two strings, so this returns y or n and the coded field is
    compared against it where it says y or n."""
    return "y" if r["arbiter"] == r["beneficiary"] else "n"


def overlap_rates(rows):
    """Per label_source class: n, strict rate (y only), half rate
    (y + 0.5 partial), chance under independence of arbiter and
    beneficiary within the class [CHOICE 1], and the count of rows
    whose coded overlap disagrees with the derived one."""
    by = defaultdict(list)
    for r in rows:
        by[r["label_source"]].append(r)
    out = {}
    for src, rs in sorted(by.items()):
        n = len(rs)
        y = sum(1 for r in rs if r["overlap"] == "y")
        p = sum(1 for r in rs if r["overlap"] == "partial")
        arb = Counter(r["arbiter"] for r in rs)
        ben = Counter(r["beneficiary"] for r in rs)
        chance = sum((arb[a] / n) * (ben.get(a, 0) / n) for a in arb)
        disagree = sum(1 for r in rs
                       if r["overlap"] in ("y", "n")
                       and r["overlap"] != overlap_derived(r))
        out[src] = {
            "n": n,
            "strict": _rate(y, n),
            "half": _rate(y + 0.5 * p, n),
            "chance": chance,
            "coded_vs_derived_disagree": disagree,
        }
    return out


# --------------------------------------------------------------- P2 leak

def leak_test(rows):
    """Can actor_class be read off the move tuple?

    in_sample: a lookup table built on all rows and scored on them --
               an UPPER bound, and 1.0 whenever every tuple is unique.
    loo:       leave-one-out -- each row scored by the majority class
               among the OTHER rows sharing its tuple, falling back to
               the majority class of the others when none share it.
    baseline:  majority-class share of actor_class [CHOICE 3].
    """
    n = len(rows)
    if n == 0:
        return {"n": 0, "in_sample": None, "loo": None, "baseline": None,
                "distinct_tuples": 0, "tuple_space": _tuple_space()}
    key = lambda r: tuple(r[f] for f in LEAK_TUPLE)  # noqa: E731
    groups = defaultdict(Counter)
    for r in rows:
        groups[key(r)][r["actor_class"]] += 1
    overall = Counter(r["actor_class"] for r in rows)
    hit_in = 0
    for r in rows:
        maj = groups[key(r)].most_common(1)[0][0]
        hit_in += maj == r["actor_class"]
    hit_loo = 0
    for r in rows:
        g = Counter(groups[key(r)])
        g[r["actor_class"]] -= 1
        g = +g
        if g:
            pred = g.most_common(1)[0][0]
        else:
            o = Counter(overall)
            o[r["actor_class"]] -= 1
            o = +o
            pred = o.most_common(1)[0][0] if o else None
        hit_loo += pred == r["actor_class"]
    return {
        "n": n,
        "in_sample": hit_in / n,
        "loo": hit_loo / n,
        "baseline": overall.most_common(1)[0][1] / n,
        "distinct_tuples": len(groups),
        "tuple_space": _tuple_space(),
    }


def _tuple_space():
    s = 1
    for f in LEAK_TUPLE:
        s *= len(VOCAB[f])
    return s


# --------------------------------------------- SEED CASE within-document

def within_document_control(rows):
    """For each source_url with two or more rows: hold actor_class and
    position_t0, let move vary, and report whether label_valence varies
    with it. A URL with one row, or with no pair differing on move at
    fixed (actor_class, position_t0), carries nothing and is listed as
    such rather than dropped."""
    by = defaultdict(list)
    for r in rows:
        by[r["source_url"]].append(r)
    out = {}
    for url, rs in sorted(by.items()):
        if len(rs) < 2:
            out[url] = {"rows": len(rs), "pairs": 0, "valence_varies": None}
            continue
        pairs = 0
        varies = 0
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, b = rs[i], rs[j]
                if (a["actor_class"] == b["actor_class"]
                        and a["position_t0"] == b["position_t0"]
                        and a["move"] != b["move"]):
                    pairs += 1
                    varies += a["label_valence"] != b["label_valence"]
        out[url] = {"rows": len(rs), "pairs": pairs,
                    "valence_varies": None if pairs == 0 else varies / pairs}
    return out


# ---------------------------------------------------------- P3 relabel

def relabel_agreement(sheet):
    """sheet: {row_id: {labeler: valence}} with the same labelers on
    every row. Returns pairwise agreement and Fleiss' kappa by hand.
    kappa is None when every rating is one category (P_e = 1)."""
    ids = sorted(sheet)
    if not ids:
        return {"rows": 0, "labelers": 0, "pairwise": None, "kappa": None}
    labelers = sorted(sheet[ids[0]])
    m = len(labelers)
    if m < 2 or any(sorted(sheet[i]) != labelers for i in ids):
        raise ValueError("every row needs the same >= 2 labelers")
    cats = sorted({sheet[i][l] for i in ids for l in labelers})
    N = len(ids)
    P_i = []
    for i in ids:
        c = Counter(sheet[i].values())
        P_i.append((sum(v * v for v in c.values()) - m) / (m * (m - 1)))
    P_bar = sum(P_i) / N
    p_j = [sum(1 for i in ids for l in labelers if sheet[i][l] == c)
           / (N * m) for c in cats]
    P_e = sum(p * p for p in p_j)
    kappa = None if P_e >= 1.0 else (P_bar - P_e) / (1 - P_e)
    return {"rows": N, "labelers": m, "pairwise": P_bar, "kappa": kappa,
            "categories": cats}


# ------------------------------------------------------- the order's rule

def h1_rule(v):
    """H1 is FALSE if V_move >= V_position AND V_move >= V_outcome."""
    a, b, c = v["V_move"], v["V_position"], v["V_outcome"]
    if a is None or b is None or c is None:
        return "undetermined"
    return "H1 FALSE by the order's rule" if (a >= b and a >= c) \
        else "H1 not falsified by the order's rule"


def h2_rule(ov, key="strict"):
    """H2 is FALSE if overlap_rate <= chance for that label_source class."""
    out = {}
    for src, o in ov.items():
        r = o[key]
        if r is None:
            out[src] = "undetermined"
        else:
            out[src] = ("H2 FALSE for this class" if r <= o["chance"]
                        else "H2 not falsified for this class")
    return out


# ---------------------------------------------------------------- output

def _f(x):
    return "--" if x is None else "%.3f" % x


def output_table(rows):
    """The order's OUTPUT row shape, one row per label_term plus ALL.

    Within a single term label_valence is a constant whenever the term
    carries one valence, so every V on that row is None: the order's
    cross-tab has nothing to vary against. The pooled row is where the
    cross-tabs live. Both are printed; neither is dropped.
    """
    terms = defaultdict(list)
    for r in rows:
        terms[r["label_term"]].append(r)
    table = []
    for term, rs in [("ALL", rows)] + sorted(terms.items()):
        v = cross_tabs(rs)
        ov = overlap_rates(rs)
        n = len(rs)
        y = sum(o["strict"] * o["n"] for o in ov.values()
                if o["strict"] is not None)
        lk = leak_test(rs)
        table.append({
            "term": term, "n": n,
            "V_position": v["V_position"], "V_move": v["V_move"],
            "V_outcome": v["V_outcome"], "V_actor": v["V_actor"],
            "overlap_rate": _rate(y, n), "leak_rate": lk["loo"],
        })
    return table


def render(rows=None, relabel=None):
    out = []
    w = out.append
    w("label_position_test -- counts from the CSV, nothing else")
    w("")
    w("[CHOICE 1] H2 chance = sum_a p_arb(a) * p_ben(a) within the label_source class")
    w("[CHOICE 2] overlap rate reported strict (y) and half (y + 0.5 partial); neither picked")
    w("[CHOICE 3] leak baseline = majority-class share of actor_class")
    w("")
    if not rows:
        w("ROWS: none. No data ships with this instrument.")
        w("  The seed case (METR / Redwood, 2026-08-26) is not reachable from")
        w("  the environment this was built in; the within-document control")
        w("  has nothing to run on. Every cell below is empty for that reason.")
        w("")
        w("OUTPUT  term | n | V_position | V_move | V_outcome | V_actor | overlap_rate | leak_rate")
        w("  (no rows)")
        w("")
        w("LEAK TEST (P2)  tuple space %d cells over %s" % (_tuple_space(), ", ".join(LEAK_TUPLE)))
        w("  at the order's N floor of 30 the space has more cells than rows,")
        w("  so the in-sample reading approaches 1.0 by construction and only")
        w("  the leave-one-out reading is informative.")
    else:
        prov = provenance(rows)
        w("ROWS: %d   provenance: %s" % (len(rows), ", ".join(
            "%s %d" % kv for kv in sorted(prov.items()))))
        if any(k != "public" for k in prov):
            w("  rows outside http(s) are not public record; the numbers below")
            w("  are about the CSV, not about any case.")
        w("")
        w("OUTPUT  term | n | V_position | V_move | V_outcome | V_actor | overlap_rate | leak_rate")
        for t in output_table(rows):
            w("  %-22s | %3d | %s | %s | %s | %s | %s | %s" % (
                t["term"][:22], t["n"], _f(t["V_position"]), _f(t["V_move"]),
                _f(t["V_outcome"]), _f(t["V_actor"]), _f(t["overlap_rate"]),
                _f(t["leak_rate"])))
        w("  a V of -- on a term row is undefined, not zero: the valence does")
        w("  not vary within that term, so there is nothing to cross-tabulate.")
        w("")
        v = cross_tabs(rows)
        w("CROSS-TABS (P4), pooled   " + "  ".join(
            "%s %s" % (k, _f(v[k])) for k, _ in CROSS_TABS))
        w("  " + h1_rule(v))
        w("")
        ov = overlap_rates(rows)
        w("OVERLAP (P5) per label_source class")
        w("  %-20s | n | strict | half | chance | coded!=derived" % "label_source")
        for src, o in ov.items():
            w("  %-20s | %d | %s | %s | %s | %d" % (
                src[:20], o["n"], _f(o["strict"]), _f(o["half"]),
                _f(o["chance"]), o["coded_vs_derived_disagree"]))
        for src, verdict in h2_rule(ov).items():
            w("  %s: %s (strict)" % (src[:20], verdict))
        w("")
        lk = leak_test(rows)
        w("LEAK TEST (P2)  n %d  distinct tuples %d of %d cells" % (
            lk["n"], lk["distinct_tuples"], lk["tuple_space"]))
        w("  in-sample %s   leave-one-out %s   baseline %s" % (
            _f(lk["in_sample"]), _f(lk["loo"]), _f(lk["baseline"])))
        w("  in-sample is an upper bound; read leave-one-out against baseline.")
        w("")
        w("WITHIN-DOCUMENT CONTROL (seed case shape)")
        wd = within_document_control(rows)
        singles = sum(1 for c in wd.values() if c["rows"] < 2)
        for url, c in wd.items():
            if c["rows"] < 2:
                continue
            w("  %-40s rows %d  pairs %d  valence varies %s" % (
                url[:40], c["rows"], c["pairs"], _f(c["valence_varies"])))
        w("  single-row URLs: %d (carry no control pair)" % singles)
        if singles == len(wd):
            w("  no URL carries two rows; the control has nothing to run on.")
    if relabel is not None:
        w("")
        ra = relabel_agreement(relabel)
        w("RELABEL (P3)  rows %d  labelers %d  pairwise %s  kappa %s" % (
            ra["rows"], ra["labelers"], _f(ra["pairwise"]), _f(ra["kappa"])))
    w("")
    w("STATES  None = not computable from these rows (undefined divisor or")
    w("  empty denominator); never rendered as 0. No interior claims.")
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------- CLI

def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("label_position_test.py has no checks of its own; "
                         "they live in selftest_lpt.py.\n")
        return 2
    rows = None
    relabel = None
    if "--csv" in argv:
        path = argv[argv.index("--csv") + 1]
        with open(path, encoding="utf-8") as fh:
            rows = load_csv(fh.read())
    if "--relabel" in argv:
        import json
        path = argv[argv.index("--relabel") + 1]
        with open(path, encoding="utf-8") as fh:
            relabel = json.load(fh)
    sys.stdout.write(render(rows, relabel))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
