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

## 6. Precedent in anthropology and archaeology (open; two searches, not a literature review)

*Delivered text, landed as written. Supersedes the one-search version of this
section; see `LOG.md`.*

The coupling variable is established under other names. In anthropology it is
called a provisioning regime; in zooarchaeology, foddering or seasonal fodder
supplementation. Neither literature frames it as a coupling variable applied
across species, and neither is routed to the resource-allocation models
audited in `entries.py`.

- **Lupo 2019, J. Anthropological Archaeology** ("Hounds follow those who feed
  them"): working dogs in cold biomes supportable only after intentional
  provisioning emerged and was incorporated into the subsistence system —
  provisioning treated as a paid-for constraint on capability.
- **Mitchell 2025, First Dogs (Routledge)**: thematic chapter on how dogs have
  been fed and cared for across hunter-gatherer populations; domestication as
  plural, long-duration, environment-dependent.
- **Pacheco-Cobos and Winterhalder, Belize lowlands**: village dogs, crop
  protection and subsistence hunting, behavioral-ecology framing.
- **Mesoamerica, quoted in the ethnographic literature**: "a household's use
  of dogs affects its investment in them" — the coupling relation stated as a
  household-level variable.

**Not found: the reverse direction.** The literature is weighted toward
provisioning enabling capability. De-provisioning under seasonal scarcity —
the animal re-coupled to its own foraging envelope and re-imported when supply
returns, with protection held constant through the switch — was not found
named as a reversible regime. Open, and possibly ahead of the record. **Not a
finding.**

## 7. Candidate anomalies already published (open)

Within-site isotopic spread in archaeological dogs is documented repeatedly
and absorbed under three explanations, none tested against variable coupling:

- **Harris et al. 2020, Labrador Inuit sled dogs** (n=35 bone, n=4 dentine):
  Double Mer Point dogs the most heterogeneous of any site; explained as
  long-distance movement of people and/or animals. Variable coupling predicts
  the same spread with no movement.
- **Arroyo Hondo Pueblo** ("What Makes a Dog?"): values "similarly varied, but
  not in ways that one might expect"; one specimen genetically *Canis latrans*
  returned isotope values in the domestic-dog range. The taxonomic category
  failed to predict the draw. The paper's own conclusion is that isotopes
  reflect variability in human-canid relationships and do not track genetics.
- **Canine Surrogacy Approach generally**: the method assumes dogs ate what
  humans ate, i.e. that the coupling is fixed. Hudson Bay Thule dogs are
  isotopically similar to humans but mixing models put them on a different
  intake. The standing offset is currently absorbed as method caution.

## 8. Discriminating test (open, runs on existing collections)

Three hypotheses predict different signal geometry:

- **mobility** → spatial signal; strontium should co-vary with the carbon and
  nitrogen spread
- **breed or status class** → between-individual spread, each individual
  internally consistent
- **variable coupling** → within-individual spread, sequential, phased to
  season, same animal switching

Bone collagen averages years and cannot separate these, which is why the
spread reads as between-animal. Incremental dentine can. Published dentine n
for dogs is approximately 4. **No new excavation required.**

## 9. Transferable instrument: intra-tooth amplitude (open)

Sequential sampling of enamel (δ18O, δ13C) and dentine collagen (δ13C, δ15N)
along a single tooth yields a time series of one individual's intake during
tooth formation. The method is mature in cattle and caprines and
experimentally calibrated: **Balasse et al.** recovered a known C3-to-C4 diet
switch and weaning from intra-tooth variation in a controlled feeding study.

Published applications measuring the switch directly:

- **Tana del Barletta, Ligurian Prealps**: intra-tooth series in cattle and
  sheep/goat, Late Neolithic to Early Bronze Age
- **Vinča-Belo brdo (PLOS One)**: cattle intra-tooth δ13C amplitude 0.7 to 2.4
  permil — some individuals nearly flat, others roughly three times the range,
  within one assemblage
- **Schipluiden, Netherlands**: δ13C lower than expected in some cattle but
  not in red deer or suids from the same site; read as leafy fodder rather
  than grazing
- **Indus Civilisation herds; Ksizovo-1 forest-steppe**: sequential
  multi-isotope husbandry and seasonal mobility
- **Perdigões, southern Portugal**: seasonal fodder supplementation invoked to
  explain sheep and goat patterns

**What transfers to this audit**: intra-tooth amplitude is a
coupling-variability measurement with a unit. Flat implies a fixed draw; high
amplitude implies a supply-coupled draw. For archaeological cases this
**replaces** the boolean `coupling_machinery_present` field with a magnitude.

**Design element worth extracting**: Schipluiden sampled wild animals from the
same site as a baseline. The domesticates deviate and the wild taxa do not,
which attributes the deviation to household provisioning rather than to
environment. This is a working coupling-strength instrument. It has not been
pointed at dogs with a wild-canid control from the same site — which is the
comparison Arroyo Hondo arrived at accidentally.

**Caveat, carry it with the number**: a 2024 *Journal of Archaeological
Science* paper finds dentine sample geometry changes the intra-tooth isotope
pattern. Amplitude is therefore partly a protocol artifact, and cross-study
comparison requires the sampling geometry to be stated. **Do not compare
amplitudes across studies without it.**

## 10. Cross-species extension (stated by the author, untested)

The same coupling is predicted for chickens, cattle, yak, and buffalo: the
household draw tracks surplus, while protection is held constant through the
switch. In species with a commodity output the switching is already measured
seasonally per individual, **because no one had to argue about whether the
animal counted.**
