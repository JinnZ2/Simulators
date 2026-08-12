# Grounding Taxonomy

Ordered from strongest to weakest grounding for any claim about a proxy:

| Level | Name | Meaning | Typical source |
|---|---|---|---|
| G1 | **Direct physical measurement** | The observable IS the quantity, up to instrument error | soil compaction test; weigh-in-motion sensor; log timestamps |
| G2 | **Replicated empirical association** | Target and observable co-move across studies/contexts, mechanism proposed | validated SES indices; fatigue-reaction-time literature |
| G3 | **Single-context empirical association** | Observed co-movement in one dataset/context | one fleet's dwell-time vs. incident data |
| G4 | **Mechanism-only inference** | Plausible causal story, no direct co-movement data | "response latency reflects withdrawal behavior" |
| G5 | **Asserted mapping** | Someone wrote the number down | most fidelity fields in most specs |

Mapping to engine provenance grades:

- G1, G2 → can support `measured` (with documented benchmark/dataset)
- G3 → typically `estimated`
- G4, G5 → `assumed` until experiments upgrade them

**Upgrade paths** are the point of the lab: every G4/G5 entry should name the
experiment or dataset that would move it up the taxonomy.
