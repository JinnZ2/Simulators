#!/usr/bin/env python3
"""readout_count -- the WORK ORDER built as one stdlib instrument.

Reads a flat CSV in the order's SCHEMA and emits what P2, P4 and P5 ask
for, every number reproducible from the CSV by this file:

    readout_count      = distinct positions_returning   (P2 / H2: a
                         declared channel with no return contributes 0)
    declared_count     = distinct positions_declared
    return_rate        = return_count / intake_count     (None on empty)
    external_detection_rate per regime
    P4 cross-tabs      Cramer's V for rate_trend x readout_count,
                       x declared_count, x intake_count -- the V is
                       imported from label-position-test, not copied
    H1 rule            rank(readout_count) against rank(rate_trend)
                       across >= 4 regimes, Spearman by hand

and applies the order's FALSIFICATION lines to the numbers, printing
`undetermined` wherever a number a rule wants is None and
`NOT_COMPUTABLE` where the schema carries no field the rule conditions
on.

No data ships. The SEED ROWS in the order are read back from the order
itself (`--seed`) and each is reported against what the order says a
row needs before it counts; none does yet, and nothing is filled in.
The order says every party that builds, reads or audits a system is a
row, the drafting model included: this file was built by a model from
a model-drafted order and is a row, not an exception.

Choices the order leaves open, marked [CHOICE] and printed:

    [CHOICE 1]  a regime's OUTPUT row is its latest year in the CSV.
    [CHOICE 2]  rate_trend is ordered down > flat > up for ranking.
    [CHOICE 3]  H1's "rank ... matches" is read as Spearman rho > 0;
                strict rank equality is impossible past three regimes
                on a three-level trend, so it is printed and not used.
    [CHOICE 4]  H2's high/low split on declared_count and return_rate
                is at the median across regimes.

CC0. stdlib only. Parses under Python 3.9. Runs on a phone.
"""

import csv
import io
import math
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "label-position-test"))
import label_position_test as LPT  # noqa: E402  (imported, not copied)

UNMEASURED = "UNMEASURED"

VOCAB = {
    "holder": ("builder", "regulator", "third_party"),
    "immunity": ("y", "partial", "n"),
    "investigator_independent": ("y", "partial", "n"),
    "external_detection": ("y", "n"),
    "rate_trend": ("up", "flat", "down"),
}
LISTS = ("positions_declared", "positions_returning")
COUNTS = ("intake_count", "return_count")
FIELDS = ("regime", "year", "positions_declared", "positions_returning",
          "holder", "immunity", "investigator_independent", "intake_count",
          "return_count", "external_detection", "rate_metric", "rate_trend",
          "source_url")

TREND_ORDER = {"up": 0, "flat": 1, "down": 2}   # [CHOICE 2]


class SchemaRefused(ValueError):
    pass


def _split_list(s):
    return sorted({p.strip() for p in s.split(";") if p.strip()})


def _count(s, where):
    s = s.strip()
    if s == UNMEASURED:
        return None
    if not re.fullmatch(r"\d+", s):
        raise SchemaRefused("%s: %r is not a count or UNMEASURED" % (where, s))
    return int(s)


def validate_rows(rows):
    """Refuse a row set outside the schema. Lists are `;`-separated;
    positions_returning must be a subset of positions_declared (a
    channel cannot return without being declared); counts are integers
    or UNMEASURED; every row carries a URL."""
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
        for f in ("regime", "year", "rate_metric", "source_url"):
            if not c[f]:
                raise SchemaRefused("row %d: %s is empty" % (i, f))
        if not re.fullmatch(r"\d{4}", c["year"]):
            raise SchemaRefused("row %d: year %r" % (i, c["year"]))
        for f, voc in VOCAB.items():
            if c[f] not in voc:
                raise SchemaRefused("row %d: %s=%r not in %s" % (i, f, c[f], voc))
        if "://" not in c["source_url"]:
            raise SchemaRefused("row %d: source_url %r is not a URL" % (i, c["source_url"]))
        c["year"] = int(c["year"])
        c["positions_declared"] = _split_list(c["positions_declared"])
        c["positions_returning"] = _split_list(c["positions_returning"])
        if not set(c["positions_returning"]) <= set(c["positions_declared"]):
            raise SchemaRefused("row %d: positions_returning not within positions_declared" % i)
        for f in COUNTS:
            c[f] = _count(c[f], "row %d: %s" % (i, f))
        out.append(c)
    return out


def load_csv(text):
    return validate_rows(list(csv.DictReader(io.StringIO(text))))


# ------------------------------------------------------------ derivations

def derive(row):
    """readout_count, declared_count, return_rate on one row."""
    d = dict(row)
    d["readout_count"] = len(row["positions_returning"])
    d["declared_count"] = len(row["positions_declared"])
    ic, rc = row["intake_count"], row["return_count"]
    d["return_rate"] = None if ic is None or rc is None or ic == 0 else rc / ic
    return d


def per_regime(rows):
    """The OUTPUT row per regime: the latest year [CHOICE 1] for the
    counts and trend, external_detection_rate over all the regime's rows."""
    by = defaultdict(list)
    for r in rows:
        by[r["regime"]].append(r)
    out = {}
    for regime, rs in sorted(by.items()):
        latest = derive(max(rs, key=lambda r: r["year"]))
        ext = sum(1 for r in rs if r["external_detection"] == "y")
        out[regime] = {
            "year": latest["year"],
            "readout_count": latest["readout_count"],
            "declared_count": latest["declared_count"],
            "return_rate": latest["return_rate"],
            "external_detection_rate": ext / len(rs),
            "rate_trend": latest["rate_trend"],
            "rows": len(rs),
        }
    return out


# ------------------------------------------------------------ rank (H1)

def average_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def spearman(x, y):
    """Spearman rho by hand as Pearson on average ranks. None below two
    points or when either side is constant."""
    if len(x) < 2 or len(x) != len(y):
        return None
    rx, ry = average_ranks(x), average_ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    if sxx == 0 or syy == 0:
        return None
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    return sxy / math.sqrt(sxx * syy)


def h1(table):
    """rank(readout_count) against rank(rate_trend) across regimes."""
    regs = sorted(table)
    if len(regs) < 4:
        return {"n_regimes": len(regs), "rho": None, "strict_equal": None,
                "verdict": "undetermined (fewer than 4 regimes)"}
    x = [table[r]["readout_count"] for r in regs]
    y = [TREND_ORDER[table[r]["rate_trend"]] for r in regs]
    rho = spearman(x, y)
    strict = average_ranks(x) == average_ranks(y)
    if rho is None:
        v = "undetermined (a side is constant)"
    elif rho > 0:                                           # [CHOICE 3]
        v = "H1 not falsified by the order's rule (rho > 0)"
    else:
        v = "H1 FALSE by the order's rule (rho <= 0)"
    return {"n_regimes": len(regs), "rho": rho, "strict_equal": strict,
            "verdict": v}


def strict_equality_possible(n_regimes, trend_levels=3):
    """Strict rank equality between a count and a three-level ordinal
    needs the count to tie exactly where the trend ties; with more
    regimes than levels the trend ranks carry ties the count need not,
    and the readout counts would have to collapse onto three values.
    Returns whether any count vector could match: it can only if the
    counts take at most `trend_levels` distinct values."""
    return n_regimes <= trend_levels or "only if readout_count takes <= %d distinct values" % trend_levels


# --------------------------------------------------------- cross-tabs (P4)

def cross_tabs(rows):
    """Cramer's V for rate_trend against readout_count, declared_count
    and intake_count, each taken as categories at its raw values. A
    count with as many levels as rows returns V = 1 by construction;
    the level count is printed beside every V."""
    ds = [derive(r) for r in rows]
    out = {}
    for f in ("readout_count", "declared_count", "intake_count"):
        use = [d for d in ds if d[f] is not None]
        tab = LPT.contingency([{"rate_trend": d["rate_trend"], f: str(d[f])}
                               for d in use], "rate_trend", f)
        out[f] = {"V": LPT.cramers_v(tab), "n": len(use),
                  "levels": len({d[f] for d in use})}
    return out


# --------------------------------------------------------------- H2, H3

def _median(xs):
    s = sorted(xs)
    n = len(s)
    return None if n == 0 else (s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2)


def h2(table):
    """Regimes with high declared_count and low return_rate against
    regimes with high return_rate: their rate_trend distributions.
    Median splits [CHOICE 4]; undetermined if a group is empty."""
    regs = [r for r in table if table[r]["return_rate"] is not None]
    if len(regs) < 2:
        return {"verdict": "undetermined (return_rate on fewer than 2 regimes)",
                "declared_low_return": {}, "high_return": {}}
    md = _median([table[r]["declared_count"] for r in regs])
    mr = _median([table[r]["return_rate"] for r in regs])
    a = [r for r in regs if table[r]["declared_count"] >= md and table[r]["return_rate"] < mr]
    b = [r for r in regs if table[r]["return_rate"] >= mr]
    ta = Counter(table[r]["rate_trend"] for r in a)
    tb = Counter(table[r]["rate_trend"] for r in b)
    if not a or not b:
        v = "undetermined (an arm is empty)"
    else:
        down_a = ta.get("down", 0) / len(a)
        down_b = tb.get("down", 0) / len(b)
        v = ("H2 FALSE by the order's rule (improvement comparable)" if down_a >= down_b
             else "H2 not falsified by the order's rule")
    return {"verdict": v, "declared_low_return": dict(ta), "high_return": dict(tb),
            "median_declared": md, "median_return_rate": mr}


H3_MISSING = ("a split of return_count by origin (internal vs external)",
              "the grading field the rule conditions on")


def h3(rows):
    """The schema carries external_detection per row and no split of
    acted-on counts by origin, and no grading field: the rule's two
    conditions have no column. NOT_COMPUTABLE, with what is missing
    named; external_detection_rate is what the schema does carry."""
    return {"verdict": "NOT_COMPUTABLE", "missing": H3_MISSING,
            "external_detection_rate": (sum(1 for r in rows if r["external_detection"] == "y")
                                        / len(rows)) if rows else None}


# ------------------------------------------------------------ the seed rows

_SEED_HDR = re.compile(r"^\s+regime\s+positions")


def seed_rows(text=None):
    """Read the SEED ROWS table back out of the delivered order, split
    on runs of two or more spaces."""
    if text is None:
        with open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8") as fh:
            text = fh.read()
    lines = text.splitlines()
    out = []
    grab = False
    for line in lines:
        if _SEED_HDR.match(line):
            grab = True
            continue
        if grab:
            if not line.strip():
                if out:
                    break
                continue
            parts = re.split(r"\s{2,}", line.strip())
            if len(parts) == 7:
                out.append(dict(zip(("regime", "positions", "holder", "immunity",
                                     "intake", "return", "rate_trend"), parts)))
    return out


def seed_readiness(seed):
    """Per delivered seed row: what the order says a row needs before it
    counts, and whether the cell as delivered supplies it. Nothing is
    filled in; a bound (`3+`), a grade (`high`), a dash or an n/a is
    reported as what it is."""
    out = []
    for s in seed:
        def kind(cell):
            c = cell.strip()
            if re.fullmatch(r"\d+", c):
                return "count"
            if re.fullmatch(r"\d+\+", c):
                return "bound"
            if c in ("—", "-", "n/a"):
                return "none"
            return "grade"
        trend = s["rate_trend"].strip()
        out.append({
            "regime": s["regime"],
            "source_url": False,                       # the table carries none
            "intake": kind(s["intake"]),
            "return": kind(s["return"]),
            "rate_trend_in_vocab": trend in VOCAB["rate_trend"],
            "rate_trend_cell": trend,
            "counts": False,
        })
    return out


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else ("%.3f" % x if isinstance(x, float) else str(x))


def render(rows=None):
    out = []
    w = out.append
    w("readout_count -- counts from the CSV, nothing else")
    w("")
    w("[CHOICE 1] a regime's OUTPUT row is its latest year")
    w("[CHOICE 2] rate_trend ordered down > flat > up for ranking")
    w("[CHOICE 3] H1 'rank matches' read as Spearman rho > 0; strict equality printed, not used")
    w("[CHOICE 4] H2 high/low splits at the median across regimes")
    w("")
    w("POSITION  this file was built by a model from a model-drafted order;")
    w("  by the order's first paragraph it is a row, not an exception.")
    w("")
    if not rows:
        w("ROWS: none. No data ships with this instrument.")
        w("")
        w("SEED ROWS as delivered, against what the order says a row carries before it counts")
        w("  %-13s | url | intake | return | trend in vocab | counts" % "regime")
        for s in seed_readiness(seed_rows()):
            w("  %-13s | %s | %-6s | %-6s | %-5s %-18s | %s" % (
                s["regime"][:13], "no", s["intake"], s["return"],
                str(s["rate_trend_in_vocab"]), "(%s)" % s["rate_trend_cell"][:16],
                "no"))
        w("  0 of %d seed rows count: none carries a URL, and the intake / return"
          % len(seed_rows()))
        w("  cells are grades, bounds or dashes where the schema wants counts.")
        w("  Nothing is filled in.")
        w("")
        w("H3  NOT_COMPUTABLE from the schema. Missing: %s; %s."
          % (H3_MISSING[0], H3_MISSING[1]))
        w("    the schema carries external_detection per row and nothing else the rule wants.")
    else:
        prov = LPT.provenance([{"source_url": r["source_url"]} for r in rows])
        w("ROWS: %d   provenance: %s" % (len(rows), ", ".join(
            "%s %d" % kv for kv in sorted(prov.items()))))
        if any(k != "public" for k in prov):
            w("  rows outside http(s) are not public record; the numbers below")
            w("  are about the CSV, not about any regime.")
        w("")
        table = per_regime(rows)
        w("OUTPUT  regime | readout_count | declared_count | return_rate | external_detection_rate | rate_trend")
        for reg, t in table.items():
            w("  %-13s | %d | %d | %s | %s | %s   (year %d, rows %d)" % (
                reg[:13], t["readout_count"], t["declared_count"], _f(t["return_rate"]),
                _f(t["external_detection_rate"]), t["rate_trend"], t["year"], t["rows"]))
        w("")
        r1 = h1(table)
        w("H1  regimes %d  rho %s  strict rank equality %s" % (
            r1["n_regimes"], _f(r1["rho"]), _f(r1["strict_equal"])))
        w("    %s" % r1["verdict"])
        w("    strict equality possible: %s" % strict_equality_possible(r1["n_regimes"]))
        w("")
        w("P4  Cramer's V, rate_trend x count (raw values as categories)")
        for f, c in cross_tabs(rows).items():
            w("    %-15s V %s  n %d  levels %d" % (f, _f(c["V"]), c["n"], c["levels"]))
        w("    a count with as many levels as rows gives V = 1 by construction.")
        w("")
        r2 = h2(table)
        w("H2  declared-high / return-low arm: %s   high-return arm: %s" % (
            r2["declared_low_return"], r2["high_return"]))
        w("    %s" % r2["verdict"])
        w("")
        r3 = h3(rows)
        w("H3  %s. Missing: %s; %s." % (r3["verdict"], r3["missing"][0], r3["missing"][1]))
        w("    external_detection_rate over all rows: %s" % _f(r3["external_detection_rate"]))
    w("")
    w("STATES  None = not computable from these rows (empty denominator or")
    w("  constant side); never rendered as 0. No interior claims.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("readout_count.py has no checks of its own; "
                         "they live in selftest_rc.py.\n")
        return 2
    rows = None
    if "--csv" in argv:
        with open(argv[argv.index("--csv") + 1], encoding="utf-8") as fh:
            rows = load_csv(fh.read())
    sys.stdout.write(render(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
