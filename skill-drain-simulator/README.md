# Skill Drain Simulator

Single-file browser simulator. A plant loses its veterans to retirement
and turnover. Scrap climbs, the scrap log blames the machines, and
inspectors get added to cover it. Two versions of the same plant (A and
B) run side by side so a setting can be changed and the outcome compared.

Illustrative model with assumed numbers, not plant data. It shows the
shape of the mechanism, not a forecast.

## Flow

```
turnover + retirement wave
        │
        ▼
veterans leave ──► mentors per new hire falls ──► learning slows
        │                                              │
        ▼                                              ▼
in-house repair share falls              operator skill stays low
        │                                              │
        ▼                                              ▼
repairs sent outside              missed drifts ──► scrap climbs
                                                       │
                                  log reads "equipment" │ (cause hidden)
                                                       ▼
                                          inspectors added per +400 parts
```

## Model (all constants assumed)

- 20 operators, 60 months, averaged over 40 seeded runs.
- Start: 12 veterans (skill 0.85-0.97), 8 mid-tenure (0.25-0.65).
- Each machine drifts ~3 times a month; the operator catches a drift with
  probability equal to their skill. A missed drift = 40 scrapped parts.
- True equipment failures ~0.3 a month, uncatchable by anyone.
- Skill grows toward 1 with time on the machine; learning slows when there
  are fewer than 1 veteran per 3 new hires.
- Written screen: new hires start near zero skill and quit twice as often in
  year one. Hands-on trial: new hires start with some mechanical skill and
  quit at the normal rate.
- Reserve line: that many senior veterans never quit, always mentor, and hand
  off to a replacement who starts at skill 0.5.
- Repairs stay in-house in proportion to veterans on site (4 covers every
  shift). Inspectors: 2 plus one for each 400 scrapped parts a month above the
  starting level.

## Readouts

- Table at month 60: scrap, change since month 1, veterans on the floor,
  inspectors, outside repairs, month the floor drops below 1 veteran, share of
  scrap that was catchable drift.
- Four charts (Plant A solid, Plant B dashed).
- Scrap log at month 36 for Plant A: what the log records (100% equipment)
  against what happened (missed drift vs true failure).
- Lead time: the veteran indicator (veterans down 30%) against the scrap alarm
  (scrap 50% above start). The indicator usually trips months earlier.

## How to use

Open `index.html` in any browser. Offline-capable except for the Google Fonts
link, which falls back to system fonts. No install, no server. Light and dark
themes follow the system setting.

## Status

Delivered as-is. Not audited against the repo's claim-table convention; no
`CLAIM_TABLE.md` yet. Every number is a stated assumption, so any finding
drawn from it is a property of the model.

CC0.
