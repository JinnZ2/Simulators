# Definition gaps (G list)

Gaps where the study text does not settle a definition, so readers must choose. Named by the owner (2026-11-19) in the order they were raised; a gap stays open until the owner decides it, and none is decided here. Each row lists the confusion rows that bear on it. Grok rows are cited by their filed ids (`confusion/2026-11-19_grok_m01-m02.md`, GR01-GR18).

| gap | question | rows | status |
|---|---|---|---|
| G1 | what "defined on every instance" means for TAG: present, populated, required, or present-or-required (key a1's reading); and how a documented-only field with no instance is read | KC01, KC02, KC03, KC05; CF11; GR09, GR10 | open |
| G2 | which record is a term's "own record" when the term is not a status / kind / verdict / state value (a class-typed term, a record concept, a class-less reserved string), or when one event builds two records | KC06, KC07, KC08, KC09; GR03, GR04, GR05, GR06 | open |
| G3 | where a reporting path starts and stops: whether a record built beside the term's own record, a wrapper, or an outer aggregate report counts | KC10, KC11 (fixture side drafted in PR #320); GR05, GR08, GR18 | open |
| G4 | void: not named in any message received in this session | void | void |
| G5 | predicate sameness across projects: when two terms from different projects share a label but are governed by different rules, what makes their predicates "the same" for clustering | GR07, GR12 | open |

What "confirmed by two readers" means here: two readers stopped or guessed at the same point independently. It shows the text leaves the point open; it does not say which reading is right.

## Later (2026-11-19): after filing the Grok record

The Grok rows were first cited from the owner's summary. Read against the filed rows: GR09 (are the four keys tied to this term only) and GR10 belong to G1, not G2; GR07 (same label, different rules) belongs to G5 with GR12, not with KC08; GR05 bears on G3 as well as G2. The table above now cites the filed rows.

## Later (2026-11-19): independence levels

Under the owner's independence rules (`../MODE_SEQUENCE.md`, dated section), the Kimi (KC) and Grok (GR) reviewers are both L2: different families, both exposed to the implementation (`INDEPENDENCE_LEDGER.md`). Where they converge (G2, G3), the agreement counts once, at L2, not as two independent confirmations. The sentence above ("two readers stopped or guessed at the same point independently") is kept as written; "independently" there means two different sessions, not L3.
