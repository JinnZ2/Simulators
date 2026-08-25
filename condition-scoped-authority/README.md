# condition-scoped-authority

**Marker under exploration.** Delivered spec:
[`SPEC_CONDITION_SCOPE.md`](SPEC_CONDITION_SCOPE.md), landed verbatim.
Companion to [`stop-authority/`](../stop-authority/).

> Authority is not held by a position. It is held by a position **for a class
> of condition**. Rank and scope are different objects and a single ranking
> cannot represent scope.

```
python3 condition_scope.py   # every total order, checked against the partition
python3 organ.py             # coordination as a specialization, not a rank
```

Both take `--selftest`. 30 / 25 checks, 55 in all, green. Samples pinned in
`samples/`, byte-reproducible.

## The claim is checkable, not arguable

A total order over positions either does or does not reproduce a
condition-scoped authority table. So `rank_search()` enumerates **every** total
order and scores each — a complete search at these sizes, not a sample.

The delivered protective-detail partition, all 2 of 2 orders:

| order | wrong | classes missed |
| --- | --- | --- |
| principal > bodyguard | 1 | threat_live |
| bodyguard > principal | 4 | clientele, finances, politics, schedule |

**Exact matches: 0. `NO_RANK_REPRESENTS_IT`.** A total order has no condition
column, so it names one decider and names them in every class. The table names
different deciders in different classes, and no reordering changes that.

**And the best ranking fails exactly where the stakes are.** Principal-on-top
gets 4 of 5 classes right — 80%, which reads as a good approximation. The one
class it misses is the live threat: the class in which the spec says the
specialist holds total authority *including physical force against the
principal's stated preference*. The classes are not interchangeable, and
averaging over them is the same move as scoring a facility on the variables
still being read.

**Adding scoped domains makes a rank fit worse, not better.** With a third
scoped position (marked in the module as an extension, not delivered), all 6
orders are checked, still 0 exact, and the best is wrong on **2** classes
instead of 1. Every domain with its own reading capacity is another class the
single ranking must get wrong — so the representation degrades with exactly the
thing that makes the structure work.

## Rank does not invert

`holds()` returns `DECIDES` or `NOT_IN_DOMAIN` — never a smaller quantity of
the same thing. The spec is explicit that the domain is partitioned and that
inside the partition the principal *was never the decider*, so modelling the
threat case as "the guard outranks the principal" is already the error.

`Partition` refuses a table where one position holds every class (a ranking
written as a table) and refuses a position with no class at all (not a party to
the arrangement, constrained by nothing, gaining for free). That enforces the
spec's symmetry — *neither party reads the other's domain* — structurally.
What it **cannot** check is whether the domains assigned actually match where
reading capacity sits, which is the whole justification.

## What the collapsed structure states silently

Written out:

> **principal holds the reading capacity for all 5 condition classes
> simultaneously**: clientele, finances, politics, schedule, threat_live

Classes actually held: 4 of 5. Overclaimed: `threat_live`.

Rank has no condition column, so a rank-only structure says the same thing in
every class. The claim is about reading capacity in domains the position does
not read — and nobody would defend it written down.

## BOUND vs ADVISORY: the offered evidence discriminates nothing

Criterion applied: *an item discriminates only if it would be FALSE under an
advisory arrangement.*

| offered item | true under advisory |
| --- | --- |
| visibility | ✓ an advisor is visible |
| seat at executive meetings | ✓ an advisor has a seat |
| influence on strategy | ✓ influence is what advisory *means* |

**Offered: 3. Discriminating: 0.** These are not weak indicators of BOUND —
they are indicators that do not vary between the two cases, so a configuration
scoring high on all three is *unmeasured*, not strong.

What would discriminate is named beside them: a finding that stood against a
party who sought its reversal, or a documented reversal and by whom. Note the
absence of a reversal record is **not** it — see
[`stop-authority/binding.py`](../stop-authority/binding.py), where an empty
reversal record beside zero findings reads `NOT_LOOKED`.

`AuthorityClaim` refuses to measure an `UNSTATED` claim rather than defaulting
it either way. That is the spec's word — *unsigned* — and the same word the
stop count carries next door.

## The organ error

`Body` refuses to build a coordinator whose sense channels are a superset of
the others': that would be a hierarchy written in anatomy vocabulary. A
coordinator must have channels the others lack **and** lack channels they have.

**Failure 1 — reassignment by decree.** Instruct the hand to do the foot's
task:

| | capacity | functioning |
| --- | --- | --- |
| before | 1.00 | True |
| after | 0.67 | **False** |

Verdict `NON_FUNCTIONING`, not degraded. The reassigned task outputs **exactly
0.0**, state `CANNOT_SENSE_THE_INPUT` — there is no partial reading of an input
the organ cannot detect, so there is nothing for a degradation to start from.

**The aggregate is itself the degradation illusion.** Capacity 0.67 presents as
a 33% shortfall. Degraded and non-functioning differ in whether a *required
channel is absent*, which is a property of the worst task and precisely what a
mean removes.

**And the decree cannot observe its own consequence.** The coordinator's task
is untouched, so `coordinator_signal_unchanged` is `True` and
`observable_at_the_decree` is `False`. No amount of attention at that point
reveals the failure — it is in a channel the coordinator does not have, which
is why the task looked reassignable in the first place.

**Failure 2 — scoring the coordinator as the system.**

| | system capacity | coordinator score |
| --- | --- | --- |
| healthy | 1.00 | 1.00 |
| broken | **0.67** | **1.00** |

The coordinator score **does not move at all**. Reporting it as the system does
not give a biased estimate of capacity — it gives a number with *zero
sensitivity* to it. The measurement cannot fail, which is what makes it
attractive.

**This is the third instance of one shape and it is not three findings.**
Measure a subset, report it as the whole: the narrow safety metric rising while
the facility degrades, the stop count read as the authority measurement, and
now the coordinator score read as system capacity. One repo, one builder — by
`operator-structure-echo/corroboration.py` that agreement is `INHERITED`.

## What is carried and not tested

- **The partition is taken on the spec's word.** Whether a bodyguard really
  holds total authority in a live threat and none over clientele is a claim
  about how protective details work. If it is wrong, the search is a complete
  proof about a table nobody should have written.
- **The rubric link is carried, not tested.** The spec says failure 2 is the
  same error as the centralized-executive prior in consciousness and
  intelligence rubrics — *org chart and measurement instrument, one shape*.
  This module has no rubric corpus. Nothing here supports it and nothing
  contradicts it.
- **The evidence audit reads three phrases**, applying a stated criterion. It
  is not a survey of the EHS literature.

## Open work, carried and not closed

| item | state |
| --- | --- |
| restore scope-partition to a structure collapsed to rank | NO_METHOD_PROPOSED |
| does BOUND survive outside regulated domains | **NOT_SEARCHED** |
| if it survives only where a regulator forced it | CONDITIONAL_ON_THE_ABOVE |

The question needs instances of BOUND authority in **unregulated** domains.
Zero are recorded, and zero without a search is `NOT_SEARCHED`, not `ABSENT` —
zero rows here is the size of the search, not the size of the population. The
spec's conditional is well-formed and its antecedent is unestablished, so the
consequent is not available.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
