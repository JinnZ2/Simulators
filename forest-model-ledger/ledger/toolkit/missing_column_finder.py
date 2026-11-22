# SPDX-License-Identifier: CC0-1.0
"""missing_column_finder: does residual spread cluster by something no
recorded column carries?  EXPLORATORY.  It scores nothing and tests no
prediction; every reading it prints is DERIVED.

    python3 ledger/toolkit/missing_column_finder.py --gate
    python3 ledger/toolkit/missing_column_finder.py run SOURCE_CSV

Steps (work order of 2026-11-22):
  a  residual spread against every recorded column, one at a time
  b  share of spread each column explains, alone and together
  c  on what is left: grouping patterns by Author (lab), region (lat/long
     bins), Year, Species, Family
  d  a grouping that explains spread no column does = MISSING COLUMN
     candidate, with its shape and an expiry_condition

What is imported and what is new:
  holdout/phase_b.py  _wls (the weighted slope fit) and dummy (the 0/1
                      coding), unchanged.  One-column fits use them.
  new here            the intercept-only between-row variance (phase_b only
                      has the one-moderator form), the all-columns fit, the
                      grouping shares and their permutation nulls.

Spread = weighted sum of squares of rr about its weighted mean, weights
1/(var + tau2_0), tau2_0 from the intercept-only fit.  One weight vector
for every column so the shares sit on one scale.

Three grouping tests, each with the null that fits its nesting:
  lab             rows by Author; null = residuals shuffled across rows
  between-study   study mean residuals by the study's modal label; null =
                  study means shuffled across studies
  within-study    residuals minus their study mean, by label; null =
                  residuals shuffled inside each study
A grouping constant inside every study (Year) has no within-study test.
Author is only read by the lab test.  Reading region, Year, Species or
Family at row level would count the lab spread a second time, so they are
never read that way.

FLAG rule (hand-set, fitted to nothing): observed share above every one of
N_PERM null shares AND observed minus null mean >= MIN_EXCESS.
"""
import csv
import hashlib
import io
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "holdout"))

import phase_b  # noqa: E402

BINARY = {
    "Experimental.setting": ("Greenhouse", "Field"), "Approach": ("Self-Sterilized", "Self-Other"),
    "Phase1.culti": ("Monoculture", "Community"), "SoilTp": ("Whole soil", "Inoculum"),
    "Life.form": ("Woody", "Nonwoody"), "F.H": ("Greenhouse", "Field"),
    "Sp.origin": ("Non-native", "Native"),
}
NUMERIC = ["Phase2.time", "MAT", "MAP", "AI", "Latitude.abs"]
COLUMNS = ["Experimental.setting", "Phase2.time", "Approach", "Phase1.culti", "SoilTp",
           "Life.form", "F.H", "Sp.origin", "MAT", "MAP", "AI", "Latitude.abs"]
GROUPINGS = ["Author", "region", "Year", "Species", "Family"]
REGION_DEG = 20            # lat/long bin width, degrees
N_PERM = 499
MIN_EXCESS = 0.02
PERM_SEED = 20261122
SOURCE_SHA = "bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c"
CUTOFF_YEAR = 2018
EXPIRY = {
    "Author": "a per-study methods table joined on Author: soil source and storage, "
              "sterilisation method, pot volume, inoculum fraction, watering and light regime",
    "region": "site covariates beyond MAT, MAP and AI joined on coordinates: soil pH, "
              "texture, total N and P, land-use history",
    "Year": "method-era fields per study: protocol family, sterilisation method and "
            "response metric as they changed over publication years",
    "Species": "species traits joined on Species: mycorrhizal type, N-fixing status, "
               "growth rate, seed mass",
    "Family": "lineage traits joined on Family: mycorrhizal type, N-fixing status, "
              "a phylogeny for the sampled families",
}


def _num(s):
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def _xfun(col):
    if col in BINARY:
        return phase_b.dummy(col, *BINARY[col])
    return lambda r: _num(r[col])


def _region(r):
    la, lo = _num(r.get("Latitude")), _num(r.get("Longitude"))
    if la is None or lo is None:
        return None
    return "lat%+04d lon%+04d" % (math.floor(la / REGION_DEG) * REGION_DEG,
                                  math.floor(lo / REGION_DEG) * REGION_DEG)


def _label(r, g):
    if g == "region":
        return _region(r)
    v = r.get(g)
    return v if v not in (None, "", "NA") else None


def tau2_intercept(y, v):
    """Method-of-moments between-row variance, intercept only."""
    w = 1.0 / v
    ym = np.sum(w * y) / np.sum(w)
    q = np.sum(w * (y - ym) ** 2)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    return max(0.0, (q - (len(y) - 1)) / c)


def _sst(y, w):
    return float(np.sum(w * (y - np.sum(w * y) / np.sum(w)) ** 2))


def eta2(e, w, codes, ngroups):
    """Weighted between-group share of the spread of e."""
    sw = np.bincount(codes, weights=w, minlength=ngroups)
    swe = np.bincount(codes, weights=w * e, minlength=ngroups)
    m = np.sum(w * e) / np.sum(w)
    ok = sw > 0
    between = np.sum(sw[ok] * (swe[ok] / sw[ok] - m) ** 2)
    total = np.sum(w * (e - m) ** 2)
    return float(between / total) if total > 0 else 0.0


def _codes(labels):
    names = sorted(set(labels))
    ix = {n: i for i, n in enumerate(names)}
    return np.array([ix[x] for x in labels]), names


def _verdict(obs, null):
    null = np.array(null)
    flag = bool(obs > null.max() and obs - null.mean() >= MIN_EXCESS)
    return {"share": obs, "null_mean": float(null.mean()), "null_max": float(null.max()),
            "excess": obs - float(null.mean()), "flag": flag}


def analyse(rows, perm_seed=PERM_SEED, n_perm=N_PERM):
    base = []
    for r in rows:
        y, v = _num(r["rr"]), _num(r["var"])
        if y is None or v is None or not v > 0:
            continue
        base.append((r, y, v))
    y = np.array([b[1] for b in base])
    v = np.array([b[2] for b in base])
    t0 = tau2_intercept(y, v)
    w = 1.0 / (v + t0)
    out = {"rows": len(base), "studies": len({b[0]["Author"] for b in base}),
           "tau2_intercept": float(t0), "columns": {}, "groupings": {}, "candidates": []}

    # a, b: one column at a time (phase_b._wls), on the rows where it is recorded
    X = {}
    for col in COLUMNS:
        f = _xfun(col)
        x = np.array([np.nan if f(b[0]) is None else f(b[0]) for b in base], dtype=float)
        X[col] = x
        ok = ~np.isnan(x)
        if ok.sum() < 3 or np.ptp(x[ok]) == 0:
            out["columns"][col] = {"share_alone": None, "rows": int(ok.sum()), "slope": None,
                                   "state": "not checkable (no variation on this side)"}
            continue
        slope, icpt = phase_b._wls(x[ok], y[ok], w[ok])
        sse = float(np.sum(w[ok] * (y[ok] - icpt - slope * x[ok]) ** 2))
        out["columns"][col] = {"share_alone": 1.0 - sse / _sst(y[ok], w[ok]),
                               "rows": int(ok.sum()), "slope": float(slope), "state": "fitted"}

    # b: all columns together, complete rows only
    used = [c for c in COLUMNS if out["columns"][c]["state"] == "fitted"]
    M = np.column_stack([X[c] for c in used])
    full = ~np.isnan(M).any(axis=1)
    A = np.column_stack([np.ones(full.sum()), M[full]])
    sw = np.sqrt(w[full])
    beta, *_ = np.linalg.lstsq(A * sw[:, None], y[full] * sw, rcond=None)
    e = y[full] - A @ beta
    wf = w[full]
    rws = [b[0] for b, k in zip(base, full) if k]
    together = 1.0 - float(np.sum(wf * e ** 2)) / _sst(y[full], wf)
    out["together"] = {"share": together, "left": 1.0 - together, "rows": int(full.sum()),
                       "columns_used": used, "rank": int(np.linalg.matrix_rank(A))}

    # c: grouping patterns on what is left
    rng = np.random.default_rng(perm_seed)
    n = len(e)
    scode, snames = _codes([r["Author"] for r in rws])
    S = len(snames)
    s_w = np.bincount(scode, weights=wf, minlength=S)
    s_m = np.bincount(scode, weights=wf * e, minlength=S) / s_w
    e_in = e - s_m[scode]
    order0 = np.argsort(scode, kind="stable")

    lab = _verdict(eta2(e, wf, scode, S),
                   [eta2(e[p], wf[p], scode, S) for p in (rng.permutation(n) for _ in range(n_perm))])
    out["groupings"]["Author"] = {"groups": S, "lab": lab, "between_study": None, "within_study": None}

    for g in GROUPINGS[1:]:
        labels = [_label(r, g) for r in rws]
        have = np.array([x is not None for x in labels])
        rec = {"rows_labelled": int(have.sum()), "between_study": None, "within_study": None, "lab": None}
        if have.sum() < 3:
            out["groupings"][g] = dict(rec, groups=0)
            continue
        gcode_all, gnames = _codes([x if x is not None else "\0" for x in labels])
        G = len(gnames)
        rec["groups"] = len({x for x in labels if x is not None})
        # between-study: study means by the study's modal label
        modal = np.full(S, -1)
        for s in range(S):
            m = have & (scode == s)
            if m.any():
                modal[s] = np.bincount(gcode_all[m], weights=wf[m], minlength=G).argmax()
        ks = modal >= 0
        if ks.sum() >= 3 and len(set(modal[ks])) > 1:
            sm, swt, mc = s_m[ks], s_w[ks], modal[ks]
            null = []
            for _ in range(n_perm):
                p = rng.permutation(len(sm))
                null.append(eta2(sm[p], swt[p], mc, G))
            rec["between_study"] = _verdict(eta2(sm, swt, mc, G), null)
        # within-study: demeaned residuals by label, shuffled inside each study
        varies = any(len(set(gcode_all[have & (scode == s)])) > 1 for s in range(S))
        if varies:
            obs = eta2(e_in[have], wf[have], gcode_all[have], G)
            null = []
            for _ in range(n_perm):
                r_ = np.lexsort((rng.random(n), scode))
                ep, wp = np.empty(n), np.empty(n)
                ep[order0], wp[order0] = e_in[r_], wf[r_]
                null.append(eta2(ep[have], wp[have], gcode_all[have], G))
            rec["within_study"] = _verdict(obs, null)
        else:
            rec["within_study"] = "nested in Author (constant inside every study)"
        # shape: largest group means on the test that flagged
        rec["top"] = []
        gw = np.bincount(gcode_all[have], weights=wf[have], minlength=G)
        gm = np.bincount(gcode_all[have], weights=(wf * e)[have], minlength=G) / np.where(gw > 0, gw, 1)
        gn = np.bincount(gcode_all[have], minlength=G)
        for i in sorted(range(G), key=lambda i: -abs(gm[i]) * (gn[i] >= 20))[:3]:
            if gn[i] >= 20:
                rec["top"].append((gnames[i].encode("ascii", "replace").decode(), float(gm[i]), int(gn[i])))
        out["groupings"][g] = rec

    for g in GROUPINGS:
        rec = out["groupings"][g]
        hits = [k for k in ("lab", "between_study", "within_study")
                if isinstance(rec.get(k), dict) and rec[k]["flag"]]
        if hits:
            out["candidates"].append({
                "clusters_by": g, "tests_flagged": hits, "groups": rec["groups"],
                "excess": {k: rec[k]["excess"] for k in hits},
                "top": rec.get("top", []), "expiry_condition": EXPIRY[g]})
    return out


# ------------------------------------------------------------------- printing
def _v(d):
    if d is None:
        return "not checkable"
    if isinstance(d, str):
        return d
    return "share %.3f  null mean %.3f  null max %.3f  excess %+.3f  %s" % (
        d["share"], d["null_mean"], d["null_max"], d["excess"], "FLAG" if d["flag"] else "-")


def render(name, o):
    L = ["%s: %d rows, %d studies, tau2 %.4f" % (name, o["rows"], o["studies"], o["tau2_intercept"]),
         "  column                 share alone   slope      rows"]
    for c in COLUMNS:
        k = o["columns"][c]
        if k["share_alone"] is None:
            L.append("  %-22s %s" % (c, k["state"]))
        else:
            L.append("  %-22s %8.4f   %+9.4f  %5d" % (c, k["share_alone"], k["slope"], k["rows"]))
    t = o["together"]
    L.append("  all %d columns together: share %.4f, left %.4f (%d complete rows)"
             % (len(t["columns_used"]), t["share"], t["left"], t["rows"]))
    L.append("  grouping patterns on what is left:")
    for g in GROUPINGS:
        r = o["groupings"][g]
        L.append("    %-8s groups %4d" % (g, r["groups"]))
        if g == "Author":
            L.append("      lab             %s" % _v(r["lab"]))
        else:
            L.append("      between-study   %s" % _v(r["between_study"]))
            L.append("      within-study    %s" % _v(r["within_study"]))
    L.append("  MISSING COLUMN candidates: %s"
             % (", ".join("%s (%s)" % (c["clusters_by"], "+".join(c["tests_flagged"]))
                          for c in o["candidates"]) or "none"))
    return "\n".join(L)


# ----------------------------------------------------------------------- gate
def synthetic(seed, planted=None, effect_sd=0.3):
    """Rows shaped like the dataset. planted in (None, 'Family', 'region',
    'Author'): a hidden effect tied to that grouping and to no column."""
    rng = np.random.default_rng(seed)
    fams = ["F%02d" % i for i in range(12)]
    fam_eff = rng.normal(0, effect_sd, len(fams))
    reg_eff, lab_eff = {}, {}
    rows = []
    for s in range(60):
        lat, lon = rng.uniform(-40, 60), rng.uniform(-120, 140)
        year = int(rng.integers(2000, 2019))
        study = {"Author": "S%02d" % s, "Year": str(year), "Latitude": "%.2f" % lat,
                 "Longitude": "%.2f" % lon, "Latitude.abs": "%.2f" % abs(lat),
                 "MAT": "%.2f" % rng.uniform(0, 25), "MAP": "%.0f" % rng.uniform(200, 2000),
                 "AI": "%.3f" % rng.uniform(0.1, 1.5),
                 "Experimental.setting": rng.choice(["Greenhouse", "Field"]),
                 "F.H": rng.choice(["Greenhouse", "Field"]),
                 "Phase1.culti": rng.choice(["Monoculture", "Community"])}
        reg = _region(study)
        reg_eff.setdefault(reg, rng.normal(0, effect_sd))
        lab_eff[s] = rng.normal(0, effect_sd)
        for _ in range(int(rng.integers(5, 40))):
            f = int(rng.integers(0, len(fams)))
            var = rng.uniform(0.01, 0.1)
            mu = {None: 0.0, "Family": fam_eff[f], "region": reg_eff[reg], "Author": lab_eff[s]}[planted]
            rows.append(dict(study, Family=fams[f], Species="%s_sp%d" % (fams[f], rng.integers(0, 4)),
                             Approach=rng.choice(["Self-Sterilized", "Self-Other"]),
                             SoilTp=rng.choice(["Whole soil", "Inoculum"]),
                             **{"Life.form": rng.choice(["Woody", "Nonwoody"]),
                                "Sp.origin": rng.choice(["Non-native", "Native"]),
                                "Phase2.time": "%.2f" % rng.uniform(1, 24)},
                             rr="%.6f" % (mu + rng.normal(0, math.sqrt(var))), var="%.6f" % var))
    return rows


def gate(seeds=(0, 1, 2, 3, 4), verbose=True):
    ok = True
    lines = []
    for planted in ("Family", "region", "Author"):
        got = 0
        for sd in seeds:
            o = analyse(synthetic(sd, planted), perm_seed=1000 + sd)
            names = [c["clusters_by"] for c in o["candidates"]]
            got += planted in names
        lines.append("known-answer, hidden variable tied to %-7s flagged on %d of %d seeds  %s"
                     % (planted + ":", got, len(seeds), "PASS" if got == len(seeds) else "FAIL"))
        ok &= got == len(seeds)
    fp, tests = 0, 0
    for sd in seeds:
        o = analyse(synthetic(sd, None), perm_seed=1000 + sd)
        fp += len(o["candidates"])
        for g in GROUPINGS:
            tests += sum(isinstance(o["groupings"][g].get(k), dict)
                         for k in ("lab", "between_study", "within_study"))
    lines.append("null-harness, pure noise: %d candidates over %d seeds (%d tests)  %s"
                 % (fp, len(seeds), tests, "PASS" if fp == 0 else "FAIL"))
    ok &= fp == 0
    lines.append("GATE %s" % ("PASS" if ok else "FAIL"))
    if verbose:
        print("\n".join(lines))
    return ok, lines


# ------------------------------------------------------------------------ run
def _rows(data):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8", errors="replace"), newline="")))


def main():
    a = sys.argv[1:]
    if a == ["--gate"]:
        raise SystemExit(0 if gate()[0] else 1)
    if len(a) == 2 and a[0] == "run":
        print("gate first:")
        if not gate()[0]:
            raise SystemExit("GATE FAIL: not run on real data")
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = _rows(raw)
        anchor = [r for r in allrows if int(r["Year"]) <= CUTOFF_YEAR]
        hold = [r for r in allrows if int(r["Year"]) > CUTOFF_YEAR]
        res = {}
        for name, rows in (("anchor (<= 2018)", anchor), ("holdout (> 2018)", hold), ("pooled", allrows)):
            res[name] = analyse(rows)
            print()
            print(render(name, res[name]))
        print("\nsame candidates on both sides?")
        ca = {c["clusters_by"]: c["tests_flagged"] for c in res["anchor (<= 2018)"]["candidates"]}
        ch = {c["clusters_by"]: c["tests_flagged"] for c in res["holdout (> 2018)"]["candidates"]}
        for g in GROUPINGS:
            print("  %-8s anchor %-28s holdout %-28s %s"
                  % (g, "+".join(ca.get(g, [])) or "-", "+".join(ch.get(g, [])) or "-",
                     "both" if g in ca and g in ch else ("one side" if g in ca or g in ch else "neither")))
        print("\ncandidate shapes (pooled):")
        for c in res["pooled"]["candidates"]:
            print("  clusters by %s; tests %s; %d groups; excess %s"
                  % (c["clusters_by"], "+".join(c["tests_flagged"]), c["groups"],
                     ", ".join("%s %+.3f" % kv for kv in c["excess"].items())))
            for lab, m, k in c["top"]:
                print("      largest group mean residual: %-22s %+.3f (%d rows)" % (lab, m, k))
            print("      expiry_condition: %s" % c["expiry_condition"])
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
