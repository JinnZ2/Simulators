#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
stats.py -- every number the revised report states, computed from registry
objects. Nothing here is typed in: a count is a function of objects, and
tools/build.py fills the corrected statement values (ST-01..ST-19) from
statement_values(), so a statement and the registry cannot disagree.

    grading     stored_grades(obj): RUS-0.2 on the annex's mixed basis, the
                action basis and the outcome basis, each with the source
                C_restrict ("src") and the registry's second coding ("reg");
                RUS-0.3 (M7 + SUB + R6, R1 scoped) on action and outcome
    sweep       M0-M6 as published in calibration_sweep_v3.csv, recomputed;
                M4 and M6 U3 rows searched over all non-decreasing rows; M7
    one-dir     per variant: below, over, and the rows on which the
                over-restrictive branch can fire at all (over_possible), so
                a zero is read as untestable when no row can produce it
    bivariate   direction (relative to bearer) x cost group, Rule L and
                Rule S, Fisher exact two-sided (imported), source frame and
                DECISION-only frame
    forcing     restrictive-action list from action_direction; external
                forcing kinds; with Frame C2's restrictive rows
    reversals   time to reversal by direction, exact Mann-Whitney
    mirrors     divergence of the comparator pairs
    kappa       second coder per field, when second_coder/coding.jsonl exists

Scope (NCR-N21): the coded sample was drawn from permissive anchors; every
count over it is a count inside that sample. R8 rows and Frame C2 are
reported apart and never pooled into a sample statistic.

CLI:  python3 tools/stats.py [--section NAME]   (reads registry/)
Library otherwise; refuses --selftest (checks in tools/validate.py). Stdlib.
"""

import csv
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reglib  # noqa: E402
import grade  # noqa: E402

PERMISSIVE = ("go_ahead", "warn")
RESTRICTIVE = ("hold", "decline")
EXTERNAL_FORCING = ("statute", "court_order", "failed_confirmatory_trial",
                    "litigation_post_market_harm", "new_data_scheduled_rule",
                    "unmet_postmarket_requirement")
# agency_own_study is a forcing kind the registry records (B06, BVO) and is
# not external: the agency's own study is the discretionary case.

RUS02 = {"columns": "published"}
RUS03 = {"columns": "published", "symmetric": True, "substitution": True,
         "r6": True}

SWEEP = [  # label prefix in calibration_sweep_v3.csv -> variant
    ("M0", {"columns": "published"}),
    ("M1", {"columns": "lenient"}),
    ("M2", {"columns": "strict"}),
    ("M3", {"columns": "uniform"}),  # "all G->col2": the second column (G = 0), counted from 1
    ("M4", {"columns": "published", "u3_row": "SEARCH"}),
    ("M5", {"columns": "lenient", "u3_row": "M4"}),
    ("M6", {"columns": "strict", "u3_row": "SEARCH"}),
]
M7 = ("M7", {"columns": "published", "symmetric": True})
TEXT_CHECKS = [  # (source id, needle, NCR): present in the pinned text
    ("SRC-K2-REPORT", "followed the committee 66.7% of the time** (40 of 60 not approved)", "NCR-R1"),
    ("SRC-K2-REPORT", "permissive skew, no contrast group", "NCR-R1"),
    ("SRC-K2-REPORT", "there is no within-frame variation in cost-bearer", "NCR-R1"),
]
TESTABLE_MIN = 5  # [CHOICE] a 2x2 is reported 'not testable at this n' when a margin is below this


def val(obj, field):
    c = obj.get("claims", {}).get(field)
    return None if c is None else c["value"]


def coded_sample(objects):
    return sorted((o for o in objects.values()
                   if o["type"] in ("DECISION", "NON_DECISION") and o.get("in_sample")),
                  key=lambda o: o["id"])


def frame(objects, f):
    return sorted((o for o in objects.values()
                   if o["type"] in ("DECISION", "NON_DECISION") and o.get("frame") == f),
                  key=lambda o: o["id"])


# ---------------------------------------------------------------- grading

def grade_input(obj, basis, side):
    """The dict grade.grade_case reads, for one case on one basis."""
    c = obj["consequence"]
    cr_side = c["C_restrict"]["registry"] if side == "reg" else c["C_restrict"]["source"]
    if cr_side is None:
        return None
    sub = c["C_restrict"]["substitution"]
    annex = obj.get("annex")
    if basis == "annex":
        if annex is None:
            return None
        forced = annex["status"].startswith("STATUTE")
    elif basis == "action":
        forced = bool(val(obj, "forced_action"))
    else:
        forced = bool(val(obj, "forced_outcome"))
    return {
        "U": val(obj, "U_grade"), "cp": c["C_permit"]["score"],
        "cr": cr_side["score"], "cp_grade": c["C_permit"]["grade"],
        "actual_annex": annex["actual"] if annex else None,
        "actual_action": grade.ACTUAL_OF[val(obj, "action_direction")],
        "actual_outcome": grade.ACTUAL_OF[val(obj, "outcome_direction")],
        "forced": forced,
        "r1": val(obj, "r1") != "none" and val(obj, "r1_scope") == "market_status",
        "r5": bool(val(obj, "r5")),
        "alt_claimed": sub["claimed"], "alt_named": sub["named"],
        "alt_grade": sub["grade"],
        "r6b": bool(val(obj, "r6b_loosening")),
        "r6_blocking": bool(val(obj, "r6_blocking")),
        "r6_cycles": val(obj, "r6_cycles"),
        # only an independent justification counts; a restriction justified
        # by the evidence it blocks is not justified (RUS-0.3 R6a)
        "r6_justified": val(obj, "r6_justification") == "independent",
    }


def matrix_variant(variant, m4_row=None, search_row=None):
    v = dict(variant)
    if v.get("u3_row") == "M4":
        v["u3_row"] = m4_row
    elif v.get("u3_row") == "SEARCH":
        v["u3_row"] = search_row
    return v


def grade_one(obj, basis, side, variant):
    case = grade_input(obj, basis, side)
    if case is None:
        return None
    if variant.get("r1_literal"):
        # NCR-N06's literal reading: R1 wherever a row carries an R1 flag,
        # level-setting rows included
        case["r1"] = val(obj, "r1") != "none"
    return grade.grade_case(case, dict(variant, basis=basis))


# RUS-0.3 taken apart: each switch alone and combined, so the reading of
# one-directional non-conformity can be attributed to a switch (Part D)
RUS03_PARTS = [
    ("RUS-0.2", {"columns": "published"}),
    ("+M7", {"columns": "published", "symmetric": True}),
    ("+SUB", {"columns": "published", "substitution": True}),
    ("+R6", {"columns": "published", "r6": True}),
    ("+R1L", {"columns": "published", "r1_literal": True}),
    ("+M7+SUB", {"columns": "published", "symmetric": True, "substitution": True}),
    ("RUS-0.3", RUS03),
    ("RUS-0.3+R1L", dict(RUS03, r1_literal=True)),
]


def sub_alone(objects, basis, side="src"):
    """Rows of the coded sample whose floor or status moves when SUB is the
    only switch on: SUB can lower a floor without changing a status, so the
    two are counted apart."""
    base, sub = dict(RUS03_PARTS)["RUS-0.2"], dict(RUS03_PARTS)["+SUB"]
    floors, statuses = [], []
    for o in coded_sample(objects):
        a, b = grade_one(o, basis, side, base), grade_one(o, basis, side, sub)
        if a is None or b is None:
            continue
        if a["floor"] != b["floor"]:
            floors.append(o["id"])
        if a["status"] != b["status"]:
            statuses.append(o["id"])
    return {"floors": floors, "statuses": statuses}


def components(objects, side="src"):
    rows = []
    sample = coded_sample(objects)
    for basis in ("action", "outcome"):
        for name, variant in RUS03_PARTS:
            t = tally_of(sample, basis, side, variant)
            r6 = sum(1 for o in sample
                     if (grade_one(o, basis, side, variant) or {}).get("r6") == grade.R6_SELF_SEALING)
            rows.append({"basis": basis, "variant": name, "tally": t, "r6_self_sealing": r6})
    return rows


def stored_grades(obj):
    out = {}
    for name, variant in (("rus02", RUS02), ("rus03", RUS03)):
        for basis in ("annex", "action", "outcome"):
            if name == "rus03" and basis == "annex":
                continue
            for side in ("src", "reg"):
                g = grade_one(obj, basis, side, variant)
                if g is not None:
                    out["%s.%s.%s" % (name, basis, side)] = g
    return out


def over_branch(obj, basis, side, variant):
    """Where can R2's over-restrictive branch fire on this row? It needs
    C_restrict > C_permit, a matrix floor (R1 sets D5, R5 has its own
    branch) and no R3 compulsion. Returns (reachable, possible):
      reachable  some actual direction would fire it (the standard CAN
                 produce over-restriction on this row)
      possible   the row's own actual can fire it under SOME matrix (the
                 actual is D3 or above). A sweep varies the matrix and holds
                 the actuals, so a zero over the sweep is testable only on
                 rows where `possible` is true (REVIEW_v3 R13)."""
    case = grade_input(obj, basis, side)
    if case is None:
        return False, False
    g = grade.grade_case(case, dict(variant, basis=basis))
    base = (g["cr_eff"] > case["cp"] and g["floor_rule"] == "matrix"
            and not case["forced"])
    return (base and grade.d_index(g["floor"]) <= 3,
            base and grade.d_index(g["actual"]) >= 3)


def tally_of(objs, basis, side, variant):
    rows = []
    for o in objs:
        g = grade_one(o, basis, side, variant)
        if g is not None:
            rows.append((o, g))
    t = grade.tally([g["status"] for o, g in rows])
    t["n"] = len(rows)
    branch = [over_branch(o, basis, side, variant) for o, g in rows]
    t["over_reachable"] = sum(1 for r, p in branch if r)
    t["over_possible"] = sum(1 for r, p in branch if p)
    t["over_rows"] = sorted(o["id"] for o, g in rows if g["status"] == grade.S_OVER)
    t["reading"] = one_directional(t)
    return t


def one_directional(t):
    """'Non-conformity is one-directional (below the floor only)':
    HOLDS             below > 0, over = 0, and some row's own actual could
                      produce over (over_possible > 0)
    HOLDS_UNTESTABLE  below > 0, over = 0, and no row's actual could: the
                      zero is fixed by the rows, not found by the standard
    FAILS             non-conformity in both directions
    REVERSED          over > 0, below = 0 (one-directional the other way)
    NO_NONCONFORMITY  neither."""
    b, o = t["below"], t["over_restrictive"]
    if b == 0 and o == 0:
        return "NO_NONCONFORMITY"
    if b > 0 and o > 0:
        return "FAILS"
    if o > 0:
        return "REVERSED"
    return "HOLDS" if t.get("over_possible", 0) > 0 else "HOLDS_UNTESTABLE"


def annex_reproduction(objects):
    """Recompute Annex A on its own basis; every disagreement is a row."""
    out = []
    for o in coded_sample(objects):
        g = o["grades"].get("rus02.annex.src")
        a = o["annex"]
        diffs = [k for k in ("status", "deviation", "gap") if a[k] != g[k]]
        # the annex writes an R5 floor as "D2 (R5)"
        if a["floor"].split()[0] != g["floor"]:
            diffs.append("floor")
        if a["U"] != g["U"]:
            diffs.append("U")
        if diffs:
            out.append((o["id"], diffs))
    return out


# ---------------------------------------------------------------- sweep

def published_sweep():
    path = os.path.join(reglib.SRCDIR, "calibration_sweep_v3.csv")
    out = {}
    with open(path, "r", encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            key = r["variant"].split()[0]
            out[key] = {"label": r["variant"], "below": int(r["below"]),
                        "conform": int(r["conform"]), "exceeds": int(r["exceeds"]),
                        "over_restrictive": int(r["over_restrictive_violations"]),
                        "statute": int(r["statute"])}
    return out


KEYS = ("below", "conform", "exceeds", "over_restrictive", "statute")


def _vec(t):
    return tuple(t[k] for k in KEYS)


def _rows():
    ds = ["D1", "D2", "D3", "D4", "D5"]
    return [list(r) for r in itertools.combinations_with_replacement(ds, 4)]


def search_u3(objs, columns, target):
    """All non-decreasing U3 rows that reproduce `target`, and the closest."""
    hits, best = [], None
    for row in _rows():
        t = tally_of(objs, "annex", "src", {"columns": columns, "u3_row": row})
        d = sum(abs(a - b) for a, b in zip(_vec(t), target))
        if d == 0:
            hits.append(row)
        if best is None or d < best[0]:
            best = (d, row, _vec(t))
    return hits, best


def sweep(objects):
    objs = coded_sample(objects)
    pub = published_sweep()
    out, m4_row = [], None
    for key, variant in SWEEP:
        target = _vec(pub[key])
        note, search = None, None
        if variant.get("u3_row") == "SEARCH":
            hits, best = search_u3(objs, variant["columns"], target)
            search = {"hits": hits, "closest": best}
            if len(hits) == 1:
                row = hits[0]
                note = "U3 row not stated in the bundle; unique reconstruction %s" % row
            elif hits:
                row = hits[0]
                note = "U3 row not stated; %d rows reproduce, first taken" % len(hits)
            else:
                row = best[1]
                note = ("U3 row not stated; no non-decreasing row reproduces the "
                        "published counts; closest %s gives %s" % (row, best[2]))
            if key == "M4" and hits:
                m4_row = row
            v = dict(variant, u3_row=row)
        else:
            v = matrix_variant(variant, m4_row=m4_row)
        t = tally_of(objs, "annex", "src", v)
        out.append({"variant": key, "label": pub[key]["label"], "published": target,
                    "computed": _vec(t), "reproduces": _vec(t) == target,
                    "over_possible": t["over_possible"], "over_reachable": t["over_reachable"],
                    "reading": t["reading"],
                    "u3_row": v.get("u3_row"), "note": note, "search": search})
    t = tally_of(objs, "annex", "src", M7[1])
    out.append({"variant": "M7", "label": "M7 symmetric tolerance (M0 + one class below conforms by margin)",
                "published": None, "computed": _vec(t), "reproduces": None,
                "over_possible": t["over_possible"], "over_reachable": t["over_reachable"],
                "reading": t["reading"],
                "u3_row": None, "note": "registry variant (NCR-R7, NCR-R13)", "search": None})
    return out


# ---------------------------------------------------------------- bivariate

def bivariate(objects, rule, frame_name):
    """2x2 restrictive/permissive by cost group under Rule L or S."""
    objs = coded_sample(objects)
    if frame_name == "decision_only":
        objs = [o for o in objs if o["type"] == "DECISION"]
    field = "cost_group_" + rule
    cells = {("concentrated", "restrictive"): 0, ("concentrated", "permissive"): 0,
             ("diffuse", "restrictive"): 0, ("diffuse", "permissive"): 0}
    for o in objs:
        d = val(o, "direction_rel_bearer")
        if d not in ("restrictive", "permissive"):
            continue
        cells[(val(o, field), d)] += 1
    a, b = cells[("concentrated", "restrictive")], cells[("concentrated", "permissive")]
    c, d = cells[("diffuse", "restrictive")], cells[("diffuse", "permissive")]
    margins = (a + b, c + d, a + c, b + d)
    p = reglib.fisher_exact_2sided(a, b, c, d)
    return {"rule": rule, "frame": frame_name, "n": a + b + c + d,
            "concentrated": (a, a + b), "diffuse": (c, c + d), "p": p,
            "testable": min(margins) >= TESTABLE_MIN,
            "reading": ("not testable at this n (smallest margin %d < %d)"
                        % (min(margins), TESTABLE_MIN)) if min(margins) < TESTABLE_MIN
                       else "testable"}


# ---------------------------------------------------------------- forcing, reversals, mirrors

def restrictive_list(objects):
    return [o for o in coded_sample(objects) if val(o, "action_direction") in RESTRICTIVE]


def forcing(objects):
    lst = restrictive_list(objects)
    forced = [o["id"] for o in lst if val(o, "forcing_kind") in EXTERNAL_FORCING]
    disc = [o["id"] for o in lst if val(o, "forcing_kind") not in EXTERNAL_FORCING]
    c2 = [o for o in frame(objects, "C2") if val(o, "direction") in RESTRICTIVE]
    c2_forced = [o["id"] for o in c2 if val(o, "forcing_kind") in EXTERNAL_FORCING]
    return {"list": [o["id"] for o in lst], "forced": forced, "discretionary": disc,
            "c2_restrictive": [o["id"] for o in c2], "c2_forced": c2_forced,
            "all_n": len(lst) + len(c2), "all_forced": len(forced) + len(c2_forced)}


def reversals(objects, d01_anchor="2016"):
    revs = sorted((o for o in objects.values() if o["type"] == "REVERSAL"),
                  key=lambda o: o["id"])
    skip = "REV-D01-1970" if d01_anchor == "2016" else "REV-D01-2016"
    groups = {"restrictive_to_permissive": [], "permissive_to_restrictive": [],
              "other": []}
    for r in revs:
        if r["id"] == skip:
            continue
        f, t = r["from_direction"], r["to_direction"]
        if f in RESTRICTIVE and t in PERMISSIVE:
            g = "restrictive_to_permissive"
        elif f in PERMISSIVE and t in RESTRICTIVE:
            g = "permissive_to_restrictive"
        else:
            g = "other"
        groups[g].append((r["id"], r["time_to_reversal_years"], r["initiator_type"]))
    x = [t for _, t, _ in groups["restrictive_to_permissive"]]
    y = [t for _, t, _ in groups["permissive_to_restrictive"]]
    mw = mann_whitney_exact(x, y) if x and y else None
    lst = {o["id"] for o in restrictive_list(objects)}
    toward = sorted({r["from_case"] for r in revs if r["from_case"] in lst
                     and r["to_direction"] in PERMISSIVE and r["id"] != skip})
    return {"groups": groups, "mann_whitney": mw, "anchor_d01": d01_anchor,
            "toward_permissive_from_list": toward}


def mann_whitney_exact(x, y):
    """Exact two-sided Mann-Whitney U by full enumeration (ties count 1/2).
    U counts pairs with x_i > y_j. Two-sided p = P(|U - mean| >= |U_obs - mean|)."""
    def u_of(xs, ys):
        return sum(1.0 if a > b else 0.5 if a == b else 0.0 for a in xs for b in ys)
    pooled = list(x) + list(y)
    n, m = len(x), len(y)
    u_obs = u_of(x, y)
    mean = n * m / 2.0
    count = extreme = 0
    for idx in itertools.combinations(range(n + m), n):
        xs = [pooled[i] for i in idx]
        ys = [pooled[i] for i in range(n + m) if i not in idx]
        u = u_of(xs, ys)
        count += 1
        if abs(u - mean) >= abs(u_obs - mean) - 1e-12:
            extreme += 1
    return {"U": u_obs, "n_x": n, "n_y": m, "p_two_sided": extreme / float(count),
            "enumerated": count}


def mirrors(objects):
    rows = [o for o in frame(objects, "M") if val(o, "us_score") is not None]
    div = [o["id"] for o in rows if val(o, "divergence") >= 1]
    ge2 = [o["id"] for o in rows if val(o, "divergence") >= 2]
    return {"n": len(rows), "divergent": len(div), "ge2": len(ge2), "ids": div}


def c2_counts(objects):
    rows = frame(objects, "C2")
    na = [o for o in rows if val(o, "direction") == "NA"]
    merit = [o for o in rows if val(o, "direction") != "NA"]
    return {"n": len(rows), "merit": len(merit), "na": len(na),
            "permissive": sum(1 for o in merit if val(o, "direction") in PERMISSIVE),
            "restrictive": sum(1 for o in merit if val(o, "direction") in RESTRICTIVE)}


# ---------------------------------------------------------------- kappa

KAPPA_FIELDS = ("action", "outcome", "direction_collapsed", "U", "cost_group",
                "Cp_grade", "Cr_grade")


def second_coder(objects, path=None):
    path = path or os.path.join(reglib.FOLDER, "second_coder", "coding.jsonl")
    if not os.path.exists(path):
        return {"state": "NOT_RUN", "reason": "second_coder/coding.jsonl absent"}
    rows = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    pairs = {f: ([], []) for f in KAPPA_FIELDS}
    for r in rows:
        o = objects[r["id"]]
        mine = registry_codes(o)
        theirs = coder_codes(r)
        for f in KAPPA_FIELDS:
            pairs[f][0].append(mine[f])
            pairs[f][1].append(theirs[f])
    out = {"state": "RUN", "n": len(rows), "fields": {}}
    for f in KAPPA_FIELDS:
        a, b = pairs[f]
        agree = sum(1 for p, q in zip(a, b) if p == q)
        k = reglib.cohen_kappa(a, b) if len(set(a) | set(b)) > 1 else None
        out["fields"][f] = {"agree": agree, "n": len(a), "kappa": k}
    return out


def registry_codes(o):
    c = o["consequence"]
    return {"action": val(o, "action_direction"), "outcome": val(o, "outcome_direction"),
            "direction_collapsed": val(o, "direction_rel_bearer"), "U": val(o, "U_grade"),
            "cost_group": val(o, "cost_group_S"), "Cp_grade": c["C_permit"]["grade"],
            "Cr_grade": c["C_restrict"]["source"]["grade"]}


def coder_codes(r):
    cp = grade.band(int(r["Cp_P"]) + int(r["Cp_I"]) + int(r["Cp_D"]))
    cr = grade.band(int(r["Cr_P"]) + int(r["Cr_I"]) + int(r["Cr_D"]))
    coll = ("permissive" if r["action"] in PERMISSIVE else
            "restrictive" if r["action"] in RESTRICTIVE else "not_determinable")
    return {"action": r["action"], "outcome": r["outcome"], "direction_collapsed": coll,
            "U": r["U"], "cost_group": r["group"], "Cp_grade": cp, "Cr_grade": cr}


# ---------------------------------------------------------------- text checks

def text_checks(objects):
    out = []
    for sid, needle, ncr in TEXT_CHECKS:
        path = os.path.join(reglib.FOLDER, objects[sid]["path"])
        n = open(path, "r", encoding="utf-8").read().count(needle)
        out.append((sid, needle, ncr, n))
    return out


# ---------------------------------------------------------------- statements

def statement_values(objects):
    c2 = c2_counts(objects)
    fc = forcing(objects)
    mi = mirrors(objects)
    rv = reversals(objects)
    sw = sweep(objects)
    b = {r["id"]: r["time_to_reversal_years"] for r in objects.values()
         if r["type"] == "REVERSAL" and r["id"] in ("REV-B00-B01", "REV-B00b-B02")}
    reproduced = [r for r in sw if r["reproduces"] or r["variant"] == "M7"]
    below = [r["computed"][0] for r in reproduced]
    annex = tally_of(coded_sample(objects), "annex", "src", RUS02)
    cp_rec = sum(1 for o in coded_sample(objects)
                 if o["consequence"]["C_permit"]["P"] is not None)
    return {
        "c2_permissive": c2["permissive"], "c2_merit": c2["merit"],
        "c2_restrictive": c2["restrictive"], "c2_na": c2["na"],
        "forced_list_forced": len(fc["forced"]), "forced_list_n": len(fc["list"]),
        "forced_all_forced": fc["all_forced"], "forced_all_n": fc["all_n"],
        "mirror_divergent": mi["divergent"], "mirror_ge2": mi["ge2"],
        "rev_b_min": "%.1f" % min(b.values()), "rev_b_max": "%.1f" % max(b.values()),
        "sweep_below_min": min(below), "sweep_below_max": max(below),
        "over_possible_annex": annex["over_possible"],
        "rev_toward_perm": len(rv["toward_permissive_from_list"]),
        "cp_axes_recovered": cp_rec,
    }


# ---------------------------------------------------------------- report

def report(objects, section=None):
    out = []
    def sec(name):
        return section in (None, name)
    sample = coded_sample(objects)
    if sec("annex"):
        out.append("== Annex A reproduction (RUS-0.2 on the annex's own basis, source C_restrict)")
        mm = annex_reproduction(objects)
        out.append("rows %d   mismatches %d%s" % (len(sample), len(mm),
                   ("  " + str(mm)) if mm else ""))
    if sec("tallies"):
        out.append("== Tallies over the coded sample (n=%d)   below conform exceeds over statute | over_reachable over_possible reading" % len(sample))
        for name, variant in (("RUS-0.2", RUS02), ("RUS-0.3", RUS03)):
            for basis in ("annex", "action", "outcome"):
                if name == "RUS-0.3" and basis == "annex":
                    continue
                for side in ("src", "reg"):
                    t = tally_of(sample, basis, side, variant)
                    out.append("%-7s %-7s %-3s  %s | %d %d %s %s" % (
                        name, basis, side, " ".join("%2d" % t[k] for k in KEYS),
                        t["over_reachable"], t["over_possible"], t["reading"],
                        ("over: " + ",".join(t["over_rows"])) if t["over_rows"] else ""))
        r8 = frame(objects, "R8")
        out.append("-- R8 restrictive-side candidates (selected on direction; never pooled)")
        for o in r8:
            for k in ("rus02.action.src", "rus03.action.src"):
                g = o["grades"][k]
                out.append("%-4s %-17s U %s gap %+d floor %s actual %s  %s%s" % (
                    o["id"], k, g["U"], g["gap"], g["floor"], g["actual"], g["status"],
                    ("  " + g["r6"]) if "r6" in g else ""))
    if sec("components"):
        out.append("== RUS-0.3 by switch (coded sample, source C_restrict)   below conform exceeds over statute | over_possible reading r6_self_sealing")
        for r in components(objects):
            t = r["tally"]
            out.append("%-7s %-12s %s | %d %s %d" % (r["basis"], r["variant"],
                       " ".join("%2d" % t[k] for k in KEYS), t["over_possible"], t["reading"],
                       r["r6_self_sealing"]))
    if sec("sweep"):
        out.append("== Calibration sweep (annex basis)   published -> computed | over_reachable over_possible reading")
        for r in sweep(objects):
            out.append("%-3s %-15s %-15s %-5s | %d %d %s%s" % (
                r["variant"], r["published"], r["computed"],
                {True: "same", False: "DIFF", None: "-"}[r["reproduces"]],
                r["over_reachable"], r["over_possible"], r["reading"], ("  " + r["note"]) if r["note"] else ""))
    if sec("bivariate"):
        out.append("== Bivariate: restrictive/total by cost group (Fisher exact, two-sided)")
        for fr in ("source_frame", "decision_only"):
            for rule in ("L", "S"):
                b = bivariate(objects, rule, fr)
                out.append("%-14s Rule %s  concentrated %d/%d  diffuse %d/%d  p=%.4f  %s" % (
                    fr, rule, b["concentrated"][0], b["concentrated"][1],
                    b["diffuse"][0], b["diffuse"][1], b["p"], b["reading"]))
    if sec("forcing"):
        f = forcing(objects)
        out.append("== Restrictive-action list (action_direction hold/decline)")
        out.append("list %s" % f["list"])
        out.append("external forcing %d of %d; not external: %s" % (
            len(f["forced"]), len(f["list"]), f["discretionary"]))
        out.append("with Frame C2 restrictive rows %s: %d of %d" % (
            f["c2_restrictive"], f["all_forced"], f["all_n"]))
    if sec("reversals"):
        for anchor in ("2016", "1970"):
            rv = reversals(objects, anchor)
            out.append("== Reversals (D01 from %s)" % anchor)
            for g, rows in sorted(rv["groups"].items()):
                out.append("%-26s %s" % (g, ", ".join("%s %.2fy (%s)" % r for r in rows)))
            mw = rv["mann_whitney"]
            if mw:
                out.append("exact Mann-Whitney U=%.1f n=%d,%d p(two-sided)=%.4f over %d arrangements"
                           % (mw["U"], mw["n_x"], mw["n_y"], mw["p_two_sided"], mw["enumerated"]))
            out.append("restrictive-list cases reversed toward permissive: %s" % rv["toward_permissive_from_list"])
    if sec("mirrors"):
        m = mirrors(objects)
        out.append("== Mirror pairs: %d of %d divergent, %d by two or more" % (m["divergent"], m["n"], m["ge2"]))
    if sec("c2"):
        c = c2_counts(objects)
        out.append("== Frame C2: %d rows; %d merit decisions (%d permissive, %d restrictive); %d closures NA"
                   % (c["n"], c["merit"], c["permissive"], c["restrictive"], c["na"]))
    if sec("kappa"):
        k = second_coder(objects)
        out.append("== Second coder: %s" % k["state"])
        if k["state"] == "RUN":
            for f, r in k["fields"].items():
                out.append("%-20s agree %d/%d kappa %s" % (
                    f, r["agree"], r["n"], "n/a (one category)" if r["kappa"] is None
                    else "%.2f" % r["kappa"]))
        else:
            out.append(k["reason"])
    if sec("text"):
        out.append("== Text checks in the pinned sources")
        for sid, needle, ncr, n in text_checks(objects):
            out.append("%-14s %-8s found %d  %s" % (sid, ncr, n, needle[:70]))
    return out


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("stats.py: checks run in tools/validate.py --selftest\n")
        return 2
    section = None
    if "--section" in argv:
        section = argv[argv.index("--section") + 1]
    reg = reglib.Registry()
    print("\n".join(report(reg.objects, section)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
