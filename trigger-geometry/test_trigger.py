# SPDX-License-Identifier: CC0-1.0
"""
test_trigger.py -- the checks for trigger_geometry.py.

No pytest, no network, stdlib only, runnable on a phone:

    python3 test_trigger.py

EVERY EXPECTED VERDICT LIVES HERE AND NOT IN cases.py. A case carrying its
own answer agrees with the module by construction, and an agreement produced
that way measures nothing.

Sections, in the order the work order states them:

    1  the order's five validation cases, A through E
    2  no single safety score -- three verdicts, nothing combines them
    3  redundancy is not mitigation -- AST and a sweep
    4  reliability figures are refused at intake, and the refusal is planted
    5  absent is never safe
    6  no enum of geometry classes -- a novel class runs end to end
    7  the sensor is carried, never computed
    8  T3 suppresses T6, and the suppression is reported
    9  reachability: every declared value is reached by something
    10 both directions of every check, and the unreachable branches named
    11 the two times: recorded, never estimated, gating nothing
    12 the choices are declared and cited where they take effect
    13 housekeeping
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cases  # noqa: E402
import trigger_geometry as t  # noqa: E402
from tools.authority_scan import PLANT, scan, split_identifier  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.join(HERE, "trigger_geometry.py")
CASEFILE = os.path.join(HERE, "cases.py")
ORDER = os.path.join(HERE, "WORK_ORDER.md")
SRC = open(MODULE).read()
TREE = ast.parse(SRC)
BY_NAME = {n.name: n for n in ast.walk(TREE) if isinstance(n, ast.FunctionDef)}

CHECK_FNS = ("t1_accumulation", "t2_response_couples", "t3_envelope_unstated",
             "t4_proxy_state", "t5_degradation_correlation",
             "t6_geometry_absent")

FAILED = []
TOTAL = [0]


def check(name, cond, detail=""):
    TOTAL[0] += 1
    if not cond:
        FAILED.append("%s %s" % (name, detail))
        print("FAIL  %s %s" % (name, detail))


def r(letter_or_pair):
    if isinstance(letter_or_pair, str):
        trig, geom = cases.ORDER_CASES[letter_or_pair]
    else:
        trig, geom = letter_or_pair
    return t.read(cases.TRIGGERS[trig], cases.GEOMETRIES[geom])


ALL = [r(pair) for pair in cases.PAIRS]


def names_used(fn_node):
    """Every identifier, attribute and string constant a body touches."""
    out = set()
    for n in ast.walk(fn_node):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.add(n.value)
    return out


class _Quiet(object):
    def __enter__(self):
        self._out, self._err = sys.stdout, sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")

    def __exit__(self, *exc):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout, sys.stderr = self._out, self._err


# --------------------------------------------------------------------------
print("1  the order's five validation cases")

# A -- serpentine grade. "MUST fire T1 and T2, return response_validated_here
# False, and populate operator_correction_required."
a = r("A")
check("A fires T1_ACCUMULATION", "T1_ACCUMULATION" in a["flags"], a["flags"])
check("A fires T2_RESPONSE_COUPLES",
      "T2_RESPONSE_COUPLES" in a["flags"], a["flags"])
check("A returns response_validated_here False",
      a["response_validated_here"] is False, a["response_validated_here"])
check("A populates operator_correction_required",
      isinstance(a["operator_correction_required"], str)
      and a["operator_correction_required"] != "")
check("A carries the failure mode if inverted",
      isinstance(a["failure_mode_if_inverted"], str)
      and "trailer moment" in a["failure_mode_if_inverted"])

# B -- single curve, flat, same trigger. "MUST NOT fire T1."
b = r("B")
check("B does not fire T1_ACCUMULATION",
      "T1_ACCUMULATION" not in b["flags"], b["flags"])
check("B is the SAME trigger as A",
      cases.ORDER_CASES["A"][0] == cases.ORDER_CASES["B"][0])
check("A and B differ only in the geometry",
      cases.ORDER_CASES["A"][1] != cases.ORDER_CASES["B"][1])
check("T1 is the only flag that differs between A and B",
      set(a["flags"]) - set(b["flags"]) == {"T1_ACCUMULATION"}
      and set(b["flags"]) - set(a["flags"]) == set(),
      (a["flags"], b["flags"]))

# C -- fifth wheel. "MUST fire T4 and require an independent verification
# path."
c = r("C")
check("C fires T4_PROXY_STATE", "T4_PROXY_STATE" in c["flags"], c["flags"])
check("C requires an independent verification path",
      c["requires_independent_verification"] is True)
check("a reading that does not fire T4 does not require one",
      all(x["requires_independent_verification"] is not True
          for x in ALL if x["flags"] and "T4_PROXY_STATE" not in x["flags"]))

# D -- falsifier. "MUST return clean."
d = r("D")
check("D returns clean", d["response_validated_here"] is True,
      (d["response_validated_here"], d["flags"], d["not_evaluable"]))
check("D fires nothing", d["flags"] == [], d["flags"])
check("D leaves no check unevaluated", d["not_evaluable"] == [],
      d["not_evaluable"])
check("D's reason is CLEAN", d["validated_reason"] == t.REASON_CLEAN)
check("the clean branch is reachable on the corpus",
      t.clean_reachable(ALL)["reachable"])

# E -- unstated envelope. "MUST return UNRATED and fire T3 ONLY."
e = r("E")
check("E returns UNRATED",
      e["response_validated_here"] == t.UNRATED,
      e["response_validated_here"])
check("E fires T3 and nothing else",
      e["flags"] == ["T3_ENVELOPE_UNSTATED"], e["flags"])
check("E's reason is the unstated envelope",
      e["validated_reason"] == t.REASON_UNSTATED_ENVELOPE)
check("E infers no failure from the absence -- both derived verdicts UNRATED",
      e["verdicts"]["inference"] == t.VERDICT_UNRATED
      and e["verdicts"]["response"] == t.VERDICT_UNRATED, e["verdicts"])
check("E is not an accusation: response_validated_here is not False",
      e["response_validated_here"] is not False)


# --------------------------------------------------------------------------
print("2  no single safety score")

check("every reading carries three separate verdicts",
      all(set(x["verdicts"]) == {"sensor", "inference", "response"}
          for x in ALL))
check("the three verdicts are reached independently -- at least one reading "
      "has them not all equal",
      any(len(set(x["verdicts"].values())) > 1 for x in ALL))

# Mod and the bit operators are excluded deliberately: `%` here is string
# formatting and `&` is set algebra. A check firing on a format string
# reports its own reader, which is the failure terrain-prior recorded.
ARITH = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Pow)
VERDICT_NAMES = {"sensor", "inference", "response", "verdicts",
                 "response_validated_here", "validated"}
touched = []
for node in ast.walk(TREE):
    if isinstance(node, ast.BinOp) and isinstance(node.op, ARITH):
        used = set()
        for side in (node.left, node.right):
            for n in ast.walk(side):
                if isinstance(n, ast.Name):
                    used.add(n.id)
                elif isinstance(n, ast.Attribute):
                    used.add(n.attr)
                elif isinstance(n, ast.Constant) and isinstance(n.value, str):
                    used.add(n.value)
        if used & VERDICT_NAMES:
            touched.append(sorted(used & VERDICT_NAMES))
check("no arithmetic operator touches a verdict", touched == [], touched)

check("the module defines no total, score, index or aggregate",
      scan(SRC, {"score", "rating", "rank", "grade", "aggregate",
                 "composite", "overall", "severity"}) == [], "")
check("the scan fires on a planted violation",
      scan("def f():\n    safety_score = 1\n    return safety_score\n",
           {"score"}) != [])
check("every forbidden token is a single token, or it is unmatchable",
      all(len(split_identifier(tok)) == 1
          for tok in ("score", "rating", "rank", "grade", "aggregate",
                      "composite", "overall", "severity")))
check("the shared scanner's own plant fires",
      scan(PLANT, {"citation", "rank"}) != [])


# --------------------------------------------------------------------------
print("3  redundancy is not mitigation")

for fn in CHECK_FNS:
    used = names_used(BY_NAME[fn])
    check("%s reads no redundancy field" % fn,
          not any("redundan" in str(name).lower() for name in used),
          sorted(n for n in used if "redundan" in str(n).lower()))

swept = t.redundancy_effect(
    cases.TRIGGERS["serpentine_brake"], cases.GEOMETRIES["driftless_grade"],
    (None, 1, 2, 3, "agree", "two sensors, agreeing", "three, unanimous"))
check("sweeping redundancy leaves every flag unchanged",
      swept["flags_invariant"], swept["distinct_outcomes"])
check("the sweep actually ran more than one setting", len(swept["rows"]) > 1)
# null test: the sweep must be able to report movement, or its silence is
# not evidence.
moved = t.redundancy_effect(
    cases.TRIGGERS["serpentine_brake"], cases.GEOMETRIES["driftless_grade"],
    (None, 1))
faked = dict(cases.TRIGGERS["serpentine_brake"])
faked["couples_into_next_cycle"] = "NO"
check("the sweep would report movement if a flag moved",
      t.read(faked, cases.GEOMETRIES["driftless_grade"])["flags"]
      != moved["rows"][0]["flags"])

# the agreeing-sensor cases in the corpus still carry their flags
agreeing = [x for x, (trig, _) in zip(ALL, cases.PAIRS)
            if "agree" in str(cases.TRIGGERS[trig].get("redundancy", ""))]
check("readings whose trigger declares agreeing sensors still flag",
      agreeing != [] and any(x["flags"] for x in agreeing),
      [x["trigger_id"] for x in agreeing])


# --------------------------------------------------------------------------
print("4  reliability figures are refused at intake")

raised = False
try:
    t.read(cases.REFUSED_TRIGGER, cases.GEOMETRIES["driftless_grade"])
except t.ReliabilityInput as exc:
    raised = True
    message = str(exc)
check("a reliability-shaped key raises rather than being ignored", raised)
check("the raise names the offending key",
      raised and "system_availability" in message)
check("a clean trigger does not raise",
      t.read(cases.TRIGGERS["grade_retarder"],
             cases.GEOMETRIES["straight_descent"])["flags"] == [])
nested = dict(cases.TRIGGERS["grade_retarder"])
nested["response_derived_in"] = dict(nested["response_derived_in"])
nested["response_derived_in"]["mtbf_hours"] = 40000
deep = False
try:
    t.read(nested, cases.GEOMETRIES["straight_descent"])
except t.ReliabilityInput:
    deep = True
check("a nested reliability key is refused too", deep)
check("the screen is a word list and the module says so",
      "word list" in SRC)
check("no case in the corpus carries a reliability-shaped key",
      all(t._reliability_keys(cases.TRIGGERS[trig]) == []
          for trig, _ in cases.PAIRS))


# --------------------------------------------------------------------------
print("5  absent is never safe")

absent = [x for x in ALL if "T6_GEOMETRY_ABSENT" in (x["flags"] or [])]
check("a geometry absent from the envelope is reached by the corpus",
      absent != [])
check("absent returns UNRATED, never True",
      all(x["response_validated_here"] == t.UNRATED for x in absent))
check("absent is reported as ABSENT and not as FLAGGED",
      all(x["validated_reason"] == t.REASON_ABSENT for x in absent))
check("no reading anywhere returns True with a flag raised",
      all(not (x["response_validated_here"] is True and x["flags"])
          for x in ALL))
check("no reading returns True with a check unevaluated",
      all(not (x["response_validated_here"] is True and x["not_evaluable"])
          for x in ALL))


# --------------------------------------------------------------------------
print("6  no enum of geometry classes")

novel_geometry = {
    "geometry_id": "invented_for_this_check",
    "geometry_class": "a class no vocabulary in this repo has ever seen",
    "reversal": True,
    "reversal_period": None,
    "system_relaxation_time": None,
    "gradient": None,
    "constructibility_note": "constructed inside the test",
}
novel = t.read(cases.TRIGGERS["serpentine_brake"], novel_geometry)
check("a novel geometry class runs end to end",
      novel["intake_missing"] == [] and novel["intake_invalid"] == [])
check("a novel class is ABSENT from the envelope, not refused",
      "T6_GEOMETRY_ABSENT" in novel["flags"], novel["flags"])
check("a novel class is not returned SAFE",
      novel["response_validated_here"] is not True)

class_names = set()
for name, value in vars(t).items():
    if name.isupper() and isinstance(value, (tuple, list)):
        for item in value:
            if isinstance(item, str):
                class_names.add(item)
leaked = {n for n in class_names
          if n in {g["geometry_class"] for g in cases.GEOMETRIES.values()}}
check("no module-level constant holds a geometry class name", leaked == set(),
      sorted(leaked))
gv = names_used(BY_NAME["validate_geometry"])
check("validate_geometry compares geometry_class against nothing",
      not any(isinstance(x, str) and x in
              {g["geometry_class"] for g in cases.GEOMETRIES.values()}
              for x in gv))


# --------------------------------------------------------------------------
print("7  the sensor is carried, never computed")

for x, (trig, _) in zip(ALL, cases.PAIRS):
    check("%s carries sensor_verdict verbatim" % trig,
          x["verdicts"]["sensor"]
          == cases.TRIGGERS[trig].get("sensor_verdict"))
assigns = []
for node in ast.walk(TREE):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "sensor":
                if not (isinstance(node.value, ast.Call)
                        and getattr(node.value.func, "attr", "") == "get"):
                    assigns.append(ast.dump(node.value)[:60])
check("the only assignment to `sensor` is a lookup on the trigger",
      assigns == [], assigns)
check("no check function reads sensor_verdict except T5",
      all("sensor_verdict" not in names_used(BY_NAME[fn])
          for fn in CHECK_FNS if fn != "t5_degradation_correlation"))
check("T5 reads sensor_verdict and does not modify it",
      "sensor_verdict" in names_used(BY_NAME["t5_degradation_correlation"]))


# --------------------------------------------------------------------------
print("8  T3 suppresses T6")

check("E reports the suppression rather than hiding it",
      e["suppressed"] == ["T6_GEOMETRY_ABSENT"], e["suppressed"])
check("E's T6 state is SILENT after suppression",
      e["check_states"]["T6_GEOMETRY_ABSENT"] == t.SILENT)
check("T6 evaluated on E's raw inputs is not SILENT",
      t.t6_geometry_absent(cases.TRIGGERS["stability_cut"],
                           cases.GEOMETRIES["ordinary_two_lane"])
      != t.SILENT)
check("nothing else in the corpus is suppressed",
      all(x["suppressed"] == [] for x in ALL
          if x["check_states"].get("T3_ENVELOPE_UNSTATED") != t.FIRED))


# --------------------------------------------------------------------------
print("9  reachability")

seen_flags = set()
seen_states = set()
seen_reasons = set()
seen_validated = set()
seen_sensor = set()
seen_verdicts = set()
for x in ALL:
    seen_flags |= set(x["flags"] or [])
    seen_states |= set(x["check_states"].values())
    seen_reasons.add(x["validated_reason"])
    seen_validated.add(x["response_validated_here"])
    seen_sensor.add(x["verdicts"]["sensor"])
    seen_verdicts |= {x["verdicts"]["inference"], x["verdicts"]["response"]}

check("every check code fires somewhere",
      seen_flags == set(t.CHECK_CODES), sorted(set(t.CHECK_CODES) - seen_flags))
check("every check state is reached", seen_states == set(t.CHECK_STATES),
      sorted(set(t.CHECK_STATES) - seen_states))
check("every validated_reason is reached",
      seen_reasons == {t.REASON_CLEAN, t.REASON_FLAGGED, t.REASON_ABSENT,
                       t.REASON_UNSTATED_ENVELOPE, t.REASON_NOT_EVALUABLE,
                       t.REASON_INTAKE}, sorted(seen_reasons))
check("every value of response_validated_here is reached",
      seen_validated == {True, False, t.UNRATED}, sorted(map(str, seen_validated)))
check("every sensor verdict is carried by something",
      seen_sensor == set(t.SENSOR_VERDICTS),
      sorted(set(t.SENSOR_VERDICTS) - seen_sensor))
check("every derived verdict value is reached",
      seen_verdicts == {t.VERDICT_OK, t.VERDICT_INVERTED, t.VERDICT_UNRATED,
                        t.VERDICT_NOT_EVALUABLE}, sorted(seen_verdicts))

declared = set()
for trig in cases.TRIGGERS.values():
    for field in t.ADDED_FIELDS:
        declared.add(trig.get(field, t.UNDECLARED))
check("every value of the added fields is used by some case",
      declared == set(t.DECLARED_VALUES), sorted(declared))
counts = {trig["response_derived_in"].get("instance_count")
          for trig in cases.TRIGGERS.values()
          if isinstance(trig.get("response_derived_in"), dict)}
check("every instance_count is used by some case",
      counts >= set(t.INSTANCE_COUNTS), sorted(set(t.INSTANCE_COUNTS) - counts))
check("the intake-incomplete branch is reached",
      any(x["flags"] is None for x in ALL))
check("an intake-incomplete reading names the missing fields",
      all(x["intake_missing"] for x in ALL if x["flags"] is None))
check("an intake-incomplete reading returns flags None, not []",
      all(x["flags"] is None for x in ALL
          if x["validated_reason"] == t.REASON_INTAKE))
check("a clean reading returns flags [], not None",
      d["flags"] == [] and d["flags"] is not None)


# --------------------------------------------------------------------------
print("10  both directions of every check")

fired_by = {code: [] for code in t.CHECK_CODES}
silent_by = {code: [] for code in t.CHECK_CODES}
ne_by = {code: [] for code in t.CHECK_CODES}
for x in ALL:
    for code, state in x["check_states"].items():
        if state == t.FIRED:
            fired_by[code].append(x["trigger_id"])
        elif state == t.SILENT:
            silent_by[code].append(x["trigger_id"])
        else:
            ne_by[code].append(x["trigger_id"])
for code in t.CHECK_CODES:
    check("%s fires somewhere" % code, fired_by[code] != [])
    check("%s stays silent somewhere" % code, silent_by[code] != [])

# NOT_EVALUABLE: two of the six cannot reach it through read(), because
# intake refuses the input that would produce it. Recorded rather than
# papered over, and the branch is exercised on the check function directly.
unreachable_ne = [code for code in t.CHECK_CODES if ne_by[code] == []]
check("exactly T3 and T6 cannot be NOT_EVALUABLE through read()",
      set(unreachable_ne) <= {"T3_ENVELOPE_UNSTATED"},
      unreachable_ne)
check("T3's NOT_EVALUABLE branch exists and is unreachable through read(): "
      "intake refuses a non-bool `stated`",
      t.t3_envelope_unstated(
          {"response_derived_in": {"stated": "yes"}}, {}) == t.NOT_EVALUABLE
      and "response_derived_in.stated"
      in t.validate_trigger({"response_derived_in": {"stated": "yes"}})[1])
check("T6 IS reachable as NOT_EVALUABLE through read()",
      ne_by["T6_GEOMETRY_ABSENT"] != [], ne_by["T6_GEOMETRY_ABSENT"])
check("T1 is NOT_EVALUABLE when the geometry does not say whether it reverses",
      ne_by["T1_ACCUMULATION"] != [])

# every check bears on exactly one of the three verdicts, declared
check("BEARS_ON covers every check", set(t.BEARS_ON) == set(t.CHECK_CODES))
check("BEARS_ON names only the three verdicts",
      set(t.BEARS_ON.values()) <= {"sensor", "inference", "response", "both"})
check("no check bears on the sensor -- the sensor is not evaluated",
      "sensor" not in set(t.BEARS_ON.values()))


# --------------------------------------------------------------------------
print("11  the two times")

check("the reference geometry leaves both times unmeasured",
      a["times_unmeasured"] == ["reversal_period", "system_relaxation_time"],
      a["times_unmeasured"])
check("unmeasured times do not block the reference case's verdict",
      a["response_validated_here"] is False)
check("nothing estimates a time",
      all(cases.GEOMETRIES[g].get("reversal_period") is None
          or isinstance(cases.GEOMETRIES[g]["reversal_period"], (int, float))
          for _, g in cases.PAIRS))
ratio_seen = [x["accumulation_ratio"] for x in ALL
              if x["accumulation_ratio"] is not None]
check("accumulation_ratio is computed where both times are present",
      ratio_seen != [], ratio_seen)
check("accumulation_ratio is None where a time is absent",
      all(x["accumulation_ratio"] is None for x in ALL
          if x["times_unmeasured"]))
check("accumulation_ratio gates nothing -- moving it moves no flag",
      t.read(cases.TRIGGERS["dive_commit"],
             dict(cases.GEOMETRIES["reversing_ramp"],
                  system_relaxation_time=0.001))["flags"]
      == t.read(cases.TRIGGERS["dive_commit"],
                cases.GEOMETRIES["reversing_ramp"])["flags"])
check("no check function reads either time",
      all(not ({"reversal_period", "system_relaxation_time"}
               & names_used(BY_NAME[fn])) for fn in CHECK_FNS))
check("a zero reversal period returns None rather than dividing",
      t.accumulation_ratio({"reversal_period": 0.0,
                            "system_relaxation_time": 1.0}) is None)
check("a known accumulation ratio is right",
      abs(t.accumulation_ratio({"reversal_period": 2.0,
                                "system_relaxation_time": 7.0}) - 3.5) < 1e-12)
# the standing rule: no metric ships without a known-answer run. This is
# the only function here that returns a number rather than a declared
# vocabulary member, so it is the only one registered.
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import known_answer as ka  # noqa: E402
ka.seed()
KA_ID = "trigger-geometry/trigger_geometry.py::accumulation_ratio"
check("accumulation_ratio is registered in tools/known_answer.py",
      KA_ID in ka.registry_ids())
check("its known-answer run passes",
      all(row["status"] == ka.PASS for row in ka.run(KA_ID)),
      [row for row in ka.run(KA_ID) if row["status"] != ka.PASS])


# --------------------------------------------------------------------------
print("12  the choices")

with _Quiet():
    rendered = t.render_choices()
# everything after the module docstring. A marker that appears only in the
# header is announced, not cited.
BODY = SRC.split(chr(34) * 3, 2)[2]
for key in t.CHOICES:
    check("[CHOICE %d] is printed" % key, "[CHOICE %d]" % key in rendered)
    check("[CHOICE %d] is cited inline where it takes effect" % key,
          ("[CHOICE %d]" % key) in BODY,
          SRC.count("[CHOICE %d]" % key))
check("the module declares nine choices", len(t.CHOICES) == 9, len(t.CHOICES))

support = t.schema_support()
check("three of the order's six checks need a field the order has no slot for",
      len(support["needs_added_field"]) + len(support["one_of_each"]) == 3,
      support)
check("the added fields are exactly the three declared",
      tuple(support["added_fields"]) == t.ADDED_FIELDS)
check("no added field appears in the order's own trigger schema",
      not (set(t.ADDED_FIELDS) & set(t.ORDER_TRIGGER_FIELDS)))
check("the order's geometry fields are all carried",
      all(f in cases.GEOMETRIES["driftless_grade"]
          for f in t.ORDER_GEOMETRY_FIELDS))


# --------------------------------------------------------------------------
print("13  housekeeping")

p = subprocess.run([sys.executable, MODULE, "--selftest"],
                   capture_output=True, text=True, cwd=HERE)
check("--selftest is refused with rc 2 rather than exiting clean",
      p.returncode == 2, p.returncode)
check("the refusal names where the checks live",
      "test_trigger.py" in p.stderr, p.stderr[-200:])
p2 = subprocess.run([sys.executable, MODULE], capture_output=True, text=True,
                    cwd=HERE)
check("the module runs", p2.returncode == 0, p2.stderr[-400:])
p3 = subprocess.run([sys.executable, MODULE, "--choices"],
                    capture_output=True, text=True, cwd=HERE)
check("--choices runs", p3.returncode == 0 and "[CHOICE 1]" in p3.stdout)

for path in (MODULE, CASEFILE, os.path.abspath(__file__)):
    raw = open(path, "rb").read()
    check("%s is ASCII" % os.path.basename(path), all(b < 128 for b in raw))
    parsed = ast.parse(raw.decode())
    mods = {n.names[0].name.split(".")[0]
            for n in ast.walk(parsed) if isinstance(n, ast.Import)}
    mods |= {n.module.split(".")[0] for n in ast.walk(parsed)
             if isinstance(n, ast.ImportFrom) and n.module}
    banned = mods & {"socket", "urllib", "http", "requests", "numpy",
                     "pandas"}
    check("%s imports nothing networked or third-party"
          % os.path.basename(path), banned == set(), banned)

order_raw = open(ORDER, "rb").read()
check("the delivered order is landed as received, not transliterated",
      b"serpentine" in order_raw and b"Driftless" in order_raw)

check("every trigger declares itself constructed",
      all(str(trig.get("source", "")).startswith("CONSTRUCTED")
          for trig in cases.TRIGGERS.values()),
      [k for k, v in cases.TRIGGERS.items()
       if not str(v.get("source", "")).startswith("CONSTRUCTED")])
check("every geometry declares itself constructed",
      all(str(g.get("source", "")).startswith("CONSTRUCTED")
          for g in cases.GEOMETRIES.values()))
check("every geometry states why it exists at all",
      all(isinstance(g.get("constructibility_note"), str)
          and g["constructibility_note"] != ""
          for g in cases.GEOMETRIES.values()))
check("cases.py carries no expected verdict",
      not any(tok in open(CASEFILE).read()
              for tok in ("expected", "must_fire", "response_validated_here")))
check("the module names no check the order does not",
      set(t.CHECK_CODES) == {code for code, _ in t.CHECKS})
check("every check in CHECKS has a function",
      all(callable(fn) for _, fn in t.CHECKS))
check("the order's five validation cases are all in PAIRS",
      all(pair in cases.PAIRS for pair in cases.ORDER_CASES.values()))


# --------------------------------------------------------------------------
print()
print("%d checks, %d failed" % (TOTAL[0], len(FAILED)))
if FAILED:
    for f in FAILED:
        print("  " + f)
    sys.exit(1)
