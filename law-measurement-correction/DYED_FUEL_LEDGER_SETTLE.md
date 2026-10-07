# CC-4 — dyed-fuel ledger, the three settle items

Run 2026-10-04 by Claude Code.

## Where the ledger is

The ledger these columns belong to was not located. It is not in this
repository, and it is not in `JinnZ2/dyed-fuel-diff` (cloned at `8d6c210`:
`01_matrix.md`, `02_triggering_actions.md`, `03_literature.md`,
`04_discriminating_checks.md`, `README.md`, `REVIEW_NOTE.md`; no file carries a
dose column, a site column, a float column or a counterfactual side). So
column A is settled against the regulation, which needs no ledger, and columns
B and E/F are reported against rows that are not in hand.

## Column A — dose figure

    SETTLED(
      value:  Solvent Red 164 (and no other dye) at a concentration SPECTRALLY
              EQUIVALENT to at least 3.9 lb of the SOLID dye standard
              Solvent Red 26 per 1,000 barrels of diesel fuel or kerosene
      unit:   lb solid SR26-equivalent / 1,000 bbl, by spectral equivalence.
              NOT liquid dye product mass.
      source: 26 CFR 48.4082-1, eCFR
              https://www.ecfr.gov/current/title-26/chapter-I/subchapter-D/part-48/subpart-H/subject-group-ECFRfec64af5287e9f1/section-48.4082-1
    )

Depth: the search index returned that URL with the text "requires diesel fuel
or kerosene to contain the dye Solvent Red 164 (and no other dye) at a
concentration spectrally equivalent to at least 3.9 pounds of the solid dye
standard Solvent Red 26 per thousand barrels of diesel fuel or kerosene". The
eCFR page itself was refused at the egress gate (WebFetch `EGRESS_BLOCKED`,
2026-10-04), as were the GPO and Cornell LII copies. The paragraph letter the
auditor gave, (b), was not confirmed; the index cites the section only.

The candidate the auditor carried from prior knowledge matches the indexed
text on every element: the dye, the comparator dye, "solid", "spectrally
equivalent", 3.9, and the per-1,000-barrel unit.

Separate field, unfilled on purpose:

    liquid_product_mass_per_1000_bbl:  UNFILLED
      needs: the concentrate strength of the specific Solvent Red 164 product
             supplied (varies by supplier and lot; the index notes SR164's
             alkylation, and so its composition, varies "from manufacturer to
             manufacturer and lot to lot"). No single strength is assumed.

## Column B — unit of "site"

    NOT_EVALUABLE(the source rows are not in hand, so whether they define
                  "site" cannot be read)

Candidate readings, listed and not ranked:

    terminal (the facility)
    terminal rack, or a rack lane within one
    bulk plant / wholesaler storage
    retail dispenser
    retail station (all dispensers at one address)
    farm or off-road on-site storage tank
    vehicle or equipment fuel tank

These are counts of different objects. A per-site figure carries no value
until the rows state which one they count.

## Columns E and F — split zeroed / moved

    NOT_EVALUABLE(the column contents are not in hand)

The split the dispatch asks for, as an empty structure for whoever holds the
rows:

    column  entry   ZEROED (cost removed)   MOVED (cost relocated)   moved to (party / ledger)
    E       ...     ...                     ...                      ...
    F       ...     ...                     ...                      ...

    placement: the MOVED half is entered on the COUNTERFACTUAL side, next to
               the float column. A moved cost entered as savings is the error
               the split exists to catch.

No row is filled here.
