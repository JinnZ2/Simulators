# grounding-layers

Ten simulators that make one argument: **any layer above L0 is bounded
by every layer below it**. AI proposals that ignore a lower-layer
constraint hallucinate; the "inspector" at each layer catches the
violation and pulls the proposal back to the feasible set.

**→ If you are an AI trying to use this stack, read
[`USAGE.md`](USAGE.md) first.** One function call:

```python
import sys; sys.path.insert(0, 'grounding-layers')
from entry import audit
result = audit("I can lift 200 kg.",
               ontological_scope='any_WEIRD_human')
```

Everything else in this folder is either detail or design record.

Source: pulled from
[JinnZ2/Resilient-AI-Human-Collaboration-/Organize.md](https://github.com/JinnZ2/Resilient-AI-Human-Collaboration-/blob/main/Organize.md)
and archived here as [`../legacy/Organize3.md`](../legacy/Organize3.md).
Each `.py` names its source line range in its docstring.

## The probabilistic pipeline (audit-grade)

The seven-layer L0-L5 + Lε **probabilistic pipeline** is the
audit-grade path — each layer's `l{N}_probabilistic_inspector`
returns a log-probability, and `integrated_probabilistic_inspector`
folds them into a single additive total with category-error
propagation for scope mismatches. Wired end-to-end from natural
language via [`playground.py`](playground.py)'s
`run_claim_probabilistic`, with a thin dispatcher in
[`entry.py`](entry.py) exposing a single `audit()` function.

- **[`SCOPE_TAXONOMY.md`](SCOPE_TAXONOMY.md)** — four-dimension
  scope vocabulary (T | S | O | C).
- **[`CLAIMS.md`](CLAIMS.md)** — 73 falsifiable claims, each with
  SCOPE annotation and status.
- **[`LOG.md`](LOG.md)** — design record (probabilistic L0 through
  L5 + rigor auditor).

419 audit-grade tests green as of the last commit.

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

**L0 is the audit-grade pilot** — [`l0_physics_causality.py`](l0_physics_causality.py)
has a `CONSTRAINTS` block + `REFUTATION_PROTOCOL` in its docstring,
its demo is wrapped in `if __name__ == "__main__":` so the module is
safely importable, and its five falsifiable claims (`GL_L0_001..004`
+ `GL_L0_PIN`) are in [`CLAIMS.md`](CLAIMS.md) alongside a full test
suite ([`tests/test_l0_physics_causality.py`](tests/test_l0_physics_causality.py))
and a captured sample ([`samples/l0_demo.sample.txt`](samples/l0_demo.sample.txt)).

`GL_L0_001` was falsified during test authoring (its v1 pinned a
specific rejection reason string; the implementation checks speed
before finite, so `-Inf` velocity is rejected as "Speed limit
exceeded" not "Non-finite"). The claim was weakened in place to pin
the rejection outcome only; the v1 statement is preserved in the
claim's History block. This is the refutation protocol working as
designed: the CLAIM changed, the frozen constants did not.

That falsification also surfaced a bigger point, now codified at the
top of [`CLAIMS.md`](CLAIMS.md) under "The instrument is not the
phenomenon". Every test is an instrument — check-order, tolerance
envelope, measurement convention, what to sample. A claim can be
PHENOMENON (an invariant of the sim) or INSTRUMENT (an invariant of
how we assess the sim) or a mix; a phenomenon-claim failure means
the inspector no longer does what it claims, an instrument-claim
failure means the instrument was retooled. `GL_L0_001` v1 was a
phenomenon claim with an instrument assertion silently attached.
The tests themselves live in Lε — they are the audit apparatus
looking at L0 — so the audit apparatus is not exempt from the same
measurement-vs-truth gap the `l_epsilon_epistemic` simulator models.

L1–L5 + Lε + temporal + tensor-field remain framed-but-not-pinned —
the CLAIMS.md contains sketched load-bearing claims (`GL_L{N}_LB`)
for each but no test wiring yet. When the L0 pattern generalises,
those get promoted one at a time.

## Running

```
pip install -r requirements.txt
python3 l0_physics_causality.py    # or any of the ten
```

Each `.py` runs the layer's inspector on a scripted AI proposal and
emits a matplotlib plot showing the raw proposal vs the grounded
(inspector-corrected) trajectory.

## Tests

Two test modules under [`tests/`](tests/):

- `test_extraction_shape.py` — stdlib-only smoke tests over every
  layer file (parse, docstring, expected names). Runs without numpy.
- `test_l0_physics_causality.py` — audit-grade tests for L0 (frozen
  constants + primitive contracts + load-bearing claim + demo pin).
  Needs `numpy` (`pip install numpy`).

```
python3 -m unittest discover grounding-layers/tests
```

30 tests total (25 audit-grade for L0 + 5 shape smoke), all green.

## License

CC0. See the repo root [`LICENSE`](../LICENSE).
