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
        E3  PASS   no "w" opens in divlog; N appends -> N loaded, in order,
                   ids stable
        E4  PASS   grep clean across clock / echo / modes / divlog
        E6  PASS   n=1 -> NEW, always
        E7  PASS   shared upstream -> HOMOLOGY (weight 0);
                   disjoint provenance -> HOMOPLASY. flip is on graph
                   structure, not on mode labels

    BLOCKED — no code yet, a green here would be fabricated
        E2  needs syndrome.digest()
        E5  needs entrain.reference_version()
        E8  needs all three axes built (this is the central test)
        E10 needs scaffold + revalidate wired as peripherals

    LIVE FINDING
        E9  surfaced early, out of order, during the divlog build.
            WALKING fires on ANY monotone band-gap sequence; at small n
            monotone and trending are near-indistinguishable by chance.
            Logged as divlog entry 03efe4e41e61. Held OPEN as empirical.
            See OPEN_E9_walking_criterion.md. NOT patched.

    NOT STARTED
        E11 E12 E13 E14   field, Kavik/partner only
        E15 E16           need calendar time

    Note on the passes: E1, E4, E7 test code that already survived prior
    sessions. They are confirmations, not new information. The tests most
    likely to find something (E2, E5, E8, E10) are exactly the ones that
    cannot run yet. Do not read the green as coverage.

## WHAT A FAILED TEST PRODUCES

    Not a fix. A divlog entry (or a row edit, for E13). A failed field test is
    a volatility-class recalibration, a blind_to growth, or a criterion shift —
    recorded, timestamped, superseding the prior. The register and the log are
    the same discipline pointed at two time-scales.
