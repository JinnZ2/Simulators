#!/usr/bin/env python3
"""queue_check.py -- checks on UPGRADE_QUEUE.md, the parked queue of
proposed changes to the falsifier / claim-record format.

This does NOT adopt anything. The queue's own first rule is that nothing
is adopted by being written, and moving an entry to ADOPTED requires its
adopt-test to have run or an explicit recorded decision. So this checker
only verifies what is verifiable WITHOUT adopting:

  1. structure: the queue parses into the tiers it declares (FORCED /
     CANDIDATE / SPECULATIVE) with the entry counts it states, and every
     entry carries the global NOT-ADOPTED status.
  2. adopt-rule classification: per the queue's own rule, an entry that
     only ADDS a field needs no branch entry; one that CHANGES a rule
     does. Each entry's kind is a declared reading of its `form` line.
  3. cross-reference resolution: each entry's referenced artifacts are
     resolved to IN-REPO paths (checked to exist) or marked EXTERNAL /
     UNLANDED -- which is what says whether an adopt-test could run here.

Nothing is fabricated: external corpora (the Kimi/Perplexity/DeepSeek
runs, registrar specs) are marked EXTERNAL, and the in-repo references are
verified against the filesystem.

    python3 upgrade-queue/queue_check.py
Refuses --selftest (checks live in selftest_uq.py). Stdlib only, parses
under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QUEUE = os.path.join(HERE, "UPGRADE_QUEUE.md")

TIER_RE = re.compile(r"^##\s+TIER\s+(\d)\s+—\s+(FORCED|CANDIDATE|SPECULATIVE)", re.I)
ENTRY_RE = re.compile(r"^###\s+(U-\d\d)\s+(.*\S)\s*$")

# Declared readings, transcribed from each entry (marked as readings, not
# parsed): kind per the adopt-rule (ADDS a field vs CHANGES a rule), and the
# adopt-test's runnability HERE. U-09 is the one the queue itself calls "most
# likely to turn into a format rewrite" -> CHANGES. U-10..U-13 are speculative
# and the queue states their placement is Unknown -> kind UNKNOWN.
KIND = {
    "U-01": "ADDS", "U-02": "ADDS", "U-03": "ADDS", "U-04": "ADDS",
    "U-05": "ADDS", "U-06": "ADDS", "U-07": "ADDS", "U-08": "ADDS",
    "U-09": "CHANGES",
    "U-10": "UNKNOWN", "U-11": "UNKNOWN", "U-12": "UNKNOWN", "U-13": "UNKNOWN",
}
ADOPT_TEST = {
    "U-01": "BLOCKED_EXTERNAL",   # needs 20 MEASURED cells; this repo has 1, the 537 are Kimi Run 2
    "U-02": "BLOCKED_EXTERNAL",   # re-run a blind sort on the external corpus
    "U-03": "BLOCKED_EXTERNAL",   # code the 13 distinct transforms (external corpus)
    "U-04": "NONE_NEEDED",        # "the nesting result is the demonstration" (in-repo)
    "U-05": "RUNNABLE_HERE",      # count the fires distribution across one repo (field not yet added)
    "U-06": "NONE_OBVIOUS",
    "U-07": "BLOCKED_UNLANDED",   # "when the FSRI report lands" -- not landed (egress)
    "U-08": "UNTESTED",
    "U-09": "UNTESTED",
    "U-10": "PARKED", "U-11": "PARKED", "U-12": "PARKED", "U-13": "PARKED",
}
# Declared cross-references: (name, in-repo path or None=EXTERNAL). In-repo
# paths are verified to exist by resolve_refs(); None marks an external
# corpus / registrar / unlanded artifact the queue names.
CROSS_REFS = {
    "U-01": [("ADDENDUM 02 (the cut rule)", "dependency-survey/ADDENDUM_02.md"),
             ("CIPM / CMC uncertainty budget", None),
             ("Kimi Run 2 (~537 MEASURED cells)", None)],
    "U-02": [("the speedup-cluster collapse (recorded)", "dependency-survey/RESULT_repair_adjacency.md"),
             ("Kimi / Perplexity / DeepSeek runs", None)],
    "U-03": [("ENG-3 sign inversion (recorded §5)", "dependency-survey/RESULT_repair_adjacency.md"),
             ("the 13 distinct transforms", None)],
    "U-04": [("the nesting result", "dependency-survey/RESULT_repair_adjacency.md"),
             ("the crossmodel nesting", "dependency-survey/taxonomy_replication.py")],
    "U-05": [("registrar when-it-fires candidate", "merge-path/UNITS.md"),
             ("CT.gov / proof assistant / nanopub behavior", None)],
    "U-06": [("branch search / prereg candidate", "merge-path/BRANCH_SEARCH.md"),
             ("CT.gov, OSF preregistration", None)],
    "U-07": [("tenability.py one-link chain in prose", "railcar-containment/tenability.py"),
             ("FSRI hold marker", "railcar-containment/FETCH_REQUIRED.md"),
             ("CMC traceability chain", None)],
    "U-08": [("mechanical-check reverse gap", "merge-path/REVERSE_GAPS.md"),
             ("proof assistants", None)],
    "U-09": [("provenance-graph reverse gap", "merge-path/REVERSE_GAPS.md"),
             ("nanopublications provenance graph", None)],
    "U-10": [("P5 lag declaration", "cooperative-substrate/WORK_ORDER_V2.md")],
    "U-11": [("§4 reverse-gap discipline", "merge-path/REVERSE_GAPS.md")],
    "U-12": [("railcar ENVELOPE", "railcar-containment/README.md")],
    "U-13": [("K4 N=4 finding (recorded)", "dependency-survey/CLAIM_TABLE.md"),
             ("K4 in the external runs", None)],
}
EXPECTED_TIER_COUNTS = {1: 4, 2: 5, 3: 4}


def parse_queue(path=QUEUE):
    """Returns {'entries': {id: {tier, tier_name, title}}, 'global_not_adopted': bool,
    'status_lines': {id: bool}, 'exclusions': [..]}."""
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    entries = {}
    status_lines = {}
    tier = None
    tier_name = None
    cur = None
    for ln in lines:
        mt = TIER_RE.match(ln)
        if mt:
            tier = int(mt.group(1))
            tier_name = mt.group(2).upper()
            continue
        me = ENTRY_RE.match(ln)
        if me:
            cur = me.group(1)
            entries[cur] = {"tier": tier, "tier_name": tier_name, "title": me.group(2)}
            continue
        if cur and re.match(r"^status\s", ln.strip()):
            status_lines[cur] = "NOT ADOPTED" in ln.upper()
    global_not_adopted = "STATUS OF EVERY ENTRY BELOW: NOT ADOPTED" in text.upper()
    exclusions = []
    if "## NOT ON THIS LIST" in text:
        tail = text.split("## NOT ON THIS LIST", 1)[1]
        for key in ("a confidence score per claim", "a severity or priority rank",
                    "a verdict field on a branch"):
            if key in tail:
                exclusions.append(key)
    return {"entries": entries, "global_not_adopted": global_not_adopted,
            "status_lines": status_lines, "exclusions": exclusions}


def resolve_refs():
    """Each entry's cross-references resolved: IN-REPO (path exists),
    MISSING (declared in-repo but not found -- a defect), or EXTERNAL."""
    out = {}
    for eid, refs in CROSS_REFS.items():
        rows = []
        for name, path in refs:
            if path is None:
                rows.append({"name": name, "state": "EXTERNAL", "path": None})
            elif os.path.exists(os.path.join(ROOT, path)):
                rows.append({"name": name, "state": "IN-REPO", "path": path})
            else:
                rows.append({"name": name, "state": "MISSING", "path": path})
        out[eid] = rows
    return out


def tier_counts(parsed):
    counts = {1: 0, 2: 0, 3: 0}
    for e in parsed["entries"].values():
        if e["tier"] in counts:
            counts[e["tier"]] += 1
    return counts


def report():
    p = parse_queue()
    refs = resolve_refs()
    tc = tier_counts(p)
    L = ["upgrade-queue check -- NOTHING here is adopted (the queue's own rule)",
         "structure: %d entries; tiers FORCED=%d CANDIDATE=%d SPECULATIVE=%d; global NOT-ADOPTED=%s"
         % (len(p["entries"]), tc[1], tc[2], tc[3], p["global_not_adopted"]),
         ""]
    for eid in sorted(p["entries"]):
        e = p["entries"][eid]
        rr = refs.get(eid, [])
        inrepo = sum(1 for r in rr if r["state"] == "IN-REPO")
        ext = sum(1 for r in rr if r["state"] == "EXTERNAL")
        miss = sum(1 for r in rr if r["state"] == "MISSING")
        L.append("%s [T%d %s] kind=%s adopt-test=%s  refs: %d in-repo / %d external%s"
                 % (eid, e["tier"], e["tier_name"], KIND.get(eid, "?"),
                    ADOPT_TEST.get(eid, "?"), inrepo, ext,
                    "" if not miss else " / %d MISSING" % miss))
    L.append("")
    changes = [e for e in KIND if KIND[e] == "CHANGES"]
    L.append("adopt-rule: entries that CHANGE a rule (need a branch entry if adopted): %s"
             % (", ".join(sorted(changes)) or "none"))
    L.append("            all others ADD a field (no branch entry) or are UNKNOWN (speculative)")
    runnable = [e for e in ADOPT_TEST if ADOPT_TEST[e] == "RUNNABLE_HERE"]
    L.append("adopt-tests runnable in THIS repo (field would still need adding first): %s"
             % (", ".join(sorted(runnable)) or "none"))
    L.append("exclusions recorded (NOT ON THIS LIST): %d" % len(p["exclusions"]))
    return "\n".join(L)


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        print("queue_check has no selftest; run selftest_uq.py", file=sys.stderr)
        sys.exit(2)
    print(report())
