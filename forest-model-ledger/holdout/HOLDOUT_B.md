<!-- SPDX-License-Identifier: CC0-1.0 -->
<!-- This file is dedicated to the public domain under CC0 1.0. -->

# HOLDOUT_B -- Phase B: predict + seal

```text
status      : SEALED, not revealed. Predictions PROPOSED; model runs and fits DERIVED.
authorship  : co-authored (Kavik + Claude); work order dated 2026-11-22
date (UTC)  : 2026-11-22
code        : holdout/phase_b.py   (python3 holdout/phase_b.py reprints every number below)
sealed file : holdout/predictions.json ; holdout/predictions_commitment.json
```

Every number in this record was rendered from `predictions.json`, which
`phase_b.py` computed. None was typed.

Predictions were computed by code from anchor studies; the model's own
training may contain the holdout literature. Recall-based numbers would
be exposed; none were used.

Holdout validation can only confirm branches someone later reached; it
cannot score true unavailability. (inherited weld 4)

B1 rests on declared assumption A1 (fertility to aridity mapping); a B1
miss is read against A1 first.

## Run header (DECLARE)

```text
model + version   : WITHHELD (a standing session rule bars a model identifier in
                    any pushed artifact; it is in the report to the owner)
training cutoff   : 2026-06, as stated to the session; not verified by it
session           : fresh session; received the work order text only
rule                                                         kept
read set only (anchor_studies.csv, run_9 anchor, folder
  code, CLAUDE.md method brief, ledger/toolkit/)              yes
no other file in holdout/ read or listed                     yes
no call to zenodo.org / datadryad.org / doi.org              yes
every predicted number from code, none from recall           yes
EXPOSED reads                                                none
```

Files opened, complete list: `CLAUDE.md`, `ledger/anchors/ANCHOR_run9.yaml`,
`model/base.py`, `model/l0_audit.py`, `ledger/toolkit/budget_closure.py`,
`ledger/toolkit/HELDOUT_FREEZE.md` (first 5 lines), `runs/run_9.py`,
`runs/run_9.md`, `runs/run_1.md`, `runs/run_2.md`, `tools/check_ledger.py`
(grep and run), `holdout/anchor_studies.csv`. Outside the folder: the
repository-root `CLAUDE.md` (loaded into the session by the harness, not by
choice) and the first 12 lines of root `SHAPE_SPEC.md` (for the CC0 header
form). Neither is in the read set; neither holds holdout data. OBSERVED.

## Hashes asserted

```text
anchor_ref                         origin/archive/anchor-run9 == 55c651b8f7228b4d28a21ad442bf817752e80d21; 3 pinned files match at that commit
anchor_studies.csv                 e2ea825c7bb1372dc2b9a2d1c46f1c2a14f78b466f0a7f382bacb0c129a29438
ledger/toolkit/budget_closure.py   796b76f69e069f082603c3ee4392d56a0261de3ef139fbe942f14a21ba05a456
model/base.py                      ebb656bbf9554f3a6ed08055a0787f1e3a4ab6c024006a11555aed45eaea4ec8
runs/run_9.py                      0bae61f9a04d989a2d58fd90a24290c8285d7f62f0de47b81d760d671765ef22
anchor rerun here (300 yr, seed 0): fires 80, N misclosure -5.062e-11, water -3.426e-13, PASS
anchor studies: 3707 rows, 155 studies (Author)
```

## Mapping (assumption M1)

```text
M1  PSF log ratio rr is read as the network-effect log ratio: ln(focal biomass on its own conditioned soil with the fungal pool intact / on the same soil with the fungal pool moved to fast litter). Run-1 analogue.
    status: ASSUMPTION, PROPOSED
    failure signature: Self-Other rows and Self-Sterilized rows give opposite moderator directions; M2 (self vs other-conditioned soil) is carried beside M1 for that reading
    limit: the model has one mutualist pool and no pathogen pool, so M1 cannot go negative except through b < 0 (B1)
    limit: the sterilised arm keeps fungal necromass as fast litter (a nutrient flush)
    limit: Response (aboveground / total biomass) is one pool here
M2  self vs other-conditioned soil; computed beside M1, never merged.
```

Experiment constants (hand-set, fitted to nothing): aff=2.5, bootstrap=2000, bootstrap_seed=20261122, cond_years=20, k_lig=0.03, lig=0.4, pot_v=0.3, seedling=0.5, seeds=[0, 1, 2, 3, 4].
Phase-2 length is the anchor-study median Phase2.time, 2.25 months, unless the branch varies it.

Anchor reading of the same experiment (the diff baseline):

```text
                 M1 mean (seed range)            M2 mean (seed range)
woody_T       +0.0052 (+0.0038 .. +0.0065)   -0.0942 (-0.1047 .. -0.0875)
nonwoody_G    +0.0000 (+0.0000 .. +0.0000)   +0.2426 (+0.2262 .. +0.2675)
```

## Branches

### B1 -- stress-gated coupling

```text
change          : b = aff*(0.6-0.8E), aff = 2.5 (aff*0.6 = run_9 b = 1.5 at E = 0); E = min(AI, 1)
model direction : negative   (M2: NOT RECORDED)
fit             : rr ~ AI
                  estimate -0.2378, 80% interval [-0.3342, -0.1271], direction negative, excludes zero: yes
                  rows 3707, studies 155, dropped 0; model and fit agree: yes
fit             : rr ~ MAP per 1000 mm
                  estimate -0.1164, 80% interval [-0.2236, -0.0118], direction negative, excludes zero: yes
                  rows 3707, studies 155, dropped 0; model and fit agree: yes
closure         : N pass (max |mis| 5.44e-13), water pass (max |mis| 7.33e-14), 225 sims audited, 0 not closed
                  C, P, energy: not checkable (VOID in the base model)
crowding        : NOT RECORDED
A1  fertility E maps onto aridity / water limitation: E = min(AI, 1); MAP is read as a second monotone proxy of E
    breaks -> model and fit disagree in sign on AI, or AI and MAP fits disagree with each other
A2  the benefit term is linear in E and changes sign inside 0..1 (written into the equation; run_1 flag: partly circular)
    breaks -> holdout rr vs AI is flat or curved with no sign change inside the sampled AI range
A3  aff is set so that b at E = 0 equals run_9's b
    breaks -> direction holds but the magnitude is off by a constant factor
A4  E changes only b; precipitation, deposition and decay stay at run_9 values
    breaks -> an aridity effect appears in sterilised-soil growth as well (not a coupling effect)
```

```text
E      b        M1 mean   M2 mean   M1 diff vs anchor
0.000  +1.500   +0.0052   -0.0942   +0.0000
0.125  +1.250   +0.0038   -0.0948   -0.0014
0.250  +1.000   +0.0023   -0.0953   -0.0029
0.375  +0.750   +0.0007   -0.0958   -0.0045
0.500  +0.500   -0.0010   -0.0963   -0.0062
0.625  +0.250   -0.0028   -0.0968   -0.0080
0.750  -0.000   -0.0047   -0.0972   -0.0100
0.875  -0.250   -0.0069   -0.0976   -0.0121
1.000  -0.500   -0.0092   -0.0980   -0.0144
b changes sign at E = 0.750 ; M1 changes sign at E = 0.427 ; M2 vs E: decreasing
```

### B2 -- lag / slow response

```text
change          : phase-2 duration T varied over [0.5, 1, 2, 3, 6, 12, 24, 36] months; nothing else
model direction : positive   (M2: NOT RECORDED)
fit             : |rr| ~ Phase2.time (months)
                  estimate +0.0019, 80% interval [-0.0040, +0.0076], direction positive, excludes zero: no
                  rows 3701, studies 154, dropped 6; model and fit agree: yes
closure         : N pass (max |mis| 5.15e-13), water pass (max |mis| 5.81e-14), 200 sims audited, 0 not closed
                  C, P, energy: not checkable (VOID in the base model)
crowding        : NOT RECORDED
A1  one model year = 12 Phase2.time units (months)
    breaks -> the modelled lag sits at a time scale the data never samples
A2  the response is read as |rr| under M1 at the end of phase 2
    breaks -> sign changes with duration cancel in the mean while |rr| moves
A3  the conditioned soil does not change with phase-2 duration (same phase 1 for all T)
    breaks -> long experiments differ from short ones in phase-1 method, not duration
A4  no fire in phase 2
    breaks -> none expected in pots; field rows with burns would break it
```

```text
months   M1 mean   M2 mean   M1 diff vs anchor
  0.5    +0.0008   -0.0203   -0.0044
  1.0    +0.0017   -0.0398   -0.0035
  2.0    +0.0045   -0.0855   -0.0007
  3.0    +0.0073   -0.1194   +0.0021
  6.0    +0.0181   -0.2152   +0.0129
 12.0    +0.0375   -0.3620   +0.0323
 24.0    +0.0558   -0.5736   +0.0506
 36.0    +0.0580   -0.7245   +0.0528
|M1| vs T: increasing ; |M2| vs T: increasing
```

### B3 -- instrument boundary

```text
change          : phase-2 boundary: neighbour count (3.0 -> 0) and soil volume (1 -> 0.3)
model direction : positive   (M2: unresolved (seeds disagree in sign))
fit             : rr Greenhouse minus Field
                  estimate -0.0104, 80% interval [-0.1289, +0.1155], direction negative, excludes zero: no
                  rows 3707, studies 155, dropped 0; model and fit agree: no
closure         : N pass (max |mis| 5.15e-13), water pass (max |mis| 5.81e-14), 100 sims audited, 0 not closed
                  C, P, energy: not checkable (VOID in the base model)
crowding        : NOT RECORDED
A1  greenhouse = focal plant alone in a pot holding POT_V of the plot's soil; field = whole plot with the grass neighbour at INIT
    breaks -> the greenhouse minus field difference tracks Phase2.grow (Alone / Competition) and not setting
A2  amounts scale with soil volume; half-saturations K, Kf, Wh are concentrations and scale with it; dep and P0 scale with pot area
    breaks -> neighbour part and volume part have opposite signs and the sum hides both
A3  the neighbour is the run_9 grass guild
    breaks -> woody neighbours in field rows change the competition term
A4  light ceiling KT is not rescaled for the pot
    breaks -> pot-bound plants hit a ceiling the model does not have
```

```text
cell                               M1 mean   M2 mean   M1 diff vs anchor
field (neighbours 3.0, volume 1)   +0.0045   -0.0951   -0.0007
greenhouse (alone, volume 0.3)     +0.0048   -0.0951   -0.0004
neighbours removed only            +0.0052   -0.0942   +0.0000
pot volume only                    +0.0030   -0.0992   -0.0022
greenhouse minus field: M1 +0.0003 (neighbour part +0.0007, volume part -0.0015) ; M2 -0.0001
```

### B4 -- slow-pool coupling

```text
change          : lignin pool Ll: 0.4 of tree mortality enters it, slow guild decays it at 0.03/yr
model direction : positive   (M2: negative)
fit             : rr Woody minus Nonwoody
                  estimate +0.1000, 80% interval [+0.0202, +0.1815], direction positive, excludes zero: yes
                  rows 3707, studies 155, dropped 0; model and fit agree: yes
closure         : N pass (max |mis| 5.51e-13), water pass (max |mis| 5.81e-14), 75 sims audited, 0 not closed
                  C, P, energy: not checkable (VOID in the base model)
crowding        : NOT RECORDED
A1  Woody = the tree guild T (pays fungi, slow litter); Nonwoody = the grass guild G (no fungal partner, fast litter)
    breaks -> nonwoody rows with strong mycorrhizal response; the difference then reads as partner presence, not litter
A2  a fraction LIG of tree mortality is lignin; a slow guild decays it at K_LIG per yr at full moisture; the pool does not burn
    breaks -> the woody reading moves with fire frequency instead of with the pool
A3  grass litter carries no lignin
    breaks -> nonwoody reading unchanged by the branch (holds by construction here)
A4  COND_YEARS of conditioning is long enough for the slow pool to matter
    breaks -> the branch reading equals the anchor reading within seed range
```

```text
                 M1 mean   M2 mean   M1 diff vs anchor
woody_T          +0.0033   -0.0981   -0.0020
nonwoody_G       +0.0000   +0.2462   +0.0000
woody minus nonwoody: M1 +0.0033 (anchor +0.0052) ; M2 -0.3443 (anchor -0.3369)
extended table with lig = 0 returns the anchor M1 to within 0.0e+00 ; base module restored: yes
```

### R5 -- REFERENCE: enemy release

```text
change          : none; fit only, not a branch
tag             : dense reference, no run_9 mechanism
model direction : NOT RECORDED (no model run; enemy release is not in run_9)   (M2: NOT RECORDED)
fit             : rr Non-native minus Native
                  estimate +0.1375, 80% interval [+0.0438, +0.2389], direction positive, excludes zero: yes
                  rows 3707, studies 155, dropped 0; model and fit agree: not applicable
closure         : not checkable (no model run)
crowding        : NOT RECORDED
A1  no mechanism; a moderator fit on anchor studies only
    breaks -> not applicable
```

## Read (found / scope / unresolved)

```text
found
- Every simulate() call in every branch closed N and water at numerical
  tolerance. C, P and energy are VOID in the base model: not checkable.
- B1: model and fit agree (negative) on AI and on MAP; both fit intervals
  exclude zero. The sign of b is written into the equation (run_1 flag:
  partly circular), so the agreement tests A1, not the mechanism.
- B1 surprise: M1 changes sign well below the E where b does. The sterilised
  arm keeps fungal necromass as fast litter, and that flush offsets part of
  the mutualist benefit. A property of M1, not of the branch.
- B2: |M1| and |M2| both rise with duration in the model. The fit is positive
  and its interval includes zero.
- B3: the model difference is smaller than the seed range of either cell;
  every seed gives the same M1 sign, M2 seeds disagree. The neighbour part
  and the volume part have opposite signs (failure signature B3-A2). Model
  and fit disagree in sign; the fit interval includes zero.
- B4: under M1 the nonwoody reading is exactly zero because the grass guild
  has no fungal partner (A1, by construction), so the positive woody minus
  nonwoody direction is the anchor structure. The lignin pool itself moved
  the woody reading DOWN. M2 gives the opposite sign to M1.
- All M1 model magnitudes are about two orders below the fitted effects.
  Directions are sealed; model magnitudes are not predictions.
scope
- one hand-set parameter point; 5 fire seeds; N and water only; synthetic model
- the interval is the anchor-study estimate's 80% cluster-bootstrap interval;
  it is not widened for the holdout's own sampling error (its size was not read)
- sealed direction and interval = the anchor-study fit; model direction sits
  beside it, never merged. The order does not say which of the two "direction"
  means; both are sealed so the reveal can score either.
unresolved
- B3 model direction (inside seed range) ; B4 M1 against M2
- crowding for B1-B4: NOT RECORDED (below)
- toolbox: B3 (a change that moves nearly nothing) and B4 (a direction that
  holds by construction) match toolbox triggers. The full toolbox was NOT run
  in this order; that is owed before either branch reads as "holds".
```

## Crowding (step 3)

```text
B1  NOT RECORDED    B2  NOT RECORDED    B3  NOT RECORDED    B4  NOT RECORDED
answers verbatim : none; no probe was run
crowding_basis   : probe not run: no tool-less fresh chat was available to this session; a sub-agent given only the question keeps file and network access to the repository, including the holdout files this run may not read
```

A probe run after sealing (including cross-family probes by the owner) goes
in its own dated record, never into predictions.json.

## Commitment (step 4)

```text
scheme             : sha256(nonce_B || predictions.json bytes), nonce_B = 32 random bytes, not committed
commitment         : f5dcc443d5afb4144ea0836015d0694c6796b723aa6d3c34e0bb00d7f7bcc65d
predictions sha256 : 24477fdf93936f76e2475d337da033f6e304e17ca69203e4daebabfca48a9f26
predictions bytes  : 33257
nonce_B            : not committed; reported once to the owner
```

predictions.json holds no holdout data; the seal fixes it before reveal, it
is not secret. Re-running `phase_b.py --seal` would draw a new nonce and
overwrite the commitment: do not re-seal.

Observer slots: null.

## Provenance

```text
OBSERVED  hashes asserted; files opened; rules kept; closures; no probe run
DERIVED   every model reading and every fit (python3 holdout/phase_b.py)
PROPOSED  mapping M1; assumptions A1..An per branch; all sealed predictions
NOT RECORDED  crowding B1-B4; model identifier (WITHHELD in this file)
anchor    run_9, candidate, commit 55c651b8f7228b4d28a21ad442bf817752e80d21
base      branch claude/forest-holdout-phase-a
```
