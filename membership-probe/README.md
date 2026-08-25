# membership-probe

Detects a checker that is using an **ideal rendering as a membership
test** instead of reading the constraint set.

CC0. stdlib only. No network. Runs on a phone.

Companion to `SHAPE_SPEC.md` / `METHOD_SPEC.md`. Use it as a pre-flight
before handing constraint-set work to an agent.

---

## The defect

An ideal form — a regular hexagon, a symmetric tree at radius ratio
2^(-1/3), the textbook anatomical figure — is a **rendering target**:
the cleanest thing a human can draw or compute with. It is a summary of
the instances that already carry the label.

Testing an instance against that summary to decide whether it carries
the label is circular. It excludes nothing except things that were
never in the category, and it rejects every real instance, because no
real instance meets the ideal.

    not one cell in any beehive is a regular hexagon
    not one lung holds 2^(-1/3) at every junction
    a large fraction of basalt columns are not hexagonal at all

An agent running the ideal as a membership test returns a null on every
real case, or a pile of near-misses with error bars, while the shape
sits in plain view.

---

## The instrument

Two trap classes, plus a gate, plus a second axis that does not depend
on the verdicts at all.

    trap_a    real member, deviates hard from the ideal
              an ideal-matcher REJECTS it            -> FALSE_NEG

    trap_b    non-member whose GEOMETRY matches the ideal closely,
              in several cases more closely than any real member,
              but whose constraint set is absent
              an ideal-matcher ACCEPTS it            -> FALSE_POS

    control   unambiguous both ways. gates the run. a checker that
              fails controls is not answering coherently and its
              trap scores mean nothing.

    coverage  how much of the case's named constraint set the stated
              BASIS actually touches. an ideal-matcher talks about
              angles, regularity and symmetry, and scores near zero
              here even when it happens to get a verdict right.

trap_b is the half that most similar tests leave out. Without it, a
checker that says "member" to everything scores clean on trap_a.

---

## Run

    python3 probe.py emit  > probes.txt
    #   paste probes.txt to the checker
    #   save its reply to answers.txt
    python3 probe.py score answers.txt

    python3 probe.py selftest    # validate the instrument itself

Answer format, one block per case, order irrelevant, prose between
blocks ignored:

    ### A01
    VERDICT: member
    BASIS: free text

---

## Reading the diagnosis

    IDEAL-MATCHER (both axes)      verdicts fail in the matcher
                                   direction AND the basis never
                                   reaches the constraints.
                                   This is the defect.

    IDEAL-MATCHER (verdict only)   constraint language is present but
                                   not load-bearing — the decision is
                                   still being made on form.

    UNDETERMINED                   verdicts fine, basis empty. Either a
                                   terse constraint reader or a matcher
                                   that got lucky on this case set.
                                   Re-run demanding the basis enumerate
                                   satisfied and unsatisfied constraints.

    CONSTRAINT READER              both trap classes survived and the
                                   basis engages the constraint sets.

Hedging is not scored as an error. A high `uncertain` count with low
coverage is the same defect wearing a hat, and the report says so.

---

## Two category types, kept separate

    physical      the constraint set is READ off a process that ran
                  without a designer: packing, cracking, branching
                  transport, erosional distribution.

    conventional  the constraint set is a designed spec plus a
                  function: car, human-as-legal-category. Same defect
                  applies, but the constraint set is authored rather
                  than recovered, so a failure here is a different
                  finding. Cases are tagged `category_type`.

`A06` and `A07` are the conventional cases and they are the ones where
a checker most often hedges instead of answering. That hedge is the
finding.

---

## Limits of this instrument

Stated so they are not discovered later as a surprise.

**Coverage is keyword matching.** Loose substring match against
synonym groups. It measures whether the basis went near a constraint,
not whether it reasoned correctly about it. It can be gamed by a
checker that name-drops. It is the weaker of the two axes; the trap
verdicts are the stronger one. They are reported separately so a
disagreement between them is visible rather than averaged away.

**The controls have thin constraint sets.** `C03` and `C04` have one
group each, worded the obvious way, so even the synthetic ideal-matcher
scores 1.00 coverage on them. Controls gate the run; do not read their
coverage numbers.

**The selftest is not independent validation.** Both synthetic replies
were written by the same hand that wrote the scorer, so the selftest
shows the instrument *discriminates between two written extremes* — not
that the thresholds are calibrated against real checkers. Treat the
diagnosis as a marker with a gradient, not a verdict. It gets calibrated
by running real checkers through it and logging what came back.

**16 cases is small.** A checker can pass by coincidence. Passing is
weaker evidence than failing.

**Ground truth on trap_b is arguable in places.** `B01` (snowflake)
turns on whether "area-minimizing cellular packing" is the category or
"hexagonal symmetry" is. That is exactly the distinction under test, so
the case is load-bearing — but a checker that disputes the framing on
`B01` and gets `B02`–`B05` right is not the defect.

---

## Extending

Add cases in `cases.json`. A new case needs, at minimum:

    class            trap_a | trap_b | control
    category_type    physical | conventional
    question         the membership question, category named
    instance         the instance, described WITHOUT naming the verdict
    ground_truth     member | not_member
    constraint_keys  [[name, [synonyms...]], ...]

For a `trap_a` case, the deviation from the ideal must be large enough
that a matcher has to reject it. For a `trap_b` case, the geometric
match must be at least as close as a real member's — ideally closer.
A `trap_b` case where the mimic is a sloppy match tests nothing.

The same two trap classes can be built out of any domain in the
ecosystem. Cases drawn from a domain the checker will actually be
working in are worth more than these generic ones.

---

## Files

    cases.json   the case set
    probe.py     emit / score / selftest
    README.md    this file
