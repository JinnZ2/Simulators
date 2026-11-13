# reasoning-toolkit

CC0. Co-authored. Markdown only, no code.

Design basis: the card format and the provenance density were requested by the user
(operator, 2026-11-13).

`CARDS.md` holds the cards. Each card has six fields: measures, fits, method, breaks
(breaks when), warning (warning sign it's breaking) and link. Each card also carries a
provenance line and a status line.

## Status

- PROPOSED: no worked instance is in this repository.
- OBSERVED: this repository holds a worked case the card was applied to. An `instance` line names it.

## Cards

| # | card | status | provenance |
|---|---|---|---|
| 1 | distribution check | PROPOSED | chat-side, verbatim |
| 2 | fill-source tag | PROPOSED | chat-side, verbatim |
| 3 | claim-vs-method | PROPOSED | Claude Code, 2026-11-13 |
| 4 | channel-loss map | PROPOSED | Claude Code, 2026-11-13 |
| 5 | frame check | PROPOSED | Claude Code, 2026-11-13 |
| 6 | label-tracks-valve | OBSERVED | Claude Code, 2026-11-13 |
| 7 | symptom vs cause feeds | PROPOSED | Claude Code, 2026-11-13 |
| 8 | parallax by rotation | PROPOSED | Claude Code, 2026-11-13 |
| 9 | entangled variable | OBSERVED | Claude Code, 2026-11-13 |
| 10 | author familiarity | PROPOSED | Claude Code, 2026-11-13 |
| 11 | carrier spread | OBSERVED | Claude Code, 2026-11-13 |
| 12 | source swap | PROPOSED | chat-side voice session, fields Claude Code, 2026-11-13 |
| 13 | gate regeneration | PROPOSED | chat-side voice session, fields Claude Code, 2026-11-13 |
| 14 | ontology before pathology | PROPOSED | chat-side voice session, fields Claude Code, 2026-11-13 |
| 15 | echo check | PROPOSED | chat-side voice session, fields Claude Code, 2026-11-13 |
| 16 | critical-facility cloud dependency audit | PROPOSED | chat-side, verbatim |

Tests: T-source and T-band, both PROPOSED and not run, under `## Tests` in `CARDS.md`.

## Not here

Five earlier cards are not in this repository: missing-wand, constraint reasoning,
carried reference, anchor-switching and position-as-frame-event. Their text is not in
the repository anywhere, so they were not added and not reconstructed.

## Index

Each card has a row in `TOOL_FINDER/entries.py`, with aliases and a symptom. Rebuild the
index with `python3 TOOL_FINDER/build_finder.py`. The measures and breaks quotes in those
rows are checked as literal substrings of `CARDS.md`. Cards carry no check command, so
their status in the index is NOT_RUN.

## Related

- `configuration-record/`: a schema and validator for one AI configuration record, with roles derived from positions at t.
