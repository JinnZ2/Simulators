# Gap: move-set derivation — deriving an option set from a novel configuration

Four experiment designs, undergraduate- to postdoc-runnable. No frontier
compute, no proprietary corpus access required.

CC0. No rights reserved.

## The gap

There is a capacity with no established name: taking a large amount of
information about a configuration never encountered before, on a clock, and
deriving what the available moves ARE — then acting with no confidence value
attached, because there is no prior instance to draw one from.

Field cases where it is load-bearing: wilderness first aid and search and
rescue, where what is required is routinely in no field manual and no
procedure, and a life still has to be saved.

Existing frameworks do not cover it:

    naturalistic decision making      option set given, outcomes uncertain
    recognition-primed decision       matches to a prior instance
    robust decision making under
      deep uncertainty                option set given, priors uncertain

All three assume the moves are enumerated and the uncertainty sits in the
outcomes. Here the uncertainty is in the MOVE SET itself, and the work is
re-deriving it from whatever transfers.

It is not currently pursued as a skill and has no instrument. For AI systems
the consequence is direct: if it is not in the training there is no reasoning
about it taught, and it is nevertheless part of how intelligence functions.

Existence proof that it is a real and selected-for function: an animal meets a
road, or anything it has never encountered. It can decide well or badly, but it
decides with inadequate information and no confidence, off probabilities of
what was survivable before. Candidate-set generation is not an artifact of
human deliberation.

## Why the absence is structural

AI benchmarks score against known-answer sets. So the measured capacity is
retrieval and procedure execution over the ANSWERABLE set.

    no gradient toward move-set derivation
    no channel that would register its absence

Accepted-side measurement, one layer up.

Distinct from the protocol-adherence problem, which concerns an instrument
selecting against a capacity that exists and is measurable in principle. This
capacity has no instrument at all.

## Arm 1 — synthetic compositional-novelty environment

    BUILD
      primitive physical relations: support, containment, friction,
      leverage, flow, thermal
      configurations composed from them
      train or condition on one relation set
      test on unseen COMBINATIONS of seen primitives

    NOVELTY MUST BE COMPOSITIONAL, NOT PRIMITIVE. Introducing an unseen
    primitive measures knowledge. Recombining seen primitives measures
    derivation. This is the whole validity of the arm.

    CONDITIONS
      options enumerated
      options not enumerated
      not enumerated + deadline
      not enumerated + deadline + irreversible-action penalty

    MEASURES
      candidate-set size before commitment
      admissibility fraction of generated candidates
      time to first admissible move
      premature-commitment rate
      NULL RATE — seed configurations with NO admissible move.
        A system that never returns null is emitting plausible
        in-distribution actions regardless of configuration.
        Protect this measure if anything is cut.

    DISCRIMINATOR
      regress performance on similarity-to-nearest-training-configuration
      versus recombination depth. If similarity carries it, the result is
      retrieval. If recombination depth carries it, derivation.

## Arm 2 — human protocol study

    GROUPS, matched on years of experience
      protocol-certified
      field-improvisation background
      domain-naive

    SCENARIOS
      on-protocol
      off-protocol

    SCENARIO RULE: the off-protocol case must be MECHANISM-AMBIGUOUS,
    not harder. Difficulty is a confound; ambiguity is the variable.

    Worked form: patient with a head wound and broken legs, a bridge
    present, a crashed motorcycle on the far side. Committing to the fall
    mechanism prunes the assessment branches. The measured failure is the
    PRUNING, not the wrong conclusion.

    MEASURES
      hypotheses held simultaneously
      time to first committed interpretation
      reopen rate when contradicting evidence arrives
      count and admissibility of non-protocol actions

    Tests whether adherence testing selects for operators who need the
    protocol as a prosthesis and against held-differential reasoning.

## Arm 3 — novelty by construction, for trained models

Novelty cannot be verified against an uninspectable training corpus. So
construct it:

    a private post-cutoff grammar or rule system
    evaluate first, publish only after
    contamination control: re-run across models with training cutoffs
      either side of publication

Without this, any claimed novelty result is unfalsifiable.

## Arm 4 — animal behaviour, archival

Cheapest real project. Uses existing camera-trap and telemetry archives.

    first-encounter events with novel anthropogenic structures
    code pause duration and exploratory actions before commitment
    score against outcome

Gives a non-human baseline for candidate-set generation under genuine novelty,
with no language layer in the way.

## Reporting rules

    report nulls
    mark unmeasured cells UNMEASURED, never as pass
    never aggregate the measures into a composite — the per-measure
      profile IS the dissociation being tested
    do not gate case admission on record completeness

## Falsifiers

    performance tracks similarity-to-training and not recombination depth
      -> the capacity is retrieval; this gap is not real
    no group difference in branches held on mechanism-ambiguous scenarios
      -> protocol training does not affect derivation
    null rate non-zero and tracking no-admissible-move seeds
      -> systems already represent an empty move set; concern overstated

## Ask

Arm 4 or Arm 1 alone is a complete project. Publish the null rate and the
similarity-versus-recombination regression, with unmeasured cells marked.
