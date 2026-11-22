# SPDX-License-Identifier: CC0-1.0
"""denominator_sorter: sort studies by what they measured against.
EXPLORATORY.  It fits nothing, scores nothing and tests no prediction.

    python3 ledger/toolkit/denominator_sorter.py --gate
    python3 ledger/toolkit/denominator_sorter.py run SOURCE_CSV
    python3 ledger/toolkit/denominator_sorter.py lab SOURCE_CSV   # addendum

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
          part in the match: two unknowns are not a match.  Latitude and
          Longitude give the field site, not the lab's location, and are
          not used to fill them.
  lab     inside each scope group, missing_column_finder's Author (lab)
          test: share of the group's spread that sits between studies,
          against rows shuffled across the group.  The spread is taken
          about the GROUP MEAN, with no column fitted first: in a group of
          k studies, k-1 study-level columns (MAT, MAP, AI, latitude)
          would absorb every between-lab difference by construction.  A
          flag tags the group "signature-matched, protocol-unmatched".

`run` and `--gate` use the standard library only.  `lab` imports
missing_column_finder (numpy) and uses its eta2, tau2_intercept, _codes
and _verdict unchanged, with its FLAG rule and shuffle count.
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
MIN_SPARE_ROWS = 2      # lab test needs rows beyond one per study; else not checkable
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
    """The three unfilled slots of one study.  Always NOT RECORDED here:
    the source carries no column for any of them."""
    return {s: NR for s in SLOTS}


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


def lab_table(rows, ids):
    import missing_column_finder as mcf
    by_study = {}
    for r in rows:
        by_study.setdefault(r["Author"], []).append(r)
    res = sort_studies(rows)
    out = []
    for i, g in enumerate(res["groups"]):
        grows = [r for s in g["studies"] for r in by_study[s]]
        out.append((ids[g["signature"]], g, lab_test(grows, mcf.PERM_SEED + i)))
    return res, out


def render_lab(name, res, table):
    tested = [t for t in table if t[2]["state"] == "tested"]
    flagged = [t for t in tested if t[2]["flag"]]
    L = ["%s: %d scope groups, %d tested, %d not checkable, %d flagged"
         % (name, len(table), len(tested), len(table) - len(tested), len(flagged)),
         "  id    studies   rows   lab share  null mean  null max   excess   tag"]
    for gid, g, t in table:
        if t["state"] != "tested":
            L.append("  %-5s %5d  %6d   not checkable (rows barely exceed studies)" % (gid, g["n_studies"], g["n_rows"]))
            continue
        L.append("  %-5s %5d  %6d   %8.3f   %8.3f  %8.3f  %+7.3f   %s"
                 % (gid, t["studies"], t["rows"], t["share"], t["null_mean"], t["null_max"], t["excess"],
                    "signature-matched, protocol-unmatched" if t["flag"] else "-"))
    L.append("  tagged signature-matched, protocol-unmatched: %s"
             % (", ".join(t[0] for t in flagged) or "none"))
    return "\n".join(L)


def lab_gate(seeds=(0, 1, 2, 3, 4), verbose=True):
    """The lab test at scope-group size: 4 studies, 15 rows each."""
    import numpy as np
    hit = clean = 0
    for sd in seeds:
        for planted in (True, False):
            rng = np.random.default_rng(sd)
            rows = []
            for s in range(4):
                eff = rng.normal(0, 0.3) if planted else 0.0
                for _ in range(15):
                    var = rng.uniform(0.01, 0.1)
                    rows.append({"Author": "S%d" % s, "var": "%.6f" % var,
                                 "rr": "%.6f" % (eff + rng.normal(0, var ** 0.5))})
            flag = lab_test(rows, 500 + sd).get("flag", False)
            hit += planted and flag
            clean += (not planted) and (not flag)
    lines = ["lab test at group size, planted lab effect: flagged on %d of %d seeds  %s"
             % (hit, len(seeds), "PASS" if hit == len(seeds) else "FAIL"),
             "lab test at group size, pure noise: clean on %d of %d seeds  %s"
             % (clean, len(seeds), "PASS" if clean == len(seeds) else "FAIL")]
    ok = hit == len(seeds) and clean == len(seeds)
    lines.append("LAB GATE %s" % ("PASS" if ok else "FAIL"))
    if verbose:
        print("\n".join(lines))
    return ok, lines


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
    if len(a) == 2 and a[0] == "lab":
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        print("gates first:")
        if not gate()[0] or not lab_gate()[0]:
            raise SystemExit("GATE FAIL: not run on real data")
        raw = open(a[1], "rb").read()
        if hashlib.sha256(raw).hexdigest() != SOURCE_SHA:
            raise SystemExit("source sha256 mismatch: not run")
        allrows = list(csv.DictReader(io.StringIO(raw.decode("utf-8", errors="replace"), newline="")))
        pooled = sort_studies(allrows)
        ids = {g["signature"]: "D%02d" % (i + 1) for i, g in enumerate(sorted(
            pooled["groups"] + pooled["singletons"], key=lambda g: (-g["n_studies"], g["signature"])))}
        sides = [("anchor (<= 2018)", [r for r in allrows if int(r["Year"]) <= CUTOFF_YEAR]),
                 ("holdout (> 2018)", [r for r in allrows if int(r["Year"]) > CUTOFF_YEAR]),
                 ("pooled", allrows)]
        for name, rows in sides:
            res, table = lab_table(rows, ids)
            print()
            print(render_lab(name, res, table))
        filled = sum(v != NR for r_ in [slots(None)] for v in r_.values())
        print("\nslots per study: %s ; filled on %d of %d studies ; expiry_condition: %s"
              % (", ".join(SLOTS), filled, pooled["studies"], SLOT_EXPIRY))
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
