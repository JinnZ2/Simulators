# CC-4 MERGED — dyed-fuel ledger, the three settle items

Merged 2026-10-04 by Claude Code, under the CC-3b dispatch: "adopt the other
session's CC-4 (it had the ledger rows)".

## Provenance

    adopted from  pass 1, Claude Code session_01Y4zVdoRHPDHpVwSPbqbeLR
                  commit 60152f7 (branch claude/law-measurement-correction,
                  2026-10-04T02:17Z)
                  file law-as-unvalidated-measurement/LEDGER_SETTLE-dyed-fuel-2026-10-03.md
                  git blob b22e599a1e3b4e04bd543f714b0bda7e1a670a79
    rows it read  the "Dyed-Fuel Enforcement Energy & Labor Ledger" marker,
                  delivered in chat on 2026-10-02 and not committed anywhere.
                  Column A: the anchor row ("26 ppm", "1 oz wt / 100 gal", the
                  DERIVED 5,688 t). Column B: "~12,000 ag sites x separate
                  tank+pump+piping+containment". Columns E (ACCOUNTING / IT)
                  and F (ENFORCEMENT), with the counterfactual side H (FLOAT).
    not adopted   pass 2's own record, DYED_FUEL_LEDGER_SETTLE.md in this
                  folder, which had no rows. It stays as run and unedited.

Columns B and E/F below are a byte copy of pass 1's text from "## COLUMN B" to
the end of that file. `check.py` compares the copy against the blob above
whenever the blob is reachable.

## COLUMN A — dose figure (unit follows CC-3b R1)

    STATE   SETTLED (unit and value), CONVERSION FIELD UNFILLED
    UNIT    pounds of SOLID Solvent Red 26 per 1,000 barrels, by SPECTRAL
            EQUIVALENCE. NOT liquid dye product mass.
    VALUE   >= 3.9 lb / 1,000 bbl        (both passes; search-index text)
            = 11.13 mg/L SR26-equivalent (pass 1, via Wikipedia Solvent_Red_26)
            = 13.1 ppm by mass at 0.85 kg/L (pass 1, DERIVED)
    SOURCE  26 CFR 48.4082-1. Paragraph letter UNCONFIRMED.
            CC-3b R1: PRIMARY_UNREACHABLE. The "(b)" that pass 1 wrote
            ("26 CFR 48.4082-1(b), via search locator") rests on the search
            route, and so does the ASTM D6258 scope that the index quotes.
            No primary page was opened, so the letter is neither kept as
            confirmed nor changed.
    R1 effect on the unit note: none. The unit and value come from the
            section's text, and that text is the same wherever the paragraph
            falls.

Pass 1's reading of the ledger's anchor row against the settled unit is
adopted as written:

    ledger figure          reading                              relation to the settled unit
    "26 ppm"               unstated unit; not SR26-equivalent    2.0x the 13.1 ppm SR26-eq by mass; plausibly a
                           by mass                               LIQUID PRODUCT dose at ~50% strength, UNVERIFIED
    "1 oz wt / 100 gal"    = 88 ppm by mass                      6.7x the SR26-eq; a field rule of thumb, not the rule
    DERIVED 5,688 t        follows the ounce figure              recompute from the settled unit:
                                                                 3.9 lb/1000 bbl x 18.2e9 gal/yr / 42 gal/bbl
                                                                 = 1.69e6 lb = 767 t metric SR26-equivalent/yr

    dye_product_mass_t_per_yr   UNFILLED   needs: supplier SDS / spec sheet, strength as SR26-eq per kg product

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
