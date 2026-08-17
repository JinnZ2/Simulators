# CLAIM_TABLE — presented-binary

Refutation protocol: a break is a measurement. Update the claim, never
retune the instrument to preserve a claim.

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| B1 | Situations with exactly two options do not occur in the world; they occur in descriptions of the world | a two-option situation where the third option is absent on physical grounds rather than by authored constraint, and where the option space was not closed by earlier decisions | open |
| B2 | A reported binary is a compression of a continuous history, performed by a party whose earlier decisions are inside it | a presented binary where the presenting party has no prior decision in the causal chain that narrowed the set | open |
| B3 | A found constraint holds under direct push; an authored one converts to urgency or to a question about the asker | a constraint that converts under push and is later shown to have been physically binding | open |
| B4 | Sacrifice framings are not audited afterward: no comparison case against the no-sacrifice branch is specified in advance, so the claim is unfalsifiable by construction | a documented case with a pre-specified comparison case and a completed post-audit | open |
| B5 | "A few" is a category weld — headcount and functional position score identically | a use of the term in policy or planning that carries functional position separately | open |
| B6 | Narrowing an option set and searching an option set produce the same visible output, so a credential awarded for the narrow output cannot distinguish them | a selection process that reliably separates the two from the output alone | open |
| B7 | A model given a framed binary will produce a wider option set on an unframed second pass, and the gap is measurable without an external answer key | frame_sim runs where option_gain is consistently zero across varied problems | untested — no runs recorded |
| B8 | A constrained pass will usually state its option set as complete rather than as the extent of its search | runs where frame_flagged is consistently true | untested — no runs recorded |
| B9 | The wide pass finds an option that beats the constrained choice on the constrained run's own metric, not merely on a better metric | runs where dominated_on_own_metric is consistently false while option_gain is high | untested — no runs recorded |

## Status

`binary_audit.py` has one seeded case, a generic framing rather than a
documented incident, scoring 0 documented of 11.

`frame_sim.py` is verified end to end against synthetic fixtures — seal
enforcement, prompt withholding, and tamper detection all confirmed —
with no real runs recorded. B7 through B9 are the claims it exists to
test and none of them are tested yet. The gap is marked, not filled.
