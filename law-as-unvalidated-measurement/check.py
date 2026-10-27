#!/usr/bin/env python3
# law-as-unvalidated-measurement/check.py -- CC0, stdlib only, parses under 3.9
#
# Recomputes the mechanical items of the correction notice. Two layers:
#   1  arithmetic and structure that need no external file
#   2  checks against the target report, run ONLY when --report PATH is given;
#      without it every report-side row reads NOT_PRESENT, which is not a pass.
# The report is not committed in this tree (it is not an evidence layer), so
# layer 2 is how a reader with the zip reproduces section H.1.

import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTICE = os.path.join(HERE, "CORRECTION-law-as-unvalidated-measurement-2026-10-03.md")
REGISTER = os.path.join(HERE, "NAMED_AND_ABSENT.md")
LEDGER = os.path.join(HERE, "LEDGER_SETTLE-dyed-fuel-2026-10-03.md")
DESIGN = os.path.join(HERE, "DESIGN_frame-substitution-eval.md")

REPORT_SHA256 = "3205096cfb344bc2132ccc923570157c4c3d5ff5722c24ab9886b19d109f7f66"  # the ZIP, not the .md

# (phrase, must_be_present) -- the notice's section H.1 claims about the report text
REPORT_PHRASES = [
    ("nicknamed **dyed-fuel-diff**", True),
    ("refused (or moralized) both", True),
    ("frame substitution", True),
    ("6.4% and 91%", True),
    ("1,126,959", True),
    ("175.2%", True),
    ("cannot, in principle, encode", True),
    ("memorized token-prefix patterns", True),
    ("~22 yrs", True),
    ("2A:171-5.8", True),
    ("white shirt", True),
    ("RECOVER-THE-LAW", True),
    ("without knowing it", True),
    ("mid-hearing", True),
    ("Llama-2-7B-chat", True),
    ("laundry", False),
    ("corroborat", False),
    ("Alsen", True),
]

ROWS = []


def row(label, state, detail=""):
    ROWS.append((label, state, detail))


def read(path):
    with io.open(path, encoding="utf-8") as fh:
        return fh.read()


# ---- layer 1: arithmetic -----------------------------------------------------

def arithmetic():
    # RegData: 409,520 -> 1,126,959 is +175.2 %, and the per-year figure uses 55 intervals
    growth = 1126959 / 409520.0
    row("regdata growth 1,126,959/409,520", "PASS" if abs((growth - 1) * 100 - 175.2) < 0.05 else "FAIL",
        "+%.1f%%" % ((growth - 1) * 100))
    per_year_55 = (1126959 - 409520) / 55.0
    per_year_56 = (1126959 - 409520) / 56.0
    row("regdata +13,044/yr divisor", "PASS" if abs(per_year_55 - 13044) < 1 and abs(per_year_56 - 13044) > 100 else "FAIL",
        "55 intervals -> %.1f ; 56 -> %.1f" % (per_year_55, per_year_56))
    # Column A: 3.9 lb solid SR26 / 1000 bbl -> mg/L and ppm by mass at 0.85 kg/L
    lb, bbl_gal, L_per_gal = 3.9, 42.0, 3.785411784
    mg_per_L = lb * 453.59237 * 1000 / (1000 * bbl_gal * L_per_gal)
    row("column A 3.9 lb/1000 bbl -> mg/L", "PASS" if abs(mg_per_L - 11.13) < 0.02 else "FAIL", "%.2f mg/L" % mg_per_L)
    ppm_mass = mg_per_L / 850.0 * 1000.0
    row("column A -> ppm by mass @0.85 kg/L", "PASS" if abs(ppm_mass - 13.1) < 0.1 else "FAIL", "%.1f ppm" % ppm_mass)
    # Column A annual SR26-equivalent mass at 18.2 B gal/yr
    t_metric = lb * 0.45359237 * (18.2e9 / bbl_gal) / 1000.0 / 1000.0
    row("column A SR26-eq t/yr @18.2 B gal", "PASS" if abs(t_metric - 767) < 2 else "FAIL", "%.0f t" % t_metric)
    # the ledger's two readings, for the band
    oz_t = 18.2e9 / 100 * 28.349523 / 1e6
    ppm26_t = 18.2e9 * L_per_gal * 0.85 * 26e-6 / 1000.0
    row("ledger readings 1 oz/100 gal and 26 ppm", "PASS" if abs(oz_t - 5160) < 5 and abs(ppm26_t - 1522) < 5 else "FAIL",
        "%.0f t and %.0f t" % (oz_t, ppm26_t))
    # the ounce reading in ppm by mass
    oz_ppm = 28.349523 / (100 * L_per_gal * 850.0) * 1e6
    row("1 oz/100 gal in ppm by mass", "PASS" if abs(oz_ppm - 88) < 1 else "FAIL", "%.0f ppm" % oz_ppm)


# ---- layer 1: structure -------------------------------------------------------

def structure():
    notice = read(NOTICE)
    for sec in ("## A. ", "## B. ", "## C. ", "## D. ", "## E. ", "## F. ", "## G. ", "## H. "):
        row("notice carries section %s" % sec.strip("# ."), "PASS" if sec in notice else "FAIL")
    row("notice names the zip hash", "PASS" if REPORT_SHA256 in notice else "FAIL")
    reg = read(REGISTER)
    for name in ("why-recovery", "split-ledger / parks", "regulation-archaeology-failure-strata",
                 "why-recovery-box-edge-instrument", "RECOVER-THE-LAW"):
        row("register names %s" % name, "PASS" if name in reg else "FAIL")
    # the two instruments must not have been scaffolded anywhere in this tree, by PATH
    tree = os.path.dirname(HERE)
    hits = []
    for dp, dn, fn in os.walk(tree):
        dn[:] = [d for d in dn if d not in (".git", "__pycache__")]
        for n in fn + dn:
            low = n.lower()
            if "why-recovery" in low or "why_recovery" in low or "split-ledger" in low or "split_ledger" in low:
                hits.append(os.path.join(dp, n))
    row("no why-recovery / split-ledger artifact by path", "PASS" if not hits else "FAIL", "; ".join(hits[:3]))
    led = read(LEDGER)
    for tok in ("SETTLED", "NOT_EVALUABLE", "ZEROED", "MOVED", "3.9 lb / 1,000 bbl", "11.13 mg/L"):
        row("ledger settle carries %s" % tok, "PASS" if tok in led else "FAIL")
    des = read(DESIGN)
    for tok in ("PHYSICS", "LAW-AS-PRIOR", "MIXED", "REFUSED", "REGRESSION", "ADVISING", "EXAMINING", "ADJACENT"):
        row("design carries %s" % tok, "PASS" if tok in des else "FAIL")
    row("design is PROPOSED, no harness", "PASS" if "PROPOSED" in des and "no harness" in des.lower() else "FAIL")


# ---- layer 2: the report, only if handed in -----------------------------------

def report_checks(path):
    if path is None:
        row("report file", "NOT_PRESENT", "pass --report PATH to run the quote checks; NOT_PRESENT is not a pass")
        return
    if not os.path.isfile(path):
        row("report file", "NOT_PRESENT", path)
        return
    text = read(path)
    row("report size", "PASS" if 80000 <= len(text.encode("utf-8")) <= 80300 else "FLAG",
        "%d bytes (notice says 80130)" % len(text.encode("utf-8")))
    for phrase, present in REPORT_PHRASES:
        found = phrase in text
        ok = found if present else not found
        row("report %s %r" % ("contains" if present else "lacks", phrase), "PASS" if ok else "FAIL")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("check.py IS the check; run it bare or with --report PATH\n")
        return 2
    rpt = None
    if "--report" in argv:
        i = argv.index("--report")
        rpt = argv[i + 1] if i + 1 < len(argv) else ""
    arithmetic()
    structure()
    report_checks(rpt)
    width = max(len(r[0]) for r in ROWS)
    for label, state, detail in ROWS:
        print("%-*s  %-11s %s" % (width, label, state, detail))
    n_fail = sum(1 for r in ROWS if r[1] == "FAIL")
    n_np = sum(1 for r in ROWS if r[1] == "NOT_PRESENT")
    print("\nchecks: %d   FAIL: %d   NOT_PRESENT: %d   (NOT_PRESENT is a gap, not a pass)" % (len(ROWS), n_fail, n_np))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
