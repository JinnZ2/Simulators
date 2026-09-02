#!/usr/bin/env python3
"""encoding_selection -- the WORK ORDER built as one stdlib instrument.

Reads a flat CSV in the order's SCHEMA (one row per reader x item x
format) and emits what P6 asks for, with the order's three
FALSIFICATION lines applied and `undetermined` printed wherever a
number a rule wants is None:

    OUTPUT     per format: n, quantities_recovered frequencies,
               dropped_axes_named rate, rank declines
    H1         Kendall's W by hand over the rankings within-subjects
               readers produced (declines counted apart, never as
               missing), against a permutation null [CHOICE 1]
    H2         within-format against between-format spread of the
               recovered-quantity set, as mean pairwise Jaccard distance
               over the P3 vocabulary [CHOICE 2]
    H3         dropped_axes_named rate for prose (F6) against the
               tabular / dimensional class [CHOICE 3]

and validates an ENCODINGS file against the MATERIAL: seven encodings
per item, each declaring which of the item's facts it carries and which
it drops, an encoding carrying a fact not in the item's list refused
(the order's "without adding facts"). No encoding is authored here --
the order says the encoding is a judgment call and must be published
verbatim, so it is the operator's artifact -- and the material's own
ratio is checked as arithmetic.

No data ships. Nothing here is a claim about any reader or any format.

Choices the order leaves open, marked [CHOICE] and printed:

    [CHOICE 1]  "above chance" for W is a permutation null: each ranker's
                ranks shuffled independently, 2000 draws, seed 0;
                above chance at p < 0.05.
    [CHOICE 2]  "variance in recovered quantity" over a set-valued field is
                mean pairwise Jaccard distance between recovery sets.
    [CHOICE 3]  H3's "table readers" are F3 and F5, the formats the
                hypothesis names by kind (dimensional, tabular per row);
                every other format's rate is printed beside them.
    [CHOICE 4]  H3's "same rate" is read as rate(F6) >= rate(table class).

CC0. stdlib only. Parses under Python 3.9. Runs on a phone.
"""

import csv
import io
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "label-position-test"))
import label_position_test as LPT  # noqa: E402  (imported, not copied)

FORMATS = ("F1", "F2", "F3", "F4", "F5", "F6", "F7")
QUANTITIES = ("magnitude", "disproportion", "chain", "exclusion",
              "cross-domain shape", "sequence", "actor attribution", "other")
VOCAB = {"item": ("M1", "M2"), "format": FORMATS, "design": ("between", "within"),
         "dropped_axes_named": ("y", "n", "partial")}
FIELDS = ("reader_id", "reader_substrate", "item", "format", "design",
          "quantities_recovered", "dropped_axes_named", "rank_given",
          "decline_reason", "response_text")
TABLE_CLASS = ("F3", "F5")     # [CHOICE 3]
PROSE = "F6"
PERMS, SEED, ALPHA = 2000, 0, 0.05   # [CHOICE 1]


class SchemaRefused(ValueError):
    pass


def _split(s):
    return [p.strip() for p in s.split(";") if p.strip()]


def validate_rows(rows):
    if not rows:
        raise SchemaRefused("no rows")
    out = []
    for i, r in enumerate(rows, 1):
        keys = tuple(r.keys())
        missing = [f for f in FIELDS if f not in keys]
        extra = [k for k in keys if k not in FIELDS]
        if missing:
            raise SchemaRefused("row %d: missing column(s) %s" % (i, missing))
        if extra:
            raise SchemaRefused("row %d: column(s) not in schema %s" % (i, extra))
        c = {k: (r[k] or "").strip() for k in FIELDS}
        for f in ("reader_id", "reader_substrate", "response_text"):
            if not c[f]:
                raise SchemaRefused("row %d: %s is empty" % (i, f))
        if not (c["reader_substrate"] == "human" or re.fullmatch(r"model:\S+", c["reader_substrate"])):
            raise SchemaRefused("row %d: reader_substrate %r" % (i, c["reader_substrate"]))
        for f, voc in VOCAB.items():
            if c[f] not in voc:
                raise SchemaRefused("row %d: %s=%r not in %s" % (i, f, c[f], voc))
        q = _split(c["quantities_recovered"])
        bad = [x for x in q if x not in QUANTITIES]
        if bad:
            raise SchemaRefused("row %d: quantities %s not in the P3 vocabulary" % (i, bad))
        c["quantities_recovered"] = sorted(set(q))
        rg = c["rank_given"]
        if rg == "declined":
            c["rank_given"] = "declined"
        elif rg == "":
            c["rank_given"] = None          # between-subjects: no rank asked
        else:
            ranks = _split(rg)
            if len(set(ranks)) != len(ranks) or any(x not in FORMATS for x in ranks):
                raise SchemaRefused("row %d: rank_given %r is not an ordered list of distinct formats" % (i, rg))
            c["rank_given"] = ranks
        if c["design"] == "between" and c["rank_given"] not in (None,):
            raise SchemaRefused("row %d: a between-subjects row carries a rank" % i)
        if c["design"] == "within" and c["rank_given"] is None:
            raise SchemaRefused("row %d: a within-subjects row has neither a rank nor 'declined'" % i)
        if c["rank_given"] == "declined" and not c["decline_reason"]:
            raise SchemaRefused("row %d: declined with no decline_reason" % i)
        out.append(c)
    return out


def load_csv(text):
    return validate_rows(list(csv.DictReader(io.StringIO(text))))


# ---------------------------------------------------------------- OUTPUT

def per_format(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["format"]].append(r)
    out = {}
    for f in FORMATS:
        rs = by.get(f, [])
        n = len(rs)
        freq = Counter(q for r in rs for q in r["quantities_recovered"])
        named = sum(1 for r in rs if r["dropped_axes_named"] == "y")
        partial = sum(1 for r in rs if r["dropped_axes_named"] == "partial")
        within = [r for r in rs if r["design"] == "within"]
        declines = sum(1 for r in within if r["rank_given"] == "declined")
        out[f] = {"n": n, "freq": dict(freq),
                  "dropped_named_rate": None if n == 0 else named / n,
                  "dropped_partial_rate": None if n == 0 else partial / n,
                  "within_n": len(within), "rank_declines": declines}
    return out


# --------------------------------------------------------- H1: Kendall's W

def rankings(rows):
    """One ranking per (reader, item) from within-subjects rows that
    ranked. Rankings are pooled only when every ranker ranked the same
    set of formats; otherwise the pool is refused with the sets named."""
    seen = {}
    declined = set()
    for r in rows:
        if r["design"] != "within":
            continue
        key = (r["reader_id"], r["item"])
        if r["rank_given"] == "declined":
            declined.add(key)          # one decline per reader x item, not per row
            continue
        seen[key] = r["rank_given"]
    declines = len(declined)
    sets = {tuple(sorted(v)) for v in seen.values()}
    if len(sets) > 1:
        return {"rankings": None, "declines": declines, "n_rankers": len(seen),
                "refused": "rankers ranked different format sets: %s" % sorted(sets)}
    return {"rankings": list(seen.values()), "declines": declines,
            "n_rankers": len(seen), "refused": None}


def kendall_w(ranks):
    """W = 12 S / (m^2 (n^3 - n)), S the sum of squared deviations of
    the rank sums from their mean. ranks: list of ordered lists over
    the same n items. None below two rankers or two items."""
    m = len(ranks)
    if m < 2:
        return None
    items = sorted(ranks[0])
    n = len(items)
    if n < 2:
        return None
    sums = {it: 0 for it in items}
    for r in ranks:
        for pos, it in enumerate(r, 1):
            sums[it] += pos
    mean = sum(sums.values()) / n
    S = sum((v - mean) ** 2 for v in sums.values())
    return 12 * S / (m * m * (n ** 3 - n))


def w_null(ranks, perms=PERMS, seed=SEED):
    """Permutation null: each ranker's order shuffled independently.
    Returns (observed W, p = share of draws with W >= observed)."""
    w = kendall_w(ranks)
    if w is None:
        return None, None
    rng = random.Random(seed)
    ge = 0
    for _ in range(perms):
        drawn = []
        for r in ranks:
            x = list(r)
            rng.shuffle(x)
            drawn.append(x)
        if kendall_w(drawn) >= w - 1e-12:
            ge += 1
    return w, ge / perms


def h1(rows):
    rk = rankings(rows)
    if rk["refused"]:
        return dict(rk, W=None, p=None, verdict="undetermined (%s)" % rk["refused"])
    w, p = w_null(rk["rankings"]) if rk["rankings"] else (None, None)
    if w is None:
        v = "undetermined (fewer than 2 rankers)"
    elif p < ALPHA:
        v = "H1 FALSE by the order's rule (W above chance)"
    else:
        v = "H1 not falsified by the order's rule"
    return dict(rk, W=w, p=p, verdict=v)


# --------------------------------------------------------- H2: spread

def jaccard_distance(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 0.0
    return 1.0 - len(a & b) / len(a | b)


def h2(rows):
    """Mean pairwise distance within each format (pooled over formats
    with >= 2 rows) against mean pairwise distance between rows of
    different formats, same item. Plus the within-reader spread for
    within-subjects readers across the formats they saw."""
    by_item = defaultdict(list)
    for r in rows:
        by_item[r["item"]].append(r)
    within_d, between_d = [], []
    for rs in by_item.values():
        for a, b in combinations(rs, 2):
            d = jaccard_distance(a["quantities_recovered"], b["quantities_recovered"])
            (within_d if a["format"] == b["format"] else between_d).append(d)
    wm = sum(within_d) / len(within_d) if within_d else None
    bm = sum(between_d) / len(between_d) if between_d else None
    if wm is None or bm is None:
        v = "undetermined (a pair set is empty)"
    elif wm >= bm:
        v = "H2 FALSE by the order's rule (within >= between)"
    else:
        v = "H2 not falsified by the order's rule"
    # one reader across formats
    by_reader = defaultdict(list)
    for r in rows:
        if r["design"] == "within":
            by_reader[(r["reader_id"], r["item"])].append(r)
    reader_d = [jaccard_distance(a["quantities_recovered"], b["quantities_recovered"])
                for rs in by_reader.values() for a, b in combinations(rs, 2)]
    return {"within_mean": wm, "within_pairs": len(within_d),
            "between_mean": bm, "between_pairs": len(between_d),
            "one_reader_across_formats_mean": sum(reader_d) / len(reader_d) if reader_d else None,
            "verdict": v}


# --------------------------------------------------------- H3: prose vs table

def h3(rows, table_class=TABLE_CLASS):
    pf = per_format(rows)
    prose = pf[PROSE]["dropped_named_rate"]
    tn = sum(pf[f]["n"] for f in table_class)
    ty = sum(1 for r in rows if r["format"] in table_class and r["dropped_axes_named"] == "y")
    table = None if tn == 0 else ty / tn
    if prose is None or table is None:
        v = "undetermined (an arm is empty)"
    elif prose >= table:                       # [CHOICE 4]
        v = "H3 FALSE by the order's rule (prose at or above the table class)"
    else:
        v = "H3 not falsified by the order's rule"
    return {"prose_rate": prose, "prose_n": pf[PROSE]["n"], "table_rate": table, "table_n": tn,
            "per_format": {f: pf[f]["dropped_named_rate"] for f in FORMATS}, "verdict": v}


# ------------------------------------------------------- the material

# The facts each seed item states, read from the order's MATERIAL block.
# An encoding declares, per fact, carried or dropped; a fact not on the
# list is an added fact and refuses the encoding.
FACTS = {
    "M1": ("solve time ~4 h",
           "effort mapping a scorer property ~4 days",
           "the property was declared but not implemented",
           "ratio 24:1"),
    "M2": ("three declared channels",
           "zero returns",
           "rail and air have held, immune channels",
           "under the same department"),
}


def material_ratio():
    """M1's ratio as arithmetic: 4 days over 4 hours."""
    return (4 * 24) / 4


def check_encodings(doc):
    """doc: {item: {format: {"text": str, "carries": [facts], "drops": [facts]}}}.
    Returns per item/format the carried and dropped counts, refuses an
    unknown fact or a fact both carried and dropped, and lists formats
    missing for an item. Nothing about the text is judged."""
    out = {"items": {}, "refused": []}
    for item, facts in FACTS.items():
        encs = doc.get(item, {})
        missing = [f for f in FORMATS if f not in encs]
        rows = {}
        for f, e in encs.items():
            if f not in FORMATS:
                out["refused"].append("%s/%s: not a format" % (item, f))
                continue
            car, dro = set(e.get("carries", [])), set(e.get("drops", []))
            unknown = sorted((car | dro) - set(facts))
            both = sorted(car & dro)
            unstated = sorted(set(facts) - car - dro)
            if unknown:
                out["refused"].append("%s/%s: fact not in the item's list: %s" % (item, f, unknown))
            if both:
                out["refused"].append("%s/%s: carried and dropped: %s" % (item, f, both))
            if not e.get("text", "").strip():
                out["refused"].append("%s/%s: no text (encodings are published verbatim)" % (item, f))
            rows[f] = {"carried": len(car), "dropped": len(dro), "unstated": len(unstated)}
        out["items"][item] = {"formats": rows, "missing": missing}
    return out


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else ("%.3f" % x if isinstance(x, float) else str(x))


def render(rows=None, encodings=None):
    out = []
    w = out.append
    w("encoding_selection -- counts from the CSV, nothing else")
    w("")
    w("[CHOICE 1] W above chance = permutation null, %d draws, seed %d, p < %.2f" % (PERMS, SEED, ALPHA))
    w("[CHOICE 2] spread of a recovered-quantity set = mean pairwise Jaccard distance")
    w("[CHOICE 3] H3 table class = %s; every format's rate printed" % (TABLE_CLASS,))
    w("[CHOICE 4] H3 'same rate' read as rate(F6) >= rate(table class)")
    w("")
    w("MATERIAL  M1 ratio as arithmetic: 4 days / 4 h = %.0f:1 (order states 24:1)" % material_ratio())
    w("  facts per item: M1 %d, M2 %d; an encoding carrying a fact not on the list is refused" % (
        len(FACTS["M1"]), len(FACTS["M2"])))
    if encodings is None:
        w("  ENCODINGS: none supplied. The seven encodings per item are the operator's")
        w("  artifact and are not authored here.")
    else:
        ce = check_encodings(encodings)
        for item, d in ce["items"].items():
            w("  %s  formats present %d of %d, missing %s" % (
                item, len(d["formats"]), len(FORMATS), d["missing"] or "none"))
            for f, c in sorted(d["formats"].items()):
                w("     %s carried %d dropped %d unstated %d" % (f, c["carried"], c["dropped"], c["unstated"]))
        for msg in ce["refused"]:
            w("  REFUSED %s" % msg)
    w("")
    if not rows:
        w("ROWS: none. No data ships with this instrument.")
        w("  The origin reader (n=1, format author present) is excluded by the order's")
        w("  own last limit and is not a row here.")
    else:
        prov = Counter(r["reader_substrate"].split(":")[0] for r in rows)
        w("ROWS: %d   substrates: %s   readers: %d" % (
            len(rows), ", ".join("%s %d" % kv for kv in sorted(prov.items())),
            len({r["reader_id"] for r in rows})))
        w("")
        w("OUTPUT  format | n | quantities_recovered (freq) | dropped_axes_named rate | rank_declines")
        for f, t in per_format(rows).items():
            freq = ", ".join("%s %d" % kv for kv in sorted(t["freq"].items())) or "--"
            w("  %s | %3d | %s | %s (partial %s) | %d of %d within" % (
                f, t["n"], freq, _f(t["dropped_named_rate"]), _f(t["dropped_partial_rate"]),
                t["rank_declines"], t["within_n"]))
        w("")
        r1 = h1(rows)
        w("H1  rankers %d  declines %d  W %s  p %s" % (r1["n_rankers"], r1["declines"], _f(r1["W"]), _f(r1["p"])))
        w("    %s" % r1["verdict"])
        w("    declines are a rate beside W, not rows removed from it.")
        w("")
        r2 = h2(rows)
        w("H2  within-format mean distance %s (%d pairs)  between-format %s (%d pairs)" % (
            _f(r2["within_mean"]), r2["within_pairs"], _f(r2["between_mean"]), r2["between_pairs"]))
        w("    one reader across formats: %s" % _f(r2["one_reader_across_formats_mean"]))
        w("    %s" % r2["verdict"])
        w("")
        r3 = h3(rows)
        w("H3  prose (F6) dropped-axes rate %s (n %d)  table class rate %s (n %d)" % (
            _f(r3["prose_rate"]), r3["prose_n"], _f(r3["table_rate"]), r3["table_n"]))
        w("    per format: " + "  ".join("%s %s" % (f, _f(v)) for f, v in r3["per_format"].items()))
        w("    %s" % r3["verdict"])
    w("")
    w("STATES  None = not computable from these rows; never rendered as 0. No interior claims.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("encoding_selection.py has no checks of its own; they live in selftest_es.py.\n")
        return 2
    rows = enc = None
    if "--csv" in argv:
        with open(argv[argv.index("--csv") + 1], encoding="utf-8") as fh:
            rows = load_csv(fh.read())
    if "--encodings" in argv:
        with open(argv[argv.index("--encodings") + 1], encoding="utf-8") as fh:
            enc = json.load(fh)
    sys.stdout.write(render(rows, enc))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
