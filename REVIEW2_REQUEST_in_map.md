# REVIEW-2 request: in_map on the multi-home register

Status: DRAFT, not sent. Drafted 2026-11-20 by the builder of the map rows (L0). Amended 2026-11-20: READ now points
at the stripped register (no in_map fields) and concept_map.json at 2fd67dd; the field list is "concept, homes".
Amended again 2026-11-20: READ points at the v2 register copy (concept and homes only) and a stripped copy of the
map (field `added` removed); see studies/review/README.md. The reviewer
must be a different model family from the builder (Claude Code).

```
MODE: REVIEW-2

The two READ files are attached to this conversation; their sha256 values are listed below. Use the
attachments; don't fetch the repository.

READ:
  studies/review/MULTI_HOME_REGISTER_for_review_2026-11-20_v2.json
      sha256 934771a52bc0be9ee29b438cf03f5752a3ccf93af86e20f438db88377a34eb1f
      28 rows; each row: concept, homes (repo:path@sha, blob)
  studies/review/concept_map_for_review_2026-11-20.json
      sha256 6604b93ea0f74578a60da2b64d78ff2eac10adc9c2b88f2de7ee75d60df6799d
      concept_map.json @ 2fd67dd3202d22bc34e06befc6648932d752b924 with one field removed
      28 rows; each row: concept, home, status, locations
  Read the files at the homes only where a row cannot be judged without them.
  Do not read, before returning: MULTI_HOME_REGISTER.json, concept_map.json, CONCEPT_MAP.md,
  FREEZE_CLEANUP_MEASURAND.md, build_multi_home_register.py, REVIEW2_REQUEST_in_map.md,
  studies/review/README.md, studies/review/MULTI_HOME_REGISTER_for_review_2026-11-20.json.
  They carry the builder's readings.

QUESTION, per register concept (28):
  Does the map copy (concept_map_for_review_2026-11-20.json) hold a row that covers this
  concept at these homes?

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

Carry steps (owner, 2026-11-20):
1. Open both download links and save the files.
   - https://raw.githubusercontent.com/JinnZ2/Simulators/7366f505be38cf1163219ea10296050e64fbe767/studies/review/MULTI_HOME_REGISTER_for_review_2026-11-20_v2.json
   - https://raw.githubusercontent.com/JinnZ2/Simulators/7366f505be38cf1163219ea10296050e64fbe767/studies/review/concept_map_for_review_2026-11-20.json
2. Start a new Kimi or GPT conversation with memory off.
3. Attach both files, then paste the block above (it opens with the attachment line).
4. Bring back its answer: 28 lines plus the filled-in attestation.
