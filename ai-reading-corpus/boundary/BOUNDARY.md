# Biomimicry boundary

CC0. Where does "learning from nature" stop? At organisms? Single cells? Crystals?
Concrete? Chemicals that organise themselves? Science has not settled this. This folder
does not settle it either. It makes the line visible and keeps it revisable.

```text
boundary.json        THE TABLE: 6 axes, 15 cases, 6 candidate lines, adopted_line = null
changelog.jsonl      append-only, hash-chained; every edit to the table is an entry
BOUNDARY_TABLE.txt   rendered matrix (tools/boundary.py render --write); checked for staleness
```

## Energy map

```text
   a structure exists ---> something holds the design ---> can that holder be lost?
                               |                                  |
          organism (C01-04, C09-11)  -- lineage holds it -->   YES, no copy  (L6 IN)
          organism-built (C05, C08)  -- lineage + place  -->   YES           (L6 IN)
          crystal, delta (C07, C14)  -- physics holds it -->   NO, regrows   (L6 OUT)
          reaction (C13)             -- recipe holds it  -->   NO            (L6 OUT)
          Roman concrete (C06)       -- surviving walls  -->   NO, recovered (L6 OUT)
          origin-of-life set (C15)   -- unknown          -->   UNKNOWN       (L6 BORDER)

   BOTTLENECK: "is it alive" (L1) and "can it be lost with no copy" (L6) are different
   axes. H0 §6 labels the table by the first and argues by the second.
```

## Axes and lines

```text
axes      living / evolved / heredity / self_organized / human_made / regenerable
values    Y  N  PARTIAL  CONTESTED  UNKNOWN      (the last three evaluate as BORDER)

L1_ORGANISM        living                              biomimicry = copying organisms
L2_SPECIES         living AND evolved AND heredity     H0 §6's word "species"
L3_EVOLVED_DESIGN  evolved                             anything selection designed
L4_SELF_ORGANIZED  self_organized                      anything that builds itself
L5_NON_HUMAN       NOT human_made                      anything humans did not design
L6_NO_COPY         NOT regenerable                     what H0 §6's argument needs
```

Rules are evaluated in three values (Kleene): N wins an AND, Y wins an OR, a border value
stays BORDER. BORDER is a reading. It is never rounded to IN or OUT.

## What the matrix shows (table 9e586455, first entry)

```text
stable under every line   C01-04, C09-11: animals and single cells        7 of 15
depends on the line       termite mound, Roman concrete, crystal, nacre,
                          virus, BZ reaction, delta, autocatalytic set    8 of 15

Roman concrete (C06)      IN under no line; BORDER only under L4. It is in the H0 §6
                          table and carries the DELAY argument (HLD_005), not the
                          lost-source argument.                           -> conflict X-22
termite mound (C05)       OUT of "species" (the mound does not reproduce),
                          IN under "no copy". The table's label and its argument split here.
single cells (C09-C11)    IN under every line. The single-cell question is not where the
                          line is unsettled.
crystal (C07)             IN only where the line is "self-organized" or "non-human".
virus, autocatalytic set  BORDER on "living": the edge science has not closed.
```

## Changing the boundary

```text
1. edit boundary.json            a cell, a basis, an axis, a case, a line, or adopted_line
2. python3 tools/boundary.py log --by NAME --change "C07.regenerable Y -> PARTIAL" --reason "..."
3. python3 tools/check_corpus.py   boundary_log goes PASS; an edit without step 2 is FAIL
```

```text
refused        a value outside the five, a rule naming an unknown axis, a border value with
               no basis, an adopted_line that is not a declared line, a log entry that
               changes nothing
kept           every earlier table, by hash, in changelog.jsonl; history is never rewritten
               (an edited entry breaks the chain and the check fails)
open           adopting a line is itself a logged change; until then status is UNSETTLED
```

Every cell is a reading by this bundle's author, from general knowledge, with the basis
stated. None was re-fetched from a source (G-B3 applies). The axes are a choice; another
axis set is a different table, logged as a change.
