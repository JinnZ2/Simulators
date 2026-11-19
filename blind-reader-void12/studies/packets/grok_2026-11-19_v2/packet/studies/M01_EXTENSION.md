# M01 extension: new readings, two arms, a D1 condition (fixed before any instrument code or new reading)

Written 2026-11-19. Extends `M01_CRITERIA.md` (pinned in `[commit]`), which stays in force for the three filed D0 readings. Design taken from a reader's proposal ((not included), filed as received), with the changes listed in section 5.

## 1. Conditions

```text
D0   the v2 packet and brief, unchanged (v2 variant A unless the owner states B)
D1   D0 plus conditions/M01_D1.md: the TAG and INDEPENDENCE wording of (not included),
     marked experimental, cited with a status note in an excluded file
```

D1 readings are their own pool. They are never pooled with D0, never scored as v2 readings toward (not included) rules 1 and 2, and never used to change a key.

## 2. Arms

- **Parallel.** Different readers, assigned to D0 or D1 before the task. Each sees one condition. Estimates the effect of the wording without carryover.
- **Sequential.** One reader does D0 then D1, or D1 then D0, order counterbalanced. Estimates within-reader change. A second session from one reader is a repeated observation, not a new reader; it is analysed by reader id and position, and the reader is asked whether they recalled or reused their earlier answer.
- **Assignment** is written down before the task (reader pseudonym, family, arm, condition, order). Pseudonyms only; no names or account details in the data.

## 3. Coding

New readings are coded with `M01_SCHEMA.json` and the rules of `M01_CRITERIA.md` sections 3 and 4, unchanged. Under D1 the reader may state TAG / INDEPENDENCE judgements; those are READER_STATED. Under D0 they are never asked, so any TAG / INDEPENDENCE value on a D0 record is CODER_INFERRED or null. **No reader choice is ever rejected by the instrument for disagreeing with the comparison key's rule**; the instrument records, it does not score.

## 4. Known-answer fixtures

Synthetic cases with stipulated answers, used to check that the instrument can represent each case, not to decide any real case. Given to a separate cohort, or to the same readers only after their real-source responses are locked; stored apart from real-source records. A failed fixture means the instrument or instructions failed it; it never justifies changing a reader's real-source record. Fixtures use neutral names, none from the packet.

## 5. Changes from the proposal as received

```text
proposal                                          here, and why
------------------------------------------------  ---------------------------------------------------------
validator rejects included=true unless TAG=YES     dropped: it would reject the D0 behaviour under study
  and INDEPENDENCE=YES                             ([a result from the filed readings, withheld])
required booleans ambiguity_detected,              nullable; null = NOT_RECORDED (silence is not "no")
  alternatives_preserved
no provenance on values                            every value carries READER_STATED / CODER_INFERRED /
                                                   SCRIPT_DERIVED / NOT_RECORDED, as in M01
fixture G02-KA-02 uses the packet's real field     rewritten with neutral names; as received it attached an
  names (Reading + error / exception_type /        answer to a real term
  missing_path)
fixture G01-KA-05 "declared only" puts the field   rewritten: the declared-only field appears on no instance
  on every instance
tests never load the fixture files                 the tests load and check every fixture
[row withheld: it concerns the status of a file not included]
ids G01 / G02                                      M01 / M02 (G01-G33 are a reader's gap inventory)
```

## 6. What is reported

As `M01_CRITERIA.md` section 5, by condition and arm, plus: per field, the D0 vs D1 listing rate (parallel arm); per reader, D0-to-D1 transitions (sequential arm, by order). Counts only; no threshold, no majority answer, no composite score.
