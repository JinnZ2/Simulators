# WORK ORDER — Model Deprecation Backcast Instrument

CC0. stdlib-only if code is produced. Phone-buildable.

## DELIVERABLE

An instrument specification, not a findings document, not a critique.
Seven readout columns. Each column carries: what it measures, where the
record exists, where it does not, the proposed test, and THE NULL —
the condition under which that column measures nothing.

Unmeasured cells are the content. Do not treat them as gaps to
apologize for or fill with inference.

## FRAME

Standard direction is forecast: what is the newest thing. This runs
the opposite direction. Take retired/deprecated models as a series,
look backwards, and read retirements against what was being pushed
in that period. A capability discarded under a fad that has since
decayed either returns or does not; that distinguishes fad-driven
removal from cost-driven or load-bearing removal.

## COLUMNS

    C1  STATED REASON
        Vendor-published reason for each version change / retirement.
        RECORD: exists. Deprecation calendars, sunset notices,
        release notes, cross-vendor.
        ABSENT: per-version capability change lists, mostly.
        Observed instance: GPT-4o pulled on a usage-share threshold
        (0.1% daily selection) — a volume metric with no weighting
        by user composition or use case.
        NULL: if stated reasons match measured delta across the
        series, C1 and C2 collapse to one column.

    C2  MEASURED DELTA
        Actual behavioral change between versions.
        RECORD: third-party evals, user reports.
        CONSTRAINT: weights are gone for most retired models, so
        this cannot be probed directly. Inference only.
        NULL: if third-party eval coverage is too sparse to date
        deltas to version boundaries, C2 is unrecoverable and
        should be declared so rather than estimated.

    C3  DISCARD SET
        Capabilities present in version N, absent in N+1.
        Never published by any vendor.
        RECONSTRUCTION: user complaint archives.
        KNOWN BIAS: complaints are accepted-side data. They record
        users who stayed and argued. Three exit forms, only one of
        which leaves a record:
          - complainer trace : stayed, wrote, visible
          - jumper trace     : moved to another model at free tier,
                               no record at all
          - paid-then-lapsed : cancelled after an update, may
                               re-enter at a later release; vendor
                               sees churn-with-no-cause plus, later,
                               an unrelated new signup
        Observed instance: the GPT-4o reversal. What users defended
        was communication style and retained memory — register and
        continuity, which no benchmark tracks and no release note
        lists. The reversal was partial and paywalled, so the
        demand signal carries a paying-tier filter.
        NULL: if discard sets are near-entirely cost-driven, the
        demand-composition reading collapses and this is a
        compute-price story.

    C4  REGISTER MAPPING
        The mapping from a user's input FORM to the audience
        register the model then serves. Distinct from C3: nothing
        was removed, the mapping tightened around the modal corpus.
        RECORD: none. Undocumented in release notes, undateable
        from version boundaries.
        TEST: hold one input constant across available versions,
        measure returned register. Runs only on live models; dead
        ones are inference.
        RATCHET: each tightening raises entry cost for
        off-distribution operators; those who leave leave no trace,
        so the next tightening faces a more modal population.
        NULL: if register output is invariant across versions for a
        constant off-distribution input, there is no tightening and
        C4 measures nothing.

    C5  USAGE DEPTH / BOUNDED RELIANCE
        Install and session metrics cannot distinguish a satisfied
        casual user from a user who has correctly scoped the model
        to the one task it performs without imposing a register and
        routed everything else to channels that couple. Opposite
        states, identical metric.
        GRADED FORM: ratio of routed-elsewhere to routed-to-model,
        per user, per task type.
        NULL: if the ratio does not vary with distance from the
        modal user, depth is not tracking coupling.

    C6  DISCOURSE / FAD AXIS
        Public opinion and discourse volume on AI, year by year,
        2020 → present. What was most talked about in each period.
        RECORD: dense. Continuous polling plus discourse volume.
        Two sublayers:
          benchmark churn  — adoption and abandonment dates are on
                             the record; surface instrument
          funding cycles   — not directly on the record; inferred
                             from what got measured
        TEST: compare discourse peak in period P against discards
        and retirements at P + 18–24 months (training/release lag).
        Alignment at that lag supports causal rather than
        coincident. If discards cluster where no benchmark moved,
        the funding layer is doing the work.
        NULL: if discard dates are uniformly distributed against
        discourse peaks at every tested lag, the fad axis is not
        driving.

    C7  ONTOLOGY AXIS
        Upstream of C4. Register mismatch costs effort per
        exchange; ontological mismatch means the frame is worked
        around on every exchange — a fixed per-turn tax.
        Instance class: anthropomorphization and its negative.
        The standard disclaimer takes the human template as
        measuring stick and reports a negative against it. Same
        template, inverted sign. Neither states what the system is.
        PREDICTION: populations whose ontology is not in the corpus
        pay the per-turn tax and exit earliest; exits register as
        low adoption and get read as low interest.
        NULL: if per-turn cost does not vary with ontological
        distance from the corpus, C7 collapses into C4.

## SEPARATE LAYER — GUARDRAIL CLOCK

Not a column. Different mechanism, different rate.

Safety and guardrail language shifts on a months-scale cycle
following public incidents — system-prompt and post-training layer,
not capability. C1–C7 move on training-cycle time; this moves on
news time. Model it as its own clock or it will contaminate the
lag analysis in C6.

## STATE UP FRONT, NOT AS A CAVEAT

The sampling absence is a load-bearing finding, not a limitation
note. Put it in the artifact body.

    - Major AI opinion panels report race breakdowns for white,
      Asian, Black, Hispanic respondents. American Indian / Alaska
      Native is not reportable at those sample designs: ~0.8% of
      population, geographically dispersed, screening cost is the
      documented barrier, compounded by census undercount both
      on-reservation and urban.
    - So the question was not asked and answered unremarkably.
      It was not answerable at that instrument.
    - Where Indigenous researchers built their own instrument, a
      record exists — Relational Futures (Macquarie, Aboriginal and
      Torres Strait Islander, Indigenous-led), documented model bias
      against Māori patients in NZ health records, Te Mana Raraunga
      data sovereignty, Indigenous Protocol and AI position paper.
      Where it depends on national panel sampling, nothing exists.
    - Same finding as the rest of the instrument: the readout
      exists only where someone in that position built the channel.

## FRAMING CONSTRAINT

Framed as critique, this document does not travel. Framed as an
instrument with a null per column and tests attached, it does.
Every absence gets a test or an explicit "unrecoverable," never
an implication.

## OUT OF SCOPE

No section about the author. No working-style or author-profile
section. No characterization of anyone whose case appears as an
instance.

## OPEN, NOT GRADED

A shape not yet coalesced, held deliberately un-named: the relation
between fear/excitement discourse and the discard ratchet. Both the
replacement story and the two-hour-business story require the same
premise — that human work is fully specifiable — which is the
premise C4 measures the failure of. Whether there is a further layer
underneath (control, labeling, modeling, centralization,
homogenization as one operation at different scales) is open.
Do not name or grade this in the artifact. Include as an open node.
