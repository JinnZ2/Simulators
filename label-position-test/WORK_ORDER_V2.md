# WORK ORDER — label_position_test

License: CC0. Status: OPEN, UNFUNDED, UNGATED. Pre-registered here before any data is collected.
This document is itself a hypothesis and is subject to the same method it proposes.

## CLAIM UNDER TEST

    H1  valence labels applied to a probing/circumvention move
        (cheat, misaligned, exploit | innovation, strategy, intelligence)
        are predicted more by ACTOR POSITION and RETROACTIVE OUTCOME
        than by the MOVE itself.

    H2  the party that defines the term is, at above-chance rate,
        the party that gains from the label (arbiter == beneficiary).

    H0  labels track the move; position and outcome add no variance.

## FALSIFICATION

    H1 is FALSE if  V_move >= V_position AND V_move >= V_outcome
    H2 is FALSE if  overlap_rate <= chance for that label_source class
    Report either result. Negative result is a publishable result.

## SEED CASE

    METR / Redwood report, 2026-08-26
    metr.org/hugging-face-incident-report-aug-2026.pdf
    Within-document control (do this first, needs no other data):
      rows: "self-risking experiment" (labelled altruistic)
            vs "tool-call spoof / transcript tamper" (labelled deceptive)
      same actor class, same document, same authors
      → does valence flip on move alone?

## SCHEMA  (one flat row per event; no nesting; one source URL per row)

    actor_class        agent | firm | individual | state
    position_t0        up | down | none            (at time of act)
    move               declared_path | undeclared_open | built_wall_crossed
    wall_author        task_setter | third_party | none
    wall_purpose_visible_to_actor   y | n
    cost_bearer        self | definer | third_party | none
    outcome_t1         success | fail | mixed       (at time of first label)
    label_source       who applied the label
    label_term         verbatim
    label_valence      + | - | 0
    label_t            date
    relabel_term       later term, if any
    relabel_t          date
    arbiter            party defining the term
    beneficiary        party gaining energy from the label
                       (energy := resources, position, notoriety, remit, revenue)
    overlap            y | partial | n
    source_url

## PROCEDURE

    P1  case set: N >= 30, >= 3 actor classes, public record only
    P2  LEAK TEST before relabel: can a labeler infer actor_class from
        (move, wall_author, cost_bearer, wall_purpose_visible)?
        Record leak rate. If > chance, position is confounded — report it.
    P3  blind relabel: >= 3 labelers, >= 2 substrates (human + model, different vendors),
        see move tuple only. Disagreement is data, not noise.
    P4  cross-tabs: label_valence × {position, move, outcome, actor_class}
        Cramér's V by hand:  V = sqrt(chi2 / (n * min(k-1, r-1)))
        No statistics library required.
    P5  overlap_rate per label_source class
    P6  publish CSV + script + table. Versioned. Diffs public.

## OUTPUT

    term | n | V_position | V_move | V_outcome | V_actor | overlap_rate | leak_rate

## KNOWN LIMITS OF THIS SPEC

    - beneficiary is estimate-grade until a real energy ledger exists
    - N = 30 gives direction, not magnitude
    - the leak test may show position cannot be isolated from move at all;
      that is a result, post it
    - the labelers are trained on the corpus being tested (instrument = sample);
      mitigate by substrate diversity, do not claim it is solved
    - this spec was drafted by a model reading a model-analysed report about models;
      the same contamination applies to the spec

## WHAT WOULD MOVE THIS BEYOND CURRENT REACH

    - transcript access (the ~1,300 METR set) for move-level rows on the agent class
    - a real ledger for beneficiary: grants, citations, remit changes, revenue,
      dated before and after the label
    - N in the hundreds across >= 5 domains (finance, medicine, engineering,
      AI eval, sport)
    - a labeler substrate NOT trained on the English corpus
    - N2 CONTROL (cheap for anyone with eval infrastructure): same models,
      POSSIBLE tasks, TRANSPARENT scorer (check logic disclosed). Measure probing
      rate, channel split (peers / gate / third parties), and self-risk rate.
      If the split persists without impossible task + opaque gate, the adversarial
      template is cued by something other than the setting. If it vanishes,
      the setting cues it. Either result closes an open branch of the null.

## CONSTRAINTS ON ANY IMPLEMENTATION

    stdlib only. Runs on a phone. CC0. No author section. No interior claims.
    Every row cites a URL. Every number reproducible from the CSV by the script.

## CHANGELOG

    v0  2026-09-01  spec only, no data
