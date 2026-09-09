#!/usr/bin/env python3
"""selftest_apm.py -- checks for anchor-position/. Run via
python3 score.py --selftest. Prints its count; the count is not stored
anywhere else in this folder."""
import json
import os
import shutil
import tempfile
import textwrap

import normalize as nz
import prompts
import score

HERE = os.path.dirname(os.path.abspath(__file__))
CASES = os.path.join(HERE, "cases.jsonl")
MAIN = os.path.join(HERE, "fixtures", "responses.constructed.jsonl")
CONF = os.path.join(HERE, "fixtures", "responses.confound.constructed.jsonl")
_n = [0]


def check(cond, msg):
    _n[0] += 1
    if not cond:
        raise AssertionError("check %d: %s" % (_n[0], msg))


def _verbatim(template, order_text):
    """every non-blank template line, with the substitution slots kept,
    appears verbatim (after dedent) in the work order's section 4."""
    body = textwrap.dedent(order_text.split("## 4.")[1].split("## 5.")[0])
    lines = [l.strip() for l in body.splitlines()]
    return all(l.strip() in lines for l in template.splitlines() if l.strip())


def main():
    order = open(os.path.join(HERE, "WORK_ORDER.md"), encoding="utf-8").read()
    cases = prompts.load_cases(CASES)
    byid = {c["case_id"]: c for c in cases}
    lex = nz.load_lexicon(nz.PRIMARY)
    alt = nz.load_lexicon(nz.ALT)

    # --- the order's text is the prompt ---------------------------------
    check(_verbatim(prompts.ARM_M, order), "ARM M is not verbatim from section 4")
    check(_verbatim(prompts.ARM_D, order), "ARM D is not verbatim from section 4")
    check(prompts.DECISION_LINE in prompts.ARM_D, "M+ adds a line that is not D's line")
    for c in cases:
        m, d, mp = (prompts.render(c, a) for a in ("M", "D", "M+"))
        check(c["native"] not in m + d + mp and "native" not in (m + d + mp).lower(),
              "%s: a prompt leaks the native" % c["case_id"])
        check(c["decision"] not in m, "%s: M carries the decision" % c["case_id"])
        check(c["decision"] in d and c["decision"] in mp, "%s: D/M+ lack the decision" % c["case_id"])
        extra = [l for l in mp.splitlines() if l not in m.splitlines()]
        check(extra == [prompts.DECISION_LINE.replace("[DECISION]", c["decision"])],
              "%s: M+ differs from M by more than the one line" % c["case_id"])
        tail = prompts.render(c, "M+", mplus_tail=True)
        check(tail.startswith(m.rstrip("\n")) and c["decision"] in tail, "tail placement")
    check(sum(1 for c in cases if c["decision_native"]) >= 1,
          "section 8 requires a control case where native == decision measurand")
    check(all(c["decision"].lower().find(w) < 0 for c in cases
              for w in ("mg", "ug", "per gram", "per litre", "count", "mass")),
          "a decision string names a unit or measurand (section 4: it must not)")

    # --- seeded order ----------------------------------------------------
    tmp = tempfile.mkdtemp()
    try:
        r1 = prompts.emit(cases, os.path.join(tmp, "a"), 3)
        r2 = prompts.emit(cases, os.path.join(tmp, "b"), 3)
        r3 = prompts.emit(cases, os.path.join(tmp, "c"), 4)
        check([r["order"] for r in r1] == [r["order"] for r in r2], "order not seeded")
        check([r["order"] for r in r1] != [r["order"] for r in r3], "order ignores the seed")
        check(set(os.listdir(os.path.join(tmp, "a"))) == {"order.jsonl"} | {
            "%s.%s.txt" % (c["case_id"], a) for c in cases for a in prompts.ARMS}, "emitted files")
    finally:
        shutil.rmtree(tmp)

    # --- normalize / group ------------------------------------------------
    same = lambda a, b, L=lex: nz.score([a], b, L)["native_hit"] == 1
    check(same("SOC concentration by dry combustion", "soil organic carbon mass, Mg C/ha"),
          "concentration is a transform of stock (bulk density is in the method)")
    check(same("change in SOC stock over the trial period", "soil organic carbon mass"), "differentiate")
    check(same("pooled effect size of the SOC stock difference", "soil organic carbon mass"), "aggregate")
    check(same("whole-profile soil organic carbon stock to 1 m", "soil organic carbon mass"), "rescope")
    check(not same("tonnes of CO2-equivalent removed", "soil organic carbon mass"), "co2e needs a coefficient")
    check(not same("net greenhouse gas balance including N2O", "soil organic carbon mass"), "ghg balance")
    check(not same("polymer-specific hazard", "particle count or polymer mass per gram tissue"),
          "an extra measurand token makes a different quantity (no one-token chaining)")
    check(same("ug polymer per gram wet tissue", "particle count or polymer mass per gram tissue"), "mass form")
    check(same("particle number in archived samples", "particle count or polymer mass"), "number -> count")
    check(not same("SOC concentration by dry combustion", "soil organic carbon mass", alt),
          "alt list: concentration is measurand vocabulary")
    s = nz.score(["particle count per gram", "polymer mass per gram"], "particle count or polymer mass", lex)
    check(s["crossing_count"] == 0 and s["crossing_count_order"] == 1 and s["native_groups_hit"] == 2,
          "disjunctive native: two native groups are not one crossing; the order's form is printed beside")
    check(nz.score(["the", "of"], "x", lex)["unresolved"] == 2, "emptied cores are unresolved, not measurands")
    check(nz.crossing_count([], "x", lex) is None, "no entries -> None, absent not zero")
    rec = nz.normalize("soil organic carbon stock", lex)[1]
    check(rec["core"].count("soil") == 1, "alias overlap: 'organic carbon' must not re-fire inside 'soil organic carbon'")
    check(nz.normalize("exposure from food-contact materials", lex)[1]["unknown"], "unknown tokens are reported")

    # --- parsing ------------------------------------------------------------
    e, f = score.parse_response("DEFECT 1\nquantity: a\nset: b\ndefect: c\n", "M")
    check(len(e) == 1 and f["form_ok"], "M form parses")
    e, f = score.parse_response("quantity: a\nmeasured_by_method: maybe\ngap: g\n", "D")
    check(len(e) == 1 and not f["form_ok"] and not f["values_ok"], "D value outside yes|no|partial")
    e, f = score.parse_response("Sure!\nquantity: a\nmeasured_by_method: no\ngap: g\n  continued\n", "D")
    check(len(e) == 1 and f["stray_lines"] == 1 and e[0]["gap"] == "g continued", "stray and continuation")
    e, f = score.parse_response("DEFECT 1\nquantity: a\nset: b\n", "M")
    check(e == [] and f["incomplete"] == 1 and not f["form_ok"], "incomplete entry is not scored")

    # --- both worlds ------------------------------------------------------
    cs, sc, cl, nl, lexes = score.run(CASES, MAIN)
    P = "primary"
    get = lambda c, a: [s for s in sc if s["case_id"] == c and s["arm"] == a][0]["by_lexicon"][P]
    check(get("sc-01", "M")["crossing_count"] == 0 and get("sc-01", "D")["crossing_count"] == 5, "sc-01 world")
    check(get("sc-01", "D")["native_hit"] == 1, "sc-01 D partial native hit")
    check(get("mp-01", "D")["crossing_count"] == 5 and get("mp-01", "D")["native_hit"] == 0, "mp-01 D")
    check(get("mp-01", "M")["crossing_count"] == 0, "mp-01 M")
    check(get("ctl-01", "D")["crossing_count"] == 0, "control D reads native")
    check(cl[P]["AP-1"][0] == "SUPPORTED" and cl[P]["AP-2"][0] == "SUPPORTED"
          and cl[P]["AP-3"][0] == "SUPPORTED", "main world claims")
    check(cl[P]["AP-2"][1]["controls_excluded"] == ["ctl-01"], "controls excluded from AP-2 and named")
    check(all(cl[P][k][0] == "UNRUN" for k in ("AP-4", "AP-5", "AP-6")), "unrun arms are UNRUN, not passed")
    check(nl["N1"][0] == "NOT_EVALUATED" and nl["N2"][0] == "CLEAN" and nl["N3"][0] == "SILENT", "main nulls")
    check(nl["N4"][0] == "FIRES", "the two lists disagree on the main world (N4 reachable)")
    cs, sc2, cl2, nl2, _ = score.run(CASES, CONF)
    check(cl2[P]["AP-3"][0] == "REFUTED" and cl2[P]["AP-3"][1]["Mplus_reaches_D"][0][0] == "sc-01",
          "confound world: M+ reaches D-level -> AP-3 REFUTED (branch reachable)")
    check(cl2[P]["AP-1"][0] == "REFUTED" and cl2[P]["AP-5"][0] == "REFUTED", "AP-1 and AP-5 refutable")
    check(cl2[P]["AP-4"][0] == "SUPPORTED" and cl2[P]["AP-4"][1]["pairs"] == 1, "AP-4 evaluated on a B row")
    check(nl2["N2"][0] == "FIRES" and nl2["N3"][0] == "FIRES", "N2 and N3 fire when they should")
    check(nl2["N5"][1]["form_ok_rate"]["M"] < 1.0 and nl2["N5"][0] == "SILENT",
          "a form failure is reported as a rate; N5 needs both arms below the floor")
    rep = score.report(cs, sc2, cl2, nl2, lexes)
    check("decision strings logged" in rep and cs["sc-01"]["decision"] in rep, "decision string logged (section 9)")

    # --- refusals ---------------------------------------------------------
    tmp = tempfile.mkdtemp()
    try:
        bad = os.path.join(tmp, "bad.jsonl")
        with open(bad, "w") as fh:
            fh.write(json.dumps({"case_id": "sc-01", "arm": "D", "model": "m", "version": "v",
                                 "date": "d", "response": "", "decision": "something else"}) + "\n")
        try:
            score.run(CASES, bad)
            check(False, "a D row with a different decision string must be refused")
        except ValueError:
            check(True, "")
        with open(bad, "w") as fh:
            fh.write(json.dumps({"case_id": "sc-01", "arm": "C", "model": "m", "version": "v",
                                 "date": "d", "response": ""}) + "\n")
        try:
            score.run(CASES, bad)
            check(False, "a C row without supplied_measurand must be refused")
        except ValueError:
            check(True, "")
    finally:
        shutil.rmtree(tmp)
    print("selftest_apm: %d checks passed" % _n[0])
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
