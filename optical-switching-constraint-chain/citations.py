#!/usr/bin/env python3
"""OSC-WO4: citation sweep of the load-bearing sources in SOURCE_DROP.md.

Each row is one checkable statement the report makes about a source. The
state is DERIVED by tools/check_citations.citation_state (imported, not
copied), never declared:

    VERIFIED     source located and the statement matches it
    CORRECTED    source located and it states something different
    NOT_FOUND    two or more empty searches, or a different object at the id
    UNREACHABLE  source located (or not) but the statement's value is not
                 reachable at the depth searched

Depth is search-result text only. arxiv.org does not resolve from this
environment, so no primary text was read; every VERIFIED here is VERIFIED
at search depth.

    python3 citations.py           the ledger and counts
The module refuses --selftest; checks live in test_citations.py.
"""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
_spec = importlib.util.spec_from_file_location("_check_citations", ROOT / "tools" / "check_citations.py")
_cc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cc)
citation_state = _cc.citation_state
STATES = _cc.STATES

SEARCHED = "2026-10-27"

# reached: Y if the source record was located; queries: searches run;
# exists: Y / N / OTHER; says: MATCH / DIFFERS / None (value not reached).
ROWS = [
    dict(id="C01", cite="Khalid et al. 2026, Nat. Commun., title/date/DOI",
         claim="published 15 Sep 2026, DOI 10.1038/s41467-026-77572-3",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="title 'Optical beam shaping induced reconfigurable magnetic domains'"),
    dict(id="C02", cite="arXiv:1312.7301 (Co nano-squares on Pt)",
         claim="depinning barrier 0.95 +/- 0.2 eV, Delta = 38, nucleus < 37 nm",
         reached="N", queries=2, exists="N", says=None,
         note="two searches, no record with this id or these values; nearest is "
              "Yun et al. 2014, ~1.0e-19 J (0.62 eV) in nanostructured Pt/Co/Pt"),
    dict(id="C03", cite="Vomir et al. 2017, arXiv:1710.10341",
         claim="record exists; single-shot Pt/Co/Pt, sub-micron spot",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="spot 0.8 um, Pt(1.5)/Co(0.7)/Pt(1.5)"),
    dict(id="C04", cite="Vomir et al. 2017 (as cited in sec. 1.2)",
         claim="~1100 K electron temperature at ~7.6 uJ/cm2",
         reached="Y", queries=1, exists="Y", says=None,
         note="value not in search text; a sibling Pt/Co/Pt single-shot paper "
              "(arXiv 2508.05460) works at 4 mJ/cm2"),
    dict(id="C05", cite="Kimel & Li 2019, Nat. Rev. Mater.",
         claim="toggle heat load < 6 J/cm3",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="abstract; origin is the garnet photomagnetic study"),
    dict(id="C06", cite="Kimel & Li 2019, Nat. Rev. Mater.",
         claim="~120 aJ for a 40 x 40 x 20 nm3 cell",
         reached="Y", queries=1, exists="Y", says=None,
         note="no aJ figure in search text; 6 J/cm3 x that cell is 192 aJ (OSC_006)"),
    dict(id="C07", cite="Zhang et al. 2011, FePtAg-C (NTU pdf, JAP 109 07B703)",
         claim="Sharrock barrier E_b = 7.6 eV ~ 300 k_BT",
         reached="Y", queries=1, exists="Y", says=None,
         note="value not in search text; the same group's IEEE TMag 47, 4062 "
              "(2011) reports E_b = 5.1 eV ~ 200 k_BT for FePtAg-C"),
    dict(id="C08", cite="Takahashi et al. 2016, Phys. Rev. Applied 6, 054004",
         claim="per-pulse switching probability below 1% (report: P1 = 0.0048)",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="'very small, less than 1%'"),
    dict(id="C09", cite="Takahashi et al. 2016",
         claim="~500 pulses to converge, ~66% of saturation",
         reached="Y", queries=1, exists="Y", says=None,
         note="search text gives 80 pulses at 1.00 mW plus a small field for full "
              "switching, and ~75% alignment in a later review; 500 and 66% not found"),
    dict(id="C10", cite="Cheng et al. 2023 (PMC10621044)",
         claim="~0.3 T effective field for >90% AO-HDS in Pt/Co/Pt",
         reached="N", queries=1, exists="N", says=None,
         note="one search; counter-source: Li et al. 2023 (Rare Metals) state the "
              "IFE field must be ~10 T in ultrafast simulations of Pt/Co/Pt"),
    dict(id="C11", cite="Gonzalez-Alcalde et al. 2024, Nanophotonics 13, 1993",
         claim="plasmonic IFE amplification 7-15x",
         reached="Y", queries=1, exists="Y", says=None,
         note="search text: 'an order-of-magnitude enhancement' vs a 20 nm Au film; "
              "no 7-15 range found"),
    dict(id="C12", cite="Wang et al. 2021, Light Sci. Appl. 10, 8",
         claim="second shot re-writes after ~300 ps; ~3 GHz ceiling",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="3 GHz is the authors' forecast; the report calls it a 'hard measured floor'"),
    dict(id="C13", cite="Verges et al. 2023, Adv. Sci. 10(4)",
         claim="~400% lower switching energy; Faraday up to 5000%",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="'400% smaller' read literally is impossible; a seminar abstract says ~4x"),
    dict(id="C14", cite="Seagate 2025",
         claim="over one million Mozaic HAMR drives shipped by mid-2025",
         reached="Y", queries=1, exists="Y", says="MATCH",
         note="company statement, not an independent count"),
]


def state(row):
    return citation_state(row["reached"], row["queries"], row["exists"], row["says"])


def counts():
    out = {s: 0 for s in STATES}
    for r in ROWS:
        out[state(r)] += 1
    return out


def render():
    lines = ["optical-switching-constraint-chain / citations.py",
             "=" * 70,
             f"searched {SEARCHED}, search-result depth only (arxiv.org unresolvable here)",
             "states derived by tools/check_citations.citation_state", ""]
    for r in ROWS:
        lines.append(f"{r['id']}  {state(r):<11}  {r['cite']}")
        lines.append(f"      claim: {r['claim']}")
        lines.append(f"      note:  {r['note']}")
    c = counts()
    lines += ["", "counts: " + ", ".join(f"{s} {c[s]}" for s in STATES),
              "", "what moves:",
              "  OSC_005 (7.6 uJ/cm2): its source value is UNREACHABLE (C04); sibling work is mJ-class",
              "  OSC_006 (120 aJ): only the 6 J/cm3 half is VERIFIED (C05); 120 aJ UNREACHABLE (C06)",
              "  sec. 6.3 depinning precedent: NOT_FOUND (C02); the ~100x discount rests on it",
              "  sec. 4.1 FePt barrier: 7.6 eV UNREACHABLE; a sibling paper says 5.1 eV (C07)",
              "  sec. 5 class split: 0.3 T NOT reached, and a counter-source puts Pt/Co/Pt at ~10 T (C10)"]
    return "\n".join(lines)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("citations.py is a ledger; run: python3 test_citations.py")
        sys.exit(2)
    print(render())
