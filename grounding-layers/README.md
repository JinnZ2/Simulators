# grounding-layers

Ten simulators that make one argument: **any layer above L0 is bounded
by every layer below it**. AI proposals that ignore a lower-layer
constraint hallucinate; the "inspector" at each layer catches the
violation and pulls the proposal back to the feasible set.

Source: pulled from
[JinnZ2/Resilient-AI-Human-Collaboration-/Organize.md](https://github.com/JinnZ2/Resilient-AI-Human-Collaboration-/blob/main/Organize.md)
and archived here as [`../legacy/Organize3.md`](../legacy/Organize3.md).
Each `.py` names its source line range in its docstring.

## The stack (read L0 up)

| file | layer | what it caps |
|---|---|---|
| [`l0_physics_causality.py`](l0_physics_causality.py) | L0 | energy conservation, position continuity, `\|v\| ≤ c`, momentum sanity |
| [`l1_thermodynamics_entropy.py`](l1_thermodynamics_entropy.py) | L1 | L0 + 2nd law, entropy generation, battery depletion, Carnot ceiling |
| [`l2_planetary_mass_balance.py`](l2_planetary_mass_balance.py) | L2 | L1 + finite pools (water, soil, minerals, carbon), heat budget |
| [`l3_ecological_homeostasis.py`](l3_ecological_homeostasis.py) | L3 | L2 + allometry, Lotka-Volterra, ~10% trophic transfer, extinction cascade |
| [`l4_biomechanical_sensorimotor.py`](l4_biomechanical_sensorimotor.py) | L4 | L3 + joint limits, grip, neural latency, thermal tolerance, ~200 W sustained |
| [`l5_human_construct.py`](l5_human_construct.py) | L5 | culture, law, theology — slack that can't violate L0-L4 |
| [`l_epsilon_epistemic.py`](l_epsilon_epistemic.py) | Lε | measurement + observation between L0-L4 truth and L5 perception |

Two related simulators sit alongside the L-stack:

| file | subject |
|---|---|
| [`temporal_dysrhythmia.py`](temporal_dysrhythmia.py) | Six timescales from μs to millennia. Translator switch bridges far scales; without it, fast layers drown the slow ones out. |
| [`tensor_field_resilience_v1.py`](tensor_field_resilience_v1.py) | F, A, T, M (Feedback / Audit / Forensic / Meta-awareness) tugs and pulls under external stress. |
| [`tensor_field_resilience_v2.py`](tensor_field_resilience_v2.py) | v1 + G/W/Y anchors (Grounding / Temporal weight / Agency). Two scenarios: unstable-fear-driven vs resilient-truth-seeking. |

## Framing

Audit-grade side of the repo: each file's constraint set is stated
up-front in its docstring; violations are surfaced by the inspector
and reported alongside the AI's original (violating) proposal.

No `CLAIM_TABLE` yet — the claim structure is not stable enough to pin.
When it is, expect a `CLAIMS.md` file listing each layer's inspection
rule as a falsifiable claim (e.g. "L1 rejects any process with total
`ΔS < 0`"; falsifier: "produce a physical process that halves entropy
without export to a hotter sink").

## Running

```
pip install -r requirements.txt
python3 l0_physics_causality.py    # or any of the ten
```

Each `.py` runs the layer's inspector on a scripted AI proposal and
emits a matplotlib plot showing the raw proposal vs the grounded
(inspector-corrected) trajectory.

## Tests

Smoke tests in [`tests/`](tests/) verify the extractions are
well-formed (parse cleanly, have module docstrings, name the source).
Stdlib only.

```
python3 -m unittest discover grounding-layers/tests
```

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
