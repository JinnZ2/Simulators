#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
m1_tenure_budget.py - holding land requires money; money requires hours.

    python3 m1_tenure_budget.py [--selftest]

An accounting identity. No moral term appears anywhere in this module: it
converts a tenure obligation and a wage into hours, and reports what is left.

inputs   tenure_cost per period, wage(position), hours_available
output   hours_remaining after the tenure obligation is met
states   HELD | AT_RISK | LOST

stdlib only, CC0.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import _shared as SH                                            # noqa: E402
import agents as AG                                             # noqa: E402

STATES = ("HELD", "AT_RISK", "LOST")

# Positions. wage is per hour in arbitrary units; hours_available is per
# period. blocks = how many separate stretches the money-economy hours are
# split into, which M2 reads as interruptions.
POSITIONS = [
    {"position": "desk_professional", "wage": 40.0,
     "hours_available": 700.0, "blocks": 13},
    {"position": "freight_driver", "wage": 22.0,
     "hours_available": 700.0, "blocks": 8},
    {"position": "fabrication", "wage": 18.0,
     "hours_available": 700.0, "blocks": 13},
    {"position": "animal_handling", "wage": 13.0,
     "hours_available": 700.0, "blocks": 20},
    {"position": "farm_labor", "wage": 11.0,
     "hours_available": 700.0, "blocks": 20},
]

TENURE_COST = 5200.0    # per period, exogenous. See agents.NOT_REPRESENTABLE


def budget(pos, tenure_cost=TENURE_COST):
    hours_needed = tenure_cost / pos["wage"]
    remaining = pos["hours_available"] - hours_needed
    if remaining <= 0:
        state = "LOST"
    elif remaining < 0.25 * pos["hours_available"]:
        state = "AT_RISK"
    else:
        state = "HELD"
    return {"position": pos["position"], "wage": pos["wage"],
            "hours_needed": hours_needed,
            "hours_remaining": max(0.0, remaining),
            "share_consumed": min(1.0, hours_needed / pos["hours_available"]),
            "blocks": pos["blocks"], "state": state}


def table(tenure_cost=TENURE_COST):
    return [budget(p, tenure_cost) for p in POSITIONS]


def cost_sweep(costs=(2000.0, 3500.0, 5200.0, 7000.0, 9000.0)):
    rows = []
    for c in costs:
        t = table(c)
        rows.append({"tenure_cost": c,
                     "n_lost": sum(1 for r in t if r["state"] == "LOST"),
                     "n_at_risk": sum(1 for r in t
                                      if r["state"] == "AT_RISK"),
                     "n_held": sum(1 for r in t if r["state"] == "HELD"),
                     "median_share": sorted(r["share_consumed"]
                                            for r in t)[len(t) // 2]})
    return rows


def confidence():
    return {"identity": "arithmetic. hours = cost / wage, and the rest is a "
                        "subtraction",
            "wage_and_cost_values": "stipulated. only the ordering and the "
                                    "ratio matter downstream",
            "any_real_tenure_data": "NONE",
            "resolved": False}


def breaks():
    return [
        "tenure_cost is exogenous and constant. Nothing in the model "
        "determines it, so no incentive running through it can be read -- "
        "this is the third entry in agents.NOT_REPRESENTABLE and it bounds "
        "what the whole module set can say",
        "hours_available is per holder, so any household labour that frees "
        "or consumes those hours has no term",
        "the AT_RISK threshold at 25 percent of available hours is a round "
        "number with nothing behind it, and the state counts in cost_sweep "
        "move with it",
        "a wage is treated as position-fixed. Nothing represents changing "
        "position, which is the obvious response to the squeeze the module "
        "describes",
    ]


def report():
    L = ["M1 -- TENURE BUDGET", "=" * 72, ""]
    L.extend(SH.wrap("An accounting identity: hours in the money economy "
                     "required to meet a tenure obligation, and what is left "
                     "over. No moral term appears in this module.", "  "))
    L.append("")
    L.append("  tenure cost per period: %.0f" % TENURE_COST)
    L.append("")
    L.append("  %-20s %-8s %-12s %-12s %-10s %s"
             % ("position", "wage", "hrs needed", "hrs left", "share", "state"))
    for r in table():
        L.append("  %-20s %-8.1f %-12.1f %-12.1f %-10.3f %s"
                 % (r["position"], r["wage"], r["hours_needed"],
                    r["hours_remaining"], r["share_consumed"], r["state"]))
    L.append("")
    L.extend(SH.wrap("The share of available hours consumed by the tenure "
                     "obligation runs inversely with wage, by construction -- "
                     "it is cost over wage. What the module supplies "
                     "downstream is not that, it is the HOURS LEFT and the "
                     "BLOCK COUNT, which M2 reads very differently from each "
                     "other.", "  "))
    L.append("")
    L.append("  TENURE COST SWEEP")
    L.append("")
    L.append("  %-14s %-8s %-10s %-8s %s"
             % ("cost", "held", "at risk", "lost", "median share consumed"))
    for r in cost_sweep():
        L.append("  %-14.0f %-8d %-10d %-8d %.3f"
                 % (r["tenure_cost"], r["n_held"], r["n_at_risk"],
                    r["n_lost"], r["median_share"]))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("agents are declared in a module imported before any equation",
       hasattr(AG, "AGENTS") and len(AG.AGENTS) == 4)
    ck("hours needed is cost over wage, exactly",
       abs(budget(POSITIONS[0])["hours_needed"]
           - TENURE_COST / POSITIONS[0]["wage"]) < 1e-9)
    ck("the share consumed runs inversely with wage",
       budget(POSITIONS[-1])["share_consumed"]
       > budget(POSITIONS[0])["share_consumed"])
    ck("all three states are reachable across the cost sweep",
       len({s for r in cost_sweep() for s in
            ("HELD",) * (r["n_held"] > 0) + ("AT_RISK",) * (r["n_at_risk"] > 0)
            + ("LOST",) * (r["n_lost"] > 0)}) == 3)
    ck("hours remaining never goes negative",
       all(r["hours_remaining"] >= 0 for r in table()))
    ck("no moral token appears in any data structure here",
       not any(w in str(POSITIONS + [TENURE_COST]).lower()
               for w in ("deserve", "lazy", "worthy", "fault")))
    ck("the exogenous tenure cost is the first break listed",
       "exogenous" in breaks()[0])
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "TENURE COST SWEEP" in report())
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "M1"))
