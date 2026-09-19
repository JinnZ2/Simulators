# SPDX-License-Identifier: CC0-1.0
"""
trust_provenance.py -- WO-1 second-order gap: the provenance of the trust
assignment itself.

The order: return-path filtration scores the PAYLOAD, but the trust score is
itself a chained artifact with its own provenance, and that provenance is not
examined. There is no common object to audit, so nobody can state whether
scorer provenance is carried at all.

This is the order's runnable step 2 -- a SPECIFICATION exercise, no vendor
internals -- made concrete:

(1) PROVENANCE_SPEC states what a trust assignment would have to carry for the
    assignment (not just the payload) to be auditable: the scored payload, the
    scorer's identity, the scorer's OWN provenance (the score is a chained
    artifact, so this is recursive), and the policy applied.

(2) assignment_auditability classifies a record. The load-bearing distinction
    is between UNEXAMINED and NOT_AUDITABLE: a record that does not DECLARE its
    scorer's provenance is UNEXAMINED -- the order's "nobody can state whether
    scorer provenance is carried at all", an undetermined state, not a
    negative -- while a record that declares the provenance absent is
    NOT_AUDITABLE, a known negative. Collapsing the two would read a silence as
    a finding.

(3) common_object_exists records the order's consequence: implementation
    varies by vendor and no vendor internals are used or sought, so there is no
    common object to audit and the order's claim ("scorer provenance goes
    unexamined") stays UNVERIFIED here -- plausible, not established.

Nothing here inspects any vendor's scorer. The records are CONSTRUCTED to
exercise the classifier's states.

Stdlib only. Parses under 3.9. ASCII only. CC0.

    python3 trust_provenance.py            # render the spec and the states
    python3 trust_provenance.py --choices  # the [CHOICE n] markers
    python3 test_chain.py                  # the checks; prints their count
"""

from __future__ import annotations

import os
import sys

# What a trust assignment must carry for the ASSIGNMENT to be auditable, not
# merely the payload. The scorer's own provenance is itself required, because
# the score is a chained artifact -- that recursion is the second-order gap.
PROVENANCE_SPEC = [
    "scored_payload",       # what was scored
    "scorer_id",            # which scorer produced the assignment
    "scorer_provenance",    # the scorer's own inputs / model / version
    "policy_applied",       # the policy under which the score was assigned
]

# [CHOICE 1] scorer_provenance is treated as DECLARED-ABSENT only when the key
#   is present with an explicit empty/None value; a MISSING key is UNEXAMINED.
#   The difference is the whole point of the second-order gap.
CHOICES = {
    1: "a MISSING scorer_provenance key is UNEXAMINED (cannot say); an "
       "explicitly empty one is NOT_AUDITABLE (declared absent) -- a silence "
       "and a known negative are different states",
}


def _declared_absent(value):
    return value is None or value == "" or value == []


def assignment_auditability(record):
    """Classify a trust-assignment record.

    UNEXAMINED     -- scorer_provenance key is missing: nobody can say whether
                      it is carried (the order's second-order gap)
    NOT_AUDITABLE  -- scorer_provenance is declared absent, or another required
                      field is missing
    AUDITABLE      -- every PROVENANCE_SPEC field is present and non-empty
    """
    if "scorer_provenance" not in record:
        return {"verdict": "UNEXAMINED", "missing": ["scorer_provenance"],
                "why": "the record does not declare scorer provenance; whether "
                       "it is carried cannot be stated from this record"}
    missing = [f for f in PROVENANCE_SPEC if f not in record]
    if missing:
        return {"verdict": "NOT_AUDITABLE", "missing": missing,
                "why": "a required field is absent from the record"}
    absent = [f for f in PROVENANCE_SPEC if _declared_absent(record[f])]
    if absent:
        return {"verdict": "NOT_AUDITABLE", "missing": absent,
                "why": "a required field is declared present but empty"}
    return {"verdict": "AUDITABLE", "missing": [],
            "why": "every field the spec requires is present and non-empty"}


def spec_satisfied(record):
    """True iff assignment_auditability reads AUDITABLE. A thin predicate over
    the classifier, so the spec and the verdict cannot drift."""
    return assignment_auditability(record)["verdict"] == "AUDITABLE"


def common_object_exists():
    """The order's consequence, carried. Implementation varies by vendor and
    no vendor internals are used, so there is no common object to audit; the
    order's claim stays UNVERIFIED here."""
    return {"exists": False,
            "why": "implementation varies by vendor, no vendor internals used "
                   "or sought; the claim that scorer provenance goes unexamined "
                   "is UNVERIFIED -- plausible, not established"}


# CONSTRUCTED records exercising each state.
def sample_records():
    return {
        "payload_only": {"scored_payload": "p", "score": 0.9},
        "declared_absent": {"scored_payload": "p", "scorer_id": "s",
                            "scorer_provenance": None, "policy_applied": "pol"},
        "auditable": {"scored_payload": "p", "scorer_id": "s",
                      "scorer_provenance": {"model": "m", "inputs": ["i"]},
                      "policy_applied": "pol"},
    }


def render():
    out = []
    out.append("WO-1 SECOND-ORDER GAP -- provenance of the trust assignment")
    out.append("CONSTRUCTED records. No vendor scorer is inspected.")
    out.append("")
    out.append("[CHOICE 1] %s" % CHOICES[1])
    out.append("")

    out.append("What an auditable trust ASSIGNMENT has to carry (the spec):")
    for f in PROVENANCE_SPEC:
        out.append("  - %s" % f)
    out.append("  scorer_provenance is itself required: the score is a chained "
               "artifact, so the recursion is the gap.")
    out.append("")

    out.append("Classifier states (the load-bearing split is UNEXAMINED vs "
               "NOT_AUDITABLE):")
    for name, rec in sample_records().items():
        r = assignment_auditability(rec)
        out.append("  %-16s -> %-13s (%s)"
                   % (name, r["verdict"],
                      ",".join(r["missing"]) if r["missing"] else "complete"))
    out.append("")

    co = common_object_exists()
    out.append("Consequence, carried: a common object to audit exists = %s"
               % co["exists"])
    out.append("  so the order's claim stays UNVERIFIED here -- plausible, not "
               "established.")
    return "\n".join(out)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "trust_provenance.py has no --selftest. The checks are in "
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
