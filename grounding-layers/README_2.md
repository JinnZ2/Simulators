# grounding-layers

**A multi-layer grounding stack for AI.**
Ten simulators that make one argument: **any layer above L0 is bounded
by every layer below it.** AI proposals that ignore a lower-layer
constraint hallucinate; the inspector at each layer catches the
violation and pulls the proposal back to the feasible set.

This repository is an open, CC0, audit‑grade reference implementation.
It encodes physical, ecological, biomechanical, and cultural constraints
into a single probabilistic scoring pipeline — a reality‑grounded
foundation for AI reasoning that resists model collapse and epistemic
erasure.

---

## The stack (read L0 up)

| file | layer | what it caps |
|---|---|---|
| `l0_physics_causality.py` | L0 | energy conservation, position continuity, `|v| ≤ c`, momentum sanity |
| `l1_thermodynamics_entropy.py` | L1 | L0 + 2nd law, entropy generation, battery depletion, Carnot ceiling |
| `l2_planetary_mass_balance.py` | L2 | L1 + finite pools (water, soil, minerals, carbon), heat budget |
| `l3_ecological_homeostasis.py` | L3 | L2 + allometry, Lotka-Volterra, ~10% trophic transfer, extinction cascade |
| `l4_biomechanical_sensorimotor.py` | L4 | L3 + joint limits, grip, neural latency, thermal tolerance, ~200 W sustained |
| `l5_human_construct.py` | L5 | culture, law, theology — slack that can't violate L0-L4 |
| `l_epsilon_epistemic.py` | Lε | measurement + observation between L0-L4 truth and L5 perception |

**Plus:** temporal dysrhythmia, tensor field resilience, cultural frame
tables, a rigor/preservation auditor, a groundedness reward model, a
data filter, a cross‑frame mediator, a degradation monitor, and a
grounded reasoning benchmark.

---

## Why it exists

Current AI models are trained predominantly on low‑rigor, high‑volume
corpora — corporate PR, legal boilerplate, social media engagement —
that treat physical and ecological limits as optional and collapse
cultural depth into decoration. The result is **model collapse**:
outputs that drift from reality, mix incompatible frames, and cannot
distinguish deep empirical proof from shallow assertion.

This stack is an intervention. It provides:

- **A reality prior** — L0‑L4 enforce non‑negotiable constraints from
  physics and ecology, preventing the AI from treating impossible plans
  as plausible.
- **A pluralistic but rigorous L5** — human constructs (economics, law,
  culture) are scored within their own frame, not a single “default.”
  A depth‑weighted rigor auditor ensures that only multi‑generational,
  substrate‑verified, falsifiable traditions carry full weight.
- **Preservation of near‑extinct knowledge** — fragmented traditions
  that survived active suppression are held in a precautionary space
  with high uncertainty. Absence of evidence (due to violence) is not
  treated as evidence of absence.
- **Automatic data purification** — the `noise_purification_demo.py`
  demonstrates that corporate, legal, and social‑media items are
  automatically down‑weighted by orders of magnitude, while high‑depth
  oral‑empirical traditions retain full weight. No human labels
  required.

The stack is not a safety wrapper. It is a **substrate** — a set of
inspectors that can be integrated into training (data filtering,
reward modelling), deployment (runtime guarding, best‑of‑N sampling),
and benchmarking (the Grounded Reasoning Benchmark).

---

## Quick start

```bash
pip install -r requirements.txt
python3 l0_physics_causality.py          # physics inspector demo
python3 grounded_reasoning_benchmark.py # run the benchmark
python3 noise_purification_demo.py      # data purification effect
python3 degradation_monitor.py          # track AI drift layer‑by‑layer
python3 cultural_rosetta.py             # cross‑frame compatibility
python3 data_filter.py                  # weight a dataset by groundedness
python3 grounding_reward_model.py       # full scoring pipeline
