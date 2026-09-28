# SPDX-License-Identifier: CC0-1.0
"""edge_taxonomy.py -- FWO-8. Two fields added to FWO-5's per-route record:
how the money medium enters a step (edge_class) and which side of the
person it couples to (coupling_side). Never one number for both.

    python3 edge_taxonomy.py             the three FWO-5 cases re-read under the two fields
    python3 edge_taxonomy.py --choices   every [CHOICE n] in force
    python3 test_single_channel.py       the checks; this module refuses --selftest

EXTENDS FWO-5 (dependency_chain_audit.py) and rebuilds none of it: the three
cases, the route records, the FWO-2 status derivation and the audit are all
D's. This module adds fields to a route COPY and reads them. The test asserts
by AST that no FWO-5 name is redefined here.

edge_class     CARRIED from a pasted third-party model output; audited, not authored.
               DIRECT | INSTITUTIONAL | ACCESS | MEASUREMENT | TEMPORAL | RECURSIVE | UNKNOWN
               Recorded on CONVERTED routes. On an INDEPENDENT route the money medium
               does not enter, so the field is None with that reason, kept apart from
               UNKNOWN (an entry nobody could classify) -- the conversion_point
               discipline of FWO-5, one field over.  [CHOICE 1]
coupling_side  PROPOSED (the order's).  SURVIVAL | SELECTION | BOTH | UNKNOWN
               Same placement rule as edge_class.
edge_basis     required on every annotation: the reading is a declared judgement, and
               a declared judgement without its basis is a label.

HARD CONSTRAINT (the order's): a route coupled on SURVIVAL only is scored INDEPENDENT
at the selection layer.  layer_status(route, layer) returns one layer's reading; there
is no function returning both, no sum, no product, no mean over the two.  The test
walks the AST for that.

WHAT RE-READING THE FWO-5 CASES SHOWS (the two-layer question)
    FWO-5's route carries medium_of_account and medium_of_settlement.  A route
    CONVERTED at input_purchase and one CONVERTED at settlement both read USD/USD on
    those two fields; the pair cannot tell them apart.  conversion_point could, but it
    is a label the author writes, not a field the schema derives.  edge_class is the
    field that separates them on this reading: every case-(c) input_purchase row is
    ACCESS (the good exists; the purchase gates it) and every case-(c) settlement row
    is INSTITUTIONAL (physically dischargeable without dollars; a rule requires them).
    misplacement_report() prints, per case, every pair of CONVERTED routes whose
    account/settlement media are identical and whose conversion points differ.

KEY-HOLDER STATUS
    EXPECTED_2026-09-27b.md was committed before this file existed (rule 1).  The
    inputs are FWO-5's three cases, CONSTRUCTED / CARRIED, and every annotation below
    is this session's reading with its basis stated -- rule 2 is NOT met and no hold
    here is scored as independent of its author.  fail_fixture() is a constructed case
    carrying a DIRECT route so the DIRECT-empty expectation can be shown to fail
    (rule 3).

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D  # noqa: E402  FWO-5, reused

EDGE_CLASSES = ("DIRECT", "INSTITUTIONAL", "ACCESS", "MEASUREMENT", "TEMPORAL", "RECURSIVE", "UNKNOWN")
COUPLING_SIDES = ("SURVIVAL", "SELECTION", "BOTH", "UNKNOWN")
LAYERS = ("selection", "survival")
NOT_ENTERING = "money does not enter this route (INDEPENDENT); field not applicable"

CHOICES = {
    1: "edge_class / coupling_side recorded on CONVERTED routes; None with a reason on INDEPENDENT; "
       "UNKNOWN on UNKNOWN-status routes unless declared otherwise",
    2: "'near-empty' for the DIRECT expectation is at most ONE route across the three cases (EXPECTED E8.1)",
    3: "a bundled route (two obligations under one name) takes the side of the more selective half and says so in edge_basis",
    4: "the misplacement report compares CONVERTED routes pairwise within one dependency AND across a case; "
       "identical (account, settlement) media with differing conversion points is the reported shape",
}


class EdgeError(ValueError):
    """An annotation the schema refuses; the message names the field."""


def annotate(route, edge_class, coupling_side, edge_basis):
    """Return a COPY of an FWO-5 route carrying the two fields and their basis.

    The FWO-5 record is not modified: D.route() still derives status, and this
    copy keeps every FWO-5 key so D's audit reads it unchanged.
    """
    if not isinstance(edge_basis, str) or not edge_basis.strip():
        raise EdgeError("edge_basis is required on every annotation")
    st = route["status"]
    if st == D.INDEPENDENT:
        if edge_class is not None or coupling_side is not None:
            raise EdgeError("%r is INDEPENDENT: money does not enter; edge_class/coupling_side are None [CHOICE 1]"
                            % route["route"])
    else:
        if edge_class not in EDGE_CLASSES:
            raise EdgeError("edge_class on %r must be one of %s; got %r" % (route["route"], EDGE_CLASSES, edge_class))
        if coupling_side not in COUPLING_SIDES:
            raise EdgeError("coupling_side on %r must be one of %s; got %r"
                            % (route["route"], COUPLING_SIDES, coupling_side))
        if st == D.UNKNOWN and edge_class != "UNKNOWN" and "declared" not in edge_basis:
            raise EdgeError("%r has UNKNOWN status; a non-UNKNOWN edge_class needs a basis saying 'declared'"
                            % route["route"])
    out = dict(route)
    out["edge_class"] = edge_class
    out["coupling_side"] = coupling_side
    out["edge_basis"] = edge_basis if st != D.INDEPENDENT else NOT_ENTERING + "; " + edge_basis
    return out


def layer_status(route, layer):
    """One layer's reading of one route. Two calls give two readings; nothing joins them."""
    if layer not in LAYERS:
        raise EdgeError("layer is one of %s" % (LAYERS,))
    if "coupling_side" not in route:
        raise EdgeError("route %r is not annotated" % route["route"])
    st, side = route["status"], route["coupling_side"]
    if st == D.INDEPENDENT:
        return D.INDEPENDENT
    if side == "UNKNOWN" or st == D.UNKNOWN:
        return D.UNKNOWN
    if side == "BOTH":
        return st
    if layer == "selection":
        return D.INDEPENDENT if side == "SURVIVAL" else st      # the order's hard constraint
    return D.INDEPENDENT if side == "SELECTION" else st


def annotate_case(res, table):
    """Annotate every route of an FWO-5 result from a {(category, route): (edge, side, basis)} table.

    A route the table does not name is REFUSED: an annotation is declared, never
    defaulted, and a missing row would otherwise read as UNKNOWN silently.
    """
    out = {"name": res["name"], "source": res["source"], "dependencies": {}}
    for cat, dep in res["dependencies"].items():
        routes = []
        for r in dep["routes"]:
            key = (cat, r["route"])
            if key not in table:
                raise EdgeError("no annotation for %s / %r" % key)
            routes.append(annotate(r, *table[key]))
        out["dependencies"][cat] = {"category": cat, "routes": routes, "not_needed": dep["not_needed"]}
    extra = [k for k in table if k[0] not in res["dependencies"]
             or k[1] not in [r["route"] for r in res["dependencies"][k[0]]["routes"]]]
    if extra:
        raise EdgeError("annotation table names routes the case does not have: %s" % extra)
    return out


def routes_of(case):
    for cat in D.CATEGORIES:
        dep = case["dependencies"].get(cat)
        if dep:
            for r in dep["routes"]:
                yield cat, r


def class_tally(case):
    t = dict((c, 0) for c in EDGE_CLASSES)
    t["none_not_entering"] = 0
    for _, r in routes_of(case):
        if r["edge_class"] is None:
            t["none_not_entering"] += 1
        else:
            t[r["edge_class"]] += 1
    return t


def direct_rows(case):
    return [(cat, r["route"], r["edge_basis"]) for cat, r in routes_of(case) if r["edge_class"] == "DIRECT"]


def layer_rows(case, layer):
    """Dependency categories with at least one route INDEPENDENT at that layer."""
    out = []
    for cat in D.CATEGORIES:
        dep = case["dependencies"].get(cat)
        if dep and any(layer_status(r, layer) == D.INDEPENDENT for r in dep["routes"]):
            out.append(cat)
    return out


def misplacement_report(case):
    """Where the two-layer (account, settlement) schema has no slot for a conversion.  [CHOICE 4]

    Per conversion point: how many CONVERTED routes carry it, how many of those have
    an (account, settlement) media pair identical to a route carrying a DIFFERENT
    point in the same case (so the pair alone cannot place the conversion), and
    which edge classes those routes take.  A point whose every route collides is a
    point the two-layer schema cannot place from its own fields.
    """
    conv = [(cat, r) for cat, r in routes_of(case) if r["status"] == D.CONVERTED]
    by_point = {}
    for cat, r in conv:
        by_point.setdefault(r["conversion_point"], []).append(r)
    rows = []
    for cp in D.CONVERSION_POINTS:
        rs = by_point.get(cp)
        if not rs:
            continue
        others = [(o["settles_in"], o["obligation_medium"]) for _, o in conv if o["conversion_point"] != cp]
        collide = sum(1 for r in rs if (r["settles_in"], r["obligation_medium"]) in others)
        rows.append({"conversion_point": cp, "routes": len(rs), "media_collide": collide,
                     "edge_classes": sorted(set(r["edge_class"] for r in rs)),
                     "no_slot": collide == len(rs)})
    return {"result": case["name"], "converted_routes": len(conv), "by_point": rows,
            "points_without_slot": [r["conversion_point"] for r in rows if r["no_slot"]]}


# ------------------------------------------------- the three cases, annotated ---
# Every row is this session's reading.  Basis strings are the argument, in place.
# rule 2 (external SOURCE for demo inputs) is NOT met here; see the docstring.

_A = {
    ("instrument", "eye and memory"): (None, None, "none/none route"),
    ("instrument", "paper notebook, bought"): (
        "ACCESS", "SURVIVAL", "paper exists; the purchase gates the object, not the observation; nothing about "
                              "WHAT is observed moves with it"),
    ("facility_space", "own land, occupancy"): (None, None, "none/none route"),
    ("energy", "daylight"): (None, None, "none/none route"),
    ("transport", "on foot"): (None, None, "none/none route"),
    ("labor", "own time, no obligation"): (None, None, "none/none route"),
    ("data_access", "own observation"): (None, None, "none/none route"),
    ("publication", "notebook, unshared; whether it is ever disseminated is undeclared"): (
        "UNKNOWN", "UNKNOWN", "settlement medium undeclared in FWO-5; nothing to classify"),
    ("legal_compliance", "property tax on the land"): (
        "INSTITUTIONAL", "SURVIVAL", "holding land is physically possible without dollars; a rule requires them; "
                                     "the tax does not touch what is observed on the land"),
}

_B = {
    ("instrument", "purchased on a grant"): (
        "RECURSIVE", "SELECTION", "the grant buys the instrument that produces the result that is cited in the next "
                                  "grant; the grant's call decides what is bought and so what is worked on"),
    ("instrument", "core-facility recharge"): (
        "ACCESS", "SELECTION", "the facility exists; recharge gates the hours; the recharge is grant-funded so the "
                               "grant's scope reaches the choice"),
    ("material_reagent", "vendor purchase"): (
        "ACCESS", "SELECTION", "reagent exists; the purchase order is against a grant line that names the project"),
    ("facility_space", "institutional space via indirect costs"): (
        "INSTITUTIONAL", "SELECTION", "space is physically available; the indirect-cost rule ties it to funded work"),
    ("energy", "utility, billed"): (
        "ACCESS", "UNKNOWN", "power exists; the bill gates it; whether the bill reaches the choice of work or only "
                             "the institution's survival is not decidable from the generic structure"),
    ("transport", "shipping"): (
        "ACCESS", "UNKNOWN", "carriage exists; payment gates it; side not decidable from the generic structure"),
    ("labor", "salary"): (
        "TEMPORAL", "BOTH", "money decides whether the hours can be allocated at all; a salaried post both meets "
                            "needs and names the work"),
    ("labor", "stipend"): (
        "TEMPORAL", "BOTH", "as salary; a stipend is tied to a programme that names the work"),
    ("data_access", "open dataset; obligation is citation, discharged in citation"): (None, None, "citation/citation route"),
    ("data_access", "licensed database"): (
        "ACCESS", "SELECTION", "the data exist; the licence gates them; which licence is bought is a project decision"),
    ("publication", "article processing charge"): (
        "INSTITUTIONAL", "SELECTION", "publishing is physically possible without a charge; the venue's rule requires "
                                      "it; the charge decides which venue, i.e. what is worked toward"),
    ("publication", "preprint deposit; no obligation at this hop"): (None, None, "none/none route"),
    ("credential_authorization", "degree; tuition"): (
        "INSTITUTIONAL", "SELECTION", "the competence is physically acquirable without tuition; the credential rule "
                                      "requires it and the programme names the field"),
    ("legal_compliance", "grant reporting; tax on salary"): (
        "INSTITUTIONAL", "BOTH", "bundled route [CHOICE 3]: tax on salary reaches survival only; grant reporting "
                                 "reaches selection; the more selective half decides the side"),
}

_C = {
    ("instrument", "own ledger / wallet; holding incurs no obligation at this hop"): (None, None, "BTC/BTC route"),
    ("material_reagent", "the physical good, priced in dollars"): (
        "ACCESS", "SURVIVAL", "the good exists; the dollar price gates it; the need is the person's and the choice of "
                              "work is untouched"),
    ("material_reagent", "a vendor accepting bitcoin; what its obligations settle in is undeclared"): (
        "UNKNOWN", "UNKNOWN", "settlement medium undeclared in FWO-5"),
    ("energy", "network fee, paid in bitcoin to whoever includes the transaction"): (None, None, "BTC/BTC route"),
    ("energy", "electricity for a node, billed"): (
        "ACCESS", "SURVIVAL", "power exists; the bill gates it; running a node is not a choice of work in this case"),
    ("transport", "delivery of the good"): (
        "ACCESS", "SURVIVAL", "carriage exists; payment gates it"),
    ("labor", "own time"): (None, None, "none/none route"),
    ("data_access", "public chain"): (None, None, "none/none route"),
    ("credential_authorization", "identity check at acquisition; what it settles in is undeclared"): (
        "UNKNOWN", "UNKNOWN", "settlement medium undeclared in FWO-5"),
    ("legal_compliance", "disposal is a taxable event; gain or loss denominated in dollars"): (
        "INSTITUTIONAL", "SURVIVAL", "the disposal is physically complete in bitcoin; a rule denominates the gain in "
                                     "dollars and requires them; the rule does not reach what the person works on"),
    ("legal_compliance", "penalty for non-reporting, denominated in dollars"): (
        "INSTITUTIONAL", "SURVIVAL", "a rule; same reading as the taxable event"),
}

TABLES = {"a_household_phenology": _A, "b_open_access_finding": _B, "c_bitcoin_exit": _C}


def annotated_cases():
    out = []
    for fn in D.DEMO_CASES:
        res = fn()
        out.append(annotate_case(res, TABLES[res["name"]]))
    return out


def fail_fixture():
    """CONSTRUCTED: one case carrying a DIRECT route, so the DIRECT-empty expectation FAILS on it.

    Two coin-operated mechanisms: the coin is the mechanical input that moves each.
    Two, because E8.1 admits one DIRECT route across the cases [CHOICE 2] and a
    fail fixture has to cross the line it is built to cross.  Labelled constructed
    in its source; it is not a claim about any gate.
    """
    src = "CONSTRUCTED: fail fixture for EXPECTED E8.1; a coin-operated mechanism; no site"
    res = D.result("z_fail_fixture_direct", [
        D.dependency("facility_space", [
            D.route("coin-operated gate", D.DOMINANT, D.DOMINANT, src, conversion_point="input_purchase"),
            D.route("coin-operated turnstile", D.DOMINANT, D.DOMINANT, src, conversion_point="input_purchase")]),
        D.dependency("labor", [D.route("own time", D.NONE_MEDIUM, D.NONE_MEDIUM, src)]),
    ], src)
    return annotate_case(res, {
        ("facility_space", "coin-operated gate"): (
            "DIRECT", "SURVIVAL", "CONSTRUCTED: the coin is the physical input that releases the mechanism"),
        ("facility_space", "coin-operated turnstile"): (
            "DIRECT", "SURVIVAL", "CONSTRUCTED: second DIRECT route, so the at-most-one expectation fails"),
        ("labor", "own time"): (None, None, "none/none route"),
    })


# ------------------------------------------------------------- expectations ---
# Copied from EXPECTED_2026-09-27b.md; the commit that registered them is cited in
# CLAIM_TABLE.md.  A MISMATCH is recorded, never tuned away.

def check_expectations(cases):
    by = dict((c["name"], c) for c in cases)
    direct = sum(len(direct_rows(c)) for c in cases)
    rows = [("E8.1 DIRECT at most one route across the cases [CHOICE 2]", direct <= 1)]
    ok = True
    for c in cases:
        for _, r in routes_of(c):
            if r["status"] == D.CONVERTED and r["edge_class"] not in ("INSTITUTIONAL", "ACCESS", "TEMPORAL", "RECURSIVE"):
                ok = False
    rec = sum(class_tally(c)["RECURSIVE"] for c in cases)
    meas_ac = sum(class_tally(by[n])["MEASUREMENT"] for n in ("a_household_phenology", "c_bitcoin_exit") if n in by)
    rows.append(("E8.2 CONVERTED routes take INSTITUTIONAL/ACCESS/TEMPORAL; RECURSIVE at most once; "
                 "no MEASUREMENT in (a) or (c)", ok and rec <= 1 and meas_ac == 0))
    if "b_open_access_finding" in by:
        aud = D.audit(by["b_open_access_finding"])
        rows.append(("E8.4 row-level: case (b) independent rows == ['data_access']", aud["independent_rows"] == ["data_access"]))
        rows.append(("E8.4 route-level: data_access and publication each carry an independent route",
                     set(c for c, r in routes_of(by["b_open_access_finding"]) if r["status"] == D.INDEPENDENT)
                     == {"data_access", "publication"}))
    if "c_bitcoin_exit" in by:
        c = by["c_bitcoin_exit"]
        ip = [r for _, r in routes_of(c) if r["conversion_point"] == "input_purchase"]
        rows.append(("E8.5 every case-(c) input_purchase row reads ACCESS and USD/USD",
                     bool(ip) and all(r["edge_class"] == "ACCESS" and (r["settles_in"], r["obligation_medium"])
                                      == (D.DOMINANT, D.DOMINANT) for r in ip)))
    return [(label, "MATCH" if v else "MISMATCH") for label, v in rows]


# ------------------------------------------------------------------- render ---

def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("edge_taxonomy -- FWO-8 over FWO-5; the three cases re-read under edge_class and coupling_side\n")
    w("every annotation is this session's reading with its basis in the table; inputs CONSTRUCTED / CARRIED "
      "(key-holder rule 2 NOT met)\n\n")
    cases = annotated_cases()
    for c in cases:
        w("== %s\n" % c["name"])
        w("   %-24s %-46s %-11s %-13s %-9s %-11s %s\n" % (
            "dependency", "route", "status", "edge_class", "side", "sel-layer", "surv-layer"))
        for cat, r in routes_of(c):
            w("   %-24s %-46s %-11s %-13s %-9s %-11s %s\n" % (
                cat, r["route"][:46], r["status"], r["edge_class"] or "--", r["coupling_side"] or "--",
                layer_status(r, "selection"), layer_status(r, "survival")))
        t = class_tally(c)
        w("   tally: %s; not entering %d\n" % (
            ", ".join("%s=%d" % (k, t[k]) for k in EDGE_CLASSES), t["none_not_entering"]))
        w("   DIRECT rows: %s\n" % (direct_rows(c) or "[]"))
        w("   independent at selection layer: %s\n" % (layer_rows(c, "selection") or "[]"))
        w("   independent at survival layer:  %s\n" % (layer_rows(c, "survival") or "[]"))
        m = misplacement_report(c)
        w("   two-layer schema: %d CONVERTED routes; points the (account, settlement) pair cannot place: %s\n"
          % (m["converted_routes"], m["points_without_slot"] or "[]"))
        for p in m["by_point"]:
            w("      %-16s routes %d  media collide with another point %d  edge classes %s\n"
              % (p["conversion_point"], p["routes"], p["media_collide"], ",".join(p["edge_classes"])))
        w("\n")
    for label, verdict in check_expectations(cases):
        w("expected %-100s %s\n" % (label, verdict))
    ff = fail_fixture()
    w("\nfail fixture (CONSTRUCTED): %s\n" % ["%s %s" % (l, v) for l, v in check_expectations([ff])][0])
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_single_channel.py prints the check count; samples/edge_taxonomy.sample.txt is one "
      "recorded render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_single_channel.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
