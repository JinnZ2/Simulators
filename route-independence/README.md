# route-independence

Three instruments and four research designs from the FABLE WORK ORDER
PACKET of 2026-09-26 (`WORK_ORDER.md`, verbatim). Instruments, not
arguments: each reports what was found, its scope, and what stayed
UNKNOWN. None returns a verdict on a study, a population, a route or a
decision.

CC0. Python 3 standard library only. No network at runtime. Parses under
3.9. Phone-buildable. Addressed to `JinnZ2/route-independence`, which
could not be created from this session (`SOURCES.md`); lands here as a
promotable folder that imports nothing across its boundary except one
optional prior-art cross-check.

```
python3 entry_condition_match.py demo/universe25_study.txt demo/population_c_paid_provision.txt
python3 entry_condition_match.py demo/universe25_study.txt demo/population_fail_gradient.txt   # refused
python3 route_independence.py    demo/routes.txt
python3 untried_options_audit.py demo/records/*.txt
python3 test_route.py                      # prints the check count
python3 <instrument>.py --choices          # every [CHOICE n] the order left open
```

## Status per item

```
FWO-1  entry_condition_match.py   BUILT    no prior instrument (RIN_001)
FWO-2  route_independence.py      BUILT    prior instrument found and IMPORTED as a
                                           cross-check, not a STOP (RIN_007)
FWO-3  untried_options_audit.py   BUILT    here, not method-layer (RIN_011)
FWO-4  RESEARCH_DESIGNS.md        DESIGN_WRITTEN; prior-art NOT_RUN vs literature
```

## FWO-1 — entry conditions before transfer

```
study.txt  ─┐    row by row              overall
            ├─►  MATCH                   TRANSFERABLE      every row MATCH
population ─┘    MISMATCH                PARTIAL           hold=[…] fail=[…]
                 UNKNOWN(reason)         NOT_TRANSFERABLE  no row MATCH
                                         NOT_EVALUABLE     load-bearing UNKNOWN
```

States are `DECOUPLED | COUPLED | REMOVED | PRESENT | UNKNOWN`, and the
first two are binary by definition (OBSERVED, carried): a gradient word
is refused at the parser as `INVALID_STATE`. `dwellings_held > 1` on a
row derives DECOUPLED. A row with no source prints SYNTHETIC.

Demo, expected structure stated before the run and met:

```
(a) effort-coupled            PARTIAL   hold=[predation]  fail=[7 rows]
(b) short on food/water/heat  NOT_EVALUABLE (waste_removal UNKNOWN); per-row MISMATCH on provision
(c) paid provision, dwellings PARTIAL   hold=[food water shelter thermal predation waste_removal]
                                        fail=[disease exit]      -- never TRANSFERABLE
(fail) gradient state         INVALID_STATE, not evaluated
```

Every study row is CARRIED from the order's transcription of Calhoun
1973; the paper was not read (host refused). Whether (c) is a partial
match or whether no human population meets the full condition is OPEN
and not resolved in code.

## FWO-2 — routes, and whether each settles in its own medium

```
per route   settles_in == obligation_medium AND not the dominant token
            -> discharges_own_obligations  True | False | None(UNKNOWN)
per need    route_count · independent_count (point or [min,max]) · ratio
flag        ENCLOSED_PLURALITY | NOT_ENCLOSED | SINGLE_ROUTE | UNKNOWN | NOT_EVALUABLE
```

`permitted` is a separate column carried to the output and reaching no
measure (checked behaviourally and over the AST): a route can be
permitted and still unable to discharge its obligations in its own
medium, which is the error the instrument exists to catch. Demo: `water`
reads ENCLOSED_PLURALITY; `food` reads UNKNOWN because the gift/mutual-aid
obligation medium is unsourced here, so its enclosure is not established
by this run; a constructed labour-hours commons reaches NOT_ENCLOSED.
`effective-redundancy-audit`'s N_eff is imported as a cross-check and
agrees on every decided need.

## FWO-3 — were the options enumerated, and was cost bound to the decider

```
C1  first_cost_bearers includes proposer      YES | NO | UNKNOWN | ABSENT_FIELD
C2  authorizer_prior_exposure recorded        YES | NO | UNKNOWN | ABSENT_FIELD
C3  options_not_tried present and non-empty   YES | NO | ABSENT_FIELD
C4  independent reviewer, may add options     YES | NO | UNKNOWN | ABSENT_FIELD
C5  reviewer-added option not already listed  RETURN_FOR_REDO(list) | ALL_ALREADY_LISTED
                                              | NONE_ADDED | UNKNOWN | ABSENT_FIELD
```

`ABSENT_FIELD` (no slot in the record) is kept apart from `NO` (slot
present, empty) on every check. Six read records are coded in
`demo/records/` with line citations (PEP 572, the Rust RFC template, the
MADR template, the OpenAI Model Spec, and two in-tree documents), plus
two constructed ones that reach `NO` and `RETURN_FOR_REDO`.

Three option fields, kept apart, because the council's structure keeps
them apart: `options_tried` (attempted in the world, consequences
recorded, C3a), `options_not_tried` (still available; a third party
could require one be tried first, C3), and `options_considered`
(evaluated and rejected on argument, never tried, C3c). The first coding
here mapped rejected-alternatives sections onto C3, which overstated it;
the operator's reading corrected that (RIN_021).

The finding, as recoded: engineering record types carry a
considered-and-rejected slot (PEP `Rejected alternative proposals`, Rust
`Rationale and alternatives`, MADR `Considered Options`: 3 of 6 read
records on C3c). The council's untried-and-available slot is on 1 of 6,
the in-tree DECISION entry. No coded type carries a slot for options
tried in the world (C3a ABSENT_FIELD, 6 of 6), a slot binding first cost
to the proposer (C1, 6 of 6), or the authorizer's prior exposure (C2,
6 of 6). **No read record gives an independent reviewer authority to add
options** (C4 YES on 0 of 6; PEP 572 reads NO on PEP 1's stated
approve-or-reject authority) and RETURN_FOR_REDO fires on none (C5). Both
AI documents read ABSENT_FIELD on C3 and C3c, which is consistent with
the order's PROPOSED reading and does not establish it at n = 2.

The structure's source line is carried verbatim in the module docstring.
No name is attached.

## FWO-4 — research designs

`RESEARCH_DESIGNS.md`: R-1 time vs money (within-person form A → B
shift), R-2 token-trading vs forage-only troops (two channels kept
apart; non-use never scored as incapacity), R-3 divergence with
intermittent contact (three contact regimes; tentative by design), R-4
condition matching in the Calhoun-citing literature (FWO-1 as the coding
instrument). Each carries scope, a kill condition and a cheapest first
run. Literature prior-art checks are NOT_RUN; in-tree adjacency is
recorded per design.

## Merge audit (RIN_020 corrected, RIN_022..RIN_024)

The operator asked for the parent diff of the merge that cut the registry.
Run over the whole history instead, with a standing instrument:

```
python3 tools/merge_silent_loss.py 57b9cdf dbf4cb0 7cf18f4     # the three registry cuts
python3 tools/merge_silent_loss.py --all                        # every merge reachable from HEAD
python3 tools/merge_silent_loss.py --selftest                   # constructed history, every state
```

Sample in `samples/merge_loss.sample.txt`. What it reads: 113 merges, 9 with
a line a parent held that the merge dropped and the other parent had not
deleted. The registry was cut three times (2026-09-09, 09-18, 09-19) and
restored three times, because it is the one file that counts itself. Seven
other files lost lines that are still absent at HEAD and carry no instrument;
one folder (`substrate-alternative/`) is two builds under one name, with the
discarded build's test left in place and crashing. The first run of the
instrument reported 1,400 phantom lines from a shallow clone, and now refuses
instead. Details in the claim table.

## What stayed UNKNOWN, and why

- Every Universe 25 row: the 1973 paper was not readable here.
- The gift/mutual-aid obligation medium: unsourced at mutual-aid scale.
- Which alternatives in PEP 572 came from third parties (C5).
- Reviewer authority on four of six read records (C4).
- The four designs' standing against their literatures.

Claims `RIN_001..019` in `CLAIM_TABLE.md`; fetch and refusal record in
`SOURCES.md`. Check count printed by `python3 route-independence/test_route.py`;
the instruments refuse `--selftest` and name that file.
