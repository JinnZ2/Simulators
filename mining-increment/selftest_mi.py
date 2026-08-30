#!/usr/bin/env python3
# selftest_mi.py -- CC0, stdlib only, parses under 3.9

import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mining_increment as MI  # noqa: E402
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
        "TRANSFER CAVEAT" in drop and "PROVENANCE FLAG" in drop
        and "UNVERIFIED-PROVENANCE" in drop
        and "WHAT THE CHINESE WORK HAS" in drop)

    # ---- the shared schema is imported, not copied
    src = io.open(os.path.join(HERE, "mining_increment.py"),
                  encoding="utf-8").read()
    chk("the parameter schema is imported from the sibling gap",
        "from bridge_impoundment import" in src
        and "def param(" not in src)

    # ---- the transfer gate is a code path, both directions
    p = MI.ImportedParam("x", 0.5, "coal-basin", "carried")
    chk("an unestablished basin returns UNDEFINED",
        p.apply_to("columbia-snake") == "UNDEFINED")
    chk("the study basin returns the value",
        p.apply_to("coal-basin") == 0.5)
    p.establish_transfer("columbia-snake", True, "a host-rock study")
    chk("an established transfer returns the value",
        p.apply_to("columbia-snake") == 0.5)
    p2 = MI.ImportedParam("y", 0.5, "coal-basin", "carried")
    p2.establish_transfer("columbia-snake", False, "refuted by study")
    chk("a refuted transfer still returns UNDEFINED",
        p2.apply_to("columbia-snake") == "UNDEFINED")
    try:
        p2.establish_transfer("z", True, "  ")
        chk("establishing transfer takes a basis", False)
    except ValueError:
        chk("establishing transfer takes a basis", True)
    chk("the two carried porosity deltas are UNDEFINED for the chain",
        MI.POROSITY_FISSURE.apply_to("columbia-snake") == "UNDEFINED"
        and MI.POROSITY_NON_FISSURE.apply_to("columbia-snake")
        == "UNDEFINED")

    # ---- the stock/flow separation
    lk = MI.water_balance_link(0.1, 0.05, "constructed")
    chk("the link carries two distinct named sides",
        "storage_side_infiltration_capacity_delta" in lk
        and "flow_side_runoff_coefficient_delta" in lk)
    try:
        MI.water_balance_link(0.1, 0.05, " ")
        chk("the link takes a basis", False)
    except ValueError:
        chk("the link takes a basis", True)
    chk("no function returns one scalar for the pair",
        "storage_and_flow" not in src)

    # ---- the interface equation
    chk("pool_effective is the delivered equation",
        MI.pool_effective(100.0, 0.05) == 105.0)
    chk("an UNDEFINED increment propagates as UNDEFINED, not a number",
        MI.pool_effective(100.0, "UNDEFINED") == "UNDEFINED")
    try:
        MI.pool_effective(-1.0, 0.0)
        chk("a negative pool raises", False)
    except ValueError:
        chk("a negative pool raises", True)
    chk("the rim flag has three states",
        MI.rim_flag(True) == "FLAG" and MI.rim_flag(False) == "CLEAR"
        and MI.rim_flag(None) == "UNMEASURED")

    # ---- the subsidence forms: the drop's stated properties, computed
    sp = MI.shared_properties()
    chk("both forms are zero at zero and approach W0",
        sp["both_zero_at_zero"] and sp["both_approach_w0"])
    chk("knothe is monotone on a sample",
        MI.knothe(1, 3, 0.3) < MI.knothe(2, 3, 0.3)
        < MI.knothe(10, 3, 0.3) < 3.0)
    chk("the strain integral of a constant profile is depth times "
        "strain",
        abs(MI.strain_integral([(0.0, 0.01), (10.0, 0.01)]) - 0.1)
        < 1e-12)
    try:
        MI.strain_integral([(0.0, 0.01)])
        chk("a one-point integral raises", False)
    except ValueError:
        chk("a one-point integral raises", True)

    # ---- both falsifiers, every branch reachable
    chk("low increments and no rim intersection close the gap",
        MI.falsifier([0.001, 0.005], [False, False]) == "GAP_CLOSES")
    chk("a reaching increment stands",
        MI.falsifier([0.02], [False]) == "GAP_STANDS")
    chk("a rim intersection stands",
        MI.falsifier([0.001], [True]) == "GAP_STANDS")
    chk("an unknown increment is UNMEASURED, never a close",
        MI.falsifier([None], [False]) == "UNMEASURED")
    chk("an UNDEFINED import is not a low value",
        MI.falsifier(["UNDEFINED"], [False]) == "UNMEASURED")
    ps = [MI.ImportedParam("a", 1, "coal-basin", "x"),
          MI.ImportedParam("b", 2, "coal-basin", "x")]
    chk("nothing established or refuted is UNMEASURED",
        MI.transfer_falsifier(ps, "columbia-snake") == "UNMEASURED")
    ps[0].establish_transfer("columbia-snake", True, "study")
    chk("any established transfer stands",
        MI.transfer_falsifier(ps, "columbia-snake") == "GAP_STANDS")
    for q in ps:
        q.establish_transfer("columbia-snake", False, "refuted")
    chk("transfer refuted everywhere NARROWS -- a third outcome",
        MI.transfer_falsifier(ps, "columbia-snake") == "GAP_NARROWS")

    # ---- chain state honestly empty
    cs = MI.chain_state()
    chk("every chain-level cell is UNMEASURED with a named mover",
        len(cs) == 6 and all(p3["knowledge_state"] == "UNMEASURED"
                             and p3["value"] is None for p3 in cs))

    # ---- the audit
    cr = A.cross_refs()
    chk("Module F, the node list, and GAP 15 by content resolve",
        cr["all_resolve"])
    chk("the register, both scope modules, and Gaps 1 and 2 are absent",
        cr["none_present"])
    pf = A.provenance_flag()
    chk("both flagged names appear only inside the flag",
        pf["all_contained"])
    chk("the anchor DOI and the do-not-publish instruction are present",
        pf["anchor_doi_present"] and pf["do_not_publish_instruction"])
    ct = A.coupling_term_tension()
    chk("the headline and the appendix are both in the delivered text",
        ct["headline"] and ct["appendix_basin_scale_carry"]
        and ct["appendix_streamflow_measured"]
        and ct["transfer_caveat_present"])
    chk("the egress vector is pinned for all three hosts",
        len(A.EGRESS) == 3
        and all(code in ("000", "2xx") for _h, code in A.EGRESS))

    # ---- CLIs refuse; the screen runs clean
    for mod in ("mining_increment.py", "audit.py"):
        rr = subprocess.run([sys.executable, os.path.join(HERE, mod),
                             "--selftest"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        chk("%s refuses --selftest" % mod, rr.returncode == 2)
    sys.path.insert(0, os.path.join(ROOT_DIR, "sheet-structure-scan"))
    import no_severity  # noqa: E402
    mout = MI.render()
    aout = A.render()
    chk("the scaffold report carries no severity language",
        not no_severity.hits(mout))
    chk("the audit report carries no severity language",
        not no_severity.hits(aout))
    chk("and the screen is not silent by construction",
        bool(no_severity.hits(aout + "\nthis design is broken\n")))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad),
                                              len(bad)))
    for x in bad:
        print("  FAILED", x)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run())
