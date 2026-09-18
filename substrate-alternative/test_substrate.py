#!/usr/bin/env python3
"""Checks for frame_audit.py and pilot_loop.py.

This file IS the known-answer harness for the folder.  There is
no shared registry to import: substrate-alternative is meant to
stand as its own repository, so the AST scan below is local
rather than imported.  That is a copy, and a copy drifts; the
cost is stated in CLAIM_TABLE.md rather than hidden.

Every classifier state is shown reachable on a constructed input
before it is trusted, and every screen is planted against before
its silence is quoted.  No pytest.  Standard library only.
"""

import ast
import os
import subprocess
import sys

import frame_audit
import pilot_loop
from pilot_loop import Capacity, Need, Node

HERE = os.path.dirname(os.path.abspath(__file__))
CHECKS = []


def check(label, got, want):
    CHECKS.append((label, got == want, got, want))


def check_true(label, got):
    check(label, bool(got), True)


def raises(label, exc, fn, *a, **kw):
    try:
        fn(*a, **kw)
    except exc:
        CHECKS.append((label, True, "raised", "raised"))
        return
    except Exception as other:  # pragma: no cover - a wrong raise
        CHECKS.append((label, False, repr(other), exc.__name__))
        return
    CHECKS.append((label, False, "no raise", exc.__name__))


# ---- an AST identifier scan, local by necessity -------------------

def identifiers(path):
    with open(path) as handle:
        tree = ast.parse(handle.read())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.arg):
            names.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.keyword) and node.arg:
            names.add(node.arg)
        elif isinstance(node, ast.Dict):
            for key in node.keys:
                if isinstance(key, ast.Constant) and \
                        isinstance(key.value, str):
                    names.add(key.value)
    return names


def tokens(names):
    out = set()
    for name in names:
        piece = ""
        for ch in name:
            if ch == "_":
                if piece:
                    out.add(piece.lower())
                piece = ""
            elif ch.isupper() and piece and not piece[-1].isupper():
                out.add(piece.lower())
                piece = ch
            else:
                piece += ch
        if piece:
            out.add(piece.lower())
    return out


def scan(path, vocabulary):
    return sorted(tokens(identifiers(path)) & set(vocabulary))


PROPOSAL_VOCAB = (
    "suggest", "suggestion", "suggested", "replace", "replacement",
    "instead", "alternative", "rewrite", "recommend",
    "recommendation", "improve", "improvement", "fix", "better",
    "prefer", "preferred", "should",
)

RANKING_VOCAB = (
    "rank", "ranking", "ranked", "score", "scored", "best", "top",
    "winner", "leaderboard", "priority", "weight", "merit",
    "standing",
)

NETWORK_VOCAB = (
    "socket", "urllib", "http", "requests", "subprocess", "ftplib",
    "telnetlib", "smtplib",
)


def imported(path):
    with open(path) as handle:
        tree = ast.parse(handle.read())
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                mods.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module.split(".")[0])
    return mods


# =================================================================
# 1.  frame_audit -- the registry
# =================================================================

reg = frame_audit.load_registry()
check("1.1 registry loads", len(reg) > 120, True)
check("1.2 every entry carries a declared frame",
      sorted({f for f, _ in reg.values()}) == sorted(frame_audit.FRAMES),
      True)
raises("1.3 duplicate surface refused [CHOICE 5]",
       frame_audit.RegistryError, frame_audit.load_registry,
       (("cost", "PRICE", None), ("cost", "TRANSACTION", None)))
raises("1.4 unknown frame refused", frame_audit.RegistryError,
       frame_audit.load_registry, (("x", "NOT_A_FRAME", None),))
raises("1.5 empty surface refused", frame_audit.RegistryError,
       frame_audit.load_registry, (("   ", "PRICE", None),))

# The two counts the README and the claim table state.  Pinned
# here so the prose cannot drift from the registry -- a first
# draft said 23 where the registry holds 32.
check("1.6 registry size as stated in the README", len(reg), 165)
check("1.7 entries carrying a second live sense",
      sum(1 for _, amb in reg.values() if amb), 32)
for name in ("README.md", "CLAIM_TABLE.md"):
    with open(os.path.join(HERE, name)) as handle:
        prose = handle.read()
    check("1.8 %s states 165" % name, "165" in prose, True)

# =================================================================
# 2.  word boundary, never substring
# =================================================================

r = frame_audit.audit("The supermarket is downtown and well known.")
check("2.1 `supermarket` does not fire `market`", r["hits_n"], 0)
check("2.2 `downtown` and `known` do not fire `own`", r["hits_n"], 0)
r = frame_audit.audit("The market is open.")
check("2.3 bare `market` does fire", r["hits_n"], 1)
check("2.4 and lands in TRANSACTION",
      r["hits"][0].frame, "TRANSACTION")

# =================================================================
# 3.  every declared frame reachable; zeros are visible
# =================================================================

ONE_EACH = ("The owner signed the deed. "
            "The fee was a dollar. "
            "They bought it from a vendor. "
            "There is a shortage and rationing. "
            "The valuation was priceless.")
r = frame_audit.audit(ONE_EACH)
for frame in frame_audit.FRAMES:
    check_true("3.%s reachable: %s" % (frame[0], frame),
               r["counts"][frame] > 0)
check("3.z counts carry every frame as a key",
      sorted(r["counts"]), sorted(frame_audit.FRAMES))

CLEAN = ("The river rose two metres overnight. "
         "Nobody had a boat. "
         "The road was under water by dawn.")
r = frame_audit.audit(CLEAN)
check("3.n reachable negative: a text with no hits", r["hits_n"], 0)
check("3.n2 and its frames are visible zeros",
      sorted(r["counts"]) == sorted(frame_audit.FRAMES)
      and set(r["counts"].values()) == {0}, True)
check("3.n3 sentences are still counted", r["sentences_n"], 3)

r = frame_audit.audit("")
check("3.e empty text: no sentences", r["sentences_n"], 0)
check("3.e2 empty text: no hits", r["hits_n"], 0)
check("3.e3 empty text: frames still present",
      sorted(r["counts"]), sorted(frame_audit.FRAMES))

# =================================================================
# 4.  sense-ambiguity is a third state, counted apart
# =================================================================

AMB = ("The absolute value is a property of the system. "
       "Ecological competition was measured.")
r = frame_audit.audit(AMB)
check_true("4.1 ambiguous-only text produces hits", r["hits_n"] > 0)
check("4.2 none of them is unambiguous",
      set(r["counts_unambiguous"].values()), {0})
check("4.3 all of them are ambiguous",
      r["ambiguous_n"], r["hits_n"])
check("4.4 every ambiguous hit states its other sense",
      all(h.ambiguity_reason for h in r["hits"] if h.sense_ambiguous),
      True)
r = frame_audit.audit(ONE_EACH + " " + AMB)
check("4.5 total = unambiguous + ambiguous, per frame",
      all(r["counts"][f] == r["counts_unambiguous"][f]
          + r["counts_ambiguous"][f] for f in frame_audit.FRAMES),
      True)
check("4.6 a mixed text reaches both states",
      min(r["ambiguous_n"], r["hits_n"] - r["ambiguous_n"]) > 0, True)

# =================================================================
# 4b.  THE LIMIT, measured rather than asserted
# =================================================================
#
# The module docstring says a paraphrase steps around the list.
# These two sentences carry the same frame.  One is caught and
# one is not, and the difference is vocabulary, not frame.

check("4b.1 the plain form is caught",
      frame_audit.audit("You have to pay for it.")["hits_n"], 1)
check("4b.2 the paraphrase is not",
      frame_audit.audit(
          "It takes something from you before you may have it."
      )["hits_n"], 0)
check("4b.3 inflections are not generated: `compete` is listed",
      frame_audit.audit("They compete.")["hits_n"], 1)
check("4b.4 and `competing` is therefore missed",
      frame_audit.audit("They are competing.")["hits_n"], 0)

# =================================================================
# 5.  longest match wins  [CHOICE 1]
# =================================================================

r = frame_audit.audit("It was cost-effective.")
check("5.1 `cost-effective` is one hit", r["hits_n"], 1)
check("5.2 filed under VALUE_AS_PRICE, not PRICE",
      r["hits"][0].frame, "VALUE_AS_PRICE")
r = frame_audit.audit("Supply and demand did the rest.")
check("5.3 `supply and demand` is one hit", r["hits_n"], 1)
check("5.4 filed under SCARCITY_AS_GIVEN [CHOICE 3]",
      r["hits"][0].frame, "SCARCITY_AS_GIVEN")
r = frame_audit.audit("supply\nand   demand")
check("5.5 a phrase matches across whitespace", r["hits_n"], 1)

# =================================================================
# 6.  sentence index  [CHOICE 2]
# =================================================================

r = frame_audit.audit("No hits here. The price was high. Nor here.")
check("6.1 one hit", r["hits_n"], 1)
check("6.2 in sentence 1", r["hits"][0].sentence_index, 1)
check("6.3 sentences counted", r["sentences_n"], 3)
check("6.4 the sentence text is carried",
      r["hits"][0].sentence, "The price was high.")
check("6.5 char span points at the token",
      "No hits here. The price was high. Nor here."
      [r["hits"][0].char_start:r["hits"][0].char_end], "price")

# =================================================================
# 7.  LOCATE ONLY, enforced structurally
# =================================================================

hits = scan(os.path.join(HERE, "frame_audit.py"), PROPOSAL_VOCAB)
check("7.1 no proposal identifier in frame_audit.py", hits, [])
check("7.2 no return field could carry one",
      sorted(set(frame_audit.Hit._fields) & set(PROPOSAL_VOCAB)), [])

PLANT = os.path.join(HERE, "_plant_tmp.py")
with open(PLANT, "w") as handle:
    handle.write("def suggestion(x):\n    return x\n")
try:
    check("7.3 the scan is not silent: a plant fires",
          scan(PLANT, PROPOSAL_VOCAB), ["suggestion"])
finally:
    os.remove(PLANT)

# =================================================================
# 8.  pilot_loop -- scenario reading refuses rather than repairs
# =================================================================

def scen(**kw):
    base = {"nodes": [Node("a", ""), Node("b", "")],
            "capacities": [Capacity("a", "food", 10, 0)],
            "needs": [Need("b", "food", 5, 0, 5)],
            "routes": {("a", "b"): 1}}
    base.update(kw)
    return base


raises("8.1 duplicate node id", pilot_loop.ScenarioError,
       pilot_loop.run, scen(nodes=[Node("a", ""), Node("a", "")]))
raises("8.2 capacity at an undeclared node",
       pilot_loop.ScenarioError, pilot_loop.run,
       scen(capacities=[Capacity("zz", "food", 1, 0)]))
raises("8.3 need at an undeclared node", pilot_loop.ScenarioError,
       pilot_loop.run, scen(needs=[Need("zz", "food", 1, 0, 5)]))
raises("8.4 non-positive need", pilot_loop.ScenarioError,
       pilot_loop.run, scen(needs=[Need("b", "food", 0, 0, 5)]))
raises("8.5 horizon before declaration", pilot_loop.ScenarioError,
       pilot_loop.run, scen(needs=[Need("b", "food", 1, 4, 2)]))
raises("8.6 route over an undeclared node",
       pilot_loop.ScenarioError, pilot_loop.run,
       scen(routes={("a", "zz"): 1}))

# =================================================================
# 9.  travel: an undeclared route is None  [CHOICE 4]
# =================================================================

routes = {("a", "b"): 3}
check("9.1 declared route", pilot_loop.travel(routes, "a", "b"), 3)
check("9.2 symmetric fallback",
      pilot_loop.travel(routes, "b", "a"), 3)
check("9.3 symmetric off -> None",
      pilot_loop.travel(routes, "b", "a", symmetric=False), None)
check("9.4 undeclared pair -> None, not a large number",
      pilot_loop.travel(routes, "a", "q"), None)
check("9.5 a node reaches itself at zero",
      pilot_loop.travel(routes, "a", "a"), 0)

# =================================================================
# 10.  all four UNMET reasons reachable
# =================================================================

def reasons(scenario):
    return sorted({u.reason for u in pilot_loop.run(scenario)["unmet"]})


s_none = {"nodes": [Node("a", ""), Node("b", "")],
          "capacities": [Capacity("a", "staples", 10, 0)],
          "needs": [Need("b", "produce", 5, 0, 5)],
          "routes": {("a", "b"): 1}}
check("10.1 NO_CAPACITY_DECLARED reachable",
      reasons(s_none), ["NO_CAPACITY_DECLARED"])

s_exh = {"nodes": [Node("a", ""), Node("b", ""), Node("c", "")],
         "capacities": [Capacity("a", "staples", 6, 0)],
         "needs": [Need("b", "staples", 5, 0, 5),
                   Need("c", "staples", 5, 0, 5)],
         "routes": {("a", "b"): 1, ("a", "c"): 1}}
check("10.2 CAPACITY_EXHAUSTED reachable",
      reasons(s_exh), ["CAPACITY_EXHAUSTED"])

s_unr = {"nodes": [Node("a", ""), Node("b", "")],
         "capacities": [Capacity("a", "staples", 10, 0)],
         "needs": [Need("b", "staples", 5, 0, 5)],
         "routes": {}}
check("10.3 UNREACHABLE reachable", reasons(s_unr), ["UNREACHABLE"])

s_late = {"nodes": [Node("a", ""), Node("b", "")],
          "capacities": [Capacity("a", "staples", 10, 0)],
          "needs": [Need("b", "staples", 5, 0, 2)],
          "routes": {("a", "b"): 9}}
check("10.4 ARRIVES_AFTER_HORIZON reachable",
      reasons(s_late), ["ARRIVES_AFTER_HORIZON"])

seen = set()
for s in (s_none, s_exh, s_unr, s_late, pilot_loop.DEMO):
    seen.update(reasons(s))
check("10.5 no declared reason is unreachable",
      sorted(seen) == sorted(pilot_loop.UNMET_REASONS), True)

s_ok = {"nodes": [Node("a", ""), Node("b", "")],
        "capacities": [Capacity("a", "staples", 10, 0)],
        "needs": [Need("b", "staples", 5, 0, 5)],
        "routes": {("a", "b"): 1}}
res = pilot_loop.run(s_ok)
check("10.6 reachable negative: nothing unmet", res["unmet"], [])
check("10.7 and something was matched", len(res["allocations"]), 1)

# =================================================================
# 11.  UNMET is a return type, and a partial fill returns both
# =================================================================

s_part = {"nodes": [Node("a", ""), Node("b", "")],
          "capacities": [Capacity("a", "staples", 4, 0)],
          "needs": [Need("b", "staples", 10, 0, 5)],
          "routes": {("a", "b"): 1}}
res = pilot_loop.run(s_part)
check("11.1 a partial fill logs an allocation",
      [(a.to_node, a.quantity) for a in res["allocations"]],
      [("b", 4)])
check("11.2 and an UNMET for the remainder",
      [(u.node, u.quantity, u.reason) for u in res["unmet"]],
      [("b", 6, "CAPACITY_EXHAUSTED")])
check("11.3 UNMET is a value, not an exception",
      isinstance(res["unmet"][0], pilot_loop.UNMET), True)
check("11.4 and not an exception type",
      isinstance(res["unmet"][0], BaseException), False)
check("11.5 its fields are the four declared",
      list(pilot_loop.UNMET._fields),
      ["node", "resource", "quantity", "reason"])

# =================================================================
# 12.  lag: known answers on the demo  [CHOICE 5] [CHOICE 6]
# =================================================================
#
# Basis, computed by hand from the demo scenario:
#   kitchen_b has the earliest horizon (2), so it is served first
#   [CHOICE 2].  depot_north -> kitchen_b is 2 cycles, depot_north
#   is ready at 0, the need was declared at 0, so arrival is 2 and
#   lag is 2.  kitchen_a (horizon 3) then draws 20 from the 20
#   left at depot_north at 1 cycle -> lag 1, and 10 from
#   depot_south, which is not ready until cycle 2, so departure is
#   2, arrival 3, lag 3.  15 staples remain at depot_south.

res = pilot_loop.run(pilot_loop.DEMO)
check("12.1 three allocations", len(res["allocations"]), 3)
check("12.2 lags are 2, 1, 3",
      [a.lag for a in res["allocations"]], [2, 1, 3])
check("12.3 ready_cycle delays departure [CHOICE 5]",
      [a.depart_cycle for a in res["allocations"]], [0, 0, 2])
check("12.4 capacity left",
      res["capacity_left"], [("depot_south", "staples", 15)])
check("12.5 two needs unfilled",
      sorted((u.node, u.reason) for u in res["unmet"]),
      [("kitchen_c", "UNREACHABLE"),
       ("kitchen_d", "NO_CAPACITY_DECLARED")])
per = res["per_node"]
check("12.6 kitchen_a lags", per["kitchen_a"]["staples"]["lags"],
      [1, 3])
check("12.7 kitchen_a max lag", per["kitchen_a"]["staples"]["max_lag"],
      3)
check("12.8 an unserved node has max_lag None, not 0",
      per["kitchen_c"]["staples"]["max_lag"], None)
check("12.9 and no lags, not a zero lag",
      per["kitchen_c"]["staples"]["lags"], [])
check("12.10 needed is carried even where nothing moved",
      per["kitchen_d"]["produce"]["needed"], 15)

# =================================================================
# 13.  no composite, no ranking  [CHOICE 7]
# =================================================================

cell = per["kitchen_a"]["staples"]
check("13.1 per-node cell keys are the seven declared",
      sorted(cell),
      ["lags", "max_lag", "met", "min_lag", "needed", "unfilled"])
check("13.2 no ranking identifier in pilot_loop.py",
      scan(os.path.join(HERE, "pilot_loop.py"), RANKING_VOCAB), [])
with open(PLANT, "w") as handle:
    handle.write("rank_score = 1\n")
try:
    check("13.3 the ranking scan is not silent",
          scan(PLANT, RANKING_VOCAB), ["rank", "score"])
finally:
    os.remove(PLANT)
check("13.4 the run carries no total across nodes",
      sorted(res) == sorted(["allocations", "unmet", "per_node",
                             "capacity_left", "unmet_reasons",
                             "choices"]), True)

# =================================================================
# 14.  determinism
# =================================================================

check("14.1 no randomness imported",
      "random" in pilot_loop.__dict__ or
      "random" in imported(os.path.join(HERE, "pilot_loop.py")),
      False)
a = pilot_loop.render(pilot_loop.run(pilot_loop.DEMO))
b = pilot_loop.render(pilot_loop.run(pilot_loop.DEMO))
check("14.2 two runs are identical", a, b)

# =================================================================
# 15.  the screen, in three arms
# =================================================================

path = os.path.join(HERE, "pilot_loop.py")
with open(path) as handle:
    source = handle.read()
lines = source.split("\n")
regions = pilot_loop._regions(lines)
check("15.0 exactly one exempt region", len(regions), 1)

masked = []
for i, line in enumerate(lines):
    inside = any(a <= i <= b for a, b, _ in regions)
    masked.append("" if inside else line)
arm_a = pilot_loop.screen("\n".join(masked), ())
check("15.1 arm A -- masked, the file is clean",
      arm_a["unexempted"], [])
check("15.1b arm A -- and nothing at all fires",
      sum(arm_a["counts"].values()), 0)

arm_b = pilot_loop.screen(source, regions)
check("15.2 arm B -- unmasked, nothing outside the region fires",
      arm_b["unexempted"], [])
check("15.2b arm B -- the region is what fires",
      sorted({h.entry for _, h, _ in arm_b["exempted"]}),
      ["compensation", "cost", "finance", "procurement"])
check("15.2c arm B -- every one is an ICS section or unit name",
      len(arm_b["exempted"]), 5)

planted = source.replace(
    "UNMET_REASONS = (",
    "# planted for the null test: profit margin\n"
    "UNMET_REASONS = (", 1)
arm_c = pilot_loop.screen(planted, pilot_loop._regions(
    planted.split("\n")))
check("15.3 arm C -- a plant outside the region is caught",
      sorted({h.entry for _, h in arm_c["unexempted"]}),
      ["margin", "profit"])
check("15.3b arm C -- and the screen flags", arm_c["flagged"], True)

check("15.4 the rendered run is clean",
      pilot_loop.screen_output(a)["unexempted"], [])
check("15.5 screen_self agrees with arm B",
      pilot_loop.screen_self()["flagged"], False)

# =================================================================
# 16.  refusals, choices, ascii, no network
# =================================================================

for name in ("frame_audit.py", "pilot_loop.py"):
    out = subprocess.run(
        [sys.executable, os.path.join(HERE, name), "--selftest"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    check("16.%s refuses --selftest with exit 2" % name,
          out.returncode, 2)
    check("16.%s names the suite to run instead" % name,
          b"test_substrate.py" in out.stderr, True)

for module, name in ((frame_audit, "frame_audit.py"),
                     (pilot_loop, "pilot_loop.py")):
    with open(os.path.join(HERE, name)) as handle:
        text = handle.read()
    report = module.choices_report()
    for n in module.CHOICES:
        check("16.%s [CHOICE %d] printed" % (name, n),
              "[CHOICE %d]" % n in report, True)
        check("16.%s [CHOICE %d] cited inline" % (name, n),
              "[CHOICE %d]" % n in text, True)
    check("16.%s is ascii" % name, text.encode("ascii") and True, True)
    check("16.%s no network module imported" % name,
          sorted(imported(os.path.join(HERE, name))
                 & set(NETWORK_VOCAB)), [])

check("16.import pilot_loop imports frame_audit rather than "
      "copying it",
      "frame_audit" in imported(os.path.join(HERE, "pilot_loop.py")),
      True)

# =================================================================

failed = [c for c in CHECKS if not c[1]]
for label, ok, got, want in CHECKS:
    if not ok:
        print("FAIL  %-58s got %r want %r" % (label, got, want))
print("checks: %d   failed: %d" % (len(CHECKS), len(failed)))
sys.exit(1 if failed else 0)
