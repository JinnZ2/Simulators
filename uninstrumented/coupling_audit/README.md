<!--
SPDX-License-Identifier: CC0-1.0
To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this file.
-->

# coupling_audit

**A marker under exploration, not a position under defense.**

## What it asks

When a model measures a flow across a set of agents, does the model's own
coupling-variability machinery get applied evenly to every agent drawing on
that flow — or is it gated?

Not "is the agent counted". The question is about **evenness**: whether a
capability the model already has, and names in its own vocabulary, runs on all
the agents in scope or stops at a line.

## Verdicts

| verdict | meaning |
|---|---|
| `ABSENT_NO_MACHINERY` | the agent is absent and the model has no coupling term for anyone — a uniform simplification, not an asymmetry |
| `ABSENT_MACHINERY_PRESENT` | the agent is absent and the model **has** a coupling term, which it runs on others |
| `PRESENT_FIXED` | the agent is in the ledger with a fixed draw, or folded into another agent's line, while others get the coupling term |
| `PRESENT_COUPLED` | the agent is in the ledger with a supply-coupled draw under the same rule as the others |

The second is the stronger finding, and the reason the audit exists: the
capability is present and stops somewhere.

## Gate types

`species` · `market_output` · `unstated` · `other`, each recorded with whether
the rule is **stated** or falls out of a definition.

## Falsifier

A model scoring `PRESENT_COUPLED`, **or** a gate that is both stated *and*
justified in the units being measured rather than by species or market
category. A stated, quantity-justified gate is a **pass, not a hit**. See
[`FALSIFIER.md`](FALSIFIER.md).

## Relationship to the parent register

[`../uninstrumented.py`](../uninstrumented.py) asks whether an instrument's
constitution prevents a quantity from **appearing at all**. This asks
something different and weaker: the quantity *can* be registered, the
machinery exists in the model, and it is applied to some agents and not
others. An exclusion register would find nothing here — nothing is excluded
from the apparatus; the apparatus is pointed at a subset.

`python3 audit.py --mechanisms` runs each gate type against the register's
eight mechanisms, importing them rather than copying them. The result:

- **`species` → `AUDIT_ASYMMETRY`, STRONG.** "Guard fires on one side only",
  one level up — the asymmetry is in the model's machinery rather than in an
  audit's hedging. **No new mechanism is claimed for it.**
- `market_output` → `PROXY_SUBSTITUTION`, PARTIAL. Salability is enforceable
  and does displace the biological criterion, but proxy substitution names a
  measure standing in for a *quantity*, and this stands in for *membership*.
  Recorded, not resolved.
- `unstated` → `BUDGET_BOUNDARY`, PARTIAL. A per-capita denominator is a
  boundary imported from an accounting convention: open numerator, denominator
  closed to one species.

**No candidate ninth is claimed.** One gate matches an existing mechanism
strongly, and separately the ordinal is taken — `MECHANISM_09`,
`MECHANISM_10` and `MECHANISM_11` are proposed in sibling folders against this
same register of eight, so "a candidate ninth" would collide even if the shape
were new.

## Files

- [`audit.py`](audit.py) — record schema and scoring. `--report`,
  `--template`, `--mechanisms`, `--selftest`.
- [`entries.py`](entries.py) — three seed entries (IPC, per-capita carbon
  footprint, FAO LEAP/GLEAM), all `MODEL_SEEDED`.
- [`provisioning.py`](provisioning.py) — the discriminating test, and the
  audit's first real unit. `--resolution`, `--cases`, `--amplitude`,
  `--selftest`.
- [`FALSIFIER.md`](FALSIFIER.md) · [`OPEN.md`](OPEN.md) · [`LOG.md`](LOG.md)

## The coupling is already measured — under other names

`audit.py` asks whether a model applies its coupling machinery evenly.
`provisioning.py` is about the other end: whether the coupling is *measurable*
in a given body of evidence, and what separates it from the explanations
already standing in the literature.

Three hypotheses account for isotopic spread in an archaeological assemblage,
and they predict different signatures:

| hypothesis | within-individual | between-individual | Sr co-varies | seasonal |
|---|---|---|---|---|
| `MOBILITY` | no | yes | **yes** | no |
| `BREED_OR_STATUS` | no | yes | no | no |
| `VARIABLE_COUPLING` | **yes** | yes | no | **yes** |

**The within-individual column is the only one that separates the coupling
hypothesis from the other two — and it is exactly the column a years-averaging
tissue removes.** Bone collagen integrates years, so a within-year switch is
averaged away before the sample is taken and the spread can only present as
between-individual. In that tissue the coupling hypothesis **cannot fail**,
which is not support for it: it is `CONSTANT_SILENT` by construction. G-RES
pairing: bone collagen is **12.2× too coarse** for a seasonal feature at a
margin of 2; incremental dentine and sequential enamel resolve it.

On the five delivered cases: **3 of 5 blind by tissue, 5 of 5** never tested
the standing explanation against the coupling hypothesis, 2 of 5 carry a
same-site wild control. Roughly a tenth of the canid individuals sit in a
tissue that can ask the question, and published dentine *n* for dogs is about
**4**. No new excavation required.

The method itself is not in doubt: **Balasse et al.** recovered a known
C3→C4 diet switch and weaning from intra-tooth variation in a *controlled
feeding study*. The positive control exists — for caprines and cattle.

**The cheapest next step is already a working design elsewhere.** Schipluiden
sampled *wild* animals from the *same site* as a baseline — domesticates
deviate, red deer and suids do not, so the deviation is attributable to
household provisioning rather than to environment. That is a control in the
`null-harness` sense, and nobody has pointed it at dogs with a wild-canid
control at the same site. Arroyo Hondo stumbled into one by accident when a
coyote came back with domestic-dog values.

## A unit that replaces the boolean

Intra-tooth amplitude is a coupling-variability measurement — flat means a
fixed draw, high amplitude means supply-coupled. **For archaeological cases it
replaces `coupling_machinery_present` rather than sitting beside it**
(`OPEN.md` item 9): the coupling there is a property of an animal's intake,
not of a document. `coupling_field_for()` implements that, with a hard scope —
it needs an incremental tissue *and* a declared geometry, and returns an
explicit non-value otherwise, so `NOT_APPLICABLE_TISSUE`,
`GEOMETRY_NOT_DECLARED`, `NOT_MEASURED` and a real reading never share a
value. There is no tooth in a national carbon inventory, so `entries.py` keeps
the boolean — a scope limit, not an inconsistency.

`amplitude_reading()` **raises without a declared sampling geometry**, because
a 2024 *Journal of Archaeological Science* paper finds dentine geometry
changes the intra-tooth pattern, so a cross-study comparison that does not
state it is comparing two instruments. Same shape as `audit.py` refusing
coupling machinery not named in the model's own vocabulary: a number from an
unnamed instrument is not yet a reading. Thresholds are conventional, scaled
to one delivered herd range, not calibrated here.

## The gate, seen from the other side

The cross-species extension (`OPEN.md` item 10, **stated by the author,
untested**) predicts the same coupling for chickens, cattle, yak and buffalo —
household draw tracks surplus, protection held constant through the switch —
and notes that in species with a commodity output the switching *is already
measured*, seasonally, per individual, "because no one had to argue about
whether the animal counted."

The corpus is consistent with that: **6 of 6 published applications of the
method are on commodity species, 0 on companion species**, against a dog
sequential *n* of about 4. The count does **not** establish the cause —
sample availability, tooth size and enamel thickness, and which
agricultural-research funding lines exist are all live alternatives. What it
shows is that the asymmetry is real and large.

Worth naming: this is **the same gate as entry 3**, seen from the other side.
There `market_output` keeps companion animals out of the water accounting.
Here the same line is why the instrument exists at all for cattle. One
criterion, two consequences — the animal that sells gets both the ledger entry
*and* the instrument.

## Reading the entries

All three seed entries carry `MODEL_SEEDED = True`. The shape and the evenness
test are the author's; the field names, verdict labels and write-ups are
model-generated from web search results; the underlying facts are cited
sources, not authored claims. A reader checking this folder should check the
cited documents, not this folder's characterisation of them.

Stdlib only. Parses under Python 3.9. CC0.
