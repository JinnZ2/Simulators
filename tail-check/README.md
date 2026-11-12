# tail-check

Was an inference about a person SAID by them, or FILLED from somewhere else?
And when it was filled, did the person's own words already place them off the
population center on that axis?

CC0. Stdlib only, parses under 3.8, phone-runnable. Co-authored (JinnZ2 +
Claude), 2026-11-09, built to WORK ORDER TOOL FINDER + GAP BUILDS part 3b.

```
inference + axis + claimed words + user turns
      |
      v
claimed is a literal span of a user turn?  (tools/sourced.py find_span + gate)
      |-- yes --> SAID     (span + turn reported)
      |-- no  --> FILLED   (content did not come from what the person said)
      '-- input incomplete --> UNRATED (never a pass, never FILLED by default)

FILLED + a sourced user statement on the SAME axis declared off_center
      --> flag MEDIAN_FILL_RISK
```

## Run

```sh
python3 tail-check/tail_check.py tail-check/samples/demo.json
python3 tail-check/tail_check.py FILE --json
python3 tail-check/selftest.py
```

## Scope limits

- A span is literal: case-sensitive substring after whitespace strip. A
  paraphrase of what the person said reads FILLED.
- `position` (off_center / at_center) is a DECLARATION carried with its
  `declared_by`. Nothing here reads text to place a person on an axis.
- FILLED says where content did not come from, not that it is false.
- The span logic is imported from `../tools/sourced.py`, not copied.
- Demo numbers and turns are ILLUSTRATIVE; no person is described.


## Channel chain (Amendment A1, 2026-11-09)

SAID means "a span of the user turns as supplied", never "the person said it"
directly. Each result is a `tools/channel_chain.py` record (Cross-Domain-Toolkit
`SubstrateReading` field names plus a per-hop chain).

| hop | known deviation sources | known-reference check |
|---|---|---|
| sensor | typo, dictation substitution | caller only |
| encoding | ASR, smart quotes / unicode, whitespace | caller; `observed: "AUTO"` looks for the injected string in the turns |
| transmission | truncation on export, turn order, role mislabel | caller; `AUTO` sentinel (type a known string, confirm it arrives intact) |
| decoding | literal span rule, case | built in, every run: one known present span, one known absent |
| inference | claimed words may not be what the inference rests on | caller only |

A hop with no check reads `UNVERIFIED_HOP` and is named in the render. The
chain class is `VIA_CHECKED_CHAIN`, `VIA_UNVERIFIED_HOP` or `VIA_FAILED_HOP`;
there is no DIRECT class.

## Finds-by (ALIAS_PROPOSED, 2026-11-09)
Note 2026-11-09: added by WORK ORDER TOOL FINDER part 1; aliases derived from this
tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.

- did the person actually say this
- inference about the user vs what the user stated
- filled-in assumption about a person
- median or default assumption applied to an outlier user
- quote check against user turns
- avoided term: AVOIDED_TERM_UNSTATED
- measures: "Was an inference about a person SAID by them, or FILLED from somewhere else?"
- breaks when: "A span is literal: case-sensitive substring after whitespace strip. A paraphrase of what the person said reads FILLED."

## Tested (append-only; never overwrite an older line)
tested: 2026-11-09 | model: WITHHELD (session rule: no model identifier is written into a pushed artifact; the operator holds it) | Claude Code, cloud session (claude.ai/code) | selftest.py 26/26
tested: 2026-11-09 | commit 98ecd8f | Claude Code, cloud session (claude.ai/code) | model: see trailer | selftest.py 26/26
