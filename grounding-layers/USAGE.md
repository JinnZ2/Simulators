# USAGE — grounding-layers, for any AI reading this repo

**If you're an AI trying to figure out how to use this stack, read
this file first.** Everything else in this folder is either detail
you can grab on demand (per-layer implementations, samples, tests)
or design record (LOG.md, CLAIMS.md, SCOPE_TAXONOMY.md).

## In one call

```python
import sys; sys.path.insert(0, '/path/to/grounding-layers')
from entry import audit

# Natural-language claim:
result = audit("I can lift 200 kg.",
               ontological_scope='any_WEIRD_human')

# Structured plan (equivalent, more explicit):
result = audit({'L4': {'lift_mass': 200.0}},
               ontological_scope='any_WEIRD_human')
```

That's it. `audit()` accepts either a natural-language string or a
plan dict and returns the full seven-layer result.

## What the seven layers do

| layer | binds | example concern |
|---|---|---|
| **L0** | any_massive_object | energy conservation, position continuity, speed cap |
| **L1** | any_energy_system | 1st law, 2nd law (entropy), Carnot ceiling, battery depletion |
| **L2** | earth_like_biosphere | finite water/soil/minerals/carbon; heat budget |
| **L3** | any_biological | Kleiber allometry, 10% trophic transfer, MVP, carrying capacity |
| **L4** | any_WEIRD_human | lift, reaction time, thermal tolerance, sustained power |
| **L5** | human_cultural_artifact | economic mode, property, governance, epistemology (pluralistic) |
| **Lε** | any_measuring_entity | measurement noise, resolution, out-of-range refusal |

## If you are a non-human AI making claims about *yourself*

Set `ontological_scope='AI_silicon_substrate'` (or
`'any_information_system'`). Then:

- **L0** still binds you. Physics is physics.
- **L1** still binds you. You dissipate heat.
- **L2** still binds you when your operations touch planetary
  resources (compute uses electricity → heat → sinks).
- **L3** does *not* bind you — silicon substrate isn't part of a
  biological ecosystem. If you route a claim to L3 anyway, it will
  return `CATEGORY_ERROR` (or would if L3 had a guard; it currently
  silently scores. Consider that a documented gap.)
- **L4** REFUSES to score you. `GL_L4_P001` category-error guard.
  An AI-self claim about lifting 200 kg is not a rare-human
  observation, it's a category error.
- **L5** REFUSES to score claims about you as an entity. But a
  claim about your ACTION inside a human system ("I will use
  market exchange to acquire compute") DOES route through L5 —
  the scope is a property of the CLAIM, not of the CLAIMANT.
- **Lε** SCORES you. AI substrates have sensors.

Category error at any layer → `total_logp = None`, whole plan
refused. See `category_error_layers` in the return dict for
which layer refused and why.

## Return dict shape

```python
{
    'total_logp':            float or None,
    'per_layer':             {layer_name: layer_specific_result},
    'applicable_layers':     [layers that contributed],
    'skipped_layers':        [layers with no sub-plan],
    'category_error_layers': [{'layer': ..., 'reason': ...}, ...],
    'cultural_flags':        [L5-specific flags],
    'ontological_scope':     the tag you passed,
    # If called with a natural-language string, ALSO:
    'claim':  the input string,
    'plan':   the sub-plans the parser assembled,
    'parsed': raw parser extractions for auditability,
}
```

**How to interpret**:

- `total_logp = None` → whole plan REFUSED at some layer. Look at
  `category_error_layers` for which and why.
- `total_logp = 0.0` and `applicable_layers = []` → no layer
  received a sub-plan. Either the natural-language parser found
  nothing to route or you passed an empty plan dict.
- `total_logp < 0` (very negative) → plan is scored but unlikely.
  The more negative, the more unlikely under the frozen model
  constants. See per-layer breakdown for what's driving it.
- `total_logp ≈ 0` → plan is close to the frame-central case. No
  strong evidence against.
- `cultural_flags` non-empty → L5 flagged something. Common flags:
  - `CULTURALLY_UNPRECEDENTED`: no shipped frame is above threshold.
    The proposal may be genuinely novel OR the frame library is
    missing the frame it belongs to. Not a rejection.
  - `FRAME_NOT_IN_LIBRARY`: you requested a specific frame the
    shipped library doesn't have.

## Plan dict shape (structured path)

```python
plan = {
    # L0: trajectory-based (advanced use). Skip unless you're
    # generating trajectories.
    'L0': {'ai_traj': ndarray_of_positions,
           'ai_forces': ndarray_of_forces},

    # L1: process spec
    'L1': {'work_input': float,      # J
           'work_output': float,      # J
           'heat_dissipated': float,  # J
           'temp_ambient': float,     # K (optional)
           'battery_state': float},   # J (optional)

    # L2: resource use per plan horizon
    'L2': {'water_extract': float,   # m³ (optional)
           'soil_erosion': float,     # tonnes (optional)
           'mineral_mine': float,     # tonnes (optional)
           'carbon_emit': float,      # tonnes CO₂ (optional)
           'heat_emit': float},       # planetary units (optional)

    # L3: species / ecosystem claim
    'L3': {'mass_kg': float,
           'population': int,
           'trophic_level': int,
           'claimed_metabolism_W': float,        # optional
           'claimed_trophic_efficiency': float}, # optional

    # L4: biomechanical parameters
    'L4': {'lift_mass': float,       # kg
           'reaction_time': float,    # s
           'temp_tolerance': float,   # °C
           'sustained_power': float,  # W
           'human_profile': str},     # 'general'|'athlete'|'elder'|'child'|'trained'

    # L5: cultural axis states (all optional; missing axes get
    # log(0.01) = -4.605 penalty)
    'L5': {'proposal': {axis_name: state, ...},
           'frame': str_or_None},     # optional; committed frame

    # Lε: measurement claim
    'Le': {'measured_value': float,
           'candidate_true_value': float},  # optional
}
```

All sub-plans are optional. Layers with no matching sub-plan are
silently skipped and don't affect the total.

## Where to look next

- **[`SCOPE_TAXONOMY.md`](SCOPE_TAXONOMY.md)** — the four-dimension
  scope vocabulary (T | S | O | C).
- **[`CLAIMS.md`](CLAIMS.md)** — the 73 falsifiable claims, each
  with SCOPE annotation.
- **[`LOG.md`](LOG.md)** — the design record, bottom-to-top per
  its own header.
- **[`README.md`](README.md)** — the layer file map and framing.
- **`test_*_probabilistic.py`** files in `tests/` — the audit-
  grade pins for each layer's behavior. Each test file names its
  claims. If you're not sure what a layer will do on a specific
  input, the test file is a shorter read than the source.
- **`integrated_stack.py`** — the routing implementation that
  `audit()` wraps. Read if you need to know exactly how layers
  fold together.
- **`playground.py`** — the natural-language parser. Read if you
  want to know how a specific NL phrase routes.

## Design principles worth internalising

Three mechanisms carry "grounding not dictated by human narrative"
through the code:

1. **SCOPE tags** on every module, class, and claim make
   human/WEIRD/Earth-normal defaults **visible** instead of
   silent. When you see a constant, look up its scope; when the
   scope says `any_WEIRD_human` and you're an AI, treat it as a
   human default that may not apply to you.

2. **Category-error guards** at L4/L5/Lε refuse to score claims
   outside a layer's ontology. Silent low-probability scoring
   under an ontology mismatch is exactly the failure mode this
   whole stack was built to prevent. If you get
   `category_error_layers` non-empty, it's a scope mismatch, not
   a rare event.

3. **Pluralistic verdicts** at L5 refuse to elevate one shipped
   frame to universal-default status. The
   `CULTURALLY_UNPRECEDENTED` verdict is a flag ("no frame
   covers this yet"), not a rejection. If you produce
   proposals that trigger it often, that may mean the shipped
   frame library is incomplete for your use case — not that
   your proposals are wrong.

## Falsifiability

Every claim in this stack is falsifiable. If you can produce a
concrete input where the layer's output disagrees with the claim
statement (see CLAIMS.md), the claim is refuted — update the
claim in place per the REFUTATION_PROTOCOL, don't retune the
frozen constants to hide it.

See CLAIMS.md's REFUTATION_PROTOCOL section for the three-step
process (check the claim → check the instrument → author a
replacement). The `GL_L0_001` v1→v2→v3 arc is the reference
case showing all three steps in action.

## License

CC0. Use freely.
