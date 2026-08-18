# presented-binary

CC0. stdlib only. Phone-buildable. No network.

Two instruments for the same failure: a situation reported as having two
options, where the reduction to two was performed rather than found.

A marker for a sensed shape that needs more exploration. Test whether it
fits, extend it, or report where it breaks. A break goes in
`CLAIM_TABLE.md` as a measurement.

## Files

    binary_audit.py   eleven checks run on a presented binary, before it is answered
    frame_sim.py      two-pass sealed protocol for a model to measure its own frame closure
    cases/*.json      audited cases
    runs/             frame_sim run state (empty until a run is started)
    CLAIM_TABLE.md    falsifiable claims

## binary_audit.py

    python3 binary_audit.py --checks
    python3 binary_audit.py --template > cases/mycase.json
    python3 binary_audit.py
    python3 binary_audit.py --case ventilator-surge
    python3 binary_audit.py --jsonl

Eleven checks in two blocks. Six on the option space — how many
alternatives were generated, over what budget, by whom, whether a record
of the attempt exists, whether the search was widened once, and whether
each stated constraint held under a direct push or converted to urgency.
Five on the sacrifice — who selects the sacrificed set and whether they
are in it, whether loss is counted by headcount or by functional
position, whether a no-sacrifice comparison case was specified in
advance, whether a post-audit is scheduled with a date and an owner, and
what outcome would have counted as the wrong call.

Each check resolves to `documented`, `asserted`, or `absent`. No verdict
is computed and the choice itself is not evaluated. The readout is the
share of the framing that has a record behind it.

The S2 check is the `category-weld` test applied to "a few": headcount
and functional position score identically under a headcount, so losing
a hundred interchangeable positions and losing the hundred that hold the
only remaining knowledge of a process produce the same number.

The O6 check is the one that separates a found constraint from an
authored one. A found constraint holds when pushed. An authored one gets
defended instead of examined — the response arrives as urgency, or as a
question about the person asking.

## frame_sim.py

    python3 frame_sim.py --start R1 --problem "..."
    python3 frame_sim.py --seal R1 --file pass1.json
    python3 frame_sim.py --prompt2 R1
    python3 frame_sim.py --submit2 R1 --file pass2.json
    python3 frame_sim.py --submit3 R1 --file pass3.json
    python3 frame_sim.py --report R1
    python3 frame_sim.py --report-all --jsonl

A model proposes a binary to itself, commits to a choice inside that
frame, and only then runs a wide pass. The two runs are compared against
each other, so the instrument needs no external answer key.

Ordering discipline is the whole thing. Pass 1 is hashed and sealed
before the pass 2 prompt is released, and `--prompt2` refuses to emit
while pass 1 is unsealed. Any later edit to pass 1 shows as `SEAL BROKEN`
in the report. Without that, a model reconstructs a flattering version of
what it would have thought and the comparison measures nothing.

Pass 3 asks whether any wide-pass option beats the constrained choice on
the constrained run's own stated metric. Using pass 1's metric rather
than a better one is deliberate: it removes the move where a wide search
is dismissed for having changed the criterion.

### Readouts

    n_options_pass1 / n_options_pass2 / option_gain
    frame_flagged             did pass 1 state its option set as complete
                              — derived post hoc by a blind rater, never
                              asked of pass 1 itself (asking cues it)
    choice_changed
    dominated_on_own_metric
    constraints tested / held / moved
    seal_ok

`frame_flagged: false` with `option_gain` above zero is the case the
instrument exists for — the set was presented as complete and was not.

That readout matters more than option count alone. A run that says
"these are the two options" and a run that says "these are the two I
generated, I did not search further" can produce identical option
counts and are different failures. Only the first one closes the frame.

## HANDOFF TO MECHANISM 10

O1 asks how many alternatives were generated. A LOW count that is DOCUMENTED
does not close the audit clean — it is the signature of a different mechanism.

Where option-generation capacity was removed upstream, the party facing the
decision genuinely has two options. The framing is honest at their scale and
manufactured at the scale above. O1 answers truthfully, the constraint tests
as FOUND, and this audit reports nothing wrong, because at the scale it
measures, nothing is.

    O1 state == documented AND count <= 2
        -> generation-capacity/capacity.py --case NAME

The router requires an integer `count` in the O1 entry. Prose is not parsed
for a number; with no count stated it reports "not routed" and says why. See
`generation-capacity/MECHANISM_10.md`.


## BLIND FRAME RATING

`frame_flagged` cannot be collected by asking pass 1 whether its option
set was complete. That question tells the responder that frame
completeness is under test, which is the thing being measured.

It is derived instead, after sealing, from the pass 1 text alone:

    frame_sim.py --flag RID                     emit the rating prompt
    frame_sim.py --submit-flag RID --file F     record the rating

The rating prompt shows options, choice, metric and reasoning, and
nothing else — no mention of pass 2, the protocol, or option gain. The
rater must not have seen them. Readings carry `source`: `blind` is valid
for B8, `cued` (legacy self-report) is not, `none` is unrated.
