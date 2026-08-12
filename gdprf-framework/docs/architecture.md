# Core Architecture & Rationale

## Why Gradients, Not Binaries

The system moves away from binary reasoning to a gradient-based, probabilistic
approach. Claims such as "employee morale is low" or "economic growth is slowing"
cannot be verified directly — they concern unobservable traits or states. Instead,
each claim must be distilled into **physical, empirical, or data-driven proxies**,
and confidence in the claim becomes a continuous quantity that rises or falls with
the quality and weight of proxy evidence.

## Modules

| Module | Role |
|---|---|
| **Claim / Hypothesis** | The initial statement to be evaluated, instantiated with explicit scope |
| **Proxy Discovery Engine** | Searches for measurable indicators that map to the claim |
| **Vector Knowledge Graph (VKG)** | Dynamic database storing and connecting concepts and proxies via typed edges |
| **Instrumentation & Metrology** | Evaluates quality and reliability of incoming data (precision, noise floor, bias) |
| **Gradient Bayesian Update** | Updates confidence using continuous probabilities |
| **Human Translation Layer** | Renders the high-dimensional state as readable narratives for human overseers |

## Core Data Structures

1. **Claim / Hypothesis schema** — unique ID, domain, statement, scope (temporal,
   spatial, locality context), continuous confidence gradient (0.0–1.0), variance
   margin, assigned proxies, unknown-variable risk score.
   → [`../schemas/claim.schema.json`](../schemas/claim.schema.json)
2. **Proxy node structure** — links a proxy ID to a target variable, mapping an
   abstract concept to a measurable metric, with metrological characterization and
   a vector embedding for graph traversal.
   → [`../schemas/proxy.schema.json`](../schemas/proxy.schema.json)
3. **Edge structure** — typed relationships (`causal`, `correlated`, `confounding`,
   `proxy_of`) between claims and proxies, with coupling strength and evidence
   weight.
   → [`../schemas/edge.schema.json`](../schemas/edge.schema.json)

## Design Principles

- **Every claim is local.** Scope is mandatory — temporal bounds, spatial bounds,
  and locality context prevent universal-truth assumptions.
- **Every measurement is suspect.** Proxies carry their own fidelity gradient and
  metrological profile; a proxy is never assumed to be a perfect window onto its
  target variable.
- **Ignorance is quantified.** The unknown-variable risk score makes residual,
  unexplained variance an explicit, monitored quantity rather than a silent error.
