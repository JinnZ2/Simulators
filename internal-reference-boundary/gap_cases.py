#!/usr/bin/env python3
"""
Records for the gap-transfer instrument.

gap-01 is the handoff's WORKED CASE, CARRIED. Every field in it is
something HANDOFF.md states, and every field HANDOFF.md does not state is
left UNDECLARED rather than filled in. It names the two hosts, the shape
of the gap, the short outcome window, and the later swing to blanket
restriction; it gives no population, no horizon value and no unit, so
this record gives none either. What the instrument returns on it is a
reading of the DELIVERED RESOLUTION, not a reading of any treatment,
prescriber, patient or policy.

gap-02 and gap-03 are CONSTRUCTED, abstract, and exist to show that the
instrument's other branches are reachable -- a carrier, a gap that was
closed rather than transferred, a successor that is not the carrier. They
are not about anything.

NO EXPECTED VERDICT LIVES HERE.

CC0. Stdlib only. Parses under 3.9.
"""

UNDECLARED = "UNDECLARED"


GAPS = [
    {
        "gap_id": "gap-01",
        "provenance": "CARRIED from HANDOFF.md, unverified",
        "gap": ("downstream course, outside the outcome window the "
                "measurand closes at"),
        "unit_of_the_missing_measurement": UNDECLARED,
        "hosts": [
            {
                "name": "host_1 (named in the handoff)",
                # The handoff states a SHORT outcome window inside the
                # measurand. It states no value and no unit, so the
                # horizon is not declared here.
                "population": UNDECLARED,
                "accounting_horizon": UNDECLARED,
                "horizon_unit": UNDECLARED,
                "gap_measured": UNDECLARED,
                "direction": "PERMISSIVE",
                "definer_rung": "INSIDE_SAME_FIELD",
                "handoff_states": ("finding true inside its boundary; short "
                                   "outcome window inside the measurand, "
                                   "downstream course outside it"),
            },
            {
                "name": "host_2 (named in the handoff)",
                "population": UNDECLARED,
                "accounting_horizon": UNDECLARED,
                "horizon_unit": UNDECLARED,
                "gap_measured": UNDECLARED,
                "direction": "PERMISSIVE",
                "definer_rung": "INSIDE_SAME_FIELD",
                "handoff_states": ("the practice that inherited the "
                                   "population and the accounting horizon"),
            },
            {
                "name": "host_3 (the later swing)",
                "population": UNDECLARED,
                "accounting_horizon": UNDECLARED,
                "horizon_unit": UNDECLARED,
                "gap_measured": UNDECLARED,
                "direction": "RESTRICTIVE",
                "definer_rung": UNDECLARED,
                "handoff_states": ("later swing to blanket restriction = "
                                   "same defect running the other way"),
            },
        ],
    },
    {
        "gap_id": "gap-02",
        "provenance": "CONSTRUCTED",
        "gap": "what happens after the window closes",
        "unit_of_the_missing_measurement": "events per person-year",
        "hosts": [
            {"name": "carrier_a", "population": "pop_P",
             "accounting_horizon": 90, "horizon_unit": "days",
             "gap_measured": False, "direction": "PERMISSIVE",
             "definer_rung": "INSIDE_SAME_BODY"},
            {"name": "carrier_b", "population": "pop_P",
             "accounting_horizon": 90, "horizon_unit": "days",
             "gap_measured": False, "direction": "PERMISSIVE",
             "definer_rung": "INSIDE_SAME_BODY"},
            {"name": "carrier_c", "population": "pop_P",
             "accounting_horizon": 90, "horizon_unit": "days",
             "gap_measured": False, "direction": "RESTRICTIVE",
             "definer_rung": "INSIDE_SAME_FIELD"},
        ],
    },
    {
        "gap_id": "gap-03",
        "provenance": "CONSTRUCTED",
        "gap": "what happens after the window closes",
        "unit_of_the_missing_measurement": "events per person-year",
        "hosts": [
            {"name": "origin", "population": "pop_Q",
             "accounting_horizon": 30, "horizon_unit": "days",
             "gap_measured": False, "direction": "PERMISSIVE",
             "definer_rung": "INSIDE_SAME_BODY"},
            # inherits the population, not the horizon
            {"name": "partial", "population": "pop_Q",
             "accounting_horizon": 3650, "horizon_unit": "days",
             "gap_measured": False, "direction": "PERMISSIVE",
             "definer_rung": "OUTSIDE_FIELD"},
            # measures the gap: closed, not transferred
            {"name": "closer", "population": "pop_Q",
             "accounting_horizon": 3650, "horizon_unit": "days",
             "gap_measured": True, "direction": "PERMISSIVE",
             "definer_rung": "OUTSIDE_FIELD"},
        ],
    },
]


# Candidates for the handoff's prediction, run by locate_carrier: given a
# host whose practice ended, which successors inherited BOTH its
# population and its accounting horizon. CONSTRUCTED and abstract.
CANDIDATE_SET = {
    "from": {"name": "ended_practice", "population": "pop_R",
             "accounting_horizon": 60, "horizon_unit": "days",
             "gap_measured": False, "direction": "PERMISSIVE"},
    "candidates": [
        {"name": "cand_same_pop_same_horizon", "population": "pop_R",
         "accounting_horizon": 60, "horizon_unit": "days",
         "gap_measured": False, "direction": "PERMISSIVE"},
        {"name": "cand_same_pop_long_horizon", "population": "pop_R",
         "accounting_horizon": 3650, "horizon_unit": "days",
         "gap_measured": False, "direction": "PERMISSIVE"},
        {"name": "cand_other_pop_same_horizon", "population": "pop_S",
         "accounting_horizon": 60, "horizon_unit": "days",
         "gap_measured": False, "direction": "PERMISSIVE"},
        {"name": "cand_overlap_declared", "population": "pop_S",
         "population_overlap": 0.80,
         "accounting_horizon": 60, "horizon_unit": "days",
         "gap_measured": False, "direction": "PERMISSIVE"},
        {"name": "cand_horizon_in_another_unit", "population": "pop_R",
         "accounting_horizon": 2, "horizon_unit": "months",
         "gap_measured": False, "direction": "PERMISSIVE"},
    ],
}
