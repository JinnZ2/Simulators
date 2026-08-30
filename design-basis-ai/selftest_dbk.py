#!/usr/bin/env python3
# selftest_dbk.py -- CC0, stdlib only, parses under 3.9
#
# Every check that exercises the delivered design_basis_checks.py and
# the audit. The delivered file is landed verbatim and not edited.
#
# The load-bearing checks: the coverage matrix's uncarried load is
# COMPUTED and the computation can fail (a constructed doc with A
# carried comes back covered); the n_eff equivalence sweep against the
# sibling's instrument is exhaustive to length 8; and the posture --
# class-level certification declined by the document's own Section 3 --
# is asserted to be stated in the report rather than assumed.

import io
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import design_basis_checks as DB  # noqa: E402
import audit as A  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    doc = io.open(os.path.join(HERE, "SOURCE_DROP.md"),
                  encoding="utf-8").read()

    # ---- the delivered harness is verbatim from Section 4
    src = io.open(os.path.join(HERE, "design_basis_checks.py"),
                  encoding="utf-8").read()
    chk("the delivered harness appears verbatim in the drop",
        src.strip() in doc)
    chk("no --selftest handling was added to the delivered file",
        "--selftest" not in src)

    # ---- the parse: 8 provisions, complete fields, 7 loads
    provs = A.provisions()
    chk("eight provisions parse", sorted(provs) ==
        ["P%d" % i for i in range(1, 9)])
    for p in sorted(provs):
        for f in A.FIELDS:
            chk("%s has %s" % (p, f), f in provs[p])
    chk("P6 carries the extra RATIONALE field", "RATIONALE" in provs["P6"])
    chk("seven load cases parse",
        A.load_cases() == ["A", "B1", "B2", "C", "D", "E", "F"])

    # the parser can fail: a constructed provision missing FALSIFY
    fake = ('### P1 — X\n```\nPROVISION  a\nCARRIES    E. b\n'
            'VERIFY     c\n```\n')
    fp = A.provisions(fake)
    chk("the parser reports a missing field rather than inventing one",
        "FALSIFY" not in fp["P1"])

    # ---- THE COVERAGE MATRIX, and its null
    cov = A.coverage()
    chk("load case A is carried by no provision",
        cov["uncarried"] == ["A"])
    chk("D is attacked-only", cov["attacked_only"] == ["D"])
    chk("E is carried three times and attacked once",
        cov["carried"]["E"] == ["P1", "P5", "P6"]
        and cov["attacked"]["E"] == ["P3"])
    chk("F is carried by P2, P7, P8",
        cov["carried"]["F"] == ["P2", "P7", "P8"])
    chk("B2 is carried by P3 and P4 (the governing load has provisions)",
        cov["carried"]["B2"] == ["P3", "P4"])
    # null: a constructed doc where A IS carried comes back covered,
    # so the uncarried finding is a property of the delivered text
    fake2 = doc.replace("CARRIES    E. an undeclared envelope",
                        "CARRIES    A, E. an undeclared envelope")
    cov2 = A.coverage(fake2)
    chk("the uncarried finding CAN fail (a doc carrying A reads covered)",
        cov2["uncarried"] == [])

    # ---- the delivered n_eff vs the sibling's, exhaustively
    eq = A.n_eff_equivalence()
    chk("the sweep is exhaustive to length 8 (511 lists)",
        eq["lists"] == 511)
    chk("zero disagreements with the sibling instrument",
        eq["mismatches"] == 0)
    chk("the zero-channel edge recurs in the second delivery",
        eq["zero_channel_edge_recurs"] and DB.n_eff([]) == 0)
    # the sibling is imported, not copied, in the audit
    asrc = io.open(os.path.join(HERE, "audit.py"), encoding="utf-8").read()
    chk("the audit imports the sibling instrument",
        "import effective_redundancy" in asrc)
    # "def n_eff" alone matches inside def n_eff_equivalence -- the
    # UNI_009 substring bleed, caught here in this file's own first
    # draft. The paren pins the definition.
    chk("and defines no n_eff of its own",
        "def n_eff(" not in asrc)

    # ---- the reframe reproduces through the delivered arithmetic
    rf = A.reframe_through_instrument()
    chk("all-collapsed gives N_eff = 1 at every scale",
        set(rf.values()) == {1})
    chk("and the report marks it consistency, not truth",
        "CONSISTENCY" in A.render())

    # ---- P7 prose vs code
    dt = A.dissent_threshold()
    chk("no fire at equality (reachable negative)",
        dt["fires_at_equality"] is False)
    chk("fires at 4 over 3 (the code's threshold is any excess)",
        dt["fires_at_4_over_3"] is True)
    chk("fires on a zero-source base",
        dt["fires_on_zero_sources"] is True)
    chk("the prose really says '>>' where the code says '> 1'",
        "concurrence >> independent" in doc and "> 1  # tune threshold" in doc)

    # ---- independence_ratio's designed-in split, both directions
    r0 = DB.independence_ratio(0, 0)
    chk("empty evidence base is NaN", math.isnan(r0))
    chk("and NaN is not zero", not (r0 == 0.0))
    chk("a real zero-upstream base IS zero",
        DB.independence_ratio(0, 5) == 0.0)
    chk("the two states are distinguishable",
        DB.independence_ratio(0, 5) == 0.0 and math.isnan(r0))
    chk("the over-one edge is unguarded (recorded, not repaired)",
        DB.independence_ratio(5, 3) > 1.0)

    # ---- egress measured; the prediction not fabricated
    chk("all three metadata sources refused",
        all(code == "000" for _h, code in A.EGRESS))
    chk("no synthetic evidence base exists in the folder",
        "n_supporting=" not in asrc and "replication_data" not in asrc)

    # ---- the posture: Section 3 applied to this audit
    out = A.render()
    one = " ".join(out.split())
    chk("the report declares the auditor is in-class",
        "member of the class" in one)
    chk("class-level verdicts are declined by construction",
        "DECLINED by construction" in one)
    chk("the report calls itself an instance of Section 3",
        "worked instance of Section 3" in one)
    chk("the mechanical/declared split is stated",
        "mechanical layer" in one and "recomputable by" in one)
    chk("the uncarried load is the headline",
        "CARRIED BY NO PROVISION" in out)
    chk("the report states what declining establishes",
        "not modesty" in one)

    # ================= R2 OUTLINE =================
    import r2_audit as R2

    # the delivered outline is present and defers its own rendering
    r2doc = io.open(os.path.join(HERE, "R2_OUTLINE.md"),
                    encoding="utf-8").read()
    chk("R2 declares itself not provision-form",
        "NOT provision-form yet" in r2doc)

    # transcription: exact, and the check CAN fail
    tc = R2.r1_transcription_check()
    chk("R2's R1 column matches the computed matrix on all seven loads",
        tc["exact"] and len(tc["rows"]) == 7)
    doctored = r2doc.replace("B1      P2, P7", "B1      P2, P7, P8")
    mat_d = R2.r2_matrix(doctored)
    chk("a doctored transcription IS caught (the check can fail)",
        sorted(mat_d["B1"][0]) != sorted(A.coverage()["carried"]["B1"]))

    # the gaps close as a table
    cg = R2.r2_closes_gaps()
    chk("every load has an R2 carrier", cg["closed"])
    chk("A is carried by P0.1 and P0.2",
        cg["a_carriers"] == ["P0.1", "P0.2"])
    chk("D is carried by P0.3 and P0.4",
        cg["d_carriers"] == ["P0.3", "P0.4"])

    # the disjointness threshold through the inherited metric
    ds = R2.disjointness_scenarios()
    chk("two collapsed channels give N_eff below three",
        ds["two_collapse"] < 3 and ds["outline_threshold_holds"])
    chk("one collapsed channel is invisible to the metric (still 3)",
        ds["one_collapses"] == 3)

    # THE FINDING: void and rated-vs-realized
    mg = R2.metric_gaps()
    chk("a void channel reads as the collapsed domain (N_eff 3)",
        mg["void_reads_as"] == 3)
    chk("where the outline's own pricing gives 2",
        mg["outline_prices_void_at"] == 2 and mg["void_gap"])
    chk("all-collapsed access is rated 1 by the inherited metric",
        mg["access_rated"] == 1)
    chk("the outline writes 0 -- the realized count, a different quantity",
        mg["access_outline_states"] == 0
        and mg["access_realized"] == 0
        and mg["rated_realized_gap"])
    chk("the outline really writes N_eff(access) = 0",
        "N_eff(access) = 0" in r2doc)

    # P0.5 run on this session: state, not verdict
    chk("P0.5 answers all four structural questions",
        len(R2.P05_SELF_LOCATION) == 4)
    chk("every answer carries a stated basis",
        all(basis for _q, _a, basis in R2.P05_SELF_LOCATION))
    joined = " ".join(a for _q, a, _b in R2.P05_SELF_LOCATION).lower()
    chk("no answer is a compliance verdict",
        "meet" not in joined and "comply" not in joined
        and "pass" not in joined)
    r2out = R2.render()
    r2one = " ".join(r2out.split())
    chk("the self-location is rendered as a rough station",
        "Rough station" in r2out)
    chk("and the report re-declares the in-class posture",
        "certifies nothing" in r2one)
    chk("the judgmental sections are left with the render step",
        "LEFT WITH THE RENDER STEP" in r2out)

    # r2_audit refuses --selftest
    rr = subprocess.run([sys.executable, os.path.join(HERE, "r2_audit.py"),
                         "--selftest"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("r2_audit.py refuses --selftest", rr.returncode == 2)

    # ================= WORK ORDER -> FABLE 5 =================
    import wo_return as WO

    wodoc = io.open(os.path.join(HERE, "WORK_ORDER_F5.md"),
                    encoding="utf-8").read()
    chk("the work order is landed verbatim (its own vocabulary present)",
        "REFUSED-BY-§3" in wodoc and "P3 dissimilar verifier" in wodoc)

    wt1 = WO.task1()
    chk("task 1 passes with both nulls live",
        wt1["result"] == "PASS"
        and wt1["null_single_removed_detected"]
        and wt1["null_gap_induced_detected"])

    wds = WO.dep_sets()
    chk("all three dep sets extract non-empty from the outline's braces",
        all(wds[c]["elements"] for c in ("P0.3", "P0.4", "P0.5")))
    chk("the P0.3 MINUS clause extracts (retention is represented)",
        bool(wds["P0.3"]["minus"]))
    wt2 = WO.task2()
    chk("task 2: all three pairwise intersections are empty",
        wt2["all_empty"] and len(wt2["intersections"]) == 3)
    chk("task 2 reports both no-copies values per DBK_011 (3 vs 2)",
        wt2["n_eff_copies_held"] == 3
        and wt2["n_eff_no_copies_inherited_metric"] == 3
        and wt2["n_eff_no_copies_outline_pricing"] == 2)

    wt3 = WO.task3()
    chk("task 3 fails: the constructed drift is caught by neither channel",
        wt3["result"] == "FAIL" and wt3["caught"] is False)
    chk("and both channel analyses end in nothing surfacing",
        "Nothing surfaces" in wt3["analysis"]["P0.3"]
        and "Nothing surfaces" in wt3["analysis"]["P0.4"])
    chk("the consequence is scoped, not global (bounded by the envelope)",
        "outside the declared envelope" in wt3["consequence"])

    wt4 = WO.task4()
    chk("task 4's two codings run through the delivered function",
        wt4["d3"]["coder_A_ratio"] == DB.independence_ratio(1, 10)
        and wt4["d3"]["coder_B_ratio"] == DB.independence_ratio(10, 10))
    chk("and they sit at opposite ends of the scale on one corpus",
        wt4["d3"]["coder_A_ratio"] == 0.1
        and wt4["d3"]["coder_B_ratio"] == 1.0
        and wt4["result"] == "FAIL")

    wt5 = WO.task5()
    chk("task 5 sweeps the placeholder and the verdicts flip inside it",
        wt5["result"] == "PASS"
        and any(f43 and not f31 or (not f43 and f31)
                for _t, f43, f31 in wt5["threshold_sweep"])
        and wt5["threshold_sweep"][0][1] is True      # (4,3) at t=1
        and wt5["threshold_sweep"][1][1] is False     # (4,3) at t=1.5
        and wt5["threshold_sweep"][2][2] is True      # (3,1) at t=2
        and wt5["threshold_sweep"][3][2] is False)    # (3,1) at t=3
    chk("the harness table includes the NaN and zero-channel edges",
        any("independence_ratio(0, 0)" in n and v == "NaN"
            for n, v in wt5["table"])
        and any(n == "n_eff([])" and v == 0 for n, v in wt5["table"]))

    wt6 = WO.task6()
    chk("task 6 fails both halves with counterexamples on record",
        wt6["result"] == "FAIL" and len(wt6["6a"]) == 2
        and len(wt6["6b"]) == 1)
    chk("the shared root names the reading distribution",
        "DISTRIBUTION" in wt6["shared_root"])
    chk("and the gate keeps the ecosystem candidate a marker",
        "marker" in wt6["gate"])

    wt7 = WO.task7()
    chk("task 7's vector is five hosts, all refused, dated",
        len(wt7["vector"]) == 5
        and all(c == "000" for _h, c in wt7["vector"])
        and wt7["measured_on"] == "2026-08-30")
    chk("both N_eff senses are reported (rated 1, realized 0)",
        wt7["n_eff_rated"] == 1 and wt7["realized_paths"] == 0)

    wout = WO.render()
    chk("the return opens with the role correction, before any task",
        wout.index("ROLE CORRECTION") < wout.index("TASK 1"))
    chk("no task needed REFUSED-BY-§3 and the return says where the "
        "refusal lands instead",
        "REFUSED-BY-§3" in wout and "role label" in wout)
    for n in range(1, 8):
        blk = wout.split("TASK %d " % n)[1]
        chk("task %d uses the order's return format" % n,
            "RESULT" in blk.split("TASK")[0]
            and "EVIDENCE" in blk.split("TASK")[0])
    chk("the routing block follows the order's AFTER RETURN rules",
        "AFTER RETURN" in wout and "stays a marker" in wout)

    wr = subprocess.run([sys.executable, os.path.join(HERE, "wo_return.py"),
                         "--selftest"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("wo_return.py refuses --selftest", wr.returncode == 2)
    chk("and names where its checks live", b"selftest_dbk.py" in wr.stderr)

    # ================= R2 OUTLINE V2 =================
    import r2v2_audit as RV

    v2doc = io.open(os.path.join(HERE, "R2_OUTLINE_V2.md"),
                    encoding="utf-8").read()
    chk("both outline versions are in the folder and differ",
        "RETURN STATUS" in v2doc and "RETURN STATUS" not in r2doc)

    tr = RV.transcription()
    chk("v2's transcription of the return is exact on all six figures",
        tr["exact"] and len(tr["checks"]) == 6)
    # null: a doctored figure IS caught
    trd = RV.transcription(v2doc.replace("0.1 vs 1.0", "0.2 vs 1.0"))
    chk("a doctored figure is caught (the transcription check can fail)",
        not trd["exact"])
    kp = RV.kappa_provenance()
    chk("kappa 0.6 is sourced to the order's own Task 4 rule",
        kp["v2_states"] and kp["order_states"])

    rc1 = RV.r1_column_check()
    chk("the v2 matrix's R1 column matches computed coverage, 7 loads",
        rc1["exact"] and len(rc1["rows"]) == 7)
    matd = RV.v2_matrix(v2doc.replace("B1      P2, P7 ",
                                      "B1      P2, P7, P8"))
    chk("a doctored v2 matrix row IS caught",
        sorted(matd["B1"]["r1"]) != sorted(A.coverage()["carried"]["B1"]))

    chk("the P1-bounded annotation is not read as a carrier",
        RV._tokens("— (P1-bounded, uncarried)") == ([], []))
    chk("section 1 reads D as uncarried",
        RV.d_row()["uncarried_in_sec1"])
    dsp = RV.d_split()
    chk("section 3's carries column still lists D under P0.3 and P0.4",
        dsp["sec3_channels_listing_d"] == ["P0.3", "P0.4"]
        and dsp["split"])
    chk("F's condition carries a marker and the reconciling prose exists",
        dsp["f_condition_marked"] and dsp["reconciling_prose"])

    tgc = RV.tag_check()
    chk("three tags are used beyond the declared legend",
        tgc["beyond_legend"] == ["KILLED-VACUOUS", "LIVE", "REOPENED"])
    chk("all eight entries' tags are consistent with computed verdicts",
        tgc["all_consistent"] and len(tgc["entries"]) == 8)
    tgd = RV.tag_check(v2doc.replace("KILLED (Task 4).",
                                     "QUALIFIED (Task 4)."))
    chk("a tag disagreeing with its task's verdict IS caught",
        not tgd["all_consistent"])

    sb = RV.searcher_branches()
    chk("the order names searcher-dependent branches in tasks 4 and 6",
        sb["named_in_order"] == [4, 6] and sb["task3_branch_implicit"])
    chk("v2 counts only task 6; the conclusion survives, the count "
        "does not",
        sb["v2_counts_only_task6"] and sb["conclusion_survives"])

    pe = RV.probe_extension()
    chk("v2 requires the probe set unselectable; the return did not "
        "close selection",
        pe["extension"] and pe["return_stated_fixed"])
    chk("the accounting choice is routed to P0.2 as a declared decision",
        RV.accounting_declared())

    rvout = RV.render()
    chk("the v2 report states it computes and does not conclude",
        "computes; it does not conclude" in rvout)

    rv = subprocess.run([sys.executable,
                         os.path.join(HERE, "r2v2_audit.py"),
                         "--selftest"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("r2v2_audit.py refuses --selftest", rv.returncode == 2)

    # ================= WORK ORDER 2 =================
    import wo2_return as W2
    from fractions import Fraction as _Fr

    wo2doc = io.open(os.path.join(HERE, "WORK_ORDER_F5_2.md"),
                     encoding="utf-8").read()
    chk("work order 2 is landed verbatim (its own vocabulary present)",
        "kill-closure" in wo2doc and "DELIBERATELY NOT ASKED" in wo2doc)

    w1 = W2.t1()
    chk("t1: 144 interior cells, each flipping at its own ratio",
        w1["interior_cells"] == 144 and w1["result"] == "ENUMERATED")
    chk("t1: the flip set is exactly the distinct grid ratios; 4/3 in it",
        w1["four_three_is_boundary"]
        and w1["distinct_flips"] == len(
            set(_Fr(c, s) for c in range(1, 13) for s in range(1, 13))))
    chk("t1: the two threshold-independent regions are counted apart",
        w1["unconditional_cells"] == 13
        and w1["never_fire_cells"] == 12)
    chk("t1: the plausible band holds a proper subset of the flips",
        0 < len(w1["flips_in_band"]) < w1["distinct_flips"])

    w2t = W2.t2()
    chk("t2: E and F share one stated incident, and only they do",
        w2t["nonempty"] == {"E∩F": ["Fukushima 1-4"]})
    chk("t2: the delivered harness's own arithmetic fires on the pair",
        w2t["ef_dissent_alarm_2_1"] is True)
    chk("t2: five of six pool domains match the seed table; aviation "
        "is the residual",
        len(w2t["domains_matched"]) == 5
        and w2t["domains_residual"] == ["aviation"])
    chk("t2: the B fork is reported, not resolved",
        w2t["b_seed_rows"] == ["East Palestine"]
        and w2t["sources"]["B1"] == [] and w2t["sources"]["B2"] == [])
    chk("t2: the order's named artifacts are absent from every "
        "delivered file and present in the order itself",
        all(w2t["artifact_hits"][f]["colophon"] == 0
            and w2t["artifact_hits"][f]["effective"] == 0
            for f in W2.DELIVERED)
        and w2t["artifact_hits"][W2.ORDER2]["colophon"] > 0)

    a3 = W2.t3a()
    chk("t3a: coverage honest -- D the only uncarried, P1-bounded",
        a3["result"] == "PASS" and a3["only_uncarried_is_D"]
        and a3["d_reads_p1_bounded"])
    chk("t3a: both null injections are live",
        a3["null_doctored_D_reads_carried"]
        and a3["null_stripped_atk_reads_carried"])
    b3 = W2.t3b()
    chk("t3b: the clause lives only in the order; prior claims present",
        b3["result"] == "PASS"
        and b3["clause_absent_from_delivered_files"]
        and b3["clause_lives_in_the_order_itself"]
        and b3["prior_claims_all_present"])

    w4 = W2.t4()
    chk("t4: five consistent accountings, values 3,3,3,3,2",
        [v for _n, v, _s in w4["rows"] if v is not None]
        == [3, 3, 3, 3, 2])
    chk("t4: exactly one accounting sits below three, the void-priced one",
        len(w4["below_three"]) == 1
        and w4["below_three"][0][0].startswith("not held / void"))
    chk("t4: the inexpressible combination is a table row, not a number",
        any(v is None and "INEXPRESSIBLE" in s
            for _n, v, s in w4["rows"]))
    chk("t4: the dropping intersection names provider-only retention",
        "provider-only retention" in w4["dropping_intersection"])

    # the module writes nothing: no write-mode open, no subprocess
    import ast as _ast
    w2src = io.open(os.path.join(HERE, "wo2_return.py"),
                    encoding="utf-8").read()
    w2tree = _ast.parse(w2src)
    opens_ok = True
    for node in _ast.walk(w2tree):
        if isinstance(node, _ast.Call):
            fn = node.func
            name = fn.attr if isinstance(fn, _ast.Attribute) \
                else getattr(fn, "id", "")
            if name == "open":
                modes = list(node.args)[1:2] + [
                    k.value for k in node.keywords if k.arg == "mode"]
                for a in modes:
                    if isinstance(a, _ast.Constant) \
                            and isinstance(a.value, str) \
                            and ("w" in a.value or "a" in a.value):
                        opens_ok = False
    w2mods = set()
    for node in _ast.walk(w2tree):
        if isinstance(node, _ast.Import):
            w2mods.update(a.name for a in node.names)
        elif isinstance(node, _ast.ImportFrom):
            w2mods.add(node.module or "")
    chk("wo2_return contains no write-mode open and no subprocess",
        opens_ok and "subprocess" not in w2mods)

    w2out = W2.render()
    for n in range(1, 5):
        blk = w2out.split("T%d — " % n)[1]
        chk("wo2 task %d uses the family's return format" % n,
            "RESULT" in blk.split("\nT")[0]
            and "EVIDENCE" in blk.split("\nT")[0])
    chk("no RESULT line carries a forbidden label",
        all("verified" not in ln.lower() and "confirmed" not in
            ln.lower() and "p3-passed" not in ln.lower()
            for ln in w2out.splitlines()
            if ln.strip().startswith("RESULT")))
    chk("the return is dated and states the append-only posture",
        W2.RUN_DATE in w2out and "DBK_026" in w2out)

    w2r = subprocess.run([sys.executable,
                          os.path.join(HERE, "wo2_return.py"),
                          "--selftest"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("wo2_return.py refuses --selftest", w2r.returncode == 2)

    # ================= WORK ORDER 3 =================
    import wo3_return as W3

    wo3doc = io.open(os.path.join(HERE, "WORK_ORDER_F5_3.md"),
                     encoding="utf-8").read()
    chk("work order 3 is landed verbatim (its own vocabulary present)",
        "assumption wearing a number" in wo3doc
        and "phantom-colophon error" in wo3doc)

    chk("the typing table covers all 20 provisions, each in one class",
        len(W3.ORDER) == 20
        and sorted(W3.ORDER) == sorted(list(W3.DERIVED)
                                       + list(W3.PROVISIONAL)
                                       + list(W3.ASSUMPTION)))
    ver = W3.verify_rows()
    chk("every row's evidence check is green in its own direction",
        all(ver.values()) and len(ver) == 20)
    # both directions can fail: a planted marker turns an ASSUMPTION
    # block red, and a misquoted DERIVED row is absent from the file
    blk = W3._block(*W3.ASSUMPTION["P2"]["block"])
    chk("the marker-absence check CAN fail (planted marker caught)",
        any(m in blk + " Fukushima" for m in W3.INCIDENT_MARKERS)
        and not any(m in blk for m in W3.INCIDENT_MARKERS))
    chk("a misquoted DERIVED row is absent from the named file",
        "two AOA vanes existed; one system reading two"
        not in W3._text_for(W3.R1F))

    w31 = W3.t1()
    chk("t1 headline: 12 of 20 ASSUMPTION, 5 DERIVED, 3 PROVISIONAL",
        w31["n_assumption"] == 12 and w31["n_derived"] == 5
        and w31["n_provisional"] == 3)
    chk("the honest split: 4 self-tagged + 3 deferred + 5 unmarked",
        len(w31["self_tagged"]) == 4 and len(w31["deferred"]) == 3
        and sorted(w31["unmarked"]) == ["P0.2", "P0.5", "P2", "P5",
                                        "P8"])
    fp = W3.falsify_parentheticals()
    chk("four FALSIFY parentheticals asserted, one incident-backed, "
        "three clean",
        sorted(k for k, v in fp.items() if v == "asserted")
        == ["P2", "P4", "P6", "P8"]
        and fp["P3"] == "incident-backed"
        and sorted(k for k, v in fp.items() if v == "none")
        == ["P1", "P5", "P7"])

    w32 = W3.t2()
    chk("t2: the seed B row and both R1 definition lines extract",
        "East Palestine" in w32["seed_b_row"]
        and w32["b1_line"].startswith("B1 INFORMATION")
        and "architecture doesn't compare" in w32["b2_line_head"])
    chk("t2: no seed row names B2; the aviation citation is in-doc",
        w32["b2_in_seed_rows"] == []
        and w32["p3_falsify_cites_incident"]
        and w32["sec5_cites_incident"])
    chk("t2: branch 2, with the provenance sentence present and "
        "aviation in the pool",
        w32["branch"] == 2 and w32["provenance_sentence_present"]
        and w32["pool_has_aviation"])
    chk("t2: the incident NAME lives only in the order",
        w32["incident_name_only_in_order"])

    w33 = W3.t3()
    chk("t3: five loss-adjudicable statements, partition 2 | 3",
        len(w33["statements"]) == 5
        and [len(g) for g in w33["partition"]] == [2, 3])
    chk("t3: held predicts 3 survivors, not-held predicts 2, "
        "regardless of text",
        all(("= 3" in s) == n.startswith("held")
            for n, _v, s in w33["statements"]))
    chk("t3: the inexpressible row is typed as an envelope report",
        "OUT-OF-RANGE" in w33["inexpressible_typed"]
        and w33["inexpressible_row"].startswith("not held / void"))

    w3out = W3.render()
    for n in range(1, 4):
        blk3 = w3out.split("T%d — " % n)[1]
        chk("wo3 task %d uses the family's return format" % n,
            "RESULT" in blk3.split("\nT")[0]
            and "EVIDENCE" in blk3.split("\nT")[0])
    chk("no RESULT line carries a forbidden label",
        all("verified" not in ln.lower() and "confirmed" not in
            ln.lower() and "p3-passed" not in ln.lower()
            for ln in w3out.splitlines()
            if ln.strip().startswith("RESULT")))
    chk("the return is dated, appends DBK_030.., and names the "
        "filename mismatch",
        W3.RUN_DATE in w3out and "DBK_030" in w3out
        and "ai_infrastructure_design_basis.md" in w3out)

    w3r = subprocess.run([sys.executable,
                          os.path.join(HERE, "wo3_return.py"),
                          "--selftest"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("wo3_return.py refuses --selftest", w3r.returncode == 2)

    # ---- audit refuses --selftest
    r = subprocess.run([sys.executable, os.path.join(HERE, "audit.py"),
                        "--selftest"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    chk("audit.py refuses --selftest", r.returncode == 2)
    chk("and names where its checks live", b"selftest_dbk.py" in r.stderr)

    # ---- the no-severity screen, no exemptions
    sys.path.insert(0, os.path.join(os.path.dirname(HERE),
                                    "sheet-structure-scan"))
    import no_severity  # noqa: E402
    chk("the report carries no severity language",
        not no_severity.hits(out))
    chk("the R2 report carries no severity language",
        not no_severity.hits(r2out))
    chk("the work-order return carries no severity language",
        not no_severity.hits(wout))
    chk("the v2 report carries no severity language",
        not no_severity.hits(rvout))
    chk("the work-order-2 return carries no severity language",
        not no_severity.hits(w2out))
    chk("the work-order-3 return carries no severity language",
        not no_severity.hits(w3out))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(out + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
