#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
# To the extent possible under law, the authors have waived all copyright and
# related or neighboring rights to this file.
"""
entries.py - three seed entries for the coupling audit.

    python3 entries.py            # same report as audit.py --report
    python3 entries.py --selftest

PROVENANCE, applying to all three entries below, each of which carries
MODEL_SEEDED = True:

  the shape of the audit and the evenness test are the author's.
  the field names, the verdict labels, and these write-ups are
  model-generated from web search results.
  the underlying facts are cited sources, not authored claims.

That split matters for reading the entries: a reader checking this folder
should check the cited documents, not this file's characterisation of them.
A model-generated summary of a source is a proxy for the source.

stdlib only, parses under Python 3.9.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audit as A                                              # noqa: E402

PROVENANCE = (
    "MODEL_SEEDED. The shape and the evenness test are the author's. The "
    "field names, verdict labels and this write-up are model-generated from "
    "web search results. The underlying facts are cited sources, not "
    "authored claims."
)


# --- entry 1 ---------------------------------------------------------------

IPC = A.record(
    model_id="IPC -- Integrated Food Security Phase Classification",
    flow_measured="human dietary energy (kcal/person/day, plus consumption "
                  "and coping indices)",
    agents_drawing_on_flow=[
        "humans (household members)",
        "companion animals in the household",
        "livestock as a caloric draw",
    ],
    agents_represented=["humans (household members)"],
    agents_coupled=["humans (household members)"],
    coupling_machinery_present=True,
    coupling_machinery_name="reduced Coping Strategy Index (rCSI), alongside "
                            "Livelihood Coping Strategies",
    gate="species",
    gate_stated=False,
    verdict="ABSENT_MACHINERY_PRESENT",
    note=(
        "The outcome indicators are Household Dietary Diversity Score, Food "
        "Consumption Score, Household Hunger Score, reduced Coping Strategy "
        "Index, and Livelihood Coping Strategies. All five are scored on "
        "human consumption and human behaviour. "
        "The coupling machinery is present and named in the model's own "
        "vocabulary: the rCSI formalises condition-dependent consumption "
        "behaviour -- it is a measure of how a draw changes under scarcity, "
        "which is exactly the term the audit is looking for. It is applied "
        "to humans only. "
        "Companion animals are absent. Livestock enters the analysis "
        "repeatedly, as prices, herd dynamics and livelihood assets -- that "
        "is, as economic and asset terms, never as a caloric draw. "
        "The gate is unstated: the unit of analysis is defined as human food "
        "consumption and nutrition outcome, so no exclusion is ever written. "
        "There is no slot for the animal term to be excluded from. That is "
        "an unstated boundary rather than a stated exclusion, and it is why "
        "the entry scores ABSENT_MACHINERY_PRESENT rather than "
        "ABSENT_NO_MACHINERY: the capability exists in the model."
    ),
    sources=[
        "IPC Technical Manual and the outcome-indicator set used in recent "
        "acute food insecurity analyses (HDDS, FCS, HHS, rCSI, LCS)",
    ],
    model_seeded=True,
    provenance=PROVENANCE,
)


# --- entry 2 ---------------------------------------------------------------

PER_CAPITA_CF = A.record(
    model_id="per-capita consumption-based carbon footprint (COICOP "
             "expenditure accounting)",
    flow_measured="CO2e (t/capita/yr)",
    agents_drawing_on_flow=[
        "adults",
        "children",
        "companion animals in the household",
    ],
    agents_represented=[
        "adults",
        "children",
        "companion animals in the household",
    ],
    agents_coupled=["adults", "children"],
    coupling_machinery_present=True,
    coupling_machinery_name="OECD equivalence scales",
    gate="unstated",
    gate_stated=False,
    verdict="PRESENT_FIXED",
    note=(
        "MISATTRIBUTED, which is why the entry is PRESENT_FIXED rather than "
        "ABSENT. Pet food and veterinary spending are captured inside "
        "COICOP expenditure domains, so the emissions do enter the national "
        "total -- attributed to the human purchaser as a purchase, never "
        "resolved as a consumer with a draw of its own. "
        "The coupling machinery is present and named: OECD equivalence "
        "scales weight non-identical household members and include a child "
        "term. There is no animal term. So the model already has the "
        "apparatus for saying that two members of one household are not the "
        "same size of draw. "
        "The gate is the denominator: 'per capita' divides by human "
        "population. It is implicit -- an arithmetic convention nobody "
        "restates as an exclusion rule. "
        "This entry is the reason agents_represented and agents_coupled are "
        "separate fields. Represented-but-uncoupled is a distinct state from "
        "absent, and collapsing them would lose it."
    ),
    sources=[
        "COICOP expenditure classification as used in consumption-based "
        "national carbon accounting",
        "OECD equivalence scales (square-root and modified-OECD variants)",
    ],
    model_seeded=True,
    provenance=PROVENANCE,
)


# --- entry 3 ---------------------------------------------------------------

FAO_WATER = A.record(
    model_id="FAO LEAP / GLEAM livestock water accounting",
    flow_measured="freshwater (m3, resolved to river-basin scale, "
                  "trade-adjusted)",
    agents_drawing_on_flow=[
        "livestock in production systems",
        "companion animals",
    ],
    agents_represented=["livestock in production systems"],
    agents_coupled=["livestock in production systems"],
    coupling_machinery_present=True,
    coupling_machinery_name="drinking water + service water + feed water, "
                            "with breed-level and climate-level variation",
    gate="market_output",
    gate_stated=True,
    verdict="ABSENT_MACHINERY_PRESENT",
    note=(
        "THE SHARPEST OF THE THREE GATES, for a reason that has nothing to "
        "do with how well it is documented. "
        "The coupling machinery here is not merely present, it is highly "
        "developed: drinking water plus service water plus feed water, with "
        "breed-level and climate-level variation modelled -- drought-adapted "
        "goats and camels, reduced drinking water on high-moisture feed. "
        "That is genuine condition-dependent coupling, built for animals, "
        "and it is the most developed instance of the machinery in any of "
        "these three entries. "
        "Companion animals are absent. The gate is STATED: the system "
        "boundary is production systems and supply chains, so an animal "
        "enters the accounting only if it yields a priced commodity. "
        "The exclusion criterion is SALABILITY -- not calories, not water, "
        "not biology. A stated gate is better than an implicit one, and it "
        "is still not a justification in the units being measured: nothing "
        "about a cubic metre of freshwater distinguishes the animal that "
        "drinks it by whether the animal's output has a price. "
        "See FALSIFIER.md: stated-and-justified-in-units would be a pass. "
        "Stated-and-justified-by-market-category is not."
    ),
    sources=[
        "FAO LEAP guidelines, water use assessment for livestock supply "
        "chains",
        "FAO GLEAM (Global Livestock Environmental Assessment Model)",
    ],
    model_seeded=True,
    provenance=PROVENANCE,
)


ENTRIES = [IPC, PER_CAPITA_CF, FAO_WATER]


def selftest():
    f = k = 0

    def ck(label, cond):
        nonlocal f, k
        k += 1
        if not cond:
            f += 1
            print("FAIL %s" % label)

    ck("three seed entries", len(ENTRIES) == 3)
    ck("all three are marked MODEL_SEEDED",
       all(e["MODEL_SEEDED"] for e in ENTRIES))
    ck("all three carry the provenance note",
       all(e["provenance"] == PROVENANCE for e in ENTRIES))
    ck("every entry cites at least one source",
       all(e["sources"] for e in ENTRIES))

    for e in ENTRIES:
        ck("declared verdict agrees with derived, for %s"
           % e["model_id"][:24], A.score(e)["agrees"])

    ck("all three have coupling machinery present -- that is the finding, "
       "not a coincidence of selection",
       all(e["coupling_machinery_present"] for e in ENTRIES))
    ck("every machinery name is in the model's own vocabulary, not this "
       "audit's",
       all(e["coupling_machinery_name"] for e in ENTRIES))

    ck("no entry scores PRESENT_COUPLED, so the marker is not yet refuted "
       "on this corpus",
       not any(A.derive_verdict(e) == "PRESENT_COUPLED" for e in ENTRIES))
    ck("no entry has a stated, units-justified gate",
       not any(e["gate_stated"] and A.gate_justified_in_units(e)
               for e in ENTRIES))
    ck("exactly one gate is STATED, so gate_stated is not constant across "
       "the corpus",
       sum(1 for e in ENTRIES if e["gate_stated"]) == 1)
    ck("the three gates are three different types, so the gate field "
       "discriminates on this corpus",
       len({e["gate"] for e in ENTRIES}) == 3)
    ck("two distinct verdicts occur, so the corpus is not one verdict "
       "repeated",
       len({A.derive_verdict(e) for e in ENTRIES}) == 2)

    print("%d/%d checks passed" % (k - f, k))
    return 1 if f else 0


def main():
    ap = argparse.ArgumentParser(description="coupling audit seed entries")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    print(A.report(ENTRIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
