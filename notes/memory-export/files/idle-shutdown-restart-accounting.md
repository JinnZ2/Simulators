---
name: idle-shutdown-restart-accounting
description: Marker under exploration — automatic idle-shutdown restart cycling as an uninstrumented cost channel; fuel savings counted, restart emissions/DEF/component wear not.
sources: [field]
aliases: [idle shutdown, two-minute shutoff, restart cycling, auto-stop, cold restart accounting, DEF cold window]
---

MARKER, not a position under defense. Test fit, extend, or report where it breaks.

## The configuration

- Automatic idle shutdown cuts the engine after a fixed short interval (two minutes is a
  common setting), with a cold-weather override threshold typically set near 0 °F, some
  fleets at −15 to −20 °F.
- A pre-trip inspection runs roughly fifteen minutes and requires the cab to stay warm.
  Against a two-minute shutoff, the engine is restarted repeatedly within a single pre-trip.
- **The restart count is imposed by the interval mismatch, not chosen by the operator.** Any
  task whose duration exceeds the shutoff interval generates the same pattern.

## Cost channels unaccounted against the fuel saving

- Ignition and start-system component degradation
- Electrical draw on components per start cycle
- DEF output during cold restarts
- Cold-restart emissions, which are not the same per-unit as steady-state idle emissions

## The question

Is the fuel saving worth those channels — and is any of it measured? The saving is counted
because fuel is metered and billed. The cost channels have no meter, so the policy is
evaluated on the only side that has an instrument.

## Why it reads as an exclusion, not an error

This is an uninstrumented gap: it wants identifying as a gap needing instrumentation even
without a resolved answer. A comparison that runs on the metered side alone will return the
same result regardless of the true balance.

## Where it would show up at scale

Rural cold-climate corridors with heavy truck traffic — restart counts stack up there and
air-quality monitoring is absent. Both terms co-locate, so the effect is largest exactly
where nothing is measuring.
