# msiaf-framework

MSIAF — **Multi-Dimensional Systemic Incident Analysis Framework**.
Docs-only landing from an OKComputer drop. Fourteen Markdown files
(~5,900 words) covering the four-dimension cascade for transportation
and logistics incidents plus reactive case studies, proactive
redesigns, and an early-warning proxy catalog.

`PACKAGE_README.md` is the upstream framework introduction — start
there for the substance. This file covers repo positioning,
provenance, and cross-references to other 4D-shaped modules in the
repo.

## What MSIAF is

A framework for analyzing transportation/logistics incidents by
tracing how friction points across **four interlocking dimensions**
align to manufacture outcomes typically mislabeled as "driver error"
or "worker inattention":

- **D1 — Human Factors & Physiology**
- **D2 — Operations & System Design**
- **D3 — Infrastructure & Environment**
- **D4 — Financial, Insurance & Regulatory**

Typical cascade: **D4 → D2 → D1 → D3**. Financial penalty structures
force rigid dispatch, which degrades the human operator's
physiological state, which meets an environmental hazard that was
never communicated or mitigated. The proactive models invert every
failure point so safety becomes the path of least resistance.

## Folder layout

```
msiaf-framework/
├── PACKAGE_README.md       — upstream framework introduction
├── README.md               — this file (repo positioning)
├── docs/
│   ├── framework-overview.md          — core thesis + cascade pathways
│   └── investigation-checklist.md     — 4-phase post-incident protocol
├── case-studies/                       — REACTIVE analysis
│   ├── reefer-trucking.md
│   ├── last-mile-delivery.md
│   ├── warehouse-distribution.md
│   ├── maritime-port.md
│   └── multimodal-infrastructure.md
├── models/                             — PROACTIVE redesigns
│   ├── reefer-financial-redesign.md
│   ├── last-mile-architecture.md
│   ├── warehouse-architecture.md
│   └── infrastructure-wim.md
└── proxies/
    └── proxy-catalog.md                — early-warning indicators
```

## Repo positioning

**Docs-only.** No code, no tests, no dependencies. Same genre as
`neural-augmentation-audit/` in this repo — a CC0 framework document,
not a simulator.

Not audited under the F-10 protocol; that protocol applies to code
and quantitative claims. MSIAF is a qualitative analytic frame with
worked case studies and design proposals — read it in its own frame,
same discipline as `relational/`.

## Cross-repo convergences

**Same 4-dimension pattern, different substrate:** the framework
parallels `fourd-municipal-engine/`'s 4D Municipal Code Entity
(**Density / Design / Delay / Dollars**), which analyzes what an
ordinance *does* along four regulatory axes. MSIAF applies the same
kind of four-dimension decomposition to what an incident *is*, along
four causal axes (human / operations / infrastructure / financial).
Both landed from OKComputer drops. Independently arrived-at 4D
thinking, worth noting.

**Constraint-axis analysis:** `neural-augmentation-audit/` names
seven constraint axes and traces what any proposed augmentation
borrows and where the deficit shows up. MSIAF's cascade
(D4 → D2 → D1 → D3) is the same shape at four axes instead of seven:
what pressure gets applied where, and which axis absorbs the deficit.

**Fragility and cascade:** the `fragility-cascade/` folder
(`THE_FRAGILITY_CASCADE.md`, `cascade_redesign_vulnerability.py`)
frames "how long does it take to redesign this" as the load-bearing
timescale. MSIAF's proactive models sit downstream of that question —
once the D4→D2 lever is identified, the redesign timescale becomes
the operative constraint.

**Incentive-blindspot topology:** `incentive-blindspot-sim/` models
how credentialed closure + capital concentration gate external
visibility and drive systems toward the failure mode they claim to
prevent. MSIAF's D4 dimension carries the same shape at the
contract/insurance layer specifically — penalty clauses that punish
incident reporting are structurally identical to the closed-with-
transparency scenario in that sim.

## What this is not

- **Not a claim table.** No `CLAIMS.md`, no `REFUTATION_PROTOCOL`.
  The framework asserts a causal thesis (incidents come from aligned
  cascades, not single failures); testing that quantitatively would
  need a claims-and-falsifiers landing on top of this — a future
  addendum, not this drop.
- **Not code.** No engine to run. If a simulator ever wants to
  operationalize the D4→D2→D1→D3 cascade (e.g. Monte Carlo an
  incident-rate distribution under changing D4 penalty structures),
  that would be a sibling folder — not an edit to this one.
- **Not exhaustive.** The upstream README's Status section names the
  known open threads: joint-employer safety liability standard,
  cross-platform fatigue ledger, V2I standards, drone corridor
  integration.

## Provenance

Source drop: **OKComputer_Repo_Creation** zip
(`3c54c695-OKComputer_Repo_Creation.zip`). The zip contained a
single top-level `msiaf-framework/` directory with no
build-artifacts. Landed as-is with the upstream README preserved as
`PACKAGE_README.md`.

CC0.
