# FWO-4 — Research designs

Study designs for the publication loop, each with scope and the cheapest
first run. Nothing here has been run. Every literature figure is
**carried** from the work order and verified against nothing: the
publisher hosts refuse CONNECT from this environment (measured,
`SOURCES.md`). Prior-art checks that need those hosts are recorded
`NOT_RUN`; what was checked is the in-tree corpus.

Provenance tags: OBSERVED (stated by the person who raised it, or by a
living practice), DERIVED (follows from stated structure), PROPOSED
(a candidate reading, untested).

---

## R-1 TIME vs MONEY — depth of answer

**Existing result (carried):** Whillans, Weidman & Dunn — about 48%
preferred more time over more money across six studies (N ~4,690),
holding even for the time-poor. Not read here.

**OBSERVED (person raising it):** go one level down — people choose money
to pay bills and get out of debt SO THAT they have more time. The stated
preference for money can be an instrumental preference for time.

**Design.** Same respondent, two forms, order counterbalanced:

```
form A   standard time-vs-money choice (the existing item)
form B   the same choice with the money restricted: it can only be
         used to pay OTHER people's bills (no own-debt relief, no own
         obligated hours bought back)
```

The within-person shift A → B is the instrumentality measure. A
respondent who chooses money on A and time on B was choosing money on A
for what it buys them; one who chooses money on both is choosing money
as money. The unit is the person, the readout is the paired shift, and
the population figure is the share who shift.

**Scope.** Measures instrumentality of a stated money preference. Does
not measure whether time is preferred once bought; does not reach
respondents with no bills (form B is inert for them, and they are
counted apart, not dropped).

**Kill condition.** The shift is zero across debt strata: money is
preferred as money, and the one-level-down reading fails.

**Cheapest first run (no new collection).** Correlate the existing
time/money split with debt load and obligated hours in any dataset
carrying both. A positive slope of money-preference on debt is
consistent with the instrumental reading and does not establish it;
form B is what separates the two.

**Prior-art check:** NOT_RUN for the published literature (hosts refuse
CONNECT). In-tree: `false-tradeoff/` classifies a posed dilemma as a
property of the system or of the posing and would file "time vs money"
under its CHECK 1 (option-set provenance) before any design runs — worth
running first, since if the tradeoff is posed rather than structural the
design is measuring the posing. PROPOSED.

---

## R-2 TEMPLE vs FORAGE-ONLY MACAQUE TROOPS

**Existing (carried):** free-ranging long-tailed macaques rob and barter
objects for food, described as a culturally maintained token economy
(Phil Trans R Soc B 376:1819, 20190677). Learned, transmitted, tracks the
human value scale. Not read here.

**NOT MEASURED anywhere found (per the work order):** whether foraging
skill declines in token-trading troops.

**Design.** Token-trading troop vs forage-only troop, same species, same
region, same season window. Measure per troop: time allocation
(foraging / trading / other), foraging success on a fixed task, and what
juveniles observe (who they watch, doing what). Tourist supply
fluctuates seasonally, which is a natural variation in token
availability inside one troop — a within-troop arm for free.

**Two channels to separate, by design:**

```
adult stops practising     -> adult foraging success falls with token
                              exposure while juvenile observation is
                              held constant
juvenile never observes    -> juvenile foraging success falls with
                              what they watched, not with their own
                              token use
```

The two need different remedies and a pooled "skill declined" cannot
tell them apart.

**Do not score non-use of a token as incapacity.** Human populations
that fully understand a token system and decline it show the design
cannot separate "does not grasp it" from "grasps and declines" without
an added arm: a comprehension probe that does not require use (a token
presented with no food behind it; does the animal treat it as a token).
Without that arm, a low-trading animal is UNKNOWN on comprehension, not
incapable. DERIVED from the standing rule that UNKNOWN is a value.

**Scope.** One species, one region; the token economy is
tourist-supplied, so the finding is about supply-coupled tokens, not
tokens as such.

**Kill condition.** Foraging success does not differ between troops at
matched season, and juvenile observation time does not differ: the
token economy is additive, not substitutive.

**Cheapest first run.** Time-allocation scans only, two troops, one
season, no foraging task: if trading time does not displace foraging
time there is nothing for the full design to find.

**Prior-art check:** NOT_RUN (hosts refuse CONNECT). In-tree:
`experience-ledger/` is built on exactly the asymmetry this design turns
on (competence decays, standing does not) and its `procedural-motor`
decay class is the channel "adult stops practising"; the design could
file its readouts into that ledger's classes rather than a new
vocabulary. PROPOSED.

---

## R-3 DIVERGENCE WITH INTERMITTENT CONTACT

**OBSERVED (living practice):** groups that cannot get along separate,
even by avoidance; after generations apart there is more to learn from
each other; reconnection stays TENTATIVE. Keeps variation and keeps
blind spots findable from outside.

**Question.** Do innovation rates track maintained divergence with
intermittent contact, against homogenization on one side and full
isolation on the other?

**Design.** Three arms, held apart by the contact regime:

```
isolated       no contact after the split
intermittent   contact at intervals, TENTATIVE: exchange of practice
               allowed, merger of membership not
homogenized    continuous contact with free movement of members
```

The readout is an innovation rate per arm (new practices per interval
that did not exist in either group before contact), and a second readout
the practice itself names: blind spots found from outside (a defect in
one group's practice first named by the other). Contact must stay
tentative in the design — merging destroys the variable, since a merged
population is the homogenized arm wearing the intermittent label.

**Scope.** Group-level practice, not individual learning. The arm
labels are regimes of contact, not judgements of the groups.

**Kill condition.** Innovation rate is monotone in contact (highest in
the homogenized arm): intermittency buys nothing and the practice's
reading fails. The other failure, isolation highest, kills the "more to
learn from each other" half.

**Cheapest first run.** No new population: code an existing comparative
record of related groups for contact regime and dated practice
introductions, and read the rate per regime. A confound to declare
before coding: contact regime is rarely assigned, so groups in each arm
differ on what put them there.

**Prior-art check:** NOT_RUN for the cultural-evolution, population-
structure and innovation literature (hosts refuse CONNECT). In-tree:
`continuity-audit/` models homogenization as the collapse vector on a
diversity field (its README, line 20: "homogenization -- breaks -->
both") and `consensus-anchor/` finds full agreement with zero consensus
under one coupling rule; both are the homogenized arm as arithmetic and
neither has an intermittent arm. `transmission-decay/` and
`revision-mechanism/` carry the ethics section this design also needs
(publishing a group's practice can damage the mechanism studied).
PROPOSED.

---

## R-4 UNIVERSE 25 CONDITION MATCHING IN THE CITING LITERATURE

**Design.** Code a sample of works citing Calhoun for claims about human
populations. Per work, three fields:

```
population_named        which human population the claim is about
condition_checked       whether ANY entry condition of the apparatus is
                        checked against that population
stocks_coupled          which of the eight rows (food, water, shelter,
                        thermal, predation, disease, waste_removal, exit)
                        the named population actually has COUPLED
```

Output: the rate of transfer with no condition check, and among checked
transfers the distribution of `entry_condition_match.py` overall
results. FWO-1 is the coding instrument: each cited population is a
`population.txt` against the demo `universe25_study.txt`.

**Scope.** Citing works only; the rate is a property of the citing
literature, not of the apparatus or of any population. The sample frame
must be stated (which index, which years) or the rate has no
denominator — the `QA_004` discipline.

**Kill condition.** The rate of unchecked transfer is low: the citing
literature already does the matching and FWO-1 adds nothing there.

**Cheapest first run.** Ten citing works from one index, coded by one
reader with the three fields above; a second reader on the same ten
before the number is quoted, since `condition_checked` is a judgement.

**Prior-art check:** NOT_RUN (citation indexes refuse CONNECT). In-tree:
`falsifier-audit/` A4 (fixed-reference-body) is the adjacent check — a
transfer that silently supplies the study's frame as the population's is
that shape one level up. The Calhoun paper itself could not be read
here (`SOURCES.md`), so the study rows the coding runs against are the
work order's transcription and carry CARRIED status until corrected.
DERIVED.
