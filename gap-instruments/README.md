# gap-instruments

CC0. Python standard library only. Co-authored.

Notation for evidence about coordination systems, physical limits, discrepancies
and abstentions. **Records evidence. Assigns no verdict.** Validation checks
record completeness and internal consistency only, never whether evidence is
true.

```text
python3 gap_instruments.py                 # demo templates + GAP summary
python3 gap_instruments.py --claim "..."   # five-axis question template
python3 gap_instruments.py --json          # demo records as JSON
python3 gap_instruments.py --selftest
```

## What is here

```text
gap_instruments.py                      working copy: supplied text + eight marked fixes
                                        + three additions A1-A3 (2026-10-27)
source/gap_instruments.as_supplied.py   delivered 2026-10-25, verbatim
source/gating_diagnostic.as_supplied.py delivered 2026-10-25, verbatim (merged into the above)
source/PINS.sha256                      sha256 of both supplied files
samples/                                demo, --json, --claim and --selftest output
```

The supplied files are kept byte for byte. The working copy is a correction
beside its original, not a replacement for it. Every change in it carries a
`Note 2026-10-25 (Fn)` comment.

Copies elsewhere, all byte-identical to `gap_instruments.py`:

```text
Simulators/tools/gap_instruments.py
method-layer/tools/gap_instruments.py
```

`method-layer/gap_instruments.py` is a different file: the same instrument
reshaped to method-layer's conventions (str Enums, frozen records,
`to_dict`/`from_dict`). It ships without the PROPOSED example instances,
and it does not carry A1-A3: the work order names the four modes of this
form (report, `--claim`, `--json`, `--selftest`), and the reshaped form has
`--claim` only.

## Fixes applied (F1-F8)

```text
id  site                     supplied behaviour                          fixed behaviour
--  -----------------------  ------------------------------------------  ----------------------------------------
F1  Abstention               only the literal "GAP" counted as not        "", whitespace and "GAP" all count as
                             reasoned; "" passed as reasoned              not reasoned
F2  Abstention               abstention_type vocabulary was a comment;   checked against ABSTENTION_TYPES
                             "made_up" passed
F3  CoordinationSystem       an axis key outside AXES was accepted and   reported as "axis not in AXES"
                             silently ignored (typo "ancor")
F4  gap_summary              a missing axis was not counted, so          NOT_RECORDED counted and included in the
                             leaving axes out raised filled_fraction     total (1 of 5 axes recorded: 0.333 -> 0.143)
                             (1 of 5 recorded read 0.333)
F5  DiscrepancyRecord        tested-vs-candidate branch did nothing      tested explanations not among the
                             (`pass`)                                    candidates are reported
F6  PhysicalLimitRecord      "replace: ..." placeholders read as         counted as unspecified, like "specify" in
                             specified                                   instance_of
F7  InstanceChange           empty label accepted                        reported
F8  main                     --claim with no text ran the demo           usage on stderr, exit 2
```

The selftest keeps every supplied assertion and adds one check per fix, plus
a negative case showing a correctly filled Abstention passes clean.

## Additions 2026-10-27 (A1-A3)

Work order "gap_instruments.py extension". Every existing behaviour is kept
and the selftest keeps every prior assertion. Each change is marked
`Note 2026-10-27 (An)`.

```text
id  what                       rule
--  -------------------------  ----------------------------------------------
A1  PhysicalLimitRecord        limit_basis: physical_bound | empirical_rule |
    .limit_basis               unknown (default). "unknown" is one GAP in
                               gap_summary and is named by gap_fields(); the
                               report prints the basis. A value outside the
                               three is reported by validate().
A2  CalibrationRecord          predict, then measure. target_match first; a
                               mismatch is TARGET_MISMATCH, logged, not an
                               error, not a miss, and enters no MAE. Outcome
                               (HIT / MISS) and method_matches_standard are
                               separate fields, never combined.
    calibration_summary        n, hits, misses, target mismatches, not scored,
                               method counts kept apart, and per quantity
                               n / scored / MAE as a (least, greatest) band.
                               A quantity with no numeric scored row reads
                               None, never 0.
A2r CalibrationRecord          operator correction, same day: error has a
    .safe_side                 direction. OVER | UNDER | SYMMETRIC | UNSTATED
                               (default; scored symmetric and reported). Under
                               OVER an overestimate of any size is a HIT and its
                               size is the realized buffer (signed_error, mean
                               signed error per quantity); an underestimate
                               beyond tolerance is a MISS.
A3  ConfoundRecord             name, present (True | False | "UNKNOWN"), size
                               (Evidence or None), control_used,
                               interpretation (default GAP). An
                               interpretation with no control is reported;
                               present without a size is reported.
```

The only change to existing output is the one A1 mandates: the demo
PHYSICAL LIMIT reads `GAP: 8` where it read 7, plus the `limit_basis` line.
`--claim` output is byte-identical. `--json` gains five keys after the
existing five.

### Seed run

```text
record            target           outcome     signed     safe      method
----------------  ---------------  ----------  ---------  --------  ----------
CAL-MILES-GPS     TARGET_MISMATCH  NOT_SCORED  --         OVER      NOT_TESTED
CAL-MILES-ACTUAL  MATCH            HIT         0 to +1    OVER      NOT_TESTED
CAL-FUEL          MATCH            HIT         --         UNSTATED  NO (categorical)
CAL-TIME          MATCH            HIT         +0.9667    OVER      NOT_TESTED

summary   n 4, hits 3, target mismatches 1
MAE       miles 0-1 (one row), on-duty time 0.9667, fuel None (categorical)
signed    miles 0 to +1, on-duty time +0.9667: both overestimates, the buffer
LIMIT-EAST-2026   limit_basis empirical_rule; not in gap_fields
confounds 12 seeded; target_mismatch present, size 2.7-3.7 mi, meaning GAP
```

The operator's correction (2026-10-27), entered as stated: a driver relying on
gauges, dashboard and GPS adds buffer for each instrument's deviation plus
environment, construction, traffic and road wear, and overestimating still
arrives on time where underestimating does not. The trip rows carry goal
"arrive on time", safe_side OVER and that buffer. The fuel row states neither
and is left UNSTATED.

The three dictated verdicts (miles vs actual hit, fuel hit, time hit) and the
miles-vs-GPS mismatch come out of the rules. They are the verdicts the rules
were checked against, so the seed is a regression fixture and not an
independent check.

### Choices the order left open

```text
id      choice                                      cost
------  ------------------------------------------  ---------------------------
A2-1    instrument_quantity added: the quantity     a field beyond the order's
        the instrument measured. instrument_scope   list
        also carries edges, so it cannot be the
        thing target_match compares
A2-2    target_match = equality after case and      two names for one quantity
        whitespace normalisation                    read as a mismatch
A2-3    tolerance declared, else half a unit in     scored symmetric, the time
        the last written digit; a leading "~"       HIT rested on it (a MISS at
        doubles it                                  +/-0.5); under OVER it rests
                                                    on direction, and the "~"
                                                    only widens the costly side
A2-4    "14:02" read as minutes:seconds             CONFIRMED by the operator
                                                    2026-10-27
A2-5    HIT when some value the measurement         a range measurement scores
        allows is within tolerance (low end of      on its nearest end
        the band)
A2-6    the standard method is the instrument's     fuel: inferred from memory
        own reading                                 = NO, outcome still HIT
A2-7    safe_side is declared, never inferred from  a goal whose wording names a
        the goal's wording. OVER: HIT unless short  direction still scores
        of every value the measurement allows by    symmetric until safe_side is
        more than the tolerance                     written
A3-1    the target_mismatch confound is logged      its meaning stays GAP: no
        present, sized from the two miles rows      control separates anything
```

The A2 docstring carries the baseline note as supplied (Barkan, Black &
Sourbut 2025; GPT-4 technical report 2023). Neither was checked here.

## Recorded, not repaired

```text
- "externality literature; cite" passes as a source. The word "cite" says a
  citation is owed. Detecting that is a word list (paraphrase steps around
  it), so it is noted rather than enforced.
- GAP means two things in the docstring: "no stable anchor" and "nothing
  recorded". F4 separates them only for missing axes; an Evidence() left at
  its GAP default still cannot say which it is.
- The four merged physical-limit files (physical_bounds.py, limit_detection.py,
  physical_limits_suite.py, physical_discrepancy.py) are in neither
  repository. The merge's inputs are not in the record; only its output is.
- gating_diagnostic.py's sharpest defect (compare() printing a never-recorded
  axis as [GAP]) does not carry over: the merged module has no compare().
  F4 is the same distinction applied to gap_summary.
- Every example instance (token-anchored system, Chrysler 1979-80, TARP 2008,
  "DeepSeek draft" sources) is PROPOSED and carried as delivered. None was
  checked against a source here.
- A1: limit_basis has no source slot. Declaring `physical_bound` with no
  support repeats the error the field exists to catch, and nothing checks it.
- A2: the seed states no confidence, so confidence against hit rate reads
  NOT_COMPUTABLE. No goal is stated either; both read UNRESOLVED rather than
  being filled in.
- A2: the miles reference "actual ~29-30" names no instrument. It is entered
  ESTIMATED from the dictation.
- The EAST 2026 figures (1.3-1.65 x the Greenwald limit) and the two
  calibration citations are carried as supplied and were not checked; the
  publisher hosts are outside this environment's egress allowlist.
```

## Neighbours

`gap-register/` (marked unmeasured quantities) and `gap-markers/` (a register
of gap locations) share the word "gap" and are different instruments. This
one records evidence status per field; neither of those does.
