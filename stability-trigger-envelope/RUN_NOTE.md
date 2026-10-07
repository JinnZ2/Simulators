# RUN_NOTE — every choice the order left open

The work order fixes the fields, the verdicts and the fixtures. It does not
fix the arithmetic between them. Each choice below is a decision this build
made, stated with what it costs and what would change it, so a later reader
can disagree with a named choice rather than with the whole folder.

---

## CHOICE 1 — onset timing replaces the phase window

**The order says**, in section 6: `thresholds (amplitude ratio, phase window)
in a data file`.

**Built instead:** onset timing. First exceedance of each body's amplitude
envelope, plus the lag at maximum cross-correlation of the two envelopes
within one forcing period of the event. There is no phase window and nothing
in `classify()` reads a phase.

**Why, and it is not a preference.** The same operator issued a later
instruction, after a finding in a sibling repository
(`Noise-as-Information-Sensor`, `tools/`, claim `NC_013`): a phase lead taken
from a cross-correlation of two periodic traces is fixed only **modulo one
period**. A cab leading the trailer by exactly one curve reversal and a cab
leading by nothing produce the same correlation peak. The case predicts a
lead of about one reversal — so a phase reading is blind at precisely the
value this instrument exists to read. In that sibling the defect was measured
rather than argued: a constructed lag of 4 samples in a 40-sample period came
back from the raw search as a lead of 36, and the sign of that lead was
deciding a verdict.

**The order is not edited to match.** `WORK_ORDER.md` is landed verbatim with
the phase wording intact, and this note records that one item in it is
superseded by its own author's later instruction. A work order quietly
rewritten to agree with the build is a work order that can no longer be used
to check the build.

**What it costs.** Onset needs an EVENT. A steady oscillation has a flat
envelope and no onset to time, so `onset()` returns `NO_RISE` and the verdict
falls back to amplitude alone. Phase would have had something to say there
and would have been wrong; this has nothing to say and says so. The three
onset states are kept apart for that reason — `MEASURED`, `NO_EVENT`
(nothing moved), `NO_RISE` (already moving when the record started) — because
they call for different next actions and only one of them is a measurement.

**Checked behaviourally, not asserted.** `test_envelope.py` builds two cab
traces with the same envelope and carriers half a period apart, and requires
the verdict, the agreement and the onset lead to be identical across them. It
then runs the same lag function on the raw traces and requires that number to
move. If a phase reading were still in the decision path the first assertion
fails.

---

## CHOICE 2 — traces are passed in memory, not as files

The order's field list names `cab_imu_file` and `trailer_imu_file`. The
record carries `cab_imu` and `trailer_imu` holding trace records instead.

**Why.** A path is a promise about a file format nobody has specified. There
is no IMU file format in this folder, no parser for one, and no sample file
to write a parser against, so a field holding a filename would be a field
holding a string nothing reads. When T1 produces real logs the format is
decided then, and a loader is one function.

**Cost.** A record cannot currently be round-tripped to disk. Nothing in the
folder needs that yet, and the moment T1 runs it will.

---

## CHOICE 3 — the reading envelope is the reader's, not the vehicle's

`OUT_OF_ENVELOPE` fires on a surface or grade outside what the READER
declares it can handle. It is not the vehicle's validation envelope, which is
what T2 and T5 measure and what neither has measured.

**The trap avoided.** A folder about a validation envelope that also emits
`OUT_OF_ENVELOPE` invites the reading that the instrument has determined the
vehicle is outside its envelope. It has determined nothing of the kind. The
verdict's reason string says which range it means, every time.

**Snow and ice are excluded, and that is a refusal rather than a finding.**
V5 says the margin is gone and the sensor degrades there. Excluding those
surfaces says this reader cannot reach the case that matters most, not that
nothing happens there.

---

## CHOICE 4 — onset is relative to each body's own peak

`onset_frac` is a fraction of the body's OWN peak envelope, not an absolute
level.

**Why.** Onset then measures WHEN a body started, never how much it moved.
Size is the amplitude ratio's job. An absolute threshold merges the two, and
a large late body and a small early one report the same.

**Cost.** A body that barely moves still gets an onset, as long as its
envelope rises. The `onset_variance_floor` is the only thing keeping a
trace's own noise from being timed as an arrival, and that floor is a
placeholder with nothing measured behind it.

**A second cost, found on the sibling side and NOT repaired here
(2026-09-27).** `envelope_window_frac` is 0.25, a quarter of the forcing
period. A moving RMS over a window shorter than the carrier period is not
stationary — over a quarter period of a sine it swings between roughly 0.43
and 0.90 of the amplitude — so where two bodies start at different carrier
phases the first-exceedance index can jitter by up to a quarter period, and a
SUB-PERIOD lead can read with the wrong sign. Every lead in F1–F9 is zero or
exactly one reversal, so the carrier phase at onset is identical on both bodies
and the defect is unreached rather than absent. `Noise-as-Information-Sensor`
`tools/two_body_source.py` sets its window to one full period for this reason
and records it as `NC_023`, DERIVED and UNTESTED — the session that found it
could not execute. The value here is left at 0.25 because changing a threshold
without a run behind it is the retune this folder refuses; the append-only
chain is where a measured value would land.

---

## CHOICE 5 — the forcing period is derived, not declared

`period_s = duration / curve_reversals`, from fields the record already
carries.

**Cost.** It assumes the reversals are evenly spaced across the descent. On a
real serpentine they are not. An unevenly spaced descent gives a period that
is right on average and wrong locally, which widens the envelope window in
some places and narrows it in others. A per-reversal timestamp list would fix
it and is not in the order's field set.

---

## CHOICE 6 — a gap in a trace refuses rather than interpolating

**Why.** An interpolated sample is a number the instrument made up, and onset
timing is exactly the quantity a made-up sample moves. The refusal names the
gap counts on both traces.

**Cost.** One dropped sample anywhere in a descent voids the whole record. A
gap-aware onset that works on the intact segment around the event is the
better instrument and is not built.

---

## CHOICE 7 — no composite, anywhere

`relocation_tally()` returns counts by event and by access bin, and
`score: None` with the refusal stated in the return. No function in the
module returns a single number summarising a record or a set.

**Why.** A relocation index would repeat the move that lost orders 2-4 in the
first place: several different costs collapsed into one number, which can
then be compared against a safety score built from different terms over a
different denominator.

---

## CHOICE 8 — expectations live in the test, not in the fixtures

`cases.py` carries no expected verdict for the classifier. `FIXTURES` holds a
label for the render, and every assertion lives in `test_envelope.py`.

**Why.** A fixture carrying its own expected answer can be made to agree with
the instrument by editing either one, and nothing shows which moved.

---

## What is NOT built, as typed absence

```
NOT_RUN            every one of T1-T6. No descent, no IMU, no vehicle, no
                   shop tool, no vendor, no fleet.

RENDER_UNOBSERVED  test_envelope.py has run once (217 checks, 0 failed,
                   2026-09-27) after being written without a runner.
                   descent_record.py's render path -- main() and the three
                   render_* formatters -- has not been executed. See README
                   STATE and ESP_010 for the sequence.

NOT_BUILT          a loader for real IMU logs (CHOICE 2)
                   a clock-synchronisation procedure for two phones (T1)
                   the T4 join against state crash records
                   a gap-aware onset (CHOICE 6)
                   any treatment of FAULT B -- see TESTS.md, last section

NAMED_AND_ABSENT   driver_hours_evidence_register.py and its
                   TRUST_PROTOCOL.machine_side_rule, cited in the order's
                   cross-links, are not in this repository. Carried as a
                   pointer, not reconstructed.

UNREAD             all four sources in section 8. Carried at SECONDARY from
                   the order; none retrieved, read or checked here, and no
                   claim in this folder rests on any of them.

REFUSED            no field for the operator, the carrier, the unit, or for
                   how anyone drove. Not an omission -- the schema is the
                   guarantee and the test reads the field names.
```
