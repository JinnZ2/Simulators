# CLAIM_TABLE — photoperiod-claim-harness

Seven claims, `PCH_001..007`, about the **harness**. **All repaired.**

Every repair is pinned by [`tests/test_repairs.py`](tests/test_repairs.py)
(29 tests), which asserted the broken behaviour when it was written and
asserts the fix now. The rule for what to fix was the delivered README:
**make the code do what the prose already says it does.** The harness carries its
own claim table (`C1..C5`) about a greenhouse result; that one is delivered
and is not restated here.

## REFUTATION_PROTOCOL

Claims here are about whether the harness can fail in the ways it says it
can, checked by running it.

The file landed **verbatim** and was audited in that state. It has since been
**repaired** — the `.py` is modified; `README.md` is not. Each claim keeps the
pre-repair evidence, because the finding is what the defect cost rather than
that a line changed, and `harness_audit.py` reproduces the pre-repair
predicate locally so the before/after stays computed rather than quoted.

The repairs follow the harness's own rule. Where a sim output changed
(`PCH_007`) it is registered as an `InstrumentEdit` and changes no mechanism.
Where a claim was wrong (`PCH_002`) **the claim was updated, not the sim.**

This folder has **no bench data**, and neither does the harness. Nothing
here is a statement about wheat, chlorophyll, or any published result. The
harness's own hypothesis block says the same thing about itself, which is
why it is worth auditing rather than arguing with.

A failed check updates the claim.

## Claims

| id | statement | status |
| --- | --- | --- |
| `PCH_001` | **`C1`'s predicate returns SUPPORTED when the sim produces nothing.** Zero signature cells gives `signature_spread = 0.0`, which passes `< 1.5`, and the `reads` line for TRUE is *"the reported metrics are diagnostic of real efficiency."* | REPAIRED |
| `PCH_002` | **`C1`'s own grid says something narrower and stronger than its `reads` line.** The signature appears in 58 cells spanning a 4.88× range of true energy-per-dry-gram, and **all 58 are below 1.0**. Non-diagnostic of magnitude, diagnostic of sign. | REPAIRED (claim updated, not sim) |
| `PCH_003` | **The `MechanismEdit` guard screens 2 of the 4 free-text fields it is given** — `reason` and `mechanism`. `basis` and `prediction` pass a forbidden reason unscreened, and they are the two fields that ask for justification. | REPAIRED |
| `PCH_004` | **`settle()` records a prediction and never adjudicates it**, and cannot tell whether the edit happened. `prediction_held` is set to `None` by construction, and `file_hash_before == file_hash_after` when nothing was edited. | REPAIRED |
| `PCH_005` | **The header's own usage example fails.** `run S2` passes a sim id to a command that looks up claim ids; `run_claim("S2")` raises an uncaught `StopIteration`. | REPAIRED |
| `PCH_006` | **The predicates are real and mostly deny.** Four of five come back REFUTED on the shipped run, including `C2`, which refutes its own stated hypothesis and explains the mechanism, then files the next candidate in `PENDING_EDITS` rather than retuning toward it. | SUPPORTED — unchanged |
| `PCH_007` | **Every number in the delivered README holds; one word does not.** `C3`'s dark-interval curve is negative throughout but **not monotone**, and every arm that breaks the ordering is one whose run ends mid-cycle. A cycle average instead of an endpoint makes it monotone — and changes no verdict. | REPAIRED |

---

## PCH_001 — a pass that an empty result set returns

```
predicate:  signature_spread < 1.5
spread   =  max/min over cells that reproduce the reported signature
         =  0.0 when there are no such cells

as shipped            cells=58  spread=4.8828  ->  REFUTED
no shade-avoidance    cells=0   spread=0.0000  ->  SUPPORTED
    signature_kWh_per_dry_min = None
    signature_kWh_per_dry_max = None
```

The second row is a run in which the sim reproduced the reported signature
**zero times**, and it returns the verdict whose `reads` line is *"the
reported metrics are diagnostic of real efficiency."* The `None` min and max
print on the line above it, so the contradiction appears in one output.

Not a modelling error — a predicate that cannot distinguish *tight spread*
from *no observations*. `../null-harness/` `CONSTANT_SILENT` one level up:
not a gate that never fires, but a **pass an empty result set returns**.

**The harness already has the branch to route it to.** `run_claim()` catches
a raising predicate and emits `UNDECIDED:`. One guard —
`if not sig_dry: raise ValueError("no signature cells")` — sends the empty
case there instead of to SUPPORTED.

**Falsifier:** a reading of `C1` under which an empty signature set genuinely
means the metrics are diagnostic. There is none: it means the sim cannot
produce the reported package at all, which is a third verdict, not either of
the two on offer.

**Evidence:** `harness_audit.py` §1.

---

## PCH_002 — the finding is narrower than the reads line, and better

```
signature cells                      58
kWh per dry gram, ratio to control   0.1439 .. 0.7027
cells with ratio >= 1.0              0
signature_no_dry_gain_cells          0
```

`S1`'s docstring names the cell it is hunting for:

> A cell where (a) is TRUE and (b) is FALSE is a configuration in which the
> whole reported package appears with no gain per unit photosynthate.

It finds none. Every one of the 58 cells that reproduces the signature also
improves energy per dry gram, and the whole range sits below 1.0.

So `C1`'s `reads` line for FALSE overstates by one word. It says the
signature is **NON-DIAGNOSTIC**. The grid shows it is non-diagnostic of
**magnitude** — a 4.9× range in the true ratio — and diagnostic of **sign**.
On this mechanism set the reported package does license *"cheaper per dry
gram"*; it does not license any particular number, and 68% is a number.

That is the stronger claim, because it survives the objection that the sim
was built to find nothing. It found the effect and still cannot size it.

**Falsifier:** a mechanism set in which signature cells straddle 1.0. The
harness's own `PENDING_EDITS` names one that might do it — tissue-age
distribution shifting wall density without changing the energy accounting.

**Evidence:** `harness_audit.py` §2.

---

## PCH_003, PCH_004 — the edit protocol

```
field        forbidden reason placed here
reason       refused
mechanism    refused
basis        ACCEPTED   <-- not screened
prediction   ACCEPTED   <-- not screened
```

`FORBIDDEN_REASONS` is checked against `reason + " " + mechanism`. The two
unscreened fields are the two that ask for justification, which is where a
motivated editor would put outcome reasoning. One-line fix: concatenate all
four.

```
after settle():
  prediction        'low duty is penalised further'
  observed          {'best_duty': 1.0}
  prediction_held   None        <- set by construction, never filled
  hash before       4a587a7ab5a7
  hash after        4a587a7ab5a7
  equal             True        <- nothing edited the file
```

Two gaps, one shape. A registered prediction can be settled with the
comparison never made, and the protocol cannot tell whether the edit it
gates actually happened — an edit registered, settled and never performed is
indistinguishable in the log from one carried out.

This is the declared-control-never-scored shape `../reasoning-gate/` hit and
repaired, where the fix was to refuse an empty observation and write a record
either way. The equivalents here: `settle(observed, held)` with `held`
required, and refusing to settle when the file hash has not moved.

**What the guard gets right:** it is a pre-registration gate, it fires at
construction rather than at settle time, and its refusal message names the
protocol. Refusing on a substring is crude, and it is a real deny branch,
which most such rules are not.

**Evidence:** `harness_audit.py` §3–§4.

---

## PCH_006 — what holds

```
C1   [REPORTED] REFUTED
C2   [PHYSICS ] REFUTED
C3   [PHYSICS ] REFUTED
C4   [PHYSICS ] REFUTED
C5   [PHYSICS ] SUPPORTED
```

Four of five deny on the shipped run, including two the file's own framing
would have preferred to support.

`C2` is the sharpest thing in the file. It states a **premise** from the
literature (angiosperms have POR only, no DPOR), then a **hypothesis** that
dark intervals could still help by recharging the Pchlide/POR/NADPH pool,
then refutes its own hypothesis — and the `reads` line for FALSE explains
*why* in mechanism terms: the FLU clamp acts on pool **size**, so a full pool
slows synthesis and draining it continuously maximises flux. Then it names
the next candidate (shade acclimation) and files it in `PENDING_EDITS`.

**`PENDING_EDITS` has no equivalent elsewhere in this repository.** Three
mechanisms, each with a basis and a prediction registered *before* any run,
all marked `UNRUN`. That is the alternative to quietly retuning a sim that
came out the wrong way, written down as a data structure.

Provenance is separated at the type level — `REPORTED`, `PHYSICS`, `SIM`,
`BENCH` — and the hypothesis block states that every number in it is `SIM`,
that a sim can show an artifact is **sufficient** to produce a signature and
not that it happened, and that the confidence and comfort readouts are
separate and are not filled in by the file.

`BENCH` is declared and no code path emits it. That is the honest state and
the file says so; the `protocol` command is the instructions for producing
one, which is more than most claim tables carry.

## Related

- `../null-harness/` — `PCH_001` is its invariant at the predicate level: a
  verdict an empty result set returns.
- `../reasoning-gate/` — `PCH_004` is the declared-control-never-scored
  shape, and `PCH_005` is the same class as its `D1` docstring defect.
- `../measurement-fork/` — `PCH_002` is a denominator result: the signature
  fixes the sign of `kWh per dry gram` and not its magnitude.
- `../criteria-drift/` — `CD_002`'s sign-vs-magnitude split, on a different
  substrate.


---

## PCH_007 — the README is right about the mechanism; the readout is not

Every stated number checks:

```
delivered README says                  stated     measured
grid cells                             75         75
cells reproducing the signature        58         58
spread of true kWh per dry gram        ~4.9x      4.8828
C1  C2  C3  C4                         REFUTED    REFUTED
C5                                     SUPPORTED  SUPPORTED
```

The one word that does not:

> **C3 REFUTED.** No crossover in this regime; dark is **monotonically
> worse** under C2's mechanism set.

```
block h  periods    endpoint       cycle-average
0.5      144.00     -2.40738       -2.38494
1.0       72.00     -2.43340       -2.39951
2.0       36.00     -2.50337       -2.44496
3.0       24.00     -2.59185       -2.50758
4.0       18.00     -2.68504       -2.57430
6.0       12.00     -2.88316       -2.72082
8.0        9.00     -3.08040       -2.87045
10.0       7.20     -2.77285       -3.00421   <- ends mid-cycle
12.0       6.00     -3.41745       -3.12255
16.0       4.50     -2.66973       -3.34152   <- ends mid-cycle
20.0       3.60     -2.98122       -3.53345   <- ends mid-cycle
24.0       3.00     -4.17996       -3.69939

endpoint curve monotone            False
cycle-average monotone             True
arms that break monotonicity       [10.0, 16.0]
arms that end mid-cycle            [10.0, 16.0, 20.0]
every breaking arm ends mid-cycle  True
```

`_pchlide_run` returns `Chl` at the **last integration step**. At `duty=0.5`
the period is `2 × dark_block`, so a 144 h run ends mid-cycle for the blocks
that do not divide it, and the endpoint lands at a different phase in each of
those arms. Reading the mean over the final complete period instead makes the
curve monotone.

Ending mid-cycle is **necessary and not sufficient** here — the 20 h arm ends
mid-cycle and happens not to break the ordering — so the diagnosis is a
containment, not an equality.

**It changes no verdict.** `C3`'s predicate looks for a **sign flip**, and both
curves are negative throughout, so `crossover_h` is `None` either way. What the
artifact costs is the ability to read the curve's **shape** as mechanism — which
is exactly what `C3`'s `reads` line offers when it says *"one process dominates
throughout."*

So the README's mechanism claim is correct and the shipped readout does not
show it. That direction is worth naming: the prose is ahead of the instrument,
not behind it.

Same class as `../aperiodic-order-sim-stack/` — a commensurability between the
sampling grid and the structure being measured — and the fix has the same
shape: read a quantity the grid cannot alias.

**Falsifier:** a cycle-averaged curve that is also non-monotone. Then the
wobble is mechanism, not sampling, and `C3`'s `reads` line for FALSE needs the
opposite correction.

**Evidence:** `harness_audit.py` §7.


---

## The repairs

One rule for all of them: **make the code do what the delivered README
already says it does.** Five of the seven were the prose being ahead of the
instrument; two were the instrument being ahead of the prose.

### `PCH_001` — a predicate that can fail

```
world                    cells    spread     pre-repair     now
as shipped               58       4.8828     REFUTED        REFUTED
no shade-avoidance       0        0.0000     SUPPORTED      UNDECIDED
```

`require(condition, why)` raises; `run_claim()` already caught a raising
predicate and recorded `UNDECIDED:`. C1's predicate now requires a non-empty
cell set first, so *"the sim cannot produce the reported package at all"*
lands on the third verdict instead of on the one that reads as confirmation.

The README's own extension rule is the invariant this restores: *"append to
`CLAIM_TABLE` with a predicate that can fail."*

### `PCH_002` — the claim was updated, not the sim

Which is what the protocol says to do. Two new fields carry the finding:

```
signature_sign_agreement = 1.0
signature_cells_below_1  = 58 of 58
```

`C1`'s `reads` line now separates **magnitude** from **sign** and names the
field, and adds an `UNDECIDED` line for the empty case. `signature_sign_-
agreement` is `None` when there is nothing to agree on, so it cannot be
misread as unanimity in that case.

### `PCH_003`, `PCH_004` — the edit protocol

The screen reads the concatenation of all four free-text fields.

```
settle without a verdict               refused
settle with a non-bool                 refused
settle an edit that did not happen     refused  (file hash unchanged)
abandon(reason)                        MECHANISM_EDIT_ABANDONED
```

`settle(observed, held)` requires `held` to be a bool, and refuses when the
file hash has not moved — settling an edit that never happened records it as
one. `abandon(reason)` is the path for an edit decided against, so the trail
is intact either way.

### `PCH_005` — the header

`run C2` with `sweep S2` labelled as a different registry on purpose.
`run_claim("S2")` still raises, unchanged: the two registries are separate by
design and the defect was in the documentation.

### `PCH_007` — the readout, and the edit category for it

`_pchlide_run` returns the mean over the final complete period.
`Chl_endpoint` is still returned — the repair adds a readout rather than
removing one. The curve is monotone, and the README's `C3` sentence is true
of the shipped output for the first time. **No verdict moved.**

**A new class: `InstrumentEdit`.** The protocol gated `MechanismEdit` and had
no category for a change to *where a number is read*, which alters sim output
while altering no mechanism and no parameter. That axis was already implicit
in the provenance types — `REPORTED / PHYSICS / SIM / BENCH` separates where a
number came from — and is now explicit. It takes **no prediction**, because it
is not a claim about the world; if it changes a verdict, that is a finding
about the old readout and goes in the claim table.

### Three promises with no implementation

| README says | was | now |
| --- | --- | --- |
| `run -> provenance record -> residual router -> hypothesis block` | `residual_route()` defined, never called | attaches on `REFUTED` and `UNDECIDED` runs, not on `SUPPORTED` |
| `BENCH is empty until someone runs one` | declared in `SOURCE`, producible by nothing | `record_bench()` / `bench_records()` / `bench` CLI; refuses a number with no method |
| the block prints a file hash for provenance | and a wall clock one line above it | deterministic `run id` = file hash + claim statuses; the clock stays in the log |

`BENCH` coverage is now a printed line per claim in the hypothesis block, so
*"no physical exit yet"* is stated rather than left as an absence the reader
has to notice. `run-all` is byte-reproducible.

**Still true and unchanged:** this folder has no bench data, and nothing in
it is a statement about wheat. What changed is that `BENCH` is now empty by
construction rather than by there being no way to fill it.
