---
name: cyclic-programming
description: Physics-substrate language for recycling code constructs across languages; core thesis is a quantity-type taxonomy. Includes a full interpreter audit.
sources: [field]
aliases: [cyclic-programming, cyclical programming language]
---

## What it actually is

A programming language based on energy physics. **True purpose: recycle and repurpose
programming-language constructs against a physics substrate so nothing is wasted.**

The "quantum/thermo toy" README framing was deliberate camouflage to get past earlier-model
guardrails and comprehension failures. The repurpose adapter, controller, and loader are the
real spine.

## Motivating problem

AI will generate astronomical volumes of code — all legacy patched on legacy, with no
physical or mathematical anchor underneath. Abstractions pile up unanchored and get wasted.
Same gap as the grounding-layers work.

## Reduction thesis

Control flow and logic (conditionals, either/or, gates — Boolean algebra) reduce cleanly to a
physical cost floor. **Logic transfers across languages; conventions do not, and conventions
are roughly 90% of the legacy sludge.**

Names reduce to role in the binding graph: who writes, who reads, lifetime, invariant held.
Held as a 3-4D object (flow / constraint / time / purpose), not a 2D graph — a name is a
low-dimensional projection of a higher-dimensional purpose-object.

## Key insight

Most of what a name smuggles is not intent but QUANTITY-TYPE. A constraint is a constraint in
physics or in code — water can be dry, none, or flood, but not negative. **Type the cell as a
physics quantity and its constraints fall out for free.**

## Next artifact — the quantity-type taxonomy

A small finite physics vocabulary: extensive/intensive, conserved or not, floor/ceiling, sign,
transfer semantics. This is the anchor the whole recycling thesis hangs on.

Residue after typing is pure social convention (zip code) — small; mark as convention and move
on.

## Interpreter audit — findings for rework

- **No system boundary.** The `fields` dict has no reservoir, sink, or global ledger, so
  conservation is unstatable. `EnergyState.conserved_with()` and `.entropy_increased()` exist
  but are never called by any operator.
- **Source-from-nothing ops:** `regenerate` (input debited from nobody, then multiplied by
  1+bonus); `resonate_with` (+20% both fields, entropy frozen, coherence unbounded despite the
  README's [0,1] claim); `fractal_spawn` (children sum to parent E but the parent is not
  debited, so system E and S both double).
- **Undeclared sinks:** `decay`, `phase_transition` — entropy sign also wrong, since ordering
  raises S with no environment to export to. The K+P=E invariant is broken at field creation
  and never reconciled.
- `symbiosis_with` mutates in place; every other op returns new objects.
- **Proposed fix:** a single Reservoir node plus a Delta contract. Every op returns
  `field_deltas` plus `reservoir_delta`; the ledger asserts sum(dE)=0 and sum(dS)>=0. This
  converts every violation into an explicit source term. The ledger-first rewrite is roughly a
  weekend; the hard part is repurpose semantics.
- README overclaims verified / tested / "100% compliant" / "[0,1]" for properties the code does
  not check and in three cases breaks — the same failure mode the calibration-audit work
  documents.
- **The COBOL bridge is the genuinely strong idea and goes unmentioned in the README:** PIC
  clauses as energy-precision constraints, with `_enforce_constraints` clamping after each op.
  Clamping is currently a silent unlogged energy sink.

## Repo hygiene blockers

- Two interpreter files differing only in case — will not clone cleanly on case-insensitive
  filesystems
- README quick-start imports a third spelling; the documented entry point does not exist
- README ships a sandbox path
- README doc names do not match repo doc names
- LICENSE is MIT; the rest of the ecosystem is CC0 — convention break
- A translation-table filename typo; an unreferenced file in tree
