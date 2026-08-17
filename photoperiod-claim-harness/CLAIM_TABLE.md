# CLAIM_TABLE — photoperiod-claim-harness

Six claims, `PCH_001..006`, about the **harness**. The harness carries its
own claim table (`C1..C5`) about a greenhouse result; that one is delivered
and is not restated here.

## REFUTATION_PROTOCOL

The delivered file is landed **verbatim** and is not modified. Claims here
are about whether it can fail in the ways it says it can, checked by running
it — `harness_audit.py` imports it and changes nothing.

This folder has **no bench data**, and neither does the harness. Nothing
here is a statement about wheat, chlorophyll, or any published result. The
harness's own hypothesis block says the same thing about itself, which is
why it is worth auditing rather than arguing with.

A failed check updates the claim.

## Claims

| id | statement | status |
| --- | --- | --- |
| `PCH_001` | **`C1`'s predicate returns SUPPORTED when the sim produces nothing.** Zero signature cells gives `signature_spread = 0.0`, which passes `< 1.5`, and the `reads` line for TRUE is *"the reported metrics are diagnostic of real efficiency."* | SUPPORTED |
| `PCH_002` | **`C1`'s own grid says something narrower and stronger than its `reads` line.** The signature appears in 58 cells spanning a 4.88× range of true energy-per-dry-gram, and **all 58 are below 1.0**. Non-diagnostic of magnitude, diagnostic of sign. | SUPPORTED |
| `PCH_003` | **The `MechanismEdit` guard screens 2 of the 4 free-text fields it is given** — `reason` and `mechanism`. `basis` and `prediction` pass a forbidden reason unscreened, and they are the two fields that ask for justification. | SUPPORTED |
| `PCH_004` | **`settle()` records a prediction and never adjudicates it**, and cannot tell whether the edit happened. `prediction_held` is set to `None` by construction, and `file_hash_before == file_hash_after` when nothing was edited. | SUPPORTED |
| `PCH_005` | **The header's own usage example fails.** `run S2` passes a sim id to a command that looks up claim ids; `run_claim("S2")` raises an uncaught `StopIteration`. | SUPPORTED |
| `PCH_006` | **The predicates are real and mostly deny.** Four of five come back REFUTED on the shipped run, including `C2`, which refutes its own stated hypothesis and explains the mechanism, then files the next candidate in `PENDING_EDITS` rather than retuning toward it. | SUPPORTED |

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
