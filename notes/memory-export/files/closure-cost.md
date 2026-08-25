---
name: closure-cost
description: Marker under exploration — response failure tracks prior closure (a variable closed as impossible) rather than event severity or information availability.
sources: [field]
aliases: [closure cost, prior closure, categorisation stall, diagnostic spend, instrument closure]
---

MARKER, not a position under defense.

## The shape

If a variable is held at a LOW LIVE PROBABILITY rather than closed as impossible, the handling
class already exists when the event fires. So the delay is not reaction time — it is
CATEGORISATION STALLING, because the reading contradicts something held as permanent.

- "That couldn't happen here / to me" is a variable removed from the tally, not a low estimate.
- Missing protocol is NOT an independent explanation: nobody learns a procedure for an event
  they have closed, so the procedure gap is a downstream readout of the closure.
- Information availability cannot explain the gap where a documented, memorialised local
  instance already exists (the Pearl Harbor point).

## Two branches

1. **Instrument closure** — over-reliance on a working instrument. Dash lights, crossing
   signals, train signals. Counter-practice: look at the track regardless.
2. **Event closure** — the event itself is closed. Breakdown cones: drivers report never being
   told a documented procedure.

Experienced operators are generally better; their mistakes are the things taken for granted
that have a closure behind them.

## Condition that prevents closure forming

Tight coupling to an environment with a probability matrix the participants can always act
outside of — bears, wolves, moose. A channel that never permits closure, so closure never
becomes habit. This suggests closure is a trained artifact of stable environments, not a
default of cognition.

## Operating side

On a mid-event unknown, quarantine the diagnostic until the vehicle stops. Spending the
resource on categorising costs the resource the situation needs.

## Scope

Explicitly NOT a trauma measurement and not a comparison between people. A trauma-measurement
design was proposed against this marker and rejected — it answers a question the marker does
not ask.

## Built

`closure.py` (15/15), README, CLAIM_TABLE C1–C5, three cases: missile-alert, breakdown-cones,
dash-warning-light. **Zero quantified** — every `diagnostic_spend` reads `--` and every
`knowledge_state` reads `not_separable`.

## Literature checked

- Hawaii 2018: most did not take protective action; the dominant response was
  information-seeking across a 38-minute window against a roughly 15-minute real budget. Of
  the quarter who thought it might be real, few acted, and those who did largely had been told
  what to do. About 64% of Americans had never heard any nuclear-attack recommendation. Some
  discounted the alert because air-raid sirens were silent — an instrument-branch fragment
  sitting inside an event case.
- Rail crossings: raw 62% active / 28% passive is exposure-free and unusable. DOT
  collision-prediction equations fit separate factors per warning-device category, which is
  circular for this test.
- Signal-detection work on driver beta at passive crossings (1986 vs 2006, roughly 50x change)
  is the nearest real instrument and was not chased.

## Next

Breakdown-cones is the highest-value case and has no data: ordinary base rate, documented
delivery, knowledge checkable cold with no event required. **The recall method must be
specified first** — same defect as generation-capacity R1.
