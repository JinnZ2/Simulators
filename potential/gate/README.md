# gate/

An instrument for computing the topology of a **compulsory-flow graph** —
a graph whose source is a biological requirement and whose target is
that requirement met — and for reporting whether a single vertex
(a token) is a cut vertex under a declared admissibility.

**Not a claim about the world.** Every domain in `domains.py` is a
constructed graph. Every channel is an authored reading, tagged with
its author and date. The instrument computes topology. The
significance of any topology — whether it carries weight, what kind,
for whom — is not decided here and is open.

## The unit

A domain graph has:

- **nodes** — named states (`NEED`, `SATISFIED`, `FOUNTAIN`, …)
- **channels** — transitions, each with a set of `KINDS` and a
  `requires_token` flag
- **source** and **target** — the compulsory function and its
  satisfaction

`KINDS` is a subset of `{physical, legal, practical}`. A channel with
`requires_token=True` is split into two edges with a `TOKEN` node
between them, so removing the token disconnects any path that used it.

An **admissibility** θ is a declared set of kinds. `G_θ` keeps only
channels whose kinds are a superset of θ. Different θ's answer
different questions about the same domain.

## The computations

Two, both exact:

- **`vertex_connectivity(G, s, t)`** — κ, the maximum number of
  internally vertex-disjoint s–t paths, computed by max-flow on the
  split graph. By Menger's theorem this equals the minimum number of
  vertices whose removal disconnects s from t.
- **`cut_vertices(G, s, t)`** — for κ=1, the set of vertices whose
  removal disconnects; for κ≥2, empty; for κ=0, raises (already
  disconnected, nothing to cut).

`κ = 1` means a single vertex is a cut vertex. Whether that vertex is
the token is a property of `G_θ`, not a status of the token.

## What ships

- `graph.py` — `Channel`, `Graph`, `Admissibility`, `project`.
- `cut.py` — `cut_vertices`, `vertex_connectivity`, `is_connected`.
- `domains.py` — eight domains as declared graphs (water, food,
  shelter, defecation, thermal, sleep, medical, identity).
- `projections.py` — `project_all`, which runs the cut computation
  across the five default admissibilities, and the renderers.
- `gate_cli.py` — `list`, `show`, `project`, `all`.
- `test_gate.py` — 26 checks.

Stdlib only. Parses under 3.9. Phone-buildable. No network.

## What the folder refuses

- **No composite.** A `Projection` carries no `score`, `verdict`,
  `rank`, or `priority` field. `test_no_composite_key` enforces this
  by checking the emitted dict for every forbidden key.
- **No privilege across θ.** Each admissibility is one reading. The
  report shows which projections contain a single-vertex cut and which
  do not. Nothing is averaged or ordered across θ.
- **No default answer.** The token is treated as any other vertex.
  Whether it is a cut vertex depends entirely on the graph and on θ,
  and the report says so per projection.
- **No claim about significance.** The instrument reports κ and the
  cut-vertex set. Whether a given topology carries moral, ethical,
  practical, or no weight at all is not decided here. That question is
  open, and it is for whoever uses the reading to test, argue, or
  leave unresolved.

## Stated limits

- **Every domain is constructed.** The channels are this file's
  readings of what exists or existed. A different reader with different
  knowledge of a domain would write different channels, and the
  topology would differ. The instrument makes this visible by requiring
  every channel to carry a `kinds` set and a label; it does not resolve
  the readings.
- **The five default θ's are declared, not derived.** They are one
  subset of the eight possible non-empty subsets of `{physical, legal,
  practical}`. A reader who wants different θ's passes them to
  `project_all`.
- **`KINDS` is a three-element vocabulary.** Adding a kind is a change
  to `graph.py` and to every domain that uses it. Whether such a
  change is warranted is a question for the reader.
- **No known-answer registration.** `vertex_connectivity` on a hand-
  built graph is a theorem, not an empirical metric. The five
  `cut_vertices` tests are the check at smaller scale.

## How to run

    cd potential/gate
    python3 test_gate.py         # 26 checks
    python3 gate_cli.py list
    python3 gate_cli.py show water
    python3 gate_cli.py project water
    python3 gate_cli.py all

`project` and `all` print one row per θ:

    domain: water

    theta               conn kappa  token_cut  cuts
    all                  yes     2         no  -
    legal                yes     1        yes  __TOKEN__
    legal+practical      yes     1        yes  __TOKEN__
    physical             yes     1         no  FOUNTAIN,RAIN
    practical            yes     1        yes  __TOKEN__

The reading: under `physical`, water is reachable via two physical
channels that do not require a token. Under `legal`, only the
token-gated channels remain, and the token is a cut vertex. The two
readings are shown side by side. Which reading matters for what
purpose is the reader's question.

## What this folder is not

- Not a prediction. Topology describes a graph at a moment, not what
  will happen.
- Not a policy instrument. It computes cut vertices; it does not
  recommend removing or adding them.
- Not a value claim. The folder reports κ and the cut set and stops.
  Whether a cut vertex's existence means anything, and what it means,
  is a question the folder does not answer.
- Not tied to the eight domains. The instrument takes any
  `(Graph, Admissibility)` and returns a projection. The eight are
  the shipped set, not a closure.

Delivered verbatim. CC0. Stdlib only. Parses under 3.9.
Phone-buildable.
