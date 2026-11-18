# CLAIM_TABLE: load-withheld

CC0. Co-authored. Ids are permanent and are never renumbered.

## REFUTATION_PROTOCOL

When a claim is refuted, the claim is updated with its id kept and the
refutation recorded beside it. The estimator is never retuned to keep a claim
standing.

Each claim is tagged OBSERVED, DERIVED or PROPOSED. All four are PROPOSED:
- no observed case is in this folder;
- the seed cases are generic constructions.

| id | claim | tag | falsifier | status |
|---|---|---|---|---|
| LWH_001 (C1) | Withheld demand is nonzero and unmeasured in service records. | PROPOSED | A service record that counts deliberately withheld demand as its own field, or a survey finding zero deliberate withholding among those eligible. | OPEN |
| LWH_002 (C2) | Withheld demand concentrates at peak conditions. | PROPOSED | Recorded cases where the share of withheld demand is no higher under peak conditions than under ordinary ones (`peak_vs_average` peak <= off_peak), on cases where peak status is known. | OPEN |
| LWH_003 (C3) | Loss of skill breadth raises shared-system load with lag. | PROPOSED | A population whose skill breadth fell with no later rise in shared-system load, or with the rise arriving at the same time as the loss (no lag). | OPEN |
| LWH_004 (C4) | Take-up literature bins deliberate withholding as barrier or absent. | PROPOSED | A take-up study with a separate measured category for deliberate, informed non-claiming. | OPEN; not checked against any literature from this session |
