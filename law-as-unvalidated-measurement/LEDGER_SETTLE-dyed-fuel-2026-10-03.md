# Dyed-fuel enforcement ledger — the three settle items (CC-4, 2026-10-03)

Settles against the "Dyed-Fuel Enforcement Energy & Labor Ledger" marker as
delivered in chat on 2026-10-02 (not committed anywhere; referenced by title).
Every value below is tagged. Nothing is a measurement of any fleet, plant or
agency.

## COLUMN A — dose figure

```
STATE     SETTLED (unit and value), CONVERSION FIELD UNFILLED
UNIT      pounds of SOLID Solvent Red 26 per 1,000 barrels, by SPECTRAL EQUIVALENCE
VALUE     >= 3.9 lb / 1,000 bbl      = 11.13 mg/L of SR26-equivalent      (OBSERVED)
          at 0.85 kg/L diesel         = 13.1 ppm by mass, SR26-equivalent   (DERIVED)
SOURCE    26 CFR 48.4082-1(b), via search locator on
          https://www.ecfr.gov/current/title-26/chapter-I/subchapter-D/part-48/subpart-H/
          subject-group-ECFRfec64af5287e9f1/section-48.4082-1 :
          "contains the dye Solvent Red 164 (and no other dye) at a concentration spectrally
          equivalent to at least 3.9 pounds of the solid dye standard Solvent Red 26 per
          thousand barrels of diesel fuel or kerosene"
          11.13 mg/L: https://en.wikipedia.org/wiki/Solvent_Red_26 ("3.9 pounds per 1000
          barrels, or 11.13 mg/l, of Solvent Red 26 in solid form")
          Route: web search snippet; ecfr.gov itself refuses CONNECT from this environment.
```

What this does to the ledger's anchor row:

```
ledger figure          reading                              relation to the settled unit
"26 ppm"               unstated unit; not SR26-equivalent    2.0x the 13.1 ppm SR26-eq by mass; plausibly a
                       by mass                               LIQUID PRODUCT dose at ~50% strength, UNVERIFIED
"1 oz wt / 100 gal"    = 88 ppm by mass                      6.7x the SR26-eq; a field rule of thumb, not the rule
DERIVED 5,688 t        follows the ounce figure              recompute from the settled unit:
                                                             3.9 lb/1000 bbl x 18.2e9 gal/yr / 42 gal/bbl
                                                             = 1.69e6 lb = 767 t metric SR26-equivalent/yr
```

SEPARATE, UNFILLED FIELD: conversion from SR26-equivalent to liquid dye PRODUCT
mass. Needs the supplier concentrate's strength (SR164 content and spectral
equivalence factor); varies by supplier; no single value assumed.

```
dye_product_mass_t_per_yr   UNFILLED   needs: supplier SDS / spec sheet, strength as SR26-eq per kg product
```

Column A's energy row therefore carries THREE readings until that field fills:

```
SR26-equivalent floor    767 t    @100 MJ/kg ->  21 GWh/yr   (DERIVED, settled unit)
"26 ppm" reading       1,522 t    @100 MJ/kg ->  42 GWh/yr   (DERIVED, unit unverified)
"1 oz/100 gal" reading 5,160 t    @100 MJ/kg -> 143 GWh/yr   (DERIVED, the ledger's own)
```

## COLUMN B — unit of "site"

```
STATE     NOT_EVALUABLE
REASON    the ledger row reads "~12,000 ag sites x separate tank+pump+piping+containment"
          and defines "site" nowhere. No source row states a unit.
CANDIDATE READINGS (listed, none picked):
  bulk plants / wholesale distributors stocking dyed product       order 10^3 - 10^4
  cardlock and retail dispensers selling dyed diesel               order 10^4
  farm bulk tanks (one or more per operation)                      order 10^5 - 10^6
  agricultural co-op fuel sites                                    order 10^3
  terminal racks injecting dye                                     order 10^3
The ~12,000 figure is consistent with the first or fourth reading and off by
one to two orders from the third. Which it is changes column B by that factor.
```

## COLUMNS E and F — split ZEROED / MOVED

Rule: a cost that leaves one ledger and lands in another is MOVED, not zeroed.
Moved cost entered as savings is the error this split exists to catch.

```
E. ACCOUNTING / IT
   ZEROED (removed under tax-at-pump + rebate)
     dyed/clear line on every invoice; tax-code and exemption-certificate handling at sale
     duplicate GL accounts, SKUs, price books for the dyed product
     database product-class split; rate-change dev+migration+QA on the dyed branch
     dyed/clear reconciliation
   MOVED (relocated, enter on the counterfactual side next to the float column)
     rebate line and its eligibility rule on the return                 -> taxpayer + IRS forms/IT
     rate-change dev+migration+QA on the REBATE line                    -> IRS IT
     audit retention of gallons-claimed records                          -> farm operation
     reconciliation of claimed vs purchased gallons                      -> IRS examination

F. ENFORCEMENT
   ZEROED
     roadside dip program; agents; lab confirmation of marker; SR-26 standards for the field test
     dye-specific penalty, appeal and litigation track (26 USC 6715)
     dye-specification rulemaking and shortage-waiver machinery
   MOVED
     fraud detection on rebate claims (over-claimed gallons)            -> IRS return examination
     proof-of-use records and audit exposure                            -> farm operation
     penalty / appeal track for false claims                            -> existing return-penalty track

COUNTERFACTUAL SIDE, as it now stands
   H. FLOAT      ~$4.4 B/yr federal tax prepaid by ag; ~6-month mean hold @5% ~ $110 M/yr carrying cost   (DERIVED, 10-02)
   E-moved       rebate line, its rate changes, claim records, claim reconciliation                        (UNRUN)
   F-moved       claim-fraud examination, proof-of-use burden, false-claim penalties                        (UNRUN)
```

What the split changes in the marker's own sentence: "Counterfactual (needs
NONE of A-G)" holds for A, B, C, D, G and the ZEROED halves of E and F. It
does not hold for the MOVED halves, which are E and F's own subject
relocated.
