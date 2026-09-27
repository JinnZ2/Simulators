# SPDX-License-Identifier: CC0-1.0
"""Checks for dependency_chain_audit.py (FWO-5, FWO-6).

Run:  python3 route-independence/test_dependency_chain.py
Prints the check count; nothing stores it. Every demo expectation below is a
PREDICTION written by hand before this file was ever executed (the authoring
session had no shell). A mismatch on first run is a finding about the author's
arithmetic and is to be recorded in CLAIM_TABLE.md, not smoothed.
"""
import ast
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import dependency_chain_audit as D   # noqa: E402
import route_independence as ri      # noqa: E402

_checks = 0
_failed = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def refuses(fn, needle, msg):
    try:
        fn()
    except D.RouteError as e:
        check(needle in str(e), "%s (refusal names %r; got %s)" % (msg, needle, e))
        return
    check(False, "%s (expected a refusal naming %r)" % (msg, needle))


def screen():
    path = os.path.join(HERE, "..", "sheet-structure-scan", "no_severity.py")
    if not os.path.exists(path):
        return None
    spec = importlib.util.spec_from_file_location("no_severity", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SRC = "CONSTRUCTED: test"
ind = lambda n: D.route(n, "hours", "hours", SRC)                                   # noqa: E731
conv = lambda n, cp="tax": D.route(n, "USD", "USD", SRC, conversion_point=cp)       # noqa: E731
unk = lambda n: D.route(n, "BTC", None, SRC)                                        # noqa: E731


def t_reuse():
    src = open(os.path.join(HERE, "dependency_chain_audit.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    defined = set(n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    for name in ("discharges_own_obligations", "measure_need", "flag_for", "independence_ratio",
                 "cross_check", "parse_routes", "n_eff"):
        check(name not in defined, "%s is FWO-2's / prior art's and is not redefined here" % name)
    check("import route_independence as ri" in src, "FWO-2 is imported by module name from the same folder")
    for banned in ("import urllib", "import socket", "import http", "import requests", "import subprocess"):
        check(banned not in src, "no network or subprocess import (%s)" % banned)
    check(src.startswith("# SPDX-License-Identifier: CC0-1.0"), "CC0 header")


def t_route():
    r = D.route("x", "USD", "USD", SRC, conversion_point="tax")
    check(r["status"] == D.CONVERTED and r["converted_into"] == "USD", "settlement in the dominant token is CONVERTED")
    r = D.route("x", "hours", "hours", SRC)
    check(r["status"] == D.INDEPENDENT and r["converted_into"] is None, "own medium, not dominant, is INDEPENDENT")
    r = D.route("x", "BTC", None, SRC)
    check(r["status"] == D.UNKNOWN and r["obligation_medium"] == "UNKNOWN", "undeclared settlement is UNKNOWN, never a negative")
    check(D.route("x", None, "hours", SRC)["settles_in"] == "UNKNOWN", "undeclared account recorded as UNKNOWN")
    r = D.route("x", "hours", "citation", SRC, conversion_point="publication")
    check(r["status"] == D.CONVERTED and r["converted_into"] == "citation",
          "[CHOICE 4] a mismatch into a non-dominant medium is CONVERTED into that medium")
    check(D.route("x", "none", "none", SRC)["status"] == D.INDEPENDENT, "[CHOICE 3] no obligation is INDEPENDENT")
    check(ri.discharges_own_obligations("none", "none", "USD") is True, "and that is FWO-2's own reading")
    # permitted: recorded, mapped, consulted by nothing
    a = D.route("x", "USD", "USD", SRC, conversion_point="tax", permitted=True)
    b = D.route("x", "USD", "USD", SRC, conversion_point="tax", permitted=False)
    c = D.route("x", "USD", "USD", SRC, conversion_point="tax", permitted=None)
    check(a["status"] == b["status"] == c["status"] == D.CONVERTED, "permitted flips nothing")
    check((a["permitted"], b["permitted"], c["permitted"]) == ("yes", "no", "UNKNOWN"), "permitted mapped to FWO-2's vocabulary")
    refuses(lambda: D.route("x", "USD", "USD", SRC, conversion_point="tax", permitted="yes"), "permitted", "permitted string refused")
    src = open(os.path.join(HERE, "dependency_chain_audit.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    for fn in ("route", "audit_dependency", "audit"):
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == fn)
        reads = [n for n in ast.walk(node) if isinstance(n, ast.Subscript)
                 and isinstance(n.slice, ast.Constant) and n.slice.value == "permitted"]
        check(not reads, "%s never reads r['permitted']" % fn)
    # conversion_point: required on CONVERTED, refused elsewhere, closed vocabulary
    refuses(lambda: D.route("x", "USD", "USD", SRC), "conversion_point", "CONVERTED without a point")
    refuses(lambda: D.route("x", "USD", "USD", SRC, conversion_point="vibes"), "conversion_point", "point outside vocabulary")
    refuses(lambda: D.route("x", "hours", "hours", SRC, conversion_point="tax"), "CONVERTED routes only", "point on INDEPENDENT")
    refuses(lambda: D.route("x", "BTC", None, SRC, conversion_point="tax"), "CONVERTED routes only", "point on UNKNOWN")
    # source typed and required
    refuses(lambda: D.route("x", "hours", "hours", ""), "source", "empty source")
    refuses(lambda: D.route("x", "hours", "hours", "from memory"), "source", "untyped source")
    refuses(lambda: D.result("r", [], "guess"), "source", "untyped result source")
    refuses(lambda: D.route("", "hours", "hours", SRC), "name", "empty name")


def t_dependency():
    refuses(lambda: D.dependency("energy"), "not_needed", "no routes and no reason")
    refuses(lambda: D.dependency("energy", [ind("a")], not_needed="no"), "exclusive", "both routes and reason")
    refuses(lambda: D.dependency("energy", not_needed=""), "reason", "empty reason")
    refuses(lambda: D.dependency("vibes", not_needed="n/a"), "CATEGORIES", "unknown category")
    refuses(lambda: D.dependency("energy", [ind("a"), ind("a")]), "twice", "duplicate route name")
    refuses(lambda: D.result("r", [D.dependency("energy", not_needed="a"), D.dependency("energy", not_needed="b")], SRC),
            "twice", "duplicate category")
    d = D.dependency("energy", [ind("a")])
    check(d["routes"][0]["need"] == "energy", "the route learns its need from the dependency")


def t_flags():
    row = D.audit_dependency(D.dependency("energy", not_needed="x"))
    check(row["flag"] == D.NOT_NEEDED and row["route_count"] == 0, "NOT_NEEDED is this order's state")
    check(D.audit_dependency(D.dependency("energy", [conv("a"), conv("b", "settlement")]))["flag"] == ri.ENCLOSED_PLURALITY,
          "two converted -> FWO-2's ENCLOSED_PLURALITY")
    check(D.audit_dependency(D.dependency("energy", [conv("a"), ind("b")]))["flag"] == ri.NOT_ENCLOSED, "one independent -> NOT_ENCLOSED")
    check(D.audit_dependency(D.dependency("energy", [conv("a"), unk("b")]))["flag"] == ri.UNKNOWN, "band straddles 0 -> UNKNOWN")
    check(D.audit_dependency(D.dependency("energy", [conv("a")]))["flag"] == ri.SINGLE_ROUTE, "one route -> SINGLE_ROUTE")
    # a limit of the imported instrument, surfaced by wrapping it (RIN_024): route_count == 1
    # is tested before the band, so a single UNKNOWN route reads SINGLE_ROUTE, not UNKNOWN.
    row = D.audit_dependency(D.dependency("energy", [unk("a")]))
    check(row["flag"] == ri.SINGLE_ROUTE and row["unknown_count"] == 1 and row["independent_band"] == (0, 1),
          "single UNKNOWN route: FWO-2 flag SINGLE_ROUTE, unknown_count 1 carried beside it")
    check(ri.flag_for(1, 0, 1) == ri.SINGLE_ROUTE, "and that ordering is FWO-2's own")
    # cross-check is the imported prior art
    row = D.audit_dependency(D.dependency("energy", [conv("a"), conv("b", "settlement"), ind("c")]))
    check(row["cross_check"] in ("AGREE", "PRIOR_ART_NOT_IMPORTED"), "cross-check runs or reports the sibling absent")
    if row["cross_check"] == "AGREE":
        check(row["n_eff"] == 2, "n_eff: one independent + one collapsed bundle = 2")
    row = D.audit_dependency(D.dependency("energy", [unk("a")]))
    check(row["cross_check"] in ("NOT_EVALUABLE", "PRIOR_ART_NOT_IMPORTED") and row["n_eff"] is None,
          "cross-check refuses to code an UNKNOWN route")


def t_result():
    res = D.result("r", [D.dependency("energy", not_needed="x"), D.dependency("labor", [unk("a")])], SRC)
    aud = D.audit(res)
    check(aud["independence_ratio"] == (0.0, 1.0) and aud["routed_count"] == 1,
          "one routed dependency with an UNKNOWN route: band [0, 1], not a point")
    check(aud["not_needed"] == ["energy"] and len(aud["absent_field"]) == 8, "not_needed and absent_field kept apart")
    aud = D.audit(D.result("r", [D.dependency("energy", not_needed="x")], SRC))
    check(aud["independence_ratio"] is None and aud["routed_count"] == 0, "no routed dependency -> None, never 0.0")
    res = D.result("r", [D.dependency("energy", [ind("a")]), D.dependency("labor", [conv("a")])], SRC)
    check(D.audit(res)["independence_ratio"] == 0.5, "point ratio when every dependency is decided")
    res = D.result("r", [
        D.dependency("energy", [conv("a", "tax"), conv("b", "tax")]),
        D.dependency("labor", [conv("a", "input_purchase")]),
        D.dependency("transport", [conv("a", "input_purchase")]),
    ], SRC)
    check(D.audit(res)["conversion_points_ordered"] == [("input_purchase", 2), ("tax", 1)],
          "[CHOICE 6] two routes through tax in one dependency count once")


def t_demo():
    A = D.audit(D.case_a_household())
    B = D.audit(D.case_b_open_access())
    C = D.audit(D.case_c_bitcoin_exit())
    # (a) predicted: 8 routed, 6 certainly independent, publication possibly (its one route is UNKNOWN)
    check(A["routed_count"] == 8 and A["independence_ratio"] == (0.75, 0.875), "case a: band [6/8, 7/8]")
    check(A["not_needed"] == ["material_reagent", "credential_authorization"] and A["absent_field"] == [],
          "case a: two declared not_needed, none absent")
    check(A["possibly_independent_rows"] == ["publication"], "case a: publication is the possibly-independent row")
    check([v for _, v in D.check_expectations(A)] == ["MATCH"] * 3, "case a meets its registered expectations")
    check(A["enclosed"] == [], "case a: nothing enclosed")
    # (b) predicted: 10 routed, 2 independent, enclosed on instrument and labor, publication NOT enclosed
    check(B["routed_count"] == 10 and B["independence_ratio"] == 0.2, "case b: 2 of 10, a point")
    check(B["enclosed"] == ["instrument", "labor"], "case b: enclosed on instrument and labor")
    check(B["independent_rows"] == ["data_access", "publication"], "case b: data_access and publication carry an independent route")
    ex = dict(D.check_expectations(B))
    check(ex["enclosed_on_publication"] == "MISMATCH", "case b: the order's publication expectation MISMATCHES, recorded")
    check(ex["ratio_at_most_0.25"] == "MATCH" and ex["enclosed_on_instrument"] == "MATCH" and ex["enclosed_on_labor"] == "MATCH",
          "case b: the other three hold")
    # (c) predicted: 8 routed, 4 certain, 2 possible; legal enclosed; input_purchase leads
    check(C["routed_count"] == 8 and C["independence_ratio"] == (0.5, 0.75), "case c: band [4/8, 6/8]")
    check(C["enclosed"] == ["legal_compliance"], "case c: enclosed on legal_compliance only")
    check(C["possibly_independent_rows"] == ["material_reagent", "credential_authorization"], "case c: the two UNKNOWN-route rows")
    check(C["conversion_points_ordered"] == [("input_purchase", 3), ("settlement", 1)], "case c: input_purchase 3, settlement 1")
    check([v for _, v in D.check_expectations(C)] == ["MATCH", "MATCH"], "case c meets both registered expectations")
    for aud in (A, B, C):
        for r in aud["rows"]:
            if r["route_count"]:
                check(r["cross_check"] in ("AGREE", "NOT_EVALUABLE", "PRIOR_ART_NOT_IMPORTED"),
                      "%s/%s: prior art never DISAGREEs with FWO-2 on the demo" % (aud["result"], r["category"]))


def t_register():
    entries = D.load_register()
    T = D.register_tally(entries)
    check(T["entries"] == 8, "eight register entries")
    check(dict(T["by_layer_ordered"]) == {"production": 6, "settlement": 4, "legal": 1, "publication": 1}, "layer counts as coded")
    check(T["reading"] == "SPREAD" and T["hypothesis_reading"] == "NOT_SUPPORTED_ON_THIS_REGISTER",
          "as coded the register SPREADS; the SETTLEMENT hypothesis is not supported on it")
    check(sorted(T["unknown_entries"]) == ["gift_across_households", "mutual_aid_networks", "open_hardware_communities", "time_banks"],
          "entries carrying an UNKNOWN mechanism, counted apart")
    mk = lambda i, layer: {"id": i, "changed": [], "source": "CONSTRUCTED",                       # noqa: E731
                           "reconversions": [{"mechanism": "tax", "layer": layer, "source": "CONSTRUCTED"}]}
    Tc = D.register_tally([mk("a", "settlement"), mk("b", "settlement"), mk("c", "settlement"), mk("d", "production")])
    check(Tc["reading"] == "CLUSTERED" and Tc["hypothesis_reading"] == "CONSISTENT_ON_THIS_REGISTER",
          "a constructed settlement-heavy register reads CLUSTERED and consistent")
    Tp = D.register_tally([mk("a", "production"), mk("b", "production"), mk("c", "production"), mk("d", "settlement")])
    check(Tp["reading"] == "CLUSTERED" and Tp["hypothesis_reading"] == "NOT_SUPPORTED_ON_THIS_REGISTER",
          "CLUSTERED on another layer is not support")
    check(D.register_tally([])["hypothesis_reading"] == "NOT_EVALUABLE", "empty register is NOT_EVALUABLE, not SPREAD")
    for e in entries:
        for rc in e["reconversions"]:
            head = rc["source"].split(":")[0].split(" ")[0]
            check(head in ("CARRIED", "VERIFIED", "CONSTRUCTED", "READ", "UNKNOWN"), "typed source on %s" % e["id"])


def t_cli_and_render():
    check(D.main(["--selftest"]) == 2, "module refuses --selftest")
    check(D.main(["--choices"]) == 0 and len(D.CHOICES) == 7, "seven choices in force")
    buf = io.StringIO()
    D.render(buf)
    txt = buf.getvalue()
    check("MISMATCH" in txt and "MATCH" in txt, "render shows both expectation outcomes on the demo")
    check("FWO-6" in txt and "SPREAD" in txt, "render carries the register tally")
    ns = screen()
    if ns is None:
        check(True, "no_severity not beside this folder; screen NOT_RUN")
    else:
        clean, hits = ns.check(txt)
        check(clean, "render screens clean: %s" % hits[:3])
        planted, _ = ns.check("this row is wrong")
        check(not planted, "screen fires on a plant")


if __name__ == "__main__":
    t_reuse()
    t_route()
    t_dependency()
    t_flags()
    t_result()
    t_demo()
    t_register()
    t_cli_and_render()
    print("dependency-chain: %d checks, %d failed" % (_checks, _failed))
    sys.exit(1 if _failed else 0)
