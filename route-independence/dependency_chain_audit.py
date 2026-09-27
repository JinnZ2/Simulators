# SPDX-License-Identifier: CC0-1.0
"""dependency_chain_audit.py -- FWO-5. One produced result, every dependency needed
to produce it, and for each dependency whether ANY route to it discharges its
own obligations in its own medium.

    python3 dependency_chain_audit.py            three demo cases + the FWO-6 register tally
    python3 dependency_chain_audit.py --choices  every [CHOICE n] in force
    python3 test_dependency_chain.py             the checks; this module refuses --selftest

EXTENDS FWO-2 (route_independence.py, same folder) and rebuilds none of it.
    per route      ri.discharges_own_obligations(settles_in, obligation_medium, dominant)
    per dependency ri.measure_need(rows, dominant)  -> route_count, independent band, flag
    flag           ri.FLAGS, unchanged: ENCLOSED_PLURALITY NOT_ENCLOSED SINGLE_ROUTE UNKNOWN NOT_EVALUABLE
    ratio          ri.independence_ratio (registered in tools/known_answer.py)
    prior art      ri.cross_check -> effective-redundancy-audit n_eff, or PRIOR_ART_NOT_IMPORTED
    The test asserts by AST that none of those names is defined here.

WHAT THIS ADDS
    result --> dependency (ten categories) --> routes        one FWO-2 need per dependency
        dependency   NOT_NEEDED with a reason, or routes; an empty list with no reason is refused
        route        medium_of_account  = FWO-2 settles_in
                     medium_of_settlement = FWO-2 obligation_medium   (None = UNKNOWN, never a negative)
                     status DERIVED from FWO-2's reading:  None -> UNKNOWN ; True -> INDEPENDENT ; False -> CONVERTED
                     conversion_point   required on CONVERTED, refused elsewhere, closed vocabulary
                     converted_into     the medium the obligation is discharged in (the dominant on every demo row)
                     source             required, typed
                     permitted          recorded, mapped to FWO-2's yes|no|UNKNOWN, and read by NOTHING here
                                        (the order's hard constraint: permitted is not independent; a route
                                        that is legal and taxed at fair market value in USD settles in USD
                                        and reads CONVERTED with no way to write it otherwise)
        result       independence band [lo, hi] over dependencies WITH routes:
                       lo = dependencies whose FWO-2 independent band has min >= 1
                       hi = dependencies whose band has max >= 1
                       None when no dependency carries a route
                     conversion points ordered by DISTINCT DEPENDENCIES routing through each
                     absent_field (category not in the map) kept apart from not_needed (declared)

CHOICES (printed by --choices; cited where each takes effect)
    1  dominant token "USD"; the order's context names dollars
    2  ONE-HOP READING: a route is read at the hop where the producer incurs an obligation
       to obtain the dependency; what the supplier did upstream is the next link of the
       chain, a nested audit, not this route.  Tracing every route to its root makes every
       route CONVERTED by construction and the instrument cannot fail; case (a) is the
       order's own test of that.
    3  a route with no obligation ("none"/"none") is INDEPENDENT under FWO-2's own rule,
       since "none" is a medium equal to itself and not the dominant token
    4  CONVERTED is FWO-2's "does not discharge in its own medium"; converted_into names
       the medium.  On every demo row it is the dominant token.
    5  the result-level band counts a dependency once, whatever its route count
    6  conversion points ordered by distinct dependencies, descending, then by name
    7  register tally: CLUSTERED iff the top layer's count exceeds the sum of every other
       known layer's; entries with an UNKNOWN mechanism are counted apart and enter neither side

EXECUTION
    Authored in a session whose shell was blocked for the whole conversation and pushed
    through the GitHub API.  NOT EXECUTED by its author.  Every number in README /
    CLAIM_TABLE about the demo is a PREDICTION until test_dependency_chain.py has run.

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import route_independence as ri  # noqa: E402  FWO-2, same folder; reused, not rebuilt

DOMINANT = "USD"  # [CHOICE 1]

INDEPENDENT, CONVERTED, UNKNOWN = "INDEPENDENT", "CONVERTED", "UNKNOWN"
NOT_NEEDED = "NOT_NEEDED"
STATUSES = (INDEPENDENT, CONVERTED, UNKNOWN)

CATEGORIES = (
    "instrument", "material_reagent", "facility_space", "energy", "transport",
    "labor", "data_access", "publication", "credential_authorization", "legal_compliance",
)
CONVERSION_POINTS = ("account", "settlement", "input_purchase", "credential", "publication", "tax")
SOURCE_KINDS = ("CONSTRUCTED", "CARRIED", "VERIFIED", "READ")
NONE_MEDIUM = "none"   # [CHOICE 3]

CHOICES = {
    1: "dominant token %r" % DOMINANT,
    2: "one-hop reading: a route is read where the producer incurs the obligation; upstream is the next link",
    3: "a route with no obligation (none/none) is INDEPENDENT under FWO-2's own rule",
    4: "CONVERTED is FWO-2's does-not-discharge; converted_into names the medium",
    5: "the result band counts each dependency once, whatever its route count",
    6: "conversion points ordered by distinct dependencies, descending, then name",
    7: "register: CLUSTERED iff top layer count > sum of other known layers; UNKNOWN entries apart",
}


class RouteError(ValueError):
    """A record the schema refuses; the message names the field."""


# ------------------------------------------------------------------ records ---

def _check_source(source):
    if not isinstance(source, str) or not source:
        raise RouteError("source is required on every record")
    if not any(source.startswith(k) for k in SOURCE_KINDS):
        raise RouteError("source starts with one of %s; got %r" % (SOURCE_KINDS, source))


def _permitted_str(permitted):
    if permitted is None:
        return "UNKNOWN"
    if permitted is True:
        return "yes"
    if permitted is False:
        return "no"
    raise RouteError("permitted is True, False or None (undeclared)")


def route(name, medium_of_account, medium_of_settlement, source,
          conversion_point=None, permitted=None, note=""):
    """One route to a dependency, shaped as an FWO-2 row plus this order's fields.

    status is DERIVED from ri.discharges_own_obligations and never hand-set.
    """
    if not isinstance(name, str) or not name:
        raise RouteError("route name is required")
    _check_source(source)
    settles = "UNKNOWN" if medium_of_account is None else str(medium_of_account)
    oblig = "UNKNOWN" if medium_of_settlement is None else str(medium_of_settlement)
    d = ri.discharges_own_obligations(settles, oblig, DOMINANT)
    status = UNKNOWN if d is None else (INDEPENDENT if d else CONVERTED)   # [CHOICE 4]
    if status == CONVERTED:
        if conversion_point not in CONVERSION_POINTS:
            raise RouteError("CONVERTED route %r needs conversion_point in %s; got %r"
                             % (name, CONVERSION_POINTS, conversion_point))
    elif conversion_point is not None:
        raise RouteError("conversion_point is recorded on CONVERTED routes only; %r is %s"
                         % (name, status))
    return {
        # FWO-2 row fields (ri.measure_need reads route / settles_in / obligation_medium / permitted / sourced)
        "need": None, "route": name, "settles_in": settles, "obligation_medium": oblig,
        "permitted": _permitted_str(permitted), "source": source, "sourced": True, "line": 0,
        # this order's fields
        "status": status, "conversion_point": conversion_point,
        "converted_into": oblig if status == CONVERTED else None, "note": note,
    }


def dependency(category, routes=None, not_needed=None):
    """Routed, OR declared not_needed with a reason. Silence is refused."""
    if category not in CATEGORIES:
        raise RouteError("category %r not in CATEGORIES" % (category,))
    routes = list(routes or [])
    if not_needed is not None and routes:
        raise RouteError("%s: not_needed and routes are exclusive" % category)
    if not_needed is None and not routes:
        raise RouteError("%s: no routes and no not_needed reason; an absence is declared, not implied" % category)
    if not_needed is not None and (not isinstance(not_needed, str) or not not_needed):
        raise RouteError("%s: not_needed carries a reason string" % category)
    names = [r["route"] for r in routes]
    if len(set(names)) != len(names):
        raise RouteError("%s: a route name appears twice" % category)
    for r in routes:
        r["need"] = category
    return {"category": category, "routes": routes, "not_needed": not_needed}


def result(name, dependencies, source):
    _check_source(source)
    cats = [d["category"] for d in dependencies]
    if len(set(cats)) != len(cats):
        raise RouteError("a category appears twice under result %r" % name)
    return {"name": name, "source": source, "dependencies": dict((d["category"], d) for d in dependencies)}


# -------------------------------------------------------------------- audit ---

def _band(v):
    return v if isinstance(v, tuple) else (v, v)


def audit_dependency(dep):
    if dep["not_needed"] is not None:
        return {"category": dep["category"], "flag": NOT_NEEDED, "route_count": 0,
                "independent_band": (0, 0), "converted_count": 0, "unknown_count": 0,
                "conversion_points": [], "cross_check": "NOT_RUN", "n_eff": None,
                "not_needed": dep["not_needed"]}
    m = ri.measure_need(dep["routes"], DOMINANT)          # FWO-2's measure, unchanged
    lo, hi = _band(m["independent_count"])
    cc = ri.cross_check(m)
    return {
        "category": dep["category"], "flag": m["flag"], "route_count": m["route_count"],
        "independent_band": (lo, hi),
        "converted_count": sum(1 for r in dep["routes"] if r["status"] == CONVERTED),
        "unknown_count": len(m["unknown_routes"]),
        "conversion_points": sorted(set(r["conversion_point"] for r in dep["routes"] if r["conversion_point"])),
        "cross_check": cc["status"], "n_eff": cc.get("n_eff"),
        "not_needed": None,
    }


def audit(res):
    deps = res["dependencies"]
    rows = [audit_dependency(deps[c]) for c in CATEGORIES if c in deps]
    absent = [c for c in CATEGORIES if c not in deps]
    not_needed = [r["category"] for r in rows if r["flag"] == NOT_NEEDED]
    routed = [r for r in rows if r["route_count"] > 0]
    lo_rows = [r["category"] for r in routed if r["independent_band"][0] >= 1]
    hi_rows = [r["category"] for r in routed if r["independent_band"][1] >= 1]
    n = len(routed)                                                      # [CHOICE 5]
    lo_ratio, hi_ratio = ri.independence_ratio(len(lo_rows), n), ri.independence_ratio(len(hi_rows), n)
    ratio = lo_ratio if lo_ratio == hi_ratio else (lo_ratio, hi_ratio)
    counts = {}
    for r in rows:
        for cp in r["conversion_points"]:
            counts[cp] = counts.get(cp, 0) + 1
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))     # [CHOICE 6]
    return {
        "result": res["name"], "source": res["source"], "rows": rows,
        "absent_field": absent, "not_needed": not_needed,
        "routed_count": n, "independent_rows": lo_rows,
        "possibly_independent_rows": [c for c in hi_rows if c not in lo_rows],
        "independence_ratio": ratio,
        "enclosed": [r["category"] for r in rows if r["flag"] == ri.ENCLOSED_PLURALITY],
        "conversion_points_ordered": ordered,
    }


# --------------------------------------------------------------- demo cases ---
# (a) CONSTRUCTED: one declared household, no person, no site.  (b) names a real
# open-access finding as the INSTANCE and codes the GENERIC dependency structure of
# its venue class; nothing is a statement about that paper's production, which was
# not read (its host refuses CONNECT).  (c) CONSTRUCTED case; the tax treatment is
# CARRIED from the order and not re-read.

def case_a_household():
    src = "CONSTRUCTED: one declared household observation record; no person, no site"
    return result("a_household_phenology", [
        dependency("instrument", [
            route("eye and memory", NONE_MEDIUM, NONE_MEDIUM, src),
            route("paper notebook, bought", DOMINANT, DOMINANT, src, conversion_point="input_purchase"),
        ]),
        dependency("material_reagent", not_needed="no consumable is used"),
        dependency("facility_space", [route("own land, occupancy", NONE_MEDIUM, NONE_MEDIUM, src,
                                            note="the tax on the land is legal_compliance, not this route")]),
        dependency("energy", [route("daylight", NONE_MEDIUM, NONE_MEDIUM, src)]),
        dependency("transport", [route("on foot", NONE_MEDIUM, NONE_MEDIUM, src)]),
        dependency("labor", [route("own time, no obligation", NONE_MEDIUM, NONE_MEDIUM, src)]),
        dependency("data_access", [route("own observation", NONE_MEDIUM, NONE_MEDIUM, src)]),
        dependency("publication", [route("notebook, unshared; whether it is ever disseminated is undeclared",
                                         NONE_MEDIUM, None, src)]),
        dependency("credential_authorization", not_needed="no authorization is required to look at one's own land"),
        dependency("legal_compliance", [route("property tax on the land", DOMINANT, DOMINANT,
                                              "CARRIED: property tax is assessed and paid in dollars; not read",
                                              conversion_point="tax", permitted=True)]),
    ], src)


B_INSTANCE = ("Kalai, Nachum, Vempala & Zhang, Nature 653:1047-1051 (2026), DOI 10.1038/s41586-026-10549-w; "
              "already cited in this tree (publication-loop-work-orders, WO-11 T-6a); "
              "NOT READ here: www.nature.com refuses CONNECT under the egress allowlist")


def case_b_open_access():
    src = "CARRIED: generic dependency structure of an open-access journal article; not read from the named instance"
    usd = DOMINANT
    return result("b_open_access_finding", [
        dependency("instrument", [
            route("purchased on a grant", usd, usd, src, conversion_point="input_purchase"),
            route("core-facility recharge", usd, usd, src, conversion_point="settlement"),
        ]),
        dependency("material_reagent", [route("vendor purchase", usd, usd, src, conversion_point="input_purchase")]),
        dependency("facility_space", [route("institutional space via indirect costs", usd, usd, src, conversion_point="settlement")]),
        dependency("energy", [route("utility, billed", usd, usd, src, conversion_point="input_purchase")]),
        dependency("transport", [route("shipping", usd, usd, src, conversion_point="input_purchase")]),
        dependency("labor", [
            route("salary", usd, usd, src, conversion_point="settlement"),
            route("stipend", usd, usd, src, conversion_point="settlement"),
        ]),
        dependency("data_access", [
            route("open dataset; obligation is citation, discharged in citation", "citation", "citation", src),
            route("licensed database", usd, usd, src, conversion_point="input_purchase"),
        ]),
        dependency("publication", [
            route("article processing charge", usd, usd, src, conversion_point="publication"),
            route("preprint deposit; no obligation at this hop", NONE_MEDIUM, NONE_MEDIUM, src,
                  note="[CHOICE 2] hosting is the next link"),
        ]),
        dependency("credential_authorization", [route("degree; tuition", usd, usd, src, conversion_point="credential")]),
        dependency("legal_compliance", [route("grant reporting; tax on salary", usd, usd, src, conversion_point="tax")]),
    ], "CARRIED: instance " + B_INSTANCE)


def case_c_bitcoin_exit():
    irs = "CARRIED: IRS Notice 2014-21, virtual currency treated as property, gain or loss computed in dollars on disposal; not re-read"
    con = "CONSTRUCTED: one physical need met by acquiring and disposing of bitcoin; no person, no exchange named"
    usd = DOMINANT
    return result("c_bitcoin_exit", [
        dependency("instrument", [route("own ledger / wallet; holding incurs no obligation at this hop", "BTC", "BTC", con)]),
        dependency("material_reagent", [
            route("the physical good, priced in dollars", usd, usd, con, conversion_point="input_purchase"),
            route("a vendor accepting bitcoin; what its obligations settle in is undeclared", "BTC", None, con),
        ]),
        dependency("facility_space", not_needed="no space is needed to hold a key"),
        dependency("energy", [
            route("network fee, paid in bitcoin to whoever includes the transaction", "BTC", "BTC", con),
            route("electricity for a node, billed", usd, usd, con, conversion_point="input_purchase"),
        ]),
        dependency("transport", [route("delivery of the good", usd, usd, con, conversion_point="input_purchase")]),
        dependency("labor", [route("own time", NONE_MEDIUM, NONE_MEDIUM, con)]),
        dependency("data_access", [route("public chain", NONE_MEDIUM, NONE_MEDIUM, con)]),
        dependency("publication", not_needed="nothing is disseminated"),
        dependency("credential_authorization", [route("identity check at acquisition; what it settles in is undeclared",
                                                      NONE_MEDIUM, None, con)]),
        dependency("legal_compliance", [
            route("disposal is a taxable event; gain or loss denominated in dollars", "BTC", usd, irs,
                  conversion_point="settlement", permitted=True),
            route("penalty for non-reporting, denominated in dollars", usd, usd, irs, conversion_point="settlement"),
        ]),
    ], con)


DEMO_CASES = (case_a_household, case_b_open_access, case_c_bitcoin_exit)


def _lo(aud):
    return _band(aud["independence_ratio"])[0]


# Expected demo structure, REGISTERED before the first run: the order's own table
# made checkable.  A MISMATCH is recorded, never tuned away.
EXPECTED = {
    "a_household_phenology": [
        ("ratio_low_end_at_least_0.5", lambda a: a["independence_ratio"] is not None and _lo(a) >= 0.5),
        ("publication_not_independent", lambda a: "publication" not in a["independent_rows"]),
        ("not_fully_converted", lambda a: len(a["independent_rows"]) > 0),
    ],
    "b_open_access_finding": [
        ("ratio_at_most_0.25", lambda a: a["independence_ratio"] is not None and _band(a["independence_ratio"])[1] <= 0.25),
        ("enclosed_on_instrument", lambda a: "instrument" in a["enclosed"]),
        ("enclosed_on_labor", lambda a: "labor" in a["enclosed"]),
        ("enclosed_on_publication", lambda a: "publication" in a["enclosed"]),
    ],
    "c_bitcoin_exit": [
        ("ledger_route_independent", lambda a: "instrument" in a["independent_rows"]),
        ("legal_conversion_point_is_settlement",
         lambda a: [r for r in a["rows"] if r["category"] == "legal_compliance"][0]["conversion_points"] == ["settlement"]),
    ],
}


def check_expectations(aud):
    return [(label, "MATCH" if bool(fn(aud)) else "MISMATCH") for label, fn in EXPECTED.get(aud["result"], [])]


# ------------------------------------------------------- FWO-6 register tally ---

REGISTER_PATH = os.path.join(HERE, "conversion_register.json")
LAYER_HYPOTHESIS = "settlement"   # PROPOSED, Claude's, stated in the order before any tally


def load_register(path=REGISTER_PATH):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    for e in data["entries"]:
        for k in ("id", "changed", "reconversions", "source"):
            if k not in e:
                raise RouteError("register entry missing %r" % k)
        for rc in e["reconversions"]:
            for k in ("mechanism", "layer", "source"):
                if k not in rc:
                    raise RouteError("reconversion in %s missing %r" % (e["id"], k))
    return data["entries"]


def register_tally(entries):
    """Counts only. CLUSTERED / SPREAD per [CHOICE 7]. No entry is rated."""
    by_mech, by_layer = {}, {}
    unknown_entries = []
    for e in entries:
        mechs = set(rc["mechanism"] for rc in e["reconversions"])
        layers = set(rc["layer"] for rc in e["reconversions"] if rc["mechanism"] != "UNKNOWN")
        if "UNKNOWN" in mechs:
            unknown_entries.append(e["id"])
        for m in mechs:
            if m != "UNKNOWN":
                by_mech[m] = by_mech.get(m, 0) + 1
        for lay in layers:
            by_layer[lay] = by_layer.get(lay, 0) + 1
    ordered = sorted(by_layer.items(), key=lambda kv: (-kv[1], kv[0]))
    if not ordered:
        reading, top = "NO_KNOWN_LAYER", None
    else:
        top = ordered[0]
        reading = "CLUSTERED" if top[1] > sum(c for _, c in ordered[1:]) else "SPREAD"
    if reading == "CLUSTERED" and top[0] == LAYER_HYPOTHESIS:
        hyp = "CONSISTENT_ON_THIS_REGISTER"
    elif reading == "NO_KNOWN_LAYER":
        hyp = "NOT_EVALUABLE"
    else:
        hyp = "NOT_SUPPORTED_ON_THIS_REGISTER"
    return {"entries": len(entries), "by_mechanism": by_mech, "by_layer_ordered": ordered,
            "unknown_entries": unknown_entries, "reading": reading, "top_layer": top,
            "hypothesis": LAYER_HYPOTHESIS, "hypothesis_reading": hyp}


# ------------------------------------------------------------------- render ---

def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("dependency_chain_audit -- FWO-5 over FWO-2; demo on CONSTRUCTED / CARRIED values, nothing read from a source\n")
    w("dominant token %s; flags and bands are route_independence.py's; cross-check is effective_redundancy n_eff\n\n" % DOMINANT)
    for fn in DEMO_CASES:
        aud = audit(fn())
        w("== %s\n   source: %s\n" % (aud["result"], aud["source"]))
        w("   %-26s %6s %8s %4s %4s  %-20s %-22s %s\n" % (
            "dependency", "routes", "ind band", "conv", "unk", "flag", "cross-check", "conversion points"))
        for r in aud["rows"]:
            band = "%d..%d" % r["independent_band"] if r["independent_band"][0] != r["independent_band"][1] \
                else "%d" % r["independent_band"][0]
            cc = r["cross_check"] + ("" if r["n_eff"] is None else " n_eff=%d" % r["n_eff"])
            w("   %-26s %6d %8s %4d %4d  %-20s %-22s %s\n" % (
                r["category"], r["route_count"], band, r["converted_count"], r["unknown_count"],
                r["flag"], cc, ",".join(r["conversion_points"]) or "--"))
        w("   independence band %s over %d routed dependencies; absent_field %s; not_needed %s\n" % (
            ri._fmt(aud["independence_ratio"]), aud["routed_count"], aud["absent_field"] or "[]", aud["not_needed"] or "[]"))
        w("   enclosed_plurality %s; independent rows %s; possibly independent (UNKNOWN routes) %s\n" % (
            aud["enclosed"] or "[]", aud["independent_rows"] or "[]", aud["possibly_independent_rows"] or "[]"))
        w("   conversion points by dependency count: %s\n" % (
            ", ".join("%s=%d" % kv for kv in aud["conversion_points_ordered"]) or "--"))
        for label, verdict in check_expectations(aud):
            w("   expected %-36s %s\n" % (label, verdict))
        w("\n")
    if os.path.exists(REGISTER_PATH):
        t = register_tally(load_register())
        w("== FWO-6 conversion-point register: counts, no verdict on any attempt\n")
        w("   entries %d; with an UNKNOWN mechanism %s\n" % (t["entries"], t["unknown_entries"] or "[]"))
        w("   by mechanism: %s\n" % (", ".join("%s=%d" % kv for kv in sorted(t["by_mechanism"].items())) or "--"))
        w("   by layer:     %s\n" % (", ".join("%s=%d" % kv for kv in t["by_layer_ordered"]) or "--"))
        w("   reading %s; hypothesis (PROPOSED, Claude, stated before tally) top layer = %s -> %s\n"
          % (t["reading"], t["hypothesis"], t["hypothesis_reading"]))
    else:
        w("== FWO-6 register: conversion_register.json ABSENT; tally NOT_RUN\n")
    w("\nchoices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_dependency_chain.py prints the check count; samples/dependency_chain.sample.txt is one recorded render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_dependency_chain.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
