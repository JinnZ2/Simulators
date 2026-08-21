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
- [`FALSIFIER.md`](FALSIFIER.md) · [`OPEN.md`](OPEN.md) · [`LOG.md`](LOG.md)

## Reading the entries

All three seed entries carry `MODEL_SEEDED = True`. The shape and the evenness
test are the author's; the field names, verdict labels and write-ups are
model-generated from web search results; the underlying facts are cited
sources, not authored claims. A reader checking this folder should check the
cited documents, not this folder's characterisation of them.

Stdlib only. Parses under Python 3.9. CC0.
