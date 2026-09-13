# SPDX-License-Identifier: CC0-1.0
"""
Checks for return_path.py. Plain script, no pytest, no network.

    python3 test_return.py

Expected verdicts live HERE and not in cases.py, so no case can agree with
the module by construction. Exits 1 on any failure.
"""

from __future__ import annotations

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cases                                                   # noqa: E402
import return_path as rp                                       # noqa: E402
from tools.authority_scan import PLANT, scan                   # noqa: E402

FAILED = []
TOTAL = [0]


def check(name, condition, detail=""):
    TOTAL[0] += 1
    print("%-6s %s%s" % ("ok" if condition else "FAIL", name,
                         "" if condition else "   <- %s" % detail))
    if not condition:
        FAILED.append(name)


def read_by_id(channel_id):
    return rp.read(cases.BY_ID[channel_id])


print("== the order's five validation cases ==")

# A -- if the instrument cannot pass this, it passes nothing.
a = read_by_id("A_physical_consequence")
check("A returns RETURN_PATH_GRADED", a["grade"] == rp.GRADED, a["grade"])
check("A's failed set is empty", a["failed"] == [], a["failed"])

# B -- C1 only. Speed does not compensate for elective receipt.
b = read_by_id("B_incident_reporting")
check("B fails C1 and nothing else", b["failed"] == ["C1_RECEIPT"], b["failed"])
check("B is not graded despite a ratio of %.4g" % b["ratio"],
      b["grade"] == rp.NOT_A_RETURN_PATH, b["grade"])

# B's own name says a report is written, and a report is an encoding.
b_written = read_by_id("B_report_written")
check("B entered as a reporting system fails C1 and C2",
      set(b_written["failed"]) == {"C1_RECEIPT", "C2_SIGNAL"},
      b_written["failed"])
check("so the order's 'C1 ONLY' holds of the zero-encoding entry alone",
      set(b_written["failed"]) - set(b["failed"]) == {"C2_SIGNAL"})

# C -- C1 and C3 must fire, C4 must not.
c = read_by_id("C_publication_loop")
check("C fails C1", "C1_RECEIPT" in c["failed"], c["failed"])
check("C fails C3", "C3_LATENCY" in c["failed"], c["failed"])
check("C passes C4", "C4_CONSTRUCTION" not in c["failed"], c["failed"])

# D -- C1, C3, C4 in both variants; C2 is the axis the order leaves open.
d_yes = read_by_id("D_field_report_written")
d_no = read_by_id("D_field_no_report")
for label, got in (("D with a report", d_yes), ("D with none", d_no)):
    for code in ("C1_RECEIPT", "C3_LATENCY", "C4_CONSTRUCTION"):
        check("%s fails %s" % (label, code), code in got["failed"],
              got["failed"])
check("D's two variants differ on C2 and on nothing else",
      set(d_yes["failed"]) ^ set(d_no["failed"]) == {"C2_SIGNAL"},
      (d_yes["failed"], d_no["failed"]))

# E -- the falsifier. Must not pass.
e = read_by_id("E_fast_side_writes")
check("E fails C2", "C2_SIGNAL" in e["failed"], e["failed"])
check("E raises F_FAST_SIDE_ENCODER",
      "F_FAST_SIDE_ENCODER" in e["flags"], e["flags"])
check("E is not graded", e["grade"] == rp.NOT_A_RETURN_PATH, e["grade"])
check("E is ideal on the other three",
      set(e["failed"]) == {"C2_SIGNAL"}, e["failed"])

print()
print("== the grade rule ==")

# `grade` is RETURN_PATH_GRADED if and only if `failed` is empty.
biconditional = True
for ch in cases.CASES:
    r = rp.read(ch)
    if r["failed"] is None:
        biconditional = biconditional and r["grade"] == rp.INTAKE_INCOMPLETE
        continue
    biconditional = biconditional and (
        (r["grade"] == rp.GRADED) == (r["failed"] == []))
check("graded iff failed is empty, across every case", biconditional)
check("no case returns GRADED with a non-empty failed set",
      all(rp.read(ch)["grade"] != rp.GRADED or rp.read(ch)["failed"] == []
          for ch in cases.CASES))

print()
print("== no scalar collapse ==")

# There is no function returning one number that stands in for the set.
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "return_path.py")).read()
tree = ast.parse(src)
sums = [n for n in ast.walk(tree)
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        and n.func.id in ("sum", "len")
        and any(isinstance(a, ast.Name) and a.id == "failed" for a in n.args)]
check("nothing sums or counts the failed set", not sums, sums)
check("read() returns the set, not a count",
      isinstance(rp.read(cases.BY_ID["C_publication_loop"])["failed"], list))

print()
print("== independence of the four checks ==")

ind = rp.independence()
check("baseline fires nothing", ind["baseline_failed"] == [],
      ind["baseline_failed"])
for row in ind["rows"]:
    check("flipping %s moves only %s" % (row["flipped"], row["flipped"]),
          row["isolated"], row["failed"])
check("all four isolated", ind["all_isolated"])

# CHECK_FIELDS is a table and a table can drift from the functions it
# describes. Read each check's body and assert it touches its own fields
# and no other intake field.
by_name = {n.name: n for n in ast.walk(tree)
           if isinstance(n, ast.FunctionDef)}
fn_of = {"C1_RECEIPT": "c1_receipt", "C2_SIGNAL": "c2_signal",
         "C3_LATENCY": "c3_latency", "C4_CONSTRUCTION": "c4_construction"}
for code, fname in fn_of.items():
    body = by_name[fname]
    touched = {n.value for n in ast.walk(body)
               if isinstance(n, ast.Constant) and isinstance(n.value, str)
               and n.value in rp.REQUIRED_FIELDS}
    check("%s reads exactly %s" % (code, ",".join(rp.CHECK_FIELDS[code])),
          touched == set(rp.CHECK_FIELDS[code]), touched)

print()
print("== every declared state is reachable ==")

grades = {rp.read(ch)["grade"] for ch in cases.CASES}
for g in (rp.GRADED, rp.NOT_A_RETURN_PATH, rp.INTAKE_INCOMPLETE):
    check("grade %s reachable" % g, g in grades)

fired_checks = set()
fired_flags = set()
ratio_states = set()
for ch in cases.CASES:
    r = rp.read(ch)
    fired_checks.update(r["failed"] or [])
    fired_flags.update(r["flags"] or [])
    ratio_states.add(r["ratio_state"])
for code in rp.CHECK_CODES:
    check("check %s fires on some case" % code, code in fired_checks)
for code in rp.FLAG_CODES:
    check("flag %s fires on some case" % code, code in fired_flags)
for state in (rp.RATIO_COMPUTED, rp.RATIO_UNDEFINED, rp.RATIO_NOT_COMPUTED):
    check("ratio state %s reachable" % state, state in ratio_states)

print()
print("== intake refuses rather than guesses ==")

g = read_by_id("G_build_on_time_absent")
check("an absent field returns INTAKE_INCOMPLETE",
      g["grade"] == rp.INTAKE_INCOMPLETE, g["grade"])
check("and names the field", g["missing"] == ["build_on_time"], g["missing"])
check("no check ran, so failed is None and not []",
      g["failed"] is None, g["failed"])
check("flags is None for the same reason", g["flags"] is None, g["flags"])

i = read_by_id("I_receipt_out_of_vocabulary")
check("an out-of-vocabulary value is invalid, not missing",
      i["missing"] == [] and len(i["invalid"]) == 1, (i["missing"], i["invalid"]))
check("it is not scored as ELECTIVE", i["grade"] == rp.INTAKE_INCOMPLETE)

j = read_by_id("J_encoder_none_above_zero")
check("encoder NONE above zero encodings is refused",
      j["grade"] == rp.INTAKE_INCOMPLETE and
      any("encoder_position" in s for s in j["invalid"]), j["invalid"])

for field in rp.REQUIRED_FIELDS:
    stripped = dict(cases.BY_ID["A_physical_consequence"])
    del stripped[field]
    r = rp.read(stripped)
    check("absent %s blocks the read" % field,
          r["grade"] == rp.INTAKE_INCOMPLETE and field in r["missing"],
          (r["grade"], r["missing"]))

check("a non-mapping is refused rather than raising",
      rp.read("not a channel")["grade"] == rp.INTAKE_INCOMPLETE)
check("an empty scope_note is a supplied value",
      rp.read(dict(cases.BY_ID["A_physical_consequence"],
                   scope_note=""))["grade"] == rp.GRADED)

print()
print("== ratio ==")

check("ratio is None where there is no denominator",
      rp.ratio(1.0, 0.0) is None)
h = read_by_id("H_build_on_time_zero")
check("and the state names why", h["ratio_state"] == rp.RATIO_UNDEFINED,
      h["ratio_state"])
check("C3 still decides where the ratio does not exist",
      h["failed"] == ["C3_LATENCY"], h["failed"])
check("ratio None from intake is a different state",
      g["ratio_state"] == rp.RATIO_NOT_COMPUTED, g["ratio_state"])
check("F_RATIO is not emitted as a flag",
      all("F_RATIO" not in (rp.read(ch)["flags"] or []) for ch in cases.CASES))

print()
print("== hard constraints ==")

FORBIDDEN = {
    "institution", "institutional", "authority", "authoritative",
    "credential", "credentials", "venue", "reach", "audience",
    "reputation", "reputational", "prestige", "standing", "rank",
    "ranking", "ranked", "seniority", "citation", "citations",
}
for path in ("return_path.py", "cases.py"):
    hits = scan(open(path).read(), FORBIDDEN)
    check("no banned field name in %s" % path, not hits,
          "found %s" % hits if hits else "")
check("the scanner fires on a plant", len(scan(PLANT, {"citation", "rank"})) >= 2)

# scope_note is carried and never parsed: no check function mentions it,
# and no comparison anywhere in the module reads it.
scope_readers = set()
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        for sub in ast.walk(node):
            if isinstance(sub, ast.Constant) and sub.value == "scope_note":
                scope_readers.add(node.name)
check("scope_note is touched only by intake and read",
      scope_readers <= {"intake", "read"}, scope_readers)
compares = [n for n in ast.walk(tree)
            if isinstance(n, ast.Compare)
            and any(isinstance(s, ast.Constant) and s.value == "scope_note"
                    for s in ast.walk(n))]
check("exactly one comparison in the module names scope_note",
      len(compares) == 1, len(compares))
check("and it is the presence test, not a read of the text",
      compares and all(isinstance(op, ast.In) for op in compares[0].ops),
      [type(op).__name__ for op in compares[0].ops] if compares else None)
# no branch inside read() is taken on the note's content.
read_branches = [n.lineno for n in ast.walk(by_name["read"])
                 if isinstance(n, (ast.If, ast.IfExp))
                 and any(isinstance(s, ast.Constant) and s.value == "scope_note"
                         for s in ast.walk(n.test))]
check("no branch inside read() is taken on scope_note",
      not read_branches, read_branches)
check("scope_note is carried through byte-for-byte",
      all(rp.read(ch)["scope_note"] == ch.get("scope_note")
          for ch in cases.CASES))

check("no 'fast' or 'slow' value stands in for a time",
      "FAST" not in rp.RECEIPT_VALUES and "SLOW" not in rp.RECEIPT_VALUES
      and not any(v in ("FAST", "SLOW") for v in rp.CONSTRUCTION_VALUES))
check("both times or no rating: neither has a default",
      "latency" in rp.REQUIRED_FIELDS and
      "build_on_time" in rp.REQUIRED_FIELDS)
check("the module converts no time",
      not any(isinstance(n, ast.Name) and n.id in ("timedelta", "strptime")
              for n in ast.walk(tree)))

print()
print("== properties the order states in prose, measured here ==")

enc = rp.encoder_reaches_no_check()
check("encoder_position moves no check verdict",
      not enc["encoder_moves_failed"], enc["failed_sets_at_one_encoding"])
fal = rp.falsifier_e_carried_by()
check("case E fails C2 with any encoder, so C2 carries the falsifier alone",
      fal["all_fail_c2"], fal["rows"])
check("and only FAST_SIDE raises the flag",
      fal["only_fast_side_flags"] == ["FAST_SIDE"], fal["only_fast_side_flags"])

# the conjunction rule is what makes E unable to pass, not the flag.
ideal_but_encoded = dict(rp._IDEAL, signal_encodings=1,
                         encoder_position="SLOW_SIDE")
check("ideal values on three checks do not carry a fired fourth to a pass",
      rp.read(ideal_but_encoded)["grade"] == rp.NOT_A_RETURN_PATH)

print()
print("== choices are declared, not silent ==")

check("every choice is numbered and non-empty",
      all(isinstance(n, int) and CH for n, CH in rp.CHOICES.items()))
rendered = rp.render_choices()
for n in rp.CHOICES:
    check("CHOICE %d appears in the header" % n, "[CHOICE %d]" % n in rendered)
check("the schema additions are listed",
      all(a in rendered for a in rp.SCHEMA_ADDITIONS))

print()
print("%d checks, %d failed" % (TOTAL[0], len(FAILED)))
if FAILED:
    print("failed: %s" % FAILED)
    sys.exit(1)
