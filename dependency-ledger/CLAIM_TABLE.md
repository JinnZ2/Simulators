# dependency-ledger — CLAIM_TABLE

`DLA_001..DLA_010`. Claims about the delivered `SOURCE_DROP.md` and
about the run.

The drop asks: *"Apply it to one case and publish the residual table,
including the unmeasured cells. The unmeasured cells are the finding."*
This is that run.

**Step 5 is CHECK against an INDEPENDENT record and egress here is an
allowlist that refuses every archive.** So on the real case every
record-bounded cell is `UNMEASURED`. That is the run, not a workaround,
and it is the finding the drop predicted.

## REFUTATION_PROTOCOL

Every claim names what would refute it. A failed check updates the
claim, never the delivered spec. Coefficients are marked with their
provenance and the unsourced share is reported with every number that
rests on them.

| id | claim | status |
|---|---|---|
| `DLA_001` | The method is right and its core move — propagate to conserved quantities, then check against an independent record — is a real instrument. | SUPPORTED |
| `DLA_002` | **Steps 3 and 4 pull opposite ways.** Step 3 stops at law-bounded quantities checkable anywhere; step 4 expands them into record-bounded ones checkable only with archives. The spec marks no crossing. | SUPPORTED |
| `DLA_003` | The real run closes on exactly one cell, and it is the one whose independent record is physiology rather than archaeology. Four of five cells are `UNMEASURED`. | SUPPORTED |
| `DLA_004` | `residual = required / attested` is a ratio and the spec does not require the two to be the same quantity. Unlike units make it void. | SUPPORTED |
| `DLA_005` | `residual >> 1` has no value. The threshold is a parameter and is declared here. | SUPPORTED |
| `DLA_006` | `attested undefined → NOT a pass` is the absent-vs-known-negative repair, designed into the spec before any code. | SUPPORTED |
| `DLA_007` | *"Do not aggregate residuals into one score"* is `domain-ledger`'s no-composite discipline arrived at independently, and it is enforced here rather than instructed. | SUPPORTED |
| `DLA_008` | COLLAPSED PROXIES is `fold-matrix`'s folded term under another name, and the vocabulary is imported rather than retyped. | SUPPORTED |
| `DLA_009` | My own collapsed-proxy guard could not fire, because the underscore was in its word class. | SUPPORTED |
| `DLA_010` | No archaeological fact is checked here and none is claimed. The residual on the one closing cell is 75% built from unsourced coefficients. | UNVERIFIED |

---

## DLA_002 — steps 3 and 4 pull opposite ways

    step 3   "Stop only at: energy, mass, momentum, time, material
             volume."
    step 4   "EXPAND each conserved quantity into its own dependency
             set. energy -> calories -> agricultural output -> arable
             area, water, storage, seasonality"

Step 3's stopping set is bounded by **physical law** and is checkable
from anywhere with no archive. Step 4's expansion set is bounded by
**the record** and is checkable only with access to granary capacities,
quarry volumes, spoil heaps, pollen cores.

The propagation crosses from one class to the other and the spec gives
one procedure with no marker for where it changes character. So a
reader running the audit cannot tell, from the procedure, which cells
they could have closed at their desk and which required an excavation —
and the two are not the same kind of unmeasured.

Every terminal requirement here carries `bound_by ∈ {LAW, RECORD}` and
the residual table is split on it. `close()` refuses a requirement that
declares neither.

**Falsifier:** a terminal requirement that is neither — or an argument
that the classes do not separate, which would mean an archive is
needed to check a conservation law.

## DLA_003 — the run, and what closed

    CASE: watercraft-propulsion   [REAL RUN]

    requirement                        bound   residual   verdict
    shaft_power_per_rower              LAW     8.71       GAP
    hull_drag_coefficient_at_loading   RECORD  --         UNMEASURED
    timber_volume_for_hull             RECORD  --         UNMEASURED
    crew_daily_calories                RECORD  --         UNMEASURED
    oar_replacement_rate               RECORD  --         UNMEASURED

    LAW      1 cell,  0 unmeasured
    RECORD   4 cells, 4 unmeasured

**The one cell that closes is the one whose independent record is
physiology.** Sustained human mechanical output is reachable from
anywhere; granary capacity is not. So the audit closed on the terminal
quantity that is a law and on none of the ones that are artifacts —
which is `DLA_002`'s split appearing as a property of a run rather than
as a distinction argued for.

And it closes as a **GAP**, not a pass: required shaft power per rower
is 8.71× sustained human output, which is the drop's own predicted
outcome for its own worked example — *"if required power per rower
exceeds sustained human output, the assumed propulsion efficiency is
wrong."* The missing-component spec follows:

    subsystem     : oar / hull / load-distribution system
    required perf : 871.2 W
    constraints   : period materials, river reach, displacement D
    reachable?    : OPEN -- separate investigation

`TIME AS SOLVENT` fires on this case and is **left firing**: a 30-day
duration enters the propagation with nothing bounding it, and bounding
it requires occupation layers this environment cannot reach.

**Falsifier:** an archive reachable from here that closes any
record-bounded cell.

## DLA_004 — the residual is a ratio and the spec does not guard it

`residual(r) = required(r) / attested(r)`. The spec does not say the
two must be the same quantity about the same object, and its own
step-4 example pushes toward pairs that are not: *"energy → calories →
agricultural output → arable area"* propagates a requirement in
kcal/day toward a record in hectares or tonnes.

`reasoning-gate` `G-DIM` — a ratio needs both operands to be properties
of one object. Enforced here: a requirement declares
`required_units` and `attested_units`, a mismatch or an undeclared unit
yields **no residual and lands on `UNMEASURED`**, and the units check
reports which of the two it was.

Routing it to `UNMEASURED` rather than raising is deliberate: a
unit-mismatched cell is a cell nobody has closed, which is exactly what
`UNMEASURED` means.

**Falsifier:** a residual across genuinely unlike units that carries
information.

## DLA_005 — `>>` has no value

    residual <= 1        requirement satisfied
    residual >  1        gap
    residual >> 1        method falsified as stated

`>>` is not a number. Declared here as `FALSIFY_AT = 10.0`, printed in
every report, and named as a parameter rather than left as a reading.

Same shape as `presented-binary` B10's `HANDOFF_CEILING`, which
disclosed its own constant, and `reasoning-dial` `RD_002`, where a
threshold moved with an unstated choice. The watercraft case lands at
**8.71** — below the threshold, so it reads `GAP` — and at
`FALSIFY_AT = 8` it would read `FALSIFIED`. The verdict on the drop's
own worked example is inside the range this one undeclared symbol
spans.

**Falsifier:** a principled value for `>>` derived from something other
than convention.

## DLA_006 — the repair is designed in

> `attested undefined   record gap, NOT a pass — flag, do not treat as
> zero`

That is the absent-vs-known-negative repair, stated in the delivered
spec before any code, on the field where it costs most. This repository
has recorded that repair roughly sixteen times and found it *designed
in* rather than *missing* in a handful of those.

It is also given its own named failure mode — `RECORD GAP AS PASS` —
so it is both a schema rule and a guard, which no other instance here
has been.

Implemented three ways: `residual()` returns `None` and never `0`;
`verdict(None)` is `UNMEASURED`; and an `attested` of literal **zero**
is *refused*, because a zero denominator is not a residual and is not
the same statement as an absent one.

**Falsifier:** a path where an absent cell scores as satisfied. The
guard exists to catch exactly that and is null-tested both ways.

## DLA_007 — no aggregation, enforced

> *Do not aggregate residuals into one score. The per-requirement
> residual is the whole point: it localises the missing capability to a
> named subsystem.*

`domain-ledger` `DL_001` reached the same rule from the other side —
four uncombined ratios, and `anchor.py`'s selftest asserting *"no
composite emitted"*. Arrived at independently, and this statement of it
is better, because it gives the reason: a mean over subsystems names
none of them.

Enforced rather than instructed. `no_aggregate()` returns
`{"aggregate": None}` with the reason, and the selftest walks the AST
of `close`, `table_split`, `no_aggregate` and
`missing_component_spec` asserting that **no residual is ever summed,
maxed, or averaged**.

The first version of that check grepped for `sum(` across the closure
path and caught `table_split`'s cell **counts** — counts of verdicts,
not aggregates of residuals. Narrowed to the rule as stated.

**Falsifier:** a caller that needs a single number, and a defence of
what it would mean.

## DLA_008 — COLLAPSED PROXIES is the folded term

> *Stopping propagation at "labor", "resources", "organisation". Each
> is a matrix entered as a scalar.*

`fold-matrix/fold_register.py` opens by defining a folded term as *"a
compact matrix wearing the costume of a scalar"* and its register
already carries `resources` — *"a stock and a flow, welded"* — and
`capacity` — *"peak force, quoted where sustained work capacity is
meant"*. Two authors, two vocabularies, one operation.

The guard **imports** that register rather than retyping the terms, so
the two cannot drift, and the selftest asserts the import is live and
that `resources` is in both. Vocabulary size is 23 and is whatever the
register currently holds.

**Falsifier:** a collapsed proxy the register does not name and would
not accept.

## DLA_009 — my own guard could not fire

`guard_collapsed_proxies` tokenised requirement names with
`re.findall(r"[a-z_]+", name)`. The underscore is **inside** the
character class, so `labor_required` is a single token, `labor` never
appears, and the guard returned `fired: False` on a requirement named
`labor_required`.

The guard whose job is to catch a term hiding inside a name could not
see a term inside a name.

`UNI_009`'s shape — `lean` matching inside `clean` — in the tokenizer
of a guard written after that finding was recorded. Caught by the
selftest arm that requires the guard to fire on a planted violation,
which is the arm that exists because a guard that cannot stay silent is
not a guard and neither is one that cannot fire.

**Falsifier:** a compound name the repaired tokenizer still misses.

## DLA_010 — nothing archaeological is checked, and the number says so

Eight coefficients in the real case. **Six are `UNSOURCED`** and each
carries a stated reason: no period hull form measured or replicated, no
attested vessel dimensions, no hydrological record for the reach, no
attested crew count, and — the one the whole audit turns on — no
measured oar propulsive efficiency, *"exactly the one the
reconstruction assumes without stating."*

So the 8.71 residual is a demonstration that the propagation runs. It
is **not** a measurement about any vessel, any river, or any period.
The `SMUGGLED_CONSTANTS` guard reports `unsourced 6 of 8 (75%)` in
every report so the number cannot be quoted without it.

The two constructed cases are labelled `CONSTRUCTED` in their own
`artifact` field and exist so the closure test can be shown to return
`SATISFIED` and `FALSIFIED` — without them the table would be
`CONSTANT_SILENT` and a run of all-`UNMEASURED` would not demonstrate
that the instrument can say anything else. All four verdicts occur
across the corpus and the selftest asserts it.

**Falsifier:** run it with an archive. Every unsourced coefficient
names what would source it, and every unmeasured cell names what would
close it — which is what the drop said the output should be.
