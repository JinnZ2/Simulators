#!/usr/bin/env python3
"""Checks for the labor-instrument rebuild. Known answers on constructed
data; no real BLS/ALFRED/QCEW data is fetched (egress-blocked) or
fabricated. The PART 1 acceptance test against the real 2026-08-28 benchmark
is marked NOT RUNNABLE here and recorded, not faked.

    python3 labor-instrument/selftest.py
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import vintage_store as VS          # noqa: E402
import instrument_registry as IR    # noqa: E402
import decompose as D               # noqa: E402
import labor_schema as LS           # noqa: E402
import no_severity                  # noqa: E402

FAILS = []
N = [0]

# the work order's acceptance target (delivered; carried, not verified --
# BLS egress-blocked). Recorded for when real vintages land.
ACCEPTANCE_TARGET = {
    "retail trade": -154600, "private education and health": -96000,
    "wholesale trade": -86200, "manufacturing": -67000,
    "release": "2026-08-28",
}


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def build_store():
    s = VS.VintageStore()
    # scenario A: no NAICS change in span, multi-vintage both endpoints
    s.add("CES_RETAIL", "2025-01", "2025-02", 100.0)
    s.add("CES_RETAIL", "2025-01", "2026-02", 98.0)    # revised -2 at benchmark
    s.add("CES_RETAIL", "2025-07", "2025-08", 110.0)
    s.add("CES_RETAIL", "2025-07", "2026-02", 105.0)   # revised -5
    # scenario B: spans the 2012 NAICS change, multi-vintage both endpoints
    s.add("CES_RETAIL", "2011-06", "2011-07", 200.0)
    s.add("CES_RETAIL", "2011-06", "2013-02", 198.0)   # rev -2
    s.add("CES_RETAIL", "2013-06", "2013-07", 210.0)
    s.add("CES_RETAIL", "2013-06", "2014-02", 209.0)   # rev -1
    # single-vintage period (revision unknown)
    s.add("CES_RETAIL", "2020-01", "2020-02", 300.0)
    return s


def main():
    print("selftest (labor-instrument)")
    for f in ("vintage_store.py", "instrument_registry.py", "decompose.py", "labor_schema.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, f), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % f, rc == 2)

    # ---- M1 vintage_store: every version retained, keyed by release_date
    s = build_store()
    check("M1: a fresh store is empty (no ALFRED data fetched)", VS.VintageStore().is_empty())
    check("M1: a period keeps every version, sorted by release_date",
          [o.value for o in s.versions("CES_RETAIL", "2025-01")] == [100.0, 98.0])
    check("M1: revision = latest - earliest (the period moved across vintages)",
          s.revision("CES_RETAIL", "2025-07") == -5.0 and s.revision("CES_RETAIL", "2025-01") == -2.0)
    check("M1: a single-vintage period has no observable revision (None, not 0)",
          s.revision("CES_RETAIL", "2020-01") is None)
    check("M1: as_of returns the version current at a release_date",
          s.as_of("CES_RETAIL", "2025-01", "2025-06").value == 100.0
          and s.as_of("CES_RETAIL", "2025-01", "2026-06").value == 98.0)

    # ---- M2 instrument_registry: seed carried (unverified), recurring change
    reg = IR.InstrumentRegistry()
    names = [c.change_name for c in reg.changes]
    check("M2: the 2026-01 ARIMA change carries the 185,000 note and its span",
          any("185,000" in c.note and c.recalculated_span for c in reg.changes if c.effective_date == "2026-01"))
    check("M2: the rolling 5-year seasonal re-estimation is a RECURRING change",
          any(c.recurring for c in reg.changes))
    check("M2: every seed entry is UNVERIFIED (BLS egress-blocked, none fabricated)",
          len(reg.unverified()) == len(reg.changes))
    # a recurring change is always in scope; a NAICS change only within its span
    check("M2: boundary_changes finds the 2012 NAICS change for a 2011->2013 span",
          any("NAICS 2007" in c.change_name for c in reg.boundary_changes("2011-06", "2013-06")))
    check("M2: no NAICS change is in scope for a 2025 span",
          reg.boundary_changes("2025-01", "2025-07") == [])
    check("M2: the recurring seasonal change is in scope for any span",
          any(c.recurring for c in reg.between("2025-01", "2025-07")))

    # ---- M3 decompose: the three-way split; band where ambiguous
    # scenario A: unambiguous (no NAICS in span, no crosswalk) -> point
    a = D.decompose("CES_RETAIL", "2025-01", "2025-07", s, reg, "retail", crosswalk={})
    check("M3(A): raw = 7, revision = -3, boundary = point(0), real_change a point",
          a["raw_delta"] == 7.0 and a["revision"] == -3.0
          and D.is_point(a["boundary_crossing"]) and D.is_point(a["real_change"]))
    check("M3(A): as_point returns the real_change (10) when unambiguous",
          D.as_point(a["real_change"]) == 10.0)
    # scenario B: NAICS change in span + ambiguous crosswalk -> BAND, never a point
    b = D.decompose("CES_RETAIL", "2011-06", "2013-06", s, reg, "retail",
                    crosswalk={"retail": (5, 15)})
    check("M3(B): an ambiguous crosswalk makes boundary_crossing a band [5,15]",
          b["boundary_crossing"] == D.Band(5.0, 15.0) and b["ambiguous"])
    check("M3(B): real_change is a band [-5, 5], never a point", not D.is_point(b["real_change"])
          and b["real_change"] == D.Band(-5.0, 5.0))
    raised = False
    try:
        D.as_point(b["real_change"])
    except D.AmbiguousPoint:
        raised = True
    check("M3(B): as_point RAISES on an ambiguous decomposition (no point where the crosswalk splits)", raised)
    # single-vintage endpoint -> revision UNKNOWN, widened, ambiguous
    c = D.decompose("CES_RETAIL", "2020-01", "2025-07", s, reg, "retail", crosswalk={})
    check("M3: a single-vintage endpoint yields revision UNKNOWN and an ambiguous result",
          c["revision"] == "UNKNOWN (single vintage)" and c["ambiguous"])
    # missing endpoint -> UNRECOVERABLE
    miss = D.decompose("CES_RETAIL", "1999-01", "2025-07", s, reg, "retail", crosswalk={})
    check("M3: a missing endpoint is UNRECOVERABLE (no data), not a fabricated split",
          miss["status"] == "UNRECOVERABLE")

    # ---- acceptance test: NOT RUNNABLE here (egress); recorded, not faked
    empty = VS.VintageStore()
    recon = {sector: D.decompose("CES_%s" % sector, "2024-03", "2025-03", empty, reg, sector, crosswalk={})
             for sector in ("retail trade", "manufacturing")}
    check("acceptance: with no ALFRED vintages fetched, reconstruction is UNRECOVERABLE, not a pass",
          all(r["status"] == "UNRECOVERABLE" for r in recon.values()) and empty.is_empty())
    check("acceptance: the 2026-08-28 target is recorded for when real data lands",
          ACCEPTANCE_TARGET["retail trade"] == -154600 and ACCEPTANCE_TARGET["release"] == "2026-08-28")

    # ---- PART 2 schema: the invariants are enforced, not just described
    hrec = LS.WorkRecord("h1", "human", exposure=8.0, load_factor=0.7,
                         task_class="sort", output_delivered=40.0, joules_in=1.2e6,
                         allocation_model="augmentation")
    crec = LS.WorkRecord("c1", "compute", exposure=8.0, load_factor=0.9,
                         task_class="sort", output_delivered=400.0, joules_in=2.0e6,
                         error_rate_under_load=0.03, allocation_model="augmentation")
    check("PART2: 'capital' is not a field on WorkRecord (capital stays out)",
          "capital" not in LS.WorkRecord.__dataclass_fields__)
    check("PART2: exposure unit is declared per class and differs across classes",
          hrec.exposure_unit() == "person-hours" and crec.exposure_unit() == "substrate-hours")
    check("PART2: efficiency is two numbers (per-joule crosses classes, per-hour is per-class)",
          set(LS.efficiency(hrec)) >= {"output_per_joule", "output_per_exposure_hour"})
    for fn, exc, label in ((lambda: LS.convert_exposure(hrec, "compute"), LS.ExposureConversion, "convert_exposure"),
                           (lambda: LS.combined_efficiency(hrec), LS.EfficiencyCollapse, "combined_efficiency"),
                           (lambda: LS.balance_on_capital(hrec), LS.CapitalImport, "balance_on_capital")):
        r = False
        try:
            fn()
        except exc:
            r = True
        check("PART2: %s RAISES (the invariant is enforced, not a note)" % label, r)
    check("PART2: allocation model is declared, never defaulted -- None is flagged",
          LS.allocation_declared(hrec)
          and not LS.allocation_declared(LS.WorkRecord("x", "human", 1, 1, "t", 1, 1)))

    # ---- read-layer: combined output-per-joule beats either substrate alone
    combined_yes = LS.WorkRecord("hc", "combined", exposure=8.0, load_factor=0.8,
                                 task_class="sort", output_delivered=900.0, joules_in=3.0e6,
                                 allocation_model="augmentation")
    q = LS.complementarity([hrec, crec, combined_yes], "sort")
    check("read-layer: combined beats either alone when its output_per_joule is higher (not CONSTANT)",
          q["combined_beats_either_alone"])
    combined_no = LS.WorkRecord("hc2", "combined", exposure=8.0, load_factor=0.8,
                                task_class="sort", output_delivered=300.0, joules_in=3.0e6,
                                allocation_model="augmentation")
    q2 = LS.complementarity([hrec, crec, combined_no], "sort")
    check("read-layer: a combined op that does NOT beat either alone reads False (both directions)",
          not q2["combined_beats_either_alone"])

    # ---- money vs joule ranking flip (constructed; real data is GAP 2)
    ops = [{"name": "hyperaccumulator", "output": 10.0, "joules_in": 5.0, "hours": 8760, "price": 1000.0},
           {"name": "smelter", "output": 100.0, "joules_in": 5000.0, "hours": 10, "price": 200.0}]
    ranks = LS.money_vs_joule_rank(ops)
    check("PART2: money and joule indices rank the same two operations differently (the denominator does the work)",
          ranks["by_money"] != ranks["by_joule"]
          and ranks["by_joule"][0] == "hyperaccumulator" and ranks["by_money"][0] == "smelter")

    # ---- renders screen clean
    outs = [D.render(a), D.render(b), D.render(miss)]
    check("decompose renders screen clean", not any(no_severity.hits(o) for o in outs))
    check("screen fires on a planted word", bool(no_severity.hits(outs[0] + "\nthis is wrong\n")))

    os.makedirs(os.path.join(HERE, "samples"), exist_ok=True)
    with open(os.path.join(HERE, "samples", "decompose.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(D.render(r) for r in (a, b, c, miss)) + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
