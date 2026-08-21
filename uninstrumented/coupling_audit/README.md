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

On the four delivered cases: 2 of 4 blind by tissue, **4 of 4** never tested
the standing explanation against the coupling hypothesis, 2 of 4 carry a
same-site wild control. Roughly a tenth of the canid individuals sit in a
tissue that can ask the question.

**The cheapest next step is already a working design elsewhere.** Schipluiden
sampled *wild* animals from the *same site* as a baseline — domesticates
deviate, red deer and suids do not, so the deviation is attributable to
household provisioning rather than to environment. That is a control in the
`null-harness` sense, and nobody has pointed it at dogs with a wild-canid
control at the same site. Arroyo Hondo stumbled into one by accident when a
coyote came back with domestic-dog values.

## A unit, not a Y/N

Intra-tooth amplitude is a coupling-variability measurement — flat means a
fixed draw, high amplitude means supply-coupled. That is the first real unit
this audit has. `amplitude_reading()` **raises without a declared sampling
geometry**, because geometry changes the intra-tooth pattern and a cross-study
comparison that does not state it is comparing two instruments. Same shape as
`audit.py` refusing coupling machinery that is not named in the model's own
vocabulary: a number from an unnamed instrument is not yet a reading. The
thresholds are conventional, scaled to one delivered herd range, and are not
calibrated against a controlled feeding experiment here.

## Reading the entries

All three seed entries carry `MODEL_SEEDED = True`. The shape and the evenness
test are the author's; the field names, verdict labels and write-ups are
model-generated from web search results; the underlying facts are cited
sources, not authored claims. A reader checking this folder should check the
cited documents, not this folder's characterisation of them.

Stdlib only. Parses under Python 3.9. CC0.
