# WORK ORDER — return_path.py

CC0. Stdlib only. No network. Phone-buildable.

## What it does

Scores a proposed or existing correction channel against four requirements.
Returns the SET of requirements failed. Does not rank channels, does not
recommend, does not resolve.

It does NOT ask whether a channel is useful. A channel can be valuable and
still not be a return path. Marking a gap is not correcting an error.

## Why the four requirements

A system whose drive rate greatly exceeds the relaxation time of whatever
checks it cannot self-correct — structurally, regardless of quality. The
correction has to arrive from something with a relaxation time attached to
physical consequence. A return path is that channel.

Each requirement removes one known failure mode:

1. RECEIPT — if the fast side decides whether to receive it, it is a
   recommendation channel. Recommendation channels are already known to fail
   (findings implemented piecemeal or arbitrarily). Must be enforced by
   structure, the way a load rating is enforced by the beam and not by the
   engineer's agreement.

2. SIGNAL — a report is re-encoded by whoever writes it, which reintroduces
   the valuation seam. Each re-encoding is a place the signal can be
   revalued. Count the encodings.

3. LATENCY — a correction arriving after the error is load-bearing downstream
   documents rather than corrects. Latency is scored against the rate at
   which output gets built on, not against a clock.

4. CONSTRUCTION — a return path prices the fast side's errors back to the fast
   side. Nobody builds a mechanism whose only function is to impose costs on
   its builder. So it must be constructible by the party already paying,
   without the other party's cooperation.

## Intake — structured only, no prose parsing

```
channel = {
  "channel_id": str,

  "receipt": "MANDATORY" | "ELECTIVE" | "UNSPECIFIED",
      # MANDATORY   = receiving party cannot decline or ignore
      # ELECTIVE    = receiving party chooses
      # UNSPECIFIED = not stated; scored as ELECTIVE, flagged separately

  "signal_encodings": int,
      # 0 = physical consequence arrives directly
      # 1 = one report written by an observer
      # 2+ = report of a report

  "encoder_position": "SLOW_SIDE" | "FAST_SIDE" | "THIRD_PARTY" | "NONE",
      # NONE only valid when signal_encodings == 0

  "latency": float,          # time from error to signal arrival
  "build_on_time": float,    # time from output to that output being built on
  "time_unit": str,          # both above in the same unit; recorded, not converted

  "construction": "SLOW_SIDE_ONLY" | "REQUIRES_FAST_SIDE" | "REQUIRES_THIRD_PARTY",

  "scope_note": str          # free text, NOT parsed, carried into output
}
```

No field may be inferred. Absent field returns `INTAKE_INCOMPLETE` naming the
field. The instrument does not guess.

## Checks

```
C1_RECEIPT      fires if receipt != "MANDATORY"
C2_SIGNAL       fires if signal_encodings > 0
C3_LATENCY      fires if latency >= build_on_time
C4_CONSTRUCTION fires if construction != "SLOW_SIDE_ONLY"
```

Additional non-scoring flags, reported alongside:

```
F_UNSPECIFIED_RECEIPT   receipt was "UNSPECIFIED" (scored as ELECTIVE)
F_FAST_SIDE_ENCODER     encoder_position == "FAST_SIDE" with encodings > 0
                        (the party being corrected writes the correction)
F_RATIO                 latency / build_on_time, always reported as a number
```

## Return

```
{
  "channel_id": str,
  "failed": [list of fired check codes],     # empty list = graded
  "flags": [list of fired flag codes],
  "ratio": float,
  "grade": "RETURN_PATH_GRADED" | "NOT_A_RETURN_PATH",
  "scope_note": str
}
```

`grade` is `RETURN_PATH_GRADED` if and only if `failed` is empty.

The set is the output. Do not collapse it to a score. Which requirement fails
determines what would have to change, and a single number destroys that.

## Validation cases — the build is wrong if any of these come out otherwise

**A — direct physical consequence.** A load fails under an unrated part;
the failure arrives at the operator, unwritten, at the moment of failure.
receipt MANDATORY, encodings 0, encoder NONE, latency << build_on_time,
construction SLOW_SIDE_ONLY.
→ MUST return `RETURN_PATH_GRADED`, empty failed set.
If the instrument cannot pass this, it passes nothing, and an instrument
that grades nothing is not a diagnostic.

**B — fast, well-run, ignorable.** An incident reporting system with
same-day turnaround that the receiving party may decline to act on.
→ MUST fail C1 ONLY. Tests that the checks are independent and that speed
does not compensate for elective receipt.

**C — the 1–2 year anonymous publication loop.** Gaps posted, carried by
crawlers, published later, statistics read back.
→ MUST fail C1 and C3. Should pass C4.
This case exists to keep the instrument honest about a channel already in
use. Failing here is not a verdict on the loop's value — the loop marks
gaps, and marking is not correcting.

**D — field observation against a corpus claim.** Long-baseline direct
observation of a behaviour the published record describes differently;
no channel exists from the observation to the claim.
→ MUST fail C1, C3, C4. C2 depends on whether a report is written.
Worked instance available: abort-rate decay in wildlife encountering
unknowns, where the corpus holds the pre-decay model as current.

**E — FALSIFIER, must not pass.** Any channel where the party being corrected
writes the correction. Set encoder_position FAST_SIDE, encodings 1, everything
else ideal.
→ MUST fail C2 and raise F_FAST_SIDE_ENCODER.
If ideal values on the other three carry this to a pass, the instrument has
renamed compliance.

## Hard constraints

- No field named or derived from: institution, authority, credential, venue,
  reach, audience size, or reputation of either party.
- No field scoring the CONTENT of the correction. This instrument rates the
  channel, not the claim travelling on it. A channel carrying a wrong
  correction is still a return path; a channel carrying a right one that
  nobody must receive is not.
- `scope_note` is carried through verbatim and never parsed.
- Latency and build_on_time are recorded in whatever unit the submitter used.
  No conversion, no default, no "fast" or "slow" as a value anywhere in the
  schema — both times or no rating.

## Open, not resolved in this spec

- `build_on_time` is the hardest field to source honestly. In most systems
  nobody measures when output starts being built on. Where it is unknown the
  correct return is `INTAKE_INCOMPLETE`, not an estimate. Expect this to be
  the most common return, and treat that as a finding about the system rather
  than a defect in the instrument.
