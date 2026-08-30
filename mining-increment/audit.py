#!/usr/bin/env python3
# audit.py (mining-increment) -- CC0, stdlib only, parses under 3.9
#
# Audit of the GAP 14 entry. The drop is landed verbatim and edited by
# nothing here. Cross-references resolve by EXISTENCE, not mention;
# the drop's own provenance flag is checked for containment (the two
# flagged names appear only inside the flag that disclaims them); and
# the one internal tension -- the headline knowledge state against the
# drop's own appendix -- is quoted from both ends rather than argued.

import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mining_increment as MI  # noqa: E402

RUN_DATE = "2026-08-30"


def _read(*parts):
    return io.open(os.path.join(*parts), encoding="utf-8").read()


def drop():
    return _read(HERE, "SOURCE_DROP.md")


# ------------------------------------------------- cross-references

def cross_refs():
    ccc = os.path.join(ROOT, "columbia-chain-cascade")
    bi = os.path.join(ROOT, "bridge-impoundment")
    rows = []
    rows.append(("Module F (the amplifier section)",
                 "MODULE F" in _read(ccc, "SOURCE_DROP.md").upper()))
    rows.append(("the Columbia/Snake node list",
                 os.path.exists(os.path.join(ccc, "eap_coverage.py"))))
    bi_drop = _read(bi, "SOURCE_DROP.md") \
        if os.path.exists(os.path.join(bi, "SOURCE_DROP.md")) else ""
    rows.append(("GAP 15, by content (the coupling pair's other half)",
                 bi_drop.startswith("# GAP 15")))
    absent = []
    for basename in ("UNDERGRADUATE_RESEARCH_GAPS.md",
                     "SCOPE_BOUNDARY.md", "knowledge_state.py",
                     "contributing_inflow.py"):
        found = False
        for dirpath, dirnames, filenames in os.walk(ROOT):
            if ".git" in dirpath or dirpath.startswith(HERE):
                continue
            if basename in filenames:
                found = True
                break
        absent.append((basename, found))
    for name in ("gap-1", "gap-2"):
        absent.append((name, os.path.isdir(os.path.join(ROOT, name))))
    return {"resolve": rows,
            "all_resolve": all(ok for _n, ok in rows),
            "named_elsewhere": absent,
            "none_present": not any(ok for _n, ok in absent)}


# ------------------------------------- the provenance flag, contained

def provenance_flag():
    """The drop flags two of its own citations as unconfirmed, with an
    anchor substituted (Knothe, full DOI) and an explicit instruction
    not to publish the flagged names as given. Checked: the flagged
    names appear ONLY inside the flag that disclaims them, and the
    anchor's DOI is present."""
    d = drop()
    flag = d.split("PROVENANCE FLAG")[1].split("CITATION STATUS")[0]
    out = {}
    for name in ("Padhy", "Piao"):
        total = d.count(name)
        inside = flag.count(name)
        out[name] = {"total": total, "inside_flag": inside,
                     "contained": total == inside and total > 0}
    out["anchor_doi_present"] = "10.1038/s41598-022-23303-9" in d
    out["do_not_publish_instruction"] = "do not publish" in flag
    out["all_contained"] = all(
        v["contained"] for k, v in out.items() if k in ("Padhy",
                                                        "Piao"))
    return out


# ------------------------------- the headline vs the appendix

def coupling_term_tension():
    """The headline says the coupling term is NOT_STUDIED; the drop's
    own trailing section lists the Kuye-basin record doing exactly the
    basin-scale carry (subsidence as a boundary condition in a coupled
    model; streamflow measured against mining). Both lines quoted; the
    surviving reading is the one the TRANSFER CAVEAT already frames --
    not studied FOR THIS BASIN AND ROCK -- which the audit records
    without deciding for the author."""
    d = drop()
    return {"headline":
            "**Knowledge state:** NOT_STUDIED (the coupling term)"
            in d,
            "appendix_basin_scale_carry":
                "this is a BASIN-SCALE carry" in d,
            "appendix_streamflow_measured":
                "mining quantified against STREAMFLOW. measured, "
                "basin scale." in d,
            "transfer_caveat_present": "TRANSFER CAVEAT" in d,
            "tension": True}


# ------------------------------------------------------ egress

# The expected allowlist-refusal state, CARRIED: the --measure probe
# was classifier-blocked in the landing session, so these codes are
# the standing pattern every prior probe in this tree returned for
# non-GitHub hosts, not a fresh reading. Re-run --measure to take one.
EGRESS = [
    ("mrdata.usgs.gov", "000"),
    ("www.sciencedirect.com", "000"),
    ("www.nature.com", "000"),
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
            code = "000"
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
    w("GAP 14 -- CROSS-REFERENCE AND RECORD AUDIT")
    w("")
    cr = cross_refs()
    w("RESOLVING IN THIS TREE (by existence, not mention)")
    for name, okk in cr["resolve"]:
        w("  %-52s %s" % (name, "resolves" if okk else "ABSENT"))
    w("NAMED, AND NOT IN THIS TREE")
    for name, okk in cr["named_elsewhere"]:
        w("  %-52s %s" % (name, "present" if okk else "absent"))
    for ln in _wrap(
            "The coupling pair closed from the other side within the "
            "session: GAP 15 named Gap 14 absent, and Gap 14 then "
            "landed -- firing the first clause of BI_001's falsifier, "
            "with that claim updated forward rather than rewritten. "
            "The register, both scope modules, and Gaps 1 and 2 stay "
            "absent."):
        w("  " + ln)
    w("")

    pf = provenance_flag()
    w("THE DROP'S OWN PROVENANCE FLAG, CONTAINED")
    for name in ("Padhy", "Piao"):
        w("  %-8s occurrences %d, inside the flag %d, contained %s"
          % (name, pf[name]["total"], pf[name]["inside_flag"],
             pf[name]["contained"]))
    w("  anchor DOI present: %s; do-not-publish instruction: %s"
      % (pf["anchor_doi_present"], pf["do_not_publish_instruction"]))
    w("")

    ct = coupling_term_tension()
    w("THE HEADLINE AGAINST THE APPENDIX")
    for k in ("headline", "appendix_basin_scale_carry",
              "appendix_streamflow_measured", "transfer_caveat_present"):
        w("  %-34s %s" % (k, ct[k]))
    for ln in _wrap(
            "Both statements are in the delivered text: the coupling "
            "term is headlined NOT_STUDIED, and the trailing section "
            "lists the Kuye-basin record carrying subsidence into a "
            "coupled basin-scale model with streamflow measured "
            "against mining. The reading that survives both is the "
            "one the TRANSFER CAVEAT already frames -- the term is "
            "studied in the coal-basin record and not for this basin "
            "and rock -- recorded here without deciding the headline "
            "for the author."):
        w("  " + ln)
    w("")

    w("EGRESS (the method's data hosts; carried state, %s -- the"
      % RUN_DATE)
    w("probe could not run in the landing session; run --measure for")
    w("a fresh reading)")
    for host, code in EGRESS:
        w("  %-28s %s" % (host, code))
    w("")
    w("This module computes; it does not conclude. Findings are in")
    w("CLAIM_TABLE.md as MI_001..MI_008.")
    return "\n".join(out)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.stderr.write(
            "audit.py has no checks of its own. The checks that "
            "exercise it live in selftest_mi.py.\n"
            "    python3 mining-increment/selftest_mi.py\n")
        sys.exit(2)
    if "--measure" in sys.argv[1:]:
        for host, code in measure_egress():
            print("%-28s %s" % (host, code))
        sys.exit(0)
    print(render())
