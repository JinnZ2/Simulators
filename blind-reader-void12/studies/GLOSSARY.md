# Glossary: one line per term, and the path where it is defined

For a reader who has only the reports. Paths are relative to `blind-reader-void12/`. A term marked **open** is a decision the owner has not made; no file defines it yet. Written 2026-11-19, after the chat session's confusion record (`confusion/2026-11-19_claude-chat_m01-m02.md`, rows CH04-CH09) showed the reports assumed their reader had the files.

## The experiment

| term | one line | defined in |
|---|---|---|
| VOID-12 | the question whether a reader who has not seen the first reading groups 15 terms from three projects the same way | `PREREG.md` "What is being tested" |
| the packet | what a reader gets: 15 terms, eight source files, a brief, a response template | `reader_packet_v2/` (v2); `reader_packet/` (v1, retired) |
| T01-T15 | the 15 terms under neutral ids, fixed shuffled order | `reader_packet_v2/terms.json` |
| the brief | the reader's instructions | `reader_packet_v2/READER_BRIEF.md` |
| variant A / B | brief as written / brief without the clause "even if the second system attaches different extra fields or detail" | A: `reader_packet_v2/READER_BRIEF.md`; B: `variants/READER_BRIEF.v2.variant_B.md`; `PREREG.md` "Packet v2" |
| task text (work order) | the message that sent the packet to a reader; its rule 4 set the label `claude-fresh-1` | `readings/WORK_ORDER_2026-11-19_as_received.md` |
| `slots_specific` | fields the source ties to one term and no other | brief, "Slots"; `PREREG.md` "Packet v2" |
| `slots_carried` | every named field of every record built or documented when the term is reported | brief, "Slots" |
| cluster / predicate | the reader's grouping; what a term records, in the reader's words | brief, "Definitions" |
| BLIND / UNCERTAIN / NOT_BLIND | status from attestation q1-q4: all no / any unsure, none yes / any yes | `PREREG.md` "Blindness is declared, not enforced" |
| family | the reader's model family; all Claude readers count as one family with the first reader | `PREREG.md` rules, rule 5 |
| rules 1-5 | how a pair is reader-confirmed, contested, confirmed | `PREREG.md` "Rules proposed for reading the results" |
| confirmation tier | which tier a confirmation counts on now that v2 has two slot meanings | **open** (owner) |

## Keys and scoring

| term | one line | defined in |
|---|---|---|
| the key | the first reading's groups, predicates and slot lists, compared against; not ground truth | `PREREG.md` "What is being tested"; `scoring/key_v2.json` |
| key v2 | the key for packet v2, both slot meanings | `scoring/key_v2.json`; `PREREG.md` "Packet v2" |
| key a1 | key v2 changed by amendment 1 (`slots_specific` of T08, T09, T10, T12) | `scoring/key_v2_a1.json` |
| amendment 1 | the rule, two owner rulings, N1, C1, ND and K1; **in force** (its line 3 is stale) | `KEY_V2_AMENDMENT_1.md`; status: `PREREG.md` "Status note on amendment 1" |
| TAG | defined on every instance of the term and on no instance of any other term | `KEY_V2_AMENDMENT_1.md` section 2 |
| INDEPENDENCE | an independent input of the record, not computed from other candidate fields | `KEY_V2_AMENDMENT_1.md` section 2 |
| S3-out | derived attributes are not slots (owner's decision) | `amendment_options/OPTIONS.md` section 6 |
| N1 / C1 / ND / K1 | strip `<>` and backticks / report the set relation / undetermined lists score n/d / how carried lists were derived | `KEY_V2_AMENDMENT_1.md` sections 4-5 |
| n/d | a key list the sources do not determine; neither match nor miss | `scoring/score_v2.py` docstring |
| MAPS / PARTIAL / HOMONYM / NONE | pair tiers: same cluster and equal slots / same cluster / different clusters, same label / neither | `scoring/score.py` lines 15-25, `tier()` |
| ARI | adjusted Rand index of the reader's grouping against the key's | `scoring/score.py` |
| `covers_effect` | an attribute computed on a scoped-absence token (limit <= effect size); excluded by S3-out | `reader_packet_v2/sources/Simulators/combined-playground/cplay/tokens.py` lines 17-18, 103 |
| HOLDS question | whether `HOLDS` (T11) groups with `CLOSED_WITHIN` (T14), with `OK` (T13), or alone; three readings, three answers | **open** (owner); readings in `readings/README.md` |
| `void_reason` question | whether TAG reads presence (key on every record) or applicability (populated on the term only) | **open** (owner); both computed in `studies/instrument/arms_report.txt` |

## Studies

| term | one line | defined in |
|---|---|---|
| M01 | which fields readers put in `slots_specific`, and why | `studies/M01_CRITERIA.md`, `M01_SCHEMA.json`, `M01_EXTENSION.md` |
| M02 | which records readers count for `slots_carried` (scope), and how far they open nested ones (traversal) | `studies/M02_CRITERIA.md`, `M02_SCHEMA.json` |
| D0 / D1 / D2 / D3 | brief unchanged / plus an experimental note (M01 D1: TAG and INDEPENDENCE; M02 D1: own record only; D2: every reporting-path record; D3: reader states its rule) | `studies/instructions/` |
| parallel / sequential arm | different readers per condition / one reader under two conditions, order counterbalanced | `studies/M01_EXTENSION.md` section 2 |
| cells A-G | M01's field classes: exclusive raw, computed, shared, documented only, parameter not stored, some instances only, two routes | `studies/M01_CRITERIA.md` section 3 |
| presence / applicability / requirement scope | key on the record / populated on the record / required by a rule, each for the term only or shared | `studies/M01_SCHEMA.json` |
| SCRIPT_DERIVED / CODER_INFERRED / READER_STATED / NOT_RECORDED | who set a value; NOT_RECORDED is null, never a default | `studies/M01_SCHEMA.json` |
| rule_on / rule_off | the GPT-6 proposal's validator rule applied as an analysis arm / the instrument as adopted | `studies/instrument/validate.py`, `arms.py` |
| known-answer fixtures (KA) | synthetic cases with stipulated answers, testing the instrument, deciding no real case; neutral names | `studies/instrument/fixtures/` |
| KA-07 | the fixture case for presence vs applicability; "the term" there is the fixture's own synthetic target, not a T-numbered term | `studies/instrument/fixtures/m01_known_answer.json` |
| mode / stage | BLIND, REVIEW, AUDIT, SUGGEST, IMPLEMENT, REVIEW-2, AUDIT-2; one per request, named in its header; authority sits in the mode, not in a person or a model | `MODE_SEQUENCE.md`; headers in `studies/REQUEST_HEADERS.md` |
| evidence status | what kind of evidence can close a confusion row (SOURCE_RUN_REQUIRED, SECOND_CODER_REQUIRED, DEFINITION_REQUIRED, ...); another reader's agreement is not one | `studies/OPEN_ROWS.md` |
| confusion record | one row per point a reader was unsure, guessed or stopped | `studies/CONFUSION_TEMPLATE.md`; records in `studies/confusion/` |

## Id families (so ids from different sources are not mixed up)

| ids | whose | where |
|---|---|---|
| F1-F15, Q1-Q15 | the combined spec's own findings and design questions, quoted in the sources | `reader_packet_v2/sources/Simulators/playground-crossrun/COMBINED_SPEC.lines_1-390.md` |
| G01-G33 | the GPT-6 reader's gap inventory | `readings/2026-11-19_gpt6-v2/followup_as_received.txt` |
| C01-C15 | the Kimi reader's branch inventory | `readings/2026-11-19_kimi-v2-A/followup_as_received.md` |
| CF01-CF17 | the Claude Code session's confusion record | `studies/confusion/2026-11-19_claude-code_m01-m02.md` |
| CH01-CH12 | the chat session's confusion record | `studies/confusion/2026-11-19_claude-chat_m01-m02.md` |
| KC01-KC13 | the Kimi reader's confusion record on the study material (its own ids C01-C12, which also name its earlier, different branch inventory) | `studies/confusion/2026-11-19_kimi_m01-m02.md` |
| GR01-GR18 | the Grok reader's confusion record on study-review packet v1 (its own numbers 1-18) | `studies/confusion/2026-11-19_grok_m01-m02.md` |
| P1-P6 | defects of the Grok study-review packet v1, fixed in the v2 draft | `studies/packets/grok_2026-11-19_v2/MANIFEST_PRIVATE.json` (`diff_from_v1`) |
| G1-G5 | definition gaps, each with its rows | `studies/GAPS.md` |
| F1-F7, E1-E7 | the Grok reader's repository read: seven claims, seven proposals | `studies/as_received/grok_repo_read_2026-11-19.md`; checked in `studies/GROK_REPO_READ_CHECK.md` |
| RR01-RR10 | residue register rows | `studies/RESIDUE_REGISTER.md` |
| M01, M02 | the studies (the GPT-6 proposal called them G01 / G02, which clashed with its own inventory) | `studies/` |
