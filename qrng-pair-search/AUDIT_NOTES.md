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

## A correction this folder made, then withdrew

The first version of this folder read `decay_alpha`'s `baths={"COS"}` as a
dropped readout chain — the same shape as
`simulation-hypothesis-budget/`'s `LABEL_TRUNCATED_IN_TRANSFER`, a term
present upstream and absent downstream. **That reading is withdrawn.**

Measured: the readout baths are identical across all seven sources, so they
form a constant across every pair, and the pair partition is the same with or
without them — two distinct overlap sets either way. A table whose purpose is
to rank pairs by independence has a reason to carry only the discriminating
bath set. The reason was in the original table and was not recovered on first
reading; absence of a legible reason was treated as absence of a reason.

The split between `source_baths` and `readout_baths` is kept, because making
the constant explicit is what produces the `separable` category. What was
actually wrong is narrower than first claimed: the verdict word `CLEAN`.
`overlap {}` over source baths is true and means *no shared source bath*; it
reads as *no shared bath*, which no pair satisfies.

This is the second finding in this folder of the same shape as the folder's
own subject — a quantity that is constant across all cases carries no
information about differences between them, and including it looks like rigour
while adding nothing.

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
