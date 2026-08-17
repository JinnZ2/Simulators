# CLAIM_TABLE — category-weld

Refutation protocol: a break is a measurement. Update the claim, never
retune the scorer to preserve a claim.

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| C1 | CATEGORY WELD is distinct from the existing eight mechanisms: those exclude a quantity from being measured, this one prevents two measurable quantities from being separated | showing any of the eight already covers the two seed terms without adding a mechanism | open |
| C2 | A term is welded iff at least one divergence case can be named AND the language has no separate handle for the diverged components | a term satisfying both that decomposes into one quantity on inspection; or a term failing one that behaves as welded | open |
| C3 | `n_cases` alone is insufficient — rare-but-enormous divergence and frequent-but-small divergence are different, and case count cannot tell them apart | showing max_spread is fully predicted by n_cases across a populated set | open |
| C4 | `bias` separates directional welds from imprecise ones, and does so without any input about intent | two terms with matching bias where the difference in behaviour requires an intent term to explain | open |
| C5 | Language models are more prone to welds than to retrieval errors, because co-occurrence training provides no gradient that would separate components a corpus never separates | a model separating components on a term whose corpus never separates them, without external tooling | open |
| C6 | "rural" is welded: density diverges from ownership distribution and functional diversity | paired series showing density and operators-per-1000-acres track each other across consolidation | open |
| C7 | "capital" is welded: title diverges from decision authority, risk bearing and revenue claim | showing the four move together across intermediated ownership and subsidy structures | open |
| C8 | Divergence in the seed terms runs in a consistent direction rather than randomly | populated readings returning bias near 0 | untested — no term quantified yet |

## Status of the readouts

Every case in `welds/` is currently unquantified: named, with no paired
before/after readings attached. `n_cases` is live. `max_spread` and `bias`
are implemented and verified against synthetic fixtures in `test_weld.py`,
and return `--` until real paired readings exist.

That is the honest state. The gap is in the data, and it is marked rather
than filled.
