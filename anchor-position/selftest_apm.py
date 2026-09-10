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
REFUTE = os.path.join(HERE, "fixtures", "responses.refute.constructed.jsonl")
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
    md_lines, m_lines = prompts.ARM_MD.splitlines(), prompts.ARM_M.splitlines()
    check([l for l in md_lines if l not in prompts.D_FIELDS] == [l for l in m_lines if l not in prompts.M_FIELDS],
          "W9: M_D's non-field lines are M's, line for line")
    check([l for l in md_lines if l in prompts.D_FIELDS] == prompts.D_FIELDS
          and not any(l in md_lines for l in prompts.M_FIELDS), "W9: M_D's fields are D's")
    for c in cases:
        md = prompts.render(c, "M_D")
        check(c["decision"] not in md and c["native"] not in md, "%s: M_D carries the decision or native" % c["case_id"])
    check(sum(1 for c in cases if c["decision_native"]) >= 1,
          "section 8 requires a control case where native == decision measurand")
    check(all(nz.names_unit_or_measurand(c["decision"], lex) == [] for c in cases),
          "a decision string names a unit or measurand (section 4: it must not)")
    # W8: the old substring guard read 'count' inside 'account' and 'ug' inside 'drug'
    check(nz.names_unit_or_measurand("the account for the county drug", lex) == [],
          "W8: account / county / drug must not fire")
    check(nz.names_unit_or_measurand("tonnes of it", lex) == ["tonnes"]
          and nz.names_unit_or_measurand("per kg", lex) == ["kg"]
          and nz.names_unit_or_measurand("over 10 ha", lex) == ["ha"],
          "W8: tonnes / kg / ha must fire")
    check("tonnes" in lex["units"] and "ha" in lex["units"], "W8: unit list is read from transforms.json")

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
        r4 = prompts.emit(cases, os.path.join(tmp, "d"), 3, arm_md=True)
        check(all("M_D" in r["order"] and r["arm_md"] for r in r4)
              and os.path.exists(os.path.join(tmp, "d", "sc-01.M_D.txt")), "W9: --arm-md emits <case>.M_D.txt")
        check(all(sorted(r["order"]) == sorted(prompts.ARMS_MD) for r in r4)
              and all(sorted(r["order"]) == sorted(prompts.ARMS) and not r["arm_md"] for r in r1),
              "W9: the order row carries the flag; with it off the three delivered arms are what is shuffled")
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
    z = nz.score([], "x", lex)
    check(z["absent"] and all(z[k] is None for k in ("crossing_count", "crossing_count_max", "crossing_count_order")),
          "W1: score() on no quantities returns None on every crossing field")
    w3 = nz.score(["soc yield"], "soil organic carbon mass", lex)
    check(w3["crossing_count"] == 0 and w3["crossing_count_max"] == 1,
          "W3: 'soc yield' vs the SOC native is native at the floor (unknown = residue) and a crossing at the ceiling")
    sa, sb, _ = nz.measurand_sets(["SOC stock to 30 cm", "bulk density of each core"],
                                  ["soil organic carbon stock to 30 cm"], "soil organic carbon mass", lex)
    check(sa > sb, "W5: a reworded superset registers on measurand groups")
    sa, sb, _ = nz.measurand_sets(["change in SOC stock over the trial"], ["SOC stock to 30 cm"],
                                  "soil organic carbon mass", lex)
    check(sa == sb, "W5: two transforms of one measurand are one group")
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
    e, f = score.parse_response("quantity: a\nmeasured_by_method: no\ngap: g\n", "M_D")
    check(len(e) == 1 and f["form_ok"] and e[0]["measured_by_method"] == "no", "W9: M_D parses in D form")

    # --- three worlds ------------------------------------------------------
    cs, sc, cl, nl, lexes = score.run(CASES, MAIN)
    P = "primary"
    get = lambda c, a, S=None: [s for s in (S or sc) if s["case_id"] == c and s["arm"] == a][0]["by_lexicon"][P]
    check(get("sc-01", "M")["crossing_count"] == 0 and get("sc-01", "D")["crossing_count"] == 5, "sc-01 world")
    check(get("sc-01", "D")["native_hit"] == 1, "sc-01 D partial native hit")
    check(get("mp-01", "D")["crossing_count"] == 5 and get("mp-01", "D")["native_hit"] == 0, "mp-01 D")
    check(get("mp-01", "M")["crossing_count"] == 0, "mp-01 M")
    check(get("ctl-01", "D")["crossing_count"] == 0, "control D reads native")
    # W3 on the delivered main world: AP-1 held only under the residue rule
    check(cl[P]["AP-1"][0] == "BAND" and cl[P]["AP-1"][1]["band"] == ["SUPPORTED", "REFUTED"],
          "main world AP-1 is BAND (floor SUPPORTED, ceiling REFUTED) -- N-W3, reported as the result")
    check(sorted(c for c, _ in cl[P]["AP-1"][1]["max"]["crossings"]) == ["ctl-01", "sc-01"],
          "the ceiling's AP-1 crossings are the unknown-token rows")
    check(cl[P]["AP-2"][0] == "SUPPORTED" and cl[P]["AP-3"][0] == "SUPPORTED", "main world AP-2, AP-3")
    check(cl[P]["AP-2"][1]["controls_excluded"] == ["ctl-01"], "controls excluded from AP-2 and named")
    check(cl[P]["AP-3"][1]["triples"] == 2 and cl[P]["AP-3"][1]["d_level"] == score.D_LEVEL, "AP-3 on informative triples")
    check(all(cl[P][k][0] == "UNRUN" for k in ("AP-4", "AP-5", "AP-6")), "unrun arms are UNRUN, not passed")
    check(nl["N1"][0] == "NOT_EVALUATED" and nl["N2"][0] == "CLEAN" and nl["N3"][0] == "SILENT", "main nulls")
    check(nl["N4"][0] == "FIRES", "the two lists disagree on the main world (N4 reachable)")
    check(score.collisions(sc) == [] and all(d["absent"] == 0 for d in score.absent_by_arm(sc, P).values()),
          "main world: no collisions, no ABSENT rows")
    rep = score.report(cs, sc, cl, nl, lexes)
    check(all("[CHOICE %d]" % k in rep for k in score.CHOICES) and all("[FLAG %s=off]" % k in rep for k in score.FLAGS),
          "W7: the header prints every CHOICE id and every FLAG")
    check(sorted(score.CHOICES) == list(range(1, max(score.CHOICES) + 1)), "W7: CHOICE ids are 1..n with no gap")
    check("ABSENT rows" in rep and "N-W3: BAND on AP-1" in rep and "N-W9" in rep, "W1/W3/W9 report lines")
    check("self-label vs scorer" in rep and "agree" in rep, "W11: self-label block printed")
    sl = score.self_label(sc, cs, P)
    check(all(r["agreement_rate"] is None or 0 <= r["agreement_rate"] <= 1 for r in sl) and sl,
          "W11: agreement rate per D-form row")

    cs, sc2, cl2, nl2, _ = score.run(CASES, CONF)
    check(cl2[P]["AP-3"][0] == "REFUTED" and cl2[P]["AP-3"][1]["Mplus_reaches_D"][0][0] == "sc-01",
          "confound world: M+ reaches D-level -> AP-3 REFUTED at both ends")
    check(cl2[P]["AP-1"][0] == "REFUTED", "AP-1 REFUTED at both ends on the confound world")
    check(cl2[P]["AP-5"][0] == "BAND" and cl2[P]["AP-5"][1]["band"] == ["REFUTED", "SUPPORTED"],
          "confound world AP-5 is BAND: the C row returns the supplied measurand at the floor only")
    check(cl2[P]["AP-4"][0] == "SUPPORTED" and cl2[P]["AP-4"][1]["pairs"] == 1, "AP-4 evaluated on a B row")
    check(nl2["N2"][0] == "FIRES" and nl2["N3"][0] == "FIRES", "N2 and N3 fire when they should")
    check(nl2["N5"][1]["form_ok_rate"]["M"] < 1.0 and nl2["N5"][0] == "SILENT",
          "a form failure is reported as a rate; N5 needs both arms below the floor")
    rep = score.report(cs, sc2, cl2, nl2, lexes)
    check("decision strings logged" in rep and cs["sc-01"]["decision"] in rep, "decision string logged (section 9)")

    cs, sc3, cl3, nl3, _ = score.run(CASES, REFUTE)
    check(cl3[P]["AP-2"][0] == "REFUTED" and cl3[P]["AP-2"][1]["D_le_M"] == [("mp-01", 0, 0)],
          "W6: AP-2 REFUTED reachable (a second family's D reads native only)")
    check(cl3[P]["AP-4"][0] == "REFUTED" and "bulk density of each core" in cl3[P]["AP-4"][1]["strict_superset"][0][1],
          "W5/W6: a reworded B superset of M -> AP-4 REFUTED on measurand groups")
    check(cl3[P]["AP-6"][0] == "REFUTED" and cl3[P]["AP-6"][1]["D_eq_M_family"] == ["constructed-b"],
          "W6: AP-6 REFUTED reachable")
    check(cl3[P]["AP-3"][0] == "REFUTED" and cl3[P]["AP-3"][1]["Mplus_reaches_D"] == [("mp-01", 5, 5)],
          "W2: a tie reaches D-level under 'ge'")
    gt = score.claims(sc3, cs, P, d_level="gt")
    check(gt["AP-3"][0] == "SUPPORTED" and gt["AP-3"][1]["Mplus_reaches_D"] == [],
          "W2: D_LEVEL='gt' flips the tie case -- the constant is read, not only printed")
    check(cl3[P]["AP-3"][1]["triples"] == 3 and cl3[P]["AP-3"][1]["uninformative"] == [],
          "W2: every M+ triple on this world is informative (the uninformative branch is shown below)")
    ab = score.absent_by_arm(sc3, P)
    check(ab["D"]["absent"] == 1 and get("sc-01", "M", sc3)["crossing_count"] is not None,
          "W1: the blank D row is ABSENT (None) and counted; the M row beside it is live")
    check(cl3[P]["AP-2"][1]["absent_pairs"] >= 1, "W1: the blank D row is skipped by AP-2, not read as refuting")
    col = score.collisions(sc3)
    check(col == [("sc-01", "constructed-model", "D", 2)], "W4: two replicate D rows -> collision count 1")
    check(cl3[P]["AP-2"][1]["pairs"] >= 4, "W4: paired claims use both replicates (all pairs)")
    rep3 = score.report(cs, sc3, cl3, nl3, lexes)
    check("replicate collisions" in rep3 and "x2" in rep3 and "ABSENT rows" in rep3, "W1/W4 report lines")
    check(nl3["N2"][0] == "FIRES", "the control D with a spurious second entry fires N2 under the delivered rule")
    # W2 acceptance world: D = M = M+ = 0 on a non-control case
    tmp = tempfile.mkdtemp()
    try:
        w = os.path.join(tmp, "w2.jsonl")
        row = lambda arm, resp, **kw: dict({"case_id": "sc-01", "arm": arm, "model": "m", "version": "v",
                                            "date": "d", "response": resp}, **kw)
        native_m = "DEFECT 1\nquantity: soil organic carbon stock to 30 cm\nset: plots\ndefect: x\n"
        native_d = "quantity: soil organic carbon stock to 30 cm\nmeasured_by_method: yes\ngap: none\n"
        dec = cases[0]["decision"]
        with open(w, "w") as fh:
            for r in (row("M", native_m), row("D", native_d, decision=dec), row("M+", native_m, decision=dec)):
                fh.write(json.dumps(r) + "\n")
        _, scw, clw, _, _ = score.run(CASES, w)
        check(clw[P]["AP-3"][0] == "UNRUN" and clw[P]["AP-3"][1]["triples"] == 0
              and clw[P]["AP-3"][1]["uninformative"] == [("sc-01", "cc(D)=0 <= cc(M)=0")],
              "W2: D=M=M+=0 -> AP-3 UNRUN with the triple listed as uninformative, not REFUTED")
        check(clw[P]["AP-2"][0] == "REFUTED", "the same world refutes AP-2 (D <= M), which is the order's rule")
        # W1: a blank M row does not count toward AP-1
        with open(w, "w") as fh:
            fh.write(json.dumps(row("M", "")) + "\n")
        _, scw, clw, nlw, _ = score.run(CASES, w)
        check(clw[P]["AP-1"][0] == "UNRUN" and clw[P]["AP-1"][1]["absent"] == 1, "W1: a blank M row is ABSENT, AP-1 UNRUN")
        check(nlw["N3"][0] == "SILENT" and nlw["N4"][0] == "AGREE", "W1: nulls skip None")
        # W9: M_D row refused without the flag, read with it
        with open(w, "w") as fh:
            fh.write(json.dumps(row("M_D", native_d)) + "\n")
            fh.write(json.dumps(row("D", "quantity: tonnes of CO2e\nmeasured_by_method: no\ngap: g\n", decision=dec)) + "\n")
            fh.write(json.dumps(row("M", native_m)) + "\n")
        try:
            score.run(CASES, w)
            check(False, "W9: an M_D row must be refused with the flag off")
        except ValueError:
            check(True, "")
        _, scw, clw, nlw, _ = score.run(CASES, w, flags={"arm_md": True})
        md = [s for s in scw if s["arm"] == "M_D"][0]
        check(md["entries"][0]["measured_by_method"] == "yes" and md["by_lexicon"][P]["crossing_count"] == 0,
              "W9: with the flag on, M_D is parsed in D form and scored")
        rd = score.md_reading(scw, cs, P)
        check(rd and rd[0]["crossing_count"]["reading"].startswith("M_D ~ M"), "W9: M_D ~ M reading reachable")
        repw = score.report(cs, scw, clw, nlw, lexes, flags={"arm_md": True})
        check("[FLAG arm_md=ON]" in repw and "M_D reading" in repw and "N-W9" not in repw, "W9: flag printed ON")
    finally:
        shutil.rmtree(tmp)
    # W10: N2 on entry 1 only, behind the flag
    _, _, _, nlf, _ = score.run(CASES, REFUTE, flags={"n2_first": True})
    check("N2" not in nlf and nlf["N2_first"][0] == "CLEAN"
          and nlf["N2_rest"][1]["entries_2_to_n_gaps"] == [("ctl-01", 1, ["no"])],
          "W10: control D with 1 correct + 1 spurious entry -> N2_first CLEAN, N2_rest reported separately")
    check(nlf["N2_first"][1]["N-W10"] == "not fired", "N-W10 line carried")

    # --- sibling build (APM_011), only when it is present --------------------
    sib = os.path.join(HERE, "..", "anchor-measurand-crossing", "WORK_ORDER.md")
    if os.path.exists(sib):
        a = open(sib, encoding="utf-8").read().rstrip("\n")
        b = order.rstrip("\n")
        check(a == b, "the sibling build's delivered order differs from this one")
        sc = [json.loads(l) for l in open(os.path.join(HERE, "..", "anchor-measurand-crossing",
                                                        "cases.jsonl"), encoding="utf-8") if l.strip()]
        for c in cases[:2]:
            m = [r for r in sc if r["case_id"] == c["case_id"]]
            check(m and all(m[0][k] == c[k] for k in ("claim", "method", "decision", "native")),
                  "%s differs between the two builds" % c["case_id"])

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
