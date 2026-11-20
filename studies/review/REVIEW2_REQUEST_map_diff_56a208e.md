# REVIEW-2 request: the map diff at 56a208e

Status: DRAFT, not sent. Written 2026-11-20 by the session that made the diff (L0).
Tail item, not a gate: the freeze lift record of 2026-11-20 does not wait on it, and nothing is
ordered from the return. The reviewer must be a different model family from the writer (Claude
Code).

Why it exists: the `covers` lists and the two added locations in `concept_map.json` were written
by the implementer after the REVIEW-2 of GPT-6 (`REVIEW2_in_map_GPT6_2026-11-20.md`). The
mechanical recheck (28 of 28 YES) reads those lists; no second reader has read them.

```
MODE: REVIEW-2

The two READ files are attached to this conversation. Use the attachments; don't fetch the
repository.

READ:
  studies/review/map_diff_148031b_56a208e.diff
      sha256 7458a757906caa3535a9b5103bd5dc514b288816ff78444b405a2b90198fa844
      git diff 148031b 56a208e -- concept_map.json build_multi_home_register.py check_concept_map.py
  studies/review/MULTI_HOME_REGISTER_for_review_2026-11-20_v2.json
      sha256 934771a52bc0be9ee29b438cf03f5752a3ccf93af86e20f438db88377a34eb1f
      28 rows; each row: concept, homes (repo:path@sha, blob)

SCOPE: the diff only.
  a) covers lists on six rows: L0 gate (budget closure); known-answer / null harness;
     anchor / return; UNKNOWN expiry; percolation; branching.
  b) two added locations: study-aperture experimental/playground/validation/planted_defects.py
     (on known-answer / null harness) and study-aperture
     experimental/playground/detection/non_detection.py (on scoped absence
     (ABSENT_AT_SENSITIVITY), with a covers entry for "non-detection as bounded null").
  c) the strict rule text in build_multi_home_register.py (docstring and strict_in_map):
     YES = one map row names the concept in concept or covers AND lists every registered home.
  Judge from the attached files only; mark GUESS where a line cannot be judged without the homes.

QUESTIONS:
  1. Per covers entry (12 entries): is the register concept named exactly as in the register,
     and does the row it sits on list every home the register gives for it?
     Return: entry | row | EXACT / NOT_EXACT | homes ALL / MISSING (which) | reason
  2. Per added location (2): is it the path the register gives as a home of the concept named
     in its note? Return: path | MATCH / NO_MATCH | reason
  3. Rule text: does strict_in_map do what the docstring sentence says? Name any case where
     the two differ. Return: SAME / DIFFERS | the case
  4. Anything in the diff outside a), b), c)? List it; do not judge it.
  - Do not edit any file. Do not return a total score. Do not say whether an umbrella row and
    a register concept are the same concept; that is outside the scope.

EXPOSURE ATTESTATION (return it filled in):
  model family and version:
  memory on / off:
  files read, with links or attachment names:
  anything else fetched (yes / no, what):
  prior exposure to this map, this register, or REVIEW2_in_map_GPT6_2026-11-20.md (yes / no, what):
  anything relayed by the owner about expected answers (yes / no, what):
  sha256 verified by the reviewer (yes / no):
```

Blob ids, for a reviewer who cannot hash the bytes:

- `studies/review/MULTI_HOME_REGISTER_for_review_2026-11-20_v2.json` at `7366f50`: `26af8dfabeb36d245ec85d432ca4d00e15afb226`
- `concept_map.json` at `148031b`: `e121c1d136167d0363d0a7d453d13e64a2bdb8a0`; at `56a208e`: `f241c8acd9070e1d282d7201ea1a69adc52bba8b`
- `build_multi_home_register.py` at `56a208e`: `0f9b3da8804430783fee8f7a3e4d9a3587469066`
- the diff file: its blob id is the one in the commit that adds this request.

Limit: the register copy carries homes as of `2fd67dd`; the register in the tree was rebuilt at
`56a208e` against newer sibling tips. The diff does not change any register home.

Observer slots: null.
