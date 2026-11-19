# Boundary cases: one neutral example each (2026-11-19)

The six cases in the owner's message of 2026-11-19 (`as_received/mode_and_authority_2026-11-19.md`, item 4). Names are neutral: none comes from the packet, which `instrument/test_instrument.py` checks for the fixture files. Four cases already have a fixture with a stipulated answer under a stated rule. The other two have no rule in any file. For those, the example is laid out and the answer is given under each candidate rule (branched, per `../MODE_SEQUENCE.md`), with no fixture written: a fixture would have to pick one rule.

| # | case | example | answer | where |
|---|---|---|---|---|
| 1 | field present everywhere, populated only on the target | target instances carry `note="x"`, `note="y"`; every other term's instances carry `note=None` | TAG by presence: NO. TAG by applicability: YES. | fixture M01-KA-07 (`instrument/fixtures/m01_known_answer.json`) |
| 2 | documented-only field, no instances | `sounding` named in prose, on no instance | TAG: NO by the fixture rule, UNRESOLVED by `validate.py` (the two disagree: CF18). INDEPENDENCE: UNRESOLVED. | fixture M01-KA-05 |
| 3 | two records built beside one another | `LOG` (the term's own record) and `SLIP`, both built on one reporting path | own-record rule: `LOG`. All-reporting-path rule: `LOG`, `SLIP`. | fixtures M02-KA-03, M02-KA-02 |
| 4 | wrapper around the term-bearing record | `BOX.items` holds `CORE` | counted only under FIRST_WRAPPER_ONLY: `CORE`, `BOX` | fixture M02-KA-04 |
| 5 | two different records both satisfy "own record" | `TALLY` with `phase="X"` and `NOTICE` with `sort="X"`, both built when term X is reported | **no rule.** Under "the first record built": the one built first. Under "every record whose status/kind/verdict/state value is X" (M02 D1's sentence read as plural): both. Under "the record the reporting function returns": the returned one. | not a fixture; KC08 (T12, two record types) |
| 6 | outer aggregate report | `SUMMARY.rows` holds many `TALLY` records, one of them for X | **no rule.** Outer report excluded: `TALLY` only. Outer report included as a wrapper: `TALLY`, `SUMMARY`. Outer report included only if built on X's own call: depends on the call graph. | not a fixture; KC10, GR08, GR18 (G3) |

Cases 5 and 6 are definition gaps G2 and G3 (`GAPS.md`). Under `../MODE_SEQUENCE.md` they go to SUGGEST. Where evidence cannot pick a rule, the branches stay, and a reading is scored under each.
