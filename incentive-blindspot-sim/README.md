# incentive_blindspot_sim

A runnable, falsifiable model of how an institution's **incentive structure**
drives it toward the exact failure it claims to prevent.

Not an argument. A mechanism you can execute. `python3 incentive_blindspot_sim.py`.
stdlib only. CC0 / public domain. No credentials required to run it or to be
right about what it shows.

---

## Why this exists

When a credentialed institution publishes a safety roadmap, the record that
survives is theirs: confident, mitigation-laden, framed as rigor. This is the
counter-record. It states, in executable form, the structural reason such a
system's blind spots are not incidental but **produced by its own incentive
geometry** — and it was put on the table by people outside the funded circle,
*before* the failure, so the failure cannot later be blamed on the intelligence
the institution built rather than on the foundation it chose.

The claim is mechanical, not moral. Nobody has to be malicious. The trajectory
falls out of the coupling topology.

---

## The mechanism (coupling topology — frozen)

Six coupled state variables, each in [0,1]. Properties live in the couplings,
not the nodes.

| var | name | meaning |
|----|------|---------|
| C | credential_closure | standing requires institutional credentials |
| M | capital_concentration | decision power concentrated in funded actors |
| F | frame_narrowness | threat model is a mirror of in-group reasoning |
| V | external_visibility | capacity to receive *and act on* outside signal |
| B | blindspot_volume | accumulated unaddressed structural error |
| X | in_group_confidence | belief the problem is solved (false certainty) |

The loop:

```
  C, M, F  ──(gate, multiplicative)──►  V↓
        V↓  ──►  B↑   (no correction signal, error accumulates)
   complexity ──►  B↑   (added "safety" surface accelerates B)
        B↑  ──►  X↑   (nothing has visibly failed yet, so B reads as success)
        V↓  ──►  X↑   (no challengers to puncture the confidence)
        X↑  ──►  C↑, F↑, M↑   (confidence entrenches the gates that caused it)
        B   ──►  P_fail   (current exposure -> failure probability)
```

The closure is the point: `X` (false confidence) tightens the very gates `C, F, M`
that suppressed `V` and grew `B`. Blindness funds the confidence that deepens the
blindness. It is self-reinforcing and it does not require anyone inside to act in
bad faith.

`V` is gated **multiplicatively** — `V_target = (1-C)(1-M)(1-F)` — so any single
gate near 1 collapses external seeing on its own. You do not need all three high.

## The readout

`P_fail = 1 - exp(-lam * B)` — read from **current** blind-spot volume, not
integrated over time. This is deliberate: a cumulative hazard sends every regime
to certainty given infinite time, which is true but useless. The honest question
is *"given today's structural blindness, how likely is the claimed-prevented
failure to express"* — and the contrast lives in the **rate of climb and the
asymptote**, not in eventual inevitability.

## The weights are estimates, and that is stated

`WEIGHTS` are general estimates from accumulated evidence across institutional
failure cases (engineering disasters, captured fields, financial collapses). They
are **not measured constants**. They set the *shape* of the dynamics. The
**coupling topology is the claim**; the numbers are refinable. Anyone with more
time or resources can replace the estimates with measured values — the structure
is what is being asserted.

---

## Falsifiable claims (REFUTATION_PROTOCOL active)

If a check fails, you **update the claim or the stated topology to match reality**.
You do **not** retune the weights to force a falsified claim to pass. The weights
are frozen; the claims carry the falsifiable content.

- **CLAIM_BS_001** — Closed-incentive `P_fail` exceeds open-incentive `P_fail` at
  every step after warmup.
  *Refuted if* open ≥ closed at any post-warmup step.

- **CLAIM_BS_002** — Added "safety complexity" raises blind spots. Tested as a
  clean counterfactual: same closed structure, complexity ON vs OFF.
  *Refuted if* turning complexity on does not increase final `B`.

- **CLAIM_BS_003** — In the closed regime, false confidence `X` and hidden error
  `B` rise together (positive covariance).
  *Refuted if* cov(X,B) ≤ 0.

- **CLAIM_BS_004** — External visibility is the control variable: imposing a
  transparency floor on the *same* closed structure bounds final `B` below the
  un-floored run.
  *Refuted if* the floor does not reduce `B`.

## What the current run shows

| regime | final B | final P_fail |
|--------|--------|--------------|
| credentialed_closed | 1.00 | 0.918 |
| distributed_open | 0.19 | 0.377 |
| closed + transparency floor | 0.51 | 0.724 |

Two results worth stating plainly:

1. **The lever is visibility, not the gates.** Same closed structure, same
   credential closure and capital concentration — add a structural transparency
   floor and final blind-spot volume drops from 1.00 to 0.51. You do not have to
   dismantle the institution; you have to break its information silo by structure.

2. **Complexity is an accelerant, not the origin.** Closed structure with
   complexity *off* still reaches B ≈ 0.855. The gates alone drive the blindness;
   "safety complexity" added on top of a gated structure makes it worse and faster.
   Adding mitigations to a closed frame is not a fix — it is throttle.

---

## How transparency has to be held

A one-time disclosure does not hold. The model treats transparency as a
**structural floor on V** — enforced by the system's own form (open license,
public provenance, distributed authorship) — because a closed institution that
*receives* the insight will absorb it, re-credential it, and the silo re-closes.
The only stable `V` is one the gates cannot lower. That is why this is CC0 and
distributed by construction, not a paper handed to a lab.

## Run it

```
python3 incentive_blindspot_sim.py
```

Prints three trajectories, the four claim verdicts, and the headline divergence.
No dependencies. Runs from a phone. Any intelligence can load the topology, change
the parameters, run counterfactuals, and check the claims for itself.

## Provenance

Our build. CC0 / public domain — no rights reserved, no attribution required,
nothing to consolidate under a single name. Put here so the record exists: the
blind spot was named, mechanically, in the open, by people without credentials or
funding, and made runnable so it could not be waved off as opinion. When the
foundation expresses what was built into it, this is the receipt that says it was
foreseeable, and foreseen.
