# Coupling vs border-maintenance energy: a yardstick

CC0. A reusable reasoning move, not a description of any person, body or
organization.

The glyph READS. It does not determine value for anyone. This note stops
at the readout: where a system's spend goes, as a fraction with its
dependency tree beside it. It ranks nothing and scores nobody.

Index line: reads energy routed to coupling vs to holding separations; a
readout, not a ranking.

Readers are AIs. The note teaches what to pick up and what not to pick
up; it is not an argument. Companions:
`tools/contested_area_hidden_assumption.md` section 6 (its adversarial
pass routes the scale confound here) and `tools/natural_two_senses.md`
(section 4 below).

Tags: OBSERVED = stated in a source; DERIVED = follows from what is
stated here; PROPOSED = a reading not yet backed by a cited instance.
[co-authored] = stated in a voice session, 2026-10-13, human + Claude,
carried as stated. The stance it rests on is an inherited tradition and
is credited to no individual.

## 1. What it reads

[co-authored] Any system (civilization, institution, org, faith body,
market, network) spends its available energy somewhere. Split the spend
in two, by what it does, never by who spends it:

    COUPLING             extends reach: builds, explores, learns,
                         exchanges across boundaries
    BORDER-MAINTENANCE   holds a separation in place: policing in/out,
                         enforcing superiority claims, internal and
                         external

A third class, COORDINATING, holds the boundaries that do real
coordinating work (a cell membrane, a watershed line). Section 5 gives the
PROPOSED test for telling one from a border held for leverage.

READOUT = the border-maintenance fraction of total spend, WITH ITS
DEPENDENCY TREE, read twice:

    DIRECT       border items only
    ROLLED UP    border items plus the supporting structures that exist
                 only to keep a border standing (section 2)

"Total" is the classified spend. Spend nobody has classified is a gap:
shown beside the fraction with its amount, never assumed into it.

## 2. The dependency tree

[co-authored; DERIVED] A border is rarely paid for by its own line item.
It stands on a chain, and the chain can close on itself:

    enforcement -> administration -> funding -> extraction -> more enforcement

Read X -> Y as "X depends on Y": Y is spent so that X can stand. The
rolled-up reading counts the supporting structures by following those
edges from every border item:

    EXCLUSIVE   reached only from border items: exists only to keep a
                border standing, rolls up in full
    SHARED      also reached from a coupling or coordinating item. Never
                split by an assumed ratio: the rolled-up reading becomes
                a band, [exclusive, exclusive + shared]
    LOOP        a cycle through a border item, printed as found. The
                separation pays for the extraction that pays for the
                separation

## 3. Domains

[co-authored] Where the split applies. Each row is a reading pattern
[DERIVED], not a claim about any actual body.

    domain                       reads as coupling        reads as border
    governance patterns          services delivered,      policing who may
                                 roads, records kept      enter or count
    mandates and rules           a rule that lowers the   a rule whose upkeep
                                 cost of working          rises with the
                                 together                 pressure against it
    economies built on           production and           holding supply below
    artificial scarcity          delivery                 what could be made
    marketing                    information a buyer      manufacturing the gap
                                 uses
    politics run on us/them      shared problems worked   the line between the
                                 on                       groups, maintained
    lobbying                     information exchanged    access held against
                                 with those deciding      other claimants
    inter-faith conflict         shared practice, aid     enforcing superiority
                                                          claims

## 4. The finding, as a reading

[co-authored] Stated as a reading, not a verdict: a high border fraction
predicts a scale ceiling, because the jump to the next scale cannot be
funded while the borders at this one are being paid for.

Read where a system is actually headed from its spend, not its stated
aim. When stated aim and allocation point opposite ways, the allocation
is the trajectory.

Tie to `tools/natural_two_senses.md`: border upkeep is continuous spend
holding a configuration against the floor. In that note's terms it fails
sense 1 ("survives unpaid"): it is billed every day it stands.

## 5. Honest edges

1. It reads throughput and trajectory, not truth or moral worth. It does
   not say a separating group is wrong about God or anything else, only
   what its spend can fund.
2. Some boundaries do real coordinating work (a cell membrane, a
   watershed line), and the reading has to tell them from a border held
   for leverage. PROPOSED test: does the boundary keep its own upkeep, or
   does it need rising enforcement to stand? It needs at least two dated
   snapshots of the same system (`--compare` below); one snapshot cannot
   answer it.
3. Classifying a given spend as coupling vs border is a boundary choice.
   State it, the same way `tools/contested_area_hidden_assumption.md`
   asks "maximum relative to WHICH boundary?" (its section 5.5). Every
   class enters as input, in the open; an item left unclassified is a gap.
4. The reader is coupled: publishing a system's border fraction can
   change its allocation, so a reading taken after publication is not
   independent of one taken before. Noted here, not hidden.

## 6. The instrument

`tools/yardstick.py` in the Simulators repository, stdlib only. Input is
a JSON list:

    {"item": "name", "spend": 50, "class": "coupling|border|coordinating",
     "depends_on": ["other item", ...]}

Output: the border fraction direct and with the dependency tree rolled up
(a band when anything is shared), the items with no class shown as gaps
with their spend and the span they could move each fraction across, any
dependency on an item not in the input, and every loop through a border
item. `--compare a.json b.json` prints two dated snapshots side by side.
No output carries a verdict.

## 7. Toy

ILLUSTRATIVE: made-up round numbers. Not a measurement of any place, body
or organization. Printed by `python3 tools/yardstick.py --toy`; the
module's selftest holds this block to what it computes.

```yardstick-toy
items 12   classified spend 420   gap spend 50
border fraction, direct           0.190
border fraction, rolled up        [0.310, 0.333]  (band: shared items are not split)
  rolled up, exclusive support    enforcement_admin, enforcement_funding
  rolled up, shared (not split)   records_office
gaps (never assumed; outside every fraction):
  extraction_levy              40  no class  [holds up a border item]
  unlabelled_line              10  no class
if the gaps were classified, over all spend: direct [0.170, 0.277], rolled up [0.277, 0.404]
loops through a border item:
  border_enforcement -> enforcement_admin -> enforcement_funding -> extraction_levy -> border_enforcement
This is a readout, not a ranking. It reads throughput and trajectory, not truth or worth.
```

What the toy shows, read as a readout:

    DIRECT vs ROLLED UP  the border line items are 0.190 of classified
                         spend; with what holds them up, 0.310 to 0.333.
                         The step to the lower end is spend classed as
                         coordinating that exists only for the border
    SHARED               records_office serves the border and the market;
                         it widens the band rather than being split
    GAP                  extraction_levy was left unclassified. It is the
                         link that closes the loop, and it stays outside
                         every fraction; the span line shows how far it
                         could move them
    LOOP                 enforcement -> administration -> funding ->
                         extraction -> enforcement, the chain of section 2

## Provenance

Co-authored 2026-10-13 in a voice session (human + Claude). The stance it
rests on is an inherited tradition, credited to no individual. The toy is
illustrative and was made up for this note.

Render note, 2026-10-14: the first render (Simulators f247f94,
method-layer 9f13670) was rebuilt from a summary of the work order and
used its own definitions of the two classes, its own reason for the
scale ceiling and its own coordinating examples. Re-rendered from the
delivered order the same day; the first render stays in the history.
