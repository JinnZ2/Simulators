# T1-T6 — the tests, as design text

Cheapest first. None has been run. Each carries what it needs, what it
predicts, and what would refute the fault it addresses; a test with no stated
falsifier is a demonstration, not a test.

Two of the six (T4, T5) end in a join or a disclosure that nobody here can
make, and they say so rather than being written as though the data were one
query away.

---

## T1 — PAIRED IMU, one descent

```
addresses   FAULT A  (measured body != at-risk body)
needs       two phones, one on the cab, one on the trailer
            phone GPS for grade
cost        one descent
```

Log both IMUs across one serpentine descent with the trigger timestamp
recorded. Feed the pair to `descent_record.classify()`.

```
PREDICTS    cab amplitude >> trailer amplitude
            cab leads the trailer by about one curve reversal
            trailer quiet at the trigger timestamp
```

```
FALSIFIER A   trailer roll high whenever the trigger fires
              -> FAULT A is void for this unit
```

**What T1 does not establish.** It compares the cab against the trailer. It
does not compare a phone against the OEM sensor, and nothing in it says the
OEM sensor read what the phone read. A phone on a cab mount and a sensor
bolted to a frame cross-member are two different instruments on two different
parts of the same body.

**The measurement to get right.** The two loggers must be on one clock to
better than the declared tolerance, or the lead between them is a lead
between the phones. `classify()` refuses the pair rather than reporting it
when the offset is too large, which turns a silent error into a visible
refusal — but the refusal costs the run, so synchronise first. No procedure
for that is written here, and writing one is the cheapest unbuilt piece in
this folder.

---

## T2 — TRIGGER-ONSET SPEED per named grade

```
addresses   FAULT C  (baseline offset on a descent)
            and produces the measured edge of the validation envelope
needs       the T1 rig, and repeats
cost        several descents per grade
```

The speed at which a correctly driven rig trips the trigger, per named grade,
repeated. `descent_record.envelope_edge()` returns it with a spread, or
`INSUFFICIENT_RUNS` below three runs with a trigger.

```
FALSIFIER C   onset speed independent of grade and bank
              -> FAULT C is void
```

**Runs where nothing fires are kept.** A descent at 40 mph with no trigger
bounds the edge from below, and dropping it leaves the edge looking tighter
than the data supports. `envelope_edge()` reports those speeds beside the
edge and never inside it.

**The word "correctly".** T2 says a correctly driven rig, and nothing in this
folder defines or measures that. It is the one place the design asks for a
judgement about driving, and it is the operator's to make and to declare per
run. No field records it and none should: a driving-quality column is the
column that turns this instrument into a scoring instrument.

---

## T3 — EVENT-LOG AUDIT

```
addresses   FAULT C, and the UNREAD in the provenance block
needs       a shop diagnostic tool
cost        one shop visit
```

Does a logged roll intervention carry a bank or grade estimate, or only raw
lateral acceleration? Does it log trailer state at all?

```
REPORT      fields present / fields absent
```

That is the whole output. It is a field inventory and not a verdict, because
the interesting result is an absence: a log with no trailer field cannot be
asked whether the trailer was moving, however many interventions it holds.

```
NOT PREDICTED   whether the controller estimates grade or bank. That is
                proprietary and UNREAD, and T3 reads the log rather than
                the controller. A log that carries a bank estimate shows
                one exists; a log that does not, shows nothing either way.
```

---

## T4 — RELOCATION COUNT

```
addresses   ORDERS 2-4  (the cost the safety score does not see)
needs       the T1 log, plus state crash records
cost        the join, which is the hard part
join status UNMEASURED
```

Field `downstream_event` per descent — `none | pass | near_miss | incident |
closure` — then join slowdown segments against state crash records filtered
to horse-drawn vehicles on the same segments.

`descent_record.relocation_tally()` does the first half: counts by event and
by access-road bin, reported separately and summed into nothing.

```
THE JOIN IS NOT BUILT AND IS NOT COSTED HERE.  Two records that were never
designed to be joined: a per-descent log kept by one operator, and a state
crash file whose segment geometry, date granularity and reporting threshold
are all unknown from here. Whether the join is possible at all is the first
finding T4 would produce.
```

**Why the tally refuses a composite.** Collapsing queue length, passes, near
misses and closures into one relocation index would repeat the move that lost
orders 2-4 in the first place — a single number that can then be compared
against a safety score built a different way, from different terms, over a
different denominator.

---

## T5 — VALIDATION COVERAGE

```
addresses   the envelope question directly
needs       vendor disclosure
cost        an ask, and an answer that may not come
status      UNMEASURED
```

Score corridors on V1-V5, then ask whether the validation sets include
high-V corridors.

```
V1  grade x curve-reversal rate      trigger envelope
V2  access-road count to the drop    closure trap
V3  alternate-route distance         reroute cost
V4  slow or vulnerable users present passing hazard
V5  winter surface duration          sensor degradation, margin gone
```

The V-scores are computable now from public road geometry; the second half is
not computable at all without a disclosure nobody is obliged to make. Those
two halves are recorded apart, because a corridor scored high on V1-V5 with
no answer about validation coverage is an open question and reads too easily
as a finding.

**Region-independence is the point.** The same dynamics are reported across
several corridors by the same operator (N=1). V1-V5 are written to be scored
anywhere, so a second operator in a different region can score their own
corridor without adopting anything about this case.

---

## T6 — SCORING-RULE DISPLACEMENT

```
addresses   ORDER 1  (a sensor-triggered event docked as a driver event)
needs       fleet telematics
cost        access nobody here has
status      UNMEASURED
```

Speed on flagged grades before versus after a policy of docking
sensor-triggered events, and queue length where it can be measured.

```
PREDICTS    speed on flagged grades falls after the docking policy
            (the avoidance in ORDER 2, as a measurable)
```

```
FALSIFIER   speed unchanged across the policy change
            -> the avoidance is not driven by the scoring rule, and
               ORDER 2's mechanism needs another explanation
```

**The confound, stated before the test.** Anything else changing at the same
time as the policy — weather, a route change, a different trailer, a
different season — moves the same number. A before-and-after on one fleet
with one policy change is n=1 on the thing that matters, and T6 as written
cannot separate the policy from whatever else moved with it. A second fleet
that did not adopt the policy over the same period is the control, and
nothing in this design has one.

---

## What none of the six does

```
- none measures FAULT B. The inverted-response claim is about what braking
  does to a combination mid-reversal, and testing it means commanding a
  brake application on a descent, which is not a test anyone should run on a
  public road with a loaded trailer. No bench or simulation version is
  specified here. FAULT B is the best-argued and least-tested of the three.
- none establishes that any intervention caused any crash. The claim
  throughout is an unrecorded risk path, not a causal chain.
- none of T1, T2, T3 needs more than one operator. T4, T5 and T6 all need a
  party this folder does not have -- a state records office, a vendor, a
  fleet -- and that is the shape of the whole case: the cheap tests are the
  ones about the vehicle, and the expensive ones are about the record.
```
