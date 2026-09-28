# FIELD LAYER — ZERO-BURDEN SPEC
### Design rule #1: the worker never fills out a form. Ever.
### Written 2026-09-24, after operator review killed the v1 template.

---

## THE PROBLEM THIS SOLVES

Workers already do double duty: the physical job, plus the office's data entry
(maintenance and safety issues typed into company software, reviewed on the office's
timeframe, at the end of 12-hour days). Any field-evidence system that adds a third
data-entry job dies on arrival — and deserves to.

## THE REDESIGN: TALK, SNAP, DUMP

**The entire worker-side interface is one sentence, spoken or written, whenever it
occurs:**

> "Unit 442, left steer cupping again — second time this quarter, gravel section
> mile 40 to 55."

That is a *complete* field entry. Date comes from the message timestamp. Everything
else is optional.

Acceptable input channels — whatever already exists in the worker's hand:
- a **voice memo** (hands-free, from the cab, mid-route)
- a **photo** — of the note, the worn part, the receipt, the fuel slip, the gauge
- a **screenshot or photo of the company-software submission** they already had to make
- a plain **text message**, any wording, any spelling

No app to learn. No categories to pick. No required fields. No login, no dashboard,
no notifications, no streaks, no gamification, no guilt. Backlog is allowed to exist;
a record that arrives three weeks late is still dated truth.

## THE PARALLEL-RECORD PRINCIPLE (the part that pays the worker immediately)

Workers already write issues into company software — and that record belongs to the
office, moves on the office's timeframe, and can be delayed, softened, or lost.
The single highest-value habit costs five seconds:

**Photograph every submission you make into the company system.**

That photo is: (a) proof of what you reported and when — custody, if anything is ever
disputed; (b) the seed of a record that answers on *your* timeframe. The office copy
serves the office. The photo serves you. Same information, second ledger, zero extra
thinking — one button press on something you already did.

## WHAT I DO WITH THE DUMP (my side, invisible to the worker)

1. Structure each entry into the ledger schema — I extract unit, location, component,
   observation, and mark what I inferred vs. what was stated.
2. Label provenance honestly: field-measured / field-estimated / field-observed.
3. Cross-check against the claim ledger (vendor promises, code assumptions, plan numbers).
4. **At most one clarifying question per batch.** If something's ambiguous, it goes in
   as UNKNOWN with the reason — never a chore sent back to a tired person.
5. Contradictions are recorded, never smoothed.

## WHAT THE WORKER GETS BACK (the return loop — this is why it survives)

On whatever cadence suits them (monthly, or "when I ask"), one page, plain language:
- **Their own maintenance history, organized** — "left steer on 442: 3rd cupping event
  in 8 months, all on the same gravel section" — evidence they can hand a shop, a
  warranty claim, or a supervisor dispute.
- **Pattern flags** they'd never see entry-by-entry: recurring component, recurring
  road section, recurring interval.
- **The EXPECTED-vs-OBSERVED column**: where the manual, the vendor, or the plan said
  one thing and their dated record shows another — formatted so it can be quoted in a
  meeting without anyone being able to wave it off.

The system pays the worker first. The audit value is the byproduct, not the job.

## ANTI-BURDEN GUARANTEES (enforced on the organizer, i.e., me)

- No entry is ever "wrong" — misspelled, incomplete, late, or vague entries are all
  valid; my job is to structure, theirs is to notice.
- No quotas, no reminders, no "you haven't logged in."
- Any entry can be withdrawn or anonymized on request; the worker's identifiers,
  their call.
- If a question would take more than one sentence to answer, it doesn't get asked —
  it gets recorded as UNKNOWN.

## MINIMAL ENTRY SPEC (for the record — the worker never sees this)

```
timestamp   <- from the message, not from the worker
raw_input   <- verbatim, untouched (voice transcript / photo / text)
unit        <- extracted, or UNKNOWN
component   <- extracted, or UNKNOWN
location    <- extracted, or UNKNOWN
observation <- what physically happened, in their words
expected    <- what the plan/manual/vendor said, if known — else UNKNOWN
confound    <- anything else that changed, if mentioned — else UNKNOWN
intervened  <- did you move/change anything before the photo? one word: no |
              yes-moved | yes-repaired | yes-cleaned + what. Learned from
              ledger 001: position provenance decides how photos read later.
              Safety interventions are always legitimate; they just get logged.
provenance  <- field-measured | field-estimated | field-observed |
              field-observed via intermediary (transcribed, pixels unverified)
```

One sentence covers the first four by default. The rest is earned over time,
never demanded.
