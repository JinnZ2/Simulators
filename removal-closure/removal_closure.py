#!/usr/bin/env python3
"""removal_closure -- the WORK ORDER built as one stdlib instrument.

Reads a flat CSV in the order's SCHEMA (one row per constant-organism-
claim) and emits what P3 asks for, with the order's three FALSIFICATION
lines applied to the numbers and `undetermined` printed wherever a
number a rule wants is None:

    years_to_closure   closure_year - first_correlation_year (None if open)
    H1 rule            a closed row with removal_demonstrated = n
    H2 rule            rank(removability) against rank(time-to-closure),
                       Spearman by hand (imported from readout-count),
                       reported twice: closed rows only, and all rows with
                       open rows right-censored at the current year
    H3 rule            a low-removability row at step >= 4
    P3 cross-tabs      Cramer's V (imported from label-position-test) for
                       step_reached x removability, x dismissal_recorded
    P2 pre-registration  a hash over (constant, organism, removability)
                       that can be published before any closure year is
                       filled, and checked against the CSV afterwards

No data ships. The SEED ROWS are read back from the order (`--seed`) and
each is reported against what the order says a cell needs before it
counts; none carries a citation. What the seed table does state is
checked against itself: the years-to-closure column is recomputed from
the two year cells, decade cells read as a range, and the delivered
figure is placed against that range.

Choices the order leaves open, marked [CHOICE] and printed:

    [CHOICE 1]  a row is CLOSED iff closure_year is not null.
    [CHOICE 2]  `partial` removal_demonstrated does not count as WITHOUT a
                demonstration for H1; the count under the strict reading
                (partial counts as without) is printed beside it.
    [CHOICE 3]  removability is ordered high > medium > low; H2 predicts
                rho(removability, years_to_closure) < 0 and is read as
                falsified at rho >= 0.
    [CHOICE 4]  open rows enter the censored H2 reading at
                CURRENT_YEAR - first_correlation_year, a lower bound.

CC0. stdlib only. Parses under Python 3.9. Runs on a phone.
"""

import csv
import hashlib
import io
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "label-position-test"))
sys.path.insert(0, os.path.join(HERE, "..", "readout-count"))
import label_position_test as LPT  # noqa: E402  (imported, not copied)
import readout_count as RC  # noqa: E402  (imported, not copied)

CURRENT_YEAR = 2026   # [CHOICE 4] the censoring year; printed

VOCAB = {
    "removability": ("high", "medium", "low"),
    "removal_demonstrated": ("y", "n", "partial"),
    "removal_method": ("centrifuge", "constant dark", "isolation", "coil",
                       "shielded chamber", "none"),
    "transducer": ("named", "none"),
    "dismissal_recorded": ("y", "n"),
}
FIELDS = ("constant", "organism", "claim", "step_reached", "removability",
          "removal_demonstrated", "removal_method", "first_correlation_year",
          "closure_year", "transducer", "gain_problem", "dismissal_recorded",
          "source_url")
REMOVABILITY_ORDER = {"low": 0, "medium": 1, "high": 2}   # [CHOICE 3]


class SchemaRefused(ValueError):
    pass


def validate_rows(rows):
    """Refuse a row set outside the schema; return cleaned rows."""
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
        for f in ("constant", "organism", "claim", "gain_problem", "source_url"):
            if not c[f]:
                raise SchemaRefused("row %d: %s is empty" % (i, f))
        if not re.fullmatch(r"[1-5]", c["step_reached"]):
            raise SchemaRefused("row %d: step_reached %r is not one of 1-5" % (i, c["step_reached"]))
        c["step_reached"] = int(c["step_reached"])
        for f, voc in VOCAB.items():
            if c[f] not in voc:
                raise SchemaRefused("row %d: %s=%r not in %s" % (i, f, c[f], voc))
        if not re.fullmatch(r"\d{4}", c["first_correlation_year"]):
            raise SchemaRefused("row %d: first_correlation_year %r" % (i, c["first_correlation_year"]))
        c["first_correlation_year"] = int(c["first_correlation_year"])
        if c["closure_year"].lower() == "null":
            c["closure_year"] = None
        elif re.fullmatch(r"\d{4}", c["closure_year"]):
            c["closure_year"] = int(c["closure_year"])
            if c["closure_year"] < c["first_correlation_year"]:
                raise SchemaRefused("row %d: closure before first correlation" % i)
        else:
            raise SchemaRefused("row %d: closure_year %r is not a year or null" % (i, c["closure_year"]))
        if "://" not in c["source_url"]:
            raise SchemaRefused("row %d: source_url %r is not a URL" % (i, c["source_url"]))
        out.append(c)
    return out


def load_csv(text):
    return validate_rows(list(csv.DictReader(io.StringIO(text))))


# ------------------------------------------------------------ derivations

def closed(r):
    return r["closure_year"] is not None          # [CHOICE 1]


def years_to_closure(r):
    return None if not closed(r) else r["closure_year"] - r["first_correlation_year"]


def years_censored(r, now=CURRENT_YEAR):
    """years_to_closure, or the elapsed open span as a lower bound."""
    return years_to_closure(r) if closed(r) else now - r["first_correlation_year"]


def output_rows(rows):
    return [{"constant": r["constant"], "organism": r["organism"],
             "step": r["step_reached"], "removability": r["removability"],
             "removal_method": r["removal_method"],
             "years_to_closure": years_to_closure(r),
             "transducer": r["transducer"]} for r in rows]


# ------------------------------------------------------------ the rules

def h1(rows):
    """H1 FALSE if >= 1 closed row closed WITHOUT a removal demonstration."""
    cl = [r for r in rows if closed(r)]
    without = [r["constant"] for r in cl if r["removal_demonstrated"] == "n"]
    strict = [r["constant"] for r in cl if r["removal_demonstrated"] in ("n", "partial")]
    if not cl:
        v = "undetermined (no closed row)"
    elif without:
        v = "H1 FALSE by the order's rule"
    else:
        v = "H1 not falsified by the order's rule"
    return {"closed": len(cl), "without": without, "without_strict": strict, "verdict": v}


def h2(rows, now=CURRENT_YEAR):
    """rank(removability) against rank(time-to-closure). Two readings."""
    cl = [r for r in rows if closed(r)]
    out = {}
    for name, rs, yf in (("closed_only", cl, years_to_closure),
                         ("censored", rows, lambda r: years_censored(r, now))):
        x = [REMOVABILITY_ORDER[r["removability"]] for r in rs]
        y = [yf(r) for r in rs]
        rho = RC.spearman(x, y) if len(rs) >= 2 else None
        if rho is None:
            v = "undetermined"
        elif rho < 0:
            v = "H2 not falsified (rho < 0)"
        else:
            v = "H2 FALSE by the order's rule (rho >= 0)"
        out[name] = {"n": len(rs), "rho": rho, "verdict": v,
                     "open_rows_included": name == "censored"}
    out["open_rows"] = [r["constant"] for r in rows if not closed(r)]
    out["open_low_removability"] = [r["constant"] for r in rows
                                    if not closed(r) and r["removability"] == "low"]
    return out


def h3(rows):
    """H3 FALSE if a non-removable constant has reached step 4."""
    hits = [r["constant"] for r in rows if r["removability"] == "low" and r["step_reached"] >= 4]
    low = [r for r in rows if r["removability"] == "low"]
    if not low:
        v = "undetermined (no low-removability row)"
    elif hits:
        v = "H3 FALSE by the order's rule"
    else:
        v = "H3 not falsified by the order's rule"
    return {"low_rows": len(low), "at_step_4_or_more": hits, "verdict": v}


def cross_tabs(rows):
    out = {}
    for f in ("removability", "dismissal_recorded"):
        tab = LPT.contingency([{"step": str(r["step_reached"]), f: r[f]} for r in rows], "step", f)
        out[f] = {"V": LPT.cramers_v(tab), "n": len(rows),
                  "step_levels": len({r["step_reached"] for r in rows}),
                  "levels": len({r[f] for r in rows})}
    return out


# ---------------------------------------------------- P2 pre-registration

def precode_hash(rows):
    """sha256 over sorted (constant, organism, removability) triples --
    the coding P2 says to fix before any closure year is looked at.
    Publish the digest; check it against the filled CSV afterwards."""
    items = sorted((r["constant"], r["organism"], r["removability"]) for r in rows)
    h = hashlib.sha256()
    for t in items:
        h.update(("|".join(t) + "\n").encode("utf-8"))
    return h.hexdigest()


def check_precode(rows, digest):
    return precode_hash(rows) == digest


# ------------------------------------------------------------ seed rows

_SEED_LINE = re.compile(
    r"^\s+(?P<constant>\S+(?: \S+)?)\s{2,}(?P<step>[\d\-]+)\s{2,}(?P<removability>(?:high|medium|LOW|low)\s*\([^)]*\))\s+"
    r"(?P<first>\d{4}s?)\s*→\s*(?P<closure>\d{4}s?|open)\s+(?P<stated>[^\n]+?)\s*$")


def seed_rows(text=None):
    if text is None:
        with open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8") as fh:
            text = fh.read()
    out = []
    for line in text.splitlines():
        m = _SEED_LINE.match(line)
        if m:
            d = m.groupdict()
            d["removability_word"] = d["removability"].split("(")[0].strip().lower()
            out.append(d)
    return out


def _year_range(cell):
    """'1806' -> (1806, 1806); '1930s' -> (1930, 1939); 'open' -> None."""
    if cell == "open":
        return None
    if cell.endswith("s"):
        y = int(cell[:-1])
        return (y, y + 9)
    y = int(cell)
    return (y, y)


def seed_arithmetic(seed, now=CURRENT_YEAR):
    """The seed table's own years-to-closure column against the two year
    cells it sits beside. A decade cell gives a range; the delivered
    figure is placed inside, above or below it."""
    out = []
    for s in seed:
        a = _year_range(s["first"])
        b = _year_range(s["closure"])
        m = re.search(r"~?(\d+)\s*yr", s["stated"])
        stated = int(m.group(1)) if m else None
        if b is None:
            lo = hi = now - a[1] if a else None
            lo = now - a[1]
            hi = now - a[0]
            kind = "open"
        else:
            lo, hi = b[0] - a[1], b[1] - a[0]
            kind = "closed"
        if stated is None:
            place = "no figure"
        elif lo <= stated <= hi:
            place = "inside"
        elif stated < lo:
            place = "below by %d" % (lo - stated)
        else:
            place = "above by %d" % (stated - hi)
        out.append({"constant": s["constant"], "kind": kind, "computed": (lo, hi),
                    "stated": stated, "place": place,
                    "step_cell": s["step"], "step_single": bool(re.fullmatch(r"[1-5]", s["step"]))})
    return out


def seed_readiness(seed):
    return [{"constant": s["constant"], "citation": False,
             "step_single_value": bool(re.fullmatch(r"[1-5]", s["step"])),
             "years_exact": not (s["first"].endswith("s") or s["closure"].endswith("s")),
             "counts": False} for s in seed]


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else ("%.3f" % x if isinstance(x, float) else str(x))


def render(rows=None):
    out = []
    w = out.append
    w("removal_closure -- counts from the CSV, nothing else")
    w("")
    w("[CHOICE 1] a row is CLOSED iff closure_year is not null")
    w("[CHOICE 2] partial removal does not count as WITHOUT for H1; strict count printed beside it")
    w("[CHOICE 3] removability ordered high > medium > low; H2 read as rho < 0")
    w("[CHOICE 4] open rows enter the censored H2 reading at %d - first_correlation_year" % CURRENT_YEAR)
    w("")
    if not rows:
        seed = seed_rows()
        w("ROWS: none. No data ships with this instrument.")
        w("")
        w("SEED ROWS as delivered, against what the order says a cell carries before it counts")
        w("  %-12s | citation | step single | years exact | counts" % "constant")
        for s in seed_readiness(seed):
            w("  %-12s | %-8s | %-11s | %-11s | %s" % (
                s["constant"][:12], "no", str(s["step_single_value"]), str(s["years_exact"]), "no"))
        rd = seed_readiness(seed)
        w("  0 of %d seed rows count: no cell carries a citation; %d step cells are" % (
            len(seed), sum(1 for s in rd if not s["step_single_value"])))
        w("  ranges where the schema wants one value; %d rows carry a decade year cell." % (
            sum(1 for s in rd if not s["years_exact"])))
        w("")
        w("SEED ARITHMETIC  the delivered years-to-closure figure against its own year cells")
        w("  %-12s | %-6s | computed range | stated | placement" % ("constant", "kind"))
        for a in seed_arithmetic(seed):
            w("  %-12s | %-6s | %4d..%-4d      | %-6s | %s" % (
                a["constant"][:12], a["kind"], a["computed"][0], a["computed"][1],
                _f(a["stated"]), a["place"]))
        w("  a decade cell gives a range; 'inside' says the stated figure is consistent")
        w("  with its own cells, not that either cell is right.")
        w("")
        w("P2  removability coding is pre-registered by publishing precode_hash(rows) before")
        w("    any closure_year is filled; the seed table carries both columns in one row.")
    else:
        prov = LPT.provenance([{"source_url": r["source_url"]} for r in rows])
        w("ROWS: %d   provenance: %s" % (len(rows), ", ".join("%s %d" % kv for kv in sorted(prov.items()))))
        if any(k != "public" for k in prov):
            w("  rows outside http(s) are not public record; the numbers below")
            w("  are about the CSV, not about any constant.")
        w("")
        w("OUTPUT  constant | organism | step | removability | removal_method | years_to_closure | transducer")
        for o in output_rows(rows):
            w("  %-12s | %-12s | %d | %-6s | %-16s | %-5s | %s" % (
                o["constant"][:12], o["organism"][:12], o["step"], o["removability"],
                o["removal_method"], _f(o["years_to_closure"]), o["transducer"]))
        w("")
        r1 = h1(rows)
        w("H1  closed rows %d  closed without removal %s  (strict, partial counted: %s)" % (
            r1["closed"], r1["without"] or "none", r1["without_strict"] or "none"))
        w("    %s" % r1["verdict"])
        w("")
        r2 = h2(rows)
        for k in ("closed_only", "censored"):
            w("H2  %-11s n %d  rho %s  %s" % (k, r2[k]["n"], _f(r2[k]["rho"]), r2[k]["verdict"]))
        w("    open rows: %s; of them low-removability: %s" % (
            r2["open_rows"] or "none", r2["open_low_removability"] or "none"))
        w("    the closed-only reading drops every open row, and open rows are where")
        w("    H2 predicts the low-removability constants sit; read the censored row too.")
        w("")
        r3 = h3(rows)
        w("H3  low-removability rows %d  at step >= 4: %s" % (r3["low_rows"], r3["at_step_4_or_more"] or "none"))
        w("    %s" % r3["verdict"])
        w("")
        w("P3  Cramer's V, step_reached x field")
        for f, c in cross_tabs(rows).items():
            w("    %-20s V %s  n %d  step levels %d  field levels %d" % (
                f, _f(c["V"]), c["n"], c["step_levels"], c["levels"]))
        w("")
        w("P2  precode_hash over (constant, organism, removability): %s" % precode_hash(rows)[:16])
    w("")
    w("STATES  None = not computable from these rows; never rendered as 0.")
    w("  No interior claims. Nothing here is a statement about any constant.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("removal_closure.py has no checks of its own; they live in selftest_rmc.py.\n")
        return 2
    rows = None
    if "--csv" in argv:
        with open(argv[argv.index("--csv") + 1], encoding="utf-8") as fh:
            rows = load_csv(fh.read())
    if "--precode" in argv:
        sys.stdout.write(precode_hash(rows) + "\n")
        return 0
    sys.stdout.write(render(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
