# Coupling vs border-maintenance energy: a yardstick

CC0. A reusable reasoning move, not a description of any person, body or
organization.

The glyph READS. It does not determine value for anyone. This note stops
at the readout: where the spend goes, as a fraction with its dependency
tree beside it. It ranks nothing and scores nobody.

Index line: reads energy routed to coupling vs to holding separations; a
readout, not a ranking.

Companions: `tools/contested_area_hidden_assumption.md` section 6 (its
adversarial pass routes the scale confound here) and
`tools/natural_two_senses.md` (section 4 below).

Tags: OBSERVED = stated in a source; DERIVED = follows from what is
stated here; PROPOSED = a reading not yet backed by a cited instance.
[co-authored] = stated in a worked voice session, 2026-10-13, human +
Claude, carried as stated. The stance it rests on is an inherited
tradition and is credited to no individual.

## 1. What it reads

Every configuration spends energy (money, hours, attention, material).
The yardstick sorts the spend by what it does, never by who spends it.

    COUPLING       spend that connects parts so something moves between
                   them: transport, repair, exchange, shared care, signal
                   carried both ways
    BORDER         spend that holds a separation in place: enforcing it,
                   checking it, advertising it, defending it
    COORDINATING   a boundary that does work for the parts it separates:
                   a membrane, a protocol, a record both sides use

The readout is the BORDER FRACTION, border spend over classified spend,
read twice:

    DIRECT       border items only
    ROLLED UP    border items plus everything that exists to hold a border
                 item up, through the dependency tree (section 2)

## 2. The dependency tree

[co-authored; DERIVED] A border is rarely paid for by its own line item.
It stands on a chain, and the chain can close on itself:

    enforcement -> administration -> funding -> extraction -> more enforcement

Read X -> Y as "X depends on Y": Y is spent so that X can stand. The
rolled-up reading follows those edges from every border item:

    EXCLUSIVE   an item reached only from border items rolls up in full
    SHARED      an item also reached from a coupling or coordinating item
                is NOT split by an assumed ratio. The rolled-up reading
                becomes a band, [exclusive, exclusive + shared]
    LOOP        a cycle through a border item is printed as found. A loop
                is the self-feeding shape: the separation pays for the
                extraction that pays for the separation

## 3. Domains

[co-authored] Where the sort applies. Each row is a reading pattern, not a
claim about any actual body.

    domain                     reads as coupling       reads as border
    governance                 services delivered,     enforcement of who
                               roads, records kept     may enter or count
    mandates and rules         a rule that lowers the  a rule whose upkeep
                               cost of working         rises with the
                               together                pressure against it
    artificial-scarcity        production and          holding supply below
    economies                  delivery                what could be made
    marketing                  information a buyer     differentiation that
                               uses                    holds a customer in
    us/them politics           shared problems worked  the line between the
                               on                      groups, maintained
    lobbying                   (rarely)                access held against
                                                       other claimants
    inter-faith conflict       shared practice, aid    the boundary of who
                                                       counts, defended

Classifying any item is the reader's call (section 5, third edge).

## 4. The reading

[PROPOSED] A high border fraction predicts a scale ceiling. Border spend
grows with the number of separations held and with the pressure against
each; coupling spend returns throughput. A configuration whose spend is
mostly holding has less left over to move anything, so it stops growing
before it stops spending.

Read trajectory from spend, not from stated aim. A stated aim is a label
(`tools/contested_area_hidden_assumption.md` 6.a); the spend is the
configuration.

Tie to `tools/natural_two_senses.md`: sense 1 of "natural" is "survives
unpaid". A border that needs rising enforcement to stand is billed
continuously, which is that note's FAMILIAR UN-NATURE: familiar, and
paid for every day.

## 5. Honest edges

1. It reads throughput and trajectory, not truth or moral worth. A high
   border fraction says where the energy goes; it says nothing about
   whether a separation is right.
2. Coordinating boundary vs border held for leverage. Some boundaries do
   work for both sides. PROPOSED test, not yet run on any case: does the
   boundary keep its own upkeep, or does it need rising enforcement to
   stand? It needs at least two dated snapshots of the same
   configuration (`--compare` below); one snapshot cannot answer it.
3. Classification is a boundary choice (`tools/contested_area_hidden_assumption.md`
   check (a)). Every class is the reader's call and enters as input, in
   the open. An item the reader cannot classify is a GAP: listed with its
   spend, outside every fraction, never assumed.
4. The reader is coupled. Publishing a readout can change the allocation
   it reads (`tools/contested_area_hidden_assumption.md` 6.g), so a
   reading taken after publication is not independent of the one taken
   before.

## 6. The instrument

`tools/yardstick.py` in the Simulators repository, stdlib only. Input is
a JSON list:

    {"item": "name", "spend": 50, "class": "coupling|border|coordinating",
     "depends_on": ["other item", ...]}

Output: the direct and rolled-up border fractions (a band when anything
is shared), the gaps with their spend and the span they could move each
fraction across, any dependency on an item not in the input, and every
loop through a border item. `--compare a.json b.json` prints two dated
snapshots side by side. No output carries a verdict.

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
