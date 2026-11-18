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
| 17 | AI sensor index (spin-up card) | PROPOSED | chat-side, verbatim |
| 18 | missing-wand protocol | PROPOSED | chat-side, verbatim (landed 2026-11-17) |
| 19 | constraint reasoning | PROPOSED | chat-side, verbatim (landed 2026-11-17) |
| 20 | carried reference / cross-site alignment | PROPOSED | chat-side, verbatim (landed 2026-11-17) |
| 21 | anchor-switching | PROPOSED | chat-side, verbatim (landed 2026-11-17) |
| 22 | position as frame event | PROPOSED | chat-side, verbatim (landed 2026-11-17) |

Tests: T-source and T-band, both PROPOSED and not run, under `## Tests` in `CARDS.md`.

## Landed later

Five earlier cards were named here as absent on 2026-11-13 because their text was in no
repository: missing-wand, constraint reasoning, carried reference, anchor-switching and
position-as-frame-event. The operator delivered their text on 2026-11-17 and they are now
cards 18 to 22, verbatim. Three of them do not carry all six fields of the card format; a
field a card does not carry is left absent, not filled in.

## Index

Each card has a row in `TOOL_FINDER/entries.py`, with aliases and a symptom. Rebuild the
index with `python3 TOOL_FINDER/build_finder.py`. The measures and breaks quotes in those
rows are checked as literal substrings of `CARDS.md`. Cards carry no check command, so
their status in the index is NOT_RUN.

## Related

- `configuration-record/`: a schema and validator for one AI configuration record, with roles derived from positions at t.
