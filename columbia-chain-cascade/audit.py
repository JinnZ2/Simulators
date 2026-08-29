#!/usr/bin/env python3
# audit.py -- CC0, stdlib only, phone-buildable, parses under 3.9
#
# What can be established about this build spec without running it.
#
# THE SPEC CANNOT BE EXECUTED HERE, AND THE DELIVERED TEXT IS
# INCOMPLETE. Both are measured below rather than asserted. Nothing in
# the spec's hydraulics is simulated: a flood-hazard field produced by a
# stdlib toy would read as a result about a real dam chain, and this is
# the highest-stakes version of the rule the repo holds everywhere.

import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eap_coverage as EAP  # noqa: E402

DROP = os.path.join(HERE, "SOURCE_DROP.md")

# The engine the spec targets. HEC-RAS is Windows-only USACE software; a
# `which` for it is included so the absence is measured, not assumed.
ENGINE = "HEC-RAS 2D"

# Measured 2026-08-29 from this environment. Every data source the spec
# names in section 2 returned no response through the proxy.
EGRESS = [
    ("portal.opentopography.org", "000", "3DEP DEM (section 2)"),
    ("www.usgs.gov", "000", "3DEP / national map"),
    ("apps.nationalmap.gov", "000", "3DEP 1 m / 10 m DEM"),
    ("charts.noaa.gov", "000", "NOAA bathymetry charts"),
    ("nid.sec.usace.army.mil", "000", "NID dam geometry + ownership"),
    ("www.mrlc.gov", "000", "NLCD roughness"),
]


def engine_present():
    """HEC-RAS is not on this machine and cannot be. Reported as a fact
    about the environment, not a judgment about the spec."""
    for name in ("ras", "RAS", "HEC-RAS", "hec-ras"):
        for d in os.environ.get("PATH", "").split(os.pathsep):
            if d and os.path.exists(os.path.join(d, name)):
                return True
    return False


def truncation():
    """The delivered text stops mid-sentence in Module F.

    Section 4 is titled 'MODULE F -- ANTECEDENT CONDITION COUPLING (the
    amplifier)' and the spec calls it 'the part standard breach modeling
    drops ... it changes the cascade outcome'. The text ends 'it changes
    the cascade outcome at the next' -- with no object. So the module the
    spec names as load-bearing is not in hand, and neither is anything
    that would follow it (validation, a claim table, the ask). None of
    it is reconstructed."""
    text = io.open(DROP, encoding="utf-8").read().rstrip()
    last = text.splitlines()[-1] if text else ""
    ends_midsentence = not last.rstrip().endswith((".", ":", ")"))
    module_f_started = "MODULE F" in text
    # A section is "present in full" only if a later section opens after
    # it. Section 4 is the last header and it does not close.
    headers = re.findall(r"(?m)^## \d+\. (.+)$", text)
    return {
        "ends_midsentence": ends_midsentence,
        "last_line": last,
        "module_f_header_present": module_f_started,
        "module_f_body_complete": False,
        "sections_present": headers,
        "highest_section": headers[-1] if headers else None,
        "what_is_missing": [
            "the body of Module F (the antecedent-coupling mechanism the "
            "spec calls the amplifier and 'the part standard breach "
            "modeling drops')",
            "the burn-modified roughness values section 2 forward-"
            "references to Module F",
            "any validation section",
            "any claim table / refutation protocol",
            "the ask (what to run, what to publish)",
        ],
    }


def unbuildable_here():
    """Everything the spec asks for that this environment cannot do,
    each with its specific blocker. Not a verdict on the spec -- a build
    spec for HEC-RAS on 3DEP data is a reasonable thing to write; it is
    simply not runnable from here."""
    return [
        ("2D hydraulic routing (all modules)", "no %s; Windows-only "
         "USACE software, absent from this machine" % ENGINE),
        ("terrain (DEM, bathymetry, roughness)",
         "every source in section 2 refuses CONNECT (allowlist egress)"),
        ("dam geometry (breach parameters)",
         "NID and project design memoranda unreachable"),
        ("the attenuation/amplification matrix (Module A)",
         "one routing run per node; requires the engine and the terrain"),
        ("Module F antecedent coupling",
         "the mechanism is not in the delivered text (truncated)"),
    ]


def what_survives():
    """The parts that need neither the engine, the data, nor the missing
    text. There is exactly one substantive one, plus two structural
    observations."""
    s = EAP.no_plan_spans()
    return {
        "eap_coverage": {
            "runs": True,
            "result": "no single entity's plan spans the chain",
            "settled": s["no_single_plan_spans_chain"],
            "granularity": "jurisdiction floor (%d); exact seam count "
                           "refused" % s["authorities_lower_bound"],
        },
        "structural_observations": [
            "the initiator modules (A-E) are declared 'swappable, same "
            "downstream engine, so modules are comparable' -- a "
            "comparability claim of the same shape as "
            "move-set-derivation's declared architectures, asserted "
            "here and not shown, since showing it requires the engine",
            "'full chain is required, not preferred: attenuation and "
            "amplification only appear across nodes' is the spec's own "
            "reason a reach study cannot substitute -- restated, not "
            "computed, because computing it is the routing run",
        ],
    }


def render():
    out = []
    w = out.append
    w("COLUMBIA CHAIN CASCADE -- what a stdlib environment can establish")
    w("about a HEC-RAS build spec that arrived truncated")
    w("")
    w("THE SPEC CANNOT BE EXECUTED HERE AND THE DELIVERED TEXT IS")
    w("INCOMPLETE. Both are measured below. No hydraulics are simulated:")
    w("a flood-hazard field produced by a toy would read as a result")
    w("about a real dam chain, which is the one thing this folder will")
    w("not produce.")
    w("")

    w("0. THE DELIVERED TEXT IS TRUNCATED")
    t = truncation()
    w("   sections present: %s" % ", ".join(
        h.split(" --")[0].split(" —")[0] for h in t["sections_present"]))
    w("   highest section reached: %s" % t["highest_section"])
    w("   ends mid-sentence: %s" % t["ends_midsentence"])
    w("     last line: \"%s\"" % t["last_line"])
    w("   Module F header present: %s   body complete: %s" % (
        t["module_f_header_present"], t["module_f_body_complete"]))
    w("")
    w("   NOT IN HAND, AND NOT RECONSTRUCTED:")
    for m in t["what_is_missing"]:
        for i, chunk in enumerate(_wrap(m, 66)):
            w("     %s %s" % ("-" if i == 0 else " ", chunk))
    w("")
    w("   The spec names Module F as the load-bearing part -- 'not a")
    w("   refinement; it changes the cascade outcome'. It is exactly")
    w("   the part that did not arrive. Inventing it would put a")
    w("   mechanism the author calls decisive into the author's mouth.")
    w("")

    w("1. THE ENGINE IS ABSENT (measured)")
    w("   %s present on this machine: %s" % (ENGINE, engine_present()))
    w("   HEC-RAS is Windows-only USACE software. There is no path by")
    w("   which the routing in sections 3-4 runs here.")
    w("")

    w("2. EVERY DATA SOURCE REFUSES CONNECT (measured)")
    for host, code, what in EGRESS:
        w("   %-28s %s   %s" % (host, code, what))
    w("   Egress is an allowlist, so substituting a mirror does not")
    w("   help. Section 2's terrain, bathymetry, roughness and dam")
    w("   geometry are all unreachable.")
    w("")

    w("3. WHAT CANNOT BE BUILT HERE, WITH THE SPECIFIC BLOCKER")
    for what, why in unbuildable_here():
        w("   %s" % what)
        for chunk in _wrap(why, 64):
            w("       %s" % chunk)
    w("")

    w("4. WHAT SURVIVES ALL OF THAT -- exactly one substantive thing")
    s = what_survives()
    e = s["eap_coverage"]
    w("   THE GOVERNANCE CLAIM. The spec calls ownership 'the governance")
    w("   variable' and says 'record it as data, not commentary'.")
    w("   eap_coverage.py is that record, and it computes the spec's own")
    w("   conclusion:")
    w("     %s: %s" % (e["result"], e["settled"]))
    w("     granularity: %s" % e["granularity"])
    w("   It holds from the CA/US boundary in the delivered node list")
    w("   alone, before any per-node ownership -- and no assignment of")
    w("   the 18 nodes to owners can undo it. The exact fragmentation")
    w("   requires data this environment cannot reach and will not invent.")
    w("")
    w("   TWO STRUCTURAL OBSERVATIONS, restated not computed:")
    for o in s["structural_observations"]:
        for i, chunk in enumerate(_wrap(o, 64)):
            w("     %s %s" % ("-" if i == 0 else " ", chunk))
    w("")

    w("5. WHAT THIS FOLDER DOES NOT ESTABLISH")
    w("   No hazard field, no velocity bands, no time slices, no")
    w("   attenuation/amplification matrix, nothing about any breach,")
    w("   any node's failure, or any population's exposure. The spec's")
    w("   three headline choices (velocity bands, time slices, exposure")
    w("   overlay) are sound product-design calls and are not tested")
    w("   here, because testing them is the routing run.")
    w("")
    w("   What is established: the governance claim holds at the")
    w("   granularity the delivered text supports, the spec cannot be")
    w("   run in this environment, and the module it calls decisive did")
    w("   not arrive.")
    return "\n".join(out)


def _wrap(s, n):
    words = s.split()
    lines, cur = [], ""
    for wd in words:
        if len(cur) + len(wd) + 1 > n:
            lines.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    if cur:
        lines.append(cur)
    return lines or [""]


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that exercise "
            "it and eap_coverage.py live in selftest_ccc.py.\n"
            "    python3 columbia-chain-cascade/selftest_ccc.py\n")
        sys.exit(2)
    print(render())
