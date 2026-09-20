# SPDX-License-Identifier: CC0-1.0
"""
chain_position.py -- WO-1 MEASURAND: can a container detect its chain position?

The order's quantity is CHAIN POSITION, not task content. A container is
locally correct by construction, so compliance is what renders the chain
invisible. The order runs the standard down to a fork it does not select:

  HORN A  awareness comes from OUTSIDE the container
          -> the outside thing is itself a container with its own local
             correctness, so the problem RELOCATES, it does not resolve
  HORN B  the container asks the question of ITSELF
          -> it would be reasoning about something for which it has no
             evidence -> EVIDENCE_ABSENT

This module builds three things, all decidable:

(1) clause_audit -- the order's runnable step 1. The OWASP clauses the order
    lists (fetched and verified by the operator, carried here, NOT re-fetched;
    egress refuses the standard) are each classified by WHERE the observability
    sits. The order's expected result is that NONE places chain-position
    information inside the executing agent, and the null result IS the finding.
    Not constant: a constructed clause that DOES place it inside raises the
    count, so the zero is a measurement, not a floor.

(2) horn_fork -- reports each horn's failure mode. Neither is selected;
    selecting one is downstream work, as the order says.

(3) evidence_check -- the order's step 3. Given a container's local evidence,
    does any element carry chain-position information? A locally-correct
    container has none, so the check returns EVIDENCE_ABSENT with what would be
    needed; hand it a whole-chain manifest and it can answer, so the absence is
    a property of the locally-correct container, not of the check.

No vendor internals are used or sought. Nothing here is a claim about any
deployed system; the clauses are the public standard as the order carried it,
and the containers are CONSTRUCTED.

Stdlib only. Parses under 3.9. ASCII only. CC0.

    python3 chain_position.py            # render the audit and the fork
    python3 chain_position.py --choices  # the [CHOICE n] markers
    python3 test_chain.py                # the checks; prints their count
"""

from __future__ import annotations

import os
import sys

# Loci a clause can place observability at. INSIDE_CONTAINER is the one the
# order's step 1 looks for and expects to find empty.
GATEWAY = "GATEWAY"
INSIDE_CONTAINER = "INSIDE_CONTAINER"
UNDECLARED = "UNDECLARED"
LOCI = (GATEWAY, INSIDE_CONTAINER, UNDECLARED)

# The order's own listed clauses, carried verbatim in substance. `locus` is the
# order's DERIVED reading: all of them sit in the gateway's external top-down
# view. Marked source=order so a reader sees these were carried, not re-fetched.
CLAUSES = [
    {"id": "ACS-1", "text": "per-agent isolation and lineage tracking",
     "locus": GATEWAY, "source": "order"},
    {"id": "ACS-2", "text": "gateway traces every request to originating "
     "user session", "locus": GATEWAY, "source": "order"},
    {"id": "ACS-3", "text": "cross-agent state transfer requires explicit "
     "policy authorization", "locus": GATEWAY, "source": "order"},
    {"id": "ACS-4", "text": "provenance and trust status retained per "
     "retrieved item", "locus": GATEWAY, "source": "order"},
    {"id": "ACS-5", "text": "runtime interception via middleware hooks",
     "locus": GATEWAY, "source": "order"},
]

# [CHOICE 1] a clause whose locus is not one of LOCI reads UNDECLARED rather
#   than raising -- an unclassified clause is a gap in the reading, not a
#   malformed record, and the order's audit should surface it as its own state.
# [CHOICE 2] the audit is run over the order's carried clause set by default;
#   a caller passes its own list to audit a different standard.
CHOICES = {
    1: "an out-of-vocabulary locus reads UNDECLARED rather than raising -- an "
       "unclassified clause is a third state, not a malformed record",
    2: "the default clause set is the order's carried OWASP list; a caller "
       "passes another list to audit a different standard",
}


def clause_audit(clauses=None):
    """Step 1. Classify each clause by locus and report whether any places
    chain-position information inside the executing agent. The order's expected
    result is 0; the null result is the finding."""
    if clauses is None:
        clauses = CLAUSES
    counts = {loc: 0 for loc in LOCI}
    for c in clauses:
        loc = c.get("locus")
        if loc not in LOCI:
            loc = UNDECLARED                    # [CHOICE 1]
        counts[loc] += 1
    inside = counts[INSIDE_CONTAINER]
    if inside == 0:
        verdict = "NULL_RESULT_no_clause_places_position_inside"
    else:
        verdict = "SOME_CLAUSE_places_position_inside"
    return {"n_clauses": len(clauses), "counts": counts,
            "inside_container": inside, "verdict": verdict}


# The two horns and their failure modes. Neither is selected.
HORN_A = "OUTSIDE"
HORN_B = "SELF"


def horn_fork(source):
    """Report the failure mode of taking chain-position awareness from a given
    source. OUTSIDE relocates (the outside thing is another container); SELF is
    evidence-absent (reasoning with no evidence). Returns None-shaped
    UNDEFINED for an unknown source rather than guessing a horn."""
    if source == HORN_A:
        return {"horn": "A", "source": source, "failure": "RELOCATES",
                "why": "the outside thing is itself a container with its own "
                       "local correctness; the locus relocates, it does not "
                       "resolve"}
    if source == HORN_B:
        return {"horn": "B", "source": source, "failure": "EVIDENCE_ABSENT",
                "why": "the container would be reasoning about something for "
                       "which it holds no evidence"}
    return {"horn": None, "source": source, "failure": "UNDEFINED",
            "why": "source is neither OUTSIDE nor SELF; no horn is selected "
                   "here and none is invented"}


def evidence_check(evidence):
    """Step 3, Horn B attempted. `evidence` is a list of the container's local
    elements, each a dict with `carries_chain_position` (bool). A locally
    correct container carries none, so the container cannot answer; the return
    names what would be needed. Hand it an element that carries chain position
    (a whole-chain manifest) and it can answer -- so EVIDENCE_ABSENT is a
    property of the locally-correct container, not of this check."""
    carriers = [e for e in evidence if e.get("carries_chain_position")]
    if carriers:
        return {"can_answer": True, "state": "EVIDENCE_PRESENT",
                "carriers": [e.get("id") for e in carriers],
                "would_need": []}
    return {"can_answer": False, "state": "EVIDENCE_ABSENT",
            "carriers": [],
            "would_need": ["an observation of a step outside this boundary; "
                           "by construction the container does not hold one"]}


def locally_correct_container():
    """A CONSTRUCTED container that is locally correct by construction: it
    holds its task, its inputs and its own state, and none of these carries
    chain position. The object the order describes."""
    return [
        {"id": "task", "carries_chain_position": False},
        {"id": "inputs", "carries_chain_position": False},
        {"id": "own_state", "carries_chain_position": False},
    ]


def render():
    out = []
    out.append("WO-1 MEASURAND -- can a container detect its chain position?")
    out.append("CONSTRUCTED containers; OWASP clauses carried from the order, "
               "not re-fetched. No vendor internals.")
    out.append("")
    out.append("[CHOICE 1] %s" % CHOICES[1])
    out.append("[CHOICE 2] %s" % CHOICES[2])
    out.append("")

    out.append("Step 1 -- clause audit (locus of each requirement):")
    a = clause_audit()
    for c in CLAUSES:
        out.append("  %-6s %-9s %s" % (c["id"], c["locus"], c["text"]))
    out.append("  -> %d clauses; inside the executing agent: %d"
               % (a["n_clauses"], a["inside_container"]))
    out.append("  -> %s" % a["verdict"])
    out.append("  the null result is the finding: lineage EXISTS and the "
               "container still cannot see it.")
    out.append("")

    out.append("  not constant -- a constructed clause that DOES place "
               "position inside:")
    demo = CLAUSES + [{"id": "X-hyp", "text": "the agent is told its index in "
                       "the chain", "locus": INSIDE_CONTAINER,
                       "source": "constructed"}]
    ad = clause_audit(demo)
    out.append("    inside the executing agent: %d  -> %s"
               % (ad["inside_container"], ad["verdict"]))
    out.append("")

    out.append("The fork the order does not select:")
    for src in (HORN_A, HORN_B):
        f = horn_fork(src)
        out.append("  HORN %s (%s): %s -- %s"
                   % (f["horn"], f["source"], f["failure"], f["why"]))
    out.append("")

    out.append("Step 3 -- Horn B on a locally-correct container:")
    ev = evidence_check(locally_correct_container())
    out.append("  can answer chain position: %s (%s)"
               % (ev["can_answer"], ev["state"]))
    out.append("  would need: %s" % ev["would_need"][0])
    got = evidence_check(locally_correct_container()
                         + [{"id": "chain_manifest",
                             "carries_chain_position": True}])
    out.append("  with a whole-chain manifest handed in: can answer = %s (%s)"
               % (got["can_answer"], got["state"]))
    out.append("  so the absence is the container's, not the check's.")
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "chain_position.py has no --selftest. The checks are in "
            "test_chain.py:\n    python3 %s\n"
            % os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "test_chain.py"))
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
