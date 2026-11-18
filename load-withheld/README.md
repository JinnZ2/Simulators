> Read first: [READING_PROTOCOL.md](../READING_PROTOCOL.md) (how to read this repo).
> Map, not prescription. Errors are data. Check it. Built for the need, revisable.

# load-withheld

CC0. Co-authored. Stdlib only, parses under Python 3.9, phone-buildable.

## Purpose

- Shared systems (yard tools, clouds, 911, EMS, hospitals, public benefits) are measured only by use. Demand people deliberately keep off them is invisible and counted as zero.
- That withheld demand is a hidden reserve. When it shrinks (skill loss, aging, exit), load rises with no warning.
- This is not "self-reliance." The center is the whole: carrying your own capacity so shared help stays available for those without alternatives.
- Skill breadth is the multiplier: more skills = more places load can be withheld.
- Map, not prescription. Errors are data.

## Files

| file | contents |
|---|---|
| `load_withheld.py` | `WithheldCase` dataclass: every field optional, unfilled = None, never dropped; JSON round trip; four seed cases, all PROPOSED |
| `estimate.py` | `withheld_estimate` (non-claimants and three separate bins) and `peak_vs_average` |
| `test_load_withheld.py` | stdlib unittest |
| `CLAIM_TABLE.md` | C1-C4, all PROPOSED, with the refutation protocol |
| `samples/` | seed cases as JSON and the estimator demo on constructed numbers |

## Schema

`case_id`, `date`, `region`, `shared_system`, `service_avoided`,
`skill_or_tool_used`, `peak_condition`, `withheld_by_choice`, `eligible`,
`reason_stated`, `scope_limit`, `fallback_if_fails`, `est_load_units`,
`est_method`, `status_tag`, `coupled_systems`, `notes`.

- Field meanings:
  - `peak_condition`: the condition under which the demand would arise, e.g. a cold morning or an outage.
  - `scope_limit`: what would trigger asking for help.
- `None` means UNKNOWN. It never means zero or False.
- `status_tag` is one of OBSERVED, DERIVED or PROPOSED.
- `est_load_units` is refused without `est_method`.
- There are no fields for names or personal identifiers.

## Estimation

- `non_claimants = eligible_population - claimants`.
- Three bins are kept separate. They are never merged and never summed into one figure:
  - `barrier_non_take_up`;
  - `unaware`;
  - `deliberate_withholding`.
- A bin holds a directly reported count, or None (UNKNOWN).
- `deliberate_withholding` is None unless it is directly reported.
- The part of `non_claimants` that no bin accounts for is `unattributed`:
  - it is computed only when all three bins are reported;
  - it is assigned to no bin.
- Peak and average load are reported separately. Rows with unknown peak status are counted apart.

## Seed cases (PROPOSED, generic, no personal identifiers)

1. Frozen trailer landing gear at −40. The driver carries their own mallet and torch, and the shared yard torches are saturated at peak.
2. Minor hand injury. It is treated in place within scope, with self-transport if that fails. No ambulance is called.
3. Eligible for public benefits, adapted, does not claim.
4. Paper map and paper logs carried. A GPS or ELD outage adds no load to the support line.

## Commands

```
python3 test_load_withheld.py
python3 load_withheld.py            # seed cases as JSON
python3 load_withheld.py FILE.json  # load and validate a case file
python3 estimate.py                 # demo on constructed numbers
```

## Related

- `uninstrumented/` (exclusions built into the apparatus)
- `configuration-record/` (frame exit, physical layer)
- `reasoning-toolkit/` card 16 (critical-facility cloud dependency audit)
