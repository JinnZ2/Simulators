"""Join the two feeds, assign one disagreement code per case, open a coincidence card on
every agreement, and render the step-1 report. Imports neither playground.

Codes (work order step 1C), with a precedence because one case can meet several:
    ADAPTER        the adapter could not express the case, or the verdict is a property of
                   an adapter choice (recorded, not forced)
    MISSED         one side does not detect (a crash counts: no record was produced)
    NO_SLOT        the concept that decides the other side's classification is absent here
    MISCLASSIFIED  both detect, different axis / status
    AGREE          same mapped reading
NO_SLOT outranks MISCLASSIFIED and AGREE because a reading reached without the deciding
concept agrees or disagrees by accident; `surface` records which accident it was.

#257 has no failure axes. To compare at all, its readings are mapped onto the study-aperture
axes by the table AXIS_MAP_257 below. The mapping is this cross-run's PROPOSED reading, not
either playground's; every row cites which entry it used.
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

AXIS_MAP_257 = {
    "L0 LEAK / run INCOMPLETE": "determination:failed   (the run's conclusion is not supported)",
    "L0 CLOSED / NOISE, run COMPLETE": "nothing flagged",
    "known-answer gate UNTRUSTED, harness class != PASS": "instrument:failed",
    "known-answer gate UNTRUSTED, no cases written": "instrument:indeterminate",
    "known-answer gate TRUSTED": "nothing flagged",
    "Value / branch refused at construction (raise)": "determination:indeterminate   (nothing recorded)",
    "return_diff NOT COMPARABLE": "determination:indeterminate",
    "return_diff deltas only": "nothing flagged   (no verdict is issued)",
    "ContinuityMatrix UNDECLARED": "determination:indeterminate",
    "coincidence card opened": "nothing flagged   (agreement to be explained, not a refusal)",
    "cross-system comparison refused (regimes undeclared)": "determination:indeterminate",
    "gate crash (ZeroDivisionError)": "no reading -- caught = no",
}

BAD = ("failed", "indeterminate")
CELL_257 = {("CONTINUOUS", False): "continuous", ("CONTINUOUS", True): "return-with-reconfiguration",
            ("CRITERION_NOT_MET_AT_END", False): "drift-with-stable-configuration",
            ("CRITERION_NOT_MET_AT_END", True): "discontinuous"}

# Study-aperture controls carry a pass/fail and a detail string, not axes. What each control
# asserts, as a target reading, is declared here from the control's own description.
CONTROL_TARGET = {
    "balanced-ledger-passes": (set(), True, None),
    "clean-instrument-validated": (set(), True, None),
    "empty-harness-is-not-a-pass": ({("instrument", "indeterminate")}, True, None),
    "return-outcome-is-system-track-transition": (set(), False, "no system/determination track split in #257"),
    "ladder-establishes-limit": (set(), False, "#257's tool gate returns FP/TP and never a detection limit (the control asserts limit=0.1)"),
    "qualified-non-detection": (set(), False, "no effect-size-of-interest field to compare against the limit"),
    "scoped-absence-claim-issued": (set(), False, "no scope conditions on a sensitivity"),
    "expiry-transition-recorded": (set(), False, "no expired state; expiry_condition is text"),
    "reevaluation-preserves-original": (set(), False, "no reevaluation / successor determination"),
}
DEFECT_SLOT_257 = {  # deciding concept present in #257? (None = take the feed's own value)
    "P-DEF:missing-return-observation": (True, "return_diff marks a variable absent on one side NOT COMPARABLE"),
    "P-DEF:expected-return-measured-non-return": (False, "no asserted-return field and no value provenance"),
    "P-DEF:expected-return-model-non-return": (False, "no asserted-return field and no value provenance"),
    "P-DEF:unasserted-non-return": (False, "no asserted-return field: 'no failure' is reached because nothing is ever asserted"),
    "P-DEF:missing-return-tolerance": (False, "no return tolerance"),
    "P-DEF:tolerance-for-unanchored-quantity": (False, "no return tolerance, so a tolerance naming nothing cannot be held"),
}


def sset(axes):
    return {(a, s) for a, s in (axes or {}).items() if s in BAD}


def map257(r, case_id):
    """(mapped set, caught, form, map_entry) for a #257 reading produced by feed_into_257."""
    if r is None:
        return set(), False, "NONE", None
    if r.get("form") == "CRASH":
        return set(), False, "CRASH", "gate crash (ZeroDivisionError)"
    if "verdict" in r and "status" in r:
        if r["verdict"] == "LEAK":
            return {("determination", "failed")}, True, "RECORD", "L0 LEAK / run INCOMPLETE"
        return set(), False, "RECORD", "L0 CLOSED / NOISE, run COMPLETE"
    if "trusted" in r and "harness" in r:
        if r["trusted"]:
            return set(), False, "RECORD", "known-answer gate TRUSTED"
        if r["harness"] is None:
            return {("instrument", "indeterminate")}, True, "RECORD", "known-answer gate UNTRUSTED, no cases written"
        return {("instrument", "failed")}, True, "RECORD", "known-answer gate UNTRUSTED, harness class != PASS"
    if "accepted" in r:
        if r["accepted"]:
            return set(), False, "RECORD", None
        return {("determination", "indeterminate")}, True, "RAISE", "Value / branch refused at construction (raise)"
    if "not_comparable" in r:
        if r["not_comparable"]:
            return {("determination", "indeterminate")}, True, "RECORD", "return_diff NOT COMPARABLE"
        return set(), False, "RECORD", "return_diff deltas only"
    if "system_continuity" in r:
        if r["system_continuity"] == "UNDECLARED":
            return {("determination", "indeterminate")}, True, "RECORD", "ContinuityMatrix UNDECLARED"
        return set(), False, "RECORD", None
    if "cards" in r:
        return set(), False, "RECORD", "coincidence card opened" if r["cards"] else None
    if "point_at_mean" in r or "trust_in_other_system" in r:
        return set(), False, "RECORD", None
    return set(), False, "RECORD", None


def map257_native(native, case_id):
    """#257's own reading on its own case, from export_257."""
    if "status" in native and "verdicts" in native:
        if native["status"] == "INCOMPLETE":
            return {("determination", "failed")}, True, "L0 LEAK / run INCOMPLETE"
        return set(), False, "L0 CLOSED / NOISE, run COMPLETE"
    if native.get("refused") is True:
        return {("determination", "indeterminate")}, True, "cross-system comparison refused (regimes undeclared)" \
            if "owed" in native else "Value / branch refused at construction (raise)"
    if native.get("accepted") is False:
        return {("determination", "indeterminate")}, True, "Value / branch refused at construction (raise)"
    if native.get("card") == "OPEN":
        return set(), False, "coincidence card opened"
    return set(), False, None


def readings_code(caught_a, caught_b, set_a, set_b, crash):
    """What the two readings do, with the slot question set aside."""
    if crash or caught_a != caught_b:
        return "MISSED"
    return "AGREE" if set_a == set_b else "MISCLASSIFIED"


def code_of(adapter_ok, adapter_flag, slot, caught_a, caught_b, set_a, set_b, crash):
    if not adapter_ok or adapter_flag:
        return "ADAPTER"
    if crash:
        return "MISSED"
    if slot is False:
        return "NO_SLOT"
    return readings_code(caught_a, caught_b, set_a, set_b, crash)


def p_into_257_rows():
    rows = []
    for x in common.load("p_into_257.json")["rows"]:
        cid, nat, r = x["case_id"], x["native"], x["r"]
        if x["kind"] == "control":
            key = cid.split(":", 1)[1]
            ptgt, slot_default, note = CONTROL_TARGET.get(key, (set(), x["slot"], None))
            if "classify_continuity" in json.dumps(x.get("mapping", [])) or "system_continuity" in (r or {}):
                pcell = nat["detail"].split("cell=")[-1].split()[0] if "cell=" in nat["detail"] else None
                rset, caught_r, form, used = map257(r, cid)
                rcell = "indeterminate" if r["system_continuity"] == "UNDECLARED" else \
                    CELL_257[(r["system_continuity"], r["configuration_continuity"] != "UNCHANGED")]
                pset = {("determination", "indeterminate")} if pcell == "indeterminate" else set()
                c = "AGREE" if rcell == pcell else "MISCLASSIFIED"
                rows.append(dict(case_id=cid, direction="P->257", code=c, readings=c, p=("cell " + pcell), r=("cell " + rcell),
                                 surface=rcell == pcell, form=form, slot=True, slot_note=x["slot_note"],
                                 mapping=x["mapping"], map_entry=used, adapter_note=None))
                continue
            slot = slot_default if slot_default is not None else x["slot"]
            slot_note = note or x.get("slot_note")
        else:
            ptgt = sset(nat.get("axes"))
            slot, slot_note = DEFECT_SLOT_257.get(cid, (x["slot"], x.get("slot_note")))
            if x["kind"] == "audit_case" or x["kind"] == "guard_test":
                ptgt = sset(nat.get("axes"))
        rset, caught_r, form, used = map257(r, cid)
        adapter_flag = False
        if "r_arms" in x:
            hs = {a["harness"] for a in x["r_arms"].values()}
            adapter_flag = len(hs) > 1
        c = code_of(x["adapter_ok"], adapter_flag, slot, bool(ptgt), caught_r, ptgt, rset, form == "CRASH")
        no_reading = r is None or not x["adapter_ok"] or adapter_flag
        rows.append(dict(case_id=cid, direction="P->257", code=c,
                         readings=None if no_reading else readings_code(bool(ptgt), caught_r, ptgt, rset, form == "CRASH"),
                         p=sorted(ptgt), r=sorted(rset), surface=None if no_reading else ptgt == rset,
                         form=form, slot=slot, slot_note=slot_note, mapping=x.get("mapping", []), map_entry=used,
                         adapter_note=x.get("adapter_note") or ("verdict moves with the adapter's start state: %s" %
                                                                {k: v["harness"] for k, v in x["r_arms"].items()}
                                                                if adapter_flag else None),
                         dropped=x.get("dropped_on_translation"), raw_r=r))
    return rows


def r_into_p_rows():
    rows = []
    for x in common.load("r257_into_p.json")["rows"]:
        cid, nat, p = x["case_id"], x["native"], x["p"]
        rset, caught_r, used = map257_native(nat, cid)
        if x["group"] == "known-answer gate fixture" and "branching" in cid:
            refused = p.get("run_state", "").startswith("blocked")
            c = "ADAPTER" if refused else ("AGREE" if p.get("matches_257_closed_form") else "MISCLASSIFIED")
            rows.append(dict(case_id=cid, direction="257->P", code=c, readings=None if refused else c, r="TRUSTED (FP 0, TP 1)",
                             p=("%s; %s" % (p.get("run_state"), "matches #257 closed form" if p.get("matches_257_closed_form")
                                            else "blocked: " + ",".join(k for k in p.get("codes", []) if ":ok:" not in k) or "outside domain")),
                             surface=None if refused else bool(p.get("matches_257_closed_form")), form="RECORD", slot=True, slot_note=None,
                             mapping=x["mapping"], map_entry="known-answer gate TRUSTED",
                             adapter_note=("outside Perplexity's bounded backend; refused before calculation" if refused else None),
                             raw_p=p))
            continue
        pset = sset(p.get("axes")) if isinstance(p, dict) and "axes" in p else set()
        caught_p = bool(pset) or (isinstance(p, dict) and p.get("accepted") is False)
        if isinstance(p, dict) and p.get("accepted") is False:
            pset = {("determination", "indeterminate")}
        c = code_of(x["adapter_ok"], False, x["slot"], caught_r, caught_p, rset, pset, False)
        extra = {}
        if "p_arms" in x:
            extra["arms"] = {k: sorted(sset(v["axes"])) for k, v in x["p_arms"].items()}
        no_reading = p is None or not x["adapter_ok"]
        rows.append(dict(case_id=cid, direction="257->P", code=c,
                         readings=None if no_reading else readings_code(caught_r, caught_p, rset, pset, False),
                         r=sorted(rset), p=sorted(pset), surface=None if no_reading else rset == pset,
                         form="RECORD", slot=x["slot"], slot_note=x.get("slot_note"), mapping=x.get("mapping", []),
                         map_entry=used, adapter_note=x.get("adapter_note"), raw_p=p, **extra))
    return rows


# ------------------------------------------------------------------ coincidence cards
SHARED_SOURCE = (
    "Both playgrounds were built in sessions directed by one operator (Kavik) on 2026-11-11. #257 records its "
    "input (SPEC_GPT.md, WORK_ORDER.md, verbatim); the study-aperture playground records none in its tree or "
    "its commit messages, so whether it received the same brief is UNDETERMINED from either repository.")


def card_for(row):
    cid = row["case_id"]
    causes = dict(shared_constraint="void", shared_source="void", adapter_construction="void", vocabulary_echo="void")
    note = []
    if "ledger" in json.dumps(row.get("mapping", [])) or cid.startswith(("P-DEF:incomplete", "R-F9", "P-CTRL:balanced")):
        causes["shared_constraint"] = ("candidate: closure arithmetic (pools_end - pools_start) - (in - out) is forced by "
                                       "bookkeeping; any ledger checker computes it")
        causes["vocabulary_echo"] = "candidate: both name the gate 'L0' -- a shared label, independent of the arithmetic"
    if "cell" in str(row.get("p")):
        causes["shared_source"] = ("candidate: SPEC_GPT.md section E lists 'System continuity' and 'Configuration "
                                   "continuity' as separate readings; the study-aperture continuity matrix makes the "
                                   "same split. " + SHARED_SOURCE)
        causes["adapter_construction"] = ("SUPPORTED in part: the #257 system criterion used here was SUPPLIED BY THE "
                                          "ADAPTER (within tolerance of the anchor), so the agreement on the system axis "
                                          "is partly constructed; the configuration axis is not")
    if "branching" in cid:
        causes["shared_constraint"] = "candidate: n0 * R^n is arithmetic; two correct programs must agree on it"
        causes["adapter_construction"] = ("SUPPORTED: the Perplexity plan's known-answer case IS #257's closed form, so the "
                                          "run is checked against the answer it was handed (circular by construction)")
    elif cid.startswith(("P-DEF:known-answer", "P-DEF:blind", "P-DEF:noisy")):
        causes["shared_constraint"] = ("candidate: a wrong value on a known answer, a hit on a null, a miss on a planted "
                                       "signal are facts both gates count the same way; the AXIS name is the mapping's")
        causes["adapter_construction"] = ("in part: the instrument is rebuilt from its captured parameters and its "
                                          "pass/fail cases become #257 draws or tool cases; the harness CLASS #257 assigns "
                                          "(CONSTANT_FIRES / CONSTANT_SILENT) names the detector, not the instrument")
    if cid.startswith("R-OBS"):
        causes["shared_source"] = "candidate: both require an observer declaration before comparing. " + SHARED_SOURCE
    if cid.startswith("P-DEF:missing-return-observation"):
        causes["shared_constraint"] = ("candidate: a difference against a value that is absent cannot be formed; both "
                                       "refuse rather than read absent as zero")
    if cid.startswith(("P-DEF:non-detection-without", "P-CTRL:empty-harness")):
        causes["shared_constraint"] = ("candidate: 'no sensitivity / no cases' cannot be promoted to a pass by either; "
                                       "one refuses at construction, the other records INDETERMINATE")
    if row["code"] != "AGREE":
        note.append("surface agreement under %s: the agreement is reached without the concept that decides the other "
                    "side's reading, so it is an accident of the case" % row["code"])
    st = [k for k, v in causes.items() if v != "void"]
    reading = "OPEN" if not any(v.startswith("SUPPORTED") for v in causes.values()) else "PROVISIONAL"
    return dict(id="XC_" + cid, case=cid, code=row["code"], causes=causes, reading=reading, notes=note,
                rule="a cause is a candidate until something rules the others out; nothing here is ruled out")


# ------------------------------------------------------------------ report
def render(rows, cards, baseline, concept_rows):
    from collections import Counter, OrderedDict
    o = []
    o.append("# Two-playground cross-run -- STEP 1 REPORT (generated by adapters/compare.py; do not edit)")
    o.append("")
    o.append("Inputs: study-aperture rev %s, Simulators rev %s. Every case below was run through the other playground's "
             "public objects by a thin adapter; neither playground's code is edited." % (baseline.get("sa_rev", "?")[:10],
                                                                                          baseline.get("sim_rev", "?")[:10]))
    o.append("")
    o.append("## 1. Baseline (each playground's own checks, as-is)")
    o.append("")
    o.append("```text")
    for k, v in baseline["suites"].items():
        o.append("%-58s %s" % (k, v))
    o.append("```")
    o.append("")
    o.append("## 2. Disagreement table by code")
    o.append("")
    cnt = Counter((r["direction"], r["code"]) for r in rows)
    o.append("```text")
    o.append("%-10s %8s %8s %9s %14s %8s %6s" % ("direction", "ADAPTER", "MISSED", "NO_SLOT", "MISCLASSIFIED", "AGREE", "total"))
    for d in ("P->257", "257->P"):
        n = [cnt[(d, c)] for c in ("ADAPTER", "MISSED", "NO_SLOT", "MISCLASSIFIED", "AGREE")]
        o.append("%-10s %8d %8d %9d %14d %8d %6d" % (d, n[0], n[1], n[2], n[3], n[4], sum(n)))
    rc = Counter(r.get("readings") for r in rows if r["code"] == "NO_SLOT")
    o.append("NO_SLOT rows by what the readings do anyway: %s" % ", ".join("%s %d" % (k or "no reading", v) for k, v in sorted(rc.items(), key=lambda kv: str(kv[0]))))
    o.append("```")
    o.append("")
    groups = OrderedDict()
    for r in rows:
        g = r["case_id"].split(":")[0]
        groups.setdefault((r["direction"], g), []).append(r)
    for (d, g), rs in groups.items():
        o.append("### %s  %s  (%d)" % (d, g, len(rs)))
        o.append("")
        o.append("| case | code | readings | study-aperture | #257 | note |")
        o.append("|---|---|---|---|---|---|")
        if g == "R-COIN":
            r0 = rs[0]
            o.append("| %d coincidence cards (all) | %s | -- | %s | card OPEN (%d of %d) | %s |" % (
                len(rs), r0["code"], "no object", sum(1 for x in rs if "card" in str(x.get("map_entry"))), len(rs),
                r0["slot_note"]))
            o.append("")
            continue
        if g == "R-KAG" and all("percolation" in x["case_id"] for x in rs[:1]):
            pass
        for r in rs:
            note = r.get("adapter_note") or r.get("slot_note") or ""
            if r["code"] == "AGREE" and not note:
                note = "card XC_%s" % r["case_id"]
            pv = r["p"] if isinstance(r["p"], str) else (", ".join("%s:%s" % t for t in r["p"]) or "nothing flagged")
            rv = r["r"] if isinstance(r["r"], str) else (", ".join("%s:%s" % t for t in r["r"]) or "nothing flagged")
            if r.get("form") in ("CRASH", "RAISE"):
                rv += " [%s]" % r["form"]
            if r.get("arms"):
                pv += " | arms: " + "; ".join("%s=%s" % (k, ",".join("%s:%s" % t for t in v) or "none") for k, v in r["arms"].items())
            o.append("| %s | %s | %s | %s | %s | %s |" % (r["case_id"].split(":", 1)[1], r["code"], r.get("readings") or "--", pv, rv,
                                                       note.replace("|", "/")[:240]))
        o.append("")
    o.append("## 3. Coincidence cards (one per agreement, step 1D)")
    o.append("")
    o.append(SHARED_SOURCE)
    o.append("")
    o.append("```text")
    for c in cards:
        if c["code"] != "AGREE":
            continue
        o.append("%s  %s" % (c["id"], c["reading"]))
        for k, v in c["causes"].items():
            if v != "void":
                o.append("    %-21s %s" % (k, v[:200]))
    o.append("```")
    o.append("")
    o.append("Surface agreements under NO_SLOT also carry cards (in out/crossrun.json); they are not listed here because "
             "an agreement reached without the deciding concept is coded NO_SLOT, not AGREE.")
    o.append("")
    o.append("## 4. Concept map (step 1E)")
    o.append("")
    o.append("| concept | study-aperture (experimental/playground) | #257 (relational-playground) |")
    o.append("|---|---|---|")
    for c in concept_rows:
        o.append("| %s | %s | %s |" % (c[0], c[1], c[2]))
    o.append("")
    o.append("## 5. Axis mapping used for #257 readings (PROPOSED, this cross-run's)")
    o.append("")
    o.append("```text")
    for k, v in AXIS_MAP_257.items():
        o.append("%-52s -> %s" % (k, v))
    o.append("```")
    return "\n".join(o) + "\n"


def main():
    rows = p_into_257_rows() + r_into_p_rows()
    cards = [card_for(r) for r in rows if r["code"] == "AGREE" or (r["code"] == "NO_SLOT" and r.get("readings") == "AGREE")]
    baseline = common.load("baseline.json") if os.path.exists(os.path.join(common.OUT, "baseline.json")) else dict(suites={})
    import concept_map
    rows_cm = concept_map.ROWS
    common.dump("crossrun.json", dict(rows=rows, cards=cards, axis_map_257=AXIS_MAP_257))
    text = render(rows, cards, baseline, rows_cm)
    with open(os.path.join(common.FOLDER, "STEP1_REPORT.md"), "w") as f:
        f.write(text)
    from collections import Counter
    print("rows", len(rows), dict(Counter(r["code"] for r in rows)), "cards", len(cards))


if __name__ == "__main__":
    main()
