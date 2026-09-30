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


---

# Order of 2026-09-27 — dependency chains, conversion points, single-medium detectability

`WORK_ORDER_2026-09-27.md`, verbatim. Extends FWO-2 and rebuilds none of
it. Claims `RIN_025..038` in `CLAIM_TABLE.md` (first drafted as
`RIN_021..034`; renumbered before push, since the packet had used those
ids at `5b2c0f0`/`0a182ed` after this order was written against `177d885`).

```
python3 test_dependency_chain.py        checks; prints its count
python3 dependency_chain_audit.py       three demo cases + the FWO-6 register tally
python3 dependency_chain_audit.py --choices
```

## STATE, before any number

```
execution   the session that wrote this order's files had NO SHELL when it wrote
            them; they were pushed through the GitHub API at 5159ba4 unexecuted.
            A later turn of the same session regained a shell and ran the test
            once on this branch before the claim table was pushed:
            dependency-chain: 128 checks, 0 failed.  Every prediction registered
            in EXPECTED before that run HELD; none was edited after it (RIN_038).
FWO-2       PRESENT on this branch and REUSED: flags, bands, ratio and the
            prior-art cross-check are route_independence.py's; the test asserts
            by AST that nothing of it is redefined.  test_route.py stays green
            under the wrapper (122 checks, 0 failed).
samples/    dependency_chain.sample.txt is the recorded render of that run.
```

## FWO-5 -- `dependency_chain_audit.py`  (BUILT, RUN)

One produced result, every dependency needed to produce it, and for each
whether ANY route discharges its own obligations in its own medium. Each
dependency is one FWO-2 need; a route is one FWO-2 row plus this order's
fields.

```
result --> dependency (10 categories) --> routes
   route   medium_of_account (= settles_in) / medium_of_settlement (= obligation_medium)
           status DERIVED from FWO-2's discharges_own_obligations:
             None -> UNKNOWN ; True -> INDEPENDENT ; False -> CONVERTED (+ converted_into)
           conversion_point   required on CONVERTED, refused elsewhere; closed vocabulary
           source             required, typed CONSTRUCTED | CARRIED | VERIFIED | READ
           permitted          recorded in FWO-2's yes|no|UNKNOWN and read by nothing
   dependency  NOT_NEEDED with a reason, or routes; silence is refused
               flag = FWO-2's ; independent band ; converted_count ; unknown_count ;
               cross-check = effective_redundancy n_eff via FWO-2, or PRIOR_ART_NOT_IMPORTED
   result  independence band [lo, hi] over dependencies with routes
             lo = dependencies certainly carrying an independent route
             hi = dependencies possibly carrying one (an UNKNOWN route counts at the top)
             None when nothing is routed
           conversion points ordered by DISTINCT DEPENDENCIES routing through each
           absent_field (category not in the map) apart from not_needed (declared)
```

**Prior art, checked first.** In-tree: FWO-2 itself, and through it
`effective-redundancy-audit`'s `Case.n_eff`; `labor-instrument/labor_schema.py`
refuses exposure conversion across classes (the same refusal one field
over, cited not imported); `substrate-alternative/frame_audit.py` locates
money-frame tokens in prose and is a different instrument. Out-of-tree
(life-cycle inventory, bill-of-materials, full economic costing of
research, open-hardware infrastructure, Ostrom-lineage commons):
NOT_RUN, no host reachable. The ten categories are the order's minimum,
unextended for want of a read alternative.

**Two readings the order leaves open, taken as choices.** `[CHOICE 2]` a
route is read at ONE hop, the obligation the producer incurs to obtain
the dependency; tracing every route to its root makes every route
CONVERTED by construction and the instrument cannot fail, which is what
case (a) tests. `[CHOICE 3]` a route with no obligation is INDEPENDENT,
which is FWO-2's own rule applied to the medium `none`. Seven choices in
all, printed by `--choices`.

**Demo, expectations REGISTERED in `EXPECTED` before the first run**
(predictions computed by hand; the RUN column is the recorded render):

| case | source | predicted | run |
|---|---|---|---|
| (a) household phenology | CONSTRUCTED; property tax CARRIED | band [6/8, 7/8]; publication the possibly-independent row; legal_compliance CONVERTED at `tax`; two NOT_NEEDED; nothing enclosed; 3 of 3 MATCH | [0.750, 0.875]; `['publication']`; `tax=1`; 3 of 3 MATCH — HELD |
| (b) open-access finding | structure CARRIED; instance named (Kalai et al., Nature 653, 2026), NOT READ | 2/10, a point; ENCLOSED on instrument and labor; **publication NOT enclosed** (preprint deposit, no obligation at one hop) and data_access independent through an open dataset settling in citation, so the order's `enclosed_on_publication` reads MISMATCH | 0.200; `['instrument', 'labor']`; independent `['data_access', 'publication']`; MISMATCH on that one expectation, as predicted — HELD |
| (c) bitcoin exit | CONSTRUCTED; IRS Notice 2014-21 CARRIED | band [4/8, 6/8]; ledger INDEPENDENT at account level; legal_compliance ENCLOSED at `settlement`; 2 of 2 MATCH; `input_purchase` leads the ordered conversion points 3 to 1 | [0.500, 0.750]; `['legal_compliance']`; `input_purchase=3, settlement=1`; 2 of 2 MATCH — HELD |

One thing wrapping FWO-2 surfaced about FWO-2 (`RIN_028`): its flag order
tests a single route before the band, so a dependency whose one route is
UNKNOWN reads `SINGLE_ROUTE`; the wrapper prints `unknown_count` and the
band beside the flag (case (a) publication, case (c) credential, both
`SINGLE_ROUTE  0..1  unk 1` in the sample). Left as found.

## FWO-6 -- `conversion_register.json`  (BUILT as data, tally RUN)

Eight exit attempts, every source CARRIED or UNKNOWN, no entry rated.
`register_tally()` counts distinct entries per mechanism and per layer.
Hypothesis registered in the order before any tally (PROPOSED, Claude):
conversion points cluster at SETTLEMENT. **Predicted as coded, and
returned by the run:** production 6 / settlement 4 / legal 1 /
publication 1, four entries with an UNKNOWN mechanism apart; `SPREAD`,
hypothesis `NOT_SUPPORTED_ON_THIS_REGISTER`. Coded by the party that
proposed the hypothesis, and running against it; `input_purchase` on six
of eight is the production-layer conversion the order's candidate list
names only by implication, and the same lead appears in FWO-5 case (c).
Prior art NOT_RUN.

## FWO-7 -- `FWO7_DESIGN.md`  (DESIGN_WRITTEN)

Three control sources for a defect with no control world: historical
parallel media; contemporaneous non-settling populations;
divergence-then-contact. Each with scope, prediction, kill condition,
cheapest first run and its own confound. Nothing run; prior art NOT_RUN.

## Carried from the 2026-09-26 audit

Answered against `177d885`; the packet moved under the build (`5b2c0f0`,
`0a182ed`) and answered items 1-3 itself in `RIN_021`/`RIN_022`. Both
readings are recorded; nothing of this order's was edited to agree.

```
1  57b9cdf merge loss   API stats read TWO files; the diff, read once a shell existed, shows
                        run_manifest.py's two lines are a replacement, not a loss -- confined
                        to known_answer.py alone, as the packet's RIN_022 found first    RIN_034
2  options_not_tried    at 177d885, considered-and-rejected sat in options_not_tried and
                        options_tried was present-empty; 5b2c0f0 (RIN_021) added
                        options_considered / C3c and made those slots ABSENT_FIELD; what
                        stands is that no field marks whether a rejected option was TRIED   RIN_035
3  C5 authority         the one YES on C4 (PEP 572 line 676) was recoded to no by RIN_021;
                        the field name still conflates propose with compel                 RIN_036
4  C / NC tallies       partial, from search fragments of a repository outside scope   RIN_037
```

## Files added by this order

```
WORK_ORDER_2026-09-27.md            verbatim
dependency_chain_audit.py           FWO-5
test_dependency_chain.py            checks; prints its count
conversion_register.json            FWO-6 data
FWO7_DESIGN.md                      FWO-7
samples/dependency_chain.sample.txt the recorded first render
CLAIM_TABLE.md                      RIN_025..038 appended
SOURCES.md                          a section appended; nothing fetched
```

# Order of 2026-09-27b — single-channel additions (FWO-8 .. FWO-14)

`WORK_ORDER_2026-09-27b.md` verbatim. Six instruments and one design, extending
FWO-5 and FWO-6 and rebuilding neither. `EXPECTED_2026-09-27b.md` was committed
at `fd198aa` before any module, fixture or annotation of this order existed;
`CLAIM_TABLE.md` RIN_039..057 score every registered expectation against it.

```
STATE   built and run; every render recorded under samples/
        key-holder rules: 1 met everywhere (fd198aa); 3 met everywhere (6 of 6
        fail fixtures); 2 met only on FWO-13 rows 1-2 -- every other input is
        the FWO-5 cases, this session's readings, or a recalled date, and each
        claim row says so.  Nothing here is a reader independent of the author.
```

| item | file | status | what it returns |
|---|---|---|---|
| FWO-8 edge taxonomy | `edge_taxonomy.py` | BUILT | the three FWO-5 cases under `edge_class` / `coupling_side`; two layer readings never merged; DIRECT 0 of 0 across the cases; the two-layer schema's unplaceable points per case |
| FWO-9 question space | `question_space.py` | BUILT | per conversion point (FWO-5's six + `tax_step`), the declared classes that stop being askable; UNKNOWN allowed; no loss estimated |
| FWO-10 standards register | `standards_register.py` | BUILT; verdict NOT_EVALUABLE | six rows CARRIED_FROM_MEMORY; applied column UNKNOWN_NOT_SEARCHED on every row; prior art NOT_RUN with the plumbing/medium reading declared |
| FWO-11 lag count | `lag_count.py` | BUILT | six seeds, every date UNSOURCED; sourced distribution empty, unsourced [550, 1506, 1921, 2297]; no seed INDEPENDENT |
| FWO-12 unpaid maintenance | `unpaid_maintenance.py` | DESIGN_WRITTEN | schema, filter, NOT_RUN share; prior art NOT_RUN; prediction NOT_RUN |
| FWO-13 tax step | `tax_step.py`, `tax_step_register.json` | BUILT | its own row type; 2 REGISTERED, 1 CANDIDATE; 4 of 8 FWO-6 entries carry a tax mechanism |
| FWO-14 reference instability | `REFERENCE_INSTABILITY_DESIGN.md` | DESIGN ONLY | row type, twelve CANDIDATE_UNSOURCED rows, the metrology comparison, G(t) at seven dates with three falsifiable directions |

Where a prediction failed, first: E8.4's row-level registration (`data_access`
alone) was REFUTED by the recorded FWO-5 render, exactly as the EXPECTED file
said it would be — case (b)'s independent rows are `data_access` and
`publication`. E10.1 and E12.1 are NOT_EVALUABLE, not held, because the
searches they need cannot run here. Every other expectation held under rules 1
and 3 with rule 2 unmet, which is the weakest kind of hold and is labelled so.

Carried audit questions: 1 and 2 are about a repository outside scope
(RIN_051, RIN_052 record what this tree does show — a second ESP-1 build on
`origin/claude/noise-information-four-tools-5u0l4k`); 3 is done (X6, first
run recorded before repair, STE_011); 4 is answered (RIN_043); 5 is done from
the losing-parent blobs (RIN_055); 6 is not resolved, by instruction.

Commands:

```
python3 route-independence/test_single_channel.py     # prints the count and the fail-fixture line
python3 route-independence/edge_taxonomy.py           # and each of the other five modules; --choices on each
```

# AMENDMENT A-1 of 2026-09-28 — settlement vs gate-removal

`AMENDMENT_A1_2026-09-28_settlement-vs-gate.md` verbatim; its section 5 is
the EXPECTED block and the file was committed alone at `bacaeab` before any
code. `settlement_split.py` extends FWO-5 and FWO-8 and rebuilds neither;
`test_settlement_split.py` prints its count. `CLAIM_TABLE.md` RIN_058..066.

```
STATE   built and run; render recorded under samples/
        key-holder rules: 1 met (bacaeab); 3 met (F-A3 as designated, and a
        constructed three-case fail fixture); 2 unmet everywhere -- every
        origin, split and token declaration is this session's reading.
        Two of three registered expectations FAILED and are reported first.
```

| expectation | result | where |
|---|---|---|
| E-A2 unamended FWO-5 forces a settlement reading on F-A3 | **REFUTED**: none/none reads INDEPENDENT, obligation `none`. The meld is real and sits on F-A1 / F-A2, which FWO-5 reads identically on every derived field | RIN_058 |
| E-A3 case (b) at two hops returns no INDEPENDENT | **REFUTED on the case**: the preprint deposit survives (token NONE); HELD on the citation route, which converts at hop 2 by the carried chain | RIN_059 |
| E-A1 majority CONSTRUCTED; 2 of 3 cases with zero BIOLOGICAL | HELD (1, 3) — 23 of 24 decided rows CONSTRUCTED; a 1, b 0, c 0; ten routes UNDECIDED because the vocabulary has no member for a route with no obligation off the biological list | RIN_060, RIN_061 |

What the split adds: `obligation_origin`, `settles_claim`, `removes_gate` on a
copy of every FWO-5 route, UNDECIDED unscorable, the two halves never combined
(AST-asserted); `token_type` / `converts_to` / `hops_to_monetary` with a
per-horizon reading where UNMEASURED hops never read INDEPENDENT (F-A4);
section 2's symmetry argument as `net_positions`, registered in
`tools/known_answer.py`. The one BOTH row in the corpus is the property tax
on the land one lives on — a placed claim standing on shelter — which is the
amendment's C2 as a record.

```
AMENDMENT_A1_2026-09-28_settlement-vs-gate.md   verbatim (EXPECTED at bacaeab)
settlement_split.py                             the instrument
test_settlement_split.py                        checks; prints its count
samples/settlement_split.sample.txt             the recorded render
```

# AMENDMENT A-2 of 2026-09-28 — gate state is time- and jurisdiction-indexed

`AMENDMENT_A2_2026-09-28_gate-state.md` verbatim; its section 5 is the
EXPECTED block and the file was committed alone at `251e12a` before any code.
`gate_state.py` extends FWO-5, FWO-8 and A-1 and rebuilds none of them;
`test_gate_state.py` prints its count. `CLAIM_TABLE.md` RIN_067..076.

```
STATE   built and run; render recorded under samples/
        key-holder rules: 1 met (251e12a); 3 met (F-W1 vs F-W2 unamended, as
        designated, plus a constructed all-OPEN set that enters no hold);
        2 met at grade S by the amendment's author -- every source CARRIED
        here unread, so every hold reads HELD(S) at most (section 7).
        One of five expectation rows is a MISMATCH and is reported first.
```

| expectation | result | where |
|---|---|---|
| E-A2-1 (literal) amended records differ on gate_state ALONE | **REFUTED**: five fields differ; only `gate_state` is a reading field, t is the index the prediction names, the instrument is a label | RIN_067 |
| E-A2-1 (reading) unamended code returns one record; the reading parts on gate_state alone | HELD(S) | RIN_067 |
| E-A2-2 F-G1 → F-G2 is one change event OPEN → DISCRETIONARY, not route absence | HELD(S): route count England 1 → 1 across 1788, closure count 1; derived events reconcile with declared 2 of 2 | RIN_068 |
| E-A2-3 no subsistence route OPEN in every sourced jurisdiction at 2026 | HELD(S), per jurisdiction: rainwater CO metered / TX open / UT unknown; gleaning England discretionary; shelter NOT_EVALUABLE | RIN_069 |
| E-A2-4 DISCRETIONARY is not OPEN; no expression reads it as independent | HELD (AST); the scan fired twice on the module's own assertions, which were split | RIN_071 |

What the fixtures showed about themselves: F-W3 is declared PROHIBITED and
reads UNKNOWN because W-2 carries no date, and F-W4 reads OPEN only at a
year precision taken from W-3's text — under the amendment's own 3a two of
six delivered rows over-assert their source (RIN_070). Section 3c: ten
UNDECIDED rows re-read, eight move to NONE on stated grounds, two stay for a
different reason, an undeclared medium (RIN_072). F-A3 is retired and kept,
tagged, reading UNKNOWN (RIN_074).

```
AMENDMENT_A2_2026-09-28_gate-state.md   verbatim (EXPECTED at 251e12a)
gate_state.py                           the instrument
test_gate_state.py                      checks; prints its count
samples/gate_state.sample.txt           the recorded render
```

# AMENDMENT A-2.1 of 2026-09-28 — source upgrades and fixture corrections

`AMENDMENT_A2.1_2026-09-28_source-upgrades.md` verbatim; its section 5 is the
EXPECTED block and the file was committed alone at `09774de` before any code.
`gate_state_a21.py` extends `gate_state.py` and rebuilds nothing: every row goes
through A-2's `gate()` with A-2.1's source table passed in, and A-2's four
expectations are re-run over the corrected rows. `CLAIM_TABLE.md` RIN_077..086.

```
STATE   built and run; render recorded under samples/
        key-holder rules: 1 met (09774de); 3 met (A-2's F-W3 row as written,
        CONFLICT beside the corrected Utah pair); 2 met at grade P by the
        amendment's author for W-1a / W-2a, CARRIED here unread.
        Both registered rows MATCH; one clause of E-A2.1-2 corrected (Utah
        moves None -> P, not S -> P).
```

| expectation | result | where |
|---|---|---|
| E-A2.1-1 rainwater at 2026: CO METERED_PERMISSION (P), UT by container size (P), TX UNKNOWN; OPEN nowhere sourced, reported UNMEASURED_OPEN | HELD(P) | RIN_077 |
| E-A2.1-2 E-A2-3 hold count unchanged; rainwater grade S → P for CO and UT | HELD(S): CO S → P; UT None → P (no in-force row under A-2) | RIN_078 |

What the corrections showed: a corrected from-state removes a direction — the
Colorado event goes from LOOSENING at S to UNKNOWN_DIRECTION at P (RIN_080);
the `condition` field is what separates BY_CONDITION from CONFLICT (RIN_081);
section 3's fields are carried PROPOSED and not built (RIN_082); section 4's
statutes are in the table and refused as gate sources (RIN_083). The A-2
module took additive parameters only and its sample moved by one note line
(RIN_084).

```
AMENDMENT_A2.1_2026-09-28_source-upgrades.md   verbatim (EXPECTED at 09774de)
gate_state_a21.py                               the instrument
test_gate_state_a21.py                          checks; prints its count
samples/gate_state_a21.sample.txt               the recorded render
```

# AMENDMENT A-3 of 2026-09-28 — thermal regulation: actuators, stacked gates, direction, condition index, cross-stock coupling

`AMENDMENT_A3_2026-09-28_thermal.md` verbatim; its section 6 is the EXPECTED
block and the file was committed alone at `87f83ce` before any code.
`thermal_gates.py` extends A-2 and A-2.1 by import: dates, in-force intervals,
gate states and the hold rule are A-2's, and A-2.1's PROPOSED `access_is_right`
/ `revocable_by` are built here. The unit is the ACTUATOR, and its state at
(jurisdiction, t, condition) is the ordered SERIES of its gates, never one
state. `CLAIM_TABLE.md` RIN_087..097.

```
actuator ---- gate(order 1) -- gate(order 2) -- ... -- gate(order n)
               same order number = alternatives; different orders = in series
stock A ---- coupling row ----> stock B      (the only route across stocks)
gate  = ACTUATOR fault        coupling SENSOR_CORRUPTED = SENSOR fault   (never merged)
direction: one input = one direction; DirectionPooled otherwise; AST-scanned (2e)
```

```
STATE   built and run; render recorded under samples/
        key-holder rules: 1 met (87f83ce); 3 met (two fail fixtures);
        2 UNMET on every row: T-1..T-9 named, not landed, grade K.
        Every expectation about the sourced set reads NOT_EVALUABLE on an
        empty set; the K-row reading is printed beside it, hold-ineligible.
```

| expectation | result | where |
|---|---|---|
| E-A3-1 (literal) F-T4 is a 4-gate series | **REFUTED**: 5 gates in 4 positions (the fuel position is purchase OR permit) | RIN_087 |
| E-A3-2a every external actuator carries >= 1 non-market gate | NOT_EVALUABLE; K: 6 of 50 cells gated, 44 UNSEARCHED, clothing RETAIN has no fixture; 2d and E-A3-2a's list part on METERED_TOKEN | RIN_089, RIN_090 |
| E-A3-3 HEAT_IN and HEAT_OUT instruments disjoint | NOT_EVALUABLE; K disjoint; market purchase would sit on both sides by definition (weakness unstated in the order) | RIN_091 |
| E-A3-4 residue holds BODY actuators only | NOT_EVALUABLE; K: huddling only, residue entered only by declaration | RIN_092 |
| E-A3-6 burn ban during a cold event | NOT_EVALUABLE, registered open | RIN_094 |
| E-A3-1 (reading) unamended collapses F-T4 and accepts pooled input; amended does neither | HELD (instrument) | RIN_088 |
| E-A3-5 F-T1 reaches WATER only via the coupling row | HELD (instrument) | RIN_093 |

Also recorded: the seed's BOTH is not a direction and would itself be a pooled
value (RIN_095); A-2.1's fields are built and filled on 0 of 14 rows, and
`revocable_by None` reads both "no office" and "not recorded" (RIN_096); locus
remapping moves no verdict (RIN_097).

```
AMENDMENT_A3_2026-09-28_thermal.md   verbatim (EXPECTED at 87f83ce)
thermal_gates.py                     the instrument
test_thermal_gates.py                checks; prints its count and 2 of 2 fail fixtures
samples/thermal_gates.sample.txt     the recorded render
```

## AMENDMENT A-3.1 of 2026-09-28 -- definitional repairs

The amendment is landed verbatim as
`AMENDMENT_A3.1_2026-09-28_definitional-repairs.md`; its section 8 is the
EXPECTED block and the file was committed ALONE at `beb0fc6` before
`repairs_a31.py` existed. The module edits none of A-1..A-3: it reads their
rows and functions by import and runs the eight sections over them.

```
STATE   built and run; render recorded under samples/
        key-holder rules: 1 met (beb0fc6); 3 met (two fail fixtures);
        2 unchanged: every thermal row is K, every source CARRIED.
```

| expectation | result | where |
|---|---|---|
| E-A3.1-1 (DECLARED_CHARITABLE reading) at least one mismatch besides E-A3-2a | **UNMET_UNFALSIFIED**: 0 others, and E-A3-2a is itself a mismatch, so P fails and F ("zero mismatches found") does not fire -- the prediction lands in its own gap | RIN_098 |
| E-A3.1-1 (LITERAL_ALL / DECLARED_LITERAL) | HELD (instrument): 10 / 2 mismatches besides E-A3-2a | RIN_099 |
| E-A3.1-2 section 4 changes the reading of at least one row | HELD (instrument) under both migration rules: 22 rows (EVIDENCE), 2 rows (SCHEMA_DEFAULT) | RIN_102 |

Section by section: one market set, and E-A3-2a's gap lands on the metered
utility (RIN_100); E-A3.1-2's P and F part on "reading" against "meaning", and
A-1 E-A1's two predicates part on 39 of 216 worlds (RIN_101); every field
migrated and every row whose meaning moved (RIN_103); the unit lint fails four
of five EXPECTED blocks including A-3.1's own (RIN_104); E-A3-3 over
non-market instruments (RIN_105); absence-bound falsifiers read
NOT_TESTABLE_AS_POSED, and under the EVIDENCE rule E-A2-3's gleaning leg does
too (RIN_106); coverage beside every hold and the execution record (RIN_107).

```
AMENDMENT_A3.1_2026-09-28_definitional-repairs.md   verbatim (EXPECTED at beb0fc6)
repairs_a31.py                     the instrument
test_repairs_a31.py                checks; prints its count and 2 of 2 fail fixtures
samples/repairs_a31.sample.txt     the recorded render
```

## AMENDMENTS A-4, A-5, A-6 of 2026-09-28 -- chains, termini, eligibility

Three amendments, each landed verbatim and committed alone before any code
(A-4 `e0083e6`, A-5 `488fe1a`, A-6 `f8f3135`), the A-3.1 complement check and
unit lint run before each commit. A-4 makes a route a CHAIN of steps whose
requirements resolve to termini (BODY / TOKEN / NOT_RECORDED / CYCLE), with
lawful_reach and physical_reach never merged. A-5 resolves each terminus
through its token hops and re-reads FWO-5's INDEPENDENT routes as possible
branches. A-6 gates the terminus count by eligibility: case sets, constructed
profiles, recognition as time-indexed events. Rows that do not hold first:

```
E-A4-1 (own steps)   UNMET_UNFALSIFIED  5 gates over 2 own steps; MATCH at 7 transitive
E-A5-1               MISMATCH under 4 of 5 readings; holds only LAWFUL_STRICT
E-A5-4 (with hops)   MISMATCH           0 of 12 reclassified; 1 of 12 declares a token
E-A4-2..5, E-A5-2/3, E-A6-1..4   NOT_EVALUABLE, K reading printed beside each
E-A4-5               holds on K, and the measure undercounts (FALSE chains cannot close)
```

Nothing is filled from memory: CS-R, CS-A and RA-1..RA-5 are unread (egress),
C-1 is a fragment, and the exists-vs-reachable gap stays NOT_EVALUABLE rather
than being copied from CS-G. Profiles are constructed; no real person is in the
folder. Claims `RIN_108..RIN_123`.

```
AMENDMENT_A4_2026-09-28_route-chains.md               verbatim (EXPECTED at e0083e6)
AMENDMENT_A5_2026-09-28_terminus-diversity.md         verbatim (EXPECTED at 488fe1a)
AMENDMENT_A6_2026-09-28_eligibility-recognition.md    verbatim (EXPECTED at f8f3135)
chains_a4.py / termini_a5.py / eligibility_a6.py      the instruments
test_chains_a456.py                  checks; prints its count and 3 of 3 fail fixtures
samples/{chains_a4,termini_a5,eligibility_a6}.sample.txt   recorded renders
```

## AMENDMENT A-6.1 of 2026-09-28 -- standing, imposed scarcity, consolidation

Landed verbatim and committed alone at `7729a07`, before any code. The text was
recovered from the chat transcript with entities decoded, not re-typed. The
boolean eligibility from A-6 becomes a (case_set, standing) pair:
MEMBER, ADMITTED_NOT_MEMBER, EXCLUDED or NOT_RECORDED. Standing then acts per
route, through min_standing. Allocation limits must name an external gate
(an IMPOSED_SCARCITY row); otherwise the route is flagged
SCARCITY_UNATTRIBUTED. Consolidation events and residence-presumption chains
are carried at the amendment's grades, and a missing link is named. The row
that does not hold comes first:

```
E-A6.1-2        NOT_EVALUABLE  band [0, 1] chains; links-only reads 1, absent-join reads 0 (F fires)
E-A6.1-1        MATCH          by construction: gap 1 with the G-T3 row, 0 without (band [0, 1])
E-A6.1-3        MATCH          over 1 aggregate ANCSA case; village corporations not enumerated
E-A6-3 REVISED  MATCH          1 evidence path, a lower bound over a TRUNCATED list; no falsifier
```

Fail fixture: A-6's boolean reads P-0 and P-ADMITTED identically, while 2a
separates EXCLUDED from ADMITTED_NOT_MEMBER. CE-1's two figures are never
pooled. Profiles, routes and the coupling row are constructed, and no person
is described. Claims `RIN_124..RIN_134`.

```
AMENDMENT_A6.1_2026-09-28_standing-scarcity-consolidation.md   verbatim (EXPECTED at 7729a07)
standing_a61.py                     the instrument (extends eligibility_a6.py by import)
test_standing_a61.py                checks; prints its count and 1 of 1 fail fixture
samples/standing_a61.sample.txt     recorded render
```

## Erratum to A-6.1, 2026-09-29

The operator's five items are landed verbatim as `ERRATUM_A6.1_2026-09-29.md` and
committed alone at `a2f6ec2`, before code, because item 1 changes a threshold.
`standing_a61.py` absorbs them. No prior module is edited.

- **E-A6-3 is NOT_EVALUABLE** (RIN_135, superseding RIN_131's MATCH). The
  erratum puts 25 CFR 83.11(b)(2) at >= 11 paths, >= 3 of them
  residence-presuming. Four paths were retrieved and one presumes residence.
  A list not declared complete is not scored under either threshold; the
  retrieved count is printed beside the status.
- **The status gate** [CHOICE 81]. A raw MATCH whose falsifier cases are not
  enumerated reads UNFALSIFIABLE_AS_RUN. A raw MATCH on any input below grade
  S reads CONSTRUCTED_PASS. So E-A6.1-3 reads UNFALSIFIABLE_AS_RUN and
  E-A6.1-1 reads CONSTRUCTED_PASS. No A-6.1 row reads MATCH.
- The same gate is applied read-only to A-1..A-5 (RIN_137): 9 of 17 prior
  MATCH rows read CONSTRUCTED_PASS.
- **Unit-lint attachment** [CHOICE 78]. An annotation belongs to the nearest
  count before it. The A-4 window rule credits "one" in "one route, ... >= 1
  (unit: routes)"; the new rule does not. Uncredited counts on the landed
  amendments do not move, and in A-6.1 two tokens trade places (RIN_138).
- **Open sourcing targets** (RIN_139):
  - the same-peoples/same-unit join (E-A6.1-2)
  - the A-3 statute text for G-T3 (E-A6.1-1)
  - S-4 and the individual ANCSA village corporations (E-A6.1-3)
  - the complete path list (E-A6-3)
