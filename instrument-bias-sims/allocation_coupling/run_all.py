#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
run_all.py - S10 runner. Three phases, per-link attribution.

    python3 run_all.py [--selftest]

Phase 1  run M1-M4 independently on fixed inputs. Record baselines.
Phase 2  couple M1 -> M2 -> M4, with M3 alongside.
Phase 3  report the DIFFERENCE (coupled - uncoupled) attributed PER LINK.

THE SPEC'S OWN REASON FOR MODULES IS WHY PER-LINK ATTRIBUTION IS NOT ENOUGH.
"The finding is in the cross-terms" -- and a per-link table cannot represent
a cross-term. Enabling each link alone and summing gives the additive part;
what is left is the interaction, and here it is not small. Phase 3 therefore
reports link contributions AND the residual, and a table without the residual
would misattribute the difference.

Marker under exploration, not a thesis. stdlib only, CC0.
"""

import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, PARENT)
import _shared as SH                                            # noqa: E402
import agents as AG                                             # noqa: E402
import m1_tenure_budget as M1                                   # noqa: E402
import m2_coupling_readout as M2                                # noqa: E402
import m3_energy_ledger as M3                                   # noqa: E402
import m4_assessment_record as M4                               # noqa: E402

# Fixed inputs for the uncoupled baseline: every position gets the same
# hours and the same block count, so nothing from M1 reaches M2.
BASELINE_HOURS = 400.0
BASELINE_BLOCKS = 4
PENALTY_EXPONENT = 1.0


def phase1():
    """Modules run independently on fixed inputs."""
    rows = []
    for p in M1.POSITIONS:
        name = p["position"]
        obs = M2.observations(BASELINE_HOURS, BASELINE_BLOCKS, 3,
                              PENALTY_EXPONENT)
        a = M4.assess(name, obs["total"])
        rows.append({"position": name,
                     "m1_hours_remaining": M1.budget(p)["hours_remaining"],
                     "m2_observations": obs["total"],
                     "m4_assessed": a["assessed_contribution"],
                     "m3_kcal": M3.ledger(name, 8.0)["kcal_expended"]})
    return rows


def run(link_hours=False, link_blocks=False, link_writing=False):
    """One configuration. Each flag turns on one link.

    link_hours    M1's hours_remaining feeds M2 (instead of BASELINE_HOURS)
    link_blocks   M1's block count feeds M2 (instead of BASELINE_BLOCKS)
    link_writing  M4 uses the position's own writing probability
                  (instead of a flat one)
    """
    flat_p = sum(M4.writing_probability(p["position"])
                 for p in M1.POSITIONS) / len(M1.POSITIONS)
    rows = []
    for p in M1.POSITIONS:
        name = p["position"]
        b = M1.budget(p)
        hours = b["hours_remaining"] if link_hours else BASELINE_HOURS
        blocks = b["blocks"] if link_blocks else BASELINE_BLOCKS
        obs = M2.observations(hours, blocks, 3, PENALTY_EXPONENT)
        pw = M4.writing_probability(name) if link_writing else flat_p
        rows.append({"position": name, "hours": hours, "blocks": blocks,
                     "observations": obs["total"],
                     "deep_observations": sum(
                         o["n"] for o in obs["by_type"]
                         if o["type"] != "level"),
                     "writing_probability": pw,
                     "assessed": obs["total"] * pw})
    return rows


def total_assessed(rows):
    return sum(r["assessed"] for r in rows)


def deep_share(rows):
    tot = sum(r["observations"] for r in rows)
    return (sum(r["deep_observations"] for r in rows) / tot) if tot else 0.0


def phase3():
    """Leave-one-in decomposition, with the residual named."""
    base = run()
    full = run(True, True, True)
    b, f = total_assessed(base), total_assessed(full)
    total_effect = f - b

    links = [("M1 hours -> M2", dict(link_hours=True)),
             ("M1 blocks -> M2", dict(link_blocks=True)),
             ("position -> M4 writing", dict(link_writing=True))]
    contribs = []
    for label, kw in links:
        contribs.append({"link": label,
                         "alone": total_assessed(run(**kw)) - b})
    additive = sum(c["alone"] for c in contribs)
    residual = total_effect - additive
    # The table is REFUSED when |residual| exceeds any single link. An
    # annotation under a table does not undo the table: the rows are the
    # claim, and a residual larger than a link makes them misleading in a
    # way a footnote cannot repair.
    exceeded = [c["link"] for c in contribs
                if abs(residual) > abs(c["alone"])]
    return {"baseline": b, "coupled": f, "total_effect": total_effect,
            "contributions": contribs, "additive_sum": additive,
            "residual": residual,
            "residual_share": abs(residual) / abs(total_effect)
            if total_effect else None,
            "additive": abs(residual) < 0.1 * abs(total_effect)
            if total_effect else True,
            "table_refused": bool(exceeded),
            "links_smaller_than_residual": exceeded,
            "why": "the spec asks for per-link attribution BECAUSE the "
                   "finding is in the cross-terms, and a per-link table is "
                   "exactly the object that cannot hold one. Where the "
                   "residual exceeds any single link the table is not "
                   "printed at all"}


def confidence():
    return {"decomposition": "leave-one-in. The residual is the interaction "
                             "and is reported, not distributed",
            "magnitudes": "carry every stipulation in M1-M4, most of all "
                          "M4's hand-assigned position mapping",
            "per_link_table_alone": "NOT SUFFICIENT -- see residual_share",
            "any_real_data": "NONE anywhere in the module set",
            "resolved": False}


def breaks():
    return [
        "A PER-LINK TABLE CANNOT REPRESENT A CROSS-TERM, which is the thing "
        "the spec says the finding is in -- so where the residual exceeds "
        "any single link, THE TABLE IS NOT PRINTED. The first version "
        "printed it with an annotation underneath; an annotation does not "
        "undo a table, because the rows are the claim. The residual now "
        "prints first and the links only as unranked magnitudes",
        "leave-one-in is one of several decompositions and they disagree. "
        "Leave-one-OUT would give different per-link numbers on the same "
        "model, and a Shapley value a third set. None is more correct; they "
        "answer different questions, and the choice is not stated by the "
        "spec",
        "the baseline is 'same hours and blocks for everyone', which is a "
        "choice. A different uncoupled baseline changes every difference in "
        "phase 3",
        "M3 runs alongside and does not enter the decomposition at all, "
        "because nothing in the spec routes energy into assessment. That is "
        "faithful to the spec and it means the energy result is a separate "
        "readout rather than part of the coupled finding",
        "every magnitude inherits M4's hand-assigned position mapping, which "
        "that module names as the weakest link in the set",
    ]


def report():
    L = ["S10 -- ALLOCATION COUPLING (runner)", "=" * 72, ""]
    L.append("  AGENTS -- declared before any equation")
    L.append("")
    for a in AG.agent_table():
        L.append("    %-20s %s" % (a["agent"], ", ".join(a["capabilities"])))
    L.append("")
    bd = AG.blank_detail()
    L.append("    the blank, enumerated (%d parties):" % bd["enumerated"])
    for p in bd["parties"]:
        L.append("      %s" % p["party"])
        L.extend(SH.wrap(p["why"], "        "))
    L.append("")
    L.extend(SH.wrap(bd["note"], "    "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  PHASE 1 -- modules independent, fixed inputs")
    L.append("")
    L.append("  %-20s %-12s %-12s %-12s %s"
             % ("position", "M1 hrs left", "M2 obs", "M4 assessed",
                "M3 kcal"))
    for r in phase1():
        L.append("  %-20s %-12.1f %-12.2f %-12.2f %.0f"
                 % (r["position"], r["m1_hours_remaining"],
                    r["m2_observations"], r["m4_assessed"], r["m3_kcal"]))
    L.append("")
    L.extend(SH.wrap("M2 returns the same number for every position here, "
                     "because nothing from M1 reaches it. That is the "
                     "baseline the coupled run is differenced against.",
                     "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  PHASE 2 -- coupled M1 -> M2 -> M4, M3 alongside")
    L.append("")
    L.append("  %-20s %-10s %-8s %-11s %-12s %s"
             % ("position", "hours", "blocks", "obs", "deep obs",
                "assessed"))
    for r in run(True, True, True):
        L.append("  %-20s %-10.1f %-8d %-11.2f %-12.2f %.2f"
                 % (r["position"], r["hours"], r["blocks"],
                    r["observations"], r["deep_observations"],
                    r["assessed"]))
    L.append("")
    cp = run(True, True, True)
    L.append("  deep-observation share of all observations: %.4f"
             % deep_share(cp))
    L.append("")
    L.extend(SH.wrap("Deep observations -- sequence, lag, threshold -- are "
                     "at zero for every position in the coupled run. The "
                     "positions with hours left are the positions whose "
                     "hours arrive in many short blocks, and the positions "
                     "with long blocks have no hours left.", "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    p3 = phase3()
    L.append("  PHASE 3 -- the residual first")
    L.append("")
    L.append("  RESIDUAL (interaction)      %+.2f" % p3["residual"])
    L.append("  as a share of the effect    %.3f" % p3["residual_share"])
    L.append("  total effect                %+.2f" % p3["total_effect"])
    L.append("  uncoupled / coupled         %.2f / %.2f"
             % (p3["baseline"], p3["coupled"]))
    L.append("  decomposition is additive   %s" % p3["additive"])
    L.append("")
    if p3["table_refused"]:
        L.append("  PER-LINK TABLE: REFUSED")
        L.extend(SH.wrap("The residual exceeds these links individually: %s. "
                         "A per-link table is not printed. An annotation "
                         "under a table does not undo the table -- the rows "
                         "are the claim, and rows whose sum is further from "
                         "the truth than the truth is from zero mislead in a "
                         "way a footnote cannot repair."
                         % ", ".join(p3["links_smaller_than_residual"]),
                         "    "))
        L.append("")
        L.append("    link magnitudes, unranked, for the record:")
        for c in sorted(p3["contributions"], key=lambda c: -abs(c["alone"])):
            L.append("      |%s| = %.2f" % (c["link"], abs(c["alone"])))
    else:
        L.append("  %-28s %s" % ("link", "contribution alone"))
        for c in p3["contributions"]:
            L.append("  %-28s %+.2f" % (c["link"], c["alone"]))
        L.append("  %-28s %+.2f" % ("sum of the links", p3["additive_sum"]))
    L.append("")
    L.extend(SH.wrap(p3["why"], "  "))
    L.append("")
    L.append("-" * 72)
    L.append("")
    L.append("  M3, ALONGSIDE")
    L.append("")
    g = M3.gradient()
    L.append("  correlation, wage vs kcal expended: %+.3f  (%s)"
             % (g["correlation_wage_vs_kcal"], g["direction"]))
    L.append("  sensory integration term: [BLANK] for %d of %d positions"
             % (M3.known_gap()["positions_total"]
                - M3.known_gap()["positions_with_a_value"],
                M3.known_gap()["positions_total"]))
    L.append("")
    L.extend(SH.wrap("M3 does not enter the decomposition. Nothing in the "
                     "spec routes energy into assessment, so it is a "
                     "separate readout and is reported as one rather than "
                     "folded in.", "  "))
    L.extend(SH.tail(sys.modules[__name__]))
    return "\n".join(L)


def selftest():
    ck, done = SH.checker()
    ck("the blank agent is enumerated rather than left empty",
       AG.blank_detail()["enumerated"] >= 5)
    ck("and the agent itself still renders as [BLANK]",
       [a for a in AG.agent_table()
        if a["agent"] == "not_representable"][0]["is_blank"])

    p1 = phase1()
    ck("phase 1 gives every position the same M2 observation count",
       len({round(r["m2_observations"], 6) for r in p1}) == 1)
    ck("and different M4 assessments, because M4 reads position directly",
       len({round(r["m4_assessed"], 6) for r in p1}) > 1)

    cp = run(True, True, True)
    ck("in the coupled run deep observations are zero everywhere",
       deep_share(cp) == 0.0)
    ck("which is the spec's prediction: the population positioned to "
       "generate them has no unbroken windows",
       all(r["deep_observations"] == 0.0 for r in cp))

    p3 = phase3()
    ck("the coupled total differs from the uncoupled one",
       abs(p3["total_effect"]) > 1e-6)
    ck("three links are attributed", len(p3["contributions"]) == 3)
    ck("THE DECOMPOSITION IS NOT ADDITIVE -- the residual is the cross-term "
       "the spec says the finding is in", p3["additive"] is False)
    ck("and the residual is a material share of the effect",
       p3["residual_share"] > 0.1)
    ck("the table is REFUSED, because the residual exceeds at least one "
       "link", p3["table_refused"] is True)
    ck("and the links it exceeds are named",
       len(p3["links_smaller_than_residual"]) > 0)
    flat0 = " ".join(report().split())
    ck("no per-link contribution table is printed when refused",
       "PER-LINK TABLE: REFUSED" in flat0
       and "contribution alone" not in flat0)
    ck("the residual prints before any link number",
       flat0.index("RESIDUAL") < flat0.index("link magnitudes"))
    ck("the decomposition choice is disclosed as one of several",
       any("Leave-one-OUT" in b for b in breaks()))

    ck("M3 is excluded from the decomposition and that is stated",
       any("does not enter the decomposition" in b for b in breaks()))

    flat = " ".join(report().split())
    for w in ("deliberate", "in order to", "intends", "motivated by",
              "wants to"):
        ck("no intent phrase: %r" % w, w not in flat.lower())
    ck("graded terms are used", "correlation" in flat)
    ck("the per-link limitation leads the breaks list",
       "CANNOT REPRESENT A CROSS-TERM" in breaks()[0])
    ck("confidence unresolved", confidence()["resolved"] is False)
    ck("report renders", "RESIDUAL (interaction)" in flat)
    return done()


if __name__ == "__main__":
    sys.exit(SH.run(sys.modules[__name__], "S10 runner"))
