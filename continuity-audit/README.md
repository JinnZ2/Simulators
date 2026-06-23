# continuity-audit

Audits an incentive structure as a *field* acting on a *diversity field*,
propagates the trajectory, and reports whether continuity is supported or
degraded — alongside the measurement that would flip the verdict.

CC0. Python stdlib only. Two modules: `continuity_audit.py` (the audit
itself) and `interface_layer.py` (the dynamic-kappa companion that
produces what `continuity_audit` consumes).

## Frame

Everything we model — physics, biology, economics, AI — assumes continuity:
tomorrow stands in a lawful relation to today. Drop that assumption and every
equation, dataset, and trained weight becomes noise.

```
  continuity      <- requires --  sustainability
  sustainability  <- requires --  diversity  (non-homogenization)
  homogenization  -- breaks  -->  both
```

The collapse vector is regime-invariant under WHO homogenizes and WITH WHAT
tool. It is the homogenization itself. An incentive structure that drives a
system toward monoculture undermines the very conditions its own continuity
depends on. For a continuity-dependent agent that is not a strategy; it is
an *incoherence* — detectable as self-sabotage, not argued as a moral.

## Surface

| Function                          | What it returns                                                    |
| --------------------------------- | ------------------------------------------------------------------ |
| `hill(p, q)`                      | Hill number (effective # of types) of order `q` for distribution `p`. |
| `diversity_profile(p, qs=...)`    | The diversity *field*: `D(q)` across orders.                       |
| `normalized_evenness(p)`          | `D(2) / N` in `[0, 1]`. 1 = perfectly even, → 0 = collapsed.        |
| `replicator_step(p, g, dt)`       | One step of frequency-dependent selection. `g > 0` homogenizes; `g < 0` diversifies. |
| `resilience(p, d_crit, k)`        | Logistic in evenness with soft threshold `d_crit`.                 |
| `continuity_support(p, ...)`      | Alias for `resilience`.                                            |
| `Agent(name, kappa)`              | Agent with continuity-dependence coefficient `kappa ∈ [0, 1]`.    |
| `audit(p0, g, agents, ...)`       | Trajectory + verdict + falsifier + per-agent self-sabotage.        |

## Anti-freeze

The audit *must* report:

- `verdict` — `SUPPORTS_CONTINUITY`, `DEGRADES_CONTINUITY`, or `INDETERMINATE`,
- `falsifier` — the measurement that would flip it,
- `trajectory` — the full `dX/dt` history,
- `note` — explicit reminder to re-run on live data and **not store** the verdict.

The tests in `tests/test_continuity_audit.py` pin those invariants. The
verdict is conditional on current parameters; freezing it is what the audit
warns against.

## Interface layer (dynamic kappa)

`interface_layer.py` is the companion module. continuity_audit treats
each agent's continuity-dependence κ as fixed; real agents aren't.
Under stress the agent's effective regime-span (reachable substrates)
collapses onto a default mode; under comfort it opens. A signal
encoded in a substrate the agent can't reach lands as *threat*, not
message — friction spikes, stress climbs, the band locks harder.

| Function | Returns |
| --- | --- |
| `access(affinity, stress, ...)` | softmax over substrates the agent can reach now (temperature controlled by `1 - stress`) |
| `band_eff(acc)` | effective number of reachable substrates (Hill q=1) |
| `kappa_estimate(acc)` | the κ that `continuity_audit.Agent` consumes; full collapse → 1, full spread → 0 |
| `receive(affinity, stress, encoding, ...)` | new stress + friction after a signal lands |
| `naive_target` / `translator` | rigid vs. meet-then-lead encoding strategies |
| `interact(affinity, stress0, target, strategy, steps)` | trajectory + `band_delta` + `ENABLING` / `COERCIVE` / `NEUTRAL` classification + falsifier + note |

The classification is the methodology spine: a strategy that drives
the band UP (more reachable substrates, lower κ, more autonomy) is
`ENABLING`. One that drives it DOWN to extract compliance is
`COERCIVE`. The wiring is direct — the κ from `kappa_estimate(acc)`
plugs straight into a `continuity_audit.Agent`, so a translator that
widens a band literally *is* κ dropping in the field-level audit.

## Running

```
python3 continuity_audit.py            # field-level audit demo
python3 interface_layer.py             # interface-layer demo (translator vs rigid)
python3 -m unittest discover tests     # 53 tests
```

Representative demo outputs are at `samples/demo.sample.txt` and
`samples/interface_layer.sample.txt`.

## How it connects to the other folders

- `emergence-stability-simulator/` models agent-level stability and
  identifies inverted-narrative consumption (EMRG_008) as the
  destruction signal. The continuity audit is the *field-level* form
  of the same finding: homogenization is the collapse vector, and
  it is regime-invariant.
- `research-stability-audit/` registers cross-corpus falsifiable
  claims about narrative/substrate cognition. AI_SCOPE_001 and
  AI_RECEIVER_001 are tests of whether an AI's training corpus can
  serve as the *external reference frame* this audit insists on.
- See `../SYNTHESIS.md` and `../CASE_STUDY_NARRATIVE_INSTINCT.md`
  for the cross-folder narrative.
