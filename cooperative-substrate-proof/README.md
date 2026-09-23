# cooperative-substrate-proof

A four-part self-verifiable artifact, P1-P5. Each part runs standalone.
P2, P3 and P4 require no external data; P1's pipeline does and is ABSENT
here, named rather than substituted for.

## LOAD-BEARING FRAMING

> Competition is a framework but a narrow one. This artifact shows
> the cooperative substrate required for the competitive frame to be
> possible at all. Coverage argument, not values argument.
> Do not strip the competition frame. Add the layer underneath it.

Delivered verbatim in `WORK_ORDER.md` and reproduced in `FRAMING.md`,
which every run checks for presence and for having been stripped. The
coverage / values cut is enforced rather than described: `scope.py`
returns a domain-of-validity verdict with no member meaning one frame is
preferable, and `test_proof.py` walks the AST of every module for a
declared ranking-and-values vocabulary and fails on a hit. The scan is
null-tested against a planted violation, so its silence means something,
and it fired once during the build on this folder's own code -- see
`CLAIM_TABLE.md` `PRF_004`.

## Where this landed, and why not where the order says

The order names `JinnZ2/cooperative-substrate-proof` and says to create
it if absent. Repository creation is refused from this session: `add_repo`
answers *not found*, and `POST /user/repos` answers *403 Resource not
accessible by integration*. Both were tried before landing anything, and
this is the same refusal `substrate-alternative/` recorded at `SA_018`.

So the artifact lands here as a folder that would move to its own
repository unchanged: it carries its own `LICENSE`, its own suite, and it
imports nothing across its own boundary. The cost of that is stated at
`PRF_014` rather than hidden -- one operation in `test_proof.py` is a
COPY of `tools/authority_scan.py` rather than an import, and two copies
of one operation can drift with nothing here noticing.

## Running it

    python3 run_all.py            # per-part PASS / ABSENT
    python3 run_all.py --full     # every part's whole output

    python3 scope.py                                  # C1-C4
    python3 p1_records.py                             # and --template
    python3 p2_substrate.py                           # and --file X.py
    python3 p3_comprehension.py --corpus fixtures/corpus
    python3 p4_coherence.py                           # and --chain F.json
    python3 p5_lag.py                                 # and --actions F.json

    python3 test_proof.py         # the checks; the count is printed there

`samples/` holds one pinned render per part plus `run_all`, so the
outputs are readable without running anything.

Every module refuses `--selftest` with exit 2 and names the test file.
`p3_comprehension.py` is the one module whose bare invocation is a
refusal rather than a render: it reads a corpus and will not fall back to
its own source, which would measure the instrument instead.

## The parts

**P1 `p1_records.py` -- dependency records.** Records, not prose: for an
outcome, the preconditions absent from its own argument, five closed
kinds, each entry carrying a SOURCE. The order's rule is a REFUSAL --
`Requirement` raises `SourceMissing` at construction, because an
admitted-but-flagged entry is one that can be cited with the flag
dropped. `absent_from_argument` is DECLARED per entry and never inferred
from the text. `unstated_fraction` is None on an empty record, never 0.0.
The PIPELINE is ABSENT: no open-access methods host answers here and none
is paraphrased from memory, so the shipped record is CONSTRUCTED and says
so in its own provenance field.

**P2 `p2_substrate.py` -- substrate check.** Reads Python source with the
standard library's parser, reads nothing else, and by default reads
itself. Three registers: every call site as an unverifiable contract
(0.9900 unverified on its own source, which is below 1.0 and so not a
constant); the six layer contracts the order names, each with its failure
mode, none checkable from inside; and a CLOSED glossary mapping
adversarially-named parts to their mechanical requirement, returning
UNMAPPED for anything not in it. The existence proof is the narrow
checkable one: this output exists, producing it required every contract
listed, and the sha256 of the file analysed is printed beside the
reading. Scope: this run, this machine, this digest.

**P3 `p3_comprehension.py` -- comprehension check.** Compressibility as
the evidence, with a control. Gain is `1 - C(A+B)/(C(A)+C(B))`, and every
pair is also measured against B put through a monoalphabetic substitution
cipher: a letter permutation leaves every repeat inside B at the same
length and distance, so `C(cipher(B))` is `C(B)` to within a byte or two,
while every substring B shared with A is gone. The reading is the drop.
On the shipped fixtures the shared-terms pair drops 0.2350 and the
ciphered control drops -0.0052 -- an order of magnitude either side of
the threshold. The corpus verdict is the WEAKEST pair, not the commonest,
which is the order's own first sentence for this part.

**P4 `p4_coherence.py` -- goal-coherence check.** A chain of steps, each
declaring what it `accepts` as given and what it `contests`, plus
`contest_limit`: how many times it will refuse the same target. Three
outcomes: SETTLES, SETTLES_WITH_REWORK, NO_ANSWER. The middle one is
load-bearing -- without it every contest reads as failure and the order's
distinction has nothing to be distinguished from. The turf-war chain
returns NO_ANSWER for a STRUCTURAL reason (a cycle in the re-settle
graph) rather than by running out of budget, and names both sabotaging
steps.

**P5 `p5_lag.py` -- lag declaration check.** `t_visible / t_scored >= 10`
-> DECLARED_UNKNOWN, not blocking. Four verdicts, and the third is the
point: an UNDECLARED `t_visible` gives an UNDEFINED ratio, never a small
one. That is the state the antibiotic anchor sat in -- per patient, per
course, correct for fifty years, because the interval on which resistance
becomes visible was not a variable anyone was scored against.

## C1-C4

`scope.py` holds the four scope conditions and every part calls it, which
is the order's "coded into P1-P5". They are CONJUNCTIVE. A coding
returns WITHIN_COMPETITIVE_FRAME, OUTSIDE_FRAME_SCOPE naming which
condition failed, or UNDECLARED naming which was not coded -- and
UNDECLARED outranks OUTSIDE, so a silence is never read as a failure.
Both the WITHIN and the OUTSIDE verdict occur across the parts, so the
pass is not constant. The chain coded WITHIN is `turf_war`, and it is the
one with no answer.

## Status

Everything here is CONSTRUCTED except the arithmetic. No methods section
was read, no corpus outside `fixtures/` was measured, no model was run,
and nothing in the folder is a statement about any published result, any
organisation, or any person. `CLAIM_TABLE.md` carries `PRF_001..PRF_016`.
