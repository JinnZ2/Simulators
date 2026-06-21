# Sample outputs

Committed artifacts from the two demos in this folder.

- `demo.sample.txt` — `python3 continuity_audit.py`. Three scenarios
  (consolidation `g=+1.0`, neutral `g=0.0`, diversifying `g=-1.0`)
  on a six-type starting distribution, audited against three reference
  agents (AI_model κ=0.95, institution κ=0.55, biology κ=0.35).
- `interface_layer.sample.txt` — `python3 interface_layer.py`. Same
  flooded agent (affinity `[2.0, 1.0, 0.0]`, `stress=0.85`,
  target=2) run under two strategies: `naive_target` (rigid) and
  `translator` (meet-then-lead). The rigid strategy drives stress
  to 1.0 and locks κ at ~0.99 (`COERCIVE`); the translator walks
  stress down to ~0.26 and drops κ from 0.89 to 0.33 over 14
  steps (`ENABLING`, band Δ = +1.12). The empirical signature of
  "lower your voice once they've lowered theirs."

The consolidation column flags `AI_model` `INCOHERENT`: a high-κ
agent pursuing a continuity-degrading incentive structure registers
as self-sabotage by the module's definition. The diversifying column
saturates: the starting distribution is already well above the
resilience floor, so `dC/dt` lands inside the `eps` band and the
verdict reads `INDETERMINATE` rather than `SUPPORTS_CONTINUITY` — an
honest reading of the live data, not a softened conclusion.
