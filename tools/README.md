# tools

Note 2026-11-09: README created by WORK ORDER TOOL FINDER part 1 because this
directory had none. It holds only the Finds-by section(s) below; the tool's own
text is in the files beside it.

## Finds-by (ALIAS_PROPOSED, 2026-11-09): sourced
Note 2026-11-09: added by WORK ORDER TOOL FINDER part 1; aliases derived from this
tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.

- value must carry its source text
- verify an extracted value against its span
- provenance gate for parsed numbers
- refuse a value with no source
- span check
- avoided term: AVOIDED_TERM_UNSTATED
- measures: "Three fields on every extracted value: the VALUE, the LITERAL SOURCE TEXT it came from, and the LOCATOR -- which document, which line, which columns."
- breaks when: NO_STATED_LIMITS

## Finds-by (ALIAS_PROPOSED, 2026-11-09): provenance_marker
Note 2026-11-09: added by WORK ORDER TOOL FINDER part 1; aliases derived from this
tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.

- record that a tool was run and with what hash
- tool run ledger
- did this tool run before
- stamp a tool with its last check
- avoided term: AVOIDED_TERM_UNSTATED
- measures: "One marker per run of a tool, appended to a ledger."
- breaks when: NO_STATED_LIMITS

## Finds-by (ALIAS_PROPOSED, 2026-11-09): check_term_collision
Note 2026-11-09: added by WORK ORDER TOOL FINDER part 1; aliases derived from this
tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.

- same phrase two meanings
- which sense of a term is declared
- term collision finder
- avoided term: AVOIDED_TERM_UNSTATED
- measures: "who uses the colliding terms, and who declares which sense."
- breaks when: NO_STATED_LIMITS

## Finds-by (ALIAS_PROPOSED, 2026-11-09): known_answer
Note 2026-11-09: added by WORK ORDER TOOL FINDER part 1; aliases derived from this
tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.

- test a metric on a fixed known case
- metric sanity check
- known-answer registry
- avoided term: AVOIDED_TERM_UNSTATED
- measures: "No metric ships without a known-answer run."
- breaks when: NO_STATED_LIMITS

## Tested (append-only; never overwrite an older line): channel_chain
tested: 2026-11-09 | model: WITHHELD (session rule: no model identifier is written into a pushed artifact; the operator holds it) | Claude Code, cloud session (claude.ai/code) | channel_chain.py --selftest 12/12
tested: 2026-11-09 | commit 98ecd8f | Claude Code, cloud session (claude.ai/code) | model: see trailer | channel_chain.py --selftest 12/12

## Finds-by (ALIAS_PROPOSED, 2026-11-17): check_cards / TOOL_CARDS
Note 2026-11-17: added with the TOOL_CARDS index; aliases derived from this tool's
stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md` (entry `tool-cards`).

- one row per tool with where it lives and its hash
- is this tool pinned to a merged commit
- tool on an unmerged branch
- card for a tool built in another repository
- find a tool card by a phrase
- which tools are not built yet
- avoided term: registry
- reason: a registry reads as the place the tools live; "A map, not a move: the code stays in the repository it was built in."
- measures: "A map, not a move: the code stays in the repository it was built in."
- breaks when: "every location it can reach and says NOT_CHECKED, never OK, for one it cannot."

`TOOL_CARDS.json` is the source; `TOOL_CARDS.md` is rendered by `python3 tools/check_cards.py --write`.
A row is pinned to a merged commit and the sha256 of the file there; a row on an unmerged branch
reads PENDING_MERGE with its PR number and is re-pinned on merge. Sibling checkouts are looked for
at `../formula-audit` and `../geometric-to-binary-computational-bridge` (override with
`CARDS_<REPO>_PATH`); without them those rows read NOT_CHECKED.

