# SPDX-License-Identifier: CC0-1.0
"""explore_next_steps: three reads after the Approach strata.  EXPLORATORY.
The holdout was spent at Phase C; nothing here is a test and nothing is
scored.  Every reading printed is DERIVED.

    python3 holdout/explore_next_steps.py coverage SOURCE_CSV
    python3 holdout/explore_next_steps.py power
    python3 holdout/explore_next_steps.py rate SOURCE_CSV

coverage  item 1: AI and MAP ranges, anchor vs holdout, pooled and inside
          each Approach.  Ranges only; no fit is run.
power     item 3 arithmetic: reads the anchor estimates and 80% intervals
          already printed in EXPLORE_DENOMINATOR_GROUPS.md section 12 and
          scales the interval width to a holdout n.  No fit is run and no
          data file is opened.
rate      item 3 arithmetic: studies per publication year in the source,
          and their Approach / setting mix, as a base for "expected n".

Mark rule for coverage (hand-set, written before the table was seen):
  narrower  holdout min-max width < NARROW * anchor min-max width
  shifted   more than SHIFT of holdout rows lie outside the anchor min-max
  either -> "possible extrapolation, not reversal"
  neither -> "flip within a shared range"
The same two tests on the central band (10th-90th percentile) are printed
beside the mark and do not change it.
"""
import csv
import hashlib
import io
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_SHA = "bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c"
ANCHOR_SHA = "e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438"
CUTOFF_YEAR = 2018
NARROW = 0.8
SHIFT = 0.10
STRATA = [("pooled", None), ("Self-Other", "Self-Other"), ("Self-Sterilized", "Self-Sterilized")]
COLS = ["AI", "MAP"]


def load(path):
    if hashlib.sha256(open(os.path.join(HERE, "anchor_studies.csv"), "rb").read()).hexdigest() != ANCHOR_SHA:
        raise SystemExit("STOP: anchor_studies.csv sha256 mismatch")
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
        raise SystemExit("STOP: source sha256 mismatch: not run")
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
    return {"anchor": [r for r in rows if int(r["Year"]) <= CUTOFF_YEAR],
            "holdout": [r for r in rows if int(r["Year"]) > CUTOFF_YEAR]}


def quantile(s, q):
    """Linear interpolation on a sorted list (the numpy default)."""
    if not s:
        return None
    h = (len(s) - 1) * q
    lo = int(math.floor(h))
    hi = min(lo + 1, len(s) - 1)
    return s[lo] + (s[hi] - s[lo]) * (h - lo)


def summary(rows, col):
    vals, studies, bad = [], set(), 0
    for r in rows:
        try:
            x = float(r[col])
        except ValueError:
            bad += 1
            continue
        if not math.isfinite(x):
            bad += 1
            continue
        vals.append(x)
        studies.add(r["Author"])
    vals.sort()
    top = max(set(vals), key=vals.count)
    return {"rows": len(vals), "studies": len(studies), "not_recorded": bad, "vals": vals,
            "modal": top, "modal_share": vals.count(top) / len(vals),
            "min": vals[0], "q1": quantile(vals, 0.25), "med": quantile(vals, 0.5),
            "q3": quantile(vals, 0.75), "max": vals[-1],
            "p10": quantile(vals, 0.10), "p90": quantile(vals, 0.90)}


def compare(a, h, lo_key="min", hi_key="max"):
    alo, ahi, hlo, hhi = a[lo_key], a[hi_key], h[lo_key], h[hi_key]
    olo, ohi = max(alo, hlo), min(ahi, hhi)
    ov = max(0.0, ohi - olo)
    outside = sum(1 for x in h["vals"] if x < alo or x > ahi)
    return {"overlap": (olo, ohi) if ohi >= olo else None,
            "overlap_of_anchor": ov / (ahi - alo), "overlap_of_holdout": ov / (hhi - hlo),
            "width_ratio": (hhi - hlo) / (ahi - alo),
            "holdout_rows_outside": outside, "share_outside": outside / h["rows"],
            "narrower": (hhi - hlo) < NARROW * (ahi - alo),
            "shifted": outside / h["rows"] > SHIFT}


def mark(c):
    if c["narrower"] or c["shifted"]:
        why = [k for k in ("narrower", "shifted") if c[k]]
        return "possible extrapolation, not reversal (%s)" % " and ".join(why)
    return "flip within a shared range"


def coverage(path):
    side = load(path)
    print("B1 CLIMATE COVERAGE: ranges only, no refit; spent holdout, scores nothing")
    print("  row-level quantiles; MAP in mm; mark rule: narrower = holdout width < %.1f x anchor width,"
          % NARROW)
    print("  shifted = more than %.0f%% of holdout rows outside the anchor min-max" % (100 * SHIFT))
    marks = []
    for col in COLS:
        fmt = "%8.4f" if col == "AI" else "%8.1f"
        print("  %s" % col)
        print("    stratum          side     studies  rows       min        q1       med        q3       max"
              "       p10       p90")
        res = {}
        for sname, val in STRATA:
            for s in ("anchor", "holdout"):
                rs = [r for r in side[s] if val is None or r["Approach"] == val]
                m = summary(rs, col)
                res[(sname, s)] = m
                print("    %-16s %-7s  %7d %5d  " % (sname if s == "anchor" else "", s, m["studies"], m["rows"])
                      + "  ".join(fmt % m[k] for k in ("min", "q1", "med", "q3", "max", "p10", "p90"))
                      + ("   (%d not recorded)" % m["not_recorded"] if m["not_recorded"] else ""))
        print("    stratum          overlap of ranges        share of     share of     holdout/anchor"
              "   holdout rows outside")
        print("                     (min-max)                anchor rng   holdout rng  width"
              "            the anchor min-max")
        for sname, _ in STRATA:
            a, h = res[(sname, "anchor")], res[(sname, "holdout")]
            c = compare(a, h)
            cc = compare(a, h, "p10", "p90")
            ov = ("[" + (fmt % c["overlap"][0]).strip() + ", " + (fmt % c["overlap"][1]).strip() + "]"
                  if c["overlap"] else "none")
            print("    %-16s %-24s %6.3f       %6.3f       %6.3f           %5d of %5d = %.4f"
                  % (sname, ov, c["overlap_of_anchor"], c["overlap_of_holdout"], c["width_ratio"],
                     c["holdout_rows_outside"], h["rows"], c["share_outside"]))
            marks.append((col, sname, mark(c), cc))
        print("    most common single value (rows are not spread evenly over studies):")
        for sname, _ in STRATA:
            for s in ("anchor", "holdout"):
                m = res[(sname, s)]
                print("      %-16s %-7s  " % (sname, s) + (fmt % m["modal"]).strip()
                      + "  on %.3f of rows" % m["modal_share"])
    print("  READ (DERIVED), by the rule above")
    for col, sname, m, cc in marks:
        print("    B1 %-3s %-16s %s" % (col, sname, m))
    print("  beside the mark, not part of it: the same two tests on the central band (p10-p90)")
    print("    col  stratum          holdout/anchor width   holdout rows outside anchor p10-p90   narrower  shifted")
    for col, sname, m, cc in marks:
        print("    %-3s  %-16s %8.3f               %8.4f                              %-8s  %s"
              % (col, sname, cc["width_ratio"], cc["share_outside"],
                 "yes" if cc["narrower"] else "no", "yes" if cc["shifted"] else "no"))


# ----------------------------------------------------------------- item 3: power
CELL = re.compile(r"^\s+(all rows|Self-Other|Self-Sterilized)?\s+(anchor|holdout)\s+"
                  r"([+-][0-9.]+) \[\s*([+-][0-9.]+),\s*([+-][0-9.]+)\]\s+(\d+) st\s+(\d+) rows")
HEAD = re.compile(r"^\s+(B1 AI|B1 MAP|B2|B3|B4|R5) \(")


def section12():
    """The strata table as printed in EXPLORE_DENOMINATOR_GROUPS.md.  No fit is run."""
    text = open(os.path.join(HERE, "EXPLORE_DENOMINATOR_GROUPS.md"), encoding="ascii").read()
    text = text[text.index("## 12. Approach strata"):]
    out, fid, stratum = {}, None, None
    for line in text.splitlines():
        m = HEAD.match(line)
        if m:
            fid = m.group(1)
            continue
        st = re.match(r"^\s+(all rows|Self-Other|Self-Sterilized)\s", line)
        if st:
            stratum = st.group(1)        # also set by a "not checkable" line, which CELL does not match
        m = CELL.match(line)
        if m and fid:
            stratum = m.group(1) or stratum
            out[(fid, stratum, m.group(2))] = {"est": float(m.group(3)), "lo": float(m.group(4)),
                                               "hi": float(m.group(5)), "studies": int(m.group(6))}
    return out


def power():
    t = section12()
    print("POWER GATE ARITHMETIC: anchor 80% interval scaled to a holdout n; no fit run, no data opened")
    print("  source: the section 12 table in EXPLORE_DENOMINATOR_GROUPS.md, as printed (4 decimals)")
    print("  expected half-width at n studies = anchor half-width * sqrt(anchor studies / n)")
    print("  studies needed = anchor studies * (anchor half-width / |anchor estimate|)^2, rounded up")
    print("  PASS = the expected interval, centred on the anchor estimate, excludes zero")
    print("  id      stratum          anchor est  half-width  anchor st   studies   spent holdout:")
    print("                                                               needed    st   exp. half-width  gate")
    for fid in ("B1 AI", "B1 MAP", "B2", "B3", "B4", "R5"):
        for s in ("Self-Other", "Self-Sterilized"):
            a, h = t.get((fid, s, "anchor")), t.get((fid, s, "holdout"))
            if a is None:
                print("  %-6s  %-16s not checkable on the anchor side (no interval printed)" % (fid, s))
                continue
            hw = (a["hi"] - a["lo"]) / 2.0
            need = int(math.ceil(a["studies"] * (hw / abs(a["est"])) ** 2))
            exp = hw * math.sqrt(a["studies"] / h["studies"])
            print("  %-6s  %-16s %+9.4f   %8.4f   %7d   %7d   %4d   %8.4f         %s"
                  % (fid, s, a["est"], hw, a["studies"], need, h["studies"], exp,
                     "PASS" if exp < abs(a["est"]) else "FAIL"))


def rate(path):
    side = load(path)
    rows = side["anchor"] + side["holdout"]
    by = {}
    for r in rows:
        by.setdefault(int(r["Year"]), {}).setdefault(r["Author"], []).append(r)
    print("PUBLICATION RATE in the source (studies = distinct Author values)")
    print("  year   studies   rows   Self-Other st   Self-Sterilized st   Greenhouse st   Field st")
    for y in sorted(by)[-8:]:
        st = by[y]

        def n(col, val):
            return sum(1 for rs in st.values() if any(r[col] == val for r in rs))
        print("  %d   %7d  %5d   %13d   %18d   %13d   %8d"
              % (y, len(st), sum(len(v) for v in st.values()), n("Approach", "Self-Other"),
                 n("Approach", "Self-Sterilized"), n("Experimental.setting", "Greenhouse"),
                 n("Experimental.setting", "Field")))
    last = max(by)
    full = [y for y in sorted(by) if 2017 <= y < last]
    counts = sorted(len(by[y]) for y in full)
    print("  last year in the source: %d (%d studies; read as a partial year)" % (last, len(by[last])))
    print("  full years %d-%d: %d to %d studies per year, median %.1f"
          % (full[0], full[-1], counts[0], counts[-1], quantile(counts, 0.5)))


def main():
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "coverage":
        return coverage(a[1])
    if a == ["power"]:
        return power()
    if len(a) == 2 and a[0] == "rate":
        return rate(a[1])
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
