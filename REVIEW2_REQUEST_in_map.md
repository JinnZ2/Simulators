# REVIEW-2 request: in_map on the multi-home register

Status: DRAFT, not sent. Drafted 2026-11-20 by the builder of the map rows (L0). Amended 2026-11-20: READ now points
at the stripped register (no in_map fields) and concept_map.json at 2fd67dd; the field list is "concept, homes". The reviewer
must be a different model family from the builder (Claude Code).

```
MODE: REVIEW-2

READ:
  studies/review/MULTI_HOME_REGISTER_for_review_2026-11-20.json
      sha256 2a2ae5a04a5075b88f80c5bab285de8f69a8b4dda37e0031bd087416a9bf9308
      28 rows; read per row: concept, homes (repo:path@sha, blob)
  concept_map.json (Simulators @ 2fd67dd3202d22bc34e06befc6648932d752b924)
      sha256 aecd39f4d4ac7c2e4beed7904bfd4c8116dbf3c18895510de7a692482939e1e6
      28 rows; each row: concept, home, status, locations
  Read the files at the homes only where a row cannot be judged without them.
  Do not read FREEZE_CLEANUP_MEASURAND.md, CONCEPT_MAP.md or build_multi_home_register.py
  before returning: they carry the builder's readings.

QUESTION, per register concept (28):
  Does concept_map.json hold a row that covers this concept at these homes?

RETURN, one line per concept:
  concept | in_map YES / PARTIAL / NO | map row read as covering it (or none) | reason
  - YES: one map row names the concept and lists every home.
  - PARTIAL: a map row lists the homes, or some of them, and does not name the concept;
    or it names the concept and lacks a home.
  - NO: no map row covers it.
  - Mark any line that is a guess: GUESS.
  - Where two map rows could cover one concept, name both.
  - Where a register row looks like two concepts, or two rows look like one, say so.
    Do not merge or split them.
  - Do not edit either file. Do not return a total score.

EXPOSURE ATTESTATION (return it filled in):
  model family and version:
  files read, with the commit:
  files from the do-not-read list seen before returning (yes / no, which):
  prior exposure to this register, this map, or the builder's in_map readings (yes / no, what):
  anything relayed by the owner about expected answers (yes / no, what):
```

Builder's readings, for comparison AFTER the return only: `MULTI_HOME_REGISTER.json` field
`in_map` (YES 25, PARTIAL 3, NO 0 at this commit).
