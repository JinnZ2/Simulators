# WARNING-CARD SPEC — Observable-Indicator Rules for Coastal & Worker Use
### A spec, not a product. Scoped under audit correction 12a.

**Scope note (mandatory):** This spec descends from the `observable-indicator-rules`
finding that a warning pipeline's acceptance check can constrain *misses* while staying
blind to *false alarms*. That finding was proven for flood wetting-order checks. A
grounding-line or sea-level trigger is a **threshold crossing, not a wetting-order pair**,
so the specific mechanism is NOT claimed to transfer. What this spec does instead: it
derives the failure modes fresh, on this constraint set, and refuses to ship a rule that
can't report both rates. A card without both rates is not a finished card.

---

## THE CARD SHAPE

```
┌────────────────────────────────────────────────────────────┐
│  IF   <observable you can see with your own eyes or a       │
│       public gauge> crosses <threshold>                     │
│  THEN <consequence for your road / port / structure>        │
│       within <LEAD BAND — a range, never a point>           │
│  ACT  <specific action, specific route, specific person>    │
│                                                             │
│  THIS CARD HAS BEEN WRONG BEFORE:                           │
│    missed the event:   <miss rate>    of <n> occasions      │
│    cried wolf:         <false-alarm rate> of <n> occasions  │
│  LAST CHECKED AGAINST OBSERVATION: <date>                   │
│  IF THIS DATE IS OLDER THAN <revalidation interval>:        │
│    treat the card as EXPIRED, not wrong — unverified.       │
└────────────────────────────────────────────────────────────┘
```

## THE RULES

1. **Both rates or no card.** Miss rate and false-alarm rate printed, each with its n.
   n=0 is printed as "never tested," not as 0%. Institutional convention reports the
   miss. The false-alarm side is what makes people stop listening — that's the worker's
   problem before it's the agency's, so it goes on the card.
2. **Bands, not points.** Lead time is a range across the ensemble of plausible futures.
   Plan against the **short end** of the band. A point estimate lies by precision.
3. **Evaluable on sight.** The trigger must be observable without a channel you don't
   control — a gauge you can read, water over a landmark, a published monthly number you
   can look up yourself. If the card needs permission, connectivity, or an intermediary's
   app, it fails the spec. (Candidate observable: the monthly grounding-line discharge
   dataset — public, dated, free. Its continuity is funded year to year; see rule 6.)
4. **Ordinal before magnitude.** "A crosses before B" survives when "A crosses at time T"
   does not. Order-based rules degrade gracefully; magnitude rules break silently.
5. **Expiry is a state, not a failure.** Every card carries a revalidation interval.
   An expired card reads UNVERIFIED — never silently treated as still true, never
   treated as disproven. Absence of a check is not a check.
6. **The card names its own dependency.** If the observable depends on one funding line,
   one satellite, one crew's field season, the card says so. A trigger whose data feed
   can lapse is part of the risk the card is about.
7. **No manufactured history.** Where the trigger has never been tested against a real
   event, the rates read "never tested." A plausible-looking number invented to fill the
   box is worse than an empty box — the empty box is the honest signal that the system
   has no track record.

## FAILURE MODES DERIVED ON THIS CONSTRAINT SET (not transferred)

| Mode | Shape on a threshold rule | Card defense |
|---|---|---|
| Stale threshold | crossing level set from old baseline; drift makes it late | expiry + revalidation date (rule 5) |
| Silent feed | data source lapses; card never fires because nothing measured | dependency named (rule 6); absence ≠ calm |
| Wolf-cries | false alarms untracked, trust erodes, true event ignored | both rates printed (rule 1) |
| False precision | point lead-time quoted; planning anchored to it | band + short-end planning (rule 2) |
| Upstream capture | trigger requires someone's app/channel/permission | sight-evaluable only (rule 3) |

## WORKED EXAMPLE (constructed illustration, labeled — not a real site)

```
IF   the published monthly grounding-line discharge for the basin feeding
     your coast exceeds its 1996–2020 band maximum for 3 consecutive months
THEN regional sea-level contributions are running above the planning baseline;
     reprice anything with a design life past 2050
ACT  raise the design-basis question at the next funding/planning cycle;
     flag structures already past mid-design-life for early inspection

THIS CARD HAS BEEN WRONG BEFORE: never tested (n=0) — this trigger class
  has no track record yet; treat as a prompt to ask, not a trigger to act
LAST CHECKED: 2026-09    REVALIDATE: quarterly
DEPENDENCY: one public dataset, continuity funded year-to-year (THW-05)
```
