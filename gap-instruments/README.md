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
`to_dict`/`from_dict`). It ships without the PROPOSED example instances.

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
```

## Neighbours

`gap-register/` (marked unmeasured quantities) and `gap-markers/` (a register
of gap locations) share the word "gap" and are different instruments. This
one records evidence status per field; neither of those does.
