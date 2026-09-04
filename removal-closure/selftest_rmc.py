#!/usr/bin/env python3
"""Checks for removal_closure.py and rhythm_gaps.py. Known answers
first, both directions of every guard. Rows are CONSTRUCTED
(constructed:// URLs). The dataset run is exercised on a constructed
CSV in the dataset's column shape; if the real file is present at the
path given by RHYTHM48_CSV it is also run and its headline numbers
pinned, and its absence is reported, not failed.

    python3 removal-closure/selftest_rmc.py
"""

import csv
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import removal_closure as RM  # noqa: E402
import rhythm_gaps as RG  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def row(**kw):
    base = dict(constant="c1", organism="o1", claim="rhythm tracks c1", step_reached="5",
                removability="high", removal_demonstrated="y", removal_method="centrifuge",
                first_correlation_year="1800", closure_year="1900", transducer="named",
                gain_problem="UNMEASURED", dismissal_recorded="n",
                source_url="constructed://fixture/1")
    base.update(kw)
    return base


def to_csv(rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=RM.FIELDS)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    return buf.getvalue()


def world(track=True):
    """Six rows: removability high/high/medium/medium/low/low; closure
    times rising with lower removability (track) or falling (anti); the
    last low row open."""
    rem = ["high", "high", "medium", "medium", "low", "low"]
    yrs = [50, 80, 120, 150, 200, None] if track else [200, 150, 120, 80, 50, None]
    out = []
    for i, (rm, y) in enumerate(zip(rem, yrs)):
        out.append(row(constant="c%d" % i, removability=rm,
                       step_reached=("3" if rm == "low" else "5") if y else "1",
                       removal_demonstrated="y" if y else "n",
                       removal_method="none" if not y else "centrifuge",
                       closure_year=str(1800 + y) if y else "null",
                       transducer="named" if y else "none",
                       source_url="constructed://fixture/%d" % i))
    return out


def main():
    print("selftest_rmc")

    # ---- derivations and rules
    r = RM.validate_rows([row()])[0]
    check("years_to_closure = closure - first", RM.years_to_closure(r) == 100)
    o = RM.validate_rows([row(closure_year="null")])[0]
    check("open row: years None, censored = current - first",
          RM.years_to_closure(o) is None and RM.years_censored(o, 2026) == 226)
    wt = RM.validate_rows(world(True))
    wa = RM.validate_rows(world(False))
    h1 = RM.h1(wt)
    check("H1 not falsified when every closed row has removal", h1["verdict"].startswith("H1 not"))
    bad = RM.validate_rows(world(True)[:4] + [row(constant="x", removal_demonstrated="n",
                                                   removal_method="none",
                                                   source_url="constructed://fixture/x")])
    check("H1 FALSE on one closed row without removal",
          RM.h1(bad)["verdict"].startswith("H1 FALSE") and RM.h1(bad)["without"] == ["x"])
    part = RM.validate_rows([row(removal_demonstrated="partial")])
    check("partial: not counted under CHOICE 2, counted under strict",
          RM.h1(part)["without"] == [] and RM.h1(part)["without_strict"] == ["c1"])
    check("H1 undetermined with no closed row",
          RM.h1(RM.validate_rows([row(closure_year="null")]))["verdict"].startswith("undetermined"))
    h2t, h2a = RM.h2(wt), RM.h2(wa)
    check("tracking world: closed-only rho < 0, H2 not falsified",
          h2t["closed_only"]["rho"] < 0 and h2t["closed_only"]["verdict"].startswith("H2 not"))
    check("anti world: closed-only rho > 0, H2 FALSE",
          h2a["closed_only"]["rho"] > 0 and h2a["closed_only"]["verdict"].startswith("H2 FALSE"))
    check("censored reading includes the open row", h2t["censored"]["n"] == 6 and h2t["closed_only"]["n"] == 5)
    check("open low-removability rows are named", h2t["open_low_removability"] == ["c5"])
    check("H2 undetermined on one row", RM.h2(wt[:1])["closed_only"]["verdict"] == "undetermined")
    h3 = RM.h3(wt)
    check("H3 not falsified when no low row reaches step 4", h3["verdict"].startswith("H3 not"))
    h3b = RM.h3(RM.validate_rows([row(removability="low", step_reached="4")]))
    check("H3 FALSE on a low row at step 4", h3b["verdict"].startswith("H3 FALSE"))
    check("H3 undetermined with no low row",
          RM.h3(RM.validate_rows([row()]))["verdict"].startswith("undetermined"))
    ct = RM.cross_tabs(wt)
    check("two cross-tabs with level counts", set(ct) == {"removability", "dismissal_recorded"}
          and ct["dismissal_recorded"]["levels"] == 1 and ct["dismissal_recorded"]["V"] is None)
    check("removability x step V computes on the world", ct["removability"]["V"] is not None)

    # ---- P2 pre-registration hash
    d = RM.precode_hash(wt)
    check("precode hash is stable across closure_year edits",
          RM.precode_hash(RM.validate_rows([dict(x, closure_year="null") for x in world(True)])) == d)
    check("precode hash moves when a removability is recoded",
          RM.precode_hash(RM.validate_rows([dict(world(True)[0], removability="low")] + world(True)[1:])) != d)
    check("check_precode both ways", RM.check_precode(wt, d) and not RM.check_precode(wt, "0" * 64))

    # ---- schema refusals
    for bad_kw, why in [({"step_reached": "4-5"}, "a step range"), ({"step_reached": "6"}, "step 6"),
                        ({"removability": "LOW"}, "case outside vocab"),
                        ({"closure_year": "2000s"}, "a decade closure year"),
                        ({"closure_year": "1700"}, "closure before first correlation"),
                        ({"source_url": ""}, "no URL"), ({"removal_method": "orbit"}, "method outside vocab")]:
        try:
            RM.validate_rows([row(**bad_kw)]); check("refuses " + why, False)
        except RM.SchemaRefused:
            check("refuses " + why, True)
    check("load_csv round-trips", len(RM.load_csv(to_csv(world()))) == 6)

    # ---- seed rows read back from the order
    seed = RM.seed_rows()
    check("five seed rows parsed", [s["constant"] for s in seed]
          == ["gravity", "day/night", "tidal/lunar", "geomagnetic", "ELF cavity"])
    rd = RM.seed_readiness(seed)
    check("no seed row carries a citation", not any(s["citation"] for s in rd))
    check("three step cells are ranges", sum(1 for s in rd if not s["step_single_value"]) == 3)
    ar = RM.seed_arithmetic(seed)
    check("gravity: 1806 -> 2000s gives 194..203, stated 200 inside",
          ar[0]["computed"] == (194, 203) and ar[0]["place"] == "inside")
    check("tidal/lunar: 1930s -> 2007 gives 68..77, stated 80 above by 3",
          ar[2]["computed"] == (68, 77) and ar[2]["place"] == "above by 3")
    check("ELF cavity: open, 2026 - 1893 = 133, stated 130 below by 3",
          ar[4]["kind"] == "open" and ar[4]["computed"] == (133, 133) and ar[4]["place"] == "below by 3")
    check("doctored order with no table parses to nothing", RM.seed_rows("# x\n") == [])

    # ---- rhythm_gaps on a constructed table in the dataset's shape
    def unit(f, sp, part, iu, start, speech, pause, lang):
        return {"file": f, "speaker": sp, "part": part, "io_unit": iu, "start": start,
                "end": start + speech, "pause": pause, "io": speech + pause, "speech": speech, "lang": lang}
    rows = [unit("f", "s", "part1", 1, 0.0, 1.0, 0.10, "L1"),
            unit("f", "s", "part1", 2, 1.1, 1.0, 0.40, "L1"),
            unit("f", "s", "part1", 3, 2.5, 1.0, 0.60, "L1"),
            unit("g", "s", "part1", 4, 0.0, 2.0, 0.05, "L2"),
            unit("g", "s", "part1", 5, 2.05, 2.0, 0.90, "L2")]
    m0 = RG.merge_at(rows, 0.0)
    check("t = 0 returns the units as delivered", len(m0) == 5 and abs(m0[0]["io"] - 1.10) < 1e-12)
    m2 = RG.merge_at(rows, 0.25)
    check("t = 0.25 merges the two units whose trailing pause < 0.25",
          len(m2) == 3 and any(abs(u["io"] - 2.50) < 1e-9 for u in m2)
          and any(abs(u["speech"] - 2.10) < 1e-9 for u in m2))
    res = RG.g2(rows, (0.0, 0.25, 0.5, 1.0))
    check("io mean monotone non-decreasing in t", RG.g2_monotone(res))
    check("unit count non-increasing in t", res[0.0]["units"] >= res[0.25]["units"] >= res[1.0]["units"])
    sym = [1.0, 1.5, 2.0, 2.0, 2.0, 2.5, 3.0]
    sh = RG.shape(sym)
    check("symmetric values: tail ratio 1.0, median 2.0, mode bin 2.00",
          abs(sh["tail_ratio"] - 1.0) < 1e-9 and sh["median"] == 2.0 and abs(sh["mode"] - 2.0) < 1e-9)
    skew = [1.0, 1.0, 1.1, 1.2, 1.3, 2.0, 4.0]
    check("right-skewed values: tail ratio > 1", RG.shape(skew)["tail_ratio"] > 1.0)
    check("tail ratio None when median == p05", RG.shape([2.0, 2.0, 2.0, 2.0, 5.0])["tail_ratio"] is None)
    check("empty shape is None throughout", RG.shape([])["median"] is None)
    check("percentile endpoints", RG._pct([1, 2, 3, 4], 0.0) == 1 and RG._pct([1, 2, 3, 4], 1.0) == 4)
    pl = RG.g3(rows, "io")
    check("g3 groups per language", set(pl) == {"L1", "L2"} and pl["L1"]["n"] == 3)
    check("five gaps declared not-run with a reason each",
          set(RG.NOT_RUN) == {"G1", "G4", "G5", "G6", "G7"} and all(RG.NOT_RUN.values()))
    # a constructed CSV through the file path, including R's 1e+05 spelling
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as fh:
        wcsv = csv.writer(fh)
        wcsv.writerow(["file", "speaker", "io_unit", "start_time", "end_time", "pause_duration",
                       "io_duration", "genre", "glottocode", "speaker_age", "speaker_sex",
                       "synthesis", "tone", "element", "sprach_dauer", "part"])
        for i, u in enumerate(rows):
            wcsv.writerow([u["file"], u["speaker"], "1e+05" if i == 4 else u["io_unit"], u["start"],
                           u["end"], u["pause"], u["io"], "g", u["lang"], 30, "m", "NA", "no", "a",
                           u["speech"], u["part"]])
        tmp = fh.name
    try:
        loaded = RG.load(tmp)
        check("load reads R's 1e+05 as 100000", loaded[4]["io_unit"] == 100000 and len(loaded) == 5)
        out_c = RG.render(tmp)
        check("constructed dataset render screens clean", not no_severity.hits(out_c))
    finally:
        os.remove(tmp)

    # ---- the real file, when present
    real = os.environ.get("RHYTHM48_CSV", "")
    if real and os.path.exists(real):
        ff = RG.file_facts(real)
        check("real file sha256 as pinned", ff["sha256"].startswith("cc3cb68c68cecdd7"))
        rr = RG.load(real)
        check("real file: 105687 rows, 49 languages", len(rr) == 105687 and len({r['lang'] for r in rr}) == 49)
        g2r = RG.g2(rr, (0.0, 0.50))
        check("real file: io mean 2.257 at t=0 and 3.531 at t=0.50",
              abs(g2r[0.0]["io_mean"] - 2.257) < 0.001 and abs(g2r[0.50]["io_mean"] - 3.531) < 0.001)
        sm = RG.g3_summary(RG.g3(rr, "io"))
        check("real file: tail ratio > 1 in 49 of 49", sm["tail_ratio_over_1"] == 49)
    else:
        print("  (real dataset not present at RHYTHM48_CSV; pinned checks skipped, not failed)")

    # ---- CLI and screen
    for mod in ("removal_closure.py", "rhythm_gaps.py"):
        rc = subprocess.run([sys.executable, os.path.join(HERE, mod), "--selftest"], capture_output=True).returncode
        check("%s refuses --selftest with rc 2" % mod, rc == 2)
    out_u = RM.render(None)
    out_f = RM.render(wt)
    out_g = RG.render(None)
    check("unfilled render screens clean", not no_severity.hits(out_u))
    check("constructed render screens clean", not no_severity.hits(out_f))
    check("gaps unfilled render screens clean", not no_severity.hits(out_g))
    check("screen fires on a planted word", bool(no_severity.hits(out_f + "\nthis is wrong\n")))
    check("every [CHOICE] printed", all("[CHOICE %d]" % i in out_u for i in (1, 2, 3, 4)))
    src = open(os.path.join(HERE, "removal_closure.py"), encoding="utf-8").read()
    check("no author section", "Author" not in src)

    sd = os.path.join(HERE, "samples")
    with open(os.path.join(sd, "constructed_rows.csv"), "w", encoding="utf-8") as fh:
        fh.write(to_csv(world()))
    with open(os.path.join(sd, "render_constructed.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_f)
    with open(os.path.join(sd, "render_unfilled.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out_u)
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
