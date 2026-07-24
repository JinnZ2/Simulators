# PROVENANCE — drift mesh: why each decision was made

CC0. Companion to SPEC_drift_mesh.md. This file is the WHY; the spec is the WHAT.
Read the decision here before "simplifying" it in the spec. Most invariants are
load-bearing against a specific failure, and the failure is named.

Format:   D#  decision  <- source borrowed from  <- failure it prevents

## LINEAGE

The mesh did not start as a design. It started as a SEAM.

    scaffold.py and revalidate.py were each written holding a PRIVATE copy of
    the volatility clock. Two copies of one reference => they drift apart, and
    nothing was watching the gap. Open-queue item 5. Still the largest drift.

Question asked was NOT "how do I stop drift." It was "how does the physical
world navigate drift it cannot stop." Three fields answered:

    PHYSICS / metrology    no instrument keeps its own copy of the standard.
                           every one traces to a single primary. drift measured
                           against primary, NEVER between copies.
                           -> the seam, restated as a discipline.

    BIOLOGY / circadian    every tissue runs its own oscillator; they drift at
                           different rates; the body does NOT force lockstep.
                           once a day it re-entrains all against one external
                           cue (light, the zeitgeber).
                           -> scheduled pull-back to one signal, not sync.

    QUANTUM / error corr.  never measures the data directly (that collapses it).
                           measures syndromes — parity between neighbors —
                           locating drift WITHOUT reading content.
                           -> the no-interior-verdicts boundary, exactly.

Operator's call: do not pick one. Run all three in parallel as a full mesh,
"so every way can clock against itself, against others, and against each way."
That is 3x3 — self-check, cross-check peers, trace to primary.

## WHY THREE AND NOT ONE — the degeneracy argument

    D0  three axes, not one averaged score
        <- Edelman degeneracy (different structure, same target)
        <- prevents single-axis blindness:
             metrology is blind to two modules agreeing wrongly
             parity   is blind to both drifting the same way off primary
             phase    is blind to content, but catches a module trusting a
                      stale copy
           each is blind where another sees.
        This is NOT belt-and-suspenders — that would be REDUNDANCY, the same
        check twice. It is DEGENERACY: different checks, same target, adds
        robustness. The framework is thereby built out of its own principle
        (modes.py audit distinguishes exactly these two).
        REJECTED: combine into one health number. That reintroduces the
        mode-supremacy collapse clock.py already refused — min/avg across
        different failure types is a category error.

## DECISION POINTS

    D1  never compare across clock targets              (SPEC I2)
        <- clock.py v2: channels typed by decay target, governing channel is
           fastest WITHIN a target, never across
        <- prevents calling a claim-band vs mode_sensitivity-band gap a
           divergence. They measure different things. Three separate meshes.

    D2  parity reads checksums, not content             (SPEC I3)
        <- quantum syndrome measurement
        <- prevents two failures: (a) reading the claim to compare modules
           re-introduces an interior verdict; (b) digests keep parity cheap
           enough to run on a phone at a fuel stop — two 12-char strings, not
           two documents.

    D3  digest renders a missing input as "None", not as absence
        <- clock.py: missing input goes LOUD, never silent-default
        <- prevents two readings fingerprinting identical because both silently
           dropped the same field. Otherwise the log certifies agreement that
           is really shared blindness.

    D4  four parity kinds, not one "disagree" flag      (SPEC syndrome.parity)
        <- signal detection: separate the finding from its cause structure
        <- prevents the common logging error — treating DIFF_INPUTS_DIFF_BAND
           (they read different facts) as SAME_INPUTS_DIFF_BAND (they disagree
           about the same facts). Only the second is module disagreement.
           DIFF_INPUTS_SAME_BAND is LOGGED, not dropped: convergent agreement
           is homoplasy — cheap, not evidence (echo.py vocabulary).

    D5  append-only; resolution is a new entry that supersedes  (SPEC I5)
        <- operator: "a place to log so that if there are discrepancies in the
           future you have a log to check against"
        <- prevents losing the baseline. The value is not any single entry, it
           is the HISTORY. "Off the same way as in March, or is this new?" is
           unanswerable if entries are mutated.

    D6  residual classifies SHAPE, never severity       (SPEC divlog.residual)
        <- SPC control charts; physics residuals (flat = calibration,
           walking = real signal)
        <- prevents reacting to single points. Reads only the band sequence.
           Never picks a correct side.

    D7  n=1 returns NEW, not a verdict                  (SPEC T9)
        <- GUM: one measurement is not a distribution
        <- prevents declaring drift or calibration from a single disagreement.

    D8  no verdict fields anywhere                      (SPEC I6, T11)
        <- ecosystem no-interior-state rule; energy_english constraint
        <- prevents winner/correct/cause/severity/score/rank creeping in as the
           log matures. T11 greps the source. If any appear, the build is wrong.

    D9  every timestamp explicit, no implicit now()     (SPEC I7, T12)
        <- clock.py: `now` is always an argument
        <- prevents a reading that cannot be replayed. Implicit now() means the
           same inputs give different bands on different days.

    D10 modules hold a ref VERSION + timestamp, never a copy   (SPEC I8)
        <- metrology, made executable
        <- fixes the ORIGINAL seam. reference_version() fingerprints primary;
           changing a channel or volatility class changes the string; every
           peripheral inside its interval flips to FREE_RUNNING. The pull comes
           due because the reference MOVED, not because a timer expired. (T6)

    D11 entrain() re-reads the reference; does NOT overwrite readings
        <- circadian: light resets phase, it does not dictate what each tissue
           then does
        <- prevents mistaking re-entrainment for correction. Pulling a module
           back means it re-reads the standard, not that a coordinator rewrote
           its answer.

## STILL OPEN — decide before assuming

    O1  fourth band NOT_APPLICABLE. An all-NA target currently reads
        UNDETERMINED, conflating "don't know if it still reads" with "nothing
        could stop it reading." Different repairs. SPEC section 7 forbids
        building it until decided — do not let it get assumed into existence.

    O2  efference-copy axis: did the referent move, or the observer/instrument?
        Not a decay channel. May be a fourth mesh axis or a clock input.

    O3  co-reference window: when are two readings "about the same referent
        state"? parity assumes same subject = same state. For a volatile
        referent, two readings hours apart may not be. Derive from volatility.

    O4  mutual-information echo continuum: parity kinds are discrete
        (same/diff digest). Partial input overlap still lands as "different."

## READING ORDER FOR THE BUILDER

    1. this file — LINEAGE + D0      (why three axes exist at all)
    2. SPEC section 1                (hard invariants)
    3. SPEC section 6                (divlog -> entrain -> syndrome -> wire in)
    4. back here for D1..D11         (as each piece is implemented)
    5. STILL OPEN                    (before touching anything it names)
