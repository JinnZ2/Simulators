# AUDIT NOTES — QRNG PAIR SEARCH

What is not established, written down before it can be forgotten.

## This folder contains no measurements

Every number in it is either arithmetic (the sample counts, the entropy
budgets) or a categorisation argued from device physics (the bath
assignments). Nothing here was measured on hardware, and the folder's central
claim — Q3, that a fielded weld with empty structural overlap is removable by
construction — is exactly the claim that needs hardware to settle. It is
marked UNTESTED rather than rounded up.

## The bath assignments are judgements, not data

`readout_baths={"TH","PWR","EM"}` on every source is a deliberate flat
assignment: essentially any semiconductor readout on a shared board couples to
all three. It is defensible and it is coarse. It does not distinguish a
well-isolated detector chain from a badly laid-out one, which is precisely the
distinction Q3 turns on. A finer assignment would need per-design data the
folder does not have, and inventing gradations would manufacture resolution.

`MECH` appears in `BATHS` and in the perturbation protocol but is assigned to
no source. Alignment-sensitive optical legs plainly couple to it. It is left
unassigned rather than guessed at, and that is a gap, not a decision.

## The rate figures are order-of-magnitude

The `rate_hz` ranges are ballpark envelopes for each mechanism, not
specifications of any part. `decay_alpha` at 1e5 Hz implies a source hot
enough that licensing and shielding become the dominant design constraints,
which the `gate` field says and the rate column does not.

`rate_cap_optimistic` takes the minimum of the two *maxima*, which is the best
case for the pair, not the fielded rate. `rate_floor_conservative` is reported
beside it so the spread is visible rather than a single optimistic number
standing alone.

## What was corrected, and a note on attribution

Three corrections went into this folder, and one of them matters beyond this
table. The source material's prose names the failure mode — same board, same
temperature, same rail — and its table exempts `decay_alpha` from exactly
those baths. The correction is not that the physics was wrong; alpha decay
really is insensitive. It is that **the bath set was assigned to the source
and the readout chain was dropped in transfer**, which is the same shape as
`simulation-hypothesis-budget/`'s `LABEL_TRUNCATED_IN_TRANSFER`: a term
present upstream and absent downstream, with everything after it inheriting
the truncation as if it were the number.

**No authorship is assigned to any part of the source material.** It arrived
co-produced, prose and table together, and the layers are not separable from
inside this folder. Crediting a claim to a person, or a mistake to a person,
requires knowing which layer produced it, and that is not knowable here. The
corrections stand on the physics; the attribution does not exist.

## The extractor is not chosen and that is the largest gap

Q6 says k1 + k2 is a budget. Turning it into a bound needs a named two-source
extractor with a stated error parameter and min-entropy requirement. That
choice drives the real output rate and is a cryptographic design decision
rather than a search-axis one, so the folder leaves it open. Anyone using the
budget line as a rate estimate is using it wrongly.

## Threat model is unstated

The drop's framing — "an attacker has to compromise both plus the correlation
rule" — is not a threat model. Who the attacker is, what access they have, and
whether the legs are attacked physically or through the environment all change
the answer, and the environment path is the one this folder is about. Q4
removes the combiner's secrecy from the accounting; it does not replace the
missing model.

## Not a certification path

Nothing here addresses NIST SP 800-90B, AIS 31, or any health-test or
on-line-test requirement. A fielded RNG needs continuous health tests that
this folder does not describe, and the pair structure does not remove that
requirement.
