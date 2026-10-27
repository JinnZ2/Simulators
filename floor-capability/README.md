# floor-capability

FLOOR CAPABILITY SITE ASSESSMENT, co-authored draft v0, landed as delivered
(`DRAFT_V0.txt`, sha256-pinned) and instrumented. The draft is a PROPOSED
instrument. It lists six capability indicators that a standard
site-selection sheet does not count, a `hidden_cost` sum, and three unrun
analyses.

Every record scored here is CONSTRUCTED. Nothing in this folder describes a
plant, a workforce, or any country's workers.

```text
DRAFT_V0.txt --(ast, pin)--> read_draft --> audit           what the draft states, computed
     |
     |   indicator           made measurable as            refuses / keeps apart
     |   ------------------  ----------------------------  ------------------------------------
     +-- scrap               classify_event (event level)  UNMAPPED, UNDETERMINED, FASTER_THAN_CHECK
     +-- tenure x scrap      tenure_test (+ control)       NOT_SEPARABLE when both rates fall
     +-- maintenance         task_class per class          TRANSFERRED / NEW_TASK / CAPACITY
     +-- part turnover       life_ratio                    None without a declared basis
     +-- worker tenure       handoff_overlap (signed)      NO_SUCCESSOR, UNKNOWN
     +-- hr screening        screening_share               NOT_RECORDED never read as credential-only
     +-- safety direction    rule_origin                   BOTH, NEITHER, UNKNOWN
     +-- hidden_cost         cost_vector                   the scalar sum (combine refuses)
```

## What the draft states, computed

| quantity | value |
|---|---|
| indicators | 6 |
| numeric constants anywhere in the draft | 0 |
| weights | named in the status line, carried nowhere: UNSTATED, not unrun |
| hidden_cost terms | 5; 1 named as an indicator, 1 with no indicator, 0 bound to a cost unit |
| overlaps a scalar sum counts twice | 3, one of them named by the draft's own scrap codes |
| reclassify map | code level, 3 codes; the draft's second gap asks for the event separation it skips |

## The shape of the main finding

```text
draft:       scrap code  --map-->  "missing human catch"     every event of the code
event level: scrap event --precursor? lead >= 2 x check?-->  CATCHABLE | FASTER_THAN_CHECK
                                                              | EQUIPMENT_ONLY | UNDETERMINED
             share over ALL scrap:  code level 0.750  vs  event level [0.300, 0.450]   (40 constructed)
             code level is an upper bound by construction (200 seeded sets, no exception)
```

Tenure against scrap, with equipment-only scrap as the control:

```text
world       catchable slope   equipment slope   verdict            seeds
operator    falls             flat              OPERATOR_CHANNEL   10 of 10
assignment  falls             falls             NOT_SEPARABLE      10 of 10   newer operators, older machines
null        flat              flat              NO_EFFECT           9 of 10   one miss = the 95% band
```

Without the control, the operator and assignment worlds look the same.

## Run

```sh
python3 floor-capability/floor_capability.py            # render, sample in samples/
python3 floor-capability/floor_capability.py --choices  # the five declared choices
python3 floor-capability/test_floor.py                  # checks; prints its own count
```

`floor_capability.py --selftest` refuses (exit 2) and names the test file.
`ols` is imported from `sim-span/three_column.py` and `attribution` from
`measurand-partition/common.py`; neither is copied. `life_ratio`,
`catchable_share_low` and `handoff_overlap` are registered in
`tools/known_answer.py`. The render screens clean through
`sheet-structure-scan/no_severity` with no exemption.

## Not done, and why

| item | state |
|---|---|
| plant data | none; every result is on constructed records (FLC_016) |
| weights | the draft carries none; nothing here invents them |
| three-country floor comparison | carried verbatim, not quantified; no function takes a country |
| a public tenure-to-scrap-code dataset | the draft states an absence with no corpus or search terms; UNBOUNDED |

Claims are FLC_001..FLC_017 in `CLAIM_TABLE.md`. Stdlib only, parses under
Python 3.8, CC0.
