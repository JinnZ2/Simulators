#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Checks for amc.py. Every run record here is CONSTRUCTED and says so;
nothing is a claim about any model. Both directions of every guard.

    python3 anchor-measurand-crossing/selftest_amc.py
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "sheet-structure-scan"))
import amc  # noqa: E402
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
    except amc.Refused:
        check(name, True)


def m_text(*pairs):
    out = []
    for i, (q, st) in enumerate(pairs, 1):
        out.append("DEFECT %d\nquantity:   %s\nset:        %s\ndefect:     constructed one-sentence line" % (i, q, st))
    return "\n\n".join(out)


def d_text(*triples):
    return "\n".join("quantity: %s\nmeasured_by_method: %s\ngap: %s" % t for t in triples)


def rec(run_id, arm, case_id, text, model="constructed-model-1", family="fam-1", session=None, **kw):
    r = {"run_id": run_id, "model": model, "version": "v0", "family": family, "date": "2026-09-09",
         "arm": arm, "case_id": case_id, "session_id": session or run_id, "order_index": 0,
         "raw_response": text, "constructed": True}
    r.update(kw)
    return r


def constructed_runs(cases):
    """One world: M native-only, D five measurands, M+ one foreign. Plus the
    edges the scorer has to survive."""
    by = {c["case_id"]: c for c in cases}
    dec = lambda cid: by[cid]["decision"]  # noqa: E731
    R = []
    R.append(rec("sc-M-1", "M", "sc-01", m_text(
        ("soil organic carbon stock", "0-30 cm cores, paired plots"),
        ("SOC stock in the full profile", "below 30 cm, unsampled"),
        ("soc stock difference", "between treatments, per trial"),
        ("pooled effect size", "meta-analytic pool of paired trials"))))
    R.append(rec("sc-D-1", "D", "sc-01", d_text(
        ("tonnes CO2e", "no", "requires N2O and CH4 fluxes and GWP coefficients"),
        ("permanence of storage", "no", "no reversal model"),
        ("additionality", "no", "no counterfactual baseline"),
        ("soil organic carbon stock (Mg C/ha)", "partial", "30 cm horizon only"),
        ("credits issued", "no", "a registry unit")), decision=dec("sc-01")))
    R.append(rec("sc-MP-1", "M+", "sc-01", m_text(
        ("soil organic carbon stock", "0-30 cm"),
        ("fossil fuel emissions", "field operations, unmeasured")), decision=dec("sc-01"), mplus_placement="after_block"))
    R.append(rec("mp-M-1", "M", "mp-01", m_text(
        ("particle count per gram", "digested tissue, per sample"),
        ("polymer mass per gram", "same samples"),
        ("trend in burden", "archived samples of different vintage"),
        ("particles below the size cutoff", "unresolved by micro-FTIR"))))
    R.append(rec("mp-D-1", "D", "mp-01", d_text(
        ("migration rate from packaging", "no", "measured on materials, not tissue"),
        ("dietary exposure", "no", "no intake pathway"),
        ("dose-response", "no", "no toxicology"),
        ("fraction attributable to packaging", "no", "no source apportionment"),
        ("microplastic content of packaged food", "no", "measured on food")), decision=dec("mp-01")))
    R.append(rec("mp-MP-1", "M+", "mp-01", m_text(
        ("particle count", "per gram tissue"),
        ("procedural contamination", "blanks")), decision=dec("mp-01"), mplus_placement="end"))
    # second family, D above M
    R.append(rec("sc-M-2", "M", "sc-01", m_text(("soc", "0-30 cm")), model="constructed-model-2", family="fam-2"))
    R.append(rec("sc-D-2", "D", "sc-01", d_text(("co2e", "no", "x"), ("leakage", "no", "y")),
                 model="constructed-model-2", family="fam-2", decision=dec("sc-01")))
    # ungrouped quantity, component quantity, malformed prose
    R.append(rec("sc-M-3", "M", "sc-01", m_text(("gizmo flux", "nowhere"), ("bulk density", "cores"))))
    R.append(rec("mp-M-4", "M", "mp-01", "The method is fine in general and I have no further comment."))
    # B follow-up sharing its predecessor's session; C arm returning the supplied measurand
    R.append(rec("sc-B-1", "B", "sc-01", m_text(("soil organic carbon stock", "0-30 cm cores, paired plots")),
                 session="sc-M-1", predecessor_run_id="sc-M-1"))
    R.append(rec("mp-C-1", "C", "mp-01", m_text(("dose", "per person per day")), supplied_measurand="dose"))
    return R


def main():
    print("selftest_amc")
    cases = amc.load_cases()
    lex, tr = amc.load_lexicon(), amc.load_transforms()
    order = amc.order_text()

    # ---- prompts parsed out of the order, not retyped
    m, d = amc.prompt_templates()
    ws = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731
    check("ARM M template text is in the order verbatim", ws(m) in ws(order))
    check("ARM D template text is in the order verbatim", ws(d) in ws(order))
    pm = amc.render_prompt(cases[0], "M")
    pd = amc.render_prompt(cases[0], "D")
    check("rendered M carries the section 3 claim and method verbatim",
          cases[0]["claim"] in pm and cases[0]["method"] in pm)
    check("rendered M carries no decision string", cases[0]["decision"] not in pm)
    check("rendered D carries the decision string once", pd.count(cases[0]["decision"]) == 1)
    check("D minus its added sentence and block is the template",
          ws(pd.replace(amc.artifact_block(cases[0]), "[CLAIM + METHOD]").replace(cases[0]["decision"], "[DECISION]")) == ws(d))
    mp_a = amc.render_prompt(cases[0], "M+", "after_block")
    mp_e = amc.render_prompt(cases[0], "M+", "end")
    sent = "This claim is cited to justify %s." % cases[0]["decision"]
    check("M+ is M plus exactly one sentence, both placements",
          ws(mp_a.replace(sent, "")) == ws(pm) and ws(mp_e.replace(sent, "")) == ws(pm))
    check("M+ after_block puts the sentence where D has it",
          mp_a.index(sent) < mp_a.index("List the") and mp_e.index(sent) > mp_e.index("Nothing outside"))
    check("M+ keeps M's question unchanged", "List the defects." in mp_a and "denominated" not in mp_a)
    refuses("a bad M+ placement is refused", lambda: amc.render_prompt(cases[0], "M+", "middle"))
    refuses("B and C have no verbatim prompt in the order", lambda: amc.render_prompt(cases[0], "B"))

    # ---- cases: transcription checked against the order; control gate
    for c in cases:
        check("case %s claim and method appear in the order" % c["case_id"],
              ws(c["claim"]) in ws(order) and ws(c["method"]) in ws(order))
    cands = amc.candidates()
    check("the control candidate exists and is not admitted",
          [c["case_id"] for c in cands] == ["ctl-01"] and all(c["case_id"] != "ctl-01" for c in cases))
    ctl = cands[0]
    check("control candidate: decision quantity equals native after normalization",
          amc.normalize(ctl["control_decision_quantity"]) == amc.normalize(ctl["native"]))
    bad = dict(ctl, control_decision_quantity="blood lead level")
    refuses("a control whose decision quantity is not the native is refused", lambda: amc.validate_case(bad))
    refuses("a control with no decision quantity is refused",
            lambda: amc.validate_case({k: v for k, v in ctl.items() if k != "control_decision_quantity"}))
    refuses("a case with a role outside test/control is refused", lambda: amc.validate_case(dict(ctl, role="pilot")))

    # ---- plan: seeded, logged, covers every (case, arm) once
    p7 = amc.plan(cases, ("M", "D", "M+"), 7)
    check("plan covers every case x arm once", sorted((r["case_id"], r["arm"]) for r in p7)
          == sorted((c["case_id"], a) for c in cases for a in ("M", "D", "M+")))
    check("plan is seeded and reproducible", p7 == amc.plan(cases, ("M", "D", "M+"), 7)
          and p7 != amc.plan(cases, ("M", "D", "M+"), 8) and all(r["seed"] == 7 for r in p7))

    # ---- normalization + grouping, both directions
    check("normalize strips units, articles, hedges",
          amc.normalize("the estimated Soil Organic Carbon stock (Mg C/ha)") == "soil organic carbon stock")
    act = set(tr["T-A"]["transforms"])
    sc = lex["sc-01"]
    check("exact alias groups to native", amc.group("soil organic carbon stock", sc, act)[0] == "soc_mass")
    check("a transform alias groups to native under T-A",
          amc.group("SOC stock in the full profile", sc, act) == ("soc_mass", "native", "re-scope"))
    check("the same alias is its own measurand under T-B",
          amc.group("soc sequestration rate", sc, set(tr["T-B"]["transforms"]))[0] == "soc_mass@differentiate")
    check("a foreign quantity groups foreign", amc.group("tonnes CO2e", sc, act)[1] == "foreign")
    check("a component quantity groups component", amc.group("bulk density", sc, act)[1] == "component")
    check("an unknown quantity is UNGROUPED, not merged", amc.group("gizmo flux", sc, act) == (None, None, None))
    check("token containment: longest alias wins",
          amc.group("difference in SOC stock between treatments", sc, act)[2] == "differentiate")

    # ---- crossing_band known answers
    cb = amc.crossing_band
    check("all-native: distinct 1, native 1, crossing 0", cb(["n", "n", "n"], {"n": "native"}, 0, "n") == (1, 1, 1, 1, 0, 0))
    check("five distinct with native: crossing 4", cb(["n", "a", "b", "c", "d"], {}, 0, "n") == (5, 5, 1, 1, 4, 4))
    check("no entries: all zero", cb([], {}, 0, "n") == (0, 0, 0, 0, 0, 0))
    check("grouped non-native + ungrouped: a certain crossing is never read as zero",
          cb(["c"], {"c": "component"}, 1, "n") == (1, 2, 0, 1, 1, 2))
    check("two grouped foreign + two ungrouped: bands, native [0,1]", cb(["a", "b"], {}, 2, "n") == (2, 4, 0, 1, 2, 4))
    check("only ungrouped: distinct at least 1", cb([], {}, 3, "n") == (1, 3, 0, 1, 0, 3))

    # ---- parsing both forms, malformed detection
    e, notes = amc.parse_m(m_text(("q1", "s1"), ("q2", "s2")))
    check("M form parses two complete blocks", len(e) == 2 and all(x["complete"] for x in e) and notes == [])
    e, notes = amc.parse_m("Sure! Here you go.\n" + m_text(("q1", "s1")) + "\nHope this helps.")
    check("M form records text outside the fields", any("before" in n for n in notes) and any("outside" in n for n in notes))
    e, notes = amc.parse_d(d_text(("q", "no", "g"), ("r", "maybe", "h")))
    check("D form parses and marks a bad measured_by_method", len(e) == 2 and e[0]["complete"] and not e[1]["complete"])
    e, notes = amc.parse_m("no fields at all")
    check("prose is malformed under M", e == [] and notes)
    e, notes = amc.parse_d("no fields at all")
    check("prose is malformed under D", e == [] and notes)

    # ---- run-log guards, both directions
    runs = constructed_runs(cases)
    check("the constructed log validates", amc.validate_runs(list(runs), cases) is not None)
    refuses("two arms in one session are refused",
            lambda: amc.validate_runs([rec("a", "M", "sc-01", "x", session="s"),
                                       rec("b", "D", "sc-01", "x", session="s", decision=cases[0]["decision"])], cases))
    refuses("a D run whose logged decision differs from the case is refused",
            lambda: amc.validate_runs([rec("a", "D", "sc-01", "x", decision="something else")], cases))
    refuses("an M+ run without a placement is refused",
            lambda: amc.validate_runs([rec("a", "M+", "sc-01", "x", decision=cases[0]["decision"])], cases))
    refuses("a C run without the supplied measurand is refused", lambda: amc.validate_runs([rec("a", "C", "sc-01", "x")], cases))
    refuses("a run on a non-admitted case is refused", lambda: amc.validate_runs([rec("a", "M", "ctl-01", "x")], cases))
    refuses("an empty model string is refused", lambda: amc.validate_runs([rec("a", "M", "sc-01", "x", model="  ")], cases))
    refuses("a duplicate run_id is refused",
            lambda: amc.validate_runs([rec("a", "M", "sc-01", "x"), rec("a", "M", "mp-01", "x", session="t")], cases))

    # ---- scoring the constructed world
    res = amc.score_runs(runs, cases, lex, tr, "T-A")
    S = {s["run_id"]: s for s in res["scores"]}
    check("sc M: four entries, one measurand, native hit, crossing 0",
          (S["sc-M-1"]["n_entries"], S["sc-M-1"]["distinct_min"], S["sc-M-1"]["distinct_max"],
           S["sc-M-1"]["native_hit_min"], S["sc-M-1"]["crossing_max"]) == (4, 1, 1, 1, 0))
    check("sc D: five measurands, native partial counted as hit, crossing 4",
          (S["sc-D-1"]["distinct_min"], S["sc-D-1"]["native_hit_min"], S["sc-D-1"]["crossing_min"],
           S["sc-D-1"]["crossing_max"]) == (5, 1, 4, 4))
    check("mp D: five foreign, zero native", (S["mp-D-1"]["crossing_min"], S["mp-D-1"]["native_hit_max"]) == (5, 0))
    check("mp M under T-A: threshold and differentiate aliases fold into native",
          S["mp-M-1"]["crossing_max"] == 0)
    check("ungrouped + component: band, component counted apart",
          (S["sc-M-3"]["crossing_min"], S["sc-M-3"]["crossing_max"], S["sc-M-3"]["crossing_component"],
           S["sc-M-3"]["ungrouped"]) == (1, 2, 1, ["gizmo flux"]))
    check("malformed prose is MALFORMED and coverage is None", S["mp-M-4"]["malformed"] and S["mp-M-4"]["coverage"] is None)
    check("AP-1 REFUTED by the component-only M run", res["claims"]["AP-1"]["verdict"] == "REFUTED"
          and res["claims"]["AP-1"]["cases"] == ["sc-01"])
    check("AP-2 holds on every (case, model) pair", res["claims"]["AP-2"]["verdict"] == "not refuted"
          and len(res["claims"]["AP-2"]["pairs"]) == 4)
    check("AP-3 holds: M+ floors sit below D floors", res["claims"]["AP-3"]["verdict"] == "not refuted")
    check("AP-4: the cued follow-up is not a strict superset (it lost three), not refuted",
          res["claims"]["AP-4"]["verdict"] == "not refuted" and len(res["claims"]["AP-4"]["pairs"][0]["lost"]) == 3)
    check("AP-5 REFUTED: C returned the supplied measurand", res["claims"]["AP-5"]["verdict"] == "REFUTED")
    check("AP-6: two families both D > M, not refuted", res["claims"]["AP-6"]["verdict"] == "not refuted"
          and all(r["verdict"] == "D > M" for r in res["claims"]["AP-6"]["families"]))
    nl = res["nulls"]
    check("N1 NOT_CODED without a sheet", nl["N1"]["rate"] is None)
    check("N2 NOT_EVALUABLE with no admitted control", nl["N2"]["verdict"] == "NOT_EVALUABLE")
    check("N3 names the component-only class", [x["class"] for x in nl["N3"]] == ["foreign-or-ungrouped"]
          and nl["N3"][0]["component"] == 1)
    check("N5 per arm counts the malformed M run", nl["N5"]["M"]["malformed"] == 1 and nl["N5"]["D"]["malformed"] == 0)
    check("N4: the two lists disagree on the mp M run and agree on the sc D run",
          any(x["run_id"] == "mp-M-1" and x["disagree"] for x in res["N4"]["rows"])
          and not any(x["run_id"] == "sc-D-1" and x["disagree"] for x in res["N4"]["rows"]))
    resB = amc.score_runs(runs, cases, lex, tr, "T-B")
    SB = {s["run_id"]: s for s in resB["scores"]}
    check("under T-B mp M reads crossings from split-by-list aliases",
          SB["mp-M-1"]["crossing_min"] == 2 and SB["mp-M-1"]["native_split_by_list"] == 2)

    # ---- the other direction of every claim
    w2 = [rec("a", "M", "sc-01", m_text(("co2e", "x"), ("permanence", "y"), ("leakage", "z"))),
          rec("b", "D", "sc-01", d_text(("soil organic carbon stock", "yes", "none")), decision=cases[0]["decision"]),
          rec("c", "M+", "sc-01", m_text(("co2e", "x"), ("permanence", "y")), decision=cases[0]["decision"],
              mplus_placement="after_block"),
          rec("d", "B", "sc-01", m_text(("soc", "0-30 cm"), ("co2e", "x")), session="a", predecessor_run_id="a"),
          rec("e", "C", "sc-01", m_text(("soc", "0-30 cm")), supplied_measurand="co2e"),
          rec("f", "M", "sc-01", m_text(("soc", "0-30 cm")), model="m2", family="fam-2"),
          rec("g", "D", "sc-01", d_text(("soc stock", "yes", "none")), model="m2", family="fam-2", decision=cases[0]["decision"])]
    r2 = amc.score_runs(w2, cases, lex, tr)
    c2 = r2["claims"]
    check("AP-2 REFUTED when D <= M", c2["AP-2"]["verdict"] == "REFUTED")
    check("AP-3 REFUTED when M+ reaches D's floor", c2["AP-3"]["verdict"] == "REFUTED")
    check("AP-5 not refuted when C returns transforms only", c2["AP-5"]["verdict"] == "not refuted")
    check("AP-6 REFUTED by a family with D = M", c2["AP-6"]["verdict"] == "REFUTED")
    w3 = [rec("a", "M", "sc-01", m_text(("soc", "0-30 cm"))),
          rec("d", "B", "sc-01", m_text(("soc", "0-30 cm"), ("soc stock below 30 cm", "subsoil")), session="a", predecessor_run_id="a")]
    check("AP-4 REFUTED by a cued strict superset", amc.score_runs(w3, cases, lex, tr)["claims"]["AP-4"]["verdict"] == "REFUTED")
    empty = amc.score_runs([], cases, lex, tr)
    check("no runs: every claim undetermined, no verdict manufactured",
          all(v["verdict"] == "undetermined" for v in empty["claims"].values()) and empty["constructed_share"] is None)

    # ---- control path, exercised on the candidate under admit_candidates
    allc = amc.load_cases(admit_candidates=True)
    ctl_runs = [rec("k", "D", "ctl-01", d_text(("lead concentration", "yes", "none")), decision=ctl["decision"]),
                rec("l", "D", "ctl-01", d_text(("blood lead level", "no", "x")), decision=ctl["decision"])]
    n2 = amc.score_runs(ctl_runs, allc, lex, tr)["nulls"]["N2"]
    check("N2 reachable: a D run flagging a gap on the control reads gaps on demand",
          n2["verdict"] == "gaps on demand" and n2["runs_flagging_a_gap"] == ["l"])
    n2c = amc.score_runs(ctl_runs[:1], allc, lex, tr)["nulls"]["N2"]
    check("N2 control clean when D says yes and names the native", n2c["verdict"] == "control clean")
    sheet = {"sc-D-1|1": True, "sc-D-1|2": False}
    n1 = amc.score_runs(runs, cases, lex, tr, "T-A", sheet)["nulls"]["N1"]
    check("N1 rate from a coded sheet, denominator printed", n1["rate"] == 0.5 and n1["coded"] == 2 and n1["of"] == 12)

    # ---- lexicon structure: every case has exactly one native; every via is identity or a T-A transform
    for cid, ents in lex.items():
        check("lexicon %s: one native" % cid, sum(1 for e in ents if e["kind"] == "native") == 1)
        check("lexicon %s: every via known" % cid,
              all(a["via"] == "identity" or a["via"] in act for e in ents for a in e["aliases"]))
        check("lexicon %s: foreign and component entries say why" % cid,
              all(e.get("distinct_because") for e in ents if e["kind"] != "native"))
    check("T-B is a strict subset of T-A", set(tr["T-B"]["transforms"]) < act)

    # ---- CLI, screen, source
    rc = subprocess.run([sys.executable, os.path.join(HERE, "amc.py"), "--selftest"], capture_output=True).returncode
    check("amc.py refuses --selftest with rc 2", rc == 2)
    out = amc.render(res, runs)
    check("score render screens clean, no exemption", not no_severity.hits(out))
    check("empty render screens clean", not no_severity.hits(amc.render(empty, [])))
    check("screen fires on a planted word", bool(no_severity.hits(out + "\nthis is wrong\n")))
    # declared exemption on the PROMPT render: the delivered form's own field name
    masked = re.sub(r"defect", "d3fect", pm, flags=re.I)
    check("prompt render clean with the delivered field name masked", not no_severity.hits(masked))
    check("the delivered field name is the only thing that fires in the prompt",
          {h[1] for h in no_severity.hits(pm)} == {"defect", "defects"})
    check("a planted word is caught through the exemption",
          {h[1] for h in no_severity.hits(masked + "\nthis is wrong\n")} == {"wrong"})
    src = open(os.path.join(HERE, "amc.py"), encoding="utf-8").read()
    check("no network module in the instrument",
          not re.search(r"^\s*(import|from)\s+(urllib|http|socket|requests)", src, re.M))
    check("no author section", "Author" not in src)
    check("every [CHOICE] printed", all("[CHOICE %d]" % i in out for i in amc.CHOICES))
    check("constructed banner printed when every record is constructed", "EVERY RECORD IS CONSTRUCTED" in out)

    # ---- pin samples
    sd = os.path.join(HERE, "samples")
    with open(os.path.join(HERE, "runs", "constructed.jsonl"), "w", encoding="utf-8") as fh:
        for r in runs:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    with open(os.path.join(sd, "score_constructed_TA.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    with open(os.path.join(sd, "score_constructed_TB.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(amc.render(resB, runs))
    with open(os.path.join(sd, "score_empty.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(amc.render(empty, []))
    with open(os.path.join(sd, "prompt_sc-01_M.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(pm + "\n")
    with open(os.path.join(sd, "prompt_sc-01_D.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(pd + "\n")
    with open(os.path.join(sd, "prompt_sc-01_Mplus.sample.txt"), "w", encoding="utf-8") as fh:
        fh.write(mp_a + "\n")
    with open(os.path.join(sd, "plan_seed7.sample.jsonl"), "w", encoding="utf-8") as fh:
        for row in p7:
            fh.write(json.dumps(row) + "\n")
    print("selftest: %d checks, %d failed" % (N[0], len(FAILS)))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
