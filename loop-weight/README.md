# loop-weight

Source-relevance weighting on **feedback-loop structure** instead of standing.

CC0. Python 3, stdlib only. No network. Phone-buildable.
Run `python3 loop_weight.py` for the case table, `python3 test_loop.py` for the checks.

---

## MEASURAND

For a source reporting on a system: **how much information about that system
the report can carry.**

Not whether the source is right. Not whether anyone agrees. What the path
between the thing and the report is physically able to deliver.

---

## THE THREE QUANTITIES

```
      the system                                      the report
          |                                                ^
          |   L hops                                       |
          v                                                |
   [action/decision] --hop--> [obs] --hop--> [relay] --> [source]
                          \       \              \
                           R        R              R        per-hop retention
                           |
                           +--- C : does the reading map to the thing at all?
                                    measured OUTSIDE the loop, never from inside it
```

| | symbol | what it measures | units | failure it catches |
|---|---|---|---|---|
| 1 | `L` | hops between the action and the observation | int >= 0 | distance |
| 2 | `R` | fraction surviving each hop, **per hop** | 0.0-1.0 or `None` | attenuation |
| 3 | `C` | whether the reading maps to the thing | 0.0-1.0 or `None` | pointing at the wrong thing |

`L` is topology. `R` is channel. `C` is aim.

**They are never combined.** No function returns one number standing in for
all three. In particular `R` is never raised to the power of `L`: a cumulative
retention figure fuses the channel with the topology and destroys the
disagreement between them, which is the whole reading.

They disagree, and the disagreement is the signal:

```
short loop + lossy channel      carries less than    long loop + clean channel
one hop + never checked         carries less than    four hops + scored
```

---

## C — THE CONSTRAINED TERM

`C` is the term everything turns on and the only one that cannot be read
from inside the loop. **Two admissible derivations, both implemented.**

```
C-1  DISAGREEMENT
     divergence against >=1 independent instrument on the same referent.
     - independence ASSERTED per pair and stored
     - a pair sharing a hop with the source is EXCLUDED whatever the
       assertion says, and the contradicted assertion is reported
     - others sharing a hop with EACH OTHER are one instrument, not N
       (union-find over hop ids; class means, then the mean of classes)

C-2  OUT-OF-FRAME OUTCOME
     prior predictions scored against outcomes the source did not
     define, select, or time, stated before resolution.
     - any of defined_by / selected_by / timed_by naming the source
       excludes that prediction
     - no timestamp before resolution excludes it

neither available  ->  C = None, return is UNCALIBRATED
                       NOT a default. NOT an imputed mean. NOT zero.
```

**C is never self-reported.** An input whose `supplied_by` is the source, or
whose provenance is unstated, raises `SelfSuppliedRefused` at load — refused,
not silently dropped.

**Both derivations landing:** both values are reported, `C` takes the lower
(`[CHOICE 5]`), and a gap wider than `derivation_gap` is flagged. A
calibration established by one check and refuted by another is not
established. The asymmetry is real and stated rather than hidden: C-1 failing
may mean the peers are wrong, not the source, so both values stay in the
record for a reader who takes the other view.

---

## RETURNS

```
                     C established high   C established low   C not established
  L short                SHORT_CALIBRATED   SHORT_MISCALIBRATED  SHORT_UNCALIBRATED
  L long                 LONG_CALIBRATED    LONG_MISCALIBRATED   LONG_UNCALIBRATED

  any hop below the retention floor   ->  LOSSY          (dominates regardless of L)
  path not described                  ->  INSUFFICIENT   (L unmeasured; no read)
```

`SHORT_UNCALIBRATED` is the confident-wrong case: a one-hop instrument that is
always wrong reports no noise **within its own frame**, and nothing in `L` or
`R` can detect it.

`UNCALIBRATED` and `MISCALIBRATED` are separate returns and stay separate in
every comparison. Unmeasured is not low.

All eight members are reachable, one per case, asserted by the test. A
declared member no path populates is a defect: a reader cannot tell *no such
case was found* from *nobody looked*.

---

## THE ORDERING — a rule, not a score

`carries_more(first, second)` returns one of
`FIRST_CARRIES_MORE / SECOND_CARRIES_MORE / INCOMPARABLE`, the rule that
decided, and the per-axis comparison. **No number is produced at any point,
and `INCOMPARABLE` is a first-class result.**

```
1. either side INSUFFICIENT            -> INCOMPARABLE   unmeasured_path
2. calibration is a PRECONDITION, not a term:
     established-high vs anything else -> the established one   calibration_established
     established-low vs not-established-> INCOMPARABLE   known_low_vs_unknown
3. carrying channel vs LOSSY           -> the carrying one      channel_carries
4. same calibration and channel state  -> Pareto on L (lower is more)
                                          and R (higher is more)
     no dominance                      -> INCOMPARABLE   no_dominance
```

Step 2 is what stops a short loop from becoming the new credential.
Step 2's third line is what stops a measured-bad instrument and an unmeasured
one from being put on one scale.

---

## WHY CALIBRATION COMES FIRST — and why `L` and `R` still matter

`C` is an **end-to-end measurement of the whole path**. C-2 scores what the
source actually delivered, after every hop has already taken its cut, so an
established `C` has already priced the topology and the channel together.

`L` and `R` are **structural descriptions** of that path. They predict what it
can deliver. They are what you have when nobody has ever checked what it did
deliver — which is most of the time.

```
C established   ->  the path was measured.    supersedes the description of it.
C unavailable   ->  the path was described.   L and R are the whole reading.
```

That is why calibration sits above `L` and `R` in the ordering rather than
beside them, and it is not a weighting: a measurement outranks a prediction of
the same quantity.

**The limit, stated:** `C` is established on reports the source has already
made. Carrying it forward assumes the path has not changed since. This
instrument cannot check that, and a source whose loop was cut last week still
reads CALIBRATED here.

---

## PASS CONDITION — the A/C falsifier

```
CASE A   one hop, no independent instrument, no scored predictions
         -> SHORT_UNCALIBRATED

CASE C   four hops, each a documented verbatim relay, C established by C-2
         -> LONG_CALIBRATED

PASS iff   carries_more(C, A) == FIRST_CARRIES_MORE
           AND the deciding rule is calibration_established
           AND A's loop is genuinely the shorter one
```

**If the implementation cannot produce C carrying more than A, the instrument
has rebuilt an authority claim with "short loop" as the new credential and
fails.** The test asserts the rule and not only the direction, so the
condition cannot be met by accident on another axis.

Two further falsifiers from the same case set:

```
CASE D   two hops, hop 2 at 0.20      -> LOSSY, though D's loop is shorter than C's
CASE I   three comparisons, two of them through one shared wire
         counted as three: mean 0.700, clears the floor  -> would read CALIBRATED
         counted as two classes: mean 0.600              -> reads MISCALIBRATED
```

Case I exists so the rule that correlated instruments count once can be shown
to change a verdict rather than only to be stated.

---

## WHAT IS REFUSED

```
- no scalar collapse
- no field named or derived from: standing, office, tenure, employer,
  works-cited count, listener count, where a thing was printed
  test_loop.py walks the AST of both code files and checks every identifier
  and dict key against that set. It is NOT a substring scan over the raw
  file: this README and the module both have to be able to NAME what they
  refuse, and a substring scan fires on the sentence saying so. The checker
  is null-tested on a plant, so its silence means something.
- no L inferred from source kind, occupation or domain. Counted from the
  described path or INSUFFICIENT.
- no database of sources, no registry of people, no ordered list
- no tie-breaker resolving to how many say the same thing. Correlated
  sources sharing a hop are one instrument, not N.
```

---

## PARAMETERS

Declared, defaulted, overridable, and printed in every record.

```
short_at_or_below      1      [CHOICE 1]  L <= this is SHORT
lossy_below            0.5    [CHOICE 2]  any single hop below this -> LOSSY
calibrated_at_or_above 0.7    [CHOICE 3]  C at or above this is established-high
derivation_gap         0.2    [CHOICE 4]  C-1 vs C-2 gap worth printing
```

The work order sets none of these. Every verdict in `samples/` is a verdict
under these four numbers and moves if they move.

---

## STATE

Ten hand-built cases, all CONSTRUCTED, none a measurement of any real source
and no real person, employer or publication named anywhere. Nothing here has
been run against a real report; the case set exercises the instrument, it
does not measure anything. The check count is printed by `python3 test_loop.py` rather than stored here.

Expected verdicts live in the test file, not in `cases.py`, so no case can
agree with the module by construction.

---

## FILES

```
loop_weight.py   module + DECLARATION
cases.py         10 hand-built cases + 2 refused-at-load
test_loop.py     the checks, stdlib only, no pytest
samples/         one pinned run
CLAIM_TABLE.md   LW_001..LW_010 with falsifiers
WORK_ORDER.md    delivered verbatim
```
