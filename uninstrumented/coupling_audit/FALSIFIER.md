<!--
SPDX-License-Identifier: CC0-1.0
To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this file.
-->

# FALSIFIER

The marker: when a model measures a flow across a set of agents, its own
coupling-variability machinery is applied unevenly — it runs on some agents
drawing on the flow and not on others, and the gate is set by species or by
market category rather than by anything in the units being measured.

Two findings would refute it. Either is sufficient.

## 1. A model scoring `PRESENT_COUPLED`

Every agent drawing on the measured flow carries a term, and the
coupling-variability machinery is applied to all of them under the same rule.
`audit.derive_verdict()` returns `PRESENT_COUPLED` for exactly this case, and
the schema reaches it — the selftest constructs one, so the verdict is not
unreachable by construction.

Where to look first: the literature that already quantifies the flow rather
than the literature that allocates it. See `OPEN.md` — the energy accounting
exists. If a model that routes it also couples it, the marker is refuted on
its strongest case.

## 2. A gate that is both STATED and justified in the units being measured

This is the more interesting refutation, because it does not require the
model to change what it counts.

**A stated, quantity-justified gate is a pass, not a hit.** A model may draw a
boundary and remain fully sound: if the exclusion rule is written down *and*
its justification is in the flow's own units — this agent's draw on freshwater
is below the resolution of the basin-scale accounting; this agent's caloric
draw is within the stated error of the household estimate — then the audit has
found a documented modelling decision, not an asymmetry. The audit should say
so and score it as a pass.

What does **not** qualify, however clearly it is written:

- **species** — that the unit of analysis is one species is a definition, not
  a justification in the units. Nothing about a kilocalorie distinguishes the
  organism metabolising it.
- **market output** — that an agent enters only if it yields a priced
  commodity is a justification in a different currency than the one being
  measured. Nothing about a cubic metre of freshwater distinguishes the animal
  that drinks it by whether the animal's output has a price. This is the
  sharpest of the three seed gates precisely because it is the best
  documented: `FAO LEAP / GLEAM` states its boundary plainly, and the boundary
  is still drawn on salability.

`audit.gate_justified_in_units()` returns `True` / `False` / `None`, with
`None` reserved for a gate not yet examined, so "not justified" and "not
looked at" do not share a value.

## Status on the current corpus

Three entries, none refuting. That is three cases, not a survey, and the
entries were selected as likely instances — see `LOG.md`, which records that
the audit was run against three models with three hits *before* the schema was
written. A corpus assembled after a hypothesis, by the party holding it, is
not evidence about a base rate.

The prediction worth stating, and worth being wrong about: no model in the
drought or regional food-security literature scores `PRESENT_COUPLED`.
