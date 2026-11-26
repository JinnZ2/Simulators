# SPDX-License-Identifier: CC0-1.0
"""denominator_sorter: sort studies by what they measured against.
EXPLORATORY.  It fits nothing, scores nothing and tests no prediction.

    python3 ledger/toolkit/denominator_sorter.py --gate
    python3 ledger/toolkit/denominator_sorter.py run SOURCE_CSV
    python3 ledger/toolkit/denominator_sorter.py addendum SOURCE_CSV
    python3 ledger/toolkit/denominator_sorter.py power SOURCE_CSV
    python3 ledger/toolkit/denominator_sorter.py dropnull SOURCE_CSV
    python3 ledger/toolkit/denominator_sorter.py slots SOURCE_CSV
    python3 ledger/toolkit/denominator_sorter.py strata SOURCE_CSV

A study's DENOMINATOR SIGNATURE is read from seven recorded columns:
    Experimental.setting, Phase2.time (binned), Approach (control type),
    Phase1.culti, SoilTp, Phase2.grow, Response (what was measured)
Per field the signature holds the SET of values the study's rows carry,
so a study that ran both a greenhouse and a field arm reads
"Field+Greenhouse" and is not forced onto one side.  A field with no
recorded value on any row reads NOT RECORDED; nothing is imputed.  A study
with some rows recorded and some not carries both ("... +NOT RECORDED").

Studies with IDENTICAL signatures form a scope group.  A study matching no
other is "no common denominator": kept and listed, never dropped.

RULE (work order of 2026-11-22): comparisons and pooling only WITHIN a
group.  A difference BETWEEN groups is a candidate scope effect, never a
contradiction.  may_pool() is that rule as code; nothing in this file
compares effect sizes across or within groups.

The Phase2.time bins are hand-set (months): <=3, 3-6, 6-12, >12.  A
different binning gives different groups; that is stated in every report.

ADDENDUM (2026-11-22):
  slots   every study also carries three EMPTY slots: lab_institution,
          lab_country, governance_regime (permits, sterilization or
          biosafety rules, funding mandates).  All read NOT RECORDED; the
          source has no such column and nothing is imputed.  They take no
          part in the match: two unknowns are not a match.  The source
          README defines "Latitude: Latitude (degree)" and "Longitude:
          Longitude (degree)" and says nothing about what they locate;
          they are not used to fill the slots.
  lab     inside each scope group, missing_column_finder's Author (lab)
          test: share of the group's spread that sits between studies,
          against rows shuffled across the group.  The spread is taken
          about the GROUP MEAN, with no column fitted first: in a group of
          k studies, k-1 study-level columns (MAT, MAP, AI, latitude)
          would absorb every between-lab difference by construction.  A
          flag tags the group "signature-matched, protocol-unmatched".

AMENDED ADDENDUM (2026-11-22, replaces the first):
  arms    UNIT = study x arm.  An arm is one value combination of the seven
          fields present in a study's rows, so every row sits in exactly
          one arm and an arm signature has single values.  The study-level
          run is kept as is; both are reported.  At arm level a group
          needs units from at least two studies.
  drop    for each field: leave it out of the signature, regroup, report.
          The signature itself is not changed.  Within-group residual
          spread = weighted mean square of the finder's all-columns
          residuals about each group's mean, with a group-count
          correction, read on the SAME rows before and after the drop
          (the rows grouped under the full signature).  A drop that does
          not raise it is marked "splits without moving outcome".
  power   the lab test runs only on groups with >= MIN_LAB_STUDIES studies
          (chosen, no external source); smaller groups read
          "underpowered, not tested".

POWER CURVE (2026-11-22, after the lab gate failed twice):
  random planted effects can fall near zero; pass/fail at one size cannot
  separate tool failure from low power.  So the lab test is characterised
  on synthetic groups instead: k studies of 15 rows, row noise as in the
  failed gate, lab effects FIXED (equally spaced, centred, scaled to the
  stated sd), 50 seeds per cell, flag rule unchanged.  RULE, declared
  before any real group is read: the real lab test runs only on group
  sizes with detection >= 0.8 at sd 0.2 and false-flag <= 0.05; other
  groups read "underpowered at this size", tag NOT RECORDED.  A real
  group of k studies is read at the largest tested size <= k.

INSTRUMENT SLOTS (2026-11-22): four more EMPTY slots on every study and
  arm, beside the three lab slots: instrument_manufacturer,
  instrument_model, calibration_date, measurement_method (how biomass or
  the response was measured: drying temperature and time, balance,
  scanner, and so on).  NOT RECORDED everywhere, never imputed, filled
  from each paper's methods section.  No slot takes part in matching
  until it is filled: two unknowns are not a match.

  A fifth, coordinate_meaning: what Latitude / Longitude locate.  The
  source README does not say.

APPROACH STRATA (2026-11-22, spent holdout, scores nothing): each Phase B
  moderator fit rerun inside Self-Other and inside Self-Sterilized, anchor
  and holdout, with phase_b.fit imported unchanged through phase_c.FITS.
  Approach defines the control soil, the denominator of rr; pooling across
  Approach mixes two measurands.  Cells under THIN_STUDIES studies read
  "thin".

FIELD-DROP NULL (2026-11-22, arm level, pooled):
  the first field-drop rule could only read "moves outcome" by
  construction (merging cannot lower within-group spread).  Replaced by a
  null: shuffle the field's values across arms (value counts kept), group
  on the signature with the shuffled field in it, then drop the field and
  record the same-rows spread rise.  DROP_SHUFFLES shuffles.  A real field
  "moves outcome" only if its real rise is above the 95th percentile of
  its own null rises; otherwise "not distinguishable from merging noise".

`run` and `--gate` use the standard library only.  `addendum` imports
missing_column_finder (numpy) and uses its eta2, tau2_intercept, _codes,
_verdict, _xfun and COLUMNS unchanged, with its FLAG rule and shuffle
count.  The all-columns residuals are recomputed here from those parts
and checked against the finder's own explained share before use.
"""
import csv
import hashlib
import io
import random
import sys

FIELDS = ["Experimental.setting", "Phase2.time", "Approach", "Phase1.culti",
          "SoilTp", "Phase2.grow", "Response"]
TIME_BINS = [(3.0, "<=3mo"), (6.0, "3-6mo"), (12.0, "6-12mo"), (float("inf"), ">12mo")]
NR = "NOT RECORDED"
SLOTS = ["lab_institution", "lab_country", "governance_regime"]
SLOT_EXPIRY = "filled from each paper's affiliations and methods"
INSTRUMENT_SLOTS = ["instrument_manufacturer", "instrument_model", "calibration_date",
                    "measurement_method"]
INSTRUMENT_EXPIRY = "filled from each paper's methods section"
OTHER_SLOTS = ["coordinate_meaning"]     # what Latitude / Longitude locate; README does not say
THIN_STUDIES = 5
MIN_SPARE_ROWS = 2      # lab test needs rows beyond one per study; else not checkable
MIN_LAB_STUDIES = 5     # power gate: chosen, no external source
SOURCE_SHA = "bb56ba5ac31b13be09cf3df42c1215b53255bb1eb3bb8a91838ab8cb4cb5c82c"
CUTOFF_YEAR = 2018


def _value(row, field):
    raw = row.get(field)
    if raw is None or raw.strip() in ("", "NA"):
        return NR
    if field != "Phase2.time":
        return raw.strip()
    try:
        t = float(raw)
    except ValueError:
        return NR
    if t != t:
        return NR
    return next(name for top, name in TIME_BINS if t <= top)


def signature(rows):
    """One study's rows -> tuple of 7 strings, one per field."""
    out = []
    for f in FIELDS:
        vals = {_value(r, f) for r in rows}
        order = [n for _, n in TIME_BINS] if f == "Phase2.time" else sorted(vals - {NR})
        out.append("+".join([v for v in order if v in vals] + ([NR] if NR in vals else [])))
    return tuple(out)


def slots(_rows):
    """The unfilled slots of one study or arm: three lab slots and four
    instrument slots.  Always NOT RECORDED here: the source carries no
    column for any of them.  None is part of the signature."""
    return {s: NR for s in SLOTS + INSTRUMENT_SLOTS + OTHER_SLOTS}


def may_pool(sig_a, sig_b):
    """The rule: pool or compare only inside one scope group."""
    return sig_a == sig_b


def sort_studies(rows):
    by_study = {}
    for r in rows:
        by_study.setdefault(r["Author"], []).append(r)
    by_sig = {}
    for study, rs in by_study.items():
        by_sig.setdefault(signature(rs), []).append((study, len(rs)))
    groups, singles = [], []
    for sig, members in by_sig.items():
        rec = {"signature": sig, "studies": sorted(m[0] for m in members),
               "n_studies": len(members), "n_rows": sum(m[1] for m in members)}
        (groups if len(members) > 1 else singles).append(rec)
    groups.sort(key=lambda g: (-g["n_studies"], -g["n_rows"], g["signature"]))
    singles.sort(key=lambda g: g["studies"][0])
    return {"studies": len(by_study), "rows": len(rows), "groups": groups, "singletons": singles,
            "studies_in_groups": sum(g["n_studies"] for g in groups),
            "rows_in_groups": sum(g["n_rows"] for g in groups),
            "fields_not_recorded": {f: sum(NR in s[i] for s in by_sig for _ in by_sig[s])
                                    for i, f in enumerate(FIELDS)}}


# ------------------------------------------------------------------- printing
def asc(s):
    return s.encode("ascii", "backslashreplace").decode()


def sig_text(sig):
    return " | ".join(sig)


def render(name, res, ids):
    L = ["%s: %d studies, %d rows -> %d scope groups holding %d studies (%d rows); "
         "%d studies with no common denominator"
         % (name, res["studies"], res["rows"], len(res["groups"]), res["studies_in_groups"],
            res["rows_in_groups"], len(res["singletons"])),
         "  id    studies   rows  signature"]
    for g in res["groups"]:
        L.append("  %-5s %5d  %6d  %s" % (ids[g["signature"]], g["n_studies"], g["n_rows"],
                                           sig_text(g["signature"])))
    nr = {f: n for f, n in res["fields_not_recorded"].items() if n}
    L.append("  studies with a field NOT RECORDED: %s"
             % (", ".join("%s %d" % kv for kv in nr.items()) or "none"))
    return "\n".join(L)


# -------------------------------------------------------- addendum: lab test
def lab_test(rows, perm_seed):
    """missing_column_finder's lab test on one scope group's rows, spread
    taken about the group mean."""
    import numpy as np
    import missing_column_finder as mcf
    keep = [(r, mcf._num(r["rr"]), mcf._num(r["var"])) for r in rows]
    keep = [k for k in keep if k[1] is not None and k[2] is not None and k[2] > 0]
    studies = sorted({k[0]["Author"] for k in keep})
    if len(studies) < 2 or len(keep) - len(studies) < MIN_SPARE_ROWS:
        return {"state": "not checkable", "rows": len(keep), "studies": len(studies)}
    y = np.array([k[1] for k in keep])
    v = np.array([k[2] for k in keep])
    w = 1.0 / (v + mcf.tau2_intercept(y, v))
    e = y - np.sum(w * y) / np.sum(w)
    code, names = mcf._codes([k[0]["Author"] for k in keep])
    rng = np.random.default_rng(perm_seed)
    null = []
    for _ in range(mcf.N_PERM):
        p = rng.permutation(len(e))
        null.append(mcf.eta2(e[p], w[p], code, len(names)))
    return dict(mcf._verdict(mcf.eta2(e, w, code, len(names)), null),
                state="tested", rows=len(keep), studies=len(studies))


def study_units(rows):
    by = {}
    for r in rows:
        by.setdefault(r["Author"], []).append(r)
    return {s: (signature(rs), s, rs) for s, rs in by.items()}


def arm_units(rows):
    by = {}
    for r in rows:
        by.setdefault((r["Author"], tuple(_value(r, f) for f in FIELDS)), []).append(r)
    return {"%s || %s" % (k[0], " | ".join(k[1])): (k[1], k[0], rs) for k, rs in by.items()}


def group_units(units, drop=None):
    """units: id -> (signature, study, rows).  A group = one signature held
    by units from at least two studies.  drop = index of a field left out."""
    by = {}
    for uid, (sig, study, rs) in units.items():
        key = sig if drop is None else sig[:drop] + sig[drop + 1:]
        by.setdefault(key, []).append(uid)
    groups, singles = {}, []
    for key, uids in by.items():
        if len({units[u][1] for u in uids}) >= 2:
            groups[key] = sorted(uids)
        else:
            singles += uids
    return groups, sorted(singles)


def _side(units, uid):
    return "anchor" if int(units[uid][2][0]["Year"]) <= CUTOFF_YEAR else "holdout"


def both_sides(units, drop=None):
    """Signatures that are groups on each side separately; units inside them."""
    ga, _ = group_units({u: v for u, v in units.items() if _side(units, u) == "anchor"}, drop)
    gh, _ = group_units({u: v for u, v in units.items() if _side(units, u) == "holdout"}, drop)
    keys = set(ga) & set(gh)
    return len(keys), sum(len(ga[k]) + len(gh[k]) for k in keys), sum(len(gh[k]) for k in keys)


def finder_residuals(rows):
    """Row id -> (residual, weight) from the finder's all-columns fit,
    rebuilt from its parts; the explained share must equal the finder's."""
    import numpy as np
    import missing_column_finder as mcf
    base = [(r, mcf._num(r["rr"]), mcf._num(r["var"])) for r in rows]
    base = [b for b in base if b[1] is not None and b[2] is not None and b[2] > 0]
    y = np.array([b[1] for b in base])
    v = np.array([b[2] for b in base])
    w = 1.0 / (v + mcf.tau2_intercept(y, v))
    X = np.array([[np.nan if mcf._xfun(c)(b[0]) is None else mcf._xfun(c)(b[0]) for c in mcf.COLUMNS]
                  for b in base], dtype=float)
    full = ~np.isnan(X).any(axis=1)
    A = np.column_stack([np.ones(full.sum()), X[full]])
    sw = np.sqrt(w[full])
    beta, *_ = np.linalg.lstsq(A * sw[:, None], y[full] * sw, rcond=None)
    e = y[full] - A @ beta
    share = 1.0 - float(np.sum(w[full] * e ** 2)) / mcf._sst(y[full], w[full])
    kept = [b[0] for b, k in zip(base, full) if k]
    return {id(r): (float(ei), float(wi)) for r, ei, wi in zip(kept, e, w[full])}, share


def within_spread(units, groups, resid, only=None):
    """Weighted mean square of residuals about group means, with a
    group-count correction.  only = set of row ids to read (same-rows rule)."""
    ss = sw = 0.0
    n = g = 0
    for uids in groups.values():
        pts = [resid[id(r)] for u in uids for r in units[u][2]
               if id(r) in resid and (only is None or id(r) in only)]
        if len(pts) < 2:
            continue
        tw = sum(p[1] for p in pts)
        m = sum(p[0] * p[1] for p in pts) / tw
        ss += sum(p[1] * (p[0] - m) ** 2 for p in pts)
        sw += tw
        n += len(pts)
        g += 1
    if n - g < 1 or sw <= 0:
        return None
    return ss / sw * n / (n - g)


def drop_table(units, resid):
    g0, s0 = group_units(units)
    common = {id(r) for uids in g0.values() for u in uids for r in units[u][2]}
    base = within_spread(units, g0, resid, common)
    out = [("(none)", len(g0), len(s0)) + both_sides(units) + (base, base, "-")]
    for i, f in enumerate(FIELDS):
        g, s = group_units(units, i)
        same = within_spread(units, g, resid, common)
        own = within_spread(units, g, resid)
        mark = "splits without moving outcome" if same is not None and same <= base else "moves outcome"
        out.append((f, len(g), len(s)) + both_sides(units, i) + (same, own, mark))
    return out


DROP_SHUFFLES = 200      # chosen, no external source
DROP_SEED = 20261122


def _rise(units, i, resid):
    """Same-rows spread rise when field i is left out of the signature."""
    g0, _ = group_units(units)
    common = {id(r) for uids in g0.values() for u in uids for r in units[u][2]}
    before = within_spread(units, g0, resid, common)
    g1, _ = group_units(units, i)
    after = within_spread(units, g1, resid, common)
    if before is None or after is None:
        return None
    return after - before


def drop_null(units, resid, shuffles=DROP_SHUFFLES, seed=DROP_SEED):
    out = []
    uids = sorted(units)
    for i, f in enumerate(FIELDS):
        real = _rise(units, i, resid)
        rng = random.Random(seed * 10 + i)
        null = []
        for _ in range(shuffles):
            vals = [units[u][0][i] for u in uids]
            rng.shuffle(vals)
            shuf = {u: (units[u][0][:i] + (v,) + units[u][0][i + 1:], units[u][1], units[u][2])
                    for u, v in zip(uids, vals)}
            r = _rise(shuf, i, resid)
            if r is not None:
                null.append(r)
        null.sort()
        p95 = null[min(len(null) - 1, int(round(0.95 * (len(null) - 1))))] if null else None
        mark = ("not checkable" if real is None or p95 is None else
                "moves outcome" if real > p95 else "not distinguishable from merging noise")
        out.append((f, real, sum(null) / len(null) if null else None, p95,
                    sum(x >= real for x in null) / len(null) if null and real is not None else None,
                    len(null), mark))
    return out


def lab_table(units, name_of):
    import missing_column_finder as mcf
    groups, _ = group_units(units)
    out = []
    order = sorted(groups, key=lambda k: (-len({units[u][1] for u in groups[k]}), k))
    for i, key in enumerate(order):
        uids = groups[key]
        nst = len({units[u][1] for u in uids})
        grows = [r for u in uids for r in units[u][2]]
        if nst < MIN_LAB_STUDIES:
            out.append((name_of(key), nst, len(grows), {"state": "underpowered, not tested"}))
        else:
            out.append((name_of(key), nst, len(grows), lab_test(grows, mcf.PERM_SEED + i)))
    return out


def render_lab(name, table):
    tested = [t for t in table if t[3]["state"] == "tested"]
    flagged = [t for t in tested if t[3]["flag"]]
    L = ["%s: %d groups; %d with >= %d studies tested; %d underpowered, not tested; %d flagged"
         % (name, len(table), len(tested), MIN_LAB_STUDIES,
            sum(t[3]["state"].startswith("underpowered") for t in table), len(flagged)),
         "  studies   rows   lab share  null mean  null max   excess   tag / signature"]
    for sig, nst, nrows, t in table:
        if t["state"] != "tested":
            continue
        L.append("  %5d  %6d   %8.3f   %8.3f  %8.3f  %+7.3f   %s"
                 % (nst, nrows, t["share"], t["null_mean"], t["null_max"], t["excess"],
                    "signature-matched, protocol-unmatched" if t["flag"] else "-"))
        L.append("        %s" % sig)
    return "\n".join(L)


def lab_gate(seeds=(0, 1, 2, 3, 4), verbose=True):
    """The lab test at the smallest group size it is allowed to run on:
    MIN_LAB_STUDIES studies, 15 rows each."""
    import numpy as np
    hit = clean = 0
    for sd in seeds:
        for planted in (True, False):
            rng = np.random.default_rng(sd)
            rows = []
            for s in range(MIN_LAB_STUDIES):
                eff = rng.normal(0, 0.3) if planted else 0.0
                for _ in range(15):
                    var = rng.uniform(0.01, 0.1)
                    rows.append({"Author": "S%d" % s, "var": "%.6f" % var,
                                 "rr": "%.6f" % (eff + rng.normal(0, var ** 0.5))})
            flag = lab_test(rows, 500 + sd).get("flag", False)
            hit += planted and flag
            clean += (not planted) and (not flag)
    lines = ["lab test at %d studies, planted lab effect: flagged on %d of %d seeds  %s"
             % (MIN_LAB_STUDIES, hit, len(seeds), "PASS" if hit == len(seeds) else "FAIL"),
             "lab test at %d studies, pure noise: clean on %d of %d seeds  %s"
             % (MIN_LAB_STUDIES, clean, len(seeds), "PASS" if clean == len(seeds) else "FAIL")]
    ok = hit == len(seeds) and clean == len(seeds)
    lines.append("LAB GATE %s" % ("PASS" if ok else "FAIL"))
    if verbose:
        print("\n".join(lines))
    return ok, lines


# ---------------------------------------------------------------- power curve
POWER_K = [2, 3, 4, 5, 8]
POWER_SD = [0.05, 0.1, 0.2, 0.4]       # chosen, no external source
POWER_SEEDS = 50
POWER_ROWS = 15
RULE_SD, RULE_DETECT, RULE_FALSE = 0.2, 0.8, 0.05


def fixed_effects(k, sd):
    """k lab effects, equally spaced, mean 0, population sd exactly sd."""
    if sd == 0:
        return [0.0] * k
    base = [i - (k - 1) / 2.0 for i in range(k)]
    s = (sum(b * b for b in base) / k) ** 0.5
    return [b / s * sd for b in base]


def power_cell(k, sd, seeds=POWER_SEEDS):
    import numpy as np
    hits = 0
    for seed in range(seeds):
        rng = np.random.default_rng(100000 * k + 1000 * int(round(sd * 100)) + seed)
        rows = []
        for s, eff in enumerate(fixed_effects(k, sd)):
            for _ in range(POWER_ROWS):
                var = rng.uniform(0.01, 0.1)
                rows.append({"Author": "S%d" % s, "var": "%.6f" % var,
                             "rr": "%.6f" % (eff + rng.normal(0, var ** 0.5))})
        hits += bool(lab_test(rows, 7000 + seed).get("flag", False))
    return hits / seeds


def power_curve():
    return {k: {sd: power_cell(k, sd) for sd in [0.0] + POWER_SD} for k in POWER_K}


def qualifies(curve, k):
    return curve[k][RULE_SD] >= RULE_DETECT and curve[k][0.0] <= RULE_FALSE


def size_for(n_studies):
    """Largest tested size not above the real group's study count."""
    below = [k for k in POWER_K if k <= n_studies]
    return max(below) if below else None


def power_lab_table(units, curve, perm_base):
    groups, _ = group_units(units)
    out = []
    order = sorted(groups, key=lambda key: (-len({units[u][1] for u in groups[key]}), key))
    for i, key in enumerate(order):
        uids = groups[key]
        nst = len({units[u][1] for u in uids})
        grows = [r for u in uids for r in units[u][2]]
        k = size_for(nst)
        if k is None or not qualifies(curve, k):
            out.append((key, nst, len(grows), {"state": "underpowered at this size"}))
        else:
            out.append((key, nst, len(grows), lab_test(grows, perm_base + i)))
    return out


# ----------------------------------------------------------------------- gate
_LEVELS = {"Experimental.setting": ["Greenhouse", "Field"], "Approach": ["Self-Other", "Self-Sterilized"],
           "Phase1.culti": ["Monoculture", "Community"], "SoilTp": ["Whole soil", "Inoculum"],
           "Phase2.grow": ["Alone", "Competition"], "Response": ["Aboveground", "Total_biomass"],
           "Phase2.time": ["2", "5", "9", "20"]}


def _study(name, design, n, rng):
    return [dict(design, Author=name, rr="%.4f" % rng.gauss(0, 0.3), var="0.05") for _ in range(n)]


def synthetic(seed, planted=3, per_group=5, loners=6):
    """planted groups of per_group studies each share one design; loners
    each get a design nobody else has.  Returns (rows, truth)."""
    rng = random.Random(seed)
    combos = [dict(zip(FIELDS, c)) for c in _product([_LEVELS[f] for f in FIELDS])]
    rng.shuffle(combos)
    rows, truth, k = [], [], 0
    for g in range(planted):
        names = ["G%d_S%d" % (g, i) for i in range(per_group)]
        truth.append(sorted(names))
        for nm in names:
            d = dict(combos[k])
            if g == 0:
                d["Phase2.time"] = rng.choice(["3.5", "4", "5", "6"])   # same bin, different values
            rows += _study(nm, d, rng.randint(3, 20), rng)
        k += 1
    for i in range(loners):
        d = dict(combos[k])
        if i == 0:
            d["Response"] = "NA"                                         # a missing field
        rows += _study("L%d" % i, d, rng.randint(3, 20), rng)
        k += 1
    rng.shuffle(rows)
    return rows, sorted(truth)


def _product(lists):
    out = [[]]
    for lst in lists:
        out = [o + [x] for o in out for x in lst]
    return out


def gate(seeds=(0, 1, 2, 3, 4), verbose=True):
    lines, ok = [], True
    hit = 0
    for sd in seeds:
        rows, truth = synthetic(sd)
        res = sort_studies(rows)
        got = sorted(g["studies"] for g in res["groups"])
        hit += got == truth and len(res["singletons"]) == 6
    lines.append("known-answer, 3 planted groups + 6 loners: recovered exactly on %d of %d seeds  %s"
                 % (hit, len(seeds), "PASS" if hit == len(seeds) else "FAIL"))
    ok &= hit == len(seeds)
    clean = 0
    for sd in seeds:
        rows, _ = synthetic(sd, planted=0, loners=40)
        res = sort_studies(rows)
        clean += len(res["groups"]) == 0 and len(res["singletons"]) == 40
    lines.append("null, 40 studies all different: no group reported on %d of %d seeds  %s"
                 % (clean, len(seeds), "PASS" if clean == len(seeds) else "FAIL"))
    ok &= clean == len(seeds)
    rows, _ = synthetic(0)
    res = sort_studies(rows)
    nr_ok = sum(NR in s["signature"][FIELDS.index("Response")] for s in res["singletons"]) == 1
    lines.append("missing field reads NOT RECORDED and is not merged with a recorded value  %s"
                 % ("PASS" if nr_ok else "FAIL"))
    ok &= nr_ok
    lines.append("GATE %s" % ("PASS" if ok else "FAIL"))
    if verbose:
        print("\n".join(lines))
    return ok, lines


# ------------------------------------------------------------------------ run
def main():
    a = sys.argv[1:]
    if a == ["--gate"]:
        raise SystemExit(0 if gate()[0] else 1)
    if len(a) == 2 and a[0] == "strata":
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        root = os.path.dirname(os.path.dirname(here))
        sys.path.insert(0, root)
        sys.path.insert(0, os.path.join(root, "holdout"))
        import phase_b
        import phase_c
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        side = {"anchor": [r for r in allrows if int(r["Year"]) <= CUTOFF_YEAR],
                "holdout": [r for r in allrows if int(r["Year"]) > CUTOFF_YEAR]}

        def cell(rows, xfun, yfun):
            n_st = len({r["Author"] for r in rows})
            try:
                with __import__("warnings").catch_warnings():
                    __import__("warnings").simplefilter("ignore")
                    f = phase_b.fit(rows, xfun, yfun=yfun)
                est, (lo, hi) = f["estimate"], f["interval80"]
                if not all(x == x for x in (est, lo, hi)):
                    raise ValueError
            except Exception:
                return {"state": "not checkable", "studies": n_st, "rows": len(rows)}
            return {"state": "thin" if f["n_studies"] < THIN_STUDIES else "ok", "est": est, "lo": lo,
                    "hi": hi, "studies": f["n_studies"], "rows": f["n_rows"]}

        def txt(c):
            if c["state"] == "not checkable":
                return "not checkable (%d studies, %d rows)" % (c["studies"], c["rows"])
            return "%+8.4f [%+8.4f, %+8.4f] %3d st %5d rows%s" % (
                c["est"], c["lo"], c["hi"], c["studies"], c["rows"], "  thin" if c["state"] == "thin" else "")

        def sgn(c):
            return None if c["state"] == "not checkable" else ("+" if c["est"] > 0 else "-")

        print("APPROACH STRATA: Phase B fits (imported, unchanged) inside each Approach; spent holdout, scores nothing")
        print("  cell = estimate [80%% interval] studies rows ; thin = under %d studies" % THIN_STUDIES)
        strata = [("all rows", None), ("Self-Other", "Self-Other"), ("Self-Sterilized", "Self-Sterilized")]
        res = {}
        for fid, pid, col, xfun, yfun in phase_c.FITS:
            print("  %s (%s)" % (fid, col))
            for sname, val in strata:
                c = {s: cell([r for r in side[s] if val is None or r["Approach"] == val], xfun, yfun)
                     for s in ("anchor", "holdout")}
                res[(fid, sname)] = c
                print("    %-16s anchor  %s" % (sname, txt(c["anchor"])))
                print("    %-16s holdout %s" % ("", txt(c["holdout"])))
        print("\nFLIP READING: anchor vs holdout sign of the point estimate")
        print("  id       all rows        Self-Other               Self-Sterilized")

        def flip(c):
            a_, h_ = sgn(c["anchor"]), sgn(c["holdout"])
            if a_ is None or h_ is None:
                return "not checkable"
            base = "%s -> %s %s" % (a_, h_, "flip" if a_ != h_ else "same")
            return base + (" (thin)" if "thin" in (c["anchor"]["state"], c["holdout"]["state"]) else "")
        for fid, pid, col, xfun, yfun in phase_c.FITS:
            print("  %-7s  %-14s  %-23s  %s" % (fid, flip(res[(fid, "all rows")]),
                                                flip(res[(fid, "Self-Other")]), flip(res[(fid, "Self-Sterilized")])))
        flips = [f[0] for f in phase_c.FITS if "flip" in flip(res[(f[0], "all rows")])]
        gone = [(fid, s) for fid in flips for s in ("Self-Other", "Self-Sterilized")
                if flip(res[(fid, s)]).endswith("same")]
        print("  flips in all rows: %s" % (", ".join(flips) or "none"))
        print("  disappear inside a stratum with both cells at >= %d studies: %s"
              % (THIN_STUDIES, ", ".join("%s in %s" % g for g in gone) or "none"))
        return
    if len(a) == 2 and a[0] == "slots":
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        su, au = study_units(allrows), arm_units(allrows)
        print("SLOTS (pooled): empty on every unit, never imputed, outside the signature")
        print("  slot                      NOT RECORDED on studies   NOT RECORDED on arms   expiry_condition")
        for names, exp in ((SLOTS, SLOT_EXPIRY), (INSTRUMENT_SLOTS, INSTRUMENT_EXPIRY),
                           (OTHER_SLOTS, INSTRUMENT_EXPIRY)):
            for s in names:
                ns = sum(slots(v[2])[s] == NR for v in su.values())
                na = sum(slots(v[2])[s] == NR for v in au.values())
                print("  %-24s  %10d of %-10d  %8d of %-10d  %s" % (s, ns, len(su), na, len(au), exp))
        in_sig = [s for s in slots(None) if s in FIELDS]
        print("  signature fields: %d ; slots inside the signature: %d ; slots: %d"
              % (len(FIELDS), len(in_sig), len(slots(None))))
        return
    if len(a) == 2 and a[0] == "dropnull":
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import missing_column_finder as mcf
        if not gate()[0]:
            raise SystemExit("GATE FAIL: not run")
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        resid, share = finder_residuals(allrows)
        ref = mcf.analyse(allrows, n_perm=1)["together"]["share"]
        if abs(share - ref) >= 1e-12:
            raise SystemExit("residuals do not match the finder: not run")
        print("FIELD-DROP NULL (arm level, pooled): %d shuffles per field, value counts kept" % DROP_SHUFFLES)
        print("  dropped field         real rise   null mean   null 95th   share of null >= real   shuffles  mark")
        for f, real, mean, p95, frac, n, mark in drop_null(arm_units(allrows), resid):
            print("  %-20s %+9.4f   %+9.4f   %+9.4f   %21.3f   %8d  %s"
                  % (f, real, mean, p95, frac, n, mark))
        return
    if len(a) == 2 and a[0] == "power":
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import missing_column_finder as mcf
        if not gate()[0]:
            raise SystemExit("GATE FAIL: not run")
        print("POWER CURVE (synthetic only): %d rows per study, %d seeds per cell, flag rule unchanged"
              % (POWER_ROWS, POWER_SEEDS))
        curve = power_curve()
        print("  detection rate, lab effects fixed at spread sd")
        print("  k studies   " + "   ".join("sd %.2f" % s for s in POWER_SD) + "   false-flag (pure noise)")
        for k in POWER_K:
            print("  %9d   " % k + "   ".join("%7.2f" % curve[k][s] for s in POWER_SD)
                  + "   %7.2f" % curve[k][0.0])
        print("RULE (declared before real data): detection >= %.1f at sd %.1f and false-flag <= %.2f"
              % (RULE_DETECT, RULE_SD, RULE_FALSE))
        ok_k = [k for k in POWER_K if qualifies(curve, k)]
        print("  qualifying sizes: %s ; a real group of k studies is read at the largest tested size <= k"
              % (", ".join(map(str, ok_k)) or "none"))
        if not ok_k:
            print("RESULT: no group size qualifies, so no real group qualifies. The lab test is not run.")
            return
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        sides = [("anchor (<= 2018)", [r for r in allrows if int(r["Year"]) <= CUTOFF_YEAR]),
                 ("holdout (> 2018)", [r for r in allrows if int(r["Year"]) > CUTOFF_YEAR]),
                 ("pooled", allrows)]
        any_real = False
        for name, rows in sides:
            for lvl, mk in (("study", study_units), ("arm", arm_units)):
                table = power_lab_table(mk(rows), curve, mcf.PERM_SEED)
                tested = [x for x in table if x[3]["state"] == "tested"]
                any_real |= bool(tested)
                flagged = [x for x in tested if x[3]["flag"]]
                under = sum(x[3]["state"].startswith("underpowered") for x in table)
                thin = sum(x[2] < POWER_ROWS * x[1] for x in tested)
                print("\n%s, %s level: %d groups; %d tested; %d underpowered at this size; "
                      "%d not checkable (rows barely exceed studies); %d flagged"
                      % (name, lvl, len(table), len(tested), under,
                         len(table) - len(tested) - under, len(flagged)))
                print("  tested groups with fewer than %d rows per study (thinner than the power curve's groups): "
                      "%d of %d ; flagged among them: %d"
                      % (POWER_ROWS, thin, len(tested), sum(x[2] < POWER_ROWS * x[1] for x in flagged)))
                show = tested if name == "pooled" else flagged
                if show:
                    print("  %s" % ("every tested group:" if name == "pooled" else "flagged groups only:"))
                    print("  studies   rows   lab share  null mean  null max   excess   tag / signature")
                for key, nst, nrows, r_ in show:
                    print("  %5d  %6d   %8.3f   %8.3f  %8.3f  %+7.3f   %s"
                          % (nst, nrows, r_["share"], r_["null_mean"], r_["null_max"], r_["excess"],
                             "signature-matched, protocol-unmatched" if r_["flag"] else "not flagged"))
                    print("        %s" % " | ".join(key))
        if not any_real:
            print("\nRESULT: no real group qualifies. The lab test is not run.")
        return
    if len(a) == 2 and a[0] == "addendum":
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import missing_column_finder as mcf
        print("gates first:")
        g_ok = gate()[0]
        lab_ok = lab_gate()[0]
        if not g_ok:
            raise SystemExit("GATE FAIL: not run on real data")
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        sides = [("anchor (<= 2018)", [r for r in allrows if int(r["Year"]) <= CUTOFF_YEAR]),
                 ("holdout (> 2018)", [r for r in allrows if int(r["Year"]) > CUTOFF_YEAR]),
                 ("pooled", allrows)]
        print("\n1 UNIT = study x arm (study-level kept beside it)")
        print("  side               level   units  groups  units in groups  singletons")
        for name, rows in sides:
            for lvl, mk in (("study", study_units), ("arm", arm_units)):
                u = mk(rows)
                g, s = group_units(u)
                print("  %-18s %-6s %6d  %6d  %15d  %10d"
                      % (name, lvl, len(u), len(g), sum(len(x) for x in g.values()), len(s)))
        for lvl, mk in (("study", study_units), ("arm", arm_units)):
            nb, ub, uh = both_sides(mk(allrows))
            print("  %-5s level: signatures that are groups on both sides %d ; units in them %d (holdout %d)"
                  % (lvl, nb, ub, uh))
        resid, share = finder_residuals(allrows)
        ref = mcf.analyse(allrows, n_perm=1)["together"]["share"]
        print("\n2 FIELD-DROP SENSITIVITY (pooled; signature not changed)")
        print("  residuals: rebuilt all-columns fit explains %.6f, finder reports %.6f  %s"
              % (share, ref, "MATCH" if abs(share - ref) < 1e-12 else "MISMATCH"))
        if abs(share - ref) >= 1e-12:
            raise SystemExit("residuals do not match the finder: sensitivity not run")
        for lvl, mk in (("study", study_units), ("arm", arm_units)):
            print("  %s level" % lvl)
            print("    dropped field         groups  singletons  both-sides groups  units in them"
                  "  spread same rows  spread own rows  mark")
            for f, ng, ns, nb, ub, uh, same, own, mark in drop_table(mk(allrows), resid):
                print("    %-20s %6d  %10d  %17d  %13d  %16s  %15s  %s"
                      % (f, ng, ns, nb, ub, "%.4f" % same if same is not None else "n/a",
                         "%.4f" % own if own is not None else "n/a", mark))
        print("\n3 LAB SPREAD inside each group (power gate: >= %d studies)" % MIN_LAB_STUDIES)
        if not lab_ok:
            print("  LAB GATE FAIL: lab test not run on real data")
        else:
            for name, rows in sides:
                for lvl, mk in (("study", study_units), ("arm", arm_units)):
                    print()
                    print(render_lab("%s, %s level" % (name, lvl),
                                     lab_table(mk(rows), lambda k: " | ".join(k))))
        print("\n4 slots per study: %s ; NOT RECORDED on %d of %d studies ; expiry_condition: %s"
              % (", ".join(SLOTS), len(study_units(allrows)), len(study_units(allrows)), SLOT_EXPIRY))
        return
    if len(a) == 2 and a[0] == "run":
        print("gate first:")
        if not gate()[0]:
            raise SystemExit("GATE FAIL: not run on real data")
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        sides = {"anchor (<= 2018)": [r for r in allrows if int(r["Year"]) <= CUTOFF_YEAR],
                 "holdout (> 2018)": [r for r in allrows if int(r["Year"]) > CUTOFF_YEAR],
                 "pooled": allrows}
        res = {k: sort_studies(v) for k, v in sides.items()}
        # one id per signature, numbered by pooled size, shared by all three reports
        every = {}
        for k in res:
            for g in res[k]["groups"] + res[k]["singletons"]:
                every.setdefault(g["signature"], 0)
        pooled_n = {g["signature"]: g["n_studies"] for g in res["pooled"]["groups"] + res["pooled"]["singletons"]}
        ids = {s: "D%02d" % (i + 1) for i, s in enumerate(
            sorted(every, key=lambda s: (-pooled_n.get(s, 0), s)))}
        for k in sides:
            print()
            print(render(k, res[k], ids))

        def count(side):
            return {g["signature"]: (g["n_studies"], g["n_rows"])
                    for g in res[side]["groups"] + res[side]["singletons"]}
        ca, ch = count("anchor (<= 2018)"), count("holdout (> 2018)")
        both = sorted(set(ca) & set(ch), key=lambda s: ids[s])
        print("\nsignatures present on both sides (anchor studies/rows ; holdout studies/rows):")
        for s in both:
            tag = "group on both sides" if ca[s][0] > 1 and ch[s][0] > 1 else "one study on a side"
            print("  %-5s anchor %3d /%5d ; holdout %3d /%5d   %s"
                  % (ids[s], ca[s][0], ca[s][1], ch[s][0], ch[s][1], tag))
        gb = [s for s in both if ca[s][0] > 1 and ch[s][0] > 1]
        print("  groups on both sides: %d ; signatures on both sides at all: %d ; "
              "anchor only: %d ; holdout only: %d"
              % (len(gb), len(both), len(set(ca) - set(ch)), len(set(ch) - set(ca))))
        print("  holdout studies inside a both-sides group: %d of %d ; holdout rows: %d of %d"
              % (sum(ch[s][0] for s in gb), res["holdout (> 2018)"]["studies"],
                 sum(ch[s][1] for s in gb), res["holdout (> 2018)"]["rows"]))
        print("\nno common denominator (pooled), %d studies:" % len(res["pooled"]["singletons"]))
        for g in res["pooled"]["singletons"]:
            print("  %-5s %-44s %4d rows  %s" % (ids[g["signature"]], asc(g["studies"][0])[:44],
                                                  g["n_rows"], sig_text(g["signature"])))
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
