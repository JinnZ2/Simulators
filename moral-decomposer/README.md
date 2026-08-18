# moral-decomposer

CC0. Stdlib only. No dependencies.

Takes a disagreement presented as moral or ethical and decomposes it into
option-distribution claims plus the frames those claims imply. The output is
the residue: what still disagrees once the lower stages are matched.

## MARKER PROTOCOL

This is a marker of something to explore, not a position under defense.
Correct responses are: test fit, extend it, or report where it breaks.

## THREE STAGES

    1  OPTION LAYER   per party: does it enter the tally, does it generate
                      options or is it held fixed, does it decide. Plus what
                      each side took out of the variable environment.
                      Divergence is COMPUTED between the two sides, not
                      declared.

    2  FRAME LAYER    the boundary criterion each side's assignments imply,
                      whether that criterion is documented, and whether it
                      was acquired in development rather than selected.

    3  CUT COUNT      further boundary decisions the frame requires, and how
                      many are documented. A frame that terminates needs one
                      cut. A frame that orders needs a supply of them.

    RESIDUE           candidates that reduce to stage 1 or 2 are accounted
                      for. Candidates that reduce to neither are the case
                      the instrument exists to find.

## RUN ORDER

Welded terms first. If a term in the dispute fuses independent quantities,
stage 1 will read divergence that is an artifact of the word. List them in
`welded_terms` and decompose in `category-weld` before trusting the output.

Presented binaries after. If both sides accept the same option set as
complete, that agreement is not residue between them — it is a shared
unmeasured assumption, and it routes to `presented-binary`.

## NO MORAL LABELS IN THE SCHEMA

Field names carry no moral terms. An instrument for reading smuggled frames
that smuggles one cannot do the job. `in_tally`, `held_fixed`, `generated`,
`decision_authority` are positional and directional; nothing in the schema
scores a side as correct, and no verdict is computed.

## USAGE

    python3 decompose.py                 table over cases/
    python3 decompose.py --case NAME     detail
    python3 decompose.py --new NAME      blank case skeleton
    python3 decompose.py --jsonl         machine readable
    python3 decompose.py --selftest      synthetic fixtures

## STATE

Two cases, both model-constructed, both reduce to zero live residue. The
selftest includes a fixture with a live residue item, so a non-empty result
is representable — zero here is an absence, not a proof, and n=2 of
self-produced cases is the weakest evidence in the repo. See CLAIM_TABLE
disclosed weaknesses.
