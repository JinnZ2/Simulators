# Geometric Neuro-Symbolic RAG

Single-file, numpy-only demonstration of the relational retrieval
architecture proposed in `../research_context.md` (the NEMGA synthesis).
Contrasts standard dense-vector RAG against the framework's
hypergraph-manifold approach on the same seven-document toy corpus.

## The two systems, side by side

| | `StandardRAG` (Cartesian) | `GeometricNeuroSymbolicRAG` (Relational) |
|-|---------------------------|------------------------------------------|
| **Memory** | Flat dict of vectors | Hypergraph on a curved manifold |
| **Relationships** | None — pairs only, via cosine | n-ary hyperedges with typed relations |
| **Attention** | Dot product, uniform | Geodesic distance, curvature-biased |
| **Verification** | None | Symbolic rules over retrieved subgraph |
| **Somatic coupling** | None | Confusion + pain → attention temperature |

Both classes share the same `query() → dict` API so the difference is
what's *inside* the result envelope, not the calling convention.

## Design of the relational side

**Hyperedge** (`@dataclass`) — an n-ary relation:
`(id, relation_type, nodes: Set[str], embedding, confidence, metadata)`.
Not restricted to binary triples the way KG-RAG is.

**ManifoldPoint** (`@dataclass`) — a document chunk placed on a
Riemannian manifold: `(node_id, coordinate, curvature, content, embedding)`.
Curvature is per-point (slightly hyperbolic by default —
`curvature ≈ -0.1 ± 0.05`), reflecting the hierarchical nature of
concept memory.

**Attention kernel** — `exp(-d · curvature_factor / T)` where
`d` is a metric-tensor geodesic distance,
`curvature_factor` biases attention toward negative-curvature regions
(hierarchies), and
`T = 0.5 + (confusion + pain)` is the somatic temperature — high
distress *widens* attention (`softmax` flattens), matching the
framework's claim that pain shifts cognition from precision to breadth.

**Manifold navigation** — geometric scores first, then two rounds of
hyperedge propagation add `0.3 · edge_score · edge.confidence` to each
member node. Fuse `0.6 · geometric + 0.4 · structural`.

**Neuro-symbolic verification** — after retrieval, symbolic rules
inspect the retrieved subgraph:

- A `contradicts` hyperedge whose nodes are all retrieved → the set is
  incoherent (flag the pair, mark the answer partial).
- Query intent gates required relation types — e.g. a query containing
  "cause" without any `causes` edge among retrieved nodes flags
  `missing_relations`.

These two rules are illustrative, not exhaustive. Extension is by
adding cases to `_verify_paths()`.

## What the demo shows

The seven-document corpus mixes drugs, symptoms, causes, and side
effects. Key facts:

- `d1` (aspirin reduces fever) and `d6` (stomach bleeding is serious)
  are marked `contradicts` (aspirin benefit vs its bleeding risk).
- `d1, d3, d7` all `treats` fever.
- `d2, d5` share `causes` (infection → fever).

Running `python3 geometric_rag.py`:

**StandardRAG** returns `d4` (aspirin bleeding) as top result for
"What reduces fever?" — a Cartesian similarity-hit with no signal that
the returned set includes a contradiction with `d1`.

**GeometricNeuroSymbolicRAG** at low confusion returns `d2, d1, d7, d5, d6`
and immediately flags `Contradiction between {'d1', 'd6'}` in the
verification envelope. The answer text is prefixed
`(Verification failed: ...)` so the downstream consumer sees the
epistemic status, not just the tokens.

**Somatic modulation** — raise `confusion_level=0.8, pain_level=0.7`
and re-query. The top score jumps from `~0.225` to `~1.001` and the
spread across returned nodes widens — attention has flattened. Same
manifold, same query, different retrieval shape because the "body" is
stressed. This is the operative claim: retrieval is not context-free.

Sample output in `samples/demo_output.sample.txt`.

## Position in the relational/ framework

This module operationalizes the NEMGA (Need-Event Modulated Geometric
Attention) synthesis from `../research_context.md`. It occupies the
bridge between:

- `../confusion_spectrum.py`'s cognitive-pain sensor — writes into
  `confusion_level` / `pain_level`
- The `GeometricSymbolicManifold` construct discussed in
  `../research_context.md` — instantiated as the `ManifoldPoint` +
  `Hyperedge` pair here
- `../pain_as_sensor.py` / `../social_pain_sensors.py` — physical and
  social channels that could feed the same coupling knobs

Same shape as the framework's other cross-domain claims: the mechanism
is a triadic sensor (internal prediction | somatic state | external
evidence), the differences are the thresholds and channels.

## What this is NOT

- **Not a benchmark.** The retrieval numbers are on hash-seeded random
  vectors, not real embeddings. Swap the `hashlib` seeding for a real
  embedding model (sentence-transformers, OpenAI-compatible endpoint)
  before quoting retrieval accuracy anywhere.
- **Not a KG-RAG replacement.** The verification layer has two rules.
  Real deployment needs a rule schema plus a rule extractor from the
  corpus.
- **Not a manifold-learning module.** The metric tensor is `I`
  (Euclidean) as a placeholder. A trainable metric or a pull-back from
  a learned encoder is the next step.

Everything above is scaffolding for a working system, following the
same "scaffold now, real components later" discipline the rest of
`relational/` uses.

## Running

```bash
cd relational/geometric_rag
python3 geometric_rag.py
```

Non-stdlib: `numpy`. Same exemption pattern as `play-sims/`, `energy/`,
and `climate-modeling/`.

CC0.
