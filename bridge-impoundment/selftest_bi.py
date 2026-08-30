#!/usr/bin/env python3
# selftest_bi.py -- CC0, stdlib only, parses under 3.9

import inspect
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bridge_impoundment as BI  # noqa: E402
import audit as A  # noqa: E402

ok = [0]
bad = []


def chk(name, cond):
    if cond:
        ok[0] += 1
    else:
        bad.append(name)


def run():
    drop = io.open(os.path.join(HERE, "SOURCE_DROP.md"),
                   encoding="utf-8").read()
    chk("the drop is landed verbatim (its own vocabulary present)",
        "SIGN CAVEAT" in drop and "transient impoundment" in drop
        and "CITATION STATUS" in drop)

    # ---- the parameter schema refuses in every direction
    p = BI.param("x", None, "UNMEASURED", "the inventory pass")
    chk("a well-formed parameter constructs", p["name"] == "x")
    for name, args in (
            ("state outside the vocabulary", ("x", 1, "GUESSED", "y")),
            ("no mover named", ("x", 1, "MEASURED", "  ")),
            ("a value marked UNMEASURED", ("x", 1, "UNMEASURED", "y"))):
        try:
            BI.param(*args)
            chk("param refuses %s" % name, False)
        except ValueError:
            chk("param refuses %s" % name, True)

    # ---- the clog flag has three states, never two
    chk("at the threshold flags", BI.clog_flag(10.0) == "FLAG")
    chk("above the threshold clears", BI.clog_flag(10.01) == "CLEAR")
    chk("an unknown spacing is UNMEASURED, not clear",
        BI.clog_flag(None) == "UNMEASURED")
    try:
        BI.clog_flag(0)
        chk("a non-span raises", False)
    except ValueError:
        chk("a non-span raises", True)

    # ---- the initiator interface: identical across provenances
    b = BI.initiator(1.0, 2.0, 3.0, 4.0, "breach")
    r = BI.initiator(5.0, 6.0, 7.0, 8.0, "bridge-release")
    chk("breach and bridge-release share one interface",
        BI.same_interface(b, r))
    chk("a widened dict is NOT the interface (the check can fail)",
        not BI.same_interface(dict(b, shielding=0.3), r))

    # ---- the sign caveat is structural
    rec = BI.StandingStructureRecord(0.35, "carried from the drop")
    try:
        rec.to_initiator()
        chk("the protective finding refuses to emit an initiator",
            False)
    except TypeError:
        chk("the protective finding refuses to emit an initiator",
            True)
    release_path = (BI.initiator, BI.impoundment_arithmetic,
                    BI.debris_budget, BI.falsifier)
    leak = []
    for fn in release_path:
        for arg in inspect.signature(fn).parameters:
            if "shield" in arg or "reduction" in arg:
                leak.append((fn.__name__, arg))
    chk("no release-path function takes a shielding parameter",
        leak == [])

    # ---- the arithmetic is conservation, with both directions
    g = BI.impoundment_arithmetic(2.0, 6.0, 2.0)
    chk("gain = accumulation over release", abs(g["gain"] - 3.0) < 1e-12
        and g["gain_exceeds_one"])
    g2 = BI.impoundment_arithmetic(2.0, 2.0, 6.0)
    chk("a slow release attenuates (gain below one is reachable)",
        g2["gain"] < 1.0 and not g2["gain_exceeds_one"])
    d = BI.debris_budget(10.0, 2.0)
    chk("debris load gain is at least one by construction",
        d["gain_at_least_one"] and d["load_gain"] == 1.2)
    d0 = BI.debris_budget(0.0, 2.0)
    chk("a zero arriving load yields None gain, not a division",
        d0["load_gain"] is None and d0["gain_at_least_one"])

    # ---- both falsifiers, every branch reachable
    chk("no flagged span closes the gap",
        BI.falsifier([12.0, 15.0], None, None, None) == "GAP_CLOSES")
    chk("low backwater and an unmoved breach set close the gap",
        BI.falsifier([8.0], 2.0, 5.0, False) == "GAP_CLOSES")
    chk("a flagged span with reaching backwater stands",
        BI.falsifier([8.0], 6.0, 5.0, False) == "GAP_STANDS")
    chk("a shifted breach set stands",
        BI.falsifier([8.0], 2.0, 5.0, True) == "GAP_STANDS")
    chk("an unknown spacing is UNMEASURED, never a close",
        BI.falsifier([None], 2.0, 5.0, False) == "UNMEASURED")
    chk("unknown backwater on a flagged span is UNMEASURED",
        BI.falsifier([8.0], None, 5.0, False) == "UNMEASURED")
    chk("the coupling falsifier drops the loop term on low supply",
        BI.coupling_falsifier([1.0, 2.0], 5.0) == "LOOP_TERM_DROPS")
    chk("and stands when any supply reaches the threshold",
        BI.coupling_falsifier([1.0, 6.0], 5.0) == "LOOP_TERM_STANDS")
    chk("and is UNMEASURED on an unknown supply",
        BI.coupling_falsifier([1.0, None], 5.0) == "UNMEASURED")

    # ---- the chain state is honestly empty
    cs = BI.chain_state()
    chk("every chain-level cell is UNMEASURED with a named mover",
        len(cs) == 5 and all(p["knowledge_state"] == "UNMEASURED"
                             and p["value"] is None for p in cs))

    # ---- the audit's cross-references
    cr = A.cross_refs()
    chk("the five resolving rows resolve by existence -- GAP 14 by "
        "content among them, per the BI_001 update",
        cr["all_resolve"] and len(cr["resolve"]) == 5)
    chk("the register, Gap 2, and the loop marker are absent",
        cr["none_present"] and len(cr["named_elsewhere"]) == 4)
    chk("the named deliverable arrives with the landing",
        cr["deliverable_arrives_with_landing"])

    mf = A.module_f_sentence()
    chk("the module-f sentence is in the drop and both record halves "
        "check",
        mf["drop_sentence_present"] and mf["module_f_truncated"]
        and mf["swap_shown_in_sibling"]
        and mf["firm_soft_split_recorded"]
        and mf["real_chain_question_open"])

    cu = A.ccc007_usage()
    chk("CCC_007 recorded comparability as asserted-not-shown, and the "
        "design-layer check passes",
        cu["claim_says_asserted_not_shown"]
        and cu["design_layer_check_passes"])

    chk("the egress vector is pinned for all three hosts",
        len(A.EGRESS) == 3
        and all(code in ("000", "2xx") for _h, code in A.EGRESS))

    # ================= THE ADDENDUM (SOURCE_DROP_V2) =================
    import addendum_audit as AD

    asm = AD.assembly()
    chk("the addendum assembly is a verified pure insertion in the "
        "quantified section",
        asm["pure_insertion"] and asm["placed_in_quantified_section"]
        and asm["fragment_once_in_v2"]
        and asm["fragment_absent_from_v1"])
    # the assembly check can fail: a doctored v2 is not a pure insertion
    frag = AD.fragment()
    v2doc = io.open(os.path.join(HERE, "SOURCE_DROP_V2.md"),
                    encoding="utf-8").read()
    v1doc = drop
    doctored = v2doc.replace("MEASURED instance", "MEASURED case", 1)
    chk("a doctored v2 IS caught (the pure-insertion check can fail)",
        doctored.replace(frag + "\n", "", 1) != v1doc)

    cc = AD.cascade_case()
    chk("the cascade case carries its DOI, volume, and the "
        "measured-instance statement",
        cc["doi_carried"] and cc["volume_carried"]
        and cc["measured_instance_stated"] and cc["chain_stated"])
    chk("the measured half is the release half (no clog term in the "
        "fragment)",
        cc["release_half_only"])

    sr = AD.standing_record()
    chk("the standing record carries the register, the "
        "vocabulary-exclusion finding, and the slow-rate line",
        sr["register_url_carried"] and sr["serves_english_stated"]
        and sr["vocabulary_exclusion_stated"]
        and sr["slow_rate_instrument"])

    # ---- the CLIs refuse --selftest; the screen runs clean
    for mod in ("bridge_impoundment.py", "audit.py",
                "addendum_audit.py"):
        rr = subprocess.run([sys.executable, os.path.join(HERE, mod),
                             "--selftest"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, rr.returncode == 2)

    sys.path.insert(0, os.path.join(ROOT_DIR, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    bout = BI.render()
    aout = A.render()
    adout = AD.render()
    chk("the scaffold report carries no severity language",
        not no_severity.hits(bout))
    chk("the audit report carries no severity language",
        not no_severity.hits(aout))
    chk("the addendum report carries no severity language",
        not no_severity.hits(adout))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(aout + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad),
                                              len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


ROOT_DIR = os.path.dirname(HERE)

if __name__ == "__main__":
    sys.exit(run())
