id: ADAPT-001
title: Pre-augmentation adaptation read through non-textual channels
status: NOT_MEASURED
term_status: UNNAMED
measurand: For a taxon, variety or practice present at a site before any documented human modification, the spread of its tolerance range read from non-textual channels -- archaeobotanical assemblage, sediment and ice cores, land-use sequence, stable isotope series, and living practice where it is continuous -- with the spread split into two components: FIT, the range present before modification, and AUGMENTATION, the range added after. Two numbers, reported separately, never summed into one tolerance.
control: Sites and taxa with an independently dated modification horizon -- a dated introduction, a dated irrigation works, a dated clearance -- so the FIT/AUGMENTATION boundary is fixed by a date established outside the spread measurement. Second arm: taxa with no documented modification at the site, whose whole spread is FIT by construction and which bound what FIT alone looks like.
scope_limits: Every channel carries its own preservation bias and they do not overlap -- archaeobotany selects for what charred or waterlogged, cores for what deposited and stayed, isotopes for what mineralised, living practice for what was still being done when someone looked. A spread read across channels inherits all four selections and the run states which channels contributed each end of the range. The modification horizon is a date with a band, so the FIT/AUGMENTATION split is a band, not a line, and an item falling inside the band is assigned to neither. Living practice is a present-day observation used to read a past range and that use is declared per row. Says nothing about intent, and nothing about whether any modification was deliberate.
thin_links: Reading an assemblage as a tolerance range is an inference over an inference: the assemblage is a proxy for what grew, what grew a proxy for what could grow, what could grow a proxy for the tolerance. Three hops, and the entry marks each row with how many it rests on. Treating continuous living practice as evidence of a pre-modification range is a second thin link -- practice is continuous in transmission, not necessarily in the range it covers, and the two are recorded apart. Assigning a spread component to AUGMENTATION because it postdates a modification horizon is a temporal ordering read as a causal one and is marked as such on every row.
would_change: A directly dated specimen from either side of a modification horizon replaces an inferred assignment and the row records the replacement. A channel returning a range that contradicts another channel at the same site is the informative case and is carried as a disagreement rather than averaged. A revised modification date moves the split for every row at that site at once, which is why the horizon date and its band are carried as a site-level field rather than copied into rows. Any taxon where the FIT component alone covers the full observed range removes the augmentation reading for that taxon.
reinspect: UNSET
owner: UNOWNED
decay_class: UNSET

## The split

```
                    modification horizon (dated, with a band)
                              |
    range present before      |      range present after
    ----------------------->  |  ----------------------->
            FIT               |        FIT + AUGMENTATION
                              |
    an item inside the band is assigned to NEITHER
```

The two components are reported separately. A single tolerance figure
for a taxon at a site is the thing this entry exists not to produce,
because the two components have different origins and a reader cannot
recover the split from the sum.

## Channels

```
    ARCHAEOBOTANY      assemblage composition, per phase, per context.
                       Preserves by charring and waterlogging.

    CORES              sediment, peat, ice. Continuous where the
                       sequence is continuous; the gap structure is
                       recorded, not interpolated across.

    LAND USE           field systems, terracing, water works, clearance
                       sequence. Dates the modification, and is also a
                       channel for the range that was being worked.

    ISOTOPES           stable isotope series, on material that
                       mineralised. Narrow coverage, strong dating.

    LIVING PRACTICE    where transmission is continuous. Recorded with
                       its own provenance and with the transmission
                       chain stated; a practice recorded once by an
                       outside observer is a different row from one
                       continuously held.
```

No channel is weighted above another and no composite is formed. A row
states which channels reached it and which did not.

## Row schema

```
    site, taxon / variety / practice
    modification horizon      date + band, site-level
    per channel               range contribution, or NOT_REACHED
    FIT component             range, channels, hop count
    AUGMENTATION component    range, channels, hop count
    unassigned                items falling inside the horizon band
    disagreements             channels returning contradicting ranges
```

NOT_REACHED is a declared value. A channel that was not searched and a
channel searched with nothing found are two different values and are
kept apart.

## Not in scope

Whether pre-modification range is better or worse than augmented range,
and any recommendation about cultivation, restoration or management.
The entry produces two numbers and a disagreement list.
