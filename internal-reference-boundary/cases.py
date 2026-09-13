#!/usr/bin/env python3
"""
Constructed corpus for the internal-reference boundary instrument.

EVERY CASE IS CONSTRUCTED. No real field, body, journal, company,
institution or person is coded anywhere in this file. The six ids map to
the six instances the handoff's invariant names, and each was authored
from the SHAPE of that instance, not to make any radial come out a
particular way.

NO EXPECTED VERDICT LIVES HERE. Whatever a radial returns on a case is
computed by radials.py and asserted, where it is asserted at all, in
test_boundary.py -- so no case can agree with the instrument by
construction.

The handoff's empirical anchors are carried in ANCHORS below, verbatim
and checked against nothing.

CC0. Stdlib only. Parses under 3.9.
"""

# Carried from HANDOFF.md, unverified. Egress here is an allowlist and
# none of these was checked against a source.
ANCHORS = {
    "R1_low": {"stated": "free-range cattle ~0",
               "as_rate_per_occasion": 0.0,
               "note": "a rate; sits on the [CHOICE 1] scale directly"},
    "R1_high": {"stated": "gated bathroom ~continuous",
                "as_rate_per_occasion": 1.0,
                "note": ("a saturation statement, not a measurement. On a "
                         "per-time scale it has no value; on the "
                         "[CHOICE 1] per-occasion scale it is 1.0")},
    "R3": {"stated": ("~1 finding per 10,000 researchers/yr vs 25-50% "
                      "self-reported incidence"),
           "consequence_rate_per_person_year": 1e-4,
           "incidence_lo": 0.25, "incidence_hi": 0.50,
           "incidence_window": "UNDECLARED",
           "note": ("the two legs sit on different time bases; the window "
                    "is not stated")},
    "R7_latency": {"stated": "anonymous-post loop, ~1-2yr latency",
                   "years_lo": 1.0, "years_hi": 2.0},
}


CASES = [
    {
        "id": "silo-01",
        "instance": "disciplinary_silo",
        "provenance": "CONSTRUCTED",
        "what_the_boundary_is": "a question is inside the field or it is not",
        "who_draws_it": "the field's own reviewers and journals",

        "encounters": 8, "occasions_of_need": 10,
        "definer_rung": "INSIDE_SAME_FIELD",
        "feedback_distance": "UNDECLARED",

        "routability": 0.50, "damage_capacity": 0.30,

        "origins": ["origin_a", "origin_b", "origin_c", "origin_d"],
        "origin_coupling": [
            {"i": 0, "j": 1, "funders": 0.90, "instruments": 0.80},
            {"i": 0, "j": 2, "citation_ancestry": 0.70},
            {"i": 1, "j": 2, "funders": 0.90},
            {"i": 0, "j": 3, "training_lineage": 0.10},
            {"i": 1, "j": 3, "training_lineage": 0.10},
            {"i": 2, "j": 3, "training_lineage": 0.10},
        ],
        "dependency_depth": 0.90,
        "necessity": 0.05,

        "confirming_entries": 12, "contradicting_entries": 3,
        "pariah_set": [
            {"ref": "p1", "rejection_reason": "METHOD",
             "outcome": "stayed_rejected"},
            {"ref": "p2", "rejection_reason": "METHOD",
             "outcome": "stayed_rejected"},
            {"ref": "p3", "rejection_reason": "CONCLUSION",
             "outcome": "came_in_without_credit",
             "labelled_year": 1978, "absorbed_year": 1996},
            {"ref": "p4", "rejection_reason": "CONCLUSION",
             "outcome": "came_in_without_credit",
             "labelled_year": 1985, "absorbed_year": 2001},
            {"ref": "p5", "rejection_reason": "CONCLUSION",
             "outcome": "came_in_with_credit",
             "labelled_year": 1990, "absorbed_year": 2004},
            {"ref": "p6", "rejection_reason": "CONCLUSION",
             "outcome": "stayed_rejected"},
        ],
    },
    {
        "id": "cred-01",
        "instance": "credential",
        "provenance": "CONSTRUCTED",
        "what_the_boundary_is": "who may practise",
        "who_draws_it": "the practitioners' own licensing body",

        "encounters": 19, "occasions_of_need": 20,
        "definer_rung": "INSIDE_SAME_BODY",
        "feedback_distance": "UNDECLARED",

        "consequence_rate": 2e-3,
        "incidence_lo": 0.10, "incidence_hi": 0.20,
        "incidence_window": "per_year",

        "routability": 0.20, "damage_capacity": 0.40,
    },
    {
        "id": "eff-01",
        "instance": "efficiency_metric",
        "provenance": "CONSTRUCTED",
        "what_the_boundary_is": "what counts in the numerator and what is "
                               "outside the accounting",
        "who_draws_it": "the operator being measured",

        "encounters": 30, "occasions_of_need": 30,
        "definer_rung": "INSIDE_SAME_BODY",
        # The handoff's RESULT section: thirty years sits on the METHOD,
        # not the difficulty of the material. Carried as a declared field
        # beside R2 and never merged into it.
        "feedback_distance": 30.0,

        "routability": 0.60, "damage_capacity": 0.50,

        "exemption_provenance": "survived_external_test",
        "extensions": [
            {"case": "x1", "extended": True, "benefit_to_claimant": 0.20},
            {"case": "x2", "extended": True, "benefit_to_claimant": 0.80},
            {"case": "x3", "extended": True, "benefit_to_claimant": 0.50},
            {"case": "x4", "extended": True, "benefit_to_claimant": 0.40},
            {"case": "x5", "extended": False, "benefit_to_claimant": 0.50},
        ],
    },
    {
        "id": "diag-01",
        "instance": "diagnostic_criterion",
        "provenance": "CONSTRUCTED",
        "what_the_boundary_is": "the presentation is the named condition or "
                               "it is not",
        "who_draws_it": "the committee that writes the criterion",

        "encounters": 9, "occasions_of_need": 10,
        "definer_rung": "INSIDE_SAME_FIELD",
        "feedback_distance": "UNDECLARED",

        "routability": 0.30, "damage_capacity": 0.70,

        # Contradicting entries are zero: exercises CONFIRMING_ONLY, which
        # the handoff reads as selection rather than evaluation.
        "confirming_entries": 5, "contradicting_entries": 0,
    },
    {
        "id": "shell-01",
        "instance": "corporate_liability_shell",
        "provenance": "CONSTRUCTED",
        "what_the_boundary_is": "which balance sheet the consequence lands "
                               "on",
        "who_draws_it": "the parent that incorporated the shell",

        "encounters": 1, "occasions_of_need": 10,
        "definer_rung": "INSIDE_SAME_BODY",
        "feedback_distance": "UNDECLARED",

        "routability": 0.95, "damage_capacity": 0.90,

        "exemption_provenance": "self_designated",
        "extensions": [
            {"case": "y1", "extended": True, "benefit_to_claimant": 0.90},
            {"case": "y2", "extended": True, "benefit_to_claimant": 0.80},
            {"case": "y3", "extended": False, "benefit_to_claimant": 0.10},
            {"case": "y4", "extended": False, "benefit_to_claimant": 0.20},
        ],
    },
    {
        "id": "selfinv-01",
        "instance": "institutional_self_investigation",
        "provenance": "CONSTRUCTED",
        "what_the_boundary_is": "what counts as a finding",
        "who_draws_it": "the institution investigating itself",

        "encounters": 1, "occasions_of_need": 20,
        "definer_rung": "INSIDE_SAME_BODY",
        "feedback_distance": "UNDECLARED",

        # The handoff's R3 anchor, carried. incidence_window is left
        # UNDECLARED because the handoff does not state one; that absence
        # is the reading, not an omission in this file.
        "consequence_rate": 1e-4,
        "incidence_lo": 0.25, "incidence_hi": 0.50,
        "incidence_window": "UNDECLARED",

        "routability": 0.80, "damage_capacity": 0.85,

        "exemption_provenance": "self_designated",
        "extensions": [
            {"case": "z1", "extended": True, "benefit_to_claimant": 0.50},
            {"case": "z2", "extended": True, "benefit_to_claimant": 0.50},
            {"case": "z3", "extended": True, "benefit_to_claimant": 0.50},
            {"case": "z4", "extended": True, "benefit_to_claimant": 0.50},
            {"case": "z5", "extended": False, "benefit_to_claimant": 0.50},
        ],
    },
]


# The fold-test's discriminating cell -- an externally-held metric with a
# self-designated exemption -- is deliberately NOT in CASES. Authoring it
# into the corpus would close the handoff's own OPEN item by writing the
# answer down. It is constructed inside test_boundary.py instead, where
# what it shows is that the test discriminates, which is a property of
# the test and not of any boundary.
FOLD_CELL_ABSENT_ON_PURPOSE = True
