# SPDX-License-Identifier: CC0-1.0
"""AMENDMENT A-5 (2026-09-28): terminus diversity -- are "independent routes" branches of
one chain?

Landed verbatim as AMENDMENT_A5_2026-09-28_terminus-diversity.md and committed ALONE at
EXPECTED_COMMIT_A5 before this module existed (rule 1).  Additive: FWO-5, FWO-8 and
A-1..A-4 are read by import; nothing in them is edited.  The origin section's framing is
provenance only and appears in no field, enum or output string.

  2a  a TOKEN leaf is resolved through FWO-8's converts_to to (kind, final type, hops);
      the hops are kept and the terminus is not the first token seen
  2b  terminus_kinds (unit: kinds), nonmonetary_chains (unit: chains); cycles apart
  2c  an FWO-5 INDEPENDENT route sharing every resolved terminus with another route of
      the same dependency reads BRANCH_OF(route); the FWO-5 row is kept beside it
  2d  every gate carries a layer; COMMUNITY_RULE grades are capped at S

CS-R and CS-A are NOT_EVALUABLE: none of their sources is read (egress refuses the
hosts) and section 6 forbids filling them from CS-G.  Nothing here is a statement about
the law of any jurisdiction or about any community's practice (RIN_076).
"""
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dependency_chain_audit as D   # noqa: E402  FWO-5
import settlement_split as S         # noqa: E402  A-1 / FWO-8 token fields
import chains_a4 as C                # noqa: E402  A-4
import repairs_a31 as R              # noqa: E402  A-3.1

EXPECTED_COMMIT_A5 = "488fe1a"
AMENDMENT_FILE = "AMENDMENT_A5_2026-09-28_terminus-diversity.md"
MONETARY = "MONETARY"
READINGS = ("LITERAL", "PATH_STRICT", "PATH_UPPER", "LAWFUL_STRICT", "LAWFUL_UPPER")
BRANCH = "BRANCH"
NOT_EVALUABLE = "NOT_EVALUABLE"

CHOICES = {
    52: "a resolved terminus is (kind, final token type, hops); BODY, NOT_RECORDED and CYCLE carry type and hops "
        "None; a token node whose converts_to is None ends at its own type",
    53: "an FWO-8 row whose converts_to is not MONETARY but whose hops_to_monetary is an integer resolves to "
        "MONETARY at those hops, the row's own statement that money is reached; UNMEASURED hops stay with the "
        "declared type",
    54: "nonmonetary_chains read three ways: LITERAL (any leaf of the section-3d multiset not (TOKEN, MONETARY)); "
        "PATH_STRICT (some alternative -- one choice at every ANY -- whose leaves are all resolved and none "
        "monetary, NOT_RECORDED or CYCLE); PATH_UPPER (as strict, NOT_RECORDED leaves admitted), the two paths "
        "printing a band; LAWFUL_STRICT / LAWFUL_UPPER (A-4's lawful_reach with every TOKEN leaf FALSE: TRUE, or "
        "TRUE or NOT_RECORDED), since a money-free path the gates prohibit and a money-free route are two things",
    55: "section 2c compares routes of the SAME dependency category; an FWO-5 route with no token fields, or token "
        "NONE, has terminus NOT_RECORDED, and NOT_RECORDED is never shared (unknown is not the same); read with "
        "hops (the terminus as section 2a defines it) and without (kind and type)",
    56: "layers are declared per A-4 gate with a reason; a gate whose issuing layer the enum does not hold (English "
        "common law) or that is not recorded reads NOT_RECORDED",
    57: "CS-G's chains per need are A-4's chains of that need; FUEL, CHARCOAL and SAND chains are inputs, not needs",
    58: "F-B1..F-B4 are CONSTRUCTED and flagged; F-B3 and F-B4 enter a copy of the CS-G world, never CS-G itself",
}


# ---------------------------------------------------------------- 2a ---

def token_nodes():
    """FWO-8 token nodes: type, converts_to (a node id or None), hops for that link."""
    return {"MON": {"token_type": MONETARY, "converts_to": None, "hops": 0},
            "CRED": {"token_type": "CREDENTIAL", "converts_to": "MON", "hops": 2},     # F-B2
            "CIT": {"token_type": "CITATION", "converts_to": "CRED", "hops": 1},
            "CYC_A": {"token_type": "SOCIAL_STANDING", "converts_to": "CYC_B", "hops": 1},
            "CYC_B": {"token_type": "OTHER_NAMED", "converts_to": "CYC_A", "hops": 1}}


def resolve(node, nodes=None):
    """[CHOICE 52]  Follow converts_to until none or a revisit."""
    nodes = token_nodes() if nodes is None else nodes
    seen, hops, cur = [], 0, node
    while True:
        if cur in seen:
            return (C.CYCLE, None, None, tuple(seen + [cur]))
        seen.append(cur)
        n = nodes[cur]
        if n["converts_to"] is None:
            return (C.TOKEN, n["token_type"], hops, tuple(seen))
        hops += n["hops"] if n["hops"] else 1
        cur = n["converts_to"]


def resolved_leaf(leaf, nodes=None):
    kind, ref = leaf
    if kind == C.TOKEN:
        r = resolve(ref, nodes)
        return r[:3]
    return (kind, None, None)


def is_monetary(t):
    return t[0] == C.TOKEN and t[1] == MONETARY


# ---------------------------------------------------------------- paths ---

def alternatives(world, c, nodes=None):
    """Every alternative set of resolved leaves: one choice at every ANY [CHOICE 54]."""
    def ex(e, stack, chain_obj):
        k = e[0]
        if k == "ALL":
            out = [frozenset()]
            for x in e[1]:
                out = [a | b for a in out for b in ex(x, stack, chain_obj)]
            return out
        if k == "ANY":
            out = []
            for x in e[1]:
                out.extend(ex(x, stack, chain_obj))
            return out
        if k == "step":
            node = "step:%s.%s" % (chain_obj["chain_id"], e[1])
            if node in stack:
                return [frozenset([(C.CYCLE, None, None)])]
            return ex(C._step_of(chain_obj, e[1])["requires"], stack + (node,), chain_obj)
        if k == "res":
            node = "res:" + e[1]
            if node in stack:
                return [frozenset([(C.CYCLE, None, None)])]
            return ex(world.resources[e[1]]["requires"], stack + (node,), chain_obj)
        if k == "chain":
            node = "chain:" + e[1]
            if node in stack:
                return [frozenset([(C.CYCLE, None, None)])]
            sub = world.chains[e[1]]
            return ex(("step", sub["steps"][-1]["step_id"]), stack + (node,), sub)
        if k == "leaf":
            return [frozenset([resolved_leaf((e[1], e[2]), nodes)])]
        raise C.ChainError("unknown requirement %r" % (e,))
    return sorted(set(ex(("step", c["steps"][-1]["step_id"]), ("chain:" + c["chain_id"],), c)), key=repr)


def resolved_termini(world, c, nodes=None):
    return [resolved_leaf(l, nodes) for l in C.termini(world, c)["leaves"]]


def chain_reading(world, c, nodes=None):
    rt = resolved_termini(world, c, nodes)
    alts = alternatives(world, c, nodes)
    strict = [a for a in alts if all(t[0] in (C.BODY, C.TOKEN) and not is_monetary(t) for t in a)]
    upper = [a for a in alts if all(t[0] in (C.BODY, C.TOKEN, C.NOT_RECORDED) and not is_monetary(t) for t in a)]
    nm = C.lawful(world, c, money=False)
    return {"termini": rt, "cycle": any(t[0] == C.CYCLE for t in rt), "lawful_no_token": nm,
            "literal": any(not is_monetary(t) and t[0] != C.CYCLE for t in rt),
            "path_strict": bool(strict), "path_upper": bool(upper), "alternatives": len(alts)}


# ---------------------------------------------------------------- 2b ---

def chains_of(world, need):
    return [c for cid, c in sorted(world.chains.items()) if c["need_id"] == need]


def terminus_kinds(world, need, with_hops=True, nodes=None):
    out = set()
    for c in chains_of(world, need):
        for t in resolved_termini(world, c, nodes):
            out.add(t if with_hops else t[:2])
    return {"kinds": sorted(out, key=repr), "count": len(out), "unit": "kinds"}


def nonmonetary_chains(world, need, nodes=None):
    rows = [(c["chain_id"], chain_reading(world, c, nodes)) for c in chains_of(world, need)]
    live = [(cid, r) for cid, r in rows if not r["cycle"]]
    return {"LITERAL": [cid for cid, r in live if r["literal"]],
            "PATH_STRICT": [cid for cid, r in live if r["path_strict"]],
            "PATH_UPPER": [cid for cid, r in live if r["path_upper"]],
            "LAWFUL_STRICT": [cid for cid, r in live if r["lawful_no_token"] == C.TRUE],
            "LAWFUL_UPPER": [cid for cid, r in live if r["lawful_no_token"] in (C.TRUE, C.NOT_RECORDED)],
            "cycles_apart": [cid for cid, r in rows if r["cycle"]], "chains": len(rows), "unit": "chains"}


# ---------------------------------------------------------------- 2d ---

LAYER_OF = {   # [CHOICE 56]
    "G-C1": ("STATE", "a state statute (C-1)"),
    "G-LAND": (C.NOT_RECORDED, "tenure by purchase, rent and property tax; the issuing layer is not recorded"),
    "G-T2": ("FEDERAL", "a national forest permit"),
    "G-T4": ("COUNTY", "a county burn ban"),
    "G-T12": (C.NOT_RECORDED, "the public-land rule is not named (T-12)"),
    "G-T11": ("MUNICIPAL", "a park ordinance"),
    "G-T5": ("FEDERAL", "a national emission standard"),
    "G-T4X": ("COUNTY", "a county burn ban"),
    "G-T3": ("STATE", "a statute or commission rule (T-3)"),
    "G-T1": ("MUNICIPAL", "a city camping ordinance"),
    "G-G2": (C.NOT_RECORDED, "English common law; the enum has no such layer"),
}


def layered_world():
    w = C.World()
    for gid, g in w.gates.items():
        g["layer"], g["layer_basis"] = LAYER_OF[gid]
    return w


def cap_grade(layer, grade):
    """COMMUNITY_RULE sources are capped at S."""
    if layer == "COMMUNITY_RULE" and grade == "P":
        return "S"
    return grade


def layer_mix(world, need):
    mix = {}
    for c in chains_of(world, need):
        for gid in sorted(C.reachable_parts(world, c)["gates"]):
            lay = world.gates[gid]["layer"]
            mix[lay] = mix.get(lay, 0) + 1
    return dict(sorted(mix.items()))


# --------------------------------------------------------------- 3 case sets ---

CASE_SETS = {
    "CS-G": {"status": "BUILT", "sources": "the rows of A-2..A-4, lifted into A-4 chains [CHOICE 57]"},
    "CS-R": {"status": NOT_EVALUABLE, "sources": {
        "R-1": "tribal code sections on water, fuel/wood, housing or land assignment (one named nation)",
        "R-2": "federal trust-land rule on land use and leasing (the BIA layer)",
        "R-3": "state/county rules reaching trust land, if any; reach recorded, never assumed"}},
    "CS-A": {"status": NOT_EVALUABLE, "sources": {
        "A-1s": "Wisconsin v. Yoder (1972) [K]", "A-2s": "IRC 1402(g) self-employment tax exemption [K]",
        "A-3s": "published ethnography of district rules (COMMUNITY_RULE, grade <= S)",
        "A-4s": "county property-tax obligation on Amish-held land, one named county"}},
}
NOT_READ = "no source read; CONNECT refused at 2026-09-28T13:14:37Z (ecfr.gov, leg.colorado.gov, law.cornell.edu)"


def compare_sets(world, other, need):
    """E-A5-2 / E-A5-3: NOT_EVALUABLE until the other set is sourced; never filled from CS-G."""
    if CASE_SETS[other]["status"] != "BUILT":
        return {"status": NOT_EVALUABLE, "reason": "%s: %d sources named, none read (%s)"
                                                    % (other, len(CASE_SETS[other]["sources"]), NOT_READ)}
    raise NotImplementedError


# --------------------------------------------------------------- 2c re-read ---

def fwo5_terminus(route):
    """[CHOICE 53] [CHOICE 55]"""
    if "token_type" not in route or route["token_type"] == "NONE":
        return (C.NOT_RECORDED, None, None)
    tt, ct, h = route["token_type"], route["converts_to"], route["hops_to_monetary"]
    if tt == MONETARY:
        return (C.TOKEN, MONETARY, 0)
    if isinstance(h, int):
        return (C.TOKEN, MONETARY, h)
    return (C.TOKEN, ct or tt, h)


def fwo5_cases():
    """FWO-5's three demo cases; case (b) carries FWO-8's token fields, (a) and (c) carry none."""
    return [D.case_a_household(), S.tokened_case_b(), D.case_c_bitcoin_exit()]


def reread(cases=None, with_hops=True):
    out = []
    for case in (fwo5_cases() if cases is None else cases):
        for cat, dep in case["dependencies"].items():
            routes = dep["routes"]
            for r in routes:
                if r["status"] != D.INDEPENDENT:
                    continue
                t = fwo5_terminus(r)
                key = t if with_hops else t[:2]
                others = [o["route"] for o in routes if o is not r and t[0] != C.NOT_RECORDED
                          and (fwo5_terminus(o) if with_hops else fwo5_terminus(o)[:2]) == key]
                out.append({"case": case["name"], "category": cat, "route": r["route"], "fwo5": D.INDEPENDENT,
                            "terminus": t, "a5": ("%s_OF(%s)" % (BRANCH, others[0])) if others else D.INDEPENDENT})
    return out


# ---------------------------------------------------------------- fixtures ---

def fixture_f_b1():
    """Two routes, different step lists, one resolved terminus.  FWO-5 reads both
    INDEPENDENT; the fail fixture."""
    src = "CONSTRUCTED: A-5 F-B1; no instance was read"
    a = D.route("route one: deposit, then cite", "citation", "citation", src, note="steps: deposit, cite")
    b = D.route("route two: certify, then practise", "credential", "credential", src, note="steps: certify, practise")
    a = S.token(a, "CITATION", "CREDENTIAL", 2, "CONSTRUCTED: F-B1")
    b = S.token(b, "CREDENTIAL", MONETARY, 2, "CONSTRUCTED: F-B1")
    return D.result("f_b1", [D.dependency("data_access", [a, b])], src)


def fixture_f_b3_b4():
    """A copy of the CS-G world with F-B3 (BODY only) and F-B4 (a CYCLE) added [CHOICE 58]."""
    w = layered_world()
    w.chains["F-B3"] = C.chain("F-B3", "FOOD", "constructed", [
        C.step("forage", "forage by hand", "FOOD", C.ALL(C.leaf_body()))], (),
        lifted_from="CONSTRUCTED A-5 F-B3; hold-ineligible")
    w.chains["F-B4"] = C.chain("F-B4", "FOOD", "constructed", [
        C.step("trade", "trade labour for food", "FOOD", C.ALL(C.chain_ref("F-B4-LABOR")))], (),
        lifted_from="CONSTRUCTED A-5 F-B4; hold-ineligible")
    w.chains["F-B4-LABOR"] = C.chain("F-B4-LABOR", "FUEL", "constructed", [
        C.step("work", "labour, fed by food", "FUEL", C.ALL(C.chain_ref("F-B4")))], (),
        lifted_from="CONSTRUCTED A-5 F-B4; hold-ineligible")
    return w


# ----------------------------------------------------------- registry, lint ---

def registry():
    E = []

    def e(eid, pq, fq, space, p, f, mn=1, mx=1):
        E.append({"id": eid, "variant": "", "amendment": "A-5", "p_quote": pq, "f_quote": fq, "f_form": R.STATED,
                  "f_requires": R.CODE_BEHAVIOUR, "requires_reason": "a count on the case sets", "space": tuple(space),
                  "min_cells": mn, "max_cells": mx, "p": p, "f": f})
    three = itertools.product(("EQUAL", "DIFFER", NOT_EVALUABLE), (True, False))
    e("E-A5-1", "nonmonetary_chains = 0 (unit: chains).", "nonmonetary_chains >= 1 for any need.", range(3),
      lambda w: w[0] == 0, lambda w: w[0] >= 1)
    e("E-A5-2", "with (TOKEN, MONETARY) present in both.", "the two sets differ for any need.", three,
      lambda w: w[0][0] == "EQUAL" and w[0][1], lambda w: w[0][0] == "DIFFER")
    e("E-A5-3", "CS-A: the same comparison against CS-G.", "the sets differ for any need.",
      itertools.product(("EQUAL", "DIFFER", NOT_EVALUABLE), (True, False)),
      lambda w: w[0][0] == "EQUAL" and w[0][1], lambda w: w[0][0] == "DIFFER")
    e("E-A5-4", "reclassifies >= 1 route as BRANCH (unit: routes).", "0 routes reclassified.", range(3),
      lambda w: w[0] >= 1, lambda w: w[0] == 0)
    return E


# ------------------------------------------------------------ expectations ---

def check_expectations():
    w = layered_world()
    rows = []
    for reading in READINGS:
        per = dict((n, nonmonetary_chains(w, n)[reading]) for n in C.ROUTE_NEEDS)
        fired = sorted(n for n, v in per.items() if v)
        rows.append({"id": "E-A5-1 (%s)" % reading, "status": "MISMATCH" if fired else "MATCH",
                     "hold": "K rows, hold-ineligible; coverage 0/%d chains sourced" % len(w.chains),
                     "detail": "falsifier %s; per need %s" % (("fires on %s" % fired) if fired else "silent",
                                                             dict((n, len(v)) for n, v in per.items()))})
    for eid, other in (("E-A5-2", "CS-R"), ("E-A5-3", "CS-A")):
        cmpr = compare_sets(w, other, "WATER")
        rows.append({"id": eid, "status": NOT_EVALUABLE, "hold": "coverage 0/%d %s sources read"
                     % (len(CASE_SETS[other]["sources"]), other),
                     "detail": "%s; beside it, uninterpreted, CS-G steps per chain %s and layer mix %s"
                               % (cmpr["reason"],
                                  dict((n, [C.steps_per_chain(w, c)["transitive"] for c in chains_of(w, n)])
                                       for n in C.ROUTE_NEEDS),
                                  dict((n, layer_mix(w, n)) for n in C.ROUTE_NEEDS))})
    for hops in (True, False):
        rr = reread(with_hops=hops)
        br = [r for r in rr if r["a5"].startswith(BRANCH)]
        rows.append({"id": "E-A5-4 (%s)" % ("with hops" if hops else "without hops"),
                     "status": "MATCH" if br else "MISMATCH",
                     "hold": "INSTRUMENT; coverage %d/%d INDEPENDENT routes carry a declared token"
                             % (len([r for r in rr if r["terminus"][0] != C.NOT_RECORDED]), len(rr)),
                     "detail": "%d of %d FWO-5 INDEPENDENT routes reclassified: %s"
                               % (len(br), len(rr), [(r["route"][:24], r["a5"][:40]) for r in br])})
    rank = {"MISMATCH": 0, NOT_EVALUABLE: 1, "MATCH": 2}
    return sorted(rows, key=lambda r: rank[r["status"]])


def fail_fixture():
    res = fixture_f_b1()
    before = [r["status"] for r in res["dependencies"]["data_access"]["routes"]]
    after = [r["a5"] for r in reread([res])]
    return {"fwo5": before, "a5": after}


# ------------------------------------------------------------------ render ---

def render(out=None):
    wr = (out or sys.stdout).write
    w = layered_world()
    wr("termini_a5 -- AMENDMENT A-5 over FWO-5 / FWO-8 / A-4: resolved termini, branch re-read, layers\n")
    wr("EXPECTED registered at %s; CS-R and CS-A NOT_EVALUABLE (no source read); CS-G is K throughout\n\n"
       % EXPECTED_COMMIT_A5)
    wr("-- expected (section 5), MISMATCH rows first, then NOT_EVALUABLE\n")
    for r in check_expectations():
        wr("expected %-13s %-28s %s\n" % (r["status"], r["id"], r["detail"]))
        wr("         hold: %s\n" % r["hold"])
    wr("\n-- CS-G terminus kinds per need (unit: kinds) [CHOICE 52]\n")
    for n in C.ROUTE_NEEDS:
        tk, tk2 = terminus_kinds(w, n), terminus_kinds(w, n, with_hops=False)
        wr("   %-8s %d with hops %s; %d without\n" % (n, tk["count"], tk["kinds"], tk2["count"]))
    wr("\n-- nonmonetary_chains per need, five readings [CHOICE 54]\n")
    for n in C.ROUTE_NEEDS:
        nm = nonmonetary_chains(w, n)
        wr("   %-8s of %d chains: LITERAL %s; PATH_STRICT %s; PATH_UPPER %s; LAWFUL_STRICT %s; LAWFUL_UPPER %s; "
           "cycles apart %s\n" % (n, nm["chains"], nm["LITERAL"], nm["PATH_STRICT"], nm["PATH_UPPER"],
                                  nm["LAWFUL_STRICT"], nm["LAWFUL_UPPER"], nm["cycles_apart"]))
    wb = fixture_f_b3_b4()
    nm = nonmonetary_chains(wb, "FOOD")
    wr("   with F-B3 and F-B4 (constructed): FOOD LITERAL %s; PATH_STRICT %s; cycles apart %s\n"
       % (nm["LITERAL"], nm["PATH_STRICT"], nm["cycles_apart"]))
    wr("\n-- 2a resolution: F-B2 CRED -> %s; the cycle pair -> %s\n" % (resolve("CRED")[:3], resolve("CYC_A")[:1]
                                                                         + resolve("CYC_A")[3:]))
    wr("\n-- 2c re-read of FWO-5 INDEPENDENT routes [CHOICE 55]\n")
    for hops in (True, False):
        for r in reread(with_hops=hops):
            wr("   %-13s %-22s %-18s %-44s %s\n" % ("with hops" if hops else "without hops", r["case"][:22],
                                                   r["category"], r["route"][:44], r["a5"][:48]))
    wr("\n-- 2d layer mix per need [CHOICE 56]; COMMUNITY_RULE P reads %s\n" % cap_grade("COMMUNITY_RULE", "P"))
    for n in C.ROUTE_NEEDS:
        wr("   %-8s %s\n" % (n, layer_mix(w, n)))
    wr("\n-- A-3.1 on section 5\n")
    for x in registry():
        cc = R.complement(x)
        wr("   %-8s %-12s %s\n" % (x["id"], cc["status"], ", ".join(cc["gap_cells"][:4])))
    q = C.quotes_present(registry(), AMENDMENT_FILE)
    wr("   quotes found in the amendment: %d/%d\n" % (len([1 for x in q if x[2]]), len(q)))
    lt = C.lint_two_ways(AMENDMENT_FILE)
    wr("   unit lint: %d of %d count tokens outside the A-3.1 list; %d with '(unit: X)' read; units declared %s\n"
       % (lt["fail_a31_list"], len(lt["tokens"]), lt["fail_with_annotation"], lt["declared_units"]))
    ff = fail_fixture()
    wr("\nfail fixture: F-B1 reads %s under FWO-5 and %s under section 2c\n" % (ff["fwo5"], ff["a5"]))
    wr("holds: rule 1 met (%s); rule 3 met; rule 2 unmet (CS-G K, CS-R and CS-A unread)\n" % EXPECTED_COMMIT_A5)
    wr("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    wr("execution note: test_chains_a456.py prints the check count; samples/termini_a5.sample.txt is one recorded "
       "render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_chains_a456.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
