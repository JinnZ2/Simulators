"""test_terrain.py -- checks for terrain_prior.py.

    python3 test_terrain.py

Every expected verdict lives HERE and not in cases.py, so no case can agree
with the module by construction.  The check count is printed by this file and
is not written down anywhere else.

Stdlib only.  No pytest.  No network.
"""

import ast
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, ROOT)

import cases
import terrain_prior as tp
from tools.authority_scan import scan, split_identifier, PLANT

PASS = [0]
FAIL = []


def check(label, condition):
    PASS[0] += 1
    if not condition:
        FAIL.append(label)


def source(name):
    return io.open(os.path.join(HERE, name), encoding="ascii").read()


SRC = source("terrain_prior.py")
CASES_SRC = source("cases.py")
TREE = ast.parse(SRC)
FUNCS = dict((n.name, n) for n in ast.walk(TREE)
             if isinstance(n, ast.FunctionDef))


def names_in(node):
    out = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Name):
            out.add(sub.id)
        elif isinstance(sub, ast.Attribute):
            out.add(sub.attr)
        elif isinstance(sub, ast.arg):
            out.add(sub.arg)
        elif isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            out.add(sub.value)
    return out


def run(obs_id):
    obs = cases.BY_ID[obs_id]
    return tp.read(obs, cases.ENTRIES,
                   cases.MORPHOLOGIES_FOR.get(obs_id, ()))


RESULTS = dict((o["obs_id"], run(o["obs_id"])) for o in cases.OBSERVATIONS)


# ---------------------------------------------------------------------------
# 1. the work order's five validation cases
# ---------------------------------------------------------------------------

# A -- BOULDER, DRY STREAMBED.  "MUST return LOW bearing AND fire
# P2_SENSOR_INVERT.  If it does not flag the sensor inversion, the instrument
# has no advantage over the existing suite."
a = RESULTS["A_boulder"]
check("A: a prior is returned", a["bearing_prior"] is not None)
check("A: P2_SENSOR_INVERT fires", "P2_SENSOR_INVERT" in a["flags"])
# the order says LOW in its validation case and "Bearing is absent" in its own
# derivation text.  [CHOICE 10] takes the derivation text.  What is asserted
# here is the direction both agree on: below MODERATE.
check("A: bearing is below MODERATE",
      a["bearing_prior"]["class"] in ("VERY_LOW", "LOW"))
check("A: bearing class is VERY_LOW under CHOICE 10",
      a["bearing_prior"]["class"] == "VERY_LOW")
check("A: the prior is reached from flow direction plus one obstruction",
      a["entry_id"] == "boulder_sorted_streambed")
check("A: the mechanism is carried",
      "sorted the sediment" in a["bearing_prior"]["mechanism"])
check("A: every supplied platform exceeds the ground",
      all(row["bearing_verdict"] == tp.EXCEEDS for row in a["by_morphology"]))
# the two rungs the order gives do not agree for every platform.
brd = tp.boulder_rung_divergence(cases.MORPHOLOGIES)
check("A: VERY_LOW and LOW disagree for at least one platform",
      len(brd["platforms_where_rung_matters"]) == 1)
check("A: the platform where the rung matters is the low-pressure one",
      brd["platforms_where_rung_matters"] == ["broad_contact_low_pressure"])
# and the order's own sentence: a prior that cannot say what would disprove it
# is not engineering grade.  The stated validation target cannot.
check("A: falsified_by is not stated and is not invented",
      a["falsified_by"] is None)

# B -- PINE STAND.  "MUST fire P1_TWO_LAYER and return bearing referencing the
# substrate, not the duff."
b = RESULTS["B_pine"]
check("B: P1_TWO_LAYER fires", "P1_TWO_LAYER" in b["flags"])
check("B: bearing references the substrate",
      "substrate" in b["bearing_prior"]["value"])
check("B: bearing says the duff is not the bearing surface",
      "duff is not the bearing surface" in b["bearing_prior"]["value"])
check("B: two-layer does not imply the dangerous direction",
      "P2_SENSOR_INVERT" not in b["flags"])

# C -- MORPHOLOGY SPLIT.  "MUST return opposite bearing results and fire
# P3_MORPH_SPLIT.  If it returns one answer, it has reverted to rating the
# terrain."
c = RESULTS["C_split"]
check("C: P3_MORPH_SPLIT fires", "P3_MORPH_SPLIT" in c["flags"])
check("C: two morphology rows are returned", len(c["by_morphology"]) == 2)
c_bearings = [row["bearing_verdict"] for row in c["by_morphology"]]
check("C: the two bearing results are opposite",
      set(c_bearings) == set([tp.WITHIN, tp.EXCEEDS]))
check("C: the high-pressure platform exceeds",
      c["by_morphology"][0]["bearing_verdict"] == tp.EXCEEDS)
check("C: the low-pressure platform is within",
      c["by_morphology"][1]["bearing_verdict"] == tp.WITHIN)
check("C: nothing merges the two rows into one answer",
      "bearing_verdict" not in c)
# the order specifies case C on a bog and ships no bog entry.  Recorded.
check("C: run on the cattail entry, no bog entry invented",
      c["entry_id"] == "cattails")
check("C: no entry in the derivation set is a bog",
      not any("bog" in e["indicator"] for e in cases.ENTRIES))

# D -- FALSIFIER, NO MECHANISM.  "MUST fire P5 and return NO prior."
d = RESULTS["D_no_mechanism"]
check("D: P5_NO_MECHANISM fires", d["flags"] == ["P5_NO_MECHANISM"])
check("D: no bearing prior", d["bearing_prior"] is None)
check("D: no entanglement prior", d["entanglement_prior"] is None)
check("D: no verdict is produced either", d["by_morphology"] == [])
check("D: the reason is stated",
      d["no_prior_reason"] == tp.UNRATED_NO_MECHANISM)
check("D: the entry is still named, so the gap is locatable",
      d["entry_id"] == "sedge_tussocks_no_mechanism")
check("D: the entry does carry an implication, so P5 is not firing on "
      "emptiness",
      cases.NO_MECHANISM["implies_bearing"] != "")

# E -- OUT OF SCOPE.  "MUST return the prior WITH P4 flagged, not suppress it."
e = RESULTS["E_out_of_scope"]
check("E: P4_OUT_OF_SCOPE fires", "P4_OUT_OF_SCOPE" in e["flags"])
check("E: the prior is returned, not suppressed",
      e["bearing_prior"] is not None)
check("E: the entanglement prior is returned too",
      e["entanglement_prior"] is not None)
check("E: region_state says out of scope",
      e["region_state"] == tp.REGION_OUT_OF_SCOPE)
check("E: the entry's own scope travels with it",
      e["scope"] == "temperate wetland margins")
check("E: the prior is the same prior as in scope",
      e["bearing_prior"]["value"] == c["bearing_prior"]["value"])


# ---------------------------------------------------------------------------
# 2. two output variables, never collapsed
# ---------------------------------------------------------------------------

check("the two verdict vocabularies are disjoint",
      set([tp.WITHIN, tp.EXCEEDS]) & set([tp.CLEARS, tp.BINDS]) == set())
check("bearing_verdict reads no entanglement table",
      "TOLERATES" not in names_in(FUNCS["bearing_verdict"]))
check("entanglement_verdict reads no bearing table",
      "SUPPORTS" not in names_in(FUNCS["entanglement_verdict"]))
check("no function reads both tables",
      not any("SUPPORTS" in names_in(f) and "TOLERATES" in names_in(f)
              for f in FUNCS.values()))
# no ordering arithmetic on a class ladder anywhere: membership only.
check("no class ladder is indexed for an ordering comparison",
      ".index(" not in SRC)
ARITH = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Pow)
check("no arithmetic operator takes an operand from each axis",
      not any(isinstance(n, ast.BinOp) and isinstance(n.op, ARITH) and
              set(["bearing"]) & names_in(n) and
              set(["entanglement"]) & names_in(n)
              for n in ast.walk(TREE)))
check("no arithmetic operator touches a verdict at all",
      not any(isinstance(n, ast.BinOp) and isinstance(n.op, ARITH) and
              (names_in(n) & set(["bearing_verdict", "entanglement_verdict",
                                  "SUPPORTS", "TOLERATES"]))
              for n in ast.walk(TREE)))

# behavioural: moving one axis never moves the other.
_probe_entry = dict(cases.CATTAILS)
_bearing_seen = set()
_ent_seen = set()
for bc in tp.BEARING_CLASSES:
    for ec in tp.ENTANGLEMENT_CLASSES:
        _probe_entry["bearing_class"] = bc
        _probe_entry["entanglement_class"] = ec
        _bearing_seen.add((bc, tp.bearing_verdict(bc, "HIGH")))
        _ent_seen.add((ec, tp.entanglement_verdict(ec, "HIGH")))
check("a bearing verdict is a function of the bearing class alone",
      len(_bearing_seen) == len(tp.BEARING_CLASSES))
check("an entanglement verdict is a function of the entanglement class alone",
      len(_ent_seen) == len(tp.ENTANGLEMENT_CLASSES))

# P3 is specified on bearing only.  An entanglement split fires nothing.
split = tp.entanglement_split_has_no_check(
    cases.BY_ID["C_split"], cases.ENTRIES, cases.MORPHOLOGIES)
check("case C's entanglement results also differ in direction",
      split["entanglement_verdicts_differ"])
check("and no check in the order covers that",
      split["any_entanglement_check"] is False)


# ---------------------------------------------------------------------------
# 3. no single traversability score, ever
# ---------------------------------------------------------------------------

FORBIDDEN = set(["traversability", "traversable", "score", "scores",
                 "rating", "rate", "passable", "impassable", "ranked",
                 "rank", "grade", "overall"])
for token in sorted(FORBIDDEN):
    check("forbidden token %r is a single token and can match" % token,
          split_identifier(token) == [token])
check("no forbidden identifier in terrain_prior.py", scan(SRC, FORBIDDEN) == [])
check("no forbidden identifier in cases.py", scan(CASES_SRC, FORBIDDEN) == [])
PLANTED = PLANT + "def g():\n    traversability_score = 1\n    return 1\n"
check("the scanner fires on a plant",
      len(scan(PLANTED, FORBIDDEN | set(["citation", "count"]))) >= 2)
check("the plant's own token is caught",
      any(t in ("traversability", "score")
          for _, t in scan(PLANTED, FORBIDDEN)))
# nothing sums or averages anything anywhere.
check("no sum() in the module", "sum(" not in SRC)
check("no mean or average in the module",
      "mean(" not in SRC and "average(" not in SRC)


# ---------------------------------------------------------------------------
# 4. no entry without a mechanism
# ---------------------------------------------------------------------------

check("a whitespace mechanism is not a mechanism",
      not tp.has_mechanism({"mechanism": "   "}))
check("a missing mechanism is not a mechanism", not tp.has_mechanism({}))
check("a non-string mechanism is not a mechanism",
      not tp.has_mechanism({"mechanism": True}))
check("a stated mechanism is one", tp.has_mechanism({"mechanism": "x"}))
check("five of six entries carry a mechanism",
      sum(1 for e in cases.ENTRIES if tp.has_mechanism(e)) == 5)
check("the one that does not is the constructed case D entry",
      [e["entry_id"] for e in cases.ENTRIES
       if not tp.has_mechanism(e)] == ["sedge_tussocks_no_mechanism"])
# P5 is checked before anything else, including scope and context.
_no_mech_out_of_scope = dict(cases.BY_ID["D_no_mechanism"])
_no_mech_out_of_scope["region"] = "somewhere the entry does not claim"
_r = tp.read(_no_mech_out_of_scope, cases.ENTRIES, cases.MORPHOLOGIES)
check("P5 pre-empts every other flag", _r["flags"] == ["P5_NO_MECHANISM"])


# ---------------------------------------------------------------------------
# 5. region is a scope field, never a lookup key
# ---------------------------------------------------------------------------

r_names = names_in(FUNCS["resolve_entry"])
check("resolve_entry does not name region", "region" not in r_names)
check("resolve_entry does not name scope_regions",
      "scope_regions" not in r_names)
for obs in cases.OBSERVATIONS:
    check("resolution is invariant under a region swap: %s" % obs["obs_id"],
          tp.region_reaches_no_lookup(obs, cases.ENTRIES,
                                      "a region no entry claims"))
check("region_state DOES read region", "region" in names_in(FUNCS["region_state"]))


# ---------------------------------------------------------------------------
# 6. observer_baseline is carried verbatim and read by no check
# ---------------------------------------------------------------------------

for obs in cases.OBSERVATIONS:
    out = RESULTS[obs["obs_id"]]
    check("observer_baseline carried byte for byte: %s" % obs["obs_id"],
          out["observer_baseline"] == obs.get("observer_baseline"))
_base_probe = dict(cases.BY_ID["C_split"])
_seen = set()
for baseline in ("", "a", "forty years on this drainage", "x" * 400):
    _base_probe["observer_baseline"] = baseline
    got = tp.read(_base_probe, cases.ENTRIES, cases.MORPHOLOGIES)
    _seen.add((tuple(got["flags"]),
               got["bearing_prior"]["class"],
               got["entanglement_prior"]["class"],
               tuple(row["bearing_verdict"] for row in got["by_morphology"])))
check("observer_baseline changes no flag, no prior and no verdict",
      len(_seen) == 1)


# ---------------------------------------------------------------------------
# 7. no terrain rating independent of a morphology profile
# ---------------------------------------------------------------------------

j = RESULTS["J_cypress"]
check("with no morphology a prior is still returned",
      j["bearing_prior"] is not None)
check("with no morphology no verdict is returned", j["by_morphology"] == [])
check("with no morphology P3 cannot fire", "P3_MORPH_SPLIT" not in j["flags"])
check("a verdict exists only inside by_morphology",
      all(k not in j for k in ("bearing_verdict", "entanglement_verdict")))
# the morphology profile as the order specifies it reaches no check.
mf = tp.morphology_fields_reaching_a_check()
check("no order-specified morphology field reaches a check", mf["read"] == [])
check("all eight order-specified fields are carried and reach none",
      len(mf["unread"]) == 8)
check("every verdict rests on two fields this build added",
      mf["declared_only"] == ["pressure_class", "entanglement_susceptibility"])
for field in ("contact_pressure", "contact_area", "n_contacts",
              "ankle_to_foot_ratio", "swing_profile", "joint_exposure",
              "recovery_from_entanglement"):
    check("no function derives anything from %s" % field,
          not any(field in names_in(f) for name, f in FUNCS.items()
                  if name != "validate_morphology"))
check("validate_morphology only validates recovery_from_entanglement",
      "recovery_from_entanglement" in names_in(FUNCS["validate_morphology"]))
check("pressure_class is not computed anywhere",
      not any(isinstance(n, ast.Assign) and
              any(isinstance(t, ast.Name) and t.id == "pressure_class"
                  for t in n.targets)
              for n in ast.walk(TREE)))


# ---------------------------------------------------------------------------
# 8. absent is not a known negative
# ---------------------------------------------------------------------------

check("no flags fired is [] and not None", RESULTS["J_cypress"]["flags"] == [])
check("no prior is None and not an empty prior",
      RESULTS["H_no_entry"]["bearing_prior"] is None)
check("no prior carries a reason, always",
      all(r["no_prior_reason"] in tp.NO_PRIOR_REASONS
          for r in RESULTS.values() if r["bearing_prior"] is None))
check("a prior carries no reason",
      all(r["no_prior_reason"] is None
          for r in RESULTS.values() if r["bearing_prior"] is not None))
check("region unstated is not out of scope",
      tp.REGION_UNSTATED != tp.REGION_OUT_OF_SCOPE)
check("an unstated region does not fire P4",
      "P4_OUT_OF_SCOPE" not in RESULTS["A_boulder"]["flags"] and
      RESULTS["A_boulder"]["region_state"] == tp.REGION_UNSTATED)
check("sensor_invert UNKNOWN is not NONE",
      tp.INVERT_DIRECTIONS.index("UNKNOWN") !=
      tp.INVERT_DIRECTIONS.index("NONE"))
check("neither UNKNOWN nor NONE fires P2",
      "P2_SENSOR_INVERT" not in RESULTS["J_cypress"]["flags"] and
      "P2_SENSOR_INVERT" not in RESULTS["G_upstream"]["flags"])
check("an unstated class is NOT_EVALUABLE, not a verdict",
      tp.bearing_verdict("NOT_STATED", "LOW") == tp.VERDICT_NOT_EVALUABLE)
check("an unstated entanglement class is NOT_EVALUABLE, not CLEARS",
      tp.entanglement_verdict("NOT_STATED", "LOW") ==
      tp.VERDICT_NOT_EVALUABLE)
check("a missing pressure class is NOT_EVALUABLE, not EXCEEDS",
      tp.bearing_verdict("LOW", None) == tp.VERDICT_NOT_EVALUABLE)
check("intake missing and intake invalid are separate lists",
      isinstance(RESULTS["I_intake"]["intake_missing"], list) and
      RESULTS["I_intake"]["intake_missing"] == ["observer_baseline"] and
      RESULTS["I_intake"]["intake_invalid"] == [])
_bad = dict(cases.BY_ID["C_split"])
_bad["indicator_type"] = "SHRUBBERY"
check("an out-of-vocabulary indicator_type is invalid, not missing",
      tp.read(_bad, cases.ENTRIES)["intake_invalid"] == ["indicator_type"])


# ---------------------------------------------------------------------------
# 9. reachability -- a declared member nothing populates is not a member
# ---------------------------------------------------------------------------

flags_seen = set()
for r in RESULTS.values():
    flags_seen |= set(r["flags"])
check("every check code is reached", flags_seen == set(tp.CHECK_CODES))
reasons_seen = set(r["no_prior_reason"] for r in RESULTS.values())
reasons_seen.discard(None)
check("every no-prior reason is reached",
      reasons_seen == set(tp.NO_PRIOR_REASONS))
states_seen = set(r["region_state"] for r in RESULTS.values())
states_seen.discard(None)
check("every region state is reached", states_seen == set(tp.REGION_STATES))
bv = set()
ev = set()
for r in RESULTS.values():
    for row in r["by_morphology"]:
        bv.add(row["bearing_verdict"])
        ev.add(row["entanglement_verdict"])
check("WITHIN and EXCEEDS are both reached on the case set",
      set([tp.WITHIN, tp.EXCEEDS]) <= bv)
check("CLEARS and BINDS are both reached on the case set",
      set([tp.CLEARS, tp.BINDS]) <= ev)
check("NOT_EVALUABLE is reached on the entanglement axis",
      tp.VERDICT_NOT_EVALUABLE in ev)
# bearing NOT_EVALUABLE needs an entry with no bearing class.  There is none
# in the derivation set; the branch is exercised directly above.
check("no entry in the set leaves bearing unstated",
      tp.class_coverage(cases.ENTRIES)["bearing_not_stated"] == 0)
inverts = set()
bases = set()
confidences = set()
b_classes = set()
b_classes_stated = set()
e_classes = set()
for entry in cases.ENTRIES:
    sources = [entry] + list(entry.get("context_branches") or [])
    for src in sources:
        inverts.add(src.get("sensor_invert", entry.get("sensor_invert",
                                                       "UNKNOWN")))
        bases.add(src.get("bearing_class_basis", "NOT_STATED"))
        bases.add(src.get("entanglement_class_basis", "NOT_STATED"))
        b_classes.add(src.get("bearing_class", "NOT_STATED"))
        e_classes.add(src.get("entanglement_class", "NOT_STATED"))
        if "bearing_class" in src:
            b_classes_stated.add(src["bearing_class"])
    confidences.add(entry.get("confidence", "NOT_STATED"))
check("every sensor_invert direction is reached",
      inverts == set(tp.INVERT_DIRECTIONS))
check("every class_basis is reached", bases == set(tp.CLASS_BASIS))
check("every bearing class is reached except NOT_STATED",
      b_classes_stated == set(tp.BEARING_CLASSES) - set(["NOT_STATED"]))
check("the boulder entry states no top-level bearing class, because its "
      "prior is branch-conditioned",
      "bearing_class" not in cases.BOULDER)
# the second output variable is the one most often unstated in the order's own
# seed set, and its LOW rung is reached by nothing.
check("entanglement LOW is reached by no entry",
      "LOW" not in e_classes)
check("entanglement MODERATE is reached only by the mechanism-less entry",
      [e["entry_id"] for e in cases.ENTRIES
       if e.get("entanglement_class") == "MODERATE"] ==
      ["sedge_tussocks_no_mechanism"])
check("confidence MEDIUM is reached by no entry",
      "MEDIUM" not in confidences)


# ---------------------------------------------------------------------------
# 10. null tests -- every check fires and every check stays silent
# ---------------------------------------------------------------------------

check("P1 fires on pine", "P1_TWO_LAYER" in RESULTS["B_pine"]["flags"])
check("P1 silent on cypress",
      "P1_TWO_LAYER" not in RESULTS["J_cypress"]["flags"])
check("P2 fires on cattails", "P2_SENSOR_INVERT" in RESULTS["C_split"]["flags"])
check("P2 silent on pine, which is two-layer the other way",
      "P2_SENSOR_INVERT" not in RESULTS["B_pine"]["flags"])
check("P3 fires on the split", "P3_MORPH_SPLIT" in RESULTS["C_split"]["flags"])
check("P3 silent when both platforms agree",
      "P3_MORPH_SPLIT" not in RESULTS["A_boulder"]["flags"])
check("P3 silent on one morphology",
      "P3_MORPH_SPLIT" not in RESULTS["K_hardwoods"]["flags"])
check("P4 fires out of scope",
      "P4_OUT_OF_SCOPE" in RESULTS["E_out_of_scope"]["flags"])
check("P4 silent in scope",
      "P4_OUT_OF_SCOPE" not in RESULTS["C_split"]["flags"])
check("P5 fires with no mechanism",
      "P5_NO_MECHANISM" in RESULTS["D_no_mechanism"]["flags"])
check("P5 silent with a mechanism",
      "P5_NO_MECHANISM" not in RESULTS["C_split"]["flags"])
check("split_is_reachable is true on C",
      tp.split_is_reachable(cases.BY_ID["C_split"], cases.ENTRIES,
                            cases.MORPHOLOGIES))
check("split_is_reachable is false on A",
      not tp.split_is_reachable(cases.BY_ID["A_boulder"], cases.ENTRIES,
                                cases.MORPHOLOGIES))
check("an entry with branches and no match returns no prior",
      RESULTS["F_no_branch"]["no_prior_reason"] == tp.NO_CONTEXT_BRANCH)
check("and does not fall back to an unconditioned reading",
      RESULTS["F_no_branch"]["bearing_prior"] is None)
check("the other branch is reachable",
      RESULTS["G_upstream"]["bearing_prior"]["class"] == "MODERATE")
check("the two branches disagree, which is why the entry has them",
      RESULTS["G_upstream"]["bearing_prior"]["class"] !=
      RESULTS["A_boulder"]["bearing_prior"]["class"])


# ---------------------------------------------------------------------------
# 11. the derivation set measured, not imputed
# ---------------------------------------------------------------------------

fc = tp.falsifier_coverage(cases.ENTRIES)
check("falsifier coverage counts every entry", fc["total"] == 6)
check("one entry states a falsifier", fc["stated"] == 1)
check("the one that does is the entry the order writes out in full",
      cases.CATTAILS["falsified_by"] is not None)
check("five do not and none is invented", fc["unstated"] == 5)
cc = tp.class_coverage(cases.ENTRIES)
check("four of six entries state no entanglement",
      cc["entanglement_not_stated"] == 4)
check("one bearing class is quoted from the order",
      cc["bearing_order_stated"] == 1)
check("one entanglement class is quoted from the order",
      cc["entanglement_order_stated"] == 1)


# ---------------------------------------------------------------------------
# 12. choices declared and cited
# ---------------------------------------------------------------------------

rendered = tp.render_choices()
check("ten choices are declared", len(tp.CHOICES) == 10)
for n in tp.CHOICES:
    check("[CHOICE %d] is printed" % n, "[CHOICE %d]" % n in rendered)
# strip the CHOICES dict literal, then require each marker to appear elsewhere.
_lines = SRC.split("\n")
_start = [i for i, ln in enumerate(_lines) if ln.startswith("CHOICES = {")][0]
_end = [i for i, ln in enumerate(_lines) if i > _start and ln == "}"][0]
_outside = "\n".join(_lines[:_start] + _lines[_end + 1:]) + CASES_SRC
for n in tp.CHOICES:
    check("[CHOICE %d] is cited where it takes effect" % n,
          "[CHOICE %d]" % n in _outside)


# ---------------------------------------------------------------------------
# 13. housekeeping
# ---------------------------------------------------------------------------

class _Quiet(object):
    def write(self, _):
        pass

    def flush(self):
        pass


_out, _err = sys.stdout, sys.stderr
sys.stdout = sys.stderr = _Quiet()
try:
    _selftest_rc = tp.main(["--selftest"])
    _choices_rc = tp.main(["--choices"])
finally:
    sys.stdout, sys.stderr = _out, _err
check("the module refuses --selftest", _selftest_rc == 2)
check("--choices returns 0", _choices_rc == 0)
for name in ("terrain_prior.py", "cases.py", "test_terrain.py"):
    raw = io.open(os.path.join(HERE, name), "rb").read()
    check("%s is ASCII" % name, all(byte < 128 for byte in bytearray(raw)))
# WORK_ORDER.md is delivered and is landed verbatim.  It carries em dashes.
# It is not transliterated, so the ASCII rule is a rule about what is built
# here and the delivered document is recorded as an exception rather than
# quietly edited into compliance.
_order_raw = io.open(os.path.join(HERE, "WORK_ORDER.md"), "rb").read()
check("the delivered order is not ASCII and is not rewritten to be",
      not all(byte < 128 for byte in bytearray(_order_raw)))
imports = set()
for node in ast.walk(TREE):
    if isinstance(node, ast.Import):
        imports |= set(a.name.split(".")[0] for a in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module:
        imports.add(node.module.split(".")[0])
check("terrain_prior imports only sys and cases",
      imports <= set(["sys", "cases"]))
check("no networked import anywhere",
      imports & set(["socket", "urllib", "http", "requests", "ssl"]) == set())
# no expected verdict lives in cases.py.
for code in tp.CHECK_CODES:
    check("%s does not appear in cases.py" % code, code not in CASES_SRC)
for word in (tp.WITHIN, tp.EXCEEDS, tp.CLEARS, tp.BINDS):
    check("verdict %s does not appear in cases.py" % word,
          word not in CASES_SRC)
check("every observation declares itself constructed",
      all(o.get("source") == cases.CONSTRUCTED for o in cases.OBSERVATIONS))
check("every morphology declares itself constructed",
      all(m.get("source") == cases.CONSTRUCTED for m in cases.MORPHOLOGIES))
check("the order's five validation cases are all present",
      set(cases.ORDER_CASES) <= set(cases.BY_ID))


# ---------------------------------------------------------------------------

print("terrain-prior: %d checks, %d failed" % (PASS[0], len(FAIL)))
for label in FAIL:
    print("  FAIL: " + label)
sys.exit(1 if FAIL else 0)
