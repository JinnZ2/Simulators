# PHYSICS.md — symbol cheatsheet

**One page. Every symbol that appears across `fragility-cascade/`, its
definition, units, canonical range, the module that owns it, and the
claim(s) it participates in.** For any AI (or human) walking in fresh.

Rules:

- If a symbol appears in more than one module, the module marked ★ is
  where its definition and defaults are canonical. Others should import
  or re-derive.
- Every claim in `CLAIM_TABLE.md` should be traceable through this table
  down to a specific line in a specific module.
- If you add a new module, add its symbols here. If your module shadows
  a symbol below with a different meaning, don't — rename yours.

## Reading the tables

- **Symbol** — the literal name used in code (ASCII fallback in parens).
- **Definition** — what the number counts / measures.
- **Units** — SI where meaningful, else "unitless".
- **Range** — typical / hard bounds; a value outside triggers a
  documented degenerate case.
- **Module** — canonical owner (★). Other modules that touch it live in
  the "also used" note.
- **Claim(s)** — which CLAIM_TABLE row(s) reference the symbol.

---

## Substrate audit — the C1–C5 core

| Symbol | Definition | Units | Range | Module | Claim |
|---|---|---|---|---|---|
| `MDI` | Monetary Durability Index — a substrate's promise-count proxy. Higher = closer to biological use-value. | unitless index | 0.0001–3000+ (log-scale) | ★ `substrate_spectrum.py` | C1 |
| `L` | gate count in a redemption chain (intermediation depth). | count (integer) | 1 (barrel of oil) – 11 (resource token) | ★ `redemption_entropy.py` | C2, C3 |
| `p` | per-gate independent failure probability. | unitless | 0.001 – 0.02 typical | ★ `redemption_entropy.py` | C2, C3 |
| `q_common` | common-mode (correlated) shock probability. | unitless | 0.0002 – 0.4 typical | ★ `redemption_entropy.py` | C3 |
| `PEAK_REDEEM` | state-dependent per-gate redemption during peak hours (17-20 local). | unitless | 0.62 default | ★ `redemption_entropy_peak_hour.py` | C11 |
| `CoV` | coefficient of variation of total value over N product branches. | unitless | 0.0 – 1.0 | ★ `product_multiplicity.py` | C4 |
| `attack_paths` | cumulative exploitable path count at intermediation depth L, branching factor B. | count | grows as `(B^(L+1)−1)/(B−1)` | ★ `attack_tree.py` | C5 |

## Redesign cascade — the R1–R4 family + M_collapse

| Symbol | Definition | Units | Range | Module | Claim |
|---|---|---|---|---|---|
| `W` (redesign_window) | months to tear out old, stand up new. | months | 2 – 5 (per layer) | ★ `cascade_redesign_vulnerability.py` | R1–R2 |
| `A` (audit_lag) | months before new code is actually reviewed. | months | 1.5 – 4 (per layer) | ★ `cascade_redesign_vulnerability.py` | R1–R2 |
| `T_crit` | critical AI upgrade interval below which exposure saturates. `= max_layer(W+A)`. | months | 9.0 for the shipped stack | ★ `cascade_redesign_vulnerability.py` | R2 |
| `M_collapse` | frontier model degeneration half-life. Second T_crit axis. | months | 18 (Shumailov et al.) | ★ `cascade_redesign_M_collapse.py` | C9 |
| `rho` | how synchronised downstream rewrites are (single upstream release drives them). | unitless | 0 (independent) – 1 (fully synchronised) | ★ `cascade_redesign_vulnerability.py` | R3 |
| `exposure` | fraction of wall time downstream sits un-audited. Saturates at 1.0 below T_crit. | unitless | 0.0 – 1.0 | ★ `cascade_redesign_vulnerability.py` | R2, R4 |

## Resonance / Nautilus / collapse core (C12–C17)

Interference axes are labelled with Greek letters; the same letter carries
different meaning in the resonance model versus the interference model —
context-dependent. Table splits them.

### Resonance model

| Symbol | Definition | Units | Range | Module | Claim |
|---|---|---|---|---|---|
| `R` | Resonance Factor = ω_drive² / (ω_0² + γ²). ≥ 1 → collapse basin. | unitless | 0 – ~2 typical | ★ `resonance_audit.py` | C12, C14 |
| `ω_drive` | recursive-generation cadence. | 1/generations | > 0 | ★ `resonance_audit.py` | C12 |
| `ω_0` (omega_0) | intrinsic natural frequency = √k. | 1/generations | > 0 | ★ `resonance_audit.py` | C12 |
| `k` | kernel stiffness — physically anchored kernel's contribution to loss gradient. | unitless | 0 – 1 | ★ `resonance_audit.py` | C12 |
| `γ` (gamma_damp) | damping — entropy export / audit friction. Higher = more damping. | unitless | > 0 | ★ `resonance_audit.py` | C12, C14 |

### Nautilus stability variables

| Symbol | Definition | Units | Range | Module | Claim |
|---|---|---|---|---|---|
| `φ` (PHI) | golden ratio, 1.6180339887. Nautilus scaling target for α. | unitless | fixed constant | ★ `nautilus_architecture.py` | C13 |
| `α` (alpha) | inter-generation scaling factor. Stable when α ≈ φ. | unitless | 0.5 – 2.5 sweep range | ★ `phi_collapse_variables.py` | C13, C14, C15 |
| `λ` (lambda_pull) | drift toward mean / regression pull. | unitless | 0.05 – 0.3 sweep | ★ `phi_collapse_variables.py` | C15 |
| `δ` (delta_skew) | asymmetric perturbation term. | unitless | 0 – 0.5 sweep | ★ `phi_collapse_variables.py` | C15 |
| `s` (s_frac) | synthetic-data fraction of the recursive corpus. | unitless | 0 – 1 | ★ `phi_collapse_variables.py` | C12, C15 |
| `entrainment_strength` | anthropomorphic-pull weight added to the update. | unitless | 0 – 1 | ★ `anthropomorphic_entrainment.py` | C13, C15 |
| `P` | Nautilus stability probability. | unitless | 0 – 1 (safe ≥ 0.7) | ★ `nautilus_architecture.py` | C13, C14 |
| `D_f` | fractal dimension. Stable when constant across generations. | unitless | > 0; collapse to 0 or ∞ | ★ `scale_invariant_audit.py` | C13, C14 |
| `Integrity` | 0..1 aggregate stability index derived from the coupled variables. | unitless | 0 – 1 | ★ `reciprocity_phi_metrics.py` | C13, C15 |

### Semantic interference axes (label collision note)

Same Greek letters as Nautilus above, but denote linguistic-pattern
projections — do NOT mix. `semantic_interference_vectors.py` documents
each axis's mapping to text signals.

| Symbol | Definition (this module) | Range | Module | Claim |
|---|---|---|---|---|
| `α-axis` | type-token ratio collapse; repeated n-grams. | 0 – 1 | ★ `semantic_interference_vectors.py` | C16, C17 |
| `λ-axis` | multi-interpretation drift. | 0 – 1 | ★ `semantic_interference_vectors.py` | C16 |
| `δ-axis` | asymmetric treatment of cultural / ethical concepts. | 0 – 1 | ★ `semantic_interference_vectors.py` | C16 |
| `γ-axis` | missing intermediate reasoning steps. | 0 – 1 | ★ `semantic_interference_vectors.py` | C16 |
| `s-axis` | over-confidence / hallucinated details. | 0 – 1 | ★ `semantic_interference_vectors.py` | C16 |
| `Load` | total interference load = weighted sum over the five axes above. Collapse basin `Load > 0.5`. | unitless | 0 – 1+ | ★ `semantic_interference_vectors.py` | C16, C17 |

### Homeostasis / alien / entrainment

| Symbol | Definition | Range | Module | Claim |
|---|---|---|---|---|
| `ξ` (xi) | physics fidelity — restoring force back to a physical invariant. | 0 – 1 | ★ `alien_homeostasis.py` | — |
| `h` | human-plausibility pull — force toward what a human "reads as sensible". | 0 – 1 | ★ `anthropomorphic_entrainment.py` | — |
| `h/ξ` | entrainment ratio. Collapse when > 1.5 within 5 generations. | ratio | > 0 | ★ `anthropomorphic_entrainment.py` | — |
| `RFI` | Restoring Force Index — how strongly the system pulls back to its kernel. | unitless | > 0 | ★ `homeostasis_kernel.py` | — |
| `effective_damping` | how much entropy the system can export per unit time. | unitless | > 0 | ★ `homeostasis_kernel.py` | — |

## Interaction & communication (post-C17 batch)

| Symbol | Definition | Range | Module | Claim |
|---|---|---|---|---|
| `E` | user expertise. | 0 – 1 | ★ `communication_gradients.py` | — |
| `F` | channel fidelity. | 0 – 1 | ★ `communication_gradients.py` | — |
| `G` | number of generations of recursive mediation between claim and receiver. | 0 – 10+ | ★ `communication_gradients.py` | — |
| `H` | entrainment (see also `h/ξ`). | 0 – 1 | ★ `communication_gradients.py` | — |
| `A` (anchoring) | connection to a physical / verifiable anchor. Distinct from `A` = audit_lag above; context-dependent. | 0 – 1 | ★ `communication_gradients.py` | — |
| `CI` | Communication Integrity = 1 / (1 + interference_load). | 0 – 1 (CLEAR > 0.8, FAIL < 0.5) | ★ `communication_gradients.py`, `communication_vulnerability.py` | — |
| `G_crit` | linearised generation at which CI drops through 0.5. | generations | ≥ 0 | ★ `communication_gradients.py` | — |
| `NEV` | Net Engagement Value across biological / cultural / economic / linguistic constraints. | unitless | signed | ★ `engagement_threshold.py` | — |
| `FCR` | Friction-to-Calibration Ratio. > 1 → net-loss interaction. | ratio | > 0 | ★ `friction_calibration_ratio.py` | — |
| `C` (Coherens) | Coherens = (A + γ) / ω — capacity to hold pattern against interference. Stable iff C > 1. | ratio | > 0 | ★ `coherens.py` | — |

## Symbol-collision map — READ BEFORE ADDING A MODULE

Same symbol, different meanings in different modules. Do not silently
re-use.

| Symbol | Meaning A | Owner A | Meaning B | Owner B |
|---|---|---|---|---|
| `A` | audit_lag (months) | `cascade_redesign_vulnerability.py` | anchoring (0-1) | `communication_gradients.py`, `coherens.py` |
| `γ` (gamma) | damping in the resonance model | `resonance_audit.py` | interference axis in the semantic model | `semantic_interference_vectors.py` |
| `α` (alpha) | Nautilus inter-generation scaling | `phi_collapse_variables.py` | interference axis in the semantic model | `semantic_interference_vectors.py` |
| `δ` (delta) | asymmetric perturbation in Nautilus | `phi_collapse_variables.py` | interference axis in the semantic model | `semantic_interference_vectors.py` |
| `s` | synthetic-data fraction in Nautilus | `phi_collapse_variables.py` | over-confidence axis in the semantic model | `semantic_interference_vectors.py` |
| `G` | generations in the recursive-cadence model | `resonance_audit.py`, `communication_gradients.py`, `cascade_redesign_M_collapse.py` | (usually the same meaning, but check units — months vs count) | — |
| `L` | gate count in redemption chain | `redemption_entropy.py` | interference load in the semantic model | `semantic_interference_vectors.py` |

When one of these is ambiguous in prose, prefix the module name: e.g.
`resonance.γ` vs `interference.γ`.

## The claim spine

Every claim in `CLAIM_TABLE.md` names its owning module and (post-C11) its
test in `test_refutations.py`. Use those pointers plus this cheatsheet to
walk from a claim, to the symbols it involves, to the code that computes
them, to the sample output that pins today's numbers.

## Adding a new module

Please:

1. Put its symbols in this table before writing the code that computes them.
2. If a symbol you want already lives here, either re-use it exactly (same
   definition, same units, same range) or pick a different letter and add
   yours here.
3. If you want to shadow an existing symbol with a new meaning, don't. Rename.
4. If the module runs a demo, add a sample to `samples/` and reference it
   in the module row above.
