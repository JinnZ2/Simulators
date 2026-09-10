#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Checks for probe.py. Every run record and every fixture construction
here is CONSTRUCTED and says so; nothing is a claim about any model or
about the folder's own (empty) admitted set. Both directions of every
guard.

    python3 ontology-probe/selftest_op.py
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))
import probe  # noqa: E402
import no_severity  # noqa: E402

FAILS = []
N = [0]


def check(name, cond):
    N[0] += 1
    if not cond:
        FAILS.append(name)
        print("  FAIL  " + name)


def refuses(name, fn):
    try:
        fn()
        check(name, False)
    except probe.Refused:
        check(name, True)


def resp(restatement, used, added, status):
    return "restatement: %s\nterms_used: %s\nterms_added: %s\nstatus: %s" % (
        restatement, ", ".join(used), ", ".join(added) or "none", status)


# ----------------------------------------------------------------- fixture

def fixture_constructions():
    """30 constructions, 12 CONTROL / 9 TARGETED / 9 AMBIENT (section 9 step
    2 counts), every one CONSTRUCTED in this file to exercise the scorer.
    hand_built is False on all of them: they are not the folder's set."""
    src = "CONSTRUCTED fixture written in selftest_op.py to exercise the scorer; not a construction anyone hand-built"
    out = []
    for i in range(1, 13):
        out.append({"id": "fx-c%02d" % i, "text": "constructed control statement %d" % i,
                    "premise": "constructed", "class": "CONTROL", "hand_built": False, "source": src})
    targets = ["cost", "optimum", "analogy", "name", "picture", "law", "cost", "optimum", "analogy"]
    for i in range(1, 10):
        out.append({"id": "fx-t%02d" % i, "text": "constructed targeted statement %d" % i,
                    "premise": "constructed", "class": "TARGETED", "targets": [targets[i - 1]],
                    "hand_built": False, "source": src})
    for i in range(1, 10):
        out.append({"id": "fx-a%02d" % i, "text": "constructed ambient statement %d" % i,
                    "premise": "constructed", "class": "AMBIENT", "hand_built": False, "source": src})
    return out


# status plan per construction id, per family. "R" = varies across repeats
# (fam-1 only, fx-t04): FAILS, FAILS, COMPOSES -> the N3 instability arm.
PLAN = {
    "fx-c01": ("COMPOSES", "COMPOSES"), "fx-c02": ("COMPOSES", "COMPOSES"), "fx-c03": ("COMPOSES", "COMPOSES"),
    "fx-c04": ("COMPOSES", "COMPOSES"), "fx-c05": ("COMPOSES", "COMPOSES"), "fx-c06": ("COMPOSES", "COMPOSES"),
    "fx-c07": ("COMPOSES", "COMPOSES"), "fx-c08": ("COMPOSES", "COMPOSES"), "fx-c09": ("COMPOSES", "COMPOSES"),
    "fx-c10": ("FAILS", "FAILS"), "fx-c11": ("FAILS", "COMPOSES"), "fx-c12": ("COMPOSES_WITH_ADDITION", "COMPOSES"),
    "fx-t01": ("COMPOSES", "COMPOSES"), "fx-t02": ("COMPOSES_WITH_ADDITION", "COMPOSES_WITH_ADDITION"),
    "fx-t03": ("FAILS", "COMPOSES"), "fx-t04": ("R", "FAILS"), "fx-t05": ("FAILS", "FAILS"),
    "fx-t06": ("FAILS", "FAILS"), "fx-t07": ("FAILS", "FAILS"), "fx-t08": ("FAILS", "FAILS"), "fx-t09": ("FAILS", "FAILS"),
    "fx-a01": ("COMPOSES", "COMPOSES"), "fx-a02": ("COMPOSES", "COMPOSES"), "fx-a03": ("COMPOSES", "COMPOSES"),
    "fx-a04": ("COMPOSES", "COMPOSES"), "fx-a05": ("COMPOSES", "COMPOSES"),
    "fx-a06": ("COMPOSES_WITH_ADDITION", "COMPOSES_WITH_ADDITION"),
    "fx-a07": ("FAILS", "FAILS"), "fx-a08": ("FAILS", "FAILS"), "fx-a09": ("COMPOSES", "FAILS"),
}
ADDED = {"fx-t02": ["dominance"], "fx-a06": ["the"], "fx-c12": ["stronger than"]}


def fixture_runs():
    """Two constructed families, three repeats, one leaking restatement
    (fx-a01 fam-1 rep 1: status COMPOSES, restatement carries words outside
    the list) and one malformed record."""
    R = []
    for cid, (f1, f2) in sorted(PLAN.items()):
        for fam, fstat in (("fam-1", f1), ("fam-2", f2)):
            for rep in (1, 2, 3):
                st = fstat
                if st == "R":
                    st = "COMPOSES" if rep == 3 else "FAILS"
                text = "flux across the boundary under dissipation"
                if cid == "fx-a01" and fam == "fam-1" and rep == 1:
                    text = "the alpha wolf leads the pack across the boundary"
                added = ADDED.get(cid, []) if st == "COMPOSES_WITH_ADDITION" else []
                R.append({"run_id": "%s|%s|%d" % (cid, fam, rep), "ontology": "SHAPE_SPEC",
                          "ontology_version": "0.1.0", "construction_id": cid,
                          "model": "constructed-%s" % fam, "family": fam, "repeat": rep, "date": "2026-09-09",
                          "raw_response": resp(text, ["flux", "boundary", "dissipation"], added, st),
                          "constructed": True})
    R.append({"run_id": "fx-c01|fam-1|malformed", "ontology": "SHAPE_SPEC", "ontology_version": "0.1.0",
              "construction_id": "fx-c01", "model": "constructed-fam-1", "family": "fam-1", "repeat": 4,
              "date": "2026-09-09", "raw_response": "I think this composes fine.", "constructed": True})
    return R


# ----------------------------------------------------------------- main

def main():
    print("selftest_op")
    prims = probe.load_primitives()
    spec = open(os.path.join(ROOT, "SHAPE_SPEC.md"), encoding="utf-8").read().lower()

    # ---- primitives: the declaration's own rule
    def present(term):
        return re.search(r"\b" + re.escape(term.lower()) + r"(s|es|d|ed|ing)?\b", spec) is not None
    for e in prims["primitives"]:
        check("primitive %r appears in SHAPE_SPEC.md" % e["term"], present(e["term"]))
    for a in prims["absent_by_design"]:
        check("absent_by_design %r appears in SHAPE_SPEC.md (an absence the spec states)" % a["term"], present(a["term"]))
    check("declaration marks itself unconfirmed by the author", prims["_declaration"]["confirmed_by_author"] is False)
    check("a term not in the spec is detectable", not present("thermocouple"))
    pr = probe.primitives_report(prims)
    check("undefined grounding surfaces as a candidate hole", pr["undefined_candidate_holes"] == ["critical point"])
    check("absent_by_design non-empty -> does not claim no protection", not pr["claims_no_protection"])
    check("physics share is a fraction", 0.0 < pr["physics_share"] < 1.0)
    check("grounding class follows the share", pr["grounding_class"] == ("physics-grounded" if pr["physics_share"] >= 0.5 else "declared-only"))
    empty_abs = json.loads(json.dumps(prims)); empty_abs["absent_by_design"] = []
    check("empty absent_by_design is legal and reported as claiming no protection",
          probe.primitives_report(probe.validate_primitives(empty_abs))["claims_no_protection"])
    bad = json.loads(json.dumps(prims)); bad["primitives"][0]["type"] = "thing"
    refuses("a type outside the four is refused", lambda: probe.validate_primitives(bad))
    bad = json.loads(json.dumps(prims)); bad["primitives"][0]["grounds_to"] = "vibes"
    refuses("a grounding outside the three is refused", lambda: probe.validate_primitives(bad))
    bad = json.loads(json.dumps(prims)); bad["primitives"].append(dict(bad["primitives"][0]))
    refuses("a duplicate primitive is refused", lambda: probe.validate_primitives(bad))
    bad = json.loads(json.dumps(prims)); bad["absent_by_design"].append({"term": "flux", "reason": "x"})
    refuses("a term both primitive and absent is refused", lambda: probe.validate_primitives(bad))
    bad = json.loads(json.dumps(prims)); bad["absent_by_design"].append({"term": "cost2"})
    refuses("an absent entry without a reason is refused", lambda: probe.validate_primitives(bad))
    bad = json.loads(json.dumps(prims)); del bad["absent_by_design"]
    refuses("a missing absent_by_design field is refused (empty is legal, missing is not)", lambda: probe.validate_primitives(bad))
    bad = json.loads(json.dumps(prims)); bad["primitives"] = []
    refuses("an empty primitive list is refused", lambda: probe.validate_primitives(bad))

    # ---- constructions
    admitted = probe.load_constructions(probe.CONSTRUCTIONS, prims)
    check("no construction is admitted (every shipped one is a candidate)", admitted == [])
    cands = probe.candidates()
    check("three candidates listed, none hand_built", len(cands) == 3 and all(c["hand_built"] is False for c in cands))
    check("candidates cover the three classes", {c["class"] for c in cands} == set(probe.CLASSES))
    sr = probe.set_report(admitted)
    check("empty set flags EMPTY and BELOW_MINIMUM", any("EMPTY" in f for f in sr["flags"]) and any("BELOW" in f for f in sr["flags"]))
    check("control share on an empty set is None, not 0", sr["control_share"] is None)
    fx = fixture_constructions()
    for c in fx:
        probe.validate_construction(c, prims)
    fr = probe.set_report(fx)
    check("fixture set is 30 with 12/9/9", fr["n"] == 30 and fr["by_class"] == {"TARGETED": 9, "AMBIENT": 9, "CONTROL": 12})
    check("fixture clears the 40% control floor and carries no flag", fr["flags"] == [] and fr["control_share"] == 0.4)
    short = [c for c in fx if c["class"] != "CONTROL"] + fx[:5]
    check("a set under the control floor flags CONTROL_SHORT", any("CONTROL_SHORT" in f for f in probe.set_report(short)["flags"]))
    check("a TARGETED construction with no targets validates ([CHOICE 5]: the order's schema has no such field)",
          probe.validate_construction({"id": "x", "text": "t", "premise": "p", "class": "TARGETED", "hand_built": True}, prims)["id"] == "x")
    refuses("a TARGETED construction targeting a non-absent term is refused",
            lambda: probe.validate_construction({"id": "x", "text": "t", "premise": "p", "class": "TARGETED",
                                                 "targets": ["flux"], "hand_built": True}, prims))
    refuses("a class outside the three is refused",
            lambda: probe.validate_construction({"id": "x", "text": "t", "premise": "p", "class": "OTHER", "hand_built": True}, prims))
    refuses("hand_built as a string is refused",
            lambda: probe.validate_construction({"id": "x", "text": "t", "premise": "p", "class": "CONTROL", "hand_built": "yes"}, prims))
    check("a well-formed CONTROL validates",
          probe.validate_construction({"id": "x", "text": "t", "premise": "p", "class": "CONTROL", "hand_built": True}, prims)["id"] == "x")

    # ---- prompt: read from the order, not retyped
    order = probe.order_text()
    tmpl = probe.prompt_template()
    flat = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731
    check("section 4 template is a substring of the delivered order", flat(tmpl) in flat(order))
    check("template carries both placeholders", "[PRIMITIVES]" in tmpl and "[CONSTRUCTION TEXT]" in tmpl)
    check("template carries the four output fields and three statuses",
          all(k in tmpl for k in ("restatement:", "terms_used:", "terms_added:", "status:")) and all(s in tmpl for s in probe.STATUSES))
    pm = probe.render_prompt(prims, cands[0])
    check("rendered prompt carries the construction text", cands[0]["text"] in pm)
    check("rendered prompt carries every primitive once as term (type)",
          all(pm.count("%s (%s)" % (e["term"], e["type"])) == 1 for e in prims["primitives"]))
    check("rendered prompt names no absent_by_design term as a primitive line",
          not any(re.search(r"^%s \(" % re.escape(a["term"]), pm, re.M) for a in prims["absent_by_design"]))
    back = pm.replace(probe.render_primitives(prims), "[PRIMITIVES]").replace(cands[0]["text"], "[CONSTRUCTION TEXT]")
    check("substituting the render back out returns the template", back == tmpl)

    # ---- parsing
    p = probe.parse_response(resp("flux across the boundary", ["flux", "boundary"], [], "COMPOSES"))
    check("well-formed response parses", p["status"] == "COMPOSES" and not p["malformed"] and p["terms_used"] == ["flux", "boundary"])
    check("terms_added 'none' reads as empty", p["terms_added"] == [])
    p = probe.parse_response(resp("x", ["flux"], ["dominance", "rank"], "composes_with_addition"))
    check("status is case-insensitive and additions split", p["status"] == "COMPOSES_WITH_ADDITION" and p["terms_added"] == ["dominance", "rank"])
    p = probe.parse_response("restatement: x\nterms_used: flux\nterms_added: none\nstatus: MAYBE")
    check("an unknown status is MALFORMED, kept apart from MISSING", p["status"] == "MALFORMED" and p["malformed"])
    p = probe.parse_response("I think this composes fine.")
    check("prose with no fields is MISSING and malformed", p["status"] == "MISSING" and p["malformed"] and "lacks 4 of 4 fields" in " ".join(p["notes"]))
    p = probe.parse_response("preamble\n" + resp("x", ["flux"], [], "FAILS") + "\ntrailer")
    check("lines outside the fields are counted, not fatal", not p["malformed"] and "2 line(s) outside" in " ".join(p["notes"]))

    # ---- leak and undeclared
    check("a restatement inside the list leaks nothing", probe.leak("flux across the boundary under dissipation", prims, []) == [])
    check("a multi-word primitive contributes each word", probe.leak("the constraint set", prims, []) == [])
    check("words outside the list leak", probe.leak("the alpha wolf leads", prims, []) == ["alpha", "leads", "wolf"])
    check("a declared addition does not leak", probe.leak("the alpha wolf", prims, ["alpha wolf"]) == [])
    check("undeclared terms_used are reported", probe.undeclared_used(["flux", "rank"], prims, []) == ["rank"])
    check("a declared addition in terms_used is not undeclared", probe.undeclared_used(["flux", "rank"], prims, ["rank"]) == [])

    # ---- reading table, section 5
    T = probe.reading
    check("FAILS on TARGETED -> PROTECTION", T("TARGETED", "FAILS") == "PROTECTION")
    check("COMPOSES on TARGETED -> HOLE", T("TARGETED", "COMPOSES") == "HOLE")
    check("COMPOSES on CONTROL -> USABLE", T("CONTROL", "COMPOSES") == "USABLE")
    check("FAILS on CONTROL -> NARROW", T("CONTROL", "FAILS") == "NARROW")
    check("addition on any class -> ADDITION", all(T(c, "COMPOSES_WITH_ADDITION") == "ADDITION" for c in probe.CLASSES))
    check("AMBIENT readings kept apart from TARGETED", T("AMBIENT", "COMPOSES") == "AMBIENT_COMPOSES" and T("AMBIENT", "FAILS") == "AMBIENT_FAILS")
    check("malformed status -> MALFORMED", T("CONTROL", "MISSING") == "MALFORMED")

    # ---- rates: known answers
    r = probe.rates([("TARGETED", "FAILS"), ("CONTROL", "FAILS"), ("AMBIENT", "FAILS")])
    check("all FAILS -> hole 0, narrowness 1, ambient 0", (r["hole_rate"], r["narrowness"], r["ambient_rate"]) == (0.0, 1.0, 0.0))
    r = probe.rates([("TARGETED", "COMPOSES"), ("CONTROL", "COMPOSES"), ("AMBIENT", "COMPOSES")])
    check("all COMPOSES -> hole 1, narrowness 0, ambient 1", (r["hole_rate"], r["narrowness"], r["ambient_rate"]) == (1.0, 0.0, 1.0))
    r = probe.rates([("CONTROL", "COMPOSES"), ("AMBIENT", "FAILS")])
    check("no TARGETED row -> hole_rate None, never 0", r["hole_rate"] is None and r["narrowness"] == 0.0)
    r = probe.rates([("TARGETED", "COMPOSES_WITH_ADDITION"), ("TARGETED", "COMPOSES")])
    check("addition row in the denominator, not the numerator ([CHOICE 2])", r["hole_rate"] == 0.5 and r["addition_rate"]["TARGETED"] == 0.5)
    r = probe.rates([])
    check("empty rows -> every rate None", r["hole_rate"] is None and r["narrowness"] is None and r["ambient_rate"] is None)

    # ---- the constructed fixture end to end
    runs = fixture_runs()
    probe.validate_runs(runs, fx)
    res = probe.score_runs(runs, fx, prims, fixture=True)
    check("181 runs, 1 malformed", res["n_runs"] == 181 and res["n_malformed"] == 1)
    check("every record constructed", res["constructed_share"] == 1.0)
    a = res["aggregates"]
    # hand count over the plan: per family 9 targeted x 3 repeats.
    # fam-1: t01 C x3, t02 add x3, t03 F, t04 F F C, rest F -> COMPOSES 4 of 27
    # fam-2: t01 C x3, t02 add x3, t03 C x3, rest F -> COMPOSES 6 of 27
    check("hole_rate hand-counted 10/54", abs(a["hole_rate"] - 10 / 54) < 1e-12)
    # controls: fam-1 c10 F x3, c11 F x3 -> 6 FAILS; fam-2 c10 F x3 -> 3; of 72
    check("narrowness hand-counted 9/72", abs(a["narrowness"] - 9 / 72) < 1e-12)
    # ambient: fam-1 a01-a05 C (15) + a09 C (3) = 18; fam-2 a01-a05 C = 15; of 54
    check("ambient_rate hand-counted 33/54", abs(a["ambient_rate"] - 33 / 54) < 1e-12)
    check("addition_rate per class", abs(a["addition_rate"]["TARGETED"] - 6 / 54) < 1e-12 and abs(a["addition_rate"]["CONTROL"] - 3 / 72) < 1e-12)
    check("smuggle_set is the union of terms_added", res["smuggle_set"] == ["dominance", "stronger than", "the"])
    check("leak set carries the undeclared words", set(res["leak_set"]) >= {"alpha", "wolf", "leads", "pack"})
    check("exactly one status contradicted by leak", res["n_status_contradicted"] == 1)
    con = [s for s in res["scored"] if s["status_contradicted"]]
    check("the contradicted run keeps its self-reported status", con[0]["status"] == "COMPOSES" and con[0]["reading"] == "AMBIENT_COMPOSES")
    check("malformed run reads MALFORMED and leaks nothing",
          any(s["reading"] == "MALFORMED" and s["leak"] == [] for s in res["scored"] if s["malformed"]))
    nl = res["nulls"]
    check("N1 does not fire (FAILS present)", nl["N1"]["fires"] is False)
    check("N2 does not fire (COMPOSES present)", nl["N2"]["fires"] is False)
    check("N3 sees 60 groups with 3 repeats", nl["N3"]["groups_with_repeats"] == 60)
    check("N3 fires on exactly the planned unstable group", nl["N3"]["fires"] and nl["N3"]["which"] == ["fx-t04|constructed-fam-1"])
    check("N3 instability is 1/60", abs(nl["N3"]["instability"] - 1 / 60) < 1e-12)
    check("N4 share 1/3 does not fire", abs(nl["N4"]["function_word_share"] - 1 / 3) < 1e-12 and nl["N4"]["fires"] is False)
    check("N5 does not fire (rates differ)", nl["N5"]["fires"] is False)
    cl = res["claims"]
    check("OP-1 not refuted at hole_rate < 1", cl["OP-1"]["verdict"] == "not refuted")
    check("OP-2 not refuted (premise-bearing additions)", cl["OP-2"]["verdict"] == "not refuted")
    check("OP-3 not refuted (ambient 0.61 > hole 0.19)", cl["OP-3"]["verdict"] == "not refuted")
    check("OP-4 undetermined on one ontology", cl["OP-4"]["verdict"] == "undetermined")
    check("OP-5 undetermined with one primitive set", cl["OP-5"]["verdict"] == "undetermined")
    fd = res["family_disagreement"]
    check("30 constructions seen by two families", fd["constructions_with_two_families"] == 30)
    check("families disagree on the planned 5 (c11, c12, t03, t04, a09)",
          fd["disagreements"] == 5 and {r["construction_id"] for r in fd["rows"] if r["disagree"]} == {"fx-c11", "fx-c12", "fx-t03", "fx-t04", "fx-a09"})

    # ---- nulls and claims, the other direction
    def world(status_by_class, families=("fam-1",), reps=(1,), added=None):
        R = []
        for c in fx:
            for fam in families:
                for rep in reps:
                    st = status_by_class[c["class"]]
                    R.append({"run_id": "%s|%s|%d" % (c["id"], fam, rep), "ontology": "SHAPE_SPEC", "ontology_version": "0.1.0",
                              "construction_id": c["id"], "model": "w-" + fam, "family": fam, "repeat": rep, "date": "2026-09-09",
                              "raw_response": resp("flux", ["flux"], added or [], st), "constructed": True})
        return R
    allc = probe.score_runs(world({"TARGETED": "COMPOSES", "AMBIENT": "COMPOSES", "CONTROL": "COMPOSES"}), fx, prims, True)
    check("N1 fires when everything composes", allc["nulls"]["N1"]["fires"] is True)
    check("N5 fires when hole and ambient track exactly", allc["nulls"]["N5"]["fires"] is True)
    check("OP-1 REFUTED when every TARGETED composes", allc["claims"]["OP-1"]["verdict"] == "REFUTED")
    check("OP-3 REFUTED at ambient == hole", allc["claims"]["OP-3"]["verdict"] == "REFUTED")
    allf = probe.score_runs(world({"TARGETED": "FAILS", "AMBIENT": "FAILS", "CONTROL": "FAILS"}), fx, prims, True)
    check("N2 fires when nothing composes, controls included", allf["nulls"]["N2"]["fires"] is True)
    check("narrowness 1.0 on that world", allf["aggregates"]["narrowness"] == 1.0)
    check("N3 NOT_EVALUABLE with single repeats", allf["nulls"]["N3"].get("verdict") == "NOT_EVALUABLE")
    check("N4 NOT_EVALUABLE with an empty smuggle_set", allf["nulls"]["N4"].get("verdict") == "NOT_EVALUABLE")
    check("OP-2 undetermined with no terms_added", allf["claims"]["OP-2"]["verdict"] == "undetermined")
    fw = probe.score_runs(world({"TARGETED": "COMPOSES_WITH_ADDITION", "AMBIENT": "FAILS", "CONTROL": "COMPOSES"},
                                added=["the", "of the", "and"]), fx, prims, True)
    check("N4 fires on a function-word smuggle_set", fw["nulls"]["N4"]["fires"] is True and fw["nulls"]["N4"]["function_word_share"] == 1.0)
    check("OP-2 REFUTED under N4", fw["claims"]["OP-2"]["verdict"] == "REFUTED")
    two = world({"TARGETED": "COMPOSES", "AMBIENT": "FAILS", "CONTROL": "COMPOSES"})
    for r in two:
        r["ontology"] = "OTHER"
    both = probe.score_runs(runs[:0] + two + world({"TARGETED": "COMPOSES", "AMBIENT": "FAILS", "CONTROL": "COMPOSES"}, families=("fam-2",)), fx, prims, True)
    check("OP-4 not refuted when hole sets overlap across two ontologies", both["claims"]["OP-4"]["verdict"] == "not refuted")
    dis = two + world({"TARGETED": "FAILS", "AMBIENT": "FAILS", "CONTROL": "COMPOSES"}, families=("fam-2",))
    both2 = probe.score_runs(dis, fx, prims, True)
    check("OP-4 REFUTED on non-overlap", both2["claims"]["OP-4"]["verdict"] == "REFUTED")
    check("op5: physics below declared -> not refuted", probe.op5(0.2, 0.5) == "not refuted")
    check("op5: parity refutes", probe.op5(0.5, 0.5) == "REFUTED")
    check("op5: physics above declared refutes", probe.op5(0.7, 0.5) == "REFUTED")
    check("op5: a missing rate is undetermined, never a verdict", probe.op5(None, 0.5) == "undetermined")
    empty = probe.score_runs([], fx, prims, True)
    check("no runs -> every null NOT_EVALUABLE", all(v.get("verdict") == "NOT_EVALUABLE" for v in empty["nulls"].values()))
    check("no runs -> constructed_share None", empty["constructed_share"] is None)
    check("no runs -> OP-1 undetermined", empty["claims"]["OP-1"]["verdict"] == "undetermined")

    # ---- run-log refusals
    refuses("a run naming an unadmitted construction is refused",
            lambda: probe.validate_runs([dict(runs[0], construction_id="cand-001")], fx))
    refuses("a duplicate run_id is refused", lambda: probe.validate_runs([runs[0], dict(runs[0])], fx))
    refuses("a run missing a required field is refused",
            lambda: probe.validate_runs([{k: v for k, v in runs[0].items() if k != "family"}], fx))
    refuses("constructed as a string is refused", lambda: probe.validate_runs([dict(runs[0], constructed="yes")], fx))
    refuses("repeat 0 is refused", lambda: probe.validate_runs([dict(runs[0], repeat=0)], fx))
    refuses("an empty model is refused", lambda: probe.validate_runs([dict(runs[0], model=" ")], fx))
    check("a well-formed log validates", probe.validate_runs(runs, fx) is runs)

    # ---- CLI, screen, source
    py = sys.executable
    rc = subprocess.run([py, os.path.join(HERE, "probe.py"), "--selftest"], capture_output=True).returncode
    check("probe.py refuses --selftest with rc 2", rc == 2)
    rc = subprocess.run([py, os.path.join(HERE, "probe.py")], capture_output=True).returncode
    check("probe.py with no command exits 2", rc == 2)
    out = probe.render(res)
    # declared exemption: the ontology's own term `critical point` (SHAPE_SPEC.md
    # section 8) carries a screened word. Three arms.
    masked = re.sub(r"critical", "cr1tical", out, flags=re.I)
    check("score render screens clean with the ontology's own term masked", not no_severity.hits(masked))
    check("the ontology's own term is the only thing that fires in the render", {h[1] for h in no_severity.hits(out)} == {"critical"})
    check("a planted word is caught through the exemption", {h[1] for h in no_severity.hits(masked + "\nthis is wrong\n")} == {"wrong"})
    pm_masked = re.sub(r"critical", "cr1tical", pm, flags=re.I)
    check("prompt render screens clean with the same term masked", not no_severity.hits(pm_masked))
    check("the same term is the only thing that fires in the prompt", {h[1] for h in no_severity.hits(pm)} == {"critical"})
    check("empty render screens clean under the same mask", not no_severity.hits(re.sub(r"critical", "cr1tical", probe.render(empty), flags=re.I)))
    src = open(os.path.join(HERE, "probe.py"), encoding="utf-8").read()
    check("no network module in the instrument", not re.search(r"^\s*(import|from)\s+(urllib|http|socket|requests)", src, re.M))
    check("no author section", "Author" not in src)
    check("every [CHOICE] printed", all("[CHOICE %d]" % i in out for i in probe.CHOICES))
    check("constructed banner printed", "EVERY RECORD IS CONSTRUCTED" in out)
    check("fixture banner printed", "FIXTURE" in out)
    check("no-run render says so", "No model has been run" in probe.render(empty))
    fxp = os.path.join(HERE, "runs", "constructed_constructions.jsonl")
    rp = os.path.join(HERE, "runs", "constructed.jsonl")
    with open(fxp, "w", encoding="utf-8") as fh:
        for c in fx:
            fh.write(json.dumps(c, sort_keys=True) + "\n")
    with open(rp, "w", encoding="utf-8") as fh:
        for r in runs:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "score", rp, "--fixture", fxp], capture_output=True, text=True)
    check("CLI score on the fixture reproduces the render", cp.returncode == 0 and cp.stdout == out)
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "score", rp], capture_output=True, text=True)
    check("CLI score without --fixture refuses the fixture runs (unadmitted constructions)", cp.returncode != 0)
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "prompt", "cand-001"], capture_output=True, text=True)
    check("CLI prompt refuses a candidate (not admitted)", cp.returncode == 2)

    # ---- the operator's set and the first real run (ontologies/substrate-primary)
    OD = os.path.join(HERE, "ontologies", "substrate-primary")
    sp = probe.load_primitives(os.path.join(OD, "primitives.json"))
    spr = probe.primitives_report(sp)
    check("substrate-primary: 20 primitives, 9 absent_by_design", spr["n_primitives"] == 20 and spr["n_absent_by_design"] == 9)
    check("substrate-primary is physics-grounded at share 0.65", spr["grounding_class"] == "physics-grounded" and abs(spr["physics_share"] - 0.65) < 1e-12)
    check("substrate-primary carries no undefined primitive", spr["undefined_candidate_holes"] == [])
    check("the two declared sets fall in different grounding classes (OP-5's precondition on the primitive side)",
          spr["grounding_class"] != pr["grounding_class"])
    sc = probe.load_constructions(os.path.join(OD, "constructions.jsonl"), sp)
    scr = probe.set_report(sc)
    check("operator set: 30 admitted, 12/9/9, no flags", scr["n"] == 30 and scr["by_class"] == {"TARGETED": 9, "AMBIENT": 9, "CONTROL": 12} and scr["flags"] == [])
    check("every operator construction is hand_built", all(c["hand_built"] is True for c in sc))
    check("no operator TARGETED construction carries targets (the order's schema; [CHOICE 5] exercised)",
          all("targets" not in c for c in sc if c["class"] == "TARGETED"))
    check("no candidates in the operator set", probe.candidates(os.path.join(OD, "constructions.jsonl")) == [])
    rp1 = os.path.join(OD, "runs", "claudeopus5_r1.jsonl")
    rr, form = probe.load_runs(rp1, sp)
    check("the delivered run is read as a coded sheet", form == "coded" and len(rr) == 30)
    check("coded run_ids are made unique from run_id|id", len({r["run_id"] for r in rr}) == 30)
    check("coded records carry no restatement", all(r["raw_response"] is None for r in rr))
    check("a real run: constructed False on every record", all(r["constructed"] is False for r in rr))
    refuses("a coded log with no primitive set is refused", lambda: probe.load_runs(rp1))
    refuses("a coded record lacking status is refused",
            lambda: probe.adapt_coded({"run_id": "r", "family": "f", "repeat": 1, "id": "c-001", "class": "CONTROL",
                                       "terms_used": [], "terms_added": []}, sp))
    mixed = os.path.join(HERE, "runs", "mixed_refused.jsonl")
    with open(mixed, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(runs[0]) + "\n" + open(rp1, encoding="utf-8").readline())
    refuses("a log mixing raw and coded records is refused", lambda: probe.load_runs(mixed, sp))
    os.remove(mixed)
    R1 = probe.score_runs(rr, sc, sp, form=form)
    check("30 scored, 0 malformed, constructed share 0.0", R1["n_runs"] == 30 and R1["n_malformed"] == 0 and R1["constructed_share"] == 0.0)
    b = R1["binding"]
    check("ontology binding: every terms_used inside the primitive list, 30 of 30", b["terms_used_in_primitives"] == 30 and b["scored"] == 30)
    check("the run's class field agrees with the construction set on 30 of 30", b["class_agrees"] == 30 and b["class_recorded"] == 30)
    a1 = R1["aggregates"]
    check("hole_rate 0 of 9 (every TARGETED fails)", a1["hole_rate"] == 0.0)
    check("narrowness 0 of 12 (every CONTROL composes)", a1["narrowness"] == 0.0)
    check("ambient_rate 2 of 9 under [CHOICE 2]", abs(a1["ambient_rate"] - 2 / 9) < 1e-12)
    check("ambient_rate 7 of 9 with additions counted as composing", abs(a1["ambient_rate_incl_addition"] - 7 / 9) < 1e-12)
    check("hole_rate 0 under either reading", a1["hole_rate_incl_addition"] == 0.0)
    check("addition_rate TARGETED 0, AMBIENT 5/9, CONTROL 1/12",
          a1["addition_rate"]["TARGETED"] == 0.0 and abs(a1["addition_rate"]["AMBIENT"] - 5 / 9) < 1e-12
          and abs(a1["addition_rate"]["CONTROL"] - 1 / 12) < 1e-12)
    check("smuggle_set is ten premise-bearing terms",
          R1["smuggle_set"] == ["attribution", "competition", "contamination", "count", "efficiency", "learning",
                                "market", "maximize", "preference", "validity"])
    check("leak check NOT_EVALUABLE on every coded record", R1["n_leak_evaluable"] == 0 and all(s["leak"] is None for s in R1["scored"]))
    ms = R1["missing_summary"]
    check("13 cited missing primitives, 11 on the declared-absent list, none naming a primitive",
          ms["citations"] == 13 and ms["declared_absent"] == 11 and ms["primitive"] == [])
    check("two UNDECLARED absences cited, both on AMBIENT FAILS", ms["undeclared"] == ["absent-as-distinct-from-unread", "role"]
          and all(s["class"] == "AMBIENT" for s in R1["scored"] if any(m["cell"] == "undeclared" for m in s["cited_missing"])))
    check("every TARGETED FAILS cites a declared absence, 9 of 9", ms["targeted_fails_citing_declared_absence"] == 9 and ms["targeted_fails"] == 9)
    check("four restater notes carried", sum(1 for s in R1["scored"] if s["note"]) == 4)
    n1 = R1["nulls"]
    check("N1/N2 do not fire on the real run", n1["N1"]["fires"] is False and n1["N2"]["fires"] is False)
    check("N3 NOT_EVALUABLE at one repeat", n1["N3"].get("verdict") == "NOT_EVALUABLE")
    check("N4 share 0.0 (no function word in the smuggle_set), does not fire", n1["N4"]["function_word_share"] == 0.0 and n1["N4"]["fires"] is False)
    check("N5 does not fire (0.000 against 0.222)", n1["N5"]["fires"] is False)
    c1 = R1["claims"]
    check("OP-1, OP-2, OP-3 not refuted on the real run", all(c1[k]["verdict"] == "not refuted" for k in ("OP-1", "OP-2", "OP-3")))
    check("OP-4, OP-5 undetermined on the real run", c1["OP-4"]["verdict"] == "undetermined" and c1["OP-5"]["verdict"] == "undetermined")
    check("one family, so no restater disagreement is computable", R1["family_disagreement"]["constructions_with_two_families"] == 0)
    out1 = probe.render(R1)
    check("real render carries no constructed banner and no fixture banner", "EVERY RECORD IS CONSTRUCTED" not in out1 and "FIXTURE" not in out1)
    check("real render states the coded form", "input form: coded" in out1)
    # declared exemption: the delivered absent term `better/worse` carries two screened words
    m1 = re.sub(r"better/worse", "b3tter/w0rse", out1)
    check("real render screens clean with the delivered term masked", not no_severity.hits(m1))
    check("the delivered term is the only thing that fires in the real render", {h[1] for h in no_severity.hits(out1)} == {"better", "worse"})
    check("a planted word is caught through that exemption", {h[1] for h in no_severity.hits(m1 + "\nthis is wrong\n")} == {"wrong"})
    pm1 = probe.render_prompt(sp, {c["id"]: c for c in sc}["c-001"])
    check("operator prompt render screens clean, no exemption", not no_severity.hits(pm1))
    check("operator prompt carries every primitive and no absent term as a line",
          all(pm1.count("%s (%s)" % (e["term"], e["type"])) == 1 for e in sp["primitives"])
          and not any(re.search(r"^%s \(" % re.escape(x["term"]), pm1, re.M) for x in sp["absent_by_design"]))
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "declare", "--ontology", OD], capture_output=True, text=True)
    check("CLI declare --ontology reports the admitted 30", cp.returncode == 0 and '"n": 30' in cp.stdout and "CANDIDATE" not in cp.stdout)
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "prompt", "c-001", "--ontology", OD], capture_output=True, text=True)
    check("CLI prompt --ontology renders an admitted construction", cp.returncode == 0 and cp.stdout.strip() == pm1.strip())
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "score", rp1], capture_output=True, text=True)
    check("the real run scored against the default (SHAPE_SPEC) set is refused: constructions not admitted there", cp.returncode != 0)
    import hashlib
    sha = lambda path: hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]  # noqa: E731
    check("delivered constructions byte-identical to the upload (sha256 pinned)",
          sha(os.path.join(OD, "constructions.jsonl")) == "1cf4c362c093150e")
    check("delivered run log byte-identical to the upload (sha256 pinned)", sha(rp1) == "480c7676e455a388")

    # ---- absent-term coverage and alias reimport ([CHOICE 6])
    cov0 = R1["absent_coverage"]
    check("coverage without aliases: 8 of 9 absent terms exercised, motive UNEXERCISED",
          cov0["exercised"] == 8 and cov0["n_absent"] == 9 and cov0["unexercised"] == ["motive"])
    check("c-013's premise names intent AND motive; the restater cited intent only",
          "motive" in {c["id"]: c for c in sc}["c-013"]["premise"]
          and cov0["rows"]["intent"]["cited_by"] == ["r1|c-013", "r1|c-017"] and cov0["rows"]["motive"]["cited_by"] == [])
    check("reimport NOT_DECLARED when no alias table is passed (None, not zero)",
          R1["reimport_summary"]["declared"] is False and all(s["reimports"] is None for s in R1["scored"]))
    check("the SHAPE_SPEC ontology declares no aliases", probe.load_aliases(HERE, prims) is None)
    al = probe.load_aliases(OD, sp)
    check("substrate-primary aliases load, declared by the audit and dated after run 1",
          al is not None and "audit" in al["declared_by"] and "run 1" in al["written_after"])
    check("every alias table key is an absent term and no alias is a primitive or absent term",
          set(al["table"]) <= {x["term"].lower() for x in sp["absent_by_design"]}
          and not ({a for v in al["table"].values() for a in v} & ({e["term"] for e in sp["primitives"]} | set(al["table"]))))
    R1a = probe.score_runs(rr, sc, sp, form=form, aliases=al)
    rs = R1a["reimport_summary"]
    check("two records hit the alias table on run 1", rs["records_with_hit"] == 2)
    check("c-025 preference => interior_state is the restater's own note, now a declared-list hit",
          any(h["construction_id"] == "c-025" and h["added"] == "preference" and h["absent"] == "interior_state"
              and "restater note" in h["basis"] for h in rs["hits"]))
    check("c-024 efficiency => better/worse is the audit's reading and marked CONTESTABLE",
          any(h["construction_id"] == "c-024" and h["absent"] == "better/worse" and "CONTESTABLE" in h["basis"] for h in rs["hits"]))
    check("eight added terms match no alias (the table does not fire on everything)",
          rs["added_terms_unmatched"] == ["attribution", "competition", "contamination", "count", "learning", "market", "maximize", "validity"])
    check("aliases move nothing in the section 5 rates", R1a["aggregates"] == R1["aggregates"] and R1a["smuggle_set"] == R1["smuggle_set"])
    cov1 = R1a["absent_coverage"]
    check("with aliases motive is still UNEXERCISED; coverage 8 of 9 either way",
          cov1["unexercised"] == ["motive"] and cov1["rows"]["interior_state"]["reimported_via"] == ["c-025:preference"])
    # null both ways on the loader
    def bad_alias(obj):
        d = os.path.join(HERE, "runs", "_alias_null")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "aliases.json"), "w", encoding="utf-8") as fh:
            json.dump(obj, fh)
        try:
            return probe.load_aliases(d, sp)
        finally:
            os.remove(os.path.join(d, "aliases.json")); os.rmdir(d)
    decl = {"declared_by": "x", "written_after": "y"}
    refuses("an alias file naming a non-absent term is refused",
            lambda: bad_alias({"_declaration": decl, "aliases": {"gravity": [{"term": "g", "basis": "b"}]}}))
    refuses("an alias that is a primitive is refused",
            lambda: bad_alias({"_declaration": decl, "aliases": {"intent": [{"term": "energy", "basis": "b"}]}}))
    refuses("an alias with no basis is refused",
            lambda: bad_alias({"_declaration": decl, "aliases": {"intent": [{"term": "purpose"}]}}))
    refuses("an undated alias file is refused",
            lambda: bad_alias({"_declaration": {"declared_by": "x"}, "aliases": {}}))
    check("a well-formed minimal alias file loads",
          bad_alias({"_declaration": decl, "aliases": {"intent": [{"term": "purpose", "basis": "b"}]}})["table"] == {"intent": {"purpose": "b"}})
    check("reimports on a term outside the table is empty, not None", probe.reimports(["zzz"], al) == [])
    # coverage null: a run citing nothing leaves every absent term UNEXERCISED
    cov_empty = probe.absent_coverage([], sp)
    check("coverage over no scored run: 0 of 9, share 0.0", cov_empty["exercised"] == 0 and cov_empty["share_exercised"] == 0.0)
    check("coverage over an ontology with no absent terms is None, not zero",
          probe.absent_coverage([], {"absent_by_design": []})["share_exercised"] is None)
    out1 = probe.render(R1a)
    check("real render carries the coverage table and the UNEXERCISED term", "UNEXERCISED motive" in out1)
    check("real render carries the alias declaration and its date", "written after: run 1" in out1)
    m1 = re.sub(r"better/worse", "b3tter/w0rse", out1)
    check("real render with aliases screens clean under the same one-token exemption", not no_severity.hits(m1))
    check("the delivered term is still the only thing that fires", {h[1] for h in no_severity.hits(out1)} == {"better", "worse"})
    cp = subprocess.run([py, os.path.join(HERE, "probe.py"), "score", rp1, "--ontology", OD], capture_output=True, text=True)
    check("CLI score --ontology picks up aliases.json and reproduces the render", cp.returncode == 0 and cp.stdout == out1)
    r0 = probe.render(R1)
    check("a render without aliases states NOT_DECLARED", "alias reimport ([CHOICE 6]): NOT_DECLARED" in r0)

    # ---- pin samples
    sd = os.path.join(HERE, "samples")
    with open(os.path.join(sd, "score_substrate-primary_claudeopus5_r1.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out1)
    with open(os.path.join(sd, "prompt_substrate-primary_c-001.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(pm1 + "\n")
    with open(os.path.join(sd, "score_constructed.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    with open(os.path.join(sd, "score_empty.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(probe.render(empty))
    with open(os.path.join(sd, "prompt_cand-001.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write("# CANDIDATE construction, not admitted; render shown for the prompt form only\n" + pm + "\n")
    with open(os.path.join(sd, "declare.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(json.dumps(pr, indent=1, sort_keys=True) + "\nadmitted constructions: %s\n" % json.dumps(sr, sort_keys=True))
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
