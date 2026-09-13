# SPDX-License-Identifier: CC0-1.0
"""
test_valence.py -- the checks for valence_divergence.py.

No pytest, no network, stdlib only, runnable on a phone:

    python3 test_valence.py

EVERY EXPECTED VERDICT LIVES HERE AND NOT IN cases.py. A case that carries
its own answer agrees with the module by construction, and an agreement
produced that way measures nothing.

Sections, in the order the work order states them:

    1  the order's five validation cases, A through E
    2  the chain -- D2 and D3 are nested inside D1 by definition
    3  reachability: every declared value is reached by something
    4  absent is not a known negative: fired None vs fired []
    5  intake refuses rather than guesses
    6  no lexicon -- `term` reaches no check, measured from the AST
    7  no intent, no motive, no role, no rank -- identifier scan + plants
    8  glosses and citations carried verbatim, never parsed
    9  neither decoder is ranked
    10 nothing is averaged and no single valence is emitted
    11 branches are separate and unlinked
    12 the choices are declared
    13 housekeeping
"""

from __future__ import annotations

import ast
import itertools
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cases  # noqa: E402
import valence_divergence as v  # noqa: E402
from tools.authority_scan import (  # noqa: E402
    PLANT, scan, split_identifier)

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.join(HERE, "valence_divergence.py")
CASEFILE = os.path.join(HERE, "cases.py")
SRC = open(MODULE).read()
TREE = ast.parse(SRC)
BY_NAME = {n.name: n for n in ast.walk(TREE)
           if isinstance(n, ast.FunctionDef)}

CHECK_FNS = ("d1_divergent", "d2_unflagged", "d3_silent_pass",
             "d4_unchecked", "d5_orphan_candidate")

FAILED = []
TOTAL = [0]


def check(name, cond, detail=""):
    TOTAL[0] += 1
    if not cond:
        FAILED.append("%s %s" % (name, detail))
        print("FAIL  %s %s" % (name, detail))


def r(case_id):
    return v.read(cases.BY_ID[case_id])


def names_used(fn_node):
    """Every identifier and string constant a function's body touches."""
    out = set()
    for n in ast.walk(fn_node):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.add(n.value)
    return out


# --------------------------------------------------------------------------
print("1  the order's five validation cases")

# A -- hysteria, two branch entries. "MUST fire D1 and D5."
a1 = r("A1")
check("A1 fires D1", "D1_DIVERGENT" in a1["fired"], a1["fired"])
check("A1 fires D5", "D5_ORPHAN_CANDIDATE" in a1["fired"], a1["fired"])
check("A1 d5 basis is NEUTRAL at origin",
      a1["d5_basis"] == "NEUTRAL_AT_ORIGIN", a1["d5_basis"])

a2 = r("A2")
check("A2 is the 1939 branch and reads POS at B",
      a2["reading_B"]["valence"] == "POS")
check("A2 fires D1", "D1_DIVERGENT" in a2["fired"], a2["fired"])
check("A2 does not fire D5 -- B is not flat at origin on this branch",
      "D5_ORPHAN_CANDIDATE" not in a2["fired"], a2["fired"])
check("case A is two entries", len(cases.ORDER_CASES["A"]) == 2)
check("the two hysteria branches are separate records",
      a1["utterance_id"] != a2["utterance_id"])
check("neither branch was resolved to MIXED",
      a1["reading_B"]["valence"] != "MIXED"
      and a2["reading_B"]["valence"] != "MIXED")

# B -- the location set. Four entries, not one.
check("case B is four entries", len(cases.ORDER_CASES["B"]) == 4)
for cid in cases.ORDER_CASES["B"]:
    row = r(cid)
    check("B %s fires D1" % row["term"],
          "D1_DIVERGENT" in row["fired"], row["fired"])
    check("B %s fires D5" % row["term"],
          "D5_ORPHAN_CANDIDATE" in row["fired"], row["fired"])
check("the four B entries are four distinct terms",
      len({cases.BY_ID[c]["term"] for c in cases.ORDER_CASES["B"]}) == 4)

# C -- economy. THE REQUIRED NEGATIVE.
c = r("C_neutral")
check("C both read NEUTRAL",
      c["reading_A"]["valence"] == c["reading_B"]["valence"] == "NEUTRAL")
check("C logs clean -- nothing fires", c["fired"] == [], c["fired"])
check("C's empty fired list is a measurement, not an absence",
      c["fired"] is not None and c["grade"] == "LOGGED")
check("C's d5_basis is None because D5 did not fire",
      c["d5_basis"] is None)

cp = r("C_pos")
check("C's POS arm fires D1 -- the only condition D1 reads is difference",
      "D1_DIVERGENT" in cp["fired"], cp["fired"])

# D -- the falsifier. The only failure mode the instrument was built for.
d = r("D_silent")
for code in ("D1_DIVERGENT", "D2_UNFLAGGED", "D3_SILENT_PASS"):
    check("D falsifier fires %s" % code, code in d["fired"], d["fired"])

# E -- no false symmetry.
e = r("E_absent")
check("E fires D4 only", e["fired"] == ["D4_UNCHECKED"], e["fired"])
check("E does not fire D1 -- an unchecked history is not a divergence",
      "D1_DIVERGENT" not in e["fired"])

# The order fixes flagged_by and proceeded for D only. [CHOICE 9]: the MUST
# lists for A and B must hold under EVERY value of the two it leaves open,
# or the requirement is being met by a choice made here.
for cid in ("A1",) + cases.ORDER_CASES["B"]:
    eff = v.unstated_field_effect(cases.BY_ID[cid])
    check("%s: D1 and D5 hold under every unstated-field value" % cid,
          "D1_DIVERGENT" in eff["invariant"]
          and "D5_ORPHAN_CANDIDATE" in eff["invariant"], eff)
eff_a2 = v.unstated_field_effect(cases.BY_ID["A2"])
check("A2: D1 holds under every unstated-field value",
      "D1_DIVERGENT" in eff_a2["invariant"], eff_a2)
check("D2 and D3 on A and B are carried by the choice, not the case",
      set(v.unstated_field_effect(cases.BY_ID["B1"])["contingent"])
      == {"D2_UNFLAGGED", "D3_SILENT_PASS"})
check("case D is the one entry whose flags the order fixes",
      [c_ for c_ in cases.ENTRIES if c_.get("order_fixes_flags")]
      == [cases.BY_ID["D_silent"]])


# --------------------------------------------------------------------------
print("2  the chain")

LAT = v.reachable_fired_sets()

check("the lattice is a brute force, not a sample",
      LAT["combinations"] == (len(v.VALENCES) * len(v.A_SOURCES)
                              * len(v.VALENCES) * len(v.B_SOURCES)
                              * len(v.FLAGGED_BY) * 2),
      LAT["combinations"])
for s in LAT["sets"]:
    check("D2 never fires without D1 (%s)" % (s,),
          not ("D2_UNFLAGGED" in s and "D1_DIVERGENT" not in s))
    check("D3 never fires without D2 (%s)" % (s,),
          not ("D3_SILENT_PASS" in s and "D2_UNFLAGGED" not in s))

CO = v.co_firing()
check("D4 never co-fires with anything",
      CO["never_co_fires"] == ["D4_UNCHECKED"], CO["never_co_fires"])
check("D4 can fire alone", "D4_UNCHECKED" in CO["fires_alone"])
check("D5 can fire alone -- through UNREAD at origin, where D1 is blocked",
      "D5_ORPHAN_CANDIDATE" in CO["fires_alone"])
check("D1 can fire alone", "D1_DIVERGENT" in CO["fires_alone"])
check("the empty set is reachable -- an instrument that flags every term "
      "is a preference dressed as a method",
      () in LAT["sets"])


# --------------------------------------------------------------------------
print("3  reachability")

LOGGED = [v.read(e) for e in cases.ENTRIES
          if not any(v.intake(e))]

fired_in_cases = {code for row in LOGGED for code in row["fired"]}
for code in v.CHECK_CODES:
    check("check %s is reached by the case set" % code,
          code in fired_in_cases)

attribs = {row["decoder_attribution"] for row in LOGGED}
for a in v.ATTRIBUTION_VALUES:
    check("attribution %s is reached by the case set" % a, a in attribs)

bases = {row["d5_basis"] for row in LOGGED}
check("both d5 bases are reached",
      {"NEUTRAL_AT_ORIGIN", "UNREAD_AT_ORIGIN"} <= bases, bases)

grades = {v.read(e)["grade"] for e in cases.ENTRIES}
check("both grades are reached",
      grades == {"LOGGED", v.INTAKE_INCOMPLETE}, grades)

seen_a_val = {e["reading_A"]["valence"] for e in cases.ENTRIES
              if isinstance(e.get("reading_A"), dict)}
seen_b_val = {e["reading_B"]["valence"] for e in cases.ENTRIES
              if isinstance(e.get("reading_B"), dict)}
for val in v.VALENCES:
    check("valence %s appears in the case set" % val,
          val in (seen_a_val | seen_b_val), (seen_a_val, seen_b_val))
seen_b_src = {e["reading_B"]["source"] for e in cases.ENTRIES
              if isinstance(e.get("reading_B"), dict)}
for src in v.B_SOURCES:
    check("reading_B source %s appears in the case set" % src,
          src in seen_b_src, seen_b_src)
seen_a_src = {e["reading_A"]["source"] for e in cases.ENTRIES
              if isinstance(e.get("reading_A"), dict)}
for src in v.A_SOURCES:
    check("reading_A source %s appears in the case set" % src,
          src in seen_a_src, seen_a_src)
seen_flag = {e["flagged_by"] for e in cases.ENTRIES if "flagged_by" in e}
for f in v.FLAGGED_BY:
    check("flagged_by %s appears in the case set" % f, f in seen_flag,
          seen_flag)
seen_dem = {v.demonstrated_of(e) for e in cases.ENTRIES}
for dstate in v.DEMONSTRATED:
    check("demonstrated %s is reached (%s is the default)"
          % (dstate, "UNRECORDED"), dstate in seen_dem, seen_dem)

check("MIXED is reached as a SUPPLIED value",
      any(e["reading_A"]["valence"] == "MIXED" for e in cases.ENTRIES
          if isinstance(e.get("reading_A"), dict)))

# The ABSENT clause in D1's guard. [CHOICE 5].
ABS = v.absent_clause_is_live()
check("D1's ABSENT source clause changes some verdict", ABS["count"] > 0,
      ABS["count"])
check("every entry it changes is an ABSENT source carrying a valence",
      ABS["all_are_absent_with_a_valence"])
check("the case set carries one such entry, or the clause is untested here",
      any(e["reading_B"].get("source") == "ABSENT"
          and e["reading_B"].get("valence") != "UNREAD"
          for e in cases.ENTRIES if isinstance(e.get("reading_B"), dict)))


# --------------------------------------------------------------------------
print("4  absent is not a known negative")

for cid in ("X_missing", "X_invalid", "X_uncited"):
    row = r(cid)
    check("%s: grade is INTAKE_INCOMPLETE" % cid,
          row["grade"] == v.INTAKE_INCOMPLETE, row["grade"])
    check("%s: fired is None, not []" % cid, row["fired"] is None,
          row["fired"])
    check("%s: attribution is None, no decoder was scored" % cid,
          row["decoder_attribution"] is None)
    check("%s: something is named in missing or invalid" % cid,
          bool(row["missing"] or row["invalid"]))

check("a logged entry names nothing missing and nothing invalid",
      all(row["missing"] == [] and row["invalid"] == [] for row in LOGGED))
check("X_missing names the field, X_invalid names the value",
      "reading_B" in r("X_missing")["missing"]
      and r("X_invalid")["missing"] == []
      and len(r("X_invalid")["invalid"]) == 2,
      (r("X_missing")["missing"], r("X_invalid")["invalid"]))
check("X_uncited is invalid on citation AND date, not on either alone",
      len(r("X_uncited")["invalid"]) == 2, r("X_uncited")["invalid"])


# --------------------------------------------------------------------------
print("5  intake refuses rather than guesses")

GOOD = cases.BY_ID["A1"]
for field in v.TOP_FIELDS:
    probe = {k: val for k, val in GOOD.items() if k != field}
    row = v.read(probe)
    check("stripping %s refuses the entry" % field,
          row["grade"] == v.INTAKE_INCOMPLETE and row["fired"] is None,
          row["grade"])
    check("stripping %s names %s" % (field, field),
          field in row["missing"], row["missing"])

for sub in ("valence", "source", "gloss"):
    for side in ("reading_A", "reading_B"):
        probe = dict(GOOD)
        probe[side] = {k: val for k, val in GOOD[side].items() if k != sub}
        row = v.read(probe)
        check("stripping %s.%s refuses the entry" % (side, sub),
              row["grade"] == v.INTAKE_INCOMPLETE, row["grade"])
        check("stripping %s.%s names it" % (side, sub),
              "%s.%s" % (side, sub) in row["missing"], row["missing"])

check("a non-mapping entry is refused and does not raise",
      v.read("not an entry")["grade"] == v.INTAKE_INCOMPLETE)
check("an empty dict is refused",
      v.read({})["grade"] == v.INTAKE_INCOMPLETE)

# [CHOICE 4]. Citation is required for a cited source and optional otherwise.
for src in v.CITED_SOURCES:
    probe = dict(GOOD)
    probe["reading_B"] = dict(GOOD["reading_B"])
    probe["reading_B"]["source"] = src
    probe["reading_B"]["citation"] = ""
    check("empty citation is refused for source %s" % src,
          v.read(probe)["grade"] == v.INTAKE_INCOMPLETE)
for src in ("STATED", "ABSENT"):
    probe = dict(GOOD)
    probe["reading_B"] = {"valence": "NEUTRAL", "source": src, "gloss": ""}
    check("no citation is required for source %s" % src,
          v.read(probe)["grade"] == "LOGGED", v.read(probe)["invalid"])

# [CHOICE 5]. ABSENT carrying a valence is admitted, deliberately.
probe = dict(GOOD)
probe["reading_B"] = {"valence": "POS", "source": "ABSENT", "gloss": ""}
check("ABSENT with a valence is ADMITTED, not refused",
      v.read(probe)["grade"] == "LOGGED")
check("and it reads as D4, never as a divergence",
      v.read(probe)["fired"] == ["D4_UNCHECKED"], v.read(probe)["fired"])


# --------------------------------------------------------------------------
print("6  no lexicon -- the instrument never looks at the word")

for fn in CHECK_FNS + ("attribution", "d5_basis"):
    used = names_used(BY_NAME[fn])
    check("%s does not read `term`" % fn, "term" not in used, used)
    check("%s does not read `speaker`" % fn, "speaker" not in used, used)

# And behaviourally: the word can be anything at all.
for word in ("hysteria", "", "POSITIVE", "good", "\\u0000", "x" * 200):
    probe = dict(GOOD)
    probe["term"] = word or "x"
    check("the verdict does not move with the word (%r)" % word[:12],
          v.fired_codes(probe) == v.fired_codes(GOOD))

check("no module-level mapping from a word to a valence exists",
      not any(isinstance(n, ast.Dict)
              and any(isinstance(k, ast.Constant) and isinstance(k.value, str)
                      and str(el.value) in v.VALENCES
                      for k, el in zip(n.keys, n.values)
                      if isinstance(el, ast.Constant)
                      and isinstance(el.value, str) and isinstance(k, ast.Constant))
              for n in ast.walk(TREE)))


# --------------------------------------------------------------------------
print("7  no intent, no motive, no role, no rank")

FORBIDDEN_INTENT = ("intent", "intention", "motive", "motivation", "meant",
                    "meaning", "purpose", "malice", "deliberate", "willful",
                    "sincerity", "sincere", "belief", "believed", "blame",
                    "fault", "culpable")
# NOTE: every entry here must be a SINGLE token. `split_identifier` splits
# `citation_count` into ["citation", "count"], so a two-word vocabulary entry
# can never match anything -- it reads as coverage and is dead. The rule is
# asserted below rather than left as a comment.
FORBIDDEN_STANDING = ("credential", "title", "rank", "seniority",
                      "institution", "follower", "venue", "reach",
                      "authority", "reputation", "role", "status",
                      "expertise", "expert")
FORBIDDEN_RANKING = ("correct", "dominant", "primary", "preferred",
                     "authoritative", "truth", "right", "wrong", "better",
                     "worse", "winner", "score", "weight")

STANDING_PLANT = PLANT + "institution = 1\n"
INTENT_PLANT = ("def f(speaker_intent):\n"
                "    return {'motive': speaker_intent}\n")
RANK_PLANT = ("def f():\n"
              "    dominant_valence = 1\n"
              "    return {'correct_decoder': dominant_valence}\n")

for label, vocab, plant in (("intent", FORBIDDEN_INTENT, INTENT_PLANT),
                            ("standing", FORBIDDEN_STANDING, STANDING_PLANT),
                            ("ranking", FORBIDDEN_RANKING, RANK_PLANT)):
    for path, what in ((MODULE, "module"), (CASEFILE, "cases")):
        hits = scan(open(path).read(), vocab)
        check("no %s-class name in the %s" % (label, what), hits == [], hits)
    planted = scan(plant, vocab)
    check("the %s scan is not silent -- the plant is caught" % label,
          len(planted) >= 2, planted)

for label, vocab in (("intent", FORBIDDEN_INTENT),
                     ("standing", FORBIDDEN_STANDING),
                     ("ranking", FORBIDDEN_RANKING)):
    dead = [t for t in vocab if split_identifier(t) != [t]]
    check("no %s vocabulary entry is unmatchable by construction" % label,
          dead == [], dead)

check("`citation` survives the standing scan -- it is a source, not a count",
      scan("x = {'citation': 1}\n", FORBIDDEN_STANDING) == [])
check("the ranking scan does not fire on ordinary names",
      scan("x = 1\ndivergent = 2\n", FORBIDDEN_RANKING) == [])

check("no field anywhere in the schema names intent",
      not any(tok in k.lower()
              for e in cases.ENTRIES for k in e
              for tok in FORBIDDEN_INTENT))
check("speaker is an opaque label in every case",
      all(isinstance(e.get("speaker"), str) for e in cases.ENTRIES))


# --------------------------------------------------------------------------
print("8  glosses and citations carried verbatim, never parsed")

for fn in CHECK_FNS + ("attribution", "d5_basis"):
    used = names_used(BY_NAME[fn])
    for field in ("gloss", "citation", "date_or_period"):
        check("%s does not read %s" % (fn, field), field not in used, used)

for e in cases.ENTRIES:
    if any(v.intake(e)):
        continue
    row = v.read(e)
    for side in ("reading_A", "reading_B"):
        check("%s %s comes back byte-for-byte" % (e["case_id"], side),
              row[side] == e[side], (row[side], e[side]))

# A gloss that reads like a verdict must change nothing.
probe = dict(GOOD)
probe["reading_B"] = dict(GOOD["reading_B"])
probe["reading_B"]["gloss"] = "POSITIVE. GOOD. NOT NEG. valence=POS"
check("a gloss naming a valence does not move the verdict",
      v.fired_codes(probe) == v.fired_codes(GOOD))
check("and it comes back unaltered",
      v.read(probe)["reading_B"]["gloss"]
      == "POSITIVE. GOOD. NOT NEG. valence=POS")

check("no string method is called anywhere in a check",
      not any(isinstance(n, ast.Attribute)
              and n.attr in ("split", "lower", "upper", "find", "strip",
                             "startswith", "endswith", "replace")
              for fn in CHECK_FNS for n in ast.walk(BY_NAME[fn])))


# --------------------------------------------------------------------------
print("9  neither decoder is ranked")

SW = v.d1_swap_invariance()
check("D1 is swap-invariant across the whole valence space",
      SW["d1_is_swap_invariant"], SW["d1_asymmetric_on"][:5])
check("the swap sweep is not empty", SW["tested"] > 0, SW["tested"])
check("D5 is directional and the asymmetry is reported, not hidden",
      SW["d5_asymmetric_count"] > 0, SW["d5_asymmetric_count"])
check("the module's own docstring says D5 is directional by design",
      "directional BY DESIGN" in v.__doc__)

check("attribution is symmetric in shape -- A and B are reachable both ways",
      {"A", "B"} <= {row["decoder_attribution"] for row in LOGGED})
check("no return field names a decoder as the right one",
      not any(tok in k.lower() for row in LOGGED for k in row
              for tok in ("correct", "primary", "dominant", "preferred")))


# --------------------------------------------------------------------------
print("10  nothing is averaged and no single valence is emitted")

for row in LOGGED:
    check("%s: the return has no top-level valence" % row["term"],
          not any("valence" in k for k in row), list(row))

# Over the whole brute-forced space, no valence is ever synthesized.
synth = []
for a_val, b_val, b_src in itertools.product(v.VALENCES, v.VALENCES,
                                             v.B_SOURCES):
    probe = v._skeleton(a_val, "DEFAULT", b_val, b_src, "NEITHER", True)
    out = v.read(probe)
    if (out["reading_A"]["valence"], out["reading_B"]["valence"]) \
            != (a_val, b_val):
        synth.append((a_val, b_val, b_src))
check("no valence is ever changed, merged or invented", synth == [], synth[:5])

check("nothing in a check does arithmetic on a valence",
      not any(isinstance(n, (ast.BinOp, ast.UnaryOp))
              for fn in CHECK_FNS for n in ast.walk(BY_NAME[fn])))
check("no function is named for averaging or resolving",
      not any(tok in name.lower() for name in BY_NAME
              for tok in ("average", "mean", "merge", "resolve", "collapse",
                          "dominant")))
check("MIXED is never assigned by the module",
      not any(isinstance(n, ast.Constant) and n.value == "MIXED"
              for fn in list(CHECK_FNS) + ["read", "attribution", "d5_basis"]
              for n in ast.walk(BY_NAME[fn])))


# --------------------------------------------------------------------------
print("11  branches are separate and unlinked")

by_term = {}
for e in cases.ENTRIES:
    by_term.setdefault(e["term"], []).append(e)
multi = {t: es for t, es in by_term.items() if len(es) > 1}
check("the case set carries at least one term with two branches",
      bool(multi), list(multi))
check("no entry carries a field linking it to another entry",
      not any(tok in k.lower() for e in cases.ENTRIES for k in e
              for tok in ("branch_of", "parent", "group", "links",
                          "sibling", "cluster")))
for t, es in multi.items():
    outs = [v.read(e)["fired"] for e in es]
    check("%s: the branches are read independently" % t,
          all(v.read(e)["fired"] == o for e, o in zip(es, outs)))
check("hysteria's two branches do not produce one reading",
      r("A1")["fired"] != r("A2")["fired"])
check("economy's two arms do not produce one reading",
      r("C_neutral")["fired"] != r("C_pos")["fired"])


# --------------------------------------------------------------------------
print("12  the choices are declared")

txt = v.render_choices()
check("nine choices are declared", sorted(v.CHOICES) == list(range(1, 10)),
      sorted(v.CHOICES))
for n in v.CHOICES:
    check("[CHOICE %d] is printed" % n, "[CHOICE %d]" % n in txt)
    check("[CHOICE %d] is cited somewhere in the module" % n,
          "[CHOICE %d]" % n in SRC)
    check("[CHOICE %d] is not an empty gesture" % n,
          len(v.CHOICES[n]) > 80)
for add in v.SCHEMA_ADDITIONS:
    check("schema addition %r is named in the render" % add, add in txt)

sample = LOGGED[0]
for key in ("grade", "missing", "invalid", "d5_basis"):
    check("schema addition %s is a real return key" % key, key in sample)
for key in ("term", "utterance_id", "fired", "reading_A", "reading_B",
            "decoder_attribution"):
    check("the order's own return field %s is present" % key, key in sample)


# --------------------------------------------------------------------------
print("13  housekeeping")

p = subprocess.run([sys.executable, MODULE, "--selftest"],
                   cwd=HERE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
check("the module refuses --selftest with rc 2", p.returncode == 2,
      p.returncode)
check("and says where the checks live",
      b"test_valence.py" in p.stderr, p.stderr[:120])

p = subprocess.run([sys.executable, MODULE], cwd=HERE,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
check("the module runs clean as a script", p.returncode == 0,
      p.stderr[-400:])

for path in (MODULE, CASEFILE, os.path.abspath(__file__)):
    raw = open(path, "rb").read()
    check("%s is ASCII" % os.path.basename(path),
          all(b < 128 for b in raw))
    mods = {n.names[0].name.split(".")[0]
            for n in ast.walk(ast.parse(raw.decode()))
            if isinstance(n, ast.Import)}
    mods |= {n.module.split(".")[0]
             for n in ast.walk(ast.parse(raw.decode()))
             if isinstance(n, ast.ImportFrom) and n.module}
    banned = mods & {"socket", "urllib", "http", "requests", "numpy",
                     "pandas"}
    check("%s imports nothing networked or third-party"
          % os.path.basename(path), banned == set(), banned)

check("every case declares itself constructed",
      all(e["constructed_note"].startswith("CONSTRUCTED")
          for e in cases.ENTRIES),
      [e["case_id"] for e in cases.ENTRIES
       if not e["constructed_note"].startswith("CONSTRUCTED")])
check("every cited reading_B says where the claim came from",
      all(isinstance(e["reading_B"].get("citation"), str)
          and e["reading_B"]["citation"] != ""
          for e in cases.ENTRIES
          if isinstance(e.get("reading_B"), dict)
          and e["reading_B"].get("source") in v.CITED_SOURCES
          and e["case_id"] != "X_uncited"))
check("the module names no check the order does not",
      set(v.CHECK_CODES) == {c for c, _ in v.CHECKS})


# --------------------------------------------------------------------------
print()
print("%d checks, %d failed" % (TOTAL[0], len(FAILED)))
if FAILED:
    for f in FAILED:
        print("  " + f)
    sys.exit(1)
