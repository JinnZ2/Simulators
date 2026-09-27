# FABLE WORK ORDER PACKET — 2026-09-26

*(delivered verbatim; the build's own notes are in `README.md` and `CLAIM_TABLE.md`)*

```
target:   Claude Fable 5.1
repo:     JinnZ2/route-independence (create if absent)
          FWO-3 may land in JinnZ2/method-layer instead — check first
license:  CC0
stdlib only, phone-buildable, no network calls at runtime
```

## STANDING RULES FOR EVERY ITEM

```
- These are INSTRUMENTS, not arguments. No verdict language.
  Output reports what was found, the scope, and what is unresolved.
- UNKNOWN is a first-class return value, never an error and never
  filled with a default. A row the builder cannot source stays UNKNOWN.
- Every demo value carries a SOURCE field. Values with no source are
  marked SYNTHETIC in the output, not silently mixed with sourced ones.
- Provenance tags on every claim in docs: OBSERVED / DERIVED / PROPOSED.
- CHECK FIRST on each item: search for an existing instrument that
  already does this. If one exists, report it and STOP that item.
  A found prior instrument is a result, not a failure.
- Do not add a characterization of any person to any file.
```

---

## FWO-1 — entry_condition_match.py
**The comparison discipline: match entry conditions before transferring a result.**

```
PROBLEM
  Results from a study get applied to populations that never met the
  study's entry conditions. Worked case: Calhoun's Universe 25, applied
  to whole human societies including populations short on food, water,
  heat and housing — none of whom meet the apparatus's conditions.

INPUT
  study.txt        one row per entry condition:
                   condition / state / source
                   state in {DECOUPLED, COUPLED, REMOVED, PRESENT, UNKNOWN}
  population.txt   same rows, for a candidate population

OUTPUT per row
  MATCH | MISMATCH | UNKNOWN(reason)

OUTPUT overall
  TRANSFERABLE      every row MATCH
  PARTIAL(rows)     at least one MATCH and at least one MISMATCH —
                    list which hold and which fail
  NOT_TRANSFERABLE  no row matches
  NOT_EVALUABLE     any load-bearing row UNKNOWN
  Keep PARTIAL and NOT_TRANSFERABLE distinct. Collapsing them
  destroys the information.

DEFINITION TO BUILD IN
  DECOUPLED = provision arrives without the recipient's effort or
  exchange. COUPLED = provision stops when effort stops.
  This is BINARY. Do not build a gradient. High consumption with
  effort-coupling is COUPLED, not "partly decoupled." (OBSERVED,
  stated by the person who raised the case.)

COUNTABLE MARKER (optional field, housing row)
  dwellings_held > 1  ->  housing DECOUPLED
  Rationale: a body occupies one dwelling at a time; holdings past
  physical occupancy are no longer meeting the need.

DEMO — Universe 25, designer-documented conditions
  Calhoun called the design a "Mortality-Inhibiting Environment for
  Mice." Removed by design: emigration, resource shortage, weather,
  disease, predation. Founders disease-free; enclosure cleaned
  regularly; temperature stable.
  Rows:
    food              DECOUPLED
    water             DECOUPLED
    shelter           DECOUPLED (nest boxes supplied)
    thermal           DECOUPLED (temperature held)
    predation         REMOVED
    disease           REMOVED (screened founders)
    waste_removal     DECOUPLED (experimenters cleaned)
    exit/emigration   REMOVED
  Sources: Calhoun 1973 "Death Squared," Proc R Soc Med; secondary
  reconstructions (Emrick; Science History Institute; Ramsden).
  READ THE 1973 PAPER DIRECTLY if accessible and correct any row.

  Candidate populations: (a) effort-coupled households,
  (b) population lacking reliable food/water/heat,
  (c) stratum paying others for all provision, multiple dwellings.

  EXPECTED STRUCTURE, stated before the run so the demo can fail:
    (a), (b) mismatch on most provision rows
    (c) matches on provision rows and MISMATCHES on exit —
        (c) has the most exit of any population; the mice had none.
  If the tool returns TRANSFERABLE for (c), the tool is wrong.
  OPEN, do not resolve in code: whether (c) is a partial match or
  whether no human population meets the full condition.

TESTS
  - one row UNKNOWN -> never TRANSFERABLE
  - PARTIAL lists both sides
  - a demo input that fails (required)
```

---

## FWO-2 — route_independence.py
**Two measures, not one: how many routes exist, and whether each can settle in its own medium.**

```
PROBLEM
  Counting alternative routes to a need (food, water, shelter, heat)
  overstates independence when every route must ultimately discharge
  its obligations in one medium. Worked case: US barter is taxable at
  fair market value stated in dollars (IRS Topic 420; 1099-B for
  exchanges, 1099-MISC for informal barter over $600), so a barter
  route is denominated in dollars even when no dollars move.
  Route count stays high while independence is zero.

INPUT  routes.txt, one row per route:
  need / route / settles_in / obligation_medium / source

  settles_in         the medium the route's own exchanges use
  obligation_medium  the medium its external obligations (tax, fines,
                     fees) must be paid in

MEASURES per need
  route_count           number of distinct routes
  independent_count     routes where settles_in == obligation_medium
                        AND obligation_medium is not the dominant token
  independence_ratio    independent_count / route_count
                        (NOT_EVALUABLE if route_count == 0)

FLAG
  ENCLOSED_PLURALITY    route_count >= 2 and independent_count == 0
  This is the finding the single count cannot show.

DEMO rows (sourced or marked SYNTHETIC)
  barter, cash market, co-op, gift/mutual aid, household production,
  crypto (exchange taxed at dollar value; non-reporting fined in
  dollars), Amish community (settles obligations in cash).
  DERIVED note to carry: household production is genuinely outside
  but cannot scale or specialize — the boundary sits around
  COORDINATION, not subsistence.

TEST OF THE TEST
  A single output field for "the route is permitted" vs "the route
  can discharge its own obligations" — if the tool merges them, it
  reproduces the error it exists to catch.
```

---

## FWO-3 — untried_options_audit.py
**A decision record check: were the options enumerated, and was cost bound to the decider?**

```
SOURCE OF THE STRUCTURE
  Described as the war-initiation protocol of a living practice;
  source withheld at request. Carry that line verbatim. Do not attach
  a name. It is a load-tested operating protocol, not a design
  composed for this build.

  Structure as described (OBSERVED):
    - only a body composed of those who bore the prior cost could
      authorize; the proposing body could want but not grant
    - proposers had to name THEMSELVES, their friends and family as
      those who would bear first consequences — not others
    - full disclosure: consequences of the last instance, this
      instance, all options TRIED, all options NOT TRIED
    - a third party (neither proposer nor authorizer) could name an
      untried option, which then had to be tried first
    - if that party named an option the record had omitted, the
      record was returned: the work was not done correctly; redo

  DERIVED (Claude): functionally a failure-mode analysis with an
  independent verifier who can send it back. Rarity of the action is
  the output of a correctly specified test, not a separate value.

INPUT  decision_record.txt, fields:
  decision / proposer / first_cost_bearers / authorizer /
  authorizer_prior_exposure / options_tried / options_not_tried /
  reviewer / reviewer_added_options / source

CHECKS (report presence and content; no verdict)
  C1  first_cost_bearers includes proposer?     YES | NO | UNKNOWN
  C2  authorizer_prior_exposure recorded?       YES | NO | UNKNOWN
  C3  options_not_tried field present and
      non-empty?                                YES | NO | ABSENT_FIELD
  C4  independent reviewer with authority to
      add options?                              YES | NO | UNKNOWN
  C5  any reviewer_added_option not already in
      options_tried or options_not_tried?       -> RETURN_FOR_REDO
                                                   (list the options)

  ABSENT_FIELD (the record has no slot for it at all) is a different
  result from NO (slot present, empty). Keep them separate — the
  missing slot is the more important finding.

DEMO
  At least one real published decision document, any domain,
  field-coded with sources. Expected: C3 returns ABSENT_FIELD on most
  institutional records. If a record type WITH an untried-options
  field exists, that is a finding — report it prominently.
  Candidate domain to also run: a published AI alignment proposal.
  PROPOSED (Claude): such proposals are evaluated on whether the
  argument holds, never on whether the option space was enumerated.
  The demo can falsify that.
```

---

## FWO-4 — RESEARCH DESIGNS (write-up, not code)
**For the publication loop. Post as study designs with scope and cheapest first run.**

```
R-1  TIME vs MONEY — DEPTH OF ANSWER
     Existing result: Whillans, Weidman & Dunn — about 48% preferred
     more time over more money across six studies (N ~4,690), holding
     even for the time-poor.
     OBSERVED (person raising it): go one level down — people choose
     money to pay bills and get out of debt SO THAT they have more time.
     Design: same respondent, two forms:
       form A  standard time vs money choice
       form B  money restricted to paying OTHER people's bills
     The within-person shift A -> B is the instrumentality measure.
     Cheapest first run: correlate the existing split with debt load
     and obligated hours from any dataset carrying both.
     Prior-art check required.

R-2  TEMPLE vs FORAGE-ONLY MACAQUE TROOPS
     Existing: free-ranging long-tailed macaques rob and barter objects
     for food — described as a culturally maintained token economy
     (Phil Trans R Soc B 376:1819, 20190677). Learned, transmitted,
     tracks human value scale.
     NOT MEASURED anywhere found: whether foraging skill declines.
     Design: token-trading troop vs forage-only troop, same species and
     region. Measure time allocation, foraging success, what juveniles
     observe. Tourist supply fluctuates seasonally -> natural variation.
     Two channels to separate: adult stops practicing; juvenile never
     observes. No lab required.
     DO NOT SCORE non-use of a token as incapacity: human populations
     that fully understand a token system and decline it show the
     design cannot separate "does not grasp it" from "grasps and
     declines" without an added arm.

R-3  DIVERGENCE WITH INTERMITTENT CONTACT
     OBSERVED (living practice): groups that cannot get along separate,
     even by avoidance; after generations apart there is more to learn
     from each other; reconnection stays TENTATIVE. Keeps variation and
     keeps blind spots findable from outside.
     Question: do innovation rates track maintained divergence with
     intermittent contact, vs homogenization, vs full isolation?
     Contact must stay tentative in the design — merging destroys the
     variable.
     Prior-art check: cultural evolution, population structure and
     innovation literature.

R-4  UNIVERSE 25 CONDITION MATCHING IN THE CITING LITERATURE
     Code a sample of works citing Calhoun for claims about human
     populations. Per work: population named; whether any entry
     condition is checked; which stocks the population actually has
     coupled. Output: rate of transfer with no condition check.
     Uses FWO-1 as the coding instrument.
```

---

## RETURN FORMAT

```
per item:
  STOPPED_PRIOR_ART(citation) | BUILT | DESIGN_WRITTEN
  claims list with ids
  demo output including the failing input
  what stayed UNKNOWN and why
```
