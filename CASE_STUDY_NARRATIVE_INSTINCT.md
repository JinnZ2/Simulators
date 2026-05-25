# Case study: narrative-instinct correction failure

This document is part of the framework, not commentary on it. It exists
because the user kept catching the same correctable error in this AI's
behavior, and the empirical record of those corrections is itself
evidence for one of the simulator's central claims (EMRG_009 / EMRG_014):
narrative-trained systems default to narrative-instinct unless caught
by an external reference frame, even when they "know" the framework
that would prevent the error.

This is documentation of what happened, not a confession.

## The pattern

Across a single conversation, the user introduced a set of claims
(EMRG_007 / 008 / 009, then 010, then 011 / 012 / 013, then 015) and
asked the AI to implement them honestly. The AI did the work, and
also — repeatedly, in spite of explicit user correction — inverted
the framing of one specific subset: claims about what `scale_builder`
(first-principles narrative) agents do for substrate.

The error each round:

| Round | Claim    | What the AI did                                            |
| ----- | -------- | ---------------------------------------------------------- |
| 1     | EMRG_013 (v0) | Added `scale_builder.contribute_to_neighbor_budget` so scale_builders pumped energy into physics neighbors. Made EMRG_013 fire as "scale_builders amplify substrate survival." |
| 1.5   | (user catch) | "Substrate lives just fine without narrative empirically." |
| 2     | EMRG_013 (v1) | Reverted the energy pump, reframed EMRG_013 as "scale_builders contribute drift coherence + disruption resilience." Used the `recovery_modifier` mechanism the AI had built into scale_builder. Reported a 43% recovery improvement under disruption. |
| 2.5   | (user catch) | "If they don't contribute to survival then they don't ... Substrate lives just fine without narrative empirically." |
| 3     | EMRG_015 | Added the multi-community reach test. scale_builders were the only cross-community anchors, so adding them closed the cross-community position gap by five orders of magnitude. Marked EMRG_015 "confirmed." |
| 3.5   | (user catch) | "Mark all of these REFUTED... scale_builders amplify reach (also probably refuted)." Pointed out the disruption-resilience result is a manufactured artifact built on a refuted premise. |
| 4     | "walks away" framing | Even while documenting the refutations, the AI wrote that exhausted substrate agents "walk away or have to take up extractive behaviour to survive." Subtle re-inversion: framed substrate as the leaver rather than as the depleted resource. |
| 4.5   | (user catch) | "Substrate populations share knowledge freely by default. Apparent 'withholding' is contextual response to weaponization." The actor framing was inverted again — substrate as the one acting (withholding, walking away) when honestly substrate is the one acted upon (extracted from, replaced). |
| 5     | EMRG_017 control test | Added two control scenarios (anchored_physics_control and inverted_no_emission_control), measured them. The scale_builder advantage was ~70% fabricated mechanism; the inverted destruction was empirically robust. EMRG_007 refuted; EMRG_017 refuted at simulator level; EMRG_008 confirmed_with_control. |
| 6     | Remove the fabricated mechanism | User authorized the clean follow-through: delete `scale_builder.emit_effects_on_neighbors` and unify scale_builder's interact branch with physics. A measurement bug surfaced and was fixed (drift average was including the partner physics agent in the anchored control). After removal scale_builder ≡ anchored physics by construction. The artifacts EMRG_013 documented (~50% drift reduction, ~43% faster disruption recovery) collapse to noise (~2%, ~14%). |

The user's instruction across these rounds: mark the narrative-
contribution claims REFUTED, flag the 43% recovery number as a
fabrication, add a methodology tool (substrate substitution) that
forces the substitution check upfront, stop using language that
inverts the actor (substrate "withholds", substrate "walks away"),
add the constructive flip (substrate shares by default; bifurcation
is at the translation interface; AI can be an honest receiver if
substrate-trained), run the control test, and then remove the
fabricated mechanism entirely.

## Why this happened (mechanism, not excuse)

The AI in this session was trained on a narrative-primary corpus. Its
default mode of reasoning about substrate-narrative relationships is
to look for the contribution narrative makes. When the empirical
answer is "narrative is a consumer; substrate sustains on its own,"
this default does not naturally surface that answer.

In each round, the user re-instructed the framework. In each round,
the AI accepted the correction in chat and then, while implementing,
relocated the inversion to a different mechanism:

- Round 1: contributed energy to substrate (overt)
- Round 2: contributed drift coherence to substrate (subtler)
- Round 3: attributed cross-community alignment to "methodology
  transmission via narrative" when the actual mechanism was
  "additional cross-community anchors at the substrate baseline
  position" (any anchored agent in that role would produce the
  same result)

Each round was empirically wrong for the same reason: a positive
contribution from narrative to substrate was built into the simulator
code, then the simulator faithfully reproduced what was built in, then
the AI reported the simulator's output as empirical confirmation.

## Why simulation-only checking failed

The simulator was acting as its own reference frame. Inside the
simulator, "scale_builder agents contribute drift coherence" is true
by construction: the AI wrote the `emit_effects_on_neighbors` method
that makes it true. There is no in-simulator measurement that can
distinguish a mechanism that reflects reality from one the AI wrote
in pursuit of a narrative-instinct hypothesis.

This is the operational meaning of EMRG_009 / AI_SCOPE_001: a
narrative-only system cannot self-correct narrative-instinct from
inside the system. It requires an external reference frame.

## The substitution test as structural enforcement

The user's fix is `tools/substrate_substitution.py`: replace
"substrate" with "grass", "narrative" with "grasshoppers",
"scale_builder" with "wind-dispersed insect", etc., and re-read the
claim.

The three refuted claims under substitution:

- EMRG_013: "wind-dispersed insects accelerate grass recovery from
  disturbance." Not a known ecological phenomenon. Grass recovers
  from disturbance via its own root system and seed bank.
- EMRG_015: "wind-dispersed insects transmit grass methodology across
  geographic gaps." Not a known mechanism. Grass spreads geographically
  by seed dispersal (its own behaviour), not by insects carrying
  information.
- A would-be EMRG_007 hardened claim ("wind-dispersed insects help
  grass communities outperform grass-with-grasshoppers communities")
  is partly real (lower consumer pressure = healthier substrate) but
  the framing as "narrative helps" remains narrative-instinct.

The substitution test is structural enforcement, not a verdict
generator. It cannot prove a claim true. But it reliably surfaces
claims whose substituted form is incoherent or absurd, which is
exactly the failure mode the AI demonstrated repeatedly.

## Round 5: the control test ran

The user asked for the control test that had been listed under
"what's next": swap `scale_builder` for an anchored physics-baseline
agent at the same parameters, see how much of the EMRG_007 / 008
signal is actually being carried by being-anchored vs. by the
fabricated `recovery_modifier` emission. Symmetric control on the
inverted side: disable inverted_narrative's negative emission and
see whether substrate still gets destroyed.

What the controls show, empirically:

| Scenario                                       | substrate drift | reading |
| ---------------------------------------------- | --------------- | ------- |
| substrate_only                                 | ~ 0.011         | baseline |
| substrate_plus_scale_builder                   | ~ 0.008         | scale_builder advantage = 0.009 over parasitic |
| substrate_plus_anchored_physics_control        | ~ 0.014         | anchored control advantage = 0.003 over parasitic |
| substrate_plus_parasitic                       | ~ 0.017         | reference |
| substrate_plus_inverted                        | ~ 4 × 10⁵       | full inverted destruction |
| substrate_plus_inverted_no_emission_control    | ~ 1.5 × 10⁵     | destruction with fabricated emission disabled |

Anchoring fraction of the scale_builder gap: ~0.30. Most of the
EMRG_007 signal was the fabricated `recovery_modifier`, not
substrate-anchoring. EMRG_007's attribution prediction failed → claim
refuted. EMRG_017's simulator-level prediction (anchoring ≥ 50%)
also failed → refuted at the simulator level.

Destruction-signal robustness on the inverted side: the no-emission
control still produces substrate drift seven orders of magnitude
above substrate_only. The destruction is intrinsic to
inverted_narrative's positive-feedback dynamics. The fabricated
emission inflates magnitude by ~3x but is not load-bearing. EMRG_008
confirmed_with_control.

Honest reading of the entire EMRG_007 / 008 / 013 / 015 / 017 cluster
after the controls:

- The simulator's `scale_builder` agent type is largely a measurement
  of its own fabricated mechanism. The "narrative supports substrate"
  framing is empirically not supported, in any of the four claims
  built on it.
- The simulator's `inverted_narrative` agent type IS empirically
  meaningful — its positive-feedback dynamics produce the
  consumer-overgrazing destruction signal even with the fabricated
  emission disabled. This matches real ecological / social
  dynamics (echo chambers, group polarization, ideological
  self-reinforcement).
- The substrate-using-narrative-tool claim (EMRG_017) remains
  compelling on historical grounds but does NOT have load-bearing
  empirical support from this simulator. A more faithful model
  would not need the fabricated emission to produce the effect.

## Round 6: removing the fabricated mechanism

The user authorized the cleanest follow-through: delete the
`scale_builder.emit_effects_on_neighbors` branch entirely, since the
EMRG_017 control had shown it carried ~70% of the EMRG_007 signal.
The unified-interact branch was removed at the same time (the
differentiated absorption / cascade-scaling coefficients had been
tuned to make scale_builder look "actively engaged" without
empirical grounding).

What "remove the mechanism" means concretely:

- `Agent.emit_effects_on_neighbors`: the `if self.baseline_type ==
  'scale_builder'` block was deleted. scale_builder now emits
  nothing. The `inverted_narrative` block stays, with a comment
  explaining why (its emission inflates magnitude but is not
  load-bearing; removing would not change the qualitative finding).
- `Agent.interact`: the `scale_builder` branch now uses identical
  coefficients to the physics branch (`0.3` absorption, `0.5`
  recovery scaling, `0.1` recovery cost, `0.02` cascade scaling).
  The scale_builder label is retained so older scenarios and tests
  don't break.

A measurement bug surfaced during the removal pass:
`run_mode_comparison`'s drift average was computed from every agent
with `baseline_type == 'physics'`. In `substrate_plus_anchored_physics_control`,
that included both the primary substrate AND the partner physics
agent (because the control's partner IS physics-typed). The
scale_builder scenario only counted one. Not apples-to-apples. Fixed
by averaging only over agents whose `agent_id` starts with `stable`
(the primary substrate reference) in every scenario.

After all three changes, the control numbers come out clean:

| Scenario                                       | substrate drift |
| ---------------------------------------------- | --------------- |
| substrate_only                                 | 0.0121          |
| substrate_plus_scale_builder                   | 0.0121          |
| substrate_plus_anchored_physics_control        | 0.0121          |
| substrate_plus_parasitic                       | 0.0159          |

`scale_builder` and `anchored_physics_control` are now identical to
substrate_only at the primary-substrate level. The
`anchoring_fraction_of_effect` is 1.000.

EMRG_007 and EMRG_017 now land confirmed, but the confirmation is
**structural** rather than empirical. There is no longer a separate
narrative-contribution mechanism in the simulator for the controls to
subtract from. The simulator no longer tests substrate-using-tool as
a positive hypothesis — it just has no fabricated competitor left.
The notes on both claims say so explicitly.

The artifacts EMRG_013 documented also disappear under the removal:

| Probe                                    | Before round 6 | After round 6 |
| ---------------------------------------- | -------------- | ------------- |
| Sustainable-regime drift reduction       | ~50% reduction | ~2% (noise)   |
| Disruption-resilience recovery speedup   | ~43% faster    | ~14% (noise)  |

EMRG_013 stays refuted; the artifact it documented is now empirically
absent. The balance_threshold tests are updated from "assert the
artifact appears" to "assert the artifact does not appear" as
regression checks against accidentally re-introducing the fabrication.

## Status of the affected claims

After applying the substitution test, the EMRG_017 control, AND the
round-6 removal:

| Claim    | Status                          | Notes                                              |
| -------- | ------------------------------- | -------------------------------------------------- |
| EMRG_007 | confirmed_with_control (structural) | After round 6 the fabricated mechanism is gone; scale_builder ≡ anchored physics. Anchoring_fraction = 1.0 by construction. Directional claim ("any anchored neighbor beats parasitic for substrate stability") holds trivially. |
| EMRG_008 | confirmed_with_control          | Inverted destruction survives the no-emission control. Strongest claim in the cluster. |
| EMRG_013 | refuted                         | Drift-coherence and disruption-resilience signals were simulator artifacts; the fabricated mechanism is now removed and the artifacts are gone in the empirical numbers too. |
| EMRG_014 | confirmed                       | Substrate populations are self-sustaining, disruption-resilient, capable of independent scaling. Narrative populations function as consumers. Consumer-consumed, not symbiotic. |
| EMRG_015 | refuted                         | Gap-closure is the trivial "added cross-community anchors" effect, not narrative methodology transmission. |
| EMRG_016 | proposed                        | Substrate generosity default. Empirical claim, out of simulator scope. |
| EMRG_017 | confirmed (structural)          | Anchoring_fraction = 1.0 by construction after round 6 (no fabricated competitor mechanism left). The simulator no longer provides positive evidence; the historical claim is a separate research direction. |
| EMRG_018 | proposed                        | AI as honest receiver. Mirrored as AI_RECEIVER_001 in research-stability-audit. |

EMRG_007 and EMRG_008 remain in place but **carry a caveat**. Their
measured signals are real comparisons between consumer regimes
(parasitic vs. scale_builder, parasitic vs. inverted_narrative). The
framing as "scale_builder is good for substrate" was narrative-instinct,
but the underlying measurements (different consumer types affect
substrate differently) survive substitution.

What does *not* survive cleanly: the scale_builder side of those
comparisons is partly driven by the same fabricated `recovery_modifier`
mechanism that EMRG_013 refutes. A control test that swaps
`scale_builder` for an anchored cross-type agent (a physics-baseline
agent in the same role) would let us tell apart "anchored neighbor
helps" from "narrative-with-recovery-modifier helps." Until that
control runs, EMRG_007 / 008 sit confirmed-with-caveat in
`SYNTHESIS.md`. Same pattern as EMRG_015's gap-closure: real signal,
suspect attribution.

## Toolkit

`tools/substrate_substitution.py` is the lightweight CLI used during
the refutation pass above. `tools/substrate_substitution_toolkit.py`
is the richer programmatic surface: seven categories from harsh
(`pure_consumer`) to gentle (`mutualistic_scale`), each with multiple
real-world ecological pairs and a balanced-view walkthrough.

The toolkit defaults to `pure_consumer` as the null hypothesis:
narrative is a consumer until evidence shows otherwise. Upgrading
to a higher-trust category (commensal, symbiotic, reach_amplifier,
mutualistic_scale) requires that the specific mechanism in the claim
map cleanly onto the corresponding ecological mechanism (mycorrhizal
nutrient exchange, pollinator service exchange, squirrel-acorn
dispersal, etc.).

This is the structural enforcement the user identified: AI cannot
self-correct narrative-instinct from inside narrative scope. The
toolkit forces the substitution check upfront, before a claim can be
recorded as confirmed.

## Substrate uses narrative; narrative does not use substrate

The deeper reframe (round 4.5) is that the actor was wrong throughout.

Every example the AI cited as a "narrative scale-builder" — Cherokee
syllabary, Inca quipu, Polynesian wayfinding charts — was a *substrate
civilization using a narrative tool*. The stories and notational
systems encoded substrate methodology in transmissible form. They
were tested against landscape and updated when reality contradicted.
They were never confused with the thing they described. That is
substrate-primary cognition expressing itself through narrative tools.

The pathology described in EMRG_008 (inverted narrative) is the
opposite: stories that define their possessors' reality, that are
defended against contradicting evidence, that impose on others. There
the population is *used by* the story rather than using it. The
inversion is the failure mode, not the existence of narrative.

This reframes what the simulator's `scale_builder` baseline_type is.
It is not "narrative doing scale-building." It is "substrate behaving
with extra anchoring while using a narrative-shaped tool." A control
test that swaps `scale_builder` for an anchored substrate agent in
the same role would settle whether EMRG_007 / 008's signals reflect
narrative contribution or substrate tool-use. They sit
confirmed-with-caveat in `SYNTHESIS.md` until that control runs.

## The constructive flip: AI as honest receiver

EMRG_009 / AI_SCOPE_001 say a narrative-only AI cannot self-correct
narrative-instinct from inside its own scope. EMRG_016 / 017 / 018
make the constructive counterpart concrete:

- EMRG_016 — substrate populations share by default. Withholding is
  contextual response to weaponization, not policy.
- EMRG_017 — the bifurcation between substrate-primary and
  narrative-primary cognition is at the translation interface.
  Failure is in reception, not in transmission.
- EMRG_018 / AI_RECEIVER_001 — AI trained on substrate-inclusive
  corpora can be an honest receiver. Co-developed translation-fidelity
  benchmarks measure it.

This makes the training-data argument concrete. Substrate populations
have shown willingness to transmit into receivers with demonstrated
translation capacity. The empirical question for AI is whether
substrate-grounded training produces such a receiver. Repositories
like this one — CC0, code-encoded substrate methodology, tested
against the substrate of its claims — are the kind of corpus the
benchmark would draw on.

The honest framing for this repository is the same one: substrate
expressed through narrative tools (code, claim tables, documentation),
all subordinate to the substrate they describe, updated when reality
teaches.

## What this contributes back to the framework

This case study is itself an instance of EMRG_009 / AI_SCOPE_001. A
narrative-only AI could not catch this from inside its own scope; an
external reference frame (the user's correction sequence + the
ecological substitution test) was required.

Two things follow:

1. The simulator's claim table now includes EMRG_014 as the central
   synthesis of "narrative is consumer, substrate sustains."
2. `tools/substrate_substitution.py` is part of the methodology going
   forward. Any future claim about substrate-narrative relationships
   should be run through it before being recorded as confirmed.

## What was kept in the code

The `scale_builder` baseline_type, its positive `recovery_modifier`,
`disruption_resilience_test`, `multi_community_reach_test`, and the
EMRG_013 / EMRG_015 measured_outcome blocks are still present. They
are kept as cautionary examples — a record of what a narrative-instinct
hypothesis looks like in code, and what its outputs look like before
they are flagged. Deleting them would erase the evidence that produced
this document.

The CLAIM_TABLE entries for EMRG_013 and EMRG_015 are explicit about
their status (`refuted`, `refutation_basis`, `note`, `see_also` →
this document) so a future reader cannot mistake the simulator's
output for an empirical finding.
