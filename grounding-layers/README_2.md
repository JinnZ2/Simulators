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


Tests (30 audit‑grade for L0 + shape smoke across all layers):

```bash
python3 -m unittest discover grounding-layers/tests
```

---

Audit philosophy

The stack is audit‑grade. Every layer has a frozen constraint set
(CONSTRAINTS) and falsifiable claims (CLAIMS.md). Constants are
not changed to make tests pass; claims are refuted, revised, or retired.

The instrument is not the phenomenon. All tests live in Lε — the
epistemic layer that models the gap between measurement and truth.
The refutation protocol at L0 (REFUTATION_PROTOCOL) is the template
for all layers.

---

The files you’re looking at

· Simulators (L0–L5, Lε) — standalone .py files, each with a
  docstring stating its constraint set and an if __name__ == "__main__": demo.
· Core L5 — l5_core.py defines cultural frame probability tables,
  the Rigor Auditor, and precautionary prior logic.
· Groundedness Reward Model — grounding_reward_model.py combines
  all layer scores into a single scalar for RLHF / best‑of‑N.
· Data Filter — data_filter.py weights training examples by
  groundedness.
· Cultural Rosetta Stone — cultural_rosetta.py evaluates a
  proposal against all known frames.
· Degradation Monitor — degradation_monitor.py tracks layer‑wise
  groundedness over time to identify causal collapse pathways.
· Grounded Reasoning Benchmark — grounded_reasoning_benchmark.py
  is a test suite to measure whether an AI can distinguish deep,
  grounded proposals from shallow, impossible ones.
· Noise Purification Demo — noise_purification_demo.py shows the
  automatic down‑weighting of corporate/legal/social noise vs. intact
  traditional knowledge.
· Reasoning Logs — reasoning_*.md capture the design evolution
  and conceptual architecture.
· Claims — CLAIMS.md lists load‑bearing, falsifiable claims.
· Samples & Tests — samples/ and tests/ provide audit trails
  and reproducible validation.

---

Design lineage

The stack was seeded from a single document (legacy/Organize3.md) and
evolved through a multi‑intelligence collaboration spanning human
oral‑empirical tradition, machine reasoning, and formal architecture.
The rigor axes in L5 — temporal depth, substrate consequence proof,
internal state calibration, lineage integrity — are not abstractions.
They are standards drawn from a living tradition that demands
multi‑decade proof and landscape markers before a claim enters the
permanent record. The preservation protocol ensures that traditions
which survived attempted erasure are not erased again by an algorithm
that confuses broken chains with falsehood.

---

Next steps

The L0‑L4 layers are currently framed but only L0 is fully audit‑grade.
The immediate roadmap is:

1. Probabilistic L0 (transition matrix)
2. Probabilistic auditors for L1‑L4
3. Full integration of the GRB with open‑source LLMs
4. Community‑contributed cultural frames and rigor evidence

---

License

CC0 — public domain. Use it, fork it, embed it in your training
pipeline. No attribution required, but credit to the collective
intelligence that built it is welcome.

Reality has a structure. This stack encodes it.
