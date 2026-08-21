<!--
SPDX-License-Identifier: CC0-1.0
To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this file.
-->

# OPEN

Unresolved items. Each is open in a different way, and the differences are
load-bearing — a missing census, a routing failure and a definitional dispute
need different work.

## 1. UNRESOLVED — global companion-animal population is not censused

Dog estimates range roughly **470M to 990M** across sources. Cats roughly
**370M to 600M**. The spread is about 2×.

The figures originate in **pet-industry market surveys**, and the unit being
counted is **owners or households**, sampled for retail forecasting — not
animals, counted for accounting. A number produced to size a market and a
number produced to close a ledger are not the same measurement even when they
carry the same units.

**No global figure exists at all** for rabbits, guinea pigs, birds, reptiles
or fish.

The spread is recorded here and **no number is picked**. Selecting a point
estimate from a 2× range would put a precision into the audit that the sources
do not carry, and the audit's own subject is machinery applied where it is not
warranted.

Note the shape: the omission is not one node. Dogs and cats are the only
classes anyone has estimated, so what is missing is an entire unenumerated
class.

## 2. UNRESOLVED (as a routing question) — biomass figures are peer-reviewed and should be cited, not restated

These are published results. They belong in this folder as **citations**, not
as findings of this audit, and nothing here should be read as having measured
them.

- Greenspoon et al., **PNAS 2023** — wild terrestrial mammals ≈ **20 Mt**
  (95% CI 13–38); domestic dogs ≈ **20 Mt**; domestic cats ≈ **2 Mt**; cattle
  ≈ **420 Mt**; humans ≈ **390 Mt**.
- **Nature Communications 2025** — 1850 baseline of ≈ **200 Mt** wild mammal
  biomass.

What is open is not the numbers. It is why a quantity of this size, published
and peer-reviewed, does not appear as a term in the models that allocate the
corresponding flows.

## 3. UNRESOLVED — energy accounting exists and is not routed

- **Okin 2017, PLOS One** — US dogs and cats consume **19% ± 2%** of the
  dietary energy humans do, and **33% ± 9%** of the animal-derived energy.
- **Alexander et al. 2020, Global Environmental Change** — global pet food
  land use, GHG and freshwater.

**This is a routing failure, not a measurement gap.** The quantity is
published, in petajoules, with error bars. It does not enter the models that
allocate under constraint. It lives in a separate literature with its own
journals, adjacent to the models that would need it.

The distinction matters for what would close it: a measurement gap is closed
by measuring, and a routing failure is closed by a citation crossing a
disciplinary boundary. The second is cheaper and has not happened.

## 4. UNRESOLVED — by-product allocation is a definitional question

Pet food impact studies allocate animal by-products by **economic value**
rather than by **caloric content**. This permits the same calories to be
counted as waste in one ledger and as food in another, without either ledger
being wrong on its own terms.

Open as a definitional dispute, not as an empirical one. No measurement
settles it; a convention would.

## 5. UNRESOLVED — single-coefficient failure

A fixed per-animal draw **must be wrong for at least one** of these two cases:

- a US companion dog, whose draw is manufactured pet food — upstream cropland
  and slaughter by-product, fully inside the industrial food system;
- a free-ranging scavenging dog, whose draw is largely municipal food waste
  and scraps.

Same species. The trophic position is set by local conditions, not by the
species. A model assigning one fixed per-animal coefficient must therefore be
wrong in at least one case, and wrong in the direction of whichever market the
coefficient was measured in.

**Flagged as needing a condition variable, not a better average.** Averaging
across the two cases produces a number that describes neither, and the error
does not shrink with a larger sample, because the sample is drawn from one of
the two regimes.

This is the same shape the audit tests for: the difference between a fixed
draw and a supply-coupled one is not a refinement of the coefficient, it is a
different kind of term.

## 6. UNRESOLVED — anthropological/archaeological precedent (open, one search only, not a literature review)

*Delivered text, landed as written.*

The coupling variable is established in this literature under the name
PROVISIONING REGIME:

- **Lupo 2019, J. Anthropological Archaeology** ("Hounds follow those who feed
  them"): working dogs in cold biomes supportable only after intentional
  provisioning emerged and was incorporated into the subsistence system —
  provisioning as a paid-for constraint on capability
- **Mitchell 2025, "First Dogs" (Routledge)**: thematic chapter on how dogs
  have been fed and cared for across hunter-gatherer populations;
  domestication as plural, long-duration, environment-dependent
- **Pacheco-Cobos & Winterhalder, Belize lowlands**: village dogs, crop
  protection and subsistence hunting, behavioral-ecology framing
- **Mesoamerica, quoted**: "a household's use of dogs affects its investment
  in them" — the coupling relation, stated at household level
- **Arctic stable-isotope work**: some ancient dog diets track diets of nearby
  people (marine signal in coastal groups) — the coupling is measurable in
  bone collagen

**ROUTING**: provisioning is a variable regime with a cost in this literature,
and a fixed coefficient or absent term in the footprint, hunger, and water
models. Third silo, same routing failure.

**GAP, unresolved**: the literature found is weighted toward provisioning
ENABLING capability. The reverse — de-provisioning under seasonal scarcity,
animal re-coupled to its own foraging envelope, re-imported when supply
returns — was not found named as a regime. Existing instruments could detect
it: a seasonal signal in dog bone collagen from a group with variable supply.
The Arctic diet-tracking method is one step from it.

**Status: not searched to exhaustion. Do not record as absent from the
literature — record as not found in one pass.**

### 6a. UNRESOLVED — the sampled tissue decides whether the question is askable

Follow-on to item 6, and the reason `provisioning.py` exists in this folder.

The three standing explanations for isotopic spread in archaeological dog
assemblages and the coupling hypothesis are **not distinguished by the tissue
most of the data sits in**. Bone collagen averages years, so a within-year
switch is averaged away before the sample is taken, and the resulting spread
presents as *between*-individual. Incremental dentine and sequential enamel
resolve sub-annually and separate the three.

This is a resolution pairing, not a disagreement about the data: see
`provisioning.py --resolution`.
