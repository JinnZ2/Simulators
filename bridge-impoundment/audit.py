#!/usr/bin/env python3
# audit.py (bridge-impoundment) -- CC0, stdlib only, parses under 3.9
#
# Audit of the GAP 15 entry. The drop is landed verbatim and edited by
# nothing here. Three jobs: resolve every cross-reference by EXISTENCE
# rather than mention (grepping the tree for the strings would count
# this folder's own files -- the QA_007 / UNI_010 loop -- so a target
# resolves only if the named artifact or claim id exists outside this
# folder); check the drop's two repo-facing sentences against the
# record they cite; and measure the egress state of the data hosts the
# method needs, so UNMEASURED cells are a property of the environment
# on record rather than an assumption.

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bridge_impoundment as BI  # noqa: E402

RUN_DATE = "2026-08-30"


def _read(*parts):
    return io.open(os.path.join(*parts), encoding="utf-8").read()


# ------------------------------------------------- cross-references

def cross_refs():
    """Two columns, mention vs artifact. A row resolves only on the
    existence of the named thing outside this folder."""
    ccc = os.path.join(ROOT, "columbia-chain-cascade")
    rcc = os.path.join(ROOT, "reservoir-chain-coupling")
    rows = []

    rows.append(("CCC_007 (initiator comparability claim)",
                 "## CCC_007" in _read(ccc, "CLAIM_TABLE.md")))
    rows.append(("Module F (the amplifier section)",
                 "MODULE F" in _read(ccc, "SOURCE_DROP.md")))
    rows.append(("the operator swap (reservoir-chain-coupling)",
                 "max(wave, pool)" in _read(rcc, "SOURCE_DROP.md")
                 or os.path.exists(os.path.join(rcc,
                                                "operator_swap.py"))))
    rows.append(("the Columbia/Snake node list",
                 os.path.exists(os.path.join(ccc, "eap_coverage.py"))))
    # GAP 14 landed after this audit's first landing, under a folder
    # name this audit had not guessed -- detected by CONTENT (its
    # SOURCE_DROP header), which is what fired BI_001's falsifier.
    gap14 = False
    for name in os.listdir(ROOT):
        sd = os.path.join(ROOT, name, "SOURCE_DROP.md")
        if name != os.path.basename(HERE) and os.path.isfile(sd):
            head = io.open(sd, encoding="utf-8").read(40)
            if head.startswith("# GAP 14"):
                gap14 = True
    rows.append(("GAP 14, by content (landed after this audit)",
                 gap14))

    absent = []
    for basename in ("OPEN_QUESTIONS.md",
                     "SCOPE_BOUNDARY.md"):
        found = False
        for dirpath, dirnames, filenames in os.walk(ROOT):
            if ".git" in dirpath or dirpath.startswith(HERE):
                continue
            if basename in filenames:
                found = True
                break
        absent.append((basename, found))
    # the remaining sibling gap and the loop marker: no folder or file
    # in the tree carries them, by name or by content header
    for name in ("gap-2", "sediment-debris-biological-loop"):
        absent.append((name, os.path.isdir(os.path.join(ROOT, name))))

    deliverable = os.path.exists(os.path.join(HERE,
                                              "bridge_impoundment.py"))
    return {"resolve": rows,
            "all_resolve": all(ok for _n, ok in rows),
            "named_elsewhere": absent,
            "none_present": not any(ok for _n, ok in absent),
            "deliverable_arrives_with_landing": deliverable}


# ------------------------------- the two repo-facing sentences

def module_f_sentence():
    """'the same operator swap Module F already proves' -- checked
    against the record. The swap is shown in reservoir-chain-coupling
    on constructed chains (FIRM layer, RCC_007), while Module F itself
    arrived truncated and never delivered its body (CCC_001). So the
    sentence's substance points at a real result and carries two
    drifts: attribution (the proof lives in the sibling, not in the
    truncated module) and strength ('proves' -- the FIRM/SOFT split
    keeps the real-chain question with the routing run, RCC_009)."""
    ccc_src = _read(ROOT, "columbia-chain-cascade", "SOURCE_DROP.md")
    ccc_claims = _read(ROOT, "columbia-chain-cascade", "CLAIM_TABLE.md")
    rcc_claims = _read(ROOT, "reservoir-chain-coupling",
                       "CLAIM_TABLE.md")
    drop = _read(HERE, "SOURCE_DROP.md")
    return {
        "drop_sentence_present":
            "the same operator swap Module F already proves"
            in " ".join(drop.split()),
        "module_f_truncated":
            ccc_src.rstrip().endswith("changes the cascade outcome "
                                      "at the next")
            or "## CCC_001" in ccc_claims,
        "swap_shown_in_sibling": "## RCC_002" in rcc_claims
            and "## RCC_005" in rcc_claims,
        "firm_soft_split_recorded": "## RCC_007" in rcc_claims,
        "real_chain_question_open": "## RCC_009" in rcc_claims,
    }


def ccc007_usage():
    """The drop cites CCC_007 as the comparability REQUIREMENT. The
    claim recorded comparability as asserted-not-shown. The citation
    is therefore to the requirement whose demonstration is still owed:
    the interface contract in bridge_impoundment.py makes the
    requirement checkable at the DESIGN layer (identical key sets),
    and showing it on the engine remains the routing run."""
    claims = _read(ROOT, "columbia-chain-cascade", "CLAIM_TABLE.md")
    blk = claims.split("## CCC_007")[1].split("## CCC_")[0] \
        if "## CCC_007" in claims else ""
    b = BI.initiator(1.0, 2.0, 3.0, 4.0, "breach")
    r = BI.initiator(5.0, 6.0, 7.0, 8.0, "bridge-release")
    return {"claim_says_asserted_not_shown":
            "asserted, not shown" in blk,
            "design_layer_check_passes": BI.same_interface(b, r),
            "engine_layer_still_owed": True}


# ------------------------------------------------------ egress

# The expected allowlist-refusal state, CARRIED: the --measure probe
# was classifier-blocked in the landing session, so these codes are
# the standing pattern every prior probe in this tree returned for
# non-GitHub hosts, not a fresh reading. Re-run --measure to take one.
EGRESS = [
    ("infobridge.fhwa.dot.gov", "000"),
    ("www.fhwa.dot.gov", "000"),
    ("waterdata.usgs.gov", "000"),
]


def measure_egress(timeout=6):
    import urllib.request
    out = []
    for host, _c in EGRESS:
        code = "000"
        try:
            urllib.request.urlopen("https://%s/" % host,
                                   timeout=timeout)
            code = "2xx"
        except Exception:
            code = "000"  # any failure: no path realized
        out.append((host, code))
    return out


# ---------------------------------------------------------- render

def _wrap(s, n=66):
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
    w("GAP 15 -- CROSS-REFERENCE AND RECORD AUDIT")
    w("")
    cr = cross_refs()
    w("RESOLVING IN THIS TREE (by existence, not mention)")
    for name, ok in cr["resolve"]:
        w("  %-46s %s" % (name, "resolves" if ok else "ABSENT"))
    w("NAMED, AND NOT IN THIS TREE")
    for name, ok in cr["named_elsewhere"]:
        w("  %-46s %s" % (name, "present" if ok else "absent"))
    for ln in _wrap(
            "The entry is a draft for a register this repository does "
            "not hold. At this audit's first landing both coupling "
            "targets were with it; GAP 14 then arrived in the same "
            "session (the mining-increment folder, detected by "
            "content), firing the first clause of BI_001's falsifier "
            "-- the claim carries its update note. Gap 2 and the loop "
            "marker stay absent. The one named artifact that arrived "
            "with the landing itself is the deliverable: "
            "bridge_impoundment.py exists (%s) -- as the scaffold its "
            "structure supports without data, not the study."
            % cr["deliverable_arrives_with_landing"]):
        w("  " + ln)
    w("")

    mf = module_f_sentence()
    w("THE MODULE-F SENTENCE, AGAINST THE RECORD")
    for k in ("drop_sentence_present", "module_f_truncated",
              "swap_shown_in_sibling", "firm_soft_split_recorded",
              "real_chain_question_open"):
        w("  %-34s %s" % (k, mf[k]))
    for ln in _wrap(
            "The substance points at a real result; the sentence "
            "carries two drifts -- the showing lives in "
            "reservoir-chain-coupling on constructed chains, Module F "
            "itself never arrived, and the FIRM/SOFT split keeps "
            "whether the swap is load-bearing for any real chain with "
            "the routing run."):
        w("  " + ln)
    w("")

    cu = ccc007_usage()
    w("THE CCC_007 CITATION")
    for k, v in cu.items():
        w("  %-34s %s" % (k, v))
    w("")

    w("EGRESS (the method's data hosts; carried state, %s -- the"
      % RUN_DATE)
    w("probe could not run in the landing session; run --measure for")
    w("a fresh reading)")
    for host, code in EGRESS:
        w("  %-28s %s" % (host, code))
    for ln in _wrap(
            "Every chain-level cell in the scaffold is UNMEASURED "
            "because the inventory and gage hosts are in the carried "
            "allowlist-refusal state and no value is supplied from "
            "memory; the gap "
            "STANDS-as-unmeasured on this chain, which is a statement "
            "about this environment and not about any bridge."):
        w("  " + ln)
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("CLAIM_TABLE.md as BI_001..BI_007.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that "
            "exercise it live in selftest_bi.py.\n"
            "    python3 bridge-impoundment/selftest_bi.py\n")
        sys.exit(2)
    if "--measure" in sys.argv[1:]:
        for host, code in measure_egress():
            print("%-28s %s" % (host, code))
        sys.exit(0)
    print(render())
