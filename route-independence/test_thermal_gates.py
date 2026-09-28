# SPDX-License-Identifier: CC0-1.0
"""Checks for AMENDMENT A-3 (thermal_gates.py).

Run:  python3 route-independence/test_thermal_gates.py
Prints the check count and whether a fixture built to FAIL exists (key-holder
rule 3); NO_FAIL_FIXTURE in the summary line otherwise.
"""
import ast
import importlib.util
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import gate_state as G          # noqa: E402
import gate_state_a21 as A21    # noqa: E402
import thermal_gates as T       # noqa: E402

_checks = 0
_failed = 0
FAIL_FIXTURES = 0


def check(cond, msg):
    global _checks, _failed
    _checks += 1
    if not cond:
        _failed += 1
        sys.stderr.write("FAIL: %s\n" % msg)


def refuses(fn, exc, needle, msg):
    try:
        fn()
    except exc as e:
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


def render():
    buf = io.StringIO()
    T.render(buf)
    return buf.getvalue()


def defined_names(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    return set(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))) | \
        set(t.id for n in tree.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name))


SRC = os.path.join(HERE, "thermal_gates.py")
CONV = {"HERE", "CHOICES", "render", "main", "check_expectations", "fail_fixture", "_fmt", "_row", "_index",
        "_name", "_order"}
SRC_TEXT = open(SRC, encoding="utf-8").read()
TREE = ast.parse(SRC_TEXT)

HEAT_IN_TOKENS = {"WARM", "RETAIN"}
HEAT_OUT_TOKENS = {"COOL", "SHED"}


def pooled_expressions(tree):
    """Section 2e: every BoolOp / Compare / BinOp / IfExp naming a heat-in and a heat-out
    direction together, by constant or by name."""
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.BoolOp, ast.Compare, ast.BinOp, ast.IfExp)):
            continue
        toks = set()
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name):
                toks.add(sub.id)
            elif isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                toks.add(sub.value)
        if toks & HEAT_IN_TOKENS and toks & HEAT_OUT_TOKENS:
            out.append(getattr(node, "lineno", None))
    return out


# ---------------------------------------------------------------- structure ---

def t_structure():
    for other in ("dependency_chain_audit.py", "edge_taxonomy.py", "settlement_split.py", "gate_state.py",
                  "gate_state_a21.py"):
        clash = (defined_names(os.path.join(HERE, other)) & defined_names(SRC)) - CONV
        check(not clash, "thermal_gates redefines no name of %s (clash %s)" % (other, sorted(clash)))
    check(T.EXPECTED_COMMIT_A3 not in (G.EXPECTED_COMMIT_A2, A21.EXPECTED_COMMIT_A21),
          "A-3 registers its own EXPECTED commit")
    check(T.STOCKS == ("THERMAL", "WATER", "FOOD", "AIR", "SLEEP"), "stock enum as delivered (2a)")
    check(T.HEAT_DIRECTIONS == ("WARM", "COOL", "RETAIN", "SHED"), "direction enum as delivered (2a)")
    check("BOTH" not in T.HEAT_DIRECTIONS, "BOTH is not a direction [CHOICE 15]")
    check(len(T.LOCI) == 5 and T.BODY == "BODY", "locus enum as delivered (2a)")
    check(len(T.GATE_KINDS) == 7 and T.PRIVATE_RULE in T.GATE_KINDS, "gate_kind enum as delivered (2b)")
    check(T.MARKET_2D == ("TOKEN_PURCHASE",), "2d excludes TOKEN_PURCHASE only")
    check(set(T.MARKET_E32A) == {"TOKEN_PURCHASE", "METERED_TOKEN"}, "E-A3-2a's list leaves METERED_TOKEN market-side")
    check(T.ACCESS == ("TRUE", "FALSE", "UNKNOWN"), "access_is_right enum as delivered (2b)")
    check(set(T.A21_FIELDS_BUILT) == {"access_is_right", "revocable_by"}, "the two fields A-2.1 proposed are the two built")
    g = T.fixture_f_t1()[0]
    check(all(f in g for f in T.A21_FIELDS_BUILT), "every gate row carries A-2.1's proposed fields")
    check(set(T.SIDE) == set(T.HEAT_DIRECTIONS) and set(T.SIDE.values()) == {T.HEAT_IN, T.HEAT_OUT},
          "every direction has one side [CHOICE 14]")


# ------------------------------------------------------------------ sources ---

def t_sources():
    check(sorted(T.SOURCES_A3) == ["T-%d" % i for i in range(1, 10)], "T-1..T-9 named (section 3)")
    check(all(s["grade"] == "K" and s["status"] == "NOT_LANDED" for s in T.SOURCES_A3.values()),
          "every section-3 source is grade K, not landed")
    check(all(G.hold_grade(sid, T.SOURCES_A3) is None for sid in T.SOURCES_A3), "no K source is a hold grade (R2)")
    gates = T.fixture_gates()
    check(not any(g["hold_eligible"] for g in gates), "no fixture gate row is hold-eligible")
    check(not any(z["hold_eligible"] for z in T.fixture_f_t6()), "F-T6 is not hold-eligible")
    check(not any(c["hold_eligible"] for c in T.seed_couplings()), "the coupling row is not hold-eligible (T-8 K)")
    check(T.sourced(gates) == [], "the sourced set is empty")


# ---------------------------------------------------------------- actuators ---

def t_actuators():
    acts = T.seed_actuators()
    ids = [a["actuator_id"] for a in acts]
    check(len(ids) == len(set(ids)) == 18, "18 actuator rows: 10 external, 8 body halves")
    check(len([a for a in acts if a["locus"] == T.BODY]) == 8, "four body-only actuators split in two [CHOICE 15]")
    check(all(a["provenance"] == T.PROVENANCE["C"] for a in acts if a["locus"] == T.BODY), "body rows are marked C")
    kav = sorted(a["actuator_id"] for a in acts if a["provenance"] == T.PROVENANCE["K"])
    check(kav == sorted(["clothing.retain", "clothing.shed", "fans", "ventilation", "heating.utility", "open_fire"]),
          "the six rows the order attributes to Kavik")
    for name in T._BODY_ONLY:
        dirs = sorted(a["direction"] for a in acts if a["actuator_id"].startswith(name + "."))
        check(dirs == ["COOL", "WARM"], "%s enters once per side" % name)
    refuses(lambda: T.actuator("x", "THERMAL", "BOTH", "BODY", "C"), T.ThermalError, "BOTH", "BOTH is refused")
    refuses(lambda: T.actuator("x", "HEAT", "WARM", "BODY", "C"), T.ThermalError, "stock", "a stock off the enum")
    refuses(lambda: T.actuator("x", "THERMAL", "WARM", "SKY", "C"), T.ThermalError, "locus", "a locus off the enum")
    refuses(lambda: T.actuator("x", "THERMAL", "WARM", "BODY", "Z"), T.ThermalError, "provenance", "provenance")
    refuses(lambda: T._index(acts + [acts[0]]), T.ThermalError, "twice", "a duplicate actuator id")


# -------------------------------------------------------------------- gates ---

def t_gates():
    ok = dict(gate_state=G.PROHIBITED, source="T-6")
    refuses(lambda: T.tgate("g", "nope", 1, T.PROHIBITION, "J", "2024", **ok), T.ThermalError, "actuator_id",
            "an undeclared actuator")
    refuses(lambda: T.tgate("g", "fans", 0, T.PROHIBITION, "J", "2024", **ok), T.ThermalError, "order", "order 0")
    refuses(lambda: T.tgate("g", "fans", True, T.PROHIBITION, "J", "2024", **ok), T.ThermalError, "order",
            "a boolean order")
    refuses(lambda: T.tgate("g", "fans", 1, "TAX", "J", "2024", **ok), T.ThermalError, "gate_kind", "a kind off the enum")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, " ", "2024", **ok), T.ThermalError, "jurisdiction",
            "a blank jurisdiction")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", gate_state="CLOSED", source="T-6"),
            T.ThermalError, "gate_state", "a state off A-2's enum")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", "2020", **ok), T.ThermalError, "t_from",
            "t_from after t_to")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "20-24", **ok), G.GateError, "ISO", "A-2's date grammar")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", condition="c", **ok), T.ThermalError,
            "trigger_condition", "a condition without a named trigger")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", access_is_right="YES", **ok), T.ThermalError,
            "access_is_right", "access off the enum")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", revocable_by=" ", **ok), T.ThermalError,
            "revocable_by", "a blank office")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", gate_state=G.PROHIBITED), T.ThermalError,
            "R2", "an unsourced untagged gate")
    refuses(lambda: T.tgate("g", "fans", 1, T.TOKEN_PURCHASE, "J", "2024", tag=G.CONSTRUCTED_UNSOURCED),
            T.ThermalError, "instrument", "an unsourced gate names its instrument [CHOICE 23]")
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", gate_state=G.PROHIBITED, source="W-1"),
            T.ThermalError, "section-3", "an A-2 source id on an A-3 gate")
    table = dict(T.SOURCES_A3)
    table["T-X"] = {"grade": "S", "input": False}
    refuses(lambda: T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", gate_state=G.PROHIBITED, source="T-X",
                            sources=table), T.ThermalError, "NOT adopted", "an input:False source")
    table["T-Y"] = {"grade": "S", "input": True}
    s_row = T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", gate_state=G.PROHIBITED, source="T-Y", sources=table)
    check(s_row["hold_eligible"], "a grade-S sourced row would be hold-eligible (the gate is reachable)")
    g = T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", **ok)
    check(g["gate_state"] == G.PROHIBITED and g["direction"] == "COOL" and g["fault_class"] == T.FAULT_ACTUATOR,
          "direction copied from the actuator; a gate is an ACTUATOR fault")
    d = T.tgate("g", "fans", 1, T.PROHIBITION, "J", "2024", source="T-6")
    check(d["gate_state"] == G.UNKNOWN_STATE, "gate_state defaults to UNKNOWN (2b)")
    check(d["access_is_right"] == "UNKNOWN" and d["revocable_by"] is None, "access UNKNOWN, revocable_by None by default")


# ------------------------------------------------------------------- series ---

def t_series():
    gates = T.fixture_gates()
    s = T.series(gates, "wood_stove", "county X", "2026")
    check(len(s) == 4, "F-T4 reads four positions")
    check([p["order"] for p in s] == [1, 2, 3, 4], "positions in order")
    check(len(s[2]["alternatives"]) == 2, "position 3 carries two alternatives [CHOICE 17]")
    check(sorted(x["gate_kind"] for x in s[2]["alternatives"]) == ["PERMIT", "TOKEN_PURCHASE"],
          "the fuel disjunction: purchase OR permit")
    r4 = s[3]["alternatives"][0]["reading"]
    check(isinstance(r4, tuple) and r4[0] == "BY_CONDITION", "the burn ban reads BY_CONDITION with no condition given")
    on = T.series(gates, "wood_stove", "county X", "2026", "drought declaration in force")
    off = T.series(gates, "wood_stove", "county X", "2026", "no drought declaration")
    check(on[3]["alternatives"][0]["reading"] == G.PROHIBITED and off[3]["alternatives"][0]["reading"] == G.OPEN,
          "the condition index moves position 4 and no other")
    check([p["alternatives"] for p in on][:3] == [p["alternatives"] for p in off][:3], "positions 1-3 condition-free")
    check(not any(isinstance(s, str) for s in (s, on, off)), "a series is never one state")
    check(T.series(gates, "wood_stove", "county X", "2023") == (), "before 2024 no position is in force")
    check(T.series(gates, "wood_stove", "state X", "2026") == (), "another jurisdiction reads no position")
    a = T.series(gates, "heating.utility", "state A", T.T_WINTER, "nonpayment, winter")
    b = T.series(gates, "heating.utility", "state B", T.T_WINTER, "nonpayment, winter")
    check(a[0]["alternatives"][0]["reading"] == G.METERED_PERMISSION and b[0]["alternatives"][0]["reading"] == G.PROHIBITED,
          "F-T3: same winter date, A with moratorium, B without")
    dup = T.fixture_f_t1() + [T.tgate("F-T1.ban", "shelter.selfbuilt", 1, T.PROHIBITION, "US city X (public land)",
                                      "2024", gate_state=G.OPEN, source="T-1")]
    c = T.series(dup, "shelter.selfbuilt", "US city X (public land)", "2026")
    check(c[0]["alternatives"][0]["reading"][0] == "CONFLICT", "two unconditioned rows of one gate read CONFLICT")


# ------------------------------------------------------------ pooling (2e) ---

def t_pooling():
    refuses(lambda: T.series_of(T.pooled_input(), "state X", "2026"), T.DirectionPooled, "2e",
            "SHED pooled with RETAIN is refused")
    refuses(lambda: T.refuse_pooled(T.fixture_f_t2() + T.fixture_f_t4()), T.ThermalError, "one actuator",
            "two actuators of one direction are refused as one series")
    check(issubclass(T.DirectionPooled, G.GateError), "the refusal is an A-2 GateError subclass")
    lines = pooled_expressions(TREE)
    check(lines == [], "no expression names a heat-in and a heat-out direction together (lines %s)" % lines)
    planted = ast.parse("x = (d == WARM) or (d == COOL)\ny = 'RETAIN' if a else 'SHED'\n")
    check(len(pooled_expressions(planted)) >= 2, "the 2e scan fires on a planted pooling expression")
    fns = [n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef)]
    reducers = [f.name for f in fns if any(isinstance(n, ast.Return) and isinstance(n.value, ast.Attribute)
                                           and n.value.attr in ("OPEN", "PROHIBITED") for n in ast.walk(f))]
    check(reducers == [], "no function returns a bare gate state from a series (%s)" % reducers)


# ----------------------------------------------------------------- derived ---

def t_derived():
    gates = T.fixture_gates()
    per = T.gates_per_actuator(gates, "county X", "2026")
    check(per["wood_stove"]["count"] == 5, "wood stove: five distinct gates in force")
    check(per["open_fire"]["count"] == 1, "the two F-T2 rows are one gate")
    check(per["wood_stove"]["by_kind"]["TOKEN_PURCHASE"] == 2, "split by kind")
    check(T.nonmarket_gates(gates, "county X", "2026")["wood_stove"] == 3, "non-market under 2d: 3")
    n2 = T.nonmarket_gates(gates, "state A", "2026")["heating.utility"]
    ne = T.nonmarket_gates(gates, "state A", "2026", market=T.MARKET_E32A)["heating.utility"]
    check((n2, ne) == (1, 0), "METERED_TOKEN: non-market under 2d, market under E-A3-2a's list [CHOICE 22]")
    per_on = T.gates_per_actuator(gates, "county X", "2026", "drought declaration in force")
    check(per_on == per, "a condition selects rows, not gates: the count is unchanged")
    acts = T.seed_actuators()
    res = T.ungated_residue(gates, T.fixture_f_t6(), acts, "state X", "2026")
    check(res["residue"] == ["huddling.warm", "huddling.cool"], "F-T6 is the residue")
    check("fans" in res["unsearched"] and "clothing.retain" in res["unsearched"],
          "an actuator with no row and no declaration is UNSEARCHED, not residue [CHOICE 20]")
    check(len(res["residue"]) + len(res["unsearched"]) + len(T.gates_per_actuator(gates, "state X", "2026")) == 18,
          "every actuator lands in exactly one of gated / residue / unsearched")
    bad = T.declare_zero("clothing.shed", "state X", "2024", tag=G.CONSTRUCTED_UNSOURCED)
    r2 = T.ungated_residue(gates, [bad], acts, "state X", "2026")
    check(r2["contradicted"] == ["clothing.shed"], "a zero beside an in-force gate is CONTRADICTED")
    refuses(lambda: T.declare_zero("fans", "J", "2024"), T.ThermalError, "source", "an unsourced untagged zero")
    refuses(lambda: T.declare_zero("fans", T.ANY_JURISDICTION, "2024", source="T-9"), T.ThermalError, "ANY",
            "jurisdiction ANY on a sourced declaration")
    rc = T.residue_capacity()
    check(rc["value"] is None and rc["status"] == T.NOT_EVALUABLE, "residue_capacity is NOT_EVALUABLE, value None")
    check(T.coincidence(gates)["status"] == T.NOT_EVALUABLE, "E-A3-6 coincidence is NOT_EVALUABLE")
    rv = T.revocation_record(gates)
    check(rv["revocable_by_named"] == 0 and rv["access_known"] == 0, "no fixture names an office or a right [CHOICE 21]")


# --------------------------------------------------------------- couplings ---

def t_couplings():
    live = [g for g in T.fixture_f_t1() if T._applies(g, g["jurisdiction"], "2026", None)]
    e = T.propagate(live, T.seed_couplings())
    check(len(e) == 1 and e[0]["to_stock"] == "WATER" and e[0]["fault_class"] == T.FAULT_SENSOR,
          "F-T1 reaches WATER as a SENSOR effect via C-1")
    check(T.propagate(live, []) == [], "removing the coupling row removes the propagation (E-A3-5)")
    other = T.coupling("C-X", "THERMAL", "SLEEP", "m", "+", "NONE", tag=G.CONSTRUCTED_UNSOURCED)
    e2 = T.propagate(live, [other])
    check(e2[0]["fault_class"] == T.FAULT_COUPLED, "sensor_effect NONE is a coupled effect, not a sensor fault")
    wat = T.coupling("C-W", "WATER", "THERMAL", "m", "+", "NONE", tag=G.CONSTRUCTED_UNSOURCED)
    check(T.propagate(live, [wat]) == [], "a coupling from another stock does not fire on a THERMAL gate")
    refuses(lambda: T.coupling("C", "THERMAL", "THERMAL", "m", "+", "NONE", tag=G.CONSTRUCTED_UNSOURCED),
            T.ThermalError, "distinct", "a coupling of one stock to itself")
    refuses(lambda: T.coupling("C", "THERMAL", "WATER", "m", "+", "NONE"), T.ThermalError, "R2", "an unsourced coupling")
    refuses(lambda: T.coupling("C", "THERMAL", "WATER", "m", "+", "BROKEN", source="T-8"), T.ThermalError,
            "sensor_effect", "a sensor_effect off the enum")
    readers = sorted(set(f.name for f in ast.walk(TREE) if isinstance(f, ast.FunctionDef)
                         for n in ast.walk(f) if isinstance(n, ast.Subscript)
                         and isinstance(n.slice, (ast.Constant, getattr(ast, "Index", ast.Constant)))
                         and "to_stock" in ast.dump(n.slice)))
    check(readers == ["check_expectations", "propagate", "render"],
          "to_stock is read only by propagate and its reporters (%s)" % readers)
    per_before = T.gates_per_actuator(T.fixture_gates(), "US city X (public land)", "2026")
    check(per_before == {"shelter.selfbuilt": {"count": 1, "by_kind": {"PROHIBITION": 1}}},
          "a propagated effect enters no gate count (two fault classes)")


# ------------------------------------------------------------- expectations ---

def t_expectations():
    rows = T.check_expectations()
    ids = [r["id"] for r in rows]
    check(ids[0] == "E-A3-1 (literal)" and rows[0]["status"] == "MISMATCH",
          "the literal E-A3-1 row fails and is printed first (R4)")
    st = [r["status"] for r in rows]
    check(st == sorted(st, key=lambda s: {"MISMATCH": 0, "NOT_EVALUABLE": 1, "MATCH": 2}[s]),
          "MISMATCH, then NOT_EVALUABLE, then MATCH")
    by = dict((r["id"], r) for r in rows)
    check(by["E-A3-1 (reading)"]["status"] == "MATCH", "E-A3-1 reading holds on the instrument")
    for k in ("E-A3-2a", "E-A3-3", "E-A3-4", "E-A3-6"):
        check(by[k]["status"] == T.NOT_EVALUABLE, "%s is NOT_EVALUABLE on the empty sourced set" % k)
    check(by["E-A3-5"]["status"] == "MATCH", "E-A3-5 holds on the instrument")
    check(by["E-A3-2a"]["claim"].startswith("WEAKNESS FIRST"), "E-A3-2's weakness is stated first")
    acts, gates, zeros = T.seed_actuators(), T.fixture_gates(), T.fixture_f_t6()
    k = T.e32a_reading(gates, zeros, acts)
    check((k["n_cells"], k["n_gated"], k["n_unsearched"]) == (50, 6, 44), "6 of 50 cells gated, 44 UNSEARCHED")
    check(sorted(set(c["aid"] for c in k["parted"])) == ["heating.utility"], "the readings part on heating.utility")
    check(k["falsifier"] == [], "the falsifier is silent on the K rows")
    r = T.e32a_reading(gates + [T.row_retain_purchase()], zeros, acts)
    check([c["aid"] for c in r["falsifier"]] == ["clothing.retain"], "the falsifier fires on the constructed RETAIN row")
    e3 = T.e33_reading(gates)
    check(e3["shared_all"] == [] and e3["out"] == ["T-6"], "K rows: disjoint")
    e3b = T.e33_reading(gates + [T.row_fan_purchase()])
    check(e3b["shared_all"] == [T.MARKET_INSTRUMENT] and e3b["shared_nonmarket"] == [],
          "one purchase gate on a HEAT_OUT object fires the falsifier only when market purchase counts")
    e4 = T.e34_reading(gates, zeros + [T.zero_fans()], acts)
    check(all(v["non_body_residue"] == ["fans"] for v in e4.values()), "the E-A3-4 falsifier is reachable")
    check(T.e33_reading(T.sourced(gates)) == {"in": [], "out": [], "shared_all": [], "shared_nonmarket": []},
          "the sourced set is empty, not disjoint")


def t_locus_invariance():
    base = [(r["id"], r["status"]) for r in T.check_expectations()]
    orig = T.seed_actuators
    moved = {"EXTERNAL_OBJECT": "LAND_ACCESS", "EXTERNAL_STRUCTURE": "EXTERNAL_ENERGY", "EXTERNAL_ENERGY": "EXTERNAL_OBJECT",
             "LAND_ACCESS": "EXTERNAL_STRUCTURE"}

    def remapped():
        rows = orig()
        for a in rows:
            a["locus"] = moved.get(a["locus"], a["locus"])
        return rows
    T.seed_actuators = remapped
    try:
        after = [(r["id"], r["status"]) for r in T.check_expectations()]
    finally:
        T.seed_actuators = orig
    check(after == base, "remapping external loci among themselves moves no verdict [CHOICE 16]")


# ------------------------------------------------------------ fail fixtures ---

def t_fail_fixture():
    global FAIL_FIXTURES
    ff = T.fail_fixture()
    b = ff["f_t4_before"]
    check(isinstance(b["one_row_per_gate"], str) and isinstance(b["one_row_per_route"], str),
          "fail fixture 1: unamended A-2 returns ONE reading for F-T4, in both encodings")
    check(b["one_row_per_gate"] == "CONFLICT" and b["one_row_per_route"] == G.UNKNOWN_STATE,
          "the two single readings as recorded")
    check(ff["f_t4_after_positions"] == 4, "amended: four positions")
    check(isinstance(ff["pooled_before"], str), "fail fixture 2: unamended A-2 accepts the pooled input")
    check(ff["pooled_after"].startswith("REFUSED") and "2e" in ff["pooled_after"], "amended refuses it by 2e")
    if b["one_row_per_gate"] == "CONFLICT" and ff["pooled_after"].startswith("REFUSED"):
        FAIL_FIXTURES = 2


# ------------------------------------------------------------------ hygiene ---

def t_hygiene():
    r = render()
    ns = screen()
    if ns is not None:
        ok, h = ns.check(r)
        check(ok, "render screens clean with no exemption (%s)" % [x[1] for x in h][:5])
    p = subprocess.run([sys.executable, SRC, "--selftest"], capture_output=True, text=True)
    check(p.returncode == 2, "refuses --selftest with exit 2")
    p = subprocess.run([sys.executable, SRC, "--choices"], capture_output=True, text=True)
    check(p.returncode == 0 and p.stdout.count("[CHOICE") == len(T.CHOICES), "--choices prints every choice")
    check(sorted(T.CHOICES) == list(range(14, 24)), "choices numbered on from A-2.1's 9..13")
    body = SRC_TEXT.split('"""', 2)[2]
    decl_end = body.index("class ThermalError")
    rest = body[:body.index("CHOICES = {")] + body[decl_end:]
    for k in T.CHOICES:
        check(("[CHOICE %d]" % k) in rest, "[CHOICE %d] is cited outside its declaration" % k)
    p = subprocess.run([sys.executable, SRC], capture_output=True, text=True)
    check(p.returncode == 0, "runs with exit 0")
    src = open(SRC, "rb").read()
    check(all(b < 128 for b in src), "ASCII")
    ast.parse(src.decode("ascii"), feature_version=(3, 8))
    check(True, "parses under 3.8")
    check(os.path.exists(os.path.join(HERE, T.AMENDMENT_FILE)), "the amendment is present verbatim")
    log = subprocess.run(["git", "log", "--format=%h", "-n", "1", "--", T.AMENDMENT_FILE], cwd=HERE,
                         capture_output=True, text=True).stdout.strip()
    if log:
        check(log == T.EXPECTED_COMMIT_A3, "the amendment's last commit is the registered EXPECTED commit (%s)" % log)
    sample = os.path.join(HERE, "samples", "thermal_gates.sample.txt")
    if os.path.exists(sample):
        check(open(sample, encoding="utf-8").read() == r, "sample matches a fresh render")
    for other in ("test_gate_state.py", "test_gate_state_a21.py"):
        p = subprocess.run([sys.executable, os.path.join(HERE, other)], capture_output=True)
        check(p.returncode == 0, "%s still green" % other)


for fn in (t_structure, t_sources, t_actuators, t_gates, t_series, t_pooling, t_derived, t_couplings,
           t_expectations, t_locus_invariance, t_fail_fixture, t_hygiene):
    fn()

tag = "" if FAIL_FIXTURES else "  NO_FAIL_FIXTURE: thermal_gates"
print("thermal-gates: %d checks, %d failed; fail fixtures present: %d of 2%s" % (_checks, _failed, FAIL_FIXTURES, tag))
sys.exit(1 if _failed else 0)
