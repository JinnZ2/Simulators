#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
agents.py - the AGENTS declaration for S10, before any equation.

Folder rule, adopted in S4: the AGENTS section comes first and a missing agent
is a VISIBLE BLANK, never an omission buried in prose. The S10 spec declares
its own blank -- "anyone the model cannot represent; list explicitly" -- so
the blank here is filled with an enumeration of who is outside the model,
which is a stronger form of the rule than S9's single empty slot.

stdlib only, CC0.
"""

AGENTS = [
    {"agent": "holder",
     "capabilities": ["works", "earns", "holds or loses tenure",
                      "may observe"]},
    {"agent": "assessor",
     "capabilities": ["scores contribution from available record"]},
    {"agent": "land",
     "capabilities": ["state changes on a slow clock",
                      "readable only by continuous presence"]},
    {"agent": "not_representable",
     "capabilities": []},
]

# The blank, enumerated. Each entry is someone whose position bears on the
# outcome and who has no state variable in any module here.
NOT_REPRESENTABLE = [
    {"party": "prior holders", "why": "tenure history is a scalar in M1; "
                                      "who held before and under what terms "
                                      "is not represented"},
    {"party": "co-resident household members",
     "why": "hours_available is per holder. Anyone whose labour frees or "
            "consumes those hours has no term"},
    {"party": "the party setting tenure_cost",
     "why": "tenure_cost is an exogenous constant. Nothing in the model "
            "determines it, so no incentive running through it can be read"},
    {"party": "non-holders present on the land",
     "why": "presence is derived from tenure in M1, so continuous observers "
            "without tenure cannot exist in this model at all"},
    {"party": "the land's other couplings",
     "why": "land state is a single slow variable. Watershed, neighbours "
            "and weather enter only through it"},
]


def agent_table():
    return [{"agent": a["agent"],
             "capabilities": a["capabilities"] or ["[BLANK]"],
             "is_blank": not a["capabilities"]} for a in AGENTS]


def blank_detail():
    return {"agent": "not_representable",
            "enumerated": len(NOT_REPRESENTABLE),
            "parties": NOT_REPRESENTABLE,
            "note": "the spec asked for the blank to be listed explicitly "
                    "rather than left empty. Five parties are named; the "
                    "fourth is load-bearing, because deriving presence from "
                    "tenure makes a continuous observer without tenure "
                    "unrepresentable, and that is the position most likely "
                    "to hold the knowledge the model is about"}
