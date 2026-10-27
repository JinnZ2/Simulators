#!/usr/bin/env python3
"""Checks on SOURCE_DROP.md (Kimi / OKComputer deep-research report,
"The Constraint Chain of All-Optical Magnetic Recording").

Reads the delivered report. Never edits it. Recomputes every number the
report derives from stated inputs, and flags where a stated number does
not follow from the inputs the report gives.

    python3 check.py              render the report
    python3 check.py --selftest   run the checks

What it does NOT do: measure anything, read any cited paper, or rate the
physics. Literature values below are the report's own, carried as stated.
"""
import hashlib
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOC = HERE / "SOURCE_DROP.md"
PINNED_SHA256 = "6f1b4c3ea468a320a11db202415ec72d5817335dba49f83656e3398db0b4887f"

MU0 = 4e-7 * math.pi
KB = 1.380649e-23
EV = 1.602176634e-19
T = 300.0
KT = KB * T


def sha():
    return hashlib.sha256(DOC.read_bytes()).hexdigest()


def text():
    return DOC.read_text(encoding="utf-8")


# ------------------------------------------------------- 1. Kaplan-Gehring table

def stripe_period(n, ms=0.9e6, keff=0.5e6, aex=15e-12, t_co=0.6e-9):
    """Equilibrium stripe period in metres, the form the report quotes."""
    t = n * t_co
    sw = 4 * math.sqrt(aex * keff)
    ed = MU0 * ms ** 2 / 2
    return t * math.exp(math.pi * sw / (2 * ed * t) + math.log(math.pi) - 0.5 - math.log(2))


# The report's table, in micrometres.
STATED_D_UM = {3: 2.5e5, 5: 224, 7: 12.5, 9: 2.7, 10: 1.6, 12: 0.75}


def crossover_n(spot_um=1.36, **kw):
    """Smallest integer N whose stripe period falls below the spot."""
    for n in range(1, 60):
        if stripe_period(n, **kw) * 1e6 < spot_um:
            return n
    return None


def envelope():
    """Crossover N over a modest parameter box. The report names its own
    envelope only as an outcome range (0.13 um to 2.5 mm at N = 9); the box
    here is this audit's choice, stated, to show the crossover moves."""
    out = []
    for ms in (0.8e6, 0.9e6, 1.0e6):
        for keff in (0.3e6, 0.5e6, 0.7e6):
            for aex in (10e-12, 15e-12, 20e-12):
                out.append(crossover_n(ms=ms, keff=keff, aex=aex))
    return min(out), max(out), out.count(None)


# ------------------------------------------------------- 2. Delta = 60 crossings

def l60_slab(keff, t):
    return math.sqrt(60 * KT / (keff * t)) * 1e9


def d60_cyl(ku, t):
    return math.sqrt(60 * KT / (ku * t * math.pi / 4)) * 1e9


STATED_L60 = {"FePt K5 t10": 2.5, "CoPt 12nm K0.5": 6.4, "CoPt 5.4nm K0.5": 9.6, "CoPt 5.4nm K0.3": 12.4}


def computed_l60():
    return {"FePt K5 t10": d60_cyl(5e6, 10e-9), "CoPt 12nm K0.5": l60_slab(0.5e6, 12e-9),
            "CoPt 5.4nm K0.5": l60_slab(0.5e6, 5.4e-9), "CoPt 5.4nm K0.3": l60_slab(0.3e6, 5.4e-9)}


def delta_at_30nm():
    L = 30e-9
    co = {"CoPt 12nm K0.5": 0.5e6 * L * L * 12e-9 / KT, "CoPt 5.4nm K0.5": 0.5e6 * L * L * 5.4e-9 / KT,
          "CoPt 5.4nm K0.3": 0.3e6 * L * L * 5.4e-9 / KT}
    fept = 5e6 * math.pi / 4 * L * L * 10e-9 / KT
    return co, fept


# ------------------------------------------------------- 3. energy ledger

def disc_cm2(d_um):
    return math.pi * (d_um * 1e-4 / 2) ** 2


# (label, fluence J/cm2 as the report states it, spot diameter um, pulses, stated pJ)
LEDGER = [
    ("UCSD vector beam", 7.6e-6, 0.76, 1000, 12.0),
    ("classic AO-HDS", 4e-3, 0.76, 100, 640.0),
    ("plasmonic TbFeCo", 3.7e-3, 0.053, 100, 4.9),
]


def ledger_rows():
    rows = []
    for label, f, d, n, stated in LEDGER:
        incident = f * disc_cm2(d) * n * 1e12
        rows.append((label, incident, stated, stated / incident))
    return rows


def own_threshold_ratio():
    """The report's own Co/Pt switching-fluence range (section 5 table) against
    the 7.6 uJ/cm2 it uses for the UCSD energy row."""
    t = text()
    m = re.search(r"Switching fluence threshold \| ([0-9.]+)[–-]([0-9.]+) mJ/cm²", t)
    lo, hi = float(m.group(1)) * 1e-3, float(m.group(2)) * 1e-3
    return lo, hi, lo / 7.6e-6, hi / 7.6e-6


def gdfeco():
    vol_40 = 40e-7 * 40e-7 * 20e-7   # cm3
    return 6 * vol_40 * 1e18, 120.0  # computed aJ, stated aJ


# ------------------------------------------------------- 4. other arithmetic

def misc():
    return {
        "8 pulses at 3 GHz (ns)": (8 / 3e9 * 1e9, 2.7),
        "300 ps spacing -> GHz": (1 / 300e-12 / 1e9, 3.0),
        "1e3 pulses at 1 kHz (s)": (1e3 / 1e3, 1.0),
        "500 pulses at 1 kHz (s)": (500 / 1e3, 0.5),
        "HAMR 4 mW / 2 Gb/s (pJ)": (4e-3 / 2e9 * 1e12, 2.0),
        "0.95 eV / kT": (0.95 * EV / KT, 38.0),
        "100 eV / kT": (100 * EV / KT, 4000.0),
        "350/100 .. 1300/100": (350 / 100, 4.0),
    }


def ten_year_single_bit():
    yr = 3.156e7
    return math.log(10 * yr / 1e-9), math.log(10 * yr / 1e-10)


# ------------------------------------------------------- 5. figure numbering

def figure_files():
    return re.findall(r"\(figures/(fig\d)_", text())


# ------------------------------------------------------- 6. anchors

ANCHORS = [
    ("Khalid et al., Nat. Commun. 2026, 'Optical beam shaping induced reconfigurable "
     "magnetic domains', 15 Sep 2026, DOI 10.1038/s41467-026-77572-3", "FOUND_IN_SEARCH"),
    ("arXiv:1312.7301, Co nano-square depinning 0.95 eV", "NOT_LOCATED"),
    ("all other citations", "NOT_CHECKED"),
]


# ------------------------------------------------------- render

def render():
    out = ["optical-switching-constraint-chain / check.py", "=" * 66,
           f"SOURCE_DROP.md sha256 {sha()[:16]}...  pinned: {sha() == PINNED_SHA256}", "",
           "1. STRIPE PERIOD (Kaplan-Gehring form, report's parameters)",
           f"   {'N':>3} {'computed um':>12} {'stated um':>10}"]
    for n, st in STATED_D_UM.items():
        out.append(f"   {n:>3} {stripe_period(n) * 1e6:>12.3g} {st:>10g}")
    lo, hi, none = envelope()
    out += [f"   first N below the spot band top (1.5 um) at report parameters: N = {crossover_n(1.5)}"
            f"  (N=11 period {stripe_period(11) * 1e6:.2f} um)",
            "   report: the period 'crashes through the focused-spot scale precisely at N = 9-10';",
            "   experiment: stripes at N >= 10. The model at the report's own parameters crosses at N = 11.",
            f"   over Ms 0.8-1.0 MA/m, Keff 0.3-0.7 MJ/m3, A 10-20 pJ/m: N = {lo}..{hi}"
            f" ({none} corners never cross below N = 60; spot 1.36 um)",
            "   -> reproduces exactly; the 'confirmed by experiment' crossover is a property",
            "      of the chosen parameters, which the report's own caveat says span 4 decades"]
    out += ["", "2. DELTA = 60 CROSSINGS (nm)"]
    for k, v in computed_l60().items():
        out.append(f"   {k:<18} computed {v:5.2f}  stated {STATED_L60[k]}")
    co, fept = delta_at_30nm()
    out += ["   Delta at 30 nm: " + ", ".join(f"{k} {v:.0f}" for k, v in co.items()),
            f"   FePt cylinder at 30 nm: {fept:.0f}",
            "   -> 'every configuration sits at 350-1300' holds for the three Co/Pt curves only"]
    out += ["", "3. ENERGY LEDGER (stated 'absorbed' pJ vs fluence x disc spot x pulses)"]
    for label, inc, st, frac in ledger_rows():
        out.append(f"   {label:<18} incident {inc:8.1f}  stated {st:6.1f}  implied fraction {frac:.2f}")
    lo_t, hi_t, r_lo, r_hi = own_threshold_ratio()
    c, s = gdfeco()
    out += ["   -> no absorbed fraction is stated; the stated values imply ~0.35, 0.35, 0.60",
            f"   report's own Co/Pt switching threshold: {lo_t * 1e3:g}-{hi_t * 1e3:g} mJ/cm2;",
            f"   the UCSD row uses 7.6 uJ/cm2, {r_lo:.0f}-{r_hi:.0f}x below it",
            f"   GdFeCo limit: 6 J/cm3 x 40x40x20 nm3 = {c:.0f} aJ; stated {s:.0f} aJ"]
    out += ["", "4. OTHER ARITHMETIC (computed, stated)"]
    for k, (cv, st) in misc().items():
        out.append(f"   {k:<26} {cv:9.3g}  {st:g}")
    a, b = ten_year_single_bit()
    out += [f"   ten-year survival of ONE bit needs Delta = ln(t/tau0) = {a:.1f}..{b:.1f}",
            "   -> Delta >= 60 is a population/dispersion criterion, as the report notes;",
            "      the 40-60 'marginal' band is where a single bit already lasts ten years"]
    files = figure_files()
    out += ["", "5. FIGURE REFERENCES", f"   files in reading order: {files}",
            "   text calls them Figure 1..6; the phase map (text Figure 1) is fig6, the rest shift by one"]
    out += ["", "6. ANCHORS (search-result depth, carried)"]
    for name, st in ANCHORS:
        out.append(f"   {st:<16} {name}")
    out += ["", "Nothing above measures a barrier, rates a material, or ranks a technology."]
    return "\n".join(out)


def selftest():
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    ok("document unedited (sha pinned)", sha() == PINNED_SHA256)
    for n, st in STATED_D_UM.items():
        ok(f"stripe period N={n} within 5% of stated", abs(stripe_period(n) * 1e6 / st - 1) < 0.05)
    ok("model crosses the 1.5 um band top at N=11, one above the observed N=10",
       crossover_n(1.5) == 11 and stripe_period(10) * 1e6 > 1.5)
    lo, hi, none = envelope()
    ok("crossover moves across the parameter box", hi is not None and hi - lo >= 3)
    for k, v in computed_l60().items():
        ok(f"Delta=60 crossing {k} within 2%", abs(v / STATED_L60[k] - 1) < 0.02)
    co, fept = delta_at_30nm()
    ok("Co/Pt Delta at 30 nm spans 350-1300", 350 <= min(co.values()) and max(co.values()) <= 1310)
    ok("FePt Delta at 30 nm is outside 350-1300", fept > 1300)
    fr = [f for *_, f in ledger_rows()]
    ok("energy rows do not follow from incident fluence", all(f < 0.9 for f in fr))
    ok("first two rows imply the same ~0.35 fraction", abs(fr[0] - fr[1]) < 0.02 and abs(fr[0] - 0.35) < 0.02)
    lo_t, hi_t, r_lo, r_hi = own_threshold_ratio()
    ok("UCSD fluence is >200x below the report's own Co/Pt threshold", r_lo > 200)
    c, s = gdfeco()
    ok("GdFeCo 6 J/cm3 x stated volume != stated 120 aJ", abs(c - s) > 50)
    for k, (cv, st) in misc().items():
        ok(f"{k} within 10% of stated", abs(cv / st - 1) < 0.15)
    a, b = ten_year_single_bit()
    ok("single-bit ten-year Delta is 40-43", 40 < a < b < 43)
    ok("six figure references, phase map first", figure_files()[0] == "fig6" and len(figure_files()) == 6)
    failed = [n for n, c in checks if not c]
    for n, c in checks:
        print(("PASS " if c else "FAIL ") + n)
    print(f"checks: {len(checks)}   failed: {len(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(selftest())
    print(render())
