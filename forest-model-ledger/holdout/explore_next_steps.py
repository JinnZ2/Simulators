# SPDX-License-Identifier: CC0-1.0
"""explore_next_steps: three reads after the Approach strata.  EXPLORATORY.
The holdout was spent at Phase C; nothing here is a test and nothing is
scored.  Every reading printed is DERIVED.

    python3 holdout/explore_next_steps.py coverage SOURCE_CSV
    python3 holdout/explore_next_steps.py power
    python3 holdout/explore_next_steps.py rate SOURCE_CSV
    python3 holdout/explore_next_steps.py loso SOURCE_CSV
    python3 holdout/explore_next_steps.py share SOURCE_CSV
    python3 holdout/explore_next_steps.py myc SOURCE_CSV FUNGALROOT_JSONL
    python3 holdout/explore_next_steps.py f2 SOURCE_CSV FUNGALROOT_JSONL
    python3 holdout/explore_next_steps.py f3 SOURCE_CSV FUNGALROOT_JSONL
    python3 holdout/explore_next_steps.py f4 SOURCE_CSV FUNGALROOT_JSONL

coverage  item 1: AI and MAP ranges, anchor vs holdout, pooled and inside
          each Approach.  Ranges only; no fit is run.
power     item 3 arithmetic: reads the anchor estimates and 80% intervals
          already printed in EXPLORE_DENOMINATOR_GROUPS.md section 12 and
          scales the interval width to a holdout n.  No fit is run and no
          data file is opened.
rate      item 3 arithmetic: studies per publication year in the source,
          and their Approach / setting mix, as a base for "expected n".
loso      follow-up item 1: holdout B1 (AI, MAP) refit with each holdout
          study removed in turn, pooled and inside each Approach.  The fit
          is phase_b.fit through phase_c.FITS, imported and unchanged
          (needs numpy).  Mark rule, written before the table was seen:
          if the slope with the dominant site removed has the anchor's
          sign -> "flip carried by one site"; else "flip not carried by
          that site".  Dominant site = the rows at the most common
          (AI, MAP) pair on the holdout side.
share     the largest single study's share of rows beside each of the six
          Phase B fits, per side and stratum.  Counts only; no fit.
myc       follow-up item 2: mycorrhizal type joined from FungalRoot
          occurrence records (GBIF dataset 744edc21-8dd2-474e-8a0b-
          b8c3d56a3c2d, fetched through the GBIF occurrence API; sha256 of
          the fetched file asserted).  No type is filled from recall: a
          taxon with no record reads NOT RECORDED.
          record -> type set (the source's own "Mycorrhiza type" values):
            AM -> AM ; "EcM, AM undetermined", "EcM, no AM colonization"
            -> ECM ; "EcM,AM" -> AM and ECM ; non-mycorrhizal -> NM ;
            ErM, OM, Other -> OTHER (the order's list has no slot for
            them; kept apart, never folded into NM or NOT RECORDED) ;
            "non-ectomycorrhizal (AM undetermined)" says nothing about
            the four classes and is not counted.
          taxon rule (hand-set): a type counts for a taxon when it is on
          at least MYC_MIN of the taxon's counted records.  AM and ECM
          both count -> AM+ECM ; else AM ; else ECM ; else NM ; else
          OTHER.
          join: Species string against the source's interpreted species
          name, then its verbatim name (level "species"); then Genus
          against all of the genus's records (level "genus"; the source
          holds records, not a genus table, so a genus type here is an
          aggregate of records and is tagged as such).
          B4 with myc_type: phase_b.fit and phase_b.dummy, imported and
          unchanged, one two-level contrast at a time (the fit takes one
          moderator).  Species test: missing_column_finder.analyse,
          unchanged, with five myc dummy columns added in memory (AM is
          the reference; NOT RECORDED is its own column so the row set is
          the same before and after).
f2        order 335-F2, on the same join: (1) ECM - AM inside Woody rows
          only; (2) leave-one-study-out on ECM - AM (Self-Other) and
          NM - AM (both strata); (3) the taxon rule at MYC_MIN 0.1 / 0.2 /
          0.3; (4) the Phase C fit-rule columns for every myc contrast,
          read against the ANCHOR fit (nothing here was sealed).  Thin =
          under F2_THIN studies on either level of the contrast.
f3        order 335-F3: (2) leave-one-SITE-out, site = the dataset's
          (Latitude, Longitude) pair, its only location field (the README
          does not say what the pair locates: coordinate_meaning is an
          empty slot); (3) four counts and two restricted fits beside the
          ECM - AM Self-Other size gap.  Nothing is read as cause.
f4        order 335-F4: ECM - AM inside Self-Other, HOLDOUT only, split by
          Experimental.setting and by Phase2.time (<= 12 / > 12 months).
          Thin = under F2_THIN ECM studies in the cell.  The anchor cells
          are printed as counts only, to show why it cannot be split.

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


def _fits():
    sys.path.insert(0, HERE)
    sys.path.insert(0, os.path.dirname(HERE))
    import warnings
    import phase_b
    import phase_c

    def est(rows, xfun, yfun):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            f = phase_b.fit(rows, xfun, yfun=yfun)
        return f["estimate"], f["interval80"], f["n_studies"], f["n_rows"]
    return phase_c.FITS, est


def loso(path):
    side = load(path)
    fits, est = _fits()
    hold = side["holdout"]
    pairs = {}
    for r in hold:
        pairs[(r["AI"], r["MAP"])] = pairs.get((r["AI"], r["MAP"]), 0) + 1
    dom = max(pairs, key=pairs.get)
    owners = {}
    for r in hold:
        if (r["AI"], r["MAP"]) == dom:
            owners[r["Author"]] = owners.get(r["Author"], 0) + 1
    print("LEAVE-ONE-STUDY-OUT, holdout B1: phase_b.fit (imported, unchanged); spent holdout, scores nothing")
    print("  dominant site: AI %s, MAP %s; %d of %d holdout rows; studies with rows there: %s"
          % (dom[0], dom[1], pairs[dom], len(hold),
             "; ".join("%s (%d rows)" % (k.encode("ascii", "replace").decode(), v)
                       for k, v in sorted(owners.items(), key=lambda kv: -kv[1]))))
    print("  id      stratum          anchor     holdout    LOSO slope range        signs   site removed"
          "                 studies  rows   mark")
    print("                           slope      slope      min        max        -  +    slope [80% interval]")
    detail = []
    for fid, pid, col, xfun, yfun in fits:
        if pid != "B1":
            continue
        for sname, val in STRATA:
            a_rows = [r for r in side["anchor"] if val is None or r["Approach"] == val]
            h_rows = [r for r in hold if val is None or r["Approach"] == val]
            a_est = est(a_rows, xfun, yfun)[0]
            h_est = est(h_rows, xfun, yfun)[0]
            res = []
            for st in sorted({r["Author"] for r in h_rows}):
                e = est([r for r in h_rows if r["Author"] != st], xfun, yfun)[0]
                res.append((e, st, sum(1 for r in h_rows if r["Author"] == st)))
            res.sort()
            neg = sum(1 for e, _, _ in res if e < 0)
            d_est, (dlo, dhi), dn, dr = est([r for r in h_rows if (r["AI"], r["MAP"]) != dom], xfun, yfun)
            same = (d_est < 0) == (a_est < 0)
            print("  %-6s  %-16s %+8.4f   %+8.4f   %+8.4f   %+8.4f   %2d %2d   %+8.4f [%+8.4f, %+8.4f]   %4d  %5d   %s"
                  % (fid, sname, a_est, h_est, res[0][0], res[-1][0], neg, len(res) - neg, d_est, dlo, dhi,
                     dn, dr, "flip carried by one site" if same else "flip not carried by that site"))
            detail.append((fid, sname, res[0], res[-1]))
    print("  the single removals that move the slope most:")
    for fid, sname, lo, hi in detail:
        print("    %-6s %-16s lowest %+8.4f without %s (%d rows); highest %+8.4f without %s (%d rows)"
              % (fid, sname, lo[0], lo[1].encode("ascii", "replace").decode(), lo[2],
                 hi[0], hi[1].encode("ascii", "replace").decode(), hi[2]))


def share(path):
    side = load(path)
    fits, _ = _fits()
    print("LARGEST SINGLE STUDY'S SHARE OF ROWS beside each Phase B fit (rows the fit can use); counts only")
    print("  id      stratum          anchor: share  rows   studies     holdout: share  rows   studies")
    for fid, pid, col, xfun, yfun in fits:
        for sname, val in STRATA:
            cells = []
            for s in ("anchor", "holdout"):
                by = {}
                for r in side[s]:
                    if val is not None and r["Approach"] != val:
                        continue
                    try:
                        if xfun(r) is None:
                            continue
                        yfun(r)
                    except ValueError:
                        continue
                    by[r["Author"]] = by.get(r["Author"], 0) + 1
                n = sum(by.values())
                cells.append((max(by.values()) / n, n, len(by)))
            print("  %-6s  %-16s        %.3f  %5d   %5d              %.3f  %5d   %5d"
                  % ((fid, sname) + cells[0] + cells[1]))


FUNGALROOT_SHA = "430ab42cadb7412deeb7fa9f81ae8e0cb8f9c8c60bba23bc5c125b8834410980"
MYC_MIN = 0.2
MYC_MAP = {"AM": {"AM"}, "EcM, AM undetermined": {"ECM"}, "EcM, no AM colonization": {"ECM"},
           "EcM,AM": {"AM", "ECM"}, "non-mycorrhizal": {"NM"}, "ErM": {"OTHER"}, "OM": {"OTHER"},
           "Other": {"OTHER"}, "ErM,EcM": {"OTHER", "ECM"}, "ErM,AM": {"OTHER", "AM"},
           "non-ectomycorrhizal (AM undetermined)": set()}
NR = "NOT RECORDED"
MYC_LEVELS = ["AM", "ECM", "AM+ECM", "NM", "OTHER", NR]
THIN = 5


def _norm(name):
    return " ".join((name or "").lower().split())


def _taxon_type(counts):
    n = counts.get("_n", 0)
    if not n:
        return None
    on = {t for t in ("AM", "ECM", "NM", "OTHER") if counts.get(t, 0) / n >= MYC_MIN}
    if "AM" in on and "ECM" in on:
        return "AM+ECM"
    for t in ("AM", "ECM", "NM", "OTHER"):
        if t in on:
            return t
    return None


def fungalroot(path):
    import json
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest() != FUNGALROOT_SHA:
        raise SystemExit("STOP: FungalRoot file sha256 mismatch: not run")
    sp, ge, unknown, n = {}, {}, {}, 0
    for line in raw.decode("ascii").splitlines():
        d = json.loads(line)
        n += 1
        types = set()
        counted = False
        for k, v in d["mof"]:
            if k != "Mycorrhiza type":
                continue
            if v not in MYC_MAP:
                unknown[v] = unknown.get(v, 0) + 1
                continue
            if MYC_MAP[v]:
                counted = True
                types |= MYC_MAP[v]
        if not counted:
            continue
        verb = " ".join((d.get("scientificName") or "").split()[:2])
        for name in {_norm(d.get("species")), _norm(verb)} - {""}:
            c = sp.setdefault(name, {})
            c["_n"] = c.get("_n", 0) + 1
            for t in types:
                c[t] = c.get(t, 0) + 1
        g = _norm(d.get("genus")) or _norm(verb.split()[0] if verb else "")
        if g:
            c = ge.setdefault(g, {})
            c["_n"] = c.get("_n", 0) + 1
            for t in types:
                c[t] = c.get(t, 0) + 1
    return sp, ge, unknown, n, len(raw)


def myc(path, frpath):
    side = load(path)
    sp, ge, unknown, nrec, nbytes = fungalroot(frpath)
    fits, est = _fits()
    import phase_b
    print("MYCORRHIZAL-TYPE JOIN: FungalRoot occurrence records; spent holdout, scores nothing")
    print("  source file: %d records, %d bytes, sha256 asserted; species names with a counted type: %d; genera: %d"
          % (nrec, nbytes, len(sp), len(ge)))
    print("  source type values outside the declared map (not counted): %s"
          % (", ".join("%s x%d" % kv for kv in sorted(unknown.items())) or "none"))
    for s in ("anchor", "holdout"):
        for r in side[s]:
            t = _taxon_type(sp.get(_norm(r["Species"]), {}))
            lvl = "species"
            if t is None:
                t = _taxon_type(ge.get(_norm(r["Genus"]), {}))
                lvl = "genus"
            if t is None:
                t, lvl = NR, "none"
            r["myc_type"], r["myc_level"] = t, lvl
    print("  MATCH RATE (no fill: unmatched = NOT RECORDED, kept)")
    print("    side     unit      total   species-level   genus-level   NOT RECORDED   matched share")
    for s in ("anchor", "holdout"):
        rows = side[s]
        for unit, items in (("rows", [(r["myc_level"],) for r in rows]),
                            ("species", [(lv,) for lv in {r["Species"]: r["myc_level"] for r in rows}.values()])):
            c = {}
            for (lv,) in items:
                c[lv] = c.get(lv, 0) + 1
            tot = len(items)
            print("    %-7s  %-8s %6d   %13d   %11d   %12d   %.3f"
                  % (s, unit, tot, c.get("species", 0), c.get("genus", 0), c.get("none", 0),
                     (tot - c.get("none", 0)) / tot))
    print("  TYPE COUNTS: rows / studies")
    print("    side     stratum          " + "".join("%-14s" % lv for lv in MYC_LEVELS))
    for s in ("anchor", "holdout"):
        for sname, val in STRATA:
            rows = [r for r in side[s] if val is None or r["Approach"] == val]
            cells = []
            for lv in MYC_LEVELS:
                rr = [r for r in rows if r["myc_type"] == lv]
                cells.append("%d / %d" % (len(rr), len({r["Author"] for r in rr})))
            print("    %-7s  %-16s " % (s, sname) + "".join("%-14s" % c for c in cells))

    print("  LIFE FORM AGAINST TYPE: rows that are Woody / all rows of the type")
    for s in ("anchor", "holdout"):
        cells = []
        for lv in MYC_LEVELS:
            rr_ = [r for r in side[s] if r["myc_type"] == lv]
            cells.append("%d / %d" % (sum(1 for r in rr_ if r["Life.form"] == "Woody"), len(rr_)))
        print("    %-7s  %-16s " % (s, "pooled") + "".join("%-14s" % c for c in cells))
    print("  B4 RERUN: myc_type in place of Life.form; phase_b.fit unchanged; one contrast at a time")
    print("    cell = estimate [80%% interval] studies rows ; thin = under %d studies on either level" % THIN)
    contrasts = [("Life.form Woody - Nonwoody (as sealed)", lambda r: phase_b.dummy("Life.form", "Woody", "Nonwoody")(r)),
                 ("ECM - AM", phase_b.dummy("myc_type", "ECM", "AM")),
                 ("AM+ECM - AM", phase_b.dummy("myc_type", "AM+ECM", "AM")),
                 ("NM - AM", phase_b.dummy("myc_type", "NM", "AM")),
                 ("any ECM - AM", lambda r: 1.0 if r["myc_type"] in ("ECM", "AM+ECM")
                  else (0.0 if r["myc_type"] == "AM" else None))]
    rr = lambda r: float(r["rr"])  # noqa: E731
    for cname, xfun in contrasts:
        print("    %s" % cname)
        for sname, val in STRATA[1:]:
            for s in ("anchor", "holdout"):
                rows = [r for r in side[s] if r["Approach"] == val]
                st = {0.0: set(), 1.0: set()}
                for r in rows:
                    x = xfun(r)
                    if x is not None:
                        st[x].add(r["Author"])
                head = "      %-16s %-7s " % (sname if s == "anchor" else "", s)
                if not st[0.0] or not st[1.0]:
                    print(head + "not checkable (one level absent: %d / %d studies)" % (len(st[1.0]), len(st[0.0])))
                    continue
                try:
                    e, (lo, hi), ns, nr = est(rows, xfun, rr)
                    if not all(v == v for v in (e, lo, hi)):
                        raise ValueError
                except Exception:
                    print(head + "not checkable (fit did not return)")
                    continue
                print(head + "%+8.4f [%+8.4f, %+8.4f] %3d st %5d rows   level studies %d / %d%s"
                      % (e, lo, hi, ns, nr, len(st[1.0]), len(st[0.0]),
                         "  thin" if min(len(st[0.0]), len(st[1.0])) < THIN else ""))

    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ledger", "toolkit"))
    import missing_column_finder as mcf
    dums = ["myc_ECM", "myc_AMECM", "myc_NM", "myc_OTHER", "myc_NR"]
    lv_of = dict(zip(dums, ["ECM", "AM+ECM", "NM", "OTHER", NR]))
    for s in ("anchor", "holdout"):
        for r in side[s]:
            for dname in dums:
                r[dname] = "yes" if r["myc_type"] == lv_of[dname] else "no"
    print("  SPECIES TEST: missing_column_finder.analyse (unchanged), before and after 5 myc columns are added")
    print("    share = Species share of the spread left after the columns ; excess = share minus null mean")
    print("    stratum          side     columns   left     between-study: share  excess  flag   "
          "within-study: share  excess  flag")
    saved = (list(mcf.COLUMNS), dict(mcf.BINARY))
    drops = []
    try:
        for sname, val in STRATA[1:]:
            for s, rows in (("anchor", side["anchor"]), ("holdout", side["holdout"]),
                            ("pooled", side["anchor"] + side["holdout"])):
                rows = [r for r in rows if r["Approach"] == val]
                got = {}
                for tag in ("before", "after"):
                    mcf.COLUMNS[:] = saved[0] + (dums if tag == "after" else [])
                    mcf.BINARY.clear()
                    mcf.BINARY.update(saved[1])
                    if tag == "after":
                        mcf.BINARY.update({dname: ("yes", "no") for dname in dums})
                    import warnings
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        o = mcf.analyse(rows)
                    g = o["groupings"]["Species"]
                    got[tag] = g

                    def cell(v):
                        if not isinstance(v, dict):
                            return "%-28s" % "not checkable"
                        return "%6.3f  %+6.3f  %-4s        " % (v["share"], v["excess"], "FLAG" if v["flag"] else "-")
                    print("    %-16s %-7s  %-7s   %.4f                  %s %s"
                          % (sname if (s == "anchor" and tag == "before") else "", s if tag == "before" else "",
                             "%d %s" % (len(o["together"]["columns_used"]), tag[:3]), o["together"]["left"],
                             cell(g["between_study"]), cell(g["within_study"])))
                for k in ("between_study", "within_study"):
                    b, a_ = got["before"][k], got["after"][k]
                    if isinstance(b, dict) and isinstance(a_, dict):
                        drops.append((sname, s, k, b["share"], a_["share"], b["excess"], a_["excess"]))
    finally:
        mcf.COLUMNS[:] = saved[0]
        mcf.BINARY.clear()
        mcf.BINARY.update(saved[1])
    print("  DOES THE SPECIES SHARE DROP? (after minus before; read on excess against the finder's own"
          " MIN_EXCESS, %.2f)" % mcf.MIN_EXCESS)
    print("    stratum          side     test            share     excess    reading")
    for sname, s, k, b, a_, be, ae in drops:
        print("    %-16s %-7s  %-14s %+8.4f  %+8.4f  %s"
              % (sname, s, k, a_ - b, ae - be,
                 "drops" if ae - be <= -mcf.MIN_EXCESS else
                 ("rises" if ae - be >= mcf.MIN_EXCESS else "no change (under %.2f)" % mcf.MIN_EXCESS)))


F2_THIN = 3
F2_SWEEP = [0.1, 0.2, 0.3]


def _assign(side, sp, ge):
    for s in ("anchor", "holdout"):
        for r in side[s]:
            t = _taxon_type(sp.get(_norm(r["Species"]), {}))
            lvl = "species"
            if t is None:
                t = _taxon_type(ge.get(_norm(r["Genus"]), {}))
                lvl = "genus"
            if t is None:
                t, lvl = NR, "none"
            r["myc_type"], r["myc_level"] = t, lvl


def _contrasts():
    import phase_b
    return [("ECM - AM", phase_b.dummy("myc_type", "ECM", "AM")),
            ("AM+ECM - AM", phase_b.dummy("myc_type", "AM+ECM", "AM")),
            ("NM - AM", phase_b.dummy("myc_type", "NM", "AM")),
            ("any ECM - AM", lambda r: 1.0 if r["myc_type"] in ("ECM", "AM+ECM")
             else (0.0 if r["myc_type"] == "AM" else None))]


def _cell(rows, xfun, est, thin=F2_THIN):
    """One contrast on one row set.  state in ok / thin / not checkable."""
    st = {0.0: set(), 1.0: set()}
    big = {}
    for r in rows:
        x = xfun(r)
        if x is not None:
            st[x].add(r["Author"])
            big[r["Author"]] = big.get(r["Author"], 0) + 1
    c = {"hi_st": len(st[1.0]), "lo_st": len(st[0.0]), "studies": len(big), "rows": sum(big.values()),
         "share": (max(big.values()) / sum(big.values())) if big else None}
    if not st[0.0] or not st[1.0]:
        return dict(c, state="not checkable")
    try:
        e, (lo, hi), ns, nr = est(rows, xfun, lambda r: float(r["rr"]))
        if not all(v == v for v in (e, lo, hi)):
            raise ValueError
    except Exception:
        return dict(c, state="not checkable")
    return dict(c, state="thin" if min(c["hi_st"], c["lo_st"]) < thin else "ok", est=e, lo=lo, hi=hi)


def _txt(c):
    if c["state"] == "not checkable":
        return "not checkable (level studies %d / %d)" % (c["hi_st"], c["lo_st"])
    return "%+8.4f [%+8.4f, %+8.4f] %3d st %5d rows   level studies %d / %d%s" % (
        c["est"], c["lo"], c["hi"], c["studies"], c["rows"], c["hi_st"], c["lo_st"],
        "  thin" if c["state"] == "thin" else "")


def f2(path, frpath):
    side = load(path)
    sp, ge, _unknown, nrec, _nbytes = fungalroot(frpath)
    _fits_, est = _fits()
    _assign(side, sp, ge)
    cons = dict(_contrasts())
    two = STRATA[1:]
    print("ORDER 335-F2 on the FungalRoot join (%d records); exploratory, post-holdout, scores nothing" % nrec)
    print("  cell = estimate [80%% interval] studies rows ; thin = under %d studies on either level" % F2_THIN)

    print("  1 SEPARATION: ECM - AM inside Life.form == Woody only (all-rows cell beside it)")
    for sname, val in two:
        for s in ("anchor", "holdout"):
            rows = [r for r in side[s] if r["Approach"] == val]
            head = "    %-16s %-7s " % (sname if s == "anchor" else "", s)
            print(head + "woody only  " + _txt(_cell([r for r in rows if r["Life.form"] == "Woody"],
                                                     cons["ECM - AM"], est)))
            print("    %-16s %-7s " % ("", "") + "all rows    " + _txt(_cell(rows, cons["ECM - AM"], est)))

    print("  2 LEAVE-ONE-STUDY-OUT (each study in the contrast removed in turn)")
    print("    contrast   stratum          side     full est   min        max        drops  - / +   sign holds"
          "   largest-study row share")
    for cname, sname in (("ECM - AM", "Self-Other"), ("NM - AM", "Self-Other"), ("NM - AM", "Self-Sterilized")):
        xfun = cons[cname]
        for s in ("anchor", "holdout"):
            rows = [r for r in side[s] if r["Approach"] == sname]
            full = _cell(rows, xfun, est)
            if full["state"] == "not checkable":
                print("    %-9s  %-16s %-7s  not checkable" % (cname, sname, s))
                continue
            res, nc = [], 0
            for stname in sorted({r["Author"] for r in rows if xfun(r) is not None}):
                c = _cell([r for r in rows if r["Author"] != stname], xfun, est)
                if c["state"] == "not checkable":
                    nc += 1
                else:
                    res.append(c["est"])
            neg = sum(1 for e in res if e < 0)
            holds = all((e < 0) == (full["est"] < 0) for e in res)
            print("    %-9s  %-16s %-7s  %+8.4f   %+8.4f   %+8.4f   %3d   %2d / %-3d  %-10s   %.3f%s%s"
                  % (cname, sname, s, full["est"], min(res), max(res), len(res), neg, len(res) - neg,
                     "yes" if holds else "no", full["share"],
                     "  thin" if full["state"] == "thin" else "",
                     "  (%d drops not checkable)" % nc if nc else ""))

    print("  4 FIT-RULE COLUMNS, Phase C definitions, holdout read against the ANCHOR fit (not sealed)")
    print("    direction: read only when the holdout 80% interval excludes zero, else INDETERMINATE")
    print("    interval_hit: holdout estimate inside the anchor interval ; overlap: the two intervals overlap")
    print("    contrast       stratum          anchor dir  holdout dir     direction       interval_hit  overlap")
    for cname, xfun in _contrasts():
        for sname, val in two:
            a = _cell([r for r in side["anchor"] if r["Approach"] == val], xfun, est)
            h = _cell([r for r in side["holdout"] if r["Approach"] == val], xfun, est)
            if "not checkable" in (a["state"], h["state"]):
                print("    %-13s  %-16s not checkable on %s"
                      % (cname, sname, " and ".join(k for k, c in (("anchor", a), ("holdout", h))
                                                    if c["state"] == "not checkable")))
                continue
            adir = "positive" if a["est"] > 0 else "negative"
            hdir = ("positive" if h["est"] > 0 else "negative") if (h["lo"] > 0 or h["hi"] < 0) else "INDETERMINATE"
            print("    %-13s  %-16s %-10s  %-14s  %-14s  %-12s  %s%s"
                  % (cname, sname, adir, hdir,
                     "INDETERMINATE" if hdir == "INDETERMINATE" else ("hit" if hdir == adir else "miss"),
                     "yes" if a["lo"] <= h["est"] <= a["hi"] else "no",
                     "yes" if (h["lo"] <= a["hi"] and a["lo"] <= h["hi"]) else "no",
                     "   thin" if "thin" in (a["state"], h["state"]) else ""))

    print("  3 THRESHOLD SWEEP: taxon rule at MYC_MIN %s (0.2 is the rule used everywhere else)"
          % " / ".join("%.1f" % v for v in F2_SWEEP))
    global MYC_MIN
    keep = MYC_MIN
    try:
        for v in F2_SWEEP:
            MYC_MIN = v
            _assign(side, sp, ge)
            print("    MYC_MIN %.1f" % v)
            print("      side     rows: species  genus  NOT RECORDED    rows by type: "
                  + "  ".join(MYC_LEVELS[:5]))
            for s in ("anchor", "holdout"):
                lv = {}
                ty = {}
                for r in side[s]:
                    lv[r["myc_level"]] = lv.get(r["myc_level"], 0) + 1
                    ty[r["myc_type"]] = ty.get(r["myc_type"], 0) + 1
                print("      %-7s        %6d  %5d  %12d                  %s"
                      % (s, lv.get("species", 0), lv.get("genus", 0), lv.get("none", 0),
                         "  ".join("%d" % ty.get(t, 0) for t in MYC_LEVELS[:5])))
            for s in ("anchor", "holdout"):
                print("      ECM - AM, Self-Other, %-7s %s"
                      % (s, _txt(_cell([r for r in side[s] if r["Approach"] == "Self-Other"],
                                       cons["ECM - AM"], est))))
    finally:
        MYC_MIN = keep


def f3(path, frpath):
    sys.path.insert(0, HERE)
    import phase_c
    side = load(path)
    sp, ge, _unknown, nrec, _nbytes = fungalroot(frpath)
    _fits_, est = _fits()
    _assign(side, sp, ge)
    cons = dict(_contrasts())
    site = lambda r: (r["Latitude"], r["Longitude"])  # noqa: E731
    woody = lambda r: r["Life.form"] == "Woody"  # noqa: E731
    print("ORDER 335-F3 on the FungalRoot join (%d records); exploratory, post-holdout, scores nothing" % nrec)
    print("  2 LEAVE-ONE-SITE-OUT: site = (Latitude, Longitude) pair; each site in the contrast removed in turn")
    for s in ("anchor", "holdout"):
        rs = side[s]
        by_site, by_auth = {}, {}
        for r in rs:
            by_site.setdefault(site(r), set()).add(r["Author"])
            by_auth.setdefault(r["Author"], set()).add(site(r))
        print("    %-7s %d sites, %d studies; sites shared by more than one study: %d; studies with more than one site: %d"
              % (s, len(by_site), len(by_auth), sum(1 for v in by_site.values() if len(v) > 1),
                 sum(1 for v in by_auth.values() if len(v) > 1)))
    print("    contrast   rows        stratum          side     full est   min        max        sites  - / +"
          "   sign holds   largest-site row share")
    cells = [("ECM - AM", "all rows", "Self-Other", None), ("ECM - AM", "woody only", "Self-Other", woody),
             ("NM - AM", "all rows", "Self-Other", None), ("NM - AM", "all rows", "Self-Sterilized", None)]
    for cname, rname, sname, keep in cells:
        xfun = cons[cname]
        for s in ("anchor", "holdout"):
            rows = [r for r in side[s] if r["Approach"] == sname and (keep is None or keep(r))]
            full = _cell(rows, xfun, est)
            if full["state"] == "not checkable":
                print("    %-9s  %-10s  %-16s %-7s  not checkable" % (cname, rname, sname, s))
                continue
            cnt = {}
            for r in rows:
                if xfun(r) is not None:
                    cnt[site(r)] = cnt.get(site(r), 0) + 1
            res, nc = [], 0
            for st in sorted(cnt):
                c = _cell([r for r in rows if site(r) != st], xfun, est)
                if c["state"] == "not checkable":
                    nc += 1
                else:
                    res.append(c["est"])
            neg = sum(1 for e in res if e < 0)
            holds = all((e < 0) == (full["est"] < 0) for e in res)
            print("    %-9s  %-10s  %-16s %-7s  %+8.4f   %+8.4f   %+8.4f   %4d  %3d / %-3d  %-10s   %.3f%s%s"
                  % (cname, rname, sname, s, full["est"], min(res), max(res), len(cnt), neg, len(res) - neg,
                     "yes" if holds else "no", max(cnt.values()) / sum(cnt.values()),
                     "  thin" if full["state"] == "thin" else "",
                     "  (%d drops not checkable)" % nc if nc else ""))

    print("  3 SIZE GAP, ECM - AM inside Self-Other: what differs between the sides (counts and two fits)")
    xfun = cons["ECM - AM"]
    so = {s: [r for r in side[s] if r["Approach"] == "Self-Other" and xfun(r) is not None]
          for s in ("anchor", "holdout")}
    print("    a) rows by match level, per type          ECM: species  genus  genus share     AM: species  genus  genus share")
    for s in ("anchor", "holdout"):
        out = []
        for t in ("ECM", "AM"):
            a_ = sum(1 for r in so[s] if r["myc_type"] == t and r["myc_level"] == "species")
            b_ = sum(1 for r in so[s] if r["myc_type"] == t and r["myc_level"] == "genus")
            out.append("%6d  %5d  %.3f      " % (a_, b_, b_ / (a_ + b_)))
        print("       %-7s                                      %s      %s" % (s, out[0], out[1]))
    print("    b) species-level matches only")
    for s in ("anchor", "holdout"):
        print("       %-7s all levels     %s" % (s, _txt(_cell(so[s], xfun, est))))
        print("       %-7s species only   %s"
              % ("", _txt(_cell([r for r in so[s] if r["myc_level"] == "species"], xfun, est))))
    print("    c) largest study dropped (the same drop as in the 335-F2 leave-one-study-out)")
    for s in ("anchor", "holdout"):
        n = {}
        for r in so[s]:
            n[r["Author"]] = n.get(r["Author"], 0) + 1
        big = max(n, key=n.get)
        ecm = sum(1 for r in so[s] if r["Author"] == big and r["myc_type"] == "ECM")
        print("       %-7s without %s (%d rows, %.3f of the contrast's rows, %d of them ECM)   %s"
              % (s, big.encode("ascii", "replace").decode(), n[big], n[big] / len(so[s]), ecm,
                 _txt(_cell([r for r in so[s] if r["Author"] != big], xfun, est))))
    print("    d) mix, rows / studies")
    for col, levels, lab in (("Experimental.setting", ["Greenhouse", "Field"], None),
                             ("Phase2.time", [b[2] for b in phase_c.TIME_BINS] + [NR], "bin")):
        print("       %-22s %s" % (col, "".join("%-14s" % v for v in levels)))
        for s in ("anchor", "holdout"):
            for t in ("ECM", "AM"):
                rr_ = [r for r in so[s] if r["myc_type"] == t]
                cellz = []
                for v in levels:
                    if lab is None:
                        m = [r for r in rr_ if r[col] == v]
                    else:
                        m = []
                        for r in rr_:
                            try:
                                tt = float(r[col])
                                b = next((n3 for lo, hi, n3 in phase_c.TIME_BINS if lo < tt <= hi), "<= 3 mo")
                            except ValueError:
                                b = NR
                            if b == v:
                                m.append(r)
                    cellz.append("%d / %d" % (len(m), len({r["Author"] for r in m})))
                print("       %-7s %-4s          %s" % (s, t, "".join("%-14s" % c for c in cellz)))


def f4(path, frpath):
    side = load(path)
    sp, ge, _unknown, nrec, _nbytes = fungalroot(frpath)
    _fits_, est = _fits()
    _assign(side, sp, ge)
    xfun = dict(_contrasts())["ECM - AM"]

    def t12(r):
        try:
            return float(r["Phase2.time"]) > 12
        except ValueError:
            return None
    splits = [("a) Experimental.setting", [("Field", lambda r: r["Experimental.setting"] == "Field"),
                                           ("Greenhouse", lambda r: r["Experimental.setting"] == "Greenhouse")]),
              ("b) Phase2.time", [("<= 12 months", lambda r: t12(r) is False),
                                  ("> 12 months", lambda r: t12(r) is True)])]
    print("ORDER 335-F4 on the FungalRoot join (%d records); exploratory, post-holdout, scores nothing" % nrec)
    print("  2 HOLDOUT-INTERNAL SPLIT: ECM - AM inside Self-Other; thin = under %d ECM studies in the cell"
          % F2_THIN)
    print("    split                    cell           side      ECM rows  ECM st   AM rows  AM st   "
          "estimate [80% interval] studies rows")
    for s in ("holdout", "anchor"):
        rows = [r for r in side[s] if r["Approach"] == "Self-Other" and xfun(r) is not None]
        for sname, cells in splits:
            for cname, keep in cells:
                rs = [r for r in rows if keep(r)]
                ecm = [r for r in rs if r["myc_type"] == "ECM"]
                am = [r for r in rs if r["myc_type"] == "AM"]
                head = "    %-24s %-14s %-8s %8d  %6d  %8d  %5d   " % (
                    sname, cname, s, len(ecm), len({r["Author"] for r in ecm}),
                    len(am), len({r["Author"] for r in am}))
                if s == "anchor":
                    print(head + "counts only (anchor not split)")
                    continue
                c = _cell(rs, xfun, est)
                if c["state"] == "not checkable":
                    print(head + "not checkable")
                    continue
                print(head + "%+8.4f [%+8.4f, %+8.4f] %3d st %5d rows%s"
                      % (c["est"], c["lo"], c["hi"], c["studies"], c["rows"],
                         "  thin" if c["hi_st"] < F2_THIN else ""))
        if s == "holdout":
            c = _cell(rows, xfun, est)
            print("    %-24s %-14s %-8s %8d  %6d  %8d  %5d   %+8.4f [%+8.4f, %+8.4f] %3d st %5d rows"
                  % ("unsplit", "all", s, sum(1 for r in rows if r["myc_type"] == "ECM"), c["hi_st"],
                     sum(1 for r in rows if r["myc_type"] == "AM"), c["lo_st"],
                     c["est"], c["lo"], c["hi"], c["studies"], c["rows"]))
            both = {}
            for r in rows:
                if r["myc_type"] == "ECM":
                    k = (r["Experimental.setting"], "> 12" if t12(r) else "<= 12")
                    both.setdefault(k, []).append(r)
            print("    holdout ECM rows by setting x duration (rows / studies): "
                  + "; ".join("%s, %s mo: %d / %d" % (k[0], k[1], len(v), len({r["Author"] for r in v}))
                              for k, v in sorted(both.items())))


def main():
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "f4":
        return f4(a[1], a[2])
    if len(a) == 3 and a[0] == "f3":
        return f3(a[1], a[2])
    if len(a) == 3 and a[0] == "f2":
        return f2(a[1], a[2])
    if len(a) == 3 and a[0] == "myc":
        return myc(a[1], a[2])
    if len(a) == 2 and a[0] == "loso":
        return loso(a[1])
    if len(a) == 2 and a[0] == "share":
        return share(a[1])
    if len(a) == 2 and a[0] == "coverage":
        return coverage(a[1])
    if a == ["power"]:
        return power()
    if len(a) == 2 and a[0] == "rate":
        return rate(a[1])
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
