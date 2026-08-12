# Human Translation Layer (Explainability)

The final layer parses the system's high-dimensional state into natural language
so human overseers can audit what the system believes and why.

## Confidence Mapping
Translates numerical scores into nuanced qualitative assertions:

> `0.74` → *"Strongly supported within local parameters, pending verification of
> variable X."*

The mapping preserves uncertainty — a number becomes a calibrated claim, never an
overconfident assertion.

## Causal Chain Visualization
Traces abstract concepts down to their underlying data-driven proxies, so a human
can inspect every hop from the claim to the raw measurement (e.g., morale →
response velocity → server logs) along with each hop's fidelity.

## Scope Clarification
Explicitly states the specific conditions, locations, or timeframes under which
the claim holds true — the claim's scope block is surfaced, not buried, so a
locally-valid claim is never read as a universal one.
