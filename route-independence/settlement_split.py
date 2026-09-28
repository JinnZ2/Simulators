# SPDX-License-Identifier: CC0-1.0
"""settlement_split.py -- AMENDMENT A-1 to FWO-5 / FWO-8: settlement vs gate-removal.

    python3 settlement_split.py             the three FWO-5 cases re-scored under the split
    python3 settlement_split.py --choices   every [CHOICE n] in force
    python3 test_settlement_split.py        the checks; this module refuses --selftest

EXTENDS FWO-5 (dependency_chain_audit.py) and FWO-8 (edge_taxonomy.py) and rebuilds
neither: every route is D.route()'s record, COPIED and given the amendment's fields.
The test asserts by AST that no FWO-5 or FWO-8 name is defined here.

THE AMENDMENT'S OBSERVATION (section 1)
    FWO-5's field medium_of_settlement is filled on every route, whether the route
    discharges a CLAIM another party holds (a fine, a price, a tax) or removes a GATE
    between a body and a physical requirement (metered water).  One word, two operations.

WHAT THIS ADDS, per route copy
    obligation_origin   CONSTRUCTED | BIOLOGICAL | UNDECIDED       required; UNDECIDED is the
                        migration default and a row carrying it is NOT scored (scorable() False)
    settles_claim       True | False | None(undeclared)           the split, field 1
    removes_gate        True | False | None(undeclared)           the split, field 2
                        An edge may carry either, both, or neither.  NO function here reads the
                        two into one value; the test walks the AST for any expression naming both.
    reads_requirement_as_claim   True when origin is BIOLOGICAL and settles_claim is True: the
                        reading the amendment's section 2 says is unsupported.  A FLAG, not a
                        refusal -- the instrument records the reading and marks it.
    origin_basis        required: a declared origin without its basis is a label

    token_type          MONETARY | CITATION | CREDENTIAL | SOCIAL_STANDING | OTHER_NAMED | NONE
    converts_to         the token this one converts into, if observed; else None
    hops_to_monetary    int >= 0, or UNMEASURED, or None(not applicable, token NONE)
    horizon_status(route, hops)   one route's reading at a horizon of `hops` conversions:
                        FWO-5's own status if it is not INDEPENDENT at hop 1; else NONE token ->
                        INDEPENDENT; UNMEASURED hops -> UNKNOWN (never INDEPENDENT: fixture F-A4);
                        an integer h <= hops -> CONVERTED with the hop recorded; h > hops ->
                        INDEPENDENT at this horizon, with h printed beside it.

E-A2, ANSWERED BEFORE ANY OF THIS WAS WRITTEN AND CONFIRMED BY RUNNING
    FWO-5 does NOT force a settlement reading on the rainwater fixture: D.route() with
    medium none/none returns INDEPENDENT under its own [CHOICE 3], obligation_medium
    'none'.  unamended_reading() prints exactly what FWO-5 returns for F-A3.  What
    FWO-5 DOES do is read F-A1 (a fine) and F-A2 (metered water) IDENTICALLY on every
    field it derives: status CONVERTED, media USD/USD, converted_into USD.  The one
    field that separates them, conversion_point, is a label the author writes.  So the
    meld is in the code, one row over from where the amendment predicted it:
    indistinguishable_under_fwo5() is that measurement.

THE SYMMETRY ARGUMENT (section 2) AS ARITHMETIC
    net_positions(claims)   claims[i][j] = what party i holds against party j.  A universal
                        uniform claim (everyone against everyone, equal) nets to zero for
                        every party: C1.  A claim held by some against all leaves a positive
                        net position: the placing party, C2's second branch.  both_sides()
                        lists parties holding and owing on one instrument: P4.  Arithmetic
                        on the premise; it establishes nothing about any real instrument.

CHOICES (printed by --choices; cited where each takes effect)
    1  BIOLOGICAL is declared only where the requirement is on the amendment's own list
       (water, food, air, shelter, warmth); CONSTRUCTED where a party's claim is discharged;
       a route carrying neither (own time, daylight, own observation) stays UNDECIDED with
       a reason and is COUNTED APART.  The vocabulary has no member for it; that is reported.
    2  a CONSTRUCTED claim interposed on a biological requirement (property tax on the land
       one lives on) carries BOTH settles_claim and removes_gate True; that is the case the
       amendment's C2 names, and the field pair is what lets it be seen
    3  token NONE carries hops_to_monetary None (not applicable), kept apart from UNMEASURED
    4  E-A1 is scored on DECIDED rows; UNDECIDED rows are listed and counted, never read as
       either origin; 'zero BIOLOGICAL edges' means zero DECLARED BIOLOGICAL
    5  the case-(b) token chain citation -> credential -> funding is the amendment's own
       stated chain, CARRIED; hops_to_monetary 2 on the citation route is that declaration
       and not an observation of any conversion
    6  the preprint deposit route in case (b) carries token NONE: its obligation at this hop
       is none, and the citations a deposit may later earn are what it returns, not what
       gates it.  The alternative reading (token CITATION, hops as the citation route) is
       the falsifier for RIN_060 and is printed, not taken.

KEY-HOLDER STATUS
    The amendment's section 5 is the EXPECTED block; the amendment was committed alone at
    bacaeab before this file existed (rule 1).  Inputs are FWO-5's three cases and every
    declaration is this session's reading with its basis stated: rule 2 is NOT met and
    no hold here is independent of its author.  Two fail fixtures: F-A3, which the
    amendment designates, and on which E-A2 FAILS; and fail_fixture(), three constructed
    cases on which E-A1 FAILS (rule 3).

Stdlib only. Parses under Python 3.8. No network. CC0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D  # noqa: E402  FWO-5, reused

ORIGINS = ("CONSTRUCTED", "BIOLOGICAL", "UNDECIDED")
CONSTRUCTED, BIOLOGICAL, UNDECIDED = ORIGINS
TOKEN_TYPES = ("MONETARY", "CITATION", "CREDENTIAL", "SOCIAL_STANDING", "OTHER_NAMED", "NONE")
UNMEASURED = "UNMEASURED"
BIOLOGICAL_LIST = ("water", "food", "air", "shelter", "warmth")   # [CHOICE 1] the amendment's own list
EXPECTED_COMMIT = "bacaeab"

CHOICES = {
    1: "BIOLOGICAL only where the requirement is on the amendment's list %s; CONSTRUCTED where a party's claim "
       "is discharged; neither -> UNDECIDED with a reason, counted apart" % (BIOLOGICAL_LIST,),
    2: "a placed claim interposed on a biological requirement carries settles_claim AND removes_gate True",
    3: "token NONE carries hops_to_monetary None (not applicable), apart from UNMEASURED",
    4: "E-A1 scored on DECIDED rows; UNDECIDED listed and counted, read as neither origin",
    5: "case-(b) chain citation -> credential -> funding is the amendment's own statement, CARRIED; hops 2 is that declaration",
    6: "preprint deposit carries token NONE; the CITATION reading is printed as the falsifier, not taken",
}


class SplitError(ValueError):
    """A record the amendment's schema refuses; the message names the field."""


# ------------------------------------------------------------------ fields ---

def migrate(route):
    """The amendment's migration: a COPY of an FWO-5 route with origin UNDECIDED and the
    split undeclared.  Nothing is auto-assigned."""
    out = dict(route)
    out["obligation_origin"] = UNDECIDED
    out["settles_claim"] = None
    out["removes_gate"] = None
    out["origin_basis"] = "migrated: UNDECIDED until declared"
    out["reads_requirement_as_claim"] = None
    return out


def _tri(v, name, route):
    if v not in (True, False, None):
        raise SplitError("%s on %r is True, False or None (undeclared); got %r" % (name, route, v))
    return v


def declare(route, origin, settles_claim, removes_gate, basis):
    """Declare the three amendment fields on a COPY of an FWO-5 route.

    UNDECIDED may be declared explicitly, with the reason in basis [CHOICE 1]; it still
    does not score.  BIOLOGICAL with settles_claim True is admitted and FLAGGED.
    """
    if origin not in ORIGINS:
        raise SplitError("obligation_origin on %r is one of %s; got %r" % (route["route"], ORIGINS, origin))
    if not isinstance(basis, str) or not basis.strip():
        raise SplitError("origin_basis is required on %r" % route["route"])
    sc = _tri(settles_claim, "settles_claim", route["route"])
    rg = _tri(removes_gate, "removes_gate", route["route"])
    if origin == UNDECIDED and (sc is not None or rg is not None):
        raise SplitError("%r: UNDECIDED carries no split declaration; declare the origin first" % route["route"])
    out = migrate(route)
    out["obligation_origin"] = origin
    out["settles_claim"] = sc
    out["removes_gate"] = rg
    out["origin_basis"] = basis
    out["reads_requirement_as_claim"] = (origin == BIOLOGICAL and sc is True)
    return out


def scorable(route):
    """The amendment: a row may NOT be scored until obligation_origin is set."""
    if "obligation_origin" not in route:
        raise SplitError("route %r has not been migrated" % route["route"])
    return route["obligation_origin"] != UNDECIDED


def split_of(route):
    """One route's position on the split, as a name.  Reads the two fields SEPARATELY
    into a label; never into a number."""
    if not scorable(route):
        return "UNDECIDED"
    sc, rg = route["settles_claim"], route["removes_gate"]
    if sc is None or rg is None:
        return "UNDECLARED_HALF"
    if sc and rg:
        return "BOTH"
    if sc:
        return "CLAIM_ONLY"
    if rg:
        return "GATE_ONLY"
    return "NEITHER"


# ------------------------------------------------------------------- tokens ---

def token(route, token_type, converts_to, hops_to_monetary, basis):
    """The FWO-8 additions on a COPY of a route."""
    if token_type not in TOKEN_TYPES:
        raise SplitError("token_type on %r is one of %s; got %r" % (route["route"], TOKEN_TYPES, token_type))
    if converts_to is not None and converts_to not in TOKEN_TYPES:
        raise SplitError("converts_to on %r is a token type or None; got %r" % (route["route"], converts_to))
    if not isinstance(basis, str) or not basis.strip():
        raise SplitError("token_basis is required on %r" % route["route"])
    h = hops_to_monetary
    if token_type == "NONE":
        if h is not None:
            raise SplitError("%r: token NONE carries hops None (not applicable) [CHOICE 3]" % route["route"])
    elif token_type == "MONETARY":
        if h != 0:
            raise SplitError("%r: token MONETARY carries hops 0" % route["route"])
    else:
        if h != UNMEASURED and not (isinstance(h, int) and not isinstance(h, bool) and h >= 1):
            raise SplitError("%r: hops_to_monetary is an int >= 1 or UNMEASURED; got %r" % (route["route"], h))
        if h == UNMEASURED and converts_to is not None:
            raise SplitError("%r: an observed converts_to with UNMEASURED hops is contradictory" % route["route"])
    out = dict(route)
    out["token_type"] = token_type
    out["converts_to"] = converts_to
    out["hops_to_monetary"] = h
    out["token_basis"] = basis
    return out


def horizon_status(route, hops):
    """One route's reading at a horizon of `hops` conversions.  Returns (status, hop_or_None, note)."""
    if "token_type" not in route:
        raise SplitError("route %r carries no token fields" % route["route"])
    if not isinstance(hops, int) or isinstance(hops, bool) or hops < 1:
        raise SplitError("hops is an int >= 1")
    st = route["status"]
    if st != D.INDEPENDENT:
        return (st, 1 if st == D.CONVERTED else None, "FWO-5 reading at hop 1")
    tt, h = route["token_type"], route["hops_to_monetary"]
    if tt == "NONE":
        return (D.INDEPENDENT, None, "no token gates this route")
    if h == UNMEASURED:
        return (D.UNKNOWN, None, "token %s; hops to monetary UNMEASURED; not read as INDEPENDENT" % tt)
    if h <= hops:
        return (D.CONVERTED, h, "token %s converts to monetary at hop %d, inside the horizon %d" % (tt, h, hops))
    return (D.INDEPENDENT, h, "token %s converts at hop %d, beyond the horizon %d" % (tt, h, hops))


# ------------------------------------------------------------ case handling ---

def routes_of(case):
    for cat in D.CATEGORIES:
        dep = case["dependencies"].get(cat)
        if dep:
            for r in dep["routes"]:
                yield cat, r


def apply_table(res, table, fn, label):
    """Apply a {(category, route): args} table through fn to every route of an FWO-5
    result.  A route the table does not name is REFUSED; so is a table row the case
    does not have."""
    out = {"name": res["name"], "source": res["source"], "dependencies": {}}
    for cat, dep in res["dependencies"].items():
        routes = []
        for r in dep["routes"]:
            key = (cat, r["route"])
            if key not in table:
                raise SplitError("no %s for %s / %r" % (label, cat, r["route"]))
            routes.append(fn(r, *table[key]))
        out["dependencies"][cat] = {"category": cat, "routes": routes, "not_needed": dep["not_needed"]}
    extra = [k for k in table if k[0] not in res["dependencies"]
             or k[1] not in [r["route"] for r in res["dependencies"][k[0]]["routes"]]]
    if extra:
        raise SplitError("%s table names routes the case does not have: %s" % (label, extra))
    return out


def origin_tally(case):
    """Counts per origin over DECIDED rows, the UNDECIDED rows listed apart [CHOICE 4]."""
    t = {CONSTRUCTED: 0, BIOLOGICAL: 0, "undecided": [], "split": {}, "flagged": []}
    for cat, r in routes_of(case):
        if not scorable(r):
            t["undecided"].append((cat, r["route"]))
            continue
        t[r["obligation_origin"]] += 1
        s = split_of(r)
        t["split"][s] = t["split"].get(s, 0) + 1
        if r["reads_requirement_as_claim"]:
            t["flagged"].append((cat, r["route"]))
    t["decided"] = t[CONSTRUCTED] + t[BIOLOGICAL]
    return t


def horizon_rows(case, hops):
    """Dependency categories carrying at least one route INDEPENDENT at this horizon, and
    the per-route readings."""
    rows, cats = [], []
    for cat, r in routes_of(case):
        st, h, note = horizon_status(r, hops)
        rows.append((cat, r["route"], st, h, note))
        if st == D.INDEPENDENT and cat not in cats:
            cats.append(cat)
    return {"hops": hops, "rows": rows, "independent_rows": cats}


# ------------------------------------------------------ the amendment's E-A2 ---

_FWO5_DERIVED = ("status", "settles_in", "obligation_medium", "converted_into")


def unamended_reading(route_):
    """What FWO-5 returns for a route, on the fields it derives itself.  E-A2 asks whether
    this forces a settlement reading on F-A3; the answer is in the record."""
    return dict((k, route_[k]) for k in _FWO5_DERIVED)


def forces_settlement(route_):
    """E-A2's predicate: does FWO-5 assign a settlement medium other than 'none', or a
    CONVERTED status, to the route?"""
    return route_["status"] == D.CONVERTED or route_["obligation_medium"] not in (D.NONE_MEDIUM, "UNKNOWN")


def indistinguishable_under_fwo5(r1, r2):
    """True when two routes agree on every field FWO-5 derives; the label conversion_point
    is excluded because the author writes it."""
    return unamended_reading(r1) == unamended_reading(r2)


# ---------------------------------------------------- section 2 as arithmetic ---

def net_positions(claims):
    """claims[i][j] = what i holds against j.  net[i] = held - owed.  None on an empty or
    non-square matrix.  Registered in tools/known_answer.py."""
    n = len(claims)
    if n == 0 or any(len(row) != n for row in claims):
        return None
    return [sum(claims[i][j] for j in range(n)) - sum(claims[j][i] for j in range(n)) for i in range(n)]


def universal_claim(n, amount=1):
    """Everyone against everyone, equal: the premise P1-P2 as a matrix."""
    return [[0 if i == j else amount for j in range(n)] for i in range(n)]


def both_sides(claims):
    """Parties that hold AND owe on the instrument: P4."""
    n = len(claims)
    return [i for i in range(n)
            if sum(claims[i][j] for j in range(n)) > 0 and sum(claims[j][i] for j in range(n)) > 0]


def placing_parties(claims):
    """Parties with a positive net position: the branch of C2 in which the claim is not
    universal and was placed."""
    net = net_positions(claims)
    return None if net is None else [i for i, v in enumerate(net) if v > 0]


# --------------------------------------------------------------- fixtures ---

def fixture_f_a1():
    src = "CONSTRUCTED: amendment fixture F-A1, a fine; no party, no jurisdiction"
    r = D.route("a fine, paid in dollars", D.DOMINANT, D.DOMINANT, src, conversion_point="settlement")
    return declare(r, CONSTRUCTED, True, False, "a claim a party holds; no physical requirement behind it")


def fixture_f_a2():
    src = "CONSTRUCTED: amendment fixture F-A2, metered water; no utility, no site"
    r = D.route("metered water, billed in dollars", D.DOMINANT, D.DOMINANT, src, conversion_point="input_purchase")
    return declare(r, BIOLOGICAL, False, True, "water is on the amendment's list; the meter is an interposed gate; "
                                              "the bill removes it and discharges no claim the body incurred")


def fixture_f_a3():
    """THE FAIL FIXTURE the amendment designates: a biological requirement, no gate."""
    src = "CONSTRUCTED: amendment fixture F-A3, rainwater on own land, no permit regime; no site"
    r = D.route("rainwater on own land, no permit regime", D.NONE_MEDIUM, D.NONE_MEDIUM, src)
    return declare(r, BIOLOGICAL, False, False, "water is on the amendment's list; nothing is interposed; nothing is owed")


def fixture_f_a4():
    src = "CONSTRUCTED: amendment fixture F-A4, a citation-gated route with unmeasured hops"
    r = D.route("dataset under a citation norm", "citation", "citation", src)
    return token(r, "CITATION", None, UNMEASURED, "CONSTRUCTED: whether citation converts downward is not observed here")


def fail_fixture():
    """Rule 3: three CONSTRUCTED cases on which E-A1 FAILS -- each carries a declared
    BIOLOGICAL edge, so 'at least 2 of 3 with zero BIOLOGICAL' is false.  Labelled
    constructed in every source; nothing about any household."""
    src = "CONSTRUCTED: fail fixture for E-A1; a gated requirement per case; no site"
    out = []
    for i, (name, need) in enumerate((("water", "metered water"), ("food", "purchased food"), ("shelter", "rented room"))):
        res = D.result("z_fail_fixture_%d" % i, [
            D.dependency("material_reagent", [D.route(need, D.DOMINANT, D.DOMINANT, src, conversion_point="input_purchase")]),
            D.dependency("labor", [D.route("own time", D.NONE_MEDIUM, D.NONE_MEDIUM, src)]),
        ], src)
        out.append(apply_table(res, {
            ("material_reagent", need): (BIOLOGICAL, False, True, "CONSTRUCTED: %s is on the list; the price is the gate" % name),
            ("labor", "own time"): (UNDECIDED, None, None, "neither a claim nor on the list [CHOICE 1]"),
        }, declare, "origin declaration"))
    return out


# ------------------------------------------------ the three cases, declared ---
# Every row is this session's reading under [CHOICE 1]; the basis is the argument.
# rule 2 is NOT met.  Keys are (category, route name) exactly as FWO-5 names them.

_ND = "neither a placed claim nor a requirement on the amendment's list [CHOICE 1]"

_A_ORIGIN = {
    ("instrument", "eye and memory"): (UNDECIDED, None, None, _ND),
    ("instrument", "paper notebook, bought"): (CONSTRUCTED, True, False, "a price; the notebook is not a requirement of existing"),
    ("facility_space", "own land, occupancy"): (BIOLOGICAL, False, False,
                                                "shelter is on the list; occupancy interposes nothing on this route; the tax is the other route"),
    ("energy", "daylight"): (UNDECIDED, None, None, _ND + "; light is not warmth"),
    ("transport", "on foot"): (UNDECIDED, None, None, _ND),
    ("labor", "own time, no obligation"): (UNDECIDED, None, None, _ND),
    ("data_access", "own observation"): (UNDECIDED, None, None, _ND),
    ("publication", "notebook, unshared; whether it is ever disseminated is undeclared"): (UNDECIDED, None, None, _ND + "; medium undeclared"),
    ("legal_compliance", "property tax on the land"): (CONSTRUCTED, True, True,
                                                        "a placed claim with a counterparty that can release it, interposed on shelter [CHOICE 2]"),
}

_B_ORIGIN = {
    ("instrument", "purchased on a grant"): (CONSTRUCTED, True, False, "a price against a grant line"),
    ("instrument", "core-facility recharge"): (CONSTRUCTED, True, False, "a recharge rate the facility holds"),
    ("material_reagent", "vendor purchase"): (CONSTRUCTED, True, False, "a price"),
    ("facility_space", "institutional space via indirect costs"): (CONSTRUCTED, True, False,
                                                                     "an indirect-cost rule; laboratory space is not the body's shelter"),
    ("energy", "utility, billed"): (CONSTRUCTED, True, False, "a bill; power to a laboratory is not on the list"),
    ("transport", "shipping"): (CONSTRUCTED, True, False, "a carriage price"),
    ("labor", "salary"): (CONSTRUCTED, True, False, "a claim the worker holds against the institution"),
    ("labor", "stipend"): (CONSTRUCTED, True, False, "as salary"),
    ("data_access", "open dataset; obligation is citation, discharged in citation"): (
        CONSTRUCTED, True, False, "a citation norm with a counterparty who can waive it; discharged in citation"),
    ("data_access", "licensed database"): (CONSTRUCTED, True, False, "a licence fee"),
    ("publication", "article processing charge"): (CONSTRUCTED, True, False, "a charge the venue holds"),
    ("publication", "preprint deposit; no obligation at this hop"): (UNDECIDED, None, None, _ND),
    ("credential_authorization", "degree; tuition"): (CONSTRUCTED, True, False, "tuition, a claim the institution holds"),
    ("legal_compliance", "grant reporting; tax on salary"): (CONSTRUCTED, True, False, "a reporting rule and a tax"),
}

_C_ORIGIN = {
    ("instrument", "own ledger / wallet; holding incurs no obligation at this hop"): (UNDECIDED, None, None, _ND),
    ("material_reagent", "the physical good, priced in dollars"): (
        CONSTRUCTED, True, None, "a price; the case names 'one physical need' without saying which, so whether a gate "
                                 "on a listed requirement is removed is undeclared"),
    ("material_reagent", "a vendor accepting bitcoin; what its obligations settle in is undeclared"): (
        CONSTRUCTED, None, None, "a price is asked; its medium is undeclared in FWO-5, so neither half is declared"),
    ("energy", "network fee, paid in bitcoin to whoever includes the transaction"): (
        CONSTRUCTED, True, False, "a fee, discharged in the medium it is asked in"),
    ("energy", "electricity for a node, billed"): (CONSTRUCTED, True, False, "a bill; a node is not on the list"),
    ("transport", "delivery of the good"): (CONSTRUCTED, True, False, "a carriage price"),
    ("labor", "own time"): (UNDECIDED, None, None, _ND),
    ("data_access", "public chain"): (UNDECIDED, None, None, _ND),
    ("credential_authorization", "identity check at acquisition; what it settles in is undeclared"): (
        CONSTRUCTED, None, False, "a requirement a party placed; its medium is undeclared; no listed requirement behind it"),
    ("legal_compliance", "disposal is a taxable event; gain or loss denominated in dollars"): (
        CONSTRUCTED, True, False, "a tax rule"),
    ("legal_compliance", "penalty for non-reporting, denominated in dollars"): (CONSTRUCTED, True, False, "a penalty rule"),
}

ORIGIN_TABLES = {"a_household_phenology": _A_ORIGIN, "b_open_access_finding": _B_ORIGIN, "c_bitcoin_exit": _C_ORIGIN}

_MON = ("MONETARY", None, 0, "priced and settled in the dominant token")
_NONE = ("NONE", None, None, "no token gates this route at this hop")
_B_TOKEN = {
    ("instrument", "purchased on a grant"): _MON,
    ("instrument", "core-facility recharge"): _MON,
    ("material_reagent", "vendor purchase"): _MON,
    ("facility_space", "institutional space via indirect costs"): _MON,
    ("energy", "utility, billed"): _MON,
    ("transport", "shipping"): _MON,
    ("labor", "salary"): _MON,
    ("labor", "stipend"): _MON,
    ("data_access", "open dataset; obligation is citation, discharged in citation"): (
        "CITATION", "CREDENTIAL", 2,
        "CARRIED: the amendment's own chain, citation -> credential -> funding [CHOICE 5]; a declaration, not an observation"),
    ("data_access", "licensed database"): _MON,
    ("publication", "article processing charge"): _MON,
    ("publication", "preprint deposit; no obligation at this hop"): (
        "NONE", None, None, "no obligation at this hop; citations a deposit may later earn are its return, not its gate [CHOICE 6]"),
    ("credential_authorization", "degree; tuition"): _MON,
    ("legal_compliance", "grant reporting; tax on salary"): _MON,
}


def declared_cases():
    out = []
    for fn in D.DEMO_CASES:
        res = fn()
        out.append(apply_table(res, ORIGIN_TABLES[res["name"]], declare, "origin declaration"))
    return out


def tokened_case_b():
    return apply_table(D.case_b_open_access(), _B_TOKEN, token, "token declaration")


def case_b_alt_reading():
    """[CHOICE 6]'s alternative: the preprint deposit read as CITATION-gated with the same
    hops as the citation route.  Printed as the falsifier for the horizon result; not taken."""
    t = dict(_B_TOKEN)
    t[("publication", "preprint deposit; no obligation at this hop")] = (
        "CITATION", "CREDENTIAL", 2, "ALTERNATIVE READING, not taken: the deposit as a citation-gated route")
    return apply_table(D.case_b_open_access(), t, token, "token declaration")


# ------------------------------------------------------------- expectations ---
# The amendment's section 5, verbatim in intent; commit bacaeab registered it.

def check_expectations(cases, case_b_tok=None):
    rows = []
    zero_bio = sum(1 for c in cases if origin_tally(c)[BIOLOGICAL] == 0)
    con = sum(origin_tally(c)[CONSTRUCTED] for c in cases)
    dec = sum(origin_tally(c)["decided"] for c in cases)
    rows.append(("E-A1 majority CONSTRUCTED over decided rows [CHOICE 4]", dec > 0 and con * 2 > dec))
    rows.append(("E-A1 at least 2 of %d cases carry zero declared BIOLOGICAL edges" % len(cases), zero_bio >= 2))
    f3 = fixture_f_a3()
    rows.append(("E-A2 unamended FWO-5 forces a settlement reading on F-A3", forces_settlement(f3)))
    if case_b_tok is not None:
        h2 = horizon_rows(case_b_tok, 2)
        rows.append(("E-A3 case (b) at two hops returns no INDEPENDENT route", h2["independent_rows"] == []))
        cit = [r for r in h2["rows"] if r[0] == "data_access" and r[2] != D.INDEPENDENT and r[3] == 2]
        rows.append(("E-A3 the citation route itself is not INDEPENDENT at two hops", len(cit) == 1))
    return [(label, "MATCH" if v else "MISMATCH") for label, v in rows]


# ------------------------------------------------------------------- render ---

def render(out=None):
    out = out or sys.stdout
    w = out.write
    w("settlement_split -- AMENDMENT A-1 over FWO-5 / FWO-8; the three cases re-scored under the split\n")
    w("every declaration is this session's reading with its basis in the table; inputs CONSTRUCTED / CARRIED "
      "(key-holder rule 2 NOT met); EXPECTED registered at %s\n\n" % EXPECTED_COMMIT)
    cases = declared_cases()
    for c in cases:
        w("== %s\n" % c["name"])
        w("   %-24s %-46s %-11s %-12s %-6s %-6s %s\n" % ("dependency", "route", "status", "origin", "claim", "gate", "split"))
        for cat, r in routes_of(c):
            w("   %-24s %-46s %-11s %-12s %-6s %-6s %s\n" % (
                cat, r["route"][:46], r["status"], r["obligation_origin"],
                "--" if r["settles_claim"] is None else str(r["settles_claim"]),
                "--" if r["removes_gate"] is None else str(r["removes_gate"]), split_of(r)))
        t = origin_tally(c)
        w("   decided %d: CONSTRUCTED %d, BIOLOGICAL %d; UNDECIDED %d %s\n"
          % (t["decided"], t[CONSTRUCTED], t[BIOLOGICAL], len(t["undecided"]), [r for _, r in t["undecided"]]))
        w("   split over decided rows: %s\n" % t["split"])
        w("   BIOLOGICAL read as a claim (flagged): %s\n\n" % (t["flagged"] or "[]"))
    w("-- E-A2, the unamended FWO-5 reading of the amendment's fixtures\n")
    for f in (fixture_f_a1(), fixture_f_a2(), fixture_f_a3()):
        w("   %-40s %s\n" % (f["route"][:40], unamended_reading(f)))
    w("   F-A3 forced to a settlement reading by FWO-5: %s\n" % forces_settlement(fixture_f_a3()))
    w("   F-A1 (a fine) and F-A2 (metered water) indistinguishable on every field FWO-5 derives: %s\n"
      % indistinguishable_under_fwo5(fixture_f_a1(), fixture_f_a2()))
    w("   under the split: F-A1 %s, F-A2 %s, F-A3 %s\n\n" % (split_of(fixture_f_a1()), split_of(fixture_f_a2()), split_of(fixture_f_a3())))
    w("-- E-A3, case (b) at a horizon of two hops (chain CARRIED from the amendment [CHOICE 5])\n")
    cb = tokened_case_b()
    for hops in (1, 2):
        h = horizon_rows(cb, hops)
        w("   horizon %d: independent rows %s\n" % (hops, h["independent_rows"]))
        for cat, name, st, hop, note in h["rows"]:
            if hop is not None and hop > 1 or st == D.INDEPENDENT:
                w("      %-24s %-46s %-11s hop %-4s %s\n" % (cat, name[:46], st, hop, note))
    alt = horizon_rows(case_b_alt_reading(), 2)
    w("   alternative reading of the deposit [CHOICE 6], NOT taken: independent rows at two hops %s\n" % alt["independent_rows"])
    f4 = fixture_f_a4()
    w("   F-A4 citation route, hops UNMEASURED, horizon 2: %s\n\n" % (horizon_status(f4, 2),))
    w("-- section 2 as arithmetic\n")
    u = universal_claim(4)
    w("   universal claim, 4 parties: net positions %s; parties on both sides %s; placing parties %s\n"
      % (net_positions(u), both_sides(u), placing_parties(u)))
    p = [[0, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    w("   one party against three:    net positions %s; parties on both sides %s; placing parties %s\n\n"
      % (net_positions(p), both_sides(p), placing_parties(p)))
    for label, verdict in check_expectations(cases, cb):
        w("expected %-80s %s\n" % (label, verdict))
    ff = fail_fixture()
    w("\nfail fixture (CONSTRUCTED, three cases): %s\n" % [l + " " + v for l, v in check_expectations(ff)][1])
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_settlement_split.py prints the check count; samples/settlement_split.sample.txt is one "
      "recorded render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_settlement_split.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
