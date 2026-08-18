# AUDIT_NOTES — constraint-assembly

Added, not delivered. [`assemble.py`](assemble.py) is the drop as received
and is not modified.

    python3 assemble.py --selftest
    python3 assembly_audit.py

## What the drop is

One file. Records cases where sufficiency was **composed from parts that
individually do not do the job**.

The operation is construction, not selection: an option that did not exist
in the environment, built out of components each of which is insufficient
alone, under a fixed budget. Three constraint classes, kept apart because
merging them loses a failure mode — **invariant** (holds regardless of
use, cannot be spent, available for the whole event), **consumable**
(finite, and availability is destroyed by spending; partial use can be
worse than none), **soft** (does not hold under load, recorded so reliance
is visible rather than to score anybody).

Rejected candidates are the data. A composed solution is only visible as
composition if the rejected options are recorded with the constraint that
ruled each out; a case with no rejections is selection and is recorded as
such.

Selftest 18/18.

## File status

| file | status |
|------|--------|
| `assemble.py` | delivered, verbatim |
| `cases/` | not delivered |
| `README.md` | not delivered |
| `CLAIM_TABLE.md` | not delivered |
| `assembly_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Nothing is reconstructed. The docstring fixes the vocabulary and the
readouts, and fixes no case — inventing one would put a situation in the
author's mouth, which is what `category-weld` `CW_004` cost when the
arithmetic was reconstructed from prose that did not fix it.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| CA_001 | The reversal is the contribution and it has a mechanism in it — constraints as the term that makes composition **decidable**, so hard laws are the parts inventory; it runs opposite to the two nearest folders on the same object without contradicting either | the argument reducing to "constraints are good", or a readout that scores constraint count as quality | SUPPORTED (holds) |
| CA_002 | The nearest-neighbour discriminator is built in — `selection_not_assembly` is a readout, not a caveat — and `composition_present` **fails closed**: an unrecorded `sufficient_alone` blocks the claim and is reported separately as `sufficiency_unknown` | unknown sufficiency being read as insufficiency, or the selection case being left to prose | SUPPORTED (holds) — ninth instance of the absent-vs-known-negative repair, fourth designed in |
| CA_003 | The headline claim is about the **available** inventory — *"more hard constraints, more composition available"* — and `score()` filters to `used` on its first line, so no readout counts available-but-unused components; the schema expresses the inventory (`used` is per-component) and the table does not report it | a count over all components rather than over used ones | SUPPORTED |
| CA_004 | `rejections_all_grounded` returns `False` both for an ungrounded rejection and for a case with nothing to ground — the narrow version of the usual shape, since `selection_not_assembly` sits beside it and the footer states the rule | returning `None` when `rejected` is empty, the way `budget_consumed` does one folder over | SUPPORTED (narrow) |
| CA_005 | `--case` has no bounds check and raises `IndexError` with no argument, while `--new` in the same function IS guarded with the expression both `domain-ledger` tools use throughout — `CC_004` recurring unchanged in the next tool | the same guard applied to both flags | SUPPORTED |
| CA_006 | The DIAGNOSTIC QUARANTINE section names the same budget `closure-cost` measures, from the other end — that folder measures the categorisation stall, this one records whether the operator declined to spend it — and the pairing is stated by the author, not inferred here | the two budgets being different quantities | SUPPORTED (holds) |
| CA_007 | With no `cases/` directory the tool prints a well-formed report with zero rows and exits 0 — fourth tool in the family to do so; three refuse and they are the older ones | the empty state refusing, or saying it is empty | SUPPORTED |

## 1 — CA_001, the reversal and where it sits

> Constraints are not what limits the option set. They are what makes
> composition computable. A term that will not move can be leaned on; a
> soft term cannot, because there is no way to know when the pieces add
> up. So the parts inventory is not domains — it is domains with hard laws
> in them. More hard constraints, more composition available.

That is an argument with a mechanism in it rather than a slogan, and the
mechanism is **decidability**. Composition needs a stopping rule; a term
that holds regardless of use supplies one. A term that moves under load
does not, so a plan resting on it carries no assembly guarantee — which is
why `soft` is a recorded class and not an excluded one.

It runs opposite to the two nearest folders in this drop family, on the
same object:

| folder | the option space |
|--------|------------------|
| `generation-capacity/` | REDUCED upstream — the party cannot generate what is missing |
| `presented-binary/` | CLOSED at presentation — the reduction is performed rather than found |
| `constraint-assembly/` | CONSTRUCTED — an option assembled from parts that individually do not do the job |

The first two measure an option space smaller than it looks. This measures
one being made larger, from components, under a fixed budget, and it names
constraints as the enabling term in that operation rather than the
limiting one. The three are not in tension; they are three positions on
one quantity, and only this one treats hard laws as the parts inventory.

The invariant/consumable split carries its own operational line, and it is
the sharpest sentence in the docstring: *"an invariant is encountered, a
consumable is SPENT. Failure on a consumable is usually spending it, not
running into it."* `consumables_destroyable_by_partial_use` is the readout
for the hazard half — a consumable is a resource and a hazard in the same
term.

## 2 — CA_002, fail-closed on unknown sufficiency

`composition_present` is the folder's central claim per case, and it does
not make that claim when the evidence for it is missing:

    used components                  composition  unknown   single_sufficient
    both explicitly insufficient     True         False     False
    one unrecorded                   False        True      False
    one sufficient alone             False        False     True

An unrecorded `sufficient_alone` blocks composition **and** is reported
separately, so the reader can tell a case that failed the test from a case
that could not be tested. This is the opposite direction from
`closure-cost` `CC_003`, where an omitted field reads as the informative
state.

Ninth instance of one repair across this drop family, fourth designed in
rather than found:

    PB_004   frame_sim option_gain          found -- merged
    PB_012   binary_audit handoff()         found -- merged
    GC_004   MECHANISM_10 R3                found -- merged
    MD_002   moral-decomposer reduces_to    found -- merged
    CC_002   closure.py rules_out           found -- merged
    GC_010   SUBCASE_10A S1                 designed in -- specified
    DL_008   anchor.py routing states       designed in -- implemented
    CC_001   closure.py knowledge_state     designed in -- vocabulary
    CA_002   assemble.py sufficiency        designed in -- fail-closed

`selection_not_assembly` is the second guard and it is aimed at the
nearest neighbour: selection from presented alternatives is the thing
assembly is most likely to be mistaken for, and it is a column in the
table rather than a warning in the prose. The selftest exercises it.

## 3 — CA_003, the reversal's own quantity does not reach the table

The headline claim is a statement about what was **available** to compose
from. Every readout is a statement about what ended up in the composition.

`score()` opens with

    used = [x for x in comps if x.get("used")]

and everything downstream derives from `used`. On a case recording five
components, three of them available and not used:

    components in the file       5   (2 used, 3 available and unused)
    components_used              2
    invariant_count              1   (used only)
    consumable_count             1   (used only)
    fields counting the unused   none

This is not the usual missing-field shape — `MF_017`, `CW_015`, `DL_004`,
`GC_012` are all cases of a stated rule with no schema slot. Here **the
slot exists**: `used` is a per-component boolean, so a case can record
what was available and not taken, and the inventory is expressible today.
What is missing is the readout. `hard_constraints_available` counted over
all components rather than over used ones is one line, and it is the
number that would let the claim be checked across cases — does a case with
a larger hard-law inventory compose more.

Without it, `invariant_count` reads as an inventory measure and is a
composition measure. Two cases with identical used-counts and very
different available-counts are indistinguishable in the table.

## 4 — CA_004, the narrow version

    "rejections_all_grounded": len(rejected) > 0 and len(grounded) == len(rejected)

| case | rej | all_grounded | selection |
|------|-----|--------------|-----------|
| 2 rejections, both grounded | 2 | True | False |
| 2 rejections, one ungrounded | 2 | False | False |
| 0 rejections (selection) | 0 | False | True |

Rows 2 and 3 return the same value for different reasons: a data-quality
failure in an assembly case, and a case with nothing to ground.

This is worth recording as the **narrow** version of the shape rather than
the usual one. `selection_not_assembly` sits beside it and separates the
two, the table prints both columns, and the footer states the reading rule
— *"A case with rej 0 is selection, not assembly."* A reader has what they
need. What is left is that the column alone reads `no` for a case with
nothing to ground, so the field is not safe to quote on its own; returning
`None` when `rejected` is empty would cost nothing and is what
`budget_consumed` does one folder over.

## 5 — CA_005, the argument guard, second consecutive tool

| tool | bounds-checked lookup after a flag |
|------|-----------------------------------|
| `domain-ledger/ledger.py` | yes |
| `domain-ledger/anchor.py` | yes |
| `closure-cost/closure.py` | no |
| `constraint-assembly/assemble.py` | no |

Measured: `assemble.py --case` with no argument raises `IndexError`, rc 1.

`CC_004` recorded this for `closure.py`. It recurs unchanged in the next
tool, and in both files `--new` IS guarded, with exactly the expression
the two `domain-ledger` tools use throughout. Same author, same pattern
available in the same function, applied to one flag of two.

## 6 — CA_006, one budget named from both ends

> DIAGNOSTIC QUARANTINE. Where a cause is unknown at the time of action,
> whether the diagnostic was deferred is recorded separately from the
> assembly. Establishing what class of event this is spends the same
> budget the assembly needs. Deferral is a recorded property, not a
> virtue.

`closure-cost`'s central readout is `diagnostic_spend` — time spent
establishing what class of event this is, over time available before
action had to be taken. This folder records whether that spend was
**deferred**, on the same budget:

| folder | what it reads |
|--------|---------------|
| `closure-cost/` | the categorisation stall, as a fraction of the budget consumed |
| `constraint-assembly/` | whether the operator declined to spend it, and assembled without knowing the cause |

The pairing is stated by the author rather than inferred here, and it is
the first time in this drop family that two folders name the same budget.
`closure-cost`'s README says the same thing from its side: *"the observed
case that generated it is a category-stall avoided, not one suffered."*

"Deferral is a recorded property, not a virtue" is consistent with the
module's own *"No scoring of the operator"*, and it is the harder version
of that rule — deferring the diagnostic is the behaviour the shape
predicts, and it is still not scored.

## 7 — CA_007, the empty corpus

    rows printed  : 0
    lines printed : 12
    exit code     : 0

| tool | refuses on empty |
|------|------------------|
| `category-weld/weld.py` | yes |
| `presented-binary/binary_audit.py` | yes |
| `generation-capacity/capacity.py` | yes |
| `domain-ledger/ledger.py` | no |
| `domain-ledger/anchor.py` | no |
| `closure-cost/closure.py` | no |
| `constraint-assembly/assemble.py` | no |

Three refuse, four print. The split is by drop age and the newer half is
now the larger one. `DL_005` and `CC_006` stand; this is the fourth
instance and adds nothing new except the count.

Unlike `closure.py`, this table's footer does not state a corpus
condition. It states a reading rule, which is the right footer for a
populated run and says nothing about an empty one.
