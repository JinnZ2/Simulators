# extraction-chain-join

Work order: joining the extraction-money-power-emissions chain. The pieces of
the chain are kept by separate custodians, and nobody has joined them end to
end. The order asks for **instruments and joined datasets, not verdicts**,
with one gap per small team. `WORK_ORDER.md` is that order, **reconstructed**
from the session summary because the original message was lost (`ECJ_001`).

Every record scored here is CONSTRUCTED. Jurisdictions are J1..J8, countries
C01.., firms E../A../H.., persons P.., legislators L... Nothing here is about
a real country, firm, person or register.

```text
chain (PROPOSED)                       instrument     unit            evidence
-------------------------------------  -------------  --------------  -------------
debt / reserve need -> extraction      g1_read, g6    country-year    CORRELATIONAL
extraction -> emissions                (records)      firm-year       DERIVED
emissions -> extracting firm           (records)      firm            OBSERVED_JOIN
extracting firm -> beneficial owner    g2 / g3 / g4   firm -> person  OBSERVED_JOIN
beneficial owner -> funding of leaders g5             person -> leg.  DERIVED
funding of leaders -> extraction policy g5            legislator      CORRELATIONAL
consumption-based correction           g7             country-year    DERIVED

  every reading:  branch + value + coverage(covered / total, unit)     result() refuses without it
  branches:       PATTERN_HOLDS  SCOPE_LIMITED  GAP  MISSED_VARIABLE   (the order's four)
                  NO_PATTERN  NOT_EVALUABLE                            (added, CHOICE 1)
  refused:        end-to-end effect | secrecy index as a chain weight | driven-by share
```

## What came out, on constructed worlds

| gap | reading |
|---|---|
| G1 | one world, three samples: dependent-only HOLDS, rest NO_PATTERN, pooled SCOPE_LIMITED; a price confound reads MISSED_VARIABLE with the column and PATTERN_HOLDS without it |
| G2 | traced + breaks = 1 for every firm; 7 breaks listed and counted; a 25% threshold traces five 20% holders to nobody under full compliance |
| G3 | country-level prior art exists (Zhang et al. 2020, investment-based accounting); parent-level targets put 7.4% of emissions in a shell's secrecy jurisdiction |
| G4 | the gap is computable from the record: 0.543 unattributable, 0.420 at secrecy breaks at cut 60, 0.074 at cut 80; an unflagged nominee makes it a lower bound |
| G5 | "predicts better" does not separate influence from selection (selection world HOLDS, influence world does not); a funding filter on who sits reads below chance among the seated |
| G6 | the reserve share of revenue is a band, and it reads lower where extraction answers the reserve need; a driven-by share is refused |
| G7 | a production plateau with consumption-based still rising; plateau years past the consumption lag cannot be read (GAP) |
| chain | 2 correlational arrows (inference of inference), the unit changes at all 5 joints; joined coverage 0.310 against an independence product of 0.242 when missingness travels together |

```text
joined coverage is read on unit records, never multiplied:

  link coverage     volume .92  emissions .89  owner .60  funding .61  policy .80
  independence product                                   0.242
  joined, coupled missingness (one secrecy flag)         0.310
```

## Run

```sh
python3 extraction-chain-join/chain_join.py            # render; sample in samples/
python3 extraction-chain-join/chain_join.py --choices  # the eleven declared choices
python3 extraction-chain-join/test_chain.py            # checks; prints its own count
```

`chain_join.py --selftest` refuses (exit 2) and names the test file. `ols` is
imported from `sim-span/three_column.py`, not copied. `coverage`,
`traced_fraction`, `consumption_based` and `reserve_share_band` are
registered in `tools/known_answer.py`. The render screens clean through
`sheet-structure-scan/no_severity` with no exemption.

## Not done, and why

| item | state |
|---|---|
| any custodian's records | not read; every reading is on constructed records (`ECJ_020`) |
| the original order's bytes | lost in compaction; carried from the summary (`ECJ_001`) |
| Davis & Caldeira's 23% | record verified, figure carried from press, used nowhere (`ECJ_017`) |
| the real China plateau's split | carried; G7's question, not answered here (`ECJ_019`) |
| selectorate theory | named by the order as an adjacent frame; not instrumented |
| candidates who never ran | the frame G5 needs and legislators cannot supply (`ECJ_014`) |

Claims are ECJ_001..ECJ_020 in `CLAIM_TABLE.md`; sources in `SOURCES.md`.
Stdlib only, parses under Python 3.8, CC0.
