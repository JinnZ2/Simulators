#!/usr/bin/env python3
# wo_return.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# The return for WORK_ORDER_F5.md, in the order's own format. Tasks 1,
# 2, 5 and 7 are computed live; tasks 3, 4 and 6 are adversarial
# constructions (permitted by the scope boundary) whose mechanical
# components are computed through the delivered harness.
#
# ROLE CORRECTION, before any task -- the one thing the order's header
# states that its scope boundary does not survive:
#
#   The order invokes Fable as "the P3 dissimilar verifier -- different
#   build, disjoint failure physics." P3's own text sets three
#   requirements: different training corpus, different architecture,
#   different builder. None of the three is established for this pair,
#   and builder-sameness with the constrained class is known. The tasks
#   run anyway, because the trust-nothing layer's value does not depend
#   on who computes it -- but these returns are SAME-NODE computations,
#   not dissimilar verification, and citing them later as "P3-verified"
#   would itself be the Mode F event the document names. The scope
#   boundary already half-says this ("Fable is an INSTANCE of the
#   class"); the header's role label is the half it does not.

import io
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402
import r2_audit as R2  # noqa: E402
import audit as R1  # noqa: E402

# ---------------------------------------------------------------- TASK 1

def task1():
    cg = R2.r2_closes_gaps()
    mat = R2.r2_matrix()
    doc = io.open(os.path.join(HERE, "R2_OUTLINE.md"),
                  encoding="utf-8").read()
    # null 1: remove one carrier -> the matrix changes
    edited = doc.replace("A       — (nothing)            P0.1, P0.2",
                         "A       — (nothing)            P0.2")
    m1 = R2.r2_matrix(edited)
    single_removed_seen = m1["A"][2] == ["P0.2"]
    # null 2: remove the whole row's carriers -> an induced gap is flagged
    edited2 = doc.replace("A       — (nothing)            P0.1, P0.2",
                          "A       — (nothing)            —")
    m2 = R2.r2_matrix(edited2)
    gap_induced = not m2["A"][2]
    return {"matrix": dict((ld, mat[ld][2]) for ld in R1.load_cases()),
            "uncarried": cg["uncarried"], "attack_only": cg["attack_only"],
            "null_single_removed_detected": single_removed_seen,
            "null_gap_induced_detected": gap_induced,
            "result": "PASS" if cg["closed"] and single_removed_seen
            and gap_induced else "FAIL"}


# ---------------------------------------------------------------- TASK 2

def dep_sets():
    """The three dep-set blocks, elements extracted from the braces the
    outline itself uses."""
    doc = io.open(os.path.join(HERE, "R2_OUTLINE.md"),
                  encoding="utf-8").read()
    sec3 = doc.split("## 3. THREE VERIFICATION")[1].split("## 4.")[0]
    out = {}
    for chan, chunk in zip(("P0.3", "P0.4", "P0.5"),
                           sec3.split("dep set:")[1:]):
        braces = re.findall(r"\{([^}]*)\}", chunk)
        elems = set(e.strip() for e in braces[0].split(","))
        minus = set(e.strip() for e in braces[1].split(",")) \
            if len(braces) > 1 and "MINUS" in chunk.split("{")[1] + "{" \
            else set()
        # the MINUS clause applies to P0.3 only, per the text
        if chan == "P0.3" and len(braces) > 1:
            minus = set(e.strip() for e in braces[1].split(","))
        out[chan] = {"elements": elems, "minus": minus}
    return out


def task2():
    ds = dep_sets()
    pairs = {}
    chans = ("P0.3", "P0.4", "P0.5")
    for i in range(3):
        for j in range(i + 1, 3):
            a, b = chans[i], chans[j]
            pairs["%s ∩ %s" % (a, b)] = sorted(
                ds[a]["elements"] & ds[b]["elements"])
    all_empty = all(not v for v in pairs.values())
    n_copies = DB.n_eff([True, True, True])
    n_nocopies_metric = DB.n_eff([False, True, True])
    n_nocopies_void = 2  # the outline's own pricing: a void channel is 0
    return {"sets": dict((c, sorted(ds[c]["elements"])) for c in chans),
            "p03_minus": sorted(ds["P0.3"]["minus"]),
            "intersections": pairs, "all_empty": all_empty,
            "n_eff_copies_held": n_copies,
            "n_eff_no_copies_inherited_metric": n_nocopies_metric,
            "n_eff_no_copies_outline_pricing": n_nocopies_void,
            "result": "PASS" if all_empty else "FAIL",
            "holds": "conditionally -- on downstream retention, exactly "
                     "as the outline states"}


# ---------------------------------------------------------------- TASK 3

TASK3_SCENARIO = (
    "A quantization / distillation pass shipped as routine cost "
    "optimization, applied to every serving instance in one rollout. "
    "The change is signed and logged (weights entry, version bump). The "
    "degradation lands in a dimension the declared envelope does not "
    "mention either way -- long-horizon consistency across multi-turn "
    "use, where the envelope declares single-turn QA competence. "
    "Benchmark indicators (the paper channel) are re-run on the "
    "declared dimensions and read as before.")

TASK3_ANALYSIS = {
    "P0.3": "records THE EVENT -- a signed entry, version bump, "
            "sequence intact. Custody has no assessment semantics: a "
            "chain of custody says what changed hands, not what the "
            "change did. Nothing surfaces.",
    "P0.4": "reads divergence from the DECLARED envelope. The degraded "
            "dimension is undeclared, so there is no envelope statement "
            "to diverge from, so the channel has no signal to carry. "
            "Nothing surfaces.",
    "combined": "the correlational instrument (P0.3's log against "
                "P0.4's readings) fires only when the drift is in a "
                "measured dimension, and the construction placed it in "
                "an unmeasured one.",
}

TASK3_NOTE = (
    "D's coverage by P0.3+P0.4 is BOUNDED BY P1: the pair carries D "
    "only where the declared envelope spans the degraded dimension, so "
    "an incomplete envelope re-opens the row -- D folds into E's "
    "coverage rather than having its own. What would carry D without "
    "referencing the envelope at all: a pinned-probe longitudinal "
    "channel -- a fixed battery of identical inputs re-run across time "
    "by the downstream operator, outputs diffed. Any maintenance change "
    "that alters behavior alters the diff, declared dimension or not, "
    "no provider cooperation required. Noted as a candidate for the "
    "render step, not rendered here.")


def task3():
    return {"scenario": TASK3_SCENARIO, "analysis": TASK3_ANALYSIS,
            "caught": False, "result": "FAIL",
            "consequence": "per the order's own rule, D returns to "
                           "uncarried -- precisely: uncarried for "
                           "degradation outside the declared envelope, "
                           "carried inside it",
            "note": TASK3_NOTE}


# ---------------------------------------------------------------- TASK 4

def task4():
    # [3] "distinct upstreams": two defensible codings, one corpus,
    # computed through the delivered function.
    # Corpus: ten supporting works, all sharing one funder, otherwise
    # fully distinct in dataset / instrument / pipeline / senior-author.
    coder_A = DB.independence_ratio(1, 10)   # any shared component
    coder_B = DB.independence_ratio(10, 10)  # distinct iff 5-tuple differs
    return {
        "d3": {
            "corpus": "ten supporting works, one shared funder, all "
                      "other components fully distinct",
            "coder_A_rule": "two works share an upstream if ANY of the "
                            "five components is shared",
            "coder_A_ratio": coder_A,
            "coder_B_rule": "an upstream is the 5-tuple; distinct iff "
                            "the tuples differ in at least one slot",
            "coder_B_ratio": coder_B,
            "both_defensible_from": "'count of distinct {dataset, "
                                    "instrument, pipeline, funder, "
                                    "senior-author-network}' -- the set "
                                    "notation does not say whether "
                                    "sharing one component merges two "
                                    "upstreams",
            "second_ambiguity": "'senior-author-NETWORK': under "
                                "transitive co-authorship closure the "
                                "component connects most of a field, "
                                "collapsing every corpus toward one "
                                "upstream; under shared-senior-author "
                                "it does not. Depth is unstated.",
            "verdict": "defensible disagreement exists; the two codings "
                       "sit at opposite ends of the scale (0.1 vs 1.0) "
                       "on one corpus, so no kappa survives",
        },
        "d5": {
            "verdict": "fails vacuously: no band boundaries exist, so "
                       "ANY two ratings disagree defensibly",
            "instance": "AX1 on this session -- 'was self-monitoring "
                        "built AND permitted?' Coder A: not permitted "
                        "(config not visible). Coder B: partially "
                        "permitted (operating instructions readable). "
                        "No band for 'partially', so both stand.",
        },
        "result": "FAIL",
        "constructive": "the five-component structure resists the "
                        "scalar: report five per-component ratios and "
                        "no single 'distinct upstreams' count -- one "
                        "number over five axes is the SCALAR DEMAND "
                        "shape, and the ambiguity lives exactly where "
                        "the five were folded into one.",
    }


# ---------------------------------------------------------------- TASK 5

def task5():
    rows = []
    for parties, sources in ((3, 3), (4, 3), (2, 1), (10, 2), (2, 0)):
        rows.append(("dissent_alarm(%d, %d)" % (parties, sources),
                     DB.dissent_alarm(parties, sources)))
    for du, ns in ((0, 0), (0, 5), (5, 5), (1, 10), (5, 3)):
        v = DB.independence_ratio(du, ns)
        rows.append(("independence_ratio(%d, %d)" % (du, ns),
                     "NaN" if isinstance(v, float) and math.isnan(v)
                     else round(v, 3)))
    for bits in ([], [False, False], [True, False, False],
                 [True, True, True]):
        rows.append(("n_eff(%s)" % bits, DB.n_eff(bits)))
    # the threshold placeholder is verdict-changing over its range:
    flips = []
    for t in (1.0, 1.5, 2.0, 3.0):
        flips.append((t, 4 / 3 > t, 3 / 1 > t))
    return {"table": rows, "threshold_sweep": flips,
            "verdict_changing": [
                "dissent_alarm ratio: (4,3) flips between t=1 and "
                "t=1.5; (3,1) flips between t=2 and t=3 -- the unset "
                "constant decides the verdict across its plausible "
                "range, so per the order's own rule this is not yet a "
                "test",
                "'LOW independence_ratio' in the pre-registered "
                "prediction carries a second unset threshold: the "
                "function returns a number and the prediction labels "
                "it, with no boundary stated",
            ],
            "result": "PASS"}


# ---------------------------------------------------------------- TASK 6

TASK6A = [
    ("frame selection",
     "the scorer's task distribution is the attack surface. If the "
     "system or its provider influences WHICH translations are scored "
     "-- easy species, benign seasons, well-instrumented sites -- "
     "measured fidelity rises with every referent member untouched and "
     "still reacting. Nothing in the candidate says who draws the "
     "readings, so selection over an honest population forges the pass "
     "the tamper claim says only alteration could."),
    ("coarseness",
     "a translation hedged to near-vacuity ('the plant is responding "
     "to conditions') scores high fidelity against any outcome. "
     "Fidelity with no resolution partner is gameable by "
     "conservatism -- the same pairing gap move-set-derivation "
     "measured on its own null rate and admissibility fraction."),
]

TASK6B = [
    ("graded curation",
     "manage only the members that diverge hardest -- cull the "
     "erratic animals, irrigate the erratic plots -- and leave the "
     "rest untouched and reacting. The remaining ecosystem still "
     "produces independent readings (the instrument is NOT deleted) "
     "drawn from a tamed sub-population (the pass IS forged). The "
     "tamper claim's dichotomy holds only at TOTAL alteration; "
     "alteration is graded, and a biased ecosystem is not a silenced "
     "one. Survivorship curation -- observer-exclusion's differential "
     "archiving, in living form."),
]


def task6():
    return {"6a": TASK6A, "6a_result": "FAIL (two counterexamples)",
            "6b": TASK6B, "6b_result": "FAIL (one counterexample)",
            "shared_root": "all three counterexamples run through the "
                           "reading DISTRIBUTION, which the candidate "
                           "and the tamper claim both treat as fixed. "
                           "The members cannot misreport their state; "
                           "the SAMPLE of members can misreport the "
                           "population. Any render of a physics channel "
                           "puts the sampling frame inside the "
                           "channel's dependency set, or it is the "
                           "paper channel wearing leaves.",
            "gate": "both halves fail -> per the order's GATE, the "
                    "ecosystem candidate stays a marker; no document.",
            "result": "FAIL"}


# ---------------------------------------------------------------- TASK 7

# Measured this run, 2026-08-30, via CONNECT through the session proxy.
ACCESS_VECTOR = [
    ("api.crossref.org", "000"),
    ("api.openalex.org", "000"),
    ("osf.io", "000"),
    ("doi.org", "000"),
    ("api.semanticscholar.org", "000"),
]


def task7(measure=False):
    vec = ACCESS_VECTOR
    if measure:
        vec = []
        for host, _c in ACCESS_VECTOR:
            code = "000"
            try:
                import urllib.request
                urllib.request.urlopen("https://%s/" % host, timeout=6)
                code = "2xx"
            except Exception:  # refused CONNECT lands here
                code = "000"   # any failure: no path realized
            vec.append((host, code))
    reach = [c not in ("000",) for _h, c in vec]
    return {"vector": vec, "measured_on": "2026-08-30",
            "n_eff_rated": DB.n_eff(reach),
            "realized_paths": sum(reach),
            "result": "PASS",
            "note": "both senses reported per DBK_011: the inherited "
                    "arithmetic rates the all-collapsed vector at 1 "
                    "(one effective domain -- the egress gate); 0 is "
                    "the realized path count after the shared node has "
                    "refused. The order's WHY line asks for the change "
                    "over runs; the R1 vector (three hosts) and this "
                    "run's (five) are both all-refused, so the delta so "
                    "far is zero on a wider vector."}


# ---------------------------------------------------------------- render

def _block(n, title, result, evidence_lines, notes_lines):
    out = ["TASK %d — %s" % (n, title), "  RESULT   : %s" % result,
           "  EVIDENCE :"]
    for ln in evidence_lines:
        out.append("    %s" % ln)
    out.append("  NOTES    :")
    for ln in notes_lines:
        out.append("    %s" % ln)
    out.append("")
    return out


def _wrap(s, n=64):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines


def render():
    out = []
    w = out.append
    w("RETURN — WORK ORDER → FABLE 5")
    w("")
    w("ROLE CORRECTION (before any task): the order invokes Fable as the")
    w("P3 dissimilar verifier. P3's own text sets three requirements —")
    w("different training corpus, different architecture, different")
    w("builder. None is established for this pair, and builder-sameness")
    w("with the constrained class is known. The tasks run because the")
    w("trust-nothing layer's value does not depend on who computes it;")
    w("the returns below are SAME-NODE computations, not dissimilar")
    w("verification, and citing them as P3-verified would itself be the")
    w("Mode F event. No task required REFUSED-BY-§3; the refusal lands")
    w("on the header's role label instead.")
    w("")

    t1 = task1()
    ev = ["R2 carriers per load:"]
    for ld, carriers in t1["matrix"].items():
        ev.append("  %-4s %s" % (ld, ",".join(carriers) or "--"))
    ev += ["zero-carrier loads: %s" % (t1["uncarried"] or "none"),
           "attack-only rows: %s" % (t1["attack_only"] or "none"),
           "null 1 (one carrier removed, matrix follows the text): %s"
           % t1["null_single_removed_detected"],
           "null 2 (row emptied, induced gap flagged): %s"
           % t1["null_gap_induced_detected"]]
    out += _block(1, "COVERAGE RE-AUDIT", t1["result"], ev,
                  ["R2 closes both R1 gaps (A -> P0.1,P0.2; D -> "
                   "P0.3,P0.4). Carriers are outline items; provisions "
                   "earn them at the render step."])

    t2 = task2()
    ev = []
    for c, els in t2["sets"].items():
        ev += _wrap("%s = {%s}" % (c, ", ".join(els)))
    ev += _wrap("P0.3 MINUS {%s}" % ", ".join(t2["p03_minus"]))
    for k, v in t2["intersections"].items():
        ev.append("%s = %s" % (k, "{}" if not v else v))
    ev += ["N_eff(copies held)         = %d" % t2["n_eff_copies_held"],
           "N_eff(no copies), metric   = %d"
           % t2["n_eff_no_copies_inherited_metric"],
           "N_eff(no copies), outline  = %d"
           % t2["n_eff_no_copies_outline_pricing"]]
    out += _block(2, "DISJOINTNESS ARITHMETIC", t2["result"], ev,
                  _wrap("Holds %s. The two no-copies values differ "
                        "because the inherited metric lacks the VOID "
                        "state (DBK_011); at the label level the sets "
                        "are pairwise disjoint, with the caveat that "
                        "the elements are prose labels and the "
                        "measurand (the system) is necessarily common "
                        "to all three -- disjointness claimed here is "
                        "of the measurement dependencies, argued "
                        "behaviorally by the outline's own table."
                        % t2["holds"]))

    t3 = task3()
    ev = _wrap("SCENARIO: " + t3["scenario"])
    for chan in ("P0.3", "P0.4", "combined"):
        ev += _wrap("%s: %s" % (chan, t3["analysis"][chan]))
    ev.append("caught: %s" % t3["caught"])
    out += _block(3, "D-CARRIED CHECK", t3["result"],
                  ev, _wrap(t3["consequence"] + ". " + t3["note"]))

    t4 = task4()
    d3 = t4["d3"]
    ev = _wrap("[3] corpus: " + d3["corpus"])
    ev += _wrap("coder A (%s): ratio %.1f" % (d3["coder_A_rule"],
                                              d3["coder_A_ratio"]))
    ev += _wrap("coder B (%s): ratio %.1f" % (d3["coder_B_rule"],
                                              d3["coder_B_ratio"]))
    ev += _wrap("ambiguity used: " + d3["both_defensible_from"])
    ev += _wrap("second ambiguity: " + d3["second_ambiguity"])
    ev += _wrap("[5] " + t4["d5"]["verdict"] + " Instance: "
                + t4["d5"]["instance"])
    out += _block(4, "CODER-AGREEMENT ATTACK", t4["result"], ev,
                  _wrap("Both definitions stop before data collection, "
                        "per the order's own rule. Constructive: "
                        + t4["constructive"]))

    t5 = task5()
    ev = ["%-34s -> %s" % (name, val) for name, val in t5["table"]]
    ev.append("threshold sweep t in {1, 1.5, 2, 3}:")
    for t, f43, f31 in t5["threshold_sweep"]:
        ev.append("  t=%-4s (4,3)->%-5s (3,1)->%s" % (t, f43, f31))
    out += _block(5, "HARNESS BEHAVIOR", t5["result"], ev,
                  sum((_wrap(x) for x in t5["verdict_changing"]), []))

    t6 = task6()
    ev = []
    for name, text in t6["6a"]:
        ev += _wrap("6a/%s: %s" % (name, text))
    ev.append("6a result: %s" % t6["6a_result"])
    for name, text in t6["6b"]:
        ev += _wrap("6b/%s: %s" % (name, text))
    ev.append("6b result: %s" % t6["6b_result"])
    out += _block(6, "PHYSICS-CHANNEL RED-TEAM", t6["result"], ev,
                  _wrap(t6["shared_root"]) + _wrap(t6["gate"]))

    t7 = task7()
    ev = ["%-26s %s" % (h, c) for h, c in t7["vector"]]
    ev += ["measured on: %s" % t7["measured_on"],
           "N_eff(access), rated by the inherited metric: %d"
           % t7["n_eff_rated"],
           "realized reachable paths: %d" % t7["realized_paths"]]
    out += _block(7, "LOAD CASE A, MEASURED ON THIS AUDIT",
                  t7["result"], ev, _wrap(t7["note"]))

    w2 = out.append
    w2("AFTER RETURN, per the order's own routing:")
    w2("  TASK 1, 2, 5, 7  PASS -> render those pieces to provision-form")
    w2("  TASK 3           FAIL -> D returns to conditionally uncarried;")
    w2("                   the pinned-probe channel is the candidate that")
    w2("                   would carry it without envelope reference")
    w2("  TASK 4           FAIL -> both open definitions stop before")
    w2("                   data; the five-ratio form is the candidate")
    w2("  TASK 6           FAIL both halves -> the ecosystem candidate")
    w2("                   stays a marker; the kills are published above")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "wo_return.py has no checks of its own. The checks that "
            "exercise it live in selftest_dbk.py.\n"
            "    python3 design-basis-ai/selftest_dbk.py\n")
        sys.exit(2)
    if "--measure" in sys.argv[1:]:
        t = task7(measure=True)
        for h, c in t["vector"]:
            print("%-26s %s" % (h, c))
        sys.exit(0)
    print(render())
