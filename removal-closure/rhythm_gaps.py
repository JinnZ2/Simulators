#!/usr/bin/env python3
"""rhythm_gaps -- the order's ATTACHED GAPS run where they can be run.

The order attaches seven questions (G1-G7) about an open dataset,
github.com/LSBurchardt/Rhythm_across_48_languages, "raised without
having run the code". The repository is on a host this environment can
reach, so this module reads its intermediate table
(`unsplit_ioi_data_for_rhythm_analysis_including_meta_data_run_Oct24.csv`,
one row per pause-bounded unit: start, end, trailing pause, unit
duration, speech duration, language) and computes the two gaps that
need only that table:

    G2  PAUSE THRESHOLD   the upstream split has no lower threshold: any
        annotated pause ends a unit (the floor in the data is printed).
        Units are re-merged here at thresholds t -- a unit whose trailing
        pause is shorter than t is joined to the next unit in the same
        file / speaker / part -- and the mean and median of the unit
        duration and of the speech-run duration are reported at each t.
    G3  DISTRIBUTION SHAPE   per language: n, median, mode in 0.05 s
        bins, CV, right-tail ratio (p95 - median) / (median - p05), on
        the unit duration the pipeline analyses and on the speech run.

and states, from the repository's own scripts, why the others do not
run here: G4 needs word-level intervals the repository does not carry
(its first script reads them from an external DoReCo path and writes
only the aggregated units); G5 needs a language -> country join the
repository performs by geocoding, which is not in the table; G1, G6 and
G7 are reading questions about the paper's comparison, not about the
CSV, and G7's one number is arithmetic and is printed.

The dataset is NOT checked into this repository (third-party, 16 MB);
the render carries the file's size and sha256 and the upstream commit
so a re-obtained copy can be checked. Every number here is a property
of that file under this module's operations. Nothing is a claim about
any language, speaker, or species.

CC0. stdlib only. Parses under Python 3.9.
"""

import csv
import hashlib
import math
import os
import statistics
import sys
from collections import Counter, defaultdict

THRESHOLDS = (0.0, 0.15, 0.25, 0.35, 0.50)   # 0.0 = the pipeline as delivered
BIN = 0.05
UPSTREAM = "github.com/LSBurchardt/Rhythm_across_48_languages"


def file_facts(path):
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            n += len(chunk)
    return {"bytes": n, "sha256": h.hexdigest()}


def load(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append({
                "file": r["file"], "speaker": r["speaker"], "part": r["part"],
                "io_unit": int(float(r["io_unit"])),   # R writes 1e+05 for 100000
                "start": float(r["start_time"]), "end": float(r["end_time"]),
                "pause": float(r["pause_duration"]),
                "io": float(r["io_duration"]),
                "speech": float(r["sprach_dauer"]),
                "lang": r["glottocode"],
            })
    return rows


# ------------------------------------------------------------ facts

def pause_floor(rows):
    p = sorted(r["pause"] for r in rows)
    n = len(p)
    return {"min": p[0], "p1": p[n // 100], "p5": p[n // 20],
            "median": statistics.median(p), "mean": statistics.mean(p), "max": p[-1]}


def stated_in_script():
    """Two numbers the upstream analysis script states in comments
    (`04_plots_analysis_revision.R`: '#1.43 sec' for the speech run,
    '# 0.83 sec' for the pause). Carried here as the script's statement;
    recomputed below."""
    return {"speech_mean": 1.43, "pause_mean": 0.83}


# --------------------------------------------------------------- G2

def merge_at(rows, t):
    """Re-merge consecutive units within (file, speaker, part) when the
    trailing pause is shorter than t. Returns merged units with io
    (onset-to-onset, including the final trailing pause) and speech
    (sum of speech plus the pauses absorbed). t = 0 returns the units as
    delivered, since no pause is shorter than zero."""
    groups = defaultdict(list)
    for r in rows:
        groups[(r["file"], r["speaker"], r["part"])].append(r)
    out = []
    for key, rs in groups.items():
        rs = sorted(rs, key=lambda r: r["start"])
        cur = None
        for r in rs:
            if cur is None:
                cur = {"lang": r["lang"], "io": r["io"], "speech": r["speech"], "pause": r["pause"]}
            else:
                cur["io"] += r["io"]
                cur["speech"] += r["speech"] + cur["pause"]
                cur["pause"] = r["pause"]
            if not (r["pause"] < t):
                out.append(cur)
                cur = None
        if cur is not None:
            out.append(cur)
    return out


def g2(rows, thresholds=THRESHOLDS):
    res = {}
    for t in thresholds:
        m = merge_at(rows, t)
        io = [u["io"] for u in m]
        sp = [u["speech"] for u in m]
        res[t] = {"units": len(m), "io_mean": statistics.mean(io), "io_median": statistics.median(io),
                  "speech_mean": statistics.mean(sp), "speech_median": statistics.median(sp)}
    return res


def g2_monotone(res):
    ts = sorted(res)
    return all(res[ts[i]]["io_mean"] <= res[ts[i + 1]]["io_mean"] + 1e-12 for i in range(len(ts) - 1))


# --------------------------------------------------------------- G3

def _pct(sorted_vals, q):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * q
    f = math.floor(k)
    c = min(f + 1, len(sorted_vals) - 1)
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def shape(values, bin_width=BIN):
    """median, mode in fixed bins (bin lower edge), CV, right-tail ratio.
    Tail ratio is None when median == p05 (zero denominator)."""
    v = sorted(values)
    n = len(v)
    if n == 0:
        return {"n": 0, "median": None, "mode": None, "cv": None, "tail_ratio": None}
    med = statistics.median(v)
    mean = statistics.mean(v)
    sd = statistics.pstdev(v) if n > 1 else 0.0
    bins = Counter(math.floor(x / bin_width) for x in v)
    mode_bin = min((b for b, c in bins.items() if c == max(bins.values())))
    p05, p95 = _pct(v, 0.05), _pct(v, 0.95)
    den = med - p05
    tail = None if den <= 0 else (p95 - med) / den
    return {"n": n, "median": med, "mode": mode_bin * bin_width,
            "cv": None if mean == 0 else sd / mean, "tail_ratio": tail}


def g3(rows, field="io"):
    by = defaultdict(list)
    for r in rows:
        by[r["lang"]].append(r[field])
    return {lang: shape(vals) for lang, vals in sorted(by.items())}


def g3_summary(per_lang):
    def rng(key):
        xs = [v[key] for v in per_lang.values() if v[key] is not None]
        return (min(xs), max(xs), statistics.median(xs)) if xs else (None, None, None)
    return {"languages": len(per_lang),
            "median": rng("median"), "mode": rng("mode"), "cv": rng("cv"), "tail_ratio": rng("tail_ratio"),
            "tail_ratio_over_1": sum(1 for v in per_lang.values()
                                     if v["tail_ratio"] is not None and v["tail_ratio"] > 1.0)}


# ------------------------------------------------- the gaps that do not run

NOT_RUN = {
    "G1": "reading question about the paper's animal rows; not in the CSV",
    "G4": "word-level intervals are not in the repository: 01_prep reads them from an "
          "external DoReCo path and writes only the pause-bounded units",
    "G5": "the height covariate joins on country, which 03_post_metadata obtains by "
          "geocoding coordinates; no country column is in the table",
    "G6": "reading question about sound-production mechanisms; not in the CSV",
    "G7": "reading question; its one number is arithmetic and is printed below",
}


# ---------------------------------------------------------------- render

def _f(x, d=3):
    return "--" if x is None else ("%%.%df" % d) % x


def render(path=None, commit=None):
    out = []
    w = out.append
    w("rhythm_gaps -- the attached gaps run where they can be run")
    w("")
    if path is None:
        w("CSV: not supplied. Pass --csv PATH to the repository's intermediate table.")
        w("  upstream: %s" % UPSTREAM)
        for g, why in NOT_RUN.items():
            w("  %s  NOT RUN  %s" % (g, why))
        w("  G2, G3  NOT RUN  (no CSV)")
        return "\n".join(out) + "\n"
    ff = file_facts(path)
    rows = load(path)
    w("CSV: %s" % os.path.basename(path))
    w("  bytes %d  sha256 %s  upstream %s%s" % (
        ff["bytes"], ff["sha256"][:16], UPSTREAM, ("  commit %s" % commit[:12]) if commit else ""))
    w("  rows %d  languages %d" % (len(rows), len({r["lang"] for r in rows})))
    w("")
    pf = pause_floor(rows)
    st = stated_in_script()
    w("PAUSE FLOOR  min %.3f  p1 %.3f  p5 %.3f  median %.3f  mean %.3f  max %.3f s" % (
        pf["min"], pf["p1"], pf["p5"], pf["median"], pf["mean"], pf["max"]))
    w("  the upstream split ends a unit at every annotated pause; no lower threshold")
    w("  is applied in the repository's scripts, so the floor is the annotation's.")
    sp_mean = statistics.mean(r["speech"] for r in rows)
    w("  script comment states speech mean %.2f / pause mean %.2f; recomputed %.3f / %.3f" % (
        st["speech_mean"], st["pause_mean"], sp_mean, pf["mean"]))
    w("")
    r2 = g2(rows)
    w("G2  re-merge at threshold t (trailing pause < t joins the next unit)")
    w("  %-5s | units  | io mean | io median | speech mean | speech median   (speech: absorbed pauses < t included)" % "t")
    for t in THRESHOLDS:
        x = r2[t]
        w("  %-5s | %6d | %s | %s | %s | %s" % (
            _f(t, 2), x["units"], _f(x["io_mean"]), _f(x["io_median"]),
            _f(x["speech_mean"]), _f(x["speech_median"])))
    base, top = r2[THRESHOLDS[0]], r2[THRESHOLDS[-1]]
    w("  io mean moves %.3f -> %.3f (x%.2f) from t=0 to t=%.2f; monotone non-decreasing: %s" % (
        base["io_mean"], top["io_mean"], top["io_mean"] / base["io_mean"], THRESHOLDS[-1],
        g2_monotone(r2)))
    w("  the direction is fixed by construction (merging only lengthens units); the")
    w("  size of the move is the measurement.")
    w("")
    for field, label in (("io", "unit duration, onset to onset (the analysed quantity)"),
                         ("speech", "speech run, pause excluded")):
        pl = g3(rows, field)
        sm = g3_summary(pl)
        w("G3  per-language shape on %s, %d languages" % (label, sm["languages"]))
        w("  %-11s | min   | max   | median across languages" % "stat")
        for k in ("median", "mode", "cv", "tail_ratio"):
            lo, hi, md = sm[k]
            w("  %-11s | %s | %s | %s" % (k, _f(lo), _f(hi), _f(md)))
        w("  languages with right-tail ratio > 1: %d of %d" % (sm["tail_ratio_over_1"], sm["languages"]))
        w("  per language:  glottocode | n | median | mode | cv | tail_ratio")
        for lang, v in pl.items():
            w("    %-10s | %5d | %s | %s | %s | %s" % (
                lang, v["n"], _f(v["median"]), _f(v["mode"], 2), _f(v["cv"]), _f(v["tail_ratio"])))
        w("")
    w("NOT RUN HERE")
    for g, why in NOT_RUN.items():
        w("  %s  %s" % (g, why))
    io_med = statistics.median(r["io"] for r in rows)
    w("  G7  1 / median unit duration = 1 / %.3f s = %.3f Hz" % (io_med, 1.0 / io_med))
    w("")
    w("Every number above is a property of the named file under this module's")
    w("operations. Nothing is a statement about any language, speaker or species.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("rhythm_gaps.py has no checks of its own; they live in selftest_rmc.py.\n")
        return 2
    path = argv[argv.index("--csv") + 1] if "--csv" in argv else None
    commit = argv[argv.index("--commit") + 1] if "--commit" in argv else None
    sys.stdout.write(render(path, commit))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
