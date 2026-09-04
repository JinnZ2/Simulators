#!/usr/bin/env python3
"""gap_audit -- the delivered GAP document read as a structure.

`GAP.md` names seven gaps in how claim refusal is measured, five
experiment designs, and a standing shape. This module reads the
delivered text and computes what its prose asserts, from the figures
the document itself carries:

  0. the anchor's two-arm contrast, with the tilde on one baseline
     carried as a range rather than dropped;
  1. G-1..G-7 parsed, each with its Missing line, and E-1..E-5 mapped
     to the gaps they name -- which gaps have no design;
  2. G-2's estimator as arithmetic: displacement of d claimants moves
     UM/BI to (U+d)/(B-d), and the reading is one number for two causes;
     the ratio's log-derivative shows what "rose anyway" requires;
  3. G-3's rebase table recomputed; the mean seam; 2023 restated;
  4. G-4's litigation move against the CWP move, and the bound on the
     netted move;
  5. G-5's volume factor: total wrongful refusals under the two readings
     E-1 discriminates, and the factor between them;
  6. G-6's estimator at the pre-instrument point: 0/0 is None, not zero;
  7. each gap against the register's eight mechanisms, by import, as
     declared readings with the nearest named where none fits;
  8. sources: named in prose, zero URLs.

Every figure is carried from the document and is not checked against
any source (allowlist egress; none reachable). Nothing here is a
statement about any carrier, line, state or claimant.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "uninstrumented"))
import uninstrumented as UN  # noqa: E402  (imported, not copied)

DOC = os.path.join(HERE, "GAP.md")


def _read(p=DOC):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------ 0. anchor

def anchor(text):
    """The two-arm table. A tilde on a value is read as a +/- band
    [CHOICE 1]; the band width is declared and printed."""
    rows = re.findall(r"^\| (auto [^|]+?) \| (~?\d+)% \| (~?\d+)% \|$", text, re.M)
    return [{"line": a.strip(), "y2016": b, "y2025": c} for a, b, c in rows]


TILDE_BAND = 2.0   # [CHOICE 1] percentage points either side of a ~ value


def _val(s):
    return float(s.lstrip("~")), s.startswith("~")


def two_arm(rows, band=TILDE_BAND):
    out = []
    for r in rows:
        a, ta = _val(r["y2016"])
        b, tb = _val(r["y2025"])
        lo = (b - (band if tb else 0)) - (a + (band if ta else 0))
        hi = (b + (band if tb else 0)) - (a - (band if ta else 0))
        out.append({"line": r["line"], "delta_point": b - a, "delta_range": (lo, hi)})
    treated, control = out[0], out[1]
    return {"arms": out,
            "difference_point": treated["delta_point"] - control["delta_point"],
            "difference_range": (treated["delta_range"][0] - control["delta_range"][1],
                                 treated["delta_range"][1] - control["delta_range"][0])}


# ------------------------------------------------------------ 1. gaps / designs

def gaps(text):
    out = {}
    for m in re.finditer(r"^### (G-\d)\s+(?:\[PRIMARY\]\s+)?(.+?)\n(.*?)(?=^### |^---|\Z)", text, re.S | re.M):
        body = m.group(3)
        miss = re.search(r"\*\*Missing:\*\*\s*(.+?)(?=\n\*\*|\n\n|\Z)", body, re.S)
        out[m.group(1)] = {"title": m.group(2).strip(),
                           "missing": " ".join(miss.group(1).split()) if miss else None,
                           "primary": "[PRIMARY]" in m.group(0)}
    return out


def designs(text):
    out = {}
    for m in re.finditer(r"^### (E-\d) \((closes|bounds) (G-\d)[^)]*\) (.+?)$", text, re.M):
        out[m.group(1)] = {"relation": m.group(2), "gap": m.group(3), "title": m.group(4).strip()}
    return out


def gap_coverage(text):
    g, d = gaps(text), designs(text)
    covered = {v["gap"]: (k, v["relation"]) for k, v in d.items()}
    return {gid: covered.get(gid) for gid in g}


# ------------------------------------------------------------ 2. G-2 estimator

def um_rate(um, bi):
    """UM claim frequency over BI claim frequency; None when BI is 0,
    which is the G-6 point: 0/0 is not a reading."""
    return None if bi == 0 else um / bi


def displacement(um, bi, d):
    """d claimants refused on BI who file on UM: (U+d)/(B-d)."""
    return um_rate(um + d, bi - d)


def same_reading_two_causes(um, bi, d):
    """A non-purchase world with the same ratio as the displacement
    world: U' = U + d, B' = B - d -- i.e. the two worlds are the same
    numbers. Returns the ratio and the fact that the pair (U', B')
    carries no cause label."""
    r = displacement(um, bi, d)
    return {"ratio": r, "displacement_world": (um + d, bi - d),
            "non_purchase_world": (um + d, bi - d), "distinguishable_from_ratio": False}


def rose_anyway(bi_growth, ratio_growth):
    """d ln(U/B) = d ln U - d ln B. If BI grew by g_B and the ratio still
    grew by g_R, UM grew by (1+g_R)(1+g_B) - 1."""
    return (1 + ratio_growth) * (1 + bi_growth) - 1


# ------------------------------------------------------------ 3. G-3 rebase

def rebase_table(text):
    rows = re.findall(r"^\| (\d{4}) \| ([\d.]+) \| ([\d.]+) \| (-?[\d.]+) \|$", text, re.M)
    out = []
    for y, old, new, d in rows:
        old, new, d = float(old), float(new), float(d)
        out.append({"year": int(y), "older": old, "newer": new, "stated_delta": d,
                    "computed_delta": round(new - old, 1), "match": abs((new - old) - d) < 1e-9})
    return out


def rebase_summary(text):
    t = rebase_table(text)
    seam = sum(r["older"] - r["newer"] for r in t) / len(t)
    m1993 = re.search(r"1993 \(([\d.]+)%\)", text)
    m2023 = re.search(r"2023 \(([\d.]+)%\)", text)
    v1993, v2023 = float(m1993.group(1)), float(m2023.group(1))
    return {"rows": t, "all_match": all(r["match"] for r in t), "mean_seam": round(seam, 2),
            "v1993": v1993, "v2023_newer": v2023, "v2023_restated": round(v2023 + seam, 1),
            "record_on_newer_basis": v2023 > v1993, "record_on_restated": v2023 + seam > v1993}


# ------------------------------------------------------------ 4. G-4 litigation

def litigation(text):
    m = re.search(r"Litigation rose (\d+)% -> (\d+)% of claimants \([\d-]+\) against a ~(\d+) point", text)
    a, b, cwp = (int(x) for x in m.groups())
    lit = b - a
    return {"litigation_move": lit, "cwp_move": cwp, "ratio": round(lit / cwp, 2),
            "netted_move_bounds": (cwp - lit, cwp),
            "reading": "if every added lawsuit were a re-routed payment the netted CWP move is %d; "
                       "if none, %d; E-3 is the share between" % (cwp - lit, cwp)}


# ------------------------------------------------------------ 5. G-5 volume

def wrongful_total(n_refusals, appeal_rate, overturn_appealed, overturn_unappealed):
    """Wrongful refusals in a population: appealed ones overturned plus
    unappealed ones that a blind audit would overturn. None if the
    unappealed rate is None -- which is the delivered state."""
    if overturn_unappealed is None:
        return None
    a = n_refusals * appeal_rate
    return a * overturn_appealed + (n_refusals - a) * overturn_unappealed


def g5_factor(appeal_rate, overturn):
    """E-1's two readings: selective on merit (unappealed rate 0) and
    capacity (rates converge). The factor between them is 1/appeal_rate."""
    n = 10000.0
    merit = wrongful_total(n, appeal_rate, overturn, 0.0)
    capacity = wrongful_total(n, appeal_rate, overturn, overturn)
    return {"published_only": merit / n, "if_converged": capacity / n,
            "factor": capacity / merit, "one_over_appeal_rate": 1 / appeal_rate}


def g5_figures(text):
    m = re.search(r"NY trend \| (\d+)% \((\d{4})\) -> ([\d.]+)% \((\d{4})\)", text)
    return {"overturn_2019": float(m.group(1)), "overturn_2025": float(m.group(3)),
            "appeal_rate_stated": "under 1%"}


# ------------------------------------------------- 7. mechanisms, by import

MECHANISM_MAP = {
    "G-1": ("SCALAR_DEMAND", "partial", "1P and 3P collapsed to one CWP; the components can move apart under one number -- also category-weld's mechanism 9"),
    "G-2": (None, "none", "two causes welded into one ratio; nearest is category-weld's CATEGORY WELD (mechanism 9), not one of the eight"),
    "G-3": ("AUTHORED_REFERENCE", "partial", "the series is rebased by the party publishing it, with no note; the register's sense is a reference produced by the measured party"),
    "G-4": ("BUDGET_BOUNDARY", "fit", "payment through suit sits outside the field the rate is computed in"),
    "G-5": (None, "none", "measured only where contested: a sample selected on the variable -- the standing shape, not one of the eight; nearest AUDIT_ASYMMETRY"),
    "G-6": (None, "none", "no reading at the pre-instrument point; 0/0 is not a value -- an absent state, not an exclusion"),
    "G-7": ("AUDIT_ASYMMETRY", "fit", "driver noncompliance counted and enforced, carrier wrongful refusal not; the guard fires on one side"),
}


def mechanism_map():
    return {g: {"mechanism": m, "fit": fit, "why": why, "in_register": (m in UN.MECHANISMS) if m else False}
            for g, (m, fit, why) in MECHANISM_MAP.items()}


# ------------------------------------------------------------ 8. sources

NAMED_SOURCES = ("WSJ", "NAIC", "California DOI", "NY external review", "ACA",
                 "Medicare Advantage", "WI Safety Responsibility Law")


def sources(text):
    return {"urls": len(re.findall(r"https?://\S+", text)),
            "named": [s for s in NAMED_SOURCES if s in text]}


# ---------------------------------------------------------------- render

def _f(x):
    return "--" if x is None else ("%.3f" % x if isinstance(x, float) else str(x))


def render():
    text = _read()
    out = []
    w = out.append
    w("gap_audit -- GAP.md read as a structure")
    w("")
    w("[CHOICE 1] a ~ on a value is read as +/- %.0f points" % TILDE_BAND)
    w("")
    ta = two_arm(anchor(text))
    w("0. ANCHOR  two arms, 2016 -> 2025")
    for a in ta["arms"]:
        w("   %-50s delta %+.0f  (range %+.0f..%+.0f)" % (a["line"][:50], a["delta_point"], *a["delta_range"]))
    w("   difference of deltas %+.0f, range %+.0f..%+.0f: the held-constant design's residual" % (
        ta["difference_point"], *ta["difference_range"]))
    w("   the +10 is 45 minus a ~35; the tilde is on the baseline, so the residual is a band.")
    w("")
    g = gaps(text)
    cov = gap_coverage(text)
    w("1. GAPS %d, DESIGNS %d" % (len(g), len(designs(text))))
    for gid, info in g.items():
        c = cov[gid]
        w("   %s %-58s %s" % (gid, info["title"][:58], ("%s (%s)" % c) if c else "NO DESIGN"))
    nodesign = [gid for gid, c in cov.items() if c is None]
    w("   gaps with no design: %s -- G-6 declares nothing recoverable; G-7 does not" % nodesign)
    w("")
    ex = same_reading_two_causes(100, 1000, 50)
    w("2. G-2  U=100, B=1000: rate %.3f; displace 50 -> (150, 950) rate %.3f" % (um_rate(100, 1000), ex["ratio"]))
    w("   a non-purchase world with 150 UM and 950 BI claims is the same pair; distinguishable from the ratio: %s" % ex["distinguishable_from_ratio"])
    w("   'BI rose, ratio rose anyway': d ln(U/B) = d ln U - d ln B; with BI +10%% and ratio +10%%, UM grew %.1f%%" % (100 * rose_anyway(0.10, 0.10)))
    w("")
    rb = rebase_summary(text)
    w("3. G-3  four rows, stated deltas reproduce: %s; mean seam %.2f" % (rb["all_match"], rb["mean_seam"]))
    w("   1993 %.1f vs 2023 %.1f (newer basis): record on newer basis %s; restated 2023 %.1f: record %s" % (
        rb["v1993"], rb["v2023_newer"], rb["record_on_newer_basis"], rb["v2023_restated"], rb["record_on_restated"]))
    w("   both readings live, as the document says; the seam decides which.")
    w("")
    li = litigation(text)
    w("4. G-4  litigation move %+d points against a CWP move of %+d: ratio %.2f" % (li["litigation_move"], li["cwp_move"], li["ratio"]))
    w("   %s" % li["reading"])
    w("")
    f5 = g5_figures(text)
    fac = g5_factor(0.01, 0.467)
    w("5. G-5  appeal rate %s; at 1%% and overturn 0.467: wrongful share published %.4f, if converged %.3f, factor %.0f = 1/appeal rate %.0f" % (
        f5["appeal_rate_stated"], fac["published_only"], fac["if_converged"], fac["factor"], fac["one_over_appeal_rate"]))
    w("   the ~100x in E-1 is 1/appeal_rate exactly; the unappealed rate is None until E-1 runs: %s" % _f(wrongful_total(1, 0.01, 0.467, None)))
    w("   overturn %.1f -> %.1f with appeal rate flat: the document reads it one way; a review standard" % (f5["overturn_2019"], f5["overturn_2025"]))
    w("   that moved is a second reading, and E-1's blind reviewers on policy language are what separate them.")
    w("")
    w("6. G-6  UM rate at (0, 0): %s -- not zero; the instrument has no reading before it is installed" % _f(um_rate(0, 0)))
    w("")
    w("7. MECHANISMS  register carries %d; declared readings:" % len(UN.MECHANISMS))
    for gid, m in mechanism_map().items():
        w("   %s %-19s %-8s in register %-5s %s" % (gid, m["mechanism"] or "--", m["fit"], m["in_register"], m["why"]))
    w("")
    s = sources(text)
    w("8. SOURCES  URLs %d; named in prose: %s" % (s["urls"], ", ".join(s["named"])))
    w("   every figure is carried from the document; none was checked against a source.")
    w("")
    w("Nothing here is a statement about any carrier, line, state or claimant.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("gap_audit.py has no checks of its own; they live in selftest_crg.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
