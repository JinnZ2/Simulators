# SPDX-License-Identifier: CC0-1.0
"""chain_join.py -- instruments for joining the extraction-money-power-emissions
chain, one per gap G1..G7 of the work order (WORK_ORDER.md, reconstructed).

The order asks for instruments and joined datasets, not verdicts. Every
function here takes records in the shape a public custodian publishes and
returns a reading. Every reading carries its coverage, because the order
says ownership data is incomplete by design and coverage goes with every
result. `result()` refuses to build a reading without one.

    chain (PROPOSED)                         instrument            unit of the record
    ---------------------------------------  --------------------  ------------------
    debt / reserve need -> extraction        g1_read               country-year
    extraction -> emissions -> firm          (records carry it)    firm-year
    firm -> beneficial owner                 trace, g2_read        firm -> person
    owner -> emissions, ownership-based      g3_read               firm -> jurisdiction
    shell-layer attribution loss             g4_read               firm -> break
    funding -> policy, upstream of the vote  g5_read               legislator
    money token as defense                   g6_read               country-year
    consumption-based correction over time   g7_read               country-year
    the chain joined end to end              chain_read            all of the above

Readings take one of six branches. The order lists four (pattern holds /
scope-limited / gap / missed variable). Two are added and say so:

    PATTERN_HOLDS     measured, the predicted pattern is there
    SCOPE_LIMITED     measured, it holds inside a declared subset only
    GAP               not measured: coverage under the floor (CHOICE 2)
    MISSED_VARIABLE   measured, a third variable removes it
    NO_PATTERN        measured, the predicted pattern is not there    (CHOICE 1)
    NOT_EVALUABLE     too few records to run the instrument

Every record this module reads is CONSTRUCTED in the world builders below.
Nothing here is a statement about any country, firm, person or legislator.
Jurisdictions are J1..J8, countries C01.., firms E../A../H.., persons P..,
legislators L... The secrecy scores are declared constants, not the Tax
Justice Network's index.

Refuses --selftest (exit 2); the checks live in
extraction-chain-join/test_chain.py. Stdlib only. Parses under Python 3.8. CC0.
"""

import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

WORK_ORDER = os.path.join(HERE, "WORK_ORDER.md")
WORK_ORDER_SHA256 = "6783651b0d6504f528f61d2c58946d242459d4b3ead44bf2a7de6be67ca5ef33"

sys.path.insert(0, os.path.join(ROOT, "sim-span"))
from three_column import ols  # noqa: E402  imported, not copied
sys.path.pop(0)

CHOICES = {
    1: "NO_PATTERN is added as a fifth branch. The order's four branches have "
       "no cell for a measured null, and filing one under GAP would read a "
       "measurement as an absence.",
    2: "coverage floor 0.50: a reading taken on less than half the units in its "
       "frame is returned with branch GAP and the reading attached. Scope-limited "
       "(measured, holds in a subset) and gap (not measured) stay apart.",
    3: "G1: first differences within country, debt pressure lagged one year, "
       "permutation of the debt differences within country, 400 draws, seed 7, "
       "two-sided alpha 0.05, minimum 30 differences.",
    4: "G1 missed-variable rule: the control removes the effect when "
       "|b_controlled| < 0.5 |b_raw| and the controlled slope is no longer "
       "significant.",
    5: "G2: disclosure threshold 0.25 on DIRECT holdings at each layer, because "
       "registers record direct holdings; swept over 0.05, 0.10, 0.25.",
    6: "G2: walk stops at 12 layers (DEPTH_LIMIT); a revisited entity is a CYCLE "
       "break and is not solved as a cross-holding series.",
    7: "G3: three attribution targets, IMMEDIATE_PARENT, ULTIMATE_PARENT and "
       "BO_RESIDENCE, all reported, none picked.",
    8: "G4: a jurisdiction is SECRECY at a declared score >= 60 on a 0..100 "
       "constructed scale; the loss share is printed over cuts 40..80.",
    9: "G5: AUC by rank, no model fitted. Better-than needs the bootstrap 95% "
       "band of the AUC difference to exclude 0 and a difference of at least "
       "0.05; 400 resamples, seed 11.",
    10: "G6 adequacy norms: 3 months of imports; Greenspan-Guidotti ratio "
        "(reserves / short-term debt) 1.0.",
    11: "G7: a plateau year is one where |dPB / PB| < 0.01.",
}

COVERAGE_FLOOR = 0.50
ALPHA = 0.05
MIN_N = 30
N_DRAWS = 400
ATTENUATION = 0.5
THRESHOLD = 0.25
DEPTH_LIMIT = 12
SECRECY_CUT = 60
AUC_MARGIN = 0.05
MONTHS_NORM = 3.0
GG_NORM = 1.0
PLATEAU = 0.01

BRANCHES = ("PATTERN_HOLDS", "SCOPE_LIMITED", "GAP", "MISSED_VARIABLE",
            "NO_PATTERN", "NOT_EVALUABLE")
DELIVERED_BRANCHES = BRANCHES[:4]
EVIDENCE = ("OBSERVED_JOIN", "DERIVED", "CORRELATIONAL")


class CoverageMissing(ValueError):
    """A reading with no coverage attached. The order: report the coverage
    percentage with every result."""


class CrossLevelRefused(ValueError):
    """A jurisdiction-level index used as a per-chain quantity."""


class CompositeRefused(ValueError):
    """An end-to-end effect multiplied through the chain."""


class CausalShareRefused(ValueError):
    """A 'driven by' share asked of an accounting identity."""


# --------------------------------------------------------------------------
# coverage and the result record

def coverage(covered, total):
    """covered / total. None when either is absent or the total is zero: an
    empty denominator is not a coverage of zero."""
    if covered is None or total is None:
        return None
    if total <= 0:
        return None
    if covered < 0 or covered > total + 1e-9:
        raise ValueError("coverage outside [0, total]: %r / %r" % (covered, total))
    return covered / total


def result(gap, branch, value, covered, total, unit, rule, evidence, **extra):
    """The one constructor every instrument returns through."""
    if covered is None or total is None or not unit:
        raise CoverageMissing("%s: a result without its coverage is refused" % gap)
    if branch not in BRANCHES:
        raise ValueError("branch %r is not one of %r" % (branch, BRANCHES))
    if evidence not in EVIDENCE:
        raise ValueError("evidence %r is not one of %r" % (evidence, EVIDENCE))
    out = {"gap": gap, "branch": branch, "value": value,
           "coverage": {"covered": covered, "total": total, "unit": unit,
                        "share": coverage(covered, total)},
           "rule": rule, "evidence": evidence}
    out.update(extra)
    return out


def _num(x):
    if x is None:
        return "--"
    if isinstance(x, float) and not x.is_integer():
        return "%.2f" % x
    return "%d" % x


def _f3(x):
    return "--" if x is None else "%.3f" % x


def cov_text(r):
    c = r["coverage"]
    s = "--" if c["share"] is None else "%.1f%%" % (100.0 * c["share"])
    return "coverage %s/%s %s = %s" % (_num(c["covered"]), _num(c["total"]),
                                       c["unit"], s)


# --------------------------------------------------------------------------
# small statistics

def slope(xs, ys):
    """Least-squares slope of ys on xs with an intercept. None when xs has
    no spread. Agrees with the imported ols on one regressor (checked)."""
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sxx


def residualize(ys, xs):
    """ys with their least-squares fit on xs removed."""
    b = slope(xs, ys)
    if b is None:
        return list(ys)
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    return [y - (my + b * (x - mx)) for x, y in zip(xs, ys)]


def perm_slope(xs, ys, groups, n_draws=N_DRAWS, seed=7):
    """Slope of ys on xs and a two-sided permutation p, shuffling xs inside
    each group so a country's own spread stays with it."""
    b = slope(xs, ys)
    if b is None:
        return None, None
    rng = random.Random(seed)
    extreme = 0
    for _ in range(n_draws):
        perm = list(xs)
        for idx in groups:
            vals = [xs[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                perm[i] = v
        bb = slope(perm, ys)
        if bb is not None and abs(bb) >= abs(b) - 1e-15:
            extreme += 1
    return b, (extreme + 1.0) / (n_draws + 1.0)


def auc(scores, labels):
    """Probability a random positive outscores a random negative, ties 0.5.
    By average ranks. None when either class is empty."""
    pairs = [(s, l) for s, l in zip(scores, labels) if s is not None and l is not None]
    npos = sum(1 for _s, l in pairs if l == 1)
    nneg = sum(1 for _s, l in pairs if l == 0)
    if npos == 0 or nneg == 0:
        return None
    order = sorted(range(len(pairs)), key=lambda i: pairs[i][0])
    ranks = [0.0] * len(pairs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and pairs[order[j + 1]][0] == pairs[order[i]][0]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    rpos = sum(ranks[k] for k in range(len(pairs)) if pairs[k][1] == 1)
    return (rpos - npos * (npos + 1) / 2.0) / (npos * nneg)


def _pct(vals, q):
    s = sorted(vals)
    if not s:
        return None
    k = (len(s) - 1) * q
    lo = int(math.floor(k))
    hi = int(math.ceil(k))
    return s[lo] + (s[hi] - s[lo]) * (k - lo)


# --------------------------------------------------------------------------
# G1 -- debt / reserve pressure -> extraction volume

def g1_differences(panel, lag=1):
    """Within-country first differences: d extraction at year y against
    d debt pressure at year y - lag, with d price beside it when present."""
    by = {}
    for r in panel:
        by.setdefault(r["country"], {})[r["year"]] = r
    out = []
    for c in sorted(by):
        yrs = by[c]
        for y in sorted(yrs):
            a, b = yrs.get(y), yrs.get(y - 1)
            d1, d0 = yrs.get(y - lag), yrs.get(y - lag - 1)
            if not (a and b and d1 and d0):
                continue
            if None in (a.get("extraction"), b.get("extraction"),
                        d1.get("debt"), d0.get("debt")):
                continue
            dp = None
            if d1.get("price") is not None and d0.get("price") is not None:
                dp = d1["price"] - d0["price"]
            out.append({"country": c, "year": y,
                        "dx": a["extraction"] - b["extraction"],
                        "dd": d1["debt"] - d0["debt"], "dp": dp,
                        "dependent": a.get("dependent")})
    return out


def _groups(diffs):
    g = {}
    for i, d in enumerate(diffs):
        g.setdefault(d["country"], []).append(i)
    return list(g.values())


def g1_core(diffs, seed=7):
    """Raw and price-controlled slopes with permutation p. The controlled
    slope is the partial regression slope (residuals on residuals), which
    equals the multiple-regression coefficient; the identity is checked
    against the imported ols."""
    if len(diffs) < MIN_N:
        return None
    xs = [d["dd"] for d in diffs]
    ys = [d["dx"] for d in diffs]
    groups = _groups(diffs)
    b, p = perm_slope(xs, ys, groups, seed=seed)
    core = {"n": len(diffs), "b": b, "p": p, "b_ctrl": None, "p_ctrl": None}
    if all(d["dp"] is not None for d in diffs):
        zs = [d["dp"] for d in diffs]
        rx = residualize(xs, zs)
        ry = residualize(ys, zs)
        bc, pc = perm_slope(rx, ry, groups, seed=seed + 1)
        core.update(b_ctrl=bc, p_ctrl=pc)
    return core


def g1_frame_total(panel, lag=1):
    """Possible differences in the panel's declared frame: every country
    over its full year span, less the lag + 1 lost at the start."""
    span = {}
    for r in panel:
        lo, hi = span.get(r["country"], (r["year"], r["year"]))
        span[r["country"]] = (min(lo, r["year"]), max(hi, r["year"]))
    return sum(max(0, hi - lo + 1 - lag - 1) for lo, hi in span.values())


def g1_read(panel, seed=7):
    diffs = g1_differences(panel)
    total = g1_frame_total(panel)
    n = len(diffs)
    base = dict(covered=n, total=total, unit="country-year differences",
                evidence="CORRELATIONAL")
    share = coverage(n, total)
    core = g1_core(diffs, seed=seed)
    parts = {}
    for v in (True, False):
        sub = [d for d in diffs if d["dependent"] is v]
        parts[v] = g1_core(sub, seed=seed) if len(sub) >= MIN_N else None
    extra = dict(core=core, partitions=parts)
    if share is None or share < COVERAGE_FLOOR:
        return result("G1", "GAP", None,
                      rule="coverage %s under the floor %.2f (CHOICE 2); reading attached"
                      % ("--" if share is None else "%.3f" % share, COVERAGE_FLOOR),
                      **dict(base, **extra))
    if core is None:
        return result("G1", "NOT_EVALUABLE", None,
                      rule="fewer than %d differences" % MIN_N, **dict(base, **extra))
    sig = core["p"] < ALPHA and core["b"] > 0
    if sig and core["b_ctrl"] is not None and \
            abs(core["b_ctrl"]) < ATTENUATION * abs(core["b"]) and core["p_ctrl"] >= ALPHA:
        return result("G1", "MISSED_VARIABLE", core["b_ctrl"],
                      rule="raw slope %.3f falls to %.3f with d price controlled (CHOICE 4)"
                      % (core["b"], core["b_ctrl"]), **dict(base, **extra))
    held = {v: (pc is not None and pc["p"] < ALPHA and pc["b"] > 0)
            for v, pc in parts.items()}
    if parts[True] is not None and parts[False] is not None and held[True] != held[False]:
        where = "dependent" if held[True] else "not dependent"
        return result("G1", "SCOPE_LIMITED", where,
                      rule="holds in the %s partition only" % where, **dict(base, **extra))
    if sig:
        return result("G1", "PATTERN_HOLDS", core["b"],
                      rule="slope %.3f, permutation p %.4f" % (core["b"], core["p"]),
                      **dict(base, **extra))
    return result("G1", "NO_PATTERN", core["b"],
                  rule="slope %.3f, permutation p %.4f%s"
                  % (core["b"], core["p"],
                     "; significant with the opposite sign" if core["p"] < ALPHA else ""),
                  **dict(base, **extra))


def g1_world(kind, seed=1, n_countries=30, n_years=16, missing=0.0, effect=0.8,
             drop_price=False):
    """A constructed country-year panel. kind:
        pressure  d extraction follows last year's d debt in every country
        scoped    ... in the dependent half only
        price     a third variable (price) moves debt now and extraction next year
        null      nothing moves extraction
    `missing` blanks extraction at random. drop_price removes the column the
    missed-variable check needs."""
    rng = random.Random(seed)
    panel = []
    for ci in range(n_countries):
        c = "C%02d" % (ci + 1)
        dep = ci < n_countries // 2
        debt, ext, price = 50.0, 100.0, 100.0
        prev_dd, prev_dp = 0.0, 0.0
        for t in range(n_years):
            if t > 0:
                dp = rng.gauss(0, 1)
                dd = rng.gauss(0, 1) + (dp if kind == "price" else 0.0)
                if kind == "pressure" or (kind == "scoped" and dep):
                    dx = effect * prev_dd + rng.gauss(0, 1)
                elif kind == "price":
                    dx = effect * prev_dp + rng.gauss(0, 1)
                else:
                    dx = rng.gauss(0, 1)
                debt += dd
                price += dp
                ext += dx
                prev_dd, prev_dp = dd, dp
            row = {"country": c, "year": 2000 + t, "debt": debt,
                   "extraction": None if rng.random() < missing else ext,
                   "price": None if drop_price else price, "dependent": dep}
            panel.append(row)
    return panel


def g1_divergence(panel, seed=7):
    """The same world read three ways: a study sampling only the dependent
    countries, one sampling only the rest, and the pooled panel."""
    dep = [r for r in panel if r["dependent"] is True]
    rest = [r for r in panel if r["dependent"] is False]
    return {"dependent only": g1_read(dep, seed=seed),
            "not dependent only": g1_read(rest, seed=seed),
            "pooled": g1_read(panel, seed=seed)}


# --------------------------------------------------------------------------
# G2 -- extracting firm -> beneficial owner

ENTITY_KINDS = ("FIRM", "PERSON", "NOMINEE")
RECORD_STATES = ("DISCLOSED", "UNDISCLOSED", "REGISTRY_ABSENT")
BREAK_TYPES = ("BELOW_THRESHOLD", "UNDISCLOSED", "REGISTRY_ABSENT", "NOMINEE",
               "CYCLE", "DEPTH_LIMIT")


def _brk(node, kind, share, path, entities, juris, cut):
    ent = entities[node]
    tags = []
    if ent["kind"] == "FIRM" and not ent.get("operating", True):
        tags.append("SHELL")
    score = juris.get(ent["jurisdiction"])
    if score is not None and score >= cut:
        tags.append("SECRECY")
    return {"at": node, "type": kind, "share": share, "tags": tuple(tags),
            "path": path + (node,)}


def trace(firm, record, entities, juris, cut=SECRECY_CUT, depth_limit=DEPTH_LIMIT):
    """Walk a firm's observed ownership record to natural persons.

    Effective shares multiply along a path. A walk ends at a PERSON (traced)
    or at a break. Traced share plus break shares is 1 for every firm: the
    shares are conserved, so the unattributed part is a measured fraction
    even where its owner is not known. A NOMINEE is a break because a
    disclosed name is not a beneficial owner."""
    traced = []
    breaks = []

    def walk(node, share, path, depth):
        ent = entities[node]
        if ent["kind"] == "PERSON":
            traced.append({"person": node, "share": share, "path": path + (node,)})
            return
        if ent["kind"] == "NOMINEE":
            breaks.append(_brk(node, "NOMINEE", share, path, entities, juris, cut))
            return
        if node in path:
            breaks.append(_brk(node, "CYCLE", share, path, entities, juris, cut))
            return
        if depth >= depth_limit:
            breaks.append(_brk(node, "DEPTH_LIMIT", share, path, entities, juris, cut))
            return
        rec = record.get(node)
        if rec is None or rec["state"] == "REGISTRY_ABSENT":
            breaks.append(_brk(node, "REGISTRY_ABSENT", share, path, entities, juris, cut))
            return
        if rec["state"] == "UNDISCLOSED":
            breaks.append(_brk(node, "UNDISCLOSED", share, path, entities, juris, cut))
            return
        listed = 0.0
        for owner, s in rec["owners"]:
            listed += s
            walk(owner, share * s, path + (node,), depth + 1)
        resid = 1.0 - listed
        if resid > 1e-12:
            breaks.append(_brk(node, "BELOW_THRESHOLD", share * resid, path,
                               entities, juris, cut))

    walk(firm, 1.0, (), 0)
    return {"firm": firm, "traced": traced, "breaks": breaks,
            "traced_fraction": sum(t["share"] for t in traced)}


def traced_fraction(firm, record, entities, juris):
    """Share of a firm traced to natural persons through its record."""
    return trace(firm, record, entities, juris)["traced_fraction"]


def disclose(truth, entities, threshold=THRESHOLD, undisclosed=(), absent=(),
             unflag_nominees=False):
    """The observed record a register would publish from a true ownership
    graph: owners under the threshold are not listed, entities in
    `undisclosed` publish no owners, entities in `absent` have no record.
    unflag_nominees records a nominee as an ordinary person."""
    rec = {}
    for node, owners in truth.items():
        if node in absent:
            rec[node] = {"state": "REGISTRY_ABSENT", "owners": []}
        elif node in undisclosed:
            rec[node] = {"state": "UNDISCLOSED", "owners": []}
        else:
            rec[node] = {"state": "DISCLOSED",
                         "owners": [(o, s) for o, s in owners if s >= threshold - 1e-12]}
    ents = entities
    if unflag_nominees:
        ents = {k: (dict(v, kind="PERSON") if v["kind"] == "NOMINEE" else v)
                for k, v in entities.items()}
    return rec, ents


def g2_world():
    """A constructed ownership world. Eleven extracting firms E01..E11, each
    built to carry one shape of chain; the shapes are what a register's
    coverage depends on. Every true chain ends at a person, so true coverage
    is 1 and every break below is a property of the record."""
    juris = {"J1": 20, "J2": 35, "J3": 45, "J4": 65, "J5": 75, "J6": 85,
             "J7": 30, "J8": 25}
    E = {}

    def firm(i, j, op=True):
        E[i] = {"kind": "FIRM", "jurisdiction": j, "operating": op}

    def person(i, j):
        E[i] = {"kind": "PERSON", "jurisdiction": j}

    for i, j in [("P01", "J1"), ("P02", "J2"), ("P03", "J7"), ("P04", "J3"),
                 ("P05", "J2"), ("P06", "J8"), ("P07", "J1"), ("P08", "J3"),
                 ("P09", "J1"), ("P14", "J4")]:
        person(i, j)
    for k in range(5):
        person("P2%d" % k, "J2")
    E["N01"] = {"kind": "NOMINEE", "jurisdiction": "J5"}
    for i, j in [("A01", "J1"), ("A02", "J2"), ("A03", "J3")]:
        firm(i, j)
    for i, j in [("H01", "J5"), ("H02", "J2"), ("H03", "J6"), ("H04", "J3"),
                 ("H05", "J4"), ("H06", "J2"), ("H07", "J2"), ("H08", "J1"),
                 ("H09", "J5")]:
        firm(i, j, op=False)
    hosts = {"E01": "J7", "E02": "J7", "E03": "J8", "E04": "J7", "E05": "J8",
             "E06": "J7", "E07": "J8", "E08": "J8", "E09": "J7", "E10": "J8",
             "E11": "J7"}
    for i, j in hosts.items():
        firm(i, j)
    truth = {
        "E01": [("A01", 1.0)],
        "E02": [("A02", 1.0)],
        "E03": [("H01", 0.7), ("P03", 0.3)],
        "E04": [("H02", 1.0)],
        "E05": [("H04", 1.0)],
        "E06": [("A03", 0.6), ("H05", 0.4)],
        "E07": [("H06", 1.0)],
        "E08": [("A01", 1.0)],
        "E09": [("P06", 0.5), ("P07", 0.25), ("H08", 0.25)],
        "E10": [("H01", 1.0)],
        "E11": [("H09", 1.0)],
        "A01": [("P01", 0.6), ("P02", 0.4)],
        "A02": [("P2%d" % k, 0.2) for k in range(5)],
        "A03": [("P04", 1.0)],
        "H01": [("P09", 1.0)],
        "H02": [("H03", 1.0)],
        "H03": [("P05", 1.0)],
        "H04": [("N01", 1.0)],
        "H05": [("P08", 1.0)],
        "H06": [("H07", 0.5), ("P05", 0.5)],
        "H07": [("H06", 1.0)],
        "H08": [("P08", 1.0)],
        "H09": [("P09", 1.0)],
    }
    nominee_for = {"N01": "P14"}
    emissions = {"E01": 10.0, "E02": 8.0, "E03": 12.0, "E04": 6.0, "E05": 5.0,
                 "E06": 9.0, "E07": 4.0, "E08": 7.0, "E09": 3.0, "E10": 11.0,
                 "E11": 6.0}
    return {"juris": juris, "entities": E, "truth": truth, "hosts": hosts,
            "nominee_for": nominee_for, "emissions": emissions,
            "undisclosed": ("H01", "H03"), "absent": ("H05",)}


def g2_record(world, threshold=THRESHOLD, unflag_nominees=False):
    return disclose(world["truth"], world["entities"], threshold,
                    world["undisclosed"], world["absent"], unflag_nominees)


def g2_read(world, threshold=THRESHOLD, cut=SECRECY_CUT, unflag_nominees=False):
    """Per firm: traced fraction and every break. Portfolio: the list of
    breaks, their count by type and by tag, and the emissions-weighted
    traced share as coverage."""
    rec, ents = g2_record(world, threshold, unflag_nominees)
    rows = [trace(f, rec, ents, world["juris"], cut) for f in sorted(world["hosts"])]
    em = world["emissions"]
    total = sum(em.values())
    traced_em = sum(em[r["firm"]] * r["traced_fraction"] for r in rows)
    breaks = [dict(b, firm=r["firm"]) for r in rows for b in r["breaks"]]
    by_type = {}
    for b in breaks:
        by_type[b["type"]] = by_type.get(b["type"], 0) + 1
    by_tag = {"SHELL": 0, "SECRECY": 0, "SHELL+SECRECY": 0, "untagged": 0}
    for b in breaks:
        t = b["tags"]
        if "SHELL" in t and "SECRECY" in t:
            by_tag["SHELL+SECRECY"] += 1
        elif "SHELL" in t:
            by_tag["SHELL"] += 1
        elif "SECRECY" in t:
            by_tag["SECRECY"] += 1
        else:
            by_tag["untagged"] += 1
    branch = "PATTERN_HOLDS" if coverage(traced_em, total) >= COVERAGE_FLOOR else "GAP"
    return result("G2", branch, len(breaks), traced_em, total,
                  "Mt CO2 of extracting firms traced to a person",
                  "%d breaks on %d firms; a break is where the record stops before a person"
                  % (len(breaks), len(rows)), "OBSERVED_JOIN",
                  firms=rows, breaks=breaks, by_type=by_type, by_tag=by_tag,
                  threshold=threshold)


def compliant_coverage(owner_shares, threshold):
    """Share of a firm a fully compliant register traces when owners hold
    `owner_shares` directly and only holdings >= threshold are listed."""
    return sum(s for s in owner_shares if s >= threshold - 1e-12)


# --------------------------------------------------------------------------
# G3 -- ownership-based accounting

TARGETS = ("IMMEDIATE_PARENT", "ULTIMATE_PARENT", "BO_RESIDENCE")


def attribute(path, entities, host, target):
    """The jurisdiction a traced path assigns its emissions to."""
    if target == "BO_RESIDENCE":
        return entities[path[-1]]["jurisdiction"]
    if target == "IMMEDIATE_PARENT":
        return entities[path[1]]["jurisdiction"]
    firms = [n for n in path[1:] if entities[n]["kind"] == "FIRM"]
    return entities[firms[-1]]["jurisdiction"] if firms else host
    # ULTIMATE_PARENT: the top corporate entity; a firm owned directly by a
    # person is its own parent and its host is the home.


def g3_read(world, threshold=THRESHOLD, cut=SECRECY_CUT):
    """Production-based against ownership-based totals per jurisdiction,
    under each target. Unattributed emissions are their own row and are
    never spread over the attributed ones."""
    rec, ents = g2_record(world, threshold)
    em = world["emissions"]
    total = sum(em.values())
    prod = {}
    for f, h in world["hosts"].items():
        prod[h] = prod.get(h, 0.0) + em[f]
    tables = {}
    unattributed = 0.0
    for t in TARGETS:
        tab = {}
        un = 0.0
        for f in sorted(world["hosts"]):
            tr = trace(f, rec, ents, world["juris"], cut)
            for p in tr["traced"]:
                j = attribute(p["path"], ents, world["hosts"][f], t)
                tab[j] = tab.get(j, 0.0) + em[f] * p["share"]
            un += em[f] * (1.0 - tr["traced_fraction"])
        tables[t] = tab
        unattributed = un
    secrecy_home = {t: sum(v for j, v in tab.items()
                           if world["juris"].get(j, 0) >= cut)
                    for t, tab in tables.items()}
    attributed = total - unattributed
    return result("G3", "PATTERN_HOLDS" if coverage(attributed, total) >= COVERAGE_FLOOR
                  else "GAP", None, attributed, total, "Mt CO2 attributed to an owner",
                  "three targets reported, none picked (CHOICE 7)", "DERIVED",
                  production=prod, ownership=tables, unattributed=unattributed,
                  secrecy_home=secrecy_home)


# --------------------------------------------------------------------------
# G4 -- shell-layer attribution loss

def fsi_weight(score):
    """Refused. A secrecy index ranks a jurisdiction's laws; it is not a
    probability that a given chain hides an owner. Multiplying a firm's
    break by it carries a jurisdiction-level ranking down to a chain."""
    raise CrossLevelRefused(
        "a jurisdiction index used as a per-chain concealment weight is a "
        "cross-level transfer; use it only to classify a jurisdiction at a "
        "declared cut (CHOICE 8)")


def g4_read(world, threshold=THRESHOLD, cut=SECRECY_CUT, unflag_nominees=False):
    """The measurement gap itself: emissions the record cannot attribute,
    split by break type and by whether the break sits in a SECRECY
    jurisdiction at the cut. Coverage is the share of firms with any
    ownership record at the first layer."""
    rec, ents = g2_record(world, threshold, unflag_nominees)
    em = world["emissions"]
    total = sum(em.values())
    by_type = {}
    secrecy = 0.0
    shell = 0.0
    lost = 0.0
    firms = sorted(world["hosts"])
    recorded = sum(1 for f in firms if rec.get(f, {}).get("state") != "REGISTRY_ABSENT")
    for f in firms:
        tr = trace(f, rec, ents, world["juris"], cut)
        for b in tr["breaks"]:
            v = em[f] * b["share"]
            lost += v
            by_type[b["type"]] = by_type.get(b["type"], 0.0) + v
            if "SECRECY" in b["tags"]:
                secrecy += v
            if "SHELL" in b["tags"]:
                shell += v
    return result("G4", "GAP", lost / total, recorded, len(firms),
                  "extracting firms with a first-layer record",
                  "the gap is the reading: %.3f of emissions unattributable, %.3f at "
                  "SECRECY breaks (cut %d)" % (lost / total, secrecy / total, cut),
                  "DERIVED", lost=lost, emissions_total=total, secrecy=secrecy, shell=shell,
                  by_type=by_type)


def g4_curve(world, cuts=(40, 50, 60, 70, 80)):
    out = []
    for c in cuts:
        r = g4_read(world, cut=c)
        out.append((c, r["secrecy"] / r["emissions_total"]))
    return out


# --------------------------------------------------------------------------
# G5 -- the visibility filter upstream of the vote

def g5_world(kind, seed=3, n=200, unpolled=0.1):
    """Constructed legislators. kind:
        influence   funding ties move no-voters to yes after the money arrives
        selection   donors fund those already voting yes; no one moves
        preference  votes follow constituency preference; funding is random
    Each row: pref (polling share, None if unpolled), tie (share of traced
    funding from extraction-tied owners), traced (share of funding traced
    to an owner at all), vote_pre, vote_post."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        pref = rng.random()
        if kind == "preference":
            vote_pre = 1 if pref + rng.gauss(0, 0.15) > 0.5 else 0
            tie = rng.random()
            vote_post = vote_pre
        elif kind == "selection":
            vote_pre = 1 if pref + rng.gauss(0, 0.4) > 0.5 else 0
            tie = min(1.0, 0.6 * vote_pre + 0.4 * rng.random())
            vote_post = vote_pre
        else:
            vote_pre = 1 if pref + rng.gauss(0, 0.4) > 0.5 else 0
            tie = rng.random()
            vote_post = 1 if (vote_pre or rng.random() < 0.9 * tie) else 0
        rows.append({"id": "L%03d" % (i + 1),
                     "pref": None if rng.random() < unpolled else pref,
                     "tie": tie, "traced": 0.4 + 0.6 * rng.random(),
                     "vote_pre": vote_pre, "vote_post": vote_post})
    return rows


def g5_filter_world(seed=5, n=400, gate=0.5):
    """Funding gates who sits: only candidates with tie >= gate win. A
    winner votes yes unless constituency preference is very low. Returns
    (candidates, winners)."""
    rng = random.Random(seed)
    cands = []
    for i in range(n):
        tie = rng.random()
        pref = rng.random()
        aligned = tie >= gate
        vote = 1 if (aligned and pref >= 0.2) or (not aligned and pref >= 0.7) else 0
        cands.append({"id": "K%03d" % (i + 1), "pref": pref, "tie": tie,
                      "traced": 1.0, "vote_pre": None, "vote_post": vote,
                      "wins": aligned})
    return cands, [c for c in cands if c["wins"]]


def g5_compare(rows, seed=11, n_boot=N_DRAWS):
    """AUC of tie and of pref for vote_post on the rows where both exist,
    and a bootstrap band of the difference."""
    common = [r for r in rows if r["pref"] is not None and r["tie"] is not None
              and r["vote_post"] is not None]
    a_tie = auc([r["tie"] for r in common], [r["vote_post"] for r in common])
    a_pref = auc([r["pref"] for r in common], [r["vote_post"] for r in common])
    rng = random.Random(seed)
    diffs = []
    for _ in range(n_boot):
        s = [common[rng.randrange(len(common))] for _k in common] if common else []
        t = auc([r["tie"] for r in s], [r["vote_post"] for r in s])
        q = auc([r["pref"] for r in s], [r["vote_post"] for r in s])
        if t is not None and q is not None:
            diffs.append(t - q)
    band = (_pct(diffs, 0.025), _pct(diffs, 0.975)) if diffs else (None, None)
    return {"n": len(common), "auc_tie": a_tie, "auc_pref": a_pref, "band": band}


def g5_mechanism(rows, seed=13):
    """Selection or influence, from timing. Selection: funding already
    predicts the vote cast before the money. Influence: among those voting
    no before, more of the high-tie switch to yes after."""
    pre = [r for r in rows if r["vote_pre"] is not None]
    if not pre:
        return {"reading": "NOT_SEPARABLE", "why": "no vote before the funding period",
                "auc_pre": None, "switch_gap": None, "p": None}
    a_pre = auc([r["tie"] for r in pre], [r["vote_pre"] for r in pre])
    no = [r for r in pre if r["vote_pre"] == 0]
    gap, p = None, None
    if len(no) >= 10:
        med = sorted(r["tie"] for r in no)[len(no) // 2]

        def gap_of(ties):
            hi = [r["vote_post"] for r, t in zip(no, ties) if t >= med]
            lo = [r["vote_post"] for r, t in zip(no, ties) if t < med]
            if not hi or not lo:
                return None
            return sum(hi) / len(hi) - sum(lo) / len(lo)

        ties = [r["tie"] for r in no]
        gap = gap_of(ties)
        rng = random.Random(seed)
        extreme = 0
        for _ in range(N_DRAWS):
            sh = list(ties)
            rng.shuffle(sh)
            g = gap_of(sh)
            if g is not None and gap is not None and g >= gap - 1e-15:
                extreme += 1
        p = (extreme + 1.0) / (N_DRAWS + 1.0)
    sel = a_pre is not None and a_pre >= 0.5 + AUC_MARGIN
    inf = gap is not None and p is not None and p < ALPHA and gap > 0
    reading = {(True, True): "BOTH", (True, False): "SELECTION_CONSISTENT",
               (False, True): "INFLUENCE_CONSISTENT", (False, False): "NEITHER"}[(sel, inf)]
    return {"reading": reading, "auc_pre": a_pre, "switch_gap": gap, "p": p}


def g5_read(rows, seed=11):
    """Does funding traced to extraction-tied owners predict the vote better
    than constituency preference? Branch on the AUC comparison; the
    mechanism reading rides beside it and is not the branch."""
    total = len(rows)
    cmp_ = g5_compare(rows, seed=seed)
    mech = g5_mechanism(rows)
    funds = sum(r["traced"] for r in rows if r["traced"] is not None)
    extra = dict(compare=cmp_, mechanism=mech,
                 funding_traced=coverage(funds, total) if total else None)
    base = dict(covered=cmp_["n"], total=total,
                unit="legislators with polling, traced funding and a vote",
                evidence="CORRELATIONAL")
    share = coverage(cmp_["n"], total)
    if share is None or share < COVERAGE_FLOOR:
        return result("G5", "GAP", None, rule="coverage under the floor", **dict(base, **extra))
    if cmp_["auc_tie"] is None or cmp_["auc_pref"] is None:
        return result("G5", "NOT_EVALUABLE", None,
                      rule="the vote has one value in the sample; AUC undefined",
                      **dict(base, **extra))
    lo, hi = cmp_["band"]
    d = cmp_["auc_tie"] - cmp_["auc_pref"]
    if lo is not None and lo > 0 and d >= AUC_MARGIN:
        return result("G5", "PATTERN_HOLDS", d,
                      rule="funding AUC above preference AUC by %.3f, band [%.3f, %.3f]"
                      % (d, lo, hi), **dict(base, **extra))
    return result("G5", "NO_PATTERN", d,
                  rule="funding AUC minus preference AUC %.3f, band [%.3f, %.3f]"
                  % (d, lo, hi), **dict(base, **extra))


# --------------------------------------------------------------------------
# G6 -- the money token as defense

def reserve_share_band(rev, other, d_reserves):
    """Share of extraction revenue that ends as reserve accumulation.
    Money is fungible, so there is no single value without an allocation
    rule. Returns (lower, proportional, upper):
        lower         other inflows fill reserves first
        proportional  reserves draw on inflows in proportion
        upper         extraction revenue fills reserves first
    None when revenue is absent or zero."""
    if rev is None or other is None or d_reserves is None or rev <= 0:
        return None
    if d_reserves <= 0:
        return (0.0, 0.0, 0.0)
    upper = min(1.0, d_reserves / rev)
    lower = max(0.0, min(1.0, (d_reserves - other) / rev))
    prop = min(1.0, d_reserves / (rev + other))
    return (lower, prop, upper)


def adequacy(reserves, imports, short_debt):
    months = None if not imports else reserves / (imports / 12.0)
    gg = None if not short_debt else reserves / short_debt
    return {"months": months, "gg": gg,
            "short": (months is not None and months < MONTHS_NORM)
            or (gg is not None and gg < GG_NORM)}


def driven_share(*_args, **_kwargs):
    """Refused. 'How much extraction is driven by the need' asks for the
    extraction that would not have happened without the need. An accounting
    identity has no counterfactual in it."""
    raise CausalShareRefused(
        "a driven-by share needs a counterfactual; the balance of payments "
        "gives an allocation band (reserve_share_band), not a cause")


def g6_world(kind, seed=9, n_countries=24, n_years=14):
    """kind: defense (extraction volume rises the year after reserves fall
    short of the norm) or null. Reserve cover in months of imports follows
    an AR(1) around 3.2 months, so a shortfall under the 3-month norm is
    common. Both kinds draw the same random sequence; they differ only in
    whether volume answers a shortfall."""
    rng = random.Random(seed)
    rows = []
    for ci in range(n_countries):
        c = "C%02d" % (ci + 1)
        months = 3.2
        reserves = None
        vol = 100.0
        short_prev = False
        for t in range(n_years):
            imports = 60.0 + 10.0 * rng.random()
            months = 3.2 + 0.6 * (months - 3.2) + rng.gauss(0, 0.8)
            new_res = max(0.5, months) * imports / 12.0
            d_res = None if reserves is None else new_res - reserves
            reserves = new_res
            sd = reserves * (0.5 + 0.4 * rng.random())
            step = rng.gauss(0, 1.5)
            vol += (4.0 + step) if (kind == "defense" and short_prev) else step
            rev = 0.3 * vol
            other = 10.0 + 5.0 * rng.random()
            a = adequacy(reserves, imports, sd)
            rows.append({"country": c, "year": 2010 + t, "rev": rev, "other": other,
                         "d_reserves": d_res, "reserves": reserves, "imports": imports,
                         "short_debt": sd, "volume": vol, "short": a["short"]})
            short_prev = a["short"]
    return rows


def g6_read(rows, seed=17):
    """Accounting band per row and the association of next-year volume
    growth with a reserve shortfall, within country, permutation null."""
    by = {}
    for r in rows:
        by.setdefault(r["country"], []).append(r)
    xs, ys, groups = [], [], []
    for c in sorted(by):
        seq = sorted(by[c], key=lambda r: r["year"])
        idx = []
        for a, b in zip(seq, seq[1:]):
            if None in (a.get("short"), a.get("volume"), b.get("volume")):
                continue
            idx.append(len(xs))
            xs.append(1.0 if a["short"] else 0.0)
            ys.append(b["volume"] - a["volume"])
        if idx:
            groups.append(idx)
    possible = sum(len(v) - 1 for v in by.values())
    bands = [reserve_share_band(r["rev"], r["other"], r["d_reserves"]) for r in rows]
    known = [b for b in bands if b is not None]
    extra = dict(bands_known=len(known), bands_total=len(bands),
                 mean_band=tuple(sum(b[k] for b in known) / len(known) for k in range(3))
                 if known else None)
    base = dict(covered=len(xs), total=possible, unit="country-year transitions",
                evidence="CORRELATIONAL")
    if len(xs) < MIN_N or len(set(xs)) < 2:
        return result("G6", "NOT_EVALUABLE", None,
                      rule="too few transitions or no shortfall years", **dict(base, **extra))
    # a shortfall sits with its country; shuffling it across countries would
    # read a country effect as an association, so the shuffle is within country
    b, p = perm_slope(xs, ys, groups, seed=seed)
    extra["b"], extra["p"] = b, p
    if b is not None and p < ALPHA and b > 0:
        return result("G6", "PATTERN_HOLDS", b,
                      rule="volume growth after a shortfall year higher by %.2f, p %.4f"
                      % (b, p), **dict(base, **extra))
    return result("G6", "NO_PATTERN", b,
                  rule="difference %.2f, p %.4f" % (b if b is not None else float("nan"), p),
                  **dict(base, **extra))


# --------------------------------------------------------------------------
# G7 -- consumption-based correction over time

def consumption_based(pb, eex, eem):
    """Consumption-based emissions: production-based minus emissions
    embodied in exports plus those embodied in imports. None if any term
    is absent."""
    if pb is None or eex is None or eem is None:
        return None
    return pb - eex + eem


def g7_world(cb_lag=2):
    """A constructed exporter X, 2018..2026. Emissions for its own final
    demand (PB - EEX) rise 2% a year throughout; emissions embodied in its
    exports rise to 2023 and then fall, so production-based emissions go
    flat. Consumption-based estimates exist only up to (last year - cb_lag),
    the way a multi-region input-output series trails the production
    series."""
    years = list(range(2018, 2027))
    dom, eex = 8000.0, 2600.0
    rows = []
    for y in years:
        if y > 2018:
            d_dom = 0.02 * dom
            dom += d_dom
            if y <= 2023:
                eex *= 1.01
            else:
                eex -= 0.9 * d_dom   # exports shed most of what demand adds
        pb = dom + eex
        eem = 600.0 + 10.0 * (y - 2018)
        rows.append({"year": y, "pb": pb, "eex": eex if y <= years[-1] - cb_lag else None,
                     "eem": eem if y <= years[-1] - cb_lag else None,
                     "eex_true": eex, "dom_true": dom, "eem_true": eem})
    return rows


def g7_read(rows):
    """Year by year: is production-based flat, what did the domestic and the
    export-embodied parts do, and what was the net embodied transfer
    (exports minus imports)? Coverage is the share of production years that
    also have a consumption-based value. A plateau year past the last
    consumption-based year cannot be read for transfers at all."""
    out = []
    for a, b in zip(rows, rows[1:]):
        dpb = b["pb"] - a["pb"]
        plateau = abs(dpb / a["pb"]) < PLATEAU
        cb = consumption_based(b["pb"], b["eex"], b["eem"])
        cb_prev = consumption_based(a["pb"], a["eex"], a["eem"])
        dcb = None if cb is None or cb_prev is None else cb - cb_prev
        if b["eex"] is not None and a["eex"] is not None:
            d_dom = (b["pb"] - b["eex"]) - (a["pb"] - a["eex"])
            d_eex = b["eex"] - a["eex"]
        else:
            d_dom, d_eex = None, None
        transfer = None if b["eex"] is None or b["eem"] is None else b["eex"] - b["eem"]
        cb_flat = None if dcb is None else abs(dcb / cb_prev) < PLATEAU
        out.append({"year": b["year"], "dpb": dpb, "plateau": plateau, "dcb": dcb,
                    "d_dom": d_dom, "d_eex": d_eex, "transfer": transfer,
                    "cb_flat": cb_flat})
    pb_years = len(rows)
    cb_years = sum(1 for r in rows
                   if consumption_based(r["pb"], r["eex"], r["eem"]) is not None)
    plat = [o for o in out if o["plateau"]]
    measured = [o for o in plat if o["dcb"] is not None]
    unread = [o["year"] for o in plat if o["dcb"] is None]
    base = dict(covered=cb_years, total=pb_years,
                unit="years with a consumption-based value", evidence="DERIVED",
                years=out, measured_plateau=measured, unread_plateau=unread)
    if not plat:
        return result("G7", "NO_PATTERN", None, rule="no plateau year (CHOICE 11)", **base)
    if unread:
        return result("G7", "GAP", unread,
                      rule="%d of %d plateau years are past the last consumption-based "
                           "year; %d measured" % (len(unread), len(plat), len(measured)),
                      **base)
    return result("G7", "PATTERN_HOLDS", [o["year"] for o in measured],
                  rule="every plateau year has a consumption-based value", **base)


# --------------------------------------------------------------------------
# the chain joined

LINKS = (
    # (arrow, unit of the record, evidence class, where it is instrumented)
    ("debt / reserve need -> extraction volume", "country-year", "CORRELATIONAL", "G1, G6"),
    ("extraction volume -> emissions", "firm-year", "DERIVED", "emission factor x volume"),
    ("emissions -> extracting firm", "firm", "OBSERVED_JOIN", "facility operator records"),
    ("extracting firm -> beneficial owner", "firm -> person", "OBSERVED_JOIN", "G2, G3, G4"),
    ("beneficial owner -> funding of leaders", "person -> legislator", "DERIVED",
     "G5: disclosure names matched to owners"),
    ("funding of leaders -> extraction policy", "legislator", "CORRELATIONAL", "G5"),
)


def inference_depth(links=LINKS):
    """Correlational arrows in the chain. Two or more is an inference of an
    inference: a cross-unit association read through another one."""
    return sum(1 for _a, _u, e, _w in links if e == "CORRELATIONAL")


def level_changes(links=LINKS):
    units = [u for _a, u, _e, _w in links]
    return sum(1 for a, b in zip(units, units[1:]) if a != b)


def chain_effect(*_args, **_kwargs):
    """Refused. A product of per-link effects is a composite verdict; the
    order asks for instruments, and the links sit at different units."""
    raise CompositeRefused(
        "no end-to-end effect: the links are read one at a time, with their "
        "own coverage, and are not multiplied through")


def chain_world(seed=19, n=300, coupled=True):
    """Constructed unit records for the end-to-end join, one per extracting
    firm. Each link resolves or not. coupled=True gives a latent secrecy
    flag that makes the ownership, funding-match and emissions links fail
    together; coupled=False draws them independently at the same rates."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        s = rng.random() < 0.3
        if coupled:
            em = rng.random() < (0.75 if s else 0.95)
            bo = rng.random() < (0.15 if s else 0.85)
            fm = rng.random() < (0.25 if s else 0.80)
        else:
            em = rng.random() < 0.3 * 0.75 + 0.7 * 0.95
            bo = rng.random() < 0.3 * 0.15 + 0.7 * 0.85
            fm = rng.random() < 0.3 * 0.25 + 0.7 * 0.80
        rows.append({"id": "E%03d" % (i + 1), "volume": rng.random() < 0.9,
                     "emissions": em, "owner": bo, "funding": fm,
                     "policy": rng.random() < 0.8})
    return rows


CHAIN_FIELDS = ("volume", "emissions", "owner", "funding", "policy")


def chain_read(rows):
    """Joined coverage (every link resolves for the unit) against the
    product of the per-link coverages. They agree only when missingness is
    independent across links."""
    n = len(rows)
    per = {f: coverage(sum(1 for r in rows if r[f]), n) for f in CHAIN_FIELDS}
    joined_n = sum(1 for r in rows if all(r[f] for f in CHAIN_FIELDS))
    product = 1.0
    for f in CHAIN_FIELDS:
        product *= per[f]
    depth = inference_depth()
    return result("CHAIN", "GAP" if coverage(joined_n, n) < COVERAGE_FLOOR else "PATTERN_HOLDS",
                  None, joined_n, n, "units with every link resolved",
                  "joined coverage read directly; the independence product is beside it",
                  "DERIVED", per_link=per, independence_product=product,
                  inference_depth=depth, inference_of_inference=depth >= 2,
                  level_changes=level_changes())


# --------------------------------------------------------------------------
# render

def _all_results():
    out = {}
    out["G1 pressure"] = g1_read(g1_world("pressure"))
    out["G1 scoped"] = g1_read(g1_world("scoped"))
    out["G1 price"] = g1_read(g1_world("price"))
    out["G1 price, column dropped"] = g1_read(g1_world("price", drop_price=True))
    out["G1 null"] = g1_read(g1_world("null"))
    out["G1 sparse"] = g1_read(g1_world("pressure", missing=0.6))
    w = g2_world()
    out["G2"] = g2_read(w)
    out["G3"] = g3_read(w)
    out["G4"] = g4_read(w)
    out["G4 nominee unflagged"] = g4_read(w, unflag_nominees=True)
    for k in ("influence", "selection", "preference"):
        out["G5 %s" % k] = g5_read(g5_world(k))
    cands, winners = g5_filter_world()
    out["G5 filter, candidates"] = g5_read(cands)
    out["G5 filter, winners"] = g5_read(winners)
    out["G6 defense"] = g6_read(g6_world("defense"))
    out["G6 null"] = g6_read(g6_world("null"))
    out["G7"] = g7_read(g7_world())
    out["CHAIN coupled"] = chain_read(chain_world(coupled=True))
    out["CHAIN independent"] = chain_read(chain_world(coupled=False))
    return out


def render():
    L = []
    w = L.append
    w("extraction-chain-join -- instruments for the extraction-money-power-emissions chain")
    w("work order: RECONSTRUCTED from the session summary, not verbatim (ECJ_001)")
    w("every record below is CONSTRUCTED; nothing is about a real country, firm or person")
    w("")
    res = _all_results()
    w("1. every reading, with its coverage")
    for k, r in res.items():
        v = r["value"]
        if isinstance(v, float):
            v = "%.3f" % v
        w("   %-26s %-15s value %-14s %s" % (k, r["branch"], v, cov_text(r)))
    w("")
    w("2. G1 divergence: one constructed world, three samples")
    for k, r in g1_divergence(g1_world("scoped")).items():
        c = r["core"]
        w("   %-20s %-14s slope %s  %s" % (k, r["branch"],
                                          "--" if not c else "%.3f (p %.4f)" % (c["b"], c["p"]),
                                          cov_text(r)))
    w("")
    w("3. G2 breaks, constructed portfolio, threshold %.2f" % THRESHOLD)
    g2 = res["G2"]
    for b in g2["breaks"]:
        w("   %s  at %-4s %-16s share %.3f  tags %s" % (b["firm"], b["at"], b["type"],
                                                    b["share"], "+".join(b["tags"]) or "-"))
    w("   count by type: %s" % ", ".join("%s %d" % kv for kv in sorted(g2["by_type"].items())))
    w("   count by tag : %s" % ", ".join("%s %d" % kv for kv in g2["by_tag"].items()))
    w("   compliant coverage of five 20%% holders: %s"
      % ", ".join("threshold %.2f -> %.2f" % (t, compliant_coverage([0.2] * 5, t))
                  for t in (0.05, 0.10, 0.25)))
    w("")
    w("4. G3 production-based against ownership-based, Mt CO2")
    g3 = res["G3"]
    js = sorted(set(g3["production"]) | set(j for t in g3["ownership"].values() for j in t))
    w("   %-6s %10s %10s %10s %10s" % ("juris", "production", "immediate", "ultimate", "bo"))
    for j in js:
        w("   %-6s %10.2f %10.2f %10.2f %10.2f" % (
            j, g3["production"].get(j, 0.0), g3["ownership"]["IMMEDIATE_PARENT"].get(j, 0.0),
            g3["ownership"]["ULTIMATE_PARENT"].get(j, 0.0),
            g3["ownership"]["BO_RESIDENCE"].get(j, 0.0)))
    w("   %-6s %10s %10.2f %10.2f %10.2f" % ("UNATTR", "", g3["unattributed"],
                                            g3["unattributed"], g3["unattributed"]))
    w("   attributed to a SECRECY jurisdiction: %s"
      % ", ".join("%s %.2f" % (t, v) for t, v in g3["secrecy_home"].items()))
    w("")
    w("5. G4 the gap, by break type, and its secrecy share over the cut")
    g4 = res["G4"]
    for t, v in sorted(g4["by_type"].items()):
        w("   %-16s %.2f Mt  (%.3f of total)" % (t, v, v / g4["emissions_total"]))
    w("   secrecy share by cut: %s" % ", ".join("%d -> %.3f" % cv for cv in g4_curve(g2_world())))
    w("   nominee recorded as a person: gap %.3f -> %.3f (the measured gap is a lower bound)"
      % (res["G4"]["value"], res["G4 nominee unflagged"]["value"]))
    w("")
    w("6. G5 AUC and mechanism")
    for k in ("G5 influence", "G5 selection", "G5 preference",
              "G5 filter, candidates", "G5 filter, winners"):
        c = res[k]["compare"]
        m = res[k]["mechanism"]
        w("   %-22s auc tie %s  auc pref %s  mechanism %s" % (
            k, _f3(c["auc_tie"]), _f3(c["auc_pref"]), m["reading"]))
    w("")
    cands, winners = g5_filter_world()
    w("   filter world: yes share among all candidates %.3f, in the seated chamber %.3f;"
      % (sum(c["vote_post"] for c in cands) / len(cands),
         sum(c["vote_post"] for c in winners) / len(winners)))
    w("   the filter moved the chamber and both samples read NO_PATTERN")
    w("")
    w("7. G6 accounting band and the causal share")
    for k in ("G6 defense", "G6 null"):
        mb = res[k]["mean_band"]
        w("   %-12s mean reserve share of extraction revenue: lower %.3f  "
          "proportional %.3f  upper %.3f  (%d of %d rows have a band)"
          % (k, mb[0], mb[1], mb[2], res[k]["bands_known"], res[k]["bands_total"]))
    w("   the band reads LOWER in the world where volume answers the shortfall:"
      " driven extraction raises revenue past the need")
    w("   driven-by share: refused (no counterfactual in an accounting identity)")
    w("")
    w("8. G7 year by year (constructed exporter; consumption-based series lags 2 years)")
    w("   year     dPB  plateau      dCB  dDomestic  dExportEmb  net transfer")
    for o in res["G7"]["years"]:
        w("   %d %7.1f  %-7s %8s  %9s  %10s  %12s" % (
            o["year"], o["dpb"], o["plateau"], _num(o["dcb"]), _num(o["d_dom"]),
            _num(o["d_eex"]), _num(o["transfer"])))
    for o in res["G7"]["measured_plateau"]:
        w("   %d: production flat, consumption-based %s" % (
            o["year"], "flat" if o["cb_flat"] else "not flat (dCB %.1f)" % o["dcb"]))
    w("   plateau years with no consumption-based value: %s"
      % (", ".join(str(y) for y in res["G7"]["unread_plateau"]) or "none"))
    w("")
    w("9. the chain")
    for a, u, e, wh in LINKS:
        w("   %-42s %-20s %-14s %s" % (a, u, e, wh))
    for k in ("CHAIN coupled", "CHAIN independent"):
        r = res[k]
        w("   %-18s joined %.3f  independence product %.3f" % (
            k, r["coverage"]["share"], r["independence_product"]))
    r = res["CHAIN coupled"]
    w("   correlational arrows %d (inference of inference: %s); unit changes %d"
      % (r["inference_depth"], r["inference_of_inference"], r["level_changes"]))
    w("   end-to-end effect: refused (no composite)")
    return "\n".join(L) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("chain_join.py: checks run in extraction-chain-join/test_chain.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
