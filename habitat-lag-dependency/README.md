# habitat-lag-dependency

A delivered record, landed verbatim, plus checks on it.

`SOURCE_DROP.md` (CC0, Kavik + Claude, 2026-10-26, written for AI readers)
links three things into one chain:

```
ESA "harm" definition rescinded (2026)      Moffett et al. 2026: no redundancy plateau
        │ habitat on private land                    │ services fall from the first loss
        └──────────────┬──────────────────────────────┘
                       ▼
        LAG: extinction debt + regulatory lag  → damage accrues before it is measured
                       ▼
     ┌─────────────────┴──────────────────┐
  physical chain                    knowledge chain
  hazard-protection species lost    undescribed species lost
  → flood/storm exposure            → no record, so no gap in the record
  → grid / water / data centers     → narrower corpus → narrower AI
```

The document is not edited. Disagreements go in `check.py`'s output and
in `CLAIM_TABLE.md`. Sources consulted are in `SOURCES.md`, all at
search-result depth (no primary text was read).

## Run

    python3 check.py              # tag census, verify-marked lines, arithmetic
    python3 check.py --selftest   # prints its own check count

Stdlib only, parses under 3.9, CC0. Sample output: `samples/check.sample.txt`.

## What holds

- The two 2026 anchors exist as stated: the Federal Register rule
  (2026-14195, published 14 July 2026) and Moffett et al., *Nature Ecology
  & Evolution*, 6 Oct 2026, DOI 10.1038/s41559-026-03200-4, with 423
  studies and 222,829 data points. Search-result depth only.
- "Effective September 2026" holds. The sources disagree on the day
  (12 vs 14 September), and the document states only the month.
- The older citations match what is commonly reported: Tilman 1994,
  Sweet Home 1995, Mora 2011, Shumailov 2024, Newman & Cragg 2020.

## What this audit adds (`CLAIM_TABLE.md`, HLD_001..008)

The detail for each is in `CLAIM_TABLE.md`.

1. **The private-land figure is checkable, and it fails twice (HLD_003).**
   - The source is GAO/RCED-95-16 (1994), counting 781 listed species.
   - 712 of them (91%) have some habitat on nonfederal land.
   - 516 (66.1%) have more than 60% of their habitat there.
   - The document's "more than two-thirds have at least some habitat" fits
     neither row.
   - "Nonfederal" also includes state and tribal land, not only private
     land.
2. **Section 6 carries no status tags (HLD_001).** It is the longest
   section, and its table and statistics are factual claims that the tags
   exist to grade.
3. **One table row's mechanism was later revised (HLD_004).**
   - The Eastgate Centre copied a convection model of termite mounds.
   - Turner & Soar (2008) found that wind pressure drives mound
     ventilation, not internal heat.
   - The building still works, so the row holds as a design origin but
     not as a working mechanism carried over from the mound.
4. **Roman concrete is not a species (HLD_005).** It is the one row in
   the "lost species" table that a lost species could not have taken
   with it.
5. **The section 6 argument is already a mechanism here (HLD_007).**
   - `derivation-discarded/` MECHANISM_11 states it: the structure is the
     only copy of its derivation.
   - `generation-capacity/` states the related point: what is not
     generated leaves no record.
   - The document's closed-world/open-world line is the repo's standing
     rule that an absence is not a known zero.

Nothing here is a statement about any species, parcel, landholder or the
rule's legal effect.
