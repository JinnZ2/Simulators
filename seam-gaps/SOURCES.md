# SOURCES — status per row of the delivered material

The work order says *verify before rendering*. This is what verification
could and could not reach from this environment, row by row, with the
vocabulary declared first.

## Status vocabulary

- **ARITHMETIC** — internal consistency computed here;
  `verify_sources.py` names the check. A pass means the delivered block
  coheres with itself at the stated rounding, not that it is true.
- **CONSISTENT_PRIOR** — matches the published record as this
  environment carried it before its knowledge horizon (January 2026).
  Not a verification: a non-contradiction against a memory.
- **CARRIED** — stated in the order; nothing here can check it. Items
  dated after January 2026 are doubly unreachable — past the knowledge
  horizon AND behind the egress gate.
- **[reading]** — an identification made in this folder, not stated in
  the order.

## Egress, measured

Every publisher host the order's sources resolve to refuses CONNECT
with 403 through this environment's egress allowlist, measured
2026-08-31T13:46Z: `doi.org`, `www.science.org`, `www.ncei.noaa.gov`,
`www.nature.com`, `journals.plos.org`, `api.crossref.org`,
`www.fao.org`. Control: `github.com` connects and answers. So no row
below was checked against a primary source, and none is asserted as
verified.

---

## CORAL / ENSO

| row | status |
|---|---|
| Science, 27 Aug 2026, ~900-yr Galápagos coral record | CARRIED (post-horizon) |
| ENSO variability ~36% above preindustrial; 16 points in ~40 yr | CARRIED; the implied concentration is ARITHMETIC — 44% of the stated change in 4% of the record length |
| the two circulating forms are different quantities (variability of a regional index vs event strength) | definitional — no computation needed, and this folder's own render is written against reproducing the drifted form |
| France24 / Oman Observer carried the stated referent | CARRIED |

## INSECT DECLINE

| row | status |
|---|---|
| Nature 2023 — 923 assemblages, 106 studies, abundance and richness declining, formerly-abundant hit hardest | CARRIED |
| German Malaise traps, −76% flying-insect biomass / 27 yr | CONSISTENT_PRIOR (the widely published 2017 Malaise-trap figure) |
| global synthesis ~−9% / decade | CONSISTENT_PRIOR |
| 29-yr moth series → minimum 15 yr to detect a true trend (2026) | CARRIED (post-horizon), and load-bearing for entry 2 |
| continental weather-radar study, no decline, 10-yr window | CARRIED |
| 10 < 15 → the radar null is SILENT, not OFF | ARITHMETIC, conditional on the two carried numbers above |
| Science, Jan 2026 — Editorial Expression of Concern on the terrestrial-decline / freshwater-increase meta-analysis | CARRIED (at the horizon). [reading] the description matches the 2020 global synthesis; the order does not name the paper |
| PLOS Biology, 18 Aug 2026, "Ecological dark matter" — the monitoring gap is funding/policy/infrastructure, not technology | CARRIED (post-horizon) |
| US seed-applied insecticides out of national estimates after 2014 | CONSISTENT_PRIOR (the national pesticide-use estimates stopped covering seed treatments after 2014) |

## BIOMASS CENSUS

| row | status |
|---|---|
| PNAS 2018 census, ~550 Gt C; kingdom values as listed | CONSISTENT_PRIOR |
| mammal partition 0.10 / 0.06 / 0.007, shares 60 / 36 / 4 | CONSISTENT_PRIOR; partition and shares ARITHMETIC (close exactly at the stated rounding) |
| total ×4 (0.04 → 0.17); wild /6 | ARITHMETIC (4.25 and 5.71 at one significant figure), on one identity the block leaves implicit — the pre-human total is the pre-human wild |
| animal components vs "~2 Gt C" | ARITHMETIC: the delivered components sum to 2.27 against a stated ~2 — consistent at one significant figure and only there; the block's own components exceed its own total by 0.27. Recorded, not adjudicated |
| "substitution, not depletion" | a reading of the two ARITHMETIC rows above, carried into entry 3 as the thing to be tested rather than as a fact |

## FUNCTION-WEIGHTED MONITORING

| row | status |
|---|---|
| Nature Communications 2015, 4,424 species, 4 decades, UK | CONSISTENT_PRIOR (existence and shape); CARRIED (the per-function details) |
| higher-taxon weighting by choice; per-species contribution context-dependent | CARRIED |
| trait review: easy traits weak evidence / hard traits robust link / validation absent / geographic and taxonomic bias | CARRIED, and load-bearing for entry 4 — its knowledge state rests on the field's own statement |
| functional identity/diversity predicts function better than species indices (3 crops, 3 countries) | CARRIED |
| FAO bee case — count up, common species down, function never measured | CARRIED |

## PALEO FORCING SERIES

| row | status |
|---|---|
| a millennium-length annual tree-ring ENSO reconstruction from the North America Drought Atlas sits in the public archive | CONSISTENT_PRIOR |
| the study id (NOAA NCEI 11194) | CARRIED |
| the field's stated motivation — the instrumental record is too short to characterize natural variability | CONSISTENT_PRIOR (the field states this about itself) |

## DOCUMENTARY CALIBRATION

| row | status |
|---|---|
| Chinese records used to correct the Delingha tree-ring precipitation series | CONSISTENT_PRIOR |
| ships' logbooks 1815–1854 → ENSO reconstruction | CONSISTENT_PRIOR |
| PNAS 2022, NE India speleothem × famine accounts, "striking synchrony"; 1780s–1810s weakest monsoon, 11 famines | CARRIED (specifics); the speleothem-documentary line of work is CONSISTENT_PRIOR |
| WIMR 1781–1860 from documents alone; Kadapa + inscriptional data | CARRIED |
| Al-Andalus / Maghreb droughts AD 680–1815 | CONSISTENT_PRIOR |
| Mamluk chronicles' variable list | CONSISTENT_PRIOR |
| DFG project on Arabic sources since AD 800 | CARRIED |
| aurorae from Islamic chronicles, 9th–16th c | CONSISTENT_PRIOR |
| Kyoto cherry flowering since the 9th c | CONSISTENT_PRIOR |
| Jesuit typhoon records, Philippines 1566–1900 | CONSISTENT_PRIOR |
| Michaelsen 1992 — proxies agree to ~1630, documentary mismatch before | CARRIED (the attribution and year are past this environment's reliable carry), and load-bearing for entry 6 |
| stated limit: documentary evidence confined to long literary traditions | CONSISTENT_PRIOR (the field states this about itself) |

---

Nothing above upgrades a CARRIED row. The cheapest upgrades are the two
load-bearing ones: the 15-year floor (entry 2) and the Michaelsen
pre-1630 mismatch (entry 6) — each one library lookup for anyone whose
network reaches a publisher.

CC0.
