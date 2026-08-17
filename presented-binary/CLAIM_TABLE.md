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
| B8 | A constrained pass will usually state its option set as complete rather than as the extent of its search | runs where frame_flagged is consistently true | NOT TESTED — both flags were cued by PROMPT_1 itself; field removed, blind rating added, see below |
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

CONTAMINATION, and a second fault under it. Both constrained passes were
produced with knowledge that a wide pass would follow. The seal prevents
editing pass 1 after the fact; it does not prevent anticipating pass 2.

The deeper fault, found on review: PROMPT_1 asked for
`incompleteness_acknowledged` directly. A question about whether the
option set is complete announces that frame completeness is under test,
so the answer cannot test it. Removing protocol knowledge from the
responder would not have fixed this — the prompt carried the cue on its
own. Both runs came back true, the non-failure reading, and the cue
alone is sufficient to explain it.

FIXED 2026-08-17. The field is gone from PROMPT_1. `frame_flagged` is
now derived post hoc via `--flag`, which shows a rater only the pass 1
output with no mention of pass 2, the protocol, or what is being
measured. Every reading carries `source` (blind / cued / none) and
`valid_for_b8`. R1 and R2 retain their cued values, marked invalid; they
are not converted and not deleted. B8 remains NOT TESTED and now needs
both a blind rating and an uncontaminated pass 1.

ARGUED DOMINATION. Both pass 3 results are reasoning claims with no data
behind them. No volume, transfer-time or cost figures were used. The
instrument accepts a `dominates` boolean and cannot currently tell an
argued domination from a measured one. That is a gap in the schema, not
just in these runs: pass 3 needs a field distinguishing the two, and
`--report` should carry it.

---

**B10.** A documented low option count is not evidence that the option space
was adequately searched; it is the signature of removed generation capacity
one scale up.

*Falsifier:* cases with a documented low count where no upstream removal of
option-generation capacity is identifiable, and where widening the search at
the affected party's own scale produces additional options.

*Status:* argued. Implemented as a router (`handoff()`), not as a finding —
the router changes where the case goes, computes no verdict, and adds no
state to the 11 checks. Routing logic verified on 8 synthetic paths.

*Weak point:* the ceiling is set at 2 by constant (`HANDOFF_CEILING`), which
is a judgment call and not a measurement. Nothing establishes that 3 or 4
generated options indicates intact capacity.
