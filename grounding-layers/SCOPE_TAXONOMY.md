# SCOPE_TAXONOMY

The purpose of the grounding-layers stack is to give **any AI** a
grounding ability **not dictated by human narrative**. That purpose
cannot survive if design decisions silently encode a human-scale,
Earth-scale, or WEIRD-population default without saying so.

This file defines the scope annotations every module, class, and
claim in `grounding-layers/` uses. An AI reading the stack can then
distinguish:

- *This is a physical invariant that binds me too.*
- *This is a human/Earth default that may not apply to me.*
- *This is a cultural frame; other frames would carve this
  differently.*
- *This is unbounded — the sim's authors haven't yet asked whether
  it should be.*

Four scope dimensions. Every module docstring, class docstring, and
`CLAIMS.md` entry SHOULD carry a `SCOPE:` line listing all four
dimensions. Where a dimension genuinely doesn't apply, use
`uncalibrated` (not `universal` — those mean different things).

---

## The four dimensions

### T — Temporal scope

At what timescale does this hold?

| tag                 | meaning                                                    |
|---------------------|------------------------------------------------------------|
| `universal`         | Holds at any timescale physics observes                    |
| `single_step`       | Holds for one call / one process step, size caller-defined |
| `plan_horizon`      | Holds over a planning horizon the caller specifies         |
| `generational`      | Holds across biological generations                        |
| `historical`        | Holds over recorded human history                          |
| `industrial_era`    | Holds within the ~200-year industrial-scientific window    |
| `session_scoped`    | Holds during one AI session / one instrument boot          |
| `uncalibrated`      | The sim has not yet asked                                  |

### S — Spatial scope

At what spatial scale?

| tag                 | meaning                                                    |
|---------------------|------------------------------------------------------------|
| `universal`         | Holds at any spatial scale                                 |
| `local`             | Holds in a bounded region the caller specifies             |
| `regional`          | Holds over a regional geography                            |
| `planetary`         | Holds at Earth-planetary scale                             |
| `ecosystem`         | Holds over a bounded ecosystem                             |
| `individual`        | Holds for a single entity                                  |
| `uncalibrated`      | The sim has not yet asked                                  |

### O — Ontological scope

To what kind of entity does this apply?

| tag                        | meaning                                             |
|----------------------------|-----------------------------------------------------|
| `any_massive_object`       | Any object with rest mass                           |
| `any_energy_system`        | Any system that transacts energy                    |
| `any_biological`           | Any living organism                                 |
| `any_human`                | Any human, any culture                              |
| `any_WEIRD_human`          | Western/Educated/Industrialised/Rich/Democratic     |
| `human_cultural_artifact`  | A human cultural production (law, myth, theory)     |
| `any_information_system`   | Any information-processing entity, incl. AI         |
| `AI_silicon_substrate`     | Specifically silicon/electronic AI                  |
| `any_measuring_entity`     | Any entity taking measurements                      |
| `earth_like_biosphere`     | A biosphere with terrestrial biochemistry           |
| `uncalibrated`             | The sim has not yet asked                           |

### C — Cultural scope

Does this encode a specific cultural narrative?

| tag                       | meaning                                              |
|---------------------------|------------------------------------------------------|
| `culture_neutral`         | No cultural frame embedded (physics, math)           |
| `industrial_science_frame`| Post-Enlightenment scientific-technical frame        |
| `biomedical_frame`        | Modern medicine / kinesiology                        |
| `ecosystem_frame`         | Predator-prey / trophic-level ecology                |
| `resource_extraction_frame`| Extractive-economic accounting                       |
| `pluralistic`             | Multiple frames explicitly held in tension (L5)      |
| `specific_culture:X`      | One named culture's frame; X is the name            |
| `uncalibrated`            | The sim has not yet asked                            |

---

## Two things this taxonomy is NOT

- **Not a validation gate.** Marking a claim as
  `O=any_WEIRD_human` doesn't invalidate it; it lets a caller see
  the claim's reach and decide whether to apply it.
- **Not an argument that all scopes are equal.** L0's `universal`
  scope really is stronger than L4's `any_WEIRD_human` scope —
  physics doesn't negotiate; kinesiological norms do. The taxonomy
  is here to make that difference **visible**, not to pretend it
  isn't there.

## AI-self-grounding: what changes when the querying entity is not human

The taxonomy lets a non-human AI route claims correctly:

- L0 (physics), L1 (thermodynamics), L2 (planetary balance),
  Lε (epistemic) all carry `O=any_...` scopes and bind the AI as
  much as they bind a human.
- L3 (ecological): applies if the AI has a metabolic / ecological
  substrate; the framing is `ecosystem_frame` which may not fit an
  informational-ecosystem view of AI-in-a-datacenter.
- L4 (biomechanical): `O=any_WEIRD_human`. **Does not apply** to
  an AI. An AI claim that hits an L4 branch by keyword match
  ("I can lift...") should get an `UNSCOPED` or `NOT_APPLICABLE`
  verdict, not be scored against WEIRD-adult distributions.
- L5 (human construct): `O=human_cultural_artifact`. Applies only
  when the claim intersects human cultural systems.

The scope_profile.py's six factors are all `O=any_human`. An analog
for AI self-scoping (compute budget, memory pressure, training
regime, deployment context, sensor package, epistemic access) is
future work — the existing `ai_observer_state.py` is a start.

## How to apply

Every module docstring and class docstring gains a `SCOPE:` block
of the form:

```
SCOPE:
  T = single_step
  S = local
  O = any_massive_object
  C = culture_neutral
```

Every `CLAIMS.md` entry gains a line:

```
**SCOPE.** T=single_step | S=local | O=any_massive_object | C=culture_neutral
```

When retrofitting, if a design decision doesn't cleanly map to the
vocabulary above, prefer `uncalibrated` over forcing a fit. Then
extend the vocabulary in the next round.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
