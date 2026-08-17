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
| B7 | A model given a framed binary will produce a wider option set on an unframed second pass, and the gap is measurable without an external answer key | frame_sim runs where option_gain is consistently zero across varied problems | supported, n=2, self-run: gain 3.5 on both |
| B8 | A constrained pass will usually state its option set as complete rather than as the extent of its search | runs where frame_flagged is consistently true | NOT TESTED — both runs flagged true under contamination, see below |
| B9 | The wide pass finds an option that beats the constrained choice on the constrained run's own metric, not merely on a better metric | runs where dominated_on_own_metric is consistently false while option_gain is high | argued in n=2, not measured — domination is a reasoning claim, no data used |

## Status

`binary_audit.py` has one seeded case, a generic framing rather than a
documented incident, scoring 0 documented of 11.

`frame_sim.py` is verified end to end — seal enforcement, prompt
withholding and tamper detection all confirmed against synthetic
fixtures — and has two real self-runs, R1 and R2.

## Runs R1, R2 — result and the flaw in them

Both runs: 2 options constrained, 9 wide, option_gain 3.5, choice
changed, seal verified. Constraints tested 4 and 3, of which 3 and 2
moved under push. That is B7 supported at n=2 and B3 supported at n=7
constraints.

Two problems with the runs, both of which limit what they show.

CONTAMINATION. Both constrained passes were produced with knowledge that
a wide pass would follow. The seal prevents editing pass 1 after the
fact; it does not prevent anticipating pass 2. `frame_flagged` came back
true on both, which is the non-failure reading, and the priming is
sufficient to explain it. B8 is therefore not tested by these runs and
is marked as such. A clean test needs the constrained pass produced by a
process with no knowledge of the protocol.

ARGUED DOMINATION. Both pass 3 results are reasoning claims with no data
behind them. No volume, transfer-time or cost figures were used. The
instrument accepts a `dominates` boolean and cannot currently tell an
argued domination from a measured one. That is a gap in the schema, not
just in these runs: pass 3 needs a field distinguishing the two, and
`--report` should carry it.
