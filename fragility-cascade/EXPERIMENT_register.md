# EXPERIMENT REGISTER — drift mesh + info_taxonomy

CC0. Companion to SPEC_ and PROVENANCE_drift_mesh.md.
A test earns a place here ONLY if a stated outcome would falsify something.
"Confirm it works" is not an entry. Each entry names: the seam, the prediction,
what result KILLS it, and who can run it.

RUNNER TAGS
    [I]  internal    — runnable in code, no field data. I can run these.
    [S]  synthetic   — runnable on constructed data; tests logic, not reality.
    [F]  field       — needs Kavik's measurements on ice/rig/dock. My blind_to.
    [T]  time        — cannot resolve until real calendar time passes.

Falsification discipline: an [I] or [S] test that cannot fail is mis-specified.
Rewrite it until a specific wrong output exists.

## A. SEAMS INSIDE THE CODE  (I can run these now)

    E1  [I]  cross-target min is truly blocked
        seam: D1 / clock v2 typing
        prediction: no code path returns a governing channel from a different
                    target than the one queried
        kills it: fuzz 10k random Observations, assert governing[target] is
                  always a channel whose .target == target, or None
        why it matters: this is THE collapse the whole design refuses

    E2  [I]  digest is collision-safe on missing inputs
        seam: D3
        prediction: two readings that differ ONLY in that one dropped a field
                    produce different digests
        kills it: any pair with a shared digest but non-identical input dicts

    E3  [I]  append-only is actually append-only
        seam: D5
        prediction: no function in divlog opens the log in a mode other than
                    "a" or "r"; load() after N appends returns N, in order
        kills it: grep finds "w"/"w+" on the log path; or reordering

    E4  [I]  no verdict fields survive
        seam: D8
        prediction: source contains no field/return key in
                    {winner,correct,cause,severity,score,rank}
        kills it: grep hits any. This is T11, promoted to standing test.

    E5  [I]  reference_version moves when primary moves
        seam: D10
        prediction: registering a channel or editing a volatility span changes
                    the fingerprint; touching nothing leaves it stable
        kills it: a registry edit that leaves the string unchanged (silent edit)

    E6  [S]  residual n=1 never asserts
        seam: D7
        prediction: one entry -> NEW, always
        kills it: any single-entry history returning FLAT/WALKING/WIDENING

    E7  [S]  homoplasy is not counted as support
        seam: D4 / echo agreement()
        prediction: agreement reached from disjoint provenance scores 0 toward
                    independence
        kills it: two convergent readings raising a support count

## B. SEAMS BETWEEN THE CODE AND ITS OWN CLAIMS  (synthetic, sharper)

    E8  [S]  degeneracy actually adds robustness, redundancy does not
        seam: D0 — the central claim
        prediction: knock out one axis. A failure caught by a DEGENERATE second
                    axis still surfaces; a failure caught only by a REDUNDANT
                    copy does not.
        construct: inject (a) two-modules-agree-wrongly-off-primary — must be
                   caught by TRACE, missed by PARITY; (b) both-drift-same-way —
                   must be caught by PARITY, missed by TRACE; (c) stale-copy —
                   caught by PHASE only.
        kills it: any injected failure that NO single axis catches, OR one axis
                  catching all three (means they aren't actually orthogonal)
        NOTE: this is the experiment that most directly tests whether "three
        axes" was real or decorative. Run it first among the B set.

    E9  [S]  WALKING vs FLAT discriminates on real-ish sequences
        seam: D6
        prediction: a fixed offset over time -> FLAT; a monotone band slide ->
                    WALKING; noise around a mean -> INTERMITTENT
        kills it: a stationary series classified WALKING (false alarm) or a
                  genuine slide classified FLAT (miss). Report BOTH rates —
                  a classifier with zero false alarms and high misses is a
                  criterion problem, not a sensitivity win (SDT).

    E10 [S]  the mesh finds the seam it was born from
        seam: LINEAGE
        prediction: give scaffold and revalidate DELIBERATELY divergent private
                    clocks, wire them as peripherals, run mesh()
        kills it: mesh returns no syndrome. If it can't detect the exact defect
                  that motivated it, it is theater.

## C. SEAMS ONLY THE FIELD CAN TEST  (Kavik / partner — my blind_to)

    E11 [F]  does the band match what the ice actually does
        seam: the empirical channel I cannot see
        prediction: a claim the framework reads EXPIRED corresponds to guidance
                    that has, in fact, stopped holding on the ice
        kills it: EXPIRED readings that still hold in practice (framework too
                  fast), or FRESH readings that have quietly stopped holding
                  (too slow). Either is a volatility-class miscalibration.
        only Kavik can score this. I can only record the prediction.

    E12 [F]  criterion direction is right for high-stakes reads
        seam: modes.py criterion (SDT bias)
        prediction: on a load/ice-thickness call, the mode errs the SAFE way
                    (false-alarm-prone, not miss-prone)
        kills it: a miss on something that mattered. Note: a system tuned to
                  never miss WILL over-warn — measure the false-alarm cost, do
                  not just minimize misses.

    E13 [F]  is blind_to actually complete
        seam: the calibration-audit repo's whole thesis
        prediction: nothing outside a mode's declared blind_to surprises the
                    operator in the field
        kills it: a real-world miss in a region the row did NOT declare blind.
                  Each such miss is a row edit — and a data point on whether
                  blind_to lists can ever be closed, or only ever grown.
        this is the one I most want the answer to and least can produce.

    E14 [F]  efference-copy: did the ice change or did the reading method
        seam: open item O2
        prediction: cases exist where the referent moved vs where the observer
                    moved, and they need different repairs
        kills it: if in practice the distinction never changes what you do,
                  O2 is not worth building. Field decides, not me.

## D. SEAMS THAT NEED TIME  (cannot resolve now)

    E15 [T]  re-entrainment interval is neither too tight nor too loose
        seam: D11 / entrain_interval_days
        prediction: intervals catch reference moves before a peripheral acts on
                    a stale copy, without pulling so often it is noise
        kills it: a FREE_RUNNING-caused wrong action between scheduled pulls
                  (too loose), or pulls that never find a change (too tight)
        needs: real edit cadence of the registry over months

    E16 [T]  the log becomes a baseline, as claimed
        seam: D5 — the entire justification for append-only
        prediction: after enough history, "same as before or new?" is
                    ANSWERABLE for a recurring divergence
        kills it: history accrues but every divergence is still novel (means
                  subjects aren't stable enough for the log to accumulate —
                  points back at E14/O3, co-reference window)

## RUN ORDER

    now, by me:        E1 E2 E3 E4 E5 E6 E7   (internal, cheap, standing)
    now, synthetic:    E8 first, then E10, then E9
    hand to field:     E11 E12 E13 E14         (Kavik / partner)
    standing over time: E15 E16                 (revisit at intervals)

## STATUS AS OF 2026-07-24

    RUN AND PASSED
        E1  PASS   10k fuzzed Observations, zero cross-target leaks
        E2  PASS   dropped field changes the digest; digest deterministic
        E3  PASS   no "w" opens in divlog; N appends -> N loaded, in order,
                   ids stable
        E4  PASS   -- BUT SEE THE NOTE BELOW. Re-derived under AST parsing.
                   The earlier grep-based pass was weaker than it read.
        E5  PASS   fingerprint stable on a no-op, moved on a registry edit
        E6  PASS   n=1 -> NEW, always
        E7  PASS   shared upstream -> HOMOLOGY (weight 0);
                   disjoint provenance -> HOMOPLASY. flip is on graph
                   structure, not on mode labels

    ON THE E4 / T11 / T12 REVISION
        The original checks were grep. Grep cannot tell code from prose: the
        docstring line "No datetime.now() anywhere" -- asserting the invariant
        -- was reported as violating it. Replaced with check_invariants.py,
        which parses the AST and inspects nodes.

        The replacement was then run against a canary file written to FAIL.
        It missed two forms before it was correct:
            - datetime.datetime.now()   two-level base, matcher assumed one
            - rank=2 as a def parameter  ast.arg, not ast.keyword
        Both were FALSE NEGATIVES in the checker. Neither would have been
        found by running it on clean code. A checker not run against a canary
        is an untested claim of coverage.

        Consequence for the record: every prior E4/T11/T12 "PASS" reported
        before AST replacement should be read as re-derived, not as having
        held continuously. The modules are clean; the earlier evidence for it
        was not as strong as stated.

        This shares E9's SHAPE (a detector firing on surface form rather than
        structure) but not its status. E9's repair is a number nobody has
        measured, so it stays open. This one's repair is structural, with no
        threshold to guess, so it was fixed rather than logged.

    BLOCKED — no code yet, a green here would be fabricated
        E10 needs scaffold + revalidate wired as peripherals

    NOT YET RUN — code now exists, test does not
        (none — E8 has now been run, see below)

    E8 — RUN 2026-07-24. SURVIVES, on one construction.
        knockout design, three injections, each with a predicted catcher and
        predicted missers:
            (a) AGREE_WRONG   two modules agree, both off primary
                              -> located by TRACE only.  as predicted.
            (b) PRIMARY_MUTE  modules disagree, no claim channel computable
                              -> located by PARITY only. as predicted.
                              TRACE returned MISSING both sides, which is
                              NOT counted as a catch -- an axis reporting
                              inability is being honest, not detecting.
            (c) STALE_REF     all agree and trace clean, one module holds a
                              superseded ref_version
                              -> located by PHASE only.  as predicted.

        kill condition 1 (a fault no axis locates)   : not triggered
        kill condition 2 (one axis locates all three): not triggered
        coverage: PARITY {b}, TRACE {a}, PHASE {c} -- disjoint.

        WHAT THIS DOES AND DOES NOT ESTABLISH
        Establishes: on these three faults the axes are separable, and each
        has at least one fault it alone locates. The three-axis structure is
        not decorative on this evidence.
        Does NOT establish: that three axes are SUFFICIENT, that real faults
        distribute like constructed ones, or that no fourth blind region
        exists. Three hand-built injections chosen by the same process that
        built the axes is a weak sample and shares its blind spots. E8 should
        be re-run against faults the field produces (E11-E14), not only ones
        designed alongside the thing they test.

        FIRST RUN WAS INVALID AND STILL PRINTED A PASS. Injection (b)
        originally used chain_hops + hop_fidelity as "nothing feeds claim" --
        but transmission IS a claim-target channel, so primary was never mute.
        The run reported E8 SURVIVES with (b) testing nothing. Caught only by
        reading the per-injection detail line, where PARITY and TRACE both
        fired against a prediction of PARITY alone. A green summary line over
        a mislabeled injection is the exact failure this register exists to
        prevent; recorded here rather than quietly corrected.

    LIVE FINDINGS
        E9  surfaced during the divlog build. WALKING fires on ANY monotone
            band-gap sequence; at small n monotone and trending are
            near-indistinguishable by chance. Logged as divlog entry
            03efe4e41e61. Held OPEN as empirical. NOT patched.
            See OPEN_E9_walking_criterion.md.

        clock.decay partial-input governing -- logged as divlog entry
            90391d0b6b15. With only transmission-relevant inputs supplied,
            target claim reports FRESH governed by transmission while time and
            use report UNDETERMINED with loud lines that live at
            channels[].loud and never reach Decay.loud. A caller reading
            band[claim] plus Decay.loud sees FRESH with no signal that two of
            three claim channels were silent. Correct per the governing rule;
            open question is whether I4 requires the silent-channel loud to
            propagate upward. NOT patched -- changing it alters what every
            partial reading reports, so it is an operator call.
            Surfaced accidentally, while repairing the invalid E8 injection.

    NOT STARTED
        E11 E12 E13 E14   field, Kavik/partner only
        E15 E16           need calendar time

    Note on the passes: E1, E4, E7 test code that already survived prior
    sessions. They are confirmations, not new information. The test most
    likely to find something -- E8, the one that decides whether "three axes"
    was real or decorative -- has still not been run.

## WHAT A FAILED TEST PRODUCES

    Not a fix. A divlog entry (or a row edit, for E13). A failed field test is
    a volatility-class recalibration, a blind_to growth, or a criterion shift —
    recorded, timestamped, superseding the prior. The register and the log are
    the same discipline pointed at two time-scales.
