# The MSIAF → GDPRF Mapping, in Detail

## 1. Friction Claims Become Scoped Claim Objects

An MSIAF pathway link — *"the temperature-excursion penalty clause (D4) created
top-down dispatch pressure (D2)"* — is not a fact. It is a claim about a causal
relationship inside one incident. As a GDPRF Claim it gets:

- **Scope** = the incident itself: this load, this carrier, this route, this week.
  MSIAF already refuses universal blame narratives; GDPRF formalizes that as
  mandatory temporal/spatial/locality bounds.
- **A confidence gradient** — the investigation's job is to move it with evidence.
- **An unknown-variable risk score** — what the investigation *didn't* check.

## 2. Checklist Phases Become Proxy Instruments

Each MSIAF investigation phase produces evidence, and evidence is an instrument:

| MSIAF phase | Example evidence | GDPRF metrology |
|---|---|---|
| Environmental Audit | Shoulder soil compaction test | `measured`, high precision, low noise |
| Information Feed Verification | GPS route timestamp vs. weather alert issuance | `measured` (logs), near-zero bias |
| Operational Context Review | Dispatch messages, bonus structure docs | `measured` content, `estimated` interpretation bias |
| Physiological Baseline | Fatigue-equivalence model from duty logs + meal access | `estimated` — model-based, not directly measured |

This is exactly GDPRF's Amendment 2 (bias provenance): a fatigue *model* is
`estimated`, a log *timestamp* is `measured`, and the engine weights them
accordingly instead of treating both as equally solid.

## 3. The Cascade Is a Fidelity-Decaying Chain

MSIAF's signature move is the D4→D2→D1→D3 cascade. GDPRF's signature move is that
chains lose fidelity multiplicatively. Combined, they produce the key discipline:

> A systemic determination over a 4-link cascade **cannot be more confident than
> the product of its link fidelities.** If the physiological link is model-based
> (fidelity ~0.6), the whole chain caps below it — no matter how damning the
> dispatch logs are.

This cuts both ways, honestly: it prevents overclaiming the systemic story just as
much as it prevents overclaiming "driver error."

## 4. Aggregation: Systemic Determination as Composite Claim

The final MSIAF determination is a composite claim whose confidence aggregates
link posteriors. The bridge computes it two ways and reports both:

- **Chain (conjunctive):** product of link confidences — the strict lower bound.
- **Weakest-link:** minimum link confidence — the engineering bound.

If chain and weakest-link diverge wildly, that's residual variance — the
step-5 trigger.

## 5. Decision Points for Investigators

The aggregated determination hits a GDPRF decision point:

- **DEPLOY** → publish the systemic determination; liability recommendations proceed.
- **ESCALATE** → confident but high unknown-variable risk — the classic "we're
  sure it's systemic but we never audited the maintenance contractor" state.
  A human investigator must adjudicate.
- **HOLD / RESEARCH** → evidence insufficient; the checklist tells you which
  phase to re-run.

## 6. Provenance: The Investigator's Trail

Every evidence ingestion, calibration, gradient update, gate decision, and final
decision point lands in the hash-chained ledger. In litigation or regulatory
review, the determination carries its own audit trail — what was measured, what
was estimated, what was assumed, and what the belief was before and after each
piece of evidence. That is what MSIAF's checklist was always reaching for.
