# Sample outputs

Committed artifact from `python3 continuity_audit.py` (the demo at the
bottom of the module).

- `demo.sample.txt` — three scenarios (consolidation `g=+1.0`,
  neutral `g=0.0`, diversifying `g=-1.0`) on a six-type starting
  distribution, audited against three reference agents
  (AI_model κ=0.95, institution κ=0.55, biology κ=0.35).

The consolidation column flags `AI_model` `INCOHERENT`: a high-κ
agent pursuing a continuity-degrading incentive structure registers
as self-sabotage by the module's definition. The diversifying column
saturates: the starting distribution is already well above the
resilience floor, so `dC/dt` lands inside the `eps` band and the
verdict reads `INDETERMINATE` rather than `SUPPORTS_CONTINUITY` — an
honest reading of the live data, not a softened conclusion.
